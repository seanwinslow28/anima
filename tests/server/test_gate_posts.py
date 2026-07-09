"""Slice 5 — the seven POST gate endpoints over the job layer.

Every mutating path runs through an injected stub driver (no real subprocess,
no spend). The endpoint's job is narrow: 404/422/409 prechecks, then one
registry.submit() carrying the exact action-args, then 202 {job_id}. Lifecycle
is driven with wait_for_terminal (join the worker thread) — never time.sleep.
"""

from pathlib import Path

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient

from server.app import create_app
from server.config import Settings


def make_client(runs_root, driver) -> TestClient:
    return TestClient(create_app(Settings(runs_root=runs_root), driver=driver))


class RecordingStubDriver:
    """Synchronous stub: records (run_dir, action_args), rc 0, no state mutation
    (so the run stays in its stage and the worker re-reads it cleanly)."""

    def __init__(self, rc: int = 0):
        self.rc = rc
        self.calls: list[tuple[Path, list[str]]] = []

    def run(self, run_dir, action_args, *, log_path, cwd, register):
        self.calls.append((Path(run_dir), list(action_args)))
        log_path.write_text("stub gate ran\n", encoding="utf-8")
        return self.rc


# -- Task 2: plan/approve ----------------------------------------------------


def test_plan_approve_happy_path_202_then_succeeded(make_run, runs_root):
    driver = RecordingStubDriver()
    client = make_client(runs_root, driver)
    run_dir, _ = make_run("plan-run")  # default stage PLAN

    r = client.post("/runs/plan-run/plan/approve")
    assert r.status_code == 202
    job_id = r.json()["job_id"]

    registry = client.app.state.jobs
    done = registry.wait_for_terminal(job_id, timeout=10)
    assert done.state == "succeeded"
    assert client.get(f"/jobs/{job_id}").json()["state"] == "succeeded"
    # The endpoint handed the driver the exact literal, gate-name-free:
    assert driver.calls[-1] == (run_dir, ["--approve-plan"])


def test_plan_approve_wrong_stage_409_and_no_job_created(make_run, runs_root):
    driver = RecordingStubDriver()
    client = make_client(runs_root, driver)
    make_run("wrong-run", stage="SCRIPT")  # not PLAN

    r = client.post("/runs/wrong-run/plan/approve")
    assert r.status_code == 409
    # Precheck fires BEFORE submit — nothing dispatched, no slot reserved:
    assert driver.calls == []
    assert client.app.state.jobs.jobs == {}
    assert client.app.state.jobs.active_for("wrong-run") is None


def test_plan_approve_unknown_run_404(runs_root):
    client = make_client(runs_root, RecordingStubDriver())
    assert client.post("/runs/does-not-exist/plan/approve").status_code == 404
