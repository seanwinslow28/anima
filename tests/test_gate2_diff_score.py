# tests/test_gate2_diff_score.py
"""G6.9 Gate 2 + Gate 4 — judge-based diff scorers (mock-judge, $0).

Gate 2 (golden agreement): does Em's proposed corrective clause express the same
fix as Sean's ratified golden_diff? Binary, LLM-judged. Gate 4 (triage): a binary
rubric per diff, never the headline. Both judges are PLUGGABLE; these tests inject
a deterministic stub judge so the SCORING PLUMBING is proven with no model call.
The real judges + their mandatory calibration are deferred to the costed phase.
"""
from __future__ import annotations

from evals.vision_critic.diff_eval import (
    score_golden_agreement, score_triage, aggregate_diff_scores, DiffScore,
)


def _judge(reply: dict):
    """A stub judge: ignores the prompt, returns a fixed JSON reply (as the real
    judges would, raw text)."""
    import json
    return lambda prompt: json.dumps(reply)


# --------------------------------------------------------------------------- #
# Gate 2 — golden agreement
# --------------------------------------------------------------------------- #
def test_golden_agreement_judge_says_match():
    r = score_golden_agreement(
        em_value="wearing a navy-blue crew-neck t-shirt",
        golden_diff="wearing a navy crew-neck tee", defect_label="palette",
        judge=_judge({"match": True, "why": "same garment color fix"}))
    assert r["em_proposed"] is True
    assert r["match"] is True


def test_golden_agreement_judge_says_no():
    r = score_golden_agreement(
        em_value="make it more dynamic", golden_diff="wearing a navy crew-neck tee",
        defect_label="palette", judge=_judge({"match": False, "why": "unrelated"}))
    assert r["em_proposed"] is True
    assert r["match"] is False


def test_golden_agreement_no_patch_is_not_a_failure():
    """Em emitting NO diff is a real measured outcome (em_proposed=False), not a
    failed match — it must not be scored as match=False (that would conflate
    'proposed nothing' with 'proposed something wrong')."""
    r = score_golden_agreement(em_value=None, golden_diff="x", defect_label="palette",
                               judge=_judge({"match": True}))
    assert r["em_proposed"] is False
    assert r["match"] is None


def test_golden_agreement_tolerates_code_fenced_json():
    r = score_golden_agreement(
        em_value="a", golden_diff="b", defect_label="palette",
        judge=lambda p: '```json\n{"match": true}\n```')
    assert r["match"] is True


# --------------------------------------------------------------------------- #
# Gate 4 — triage rubric
# --------------------------------------------------------------------------- #
def test_triage_rubric_parses_all_axes():
    r = score_triage(
        em_value="wearing a navy-blue crew-neck t-shirt", defect_label="palette",
        expected_cites=["IR.sean.costume.navy-tee-cool-gray-jeans"], reasoning="shirt is red",
        judge=_judge({"targets_defect": True, "actionable": True,
                      "no_recharacterization": True, "style_neutral": True}))
    assert r == {"targets_defect": True, "actionable": True,
                 "no_recharacterization": True, "style_neutral": True}


# --------------------------------------------------------------------------- #
# Aggregation — per-class segmentation with bands
# --------------------------------------------------------------------------- #
def _ds(label, match, p, rcl):
    return DiffScore(name=f"{label}-x", defect_label=label, em_value="v",
                     golden_diff="g", em_proposed=True, golden_agreement=match,
                     cite_precision=p, cite_recall=rcl, triage=None)


def test_aggregate_segments_by_label_and_overall():
    scores = [
        _ds("palette", True, 1.0, 1.0),
        _ds("palette", False, 0.5, 1.0),
        _ds("proportion", True, 1.0, 1.0),
    ]
    agg = aggregate_diff_scores(scores)
    assert agg["overall"]["golden_agreement_rate"] == 2 / 3
    assert agg["by_label"]["palette"]["golden_agreement_rate"] == 0.5
    assert agg["by_label"]["proportion"]["golden_agreement_rate"] == 1.0
    # cite precision mean over the proposed diffs
    assert round(agg["overall"]["cite_precision_mean"], 3) == round((1.0 + 0.5 + 1.0) / 3, 3)


def test_aggregate_excludes_no_proposal_from_agreement_denominator():
    """proposal-rate and agreement-given-proposed are SEPARATE numbers (the brief's
    locked policy) — a no-proposal case must not drag the agreement rate to 0."""
    scores = [
        _ds("palette", True, 1.0, 1.0),
        DiffScore(name="palette-none", defect_label="palette", em_value=None,
                  golden_diff="g", em_proposed=False, golden_agreement=None,
                  cite_precision=0.0, cite_recall=None, triage=None),
    ]
    agg = aggregate_diff_scores(scores)
    assert agg["overall"]["proposal_rate"] == 0.5
    assert agg["overall"]["golden_agreement_rate"] == 1.0  # only the 1 proposed, matched
    assert agg["overall"]["agreement_scored_n"] == 1
