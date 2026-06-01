"""score.py's report rendering is pure and testable without model calls."""
from evals.vision_critic.score import render_last_run_md
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
