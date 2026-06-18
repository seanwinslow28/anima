# Animatic phase — converged design (v1: the placement seed)

*2026-06-18. Brainstormed with Sean in Cowork; this is the ratified design the build session works from. It settles the five open questions the [ROADMAP](../ROADMAP.md) reserved for the Animatic brainstorm and names the one bet the whole thing rests on — plus the cheap test that proves or kills it before any plumbing gets built. The build handoff is [`2026-06-18-animatic-phase-kickoff.md`](2026-06-18-animatic-phase-kickoff.md).*

---

## Why now

The Animatic phase (TOP-1) is the single non-negotiable belief in [PHILOSOPHY](../PHILOSOPHY.md) — *"the human owns timing; AI that generates motion without a human-authored timing constraint is the template trap, and the template trap is the only thing that kills this project"* — and the one keystone idea from the original architecture that was never built. The ROADMAP exists in large part because of that gap: the fleet went five rounds deep on Em's eval suite while the keystone it was meant to support sat unbuilt.

And the most recent live run re-derived the need on its own. The [2026-06-18 validation run](anima-test-runs/2026-06-18-tier1-validation-run-post-mortem.md) shipped a clean five-frame loop, but the mascot landed on the wrong shoulder in places, drew at inconsistent scale, and wobbled between two and four legs frame to frame. The throughline diagnosis: **the image model cannot reliably tell left from right, and it guesses placement from prose.** Sean's own words — *"start with my pre-drawn stick figure so NB2 knows exactly where the characters should be."* That is the animatic phase, arriving as a felt need rather than a planned one.

## The reframe — what the animatic is FOR

The origin docs ([pipeline-v2-brainstorm](2026-05-24-pipeline-v2-brainstorm.md) TOP-1) framed the animatic as a **timing** seed: block motion in shapes, feed it to Seedance so the *motion* respects the human's timing. The field evidence points somewhere adjacent and more urgent — a **placement** seed for *stills*: pin where characters stand, which way they face, their scale, the shoulder side, the leg count, before any frame is drawn. Those are two different products that share a name, and one of them (timing-for-motion) has no consumer today because Phase 6 Motion isn't orchestrated.

The converged scope keeps **both**, but sequences them honestly so neither half is built ahead of a consumer:

- **Placement** is the live problem and the half with the unproven model bet. It conditions GENERATE.
- **Timing** rides along on the same human-authored pass — honoring "the human owns timing" in full rather than half — and is wired to the consumer it actually has *today*: the loop's hold durations and pacing at ASSEMBLE. The same timing data is captured for Seedance to read *later*, when Motion is promoted.

This is the anti-drift discipline applied to the design itself: every half ships with a job today. We are explicitly **not** building Seedance/motion conditioning in this phase.

## The design

### One human-authored pass, two consumers

The human draws one rough, shape-block pass of the piece — stick figures and silhouettes, thirty seconds a frame. It is the animation equivalent of a director walking the set and taping marks on the floor before the cameras roll. That single pass carries two things: **where everyone is** (the placement) and **how long each pose holds** (the timing). Placement feeds drawing; timing feeds the cut.

### The stage — a human author-and-ingest gate

A new **opt-in ANIMATIC stage** sits between STORYBOARD and GENERATE. It is structurally a twin of the storyboard curation gate — the orchestrator pauses for human authoring, then a deterministic ingest step validates and advances:

```
storyboard-approve  (board locked)
   → ANIMATIC: orchestrator pauses
        → Sean drops placement roughs into the run's animatic directory + sets holds
   → approve-animatic: deterministic ingest validates the roughs, wires each into its
        shot, records the holds, captures the artifacts → advances to GENERATE
```

The stage comes **after** storyboard-approve on purpose: the roughs are placement for specific, already-locked shots, so they depend on the board existing. The board stays the source of beats and prompts — the rough *constrains* generation, it does not replace the board. Prose placement (from the board) and the visual rough reinforce each other, which is exactly what the [NB2 editing research](research/2026-05-30-nb2-editing-character-consistency-template.md) calls for: the image carries the *where*, the prompt clause names it.

**Opt-in, default off.** A run that provides no animatic goes STORYBOARD → GENERATE exactly as today — the pencil-test and every existing run stay byte-for-byte identical. The stage is switched on per run when the human wants the extra control. This is the same back-compat discipline the orchestrator already uses to auto-detect its two run modes.

### The data contract — one contract, Dreams-compatible later

The run's animatic directory holds frame-named placement roughs (one per keyframe, matching the board's frame ids) plus a small holds sidecar expressing timing as integers. The ingest step validates that each rough names a real frame and the sidecar parses, then it populates each shot's placement reference *from the convention into the run's durable state* — **the locked board file is never mutated** — and overrides the run's hold values from the sidecar (which ASSEMBLE already reads).

This is one contract, not two parsers. It is the honest version of the origin doc's "ingest both Procreate Dreams and PNG stacks": a Dreams frame-export can populate the *same* frame-named directory + timing later, with no schema change. Dreams' continuous timeline is overkill for on-twos holds anyway. We build one ingestion path now.

### The mechanism — a role-tagged placement reference

A new **optional, per-frame placement reference** on the shot schema. When absent it resolves exactly as today (byte-identical — this is the back-compat hinge). When present, it is **appended last** in the generation reference stack, and Flo's prompt gets a positional role-tag clause:

> *"The final reference is the composition target: match the character positions, facing direction, and relative scale shown there; do NOT copy its line quality, colour, or style — identity comes only from the character anchor(s)."*

The image carries the staging; the clause quarantines the look. This directly answers the two failure modes the NB2 research names: the **reference-gap** failure (the model invents what it can't see — the L/R drift) is fixed by supplying a dedicated reference for the thing we want controlled; the **attribute/context bleed** failure (a reference's style leaking into the subject) is prevented by the explicit "don't copy its look" role-tag. It is optional **per frame**, so the human can author at least the establishing frame, or one rough per key.

## The load-bearing assumption — and the cheap test that gates the build

Everything above rests on one bet:

> **A hand-drawn stick-figure placement rough actually makes the image model respect placement** — shoulder side, scale, leg count, left/right.

If that is false, the stage is wasted plumbing. So the **first build step is a costed spike, before any orchestrator code** — and the corpus is even better than reproducing the drift: a **skateboard kickflip** from a prior project (18 hand-drawn roughs Sean already has), curated to six keys, single character (Sean's anchor, no mascot). It tests the bet harder and on a more honest question — *can a rough push Sean into poses far outside his sitting-and-drawing register, while holding his identity?* The roughs are a finished *different* character on a pink ground, so the role-tag quarantine is stressed at its hardest. Feed each key as a role-tagged reference through the existing image-edit transport (no orchestrator changes needed), regenerate against Sean's anchor, and judge with Sean's eye — *the engine-truth arbiter* — whether the rough lands the pose and Sean stays Sean. A built-in **A/B** (the colored rough as-is vs. a stripped pose silhouette, on two keys) answers whether finished roughs work or silhouettes are needed. The loop-specific sub-questions (establishing-frame-only propagation, fifth-reference dilution) ride to the first costed *loop* run — they don't map to a one-shot kickflip.

About a dozen image calls (~$2.5), Gemini-metered. **Green spike → build the stage. Red or ambiguous spike → stop and rethink the mechanism** (a stronger conditioning approach, or leaning harder on the prompt's staging vocabulary) before spending effort on the gate. Empirical, not vibes — the spike is the eval-gate for the central bet. The corpus is prepared and turnkey at [`images/anima-frames-test/spike-selection/`](../images/anima-frames-test/spike-selection/) (the full 18 stay in the parent dir for the proven-bet follow-on + museum piece). The authoring-effort question (the original #1 risk: *will Sean actually draw these every run?*) gets its own test later, when Sean draws roughs for a real loop run.

## Consciously deferred — seam kept, trigger named

The **`post_animatic` T3 critic gate** is declared in the manifest but stays unwired in v1. T3's job is to validate a *timing arc* before tens of dollars of downstream Seedance burn — but v1 has no orchestrated Motion, the human just authored the roughs (they are the timing author *and* the eye), and a three-CLI council critiquing stick figures is several minutes of compute for unclear signal. We keep the manifest seam declared and place the one-line hook point in the new stage, and we **promote the gate when the timing-animatic feeds an orchestrated Motion phase** — when a bad timing arc actually costs Seedance money. This is distinct from the deterministic ingest validation, which runs at the gate regardless; that is plumbing, not a critic.

## Out of scope for this phase

- **Seedance / motion conditioning.** Deferred with Phase 6 Motion; the timing artifact is captured for it.
- **Pinning the loaded object** (the drifting desk drawing, Finding B in the post-mortem). Sean's call: he hand-draws the page — the human-owns-the-mark division of labor. Not this phase.
- **The Em escalation question** (Finding C) and any Em / eval change. That is workstream 2 (Tier-2 calibration), and the verdict-baseline md5 is guarded.
- **Anything beyond a fixed-camera placement+holds animatic.** Moving camera and longer sequences will surface more; this is the smallest honest version.

## The decisions, and what was weighed against them

| Question | Decision | What was rejected, and why |
|---|---|---|
| What is it FOR? | Both placement + timing, honestly sequenced | *Placement-only* (loses the philosophy's "human owns timing" in full); *timing-only / full Seedance now* (builds a producer with no consumer — the exact unsequenced-depth pattern the ROADMAP exists to stop) |
| Format | PNG roughs per keyframe + a holds sidecar; one ingestion contract | *Procreate Dreams timeline* (heavier authoring, overkill for on-twos; raises the "will Sean skip it" risk); *building dual parsers now* (two code paths before either is proven) |
| Mechanism | Dedicated optional per-frame placement reference, appended last + role-tagged; back-compat | *Reuse the existing extras list* (conflates placement with identity/style refs; can't quarantine the rough's look); *establishing-frame-only by design* (can't correct a per-frame facing change) |
| Pipeline placement | Separate opt-in ANIMATIC stage between STORYBOARD and GENERATE | *Fold into the storyboard gate* (lighter, but demotes the one stage PHILOSOPHY calls non-negotiable); *default-on for authoring runs* (a stronger nudge, but opt-in keeps the human's choice explicit per run) |
| `post_animatic` T3 gate | Consciously defer; keep seam + hook point | *Wire the full council now* (compute critiquing roughs the human just authored, before any Motion burn exists to protect); *a lightweight coherence check* (largely redundant with the human author-and-eye) |

## PHILOSOPHY check

- **The human owns timing and taste.** This stage is its literal structural form — the human blocks placement and timing by hand before a frame is drawn. ✅
- **The critic earns its keep by proposing fixes.** Em still runs per-frame at GENERATE proposing prompt diffs; deferring the T3 *timing* gate doesn't weaken that. ✅
- **Iteration must be cheap.** Spike-first; back-compat means the content-addressed cache and existing runs are untouched. ✅
- **The pipeline is the portfolio.** The roughs plus the drift-vs-placement-locked before/after are museum gold — *"we drew stick figures so the AI knew where to stand."* (Capture is workstream 3; the artifacts this phase produces are capturable by design.) ✅
- **Empirical, not vibes.** The spike is the eval-gate for the central bet, judged by the engine-truth arbiter. ✅
- **Read like a studio, not a terminal.** This doc and the kickoff are authored, not generated. ✅
- **Not a click-to-generate service.** The human-authored animatic is the structural refusal, now real in the line. ✅

## Definition of Done (refines the ROADMAP candidate)

1. This ratified design doc (done) and the Claude Code execution kickoff.
2. **A green costed spike** proving a placement rough makes the model respect placement, with a field report and a go/no-go — *before* the stage is built.
3. The ANIMATIC stage wired into the run orchestrator between STORYBOARD and GENERATE, opt-in, with its own author-and-ingest gate; existing runs byte-identical (back-compat tests green).
4. The placement reference mechanism wired into generation, role-tagged; the timing sidecar driving the loop's holds at ASSEMBLE; both captured in the run's animatic directory.
5. The `post_animatic` T3 gate consciously deferred — seam kept, hook point placed, promotion trigger recorded.
6. A costed run that exercises the new stage end-to-end and ships a loop whose placement holds.
7. Both md5 guards intact; nothing touched under `evals/vision_critic/`; ROADMAP updated.
