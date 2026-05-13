# Act 1 v2 — Seedance Intro (v2) Frame Selection

**Source MP4:** `runs/run_2026-04-04_174805/export/seedance-2.0-output/Act-1-Test-2-Seedance-2.0.mp4`
**Extraction:** `runs/run_2026-04-04_174805/seedance_frames/raw_24fps/frame_NNNN.png` (166 frames @ 24fps, 6.92s)
**Design spec:** `docs/2026-05-12-act1-seedance-v2-integration-design.md`
**Signed off by:** [User name + date when approved]

> **How to read this file.** Each row is one extracted 24fps frame (or a HOLD-COLLAPSE range of consecutive frames covered by the surrounding KEEP slot). KEEP rows get a unique slot number — these are the frames that go through NB2 cleanup and end up in the final assembly. HOLD-COLLAPSE ranges are dropped from the pipeline but the preceding KEEP frame is held at assembly time to cover their duration. Slot numbering is contiguous across this file and `seedance_frames_v3_loopclose/selection.md` — v2 ends at slot 074, v3 starts at slot 075.
>
> Action beats (2, 3) are written as "default KEEP — to be visually reviewed by user". The user may flip individual rows to DROP / HOLD-COLLAPSE at sign-off; downstream linter will rebuild slot numbering.

---

## Beat 1: Idle (intro) — cadence: 12fps

| Slot | Source frame | Cadence | Decision | A-N anchors | Rationale |
|---|---|---|---|---|---|
| 001 | frame_0001.png | 12fps | KEEP | approved/PT_A1_F01_key.png, approved/PT_A1_F40_key.png | Loop-start idle frame, identity baseline |
| —   | frame_0002.png – frame_0010.png | — | HOLD-COLLAPSE | — | Redundant idle — slot 001 held over this range |
| 002 | frame_0011.png | 12fps | KEEP | approved/PT_A1_F01_key.png, approved/PT_A1_F40_key.png | Breath sub-beat |
| —   | frame_0012.png – frame_0020.png | — | HOLD-COLLAPSE | — | Redundant idle — slot 002 held over this range |
| 003 | frame_0021.png | 12fps | KEEP | approved/PT_A1_F01_key.png, approved/PT_A1_F40_key.png | Breath sub-beat |
| —   | frame_0022.png – frame_0030.png | — | HOLD-COLLAPSE | — | Redundant idle — slot 003 held over this range |
| 004 | frame_0031.png | 12fps | KEEP | approved/PT_A1_F01_key.png, approved/PT_A1_F40_key.png | Last idle frame before arm-up — anticipation anchor |
| —   | frame_0032.png – frame_0040.png | — | HOLD-COLLAPSE | — | Anticipation hold — slot 004 held over this range |

## Beat 2: Arm-up + draw circle — cadence: 24fps

> Default KEEP for every 24fps frame. To be visually reviewed by user — drop any row showing morphing fingers, stylus drift, or identity wobble.
>
> Note: source range is 41–65 (25 frames) but beat 2 allocates 24 KEEP slots (005–028) so slot 029 lands cleanly on frame_0066 = beat 3 start. Frame 0041 is HOLD-COLLAPSED into slot 004's anticipation hold to absorb the seam.

| Slot | Source frame | Cadence | Decision | A-N anchors | Rationale |
|---|---|---|---|---|---|
| —   | frame_0041.png | — | HOLD-COLLAPSE | — | Beat 1→2 seam — slot 004 held over this frame |
| 005 | frame_0042.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png | Arm starts to lift — to be visually reviewed by user — default KEEP |
| 006 | frame_0043.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png | Arm rising — to be visually reviewed by user — default KEEP |
| 007 | frame_0044.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png | Arm rising — to be visually reviewed by user — default KEEP |
| 008 | frame_0045.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png | Arm rising — to be visually reviewed by user — default KEEP |
| 009 | frame_0046.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png | Arm mid-lift — to be visually reviewed by user — default KEEP |
| 010 | frame_0047.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png | Arm mid-lift — to be visually reviewed by user — default KEEP |
| 011 | frame_0048.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png | Arm mid-lift — to be visually reviewed by user — default KEEP |
| 012 | frame_0049.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png | Arm near peak — to be visually reviewed by user — default KEEP |
| 013 | frame_0050.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png | Arm at peak — stylus about to draw — to be visually reviewed by user — default KEEP |
| 014 | frame_0051.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png, approved/PT_A1_F18_key.png | Circle stroke begins — motion-line refs from F18 — to be visually reviewed by user — default KEEP |
| 015 | frame_0052.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png, approved/PT_A1_F18_key.png | Circle stroke — to be visually reviewed by user — default KEEP |
| 016 | frame_0053.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png, approved/PT_A1_F18_key.png | Circle stroke — to be visually reviewed by user — default KEEP |
| 017 | frame_0054.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png, approved/PT_A1_F18_key.png | Circle stroke — to be visually reviewed by user — default KEEP |
| 018 | frame_0055.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png, approved/PT_A1_F18_key.png | Circle stroke mid — to be visually reviewed by user — default KEEP |
| 019 | frame_0056.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png, approved/PT_A1_F18_key.png | Circle stroke mid — to be visually reviewed by user — default KEEP |
| 020 | frame_0057.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png, approved/PT_A1_F18_key.png | Circle stroke mid — to be visually reviewed by user — default KEEP |
| 021 | frame_0058.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png, approved/PT_A1_F18_key.png | Circle stroke — to be visually reviewed by user — default KEEP |
| 022 | frame_0059.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png, approved/PT_A1_F20_key.png | Trail-swirl emerging — F20 ref for trail aesthetic — to be visually reviewed by user — default KEEP |
| 023 | frame_0060.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png, approved/PT_A1_F20_key.png | Trail-swirl emerging — to be visually reviewed by user — default KEEP |
| 024 | frame_0061.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png, approved/PT_A1_F20_key.png | Trail-swirl — to be visually reviewed by user — default KEEP |
| 025 | frame_0062.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png, approved/PT_A1_F20_key.png | Trail-swirl — to be visually reviewed by user — default KEEP |
| 026 | frame_0063.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png, approved/PT_A1_F20_key.png | Trail-swirl — to be visually reviewed by user — default KEEP |
| 027 | frame_0064.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png, approved/PT_A1_F20_key.png | Trail-swirl resolving — to be visually reviewed by user — default KEEP |
| 028 | frame_0065.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png, approved/PT_A1_F20_key.png | End of arm-up beat — last frame before companion emerges — to be visually reviewed by user — default KEEP |

## Beat 3: Companion emerges from trails — cadence: 24fps SPIKE TARGET

> Default KEEP for every 24fps frame. To be visually reviewed by user — drop any row where the orange creature morphs toward the pixel-sprite / armored silhouette (the A-6 F24/F26/F28 reading) instead of the amorphous emerging form.
>
> Slot range 029–068 inclusive (40 slots) is the spike validation target.

| Slot | Source frame | Cadence | Decision | A-N anchors | Rationale |
|---|---|---|---|---|---|
| 029 | frame_0066.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | First moment companion form is visible — spike start — to be visually reviewed by user — default KEEP |
| 030 | frame_0067.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion emerging — to be visually reviewed by user — default KEEP |
| 031 | frame_0068.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion emerging — to be visually reviewed by user — default KEEP |
| 032 | frame_0069.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion emerging — to be visually reviewed by user — default KEEP |
| 033 | frame_0070.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion emerging — to be visually reviewed by user — default KEEP |
| 034 | frame_0071.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion emerging — to be visually reviewed by user — default KEEP |
| 035 | frame_0072.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion emerging — to be visually reviewed by user — default KEEP |
| 036 | frame_0073.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion emerging — to be visually reviewed by user — default KEEP |
| 037 | frame_0074.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion emerging — to be visually reviewed by user — default KEEP |
| 038 | frame_0075.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion emerging — to be visually reviewed by user — default KEEP |
| 039 | frame_0076.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion emerging — to be visually reviewed by user — default KEEP |
| 040 | frame_0077.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion emerging — to be visually reviewed by user — default KEEP |
| 041 | frame_0078.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion emerging — to be visually reviewed by user — default KEEP |
| 042 | frame_0079.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion emerging — to be visually reviewed by user — default KEEP |
| 043 | frame_0080.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion mid-emergence — to be visually reviewed by user — default KEEP |
| 044 | frame_0081.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion mid-emergence — to be visually reviewed by user — default KEEP |
| 045 | frame_0082.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion mid-emergence — to be visually reviewed by user — default KEEP |
| 046 | frame_0083.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion mid-emergence — to be visually reviewed by user — default KEEP |
| 047 | frame_0084.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion mid-emergence — to be visually reviewed by user — default KEEP |
| 048 | frame_0085.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion mid-emergence — to be visually reviewed by user — default KEEP |
| 049 | frame_0086.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion approaching shoulder — to be visually reviewed by user — default KEEP |
| 050 | frame_0087.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion approaching shoulder — to be visually reviewed by user — default KEEP |
| 051 | frame_0088.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion approaching shoulder — to be visually reviewed by user — default KEEP |
| 052 | frame_0089.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion approaching shoulder — to be visually reviewed by user — default KEEP |
| 053 | frame_0090.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion approaching shoulder — to be visually reviewed by user — default KEEP |
| 054 | frame_0091.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion approaching shoulder — to be visually reviewed by user — default KEEP |
| 055 | frame_0092.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion approaching shoulder — to be visually reviewed by user — default KEEP |
| 056 | frame_0093.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion approaching shoulder — to be visually reviewed by user — default KEEP |
| 057 | frame_0094.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion approaching shoulder — to be visually reviewed by user — default KEEP |
| 058 | frame_0095.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion approaching shoulder — to be visually reviewed by user — default KEEP |
| 059 | frame_0096.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion approaching shoulder — to be visually reviewed by user — default KEEP |
| 060 | frame_0097.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion near shoulder — to be visually reviewed by user — default KEEP |
| 061 | frame_0098.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion near shoulder — to be visually reviewed by user — default KEEP |
| 062 | frame_0099.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion near shoulder — to be visually reviewed by user — default KEEP |
| 063 | frame_0100.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion near shoulder — to be visually reviewed by user — default KEEP |
| 064 | frame_0101.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion settling on shoulder — to be visually reviewed by user — default KEEP |
| 065 | frame_0102.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion settling on shoulder — to be visually reviewed by user — default KEEP |
| 066 | frame_0103.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion settling on shoulder — to be visually reviewed by user — default KEEP |
| 067 | frame_0104.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion settling on shoulder — to be visually reviewed by user — default KEEP |
| 068 | frame_0105.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | Companion fully seated — spike end — to be visually reviewed by user — default KEEP |

## Beat 4: Hold on shoulder — cadence: 12fps

> Idle/hold beat — sample sparsely. Six KEEP slots distributed across the 61-frame hold (frames 106–166) to capture the subtle settle and breath.

| Slot | Source frame | Cadence | Decision | A-N anchors | Rationale |
|---|---|---|---|---|---|
| 069 | frame_0106.png | 12fps | KEEP | approved/PT_A1_F31_key.png, approved/PT_A1_F36_key.png | First frame post-emergence — companion fully seated |
| —   | frame_0107.png – frame_0117.png | — | HOLD-COLLAPSE | — | Hold — slot 069 held over this range |
| 070 | frame_0118.png | 12fps | KEEP | approved/PT_A1_F31_key.png, approved/PT_A1_F36_key.png | Settle sub-beat |
| —   | frame_0119.png – frame_0129.png | — | HOLD-COLLAPSE | — | Hold — slot 070 held over this range |
| 071 | frame_0130.png | 12fps | KEEP | approved/PT_A1_F31_key.png, approved/PT_A1_F36_key.png | Breath sub-beat |
| —   | frame_0131.png – frame_0141.png | — | HOLD-COLLAPSE | — | Hold — slot 071 held over this range |
| 072 | frame_0142.png | 12fps | KEEP | approved/PT_A1_F31_key.png, approved/PT_A1_F36_key.png | Breath sub-beat |
| —   | frame_0143.png – frame_0153.png | — | HOLD-COLLAPSE | — | Hold — slot 072 held over this range |
| 073 | frame_0154.png | 12fps | KEEP | approved/PT_A1_F31_key.png, approved/PT_A1_F36_key.png | Breath sub-beat |
| —   | frame_0155.png – frame_0165.png | — | HOLD-COLLAPSE | — | Hold — slot 073 held over this range |
| 074 | frame_0166.png | 12fps | KEEP | approved/PT_A1_F31_key.png, approved/PT_A1_F36_key.png | End of v2 — handoff to v3 loop-closer (slot 075) |

## Beat 5: (loop-closer starts) — see `seedance_frames_v3_loopclose/selection.md`

Slot numbering continues at slot 075 in the v3 file.

---

## Summary

| Metric | Value |
|---|---|
| Source frames extracted | 166 |
| KEEP decisions | 74 |
| DROP decisions | 0 |
| HOLD-COLLAPSE decisions | 92 |
| 12fps cadence slots | 10 (slots 001–004, 069–074) |
| 24fps cadence slots | 64 (slots 005–068) |
| Spike target slots | 029–068 (inclusive, 40 slots = beat 3, source frames 66–105) |
| Slot range covered by this file | 001–074 |
| Handoff to v3 | v3 selection.md starts at slot 075 |
