# Implementation Prompt — Cy the Character Designer (Commits 2 + 2b)

**Created:** 2026-05-27
**For:** The next Claude Code execution session (plan mode, multi-file edits, git).
**Workstream:** anima Phase 2 — Character Bible. Implement the `characters/{character_id}/` folder schema, Cy's three-phase AgentSpec (Opus authors + NB Pro generates + Gemini verifies), the `IR.*` namespace extension to `acceptance_criteria.json`, the bible CLI surface, the project-type routing through Maya, the migration of the pencil-test anchor, the second-character Claude-mascot Bible as validation, and the closing-the-loop eval that proves Em can cite Cy's rules at T2-critic time.
**Reads as:** Studio-manual voice, prose where reasonable. Sean's exact tonal directive — *"I don't like it when the docs feel like it was strictly made for the terminal. We're making art. It should feel free."*

---

You're picking up the anima project after a Cowork brainstorm session shipped two artifacts. anima is a reusable human + AI 2D animation production pipeline at `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/`. The architecture and agent fleet are locked in v2; commits 3 + 3b + 8 + 8.1 + 8.1a all shipped on a feature branch — Maya the planner, the planner eval suite, Em the vision critic, the Antigravity CLI rename + flag-shape corrections, and the sdk_runners refactor against the real claude-agent-sdk v0.2.x API. Test suite stands at 90 green + 5 passing / 1 xfailed in `evals/planner/`. Maya and Em both run live against real Opus and real Gemini 3.1 Pro respectively.

The Cowork brainstorm ran a `pm-product-discovery:brainstorm-ideas-existing` pass on commit 2 (Cy and the Character Bible) and converged on five locked decisions written up at [`docs/2026-05-27-cy-character-bible-brainstorm.md`](2026-05-27-cy-character-bible-brainstorm.md). It also surveyed the on-disk character-reference material at `images/NEW-ANIMATION-PIPELINE/`, `images/Claude-Mascot/`, `images/Sprite-reference/`, `images/3D-Character-Reference-Test/`, `images/head-turn/`, and `references/visual-guides/` and surfaced two structural findings the v1 change-map sketch had missed: motion plates are a sixth Bible category (walk cycle, head turn — neither expressions nor turnarounds), and aesthetic style register is a Bible-level top-level attribute (pencil-test-colored Sean vs pixel-art-8bit Claude mascot would route to categorically different Phase 5 models if style register were a downstream prompt detail). This session implements those decisions.

The Cowork preamble also resolved three structural splits before the brainstorm proper:
- **Workflow is Cy-leads, Sean-reviews** — Cy drafts identity rules + candidate Bible directory; Sean reviews via `pipeline bible show`, approves, edits with `pipeline bible mutate`. Mirrors Maya verbatim.
- **Commit 2 ships both Project-Types day one** — Bible-authoring and animation-piece both routable from Maya. Resolves v2 Open Q6.
- **Symlink at the legacy anchor path through commit 7** — long-enough back-compat that no Act 2 session breaks; short enough that the symlink isn't permanent.

## Read these binding docs first, in this order

Philosophy before architecture before brainstorm output. Don't skip ahead.

1. [`PHILOSOPHY.md`](../../../PHILOSOPHY.md) — the load-bearing intent doc, six load-bearing beliefs. Sean's quotes on tone (*"we're making art, it should feel free"*) and on the critic (*"a judge agent will be a staple in all of my agentic workflows from here on out"*) preserved verbatim. Both load-bearing for this session — Cy's verification half IS a judge agent at the Bible layer.
2. [`CLAUDE.md`](../../../CLAUDE.md) — anima project manual, current state post-commits 3 + 3b + 8.1a.
3. [`docs/2026-05-27-cy-character-bible-brainstorm.md`](2026-05-27-cy-character-bible-brainstorm.md) — the brainstorm artifact this session implements. Top 5 in §6, deferred items in §7, the explicit "what commit 2 looks like" file map in §8.
4. [`docs/2026-05-26-agent-fleet-brainstorm-v2.md`](../agent-fleet/2026-05-26-agent-fleet-brainstorm-v2.md) — the v2 architecture lock, especially §2.1 (Cy as the missed pinnacle phase — the headline finding), §6 (Cy's per-role assignment at 92% confidence — the highest non-Chairman seat), §11 (Phase 2 wiring in the architecture-implied strawman).
5. [`docs/research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md`](../../research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md) — cross-source synthesis grounding v2. §5 names Cy as *the single most important decision Sean was about to get wrong if he shipped v1*. Read for why the Bible-as-cross-phase-invariant thesis earned the headline.
6. [`docs/Image-Model-DR-2026/SYNTHESIS.md`](../../Image-Model-DR-2026/SYNTHESIS.md) — Phase 5 image-model router source. NB Pro for hero shots is Cy's plate-generation tier per v2 §6.
7. [`docs/pipeline-architecture-v1.md`](../../architecture/pipeline-architecture-v1.md) — canonical 10-phase architecture, especially Phase 2 spec.
8. [`docs/2026-05-24-pipeline-v2-change-map.md`](../pipeline-v2/2026-05-24-pipeline-v2-change-map.md) §2 TOP-5 (the original folder-shape sketch the brainstorm extended) + §4 (Commit 2 in the sequence — independent of DAG, low-risk, immediately useful).
9. [`docs/2026-05-26-maya-planner-brainstorm.md`](../../design/2026-05-26-maya-planner-brainstorm.md) + [`docs/2026-05-26-maya-planner-implementation-prompt.md`](../maya/2026-05-26-maya-planner-implementation-prompt.md) — the structural templates Cy's artifacts mirror. The lift-from-Maya pattern is named in brainstorm TOP-3 and TOP-4 explicitly.
10. [`docs/research/2026-05-26-anti-gravity-cli-findings.md`](../../research/2026-05-26-anti-gravity-cli-findings.md) — the Antigravity CLI findings doc with the 2026-05-27 verification addendum. Cy's Pass-3 Gemini verification uses the same corrected `agy` incantation Em uses; no new CLI work.
11. [`CHANGELOG.md`](../../../CHANGELOG.md) — recent entries (top of the file).

## Reference implementations to ground every contract against

- `pipeline/agents/__init__.py` + `pipeline/agents/planner.py` — Maya's AgentSpec implementation. Cy's `character_designer.py` follows the same three-phase shape (Opus authors → second-model-tier executes → third-model-tier verifies). Pass 1 lifts directly from Maya's Pass 1 Opus call.
- `pipeline/agents/vision_critic.py` + `pipeline/agents/cli_runners.py` — Em's commit 8 + 8.1a implementation. Cy's Pass 3 is structurally adjacent to Em — same `agy` wrapper, same JSON-in-prompt contract, same `{verdict, reasoning, confidence, cites_*}` envelope. Lift verbatim.
- `pipeline/agents/prompts/maya-planner-context.md` + `pipeline/agents/prompts/em-vision-critic-context.md` + `pipeline/agents/prompts/anima-standing-context.md` — the standing-context preamble pattern. Cy gets her own role addendum in the same shape; the addendum loads the `2d-animation-principles` skill verbatim (per brainstorm ENG5, folded into TOP-3).
- `pipeline/criteria.py` — commit 3's v1.1 graph-shaped schema. This session extends it with the `character_id` field and the extended `derived_from` plate-region pointer syntax from brainstorm TOP-2. Keep `criteria_locked: true` enforcement intact; the `IR.*` namespace lives inside the broader `AC.*` graph.
- `pipeline/cli/plan.py` — Maya's `plan init / show / approve / mutate` subcommand template. The new `pipeline/cli/bible.py` follows the same shape with one extra subcommand: `iterate` (the reject-aware regeneration loop from brainstorm DES5).
- `pipeline/agents/patch_stager.py` — commit 8's post_run hook pattern. Cy's plate-regeneration loop uses the same atomic-write idiom for cache files.
- `tests/test_planner.py` + `evals/planner/runner.py` + `evals/planner/README.md` — the test and eval-suite patterns Cy's commit 2b mirrors. The closing-the-loop eval (brainstorm TOP-5) is the structural novelty; everything else is the planner template applied to character design.
- `images/2D-Character-Sketch-Sean-v1.png` — the load-bearing pencil-test anchor. Migrates to `characters/sean-anchor/anchor.png` in Phase 0 of this session.
- `images/NEW-ANIMATION-PIPELINE/` — the input material for Cy's first real Bible authoring run. The brainstorm surveyed it in detail; consult §1 + the file map in §8 before commit 2 implementation starts.
- `images/Claude-Mascot/` — the source refs for Cy's second-character validation Bible. Pixel-art-8bit register; different palette vocabulary; same schema.

## Your job this session — three phases

### Phase 0 — Sean-anchor migration (warmup, ~30 minutes)

**Goal.** Move the existing pencil-test anchor into the new Bible folder structure with a back-compat symlink, so all subsequent Phase 1 work has a real `characters/sean-anchor/` directory to write into.

**Specific tasks.**

1. **Verify the legacy path one last time.** Run `git log --oneline -- images/2D-Character-Sketch-Sean-v1.png | head -5` to confirm the anchor's history is what's expected. Capture for the CHANGELOG entry.
2. **Create the new directory structure** per brainstorm TOP-1's schema (anchor / turnarounds / expressions / motion_plates / costumes / props / source-refs). Empty placeholders are fine — Cy populates them in Phase 1.
3. **`git mv images/2D-Character-Sketch-Sean-v1.png characters/sean-anchor/anchor.png`** — preserve git history. Don't `cp` — the renamed-file blame trail is portfolio content.
4. **Create the symlink at the legacy path.** `cd images && ln -s ../characters/sean-anchor/anchor.png 2D-Character-Sketch-Sean-v1.png` so any pencil-test script still works during the back-compat window. Document the symlink in CLAUDE.md's File map section + add a removal-trigger note pointing at commit 7.
5. **Verify the pencil-test Act 2 work still resolves.** Run `python3 pipeline/generate.py --help` and `python3 pipeline/audit.py --help` smoke tests. If anything errors on the missing path, the symlink isn't resolving — check first.
6. **Update manifest.yaml's `anchor:` reference** from the legacy path to the new path. Keep additive — Act 2 work in flight runs against the new path through the symlink unchanged.
7. **Commit as `commit 2.0 — sean-anchor migration with back-compat symlink`** with a CHANGELOG entry naming the symlink and the commit-7 removal trigger.

### Phase 1 — Commit 2 (the main event)

**Goal.** Implement Cy the Character Designer per the brainstorm's converged Top 5. The five locked ideas:

- **TOP-1** — `characters/{character_id}/` folder schema with motion_plates/ as a sixth category and source/derived/ split inside motion plates. `character.yaml` carries `style_register` (closed vocabulary: `pencil-test-colored | pixel-art-8bit | line-art-only | watercolor | photoreal | 3d-rendered`) as a top-level field Em loads *before* identity rules and Flo reads when routing Phase 5 generation. `flux_lora_seed_plates` field added per ROT4 (informational, anticipates Image-Model-DR Experiment 1).
- **TOP-2** — Identity rules extend `acceptance_criteria.json` with `IR.{character_id}.{category}.{specific-handle}` namespace inside the broader `AC.*` graph. Category vocabulary closed: `anatomy / hair / face / proportion / palette / costume / prop / pose / motion / style`. Each entry carries `character_id` and `derived_from: characters/sean-anchor/turnarounds/body-front.png#region:hair`. Impact tags from the same closed vocabulary Maya uses; Em's escalation hatch fires on Cy's rules unchanged.
- **TOP-3** — Cy as three-phase AgentSpec mirroring Maya. Pass 1 Opus authors `character.yaml` + `IR.*` graph entries + `risk-bible.md` + `cy-confidence-notes.md` + a structured plate-generation plan. Pass 2 NB Pro generates plates per the plan, content-addressed cached. Pass 3 Gemini 3.1 Pro via `agy` verifies every plate, regeneration loop with three-attempt ceiling per plate. Total cost ~$3-5 in NB Pro + zero incremental Opus + Gemini.
- **TOP-4** — `pipeline bible init / show / approve / mutate / iterate` CLI mirrors Maya's plan CLI. `init` scaffolds the folder structure + `0-sean-author-this.md` checklist. `show` is the Python rendering layer (boxes in the renderer, never on disk). `approve` locks the `IR.{character_id}.*` namespace. `mutate --force --actor --reason` writes to `runs/{run_id}/bible_audit.jsonl`. `iterate` is the reject-aware regeneration loop — Cy-specific extension because Cy generates plates while Maya doesn't.
- **TOP-5** — Bible-authoring as a Maya Project-Type. `01_production_brief.md` template gains `project_type: bible_authoring | animation_piece`. When `bible_authoring`, Maya's plan skips Phases 3-9. Plus the closing-the-loop eval (lands in commit 2b) — Em must cite Cy's `IR.*` rules during a T2 critique on a deliberately-broken Phase 5 frame.

**Specific tasks.**

1. **Read the brainstorm's §6 Top 5 + §8 file map carefully.** Every file listed in §8 is in scope; everything else is deferred.
2. **NEW `pipeline/agents/character_designer.py`** — Cy's AgentSpec implementation. Three-phase flow inside `run()`. Pass 1 uses `pipeline/agents/sdk_runners.py:invoke_opus_text` (already extended in commit 3 for Maya). Pass 2 calls NB Pro via Flo's routing — *if Flo isn't yet implemented as a callable AgentSpec at the time of this session*, ship Cy's Pass 2 against a direct NB Pro wrapper at `pipeline/agents/nb_pro_runner.py` (mirroring `pipeline/agents/cli_runners.py`'s shape) and leave the Flo migration as a commit-5+ follow-up. Pass 3 calls `pipeline/agents/cli_runners.py:run_antigravity_with_image` directly — same wrapper Em uses, no new CLI code. Three-attempt ceiling per plate guarded by an explicit counter. Stub-fallback ladder mirrors Maya's three-call stub pattern.
3. **NEW `pipeline/agents/prompts/cy-character-designer-context.md`** — standing-context preamble for Cy. Mirror the structure of `maya-planner-context.md`. Sections to include: persona introduction (character designer), how Cy consumes the Studio Brief + source-refs directory, the `IR.*` graph schema with mnemonic ID convention and a sample entry, the three-phase flow contract, the closing-the-loop expectation (Em must be able to cite the rules Cy emits — the rules' specificity is what makes Em's verdicts grounded). Load the `2d-animation-principles` skill verbatim as an inline appendix per ENG5. Studio-manual voice throughout — pretend you're writing the role description for a real animation-studio character designer.
4. **EXTEND `pipeline/criteria.py`** — add `character_id` as an optional field on `AcceptanceCriterion` (defaults to None for non-character criteria). Extend the `derived_from` parser to handle the `#region:X` plate-pointer syntax. Validate the closed `IR.*` category vocabulary (`anatomy / hair / face / proportion / palette / costume / prop / pose / motion / style`). Add `CriteriaBundle.query_by_character(character_id)` accessor. Keep backward compatibility with v1.1 — Maya's existing `AC.*` criteria continue to validate.
5. **EXTEND `pipeline/agents/cost_estimator.py`** — add a Phase 2 row with NB Pro plate-authoring spend. The estimator reads the per-character plate-generation plan from Cy's Pass-1 envelope and prices accordingly. ~$0.15 per plate × ~20-30 plates per Bible = $3-5 per Bible. Subscription-absorbed Opus + Gemini contribute $0.
6. **NEW `pipeline/agents/nb_pro_runner.py`** — direct NB Pro wrapper if Flo isn't yet a callable AgentSpec. Mirror `pipeline/agents/cli_runners.py`'s shape: takes (prompt, reference_images, output_path); returns a `NBProResponse` with the generated plate path + the content-addressed cache key. Content-addressed cache lives at `runs/{run_id}/cache/nb_pro/{sha256}.png` per node invocation. Cache key includes the identity rules cited in the prompt + the reference-image hashes + the prompt text — `cy iterate` reject regenerations invalidate by appending the reject-reason to the prompt text, which changes the hash.
7. **NEW `pipeline/cli/bible.py`** — `pipeline bible init / show / approve / mutate / iterate` subcommands. Mirror `pipeline/cli/plan.py`'s structure. The `mutate` command writes to `runs/{run_id}/bible_audit.jsonl` atomically (temp-then-rename idiom from `pipeline/agents/patch_stager.py`). The `show` rendering layer parses the Bible directory and paints a terminal tear sheet — character header, anchor thumbnail (path + placeholder ASCII), palette swatch line (color blocks rendered with ANSI background), identity rules grouped by category with their plate refs, motion-plate inventory, risks, hedges. **Boxes live in the renderer, never on disk.**
8. **NEW `templates/bible/character.yaml.template`** — anchored template with all top-level fields: `character_id`, `display_name`, `style_register` (closed vocabulary documented in the comment), `palette` (named-color list), `proportions` (head-to-body ratio + key landmarks), `identity_rules_pointer` (path to the `IR.*` entries in `acceptance_criteria.json`), `cy_confidence_notes` (prose section), `flux_lora_seed_plates` (informational seed list for future LoRA training), `risks` (pointer to `risk-bible.md`). Studio-manual voice — comments read like a real character bible template, not a YAML schema doc.
9. **NEW `templates/bible/source-refs-checklist.md`** — the `0-sean-author-this.md` content. Asks Sean to drop: anchor image, turnaround sheet if he has one, motion refs if he has any, 3D mannequin or pose refs if he has any, voice/mood notes. One-page; opinionated defaults.
10. **REGISTER the new node** in `pipeline/agents/__init__.py` via `@register_node("character_designer")`. If Flo doesn't yet exist, register `@register_node("nb_pro_runner")` for the direct wrapper.
11. **EXTEND `templates/brief/01_production_brief.md`** — add `project_type: bible_authoring | animation_piece` to the YAML frontmatter. Document in the comment that `bible_authoring` makes Maya skip Phases 3-9 and ship a Bible as the deliverable.
12. **EXTEND `pipeline/agents/planner.py`** — Maya's plan routing honors `project_type`. When `bible_authoring`, the plan structurally includes Phase 0 + Phase 2 only and routes Phase 2 to Cy. When `animation_piece`, behavior is unchanged from commit 3.
13. **MANIFEST schema extension** — `characters:` block points at the active Bible directories. Keep additive; Act 2 work continues unchanged. The `anchor:` field (now pointing at the symlink target) coexists with the new `characters:` block during the back-compat window.
14. **REAL BIBLE AUTHORING — `characters/sean-anchor/`.** Run Cy end-to-end against the existing material. Source refs come from `images/NEW-ANIMATION-PIPELINE/` (anchor-1.png, sean-character-turnaround-2.png, sean-head-turn-1.png, sean-walk-cycle.png, the Original-* line-art versions) + `images/Sprite-reference/` + `images/3D-Character-Reference-Test/`. The first real Bible is the most load-bearing portfolio artifact this session ships — Cy's authoring run produces the canonical Sean character Bible the rest of anima will reference.
15. **REAL BIBLE AUTHORING — `characters/claude-mascot/`.** Run Cy end-to-end against the `images/Claude-Mascot/` source refs. The second character validates the schema against a categorically different style register (pixel-art-8bit vs pencil-test-colored). If anything in the schema is single-case-biased toward Sean, this is where it surfaces.
16. **Run the full test suite.** Add new tests; don't reduce the green count. Cy's three-phase loop gets its own test coverage (AgentSpec conformance, four-artifact emission, clean Pass-3 path, Gemini-flag-then-regenerate path, three-attempt-ceiling path, clean-markdown invariant, missing-source-refs precondition).
17. **Commit as `commit 2 — Cy the Character Designer + two real Bibles`** with a CHANGELOG entry covering all five Top-5 decisions, the deferred items, the two real Bibles authored, the schema validations across the two style registers, and the open assumptions to validate.

### Phase 2 — Commit 2b (the eval suite)

**Goal.** Mirror the commit 3b pattern. Plant the character-designer eval suite that catches Cy's regression failures AND lands the closing-the-loop test (TOP-5) that proves Em can cite Cy's rules at T2-critic time. The closing-the-loop diff (red → green) is the museum content that documents the moment Bible authoring became contract-grounded.

**Specific tasks.**

1. **NEW `evals/character-designer/cases.yaml`** — 5-7 seed cases. At minimum: (a) a sean-anchor Bible reproduction case (clean Pass-3, three-call ceiling not hit), (b) a Gemini-flags-three-plates case (regeneration loop exercises), (c) a three-attempt-ceiling case (one plate that converges only on the third attempt — failure-mode anchor), (d) the closing-the-loop case (Em cites Cy's IR.* rules on a deliberately-broken Phase 5 frame), (e) the schema-validation case (IR.* namespace inside the AC.* graph parses correctly across both characters), (f) the deliberately-red under-specified-source-refs case (Cy's risk-bible flags the gaps, doesn't silently ship a thin Bible). Mirror `evals/planner/cases.yaml` structurally.
2. **NEW `evals/character-designer/runner.py`** — pytest harness. Lift the shape from `evals/planner/runner.py`. The closing-the-loop case calls Em directly via `pipeline/agents/vision_critic.py:VisionCriticNode.run()` against the broken-frame fixture and asserts on Em's verdict envelope's `cites_criteria` list — it must contain at least one `IR.sean.*` entry. Intentionally-red cases get `pytest.mark.xfail` markers per the change-map §7 discipline.
3. **NEW `evals/character-designer/conftest.py`** — shared fixtures. The deliberately-broken Phase 5 frame for the closing-the-loop test is the load-bearing fixture — pre-generated once via a manual NB Pro run, committed to the fixtures directory, ~1MB committed to git is acceptable for this single load-bearing artifact.
4. **NEW `evals/character-designer/fixtures/`** — three fixture source-refs directories (well-specified / under-specified / multi-character) plus the deliberately-broken Phase 5 frame. The well-specified fixture mirrors `images/NEW-ANIMATION-PIPELINE/`'s actual contents; the under-specified strips out the motion plates; the multi-character bundles sean-anchor + claude-mascot source refs together.
5. **NEW `evals/character-designer/failure-modes.md`** — observed failure taxonomy. Start with four: `identity-rule-too-generic-to-cite` (caught by the closing-the-loop test — Em can't cite a vague rule), `plate-passes-gemini-but-drifts-from-source-refs` (Gemini approves a plate that doesn't match Sean's actual references — caught by Sean's review), `motion-plate-source-derived-mismatch` (the source line-art and the derived plate don't align — Em flags), `em-cannot-cite-cy-rules-at-T2-critic` (the structural-fix-at-the-source failure — the closing-the-loop test's xfail-then-pass arc IS the regression test for this).
6. **NEW `evals/character-designer/last-run.md`** — baseline trace. First run includes the closing-the-loop test as red (Cy ships, Em can't yet cite IR.* rules because Em's prompt doesn't load Cy's rules into context). Subsequent commits tighten Em's prompt to load Cy's rules and the test flips green. The diff is portfolio content.
7. **NEW `evals/character-designer/README.md`** — portfolio-grade write-up. Mirror `evals/planner/README.md`. Name the closing-the-loop test as the structural novelty over the planner eval suite — *why* it exists, *what* it proves, the synthesis §5 thesis it operationalizes. This README is itself a museum artifact.
8. **Run the eval suite.** Expect mixed pass/fail with the closing-the-loop test red on first land. The xfail-then-pass arc across the next commit (when Em's prompt is tightened to load Cy's rules) is the eval discipline made operational.
9. **Commit as `commit 2b — character-designer eval suite + closing-the-loop test`** with a CHANGELOG entry naming the red-to-green arc as the structural fix synthesis §5 demands.

## Working pattern + constraints

- **v2's architecture decisions are LOCKED.** Cy's persona, model assignment (Opus authors + NB Pro generates + Gemini verifies), and the three structural patterns from v2 §5 are not for redecision in this session. If something seems wrong on fresh reading, flag it as a question — don't silently correct.
- **The Cowork preamble's three structural splits are LOCKED.** Cy-leads-Sean-reviews workflow, commit 2 ships both Project-Types day one, symlink at the legacy anchor path through commit 7. These are not for re-decision either.
- **Studio-manual voice in every doc.** Sean's exact tonal directive — *"we're making art, it should feel free."* Prose where reasonable. Tables only for genuine reference data. The CHANGELOG entry, the READMEs, the standing-context preamble, the inline code comments, the CLI output, the bible.yaml template — all in studio voice.
- **Don't disturb Act 2 work.** The pencil-test reference implementation runs against the legacy anchor path through the symlink. Manifest schema additions are additive. The new `characters:` block coexists with the existing `anchor:` reference (which now resolves through the symlink to the migrated file).
- **Mirror, don't reinvent.** Maya (commit 3) is the structural template for Cy. Em (commit 8 + 8.1a) is the structural template for Cy's Pass 3. cli_runners.py + sdk_runners.py + the patch_stager hook + the standing-context preamble pattern + the CLI subcommand shape + the eval-suite shape all carry over. Read those files before writing equivalent code.
- **Stage-first, never auto-apply.** Per v2 §2.5: Sean approves Bibles, mutates rules with `--force`, locks with `criteria_locked: true`. The runner refuses mutation after lock without `--force --actor --reason`. Mirror commit 4's enforcement.
- **The two real Bibles are not optional.** Authoring `characters/sean-anchor/` and `characters/claude-mascot/` end-to-end in this session is the validation that the schema works against actual diversity. Skipping this and shipping schema-only would carry forward the same single-case bias the v1 sketch had.
- **Use plan mode for the multi-file shape, then execute.** Commit 2 touches roughly 12 new files + 4 extended files. Plan mode catches the cross-file consistency issues before they ship.
- **End-of-session deliverables.** (1) Commit 2.0 — sean-anchor migration with back-compat symlink. (2) Commit 2 — Cy the Character Designer + two real Bibles. (3) Commit 2b — character-designer eval suite + closing-the-loop test. (4) CHANGELOG entries for each. (5) An updated `CLAUDE.md` if any architectural detail moves (most likely the "Active phase" pointer, the Skills Map's character_designer row, the source-of-truth table). (6) Optional: a brief Cowork continuation prompt if Sean wants to brainstorm commit 5 (Draft → Pro tier escalation runtime), commit 6 (Museum capture layer + Mo persona), or commit 9 (Codie + Annie + Sage + Chairman at T3) next.

## Remaining work after this session (for context)

- **Commit 5 — Draft → Pro tier escalation wired into the DAG runner.** Depends on commit 3's cost estimator (shipped) and Cy's Bible-aware generation plan (shipping this session — Cy's plate plan is naturally draft/pro tiered).
- **Commit 6 — Museum capture layer + Mo persona + Astro content-collection integration.** Pending its own brainstorm. ROT1's `bible-walkthrough.md` and ROT5's `comparison-strip.png` promoted to museum surfaces in commit 6.
- **Commit 7 — Animatic ingestion (Procreate Dreams + Procreate PNG sequences).** Triggers the symlink-removal cleanup the warmup left as a tracked todo.
- **Commit 9 + 9b — Codie + Annie + Sage + Chairman at T3 + eval suite + standing-context ablation.** Annie's wrapper inherits commit 8.1a's flag shape directly. Sage / Codie / Chairman / Annie are all structurally similar to existing patterns.
- **Phase 5 Flo persona + per-shot routing wired in.** ENG2's `character_id` field on criteria is the connection point — when Flo generates a Phase 5 frame for a shot involving Sean, the routing reads Cy's `IR.sean.*` rules and the `style_register` to pick the right model. Pre-Flo, the `cy iterate` regeneration loop demonstrates the contract works in isolation.
- **First real Bible-authoring Maya run end-to-end** — Maya plans a Bible for a hypothetical third character (or the next character Sean wants to ship). Portfolio-grade first Bible-authoring ceremony.

Post-implementation bake-offs (from v2 §8) — not gating commit 2, but informing future tuning:

1. T2 critic shoot-out (Gemini vs Sonnet vs Opus on a 200-frame defect set, with Cy's rules loaded)
2. Sage tier ablation
3. Planner downgrade ablation
4. Orchestrator drift test
5. Storyboard three-way bake-off
6. DeepSeek V4 Flash as candidate fourth T3 peer

## Start

1. Read the binding docs in the listed order.
2. Begin Phase 0 — the sean-anchor migration. The `git mv` + symlink + manifest update should take 15 minutes; the verification smoke tests should take 15.
3. Plan mode for Phase 1 — commit 2. Write the plan first; execute against the plan. The two real Bibles authoring runs are the load-bearing portfolio artifacts; budget time accordingly.
4. Phase 2 — commit 2b — lands as a coda once commit 2 is green. The closing-the-loop test is the structural novelty; ship it red and let the diff become museum content.

Net wall-clock estimate: 5-7 evenings for commit 2, 1-2 evenings for commit 2b, 30 minutes for the warmup. The two real Bible authoring runs are the variable — Pass-1 Opus prompt iteration on the first Bible calibrates the prompt for the second; the second Bible runs faster.

---

*The folder schema is grounded in real on-disk material. The contract layer extends Maya's graph rather than parallel-structuring. The CLI muscle memory carries over. The two real Bibles will validate the schema against actual diversity. The closing-the-loop test proves Em can cite Cy's rules at T2-critic time. The structural fix synthesis §5 demands becomes operational. Cy is ready to be built.*
