# Tier-2, Slice 2 — the Em calibration (converged design)

> **⛔ SHELVED — NOT PURSUED (Sean's decision, 2026-07-01).** Tier-2 was closed *done-enough* the same day this was designed: Em is a good-enough gross-defect assistant, the construction-lines-detection target this design *leads with* turned out to be a **phantom** (Sean ruled `cld1/cld2/cld3` shippable — a faint/absent construction line is not a defect he'd reject), and per-character calibration was ruled **unscalable** for a many-characters project. This document is retained **only as the reasoning record** — the honest trail of why the calibration was designed and then deliberately *not* built. Do not execute it. See `ROADMAP.md` → *Current focus* for the decision.

*2026-07-01. Brainstormed with Sean in-session; this is the ratified design for the second slice of workstream 2 (Tier-2 Em calibration). Slice 1 — the mascot eval corpus + reference-blind baseline — shipped and was ratified 2026-07-01 ([field report](../anima-test-runs/2026-07-01-tier2-slice1-mascot-corpus-field-report.md)); this slice is eval-gated against that baseline. Predecessor design: [`2026-06-22-tier2-mascot-corpus-design.md`](2026-06-22-tier2-mascot-corpus-design.md). Baseline trace (the gate): [`evals/vision_critic/traces/mascot-baseline-2026-06-30.md`](../../evals/vision_critic/traces/mascot-baseline-2026-06-30.md). This is a **brainstorm artifact — a design, not a plan.** No build, no plan, no costed run until Sean ratifies it.*

---

## Why this, why now

Slice 1 made the mascot measurable and handed us a number and a seam. The number: reference-blind, N=5, **performs (n=46) precision 0.93 / recall 0.90 / false-pass 0.10, cites 0.17** — measurably weaker than sean's G5 (0.97 / 1.00 / 0.00), *which was the point.* The seam is not spread across classes; it is concentrated in one: **all three false-passes are the construction-lines-absent class** (`cld1/cld2/cld3-cleaned-*`). Reference-blind, Em passes a cleaned-up final that carries no visible pencil under-drawing. On the runs where she *does* catch it she cites `IR.claude-mascot.face.construction-cross-line` correctly at 0.98–1.00 confidence — so this is a **detection-sensitivity gap, not a grounding gap.** It is exactly the finish-register drift the 2026-06-21 driven run flagged by eye.

Slice 2 is where Em actually moves toward Sean's eye — and the first honest step is to notice that **we have never measured her in the config she actually runs in.**

## The reframe that shapes everything

Slice 1's baseline was run **reference-blind** to be directly comparable to sean's G5 protocol. But production Em ships `critics.t2.attach_criteria_text: true` (flipped globally at G6.1b, 2026-06-08 — the exact fact the Slice-1 kickoff got wrong until the tree caught it at spend-time). So the ratified 0.93 / 0.90 / 0.10 is a **comparability artifact, not the production number.** The mascot has never been scored in its real config.

That reframes the lead move: measuring criteria-text-on is not merely an experiment, it is a **correction** — measuring production reality for the first time. And it sets up the central question cleanly. The construction-lines-absent defect is the *absence of a faint feature*. The eval handbook (§3.5) is blunt about this class: MLLM judges are weakest on **low-level / faint visual quality** (Q-Bench: "preliminary and imprecise" on distortion/blur/artifact), and the prescription is to **back it with deterministic T1 rules / DINOv2, not lean on the MLLM alone.** Against that, the handbook also documents that **criteria injection is a large, cheap alignment lift** (Databricks "Grading Notes": 67–85% misalignment cut). So the empirical question is sharp and worth money to answer:

> Can *any* grounding config or a stronger model lift Em's detection of an absent under-drawing — or is this the class where the honest fix is a deterministic backstop, not a better prompt?

## The trust bar (unchanged, restated)

Tier-2's "done" is **trustworthy assistant** — Em's flags get good enough that Sean spot-checks the frames she flags instead of reviewing every one, with **false-pass held low.** Full hands-off autonomy and propose→apply auto-fix stay as later exits, not this workstream's bar. The handbook's calibration lodestar applies directly: **match Sean's judgment *including its variance* (|z| < 1), don't exceed his consistency.** A "super-consistent" Em that is *more* strict than Sean is a worse judge, not a better one — which is the lens through which the clean false-positives get read (below), not a defect to prompt away.

---

## The decomposition

Slice 2 splits the way Slice 1 did — a safe measurement slice first, then a data-driven fix.

### Slice 2a — the configuration bake-off + the severity-axis scorer

**Pure measurement plus *additive* scoring. Nothing in [`pipeline/agents/vision_critic.py`](../../pipeline/agents/vision_critic.py) changes; no prompt edit.** 2a:

1. establishes the mascot's **true production config** by letting the grounding configs and the Opus arm compete on the numbers;
2. re-establishes the **gate-baseline under that winning config**, in its own dated trace;
3. quantifies how much of the construction-lines-absent gap grounding and/or a stronger model close **for free**;
4. makes **severity measurable, separately from detection**, via an additive extension to [`scoring.py`](../../evals/vision_critic/scoring.py).

Because it never touches Em's code and writes only a new mascot trace plus additive scorer functions, 2a **cannot move the frozen sean verdict md5** — it is as safe an entry as Slice 1 was.

### Slice 2b — the residual fix (shape deliberately deferred to 2a's data)

Scoped to *only* whatever 2a leaves open, eval-gated against 2a's ratified config-baseline. **We do not design the fix before we have the measurement.** The handbook already names the leading candidate for the construction residual: since construction-lines-absence is the MLLM's weakest class, the honest fix is most likely a **deterministic T1 construction-line-presence backstop** — Bible-lock / T1-owned per the locked layer-ownership map (style classes are Em-owned in production, but *detecting the absence of a faint feature* is precisely where the handbook says use a deterministic gate), **not** an Em prompt clause. That reading is a hypothesis 2a tests, not a decision made now. 2b gets its own build-brainstorm once 2a's numbers are in.

### The decision tree between them

- If a Gemini grounding arm (criteria-text or reference-images) closes construction detection with false-pass held → **flip that as the mascot production config, re-baseline, and 2b may be empty** (no Em code change; frozen md5 untouched).
- If only the **Opus arm** closes it → the fork becomes the escalation decision (2b / discrepancy B): wire first-pass identity escalation vs. accept the cost, informed by real data.
- If **no arm** closes it → the residual is confirmed as the MLLM-weak class, and 2b leads with the **deterministic T1 construction-line backstop**, eval-gated against the best config from 2a.

---

## Slice 2a in detail

### The bake-off matrix

Arm 1 exists (Slice 1's ratified blind baseline). The three new arms:

| Arm | Grounding | Model | What it answers |
|---|---|---|---|
| 1 | blind | Gemini | the ratified reference (already have it) |
| 2 | criteria-text | Gemini | **production reality** — the primary gate candidate |
| 3 | +reference-images | Gemini | does *seeing* a reference lift absence-detection (lever off in prod; measured here) |
| 4 | criteria-text | Opus-forced | does a stronger model see the absent under-drawing |

The levers already exist in [`score.py`](../../evals/vision_critic/score.py): `--attach-criteria-text`, `--attach-references`, `--reference-blind`, `--character-id claude-mascot`, all run-scoped and forwarded to every per-case worker (the Slice-1 tooling that made blind-vs-attached honest). The Opus arm is forced via the `identity_critical` escalation path, exercised through the existing `escalation_tags` machinery — this is also the arm that supplies data for discrepancy B without yet wiring anything into the orchestrator.

### Cost staging (smoke-first, Slice-1 discipline)

Run a **targeted construction-class smoke first** — the four construction cases (`cld1/cld2/cld3` + the `clb1` borderline) plus a clean control, all four arms, N=5. Cheap, and it answers the priority fork before committing to a full re-baseline. Only after the smoke names a winning config does the **full 46 × N=5 re-baseline of that config** run to produce the ratified gate. The Opus arm (4) goes full **only if** the Gemini arms leave construction open — keeping Opus spend bounded. This mirrors the Em-saga instrumented-mini-run → full-baseline sequence and Slice 1's `--limit 2` live smoke.

### The severity axis (additive to `scoring.py`)

Today the scorer counts `{fail, borderline}` both as "flagged," so **detection and severity are fused** — it cannot tell "Em saw it but under-rated it" from "Em over-flagged a shippable frame" from "Em missed it." The handbook prescribes the fix directly (§2, §6): grade the **outcome (did she detect the defect)** separately from the **threshold call (should this have been a fail)**, and treat the latter as *its own labeled question.*

So 2a extends `scoring.py` with a **severity axis** scored against Sean's three-level labels, reported *alongside* the detection axis and never merged into it:

- **over-severity** — Sean labels pass/clean, Em flags borderline/fail. The clean-FP over-caution (`clean-c02`, `clean-c07`) and the 06-21 finish over-flag land here. Read through the handbook's **|z| < 1** rule: over-severity is Em exceeding Sean's strictness, which is a *worse* judge, and the axis makes it a tracked number rather than an anecdote.
- **under-severity** — Sean labels fail, Em softens to borderline/pass. Generalizes the existing `borderline_slippage`.
- **threshold probes** — the corpus's borderline-labeled cases (`pb1`, `vb1`, `clb1`, `shb1`) are the direct fixtures for where Em's accept line sits vs Sean's.

Strictly additive: existing detection metrics, the mocked-runner assertions, and the segmented report shape are unchanged. The sean verdict baseline is a frozen *trace file*, not a `scoring.py` output, so additive functions cannot move it.

---

## The six brainstorm inputs — where each landed

1. **Construction-lines-absent detection (the priority).** The lead target. Resolved *empirically first* by the 2a bake-off, before any code change. The handbook flags it as the MLLM-weak class, so the T1-backstop is the standing 2b candidate if grounding/Opus don't close it.
2. **Severity vs detection, separated.** Built into 2a as the additive severity axis. The corpus's borderline cases are the threshold probes.
3. **Leg-count / anatomy (the 06-18 blind spot).** Reframed: the corpus `ad1–ad6` already pass reference-blind, so this is **not a live detection failure in the corpus** — it is a **corpus-coverage question.** The 06-18 miss was on *subtle / occluded* drift (2 visible nubs vs the anchor's 4), not the extreme single-axis defect the corpus carries. **Deferred** to a measurement add: borderline anatomy fixtures (Sean in Flow, $0, Slice-1-shaped) that probe the realistic drift. 2a's findings will state whether the extreme cases suffice or the borderline set is needed. *Promotion trigger: the driven-run leg-count miss recurs, or 2a shows the anatomy class needs a borderline tier to be honest.*
4. **The view seam handle → real `IR.claude-mascot.view.*` rules.** This is a **citation-floor** fix (it would lift `cites` on the view class, which currently names a handle the Bible doesn't carry), **not** a detection or severity fix — the view cases (`vd1–vd4`) already fail correctly. **Deferred.** *Promotion trigger: view-class citation grounding becomes load-bearing for the production trust bar, or it bundles into a dedicated G6.1-style mascot-citation slice.*
5. **The 2 clean false-positives (`clean-c02`, `clean-c07`).** A **calibration question, not a fixture change** — Sean ratified them accepted-red (Em over-caution). 2a's severity axis makes the over-caution measurable and trended under the |z| < 1 rule; per ships-red, no label is edited to flatter Em, and any severity tuning is 2b's call against 2a's number.
6. **The standing open questions.**
   - **L/R-axis unreliability** (shared by generator *and* critic) — the animatic placement seed already mitigates it upstream. Known hard axis, not this slice's target. **Deferred** with trigger: promote if a driven run shows L/R misreads dominating Em's false-positives after the construction gap closes.
   - **`identity_critical` → Opus escalation gap (discrepancy B).** 2a's arm 4 *tests* Opus without committing to it. **Wiring** first-pass escalation is deferred to 2b and gated on arm 4's result.
   - **propose→apply.** The autonomy exit; stays parked per ROADMAP until Em is calibrated.

---

## Guards (load-bearing)

- **`vision_critic.py` byte-unchanged in 2a.** No prompt edit, no contract change; the `cites_criteria` invariant and verdict vocabulary are off-limits.
- **`scoring.py` additive-only.** New severity functions; existing detection metrics and the segmented report byte-stable.
- **The two frozen md5s do not move:** the sean verdict baseline `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4`, and the shared voice `pipeline/agents/prompts/sean-screenwriting-voice.md` = `945af824fa53b948a18ac6bf206d67ef`. The mascot bake-off writes its own dated traces; the sean 52 cases stay untouched.
- **Ships-red discipline.** A red case is a finding, never tuned away; a label is edited *only* as a validity fix, never to flatter Em. Sean is the single labeler and decider; Em proposes, Sean decides.
- **Fleet-ops.** Subscription billing (never `ANTHROPIC_API_KEY`), the env-strip operator path, smoke-before-burn, clean teardown — the Slice-1 costed-run discipline carries over verbatim.
- **Anti-drift.** Current Focus stays Tier-2; nothing outside it opens until the DoD is met. 2b gets its own build-brainstorm — this design does not pre-authorize a fix.

## Cost

Subscription Gemini throughout, bounded Opus on arm 4. Staged: the construction-class smoke is a few dozen case-runs; the full winning-config re-baseline is ~46 × 5 ≈ 230 case-runs (Slice-1 scale); arm 4 full only if triggered. In the **~$2–15 band**, subscription-absorbed, fleet-ops-governed, Claude-Code-driven with Sean making every taste call.

## Slice 2a — Definition of Done

1. A **ratified mascot production-config decision** — which arm (blind / criteria-text / +references / Opus-forced) the mascot ships in, chosen on false-pass + construction-detection numbers.
2. A **re-established gate-baseline** under that config, in its own dated trace, replacing the blind 0.93 / 0.90 / 0.10 as the number Slice-2b changes are measured against (the blind trace stays as the comparability reference).
3. The **severity axis live in `scoring.py`** and reported in the mascot segment report, with the clean-FP over-caution and the borderline threshold probes read against the |z| < 1 rule.
4. A **findings doc** that scopes Slice 2b — states whether grounding/Opus closed construction detection, whether the anatomy class needs a borderline tier, and which residual (if any) 2b leads with.
5. **Guards proven:** sean md5 + sean 52 cases untouched; `vision_critic.py` byte-unchanged; `scoring.py` additive-only.

## What it unblocks

Once 2a names the production config and the real gate, **Slice 2b — the residual detection/severity fix — becomes eval-gated, safe Em work.** That is where Em finally moves toward Sean's eye on the construction-lines axis; this slice is what makes that movement measurable, honest, and cheap to attempt first without touching Em at all.

---

*Discipline note: this is a brainstorm artifact. The terminal state is this ratified design plus the decomposition — no implementation plan, no code, no costed run until Sean ratifies. Slice 2b is intentionally under-specified: its shape is a function of 2a's data, and pre-designing it would be the drift this project is built to refuse.*
