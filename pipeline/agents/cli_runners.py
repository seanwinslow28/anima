"""Async subprocess wrapper for Antigravity CLI with image input + stub fallback.

Mirrors code-brain/agents-sdk/lib/cli_runners.py structurally. v2 brainstorm §6
locked Gemini 3.1 Pro via Antigravity CLI as Em's default model. When the
binary is not on PATH (typical for fresh machines, CI, or first-hour
verification), the stub fallback returns a deterministic structured response so
tests stay green and the routing logic in vision_critic.py is verifiable
offline.

Subscription-absorbed in production via Sean's Google personal OAuth on the
Antigravity CLI. The wrapper is the single point in this codebase that knows
the CLI's invocation flags and rate-cap signatures; vision_critic.py imports
from here and never shells out directly.

Commit 8.1 (2026-05-27) migrated from the pre-Antigravity Gemini CLI to the
new `agy` binary per docs/research/2026-05-26-anti-gravity-cli-findings.md:
- ANTI_GRAVITY_BIN: `anti-gravity` → `agy`
- Flag shape: `--prompt PROMPT --json --image PATH` → `-p PROMPT --output-format json`
- Image attachment: `--image PATH` flag → `@path` inline references in prompt text
The sunset for the consumer-tier Gemini CLI is 2026-06-18; the migration is
mechanical and Gemini 3.1 Pro stays accessible by name.
"""

from __future__ import annotations

import asyncio
import json
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

ANTI_GRAVITY_BIN = "agy"

# Signatures the wrapper recognizes as rate-capped responses. Per the
# vault_critic precedent, treat rate-capped responses as failures even when
# exit_code == 0 — the CLI sometimes returns success with empty body when
# the upstream quota is exhausted.
_RATE_CAP_SIGNALS = ("rate limit", "quota", "429", "rate-limited")


@dataclass(frozen=True)
class CLIResponse:
    """Result of a single CLI invocation.

    `text` is the raw JSON response (Anti-Gravity's `response` field surfaced as
    stdout in --json mode). `tokens` is None when the CLI did not report a
    count. `rate_capped` is set by the wrapper when the CLI's stderr matches
    a known signature; callers MUST treat rate-capped responses as failures
    even if exit_code == 0. `stub_fallback` is True when the wrapper used the
    deterministic stub because the binary wasn't on PATH; `.ok` returns True
    for stub responses so callers can rely on the payload shape.
    """

    cli: Literal["antigravity", "codex"]
    text: str
    tokens: int | None
    duration_s: float
    exit_code: int
    rate_capped: bool
    error: str | None
    stub_fallback: bool = False

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and not self.rate_capped and self.error is None


def _stub_response(prompt: str, image_paths: list[Path]) -> CLIResponse:
    """Deterministic structured stub response.

    Returns a borderline verdict at confidence 0.65 so the escalation hatch
    in vision_critic.py (threshold default 0.7) exercises the Opus path on
    every stub-only run. The cites_criteria list carries AC01 so the
    cites_criteria invariant in VisionCriticNode.run() is satisfied.
    """
    payload = {
        "verdict": "borderline",
        "confidence": 0.65,
        "reasoning": (
            "STUB FALLBACK — agy binary not found on PATH. Returning a "
            "borderline verdict at confidence 0.65 so the escalation hatch "
            "and downstream contract tests exercise the full path. Install "
            "the Antigravity CLI (curl -fsSL https://antigravity.google/cli/install.sh | bash) "
            "and authenticate to get real Gemini 3.1 Pro critique against "
            "the pencil-test aesthetic."
        ),
        "proposed_patches": [],
        "cites_criteria": ["AC01"],
    }
    return CLIResponse(
        cli="antigravity",
        text=json.dumps(payload),
        tokens=None,
        duration_s=0.0,
        exit_code=0,
        rate_capped=False,
        error=None,
        stub_fallback=True,
    )


async def run_antigravity_with_image(
    *,
    prompt: str,
    image_paths: list[Path],
    timeout_s: int = 120,
) -> CLIResponse:
    """Invoke Antigravity CLI with a prompt + one-or-more images.

    Returns CLIResponse with the parsed text, exit code, and rate-cap status.
    Falls back to a deterministic stub when the binary isn't on PATH so
    commit 8's tests stay green on a fresh machine and the stub trace under
    evals/vision-critic/traces/baseline-2026-05-26.md is reproducible.

    Image attachment uses the `@path` inline syntax (the Gemini CLI idiom
    carried forward into Antigravity CLI per the migration findings doc),
    not a separate `--image` flag. The wrapper formats image paths into the
    prompt body and lets the agent's file-reading capability resolve them.
    """
    if shutil.which(ANTI_GRAVITY_BIN) is None:
        return _stub_response(prompt, image_paths)

    start = time.monotonic()
    if image_paths:
        attachments = "\n\nAttached images:\n" + "\n".join(f"@{p}" for p in image_paths)
        full_prompt = prompt + attachments
    else:
        full_prompt = prompt
    cmd: list[str] = [ANTI_GRAVITY_BIN, "-p", full_prompt, "--output-format", "json"]

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=timeout_s
        )
        text = stdout.decode("utf-8", errors="replace")
        err_text = stderr.decode("utf-8", errors="replace")
        rate_capped = any(sig in err_text.lower() for sig in _RATE_CAP_SIGNALS)
        return CLIResponse(
            cli="antigravity",
            text=text,
            tokens=None,
            duration_s=time.monotonic() - start,
            exit_code=proc.returncode or 0,
            rate_capped=rate_capped,
            error=err_text if proc.returncode else None,
        )
    except asyncio.TimeoutError:
        return CLIResponse(
            cli="antigravity",
            text="",
            tokens=None,
            duration_s=time.monotonic() - start,
            exit_code=124,
            rate_capped=False,
            error=f"timeout after {timeout_s}s",
        )
    except FileNotFoundError:
        # Race: which() returned a path but the binary disappeared. Fall
        # back to the stub rather than crashing the critic.
        return _stub_response(prompt, image_paths)
