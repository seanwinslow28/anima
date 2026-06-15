"""Silent-stub guards — extracted from scripts/author_plan.py (seam #1).

PlannerNode discards SDKResponse.stub_fallback and only reads .text; the Opus
text stub returns a fully-valid three-key envelope, so a stubbed Maya plan
parses cleanly and could pass the human gate undetected. Two guards:

  1. smoke_live_opus() — a cheap real Opus call BEFORE the costed run; raises
     GuardError if the SDK path is stub or the call errors.
  2. scan_stub_marker(paths) — post-hoc scan of emitted artifacts for the
     "STUB FALLBACK" marker. Belt and suspenders.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from pipeline.agents.sdk_runners import invoke_opus_text, invoke_sonnet_text

STUB_MARKER = "STUB FALLBACK"


class GuardError(Exception):
    """A pre/post-run guard failed — do not proceed to (or trust) the costed path."""


def smoke_live_opus() -> None:
    """Cheap real Opus call to confirm the live (non-stub) subscription path.

    Raises GuardError if the SDK is unavailable (stub) or the call errors
    (CLI not authed / API key absent on the fallback path). Subscription-
    absorbed — one tiny prompt.
    """
    print("Smoke: confirming live Opus path (subscription billing)…")
    resp = asyncio.run(invoke_opus_text(prompt="Reply with exactly: SPARK-OK"))
    if resp.stub_fallback:
        raise GuardError(
            "Opus smoke returned a STUB envelope — no real SDK path.\n"
            "  Maya would silently produce a stub plan that parses cleanly and could\n"
            "  pass the human gate. Install claude-agent-sdk and authenticate the\n"
            "  `claude` CLI (subscription), then re-run."
        )
    if not resp.ok:
        raise GuardError(
            f"Opus smoke failed (exit_code={resp.exit_code}, error={resp.error}).\n"
            "  The claude-agent-sdk path is importable but the call did not succeed —\n"
            "  likely the `claude` CLI isn't authenticated, or it fell through to the\n"
            "  anthropic SDK with no ANTHROPIC_API_KEY. Fix auth, then re-run."
        )
    print(f"  live: model={resp.model} duration={resp.duration_s:.1f}s ok=True")


def smoke_live_sonnet() -> None:
    """Cheap real Sonnet call to confirm the live (non-stub) subscription path.

    Bea (the storyboard artist) authors through invoke_sonnet_text, so her driver
    smokes Sonnet — not Opus. Raises GuardError if the SDK is unavailable (stub)
    or the call errors. Subscription-absorbed — one tiny prompt.
    """
    print("Smoke: confirming live Sonnet path (subscription billing)…")
    resp = asyncio.run(invoke_sonnet_text(prompt="Reply with exactly: BOARD-OK"))
    if resp.stub_fallback:
        raise GuardError(
            "Sonnet smoke returned a STUB envelope — no real SDK path.\n"
            "  Bea would silently produce a stub board that parses cleanly and could\n"
            "  pass the human gate. Install claude-agent-sdk and authenticate the\n"
            "  `claude` CLI (subscription), then re-run."
        )
    if not resp.ok:
        raise GuardError(
            f"Sonnet smoke failed (exit_code={resp.exit_code}, error={resp.error}).\n"
            "  The claude-agent-sdk path is importable but the call did not succeed —\n"
            "  likely the `claude` CLI isn't authenticated, or it fell through to the\n"
            "  anthropic SDK with no ANTHROPIC_API_KEY. Fix auth, then re-run."
        )
    print(f"  live: model={resp.model} duration={resp.duration_s:.1f}s ok=True")


def scan_stub_marker(paths: list[Path]) -> bool:
    """True if any existing artifact carries the STUB FALLBACK marker."""
    for p in paths:
        p = Path(p)
        if p.exists() and STUB_MARKER in p.read_text(encoding="utf-8"):
            return True
    return False
