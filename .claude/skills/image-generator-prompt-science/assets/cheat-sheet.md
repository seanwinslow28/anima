# Prompt Engineering Quick Reference

## The 7 Layers (In Order)
1. **Task Declaration** - What to create
2. **Context Foundation** - Background & format
3. **Style Definition** - Visual specs in (parentheses)
4. **Compositional Layout** - Spatial arrangement with explicit order
5. **Consistency Constraints** - Identity/scale/alignment rules
6. **Technical Uniformity** - Lighting/shadow consistency
7. **Output Specs + Negatives** - Quality + exclusions

## Golden Rules
- Sentences > keyword lists
- Numbers > adjectives (`3-4 tones` not `limited palette`)
- Enumerate order explicitly (`in this order: A, B, C`)
- Repeat "consistent" for emphasis (4-5 times)
- Group style specs in (parentheses) as clusters
- Use known reference anchors (game titles, eras)
- Plain English negatives work ("No gradients")

## Common Negatives for Pixel Art
```
No anti-aliasing. No gradients. No blur. No soft edges. 
No sub-pixel rendering. No smoothing.
```

## Quantify Everything
| Vague | Specific |
|-------|----------|
| thick outline | 2-3px outline |
| limited palette | 4-color palette |
| dark color | #272929 |
| small | 32x32 pixels |
| cel shaded | 3-4 tone shading |

## Style Cluster Template
```
([GAME/ERA] aesthetic with [COLOR] outlines ([WIDTH]px), 
[N]-tone [SHADING TYPE], [DIRECTION] lighting, [RENDERING] approach)
```
