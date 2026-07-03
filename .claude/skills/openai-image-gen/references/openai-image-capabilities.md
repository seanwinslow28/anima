# GPT Image 2 — Capabilities Reference

> **When to read:** Consult this file when you need OpenAI-specific optimization details — model ID resolution, size/quality selection, the `images.edit` style-transfer endpoint, prompt-revision behavior, cost math, or workarounds for known limitations. For prompt structure and the 7-Layer Framework, see the `image-generator-prompt-science` skill instead.

---

## 1. Model Overview

| Field | Value |
|-------|-------|
| **Model ID** | `gpt-image-2` |
| **Marketing name** | ChatGPT Images 2.0 / GPT Image 2 |
| **Generation** | Third-generation flagship (succeeds `gpt-image-1` Apr 2025 and `gpt-image-1.5` Dec 2025) |
| **Release date** | April 21, 2026 |
| **Status** | GA |
| **Best for** | Editorial illustration, style-transfer via reference images, photorealistic photography with identity locking, in-image text rendering, Substack/blog headers |

### Available image-model IDs as of May 2026

| Model ID | Status | Notes |
|---|---|---|
| `gpt-image-2` | GA, recommended | Current flagship. Best style fidelity + text rendering. |
| `gpt-image-1.5` | GA | Previous flagship (Dec 2025). Still available; slightly cheaper. |
| `gpt-image-1` | **Deprecating 2026-10-23** | First-generation GA (Apr 2025). Migrate off. |
| `gpt-image-1-mini` | GA | Cheapest tier (~$0.005–0.052 per image). Lower fidelity. |
| `dall-e-2` / `dall-e-3` | **REMOVED 2026-05-12** | Removed from API. Do not use. |

### Key differentiators from prior generations

- **Style transfer via reference images** on the `images.edit` endpoint with `input_fidelity=high` — preserves the reference's aesthetic when generating a new scene, not just inpainting
- **In-image text rendering** is state of the art — headlines, chart labels, handwritten notebook text all reliably legible at `quality=high`
- **Arbitrary resolutions** within the divisible-by-16 / aspect-ratio-≤-3:1 constraint envelope, not just three named presets
- **`moderation: "low"`** option relaxes the safety filter for legitimate editorial / artistic work
- **Token-based billing** rather than flat per-image pricing — actual cost scales with quality tier and output resolution

---

## 2. Capabilities Matrix

| Capability | Quality Rating | Notes |
|---|---|---|
| **Editorial illustration with style reference** | Excellent | The standout strength. Steadman, Wes Anderson, comic ink — strong fidelity at `input_fidelity=high`. |
| **Photorealism** | Excellent | On par with leading peers; default bias toward realism (helpful here, fight only for stylized work). |
| **In-image text rendering** | Excellent | State of the art at `quality=high`. Short headlines, chart axes, hand-written notes. |
| **Character / face consistency** | Very Good | Reference-image identity locking via `images.edit` is the recommended path. |
| **Pixel art** | Adequate | Use `gemini-pixel-image-gen` instead — better at strict pixel constraints. |
| **Product photography** | Excellent | Clean studio shots; lifestyle scenes; reflective surfaces. |
| **Landscape / environment** | Excellent | Rich atmospheric textures, natural light. |
| **UI mockups** | Very Good | Works from wireframe references; component-level fidelity. |
| **Concept art** | Excellent | Especially strong with an explicit style anchor in the prompt. |
| **Conversational editing** | Moderate | Weaker than NB2 here — prefer re-running with a refined prompt over multi-turn editing. |
| **Multi-reference style blending** | Moderate | Accepts up to 16 reference files, but blending 3+ aesthetics in one call gives less predictable results than a single anchor + textual style description. |

---

## 3. Technical Specifications

### Image Sizes

GPT Image 2 accepts:

**Named presets** (universally supported):
```
1024x1024   1024x1536   1536x1024
256x256     512x512     1792x1024   1024x1792
auto        (model picks)
```

**Arbitrary custom sizes** on `images.generate`:
- Max edge ≤ 3840 px
- Both width and height divisible by 16
- Aspect ratio between 1:3 and 3:1
- Total pixels between 655,360 and 8,294,400

**Substack header sweet spot:** `1536x864` (16:9 native, divisible by 16, ~1.33 MP — well within range).

### Quality Tiers

| Quality | Use Case |
|---|---|
| `low` | Drafting, exploration, internal review |
| `medium` (default) | General production work, social media, blog images without text |
| `high` | Final output, in-image text, fine detail, hero assets |
| `auto` | Model picks based on prompt complexity |

`hd` and `standard` are accepted (legacy DALL-E 3 aliases) but only meaningful on older models.

### Input Image Constraints (edit endpoint)

| Parameter | Value |
|---|---|
| Max reference images per call | 16 |
| Max file size | 50 MB per file |
| Supported formats | PNG, JPEG, WebP |
| Max edge | 4096 px recommended |

### Output Format

| Parameter | Value |
|---|---|
| Default response | base64-encoded PNG in `data[i].b64_json` |
| Alternative | URL via `response_format="url"` (expires; download promptly) |
| `output_format` | `png` (default), `jpeg`, `webp` |

### Response Schema (relevant fields)

```python
ImagesResponse(
    created=1716480000,
    data=[
        ImagesResponseDataInner(
            b64_json="<base64-png-bytes>",  # if response_format="b64_json" (default)
            url=None,                       # set instead if response_format="url"
            revised_prompt="...",           # auto-revised version of your prompt
        )
    ],
    usage=Usage(
        input_tokens=..., output_tokens=..., total_tokens=...,
    ),
)
```

The `revised_prompt` field is **load-bearing for debugging.** When output drifts from intent, the revision is usually the culprit. Always log it.

---

## 4. API Configuration

### Python SDK (openai >= 2.0)

```python
from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY from env

# Plain text-to-image
response = client.images.generate(
    model="gpt-image-2",
    prompt="Your prompt here",
    size="1536x864",        # custom 16:9 for Substack headers
    quality="high",
    n=1,
)

image_b64 = response.data[0].b64_json
revised = response.data[0].revised_prompt  # log this for debugging
```

### Reference-Image Style Transfer (edit endpoint)

```python
from openai import OpenAI

client = OpenAI()

with open("steadman-reference.png", "rb") as ref:
    response = client.images.edit(
        model="gpt-image-2",
        image=ref,                  # single file; or pass a list of files
        prompt="Editorial illustration in the unmistakable style of Ralph Steadman...",
        size="1536x1024",           # edit endpoint prefers preset sizes
        quality="high",
        input_fidelity="high",      # preserve reference aesthetic
        n=1,
    )
```

The `input_fidelity="high"` parameter is the crucial one for style-anchor workflows. Without it, the model treats the reference as a loose suggestion; with it, the reference's medium, palette, and gestural quality survive the generation.

### Key Configuration Parameters

| Parameter | Values | Default | Notes |
|---|---|---|---|
| `model` | `"gpt-image-2"` | — | Required for current flagship |
| `prompt` | str | — | Required. Auto-revised — see §5. |
| `size` | str / preset | `"auto"` | See size table above |
| `quality` | `low` / `medium` / `high` / `auto` | `auto` | Affects text legibility and detail |
| `n` | 1–10 | 1 | Number of variants |
| `response_format` | `b64_json` / `url` | `b64_json` | Prefer b64 for local save |
| `output_format` | `png` / `jpeg` / `webp` | `png` | PNG default |
| `moderation` | `auto` / `low` | `auto` | `low` relaxes filter for editorial work |
| `background` | `transparent` / `opaque` / `auto` | `auto` | `transparent` for assets needing chroma |
| `input_fidelity` (edit) | `high` / `low` | `low` | Available on `gpt-image-1` / `gpt-image-1.5` only — `gpt-image-2` rejects it (verified live 2026-05-23). The script auto-omits it for `gpt-image-2`. |

### Authentication

Standard bearer token: `Authorization: Bearer $OPENAI_API_KEY`. The Python SDK reads `OPENAI_API_KEY` from environment automatically; the wrapper script also loads from a `.env` file.

---

## 5. Prompting Best Practices (Model-Specific)

### The auto-prompt-revision problem

GPT Image 2 silently rewrites your prompt before generation — there is no flag to disable this. The revised prompt is returned in `response.data[i].revised_prompt`. Most failures of "I asked for Steadman gonzo and got polished magazine illustration" are revisions softening your style anchor.

**Defensive writing patterns that survive revision:**

1. **Front-load the load-bearing style anchor** in Layer 3, with explicit modifier words:
   ```
   In the unmistakable style of Ralph Steadman — gestural india-ink linework with visible
   pen-pressure variation, calligraphic flicks, deliberate ink splatters and drips.
   ```
2. **Repeat the load-bearing constraint twice** at different points in the prompt — once in Layer 3, once in Layer 7 negatives:
   ```
   Layer 3: "Hand-drawn ink and watercolor medium."
   Layer 7: "NOT digital flat. NOT photorealistic. NOT polished magazine illustration."
   ```
3. **Use explicit medium terms** (ink, watercolor, oil, pencil, vector, 3D render) — the revision preserves these better than vague descriptors ("artistic," "stylized")
4. **Log `revised_prompt`** on every run during prompt development to see what the model actually generated against

### Reference-image identity locking

When using a reference image via `images.edit`:
- Use `input_fidelity="high"` — non-negotiable for style-transfer workflows
- One reference image > three blended references for style fidelity (multi-ref gives "style soup")
- Phrase the prompt as *"in the unmistakable style of"* + describe what the reference carries (medium, line quality, palette)
- Include explicit subject content the reference does NOT show, so the model knows what to draw on top of the inherited style

### In-image text rendering

GPT Image 2 is state of the art at text, but rules still apply:
- Wrap exact text in quotes: `'The sign reads "OPEN 24 HOURS"'`
- Specify position: `"Title centered at top, subtitle below in smaller italic"`
- Use `quality="high"` for any image carrying text
- Keep headlines under 15 words; multi-line text works but accuracy drops with length

### Negative constraints

There is no separate negative-prompt parameter. Write plain-English negatives in the Layer 7 block:
```
NO text in the image. NO watermark. NO signature. NOT photorealistic.
Negative space is a feature, not a bug.
```

The model treats these as hard constraints when stated clearly.

### Aspect ratios on the edit endpoint

The `images.edit` endpoint historically preferred preset sizes (`1024x1024`, `1536x1024`, `1024x1536`). Custom sizes accept on `images.generate` but may be more strictly validated on edit. If a custom size errors, fall back to `1536x1024` for landscape or `1024x1536` for portrait.

---

## 6. Style-Specific Tips

### Editorial illustration (Substack headers — Sean's primary use case)
- Reference image is non-negotiable for style-anchor work. One Steadman PNG > a thousand adjectives.
- Layer 3 lead: *"In the unmistakable style of [ARTIST], dialed down to a [register] register"*
- Negatives: "NOT polished magazine illustration. NOT digital flat. Hand-drawn at speed."
- Quality: `high` (text in scene is common — handwritten notebooks, hand-painted chart labels)
- Aspect: `--aspect-ratio 16:9` → 1536×864

### Photorealistic
- Specify camera: `85mm portrait lens, f/2.0`, `35mm wide`
- Lighting setup: three-point, Rembrandt, butterfly, golden hour
- Material texture: `"matte skin with natural pores"`, `"brushed stainless with subtle fingerprints"`
- GPT Image 2's default — minimal style overrides needed

### Concept art
- Style anchor is critical — name the artist or franchise lineage
- Aspect: `3:4` for character, `16:9` for environment
- Quality: `high` (rich detail expected)

### Infographic / diagram
- Section text in quotes, position specified
- Layout: `"Three columns, header at top, data middle, legend bottom"`
- Quality: `high` (text legibility is the whole point)
- Aspect: `2:3` vertical for scroll-feed, `16:9` for slide deck

### Product photography
- Background described: `"white seamless"`, `"marble"`, `"lifestyle kitchen counter"`
- Lighting: `"soft overhead diffused with fill card on the left"`
- Aspect: `1:1` for e-commerce, `4:3` for catalog

### Architecture / interior
- Style: `"Modern minimalist"`, `"Industrial loft"`, `"Mid-century modern"`
- Materials: `"warm oak flooring, off-white walls, brass fixtures"`
- Lighting: `"natural light from floor-to-ceiling windows, late afternoon"`

---

## 7. Known Limitations & Workarounds

| Limitation | Description | Workaround |
|---|---|---|
| **Silent prompt revision** | Auto-rewrite degrades style anchors | Log `revised_prompt`; repeat load-bearing constraint twice; use explicit medium terms |
| **Weaker conversational editing** | Multi-turn refinement is less predictable than NB2 | Re-run with refined prompt rather than chaining edits |
| **Edit endpoint size strictness** | Custom WxH may error on edit calls | Fall back to `1536x1024` / `1024x1536` presets |
| **Realism pull** | Default bias toward photorealism | Explicit non-realistic medium + triple negative ("NOT photorealistic" × 3) |
| **Multi-reference style soup** | 3+ references blended give noisy results | One reference + textual style description |
| **Safety filter false positives** | Some editorial prompts blocked | Rephrase; try `moderation="low"` for legitimate work |
| **Cost cliff at `high`** | `high` quality is ~40× the price of `low` (~$0.211 vs $0.006 at 1024×1024) | Use `medium` for iteration, `high` only for final output |
| **No free tier** | Paid API key required | Use `low` quality for exploration (~$0.006/image) |

---

## 8. Cost Optimization

### Pricing as of May 2026 (1024×1024)

| Quality | Cost per image | Use |
|---|---|---|
| `low` | ~$0.006 | Drafting / exploration |
| `medium` | ~$0.053 | General production |
| `high` | ~$0.211 | Final output, in-image text |

Underlying token pricing: $8/M image input tokens, $30/M image output tokens, $5/M text input tokens. Per-image numbers above are calculator-derived; actual billing is token-based and varies with prompt length and output resolution.

A 50% Batch discount is available for asynchronous jobs.

### Strategies

| Strategy | How | Savings |
|---|---|---|
| Iterate at `medium`, finalize at `high` | First passes at `quality=medium`, only re-run at `high` once composition is locked | ~75% vs all-high |
| Right-size resolution | Substack auto-resizes — generate at 1536×864 (not 2048×1152) unless print-bound | ~30% |
| Batch discount | Use async batch API for non-realtime jobs | 50% |
| Single-reference > multi-reference | One ref + text description is cheaper than 4-ref blend AND more predictable | Implicit (avoids rework) |

### Per-Substack-post budget (Sean's workflow)

Assuming 1–2 iterations to land final at `quality=high`, 16:9 (1536×864):
- 1 iteration at high: ~$0.18
- 2 iterations (1 medium draft + 1 high final): ~$0.23
- Sean's per-post budget recommendation: ~$0.25 / header

### GPT Image 2 vs Nano Banana 2 — when to choose which

| Decision factor | Pick GPT Image 2 | Pick NB2 |
|---|---|---|
| One style-reference image, editorial illustration | ✅ | |
| Substack post headers (Sean's validated 2026-05-23) | ✅ | |
| In-image text rendering at high fidelity | ✅ | |
| Photorealistic portrait with identity reference | ✅ | |
| Conversational multi-turn editing | | ✅ |
| Batch ≥10 images, cost-sensitive | | ✅ (cheaper per-image) |
| Multi-reference style blending (3+ anchors) | | ✅ (up to 14 cleanly) |
| Pixel art | | (use `gemini-pixel-image-gen`) |
| Image Search Grounding (real-world references) | | ✅ |
| Fastest single-image latency | ~tied | ✅ (4–6s at 1K) |

**Sean's default routing rule (set 2026-05-23):** editorial illustration with one style-reference image → GPT Image 2. Everything else, evaluate per-job.

---

## 9. Rate Limits & Safety

### Rate limits

OpenAI does not publish a single canonical rate limit for image endpoints; limits scale with account tier and historical usage. Practical observation:
- Tier 1 accounts: ~5 images/minute on `gpt-image-2`
- Tier 2+: ~20 images/minute
- Hitting `429 Too Many Requests` — wait 30s and retry; lower `--n`

### Safety filter

All prompts and outputs are filtered. Failure surfaces as `400 Bad Request` with `code: "moderation_blocked"` and the message *"Your request was rejected by the safety system."*

`moderation` parameter:
- `auto` (default): standard filter
- `low`: relaxed filter for legitimate editorial / artistic work

**Verified live 2026-05-23:** the API safety filter is materially stricter than the ChatGPT consumer UI. Three reproducible triggers observed against legitimate editorial-illustration work:

1. **Naming "Ralph Steadman"** in the prompt → reliably blocked (even with `moderation=low`). The same prompt with the artist's name removed and the style described technique-by-technique (gestural ink, calligraphic flicks, pen-pressure variation, splatter) sails through. The gonzo-aesthetic association with substance-related imagery is the suspected trigger.
2. **Steadman-style reference images** uploaded to `images.edit` → blocked even with `moderation=low`. Reference images whose own content trips the visual safety filter (intense expressions, drips, dripping color, characters from morally-coded TV) reject the entire call.
3. The Python SDK's `images.edit()` does NOT expose `moderation` as a kwarg in version 2.38.0 (it's documented for the API but missing from the SDK signature). The script passes it via `extra_body={"moderation": "low"}` to push it through. Even then, it does not unblock the above two triggers.

**Pragmatic guidance for Steadman-aesthetic / gonzo workflows:**
- Describe the technique, not the artist. *"Gestural india-ink linework with visible pen-pressure variation, calligraphic flicks, and deliberate ink splatters"* outperforms *"in the style of Ralph Steadman"* across the API.
- Do NOT pass Steadman-source reference images through `images.edit`. Use textual style description on `images.generate` instead.
- For workflows that genuinely need a Steadman reference image, fall back to `gemini-image-gen` — Nano Banana 2's safety filter is less aggressive on artist-name + intense-imagery combinations.
- For most other style anchors (Wes Anderson, Saul Steinberg, Maira Kalman, Edward Gorey, James Turrell, Hokusai etc.) the artist's name passes through fine. The Steadman / Hunter-S-Thompson lineage is the specific exception.

---

*Last verified: 2026-05-23 via OpenAI developer docs (developers.openai.com) and openai Python SDK 2.38.0 introspection.*
