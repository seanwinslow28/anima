# tests/test_gate3_null_lift.py
"""G6.9 Gate 3 — costed-run additions: null/placebo arm, normalized lift, em-capture.

Sean's locked attribution (2026-06-08): the first costed run adds a NULL/placebo arm
so fix-rate is read as normalized lift (em − null)/(golden − null), with the per-class
floor exposed. These tests pin that machinery on stubs ($0); no live model call.
"""
from __future__ import annotations

import yaml
from pathlib import Path

from pipeline.agents import AgentContext
from pipeline.agents.vision_critic import VisionCriticNode
from evals.vision_critic.conftest import (
    make_vision_verdict, _FakeCLIResponse, _FakeSDKResponse, eval_manifest, merged_criteria,
)
from evals.vision_critic.prompt_apply import parse_corpus
from evals.vision_critic.patch_efficacy import (
    _NULL_CLAUSE, _ARM_SETS, normalized_lift, estimate_cost, run_case, select_sample,
    _capture_em_value, FakeRegen, FakeCritique,
)

_ROOT = Path(__file__).resolve().parents[1]
_DEFECTS = [c for c in yaml.safe_load((_ROOT / "evals/vision_critic/cases.yaml").read_text())["cases"]
            if c["case_class"] == "identity_style"]
_CORPUS = parse_corpus(_ROOT / "prompts/eval-corpus/sean-anchor-fixture-corpus.md")


def _case(label):
    return next(c for c in _DEFECTS if c["defect_label"] == label and c["expected_verdict"] == "fail")


# --------------------------------------------------------------------------- #
# Null/placebo arm
# --------------------------------------------------------------------------- #
def test_arm_sets_both_plus_null_is_the_default_baseline():
    assert _ARM_SETS["both+null"] == ("em", "golden", "null")
    assert _ARM_SETS["all"] == ("em", "golden", "null")


def test_null_arm_splices_the_fixed_placebo_clause():
    fake = FakeRegen(stub=True)
    eff = run_case(_case("palette"), arms=["null"], rerolls=2, corpus=_CORPUS,
                   manifest={}, criteria=None,
                   regenerate_fn=fake, recritique_fn=FakeCritique(verdict="pass", cites=[]))
    assert eff.arms["null"].clause == _NULL_CLAUSE
    assert fake.calls == 2  # null regenerates like the real arms (it's a floor control)


def test_three_arms_run_independently():
    c = _case("palette")
    eff = run_case(c, arms=["em", "golden", "null"], rerolls=1, corpus=_CORPUS,
                   manifest={}, criteria=None, em_value="navy tee",
                   regenerate_fn=FakeRegen(stub=True),
                   recritique_fn=FakeCritique(verdict="pass", cites=[]))
    assert set(eff.arms) == {"em", "golden", "null"}
    assert eff.arms["golden"].clause == c["golden_diff"]
    assert eff.arms["em"].clause == "navy tee"
    assert eff.arms["null"].clause == _NULL_CLAUSE


# --------------------------------------------------------------------------- #
# Normalized lift (em − null)/(golden − null)
# --------------------------------------------------------------------------- #
def _agg(em, gold, null):
    def arm(r):
        return {"overall": {"fix_rate_mean": r},
                "by_label": {"palette": {"fix_rate_mean": r}}}
    return {"by_arm": {"em": arm(em), "golden": arm(gold), "null": arm(null)}}


def test_lift_cancels_the_floor():
    lift = normalized_lift(_agg(em=0.8, gold=1.0, null=0.5))
    assert lift["overall"]["lift"] == 0.6          # (0.8-0.5)/(1.0-0.5)
    assert lift["overall"]["discriminative"] is True
    assert lift["by_label"]["palette"]["lift"] == 0.6


def test_lift_flags_no_discriminative_power_when_golden_equals_null():
    """If the placebo clears as often as the golden, the instrument can't tell em from
    placebo on that class — a measured finding (lift None, discriminative False)."""
    lift = normalized_lift(_agg(em=0.9, gold=0.9, null=0.9))
    assert lift["overall"]["lift"] is None
    assert lift["overall"]["discriminative"] is False


def test_lift_is_na_without_all_three_arms():
    agg_two = {"by_arm": {"em": {"overall": {"fix_rate_mean": 0.8}, "by_label": {}},
                          "golden": {"overall": {"fix_rate_mean": 1.0}, "by_label": {}}}}
    assert normalized_lift(agg_two) == {}


# --------------------------------------------------------------------------- #
# Cost estimate accounts for the em-capture
# --------------------------------------------------------------------------- #
def test_estimate_counts_em_capture_once_per_case():
    est = estimate_cost(sample=12, rerolls=3, arms=("em", "golden", "null"), view_count=2)
    assert est["em_capture_calls"] == 12          # one per case, em arm only
    # em re-critiques (3 arms × 12 × 3) + 12 captures
    assert est["em_calls"] == 3 * 12 * 3 + 12
    no_em = estimate_cost(sample=12, rerolls=3, arms=("golden", "null"), view_count=2)
    assert no_em["em_capture_calls"] == 0
    assert est["dollars"] > 0


# --------------------------------------------------------------------------- #
# Live em-capture (stubbed transports — $0)
# --------------------------------------------------------------------------- #
def _stub_transports(monkeypatch, verdict_json):
    async def fake(*, prompt, image_paths, timeout_s=120):
        return _FakeCLIResponse(text=verdict_json)
    async def fake_opus(*, prompt, image_paths, timeout_s=120):
        return _FakeSDKResponse(text=verdict_json)
    monkeypatch.setattr("pipeline.agents.vision_critic.run_antigravity_with_image", fake)
    monkeypatch.setattr("pipeline.agents.vision_critic.run_gemini_api_with_image", fake)
    monkeypatch.setattr("pipeline.agents.vision_critic.invoke_opus_vision", fake_opus)


def test_capture_em_value_returns_proposed_clause(monkeypatch):
    case = _case("palette")
    _stub_transports(monkeypatch, make_vision_verdict(verdict="fail", cites=case["expected_cites"]))
    manifest = eval_manifest()
    val = _capture_em_value(case, manifest=manifest, criteria=merged_criteria(manifest))
    assert isinstance(val, str) and val.strip()   # the stub's patch value


def test_capture_em_value_none_when_no_patch(monkeypatch):
    case = _case("palette")
    # a pass verdict carries no diff → capture returns None (em arm skips, not a 0)
    _stub_transports(monkeypatch, make_vision_verdict(verdict="pass"))
    manifest = eval_manifest()
    assert _capture_em_value(case, manifest=manifest, criteria=merged_criteria(manifest)) is None
