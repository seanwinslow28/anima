---
name: gemini-image-gen
description: Universal image generator using Google Gemini's Nano Banana 2 API. Use when generating any image that is NOT pixel art or pencil animation — photorealistic images, illustrations, concept art, UI mockups, infographics, product photos, portraits, landscapes, architectural visualizations, social media graphics, abstract art, food photography, or diagrams. Triggers on "generate image", "create image", "make a picture", "image of", "illustration of", "photo of", "render", "visualize", "design an image", "draw", "concept art", "mockup image", "product shot", "portrait of", "landscape of".
---

# Gemini Universal Image Generator

## Purpose

Generate any type of image by automatically optimizing the user's prompt using the 7-Layer Prompt Framework from the `image-generator-prompt-science` skill and sending it to Gemini's Nano Banana 2 model (`gemini-3.1-flash-image-preview`). This is the general-purpose catch-all for image generation requests that don't fit the `gemini-pixel-image-gen` (pixel art) or `gemini-pencil-animation-image-gen` (pencil animation) specialized skills.

## When to Use

- User asks to generate any image that is NOT pixel art or traditional animation pencil test
- Photorealistic images, portraits, headshots, lifestyle photography
- Illustrations, concept art, digital paintings
- Product photography, food photography, architectural visualization
- UI mockups, wireframe-to-high-fidelity conversions
- Infographics, diagrams, data visualizations with text
- Social media graphics, marketing visuals, ad creatives
- Landscape, environment, or nature scenes
- Character designs (non-pixel-art), creature concepts, vehicle designs
- Abstract art, generative visuals, artistic compositions
- Any "generate an image of..." or "make a picture of..." request
- User provides a rough description and wants it optimized for best results

## Examples

**Example 1: Simple request, optimized through the 7-Layer Framework**
```
User: "Make an image of a sunset over mountains"
Claude: [Uses gemini-image-gen] Analyzes request → applies 7-Layer Framework:
  Layer 1 (Task): "Create a cinematic landscape photograph of a mountain range at sunset"
  Layer 2 (Context): "Golden hour in the Pacific Northwest, for a desktop wallpaper"
  Layer 3 (Style): "Landscape photography (24mm wide-angle, deep focus, Fuji Velvia-like saturation)"
  Layer 4 (Layout): "Rule of thirds, horizon on lower third, mountain peak at right intersection"
  Layer 5 (Consistency): "Physically accurate lighting matching golden hour sun position"
  Layer 6 (Uniformity): "Warm orange-to-purple gradient sky, long shadows from low sun angle"
  Layer 7 (Output): "Ultra-high detail. No HDR halos. No oversaturation."
Runs: python3 scripts/generate_image.py "[optimized prompt]" --output sunset.png --aspect-ratio 16:9
```

**Example 2: Complex multi-element request**
```
User: "Create an infographic comparing the top 5 programming languages by popularity,
       with icons and a clean modern look"
Claude: [Uses gemini-image-gen] Breaks down the request:
  - Type: Infographic with text and icons
  - Style: Clean modern flat design
  - Layout: Vertical flow with 5 sections
  Reads references/universal-prompt-templates.md (Template 4: Infographic).
  Applies 7-Layer Framework with explicit text in quotes, enumerated sections,
  and consistent icon style. Selects 9:16 aspect ratio for vertical format.
Runs: python3 scripts/generate_image.py "[optimized prompt]" --output infographic.png --aspect-ratio 9:16
```

**Example 3: Professional asset with reference image**
```
User: "Create a product photo of this coffee mug for our e-commerce site" [attaches photo]
Claude: [Uses gemini-image-gen] Reads references/nano-banana-2-capabilities.md for
  identity locking technique. Uses Template 2 (Product Photography) with:
  - Reference image loaded via --reference flag
  - "Keep the mug exactly as shown in the reference image"
  - Clean white backdrop, soft overhead lighting, 45-degree hero angle
  - Context: "for an e-commerce product listing" (helps model infer styling)
Runs: python3 scripts/generate_image.py "[optimized prompt]" --output mug_product.png \
  --aspect-ratio 1:1 --reference mug_photo.png
```

## Core Workflow: Prompt Optimization Pipeline

When the user gives an image generation request, follow this 5-step pipeline:

### Step 1: Analyze the Request

Before writing any prompt, determine:
- **Image type:** Photo, illustration, diagram, mockup, concept art, abstract, etc.
- **Style/mood:** Implied or stated? Photorealistic, stylized, minimal, dramatic?
- **Intended use:** Web, print, social media, presentation, portfolio?
- **Explicit details:** What did the user specify clearly?
- **Gaps to fill:** What needs to be inferred or added for a strong result?

### Step 2: Apply the 7-Layer Prompt Framework

Reconstruct the user's request through the framework from the `image-generator-prompt-science` skill. Not every layer applies to every request — use judgment:

| Layer | What It Adds | Skip When... |
|-------|-------------|--------------|
| 1. Task Declaration | Clear action + output type | Never skip |
| 2. Context Foundation | Environment, background, format, purpose | Request is self-contained |
| 3. Style Definition | Visual language with technical specs | User specified exact style |
| 4. Compositional Layout | Spatial organization, explicit ordering | Simple single-subject image |
| 5. Consistency Constraints | Identity, scale, alignment rules | No multi-element consistency needed |
| 6. Technical Uniformity | Lighting, shadows, mood, color | Quick sketch or simple icon |
| 7. Output Specs + Negatives | Quality descriptors + exclusions | Never skip |

Read the `image-generator-prompt-science` skill for the complete framework and fill-in template.
Read `references/universal-prompt-templates.md` for 10 ready-to-use templates matching common image types.

### Step 3: Apply Model-Specific Optimizations

Based on Nano Banana 2's strengths and quirks (see `references/nano-banana-2-capabilities.md`):

- **Natural language, not keywords:** Write full sentences describing the scene
- **Provide context ("the why"):** "for a professional cookbook" beats "food photo"
- **Specific technical details:** Camera lens, lighting setup, materials > vague adjectives
- **Fight the realism bias:** For stylized work, explicitly state the style AND add "Not photorealistic"
- **Text rendering:** Keep text short (<15 words), use quotes, describe font style
- **Identity locking:** When using references, repeat "exactly the same as the reference" 3+ times

### Step 4: Generate

Run the script with the optimized prompt:

```bash
python3 [SKILL_DIR]/scripts/generate_image.py "[OPTIMIZED_PROMPT]" \
  --output [PATH] \
  --aspect-ratio [RATIO] \
  --env-file .env
```

Add `--reference [IMAGE_PATH]` if using reference images for identity locking.

### Step 5: Evaluate and Iterate

After generation, review the output. If it's close but not right:
- **Don't regenerate from scratch.** NB2 excels at conversational editing.
- Describe specific changes: "Make the lighting warmer", "Move the subject left", "Change the sky to overcast"
- Re-run with the adjusted prompt
- Repeat until the result matches the user's intent

## Aspect Ratio Selection Guide

| Use Case | Recommended Ratio | Notes |
|----------|------------------|-------|
| Portrait photos, headshots | `3:4` or `2:3` | Vertical framing for people |
| Landscape, environment | `16:9` or `3:2` | Widescreen for scenic views |
| Social media posts | `1:1` or `4:5` | Square or near-square for feeds |
| Presentations, slides | `16:9` | Standard slide dimensions |
| Phone wallpaper | `9:16` | Full-screen vertical |
| Cinematic, widescreen | `21:9` | Ultra-wide dramatic shots |
| Product photos, e-commerce | `1:1` or `4:3` | Standard catalog format |
| Infographics, tall content | `9:16` or `2:3` | Vertical scrolling format |
| YouTube thumbnails | `16:9` | Standard video thumbnail |
| Character concept art | `3:4` | Portrait orientation for full body |

## Script Usage

```bash
# Basic generation
python3 scripts/generate_image.py "your prompt here" --output ./image.png

# With specific aspect ratio and env file
python3 scripts/generate_image.py "A cinematic landscape..." \
  --output ./landscape.png \
  --aspect-ratio 16:9 \
  --env-file .env

# With reference image for identity locking
python3 scripts/generate_image.py "Portrait of this person in a fantasy setting..." \
  --output ./portrait.png \
  --aspect-ratio 3:4 \
  --reference ./photo.png
```

### Script Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `prompt` | Yes | — | The image generation prompt (positional) |
| `--output` / `-o` | No | `./generated.png` | Output file path |
| `--aspect-ratio` | No | `1:1` | Aspect ratio (1:1, 16:9, 9:16, 3:2, 4:3, etc.) |
| `--model` | No | `gemini-3.1-flash-image-preview` | Gemini model name |
| `--env-file` | No | `.env` | Path to .env file containing GEMINI_API_KEY |
| `-r` / `--reference` | No | — | Reference image path(s) for identity locking |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `GEMINI_API_KEY not found` | Missing env variable | Add to `.env` file or export in shell |
| `403 Forbidden` | API key lacks image gen access | Ensure billing is enabled on Google AI account |
| `400 Bad Request` | Prompt blocked by safety filter | Rephrase prompt, remove potentially flagged terms |
| `No image in response` | Model returned text only | Add "Generate an image of..." prefix to prompt |
| `command not found: python` | macOS uses python3 | Use `python3` instead of `python` |
| `Image data is only N bytes` | Corrupt output | Check API key, retry with simpler prompt |
| `ModuleNotFoundError: google` | SDK not installed | Run `pip install google-genai` |
| Rate limit exceeded | Too many requests | Wait and retry; consider batch timing |

## Cross-References

- **Prompt framework:** `image-generator-prompt-science` skill — the 7-Layer Prompt Framework used in Step 2
- **Model deep-dive:** `references/nano-banana-2-capabilities.md` in this skill — NB2 specs, pricing, API config, limitations
- **Prompt templates:** `references/universal-prompt-templates.md` in this skill — 10 ready-to-use templates
- **Nano Banana Pro reference:** `gemini-nanobanana-visual/references/Gemini-3-Pro-Image-Master-Prompt-Guide.md` — detailed guide for the older Pro model (much still applies)
- **Pixel art generation:** Use `gemini-pixel-image-gen` skill instead for pixel art sprites, tiles, and game assets
- **Pencil animation:** Use `gemini-pencil-animation-image-gen` skill instead for traditional animation pencil test drawings

## Success Criteria

- [ ] User's request was analyzed for type, style, mood, and intended use
- [ ] Prompt was optimized using the 7-Layer Framework (not just passed through raw)
- [ ] Appropriate aspect ratio was selected for the use case
- [ ] Script ran without errors and saved a PNG file
- [ ] Output matches the user's intent (style, content, composition)
- [ ] If close but not perfect, iterative refinement was used instead of full regeneration
- [ ] Model-specific optimizations were applied (natural language, context, specificity)

## Copy/Paste Ready

```
"Generate an image of [subject]"
"Create a professional photo of [subject] for [purpose]"
"Make an illustration of [scene]"
"Design a mockup for [app/product]"
"Render a concept art of [character/environment]"
"Visualize [data/concept] as an infographic"
"Create a product shot of [item]"
```
