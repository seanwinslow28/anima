"""Tests for pipeline.criteria — acceptance_criteria.json schema + lock enforcement."""

import json
from pathlib import Path

import pytest

from pipeline.criteria import (
    AcceptanceCriterion,
    CriteriaLockViolation,
    bump_version,
    enforce_lock,
    load_criteria,
    validate_criteria,
)

FIXTURE = Path(__file__).parent / "fixtures"


def test_load_returns_typed_criteria():
    bundle = load_criteria(FIXTURE / "criteria_unlocked.json")
    assert bundle.locked is False
    assert len(bundle.criteria) == 3
    assert all(isinstance(c, AcceptanceCriterion) for c in bundle.criteria)
    assert bundle.criteria[0].id == "AC01"
    assert bundle.criteria[0].severity == "blocking"


def test_validate_rejects_duplicate_ids(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({
        "version": "1.0",
        "locked": False,
        "criteria": [
            {"id": "AC01", "phase": "phase_5", "description": "x", "severity": "blocking"},
            {"id": "AC01", "phase": "phase_6", "description": "y", "severity": "blocking"},
        ],
    }))
    with pytest.raises(ValueError, match="Duplicate criterion id: AC01"):
        load_criteria(bad)


def test_validate_rejects_unknown_severity(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({
        "version": "1.0",
        "locked": False,
        "criteria": [{"id": "AC01", "phase": "phase_5", "description": "x", "severity": "nuclear"}],
    }))
    with pytest.raises(ValueError, match="severity"):
        load_criteria(bad)


def test_enforce_lock_allows_mutation_when_unlocked(tmp_path):
    src = FIXTURE / "criteria_unlocked.json"
    dst = tmp_path / "criteria.json"
    dst.write_text(src.read_text())
    enforce_lock(dst, force=False)  # should not raise


def test_enforce_lock_raises_when_locked_and_unforced(tmp_path):
    src = FIXTURE / "criteria_locked.json"
    dst = tmp_path / "criteria.json"
    dst.write_text(src.read_text())
    with pytest.raises(CriteriaLockViolation, match="criteria_locked"):
        enforce_lock(dst, force=False)


def test_enforce_lock_writes_audit_entry_when_forced(tmp_path):
    src = FIXTURE / "criteria_locked.json"
    dst = tmp_path / "criteria.json"
    dst.write_text(src.read_text())
    audit_log = tmp_path / "criteria_audit.jsonl"
    enforce_lock(
        dst,
        force=True,
        audit_log=audit_log,
        actor="test-user",
        reason="test override",
    )
    assert audit_log.exists()
    line = audit_log.read_text().strip()
    record = json.loads(line)
    assert record["actor"] == "test-user"
    assert record["reason"] == "test override"
    assert record["criteria_path"].endswith("criteria.json")
    assert "timestamp" in record


def test_lock_violation_message_names_the_file_and_flag(tmp_path):
    src = FIXTURE / "criteria_locked.json"
    dst = tmp_path / "criteria.json"
    dst.write_text(src.read_text())
    try:
        enforce_lock(dst, force=False)
    except CriteriaLockViolation as e:
        assert "criteria.json" in str(e)
        assert "--force-criteria-mutation" in str(e)
    else:
        pytest.fail("Expected CriteriaLockViolation")


# ---------------------------------------------------------------------------
# v1.1 graph schema — commit 3 additions
# ---------------------------------------------------------------------------


def test_load_criteria_v1_1_graph_schema():
    """v1.1 graph schema loads with mnemonic IDs and graph fields."""
    bundle = load_criteria(FIXTURE / "criteria_graph_v1_1.json")
    assert bundle.version == "1.1"
    assert len(bundle.criteria) == 3
    tone = next(c for c in bundle.criteria if c.id == "AC.tone.melancholy-not-grief")
    assert tone.description.startswith("Beat 3's hold reads as melancholic")
    assert tone.cites_phase == (4, 5, 6, 8)
    assert "em" in tone.cites_personas
    assert tone.impact_tag == "aesthetic"
    assert tone.derived_from == ("studio_brief.tone", "philosophy.engine-truth")
    assert tone.parent_id is None
    # v1.0 fields default to None on v1.1 records.
    assert tone.phase is None
    assert tone.severity is None


def test_load_criteria_v1_0_still_works():
    """v1.0 flat schema continues to load (backward compatibility)."""
    bundle = load_criteria(FIXTURE / "criteria_unlocked.json")
    assert bundle.version == "1.0"
    assert bundle.criteria[0].id == "AC01"
    # v1.1 fields are empty / None on v1.0 records.
    assert bundle.criteria[0].cites_phase == ()
    assert bundle.criteria[0].impact_tag is None


def test_v1_1_rejects_unknown_category():
    """A criterion with an unknown category prefix is rejected."""
    with pytest.raises(ValueError, match="unknown category"):
        validate_criteria({
            "version": "1.1",
            "criteria": [{
                "id": "AC.glitter.sparkles",
                "description": "x",
                "cites_phase": [5],
                "cites_personas": ["em"],
                "impact_tag": "aesthetic",
            }],
        })


def test_v1_1_rejects_malformed_id():
    """A criterion with a malformed mnemonic ID is rejected."""
    with pytest.raises(ValueError, match="malformed id"):
        validate_criteria({
            "version": "1.1",
            "criteria": [{
                "id": "not-a-mnemonic",
                "description": "x",
                "cites_phase": [5],
                "cites_personas": [],
                "impact_tag": "aesthetic",
            }],
        })


def test_v1_1_rejects_unknown_impact_tag():
    """A criterion with an unknown impact_tag is rejected."""
    with pytest.raises(ValueError, match="unknown impact_tag"):
        validate_criteria({
            "version": "1.1",
            "criteria": [{
                "id": "AC.tone.sample-criterion",
                "description": "x",
                "cites_phase": [5],
                "cites_personas": [],
                "impact_tag": "sparkles",
            }],
        })


def test_query_by_phase():
    """CriteriaBundle.query_by_phase(n) returns criteria citing phase n."""
    bundle = load_criteria(FIXTURE / "criteria_graph_v1_1.json")
    p5 = bundle.query_by_phase(5)
    assert len(p5) == 3
    p8 = bundle.query_by_phase(8)
    assert len(p8) == 1
    assert p8[0].id == "AC.tone.melancholy-not-grief"


def test_query_by_persona():
    """CriteriaBundle.query_by_persona(name) returns criteria citing name."""
    bundle = load_criteria(FIXTURE / "criteria_graph_v1_1.json")
    em = bundle.query_by_persona("em")
    assert len(em) == 2
    cy = bundle.query_by_persona("cy")
    assert len(cy) == 2
    chairman = bundle.query_by_persona("chairman")
    assert len(chairman) == 1


def test_bump_version_writes_new_file_and_repoints_symlink(tmp_path):
    """bump_version() writes a semver-bumped file and re-points the symlink."""
    versioned = tmp_path / "acceptance_criteria-1.1.0.json"
    fixture = FIXTURE / "criteria_graph_v1_1.json"
    versioned.write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8")
    symlink = tmp_path / "acceptance_criteria.json"
    symlink.symlink_to("acceptance_criteria-1.1.0.json")

    new_path = bump_version(symlink, new_version="1.2.0")
    assert new_path.name == "acceptance_criteria-1.2.0.json"
    assert new_path.exists()
    assert symlink.is_symlink()
    assert symlink.resolve() == new_path.resolve()
    # Old versioned file preserved (history kept).
    assert versioned.exists()
    raw = json.loads(new_path.read_text(encoding="utf-8"))
    assert raw["version"] == "1.2.0"
