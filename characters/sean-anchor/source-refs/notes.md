# Sean — voice + style notes for Cy

*A short prose note Sean leaves for Cy ahead of her Pass-1 authoring. The things that don't fit in image references but Cy reads before emitting a single identity rule.*

---

## Style register

`pencil-test-colored`. Warm cream paper, warm graphite gray line weight (HB through 2B), construction lines visible beneath the final drawing, cross-hatching in shadow areas (under chin, clothing folds), limited desaturated color palette. The aesthetic is traditional pencil animation — *not* digital cleanup, not vector linework, not cel shading. The `style:` block in `manifest.yaml` carries the canonical register description for the Pencil Test reference implementation; treat that block as authoritative when the source refs are ambiguous.

## The stylus is the prop

Sean's stylus stays in his right hand in every frame. The right hand grips near the barrel with three fingers visible (thumb + index + middle); the left hand never holds the stylus. This is the load-bearing prop continuity rule the existing Act 1 shipped against, and the rule Em catches drift on at T2 critic time. Visible in front, 3-quarter, and profile views; back view shows the right arm's silhouette indicating the grip.

## Proportion

Heroic-realistic. Head height fits seven times into total body height (1:7), measured from crown to sole. Shoulders sit roughly 1.5 head-widths apart at neutral pose; hip-to-floor is approximately 4 head-heights. This is not chibi, not stylized-tall — it's a working-illustrator's grown adult proportion. The walk-cycle source line-art and the existing approved Act 1 frames are the canonical references for proportion.

## What's already shipped

The Pencil Test Act 1 (Frames 1-42, 12fps loop) shipped against the A-2 anchor at `characters/sean-anchor/anchor.png`. The approved keyframes live under `runs/act1-*/approved/` and serve as the authoritative continuity reference for what already exists. Act 2 is in flight; the Seedance generation plan + shot list live at `docs/act2-seedance-shot-list.md` and `docs/2026-04-27-act2-seedance-execution-plan.md`. Cy should consider any IR.sean.* rule that would invalidate Act 1's shipped frames a contract conflict — Sean reviews those flags before approval.

**`anchor.png` label-cleaned 2026-06-17 (Tier 1 Slice A).** The drawn `(A-2)` corner label was patched out — it bleeds as text into generated frames (NB2's caption-rendering failure mode) and the anchor is injected first on every Spark frame. The labeled original is kept verbatim at `characters/sean-anchor/anchor.labeled-original.png`; the figure and dimensions are byte-untouched. (Reference hygiene only — no IR.sean.* rule changed; the criteria lock is intact.)

## Costume

Default outfit: dark navy tee, cool gray jeans, the stylus. No outfit variations exist in commit 2; a hoodie / jacket / formal variant would be a future Bible authoring pass (a new entry under `characters/sean-anchor/costumes/{variant}/`).

## Source refs in this folder

  - `turnaround-1.png` — the cleaner-line full turnaround from `images/NEW-ANIMATION-PIPELINE/sean-character-turnaround-2.png`. Front, 3-quarter, profile, back.
  - `turnaround-2.png` — the earlier rougher turnaround from `images/sean-character-turnaround.png`. Lower fidelity but carries the original character-design intent before the Act 1 production cleanup.
  - `head-turn/head-turn-{1..9}.png` — the 9-frame head-turn sequence Sean drew in Procreate. The first and last frames are anchor-grade; the middle frames are interpretive. Cy's risk-bible should hedge on which middle frames the back-of-skull is canonically drawn from.
  - `walk-cycle/source.png` — Sean's raw line-art walk cycle (the source plate).
  - `walk-cycle/derived-v{1,2}.png` — two earlier derived-style passes of the walk cycle. The derived plates aren't authoritative for IR.sean.motion.walk-cycle.* rules; the source line-art is.
  - `3d-mannequin/*.png` — Five sprite-reference Mannequin poses + three 3D character reference renders. Useful for the proportion + pose-vocabulary rules; not direct identity references (the mannequin doesn't carry Sean's face or hair).

## What the references *don't* cover

  - Expressions beyond neutral / focused / surprised / contemplative — Cy should treat the expression set as interpretive and surface "expression range" as a covered scope in the risk-bible.
  - Motion plates beyond walk cycle and head turn — turns, runs, jumps, gesture variants are absent. Phase 6 motion shots needing these need their own plate authoring pass before they can cite IR.sean.motion.* rules confidently.
  - Lit skin tones — the pencil-test register flattens skin to paper-base + cross-hatching shadow. A future variant in `costumes/{lit-skin}/` or a separate Bible authoring pass would extend the palette.

---

*Cy: read the source refs in the order above. Author Pass-1 IR.* rules against the canonical references first (turnaround-1, head-turn 1 + 9, walk-cycle/source.png, the anchor); reach for the secondary references only when the primary doesn't constrain the rule you want to write.*
