# Plate — turnarounds/body-3quarter.png

- kind: plate_verdict
- outcome: ingested
- decided by: cy
- date: 2026-05-30
- dinov2 similarity: 0.922
- evidence: rich

## Rationale

The plate overall honors the identity rules, with a minor numeric color shift due to background paper texture blending. 

- **IR.claude-mascot.proportion.rounded-box-silhouette**: Honored. The body is a single rounded box with no separate head. The ratio of width to height is approximately 195:234 (~1:1.2), and all edges/corners are generously curved.
- **IR.claude-mascot.proportion.shoulder-companion-scale**: Honored. The notebook paper line spacing relative to the mascot confirms its small, desktop/shoulder-companion scale.
- **IR.claude-mascot.anatomy.two-ear-arm-nubs**: Honored. Exactly two short (~1/5 body width), unarticulated, rounded cylindrical nubs project horizontally near the vertical mid-height.
- **IR.claude-mascot.anatomy.four-stub-legs**: Honored. Exactly four short (~1/6 body height) stub legs sit under the body's footprint without splaying or detail (no feet or toes).
- **IR.claude-mascot.anatomy.no-arms-no-hands**: Honored. The mascot has no arms, hands, or grasping limbs.
- **IR.claude-mascot.palette.terracotta-orange-body**: Borderline/Pass. Visually, the body fills with a warm, medium-saturation terracotta clay orange, and the shadow is rendered as warm-graphite cross-hatching. Numerically, the colors are shifted to ~#DA9673 (RGB [218, 150, 115]) on the main body fill due to blending with the warm cream notebook paper background (#FCF4DD), which exceeds the strict ±10 RGB tolerance for #C77C52 ([199, 124, 82]). However, it is consistent with the rest of the turnaround model sheets.
- **IR.claude-mascot.style.warm-graphite-line-cross-hatch**: Honored. Contour and interior lines are warm-graphite pencil (~1-2px, peak color ~#583F2B close to target #3D3530) showing varied weight. Shading is strictly hand-drawn cross-hatching rather than flat/cel/airbrush gradients.

_(source: plate_verdicts.jsonl)_

## Cites criteria

- `IR.claude-mascot.proportion.rounded-box-silhouette`
- `IR.claude-mascot.proportion.shoulder-companion-scale`
- `IR.claude-mascot.anatomy.two-ear-arm-nubs`
- `IR.claude-mascot.anatomy.four-stub-legs`
- `IR.claude-mascot.anatomy.no-arms-no-hands`
- `IR.claude-mascot.palette.terracotta-orange-body`
- `IR.claude-mascot.style.warm-graphite-line-cross-hatch`

## Provenance

- `runs/2026-05-30-cy-claude-mascot-pencil-bake-v2/plate_verdicts.jsonl#L2`
