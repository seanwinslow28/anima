"""Tests for pipeline.cli.plan — init / show / approve / mutate subcommands."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.cli.plan import (
    approve_plan,
    init_plan,
    mutate_plan,
    render_plan_markdown,
    show_plan,
)


# ---- plan init ----


def test_init_scaffolds_brief_dir_with_both_templates(tmp_path):
    target = tmp_path / "briefs" / "2026-05-27-test"
    rc = init_plan(str(target))
    assert rc == 0
    assert (target / "00_studio_brief.md").exists()
    assert (target / "01_production_brief.md").exists()
    # Studio Brief should contain the "what this is NOT" anchor from the template.
    studio = (target / "00_studio_brief.md").read_text(encoding="utf-8")
    assert "What this is NOT" in studio


def test_init_preserves_existing_files(tmp_path):
    target = tmp_path / "briefs" / "2026-05-27-existing"
    target.mkdir(parents=True)
    (target / "00_studio_brief.md").write_text("EXISTING\n")
    rc = init_plan(str(target))
    assert rc == 0
    # Existing file untouched.
    assert (target / "00_studio_brief.md").read_text() == "EXISTING\n"
    # The other one is still created.
    assert (target / "01_production_brief.md").exists()


# ---- plan show / render_plan_markdown ----


def test_render_adds_ascii_boxes_to_cost_preview():
    """render_plan_markdown adds box chars to the Cost preview section only."""
    md = (
        "# Plan\n\n"
        "## Cost preview\n\n"
        "Low: $5\nMedian: $12\nHigh: $30\n\n"
        "## Phases\n\n"
        "Phase 5 keyframes, Phase 6 Seedance.\n"
    )
    out = render_plan_markdown(md)
    # Box characters appear in rendered output.
    assert any(ch in out for ch in "╔═╗║╚╝")
    # But the Phases section (not in _BOX_SECTIONS) stays as plain markdown.
    assert "## Phases" in out


def test_render_leaves_source_markdown_clean():
    """Rendering is a pure function — the source plan.md text is unchanged."""
    md = "# Plan\n\n## Cost preview\n\nLow $5\n"
    render_plan_markdown(md)
    # No box characters in the input.
    for ch in "╔═╗║╚╝":
        assert ch not in md


def test_show_reads_plan_and_writes_to_stdout(tmp_path, capsys):
    plan = tmp_path / "plan.md"
    plan.write_text("# Plan\n\n## Cost preview\n\nLow $5\n", encoding="utf-8")
    rc = show_plan(str(plan))
    assert rc == 0
    out = capsys.readouterr().out
    assert "╔" in out or "═" in out


def test_show_missing_plan_returns_error(tmp_path, capsys):
    rc = show_plan(str(tmp_path / "nope.md"))
    assert rc == 1
    err = capsys.readouterr().err
    assert "not found" in err


# ---- plan approve ----


def test_approve_flips_locked_true(tmp_path):
    bd = tmp_path / "briefs" / "test"
    bd.mkdir(parents=True)
    crit = {"version": "1.1", "locked": False, "criteria": []}
    (bd / "acceptance_criteria.json").write_text(json.dumps(crit), encoding="utf-8")
    rc = approve_plan(str(bd))
    assert rc == 0
    loaded = json.loads((bd / "acceptance_criteria.json").read_text(encoding="utf-8"))
    assert loaded["locked"] is True


def test_approve_resolves_symlink_before_writing(tmp_path):
    """When acceptance_criteria.json is a symlink, the underlying versioned
    file gets the locked=true flip, not the symlink."""
    bd = tmp_path / "briefs" / "test"
    bd.mkdir(parents=True)
    versioned = bd / "acceptance_criteria-1.1.0.json"
    versioned.write_text(json.dumps({"version": "1.1", "locked": False, "criteria": []}))
    (bd / "acceptance_criteria.json").symlink_to("acceptance_criteria-1.1.0.json")
    rc = approve_plan(str(bd))
    assert rc == 0
    raw = json.loads(versioned.read_text(encoding="utf-8"))
    assert raw["locked"] is True


def test_approve_idempotent_when_already_locked(tmp_path, capsys):
    bd = tmp_path / "briefs" / "test"
    bd.mkdir(parents=True)
    (bd / "acceptance_criteria.json").write_text(json.dumps({"version": "1.1", "locked": True, "criteria": []}))
    rc = approve_plan(str(bd))
    assert rc == 0
    out = capsys.readouterr().out
    assert "already locked" in out


# ---- plan mutate ----


def test_mutate_refuses_without_force(tmp_path, capsys):
    bd = tmp_path / "briefs" / "test"
    bd.mkdir(parents=True)
    (bd / "acceptance_criteria.json").write_text(json.dumps({"version": "1.1", "locked": True, "criteria": []}))
    rc = mutate_plan(
        run_dir=str(tmp_path / "runs" / "test"),
        brief_dir=str(bd),
        force=False,
        actor="sean",
        reason="test",
        target="AC.tone.example",
        field="impact_tag",
        value="aesthetic",
        new_version="1.2.0",
    )
    assert rc == 1
    err = capsys.readouterr().err
    assert "--force" in err


def test_mutate_requires_actor_and_reason(tmp_path, capsys):
    bd = tmp_path / "briefs" / "test"
    bd.mkdir(parents=True)
    (bd / "acceptance_criteria.json").write_text(json.dumps({"version": "1.1", "locked": True, "criteria": []}))
    rc = mutate_plan(
        run_dir=str(tmp_path / "runs" / "test"),
        brief_dir=str(bd),
        force=True,
        actor="",
        reason="",
        target="AC.tone.example",
        field="impact_tag",
        value="aesthetic",
        new_version="1.2.0",
    )
    assert rc == 1


def test_mutate_writes_audit_jsonl_and_bumps_version(tmp_path):
    bd = tmp_path / "briefs" / "test"
    bd.mkdir(parents=True)
    versioned = bd / "acceptance_criteria-1.1.0.json"
    versioned.write_text(json.dumps({"version": "1.1", "locked": True, "criteria": []}))
    (bd / "acceptance_criteria.json").symlink_to("acceptance_criteria-1.1.0.json")
    (bd / "plan.md").write_text(
        "# Plan\n\n## Cost preview\n\nLow $5\n", encoding="utf-8",
    )
    run_dir = tmp_path / "runs" / "test_run"

    rc = mutate_plan(
        run_dir=str(run_dir),
        brief_dir=str(bd),
        force=True,
        actor="sean",
        reason="tighten timing tolerance",
        target="AC.timing.beat3-hold",
        field="tolerance",
        value="0.15",
        new_version="1.2.0",
    )
    assert rc == 0

    # New versioned file exists; symlink re-pointed.
    assert (bd / "acceptance_criteria-1.2.0.json").exists()
    assert (bd / "acceptance_criteria.json").is_symlink()
    new_raw = json.loads((bd / "acceptance_criteria.json").read_text(encoding="utf-8"))
    assert new_raw["version"] == "1.2.0"

    # Audit log has one line with the mutation record.
    audit_path = run_dir / "plan_audit.jsonl"
    assert audit_path.exists()
    lines = audit_path.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["actor"] == "sean"
    assert record["reason"] == "tighten timing tolerance"
    assert record["target"] == "AC.timing.beat3-hold"
    assert record["field"] == "tolerance"
    assert record["value"] == "0.15"
    assert record["criteria_version_from"] == "1.1"
    assert record["criteria_version_to"] == "1.2.0"

    # plan.md got the delta block prepended.
    plan = (bd / "plan.md").read_text(encoding="utf-8")
    assert "Plan changes since approval (1)" in plan
    assert "tighten timing tolerance" in plan


def test_mutate_appends_audit_lines_across_invocations(tmp_path):
    """Second mutate adds a second JSONL line and bumps the delta counter."""
    bd = tmp_path / "briefs" / "test"
    bd.mkdir(parents=True)
    versioned = bd / "acceptance_criteria-1.1.0.json"
    versioned.write_text(json.dumps({"version": "1.1", "locked": True, "criteria": []}))
    (bd / "acceptance_criteria.json").symlink_to("acceptance_criteria-1.1.0.json")
    (bd / "plan.md").write_text("# Plan\n\n", encoding="utf-8")
    run_dir = tmp_path / "runs" / "test_run"

    mutate_plan(
        run_dir=str(run_dir), brief_dir=str(bd), force=True,
        actor="sean", reason="first", target="AC.x.y", field="f", value="1",
        new_version="1.2.0",
    )
    mutate_plan(
        run_dir=str(run_dir), brief_dir=str(bd), force=True,
        actor="sean", reason="second", target="AC.x.z", field="f", value="2",
        new_version="1.3.0",
    )
    lines = (run_dir / "plan_audit.jsonl").read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 2
    plan = (bd / "plan.md").read_text(encoding="utf-8")
    assert "Plan changes since approval (2)" in plan
