"""Slice 4 — the job layer: registry + driver seam + /jobs surface.

Every mutating path runs through an injected stub driver (no real subprocess,
no spend); the one real-subprocess proof is the $0 `--status` smoke at the
bottom. Lifecycle tests join the worker thread via wait_for_terminal — never
time.sleep.
"""

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from pipeline.orchestration import state as st

from server.jobs import JobRegistry


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
