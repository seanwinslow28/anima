# ChatGPT Image Generation (gpt-image-1 / DALL-E)

## Model Characteristics

OpenAI's image generation models excel at:
- Photorealistic rendering
- Creative interpretation of concepts
- Text rendering in images (improved in recent versions)
- Artistic style blending

## Prompt Optimization

### Strengths to Leverage
- **Conversational prompts:** Natural language descriptions work well
- **Concept blending:** "X meets Y" style descriptions are understood
- **Artistic references:** Named art movements and styles are recognized
- **Detail layering:** Can handle complex scene descriptions

### Syntax Preferences
- Conversational, descriptive sentences preferred
- Style references can be more abstract: "in the style of pixel art"
- Aspect ratio specifications are respected
- Quality modifiers: "high quality", "detailed", "professional"

### Effective Patterns
```
"A [subject description] in [style]. The [composition details]. 
[Lighting and mood]. [Technical specifications]. [Quality modifiers]."
```

### Known Behaviors
- May add artistic interpretation to prompts (less literal than Gemini)
- Tends toward photorealism unless explicitly steered
- Responds to mood/atmosphere descriptors
- "Illustration", "concept art", "sprite sheet" are recognized formats

## Pixel Art Optimization

For retro game aesthetics, be explicit:
```
"pixel art sprite, exactly [N]x[N] pixels, limited color palette of [N] colors, 
no anti-aliasing, sharp pixel edges, retro video game style"
```

For authentic retro look:
```
"8-bit style pixel art, NES color palette, dithering pattern shading, 
clean pixel edges with no smoothing"
```

## Character Sheets

ChatGPT can generate character sheets but may require:
- Explicit "character reference sheet" or "model sheet" terminology
- View specifications: "front view, side view, back view, 3/4 view"
- "Same character in each pose" for consistency
- "White background, evenly spaced poses"

## Limitations to Work Around
- May "improve" pixel art with anti-aliasing (counter with explicit negatives)
- Can drift on color palettes (specify exact colors if critical)
- Multi-panel consistency may require regeneration attempts

## API Considerations
- gpt-image-1 models have specific size options
- Consider cost per generation for iteration workflows
- Batch generation may be more cost-effective for exploration
