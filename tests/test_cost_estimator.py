"""Tests for pipeline.agents.cost_estimator — the CostEstimatorNode AgentSpec."""

from __future__ import annotations

from pathlib import Path

from pipeline.agents import (
    AgentContext,
    AgentResult,
    AgentSpec,
    NODE_REGISTRY,
)

# Trigger @register_node("cost_estimator") side-effect:
import pipeline.agents.cost_estimator  # noqa: F401
from pipeline.agents.cost_estimator import RunCostEstimate


def _ctx(tmp_path: Path, manifest: dict) -> AgentContext:
    return AgentContext(
        run_dir=tmp_path,
        inputs={"manifest": manifest},
        manifest=manifest,
        criteria=None,
        tier="draft",
        cache_dir=tmp_path / ".cache",
    )


def test_cost_estimator_registered_and_satisfies_agentspec():
    cls = NODE_REGISTRY["cost_estimator"]
    assert isinstance(cls(), AgentSpec)


def test_emits_run_cost_estimate_shape(tmp_path):
    cls = NODE_REGISTRY["cost_estimator"]
    manifest = {
        "generation": {
            "routing": {
                "hero_keyframe": {"model": "nb-pro", "usd_per_frame": 0.15},
                "standard_keyframe": {"model": "nb2", "usd_per_frame": 0.07},
            }
        },
        "tiering": {"phase_5": "draft", "phase_6": "draft"},
        "phases": {
            "phase_5": {"frame_count_hero": 2, "frame_count_standard": 6},
            "phase_6": {"clip_count": 4, "seconds_per_clip": 5},
        },
    }
    result = cls().run(_ctx(tmp_path, manifest))
    assert isinstance(result, AgentResult)
    estimate = result.outputs["estimate"]
    assert isinstance(estimate, RunCostEstimate)
    assert estimate.low_usd >= 0
    assert estimate.median_usd >= estimate.low_usd
    assert estimate.high_usd >= estimate.median_usd
    assert "phase_5" in estimate.by_phase
    assert "phase_6" in estimate.by_phase
    assert estimate.draft_total_usd == estimate.low_usd
    assert estimate.pro_total_usd == estimate.high_usd


def test_subscription_absorbed_phases_are_zero(tmp_path):
    """Agent fleet runtime is $0 incremental — Maya/Cy/Sage etc. don't add cost."""
    cls = NODE_REGISTRY["cost_estimator"]
    manifest = {
        "generation": {"routing": {}},
        "tiering": {},
        "phases": {"phase_0": {}, "phase_2": {}, "phase_3": {}, "phase_7": {}},
    }
    result = cls().run(_ctx(tmp_path, manifest))
    estimate = result.outputs["estimate"]
    for phase_id in ("phase_0", "phase_2", "phase_3", "phase_7"):
        assert estimate.by_phase[phase_id]["low_usd"] == 0
        assert estimate.by_phase[phase_id]["median_usd"] == 0
        assert estimate.by_phase[phase_id]["high_usd"] == 0


def test_phase_5_uses_routing_table_prices(tmp_path):
    """Per Flo's routing block — hero/standard split drives Phase 5 cost."""
    cls = NODE_REGISTRY["cost_estimator"]
    manifest = {
        "generation": {
            "routing": {
                "hero_keyframe": {"usd_per_frame": 0.20},      # custom hero price
                "standard_keyframe": {"usd_per_frame": 0.05},  # custom standard price
            }
        },
        "phases": {"phase_5": {"frame_count_hero": 4, "frame_count_standard": 10}},
    }
    estimate = cls().run(_ctx(tmp_path, manifest)).outputs["estimate"]
    p5 = estimate.by_phase["phase_5"]
    # Low band: all standard-price (draft, single attempt). 14 frames × $0.05 = $0.70.
    assert p5["low_usd"] == 0.70
    # High band: 14 frames × $0.20 hero price × 3 attempts = $8.40.
    assert p5["high_usd"] == 8.40


def test_phase_6_seedance_fast_to_pro_split(tmp_path):
    """Phase 6 uses Seedance Fast → Pro escalation rate."""
    cls = NODE_REGISTRY["cost_estimator"]
    manifest = {
        "generation": {"routing": {}},
        "phases": {"phase_6": {"clip_count": 10, "seconds_per_clip": 5}},
    }
    estimate = cls().run(_ctx(tmp_path, manifest)).outputs["estimate"]
    p6 = estimate.by_phase["phase_6"]
    # Low: 10 clips × 5s × $0.24/s = $12.00 (Fast throughout).
    assert p6["low_usd"] == 12.00
    # High: 10 × 5 × $0.50/s = $25.00 (Pro throughout).
    assert p6["high_usd"] == 25.00
    # Median: between the two.
    assert p6["low_usd"] < p6["median_usd"] < p6["high_usd"]


def test_empty_manifest_returns_zero_cost(tmp_path):
    """Defensive: an empty manifest doesn't crash; everything is zero."""
    cls = NODE_REGISTRY["cost_estimator"]
    estimate = cls().run(_ctx(tmp_path, {})).outputs["estimate"]
    assert estimate.low_usd == 0
    assert estimate.median_usd == 0
    assert estimate.high_usd == 0
