# Reve vs NB2 — image-editing bake-off — 2026-06-08

Generator head-to-head. **Headline metric: DINOv2-vs-per-view-anchor**, read as the **Δ vs the `nb2` baseline** on the same case + same anchor (eval-strategy §3.5: no universal DINO threshold — the delta is the signal). Em (if run) is a **secondary** corroborator; a still-image judge is trustworthy mainly pairwise.

**DINOv2 method engaged:** dinov2 (`pil-perceptual` = torch/transformers absent → NOT a real identity read; install `torch torchvision transformers` for the DINOv2 tier).

**Stub run:** no (real generations)

## DINOv2 identity hold — case × variant (higher = closer to the per-view anchor)

| case | difficulty | nb2 | reve-standard | reve-fast | Δ(best Reve − nb2) |
|---|---|---|---|---|---|
| `t1-edit-neutral-control` | easy | 0.715 | 0.723 | 0.729 | +0.014 |
| `t1-edit-focused` | moderate | 0.774 | 0.778 | 0.774 | +0.003 |
| `t2-remix-3quarter` | hard | 0.807 | 0.848 | 0.845 | +0.041 |
| `t2-remix-3ref-pairing` | hardest | 0.905 | 0.907 | 0.881 | +0.002 |
| `t3-inbetween-f06-f10` | hard | 0.971 | 0.977 | 0.976 | +0.006 |

## Per-variant aggregate (mean ± stderr; Subject-Collapse = # below 0.5)

| variant | mean DINOv2 | stderr | SCR (below-thresh / n) | $/img |
|---|---|---|---|---|
| `nb2` | 0.835 | ±0.166 | 0/5 | $0.067 |
| `reve-standard` | 0.847 | ±0.161 | 0/5 | $0.040 |
| `reve-fast` | 0.841 | ±0.164 | 0/5 | $0.007 |

## Em verdicts (SECONDARY — reference-blind absolute; see §caveat)

| case | nb2 | reve-standard | reve-fast |
|---|---|---|---|
| `t1-edit-neutral-control` | pass | pass | borderline |
| `t1-edit-focused` | pass | pass | borderline |
| `t2-remix-3quarter` | pass | pass | borderline |
| `t2-remix-3ref-pairing` | pass | pass | pass |
| `t3-inbetween-f06-f10` | fail | pass | pass |

_Reference-blind Em. `pass` = Em accepts the output; `fail`/`borderline` = Em flags drift/register. Read as corroboration of the DINOv2 delta, not the decider._

---

## Decision — Sean's eyeball verdict: REVE FAILS for editing the Sean character

**Run:** live, 2026-06-08 UTC (executed 2026-06-07 local, isolated worktree, subscription billing for Em). DINOv2 tier engaged (`dinov2`, a real identity read). N=1 per cell. Reve schema corrected against the live API before this run (see field report + postmortem). `t3` used the real approved F06→F10 in-between (committed fixtures).

**The metric said "adopt." The human eye said "fail." The eye wins (Engine Truth).** DINOv2-vs-anchor scored Reve ≥ NB2 on identity (decisive `t2-remix-3quarter` +0.041; in-between +0.006), which *by the harness rule* would have meant pilot-keyframes + adopt-in-betweens. **But on face-crop inspection, the Reve outputs are morphed and skewed** — the body, pose, palette, and pencil-test register hold, but the *face* (the identity-critical region) distorts: asymmetric/melted eyes, skewed features. DINOv2 missed it because the face is a small fraction of a full-figure embedding and the overall composition matched the anchor — the exact §3.5 failure mode ("DINOv2 over-rewards composition; cannot be the sole good-frame gate"). **This is why the score-based verdict is overridden.**

**Verdict (Sean, 2026-06-08):**
- **Editing the Sean character (keyframes / Cy Bible / in-betweens): FAIL — do NOT adopt at any tier.** The face morph is disqualifying for an identity-locked character; pose/cost wins don't matter if the face isn't Sean.
- **reve-fast is NOT added to the in-between lineup.** NB2 remains the editing engine for Sean.
- **The "no NB-Pro downsampling regression" finding still holds** at the composition level (no washed-out/generic faces, no collapse) — but Reve substitutes a *different* identity failure (morph/skew) that is just as disqualifying for this use case.
- **Future direction (not now):** test Reve for *creating new characters* and *backgrounds* in different art styles — use cases with no existing identity to preserve, where the morph-under-edit failure mode may not apply. Reve's pose control, 16:9 native output, speed, and cost remain attractive there.

**What the metrics got right / wrong:**
- **Right:** flagged no composition collapse; cheaper at every tier; reve-standard's clean Em profile.
- **Wrong:** DINOv2-vs-full-figure-anchor cannot see facial-identity morph. N=1 + full-figure framing masked it. **Lesson: zoom to the face, and gate identity edits on the human eye (or a face-region metric / pairwise-Em), never on whole-figure DINOv2 alone.**

---

## How to read this

- **Decision metric:** the Δ column. A Reve variant earns *adopt for keyframes/Bible* only if its DINOv2 **matches or beats `nb2`** on the identity cases (`t1-edit-focused`, `t2-remix-3quarter`, `t2-remix-3ref-pairing`). A `⚠ worse` on `t2-remix-3quarter` means Reve shares NB-Pro's multi-reference downsampling regression → **disqualified for multi-ref keyframes**.
- **In-between fit:** `t3-inbetween-*` is scored against both endpoints (min). Reve Fast *adopts for in-betweens* if it holds here and `t2-remix-3quarter` shows no downsampling collapse — a mild wobble is tolerable on an in-between.
- **Em is secondary.** Reference-blind Em cannot truly verify identity (the documented limitation); it corroborates SF01/register and flags gross drift. The recommended refinement is **pairwise Em** ("is variant A or B closer to the anchor?") — not built here; see README §Em pairwise.
- **Do not** declare a winner off a `pil-perceptual` run or a stub run — neither is a real identity read.