"""Live scored baseline for Em — the deliberate, costed run (NOT a CI default).

Invokes Em real across cases.yaml (agy + Claude Agent SDK present on this
machine), computes the segmented confusion matrix, and writes last-run.md +
a dated baseline trace. Mirrors Mo's --no-sonnet opt-in: --stub forces the
credential-free path so the script is exercisable in CI without a scored claim.

Usage:
    .venv/bin/python -m evals.vision_critic.score            # live
    .venv/bin/python -m evals.vision_critic.score --stub     # credential-free
    .venv/bin/python -m evals.vision_critic.score --model gemini   # one config
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import types
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

from pipeline.agents import AgentContext
from pipeline.agents.vision_critic import VisionCriticNode
from pipeline.agents.reference_selection import select_references
from pipeline.contact_sheet import build_contact_sheet  # noqa: F401 (cases pre-build sheets)
from evals.vision_critic.scoring import CaseScore, segment_report
from evals.vision_critic.conftest import merged_criteria

HERE = Path(__file__).parent
FIXTURES = HERE / "fixtures"
CASES = yaml.safe_load((HERE / "cases.yaml").read_text(encoding="utf-8"))["cases"]


def _manifest() -> dict:
    """The real critics.t2 config + the locked Bibles as criteria sources, so
    Em runs as she ships. Read the live manifest.yaml's critics block."""
    root = HERE.parents[1]  # repo root
    full = yaml.safe_load((root / "manifest.yaml").read_text(encoding="utf-8"))
    return {
        "critics": full.get("critics", {}),
        "criteria_sources": full.get("criteria_sources", {}),
        "characters_root": str(root / "characters"),
    }


def _force_stub_runners() -> None:
    """Force the credential-free path even when agy/SDK are present.

    The runners self-stub only when their backend is absent; on a machine with
    `agy` + the SDK installed, --stub would otherwise fire live (and costed)
    calls. This mirrors Mo's --no-sonnet opt-OUT: --stub must genuinely avoid
    the model. We patch the two runner references Em imports, returning a
    deterministic borderline verdict (cited, so the cites_criteria invariant is
    satisfied) — the resulting matrix is degenerate and labelled STUB.
    """
    from pipeline.agents import vision_critic as _vc

    stub_text = json.dumps({
        "verdict": "borderline",
        "confidence": 0.78,
        "reasoning": "STUB (--stub forced credential-free path; no scored claim).",
        "proposed_patches": [],
        "cites_criteria": ["AC01"],
    })

    async def _stub(*, prompt, image_paths, timeout_s=120):
        return types.SimpleNamespace(text=stub_text)

    _vc.run_antigravity_with_image = _stub
    _vc.run_gemini_api_with_image = _stub
    _vc.invoke_opus_vision = _stub


def _ctx(case: dict, manifest: dict, criteria) -> AgentContext:
    return AgentContext(
        run_dir=Path("/tmp/em-baseline"),
        inputs={
            "image_path": str(FIXTURES / case["input"]),
            "beat_description": case["beat_description"],
            "frame_id": case["name"],
            "impact_tags": case.get("impact_tags", []),
            "checkpoint": case["checkpoint"],
            "character_id": case.get("character_id", "sean"),
        },
        manifest=manifest,
        criteria=criteria,
        tier="draft",
        cache_dir=Path("/tmp/em-baseline/.cache"),
    )


def _score_one(case: dict, manifest: dict, criteria) -> CaseScore:
    """Run production Em (Gemini default + Opus escalation) against one case."""
    start = datetime.now(timezone.utc)
    result = VisionCriticNode().run(_ctx(case, manifest, criteria))
    wall = (datetime.now(timezone.utc) - start).total_seconds()
    refs = select_references(
        case.get("character_id", "sean"), case["checkpoint"], case["beat_description"],
        characters_root=Path(manifest["characters_root"]),
    )
    return CaseScore(
        name=case["name"],
        case_class=case["case_class"],
        expected_verdict=case["expected_verdict"],
        predicted_verdict=result.outputs["verdict"],
        expected_cites=case.get("expected_cites", []),
        actual_cites=result.cites_criteria,
        confidence=result.outputs["confidence"],
        wall_s=wall,
        # `refs` (resolved reference plate names) is logged per-case for trace
        # transparency — see the print() in main()'s loop below.
    )


def render_last_run_md(report: dict, *, model_label: str, n_total: int) -> str:
    """Render the segmented confusion matrix as studio-manual markdown."""
    def block(title: str, b: dict) -> str:
        cm = b["cm"]
        lines = [
            f"### {title}  (n={b['n']})",
            "",
            f"- confusion: TP={cm['tp']} FP={cm['fp']} FN={cm['fn']} TN={cm['tn']}",
            f"- **precision={b['precision']:.2f}  recall={b['recall']:.2f}**  "
            f"(recall ±{b['recall_stderr']:.2f})",
            f"- **false_pass_rate={b['false_pass_rate']:.2f}**  "
            f"(false passes: {', '.join(b['false_passes']) or 'none'})",
            f"- 3-way exact agreement={b['exact_agreement']:.2f}",
            f"- borderline->fail slippages: {', '.join(b['borderline_slippages']) or 'none'}",
            f"- cites-correct: "
            f"{b['cites_correct']:.2f}" if b['cites_correct'] is not None else
            f"- cites-correct: n/a",
            f"- mean wall: {b['mean_wall_s']:.1f}s",
            "",
        ]
        return "\n".join(lines)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    head = [
        f"# Em — scored baseline ({ts})",
        "",
        f"Model: **{model_label}**  ·  cases: {n_total}",
        "",
        "Metric contract: precision/recall on the defect class; **false-pass "
        "rate front and center** (the costly error). Raw agreement is NOT the "
        "headline (class imbalance); F1 is secondary. Segmented per Sean's call: "
        "identity/style+clean ('performs') reported apart from motion-proper "
        "(expected-red — the contact sheet structurally can't see motion).",
        "",
    ]
    body = [
        block("Performs (identity/style + clean)", report["performs"]),
        block("Motion-proper (expected red)", report["motion_proper"]),
        block("Overall", report["overall"]),
    ]
    return "\n".join(head + body)


# ---------------------------------------------------------------------------
# Subprocess-per-case isolation (Sean's call, 2026-06-01). The live run spawns
# one short-lived Python process per case so each case's asyncio + subprocess
# lifecycle (agy + Opus-SDK children) is fully isolated. Observed failure: a
# slow agy/Opus child's ThreadedChildWatcher thread races the closing event
# loop at INTERPRETER SHUTDOWN ("Loop ... is closed", exit 144, no traceback) —
# AFTER the verdict is computed. Because the worker flushes its CaseScore JSON
# to stdout BEFORE exit, the orchestrator captures the verdict regardless of a
# teardown crash or non-zero exit; only a case that dies BEFORE emitting JSON
# becomes an honest errored gap. The process-boundary version of score.py's
# existing per-case resilience; de-risks Task 8 (the bake-off) too.
# ---------------------------------------------------------------------------
_CASESCORE_SENTINEL = "CASESCORE_JSON:"
_PER_CASE_TIMEOUT_S = 600  # ~3x the observed 199s escalating-case latency


def _select_cases(segment: str, motion_smoke: int) -> tuple[list[dict], list[dict]]:
    """Return (selected, excluded). segment='all' runs every case; 'performs' runs
    the 23 clean+identity_style cases plus the first `motion_smoke` motion cases.
    The headline metrics (precision / false-pass / cites-correct) all live in the
    performs segment; a still-image contact sheet structurally can't score
    motion-proper (eval-strategy §3.5), so the remaining motion cases are excluded
    and LOGGED — honest segmentation, never silent truncation. One motion case is
    kept live to smoke-test reference-attach on the phase-6 contact-sheet path
    (spec §5.1)."""
    performs = [c for c in CASES if c["case_class"] in ("clean", "identity_style")]
    motion = [c for c in CASES if c["case_class"] == "motion_proper"]
    if segment == "all":
        return list(CASES), []
    return performs + motion[:motion_smoke], motion[motion_smoke:]


def _run_case_subprocess(case: dict, stub: bool) -> CaseScore:
    """Run ONE case in a fresh Python process and parse its emitted CaseScore.

    The worker re-loads manifest + criteria + the worktree .env (GEMINI/FAL only,
    no ANTHROPIC — the SDK keeps Claude Code auth), so parity with a direct run
    holds. We look for the CaseScore sentinel in stdout FIRST and only raise if it
    is absent — a worker that computed its verdict then crashed at teardown still
    flushed the JSON, so its verdict is captured; a worker that died before
    emitting one becomes an honest errored gap."""
    cmd = [sys.executable, "-m", "evals.vision_critic.score", "--only", case["name"]]
    if stub:
        cmd.append("--stub")
    proc = subprocess.run(
        cmd, capture_output=True, text=True, timeout=_PER_CASE_TIMEOUT_S,
        cwd=str(HERE.parents[1]),  # repo root: find_dotenv + relative bible paths resolve
        # Do NOT pass start_new_session here. Detaching the WORKER into a new session
        # breaks Claude Code auth for the Opus-SDK `claude` child (verified 2026-06-02:
        # detached workers returned unparseable output → borderline + empty cites →
        # Em's cites_criteria invariant raised → every case errored). The worker must
        # keep the normal session so the model CLIs authenticate. Isolation against the
        # exit-144 teardown signal is handled by detaching the ORCHESTRATOR at launch
        # (its own session), which the smoke confirmed survives multiple teardowns —
        # NOT by detaching the workers.
    )
    for line in proc.stdout.splitlines():
        if line.startswith(_CASESCORE_SENTINEL):
            return CaseScore(**json.loads(line[len(_CASESCORE_SENTINEL):]))
    raise RuntimeError(
        f"worker emitted no CaseScore (exit={proc.returncode}); "
        f"stderr tail: {proc.stderr.strip()[-300:] or '(empty)'}"
    )


def main() -> None:
    ap = argparse.ArgumentParser(prog="em-score")
    ap.add_argument("--stub", action="store_true",
                    help="Force credential-free runners (no scored claim).")
    ap.add_argument("--model", choices=["production"], default="production",
                    help="production = Gemini default + Opus escalation (as shipped).")
    ap.add_argument("--only", metavar="CASE_NAME",
                    help="Run exactly ONE case in THIS process and emit its CaseScore "
                         "as JSON (the per-case isolation worker; also usable manually).")
    ap.add_argument("--segment", choices=["all", "performs"], default="all",
                    help="all = every case; performs = the 23 clean+identity_style "
                         "cases (+ --motion-smoke motion cases).")
    ap.add_argument("--motion-smoke", type=int, default=0,
                    help="With --segment performs, include the first N motion_proper "
                         "cases (a phase-6 reference-attach smoke check). The rest are "
                         "excluded and logged.")
    ap.add_argument("--limit", type=int, default=0,
                    help="Run only the first N selected cases (0 = all). For a cheap "
                         "live smoke-validation of the harness (does the orchestrator "
                         "survive multiple worker teardowns?) before a full costed run. "
                         "A --limit run is partial — its last-run.md is not a baseline.")
    ap.add_argument("--allow-api-key", action="store_true",
                    help="Escape hatch: permit a live run while ANTHROPIC_API_KEY is set "
                         "in the environment. NOT recommended — Em's SDK escalation bills "
                         "the Anthropic API instead of your Claude subscription when the "
                         "key is present (Claude Code uses it in non-interactive mode). "
                         "Leave unset so a leaked key fails fast. Ignored with --stub.")
    args = ap.parse_args()

    # Env-hygiene guard (operational incident #1, 2026-06-02). A present
    # ANTHROPIC_API_KEY silently routes Em's Opus/Sonnet escalation to API
    # billing (precedence: in non-interactive mode the `claude` CLI always uses
    # the key when set, ahead of subscription OAuth). A costed run must never
    # start in that state by accident. --stub never touches a model, so it's
    # exempt; --allow-api-key is the explicit override.
    if os.environ.get("ANTHROPIC_API_KEY") and not args.stub and not args.allow_api_key:
        print(
            "REFUSING TO RUN: ANTHROPIC_API_KEY is set in the environment.\n"
            "A live Em run would bill the Anthropic API, not your Claude subscription.\n"
            "Fix: `unset ANTHROPIC_API_KEY` (and remove it from your shell rc), confirm\n"
            "subscription auth with `claude /status`, then re-run. For headless\n"
            "subscription billing use `claude setup-token` → CLAUDE_CODE_OAUTH_TOKEN.\n"
            "Override (not recommended): --allow-api-key.  See\n"
            "docs/anima-test-runs/2026-06-02-operational-incidents-remediation-plan.md",
            file=sys.stderr,
        )
        raise SystemExit(3)

    manifest = _manifest()

    # ---- worker mode: run one case in this process, emit JSON, exit ----
    if args.only:
        criteria = merged_criteria(manifest)
        if args.stub:
            _force_stub_runners()
        case = next((c for c in CASES if c["name"] == args.only), None)
        if case is None:
            print(f"unknown case: {args.only}", file=sys.stderr)
            raise SystemExit(2)
        cs = _score_one(case, manifest, criteria)
        refs = select_references(case.get("character_id", "sean"), case["checkpoint"],
                                 case["beat_description"], characters_root=Path(manifest["characters_root"]))
        print(f"{args.only}: {cs.predicted_verdict} (conf={cs.confidence:.2f}, "
              f"{cs.wall_s:.0f}s) refs=[{', '.join(p.name for p in refs) or 'none'}]",
              file=sys.stderr, flush=True)
        # Flush the verdict BEFORE returning, so a teardown crash can't lose it.
        print(_CASESCORE_SENTINEL + json.dumps(asdict(cs)), flush=True)
        return

    # ---- orchestrator mode: select cases, run each in an isolated subprocess ----
    selected, excluded = _select_cases(args.segment, args.motion_smoke)
    if args.limit:
        selected = selected[:args.limit]  # cheap smoke-validation; partial, not a baseline
    transport = manifest.get("critics", {}).get("t2", {}).get("transport", "agy")
    model_label = ("STUB (no scored claim)" if args.stub
                   else f"production: gemini-3.1-pro@{transport} + opus-4.7-escalation")

    scores: list[CaseScore] = []
    errored: list[tuple[str, str]] = []
    for i, c in enumerate(selected, 1):
        try:
            cs = _run_case_subprocess(c, args.stub)
            scores.append(cs)
            refs = select_references(c.get("character_id", "sean"), c["checkpoint"],
                                     c["beat_description"], characters_root=Path(manifest["characters_root"]))
            print(f"[{i}/{len(selected)}] {c['name']}: {cs.predicted_verdict} "
                  f"(conf={cs.confidence:.2f}, {cs.wall_s:.0f}s) "
                  f"refs=[{', '.join(p.name for p in refs) or 'none'}]", flush=True)
        except subprocess.TimeoutExpired:
            errored.append((c["name"], f"timeout after {_PER_CASE_TIMEOUT_S}s"))
            print(f"[{i}/{len(selected)}] {c['name']}: ERRORED — timeout", flush=True)
        except Exception as exc:  # noqa: BLE001 — record, don't abort
            errored.append((c["name"], f"{type(exc).__name__}: {exc}"))
            print(f"[{i}/{len(selected)}] {c['name']}: ERRORED — {type(exc).__name__}: {exc}",
                  flush=True)

    report = segment_report(scores)
    md = render_last_run_md(report, model_label=model_label, n_total=len(scores))
    # Honest segmentation: record cases intentionally NOT live-scored (never silent).
    if excluded:
        lines = ["", "## Intentionally NOT live-scored (segment scoping)", ""]
        lines += [f"- `{c['name']}` ({c['case_class']})" for c in excluded]
        lines += ["",
                  f"_{len(excluded)} motion_proper case(s) excluded from this live run. A "
                  "still-image contact sheet structurally cannot score motion-proper "
                  "(eval-strategy §3.5); these are the deferred E_warp/VBench validation "
                  "set, not a live-Em measurement. One motion case WAS run live as a "
                  "phase-6 reference-attach smoke check. This is scoping, not truncation._", ""]
        md = md + "\n" + "\n".join(lines)
    if errored:
        lines = ["", "## Errored cases (excluded from the matrix — NOT scored)", ""]
        lines += [f"- `{name}` — {err}" for name, err in errored]
        lines += ["",
                  f"_{len(errored)} of {len(selected)} selected cases errored. With "
                  "subprocess-per-case isolation, a crash/hang/quota-out (or Em's "
                  "empty-cites invariant) in one case lands here as an honest gap rather "
                  "than aborting the run. Not passes._", ""]
        md = md + "\n" + "\n".join(lines)

    (HERE / "last-run.md").write_text(md, encoding="utf-8")
    trace = HERE / "traces" / f"baseline-{datetime.now(timezone.utc):%Y-%m-%d}-scored.md"
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_text(md, encoding="utf-8")
    print(md)
    print(f"\nWrote {HERE/'last-run.md'} and {trace}")
    if errored:
        print(f"\n⚠ {len(errored)}/{len(selected)} cases errored (see report).")


if __name__ == "__main__":
    main()
