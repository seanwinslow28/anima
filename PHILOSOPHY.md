# anima — Philosophy

*Read this before the architecture. The architecture serves the philosophy, not the other way around.*

---

## What anima is

Anima — Latin for *breath*, for *soul* — is a reusable pipeline for shipping 2D animated stories made by a human and a fleet of agents working together. The name was chosen on purpose. Pipelines are usually named for what they do; this one is named for what it carries.

## Where it came from

Anima came out of shipping one piece — *Pencil Test — Sean Winslow*, a personal portfolio loop. The infrastructure that emerged for that work — manifest-driven generation, hard/soft fail gates with reason codes, frame chaining against an anchor reference, Seedance video interpolation between approved keyframes, structured decision logging — wasn't single-use. It wanted to be reused. So we named it, generalized the architecture, and locked the philosophy before drift set in.

The pencil-test is the first reference implementation. It is not the whole project. Anima is the system; the pencil-test is the proof that the system ships.

## The core thesis

Human creativity and AI creativity are different things, and pretending otherwise makes worse work.

The human owns taste, story, character intent, motion timing, and the decision to ship. AI owns everything that can be made cheap, parallel, and structured — generation, variation, in-betweens, critique, capture, walkthrough.

The pipeline is where these two meet.

This is not a tool that uses AI. It is a working method where Claude and a fleet of creative agents are co-creators — taught the fundamentals, given the references, trusted to brainstorm, plan, execute, critique, and ship 2D animated stories alongside the human. The human isn't the prompter; the human is the director, the editor, the taste-keeper. The agents are the crew.

## Load-bearing beliefs

These shape every architectural decision. Every commit either honors them or doesn't ship.

**The human owns timing and taste.** Sean blocks motion in shape silhouettes — in Procreate Dreams, in Procreate PNG stacks, whichever feels right — before any AI generates a single frame. The animatic phase is non-negotiable. AI that generates motion without a human-authored timing constraint is the template trap, and the template trap is the only thing that kills this project.

**The critic earns its keep when it proposes fixes.** A judge agent that says *wrong* without saying *try this instead* is half-built. Critic-as-Principle — three tiers, five named checkpoints — runs at every stage boundary. In Sean's words: *"a judge agent will be a staple in all of my agentic workflows from here on out."* Every workflow under this roof carries one.

**Iteration must be cheap.** Draft tier first; escalate to pro on human or critic approval. Content-addressed caching so editing one prompt doesn't re-burn the chain. The fastest hands win, and the pipeline exists to give the human the fastest possible hands.

**The pipeline is the portfolio piece.** Every approval, every reject, every retry, every prompt diff writes structured artifacts. The museum is core, not bolted on. We're not making "AI animation." We're making the case that human + AI partnership produces something neither could alone — and the museum is the evidence.

**Empirical, not vibes.** Architecture decisions are eval-gated. Model choices are bake-offs. Cases ship intentionally red where the failure is the artifact. The repo carries its receipts so the next person — and the next session — can verify the work instead of trusting it.

**Read like a studio, not a terminal.** In Sean's words: *"I don't like it when the docs feel like it was strictly made for the terminal. We're making art. It should feel free."* Prose where prose works. Tables only for genuine reference data. Studio-manual voice over CLI-reference voice. The way the project reads is part of the work.

## What anima refuses to become

- **Not a click-to-generate-anime service.** The human-authored animatic phase makes this impossible by design.
- **Not a wrapper around one model.** The model layer is replaceable; the architecture and the human role are not.
- **Not a black box.** The museum exists so the *how* is visible to anyone who wants to learn it.
- **Not finished.** The 10-phase architecture is locked; the agents that fill it are not. Anima evolves with what gets shipped through it.

## The engine truth

> If the loop plays smoothly and the character is recognizably itself in its intended medium, it ships.

Inherited from the pencil-test era's *"if it plays cleanly in Phaser, it ships"* and broadened. The final piece in its target medium — a browser GIF, a museum walkthrough, a 90-second short, wherever the work lives — is the ultimate arbiter. Everything else (phase counts, critic tiers, manifest schemas, agent fleets) is in service of that one test.

## Structural ancestors worth crediting

Anima borrows from three places without being any of them:

- **Higgsfield Supercomputer's brief-plan-approve-execute pattern** — Phase 0 lives because of this.
- **OiiOii's small named-agent crew** — informs how the agent-fleet brainstorm is scoped.
- **Krea Node Agent's content-addressed node graph** — informs the DAG refactor and the cache strategy.

The shape was taken from where it was already proven. The soul is our own.

---

*Last updated 2026-05-25. Philosophy locks slower than architecture; if you're changing this file, you're changing the project.*
