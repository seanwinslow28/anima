"""score.py's report rendering is pure and testable without model calls."""
from evals.vision_critic.score import render_last_run_md, render_per_case_detail
from evals.vision_critic.scoring import CaseScore, segment_report


def test_render_last_run_md_has_segments_and_false_pass():
    scores = [
        CaseScore("a", "identity_style", "fail", "fail", ["IR.x"], ["IR.x"]),
        CaseScore("b", "clean", "pass", "pass"),
        CaseScore("c", "motion_proper", "fail", "pass", ["SF01"], []),
    ]
    md = render_last_run_md(segment_report(scores), model_label="gemini-3.1-pro@agy", n_total=3)
    assert "Performs (identity/style + clean)" in md
    assert "Motion-proper (expected red)" in md
    assert "false_pass_rate" in md.lower() or "false pass" in md.lower()
    assert "gemini-3.1-pro@agy" in md


def test_render_per_case_detail_surfaces_cites_and_reasoning():
    """G6.2 diagnostic: the per-case detail section must persist each case's
    actual_cites, the cites_correct judgement, and Em's reasoning prose."""
    scores = [
        # A correctly-grounded defect: expected cite appears in actual_cites.
        CaseScore("palette-pd1", "identity_style", "fail", "fail",
                  ["IR.sean.palette.warm-graphite"], ["IR.sean.palette.warm-graphite"],
                  confidence=0.9, reasoning="Palette runs cold; greys are blue-shifted."),
        # A clean pass (no cite required -> cites_correct n/a).
        CaseScore("clean-c01", "clean", "pass", "pass", confidence=0.8,
                  reasoning="Reads on-model and on-register."),
    ]
    md = render_per_case_detail(scores)
    # Reasoning prose is persisted verbatim (newlines stripped, never lost).
    assert "Palette runs cold; greys are blue-shifted." in md
    assert "Reads on-model and on-register." in md
    # actual_cites are rendered.
    assert "IR.sean.palette.warm-graphite" in md
    # cites_correct uses the existing scorer: grounded defect -> yes; clean -> n/a.
    assert "yes" in md
    assert "n/a" in md
    # the case names anchor the rows.
    assert "palette-pd1" in md and "clean-c01" in md
