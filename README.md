# anima

**A 2D-animation pipeline made by a human and a fleet of AI agents working together.**

*Anima* — Latin for *breath*, for *soul*. Pipelines are usually named for what they do; this one is named for what it carries.

The premise is older than the tools: **the human owns timing, casting, and taste; the agents own everything that can be made cheap, parallel, and structured — and they *propose*, they don't decide.** The pipeline is where the two meet. A brief becomes a plan; the plan becomes an animatic; the animatic constrains motion; motion gets cleaned to the aesthetic; and everything that happened along the way is captured into a public walkthrough.

This repository is both the working system and the record of how it was built — including the post-mortems, the cost figures, and the things that didn't work the first time. That candor is deliberate. For an AI product manager, the evidence of rigor *is* the portfolio.

> **New here?** The fastest read of *what this is and why it's built this way* is [`PHILOSOPHY.md`](PHILOSOPHY.md) (the intent) and [`ROADMAP.md`](ROADMAP.md) (where it stands today, with an honest build scorecard). [`CLAUDE.md`](CLAUDE.md) is the deep internal manual.

---

## The thesis

Human creativity and AI creativity are different things, and pretending otherwise makes worse work.

So anima draws a hard line. The human is the director, the editor, the taste-keeper — blocking motion, casting characters, and making the call to ship. The agents are the crew — generating, varying, in-betweening, critiquing, capturing. This is not a tool that *uses* AI; it's a working method where a fleet of named agents are co-creators, taught the fundamentals, given the references, and trusted to brainstorm, plan, execute, and critique — with a human gate at every decision that matters.

Two beliefs shape every line of the architecture:

- **The animatic is non-negotiable.** A human blocks motion and placement in rough shapes *before* any model generates a frame. AI that generates motion with no human-authored constraint is the template trap — the one failure mode that would make this just another click-to-generate service.
- **A critic earns its keep when it proposes a fix, not when it flags a problem.** Every stage boundary runs a critic that says *try this instead*, not just *wrong*.

---

## The 10-phase pipeline

A free-text brief flows through ten phases. Expensive phases run a cheap **draft** tier first and escalate to **pro** only on human or critic approval; nothing burns compute before a human approves the plan.

| # | Phase | What happens | Gate |
|---|-------|--------------|------|
| 0 | **Brief & Plan** | A planner agent turns a markdown brief into a structured plan + a cost estimate | human approves |
| 1 | **Scaffold** | Project structure + manifest skeleton | — |
| 2 | **Character Bible** | Each character is a *folder* — anchor, turnarounds, expressions, costumes, props | — |
| 3 | **Storyboard** | A scriptwriter drafts the beats; a storyboard artist drafts the shots | human curates |
| 4 | **Animatic** | The human drops a placement-rough per keyframe — where characters stand, which way they face, scale, leg count — *before* a frame is drawn | human authors |
| 5 | **Generate** | Stills generated per shot, Bible-loaded, content-hash cached | T1 + T2 critics |
| 6 | **Motion** | Video interpolation between approved anchors, draft→pro | T2 critic |
| 7 | **Audit** | Consolidates critic findings, routes them to the retry ladder | — |
| 8 | **Assemble** | The cut is built; comparison artifacts render | T2 critic |
| 9 | **QA Review** | A creative-director rubric, then the final human look | human ships |

Running in parallel with all of it: the **Museum** — a capture layer that writes a structured artifact for every approval, reject, and retry, and renders a public walkthrough of how the piece was made.

The full spec lives in [`docs/architecture/pipeline-architecture-v1.md`](docs/architecture/pipeline-architecture-v1.md).

---

## The agent fleet

Seven named agents, one council, one orchestrator, one human. Each carries its own eval suite from day one.

| Agent | Role | Model |
|-------|------|-------|
| **Maya** | Planner — brief → plan + cost estimate | Opus 4.8 → Sonnet adversarial pass |
| **Cy** | Character designer — authors a character Bible (author → generate → verify) | Opus + Gemini NB2 |
| **Sam** | Scriptwriter — the beat sheet | Opus 4.8 |
| **Bea** | Storyboard artist — the shot list | Sonnet 4.6 |
| **Flo** | Frame router — picks the right model per shot type & tier | route table |
| **Em** | Vision critic — reviews each frame against the beat + style, proposes prompt fixes | Gemini 3.5 Flash → Opus escalation |
| **Mo** | Museum writer — narrates the captured exhibits into studio prose | Sonnet 4.6 |
| **T3 council** | Codie / Annie / Sage + a chairman — independent multi-model variance review at phase boundaries | Codex + Gemini + Opus |

---

## Engineering rigor (the part a PM cares about)

**A three-tier critic stack.** T1 is deterministic rule gates (aspect ratio, paper texture, continuity) — free, instant, every frame. T2 is a vision critic that reads output against the beat description and *proposes prompt diffs*. T3 is a heterogeneous multi-model council that runs at phase transitions, where independent eyes catch what a single judge can't.

**Empirical, not vibes.** Architecture decisions are eval-gated; model choices are settled by dated bake-offs, not preference. Eval suites are built error-analysis-first, with binary cases and deliberate class balance, and some cases ship *intentionally red* because the failure is the artifact worth tracking. The vision critic's suite went five ratified rounds deep on a contamination-guarded 52-case corpus — taking its verdict profile to precision 0.97 / recall 1.00 / false-pass 0.00 and its citation grounding from 0.03 to 0.97 — and that depth then became a lesson in *sequencing* (see the roadmap's honest scorecard).

**The pipeline is the portfolio.** Capture isn't bolted on after the fact; it's a first-class layer. Draft outputs aren't waste — they're evidence of iteration, and the walkthrough renders "we tried draft, here's what it showed, here's why we committed to pro." A compute-cost optimization becomes a narrative asset.

**Content-addressed caching.** Editing one prompt re-runs only its node and what's downstream — the DAG knows what changed.

---

## Where it actually stands

This repo doesn't pretend to be finished, and the honesty is the point. The 10-phase architecture is locked; the agents that fill it are at different maturities. [`ROADMAP.md`](ROADMAP.md) carries a full build scorecard grading every idea against the code — not against the optimism. As of this writing:

- The full agent fleet is **built and merged**; the run orchestrator chains Phase 0 → Generate → Assemble as one resumable program.
- The **Animatic phase** (the keystone) shipped a v1 placement seed, gated by a costed spike — its end-to-end costed run is the current focus.
- The **vision critic** is detection-strong but not yet calibrated to the human eye; closing that gap is the path to autonomous runs.
- The **Museum** capture layer and its exhibits exist; wiring capture *into* the run loop (vs. a post-run pass) is queued.

The candid record of how all of this was learned — field reports, cost figures, operational-incident write-ups, post-mortems — lives in [`docs/anima-test-runs/`](docs/anima-test-runs/) and the build journal under [`docs/COMPLETED/`](docs/COMPLETED/).

---

## Repo map

```
PHILOSOPHY.md          why anima exists, and what it refuses to become
ROADMAP.md             where the system is, with the build scorecard + anti-drift contract
CLAUDE.md              the deep internal manual (the fleet's operating instructions)
docs/
  architecture/        canonical specs & doctrine (read-first)
  active/              the current workstream + in-flight planning
  pencil-test/         the first reference implementation
  design/              canonical design inputs (agent voice, planner brainstorm, eval baseline)
  COMPLETED/           the build journal — historical session docs, by workstream
  anima-test-runs/     field reports, post-mortems, cost figures (the candid record)
  research/            external research notes
pipeline/              the code — run orchestrator, agents, critics, DAG, museum
characters/            the Character Bibles (sean-anchor, claude-mascot)
evals/                 each agent's eval suite (cases, fixtures, scored runners)
museum/                the committed exhibit tree
```

## The reference implementation

The first piece shipped through anima is **Pencil Test — Sean Winslow**, a hand-drawn-style portfolio loop. It's the proof that the system ships, not the definition of the project. The aesthetic target and the engine truth are one sentence:

> If the loop plays smoothly and the character is recognizably itself in its intended medium, it ships.

---

## Tech

Python pipeline (PyYAML, Pillow, google-genai, fal-client) + FFmpeg. Models: Claude (Opus 4.8 / Sonnet 4.6) via the Claude Agent SDK, Google Gemini (Nano Banana 2 image gen + Gemini 3.5 Flash vision), and Seedance 2.0 for motion. The test suite is hundreds of contract tests that stay green in CI without any API keys — agent runners fall back to deterministic stubs.

```bash
python -m pytest tests/            # contract suite
python -m pytest pipeline/tests/   # seedance select/cleanup (run separately)
```
