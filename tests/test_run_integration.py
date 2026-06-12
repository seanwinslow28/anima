"""P4 — full stub-green brief -> loop, plus resume durability (seam #16 end to end).

Every run_cli.main() call re-loads state from disk, so the resume round-trip
is intrinsic to the flow: each gate is a separate process-equivalent
invocation against the durable run_state.json.
"""

from __future__ import annotations

import json
import os

from pipeline import run as run_cli
from pipeline.orchestration import state as st
from tests.orch_fixtures import (
    fake_ffmpeg_path,
    mk_project,
    spy_flo_stub,
    stub_critic_env,
)


def test_full_stub_green_brief_to_loop(tmp_path, monkeypatch):
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    stub_critic_env(monkeypatch)
    flo_calls = spy_flo_stub(monkeypatch)
    fake_ffmpeg_path(tmp_path, monkeypatch)
    run_dir = root / "runs" / "tt-run"

    # PLAN: draft, stop at the plan gate
    assert run_cli.main(["--brief", str(brief_dir), "--stub",
                         "--run-dir", str(run_dir)]) == 0
    assert st.load_state(run_dir)["stage"] == "PLAN"

    # plan gate -> GENERATE, frame 1 fanned, eye gate
    assert run_cli.main(["--resume", str(run_dir), "--approve-plan"]) == 0
    assert st.load_state(run_dir)["stage"] == "GENERATE"

    # the eye says no once: retry with a correction note
    assert run_cli.main(["--resume", str(run_dir), "--retry-frame", "1",
                         "--note", "tighter silhouette"]) == 0
    state = st.load_state(run_dir)
    assert [a["index"] for a in st.get_frame(state, 1)["attempts"]] == [1, 2]

    # approve attempt 2 explicitly -> frame 2 generates in the same invocation
    assert run_cli.main(["--resume", str(run_dir), "--approve-frame", "1",
                         "--attempt", "2"]) == 0
    state = st.load_state(run_dir)
    assert st.get_frame(state, 1)["approved_attempt"] == 2
    assert st.get_frame(state, 2)["status"] == "generated"

    # approve the last frame -> ASSEMBLE auto-runs -> DONE
    assert run_cli.main(["--resume", str(run_dir), "--approve-frame", "2"]) == 0
    state = st.load_state(run_dir)
    assert state["stage"] == "DONE"

    # the loop exists, slugged + staged per holds (2 + 3)
    assert (run_dir / "export" / "TT.gif").exists()
    assert (run_dir / "export" / "TT.webm").exists()
    assert (run_dir / "export" / "TT.mp4").exists()
    assert (run_dir / "export" / "sequence.txt").read_text() == "TT_F01_key:2\nTT_F02_key:3\n"
    assert len(list((run_dir / "export" / "sequence").glob("frame_*.png"))) == 5

    # the evidence trail: 3 attempts x cast size = 2+2+1 Em verdicts, 2 approvals
    vlog = (run_dir / "em_verdicts.jsonl").read_text().strip().splitlines()
    assert len(vlog) == 5
    approvals = (run_dir / "approved" / "approvals.jsonl").read_text().strip().splitlines()
    assert [json.loads(line)["frame"] for line in approvals] == ["TT_F01", "TT_F02"]
    # 3 real generations fired (F01 x2, F02 x1)
    assert [c["frame_num"] for c in flo_calls] == [1, 1, 2]

    # a finished run politely refuses further gates
    assert run_cli.main(["--resume", str(run_dir), "--approve-frame", "2"]) == 2
    assert run_cli.main(["--resume", str(run_dir), "--status"]) == 0


def test_interrupt_mid_generate_state_intact_and_continues(tmp_path, monkeypatch):
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    stub_critic_env(monkeypatch)
    fake_ffmpeg_path(tmp_path, monkeypatch)
    run_dir = root / "runs" / "tt-run"

    # frame 1 generates fine; frame 2's generation "crashes" mid-fan.
    # Post-Fix-A the --stub fan dispatches flo_stub, so that's the node to crash.
    import pipeline.agents.flo_stub as fs

    calls = {"n": 0}
    real_run = fs.FloStubNode.run

    def flaky(self, ctx):
        calls["n"] += 1
        if int(ctx.inputs["frame_num"]) == 2 and calls["n"] == 2:
            raise KeyboardInterrupt("laptop closed")  # not even an Exception subclass
        return real_run(self, ctx)

    monkeypatch.setattr(fs.FloStubNode, "run", flaky)

    assert run_cli.main(["--brief", str(brief_dir), "--stub",
                         "--run-dir", str(run_dir)]) == 0
    assert run_cli.main(["--resume", str(run_dir), "--approve-plan"]) == 0

    # approving F01 chains into F02, which dies mid-generation
    try:
        run_cli.main(["--resume", str(run_dir), "--approve-frame", "1"])
    except BaseException:
        pass

    # the state on disk is intact and resumable: F01 approved survived the crash
    state = st.load_state(run_dir)
    assert state["stage"] == "GENERATE"
    assert st.get_frame(state, 1)["status"] == "approved"
    assert st.current_frame(state) == 2
    assert run_cli.main(["--resume", str(run_dir), "--status"]) == 0

    # continue: retry F02, approve, assemble -> DONE
    assert run_cli.main(["--resume", str(run_dir), "--retry-frame", "2",
                         "--note", "resume after interrupt"]) == 0
    assert run_cli.main(["--resume", str(run_dir), "--approve-frame", "2"]) == 0
    assert st.load_state(run_dir)["stage"] == "DONE"


def test_production_path_offline_stub_run_reaches_done(tmp_path, monkeypatch, capsys):
    """THE Slice 2.1 headline: the real CLI walks PLAN -> GENERATE (all frames)
    -> ASSEMBLE -> DONE with --stub and no GEMINI_API_KEY — no flo monkeypatch,
    no spies, no fixtures on the generation path. flo_stub + Em-no-key +
    assemble.sh are the real production stub chain (env shaping only)."""
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    stub_critic_env(monkeypatch)            # env shaping only — no behavior fakes
    fake_ffmpeg_path(tmp_path, monkeypatch) # encodes skipped; assemble.sh runs real
    assert os.environ.get("GEMINI_API_KEY") is None
    run_dir = root / "runs" / "tt-run"

    assert run_cli.main(["--brief", str(brief_dir), "--stub",
                         "--run-dir", str(run_dir)]) == 0
    assert run_cli.main(["--resume", str(run_dir), "--approve-plan"]) == 0
    state = st.load_state(run_dir)
    while state["stage"] == "GENERATE":
        n = st.current_frame(state)
        assert run_cli.main(["--resume", str(run_dir),
                             "--approve-frame", str(n)]) == 0
        state = st.load_state(run_dir)

    assert state["stage"] == "DONE"
    assert (run_dir / "export" / "TT.gif").exists()
    assert (run_dir / "export" / "TT.webm").exists()
    assert (run_dir / "export" / "TT.mp4").exists()
    # real placeholder candidates exist on disk (flo_stub wrote them)
    assert (run_dir / "candidates" / "F01" / "attempt_01.png").exists()
    assert (run_dir / "candidates" / "F02" / "attempt_01.png").exists()
    # honesty: a stub run is never mistaken for real
    capsys.readouterr()
    assert run_cli.main(["--resume", str(run_dir), "--status"]) == 0
    assert "[stub]" in capsys.readouterr().out
