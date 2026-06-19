# Agent Fleet — Implementation Handoff Prompt

**Paste-ready continuation prompt for the next Claude Code session.** Mirrors the 2026-05-24 → 2026-05-25 handoff pattern: Cowork brainstorms, Claude Code executes.

Open Claude Code at `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/`, enter plan mode (`Shift+Tab` twice), and paste everything below the divider.

> ## ⚠ DO NOT PASTE — SUPERSEDED BY V2 (2026-05-26)
>
> **v2 ships at [`docs/2026-05-26-agent-fleet-implementation-prompt-v2.md`](2026-05-26-agent-fleet-implementation-prompt-v2.md).** Paste *that* into Claude Code plan mode, not this v1 prompt. v2 lands the corrections from the 2026-05-26 review pass and the synthesis decisions from three research outputs.
>
> What changed in v2: T3 grows to 3 peers + Opus chairman (Sage as third voice via Claude SDK); best-models-on-pinnacle-phases re-tier (Opus 4.7 at Planner, Character Designer, Scriptwriter, T3 Sage, T3 Chairman); Phase 3 un-defers with Sam (Scriptwriter, Opus) + Bea (Storyboard Artist, Sonnet default with Opus escalation); Phase 5 routing per [`docs/Image-Model-DR-2026/SYNTHESIS.md`](../../Image-Model-DR-2026/SYNTHESIS.md) via persona Flo; Sonnet 4.6 orchestrator (not Opus) with Opus escalation hatch — architectural diversity at the highest-frequency interaction (orchestrator + T2 critic must not share a model family); Planner-Chairman shared-rubric pattern via immutable `acceptance_criteria.json`; T2 critic Em = Gemini 3.1 Pro default with Opus escalation.
>
> v1 retained for historical context only. v1's structure (binding-doc read order, code-brain reference files, commit sequence) carried over into v2 with the corrected model assignments.

---

You're picking up the anima project mid-execution. anima is a reusable human + AI 2D animation production pipeline at `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/`. Commit 1 (doc-only foundation) shipped 2026-05-25 and locked the 10-phase architecture + critic stack + draft→pro principle + Character Bible primitive. The 2026-05-25 Cowork session ran an agent-fleet brainstorm (`docs/2026-05-25-agent-fleet-brainstorm.md`) and locked five decisions that fill the empty slots in that architecture. This session implements them.

## Read these binding docs first, in this order

Philosophy before architecture before tactical brainstorm output. Don't skip ahead.

1. **`PHILOSOPHY.md`** — the load-bearing intent doc, ~750 words. Six load-bearing beliefs. Sean's exact quote on tonal voice (*"we're making art, it should feel free"*) and on the critic (*"a judge agent will be a staple in all of my agentic workflows from here on out"*) preserved verbatim — both are load-bearing for this session.
2. **`CLAUDE.md`** — anima project manual, post-commit-1. Operational orientation, source-of-truth table, the 10-phase pipeline diagram.
3. **`docs/pipeline-architecture-v1.md`** — canonical 10-phase architecture lock. Per-phase spec, full critic stack table, draft→pro coverage, Character Bible directory layout, museum capture layer.
4. **`docs/2026-05-25-agent-fleet-brainstorm.md`** — *the new artifact this session implements against*. 18-idea ideation pass, top 5 locked (T3 subprocess critics, T2 vision critic, named-role personas + preamble, typed `AgentSpec` Protocol + `proposed_patches`, single-orchestrator topology). Locked topology answer at §5. Cost ceilings at §6. Open Q1–Q7 at §8 are for *this session* to resolve through implementation, not to re-brainstorm.
5. **`docs/2026-05-24-pipeline-v2-change-map.md`** — 9-commit sequence at §4. The implementation order this session follows.
6. **`CHANGELOG.md`** — top four entries (2026-05-25 agent-fleet brainstorm, 2026-05-25 PHILOSOPHY.md, 2026-05-25 commit-1, 2026-05-24 architecture-lock).

Reference implementations to ground every contract against — *read before writing the equivalent anima code*:

- **`/Users/seanwinslow/Code-Brain/code-brain/agents-sdk/agents/vault_critic.py`** — the T3 pattern. asyncio parallel subprocess fan-out, per-CLI 120s timeout, 600s wall budget, status promotion (`ok` / `partial` / `success-empty` / `error`), manual-mode bypass, `--target` / `--from-list` / `--force` / `--no-standing-context` / `--context` / `--no-default-context` CLI surface, atomic manifest write via temp-then-rename. **Anima's T3 should adapt this file structurally, not write from scratch.**
- **`/Users/seanwinslow/Code-Brain/code-brain/agents-sdk/prompts/vault-critic-standing-context.md`** — the standing-context preamble pattern. 22 lines, "About Sean" framing, "What useful critique looks like for him" closer. Anima's `pipeline/agents/prompts/anima-standing-context.md` should be the same shape, anima-specific content.
- **`/Users/seanwinslow/Code-Brain/code-brain/agents-sdk/config.toml`** lines 176–214 (`[agents.vault_critic]` block) — the supporting-doc injection pattern (`default_context_files`). Anima's `manifest.yaml`'s `critics:` block should grow a parallel `default_context_files` list under each tier.

## Working pattern

This session executes. Plan mode → review the plan → exit plan mode → commit-by-commit work with the human in the loop. Multi-file edits welcome. Git commits per logical unit. Mirror the 2026-05-25 commit-1 discipline: every commit gets a CHANGELOG entry, structurally significant changes get a CLAUDE.md update.

## Your job this session

Implement commits 4, 8, 8b, 9, 9b in that order. Commit 4 (DAG runner) is the foundation; without it commits 8 and 9 can't wire cleanly. Commits 8b and 9b are the eval suites — they ship alongside their agent commits, not after.

### Commit 4 — DAG runner with content-hashed caching and `AgentSpec` Protocol

**Goal.** Refactor the current linear `generate.py` → `audit.py` → `assemble.sh` flow into a typed DAG. Each pipeline stage becomes an agent declaring an `AgentSpec` Protocol. Foundation for everything downstream — commits 5 (draft→pro), 6 (museum capture), 8 (T2 vision critic), 9 (T3 CLI critic) all wire against this.

**Land.**

- `pipeline/agents/__init__.py` — module init with the `AgentSpec` Protocol, `AgentResult` dataclass, `CostEstimate` dataclass, `AgentContext` dataclass.
- `pipeline/dag.py` — hand-rolled DAG runner, ~300–500 LOC (per change-map §6). Topological sort + parallel execution via `concurrent.futures.ThreadPoolExecutor` for I/O-bound nodes (`ProcessPoolExecutor` available behind a flag for CPU-heavy). Content-addressed cache at `runs/{run_id}/.cache/{sha256}.{ext}` + `.json` sidecar. Tier-aware cache keys so draft + pro outputs coexist. Observer-pattern hook system (`post_run` events) for museum capture, eval recorders, the orchestrator itself.
- `pipeline/nodes/frame_generate.py`, `pipeline/nodes/audit_gate.py`, `pipeline/nodes/seedance_motion.py`, `pipeline/nodes/assemble.py` — existing scripts wrapped as `AgentSpec` implementations. Don't rewrite the inner logic; wrap it.
- Feature flag `USE_DAG_RUNNER=1` so the linear path stays usable through the migration. Both can coexist for the duration.
- `manifest.yaml` schema extension: each phase block grows a `nodes:` sub-list that maps node IDs to their `AgentSpec` classes. Backward-compatible — old `act1:` keyframe block stays untouched.

**Don't land in this commit.** No T2, no T3, no Phase 0 planner. The runner exists; the agents that fill it land in subsequent commits.

**Verify.** Run the existing Act 2 Seedance generation through the DAG runner with `USE_DAG_RUNNER=1`. Output must match the linear path byte-identical for the no-cache case. Edit one prompt; confirm only the affected node + downstream re-run.

### Commit 8 — T2 vision critic ("Em")

**Goal.** Single SDK agent at `pipeline/agents/vision_critic.py`. Wires at three checkpoints: per-frame Generate (Phase 5), post-Motion (Phase 6 → 7), post-Assemble (Phase 8 → 9).

**Land.**

- `pipeline/agents/vision_critic.py` — Claude SDK agent. Accepts `(image_or_video_path, beat_description, style_guide, character_bible_sheets, anima_standing_context, role_addendum)`. Returns `{verdict: pass | borderline | fail, reasoning: str, prompt_diff: list[str], confidence: float}`. Default model `claude-sonnet-4-6` per `agents-sdk/config.toml` precedent.
- `pipeline/agents/prompts/anima-standing-context.md` — the shared 1–2 page preamble. Mirrors `agents-sdk/prompts/vault-critic-standing-context.md` shape. Carries the philosophy's load-bearing claims, the locked architecture, the failure modes (template-trap drift, generic recommendations, recommending tools Sean already uses).
- `pipeline/agents/prompts/em-vision-critic-context.md` — role addendum. Em is the script supervisor — continuity nerd voice, proposes prompt diffs in NB2-compatible format, never gives pass/fail without a proposed fix.
- `manifest.yaml` `critics:` block grows `t2.model`, `t2.max_cost_per_call_usd: 0.05`, `t2.daily_cap_usd: 5`, `t2.monthly_cap_usd: 40`, `t2.default_context_files: [...]`.
- `proposed_patches:` writeback into `manifest.lock.yaml` when a critic finding is generated. Stage-first (no auto-apply); a future commit adds `auto_apply: true` per-checkpoint.

**Don't land.** Director's chair UX for reviewing `proposed_patches:` (deferred to a later commit). For now, Sean reviews the YAML directly or via a `pipeline/cli/patches.py review` command if that proves trivial to add.

### Commit 8b — `evals/vision-critic/` + Sonnet vs Gemini 3 Pro bake-off

**Goal.** Eval suite gates Em's quality. Bake-off lands as portfolio content.

**Land.**

- `evals/README.md` — portfolio-grade pattern doc (cite `code-brain/evals/vault-synthesizer/README.md` as the lineage). The README itself is the artifact.
- `evals/vision-critic/cases.yaml` — 10 cases minimum, grounded in real Act 1 + Act 2 frames (the pencil-test corpus). Include intentionally-red cases the way `vault-synthesizer/cases.yaml` does — the failure mode evidence is the point.
- `evals/vision-critic/runner.py` — pytest harness. Reusable across critic agents.
- `evals/vision-critic/traces/baseline-2026-MM-DD.md` — first-run trace. Baseline must exist before the agent ships.
- `evals/bakeoffs/2026-MM-DD-sonnet-vs-gemini-vision-critic/` — dated bake-off folder. `cases.yaml` mirrors the vision-critic cases; `results.md` records per-case scores + qualitative notes + dollar-cost; `traces/` carries the raw runs from each model.

**Verify.** Em passes the baseline cases at the Sonnet 4.6 default before the bake-off runs. Bake-off result is the artifact, not the decision — Sean reviews the report, picks the production model, the loser's failure modes become museum content.

### Commit 9 — T3 multi-CLI critic ("Codie + Annie")

**Goal.** `pipeline/agents/cli_critic.py` — the vault-critic pattern transplanted. Codex CLI (gpt-5.5) + Anti-Gravity CLI (Gemini 3.1 Pro) in parallel. $0 incremental on subscriptions. Wires at two checkpoints: post-Animatic (Phase 4 → 5) and pre-Museum-publish (orthogonal).

**Land.**

- `pipeline/agents/cli_critic.py` — adapts `agents-sdk/agents/vault_critic.py` structurally. Same asyncio.gather subprocess fan-out, same per-CLI 120s timeout + 600s wall budget, same status promotion. Targets become images/videos (animatic shape-block, rendered museum walkthrough HTML/MDX) instead of markdown. Output is a comparison-card under `museum/{project_slug}/critics/` + a `proposed_patches:` entry on the run manifest.
- `pipeline/agents/prompts/codie-cli-critic-context.md` and `pipeline/agents/prompts/annie-cli-critic-context.md` — two role addenda. Same shared `anima-standing-context.md` preamble + supporting-doc injection from `manifest.yaml`'s `critics.t3.default_context_files`. Different role voices: Codie = production-discipline lens; Annie = narrative-coherence lens. Verify by ablation in commit 9b.
- `manifest.yaml` `critics:` block grows `t3.cli_a: codex`, `t3.cli_b: anti-gravity`, `t3.per_cli_timeout_s: 120`, `t3.wall_budget_s: 600`, `t3.default_context_files: [...]`, `t3.daily_cap_usd: 0` (subscription-absorbed).
- CLI surface mirrors vault-critic: `--target` / `--from-list` / `--force` / `--no-standing-context` / `--context` / `--no-default-context`. Manual-mode bypasses the nightly gate (which anima doesn't have, so this maps to "any artifact path").
- Verify Codex CLI + Anti-Gravity CLI both accept image/video input at the resolutions anima produces (Q3 from brainstorm §8). First hour of this commit.

### Commit 9b — `evals/cli-critic/`

**Goal.** Codie + Annie agreement-rate measurement + standing-context ablation runs.

**Land.**

- `evals/cli-critic/cases.yaml` — 10 cases, mix of clean animatic shape-blocks and intentionally-broken ones.
- `evals/cli-critic/agreement-rate.md` — measurement methodology. Codie + Annie scores per case, agreement rate, disagreement pattern analysis (where do they split? on which kinds of failures?).
- `evals/cli-critic/ablations/with-standing-context-vs-without.md` — confirms the preamble earns its keep on anima just as it did on vault-critic.

## Constraints

- **The architecture lock from 2026-05-24 and the agent-fleet decisions from 2026-05-25 are LOCKED.** Don't re-decide them. If something seems wrong on fresh reading, flag it before changing — don't silently correct.
- **Mirror `vault_critic.py` structurally for Commit 9.** Don't reinvent the asyncio + subprocess + status promotion pattern; it's proven. The adapter work is target type (image/video instead of markdown), output format (prompt-diff cards instead of expansion files), and persona naming.
- **Standing-context preamble is non-optional.** Every agent ships with one. Round 3 enrichment on vault-critic proved this; anima doesn't get to skip the proof.
- **`proposed_patches:` stages, never auto-applies in this session.** Director's chair UX comes later. For now Sean reviews the YAML directly.
- **Studio-manual voice.** Per the tonal directive — prose over tables where reasonable, no terminal-aesthetic in any new doc. Applies to CHANGELOG entries, the `evals/README.md`, every persona preamble file.
- **The pencil-test Act 2 work is still in flight.** Don't disturb it. The DAG runner ships behind `USE_DAG_RUNNER=1` flag so the linear path remains. Act 2 Seedance generation stays on the existing manifest's `act1:` / `anchor:` / `seedance:` blocks unchanged.

## Verify and CHANGELOG

After each commit:

- `CHANGELOG.md` gets an entry. "What changed" + "why" — capture rationale future sessions need.
- `CLAUDE.md` updates only if the change is structurally significant (new directory layout, new source-of-truth doc, new convention). Code-only changes do not trigger a CLAUDE.md update.
- Verify with the eval suite where one exists (commits 8b, 9b). For commit 4, verify via Act 2 byte-identical comparison of linear-path vs DAG-runner output.

## Remaining work after this session

Per change-map §4 + carry-overs:

- **Commit 2** — Character Bible migration (`characters/sean-anchor/` from the single anchor PNG, `character.yaml` schema). Smaller scope; brainstorm pending.
- **Commit 3 + 3b** — Brief→Plan planner wrapper ("Maya") + `evals/planner/`. Persona file lands here.
- **Commit 5** — Draft→Pro tier escalation wired into the DAG runner.
- **Commit 6** — Museum capture layer ("Mo") + Astro content-collection integration with `sw-ai-pm-portfolio`.
- **Commit 7** — Animatic ingestion (Procreate Dreams + Procreate PNG sequences).

Pending brainstorms:

- **Character Bible scaffolding** — gates commit 2. Cy's persona + character.yaml schema + authoring workflow.
- **Multimodal vault / RAG** — Gemini Embedding 2 vs OpenRouter, Obsidian integration, content-addressed asset store (ENG-5 from the original pipeline-v2 brainstorm).
- **Museum showcase format** — Mo's persona + comparison-GIF rendering pipeline + decision-ledger surfacing in walkthrough docs.
- **Pressure-test the locked architecture** — multi-perspective critique pass. Worth doing once commits 4, 8, 9 ship and the architecture has real agents inside it; doing it before is too early to find the interesting failure modes.

## Start

Begin by reading the binding docs in the listed order. Then read the three code-brain reference files. Then enter plan mode and produce a written implementation plan for commit 4 — what files land, what `AgentSpec` Protocol looks like, what the cache key derivation is, how the feature flag wires in. Sean reviews the plan before any code lands.

Once commit 4 is in, the implementation pattern for commits 8, 8b, 9, 9b is a copy of the same discipline: plan, review, ship, CHANGELOG, eval. Don't batch them — one commit per logical unit, one CHANGELOG entry per commit, one verification step per ship.
