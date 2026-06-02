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

class RateCapExhausted(Exception):
    """agy returned a quota-exhausted / empty response (not a verdict).

    Distinct from a JSON-parse failure (the documented defensive-borderline mode):
    this means the upstream quota is exhausted and Em received NO usable answer.
    Callers must surface it as an errored gap or escalate — never silently
    borderline. See docs/anima-test-runs/2026-06-01-em-critic-spine-hardening-
    postmortem.md (the bake-off finding)."""


ANTI_GRAVITY_BIN = "agy"

# Signatures that mean the upstream quota is exhausted. agy writes these to its
# LOG FILE (and sometimes stderr); they are NOT in stdout. Treated as a RAISE,
# distinct from a non-empty-but-malformed response (defensive-borderline).
_QUOTA_SIGNALS = ("429", "resource_exhausted", "quota", "rate limit", "rate-limited")

# Best-effort candidate paths for agy's recent log (filled from Task 1 Step 3;
# empty tuple is fine — signal (a) empty-stdout still catches the observed bug).
_AGY_LOG_CANDIDATES: tuple[str, ...] = ()


def _read_agy_log() -> str:
    """Best-effort read of agy's recent log tail, where it writes 429 /
    RESOURCE_EXHAUSTED that don't appear on stderr. Returns '' if no log can be
    located/read — in which case the empty-stdout signal still catches the
    observed quota failure. Monkeypatched in tests."""
    from pathlib import Path as _Path
    for candidate in _AGY_LOG_CANDIDATES:
        try:
            p = _Path(candidate).expanduser()
            if p.exists():
                return p.read_text(encoding="utf-8", errors="replace")[-4000:]
        except OSError:
            continue
    return ""


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
    # agy v1.0.2 reads image / file references when the workspace contains
    # them. The pre-Antigravity Gemini CLI's `@path` syntax did not carry
    # forward — instead, you pass each image's parent via `--add-dir` to
    # grant workspace access, and reference the path as plain text in the
    # prompt body. agy resolves the read via its built-in file tool.
    if image_paths:
        attachments = "\n\nAttached images:\n" + "\n".join(str(p) for p in image_paths)
        full_prompt = prompt + attachments
    else:
        full_prompt = prompt
    # One --add-dir per unique parent directory of the image paths so agy
    # can resolve any of them. De-duped to keep the command line tight.
    add_dirs: list[str] = []
    seen_dirs: set[str] = set()
    for p in image_paths:
        parent = str(Path(p).resolve().parent)
        if parent not in seen_dirs:
            seen_dirs.add(parent)
            add_dirs.extend(["--add-dir", parent])
    # `-p` is the only print-mode flag; there is no `--output-format json`.
    # Output comes back as raw text; the model's system prompt (Em's role
    # addendum) tells it to return a JSON envelope, which `vision_critic.py`'s
    # parser strips of any code fence before json.loads.
    #
    # --dangerously-skip-permissions: required in headless mode. Without it
    # agy blocks waiting for an interactive permission grant when the prompt
    # references a file. Em runs read-only against project images; no tool
    # permissions to be tightened.
    cmd: list[str] = [
        ANTI_GRAVITY_BIN,
        "--dangerously-skip-permissions",
        *add_dirs,
        "-p",
        full_prompt,
    ]

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=timeout_s
        )
        text = stdout.decode("utf-8", errors="replace")
        err_text = stderr.decode("utf-8", errors="replace")
        exit_code = proc.returncode or 0
        # Rate-cap / quota detection (spec §6). Two RAISE signals, kept distinct
        # from a parse failure:
        #   (a) empty/whitespace stdout on exit-0  — the observed failure; primary.
        #   (b) an explicit quota signal in stderr OR agy's log  — corroborating.
        # A NON-EMPTY but unparseable response is NOT a rate cap: it returns
        # normally and vision_critic._parse handles it as defensive-borderline.
        combined = (err_text + "\n" + _read_agy_log()).lower()
        quota_signal = any(sig in combined for sig in _QUOTA_SIGNALS)
        if exit_code == 0 and (not text.strip() or quota_signal):
            raise RateCapExhausted(
                f"agy returned a quota-exhausted/empty response "
                f"(empty_stdout={not text.strip()}, quota_signal={quota_signal}). "
                "Treating as missing data, not a verdict — Em must error/escalate, "
                "never silently borderline."
            )
        return CLIResponse(
            cli="antigravity",
            text=text,
            tokens=None,
            duration_s=time.monotonic() - start,
            exit_code=exit_code,
            rate_capped=False,
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
