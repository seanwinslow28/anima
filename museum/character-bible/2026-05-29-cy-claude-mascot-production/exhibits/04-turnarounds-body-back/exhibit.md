# Plate — turnarounds/body-back.png

- kind: plate_verdict
- outcome: human_gate_required
- decided by: cy
- date: 2026-05-29
- pil-perceptual similarity: 0.2673
- evidence: rich

## Rationale

The plate body-back.png fails to honor almost all the cited identity rules. (1) IR.claude-mascot.palette.four-indexed-color-vocabulary is violated: 42.24% of the pixels inside the silhouette fall outside the strict palette tolerances, and the image contains 9,957 unique colors due to lossy JPEG compression and anti-aliasing. (2) IR.claude-mascot.palette.no-anti-aliasing-between-steps is violated: transitions between boundaries are smoothed gradients spanning 3-4 pixels (e.g., #a8673f -> #a76239 -> #be7349 -> #e59769 -> #e49364) instead of direct 1-pixel changes. (3) IR.claude-mascot.palette.primary-orange-dominant-fill is borderline/honored: primary orange makes up 49.58% under strict tolerance, but visually dominates >50% of the silhouette due to color-shifted orange pixels. (4) IR.claude-mascot.proportion.head-to-body-2-to-3-chibi is violated: with a total height of 779px and neck division at y=567 (rel_y=465), the head height is 466px (59.8% of total height) and body is 313px (40.2%), yielding a ratio of 1.49:1 (target 2:3/0.67; deviation is 19.8%, which exceeds the ±10% tolerance). (5) IR.claude-mascot.proportion.silhouette-round-topped-lozenge is violated: the profile is hourglass-shaped, narrowing from a head width of 479px to a neck width of 297px before expanding to a body width of 478px, rather than a tapering round-topped lozenge. (6) IR.claude-mascot.style.integer-pixel-grid-no-subpixel is violated: edges exhibit significant sub-pixel smoothing/anti-aliasing. (7) IR.claude-mascot.style.dither-vertical-2px-warm-brown is violated: there are 0 isolated warm brown shadow pixels (0.00% dither candidates); shadows are rendered as solid blocks with blurry edges.

_(source: plate_verdicts.jsonl)_

## Cites criteria

- `IR.claude-mascot.palette.four-indexed-color-vocabulary`
- `IR.claude-mascot.palette.no-anti-aliasing-between-steps`
- `IR.claude-mascot.palette.primary-orange-dominant-fill`
- `IR.claude-mascot.proportion.head-to-body-2-to-3-chibi`
- `IR.claude-mascot.proportion.silhouette-round-topped-lozenge`
- `IR.claude-mascot.style.integer-pixel-grid-no-subpixel`
- `IR.claude-mascot.style.dither-vertical-2px-warm-brown`

## Provenance

- `runs/2026-05-29-cy-claude-mascot-production/plate_verdicts.jsonl#L4`
