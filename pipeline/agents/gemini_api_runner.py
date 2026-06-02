"""anima — Gemini-API vision transport for Em (T2 vision critic).

A drop-in alternative to pipeline.agents.cli_runners.run_antigravity_with_image:
same `(*, prompt, image_paths, timeout_s)` signature, same `.text`-bearing
response, same RateCapExhausted honesty contract. Added 2026-06-02 to unblock
the live re-baseline when agy's personal-tier Gemini quota is 429-exhausted
(field report 2026-06-02). This path calls the Gemini API directly via
google-genai with GEMINI_API_KEY (a SEPARATE vendor billing line from agy's
Google personal OAuth), so it does not share agy's exhausted consumer quota.

Transport-only swap: the MODEL is held constant (GEMINI_VISION_MODEL pins
gemini-3.5-flash — the model agy actually ran for the 0.62 baseline, per the
Task 4 log forensics; see the constant's comment). References, criteria, and the
Opus-SDK escalation are built upstream in vision_critic; this module only
delivers the images + prompt and returns raw text in the shape Em's _parse
already consumes.

# The honesty contract (mirrors cli_runners)
An empty response or an explicit quota signal RAISES RateCapExhausted — Em must
surface it as an errored gap or escalate, never silently degrade to borderline.
A non-empty-but-malformed response is NOT a rate cap: it returns normally and
vision_critic._parse handles it as defensive-borderline. A non-quota hard error
returns an errored response (empty text + error set) → Em's empty-cites invariant
turns it into an honest errored gap, parallel to the agy path's non-zero exit.

# Stub fallback
When google-genai is unavailable OR GEMINI_API_KEY is absent, a deterministic
borderline@0.65 stub (cites AC01, so the cites_criteria invariant is satisfied)
keeps the contract suite green credential-free — the same ladder as cli_runners
and nb_pro_runner.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from dataclasses import dataclass
from pathlib import Path

# Reuse the agy wrapper's exception so vision_critic's propagation is unchanged
# regardless of which transport produced the gap.
from pipeline.agents.cli_runners import RateCapExhausted

_LOG = logging.getLogger("anima.gemini_api_runner")

# The pinned model. SINGLE SOURCE of the model pin — held CONSTANT vs the
# reference-blind baseline so the re-baseline isolates the references lift, not a
# model change. Validity gate (runbook Task 4, verified 2026-06-02): agy passes
# no -m flag, so its print-mode calls log model="" and the Antigravity backend
# picks the model. Across 272/272 Em-sized agy calls — spanning the 2026-06-01
# 0.62 baseline AND the 2026-06-02 attempts — the propagated backend model was
# "Gemini 3.5 Flash (Medium)", never Pro. So the 0.62 baseline ran on Flash; the
# manifest's "gemini-3.1-pro-via-anti-gravity" label was aspirational. Sean
# confirmed (2026-06-02) the pin holds the model constant at gemini-3.5-flash;
# Pro is a separate model-upgrade experiment. The bare API name is
# "gemini-3.5-flash" (models.list exposes it exactly).
GEMINI_VISION_MODEL = "gemini-3.5-flash"

# Substrings that mean the upstream quota is exhausted (raise, don't degrade).
_QUOTA_SIGNALS = ("429", "resource_exhausted", "quota", "rate limit", "rate-limited")

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_ENV_FILE = _PROJECT_ROOT / ".env"


@dataclass(frozen=True)
class GeminiAPIResponse:
    """Result of one Gemini-API vision call. Parallel to cli_runners.CLIResponse;
    `text` is the raw model response Em's _parse consumes."""

    model: str
    text: str
    duration_s: float
    exit_code: int
    error: str | None
    stub_fallback: bool = False

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and self.error is None


def _genai_available() -> bool:
    try:
        from google import genai  # noqa: F401
        return True
    except ImportError:
        return False


def _resolve_gemini_key() -> str | None:
    """GEMINI_API_KEY from the live env first, then the project .env (the same
    source nb_pro_runner honors, so a populated-.env machine behaves identically
    whether or not the var is exported)."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    if not _ENV_FILE.exists():
        return None
    try:
        for line in _ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() == "GEMINI_API_KEY":
                v = v.strip().strip("'\"")
                if v:
                    return v
    except OSError:
        return None
    return None


def _has_gemini_api_key() -> bool:
    return _resolve_gemini_key() is not None


_MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}


def _stub_response(prompt: str, image_paths: list[Path]) -> GeminiAPIResponse:
    """Deterministic borderline@0.65 stub (cites AC01) — mirrors cli_runners._stub_response."""
    payload = {
        "verdict": "borderline",
        "confidence": 0.65,
        "reasoning": (
            "STUB FALLBACK — google-genai or GEMINI_API_KEY unavailable. Borderline "
            "@0.65 so the escalation hatch and contract tests exercise the full path. "
            "Set GEMINI_API_KEY (and `pip install google-genai`) for real Gemini "
            "critique via the API transport."
        ),
        "proposed_patches": [],
        "cites_criteria": ["AC01"],
    }
    return GeminiAPIResponse(
        model="stub-fallback",
        text=json.dumps(payload),
        duration_s=0.0,
        exit_code=0,
        error=None,
        stub_fallback=True,
    )


def _generate(prompt: str, image_paths: list[Path]) -> tuple[str, str]:
    """The blocking google-genai call. Monkeypatched in tests. Prompt FIRST then
    images in their given order (subject = image 1), matching the Opus SDK path
    (sdk_runners._invoke_real_vision builds [text, *image_blocks]).

    Returns (text, served_model). The served model is read BACK from the response
    (resp.model_version) rather than echoing the pinned constant — A2's verify-it-
    fired contract (2026-06-02 provenance forensics). Falls back to the requested
    constant only if the SDK omits model_version (we still pinned it in the request,
    so that is an explicit pin, not a silent backend-default)."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=_resolve_gemini_key())
    contents: list = [prompt]
    for p in image_paths:
        path = Path(p)
        contents.append(
            types.Part.from_bytes(
                data=path.read_bytes(),
                mime_type=_MIME.get(path.suffix.lower(), "image/png"),
            )
        )
    resp = client.models.generate_content(model=GEMINI_VISION_MODEL, contents=contents)
    served = getattr(resp, "model_version", None) or GEMINI_VISION_MODEL
    return (resp.text or "", served)


async def run_gemini_api_with_image(
    *,
    prompt: str,
    image_paths: list[Path],
    timeout_s: int = 120,
) -> GeminiAPIResponse:
    """Invoke Gemini via the API with a prompt + one-or-more images. Drop-in for
    run_antigravity_with_image. Removes the Go/Node child entirely — no detach
    gymnastics needed (a plain foreground run is fine)."""
    if not _genai_available() or not _has_gemini_api_key():
        return _stub_response(prompt, image_paths)

    start = time.monotonic()
    served_model = GEMINI_VISION_MODEL  # requested pin; overwritten by the read-back below
    try:
        text, served_model = await asyncio.wait_for(
            asyncio.to_thread(_generate, prompt, image_paths),
            timeout=timeout_s,
        )
    except asyncio.TimeoutError:
        return GeminiAPIResponse(
            model=GEMINI_VISION_MODEL, text="",
            duration_s=time.monotonic() - start, exit_code=124,
            error=f"timeout after {timeout_s}s",
        )
    except RateCapExhausted:
        raise
    except Exception as exc:  # noqa: BLE001 — classify, then re-shape
        msg = str(exc).lower()
        if any(sig in msg for sig in _QUOTA_SIGNALS):
            raise RateCapExhausted(
                f"Gemini API quota-exhausted/rate-limited: {str(exc)[:200]}. "
                "Treating as missing data, not a verdict."
            ) from exc
        return GeminiAPIResponse(
            model=GEMINI_VISION_MODEL, text="",
            duration_s=time.monotonic() - start, exit_code=1,
            error=str(exc)[:500],
        )

    if not text.strip():
        raise RateCapExhausted(
            "Gemini API returned an empty response (exit-0, empty text) — "
            "treating as a quota/refusal gap, not a verdict (parallels agy's "
            "empty-stdout-exit-0 signal)."
        )
    # Provenance log (A2): record the model the API actually SERVED, read back from
    # the response — not just the pinned constant. The line lands in the run logs so
    # a future re-baseline never has to re-derive the model from forensics.
    _LOG.info(
        "gemini-api vision call: served model=%s (requested=%s)",
        served_model, GEMINI_VISION_MODEL,
    )
    return GeminiAPIResponse(
        model=served_model, text=text,
        duration_s=time.monotonic() - start, exit_code=0, error=None,
    )
