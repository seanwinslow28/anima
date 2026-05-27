# Agent Fleet — Implementation Handoff Prompt v2

**Paste-ready continuation prompt for the next Claude Code session.** Mirrors the 2026-05-24 → 2026-05-25 → 2026-05-26 handoff pattern: Cowork brainstorms (now twice — initial + post-research v2), Claude Code executes.

**Supersedes:** [`docs/2026-05-25-agent-fleet-implementation-prompt.md`](2026-05-25-agent-fleet-implementation-prompt.md) (v1, DO NOT PASTE). v1 had five corrections pending the research pass; v2 lands the synthesis decisions and is paste-ready.

Open Claude Code at `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/`, enter plan mode (`Shift+Tab` twice), and paste everything below the divider.

---

You're picking up the anima project mid-execution. anima is a reusable human + AI 2D animation production pipeline at `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/`. Commit 1 (doc-only foundation) shipped 2026-05-25 and locked the 10-phase architecture + critic stack + draft→pro principle + Character Bible primitive. Two Cowork sessions on 2026-05-25 and 2026-05-26 produced the agent-fleet decisions in [`docs/2026-05-26-agent-fleet-brainstorm-v2.md`](2026-05-26-agent-fleet-brainstorm-v2.md), grounded in three commissioned research outputs that the [`docs/research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md`](research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md) cross-references. This session implements commits 4 / 8 / 8b / 9 / 9b against v2.

## Read these binding docs first, in this order

Philosophy before architecture before tactical brainstorm output before implementation. Don't skip ahead.

1. **`PHILOSOPHY.md`** — the load-bearing intent doc, ~750 words. Six load-bearing beliefs. Sean's quotes on tone (*"we're making art, it should feel free"*) and on the critic (*"a judge agent will be a staple in all of my agentic workflows from here on out"*) preserved verbatim — both load-bearing for this session.
2. **`CLAUDE.md`** — anima project manual, post-commit-1.
3. **`docs/pipeline-architecture-v1.md`** — canonical 10-phase architecture lock. Untouched by v2.
4. **`docs/2026-05-26-agent-fleet-brainstorm-v2.md`** — *the artifact this session implements against*. Locked per-role table at §6. Three structural patterns at §5. Phase 5 routing at §4. Three open splits at §9 (Sonnet vs Opus orchestrator, Opus vs Sonnet Sage, Sonnet vs Gemini vs Codex storyboard) — resolved by bake-offs that ship post-implementation, not pre-implementation. The defaults from v2 ship now.
5. **`docs/research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md`** — cross-source synthesis grounding v2's decisions. Reference for *why* a given assignment was made; the architecture decisions track back to specific citations.
6. **`docs/Image-Model-DR-2026/SYNTHESIS.md`** — Phase 5 image-model routing source. Flo's routing table lives here; v2 §4 is the digest.
7. **`docs/2026-05-24-pipeline-v2-change-map.md`** — 9-commit sequence at §4. Implementation order: 4 → 8 + 8b → 9 + 9b. Commits 2, 3, 5, 6, 7 either landed or remain post-this-session.
8. **`CHANGELOG.md`** — recent entries (2026-05-26 v2 brainstorm, 2026-05-26 synthesis, 2026-05-26 research-prompts + REVISION PENDING, 2026-05-25 v1 brainstorm, 2026-05-25 PHILOSOPHY.md, 2026-05-25 commit-1, 2026-05-24 architecture-lock).

Reference implementations to ground every contract against — *read before writing equivalent anima code*:

- **`/Users/seanwinslow/Code-Brain/code-brain/agents-sdk/agents/vault_critic.py`** — the T3 pattern. asyncio parallel subprocess fan-out, per-CLI 120s timeout, 600s wall budget, status promotion (`ok` / `partial` / `success-empty` / `error`), manual-mode bypass, `--target` / `--from-list` / `--force` / `--no-standing-context` / `--context` / `--no-default-context` CLI surface, atomic manifest write via temp-then-rename. **Adapt structurally for commit 9; do not rewrite from scratch.** v2 adds a third peer (Sage via Claude Agent SDK, not CLI) and a separate Opus chairman call — both new code, but the asyncio + status-promotion + manifest patterns transfer.
- **`/Users/seanwinslow/Code-Brain/code-brain/agents-sdk/prompts/vault-critic-standing-context.md`** — the standing-context preamble pattern. 22 lines, "About Sean" framing, "What useful critique looks like for him" closer. v2's agents each ship with a 1–2 page preamble at `pipeline/agents/prompts/{role}-standing-context.md`. Shared anima-wide preamble + role addendum.
- **`/Users/seanwinslow/Code-Brain/code-brain/agents-sdk/config.toml`** lines 176–214 (`[agents.vault_critic]` block) — supporting-doc injection pattern (`default_context_files`). v2's manifest `critics:` block grows parallel `default_context_files` lists under each tier.
- **`/Users/seanwinslow/Code-Brain/code-brain/tools/llm-council/council/`** — premium-profile chairman pattern. Adapt the chairman synthesis call structure for T3.

## Working pattern

This session executes. Plan mode → review the plan → exit plan mode → commit-by-commit work with the human in the loop. Multi-file edits welcome. Git commits per logical unit. Mirror the 2026-05-25 commit-1 discipline: every commit gets a CHANGELOG entry, structurally significant changes get a CLAUDE.md update.

## Your job this session

Implement commits 4, 8, 8b, 9, 9b in that order. Commit 4 (DAG runner + `AgentSpec` Protocol + `acceptance_criteria.json` enforcement) is the foundation; commits 8 and 9 wire critics against it; commits 8b and 9b ship eval suites alongside.

### Commit 4 — DAG runner with content-hashed caching, `AgentSpec` Protocol, and `acceptance_criteria.json` enforcement

**Goal.** Refactor the current linear `generate.py` → `audit.py` → `assemble.sh` flow into a typed DAG. Each pipeline stage becomes an agent declaring an `AgentSpec` Protocol. Add the `acceptance_criteria.json` mechanism that the synthesis identified as the structural fix for local-optimization drift.

**Land.**

- `pipeline/agents/__init__.py` — `AgentSpec` Protocol (`inputs: dict`, `outputs: dict`, `cost_estimate: CostEstimate`, `cites_criteria: list[str]`, `run(ctx) -> AgentResult`), `AgentResult` dataclass with `tier: draft | pro` field and `proposed_patches: list[Patch]` field, `CostEstimate` dataclass, `AgentContext` dataclass.
- `pipeline/dag.py` — hand-rolled DAG runner, ~300–500 LOC (per change-map §6). Topological sort + parallel execution via `concurrent.futures.ThreadPoolExecutor`. Content-addressed cache at `runs/{run_id}/.cache/{sha256}.{ext}` + `.json` sidecar. Tier-aware cache keys. Observer-pattern hook system (`post_run` events) for museum capture, eval recorders.
- `pipeline/criteria.py` — `acceptance_criteria.json` schema, loader, validator. Manifest schema gets `criteria_locked: true` flag post-Phase-0 approval; runner refuses to mutate criteria post-lock without a `force` flag (with audit log).
- `pipeline/nodes/frame_generate.py`, `pipeline/nodes/audit_gate.py`, `pipeline/nodes/seedance_motion.py`, `pipeline/nodes/assemble.py` — existing scripts wrapped as `AgentSpec` implementations. Don't rewrite the inner logic; wrap it.
- Feature flag `USE_DAG_RUNNER=1` so the linear path stays usable through the migration.
- Manifest schema extensions: `nodes:` sub-lists under each phase, `acceptance_criteria:` block, `criteria_locked: bool` flag. Backward-compatible — old `act1:` keyframe block stays untouched.

**Don't land in this commit.** No T2, no T3, no Phase 0 planner persona (Maya), no Phase 2 (Cy), no Phase 3 (Sam + Bea), no Phase 5 routing (Flo). The runner exists; the agents that fill it land in subsequent commits.

**Verify.** Run the existing Act 2 Seedance generation through the DAG runner with `USE_DAG_RUNNER=1`. Output byte-identical to linear-path baseline for no-cache case. Edit one prompt; confirm only the affected node + downstream re-run. Sanity-check `acceptance_criteria.json` lock — create a test criteria block, flip `criteria_locked: true`, attempt mutation, confirm runner refuses without `force`.

### Commit 8 — T2 vision critic ("Em")

**Goal.** `pipeline/agents/vision_critic.py` — single SDK agent at three checkpoints: per-frame Generate (Phase 5), post-Motion (Phase 6 → 7), post-Assemble (Phase 8 → 9). v2 model assignment: **Gemini 3.1 Pro (Anti-Gravity CLI) default, Opus 4.7 escalation on borderline / high-impact shots.**

**Land.**

- `pipeline/agents/vision_critic.py` — agent shells out to Anti-Gravity CLI for Gemini 3.1 Pro by default; escalation hatch invokes Claude Agent SDK for Opus 4.7 on `confidence < threshold` or `impact_tag == hero`. Accepts `(image_or_video_path, beat_description, style_guide, character_bible_sheets, anima_standing_context, role_addendum, acceptance_criteria)`. Returns `{verdict: pass | borderline | fail, reasoning, prompt_diff: list[str], confidence: float, cites_criteria: list[str]}`. `cites_criteria` MUST be non-empty when verdict is `fail` or `borderline`.
- `pipeline/agents/prompts/anima-standing-context.md` — shared 1–2 page preamble mirroring `agents-sdk/prompts/vault-critic-standing-context.md`. Carries PHILOSOPHY's load-bearing claims, the 10-phase architecture, the failure modes (template-trap drift, generic recommendations, recommending tools Sean already uses, validators-can't-recover-taste-that-wasn't-there).
- `pipeline/agents/prompts/em-vision-critic-context.md` — role addendum. Em is the script supervisor — continuity nerd voice, proposes prompt diffs in NB Pro / NB2 / Seedream-compatible format, never gives pass/fail without a proposed fix or citation against `acceptance_criteria.json`.
- `manifest.yaml` `critics:` block grows: `t2.default_model: gemini-3.1-pro-via-anti-gravity`, `t2.escalation_model: claude-opus-4-7-via-sdk`, `t2.escalation_threshold: 0.7`, `t2.escalation_tags: [hero, identity_critical]`, `t2.default_context_files: [...]`. Cost cap discipline is decorative for subscription-absorbed models but lands as schema for future runtime enforcement.
- `proposed_patches:` writeback into `manifest.lock.yaml`. Stage-first (no auto-apply). Per-checkpoint `auto_apply: false` is the explicit default v2 ships.

**Don't land.** Director's chair UX for reviewing `proposed_patches:` (deferred). Sean reviews YAML directly or via a `pipeline/cli/patches.py review` command if trivial. Phase 0 planner (Maya) not yet built; for now Em runs against hand-authored `acceptance_criteria.json`.

**Verify.** Em runs against all three checkpoints on Act 2 Seedance output. Borderline / hero-tag shots correctly escalate to Opus. Every `fail` verdict includes a non-empty `cites_criteria`. Stage-first writeback observed; no auto-apply.

### Commit 8b — `evals/vision-critic/` + Sonnet vs Gemini vs Opus three-way bake-off

**Goal.** Eval suite gates Em. Bake-off resolves Open Q1 (T2 model winner) per v2 §9.

**Land.**

- `evals/README.md` — portfolio-grade pattern doc citing `code-brain/evals/vault-synthesizer/README.md` as the lineage. The README is the artifact.
- `evals/vision-critic/cases.yaml` — 10+ cases minimum, grounded in real Act 1 + Act 2 frames + intentionally-red cases the way `vault-synthesizer/cases.yaml` does.
- `evals/vision-critic/runner.py` — pytest harness, reusable across critic agents.
- `evals/vision-critic/traces/baseline-2026-MM-DD.md` — first-run trace. Baseline must exist before Em ships.
- `evals/bakeoffs/2026-MM-DD-gemini-vs-sonnet-vs-opus-vision-critic/` — dated three-way bake-off (per v2's Opus-inclusion correction). `cases.yaml` mirrors vision-critic cases; `results.md` records per-case scores + qualitative notes + dollar-cost-when-applicable + latency; `traces/` carries raw runs from each model.

**Verify.** Em passes the baseline cases on the Gemini default before the bake-off runs. Bake-off results are the artifact; the production-model decision is reviewed by Sean against the results. Loser's failure modes become museum content.

### Commit 9 — T3 multi-CLI + SDK critic stack ("Codie + Annie + Sage" + separate Opus chairman)

**Goal.** `pipeline/agents/cli_critic.py` — adapts `agents-sdk/agents/vault_critic.py` structurally with v2's correction: T3 grows from 2 voices to 3 peers + 1 chairman. Codex CLI (gpt-5.5) + Anti-Gravity CLI (Gemini 3.1 Pro) + **Claude Agent SDK (Opus 4.7) as Sage**, plus a separate Opus 4.7 chairman call. All four subscription-absorbed.

**Land.**

- `pipeline/agents/cli_critic.py` — asyncio.gather subprocess fan-out for Codie + Annie. Sage runs via Claude Agent SDK (Python async call to Opus 4.7). Per-call 120s timeout, 600s wall budget across the three peers. Status promotion verbatim from `vault_critic.py`: `ok` / `partial` / `success-empty` / `error`. After all three peers complete, separate Opus 4.7 chairman call synthesizes using structured output schema (`overall_verdict / consensus_findings / dissent_map / blocking_issues / non_blocking_issues / recommended_next_action / confidence` per the synthesis adopting GPT-5.5 council member's schema).
- Chairman is a *distinct fourth call*, not a promoted peer (Pattern C from v2 §5). Hardcoded Opus 4.7 model; rotation explicitly disabled.
- Wires at two checkpoints: post-Animatic (Phase 4 → 5) and pre-Museum-publish (orthogonal). Targets become images/videos/rendered-MDX instead of markdown. Outputs are comparison-cards under `museum/{project_slug}/critics/` + `proposed_patches:` entries on the run manifest. `cites_criteria` populated from `acceptance_criteria.json`.
- `pipeline/agents/prompts/codie-cli-critic-context.md` (production / reproducibility lens), `pipeline/agents/prompts/annie-cli-critic-context.md` (visual / spatial / continuity lens), `pipeline/agents/prompts/sage-sdk-critic-context.md` (narrative / tonal / semantic lens). Same shared `anima-standing-context.md` preamble; different role addenda.
- `pipeline/agents/prompts/chairman-context.md` — chairman role addendum. Explicit instructions: preserve dissent (don't average it away), cite criteria IDs in resolution, never become a fourth peer.
- `manifest.yaml` `critics:` block grows: `t3.peers: [codie, annie, sage]`, `t3.peer_models: {codie: codex-gpt-5.5, annie: anti-gravity-gemini-3.1-pro, sage: claude-sdk-opus-4.7}`, `t3.chairman_model: claude-sdk-opus-4.7`, `t3.per_call_timeout_s: 120`, `t3.wall_budget_s: 600`, `t3.default_context_files: [...]`.
- CLI surface mirrors vault-critic: `--target` / `--from-list` / `--force` / `--no-standing-context` / `--context` / `--no-default-context`. Manual-mode bypass.
- First-hour verification (synthesis Open Q4): Codex CLI + Anti-Gravity CLI both accept image/video input at anima's resolutions. If either fails this check, the commit pauses for fallback design.

**Don't land.** Auto-merge of accepted `proposed_patches:`. Director's chair UX. Q2/Q3 ablations from v2 §9 (those are commit-9b + post-implementation bake-offs).

**Verify.** T3 stack runs end-to-end on the existing Act 1 hero loop's animatic shape-block (if Sean has it captured) and on the rendered Act 1 museum walkthrough. Chairman synthesis preserves dissent map (no averaging). Subscription-absorbed cost confirmed via no API charges hitting the dashboard.

### Commit 9b — `evals/cli-critic/` + Sage tier ablation + standing-context ablation

**Goal.** Eval suite + the two highest-priority T3 ablations from v2 §9.

**Land.**

- `evals/cli-critic/cases.yaml` — 10+ cases, mix of clean animatic shape-blocks and intentionally-broken ones.
- `evals/cli-critic/agreement-rate.md` — methodology + measurement for Codie + Annie + Sage agreement rate, disagreement pattern analysis (where do they split? on which kinds of failures?).
- `evals/cli-critic/ablations/with-standing-context-vs-without.md` — confirms the preamble earns its keep on anima (mirrors the vault-critic 2026-05-24 Round 3 enrichment validation).
- `evals/bakeoffs/2026-MM-DD-sage-opus-vs-sonnet/` — Open Q2 resolution. Hold Opus chairman constant; run Opus-Sage vs Sonnet-Sage on 10 cases. Measure dissent-map richness, chairman synthesis quality, peer panel correlation.

**Verify.** Standing-context ablation shows clear quality lift with the preamble (matching vault-critic's documented result). Sage ablation produces a winner; results feed into a v2.1 brainstorm revision if Sonnet-Sage wins (i.e., if rate-limit budget on Opus is preserved without dissent-map degradation).

## Constraints

- **The architecture lock from 2026-05-24 and the agent-fleet decisions from v2 (2026-05-26) are LOCKED.** Don't re-decide them. The three open splits at v2 §9 resolve through bake-offs in this session and post-session, NOT through implementation-time revision.
- **Mirror `vault_critic.py` structurally for Commit 9.** The asyncio + subprocess + status-promotion + manifest-write patterns transfer verbatim. v2's additions (third peer via Claude SDK, separate chairman call) are new code on top of the proven pattern, not a rewrite.
- **Standing-context preamble is non-optional.** Every agent ships with one. The shared `anima-standing-context.md` plus per-role addendum mirrors `vault-critic`'s shared-context + per-target-supporting-doc structure.
- **`proposed_patches:` stages, never auto-applies.** v2 ships `auto_apply: false` as the explicit default.
- **`acceptance_criteria.json` is enforced.** Critic outputs include `cites_criteria` on every `fail` or `borderline` verdict. Runner refuses to mutate criteria post-`criteria_locked: true` without a `force` flag + audit log.
- **Architectural diversity at the highest-frequency interaction.** Orchestrator (Sonnet 4.6) and T2 critic (Gemini 3.1 Pro) MUST come from different model families. If a temptation arises during implementation to swap T2 to a Claude model "for consistency," that breaks Pattern A from v2 §5. Don't.
- **Chairman is a distinct fourth call. Don't promote a peer.** v2 §5 Pattern C. The synthesis tested this and rejected the promoted-peer pattern on self-favoring-bias grounds.
- **Studio-manual voice.** Per the tonal directive — prose over tables where reasonable, no terminal-aesthetic in any new doc. Applies to CHANGELOG entries, `evals/README.md`, every persona preamble file, every critic-output card rendered to the museum.
- **The pencil-test Act 2 work is still in flight.** DAG runner ships behind `USE_DAG_RUNNER=1` flag so the linear path remains. Act 2 Seedance generation stays on existing manifest's `act1:` / `anchor:` / `seedance:` blocks unchanged.

## Verify and CHANGELOG

After each commit:

- `CHANGELOG.md` gets an entry. "What changed" + "why" — capture rationale future sessions need.
- `CLAUDE.md` updates only if the change is structurally significant.
- Verify with the eval suite where one exists (8b, 9b). For commit 4, verify via Act 2 byte-identical comparison of linear-path vs DAG-runner output.

## Remaining work after this session

Per change-map §4 + v2 carry-overs:

- **Commit 2** — Character Bible migration + Cy persona (`characters/sean-anchor/` from the single anchor PNG, `character.yaml` schema). v2 ratifies Cy = Opus 4.7 lead + Gemini 3.1 Pro visual verify + NB Pro generate. Brainstorm pending if Sean wants to scope authoring-as-Project-Type ahead of consuming.
- **Commit 3 + 3b** — Maya persona (Brief→Plan planner with `acceptance_criteria.json` emission) + `evals/planner/`. v2 ratifies Maya = Opus 4.7 → Sonnet validation → human gate.
- **Commit 5** — Draft→Pro tier escalation wired into the DAG runner. Schema lands here; cache layer becomes tier-aware.
- **Commit 6** — Museum capture layer + Mo persona + Astro content-collection integration with `sw-ai-pm-portfolio`.
- **Commit 7** — Animatic ingestion (Procreate Dreams + Procreate PNG sequences).

Post-implementation bake-offs (v2 §8 priority order):

3. **Planner downgrade ablation** — Opus → Sonnet after first short is planned (Open Q-resolver).
4. **Orchestrator drift test** — Sonnet for 20 pieces, measure restart rate (Open Q1 resolver).
5. **Storyboard three-way** — Sonnet vs Gemini vs Codex on an 8-shot board (Open Q3 resolver).

Pending brainstorms (kept from v1):

- **Character Bible scaffolding** — gates commit 2 if Sean wants authoring-as-Project-Type. Cy's persona file + character.yaml schema + authoring workflow.
- **Multimodal vault / RAG** — Gemini Embedding 2 vs OpenRouter, Obsidian integration, content-addressed asset store.
- **Museum showcase format** — Mo's persona + comparison-GIF rendering pipeline + decision-ledger surfacing in walkthrough docs.
- **Pressure-test the locked architecture** — multi-perspective critique pass. Worth doing once commits 4 / 8 / 9 ship and the architecture has real agents inside it.

## Start

Begin by reading the binding docs in the listed order. Then read the four code-brain reference files (vault_critic.py, vault-critic-standing-context.md, agents-sdk/config.toml [vault_critic block], tools/llm-council/council/). Then enter plan mode and produce a written implementation plan for commit 4 — what files land, what `AgentSpec` Protocol looks like, what the cache key derivation is, how the feature flag wires in, how `acceptance_criteria.json` enforcement works. Sean reviews the plan before any code lands.

Once commit 4 is in, the pattern for commits 8 / 8b / 9 / 9b is a copy of the same discipline: plan, review, ship, CHANGELOG, eval. Don't batch them — one commit per logical unit, one CHANGELOG entry per commit, one verification step per ship.
