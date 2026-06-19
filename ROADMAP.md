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

**Workstream: brainstorm + build the Animatic phase (TOP-1).** This is the single active workstream. Everything else waits.

It's the right thing to build now for two independent reasons. PHILOSOPHY names it the one non-negotiable belief — *"AI that generates motion without a human-authored timing constraint is the template trap, and the template trap is the only thing that kills this project."* And the most recent live run **re-derived the need for it on its own**: the placement, leg-count, and shoulder problems the 2026-06-18 validation run surfaced are exactly what a human-authored rough-frame/stick-figure placement seed would constrain before any compute burns.

**Brainstorm ratified 2026-06-18.** v1 is the **placement seed** — a human-authored rough that pins where characters stand, facing, scale, shoulder side, leg count before any frame is drawn — carrying placement (conditions GENERATE) *and* timing (drives holds/pacing at ASSEMBLE now, captured for Seedance later). Design: [`docs/active/2026-06-18-animatic-phase-design.md`](docs/active/2026-06-18-animatic-phase-design.md). Build handoff: [`docs/active/2026-06-18-animatic-phase-kickoff.md`](docs/active/2026-06-18-animatic-phase-kickoff.md).

**Definition of Done (ratified):**
1. ✅ A ratified Animatic design doc + Claude Code execution kickoff (this session).
2. ✅ **A green costed spike** proving a placement rough makes NB2 respect placement — judged by Sean's eye — *before* any stage code. (Kickflip spike, ~$1.0 Gemini; **Sean ruled GO** 2026-06-18; [field report](docs/anima-test-runs/2026-06-18-animatic-spike-field-report.md). Riders: silhouette = recommended form; the end-of-run "trail-off" diagnosed (production-sheet text / hole-punches / loose sketch) + fixed with a no-text/finished-frame negative baked into the role-tag clause.)
3. ✅ A new **opt-in `ANIMATIC` stage** wired into [`pipeline/run.py`](pipeline/run.py) between `STORYBOARD` and `GENERATE`, with its own author-and-ingest gate; existing runs byte-identical (back-compat tests green).
4. ✅ The placement reference wired into generation (role-tagged, appended last, run-state primary so the locked board is never mutated); the timing sidecar driving ASSEMBLE holds; both captured under `runs/<id>/animatic/`.
5. ✅ The `post_animatic` T3 gate **consciously deferred** — seam kept in [`manifest.yaml`](manifest.yaml), hook point placed, promotion trigger recorded (timing feeds an orchestrated Motion phase). Not wired in v1.
6. ⏳ A costed run exercising the new stage end-to-end that ships a loop whose placement holds. **The one open item** — the build is stub-green complete (+20 tests, 665 → 685; both md5 guards intact); this is the real proof and needs Sean drawing roughs for a real loop.

**Status:** the Animatic *stage* is **BUILT** (spike GO + $0 stub-green, TDD, 2026-06-18). Current focus **stays on Animatic** until DoD #6 (the costed end-to-end run) closes — per the anti-drift contract, Tier-2 does not open until then.

**Explicitly not now:** Tier-2 Em calibration and the Museum orchestrator wiring. Both are real, both are next, and both are held until this DoD is met (DoD #6).

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
| **TOP-1 Animatic** | ◑ (stage BUILT; costed run pending) | `STAGES = (...,"STORYBOARD","ANIMATIC","GENERATE",...)` in [`pipeline/orchestration/state.py`](pipeline/orchestration/state.py); new [`pipeline/orchestration/animatic_stage.py`](pipeline/orchestration/animatic_stage.py) + `--animatic`/`--approve-animatic` in [`pipeline/run.py`](pipeline/run.py); `animatic_ref` + role-tag clause in [`generate_stage.py`](pipeline/orchestration/generate_stage.py); `animatic:` block in `manifest.yaml`. Costed kickflip spike **GO** ([field report](docs/anima-test-runs/2026-06-18-animatic-spike-field-report.md)). +20 tests (665→685), both md5 guards intact. | **Still the current focus.** Built $0 stub-green (TDD) 2026-06-18 — opt-in placement gate (default off ⇒ byte-identical). `post_animatic` T3 deferred (seam + hook kept). **DoD #6 open:** a costed end-to-end run shipping a loop whose placement holds (Sean draws real roughs). |
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

## The road ahead

Three workstreams, in Sean's locked priority order. Each is a **to-brainstorm placeholder, not a design** — every one gets its own brainstorm session before any plan. Do not design them here.

**1. Animatic (TOP-1) — the keystone, design ratified, build pending.** *(This is the current focus.)* The brainstorm settled all five open questions (2026-06-18, [design doc](docs/active/2026-06-18-animatic-phase-design.md)): v1 is a **placement seed**, not a timing-for-motion seed — a human-authored shape-block rough carrying placement (a role-tagged reference appended last, fixing the L/R / scale / shoulder / leg-count drift) and timing (a holds sidecar driving ASSEMBLE pacing now, captured for Seedance later); format is PNG roughs + holds in one Dreams-compatible ingestion contract; the stage is an **opt-in** author-and-ingest gate between STORYBOARD and GENERATE (back-compat byte-identical); the `post_animatic` T3 gate is consciously deferred. The whole design rests on one bet — *a hand-drawn rough actually makes NB2 respect placement* — de-risked by a **costed spike as build step 1** that gates everything downstream. Build handoff: [kickoff](docs/active/2026-06-18-animatic-phase-kickoff.md).

**2. Tier 2 — Em calibration (the autonomy core).** Flows naturally out of the Animatic work: a human-authored placement seed reduces what Em must catch, which narrows the calibration target. The data is already harvested — the Em-vs-eye label table in [`docs/anima-test-runs/2026-06-18-tier1-validation-run-post-mortem.md`](docs/anima-test-runs/2026-06-18-tier1-validation-run-post-mortem.md). Open questions for the brainstorm: severity/threshold calibration separate from detection coverage; the left/right-axis unreliability shared by *both* generator and critic; the mascot-anatomy blind spots (leg-count); the `identity_critical` → Opus escalation gap (discrepancy B); and whether to wire propose→apply. **Hard guard: any Em change is eval-gated, and the verdict-baseline md5 moves only on a deliberate, ratified re-baseline.**

**3. Museum — make "the pipeline is the portfolio" true.** Wire museum capture into the orchestrator (today it's a separate post-run pass) and build the Astro publish into `sw-ai-pm-portfolio`. Open questions: when capture fires within a run, how the standalone render and the published site relate, and the `pre_museum` T3 gate's role in the run loop (it exists, but only on the standalone path today).

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
