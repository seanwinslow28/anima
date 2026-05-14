# Act 1 v2 Spike Validation

**Date:** 2026-05-13
**Reviewer:** Sean Winslow
**Spike scope:** Slots 029–068 (companion emerges from trails beat, 40 frames @ 24fps)

**Artifacts:**
- Cleaned PNGs: `runs/run_2026-04-04_174805/seedance_clean_v2/PT_A1_v2_slot{029..068}.png`
- Contact sheet: `runs/run_2026-04-04_174805/audit/spike_contact_sheet.png`
- Assembled clip: `runs/run_2026-04-04_174805/audit/spike.mp4` (1.67s @ 24fps, 1920×1080)
- Frame sequence: `runs/run_2026-04-04_174805/audit/spike_sequence/frame_{0001..0040}.png`
- Cleanup log: `runs/run_2026-04-04_174805/audit/spike_cleanup.log` (40/40 cleanup success, 0 errors)
- HF01 audit log: `runs/run_2026-04-04_174805/audit/spike_hf01.log` (40/40 HF01 PASS, 0 FAIL)

**Cleanup pipeline notes:**
- All 40 slots cleaned successfully on attempt 1; zero retries needed.
- Chained-reference cleanup applied (every frame after slot 029 used the prior cleaned frame as a 4th reference, alongside A-2, A-6 F22, A-7 F31, and the Seedance source frame).
- Technical pipeline (subprocess, cmd construction, retry ladder, file promotion) worked correctly.

## Per-criterion verdict

| Criterion | Verdict | Notes |
|---|---|---|
| No visible boil between adjacent frames | FAIL | Frames jump back and forth sporadically — not a smooth temporal progression. Reads as messy AI noise, not artistic boiling lines. |
| Identity holds (SF02) | FAIL | Sean is inconsistent across frames — different colored shirts and other details vary. Identity drift visible across the 40-frame stretch. |
| Stylus in right hand (CC01) every frame | Not evaluated (gated by other failures) | — |
| Companion stays orange + amorphous (CMP01) | Not evaluated (gated by other failures) | — |
| Pencil-test fidelity matches A-2 | FAIL | Inconsistent style — some frames more colored/finished, others more rough pencil. |

## Overall verdict

**[x] FAIL — see "Replan options" below**

## Root cause (per user observation)

The reference layering used in this spike was:
1. A-2 anchor (`approved/PT_A1_F01_key.png`) — pencil-test style target
2. Beat-matched A-N anchors (A-6 F22, A-7 F31)
3. Seedance source frame (also serves as style/identity ref by virtue of being a reference at all)
4. Previous cleaned frame (24fps chained reference)

The issue: NB2 is being asked to derive Sean's identity from a mix of these refs. The A-N approved anchors are rough pencil-test sketches with limited color/finish information; the Seedance source frames carry their own (different) interpretation of Sean; the prev-cleaned chained reference compounds drift across the stretch. Result: identity wobble + style drift across frames.

**The user's preferred reference layering:**
- **Canonical character reference** (identity anchor): `runs/sw-portfolio-frame_0001.png` OR `runs/run_2026-04-04_174805/export/sw-portfolio-animation-frames-4-7/frame_0001.png` (1.5 MB version with full identity information — hair, shirt, build, face).
- **Pose reference** (what NB2 should replicate as a pose, NOT as identity): the Seedance frame for that slot.
- Approved A-N pencil-test anchors should NOT be primary identity references — they introduce sketch-variation that compounds across a 40-frame stretch.

## Replan direction (for tomorrow's session)

Sean is going to manually curate the frames to clean on iPad before we re-run NB2. Open questions to resolve before the next spike:

1. **Reference layering update.** Refactor `seedance_v2_cleanup.py` so the reference stack is:
   - Slot 1: `runs/sw-portfolio-frame_0001.png` (canonical character identity) — always
   - Slot 2: Seedance source frame (pose reference)
   - Slot 3 (optional, 24fps only): previous cleaned frame for temporal consistency

   Drop the A-N approved anchors from the cleanup prompt path — they're hurting identity stability more than they help.

2. **Universal prompt tightening.** The prompt should emphasize "match the character in REF 1 (identity). Replicate the EXACT pose / position / gesture from REF 2 (Seedance source). Do not invent details. Keep clothing consistent across frames."

3. **Manual frame curation.** Sean will pre-curate which Seedance frames to clean (on iPad). This means updating `selection.md` to mark a smaller, hand-picked KEEP set instead of "default KEEP every 24fps frame."

4. **selection.md format implication.** Either re-author selection.md against the new curated set, or add a new column / DROP-flag mechanism so the linter respects manual culls without needing a full rewrite.

5. **Re-run the spike** with the new reference layering on the manually-curated frames. Same 5 pass criteria.

## Stopping point (2026-05-13)

- 40 NB2 calls spent on the failed spike (~$1.60 sunk cost).
- All artifacts preserved in `runs/run_2026-04-04_174805/seedance_clean_v2/` and `runs/run_2026-04-04_174805/audit/`.
- Pipeline scripts (`seedance_v2_select.py`, `seedance_v2_cleanup.py`, `seedance_v2_audit.py`) are functional but need reference-layering changes per Replan #1.
- Production checklist + CHANGELOG NOT updated since v2 integration is still in progress, not shipped.
- Original Act 1 (`pencil-test-act1.{mp4,webm,gif}`) remains untouched as the production loop.

**Resume tomorrow:** start by reviewing the manually-curated frame list from Sean's iPad, then update `selection.md` and refactor `seedance_v2_cleanup.py`'s `build_references()` per Replan #1 before re-running the spike.
