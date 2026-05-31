# Plate — expressions/neutral.png

- kind: plate_verdict
- outcome: human_gate_required
- decided by: cy
- date: 2026-05-30
- dinov2 similarity: 0.8975
- evidence: rich

## Rationale

The plate fails to honor several of the cited identity rules. 1. Under IR.claude-mascot.face.two-dot-eyes-with-brows, the eyes are positioned extremely far apart (approximately 196px gap for eyes that are ~30px wide, which is roughly 6.5 times the eye-width instead of the required 'roughly one eye-width apart'). 2. Under IR.claude-mascot.palette.terracotta-orange-body, the body fill color (#d59573 / RGB 213, 149, 115) deviates significantly from the target terracotta orange (#C77C52 / RGB 199, 124, 82) by up to +33 RGB, which is far outside the specified +/-10 RGB tolerance. 3. Under IR.claude-mascot.proportion.rounded-box-silhouette, the body box is wider than it is tall (approx. 495px wide by 450px high, or a 1.1:1 ratio), which is the opposite of the specified 'slightly taller than wide, approximately 1:1.2'. The plate successfully honors IR.claude-mascot.face.construction-cross-line (construction lines are visible), IR.claude-mascot.face.minimal-mouth-line (no mouth line exists, which is acceptable), IR.claude-mascot.style.warm-graphite-line-cross-hatch (warm graphite linework and cross-hatched shading are present), and IR.claude-mascot.style.cream-paper-and-cast-shadow (cream substrate with visible grain, hole-punches, and a scribble ellipse cast shadow).

_(source: plate_verdicts.jsonl)_

## Cites criteria

- `IR.claude-mascot.proportion.rounded-box-silhouette`
- `IR.claude-mascot.face.two-dot-eyes-with-brows`
- `IR.claude-mascot.face.construction-cross-line`
- `IR.claude-mascot.face.minimal-mouth-line`
- `IR.claude-mascot.palette.terracotta-orange-body`
- `IR.claude-mascot.style.warm-graphite-line-cross-hatch`
- `IR.claude-mascot.style.cream-paper-and-cast-shadow`

## Provenance

- `runs/2026-05-30-cy-claude-mascot-pencil-bake/plate_verdicts.jsonl#L6`
