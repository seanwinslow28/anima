# Brainstorm Front Door — Design Note (Direction ①)

**Date:** 2026-06-29
**Status:** Scoped and ratified in the 2026-06-29 vision-expansion brainstorm. **Not built.** Named as a future workstream — the first build picked up once Tier-2's Definition of Done is met.
**Session kickoff:** [`docs/active/2026-06-22-anima-vision-expansion-kickoff.md`](2026-06-22-anima-vision-expansion-kickoff.md)
**Companions:** the ② interface note, the ③ economics note, and the new *Product vision* section in [`ROADMAP.md`](../../ROADMAP.md).

---

## The vision

A relentless, structured elicitation that turns a spark into a fully-fleshed **concept doc** — which becomes the pipeline's brief, the Phase 0 input Maya already consumes. Mid-session it can fire a few sample frames so Sean locks the *look* before any costed run. This is the creative front door: the room where the director meets the crew before a single frame is drawn, and walks out with a brief the pipeline can build.

## What it stands on (already in the tree)

This isn't built from zero. It's an elevation of things that already exist:

- **`creative-director` is already a proto-front-door.** It runs a six-point "North Star" interview, proposes two or three visual routes with effort estimates, writes a technical execution plan, and hands off. What it *isn't*: a relentless multi-turn grill, and it hands off to *generation skills* rather than to Maya's brief. ① makes the interview relentless, adds story and PM substance, and redirects the hand-off into the pipeline.
- **The brief → Maya seam already exists.** `run.py` starts *from* a brief; ① is the thing that produces that brief.
- **The voice instrument is already vendored** — `pipeline/agents/prompts/sean-screenwriting-voice.md` (md5-guarded) is loaded verbatim into Sam and Bea. The front door draws on the same voice.
- **The creative substance is a skill shelf, not a gap:** `creative-director`, `sw-creative-toolkit` (storytelling / design-thinking / innovation-strategy), `pm-product-discovery:brainstorm`, `writing-voice-modes`, and the image-gen skills (`gemini-image-gen`, `gemini-pencil-animation-image-gen`).
- **Grill Me is the architectural model** (`mattpocock/skills`). Its doctrine: *user-invoked skills orchestrate* (`/grill-me`, `/to-prd`, `/prototype`); *model-invoked skills hold reusable discipline* (`/grilling`, the loop). "Small, easy to adapt, composable." Its `/prototype` ("several radically different variations you can toggle") is the art-viz analog. The whole repo is the shape ① should take.

## Forks resolved (2026-06-29)

- **Architecture → an orchestrated chain**, not a mega-skill. A model-invoked *grilling* loop holds the interview discipline; a user-invoked orchestrator runs the room and pulls creative substance from `creative-director` + the PM-discovery + the SW-creative storytelling + the voice skills; a no-interview *to-concept* synthesizer (Matt's `/to-prd` move) writes the artifacts. A mega-skill fights both Matt's doctrine and anima's own fleet pattern.
- **Art-viz → in-session, optional, cheap.** Generate two or three style routes as sample frames during the grill ($0 via Flow, cheap via NB2) so the look is locked before any costed run. Honors *iteration must be cheap* and *lock the look before compute*.
- **Output contract → brief + concept doc + locked style refs, with character seeds handing to Cy.** The richest hand-off: it enriches the Studio Brief Maya already consumes, plus a standalone concept doc (logline, world, characters, tone — human-facing and museum-worthy), plus the chosen style references. Character concepts seed Cy's Bible authoring.
- **Where it sits → a standalone interactive skill chain (a Phase 0− "Concept" front door), opt-in and back-compat.** It runs in a session and emits the brief directory; it is *not* a headless stage inside `run.py` — a relentless grill doesn't fit the gate model, and the run machine is designed to start *from* a brief. A hand-written brief simply skips it. Cleanest identity: the `creative-director` persona elevated from proto to the real thing.

## Verdict

**HIGH achievability · near-term · parallel-safe with Tier-2.** It's mostly skill authoring, chaining, and a clean hand-off into the existing brief; the art-viz loop is cheap. It touches **nothing** in the Em critic, so it cannot regress the frozen verdict baseline. The only real risk is loop quality — does it produce *specific* concepts rather than generic ones — which is a cheap skill-authoring and eval problem, not an architectural one.

## Cheapest next step (not a build)

A **$0 manual dry-run.** In one session, Claude plays the orchestrator by hand — pulls the skills in order on a real spark, fires the art-viz through Flow/NB2, and emits a real concept doc + brief — and Sean judges whether the output is good *before* a single skill file is authored. It's the spike-before-build discipline anima already runs, except the spike is free.

## Where it sits in the sequence

**First build after Tier-2's DoD** (Sean's locked order, 2026-06-29). The $0 dry-run *may* run in parallel earlier if Sean opts in; the build itself waits for Tier-2. It is the front door the whole product arc — ① concept → pipeline builds → ② shell strings and exports → ③ transports underneath — begins from.
