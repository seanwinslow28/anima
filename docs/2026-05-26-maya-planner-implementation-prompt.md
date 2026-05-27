# Implementation Prompt — Maya the Planner (Commits 3 + 3b)

**Created:** 2026-05-26
**For:** The next Claude Code execution session (plan mode, multi-file edits, git).
**Workstream:** anima Phase 0 — Brief & Plan. Implement Maya's three-phase planner + the `acceptance_criteria.json` graph + the brief.md two-tier template + the cost estimator AgentSpec + the plan CLI + the plan_audit JSONL stream + the planner eval suite.
**Reads as:** Studio-manual voice, prose where reasonable. Sean's exact tonal directive — *"I don't like it when the docs feel like it was strictly made for the terminal. We're making art. It should feel free."*

---

You're picking up the anima project after a Cowork brainstorm session shipped two artifacts. anima is a reusable human + AI 2D animation production pipeline at `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/`. The architecture and agent fleet are locked in v2; commit 4 shipped on main as `fcf28cd` (DAG runner, AgentSpec Protocol, acceptance_criteria.json enforcement, content-addressed cache, hook system — 27/27 tests green). Commit 8 (Em vision critic) shipped in stub-fallback mode in a parallel session today.

The Cowork brainstorm did two things. First, it confirmed that Google's Gemini CLI → Antigravity CLI migration (sunset 2026-06-18) is a small mechanical patch — see [`docs/research/2026-05-26-anti-gravity-cli-findings.md`](research/2026-05-26-anti-gravity-cli-findings.md) — not a structural rethink, and parked it as a 30-minute follow-on patch (commit 8.1) you'll do during this session as a warmup. Second, it ran a `pm-product-discovery:brainstorm-ideas-existing` pass on commit 3 (Maya the planner) and converged on five locked decisions written up at [`docs/2026-05-26-maya-planner-brainstorm.md`](2026-05-26-maya-planner-brainstorm.md). This session implements those decisions.

## Read these binding docs first, in this order

Philosophy before architecture before brainstorm output. Don't skip ahead.

1. [`PHILOSOPHY.md`](../PHILOSOPHY.md) — the load-bearing intent doc, six load-bearing beliefs. Sean's quotes on tone *("we're making art, it should feel free")* and on the critic *("a judge agent will be a staple in all of my agentic workflows from here on out")* preserved verbatim. Both load-bearing for this session.
2. [`CLAUDE.md`](../CLAUDE.md) — anima project manual, current state post-commit-8.
3. [`docs/2026-05-26-maya-planner-brainstorm.md`](2026-05-26-maya-planner-brainstorm.md) — the brainstorm artifact this session implements. Top 5 in §6, deferred items in §7, the explicit "what commit 3 looks like" file map in §8.
4. [`docs/2026-05-26-agent-fleet-brainstorm-v2.md`](2026-05-26-agent-fleet-brainstorm-v2.md) — the v2 architecture lock, especially §2.3 (Pattern B — Planner-Chairman shared rubric), §6 (Maya's per-role assignment, confidence 90%), §7 (cost ceiling).
5. [`docs/research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md`](research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md) — cross-source synthesis grounding v2. §1.3 names `acceptance_criteria.json` as the structural fix; §1.5 names the cheap-judge defense ladder Maya's adversarial Sonnet validation lifts from.
6. [`docs/research/2026-05-26-anti-gravity-cli-findings.md`](research/2026-05-26-anti-gravity-cli-findings.md) — the Antigravity CLI migration findings. Drives the commit 8.1 patch (binary rename, flag swap) you'll ship at the start of this session.
7. [`docs/pipeline-architecture-v1.md`](pipeline-architecture-v1.md) — canonical 10-phase architecture, especially Phase 0 spec.
8. [`docs/2026-05-24-pipeline-v2-change-map.md`](2026-05-24-pipeline-v2-change-map.md) §4 (Commit 3 in the sequence) + §7 (evals workstream — commit 3 ships with its 3b eval suite).
9. [`CHANGELOG.md`](../CHANGELOG.md) — recent entries (top of the file).

## Reference implementations to ground every contract against

* `pipeline/agents/__init__.py` — the AgentSpec Protocol shipped in commit 4. Every new node in this session implements against it.
* `pipeline/agents/vision_critic.py` — Em's commit 8 implementation. Maya's planner follows the same three-section shape (standing context → role addendum → per-invocation brief).
* `pipeline/agents/prompts/em-vision-critic-context.md` + `pipeline/agents/prompts/anima-standing-context.md` — the preamble pattern that mirrors `code-brain/agents-sdk/prompts/vault-critic-standing-context.md`. Maya gets her own role addendum in the same shape.
* `pipeline/criteria.py` — commit 4's acceptance_criteria.json schema + lock enforcement. This session extends it to the graph shape from the brainstorm's TOP-2 idea, while keeping `criteria_locked: true` enforcement intact.
* `pipeline/cli/patches.py` — commit 8's CLI subcommand pattern. The new `pipeline/cli/plan.py` follows the same shape.
* `pipeline/agents/patch_stager.py` — commit 8's post_run hook pattern. The plan_mutate command writes to a sibling JSONL stream using the same atomic-write idiom.
* `tests/test_vision_critic.py` + `tests/test_cli_runners.py` — the test patterns for AgentSpec nodes and CLI wrappers. The planner eval suite + the cost estimator unit tests follow them.

## Your job this session — three phases

### Phase 0 — Commit 8.1 (warmup, ~30 minutes)

**Goal.** Land the Antigravity CLI rename + flag swap in `pipeline/agents/cli_runners.py` so Em can talk to the real Gemini 3.1 Pro instead of permanently running on stub fallback.

**Specific tasks.**

1. **Verify `agy` is installed** on Sean's machine. Run `which agy && agy --version`. If absent, ask Sean before running the installer (`curl -fsSL https://antigravity.google/cli/install.sh | bash`).
2. **Smoke-test the new flag shape.** Run `agy -p "Return the JSON {\"hello\": \"world\"}. No other text." --output-format json`. Capture the stdout/stderr. Confirm the response is parseable JSON.
3. **Smoke-test image attachment via `@path` syntax.** From the anima repo: `agy -p "Describe the image at @images/2D-Character-Sketch-Sean-v1.png in two sentences." --output-format json`. If this doesn't work, fall back to base64-inline via stdin and document the actual working pattern.
4. **Patch `pipeline/agents/cli_runners.py`.** Rename `ANTI_GRAVITY_BIN = "anti-gravity"` to `ANTI_GRAVITY_BIN = "agy"`. Restructure the `cmd` list from `["--json", "--prompt", prompt, "--image", path, ...]` to `["-p", prompt, "--output-format", "json"]` with image paths formatted as `@path` references inside the prompt text. Keep the stub fallback, keep the rate-cap detection, keep the timeout handling, keep the `CLIResponse` shape.
5. **Update tests** in `tests/test_cli_runners.py` if the binary-name change affects fixtures. The mock-based tests should pass unchanged.
6. **Run the full test suite.** `pytest -xvs`. All 27 tests still green (or whatever the count is post-commit-8).
7. **Write a second baseline trace** at `evals/vision-critic/traces/baseline-2026-05-MM-with-cli.md` showing Em's real Gemini 3.1 Pro behavior diffed against the stub baseline. One Act 1 frame is enough.
8. **Commit as `commit 8.1 — Antigravity CLI rename`** with a short message and reference the findings doc.

### Phase 1 — Commit 3 (the main event)

**Goal.** Implement Maya the Planner per the brainstorm's converged Top 5. The five locked ideas:

- **TOP-1** — Two-tier brief (`00_studio_brief.md` + `01_production_brief.md`) with `pipeline plan init` scaffolding both files. The anchored Studio Brief template includes a "what this is NOT" anti-template-trap subsection per ROT4 (folded in).
- **TOP-2** — `acceptance_criteria.json` as a graph: each entry has `id`, `description`, `cites_phase`, `cites_personas`, `impact_tag`, `parent_id`, `derived_from`. Mnemonic IDs follow `AC.{category}.{specific-handle}`. Category vocabulary starts at `identity / proportion / continuity / timing / tone / structural / technical`. Impact tag drives Em's escalation hatch (already wired in commit 8).
- **TOP-3** — Cost estimator as its own AgentSpec at `pipeline/agents/cost_estimator.py`. Reads Flo's `generation.routing:` block, the manifest's `tiering:` block, and any historical-runs corpus. Emits structured `CostEstimate` with low/median/high bands by phase. Maya calls it; commit 5's runtime will too. Optional `cost-preview.png` render via Pillow + matplotlib (ROT3 folded in).
- **TOP-4** — Plan mutation contract: `pipeline plan mutate --force --actor sean --reason "..."` writes one line to `runs/{id}/plan_audit.jsonl` + re-emits plan.md with a delta block. Criteria file gets semver-bumped (`acceptance_criteria-1.1.0.json`) with the symlink at `acceptance_criteria.json` re-pointing. `pipeline plan show` is a **Python rendering layer** that reads plan.md (which Maya emits as clean markdown) and paints it on the terminal as a tear sheet with ASCII box-drawing around the cost preview, criteria summary, character box, beat strip, and routing legend. **Critical separation: the boxes live in the renderer, not in plan.md on disk.** Maya never generates box characters (zero Opus tokens spent on `╔═╗`); downstream consumers (Cy, Em, Sage, chairman, museum writer) read clean markdown and clean JSON. Box-drawing is Python string ops in the `plan show` command, no new dependencies. (DES1 folded in.)
- **TOP-5** — Maya's three-phase flow: Opus primary → Sonnet adversarial validation ("find one criterion that's untestable; find one cost line that's under-estimated; find one impact_tag that's wrong; if you can't, flag low-signal") → resolution. Three-call ceiling per plan.

**Specific tasks.**

1. **Read the brainstorm's §6 Top 5 + §8 file map carefully.** Every file listed in §8 is in scope; everything else is deferred.
2. **NEW `pipeline/agents/planner.py`** — Maya's AgentSpec implementation. Three-phase flow inside `run()`. Use `pipeline/agents/sdk_runners.py`'s `invoke_opus_vision()` pattern as a starting point for the Opus calls (Maya doesn't need vision multimodal — extend or add `invoke_opus_text()` if needed). Sonnet adversarial pass uses `invoke_sonnet_text()` (add if missing). Three-call ceiling guarded by an explicit counter.
3. **NEW `pipeline/agents/cost_estimator.py`** — `CostEstimatorNode` AgentSpec. Reads `manifest['generation']['routing']` and `manifest['tiering']`. Returns a structured `CostEstimate` dataclass with `low / median / high / by_phase / draft_total / pro_total` fields. Unit tests in `tests/test_cost_estimator.py` against fixture manifests.
4. **NEW `pipeline/agents/prompts/maya-planner-context.md`** — standing-context preamble for Maya. Mirror the structure of `em-vision-critic-context.md`. Include: persona introduction (line producer), how Maya consumes the two-tier brief, the criteria graph schema with mnemonic ID convention, the three-phase flow contract.
5. **EXTEND `pipeline/criteria.py`** — graph-shaped criteria parsing per TOP-2. Add a `CriterionGraph` class that loads the JSON, validates the closed category vocabulary, and exposes `query_by_phase(n)` and `query_by_persona(name)` accessors. Keep `criteria_locked: true` enforcement intact from commit 4. Add a `bump_version(reason: str, actor: str)` method that handles the semver-bumped file convention.
6. **NEW `pipeline/cli/plan.py`** — `pipeline plan init / show / approve / mutate` subcommands. Mirror the structure of `pipeline/cli/patches.py`. The `mutate` command writes to `runs/{run_id}/plan_audit.jsonl` atomically (use the temp-then-rename idiom from `pipeline/agents/patch_stager.py`).
7. **NEW `templates/brief/00_studio_brief.md`** — anchored Studio Brief template with seven prompts (story / character / tone / format / medium / deadline / non-negotiables). Tone section includes a "what this is NOT" anti-template-trap subsection. Studio-manual voice throughout — pretend you're writing instructions for a film line producer, not a CLI user.
8. **NEW `templates/brief/01_production_brief.md`** — Production Brief template with YAML frontmatter for the structured fields (phases enabled, characters loaded, target medium, deadline, routing tier defaults) and a markdown body for free-text production notes.
9. **REGISTER the new node** in `pipeline/agents/__init__.py` via `@register_node("planner")` and `@register_node("cost_estimator")`.
10. **MANIFEST schema extension** — add a `brief:` block to `manifest.yaml` pointing at the active brief directory. Keep it additive; don't break the Act 2 work in flight.
11. **Run the full test suite.** Add new tests; don't reduce the green count.
12. **Commit as `commit 3 — Maya the Planner`** with a CHANGELOG entry covering all five Top-5 decisions, the deferred items, and the open assumptions to validate.

### Phase 2 — Commit 3b (the eval suite)

**Goal.** Mirror the commit 8b pattern. Plant the planner eval suite that catches Maya's regression failures and seeds the planner's historical-corpus for ENG4 (deferred).

**Specific tasks.**

1. **NEW `evals/planner/cases.yaml`** — 5–10 seed briefs paired with expected plan-shape assertions. At minimum: (a) a pencil-test Act 1 reproduction case, (b) a hypothetical multi-character case, (c) a hypothetical authoring-first Bible case, (d) a deliberately ambiguous brief case that should trigger Sonnet's adversarial flag, (e) a deliberately under-spec'd brief case that should require Maya to ask for clarification. The cases mirror `evals/vision-critic/cases.yaml` structurally.
2. **NEW `evals/planner/runner.py`** — pytest harness. Lift the shape from `evals/vision-critic/runner.py`. Cases shipped intentionally red are the artifact (per change-map §7); the eval suite's job is to catch real failure modes, not pass everything.
3. **NEW `evals/planner/conftest.py`** — shared fixtures.
4. **NEW `evals/planner/failure-modes.md`** — observed failure taxonomy. Start with three: criteria-too-vague-to-test, cost-line-under-estimates-by-2x+, impact-tag-mismatch.
5. **NEW `evals/planner/last-run.md`** — baseline trace. First run is the artifact; subsequent runs append.
6. **NEW `evals/planner/README.md`** — portfolio-grade write-up. Mirror the structure of `code-brain/evals/vault-synthesizer/README.md` (pattern citations to Hamel Husain, Shreya Shankar, Anthropic's "Demystifying Agent Evals"). This README is itself a museum artifact.
7. **Run the eval suite.** Expect mixed pass/fail; that's the design.
8. **Commit as `commit 3b — planner eval suite`** with a CHANGELOG entry.

## Working pattern + constraints

- **v2's architecture decisions are LOCKED.** Maya's persona, model assignment (Opus → Sonnet validation → human gate), and the three structural patterns from v2 §5 are not for redecision in this session. If something seems wrong on fresh reading, flag it as a question — don't silently correct.
- **Studio-manual voice in every doc.** Sean's exact tonal directive — *"we're making art, it should feel free."* Prose where reasonable. Tables only for genuine reference data. The CHANGELOG entry, the README, the standing-context preamble, the inline code comments, the CLI output — all in studio voice.
- **Don't disturb Act 2 work.** The pencil-test reference implementation runs against the existing manifest's v1 blocks. Manifest schema additions are additive (per change-map §3 "must be backward-compatible in commit 1" — the same rule applies here). The new `brief:` block coexists with the existing `act1:` / `anchor:` structure.
- **Mirror, don't reinvent.** Em (commit 8) is the structural template for Maya. cli_runners.py + sdk_runners.py + the patch_stager hook + the standing-context preamble pattern + the CLI subcommand shape all carry over. Read those files before writing equivalent code.
- **Stage-first, never auto-apply.** Per v2 §2.5: Sean approves plans, mutates criteria with `--force`, locks with `criteria_locked: true`. The runner refuses mutation after lock without `--force --actor --reason`. Mirror commit 4's enforcement.
- **Use plan mode for the multi-file shape, then execute.** Commit 3 touches roughly 11 new files + 2 extended files. Plan mode catches the cross-file consistency issues before they ship.
- **End-of-session deliverables.** (1) Commit 8.1 — Antigravity CLI rename. (2) Commit 3 — Maya the Planner. (3) Commit 3b — planner eval suite. (4) CHANGELOG entries for each. (5) An updated `CLAUDE.md` if any architectural detail moves (most likely the "Active phase" pointer and the source-of-truth table). (6) Optional: a brief Cowork continuation prompt if Sean wants to brainstorm commit 2 (Cy / Character Bible) next.

## Remaining work after this session (for context)

- **Commit 2 — Character Bible migration + Cy persona.** Workstream B from the Cowork brainstorm options. Independent of agent fleet; pending brainstorm pass.
- **Commit 5 — Draft → Pro tier escalation wired into the DAG runner.** Depends on commit 3's cost estimator (now landing this session).
- **Commit 6 — Museum capture layer + Mo persona + Astro content-collection integration.** Workstream D from the Cowork brainstorm; pending.
- **Commit 7 — Animatic ingestion (Procreate Dreams + Procreate PNG sequences).**
- **Commit 9 + 9b — Codie + Annie + Sage + Chairman at T3 + eval suite + standing-context ablation.** Annie's wrapper inherits commit 8.1's Antigravity flag shape directly. Otherwise structurally similar to vault_critic.

## Start

1. Read the binding docs in the listed order.
2. Begin Phase 0 — commit 8.1. The smoke tests against `agy` should take 5 minutes. The patch should take 15. The baseline trace should take 10.
3. Plan mode for Phase 1 — commit 3. Write the plan first; execute against the plan.
4. Phase 2 — commit 3b — lands as a coda once commit 3 is green.

Net wall-clock estimate: 4–6 evenings for commit 3, 1 evening for commit 3b, 30 minutes for commit 8.1. Plan-mode iteration during commit 3 is the variable.

---

*The criteria contract is concrete. The brief shape is decided. The cost estimator has a home. The approval ceremony has an audit trail. The Sonnet validator has teeth. Maya is ready to be built.*
