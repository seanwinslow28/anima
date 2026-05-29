# anima

A pipeline for 2D animation made by a human and a fleet of agents working together. The name is Latin — *breath*, *soul* — short enough to fit anywhere, available enough to grow into.

The premise is older than the tools: the human owns timing, casting, and taste. The agents own everything that can be made cheap, parallel, and structured — and they *propose*, they don't decide. The pipeline is where the two meet. Brief becomes plan; plan becomes animatic; animatic constrains motion; motion gets cleaned to the aesthetic; everything that happened along the way gets captured into a public walkthrough.

anima came out of shipping a single piece — **Pencil Test — Sean Winslow** (Act 1 shipped, Act 2 in progress). That work is the first reference implementation, not the project's definition. The shape of the system was suggested by three structural ancestors worth crediting: Higgsfield's plan-approve-execute pattern, OiiOii's small named-agent crew, and Krea's content-addressed node graph. None of them are the same thing as this — but they were the right places to steal architecture from.

## Start Here

Every session, read **[`PHILOSOPHY.md`](PHILOSOPHY.md)** first — it's the load-bearing intent document, the soul of what anima is for. The architecture serves the philosophy, not the other way around. Then **[`docs/pipeline-architecture-v1.md`](docs/pipeline-architecture-v1.md)** for the canonical 10-phase architecture lock. After that, **[`docs/production-checklist.md`](docs/production-checklist.md)** tracks where the current work actually is (Pencil Test status across acts and frames). Update the checklist as work completes.

## Maintenance Conventions

These rules apply to **every** Claude Code session working in this project. They override default behavior — keep CLAUDE.md and CHANGELOG.md trustworthy, or future sessions start from a wrong premise.

- **CHANGELOG.md — update on every change.** Whenever you add, modify, remove, refactor, or reorganize anything (code, docs, prompts, manifest, repo structure, conventions), append a CHANGELOG entry. Capture **what changed and why** so future sessions understand the rationale and don't undo intentional decisions. Date the entry. Group related changes under one heading. The CHANGELOG is the project's decision log — not a release-note tally.

- **CLAUDE.md — update on significant project changes.** When the project's structure, pipeline phases, conventions, source-of-truth documents, naming, or active phase shifts, update CLAUDE.md so it reflects the **current** state. CLAUDE.md is what every future session reads first; if it points at the wrong files or describes a stale architecture, the session starts wrong.
  - "Significant" = anything that changes how someone works on the project: new pipeline phase, new directory layout, new source-of-truth doc, new tools/dependencies, document moves, new conventions.
  - Routine code edits, single-file content tweaks, small bug fixes do NOT require a CLAUDE.md update — only a CHANGELOG entry.

- **Archive convention — `COMPLETED/` and `OLD/` subfolders.** Within `docs/` and `prompts/`, completed (shipped, done) and old (superseded) artifacts live in `COMPLETED/` and `OLD/` subdirectories respectively. The roots stay focused on what's active. When you finish a phase or supersede a doc, move it into the correct archive folder rather than leaving it in the root. Use `git mv` so renames are tracked.

## The 10-Phase Pipeline

```
Phase 0  BRIEF & PLAN       brief.md → planner agent → plan.md + cost estimate → human gate
Phase 1  SCAFFOLD           project structure + manifest skeleton
Phase 2  CHARACTER BIBLE    characters/{id}/ folders authored or referenced
Phase 3  STORYBOARD         beat sheet + shot list (largely human-authored)
Phase 4  ANIMATIC           shape-block timing pass (Procreate Dreams / Procreate PNG)
                            ⚖ T3 critic gate
Phase 5  GENERATE           NB2 stills, DAG-orchestrated, multi-character Bible-loaded
                            ⚖ T1 + T2 critics
Phase 6  MOTION             Seedance video between approved anchors, draft → pro escalation
                            ⚖ T2 critic
Phase 7  AUDIT              consolidation — routes critic findings to retry ladder
Phase 8  ASSEMBLE           FFmpeg, comparison GIFs, museum capture fires
                            ⚖ T2 critic
Phase 9  QA REVIEW          creative-director + final human gate

(parallel)  MUSEUM          every approve/reject/retry writes capture artifacts
                            ⚖ T3 critic gate before publish
```

**Phase 0 — Brief & Plan.** A free-text markdown brief becomes a structured plan: which phases run, how many frames, which characters get loaded, draft prompts, retry budget, and an *estimated* model spend. Approval is a human gate; nothing burns compute until the plan is approved.

**Phase 1 — Scaffold.** File structure, manifest skeleton, run directory layout. Free.

**Phase 2 — Character Bible.** Each character lives in its own folder with an anchor, turnarounds, expression sheets, and a `character.yaml`. The single-anchor pattern from the pencil-test era is gone; a character is a whole library that the generator loads selectively per shot.

**Phase 3 — Storyboard.** Beat sheet plus shot list. Mostly human-authored — agents assist with prompt drafts and continuity checks; they don't pick beats.

**Phase 4 — Animatic.** The load-bearing pre-production stage. Sean blocks motion and timing in simple shapes — Procreate Dreams when the artifact wants to be a video, Procreate PNG sequences when it wants to be a stack of hand-drawn keys. The pipeline ingests either as a motion-and-timing constraint downstream. A **T3 critic gate** runs here because everything after this point is expensive; if the timing arc didn't land in shapes, no amount of Seedance compute will save it.

**Phase 5 — Generate.** NB2 produces stills, DAG-orchestrated with content-hashed caching so editing one prompt only re-runs its node and downstream. Character Bibles load per shot. **T1** is the existing HF/SF rule gates; **T2** is a vision critic that reads the frame against the beat description and *proposes* prompt diffs, not pass/fail.

**Phase 6 — Motion.** Seedance generates fluid motion video between approved anchor stills. Draft tier (Fast) is the production default; pro tier (Standard) is reserved for shots that need it. A **T2 critic** reviews motion arc and identity drift in video output — the existing gap where Seedance currently isn't QA'd beyond visual review.

**Phase 7 — Audit.** Consolidation. Used to be where critique happened; now it's where critique findings from Phases 4-6 get *routed* to the retry ladder. No new critique here.

**Phase 8 — Assemble.** FFmpeg builds the cut. Comparison GIFs render automatically where a manual reference exists. Museum capture hooks fire as nodes complete. A **T2 critic** reads loop coherence and pacing across the whole cut, not just per-frame.

**Phase 9 — QA Review.** The `creative-director` skill runs its critique rubric, and a human takes the last look. Single human pass; no escalation.

**Museum (orthogonal).** Not a phase — a capture layer that runs in parallel with everything else. Every approval, every reject, every retry decision writes structured artifacts to a `museum/{project_slug}/` tree. At the end of a run, a static site generator (Astro content collection targeted at `sw-ai-pm-portfolio`) renders a public walkthrough. The **T3 critic gate** before publish gives multi-CLI variance the strongest read on whether narrative + comparison artifacts hold up under independent eyes.

The full per-phase spec (inputs, outputs, draft/pro tiers, status) lives in [`docs/pipeline-architecture-v1.md`](docs/pipeline-architecture-v1.md). This section is the orientation.

## The Critic Stack

The critic earns its keep when it proposes fixes, not when it flags problems. Three tiers, escalating in cost and signal:

| Tier | What it is | When it runs | Cost / latency |
|------|------------|--------------|----------------|
| **T1** | Rule gates — HF/SF/CC reason codes, PIL dimension checks. Deterministic, instant. | Every frame, every node | $0, <100ms |
| **T2** | Vision critic — Claude or Gemini reviews output against beat description + style guide. **Proposes prompt diffs**, not pass/fail. | Per major node output (Generate, Motion, Assemble) | ~$0.01–0.05 per call, 5–15s |
| **T3** | Multi-CLI variance — Codex CLI + Anti-Gravity CLI run in parallel. The vault-critic pattern, $0 incremental on subscriptions. | Phase transitions only | $0 incremental, ~120s per CLI |

Placement of the five named checkpoints is locked here in commit 1. Implementation of T2 + T3 belongs to the agent-fleet session. Phase 7 Audit's role has changed: it is no longer *where critique happens*; it is where critique findings are *consolidated and routed* to the retry ladder.

## Draft → Pro Escalation

Every expensive node declares a draft tier and a pro tier. Default behavior: run draft, present the preview, escalate to pro on approval or critic-pass. The Seedance Fast→Pro pattern already in [`prompts/seedance-template-v4.md`](prompts/seedance-template-v4.md) is the prototype; anima generalizes it to a pipeline-wide convention.

Seven of the ten phases participate. Cost-light or human-only phases (Scaffold, Audit, QA Review) opt out. The principle pairs naturally with museum capture: draft outputs aren't waste, they're evidence of iteration — the walkthrough renders "we tried draft, here's what it showed, here's why we committed to pro." A compute-cost optimization becomes a narrative asset.

Full per-phase coverage table lives in [`docs/pipeline-architecture-v1.md`](docs/pipeline-architecture-v1.md) §Draft → Pro Coverage.

## The Character Bible Primitive

A character is no longer a single PNG. It is a folder.

```
characters/{character_id}/
├── character.yaml        # palette, proportions, identity-drift triggers
├── anchor.png            # primary identity reference (replaces the old A-2 single anchor)
├── turnarounds/          # front, 3-quarter, profile, back
├── expressions/          # 8-12 emotional states
├── costumes/{variant}/   # outfit variations
└── props/                # key prop attachments (the stylus, etc.)
```

The manifest references characters by ID; the generator auto-loads the relevant Bible sheets per shot. Bible authoring is itself a use case anima supports — the same pipeline that consumes a Bible can also produce one, with its own Project-Type template (authoring-first).

The migration from `images/2D-Character-Sketch-Sean-v1.png` → `characters/sean-anchor/anchor.png` shipped in commit 2.0 (2026-05-28). The legacy path is now a back-compat symlink resolving to the new location; it stays in place through commit 7 (Animatic ingestion lands and Act 2 work is structurally complete), then retires. Pencil-test scripts that haven't been updated to the new path keep working unchanged during the back-compat window.

## Source of Truth Documents

| Document | Path | Role |
|----------|------|------|
| **Pipeline Architecture (v1)** | [`docs/pipeline-architecture-v1.md`](docs/pipeline-architecture-v1.md) | **Canonical architecture lock — read first every session.** 10-phase spec, critic stack, draft→pro, Character Bible primitive, museum layer, reserved open questions |
| **Production Checklist** | [`docs/production-checklist.md`](docs/production-checklist.md) | Current status of the in-flight pencil-test work — phases, frames, assets |
| Pipeline v2 Brainstorm | [`docs/2026-05-24-pipeline-v2-brainstorm.md`](docs/2026-05-24-pipeline-v2-brainstorm.md) | Historical artifact — the 15-idea PM/Designer/Engineer brainstorm that produced the v2 lock. Read for *why*, not *what* |
| Pipeline v2 Change Map | [`docs/2026-05-24-pipeline-v2-change-map.md`](docs/2026-05-24-pipeline-v2-change-map.md) | Historical artifact — 9-commit sequence, file-by-file delta, DAG library rationale, evals workstream scope |
| **Maya Planner Brainstorm** | [`docs/2026-05-26-maya-planner-brainstorm.md`](docs/2026-05-26-maya-planner-brainstorm.md) | Phase 0 design decisions — Top 5 locked (two-tier brief, graph criteria, cost-estimator AgentSpec, audited mutation contract, adversarial Sonnet pass), deferred items with promotion triggers, file map. Drives commits 3 + 3b |
| **Anti-Gravity CLI Findings** | [`docs/research/2026-05-26-anti-gravity-cli-findings.md`](docs/research/2026-05-26-anti-gravity-cli-findings.md) | The Antigravity CLI migration — binary `gemini` → `agy`, new flag shape, `@path` image attachment, 2026-06-18 sunset. Drives commit 8.1 (Em's CLI wrapper patch) |
| **Prompt Style-Neutrality Doctrine** | [`docs/prompt-style-neutrality-doctrine.md`](docs/prompt-style-neutrality-doctrine.md) | One-page doctrine on keeping anima's prompts style-agnostic across the six closed-vocabulary style registers. Enforced at CI time by [`tests/test_prompt_style_neutrality.py`](tests/test_prompt_style_neutrality.py). Read before adding a new register or editing a standing-context preamble |
| Manifest | [`manifest.yaml`](manifest.yaml) | Pipeline configuration — current state has both the pencil-test reference blocks and the new optional v2 schema blocks |
| Changelog | [`CHANGELOG.md`](CHANGELOG.md) | Decision history — what changed, why, and lessons learned |
| **Seedance Prompt Template (v4)** | [`prompts/seedance-template-v4.md`](prompts/seedance-template-v4.md) | Canonical Seedance 2.0 prompt template. Fast tier is the production default. Also packaged as the portable `seedance-prompting` skill at `~/.claude/skills/seedance-prompting/SKILL.md` |
| Seedance Research | [`docs/research/seedance-research-findings.md`](docs/research/seedance-research-findings.md) | Seedance 2.0 capabilities, API specs, prompting guide |

### Pencil Test — First Reference Implementation

The pencil-test work is anima's first reference implementation, not the whole project. Its docs are still authoritative for that piece, and are framed accordingly:

| Document | Path | Role (within Pencil Test) |
|----------|------|---------------------------|
| Storyboard | [`docs/pencil-test-storyboard.md`](docs/pencil-test-storyboard.md) | Complete storyboard — 7 beats, 2 acts, frame counts |
| Keyframe Prompts (Act 1, archived) | [`docs/COMPLETED/act1-keyframe-prompts.md`](docs/COMPLETED/act1-keyframe-prompts.md) | 6 Gemini prompts that produced the Act 1 key poses (shipped — kept for re-runs) |
| A-2 Anchor | [`characters/sean-anchor/anchor.png`](characters/sean-anchor/anchor.png) | Identity reference for the Sean character. Migrated 2026-05-28 in commit 2.0; legacy path [`images/2D-Character-Sketch-Sean-v1.png`](images/2D-Character-Sketch-Sean-v1.png) is a back-compat symlink through commit 7 |
| Act 2 Seedance Shot List | [`docs/act2-seedance-shot-list.md`](docs/act2-seedance-shot-list.md) | Current source of truth for Act 2 — 10 clips + 4 holds, anchor frame paths, draft prompts, fallback strategies |
| Act 2 Seedance Execution Plan | [`docs/2026-04-27-act2-seedance-execution-plan.md`](docs/2026-04-27-act2-seedance-execution-plan.md) | Approved 12-task implementation plan for the Seedance generation phase |
| Round 2 Beat Decisions | [`runs/act2-exploration/concepts/round2-decisions.md`](runs/act2-exploration/concepts/round2-decisions.md) | Locked Act 2 11-beat sheet |
| Seedance Production Plan (archived) | [`docs/OLD/seedance-production-plan.md`](docs/OLD/seedance-production-plan.md) | Superseded for Act 2; Act 1 sections valid as historical reference |
| Original Pipeline Notes | [`docs/Sprite-Sheet-Automation-Project_OG-Workflow-Summary.md`](docs/Sprite-Sheet-Automation-Project_OG-Workflow-Summary.md) | Architectural ancestor — manifest-driven design, audit loop, retry ladder |

## Skills Map

Skills map to the 10-phase architecture. Most carry over from the pencil-test era; a few are pending the agent-fleet session.

| Skill | Phase(s) | Role |
|-------|----------|------|
| `gemini-pencil-animation-image-gen` | 5 Generate | Primary keyframe generator — pencil test style via Gemini Nano Banana 2 |
| `gemini-image-gen` | 5 Generate | Non-pencil assets — zone backgrounds, props |
| `image-generator-prompt-science` | 5 Generate | 7-Layer prompt framework, refinement tips for retries |
| `animation-pipeline` | All | Pipeline orchestration — manifest-driven generation, frame chaining, QA gates (HF/SF/CC), assembly |
| `2d-animation-principles` | 4 Animatic, 7 Audit, 8 Assemble | Animation physics, timing/spacing validation, expression arc, hold duration |
| `creative-director` | 9 QA Review | Critique rubric (Identity/Style/Composition/Continuity/Technical), prompt refinement as art direction |
| `comfyui-workflows` | 5 Generate (in-betweens) | OpenPose ControlNet in-between generation, IPAdapter identity lock |
| `seedance-prompting` (portable) | 6 Motion | Locked v4 Seedance prompt template; auto-loads in any project |
| `video-animation-production` | 6 Motion, 8 Assemble | FFmpeg frame sequence assembly, two-pass GIF optimization, WebM/MP4 export |
| `planner` — Maya | 0 Brief & Plan | Opus 4.8 primary → Sonnet 4.6 adversarial validation → human gate. Emits two-tier brief (Studio + Production) + v1.1 graph-shaped `acceptance_criteria.json` + clean-markdown `plan.md` + `RunCostEstimate` from `CostEstimatorNode`. Three-call ceiling. `project_type: bible_authoring` scopes plan.md to Phase 0 + Phase 2 only. CLI: `python -m pipeline.cli plan init/show/approve/mutate`. Commit 3 shipped 2026-05-27 |
| `character_designer` — Cy | 2 Character Bible | Opus 4.8 authors (Pass 1) → NB Pro generates plates (Pass 2) → Gemini 3.1 Pro verifies via `agy` (Pass 3). Three-attempt ceiling per plate. **Plate-generation contract (fidelity fix, 2026-05-29):** the runner is the source of truth for references — `anchor.png` is injected first on every `generate` plate, source-refs are kept, references to other generated plates are stripped (no chaining); plate prompts are short plate-intent wrapped in runner-owned reference-role-tag framing, never verbal character re-descriptions or pipeline-meta text. **Pass-2.5 pixel-similarity gate** (`pipeline/agents/similarity_gate.py`, DINOv2→CLIP→PIL ladder) scores each plate vs the anchor before Gemini's prose Pass-3 and persists a per-plate verdict trail to `runs/{run_id}/plate_verdicts.jsonl`. **`#region:NAME` ingest crops** read a `<sheet>.regions.json` sidecar (fractional/pixel boxes) and crop the source sheet; unmappable regions fall back to a full copy flagged `region_not_cropped` (never a silent wrong crop). Emits `character.yaml` + per-character `acceptance_criteria.json` (v1.2 graph with `IR.{character_id}.*` entries) + `risk-bible.md` + `cy-confidence-notes.md` + `plate_generation_plan.json`. CLI: `python -m pipeline.cli bible init/show/approve/mutate/iterate`. Commit 2 shipped 2026-05-28 |
| `vision_critic` — Em | 5, 6, 8 (T2 checkpoints) | Gemini 3.1 Pro via Anti-Gravity CLI default, Opus 4.7 via Claude Agent SDK escalation. Patches stage in `manifest.lock.yaml`. Commit 8 shipped 2026-05-26 |
| _(CLI critic)_ | 4→5, pre-Museum (T3 checkpoints) | Pending agent-fleet session — Codex + Anti-Gravity parallel |

## Directory Structure

The working directory is `sw-portfolio-animation-pipeline/` for now. The rename to `anima/` happens at public-repo creation time so git history stays clean during the transition. New top-level conventions (`characters/`, `museum/`, `evals/`) are marked planned — they land across commits 2-8.

```
sw-portfolio-animation-pipeline/        # renames to anima/ at public-repo creation
├── CLAUDE.md                            # This file — anima project manual
├── CHANGELOG.md                         # Decision log (append on every change)
├── manifest.yaml                        # Pipeline configuration (v1 + v2 blocks coexist)
├── docs/                                # Active source-of-truth documents
│   ├── pipeline-architecture-v1.md      # Canonical architecture lock
│   ├── production-checklist.md
│   ├── 2026-05-24-pipeline-v2-brainstorm.md
│   ├── 2026-05-24-pipeline-v2-change-map.md
│   ├── pencil-test-storyboard.md
│   ├── act2-seedance-shot-list.md
│   ├── 2026-04-27-act2-seedance-execution-plan.md
│   ├── research/                        # External research notes
│   ├── COMPLETED/                       # Shipped/done plans + prompts (Act 1)
│   └── OLD/                             # Superseded docs (do not act on)
├── prompts/
│   ├── seedance-template-v4.md          # Canonical Seedance prompt template
│   ├── act2/                            # Current Act 2 prompts
│   ├── COMPLETED/                       # Shipped Act 1 prompts
│   └── OLD/                             # Superseded session prompts
├── images/                              # Reference assets (Pencil Test era)
│   └── 2D-Character-Sketch-Sean-v1.png  # Back-compat symlink → characters/sean-anchor/anchor.png (retires commit 7)
├── pipeline/                            # Pipeline scripts
│   ├── generate.py                      # Generation orchestrator with frame chaining (USE_DAG_RUNNER=1 routes to dag.py)
│   ├── audit.py                         # T1 rule gate runner (USE_DAG_RUNNER=1 routes to dag.py)
│   ├── continuity_audit.py              # CC01-CC08 frame-to-frame continuity
│   ├── assemble.sh                      # FFmpeg assembly
│   ├── seedance_*.py                    # Seedance 2.0 generation, extract, audit, cleanup
│   ├── agents/                          # AgentSpec Protocol + critic agents
│   │   ├── __init__.py                  # AgentSpec, AgentResult, Patch, register_node (commit 4)
│   │   ├── vision_critic.py             # Em — T2 vision critic (commit 8)
│   │   ├── cli_runners.py               # Anti-Gravity CLI wrapper + stub fallback (commit 8)
│   │   ├── sdk_runners.py               # Claude Agent SDK / anthropic SDK wrapper + stub (commit 8)
│   │   ├── patch_stager.py              # post_run hook → runs/{run_id}/manifest.lock.yaml (commit 8)
│   │   └── prompts/                     # Persona standing-context preambles (commit 8)
│   ├── cli/                             # `python -m pipeline.cli` subcommands
│   │   ├── patches.py                   # `patches list` — survey staged proposed_patches (commit 8)
│   │   ├── plan.py                      # Maya plan init/show/approve/mutate (commit 3)
│   │   └── bible.py                     # Cy bible init/show/approve/mutate/iterate (commit 2)
│   ├── criteria.py                      # acceptance_criteria.json v1.2 schema (AC.* + IR.* graph) + lock enforcement (commit 4 + commit 2)
│   ├── dag.py                           # Hand-rolled DAG runner (commit 4)
│   ├── agents/character_designer.py    # Cy's three-phase AgentSpec (commit 2)
│   ├── agents/nb_pro_runner.py         # NB Pro plate-generation wrapper, content-addressed cache (commit 2)
│   └── nodes/                           # AgentSpec wrappers around legacy scripts (commit 4)
├── characters/                          # Character Bible folders (Bible primitive — commit 2.0 + commit 2 scaffolded sean-anchor + claude-mascot)
│   ├── sean-anchor/                     # Sean's Bible — pencil-test-colored register; first reference implementation
│   │   ├── anchor.png                   # The migrated A-2 reference (legacy path is a symlink → here)
│   │   ├── character.yaml               # Scaffolded template; Cy populates in Task 1.10's real authoring run
│   │   ├── turnarounds/ expressions/ motion_plates/ costumes/default/ props/  # Cy populates per Pass-1 plate plan
│   │   └── source-refs/                 # POPULATED: notes.md, turnaround-{1,2}.png, head-turn/{1..9}.png,
│   │                                    #   walk-cycle/{source,derived-v1,derived-v2}.png, 3d-mannequin/
│   ├── claude-mascot/                   # Claude Mascot Bible — pixel-art-8bit register; second-character schema validation
│   │   ├── anchor.png                   # claude-mascot-2.png (2048×2048), the canonical identity reference
│   │   ├── character.yaml               # Scaffolded template; Cy populates in Task 1.11's real authoring run
│   │   ├── turnarounds/ expressions/ motion_plates/ costumes/default/ props/
│   │   └── source-refs/                 # POPULATED: notes.md (palette + proportion + grid invariants),
│   │                                    #   claude-mascot-{1,3}.png as secondary references
│   └── _per-character_                  # Each Bible folder is self-contained; manifest's characters: dict
│                                        #   registers folder + style_register. criteria_sources: lists the
│                                        #   per-character acceptance_criteria.json paths for runtime merge.
├── museum/                              # PLANNED (commit 6) — capture artifacts per run
├── evals/                               # Agent eval suites + dated bake-offs
│   └── vision-critic/                   # Em eval suite (commit 8 baseline trace, 8b adds cases.yaml + runner.py)
└── runs/                                # Per-run output (gitignored)
    └── {run_id}/
        ├── manifest.lock.yaml           # Frozen config snapshot
        ├── candidates/                  # All generated candidates (preserved)
        ├── approved/                    # Approved keyframes
        ├── rejected/                    # Rejected frames with failure codes
        ├── audit/                       # Audit logs
        ├── animatic/                    # PLANNED (commit 7) — shape-block timing artifact
        └── export/                      # Final outputs
```

## Asset Naming Convention

The current naming pattern stays in place for the pencil-test reference implementation:

```
PT_{ActID}_{FrameNumber}_{AssetType}.{ext}
```

| Example | Meaning |
|---------|---------|
| `PT_A1_F06_key.png` | Pencil Test, Act 1, Frame 6, keyframe |
| `PT_A1_F18_key.png` | Pencil Test, Act 1, Frame 18, keyframe |
| `PT_A2_F97_key.png` | Pencil Test, Act 2, Frame 97, keyframe |

Candidates: `F{##}/attempt_{##}.png` (e.g., `F06/attempt_01.png`)
Rejected: `F{##}_attempt_{##}_{FAIL_CODE}.png` (e.g., `F06_attempt_01_SF01.png`)

Future anima projects use their own project prefixes (`{PROJECT}_{ActID}_{FrameNumber}_{AssetType}.{ext}`).

## Manifest Schema

`manifest.yaml` carries two generations of schema side by side. The pencil-test reference implementation uses the original blocks; the v2 architecture is declared in new additive blocks that point at the architecture doc for their semantics.

**Existing (untouched, backward-compatible):**

- `project:` — name, version, description (only `name` updated to `"anima"` in commit 1; description retained)
- `anchor:` — single-character reference (deprecated by `characters:`; still authoritative for Act 2 in flight)
- `style:` — pencil-test aesthetic constraints
- `generation:` — Gemini NB2 model config
- `act1:` — Act 1 keyframe definitions
- `audit:` — Hard fails (HF01-HF05) + soft fails (SF01-SF05) + retry ladder
- `export:` — GIF / WebM / MP4 specs

**New (additive, schema-only in commit 1; wiring lands across commits 2-7):**

- `phases:` — 10-phase architecture node enablement. See [`docs/pipeline-architecture-v1.md`](docs/pipeline-architecture-v1.md)
- `tiering:` — draft → pro escalation defaults per phase
- `critics:` — T1/T2/T3 checkpoint placement
- `characters:` — Character Bible registry (commit 2)
- `museum:` — auto-capture configuration + publishing target
- `brief:` — Phase 0 brief file convention (commit 3)

## QA Gates

### Hard Fails (Blocking — instant reject)

| Code | Name | Test |
|------|------|------|
| HF01 | Wrong aspect ratio | Image is not 16:9 (within 2% tolerance). Checked via PIL. |
| HF02 | Missing paper texture | Background is pure white, gray, or lacks cream paper grain |
| HF03 | Wrong direction | Character orientation doesn't match storyboard beat |
| HF04 | Wrong pose | Pose doesn't match storyboard description (e.g., arms down when should be raised) |
| HF05 | Wrong aesthetic | Digital/anime/3D render look instead of pencil test drawing |

### Soft Fails (Trigger retry with corrections)

| Code | Name | Test | Retry Strategy |
|------|------|------|----------------|
| SF01 | Style drift | Line weight inconsistent, construction lines absent, cross-hatching missing | Re-anchor with A-2 + style refinement prompt |
| SF02 | Identity drift | Facial features don't match Sean (hair, jaw, eyes differ from A-2) | Re-anchor + explicit identity corrections |
| SF03 | Proportion drift | Head-to-body ratio, arm length, height inconsistent with A-2 | Add proportion constraints referencing A-2 |
| SF04 | Paper texture | Wrong grain, missing hole-punch marks or production label | Add paper texture refinement block |
| SF05 | Expression mismatch | Expression doesn't match storyboard beat description | Add explicit expression direction |

### Retry Ladder

1. **Attempt 1:** Original prompt from `docs/COMPLETED/act1-keyframe-prompts.md`
2. **Attempt 2:** Re-anchor from A-2 + specific correction notes based on failure
3. **Attempt 3:** Tighten prompt with refinement tips from `pencil-animation-prompt-templates.md`
4. **Attempt 4:** STOP — flag for human review with diagnostic report

## Key Commands

### Generation

Generate a single keyframe (example: F06):
```bash
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "[PROMPT]" \
  --output runs/{run_id}/candidates/F06/attempt_01.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env
```

With frame chaining (example: F10 references A-2 + approved F06):
```bash
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "[PROMPT]" \
  --output runs/{run_id}/candidates/F10/attempt_01.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png runs/{run_id}/approved/PT_A1_F06_key.png \
  --env-file .env
```

### Orchestrated generation run
```bash
python3 pipeline/generate.py --manifest manifest.yaml
```

### Audit
```bash
python3 pipeline/audit.py --run-dir runs/{run_id} --frame F06 --attempt 1
```

### Assembly
```bash
bash pipeline/assemble.sh runs/{run_id}
```

### DAG-orchestrated run (commit 4+, opt-in)

The hand-rolled DAG runner orchestrates pipeline phases as typed nodes with
content-addressed caching. The legacy linear path stays usable; opt in by
setting `USE_DAG_RUNNER=1` or invoking the runner directly:

```bash
USE_DAG_RUNNER=1 python pipeline/generate.py --manifest manifest.yaml
# or
python -m pipeline.dag run --manifest manifest.yaml --run-dir runs/{run_id}
```

Cache lives at `runs/{run_id}/.cache/{sha256}.json` per node invocation.
Cache keys include tier (`draft | pro`) and the `acceptance_criteria.json`
file hash, so a tier change or a criteria mutation invalidates downstream
nodes. The runner declines to mutate a locked criteria file without
`--force-criteria-mutation` plus an actor + reason; the override is
audited to `runs/{run_id}/criteria_audit.jsonl`.

### Surveying staged patches (commit 8+)

Em (and from commit 9, the T3 stack) emit `proposed_patches:` that stage into
`runs/{run_id}/manifest.lock.yaml` via the DAG runner's `post_run` hook.
Stage-first per v2 lock; never auto-apply. Survey them with:

```bash
python -m pipeline.cli patches list --run-dir runs/{run_id}
```

Output groups patches by persona (`em-vision-critic`, future `codie` / `annie`
/ `sage`) with target / path / operation / value / rationale / cites_criteria
/ node_id. Read-only — interactive accept/reject is commit 8b or commit 10.

### Character Bible authoring (commit 2+)

Cy's CLI surface mirrors Maya's plan CLI structurally. Five subcommands:

```bash
# Scaffold a new character bible folder (idempotent — re-running won't overwrite).
python -m pipeline.cli bible init --target characters/{character_id}/

# Render the Bible as a terminal tear sheet: header / ANSI palette swatch /
# proportions / IR.* rules grouped by category / motion plate inventory /
# risks / Cy's confidence hedges. Boxes live in the renderer; clean prose on disk.
python -m pipeline.cli bible show --character-dir characters/{character_id}/

# Flip locked=true on the character's acceptance_criteria.json. Idempotent.
python -m pipeline.cli bible approve --character-dir characters/{character_id}/

# Audited mutation of a locked Bible. Refuses without --force. Bumps semver,
# re-points the symlink, appends to runs/{run_id}/bible_audit.jsonl.
python -m pipeline.cli bible mutate --force --actor <name> --reason "<why>" \
    --target IR.<character_id>.<category>.<handle> --field <field> --value <value> \
    --character-dir characters/{character_id}/ --run-dir runs/{run_id} \
    --new-version 1.3.0

# Re-run Cy narrowed to rejected plates; cached passing plates are preserved.
python -m pipeline.cli bible iterate --character-dir characters/{character_id}/ \
    --target turnarounds,expressions --reject neutral,surprised \
    --reason "<why>" --run-dir runs/{run_id}
```

To actually author a Bible end-to-end (Tasks 1.10 + 1.11 in Sean's
authoring session, with live Opus + NB Pro + Gemini calls), use the
orchestrator:

```bash
python scripts/author_bible.py characters/sean-anchor/ \
    --studio-brief "Pencil Test reference character — see source-refs/notes.md" \
    --run-dir runs/2026-MM-DD-cy-sean-anchor-bake/

python scripts/author_bible.py characters/claude-mascot/ \
    --studio-brief "Pixel-art mascot — see source-refs/notes.md" \
    --run-dir runs/2026-MM-DD-cy-claude-mascot-bake/
```

Cy's three-phase loop fires (Opus authors → NB Pro generates → Gemini
verifies); stub fallback runs end-to-end without API credentials so the
contract layer exercises in CI. Real authoring requires `GEMINI_API_KEY`
in `.env` for NB Pro and `agy` on PATH for Gemini verification.

### Frame Sequence (12fps, Act 1 hero loop)
```bash
# MP4 (archival)
ffmpeg -framerate 12 -i frame_%04d.png -c:v libx264 -crf 18 -pix_fmt yuv420p pencil-test-act1.mp4

# WebM (web)
ffmpeg -i pencil-test-act1.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 pencil-test-act1.webm

# GIF (hero loop, two-pass palette, <5MB)
ffmpeg -i pencil-test-act1.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" pencil-test-act1.gif
```

## Generation Chains

Act 1 has two independent generation chains. Each frame in a chain depends on the previous frame being approved first.

- **Chain 1:** F06 → F10 → F13 → F18 (Beat 1-2: idle through mid-gesture)
- **Chain 2:** F31 → F36 (Beat 3: sprite lands through nod)

Chains 1 and 2 are independent and can run in parallel.

F01 and F40 use the A-2 anchor directly (no generation needed).

## Continuity Audit

Run after a full generation pass to catch frame-to-frame continuity errors:

```bash
python3 pipeline/continuity_audit.py --run-dir runs/{run_id}
```

Checks 8 continuity dimensions across all consecutive frame pairs:

| Check | Severity | What it catches |
|-------|----------|----------------|
| CC01 — Stylus hand | Blocker | Stylus must stay in character's RIGHT hand |
| CC02 — Stylus presence | Blocker | Stylus must be visible in every frame |
| CC03 — Clothing | Blocker | Same outfit in every frame |
| CC04 — Facing direction | Warning | General body orientation consistency |
| CC05 — Scale/position | Warning | Character height and ground plane |
| CC06 — Hair | Warning | Shape, volume, part direction |
| CC07 — Foot position | Warning | Ground plane and stance width |
| CC08 — Expression arc | Warning | Emotional progression follows storyboard |

Log findings: `python3 pipeline/continuity_audit.py --run-dir runs/{run_id} --log-finding CC01 F13 "description"`

## Seedance Generation

Generate a Seedance 2.0 video with start+end frame interpolation:
```python
import fal_client, os
os.environ["FAL_KEY"] = os.getenv("FAL_KEY")

result = fal_client.subscribe(
    "bytedance/seedance-2.0/image-to-video",
    arguments={
        "prompt": "[COMPRESSED ACTION PROMPT — 60-80 words]",
        "image_url": "[START FRAME URL]",
        "end_image_url": "[END FRAME URL]",
        "resolution": "720p",
        "duration": "5",
        "generate_audio": False,
    },
)
video_url = result["video"]["url"]
```

Extract frames at 12fps from Seedance output:
```bash
ffmpeg -i seedance_output.mp4 -vf fps=12 frame_%04d.png
```

**Seedance prompting rules:**
- 60–80 words, action-focused (WHAT happens, not body mechanics)
- Always include: "fixed camera, locked tripod" and "stylus in right hand"
- Never use: "cinematic", "4K", "glow", "epic", unqualified "fast"
- Don't re-describe the character — the start/end frames provide that
- **For all new shots, use the v4 template at [`prompts/seedance-template-v4.md`](prompts/seedance-template-v4.md).** Fill the `[BRACKETED]` placeholders; do not modify the structural scaffolding. Run at Fast tier as the production default.
- See [`docs/research/seedance-research-findings.md`](docs/research/seedance-research-findings.md) for full prompting guide

## Dependencies

```bash
pip install pyyaml Pillow google-genai fal-client
```

- **PyYAML** — manifest parsing in generate.py
- **Pillow** — aspect ratio check in audit.py (HF01)
- **google-genai** — Gemini API calls in generate_image.py
- **fal-client** — Seedance 2.0 API calls via fal.ai
- **FFmpeg** — frame assembly in assemble.sh (`brew install ffmpeg`)
- **bc** — GIF size calculation in assemble.sh (pre-installed on macOS)

Environment variables (in `.env`):
- `GEMINI_API_KEY` — Google Gemini API key
- `FAL_KEY` — Fal.ai API key for Seedance 2.0

## Prompt Files

Active Act 2 prompts live under `prompts/act2/`. Shipped Act 1 keyframe + transition + sprite prompts are archived at `prompts/COMPLETED/F{##}.txt` (e.g. `prompts/COMPLETED/F06.txt`) — extracted from `docs/COMPLETED/act1-keyframe-prompts.md`.

`pipeline/generate.py` auto-loads `prompts/F{##}.txt` first, then falls back to `prompts/COMPLETED/F{##}.txt`. Override with `--prompt "..."` or `--prompt-file path.txt`.

## Engine Truth

> If the loop plays smoothly and the character is recognizably itself in its intended medium, it ships.

This is the inherited north star from the pencil-test era — adapted from the original sprite pipeline's "if it plays cleanly in Phaser, it ships." The final piece in its target medium (browser GIF/WebM loop, public museum walkthrough, wherever the work lives) is the ultimate arbiter of quality. Everything else — phase counts, critic tiers, manifest schemas — is in service of that one test.
