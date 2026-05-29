"""Tests for pipeline.criteria.load_all_criteria — multi-file criteria merge.

Per Task 1.8. The runner calls load_all_criteria(manifest) at run start to
read Maya's brief file + every loaded Bible's IR.* file into one bundle.
Per-character IR.{character_id}.* namespacing prevents accidental collisions;
when collisions do happen (a brief and a Bible both authoring an AC.* ID),
the loader raises with both file paths in the message.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.criteria import load_all_criteria


def _write_criteria(
    path: Path,
    *,
    version: str = "1.2",
    locked: bool = False,
    criteria: list[dict],
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"version": version, "locked": locked, "criteria": criteria}, indent=2),
        encoding="utf-8",
    )
    return path


def _ir(character_id: str, category: str, handle: str) -> dict:
    return {
        "id": f"IR.{character_id}.{category}.{handle}",
        "description": f"{character_id} {category} {handle} rule.",
        "cites_phase": [5],
        "cites_personas": ["em"],
        "impact_tag": "identity_critical",
        "character_id": character_id,
    }


def _ac(category: str, handle: str) -> dict:
    return {
        "id": f"AC.{category}.{handle}",
        "description": f"AC {category} {handle} criterion.",
        "cites_phase": [5],
        "cites_personas": ["em"],
        "impact_tag": "structural",
        "parent_id": None,
        "derived_from": [],
    }


def test_criteria_sources_merge_concatenates_lists(tmp_path):
    """Three files merged returns a bundle whose criteria == sum of inputs."""
    brief = _write_criteria(
        tmp_path / "briefs" / "x" / "acceptance_criteria.json",
        version="1.2",
        criteria=[_ac("identity", "stylus"), _ac("technical", "aspect-ratio")],
    )
    sean = _write_criteria(
        tmp_path / "characters" / "sean-anchor" / "acceptance_criteria.json",
        version="1.2",
        criteria=[_ir("sean", "hair", "center-cowlick"), _ir("sean", "prop", "stylus")],
    )
    mascot = _write_criteria(
        tmp_path / "characters" / "claude-mascot" / "acceptance_criteria.json",
        version="1.2",
        criteria=[_ir("claude-mascot", "palette", "limited-orange")],
    )
    manifest = {
        "criteria_sources": {
            "brief_file": str(brief),
            "bibles": [str(sean), str(mascot)],
        }
    }
    bundle = load_all_criteria(manifest)
    assert len(bundle.criteria) == 5
    assert bundle.version == "1.2"


def test_criteria_sources_duplicate_id_raises(tmp_path):
    """Two files asserting the same ID raises ValueError naming both files."""
    a = _write_criteria(
        tmp_path / "a" / "acceptance_criteria.json",
        criteria=[_ac("identity", "stylus")],
    )
    b = _write_criteria(
        tmp_path / "b" / "acceptance_criteria.json",
        criteria=[_ac("identity", "stylus")],
    )
    manifest = {"criteria_sources": {"brief_file": str(a), "bibles": [str(b)]}}
    with pytest.raises(ValueError, match="Duplicate criterion id"):
        load_all_criteria(manifest)


def test_criteria_sources_missing_file_logged_not_fatal(tmp_path):
    """A referenced Bible that doesn't exist yet is skipped, not raised."""
    brief = _write_criteria(
        tmp_path / "briefs" / "x" / "acceptance_criteria.json",
        criteria=[_ac("identity", "stylus")],
    )
    missing_bible = tmp_path / "characters" / "not-authored" / "acceptance_criteria.json"
    manifest = {
        "criteria_sources": {
            "brief_file": str(brief),
            "bibles": [str(missing_bible)],
        }
    }
    bundle = load_all_criteria(manifest)
    # Only the brief loaded; the missing Bible was skipped without raising.
    assert len(bundle.criteria) == 1
    assert bundle.criteria[0].id == "AC.identity.stylus"


def test_criteria_sources_empty_manifest_returns_empty_bundle(tmp_path):
    """Missing criteria_sources block → empty bundle, version 1.2 default."""
    bundle = load_all_criteria({})
    assert len(bundle.criteria) == 0
    assert bundle.locked is False


def test_query_by_character_filters_merged_bundle(tmp_path):
    """Merged Bundle.query_by_character returns only that character's IR.* rules."""
    sean = _write_criteria(
        tmp_path / "characters" / "sean-anchor" / "acceptance_criteria.json",
        criteria=[
            _ir("sean", "hair", "center-cowlick"),
            _ir("sean", "prop", "stylus"),
        ],
    )
    mascot = _write_criteria(
        tmp_path / "characters" / "claude-mascot" / "acceptance_criteria.json",
        criteria=[_ir("claude-mascot", "palette", "limited-orange")],
    )
    manifest = {"criteria_sources": {"bibles": [str(sean), str(mascot)]}}
    bundle = load_all_criteria(manifest)
    sean_rules = bundle.query_by_character("sean")
    mascot_rules = bundle.query_by_character("claude-mascot")
    assert len(sean_rules) == 2
    assert len(mascot_rules) == 1
    assert all(c.id.startswith("IR.sean.") for c in sean_rules)
    assert all(c.id.startswith("IR.claude-mascot.") for c in mascot_rules)


def test_brief_template_carries_project_type_field(tmp_path):
    """templates/brief/01_production_brief.md frontmatter includes project_type."""
    template_path = (
        Path(__file__).resolve().parents[1]
        / "templates" / "brief" / "01_production_brief.md"
    )
    body = template_path.read_text(encoding="utf-8")
    assert "project_type:" in body
    assert "animation_piece" in body
    assert "bible_authoring" in body
