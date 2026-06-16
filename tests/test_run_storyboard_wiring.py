"""Phase 3 wiring — the SCRIPT + STORYBOARD stages inside the run orchestrator.

The deliberate third Phase-3 slice: `python -m pipeline.run` drives Maya -> Sam
-> Bea -> human-curate -> Flo/Em -> assemble as one resumable program. Two new
gates (--approve-script, --approve-storyboard) sit between the plan gate and
GENERATE, chosen at start by a needs_storyboard flag:

  authoring brief (00_studio_brief.md, no shots.yaml):
    PLAN -> SCRIPT (Sam) -> STORYBOARD (Bea) -> GENERATE -> ASSEMBLE -> DONE
  back-compat brief (carries shots.yaml):
    PLAN -> GENERATE -> ASSEMBLE -> DONE         (SCRIPT/STORYBOARD skipped)

$0 stub-green: --stub exports ANIMA_FORCE_STUB, so Sam (Opus) + Bea (Sonnet)
fall back to their deterministic stubs and no transport goes live. The
authoring walk reaches DONE with no key; the back-compat brief is byte-unchanged.
"""

from __future__ import annotations

import json

import yaml

from pipeline import run as run_cli
from pipeline.orchestration import state as st
from tests.orch_fixtures import (
    fake_ffmpeg_path,
    mk_project,
    spy_flo_stub,
    stub_critic_env,
)

# Folder-key / IR-namespace pairs matching Sam's deterministic stub cast
# (scriptwriter._stub_sam_text emits sean / claude-mascot).
AUTHORING_CAST = (("sean-anchor", "sean"), ("claude-mascot", "claude-mascot"))


def _approve_all_frames_to_done(run_dir) -> None:
    """Eye-gate loop: approve the current frame until the run reaches DONE."""
    for _ in range(50):  # generous bound; the stub board is 5 frames
        state = st.load_state(run_dir)
        if state["stage"] == "DONE":
            return
        assert state["stage"] == "GENERATE", f"unexpected stage {state['stage']}"
        n = st.current_frame(state)
        assert n is not None
        assert run_cli.main(["--resume", str(run_dir), "--approve-frame", str(n)]) == 0
    raise AssertionError("did not reach DONE within the frame bound")


# ---------- the headline: the authoring stub-walk reaches DONE, fully offline ----------


def test_authoring_stub_walk_plan_to_script_to_storyboard_to_done(tmp_path, monkeypatch):
    root, brief_dir = mk_project(
        tmp_path, monkeypatch, with_shots=False, cast=AUTHORING_CAST
    )
    stub_critic_env(monkeypatch)   # Em transports -> stubs (Sam/Bea via ANIMA_FORCE_STUB)
    spy_flo_stub(monkeypatch)
    fake_ffmpeg_path(tmp_path, monkeypatch)
    run_dir = root / "runs" / "authoring-run"

    # start: no shots.yaml -> authoring mode; --slug required (no board to read it from)
    assert run_cli.main([
        "--brief", str(brief_dir), "--stub", "--slug", "SS", "--run-dir", str(run_dir),
    ]) == 0
    state = st.load_state(run_dir)
    assert state["stage"] == "PLAN"
    assert state["needs_storyboard"] is True
    assert state["slug"] == "SS"

    # plan gate -> SCRIPT (Sam drafts beats.json into the snapshot)
    assert run_cli.main(["--resume", str(run_dir), "--approve-plan"]) == 0
    state = st.load_state(run_dir)
    assert state["stage"] == "SCRIPT"
    assert state["script"]["status"] == "drafted"
    assert (run_dir / "brief" / "beats.json").exists()
    assert (run_dir / "brief" / "script.md").exists()

    # script gate -> STORYBOARD (beats locked; Bea drafts shots.yaml)
    assert run_cli.main(["--resume", str(run_dir), "--approve-script"]) == 0
    state = st.load_state(run_dir)
    assert state["stage"] == "STORYBOARD"
    assert state["storyboard"]["status"] == "drafted"
    beats = json.loads((run_dir / "brief" / "beats.json").read_text())
    assert beats["locked"] is True
    shots_path = run_dir / "brief" / "shots.yaml"
    assert shots_path.exists()
    assert state["shots_path"] == str(shots_path)  # established at the storyboard stage

    # curation gate -> GENERATE (board validated + locked; frame 1 fanned)
    assert run_cli.main(["--resume", str(run_dir), "--approve-storyboard"]) == 0
    state = st.load_state(run_dir)
    assert state["stage"] == "GENERATE"
    assert yaml.safe_load(shots_path.read_text())["locked"] is True
    assert state["frame_order"]  # seeded from Bea's board
    assert st.get_frame(state, state["frame_order"][0])["status"] == "generated"

    # eye-gate loop -> DONE, all offline ($0)
    _approve_all_frames_to_done(run_dir)
    state = st.load_state(run_dir)
    assert state["stage"] == "DONE"
    assert state["assemble"]["gif"]  # loop assembled


# ---------- back-compat: a provided shots.yaml still skips authoring ----------


def test_backcompat_brief_with_shots_skips_to_generate(tmp_path, monkeypatch):
    root, brief_dir = mk_project(tmp_path, monkeypatch)  # default: carries shots.yaml
    stub_critic_env(monkeypatch)
    spy_flo_stub(monkeypatch)
    run_dir = root / "runs" / "bc-run"

    assert run_cli.main(["--brief", str(brief_dir), "--stub", "--run-dir", str(run_dir)]) == 0
    state = st.load_state(run_dir)
    assert state["needs_storyboard"] is False
    assert state["stage"] == "PLAN"

    # plan gate goes straight to GENERATE (SCRIPT/STORYBOARD skipped), as today
    assert run_cli.main(["--resume", str(run_dir), "--approve-plan"]) == 0
    state = st.load_state(run_dir)
    assert state["stage"] == "GENERATE"
    assert "script" not in state  # authoring stages never ran


def test_authoring_brief_requires_slug(tmp_path, monkeypatch):
    root, brief_dir = mk_project(
        tmp_path, monkeypatch, with_shots=False, cast=AUTHORING_CAST
    )
    stub_critic_env(monkeypatch)
    run_dir = root / "runs" / "noslug-run"

    rc = run_cli.main(["--brief", str(brief_dir), "--stub", "--run-dir", str(run_dir)])

    assert rc == 2  # no shots.yaml to read a slug from, and no --slug given
