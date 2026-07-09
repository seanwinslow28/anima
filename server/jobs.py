"""Slice 4 — the job layer: in-memory registry + injectable driver.

Every future write (gate approve/retry, run-create — Slice 5/6) rides on this:
submit() reserves a per-run single-writer slot and hands the action to a
daemon worker thread; the driver runs `python -m pipeline.run --resume …` as a
subprocess (tests inject a synchronous stub — no real process, no spend). The
registry is process-lifetime only: a daemon restart loses job records
(accepted, per the converged plan's Fork 1).

Locking discipline: one threading.Lock guards ONLY the dict/field mutations —
never held around driver.run, so GET polls are never serialized behind a job.
"""

from __future__ import annotations

import errno
import fcntl
import os
import threading
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Protocol

from pipeline.orchestration import state as st

from server.state_view import next_action

TERMINAL_STATES = frozenset({"succeeded", "failed", "cancelled"})

JOB_LOG_TEMPLATE = "job-{job_id}.log"
RUN_LOCK_FILENAME = ".daemon-job.lock"


class _RunLockHeld(Exception):
    """Another daemon's job holds this run's flock (EACCES/EAGAIN)."""


class RunBusyError(Exception):
    """The run already has a non-terminal job — the single-writer guard.

    Carries the active job_id so the (Slice 5) 409 response can point at it.
    """

    def __init__(self, active_job_id: str):
        super().__init__(f"run is busy: job {active_job_id} owns it")
        self.active_job_id = active_job_id


class Driver(Protocol):
    """Runs one pipeline.run action; writes combined stdout+stderr to log_path,
    calls register(proc) once a live process handle exists, returns the rc."""

    def run(self, run_dir: Path, action_args: list[str], *,
            log_path: Path, cwd: Path,
            register: Callable[[Any], None]) -> int: ...


@dataclass
class Job:
    job_id: str
    run_id: str
    state: str = "pending"  # pending | running | succeeded | failed | cancelled
    rc: int | None = None
    logs: str = ""
    log_path: Path | None = None
    fresh_state: dict | None = None
    load_error: str | None = None
    next_action: dict | None = None
    # Internal: the live process handle the driver registers (for cancel) and
    # the cancel flag the worker folds into the terminal state.
    _proc: Any = field(default=None, repr=False)
    _cancelled: bool = field(default=False, repr=False)

    @property
    def terminal(self) -> bool:
        return self.state in TERMINAL_STATES


class JobRegistry:
    """In-memory job table + per-run active-slot, on app.state.jobs."""

    def __init__(self, runs_root: Path, driver: Driver,
                 killer: Callable[[Any], None] | None = None):
        self.runs_root = Path(runs_root)
        self.driver = driver
        self._lock = threading.Lock()
        self.jobs: dict[str, Job] = {}
        self.active_by_run: dict[str, str] = {}
        self._threads: dict[str, threading.Thread] = {}

    def submit(self, run_dir: Path, action_args: list[str]) -> Job:
        run_dir = Path(run_dir)
        run_id = run_dir.name
        # Reserve the slot AND start the worker in ONE locked section — a
        # separate reserve-then-start reopens the TOCTOU race (research Q3).
        with self._lock:
            active_id = self.active_by_run.get(run_id)
            if active_id is not None and not self.jobs[active_id].terminal:
                raise RunBusyError(active_id)
            job = Job(job_id=uuid.uuid4().hex, run_id=run_id)
            job.log_path = run_dir / JOB_LOG_TEMPLATE.format(job_id=job.job_id)
            self.jobs[job.job_id] = job
            self.active_by_run[run_id] = job.job_id
            worker = threading.Thread(
                target=self._work, args=(job, run_dir, list(action_args)),
                name=f"job-{job.job_id}", daemon=True,
            )
            self._threads[job.job_id] = worker
            worker.start()
        return job

    def get(self, job_id: str) -> Job | None:
        with self._lock:
            return self.jobs.get(job_id)

    def active_for(self, run_id: str) -> dict | None:
        """The non-terminal job owning run_id, as {job_id, mutation_status}."""
        with self._lock:
            job_id = self.active_by_run.get(run_id)
            if job_id is None:
                return None
            job = self.jobs[job_id]
            if job.terminal:
                return None
            return {"job_id": job_id, "mutation_status": job.state}

    def wait_for_terminal(self, job_id: str, timeout: float = 10.0) -> Job:
        """Test/ops helper: join the worker thread — deterministic, no sleeps."""
        with self._lock:
            job = self.jobs[job_id]
            worker = self._threads.get(job_id)
        if worker is not None:
            worker.join(timeout)
        if not job.terminal:
            raise TimeoutError(f"job {job_id} not terminal after {timeout}s")
        return job

    # -- worker ------------------------------------------------------------

    def _acquire_run_lock(self, run_dir: Path, run_id: str) -> int:
        """Per-run flock(LOCK_EX|LOCK_NB) — the daemon-vs-daemon writer guard.

        HONEST SCOPE (converged plan, Fork 1 red-team correction): flock is
        advisory and only excludes other lock-takers. The pipeline CLI never
        takes this lock, so CLI-vs-daemon on the same run is NOT protected —
        that remains the fleet-ops "one owner" operational rule. The fd is held
        for the job's life and auto-releases if the daemon dies.
        """
        fd = os.open(run_dir / RUN_LOCK_FILENAME, os.O_RDWR | os.O_CREAT, 0o644)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as e:
            os.close(fd)
            if e.errno in (errno.EACCES, errno.EAGAIN):  # both, for portability
                raise _RunLockHeld(
                    f"another daemon job holds the run lock for {run_id!r} "
                    f"({run_dir / RUN_LOCK_FILENAME}) — daemon-vs-daemon guard; "
                    "CLI-vs-daemon is NOT covered (fleet-ops one-owner rule)"
                ) from e
            raise
        return fd

    def _work(self, job: Job, run_dir: Path, action_args: list[str]) -> None:
        with self._lock:
            job.state = "running"
        try:
            try:
                lock_fd = self._acquire_run_lock(run_dir, job.run_id)
            except _RunLockHeld as e:
                self._finalize_without_running(job, str(e))
                return
            try:
                self._drive(job, run_dir, action_args)
            finally:
                os.close(lock_fd)  # releases the flock with the fd
        except Exception as e:  # noqa: BLE001 — a stuck "running" job is worse
            self._finalize_without_running(job, f"worker error: {e!r}")

    def _finalize_without_running(self, job: Job, message: str) -> None:
        """Terminal-fail a job whose driver never ran (lock conflict, worker
        error) — state on disk is untouched, so there is nothing to re-read."""
        with self._lock:
            job.logs = message
            job.state = "cancelled" if job._cancelled else "failed"
            self.active_by_run.pop(job.run_id, None)

    def _drive(self, job: Job, run_dir: Path, action_args: list[str]) -> None:
        rc: int | None = None
        driver_error: str | None = None
        try:
            proc_slot: list[Any] = []

            def register(proc: Any) -> None:
                proc_slot.append(proc)
                with self._lock:
                    job._proc = proc

            rc = self.driver.run(
                run_dir, action_args,
                log_path=job.log_path, cwd=self.runs_root.parent,
                register=register,
            )
        except Exception as e:  # noqa: BLE001 — nothing may escape the worker
            driver_error = f"driver error: {e!r}"
        logs = ""
        try:
            logs = job.log_path.read_text(encoding="utf-8")
        except OSError:
            pass
        if driver_error:
            logs = f"{logs}\n{driver_error}" if logs else driver_error
        # Re-read state after ANY rc — rc 1 paths durably save (errored fan
        # attempt, assemble sequence_file); the reload itself can fail.
        fresh: dict | None = None
        na: dict | None = None
        load_error: str | None = None
        try:
            fresh = st.load_state(run_dir)
            na = next_action(fresh)
        except (st.StateError, KeyError, TypeError) as e:
            fresh, na = None, None
            load_error = str(e)
        with self._lock:
            job.rc = rc
            job.logs = logs
            job.fresh_state = fresh
            job.next_action = na
            job.load_error = load_error
            if job._cancelled:
                job.state = "cancelled"
            elif rc == 0:
                job.state = "succeeded"
            else:
                job.state = "failed"
            self.active_by_run.pop(job.run_id, None)  # idempotent slot clear
