# Brainstorm Front Door (①) — Build Plan

**Date:** 2026-07-02
**Status:** Planning — **① is now the active build** (Tier-2's DoD is met; per the ROADMAP locked sequence, ① is first up). This plan supersedes the ①-scoping note's build section ([2026-06-29-brainstorm-front-door-design.md](2026-06-29-brainstorm-front-door-design.md)) with what the dry-run taught.
**Validated by:** the 2026-07-02 hand-run dry-run on Sean's Samurai-Jack-piñata spark ([concept doc](2026-07-02-frontdoor-dryrun-pinata-short-concept.md) + [Studio Brief](2026-07-02-frontdoor-dryrun-pinata-short-studio-brief.md)).

---

## What the dry-run changed

The dry-run proved the front door produces a concept worth iterating on (Sean: "the output is perfect," then immediately recast the dad → a secret-badass grandma — the sign it *engaged*). But it also exposed the real shape: because Sean handed over a near-complete spark, the run was almost pure *convergence* (interrogate + resolve). The built chain has to lead with **divergence** — take a one-line spark and *expand* it into avenues, styles, and themes — and it has to **stress-test** the concept before compute burns. Those two layers, both named by Sean, are the difference between "a good interviewer" and "a creative partner."

So the front door is a **five-stage chain**, not one interview.

## Architecture

A **user-invoked orchestrator** skill runs the room; each stage is a **model-invoked discipline skill** it reaches for (Matt Pocock's composable shape — user-invoked orchestrates, model-invoked holds the reusable craft; never a mega-skill). New skills live in `anima/.claude/skills/`. The front door is a **standalone interactive session** (not a headless `run.py` stage) that emits a **brief directory** → `python -m pipeline.run` consumes it. Opt-in and back-compat: a hand-written brief skips the whole thing.

## The five stages

| # | Stage | Role | Borrows from | Decision (2026-07-02) |
|---|-------|------|--------------|------------------------|
| 1 | **EXPAND** | Blow a spark open into premises, tones, themes, animation styles, "what-if" spins — options to react to, not questions to answer | `sw-creative-toolkit:brainstorm` (SCAMPER, Six Hats, Crazy-8s, Worst-Possible-Idea, anti-bias rotation, 100+ ideas), `innovation-strategy` | **Adaptive to the spark** — a one-liner gets the full fan-out; a rich concept gets a light touch straight to INTERROGATE |
| 2 | **INTERROGATE** | Relentless, one-at-a-time, *adaptive* grill — resolve every branch (emotional core, structure, tone, the open calls) | Grill Me `/grilling` + `creative-director` North Star (6-point) + `voiceprint-interviewing` craft | Adaptive branch-following (the dad→grandma pivot is the model) |
| 3 | **ART-VIZ** | Workshop characters + animation styles *visually* so the look is locked before compute | Higgsfield MCP + Flow ($0) + **customized** AKCodez style-prompt craft + `creative-director` art direction + the gemini/pencil image skills | **Flow $0 by default; Higgsfield MCP on demand** (matches the ③ trial) |
| 4 | **STRESS-TEST** | Creative pre-mortem + red-team on the *concept* before it's committed — the "extra layer of strategizing" | `pm-execution:pre-mortem` (Tigers / Paper Tigers / Elephants) + `strategy-red-team` (attack load-bearing assumptions, cheapest test) + `sw-creative:problem-solving` | On by default at concept-lock; findings surface, human decides |
| 5 | **SYNTHESIZE** | Emit the artifacts | Grill Me `/to-prd` pattern + the anima Studio Brief contract | Concept doc + Studio Brief + locked style refs + character seeds → Cy |

A one-line spark enters at EXPAND and leaves SYNTHESIZE as **a concept doc + a Maya-ready Studio Brief + locked style refs + character seeds** — exactly the bundle the dry-run produced by hand.

## The AKCodez skills — disposition

Vetted safe (2026-07-02): 19 pure-markdown skills, zero code, clean danger + injection scans. **Decision: customize the useful ones.**

- **Borrow + customize (5):** `01-cinematic`, `03-cartoon`, `05-fight-scenes`, `08-anime-action`, `04-comic-to-video`. Their structure is genuinely good — 2-second hook, timeline segmentation, a camera-movement encyclopedia, lighting/sound, 5+ example prompts. We adapt them into **anima style-prompt skills for creative shorts** (starting with a **`genndy-tartakovsky` style skill** built from this session's research sheet), stripping the UGC/marketing flavor.
- **Drop:** the marketing/vertical genres (ecommerce, real-estate, fashion, food, product-360, motion-design-ad, brand-story, music-video, social-hook) and the `ugc-*` skills.
- **Replace, don't import:** their automation wrappers (`higgsfield-image-auto`, `seedance-auto-generate`, `ugc-video-auto`) drive Higgsfield by **Playwright browser-clicking**. Sean's **Higgsfield MCP + CLI is API-backed** and supersedes them — ART-VIZ drives generation through the MCP, never browser automation.

## The art-viz engine (cost-aware)

- **Default: Flow ($0).** ART-VIZ emits Flow-ready prompts (the 3-style-route pattern from the dry-run); Sean generates on his subscription at $0.
- **On demand: Higgsfield MCP.** For richer/faster in-loop exploration — `generate_image` across the model palette (Soul 2.0, Nano Banana Pro/2, Seedream, FLUX.2, Reve, GPT Image), `show_characters` for reusable character refs, `generate_video`/`motion_control` for motion tests. Credit-metered — used deliberately during the trial month, tracked against the ③ decision.
- The customized style skills feed *both* engines (they generate the prompt; the engine renders it).

## Output contract (what the pipeline gets)

- **Studio Brief** (`00_studio_brief.md`) — Maya's Phase-0 input, in the exact contract shape (What is this about / Who is this character / Tone / What this is NOT / Format / Medium / Deadline / Non-negotiables).
- **Concept doc** — the rich, human-facing, museum-worthy artifact.
- **Locked style refs** — the chosen art-viz frames.
- **Character seeds** — hand to Cy for Bible authoring.

## Build slices (phased, walking-skeleton first)

1. **Slice 1 — the walking skeleton.** The orchestrator + INTERROGATE + SYNTHESIZE → emits a real brief directory. Prove the output contract end-to-end (a brief `pipeline.run` accepts). **The dry-run's piñata concept + Studio Brief is the ground-truth fixture** — the built skeleton must re-produce a brief of that quality. TDD/stub-green where it applies.
2. **Slice 2 — EXPAND.** The adaptive divergence engine (sw-creative borrow). Validate on a *one-line* spark ("a kid at a birthday party that feels like a samurai movie") — it must fan out into avenues before narrowing.
3. **Slice 3 — ART-VIZ + style-skill library.** Flow-prompt path + Higgsfield MCP on-demand path; customize the first style skill (`genndy-tartakovsky`) from the AKCodez shape + this session's research. Validate: it renders the 3 style routes.
4. **Slice 4 — STRESS-TEST.** The pre-mortem + red-team layer on a locked concept. Validate: it catches a deliberately weak concept (a ships-red fixture).

## Cheapest next step

**Slice 1, authored + validated against the piñata dry-run.** The dry-run already *is* the spec and the eval fixture — build the skeleton so it reproduces a piñata-grade brief from the same inputs, and the front door is real end-to-end before we enrich it.

## Open threads / deferred

- The full style-skill library beyond `genndy-tartakovsky` (add per project).
- EXPAND's technique rotation (which sw-creative techniques, when) — tune on real sparks.
- ART-VIZ motion tests (Seedance via MCP) vs stills-only in the front door.
- Whether STRESS-TEST is always-on or a `--stress-test` toggle.
- Eval suite for the chain (the piñata run is fixture #1; add more sparks).

## Anti-drift note

Tier-2's DoD is met, so **① is the active build** — this plan is its spec. ②'s daemon foundation remains the parallel-safe next slice (its own plan). ③ (cost) runs alongside as a decision. The order holds.
