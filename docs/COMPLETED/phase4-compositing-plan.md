# Phase 4 Compositing Plan — Sprite Transitions

**Date:** 2026-04-08
**Route:** B (Layer Separation) with Route C smear fallback
**Scope:** F28→F31 sprite landing + F36→F40 sprite fade
**Prerequisite:** Procreate sprite extraction (manual, ~30 min)

---

## Overview

Two transitions need compositing work:

1. **F28→F31 (Beat 2→3 boundary):** Sprite teleports from bouncing at arm's length to sitting on the shoulder. Sean's pose snaps from arm-extended to relaxed-head-turned. No transition frames exist.
2. **F36→F40 (sprite fade):** Sprite pops off between F37 and F38 instead of dissolving over 3 frames as the storyboard specifies.

**Strategy:** Decouple the sprite from the character animation. Generate Sean-only in-betweens for the pose transition, then composite the sprite at interpolated positions using a Python script with arc-based flight path and multiply blending.

---

## Pre-Flight: Procreate Sprite Extraction

> **This step must be completed by Sean before any pipeline work begins.**
> See the detailed Procreate instructions in `docs/procreate-sprite-extraction-guide.md`.

### Assets to Produce

| Asset | Source | Pose | Output Path | Status |
|-------|--------|------|-------------|--------|
| `sprite_seated_alpha.PNG` | Generated standalone via Gemini (`sprite_shoulder_standalone_01.png`), extracted in Procreate with mask trick | Perched on curved shoulder, facing camera-left, desaturated graphite | `candidates/sprite/sprite_seated_alpha.PNG` | DONE |

**Source pipeline:** F31 shoulder crop used as Gemini reference → standalone sprite generated at 3:4 → Procreate mask trick extraction → RGBA PNG at 1376x768 (90.9% transparent, 9.1% semi-transparent pencil lines, 0% fully opaque).

### Why This Asset

The sprite needed to match what's baked into F31/F36 — facing left, perched on a curved shoulder, desaturated pencil style. The original `seated_sprite_01.png` faced right and sat on a flat surface. We cropped the sprite from F31 as a reference, generated a clean standalone via Gemini, then Sean extracted it in Procreate using the luminosity mask trick.

---

## Step 1: Generate Sean-Only In-Betweens (F28→F31)

### 1a. Skeleton Extraction

Extract DWPose skeletons from F28 and F31 boundary keyframes. These must be Sean-only poses — the skeleton extractor will detect Sean's body (the larger figure), not the sprite.

```bash
python3 pipeline/generate_inbetweens.py --extract-only \
  --frames F28,F31 \
  --run-dir runs/run_2026-04-04_174805
```

If the skeleton extractor picks up the sprite as a second person, crop or mask the sprite region before extraction.

### 1b. Skeleton Blending

Generate 2 interpolated skeletons for the F28→F31 transition:

| IB | Blend Factor | Easing | Sean's Pose |
|----|-------------|--------|-------------|
| IB01 | 0.40 | ease-out | Arm ~60% lowered, head beginning to turn left |
| IB02 | 0.75 | ease-out | Arm nearly at side, head mostly turned left |

Ease-out (fast departure from F28, slow arrival at F31) because the arm drops with gravity and the head turn decelerates into the hold.

```bash
python3 pipeline/generate_inbetweens.py --blend-only \
  --transition F28toF31 \
  --factors 0.40,0.75 \
  --easing ease_out_2 \
  --run-dir runs/run_2026-04-04_174805
```

### 1c. Review Blended Skeletons

**Checkpoint:** Read both blended skeleton images before generating. Verify:
- Arm arc looks natural (follows a curved path, not a straight diagonal)
- Head rotation is progressive
- No limb intersection or unnatural joint angles
- The IB01 skeleton shows a clear midpoint between extended arm and relaxed arm

If skeletons look unnatural at these blend factors, adjust to 0.33/0.67 (linear) or manually edit the skeleton joint positions.

### 1d. Write Prompts

Write prompts for 2 Sean-only in-betweens. Critical differences from previous IB prompts:
- **NO sprite mentioned** — Sean is alone in the frame
- Reference F28 for style continuity (it's the nearest keyframe in the same beat)
- Explicit "NO small character, NO sprite, NO companion figure" negative constraint
- Match F28/F31 scale and position

Save to:
- `prompts/in-betweens/F28toF31_IB01.txt`
- `prompts/in-betweens/F28toF31_IB02.txt`

### 1e. Generate via Gemini

```bash
# IB01 — arm lowering, head beginning to turn
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/in-betweens/F28toF31_IB01.txt)" \
  --output runs/run_2026-04-04_174805/candidates/inbetweens/PT_A1_F28toF31_IB01.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png runs/run_2026-04-04_174805/approved/PT_A1_F28_key.png \
  --env-file .env

# IB02 — arm nearly down, head mostly turned
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/in-betweens/F28toF31_IB02.txt)" \
  --output runs/run_2026-04-04_174805/candidates/inbetweens/PT_A1_F28toF31_IB02.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png runs/run_2026-04-04_174805/approved/PT_A1_F31_key.png \
  --env-file .env
```

### 1f. Audit Generated Frames

For each generated IB, check:
- [ ] Sean is alone (no sprite, no extra figures)
- [ ] Stylus in RIGHT hand (CC01)
- [ ] Dark navy t-shirt (CC03)
- [ ] Pencil test aesthetic on cream paper (HF02, HF05)
- [ ] Scale matches F28/F31 (CC05)
- [ ] Pose matches the skeleton blend (arm position, head angle)

Copy approved frames:
```bash
cp candidates/inbetweens/PT_A1_F28toF31_IB01.png approved/PT_A1_F28toF31_IB01.png
cp candidates/inbetweens/PT_A1_F28toF31_IB02.png approved/PT_A1_F28toF31_IB02.png
```

---

## Step 2: Sprite Compositing Script

### 2a. Write `pipeline/composite_sprite.py`

A Python script using PIL/Pillow that:

1. **Loads** the Sean-only IB frames and the extracted seated sprite asset
2. **Interpolates** the sprite's position along an arc path from F28 position to F31 position
3. **Interpolates** scale from the F28 sprite size down to the F31 shoulder size
4. **Composites** using multiply blend mode to preserve paper texture
5. **Outputs** final composite frames

### 2b. Sprite Position Data

Measure from the approved keyframes (values are approximate — refine after extraction):

| Parameter | F28 Value | F31 Value |
|-----------|-----------|-----------|
| Sprite center X | ~920 px | ~540 px |
| Sprite center Y | ~350 px | ~180 px |
| Sprite height | ~120 px | ~80 px |
| Sprite rotation | 0 deg | 0 deg |

### 2c. Flight Path Math

```python
import math

def sprite_position(t, start, end, arc_height=80):
    """
    Interpolate sprite position along a parabolic arc.
    t: 0.0 (at F28) to 1.0 (at F31)
    arc_height: pixels above the straight-line path at midpoint
    """
    # Linear interpolation for X and Y
    x = start[0] * (1 - t) + end[0] * t
    y = start[1] * (1 - t) + end[1] * t

    # Parabolic arc offset (peaks at t=0.5)
    y -= arc_height * math.sin(t * math.pi)

    return int(x), int(y)

def sprite_scale(t, start_h, end_h):
    """Interpolate sprite height with ease-out."""
    # Ease-out: fast at start, slow at end
    t_eased = 1 - (1 - t) ** 2
    return start_h * (1 - t_eased) + end_h * t_eased
```

### 2d. Multiply Blend Mode

To prevent the "pasted on" look, use multiply blending instead of simple alpha paste:

```python
from PIL import Image, ImageChops

def composite_multiply(background, sprite, position):
    """
    Composite sprite using multiply blend, preserving paper texture.
    Multiply: result = (bg * sprite) / 255
    Paper grain shows through the sprite's lighter areas.
    """
    # Create a white canvas the size of the background
    sprite_layer = Image.new("RGBA", background.size, (255, 255, 255, 255))

    # Paste sprite onto the white canvas at the target position
    sprite_layer.paste(sprite, position, sprite)  # alpha-masked paste

    # Multiply blend: dark pencil lines darken the paper, white areas = no change
    bg_rgb = background.convert("RGB")
    sprite_rgb = sprite_layer.convert("RGB")
    multiplied = ImageChops.multiply(bg_rgb, sprite_rgb)

    # Convert back to RGBA and return
    return multiplied.convert("RGBA")
```

**Why multiply works here:** In multiply mode, white pixels (255) have no effect — they leave the background untouched. Dark pencil lines (50-100 value) darken the paper texture beneath them. This means the cream paper grain shows through the sprite's lighter areas, making it look drawn-on rather than pasted-on.

---

## Step 3: Sprite Fade (F38-F40)

Much simpler. The sprite is already baked into F36 (held through F37). For F38 and F39, composite the seated sprite at the F31 shoulder position with decreasing opacity.

| Frame | Sprite Opacity | Source for Sean |
|-------|---------------|-----------------|
| F36 (0036-0037) | 100% (baked in) | No compositing needed |
| F38 (0038) | 66% | Use existing F36toF40_IB01 + sprite overlay |
| F39 (0039) | 33% | Use existing F36toF40_IB02 + sprite overlay |
| F40 (0040-0042) | 0% (gone) | No compositing needed (A-2 anchor) |

```python
def fade_sprite(sean_frame, sprite, position, opacity):
    """Apply sprite at reduced opacity."""
    faded = sprite.copy()
    alpha = faded.getchannel("A")
    alpha = alpha.point(lambda a: int(a * opacity))
    faded.putalpha(alpha)
    return composite_multiply(sean_frame, faded, position)
```

---

## Step 4: Update Assembly

### 4a. New Frame Sequence

The assembly script needs to include the new F28→F31 in-betweens and the composited sprite frames. Updated beat boundary:

```
# Beat 2→3 transition (UPDATED):
F28_key            hold 2   (frames 0028-0029)  sprite bounces (reduced from 3)
F28toF31_IB01_comp hold 1   (frame  0030)       sprite flight arc mid
F28toF31_IB02_comp hold 1   (frame  0031)       sprite approaching shoulder
F31_key            hold 2   (frames 0032-0033)  sprite lands (reduced from 3)

# Beat 3 fade (UPDATED):
F36_key            hold 2   (frames 0036-0037)  the nod (sprite 100%)
F36toF40_IB01_comp hold 1   (frame  0038)       sprite at 66% opacity
F36toF40_IB02_comp hold 1   (frame  0039)       sprite at 33% opacity
F40_key            hold 3   (frames 0040-0042)  return to idle (sprite gone)
```

Net frame change: +2 frames from the F28→F31 IBs, -2 from reducing F28 hold (3→2) and F31 hold (3→2) = **0 net change, still 42 frames, still 3.5s**.

### 4b. Rebuild and Export

```bash
bash pipeline/assemble.sh runs/run_2026-04-04_174805
```

---

## Step 5: Route C Fallback

If the composited sprite looks "pasted on" after multiply blending and all mitigations, fall back to Route C:

1. Replace the 2 composite IB frames with a **single smear frame** showing:
   - Sean's arm blurring downward (drybrush multi-position ghost, same as frame 0016)
   - The sprite trailing as a motion smear from the arm to the shoulder
2. Generate via Gemini with the drybrush smear technique
3. Use the compositing script ONLY for the sprite fade (F38-F40), where accuracy demands are lower

---

## Verification Checkpoints

### 30% — Extraction + First IB
- [ ] Both sprite PNGs extracted with clean transparency
- [ ] First Sean-only IB (F28toF31_IB01) generated and approved
- [ ] Sprite compositing script runs end-to-end on one test frame

### 60% — All Composites Done
- [ ] Both Sean-only IBs approved
- [ ] All 4 composite frames produced (2 flight + 2 fade)
- [ ] Visual inspection: sprite doesn't look "pasted on"
- [ ] Multiply blending preserves paper texture through sprite

### 90% — Assembly + Final QA
- [ ] Updated assembly with composited frames
- [ ] 42 frames, 3.5s, seamless loop
- [ ] GIF < 5MB, MP4 and WebM within spec
- [ ] Playback at 12fps: sprite flight reads as intentional motion
- [ ] Sprite fade is smooth, not a pop
- [ ] Continuity audit passes CC01-CC08

---

## Execution Order

| Step | Task | Who | Tool |
|------|------|-----|------|
| 0 | Sprite extraction in Procreate | Sean | Procreate (see guide) |
| 1a-c | Skeleton extraction + blending | Claude Code | `generate_inbetweens.py` |
| 1d-e | Write prompts + generate Sean IBs | Claude Code | `gemini-pencil-animation-image-gen` |
| 1f | Audit Sean IBs | Claude Code | Vision review |
| 2 | Write + run compositing script | Claude Code | `pipeline/composite_sprite.py` |
| 3 | Sprite fade compositing | Claude Code | `pipeline/composite_sprite.py` |
| 4 | Update assembly + rebuild exports | Claude Code | `assemble.sh` |
| 5 | Phase E QA re-review on transitions | Claude Code | `creative-director` |
