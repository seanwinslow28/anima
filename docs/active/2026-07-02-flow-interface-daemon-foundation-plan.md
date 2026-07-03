# Flow-like Interface (②) — Daemon Foundation + v1 Screen Inventory

**Date:** 2026-07-02
**Status:** Planning — ②'s **daemon foundation** is the parallel-safe slice that can start behind ① (it touches nothing in Em/pipeline logic — it *drives* the existing functions). The full UI (v1→v3) stays the LATER lane. Companion: the ②-scoping note ([2026-06-29-flow-like-interface-design.md](2026-06-29-flow-like-interface-design.md)).

---

## The premise, verified against the tree

`pipeline/run.py` is a resumable state machine over `runs/<id>/run_state.json`. The stages are importable functions in `pipeline/orchestration/`; the gates are CLI flags; each gate function **already mutates and atomically saves state**. Confirmed this session:

- **STAGES** = `PLAN → SCRIPT → STORYBOARD → ANIMATIC → GENERATE → ASSEMBLE → DONE` (forks: `PLAN→{SCRIPT|GENERATE}`, `STORYBOARD→{ANIMATIC|GENERATE}`) — [`state.py`](../../pipeline/orchestration/state.py).
- **The gate functions** return `int` exit codes and print `render_status`: `run_plan_stage`/`approve_plan_gate`, `run_script_stage`/`approve_script_gate`, `run_storyboard_stage`/`approve_storyboard_gate`, `run_animatic_stage`/`approve_animatic_gate`, `enter_generate`/`run_frame_fan`/`approve_frame`, `run_assemble_stage`.
- **`render_status` + `_next_hint` already compute the next action per stage** — the exact affordance a UI needs.

**So the daemon is a thin FastAPI that imports those functions, calls them, and returns the fresh `load_state()` as JSON + a `next_action`.** Not a rewrite — a face over what's there.

## The wire schema (`run_state.json`)

The daemon's data model, verbatim from the tree (`schema_version: 1`): `run_id`, `created_at`/`updated_at`, `brief_dir`/`brief_src`, `manifest_path`, `shots_path`, `slug`, `stub`, `stage`, `needs_storyboard`, `animatic_enabled`, `target_frames`, `cast[]` (`folder_key`/`ir_namespace`/`anchor`/`criteria`), `plan{status, plan_path, criteria_path, production_brief_path, cost_estimate{low/median/high_usd, by_phase}}`, `frame_order[]`, `holds{}`, `frames{}` (per-frame `status` ∈ pending/generated/approved + `attempts[]`), `assemble{sequence_file, gif, webm, mp4}`. (`script{}`/`storyboard{}` appear when those stages run.) The daemon returns this object as-is — no new schema.

## The API surface (endpoints ← CLI gates + stage functions)

| Method | Endpoint | Backed by | Returns |
|---|---|---|---|
| `GET` | `/runs` | scan `runs/*/run_state.json` | run list (id, stage, slug, updated_at, thumb) |
| `POST` | `/runs` | `--brief` → `new_state` + `run_plan_stage` | fresh state |
| `GET` | `/runs/{id}` | `load_state` | full `run_state.json` |
| `GET` | `/runs/{id}/status` | `render_status` / `_next_hint` | `{stage, next_action, frames}` |
| `POST` | `/runs/{id}/plan/approve` | `approve_plan_gate` | fresh state |
| `POST` | `/runs/{id}/script/approve` | `approve_script_gate` | fresh state |
| `POST` | `/runs/{id}/storyboard/approve` | `approve_storyboard_gate` | fresh state |
| `POST` | `/runs/{id}/animatic/approve` | `approve_animatic_gate` (+ rough upload) | fresh state |
| `POST` | `/runs/{id}/frames/{n}/approve` | `approve_frame` (body: `attempt?`) | fresh state |
| `POST` | `/runs/{id}/frames/{n}/retry` | `run_frame_fan` (body: `note`) | fresh state |
| `POST` | `/runs/{id}/assemble` | `run_assemble_stage` | fresh state |
| `GET` | `/runs/{id}/artifacts/{plan\|script\|storyboard\|brief}` | files in `brief_dir` | markdown / yaml |
| `GET` | `/runs/{id}/frames/{n}/candidates` | `candidates/` + Em verdict | image list + verdict |
| `GET` | `/runs/{id}/frames/{n}/image?attempt=K` | `candidates/` or `approved/` | image bytes |
| `GET` | `/runs/{id}/cost-estimate` | `plan.cost_estimate` | `{low, median, high, by_phase}` |
| `GET` | `/characters` · `/characters/{id}` | `characters/` | Bible list / `character.yaml` |

The daemon is **read-heavy** (render state + artifacts) with a handful of **POST gate actions** — and it never mutates run history destructively; it drives the same audited functions the CLI does.

## The one real adaptation

The gate functions return `int` exit codes and *print* hints today. The daemon wrapper: `try: gate_fn(...)` → on success `return load_state(run_dir)` (fresh JSON) + `next_action = _next_hint(state)`. That's it. The state machine's own "what to do next" logic becomes the UI's navigation logic — **the `next_action` field tells the frontend which gate screen to surface**, so the run *drives* the app.

## v1 screen inventory (screen ← endpoints ← Flow precedent)

| Screen | Endpoints | Flow screenshot precedent |
|---|---|---|
| **Dashboard** (run gallery) | `GET /runs`, `POST /runs` | the project gallery (Pencil&Prompt, Claude Mascot Dataset…) |
| **Run overview / status** | `GET /runs/{id}/status`, `/runs/{id}` | the project workspace + left-nav (Characters/Scenes) |
| **Plan gate** | `GET artifacts/plan` + `cost-estimate`; `POST plan/approve` | *(anima-only — Flow has no plan gate; this is the differentiator)* |
| **Script gate** | `GET artifacts/script`; `POST script/approve` | the text/prompt panels |
| **Storyboard curation gate** | `GET artifacts/storyboard`; `POST storyboard/approve` | the 2×3 storyboard view ("Boy growing up") |
| **Animatic placement gate** (opt-in) | rough upload; `POST animatic/approve` | the asset-upload modal |
| **Generate / eye-gate** (most-used) | `GET frames/{n}/candidates`; `POST approve` / `retry` | "What do you want to change?" + history filmstrip |
| **Assemble / done** | `POST assemble`; `GET assemble` | the clip-strip + preview player (→ the v3 timeline) |
| **Chat shell** (persistent) | drives all of the above | the bottom chat bar on every screen |

**The gate screens ARE the pipeline's opinion made visible** — the plan gate + cost preview, the storyboard curation, the per-frame eye-gate with Em's read. That's what Flow can't show and what makes ② a portfolio piece.

## The tracer-bullet (first real code, whenever ② is promoted)

`GET /runs/{id}/status` → one **status screen** rendering a real `run_state.json` (stage machine + `next_action` + frame list). Read-only, one endpoint, one screen — proves the daemon-reads-state-renders-screen loop end to end on a real run before any gate action is wired.

## The desktop shell

Per Sean's stack call: an **Electron/Tauri** shell spawns the FastAPI daemon as a **sidecar** and loads the web frontend (Open Design's pattern). Electron vs Tauri stays a build-time decision (Electron = lower-friction/matches Open Design; Tauri = lighter). BYOK/local-files: reads the existing `.env`, `runs/`, `characters/`.

## Cheapest next step

This doc **is** the API-surface map. The next tangible artifacts (design, not the full build): the **tracer-bullet** above + a **v1 wireframe** of the dashboard + status + eye-gate screens (via `frontend-design`/`impeccable`), laid over the Flow screenshots. The deeper Flow teardown is v2-build-time.

## Parallel-safe note

The daemon reads state + drives existing functions — it changes **nothing** in Em, the criteria, or the pipeline logic, so it cannot regress the frozen baseline. It can start behind ① without contending for the active-build slot. ①'s front door emits the brief the daemon's `POST /runs` consumes — the two directions meet exactly at the brief.
