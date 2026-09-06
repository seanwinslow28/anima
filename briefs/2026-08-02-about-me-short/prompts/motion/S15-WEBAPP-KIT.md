# S15 — the wide's clip: THE KIT for Sean's own roll (Higgsfield web app, Seedance 2.0 fast, 720p, 16:9)

Three CLI rolls of the two-keyframe wide (v2 7s, v3 7s, v4 5s) all did the same thing: **the swivel lands with the right face, then the
model rolls Sean and his chair forward until he fills a third of the frame.** Constants tried and failed: the chair "turns on the spot and
goes nowhere", "the same small far-away size in every frame", "nothing comes closer to the camera", START upscaled to the END's exact size,
no face words, 5s. The single-image v1 held his size but invented his face on the turn (law 13). Three misses = the stop rule.

**Inputs**
- START: `normalised/S15-A-all-HQ-2688.png` (your deblurred chain-5, normalised, 2688×1520)
- END: `normalised/S15-A-end-5.png` (the freeze: you facing the camera with your face, everyone mid-chaos)
- Prompt: the body of `prompts/motion/63d-M3-S15-the-wide-chaos-swivel-2kf-v4-5s.txt` (everything below the `#` header)
- What to try that the CLI cannot: **std mode** instead of fast (the doc's `fast`/`std` finding was about stutter, not framing — a different
  sampler may hold the END); **a shorter duration (4s)**; or **no END frame + `--image refs/turnaround-views/sean-v2.png` as a character
  reference** (the untested lever in `_blocks.md` § CHARACTER REFERENCES IN VIDEO — it fixes the face without a second keyframe to zoom toward).

**The $0 alternative already in the rough cut (v4):** every version completes the swivel at normal scale by ~2.4s. The cut uses v4 from
0.3s to ~2.5s (chaos, then the spin) and then cuts to the END still as the freeze — which is where the record scratch lands anyway — then
beat 12's S10 close-up for the breath. If the trimmed clip reads, no roll is needed.
