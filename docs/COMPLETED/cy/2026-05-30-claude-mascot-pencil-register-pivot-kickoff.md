# Kickoff prompt — re-author the claude-mascot Bible in pencil-test register (Act 2 pivot)

*Paste everything below the divider into a Claude Code session opened at `/Users/seanwinslow/Code-Brain/anima`. This is a CODE + authoring session with live model calls and human-review gates (🚦 STOP). The decision is made: retire the pixel-art claude-mascot, re-author it in the same `pencil-test-colored` register as Sean, using the multi-view reference assets that already exist — which simultaneously advances the Act 2 animation. Read the rationale in `docs/research/2026-05-30-nb-pro-nb2-prompting-for-pixel-and-angle-expansion.md` and the hold finding in `docs/anima-test-runs/2026-05-29-production-bake-and-gate-hardening.md` §6 before starting.*

---

You are pivoting the **claude-mascot** character from the `pixel-art-8bit` register to `pencil-test-colored`, and re-authoring its Bible against real multi-view reference art. **Why this pivot:** the pixel mascot failed on a *reference gap* (one flat sprite → NB Pro invented a standing biped for turnarounds), and Sean won't ship a pixelated mascot anyway. The pencil-test version (a) has a real 5-view turnaround sheet that closes the reference gap, (b) lives in the same register as the sean-anchor Bible, and (c) is the actual Act 2 character — Sean carries the mascot on his shoulder. This pass tests Cy on a second same-register character *and* produces shippable Act 2 assets.

**The reference assets (already on disk) at `images/NEW-ANIMATION-PIPELINE/claude-mascot-pencil-test/`:**
- `claude-mascot.png` — labeled "C-B", a clean ¾-front hero portrait of the creature in pencil-test color. **→ this becomes the new `anchor.png`.**
- `claude-mascot-turnaround.png` — labeled "C-1 TURNAROUND", five views (FRONT / ¾ FRONT / SIDE / ¾ BACK / BACK) on one sheet. **→ the load-bearing multi-view reference** (per the research doc, a single multi-view sheet is what enables NB's "photogrammetric inference" for new angles — this is exactly what the pixel mascot lacked).
- `sean-with-claude-mascot.png` — labeled "A-7", Sean (full-color pencil-test, stylus in hand) with the mascot on his shoulder. **→ the relationship/scale reference and the Act 2 two-character continuity ground-truth.**

**The creature's form (for `notes.md` and trait-locking):** a rounded-box body in warm terracotta-orange, two small ear/arm nubs on the sides, four short stub legs, two dot eyes with a faint pencil construction cross-line, soft cast shadow, warm cream paper. No arms, no hands, no mouth-as-feature beyond a small line. It is small enough to perch on a shoulder. Same pencil-test-colored register as Sean: warm graphite line, flat color fills, cross-hatch shadow, cream paper, hole-punch production marks.

**Read this before planning — the editing template + routing decisions (new, 2026-05-30):** Two companion docs now sit alongside this kickoff and change how the plate prompting and the bake should run. Read both before mapping execution. [`docs/research/2026-05-30-nb2-editing-character-consistency-template.md`](../../research/2026-05-30-nb2-editing-character-consistency-template.md) is the research + the headline artifact: a **register-agnostic five-slot editing-prompt template** (`{identity_lock}` / `{variation}` / `{preserve_and_negative}` / `{style_register}` / `{output_spec}`) where Cy authors only the terse `{variation}` intent and the runner fills the rest from a per-register clause library. The pencil-test mascot plates this kickoff bakes are the `pencil-test-colored` instance of that template — the same "terse intent + strong reference + trait-lock" discipline this kickoff already mandates, now generalized and named. [`docs/2026-05-30-claude-mascot-pencil-register-pivot-kickoff-amendments.md`](2026-05-30-claude-mascot-pencil-register-pivot-kickoff-amendments.md) is the plan that wires it into Cy.

**Two decisions Sean made this session that this pass must honor.** First, **route the Phase 4 bake to NB2 (`gemini-3.1-flash-image-preview`), not NB Pro.** The research is decisive that editing/consistency work holds identity better on NB2, costs half, runs 4× faster, and avoids NB Pro's documented multi-reference downsampling regression (Google AI dev forum, Mar 2026) — and `pencil-test-colored` routes to NB2 per the amendments' per-register table. `invoke_nb_pro` currently defaults to the wrong model for this; pass the NB2 slug (or set it in the manifest) for the mascot bake, which also strengthens this kickoff's own expectation that the across-angle plates hold the box-creature form. Second, the broader template-emitter refactor of `_build_nb_pro_prompt` and the manifest per-register routing are **planned for a follow-on, not required to complete this mascot pass** — but the execution plan should note them so the bake here doesn't bake in a prompt shape the refactor will immediately rework. Treat the NB Pro regression as a condition to re-verify at implementation time, not a permanent law. When you map the full execution (via `/writing-plans`), fold these two docs in as inputs: the bake runs on NB2, the plate prompts follow the template's terse-`{variation}` contract, and the Phase 5 two-character frame uses the template's **storyboard variant** (see Amendment C).

**Working discipline (non-negotiable):**
- Plan mode first (`Shift+Tab` twice). Show the plan. Proceed only on Sean's approval.
- `.venv/bin/pytest tests/ -q` stays green (≥187) before and after every commit.
- Each phase is its own commit; CHANGELOG per commit.
- 🚦 **STOP gates are real** — present the artifact to Sean and wait for an explicit go before `bible approve`, before committing baked plates, and at the two-character check.
- Apply the fidelity-fix lessons: **terse plate prompts + strong references + trait-locked tokens beat verbose descriptions** (the `focused`-went-monochrome lesson). No pixel post-process node here — that was the pixel register; this is pencil.

---

## Phase 1 — Retire the pixel-art mascot Bible (preserve as evidence, do not delete)

The current `characters/claude-mascot/` is a **locked** `pixel-art-8bit` Bible (13 rules). Supersede it cleanly:

1. Archive the whole current Bible folder to `characters/_archive/claude-mascot-pixel-art-8bit/` (use `git mv` so history is preserved). Add a short `README.md` there: "Retired 2026-05-30. The pixel-art-8bit mascot failed on a reference-gap (single flat anchor → invented biped turnarounds; see `docs/anima-test-runs/2026-05-29-production-bake-and-gate-hardening.md` §6). Superseded by the pencil-test-colored mascot Bible. Kept as register-vocabulary validation evidence — the schema authored clean pixel-art rules; the failure was generation, not schema."
2. Update `manifest.yaml`: change `characters.claude-mascot.style_register` from `pixel-art-8bit` to `pencil-test-colored`, and repoint `characters.claude-mascot.folder` if the path changes (it shouldn't — re-author in place at `characters/claude-mascot/`). Leave `criteria_sources` pointing at `characters/claude-mascot/acceptance_criteria.json` (the new Bible will write there).
3. Commit: `retire: archive pixel-art-8bit claude-mascot Bible; flip register → pencil-test-colored`.

## Phase 2 — Stage the new source material

Re-create `characters/claude-mascot/` as a fresh pencil-test Bible scaffold (`python -m pipeline.cli bible init --target characters/claude-mascot/`), then stage source material per `templates/bible/source-refs-checklist.md`:

1. **Anchor:** copy `images/NEW-ANIMATION-PIPELINE/claude-mascot-pencil-test/claude-mascot.png` → `characters/claude-mascot/anchor.png` (the C-B ¾ hero portrait — the canonical identity).
2. **Multi-view turnaround (load-bearing):** copy `claude-mascot-turnaround.png` → `characters/claude-mascot/source-refs/turnaround-c1.png`. This is the reference that closes the angle-expansion gap — Cy's generate plates for new angles reference this, not just the anchor.
3. **Relationship/scale + continuity ground-truth:** copy `sean-with-claude-mascot.png` → `characters/claude-mascot/source-refs/sean-with-claude-mascot.png`.
4. **`source-refs/notes.md`:** author a short note covering — register (`pencil-test-colored`); the creature's form (box body, ear/arm nubs, four stub legs, dot eyes, construction cross-line, no arms/hands); proportions (roughly 1:1.2 box, small enough to perch on a shoulder); the relationship to Sean (rides on his shoulder — A-7 is the canonical pairing); expression baseline (calm, curious). Tell Cy the turnaround sheet is the authoritative multi-angle reference and the C-B portrait is the identity anchor.
5. Commit: `feat: stage pencil-test claude-mascot source-refs (C-B anchor, C-1 turnaround, A-7 pairing)`.

## Phase 3 — Re-author the Bible (full authoring run, new register)

This is a **full** Cy authoring run (Pass 1 re-authors the rule graph for the new register) — NOT plates-only, because palette/proportion/style rules all change from pixel to pencil. The Pass-1 retry-on-parse-failure + loud stub guard (shipped 2026-05-29) handle transient Opus 4.8 malformations; if it stubs three times, stop and report.

1. Run:
   `python scripts/author_bible.py characters/claude-mascot/ --studio-brief "Claude-mascot in pencil-test-colored register — Sean's shoulder companion for Act 2. Box-body creature, see source-refs/notes.md and the C-1 turnaround for all angles." --run-dir runs/2026-05-30-cy-claude-mascot-pencil/`
2. Cy emits the rule graph (`IR.claude-mascot.*` — same namespace, new register vocabulary: warm-graphite line, the terracotta-orange + cream palette in *pencil* terms, box-creature proportion rules, cross-hatch shadow, construction lines), the plate plan, risk-bible, confidence-notes.
3. **Verify the plate plan applies the research before baking:** generated angle plates must reference `anchor.png` + `source-refs/turnaround-c1.png` (the multi-view sheet), and the prompts must be **terse intent + trait-lock tokens**, not verbose monochrome-era prose. The trait-lock block to reuse verbatim: `rounded-box body · warm terracotta-orange fill · cream paper #F2E6CC · warm-graphite line + cross-hatch shadow · two ear/arm nubs · four stub legs · two dot eyes + construction cross-line · no arms, no hands · shoulder-companion scale`. If Cy emitted verbose prose, trim it before Phase 4.
4. `bible show --character-dir characters/claude-mascot/` and 🚦 **STOP — present the rule graph to Sean** (register correct? palette in pencil terms? proportions match the creature? any pixel-era language leaked? `grep -iE "pixel|integer-grid|dither|anti-alias|indexed"` across the four Bible artifacts must return ZERO hits — this is the register-purity check, the mirror of the original defang). Fix anything Sean calls, then on his go: `bible approve --character-dir characters/claude-mascot/`. Commit: `bible: author + approve pencil-test claude-mascot Bible (IR.claude-mascot.* re-registered)`.

## Phase 4 — Bake the plates against the approved Bible

With the Bible approved (`locked: true`), the bake runs **plates-only** (the locked auto-detect routes it — no Pass 1 re-author, no Opus call, no stub risk):

1. `python scripts/author_bible.py characters/claude-mascot/ --run-dir runs/2026-05-30-cy-claude-mascot-pencil-bake/` (plates-only auto-selected because the Bible is locked).
2. The turnaround/expression plates generate against the anchor + C-1 multi-view sheet using the fixed runner mechanism (anchor injection, no chaining, terse role-tag prompts). **Expectation:** because the turnaround sheet supplies all five real angles, the new-angle plates should hold the box-creature form — no invented biped, the failure mode that held the pixel run.
3. Copy approved plate PNGs into `characters/claude-mascot/{turnarounds,expressions,...}/`.
4. 🚦 **STOP — show Sean the full plate set.** The bar: every plate reads as the *same box-creature from the turnaround sheet* across angles — not a new creature, not a humanoid. Re-roll any individual drifter via `bible iterate --target <dir> --reject <plate> --reason "..."`. Score with the DINOv2 similarity tier (now installed) against the anchor and persist to `plate_verdicts.jsonl`. On Sean's approval, commit: `bake: claude-mascot pencil-test production plates (form held across angles)`.

## Phase 5 — First two-character continuity check (exploratory — scope, don't over-build)

This is new ground: the pipeline has never loaded two real Bibles into one scene. Keep it light and exploratory — the goal is to *exercise the path and find the gaps*, not build a finished multi-character system.

1. **Confirm both Bibles load together.** The manifest `criteria_sources` already merges `sean-anchor` + `claude-mascot` acceptance criteria — verify the merged CriteriaBundle carries both `IR.sean.*` and `IR.claude-mascot.*` without ID collisions. Report what loads.
2. **The continuity ground-truth is A-7** (`source-refs/sean-with-claude-mascot.png`). Generate one test two-character frame (Sean with the mascot on his shoulder) referencing both anchors + A-7, and 🚦 **STOP — show Sean** a visual continuity check against A-7: is Sean still Sean, is the mascot still the box-creature, is the *scale* right (mascot sized to perch on a shoulder), is the register consistent across both?
3. **Name the gap, don't fill it blindly.** `pipeline/continuity_audit.py`'s CC01–CC08 checks are hardcoded to Sean/Act-1 (stylus hand, hair, etc.) — there is no generalized *cross-character* continuity audit. Write a short findings note (`docs/anima-test-runs/2026-05-30-two-character-first-light.md`) scoping what a real multi-character continuity check needs (per-character IR loading, relative-scale rule, who-occludes-whom, shared-register check) as the input to a future dedicated session. Do **not** build that system in this session.
4. Commit the findings note + the test frame as evidence: `docs: two-character first-light — Sean + mascot continuity scope`.

## Phase 6 — Wrap

1. `.venv/bin/pytest tests/ -q` — green, report count.
2. CHANGELOG entry covering the register pivot + re-author + bake + two-character first-light. Update `CLAUDE.md`: the claude-mascot is now `pencil-test-colored` (update the characters table / register references and the "second-character validation" framing — it now validates *same-register second character + Act 2 companion*, and the pixel-art cross-register validation is explicitly deferred to a future 16BitFit-humanoid pass per `docs/research/2026-05-30-...`).
3. `git push`. Report: commits shipped, test count, plate verdicts, and exactly what Sean still needs to eyeball before this feeds Act 2.

**Out of scope (queued, do not start):** the 16BitFit-humanoid pixel-register pass (the deferred cross-register validation — its own future session); the per-view-reference hard gate; Em's closing-the-loop case 7; sean-anchor rounder-cartoon identity tuning. Don't touch the rename or the sean-anchor Bible.

**Rollback:** every phase is its own commit. The archived pixel Bible at `characters/_archive/` is the restore point if the pivot is reversed. A bad bake is `git revert` + re-roll; the approved rules aren't touched by a bake.
