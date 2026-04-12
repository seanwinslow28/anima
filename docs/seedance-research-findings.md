# Seedance 2.0 — Research Findings

> Research conducted 2026-04-12. Sources: fal.ai docs, ByteDance official, community benchmarks, practitioner guides, Reddit/X threads.

---

## Model Overview

Seedance 2.0 is ByteDance's multimodal video generation model (released Feb 2026, fal.ai API live April 9, 2026). Unified audio-video architecture. Scored 8.2/10 in independent benchmarks (Lanta AI Research) — ahead of Veo 3 (7.0) and Kling 2.1 (4.4). 9/10 for camera control.

---

## Capabilities Summary

| Capability | Spec |
|-----------|------|
| **Generation modes** | Text-to-video, Image-to-video (start frame only OR start+end frame), Reference-to-video (up to 9 images + 3 videos + 3 audio) |
| **Resolution** | 480p, 720p (no 1080p native) |
| **Duration** | 4–15 seconds per generation |
| **Frame rate** | 24fps |
| **Aspect ratios** | 21:9, 16:9, 4:3, 1:1, 3:4, 9:16, auto |
| **Audio** | Native synchronized audio generation (lip-sync, SFX, ambient) — included at no extra cost |
| **Start+End frame** | YES — interpolation mode. Generates "plausible path between two known states" |
| **End frame accuracy** | Approximate, not pixel-exact. Treat as directional guide |
| **Negative prompts** | NOT supported on fal.ai. Style control is prompt-only via positive descriptors |

### Start+End Frame Interpolation — How It Works

When both `image_url` (start) and `end_image_url` (end) are provided, the model encodes both into latent space, computes the difference, and distributes change across frames via diffusion. This produces more constrained, coherent motion than single-frame extrapolation.

**Limitations:**
- Final generated frame won't match end reference exactly
- Consistency decreases over longer durations (keep clips 4–6 seconds)
- Start and end frames should have matching lighting/style
- Output inherits aspect ratio from the first frame (aspect_ratio param ignored in this mode)

---

## Fal.ai API

### Model IDs

| Mode | Standard | Fast |
|------|----------|------|
| Text-to-Video | `bytedance/seedance-2.0/text-to-video` | `bytedance/seedance-2.0/fast/text-to-video` |
| Image-to-Video | `bytedance/seedance-2.0/image-to-video` | `bytedance/seedance-2.0/fast/image-to-video` |
| Reference-to-Video | `bytedance/seedance-2.0/reference-to-video` | `bytedance/seedance-2.0/fast/reference-to-video` |

### Authentication

```bash
export FAL_KEY="your-key-here"  # Add to .env
pip install fal-client
```

### Image-to-Video Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | YES | — | Motion/action description |
| `image_url` | string | YES | — | Start frame URL |
| `end_image_url` | string | no | — | End frame URL (enables interpolation) |
| `resolution` | string | no | `"720p"` | `"480p"` or `"720p"` |
| `duration` | string | no | `"auto"` | `"4"` through `"15"` or `"auto"` |
| `aspect_ratio` | string | no | `"auto"` | Ignored when start frame provided |
| `generate_audio` | boolean | no | `true` | Generate synchronized audio |
| `seed` | integer | no | — | For reproducibility |

### Pricing (per second of generated video)

| Tier | 720p | 480p (est.) |
|------|------|-------------|
| Standard | $0.30/s | ~$0.08–0.10/s |
| Fast | $0.24/s | ~$0.07/s |

**Cost per generation (720p, 16:9):**

| Duration | Standard | Fast |
|----------|----------|------|
| 4 seconds | ~$1.21 | ~$0.97 |
| 5 seconds | ~$1.52 | ~$1.21 |
| 10 seconds | ~$3.03 | ~$2.42 |

**Generation time:** 60–180 seconds via fal.ai API.

### Python Code — Start+End Frame Interpolation

```python
import fal_client
import os

os.environ["FAL_KEY"] = os.getenv("FAL_KEY")

result = fal_client.subscribe(
    "bytedance/seedance-2.0/image-to-video",
    arguments={
        "prompt": "Character smoothly raises right arm from side to shoulder height, pencil lines on cream paper.",
        "image_url": "https://your-bucket.com/keyframe_start.png",
        "end_image_url": "https://your-bucket.com/keyframe_end.png",
        "resolution": "720p",
        "duration": "5",
        "generate_audio": False,
        "seed": 42,
    },
)

video_url = result["video"]["url"]
print(f"Video: {video_url}")
print(f"Seed: {result['seed']}")
```

### Batch/Queue Pattern

```python
# Submit without waiting
handler = fal_client.submit(
    "bytedance/seedance-2.0/image-to-video",
    arguments={...},
)
request_id = handler.request_id

# Poll later
status = fal_client.status("bytedance/seedance-2.0/image-to-video", request_id)
result = fal_client.result("bytedance/seedance-2.0/image-to-video", request_id)
```

### Other API Providers

| Platform | Status | Notes |
|----------|--------|-------|
| Fal.ai | Live (April 9, 2026) | Primary, all modes, standard+fast |
| Replicate | Available | `bytedance/seedance-2.0` |
| Segmind | Fast tier only | `seedance-2.0-fast` |
| Dreamina | Official ByteDance UI | $9.60/mo, Fast tier much cheaper ($0.022/s) |

---

## Prompting Best Practices

### The Formula

**Subject → Action → Environment → Camera → Style → Constraints**

60–100 words. Every word should serve a purpose — cut filler adjectives.

### For Image-to-Video (Our Primary Mode)

Critical rules:
1. **DO NOT re-describe the subject's appearance** — the start/end frames already provide that
2. **Focus entirely on movement and action** — what changes between the frames
3. **Include "preserve composition and colors"** to maintain visual consistency
4. **Specify motion intensity explicitly** — the model can't infer degree from reference images alone
5. **ONE camera instruction only** — multiple movements produce jitter
6. **Add lighting description** — "biggest impact on video quality among all prompt elements"

### Style Preservation Keywords

**Use:**
- "Hand-drawn pencil animation on cream paper"
- "Traditional 2D animation, visible pencil strokes"
- "Graphite pencil lines, paper grain texture"
- "Monochrome sketch animation"
- "Consistent line weight, visible construction marks"
- "Preserve hand-drawn quality throughout"

**Avoid:**
- "Cinematic" (pulls toward polish)
- "4K", "photorealistic", "high detail" (pull toward digital)
- "Glow", "glimmer", "glints" (trigger sparkle artifacts)
- "Fast" without qualification (causes chaos)
- "Epic" (too vague)

### Prompt Template for Our Pipeline

```
@Image1 as the first frame. @Image2 as the last frame.
Hand-drawn pencil animation on cream paper. The character [SPECIFIC MOTION].
Fixed camera, locked tripod. Even, diffuse lighting.
Maintain pencil line quality, paper texture, and graphite shading throughout.
Consistent line weight, visible construction marks.
No photorealistic rendering, no digital effects.
Smooth interpolation, [DURATION] seconds.
```

---

## Character Consistency

### What Works
- **2–3 reference images max** — one source reduced drift by ~60% going from 6 to 2 references
- **3-Angle Rule:** front, profile, three-quarter view collage
- **Immutable character block:** write once, reuse verbatim in every prompt
- **Start+end frame mode** is the strongest consistency tool — interpolation inherits identity from both anchors

### Identity Drift Patterns
1. **Feature erosion** — accessories (stylus!) disappear first
2. **Pose flip** — hand dominance switches left/right (critical for our stylus-in-right-hand rule)
3. **Stylization shift** — line weight, proportions change mid-clip
4. **Identity blend** — features average between multiple references

### Mitigation
- Include explicit negatives in character block: "stylus always in RIGHT hand, no mirrored features"
- Keep motion prompts minimal for identity-critical shots
- Shorter clips (4–6s) hold identity better than 10–15s
- Manually verify stylus hand in every extracted frame

---

## Known Failure Modes

| Issue | Cause | Mitigation |
|-------|-------|-----------|
| Hand/finger artifacts | Thin structures, fast finger actions | Keep hands larger in frame, avoid intricate gestures |
| Morphing/warping | Geometry distortion at thin lines, small objects | Wider lens, fewer thin lines, slower motion |
| Style drift mid-clip | Vague style description | Treat style as checklist, not vibe; keep clips short |
| Temporal flicker | Conflicting lighting instructions | Single consistent light source, "locked tripod" |
| Texture crawl | High-frequency detail (paper grain) in static areas | Explicitly state "static paper texture, no movement in background" |
| Jitter | Multiple camera movements, unqualified "fast" | One camera instruction only |

### Risks Specific to Our Pencil Test Aesthetic

**High risk:**
- "Thin, high-contrast edges" (pencil lines) are listed as a known limitation resistant to full artifact elimination
- Paper texture may trigger "texture crawl" — the grain shifts/moves despite being static

**Medium risk:**
- Style drift toward digital/clean look over longer clips
- Construction lines may be interpreted as noise and cleaned up by the model

**Mitigation strategy:**
- 4–5 second clips maximum
- Aggressive style anchoring in every prompt
- Pre-clean keyframes: normalize exposure, remove scan artifacts
- Test with simplest transition first (F01→F06 idle settle)

---

## Comparison: Which Model for Our Use Case?

| Dimension | Seedance 2.0 | Kling 2.1/3.0 | Veo 3.1 |
|-----------|-------------|---------------|---------|
| Illustrated style handling | Strong (anime, cel, line art) | Defaults to photorealism | Mixed |
| Character consistency | Strong (reference system) | Moderate | Moderate |
| Start+End frame | YES | YES (Kling 2.0+) | Limited |
| Max resolution | 720p | 1080p | 1080p |
| Cost (5s, 720p) | ~$1.50 standard | ~$1.25 | ~$1.00 |
| Generation time | 60–180s (API) | 60–120s | 30–90s |
| Content filters | Aggressive (blocks realistic faces) | Moderate | Moderate |
| Our test result | Successful (Act 1 test exists) | Tested, compressed prompts better | Tested, compressed prompts better |

**Recommendation:** Seedance 2.0 remains our primary choice — we have a proven test, it handles illustrated styles well, and the start+end frame interpolation is exactly what our pipeline needs. Content filters shouldn't affect us since our inputs are pencil drawings, not photographs.

---

## Setup Checklist

1. Get Fal.ai API key from [fal.ai dashboard](https://fal.ai/dashboard)
2. Add to `.env`: `FAL_KEY=your-key-here`
3. Install: `pip install fal-client`
4. Host keyframe images at accessible URLs (fal.ai accepts direct URLs or base64)
5. Test with Fast tier at 480p/4s first, scale up after validating aesthetic
