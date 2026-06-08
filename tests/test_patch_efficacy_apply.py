# tests/test_patch_efficacy_apply.py
"""G6.9 Gate 3 (pure core) — the corpus parser + deterministic diff splice.

prompt_apply.py is the riskiest I/O dependency of the empirical loop: it parses
the real fixture-corpus markdown into per-id base prompts, and it splices a
corrective clause INTO a defect prompt to make the re-generation prompt. The
single most dangerous silent bug is forgetting to restore the canonical style
line for monochrome/shading defects (whose defect prompt has the corrupted axis
phrase stripped) — so the fix can never land. That restoration is asserted here.

All $0 — pure string work over the committed corpus markdown, no model, no I/O
beyond reading the corpus file.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from evals.vision_critic.prompt_apply import (
    parse_corpus, build_corrected_prompt, clean_stem_of, NoRegenForView,
    CANONICAL_STYLE_LINE,
)

_CORPUS_MD = Path(__file__).resolve().parents[1] / "prompts/eval-corpus/sean-anchor-fixture-corpus.md"


@pytest.fixture(scope="module")
def corpus() -> dict:
    return parse_corpus(_CORPUS_MD)


# --------------------------------------------------------------------------- #
# parse_corpus
# --------------------------------------------------------------------------- #
def test_parse_corpus_has_clean_pool_and_gen_defects(corpus):
    # all 16 clean fixtures + the generated single-axis defects resolve to FULL
    # prompts (they carry the style marker — they are regeneratable).
    for cid in ["C01", "C13", "C16"]:
        assert cid in corpus and "Maintain the warm 2D Disney pencil-test render" in corpus[cid]
    for cid in ["P-D1", "PA-D1", "PA-D2", "V-D1", "A-D1", "CL-D1", "SH-D1"]:
        assert cid in corpus, f"{cid} missing from parsed corpus"
        assert "Have the subject" in corpus[cid]


def test_parse_corpus_borderlines_are_notes_not_full_prompts(corpus):
    # The hand-drawn borderlines are short notes (no style line) — Gate 3 must
    # route them through the clean-pair prompt, never regenerate from this text.
    for cid in ["P-B1", "P-B2", "CL-B1", "SH-B1"]:
        assert cid in corpus
        assert "Maintain the warm 2D Disney pencil-test render" not in corpus[cid]


# --------------------------------------------------------------------------- #
# build_corrected_prompt — the splice (onto the CLEAN PAIR prompt)
# --------------------------------------------------------------------------- #
def test_splice_appends_corrective_to_clean_pair(corpus):
    # P-D1 pairs C01. The re-gen prompt = C01's clean stem + Em's corrective clause.
    out = build_corrected_prompt(
        corpus["C01"], "drawn at natural adult proportions, about seven heads tall",
        label="proportion")
    assert "natural adult proportions, about seven heads tall" in out
    assert "standing idle" in out  # clean stem of C01 preserved (scene/pose)
    assert out.rstrip().endswith("warm cream paper.")


def test_corrected_prompt_always_carries_full_canonical_style(corpus):
    """The corrected prompt ALWAYS re-emits the full canonical style line, so a
    palette/shading correction can never ship axis-deficient (no color wash / no
    cross-hatch). The load-bearing guard against silently dropping an axis."""
    out = build_corrected_prompt(corpus["C07"], "rendered in the full reference color palette",
                                 label="palette")
    assert "light hand-painted color wash" in out
    assert "cross-hatch shadow" in out


def test_splice_emits_exactly_one_style_line_no_duplication(corpus):
    # The pair prompt already ends in a style line; the splice strips it and emits
    # exactly one canonical line (never two).
    out = build_corrected_prompt(corpus["C02"], "drawn at natural adult proportions",
                                 label="proportion")
    assert out.count("Maintain the warm 2D Disney pencil-test render") == 1
    assert out.endswith(CANONICAL_STYLE_LINE)


def test_view_correctness_refuses_regeneration(corpus):
    """View defects are label-side (pixel-correct image, wrong declared view) — a
    re-generation can't clear them. The splice must refuse, forcing the caller's
    no-regen branch."""
    with pytest.raises(NoRegenForView):
        build_corrected_prompt(corpus["C02"], "left profile, full body visible",
                               label="view-correctness")


def test_splice_rejects_empty_clause(corpus):
    with pytest.raises(ValueError):
        build_corrected_prompt(corpus["C01"], "   ", label="proportion")


def test_clean_stem_strips_style_line(corpus):
    stem = clean_stem_of(corpus["C13"])
    assert "Maintain the warm 2D Disney pencil-test render" not in stem
    assert "computer desk" in stem


def test_clean_stem_drops_but_tail_guard(corpus):
    """Cheap guard: a ', but …' defect tail is dropped if a defect prompt slips in.
    (Mid-sentence ', rendered …' defects are NOT strippable — caller error by the
    clean-pair contract; not asserted here.)"""
    assert "chibi" not in clean_stem_of(corpus["P-D1"]).lower()
    assert "standing idle" in clean_stem_of(corpus["P-D1"]).lower()
