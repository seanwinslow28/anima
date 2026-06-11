"""P0 — the run orchestrator's durable state model.

`pipeline/orchestration/state.py` owns runs/<id>/run_state.json: atomic
read/write, the PLAN→GENERATE→ASSEMBLE→DONE stage enum, and the int↔str
frame-key boundary (JSON object keys are strings; accessors take ints).
`pipeline/run.py` is the CLI skeleton — P0 covers --status and the clean
error paths (missing state, action in the wrong stage).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.orchestration import state as st
from pipeline import run as run_cli


def _cast() -> list[dict]:
    return [
        {
            "folder_key": "sean-anchor",
            "ir_namespace": "sean",
            "anchor": "characters/sean-anchor/anchor.png",
            "criteria": "characters/sean-anchor/acceptance_criteria.json",
        },
        {
            "folder_key": "claude-mascot",
            "ir_namespace": "claude-mascot",
            "anchor": "characters/claude-mascot/anchor.png",
            "criteria": "characters/claude-mascot/acceptance_criteria.json",
        },
    ]


def _new_state() -> dict:
    return st.new_state(
        run_id="2026-06-12-ss-run",
        brief_dir="briefs/2026-06-10-spark-shared",
        manifest_path="manifest.yaml",
        shots_path="briefs/2026-06-10-spark-shared/shots.yaml",
        slug="SS",
        stub=True,
        cast=_cast(),
    )


# ---------- state file round-trip ----------


def test_state_roundtrip_preserves_all_fields(tmp_path):
    s = _new_state()
    s["frame_order"] = [1, 2, 3]
    s["holds"] = {"1": 2, "2": 3, "3": 2}
    st.set_frame(s, 1, {"status": "generated", "attempts": [{"index": 1}],
                        "approved_attempt": None, "approved_path": None})

    st.save_state(tmp_path, s)
    loaded = st.load_state(tmp_path)

    assert loaded == s
    # int accessor crosses the JSON str-key boundary
    assert st.get_frame(loaded, 1)["status"] == "generated"
    assert loaded["stage"] == "PLAN"
    assert loaded["cast"][0]["ir_namespace"] == "sean"
    assert loaded["schema_version"] == 1


def test_save_state_is_atomic(tmp_path):
    s = _new_state()
    st.save_state(tmp_path, s)
    before = (tmp_path / "run_state.json").read_text(encoding="utf-8")

    bad = dict(s)
    bad["frames"] = {"1": {"status": {1, 2, 3}}}  # a set: not JSON-serializable
    with pytest.raises(Exception):
        st.save_state(tmp_path, bad)

    # The prior good file survives, byte-identical; no .tmp residue.
    assert (tmp_path / "run_state.json").read_text(encoding="utf-8") == before
    assert list(tmp_path.glob("*.tmp")) == []


def test_load_state_missing_raises_with_clear_message(tmp_path):
    with pytest.raises(st.StateError, match="run_state.json"):
        st.load_state(tmp_path / "nope")


# ---------- stage transitions ----------


def test_advance_stage_rejects_illegal_transition():
    s = _new_state()
    with pytest.raises(st.StateError):
        st.advance_stage(s, "ASSEMBLE")  # PLAN -> ASSEMBLE skips GENERATE
    st.advance_stage(s, "GENERATE")
    assert s["stage"] == "GENERATE"
    with pytest.raises(st.StateError):
        st.advance_stage(s, "PLAN")  # no going back


def test_current_frame_first_non_approved():
    s = _new_state()
    s["frame_order"] = [1, 2, 3]
    for n in (1, 2, 3):
        st.set_frame(s, n, {"status": "pending", "attempts": [],
                            "approved_attempt": None, "approved_path": None})
    assert st.current_frame(s) == 1
    st.get_frame(s, 1)["status"] = "approved"
    assert st.current_frame(s) == 2
    for n in (2, 3):
        st.get_frame(s, n)["status"] = "approved"
    assert st.current_frame(s) is None
    # PLAN-era state has no frames yet
    assert st.current_frame(_new_state()) is None


# ---------- CLI skeleton ----------


def test_status_renders_without_advancing(tmp_path, capsys):
    s = _new_state()
    st.save_state(tmp_path, s)
    before = (tmp_path / "run_state.json").read_bytes()

    rc = run_cli.main(["--resume", str(tmp_path), "--status"])

    assert rc == 0
    out = capsys.readouterr().out
    assert "PLAN" in out
    assert "2026-06-12-ss-run" in out
    # --status never writes
    assert (tmp_path / "run_state.json").read_bytes() == before


def test_resume_missing_state_errors_cleanly(tmp_path, capsys):
    rc = run_cli.main(["--resume", str(tmp_path / "nope"), "--status"])
    assert rc == 2
    err = capsys.readouterr().err
    assert "run_state.json" in err


def test_action_in_wrong_stage_rejected(tmp_path, capsys):
    s = _new_state()  # stage == PLAN
    st.save_state(tmp_path, s)

    rc = run_cli.main(["--resume", str(tmp_path), "--approve-frame", "1"])

    assert rc == 2
    err = capsys.readouterr().err
    assert "GENERATE" in err  # the message names the stage the action needs
    # state untouched
    assert st.load_state(tmp_path)["stage"] == "PLAN"
