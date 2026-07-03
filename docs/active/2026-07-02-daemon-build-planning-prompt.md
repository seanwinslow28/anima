# ② Flow Interface Daemon — Build Planning Prompt

**How to use:** open a fresh Claude Code session in the `anima` repo, set the model to **Opus 4.8**, and paste everything below the line. It co-plans the daemon-foundation build with **Codex** and ends by printing a **Fable 5 execution kickoff**.

**Brainstorm recommendation (Sean asked):** ② has **one genuine open architecture fork** — the long-running-job / async model, because the gate functions are synchronous and slow (they call models for minutes). That's worth nailing before the detailed plan. This prompt resolves it inline (Step 2, with Codex). If you'd rather lock it in isolation first, run a short `superpowers:brainstorming` session on *just* "how should a FastAPI daemon drive slow, synchronous gate functions?" and then run this. ① did **not** need this; ② does.

---

▼▼▼ PASTE EVERYTHING BELOW THIS LINE ▼▼▼

You are **Opus 4.8**, planning the build of anima's **② Flow-like interface — the daemon foundation only** (the parallel-safe backend slice; NOT the full UI). Produce a **detailed, TDD-sliced implementation plan** that **Fable 5 will execute**, co-planned with **Codex** via the `codex` plugin. **Plan only — no implementation code this session.**

## 1. Read first (source of truth)
- `CLAUDE.md`, `PHILOSOPHY.md`, `ROADMAP.md`.
- **The build plan you're implementing:** `docs/active/2026-07-02-flow-interface-daemon-foundation-plan.md` — the API-surface map, the `run_state.json` wire schema, the v1 screen inventory, the tracer-bullet.
- **The real orchestrator the daemon wraps:** `pipeline/run.py` (the CLI gates) and `pipeline/orchestration/state.py` (`STAGES`, the state schema, `load_state`/`save_state`/`advance_stage`, `render_status`/`_next_hint`), plus the stage entry functions (`plan_stage`, `script_stage`, `storyboard_stage`, `animatic_stage`, `generate_stage`, `assemble_stage`). Note they return **int exit codes** and print `render_status`.
- **Skills this build references that are NOT in `anima/.claude/`:** the superpowers discipline skills (`test-driven-development`, `using-git-worktrees`, `verification-before-completion`, `brainstorming`) and `impeccable` (the v1-UI-polish cheapest-next-step). Their details are vendored, organized by build stage, in **[`docs/active/2026-07-02-referenced-skills-detail-reference.md`](2026-07-02-referenced-skills-detail-reference.md) — read it for any referenced skill not in `.claude/skills/`.**
- `docs/architecture/fleet-ops-protocol.md`.

## 2. Resolve the architecture forks FIRST (with Codex)
Lock these before detailed planning:
- **The long-running-job model — the crux.** The gate functions are **synchronous and slow** (`run_plan_stage` / `run_frame_fan` call models, minutes each). HTTP handlers can't block that long. Decide the model: a background job queue + a job-status endpoint (mirroring the CLI's `--background` / `--status` shape)? A threadpool executor? Sync-with-polling? Pick one and justify it.
- **Sync-function → JSON-response adaptation.** Handlers call the existing gate function, then return the fresh `load_state()` + a `next_action` derived from `_next_hint`. Confirm the wrapper pattern (the functions already mutate + atomically save state, so the daemon must not double-write).
- **Process / sidecar model.** Defer the Electron/Tauri shell — build the **daemon standalone** (runnable + testable on its own) first; note the sidecar seam for later.
- **Scope guard.** Daemon + the **tracer-bullet** (`GET /runs/{id}/status` → one status view over a real `run_state.json`) ONLY. No v1 UI, no gate-action endpoints beyond what the tracer-bullet needs, this round.

Get Codex's read on these before you commit: `/codex:rescue --background "Read docs/active/2026-07-02-flow-interface-daemon-foundation-plan.md, pipeline/run.py, and pipeline/orchestration/state.py. Advise on the best long-running-job/async model for a FastAPI daemon that must drive these slow synchronous gate functions without blocking, and flag state-race risks."` — then `/codex:status`, `/codex:result`. Write your resolved fork-decisions down, then `/codex:adversarial-review` them.

## 3. Co-plan with Codex
1. Draft your plan — the FastAPI app layout in a **new dir** (e.g. `server/`); endpoint handlers ↔ gate functions per the API-surface table; the job model from Step 2; the tracer-bullet as Slice 1; the test strategy (FastAPI `TestClient` against real `runs/*/run_state.json` fixtures). Write it to `docs/active/2026-07-02-daemon-build-plan-CONVERGED.md`.
2. Codex's **independent** plan: `/codex:rescue --background "Produce your own independent, TDD-sliced implementation plan for a thin FastAPI daemon over anima's orchestration gate functions, tracer-bullet first (GET /runs/{id}/status), with special attention to the job/async model and testing."` — `/codex:status`, `/codex:result`.
3. **Reconcile**; record disagreements + your calls.
4. **Red-team:** `/codex:adversarial-review challenge this daemon plan — attack the job/async model, state races (two clients driving one run at once), error/rollback handling, and whether the tracer-bullet is truly the smallest safe first slice.`
5. Fold in the red-team.

## 4. anima discipline (bake in)
- **Worktree isolation**; **TDD** — FastAPI `TestClient`, credential-free against `runs/` fixtures (stub the gate calls so no model runs in CI).
- **Parallel-safe guarantee — prove it:** the daemon changes **NOTHING** in Em, the criteria, or pipeline logic — all new code in the new dir, the pipeline byte-identical, the existing suites still green.
- **Fleet-ops:** subscription billing, **never `ANTHROPIC_API_KEY`**.
- **The two md5 guards must NOT move:** `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4`; `pipeline/agents/prompts/sean-screenwriting-voice.md` = `945af824fa53b948a18ac6bf206d67ef`.
- Tests **per-directory**; `superpowers:verification-before-completion` before any "done."

## 5. Deliverables (this session — no building)
1. `docs/active/2026-07-02-daemon-build-plan-CONVERGED.md` — the final plan: the resolved job/async model, the FastAPI app layout, the endpoint↔function map, per-slice TDD tasks, the tracer-bullet as Slice 1, state-race handling, risks, and the Codex-reconciliation notes.
2. A **Fable 5 execution kickoff** — print, at the very end, a ready-to-paste prompt for a fresh Claude Code session **set to Fable 5** that executes **the tracer-bullet slice only** (the daemon skeleton + `GET /runs/{id}/status` + its tests), stopping green for Sean's review.

Do not build. End by printing the Fable 5 kickoff.
