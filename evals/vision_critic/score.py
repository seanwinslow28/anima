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
import types
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


def main() -> None:
    ap = argparse.ArgumentParser(prog="em-score")
    ap.add_argument("--stub", action="store_true",
                    help="Force credential-free runners (no scored claim).")
    ap.add_argument("--model", choices=["production"], default="production",
                    help="production = Gemini default + Opus escalation (as shipped).")
    args = ap.parse_args()

    manifest = _manifest()
    # Built once and reused by both the live and --stub branches, so the stub
    # still exercises the criteria-surfacing path end-to-end (parity).
    criteria = merged_criteria(manifest)
    if args.stub:
        # Mirror Mo's --no-sonnet: force the credential-free path so the matrix
        # is the stub's degenerate one. Label it so no one mistakes it for a
        # baseline.
        _force_stub_runners()
        model_label = "STUB (no scored claim)"
    else:
        model_label = "production: gemini-3.1-pro@agy + opus-4.7-escalation"

    # Per-case resilience: a scoring harness must not let ONE bad case abort a
    # ~24-min live run. Em's cites_criteria invariant legitimately raises a
    # ValueError when a model returns a blocking verdict with no citation (e.g.
    # a JSON parse-failure → defensive borderline + empty cites); a single such
    # case used to kill the whole baseline. We catch per case, record errors
    # HONESTLY (excluded from the matrix, listed explicitly — never fabricated
    # into a verdict), and print incremental progress so the failure point is
    # always visible.
    scores: list[CaseScore] = []
    errored: list[tuple[str, str]] = []
    for i, c in enumerate(CASES, 1):
        try:
            cs = _score_one(c, manifest, criteria)
            scores.append(cs)
            refs = select_references(c.get("character_id", "sean"), c["checkpoint"],
                                     c["beat_description"], characters_root=Path(manifest["characters_root"]))
            print(f"[{i}/{len(CASES)}] {c['name']}: {cs.predicted_verdict} "
                  f"(conf={cs.confidence:.2f}, {cs.wall_s:.0f}s) refs=[{', '.join(p.name for p in refs) or 'none'}]",
                  flush=True)
        except Exception as exc:  # noqa: BLE001 — record, don't abort
            errored.append((c["name"], f"{type(exc).__name__}: {exc}"))
            print(f"[{i}/{len(CASES)}] {c['name']}: ERRORED — {type(exc).__name__}: {exc}",
                  flush=True)

    report = segment_report(scores)
    md = render_last_run_md(report, model_label=model_label, n_total=len(scores))
    if errored:
        lines = ["", "## Errored cases (excluded from the matrix — NOT scored)", ""]
        lines += [f"- `{name}` — {err}" for name, err in errored]
        lines += ["",
                  f"_{len(errored)} of {len(CASES)} cases errored. A blocking "
                  "verdict with empty cites (Em's invariant) or a runner error "
                  "lands here rather than aborting the run. These are honest "
                  "gaps, not passes._", ""]
        md = md + "\n" + "\n".join(lines)

    (HERE / "last-run.md").write_text(md, encoding="utf-8")
    trace = HERE / "traces" / f"baseline-{datetime.now(timezone.utc):%Y-%m-%d}-scored.md"
    trace.parent.mkdir(parents=True, exist_ok=True)
    trace.write_text(md, encoding="utf-8")
    print(md)
    print(f"\nWrote {HERE/'last-run.md'} and {trace}")
    if errored:
        print(f"\n⚠ {len(errored)}/{len(CASES)} cases errored (see report).")


if __name__ == "__main__":
    main()
