"""Slice 4 — the job layer: registry + driver seam + /jobs surface.

Every mutating path runs through an injected stub driver (no real subprocess,
no spend); the one real-subprocess proof is the $0 `--status` smoke at the
bottom. Lifecycle tests join the worker thread via wait_for_terminal — never
time.sleep.
"""

import threading

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from pipeline.orchestration import state as st

from server.jobs import JobRegistry, RunBusyError


class ApprovePlanStubDriver:
    """Synchronous stub: mutates run-state like the plan gate would, rc 0."""

    def run(self, run_dir, action_args, *, log_path, cwd, register):
        log_path.write_text("stub: plan approved\n", encoding="utf-8")
        s = st.load_state(run_dir)
        s["plan"]["status"] = "approved"
        s["stage"] = "GENERATE"
        st.save_state(run_dir, s)
        return 0


def test_submit_runs_to_succeeded_with_fresh_state(make_run, runs_root):
    run_dir, _ = make_run("job-run")
    reg = JobRegistry(runs_root=runs_root, driver=ApprovePlanStubDriver())

    job = reg.submit(run_dir, ["--approve-plan"])
    assert job.run_id == "job-run"
    assert job.state in ("pending", "running", "succeeded")  # 202-time snapshot

    done = reg.wait_for_terminal(job.job_id, timeout=10)
    assert done is job
    assert done.state == "succeeded"
    assert done.rc == 0
    assert "plan approved" in done.logs
    # The worker re-read run_state.json after the driver ran:
    assert done.fresh_state is not None
    assert done.fresh_state["stage"] == "GENERATE"
    assert done.load_error is None
    # and projected the pipeline's own next_action from the fresh state:
    assert done.next_action == {"kind": "assemble", "hint": done.next_action["hint"]}


def test_terminal_job_releases_the_run_slot(make_run, runs_root):
    run_dir, _ = make_run("slot-run")
    reg = JobRegistry(runs_root=runs_root, driver=ApprovePlanStubDriver())
    job = reg.submit(run_dir, ["--approve-plan"])
    reg.wait_for_terminal(job.job_id, timeout=10)
    assert reg.active_for("slot-run") is None
    assert reg.get(job.job_id) is job          # the record survives the slot


def test_get_unknown_job_is_none(runs_root):
    reg = JobRegistry(runs_root=runs_root, driver=ApprovePlanStubDriver())
    assert reg.get("nope") is None


class GatedStubDriver:
    """Holds the run busy until the test releases it. Optionally registers a
    fake process handle so cancel has something to kill."""

    def __init__(self, rc: int = 0, proc=None):
        self.rc = rc
        self.proc = proc
        self.started = threading.Event()
        self.release = threading.Event()

    def run(self, run_dir, action_args, *, log_path, cwd, register):
        log_path.write_text("gated stub\n", encoding="utf-8")
        if self.proc is not None:
            register(self.proc)
        self.started.set()
        assert self.release.wait(10), "test never released the gated driver"
        return self.rc


def test_second_submit_to_busy_run_raises_with_active_job_id(make_run, runs_root):
    run_dir, _ = make_run("busy-run")
    gated = GatedStubDriver()
    reg = JobRegistry(runs_root=runs_root, driver=gated)

    first = reg.submit(run_dir, ["--approve-plan"])
    assert gated.started.wait(10)
    with pytest.raises(RunBusyError) as excinfo:
        reg.submit(run_dir, ["--approve-plan"])
    assert excinfo.value.active_job_id == first.job_id

    gated.release.set()
    done = reg.wait_for_terminal(first.job_id, timeout=10)
    assert done.state == "succeeded"
    # Slot released -> the run accepts a new job.
    gated.release.set()  # let the second worker straight through
    second = reg.submit(run_dir, ["--approve-plan"])
    assert reg.wait_for_terminal(second.job_id, timeout=10).state == "succeeded"


def test_two_different_runs_run_concurrently(make_run, runs_root):
    dir_a, _ = make_run("run-a")
    dir_b, _ = make_run("run-b")
    gated = GatedStubDriver()
    reg = JobRegistry(runs_root=runs_root, driver=gated)
    job_a = reg.submit(dir_a, ["--approve-plan"])
    job_b = reg.submit(dir_b, ["--approve-plan"])  # must NOT raise: other run
    gated.release.set()
    assert reg.wait_for_terminal(job_a.job_id, timeout=10).state == "succeeded"
    assert reg.wait_for_terminal(job_b.job_id, timeout=10).state == "succeeded"
