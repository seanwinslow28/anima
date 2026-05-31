# Plate — turnarounds/body-front.png

- kind: plate_verdict
- outcome: human_gate_required
- decided by: cy
- date: 2026-05-29
- pil-perceptual similarity: 1.0
- evidence: rich

## Rationale

The plate turnarounds/body-front.png fails all cited identity rules. 1. IR.claude-mascot.palette.four-indexed-color-vocabulary: The plate renders with 8,987 unique colors instead of exactly four indexed colors due to heavy anti-aliasing. Additionally, the colors do not fall within the specified RGB tolerances (the dominant orange is #D67656 instead of #E89B6B, which is outside the ±10 tolerance; the light gray is #CAC9C7 instead of cream #F4DDB8, etc.). 2. IR.claude-mascot.palette.primary-orange-dominant-fill: The primary orange color does not occupy the majority of the silhouette, and the incorrect palette lacks the flat orange fill. 3. IR.claude-mascot.proportion.head-to-body-2-to-3-chibi: The character's proportions are distorted; the head height (approx. 328px) is twice the height of the remaining body (approx. 164px), violating the 2:3 chibi ratio. Counting the thin vertical artifact line at the bottom-right extends total height to 1245px, which also deviates completely from the chibi register. 4. IR.claude-mascot.proportion.body-width-1-2x-head-width: The body width does not measure 1.2x the head width, and the shape lacks defined shoulders. 5. IR.claude-mascot.proportion.silhouette-round-topped-lozenge: The silhouette reads as a horizontal rectangle with a thin line at the bottom-right rather than a round-topped lozenge. 6. IR.claude-mascot.style.integer-pixel-grid-no-subpixel: There is extensive sub-pixel rendering and anti-aliasing along the color boundaries and contours.

_(source: plate_verdicts.jsonl)_

## Cites criteria

- `IR.claude-mascot.palette.four-indexed-color-vocabulary`
- `IR.claude-mascot.palette.primary-orange-dominant-fill`
- `IR.claude-mascot.proportion.head-to-body-2-to-3-chibi`
- `IR.claude-mascot.proportion.body-width-1-2x-head-width`
- `IR.claude-mascot.proportion.silhouette-round-topped-lozenge`
- `IR.claude-mascot.style.integer-pixel-grid-no-subpixel`

## Provenance

- `runs/2026-05-29-cy-claude-mascot-production/plate_verdicts.jsonl#L1`
