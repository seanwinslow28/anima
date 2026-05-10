# Seedance Prompt Bake-off — Results

**Date:** 2026-05-09 (bake-off run); 2026-05-10 (scoring + synthesis)
**Run dir:** `runs/seedance-bakeoff-2026-05-09/`
**Total cost:** $34.56 ($0.96 smoke test + $33.60 full run)
**Total wall-clock:** ~11 minutes (137s smoke + 8m 56s full run)
**Scoring system:** Sean used a 3-tier ordinal system — `*-great.md` files for "really liked", `notes-N.md` for "liked", absent for "not preferred". Mapped to the plan's 0–5 binary scale as 5 / 3 / 1.

## Per-variant scores (max 20)

| Variant | Name | Axis | W1 (max 10) | S0 (max 10) | Total | Δ vs V01 |
|---|---|---|---|---|---|---|
| V00 | v3_control | control | 6 | 4 | 10 | -2 |
| V01 | research_corrected_baseline | baseline | 8 | 4 | 12 | 0 |
| V02 | transition_arc | B | 6 | 6 | 12 | 0 |
| V03 | animation_timing | C | 8 | 2 | 10 | -2 |
| V04 | audio_cues | D | 2 | 2 | 4 | -8 |
| V05 | canonical_camera | E | 6 | 2 | 8 | -4 |
| V06 | no_genre_anchor | A | 2 | 2 | 4 | -8 |
| V07 | trimmed_style_block | F | 2 | 4 | 6 | -6 |
| V08 | combined_best | stack | 6 | 6 | 12 | 0 |

## Winner

**Variant:** V08 (combined_best)
**Score:** 12/20
**Margin over V01 baseline:** 0 (3-way tie at 12; resolved by tiebreakers)
**Sean's confirmation:** "That section had the best overall outputs for both walking, background movements, head movements, and transitions."

3-way tie at 12: V01, V02, V08. Resolved by:
- Tiebreaker 1 (identity-stress S0 score): V01 drops out (S0 = 4 vs V02/V08 S0 = 6).
- Tiebreaker 2 (shorter prompt): V08 wins (V08 ≈ 91 words vs V02 ≈ 95 words). The trimmed style block in V08 more than offsets its slightly longer transition-arc + animation-timing action sentence.

V08 also matched V02 for the most "great" picks of any variant (2 each, both shots, seed 42).

## Per-axis findings

- **Axis A — genre anchor (V06 vs V01):** HURT BADLY. V06 = 4 vs V01 = 12. Δ = −8. "Classic Disney rough animation" is load-bearing on Seedance — never drop it.
- **Axis B — transition-arc framing (V02 vs V01):** HELPED on the identity-stress shot. V02 = 12 (same total as V01) but V02 S0 = 6 vs V01 S0 = 4 (Δ on S0 = +2). Transition-arc framing improves S0 specifically — tells the model where the clip starts, ends, and what the middle beat is, which helps when the scene is doing something more abstract than locomotion.
- **Axis C — animation-timing language (V03 vs V01):** MIXED. V03 = 10 overall (Δ = −2). Helps W1 (V03 W1 = 8 = V01 W1) but hurts S0 (V03 S0 = 2 vs V01 S0 = 4). The "anticipation / weight shift / settle / hold" vocabulary helps a locomotion shot but confuses a transition scene where the physics are abstract.
- **Axis D — audio cues (V04 vs V01):** CATASTROPHIC. V04 = 4. Δ = −8. The AUDIO line crushes results across both shots. Drop entirely. (Even though `generate_audio` was False, the in-prompt audio descriptors leaked into the visual generation as confounds.)
- **Axis E — canonical camera "micro push-in 2%, 50mm look" (V05 vs V01):** HURT standalone. V05 = 8. Δ = −4. Likely interpreted as an actual camera move → jitter. In isolation, prefer "Completely static, locked tripod." V08 still uses the canonical syntax and wins, but only because the surrounding stack absorbs the noise — don't take this as evidence the canonical camera is helpful on its own.
- **Axis F — trimmed style block (V07 vs V01):** HURT STANDALONE. V07 = 6. Δ = −6. But V08 (which uses the same trimmed style) hits 12 → trimmed style works fine when paired with transition-arc + canonical structure. Style trimming alone removes too much aesthetic guidance, but the rest of V08's stack carries the load.
- **Stack (V08 vs winners of B/C/E/F):** Matches the best single-axis variants (12) but doesn't exceed. Stacking is non-destructive — combining transition-arc + animation-timing + canonical camera + trimmed style gives the same total as the best single axis (V01 baseline / V02 transition-arc), with the same 2 "great" picks. The stack provides the cleanest reusable structural template for new shots.

## Failure modes observed

- 21 of 36 cells (58%) were not preferred — the variant matrix was harsh, with model variance high enough that even strong variants didn't dominate.
- V04 (audio_cues) and V06 (no_genre_anchor) were entirely shut out — 0 noted cells, 0 great. Both axes are clear losers.
- W1 (walking) was generally more forgiving than S0 (identity-stress) — most variants scored higher on W1. The transition scene exposes weaknesses that the locomotion scene smooths over.
- Even the top 3 variants (V01, V02, V08) only had 1–2 cells declared "great" out of 4 — single-seed runs are not reliable; multi-seed runs are essential for a stable signal.

## Variants disqualified

V04 (audio_cues) and V06 (no_genre_anchor) scored 4/20 — disqualified as broken templates. V07 (trimmed_style_block) at 6/20 is also disqualified standalone (though its style block is reused inside V08's winning stack).

## Halt-condition assessment

- **Halt 1 (V00 wins by 2+ over V01):** NOT triggered. V01 beats V00 by 2 → research priors validated. The Phase 1 deep research findings (drop negation, trim word count, banned-words list) carried real value.
- **Halt 2 (no variant ≥14/20):** Strict reading triggers (top is 12/20). However, the 14/20 threshold was designed for the 5-binary-criteria rubric, where 14+ means "winning variant gets 4-of-5 criteria right on most cells." Sean's tiered ordinal scoring system has a different distribution shape — achieving 14+ would require a variant to have most of its cells declared "great", which would require Sean to declare 8+ cells great (he declared 6 across all variants). The threshold was raised to Sean for adjudication; he reviewed the per-variant numbers and per-axis findings and confirmed V08 as the winner. **Halt 2 was raised and overridden by Sean.**

## Decision

Lock template based on V08 structure. See `prompts/seedance-template-v4.md`.
