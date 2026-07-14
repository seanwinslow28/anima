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
from dataclasses import dataclass
from pathlib import Path

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

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and Path(self.output_path).exists()


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
        staged_sidecar.write_text(json.dumps(provenance, indent=2))
        os.replace(staged_sidecar, sidecar)
        os.replace(staged_image, cached)
    finally:
        staged_image.unlink(missing_ok=True)
        staged_sidecar.unlink(missing_ok=True)


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
    # Forced stub is absolute and never reads or writes the real cache.
    if os.environ.get("ANIMA_FORCE_STUB"):
        _write_placeholder_png(output_path)
        return HiggsfieldResponse(
            output_path, cache_key, False, stub_fallback=True
        )
    if cached.exists():
        provenance = _read_valid_provenance(
            sidecar, model=model, job_type=job_type, resolution=resolution,
            quality=quality, aspect_ratio=aspect_ratio,
        )
        if provenance is not None:
            shutil.copy2(cached, output_path)
            return HiggsfieldResponse(
                output_path, cache_key, True,
                job_id=provenance.get("job_id"),
                result_url=provenance.get("result_url"),
                display_name=provenance.get("display_name"),
                cli_version=provenance.get("cli_version"),
            )
        # A cache image without matching, readable provenance is untrusted.
        # Remove the incomplete pair before a replacement generation so a
        # concurrent reader cannot accept old bytes under new provenance.
        cached.unlink(missing_ok=True)
        sidecar.unlink(missing_ok=True)

    # No CLI on PATH (CI): return an honest placeholder, but never put stub
    # bytes into the real cache.
    if shutil.which(_HIGGSFIELD_BIN) is None:
        _write_placeholder_png(output_path)
        return HiggsfieldResponse(output_path, cache_key, False, stub_fallback=True)

    return _invoke_real(
        prompt=prompt, reference_images=reference_images,
        output_path=output_path, cached=cached, cache_key=cache_key,
        model=model, job_type=job_type, resolution=resolution, quality=quality,
        aspect_ratio=aspect_ratio, timeout_s=timeout_s, cache_dir=cache_dir,
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
        result = _run_cli(cmd, timeout_s)
        metadata = _merge_cli_metadata(metadata, _parse_cli_output(result.stdout))
        transient = _is_transient_failure(result)
        if not transient or attempt == _MAX_ATTEMPTS:
            return result, metadata
        time.sleep(2 * attempt)
    assert result is not None  # loop is non-empty; narrows for type checkers
    return result, metadata


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
    cache_dir: Path,
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

    result = None
    metadata = (None, None, None)
    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            result = _run_cli(cmd, timeout_s)
        except subprocess.TimeoutExpired:
            return HiggsfieldResponse(output_path, cache_key, False, exit_code=124)
        parsed = _parse_cli_output(result.stdout)
        metadata = _merge_cli_metadata(metadata, parsed)
        url, job_id, _ = parsed
        if result.returncode != 0 and job_id:
            # The job exists: resume it before classifying the create failure.
            # A second create could duplicate a charged generation.
            result, wait_metadata = _resume_existing_job(job_id, timeout_s)
            metadata = _merge_cli_metadata(metadata, wait_metadata)
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
        return HiggsfieldResponse(
            output_path, cache_key, False, exit_code=result.returncode or 1)

    url, job_id, display_name = metadata
    if not url:
        return HiggsfieldResponse(output_path, cache_key, False, exit_code=1)

    # Immediate download — Higgsfield retains outputs ~7 days (D5).
    _download(url, output_path, timeout_s)
    # Provenance sidecar: the honest substitute for served-model read-back.
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
    _publish_cache_entry(
        output_path=output_path,
        cached=cached,
        sidecar=cache_dir / f"{cache_key}.provenance.json",
        provenance=provenance,
    )
    _LOG.info("higgsfield %s ok: url=%s job_id=%s", job_type, url, job_id)
    return HiggsfieldResponse(
        output_path, cache_key, False, job_id=job_id, result_url=url,
        display_name=display_name, cli_version=cli_version)
