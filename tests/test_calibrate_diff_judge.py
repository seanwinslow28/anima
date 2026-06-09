# tests/test_calibrate_diff_judge.py
"""Tier 1 — Gate-2 golden-agreement judge CALIBRATION harness (G6.9 follow-on).

These tests pin the math + plumbing of evals/vision_critic/calibrate_diff_judge.py
WITHOUT any model call (the SF03 scaffold-first discipline). The calibration run
itself is costed + Sean-labeled; here we prove the ruler is honest:

  - the positive class is MATCH (the dangerous error is the judge over-calling
    match), so FPR = FP/(FP+TN) — NOT scoring.precision_recall's verdict-suite
    false_pass_rate (FN/(TP+FN)); the two are explicitly contrasted below;
  - "no diff proposed" stays match=None and is EXCLUDED from the matrix, never a 0;
  - N=5 majority vote (sampling consistency > verbalized confidence);
  - Cohen's κ over the 2x2;
  - the credential-free --check-only pipeline runs end-to-end (no scored claim);
  - live Em-diff capture asserts non-empty before any spend (kills the
    2026-06-07 "measured nothing" mode).

Credential-free: the judge is a stub / injected, so no model is called, nothing spent.
"""
from __future__ import annotations

import json

import pytest

import evals.vision_critic.calibrate_diff_judge as cal


# --------------------------------------------------------------------------- #
# Cohen's κ (no helper existed in scoring.py — built here)
# --------------------------------------------------------------------------- #
def test_cohens_kappa_perfect_agreement():
    # Only TP + TN, both classes present → κ == 1.0.
    assert cal.cohens_kappa({"tp": 5, "fp": 0, "fn": 0, "tn": 5}) == 1.0


def test_cohens_kappa_zero_at_chance():
    # judge ⟂ Sean: po == pe → κ == 0.0.
    assert cal.cohens_kappa({"tp": 25, "fp": 25, "fn": 25, "tn": 25}) == 0.0


def test_cohens_kappa_known_value():
    # Worked example: po=0.70, pe=0.50 → κ=(0.70-0.50)/(1-0.50)=0.40.
    assert round(cal.cohens_kappa({"tp": 20, "fp": 5, "fn": 10, "tn": 15}), 4) == 0.4


def test_cohens_kappa_degenerate_and_empty():
    # No variance (all match) → perfect agreement returns 1.0, not a div-by-zero.
    assert cal.cohens_kappa({"tp": 10, "fp": 0, "fn": 0, "tn": 0}) == 1.0
    # Empty matrix → 0.0 (no crash).
    assert cal.cohens_kappa({"tp": 0, "fp": 0, "fn": 0, "tn": 0}) == 0.0


# --------------------------------------------------------------------------- #
# Match-class confusion matrix (positive class = MATCH)
# --------------------------------------------------------------------------- #
def _scored(judge_match, sean_match, *, label="palette", em_proposed=True, kind="real", pid=None):
    return cal.Scored(
        pair_id=pid or f"{judge_match}-{sean_match}",
        defect_label=label,
        kind=kind,
        em_proposed=em_proposed,
        judge_match=judge_match,
        sean_match=sean_match,
        votes=[bool(judge_match)] * 5 if judge_match is not None else [],
    )


def test_match_confusion_positive_class_is_match():
    scored = [
        _scored(True, True),                       # TP
        _scored(True, False),                      # FP  ← the dangerous over-call
        _scored(False, True),                      # FN
        _scored(False, False),                     # TN
        _scored(None, None, em_proposed=False),    # no diff proposed → EXCLUDED
        _scored(True, None),                       # Sean unlabeled → EXCLUDED
    ]
    cm = cal.match_confusion(scored)
    assert cm == {"tp": 1, "fp": 1, "fn": 1, "tn": 1}


def test_match_metrics_fpr_is_match_overcall_not_verdict_false_pass():
    cm = {"tp": 2, "fp": 1, "fn": 1, "tn": 1}
    m = cal.match_metrics(cm)
    assert m["precision"] == 2 / 3
    assert m["recall"] == 2 / 3
    # The dangerous error for THIS proxy: judge over-calls match on a true non-match.
    # FPR = FP / (FP + TN) = 1 / 2 — distinct from the verdict suite's
    # false_pass_rate = FN/(TP+FN) = 1/3.
    assert m["fpr"] == 1 / 2
    assert m["raw_agreement"] == 3 / 5  # imbalance-sensitive; never the headline


def test_match_metrics_zero_division_safe():
    m = cal.match_metrics({"tp": 0, "fp": 0, "fn": 0, "tn": 0})
    assert m["precision"] == 0.0 and m["recall"] == 0.0
    assert m["fpr"] == 0.0 and m["raw_agreement"] == 0.0


# --------------------------------------------------------------------------- #
# N=5 majority vote
# --------------------------------------------------------------------------- #
class _SeqJudge:
    """Returns a preset sequence of match verdicts as JSON (one per call)."""
    def __init__(self, verdicts):
        self.verdicts = list(verdicts)
        self.calls = 0

    def __call__(self, prompt):
        v = self.verdicts[self.calls]
        self.calls += 1
        return json.dumps({"match": v, "why": "seq"})


def test_judge_majority_three_of_five_wins():
    j = _SeqJudge([True, True, True, False, False])
    out = cal.judge_pair_majority(candidate="recolor it", golden="recolor it",
                                  defect_label="palette", judge=j, n=5)
    assert out["em_proposed"] is True
    assert out["majority_match"] is True
    assert out["spread"] == (3, 5)
    assert j.calls == 5


def test_judge_majority_one_of_five_loses():
    j = _SeqJudge([True, False, False, False, False])
    out = cal.judge_pair_majority(candidate="x", golden="y",
                                  defect_label="palette", judge=j, n=5)
    assert out["majority_match"] is False
    assert out["spread"] == (1, 5)


def test_judge_majority_no_diff_is_none_and_judge_not_called():
    def _exploding_judge(prompt):
        raise AssertionError("judge must not be called when Em proposed no diff")

    out = cal.judge_pair_majority(candidate=None, golden="y",
                                  defect_label="palette", judge=_exploding_judge, n=5)
    assert out["em_proposed"] is False
    assert out["majority_match"] is None       # never a 0
    assert out["votes"] == []


# --------------------------------------------------------------------------- #
# Aggregation + run_calibration (join labels, segment by class)
# --------------------------------------------------------------------------- #
def test_aggregate_overall_and_by_label():
    scored = [
        _scored(True, True, label="palette"),
        _scored(True, False, label="palette"),
        _scored(False, False, label="view-correctness"),
    ]
    agg = cal.aggregate(scored)
    assert "overall" in agg and "by_label" in agg
    assert set(agg["by_label"]) == {"palette", "view-correctness"}
    assert agg["overall"]["cm"] == {"tp": 1, "fp": 1, "fn": 0, "tn": 1}
    for block in (agg["overall"], *agg["by_label"].values()):
        assert "kappa" in block and "fpr" in block and "precision" in block


def test_run_calibration_joins_labels_and_excludes_unlabeled():
    pairs = [
        cal.Pair(pair_id="p-match", defect_label="palette", kind="real",
                 candidate="recolor", golden="recolor it fully"),
        cal.Pair(pair_id="p-nomatch", defect_label="palette", kind="cross_negative",
                 candidate="add a sixth finger", golden="recolor it fully"),
        cal.Pair(pair_id="p-noprop", defect_label="view-correctness", kind="real",
                 candidate=None, golden="redraw as profile"),
    ]
    labels = {
        "p-match": {"sean_match": True, "sean_why": "same intent"},
        "p-nomatch": {"sean_match": False, "sean_why": "different defect"},
        # p-noprop: Em proposed nothing → sean_match N/A; excluded from the matrix.
    }
    scored, agg = cal.run_calibration(pairs, labels, judge=cal._stub_judge, n=5)
    # The stub always says match=True → p-match TP, p-nomatch FP, p-noprop excluded.
    assert agg["overall"]["cm"] == {"tp": 1, "fp": 1, "fn": 0, "tn": 0}
    by_pid = {s.pair_id: s for s in scored}
    assert by_pid["p-noprop"].em_proposed is False
    assert by_pid["p-noprop"].judge_match is None
    assert agg["overall"]["n_no_proposal"] == 1


def test_synthetic_check_pipeline_runs_credential_free():
    """The --check-only path: full pipeline on a stub judge + synthetic labels,
    well-formed aggregate, NO scored claim, no model call."""
    agg = cal._synthetic_check()
    assert "overall" in agg and "by_label" in agg
    assert set(agg["overall"]["cm"]) == {"tp", "fp", "fn", "tn"}


# --------------------------------------------------------------------------- #
# Live-capture assembly (capture_fn injected; no real Em call in CI)
# --------------------------------------------------------------------------- #
def test_capture_assembles_jsonl_rows_and_passes_nonempty_guard():
    cases = [
        {"name": "palette-x", "defect_label": "palette",
         "golden_diff": "recolor it", "expected_cites": ["IR.sean.palette.full-color"]},
        {"name": "view-y", "defect_label": "view-correctness",
         "golden_diff": "redraw profile", "expected_cites": []},
    ]

    def fake_capture(case, *, manifest, criteria):
        return f"em-clause-for-{case['name']}"

    rows = cal.capture_em_diffs(cases, manifest={}, criteria=None, capture_fn=fake_capture)
    assert [r["name"] for r in rows] == ["palette-x", "view-y"]
    assert rows[0]["em_value"] == "em-clause-for-palette-x"
    assert rows[0]["golden_diff"] == "recolor it"
    assert rows[0]["defect_label"] == "palette"


def test_capture_raises_when_every_diff_empty():
    cases = [{"name": "a", "defect_label": "palette", "golden_diff": "g", "expected_cites": []}]

    def empty_capture(case, *, manifest, criteria):
        return None

    with pytest.raises(RuntimeError, match="non-empty"):
        cal.capture_em_diffs(cases, manifest={}, criteria=None, capture_fn=empty_capture)


def test_capture_contains_per_case_failure_as_none_gap():
    """A worker that dies on ONE case is an honest None gap (with a reason), NOT a
    run-aborting crash — the Gate-3 v1 containment lesson applied to capture."""
    cases = [
        {"name": "a", "defect_label": "palette", "golden_diff": "g", "expected_cites": []},
        {"name": "b-dies", "defect_label": "palette", "golden_diff": "g", "expected_cites": []},
        {"name": "c", "defect_label": "palette", "golden_diff": "g", "expected_cites": []},
    ]

    def flaky(case, *, manifest, criteria):
        if case["name"] == "b-dies":
            raise RuntimeError("worker died")
        return f"clause-{case['name']}"

    rows = cal.capture_em_diffs(cases, manifest={}, criteria=None, capture_fn=flaky)
    vals = {r["name"]: r["em_value"] for r in rows}
    assert vals == {"a": "clause-a", "b-dies": None, "c": "clause-c"}
    assert rows[1]["error"] and "worker died" in rows[1]["error"]


def test_capture_calls_on_row_incrementally():
    """on_row fires per case so partial progress persists if the long run dies."""
    cases = [
        {"name": "a", "defect_label": "palette", "golden_diff": "g", "expected_cites": []},
        {"name": "b", "defect_label": "palette", "golden_diff": "g", "expected_cites": []},
    ]
    seen = []
    cal.capture_em_diffs(cases, manifest={}, criteria=None,
                         capture_fn=lambda case, *, manifest, criteria: "x",
                         on_row=seen.append)
    assert [r["name"] for r in seen] == ["a", "b"]


def test_subprocess_capture_value_parses_value_empty_and_guards_stub(monkeypatch):
    import subprocess

    def _fake(returncode, stdout, stderr=""):
        class R:
            pass
        r = R()
        r.returncode, r.stdout, r.stderr = returncode, stdout, stderr
        return lambda *a, **k: r

    # rc 0 with a real clause → returns it.
    monkeypatch.setattr(subprocess, "run", _fake(0, json.dumps([{"value": "real clause"}])))
    assert cal._subprocess_capture_value("x") == "real clause"

    # rc 4 (flagged case captured no diffs) → None, never a crash.
    monkeypatch.setattr(subprocess, "run", _fake(4, "[]", "no diffs"))
    assert cal._subprocess_capture_value("x") is None

    # A STUB value means the live path silently fell back → hard stop.
    monkeypatch.setattr(subprocess, "run", _fake(0, json.dumps([{"value": "STUB corrective clause"}])))
    with pytest.raises(RuntimeError, match="STUB"):
        cal._subprocess_capture_value("x")
