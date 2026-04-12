---
name: image-generator-prompt-science
description: Engineering effective prompts for AI image generation models (Nano Banana Pro, ChatGPT/DALL-E, Midjourney, Flux, Stable Diffusion, etc.). Use when creating, refining, or analyzing prompts for generating images, sprites, character sheets, UI assets, concept art, or any visual content. Triggers include requests to write image prompts, improve existing prompts, create visual assets, generate character turnarounds, design sprites, or when troubleshooting why generated images don't match expectations.
---

# Image Generator Prompt Science

This skill provides a systematic framework for engineering prompts that produce consistent, high-quality results across AI image generation models.

## Core Principle: Narrative Structure Over Keywords

Image models trained on image-caption pairs parse natural language better than comma-separated tags. Write prompts as clear instructions, not keyword lists.

```
❌ "pixel art, sf2 style, turnaround, consistent, high quality, 4k, detailed"
✅ "Create a character reference sheet matching the Street Fighter II arcade aesthetic with bold outlines and 3-4 tone cel shading"
```

## The 7-Layer Prompt Framework

Build prompts using these layers in order:

### Layer 1: Task Declaration
Clear action + output type. State exactly what you want created.
```
"Create a professional character reference sheet based on the uploaded reference image"
"Generate a 32x32 pixel sprite walk cycle for a fantasy warrior"
```

### Layer 2: Context Foundation
Environment, background, and format specifications.
```
"Use a clean, neutral plain background and present as a technical model turnaround"
"On a transparent background, formatted as a horizontal sprite strip"
```

### Layer 3: Style Definition
Visual language with technical specs. Use parenthetical grouping for style clusters.
```
"Match the Street Fighter II arcade aesthetic (bold #272929 dark outlines at 2-3px, 
3-4 tone cel shading, top-front lighting, pixel rendering approach)"
```

**Style cluster components:**
- Visual anchor (known game, artist, era)
- Line treatment (weight, color, approach)
- Shading method (tone count, direction)
- Lighting setup (direction, intensity, softness)
- Rendering approach (pixel, vector, painted, cel)

### Layer 4: Compositional Layout
Spatial organization with explicit ordering. Never leave arrangement ambiguous.
```
"Arrange into two horizontal rows. Top row: four full-body views placed side-by-side 
in this order: front view, left profile (facing left), right profile (facing right), 
back view. Bottom row: three close-up portraits aligned beneath."
```

**Key principle:** Enumerate elements in explicit order rather than just counting them.

### Layer 5: Consistency Constraints
Identity, scale, and alignment rules. Repeat "consistent" for emphasis.
```
"Maintain perfect identity consistency across every panel. Keep consistent scale 
and alignment between views, accurate anatomy, and clear silhouette. Ensure 
uniform framing and consistent head height across the lineup."
```

### Layer 6: Technical Uniformity
Lighting, shadows, mood, and rendering consistency across the output.
```
"Lighting should be consistent across all panels (same top-front lighting, intensity, 
and softness), with natural, controlled shadows that preserve detail without dramatic 
mood shifts."
```

### Layer 7: Output Specs + Negatives
Quality descriptors AND explicit exclusions.
```
"Output crisp, print-ready reference sheet with pixel details. 
No anti-aliasing. No gradients. No motion blur."
```

**Critical:** Negative constraints in plain English often work better than negative prompt fields.

## Fill-In Template

```markdown
[TASK DECLARATION]
Create a [output type] based on [reference/context]. 

[CONTEXT FOUNDATION]  
Use [environment/background] and present as [format/genre].

[STYLE DEFINITION]
Achieve [style reference] with ([technical specs]):
- Visual anchor: [known style, game, artist]
- Lines: [weight, color, approach]
- Shading: [tone count, direction]
- Lighting: [direction, intensity]
- Rendering: [pixel, vector, painted]

[COMPOSITIONAL LAYOUT]
Arrange [spatial organization]. 
[Section 1]: [enumerated elements in explicit order].
[Section 2]: [enumerated elements in explicit order].

[CONSISTENCY CONSTRAINTS]
Maintain [identity/style] consistency across [all elements].
Keep [subject attributes] with [scale/alignment/pose rules].
Ensure [spacing/framing/proportion rules].

[TECHNICAL UNIFORMITY]
[Lighting/color/mood] consistent across [scope]:
- Same [specific attributes]
- [Shadow/highlight behavior rules]

[OUTPUT SPECS + NEGATIVES]
Output [quality descriptors].
No [exclusion 1]. No [exclusion 2]. No [exclusion 3].
```

## Effectiveness Techniques

### Quantified Parameters
Numbers beat adjectives. Be specific.
```
❌ "limited palette"     ✅ "3-4 tone palette"
❌ "thick outlines"      ✅ "2-3px outlines"
❌ "dark color"          ✅ "#272929"
❌ "small sprite"        ✅ "32x32 pixels"
```

### Nested Parenthetical Detail
Group related style attributes as a unified concept:
```
"matching the exact visual style (Street Fighter II arcade aesthetic with bold 
#272929 dark outlines (2-3px), 3-4 tone cel shading on face showing bone structure, 
top-front lighting, pixel rendering)"
```

### Repetition for Emphasis
Models weight repeated concepts more heavily. Saying "consistent" 4-5 times across different constraints reinforces the requirement.

### Known Reference Anchoring
Anchor to well-known visual styles the model has seen during training:
- Games: "Street Fighter II", "Final Fantasy VI", "Pokémon Red/Blue"
- Eras: "16-bit SNES era", "Game Boy DMG aesthetic"
- Artists: "Akira Toriyama style", "Moebius-inspired"

## Video Models: A Different Philosophy

The 7-Layer framework is designed for **image** generation. Video generation models (Veo, Kling, etc.) work on the opposite principle: **less detail = better motion**.

Video models interpolate motion between concepts. Over-detailed prompts over-constrain the generation — the model tries to hit every specified movement and overcomplicates the result. Compress to 3 layers:

1. **Medium + Style** (one sentence) — what visual medium
2. **Action Arc** (bulk) — WHAT happens in plain verbs, not HOW each body part moves
3. **Style Guardrails + Negatives** (one sentence) — what to preserve, what to prevent

```
❌ "His head tilts ~15° downward. Eyes drop to the stylus. After 2-3 frames, 
his head snaps back up over 3-4 frames. Eyebrows lift, eyes widen slightly..."

✅ "He glances down at his stylus, then snaps his head up with an idea — 
eyebrows lift, smile widens."
```

Skip frame counts, degree measurements, secondary motion details, and animation jargon. Describe the action, not the mechanics — let the model fill in the motion.

See [references/video-models.md](references/video-models.md) for full guidance including start-frame/end-frame prompting (Kling `@Image1`/`@Image2` format, Veo).

## Model-Specific Guidance

See reference files for model-specific optimization:
- [references/nano-banana-pro.md](references/nano-banana-pro.md) - Google Gemini's image model
- [references/chatgpt-dalle.md](references/chatgpt-dalle.md) - OpenAI's gpt-image-1 models
- [references/flux-midjourney.md](references/flux-midjourney.md) - Flux, Midjourney, and artistic models
- [references/video-models.md](references/video-models.md) - Video generation models (Veo, Kling) — less is more

## Project-Specific Style References

- [references/16bitfit-styles.md](references/16bitfit-styles.md) - Dual-aesthetic system (DMG 4-color + Battle Mode full-color)

## Common Asset Type Patterns

### Character Turnaround Sheets
Emphasize: identity consistency, panel ordering, uniform lighting, A-pose or T-pose, clean panel separation.

### Sprite Sheets & Animation Frames
Emphasize: grid alignment, frame count, pixel-perfect edges, transparent background, consistent palette.

### UI Elements & Icons
Emphasize: exact dimensions, padding consistency, state variations (normal/hover/pressed), scalability.

### Environment & Background Art
Emphasize: parallax layer separation, color atmosphere, focal point, edge treatment for tiling.

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|--------------|-----|
| Inconsistent character identity | Missing consistency constraints | Add explicit identity repetition in Layer 5 |
| Wrong art style | Vague style reference | Use specific game/era anchors with technical specs |
| Color bleeding/gradients | No negative constraints | Add "No gradients. No anti-aliasing." |
| Layout chaos | Ambiguous composition | Enumerate exact positions and ordering |
| Over-detailed output | No simplicity constraints | Add "clean", "minimal", specific poly/tone counts |
| Wrong dimensions | Assumed defaults | Specify exact pixel dimensions early |
