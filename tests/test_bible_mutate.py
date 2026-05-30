"""bible mutate must edit rule content AND keep the Bible loadable."""
import json
from pathlib import Path

from pipeline.cli.bible import mutate_bible
from pipeline.criteria import load_criteria

_LOCKED_BIBLE = {
    "version": "1.2",
    "locked": True,
    "criteria": [
        {
            "id": "IR.test.anatomy.no-hair",
            "description": "Original description.",
            "cites_phase": [5],
            "cites_personas": ["em"],
            "impact_tag": "identity_critical",
            "character_id": "test",
            "derived_from": ["characters/test/anchor.png"],
        }
    ],
}


def _write_bible(tmp_path: Path) -> Path:
    cd = tmp_path / "characters" / "test"
    cd.mkdir(parents=True)
    (cd / "acceptance_criteria.json").write_text(json.dumps(_LOCKED_BIBLE, indent=2))
    return cd


def test_mutate_applies_field_change_and_stays_loadable(tmp_path):
    cd = _write_bible(tmp_path)
    rc = mutate_bible(
        run_dir=str(tmp_path / "runs" / "r1"),
        character_dir=str(cd),
        force=True,
        actor="sean",
        reason="sharpen the no-hair rule",
        target="IR.test.anatomy.no-hair",
        field="description",
        value="The mascot has no hair or tuft on top; the box-top is not a head.",
        content_version="1.3.0",
    )
    assert rc == 0
    raw = json.loads((cd / "acceptance_criteria.json").read_text())
    # (a) the field change was applied to the rule content
    rule = next(c for c in raw["criteria"] if c["id"] == "IR.test.anatomy.no-hair")
    assert rule["description"].startswith("The mascot has no hair")
    # (b) the schema version field was NOT overwritten with the content semver
    assert raw["version"] == "1.2"
    # content_version recorded separately
    assert raw["content_version"] == "1.3.0"
    # (c) the Bible still loads — this is the regression for the §4 break
    bundle = load_criteria(cd / "acceptance_criteria.json")
    assert any(c.id == "IR.test.anatomy.no-hair" for c in bundle.criteria)


def test_mutate_without_new_version_still_edits_and_loads(tmp_path):
    cd = _write_bible(tmp_path)
    rc = mutate_bible(
        run_dir=str(tmp_path / "runs" / "r1"),
        character_dir=str(cd),
        force=True,
        actor="sean",
        reason="no content-version bump",
        target="IR.test.anatomy.no-hair",
        field="impact_tag",
        value="hero",
        content_version=None,
    )
    assert rc == 0
    raw = json.loads((cd / "acceptance_criteria.json").read_text())
    assert raw["version"] == "1.2"
    rule = next(c for c in raw["criteria"] if c["id"] == "IR.test.anatomy.no-hair")
    assert rule["impact_tag"] == "hero"
    load_criteria(cd / "acceptance_criteria.json")  # must not raise


def test_mutate_unknown_target_errors(tmp_path):
    cd = _write_bible(tmp_path)
    rc = mutate_bible(
        run_dir=str(tmp_path / "runs" / "r1"),
        character_dir=str(cd),
        force=True,
        actor="sean",
        reason="typo target",
        target="IR.test.face.does-not-exist",
        field="description",
        value="x",
        content_version=None,
    )
    assert rc == 1  # surfaced, not silently no-op
