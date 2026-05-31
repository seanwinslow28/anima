from pathlib import Path

from pipeline.museum.schema import (
    Exhibit, Decision, Verdict, SCHEMA_VERSION,
    write_exhibit, read_exhibit, derive_project_slug,
)


def _fixture_exhibit() -> Exhibit:
    return Exhibit(
        exhibit_id="03-expr-neutral",
        project_slug="character-bible",
        run_slug="2026-05-30-cy-claude-mascot-pencil-bake",
        title="Expression plate — neutral",
        kind="plate_verdict",
        phase=2,
        persona="cy",
        date="2026-05-30",
        decision=Decision(
            outcome="fail", attempts=3,
            rationale="NB2 invented a hair tuft; no-hair invariant violated.",
            rationale_source="plate_verdicts.jsonl",
        ),
        references=["assets/anchor.png"],
        output="assets/neutral.png",
        verdict=Verdict(method="dinov2", score=0.8857, reference="anchor.png",
                        model_verdict="fail", model_confidence=0.7),
        cites_criteria=["IR.claude-mascot.anatomy.no-hair"],
        evidence_completeness="rich",
        source_paths=["runs/2026-05-30-cy-claude-mascot-pencil-bake/plate_verdicts.jsonl#L6"],
    )


def test_exhibit_roundtrips_json(tmp_path: Path):
    ex = _fixture_exhibit()
    path = write_exhibit(tmp_path, ex)
    assert (path / "exhibit.json").exists()
    back = read_exhibit(path / "exhibit.json")
    assert back == ex
    assert back.schema_version == SCHEMA_VERSION


def test_markdown_is_clean_prose_no_chrome(tmp_path: Path):
    ex = _fixture_exhibit()
    md = ex.to_markdown()
    assert "Expression plate — neutral" in md
    assert "no-hair invariant violated" in md
    assert "<" not in md and "```html" not in md  # boxes/chrome live in the renderer


def test_thin_exhibit_is_honest_not_invented(tmp_path: Path):
    ex = Exhibit(
        exhibit_id="01-thin", project_slug="pencil-test", run_slug="run_x",
        title="Sparse decision", kind="note",
        decision=Decision(outcome="approved", rationale="", rationale_source=None),
        evidence_completeness="thin",
    )
    d = ex.to_json_dict()
    assert d["decision"]["rationale"] == ""        # silence stays silent
    assert d["decision"]["rationale_source"] is None
    assert d["evidence_completeness"] == "thin"
    assert "no rationale recorded" in ex.to_markdown().lower()


def test_derive_project_slug_config_driven():
    rules = {
        "character-bible": ["cy-", "mascot", "bible", "sean-anchor", "two-character", "emitter"],
        "pencil-test": ["seedance", "act1", "act2", "head-turn", "pose", "run_"],
    }
    assert derive_project_slug("2026-05-30-cy-claude-mascot-pencil-bake", rules) == "character-bible"
    assert derive_project_slug("act2-seedance-2026-04-27", rules) == "pencil-test"
    assert derive_project_slug("run_2026-04-04_173445", rules) == "pencil-test"
    assert derive_project_slug("totally-unknown-run", rules) is None  # -> _unclassified, never silently misfiled
