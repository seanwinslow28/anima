"""Slice 5 — the seven POST gate endpoints over the job layer.

Every mutating path runs through an injected stub driver (no real subprocess,
no spend). The endpoint's job is narrow: 404/422/409 prechecks, then one
registry.submit() carrying the exact action-args, then 202 {job_id}. Lifecycle
is driven with wait_for_terminal (join the worker thread) — never time.sleep.
"""

import threading
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


# -- Task 3: script / storyboard / animatic / assemble -----------------------

# (name, required_stage, url_suffix, expected action-args). PLAN is the wrong
# stage for all four, so the wrong-stage case uses a default (PLAN) run.
STATIC_GATES = [
    ("script", "SCRIPT", "script/approve", ["--approve-script"]),
    ("storyboard", "STORYBOARD", "storyboard/approve", ["--approve-storyboard"]),
    ("animatic", "ANIMATIC", "animatic/approve", ["--approve-animatic"]),
    ("assemble", "ASSEMBLE", "assemble", ["--assemble"]),
]


@pytest.mark.parametrize("name,stage,suffix,args", STATIC_GATES)
def test_static_gate_right_stage_202_dispatches_exact_args(
        name, stage, suffix, args, make_run, runs_root):
    driver = RecordingStubDriver()
    client = make_client(runs_root, driver)
    run_dir, _ = make_run(f"{name}-ok", stage=stage)

    r = client.post(f"/runs/{name}-ok/{suffix}")
    assert r.status_code == 202
    job_id = r.json()["job_id"]
    done = client.app.state.jobs.wait_for_terminal(job_id, timeout=10)
    assert done.state == "succeeded"
    assert driver.calls[-1] == (run_dir, args)


@pytest.mark.parametrize("name,stage,suffix,args", STATIC_GATES)
def test_static_gate_wrong_stage_409_and_no_job(
        name, stage, suffix, args, make_run, runs_root):
    driver = RecordingStubDriver()
    client = make_client(runs_root, driver)
    make_run(f"{name}-bad")  # default stage PLAN — wrong for all four

    r = client.post(f"/runs/{name}-bad/{suffix}")
    assert r.status_code == 409
    assert driver.calls == []
    assert client.app.state.jobs.jobs == {}
    assert client.app.state.jobs.active_for(f"{name}-bad") is None


# -- Task 4: frame approve + retry (GENERATE stage) --------------------------


def test_approve_frame_202_dispatches_approve_frame_n(make_generate_run, runs_root):
    driver = RecordingStubDriver()
    client = make_client(runs_root, driver)
    run_dir, _ = make_generate_run("gen-approve")

    r = client.post("/runs/gen-approve/frames/1/approve")
    assert r.status_code == 202
    done = client.app.state.jobs.wait_for_terminal(r.json()["job_id"], timeout=10)
    assert done.state == "succeeded"
    assert driver.calls[-1] == (run_dir, ["--approve-frame", "1"])


def test_approve_frame_attempt_query_appends_attempt_arg(make_generate_run, runs_root):
    driver = RecordingStubDriver()
    client = make_client(runs_root, driver)
    run_dir, _ = make_generate_run("gen-attempt")

    r = client.post("/runs/gen-attempt/frames/1/approve?attempt=2")
    assert r.status_code == 202
    client.app.state.jobs.wait_for_terminal(r.json()["job_id"], timeout=10)
    assert driver.calls[-1] == (run_dir, ["--approve-frame", "1", "--attempt", "2"])


def test_retry_frame_202_dispatches_retry_with_note(make_generate_run, runs_root):
    driver = RecordingStubDriver()
    client = make_client(runs_root, driver)
    run_dir, _ = make_generate_run("gen-retry")

    r = client.post("/runs/gen-retry/frames/1/retry",
                    json={"note": "hold the line weight"})
    assert r.status_code == 202
    client.app.state.jobs.wait_for_terminal(r.json()["job_id"], timeout=10)
    assert driver.calls[-1] == (
        run_dir, ["--retry-frame", "1", "--note", "hold the line weight"])


def test_retry_frame_empty_note_422_and_no_job(make_generate_run, runs_root):
    driver = RecordingStubDriver()
    client = make_client(runs_root, driver)
    make_generate_run("gen-empty")

    r = client.post("/runs/gen-empty/frames/1/retry", json={"note": "   "})
    assert r.status_code == 422
    assert driver.calls == []
    assert client.app.state.jobs.jobs == {}


def test_retry_frame_missing_note_422(make_generate_run, runs_root):
    client = make_client(runs_root, RecordingStubDriver())
    make_generate_run("gen-missing")
    r = client.post("/runs/gen-missing/frames/1/retry", json={})
    assert r.status_code == 422


def test_frame_gates_wrong_stage_409_before_note_check(make_run, runs_root):
    driver = RecordingStubDriver()
    client = make_client(runs_root, driver)
    make_run("gen-wrong")  # default PLAN, not GENERATE

    assert client.post("/runs/gen-wrong/frames/1/approve").status_code == 409
    # A valid note still 409s on the (earlier) stage check:
    assert client.post("/runs/gen-wrong/frames/1/retry",
                       json={"note": "x"}).status_code == 409
    assert driver.calls == []
    assert client.app.state.jobs.jobs == {}


# -- Task 5: the single-writer 409 -------------------------------------------


class GatedStubDriver:
    """Holds the run busy inside run() until the test releases the Event."""

    def __init__(self, rc: int = 0):
        self.rc = rc
        self.started = threading.Event()
        self.release = threading.Event()

    def run(self, run_dir, action_args, *, log_path, cwd, register):
        log_path.write_text("gated gate\n", encoding="utf-8")
        self.started.set()
        assert self.release.wait(10), "test never released the gated driver"
        return self.rc


def test_second_gate_post_to_busy_run_409_with_active_job_id(
        make_generate_run, runs_root):
    gated = GatedStubDriver()
    client = make_client(runs_root, gated)
    make_generate_run("busy-run")
    registry = client.app.state.jobs

    first = client.post("/runs/busy-run/frames/1/approve")
    assert first.status_code == 202
    first_job = first.json()["job_id"]
    assert gated.started.wait(10)  # the worker is in the driver, holding the slot

    # A second POST to the SAME run via a DIFFERENT gate is refused with the
    # active job_id — the guard is per-run, not per-endpoint — and dispatches
    # nothing new (still only the one job).
    second = client.post("/runs/busy-run/frames/1/retry", json={"note": "again"})
    assert second.status_code == 409
    assert second.json()["detail"]["active_job_id"] == first_job
    assert len(registry.jobs) == 1

    gated.release.set()
    assert registry.wait_for_terminal(first_job, timeout=10).state == "succeeded"

    # Slot released with the terminal job -> the run accepts a fresh gate.
    third = client.post("/runs/busy-run/frames/1/approve")
    assert third.status_code == 202
    assert registry.wait_for_terminal(third.json()["job_id"], timeout=10).state == "succeeded"


# -- Task 6: next_action suppression, end to end -----------------------------


def test_status_endpoint_blocks_next_action_while_a_gate_job_runs(
        make_generate_run, runs_root):
    gated = GatedStubDriver()
    client = make_client(runs_root, gated)
    make_generate_run("cascade-run")
    registry = client.app.state.jobs

    job_id = client.post("/runs/cascade-run/frames/1/approve").json()["job_id"]
    assert gated.started.wait(10)
    body = client.get("/runs/cascade-run/status").json()
    assert body["active_job"] == {"job_id": job_id, "mutation_status": "running"}
    assert body["next_action"]["blocked_by_job"] == job_id

    gated.release.set()
    registry.wait_for_terminal(job_id, timeout=10)
    idle = client.get("/runs/cascade-run/status").json()
    assert idle["active_job"] is None
    assert "blocked_by_job" not in idle["next_action"]


# -- Task 7: wiring guard ----------------------------------------------------


def test_create_app_registers_the_seven_gate_post_routes(runs_root):
    # The default app (real subprocess driver) must expose every gate as a POST.
    # Via the resolved OpenAPI schema (version-robust — this FastAPI lazily wraps
    # included routers); breaks loudly if include_router(gates_router) is dropped.
    app = create_app(Settings(runs_root=runs_root))
    paths = app.openapi()["paths"]
    for gate in (
        "/runs/{run_id}/plan/approve",
        "/runs/{run_id}/script/approve",
        "/runs/{run_id}/storyboard/approve",
        "/runs/{run_id}/animatic/approve",
        "/runs/{run_id}/assemble",
        "/runs/{run_id}/frames/{n}/approve",
        "/runs/{run_id}/frames/{n}/retry",
    ):
        assert "post" in paths.get(gate, {}), f"gate route not registered: {gate}"
