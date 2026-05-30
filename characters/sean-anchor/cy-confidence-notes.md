# Cy Confidence Notes — sean-anchor

Five prose hedges. The places Pass 1 reached a decision without full source-reference ground truth. Downstream consumers should treat these as load-bearing signals for escalation rather than trust.

## 1. Head-turn frame-to-angle mapping

The 9-frame head-turn sequence (`source-refs/head-turn/head-turn-{1..9}.png`) is preserved as the canonical motion-plate set, with frames 1 and 9 anchor-grade and the middle frames interpretive. The head TURNAROUND plates, however, are sourced from the colored turnaround sheet, not the line-art head-turn frames (the line-art-vs-color register inconsistency fixed 2026-05-29): head-front, head-3quarter, and head-profile-left are colored `#region` crops of `source-refs/turnaround-1.png`, head-profile-right and head-back are generated against the anchor. Cy did not visually verify the exact angle each head-turn frame lands on; if a Phase 6 head-turn clip needs precise per-frame angles, Sean should open the source-refs head-turn folder and confirm the 1→9 rotation direction.

## 2. Back-of-skull silhouette

The back view ingested from `source-refs/turnaround-1.png` is the only direct reference to Sean's back, and it is a single small-area view inside a larger turnaround sheet. Cy authored IR.sean.hair.center-cowlick and IR.sean.hair.silhouette-tousled-medium-short with the disclaimer that the back-view cowlick is below the visible silhouette line — true to the references, but it means the Bible cannot honestly defend a tight back-of-head crop. The generated head-back plate is Cy's best interpretation extrapolated from the profile and front references, not an observed angle.

## 3. Expression set is interpretive

The source references do not carry a discrete expression library. Cy chose the four states — neutral, focused, surprised, contemplative — by reading the emotional arc visible in the Act 1 storyboard plus the anchor's neutral baseline. NB Pro generates the four plates in Pass 2 against the anchor plus the head-front turnaround. The set is bounded by Cy's read of what the production needs at commit 2, not by what the references directly authorize. Em should treat any verdict citing an expression outside this set as a Bible silence and escalate to Sean.

## 4. Walk-cycle is a single source plate, not a cycle

The canonical motion plate `motion_plates/walk-cycle-source.png` is ingested from a single source line-art pose. It is not a 12-frame or 8-frame cycle suitable for direct runtime reuse. The IR.sean.motion.walk-cycle-neutral-gait-source-plate rule describes the plate's load — stride length, arm swing arc, posture — as proportion-and-rhythm reference for Phase 6 motion clips, not as frame-by-frame reuse material. The derived plates in source-refs are stylistic experiments and were not promoted into the Bible.

## 6. Generated faces lean more realistic than the round-cartoon anchor (known item)

The 2026-05-29 production bake recovered identity and full color decisively — the generated head and expression plates are recognizably Sean, consistent across plates, and a categorical improvement over the pre-fix monochrome "different person." The remaining gap, flagged by Sean at the Phase 5 review and shipped knowingly: the generated faces read a touch more *realistic-handsome* than the anchor's *friendlier rounder cartoon*. This is a stylization-amount drift, not an identity drift — same character, slightly less cartoon. A future tuning pass (prompt nudge toward "rounder cartoon proportions," or a character LoRA trained on the round anchor) should pull them back toward the anchor's register. Not blocking for commit 2; logged so the next session doesn't rediscover it.

## 5. Full color is canonical — the skin and eye hexes are sampled, not measured

Full color is canonical Sean (director decision, 2026-05-29). The earlier "no explicit skin tone / skin is paper-base" spec was the visual-fidelity bug, not the character; `IR.sean.palette.warm-skin-tone` and `IR.sean.palette.full-color-pencil-test-vocabulary` now carry the anchor's real palette. The remaining hedge is precision, not presence: the skin hex `#F0DFCB` and the eye hex `#4A6D8C` were sampled/estimated from the anchor by eye, and the eye rule says "adjust on review." Sean should eyeball both against the anchor before approval and nudge either hex if it reads off. The register stays pencil-test (flat color fills with warm-graphite cross-hatched shadow, never gradient- or cel-shaded); "full color" means the anchor's limited, desaturated palette, not a rendering-style change.
