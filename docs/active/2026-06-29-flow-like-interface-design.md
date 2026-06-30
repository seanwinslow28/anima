# Flow-like Interface — Design Note (Direction ②)

**Date:** 2026-06-29
**Status:** Scoped and ratified in the 2026-06-29 vision-expansion brainstorm. **Not built.** The long-game centerpiece; its daemon foundation is a parallel-safe early slice, the full UI is the LATER lane.
**Session kickoff:** [`docs/active/2026-06-22-anima-vision-expansion-kickoff.md`](2026-06-22-anima-vision-expansion-kickoff.md)
**Companions:** the ① front-door note, the ③ economics note, and the *Product vision* section in [`ROADMAP.md`](../../ROADMAP.md).

---

## The vision

A native desktop app for making animated shorts with the crew: a project gallery, a page per stage (character builder, scene/storyboard board, generate, motion), a chat window and buttons in place of the terminal, ending on a **simple timeline** to arrange clips, preview, and export — after which Sean finishes in real editing tools. Layout inspired by **Google Flow**; architecture inspired by **Open Design**. The literal expression of two load-bearing beliefs: *the pipeline is the portfolio piece*, and *read like a studio, not a terminal*.

## What it stands on (verified against the tree)

- **The orchestrator is already API-shaped.** `pipeline/run.py` doesn't bury logic in the CLI — it delegates to importable stage functions (`plan_stage`, `script_stage`, `storyboard_stage`, `generate_stage`, `animatic_stage`) over a `run_state.json` the gates read and write, and the gates are CLI flags (`--approve-plan`, `--approve-frame N`, `--retry-frame N --note`). A grep confirms there is **zero** HTTP/server/websocket code today — so the daemon is a real prerequisite, but it's "expose the existing functions over HTTP," not a rewrite. The state machine is the data model; the gates are the endpoints.
- **Open Design is the proven shape to copy.** Local-first, BYOK at every layer: a web frontend (Next.js, Vercel-deployable) talking to a local daemon (Express + SQLite) that proxies to any provider; an optional Electron desktop shell discovers the daemon via sidecar IPC. anima already has the local-files half (`runs/`, `characters/`, `run_state.json`) and the BYOK half (`.env` keys + subscription transports). The UI is the missing face.
- **Flow's surfaces map ~1:1 onto anima's stages** (from Sean's 2026-06-29 screenshots): the project gallery → the v1 dashboard; the workspace left-nav (Images / Videos / **Characters / Scenes** / Tools) → the stage-navigation spine; "New character" (sample cards + describe + reuse-for-consistency) → Cy's Character Builder; the 2×3 storyboard → Bea; "What do you want to change?" + the history filmstrip → Flo + Em's generate/edit loop (the `ONLY CHANGE:` discipline made visible); the asset picker's "Add to Prompt" → reference injection; the clip strip + preview → the v3 timeline. Sean is *already* running anima-adjacent work through Flow by hand — ② brings it in-house behind his own fleet and gates.
- **Build skills exist:** `frontend-design`, `impeccable`, `prompting-beautiful-ui`.

## Forks resolved (2026-06-29)

- **v1 scope → chat + gates over the orchestrator.** A project dashboard, the existing plan/frame/retry gates rendered as screens, and a chat shell driving the agents. Kills the terminal; lowest new surface; fastest to a working demo.
- **API foundation → early and standalone.** A thin FastAPI over the existing stage modules — backend plumbing that touches nothing in Em, so it's parallel-safe and can't regress the baseline. Built before the UI; useful on its own as programmatic run control.
- **Stack & shape → native desktop app (Electron/Tauri).** A desktop shell spawns the FastAPI daemon as a sidecar and loads the web frontend — exactly Open Design's Electron-plus-daemon pattern. Electron vs Tauri stays a build-time call (Electron is lower-friction and matches Open Design; Tauri is lighter). The one real trade: a recruiter can't click a link to try it — but a screen-recorded walkthrough keeps the portfolio weight, so the demo value survives.
- **Timeline reach (asked directly):** simple arrange / trim / preview / export is achievable as v3. A full NLE (effects, audio mixing, keyframed transitions) is *not*, and by design Sean doesn't want it — he exports and finishes in real tools. Simple timeline yes; full editor no.

## Phasing ladder

1. **Foundation (early, standalone, parallel-safe):** the FastAPI daemon over the orchestrator.
2. **v1:** the desktop shell + chat + the existing gates as screens.
3. **v2:** the per-stage visual pages (character builder, storyboard board, generate grid, motion) — each with a proven Flow precedent to copy one at a time.
4. **v3:** the simple timeline (arrange / trim / preview / export).

## The differentiator (why it's a portfolio piece, not a Flow clone)

Flow is a freeform generation playground with no opinion. anima wraps the *same surfaces* around the **gated pipeline** — the critic, the Bible lock, the animatic placement, the run state, the museum. That judgment is the part Flow can't show, and it's exactly what makes ② demonstrate product craft to a hiring manager rather than just "I used an AI tool."

## Verdict

**MEDIUM, phased — the long-game centerpiece, but the foundation is a clean early slice.** The daemon is HIGH-achievability on its own and parallel-safe. The full UI is the biggest build of the three and genuinely wants the internals reasonably settled, since it's a face over them — but it's de-risked by the orchestrator already being factored into importable functions.

## Cheapest next step (not a build)

A one-page **API-surface map** — each gate/stage function → an endpoint, `run_state.json` as the wire schema. Then, with Flow's screenshots in hand, a **v1 screen inventory** (which gate → which screen) plus a wireframe via `frontend-design`/`impeccable`. The first real code, whenever ② is promoted, is a tracer-bullet: `GET /runs/<id>/state` → one status screen reading a real `run_state.json`. The deeper Flow teardown (exact layouts, interactions) is real but it's v2-build-time work, deferred intentionally.

## Where it sits in the sequence

The **daemon foundation** is the second build after Tier-2 and can overlap behind ①. The **v1 → v3 interface** plus **Museum wiring** are the LATER lane — the long game, once the internals are settled. ③'s transport decision is the cost spine under the generate and motion screens.
