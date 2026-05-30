"""Tests for pipeline.cli.plan — init / show / approve / mutate subcommands."""

from __future__ import annotations

import json
from pathlib import Path

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


def _seed_brief(bd: Path) -> None:
    """Seed a brief dir with a regular-file v1.1 criteria carrying two AC rules
    plus a plan.md. mutate_plan now edits a rule in place (not bump_version),
    so the criteria must hold a real rule to edit."""
    bd.mkdir(parents=True, exist_ok=True)
    crit = {
        "version": "1.1",
        "locked": True,
        "criteria": [
            {
                "id": "AC.identity.sean-jaw",
                "description": "Sean's jaw is square.",
                "cites_phase": [5],
                "cites_personas": ["em"],
                "impact_tag": "identity_critical",
            },
            {
                "id": "AC.timing.beat3-hold",
                "description": "Beat 3 holds two beats.",
                "cites_phase": [4],
                "cites_personas": ["em"],
                "impact_tag": "structural",
            },
        ],
    }
    (bd / "acceptance_criteria.json").write_text(json.dumps(crit, indent=2), encoding="utf-8")
    (bd / "plan.md").write_text("# Plan\n\n## Cost preview\n\nLow $5\n", encoding="utf-8")


def test_mutate_edits_rule_in_place_and_stays_loadable(tmp_path):
    """The fixed contract: mutate edits the rule in place, keeps the schema
    `version` field loadable, and records the content revision separately —
    the 2026-05-30 sibling-bug fix mirrored from `bible mutate`."""
    from pipeline.criteria import load_criteria

    bd = tmp_path / "briefs" / "2026-05-27-test"
    _seed_brief(bd)
    run_dir = tmp_path / "runs" / "r1"

    rc = mutate_plan(
        run_dir=str(run_dir), brief_dir=str(bd),
        force=True, actor="sean", reason="tighten jaw",
        target="AC.identity.sean-jaw", field="description",
        value="Sean's jaw is very square.", new_version="1.2.0",
    )
    assert rc == 0

    saved = json.loads((bd / "acceptance_criteria.json").read_text(encoding="utf-8"))
    # (a) the field change was applied to the rule content.
    rule = next(c for c in saved["criteria"] if c["id"] == "AC.identity.sean-jaw")
    assert rule["description"] == "Sean's jaw is very square."
    # (b) schema version field NOT overwritten with the content semver.
    assert saved["version"] == "1.1"
    # content revision recorded separately.
    assert saved["content_version"] == "1.2.0"
    # (c) the criteria still loads — the regression for the schema break.
    load_criteria(bd / "acceptance_criteria.json")

    # Audit log + plan.md delta block.
    audit = (run_dir / "plan_audit.jsonl").read_text(encoding="utf-8")
    assert "tighten jaw" in audit
    plan_md = (bd / "plan.md").read_text(encoding="utf-8")
    assert "Plan changes since approval (1)" in plan_md
    assert "tighten jaw" in plan_md


def test_mutate_unknown_target_errors(tmp_path):
    """An unknown --target is a hard error (rc 1), not a silent no-op."""
    bd = tmp_path / "briefs" / "2026-05-27-test"
    _seed_brief(bd)
    rc = mutate_plan(
        run_dir=str(tmp_path / "runs" / "r1"), brief_dir=str(bd),
        force=True, actor="sean", reason="edit a missing rule",
        target="AC.identity.nonexistent", field="description",
        value="x", new_version="1.2.0",
    )
    assert rc == 1


def test_mutate_appends_audit_lines_across_invocations(tmp_path):
    """Second mutate adds a second JSONL line and bumps the delta counter."""
    bd = tmp_path / "briefs" / "2026-05-27-test"
    _seed_brief(bd)
    run_dir = tmp_path / "runs" / "test_run"

    mutate_plan(
        run_dir=str(run_dir), brief_dir=str(bd), force=True,
        actor="sean", reason="first", target="AC.identity.sean-jaw",
        field="description", value="A.", new_version="1.2.0",
    )
    mutate_plan(
        run_dir=str(run_dir), brief_dir=str(bd), force=True,
        actor="sean", reason="second", target="AC.timing.beat3-hold",
        field="description", value="B.", new_version="1.3.0",
    )
    lines = (run_dir / "plan_audit.jsonl").read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 2
    saved = json.loads((bd / "acceptance_criteria.json").read_text(encoding="utf-8"))
    # Both content revisions land; schema version stays loadable throughout.
    assert saved["version"] == "1.1"
    assert saved["content_version"] == "1.3.0"
    plan_md = (bd / "plan.md").read_text(encoding="utf-8")
    assert "Plan changes since approval (2)" in plan_md
