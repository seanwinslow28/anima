# Commits 8 / 8b / 9 / 9b — Continuation Prompt

**Paste everything below the divider into a fresh Claude Code session at /Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline.** The session will read its binding context, enter plan mode for commit 8, get your review, exit plan mode, ship via the `superpowers:executing-plans` skill, then repeat the discipline for commits 8b → 9 → 9b. Commit 4 (the DAG runner + AgentSpec foundation) shipped on 2026-05-26 as `fcf28cd`; this session implements the agent fleet on top of that contract.

---

You're picking up the anima project mid-execution. anima is a reusable human + AI 2D animation production pipeline at `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/`. Commit 4 (DAG runner + AgentSpec Protocol + acceptance_criteria.json enforcement) shipped 2026-05-26 as `fcf28cd` and locked the contract every critic in this session wires against. This session implements commits 8 / 8b / 9 / 9b against the v2 agent-fleet decisions.

## Read these binding docs first, in this order

Philosophy before architecture before tactical brainstorm output before commit-4 contract before implementation. Don't skip ahead.

1. **`PHILOSOPHY.md`** — the load-bearing intent doc, ~750 words. Six load-bearing beliefs. Sean's quotes on tone (*"we're making art, it should feel free"*) and on the critic (*"a judge agent will be a staple in all of my agentic workflows from here on out"*) are preserved verbatim — both load-bearing for this session.
2. **`CLAUDE.md`** — anima project manual, post-commit-4. Note the new `pipeline/agents/`, `pipeline/criteria.py`, `pipeline/dag.py`, `pipeline/nodes/` entries in Directory Structure, and the new "DAG-orchestrated run" sub-section in §Key Commands.
3. **`docs/pipeline-architecture-v1.md`** — canonical 10-phase architecture lock. Untouched by v2.
4. **`docs/2026-05-26-agent-fleet-brainstorm-v2.md`** — the artifact this session implements against. Locked per-role table at §6. Three structural patterns at §5 (architectural diversity, Planner-Chairman shared rubric, chairman is a distinct fourth call). Phase 5 routing at §4. Three open splits at §9 — resolved by bake-offs that ship post-implementation, not pre-implementation. v2 defaults ship now; bake-offs come later.
5. **`docs/research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md`** — cross-source synthesis grounding v2's decisions. Reference for *why* a given assignment was made; the architecture decisions track back to specific citations.
6. **`docs/Image-Model-DR-2026/SYNTHESIS.md`** — Phase 5 image-model routing source. Flo's routing table lives here; v2 §4 is the digest. Mostly relevant for future Flo work, but the routing-table shape is what proposed_patches: in T2 critique reference.
7. **`docs/2026-05-24-pipeline-v2-change-map.md`** — 9-commit sequence at §4. This session is commits 8 / 8b / 9 / 9b. Commit 4 done.
8. **`CHANGELOG.md`** — recent entries (2026-05-26 commit 4, 2026-05-26 v2 brainstorm + synthesis + implementation prompt, 2026-05-25 v1 brainstorm, 2026-05-25 PHILOSOPHY.md, 2026-05-25 commit 1).

## Read the commit-4 artifacts before writing equivalent code

Commit 4 is the contract every critic in this session implements. Read these before writing T2 or T3 code:

- **`pipeline/agents/__init__.py`** — `AgentSpec` Protocol, `AgentResult` dataclass (note `tier`, `proposed_patches`, `cites_criteria` fields), `AgentContext`, `CostEstimate`, `Patch`, `NODE_REGISTRY`, `@register_node` decorator. Every new critic class in commits 8 + 9 satisfies this Protocol and registers under this decorator. The Patch dataclass is what `proposed_patches:` carries — read its docstring for the stage-not-auto-apply contract.
- **`pipeline/dag.py`** — the runner that orchestrates nodes. The observer-pattern `add_hook("post_run", fn)` is where commit 8b's vision-critic eval recorder will subscribe; the same for commit 9b. The cache key includes `criteria_hash` so a criteria mutation invalidates downstream — your T2/T3 critics will leverage this for re-validation.
- **`pipeline/criteria.py`** — `AcceptanceCriterion`, `CriteriaBundle`, `enforce_lock()`, `CriteriaLockViolation`. Every critic's `cites_criteria` field in `AgentResult` references IDs from the bundle. Maya (commit 3) will populate the file for real; for now, fixtures in `tests/fixtures/criteria_*.json` show the shape. Em (commit 8) must populate `cites_criteria` non-empty when verdict is `fail` or `borderline`.
- **`pipeline/nodes/{frame_generate,audit_gate,seedance_motion,assemble}.py`** — four worked examples of `AgentSpec` implementations wrapping legacy code. Your new critic nodes follow the same shape.
- **`tests/test_{agents,criteria,dag}.py`** — TDD patterns for the next commits' eval suites mirror.
- **`tests/fixtures/manifest_assemble_only.yaml`** — minimal manifest exercising the DAG runner end-to-end. The pattern for commit 8b's vision-critic eval cases mirrors this.

## Read the code-brain reference implementations for commit 9

Mirror structurally; do not rewrite from scratch.

- **`/Users/seanwinslow/Code-Brain/code-brain/agents-sdk/agents/vault_critic.py`** — the T3 pattern. asyncio parallel subprocess fan-out, per-CLI 120s timeout, 600s wall budget, status promotion (`ok` / `partial` / `success-empty` / `error`), manual-mode bypass, `--target` / `--from-list` / `--force` / `--no-standing-context` / `--context` / `--no-default-context` CLI surface, atomic manifest write via temp-then-rename. v2 adds a third peer (Sage via Claude Agent SDK, not CLI) and a separate Opus chairman call — both new code, but the asyncio + status-promotion + manifest patterns transfer.
- **`/Users/seanwinslow/Code-Brain/code-brain/agents-sdk/prompts/vault-critic-standing-context.md`** — the standing-context preamble pattern. 22 lines, "About Sean" framing, "What useful critique looks like for him" closer. v2's agents each ship with a 1–2 page preamble at `pipeline/agents/prompts/{role}-standing-context.md` — shared anima-wide preamble + role addendum.
- **`/Users/seanwinslow/Code-Brain/code-brain/agents-sdk/config.toml`** lines 176–214 (`[agents.vault_critic]` block) — supporting-doc injection pattern (`default_context_files`). v2's `manifest.yaml` `critics:` block grows parallel `default_context_files` lists under each tier.
- **`/Users/seanwinslow/Code-Brain/code-brain/tools/llm-council/council/`** — premium-profile chairman pattern. Adapt the chairman synthesis call structure for T3.

## Read commit 4's continuation context

- **`/Users/seanwinslow/.claude/plans/you-re-picking-up-the-velvet-dove.md`** — commit 4's plan (already shipped). Read it to understand the discipline this session is replicating: context → file structure → bite-sized tasks with TDD where it pays → verification protocol → CHANGELOG entry → commit. The plan-mode workflow + executing-plans skill drove that commit; same pattern here, one plan per commit.

## Working pattern

This session executes. For each commit:

1. Enter plan mode. Read whatever additional context the specific commit needs (e.g., commit 8 needs to read the existing `audit.py` to know what `verdict_codes` Em will cite; commit 9 needs to confirm Codex CLI + Anti-Gravity CLI accept image input at anima's resolutions before touching code).
2. Write the plan to `/Users/seanwinslow/.claude/plans/{plan-name}.md`. Use the `superpowers:writing-plans` skill's structure: header + context + bounded scope + file structure + bite-sized tasks + verification + CHANGELOG entry template.
3. Use `AskUserQuestion` to surface meaningful design forks BEFORE exiting plan mode.
4. `ExitPlanMode` — Sean reviews.
5. Once approved, invoke `superpowers:executing-plans` and ship the commit task-by-task.
6. Verify per the plan's protocol.
7. Append the CHANGELOG entry. Update CLAUDE.md only if structurally significant.
8. Commit on `main` (one commit per logical unit; mirror commit 4's discipline).
9. Surface what's next to Sean.

The `.venv/` already exists with `pytest`, `pyyaml`, and `Pillow` installed (created during commit 4). Use `.venv/bin/pytest tests/` to run the suite. Python 3.13.12.

## Your job this session

Commits 8 → 8b → 9 → 9b in that order. One commit per logical unit. One CHANGELOG entry per commit. One verification step per ship.

### Commit 8 — T2 vision critic ("Em")

**Goal.** `pipeline/agents/vision_critic.py` — single SDK agent at three checkpoints: per-frame Generate (Phase 5), post-Motion (Phase 6 → 7), post-Assemble (Phase 8 → 9). v2 model assignment: **Gemini 3.1 Pro via Anti-Gravity CLI default, Opus 4.7 escalation on borderline / hero shots**.

**Land:**

- `pipeline/agents/vision_critic.py` — `VisionCriticNode` registered under `register_node("vision_critic")`. The class satisfies `AgentSpec` (from commit 4's `pipeline/agents/__init__.py`). Shells to Anti-Gravity CLI for Gemini 3.1 Pro by default; escalation hatch invokes the Claude Agent SDK for Opus 4.7 when `confidence < threshold` or `impact_tag == "hero"`. Accepts: image_or_video_path, beat_description, style_guide, character_bible_sheets (for now: the manifest's `anchor:` block; commit 2 lands the full Bible loader), anima_standing_context, role_addendum, acceptance_criteria. Returns `AgentResult` with `outputs = {verdict, reasoning, confidence}`, `proposed_patches: list[Patch]`, `cites_criteria: list[str]`. **`cites_criteria` MUST be non-empty when verdict is `fail` or `borderline`** — enforce this in the node's `run()` method before returning.
- `pipeline/agents/prompts/anima-standing-context.md` — shared 1–2 page preamble mirroring `agents-sdk/prompts/vault-critic-standing-context.md`. Carries PHILOSOPHY's load-bearing claims, the 10-phase architecture summary, the failure modes (template-trap drift, generic recommendations, recommending tools Sean already uses, *"validators cannot recover taste that was absent at generation time"* from the synthesis §5).
- `pipeline/agents/prompts/em-vision-critic-context.md` — role addendum. Em is the **script supervisor** — continuity nerd voice, proposes prompt diffs in NB Pro / NB2 / Seedream-compatible format, **never** gives pass/fail without a proposed fix or a citation against `acceptance_criteria.json`.
- `manifest.yaml` `critics:` block grows: `t2.default_model: gemini-3.1-pro-via-anti-gravity`, `t2.escalation_model: claude-opus-4-7-via-sdk`, `t2.escalation_threshold: 0.7`, `t2.escalation_tags: [hero, identity_critical]`, `t2.default_context_files: [PHILOSOPHY.md, CLAUDE.md, docs/pipeline-architecture-v1.md]`, `t2.auto_apply: false`. Cost cap discipline is decorative for subscription-absorbed models but lands as schema for future runtime enforcement.
- `proposed_patches:` writeback into `manifest.lock.yaml`. **Stage-first (no auto-apply).** Per-checkpoint `auto_apply: false` is the explicit default v2 ships.

**Don't land:**

- Director's-chair UX for reviewing `proposed_patches:` (deferred to commit 8b or commit 10). Sean reviews YAML directly or via a `pipeline/cli/patches.py review` command if it's trivial enough to scope in.
- Phase 0 planner (Maya) — for now Em runs against hand-authored `acceptance_criteria.json` fixtures.

**Verify.** Em runs against all three checkpoints on Act 2 Seedance output. Borderline / hero-tag shots correctly escalate to Opus. Every `fail` verdict includes a non-empty `cites_criteria`. Stage-first writeback observed; no auto-apply.

### Commit 8b — `evals/vision-critic/` + Sonnet vs Gemini vs Opus three-way bake-off

**Goal.** Eval suite gates Em. Bake-off resolves Open Q1 (T2 model winner) per v2 §9.

**Land:**

- `evals/README.md` — portfolio-grade pattern doc citing `code-brain/evals/vault-synthesizer/README.md` as the lineage. The README is the artifact.
- `evals/vision-critic/cases.yaml` — 10+ cases minimum, grounded in real Act 1 + Act 2 frames + intentionally-red cases the way `vault-synthesizer/cases.yaml` does.
- `evals/vision-critic/runner.py` — pytest harness, reusable across critic agents.
- `evals/vision-critic/traces/baseline-2026-MM-DD.md` — first-run trace. **Baseline must exist before Em ships.** (Commit 8b can land alongside or just after commit 8; if you ship 8 first then run 8b, the baseline trace must come BEFORE you mark commit 8 done. Plan accordingly.)
- `evals/bakeoffs/2026-MM-DD-gemini-vs-sonnet-vs-opus-vision-critic/` — dated three-way bake-off (per v2's Opus-inclusion correction). `cases.yaml` mirrors vision-critic cases; `results.md` records per-case scores + qualitative notes + dollar-cost-when-applicable + latency; `traces/` carries raw runs from each model.

**Verify.** Em passes the baseline cases on the Gemini default before the bake-off runs. Bake-off results are the artifact; the production-model decision is Sean's against the results. Loser's failure modes become museum content.

### Commit 9 — T3 multi-CLI + SDK critic stack ("Codie + Annie + Sage" + separate Opus chairman)

**Goal.** `pipeline/agents/cli_critic.py` — adapts `agents-sdk/agents/vault_critic.py` structurally with v2's correction: **T3 grows from 2 voices to 3 peers + 1 chairman.** Codex CLI (gpt-5.5) + Anti-Gravity CLI (Gemini 3.1 Pro) + Claude Agent SDK (Opus 4.7) as Sage, plus a separate Opus 4.7 chairman call. All four subscription-absorbed.

**Land:**

- `pipeline/agents/cli_critic.py` — `asyncio.gather` subprocess fan-out for Codie + Annie. Sage runs via Claude Agent SDK (Python async call to Opus 4.7). Per-call 120s timeout, 600s wall budget across the three peers. Status promotion verbatim from `vault_critic.py`: `ok` / `partial` / `success-empty` / `error`. After all three peers complete, **separate Opus 4.7 chairman call** synthesizes using structured output schema (`overall_verdict / consensus_findings / dissent_map / blocking_issues / non_blocking_issues / recommended_next_action / confidence` per the synthesis adopting the GPT-5.5 council member's schema).
- Chairman is a **distinct fourth call**, not a promoted peer (Pattern C from v2 §5). Hardcoded Opus 4.7 model; rotation explicitly disabled.
- Wires at two checkpoints: post-Animatic (Phase 4 → 5) and pre-Museum-publish (orthogonal). Targets become images/videos/rendered-MDX instead of markdown. Outputs are comparison-cards under `museum/{project_slug}/critics/` + `proposed_patches:` entries on the run manifest. `cites_criteria` populated from `acceptance_criteria.json`.
- `pipeline/agents/prompts/codie-cli-critic-context.md` (production / reproducibility lens), `pipeline/agents/prompts/annie-cli-critic-context.md` (visual / spatial / continuity lens), `pipeline/agents/prompts/sage-sdk-critic-context.md` (narrative / tonal / semantic lens). Same shared `anima-standing-context.md` preamble (from commit 8); different role addenda.
- `pipeline/agents/prompts/chairman-context.md` — chairman role addendum. Explicit instructions: preserve dissent (don't average it away), cite criteria IDs in resolution, never become a fourth peer.
- `manifest.yaml` `critics:` block grows: `t3.peers: [codie, annie, sage]`, `t3.peer_models: {codie: codex-gpt-5.5, annie: anti-gravity-gemini-3.1-pro, sage: claude-sdk-opus-4.7}`, `t3.chairman_model: claude-sdk-opus-4.7`, `t3.per_call_timeout_s: 120`, `t3.wall_budget_s: 600`, `t3.default_context_files: [...]`.
- CLI surface mirrors vault-critic: `--target` / `--from-list` / `--force` / `--no-standing-context` / `--context` / `--no-default-context`. Manual-mode bypass.
- **First-hour verification** (synthesis Open Q4): Codex CLI + Anti-Gravity CLI both accept image/video input at anima's resolutions. If either fails this check, **the commit pauses for fallback design** — surface the failure to Sean and ask before proceeding.

**Don't land:**

- Auto-merge of accepted `proposed_patches:`.
- Director's chair UX.
- Q2/Q3 ablations from v2 §9 (those are commit 9b + post-implementation bake-offs).

**Verify.** T3 stack runs end-to-end on the existing Act 1 hero loop's animatic shape-block (if Sean has it captured) and on the rendered Act 1 museum walkthrough. Chairman synthesis preserves the dissent map (no averaging). Subscription-absorbed cost confirmed via no API charges hitting the dashboard.

### Commit 9b — `evals/cli-critic/` + Sage tier ablation + standing-context ablation

**Goal.** Eval suite + the two highest-priority T3 ablations from v2 §9.

**Land:**

- `evals/cli-critic/cases.yaml` — 10+ cases, mix of clean animatic shape-blocks and intentionally-broken ones.
- `evals/cli-critic/agreement-rate.md` — methodology + measurement for Codie + Annie + Sage agreement rate, disagreement pattern analysis (where do they split? on which kinds of failures?).
- `evals/cli-critic/ablations/with-standing-context-vs-without.md` — confirms the preamble earns its keep on anima (mirrors the vault-critic 2026-05-24 Round 3 enrichment validation).
- `evals/bakeoffs/2026-MM-DD-sage-opus-vs-sonnet/` — Open Q2 resolution. Hold Opus chairman constant; run Opus-Sage vs Sonnet-Sage on 10 cases. Measure dissent-map richness, chairman synthesis quality, peer panel correlation.

**Verify.** Standing-context ablation shows clear quality lift with the preamble (matching vault-critic's documented result). Sage ablation produces a winner; results feed into a v2.1 brainstorm revision if Sonnet-Sage wins (i.e., if Opus rate-limit budget is preserved without dissent-map degradation).

## Constraints (locked — don't re-decide)

- The architecture lock from 2026-05-24 and the agent-fleet decisions from v2 (2026-05-26) are **LOCKED**. The three open splits at v2 §9 resolve through bake-offs in this session and post-session, **NOT** through implementation-time revision.
- **Mirror `vault_critic.py` structurally for Commit 9.** The asyncio + subprocess + status-promotion + manifest-write patterns transfer verbatim. v2's additions (third peer via Claude SDK, separate chairman call) are new code on top of the proven pattern, not a rewrite.
- **Standing-context preamble is non-optional.** Every agent ships with one. The shared `anima-standing-context.md` + per-role addendum mirrors vault-critic's shared-context + per-target-supporting-doc structure.
- **`proposed_patches:` stages, never auto-applies.** v2 ships `auto_apply: false` as the explicit default.
- **`acceptance_criteria.json` is enforced.** Critic outputs include `cites_criteria` on every `fail` or `borderline` verdict. The runner (already shipped in commit 4) refuses to mutate criteria post-`criteria_locked: true` without a `--force-criteria-mutation` flag + audit log.
- **Architectural diversity at the highest-frequency interaction.** Orchestrator (Sonnet 4.6) and T2 critic (Gemini 3.1 Pro) **MUST** come from different model families. If a temptation arises during implementation to swap T2 to a Claude model "for consistency," that breaks Pattern A from v2 §5. Don't.
- **Chairman is a distinct fourth call.** Don't promote a peer. v2 §5 Pattern C. The synthesis tested this and rejected the promoted-peer pattern on self-favoring-bias grounds.
- **Studio-manual voice.** Per the tonal directive — prose over tables where reasonable, no terminal-aesthetic in any new doc. Applies to CHANGELOG entries, `evals/README.md`, every persona preamble file, every critic-output card rendered to the museum.
- **The pencil-test Act 2 work is still in flight.** Don't break the linear path. The DAG runner shipped in commit 4 with `USE_DAG_RUNNER=1` feature flag; the legacy path stays available. Act 2 Seedance generation stays on the existing manifest's `act1:` / `anchor:` / `seedance:` blocks unchanged.
- **Build the contract on top of commit 4, don't bypass it.** Every critic in commits 8 + 9 is a node class that satisfies `AgentSpec` (from `pipeline/agents/__init__.py`) and registers under `@register_node`. Cost estimates feed Maya's preview (future). Patches stage as `Patch` instances. `cites_criteria` and `acceptance_criteria.json` are enforced together.

## Per-commit discipline

After each commit:

- **`CHANGELOG.md` gets an entry.** What changed + why — capture rationale future sessions need.
- **`CLAUDE.md` updates only if the change is structurally significant** (new top-level convention, new skill, new directory). Not for routine code edits.
- **Verify with the eval suite where one exists** (8b, 9b). For commits 8 + 9, verify via the protocols in their respective "Verify" sections above.
- **Commit on main per session direction.** Mirror commit 4's discipline: one commit per logical unit, focused diff, clear message.
- **Surface what's next to Sean** at end of each commit. Don't auto-continue to the next commit without his explicit go-ahead.

## Remaining work after this session

Per change-map §4 + v2 carry-overs:

- **Commit 2** — Character Bible migration + Cy persona (`characters/sean-anchor/` from the single anchor PNG, `character.yaml` schema). v2 ratifies Cy = Opus 4.7 lead + Gemini 3.1 Pro visual verify + NB Pro generate. Brainstorm pending if Sean wants to scope authoring-as-Project-Type ahead of consuming.
- **Commit 3 + 3b** — Maya persona (Brief → Plan planner with `acceptance_criteria.json` emission) + `evals/planner/`. v2 ratifies Maya = Opus 4.7 → Sonnet validation → human gate. Schema for `acceptance_criteria.json` is already in place from commit 4; commit 3 populates the file from Maya's output.
- **Commit 5** — Draft → Pro tier escalation wired into the DAG runner. Schema lands here; cache layer becomes tier-aware. (Cache is already tier-aware from commit 4; commit 5 wires the auto-escalation logic.)
- **Commit 6** — Museum capture layer + Mo persona + Astro content-collection integration with `sw-ai-pm-portfolio`. Subscribes to the DAG runner's `post_run` hook (already shipped in commit 4).
- **Commit 7** — Animatic ingestion (Procreate Dreams + Procreate PNG sequences).

Post-implementation bake-offs (v2 §8 priority order):

- Planner downgrade ablation — Opus → Sonnet after first short is planned (Open Q-resolver).
- Orchestrator drift test — Sonnet for 20 pieces, measure restart rate (Open Q1 resolver).
- Storyboard three-way — Sonnet vs Gemini vs Codex on an 8-shot board (Open Q3 resolver).

## Start

Begin by reading the binding docs in the listed order. Then read the four code-brain reference files (`vault_critic.py`, `vault-critic-standing-context.md`, `agents-sdk/config.toml` `[agents.vault_critic]` block, `tools/llm-council/council/`). Then read the commit-4 artifacts (`pipeline/agents/__init__.py`, `pipeline/dag.py`, `pipeline/criteria.py`, `pipeline/nodes/*.py`, the test files) so you internalize the AgentSpec contract. Then enter plan mode and produce a written implementation plan for commit 8 — what files land, what the Em vision-critic class shape looks like, how the standing-context preamble is wired in, how the Gemini default + Opus escalation hatch is implemented, how `proposed_patches:` stage into `manifest.lock.yaml`, how `cites_criteria` is enforced when verdict is `fail` or `borderline`. Sean reviews the plan before any code lands. Use `superpowers:writing-plans` for the plan structure; use `superpowers:executing-plans` to ship it.

Once commit 8 is in, the pattern for commits 8b / 9 / 9b is a copy of the same discipline: plan, review, ship, CHANGELOG entry, verify, surface what's next. Don't batch them — one commit per logical unit.
