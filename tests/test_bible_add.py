"""bible add — the audited additive path for a LOCKED Bible.

Adding new expression plates + new IR.* rules to an approved Bible has no path
through `bible mutate` (edits an existing rule only) or `bible iterate` (narrows
the existing plan only). `add_to_bible` appends both, audited, while keeping the
schema `version` field loadable and the Bible locked.
"""
import json
from pathlib import Path

from pipeline.cli.bible import add_to_bible
from pipeline.criteria import load_criteria

_LOCKED_BIBLE = {
    "version": "1.2",
    "locked": True,
    "criteria": [
        {
            "id": "IR.test-char.anatomy.no-hair",
            "description": "The box-top is not a head; no hair or tuft.",
            "cites_phase": [5],
            "cites_personas": ["em"],
            "impact_tag": "identity_critical",
            "character_id": "test-char",
            "derived_from": ["characters/test-char/anchor.png"],
        }
    ],
}

_PLATE_PLAN = {
    "plates": [
        {
            "target_path": "expressions/neutral.png",
            "source": "generate",
            "prompt": "calm neutral expression",
            "cites_identity_rules": ["IR.test-char.anatomy.no-hair"],
        }
    ]
}


def _write_locked_bible_with_plan(tmp_path: Path) -> Path:
    cd = tmp_path / "characters" / "test-char"
    cd.mkdir(parents=True)
    (cd / "acceptance_criteria.json").write_text(json.dumps(_LOCKED_BIBLE, indent=2))
    (cd / "plate_generation_plan.json").write_text(json.dumps(_PLATE_PLAN, indent=2))
    return cd


def _good_spec(cd: Path) -> Path:
    spec = cd / "additions.json"
    spec.write_text(json.dumps({
        "plates": [{
            "target_path": "expressions/alarm.png",
            "source": "generate",
            "prompt": "alarm expression",
            "cites_identity_rules": ["IR.test-char.anatomy.no-hair"],
        }],
        "rules": [{
            "id": "IR.test-char.face.alarm-expression",
            "description": "Alarm: eyes wide, small graphite dots, no hair.",
            "cites_phase": [5, 6],
            "cites_personas": ["em"],
            "impact_tag": "aesthetic",
            "character_id": "test-char",
            "derived_from": ["characters/test-char/expressions/alarm.png"],
        }],
    }), encoding="utf-8")
    return spec


def test_add_appends_plates_and_rules_stays_loadable(tmp_path):
    cd = _write_locked_bible_with_plan(tmp_path)
    spec = _good_spec(cd)
    rc = add_to_bible(
        run_dir=str(tmp_path / "runs" / "r1"), character_dir=str(cd),
        force=True, actor="sean", reason="Act 2 expressions",
        spec_path=str(spec), content_version="1.1.0",
    )
    assert rc == 0
    crit = json.loads((cd / "acceptance_criteria.json").read_text())
    assert crit["version"] == "1.2"            # schema unchanged
    assert crit["content_version"] == "1.1.0"
    assert crit["locked"] is True              # add does NOT unlock
    assert any(c["id"] == "IR.test-char.face.alarm-expression" for c in crit["criteria"])
    load_criteria(cd / "acceptance_criteria.json")  # must not raise
    plan = json.loads((cd / "plate_generation_plan.json").read_text())
    assert any(p["target_path"] == "expressions/alarm.png" for p in plan["plates"])
    audit = (tmp_path / "runs" / "r1" / "bible_audit.jsonl").read_text()
    assert "Act 2 expressions" in audit


def test_add_duplicate_rule_id_errors(tmp_path):
    cd = _write_locked_bible_with_plan(tmp_path)
    spec = cd / "additions.json"
    spec.write_text(json.dumps({
        "plates": [],
        "rules": [{
            "id": "IR.test-char.anatomy.no-hair",  # already present
            "description": "dup",
            "cites_phase": [5], "cites_personas": ["em"],
            "impact_tag": "aesthetic", "character_id": "test-char",
            "derived_from": ["characters/test-char/anchor.png"],
        }],
    }), encoding="utf-8")
    rc = add_to_bible(
        run_dir=str(tmp_path / "runs" / "r1"), character_dir=str(cd),
        force=True, actor="sean", reason="dup rule", spec_path=str(spec),
    )
    assert rc == 1
    # The Bible was not mutated.
    crit = json.loads((cd / "acceptance_criteria.json").read_text())
    assert len(crit["criteria"]) == 1


def test_add_duplicate_plate_path_errors(tmp_path):
    cd = _write_locked_bible_with_plan(tmp_path)
    spec = cd / "additions.json"
    spec.write_text(json.dumps({
        "plates": [{
            "target_path": "expressions/neutral.png",  # already in the plan
            "source": "generate", "prompt": "dup",
            "cites_identity_rules": ["IR.test-char.anatomy.no-hair"],
        }],
        "rules": [],
    }), encoding="utf-8")
    rc = add_to_bible(
        run_dir=str(tmp_path / "runs" / "r1"), character_dir=str(cd),
        force=True, actor="sean", reason="dup plate", spec_path=str(spec),
    )
    assert rc == 1
    plan = json.loads((cd / "plate_generation_plan.json").read_text())
    assert len(plan["plates"]) == 1


def test_add_refuses_without_force(tmp_path, capsys):
    cd = _write_locked_bible_with_plan(tmp_path)
    spec = _good_spec(cd)
    rc = add_to_bible(
        run_dir=str(tmp_path / "runs" / "r1"), character_dir=str(cd),
        force=False, actor="sean", reason="no force", spec_path=str(spec),
    )
    assert rc == 1
    assert "--force" in capsys.readouterr().err


def test_add_requires_actor_and_reason(tmp_path):
    cd = _write_locked_bible_with_plan(tmp_path)
    spec = _good_spec(cd)
    rc = add_to_bible(
        run_dir=str(tmp_path / "runs" / "r1"), character_dir=str(cd),
        force=True, actor="", reason="", spec_path=str(spec),
    )
    assert rc == 1
