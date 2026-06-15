"""Tests for pipeline/cli/storyboard.py — Bea's `storyboard init/show/approve/mutate`.

Mirrors the script CLI: `show` renders a tear sheet (boxes in the renderer, clean
prose on disk); `approve` is the CURATION GATE — it re-validates the curated
shots.yaml against beats.json (load_shots + storyboard_validate) before flipping
locked:true; `mutate` is the audited force-flag edit appending to
storyboard_audit.jsonl.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from pipeline.cli import storyboard as sb_cli
from pipeline.cli.__main__ import main as cli_main

# The committed manifest (characters: sean-anchor + claude-mascot) — derive_cast
# resolves the real Bibles; cwd at test time is the repo root.
_MANIFEST = str(Path(__file__).resolve().parents[1] / "manifest.yaml")


def _beats() -> dict:
    return {
        "slug": "the-spark-shared",
        "logline": "Sean draws; the mascot notices; it settles back.",
        "locked": True,
        "beats": [
            {"id": 1, "title": "Establishing", "intent": "Set the look.",
             "emotional_beat": "calm focus", "cast": ["sean", "claude-mascot"]},
            {"id": 2, "title": "The notice", "intent": "The mascot perks up.",
             "emotional_beat": "spark", "cast": ["claude-mascot"]},
        ],
    }


def _shots(*, cover_all: bool = True) -> dict:
    frames = [
        {"id": 1, "beat_id": 1, "cast": ["sean", "claude-mascot"],
         "beat": "establishing two-shot", "prompt": "board it. pencil test.", "hold": 2},
    ]
    if cover_all:
        frames.append(
            {"id": 2, "beat_id": 2, "cast": ["sean", "claude-mascot"],
             "beat": "the notice", "prompt": "board it. pencil test.", "hold": 2}
        )
    return {"slug": "SS", "frames": frames}


def _write_brief(brief: Path, *, shots: dict | None = None, beats: dict | None = None) -> None:
    brief.mkdir(parents=True, exist_ok=True)
    (brief / "beats.json").write_text(json.dumps(beats or _beats(), indent=2), encoding="utf-8")
    (brief / "shots.yaml").write_text(yaml.safe_dump(shots or _shots()), encoding="utf-8")


# ----- init -----

def test_init_scaffolds_idempotent(tmp_path):
    target = tmp_path / "brief"
    assert sb_cli.init_storyboard(str(target)) == 0
    assert (target / "shots.yaml").exists()
    assert (target / "storyboard.md").exists()
    body = (target / "shots.yaml").read_text(encoding="utf-8")
    assert sb_cli.init_storyboard(str(target)) == 0  # idempotent
    assert (target / "shots.yaml").read_text(encoding="utf-8") == body


# ----- show / render -----

def test_render_shots_has_boxes_and_content():
    out = sb_cli.render_shots(yaml.safe_dump(_shots()))
    assert "SS" in out
    assert "claude-mascot" in out
    assert "beat 1" in out.lower() or "beat_id" in out.lower()  # coverage link shown
    assert any(ch in out for ch in "╔═╗║╚╝┌─┐└┘")  # boxes live in the renderer


def test_show_reads_file(tmp_path):
    brief = tmp_path / "brief"
    _write_brief(brief)
    assert sb_cli.show_storyboard(str(brief / "shots.yaml")) == 0


# ----- approve (the curation gate) -----

def test_approve_validates_then_locks_idempotent(tmp_path, capsys):
    brief = tmp_path / "brief"
    _write_brief(brief)
    assert sb_cli.approve_storyboard(str(brief), _MANIFEST) == 0
    loaded = yaml.safe_load((brief / "shots.yaml").read_text(encoding="utf-8"))
    assert loaded["locked"] is True
    # Idempotent no-op.
    assert sb_cli.approve_storyboard(str(brief), _MANIFEST) == 0
    assert "already locked" in capsys.readouterr().out


def test_approve_refuses_on_coverage_gap(tmp_path):
    brief = tmp_path / "brief"
    _write_brief(brief, shots=_shots(cover_all=False))  # beat 2 has no shot
    rc = sb_cli.approve_storyboard(str(brief), _MANIFEST)
    assert rc == 1
    # Did NOT lock a failing board.
    loaded = yaml.safe_load((brief / "shots.yaml").read_text(encoding="utf-8"))
    assert not loaded.get("locked")


def test_approve_missing_shots_errors(tmp_path):
    brief = tmp_path / "brief"
    brief.mkdir()
    (brief / "beats.json").write_text(json.dumps(_beats()), encoding="utf-8")
    assert sb_cli.approve_storyboard(str(brief), _MANIFEST) == 1


# ----- mutate -----

def test_mutate_requires_force(tmp_path):
    brief = tmp_path / "brief"
    _write_brief(brief)
    rc = sb_cli.mutate_storyboard(
        run_dir=str(tmp_path / "run"), brief_dir=str(brief),
        force=False, actor="", reason="", target="1", field="beat", value="X",
    )
    assert rc == 1


def test_mutate_edits_frame_and_audits(tmp_path):
    brief = tmp_path / "brief"
    _write_brief(brief)
    run_dir = tmp_path / "run"
    rc = sb_cli.mutate_storyboard(
        run_dir=str(run_dir), brief_dir=str(brief),
        force=True, actor="sean", reason="tighten beat",
        target="1", field="beat", value="tighter establishing",
    )
    assert rc == 0
    loaded = yaml.safe_load((brief / "shots.yaml").read_text(encoding="utf-8"))
    assert loaded["frames"][0]["beat"] == "tighter establishing"
    audit = (run_dir / "storyboard_audit.jsonl").read_text(encoding="utf-8")
    assert "tighten beat" in audit


def test_mutate_unknown_frame_id_errors(tmp_path):
    brief = tmp_path / "brief"
    _write_brief(brief)
    rc = sb_cli.mutate_storyboard(
        run_dir=str(tmp_path / "run"), brief_dir=str(brief),
        force=True, actor="sean", reason="x", target="99", field="beat", value="X",
    )
    assert rc == 1


# ----- dispatch through the CLI entrypoint -----

def test_cli_dispatch_init_show_approve(tmp_path):
    brief = tmp_path / "brief"
    assert cli_main(["storyboard", "init", "--target", str(brief)]) == 0
    _write_brief(brief)  # author real artifacts over the template
    assert cli_main(["storyboard", "show", "--shots", str(brief / "shots.yaml")]) == 0
    assert cli_main(["storyboard", "approve", "--brief-dir", str(brief), "--manifest", _MANIFEST]) == 0
    loaded = yaml.safe_load((brief / "shots.yaml").read_text(encoding="utf-8"))
    assert loaded["locked"] is True
