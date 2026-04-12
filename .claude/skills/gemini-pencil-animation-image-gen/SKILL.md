---
name: gemini-pencil-animation-image-gen
description: Generate traditional animation pencil test drawings, character design sketches, expression sheets, pose studies, turnaround sheets, and scene compositions using Google Gemini's image generation API. Use when creating pencil animation art, pencil test drawings, animation sketch characters, character design sketches, traditional animation style illustrations, animation production art, pencil drawings of characters, or animator sketchbook-style images. Triggers on "pencil animation", "pencil test", "animation sketch", "character design sketch", "pencil drawing", "animation production art", "traditional animation style", "animator drawing", "Disney sketch style".
---

# Gemini Pencil Animation Image Generator

## Purpose

Generate character designs, expression sheets, pose studies, turnaround sheets, and scene compositions in the traditional animation pencil test style using the Gemini image generation API. Produces warm, hand-drawn graphite artwork on cream animation paper — the look of a professional animator's sketchbook or a "making of" art book page.

## When to Use

- Creating character design sketches in a traditional animation pencil test style
- Generating a pencil-drawn character based on a real person's reference photo
- Building expression sheets (6-9 facial expressions of one character)
- Producing pose study / action sheets with multiple full-body poses
- Creating turnaround sheets (front, 3/4, side, 3/4 back, back views)
- Composing scene sketches with characters interacting in an environment
- Making character comparison lineups for cast design
- User mentions "pencil animation", "pencil test", "animation sketch", "character design drawing", "traditional animation", or "animator sketchbook"

## Examples

**Example 1: Character design from a photo**
```
User: "Draw me as a pencil animation character based on this photo"
Claude: [Uses gemini-pencil-animation-image-gen] Reads references/pencil-animation-prompt-templates.md,
uses Template 1 (Character Design from Reference Photo), captures distinguishing features
from the photo, translates them into slightly stylized animation proportions, includes
cream paper texture and production label, runs generate_image.py, saves PNG.
```

**Example 2: Expression sheet**
```
User: "Create an expression sheet for my character with different emotions"
Claude: [Uses gemini-pencil-animation-image-gen] Uses Template 2 (Expression Sheet),
arranges 6-9 facial expressions in a grid on a single animation paper sheet,
maintains identity consistency across all expressions, runs the script.
```

**Example 3: Scene composition**
```
User: "Sketch a scene of two characters working at a coffee shop in that pencil animation style"
Claude: [Uses gemini-pencil-animation-image-gen] Uses Template 5 (Scene Composition Sketch),
places characters in a minimal environment with emphasis on character interaction,
maintains the pencil-on-paper aesthetic throughout, runs the script.
```

## Prerequisites

1. **API Key:** Set `GEMINI_API_KEY` in your `.env` file or as an environment variable
2. **Python packages:** `pip install google-genai`
3. **Script location:** `scripts/generate_image.py` in this skill directory

## How It Works

The skill uses a single Python script that:
1. Reads your `GEMINI_API_KEY` from environment variables (or `.env` file)
2. Sends your prompt to `gemini-3.1-flash-image-preview` (Nano Banana 2) via the `google-genai` SDK
3. Optionally includes reference image(s) for identity locking (e.g., a photo of the person)
4. Decodes the image response and saves it as a PNG

The script is identical to `gemini-pixel-image-gen` — the only difference between skills is the prompt content and templates. The generation pipeline is shared.

## Script Usage

```bash
# Basic — generate and save
python3 scripts/generate_image.py "your prompt here" --output ./sketch.png

# With reference photo for character likeness
python3 scripts/generate_image.py "your prompt here" \
  --output ./character_design.png \
  --aspect-ratio 3:2 \
  --reference ./photo.jpg \
  --env-file .env

# Landscape scene composition
python3 scripts/generate_image.py "your prompt here" \
  --output ./scene.png \
  --aspect-ratio 16:9 \
  --env-file .env
```

### Script Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `prompt` | Yes | — | The image generation prompt (positional) |
| `--output` / `-o` | No | `./generated.png` | Output file path |
| `--aspect-ratio` | No | `1:1` | Aspect ratio (1:1, 16:9, 9:16, 3:2, 4:3, etc.) |
| `--model` | No | `gemini-3.1-flash-image-preview` | Gemini model name (Nano Banana 2) |
| `--env-file` | No | `.env` | Path to .env file containing GEMINI_API_KEY |
| `-r` / `--reference` | No | — | Reference image path(s) for identity locking |

### Recommended Aspect Ratios by Template

| Template | Recommended Ratio | Why |
|----------|-------------------|-----|
| Character Design | `3:4` or `4:5` | Portrait orientation suits a single standing figure |
| Expression Sheet | `1:1` or `4:3` | Grid of faces needs roughly square canvas |
| Pose Study | `16:9` or `3:2` | Multiple full-body poses need horizontal space |
| Turnaround Sheet | `16:9` or `21:9` | 5 views in a horizontal lineup |
| Scene Composition | `16:9` or `3:2` | Landscape framing for environment + characters |
| Character Lineup | `16:9` or `21:9` | Side-by-side comparison needs width |

## Prompt Construction Workflow

### Step 1: Read the Templates
Always read `references/pencil-animation-prompt-templates.md` first. It contains 6 ready-to-use templates:
1. Character Design from Reference Photo
2. Expression Sheet (6-9 emotions)
3. Pose Study / Action Sheet
4. Turnaround Sheet (5 views)
5. Scene Composition Sketch
6. Character Comparison Lineup

It also contains the **Pencil Animation Style Cluster** — a reusable style block that must be included in every prompt to reproduce the target aesthetic.

### Step 2: Apply the 7-Layer Framework
Reference the `image-generator-prompt-science` skill for the 7-Layer Prompt Framework when customizing templates. Key layers for this style:
- **Layer 1 (Task):** State the exact output type (e.g., "Create a character turnaround sheet")
- **Layer 2 (Context):** Warm cream animation paper, production label, hole-punch marks
- **Layer 3 (Style):** The Pencil Animation Style Cluster (always include)
- **Layer 4 (Layout):** Explicit spatial arrangement of elements
- **Layer 5 (Consistency):** Identity consistency across views/expressions
- **Layer 6 (Uniformity):** Same pencil weight, same paper texture throughout
- **Layer 7 (Output + Negatives):** Exclude digital looks, anime, vector lines, saturated colors

### Step 3: Run the Script
```bash
python3 [SKILL_DIR]/scripts/generate_image.py "[PROMPT]" \
  --output [OUTPUT_PATH] \
  --aspect-ratio [RATIO] \
  --reference [PHOTO_PATH]  # optional, for likeness
```

### Step 4: Verify Output
After generation, use the Read tool to view the image. Check:
- Warm cream paper background with visible grain texture
- Graphite gray pencil lines (NOT solid black, NOT ink)
- Visible construction line artifacts beneath the final drawing
- Limited, desaturated flat color fills over the pencil work
- Three hole-punch marks at the bottom edge
- Hand-written production label (e.g., "A-1") in the top-left corner
- Character proportions are slightly stylized (Disney/Pixar pre-production adjacent)

If the image is 80% correct, adjust the prompt rather than starting from scratch — Gemini works well with iterative refinement. See the "Prompt Refinement Tips" section in the templates file.

## Cross-References

- For prompt engineering techniques: See `image-generator-prompt-science` skill
- For the Python script (shared): See `gemini-pixel-image-gen/scripts/generate_image.py`
- For Gemini model capabilities: See `gemini-nanobanana-visual/references/Gemini-3-Pro-Image-Master-Prompt-Guide.md`

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `GEMINI_API_KEY not found` | Missing env variable | Add to `.env` file or export in shell |
| `403 Forbidden` | API key lacks image gen access | Ensure billing is enabled on Google AI account |
| `400 Bad Request` | Prompt blocked by safety filter | Rephrase prompt, remove potentially flagged terms |
| `No image in response` | Model returned text only | Add "Generate an image of..." prefix |
| `command not found: python` | macOS uses python3 | Use `python3` instead of `python` |
| `Image data is only N bytes` | Corrupt output | Check API key, retry with simpler prompt |

## Success Criteria

- [ ] Script runs without errors and saves a PNG file
- [ ] Background is warm cream/off-white (NOT pure white, NOT gray)
- [ ] Lines are warm graphite gray with natural stroke-weight variation (NOT solid black, NOT ink)
- [ ] Visible construction/guide line artifacts beneath the final drawing
- [ ] Cross-hatching present on shaded areas (clothing folds, under chin, shadows)
- [ ] Color is limited, desaturated, and flat — pencil lines visible through color fills
- [ ] Three hole-punch marks visible at the bottom edge of the paper
- [ ] Hand-written production label (e.g., "A-1") in the top-left corner
- [ ] Character proportions are slightly stylized, appealing, clean silhouette
- [ ] Overall feel is "professional animator's sketchbook page" — NOT digital, NOT anime

## Copy/Paste Ready

```
"Draw me as a pencil animation character from this photo"
"Create an expression sheet with different emotions for my character"
"Generate a pose study sheet showing different body positions"
"Make a character turnaround sheet with front, side, and back views"
"Sketch a scene of two characters in a coffee shop in traditional animation pencil style"
"Create a character lineup comparing heights and proportions"
"Draw this person as a Disney-style pencil animation sketch"
```
