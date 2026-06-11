"""P3 — the ASSEMBLE tail.

export/sequence.txt is written from state (frame_order + holds, full-basename
KEY:hold lines), then the generalized assemble.sh (#13) runs through the same
Runner via the AssembleNode, consuming the approved keys. Runs from the repo
root (assemble.sh is CWD-relative); ffmpeg is the PATH shim — staging is real,
encodes are not.
"""

from __future__ import annotations

from pathlib import Path

from pipeline import run as run_cli
from pipeline.orchestration import assemble_stage
from pipeline.orchestration import state as st
from tests.orch_fixtures import fake_ffmpeg_path, write_png


def _assemble_ready_state(run_dir: Path) -> dict:
    state = st.new_state(
        run_id="tt-run", brief_dir="briefs/x", manifest_path="manifest.yaml",
        shots_path="briefs/x/shots.yaml", slug="TT", stub=True, cast=[],
    )
    state["frame_order"] = [1, 2]
    state["holds"] = {"1": 2, "2": 3}
    for n in (1, 2):
        approved = run_dir / "approved" / f"TT_F{n:02d}_key.png"
        write_png(approved, size=(64, 36))
        st.set_frame(state, n, {"status": "approved", "attempts": [],
                                "approved_attempt": 1, "approved_path": str(approved)})
    state["stage"] = "ASSEMBLE"
    st.save_state(run_dir, state)
    return state


def test_sequence_file_written_from_frame_order_and_holds(tmp_path):
    run_dir = tmp_path / "run"
    state = _assemble_ready_state(run_dir)

    seq = assemble_stage.write_sequence_file(state, run_dir)

    assert seq == run_dir / "export" / "sequence.txt"
    assert seq.read_text() == "TT_F01_key:2\nTT_F02_key:3\n"


def test_assemble_runs_with_slug_and_sequence_and_reaches_done(tmp_path, monkeypatch):
    run_dir = tmp_path / "run"
    state = _assemble_ready_state(run_dir)
    fake_ffmpeg_path(tmp_path, monkeypatch)

    rc = assemble_stage.run_assemble_stage(state, {}, None, run_dir)

    assert rc == 0
    # staging honored the holds: 2 + 3 = 5 frames
    staged = sorted((run_dir / "export" / "sequence").glob("frame_*.png"))
    assert len(staged) == 5
    # the slugged outputs exist (fake-ffmpeg creates them) and state records them
    assert state["stage"] == "DONE"
    assert state["assemble"]["gif"].endswith("TT.gif")
    assert state["assemble"]["webm"].endswith("TT.webm")
    assert state["assemble"]["mp4"].endswith("TT.mp4")
    assert (run_dir / "export" / "TT.gif").exists()
    # durable: the on-disk state agrees
    assert st.load_state(run_dir)["stage"] == "DONE"


def test_resume_assemble_action_runs_tail_and_guards_stage(tmp_path, monkeypatch, capsys):
    run_dir = tmp_path / "run"
    _assemble_ready_state(run_dir)
    fake_ffmpeg_path(tmp_path, monkeypatch)

    # wrong stage first: a DONE run refuses --assemble
    rc = run_cli.main(["--resume", str(run_dir), "--assemble"])
    assert rc == 0
    assert st.load_state(run_dir)["stage"] == "DONE"

    capsys.readouterr()
    rc = run_cli.main(["--resume", str(run_dir), "--assemble"])
    assert rc == 2
    assert "ASSEMBLE" in capsys.readouterr().err
