# Nano Banana Pro (Google Gemini Image Generation)

## Model Characteristics

Nano Banana Pro (Gemini 3 Pro Image) excels at:
- Following complex multi-panel instructions
- Maintaining character consistency across views
- Understanding spatial relationships and layouts
- Processing reference images for style matching

## Prompt Optimization

### Strengths to Leverage
- **Instruction following:** Use detailed, multi-sentence descriptions
- **Reference handling:** "based strictly on the uploaded reference" works well
- **Layout comprehension:** Explicit grid/row/column instructions are respected
- **Style matching:** Parenthetical style clusters are parsed effectively

### Syntax Preferences
- Plain English paragraphs outperform tag lists
- Hex color codes are understood: `#272929`, `#9BBC0F`
- Pixel dimensions are respected: `32x32`, `2-3px`
- Explicit ordering: "in this order: A, B, C, D" prevents randomization

### Effective Patterns
```
"Create [output] based strictly on [reference]. Use [background]. Present as [format] 
while matching the exact visual style of the reference ([style cluster with technical specs]). 
Arrange [layout description with explicit enumeration]. Maintain [consistency rules]. 
Output [quality specs]. No [negatives]."
```

### Known Behaviors
- Responds well to repetition of key constraints (consistency, alignment)
- Processes parenthetical groupings as unified style concepts
- Negatives in plain English ("No gradients") are effective
- "Print-ready" triggers higher detail retention

## Pixel Art Optimization

For retro game aesthetics:
```
"pixel rendering approach, pixel details, crisp edges. No anti-aliasing, No gradients, 
No soft edges, No blur"
```

Palette enforcement:
```
"strict 4-color palette using only: #9BBC0F (lightest), #8BAC0F (light), 
#306230 (dark), #0F380F (darkest)"
```

## Pricing Context
- ~$0.139 per 2K resolution image
- Cost-effective for iteration and batch generation
- Consider for high-volume asset pipelines
