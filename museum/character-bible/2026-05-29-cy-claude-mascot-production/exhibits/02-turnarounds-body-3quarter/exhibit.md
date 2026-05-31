# Plate — turnarounds/body-3quarter.png

- kind: plate_verdict
- outcome: human_gate_required
- decided by: cy
- date: 2026-05-29
- pil-perceptual similarity: 0.2738
- evidence: rich

## Rationale

The plate fails multiple critical color, style, and outline rules due to being saved as a JPEG (with a .png extension) and containing 12,238 unique colors instead of 4. Specifically: 
1. IR.claude-mascot.palette.four-indexed-color-vocabulary is violated: 36.74% of the silhouette pixels are violating. The dark outline uses colors around #432614 instead of the target deep brown #5C3A24 (only 32 pixels match the deep brown range). Additionally, cream highlight is present down to y=923 (feet/toes), violating the constraint that it only appear on the face, crown, and fingertips.
2. IR.claude-mascot.palette.no-anti-aliasing-between-steps and IR.claude-mascot.style.no-gradient-interpolation-between-palette are violated: transitions between colors are multi-pixel gradients rather than sharp 1-pixel steps.
3. IR.claude-mascot.style.integer-pixel-grid-no-subpixel is violated due to sub-pixel smoothing and compression artifacts.
4. IR.claude-mascot.style.dither-vertical-2px-warm-brown is violated: there is no vertical dither pattern (0 isolated shadow pixels found); shadows are solid fills with anti-aliased boundaries.
5. IR.claude-mascot.proportion.silhouette-round-topped-lozenge is borderline/fail: at 32px scale, the silhouette displays an hourglass contour (neck indentation of 18px between a 20px head and 22px body) and separated legs instead of a tapering lozenge.
6. IR.claude-mascot.palette.primary-orange-dominant-fill, IR.claude-mascot.proportion.head-to-body-2-to-3-chibi (deviation is 4.62% of total height, within ±10% tolerance), and IR.claude-mascot.proportion.body-width-1-2x-head-width (ratio is 1.159, within ±15% tolerance of 1.2) are honored.

_(source: plate_verdicts.jsonl)_

## Cites criteria

- `IR.claude-mascot.palette.four-indexed-color-vocabulary`
- `IR.claude-mascot.palette.no-anti-aliasing-between-steps`
- `IR.claude-mascot.palette.primary-orange-dominant-fill`
- `IR.claude-mascot.proportion.head-to-body-2-to-3-chibi`
- `IR.claude-mascot.proportion.body-width-1-2x-head-width`
- `IR.claude-mascot.proportion.silhouette-round-topped-lozenge`
- `IR.claude-mascot.style.integer-pixel-grid-no-subpixel`
- `IR.claude-mascot.style.dither-vertical-2px-warm-brown`
- `IR.claude-mascot.style.no-gradient-interpolation-between-palette`

## Provenance

- `runs/2026-05-29-cy-claude-mascot-production/plate_verdicts.jsonl#L2`
