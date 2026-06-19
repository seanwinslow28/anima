# Kickoff — build `ROADMAP.md`, anima's source-of-truth tracker

*Paste this whole document into a fresh Cowork session opened on the `anima` project. It is self-contained. Your job is to produce one document — `ROADMAP.md` at the repo root — and the small doc updates that wire it in. No code, no model spend, no building of features. This is a synthesis-and-archaeology session: read widely, verify against the tree, and produce the map this project keeps wishing it had.*

---

## Why you're here

anima is a 2D-animation pipeline made by a human (Sean) plus a fleet of named agents. The whole fleet is built, a first loop shipped, and a round of fixes (Tier 1) just validated against live models. But the project has a recurring failure mode, in Sean's own words:

> *"We keep going off track and diving further down a rabbit hole of testing before completing anything, so we need to make sure we have a roadmap to go back to each time."*

The evidence backs him up. The single highest-priority idea in the original architecture brainstorm — the **Animatic phase (TOP-1)**, which PHILOSOPHY calls *non-negotiable* — was never built, while the Em vision-critic's eval suite went five deep rounds (G5 → G6 → G6.1 → G6.1b → Gate-3 → Gate-2). That's not bad work; the Em work is excellent. It's *unsequenced* work. The cure is a **single source-of-truth roadmap**: a checklist of where we started, how we got here, what's actually done, and what's left — that every future session reads and returns to before starting anything.

**Your deliverable is that document: `ROADMAP.md`, a peer to [`PHILOSOPHY.md`](../../PHILOSOPHY.md).** PHILOSOPHY says *why* the project exists and what it refuses to become; CLAUDE.md is the *current* fleet manual; ROADMAP.md is the *trajectory* — origin, progress, and the ordered path forward. It is the document a drifting session opens to remember what it's supposed to be doing.

---

## First: read these, in this order (do the archaeology before writing a line)

You must understand where the project *started*, *how it got here*, and *what's actually true now* — and the third must come from the tree, not the docs. Read in these four passes.

**Pass 1 — Intent (the fixed stars):**
1. [`PHILOSOPHY.md`](../../PHILOSOPHY.md) — the load-bearing thesis. ROADMAP.md serves this. The six load-bearing beliefs are the lens you grade progress against.
2. `CLAUDE.md` (repo root, auto-loaded) — the fleet manual + the **Skills Map** (every built agent, with status notes baked into each row). This is the densest current-state ground truth; read the whole Skills Map and the Key Commands → "the run orchestrator" section.
3. [`docs/pipeline-architecture-v1.md`](../architecture/pipeline-architecture-v1.md) — the canonical 10-phase architecture lock + the critic stack + draft→pro + the five named critic checkpoints. This is the shape everything is measured against.

**Pass 2 — Origin (where we started — these become the frozen "where we started" the roadmap supersedes for tracking):**
4. [`docs/2026-05-24-pipeline-v2-brainstorm.md`](../COMPLETED/pipeline-v2/2026-05-24-pipeline-v2-brainstorm.md) — the 5 TOP architectural ideas + 2 promoted principles (Critic-as-Principle, Draft→Pro). This is the spine of the "what we set out to build" checklist.
5. [`docs/2026-05-24-pipeline-v2-change-map.md`](../COMPLETED/pipeline-v2/2026-05-24-pipeline-v2-change-map.md) — the 9-commit sequence, the file-by-file deltas, the DAG-library rationale, and the **evals + traces workstream** scope.
6. [`docs/2026-05-26-agent-fleet-brainstorm-v2.md`](../COMPLETED/agent-fleet/2026-05-26-agent-fleet-brainstorm-v2.md) — the full **persona roster** (Maya, Cy, Sam, Bea, Flo, Em, Mo, the T3 council Codie/Annie/Sage + Chairman, the orchestrator), their model assignments, the **bake-off sequence**, and **Open Q1–Q6**. Every named agent and every open question here is a checklist row.
7. [`docs/2026-05-26-maya-planner-brainstorm.md`](../design/2026-05-26-maya-planner-brainstorm.md) — Phase 0 design decisions (deferred items + promotion triggers).

**Pass 3 — How we got here (the decision + build trail, chronological):**
8. `CHANGELOG.md` (repo root) — the append-only decision log; the chronological spine of "how we got here." Skim the whole arc; it dates every significant decision and its rationale.
9. [`docs/production-checklist.md`](../architecture/production-checklist.md) — the in-flight **pencil-test piece** tracker. Note its scope: it tracks one *artifact* (the Pencil Test acts/frames), not the *system*. ROADMAP.md tracks the system; clarify the division so they don't fight.
10. The post-mortems + field reports under [`docs/anima-test-runs/`](../anima-test-runs) — the lived record. At minimum read, in order:
    - `2026-06-02-operational-incidents-remediation-plan.md` (why the fleet-ops protocol exists — a real money incident)
    - `2026-06-11-first-integrated-run.md` (first orchestrator run, the seam log)
    - `2026-06-17-spark-authored-costed-run-post-mortem.md` (**the first live end-to-end run — its 5+1 findings, esp. Finding 1: Em mis-calibrated to Sean's eye, the autonomy blocker**)
    - `2026-06-17-bea-prompt-quality-field-report.md` (Tier-1 Slice A)
    - `2026-06-18-tier1-slice-b-field-report.md` (Tier-1 Slice B)
    - `2026-06-18-tier1-validation-run-post-mortem.md` (**the most recent run — Tier-1 fixes validated live + the harvested Em-vs-eye label table + new findings: leg-count blind spot, desk-drawing drift, Em self-contradiction, the identity_critical escalation gap**)
    - the Em-eval field reports (the `*-em-*` files: G5 re-baseline, G6 instrumented, G6.1b criteria-attached, Gate-3 fix-rate, Gate-2 calibration) — skim these as the "rabbit hole" exhibit: real depth, but it's the workstream that ran ahead of the roadmap.
11. [`docs/fleet-ops-protocol.md`](../architecture/fleet-ops-protocol.md) — the operating discipline for any costed/multi-step run (subscription billing, worktree isolation, single owner, clean teardown). A standing convention the roadmap should reference.

**Pass 4 — Current state from the tree (VERIFY — do not trust labels, including this kickoff and the prior session's review):**
12. `pipeline/run.py` + `pipeline/orchestration/` — what stages the orchestrator *actually* runs (`PLAN → SCRIPT → STORYBOARD → GENERATE → ASSEMBLE`). Confirm by reading, e.g., whether an Animatic stage exists.
13. `pipeline/agents/` — which personas are real code: `planner` (Maya), `character_designer` (Cy), `scriptwriter` (Sam), `storyboard_artist` (Bea), `frame_router` (Flo), `vision_critic` (Em), `museum_writer` (Mo), `t3_council`, `cost_estimator`.
14. `pipeline/dag.py` (the DAG runner) · `evals/` (the eval suites — `vision_critic/` is the deep one) · `characters/` (the locked Bibles) · `manifest.yaml` (the additive schema blocks: `phases`, `tiering`, `critics`, `characters`, `museum`, `brief`, `generation.routing`).
15. Run the suite to confirm green, and read `git log --oneline -30` for the recent build arc:
    ```bash
    source .venv/bin/activate
    python -m pytest tests/ -q && python -m pytest pipeline/tests/ -q
    git log --oneline -30
    ```

A roadmap built from the docs alone will inherit their optimism. Build it from the tree, and use the docs for *intent and history*. Where a doc claims something the code doesn't bear out (e.g., the agent-fleet brainstorm's Flo routing table lists Seedream/Qwen/FLUX, but CLAUDE.md records the Flo-B pivot to NB2; the plan says `identity_critical` forces Opus escalation, but the 2026-06-18 post-mortem found per-frame reads ran on Gemini) — **flag the discrepancy in the roadmap.** Discrepancies are some of the most valuable rows.

---

## Standing doctrine for this session

- **Verify against the tree, never trust a label** — including this kickoff. The prior session's strategic review (in `2026-06-18-tier1-validation-run-post-mortem.md` §5 and the conversation that produced it) concluded that **TOP-1 Animatic is unbuilt, the Museum layer is built-but-not-wired-into-runs, and Em is built-but-uncalibrated**. Treat those as *hypotheses to confirm against the code*, not findings to copy.
- **Two standing guards must never move.** This session writes only docs, but if anything you do touches the tree, re-check:
  - `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` → must stay `2af75906502f1caf8857e18828ceb2e4` (Em's eval baseline).
  - `md5sum pipeline/agents/prompts/sean-screenwriting-voice.md` → must stay `945af824fa53b948a18ac6bf206d67ef` (Sam/Bea's shared voice instrument).
- **$0, no spend, no building.** This is pure synthesis. Do not run the orchestrator, do not call a model, do not start any of the three upcoming phases. The only outputs are `ROADMAP.md`, a `CHANGELOG.md` entry, and a one-line pointer added to CLAUDE.md's "Start Here."
- **Read like a studio, not a terminal** (PHILOSOPHY). Prose where prose works; tables only for genuine reference data (the scorecard is genuine reference data). Studio-manual voice. The way the roadmap reads is part of the work.
- **Scope discipline is the whole point.** This document exists because the project over-runs scope. Model the cure: produce the roadmap, present it, stop. Don't slide into designing the Animatic phase because you got excited.

---

## The deliverable: `ROADMAP.md`

A source-of-truth tracker at the repo root, written so a future session can open it cold and know exactly where the project is and what to do next. Ground **every** status claim in evidence — a file path, a test name, a run dir, a CHANGELOG date, a commit. Suggested section shape (adapt if a better structure emerges, but cover all of this):

1. **What this is.** The framing: ROADMAP.md is the trajectory source of truth, read after PHILOSOPHY. Its contract: the project does not start a new workstream until the current one's Definition of Done is met. State that contract plainly — it's the anti-drift rule.

2. **Current focus (you-are-here).** The single active workstream, named, with its Definition of Done, and a one-line "what's explicitly *not* now." Per Sean's 2026-06-18 decision the active focus is **brainstorm + build the Animatic phase (TOP-1)**. Everything else waits.

3. **Where we started.** The original vision, sourced to the brainstorms: the 5 TOP ideas, the 2 promoted principles, the persona fleet, the evals workstream, the bake-off sequence. Compact — this is the baseline the scorecard grades against, not a re-print of the brainstorms (link them).

4. **How we got here.** The chronological arc in studio prose: the doc-only foundation → Bible → planner → DAG → the persona fleet builds → the Em eval saga → the first integrated run → the first live end-to-end run and its findings → the Tier-1 slices → the Tier-1 validation run. Sourced to CHANGELOG + the post-mortems/field reports. This is the "how we got here" Sean asked for — honest about the rabbit holes, not just the wins.

5. **The build scorecard (the checklist — the heart of the doc).** Every original idea / principle / persona / critic checkpoint / phase as a row, with a status and evidence and what's left. Suggested status taxonomy:
   - ✅ **Built + verified** (exists in code, tests green, exercised in a run)
   - ◑ **Partial** (built but not wired into the orchestrator, or lightly exercised, or schema-only)
   - 🔬 **Built but not calibrated** (works, but doesn't yet meet its quality/trust bar — Em is the case)
   - ⏳ **Deferred** (intentionally parked, with the promotion trigger named)
   - ❌ **Not built** (e.g., the Animatic phase)
   
   Cover at least: the 5 TOP ideas; the 2 principles (critic stack T1/T2/T3, draft→pro); each persona (Maya, Cy, Sam, Bea, Flo, Em, Mo, T3 council, orchestrator); the five named critic checkpoints (incl. the pending `post_animatic` gate); the evals workstream per agent; the bake-offs / Open Q1–Q6; the museum layer; the Character Bible primitive; the run orchestrator; the Tier-1 fixes. Each row cites its evidence and names what remains.

6. **The road ahead.** The three workstreams **in Sean's locked priority order**, each as a *to-brainstorm* placeholder — NOT a design (each gets its own brainstorm session before any plan):
   1. **Animatic phase (TOP-1)** — the unbuilt keystone. Why now: PHILOSOPHY calls it non-negotiable, and the 2026-06-18 run re-derived it independently (the placement / leg-count / shoulder problems are exactly what a human-authored rough-frame/stick-figure placement seed would fix). Capture the open questions to brainstorm (ingestion format — Procreate Dreams / PNG; how a rough frame conditions NB2 placement; where it sits relative to GENERATE; the `post_animatic` T3 gate), the dependencies, and a candidate Definition of Done. Do not design it.
   2. **Tier 2 — Em calibration** (the autonomy core) — flows out of the Animatic work (a placement seed reduces what Em must catch). The data is already harvested: the Em-vs-eye label table in `2026-06-18-tier1-validation-run-post-mortem.md`. Capture the open questions (threshold/severity vs detection-coverage; the L/R-axis unreliability shared by generator and critic; the mascot-anatomy blind spots; the identity_critical→Opus escalation gap; whether to wire propose→apply) and the hard guard: **any Em change is eval-gated; the verdict-baseline md5 only moves on a deliberate, ratified re-baseline.**
   3. **Museum** (make "the pipeline is the portfolio" true) — wire museum capture into the orchestrator and the Astro publish into `sw-ai-pm-portfolio`. Capture open questions and dependencies.

7. **Standing guards & conventions.** The two md5 guards; the fleet-ops protocol; the archive convention (`COMPLETED/`, `OLD/`); and **the maintenance rule for ROADMAP.md itself** — when a workstream's Definition of Done is met, update the scorecard and advance "Current focus" before starting the next. Model it on CLAUDE.md's maintenance conventions.

8. **Explicitly parked (so it's tracked, not lost).** The deferred items with their promotion triggers: Phase 6 Seedance motion (no motion piece run yet), Flo's multi-model in-between routing (pivoted to NB2; fal transports retained, self-hosted FLUX+LoRA ticketed), the deferred bake-offs (Open Q2 Sage tier, Open Q3 storyboard three-way, orchestrator drift test), propose→apply, the autonomous mode, Bible-authoring-as-project-type.

---

## How ROADMAP.md relates to the existing docs

- **Sibling to PHILOSOPHY.md**, read right after it. Add a one-line pointer in CLAUDE.md's "Start Here" so future sessions read PHILOSOPHY → ROADMAP → architecture lock → CLAUDE.md.
- **Supersedes the *tracking* function** of the three origin brainstorms (`2026-05-24-pipeline-v2-brainstorm.md`, `2026-05-24-pipeline-v2-change-map.md`, `2026-05-26-agent-fleet-brainstorm-v2.md`) — those stay as the frozen, dated record of *where we started* and the *why*; ROADMAP.md becomes the living tracker of *where we are*. Say so in both ROADMAP.md and (briefly) where it helps.
- **Does not duplicate** CLAUDE.md (the how-it-works manual) or `production-checklist.md` (the pencil-test *artifact* tracker). ROADMAP tracks the *system's* trajectory. Name the division so the three don't drift into each other.

---

## Definition of done for this session

- `ROADMAP.md` exists at the repo root, covers all eight sections, and every status row cites real evidence from the tree (not from the brainstorms' optimism).
- Discrepancies between the origin docs and the actual code are flagged in the scorecard, not silently reconciled.
- "Current focus" names the Animatic phase as the single active workstream, with a Definition of Done.
- A `CHANGELOG.md` entry is added (dated, with rationale, both md5 guards re-asserted as unchanged), and CLAUDE.md's "Start Here" gains the one-line ROADMAP pointer.
- The file is presented to Sean for review. No feature work started; no model spend; both md5 guards intact.

## Immediate first action

Confirm the tree state (`git log --oneline -5`, the two md5 guards, the green suite), then begin Pass 1 of the reading. When you've done all four passes, draft `ROADMAP.md`, present it, and stop. If the forward-path framing is ambiguous after reading, ask Sean one focused question — but the sequence is already locked (Animatic → Em calibration → Museum), so most of what's left is faithful archaeology and honest accounting.

*Build the map. Then we stop drifting.*
