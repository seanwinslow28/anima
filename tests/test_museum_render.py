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


def test_render_motion_comparison_layout(tmp_path: Path):
    museum = tmp_path / "museum"
    write_exhibit(museum, Exhibit(
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
    out = tmp_path / "_site"
    render_static(museum, out)
    page = next(p for p in out.rglob("*.html") if "motion-idle" in str(p))
    html_text = page.read_text(encoding="utf-8")
    # Human/agent division is labeled and both sides + the frame strip render.
    assert "Hand-drawn" in html_text and "Sean" in html_text
    assert "Idle-settle-loop.png" in html_text          # manual-left sketch sheet
    assert "idle-loop.gif" in html_text                  # the colored loop (the playing result)
    assert "idle-01.png" in html_text and "idle-02.png" in html_text  # the frame strip
    assert "http://" not in html_text and "https://" not in html_text
