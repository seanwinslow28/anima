"""Pure scoring functions for the Em vision-critic eval.

The metric contract (docs/research/2026-05-31-ai-evals-...md §4):
  - precision/recall on the DEFECT CLASS, reported separately
  - false-pass rate front and center (the costly error: a drifted frame let
    through). false_pass_rate = FN / labeled-defects = 1 - recall.
  - never raw agreement as the headline (misleads under class imbalance)
  - never F1 alone (hides true negatives / the false-pass blind spot)

Defect-class convention: a verdict in {fail, borderline} flags a defect; pass
is clean. So borderline counts as "flagged" for detection. A separate 3-way
exact-verdict view and the borderline->pass slippage are scored too.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

_FLAGGED = {"fail", "borderline"}


@dataclass
class CaseScore:
    name: str
    case_class: str            # identity_style | clean | motion_proper
    expected_verdict: str      # pass | borderline | fail
    predicted_verdict: str
    expected_cites: list[str] = field(default_factory=list)
    actual_cites: list[str] = field(default_factory=list)
    confidence: float = 0.0
    wall_s: float = 0.0

    @property
    def expected_defect(self) -> bool:
        return self.expected_verdict in _FLAGGED

    @property
    def predicted_defect(self) -> bool:
        return self.predicted_verdict in _FLAGGED

    @property
    def exact_match(self) -> bool:
        return self.expected_verdict == self.predicted_verdict

    @property
    def is_false_pass(self) -> bool:
        # Labeled a defect, Em said pass — the costly error.
        return self.expected_defect and self.predicted_verdict == "pass"

    @property
    def borderline_slippage(self) -> bool:
        # Expected a hard fail, Em softened to borderline (or pass).
        return self.expected_verdict == "fail" and self.predicted_verdict != "fail"


def confusion_matrix(scores: list[CaseScore]) -> dict[str, int]:
    tp = fp = fn = tn = 0
    for s in scores:
        if s.expected_defect and s.predicted_defect:
            tp += 1
        elif (not s.expected_defect) and s.predicted_defect:
            fp += 1
        elif s.expected_defect and (not s.predicted_defect):
            fn += 1
        else:
            tn += 1
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}


def precision_recall(cm: dict[str, int]) -> dict[str, float]:
    tp, fp, fn = cm["tp"], cm["fp"], cm["fn"]
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    false_pass_rate = fn / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return {
        "precision": precision,
        "recall": recall,
        "false_pass_rate": false_pass_rate,
        "f1": f1,  # secondary only — never the headline
    }


def exact_agreement(scores: list[CaseScore]) -> float:
    if not scores:
        return 0.0
    return sum(1 for s in scores if s.exact_match) / len(scores)


def cites_correctness(*, predicted: str, expected_cites: list[str],
                      actual_cites: list[str]) -> bool | None:
    """Did Em cite a correct criterion when she flagged a defect?

    Returns None when N/A (verdict is pass — no citation required/expected).
    Returns True if at least one expected criterion appears in actual_cites.
    """
    if predicted not in _FLAGGED:
        return None
    if not expected_cites:
        # Flagged but the case declared no specific expected criterion — any
        # non-empty citation counts (the cites_criteria invariant is satisfied).
        return bool(actual_cites)
    return any(c in actual_cites for c in expected_cites)


def stderr(*, p: float, n: int) -> float:
    """Standard error of a proportion p over n samples (findings §5 borrow #2)."""
    if n <= 0:
        return 0.0
    return math.sqrt(max(0.0, p * (1 - p)) / n)


def _block(scores: list[CaseScore]) -> dict:
    cm = confusion_matrix(scores)
    pr = precision_recall(cm)
    n = len(scores)
    cites = [cites_correctness(predicted=s.predicted_verdict,
                               expected_cites=s.expected_cites,
                               actual_cites=s.actual_cites) for s in scores]
    cites_scored = [c for c in cites if c is not None]
    return {
        "n": n,
        "cm": cm,
        **pr,
        "recall_stderr": stderr(p=pr["recall"], n=cm["tp"] + cm["fn"]),
        "exact_agreement": exact_agreement(scores),
        "false_passes": [s.name for s in scores if s.is_false_pass],
        "borderline_slippages": [s.name for s in scores if s.borderline_slippage],
        "cites_correct": (sum(1 for c in cites_scored if c) / len(cites_scored))
                         if cites_scored else None,
        "mean_wall_s": (sum(s.wall_s for s in scores) / n) if n else 0.0,
    }


def segment_report(scores: list[CaseScore]) -> dict:
    """Segment per Sean's call: the cases Em SHOULD perform on (identity_style
    + clean) reported together as 'performs'; motion_proper (expected-red)
    reported apart so it doesn't bury the contact sheet's real performance.
    Plus an 'overall' block.
    """
    performs = [s for s in scores if s.case_class in ("identity_style", "clean")]
    motion = [s for s in scores if s.case_class == "motion_proper"]
    return {
        "overall": _block(scores),
        "performs": _block(performs),
        "motion_proper": _block(motion),
    }
