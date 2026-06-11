"""P4 — full stub-green brief -> loop, plus resume durability (seam #16 end to end).

Every run_cli.main() call re-loads state from disk, so the resume round-trip
is intrinsic to the flow: each gate is a separate process-equivalent
invocation against the durable run_state.json.
"""

from __future__ import annotations

import json

from pipeline import run as run_cli
from pipeline.orchestration import state as st
from tests.orch_fixtures import (
    fake_ffmpeg_path,
    fake_flo_generate,
    mk_project,
    stub_critic_env,
)


def test_full_stub_green_brief_to_loop(tmp_path, monkeypatch):
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    stub_critic_env(monkeypatch)
    flo_calls = fake_flo_generate(monkeypatch)
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

    # frame 1 generates fine; frame 2's generation "crashes" mid-fan
    from pipeline import generate as legacy_generate
    from tests.orch_fixtures import write_png

    calls = {"n": 0}

    def flaky(*, frame_num, prompt, references, manifest, run_dir):
        calls["n"] += 1
        if frame_num == 2 and calls["n"] == 2:
            raise KeyboardInterrupt("laptop closed")  # not even an Exception subclass
        out = run_dir / "candidates" / f"F{frame_num:02d}" / "attempt_01.png"
        write_png(out, size=(1376, 768))
        return out

    monkeypatch.setattr(legacy_generate, "generate_frame", flaky)

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
