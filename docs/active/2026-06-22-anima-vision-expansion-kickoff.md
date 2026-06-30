# Kickoff — anima vision-expansion brainstorm: three new directions → the roadmap

*Paste this whole document into a fresh Cowork session on the `anima` project. This is a **strategic vision + roadmap-expansion brainstorm**, not a build session. You are Sean's thinking partner: scope three new directions he wants for the project, pressure-test what's achievable, sequence them honestly against the existing roadmap, and fold them in — without breaking the anti-drift discipline or abandoning the internals work in flight. No building. No model spend beyond cheap research math.*

---

## The inflection point

For months anima has been built **inward** — the 10-phase pipeline, the agent fleet, the critic stack, the evals. That work continues (Tier-2 Em calibration is mid-flight; see ROADMAP). But Sean has started thinking about where the project actually *goes*: not just "a pipeline that ships one short," but **a creative tool he uses to make animated shorts and films with an AI crew.** This session is about that outward turn — features, UX, and the economics underneath — and getting it onto the map so it's intentional, not a rabbit hole.

Three directions, in Sean's words:

1. **A brainstorming session as a kickoff option** — a long, rich back-and-forth that turns a spark into a fully-fleshed concept doc, which then feeds the orchestrated pipeline. A mix of Matt Pocock's *Grill Me* skill + the PM skills + the SW creative skills + the local `creative-director` skill, optionally generating sample art so Sean can *see* the style before committing compute. One big `anima-brainstorming` skill, or a pipeline of skills — to be worked out.
2. **A real interface — a Google-Flow-like visual app** — pages per stage (characters, scenes, storyboard, generate, motion) that end on a simple editing timeline to string clips together, preview, and export. Chat window + buttons instead of the terminal. Inspired by **Open Design** (the open-source Claude-Design response: plug in your own API keys, use whatever coding agent you prefer, same interface) — which is essentially what anima already does across its model fleet.
3. **The economics of generation** — the best and most cost-saving way to actually generate the images and videos. Higgsfield (added to the repo, great but expensive) vs Fal.ai vs the Gemini/OpenAI APIs; whether there's a cheaper/broader CLI or MCP for top image+video models; the real per-asset math.

## The discipline that still holds (read this before you get excited)

anima has one sacred rule, and this session must honor it: **the project does not open a new build workstream until the current one's Definition of Done is met** (ROADMAP, the anti-drift contract). Tier-2 Em calibration is the active focus; Slice 1 (the mascot eval corpus) is ingested and waiting on a costed baseline.

So this session's job is **NOT to start building any of the three.** It is to: scope them, decide what's achievable, find the dependencies and synergies, and **sequence them onto the roadmap** — where each slots relative to Tier-2 and the remaining internals. Sean is the director; he can re-prioritize. But the output is a *plan and a sequence*, not code. Naming a big vision is how you make room for it without drifting into it.

## First, read

1. **`ROADMAP.md`** — where the system is, the single active workstream, the anti-drift contract, the "road ahead" + parked sections (this is where the three new directions will land).
2. **`PHILOSOPHY.md`** — the load-bearing beliefs. Pressure-test every idea against them. Two are directly in play: *"the pipeline is the portfolio piece"* (a real UI makes that literal and demoable — and Sean is on a PM job hunt) and *"read like a studio, not a terminal"* (the whole point of direction 2).
3. **`CLAUDE.md`** — the current fleet manual; skim for what already exists that each direction can stand on.
4. Per-direction grounding is listed inline below.

## The three directions — scope, what exists, and a first-pass take

Work them **one at a time** (don't boil the ocean in one message). For each, the pattern that worked all session: lay out the open questions with a first-pass take, then explore with `AskUserQuestion` on the genuine forks.

### ① Brainstorm-as-kickoff — the creative front door *(most tractable; likely highest near-term leverage)*

**The vision.** A relentless, structured elicitation that produces a fleshed-out **concept doc** — which becomes the pipeline's brief (the Phase 0 input Maya already consumes). Optionally it generates sample frames mid-session so Sean locks the *look* before any costed run.

**What already exists to stand on:** the pipeline already *starts* from a brief → Maya, so there's a clean insertion point (a "Phase 0− / Concept" front door, exactly the "kickoff option" Sean asked for). Local assets: `creative-director` skill (`.claude/skills/creative-director/`, art direction + critique); the **PM plugins** (`pm-product-discovery:brainstorm`/`discover`, `pm-product-strategy`, `pm-market-research`); **`sw-creative-toolkit`** (brainstorm / design-thinking / storytelling / problem-solving / innovation-strategy); the screenwriting/`writing-voice-modes` skills; and the image-gen skills (`gemini-image-gen`, `gemini-pencil-animation-image-gen`) plus Sean's **free NB2-via-Flow** path for $0 art viz.

**Grill Me (the engine):** `mattpocock/skills` — `/grill-me` is *"get relentlessly interviewed about a plan or design until every branch of the decision tree is resolved,"* with `/grilling` as the reusable loop and `/to-prd` to *"turn the conversation into a structured doc."* That interrogation→document spine is the backbone; the PM/creative/creative-director skills supply the *creative* substance (story, character, art direction) the engineering-flavored Grill Me doesn't. Study the repo's structure (small, composable, user-invoked-orchestrates / model-invoked-discipline) — it's a model for how to build this.

**Open questions / forks to crack:** (a) **one mega-skill vs an orchestrated chain** — the fleet already chains skills/agents, and Matt's own doctrine favors small composable skills, so a *chain* may be more anima-native; decide. (b) **The output contract** — what exactly does it emit that the pipeline consumes (a studio brief + concept doc + a set of locked art-style references)? (c) **The art-viz loop** — generate sample frames during the session so Sean sees the look ($0 via Flow / cheap via NB2); how tight is that loop? (d) **Where it sits** — a new kickoff option feeding Phase 0, vs a standalone pre-pipeline skill.

**First-pass achievability: HIGH.** Mostly skill authoring + chaining + a clean hand-off into the existing brief; the art-viz loop is cheap. Strong candidate to build relatively soon and somewhat in parallel with the internals (it doesn't touch the Em calibration).

### ② The Flow-like interface — the long-game centerpiece *(biggest build; phase it)*

**The vision.** A visual app: a project gallery, a page per stage (character builder, scene/storyboard board, generate, motion), a chat window + buttons replacing the terminal, ending on a **simple timeline** to arrange clips, make basic cuts, preview, and export. Then Sean takes the export into real editing (effects, music). Layout/UX inspired by **Google Flow** (`labs.google/fx/tools/flow` — Sean will provide screenshots) and **Open Design** (`github.com/nexu-io/open-design` — the BYO-key, BYO-agent, Claude-Design-like shell).

**The key insight that makes it feasible:** anima is **already a structured, resumable state machine** — `pipeline/run.py`, `run_state.json`, the gates (plan / script / storyboard / animatic / per-frame approvals). A UI is a **face over the existing orchestrator**, not a rewrite. The gates become screens; the chat drives the agents; the run state is the data model. The `frontend-design` and `impeccable` skills are available for the build.

**Open questions / forks:** (a) **Scope + phasing** — this is the largest effort; a sane phase order is v1 a project dashboard + gate screens + a chat shell over the orchestrator (kills the terminal), v2 the per-stage visual pages, v3 the timeline. (b) **The timeline reach** (Sean asked directly) — honest first read: a *simple* arrange-trim-preview-export timeline is achievable as a later phase; a full NLE is not, and Sean doesn't want it (he exports to real editing). So *simple timeline = yes, phased; full editor = no, by design.* (c) **The foundational work** — a web UI over a Python *CLI* needs an **API/server wrapper around the orchestrator**; that server layer is the real prerequisite and could start early even if the UI comes later. (d) **Extensive UX research** — Flow's layout, Open Design's architecture (Sean provides screenshots; this is a research-heavy direction). (e) **The portfolio multiplier** — a slick anima UI is PM-job-hunt gold; it makes "the pipeline is the portfolio" literal and demoable.

**First-pass achievability: MEDIUM, phased.** Highest value, biggest effort; wants the internals reasonably settled (it's a face over them) but its *foundation* (orchestrator-as-API) is a clean early slice. The centerpiece of the long game.

### ③ The economics of generation — research + math + a decision *(most bounded; lowest usage; do soon)*

**The vision.** Decide the best, most cost-saving way to generate the pipeline's images and videos. Higgsfield (added — `.claude/skills/higgsfield-*`, the `2026-06-22-higgsfield-seedance-generation-runbook.md`; great but expensive) vs **Fal.ai** vs the **Gemini/OpenAI** APIs; whether a cheaper/broader **CLI or MCP** exists for top models; the per-asset math.

**What already exists:** transports in use — NB2/Gemini for images (~$0.07, and **$0 via Sean's Flow subscription** for manual gen), fal Seedance for video (in-pipeline Motion), the Higgsfield CLI (manual/exploratory). The **Flo-B pilot** already compared fal Seedream/Qwen vs NB2 for in-betweens (NB2 won Sean's eye). Existing research to build on: `docs/research/2026-06-19-seedance-2.0-access-cost-comparison.md`, `deep-research-prompts-image-models(-v2).md`, `seedance-research-findings.md`. The **self-hosted FLUX + sketch-LoRA** path is already ticketed as the $0-ongoing future.

**Open questions / forks:** (a) **The cost table** — per-image and per-second-of-video across Higgsfield / Fal.ai / Gemini / OpenAI / Replicate, at *current* prices (live research — prices move). (b) **The free-subscription angle** — Sean gets free NB2 via Flow; does Flow (or another subscription) cover *video* cheaply too? (c) **Quality vs cost** — the pipeline cares about identity/style consistency (NB2 won images; video needs Seedance/Higgsfield-class). (d) **A unified cheaper CLI/MCP** — does a "Higgsfield-but-cheaper/broader" exist (fal's API/CLI, Replicate, others)? (e) **The deliverable** — a recommended transport-per-stage cost/quality decision table. The `deep-research` skill is the right tool here.

**First-pass achievability: HIGH, ~$0.** Research + math + a decision; directly serves Sean's cost/usage concern. The most immediately actionable, and low-usage — a strong candidate to start soon and in parallel (it competes with nothing).

## The synthesis to surface

These three aren't separate features — they're **one product arc.** The brainstorm-skill (①) is the front door; the interface (②) is the shell around the whole pipeline *including* that front door; the cost research (③) decides what powers it underneath. Named together: *anima becomes a Flow-like creative tool where you brainstorm a concept with an agent crew, the orchestrated pipeline builds it, a simple timeline strings it together, and cost-optimized transports run it.* Part of this session's value is helping Sean **see that coherent arc** and decide how fast to walk it.

**A sequencing straw-man to react to (not a decree):** Tier-2 stays the active *internals* focus. ③ (cost research, low-usage, bounded) can start soon, in parallel. ① (brainstorm front-door, tractable, independent of Em) is the strong near-term build candidate. ②'s *foundation* (orchestrator-as-API) is an early slice; its *full UI + timeline* is the long game once internals settle. Sean rules on the actual order.

## How to run the session

- **Invoke `superpowers:brainstorming` first**, and lean on the PM/Designer/Engineer multi-perspective lens. This is breadth-then-converge work.
- **One direction at a time.** Lay out each direction's open questions with your first-pass take, then `AskUserQuestion` on the genuine forks (scope cuts, skill-vs-chain, timeline reach, build order). Converge before moving on.
- **Research as needed, cheaply.** Direction ③ wants live pricing (use `deep-research` / web search + math). Direction ② wants UX research (Flow + Open Design; ask Sean for the screenshots he offered). Direction ① wants you to actually read the Grill Me + creative-director + relevant PM/SW-creative SKILL.md files. None of this needs costed model runs.
- **Pressure-test against PHILOSOPHY and the anti-drift contract** every time. The killer question: *is this the right evolution of anima, or the rabbit hole the roadmap exists to prevent?* Both can be true of the same idea depending on **when** it's built — so sequence, don't just approve.

## What you produce

1. **A scoped design note per direction** (saved under `docs/`, dated) — the vision, what it stands on, the forks resolved, an honest achievable/phased/not-yet verdict, and the cheapest next step (often a spike or a research pass, not a build).
2. **A sequencing recommendation** — how the three slot against Tier-2 and the remaining internals: what's parallelizable, what depends on what, what's near-term vs long-game. Sean ratifies.
3. **A ROADMAP update** — add the three as named future workstreams (and likely a short "Product vision" section naming the outward turn), each with its scope verdict and promotion trigger, in Sean's locked priority order. Keep Tier-2 the active build focus unless Sean consciously re-sequences.

## Doctrine (same as every anima session)

- **Verify against the tree, never trust a label** — including this kickoff. If a referenced file/skill differs from the prose, the tree wins; flag it.
- **Anti-drift is the whole point.** Scope + sequence; do not start building any direction, and do not abandon Tier-2. The deliverable is a map, not code.
- **Two standing md5 guards must not move:** `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4`; `pipeline/agents/prompts/sean-screenwriting-voice.md` = `945af824fa53b948a18ac6bf206d67ef`.
- **$0.** Brainstorming, planning, and cheap research math only — no costed generation, no orchestrator runs. (Mind Sean's usage: he's preserving headroom until a Wednesday refresh.)
- **Read like a studio.** The design notes and the roadmap section should feel authored, not generated.

## Definition of done

- All three directions are scoped, their forks resolved, and an honest achievability/phasing verdict recorded for each.
- A ratified sequencing against the existing roadmap, in Sean's priority order, with Tier-2 still the active build focus (or a conscious, recorded re-sequence).
- `ROADMAP.md` updated with the three as named workstreams + the product-vision framing.
- No code, no model spend, both md5 guards intact. Everything presented to Sean for review.

## Immediate first action

Read `ROADMAP.md`, then `PHILOSOPHY.md`, then skim `CLAUDE.md`. Invoke `superpowers:brainstorming`. Open with Sean by reflecting the inflection point back to him in one paragraph (the outward turn, held against the anti-drift contract), then start on **whichever direction he wants first** — laying out its open questions and your first-pass take, then exploring. Brainstorm wide, converge hard, sequence honestly, hand back a map.
