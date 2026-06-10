"""fal.ai image-edit transports for Flo's in-between routes — with a credential-free stub.

Two entry points, `invoke_fal_seedream` and `invoke_fal_qwen`, mirroring the shape of
`pipeline/agents/nb_pro_runner.py::invoke_image_edit` and the bake-off's `reve_runner.py`:
a single call that self-stubs when FAL_KEY is absent (placeholder PNG, stub_fallback=True),
a content-addressed cache, and a real path behind `fal_client.subscribe` (the idiom already
in `pipeline/seedance_generate.py`).

SCHEMA STATUS (VERIFIED 2026-06-10, STEP B0) against the live fal OpenAPI — first-party, not
guessed (the reve mirror-schema lesson):
  • Seedream: `fal-ai/bytedance/seedream/v4/edit` — {prompt, image_urls[] (≤10)} required, output
    images[].url. image_size defaults to 2048² SQUARE, so we pass the 16:9 source-frame size.
  • Qwen: `fal-ai/qwen-image-edit-plus` — the MULTI-IMAGE variant ({prompt, image_urls[]}). The base
    `fal-ai/qwen-image-edit` takes a single image_url and is unusable for a two-endpoint in-between.
    Knobs: guidance_scale (def 4) + num_inference_steps (def 50). NO denoise/strength is exposed —
    the kickoff's "denoise 0.78–0.82" does not exist on this endpoint (left at fal defaults).
    image_size defaults to square_hd → we pass 16:9. output images[].url.
`_FAL_ENGINES[engine]['verified']` is True for both. The flag stays as a re-gate: a provider bump
that invalidates the schema flips it back to False, restoring the loud refusal. The stub path
(FAL_KEY absent) is CI-green; the unverified-refusal is exercised by forcing verified=False.
"""
from __future__ import annotations

import hashlib
import os
import shutil
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

_REQUEST_TIMEOUT_S = 180

# --- Engine config — endpoint ids are CANDIDATES, UNVERIFIED until STEP B0. ---
# `verified` is the reve-fast-version guard generalized: the real path refuses to call an
# endpoint that hasn't been confirmed live, so a wrong-id guess can't silently mis-generate.
# B0 confirms the id + arg schema + output field, then sets verified=True and pins the
# served-model string into the bake-off's variants.yaml `snapshots:` block.
_FAL_ENGINES: dict[str, dict] = {
    "seedream": {
        # VERIFIED 2026-06-10 (B0) against the live fal OpenAPI.
        "endpoint": "fal-ai/bytedance/seedream/v4/edit",
        "verified": True,
        "cost_usd": 0.02,
    },
    "qwen": {
        # VERIFIED 2026-06-10 (B0): the `-plus` MULTI-IMAGE variant (base qwen-image-edit takes a
        # single image_url — unusable for a two-endpoint in-between). ~$0.03/MP.
        "endpoint": "fal-ai/qwen-image-edit-plus",
        "verified": True,
        "cost_usd": 0.03,
    },
}


@dataclass(frozen=True)
class FalResponse:
    output_path: Path
    cache_key: str
    cache_hit: bool
    stub_fallback: bool
    endpoint: str          # "seedream" | "qwen" | "stub"
    cost_usd: float        # published per-image rate for the engine
    exit_code: int = 0

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and Path(self.output_path).exists()


def _has_fal_key() -> bool:
    # Reads os.environ only (NOT the .env file) so `--stub` popping FAL_KEY genuinely
    # disables the live path — see the bake-off's hard short-circuit note.
    return bool(os.environ.get("FAL_KEY"))


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()


def _cache_key(*, prompt: str, references: list[Path], model: str,
               endpoint: str, denoise: float | None) -> str:
    h = hashlib.sha256()
    h.update(prompt.encode("utf-8"))
    h.update(model.encode("utf-8"))
    h.update(endpoint.encode("utf-8"))
    h.update(str(denoise).encode("utf-8"))
    for ref in references:
        h.update(_hash_file(ref).encode("utf-8"))
    return h.hexdigest()


def _write_placeholder_png(path: Path) -> None:
    """Mid-gray 1376×768 placeholder — the stub is NOT a scored claim (DINOv2 against
    it is meaningless; --stub proves plumbing only). Matches reve_runner's placeholder."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (1376, 768), (128, 128, 128)).save(path, "PNG")


def _image_size_for(references: list[Path]) -> dict:
    """16:9-preserving output size = the first reference frame's dimensions. Both fal endpoints
    default to a SQUARE output (Seedream 2048², Qwen square_hd), which would distort the
    pencil-test frames and skew the DINOv2 read against the endpoints."""
    with Image.open(references[0]) as im:
        w, h = im.size
    return {"width": w, "height": h}


def _build_arguments(engine: str, *, prompt: str, image_urls: list[str],
                     image_size: dict, denoise: float | None) -> dict:
    """Construct the fal.subscribe arguments (VERIFIED 2026-06-10 against the live fal OpenAPI).

    Both endpoints take {prompt, image_urls[]} and default to a SQUARE output, so we pass an
    explicit `image_size` matching the source frames. `denoise` is accepted for API symmetry but
    NOT forwarded — neither endpoint exposes a denoise/strength knob (Qwen's cfg lever is
    guidance_scale, left at the fal default 4; Seedream has none)."""
    return {"prompt": prompt, "image_urls": image_urls, "image_size": image_size}


def _extract_output_url(result: object) -> str | None:
    """Pull the generated image URL out of a fal result. VERIFY the field in B0 — fal image
    models commonly return result['images'][0]['url']; some return result['image']['url']."""
    if isinstance(result, dict):
        imgs = result.get("images")
        if isinstance(imgs, list) and imgs and isinstance(imgs[0], dict):
            return imgs[0].get("url")
        img = result.get("image")
        if isinstance(img, dict):
            return img.get("url")
    return None


def _download(url: str, output_path: Path) -> None:
    import urllib.request
    try:
        urllib.request.urlretrieve(url, output_path)
    except Exception:  # noqa: BLE001 — fall back to manual read/write
        with urllib.request.urlopen(url) as resp:
            Path(output_path).write_bytes(resp.read())


def _invoke_fal(
    engine: str,
    *,
    prompt: str,
    reference_images: list[Path],
    output_path: Path,
    cache_dir: Path,
    model: str | None,
    denoise: float | None,
    timeout_s: int,
) -> FalResponse:
    cfg = _FAL_ENGINES[engine]
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    references = [Path(p) for p in reference_images]
    cost = cfg["cost_usd"]
    key = _cache_key(prompt=prompt, references=references,
                     model=model or cfg["endpoint"], endpoint=engine, denoise=denoise)
    cached = cache_dir / f"{key}.png"

    if cached.exists():
        shutil.copy2(cached, output_path)
        return FalResponse(output_path, key, True, False, engine, cost)

    # Stub fallback — no key, no spend. Mirrors invoke_image_edit's gate exactly.
    if not _has_fal_key():
        _write_placeholder_png(output_path)
        shutil.copy2(output_path, cached)
        return FalResponse(output_path, key, False, True, "stub", cost)

    # ---- Real path — REFUSE an unverified endpoint (the reve schema-was-wrong lesson). ----
    if not cfg["verified"]:
        raise RuntimeError(
            f"fal {engine} endpoint {cfg['endpoint']!r} is NOT verified — run STEP B0 "
            f"(probe the live fal model page; confirm the arg schema + output field), then "
            f"set _FAL_ENGINES['{engine}']['verified'] = True. Refusing rather than silently "
            f"calling the wrong model (the reve mirror-schema lesson)."
        )

    try:
        import fal_client  # local import — only the live path needs it
    except ImportError as exc:  # pragma: no cover - environment-dependent
        raise RuntimeError("live fal path needs `fal-client` (pip install fal-client)") from exc

    image_urls = [fal_client.upload_file(str(p)) for p in references]
    arguments = _build_arguments(engine, prompt=prompt, image_urls=image_urls,
                                 image_size=_image_size_for(references), denoise=denoise)
    result = fal_client.subscribe(cfg["endpoint"], arguments=arguments)
    url = _extract_output_url(result)
    if not url:
        return FalResponse(output_path, key, False, False, engine, cost, exit_code=1)
    _download(url, output_path)
    shutil.copy2(output_path, cached)
    return FalResponse(output_path, key, False, False, engine, cost)


def invoke_fal_seedream(
    *,
    prompt: str,
    reference_images: list[Path],
    output_path: Path,
    cache_dir: Path,
    model: str | None = None,
    timeout_s: int = _REQUEST_TIMEOUT_S,
) -> FalResponse:
    """Edit via fal Seedream 4.0 (`…/seedream/v4/edit`), or stub if no FAL_KEY.

    In-betweens pass both endpoint keyframes as `reference_images` (image_urls[]); the prompt
    describes the tween position; output size is forced to the 16:9 source-frame size. Content-
    addressed cache (same prompt+refs+model -> cache hit). Verified B0 2026-06-10.
    """
    return _invoke_fal("seedream", prompt=prompt, reference_images=reference_images,
                       output_path=output_path, cache_dir=cache_dir, model=model,
                       denoise=None, timeout_s=timeout_s)


def invoke_fal_qwen(
    *,
    prompt: str,
    reference_images: list[Path],
    output_path: Path,
    cache_dir: Path,
    model: str | None = None,
    denoise: float | None = None,
    timeout_s: int = _REQUEST_TIMEOUT_S,
) -> FalResponse:
    """Edit via fal Qwen-Image-Edit-Plus (`…/qwen-image-edit-plus`, multi-image), or stub if no
    FAL_KEY.

    Both endpoint keyframes pass as image_urls[]; output size is forced to the 16:9 source-frame
    size. `denoise` is accepted for API symmetry but NOT sent — qwen-image-edit-plus exposes no
    denoise/strength knob (verified B0; its cfg lever is guidance_scale, left at the fal default).
    Content-addressed cache. Verified B0 2026-06-10.
    """
    return _invoke_fal("qwen", prompt=prompt, reference_images=reference_images,
                       output_path=output_path, cache_dir=cache_dir, model=model,
                       denoise=denoise, timeout_s=timeout_s)
