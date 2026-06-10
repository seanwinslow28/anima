"""Async subprocess wrapper for Antigravity CLI with image input + stub fallback.

Mirrors code-brain/agents-sdk/lib/cli_runners.py structurally. v2 brainstorm §6
NAMED "Gemini 3.1 Pro via Antigravity CLI" as Em's default — but the 2026-06-02
forensics found agy passed no -m flag, so the Antigravity backend silently served
gemini-3.5-flash (the label was aspirational; see the A2 note below). When the
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
mechanical.

A2 (2026-06-02) — model provenance. A real agy call now REQUIRES an explicit
`model=` (passed as `-m`), recorded on CLIResponse.model and logged; a real call
without a model RAISES (no silent backend-default ever again — that is the bug
this guards: `agy -p` with no -m ran the backend-default Flash on 272/272 Em-sized
calls while every label claimed Pro). agy print-mode stdout does not echo the
served model, so the recorded value is the REQUESTED pin, not a stdout
confirmation — which is why both Em (default) and Cy's Pass-3 now run on the
Gemini API transport (gemini_api_runner.run_gemini_api_with_image), where
resp.model_version confirms what actually served. `-m gemini-3.1-pro` is only a
real pin IF the installed agy supports the flag (the findings doc is contradictory
on v1.0.2; unverified) — the 0.62 baseline ran on the backend-default Flash.
"""

from __future__ import annotations

import asyncio
import json
import logging
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

_LOG = logging.getLogger("anima.cli_runners")


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
    # The model explicitly pinned for this call (A2 provenance). None on the stub
    # path (not a costed call). A real call without a pin is refused, so a non-stub
    # CLIResponse always carries the model the call requested via `-m` — never the
    # silent Antigravity backend-default that mislabeled 272 calls (2026-06-02).
    model: str | None = None

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
            "and authenticate (and pass an explicit model=, per A2) to get real "
            "Gemini critique against the pencil-test aesthetic."
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
    model: str | None = None,
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

    `model` (A2, 2026-06-02): a REAL agy call requires an explicit model pin — it
    is passed as `-m <model>` and recorded on the response. A real call WITHOUT a
    model is refused (ValueError), because the bug this guards against is exactly
    `agy -p` with no -m silently running the Antigravity backend-default while every
    label claimed something else (272/272 Em-sized calls; the two Cy Bibles too).
    Note: agy print-mode stdout does not echo the served model, so the recorded
    model is the REQUESTED pin, not a stdout-confirmation — the limitation that
    motivated routing Cy's costed verification through the Gemini API transport
    (run_gemini_api_with_image), where resp.model_version confirms what served. The
    stub path needs no model (it is not a costed call). See the provenance kickoff §A2.
    """
    if shutil.which(ANTI_GRAVITY_BIN) is None:
        return _stub_response(prompt, image_paths)

    # No silent backend-default ever again (A2). A real, costed agy call must pin a
    # model by ID; refuse otherwise rather than let the backend choose unobserved.
    if not model:
        raise ValueError(
            "run_antigravity_with_image: a real agy call requires an explicit "
            "model= (pin by ID — no silent Antigravity backend-default; see the "
            "2026-06-02 provenance forensics). Pass model=, or use the Gemini API "
            "transport (run_gemini_api_with_image), which confirms the served model "
            "from resp.model_version."
        )

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
        "-m",
        model,
        *add_dirs,
        "-p",
        full_prompt,
    ]
    # Provenance log (A2): record the model we pinned for this costed agy call.
    _LOG.info("agy vision call: requested model=%s via -m", model)

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
            model=model,
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
            model=model,
        )
    except FileNotFoundError:
        # Race: which() returned a path but the binary disappeared. Fall
        # back to the stub rather than crashing the critic.
        return _stub_response(prompt, image_paths)


# --------------------------------------------------------------------------- #
# Codex transport (Codie — T3 production peer).                                #
#                                                                              #
# Sibling of run_antigravity_with_image, structurally mirroring the proven     #
# code-brain vault_critic run_codex (`codex exec --sandbox read-only           #
# --skip-git-repo-check <prompt>`, run from $HOME). The differences vs agy:    #
#   - No required model pin. codex selects its model from ~/.codex/config.toml #
#     by default; `model=` is OPTIONAL and only appended as `--model` when      #
#     given (unlike agy, where the silent-backend-default forensics forced a    #
#     required pin — codex has no such trap here).                              #
#   - Image attachment is UNVERIFIED on this machine (codex absent at build     #
#     time — see docs/research/2026-06-10-t3-cli-multimodal-smoke.md). The      #
#     live `-i/--image` invocation is confirmed in Session B; the stub path is  #
#     what CI exercises, so the build is unblocked.                             #
# Honesty contract is identical: empty-stdout-on-exit-0 OR a quota signal       #
# RAISES RateCapExhausted (never a silent verdict); a timeout returns exit 124. #
# --------------------------------------------------------------------------- #

CODEX_BIN = "codex"


def _codex_stub_response(prompt: str, image_paths: list[Path]) -> CLIResponse:
    """Deterministic structured stub for Codie when the codex binary is absent.

    Mirrors _stub_response (borderline@0.65, cites AC01 so the cites_criteria
    invariant holds) but tagged cli="codex" with codex-specific install hint."""
    payload = {
        "verdict": "borderline",
        "confidence": 0.65,
        "reasoning": (
            "STUB FALLBACK — codex binary not found on PATH. Returning a "
            "borderline verdict at confidence 0.65 so the council fan-out and "
            "downstream contract tests exercise the full path without credentials. "
            "Install the Codex CLI and authenticate to get a real production-lens "
            "critique from Codie."
        ),
        "proposed_patches": [],
        "cites_criteria": ["AC01"],
    }
    return CLIResponse(
        cli="codex",
        text=json.dumps(payload),
        tokens=None,
        duration_s=0.0,
        exit_code=0,
        rate_capped=False,
        error=None,
        stub_fallback=True,
    )


async def run_codex_with_image(
    *,
    prompt: str,
    image_paths: list[Path],
    timeout_s: int = 120,
    model: str | None = None,
) -> CLIResponse:
    """Invoke `codex exec` with a prompt + optional image(s); stub when absent.

    Returns CLIResponse(cli="codex"). Falls back to a deterministic stub when
    the binary isn't on PATH so the council suite stays green on a fresh
    machine. `model` is optional — appended as `--model <model>` only if given
    (codex otherwise uses its config.toml default; there is no silent-backend
    trap to guard against, unlike agy's `-m`).

    Image attachment uses `-i <path>` per image (Codex's documented multimodal
    flag). VERIFIED LIVE against codex-cli 0.139.0 (Session B, 2026-06-10): the
    prompt positional MUST precede the `-i` flags — `-i/--image <FILE>...` is
    variadic and otherwise swallows the prompt (codex then reads from stdin and
    exits 1). See test_codex_prompt_precedes_image_flags + the smoke-doc append.
    """
    if shutil.which(CODEX_BIN) is None:
        return _codex_stub_response(prompt, image_paths)

    start = time.monotonic()
    cmd: list[str] = [CODEX_BIN, "exec", "--sandbox", "read-only", "--skip-git-repo-check"]
    if model:
        cmd += ["--model", model]
    # The prompt MUST be the positional and MUST precede the image flags. `-i,
    # --image <FILE>...` is VARIADIC (codex-cli 0.139.0) — a prompt placed after
    # `-i` is swallowed as an extra image, and codex falls back to reading the
    # prompt from stdin ("No prompt provided via stdin", exit 1). Verified live in
    # Session B (2026-06-10); see test_codex_prompt_precedes_image_flags.
    cmd.append(prompt)
    for p in image_paths:
        cmd += ["-i", str(Path(p).resolve())]
    _LOG.info("codex exec call: model=%s images=%d", model or "<config-default>", len(image_paths))

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(Path.home()),
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout_s)
        text = stdout.decode("utf-8", errors="replace")
        err_text = stderr.decode("utf-8", errors="replace")
        exit_code = proc.returncode or 0
        # Same honesty contract as agy: empty stdout on exit-0, or an explicit
        # quota signal in stderr, RAISES — never degrade to a silent verdict.
        quota_signal = any(sig in err_text.lower() for sig in _QUOTA_SIGNALS)
        if exit_code == 0 and (not text.strip() or quota_signal):
            raise RateCapExhausted(
                f"codex returned a quota-exhausted/empty response "
                f"(empty_stdout={not text.strip()}, quota_signal={quota_signal}). "
                "Treating as missing data, not a verdict — Codie must error/escalate, "
                "never silently borderline."
            )
        return CLIResponse(
            cli="codex",
            text=text,
            tokens=None,
            duration_s=time.monotonic() - start,
            exit_code=exit_code,
            rate_capped=False,
            error=err_text if proc.returncode else None,
            model=model,
        )
    except asyncio.TimeoutError:
        return CLIResponse(
            cli="codex",
            text="",
            tokens=None,
            duration_s=time.monotonic() - start,
            exit_code=124,
            rate_capped=False,
            error=f"timeout after {timeout_s}s",
            model=model,
        )
    except FileNotFoundError:
        # Race: which() returned a path but the binary disappeared.
        return _codex_stub_response(prompt, image_paths)
