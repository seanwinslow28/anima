from pathlib import Path

from pipeline.museum.schema import Exhibit, Decision, Verdict, write_exhibit
from pipeline.museum.render import render_static, md_to_html


def test_md_to_html_basics():
    html = md_to_html("# Title\n\nA **bold** word and `code`.\n\n- one\n- two\n")
    assert "<h1>Title</h1>" in html
    assert "<strong>bold</strong>" in html and "<code>code</code>" in html
    assert "<li>one</li>" in html and "<ul>" in html


def test_render_static_project_pages_and_mo_prose(tmp_path: Path):
    museum = tmp_path / "museum"
    d = write_exhibit(museum, Exhibit(
        exhibit_id="01-body-front", project_slug="character-bible",
        run_slug="2026-05-30-cy-claude-mascot-pencil-bake",
        title="Plate — turnarounds/body-front.png", kind="plate_verdict",
        persona="cy", date="2026-05-30",
        decision=Decision(outcome="pass", rationale="Holds identity.", rationale_source="plate_verdicts.jsonl"),
        verdict=Verdict(method="dinov2", score=0.92),
        cites_criteria=["IR.claude-mascot.anatomy.no-hair"], evidence_completeness="rich"))
    # Mo's narration lives in exhibit.md — the renderer must surface it.
    (d / "exhibit.md").write_text("Cy approved this plate; identity holds at 0.92.\n", encoding="utf-8")
    (museum / "character-bible" / "project.json").write_text(
        '{"project_slug":"character-bible","title":"Character Bible — building Cy in the open"}',
        encoding="utf-8")

    out = tmp_path / "_site"
    index = render_static(museum, out)
    assert index.name == "index.html"
    index_html = index.read_text(encoding="utf-8")
    # Index links to a PROJECT page (not directly to exhibits).
    assert "Character Bible — building Cy in the open" in index_html
    assert "character-bible/index.html" in index_html
    # Project page exists.
    project_page = (out / "character-bible" / "index.html").read_text(encoding="utf-8")
    assert "2026-05-30-cy-claude-mascot-pencil-bake" in project_page
    # Exhibit page surfaces Mo's prose + the structured decision trail.
    ex_page = next(p for p in out.rglob("*.html") if "01-body-front" in str(p)).read_text(encoding="utf-8")
    assert "identity holds at 0.92" in ex_page          # Mo's narrative
    assert "no-hair" in ex_page                          # cites from the json
    assert "0.92" in ex_page                             # verdict score
    assert "http://" not in ex_page and "https://" not in ex_page


def test_render_motion_comparison_layout(tmp_path: Path):
    museum = tmp_path / "museum"
    d = write_exhibit(museum, Exhibit(
        exhibit_id="motion-idle", project_slug="character-bible",
        run_slug="2026-05-30-mascot-motion-ingest",
        title="Motion — Idle / settle loop", kind="motion_keys",
        persona="human", date="2026-05-31",
        decision=Decision(outcome="ingested", rationale="A slow breath.",
                          rationale_source="source-refs/motion-direction.md"),
        references=["assets/Idle-settle-loop.png"],
        output="assets/idle-loop.gif",
        frames=["assets/idle-01.png", "assets/idle-02.png"],
        cites_criteria=["IR.claude-mascot.motion.idle-breath-volume"]))
    (d / "exhibit.md").write_text("Sean drew the idle keys; the pipeline colored them.\n", encoding="utf-8")
    out = tmp_path / "_site"
    render_static(museum, out)
    page = next(p for p in out.rglob("*.html") if "motion-idle" in str(p)).read_text(encoding="utf-8")
    assert "Hand-drawn" in page and "Sean" in page
    assert "Idle-settle-loop.png" in page and "idle-loop.gif" in page
    assert "idle-01.png" in page and "idle-02.png" in page
    assert "http://" not in page and "https://" not in page
