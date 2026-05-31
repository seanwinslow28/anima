Cy recorded this as **human_gate_required** on 2026-05-30 — plate — turnarounds/body-front.png. It took 1 attempt.

The note on record reads: "The plate violates several identity rules. Specifically: 
1. **IR.claude-mascot.proportion.rounded-box-silhouette** is violated: The mascot's body is wider than it is tall (approx 1.2:1 width:height), whereas the rule specifies it should read slightly taller than wide, approximately 1:1.2 (width:height).
2. **IR.claude-mascot.anatomy.four-stub-legs** is violated: Only two legs are drawn; there is no second pair of legs partly occluded behind them as required by the rule ('In front view the front pair reads clearly with the back pair partly occluded behind').
3. **IR.claude-mascot.style.cream-paper-and-cast-shadow** is violated: There is no soft, loose graphite-scribble cast shadow directly beneath the box on the paper.
4. **IR.claude-mascot.face.two-dot-eyes-with-brows** is borderline: The eyes have distinct glossy highlights, which the rule warns can drift the character ('large round cartoon eyes with big glossy highlights... drift the character').

The following rules are honored:
- **IR.claude-mascot.anatomy.two-ear-arm-nubs**: Two short, unarticulated nubs project horizontally near the construction midline.
- **IR.claude-mascot.face.construction-cross-line**: The faint pencil construction cross-lines are visible under the eyes and bisecting the face.
- **IR.claude-mascot.face.minimal-mouth-line**: The face has no mouth line, which satisfies the 'at most a small, short mouth line' constraint.
- **IR.claude-mascot.palette.terracotta-orange-body**: The body color matches the warm terracotta orange fill with cross-hatched shading on the underside.
- **IR.claude-mascot.style.warm-graphite-line-cross-hatch**: The drawing features warm-graphite line art and pencil cross-hatching." (from plate_verdicts.jsonl).

Measured similarity to the reference: 0.8857 via dinov2; the vision read was fail.

It cites `IR.claude-mascot.proportion.rounded-box-silhouette`, `IR.claude-mascot.anatomy.two-ear-arm-nubs`, `IR.claude-mascot.anatomy.four-stub-legs`, `IR.claude-mascot.face.two-dot-eyes-with-brows` (and 5 more).
