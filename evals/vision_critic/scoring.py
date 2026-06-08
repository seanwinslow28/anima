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
import re
from dataclasses import dataclass, field

_FLAGGED = {"fail", "borderline"}

# --------------------------------------------------------------------------- #
# Citation grounding (G6.1, 2026-06-07). Two axes scored separately: verdict
# accuracy (the confusion matrix above) and CITATION accuracy (did Em name the
# right Bible criterion when she flagged a defect). Citation credit is TIERED:
#   - full (1.0)    : a leaf-normalized IR-handle match against an expected cite
#   - partial (0.5) : the correct manifest QA reason-code for the defect class
#                     (Em reflexively pairs the right code on geometry defects —
#                     credit it as partial grounding, not zero)
#   - none (0.0)    : flagged but no creditable citation (incl. a clean fixture
#                     wrongly flagged — a false positive grounds nothing)
# The matcher normalizes NAMESPACE (sean-anchor -> sean) and number FORMAT
# (1-to-7 <-> 1-7) but STILL REQUIRES THE CORRECT LEAF — it measures "did she
# name the right criterion," not a loosening that flatters her. The de-confound
# (2026-06-04 instrumented mini-run, Q3) showed Em's proportion misses were
# pure namespace/format drift (IR.sean-anchor.proportion.head-to-body-1-7 vs the
# real IR.sean.proportion.head-to-body-1-to-7); those recover here, a wrong leaf
# does not.
_PARTIAL_CREDIT = 0.5

# Per the G6.1 handoff (Sean, 2026-06-06): the manifest QA reason-code Em
# reflexively substitutes for a real handle, keyed by the EXPECTED criterion's
# IR category. A correct substitution earns partial grounding. anatomy and style
# are intentionally absent: once those classes have citeable handles (the G6.1
# Bible add + the style-handle surfacing in _criteria_block), the real handle is
# reachable, so a reason-code substitution there scores none — it must cite the
# rule. proportion->SF03, view->HF03 (wrong direction), pose->HF04, identity
# (face/hair)->SF02.
_REASON_CODE_FOR_CATEGORY: dict[str, frozenset[str]] = {
    "proportion": frozenset({"SF03"}),
    "view": frozenset({"HF03"}),
    "pose": frozenset({"HF04"}),
    "face": frozenset({"SF02"}),
    "hair": frozenset({"SF02"}),
}

_TO_BETWEEN_DIGITS = re.compile(r"(\d)-to-(\d)")


def normalize_cite(cite: str) -> str:
    """Canonical (category, leaf) form of a citation, namespace/format-insensitive.

    Drops the `IR` prefix and the character_id segment (so `IR.sean.X`,
    `IR.sean-anchor.X`, and a bare category-led `view.X` collapse together) and
    canonicalizes number format (`1-to-7` -> `1-7`) and `_`->`-`. The LEAF is
    preserved exactly — `head-to-body` and `head-to-body-1-to-7` stay distinct,
    so a wrong/incomplete leaf still fails. Returns `category.leaf`.
    """
    s = cite.strip().lower().rstrip(".").replace("_", "-")
    parts = [p for p in s.split(".") if p]
    if parts and parts[0] == "ir":
        parts = parts[1:]          # drop 'ir'
        if parts:
            parts = parts[1:]      # drop the character_id segment (sean / sean-anchor)
    if not parts:
        return s
    category = parts[0]
    leaf = "-".join(parts[1:])
    leaf = _TO_BETWEEN_DIGITS.sub(r"\1-\2", leaf)   # 1-to-7 -> 1-7 (both directions canon)
    return f"{category}.{leaf}" if leaf else category


def _expected_category(expected_cites: list[str]) -> str | None:
    """The IR category of the (first) expected criterion — keys the reason-code
    partial-credit lookup. Returns None when no category can be parsed."""
    for c in expected_cites:
        norm = normalize_cite(c)
        if "." in norm:
            return norm.split(".", 1)[0]
    return None


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
    reasoning: str = ""   # Em's verdict prose (G6.2 instrumentation). Carried for
                          # the per-case diagnostic trace; never scored. Default ""
                          # keeps positional constructors + the asdict<->CaseScore(**)
                          # subprocess round-trip (score.py) back-compatible.

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

    @property
    def citation_credit(self) -> float | None:
        """The CITATION axis for this case, scored independently of the verdict
        axis (G6.1). None when the verdict is pass (N/A); else 0.0 / 0.5 / 1.0
        per cites_correctness. Carries expected_verdict so the clean-FP fix
        engages."""
        return cites_correctness(
            predicted=self.predicted_verdict,
            expected_cites=self.expected_cites,
            actual_cites=self.actual_cites,
            expected_verdict=self.expected_verdict,
        )


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
                      actual_cites: list[str],
                      expected_verdict: str | None = None) -> float | None:
    """Graded citation credit when Em flags a defect (G6.1 tiered scoring).

    Returns:
      - None  when N/A (verdict is pass — no citation required/expected).
      - 0.0   flagged but no creditable citation. INCLUDES a clean fixture
              wrongly flagged (expected_verdict == 'pass'): a false positive
              grounds nothing, so it scores none, not credit (the clean-c06
              quirk fix — previously an FP with any non-empty cite scored True).
      - 0.5   the correct manifest QA reason-code for the expected defect class
              (partial grounding; see _REASON_CODE_FOR_CATEGORY).
      - 1.0   a leaf-normalized IR-handle match against an expected criterion.

    The leaf-normalized matcher (normalize_cite) is namespace/format-insensitive
    but leaf-exact — a wrong leaf never matches. `expected_verdict` is optional
    for back-compat; pass it (callers have it on CaseScore) so the clean-FP fix
    engages.
    """
    if predicted not in _FLAGGED:
        return None
    # Clean fixture wrongly flagged: a false positive cannot be "correctly
    # grounded" — the defect it cites does not exist. Score none, never credit.
    if expected_verdict == "pass":
        return 0.0
    if not expected_cites:
        # Flagged with no declared expected criterion — the cites_criteria
        # invariant is satisfied iff Em cited something. Full credit / none.
        return 1.0 if actual_cites else 0.0
    norm_actual = {normalize_cite(c) for c in actual_cites}
    if any(normalize_cite(e) in norm_actual for e in expected_cites):
        return 1.0
    # Partial: the right manifest reason-code for the expected defect class.
    category = _expected_category(expected_cites)
    codes = _REASON_CODE_FOR_CATEGORY.get(category or "", frozenset())
    if codes & {c.strip().upper() for c in actual_cites}:
        return _PARTIAL_CREDIT
    return 0.0


def stderr(*, p: float, n: int) -> float:
    """Standard error of a proportion p over n samples (findings §5 borrow #2)."""
    if n <= 0:
        return 0.0
    return math.sqrt(max(0.0, p * (1 - p)) / n)


def _block(scores: list[CaseScore]) -> dict:
    cm = confusion_matrix(scores)
    pr = precision_recall(cm)
    n = len(scores)
    # Citation axis (scored independently of the verdict axis above). Graded:
    # 1.0 full IR-handle / 0.5 partial reason-code / 0.0 none; None = pass (N/A).
    cites = [s.citation_credit for s in scores]
    cites_scored = [c for c in cites if c is not None]
    return {
        "n": n,
        "cm": cm,
        **pr,
        "recall_stderr": stderr(p=pr["recall"], n=cm["tp"] + cm["fn"]),
        "exact_agreement": exact_agreement(scores),
        "false_passes": [s.name for s in scores if s.is_false_pass],
        "borderline_slippages": [s.name for s in scores if s.borderline_slippage],
        # cites_correct is the GRADED mean over flagged cases (full=1.0, partial=0.5).
        "cites_correct": (sum(cites_scored) / len(cites_scored))
                         if cites_scored else None,
        # Split-axis legibility: how the flagged-case citations distribute.
        "cites_scored_n": len(cites_scored),
        "cites_full": sum(1 for c in cites_scored if c == 1.0),
        "cites_partial": sum(1 for c in cites_scored if 0.0 < c < 1.0),
        "cites_none": sum(1 for c in cites_scored if c == 0.0),
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
