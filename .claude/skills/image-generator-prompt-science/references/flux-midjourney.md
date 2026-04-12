# Flux, Midjourney & Artistic Models

## Model Family Overview

### Flux (Black Forest Labs)
- High coherence and prompt adherence
- Strong at complex compositions
- Good text rendering capabilities
- Available via Fal.ai, Replicate, and other APIs

### Midjourney
- Exceptional aesthetic quality
- Strong artistic stylization
- Discord-based or API access
- Unique parameter syntax (--ar, --v, --style)

### Stable Diffusion (SDXL, SD3)
- Open source, highly customizable
- LoRA and fine-tuning support
- Local or cloud deployment
- Requires more prompt engineering

## Flux Optimization

### Prompt Structure
Flux responds well to detailed, structured prompts:
```
"[Subject] in [setting]. [Action/pose]. [Style description]. [Lighting]. [Technical specs]."
```

### Effective Techniques
- Front-load important elements
- Use specific artistic references
- Detailed composition descriptions work well
- Supports negative prompts for exclusions

### Pixel Art with Flux
```
"pixel art sprite of [subject], [N]-bit video game style, limited [N]-color palette, 
sharp pixel edges, no anti-aliasing, retro game aesthetic, clean sprite work"
```

## Midjourney Optimization

### Parameter Syntax
- `--ar 16:9` - Aspect ratio
- `--v 6` - Version selection
- `--style raw` - Less stylization
- `--no [element]` - Negative prompting
- `--q 2` - Quality setting

### Prompt Structure
Midjourney favors concise, evocative prompts:
```
[subject], [style keywords], [mood], [technical params] --ar 1:1 --v 6
```

### Style Keywords That Work
- Art movements: "art nouveau", "bauhaus", "ukiyo-e"
- Game aesthetics: "16-bit", "pixel art", "sprite sheet"
- Rendering: "cel shaded", "flat colors", "vector art"
- Quality: "detailed", "professional", "crisp"

### Pixel Art Challenges
Midjourney tends toward aesthetic interpretation. For strict pixel art:
```
pixel art, 8-bit style, limited palette, sharp pixels, no smoothing, 
retro video game sprite --style raw --no gradient --no blur --no anti-aliasing
```

## Stable Diffusion Optimization

### Prompt Weighting
Use parentheses for emphasis:
- `(important element)` - Slight emphasis
- `((very important))` - Strong emphasis
- `[de-emphasized]` - Reduced weight

### Negative Prompts
SD models use separate negative prompt fields effectively:
```
Negative: blurry, smooth, gradient, anti-aliased, soft edges, watermark, 
signature, low quality, jpeg artifacts
```

### LoRA Integration
For consistent styles, LoRA models can enforce:
- Specific color palettes
- Character consistency
- Art style adherence
- Technical rendering approaches

### Pixel Art Checkpoint/LoRA
Consider specialized pixel art models:
- Pixel art LoRAs trained on authentic retro sprites
- Palette-specific models for era accuracy
- Character-consistent LoRAs for animation frames

## Cross-Model Consistency Tips

When working across multiple models:
1. **Document your working prompts** - What works varies by model
2. **Test core elements first** - Style, composition, then details
3. **Build a prompt library** - Save successful patterns per model
4. **Plan for post-processing** - Color quantization, cleanup may be needed
5. **Batch for comparison** - Generate same concept across models to compare
