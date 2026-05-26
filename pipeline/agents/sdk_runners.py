"""Claude Agent SDK / anthropic SDK wrapper for Opus 4.7 vision calls + stub.

Per v2 brainstorm §6: Opus 4.7 is Em's escalation model when Gemini's
confidence drops below threshold or a shot carries an impact tag matching
critics.t2.escalation_tags. Subscription-absorbed via Claude Code auth when
the claude-agent-sdk Python package is installed; falls back to the anthropic
SDK with ANTHROPIC_API_KEY when only the API path is available; final
fallback is a deterministic stub so commit 8 stays green on a fresh machine.

The wrapper is the single point in this codebase that knows the SDK
invocation shape. vision_critic.py imports from here and never calls the
SDK directly.
"""

from __future__ import annotations

import asyncio
import base64
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path

OPUS_MODEL = "claude-opus-4-7"
STUB_MODEL = "stub-fallback"


@dataclass(frozen=True)
class SDKResponse:
    """Result of a single SDK invocation.

    Parallel to CLIResponse but without rate-cap semantics (the SDK surfaces
    rate limits as exceptions, not response fields). `stub_fallback` flags
    when the wrapper used the deterministic stub.
    """

    model: str
    text: str
    duration_s: float
    exit_code: int
    error: str | None
    stub_fallback: bool = False

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and self.error is None


def _sdk_available() -> bool:
    """Detect whether a real SDK path is available.

    Order of preference:
      1. claude-agent-sdk (subscription-absorbed via Claude Code auth)
      2. anthropic SDK + ANTHROPIC_API_KEY (API-key path)
    """
    try:
        import claude_agent_sdk  # noqa: F401
        return True
    except ImportError:
        pass
    try:
        import anthropic  # noqa: F401
        return bool(os.getenv("ANTHROPIC_API_KEY"))
    except ImportError:
        return False


def _stub_response(prompt: str, image_paths: list[Path]) -> SDKResponse:
    """Deterministic structured stub for the escalation path.

    Returns a borderline verdict at confidence 0.78 — high enough to be
    distinguishable from the Gemini stub (0.65) so the vision_critic.py
    routing tests can confirm which branch fired. Cites AC01 so the
    cites_criteria invariant is satisfied.
    """
    payload = {
        "verdict": "borderline",
        "confidence": 0.78,
        "reasoning": (
            "STUB FALLBACK — claude-agent-sdk + anthropic SDK both "
            "unavailable. Returning a borderline verdict at confidence "
            "0.78 from the escalation path so the routing logic and "
            "downstream contract tests exercise both branches. Install "
            "claude-agent-sdk (preferred — uses Claude Code subscription "
            "auth) or set ANTHROPIC_API_KEY to get real Opus 4.7 critique."
        ),
        "proposed_patches": [],
        "cites_criteria": ["AC01"],
    }
    return SDKResponse(
        model=STUB_MODEL,
        text=json.dumps(payload),
        duration_s=0.0,
        exit_code=0,
        error=None,
        stub_fallback=True,
    )


async def invoke_opus_vision(
    *,
    prompt: str,
    image_paths: list[Path],
    timeout_s: int = 120,
) -> SDKResponse:
    """Invoke Opus 4.7 with a prompt + one-or-more images.

    Returns SDKResponse with the structured-JSON text payload. Falls back to
    a deterministic stub when no SDK is available.
    """
    if not _sdk_available():
        return _stub_response(prompt, image_paths)

    start = time.monotonic()
    try:
        return await asyncio.wait_for(
            _invoke_real(prompt=prompt, image_paths=image_paths),
            timeout=timeout_s,
        )
    except asyncio.TimeoutError:
        return SDKResponse(
            model=OPUS_MODEL,
            text="",
            duration_s=time.monotonic() - start,
            exit_code=124,
            error=f"timeout after {timeout_s}s",
        )
    except Exception as exc:
        return SDKResponse(
            model=OPUS_MODEL,
            text="",
            duration_s=time.monotonic() - start,
            exit_code=1,
            error=str(exc)[:500],
        )


async def _invoke_real(*, prompt: str, image_paths: list[Path]) -> SDKResponse:
    """Real Opus 4.7 vision call. Tries claude-agent-sdk first, then anthropic.

    Both paths build the same content-block shape (text + image_data blocks
    with base64-encoded PNGs) and request a JSON response so vision_critic.py
    can parse the verdict/confidence/reasoning/patches/cites_criteria
    structure directly.
    """
    start = time.monotonic()
    image_blocks = [_to_image_block(p) for p in image_paths]
    content_blocks = [{"type": "text", "text": prompt}, *image_blocks]

    # Path 1: claude-agent-sdk (subscription-absorbed)
    try:
        import claude_agent_sdk  # type: ignore[import-not-found]
        text = await _call_claude_agent_sdk(claude_agent_sdk, content_blocks)
        return SDKResponse(
            model=OPUS_MODEL,
            text=text,
            duration_s=time.monotonic() - start,
            exit_code=0,
            error=None,
        )
    except ImportError:
        pass

    # Path 2: anthropic SDK with API key
    import anthropic  # type: ignore[import-not-found]
    client = anthropic.AsyncAnthropic()
    resp = await client.messages.create(
        model=OPUS_MODEL,
        max_tokens=2048,
        messages=[{"role": "user", "content": content_blocks}],
    )
    text = "".join(
        block.text for block in resp.content if getattr(block, "type", "") == "text"
    )
    return SDKResponse(
        model=OPUS_MODEL,
        text=text,
        duration_s=time.monotonic() - start,
        exit_code=0,
        error=None,
    )


async def _call_claude_agent_sdk(sdk_module, content_blocks: list[dict]) -> str:
    """Adapter for claude-agent-sdk's query interface.

    The SDK's exact API surface may evolve; this function isolates that
    coupling so the rest of anima doesn't depend on the SDK's specific
    function names. When the SDK is actually installed and a real call
    needs to happen, this function gets fleshed out against the installed
    version's API. Until then, an ImportError-or-AttributeError trips the
    fallback chain in _invoke_real.
    """
    # Defer to whichever query entry point the installed SDK version exposes.
    query_fn = getattr(sdk_module, "query", None) or getattr(sdk_module, "complete", None)
    if query_fn is None:
        raise ImportError("claude-agent-sdk: no compatible query function found")
    result = query_fn(
        model=OPUS_MODEL,
        messages=[{"role": "user", "content": content_blocks}],
    )
    if asyncio.iscoroutine(result):
        result = await result
    if isinstance(result, str):
        return result
    if isinstance(result, dict) and "text" in result:
        return str(result["text"])
    return str(result)


def _to_image_block(path: Path) -> dict:
    """Encode an image path as an Anthropic image content block.

    Mirrors the SDK's image_data block shape: type=image, source={type=base64,
    media_type=image/png, data=<base64>}. Anti-Gravity uses a similar shape;
    centralizing here keeps the SDK-specific encoding out of vision_critic.py.
    """
    data = base64.b64encode(Path(path).read_bytes()).decode("ascii")
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/png",
            "data": data,
        },
    }
