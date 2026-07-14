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
_TRANSIENT_SIGNALS = ("502", "503", "504", "timeout", "temporarily")


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
        shutil.copy2(cached, output_path)
        provenance = json.loads(sidecar.read_text()) if sidecar.exists() else {}
        return HiggsfieldResponse(
            output_path, cache_key, True,
            job_id=provenance.get("job_id"),
            result_url=provenance.get("result_url"),
            display_name=provenance.get("display_name"),
            cli_version=provenance.get("cli_version"),
        )

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


def _invoke_real(**kwargs) -> HiggsfieldResponse:  # implemented in Task 2
    raise NotImplementedError("real path lands in Task 2")
