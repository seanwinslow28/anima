"""Tests for pipeline.criteria — acceptance_criteria.json schema + lock enforcement."""

import json
from pathlib import Path

import pytest

from pipeline.criteria import (
    AcceptanceCriterion,
    CriteriaLockViolation,
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
