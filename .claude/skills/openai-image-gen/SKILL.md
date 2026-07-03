---
name: openai-image-gen
description: Universal image generator using OpenAI's GPT Image 2 API. Use when generating any non-pixel-art image — editorial illustrations with style-reference images, photorealistic photos, portraits, headshots, concept art, UI mockups, infographics, product photography, social-media graphics, landscapes, food shots, architectural renderings. Strongest fit for editorial illustration with a Ralph-Steadman-style reference image attached (Sean's Substack header workflow, validated 2026-05-23). Triggers on "generate image", "create image", "make a picture", "make an image", "image of", "illustration of", "photo of", "portrait of", "render", "visualize", "design an image", "draw a", "concept art", "product shot", "headshot", "Substack header", "post header", "header image".
---

# OpenAI Universal Image Generator

## Purpose

Generate any type of image by optimizing the user's prompt with the 7-Layer Prompt Framework from the `image-generator-prompt-science` skill, then routing it to OpenAI's GPT Image 2 (`gpt-image-2`) via `images.generate` or — when a style-reference image is attached — `images.edit`. This is the preferred engine for editorial illustration and style-transfer workflows where a reference image carries the aesthetic. For pixel art, use `gemini-pixel-image-gen`. For pencil-test animation drawings, use `gemini-pencil-animation-image-gen`.

## When to Use

- User asks to generate any image that is NOT pixel art or traditional animation pencil test
- **Style-reference workflows** where the user attaches an aesthetic anchor (Steadman, Wes Anderson, comic-book ink, etc.) and wants the output to inherit it
- Substack post headers, blog hero images, newsletter banners (16:9 editorial illustration)
- Photorealistic portraits, headshots, lifestyle photography, food photography
- Editorial illustration, concept art, digital painting
- Product shots for e-commerce, UI mockups, infographics with text
- Landscape and environment scenes, architectural visualization
- Social-media graphics, ad creatives, presentation hero images
- User provides a rough description and wants it optimized via the 7-Layer Framework

### When to use this vs `gemini-image-gen`

| Workflow | Pick |
|---|---|
| Editorial illustration with **one** style-reference image | **openai-image-gen** (default) |
| Substack post headers (validated 2026-05-23 — OpenAI beat NB2 on Steadman gonzo) | **openai-image-gen** |
| Photorealistic portraits with reference-image identity locking | **openai-image-gen** |
| High-volume / cost-sensitive batches (≥10 images per pass) | `gemini-image-gen` (NB2 is cheaper at scale) |
| Conversational multi-turn editing — "now make the sky overcast" | `gemini-image-gen` (NB2 excels here) |
| Multi-reference style soup (need 3+ references blended in one call) | `gemini-image-gen` (NB2 handles up to 14 refs cleanly) |
| Pixel art / sprite sheets | `gemini-pixel-image-gen` |
| Pencil-test animation frames | `gemini-pencil-animation-image-gen` |

## Examples

**Example 1: Editorial illustration with style-reference image**
```
User: "Generate the Substack header for the 'Vault Said Nothing' post — Sedaris voice,
       Steadman aesthetic."
Claude: [Uses openai-image-gen] Reads the post .md to extract POST_TITLE + POST_SUBJECT.
  Loads voice-mode → ref-image mapping from the substack image-gen design doc.
  Applies the locked Sedaris v2 voice slots into the universal 7-Layer template.
  Runs:
    python3 scripts/generate_image.py "[optimized prompt with explicit Steadman anchor]" \
      --output vault/.../images/<slug>-header.png \
      --aspect-ratio 16:9 \
      --reference vault/.../references/ref-3.png \
      --quality high
  Routes to images.edit (reference present) with input_fidelity=high.
```

**Example 2: Simple photorealistic generation, no reference**
```
User: "Make a photo of a vintage typewriter on a wood desk, golden-hour window light"
Claude: [Uses openai-image-gen] Applies 7-Layer Framework:
  Layer 1 (Task): "Create a photorealistic still life photograph"
  Layer 3 (Style): "85mm prime lens, shallow depth of field, natural light"
  Layer 6 (Uniformity): "Golden-hour key light through a window, warm tone"
  Layer 7 (Output): "Sharp focus on the keys. No HDR halos."
  Selects 3:2 aspect ratio. Runs images.generate at quality=medium.
```

**Example 3: Infographic with text**
```
User: "Create a vertical infographic comparing 5 LLMs by latency and cost"
Claude: [Uses openai-image-gen] Reads references/universal-prompt-templates.md
  Template 4 (Infographic). Writes the section text in quotes so GPT Image 2
  renders it accurately. Selects 2:3 vertical. Quality=high for text legibility.
  Runs images.generate.
```

## Core Workflow: Prompt Optimization Pipeline

When the user gives an image-generation request, follow this 5-step pipeline:

### Step 1: Analyze the Request

Before writing any prompt, determine:
- **Image type:** Photo, editorial illustration, diagram, mockup, concept art, abstract, infographic
- **Reference image:** Is one provided? What aesthetic does it carry?
- **Voice / style anchor:** Explicit ("Steadman gonzo") or implicit ("Sedaris-domestic" → infer)
- **Intended use:** Substack header, social post, print, presentation, portfolio
- **Explicit details:** What did the user specify clearly?
- **Gaps to fill:** What needs to be inferred for a strong result?

### Step 2: Apply the 7-Layer Prompt Framework

Reconstruct the user's request through the framework from the `image-generator-prompt-science` skill. Not every layer applies to every request — use judgment:

| Layer | What It Adds | Skip When... |
|-------|-------------|--------------|
| 1. Task Declaration | Clear action + output type | Never skip |
| 2. Context Foundation | Environment, purpose, audience | Request is self-contained |
| 3. Style Definition | Visual language + style anchor | User specified exact style |
| 4. Compositional Layout | Spatial organization, framing | Simple single-subject |
| 5. Consistency Constraints | Identity, scale, medium discipline | No multi-element constraint |
| 6. Technical Uniformity | Lighting, palette, mood | Quick sketch / utility icon |
| 7. Output Specs + Negatives | Quality + exclusions | Never skip |

For Substack-header workflows, read `docs/substack-image-generation-design-2026-05-23.md` for the locked voice-mode → slot mapping. The Sedaris v2 slots are LOCKED canonical as of 2026-05-23.

Read `references/universal-prompt-templates.md` for 10 ready-to-use templates per image type.

### Step 3: Apply Model-Specific Optimizations

Based on GPT Image 2's strengths and quirks (see `references/openai-image-capabilities.md`):

- **Auto-prompt-revision is on by default.** GPT Image 2 silently rewrites prompts. Defensive write: state the style anchor explicitly and repeat the load-bearing constraint twice ("In the unmistakable style of Ralph Steadman... Hand-drawn ink and watercolor, NOT digital flat, NOT photorealistic.") so the revised prompt preserves the intent. The revised prompt is returned in the response's `revised_prompt` field — log it for debugging.
- **Style-transfer via reference image** uses the `images.edit` endpoint, NOT `images.generate`. The script auto-routes when `--reference` is set.
- **`input_fidelity=high` on edits** preserves more of the reference's aesthetic — important for style-anchor workflows. **Only supported on `gpt-image-1` / `gpt-image-1.5`** (verified live 2026-05-23 — `gpt-image-2` returns `invalid_input_fidelity_model` if you pass it). The script auto-detects the model and omits the parameter for `gpt-image-2`; style transfer on `gpt-image-2` still works via the edit endpoint, just without the explicit fidelity dial.
- **Quality tiers materially affect text legibility.** Use `high` when the image contains rendered text (handwriting on a notebook, chart labels, headlines). `medium` is fine for general illustration without text.
- **Plain-English negatives** work in the prompt body — there is no separate negative-prompt parameter. Write "NO text in the image. NO watermark. NOT photorealistic." at the end.
- **Steadman-aesthetic safety-filter gotcha (verified live 2026-05-23):** naming "Ralph Steadman" in the prompt OR passing a Steadman-source reference image gets blocked by the API safety filter even with `--moderation low`. Describe the technique (gestural ink, calligraphic flicks, pen-pressure variation, deliberate splatter) instead of naming the artist, and skip `--reference` for Steadman work. For genuine Steadman-reference workflows, fall back to `gemini-image-gen`. Other artist names (Wes Anderson, Saul Steinberg, Maira Kalman, Edward Gorey, etc.) pass through fine. See `references/openai-image-capabilities.md` §9 for the full safety-filter cookbook.

### Step 4: Generate

Run the script with the optimized prompt:

```bash
python3 [SKILL_DIR]/scripts/generate_image.py "[OPTIMIZED_PROMPT]" \
  --output [PATH] \
  --aspect-ratio [RATIO] \
  --env-file .env
```

Add `--reference [IMAGE_PATH]` for style-transfer / identity locking (routes to `images.edit`).
Add `--quality high` when the image carries text or fine detail.

### Step 5: Evaluate and Iterate

After generation, review the output. GPT Image 2's conversational-edit support is weaker than NB2's, so iterate by re-running with a refined prompt rather than chaining. If the result is close but off:
- Tighten the load-bearing constraint (more explicit style anchor, more repetition)
- Adjust the voice slot that owns the failure mode (composition vs palette vs ink density)
- Try `--quality high` if text or fine detail is muddy
- If style drift toward photorealism, add "NOT photorealistic. Hand-drawn medium." three times in the prompt

For Substack workflows, supersede outputs into `*-v1-superseded.png` files rather than overwriting — Sean compares versions across iterations (the established pattern in `vault/.../substack-drafts/images/`).

## Aspect Ratio Selection Guide

The script maps friendly ratios to OpenAI sizes (divisible-by-16 widths/heights, max edge ≤ 3840px):

| Ratio | OpenAI Size | Use Case |
|---|---|---|
| `1:1` | 1024×1024 | E-commerce, Instagram, square thumbnails |
| `3:2` | 1536×1024 | Classic landscape, photo |
| `2:3` | 1024×1536 | Portrait, vertical posters |
| `4:3` | 1408×1056 | Catalog, standard photo |
| `3:4` | 1056×1408 | Portrait, character art |
| `16:9` | 1536×864 | **Substack headers**, YouTube thumbnails, slides |
| `9:16` | 864×1536 | Phone wallpaper, vertical reels |
| `21:9` | 1792×768 | Cinematic ultra-wide |
| `4:5` | 1024×1280 | Social portrait, Instagram-portrait |
| `5:4` | 1280×1024 | Magazine layout |

## Script Usage

```bash
# Basic generation (no reference)
python3 scripts/generate_image.py "your prompt here" --output ./image.png

# Substack 16:9 header with style-reference image
python3 scripts/generate_image.py "Editorial illustration in the style of..." \
  --output ./header.png \
  --aspect-ratio 16:9 \
  --reference ./steadman-ref.png \
  --quality high

# Multiple variants at medium quality
python3 scripts/generate_image.py "Concept art of..." \
  --output ./concept.png \
  --aspect-ratio 3:4 \
  --quality medium \
  --n 4
```

### Script Arguments

| Argument | Required | Default | Description |
|---|---|---|---|
| `prompt` | Yes | — | The image generation prompt (positional) |
| `--output` / `-o` | No | `./generated.png` | Output file path |
| `--aspect-ratio` | No | `1:1` | Friendly ratio mapped to OpenAI size |
| `--model` | No | `gpt-image-2` | OpenAI image model ID |
| `--quality` | No | `medium` | `low` (~$0.006), `medium` (~$0.053), `high` (~$0.211) at 1024×1024 |
| `--n` | No | `1` | Number of variants (1–10) |
| `--env-file` | No | `.env` | Path to .env containing `OPENAI_API_KEY` |
| `-r` / `--reference` | No | — | Reference image(s) — routes to `images.edit` |

When `--reference` is set, the script routes to `images.edit` with `input_fidelity=high` for stronger style preservation. Multiple references (`-r a.png b.png`) are passed as a sequence to the edit endpoint.

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| `OPENAI_API_KEY not found` | Missing env variable | Add to `.env` or `export OPENAI_API_KEY=...` |
| `401 Unauthorized` | Bad / revoked API key | Regenerate at platform.openai.com |
| `400 Bad Request — invalid size` | Size not divisible by 16 or out of range | Use one of the friendly `--aspect-ratio` values |
| `400 — content policy violation` | Prompt blocked by safety filter | Rephrase, remove flagged terms, retry with `moderation=low` |
| `429 Too Many Requests` | Rate limit hit | Wait 30s; lower `--n`; spread batch over time |
| `Reference image not found` | Wrong path | Use absolute path or `ls` to verify |
| `Reference image too large` | >50MB or wrong format | Convert to PNG ≤ 50MB; resize to ≤4096px max edge |
| `No image in response` | API returned text only | Check `revised_prompt` in stderr; rephrase |
| `ModuleNotFoundError: openai` | SDK not installed | `python3 -m pip install openai` |

## Cross-References

- **Prompt framework:** `image-generator-prompt-science` skill — the 7-Layer Prompt Framework used in Step 2 (delegate to it; do not duplicate)
- **Model deep-dive:** `references/openai-image-capabilities.md` — GPT Image 2 specs, sizes, pricing, edit endpoint, prompt-revision behavior, head-to-head vs NB2
- **Prompt templates:** `references/universal-prompt-templates.md` — 10 ready-to-use templates per image type
- **Substack workflow:** `docs/substack-image-generation-design-2026-05-23.md` — voice-mode → reference-image mapping, locked Sedaris v2 slots, Sean Mode initial slots
- **Alt engine:** `gemini-image-gen` — pick this for high-volume batches or conversational multi-turn editing
- **Pixel art:** `gemini-pixel-image-gen` — pick this for pixel art / sprite sheets
- **Pencil animation:** `gemini-pencil-animation-image-gen` — pick this for traditional animation pencil tests

## Success Criteria

- [ ] User's request was analyzed for type, style anchor, reference, and intended use
- [ ] Prompt was optimized via the 7-Layer Framework (not passed through raw)
- [ ] Appropriate `--aspect-ratio` was selected for the use case
- [ ] When a style-reference was provided, the script routed to `images.edit` (not `generate`)
- [ ] `--quality high` was used when the image carries text or fine detail
- [ ] Output PNG was saved at the requested path with non-trivial file size (>50KB typical)
- [ ] Output matches user intent for style, content, composition; if close but off, prompt was tightened rather than blindly regenerated
- [ ] Model-specific optimizations applied (explicit style anchor + repeated load-bearing constraint to survive auto-revision)

## Copy/Paste Ready

```
"Generate an image of [subject]"
"Make a portrait of [subject] for [purpose]"
"Create an editorial illustration of [scene] in the style of [anchor]"
"Render a Substack header for the [post-slug] post"
"Design a mockup of [app/product]"
"Visualize [data/concept] as an infographic"
"Create a product shot of [item] on [surface]"
```
