# ② Flow Interface — Daemon Foundation: Converged Build Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Build discipline: superpowers:test-driven-development (red → verify-red → green → verify-green), superpowers:using-git-worktrees (isolate), superpowers:verification-before-completion (evidence before "done").

**Date:** 2026-07-02
**Status:** Plan — ready to execute the tracer-bullet slice. Co-planned this session with Codex (fork-advice pass + independent-plan pass + adversarial-review pass; reconciliation notes at the end).
**Goal:** Stand up a thin, standalone FastAPI daemon that reads `runs/<id>/run_state.json` and renders the pipeline's own "what to do next" as JSON — proving the *daemon-reads-state → renders-screen-contract* loop end-to-end on a real run, with **one read-only endpoint** (`GET /runs/{id}/status`) and zero changes to the pipeline.

**Architecture:** The daemon is a *face* over the existing resumable state machine in [`pipeline/run.py`](../../pipeline/run.py) + [`pipeline/orchestration/`](../../pipeline/orchestration). Read endpoints call `state.load_state()` in-process and project it. Write endpoints (a later lane) drive the **existing CLI** as background jobs — the pipeline stays the single source of truth. This session builds **only** the read side (the tracer-bullet); every write/async mechanism is designed here and deferred to a named later slice.

**Tech Stack:** Python 3, FastAPI, Starlette `TestClient` (via `httpx`), uvicorn (run only; not under test). No new pipeline dependencies; all daemon code lives under a new `server/` package.

---

## Global Constraints

Copied verbatim from the source build plan, ROADMAP, and fleet-ops protocol. Every task's requirements implicitly include this section.

- **New code only in `server/`.** `pipeline/` and `evals/` stay **byte-identical**. The daemon *imports and drives* existing functions; it changes nothing in pipeline logic, Em, or the criteria. This is what makes ② parallel-safe behind ①. *(Sharpened per Codex: "parallel-safe" holds unconditionally for the read-only status slice; POST gate actions are **not** race-safe without the single-writer guard in §Fork 1 — do not claim blanket parallel-safety once writes land.)*
- **Two md5 guards must NOT move:** `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4`; `pipeline/agents/prompts/sean-screenwriting-voice.md` = `945af824fa53b948a18ac6bf206d67ef`. The daemon touches neither file; the verification step re-checks both.
- **Credential-free tests.** FastAPI `TestClient` against fixture `run_state.json` built via `state.new_state()` + `state.save_state()`. The tracer-bullet calls **no gate function**, so no model can run. Later write-slice tests inject a stub driver — no real subprocess, no spend.
- **Fleet-ops billing:** never rely on `ANTHROPIC_API_KEY`; subscription/OAuth only. The read-only daemon makes no model calls; the later job worker inherits `pipeline/run.py`'s existing `_api_key_guard` for free by driving the CLI (see §Fork 2).
- **Per-directory pytest.** New tests run as `python -m pytest tests/server/`. The existing contract suite (`python -m pytest tests/`, ~562 tests) and `python -m pytest pipeline/tests/` stay green.
- **Worktree isolation.** Execute in a dedicated `git worktree` on a feature branch, per fleet-ops §2.
- **Scope guard (this session):** daemon skeleton + the tracer-bullet **only**. No UI, no POST gate actions, no job queue, no artifact/image endpoints. Those are designed below and deferred.

---

## The premise, re-verified against the tree

`pipeline/run.py` is a resumable stage machine over `runs/<id>/run_state.json`. Confirmed this session by reading the source:

- **STAGES** = `PLAN → SCRIPT → STORYBOARD → ANIMATIC → GENERATE → ASSEMBLE → DONE` ([`state.py:17`](../../pipeline/orchestration/state.py)). Forks: `PLAN→{SCRIPT|GENERATE}` on `needs_storyboard`; `STORYBOARD→{ANIMATIC|GENERATE}` on `animatic_enabled`.
- **Gate functions** are `fn(state: dict, manifest: dict, run_dir: Path, ...) -> int`. Each **mutates `state` in place, calls `state.save_state(run_dir, state)`, prints human text, returns an exit code** (0 ok / 1 gate failure / 2 bad request or wrong stage). Several **cascade**: `approve_plan_gate` calls `run_script_stage` or `enter_generate` ([`plan_stage.py:130-142`](../../pipeline/orchestration/plan_stage.py)); `approve_frame` can generate the next frame or run assemble.
- **`state.load_state(run_dir)`** is the read side — atomic, raises `StateError` on a missing file, unparseable JSON, or `schema_version != 1`. **It does NOT validate object shape** (Codex red-team, verified against [`state.py:89-104`](../../pipeline/orchestration/state.py)): a file that is valid JSON with `schema_version: 1` but missing `plan`/`stage`/`frames` keys passes `load_state`, then the projector's key access raises `KeyError`. The router therefore maps `StateError` **and** projector `KeyError`/`TypeError` to `422` (see Task 5), so a malformed-but-parseable state never 500s.
- **`state._next_hint(state)`** computes the next action per stage — but as a **CLI-oriented string** (`"...--approve-plan"`), and **`state.render_status(state)` returns a plain string, not JSON** ([`state.py:147`](../../pipeline/orchestration/state.py)).

**Correction folded in (Codex, verified):** the source build plan says gate functions "print `render_status`" — they do not; each prints its *own* CLI text, and only `run.py`'s `--status` path calls `render_status`. The JSON status shape the UI needs must be **built by the daemon**, not read off an existing function. This plan builds it in `server/state_view.py`.

---

## The four architecture forks — resolved

These were the crux. Each is resolved below with Codex's independent read (fork-advice pass) noted; Codex agreed with the resolution on all four.

### Fork 1 — The long-running-job model

**Decision:** For mutating gate actions, a **per-run background job queue + a job-status polling endpoint** (`POST → 202 {job_id}` / `GET /jobs/{job_id}`), with a **single-writer-per-run guard**. **For the tracer-bullet, none of this is built** — `GET /runs/{id}/status` is read-only and instant.

**Why:** HTTP handlers cannot block for minutes (proxy/client timeouts, double-submits, no progress signal), and cascades make "one POST = one quick transition" false — `approve_plan_gate` can run Maya *and* Sam *and* Bea before returning. A "job" maps cleanly to one CLI invocation: **one gate action = advance to the next human gate.** Rejected alternatives: sync-with-polling (initiating request times out; cascades break it); bare FastAPI `BackgroundTasks` (in-process, opaque, no `pending/running/succeeded/failed`, no `rc`/logs, no per-run writer control).

**Single-writer guard:** a per-run lock in the job worker, rejecting a second mutating request with `409` + the active `job_id`. `save_state`'s tmp-write+`replace()` is atomic for *readers* (POSIX rename) but offers **no writer mutual-exclusion** — two POSTs can clobber. The read-only status slice needs no lock (a reader sees old-or-new complete JSON, never torn). **Ship the lock with the first POST gate, not before.**

**Honest limit on the lock (Codex red-team correction — my earlier "cross-process file lock" overclaimed).** A daemon-held `flock` only excludes *other lock-takers*. `pipeline/run.py` resumes and `save_state`s with **no lock** ([`run.py:268-335`](../../pipeline/run.py), [`state.py:107-114`](../../pipeline/orchestration/state.py)), and the daemon **cannot add a lock to `run.py`** — the pipeline must stay byte-identical. So the guarantee is precisely: **the file lock excludes daemon-job-vs-daemon-job; CLI-vs-daemon on the same run is NOT lock-protected and is governed by the fleet-ops "one owner" operational rule** (don't drive a run from the CLI while the daemon owns it). Promoting real cross-process safety would require a lock inside `pipeline/run.py` — a *separate pipeline PR*, explicitly out of this workstream's scope. State the guarantee at this exact strength in the code and the UI; do not imply CLI-vs-daemon mutual exclusion.

**Active-cascade overlay (Codex red-team, blocker-2 — a write-slice contract the status view must anticipate).** A cascading gate saves an *intermediate* stage mid-run — e.g. `approve_frame` saves `ASSEMBLE` ([`generate_stage.py:425`](../../pipeline/orchestration/generate_stage.py)) **before** assemble finishes. A GET during that window returns `next_action.kind == "assemble"` while assemble is already running — inviting a duplicate. **Resolution:** once the job layer exists (Slice 4), `status_view` gains an `active_job` field (`{job_id, mutation_status}`), and the daemon **suppresses/disables the mutating `next_action`** whenever a job owns the run. Slice 1 has no jobs, so `active_job` is absent and `next_action` is advisory-only; the field is reserved now so the projector's contract doesn't churn when writes land.

**Deferred to:** Slice 4 (job layer) + Slice 5 (POST gates). Designed here, unbuilt this session.

### Fork 2 — Sync-function → JSON-response adaptation

**Decision — split the two directions:**
- **Reads (GET):** call `state.load_state(run_dir)` in-process and project. Fast, pure, no model, no subprocess. This is the whole tracer-bullet.
- **Writes (POST, later):** the job worker drives the **existing CLI** as a subprocess — `python -m pipeline.run --resume <run_dir> --approve-*` — under the **fleet-ops env-strip** (`env -u CLAUDECODE -u CLAUDE_CODE_SESSION_ID …`), then on exit re-reads `load_state(run_dir)` for the result.

**Why subprocess-drives-CLI for writes (vs in-process import):** the daemon's thesis is "a face over the existing CLI." Driving the CLI means **zero logic duplication** — `run.py` already owns the api-key guard (`_api_key_guard`), the stage guards, the cascade, the `--stub` env contract, the manifest + criteria bundle wiring (`_resume_manifest_and_bundle`, seam #8), and the atomic save. It also gives **process isolation** (a gate crash can't take the daemon down), **trivial cancellation** (kill the subprocess), and — decisively — it resolves **fleet-ops seam #4 (the nested-SDK throttle)**: a gate function calling the Claude SDK from inside a long-lived daemon would inherit throttle markers; the env-strip on the subprocess is the exact documented remedy. In-process import is the alternative (faster, easier to stub) but would re-implement the guards and re-open seam #4 — rejected for the writer path.

**The wrapper contract (for the later write slices):**
```
1. Pre-check stage synchronously (mirror run.py's stage guards) → 409 if the action doesn't apply.
   This is advisory only — it can go stale before the worker runs (Codex red-team, should-fix 2).
2. Reserve the run's active-job slot ATOMICALLY, then return 202 {job_id}. A second POST to a run
   that already holds a job slot → 409 + the active job_id (the single-writer guard).
3. Worker: acquire the per-run file lock, then RE-CHECK the stage under the lock immediately before
   spawning (the step-1 precheck may have raced). Spawn
   `python -m pipeline.run --resume <run_dir> <action>` with cwd=<repo root>, under the env-strip.
   Capture stdout/stderr into the job record (the gates print human CLI text, not JSON).
4. On exit: re-read load_state(run_dir). A nonzero rc can still leave meaningful state
   (run_frame_fan records an errored attempt and saves before returning 1; assemble writes
   sequence_file before the node runs) — so re-read even on rc != 0. BUT the reload itself can fail
   (run dir deleted/corrupted mid-job): on StateError, report fresh_state=null + load_error rather
   than 500. Job result shape: {rc, logs, fresh_state | null, load_error?, next_action?}.
5. Release the lock + the job slot. The daemon NEVER calls save_state — the CLI is the sole writer.
```
**Retry maps to `retry_frame`, not raw `run_frame_fan`** (Codex, verified): `retry_frame` validates the current frame and resolves the `Shot`; `run_frame_fan` takes a `Shot` and is the wrong seam for the API. The endpoint map below reflects this.

### Fork 3 — `next_action` derivation

**Decision:** a small **pure projector** `server/state_view.py::next_action(state) -> dict` that returns a **machine token** `kind` plus the **verbatim CLI hint** for provenance: `{"kind": "...", "frame"?: n, "hint": state._next_hint(state)}`. `kind` is a tested projection over the same state fields `_next_hint` branches on (`stage`, `plan.status`, `script.status`, `storyboard.status`, `current_frame`). Reusing `_next_hint` for the human string avoids re-deriving the CLI text; the `kind` token is what the UI navigates by. Duplication risk is bounded: a test asserts the `(stage) → kind` mapping for **every** stage, and asserts the hint substring, so any drift in `state.py` breaks loudly.

**Note (accepted coupling):** the projector imports the private `state._next_hint`. This is a deliberate reuse of the pipeline's own "what to do next" logic — the design's core idea that *the run drives the app*. If `_next_hint` is later promoted to a public name, update the one import; the mapping test guards the rename.

`kind` values, one per stage branch:
| stage | condition | `kind` |
|---|---|---|
| PLAN | `plan.status == "drafted"` | `approve_plan` |
| PLAN | else | `planning` |
| SCRIPT | `script.status == "drafted"` | `approve_script` |
| SCRIPT | else | `scripting` |
| STORYBOARD | `storyboard.status == "drafted"` | `approve_storyboard` |
| STORYBOARD | else | `storyboarding` |
| ANIMATIC | — | `approve_animatic` |
| GENERATE | `current_frame is None` | `assemble` |
| GENERATE | current frame `status == "generated"` | `review_frame` (+ `frame`) |
| GENERATE | else | `generating` (+ `frame`) |
| ASSEMBLE | — | `assemble` |
| DONE | — | `done` |

### Fork 4 — Process / sidecar model

**Decision:** build the daemon **standalone** — `uvicorn server.app:app`, runnable and testable on its own, binding localhost, **single worker** (so the future in-memory job registry + per-run lock are authoritative). **Defer** the Electron/Tauri shell entirely. Record the **sidecar seam**: the desktop shell will later spawn this daemon as a subprocess and point a webview at it (Open Design's pattern); BYOK/local-files means the daemon reads the existing `.env`, `runs/`, `characters/`. Nothing in this plan blocks that; the app factory (`create_app`) already takes injectable settings so the shell can pass a runs-root.

---

## File structure

All new. One responsibility per file; files that change together live together.

```
server/
├── __init__.py            # package marker
├── app.py                 # create_app(settings) -> FastAPI; /health; mounts routers
├── config.py              # Settings(runs_root: Path); get_settings() reads ANIMA_RUNS_ROOT (default runs/)
├── runs.py                # resolve_run_dir(runs_root, run_id) -> Path | None  (traversal-safe)
├── state_view.py          # next_action(state) -> dict ; status_view(state) -> dict  (pure projectors)
└── routers/
    ├── __init__.py
    └── runs_router.py     # GET /runs/{run_id}/status  (Slice 1). GET /runs, GET /runs/{id}: Slice 2.

# Designed, NOT built this session (later slices):
# server/jobs.py           # job registry + per-run cross-process lock + subprocess CLI driver (Slice 4)
# server/models.py         # optional Pydantic response models if we want typed schemas (Slice 2+)
# server/artifacts.py      # file reads: plan/script/storyboard/brief, frame images/candidates (Slice 3)

tests/server/
├── __init__.py
├── conftest.py            # importorskip(fastapi/httpx); runs_root, client, make_run fixtures
└── test_status.py         # Slice 1 tracer-bullet: health, happy paths, next_action, 404, traversal, corrupt
```

**Why `tests/server/` (not `server/tests/`):** CLAUDE.md documents a duplicate-`tests`-package-basename collision when two dirs both ship `__init__.py`. Nesting under the existing `tests/` package avoids a second top-level `tests` package. A module-level `pytest.importorskip("fastapi")` in `conftest.py` keeps the main `tests/` run green even if FastAPI isn't installed in a given env.

**New dependencies** (add to the project's install list / `requirements`, documented in CHANGELOG): `fastapi`, `uvicorn[standard]`, `httpx` (TestClient transport). None imported by `pipeline/` — the byte-identical guarantee holds.

---

## Endpoint ↔ gate-function map

The full surface (from the source build plan), annotated with the resolved backing and the slice that builds it. **Only the first row ships this session.**

| Method | Endpoint | Backed by | Slice | Notes |
|---|---|---|---|---|
| `GET` | `/runs/{id}/status` | `load_state` + `state_view` | **1 (this session)** | read-only; the tracer-bullet |
| `GET` | `/health` | — | **1 (this session)** | liveness only; proves boot |
| `GET` | `/runs` | scan `runs/*/run_state.json` | 2 | read-only list |
| `GET` | `/runs/{id}` | `load_state` (passthrough) | 2 | read-only full state |
| `GET` | `/runs/{id}/artifacts/{plan\|script\|storyboard\|brief}` | files in `brief_dir` | 3 | read-only |
| `GET` | `/runs/{id}/frames/{n}/candidates` | `candidates/` + Em verdict | 3 | read-only |
| `GET` | `/runs/{id}/frames/{n}/image?attempt=K` | `candidates/`/`approved/` | 3 | read-only bytes |
| `POST` | `/runs/{id}/plan/approve` | CLI `--approve-plan` job | 5 | 202+job; cascades |
| `POST` | `/runs/{id}/script/approve` | CLI `--approve-script` job | 5 | 202+job |
| `POST` | `/runs/{id}/storyboard/approve` | CLI `--approve-storyboard` job | 5 | 202+job |
| `POST` | `/runs/{id}/animatic/approve` | CLI `--approve-animatic` job (+ rough upload) | 5 | 202+job |
| `POST` | `/runs/{id}/frames/{n}/approve` | CLI `--approve-frame N [--attempt K]` job | 5 | 202+job; cascades |
| `POST` | `/runs/{id}/frames/{n}/retry` | CLI `--retry-frame N --note …` job (`retry_frame`, **not** `run_frame_fan`) | 5 | 202+job |
| `POST` | `/runs/{id}/assemble` | CLI `--assemble` job | 5 | 202+job |
| `POST` | `/runs` | CLI `--brief …` job (+ brief upload) | 6 | 202+job |
| `GET` | `/jobs/{job_id}` | job registry | 4 | poll target for every POST |

---

## Slice 1 — Daemon skeleton + `GET /runs/{id}/status` (the tracer-bullet)

Fully spelled out. Each task ends with an independently testable deliverable, its own red→green→commit.

### Task 1 — Package skeleton + app factory + `/health`

**Files:**
- Create: `server/__init__.py` (empty)
- Create: `server/config.py`
- Create: `server/app.py`
- Create: `tests/server/__init__.py` (empty), `tests/server/conftest.py`, `tests/server/test_status.py`

**Interfaces produced:**
- `server/config.py`: `@dataclass(frozen=True) class Settings: runs_root: Path` ; `get_settings() -> Settings`
- `server/app.py`: `create_app(settings: Settings | None = None) -> FastAPI` ; module-level `app = create_app()`

- [ ] **Step 0: Install the daemon deps concretely** (Codex red-team, should-fix 5 — otherwise `importorskip` silently skips every server test and Task 7 false-greens). Add to the repo's install list (a `requirements-server.txt` or the documented `pip install` line in the README/CHANGELOG) and install into the working env:

```bash
python -m pip install fastapi "uvicorn[standard]" httpx
```

- [ ] **Step 1: Write the failing test** — `tests/server/conftest.py`:

```python
import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from pathlib import Path

from fastapi.testclient import TestClient

from pipeline.orchestration import state as st
from server.app import create_app
from server.config import Settings


def _cast() -> list[dict]:
    return [{
        "folder_key": "sean-anchor", "ir_namespace": "sean",
        "anchor": "characters/sean-anchor/anchor.png",
        "criteria": "characters/sean-anchor/acceptance_criteria.json",
    }]


@pytest.fixture
def runs_root(tmp_path) -> Path:
    root = tmp_path / "runs"
    root.mkdir()
    return root


@pytest.fixture
def client(runs_root) -> TestClient:
    return TestClient(create_app(Settings(runs_root=runs_root)))


@pytest.fixture
def make_run(runs_root):
    """Write a real run_state.json under runs_root; return (run_dir, state)."""
    def _make(run_id: str = "2026-07-02-demo-run", **overrides):
        s = st.new_state(
            run_id=run_id, brief_dir="brief", manifest_path="manifest.yaml",
            shots_path="brief/shots.yaml", slug="DEMO", stub=True, cast=_cast(),
        )
        for k, v in overrides.items():
            s[k] = v
        run_dir = runs_root / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        st.save_state(run_dir, s)
        return run_dir, s
    return _make
```

and in `tests/server/test_status.py`:

```python
def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
```

- [ ] **Step 2: Run it, verify RED** — `python -m pytest tests/server/test_status.py::test_health_ok -v` → FAIL (`ModuleNotFoundError: server`).

- [ ] **Step 3: Minimal implementation** — `server/config.py`:

```python
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    runs_root: Path


def get_settings() -> Settings:
    return Settings(runs_root=Path(os.environ.get("ANIMA_RUNS_ROOT", "runs")))
```

`server/app.py`:

```python
from __future__ import annotations

from fastapi import FastAPI

from server.config import Settings, get_settings
from server.routers import runs_router


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(title="anima daemon", version="0")
    app.state.settings = settings
    app.include_router(runs_router.router)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()
```

(Task 1 also creates `server/routers/__init__.py` and a minimal `server/routers/runs_router.py` with an empty `router = APIRouter()` so the import in `app.py` resolves; Task 3 fills the route in.)

- [ ] **Step 4: Verify GREEN** — `python -m pytest tests/server/test_status.py::test_health_ok -v` → PASS.

- [ ] **Step 5: Commit** — `git add server/ tests/server/ && git commit -m "feat(server): daemon skeleton + /health"`

### Task 2 — Traversal-safe run-dir resolver

**Files:** Create `server/runs.py`; Test in `tests/server/test_status.py`.
**Interfaces produced:** `resolve_run_dir(runs_root: Path, run_id: str) -> Path | None` — returns the run dir iff it exists and holds a `run_state.json`, else `None`; rejects any `run_id` containing a path separator, `..`, or a leading dot.

- [ ] **Step 1: Failing test**:

```python
from pathlib import Path
from server.runs import resolve_run_dir


def test_resolve_run_dir_found(make_run, runs_root):
    run_dir, _ = make_run("abc")
    assert resolve_run_dir(runs_root, "abc") == run_dir


def test_resolve_run_dir_missing(runs_root):
    assert resolve_run_dir(runs_root, "nope") is None


def test_resolve_run_dir_rejects_traversal(runs_root):
    for bad in ["../etc", "a/b", "..", ".hidden", "", "a\\b"]:
        assert resolve_run_dir(runs_root, bad) is None
```

- [ ] **Step 2: Verify RED** — `python -m pytest tests/server/test_status.py -k resolve_run_dir -v` → FAIL (`ModuleNotFoundError: server.runs`).

- [ ] **Step 3: Minimal implementation** — `server/runs.py`:

```python
from __future__ import annotations

from pathlib import Path

from pipeline.orchestration import state as st


def resolve_run_dir(runs_root: Path, run_id: str) -> Path | None:
    # Reject separators / dot-segments, then confirm the resolved path is a
    # DIRECT child of runs_root (traversal-proof, and not over-broad: a legit id
    # that merely contains ".." as characters is fine — only path segments matter).
    if not run_id or "/" in run_id or "\\" in run_id or run_id in (".", ".."):
        return None
    candidate = (runs_root / run_id)
    try:
        if candidate.resolve().parent != runs_root.resolve():
            return None
    except OSError:
        return None
    if (candidate / st.STATE_FILENAME).exists():
        return candidate
    return None
```

- [ ] **Step 4: Verify GREEN** — `python -m pytest tests/server/test_status.py -k resolve_run_dir -v` → PASS.

- [ ] **Step 5: Commit** — `git add server/runs.py tests/server/test_status.py && git commit -m "feat(server): traversal-safe run-dir resolver"`

### Task 3 — `next_action` projector (the state-machine → UI token)

**Files:** Create `server/state_view.py`; Test in `tests/server/test_status.py`.
**Interfaces produced:** `next_action(state: dict) -> dict` returning `{"kind": str, "hint": str}` and, in GENERATE, an added `"frame": int`.

- [ ] **Step 1: Failing test** (one assertion per stage branch — this is the anti-drift guard):

```python
from pipeline.orchestration import state as st
from server.state_view import next_action


def _base():
    return st.new_state(run_id="r", brief_dir="b", manifest_path="m",
                        shots_path="s", slug="X", stub=True, cast=[])


def test_next_action_plan_planning_then_approve():
    s = _base()
    assert next_action(s)["kind"] == "planning"       # plan.status == "pending"
    s["plan"]["status"] = "drafted"
    na = next_action(s)
    assert na["kind"] == "approve_plan"
    assert "--approve-plan" in na["hint"]             # provenance from _next_hint


def test_next_action_script_in_progress_then_approve():
    s = _base(); s["stage"] = "SCRIPT"
    assert next_action(s)["kind"] == "scripting"          # no script.status yet
    s["script"] = {"status": "drafted"}
    assert next_action(s)["kind"] == "approve_script"


def test_next_action_storyboard_in_progress_then_approve():
    s = _base(); s["stage"] = "STORYBOARD"
    assert next_action(s)["kind"] == "storyboarding"      # no storyboard.status yet
    s["storyboard"] = {"status": "drafted"}
    assert next_action(s)["kind"] == "approve_storyboard"


def test_next_action_animatic():
    s = _base(); s["stage"] = "ANIMATIC"
    assert next_action(s)["kind"] == "approve_animatic"


def test_next_action_generate_generating_review_then_assemble():
    s = _base(); s["stage"] = "GENERATE"; s["frame_order"] = [1]
    st.set_frame(s, 1, {"status": "pending", "attempts": []})
    assert next_action(s)["kind"] == "generating"         # frame not yet generated
    st.get_frame(s, 1)["status"] = "generated"
    na = next_action(s)
    assert na["kind"] == "review_frame" and na["frame"] == 1
    st.get_frame(s, 1)["status"] = "approved"
    assert next_action(s)["kind"] == "assemble"           # current_frame is None


def test_next_action_assemble_stage_and_done():
    s = _base(); s["stage"] = "ASSEMBLE"
    assert next_action(s)["kind"] == "assemble"
    s["stage"] = "DONE"
    assert next_action(s)["kind"] == "done"
```

- [ ] **Step 2: Verify RED** — `python -m pytest tests/server/test_status.py -k next_action -v` → FAIL (`ModuleNotFoundError: server.state_view`).

- [ ] **Step 3: Minimal implementation** — `server/state_view.py`:

```python
from __future__ import annotations

from pipeline.orchestration import state as st


def next_action(state: dict) -> dict:
    """Project run-state onto a machine token + the pipeline's own CLI hint.

    Reuses state._next_hint for the human string so the daemon never re-derives
    the pipeline's 'what to do next' logic. `kind` is the UI navigation token.
    """
    stage = state["stage"]
    hint = st._next_hint(state)
    if stage == "PLAN":
        kind = "approve_plan" if state["plan"]["status"] == "drafted" else "planning"
        return {"kind": kind, "hint": hint}
    if stage == "SCRIPT":
        drafted = state.get("script", {}).get("status") == "drafted"
        return {"kind": "approve_script" if drafted else "scripting", "hint": hint}
    if stage == "STORYBOARD":
        drafted = state.get("storyboard", {}).get("status") == "drafted"
        return {"kind": "approve_storyboard" if drafted else "storyboarding", "hint": hint}
    if stage == "ANIMATIC":
        return {"kind": "approve_animatic", "hint": hint}
    if stage == "GENERATE":
        n = st.current_frame(state)
        if n is None:
            return {"kind": "assemble", "hint": hint}
        rec = state["frames"].get(str(n), {})
        kind = "review_frame" if rec.get("status") == "generated" else "generating"
        return {"kind": kind, "frame": n, "hint": hint}
    if stage == "ASSEMBLE":
        return {"kind": "assemble", "hint": hint}
    return {"kind": "done", "hint": hint}
```

- [ ] **Step 4: Verify GREEN** — `python -m pytest tests/server/test_status.py -k next_action -v` → PASS.

- [ ] **Step 5: Commit** — `git add server/state_view.py tests/server/test_status.py && git commit -m "feat(server): next_action projector"`

### Task 4 — `status_view` projector

**Files:** Modify `server/state_view.py`; Test in `tests/server/test_status.py`.
**Interfaces produced:** `status_view(state: dict) -> dict` → `{run_id, stage, stub, plan_status, next_action, frames[], updated_at}` where each `frames[]` item is `{n, status, attempts, hold}`.

- [ ] **Step 1: Failing test**:

```python
from server.state_view import status_view


def test_status_view_shape_plan_stage():
    s = _base()
    view = status_view(s)
    assert view["run_id"] == "r"
    assert view["stage"] == "PLAN"
    assert view["stub"] is True
    assert view["plan_status"] == "pending"
    assert view["next_action"]["kind"] == "planning"
    assert view["frames"] == []


def test_status_view_frames_projection():
    s = _base(); s["stage"] = "GENERATE"; s["frame_order"] = [1, 2]
    s["holds"] = {"1": 3}
    st.set_frame(s, 1, {"status": "approved", "attempts": [{"index": 1}, {"index": 2}]})
    st.set_frame(s, 2, {"status": "generated", "attempts": [{"index": 1}]})
    frames = status_view(s)["frames"]
    assert [f["n"] for f in frames] == [1, 2]
    assert frames[0] == {"n": 1, "status": "approved", "attempts": 2, "hold": 3}
    assert frames[1]["status"] == "generated" and frames[1]["hold"] == 2  # default hold
```

- [ ] **Step 2: Verify RED** — `python -m pytest tests/server/test_status.py -k status_view -v` → FAIL (`AttributeError: status_view`).

- [ ] **Step 3: Minimal implementation** — append to `server/state_view.py`:

```python
def status_view(state: dict) -> dict:
    frames = []
    for n in state.get("frame_order", []):
        rec = state["frames"].get(str(n), {})
        frames.append({
            "n": n,
            "status": rec.get("status", "pending"),
            "attempts": len(rec.get("attempts", [])),
            "hold": st.get_hold(state, n),
        })
    return {
        "run_id": state["run_id"],
        "stage": state["stage"],
        "stub": bool(state.get("stub")),
        "plan_status": state["plan"]["status"],
        "next_action": next_action(state),
        "frames": frames,
        "updated_at": state.get("updated_at"),
    }
```

- [ ] **Step 4: Verify GREEN** — `python -m pytest tests/server/test_status.py -k status_view -v` → PASS.

- [ ] **Step 5: Commit** — `git add server/state_view.py tests/server/test_status.py && git commit -m "feat(server): status_view projector"`

### Task 5 — `GET /runs/{id}/status` endpoint (happy path)

**Files:** Modify `server/routers/runs_router.py`; Test in `tests/server/test_status.py`.
**Interfaces produced:** `GET /runs/{run_id}/status` → `200` with the `status_view` body.

- [ ] **Step 1: Failing test** (via `TestClient` against a real fixture state):

```python
def test_status_happy_path_plan(client, make_run):
    make_run("2026-07-02-demo-run")
    r = client.get("/runs/2026-07-02-demo-run/status")
    assert r.status_code == 200
    body = r.json()
    assert body["run_id"] == "2026-07-02-demo-run"
    assert body["stage"] == "PLAN"
    assert body["next_action"]["kind"] == "planning"
    assert body["frames"] == []


def test_status_reflects_generate_progress(client, make_run, runs_root):
    run_dir, s = make_run("gen-run")
    s["stage"] = "GENERATE"; s["frame_order"] = [1, 2]
    st.set_frame(s, 1, {"status": "approved", "attempts": [{"index": 1}]})
    st.set_frame(s, 2, {"status": "generated", "attempts": [{"index": 1}]})
    st.save_state(run_dir, s)
    body = client.get("/runs/gen-run/status").json()
    assert body["next_action"]["kind"] == "review_frame"
    assert body["next_action"]["frame"] == 2
    assert [f["n"] for f in body["frames"]] == [1, 2]
```

- [ ] **Step 2: Verify RED** — `python -m pytest tests/server/test_status.py -k "status_happy_path or generate_progress" -v` → FAIL (404, route not implemented).

- [ ] **Step 3: Minimal implementation** — `server/routers/runs_router.py`:

```python
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from pipeline.orchestration import state as st
from server.runs import resolve_run_dir
from server.state_view import status_view

router = APIRouter(prefix="/runs", tags=["runs"])


@router.get("/{run_id}/status")
def get_status(run_id: str, request: Request) -> dict:
    run_dir = resolve_run_dir(request.app.state.settings.runs_root, run_id)
    if run_dir is None:
        raise HTTPException(status_code=404, detail=f"no run {run_id!r}")
    try:
        state = st.load_state(run_dir)
        return status_view(state)
    except st.StateError as e:
        # missing file / unparseable JSON / bad schema_version
        raise HTTPException(status_code=422, detail=str(e))
    except (KeyError, TypeError) as e:
        # load_state does NOT validate object shape (state.py:89-104); a parseable
        # but malformed state makes the projector raise. Map to 422, not 500.
        raise HTTPException(status_code=422, detail=f"malformed run_state.json: {e}")
```

- [ ] **Step 4: Verify GREEN** — `python -m pytest tests/server/test_status.py -k "status_happy_path or generate_progress" -v` → PASS.

- [ ] **Step 5: Commit** — `git add server/routers/runs_router.py tests/server/test_status.py && git commit -m "feat(server): GET /runs/{id}/status tracer-bullet"`

### Task 6 — Error paths: 404 unknown, 404 traversal, 422 corrupt

**Files:** Test-only in `tests/server/test_status.py` (impl already covers these via Task 2 + Task 5).

- [ ] **Step 1: Failing/【confirming】test**:

```python
def test_status_unknown_run_404(client):
    assert client.get("/runs/does-not-exist/status").status_code == 404


def test_status_traversal_404(client):
    # Starlette normalizes many dot-segments; this asserts we never 200 on traversal.
    assert client.get("/runs/..%2f..%2fetc/status").status_code == 404


def test_status_corrupt_state_422(client, runs_root):
    run_dir = runs_root / "corrupt"
    run_dir.mkdir(parents=True)
    (run_dir / "run_state.json").write_text("{ not json", encoding="utf-8")
    r = client.get("/runs/corrupt/status")
    assert r.status_code == 422
    assert "run_state.json" in r.json()["detail"]


def test_status_malformed_shape_is_422_not_500(client, runs_root):
    # load_state accepts this (valid JSON + schema_version==1) but it lacks
    # 'stage'/'plan'/'frames' — the projector must 422, never 500.
    run_dir = runs_root / "malformed"
    run_dir.mkdir(parents=True)
    (run_dir / "run_state.json").write_text('{"schema_version": 1}', encoding="utf-8")
    r = client.get("/runs/malformed/status")
    assert r.status_code == 422
    assert "malformed" in r.json()["detail"]
```

- [ ] **Step 2: Run** — `python -m pytest tests/server/test_status.py -k "unknown_run or traversal or corrupt_state or malformed_shape" -v`. Expected PASS (impl exists from Tasks 2 + 5). If the traversal test does **not** 404 (framework URL-decoding surprise), tighten `resolve_run_dir` — do not relax the assertion.

- [ ] **Step 3: Gate-decoupling test** (Codex independent-plan addition — proves the read path never touches a gate function, so no model can run):

```python
def test_status_never_calls_a_gate(client, make_run, monkeypatch):
    import pipeline.orchestration.generate_stage as gs
    import pipeline.orchestration.plan_stage as ps

    def _explode(*a, **k):
        raise AssertionError("a gate function was called from the read path")

    monkeypatch.setattr(gs, "run_frame_fan", _explode, raising=False)
    monkeypatch.setattr(ps, "run_plan_stage", _explode, raising=False)
    make_run("decoupled")
    assert client.get("/runs/decoupled/status").status_code == 200
```

- [ ] **Step 4: Verify GREEN** — `python -m pytest tests/server/test_status.py -v` → all PASS (the whole tracer-bullet suite).

- [ ] **Step 5: Commit** — `git add tests/server/test_status.py && git commit -m "test(server): status error paths + gate-decoupling"`

### Task 7 — Verification gate: parallel-safe + byte-identical + full suite

Per superpowers:verification-before-completion — evidence before any "done."

- [ ] **Step 1: The daemon touched nothing in the pipeline.** Run and read the output:
```
git status --porcelain            # only server/, tests/server/, docs, CHANGELOG, deps manifest
git diff --stat main -- pipeline/ evals/   # expect: no output (byte-identical)
```
- [ ] **Step 2: The two md5 guards held:**
```
md5 -q evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md   # 2af75906502f1caf8857e18828ceb2e4
md5 -q pipeline/agents/prompts/sean-screenwriting-voice.md                # 945af824fa53b948a18ac6bf206d67ef
```
(`md5sum` on Linux; the CI form is `md5sum <file>`.)
- [ ] **Step 3: Full existing suite green + new suite green — and prove the server suite actually RAN (not skipped):**
```
python -m pytest tests/            # ~562 existing + new tests/server/, all pass
python -m pytest pipeline/tests/   # separate per the duplicate-basename rule
# Guard against the importorskip false-green (Codex red-team, should-fix 5):
# assert the tracer-bullet tests were collected & ran, not skipped for a missing dep.
python -m pytest tests/server/ -v -rsx | tee /tmp/server-tests.log
grep -q "skipped" /tmp/server-tests.log && echo "FAIL: server tests skipped — install deps (Task 1 Step 0)" || echo "OK: server tests ran"
```
- [ ] **Step 4: The daemon boots and serves a real run (manual smoke, no model):**
```
ANIMA_RUNS_ROOT=runs uvicorn server.app:app --port 8973 &
curl -s localhost:8973/health
curl -s localhost:8973/runs/<a-real-run-id>/status | python -m json.tool
kill %1
```
- [ ] **Step 5: CHANGELOG entry** (per CLAUDE.md maintenance convention) — what/why: the daemon foundation + tracer-bullet, new `server/` package, new deps, the parallel-safe/byte-identical proof. **Stop green for Sean's review** — do not start Slice 2.

---

## Later slices — titled stubs (designed, not built this session)

- **Slice 2 — read-only run listing + full state.** `GET /runs` (scan `runs/*/run_state.json`, project id/stage/slug/updated_at) + `GET /runs/{id}` (raw `load_state` passthrough). Still read-only, still no async. Optional Pydantic models in `server/models.py`.
- **Slice 3 — read-only artifacts + images.** `GET /runs/{id}/artifacts/{plan|script|storyboard|brief}` (markdown/yaml from `brief_dir`), `GET /runs/{id}/frames/{n}/candidates` (+ Em verdict), `GET /runs/{id}/frames/{n}/image?attempt=K` (bytes). All read-only; traversal-guard every path param.
- **Slice 4 — the job layer.** `server/jobs.py`: an in-memory job registry (`pending/running/succeeded/failed`, `rc`, captured stdout/stderr, `fresh_state | null`, `load_error?`), a **per-run file lock** (daemon-vs-daemon only — see Fork 1's honest-limit note), and a subprocess driver that runs `python -m pipeline.run --resume …` with `cwd=<repo root>` under the fleet-ops env-strip (never `--allow-api-key`). `GET /jobs/{job_id}`, and `status_view` gains an `active_job` field. **Test seam:** the driver is an injectable callable (default = real subprocess); tests inject a stub driver that mutates a fixture state + returns `rc` — no real process, no spend.
- **Slice 5 — POST gate actions.** The eight write endpoints over the job layer, per the wrapper contract in Fork 2: advisory stage pre-check → 409; **atomically reserve the active-job slot** → 202 `{job_id}` (second POST to a run holding a slot → 409 + active `job_id`); the worker re-checks the stage **under the lock** before spawning (the precheck can go stale); on completion re-read `load_state` (even on `rc != 0`), reporting `load_error` if the reload itself fails; **suppress the mutating `next_action` while a job owns the run** (the active-cascade overlay). Retry uses `--retry-frame`/`retry_frame`, not `run_frame_fan`.
- **Slice 6 — run creation + brief upload.** `POST /runs` (brief upload → `python -m pipeline.run --brief …` job). `GET /characters`, `GET /runs/{id}/cost-estimate`.
- **Deferred beyond the daemon:** the Electron/Tauri sidecar shell and the v1 UI (`frontend-design` + `impeccable`), per Fork 4.

---

## Testing strategy

- **Transport:** Starlette `TestClient` (needs `httpx`). App built per-test via `create_app(Settings(runs_root=tmp_path/"runs"))` so every test is hermetic against a temp runs-root — no reliance on the repo's real `runs/`.
- **Fixtures:** `make_run` writes a genuine `run_state.json` through `state.new_state()` + `state.save_state()` — the exact production writer, so the daemon reads real shapes, not hand-rolled JSON. This mirrors `tests/test_run_state.py`.
- **Credential-free by construction:** Slice 1 calls no gate function; later slices inject a stub driver into the job worker. `pytest.importorskip("fastapi")`/`("httpx")` keeps the main suite green where the deps are absent.
- **Coverage per slice:** happy path + every `next_action` branch + 404 (unknown, traversal) + 422 (corrupt state). Later write slices add: 409 (wrong stage), 409 (in-flight-job single-writer), and the "re-read on `rc != 0`" partial-state case.
- **Run command:** `python -m pytest tests/server/` (and the whole `tests/` suite for the regression guard).

---

## Risks

1. **`_next_hint` is a private coupling.** The projector imports `state._next_hint`. *Mitigation:* the per-stage `next_action` mapping test breaks loudly on any rename; the coupling is deliberate (reuse the pipeline's own next-action logic). *If it churns often, promote `_next_hint` to public in a separate pipeline PR — out of scope here.*
2. **The projector can raise on a parseable-but-malformed state** (`load_state` validates JSON + `schema_version` but **not** object shape). *Mitigation (built, not hypothetical):* Task 5's router catches `KeyError`/`TypeError` → 422, and Task 6's `test_status_malformed_shape_is_422_not_500` proves a `{"schema_version":1}`-only file returns 422, never 500.
3. **New dependencies (`fastapi`/`uvicorn`/`httpx`) in a repo that's been pipeline-only.** *Mitigation:* `importorskip` guards collection; deps documented in CHANGELOG; none imported by `pipeline/`.
4. **"Parallel-safe" is only true for reads.** Overstating it invites an unguarded POST later. *Mitigation:* this doc scopes the claim to the read slice and blocks writes behind the single-writer lock (Fork 1).
5. **Traversal / URL-decoding surprises** in path params across framework versions. *Mitigation:* `resolve_run_dir` rejects separators/`..`/leading-dot **and** requires the state file to exist; a dedicated traversal test asserts non-200.
6. **(later) Cross-process writer race** — CLI and daemon both driving one run. *Mitigation:* the Slice-4 cross-process file lock + the fleet-ops "one owner" rule; documented, not this session's code.
7. **(later) `pipeline.run` assumes repo-root CWD + relative manifest paths** (Codex, verified — `run.py`'s docstring: "Run from the repo root; manifest, assemble.sh, and Em's context files resolve CWD-relative"). *Mitigation:* the Slice-4 subprocess driver must set `cwd=<repo root>` (matching fleet-ops §6 "background commands must `cd` explicitly"); the read-only status slice is CWD-independent (it only touches `runs_root/<id>/run_state.json`). *Also (Codex sharpening):* the job driver **never** passes `--allow-api-key` — make an API-billed daemon job impossible, not merely defaulted-off.

---

## Codex reconciliation notes

Three Codex passes informed this plan: a fork-advice pass, an independent-plan pass (`codex exec`, gpt-5.5), and an adversarial-review pass. Agreements, disagreements, and my calls below.

**Independent-plan pass (Codex) — strong convergence.** Codex's from-scratch plan landed on the **same architecture** with no material disagreement:
- **Same `server/` decomposition** (config/app/runs + a pure status projector + a routers module; `jobs.py`/`actions.py` deferred). Codex named the projector `status.py`; I named it `state_view.py` — cosmetic; I kept mine.
- **Same async model:** "daemon-local async job registry with per-run locks, but execute each mutating action as a `python -m pipeline.run …` subprocess, with `ANTHROPIC_API_KEY` stripped/refused." Identical to Fork 1 + Fork 2.
- **Same `next_action`:** `{token, cli_hint}` where `cli_hint` comes from `_next_hint` and the token is a thin normalization — identical to Fork 3. Codex explicitly would "not duplicate the state machine in `server/`" and would "not add a public helper to `pipeline/orchestration/state.py` yet, because `pipeline/` must remain byte-identical" — both are this plan's calls.
- **Same top risks:** private `_next_hint`, token/wording drift, cascades mutating more than one field, CLI/daemon race, repo-root-CWD assumption.
- **Two additions adopted:** (a) a **gate-decoupling test** — monkeypatch the gate functions to explode and assert `/status` still returns 200 (now Task 6, Step 3); (b) the **repo-root-CWD risk** for the later subprocess driver (now Risk 7). Also adopted its sharpening that an API-billed daemon job should be **impossible**, not overrideable (Risk 7).
- **Codex's stated disagreements were with a naive wrapper, not with this plan** — it "would not call gate functions in-process," "would not build POSTs in Slice 1 even stubbed," which this plan already honors. **No unresolved disagreement.**

**Fork-advice pass (Codex) — agreements & sharpenings already folded in:**
- Confirmed all four fork resolutions (background-job model for writes / none for the tracer-bullet; re-read-not-rewrite wrapper; reader-safe/writer-unsafe race analysis; status is the smallest safe slice).
- **Sharpenings adopted:** re-read `load_state` even on `rc != 0` (partial state is meaningful); retry → `retry_frame` not `run_frame_fan`; a per-run writer guard; capture stdout/stderr into the job record.
- **Source-doc corrections adopted:** gate functions do **not** print `render_status` (they print their own CLI text); `render_status`/`_next_hint` return **strings**, so the JSON shape is daemon-built; "parallel-safe" applies to reads only.

**Adversarial-review pass (Codex) — verdict + fixes folded in.** Codex confirmed the read-only slice is sound ("GET-only is the smallest safe slice: atomic rename means no torn reads, no gate/model path invoked"; `tests/server/` is the right layout for the duplicate-package hazard; md5 discipline adequate *if Task 7 is actually run*). Findings, with my calls:
- **Blocker — the "cross-process file lock" overclaimed.** A daemon lock can't exclude the CLI, and I can't add a lock to `run.py` (byte-identical). **Corrected:** Fork 1 now scopes the lock to daemon-vs-daemon and puts CLI-vs-daemon under the fleet-ops one-owner operational rule; real cross-process safety is a separate pipeline PR, out of scope. *(This was the single most important catch.)*
- **Blocker — future status exposes a clickable action mid-cascade** (`approve_frame` saves `ASSEMBLE` before assemble finishes). **Corrected:** Fork 1 reserves an `active_job` overlay + suppresses the mutating `next_action` while a job owns the run (Slice 4/5); the field is declared now so the projector contract doesn't churn.
- **Should-fix — factual error: `load_state` is not shape-checked.** **Corrected** in the premise + Task 5 (`KeyError`/`TypeError`→422) + Task 6 (`test_status_malformed_shape_is_422_not_500`).
- **Should-fix — Slice-1 `next_action` tests didn't cover every branch.** **Corrected:** Task 3 now tests `scripting`, `storyboarding`, `generating`, and the `ASSEMBLE`-stage mapping.
- **Should-fix — dependency verification can false-green via `importorskip`.** **Corrected:** Task 1 Step 0 installs the deps concretely; Task 7 Step 3 fails (not skips) if the server suite was skipped.
- **Should-fix — write-slice precheck races the worker; `rc!=0` reload can itself fail.** **Corrected** in Fork 2's wrapper contract (atomic slot reservation + re-check under lock; `load_error` branch).
- **Nit — `resolve_run_dir`'s `".."`-substring check is over-broad.** **Corrected:** Task 2 now rejects path *segments*/separators and confirms the resolved path is a direct child of `runs_root`.
- **No disagreement stands unresolved.** Every blocker/should-fix is either fixed in Slice 1 or recorded as an explicit write-slice constraint.
