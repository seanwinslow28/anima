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
SONNET_MODEL = "claude-sonnet-4-6"
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

    Vision via claude-agent-sdk uses the async-iterable form of `query` so
    image content blocks ride alongside the text in the user message. The
    anthropic SDK path builds the equivalent `messages.create` payload.
    Both return JSON conforming to vision_critic.py's parser expectations
    (the model's system prompt instructs the JSON schema).
    """
    start = time.monotonic()
    image_blocks = [_to_image_block(p) for p in image_paths]
    content_blocks = [{"type": "text", "text": prompt}, *image_blocks]

    # Path 1: claude-agent-sdk (subscription-absorbed via `claude` CLI)
    try:
        import claude_agent_sdk  # type: ignore[import-not-found]
        try:
            text = await _call_csdk(
                claude_agent_sdk,
                model=OPUS_MODEL,
                content_blocks=content_blocks,
            )
            return SDKResponse(
                model=OPUS_MODEL,
                text=text,
                duration_s=time.monotonic() - start,
                exit_code=0,
                error=None,
            )
        except claude_agent_sdk.CLINotFoundError:
            # `claude` CLI not installed — fall through to anthropic SDK.
            pass
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


async def _call_csdk(
    sdk_module,
    *,
    model: str,
    content_blocks: list[dict] | None = None,
    text_prompt: str | None = None,
) -> str:
    """Adapter for claude-agent-sdk's actual API (v0.2.x).

    The SDK's `query()` returns an AsyncIterator of {User, Assistant, System,
    Result}Message + StreamEvent + RateLimitEvent. We collect text from
    AssistantMessage.content TextBlocks; AssistantMessage.error surfaces
    auth/billing/rate-limit conditions which we promote to a raised exception
    so the outer wrapper's error-path catches them.

    Two call shapes:
      - text-only: pass `text_prompt=str` (string prompt to query())
      - with images: pass `content_blocks=[...text+image]` (async-iterable
        prompt yielding a user message with mixed text + image content)
    """
    options = sdk_module.ClaudeAgentOptions(
        model=model,
        # Headless mode — no tools, single turn, bypass interactive permission
        # prompts. Maya and Em both want one structured response, no tool use.
        permission_mode="bypassPermissions",
        max_turns=1,
        allowed_tools=[],
        disallowed_tools=[],
    )

    if text_prompt is not None:
        # Text-only path — string prompt is the simplest form.
        return await _drain_csdk_query(sdk_module, prompt=text_prompt, options=options)

    if content_blocks is None:
        raise ValueError("_call_csdk requires either text_prompt or content_blocks")

    # Vision path — wrap content blocks in the SDK's async-iterable message
    # stream so image content rides alongside text in a user message.
    async def message_stream():
        yield {
            "type": "user",
            "message": {
                "role": "user",
                "content": content_blocks,
            },
        }

    return await _drain_csdk_query(sdk_module, prompt=message_stream(), options=options)


async def _drain_csdk_query(sdk_module, *, prompt, options) -> str:
    """Iterate the SDK's AsyncIterator, collect assistant text, raise on error."""
    text_parts: list[str] = []
    async for msg in sdk_module.query(prompt=prompt, options=options):
        if isinstance(msg, sdk_module.AssistantMessage):
            if msg.error:
                raise RuntimeError(f"claude-agent-sdk error: {msg.error}")
            for block in msg.content:
                if isinstance(block, sdk_module.TextBlock):
                    text_parts.append(block.text)
    return "".join(text_parts)


# ---------------------------------------------------------------------------
# Text-only invocations (Maya — commit 3)
#
# Maya's three-phase flow needs text-only calls to Opus + Sonnet (no images;
# the brief is markdown). Stubs return deterministic JSON shaped for the
# planner's _parse_opus and _parse_sonnet helpers so commit 3 tests stay
# green on a fresh machine.
# ---------------------------------------------------------------------------


def _stub_opus_text(prompt: str) -> SDKResponse:
    """Stub planning envelope. Shape matches Maya's _parse_opus expectations."""
    payload = {
        "production_brief_md": (
            "---\npiece_id: \"stub-piece\"\nphases_enabled: [0, 5, 6, 8]\n"
            "characters_loaded: [sean-anchor]\ntarget_medium: gif\n---\n\n"
            "# Production Brief (STUB)\n\nSTUB FALLBACK — Opus SDK unavailable. "
            "Maya's primary pass returned this deterministic envelope so "
            "downstream tests exercise the parser + audit shape end-to-end. "
            "Install claude-agent-sdk or set ANTHROPIC_API_KEY for real planning."
        ),
        "criteria_json": {
            "version": "1.1",
            "locked": False,
            "criteria": [
                {
                    "id": "AC.technical.aspect-ratio-16-9",
                    "description": "STUB criterion — every frame is 16:9 within 2% tolerance.",
                    "cites_phase": [5],
                    "cites_personas": ["em"],
                    "impact_tag": "structural",
                    "parent_id": None,
                    "derived_from": ["production_brief.target_medium"],
                }
            ],
        },
        "plan_md": (
            "# Plan (STUB)\n\nSTUB FALLBACK — Opus SDK unavailable. "
            "Maya's clean-markdown plan output would render here.\n\n"
            "## Cost preview\n\nStub run: $0 incremental (subscription-absorbed agents only).\n"
        ),
    }
    return SDKResponse(
        model=STUB_MODEL,
        text=json.dumps(payload),
        duration_s=0.0,
        exit_code=0,
        error=None,
        stub_fallback=True,
    )


def _stub_sonnet_text(prompt: str) -> SDKResponse:
    """Stub adversarial-validation envelope. Shape matches _parse_sonnet."""
    payload = {
        "flag": None,
        "low_signal": True,
        "reasoning": (
            "STUB FALLBACK — Sonnet SDK unavailable. Returning low_signal=True "
            "so Maya's escalation hatch fires a second Opus pass on the routing "
            "test. Install claude-agent-sdk or set ANTHROPIC_API_KEY to get "
            "real adversarial validation."
        ),
    }
    return SDKResponse(
        model=STUB_MODEL,
        text=json.dumps(payload),
        duration_s=0.0,
        exit_code=0,
        error=None,
        stub_fallback=True,
    )


async def invoke_opus_text(
    *,
    prompt: str,
    timeout_s: int = 120,
) -> SDKResponse:
    """Invoke Opus 4.7 with a text-only prompt. Maya's primary + resolution passes."""
    return await _invoke_text(
        model=OPUS_MODEL,
        prompt=prompt,
        timeout_s=timeout_s,
        stub_fn=_stub_opus_text,
    )


async def invoke_sonnet_text(
    *,
    prompt: str,
    timeout_s: int = 120,
) -> SDKResponse:
    """Invoke Sonnet 4.6 with a text-only prompt. Maya's adversarial validation pass."""
    return await _invoke_text(
        model=SONNET_MODEL,
        prompt=prompt,
        timeout_s=timeout_s,
        stub_fn=_stub_sonnet_text,
    )


async def _invoke_text(
    *,
    model: str,
    prompt: str,
    timeout_s: int,
    stub_fn,
) -> SDKResponse:
    """Shared text-only call path. Mirrors invoke_opus_vision sans images."""
    if not _sdk_available():
        return stub_fn(prompt)

    start = time.monotonic()
    try:
        return await asyncio.wait_for(
            _invoke_real_text(model=model, prompt=prompt),
            timeout=timeout_s,
        )
    except asyncio.TimeoutError:
        return SDKResponse(
            model=model,
            text="",
            duration_s=time.monotonic() - start,
            exit_code=124,
            error=f"timeout after {timeout_s}s",
        )
    except Exception as exc:
        return SDKResponse(
            model=model,
            text="",
            duration_s=time.monotonic() - start,
            exit_code=1,
            error=str(exc)[:500],
        )


async def _invoke_real_text(*, model: str, prompt: str) -> SDKResponse:
    """Real text-only call. Mirrors _invoke_real but with no image content blocks."""
    start = time.monotonic()

    # Path 1: claude-agent-sdk (subscription-absorbed via `claude` CLI)
    try:
        import claude_agent_sdk  # type: ignore[import-not-found]
        try:
            text = await _call_csdk(claude_agent_sdk, model=model, text_prompt=prompt)
            return SDKResponse(
                model=model,
                text=text,
                duration_s=time.monotonic() - start,
                exit_code=0,
                error=None,
            )
        except claude_agent_sdk.CLINotFoundError:
            # `claude` CLI not installed — fall through to anthropic SDK.
            pass
    except ImportError:
        pass

    # Path 2: anthropic SDK with API key
    import anthropic  # type: ignore[import-not-found]
    client = anthropic.AsyncAnthropic()
    resp = await client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
    )
    text = "".join(
        block.text for block in resp.content if getattr(block, "type", "") == "text"
    )
    return SDKResponse(
        model=model,
        text=text,
        duration_s=time.monotonic() - start,
        exit_code=0,
        error=None,
    )


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
