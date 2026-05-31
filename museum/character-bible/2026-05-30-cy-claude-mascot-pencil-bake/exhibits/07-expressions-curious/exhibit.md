# Plate — expressions/curious.png

- kind: plate_verdict
- outcome: human_gate_required
- decided by: cy
- date: 2026-05-30
- dinov2 similarity: 0.9705
- evidence: rich

## Rationale

The plate violates two key identity rules. First, under IR.claude-mascot.proportion.rounded-box-silhouette, the mascot's body is wider than tall (approximately 1.2:1 width:height) instead of the required taller-than-wide proportion (approximately 1:1.2 width:height). Second, under IR.claude-mascot.face.two-dot-eyes-with-brows, the eyes are not simple dots/ovals, but rather large cartoon eyes with prominent glossy white highlights, which is explicitly cited as a violation. The other rules are honored: the construction cross-line is visible (IR.claude-mascot.face.construction-cross-line), there is no mouth (IR.claude-mascot.face.minimal-mouth-line), the palette is a warm terracotta orange (IR.claude-mascot.palette.terracotta-orange-body), and the drawing uses hand-drawn warm graphite lines with cross-hatched shadows (IR.claude-mascot.style.warm-graphite-line-cross-hatch).

_(source: plate_verdicts.jsonl)_

## Cites criteria

- `IR.claude-mascot.proportion.rounded-box-silhouette`
- `IR.claude-mascot.face.two-dot-eyes-with-brows`
- `IR.claude-mascot.face.construction-cross-line`
- `IR.claude-mascot.face.minimal-mouth-line`
- `IR.claude-mascot.palette.terracotta-orange-body`
- `IR.claude-mascot.style.warm-graphite-line-cross-hatch`

## Provenance

- `runs/2026-05-30-cy-claude-mascot-pencil-bake/plate_verdicts.jsonl#L7`
