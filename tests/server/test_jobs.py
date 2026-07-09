"""Slice 4 — the job layer: registry + driver seam + /jobs surface.

Every mutating path runs through an injected stub driver (no real subprocess,
no spend); the one real-subprocess proof is the $0 `--status` smoke at the
bottom. Lifecycle tests join the worker thread via wait_for_terminal — never
time.sleep.
"""

import sys
import threading
from pathlib import Path

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient

from pipeline.orchestration import state as st

from server.app import create_app
from server.config import Settings
from server.jobs import (ENV_STRIP_VARS, JobRegistry, RunBusyError,
                         SubprocessDriver, build_argv, build_env)

REPO_ROOT = Path(__file__).resolve().parents[2]


def make_client(runs_root, driver) -> TestClient:
    return TestClient(create_app(Settings(runs_root=runs_root), driver=driver))


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


class FailAfterSaveStubDriver:
    """rc 1 AFTER durably mutating state — the errored-fan / failed-assemble
    shape (generate_stage.py saves an honest errored attempt before return 1)."""

    def run(self, run_dir, action_args, *, log_path, cwd, register):
        log_path.write_text("frame fan errored\n", encoding="utf-8")
        s = st.load_state(run_dir)
        s["stage"] = "GENERATE"
        s["frame_order"] = [1]
        s["frames"]["1"] = {"status": "pending", "attempts": [{"index": 1, "errored": "boom"}]}
        st.save_state(run_dir, s)
        return 1


class CorruptStateStubDriver:
    """Destroys run_state.json mid-job (dir deleted / corrupted) — the reload
    itself must fail into load_error, never an escaping exception."""

    def run(self, run_dir, action_args, *, log_path, cwd, register):
        log_path.write_text("gate ran then the state went bad\n", encoding="utf-8")
        (run_dir / st.STATE_FILENAME).write_text("{ not json", encoding="utf-8")
        return 0


def test_rc_nonzero_still_rereads_saved_state(make_run, runs_root):
    run_dir, _ = make_run("rc1-run")
    reg = JobRegistry(runs_root=runs_root, driver=FailAfterSaveStubDriver())
    job = reg.submit(run_dir, ["--retry-frame", "1", "--note", "hold the line"])
    done = reg.wait_for_terminal(job.job_id, timeout=10)
    assert done.state == "failed"
    assert done.rc == 1
    # rc 1 saved durable state BEFORE returning — the worker must surface it:
    assert done.fresh_state is not None
    assert done.fresh_state["frames"]["1"]["attempts"][0]["errored"] == "boom"
    assert done.load_error is None


def test_state_reload_failure_reports_load_error_not_exception(make_run, runs_root):
    run_dir, _ = make_run("corrupt-run")
    reg = JobRegistry(runs_root=runs_root, driver=CorruptStateStubDriver())
    job = reg.submit(run_dir, ["--approve-plan"])
    done = reg.wait_for_terminal(job.job_id, timeout=10)  # worker never raises
    assert done.rc == 0 and done.state == "succeeded"      # rc drives the state
    assert done.fresh_state is None
    assert done.next_action is None
    assert done.load_error and "run_state.json" in done.load_error


def test_flock_excludes_a_second_daemon_on_the_same_run(make_run, runs_root):
    """Two registries over one run dir = two daemons. The second's
    LOCK_EX|LOCK_NB must fail (EACCES/EAGAIN) into an honest failed job.

    HONEST SCOPE: this covers daemon-vs-daemon ONLY. The pipeline CLI never
    takes this flock, so CLI-vs-daemon on the same run is NOT protected here —
    that stays the fleet-ops "one owner" operational rule (converged plan,
    Fork 1 red-team correction).
    """
    run_dir, _ = make_run("locked-run")
    gated = GatedStubDriver()
    daemon_a = JobRegistry(runs_root=runs_root, driver=gated)
    daemon_b = JobRegistry(runs_root=runs_root, driver=ApprovePlanStubDriver())

    holder = daemon_a.submit(run_dir, ["--approve-plan"])
    assert gated.started.wait(10)  # daemon A's worker holds the flock

    contender = daemon_b.submit(run_dir, ["--approve-plan"])
    done = daemon_b.wait_for_terminal(contender.job_id, timeout=10)
    assert done.state == "failed"
    assert done.rc is None                       # nothing ran — pure lock conflict
    assert "another daemon job holds the run lock" in done.logs
    assert daemon_b.active_for("locked-run") is None

    gated.release.set()
    assert daemon_a.wait_for_terminal(holder.job_id, timeout=10).state == "succeeded"
    # Lock released with the fd -> a fresh job on daemon B now proceeds.
    retry = daemon_b.submit(run_dir, ["--approve-plan"])
    assert daemon_b.wait_for_terminal(retry.job_id, timeout=10).state == "succeeded"


def test_get_job_endpoint_returns_the_projection(make_run, runs_root):
    client = make_client(runs_root, ApprovePlanStubDriver())
    run_dir, _ = make_run("api-run")
    registry = client.app.state.jobs
    job = registry.submit(run_dir, ["--approve-plan"])
    registry.wait_for_terminal(job.job_id, timeout=10)

    r = client.get(f"/jobs/{job.job_id}")
    assert r.status_code == 200
    body = r.json()
    assert set(body) == {"job_id", "run_id", "state", "rc", "logs",
                         "fresh_state", "load_error", "next_action"}
    assert body["job_id"] == job.job_id
    assert body["run_id"] == "api-run"
    assert body["state"] == "succeeded"
    assert body["rc"] == 0
    assert body["fresh_state"]["stage"] == "GENERATE"
    assert body["load_error"] is None
    assert body["next_action"]["kind"] == "assemble"


def test_get_unknown_job_is_404(runs_root):
    client = make_client(runs_root, ApprovePlanStubDriver())
    assert client.get("/jobs/no-such-job").status_code == 404


def test_create_app_without_driver_defaults_to_the_real_subprocess_driver(runs_root):
    app = create_app(Settings(runs_root=runs_root))
    assert isinstance(app.state.jobs.driver, SubprocessDriver)
    assert app.state.jobs.runs_root == runs_root


class FakeProc:
    pid = 424242


def test_cancel_running_job_invokes_the_killer_and_lands_cancelled(make_run, runs_root):
    run_dir, _ = make_run("cancel-run")
    fake = FakeProc()
    gated = GatedStubDriver(rc=143, proc=fake)  # rc mimics a SIGTERM'd child
    client = make_client(runs_root, gated)
    registry = client.app.state.jobs

    killed = []

    def spy_killer(proc):
        killed.append(proc)
        gated.release.set()  # the "kill" is what unblocks the fake child

    registry.killer = spy_killer
    job = registry.submit(run_dir, ["--approve-frame", "1"])
    assert gated.started.wait(10)

    r = client.post(f"/jobs/{job.job_id}/cancel")
    assert r.status_code == 200
    assert r.json()["state"] == "cancelled"
    assert killed == [fake]                     # the registered live handle
    done = registry.wait_for_terminal(job.job_id, timeout=10)
    assert done.state == "cancelled"            # _cancelled outranks the rc
    assert registry.active_for("cancel-run") is None


def test_cancel_unknown_job_is_404(runs_root):
    client = make_client(runs_root, ApprovePlanStubDriver())
    assert client.post("/jobs/no-such-job/cancel").status_code == 404


def test_cancel_terminal_job_is_409(make_run, runs_root):
    run_dir, _ = make_run("done-run")
    client = make_client(runs_root, ApprovePlanStubDriver())
    registry = client.app.state.jobs
    job = registry.submit(run_dir, ["--approve-plan"])
    registry.wait_for_terminal(job.job_id, timeout=10)
    assert client.post(f"/jobs/{job.job_id}/cancel").status_code == 409


def test_kill_proc_tree_terminates_a_real_child():
    """The default psutil killer against a real (cheap, credential-free)
    subprocess — SIGTERM-then-grace, no zombie left behind."""
    import subprocess
    import sys as _sys

    from server.jobs import kill_proc_tree

    proc = subprocess.Popen([_sys.executable, "-c",
                             "import time; time.sleep(60)"])
    try:
        kill_proc_tree(proc)
        assert proc.wait(timeout=10) is not None  # reaped, no zombie
    finally:
        if proc.poll() is None:
            proc.kill()


def test_run_status_carries_active_job_while_a_job_owns_the_run(make_run, runs_root):
    """The active-cascade overlay (Codex blocker-2): a GET mid-job must say a
    job owns the run. Slice 4 only EXPOSES active_job — the next_action
    suppression is Slice 5."""
    run_dir, _ = make_run("status-run")
    gated = GatedStubDriver()
    client = make_client(runs_root, gated)
    registry = client.app.state.jobs

    job = registry.submit(run_dir, ["--approve-plan"])
    assert gated.started.wait(10)
    body = client.get("/runs/status-run/status").json()
    assert body["active_job"] == {"job_id": job.job_id, "mutation_status": "running"}
    assert body["next_action"]["kind"] == "planning"  # unchanged, no suppression

    gated.release.set()
    registry.wait_for_terminal(job.job_id, timeout=10)
    assert client.get("/runs/status-run/status").json()["active_job"] is None


# -- the real SubprocessDriver (task 8) -------------------------------------


def test_build_argv_shape_and_no_api_key_override():
    argv = build_argv(Path("runs/some-run"), ["--approve-frame", "3", "--attempt", "2"])
    assert argv == [sys.executable, "-m", "pipeline.run",
                    "--resume", "runs/some-run",
                    "--approve-frame", "3", "--attempt", "2"]
    # An API-billed daemon job must be IMPOSSIBLE, not merely defaulted-off:
    assert "--allow-api-key" not in argv


def test_build_env_strips_session_markers_keeps_execpath(monkeypatch):
    # fleet-ops §6: the six nested-SDK throttle markers stripped,
    # CLAUDE_CODE_EXECPATH preserved so shutil.which('claude') still resolves.
    assert set(ENV_STRIP_VARS) == {
        "CLAUDECODE", "CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_CHILD_SESSION",
        "CLAUDE_CODE_ENTRYPOINT", "AI_AGENT", "CLAUDE_CODE_ENABLE_TASKS",
    }
    for var in ENV_STRIP_VARS:
        monkeypatch.setenv(var, "1")
    monkeypatch.setenv("CLAUDE_CODE_EXECPATH", "/usr/local/bin/claude")
    monkeypatch.setenv("ANIMA_UNRELATED", "kept")
    env = build_env()
    for var in ENV_STRIP_VARS:
        assert var not in env
    assert env["CLAUDE_CODE_EXECPATH"] == "/usr/local/bin/claude"
    assert env["ANIMA_UNRELATED"] == "kept"


def test_real_subprocess_driver_status_smoke(make_run):
    """The one real-subprocess proof, $0: `--status` reads state and prints —
    no model call, no spend. Exercises argv + env-strip + cwd + log capture +
    rc plumbing end to end against the worktree's pipeline.run."""
    run_dir, _ = make_run("smoke-run")
    log_path = run_dir / "smoke.log"
    registered = []
    rc = SubprocessDriver().run(
        run_dir, ["--status"],
        log_path=log_path, cwd=REPO_ROOT, register=registered.append,
    )
    assert rc == 0
    assert registered and registered[0].pid > 0   # register() got the live handle
    log = log_path.read_text(encoding="utf-8")
    assert "stage:" in log                        # render_status output captured


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
