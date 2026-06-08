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
import math
import os
import subprocess
import sys
import types
from collections import Counter
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

from pipeline.agents import AgentContext
from pipeline.agents.vision_critic import VisionCriticNode, EmptyCitesInvariant
from pipeline.agents.reference_selection import select_references
from pipeline.contact_sheet import build_contact_sheet  # noqa: F401 (cases pre-build sheets)
from evals.vision_critic.scoring import CaseScore, segment_report
from evals.vision_critic.conftest import merged_criteria

HERE = Path(__file__).parent
FIXTURES = HERE / "fixtures"
CASES = yaml.safe_load((HERE / "cases.yaml").read_text(encoding="utf-8"))["cases"]


# --------------------------------------------------------------------------- #
# Replication (A5, 2026-06-02). --runs N replicates each case; the per-case
# MAJORITY verdict is the point estimate, and a per-segment false_pass BAND plus
# a persisted per-run verdict table surface the run-to-run variance the single
# point estimate hides (the Opus-variance the re-baseline diagnosed). Pure +
# testable (tests/test_score_replication.py); no model calls.
# --------------------------------------------------------------------------- #

_VERDICT_CONSERVATISM = {"fail": 0, "borderline": 1, "pass": 2}


def majority_verdict(verdicts: list[str]) -> str:
    """Most common verdict across N runs. Deterministic tie-break: the MORE
    conservative verdict wins (fail > borderline > pass) — a tie must never
    launder a flagged defect into a pass. Empty -> 'borderline' (defensive)."""
    if not verdicts:
        return "borderline"
    counts = Counter(verdicts)
    top = max(counts.values())
    tied = [v for v, c in counts.items() if c == top]
    if len(tied) == 1:
        return tied[0]
    return min(tied, key=lambda v: _VERDICT_CONSERVATISM.get(v, 1))


def consensus_scores(runs: list[list[CaseScore]]) -> list[CaseScore]:
    """Collapse N passes into one consensus CaseScore per case: majority verdict
    for the point estimate, mean confidence/wall, and cites taken from a run whose
    verdict matched the majority (so the cites align with the chosen verdict).
    Cases keep first-seen order."""
    by_name: dict[str, list[CaseScore]] = {}
    order: list[str] = []
    for pass_scores in runs:
        for s in pass_scores:
            if s.name not in by_name:
                by_name[s.name] = []
                order.append(s.name)
            by_name[s.name].append(s)
    out: list[CaseScore] = []
    for name in order:
        group = by_name[name]
        maj = majority_verdict([s.predicted_verdict for s in group])
        rep = next((s for s in group if s.predicted_verdict == maj), group[0])
        out.append(CaseScore(
            name=name,
            case_class=rep.case_class,
            expected_verdict=rep.expected_verdict,
            predicted_verdict=maj,
            expected_cites=rep.expected_cites,
            actual_cites=rep.actual_cites,
            confidence=sum(s.confidence for s in group) / len(group),
            wall_s=sum(s.wall_s for s in group) / len(group),
            reasoning=rep.reasoning,  # prose from the run whose verdict won (aligns with cites)
        ))
    return out


def false_pass_band(runs: list[list[CaseScore]]) -> dict:
    """Per segment, the false_pass_rate across the N passes: min/max/mean + the
    stderr of the mean. Surfaces the variance the point estimate hides — the
    headline safety number is exactly the one that flips run-to-run."""
    segments = ("performs", "motion_proper", "overall")
    band: dict[str, dict] = {}
    for seg in segments:
        vals = [segment_report(p)[seg]["false_pass_rate"] for p in runs]
        n = len(vals)
        mean = sum(vals) / n if n else 0.0
        if n > 1:
            var = sum((v - mean) ** 2 for v in vals) / (n - 1)
            se = math.sqrt(var) / math.sqrt(n)
        else:
            se = 0.0
        band[seg] = {
            "per_run": vals,
            "min": min(vals) if vals else 0.0,
            "max": max(vals) if vals else 0.0,
            "mean": mean,
            "stderr": se,
        }
    return band


def render_per_run_table(runs: list[list[CaseScore]]) -> str:
    """A markdown table: one row per case, one column per run, cell = verdict.
    A case whose verdicts disagree across runs is marked FLIP — the whole point
    of replication is that these never get averaged away silently."""
    by_name: dict[str, dict[int, str]] = {}
    order: list[str] = []
    for i, pass_scores in enumerate(runs):
        for s in pass_scores:
            if s.name not in by_name:
                by_name[s.name] = {}
                order.append(s.name)
            by_name[s.name][i] = s.predicted_verdict
    n = len(runs)
    header = "| case | " + " | ".join(f"run{i+1}" for i in range(n)) + " | flip? |"
    sep = "|" + "---|" * (n + 2)
    rows = [header, sep]
    for name in order:
        cells = [by_name[name].get(i, "—") for i in range(n)]
        present = [c for c in cells if c != "—"]
        flip = "**FLIP**" if len(set(present)) > 1 else ""
        rows.append(f"| `{name}` | " + " | ".join(cells) + f" | {flip} |")
    return "\n".join(rows)


def render_per_case_detail(scores: list[CaseScore]) -> str:
    """G6.2 diagnostic: per-case expected/actual cites + cites_correct + reasoning.

    Pure; no model calls. The verdict-by-verdict table lets the cite-classification
    work (Q1 style / Q3 geometry) read by case, and the reasoning is rendered in
    its OWN block per case (never inside a table cell — long prose with pipes or
    newlines would otherwise shred the markdown table). `cites_correct` reuses the
    scorer the headline metric uses, so the table and the matrix can never disagree.
    """
    lines = ["", "## Per-case cite + reasoning detail (G6.2 diagnostic)", "",
             "| case | class | expected | predicted | expected_cites | actual_cites | cites_correct | conf |",
             "|---|---|---|---|---|---|---|---|"]
    for s in scores:
        # G6.1 tiered citation credit (None=n/a, 1.0=yes/full, 0.5=~partial, 0.0=NO).
        cc = s.citation_credit
        if cc is None:
            cc_str = "n/a"
        elif cc == 1.0:
            cc_str = "yes"
        elif cc > 0.0:
            cc_str = "~part"
        else:
            cc_str = "**NO**"
        exp = ", ".join(s.expected_cites) or "—"
        act = ", ".join(s.actual_cites) or "—"
        lines.append(f"| `{s.name}` | {s.case_class} | {s.expected_verdict} | "
                     f"{s.predicted_verdict} | {exp} | {act} | {cc_str} | {s.confidence:.2f} |")
    lines += ["", "### Reasoning (per case)", ""]
    for s in scores:
        prose = " ".join(s.reasoning.split()).strip() or "(no reasoning captured)"
        lines.append(f"- **`{s.name}`** ({s.predicted_verdict}, conf {s.confidence:.2f}): {prose}")
    lines.append("")
    return "\n".join(lines)


def render_replication_md(runs: list[list[CaseScore]]) -> str:
    """The replication section appended to last-run.md when --runs > 1."""
    n = len(runs)
    band = false_pass_band(runs)
    def line(seg: str) -> str:
        b = band[seg]
        return (f"- **{seg}**: false_pass mean={b['mean']:.2f} "
                f"(band {b['min']:.2f}–{b['max']:.2f}, ±{b['stderr']:.2f} stderr); "
                f"per-run {[round(v, 2) for v in b['per_run']]}")
    lines = [
        "", f"## Replication ({n} runs)", "",
        "Point estimate above uses the per-case MAJORITY verdict across the "
        f"{n} runs. The false_pass BAND below is the run-to-run spread the single "
        "estimate hides:", "",
        line("performs"), line("motion_proper"), line("overall"), "",
        "### Per-run verdicts (flips are not averaged away)", "",
        render_per_run_table(runs), "",
    ]
    return "\n".join(lines)


def _refs_label(case: dict, manifest: dict, attach_refs: bool,
                attach_criteria_text: bool = False) -> str:
    """Trace label for the attachment state (A1/G6.1b honesty) — three states, the
    trace must never claim more than Em actually saw:
      - attach_refs ON           -> the actual reference-plate filenames (images + criteria)
      - refs OFF, criteria-text ON -> 'criteria-text (images off)'
      - both OFF                  -> 'blind (attach_references off)' (production default)
    Criteria-text mode must NEVER print 'blind' — that was the prior run's invisible
    miss (the criteria block was inert and the trace still read blind)."""
    if attach_refs:
        refs = select_references(case.get("character_id", "sean"), case["checkpoint"],
                                 case["beat_description"], characters_root=Path(manifest["characters_root"]))
        return ", ".join(p.name for p in refs) or "none"
    if attach_criteria_text:
        return "criteria-text (images off)"
    return "blind (attach_references off)"


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
        reasoning=result.outputs.get("reasoning", ""),  # G6.2: persist Em's prose
        # `refs` (resolved reference plate names) is logged per-case for trace
        # transparency — see the print() in main()'s loop below.
    )


def _cites_line(b: dict) -> str:
    """The citation axis (G6.1), reported apart from the verdict axis above:
    the graded cites-correct mean plus the full / partial / none breakdown so a
    right-verdict-wrong-cite case is legible. `cites_correct` is graded (full=1.0,
    partial=0.5); n is the flagged-case denominator (pass verdicts are N/A)."""
    if b.get("cites_correct") is None:
        return "- cites-correct (citation axis): n/a (no flagged cases)"
    return (
        f"- **cites-correct (citation axis)={b['cites_correct']:.2f}** "
        f"over n={b['cites_scored_n']} flagged "
        f"(full={b['cites_full']} · partial={b['cites_partial']} · none={b['cites_none']})"
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
            _cites_line(b),
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


def _run_case_subprocess(case: dict, stub: bool, attach_references: bool = False,
                         attach_criteria_text: bool = False) -> CaseScore:
    """Run ONE case in a fresh Python process and parse its emitted CaseScore.

    The worker re-loads manifest + criteria + the worktree .env (GEMINI/FAL only,
    no ANTHROPIC — the SDK keeps Claude Code auth), so parity with a direct run
    holds. The worker re-reads manifest.yaml from disk, so --attach-references must
    ride the command line for the worker to actually attach the bundle — otherwise
    the orchestrator's refs= label would claim references the blind worker never
    saw. We look for the CaseScore sentinel in stdout FIRST and only raise if it
    is absent — a worker that computed its verdict then crashed at teardown still
    flushed the JSON, so its verdict is captured; a worker that died before
    emitting one becomes an honest errored gap."""
    cmd = [sys.executable, "-m", "evals.vision_critic.score", "--only", case["name"]]
    if stub:
        cmd.append("--stub")
    if attach_references:
        cmd.append("--attach-references")
    if attach_criteria_text:
        cmd.append("--attach-criteria-text")
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
    ap.add_argument("--runs", type=int, default=1,
                    help="Replicate the whole selected set N times (A5). Default 1 (cheap "
                         "smoke). The real baseline runs --runs 5: the point estimate uses "
                         "the per-case MAJORITY verdict, and last-run.md reports a per-segment "
                         "false_pass BAND (min/max ± stderr across runs) plus a per-run verdict "
                         "table so a flip is visible, not silently averaged away.")
    ap.add_argument("--allow-api-key", action="store_true",
                    help="Escape hatch: permit a live run while ANTHROPIC_API_KEY is set "
                         "in the environment. NOT recommended — Em's SDK escalation bills "
                         "the Anthropic API instead of your Claude subscription when the "
                         "key is present (Claude Code uses it in non-interactive mode). "
                         "Leave unset so a leaked key fails fast. Ignored with --stub.")
    ap.add_argument("--trace-name", metavar="LABEL", default=None,
                    help="Override the dated trace filename stem. When set, write ONLY "
                         "traces/{LABEL}.md and DO NOT touch last-run.md or the default "
                         "baseline-{date}-scored.md. Use for a diagnostic run that must "
                         "not clobber or move the ratified baseline trace.")
    ap.add_argument("--attach-references", action="store_true",
                    help="Run-scoped override: attach the Bible reference bundle "
                         "(critics.t2.attach_references=true) for THIS run only, WITHOUT "
                         "editing manifest.yaml. Wins over the manifest read and is "
                         "propagated to every per-case worker, so the orchestrator's refs= "
                         "trace label can never claim references a blind worker didn't "
                         "actually attach. Default off = reference-blind (the production "
                         "default). For the diagnostic references re-test only.")
    ap.add_argument("--attach-criteria-text", action="store_true",
                    help="Run-scoped override: attach the IR/AC criteria block (the text "
                         "handles Em cites) WITHOUT reference images, for THIS run only "
                         "(critics.t2.attach_criteria_text=true). Independent of "
                         "--attach-references — decoupled in G6.1b after the 2026-06-07 "
                         "re-baseline proved the criteria block was inert reference-blind. "
                         "Propagated to every per-case worker so the trace can't claim a "
                         "criteria block a blind worker never saw. Repo default stays off.")
    ap.add_argument("--dump-prompt", action="store_true",
                    help="With --only: build the prompt for that one case (exactly as "
                         "run() would, honoring --attach-criteria-text / --attach-references), "
                         "print it to stdout, and EXIT before any model call. $0 pre-flight "
                         "gate — proves the criteria block reaches Em without spending.")
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
    # Run-scoped references override (--attach-references). Mutating the in-memory
    # manifest here — before the attach_refs read below and before the worker/
    # orchestrator split — is the SINGLE enable point: it flows to the worker's
    # VisionCriticNode (the actual attach, via _ctx(manifest)) AND to _refs_label
    # (the honest trace label). The repo manifest.yaml is never touched; the repo
    # default stays attach_references: false. The worker is a fresh process that
    # re-reads manifest.yaml, so the flag is also forwarded on its command line
    # (_run_case_subprocess) — never enabled by a committed manifest change.
    if args.attach_references:
        manifest.setdefault("critics", {}).setdefault("t2", {})["attach_references"] = True
    # Run-scoped criteria-text override (--attach-criteria-text, G6.1b). Same single
    # enable point as --attach-references and equally forwarded to the worker cmd —
    # but it attaches ONLY the criteria block (text handles), zero reference images.
    if args.attach_criteria_text:
        manifest.setdefault("critics", {}).setdefault("t2", {})["attach_criteria_text"] = True
    # Trace-honesty (A1/G6.1b): only claim in the log what Em actually attaches.
    # attach_references defaults off (reference-blind is production); attach_criteria_text
    # defaults off. The trace must not list refs/criteria Em never saw.
    attach_refs = bool(manifest.get("critics", {}).get("t2", {}).get("attach_references", False))
    attach_criteria_text = bool(manifest.get("critics", {}).get("t2", {}).get("attach_criteria_text", False))

    # ---- worker mode: run one case in this process, emit JSON, exit ----
    if args.only:
        criteria = merged_criteria(manifest)
        if args.stub:
            _force_stub_runners()
        case = next((c for c in CASES if c["name"] == args.only), None)
        if case is None:
            print(f"unknown case: {args.only}", file=sys.stderr)
            raise SystemExit(2)
        if args.dump_prompt:
            # $0 pre-flight gate (G6.1b §0): build the prompt EXACTLY as run() would
            # (mirrors run() lines 129-131 — references gate on attach_references
            # alone) and exit before any model call. In criteria-text mode the
            # reference images stay off, so n_references == 0 and no "Reference
            # plates" section appears — the decoupling guarantee, observable in the dump.
            node = VisionCriticNode()
            ctx = _ctx(case, manifest, criteria)
            t2_cfg = node._t2_config(ctx)
            refs = node._resolve_references(ctx) if node._attach_references(t2_cfg) else []
            print(node._build_prompt(ctx, t2_cfg, n_references=len(refs)))
            return
        try:
            cs = _score_one(case, manifest, criteria)
        except EmptyCitesInvariant as inv:
            # DIAGNOSTIC capture only (G6.2). In production this still raised upstream
            # — the critic spine rejects the ungrounded block. Here we record what Em
            # saw so the geometry empty-cites cases (proportion/view/anatomy) contribute
            # their reasoning instead of dying as a blind errored gap. confidence=0.0 is
            # a SENTINEL (not parsed at trip time) — exclude it from confidence means.
            cs = CaseScore(
                name=case["name"],
                case_class=case["case_class"],
                expected_verdict=case["expected_verdict"],
                predicted_verdict=inv.verdict,
                expected_cites=case.get("expected_cites", []),
                actual_cites=list(inv.cites),  # empty by definition — recorded explicitly
                confidence=0.0,
                wall_s=0.0,
                reasoning=f"[INVARIANT_TRIPPED empty-cites] {inv.reasoning}",
            )
        print(f"{args.only}: {cs.predicted_verdict} (conf={cs.confidence:.2f}, "
              f"{cs.wall_s:.0f}s) refs=[{_refs_label(case, manifest, attach_refs, attach_criteria_text)}]",
              file=sys.stderr, flush=True)
        # Flush the verdict BEFORE returning, so a teardown crash can't lose it.
        print(_CASESCORE_SENTINEL + json.dumps(asdict(cs)), flush=True)
        return

    # ---- orchestrator mode: select cases, run each in an isolated subprocess ----
    selected, excluded = _select_cases(args.segment, args.motion_smoke)
    if args.limit:
        selected = selected[:args.limit]  # cheap smoke-validation; partial, not a baseline
    transport = manifest.get("critics", {}).get("t2", {}).get("transport", "agy")
    # Honest label: agy never ran 3.1 Pro — its backend default was gemini-3.5-flash
    # (Task 4 log forensics, 2026-06-02). The gemini_api transport pins that same
    # model (gemini_api_runner.GEMINI_VISION_MODEL), holding it constant vs the 0.62.
    from pipeline.agents.gemini_api_runner import GEMINI_VISION_MODEL
    gemini_model = GEMINI_VISION_MODEL if transport == "gemini_api" else "gemini-3.5-flash"
    # Attach-mode label rides into the trace header (G6.1b trace honesty) — the
    # persistent .md must record which lever was on, never read "blind" when
    # criteria-text was attached.
    attach_mode = ("references (images+criteria)" if attach_refs
                   else "criteria-text (images off)" if attach_criteria_text
                   else "reference-blind")
    model_label = ("STUB (no scored claim)" if args.stub
                   else f"production: {gemini_model}@{transport} + opus-4.7-escalation [{attach_mode}]")

    n_runs = max(1, args.runs)
    runs: list[list[CaseScore]] = []
    errored: list[tuple[str, str]] = []
    for run_idx in range(n_runs):
        pass_scores: list[CaseScore] = []
        run_tag = f"run {run_idx + 1}/{n_runs} | " if n_runs > 1 else ""
        for i, c in enumerate(selected, 1):
            try:
                cs = _run_case_subprocess(c, args.stub, args.attach_references,
                                          args.attach_criteria_text)
                pass_scores.append(cs)
                print(f"[{run_tag}{i}/{len(selected)}] {c['name']}: {cs.predicted_verdict} "
                      f"(conf={cs.confidence:.2f}, {cs.wall_s:.0f}s) "
                      f"refs=[{_refs_label(c, manifest, attach_refs, attach_criteria_text)}]", flush=True)
            except subprocess.TimeoutExpired:
                errored.append((c["name"], f"{run_tag}timeout after {_PER_CASE_TIMEOUT_S}s"))
                print(f"[{run_tag}{i}/{len(selected)}] {c['name']}: ERRORED — timeout", flush=True)
            except Exception as exc:  # noqa: BLE001 — record, don't abort
                errored.append((c["name"], f"{run_tag}{type(exc).__name__}: {exc}"))
                print(f"[{run_tag}{i}/{len(selected)}] {c['name']}: ERRORED — "
                      f"{type(exc).__name__}: {exc}", flush=True)
        runs.append(pass_scores)

    # Point estimate = per-case MAJORITY verdict across the runs (A5). For n_runs=1
    # this is identical to the single pass, so the cheap smoke is unchanged.
    consensus = consensus_scores(runs)
    report = segment_report(consensus)
    md = render_last_run_md(report, model_label=model_label, n_total=len(consensus))
    if n_runs > 1:
        md = md + "\n" + render_replication_md(runs)
    # G6.2: per-case cites + reasoning. Pure render over `consensus`; additive (no
    # metric/verdict/model effect), so it is always on — every future trace carries it.
    md = md + "\n" + render_per_case_detail(consensus)
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
                  f"_{len(errored)} of {len(selected) * n_runs} case-runs errored "
                  f"({len(selected)} cases × {n_runs} run(s)). With subprocess-per-case "
                  "isolation, a crash/hang/quota-out (or Em's empty-cites invariant) in "
                  "one case-run lands here as an honest gap rather than aborting the run. "
                  "Not passes._", ""]
        md = md + "\n" + "\n".join(lines)

    if args.trace_name:
        # Diagnostic run: write ONLY the labelled trace; leave last-run.md and the
        # default dated baseline trace byte-identical (so a same-day diagnostic can
        # never clobber the ratified baseline — G6.2 F1).
        trace = HERE / "traces" / f"{args.trace_name}.md"
        trace.parent.mkdir(parents=True, exist_ok=True)
        trace.write_text(md, encoding="utf-8")
        print(md)
        print(f"\nWrote {trace} (last-run.md + baseline trace untouched — --trace-name set)")
    else:
        (HERE / "last-run.md").write_text(md, encoding="utf-8")
        trace = HERE / "traces" / f"baseline-{datetime.now(timezone.utc):%Y-%m-%d}-scored.md"
        trace.parent.mkdir(parents=True, exist_ok=True)
        trace.write_text(md, encoding="utf-8")
        print(md)
        print(f"\nWrote {HERE/'last-run.md'} and {trace}")
    if errored:
        print(f"\n⚠ {len(errored)}/{len(selected) * n_runs} case-runs errored (see report).")


if __name__ == "__main__":
    main()
