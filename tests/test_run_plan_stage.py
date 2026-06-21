"""P1 — the PLAN stage (seams #1, #4, #8).

--brief drives Maya (PlannerNode) behind author_plan.py's extracted guards
(live-Opus smoke + the silent-stub marker scan), emits the Phase-0 artifacts,
and stops at the plan gate. --approve-plan locks the brief criteria, wires
criteria_sources.brief_file in-memory, builds the merged bundle once
(load_all_criteria), and enters GENERATE.
"""

from __future__ import annotations

import hashlib
import json

import pytest

from pipeline import run as run_cli
from pipeline.orchestration import generate_stage
from pipeline.orchestration import guards
from pipeline.orchestration import state as st
from tests.orch_fixtures import force_stub_sdk, mk_project


def _start_stub_run(root, brief_dir):
    run_dir = root / "runs" / "tt-run"
    rc = run_cli.main([
        "--brief", str(brief_dir), "--stub", "--run-dir", str(run_dir),
        "--manifest", "manifest.yaml",
    ])
    return rc, run_dir


def test_brief_runs_maya_stub_and_stops_at_plan_gate(tmp_path, monkeypatch, capsys):
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    force_stub_sdk(monkeypatch)

    rc, run_dir = _start_stub_run(root, brief_dir)

    assert rc == 0
    # Fix B: Maya writes into the run-local snapshot, never the committed brief
    assert (run_dir / "brief" / "plan.md").exists()
    assert (run_dir / "brief" / "acceptance_criteria.json").exists()
    assert not (brief_dir / "plan.md").exists()
    state = st.load_state(run_dir)
    assert state["stage"] == "PLAN"
    assert state["plan"]["status"] == "drafted"
    assert state["plan"]["stub"] is True  # a stub plan is recorded as such, never silently real
    assert state["slug"] == "TT"  # from shots.yaml
    assert [m["ir_namespace"] for m in state["cast"]] == ["al", "be"]
    out = capsys.readouterr().out
    assert "approve-plan" in out  # the gate prints the next command


def test_stub_marker_blocks_without_stub_flag(tmp_path, monkeypatch, capsys):
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    force_stub_sdk(monkeypatch)

    run_dir = root / "runs" / "tt-run"
    rc = run_cli.main([
        "--brief", str(brief_dir), "--skip-smoke", "--run-dir", str(run_dir),
        "--manifest", "manifest.yaml",
    ])

    assert rc == 1  # the silent-stub trap, now a hard guard
    err = capsys.readouterr().err
    assert "STUB" in err
    state = st.load_state(run_dir)
    assert state["plan"]["status"] != "drafted"  # never presentable at the gate


def test_smoke_guard_raises_on_stub_path(monkeypatch):
    force_stub_sdk(monkeypatch)
    with pytest.raises(guards.GuardError, match="STUB"):
        guards.smoke_live_opus()


def test_api_key_present_refused_without_allow(tmp_path, monkeypatch, capsys):
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")

    rc = run_cli.main(["--brief", str(brief_dir), "--stub", "--run-dir", str(root / "runs" / "x")])

    assert rc == 1
    assert "ANTHROPIC_API_KEY" in capsys.readouterr().err


def test_approve_plan_locks_criteria_and_advances(tmp_path, monkeypatch, capsys):
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    force_stub_sdk(monkeypatch)
    rc, run_dir = _start_stub_run(root, brief_dir)
    assert rc == 0

    fan_calls = []

    def fake_generate_current_frame(state, manifest, bundle, run_dir):
        fan_calls.append({"state": state, "manifest": manifest,
                          "bundle": bundle, "run_dir": run_dir})
        n = st.current_frame(state)
        st.get_frame(state, n)["status"] = "generated"
        st.get_frame(state, n)["attempts"].append({"index": 1})
        st.save_state(run_dir, state)
        return 0

    monkeypatch.setattr(generate_stage, "generate_current_frame", fake_generate_current_frame)

    rc = run_cli.main(["--resume", str(run_dir), "--approve-plan"])

    assert rc == 0
    # criteria locked on disk — in the run-local snapshot (Fix B)
    raw = json.loads((run_dir / "brief" / "acceptance_criteria.json").read_text())
    assert raw["locked"] is True
    # state advanced, shots persisted, frame 1 attempted
    state = st.load_state(run_dir)
    assert state["stage"] == "GENERATE"
    assert state["plan"]["status"] == "approved"
    assert state["frame_order"] == [1, 2]
    assert state["holds"] == {"1": 2, "2": 3}
    assert len(st.get_frame(state, 1)["attempts"]) == 1
    assert len(fan_calls) == 1


def test_approve_plan_refuses_to_lock_illegal_criteria(tmp_path, monkeypatch, capsys):
    """An illegal impact_tag in the brief criteria can NEVER lock — the gate
    refuses at plan-approve, not four gates later (the cancelled 2026-06-21 run).
    Defense in depth: even if a bad criteria file lands in the snapshot (hand
    edit, bad merge), the human gate refuses it."""
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    force_stub_sdk(monkeypatch)
    rc, run_dir = _start_stub_run(root, brief_dir)
    assert rc == 0

    snap_criteria = run_dir / "brief" / "acceptance_criteria.json"
    snap_criteria.write_text(json.dumps({
        "version": "1.1", "locked": False, "criteria": [{
            "id": "AC.timing.on-twos",
            "description": "Animate on twos; enforcement is structural, not perceptual.",
            "cites_phase": [4, 8],
            "cites_personas": [],
            "impact_tag": "timing",  # illegal — a category, not an impact_tag
            "parent_id": None,
            "derived_from": ["studio_brief.timing"],
        }],
    }), encoding="utf-8")

    rc = run_cli.main(["--resume", str(run_dir), "--approve-plan"])

    assert rc != 0
    assert "impact_tag" in capsys.readouterr().err  # the legal-set message at the gate
    # never locked, never advanced past PLAN
    raw = json.loads(snap_criteria.read_text())
    assert raw["locked"] is False
    state = st.load_state(run_dir)
    assert state["stage"] == "PLAN"
    assert state["plan"]["status"] == "drafted"


def test_approve_plan_wires_brief_file_and_merges_bundle(tmp_path, monkeypatch):
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    force_stub_sdk(monkeypatch)
    rc, run_dir = _start_stub_run(root, brief_dir)
    assert rc == 0

    seen = {}

    def fake_generate_current_frame(state, manifest, bundle, run_dir):
        seen["manifest"] = manifest
        seen["bundle"] = bundle
        return 0

    monkeypatch.setattr(generate_stage, "generate_current_frame", fake_generate_current_frame)

    rc = run_cli.main(["--resume", str(run_dir), "--approve-plan"])

    assert rc == 0
    # brief_file wired in-memory from state.brief_dir — the run-local snapshot
    # under Fix B (manifest.yaml on disk never edited)
    assert seen["manifest"]["criteria_sources"]["brief_file"] == str(
        run_dir / "brief" / "acceptance_criteria.json"
    )
    import yaml
    on_disk = yaml.safe_load((root / "manifest.yaml").read_text())
    assert "brief_file" not in on_disk["criteria_sources"]
    # the merged bundle carries Maya's AC.* AND both Bibles' IR.*
    ids = {c.id for c in seen["bundle"].criteria}
    assert "AC.technical.aspect-ratio-16-9" in ids  # the stub planner's criterion
    assert "IR.al.style.line-weight" in ids
    assert "IR.be.style.line-weight" in ids


def _md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def test_brief_snapshot_leaves_committed_brief_byte_unchanged(tmp_path, monkeypatch):
    """Fix B regression (the 2026-06-11 audit clobber): PLAN writes into
    run_dir/brief/, never the committed brief dir."""
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    force_stub_sdk(monkeypatch)
    # Mimic a committed brief that already carries Maya artifacts (spark-shared shape)
    (brief_dir / "plan.md").write_text("# committed plan — do not clobber\n")
    (brief_dir / "acceptance_criteria.json").write_text(
        '{"version": "1.1", "locked": true, "criteria": []}\n')
    (brief_dir / "01_production_brief.md").write_text("# committed production brief\n")
    before = {p.name: _md5(p) for p in sorted(brief_dir.iterdir()) if p.is_file()}

    rc, run_dir = _start_stub_run(root, brief_dir)

    assert rc == 0
    after = {p.name: _md5(p) for p in sorted(brief_dir.iterdir()) if p.is_file()}
    assert after == before  # the committed brief is byte-identical
    # the run-local snapshot carries the GENERATED artifacts
    snap = run_dir / "brief"
    assert (snap / "plan.md").exists()
    assert (snap / "acceptance_criteria.json").exists()
    assert _md5(snap / "plan.md") != before["plan.md"]
    state = st.load_state(run_dir)
    assert state["brief_dir"] == str(snap)
    assert state["shots_path"] == str(snap / "shots.yaml")


def test_resume_after_snapshot_finds_brief_and_shots(tmp_path, monkeypatch):
    """--resume after the snapshot still finds brief + shots (Fix B durability)."""
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    force_stub_sdk(monkeypatch)
    rc, run_dir = _start_stub_run(root, brief_dir)
    assert rc == 0

    # Fix-A-independent fan stand-in (same pattern as the approve-plan tests).
    def fake_generate_current_frame(state, manifest, bundle, run_dir):
        n = st.current_frame(state)
        st.get_frame(state, n)["status"] = "generated"
        st.get_frame(state, n)["attempts"].append({"index": 1})
        st.save_state(run_dir, state)
        return 0

    monkeypatch.setattr(generate_stage, "generate_current_frame", fake_generate_current_frame)

    # status resumes cleanly; approve-plan locks the SNAPSHOT criteria and loads shots
    assert run_cli.main(["--resume", str(run_dir), "--status"]) == 0
    assert run_cli.main(["--resume", str(run_dir), "--approve-plan"]) == 0
    state = st.load_state(run_dir)
    assert state["stage"] == "GENERATE"
    assert state["frame_order"] == [1, 2]  # shots.yaml found via the snapshot
    raw = json.loads((run_dir / "brief" / "acceptance_criteria.json").read_text())
    assert raw["locked"] is True
