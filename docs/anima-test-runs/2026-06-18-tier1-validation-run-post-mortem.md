# Post-Mortem — Tier-1 validation run: "The Spark, Shared," second pass

**Date:** 2026-06-18
**Run:** `runs/2026-06-18-spark-authored-run/` · slug `the-spark-shared`
**Command path:** `python -m pipeline.run --brief briefs/2026-06-16-spark-authored --slug spark-authored` → plan → script → storyboard-curation → 5 per-frame eye gates → assemble
**Spend:** Gemini-metered only — 5 NB2 frames + 10 Em reads (2 per frame), **zero retries** → at/near the $0.35 low band. Authoring (Maya/Sam/Bea, Opus + Sonnet) subscription-absorbed.
**Outcome:** Shipped. A clean 5-frame pencil-test loop at `runs/2026-06-18-spark-authored-run/export/` (gif/mp4/webm). **All five frames approved first-shot.**

> This run had two jobs and did both. **Job 1:** prove the Tier-1 fixes (Slices A + B) against live models for the first time — they all held. **Job 2:** harvest the Em-vs-eye labels that feed Tier 2 (the Em calibration campaign) — it produced the richest labeled set we have, including failure shapes the first run never surfaced. The headline: the pipeline is now visibly *better than the first run* (zero retries vs three attempts on F5 alone), and the autonomy blocker is exactly where we left it — Em's eye doesn't yet match Sean's, in both directions, now with specifics.

---

## 1. What shipped

Five keyframes on twos, one continuous fixed-camera two-shot, looping. Sean ¾ at the desk drawing; the terracotta mascot perched on his shoulder runs idle → look → (weak) perk → delight → settle. The loop returns (F5 ≈ F1). Reviewed against the brief's non-negotiables — stylus in the right hand, two distinct identities, terracotta box-creature held, cream-paper pencil register, 16:9 — the shipped loop passes Sean's eye. Every frame was a first-shot approval; **no frame needed a second attempt.**

## 2. Job 1 — did the Tier-1 fixes hold against live models?

All four, yes. This is the first time real Sonnet (Bea) + real NB2 (Flo) touched these fixes; stubs can't prove them.

| Fix (slice) | First run (2026-06-17) | This run | Verdict |
|---|---|---|---|
| **Terse edit-frame prompts** (A) | Sean hand-rewrote **all 4** edit prompts at the gate | Bea wrote F2–F4 as `Same fixed two-shot … ONLY CHANGE:` and F5 as `Composition identical to frame 1` — **board approved with ZERO hand-edits** | ✅ **Held — the biggest win.** The curation-cost metric we said to watch went from four rewrites to none. |
| **No text bleed** (A) | `A-2` / `A-7` / `C-B` labels bled into frames | **No label on any frame** (F01 top-left is clean; cf. first-run F01's stamped "A-7") | ✅ Held. Cleaned anchors + the no-text negative did the job. |
| **Loop-return holds first-try** (B) | F5 took **3 attempts** | F5 carried `chain_from: 1` + match-frame-1 authoring → **first-shot approval** | ✅ Held. The loop-return chaining off frame 1 (not the delight frame) is the structural fix proving out. |
| **Eye gate legible** (B) | gate printed only `verdict (conf, cites)` | gate prints Em's reasoning + proposed patch on flagged verdicts | ◑ Worked where used (F1/F2 decisions were made off the surfaced reasoning); F3–F5 were run straight through without pausing, so the live legibility wasn't leaned on for those. |

**Net:** the curation burden dropped to ~zero and the loop closed on the first try. The two slices earned out exactly as scoped.

## 3. Job 2 — the Em-vs-eye harvest (the Tier-2 data)

Ten per-character verdicts, all against frames Sean approved first-shot. This is the labeled set the calibration campaign runs on.

| Frame · char | Em verdict | Cites | Sean's eye | Read |
|---|---|---|---|---|
| F01 · sean | pass 1.0 | — | approve | **AGREE** |
| F01 · mascot | borderline 0.95 | `pose.shoulder-perch-canonical-pairing`, `anatomy.two-ear-arm-nubs` | approve | **OVERRIDE** — shoulder: detection-right / severity-over; ear-nub: **false-positive misread** (called the arm-nub a floppy ear) |
| F02 · sean | **fail 1.0** | `prop.stylus-right-hand-always` | approve | **OVERRIDE — false positive** (L/R misread; stylus *is* in the right hand) **+ blind spot** (missed a slight face drift Sean's eye caught) |
| F02 · mascot | pass 1.0 | — | approve | **AGREE** |
| F03 · sean | pass 0.98 | 5 IR rules | approve | **AGREE** |
| F03 · mascot | borderline 0.95 | `face.alert-perk-expression` | approve | **OVERRIDE — but defensible**: the perk reads weak; the arc is carried by F04's delight |
| F04 · sean | borderline 0.7 | `AC02` (invalid handle) | approve | **Em ERROR** — the "sean" pass reasons about the *mascot's* eyes (wrong-character attribution) and cites a non-existent handle |
| F04 · mascot | pass 0.98 | `face.delight-expression` + 3 | approve | **AGREE** — and Em correctly prioritized the Bible's delight over the storyboard's literal "widening eyes" prose |
| F05 · sean | pass 1.0 | — | approve | **AGREE** |
| F05 · mascot | borderline 0.95 | `face.construction-cross-line`, `face.two-dot-eyes-with-brows` | approve | **OVERRIDE** — register-detail strictness; (placement now correct, viewer's-left matching A-7) |

**What the table says about Em, in both directions:**

- **Over-strict / false-positive (her dominant failure mode this run).** Two of her flags are flat wrong: the **F02 stylus-hand `fail`** (she can't tell left from right any better than NB2 can — she reasoned "screen-right-facing → foreground arm is the left hand," and was wrong) and the **F01 ear-nub** (she misread the canonical arm-nub as a drooping animal ear). The F01 shoulder flag is the interesting middle case — her *detection* was correct (it really was on the wrong shoulder vs the beat), but she rated a perfectly good-looking frame `borderline`, so her **severity scale doesn't match Sean's accept line**.
- **Under-strict / blind spots.** She **missed the mascot's leg-count drift entirely** (see §4) and **missed the slight Sean face-drift on F02** that Sean caught by eye. So on F02's Sean she simultaneously over-called the hand and under-called the face.
- **Internal errors.** F04's "sean" verdict is a genuine malfunction: it critiques the *mascot's* expression under the `sean` namespace and cites `AC02`, which isn't a handle in this run's criteria. And across F04's two per-namespace passes she **contradicts herself** about the same mascot — the `sean` pass (0.7) says the eyes are "closed, squinting" and fail delight; the `mascot` pass (0.98) praises the "happy upward-arched crescent eyes." Same frame, opposite reads.

The L/R unreliability is the throughline: it shows up in F01 (shoulder) and F02 (stylus hand), and it's the *critic* failing the same axis the *generator* fails. That's two fixes, not one (§5).

## 4. New findings this run (not present in the first post-mortem)

### Finding A — Mascot leg-count drift, and Em is blind to it *despite the rule existing*

Sean's eye caught it immediately: the mascot shows **2 leg-nubs in some frames and 4 in others**. The canonical anchor has **4** (`character.yaml`: "four stub legs sit close together beneath the footprint"), and there is an enumerated rule for it — **`IR.claude-mascot.anatomy.four-stub-legs`**. Em cited it **zero times across all ten verdicts.** This is not a missing-rule problem (the handle exists, the same way G6.1 authored the geometry handles for Sean) — it's a **pure detection-coverage gap**: Em has the rule and didn't fire it. That makes it the *cleanest* Tier-2 target we have — measurable against a rule that already exists.

**Mechanism of the drift itself:** the establishing frame F01 rendered with only 2 nubs visible (Sean let it slide assuming 2 were occluded). F01 then became a chain reference for every later frame. So from F02 on, NB2 saw a *conflicting* reference stack — the approved F01 (2 visible) **and** the mascot anchor (4) — and resolved it differently frame to frame. The anchor was always present (see §6); the establishing frame disagreeing with it is what let the count wobble, with no T1/T2 gate to catch it.

### Finding B — The loaded object (the desk drawing) drifts every frame

The drawing on the page changes content shot to shot (F05 even resolves into a 3D box that wasn't there earlier). Over a 1-second loop the page should read as one continuous drawing. Sean's call: **not blocking — he'll hand-draw the page corrections** (this is exactly the human-owns-the-mark division of labor). But it's a flagged scaling risk: nothing pins the loaded object. There's no IR/AC rule for page content, and the chain doesn't lock it. For longer pieces this needs either a page-content constraint or a designated "draw the page by hand, composite it in" step.

### Finding C — `identity_critical` did **not** force Opus escalation on the per-frame reads

Every Em verdict this run is tagged `(gemini)` in `em_verdicts.jsonl` — i.e. all ten ran on Gemini, none on the Opus escalation the plan promised ("the `identity_critical` tags force Opus escalation on every identity read"). Reading the code: `run_frame_fan` sets `impact_tags = ["identity_critical"] if escalate else []`, and `escalate` is only True on an explicit retry path — first-generation reads pass `impact_tags=[]`, so the criteria's `identity_critical` tags never reach Em on the first pass. **Consequence:** this run's identity labels are *Gemini*-grounded, not Opus-grounded. That's fine for cost, but it's a real gap between the plan's stated behavior and the orchestrator's, and it matters for Tier 2 — if calibrated-Em is meant to gate identity autonomously, we need to decide whether first-pass identity reads should escalate, and the labels above were not collected under escalation.

## 5. What this means for Tier 2 (the Em calibration campaign)

The autonomy blocker is unchanged in shape from the first post-mortem (Em ≠ Sean's eye, both directions) but is now backed by specifics that point at concrete, separable work:

1. **The left/right axis is unreliable for the critic, not just the generator.** Em's two clear false-positives (F02 hand, F01 shoulder-detection-aside) are both L/R reasoning. *Fix candidates:* down-weight or re-ground L/R-dependent cites; and upstream, **seed generation with a rough/stick-figure placement frame** (the animatic phase as a hard placement constraint — Sean's own call, and a PHILOSOPHY load-bearing belief) so the generator stops guessing L/R and the critic has less to misread.
2. **The leg-count blind spot is the cleanest measurable target.** The rule exists; Em ignores it. A calibration pass should be able to move `four-stub-legs` detection from 0% to caught, and it's gradeable against the existing handle.
3. **Severity calibration is its own axis from detection.** F01's shoulder shows Em can detect correctly but rate `borderline` where Sean ships. The campaign needs to separate "did she see it" from "did she rate it like Sean would" — they're different knobs.
4. **There are correctness bugs, not just calibration gaps.** F04's wrong-character attribution + invalid `AC02` cite, and the F04 self-contradiction across namespaces, are robustness/parsing issues that no amount of threshold-tuning fixes. Worth a separate look before/alongside calibration.
5. **Decide the escalation question (Finding C).** The labels were collected on Gemini. If Opus-escalated identity reads behave differently, the calibration target may shift. Either wire first-pass `identity_critical` escalation and re-harvest, or explicitly decide Gemini-first is the calibration baseline.

**Guard, restated:** any Em change is eval-gated. The verdict-baseline md5 (`evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906…`) only moves on a deliberate, ratified re-baseline. This run touched nothing under `evals/vision_critic/`.

## 6. Answer to the reference question (for the record)

> *"When generating the remaining frames, are we providing just the establishing shot, or the establishing shot + the anchor images?"*

**Both — plus the prior approved frame.** Per `generate_stage.resolve_references`: frame 1 generates off the **cast Bible anchors** (sean's + the mascot's `anchor.png`) + any `extra_references`. Every later frame gets **`approved(F1)` + `approved(prior frame)` + the original Bible anchors again** (`chain_anchors` defaults to the full cast, so the anchors are re-injected on every frame) + extras. The loop-return F5 (with `chain_from: 1`) chains off `approved(F1)` instead of the prior frame, and the dedup collapses the duplicate.

So the mascot's 4-leg anchor *was* fed on every frame. The leg-count still wobbled because the approved establishing frame (2 nubs visible) sat alongside the anchor (4 nubs) in the reference stack and the two disagreed — a reminder that **an approved frame becomes an authority equal to the anchor, so a flaw you "let slide" on the anchor frame propagates as a competing signal.** (This run did *not* feed the A-7 pairing reference — Sean's deliberate call at the curation gate to test Bea's board standing alone; placement came from the solo anchors + prose, and it held well enough that Em judged F05's placement canonical.)

## 7. What this run doesn't decide

- **The Em calibration *method*** — more cases, a threshold re-fit, an L/R-grounding fix, a mascot-anatomy detection axis, a Sonnet/Gemini/Codex bake-off, or the escalation decision — is Tier 2's design pass. This run gives it data, not a method.
- **Whether to pin the loaded object** (Finding B) and whether to wire first-pass identity escalation (Finding C) are scoped here, not resolved.
- **Museum capture + the T3 pre-publish gate** still didn't run (not wired into the orchestrator). A full autonomous run needs them.
- **Anything beyond a 5-frame fixed-camera loop.** Moving camera, longer sequences, and dialogue will surface more — this is still the smallest honest test.

---

*Progress is real: zero retries, a clean loop, near-zero curation. The fleet is a better human-in-the-loop tool than it was 24 hours ago. The road to hands-off still runs through Em's eye matching Sean's — and this run handed us the sharpest map of that gap we've had.*
