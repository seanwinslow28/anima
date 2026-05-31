# Plate — turnarounds/body-3quarter.png

- kind: plate_verdict
- outcome: human_gate_required
- decided by: cy
- date: 2026-05-30
- dinov2 similarity: 0.911
- evidence: rich

## Rationale

The plate fails to honor the identity rules due to a clear palette violation, along with borderline issues in body proportion and shadow rendering. Specifically:

1. Palette Violation (IR.claude-mascot.palette.terracotta-orange-body): The body fill color measures at `#d5926f` (RGB [214, 146, 112]), which is significantly lighter and peachier than the warm terracotta orange `#C77C52` (RGB [199, 124, 82]). The deviation (R: +15, G: +22, B: +30) exceeds the specified ±10 RGB tolerance.
2. Proportion Borderline (IR.claude-mascot.proportion.rounded-box-silhouette): The body box in the FRONT view measures 204px wide by 189px tall (ratio 1.08:1, wider than tall), failing the requirement to read slightly taller than wide (~1:1.2 width:height). The BACK view reads as a square (ratio 0.99:1). Only the SIDE view is taller than wide (ratio 0.78:1).
3. Style Borderline (IR.claude-mascot.style.warm-graphite-line-cross-hatch): While the hand-drawn pencil cross-hatching style is followed, the shadow area fails to read as `#9E5A38` due to the lighter base fill color, with shadow line segments measuring around `#a56e4f` instead.
4. Anatomy Rules (IR.claude-mascot.anatomy.two-ear-arm-nubs, IR.claude-mascot.anatomy.four-stub-legs, IR.claude-mascot.anatomy.no-arms-no-hands): These rules are fully honored. The nubs are unarticulated cylinder nubs, there are no arms or hands, and the stub legs are peg-like with no details. The front view hides the back legs completely, and the profile view shows exactly two legs.

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

- `runs/2026-05-30-cy-claude-mascot-pencil/plate_verdicts.jsonl#L2`
