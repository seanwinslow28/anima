# anima — Pipeline Architecture v1

**Status:** LOCKED 2026-05-25 · implementation in progress (commit 1 of 9)
**Supersedes:** the brainstorm + change-map dated 2026-05-24 are historical artifacts that *produced* this lock. This document is the canonical reference going forward.
**Addendum (2026-07-03):** the Brainstorm Front Door (①) shipped as a new capability upstream of Phase 0 — see [Brainstorm Front Door](#brainstorm-front-door-①--the-creative-entry-point-to-phase-0) below. It was built outside the original 9-commit sequence, as the first "outward turn" workstream after Tier-2 (Em calibration) closed.

A new session reading only this file should be able to act on the architecture without back-references. If something here turns out to be wrong, flag it — don't silently correct it. The architectural decisions below are locked.

---

## Philosophy

anima is a pipeline for 2D animation made by a human and a fleet of agents working together. The shape of the system rests on three load-bearing claims.

**The human owns timing, casting, and the museum's narrative voice.** The animatic in Phase 4 is the structural expression of this — it's where shape-block timing gets blocked by hand before a single dollar of model compute is spent. The human's job isn't to approve agent output; it's to make the choices that downstream agents are conditioned on. Approval gates exist, but the more important pattern is *human-as-source-of-constraint*.

**The agents own the cheap, parallelizable, structured work — and they propose, not decide.** The planner agent in Phase 0 proposes a plan. The vision critic in Phase 5 proposes prompt diffs. The CLI critics in Phase 4 and pre-publish surface variance, not verdicts. Every critic earns its keep by proposing fixes, not by flagging problems. Pass/fail is what T1 rule gates do, and T1 is the cheapest tier on purpose.

**The artifacts are durable; the model choices behind them are not.** The brief, the animatic, the Character Bible, the decision log, the museum walkthrough — these survive model swaps, vendor migrations, and price changes. Bake-offs under `evals/bakeoffs/` record *why* a particular model was in production at a particular time, and become first-class portfolio content in their own right. The pipeline's job is to keep the artifacts coherent while the underlying models churn.

The pipeline is where taste meets compute. The shape that follows is the simplest one that makes both halves of that visible.

---

## Brainstorm Front Door (①) — the creative entry point to Phase 0

**Status: BUILT.** All four slices shipped 2026-07-02 → 2026-07-03; the five-stage chain is complete and validated against two live runs (the piñata/GRANDMASTER dry-run — its own spec + eval fixture — and the ai-guru-pilot run).

**Purpose.** Phase 0 assumes `docs/brief.md` already exists. The front door is what produces one from nothing but a one-line spark — "what if we made X" — turning it into the exact bundle Phase 0 consumes: a museum-worthy `concept.md`, a Maya-ready `00_studio_brief.md`, `character_seeds.yaml` for Cy, and a `frontdoor.json` machine handoff. It is opt-in and strictly additive: a hand-written brief skips it entirely, and `python -m pipeline.run --brief <dir>` is the unchanged consumer either way.

**Architecture — a user-invoked orchestrator + two model-invoked skills, over a thin code seam.** Two layers, cleanly separated:

- **The skill layer** (`.claude/skills/`, human-facing, all markdown). [`brainstorm-front-door`](../../.claude/skills/brainstorm-front-door/SKILL.md) is the **user-invoked orchestrator** — it runs the room, owns every locked decision, and is the only thing that ever emits the final bundle. It reaches for two **model-invoked discipline skills**: `frontdoor-interrogate` (the relentless one-question-at-a-time grill, with a generic-answer detector that pushes toward named specifics, gated by the creative-director six-point North Star) and `frontdoor-synthesize` (writes the bundle from the running session sidecar — no new interviewing — self-checks it against an anti-pattern rubric, then calls the code seam to emit + validate).
- **The code seam** (`pipeline/frontdoor/`), pure Python, credential-free, TDD-tested: `brief.py` (the `StudioBrief` schema — 7 exact H2 headers order-enforced, with a required nested `### What this is NOT` sub-block — plus parse/render/validate), `handoff.py` (the `frontdoor.json` descriptor: `slug` / `characters` / `stage_provenance` + a `mode: interactive|fixture` marker so a test fixture can never masquerade as a live session), `emit.py` (writes the 5-file bundle plus `manifest_gap_report.md`), `validate.py` (structural checks + a `register_warnings()` soft flag — an unregistered nonempty `style_register` warns, never blocks, because the front door is where a new register is *discovered*), `cli.py` (`python -m pipeline.frontdoor validate <dir>`). The skills produce prose; the code only validates structure and emits the handoff — CI stays green without API keys, and interview *quality* is judged by the golden-fixture eval (piñata + ai-guru), never a unit test.

**The chain — five named stages, but three of them are inline orchestrator disciplines, not skills (a load-bearing reversal from the original plan).** The 2026-07-02 converged build plan specified five separate model-invoked skills (`frontdoor-expand`, `frontdoor-art-viz`, `frontdoor-stress-test`, alongside interrogate/synthesize) and five code modules. Live dry-runs proved that wrong — EXPAND, ART-VIZ, and STRESS-TEST all did their job *inside the room*, without ever stepping out to a sibling skill — and two rounds of Codex red-team agreed each time. What actually shipped:

1. **MICRO-EXPAND** (always-on, inline, every session). Before any interviewing: 3 alternate premises, 3 style-tone routes, 3 risk questions — then one question, "deepen, or proceed to interrogate?"
2. **The contested-axis workshop** (EXPAND, inline — no `frontdoor-expand` skill). Reached on "deepen," or whenever an axis turns contested mid-grill; the room never leaves itself. N≈3–5 mutually distinct options per axis, each a named specific with a stated tradeoff, converging on one recommendation. The original "≥8 avenues across ≥4 domains" volume metric is dead (gameable — eight semantic neighbors can hit the count and say nothing); a six-criterion live-review rubric replaced it.
3. **INTERROGATE** — the one stage that stayed a skill call (`frontdoor-interrogate`). Grills one question at a time until the North Star is nailed down.
4. **ART-VIZ** (Step 2.5, inline — no `frontdoor-art-viz` skill, no `genndy-tartakovsky` style skill built). One fixed hero frame, ≥3 mutually distinct Flow-ready route prompts rendering the *same composition* in different registers, so comparison stays apples-to-apples. **$0, prompt-only** — a live Higgsfield MCP render is deferred behind an explicit human-typed `SPEND OK: Higgsfield <model> <count> <max-credits>` phrase, never fired by a skill on its own. An un-buildable register is surfaced as an `open_question` against the closed style-register vocabulary ([`prompt-style-neutrality-doctrine.md`](prompt-style-neutrality-doctrine.md)), never silently extended.
5. **STRESS-TEST** (Step 2.75, inline reflex → fresh-context authority — no `frontdoor-stress-test` skill). A cheap in-room pre-mortem warm-up first, then a **fresh-context sub-agent** — reading only the draft `concept.md` + `00_studio_brief.md`, blind to the session sidecar's "love story" — runs the authoritative pass: Tiger / Paper-Tiger / Elephant triage (default to Tiger when unsure) + steelman-then-attack red-team, each surviving risk written as "Fails if ___" with its cheapest test. Recommends `proceed` (with named residuals) or `revise`; the orchestrator locks the verdict. **A production-binding residual** — one that changes buildability, budget, or constraints — must land in the Studio Brief itself (under `### What this is NOT` or the non-negotiables), never left in `concept.md` alone, because Maya/Sam/Bea only ever read the brief.
6. **SYNTHESIZE** — the second stage that stayed a skill call (`frontdoor-synthesize`). Writes the bundle from the locked decisions, self-checks against the anti-pattern rubric, and is the *only* stage that emits — always through the code seam.

The chain-wide invariant, held since Slice 1: a stage skill may return only four kinds of content — `observations`, `options`, `recommendation`, `open_questions`. Only the orchestrator writes locked-decision fields (`chosen_route`, `skip_stage`, `locked_style`, `stress_verdict`, `stage_provenance`), and a lock is append-only — no later stage can rewrite an earlier one. This is the same "critics propose, humans decide" pattern as the T1/T2/T3 stack, one level upstream of it — Sean is the one decider throughout.

**What was deliberately never built.** No `frontdoor-expand`, `frontdoor-art-viz`, or `frontdoor-stress-test` skill. No `seeds.py`, `spark.py`, `style_refs.py`, or `stress.py` modules — cut by red-team as schema theater before they were written. No `style_route` or `stress_verdict` field in `frontdoor.json` — nothing reads either one, so neither exists (style routes and the stress verdict are prose in `concept.md` plus a locked decision in the sidecar). `pipeline/frontdoor/` has stayed schema- and behavior-identical since Slice 1 across three subsequent slices of pure prose + rubric + a handful of characterization tests.

**Downstream boundary.** The front door's output is **Maya-ready, not GENERATE-ready**, for any new character it seeds. Cy still has to author a Bible (Cy's node requires a non-empty `source-refs/` directory before it will start) and the character has to be registered in the manifest before Phase 5 can touch it. `manifest_gap_report.md` names exactly which seed characters still need that work; the front door never mutates `manifest.yaml` itself. In production this boundary already did real work once: the GRANDMASTER dry-run's STRESS-TEST flagged a style-register gap as a Launch-Blocking Tiger, which surfaced in its Studio Brief and gated the character's Bible pass until the animation-vocabulary-expansion workstream authored the missing register — the honest-boundary behavior working exactly as designed, not a hypothetical.

**Provenance.** Design: [`docs/active/2026-06-29-brainstorm-front-door-design.md`](../active/2026-06-29-brainstorm-front-door-design.md). Build plan (Slice 1's *how*, superseded in shape by the Slice 2-4 inline reversal but kept as the *why*): [`docs/active/2026-07-02-frontdoor-build-plan-CONVERGED.md`](../active/2026-07-02-frontdoor-build-plan-CONVERGED.md). Per-slice converged specs: [Slice 2 EXPAND](../active/2026-07-02-frontdoor-slice2-expand-CONVERGED.md), [Slice 3 ART-VIZ](../active/2026-07-02-frontdoor-slice3-artviz-CONVERGED.md), [Slice 4 STRESS-TEST](../active/2026-07-03-frontdoor-slice4-stress-test-CONVERGED.md). Orchestrator skill: [`brainstorm-front-door/SKILL.md`](../../.claude/skills/brainstorm-front-door/SKILL.md).

---

## The 10 Phases

Phase numbering runs 0 through 9 plus an orthogonal Museum capture layer that runs in parallel with all other phases. Phases 1, 7, and 9 are cost-light or human-only and do not participate in draft → pro escalation. The remaining seven phases do.

### Phase 0 — BRIEF & PLAN

**Purpose.** Turn a free-text brief into a structured plan + cost estimate before any model call. Approval is a human gate; nothing burns compute until the plan is approved. This is anima's structural answer to the cost-surprise problem — the user signs off on intent and budget upfront, then argues with the plan rather than with the bill.

**Inputs.** `docs/brief.md` (free-form markdown — the user describes the project in prose, not a structured form), **or**, since 2026-07-03, the `concept.md` + `00_studio_brief.md` bundle emitted by the [Brainstorm Front Door (①)](#brainstorm-front-door-①--the-creative-entry-point-to-phase-0) skill chain — Maya reads `00_studio_brief.md` as free-text context either way; the front door is what a spark passes through before it becomes that file.

**Outputs.** `docs/plan.md` (structured): phase list, frame counts, character IDs to load, draft prompts, retry budget, estimated spend across NB2 + Seedance + Claude tokens. Optionally seeds the manifest.

**Draft tier.** Haiku planner, rough cost band.
**Pro tier.** Sonnet planner, fine cost estimate.

*Flagged (2026-07-07): this Haiku-draft/Sonnet-pro split was the plan at lock time; it is not what shipped. The planner agent (Maya) runs as Opus 4.8 primary authoring + a Sonnet 4.6 adversarial validation pass, not a model-tier swap — see CLAUDE.md's `planner — Maya` row for the current, actively-maintained description. Left as a flag rather than silently rewritten, per this doc's own convention.*

**Critic checkpoint.** None at phase exit — the human approval gate replaces it. The planner agent itself is the subject of an eval suite under `evals/planner/` from day one.

**Status.** **Built and shipping** (landed 2026-06-11 as the PLAN stage of the Slice-2 run orchestrator). CLI: `python -m pipeline.cli plan init/show/approve/mutate`; folded into `python -m pipeline.run --brief <dir>` as the first stage. Since 2026-07-03 it can also be fed by the [Brainstorm Front Door (①)](#brainstorm-front-door-①--the-creative-entry-point-to-phase-0)'s emitted brief bundle.

### Phase 1 — SCAFFOLD

**Purpose.** Lay down file structure, manifest skeleton, run directory layout. Pure file-system bookkeeping.

**Inputs.** Approved `plan.md`.

**Outputs.** Project skeleton: `manifest.yaml` seeded from plan, `runs/{run_id}/` directory tree, `characters/` and `museum/{project_slug}/` directories.

**Tiering.** n/a. No model compute.

**Status.** Trivial — wraps existing logic; lands with commit 4 (DAG runner).

### Phase 2 — CHARACTER BIBLE

**Purpose.** Make sure every character in the project has a usable identity reference before frame generation starts. Either references an existing Bible or authors a new one (Bible-authoring is itself a Project-Type — anima can produce Bibles, not just consume them).

**Inputs.** Character IDs from `plan.md`; existing `characters/{character_id}/` folders if present; user-provided source images if authoring.

**Outputs.** Validated `characters/{character_id}/` folders, one per character: anchor, turnarounds, expressions, costumes, props, `character.yaml`.

**Draft tier.** 2-3 anchor angles, no expression sheet — *"does this character work?"*
**Pro tier.** Full 8-angle turnaround + 8-12 expressions + costume variants + props — the reusable artifact.

**Critic checkpoint.** None at phase exit; identity drift is caught downstream at Phase 5's T2 critic against the Bible.

**Status.** Migration of `images/2D-Character-Sketch-Sean-v1.png` → `characters/sean-anchor/` lands in commit 2. Authoring workflow lands later.

### Phase 3 — STORYBOARD

**Purpose.** Lock the beat sheet and shot list. Mostly human-authored. Agents assist with prompt drafts and continuity checks; they don't pick beats.

**Inputs.** `plan.md`, Character Bible references.

**Outputs.** `docs/storyboard.md` or per-shot files: beat sheet, shot list, per-shot intent, camera notes.

**Draft tier.** Rough beat sketches (silhouettes).
**Pro tier.** Full storyboard panels — composition + camera.

**Critic checkpoint.** None at phase exit; storyboard coherence is the human's responsibility here.

**Status.** Existing pencil-test storyboard ([`pencil-test-storyboard.md`](../pencil-test/pencil-test-storyboard.md)) is the reference shape.

### Phase 4 — ANIMATIC

**Purpose.** Block motion and timing in simple shapes before any expensive generation. This is the load-bearing pre-production stage and anima's highest-differentiation move. Every other AI animation pipeline starts at prompt-to-image or prompt-to-video; the animatic stage is where the human's "I own timing" thesis becomes structural rather than decorative.

**Inputs.** Storyboard, beat timing.

**Outputs.** Shape-block animatic artifacts. Format is dual: **Procreate Dreams** when the artifact wants to be a video file; **Procreate PNG sequences** when it wants to be a stack of hand-drawn keys. The pipeline ingests either as a downstream motion-and-timing constraint.

**Draft tier.** Circles and silhouettes, timing block only.
**Pro tier.** Cleaner shape-block with intended-pose silhouettes.

Both tiers stay human-authored — the pipeline distinguishes tier for museum capture purposes, not for which one auto-runs.

**Critic checkpoint.** **T3 multi-CLI variance gate** at phase exit. Worth the compute to validate timing arc before $20+ of NB2 + Seedance burn downstream. If the timing arc didn't land in shapes, no amount of generation budget will save it.

**Status.** Pending — lands in commit 7.

### Phase 5 — GENERATE

**Purpose.** Produce the still keyframes that anchor the animation. DAG-orchestrated with content-hashed caching: editing one prompt re-runs that node and its downstream only, never the whole chain. Character Bibles load selectively per shot.

**Inputs.** Storyboard, Character Bible, per-frame prompts.

**Outputs.** `runs/{run_id}/approved/{PROJECT}_{ActID}_{FrameNumber}_{AssetType}.png` per approved frame; `runs/{run_id}/rejected/` for failures with reason codes; `runs/{run_id}/candidates/F{##}/attempt_{##}.png` preserving every attempt.

**Draft tier.** Single attempt, 1-reference stack.
**Pro tier.** Multi-attempt, 2-reference stack with frame chaining (the existing pencil-test pattern).

**Critic checkpoint.** **T1 + T2.** T1 is the existing HF/SF/CC rule gates ([`pipeline/audit.py`](../../pipeline/audit.py), [`pipeline/continuity_audit.py`](../../pipeline/continuity_audit.py)) — they catch aspect ratio, paper texture, identity drift, stylus continuity. T2 is a vision critic (Claude Sonnet or Gemini 3 Pro — TBD in agent-fleet session) that reviews each approved frame against beat description + style guide and **proposes prompt diffs** for borderline cases. T2 implementation pending.

**Status.** T1 implemented and shipping. T2 pending agent-fleet session. DAG refactor lands in commit 4.

### Phase 6 — MOTION

**Purpose.** Generate fluid motion video between approved anchor stills. Seedance finds the motion; downstream NB2 cleanup protects the aesthetic. This is the existing two-engine philosophy promoted to a named phase.

**Inputs.** Approved anchor stills (start frame + end frame), Seedance prompts from [`prompts/seedance-template-v4.md`](../../prompts/seedance-template-v4.md).

**Outputs.** Per-shot MP4s in `runs/{run_id}/seedance/`; extracted frames at 12fps; optional NB2 cleanup pass.

**Draft tier.** Seedance Fast tier, 480p — production default.
**Pro tier.** Seedance Pro (Standard) tier, 720p with end-frame anchor — reserved for shots that need it.

The Fast→Pro distinction is locked from the 9-variant bake-off recorded in CHANGELOG 2026-05-10 — Fast won at half the cost. This is the prototype for the pipeline-wide draft → pro pattern.

**Critic checkpoint.** **T2 vision critic** at phase exit — currently an existing gap. Seedance output isn't QA'd beyond visual review today; T2 flags arc fidelity, timing, and identity drift in video output. Implementation pending agent-fleet session.

**Status.** Generation shipping ([`pipeline/seedance_*.py`](../../pipeline)). T2 critic pending.

### Phase 7 — AUDIT

**Purpose.** **Consolidation**, not critique. Routes findings from the T1/T2/T3 critics at Phases 4-6 to the retry ladder. This is the role-change: in the pencil-test era, Audit was *where critique happened*. In anima, critique is distributed across phases, and Phase 7 is where the findings get gathered, deduplicated, prioritized, and assigned to retries or to the human for manual decision.

**Inputs.** Critic outputs from Phases 4-6 (rule gate logs, vision critic notes, multi-CLI variance reports).

**Outputs.** `runs/{run_id}/audit/run_summary.json`, retry queue, human-review escalation queue.

**Tiering.** n/a. Consolidation only.

**Critic checkpoint.** None.

**Status.** Existing `audit.py` covers T1 consolidation; T2/T3 integration lands as those critics ship.

### Phase 8 — ASSEMBLE

**Purpose.** Build the final cut. FFmpeg renders the frame sequence to MP4, WebM, and GIF; comparison GIFs render automatically where a manual reference exists; museum capture hooks fire as nodes complete.

**Inputs.** Approved frames + Seedance shots from Phases 5-6.

**Outputs.** `runs/{run_id}/export/*.mp4`, `*.webm`, `*.gif`; comparison GIFs where applicable; museum capture artifacts.

**Draft tier.** Low-fps preview cut, no GIF palette optimization — enables fast playback review.
**Pro tier.** Full export: MP4 archival + WebM web + GIF with two-pass palette and <5MB target.

**Critic checkpoint.** **T2 vision critic** at phase exit — reads loop coherence and pacing across the whole cut, not just per-frame quality.

**Status.** Existing `assemble.sh` covers draft + pro export. T2 pending. Comparison GIF rendering + museum capture hooks land with commit 6.

### Phase 9 — QA REVIEW

**Purpose.** Final human gate, structured against the `creative-director` skill's critique rubric (Identity / Style / Composition / Continuity / Technical).

**Inputs.** Final cut from Phase 8.

**Outputs.** Ship decision + revision notes.

**Tiering.** n/a. Single human pass.

**Critic checkpoint.** None — the human *is* the critic here.

**Status.** Existing `creative-director` skill shipping.

### Museum (orthogonal capture layer)

**Purpose.** Capture the production process as durable, public-ready artifacts. Not a phase — runs in parallel with all other phases, hooked into DAG node-completion events. The thesis: portfolio content is a free byproduct of production, not a downstream write-up.

**Inputs.** Every approve / reject / retry decision; every node's prompt + reference + output + rationale; manual shape-block references where they exist (for comparison GIFs).

**Outputs.** `museum/{project_slug}/` tree of structured markdown + assets; rendered static site at the end of each run.

**Publishing target.** Astro content collection in [`sw-ai-pm-portfolio`](https://github.com/seanwinslow28/sw-ai-pm-portfolio). MDX matches the portfolio's content-collection schema. Standalone site only if anima outgrows the portfolio.

**Signature artifact format.** Comparison GIFs — manual shape-block on left, AI output on right, synced via FFmpeg. The single artifact that most clearly shows what the human did and what the agents did.

**Critic checkpoint.** **T3 multi-CLI variance gate** before publish. The museum doc is public-facing; multi-CLI variance gives the strongest read on whether narrative + comparison artifacts hold up under independent eyes.

**Status.** Pending — capture hooks land with commit 6 (depends on DAG refactor for clean hook points).

---

## Critic Stack (Full)

The critic earns its keep when it proposes fixes, not when it flags problems. Three tiers, escalating in cost and signal:

| Tier | What it is | Who runs it | What it produces | Cost / latency |
|------|------------|-------------|------------------|----------------|
| **T1** | Rule gates — HF/SF/CC reason codes, PIL dimension checks. Deterministic, instant. | `pipeline/audit.py` + `pipeline/continuity_audit.py` (shipping) | Pass/fail per rule + retry strategy from manifest's retry ladder | $0, <100ms per frame |
| **T2** | Vision critic — Claude Sonnet or Gemini 3 Pro (TBD bake-off) reviews output against beat description + style guide + storyboard intent. **Proposes specific prompt diffs**, not pass/fail. | Pending agent-fleet session — likely `pipeline/critics/vision_critic.py` | Structured critique notes + proposed prompt diff + confidence | ~$0.01–0.05 per call, 5–15s |
| **T3** | Multi-CLI variance council — three heterogeneous peers (Codie/`codex exec`, Annie/Gemini API, Sage/Opus-SDK) fan out in parallel + a separate Opus chairman adjudicates. The vault-critic pattern: $0 incremental on the Codex/Claude subscriptions, bounded Gemini for Annie. | **BUILT (Session B, 2026-06-10):** `pipeline/agents/t3_council.py` (`T3CouncilNode`) + `pipeline/museum/t3_gate.py` (the `pre_museum` gate) | Per-peer verdicts + agreement score + chairman adjudication note + staged patches (`auto_apply: false`) | $0 incremental + ~pennies Gemini, ~58–86s per artifact |

### The Five Named Checkpoints

| Checkpoint | Phase transition | Tier | What it gates |
|------------|------------------|------|---------------|
| post-Animatic | 4 → 5 | T3 | Timing arc validated before downstream compute burn |
| per-frame Generate | within 5 | T1 + T2 | Rule failures + beat fidelity per frame; T2 proposes prompt diffs |
| post-Motion | 6 → 7 | T2 | Motion arc, timing, identity drift in video output (currently an existing gap) |
| post-Assemble | 8 → 9 | T2 | Loop coherence + pacing across the whole cut |
| pre-Museum publish | parallel | T3 | Narrative + comparison artifacts hold up to independent eyes |

T1 is implemented and shipping. T2 (Em) shipped and is fully measured (verdict + citation + fix-rate axes). **T3 is BUILT + live-validated (Session B, 2026-06-10)** and wired at the **pre-Museum publish** checkpoint (`build_museum.py --t3-gate`; chairman `fail` blocks `--render`, `borderline` proceeds, patches stage). The **post-Animatic** T3 checkpoint stays a **declared seam** — Phase 4 Animatic is not built yet, so its gate is placement-locked + ticketed, not wired (don't build a gate for a phase that doesn't exist). The `critics.t3` config block lives in `manifest.yaml`; the live-smoke evidence is at [`docs/anima-test-runs/2026-06-10-t3-council-live-smoke.md`](../anima-test-runs/2026-06-10-t3-council-live-smoke.md).

Phase 7 Audit's role has changed from the pencil-test era. It is no longer *where critique happens*; it is where critique findings from distributed critics are *consolidated and routed* to the retry ladder.

---

## Draft → Pro Coverage by Phase

Every expensive node declares a draft tier and a pro tier. Default behavior: run draft, present preview, escalate to pro on approval (human-routed or critic-passed). The Seedance Fast→Pro pattern is the validated prototype; anima generalizes it.

| Phase | Draft tier | Pro tier | Notes |
|-------|------------|----------|-------|
| 0 BRIEF & PLAN | Haiku planner, rough cost band | Sonnet planner, fine cost estimate | Plan-time-only sketch; shipped instead as Opus 4.8 authoring + Sonnet 4.6 adversarial validation (see Phase 0 above, flagged) |
| 1 SCAFFOLD | n/a | n/a | File structure, no compute |
| 2 CHARACTER BIBLE | 2-3 anchor angles, no expression sheet | Full 8-angle turnaround + 8-12 expressions + costume variants | Draft answers "does this character work?"; pro is the reusable artifact |
| 3 STORYBOARD | Rough beat sketches (silhouettes) | Full storyboard panels (composition + camera) | Human often hand-authors draft; agent fills pro |
| 4 ANIMATIC | Circles/silhouettes timing block | Cleaner shape-block with intended-pose silhouettes | Both stay human-authored; pipeline distinguishes tier for museum capture |
| 5 GENERATE | Single attempt, 1-reference stack | Multi-attempt, 2-reference stack with frame chaining | Maps to existing retry ladder; draft = lite first attempt |
| 6 MOTION | Seedance Fast, 480p | Seedance Pro, 720p+ end-frame anchor | Already implemented — the prototype |
| 7 AUDIT | n/a | n/a | Consolidation phase, no escalation |
| 8 ASSEMBLE | Low-fps preview cut, no GIF palette opt | Full export (MP4 + WebM + optimized GIF) | Draft enables fast playback review |
| 9 QA REVIEW | n/a | n/a | Single human pass |

**Seven of ten phases have meaningful draft ↔ pro distinction.** Cost-light or human-only phases opt out.

The principle pairs with museum capture: draft outputs aren't waste, they're evidence of iteration. The museum walkthrough renders "we tried draft, here's what it showed, here's why we committed to pro" — turning a compute-cost optimization into a narrative asset.

There's also a symmetry worth naming: the critic stack itself is a draft → pro structure applied to *critique*. T1 = trivial draft (rules), T2 = draft critique (single vision model), T3 = pro critique (multi-CLI variance). Same iteration-speed logic, same architectural metaphor. Draft → pro escalation is the pattern; both the generation stack and the critic stack are expressions of it.

---

## The Character Bible Primitive

The single-anchor pattern (`images/2D-Character-Sketch-Sean-v1.png`) is gone. A character is now a folder:

```
characters/{character_id}/
├── character.yaml        # canonical palette, proportion rules, identity-drift triggers (SF02 conditions)
├── anchor.png            # primary identity reference (the old A-2 role)
├── turnarounds/
│   ├── front.png
│   ├── three-quarter.png
│   ├── profile.png
│   └── back.png
├── expressions/          # 8–12 emotional states (neutral, smile, surprised, focused, frustrated, etc.)
│   ├── neutral.png
│   ├── smile.png
│   └── ...
├── costumes/             # outfit variants
│   ├── default/          # mirrors the anchor's outfit
│   └── {variant}/
└── props/                # key prop attachments
    └── stylus.png
```

`character.yaml` shape (sketch — final schema lands with commit 2):

```yaml
id: sean-anchor
name: "Sean (Pencil Test character)"
palette:
  skin: "warm skin tones"
  hair: "muted sandy blonde"
  shirt: "dark navy"
  pants: "cool gray"
proportions:
  head_to_body: "1:7"
  notes: "lean build, broad shoulders"
identity_drift_triggers:
  - "hair shape varies from anchor"
  - "jaw angle different from anchor"
  - "eye spacing inconsistent with anchor"
props:
  stylus:
    hand: right
    presence: always
```

The manifest references characters by ID (`character_id: sean-anchor` per shot). The generator auto-loads relevant sheets per call — anchor + nearest-pose turnaround + matching expression — instead of hard-coding the reference paths in every prompt.

**Authoring-first.** Bible authoring is itself a Project-Type. The same pipeline that consumes a Bible can produce one, following the same brainstorm → propose → approve workflow the v2 architecture was built with. Multi-character shorts and character-design extensions (turnarounds, expression variations, costume swaps) both run as Bible-authoring projects before they run as animation projects.

The migration of the pencil-test anchor lands in commit 2 — `images/2D-Character-Sketch-Sean-v1.png` becomes `characters/sean-anchor/anchor.png`. The old path stays as a symlink for backward compatibility through commits 2-4.

---

## Open Questions Reserved for Future Sessions

These are deliberately not decided in commit 1. They unblock as their respective sessions land.

**Agent-fleet session (gates commits 8-9).** T2 vision critic model choice — Claude Sonnet vs Gemini 3 Pro, decided by a dated bake-off under `evals/bakeoffs/`. T3 Codex + Anti-Gravity wiring topology — how the parallel critique runs, how outputs reconcile, whether shared standing-context preambles work the way they do in code-brain's vault-critic. Planner agent shape — prompt template, few-shot examples from the pencil-test manifest, cost-estimation accuracy targets. Named roles inspired by OiiOii's 7-agent crew — director, casting, blocking, lighting, etc. — mapped to anima's actual phase needs rather than copied wholesale.

**Multimodal vault/RAG session (later — feeds future commits).** Embedding model choice — Gemini Embedding 2 vs OpenRouter alternatives, with cost and latency targets. Obsidian integration for the human-side knowledge base. Content-addressed asset store (ENG-5 in the brainstorm) — `{sha256}.png` + `{sha256}.json` sidecar shape, with parent-asset tracing and critic-note attachment.

**Museum showcase format session (later).** MDX schema matching `sw-ai-pm-portfolio`'s content collection. Comparison-GIF rendering pipeline (FFmpeg recipe + frame-alignment strategy). Decision-ledger surfacing in walkthrough docs — how much of the rejected-and-retried history shows publicly vs stays in the run dir.

**Public GitHub repo creation + directory rename.** Directory rename `sw-portfolio-animation-pipeline/` → `anima/` shipped 2026-05-29 via a single `mv` (git history preserved), and the GitHub repo was renamed `sw-portfolio-2D-animation` → `anima` in the same pass. Making the repo *public* is the remaining future step; not blocking on any other work.

---

## Pencil Test — First Reference Implementation

The pencil-test work is anima's first reference implementation, not anima's definition. Treating it as the reference rather than the spec lets anima generalize without invalidating the work-in-flight.

What generalizes from Pencil Test:
- The retry ladder (HF/SF/CC reason codes + attempt escalation) generalizes as the T1 critic across all projects.
- The Seedance Fast→Pro pattern generalizes as the draft → pro principle across all expensive phases.
- The frame chaining + reference stacking pattern in `generate.py` becomes the Character Bible loading logic in commit 2.
- The single-source `manifest.yaml` shape generalizes by becoming additive (existing blocks for pencil-test, new optional blocks for the v2 schema).
- The decision-log discipline in `CHANGELOG.md` is exactly the museum capture layer's source material.

What stays specific to Pencil Test:
- The `PT_{ActID}_{FrameNumber}_{AssetType}` asset naming pattern is the pencil-test prefix; future projects use their own.
- The Act 1 / Act 2 storyboard, beat sheet, and shot list are project artifacts, not architectural ones.
- The pencil-test aesthetic block in `manifest.yaml` (`style:`) is one possible aesthetic, not the only one.
- The cream paper / graphite line / hole-punch marks are a single character's costume, not the system's costume.

Current Pencil Test status: Act 1 hero loop has shipped. Act 2 is in active Seedance generation (10 clips + 4 holds, ~50s runtime), tracked in [`docs/production-checklist.md`](production-checklist.md) and [`docs/act2-seedance-shot-list.md`](../pencil-test/act2-seedance-shot-list.md). All Act 2 work in flight uses the pre-v2 manifest blocks and is not disturbed by commit 1.
