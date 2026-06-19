# Kickoff — brainstorm the next phase with Sean, then hand a plan to Claude Code

*Paste this whole document into a fresh Cowork session on the `anima` project. This is a **brainstorm + planning** session, not a build session. You are Sean's thinking partner: you generate breadth, pressure-test against anima's soul, converge with him on a design, and then write a plan + a Claude Code execution kickoff. The building happens in Claude Code afterward — never here.*

---

## The rhythm you're part of

anima ships work in a deliberate loop, and this session is the front half of it:

```
Cowork BRAINSTORM (this session)  →  a converged design + a plan + a Claude Code kickoff
        ↓
Claude Code EXECUTES under fleet-ops  →  builds it, $-aware, isolated worktree, TDD
        ↓
FIELD REPORT + verify  →  what changed, what broke, what we learned
        ↓
update ROADMAP.md (advance "Current focus")  →  return here for the NEXT phase
```

You own the first box. The discipline that makes this work — and the reason `ROADMAP.md` exists — is that **we finish one workstream before starting the next.** So this session brainstorms **exactly one phase: whatever `ROADMAP.md` names as the Current Focus.** Right now that is the **Animatic phase**. You do *not* pre-design the later two — the Animatic build will teach us things that change the Em and Museum brainstorms, so brainstorming them now would be wasted motion and exactly the drift we're trying to kill. (The three are sketched below so you see the arc; only the current one gets worked.)

The full sequence, locked by Sean: **Animatic → Em calibration → Museum.**

---

## First: read these, in this order

**Always, every time:**
1. [`ROADMAP.md`](../../ROADMAP.md) (repo root) — **the source of truth.** It tells you the Current Focus, that phase's open questions and candidate Definition of Done, and the anti-drift contract. Start here; let it tell you which phase you're brainstorming.
2. [`PHILOSOPHY.md`](../../PHILOSOPHY.md) — the six load-bearing beliefs. Every idea you generate gets pressure-tested against these. The animatic phase in particular is *named here as non-negotiable* ("the human owns timing and taste… AI that generates motion without a human-authored timing constraint is the template trap").
3. `CLAUDE.md` (auto-loaded) — the current fleet manual + the Skills Map (what each agent actually is) + the run orchestrator commands. Skim for the phase you're on.

**Then the context for the current phase** (the "Three phases at a glance" section below lists the specific files per phase). Read them. Verify claims against the tree, not the prose.

---

## How to brainstorm here

- **Invoke the brainstorming skill first.** This is creative/architectural design work — start with `superpowers:brainstorming` (explore intent, requirements, and design before any implementation), and lean on the PM/Designer/Engineer multi-perspective lens (`pm-product-discovery:brainstorm`) to generate breadth. Sean works in this headspace on purpose; honor it.
- **Be a thinking partner, not an order-taker.** Generate options before converging. Challenge weak ideas. Cross-pollinate from animation, game design, and PM. Then, once Sean commits, amplify and converge.
- **Pressure-test every idea against two questions:** (1) *Does this honor PHILOSOPHY's load-bearing beliefs* — especially "human owns timing and taste" and "the critic earns its keep by proposing fixes"? (2) *Is this Sean's pipeline, or a generic AI-animation template?* If an idea drifts toward click-to-generate, kill it.
- **Use `AskUserQuestion` for genuine forks** (format choices, mechanism choices, scope cuts). Keep it to the decisions that actually branch the design. Sean is a PM who digs into the "how" — give him the trade-offs, not just a recommendation.
- **Find the load-bearing assumption and name it.** Every phase has one technical bet the whole design rests on (called out per phase below). The plan you hand to Claude Code should de-risk it with the *cheapest possible test first* — usually a small costed spike — before committing the full build.
- **$0 in this session.** Brainstorming and planning cost nothing. Any costed validation (e.g., "does NB2 actually respect a placement seed?") belongs in the Claude Code plan, run under the fleet-ops protocol — not here. Do not run the orchestrator or call a model in this session.
- **Read like a studio, not a terminal** (PHILOSOPHY). The design doc and the kickoff you produce should feel authored, not generated.

---

## The three phases at a glance

Work only the Current Focus. The other two are here for arc, not action.

### ① Animatic phase (TOP-1) — the current focus

**Why now.** It's the single highest-priority idea in the original architecture brainstorm and the one major piece still unbuilt — and PHILOSOPHY calls it non-negotiable. The 2026-06-18 validation run *independently re-derived it*: NB2 can't reliably tell left from right, so character placement, the shoulder side, and the mascot's leg count drifted — and Sean's own diagnosis was *"start with my pre-drawn stick figure so NB2 knows exactly where the characters should be."* That is the animatic phase. The fleet was built around this keystone; now we build the keystone.

**Read for this phase:** `ROADMAP.md` (the Animatic row + open questions) · [`docs/pipeline-architecture-v1.md`](../architecture/pipeline-architecture-v1.md) §Phase 4 ANIMATIC + the `post_animatic` T3 gate · [`docs/2026-05-24-pipeline-v2-brainstorm.md`](../COMPLETED/pipeline-v2/2026-05-24-pipeline-v2-brainstorm.md) TOP-1 (esp. its "key assumptions to validate") · [`docs/2026-05-24-pipeline-v2-change-map.md`](../COMPLETED/pipeline-v2/2026-05-24-pipeline-v2-change-map.md) TOP-1 row (manifest `animatic:` block, `runs/{id}/animatic/` convention, the ingestion script) · [`docs/anima-test-runs/2026-06-18-tier1-validation-run-post-mortem.md`](../anima-test-runs/2026-06-18-tier1-validation-run-post-mortem.md) (the field evidence — the placement/leg/shoulder drift this phase fixes) · [`docs/research/2026-05-30-nb2-editing-character-consistency-template.md`](../research/2026-05-30-nb2-editing-character-consistency-template.md) (how reference images condition NB2 — the mechanism a rough frame would use; the reference-gap failure mode) · `pipeline/orchestration/generate_stage.py` + `shots.py` (`resolve_references` — exactly where a placement frame plugs into the reference stack).

**Open questions to crack with Sean:**
- **Format & authoring effort.** Procreate Dreams (video/frame export) vs Procreate PNG stacks vs dead-simple stick-figure/silhouette frames drawn anywhere. The original's #1 risk: *will Sean actually author these every time, or do they get skipped under deadline?* Pick the lightest thing he'll really do.
- **What the animatic is FOR.** A *placement/composition* seed (fixes the L/R/scale/leg problems this run hit — the urgent half for still-loops) or a *timing* seed (for Phase 6 motion later) or both. Be honest about which problem we're solving now.
- **The mechanism.** How does a rough frame condition NB2 — as an extra reference image fed to Flo (an image-to-image composition scaffold)? A pose/layout constraint? The run showed NB2 honors reference *images* on identity but guesses placement from *prose* — so feeding a rough composition frame as a reference is the natural lever. Where does it enter `resolve_references` (a new animatic ref slot? `extra_references`?), and does it ride on every frame or just the establishing anchor that the chain carries?
- **Pipeline placement.** Phase 4 between STORYBOARD and GENERATE; a new ANIMATIC stage in the orchestrator; an `animatic:` manifest block; the `runs/{id}/animatic/` convention; how it interacts with the curation gate and `shots.yaml`.
- **The `post_animatic` T3 gate** (declared-pending) — does it light up now, or stay deferred?

**The load-bearing assumption to pressure-test:** *a Sean-authored rough/blocked frame actually makes NB2 respect placement.* The plan must de-risk this with a cheap costed spike (a handful of Gemini calls in Claude Code under fleet-ops — feed a stick-figure placement frame as a reference, measure whether the shoulder/scale/leg problems from 2026-06-18 measurably improve) **before** committing the full ingestion build.

**Candidate Definition of Done** (refine with Sean): the orchestrator ingests a Sean-authored rough frame as a placement constraint into GENERATE; a spike proves NB2 respects it; the placement class of defects measurably drops; the `post_animatic` gate is wired or consciously deferred; ROADMAP updated.

### ② Em calibration (Tier 2) — next, not now

The autonomy core: Em's eye matching Sean's is the one thing between "human at every gate" and "step away." The data is already harvested — the Em-vs-eye label table in `2026-06-18-tier1-validation-run-post-mortem.md`. When this becomes the focus, the brainstorm cracks: detection-coverage vs severity-threshold (they're separate knobs); the L/R axis being unreliable for *both* generator and critic (does the Animatic seed reduce what Em must catch?); the `identity_critical`→Opus escalation gap; whether to wire propose→apply; and how to *measure* "Em ≈ Sean's eye." Hard guard: any Em change is eval-gated, and the verdict-baseline md5 only moves on a deliberate ratified re-baseline. **Do not work this until Animatic is built.**

### ③ Museum — last

Make "the pipeline is the portfolio" true. The capture machinery, Mo the docent, the schema, and the `pre_museum` T3 gate all exist — but capture doesn't fire during a run and the Astro publish into `sw-ai-pm-portfolio` is deferred. When this becomes the focus, the brainstorm cracks: wiring capture into the orchestrator's node-completion hooks, what gets captured, standalone vs portfolio publish, and whether "The Spark, Shared" becomes the first published walkthrough. **Do not work this until Em calibration is done.**

---

## What you produce this session (for the current phase only)

1. **A converged design doc** — the brainstorm's output: the decisions made, the options weighed and rejected, the load-bearing assumption and how the plan de-risks it. Studio voice. Save it under `docs/` dated.
2. **A Claude Code execution kickoff** — the self-contained handoff Claude Code receives to build the phase under the fleet-ops protocol (subscription billing, isolated worktree, TDD, $0-or-costed-spike-aware), ending in a field report + verification. Model its shape on the existing kickoffs ([`docs/2026-06-18-roadmap-kickoff.md`](2026-06-18-roadmap-kickoff.md) and the Tier-1 slice kickoffs in `docs/`): required reading, doctrine, the two md5 guards, scope guardrails, a definition of done. Include the costed spike as the first build step where the load-bearing assumption needs proving.
3. **A ROADMAP.md update** — reflect the converged design in the Animatic row and confirm it remains the Current Focus until Claude Code reports done.

## Doctrine (same as every anima session)

- **Verify against the tree, never trust a label** — including this kickoff and `ROADMAP.md`. If the code says something different from a doc, the code wins and you flag it.
- **Two standing guards must never move** (re-check if anything touches the tree): `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` md5 `2af75906502f1caf8857e18828ceb2e4`; `pipeline/agents/prompts/sean-screenwriting-voice.md` md5 `945af824fa53b948a18ac6bf206d67ef`.
- **No building, no spend, one phase.** Brainstorm and plan only. The costed spike and the build are Claude Code's job, downstream.

## Definition of done for this session

- The Current Focus phase (Animatic) has a converged design Sean signed off on, a Claude Code execution kickoff ready to paste, and an updated ROADMAP row.
- The later two phases are untouched. No code, no model spend, both md5 guards intact.
- Everything is presented to Sean for review before the handoff to Claude Code.

## Immediate first action

Read `ROADMAP.md` to confirm the Current Focus (expected: the Animatic phase), then `PHILOSOPHY.md`, then the Animatic context files above. Invoke `superpowers:brainstorming`. Open the brainstorm with Sean by laying out the phase's open questions and your first-pass take on each — then explore. Converge, pressure-test, and only then write the plan.

*Brainstorm wide, converge hard, hand off clean. One phase at a time.*
