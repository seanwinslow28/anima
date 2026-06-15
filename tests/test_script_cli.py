"""Tests for pipeline/cli/script.py — Sam's `script init/show/approve/mutate`.

Mirrors the plan CLI: `show` renders a tear sheet (boxes in the renderer, clean
prose on disk); `approve` flips locked:true idempotently; `mutate` is the
audited force-flag edit appending to script_audit.jsonl.
"""

from __future__ import annotations

import json
from pathlib import Path

from pipeline.cli import script as script_cli
from pipeline.cli.__main__ import main as cli_main


def _write_beats(path: Path, *, locked: bool = False) -> None:
    payload = {
        "slug": "the-spark-shared",
        "logline": "Sean draws; the mascot delights; the loop returns.",
        "locked": locked,
        "beats": [
            {"id": 1, "title": "Establishing", "intent": "Set the look.",
             "emotional_beat": "calm focus", "cast": ["sean", "claude-mascot"]},
            {"id": 2, "title": "The delight", "intent": "The mascot reacts.",
             "emotional_beat": "delight", "cast": ["sean", "claude-mascot"]},
        ],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


# ----- init -----

def test_init_scaffolds_idempotent(tmp_path):
    target = tmp_path / "brief"
    assert script_cli.init_script(str(target)) == 0
    assert (target / "beats.json").exists()
    assert (target / "script.md").exists()
    body = (target / "beats.json").read_text(encoding="utf-8")
    # Idempotent — re-running doesn't overwrite.
    assert script_cli.init_script(str(target)) == 0
    assert (target / "beats.json").read_text(encoding="utf-8") == body


# ----- show / render -----

def test_render_beats_has_boxes_and_content():
    payload = {
        "slug": "the-spark-shared", "logline": "A quiet spark.", "locked": False,
        "beats": [{"id": 1, "title": "Establishing", "intent": "Set the look.",
                   "emotional_beat": "calm focus", "cast": ["sean", "claude-mascot"]}],
    }
    out = script_cli.render_beats(json.dumps(payload))
    assert "the-spark-shared" in out
    assert "Establishing" in out
    assert "sean" in out
    assert any(ch in out for ch in "╔═╗║╚╝┌─┐└┘")  # boxes live in the renderer


# ----- approve -----

def test_approve_flips_locked_idempotent(tmp_path, capsys):
    brief = tmp_path / "brief"
    brief.mkdir()
    beats = brief / "beats.json"
    _write_beats(beats, locked=False)
    assert script_cli.approve_script(str(brief)) == 0
    assert json.loads(beats.read_text(encoding="utf-8"))["locked"] is True
    # Idempotent no-op.
    assert script_cli.approve_script(str(brief)) == 0
    assert "already locked" in capsys.readouterr().out


def test_approve_missing_beats_errors(tmp_path):
    brief = tmp_path / "brief"
    brief.mkdir()
    assert script_cli.approve_script(str(brief)) == 1


# ----- mutate -----

def test_mutate_requires_force(tmp_path):
    brief = tmp_path / "brief"
    brief.mkdir()
    _write_beats(brief / "beats.json")
    rc = script_cli.mutate_script(
        run_dir=str(tmp_path / "run"), brief_dir=str(brief),
        force=False, actor="", reason="", target="1", field="title", value="X",
    )
    assert rc == 1


def test_mutate_edits_beat_and_audits(tmp_path):
    brief = tmp_path / "brief"
    brief.mkdir()
    beats = brief / "beats.json"
    _write_beats(beats)
    run_dir = tmp_path / "run"
    rc = script_cli.mutate_script(
        run_dir=str(run_dir), brief_dir=str(brief),
        force=True, actor="sean", reason="tighten title",
        target="1", field="title", value="The Spark",
    )
    assert rc == 0
    assert json.loads(beats.read_text(encoding="utf-8"))["beats"][0]["title"] == "The Spark"
    audit = (run_dir / "script_audit.jsonl").read_text(encoding="utf-8")
    assert "tighten title" in audit
    assert "The Spark" in audit


def test_mutate_unknown_beat_id_errors(tmp_path):
    brief = tmp_path / "brief"
    brief.mkdir()
    _write_beats(brief / "beats.json")
    rc = script_cli.mutate_script(
        run_dir=str(tmp_path / "run"), brief_dir=str(brief),
        force=True, actor="sean", reason="x", target="99", field="title", value="X",
    )
    assert rc == 1


# ----- dispatch through the CLI entrypoint -----

def test_cli_dispatch_init_show_approve(tmp_path):
    brief = tmp_path / "brief"
    assert cli_main(["script", "init", "--target", str(brief)]) == 0
    _write_beats(brief / "beats.json")  # author a real sheet over the template
    assert cli_main(["script", "show", "--beats", str(brief / "beats.json")]) == 0
    assert cli_main(["script", "approve", "--brief-dir", str(brief)]) == 0
    assert json.loads((brief / "beats.json").read_text(encoding="utf-8"))["locked"] is True
