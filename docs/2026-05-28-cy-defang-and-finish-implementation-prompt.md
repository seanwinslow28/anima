# Implementation Prompt — Cy defang + finish commit 2 + 2b

**Created:** 2026-05-28
**For:** The next Claude Code execution session (plan mode, multi-file edits, git).
**Workstream:** anima Phase 2 — finish what's left of commit 2 + ship commit 2b. **One critical insertion: Task 1.4.5 — defang the pencil-test bias in Cy and Em's standing contexts, BEFORE Tasks 1.10 + 1.11 (the two real Bible authoring runs).** Sean caught the bias during a pacing-pause review and the audit confirmed it: the contracts are style-agnostic but the prompts that drive Pass-1 Opus output tilt every Bible toward pencil-test patterns regardless of what `style_register` says. Without the defang, the claude-mascot Bible run in Task 1.11 fights the preamble.
**Reads as:** Studio-manual voice, prose where reasonable. Sean's exact tonal directive — *"I don't like it when the docs feel like it was strictly made for the terminal. We're making art. It should feel free."*

---

You're picking up the anima project mid-commit. Seven commits landed in the previous session on `feature/maya-planner-and-em-live`:

| # | Commit | Task |
|---|--------|------|
| 1 | a4a0614 | docs — Cy brainstorm artifacts |
| 2 | 63b6603 | 2.0 — sean-anchor migration with back-compat symlink |
| 3 | 643d8bc | 1.1 — criteria.py v1.2 IR.* namespace + character_id + plate-region pointer |
| 4 | dcc2cf9 | 1.2 — NB Pro runner wrapper with content-addressed cache + reject-aware invalidation |
| 5 | 3461c67 | 1.3 — Bible templates (character.yaml + source-refs-checklist) |
| 6 | 4c00937 | 1.4 — Cy's standing-context preamble |
| 7 | c869b0b | 1.5 — Cy three-phase AgentSpec (1,091 LOC + 9 tests) |

Test suite stands at **122 green** (90 prior + 16 IR + 7 NB Pro + 9 Cy). No regressions in any prior surface. The pacing-pause was deliberate: Task 1.5 is the structural heart Tasks 1.6 / 1.7 / 1.8 / 1.9 all inherit, so Sean reviewed Cy's AgentSpec contract before letting four dependents land on it.

**The review surfaced a real problem.** The architecture supports arbitrary 2D styles — the contracts are clean — but the prompts have pencil-test bias baked in that will tilt every Cy run toward pencil-test patterns regardless of what `style_register` says. The closed-vocabulary `style_register` field on `character.yaml` has six values (`pencil-test-colored | pixel-art-8bit | line-art-only | watercolor | photoreal | 3d-rendered`) and the validator enforces them, but the four prompt files that drive Opus output anchor implicitly on pencil-test as the default register, the default failure mode, and the default "what good looks like" example. A pixel-art-8bit Bible authoring run would have Cy defending against "digital cleanup" — which is what pixel-art *looks like*. A watercolor Bible run would land cross-hatching rules. A 3d-rendered Bible run would still get told to watch for paper-texture flattening.

The defang pass is a surgical four-file edit. It lands as Task 1.4.5 between the non-interactive Phase 1 work and the Sean-driven Bible authoring runs. Without it, Task 1.11 (claude-mascot) is fighting the preamble. With it, Task 1.11 IS the validation that the defang worked.

This session executes the rest of the existing plan at `docs/superpowers/plans/you-re-picking-up-the-refactored-hickey.md` with the defang inserted at the right seam, plus a guardrail layer so this kind of bias can't creep back into future prompt additions.

## Read these binding docs first, in this order

Don't skip ahead.

1. [`PHILOSOPHY.md`](../PHILOSOPHY.md) — the load-bearing intent doc, six load-bearing beliefs. The engine truth (*"If the loop plays smoothly and the character is recognizably itself in its intended medium, it ships"*) is style-agnostic by design and the defang must honor that — the medium is whatever the Studio Brief said, not pencil-test by default.
2. [`CLAUDE.md`](../CLAUDE.md) — anima project manual, current state post-commits 3 + 3b + 8.1a + 2.0 + 1.1-1.5.
3. [`docs/superpowers/plans/you-re-picking-up-the-refactored-hickey.md`](superpowers/plans/you-re-picking-up-the-refactored-hickey.md) — the existing implementation plan with the full task graph. **This session executes Tasks 1.6, 1.7, 1.8, 1.9, then the new Task 1.4.5 inserted here, then 1.10, 1.11, 1.12, then Phase 2 (commit 2b).** The plan's task descriptions stand verbatim — this prompt amends the sequencing and adds 1.4.5 + the guardrail layer.
4. [`docs/2026-05-27-cy-character-bible-brainstorm.md`](2026-05-27-cy-character-bible-brainstorm.md) — the brainstorm artifact. The closed `style_register` vocabulary in TOP-1 is the structural commitment that anima is a 2D animation pipeline, NOT a pencil-test pipeline.
5. [`docs/2026-05-26-agent-fleet-brainstorm-v2.md`](2026-05-26-agent-fleet-brainstorm-v2.md) §2.1 (Cy as the missed pinnacle phase). The thesis — *validators cannot recover taste that was absent at generation time* — applies to style register too. If Opus's preamble teaches Cy to author pencil-test rules by default, the rules for a pixel-art Bible will silently fail to constrain.
6. [`docs/research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md`](research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md) §5 — the structural-fix-at-the-source thesis. Style-register-anchored prompts ARE a source bias.
7. [`docs/Image-Model-DR-2026/SYNTHESIS.md`](Image-Model-DR-2026/SYNTHESIS.md) §2 — Flo's Phase 5 routing reads `style_register` to pick the right generator. Pencil-test-colored routes to NB Pro; pixel-art-8bit may route differently; future registers will route differently again. The routing layer already treats style as a categorical choice — the prompts must match.
8. [`CHANGELOG.md`](../CHANGELOG.md) — recent entries (top of the file).

## What the audit found (the defang's targets)

Four files carry the bias. Each fix is surgical — name the specific lines, replace pencil-test-specific framing with style-register-aware framing, preserve the studio-manual voice.

**1. `pipeline/agents/prompts/anima-standing-context.md` line 37 — the highest-leverage problem.** The "Template-trap drift" section in the `## What you must not do` block currently reads:

> **Template-trap drift.** Generic AI-animation aesthetic creeps in when the prompt loses pencil-test specificity. Construction lines disappear, cross-hatching smooths out, line weight homogenizes. If you notice the aesthetic drifting from pencil-test toward digital-cleanup, name it and propose the prompt fix.

Every agent — Cy, Em, Maya, eventually Sam / Bea / Mo — reads this preamble. A pixel-art Bible run inherits "watch for cross-hatching smoothing out" as a structural concern, which is incoherent against the register. The fix: rewrite so the template trap is *drifting from the character's manifested style register toward a generic AI-animation aesthetic*, with pencil-test as ONE example among the closed vocabulary. The replacement reads roughly:

> **Template-trap drift.** Generic AI-animation aesthetic creeps in when the prompt loses the character's manifested style register specificity — whatever `character.yaml`'s `style_register` field declares (`pencil-test-colored`, `pixel-art-8bit`, `line-art-only`, `watercolor`, `photoreal`, `3d-rendered`). Each register has its own load-bearing markers: pencil-test wants construction lines + varied 1-3px line weight + cross-hatching shadows + cream paper texture; pixel-art wants closed-palette dithering + integer-pixel grid alignment + sub-1x scale silhouette readability; watercolor wants edge-feathering + pigment-pool color variation; and so on. If you notice the aesthetic drifting from the declared register toward a generic digital-cleanup look, name what drifted by register-specific marker (not by pencil-test default) and propose the prompt fix in the register's own vocabulary.

The voice stays studio-manual. The examples stay specific. The default stops being pencil-test.

**2. `pipeline/agents/prompts/cy-character-designer-context.md` lines 135-181 — Cy's "What good looks like" section.** Three sample IR.* entries (all `IR.sean.*`, all pencil-test) plus a four-paragraph risk-bible excerpt that explicitly anchors on pencil-test-colored. This is Cy's primary Pass-1 seed; her output looks like the examples. The fix: keep the sean-anchor pencil-test example block AND add a parallel pixel-art-8bit Claude Mascot example block so Opus sees the schema work for two distinct registers. The studio-manual voice stays — these are excerpts from real Bibles, not abstract schema notes. The two examples teach Cy that the schema is register-agnostic; the rules describe whatever the register requires.

The pixel-art Claude Mascot example block should have:
- Three sample `IR.claude-mascot.*` entries — one each across the palette / proportion / style categories. Sample IDs: `IR.claude-mascot.palette.limited-orange-cream-vocabulary`, `IR.claude-mascot.proportion.head-to-body-2-to-3-chibi`, `IR.claude-mascot.style.integer-pixel-grid-no-anti-aliasing`. Descriptions specific enough that Em can ground a verdict in them — "the orange hex is `#E89B6B` ± 10 RGB units; any orange outside this range is a palette violation" beats "the orange is consistent."
- A four-paragraph risk-bible excerpt for claude-mascot that mirrors the structure of the sean-anchor risk-bible excerpt — what plates the Bible covers, what costume variations exist (none — single sprite outfit), what the palette locks (4-color closed vocab), what's deliberately absent from the Bible (no motion plates yet, no expression variations beyond default).

The pencil-test sean-anchor example stays as-is — it's a real working Bible reference. The new pixel-art-8bit example sits alongside it. Together they demonstrate the schema is style-agnostic by construction.

**3. `pipeline/agents/prompts/em-vision-critic-context.md` line 52 — Em's preamble has the same problem.** The "Aesthetic drift" failure mode in Em's `## What you must not do` block currently reads:

> **Aesthetic drift.** Construction lines disappear. Line weight homogenizes from 1-3px varied to flat 1px. Cross-hatching softens into gradient shading. Paper texture flattens. The pencil test starts looking like digital cleanup.

Em runs across every style register but this teaches it pencil-test as the default failure mode. The fix: register-aware drift language — Em loads the character's `style_register` first (already in Cy's contract), then watches for drift in that register's specific markers. The replacement reads roughly:

> **Aesthetic drift.** The character's manifested style register specifics start washing out toward generic AI-animation cleanup. For a `pencil-test-colored` register: construction lines disappear, line weight homogenizes from 1-3px varied to flat 1px, cross-hatching softens into gradient shading, paper texture flattens. For `pixel-art-8bit`: the integer-pixel grid breaks (sub-pixel anti-aliasing appears), the palette opens past its declared vocabulary, dithering patterns smooth into gradient banding. For `watercolor`: edges harden, pigment-pool variation flattens. Load the character's `style_register` first; cite register-specific markers in your verdict — *"line weight drifted from 1-3px varied to 1px flat"* beats *"the line weight is wrong."*

The pencil-test specifics stay as an example because Em currently runs primarily against pencil-test work; pixel-art and watercolor examples join the rotation so the prompt doesn't single-case-bias.

**4. `pipeline/agents/prompts/maya-planner-context.md` lines 98-99 — Maya's sample criterion.** Currently `AC.tone.pencil-not-digital`. The description references pencil-test specifically (`Construction lines visible; line weight varies 1–3px; cross-hatching present in shadow areas; the piece reads as pencil-test rough, not digital cleanup.`). Maya emits criteria seeded by her own examples; a future bible-authoring brief for a watercolor character would carry pencil-test bias into the criteria. The fix: change the sample to `AC.tone.matches-style-register` (or similar register-aware ID) with a description that reads *"The piece manifests the brief's declared style register cleanly across every shot. The Cy-authored character Bibles in this run carry the per-register markers; this AC enforces consistency at the production layer."* The example stays concrete; the bias stops.

**5. Minor — `pipeline/agents/character_designer.py:380` stub fallback.** Hardcodes `style_register: "pencil-test-colored"`. Only fires when Opus is unavailable (tests + dev machines without SDK). Fix: make it folder-name-aware — if the character_id contains `mascot` → `pixel-art-8bit`; otherwise default `pencil-test-colored` AND add a code comment naming the limitation so future Cy-stub readers understand the bias is intentional-test-only. Production runs never hit this path; this is a test-fixture cleanup.

## Reference implementations to ground every contract against

These haven't changed since the previous session's prompt:

- `pipeline/agents/character_designer.py` — Cy's three-phase AgentSpec. Don't edit the contract during the defang — only the stub fallback at line 380.
- `pipeline/agents/prompts/anima-standing-context.md` — the preamble every agent reads. The big defang target.
- `pipeline/agents/prompts/cy-character-designer-context.md` — Cy's role addendum. The second-biggest defang target.
- `pipeline/agents/prompts/em-vision-critic-context.md` — Em's role addendum. Third defang target.
- `pipeline/agents/prompts/maya-planner-context.md` — Maya's role addendum. Fourth defang target (smallest).
- `pipeline/criteria.py` — the v1.2 graph schema. Style-agnostic; no changes here.
- `pipeline/cli/plan.py` — Maya's CLI shape. The bible CLI in Task 1.7 mirrors this.
- `evals/planner/` — the eval suite template Task 2.1-2.5 mirrors.

## Your job this session — five phases

The plan's task numbers are preserved. Task 1.4.5 is the new insertion.

### Phase A — Resume Tasks 1.6 → 1.7 → 1.8 → 1.9 (4-6 hours focused work, non-interactive)

These four tasks land per the existing plan at `docs/superpowers/plans/you-re-picking-up-the-refactored-hickey.md` verbatim. None of them touch the prompt files — they consume Cy's already-shipped AgentSpec contract.

**Task 1.6** — Extend `pipeline/agents/cost_estimator.py` with a Phase 2 row that reads Cy's per-character `plate_generation_plan.json` from `runs/{run_id}/characters/{character_id}/` and prices each `generate` plate at $0.15 NB Pro + $0 Opus + $0 Gemini. Tests per the plan's §"Task 1.6" block. Commit: `Cy: cost estimator includes Phase 2 NB Pro Bible-authoring spend`.

**Task 1.7** — Create `pipeline/cli/bible.py` + wire into `pipeline/cli/__main__.py`. Five subcommands: `init / show / approve / mutate / iterate`. Renderer-as-separate-layer (boxes in the CLI, never on disk). The `mutate` audit trail writes to `runs/{run_id}/bible_audit.jsonl`. The `iterate` command threads `reject_reason` into NB Pro via the cache-invalidation idiom from `nb_pro_runner.py`. Tests per the plan. Commit: `Cy: pipeline bible init/show/approve/mutate/iterate CLI`.

**Task 1.8** — Manifest schema extension (`criteria_sources:` block + multi-criteria-file load merge) + add `project_type: bible_authoring | animation_piece` to `templates/brief/01_production_brief.md`'s YAML frontmatter. The merge helper (`load_all_criteria(manifest) -> CriteriaBundle`) reads Maya's brief file + every loaded Bible's `acceptance_criteria.json`, deduplicates by ID, raises on collisions. Tests per the plan. Commit: `Cy: manifest criteria_sources + project_type frontmatter + multi-criteria load`.

**Task 1.9** — Extend Maya's `pipeline/agents/planner.py` to parse `project_type`. When `bible_authoring`, the emitted plan structurally includes Phase 0 + Phase 2 only (omits Phases 3-9 from the routing legend) and the AC criteria are scoped to Phase 0 + Phase 2. When `animation_piece` (default), behavior is unchanged. Tests per the plan. Commit: `Cy: Maya routes bible_authoring Project-Type to Phase 0 + Phase 2 only`.

### Phase B — Task 1.4.5: defang the pencil-test bias in standing contexts (~45-60 min)

**This task DOES NOT exist in the existing plan.** Insert it here, between Phase A and Phase C. Without it, Phase D's claude-mascot Bible run is fighting the preamble.

**Specific edits, in order:**

1. **Edit `pipeline/agents/prompts/anima-standing-context.md` line 37** per the audit section above. Rewrite the Template-trap drift entry to anchor on "the character's manifested style register" with pencil-test as one example among the closed vocabulary. Keep the studio-manual voice. Preserve the rest of the file unchanged.

2. **Edit `pipeline/agents/prompts/cy-character-designer-context.md` lines 135-181**. Keep the existing pencil-test sean-anchor example block. Insert a parallel pixel-art-8bit Claude Mascot example block immediately after — three sample `IR.claude-mascot.*` entries across palette / proportion / style categories, plus a four-paragraph risk-bible excerpt that mirrors the sean-anchor structure. The two examples sit side by side under the same `## What good looks like` heading. After the second example block, add one short paragraph: *"Both examples land the same schema. The rules describe whatever the register requires — Sean's stylus and cowlick belong to pencil-test-colored; Claude Mascot's integer-pixel grid and limited palette belong to pixel-art-8bit. Style register is what the rules orient against; the schema is what they fit into."*

3. **Edit `pipeline/agents/prompts/em-vision-critic-context.md` line 52** per the audit section above. Rewrite the Aesthetic drift entry to be register-aware. Cite pencil-test, pixel-art, and watercolor specifics so the prompt doesn't single-case-bias. The pencil-test specifics stay because Em currently runs primarily against pencil-test work; the other registers join the rotation explicitly.

4. **Edit `pipeline/agents/prompts/maya-planner-context.md` lines 98-99**. Change the sample criterion ID from `AC.tone.pencil-not-digital` to `AC.tone.matches-style-register`. Rewrite the description to be register-aware. The example stays concrete; the bias stops.

5. **Edit `pipeline/agents/character_designer.py` line 380** (the stub fallback envelope). Make `style_register` folder-name-aware: `"pixel-art-8bit" if "mascot" in character_id else "pencil-test-colored"`. Add a code comment: *"Stub fallback only — production runs never hit this path. The folder-name inference is intentional-test-only: real Cy reads source-refs and infers register from the material."*

6. **Run the full test suite.** `pytest tests/ -v`. The 122 prior tests stay green. The prompt edits don't touch the contract layer; the stub-fallback edit doesn't change test fixtures because the test for `test_three_phase_clean_path_emits_five_artifacts` uses `_make_pass1_envelope` (a non-stub envelope), and stub-fallback tests don't assert on `style_register` value specifically.

7. **Commit:** `Task 1.4.5 — defang pencil-test bias in standing contexts (style-agnostic preambles)`

### Phase C — Task 1.4.6: ship the style-neutrality guardrail (~30-45 min)

Without a guardrail, the bias creeps back. Future prompt additions (new agent role addendums, new skill loads, edits to existing files) can reintroduce register-anchored language without anyone noticing until a non-pencil-test Bible authoring run fights the preamble. The guardrail catches it at test time.

**Specific tasks:**

1. **NEW `tests/test_prompt_style_neutrality.py`** — a unit test that asserts the standing-context preambles and shared anima context don't contain register-anchored language outside of explicitly-scaffolded example blocks. Implementation shape:

   ```python
   # The closed style-register vocabulary. Every register is fine to mention;
   # the failure mode is mentioning ONE register as if it were the default.
   _STYLE_REGISTERS = frozenset({
       "pencil-test-colored", "pixel-art-8bit", "line-art-only",
       "watercolor", "photoreal", "3d-rendered",
   })

   # Register-specific markers that, when found outside an example block,
   # signal default-register bias. The test fails if any of these appears in
   # the load-bearing preamble sections — the load-bearing sections being
   # the "what you must not do" / "what good looks like" / "the lens you bring"
   # blocks that drive Opus's seed behavior. Inside explicitly-scaffolded
   # `## What good looks like — {register}` example blocks the markers are
   # allowed because they're scoped to a named register.
   _PENCIL_MARKERS = frozenset({
       "cross-hatching", "construction lines", "graphite", "cream paper",
       "varied 1-3px", "pencil-test rough",
   })
   _PIXEL_MARKERS = frozenset({
       "dithering", "integer-pixel grid", "anti-aliasing",
       "closed palette",
   })
   ```

   The test parses each preamble file's markdown, identifies the load-bearing sections (everything outside `## What good looks like` example blocks), and asserts that any register-anchored marker found there is accompanied by at least one marker from a different register (proving the language is comparative, not default). If pencil-test markers appear without pixel-art / watercolor / photoreal companions, the test fails with a message naming the line and the missing companion register.

   The test runs against four files: `anima-standing-context.md`, `cy-character-designer-context.md`, `em-vision-critic-context.md`, `maya-planner-context.md`. The test is intentionally tolerant in the `## What good looks like` blocks — those are explicit examples and can ship single-register content; the bias prevention is for the load-bearing instruction sections.

2. **NEW `docs/prompt-style-neutrality-doctrine.md`** — a one-page studio-manual-voice doctrine note explaining the principle, the test, and the procedure for adding a new style register or a new prompt file. Sections:

   - **The principle.** anima is a 2D animation pipeline, not a pencil-test pipeline. The closed `style_register` vocabulary on `character.yaml` declares what the pipeline supports as first-class registers. Every prompt that drives agent behavior must work for every register in the vocabulary — *recognizably itself in its intended medium* is the engine truth, and the medium varies per character.

   - **The test.** `tests/test_prompt_style_neutrality.py` enforces the principle at CI time. Register-specific markers in load-bearing prompt sections must be paired with at least one cross-register example. Single-register examples belong in scaffolded `## What good looks like — {register}` blocks where the scope is named.

   - **Adding a new style register.** Three steps: (1) extend the closed vocabulary in `pipeline/criteria.py` (or wherever the validator lives) + add the value to `templates/bible/character.yaml.template`'s comment; (2) add a `## What good looks like — {register}` example block to `cy-character-designer-context.md` showing three sample IR.* entries and a four-paragraph risk-bible excerpt in the new register; (3) update `_STYLE_REGISTERS` in `tests/test_prompt_style_neutrality.py` and add register-specific markers to the marker frozensets if applicable. Commit with a message naming the new register and the rationale.

   - **Adding a new prompt file or editing an existing one.** Before commit, re-read the load-bearing sections with this question: *would this prompt make sense to a pixel-art Bible author? A watercolor Bible author? A 3d-rendered Bible author?* If the answer is no for any of the six registers, the prompt is biased — generalize it. The test catches obvious bias; the question catches subtler bias the test misses.

   - **What this doctrine doesn't apply to.** The pencil-test reference implementation (Act 1 + Act 2 work in flight) is allowed to be pencil-test-specific in its run-specific artifacts (briefs, manifests, run notes). The doctrine governs reusable infrastructure (prompts, schemas, templates), not single-piece production assets.

3. **Update `CLAUDE.md`** — add a one-line pointer to the new doctrine in the Source of Truth Documents table.

4. **Run `pytest tests/test_prompt_style_neutrality.py -v`** — expect 4 pass (one per audited file).

5. **Commit:** `Task 1.4.6 — style-neutrality guardrail (test + doctrine note)`

### Phase D — Task 1.10: the sean-anchor Bible authoring run (Sean-driven, ~30-60 min)

Per the existing plan's Task 1.10. Cy authors `characters/sean-anchor/` end-to-end from the source-refs material already on disk. **This is the bias-friendly case** — Sean IS pencil-test-colored, so the defang shouldn't change Cy's output meaningfully. The Bible should look the same with or without Phase B's edits. Use it as a control.

Follow the plan's source-ref mapping verbatim (lines 521-531). Review the emitted `character.yaml`, IR.* rules, risk-bible, cy-confidence-notes. Spot-check at least 5 Pass-3 Gemini verdicts. Approve via `pipeline bible approve`.

**One change to the plan's Task 1.10 source-ref mapping:** before copying source-refs into `characters/sean-anchor/source-refs/`, verify each file's intended destination with Sean — the plan's mapping is opinionated (which `Original-*` is the source line-art vs the derived plate, which `sprite-reference-{1..5}` belongs where) and Sean's intuitions about specific frames may differ. Five-minute pre-flight check; ask if unclear.

Commit per the plan: `Cy: characters/sean-anchor/ — first real Bible authored end-to-end`.

### Phase E — Task 1.11: the claude-mascot Bible authoring run (Sean-driven, ~30-60 min)

**This run IS the validation that the defang worked.** Per the existing plan's Task 1.11. Cy authors `characters/claude-mascot/` end-to-end against the `images/Claude-Mascot/` source-refs (pixel-art-8bit register).

After the run completes, check Cy's emitted Bible against the success criteria:

- `character.yaml`'s `style_register` field is `pixel-art-8bit` (NOT `pencil-test-colored` — if Cy defaulted to pencil-test, the defang failed and Phase B needs a deeper pass).
- The `IR.claude-mascot.*` rules describe pixel-art-appropriate markers — palette by hex / dithering patterns / integer-pixel grid / sub-1x silhouette readability. **None of them should mention cross-hatching, graphite gray line weight, paper texture, or construction lines.** If any of those appear, the defang didn't go deep enough and a second pass is needed before Task 1.12 lands.
- The `risk-bible.md` names the Bible's negative space in pixel-art terms (no motion plates yet, no expression set beyond default, no costume variations).
- The Pass-3 Gemini verdicts cite IR.claude-mascot.* rules specific to pixel-art — *"the dithering pattern in the shadow region honors `IR.claude-mascot.style.vertical-dither-2px-spacing`"* rather than generic *"the character looks consistent."*

**If the success criteria don't all hold:** stop, surface the gap to Sean, run a deeper defang pass before continuing. Don't ship a thinly-bias-fixed Bible — the closing-the-loop eval in Phase G is meaningless if the Bible's rules don't match the register.

**If the success criteria hold:** proceed to Phase F. The defang shipped. Sean reviews the Bible artifacts. Approve via `pipeline bible approve`.

Commit per the plan: `Cy: characters/claude-mascot/ — pixel-art-8bit second-character schema validation + defang verification`.

### Phase F — Task 1.12: commit 2 wrap-up (~30 min)

Per the existing plan's Task 1.12. CHANGELOG entry covering:

- All five TOP-5 decisions from the brainstorm (folder schema, IR.* namespace, three-phase AgentSpec, CLI surface, Project-Type routing)
- The two real Bibles authored (sean-anchor as pencil-test-colored, claude-mascot as pixel-art-8bit)
- **Task 1.4.5 — the defang pass.** Name the four files edited, the bias they carried, the fix shape. This is portfolio content — the audit + the fix is itself a documented case of "validators cannot recover taste that was absent at generation time" applied at the prompt layer, not just the Bible layer.
- **Task 1.4.6 — the style-neutrality guardrail.** Name the test file and the doctrine note. The guardrail prevents regression.
- The claude-mascot Bible's success against the post-defang success criteria — the validation that the architecture supports arbitrary 2D styles, not just pencil-test.
- Deferred items per brainstorm §7 (ROT1 walkthrough, ROT3 em-citation-cheatsheet, ROT5 comparison-strip — these are commit 6 surface; ROT4 LoRA seed plates shipped).
- The closing-the-loop test arc (red on first land in commit 2b; green when Em's prompt is tightened to load IR.* rules into context).
- Open assumptions to validate (the six items from the existing plan's §"Open assumptions" + add a seventh: *the style-neutrality guardrail's marker frozensets cover the bias modes the audit caught and don't false-positive on legitimate register comparisons*).

Update `CLAUDE.md` per the plan: Source of Truth Documents table, Skills Map (Cy under Phase 2), Directory Structure (`characters/sean-anchor/` and `characters/claude-mascot/` shipped), Key Commands, Asset Naming Convention.

Run full test suite: `pytest tests/ -v`. Expect 90 prior + 16 IR + 7 NB Pro + 9 Cy + 6 cost estimator + 7 CLI bible + 4 criteria_sources merge + 4 prompt style neutrality = ~143 green. (Adjust expected count per actual task ship.) Run planner eval suite: `pytest evals/planner/runner.py -v`. Expect prior baseline (5 passing + 1 xfailed) unchanged.

Commit per the plan: `Commit 2: Cy the Character Designer + two real Bibles + defang + guardrail + CHANGELOG/CLAUDE.md`.

### Phase G — Commit 2b: character-designer eval suite + closing-the-loop test (~1-2 evenings)

Per the existing plan's Phase 2 (Tasks 2.1 → 2.5). The eval-suite shape mirrors `evals/planner/`. The closing-the-loop test (Case 4) is the structural novelty — ships red on first land because Em's prompt doesn't yet load Cy's IR.* rules into context. The xfail-to-green diff in a follow-up commit (when Em's prompt is tightened) is the museum content documenting *the moment Bible authoring became contract-grounded*.

**One amendment to the existing plan's Task 2.2 case list:** because Task 1.4.5 + 1.4.6 shipped a style-neutrality guardrail, the existing Case 5 (`schema-validation-cross-style-registers`) gains structural weight — it's no longer just a schema check; it's verification that the merged CriteriaBundle works across the two distinct registers Sean's now authored. Update the case description to reflect this. The assertion structure stays the same: `query_by_character("sean-anchor")` returns sean's rules only; `query_by_character("claude-mascot")` returns claude-mascot's rules only; no ID collisions; both validate against the closed vocabularies.

Final commit per the plan: `Commit 2b: character-designer eval suite + closing-the-loop test (red-on-first-land)`.

## Working pattern + constraints

- **v2's architecture decisions are LOCKED.** Cy's persona, model assignment, and the three structural patterns from v2 §5 are not for redecision. The defang doesn't touch the architecture — it removes default-register bias from prompts that the architecture is supposed to drive.
- **The Cowork preamble's three structural splits from the previous session are LOCKED.** Cy-leads-Sean-reviews workflow, both Project-Types ship day one, symlink at the legacy anchor path through commit 7.
- **Studio-manual voice in every doc edit.** The defang IS a voice edit — the studio-manual register stays; the pencil-test default register stops being default. Read each prompt edit and ask: *does this still read as a working studio's role description?* If it reads as a schema doc or a CLI man page, rewrite.
- **Don't disturb Act 2 work.** The pencil-test reference implementation runs against the legacy anchor path through the symlink. The doctrine note explicitly carves out the pencil-test reference implementation from the style-neutrality discipline — run-specific artifacts (briefs, manifests, notes) can be register-specific; the reusable infrastructure (prompts, schemas, templates, tests) cannot.
- **Mirror, don't reinvent.** The Phase A tasks lift verbatim from the existing plan — don't redesign them. The defang in Phase B is surgical — name the lines, replace the language, preserve the structure. The guardrail in Phase C is a unit test + a doctrine note — no new infrastructure.
- **Stage-first, never auto-apply.** All four prompt edits commit as single discrete commits. The bible mutations (Phase D + E approval ceremonies) follow the Maya pattern — `--force --actor --reason` required after lock.
- **Use plan mode for the multi-file shape, then execute.** Phase A touches 5 new files + 3 modified files. Phase B touches 5 prompt files + 1 stub-fallback edit. Phase C touches 2 new files + 1 modified file. Plan mode catches cross-file consistency issues before they ship.

## End-of-session deliverables

1. **Phase A commits** — Tasks 1.6 / 1.7 / 1.8 / 1.9 land as four separate commits per the existing plan.
2. **Phase B commit** — Task 1.4.5 lands as one commit named `Task 1.4.5 — defang pencil-test bias in standing contexts (style-agnostic preambles)`.
3. **Phase C commit** — Task 1.4.6 lands as one commit named `Task 1.4.6 — style-neutrality guardrail (test + doctrine note)`.
4. **Phase D + E commits** — sean-anchor and claude-mascot Bibles, two commits per the existing plan.
5. **Phase F commit** — commit 2 wrap-up with CHANGELOG + CLAUDE.md updates.
6. **Phase G commits** — Phase 2 eval suite + closing-the-loop test (5 Task-2.* commits per the existing plan).
7. **Updated CLAUDE.md** — Skills Map row for Cy, Directory Structure showing two shipped Bibles, Source of Truth Documents pointing at the new doctrine, Key Commands showing the bible CLI.
8. **Test suite green at ~143 + Phase 2 evals running 5 pass + 2 xfail.**
9. **Optional: a brief Cowork continuation prompt** if Sean wants to brainstorm commit 5 (Draft → Pro tier escalation), commit 6 (Museum capture + Mo persona), or commit 9 (T3 stack) next.

## Verification (end-to-end, post-Phase G)

```bash
# Schema verification
pytest tests/test_criteria_ir_namespace.py -v
python -c "from pipeline.criteria import load_criteria; b = load_criteria('characters/sean-anchor/acceptance_criteria.json'); print(f'{len(b.criteria)} criteria loaded; first ID: {b.criteria[0].id}')"
python -c "from pipeline.criteria import load_criteria; b = load_criteria('characters/claude-mascot/acceptance_criteria.json'); print(f'{len(b.criteria)} criteria loaded; first ID: {b.criteria[0].id}')"

# AgentSpec verification
pytest tests/test_character_designer.py -v
pytest tests/test_nb_pro_runner.py -v

# Defang verification
pytest tests/test_prompt_style_neutrality.py -v   # 4 pass
grep -c "pencil" pipeline/agents/prompts/anima-standing-context.md  # should drop relative to pre-defang count
grep -c "pencil" pipeline/agents/prompts/cy-character-designer-context.md  # should NOT drop (pencil-test example block stays) but the load-bearing sections shouldn't anchor
grep -c "pixel-art-8bit" pipeline/agents/prompts/cy-character-designer-context.md  # should rise (new example block added)

# CLI verification
python -m pipeline.cli bible --help
python -m pipeline.cli bible show --character-dir characters/sean-anchor/
python -m pipeline.cli bible show --character-dir characters/claude-mascot/   # pixel-art Bible renders without trying to render boxes around graphite-gray callouts

# Eval suite
pytest evals/planner/runner.py -v               # prior baseline unchanged (5 pass + 1 xfail)
pytest evals/character-designer/runner.py -v    # new suite, expected 5 pass + 2 xfail

# Full test suite
pytest tests/ -v                                 # ~143 green (122 prior + new from Tasks 1.6/1.7/1.8/1.9/1.4.5/1.4.6)
```

The claude-mascot Bible's `character.yaml` is the load-bearing visual confirmation that the defang worked. If `style_register: pixel-art-8bit` and the IR.* rules describe pixel-art markers without contaminating pencil-test vocabulary, the architecture supports arbitrary 2D styles as designed.

## Why this matters (the broader stake)

anima is a 2D animation pipeline, not a pencil-test pipeline. Sean's portfolio thesis depends on this distinction — the pipeline ships a *working method* that handles whatever 2D character Sean (or anyone using anima) decides to make. The pencil-test reference implementation is the first proof of concept, not the project's identity. Without the defang, the prompts silently coerce every character into pencil-test patterns, which means the pipeline silently fails the watercolor character, the line-art-only character, the 3d-rendered character, the photoreal character, and yes — the pixel-art-8bit character that's about to land as Sean's claude-mascot Bible.

The guardrail in Phase C is the structural fix synthesis §5 demands applied at the prompt layer. The validator already catches schema bias (the closed `style_register` vocabulary, the closed IR.* category vocabulary). The new test catches prompt bias (default-register anchoring in load-bearing instruction blocks). The doctrine note is the human-readable companion that explains the principle to future contributors (or future Sean, six months from now, having forgotten which decisions are load-bearing).

The discovery — Sean caught the bias during a pacing-pause review before the claude-mascot run surfaced it as a Bible authoring failure — is itself portfolio content. It's the "verification addendum as load-bearing artifact" pattern from `PORTFOLIO-GOLD.md`, applied to prompts: when the world contradicts the prompt, the prompt gets an audit, not a workaround.

## Start

1. Read the binding docs in the listed order. Pay particular attention to the audit findings section above — the four files + the specific line numbers are the surgical targets.
2. Plan mode for Phase A (Tasks 1.6 → 1.7 → 1.8 → 1.9). Write the plan first; execute against the plan. Each task lands its own commit.
3. Phase B — Task 1.4.5 — the defang. Surgical edits per the audit. Test suite stays green.
4. Phase C — Task 1.4.6 — the guardrail. Test + doctrine.
5. Phase D — sean-anchor Bible (Sean-driven). Control case.
6. Phase E — claude-mascot Bible (Sean-driven). Validation case. **If success criteria don't hold, stop and run a deeper defang.**
7. Phase F — commit 2 wrap-up.
8. Phase G — Phase 2 eval suite + closing-the-loop test.

Net wall-clock estimate: 4-6 hours for Phase A, 45-60 min for Phase B, 30-45 min for Phase C, 30-60 min each for Phase D and Phase E (Sean-driven so actual time varies), 30 min for Phase F, 1-2 evenings for Phase G. Total: roughly 7-10 hours of focused work plus the two Bible authoring ceremonies, plus the Phase G coda.

---

*The architecture is sound. The contracts are clean. The prompts now carry the same style-agnostic discipline the validator already enforces. The guardrail catches regression. The claude-mascot Bible is the validation. anima ships as a 2D animation pipeline, not a pencil-test pipeline — which is what it was always supposed to be.*
