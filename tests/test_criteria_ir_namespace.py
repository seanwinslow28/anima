"""Tests for the IR.* namespace extension to pipeline.criteria.

Commit 2 lands the Bible-layer identity rules as first-class criteria entries.
The schema extension adds:
- A second mnemonic ID pattern: IR.{character_id}.{category}.{handle} (three
  dotted segments instead of AC.*'s two).
- A closed IR-specific category vocabulary distinct from AC.*'s — anatomy /
  hair / face / proportion / palette / costume / prop / pose / motion / style.
- An optional character_id field on AcceptanceCriterion. None for AC.*
  records; required to match the parsed character_id for IR.* records.
- An extended derived_from parser that accepts plate-region pointer syntax
  like 'characters/sean-anchor/turnarounds/body-front.png#region:hair'.
- A CriteriaBundle.query_by_character(character_id) accessor.

The schema version bumps to 1.2 when IR.* entries are present. v1.1 with
AC.*-only and v1.0 flat schema continue to load unchanged (backward compat).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.criteria import (
    AcceptanceCriterion,
    VALID_IR_CATEGORIES,
    load_criteria,
    validate_criteria,
)

FIXTURE = Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------------------
# IR.* mnemonic ID pattern
# ---------------------------------------------------------------------------


def test_ir_id_pattern_parses_three_segments():
    """IR.{character_id}.{category}.{handle} validates as a three-part ID."""
    validate_criteria({
        "version": "1.2",
        "criteria": [{
            "id": "IR.sean.hair.center-cowlick",
            "description": "Sean's hair has a center cowlick visible on the crown.",
            "cites_phase": [5],
            "cites_personas": ["em"],
            "impact_tag": "identity_critical",
            "character_id": "sean",
            "derived_from": ["characters/sean-anchor/anchor.png#region:hair"],
        }],
    })


def test_ir_id_with_kebab_character_id_validates():
    """Character IDs are lowercase-kebab; the parser accepts them."""
    validate_criteria({
        "version": "1.2",
        "criteria": [{
            "id": "IR.claude-mascot.palette.pixel-orange-e89b6b",
            "description": "Claude mascot's primary orange is approximately #E89B6B.",
            "cites_phase": [5],
            "cites_personas": ["em"],
            "impact_tag": "identity_critical",
            "character_id": "claude-mascot",
        }],
    })


def test_ir_id_with_two_segments_rejected():
    """IR.sean.hair (only two segments) doesn't satisfy IR.{char}.{cat}.{handle}."""
    with pytest.raises(ValueError, match="malformed id"):
        validate_criteria({
            "version": "1.2",
            "criteria": [{
                "id": "IR.sean.hair",  # missing handle
                "description": "x",
                "cites_phase": [5],
                "cites_personas": [],
                "character_id": "sean",
            }],
        })


# ---------------------------------------------------------------------------
# Closed IR category vocabulary
# ---------------------------------------------------------------------------


def test_ir_category_closed_vocab_includes_eleven_categories():
    """The closed IR category vocabulary is exactly these eleven categories.

    `view` added 2026-06-07 (G6.1): view-correctness is a first-class geometry
    class in the layer-ownership map; Em authors real IR.sean.view.* rules
    against it. A deliberate expansion of the closed vocab, not an inline tweak.
    """
    assert VALID_IR_CATEGORIES == frozenset({
        "anatomy", "hair", "face", "proportion", "palette",
        "costume", "prop", "pose", "motion", "style", "view",
    })


def test_ir_category_closed_vocab_rejects_unknown():
    """An IR.* category outside the closed vocab is rejected."""
    with pytest.raises(ValueError, match="unknown IR category"):
        validate_criteria({
            "version": "1.2",
            "criteria": [{
                "id": "IR.sean.unknown.foo",
                "description": "x",
                "cites_phase": [5],
                "cites_personas": [],
                "character_id": "sean",
            }],
        })


def test_ir_uses_different_category_vocab_than_ac():
    """AC.identity.* validates because 'identity' is in AC's vocab; IR.identity.*
    does NOT validate because 'identity' is not in IR's vocab (Cy's identity
    rules live under anatomy/hair/face/proportion etc., not 'identity')."""
    # AC.identity.* is fine.
    validate_criteria({
        "version": "1.2",
        "criteria": [{
            "id": "AC.identity.front-pose",
            "description": "x",
            "cites_phase": [5],
            "cites_personas": [],
            "impact_tag": "identity_critical",
        }],
    })
    # IR.X.identity.handle fails — 'identity' isn't in IR's category vocab.
    with pytest.raises(ValueError, match="unknown IR category"):
        validate_criteria({
            "version": "1.2",
            "criteria": [{
                "id": "IR.sean.identity.front-pose",
                "description": "x",
                "cites_phase": [5],
                "cites_personas": [],
                "character_id": "sean",
            }],
        })


# ---------------------------------------------------------------------------
# character_id field
# ---------------------------------------------------------------------------


def test_ir_character_id_must_match_parsed():
    """The character_id field must match the parsed character_id from the ID."""
    with pytest.raises(ValueError, match="character_id"):
        validate_criteria({
            "version": "1.2",
            "criteria": [{
                "id": "IR.sean.hair.center-cowlick",
                "description": "x",
                "cites_phase": [5],
                "cites_personas": [],
                "character_id": "claude-mascot",  # mismatch
            }],
        })


def test_ir_character_id_field_required_on_ir_records():
    """IR.* entries must carry the character_id field explicitly."""
    with pytest.raises(ValueError, match="character_id"):
        validate_criteria({
            "version": "1.2",
            "criteria": [{
                "id": "IR.sean.hair.center-cowlick",
                "description": "x",
                "cites_phase": [5],
                "cites_personas": [],
                # character_id missing
            }],
        })


def test_ac_records_dont_require_character_id():
    """AC.* records have character_id=None by default; the field is optional."""
    validate_criteria({
        "version": "1.2",
        "criteria": [{
            "id": "AC.tone.melancholy",
            "description": "x",
            "cites_phase": [5],
            "cites_personas": [],
            "impact_tag": "aesthetic",
        }],
    })


# ---------------------------------------------------------------------------
# AC and IR coexist in the same bundle
# ---------------------------------------------------------------------------


def test_ac_and_ir_coexist_in_same_bundle(tmp_path):
    """A v1.2 file with both AC.* and IR.* entries validates and loads."""
    f = tmp_path / "mixed.json"
    f.write_text(json.dumps({
        "version": "1.2",
        "locked": False,
        "criteria": [
            {
                "id": "AC.tone.melancholy",
                "description": "Tone reads as melancholic.",
                "cites_phase": [4, 5, 6, 8],
                "cites_personas": ["em"],
                "impact_tag": "aesthetic",
            },
            {
                "id": "IR.sean.hair.center-cowlick",
                "description": "Sean's hair has a center cowlick.",
                "cites_phase": [5],
                "cites_personas": ["em"],
                "impact_tag": "identity_critical",
                "character_id": "sean",
                "derived_from": ["characters/sean-anchor/anchor.png#region:hair"],
            },
            {
                "id": "IR.claude-mascot.palette.pixel-orange",
                "description": "Claude mascot's primary orange.",
                "cites_phase": [5],
                "cites_personas": ["em"],
                "impact_tag": "identity_critical",
                "character_id": "claude-mascot",
            },
        ],
    }))
    bundle = load_criteria(f)
    assert bundle.version == "1.2"
    assert len(bundle.criteria) == 3
    assert all(isinstance(c, AcceptanceCriterion) for c in bundle.criteria)
    # AC record: character_id is None.
    ac = next(c for c in bundle.criteria if c.id.startswith("AC."))
    assert ac.character_id is None
    # IR records: character_id matches their parsed prefix.
    sean = next(c for c in bundle.criteria if c.id == "IR.sean.hair.center-cowlick")
    assert sean.character_id == "sean"
    claude = next(c for c in bundle.criteria if c.id.startswith("IR.claude-mascot"))
    assert claude.character_id == "claude-mascot"


# ---------------------------------------------------------------------------
# query_by_character accessor
# ---------------------------------------------------------------------------


def test_query_by_character_returns_only_matching_ir(tmp_path):
    """CriteriaBundle.query_by_character(id) returns IR.{id}.* entries only."""
    f = tmp_path / "multi-character.json"
    f.write_text(json.dumps({
        "version": "1.2",
        "locked": False,
        "criteria": [
            {
                "id": "AC.tone.melancholy",
                "description": "Tone.",
                "cites_phase": [5],
                "cites_personas": [],
                "impact_tag": "aesthetic",
            },
            {
                "id": "IR.sean.hair.center-cowlick",
                "description": "Sean's hair.",
                "cites_phase": [5],
                "cites_personas": [],
                "impact_tag": "identity_critical",
                "character_id": "sean",
            },
            {
                "id": "IR.sean.prop.stylus-right-hand",
                "description": "Stylus always in right hand.",
                "cites_phase": [5],
                "cites_personas": [],
                "impact_tag": "identity_critical",
                "character_id": "sean",
            },
            {
                "id": "IR.claude-mascot.palette.pixel-orange",
                "description": "Mascot orange.",
                "cites_phase": [5],
                "cites_personas": [],
                "impact_tag": "identity_critical",
                "character_id": "claude-mascot",
            },
        ],
    }))
    bundle = load_criteria(f)
    sean_rules = bundle.query_by_character("sean")
    assert len(sean_rules) == 2
    assert all(r.id.startswith("IR.sean.") for r in sean_rules)
    mascot_rules = bundle.query_by_character("claude-mascot")
    assert len(mascot_rules) == 1
    assert mascot_rules[0].id == "IR.claude-mascot.palette.pixel-orange"
    # No IR.* entries for an unknown character.
    nobody = bundle.query_by_character("nobody")
    assert nobody == []


# ---------------------------------------------------------------------------
# derived_from with #region:X plate-pointer syntax
# ---------------------------------------------------------------------------


def test_derived_from_accepts_plate_region_pointer():
    """derived_from accepts 'path/to/plate.png#region:hair' pointer syntax."""
    validate_criteria({
        "version": "1.2",
        "criteria": [{
            "id": "IR.sean.hair.center-cowlick",
            "description": "x",
            "cites_phase": [5],
            "cites_personas": [],
            "impact_tag": "identity_critical",
            "character_id": "sean",
            "derived_from": [
                "characters/sean-anchor/turnarounds/body-front.png#region:hair",
                "characters/sean-anchor/anchor.png#region:head",
            ],
        }],
    })


def test_derived_from_without_region_pointer_still_works():
    """Backward-compat: derived_from entries without #region: still validate."""
    validate_criteria({
        "version": "1.2",
        "criteria": [{
            "id": "IR.sean.hair.center-cowlick",
            "description": "x",
            "cites_phase": [5],
            "cites_personas": [],
            "impact_tag": "identity_critical",
            "character_id": "sean",
            "derived_from": ["studio_brief.character"],
        }],
    })


# ---------------------------------------------------------------------------
# Backward compatibility — v1.0 and v1.1
# ---------------------------------------------------------------------------


def test_v1_1_ac_only_still_loads():
    """v1.1 graph schema with AC.*-only entries loads unchanged."""
    bundle = load_criteria(FIXTURE / "criteria_graph_v1_1.json")
    assert bundle.version == "1.1"
    assert len(bundle.criteria) == 3
    # No character_id on v1.1 records.
    assert all(c.character_id is None for c in bundle.criteria)


def test_v1_0_flat_schema_still_loads():
    """v1.0 flat schema (pencil-test era) loads unchanged."""
    bundle = load_criteria(FIXTURE / "criteria_unlocked.json")
    assert bundle.version == "1.0"
    assert all(c.character_id is None for c in bundle.criteria)


def test_query_by_character_returns_empty_on_ac_only_bundle():
    """query_by_character on a bundle with no IR.* entries returns []."""
    bundle = load_criteria(FIXTURE / "criteria_graph_v1_1.json")
    assert bundle.query_by_character("sean") == []
