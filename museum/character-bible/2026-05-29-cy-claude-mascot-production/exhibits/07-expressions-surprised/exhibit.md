Cy recorded this as **human_gate_required** on 2026-05-29 — plate — expressions/surprised.png. It took 3 attempts.

The note on record reads: "The plate image 'expressions/surprised.png' fails to honor the identity rules for the claude-mascot character across multiple criteria. Specifically:
1. Palette Violation (IR.claude-mascot.palette.four-indexed-color-vocabulary): The image is a 1024x1024 RGB image containing 8,205 unique colors rather than the canonical four-indexed colors. A solid grey background of (32, 32, 32) is also present, which is not in the palette.
2. Anti-aliasing Violation (IR.claude-mascot.palette.no-anti-aliasing-between-steps): Transitions are smooth gradients containing thousands of intermediate RGB values rather than stair-stepped, single-pixel boundary changes.
3. Pixel Grid Violation (IR.claude-mascot.style.integer-pixel-grid-no-subpixel): Every edge and contour is rendered using high-resolution continuous lines with sub-pixel gradients rather than landing on integer coordinates at the native low resolution.
4. Eye Clusters Violation (IR.claude-mascot.face.eye-deep-brown-dot-cluster): The eyes are rendered as large, anti-aliased circular shapes consisting of hundreds of pixels, not the required small 1-to-4 deep brown #5C3A24 pixel clusters.
5. Mouth Line Violation (IR.claude-mascot.face.mouth-line-deep-brown-single-stroke): The open mouth is rendered as a large high-resolution shape with gradient transitions and anti-aliased boundaries, violating the style and color rules.
6. Chibi Proportion Violation (IR.claude-mascot.proportion.head-to-body-2-to-3-chibi): The character spans 638 pixels vertically (Y=224 to Y=861). The head spans approximately 328 pixels (Y=224 to Y=552), representing ~51.4% of total height. This falls below the lower tolerance limit of the chibi 2:3 ratio (66.7% ± 10%, i.e., 56.7% to 76.7%), making the head too small and proportioned more like a standard 1:2 chibi humanoid.
7. Expression Vocabulary (IR.claude-mascot.face.expression-vocabulary-three-only): The surprised expression is part of the three authored expressions, so this rule is technically honored without requiring escalation, though its visual implementation is incorrect." (from plate_verdicts.jsonl).

Measured similarity to the reference: 0.1451 via pil-perceptual; the vision read was fail.

It cites `IR.claude-mascot.face.eye-deep-brown-dot-cluster`, `IR.claude-mascot.face.mouth-line-deep-brown-single-stroke`, `IR.claude-mascot.face.expression-vocabulary-three-only`, `IR.claude-mascot.palette.four-indexed-color-vocabulary` (and 3 more).
