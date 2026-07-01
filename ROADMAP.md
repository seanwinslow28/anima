# anima — Roadmap

*Read this right after [`PHILOSOPHY.md`](PHILOSOPHY.md), before the architecture lock. Philosophy says why anima exists; this says where it is and where it's going next.*

---

## What this is

`ROADMAP.md` is the trajectory source of truth — the document a drifting session opens to remember what it's supposed to be doing. It exists because anima has a documented failure mode, in Sean's words: *"We keep going off track and diving further down a rabbit hole of testing before completing anything, so we need to make sure we have a roadmap to go back to each time."*

The evidence backs him up. The single highest-priority idea in the original architecture brainstorm — the **Animatic phase (TOP-1)**, which PHILOSOPHY calls *non-negotiable* — was never built, while the Em vision-critic's eval suite went five rounds deep (G5 → G6 → G6.1 → G6.1b → Gate-3 → Gate-2). The Em work is excellent. It is also *unsequenced* — it ran ahead of the keystone it was meant to support. That is the pattern this document is built to break.

So this roadmap carries one contract, and it is the whole point of the document:

> **The project does not open a new workstream until the current one's Definition of Done is met.** When a DoD is met, update the scorecard and advance "Current focus" *before* starting the next thing.

That's the anti-drift rule. Everything below serves it.

**How this relates to the other source-of-truth docs.** Four documents, four jobs, no overlap:

- [`PHILOSOPHY.md`](PHILOSOPHY.md) — *why* anima exists and what it refuses to become. The fixed stars.
- **`ROADMAP.md`** (this) — *where the system is and what to do next*. The trajectory.
- [`CLAUDE.md`](CLAUDE.md) — *how the system works right now*. The fleet manual, updated as the current state shifts.
- [`docs/architecture/production-checklist.md`](docs/architecture/production-checklist.md) — *where one artifact stands* (the Pencil Test acts and frames). It tracks a **piece**; this roadmap tracks the **system**. They don't compete.

This document **supersedes the tracking function** of the three origin brainstorms ([pipeline-v2-brainstorm](docs/COMPLETED/pipeline-v2/2026-05-24-pipeline-v2-brainstorm.md), [pipeline-v2-change-map](docs/COMPLETED/pipeline-v2/2026-05-24-pipeline-v2-change-map.md), [agent-fleet-brainstorm-v2](docs/COMPLETED/agent-fleet/2026-05-26-agent-fleet-brainstorm-v2.md)). Those stay frozen as the dated record of *where we started* and *why we chose it*. This is the living record of *where we are*.

---

## Current focus — you are here

**Workstream: Tier-2 — Em calibration (the autonomy core).** This is the single active workstream as of 2026-06-22. Everything else waits.

**TOP-1 Animatic closed 2026-06-22** — DoD #6 was met by the costed Spark-animatic driven run (operator-driven: Claude Code ran every command; Sean made every taste call and never an auto-approval). A 7-frame loop shipped at **zero retries / ~$0.50 Gemini**, and Sean's eye confirmed placement held — mascot on the right shoulder, consistent scale, no leg-count drift — where the 2026-06-18 run drifted. [Field report](docs/anima-test-runs/2026-06-21-spark-animatic-run-post-mortem.md). Per the anti-drift contract, focus now advances to workstream 2.

Why Tier-2 next: the Animatic placement seed reduces what Em must catch, which narrows the calibration target — and the driven run handed it a concrete data point. Em[claude-mascot] went borderline three times (a consistent mascot finish-register drift) and Sean over-rode each; Em[sean] passed all seven and once contradicted the mascot read. The production trust bar — **Em ≈ Sean's eye** — is the autonomy blocker, and it is unmet. The data is already harvested (this run's Em-vs-eye table + the [2026-06-18 validation run](docs/anima-test-runs/2026-06-18-tier1-validation-run-post-mortem.md)). **Hard guard: any Em change is eval-gated, and the verdict-baseline md5 moves only on a deliberate, ratified re-baseline.**

**Brainstormed 2026-06-22 (this session) — trust bar + Slice 1 ratified.** The trust bar is **trustworthy assistant**: Em's flags get good enough that Sean spot-checks the flagged frames instead of reviewing every one, false-pass held at 0 (full hands-off + propose→apply auto-fix are later exits). Tier-2 is too big for one slice, so it decomposes — and the entry is gated by a stark fact: **the Em eval corpus is 52 cases, 100% `sean`, zero mascot**, yet every measured gap is on the mascot. So **Slice 1 = the mascot eval corpus + baseline** — pure measurement, changes nothing in Em, so it *cannot* regress the frozen md5. Full mirror of the sean six classes; **Sean generates the ~46 fixtures in Google Flow ($0 on subscription)** against [`prompts/eval-corpus/claude-mascot-fixture-corpus.md`](prompts/eval-corpus/claude-mascot-fixture-corpus.md); Claude Code ingests + runs the reference-blind N=5 baseline → the mascot verdict baseline. Design: [`docs/active/2026-06-22-tier2-mascot-corpus-design.md`](docs/active/2026-06-22-tier2-mascot-corpus-design.md); kickoff: [`docs/active/2026-06-22-tier2-mascot-corpus-kickoff.md`](docs/active/2026-06-22-tier2-mascot-corpus-kickoff.md). **Slice 1 SHIPPED + ratified-with-notes 2026-07-01.** The 46-fixture / 46-case mascot corpus is live in `cases.yaml` (Sean-ratified 2026-06-30) and the reference-blind N=5 baseline (sean's G5 protocol) reads **performs (n=46) precision 0.93 / recall 0.90 / false-pass 0.10, cites 0.17** ([trace](evals/vision_critic/traces/mascot-baseline-2026-06-30.md)) — measurably weaker than sean's 0.97/1.00/0.00, *which is the point*. The seam is specific: **all 3 false-passes are the construction-lines-absent class** (Em passes a cleaned-up final with no visible pencil under-drawing reference-blind) → **construction-lines detection is the priority Slice-2 target**; the 2 clean FPs are accepted red (Em over-caution, not tuned). Nothing in Em changed; the frozen md5 held. Slice 2 (the calibration — construction-lines / finish-register *severity* + leg-count *detection* + cross-namespace *coherence*) brainstorms next, now eval-gated against this baseline.

**The Animatic Definition of Done — all met (closed 2026-06-22):**
1. ✅ A ratified Animatic design doc + Claude Code execution kickoff (this session).
2. ✅ **A green costed spike** proving a placement rough makes NB2 respect placement — judged by Sean's eye — *before* any stage code. (Kickflip spike, ~$1.0 Gemini; **Sean ruled GO** 2026-06-18; [field report](docs/anima-test-runs/2026-06-18-animatic-spike-field-report.md). Riders: silhouette = recommended form; the end-of-run "trail-off" diagnosed (production-sheet text / hole-punches / loose sketch) + fixed with a no-text/finished-frame negative baked into the role-tag clause.)
3. ✅ A new **opt-in `ANIMATIC` stage** wired into [`pipeline/run.py`](pipeline/run.py) between `STORYBOARD` and `GENERATE`, with its own author-and-ingest gate; existing runs byte-identical (back-compat tests green).
4. ✅ The placement reference wired into generation (role-tagged, appended last, run-state primary so the locked board is never mutated); the timing sidecar driving ASSEMBLE holds; both captured under `runs/<id>/animatic/`.
5. ✅ The `post_animatic` T3 gate **consciously deferred** — seam kept in [`manifest.yaml`](manifest.yaml), hook point placed, promotion trigger recorded (timing feeds an orchestrated Motion phase). Not wired in v1.
6. ✅ **A costed run exercising the new stage end-to-end shipped a loop whose placement holds** (2026-06-22; run `2026-06-21-spark-animatic-driven`). Sean drew 7 placement roughs; the operator-driven run ingested them, generated all 7 frames at **zero retries**, and Sean's eye confirmed placement held against the 06-18 drift. The build was stub-green complete beforehand (+20 tests, 665 → 685; both md5 guards intact); this run is the live proof. [Field report](docs/anima-test-runs/2026-06-21-spark-animatic-run-post-mortem.md).

**Status:** the Animatic *stage* is **BUILT + PROVEN** — DoD #6 closed 2026-06-22 by the costed Spark-animatic driven run (placement held, loop shipped, Sean's eye). **All six DoD items met; this workstream is complete.** Per the anti-drift contract, the current focus now advances to **workstream 2 (Tier-2 Em calibration).**

**Outward turn scoped (2026-06-29).** The three vision-expansion directions — ① brainstorm front door, ② Flow-like interface, ③ generation economics — were scoped and sequenced as future workstreams (see *Product vision* and *The road ahead* below). ③ runs in parallel now (a decision, not a build); ① then ② wait for Tier-2's DoD. Tier-2 remains the only active build.

**Explicitly not now:** the Museum orchestrator wiring (workstream 3). Real and next, but held until Tier-2's DoD is met. The `post_animatic` T3 gate stays consciously deferred (its promotion trigger — timing feeding an orchestrated Motion phase — is unchanged).

---

## Where we started

The shape of anima was locked across three brainstorms in late May 2026. The full *why* lives in those docs; the baseline the scorecard grades against is this:

**The five TOP architectural ideas** ([pipeline-v2-brainstorm](docs/COMPLETED/pipeline-v2/2026-05-24-pipeline-v2-brainstorm.md) §3):

1. **TOP-1 — the Animatic phase.** A formal stage where the human blocks motion and timing in shapes before any AI generates a frame. Called *"the highest-differentiation move in the entire brainstorm"* and *non-negotiable* in PHILOSOPHY.
2. **TOP-2 — Brief → Plan → Approval (Phase 0).** A planner agent turns a brief into a structured plan plus a cost estimate; nothing burns compute until a human approves.
3. **TOP-3 — the Museum.** Every approval, reject, and retry writes structured artifacts to a parallel tree; a static site renders the walkthrough. *"Pipeline as portfolio only works if portfolio content is a free byproduct."*
4. **TOP-4 — the DAG refactor with content-hashed caching.** Typed nodes, cache hits return immediately, editing one prompt re-runs only its downstream.
5. **TOP-5 — the Character Bible as a project entity.** A character is a folder (anchor, turnarounds, expressions, costumes, props, `character.yaml`), not a single PNG.

**The two promoted principles:** *Critic-as-Principle* (the three-tier T1/T2/T3 stack at five named checkpoints, a structural principle not a deferred feature) and *Draft → Pro escalation* (every expensive node declares a draft tier and a pro tier; escalate on approval).

**The persona fleet** ([agent-fleet-brainstorm-v2](docs/COMPLETED/agent-fleet/2026-05-26-agent-fleet-brainstorm-v2.md) §3): Maya (planner), Cy (character designer), Sam (scriptwriter), Bea (storyboard artist), Flo (frame router), Em (vision critic), Mo (museum writer), the T3 council (Codie / Annie / Sage + a chairman), and the orchestrator. Seven named agents, one council, one orchestrator, one human.

**The empirical workstream:** every agent ships with an eval suite from day one (cases grounded in real production logs, intentionally red where the failure is the artifact); model choices are settled by dated bake-offs; six open questions (Q1–Q6) were reserved for empirical tests rather than guessed.

---

## How we got here

The honest arc — wins and rabbit holes both.

**The doc-only foundation (2026-04 → 05-26).** The production checklist, then the pipeline-v2 brainstorm and change-map, then the Maya-planner brainstorm. The architecture was locked on paper before any v2 code was written — deliberately, to lock philosophy before drift.

**Bible and Cy (2026-05-28 → 30).** The Character Bible primitive landed — `images/2D-Character-Sketch-Sean-v1.png` became `characters/sean-anchor/anchor.png` (legacy path kept as a symlink) — and Cy, the character designer, was built as a three-pass loop (Opus authors → NB2 generates → Gemini verifies).

**The ops incident and the eval reset (2026-06-02 → 03).** A real billing leak, MCP overhead, and agents outliving their session produced the [fleet-ops protocol](docs/architecture/fleet-ops-protocol.md) — the standing discipline for any costed run. In the same window, Em's reference-grounding "regression" was traced to **fixture contamination** (19 of 23 fixtures were SHA-identical Bible copies), which voided the old baseline and forced a clean rebuild of the eval corpus.

**The Em eval saga (2026-06-04 → 10) — the unsequenced-depth exhibit.** Six gated, ratified rounds on a 52-case corpus took Em's verdict profile to precision 0.97 / recall 1.00 / false-pass 0.00 and its citation grounding from 0.03 to 0.97, then measured fix-rate and calibrated a cheap between-run proxy (κ 0.885). This was the *right* work — it's the baseline that gates every future Em change — but it ran **ahead of the orchestrator and ahead of the Animatic keystone**. It is the clearest illustration of why this roadmap exists: real depth, wrong sequence. (Dates in the saga table below.)

**The fleet completes (2026-06-10 → 15).** Flo (frame router) and the T3 council were built and live-validated on 06-10; the Flo-B pilot picked NB2 for pencil in-betweens after fal Seedream/Qwen failed Sean's eye. Sam (scriptwriter) and Bea (storyboard artist) — the last two named agents — shipped 06-15, completing the roster.

**The orchestrator and first runs (2026-06-11 → 18).** The first integrated run (06-11) chained Maya → Flo → Em and logged sixteen seams. Phase-3 wiring (06-16) folded Sam and Bea into `python -m pipeline.run`. The **first live end-to-end costed run** (06-17) shipped a five-frame two-character loop — and surfaced the autonomy blocker: **Em's eye ≠ Sean's eye.** Tier-1 slices A and B (06-17 → 18) fixed the tractable curation friction (Bea's prompt discipline, label hygiene, eye-gate legibility, loop-return chaining), and the **Tier-1 validation run** (06-18) confirmed all of it held live — five frames, first-shot approval, zero retries — while harvesting the Em-vs-eye label table that Tier-2 will calibrate against.

---

## The build scorecard

The heart of the document. Every original idea, principle, persona, and checkpoint is a row, graded against the tree — not against the brainstorms' optimism. Status legend:

| | Status | Meaning |
|---|---|---|
| ✅ | **Built + verified** | Exists in code, tests green, exercised in a run |
| ◑ | **Partial** | Built but not orchestrator-wired, schema-only, or lightly exercised |
| 🔬 | **Built, not calibrated** | Works, but doesn't yet meet its quality/trust bar |
| ⏳ | **Deferred** | Intentionally parked; promotion trigger named |
| ❌ | **Not built** | — |

### The five TOP ideas

| Idea | Status | Evidence | What's left |
|---|---|---|---|
| **TOP-1 Animatic** | ✅ (stage BUILT + costed run PROVEN) | `STAGES = (...,"STORYBOARD","ANIMATIC","GENERATE",...)` in [`pipeline/orchestration/state.py`](pipeline/orchestration/state.py); new [`pipeline/orchestration/animatic_stage.py`](pipeline/orchestration/animatic_stage.py) + `--animatic`/`--approve-animatic` in [`pipeline/run.py`](pipeline/run.py); `animatic_ref` + role-tag clause in [`generate_stage.py`](pipeline/orchestration/generate_stage.py); `animatic:` block in `manifest.yaml`. Costed kickflip spike **GO** ([spike report](docs/anima-test-runs/2026-06-18-animatic-spike-field-report.md)); **costed driven run shipped a placement-holding 7-frame loop** 2026-06-22 ([field report](docs/anima-test-runs/2026-06-21-spark-animatic-run-post-mortem.md)). +20 tests (665→685), both md5 guards intact. | **Complete (DoD #6 met 2026-06-22).** Built $0 stub-green (TDD) 2026-06-18 — opt-in placement gate (default off ⇒ byte-identical); proven live by the operator-driven Spark run (zero retries, ~$0.50 Gemini, placement held). `post_animatic` T3 stays deferred (seam + hook kept). |
| **TOP-2 Brief→Plan→Approval** | ✅ | Maya wired via `plan_stage.run_plan_stage` ([`pipeline/orchestration/plan_stage.py`](pipeline/orchestration/plan_stage.py)); plan gate in `run.py`; [`pipeline/agents/cost_estimator.py`](pipeline/agents/cost_estimator.py) emits the spend preview. Exercised in the 06-17/06-18 costed runs. | — |
| **TOP-3 Museum** | ◑ | [`pipeline/museum/`](pipeline/museum) + [`scripts/build_museum.py`](scripts/build_museum.py) + committed exhibit tree all exist. But `pipeline/run.py` has **zero** museum references — capture is a separate post-run invocation, not wired into the run. Astro publish into `sw-ai-pm-portfolio` not built. | Wire capture into the orchestrator; build the Astro export. (Road-ahead workstream 3.) |
| **TOP-4 DAG + cache** | ✅ | [`pipeline/dag.py`](pipeline/dag.py): `NODE_REGISTRY`, topological sort, `.cache/{sha256}.json` per node. Note `manifest phases.enabled: []` is intentionally empty (keeps pencil-test runs byte-identical); the orchestrator uses inline stages plus `dag.Runner` where it needs the graph. | — |
| **TOP-5 Character Bible** | ✅ | `characters/sean-anchor/` and `characters/claude-mascot/` both carry `locked: true` in their `acceptance_criteria.json`. | Cy *authoring* is standalone (`scripts/author_bible.py`), not in the orchestrator; Bible *consumption* is wired. Authoring-as-a-run is parked (Q6). |

### The two principles

| Principle | Status | Evidence | What's left |
|---|---|---|---|
| **Critic-as-Principle (T1/T2/T3)** | ◑ | **T1** ✅ — deterministic HF/SF/CC rule gates ([`pipeline/audit.py`](pipeline/audit.py), [`pipeline/continuity_audit.py`](pipeline/continuity_audit.py)). **T2 (Em)** 🔬 — built, wired per-frame, eval-deep, but not eye-calibrated (see below). **T3 council** ◑ — built and live-validated, but only the `pre_museum` gate is wired. | Calibrate T2 (workstream 2); wire `post_animatic` T3 (workstream 1). |
| **Draft → Pro escalation** | ◑ | Flo's route table does `standard@pro → hero` ([`pipeline/agents/frame_router.py`](pipeline/agents/frame_router.py)); the Seedance Fast→Pro pattern is the proven prototype ([`prompts/seedance-template-v4.md`](prompts/seedance-template-v4.md)). | Lightly exercised — no Motion run has driven the escalation in anger. |

### The personas

| Persona | Role | Status | Note |
|---|---|---|---|
| **Maya** | Planner (Phase 0) | ✅ | Wired (`plan_stage`); Opus 4.8 → Sonnet adversarial → human gate. |
| **Cy** | Character designer (Phase 2) | ✅ / ◑ | Built and proven; standalone (`author_bible.py`), not orchestrator-wired. |
| **Sam** | Scriptwriter (Phase 3a) | ✅ | Wired (`script_stage`); Opus 4.8 + deterministic structural pass. |
| **Bea** | Storyboard artist (Phase 3b) | ✅ | Wired (`storyboard_stage`); Sonnet 4.6 + deterministic validation. |
| **Flo** | Frame router (Phase 5) | ✅ | Wired, inlined in `generate_stage`. |
| **Em** | Vision critic (T2) | 🔬 | Built + wired per-frame; **the autonomy blocker** — detection-deep but not calibrated to Sean's eye. |
| **Mo** | Museum writer | ◑ | Built; standalone (`build_museum.py --narrate`), not orchestrator-wired. |
| **T3 council** | Codie / Annie / Sage + Chairman | ◑ | Built + live-validated; only `pre_museum` gate wired. |
| **Orchestrator** | Run state machine | ✅ | [`pipeline/run.py`](pipeline/run.py) — resumable `PLAN→…→DONE` state machine. |
| **Cost estimator** | Maya's spend preview | ✅ | Wired into Phase 0. |

### The five named critic checkpoints

| Checkpoint | Tier | Status | Evidence |
|---|---|---|---|
| post-Animatic (4→5) | T3 | ⏳ (consciously deferred) | The ANIMATIC phase now exists (2026-06-18), but the T3 gate is deliberately unwired in v1 — seam declared in `manifest.yaml`, a no-op hook point placed in [`animatic_stage.py`](pipeline/orchestration/animatic_stage.py). Promote when the timing animatic feeds an orchestrated Motion phase (the Seedance burn it exists to protect). |
| per-frame Generate (within 5) | T1 + T2 | ✅ | Wired in `generate_stage` (Flo → T1 → Em per frame). |
| post-Motion (6→7) | T2 | ⏳ | Motion isn't orchestrated (Seedance scripts standalone). |
| post-Assemble (8→9) | T2 | ⏳ | Declared; not wired. |
| pre-Museum publish | T3 | ✅ | `scripts/build_museum.py --t3-gate` ([`pipeline/museum/t3_gate.py`](pipeline/museum/t3_gate.py)). |

### The eval workstream

| Suite | Status | Note |
|---|---|---|
| `planner` / `character_designer` / `scriptwriter` / `storyboard_artist` | ✅ | `cases.yaml` + `runner.py` each. |
| `vision_critic` (Em) | 🔬 | The deep one — scored suite, verdict baseline 0.97/1.00/0.00, citation 0.97, Gate-2 proxy κ 0.885. But the *production* trust bar (Em ≈ Sean's eye) is unmet. |

The Em eval saga, as the unsequenced-depth exhibit:

| Date | Round | Outcome |
|---|---|---|
| 2026-06-03 | Eval foundation reset | 52-case contamination-guarded corpus; old baseline voided. |
| 2026-06-04 | G5 re-baseline | precision 0.97 / recall 1.00 / false-pass 0.00 (ratified). |
| 2026-06-04 | G6 instrumented + references re-test | cites-correct de-confounded; reference regression confirmed fixture-borne. |
| 2026-06-07 | G6.1 | 9 geometry IR rules authored; stylus rule scoped. |
| 2026-06-08 | G6.1b | criteria-text decoupled; cites 0.03 → 0.97; **live baseline**. |
| 2026-06-08 | G6.9 Gate-3 | fix-rate measured (normalized lift 0.667). |
| 2026-06-10 | Gate-2 | between-run proxy calibrated (κ 0.885). |

### Bake-offs and open questions

| Item | Status | Note |
|---|---|---|
| Q1 — orchestrator Sonnet vs Opus (drift test) | ⏳ | Not run. |
| Q2 — Sage tier ablation | ⏳ | Ticketed. |
| Q3 — storyboard three-way | ⏳ | Deferred. |
| Q4 — CLI multimodal input | ✅ | Verified live in the T3 council smoke (06-10). |
| Q5 — `proposed_patches` UX | ◑ | Stage-first survey built (`patches list`); accept/reject UI not built. |
| Q6 — Bibles authored vs consumed | ✅ | Both paths exist (authoring standalone, consumption wired). |

### The Tier-1 fixes

✅ **Validated live 2026-06-18.** Slice A: Bea's establishing-vs-edit prompt discipline + reference-label hygiene. Slice B: eye-gate ergonomics (prints Em's reasoning + proposed fix on non-pass) + `chain_from` loop-return chaining. The validation run shipped five frames at first-shot approval, against three retries on the equivalent frame in the first run.

---

## Discrepancies — flagged, not reconciled

Where an origin doc claims something the code or the runs don't bear out. These are some of the most valuable rows in the document.

**A — Flo's in-between routing.** The agent-fleet brainstorm's route table lists fal Seedream 4.0, Qwen-Image-Edit-Plus, and FLUX as in-between options. The **Flo-B pilot (2026-06-10)** pivoted to **NB2 (winner) / NB Pro (backup)** after Seedream morphed the face through the tween and Qwen reframed/degraded — failures Sean's eye caught that the metric would have passed. The fal transports are retained in `fal_runner.py` for future *non-pencil* creation; a self-hosted FLUX + sketch-LoRA path is ticketed. *Impact: low — the live routes are correct; only the planning doc over-shot the hardware.*

**B — the `identity_critical` → Opus escalation gap.** The plan says identity-critical criteria force an Opus escalation on Em's reads. The 2026-06-18 run found that first-pass frame reads pass `impact_tags=[]`, so the identity-critical tags never reach Em and **every verdict this run ran on Gemini, not Opus.** *Impact: real — it shifts the Tier-2 calibration target. The harvested Em-vs-eye labels are Gemini-grounded; if first-pass identity reads should escalate, the labels need re-harvesting. This is an open decision for workstream 2.*

**C — reference re-injection is undocumented.** Every generated frame re-injects the Bible anchors plus the prior approved frame; a loop-return with `chain_from: 1` chains off frame 1 instead. The order-preserving dedup keeps the final reference list clean, but **an approved frame silently becomes a competing authority** against the anchor — the likely mechanism behind the mascot leg-count drift (frame 1 approved with two visible nubs, then seeded into later frames against the anchor's four). *Impact: medium — the behavior is intentional but invisible in the prompt/context, and it propagates silent drift. Worth documenting in `generate_stage` or the runbook.*

---

## Product vision — the outward turn

For months anima was built **inward** — the ten phases, the fleet, the critic stack, the Em eval saga. The 2026-06-29 vision-expansion brainstorm named the **outward turn**: anima as a creative *tool* Sean uses to make animated shorts with an agent crew, not only a pipeline that ships one piece. The three directions scoped that day are one product arc — *brainstorm a concept with the crew, the orchestrated pipeline builds it, a desktop shell with a timeline strings it together and exports, and cost-optimized transports run the whole thing underneath.*

- **① Brainstorm front door** — a relentless elicitation chain (Grill Me's shape, anima's crew) that turns a spark into a concept doc + Studio Brief (the Phase 0 input Maya consumes), with a cheap in-session art-viz loop to lock the look first. *Verdict: HIGH, near-term, parallel-safe — touches nothing in Em.* Design: [`docs/active/2026-06-29-brainstorm-front-door-design.md`](docs/active/2026-06-29-brainstorm-front-door-design.md).
- **② Flow-like interface** — a native desktop app (Electron/Tauri) that wraps the orchestrator as a face: a FastAPI daemon over the existing stage functions + a frontend rendering the gates as screens, phased v1 chat+gates → v2 stage pages → v3 simple timeline. *Verdict: MEDIUM, phased — the long-game centerpiece; its daemon foundation is a parallel-safe early slice.* Design: [`docs/active/2026-06-29-flow-like-interface-design.md`](docs/active/2026-06-29-flow-like-interface-design.md).
- **③ Generation economics** — the transport-per-stage cost decision: run the pipeline on fal + direct Gemini/OpenAI keys (already wired, cheapest), trial Higgsfield a month, measure, decide. *Verdict: a decision, not a build; ~$0; runs now.* Design: [`docs/active/2026-06-29-generation-economics-design.md`](docs/active/2026-06-29-generation-economics-design.md).

Naming these is how we make room for them without drifting into them. The order below is the anti-drift contract applied to ambition.

---

## The road ahead

In Sean's locked priority order (ratified 2026-06-29). Each future item is a **scoped placeholder, not a green-lit build** — every one gets its own build-brainstorm before any plan, and **none opens until the active workstream's DoD is met** (the anti-drift contract). The *why* and the resolved forks live in the three design notes linked from the *Product vision* section above.

**NOW — active build · Tier 2, Em calibration (the autonomy core).** The data is already harvested — the Em-vs-eye label table in [`docs/anima-test-runs/2026-06-18-tier1-validation-run-post-mortem.md`](docs/anima-test-runs/2026-06-18-tier1-validation-run-post-mortem.md). Open questions for the brainstorm: severity/threshold calibration separate from detection coverage; the left/right-axis unreliability shared by *both* generator and critic; the mascot-anatomy blind spots (leg-count); the `identity_critical` → Opus escalation gap (discrepancy B); and whether to wire propose→apply. Slice 1 (the mascot eval corpus + baseline) **SHIPPED + ratified 2026-07-01** — the mascot is now measurable (performs 0.93/0.90/0.10 reference-blind; construction-lines-absent is the priority target; [trace](evals/vision_critic/traces/mascot-baseline-2026-06-30.md)); Slice 2 (the calibration) brainstorms next, eval-gated against it. **Hard guard: any Em change is eval-gated, and the verdict-baseline md5 moves only on a deliberate, ratified re-baseline.**

**NOW — parallel, not a build · ③ Generation economics.** The pipeline already runs the cheap path (fal + direct Gemini/OpenAI keys); the open call — keep or drop the Higgsfield subscription — is settled by a one-month measurement against a ~100-Seedance-clip/month break-even. ~$0, zero drift risk, so it rides alongside Tier-2 without competing for the active-build slot. Decision note: [`docs/active/2026-06-29-generation-economics-design.md`](docs/active/2026-06-29-generation-economics-design.md).

**NEXT — ① Brainstorm front door.** The creative entry point and the start of the arc: an orchestrated grilling-loop chain that emits a concept doc + Studio Brief + locked style refs, with character seeds handing to Cy. HIGH achievability, independent of Em. Its $0 manual dry-run may precede in parallel if Sean opts in; the build itself waits for Tier-2's DoD. Design: [`docs/active/2026-06-29-brainstorm-front-door-design.md`](docs/active/2026-06-29-brainstorm-front-door-design.md).

**THEN — ② interface · the daemon foundation.** A thin FastAPI over the existing stage functions (`plan_stage` … `animatic_stage`, over `run_state.json`) — backend plumbing, parallel-safe, the spine both ① and the UI plug into. Can overlap behind ①. Design: [`docs/active/2026-06-29-flow-like-interface-design.md`](docs/active/2026-06-29-flow-like-interface-design.md).

**LATER (the long game) — Museum wiring + the ② interface (v1→v3).** Wire museum capture into the orchestrator (today it's a separate post-run pass) and build the Astro publish into `sw-ai-pm-portfolio` — open questions: when capture fires within a run, how the standalone render and the published site relate, and the `pre_museum` T3 gate's role in the run loop (it exists, but only on the standalone path today). Alongside it, the desktop interface itself: v1 chat + gates (kills the terminal) → v2 per-stage pages → v3 simple timeline (arrange/trim/preview/export; no full NLE, by design). The Museum is naturally a view inside that app.

*Animatic (TOP-1) closed 2026-06-22 — see Current focus and the scorecard; it shipped a placement-holding 7-frame loop. The `post_animatic` T3 gate stays consciously deferred (promotion trigger: timing feeding an orchestrated Motion phase).*

---

## Standing guards & conventions

- **Two md5 guards that must not move** without a deliberate, ratified change:
  - `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` → `2af75906502f1caf8857e18828ceb2e4` (Em's verdict baseline).
  - `pipeline/agents/prompts/sean-screenwriting-voice.md` → `945af824fa53b948a18ac6bf206d67ef` (Sam/Bea's shared voice instrument).
- **Fleet-ops protocol** ([`docs/architecture/fleet-ops-protocol.md`](docs/architecture/fleet-ops-protocol.md)) governs any costed/multi-step run: subscription billing (never `ANTHROPIC_API_KEY`), one isolated worktree per plan, singleton pre-flight, a single known owner, clean teardown.
- **Archive convention:** completed artifacts move to `COMPLETED/`, superseded ones to `OLD/`, via `git mv`. Roots stay focused on what's active.
- **ROADMAP's own maintenance rule** (the anti-drift contract, made operational): when a workstream's Definition of Done is met, **update the scorecard and advance "Current focus" before starting the next workstream.** Treat this file the way CLAUDE.md treats its maintenance conventions — keep it trustworthy, or the next session starts from a wrong premise.

---

## Explicitly parked

Tracked so it isn't lost, with the trigger that promotes it back to active:

- **Phase 6 Seedance Motion** — no motion piece has run through the orchestrator. *Promote when a piece needs motion between approved anchors.*
- **Flo multi-model in-between routing** — pivoted to NB2; fal transports retained, self-hosted FLUX + LoRA ticketed. *Promote when non-pencil creation needs a different transport.*
- **Deferred bake-offs** — Q1 orchestrator drift, Q2 Sage tier, Q3 storyboard three-way. *Promote when the relevant agent's model choice becomes load-bearing.*
- **propose → apply** — Em's patches stage but don't auto-apply (Q5). *Promote inside workstream 2, once Em is calibrated enough to trust.*
- **Autonomous mode** — hands-off runs with a budget and a T3 variance check. *Promote only after Em ≈ Sean's eye is proven (the workstream-2 exit).*
- **Bible-authoring-as-project-type** — Cy as a first-class authoring run (Q6). *Promote when a second character needs authoring through the orchestrator.*

---

*The map exists so we stop drifting. Read it at the start of every session; return to it before starting anything new.*
