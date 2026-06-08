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

## Decision (applying the rule above)

**Run:** live, 2026-06-08 UTC (executed 2026-06-07 local, an isolated worktree, subscription billing for Em). DINOv2 tier engaged (`dinov2`, a real identity read). N=1 generation per cell. The Reve endpoint schema was wrong as scaffolded and was **corrected against the live API** before this run (see the field report + postmortem). `t3` uses the real approved F06→F10 in-between (committed fixtures), not the original turnaround stand-ins.

**1 — The decisive question (multi-reference downsampling): ANSWERED — Reve does NOT share NB-Pro's regression.** On `t2-remix-3quarter`, *both* Reve variants **beat** NB2 (standard +0.041, fast +0.038) — no `⚠ worse`, no washed-out/generic face (confirmed by eye). This was the #1 open question the bake-off existed to settle. Reve is **not disqualified** for multi-reference keyframes.

**2 — Keyframe / Cy Bible (reve-standard): viable adopt candidate — pilot, don't wholesale-migrate.** reve-standard **matches or beats** NB2 on all three identity cases (`t1-focused` +0.003, `t2-remix-3quarter` +0.041, `t2-remix-3ref-pairing` +0.002), at ~40% lower cost ($0.040 vs $0.067) and in true 16:9. It clears the rule's keyframe bar. **reve-fast is the wrong tier for keyframes** — it slips to −0.024 on the hardest 3-ref pairing (within tolerance, *not* a collapse, but below NB2).

**3 — In-between (reve-fast): ADOPT.** reve-fast holds `t3-inbetween` (+0.006 vs NB2) and the decisive `t2-remix-3quarter` shows no collapse — both rule conditions met. At ~10× lower cost ($0.007 vs $0.067) and ~2× faster (11–14s vs 20–26s), this is the strongest, cleanest result.

**Honesty caveats (these bound the verdict):**
- **Small margins, N=1.** Per-case Δ ranges +0.002…+0.041 with one generation per cell — there is no per-case stderr, so the sub-0.04 deltas are ties within noise. The conclusions rest on the *direction* (no collapse; Reve ≥ NB2 on identity) more than the magnitude. For a stronger keyframe verdict, run the documented **pairwise-Em** refinement + a replicated (N≥3) pass before trusting Reve with hero keyframes.
- **DINOv2 over-rewards copying (§3.5).** NB2 reinterprets more (re-poses to a *walking* figure, more polished/finished line, 1024² square — `invoke_image_edit` passes no aspect_ratio); both Reve variants stay closer to the reference composition + the looser pencil-test line + 16:9. So part of Reve's edge is "stayed closer to the reference," which is *desirable* for identity-hold-under-edit but should not be read as "Reve is the better illustrator."
- **Em (secondary) nuance.** reve-standard earned clean passes 5/5 (best profile); reve-fast drew `borderline` on three simple cases (mild register/identity caution); NB2's lone `fail` is on `t3` and is a **beat-fidelity** flag (NB2 rendered a walking pose, not the idle→raised-gesture in-between), not an identity collapse — illustrating why DINOv2 decides and Em corroborates.

**Bottom line:** Reve clears the bar the bake-off set. Pilot **reve-standard for multi-reference keyframes / Cy Bible plates** and **adopt reve-fast for in-betweens**; keep NB2 the incumbent until a replicated + pairwise-Em pass confirms the small-margin keyframe call. Cost is a tailwind (cheaper at every tier), not the decider.

---

## How to read this

- **Decision metric:** the Δ column. A Reve variant earns *adopt for keyframes/Bible* only if its DINOv2 **matches or beats `nb2`** on the identity cases (`t1-edit-focused`, `t2-remix-3quarter`, `t2-remix-3ref-pairing`). A `⚠ worse` on `t2-remix-3quarter` means Reve shares NB-Pro's multi-reference downsampling regression → **disqualified for multi-ref keyframes**.
- **In-between fit:** `t3-inbetween-*` is scored against both endpoints (min). Reve Fast *adopts for in-betweens* if it holds here and `t2-remix-3quarter` shows no downsampling collapse — a mild wobble is tolerable on an in-between.
- **Em is secondary.** Reference-blind Em cannot truly verify identity (the documented limitation); it corroborates SF01/register and flags gross drift. The recommended refinement is **pairwise Em** ("is variant A or B closer to the anchor?") — not built here; see README §Em pairwise.
- **Do not** declare a winner off a `pil-perceptual` run or a stub run — neither is a real identity read.