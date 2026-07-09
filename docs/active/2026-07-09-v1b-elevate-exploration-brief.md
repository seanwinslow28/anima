# v1b "Elevate" — creative-exploration brief

**Date:** 2026-07-09 · **For:** a Fable-5 exploration session · **Status:** approved (Sean, 2026-07-09), kickoff issued. · **Feeds:** the v1b TDD build (a later, separate session).

## Why this exists

The ② daemon's entire **core gate-loop backend is done** — read API (Slices 1–3), the job layer (Slice 4), the seven POST gate actions (Slice 5). The next milestone is **v1b — the gate screens + eye-gate ("the terminal is dead")**. Before we TDD-build it, Sean wants to **unleash Fable 5's frontend strength**: hand it the plan, give it real reference + generation tooling, loosen the guardrails, and see how much better v1b can be than the spec-as-written.

This is a **divergent visual-direction pass** — explore first, commit later. It produces **3 distinct directions** Sean judges; a *separate* TDD build session executes whichever he picks (or a blend). **No production code, no daemon wiring, no tests** here.

## The decisions that shaped this (from the 2026-07-09 brainstorm)

1. **Pass shape** — divergent visual-direction pass FIRST (no production code); a separate TDD build follows against the chosen direction.
2. **Latitude** — **reinvent freely from the soul.** The only locked floor is the philosophy + the daemon data contract; everything visual/interaction is open.
3. **Scope** — each direction goes deep on **3 hero surfaces** that bracket the app's range.
4. **Deliverable** — **coded animated HTML mockups + mood boards** (feel the real motion in a browser), not static art or described motion.
5. **References** — **Fable discovers autonomously** (with the access caveat + fallback below).

## The locked floor (Fable may NOT break these)

- **The philosophy** ([`PHILOSOPHY.md`](../../PHILOSOPHY.md)) — the human owns taste and timing; the critic **proposes fixes, never decides**; **"read like a studio, not a terminal"**; iteration is cheap (draft→pro); the museum is evidence; engine truth is the arbiter. **Every direction must argue *how* it serves this** — the interface is a *face over the pipeline* that makes the human's taste-keeping the fastest possible, not a click-to-generate toy.
- **The daemon data contract** — Fable may imagine any UI, but anything that needs data the daemon doesn't already serve (Slices 1–5: `GET /runs`, `/runs/{id}`, `/status`, `/artifacts/{kind}`, `/frames/{n}/candidates`, `/frames/{n}/image`, the `202`+`GET /jobs/{id}` job layer, the seven gate POSTs, `active_job`/`blocked_by_job`) must be **flagged as a backend delta** (map it to D1–D6 or name a new one), never silently assumed. This keeps the exploration honest about what's buildable.

**Everything else is OPEN** — palette, typography, motion language, layout, density, the signature moments, even the eye-gate's core feel. The current warm/dark spec (uxui-spec + addendum) is **input to react against, not a constraint to honor.** A direction may look nothing like it.

**One consequence to hold:** a freely-reinvented language re-skins the **already-shipped v1a** (Dashboard + Run overview) too — the winning direction becomes the *whole app's* language. That's expected; the run-overview hero surface is where it shows.

## What each of the 3 directions delivers

- **Three hero surfaces, each a self-contained animated `.html`** Sean opens in a browser and *feels*:
  1. **The eye-gate** — the instrument. The **rock/flip loop, the cel-flip frame-advance, the critic's mark, onion-skin/diff** must **actually move** (real CSS/JS animation over placeholder frames). This is the emotional core — "the terminal is dead" lives or dies here.
  2. **A reading gate** — the **storyboard curation gate** (or plan gate): how the language handles *calm, text-heavy judging* — long prose, a shot list, the human's approve/curate decision.
  3. **The run overview** — the home base (re-skinned from v1a): the stepper, the hero decision block, the cost ledger, the mini-reel.
- **Real anima content, never lorem ipsum** — so Sean judges the true thing. Sources in-repo (a fresh checkout has these; `runs/` is gitignored so don't rely on it):
  - Real pencil frames: [`characters/sean-anchor/`](../../characters/sean-anchor) (anchor, turnarounds, expressions), [`characters/claude-mascot/`](../../characters/claude-mascot), [`evals/vision_critic/fixtures/frames/`](../../evals/vision_critic/fixtures/frames) (44 corpus images), [`museum/`](../../museum) (committed exhibit thumbnails).
  - Real data shapes + copy: [`tests/server/conftest.py`](../../tests/server/conftest.py) `make_generate_run` (a real frame with two attempts + Em records — verdict `flag`, cites `IR.sean.style.line-weight`, reasoning "line weight drifts on the arm", a proposed fix, then a `pass`), [`server/state_view.py`](../../server/state_view.py) + [`server/artifacts.py`](../../server/artifacts.py) (the exact `next_action`/`candidates`/`status` shapes), and a real Em trace under [`evals/vision_critic/traces/`](../../evals/vision_critic/traces).
- **A mood board** per direction — the references Fable found + any Higgsfield-generated textures/hero imagery that shaped it (embed as data-URIs so the page is self-contained).
- **A one-screen rationale** per direction — *how it serves the soul* (name the philosophy tenets it leans on) + its **"what it'd need from the daemon"** note (deltas, if any).

## How Fable works

- **References — autonomous, with an honest fallback.** Fable discovers its own references from the soul brief. **Verify site access first:** a session's web fetch does NOT carry Sean's browser logins, and Cosmos/Pinterest are JS/auth-walled — so expect thin results there. **Fall back to the openly-fetchable design web** (Awwwards, editorial/animation-studio sites, design writing, museum/gallery UIs) **+ Higgsfield generation** for original mood. If Fable wants Sean's specific boards, it should say so and ask him to paste public URLs/screenshots.
- **Generation** — Higgsfield MCP is available for mood textures / hero imagery (subscription credits — spending them here is the point; keep it proportional).
- **Real, felt UI** — Fable's actual strength. Each direction is genuinely different *points of view*, not variations on one theme.
- **a11y** — not a hard gate on exploration, but design **buildable-accessible**: no color-only signaling, keyboard-first intact, real focus states — because the build will enforce **WCAG 2.1 AA**.
- **Boundary** — this session writes **no** `pipeline/`, `server/`, `web/` production code and **no** tests. Its output is direction artifacts (HTML + moodboards + rationales) only.

## Delivery + how we converge

- Each direction is a **self-contained `.html`** (inline CSS/JS, assets as data-URIs) Sean can open directly; **also publish each via the Artifact tool** for one-click viewing (CSP blocks external hosts, so everything must be inlined). Add a small **comparison index** linking the three.
- Preserve the work on a branch `feature/v1b-elevate-exploration` with a **draft PR** (the exploration is a real artifact worth keeping); bulky raw generation output stays in a gitignored scratch dir.
- **Convergence:** Sean opens the three, feels them, **picks one or blends.** Then the planning seat reviews, and we write the **v1b TDD build kickoff** against the chosen direction — where we JIT-decide Slice 6 and which gate screens land in the first build increment.

## Session hygiene

- Fresh worktree off **latest** `main` (`git fetch origin && git reset --hard origin/main`).
- Model **Fable 5** (the frontend-design strength this whole pass is built around).
- Read first: [`PHILOSOPHY.md`](../../PHILOSOPHY.md), [`docs/active/2026-07-03-flow-interface-uxui-spec.md`](2026-07-03-flow-interface-uxui-spec.md), [`docs/active/2026-07-03-flow-interface-spec-addendum-v1.1.md`](2026-07-03-flow-interface-spec-addendum-v1.1.md) (the plan it's elevating — react against it), and this brief.
- Reminder: subscription billing, `ANTHROPIC_API_KEY` absent (fleet-ops); Higgsfield via its MCP.
