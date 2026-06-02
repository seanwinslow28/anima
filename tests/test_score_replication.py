"""A5 — replication in the costed scorer (score.py).

The N=1 point estimate hides run-to-run verdict variance — exactly the Opus
variance the 2026-06-02 re-baseline diagnosed. --runs N replicates each case N
times: the per-case MAJORITY verdict is the point estimate, and a per-segment
false_pass BAND (min/max + stderr across runs) plus a persisted per-run verdict
table make a flip (like the stylus case) visible instead of silently averaged
away. These tests pin the pure helpers with mocked verdicts — no model calls.
See docs/2026-06-02-em-provenance-and-hardening-kickoff.md §A5.
"""
from __future__ import annotations

from evals.vision_critic.score import (
    majority_verdict,
    consensus_scores,
    false_pass_band,
    render_per_run_table,
)
from evals.vision_critic.scoring import CaseScore


def _defect(name: str, predicted: str) -> CaseScore:
    """A labeled-defect (expected fail) identity_style case with a given prediction."""
    return CaseScore(
        name=name, case_class="identity_style",
        expected_verdict="fail", predicted_verdict=predicted,
        expected_cites=["IR.x"], actual_cites=(["IR.x"] if predicted != "pass" else []),
    )


def test_majority_verdict_flip_3pass_2fail_is_pass():
    assert majority_verdict(["pass", "pass", "fail", "pass", "fail"]) == "pass"


def test_majority_verdict_tie_prefers_more_conservative():
    # 1 pass / 1 fail tie → the defect-side verdict wins; a tie must not launder
    # a flagged defect into a pass.
    assert majority_verdict(["pass", "fail"]) == "fail"
    assert majority_verdict(["pass", "borderline"]) == "borderline"


def test_consensus_scores_uses_per_case_majority():
    # One case, 5 runs: 3 pass / 2 fail → consensus verdict = pass.
    runs = [
        [_defect("stylus", "pass")],
        [_defect("stylus", "pass")],
        [_defect("stylus", "fail")],
        [_defect("stylus", "pass")],
        [_defect("stylus", "fail")],
    ]
    consensus = consensus_scores(runs)
    assert len(consensus) == 1
    assert consensus[0].name == "stylus"
    assert consensus[0].predicted_verdict == "pass"


def test_false_pass_band_reports_min_max_mean_across_runs():
    # The flip case: 3 runs let the defect through (false pass → fp_rate 1.0),
    # 2 runs catch it (fp_rate 0.0). The band must surface 0.0..1.0, not a single
    # averaged number.
    runs = [
        [_defect("stylus", "pass")],
        [_defect("stylus", "pass")],
        [_defect("stylus", "fail")],
        [_defect("stylus", "pass")],
        [_defect("stylus", "fail")],
    ]
    band = false_pass_band(runs)
    performs = band["performs"]
    assert performs["min"] == 0.0
    assert performs["max"] == 1.0
    assert abs(performs["mean"] - 0.6) < 1e-9   # 3/5 runs false-pass
    assert performs["stderr"] > 0.0             # variance is real, not hidden
    assert len(performs["per_run"]) == 5


def test_render_per_run_table_marks_the_flip():
    runs = [
        [_defect("stylus", "pass")],
        [_defect("stylus", "fail")],
    ]
    table = render_per_run_table(runs)
    assert "stylus" in table
    assert "pass" in table and "fail" in table
    # A case whose verdicts disagree across runs is flagged as a flip.
    assert "FLIP" in table.upper()
