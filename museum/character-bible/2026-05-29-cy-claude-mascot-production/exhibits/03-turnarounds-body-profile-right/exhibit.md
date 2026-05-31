# Plate — turnarounds/body-profile-right.png

- kind: plate_verdict
- outcome: human_gate_required
- decided by: cy
- date: 2026-05-29
- pil-perceptual similarity: 0.374
- evidence: rich

## Rationale

The plate violates several core design rules: 1) Palette & AA: The image contains 10,307 unique colors instead of exactly four indexed colors due to JPEG compression artifacts and visible anti-aliasing (23.33% of silhouette pixels violate the palette ranges), violating IR.claude-mascot.palette.four-indexed-color-vocabulary, IR.claude-mascot.palette.no-anti-aliasing-between-steps, and IR.claude-mascot.style.no-gradient-interpolation-between-palette. 2) Grid & Dither: The pixel-art elements are not aligned to a native 1:1 integer pixel grid and feature smoothed, rounded shapes (including the dither dots on the left, which render as anti-aliased circles rather than single-pixel marks), violating IR.claude-mascot.style.integer-pixel-grid-no-subpixel and IR.claude-mascot.style.dither-vertical-2px-warm-brown. 3) Silhouette: The silhouette fails the round-topped lozenge requirement at thumbnail scale due to a protruding muzzle, two separate protruding feet, and a body wider than the head (1.04x ratio instead of tapering narrower), violating IR.claude-mascot.proportion.silhouette-round-topped-lozenge. Proportions (IR.claude-mascot.proportion.head-to-body-2-to-3-chibi) are within the 10% tolerance (head-to-body ratio is 0.63 vs 0.67 target), and primary orange remains the dominant silhouette color (>50%), honoring IR.claude-mascot.palette.primary-orange-dominant-fill.

_(source: plate_verdicts.jsonl)_

## Cites criteria

- `IR.claude-mascot.palette.four-indexed-color-vocabulary`
- `IR.claude-mascot.palette.no-anti-aliasing-between-steps`
- `IR.claude-mascot.palette.primary-orange-dominant-fill`
- `IR.claude-mascot.proportion.head-to-body-2-to-3-chibi`
- `IR.claude-mascot.proportion.silhouette-round-topped-lozenge`
- `IR.claude-mascot.style.integer-pixel-grid-no-subpixel`
- `IR.claude-mascot.style.dither-vertical-2px-warm-brown`
- `IR.claude-mascot.style.no-gradient-interpolation-between-palette`

## Provenance

- `runs/2026-05-29-cy-claude-mascot-production/plate_verdicts.jsonl#L3`
