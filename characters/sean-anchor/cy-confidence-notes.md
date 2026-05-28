# Cy Confidence Notes — sean-anchor

Five prose hedges. The places Pass 1 reached a decision without full source-reference ground truth. Downstream consumers should treat these as load-bearing signals for escalation rather than trust.

## 1. Head-turn frame-to-angle mapping

The source-refs/notes.md states that the first and last frames of the 9-frame head-turn sequence are anchor-grade and the middle frames are interpretive. Cy mapped `head-turn-1.png` to head-profile-left, `head-turn-9.png` to head-profile-right, and `head-turn-5.png` to head-front, then generated the front-facing head turnaround anchored on the two profile ingests plus the existing A-2 anchor. This mapping is a reasonable inference from a 9-frame symmetric turn, but Cy did not visually verify the angle of each numbered frame. If the actual sequence runs the other direction (frame 1 is the other-side profile, frame 9 the first) or if frame 5 is not the front-facing midpoint, the plate ingestion in Pass 2 will pull the wrong frames into the wrong turnaround slots. Sean should sanity-check the mapping by opening the source-refs head-turn folder before approval.

## 2. Back-of-skull silhouette

The back view ingested from `source-refs/turnaround-1.png` is the only direct reference to Sean's back, and it is a single small-area view inside a larger turnaround sheet. Cy authored IR.sean.hair.center-cowlick and IR.sean.hair.silhouette-tousled-medium-short with the disclaimer that the back-view cowlick is below the visible silhouette line — true to the references, but it means the Bible cannot honestly defend a tight back-of-head crop. The generated head-back plate is Cy's best interpretation extrapolated from the profile and front references, not an observed angle.

## 3. Expression set is interpretive

The source references do not carry a discrete expression library. Cy chose the four states — neutral, focused, surprised, contemplative — by reading the emotional arc visible in the Act 1 storyboard plus the anchor's neutral baseline. NB Pro generates the four plates in Pass 2 against the anchor plus the head-front turnaround. The set is bounded by Cy's read of what the production needs at commit 2, not by what the references directly authorize. Em should treat any verdict citing an expression outside this set as a Bible silence and escalate to Sean.

## 4. Walk-cycle is a single source plate, not a cycle

The canonical motion plate `motion_plates/walk-cycle-source.png` is ingested from a single source line-art pose. It is not a 12-frame or 8-frame cycle suitable for direct runtime reuse. The IR.sean.motion.walk-cycle-neutral-gait-source-plate rule describes the plate's load — stride length, arm swing arc, posture — as proportion-and-rhythm reference for Phase 6 motion clips, not as frame-by-frame reuse material. The derived plates in source-refs are stylistic experiments and were not promoted into the Bible.

## 5. Skin tone is intentionally absent in this register

The pencil-test-colored register flattens skin to the cream paper substrate showing through, with cross-hatching in warm graphite for shadow. Cy authored IR.sean.palette.no-explicit-skin-tone to make this property explicit at the Bible level, because a downstream agent reading only the four-step palette might otherwise assume skin tone was a Bible silence (an unauthored rule) rather than a register property (a deliberate absence). If a future piece needs Sean rendered with lit skin, the correct path is a style register escalation to a separate Bible variant — not a palette extension to this one.
