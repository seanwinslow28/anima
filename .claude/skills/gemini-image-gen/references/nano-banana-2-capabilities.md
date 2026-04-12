# Nano Banana 2 (Gemini 3.1 Flash Image Preview) — Capabilities Reference

> **When to read:** Consult this file when you need model-specific optimization details for image generation — resolution selection, API configuration, speed/cost trade-offs, or workarounds for known limitations. For prompt structure and layering, see the `image-generator-prompt-science` skill instead.

---

## 1. Model Overview

| Field | Value |
|-------|-------|
| **Model ID** | `gemini-3.1-flash-image-preview` |
| **Nickname** | Nano Banana 2 (NB2) |
| **Internal Codename** | GEMPIX2 |
| **Base Architecture** | Gemini 3.1 Flash |
| **Release Date** | February 26, 2026 |
| **Status** | Public Preview |
| **Best For** | High-volume image generation, fast iteration, cost-effective production pipelines |

### Key Differentiators from Other Models

- **Speed-first design:** 3–5x faster than Nano Banana Pro while reaching ~95% of its image quality
- **Image Search Grounding:** Retrieves real-world reference images via Google Search during generation — dramatically improves accuracy for landmarks, logos, and well-known subjects
- **Thinking Mode:** Three levels (Minimal, High, Dynamic) to tune speed-quality balance per request
- **0.5K resolution tier:** Low-cost option not available on Pro
- **Natural language understanding:** Conversational prompts work well without keyword formatting

### Nano Banana 2 vs Nano Banana Pro

| Feature | Nano Banana 2 (Flash) | Nano Banana Pro |
|---------|----------------------|-----------------|
| Base Model | Gemini 3.1 Flash | Gemini 3 Pro |
| Model ID | `gemini-3.1-flash-image-preview` | `gemini-3-pro-image-preview` |
| Speed (1K) | 4–6 seconds | 10–20 seconds |
| Speed (4K) | 15–30 seconds | 30–60 seconds |
| Max Resolution | 4096px (4K) | 4096px (4K) |
| Quality | ~95% of Pro | Reference standard |
| Thinking Mode | Yes (3 levels: Minimal, High, Dynamic) | Yes (mandatory) |
| Image Search Grounding | Yes | Yes |
| System Prompts | Yes | Yes |
| Reference Images | Up to 14 | Up to 14 |
| Text Rendering | Very good | State-of-the-art |
| Cost (1K image) | ~$0.045 | ~$0.05 |
| Cost (2K image) | ~$0.10 | ~$0.134 |
| Cost (4K image) | ~$0.15 | ~$0.134+ |
| Input token price | 8x cheaper than Pro | 8x more expensive |
| 0.5K tier | Yes | No |
| Free tier | No | No |

**When to choose NB2:** Fast iteration, high-volume pipelines, cost-sensitive production, day-to-day creative work, rapid prototyping.
**When to choose Pro:** Premium visual quality, complex reasoning about composition, fine art, high-end editorial work.

---

## 2. Capabilities Matrix

| Capability | Quality Rating | Notes |
|-----------|---------------|-------|
| **Photorealism** | Excellent | Near-Pro quality; default bias toward realism |
| **Illustration / Stylized** | Very Good | Must explicitly specify style to avoid realism pull |
| **Text Rendering** | Very Good | Legible, stylistically consistent; short text most reliable |
| **Character Consistency** | Very Good | Up to 5 humans, 14 objects with identity locking |
| **Pixel Art** | Good | Needs explicit constraints (no anti-aliasing, no gradients) |
| **Diagrams / Infographics** | Very Good | Strong at structured layouts with labels |
| **Product Photography** | Excellent | Clean studio shots, contextual mockups |
| **Landscape / Environment** | Excellent | Rich textures, natural lighting |
| **UI Mockups** | Good | Works well from wireframe references |
| **Concept Art** | Very Good | Better with explicit style anchors |
| **Architecture Viz** | Very Good | Supports 2D-to-3D translation from floor plans |
| **Conversational Editing** | Excellent | Edit, don't re-roll — iterative refinement is a core strength |
| **Image Search Grounding** | Good | Real-world references for landmarks, logos, known subjects |
| **Multi-turn Workflows** | Excellent | Build on previous outputs without regenerating from scratch |

---

## 3. Technical Specifications

### Token Limits

| Parameter | Value |
|-----------|-------|
| Max input tokens | 1,000,000 (1M context window) |
| Max output tokens | 64,000 |
| Max images per prompt | 14 |

### Image Constraints

| Parameter | Value |
|-----------|-------|
| Max inline upload | 7 MB per file |
| Max Cloud Storage upload | 30 MB per file |
| Supported input formats | PNG, JPEG, WebP, HEIC, HEIF |
| Output format | PNG |
| SynthID watermark | Always present (imperceptible, cannot be removed) |

### Supported Aspect Ratios

```
1:1   |  1:4   |  1:8   |  2:3   |  3:2
3:4   |  4:1   |  4:3   |  4:5   |  5:4
8:1   |  9:16  |  16:9  |  21:9
```

### Resolution Options & Pricing

| Resolution | Pixel Dimensions | Approx. Output Tokens | Cost per Image |
|-----------|-----------------|----------------------|----------------|
| 0.5K | 512x512 | ~747 | ~$0.045 |
| 1K (default) | 1024x1024 | ~1,120 | ~$0.067 |
| 2K | 2048x2048 | ~1,680 | ~$0.101 |
| 4K | 4096x4096 | ~2,520 | ~$0.151 |

> **Note:** Resolution must be specified in UPPERCASE: `"1K"`, `"2K"`, `"4K"`. Lowercase is ignored.

### Generation Speed

| Resolution | Time |
|-----------|------|
| 0.5K | 2–4 seconds |
| 1K | 4–6 seconds |
| 2K | 8–15 seconds |
| 4K | 15–30 seconds |

---

## 4. API Configuration

### Python SDK (google-genai)

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_KEY")

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=["Your prompt here"],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],       # Use ["TEXT", "IMAGE"] for mixed output
        image_config=types.ImageConfig(
            aspect_ratio="16:9",             # See supported ratios above
            # image_size="2K",               # Optional: "1K", "2K", "4K"
        ),
    ),
)
```

### Key Configuration Parameters

| Parameter | Values | Default | Notes |
|-----------|--------|---------|-------|
| `response_modalities` | `["IMAGE"]` or `["TEXT", "IMAGE"]` | Text only | **Required** for image generation |
| `aspect_ratio` | See list above | `"1:1"` | Set in `image_config` |
| `image_size` | `"1K"`, `"2K"`, `"4K"` | `"1K"` | Uppercase required |
| `temperature` | 0.0–2.0 | 1.0 | Higher = more creative |
| `topP` | 0.0–1.0 | 0.95 | Nucleus sampling |

### Reference Image Input (Identity Locking)

```python
from google.genai import types

# Load reference image
with open("reference.png", "rb") as f:
    img_bytes = f.read()

contents = [
    types.Part.from_bytes(data=img_bytes, mime_type="image/png"),
    "Create a portrait of this person in a fantasy setting, keeping facial features exactly the same."
]

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=contents,
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(aspect_ratio="3:4"),
    ),
)
```

---

## 5. Prompting Best Practices (Model-Specific)

### Golden Rules for NB2

1. **Natural language over keywords.** NB2 understands full sentences better than comma-separated tags.
   ```
   Bad:  "sunset, mountains, dramatic, cinematic, 8k, golden hour"
   Good: "A cinematic wide shot of snow-capped mountains at sunset, with golden hour
         light painting the peaks warm orange against a deep purple sky."
   ```

2. **Provide context ("the why").** Context helps NB2 make better artistic decisions.
   ```
   Good: "A close-up photo of a gourmet burger for a high-end restaurant menu"
   → Model infers: professional food styling, shallow depth of field, warm lighting
   ```

3. **Be specific with technical details.** Lenses, lighting setups, and materials beat vague adjectives.
   ```
   Bad:  "good lighting"        Good: "three-point softbox setup with golden hour backlight"
   Bad:  "shiny material"       Good: "brushed stainless steel with subtle fingerprint smudges"
   ```

4. **Edit, don't re-roll.** If an image is 80% right, request specific changes rather than regenerating. NB2 excels at conversational editing.

5. **Use negative constraints in plain English.** More effective than separate negative prompt fields.
   ```
   "No blur, no noise, no watermarks. Not cartoonish. Full figure visible."
   ```

6. **Repeat key requirements.** Saying "consistent" 4–5 times across different parts of the prompt reinforces identity/style preservation.

7. **Anchor to known references.** Use well-known visual styles the model has been trained on.
   ```
   "In the style of a Wes Anderson film — symmetrical composition, pastel palette"
   "Studio Ghibli-inspired watercolor landscape with soft edges and warm tones"
   ```

### Fighting the Realism Bias

NB2 has a natural pull toward photorealism. For stylized outputs:
- Be extremely explicit: `"stylized cel-shaded illustration, NOT photorealistic"`
- Upload a style reference image
- Include negative constraints: `"not hyperrealistic, not photographic"`
- Describe the rendering technique: `"flat vector illustration with clean line work and solid color fills"`

### Text Rendering Tips

- Keep text short (under 15 words) for best accuracy
- Use quotes around exact text: `'The sign reads "OPEN 24 HOURS"'`
- Describe font characteristics rather than naming fonts: `"bold sans-serif in all caps"`
- For multi-line text, specify layout: `"Title centered at top, subtitle below in smaller italic"`

---

## 6. Style-Specific Tips

### Photorealistic
- Specify camera: lens (85mm portrait, 24mm wide), aperture (f/1.4 for bokeh)
- Describe lighting setup: three-point, Rembrandt, butterfly, golden hour
- Add material textures: "matte skin with natural pores", "glossy ceramic with reflections"
- NB2's default strength — minimal style overrides needed

### Illustration / Digital Art
- Always specify rendering approach: "digital illustration", "watercolor", "vector art"
- Include a style anchor: artist, era, or well-known aesthetic
- Add "Not photorealistic" to prevent realism drift
- Describe line treatment: "clean 2px outlines", "sketchy pencil lines", "no outlines"

### Pixel Art
- Explicit constraints critical: "No anti-aliasing. No gradients. No sub-pixel rendering."
- Specify exact dimensions: "32x32 pixels per sprite"
- Use hot pink (#FF00FF) background for chroma keying
- Specify palette: "strict 4-color palette using only: [hex values]"
- Always specify perspective: "top-down orthogonal, NOT isometric"

### Diagrams & Infographics
- Structure layout explicitly: "Three columns, header at top, data in middle, legend at bottom"
- Put text content in quotes
- Specify visual style: "clean modern infographic", "hand-drawn whiteboard", "technical blueprint"
- Request legible text: "All text must be sharp and readable at final resolution"

### Product Photography
- Describe surface/background: "white seamless backdrop", "marble tabletop", "lifestyle setting"
- Specify lighting: "soft diffused overhead lighting with a fill card on the left"
- Include context: "for an e-commerce listing" or "for a luxury brand campaign"

### Portraits
- Identity locking: "Keep facial features exactly the same as the reference image"
- Specify framing: "headshot", "bust shot", "three-quarter body"
- Lighting matters most: "Rembrandt lighting with soft fill"

### Architecture / Interior Design
- NB2 can do 2D-to-3D translation from floor plans
- Specify style: "Modern minimalist", "Industrial loft", "Mid-century modern"
- Describe materials: "warm oak flooring, off-white walls, brass fixtures"
- Include lighting: "natural light from floor-to-ceiling windows, late afternoon"

---

## 7. Known Limitations & Workarounds

| Limitation | Description | Workaround |
|-----------|-------------|------------|
| **Realism Bias** | Default pull toward photorealistic output | Explicitly specify non-realistic style + negative constraints |
| **Small Faces** | Struggles with detailed facial features at small scale | Use close-up framing or generate at 4K and crop |
| **Fine Text (long)** | Accuracy drops with text over ~15 words | Keep text short; generate text separately if needed |
| **Transparency** | Cannot generate true PNG transparency | Use hot pink (#FF00FF) chroma key background for later removal |
| **Fine Details** | Very intricate details may be simplified | Generate at 4K resolution and crop to region of interest |
| **Safety Filters** | May block some prompts unexpectedly | Rephrase; avoid potentially flagged terms; keep it professional |
| **No Free Tier** | Paid API key required from day one | Use 0.5K resolution for exploration (~$0.045/image) |
| **Character Substitution** | May use canonical character versions over references | Emphasize "exactly as shown in reference image" repeatedly |
| **SynthID Watermark** | All outputs include imperceptible watermark | Cannot be removed; required by Google ToS |
| **Rate Limits** | More restrictive for preview models | Plan for rate limiting in batch workflows |

---

## 8. Cost Optimization

### Strategies

| Strategy | How | Savings |
|----------|-----|---------|
| Use 0.5K for exploration | `image_size="0.5K"` during iteration | 33% vs 1K |
| Grid trick | Request 4x4 grid at 2K = 16 images for ~$0.10 | ~$0.006/image |
| Edit, don't regenerate | Conversational follow-ups | 50%+ (avoids full regen) |
| Right-size resolution | Only use 4K for final production assets | 55% vs 4K for everything |
| Batch similar requests | Group style-consistent assets in one session | Amortize thinking overhead |

### Resolution Selection Guide

| Use Case | Recommended Resolution |
|----------|----------------------|
| Quick prototyping / exploration | 0.5K |
| Web assets, social media | 1K |
| Print-ready, high-DPI screens | 2K |
| Large format print, wallpapers | 4K |
| Sprite sheets, pixel art | 1K (then scale in post) |

---

*Last Updated: April 2026*
*Sources: Google AI documentation, Google DeepMind, community benchmarks, Nano Banana 2 API guides*
