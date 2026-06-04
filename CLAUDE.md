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

The five named checkpoints are placement-locked. T2 (Em) has shipped, and her **eval foundation was reset and rebuilt 2026-06-03** ([`docs/2026-06-03-eval-foundation-reset-plan.md`](docs/2026-06-03-eval-foundation-reset-plan.md)): the old fixture set was condemned (19/23 SHA-identical Bible copies, compound labels, drifted ~1:4–1:5.3 ground truth) and its baseline figures (0.62 / 1.00 / 0.15) are **void**. The new Sean-ratified corpus is live at [`evals/vision_critic/`](evals/vision_critic/) — 50 cases, six single-axis classes, paired clean/defect, fixture independence enforced by [`tests/test_fixture_contamination.py`](tests/test_fixture_contamination.py). The **G5 re-baseline RAN 2026-06-04 and is Sean-ratified** ([field report](docs/anima-test-runs/2026-06-04-em-rebaseline-g5-field-report.md)): reference-blind, N=5 majority vote, gemini-3.5-flash pinned — **performs precision 0.97 / recall 1.00 / false_pass 0.00** (caught all 28 single-axis defects, FN=0; 1 clean FP), retiring the void 0.62/1.00/0.15. This number gates all further critic work. **G6 roadmap locked 2026-06-04:** instrumented mini-run → references re-test → citation grounding (geometry IR criteria + split verdict/citation scoring, which triggers the next re-baseline), with the SF03 build in parallel; DINOv2 is **superseded-pending** (final call after the re-test + SF03 report).

**Layer-ownership map (locked 2026-06-03):** geometry classes — **proportion, view-correctness, anatomy-count** — are owned by the **Bible-lock** (deterministic, at author-time); style classes — **palette, construction-lines, shading-register** — are owned by **Em / T2** (MLLM, per production frame). Em is *measured* on all six in the eval; ownership says who acts in production. Reference-grounding stays **flag-gated off** (`critics.t2.attach_references: false` — the 2026-06-02 regression was the contaminated fixtures' confabulation trap by construction). The T3 council is still pending. Phase 7 Audit no longer *hosts* critique — it *consolidates and routes* critic findings to the retry ladder.

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

The migration from `images/2D-Character-Sketch-Sean-v1.png` → `characters/sean-anchor/anchor.png` shipped 2026-05-28. The legacy path is now a back-compat symlink to the new location, keeping unported pencil-test scripts working unchanged; it retires once Animatic ingestion lands and Act 2 is structurally complete.

## Source of Truth Documents

| Document | Path | Role |
|----------|------|------|
| **Pipeline Architecture (v1)** | [`docs/pipeline-architecture-v1.md`](docs/pipeline-architecture-v1.md) | **Canonical architecture lock — read first every session.** 10-phase spec, critic stack, draft→pro, Character Bible primitive, museum layer, reserved open questions |
| **Production Checklist** | [`docs/production-checklist.md`](docs/production-checklist.md) | Current status of the in-flight pencil-test work — phases, frames, assets |
| **Fleet Ops Protocol** | [`docs/fleet-ops-protocol.md`](docs/fleet-ops-protocol.md) | **Standing operating discipline for any costed/multi-step run — read before launching one.** Subscription billing (never `ANTHROPIC_API_KEY`), one isolated worktree per plan, singleton pre-flight + own-PID resolution, single owner, clean teardown (don't `start_new_session` a costed worker). Adopted 2026-06-02 after three operational incidents; remediation plan + verified diagnosis at [`docs/anima-test-runs/2026-06-02-operational-incidents-remediation-plan.md`](docs/anima-test-runs/2026-06-02-operational-incidents-remediation-plan.md) |
| Pipeline v2 Brainstorm | [`docs/2026-05-24-pipeline-v2-brainstorm.md`](docs/2026-05-24-pipeline-v2-brainstorm.md) | Historical artifact — the 15-idea PM/Designer/Engineer brainstorm that produced the v2 lock. Read for *why*, not *what* |
| Pipeline v2 Change Map | [`docs/2026-05-24-pipeline-v2-change-map.md`](docs/2026-05-24-pipeline-v2-change-map.md) | Historical artifact — 9-commit sequence, file-by-file delta, DAG library rationale, evals workstream scope |
| **Maya Planner Brainstorm** | [`docs/2026-05-26-maya-planner-brainstorm.md`](docs/2026-05-26-maya-planner-brainstorm.md) | Phase 0 design decisions — Top 5 locked (two-tier brief, graph criteria, cost-estimator AgentSpec, audited mutation contract, adversarial Sonnet pass), deferred items with promotion triggers, file map |
| **Anti-Gravity CLI Findings** | [`docs/research/2026-05-26-anti-gravity-cli-findings.md`](docs/research/2026-05-26-anti-gravity-cli-findings.md) | The Antigravity CLI migration — binary `gemini` → `agy`, new flag shape, `@path` image attachment, 2026-06-18 sunset |
| **Prompt Style-Neutrality Doctrine** | [`docs/prompt-style-neutrality-doctrine.md`](docs/prompt-style-neutrality-doctrine.md) | One-page doctrine on keeping anima's prompts style-agnostic across the six closed-vocabulary style registers. Enforced at CI time by [`tests/test_prompt_style_neutrality.py`](tests/test_prompt_style_neutrality.py). Read before adding a new register or editing a standing-context preamble |
| **Museum Exhibit Schema** | [`docs/museum-exhibit-schema.md`](docs/museum-exhibit-schema.md) | **The load-bearing data model for the Museum capture layer.** Exhibit/Decision/Verdict fields, the `museum/{project_slug}/{run_slug}/` tree, `derive_project_slug`, and the structural honesty contract (thin exhibits are truthful, never invented). Read before touching `pipeline/museum/` or `museum/` |
| **AI Evals Best Practice + Fleet Eval Strategy** | [`docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md`](docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md) | **The eval handbook for the fleet — read before building or scoring ANY agent's eval suite.** Verified 2026 best practice (error-analysis-first, binary cases, ships-red, class balance), the LLM-as-judge calibration procedure + corrected judge-bias ledger (overrides brainstorm §2.5), the vision/motion-judge findings (contact sheets see identity/style across a clip but NOT motion-proper), borrow-vs-build tooling, and the **per-agent-type eval-strategy matrix** (Maya / Cy / Em / Mo / Flo / Sam / Bea / T3 / orchestrator). Methodological basis for the critic-spine kickoff and every agent baseline. |
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
| A-2 Anchor | [`characters/sean-anchor/anchor.png`](characters/sean-anchor/anchor.png) | Identity reference for the Sean character. Migrated 2026-05-28; legacy path [`images/2D-Character-Sketch-Sean-v1.png`](images/2D-Character-Sketch-Sean-v1.png) is a back-compat symlink until Animatic lands |
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
| `planner` — Maya | 0 Brief & Plan | Opus 4.8 primary → Sonnet 4.6 adversarial validation → human gate. Emits two-tier brief (Studio + Production) + v1.1 graph-shaped `acceptance_criteria.json` + clean-markdown `plan.md` + `RunCostEstimate` from `CostEstimatorNode`. Three-call ceiling. `project_type: bible_authoring` scopes plan.md to Phase 0 + Phase 2 only. CLI: `python -m pipeline.cli plan init/show/approve/mutate`. |
| `character_designer` — Cy | 2 Character Bible | Three passes, three-attempt ceiling per plate: Opus 4.8 authors → NB2 (`gemini-3.1-flash-image-preview`) generates/edits → **gemini-3.5-flash verifies via the Gemini API** (`run_gemini_api_with_image`). **Model-provenance correction (2026-06-02, A2):** Pass-3 previously called `agy` with no `-m`, so the Antigravity backend silently served Gemini 3.5 Flash while this row claimed "Gemini 3.1 Pro" — both locked Bibles (sean-anchor, claude-mascot) were Flash-verified, not Pro. Pass-3 now routes through the Gemini API transport (`pipeline/agents/gemini_api_runner.py`), which pins gemini-3.5-flash by ID and reads the served model back from `resp.model_version`; a costed re-verification on a pinned model is ticketed (see CHANGELOG 2026-06-02). **Prompt construction (source of truth):** `_build_plate_prompt` in `pipeline/agents/character_designer.py` is the single home for plate prompts — the register-parameterized five-slot emitter (spec: [`docs/research/2026-05-30-nb2-editing-character-consistency-template.md`](docs/research/2026-05-30-nb2-editing-character-consistency-template.md)). It reads `_REGISTER_CLAUSE_LIBRARY` (six closed registers) to fill `{identity_lock}` / `{preserve_and_negative}` / `{style_register}`; Cy authors only the terse `{variation}`, and a reject reason threads into `{preserve_and_negative}` to steer the re-roll. `_build_prop_prompt` is the isolated-object case. **Model routing:** `_resolve_plate_model` / `_REGISTER_MODELS` route editing to NB2 for every register (better identity hold, ~½ cost, ~4× faster, dodges NB Pro's multi-reference downsampling regression); NB Pro is reserved for painterly *finals* (no consumer yet — re-verify the regression first). A `characters.{id}.generation_model` manifest override wins. Runner: `invoke_image_edit` (alias `invoke_nb_pro`). **Plate contract:** the runner owns references — `anchor.png` injected first on every `generate` plate, source-refs kept, no plate-to-plate chaining; prompts are short plate-intent, never verbal re-descriptions or pipeline-meta. **Prop exception:** plates under `props/` are isolated objects — no anchor, no figure/text, Pass-2.5 record-only. **Pass-2.5 similarity gate** (`pipeline/agents/similarity_gate.py`, DINOv2→CLIP→PIL ladder; persists `runs/{run_id}/plate_verdicts.jsonl`) is **record-only, not a hard reject** — a single front anchor can't separate legitimate view/expression variation from drift; a real gate needs per-view refs (future work). **Plates-only bake:** re-running against a *locked* Bible bakes plates only — an approved Bible is never re-authored. **`#region:NAME` ingest crops** read a `<sheet>.regions.json` sidecar; an unmappable region falls back to a full copy flagged `region_not_cropped`. Emits `character.yaml` + per-character `acceptance_criteria.json` (v1.2 graph, `IR.{character_id}.*`) + `risk-bible.md` + `cy-confidence-notes.md` + `plate_generation_plan.json`. CLI: `python -m pipeline.cli bible init/show/approve/mutate/add/iterate` — **mutate** edits / **iterate** re-rolls / **add** extends. (Dated authoring + bug-fix log in CHANGELOG.md.) |
| `vision_critic` — Em | 5, 6, 8 (T2 checkpoints) | **gemini-3.5-flash via the Gemini API** default (`critics.t2.transport: gemini_api`, config-selectable `agy \| gemini_api`; transport in [`pipeline/agents/gemini_api_runner.py`](pipeline/agents/gemini_api_runner.py)), Opus 4.7 via Claude Agent SDK escalation. **Model-label correction (2026-06-02 forensics):** agy passed no `-m` flag, so its Em calls ran the Antigravity **backend default — Gemini 3.5 Flash, not the `gemini-3.1-pro` the old label claimed** (272/272 Em-sized calls). The transport pivot (agy→API) unblocked the re-baseline that agy's personal-tier quota kept 429-walling; it pins gemini-3.5-flash to hold the model constant. Patches stage in `manifest.lock.yaml`. **Scored eval suite + motion-sight path shipped** ([`evals/vision_critic/`](evals/vision_critic/): segmented confusion matrix — precision/recall/**false-pass** on the defect class; `phase_6_motion` contact-sheet honesty clause via [`pipeline/contact_sheet.py`](pipeline/contact_sheet.py) lets a still-image judge see identity/style across a clip but **not** motion-proper). **Reference-grounding: shipped in code (PR #13) but the live re-baseline MEASURED it as a REGRESSION (2026-06-02) — now FLAG-GATED OFF (`critics.t2.attach_references: false`, A1).** Reference-blind is the shipped default (the safe recall-1.00 / false_pass-0.00 profile). When the flag is set true, Em attaches a capped Bible reference bundle (anchor + deduped front/3-quarter/profile turnarounds) via [`reference_selection.py`](pipeline/agents/reference_selection.py)'s `select_references` (subject = image 1, both paths, incl. phase-6) + surfaces `IR.*`/`AC.*` (`_criteria_block`) — but that path performs **false_pass 0.00→0.15, recall 1.00→0.85** (precision 0.62→0.73, disqualified), which is why it defaults off. Diagnosis: Opus verdict **variance** + reference **confabulation** (recites the reference register onto an off-register subject; a prompt-ablation showed the "matches references = correct" wording is a forgiveness lever but not a fix). **→ DINOv2: superseded-pending (G6 call, 2026-06-04)** — the B1b NO-GO spike plus the contamination explanation of the regression (the old fixtures were a confabulation trap by construction) demote it from NEXT; final call after the references re-test + SF03 report. The references **re-test is ungated** (runs on the clean corpus, before the citation-grounding change lands, for G5 comparability); the **flag flip** stays gated on clearing the false-pass gate. Bake-off not re-run (same gate). Field report + matrix: [2026-06-02 postscript](docs/anima-test-runs/2026-06-02-em-reference-images-field-report.md). Still deferred: view-aware selection (A), pairwise reframe. **Eval-foundation reset (2026-06-03): the old 29-case set + its 0.62/1.00/0.15 baseline are VOID** (19/23 fixtures were SHA-identical Bible copies — the by-construction cause of the reference-grounding regression). Rebuilt: 50 Sean-ratified cases (16 clean + 28 single-axis across the six classes + 6 motion_proper ships-red carried forward), independent Flow-authored fixtures (uniform JPEG 1376×768), `pair`/`corpus_id` fields, declared-view trick for view-correctness, contamination guard at [`tests/test_fixture_contamination.py`](tests/test_fixture_contamination.py). Two slots pending Sean re-rolls (P-B1, PA-D4 at `images/sean-character-dataset/_pending-reroll/`). **G5 re-baseline RAN + Sean-ratified 2026-06-04** ([field report](docs/anima-test-runs/2026-06-04-em-rebaseline-g5-field-report.md); matrix `evals/vision_critic/last-run.md` + `traces/baseline-2026-06-04-scored.md`): N=5 majority vote, reference-blind, gemini-3.5-flash pinned + opus-4.7 escalation, 247/250 case-runs scored. **THE new baseline — performs (n=44): precision 0.97 / recall 1.00 / false_pass 0.00** (caught all 28 single-axis defects, FN=0; 1 clean FP `clean-c06`) — **replaces the void 0.62/1.00/0.15**. Caveats: **cites-correct=0.03** (verdicts right, citations almost never match the expected criterion — partly geometry classes lacking citeable IR rules, partly possibly real on style; top G6 input); **geometry classes trip the empty-cites invariant** (proportion/view/anatomy, 3/250 case-runs, all recovered by majority — Em detects but can't ground, so a production block would be rejected); **motion 5/6 flagged via spatial traces** in the contact sheet, not motion perception (`motion-t2-arc` the lone slip). **G6 roadmap locked 2026-06-04** (Sean's calls, sequenced so G5-comparable diagnostics run before Em's input surface changes): (1) instrumented mini-run — persist per-case cites + reasoning, settle style-cite-vs-scoring-artifact + read `clean-c06` ([handoff](docs/2026-06-04-em-instrumented-mini-run-handoff.md)); (2) references re-test on the clean corpus; (3) citation grounding — real geometry IR criteria + split verdict/citation eval axes (→ the next re-baseline); SF03 build in parallel ([handoff](docs/2026-06-04-sf03-proportion-gate-build-handoff.md)); prompt-diff eval design opened ([draft](docs/2026-06-04-prompt-diff-eval-design.md)). Identity modes (hair/jaw/eye) consciously re-deferred; mascot corpus deferred on its turnaround sheet. |
| `museum_writer` — Mo | Museum (orthogonal) | Sonnet 4.6 docent ([`pipeline/agents/museum_writer.py`](pipeline/agents/museum_writer.py)). Narrates an already-structured exhibit into studio-manual prose; **never invents a fact the exhibit doesn't carry** (a thin exhibit reads as honestly sparse). Real path: `invoke_museum_prose` (sdk_runners); a faithful **deterministic local fallback** runs credential-free (CI-green) and is what the committed museum carries — real Sonnet prose is a one-command upgrade (`python scripts/build_museum.py --narrate`; `--no-sonnet` forces the fallback). The exhibit **schema is load-bearing; Mo is the prose layer over it.** |
| _(CLI critic)_ | 4→5, pre-Museum (T3 checkpoints) | Pending agent-fleet session — Codex + Anti-Gravity parallel. The Museum's **pre-publish T3 gate** is a declared seam — a human takes the look for now |

## Directory Structure

The working directory is `anima/` — renamed from `sw-portfolio-animation-pipeline/` on 2026-05-29 via a single `mv` that preserved full git history. The top-level `characters/`, `museum/`, and `evals/` conventions have since landed.

```
anima/                                   # renamed from sw-portfolio-animation-pipeline/ on 2026-05-29
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
│   ├── 2D-Character-Sketch-Sean-v1.png  # Back-compat symlink → characters/sean-anchor/anchor.png (retires when Animatic lands)
│   └── sean-character-dataset/          # Corpus staging — only _pending-reroll/ remains (P-B1, PA-D4 awaiting Sean's
│                                        #   Flow re-rolls); the 44 ratified images MOVED to evals/vision_critic/fixtures/frames/
├── pipeline/                            # Pipeline scripts
│   ├── generate.py                      # Generation orchestrator with frame chaining (USE_DAG_RUNNER=1 routes to dag.py)
│   ├── audit.py                         # T1 rule gate runner (USE_DAG_RUNNER=1 routes to dag.py)
│   ├── continuity_audit.py              # CC01-CC08 frame-to-frame continuity
│   ├── assemble.sh                      # FFmpeg assembly
│   ├── seedance_*.py                    # Seedance 2.0 generation, extract, audit, cleanup
│   ├── agents/                          # AgentSpec Protocol + critic agents
│   │   ├── __init__.py                  # AgentSpec, AgentResult, Patch, register_node
│   │   ├── vision_critic.py             # Em — T2 vision critic
│   │   ├── cli_runners.py               # Anti-Gravity CLI wrapper + stub fallback
│   │   ├── sdk_runners.py               # Claude Agent SDK / anthropic SDK wrapper + stub
│   │   ├── patch_stager.py              # post_run hook → runs/{run_id}/manifest.lock.yaml
│   │   └── prompts/                     # Persona standing-context preambles
│   ├── cli/                             # `python -m pipeline.cli` subcommands
│   │   ├── patches.py                   # `patches list` — survey staged proposed_patches
│   │   ├── plan.py                      # Maya plan init/show/approve/mutate
│   │   └── bible.py                     # Cy bible init/show/approve/mutate/iterate
│   ├── criteria.py                      # acceptance_criteria.json v1.2 schema (AC.* + IR.* graph) + lock enforcement
│   ├── dag.py                           # Hand-rolled DAG runner
│   ├── agents/character_designer.py    # Cy's three-phase AgentSpec
│   ├── agents/nb_pro_runner.py         # NB Pro plate-generation wrapper, content-addressed cache
│   └── nodes/                           # AgentSpec wrappers around legacy scripts
├── characters/                          # Character Bible folders (Bible primitive); holds sean-anchor + claude-mascot
│   ├── sean-anchor/                     # Sean's Bible — pencil-test-colored register; first reference implementation
│   │   ├── anchor.png                   # The migrated A-2 reference (legacy path is a symlink → here)
│   │   ├── character.yaml               # Authored + approved Bible (v1.2)
│   │   ├── turnarounds/                 # body-* RE-LOCKED 2026-06-03 at 1:7 — five zero-drift region crops from the
│   │   │                                #   gold-standard sheet (incl. net-new body-front); drifted ~1:4-1:5.3 originals
│   │   │                                #   archived at characters/_archive/sean-anchor-drifted-body-turnarounds-2026-06-03/
│   │   ├── expressions/ motion_plates/ costumes/default/ props/  # Cy populates per Pass-1 plate plan
│   │   └── source-refs/                 # POPULATED: notes.md, turnaround-{1,2}.png, head-turn/{1..9}.png,
│   │                                    #   walk-cycle/{source,derived-v1,derived-v2}.png, 3d-mannequin/,
│   │                                    #   sean-character-full-body-turnaround.png (+ .regions.json sidecar) +
│   │                                    #   sean-head-turnaround.png — the 1:7 GOLD STANDARD (Sean-ratified 2026-06-03)
│   ├── claude-mascot/                   # Claude Mascot Bible — pencil-test-colored register; Act 2 shoulder companion
│   │   ├── anchor.png                   # The C-B ¾ hero portrait — the terracotta box-creature identity reference
│   │   ├── character.yaml               # 25 IR.claude-mascot.* rules (incl. 7 motion); criteria locked (v1.2, content_version 1.2.1)
│   │   ├── turnarounds/                 # 5 plates INGESTED as crops from the real C-1 turnaround sheet (zero-drift)
│   │   ├── expressions/ motion_plates/ costumes/default/ props/  # 6 expressions + 23 COLORED motion plates (idle-01..04/look/perch/alert/hop/sleep, Sean's hand-drawn+colored keys; line-rough animatic preserved at source-refs/motion-line-roughs/)
│   │   └── source-refs/                 # POPULATED: notes.md, turnaround-c1.png (5-view sheet) + .regions.json
│   │                                    #   crop sidecar, sean-with-claude-mascot.png (A-7 pairing)
│   ├── _archive/                        # Retired Bibles kept as evidence (not active). claude-mascot-pixel-art-8bit/
│   │                                    #   = the superseded pixel mascot (reference-gap failure; see its README)
│   └── _per-character_                  # Each Bible folder is self-contained; manifest's characters: dict
│                                        #   registers folder + style_register. criteria_sources: lists the
│                                        #   per-character acceptance_criteria.json paths for runtime merge.
├── museum/                              # Committed exhibit tree (schema SoT: docs/museum-exhibit-schema.md)
│   ├── {project_slug}/                  #   character-bible/ (84) + pencil-test/ (13). project.json + project.md
│   │   └── {run_slug}/exhibits/{id}/    #   exhibit.json (structured) + exhibit.md (Mo's prose) + assets/ (thumbnails)
│   └── _site/                           #   GITIGNORED static render (regenerate: build_museum.py --render). Full-res originals stay in runs/
├── evals/                               # Agent eval suites + dated bake-offs
│   ├── planner/ character_designer/     # cases.yaml + fixtures + pytest runner.py per agent
│   ├── similarity-gate/                 # fixtures for the in-suite DINOv2 regression
│   ├── vision_critic/                   # Em — scored suite: scoring.py + cases.yaml (50, ratified 2026-06-03) + conftest +
│   │                                    #   runner.py (CI-green) + score.py (live) + bakeoff_lib.py + traces/ +
│   │                                    #   fixtures/frames/ (44 Sean-authored corpus images; guarded by tests/test_fixture_contamination.py)
│   └── bakeoffs/                        # dated model shoot-outs (2026-05-31-t2-vision-critic-gemini-vs-sonnet-vs-opus)
└── runs/                                # Per-run output (gitignored)
    └── {run_id}/
        ├── manifest.lock.yaml           # Frozen config snapshot
        ├── candidates/                  # All generated candidates (preserved)
        ├── approved/                    # Approved keyframes
        ├── rejected/                    # Rejected frames with failure codes
        ├── audit/                       # Audit logs
        ├── animatic/                    # PLANNED — shape-block timing artifact
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

- `project:` — name, version, description (only `name` updated to `"anima"`; description retained)
- `anchor:` — single-character reference (deprecated by `characters:`; still authoritative for Act 2 in flight)
- `style:` — pencil-test aesthetic constraints
- `generation:` — Gemini NB2 model config
- `act1:` — Act 1 keyframe definitions
- `audit:` — Hard fails (HF01-HF05) + soft fails (SF01-SF05) + retry ladder
- `export:` — GIF / WebM / MP4 specs

**New (additive v2 blocks — schema declared first, wiring landed since):**

- `phases:` — 10-phase architecture node enablement. See [`docs/pipeline-architecture-v1.md`](docs/pipeline-architecture-v1.md)
- `tiering:` — draft → pro escalation defaults per phase
- `critics:` — T1/T2/T3 checkpoint placement
- `characters:` — Character Bible registry
- `museum:` — capture config + `project_slugs` derivation rules + noise-filter + standalone render target + publishing target (schema source of truth: [`docs/museum-exhibit-schema.md`](docs/museum-exhibit-schema.md))
- `brief:` — Phase 0 brief file convention

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

### DAG-orchestrated run (opt-in)

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

### Surveying staged patches

Em (and, once built, the T3 stack) emit `proposed_patches:` that stage into
`runs/{run_id}/manifest.lock.yaml` via the DAG runner's `post_run` hook.
Stage-first per v2 lock; never auto-apply. Survey them with:

```bash
python -m pipeline.cli patches list --run-dir runs/{run_id}
```

Output groups patches by persona (`em-vision-critic`, future `codie` / `annie`
/ `sage`) with target / path / operation / value / rationale / cites_criteria
/ node_id. Read-only — interactive accept/reject is not built yet.

### Building the Museum

The Museum capture layer turns `runs/` evidence into a self-contained static site
inside `anima/`. The orchestrator ([`scripts/build_museum.py`](scripts/build_museum.py))
is strictly read-only against `runs/` and the locked Bibles — it copies thumbnails
OUT into `museum/`, never mutating run history. Schema source of truth:
[`docs/museum-exhibit-schema.md`](docs/museum-exhibit-schema.md).

```bash
# Full backfill across all of runs/ (noise-filtered, every skip logged), narrate
# with Mo's deterministic fallback, and render the standalone site. The default
# committed museum is built this way.
python scripts/build_museum.py --all --narrate --no-sonnet --render --site museum/_site/

# Upgrade narration to real Sonnet 4.6 docent prose (needs claude-agent-sdk or
# ANTHROPIC_API_KEY; ~minutes, subscription-absorbed). Drop --no-sonnet:
python scripts/build_museum.py --narrate --render

# Targeted: one run's structured artifacts, or one character's motion comparison batch.
python scripts/build_museum.py --only 2026-05-30-cy-claude-mascot-pencil-bake --render
python scripts/build_museum.py --motion claude-mascot --render

# Open it (no build step, no CDN — browses by opening a file):
open museum/_site/index.html
```

`museum/_site/` is gitignored (regenerable); the `museum/{project_slug}/` exhibit
tree (exhibit.json + Mo's exhibit.md + thumbnail assets) is committed. **Named
follow-ons (NOT built):** the Astro export into `sw-ai-pm-portfolio` (standalone-first
deferral) and the T3 pre-publish critic gate (a human takes the look for now).

### Character Bible authoring

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

# Audited mutation of a locked Bible. Refuses without --force. Appends to
# runs/{run_id}/bible_audit.jsonl. Edits the rule whose id == --target in
# place (sets --field = --value), re-validates the graph, and writes back at
# the same schema `version` (1.2). `--new-version` is OPTIONAL and now records
# a separate content_version field the loader ignores — it never touches the
# schema-version field, so it is safe to pass (the 2026-05-30 schema-conflation
# bug that broke the claude-mascot Bible is fixed). An unknown --target errors.
python -m pipeline.cli bible mutate --force --actor <name> --reason "<why>" \
    --target IR.<character_id>.<category>.<handle> --field <field> --value <value> \
    --character-dir characters/{character_id}/ --run-dir runs/{run_id}

# Audited additive path: append new plates + IR rules to a LOCKED Bible.
# mutate edits an existing rule; iterate re-rolls existing plates; add EXTENDS.
python -m pipeline.cli bible add --character-dir characters/{character_id}/ \
    --spec characters/{character_id}/additions.json \
    --force --actor <name> --reason "<why>" \
    --run-dir runs/{run_id} --content-version 1.1.0

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
    --studio-brief "Claude-mascot in pencil-test-colored register — see source-refs/notes.md and the C-1 turnaround" \
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

## Testing

Tests are pytest, run **per-directory** from the repo root (there is no `pytest.ini`/`pyproject.toml`; a bare `pytest` collects `site-packages` and is noisy). All tests are credential-free — agent runners fall back to stubs, so the suite is green in CI without API keys.

```bash
# Contract suite — the core 242 tests (agents, CLI, criteria, DAG, museum, scrapers, eval regressions, motion-sight)
python -m pytest tests/

# Seedance v2 select/cleanup — MUST run separately. A combined `tests/ pipeline/tests/`
# run errors on a duplicate `tests` package basename (both dirs ship an __init__.py).
python -m pytest pipeline/tests/

# One file
python -m pytest tests/test_criteria.py -q
```

`evals/{agent}/` carries each agent's eval cases (`cases.yaml`), fixtures, and a README; `planner/` and `character_designer/` also ship a pytest `runner.py` parameterized over the cases. Run those explicitly — they're named `runner.py`, so default discovery skips them: `python -m pytest evals/planner/runner.py` (intentionally-red cases are marked `xfail`, so a green run can still report `xfailed`). The `similarity-gate` regression instead runs *inside* the contract suite, reading `evals/similarity-gate/fixtures/` (`tests/test_similarity_gate.py::test_dinov2_regression_recovered_above_drifted`). `evals/vision_critic/` is now a **full scored suite** with two modes: CI-green mocked `python -m pytest evals/vision_critic/runner.py` (proves the scoring plumbing; the 6 motion-proper-red cases `xfail`), and the deliberate, costed **live** baseline `python -m evals.vision_critic.score` (invokes Em real → writes `last-run.md` + a dated trace; `--stub` forces the credential-free path, à la Mo's `--no-sonnet`). The dated three-way model bake-off runs via `python evals/bakeoffs/2026-05-31-t2-vision-critic-gemini-vs-sonnet-vs-opus/bakeoff.py` (live; `--variants gemini` to scope).

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
