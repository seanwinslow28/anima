# Daemon Slice 4 — the job layer: implementation-pattern research

**Date:** 2026-07-08 · **For:** the Fable-5 build of ② daemon Slice 4 (subprocess job driver + registry + lock + `202`/poll + cancel). · **Status:** research complete, feeds the kickoff.

The architecture forks (Fork 1 background-job model, Fork 2 subprocess-drives-CLI, the 5-step wrapper contract, the flock scoped daemon-vs-daemon only) were **already decided and Codex-red-teamed** in [`2026-07-02-daemon-build-plan-CONVERGED.md`](../active/2026-07-02-daemon-build-plan-CONVERGED.md). This note pins the *concrete implementation patterns* underneath those forks — the part the plan left open — plus the exact `pipeline.run` CLI contract the driver must honor. Two parallel research passes: the internal CLI-contract extraction and an external (web-cited) patterns pass.

---

## Part A — the `python -m pipeline.run` subprocess contract (internal, code-verified)

The driver shells out to the existing CLI (never `import main` — `main()` mutates/restores `os.environ[ANIMA_FORCE_STUB]` in-process and only `sys.exit`s under `__main__`). Verified against `pipeline/run.py` + the `orchestration/*_stage.py` modules.

**Invocation shape.** `[sys.executable, "-m", "pipeline.run", "--resume", <run_dir>, *action_args]`, `cwd=<repo root>`. The driver supplies the wrapper; **Slice 5 supplies `action_args`** per gate. One `--resume` action per call (the 8 are counted manually, not an argparse mutex; `sum != 1` → rc 2).

**The action → required stage map (no reusable predicate exists — replicate it):**

| Action args | Requires `state["stage"]` |
|---|---|
| `--approve-plan` | `PLAN` |
| `--approve-script` | `SCRIPT` |
| `--approve-storyboard` | `STORYBOARD` |
| `--approve-animatic` | `ANIMATIC` |
| `--approve-frame N [--attempt K]` | `GENERATE` |
| `--retry-frame N --note "…"` (note **required**, else rc 2) | `GENERATE` |
| `--assemble` | `ASSEMBLE` |
| `--status` | any (no guard; $0, no model) |

`run.py:282-321` hand-codes these six `state["stage"] != "…"` checks. A **second guard** re-checks sub-status at the real gate (`plan.status=="drafted"`, `animatic.status=="awaiting"`, …), so the daemon's stage pre-check is a *superset* pre-filter — the gate can still reject with rc 2.

**Exit codes — and the load-bearing "re-read state even on rc≠0" cases:**
- **0** = success. **2** = pure pre-checks that saved *nothing* (arg-count, stage-guard mismatch, `--retry-frame` w/o `--note`, `load_state` StateError, "nothing to approve"). Safe to treat rc 2 as an advisory conflict.
- **1** = ran and failed, and **may have durably saved state**:
  - a frame that **errored during the fan** → `run_frame_fan` appends an honest errored attempt and `save_state`s at `generate_stage.py:235` **before** `return 1`.
  - an **assemble failure** → `run_assemble_stage` writes `sequence_file` + `save_state`s at `assemble_stage.py:46` **before** the FFmpeg node runs, stage stays `ASSEMBLE`, `return 1`.
  - the **api-key guard** (rc 1, `run.py:141`), live-smoke `GuardError` (rc 1), stub-marker scan trip (rc 1) — no state change.
  - **⇒ The worker MUST re-read `run_state.json` after *any* rc.** And the reload itself can fail (dir deleted/corrupted mid-job) → report `fresh_state=null` + `load_error`, never a 500.

**The mid-cascade intermediate save (Codex blocker-2, confirmed):** approving the **last** frame flips the stage to `ASSEMBLE` and `save_state`s at `generate_stage.py:425-426`, *then* assembly runs in the same process. A GET during that window reads `stage: ASSEMBLE` while assemble is already in flight → a naive UI would offer a duplicate `--assemble`. **This is why `status_view` needs `active_job`** and the mutating `next_action` must be suppressed while a job owns the run (the field lands in Slice 4; the suppression is Slice 5).

**No lock anywhere in the pipeline.** `save_state` is atomic *for readers* (`tmp.replace()`, `state.py:107-114`) — no torn reads — but offers **no writer mutual-exclusion**. Two writers clobber. Single-writer is entirely the daemon's job.

**Billing / env (fleet-ops, baked into the real driver):**
- `_api_key_guard` (`run.py:133-142`) refuses rc 1 if `ANTHROPIC_API_KEY` is set unless `--allow-api-key`. **The driver must NEVER pass `--allow-api-key`** — an API-billed daemon job must be *impossible*, not merely defaulted-off.
- **Repo-root CWD is assumed and documented** (`run.py:26-27`): manifest, `assemble.sh`, Em context files all resolve CWD-relative. Set `cwd=<repo root>`. The daemon's existing convention (`artifacts.py`) is **repo_root == `runs_root.parent`** — reuse it; an explicit `repo_root` setting is a follow-on only if `runs_root` ever relocates away from repo-root.

---

## Part B — implementation patterns (external, web-cited)

### Q1 · Async subprocess vs thread-pool vs BackgroundTasks → **dedicated worker thread**
Return `202` synchronously; run each job on a `threading.Thread(daemon=True)` calling an injectable driver. **Not** `BackgroundTasks` (runs *after* the response but in-process on the event loop, "can tie up the main event loop," and gives no handle / no status / no cancel — the three things we need). **Not** the async-subprocess path as primary (binds the job to the loop, forces an async stub, and carries the [strong-reference GC footgun](https://dev.to/kaushikcoderpy/python-background-tasks-asyncio-traps-fastapi-celery-2026-381i)). A thread is the natural home for the blocking `flock` + `Popen` pair and is trivially stubbable. Refs: [FastAPI concurrency](https://fastapi.tiangolo.com/async/), [FastAPI BackgroundTasks](https://fastapi.tiangolo.com/tutorial/background-tasks/), [Discussion #11210](https://github.com/fastapi/fastapi/discussions/11210).

### Q2 · In-memory registry → **module/`app.state` `dict` + one `threading.Lock`**
`dict[job_id, Job]`, guarded by a single `threading.Lock` held *only* around dict read/writes. Single-worker + GIL makes individual dict ops atomic, but our status transitions are **read-modify-write / check-then-act, which are explicitly NOT atomic** — so the lock is necessary and sufficient. Don't hold the lock during I/O (the subprocess run) or you serialize GET polls behind the job. In-memory = process-lifetime only: a daemon restart loses records + orphans children (accepted). Refs: [Python thread-safety guarantees](https://docs.python.org/3/library/threadsafety.html), [Real Python: thread lock](https://realpython.com/python-thread-lock/).

### Q3 · Single-writer 409 → **compare-and-set in ONE locked section**
Under the lock: if the run already has a non-terminal job → return the active `job_id` for a 409; else create the `pending` record and set `active_by_run[run_id]` **before releasing the lock**, then start the thread. Reserving and starting in *separate* lock acquisitions reopens the TOCTOU race. Make slot-clear idempotent (`pop(run_id, None)` — worker-completion and cancel can both fire). This in-process slot is the single-writer guard *within* the one daemon; flock is the cross-process backstop, not a substitute. Refs: [Python thread-safety (check-then-act)](https://docs.python.org/3/library/threadsafety.html).

### Q4 · `fcntl.flock` → **`LOCK_EX | LOCK_NB` on a per-run lock file, in the worker**
Catch `OSError` and check `errno in (EACCES, EAGAIN)` ("check both for portability") → treat as "another daemon owns this run." Hold the fd open for the job's life; auto-releases when the fd closes / the process dies (tied to the open file description) — so a crashed daemon frees it. **Honest limits (state them at this exact strength in code + UI):** flock is **advisory** — it only excludes cooperating processes that *also* take the lock; **the pipeline CLI never takes it, so CLI-vs-daemon on the same run is NOT protected** (that stays the fleet-ops "one owner" operational rule). No deadlock detection; unreliable over NFS; on some systems it's emulated via `fcntl()` so don't mix the two on one file. macOS: lock-release-on-close has a subtle timing caveat but is fine here. Refs: [Python `fcntl`](https://docs.python.org/3/library/fcntl.html), [flock(2)](https://man7.org/linux/man-pages/man2/flock.2.html), [allenap.me flock macOS/Linux](https://allenap.me/posts/flock-behaviour).

### Q5 · Cancellation of a tree we can't `setsid` → **psutil tree-walk (an honest tradeoff, not a clean win)**
The constraint (fleet-ops §5): the CLI child must stay a **reap-able child** of the daemon — so no `start_new_session=True`/`setsid`, which means no clean `os.killpg` on a dedicated group. Given that, the standard answer is `psutil`: from the child pid, `children(recursive=True)` → `terminate()` (SIGTERM) parent+children → `wait_procs(timeout=…)` → `kill()` (SIGKILL) survivors. SIGTERM-then-grace-then-SIGKILL lets the `claude`/`agy` SDK grandchildren flush before the hammer.
- **The tradeoff, stated plainly:** killing only the direct `Popen` child does **not** cascade — grandchildren orphan and keep burning tokens. The psutil walk handles the tree *without* `setsid`, at the cost of an inherent **snapshot race** (a grandchild spawned between snapshot and kill can slip through) and PID-reuse risk.
- **Mitigations:** keep the psutil `Process` handles in the job record (don't re-discover pids); signal the parent then re-scan once; act on live handles and catch `NoSuchProcess`; ensure the daemon `wait()`s the child so no zombies.
- **Dependency call:** this adds `psutil`. If Sean wants to avoid a new dep in `server/`, the fallback is "kill the direct child + document that in-flight SDK grandchildren may finish" — weaker but dependency-free. **Kickoff carries this as an explicit decision point.** Refs: [subprocess `terminate`/`kill`](https://docs.python.org/3/library/subprocess.html), [psutil `kill_proc_tree`](https://psutil.readthedocs.io/), [SuperFastPython: kill child processes](https://superfastpython.com/kill-all-child-processes-in-python/).

### Q6 · Capture without deadlock → **redirect child stdout+stderr to a run-dir logfile, then `wait()`**
Don't hand-roll `proc.stdout.read()` loops. The classic deadlock: `wait()` with `stdout=PIPE`/`stderr=PIPE` hangs when the child fills the ~64KB pipe buffer. Two safe routes: (a) `Popen(stdout=logfile, stderr=logfile)` + `wait()` — **preferred here** because a poller can *tail the file for live logs while the job runs*; (b) `communicate()` (reads both pipes to EOF concurrently) — but it only returns when the process *ends*, so no live progress. If ever streaming from PIPEs, read stdout+stderr on separate threads (or `stderr=STDOUT`). Files also bound memory for minutes-long output. Refs: [subprocess deadlock warning + `communicate`](https://docs.python.org/3/library/subprocess.html), [Computing Arts: subprocess deadlock](https://computingarts.com/posts/2026-03-16-python-subprocess-hangs-deadlock-fix/).

### Q7 · Deterministic testing → **sync `TestClient` + injected stub driver, poll registry to terminal (no sleeps)**
Abstract the subprocess behind a `Driver` protocol (`run(run_dir, action_args) -> RunResult(rc, stdout, stderr)`); real driver does Popen/flock, **stub driver** is synchronous (or gated on a `threading.Event`). Inject it the way the codebase already injects `Settings` — as a `create_app(settings, *, driver=...)` arg (the repo doesn't use `dependency_overrides` today; match its constructor-injection idiom). Drive the lifecycle with the sync `TestClient` and **poll `GET /jobs/{id}` in a bounded loop until terminal** — never `time.sleep`. Lifecycle coverage: `pending→running→succeeded`; **409** (stub holds the run busy via an un-set Event, 2nd submit → 409 + active job_id, then release); **cancel** (event-gated stub exposes a `killed` flag, POST cancel → terminal `cancelled` + kill invoked). Refs: [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/), [testing dependencies](https://fastapi.tiangolo.com/advanced/testing-dependencies/), [Issue #1205](https://github.com/fastapi/fastapi/issues/1205).

**Real-driver smoke (credential-free, $0):** `--status` spawns a real `pipeline.run` subprocess that only reads state and prints — no model, no spend, rc 0. It's the one real end-to-end proof the driver's env-strip + `cwd` + capture + rc plumbing actually works, and it can live in the verification gate. The stub covers every *mutating* path.

---

## The recommended stack for Slice 4 (synthesis)

`server/jobs.py`: an in-memory `dict` **JobRegistry** on `app.state.jobs`, one `threading.Lock`. `submit(run_dir, action_args)` does the **atomic check-then-set** of a per-run active-job slot under the lock, records a `pending` `Job`, and hands it to a `daemon=True` worker thread. The worker: take the per-run **`flock(LOCK_EX|LOCK_NB)`** (→ conflict on `EACCES`/`EAGAIN`), then the injectable **driver** `Popen`s the CLI (`cwd=repo_root`, fleet-ops env-strip, **never `--allow-api-key`**) with stdout+stderr → a run-dir logfile, `wait()`s, then **re-reads `load_state` even on rc≠0** (→ `fresh_state|null` + `load_error?`), releases the flock + slot (idempotent). `Job` fields: `job_id, run_id, state(pending|running|succeeded|failed|cancelled), rc, logs, fresh_state|null, load_error?, next_action?`. Surface: `GET /jobs/{job_id}` (projection) + `POST /jobs/{job_id}/cancel` (psutil tree-kill). `status_view` gains **`active_job`** (`{job_id, mutation_status}` or absent), fed from the registry by the `get_status` router. Cancellation uses the **psutil terminate→wait→kill tree-walk** (the honest no-`setsid` answer). Everything mutating is tested through an **injected stub driver**; `--status` is the one real-subprocess $0 smoke.

**Slice 4 ships:** the mechanism + `/jobs` read/cancel surface + `active_job` on status. **Slice 4 does NOT ship:** the 8 `/runs/{id}/<gate>` POST endpoints, nor the `next_action` suppression — those are **Slice 5**, built on this layer.
