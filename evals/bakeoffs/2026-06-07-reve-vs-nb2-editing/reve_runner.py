"""Thin Reve API client for the editing bake-off — with a credential-free stub.

Mirrors pipeline/agents/nb_pro_runner.py's shape: a single entry point that
self-stubs when the key is absent (writes a placeholder PNG, stub_fallback=True),
content-addressed cache, and a real path behind it. Routes by reference count —
1 ref -> Edit, >=2 refs -> Remix (the report §A operation split).

SCHEMA STATUS (2026-06-08): the request/response shape was originally INFERRED from
third-party mirrors and was WRONG. It has since been VERIFIED against the live API
(api.reve.com) from the API's own error messages + successful calls — Edit uses
`edit_instruction` + `reference_image` (single b64); Remix uses `prompt` +
`reference_images` (list b64); both accept optional `aspect_ratio` + `version`; the
response is FLAT with a top-level base64 PNG in `image` plus `version` / `credits_used`
/ `credits_remaining` / `content_violation` / `request_id`. The ONE remaining gap is the
FAST-tier `version` string (console-gated, unverifiable by probing) — see `_REVE_VERSION`.
Full account in the bake-off postmortem. The stub path is exercised in CI.
"""
from __future__ import annotations

import base64
import hashlib
import os
import shutil
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

# --- Endpoint config — SCHEMA VERIFIED AGAINST THE LIVE API 2026-06-08 ---
# The original mirror-inferred schema was WRONG (prompt/image/images/fast + data[0].b64_json);
# corrected here from the API's own error messages + successful calls. See the bake-off
# postmortem (docs/anima-test-runs/2026-06-07-reve-vs-nb2-bakeoff-postmortem.md).
_REVE_BASE = os.environ.get("REVE_API_BASE", "https://api.reve.com")
_REVE_EDIT_PATH = "/v1/image/edit"     # VERIFIED: {edit_instruction, reference_image (single b64), aspect_ratio?, version?}
_REVE_REMIX_PATH = "/v1/image/remix"   # VERIFIED: {prompt, reference_images (list b64), aspect_ratio?, version?}
# Tier is selected by the `version` request param (NOT a `fast` boolean — that 400s as
# UNRECOGNIZED). Standard default (server-reported): reve-edit@20250915 / reve-remix@20250915,
# 30 credits/call. None => omit `version` => the API default (= standard).
# The FAST-tier version strings are CONSOLE-GATED and UNVERIFIED: `version` accepts any string
# without validating it at parse time, and no models/versions listing endpoint exists, so they
# can't be discovered by probing. They MUST be filled from the authenticated Reve console before
# the reve-fast variant runs — the runner REFUSES fast with an unknown version rather than
# silently running standard (which would misreport fast results).
_REVE_VERSION = {
    "standard": {"edit": None, "remix": None},
    "fast": {"edit": None, "remix": None},   # TODO(sean): fill fast version strings from console
}
_REQUEST_TIMEOUT_S = 120


@dataclass(frozen=True)
class ReveResponse:
    output_path: Path
    cache_key: str
    cache_hit: bool
    stub_fallback: bool
    endpoint: str          # "edit" | "remix" | "stub"
    cost_usd: float        # the published per-image rate for (engine, tier)
    exit_code: int = 0

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and self.output_path.exists()


def _has_reve_key() -> bool:
    return bool(os.environ.get("REVE_API_KEY"))


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()


def _cache_key(*, prompt: str, references: list[Path], tier: str, endpoint: str) -> str:
    h = hashlib.sha256()
    h.update(prompt.encode("utf-8"))
    h.update(tier.encode("utf-8"))
    h.update(endpoint.encode("utf-8"))
    for ref in references:
        h.update(_hash_file(ref).encode("utf-8"))
    return h.hexdigest()


def _write_placeholder_png(path: Path) -> None:
    """A small, deterministic placeholder so the stub path produces a real PNG.
    Mid-gray field — the stub is NOT a scored claim (DINOv2 against it is
    meaningless; the bake-off's stub mode proves plumbing only)."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (1376, 768), (128, 128, 128)).save(path, "PNG")


_TIER_COST = {  # published per-image USD (report §B; Sean's console screenshots)
    "fast": 0.007,
    "standard": 0.040,
}


def _reve_debug_log(log_path: str, endpoint: str, tier: str, resp) -> None:
    """Opt-in, NON-SCORING observability for §5 Test 4 + snapshot pinning.

    Active only when REVE_DEBUG_LOG names a file. Records status / latency /
    rate-limit + model/build headers, and the response body's non-image scalar
    fields (image bytes elided), one JSON line per call. Wrapped so a logging
    failure can NEVER break a costed generation — it does not touch the request,
    the parse, or the returned ReveResponse.
    """
    import json
    try:
        hdr_tokens = ("rate", "limit", "remaining", "reset", "retry",
                      "model", "build", "version", "request-id", "content-type")
        headers = {k: v for k, v in resp.headers.items()
                   if any(t in k.lower() for t in hdr_tokens)}
        body_scalars = None
        if "json" in resp.headers.get("content-type", "").lower():
            try:
                data = resp.json()
                # Verified response is FLAT: top-level `image` (b64) + scalars. Elide the image.
                body_scalars = {
                    "top_keys": sorted(data.keys()) if isinstance(data, dict) else None,
                    "scalars": {k: v for k, v in (data.items() if isinstance(data, dict) else [])
                                if k != "image" and not isinstance(v, (list, dict))},
                }
            except Exception:  # noqa: BLE001
                body_scalars = {"parse": "non-json-or-error", "text_head": resp.text[:200]}
        rec = {"endpoint": endpoint, "tier": tier, "status": resp.status_code,
               "elapsed_s": round(resp.elapsed.total_seconds(), 3),
               "headers": headers, "body": body_scalars}
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception:  # noqa: BLE001 — observability must never break the costed path
        pass


def invoke_reve(
    *,
    prompt: str,
    reference_images: list[Path],
    output_path: Path,
    cache_dir: Path,
    tier: str = "standard",
    aspect_ratio: str = "16:9",
    timeout_s: int = _REQUEST_TIMEOUT_S,
) -> ReveResponse:
    """Edit (1 ref) or Remix (>=2 refs) one image via Reve, or stub if no key.

    Routes on reference count. Content-addressed cache (same prompt+refs+tier+endpoint
    -> cache hit). Returns a ReveResponse whose `stub_fallback` tells the caller the
    output is a placeholder, not a scored generation.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)
    references = [Path(p) for p in reference_images]

    endpoint = "edit" if len(references) == 1 else "remix"
    cost = _TIER_COST.get(tier, 0.040)
    key = _cache_key(prompt=prompt, references=references, tier=tier, endpoint=endpoint)
    cached = cache_dir / f"{key}.png"

    if cached.exists():
        shutil.copy2(cached, output_path)
        return ReveResponse(output_path, key, True, False, endpoint, cost)

    # Stub fallback — no key, no spend. Mirrors invoke_image_edit's gate exactly.
    if not _has_reve_key():
        _write_placeholder_png(output_path)
        shutil.copy2(output_path, cached)
        return ReveResponse(output_path, key, False, True, "stub", cost)

    # ---- Real path — SCHEMA VERIFIED against the live API 2026-06-08 (see module header). ----
    try:
        import requests  # local import — only the live path needs it
    except ImportError as exc:  # pragma: no cover - environment-dependent
        raise RuntimeError("live Reve path needs `requests` (pip install requests)") from exc

    path = _REVE_EDIT_PATH if endpoint == "edit" else _REVE_REMIX_PATH
    version = _REVE_VERSION.get(tier, {}).get(endpoint)
    if tier == "fast" and version is None:
        # Refuse rather than silently running standard and mislabeling it as fast.
        raise RuntimeError(
            "Reve FAST tier requested but the fast `version` string is unknown — fill "
            "_REVE_VERSION['fast'] from the authenticated console. (The API accepts any "
            "version string without validating it, so a guess would silently run standard.)"
        )
    images_b64 = [base64.b64encode(p.read_bytes()).decode("ascii") for p in references]
    if endpoint == "edit":
        payload = {"edit_instruction": prompt, "reference_image": images_b64[0],
                   "aspect_ratio": aspect_ratio}
    else:  # remix
        payload = {"prompt": prompt, "reference_images": images_b64,
                   "aspect_ratio": aspect_ratio}
    if version is not None:
        payload["version"] = version
    headers = {
        "Authorization": f"Bearer {os.environ['REVE_API_KEY']}",
        "Content-Type": "application/json",
    }
    resp = requests.post(f"{_REVE_BASE}{path}", json=payload, headers=headers, timeout=timeout_s)
    if os.environ.get("REVE_DEBUG_LOG"):
        _reve_debug_log(os.environ["REVE_DEBUG_LOG"], endpoint, tier, resp)
    if resp.status_code != 200:
        return ReveResponse(output_path, key, False, False, endpoint, cost,
                            exit_code=resp.status_code)
    # Response (VERIFIED): top-level base64 PNG in `image`; also content_violation,
    # credits_used/remaining, version, request_id.
    data = resp.json()
    if data.get("content_violation"):
        return ReveResponse(output_path, key, False, False, endpoint, cost, exit_code=2)
    img_b64 = data.get("image")
    if not isinstance(img_b64, str) or not img_b64:
        return ReveResponse(output_path, key, False, False, endpoint, cost, exit_code=1)
    output_path.write_bytes(base64.b64decode(img_b64))

    shutil.copy2(output_path, cached)
    return ReveResponse(output_path, key, False, False, endpoint, cost)
