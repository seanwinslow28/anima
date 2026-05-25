# Pipeline v2 — Change Map

**Date:** 2026-05-24
**Inputs:** [`docs/2026-05-24-pipeline-v2-brainstorm.md`](./2026-05-24-pipeline-v2-brainstorm.md) (5 architectural ideas + 2 principles locked)
**Purpose:** Concrete delta between today's codebase and the v2 strawman. What changes in which files, with what effort and what dependencies, plus a recommended commit sequence.

---

## 1. Current State (Ground Truth — 2026-05-24)

### `manifest.yaml` shape today
- `project:` — hardcoded to "Pencil Test — Sean Winslow"
- `anchor:` — single path to `images/2D-Character-Sketch-Sean-v1.png` (the Character Bible primitive doesn't exist; one image is the whole identity reference)
- `style:` — pencil-test specific (paper color, graphite line, hole-punch marks, etc.)
- `generation:` — single model config (Gemini NB2), single prompt source
- `act1:` — hardcoded keyframe definitions with frame numbers, poses, references, hold counts
- `audit:` — HF01-HF05 + SF01-SF05 + retry ladder (these generalize fine, just currently tuned to pencil test)
- `export:` — GIF / WebM / MP4 specs (generalize fine)

**Missing in current schema:** `phases:`, `tiering:`, `critics:`, `characters:`, `museum:`, `brief:`. No general `shots:` or `sequence:` abstraction.

### `pipeline/` scripts today
- `generate.py` (10.7KB) — main generation orchestrator with frame chaining
- `audit.py` (10.2KB) — rule-based HF/SF gate runner
- `assemble.sh` (7.3KB) — FFmpeg assembly + GIF/WebM/MP4 export
- `continuity_audit.py` (10.8KB) — frame-to-frame continuity QA (CC01-CC08)
- `seedance_generate.py` (30.7KB) — Seedance 2.0 API wrapper (Phase B.5)
- `seedance_lib.py` (9.7KB) — shared Seedance utilities
- `seedance_v2_audit.py` / `seedance_v2_cleanup.py` / `seedance_v2_select.py` — Seedance frame post-processing (already a mini-DAG)
- `seedance_bakeoff.py` + `seedance_bakeoff_variants.yaml` — variant testing harness
- `composite_sprite.py`, `blender_render_bvh.py`, `render_bvh_2d.py`, `generate_inbetweens.py` — experimental helpers

**The Seedance v2 sub-family is already DAG-shaped** (generate → audit → cleanup → select with intermediate artifacts). It's the proof-of-concept for the broader refactor.

### Docs source-of-truth today
- `CLAUDE.md` (19KB) names the project "Pencil Test — Sean Winslow", describes the 6-phase pipeline (Scaffold → Generate → Motion → Audit → Assemble → QA), references Act 1 / Act 2 specifics
- `CHANGELOG.md` (77KB) — decision log, append-only
- `docs/production-checklist.md` — phase status tracker

---

## 2. Change Map by Locked Decision

### TOP-1 — Animatic Phase

| | |
|--|--|
| Current state | Doesn't exist. Pipeline jumps from storyboard description to NB2 frame generation. |
| Target state | New Phase 4 between Storyboard and Generate. Sean authors a shape-block timing artifact (format TBD per Q1); pipeline ingests as a downstream constraint. |
| Delta | New manifest `animatic:` block; new `runs/{id}/animatic/` directory convention; new ingestion script; T3 critic checkpoint after this phase. |
| Files touched | `manifest.yaml` (+ `animatic:` block) · NEW `pipeline/animatic_ingest.py` · `CLAUDE.md` (10-phase diagram + new phase entry) |
| Effort | **M** (~2-3 evenings) |
| Blocks | Nothing critical, but the post-Animatic T3 critic gate is meaningless without it |
| Blocked by | Open Q1 — animatic format (Procreate Dreams / AE / PNG sequence) |

### TOP-2 — Brief → Plan → Approval gate (Phase 0)

| | |
|--|--|
| Current state | Doesn't exist. `manifest.yaml` is hand-authored from scratch per project. |
| Target state | Planner agent reads `brief.md`, emits a draft manifest + structured cost estimate; Sean approves before any model call. Approved plan seeds the manifest. |
| Delta | New `pipeline/planner.py` (Claude-driven, Haiku draft / Sonnet pro per draft→pro principle); brief.md template; plan.md schema; cost estimator (NB2 + Seedance + Claude tokens); CLI approval prompt or `--auto-approve` flag. |
| Files touched | NEW `pipeline/planner.py` · NEW `docs/brief-template.md` · `manifest.yaml` (extension hooks for planner-emitted fields) · `CLAUDE.md` |
| Effort | **M-L** (~3-5 evenings — planner prompt iteration is the variable) |
| Blocks | Project-Type templates (deferred), generalizing to "any project" |
| Blocked by | Open Q2 — brief format (free-text vs structured); few-shot examples from current pencil-test manifest |

### TOP-3 — Museum auto-capture layer

| | |
|--|--|
| Current state | `runs/{id}/audit/audit_log.jsonl` captures partial decisions. `assemble.sh` produces final frames. No structured walkthrough output. |
| Target state | Parallel `museum/{project_slug}/` tree. Every approve/reject/retry writes structured artifacts. Comparison GIFs auto-rendered. Static site generator produces a public walkthrough at end of run. T3 critic gate before publish. |
| Delta | Capture hooks injected at DAG node boundaries (depends on TOP-4); new `pipeline/museum_build.py`; static site template (Astro content-collection if museum publishes to portfolio, or standalone if separate); GIF comparison renderer. |
| Files touched | NEW `pipeline/museum_build.py` · NEW `templates/museum/*` · hook points in DAG nodes (post TOP-4) · `manifest.yaml` (+ `museum:` block) · `CLAUDE.md` |
| Effort | **L** (~5-7 evenings) |
| Blocks | "Pipeline as portfolio" thesis lives or dies here |
| Blocked by | TOP-4 (clean DAG hook points) · Open Q4 (Astro vs standalone) |

### TOP-4 — DAG refactor with content-hashed caching

| | |
|--|--|
| Current state | Linear shell-orchestrated flow. `generate.py` chains frames in sequence; `audit.py` validates; `assemble.sh` builds. Any config tweak re-runs the chain from the affected point. The Seedance v2 family is already DAG-shaped (proof point). |
| Target state | Typed DAG runner. Each node declares inputs / config / output type. Hash inputs+config; cache hit returns immediately; only downstream-of-edit re-runs. Pipeline phases become DAG subgraph tags for human readability. |
| Delta | New `pipeline/dag.py` runner; existing scripts refactored as DAG node types (`generate.py` → `nodes/frame_generate.py`, `audit.py` → `nodes/audit_gate.py`, etc.); content-addressed cache directory (`.cache/{sha256}/`); per-node tier awareness baked in. |
| Files touched | NEW `pipeline/dag.py` · NEW `pipeline/nodes/*.py` · refactor `generate.py` / `audit.py` / `assemble.sh` into node wrappers · `manifest.yaml` (nodes become first-class) · `CLAUDE.md` (architecture diagram update) |
| Effort | **L** (~7-10 evenings — biggest single commit) |
| Blocks | Museum capture (TOP-3), Draft→Pro state machine, future T2/T3 critic wiring |
| Blocked by | Open Q5 — DAG library choice (hand-rolled vs Prefect 3 vs Dagster). At solo-creator scale, **hand-rolled recommended**. |

### TOP-5 — Character Bible

| | |
|--|--|
| Current state | Single `images/2D-Character-Sketch-Sean-v1.png` is the only identity reference. Manifest references it as `anchor:`. |
| Target state | `characters/{character_id}/` folder per character with: `anchor.png`, `turnarounds/` (front/3-quarter/profile/back), `expressions/` (8-12 emotions), `costumes/{variant}/`, `props/`, `character.yaml` (palette, proportions, identity-drift triggers). Manifest references characters by ID; generator auto-loads relevant Bible sheets per shot. |
| Delta | New directory convention; migration of current anchor PNG → `characters/sean-anchor/anchor.png` (+ symlink for back-compat); manifest schema extension (`characters:` block, shot-level `character_id:` field); generator updated to load relevant Bible sheets per call. |
| Files touched | NEW `characters/sean-anchor/*` · `manifest.yaml` (+ `characters:` block) · `pipeline/generate.py` (reference-loading logic) · `CLAUDE.md` |
| Effort | **M** (~2-3 evenings) |
| Blocks | Multi-character shorts, character-design-extension work (turnarounds / variations / clothes swap) |
| Blocked by | Open Q3 — does pipeline support Bible *authoring* as a project type, or only *consuming*? Both eventually; consuming first. |

### Principle — Critic Stack (T1 / T2 / T3)

| | |
|--|--|
| Current state | T1 (rule-based HF/SF) implemented in `audit.py`. T2 (vision critic) does not exist. T3 (multi-CLI variance) does not exist. |
| Target state | T1 stays as-is. T2 + T3 implementations deferred to agent-fleet session, but checkpoints declared in manifest now. Phase 7 Audit role changes from "primary critic location" to "consolidation phase routing findings from distributed critics." |
| Delta | Manifest `critics:` block declaring which checkpoints run which tier (e.g. `post_animatic: T3`, `post_generate: T1+T2`, `post_motion: T2`, `post_assemble: T2`, `pre_museum_publish: T3`). No implementation this commit cycle. |
| Files touched | `manifest.yaml` (+ `critics:` block, schema-only) · `CLAUDE.md` (critic stack section) · NEW `docs/critic-stack-v1.md` (reference doc) |
| Effort | **S** for schema (~1 evening) · **L** for implementation (agent-fleet session, multiple weeks) |
| Blocks | "Critic earns its keep by proposing fixes" promise — full delivery depends on T2/T3 implementation |
| Blocked by | Agent-fleet session decisions (which model for T2, how to wire Codex/Anti-Gravity for T3, standing-context shared with vault-critic) |

### Principle — Draft → Pro escalation

| | |
|--|--|
| Current state | Only Seedance Fast → Pro is implemented (implicit in `prompts/seedance-template-v4.md`). No other phase has tier escalation. |
| Target state | Every DAG node declares `tier: draft \| pro` in config. Manifest `tiering:` block defines per-phase defaults + escalation rules (auto on critic-pass vs always human-approval). Cache layer keys outputs by tier; both available. Cost preview surfaces both tiers. 7 of 10 phases participate. |
| Delta | Manifest `tiering:` block; DAG runner respects tier; cache layer tier-aware; planner cost preview computes draft-only and draft→pro paths. |
| Files touched | `manifest.yaml` (+ `tiering:` block) · `pipeline/dag.py` (after TOP-4) · `pipeline/planner.py` (after TOP-2 — cost preview) · `CLAUDE.md` |
| Effort | **M** (schema is ~1 evening; full implementation needs DAG, ~3 evenings on top of TOP-4) |
| Blocks | Iteration speed / cost predictability |
| Blocked by | TOP-4 (DAG runner). Schema can land independently. |

---

## 3. Recommended First Commit (Monday) — DOC-ONLY FOUNDATION

Zero code changes. Risk-free. Establishes direction so subsequent commits don't drift.

**Files touched:**

| File | Change |
|------|--------|
| `CLAUDE.md` | Full rewrite — project rename (TBD — see open Q6), philosophy update (human+AI partnership thesis), 10-phase pipeline diagram with critic checkpoints, critic stack reference, draft→pro principle, Character Bible primitive, source-of-truth table refresh, Higgsfield/OiiOii/Krea attribution |
| NEW `docs/pipeline-architecture-v1.md` | Single source of truth for the 10-phase architecture. References brainstorm + change-map but is the canonical lock document |
| `manifest.yaml` | Backward-compatible schema extension only — add optional `phases:`, `tiering:`, `critics:`, `characters:`, `museum:`, `brief:` blocks **without removing current `act1:` / `anchor:` structure**. Current Act 1 runs still work. |
| `CHANGELOG.md` | Entry covering rebrand intent, 5 locked architectural ideas, 2 principles, rationale, links to brainstorm + change-map |
| NEW `docs/2026-05-24-pipeline-v2-change-map.md` | This doc |

**What is explicitly NOT in commit 1:** any change to `pipeline/*.py`, `pipeline/*.sh`, or removal of current manifest fields. Current pencil-test workflows keep running.

---

## 4. Recommended Sequencing After First Commit

| # | Commit | Touches | Effort | Why this order |
|---|--------|---------|--------|----------------|
| 2 | **Character Bible migration** | `characters/sean-anchor/` (migrate from `images/2D-Character-Sketch-Sean-v1.png`) · `manifest.yaml` `characters:` block honored · `generate.py` reference-loading | M | Independent of DAG; low-risk; immediately useful for any new character work; tests Bible schema before more complex projects need it |
| 3 | **Brief → Plan planner wrapper** | NEW `pipeline/planner.py` · `docs/brief-template.md` · plan.md schema · CLI approval UX | M-L | Independent of DAG; unlocks "any project" generalization; can use Haiku for draft tier; gives the Phase 0 ceremony first |
| 4 | **DAG runner refactor** | NEW `pipeline/dag.py` · NEW `pipeline/nodes/*.py` · existing scripts wrapped as nodes · cache directory | L | Foundation for everything downstream; biggest single commit; gates Museum, Draft→Pro full impl, future critic wiring |
| 5 | **Draft → Pro tier escalation in DAG** | `pipeline/dag.py` tier awareness · cache keys by tier · planner cost preview both tiers | M | Depends on commit 4 |
| 6 | **Museum capture layer** | NEW `pipeline/museum_build.py` · capture hooks in DAG nodes · static site template (Astro content-collection or standalone TBD) · comparison GIF renderer | L | Depends on commit 4 (hook points) |
| 7 | **Animatic ingestion** | NEW `pipeline/animatic_ingest.py` · `manifest.yaml` `animatic:` block honored · `runs/{id}/animatic/` convention | M | Independent of DAG technically; cleaner if DAG exists; format choice (open Q1) must be locked first |
| 8 | **T2 vision critic** | NEW `pipeline/critics/vision_critic.py` · wired into DAG nodes at Generate / Motion / Assemble checkpoints | M | Agent-fleet session deliverable; depends on commit 4 |
| 9 | **T3 multi-CLI critic** | NEW `pipeline/critics/cli_critic.py` (Codex + Anti-Gravity parallel) · wired at Animatic→Generate and pre-Museum-publish | M-L | Agent-fleet session deliverable; depends on commit 4 + agent-fleet decisions |

**Roughly 3-4 weeks of solo-evening pace** to land commits 1-7. Commits 8-9 follow the agent-fleet brainstorm session.

---

## 5. Open Decisions — RESOLVED (2026-05-24)

All commit-1 blockers cleared.

| # | Decision | Answer | Status |
|---|----------|--------|--------|
| Q6 | Project rename | **`anima`** (Latin: breath/soul) | Commit 1 unblocked |
| Q5 | DAG library | **Hand-rolled minimal runner** (see §6) | Commit 4 unblocked |
| Q2 | Brief format | **Free-text markdown** (tonal directive: prose over tables where reasonable) | Commit 3 unblocked |
| Q4 | Museum target | **Astro content collection in `sw-ai-pm-portfolio`** | Commit 6 unblocked |
| Q1 | Animatic format | **Procreate Dreams + Procreate PNG sequences** | Commit 7 unblocked |
| Q3 | Bible authoring | **Both — authoring-first as a Project-Type** | Commit 2 unblocked |

**Commit 1 ships as `anima` in CLAUDE.md + manifest.yaml + CHANGELOG.md.** Directory rename (`sw-portfolio-animation-pipeline/` → `anima/`) deferred to public-repo creation time so git history stays clean during the transition.

---

## 6. DAG Library Recommendation — Hand-Rolled (Locked 2026-05-24)

**Recommendation:** Build `pipeline/dag.py` from scratch as a minimal Python DAG runner (~300-500 LOC).

**Why not Prefect 3 / Dagster / Luigi / Airflow:**

Solo-creator scale never crosses ~200 nodes per run, and heavyweight workflow engines are designed for distributed/team workflows with scheduling, retry policies, and dashboards — none of which anima needs. New dependency = version drift + abstraction tax; Prefect 3 alone is ~30MB of transitive deps and brings its own opinions about runs/deployments/flows that fight anima's manifest-driven shape. Content-addressed caching with multimodal inputs (image bytes + prompt + model config) is easier to control end-to-end in pure Python than fighting a framework's cache-key system. Stack traces beat framework magic — easier to debug, easier to teach, easier to put on the museum walkthrough page. And the museum's job is to *show the work*, which means the work has to be readable: hand-rolled code is portfolio gold, "I configured Prefect" is not.

The Seedance v2 sub-family (already DAG-shaped: `seedance_generate` → `seedance_v2_audit` → `seedance_v2_cleanup` → `seedance_v2_select`) is the proof point that hand-rolling scales fine at this domain.

**What the runner needs:**

- Typed `Node` Protocol: declares input types, output type, config, `tier: draft | pro`
- Topological sort + parallel execution via `concurrent.futures.ThreadPoolExecutor` (or `ProcessPoolExecutor` for CPU-heavy nodes)
- Content-addressed cache: `cache/{sha256_of_inputs_and_config}.{ext}` + `.json` sidecar
- Tier-aware cache keys so draft and pro outputs both persist
- Hook system (observer pattern) for capture: Museum, evals, traces — all subscribe to node-completion events
- Feature flag (`USE_DAG_RUNNER=1`) so the linear path remains usable during the migration

Inspirations to *skim, not adopt wholesale*: `doit` (file-based DAG semantics), `make` (content-addressed thinking), `snakemake` (wildcard pattern matching for batch nodes).

---

## 7. NEW Workstream — Evals + Traces (Locked 2026-05-24)

**Scope:** Mirror the `code-brain/evals/vault-synthesizer/` pattern for anima's agents and for empirical model selection.

**Pattern reference:** That suite ships intentionally red — each ❌ is a real production failure mode the eval catches. Pre-fix baseline (1/10 passing) → post-fix (7/10) is the artifact. Cases grounded in 17 days of real production logs, not imagined failure modes. Discipline transferred from Hamel Husain, Shreya Shankar, and Anthropic's "Demystifying Agent Evals" canon. The README itself is a portfolio piece.

**Directory structure (proposed):**

```
evals/
├── README.md                  ← portfolio-grade write-up + pattern citations
├── planner/
│   ├── cases.yaml             ← brief → expected manifest shape; 10 cases grounded in real briefs
│   ├── runner.py              ← pytest harness
│   ├── conftest.py
│   ├── failure-modes.md       ← observed failure taxonomy
│   ├── last-run.md            ← most recent run summary
│   └── traces/                ← open-coded traces of real runs
├── vision-critic/             ← T2 critic eval (Generate, Motion, Assemble checkpoints)
├── cli-critic/                ← T3 multi-CLI critic eval (Animatic→Generate, pre-Museum-publish)
└── bakeoffs/                  ← model head-to-head reports (first-class artifact, like seedance_bakeoff)
    ├── README.md
    └── 2026-MM-DD-{model_a}-vs-{model_b}-{job}/
        ├── cases.yaml
        ├── results.md
        └── traces/
```

**Two parallel use cases:**

1. **Agent quality regression.** Each agent (planner, vision critic, CLI critic) ships with its eval suite from day one. Cases grounded in real production logs (or seeded fixtures during pre-production), not imagined failure modes. The discipline is: no agent ships without a baseline run captured in `traces/baseline-*.md`.
2. **Model bake-offs.** Architecture decisions like *"Gemini 3 Pro vs Claude Sonnet for vision critic"* run as dated bake-offs against the same eval cases. Results become museum content — the empirical record of *why* a particular model is in production. Mirrors how `seedance_bakeoff.py` already worked for Seedance variants and how `docs/Image-Model-DR-2026/SYNTHESIS.md` ran cross-model deep-research comparison for image gen.

**Sequencing in the commit plan:**

| Commit | Eval addition |
|--------|---------------|
| Commit 3 (planner wrapper) | **Commit 3b**: `evals/planner/` scaffold + initial 5-10 cases (this sets up the shared `runner.py` / `conftest.py` patterns) |
| Commit 8 (T2 vision critic) | **Commit 8b**: `evals/vision-critic/` + bake-off `bakeoffs/2026-MM-DD-gemini3pro-vs-sonnet-vision-critic/` |
| Commit 9 (T3 CLI critic) | **Commit 9b**: `evals/cli-critic/` + Codex/Anti-Gravity agreement-rate measurement |

**Each agent commit is gated by its eval suite.** No green light without a baseline trace.

**Effort:** S per eval suite once the pattern's established (~1 evening for scaffold + 5-10 cases). M for the first one (commit 3b) because it lays down `runner.py` + `conftest.py` + `README.md` templates the others reuse.

**Blocks / blocked by:** Independent of pipeline foundation commits 1-2. First eval suite lands with commit 3 (planner).

---

## 8. Risk Notes

- **Manifest schema additions must be backward-compatible in commit 1.** If `act1:` block is removed before commit 4 lands, current pencil-test workflows break. Use additive extension only.
- **DAG refactor (commit 4) is the highest-risk change.** Recommend a feature flag (`USE_DAG_RUNNER=1`) so the linear path remains available during the transition. Both can coexist for the duration of commits 4-7.
- **Critic schema declared without implementation (commit 1) is a checked promise.** The `critics:` block ships before T2/T3 exist; this is fine as long as the agent-fleet session lands within ~4 weeks. Otherwise the schema becomes vestigial.
- **Museum capture without DAG hooks (if commit 6 attempted before commit 4) becomes a maintenance burden.** Hooks scattered across `generate.py` / `audit.py` / `assemble.sh` are exactly what the DAG refactor consolidates. Don't shortcut the order.
