# Plate — expressions/curious.png

- kind: plate_verdict
- outcome: human_gate_required
- decided by: cy
- date: 2026-05-30
- dinov2 similarity: 0.9124
- evidence: rich

## Rationale

The plate at expressions/curious.png fails multiple core identity rules. First, the body silhouette (IR.claude-mascot.proportion.rounded-box-silhouette) is wider than it is tall (approx. 1.1:1) instead of reading slightly taller than wide (~1:1.2). Second, the eyes (IR.claude-mascot.face.two-dot-eyes-with-brows) are rendered as large round cartoon eyes with white scleras, pupils, and prominent glossy highlights instead of simple warm-graphite dot/oval eyes. Third, the pencil construction cross-line (IR.claude-mascot.face.construction-cross-line) is completely missing from the face, yielding a clean digital finish. Fourth, the mouth (IR.claude-mascot.face.minimal-mouth-line) is a gaping, open oval expressing emotion, violating the prohibition against open-mouth shapes. Finally, both the palette and style rules (IR.claude-mascot.palette.terracotta-orange-body and IR.claude-mascot.style.warm-graphite-line-cross-hatch) are violated by the use of smooth airbrush/gradient shading on the body rather than a flat terracotta fill with warm-graphite cross-hatched shadows.

_(source: plate_verdicts.jsonl)_

## Cites criteria

- `IR.claude-mascot.proportion.rounded-box-silhouette`
- `IR.claude-mascot.face.two-dot-eyes-with-brows`
- `IR.claude-mascot.face.construction-cross-line`
- `IR.claude-mascot.face.minimal-mouth-line`
- `IR.claude-mascot.palette.terracotta-orange-body`
- `IR.claude-mascot.style.warm-graphite-line-cross-hatch`

## Provenance

- `runs/2026-05-30-cy-claude-mascot-pencil/plate_verdicts.jsonl#L7`
