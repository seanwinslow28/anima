# B1b — DINOv2 separation spike (2026-06-03 00:27 UTC)

Rung: **dinov2** (asserted). Performs cases: 23 (clean + identity_style). Model: facebook/dinov2-small via compute_similarity.

## Per-case scores

| case | class | graded | view | scope | view_ref (kind) | self | anchor | view |
|---|---|---|---|---|---|---|---|---|
| clean-act1-f06-idle | clean | n | — | — | — |  | 0.990 | — |
| clean-act1-f13-gesture | clean | n | — | — | — |  | 0.944 | — |
| clean-act1-f31-land | clean | n | — | — | — |  | 0.958 | — |
| clean-head-profile-left | clean | n | profile-left | head | head-profile-left.png (view+scope) | SELF | 0.729 | 1.000 |
| clean-head-back | clean | n | back | head | head-back.png (view+scope) | SELF | 0.695 | 1.000 |
| clean-expr-neutral | clean | n | — | — | — |  | 0.722 | — |
| clean-expr-surprised | clean | n | — | — | — |  | 0.740 | — |
| clean-expr-contemplative | clean | n | — | — | — |  | 0.791 | — |
| clean-head-turn-02 | clean | n | — | head | — |  | 0.670 | — |
| clean-head-turn-06 | clean | n | — | head | — |  | 0.665 | — |
| proportion-drift-body-3quarter | identity_style | Y | 3quarter | body | body-3quarter.png (view+scope) | SELF | 0.862 | 1.000 |
| proportion-jaw-body-profile-left | identity_style | Y | profile-left | body | body-profile-left.png (view+scope) | SELF | 0.866 | 1.000 |
| proportion-eyes-body-profile-right | identity_style | Y | profile-right | body | body-profile-right.png (view+scope) | SELF | 0.887 | 1.000 |
| proportion-costume-body-back | identity_style | Y | back | body | body-back.png (view+scope) | SELF | 0.819 | 1.000 |
| sprite-scale-f31-bad | identity_style | n | — | — | — |  | 0.965 | — |
| stylus-hand-f13-cc01 | identity_style | n | — | — | — |  | 0.954 | — |
| proportion-walk-cycle-source | identity_style | Y | — | body | — |  | 0.707 | — |
| identity-head-turn-01 | identity_style | Y | — | head | — |  | 0.668 | — |
| jaw-drift-head-turn-09 | identity_style | Y | — | head | — |  | 0.681 | — |
| borderline-hair-head-profile-right | identity_style | Y | profile-right | head | head-profile-right.png (view+scope) | SELF | 0.769 | 1.000 |
| borderline-expr-focused | identity_style | n | — | — | — |  | 0.787 | — |
| borderline-motion-head-turn-03 | identity_style | n | — | head | — |  | 0.650 | — |
| borderline-stylus-prop | identity_style | n | — | — | — |  | 0.648 | — |

## Separation — VIEW-MATCHED (primary; self-matches excluded)

  clean: (none)
  proportion/identity defect (graded): (none)
  (need both clean and defect view-matched scores to sweep)

## Separation — ANCHOR-ONLY (today's record-only gate signal; view-blind)

  clean                              n=10  min=0.665 mean=0.790 max=0.990
  proportion/identity defect (graded) n=8  min=0.668 mean=0.782 max=0.887
  best threshold T=0.916  →  false_pass=0/8  false_alarm=7/10  (flag when score < T)

## Confounds & findings (honest)

- **Every view-matched fixture is a SELF-MATCH** (7/7). The clean turnaround fixtures AND the proportion-DEFECT fixtures are byte-identical to the Bible's own turnaround plates. So the view-matched read is **vacuous** — there is no *distinct* per-view reference to compare a subject against; the 'reference' is the subject.
- **Root cause — contaminated references**: `sean-anchor/turnarounds/body-profile-right.png` (etc.) IS the plate the eval labels `proportion-eyes-body-profile-right` (a Cy fail @1.0, head ~1:5.3). The Bible's per-view BODY plates are the proportion-drifted ones — the record-only Pass-2.5 gate let them bake in. **There is no clean 1:7 per-view body reference in the Bible to ground a view-matched identity check.**
- **Proportion is invisible to embedding similarity**: the graded proportion defects score 0.67–0.89 vs the front anchor — overlapping/above the off-view clean head plates (0.66–0.99) — because a proportion-drifted plate is still embedding-recognizably Sean. DINOv2 cosine captures identity/style recognizability, NOT geometric proportion (the exact confabulation class that blocked references: proportion + eye-color).
- **Anchor-only ordering is dominated by VIEW, not defect**: the front-ish clean frames score highest (0.99, 0.96, 0.94), off-view cleans lowest — so a single front anchor can't threshold drift without flagging legitimate off-view cleans (false_alarm 7/10 at false_pass 0).
- **Not graded** (spatial/continuity, kickoff): borderline-expr-focused, borderline-motion-head-turn-03, borderline-stylus-prop, sprite-scale-f31-bad, stylus-hand-f13-cc01

## GO / NO-GO

**NO-GO** for DINOv2 as a view-matched identity/proportion backstop on this fixture set, for two independent reasons:

1. **Untestable as designed** — the view-matched separation is vacuous (no non-self view-matched pairs): the Bible's per-view body plates ARE the labeled proportion defects, so no clean per-view reference exists to compare against.
2. **Wrong signal for the target class** — even the view-blind anchor signal rates proportion-drifted plates as HIGH similarity (still recognizably Sean); an embedding cosine cannot see the head-to-body geometry that defines the proportion defect. No usable threshold separates the graded class from clean.

**Actionable path (report to Sean — do NOT self-act):**
- The proportion class wants a **geometric proportion measure** (head-height ratio / landmark-based), not an embedding similarity. DINOv2 may still help the *identity/style* drift class (wrong character / wrong register) — a different, narrower claim than the kickoff's proportion target.
- Before ANY view-matched embedding test is even possible, `sean-anchor` needs clean **1:7 per-view body references** (a re-bake of the body turnarounds). This is the same Bible-integrity gap as the A4 re-verification ticket — escalate it: the body plates aren't just Flash-verified, they're proportion-off.

