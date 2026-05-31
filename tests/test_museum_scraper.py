import json
from pathlib import Path

from pipeline.museum.scraper import scrape_plate_verdicts, scrape_bible_audit, scrape_run

SLUG_RULES = {
    "character-bible": ["cy-", "mascot", "bible"],
    "pencil-test": ["seedance", "run_"],
}


def _write_jsonl(path: Path, rows: list[dict]):
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


def test_scrape_plate_verdicts_maps_real_fields(tmp_path: Path):
    run = tmp_path / "2026-05-30-cy-claude-mascot-pencil-bake"
    run.mkdir()
    _write_jsonl(run / "plate_verdicts.jsonl", [
        {"target_path": "turnarounds/body-3quarter.png", "attempts": 1, "cache_hit": True,
         "status": "ingested", "gemini_verdict": "pass", "gemini_confidence": 1.0,
         "reasoning": "Honors all cited identity rules.", "similarity_method": "dinov2",
         "similarity_score": 0.922, "similarity_reference": "anchor.png",
         "cites_identity_rule": ["IR.claude-mascot.proportion.rounded-box-silhouette"]},
        {"target_path": "expressions/neutral.png", "attempts": 3, "cache_hit": False,
         "status": "fail", "gemini_verdict": "fail", "gemini_confidence": 0.7,
         "reasoning": "", "similarity_method": "dinov2", "similarity_score": 0.81,
         "similarity_reference": "anchor.png", "cites_identity_rule": []},
    ])
    exs = scrape_plate_verdicts(run, "character-bible", run.name)
    assert len(exs) == 2
    a, b = exs
    assert a.kind == "plate_verdict"
    assert a.decision.outcome == "ingested"
    assert a.verdict.method == "dinov2" and a.verdict.score == 0.922
    assert a.cites_criteria == ["IR.claude-mascot.proportion.rounded-box-silhouette"]
    assert a.decision.rationale_source == "plate_verdicts.jsonl"
    assert a.evidence_completeness == "rich"
    # Silent reasoning -> honest thin/partial, rationale stays empty
    assert b.decision.rationale == ""
    assert b.evidence_completeness == "partial"


def test_scrape_bible_audit_mutation_and_add(tmp_path: Path):
    run = tmp_path / "2026-05-30-cy-mascot-expression-expansion"
    run.mkdir()
    _write_jsonl(run / "bible_audit.jsonl", [
        {"ts": "2026-05-30T14:43:18+00:00", "actor": "sean", "reason": "no-hair invariant",
         "target": "IR.claude-mascot.anatomy.no-hair", "field": "description", "value": "no hair, ever",
         "criteria_version_from": "1.2", "criteria_version_to": "1.3.0"},
        {"ts": "2026-05-30T21:09:00+00:00", "actor": "sean", "reason": "Act 2 expressions",
         "kind": "add", "added_rule_ids": ["IR.claude-mascot.face.alarm-expression"],
         "added_plate_paths": ["expressions/alarm.png"],
         "content_version_from": None, "content_version_to": "1.1.0"},
    ])
    exs = scrape_bible_audit(run, "character-bible", run.name)
    assert [e.kind for e in exs] == ["bible_mutation", "bible_add"]
    assert exs[0].persona == "human" and exs[0].decision.outcome == "mutated"
    assert exs[0].cites_criteria == ["IR.claude-mascot.anatomy.no-hair"]
    assert exs[1].decision.outcome == "added"
    assert "IR.claude-mascot.face.alarm-expression" in exs[1].cites_criteria


def test_scrape_run_derives_slug_and_collects(tmp_path: Path):
    run = tmp_path / "2026-05-30-cy-claude-mascot-pencil-bake"
    run.mkdir()
    _write_jsonl(run / "plate_verdicts.jsonl", [
        {"target_path": "turnarounds/body-front.png", "attempts": 1, "cache_hit": True,
         "status": "pass", "gemini_verdict": "pass", "reasoning": "ok",
         "similarity_method": "dinov2", "similarity_score": 0.9, "cites_identity_rule": []}])
    slug, exs = scrape_run(run, SLUG_RULES)
    assert slug == "character-bible"
    assert len(exs) == 1 and exs[0].project_slug == "character-bible"
