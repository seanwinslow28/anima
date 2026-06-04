# evals/vision_critic/runner.py  (PART 1 — scoring unit tests; PART 2 added in Task 6)
"""Em vision-critic eval — CI-green harness.

Two things live here:
  PART 1 — unit tests of scoring.py (pure functions, synthetic inputs).
  PART 2 — a mocked end-to-end pass proving the harness scores every case in
           cases.yaml and segments correctly, with intentionally-red cases
           xfailing. Stub verdicts → the matrix is degenerate; that is fine.
           CI asserts the HARNESS works, not that Em is accurate. The real
           scored matrix is score.py's job (deliberate, costed, live).

Run with: .venv/bin/pytest evals/vision_critic/runner.py -v
"""
from __future__ import annotations

from evals.vision_critic.scoring import (
    CaseScore,
    confusion_matrix,
    precision_recall,
    segment_report,
    cites_correctness,
    stderr,
)


def _score(expected, predicted, expected_cites=(), actual_cites=(), case_class="identity_style"):
    return CaseScore(
        name=f"{expected}->{predicted}",
        case_class=case_class,
        expected_verdict=expected,
        predicted_verdict=predicted,
        expected_cites=list(expected_cites),
        actual_cites=list(actual_cites),
        confidence=0.8,
        wall_s=1.0,
    )


def test_confusion_matrix_defect_class():
    scores = [
        _score("fail", "fail"),            # TP
        _score("borderline", "pass"),      # FN (false pass — costly)
        _score("pass", "fail"),            # FP (cheap false alarm)
        _score("pass", "pass"),            # TN
        _score("fail", "borderline"),      # TP (borderline counts as flagged)
    ]
    cm = confusion_matrix(scores)
    assert cm == {"tp": 2, "fp": 1, "fn": 1, "tn": 1}


def test_precision_recall_and_false_pass():
    cm = {"tp": 2, "fp": 1, "fn": 1, "tn": 1}
    pr = precision_recall(cm)
    assert pr["precision"] == 2 / 3
    assert pr["recall"] == 2 / 3
    # false-pass rate = FN / labeled-defects = 1 - recall on defects
    assert pr["false_pass_rate"] == 1 / 3


def test_precision_recall_zero_division_safe():
    pr = precision_recall({"tp": 0, "fp": 0, "fn": 0, "tn": 5})
    assert pr["precision"] == 0.0
    assert pr["recall"] == 0.0
    assert pr["false_pass_rate"] == 0.0


def test_segment_report_splits_classes():
    scores = [
        _score("fail", "fail", case_class="identity_style"),
        _score("pass", "pass", case_class="clean"),
        _score("fail", "pass", case_class="motion_proper"),  # expected-red FN
    ]
    rep = segment_report(scores)
    # identity_style + clean reported together as "performs"; motion_proper apart.
    assert "performs" in rep and "motion_proper" in rep
    assert rep["motion_proper"]["cm"]["fn"] == 1
    assert rep["performs"]["cm"]["tp"] == 1
    assert rep["performs"]["cm"]["tn"] == 1


def test_cites_correctness_requires_one_expected_hit():
    # flagged + cites a correct criterion → correct.
    assert cites_correctness(
        predicted="fail", expected_cites=["IR.sean.proportion.x", "SF02"],
        actual_cites=["SF02"],
    ) is True
    # flagged but cites nothing relevant → incorrect.
    assert cites_correctness(
        predicted="fail", expected_cites=["IR.sean.proportion.x"],
        actual_cites=["AC99"],
    ) is False
    # pass verdict → citation correctness is N/A (None).
    assert cites_correctness(
        predicted="pass", expected_cites=[], actual_cites=[],
    ) is None


def test_stderr_of_proportion():
    # stderr of a pass-rate p over n samples = sqrt(p(1-p)/n).
    assert round(stderr(p=0.5, n=100), 4) == 0.05
    assert stderr(p=1.0, n=10) == 0.0
    assert stderr(p=0.5, n=0) == 0.0


# ============================================================================
# PART 2 — mocked end-to-end harness (credential-free, proves scoring plumbing)
# ============================================================================
from pathlib import Path

import pytest
import yaml

from pipeline.agents import AgentContext
from pipeline.agents.vision_critic import VisionCriticNode
from evals.vision_critic.conftest import (
    make_vision_verdict, _FakeCLIResponse, _FakeSDKResponse,
)
from evals.vision_critic.scoring import CaseScore, segment_report

_CASES = yaml.safe_load(
    (Path(__file__).parent / "cases.yaml").read_text(encoding="utf-8")
)["cases"]
_FIXTURES = Path(__file__).parent / "fixtures"

from evals.vision_critic.conftest import eval_manifest, merged_criteria

_EVAL_MANIFEST = eval_manifest()
_MERGED_CRITERIA = merged_criteria(_EVAL_MANIFEST)


def _patch_em_runners(monkeypatch, verdict_json: str):
    """Stub EVERY Em transport with a fixed verdict so the harness is credential-free.

    Em selects its Gemini transport from critics.t2.transport: `agy`
    (run_antigravity_with_image) or `gemini_api` (run_gemini_api_with_image).
    Both must be patched — the gemini_api runner resolves GEMINI_API_KEY straight
    from .env, so leaving it un-stubbed makes "mocked" runner.py fire REAL costed
    calls on any machine with a key (the 2026-06-04 G5 pre-flight cost-leak: the
    mock predated the 2026-06-02 agy→gemini_api pivot and never covered the new
    transport)."""
    async def fake_gemini(*, prompt, image_paths, timeout_s=120):
        return _FakeCLIResponse(text=verdict_json)

    async def fake_opus(*, prompt, image_paths, timeout_s=120):
        return _FakeSDKResponse(text=verdict_json)

    monkeypatch.setattr("pipeline.agents.vision_critic.run_antigravity_with_image", fake_gemini)
    monkeypatch.setattr("pipeline.agents.vision_critic.run_gemini_api_with_image", fake_gemini)
    monkeypatch.setattr("pipeline.agents.vision_critic.invoke_opus_vision", fake_opus)


def _ctx_for_case(case: dict) -> AgentContext:
    return AgentContext(
        run_dir=Path("/tmp/em-eval"),
        inputs={
            "image_path": str(_FIXTURES / case["input"]),
            "beat_description": case["beat_description"],
            "frame_id": case["name"],
            "impact_tags": case.get("impact_tags", []),
            "checkpoint": case["checkpoint"],
            "character_id": case.get("character_id", "sean"),
        },
        manifest=_EVAL_MANIFEST,
        criteria=_MERGED_CRITERIA,
        tier="draft",
        cache_dir=Path("/tmp/em-eval/.cache"),
    )


@pytest.mark.parametrize("case", _CASES, ids=[c["name"] for c in _CASES])
def test_harness_scores_every_case(case, monkeypatch, request):
    """Mocked: Em runs against each fixture under a fixed verdict; we assert the
    harness produces a CaseScore. Accuracy is NOT asserted here (stub verdict).
    Intentionally-red cases xfail (Em is expected to miss motion-proper)."""
    if case.get("is_intentionally_red"):
        request.node.add_marker(pytest.mark.xfail(
            reason=f"intentionally red: {case['description']}", strict=False))

    # Stub verdict echoes the EXPECTED verdict so non-red cases "pass" the
    # harness check — this proves scoring wiring, not Em's real judgment.
    stub = make_vision_verdict(
        verdict=case["expected_verdict"],
        cites=case.get("expected_cites") or None,
    )
    _patch_em_runners(monkeypatch, stub)

    result = VisionCriticNode().run(_ctx_for_case(case))
    score = CaseScore(
        name=case["name"],
        case_class=case["case_class"],
        expected_verdict=case["expected_verdict"],
        predicted_verdict=result.outputs["verdict"],
        expected_cites=case.get("expected_cites", []),
        actual_cites=result.cites_criteria,
        confidence=result.outputs["confidence"],
        wall_s=0.0,
    )
    assert score.predicted_verdict in {"pass", "borderline", "fail"}
    # For non-red cases the stub echoes expected → exact match (harness sanity).
    assert score.exact_match


def test_segment_report_well_formed(monkeypatch):
    """Run all cases under a fixed 'pass' stub and assert the segmented report
    has the three blocks with integer confusion matrices."""
    _patch_em_runners(monkeypatch, make_vision_verdict(verdict="pass"))
    scores = []
    for case in _CASES:
        result = VisionCriticNode().run(_ctx_for_case(case))
        scores.append(CaseScore(
            name=case["name"], case_class=case["case_class"],
            expected_verdict=case["expected_verdict"],
            predicted_verdict=result.outputs["verdict"],
            expected_cites=case.get("expected_cites", []),
            actual_cites=result.cites_criteria,
        ))
    rep = segment_report(scores)
    for block in ("overall", "performs", "motion_proper"):
        assert block in rep
        assert set(rep[block]["cm"]) == {"tp", "fp", "fn", "tn"}
