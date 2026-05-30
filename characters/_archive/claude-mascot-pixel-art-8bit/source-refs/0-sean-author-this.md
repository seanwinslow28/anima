# Drop your source material here

*This is the blank-page tax for Bible authoring — paid once, by Cy, before she authors. The folder this file lives in is the surface where Sean drops the inputs Cy reads during Pass 1. Cy is opinionated about what she needs but generous about what she'll work with.*

The Cy-leads-Sean-reviews workflow assumes Sean drops material in here and Cy reads what's actually present. She won't refuse a thin folder — but she will say so explicitly in her risk-bible (the Bible's negative space). The more Sean drops, the less Cy has to extrapolate.

---

## Required (Cy can't author without these)

- [ ] **Anchor image.** The single canonical identity reference for this character. Save as `anchor.png` in the parent character folder (one level up from `source-refs/`). Cy will read this dozens of times during Pass 1 before emitting a single identity rule. If Sean is migrating an existing character (sean-anchor), the anchor is already in place from commit 2.0; this checkbox is satisfied.

## Strongly recommended (cuts Cy's Pass-1 hedging in half)

- [ ] **Turnaround sheet.** Front / 3-quarter / profile / back. One image with all angles, or one image per angle — Cy reads either shape. Drop in `source-refs/` with any filename; Cy infers the category from contents.
- [ ] **Motion references.** Walk cycle, head turn, gesture set — whatever Sean has drawn. Drop the raw line-art under `source-refs/motion-{walk,head-turn,...}/source/` if he wants the source/derived split preserved; otherwise just drop the file and Cy will route it. Sean's hand-drawn motion plates are load-bearing for Phase 6 motion shots — Em's continuity rule grounds against these directly.
- [ ] **3D mannequin or pose references.** Drop under `source-refs/3d-mannequin/`. Useful when the character's pose vocabulary needs to extend beyond the two or three poses the anchor covers.

## Helpful (Cy reads but doesn't require)

- [ ] **Voice and mood notes.** Write a short prose note to `source-refs/notes.md`. What Sean wants Cy to know that won't fit in image references: the character's voice register, posture habits, expression baseline, the small thing about them that's recognizable even when the rendering is rough. One page is the target. Two paragraphs is fine. Half a page is fine.
- [ ] **Existing approved frames from prior productions.** If this character has already shipped in a prior anima piece, the approved frames are the authoritative continuity reference for what already exists. Drop pointers in `notes.md`; Cy doesn't need copies.
- [ ] **Style register declaration**, if it's not obvious from the anchor. The `character.yaml` field is closed-vocabulary (pencil-test-colored / pixel-art-8bit / line-art-only / watercolor / photoreal / 3d-rendered). Cy will infer if she can; Sean's explicit declaration is faster and more reliable.

---

## What Cy will not ask Sean to author

- A complete identity rule graph (Cy emits IR.* entries; Sean reviews and edits via `pipeline bible mutate`)
- Risk inventory (Cy emits `risk-bible.md`; Sean reviews)
- Confidence notes (Cy hedges, Sean reads)
- Per-plate prompts (Cy authors during Pass 1; Sean reviews the Pass-2 generated plates)

---

## What happens after Sean drops material

1. Sean runs `python -m pipeline.cli bible init --target characters/{character_id}/` (or has already, if this folder exists).
2. Sean populates `source-refs/` per the checklist above.
3. Sean invokes Cy (programmatically or via a Maya bible_authoring run). Cy's three-phase loop runs: Opus authors → NB Pro generates → Gemini verifies. Wall time: 5–15 min depending on plate count and how many Gemini-flagged regenerations fire.
4. Sean reviews via `python -m pipeline.cli bible show --character-dir characters/{character_id}/`. The tear sheet renders the Bible header, palette swatch line, identity rules grouped by category, motion-plate inventory, risk-bible callouts, Cy's confidence hedges.
5. Sean approves via `pipeline bible approve`. Identity rules lock; mutations from this point require `--force --actor --reason` and audit to `runs/{run_id}/bible_audit.jsonl`.
6. The Bible is now live. Downstream Phase 5 frames involving this character cite its IR.* rules at T2-critic time. Em grounds verdicts in them. The chairman cites them in T3 disputes. Mo narrates them in the museum walkthrough.

---

*Cy is the character designer. Sean is the director. The Bible is the contract between them.*
