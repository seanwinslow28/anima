"""Thin Reve API client for the editing bake-off — with a credential-free stub.

Mirrors pipeline/agents/nb_pro_runner.py's shape: a single entry point that
self-stubs when the key is absent (writes a placeholder PNG, stub_fallback=True),
content-addressed cache, and a real path behind it. Routes by reference count —
1 ref -> Edit, >=2 refs -> Remix (the report §A operation split).

⚠ ENDPOINT SCHEMA IS INFERRED, NOT FIRST-PARTY-VERIFIED. Reve's console docs
(api.reve.com/console/.../docs/{edit,remix}) are an auth-gated JS SPA that desk
research could not read; the request/response shape below is reconstructed from
third-party mirrors (AIMLAPI `/v1/images/generations`, Replicate, fal — see the
report §Sources). BEFORE the live run, the operator MUST verify the real
endpoint, auth header, field names, and tier selector against the authenticated
console and correct `_REVE_*` below. The stub path is exercised in CI; the real
path is the operator's to confirm. Pin the build/model header the API returns
into the trace (variants.yaml `snapshots.reve`).
"""
from __future__ import annotations

import base64
import hashlib
import os
import shutil
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

# --- Endpoint config (VERIFY against the authenticated console before live run) ---
_REVE_BASE = os.environ.get("REVE_API_BASE", "https://api.reve.com")
_REVE_EDIT_PATH = "/v1/image/edit"     # 1 image + instruction -> 1 image     (VERIFY)
_REVE_REMIX_PATH = "/v1/image/remix"   # 1-6 images + prompt -> 1 image        (VERIFY)
# Tier -> the API's fast/standard selector. The console exposes "Fast" variants
# (Edit Fast / Remix Fast, 5 credits) vs standard (30 credits). The exact request
# field is unconfirmed; `fast: bool` is the inferred shape. (VERIFY)
_TIER_FAST = {"fast": True}
_TIER_STANDARD = {"fast": False}
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
        if resp.status_code == 200 and "json" in resp.headers.get("content-type", "").lower():
            try:
                data = resp.json()
                item = (data.get("data") or [{}])[0] if isinstance(data, dict) else {}
                body_scalars = {
                    "top_keys": sorted(data.keys()) if isinstance(data, dict) else None,
                    "item_keys": sorted(item.keys()) if isinstance(item, dict) else None,
                    "item_nonimage": {k: v for k, v in (item.items() if isinstance(item, dict) else [])
                                      if k not in ("b64_json", "url") and not isinstance(v, (list, dict))},
                }
            except Exception:  # noqa: BLE001
                body_scalars = {"parse": "non-json-or-error"}
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

    # ---- Real path (operator-verified). Inferred schema; see module docstring. ----
    try:
        import requests  # local import — only the live path needs it
    except ImportError as exc:  # pragma: no cover - environment-dependent
        raise RuntimeError("live Reve path needs `requests` (pip install requests)") from exc

    path = _REVE_EDIT_PATH if endpoint == "edit" else _REVE_REMIX_PATH
    tier_field = _TIER_FAST if tier == "fast" else _TIER_STANDARD
    images_b64 = [base64.b64encode(p.read_bytes()).decode("ascii") for p in references]
    payload = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        # Edit uses one image; Remix takes the list. Field names are INFERRED — VERIFY.
        ("image" if endpoint == "edit" else "images"): (
            images_b64[0] if endpoint == "edit" else images_b64
        ),
        **tier_field,
    }
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
    data = resp.json()
    # Response shape INFERRED: {data:[{b64_json|url, content_violation}]}. VERIFY.
    item = (data.get("data") or [{}])[0]
    if item.get("b64_json"):
        output_path.write_bytes(base64.b64decode(item["b64_json"]))
    elif item.get("url"):
        img = requests.get(item["url"], timeout=timeout_s)
        output_path.write_bytes(img.content)
    else:
        return ReveResponse(output_path, key, False, False, endpoint, cost, exit_code=1)

    shutil.copy2(output_path, cached)
    return ReveResponse(output_path, key, False, False, endpoint, cost)
