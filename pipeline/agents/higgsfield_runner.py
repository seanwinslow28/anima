"""anima — Higgsfield image transport (decision D5, 2026-07-13).

The ratified transport for models whose vendor API anima deliberately does
not wire (today: gpt-image-2 -> the Higgsfield `gpt_image_2` job type).
Shape mirrors nb_pro_runner.invoke_image_edit: typed response envelope,
content-addressed cache, credential-free stub ladder. Dispatch into this
module happens inside nb_pro_runner.invoke_image_edit — callers never
import this directly.

D5 mitigations baked in (see docs/active/2026-07-13-transport-strategy-decision.md):
- EXPLICIT resolution + quality on every call (per-surface default drift
  swings cost 4-8x — CLI defaults 2k/high, MCP 1k/low; we never rely on
  either).
- Bounded retry on transient CLI/API failures (a real HTTP 502 hit the
  2026-07-13 probe mid-batch; failed jobs auto-refund credits).
- Immediate download (Higgsfield retains outputs ~7 days).
- Job-id + result-URL provenance sidecar per generation — the honest
  substitute for a served-model read-back Higgsfield does not offer.
- Auth is the human-run `higgsfield auth login` (cached token). The stub
  gate is CLI *presence*; a present-but-unauthenticated CLI surfaces as an
  errored (non-ok) response, never a silent stub.
"""

from __future__ import annotations

import fcntl
import hashlib
import json
import logging
import os
import re
import shutil
import subprocess
import tempfile
import time
import urllib.request
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Iterator

from pipeline.agents.nb_pro_runner import (
    UnwiredTransportError,
    _hash_file,
    _write_placeholder_png,
)
from pipeline.registers import GPT_IMAGE

_LOG = logging.getLogger("anima.higgsfield_runner")

# The transport map (D4/D5): honest vendor model id -> Higgsfield CLI job
# type. The registry keeps recording the vendor id; THIS map owns the
# routing. Exact allowlist, never a prefix — an unmapped model raises.
HIGGSFIELD_IMAGE_MODELS: dict[str, str] = {GPT_IMAGE: "gpt_image_2"}
PINNED_HIGGSFIELD_CLI_VERSION = "0.2.3"

_HIGGSFIELD_BIN = "higgsfield"
_MAX_ATTEMPTS = 3  # 1 call + 2 retries on transient failure
_TRANSIENT_SIGNALS = ("timeout", "temporarily")
_HTTP_5XX = re.compile(r"(?<!\d)5\d{2}(?!\d)")


class UnsupportedHiggsfieldCLIVersion(RuntimeError):
    pass


class PendingReceiptQuarantined(RuntimeError):
    def __init__(self, quarantine: Path, payload: dict, cause: OSError):
        self.quarantine = quarantine
        self.payload = payload
        self.cause = cause
        super().__init__(
            f"pending receipt write failed; charged job quarantined at "
            f"{quarantine}: {cause}"
        )


class MismatchedHiggsfieldJobIdentity(RuntimeError):
    def __init__(self, requested: str, observed: str):
        self.requested = requested
        self.observed = observed
        super().__init__(
            f"Higgsfield wait job ID mismatch: requested {requested}, "
            f"received {observed}"
        )


class PendingDurability(Enum):
    DURABLE_PENDING = "durable_pending"
    DURABLE_QUARANTINE = "durable_quarantine"
    NOT_DURABLE = "not_durable"


@contextmanager
def _cache_key_lock(lock_path: Path) -> Iterator[None]:
    """Serialize charged work and cache publication for one content key."""
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


@dataclass(frozen=True)
class HiggsfieldResponse:
    """Result envelope for one Higgsfield image generation. Field-compatible
    with nb_pro_runner.NBProResponse (ok/stub_fallback/cache_hit/cache_key/
    exit_code/output_path) so Cy/Flo call sites duck-type unchanged, plus
    the provenance fields Higgsfield's weak pinning makes load-bearing."""

    output_path: Path
    cache_key: str
    cache_hit: bool
    stub_fallback: bool = False
    exit_code: int = 0
    job_id: str | None = None
    result_url: str | None = None
    display_name: str | None = None
    cli_version: str | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and Path(self.output_path).exists()


@dataclass(frozen=True)
class PendingPersistenceResult:
    outcome: PendingDurability
    response: HiggsfieldResponse | None = None


def _compute_cache_key(
    *,
    prompt: str,
    reference_images: list[Path],
    cites_identity_rules: tuple[str, ...],
    reject_reason: str | None,
    model: str,
    job_type: str,
    resolution: str,
    quality: str,
    aspect_ratio: str | None,
) -> str:
    """SHA-256 over everything that determines the output. Unlike
    nb_pro_runner's key there is no None-elision back-compat concern —
    this is a new cache namespace, so every explicit param is always in."""
    h = hashlib.sha256()
    h.update(b"transport:higgsfield\n")
    for tag, val in (
        (b"prompt:", prompt),
        (b"model:", model),
        (b"job:", job_type),
        (b"res:", resolution),
        (b"q:", quality),
        (b"aspect:", aspect_ratio or ""),
        (b"reject:", reject_reason or ""),
    ):
        h.update(tag)
        h.update(val.encode("utf-8"))
        h.update(b"\n")
    h.update(b"rules:")
    for rule_id in sorted(cites_identity_rules):
        h.update(rule_id.encode("utf-8"))
        h.update(b",")
    h.update(b"\nrefs:")
    # Order is semantic: the live contract is anchor-first. Never sort.
    for index, path in enumerate(reference_images):
        rh = _hash_file(path)
        h.update(f"{index}:".encode("ascii"))
        h.update(rh.encode("utf-8"))
        h.update(b",")
    return h.hexdigest()


def _read_valid_provenance(
    sidecar: Path,
    *,
    model: str,
    job_type: str,
    resolution: str,
    quality: str,
    aspect_ratio: str | None,
) -> dict | None:
    try:
        payload = json.loads(sidecar.read_text())
    except (OSError, json.JSONDecodeError, ValueError):
        return None
    if not isinstance(payload, dict):
        return None
    required = {
        "transport", "vendor_model", "job_type", "quality", "resolution",
        "aspect_ratio", "job_id", "result_url", "display_name", "cli_version",
    }
    if not required.issubset(payload):
        return None
    expected = {
        "transport": "higgsfield",
        "vendor_model": model,
        "job_type": job_type,
        "quality": quality,
        "resolution": resolution,
        "aspect_ratio": aspect_ratio,
        "cli_version": PINNED_HIGGSFIELD_CLI_VERSION,
    }
    if any(payload.get(key) != value for key, value in expected.items()):
        return None
    if not isinstance(payload["result_url"], str):
        return None
    if payload["job_id"] is not None and not isinstance(payload["job_id"], str):
        return None
    if payload["display_name"] is not None and not isinstance(
        payload["display_name"], str
    ):
        return None
    return payload


def _read_valid_pending(
    pending: Path,
    *,
    cache_key: str,
    model: str,
    job_type: str,
    resolution: str,
    quality: str,
    aspect_ratio: str | None,
) -> dict | None:
    """Return a same-input charged-job receipt, or reject it fail-closed."""
    try:
        payload = json.loads(pending.read_text())
    except (OSError, json.JSONDecodeError, ValueError):
        return None
    if not isinstance(payload, dict):
        return None
    required = {
        "cache_key", "transport", "vendor_model", "job_type", "quality",
        "resolution", "aspect_ratio", "job_id", "result_url",
        "display_name", "cli_version",
    }
    if not required.issubset(payload):
        return None
    expected = {
        "cache_key": cache_key,
        "transport": "higgsfield",
        "vendor_model": model,
        "job_type": job_type,
        "quality": quality,
        "resolution": resolution,
        "aspect_ratio": aspect_ratio,
        "cli_version": PINNED_HIGGSFIELD_CLI_VERSION,
    }
    if any(payload.get(key) != value for key, value in expected.items()):
        return None
    for key in ("job_id", "result_url", "display_name"):
        if payload[key] is not None and not isinstance(payload[key], str):
            return None
    if payload["job_id"] is None and payload["result_url"] is None:
        return None
    return payload


def _fsync_directory(path: Path) -> None:
    directory_fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def _durable_unlink(path: Path) -> None:
    try:
        path.unlink()
    except FileNotFoundError:
        return
    _fsync_directory(path.parent)


def _atomic_write_json(path: Path, payload: dict) -> None:
    fd, staged_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.stem}.", suffix=".json.tmp"
    )
    staged = Path(staged_name)
    try:
        with os.fdopen(fd, "w") as handle:
            json.dump(payload, handle, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(staged, path)
        _fsync_directory(path.parent)
    finally:
        staged.unlink(missing_ok=True)


def _publish_create_intent(path: Path, payload: dict) -> None:
    """Durably publish the pre-charge marker before invoking create --wait."""
    fd, staged_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.stem}.", suffix=".json.tmp"
    )
    staged = Path(staged_name)
    try:
        with os.fdopen(fd, "w") as handle:
            json.dump(payload, handle, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(staged, path)
        _fsync_directory(path.parent)
    finally:
        staged.unlink(missing_ok=True)


def _durable_write_quarantine(path: Path, payload: dict, reason: str) -> None:
    """Independent low-level fallback when canonical atomic publication fails."""
    quarantined = dict(payload)
    quarantined["quarantine_reason"] = reason
    quarantined["operator_action"] = (
        "Inspect this charged-job receipt; restore it to .pending.json or "
        "remove it only after explicitly resolving the job."
    )
    staged = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    data = json.dumps(quarantined, indent=2).encode("utf-8")
    fd = os.open(staged, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb", closefd=False) as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(staged, path)
        _fsync_directory(path.parent)
    finally:
        os.close(fd)
        staged.unlink(missing_ok=True)


def _pending_payload(
    *,
    cache_key: str,
    model: str,
    job_type: str,
    resolution: str,
    quality: str,
    aspect_ratio: str | None,
    metadata: tuple[str | None, str | None, str | None],
    cli_version: str,
) -> dict:
    url, job_id, display_name = metadata
    return {
        "cache_key": cache_key,
        "transport": "higgsfield",
        "vendor_model": model,
        "job_type": job_type,
        "quality": quality,
        "resolution": resolution,
        "aspect_ratio": aspect_ratio,
        "job_id": job_id,
        "result_url": url,
        "display_name": display_name,
        "cli_version": cli_version,
    }


def _persist_pending(
    pending: Path,
    *,
    quarantine: Path,
    cache_key: str,
    model: str,
    job_type: str,
    resolution: str,
    quality: str,
    aspect_ratio: str | None,
    metadata: tuple[str | None, str | None, str | None],
    cli_version: str,
) -> dict | None:
    url, job_id, _ = metadata
    if url is None and job_id is None:
        return None
    payload = _pending_payload(
        cache_key=cache_key, model=model, job_type=job_type,
        resolution=resolution, quality=quality, aspect_ratio=aspect_ratio,
        metadata=metadata, cli_version=cli_version,
    )
    try:
        _atomic_write_json(pending, payload)
    except OSError as exc:
        _durable_write_quarantine(quarantine, payload, str(exc))
        raise PendingReceiptQuarantined(quarantine, payload, exc) from exc
    return payload


def _publish_cache_entry(
    *,
    output_path: Path,
    cached: Path,
    sidecar: Path,
    provenance: dict,
) -> None:
    """Stage both artifacts, publish valid provenance, then expose the image."""
    image_fd, image_name = tempfile.mkstemp(
        dir=cached.parent, prefix=f".{cached.stem}.", suffix=".png.tmp"
    )
    os.close(image_fd)
    sidecar_fd, sidecar_name = tempfile.mkstemp(
        dir=sidecar.parent, prefix=f".{cached.stem}.", suffix=".json.tmp"
    )
    os.close(sidecar_fd)
    staged_image = Path(image_name)
    staged_sidecar = Path(sidecar_name)
    try:
        shutil.copy2(output_path, staged_image)
        with staged_image.open("rb") as image_handle:
            os.fsync(image_handle.fileno())
        with staged_sidecar.open("w") as sidecar_handle:
            json.dump(provenance, sidecar_handle, indent=2)
            sidecar_handle.flush()
            os.fsync(sidecar_handle.fileno())
        os.replace(staged_sidecar, sidecar)
        os.replace(staged_image, cached)
        _fsync_directory(cached.parent)
    finally:
        staged_image.unlink(missing_ok=True)
        staged_sidecar.unlink(missing_ok=True)


def _load_cache_response(
    *,
    cached: Path,
    sidecar: Path,
    output_path: Path,
    cache_key: str,
    model: str,
    job_type: str,
    resolution: str,
    quality: str,
    aspect_ratio: str | None,
    remove_invalid: bool = False,
) -> HiggsfieldResponse | None:
    if not cached.exists():
        return None
    provenance = _read_valid_provenance(
        sidecar, model=model, job_type=job_type, resolution=resolution,
        quality=quality, aspect_ratio=aspect_ratio,
    )
    if provenance is None:
        if remove_invalid:
            cached.unlink(missing_ok=True)
            sidecar.unlink(missing_ok=True)
        return None
    shutil.copy2(cached, output_path)
    return HiggsfieldResponse(
        output_path, cache_key, True,
        job_id=provenance.get("job_id"),
        result_url=provenance.get("result_url"),
        display_name=provenance.get("display_name"),
        cli_version=provenance.get("cli_version"),
    )


def invoke_higgsfield_image_edit(
    *,
    prompt: str,
    reference_images: list[Path],
    output_path: Path,
    cache_dir: Path,
    cites_identity_rules: tuple[str, ...] = (),
    reject_reason: str | None = None,
    model: str = GPT_IMAGE,
    resolution: str = "1k",
    quality: str = "high",
    aspect_ratio: str | None = None,
    timeout_s: int = 600,
) -> HiggsfieldResponse:
    """Generate (or fetch from cache) one image via the Higgsfield CLI."""
    if model not in HIGGSFIELD_IMAGE_MODELS:
        raise UnwiredTransportError(model)
    job_type = HIGGSFIELD_IMAGE_MODELS[model]

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    reference_images = [Path(p) for p in reference_images]

    cache_key = _compute_cache_key(
        prompt=prompt, reference_images=reference_images,
        cites_identity_rules=cites_identity_rules, reject_reason=reject_reason,
        model=model, job_type=job_type, resolution=resolution,
        quality=quality, aspect_ratio=aspect_ratio,
    )
    cached = cache_dir / f"{cache_key}.png"
    sidecar = cache_dir / f"{cache_key}.provenance.json"
    pending = cache_dir / f"{cache_key}.pending.json"
    quarantine = cache_dir / f"{cache_key}.quarantine.json"
    intent = cache_dir / f"{cache_key}.create_in_flight.json"
    lock_path = cache_dir / f"{cache_key}.lock"
    # Forced stub is absolute and never reads or writes the real cache.
    if os.environ.get("ANIMA_FORCE_STUB"):
        _write_placeholder_png(output_path)
        return HiggsfieldResponse(
            output_path, cache_key, False, stub_fallback=True
        )
    if not pending.exists() and not quarantine.exists() and not intent.exists():
        hit = _load_cache_response(
            cached=cached, sidecar=sidecar, output_path=output_path,
            cache_key=cache_key, model=model, job_type=job_type,
            resolution=resolution, quality=quality, aspect_ratio=aspect_ratio,
        )
        if hit is not None:
            return hit

    # The second cache/pending check and all charged work/publication are one
    # per-key critical section. Concurrent processes cannot double-spend or
    # pair one writer's image with another writer's provenance.
    with _cache_key_lock(lock_path):
        if intent.exists():
            return _blocked_receipt_response(
                receipt=intent, output_path=output_path,
                cache_key=cache_key,
                reason="Unresolved create-in-flight intent",
            )
        if quarantine.exists():
            return _blocked_receipt_response(
                receipt=quarantine, output_path=output_path,
                cache_key=cache_key, reason="Quarantined charged-job receipt",
            )

        pending_exists = pending.exists()
        pending_payload = _read_valid_pending(
            pending, cache_key=cache_key, model=model, job_type=job_type,
            resolution=resolution, quality=quality,
            aspect_ratio=aspect_ratio,
        )
        if pending_payload is not None:
            return _recover_pending_job(
                pending_payload=pending_payload, pending=pending,
                output_path=output_path, cached=cached, sidecar=sidecar,
                cache_key=cache_key, model=model, job_type=job_type,
                resolution=resolution, quality=quality,
                aspect_ratio=aspect_ratio, timeout_s=timeout_s,
                quarantine=quarantine,
            )
        if pending_exists:
            return _blocked_receipt_response(
                receipt=pending, output_path=output_path,
                cache_key=cache_key,
                reason="Invalid or version-stale pending receipt",
            )
        hit = _load_cache_response(
            cached=cached, sidecar=sidecar, output_path=output_path,
            cache_key=cache_key, model=model, job_type=job_type,
            resolution=resolution, quality=quality, aspect_ratio=aspect_ratio,
            remove_invalid=True,
        )
        if hit is not None:
            return hit

        # No CLI on PATH (CI): return an honest placeholder, but never put
        # stub bytes into the real cache.
        if shutil.which(_HIGGSFIELD_BIN) is None:
            _write_placeholder_png(output_path)
            return HiggsfieldResponse(
                output_path, cache_key, False, stub_fallback=True
            )

        return _invoke_real(
            prompt=prompt, reference_images=reference_images,
            output_path=output_path, cached=cached, cache_key=cache_key,
            model=model, job_type=job_type, resolution=resolution,
            quality=quality, aspect_ratio=aspect_ratio, timeout_s=timeout_s,
            sidecar=sidecar, pending=pending, quarantine=quarantine,
            intent=intent,
        )


def _run_cli(cmd: list[str], timeout_s: int) -> subprocess.CompletedProcess:
    """The subprocess seam — monkeypatched by every unit test (an unmocked
    call on a machine with an authenticated CLI SPENDS CREDITS)."""
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s)


def _read_cli_version() -> str:
    result = _run_cli([_HIGGSFIELD_BIN, "--version"], 10)
    match = re.search(r"\bhiggsfield\s+(\d+\.\d+\.\d+)\b", result.stdout)
    if result.returncode != 0 or match is None:
        raise UnsupportedHiggsfieldCLIVersion(result.stdout or result.stderr)
    version = match.group(1)
    if version != PINNED_HIGGSFIELD_CLI_VERSION:
        raise UnsupportedHiggsfieldCLIVersion(
            f"higgsfield CLI {version} is unverified; pinned "
            f"{PINNED_HIGGSFIELD_CLI_VERSION}"
        )
    return version


def _parse_cli_output(
    stdout: str,
) -> tuple[str | None, str | None, str | None]:
    """(result_url, job_id, display_name). JSON is primary; the bare URL
    printed by v0.2.3 without --json is a compatibility fallback only."""
    url, job_id, display_name = None, None, None
    try:
        payload = json.loads(stdout)
        if isinstance(payload, dict):
            job_id = payload.get("id") or payload.get("job_id")
            url = payload.get("result_url") or payload.get("url")
            display_name = payload.get("display_name")
    except (json.JSONDecodeError, ValueError):
        pass
    if url is None:
        for tok in stdout.split():
            if tok.startswith("https://"):
                url = tok.strip()
                break
    return url, job_id, display_name


def _as_text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _read_receipt_identity(
    receipt: Path,
) -> tuple[
    tuple[str | None, str | None, str | None],
    str | None,
]:
    """Best-effort identity for an invalid receipt; never authorizes recovery."""
    try:
        payload = json.loads(receipt.read_text())
    except (OSError, json.JSONDecodeError, ValueError):
        return (None, None, None), None
    if not isinstance(payload, dict):
        return (None, None, None), None

    def text_or_none(key: str) -> str | None:
        value = payload.get(key)
        return value if isinstance(value, str) else None

    return (
        text_or_none("result_url"),
        text_or_none("job_id"),
        text_or_none("display_name"),
    ), text_or_none("cli_version")


def _merge_cli_metadata(
    current: tuple[str | None, str | None, str | None],
    update: tuple[str | None, str | None, str | None],
) -> tuple[str | None, str | None, str | None]:
    """Keep every non-null URL/job/display value observed across CLI calls."""
    return tuple(new if new is not None else old for old, new in zip(current, update))


def _is_transient_failure(result: subprocess.CompletedProcess) -> bool:
    """Retry failed CLI calls on any 5xx, timeout, or temporary condition."""
    if result.returncode == 0:
        return False
    blob = f"{result.stdout or ''}{result.stderr or ''}".lower()
    return _HTTP_5XX.search(blob) is not None or any(
        signal in blob for signal in _TRANSIENT_SIGNALS
    )


def _download(url: str, dest: Path, timeout_s: int) -> None:
    with urllib.request.urlopen(url, timeout=timeout_s) as resp:  # noqa: S310
        Path(dest).write_bytes(resp.read())


def _download_with_retries(url: str, dest: Path, timeout_s: int) -> bool:
    """Bound CDN retries and never leak a download exception to callers."""
    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            _download(url, dest, timeout_s)
            return True
        except Exception as exc:  # downloader implementations vary by platform
            dest.unlink(missing_ok=True)
            _LOG.warning(
                "higgsfield download failure (attempt %d/%d): %s",
                attempt, _MAX_ATTEMPTS, str(exc)[:200],
            )
            if attempt < _MAX_ATTEMPTS:
                time.sleep(2 * attempt)
    return False


def _resume_existing_job(
    job_id: str,
    timeout_s: int,
) -> tuple[
    subprocess.CompletedProcess,
    tuple[str | None, str | None, str | None],
]:
    """Resume an existing job with bounded 5xx retries on the same id."""
    cmd = [
        _HIGGSFIELD_BIN, "generate", "wait", job_id,
        "--quiet", "--json", "--timeout", "9m",
    ]
    result = None
    metadata = (None, job_id, None)
    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            result = _run_cli(cmd, timeout_s)
        except subprocess.TimeoutExpired:
            result = subprocess.CompletedProcess(
                cmd, 124, stdout="", stderr="wait timed out"
            )
        parsed = _parse_cli_output(result.stdout)
        observed_job_id = parsed[1]
        if observed_job_id is not None and observed_job_id != job_id:
            raise MismatchedHiggsfieldJobIdentity(job_id, observed_job_id)
        metadata = _merge_cli_metadata(metadata, parsed)
        transient = result.returncode == 124 or _is_transient_failure(result)
        if not transient or attempt == _MAX_ATTEMPTS:
            return result, metadata
        time.sleep(2 * attempt)
    assert result is not None  # loop is non-empty; narrows for type checkers
    return result, metadata


def _response_for_failure(
    *,
    output_path: Path,
    cache_key: str,
    exit_code: int,
    metadata: tuple[str | None, str | None, str | None],
    cli_version: str,
    error: str | None = None,
) -> HiggsfieldResponse:
    url, job_id, display_name = metadata
    return HiggsfieldResponse(
        output_path, cache_key, False, exit_code=exit_code or 1,
        job_id=job_id, result_url=url, display_name=display_name,
        cli_version=cli_version, error=error,
    )


def _blocked_receipt_response(
    *,
    receipt: Path,
    output_path: Path,
    cache_key: str,
    reason: str,
) -> HiggsfieldResponse:
    metadata, cli_version = _read_receipt_identity(receipt)
    return _response_for_failure(
        output_path=output_path, cache_key=cache_key, exit_code=78,
        metadata=metadata,
        cli_version=cli_version or PINNED_HIGGSFIELD_CLI_VERSION,
        error=(
            f"{reason}: {receipt}. Operator resolution required: inspect the "
            f"receipt and restore/remove it only after resolving the known or "
            f"possible charged job; automatic create is blocked."
        ),
    )


def _mismatched_wait_response(
    *,
    exc: MismatchedHiggsfieldJobIdentity,
    output_path: Path,
    cache_key: str,
    metadata: tuple[str | None, str | None, str | None],
    cli_version: str,
) -> HiggsfieldResponse:
    return _response_for_failure(
        output_path=output_path, cache_key=cache_key, exit_code=78,
        metadata=metadata, cli_version=cli_version,
        error=(
            f"Higgsfield wait job ID mismatch: requested {exc.requested}, "
            f"received {exc.observed}. The original receipt was retained; "
            "operator resolution is required and automatic download/cache "
            "publication is blocked."
        ),
    )


def _quarantined_write_response(
    *,
    exc: PendingReceiptQuarantined,
    output_path: Path,
    cache_key: str,
) -> HiggsfieldResponse:
    payload = exc.payload
    metadata = (
        payload.get("result_url"),
        payload.get("job_id"),
        payload.get("display_name"),
    )
    return _response_for_failure(
        output_path=output_path, cache_key=cache_key, exit_code=78,
        metadata=metadata,
        cli_version=payload.get("cli_version") or PINNED_HIGGSFIELD_CLI_VERSION,
        error=(
            f"Charged job receipt write failed and identity was quarantined at "
            f"{exc.quarantine}. Operator resolution required before retry."
        ),
    )


def _persist_pending_or_failure(
    *,
    pending: Path,
    quarantine: Path,
    output_path: Path,
    cache_key: str,
    model: str,
    job_type: str,
    resolution: str,
    quality: str,
    aspect_ratio: str | None,
    metadata: tuple[str | None, str | None, str | None],
    cli_version: str,
) -> PendingPersistenceResult:
    try:
        payload = _persist_pending(
            pending, quarantine=quarantine, cache_key=cache_key, model=model,
            job_type=job_type, resolution=resolution, quality=quality,
            aspect_ratio=aspect_ratio, metadata=metadata,
            cli_version=cli_version,
        )
    except PendingReceiptQuarantined as exc:
        return PendingPersistenceResult(
            PendingDurability.DURABLE_QUARANTINE,
            _quarantined_write_response(
                exc=exc, output_path=output_path, cache_key=cache_key,
            ),
        )
    except OSError as exc:
        return PendingPersistenceResult(
            PendingDurability.NOT_DURABLE,
            _response_for_failure(
                output_path=output_path, cache_key=cache_key, exit_code=78,
                metadata=metadata, cli_version=cli_version,
                error=(
                    "Neither canonical nor quarantine charged-job receipt "
                    f"could be published durably: {exc}. The pre-existing "
                    "pending receipt or pre-create intent remains the "
                    "fail-closed recovery marker; operator resolution is "
                    "required."
                ),
            ),
        )
    return PendingPersistenceResult(
        PendingDurability.DURABLE_PENDING
        if payload is not None else PendingDurability.NOT_DURABLE
    )


def _finish_create_receipt_transition(
    *,
    persistence: PendingPersistenceResult,
    intent: Path,
    output_path: Path,
    cache_key: str,
    metadata: tuple[str | None, str | None, str | None],
    cli_version: str,
) -> HiggsfieldResponse | None:
    if persistence.outcome is not PendingDurability.NOT_DURABLE:
        try:
            _durable_unlink(intent)
        except OSError as exc:
            return _response_for_failure(
                output_path=output_path, cache_key=cache_key, exit_code=78,
                metadata=metadata, cli_version=cli_version,
                error=(
                    "Charged-job successor is durable, but pre-create intent "
                    f"removal was not durably confirmed: {exc}. Automatic "
                    "create remains blocked by the successor receipt."
                ),
            )
    return persistence.response


def _finish_known_job(
    *,
    metadata: tuple[str | None, str | None, str | None],
    pending: Path,
    quarantine: Path,
    output_path: Path,
    cached: Path,
    sidecar: Path,
    cache_key: str,
    model: str,
    job_type: str,
    resolution: str,
    quality: str,
    aspect_ratio: str | None,
    cli_version: str,
    timeout_s: int,
    refresh_on_download_failure: bool = False,
) -> HiggsfieldResponse:
    url, job_id, display_name = metadata
    if not url:
        return _response_for_failure(
            output_path=output_path, cache_key=cache_key, exit_code=1,
            metadata=metadata, cli_version=cli_version,
        )
    if not _download_with_retries(url, output_path, timeout_s):
        if not refresh_on_download_failure or job_id is None:
            return _response_for_failure(
                output_path=output_path, cache_key=cache_key, exit_code=1,
                metadata=metadata, cli_version=cli_version,
                error="Higgsfield result download failed after bounded retries.",
            )
        if shutil.which(_HIGGSFIELD_BIN) is None:
            return _response_for_failure(
                output_path=output_path, cache_key=cache_key, exit_code=127,
                metadata=metadata, cli_version=cli_version,
                error=(
                    "Stored result URL failed and the known job ID cannot be "
                    "refreshed because the Higgsfield CLI is unavailable."
                ),
            )
        try:
            result, wait_metadata = _resume_existing_job(job_id, timeout_s)
        except MismatchedHiggsfieldJobIdentity as exc:
            return _mismatched_wait_response(
                exc=exc, output_path=output_path, cache_key=cache_key,
                metadata=metadata, cli_version=cli_version,
            )
        metadata = _merge_cli_metadata(metadata, wait_metadata)
        persistence = _persist_pending_or_failure(
            pending=pending, quarantine=quarantine, output_path=output_path,
            cache_key=cache_key, model=model, job_type=job_type,
            resolution=resolution, quality=quality,
            aspect_ratio=aspect_ratio, metadata=metadata,
            cli_version=cli_version,
        )
        if persistence.response is not None:
            return persistence.response
        if result.returncode != 0:
            return _response_for_failure(
                output_path=output_path, cache_key=cache_key,
                exit_code=result.returncode, metadata=metadata,
                cli_version=cli_version,
                error="Known Higgsfield job URL refresh failed.",
            )
        url, job_id, display_name = metadata
        if not url or not _download_with_retries(url, output_path, timeout_s):
            return _response_for_failure(
                output_path=output_path, cache_key=cache_key, exit_code=1,
                metadata=metadata, cli_version=cli_version,
                error=(
                    "Refreshed Higgsfield result download failed after "
                    "bounded retries."
                ),
            )

    provenance = {
        "transport": "higgsfield",
        "vendor_model": model,
        "job_type": job_type,
        "quality": quality,
        "resolution": resolution,
        "aspect_ratio": aspect_ratio,
        "job_id": job_id,
        "result_url": url,
        "display_name": display_name,
        "cli_version": cli_version,
    }
    try:
        _publish_cache_entry(
            output_path=output_path, cached=cached, sidecar=sidecar,
            provenance=provenance,
        )
    except Exception as exc:
        _LOG.warning("higgsfield cache publication failed: %s", str(exc)[:200])
        return _response_for_failure(
            output_path=output_path, cache_key=cache_key, exit_code=1,
            metadata=metadata, cli_version=cli_version,
        )
    try:
        _durable_unlink(pending)
    except OSError as exc:
        return _response_for_failure(
            output_path=output_path, cache_key=cache_key, exit_code=78,
            metadata=metadata, cli_version=cli_version,
            error=(
                "Cache pair is durable, but pending-receipt removal was not "
                f"durably confirmed: {exc}. Automatic create remains blocked "
                "by the durable cache or receipt."
            ),
        )
    _LOG.info("higgsfield %s ok: url=%s job_id=%s", job_type, url, job_id)
    return HiggsfieldResponse(
        output_path, cache_key, False, job_id=job_id, result_url=url,
        display_name=display_name, cli_version=cli_version,
    )


def _recover_pending_job(
    *,
    pending_payload: dict,
    pending: Path,
    quarantine: Path,
    output_path: Path,
    cached: Path,
    sidecar: Path,
    cache_key: str,
    model: str,
    job_type: str,
    resolution: str,
    quality: str,
    aspect_ratio: str | None,
    timeout_s: int,
) -> HiggsfieldResponse:
    metadata = (
        pending_payload.get("result_url"),
        pending_payload.get("job_id"),
        pending_payload.get("display_name"),
    )
    cli_version = pending_payload["cli_version"]
    url, job_id, _ = metadata
    if url is None and job_id is not None:
        if shutil.which(_HIGGSFIELD_BIN) is None:
            return _response_for_failure(
                output_path=output_path, cache_key=cache_key, exit_code=127,
                metadata=metadata, cli_version=cli_version,
            )
        try:
            result, wait_metadata = _resume_existing_job(job_id, timeout_s)
        except MismatchedHiggsfieldJobIdentity as exc:
            return _mismatched_wait_response(
                exc=exc, output_path=output_path, cache_key=cache_key,
                metadata=metadata, cli_version=cli_version,
            )
        metadata = _merge_cli_metadata(metadata, wait_metadata)
        persistence = _persist_pending_or_failure(
            pending=pending, quarantine=quarantine, output_path=output_path,
            cache_key=cache_key, model=model, job_type=job_type,
            resolution=resolution, quality=quality,
            aspect_ratio=aspect_ratio, metadata=metadata,
            cli_version=cli_version,
        )
        if persistence.response is not None:
            return persistence.response
        if result.returncode != 0:
            return _response_for_failure(
                output_path=output_path, cache_key=cache_key,
                exit_code=result.returncode, metadata=metadata,
                cli_version=cli_version,
            )
    return _finish_known_job(
        metadata=metadata, pending=pending, quarantine=quarantine,
        output_path=output_path,
        cached=cached, sidecar=sidecar, cache_key=cache_key, model=model,
        job_type=job_type, resolution=resolution, quality=quality,
        aspect_ratio=aspect_ratio, cli_version=cli_version,
        timeout_s=timeout_s,
        refresh_on_download_failure=job_id is not None,
    )


def _invoke_real(
    *,
    prompt: str,
    reference_images: list[Path],
    output_path: Path,
    cached: Path,
    cache_key: str,
    model: str,
    job_type: str,
    resolution: str,
    quality: str,
    aspect_ratio: str | None,
    timeout_s: int,
    sidecar: Path,
    pending: Path,
    quarantine: Path,
    intent: Path,
) -> HiggsfieldResponse:
    cli_version = _read_cli_version()  # fail closed before any generation
    cmd = [
        _HIGGSFIELD_BIN, "generate", "create", job_type,
        "--prompt", prompt,
        "--quality", quality,
        "--resolution", resolution,
        "--wait", "--wait-timeout", "9m", "--json",
    ]
    if aspect_ratio is not None:
        cmd.extend(["--aspect_ratio", aspect_ratio])
    for ref in reference_images:
        cmd.extend(["--image", str(ref)])

    intent_payload = {
        "cache_key": cache_key,
        "transport": "higgsfield",
        "vendor_model": model,
        "job_type": job_type,
        "quality": quality,
        "resolution": resolution,
        "aspect_ratio": aspect_ratio,
        "cli_version": cli_version,
        "state": "create_in_flight",
        "operator_action": (
            "Resolve whether the combined create/wait charged a job before "
            "removing this marker. Automatic create is blocked."
        ),
    }
    try:
        _publish_create_intent(intent, intent_payload)
    except OSError as exc:
        return _response_for_failure(
            output_path=output_path, cache_key=cache_key, exit_code=78,
            metadata=(None, None, None), cli_version=cli_version,
            error=(
                f"Could not durably publish pre-create intent at {intent}: "
                f"{exc}. Higgsfield create was not invoked."
            ),
        )

    result = None
    metadata = (None, None, None)
    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            result = _run_cli(cmd, timeout_s)
        except subprocess.TimeoutExpired as exc:
            timeout_metadata = _parse_cli_output(_as_text(exc.output))
            timeout_metadata = _merge_cli_metadata(
                timeout_metadata, _parse_cli_output(_as_text(exc.stderr))
            )
            metadata = _merge_cli_metadata(metadata, timeout_metadata)
            persistence = _persist_pending_or_failure(
                pending=pending, quarantine=quarantine,
                output_path=output_path, cache_key=cache_key, model=model,
                job_type=job_type, resolution=resolution, quality=quality,
                aspect_ratio=aspect_ratio, metadata=metadata,
                cli_version=cli_version,
            )
            blocked = _finish_create_receipt_transition(
                persistence=persistence, intent=intent,
                output_path=output_path, cache_key=cache_key,
                metadata=metadata, cli_version=cli_version,
            )
            if blocked is not None:
                return blocked
            return _response_for_failure(
                output_path=output_path, cache_key=cache_key, exit_code=124,
                metadata=metadata, cli_version=cli_version,
                error=(
                    "Higgsfield create/wait timed out; any emitted charged-job "
                    "identity was retained for identical-retry recovery."
                ),
            )
        parsed = _parse_cli_output(result.stdout)
        metadata = _merge_cli_metadata(metadata, parsed)
        url, job_id, _ = parsed
        persistence = _persist_pending_or_failure(
            pending=pending, quarantine=quarantine, output_path=output_path,
            cache_key=cache_key, model=model, job_type=job_type,
            resolution=resolution, quality=quality,
            aspect_ratio=aspect_ratio, metadata=metadata,
            cli_version=cli_version,
        )
        blocked = _finish_create_receipt_transition(
            persistence=persistence, intent=intent,
            output_path=output_path, cache_key=cache_key,
            metadata=metadata, cli_version=cli_version,
        )
        if blocked is not None:
            return blocked
        if result.returncode != 0 and job_id:
            # The job exists: resume it before classifying the create failure.
            # A second create could duplicate a charged generation.
            try:
                result, wait_metadata = _resume_existing_job(job_id, timeout_s)
            except MismatchedHiggsfieldJobIdentity as exc:
                return _mismatched_wait_response(
                    exc=exc, output_path=output_path, cache_key=cache_key,
                    metadata=metadata, cli_version=cli_version,
                )
            metadata = _merge_cli_metadata(metadata, wait_metadata)
            persistence = _persist_pending_or_failure(
                pending=pending, quarantine=quarantine,
                output_path=output_path, cache_key=cache_key, model=model,
                job_type=job_type, resolution=resolution, quality=quality,
                aspect_ratio=aspect_ratio, metadata=metadata,
                cli_version=cli_version,
            )
            blocked = _finish_create_receipt_transition(
                persistence=persistence, intent=intent,
                output_path=output_path, cache_key=cache_key,
                metadata=metadata, cli_version=cli_version,
            )
            if blocked is not None:
                return blocked
            break
        transient = _is_transient_failure(result)
        if not transient:
            break
        if url:
            # A result URL proves a job exists, but without an id it cannot be
            # resumed safely. Never issue another charged create.
            break
        _LOG.warning(
            "higgsfield %s transient failure (attempt %d/%d): %s",
            job_type, attempt, _MAX_ATTEMPTS, result.stderr.strip()[:200],
        )
        if attempt < _MAX_ATTEMPTS:
            time.sleep(2 * attempt)

    if result.returncode != 0:
        return _response_for_failure(
            output_path=output_path, cache_key=cache_key,
            exit_code=result.returncode, metadata=metadata,
            cli_version=cli_version,
        )

    url, job_id, display_name = metadata
    if not url:
        return _response_for_failure(
            output_path=output_path, cache_key=cache_key, exit_code=1,
            metadata=metadata, cli_version=cli_version,
        )

    return _finish_known_job(
        metadata=metadata, pending=pending, quarantine=quarantine,
        output_path=output_path,
        cached=cached, sidecar=sidecar, cache_key=cache_key, model=model,
        job_type=job_type, resolution=resolution, quality=quality,
        aspect_ratio=aspect_ratio, cli_version=cli_version,
        timeout_s=timeout_s,
    )
