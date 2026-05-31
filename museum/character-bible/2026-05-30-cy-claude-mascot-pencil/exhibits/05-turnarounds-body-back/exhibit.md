# Plate — turnarounds/body-back.png

- kind: plate_verdict
- outcome: human_gate_required
- decided by: cy
- date: 2026-05-30
- dinov2 similarity: 0.911
- evidence: rich

## Rationale

The plate violates two of the cited identity rules: 1. IR.claude-mascot.proportion.rounded-box-silhouette is violated because the body box is wider than it is tall (approx. 1.2:1 width:height ratio, ~200px wide by ~170px tall), which is the inverse of the requirement to be slightly taller than wide (approx. 1:1.2 width:height). 2. IR.claude-mascot.anatomy.four-stub-legs is violated because the front view shows only two legs without the back pair being partly occluded behind, and the side view shows three legs instead of only the two near legs (near front and near back) reading as required by the occlusion description. The remaining rules (IR.claude-mascot.anatomy.two-ear-arm-nubs, IR.claude-mascot.anatomy.no-arms-no-hands, and IR.claude-mascot.style.warm-graphite-line-cross-hatch) are honored.

_(source: plate_verdicts.jsonl)_

## Cites criteria

- `IR.claude-mascot.proportion.rounded-box-silhouette`
- `IR.claude-mascot.anatomy.two-ear-arm-nubs`
- `IR.claude-mascot.anatomy.four-stub-legs`
- `IR.claude-mascot.anatomy.no-arms-no-hands`
- `IR.claude-mascot.style.warm-graphite-line-cross-hatch`

## Provenance

- `runs/2026-05-30-cy-claude-mascot-pencil/plate_verdicts.jsonl#L5`
