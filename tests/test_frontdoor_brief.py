"""Front-door code seam — StudioBrief parse / validate / render (§5.1).

The 8-section shape (7 H2 headers + the nested `### What this is NOT`) is a
convention anima enforces on itself — nothing downstream parses the headers
(Maya/Sam/Bea consume the brief as free text). The validator here is that
enforcement. Shape source: tests/fixtures/studio_brief_seed.md + the piñata
dry-run brief (they agree).
"""

from __future__ import annotations

from pathlib import Path

from pipeline.frontdoor.brief import REQUIRED_SECTIONS, parse

FIXTURES = Path(__file__).resolve().parent / "fixtures"
SEED = FIXTURES / "studio_brief_seed.md"


def seed_text() -> str:
    return SEED.read_text(encoding="utf-8")


def test_parses_seed_into_seven_sections():
    brief = parse(seed_text())
    assert list(brief.sections) == list(REQUIRED_SECTIONS)
    assert brief.validate() == []


def test_missing_non_negotiables_fails():
    text = seed_text().split("## What are the non-negotiables?")[0]
    problems = parse(text).validate()
    assert any("non-negotiables" in p for p in problems)


def test_missing_what_this_is_not_subblock_fails():
    lines = [
        line for line in seed_text().splitlines(keepends=True)
        if not line.startswith("### What this is NOT")
    ]
    problems = parse("".join(lines)).validate()
    assert any("What this is NOT" in p for p in problems)


def test_out_of_order_sections_fail():
    text = seed_text()
    tone_header = "## What is the tone?"
    fmt_header = "## What is the format?"
    swapped = (
        text.replace(tone_header, "@@FMT@@")
        .replace(fmt_header, tone_header)
        .replace("@@FMT@@", fmt_header)
    )
    problems = parse(swapped).validate()
    assert any("order" in p for p in problems)


def test_empty_section_body_fails():
    text = seed_text()
    head, _, _ = text.partition("## What is the deadline?")
    truncated = (
        head
        + "## What is the deadline?\n\n"
        + "## What are the non-negotiables?\n\n- One rule.\n"
    )
    problems = parse(truncated).validate()
    assert any("deadline" in p and "empty" in p for p in problems)


def test_render_roundtrips():
    text = seed_text()
    assert parse(text).render() == text
