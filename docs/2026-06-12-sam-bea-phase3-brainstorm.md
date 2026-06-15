# Sam + Bea — Phase 3 Storyboard Brainstorm

*The writers' room and the board artist — the last two named agents. Dated 2026-06-12. Cowork brainstorm; $0, no model spend. Companion to the [Sam build plan](2026-06-12-sam-scriptwriter-build-plan.md) and the [Sam kickoff](2026-06-12-sam-scriptwriter-kickoff.md).*

> **⚠ Updated 2026-06-15 — read [`2026-06-15-screenwriting-modes-integration-addendum.md`](2026-06-15-screenwriting-modes-integration-addendum.md) before building.** Sean's `screenwriting-modes` skill now exists, so Sam vendors the **full** voice instrument (not a condensed note). This supersedes §8 row 1 (the deferred-calibration row) and the §5 "condensed register note" bullet. Everything else here stands.

---

## Why this is the session that completes the fleet

The fleet has agents on both sides of Phase 3 and nothing in the middle. Maya plans the piece (Phase 0). Flo and the orchestrator generate it (Phase 5). In between sits the one artifact the orchestrator can't author itself: `shots.yaml`, the human-written frame list. Today Sean writes it from scratch — by hand, every frame, every prompt. Sam and Bea are the missing middle. They draft that file *for* him to curate.

This is the whole structural payoff, and it's worth saying plainly before any design detail:

```
Maya (Phase 0)  →  plan.md
        ↓
Sam (Phase 3a)  →  script.md + beats.json          [human gate: script approve]
        ↓
Bea (Phase 3b)  →  storyboard.md + draft shots.yaml  [human curation gate: storyboard approve]
        ↓
Sean curates    →  shots.yaml (the locked run input)
        ↓
Orchestrator    →  Flo / T1 / Em per frame  →  assemble
```

Phase 0 and Phase 5 already exist on both ends. Sam and Bea close the loop. After they land, every node of that graph has an agent — and the human still owns the only node that matters: the curation gate where a *draft* becomes the *run*.

## The thing that must not happen

Phase 3 is, in the architecture's exact words, *"mostly human-authored. Agents assist with prompt drafts and continuity checks; they don't pick beats."* PHILOSOPHY says it harder: the human owns story, character intent, and timing; the animatic phase is non-negotiable; *"AI that generates motion without a human-authored timing constraint is the template trap, and the template trap is the only thing that kills this project."*

So the failure to design against isn't a bug — it's a category error: **Sam and Bea writing the movie instead of drafting a proposal the human reshapes.** Every decision below is bent toward *propose, don't decide*. The agents are fast hands in the writers' room. Sean is still the director.

---

## 1. The two roles, in one paragraph each

**Sam — the scriptwriter (Phase 3a, Opus).** Sam reads Maya's `plan.md` plus the Studio Brief and the cast's Character Bible references, and drafts the *script*: a short prose treatment and a structured beat sheet — the sequence of story beats, each with intent, emotional arc, and timing feel. Sam does not lock the beats; Sam *proposes* a structure for Sean to cut, reorder, and rewrite. Sam writes in Sean's register — comedic, specific, earned-not-mugging ("a quiet beat, not a gag," as the Spark beats put it) — not generic screenplay pastiche. Sam is Opus because the failure mode that matters is depth: surface pastiche versus real modeling of *why* a beat lands. The taste call is the human's; Sam's job is to give the human something true enough to react to.

**Bea — the storyboard artist (Phase 3b, Sonnet).** Bea reads Sam's approved beat sheet plus `plan.md` and the Bible references, and turns beats into the *shot list*: each beat becomes one or more shots, each shot carrying per-shot intent and camera/composition notes. Bea drafts two artifacts in lockstep — a human-readable `storyboard.md` (Phase 3's named output, in studio voice) and a **draft `shots.yaml`** (the orchestrator's machine input). Both are proposals. The shots.yaml is born unlocked and never auto-feeds a run; Sean curates it through the gate. Text-only in v1 — structured shot descriptions and camera notes, no generated panels. Bea is Sonnet, and per the eval handbook the lowest-confidence assignment in the fleet (65%) — which is exactly why her output is gated by a *deterministic* check (does the draft parse against the real schema, does every beat get a shot) and a human preference call, not by trusting the model.

---

## 2. PM perspective — value, alignment, impact

The business case is the loop-closer. Maya and Flo are expensive infrastructure that currently dead-ends into a manual step: Sean transcribing a story into a 5-to-N frame YAML file with hand-written generation prompts. That's the slowest hands in the pipeline, sitting in the middle of the fastest. Sam and Bea convert "Sean writes shots.yaml from a blank page" into "Sean curates a drafted shots.yaml" — the difference between authoring and editing, which is the difference the whole project is built to deliver ("the pipeline exists to give the human the fastest possible hands").

Strategic alignment is exact: this is the last roster gap. The eval handbook's canonical fleet is Maya / Cy / Em / Mo / Flo / Sam / Bea / T3 / orchestrator. Eight of nine exist. Completing it makes the museum's "human + fleet" claim literally true end-to-end, and it makes the *next* piece cheaper to start — the first real test of anima-as-reusable-pipeline rather than anima-as-one-shipped-loop.

Customer impact (the customer is Sean, then the museum's reader): the museum gets a new exhibit class it can't show today — *the fleet drafting its own shot list, and the human's red pen on top of it.* That's the most honest possible illustration of the thesis. The draft and the curated diff, side by side, is the evidence.

## 3. Designer perspective — experience, usability, delight

The experience to protect is the gate. Maya's plan gate and Cy's Bible lock already taught Sean a rhythm: agent proposes → `show` renders a clean tear sheet → human reads, edits, approves. Sam and Bea must feel identical. `script show` and `storyboard show` render terminal tear sheets in the same studio voice; `script approve` and `storyboard approve` are the same idempotent lock. No new ceremony to learn — Phase 3 should feel like two more stops on a road Sean already drives.

The delight is in the curation, not the generation. The wrong design makes Sean feel replaced ("the AI wrote my movie"); the right one makes him feel amplified ("the AI gave me a full draft and I made it mine in ten minutes"). The artifact contract enforces this: the draft `shots.yaml` is *visibly* a draft — unlocked, annotated with Bea's confidence hedges, never the thing the orchestrator runs until Sean has touched it. The friction is intentional. The gate is the feature.

One real usability risk: Bea's hardest output is the per-shot `prompt` field — the actual Flo generation prompt in the pencil-test register. If Bea writes weak prompts, Sean rewrites all of them and the loop-closer saved him nothing. Mitigation (carried into the build): seed Bea with the register clause exemplars and the Spark prompts as few-shot anchors, and measure *revision count* as the headline Bea metric — if Sean rewrites every prompt, Bea isn't done.

## 4. Engineer perspective — leverage, contracts, what's cheap

The leverage is that the hard contract already exists. `pipeline/orchestration/shots.py:load_shots` is a strict validator: slug pattern, strictly-ascending frame ids, non-empty beat and prompt, `cast ⊆ known IR namespaces`, `chain_anchors ⊆ cast`, `hold ≥ 1`. Bea's draft `shots.yaml` is validated *by the very function the orchestrator consumes it with* — so "does Bea's output parse and cover the cast" is a free, deterministic, zero-cost gate. This is the handbook's "deterministic coverage checks" handed to us by construction. We don't build a Bea-quality metric; we run her output through the real schema.

Symmetrically, Sam needs a typed contract to hand Bea. Mirror `shots.py`: a new `pipeline/orchestration/beats.py` with `Beat` / `BeatSheet` / `load_beats`, so the Sam→Bea handoff is a validated dataclass, not loose prose. `beats.json` is the machine artifact; `script.md` is the human-readable sibling — exactly Maya's `criteria.json` + `plan.md` split.

The build pattern is a known quantity. Both agents are `@register_node` AgentSpecs cloned from `planner.py`'s shape: `ClassVar` name/inputs/outputs, a `cost_estimate()` (both subscription-absorbed, $0 incremental), a multi-pass `run()`, persona context preambles in `pipeline/agents/prompts/`, CLI subcommands mirroring `plan.py`/`bible.py`, and a `scripts/author_*.py` driver mirroring `author_plan.py`. Stub fallback keeps the whole thing CI-green credential-free, like every agent before it. The costed validation (real Opus authoring a real script) is deferred — same discipline as the parked end-to-end run.

The one design choice worth flagging as *deliberate*, not copied: Maya's second pass is a Sonnet **adversarial** validation of the plan. Sam's second pass is **structural, not aesthetic** — because the eval handbook is explicit that LLM judges are weak and self-preferring on creative quality. Sam's pass 2 checks beat coverage, arc presence, cast consistency, sane beat count — never "is this good writing." Good writing is Sean's call at the gate. This keeps Sam honest about where the human's taste is load-bearing.

## 5. Anti-bias rotation — what each lens suppressed

- **The PM lens over-valued the loop-closer** and almost made Bea emit `shots.yaml` as the *primary* artifact, demoting the human-readable storyboard the Phase 3 spec actually names. Correction: both artifacts are first-class; the storyboard is the spec's output, the shots.yaml is the convenience that closes the loop.
- **The Designer lens wanted panels** — silhouettes, composition sketches, the works — because a storyboard "should" be visual. Correction (and Sean's call): text-only v1. The loop-closing use case needs structured text, not pictures; panels are a deferred pro tier with a real promotion trigger, not a v1 requirement. Resisting the visual reflex *is* resisting scope creep here.
- **The Engineer lens wanted one Phase 3 agent** with two passes (script-pass, board-pass) because the code would be tidier. Correction: the roster names two agents with two models (Opus vs Sonnet) and two different eval problems (pairwise-creative vs coverage-deterministic). They're built as siblings, sequenced, not fused — the model and eval split is the reason they're two names.
- **All three lenses under-weighted voice drift.** Sam writing in generic-screenplay voice is the quiet failure that makes the museum exhibit feel like every other AI-writes-the-movie demo. The full `writing-voice-modes` calibration lives in another repo; v1 embeds a condensed "Sean's register" note and flags the full calibration as a campaign promotion. Naming it here so it isn't lost.

---

## 6. Converged decisions (the four forks, locked 2026-06-12)

| # | Fork | Decision | Why |
|---|------|----------|-----|
| 1 | Sequencing | **Sam first, then Bea** | Sam's beat sheet is Bea's input — linear dependency. Sam is the lower-risk build (text-only, Opus, closest clone of Maya). Land Sam, lock the Sam→Bea contract via `beats.py`, then build Bea with its bake-off complexity. |
| 2 | Bea's output | **Draft `shots.yaml` + `storyboard.md`; human curates** | Closes the loop and is the strongest museum payoff. The shots.yaml is born unlocked, validated by the real `load_shots`, never auto-run. The storyboard.md remains the spec's named human-readable output. |
| 3 | Bea panels | **Text-only v1; panels deferred with trigger** | Structured shot text is exactly what `shots.yaml` needs; panels add an image route, per-panel cost, and a composition eval axis for no v1 benefit. Draft→pro panel generation is declared and deferred. |
| 4 | Eval scope | **Scaffold + a few real cases now; full eval in the campaign** | Land `evals/scriptwriter/` and `evals/storyboard_artist/` with `cases.yaml`, a handful of real hand-labeled cases (the Spark beats/shots are ready-made ground truth), and a runner stub. The pairwise-preference harness and Bea's Sonnet/Gemini/Codex bake-off ride the already-ticketed hardening campaign. |

## 7. The artifact contracts (the load-bearing detail)

**Sam emits:**

- `script.md` — studio-voice prose treatment + beat sheet, human-readable. The thing Sean reads at the gate.
- `beats.json` — the machine handoff to Bea, validated by `pipeline/orchestration/beats.py:load_beats`. Proposed shape:

  ```
  slug: "SS"
  logline: "Sean draws; the mascot notices and delights; everything settles back to the start."
  beats:
    - id: 1
      title: "The Spark"
      intent: "Establishing two-shot; Sean focused, mascot idle and unaware."
      emotional_beat: "calm focus"
      cast: ["sean", "claude-mascot"]      # ⊆ manifest IR namespaces
      feel: "establishing — let it breathe; the loop's compositional anchor"
      notes: "F05 returns here so the cycle reads continuous"
  ```

  `cast` flows beat → shot → `shots.yaml` cast unchanged. `id` is strictly ascending (chain order), mirroring `Shot.id`.

**Bea emits:**

- `storyboard.md` — human-readable beats→shots with intent + camera notes, in the shape of `docs/pencil-test-storyboard.md` (Act → Beat → Action → key poses → notes).
- `shots.yaml` (draft, unlocked) — conforms exactly to `load_shots`: `slug` + `frames[{id, cast, beat, prompt, extra_references, chain_anchors, hold}]`. Validated at emit time against the real schema with the manifest's known namespaces. A parse failure or coverage gap triggers one re-roll with the error threaded back into the prompt (Cy's reject-reason pattern).

**The gates:** `script approve` locks `beats.json`; `storyboard approve` is the curation gate where Sean's edited `shots.yaml` becomes the run input. Both idempotent, both mirroring Maya's plan gate and Cy's Bible lock. Nothing Sam or Bea emits is consumed downstream until a human approve flips the lock.

## 8. Deferred — not rejected (promotion triggers)

| Item | Owner | Promotion trigger |
|------|-------|-------------------|
| Full `writing-voice-modes` calibration (5-mode rotation) | Sam | A piece that needs a register distinct from Sean-default. v1 embeds a condensed register note. |
| Pairwise-preference eval harness (Sean win/lose/tie) | Sam | The hardening campaign. v1 ships structural beat-coverage checks + a few labeled cases. |
| Sonnet / Gemini / Codex three-way bake-off | Bea | The hardening campaign. Bea is the lowest-confidence assignment (65%), so a bake-off is *warranted* — but it's not blocking for a stub-green v1. |
| Draft silhouette panels (gemini pencil skill, draft tier) | Bea | Once the text shot list proves stable across ≥2 pieces. |
| Pro composition panels (full storyboard art) | Bea | A piece where composition is the differentiator, not a fixed-camera loop. |
| Camera-move vocabulary (pans, push-ins) | Bea | A Seedance Phase 6 motion-video piece. The Spark loop is fixed-camera keyframes, so v1 camera notes are framing-only. |
| Multi-act / longer-form beat structure | Sam | A piece longer than a single loop (e.g., Act 2 of the pencil test). |

## 9. What this brainstorm doesn't decide

- The exact `beats.json` field set is a *proposal* — the build session ratifies it against what Bea actually needs to write good shots. Treat §7 as a strong default, not a lock.
- Node id naming (`scriptwriter` / `storyboard_artist` to match the role-named registry, personas Sam/Bea) is a soft call carried into the build plan; `sam`/`bea` are acceptable if the build prefers persona-named ids.
- Whether Bea's re-roll budget is one or two attempts on validation failure — a build-time tuning call, defaulted to one.
- Anything about the parked items: the costed validation run and the fleet-wide hardening campaign stay parked. This session completes the *design*; it spends nothing.

---

*Next: the [Sam scriptwriter build plan](2026-06-12-sam-scriptwriter-build-plan.md) specs the first build in full and scopes Bea for a follow-on kickoff after Sam merges.*
