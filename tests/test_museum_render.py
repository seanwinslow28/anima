from pathlib import Path

from pipeline.museum.schema import Exhibit, Decision, Verdict, write_exhibit
from pipeline.museum.render import render_static


def test_render_static_self_contained(tmp_path: Path):
    museum = tmp_path / "museum"
    write_exhibit(museum, Exhibit(
        exhibit_id="01-body-front", project_slug="character-bible",
        run_slug="2026-05-30-cy-claude-mascot-pencil-bake",
        title="Plate — turnarounds/body-front.png", kind="plate_verdict",
        persona="cy", date="2026-05-30",
        decision=Decision(outcome="pass", rationale="Holds identity.", rationale_source="plate_verdicts.jsonl"),
        verdict=Verdict(method="dinov2", score=0.92),
        cites_criteria=["IR.claude-mascot.anatomy.no-hair"], evidence_completeness="rich"))
    out = tmp_path / "_site"
    index = render_static(museum, out)
    assert index.exists() and index.name == "index.html"
    index_html = index.read_text(encoding="utf-8")
    assert "character-bible" in index_html
    # Self-contained: no external CDN/script dependency the museum can't survive
    assert "http://" not in index_html and "https://" not in index_html
    exhibit_pages = list(out.rglob("*.html"))
    assert any("body-front" in p.read_text(encoding="utf-8") for p in exhibit_pages)
    assert any("Holds identity" in p.read_text(encoding="utf-8") for p in exhibit_pages)
