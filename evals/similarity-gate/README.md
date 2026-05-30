# Similarity-gate regression eval

The Pass-2.5 similarity gate (`pipeline/agents/similarity_gate.py`) scores a
generated plate against the anchor. Its method ladder prefers **DINOv2**
(semantic, scale/background-robust) when `torch + transformers + torchvision`
are installed, and falls back to a coarse **PIL-perceptual** metric otherwise.

## What this eval guards

For a held **recovered / drifted** pair on each register, the gate must score
the *recovered* plate (recognizably the character) **above** the *drifted* plate
(wrong character) when measured against the anchor. The executable assertion
lives in `tests/test_similarity_gate.py::test_dinov2_regression_recovered_above_drifted`
(skipped when torch is absent). The fixtures and the measured scores are here.

## Held pairs + measured scores (DINOv2, `facebook/dinov2-small`)

| Register | recovered vs anchor | drifted vs anchor | margin |
|----------|--------------------|--------------------|--------|
| sean-anchor (pencil-test-colored) | 0.838 | 0.755 | +0.083 |
| claude-mascot (pixel-art-8bit) | 0.858 | 0.715 | +0.143 |

Fixtures (`fixtures/`): `{sean,mascot}-{anchor,recovered,drifted}.png`.
- sean recovered = the Phase-0 anchor-only terse-prompt result; drifted = the pre-fix monochrome romance-hero head-front.
- mascot recovered = the recovered octopus head-front; drifted = the chibi-humanoid body-3quarter from the 2026-05-29 held re-bake.

## Why the gate stays RECORD-ONLY (not a hard pre-Gemini reject)

DINOv2 cleanly separates recovered from drifted **at the same view**. But across
the full plate set, legitimate view/expression variation moves the score as much
as identity drift does — measured on the sean-anchor production bake:

```
good plates:   head-back 0.695 · neutral 0.722 · head-profile-left 0.729 ·
               surprised 0.740 · head-3quarter 0.741 ... body-profile-right 0.887
drifted refs:  sean monochrome 0.755 · mascot chibi 0.715
```

The drifted references (0.715–0.755) sit **inside** the good-plate range — a
drift-catching threshold (>0.76) would false-reject head-back / neutral /
surprised; a safe threshold (<0.69) catches nothing. So a single blanket
threshold against the one front anchor cannot gate without harming good plates.
A trustworthy hard gate needs **per-view references** (compare a back-view plate
against a back-view reference), which is future work. Until then the gate
persists the DINOv2 score in `plate_verdicts.jsonl` as a record-only signal, and
the human/visual gate remains the arbiter. Prop plates are exempt entirely
(an isolated object is never identity-scored against a full-character anchor).
