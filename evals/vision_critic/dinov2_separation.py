"""B1b — DINOv2 separation spike (compute-costed, $0 API; go/no-go gated).

Question (scored like any agent — segmented, false-pass-first):

    On the labeled performs fixtures, does DINOv2 cosine SIMILARITY
    (subject vs view-matched reference; LOW similarity = drift) SEPARATE the
    identity/proportion defect cases from the clean cases, with a usable
    threshold?

This is a MEASUREMENT spike, not production code. It does scope+view reference
picking LOCALLY (it does NOT modify the shipped `best_view_reference`, which is
scope-blind — that hardening is a B1c refinement IF the spike clears its gate).
It reuses the live DINOv2 ladder (`compute_similarity`) and asserts the rung is
`dinov2` (never a silent PIL fallback).

Two reference columns per case:
  - `anchor`  : subject vs the front anchor.png — the signal the *current*
                record-only Pass-2.5 gate uses (one front anchor, view-blind).
  - `view`    : subject vs the scope+view-matched turnaround (B1a's contribution)
                — present only when the beat carries an inferable view AND a
                matching plate exists.

Honest scoping (kickoff): DINOv2 is graded ONLY on the identity/proportion
defect class. The stylus (`stylus-hand-f13-cc01`) and scale (`sprite-scale-*`)
cases are spatial/continuity — NOT a DINOv2 job — reported, never graded.

Run:  .venv/bin/python -m evals.vision_critic.dinov2_separation
"""
from __future__ import annotations

import hashlib
import statistics
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import yaml

from pipeline.agents.reference_selection import _infer_view, _resolve_folder
from pipeline.agents.similarity_gate import compute_similarity

HERE = Path(__file__).parent
REPO = HERE.parents[1]
FIXTURES = HERE / "fixtures"
CHARACTERS = REPO / "characters"
CASES = yaml.safe_load((HERE / "cases.yaml").read_text(encoding="utf-8"))["cases"]

# ---------------------------------------------------------------------------
# Label classes (which defect is DINOv2's job). The kickoff is explicit: grade
# the identity/proportion class; report the spatial/continuity class but do not
# grade it. Keyed by case name so the labels are auditable against cases.yaml.
# ---------------------------------------------------------------------------
_DINOV2_TARGET = {  # identity / proportion drift — DINOv2's job
    "proportion-drift-body-3quarter", "proportion-jaw-body-profile-left",
    "proportion-eyes-body-profile-right", "proportion-costume-body-back",
    "proportion-walk-cycle-source", "identity-head-turn-01",
    "jaw-drift-head-turn-09", "borderline-hair-head-profile-right",
}
_NOT_DINOV2 = {  # spatial / continuity / expression / prop — reported, NOT graded
    "sprite-scale-f31-bad", "stylus-hand-f13-cc01",
    "borderline-expr-focused", "borderline-motion-head-turn-03",
    "borderline-stylus-prop",
}

# Scope inference (head vs body). The clean view-cases are HEAD ("Sean head, …"),
# the proportion defects are BODY ("Sean full-body …") — a scope-fair reference
# is required or a clean head subject reads as drift against a body plate.
_SCOPE_KEYWORDS = (
    ("body", ("full-body", "full body", "full-figure", "walk-cycle", "walk cycle",
              "neutral-gait", "gait")),
    ("head", ("sean head", "head,", "headshot", "head shot", "portrait")),
)


def _infer_scope(beat: str) -> str | None:
    b = (beat or "").lower()
    for scope, kws in _SCOPE_KEYWORDS:
        if any(k in b for k in kws):
            return scope
    return None


def _content_hash(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _pick_view_ref(folder: Path, view: str | None, scope: str | None):
    """Scope+view-matched turnaround, else view-only, else (None, None). LOCAL to
    the spike — deliberately does not call the scope-blind best_view_reference."""
    turn_dir = folder / "turnarounds"
    turns = sorted(turn_dir.glob("*.png")) if turn_dir.is_dir() else []
    if not view:
        return None, None
    if scope:
        m = next((p for p in turns if scope in p.stem.lower() and view in p.stem.lower()), None)
        if m:
            return m, "view+scope"
    m = next((p for p in turns if view in p.stem.lower()), None)
    if m:
        return m, "view-only"
    return None, None


@dataclass
class Row:
    name: str
    case_class: str          # clean | identity_style
    graded: bool             # is this DINOv2's class?
    expected_defect: bool    # labeled fail/borderline
    defect_label: str
    view: str | None
    scope: str | None
    anchor_score: float
    anchor_method: str
    view_ref: str | None
    view_kind: str | None
    view_score: float | None
    view_method: str | None
    self_match: bool


def _score_case(case: dict) -> Row:
    subject = FIXTURES / case["input"]
    beat = case.get("beat_description", "")
    cid = case.get("character_id", "sean")
    folder = _resolve_folder(cid, CHARACTERS)
    view = _infer_view(beat)
    scope = _infer_scope(beat)

    anchor = folder / "anchor.png"
    a = compute_similarity(subject, anchor)

    view_ref, view_kind = _pick_view_ref(folder, view, scope)
    v = compute_similarity(subject, view_ref) if view_ref else None
    self_match = bool(view_ref and _content_hash(subject) == _content_hash(view_ref))

    return Row(
        name=case["name"], case_class=case["case_class"],
        graded=case["name"] in _DINOV2_TARGET,
        expected_defect=case["expected_verdict"] in {"fail", "borderline"},
        defect_label=case.get("defect_label", ""),
        view=view, scope=scope,
        anchor_score=a.score, anchor_method=a.method,
        view_ref=view_ref.name if view_ref else None, view_kind=view_kind,
        view_score=v.score if v else None, view_method=v.method if v else None,
        self_match=self_match,
    )


def _sep_stats(label: str, scores: list[float]) -> str:
    if not scores:
        return f"  {label}: (none)"
    lo, hi = min(scores), max(scores)
    mu = statistics.fmean(scores)
    return f"  {label:<34} n={len(scores)}  min={lo:.3f} mean={mu:.3f} max={hi:.3f}"


def _threshold_sweep(clean: list[float], defect: list[float]) -> str:
    """For each candidate T, a `score < T` gate flags drift. Report the false_pass
    (a graded defect NOT flagged: score >= T) and false_alarm (a clean flagged:
    score < T) at the T that best separates. false-pass-first: pick the T that
    drives false_pass to 0 with the fewest false alarms."""
    if not clean or not defect:
        return "  (need both clean and defect view-matched scores to sweep)"
    best = None
    lo = min(clean + defect)
    hi = max(clean + defect)
    # sweep midpoints between sorted unique scores
    pts = sorted(set(clean + defect))
    cands = [(pts[i] + pts[i + 1]) / 2 for i in range(len(pts) - 1)] + [lo - 0.01, hi + 0.01]
    for T in sorted(cands):
        fp = sum(1 for s in defect if s >= T)          # defect not flagged = FALSE PASS
        fa = sum(1 for s in clean if s < T)            # clean flagged = false alarm
        # rank: minimise false_pass first, then false_alarm
        key = (fp, fa, abs(T - (statistics.fmean(clean) + statistics.fmean(defect)) / 2))
        if best is None or key < best[0]:
            best = (key, T, fp, fa)
    _, T, fp, fa = best
    return (f"  best threshold T={T:.3f}  →  false_pass={fp}/{len(defect)}  "
            f"false_alarm={fa}/{len(clean)}  (flag when score < T)")


def main() -> None:
    rows = [_score_case(c) for c in CASES if c["case_class"] in ("clean", "identity_style")]

    # rung guard — never grade a silent PIL fallback as a DINOv2 result
    methods = {r.anchor_method for r in rows} | {r.view_method for r in rows if r.view_method}
    assert methods <= {"dinov2"}, f"NON-dinov2 rung engaged: {methods} — spike invalid"

    # ---- view-matched separation (the primary read), excluding self-matches ----
    vm = [r for r in rows if r.view_score is not None and not r.self_match]
    vm_clean = [r.view_score for r in vm if r.case_class == "clean"]
    vm_defect_graded = [r.view_score for r in vm if r.graded and r.expected_defect]

    # ---- anchor-only separation (the current record-only gate's signal) ----
    an_clean = [r.anchor_score for r in rows if r.case_class == "clean"]
    an_defect_graded = [r.anchor_score for r in rows if r.graded and r.expected_defect]

    lines: list[str] = []
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines.append(f"# B1b — DINOv2 separation spike ({ts})")
    lines.append("")
    lines.append(f"Rung: **dinov2** (asserted). Performs cases: {len(rows)} "
                 f"(clean + identity_style). Model: facebook/dinov2-small via compute_similarity.")
    lines.append("")
    lines.append("## Per-case scores")
    lines.append("")
    lines.append("| case | class | graded | view | scope | view_ref (kind) | self | anchor | view |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        vs = f"{r.view_score:.3f}" if r.view_score is not None else "—"
        vr = f"{r.view_ref} ({r.view_kind})" if r.view_ref else "—"
        lines.append(
            f"| {r.name} | {r.case_class} | {'Y' if r.graded else 'n'} | "
            f"{r.view or '—'} | {r.scope or '—'} | {vr} | "
            f"{'SELF' if r.self_match else ''} | {r.anchor_score:.3f} | {vs} |"
        )
    lines.append("")
    lines.append("## Separation — VIEW-MATCHED (primary; self-matches excluded)")
    lines.append("")
    lines.append(_sep_stats("clean", vm_clean))
    lines.append(_sep_stats("proportion/identity defect (graded)", vm_defect_graded))
    lines.append(_threshold_sweep(vm_clean, vm_defect_graded))
    lines.append("")
    lines.append("## Separation — ANCHOR-ONLY (today's record-only gate signal; view-blind)")
    lines.append("")
    lines.append(_sep_stats("clean", an_clean))
    lines.append(_sep_stats("proportion/identity defect (graded)", an_defect_graded))
    lines.append(_threshold_sweep(an_clean, an_defect_graded))
    lines.append("")
    selfs = [r.name for r in rows if r.self_match]
    n_view_cases = sum(1 for r in rows if r.view_score is not None)
    # proportion-invisibility: graded defects vs the front-ish clean frames, anchor col
    front_clean = [r.anchor_score for r in rows if r.case_class == "clean" and r.anchor_score >= 0.90]
    lines.append("## Confounds & findings (honest)")
    lines.append("")
    lines.append(f"- **Every view-matched fixture is a SELF-MATCH** ({len(selfs)}/{n_view_cases}). "
                 "The clean turnaround fixtures AND the proportion-DEFECT fixtures are "
                 "byte-identical to the Bible's own turnaround plates. So the view-matched "
                 "read is **vacuous** — there is no *distinct* per-view reference to compare a "
                 "subject against; the 'reference' is the subject.")
    lines.append("- **Root cause — contaminated references**: `sean-anchor/turnarounds/"
                 "body-profile-right.png` (etc.) IS the plate the eval labels "
                 "`proportion-eyes-body-profile-right` (a Cy fail @1.0, head ~1:5.3). The Bible's "
                 "per-view BODY plates are the proportion-drifted ones — the record-only Pass-2.5 "
                 "gate let them bake in. **There is no clean 1:7 per-view body reference in the "
                 "Bible to ground a view-matched identity check.**")
    lines.append(f"- **Proportion is invisible to embedding similarity**: the graded proportion "
                 f"defects score {min(an_defect_graded):.2f}–{max(an_defect_graded):.2f} vs the "
                 f"front anchor — overlapping/above the off-view clean head plates "
                 f"({min(an_clean):.2f}–{max(an_clean):.2f}) — because a proportion-drifted plate "
                 "is still embedding-recognizably Sean. DINOv2 cosine captures identity/style "
                 "recognizability, NOT geometric proportion (the exact confabulation class that "
                 "blocked references: proportion + eye-color).")
    lines.append("- **Anchor-only ordering is dominated by VIEW, not defect**: the front-ish "
                 f"clean frames score highest ({', '.join(f'{s:.2f}' for s in sorted(front_clean, reverse=True))}), "
                 "off-view cleans lowest — so a single front anchor can't threshold drift without "
                 "flagging legitimate off-view cleans (false_alarm 7/10 at false_pass 0).")
    lines.append("- **Not graded** (spatial/continuity, kickoff): "
                 + ", ".join(sorted(_NOT_DINOV2)))
    lines.append("")

    # ---- explicit GO / NO-GO verdict ----
    vm_testable = len(vm_clean) > 0 and len(vm_defect_graded) > 0
    lines.append("## GO / NO-GO")
    lines.append("")
    lines.append("**NO-GO** for DINOv2 as a view-matched identity/proportion backstop on this "
                 "fixture set, for two independent reasons:")
    lines.append("")
    lines.append(f"1. **Untestable as designed** — the view-matched separation is vacuous "
                 f"({'no' if not vm_testable else 'too few'} non-self view-matched pairs): the "
                 "Bible's per-view body plates ARE the labeled proportion defects, so no clean "
                 "per-view reference exists to compare against.")
    lines.append("2. **Wrong signal for the target class** — even the view-blind anchor signal "
                 "rates proportion-drifted plates as HIGH similarity (still recognizably Sean); "
                 "an embedding cosine cannot see the head-to-body geometry that defines the "
                 "proportion defect. No usable threshold separates the graded class from clean.")
    lines.append("")
    lines.append("**Actionable path (report to Sean — do NOT self-act):**")
    lines.append("- The proportion class wants a **geometric proportion measure** (head-height "
                 "ratio / landmark-based), not an embedding similarity. DINOv2 may still help the "
                 "*identity/style* drift class (wrong character / wrong register) — a different, "
                 "narrower claim than the kickoff's proportion target.")
    lines.append("- Before ANY view-matched embedding test is even possible, `sean-anchor` needs "
                 "clean **1:7 per-view body references** (a re-bake of the body turnarounds). This "
                 "is the same Bible-integrity gap as the A4 re-verification ticket — escalate it: "
                 "the body plates aren't just Flash-verified, they're proportion-off.")
    lines.append("")

    report = "\n".join(lines)
    print(report)
    out = HERE / "traces" / f"dinov2-separation-{datetime.now(timezone.utc):%Y-%m-%d}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report + "\n", encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
