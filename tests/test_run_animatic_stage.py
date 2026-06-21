"""Phase 4 — the opt-in ANIMATIC stage inside the run orchestrator.

A human author-and-ingest gate between STORYBOARD and GENERATE (mirrors the
storyboard curation gate, but human-authored — no LLM call). Sean drops
frame-named placement roughs into runs/<id>/animatic/ + an optional holds.json;
--approve-animatic deterministically ingests them (each rough -> a real frame id,
the sidecar parses), populates run-state refs + holds (the locked board is never
mutated), and hands off to the shared enter_generate.

Opt-in, default off: --animatic (or manifest animatic.enabled) switches it on per
run. A run without it goes STORYBOARD -> GENERATE byte-identical to today, and a
back-compat brief (carrying shots.yaml) never enters ANIMATIC at all.

$0 stub-green throughout (--stub exports ANIMA_FORCE_STUB).
"""

from __future__ import annotations

import json

import yaml

from pipeline import run as run_cli
from pipeline.orchestration import animatic_stage
from pipeline.orchestration import state as st
from tests.orch_fixtures import (
    fake_ffmpeg_path,
    mk_project,
    spy_flo_stub,
    stub_critic_env,
)

AUTHORING_CAST = (("sean-anchor", "sean"), ("claude-mascot", "claude-mascot"))


def _approve_all_frames_to_done(run_dir) -> None:
    for _ in range(50):
        state = st.load_state(run_dir)
        if state["stage"] == "DONE":
            return
        assert state["stage"] == "GENERATE", f"unexpected stage {state['stage']}"
        n = st.current_frame(state)
        assert n is not None
        assert run_cli.main(["--resume", str(run_dir), "--approve-frame", str(n)]) == 0
    raise AssertionError("did not reach DONE within the frame bound")


# ---------- the deterministic ingest (unit) ----------


def test_ingest_maps_frame_named_roughs_and_holds(tmp_path):
    adir = tmp_path / "animatic"
    adir.mkdir()
    (adir / "F01.png").write_bytes(b"x")
    (adir / "F03.png").write_bytes(b"x")           # per-frame optional: F02 has no rough
    (adir / "holds.json").write_text(json.dumps({"1": 5, "3": 4}), encoding="utf-8")

    refs, holds = animatic_stage.ingest_animatic({1, 2, 3}, adir)

    assert refs == {"1": str(adir / "F01.png"), "3": str(adir / "F03.png")}
    assert holds == {"1": 5, "3": 4}


def test_ingest_padding_insensitive_and_no_sidecar(tmp_path):
    adir = tmp_path / "animatic"
    adir.mkdir()
    (adir / "F1.png").write_bytes(b"x")             # unpadded also maps to frame 1
    refs, holds = animatic_stage.ingest_animatic({1, 2}, adir)
    assert refs == {"1": str(adir / "F1.png")}
    assert holds == {}                              # no sidecar -> no override


def test_ingest_rejects_rough_naming_a_frame_not_in_the_board(tmp_path):
    adir = tmp_path / "animatic"
    adir.mkdir()
    (adir / "F09.png").write_bytes(b"x")            # board only has 1..3
    try:
        animatic_stage.ingest_animatic({1, 2, 3}, adir)
    except ValueError as e:
        assert "9" in str(e)
    else:
        raise AssertionError("expected ValueError for an out-of-board rough")


def test_ingest_rejects_bad_holds_sidecar(tmp_path):
    adir = tmp_path / "animatic"
    adir.mkdir()
    # unknown frame
    (adir / "holds.json").write_text(json.dumps({"9": 3}), encoding="utf-8")
    try:
        animatic_stage.ingest_animatic({1, 2, 3}, adir)
        raise AssertionError("expected ValueError for unknown-frame hold")
    except ValueError:
        pass
    # non-positive hold
    (adir / "holds.json").write_text(json.dumps({"1": 0}), encoding="utf-8")
    try:
        animatic_stage.ingest_animatic({1, 2, 3}, adir)
        raise AssertionError("expected ValueError for hold < 1")
    except ValueError:
        pass


# ---------- the legal-transition change ----------


def test_animatic_is_between_storyboard_and_generate():
    assert st.STAGES == ("PLAN", "SCRIPT", "STORYBOARD", "ANIMATIC", "GENERATE",
                         "ASSEMBLE", "DONE")
    # STORYBOARD keeps GENERATE (the animatic-off path) AND gains ANIMATIC
    assert set(st._LEGAL_TRANSITIONS["STORYBOARD"]) == {"ANIMATIC", "GENERATE"}
    assert st._LEGAL_TRANSITIONS["ANIMATIC"] == ("GENERATE",)


# ---------- the headline: authoring + animatic reaches DONE, fully offline ----------


def test_authoring_walk_with_animatic_reaches_done(tmp_path, monkeypatch):
    root, brief_dir = mk_project(tmp_path, monkeypatch, with_shots=False, cast=AUTHORING_CAST)
    stub_critic_env(monkeypatch)
    spy_flo_stub(monkeypatch)
    fake_ffmpeg_path(tmp_path, monkeypatch)
    run_dir = root / "runs" / "anim-run"

    assert run_cli.main([
        "--brief", str(brief_dir), "--stub", "--animatic", "--slug", "SS",
        "--run-dir", str(run_dir),
    ]) == 0
    assert st.load_state(run_dir)["animatic_enabled"] is True

    assert run_cli.main(["--resume", str(run_dir), "--approve-plan"]) == 0
    assert run_cli.main(["--resume", str(run_dir), "--approve-script"]) == 0

    # storyboard-approve now routes to ANIMATIC (not straight to GENERATE)
    assert run_cli.main(["--resume", str(run_dir), "--approve-storyboard"]) == 0
    state = st.load_state(run_dir)
    assert state["stage"] == "ANIMATIC"
    assert state["animatic"]["status"] == "awaiting"
    adir = run_dir / "animatic"
    assert adir.is_dir()                            # the stage made the drop dir

    # Sean drops a placement rough for frame 1 + a holds override
    shot_ids = [s["id"] if isinstance(s, dict) else s
                for s in yaml.safe_load((run_dir / "brief" / "shots.yaml").read_text())["frames"]]
    first = sorted(shot_ids)[0]
    (adir / f"F{first:02d}.png").write_bytes(b"x")
    (adir / "holds.json").write_text(json.dumps({str(first): 5}), encoding="utf-8")

    # approve-animatic ingests + enters GENERATE (frame 1 fanned)
    assert run_cli.main(["--resume", str(run_dir), "--approve-animatic"]) == 0
    state = st.load_state(run_dir)
    assert state["stage"] == "GENERATE"
    assert state["animatic"]["status"] == "ingested"
    assert state["animatic"]["refs"][str(first)] == str(adir / f"F{first:02d}.png")
    assert state["holds"][str(first)] == 5          # sidecar override beat the board hold
    assert st.get_frame(state, first)["status"] == "generated"

    _approve_all_frames_to_done(run_dir)
    assert st.load_state(run_dir)["stage"] == "DONE"
    # the timing half landed: the sidecar hold rode through to the assembled sequence
    seq = (run_dir / "export" / "sequence.txt").read_text()
    assert f"SS_F{first:02d}_key:5" in seq


# ---------- Fix B: the ANIMATIC gate states the board count ----------


def test_animatic_gate_surfaces_board_frame_count(tmp_path, monkeypatch, capsys):
    """The ANIMATIC gate states the board's frame COUNT explicitly so a rough/board
    mismatch (the 2026-06-21 7-roughs-vs-5-board) is visible BEFORE dropping."""
    root, brief_dir = mk_project(tmp_path, monkeypatch, with_shots=False, cast=AUTHORING_CAST)
    stub_critic_env(monkeypatch)
    run_dir = root / "runs" / "anim-count-run"
    assert run_cli.main([
        "--brief", str(brief_dir), "--stub", "--animatic", "--slug", "SS",
        "--frames", "7", "--run-dir", str(run_dir),
    ]) == 0
    assert run_cli.main(["--resume", str(run_dir), "--approve-plan"]) == 0
    assert run_cli.main(["--resume", str(run_dir), "--approve-script"]) == 0
    capsys.readouterr()  # clear prior output
    assert run_cli.main(["--resume", str(run_dir), "--approve-storyboard"]) == 0

    assert st.load_state(run_dir)["stage"] == "ANIMATIC"
    out = capsys.readouterr().out
    assert "Board has 7 frame(s)" in out  # the explicit count, not just ids


# ---------- default off: authoring without --animatic skips the stage ----------


def test_authoring_without_animatic_skips_stage_to_generate(tmp_path, monkeypatch):
    root, brief_dir = mk_project(tmp_path, monkeypatch, with_shots=False, cast=AUTHORING_CAST)
    stub_critic_env(monkeypatch)
    spy_flo_stub(monkeypatch)
    run_dir = root / "runs" / "noanim-run"

    assert run_cli.main([
        "--brief", str(brief_dir), "--stub", "--slug", "SS", "--run-dir", str(run_dir),
    ]) == 0
    assert st.load_state(run_dir)["animatic_enabled"] is False

    assert run_cli.main(["--resume", str(run_dir), "--approve-plan"]) == 0
    assert run_cli.main(["--resume", str(run_dir), "--approve-script"]) == 0
    assert run_cli.main(["--resume", str(run_dir), "--approve-storyboard"]) == 0

    # straight to GENERATE, no ANIMATIC, no animatic substate
    state = st.load_state(run_dir)
    assert state["stage"] == "GENERATE"
    assert "animatic" not in state or not state.get("animatic")


# ---------- the timing half: animatic holds drive ASSEMBLE ----------


def test_animatic_holds_drive_the_assemble_sequence_file(tmp_path):
    """The override the ingest writes to state['holds'] (via enter_generate) is what
    assemble_stage.write_sequence_file consumes — the timing half's real consumer."""
    from pipeline.orchestration.assemble_stage import write_sequence_file

    # frame 1's hold overridden to 5 by an animatic sidecar; frame 2 keeps the board's 2
    state = {"slug": "TT", "frame_order": [1, 2], "holds": {"1": 5, "2": 2}}
    seq = write_sequence_file(state, tmp_path)

    assert seq.read_text().strip().splitlines() == ["TT_F01_key:5", "TT_F02_key:2"]


# ---------- the gate guard ----------


def test_manifest_animatic_enabled_turns_the_gate_on_without_the_flag(tmp_path, monkeypatch):
    """manifest animatic.enabled: true is the other on-switch (no --animatic needed)."""
    root, brief_dir = mk_project(tmp_path, monkeypatch, with_shots=False, cast=AUTHORING_CAST)
    stub_critic_env(monkeypatch)
    manifest_path = root / "manifest.yaml"
    data = yaml.safe_load(manifest_path.read_text())
    data["animatic"] = {"enabled": True}
    manifest_path.write_text(yaml.safe_dump(data), encoding="utf-8")
    run_dir = root / "runs" / "manifest-anim-run"

    assert run_cli.main([
        "--brief", str(brief_dir), "--stub", "--slug", "SS", "--run-dir", str(run_dir),
    ]) == 0
    assert st.load_state(run_dir)["animatic_enabled"] is True


def test_approve_animatic_only_applies_in_animatic_stage(tmp_path, monkeypatch, capsys):
    root, brief_dir = mk_project(tmp_path, monkeypatch)  # back-compat brief
    stub_critic_env(monkeypatch)
    spy_flo_stub(monkeypatch)
    run_dir = root / "runs" / "guard-run"
    assert run_cli.main(["--brief", str(brief_dir), "--stub", "--run-dir", str(run_dir)]) == 0

    rc = run_cli.main(["--resume", str(run_dir), "--approve-animatic"])

    assert rc == 2
    assert "animatic" in capsys.readouterr().err.lower()
