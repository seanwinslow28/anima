"""Tests for pipeline.agents.cost_estimator — the CostEstimatorNode AgentSpec."""

from __future__ import annotations

import json
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


# ---------------------------------------------------------------------------
# Phase 2 — Cy Bible authoring spend (Task 1.6)
# ---------------------------------------------------------------------------


def _write_plate_plan(folder: Path, plates: list[dict]) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "plate_generation_plan.json").write_text(
        json.dumps({"plates": plates}), encoding="utf-8"
    )


def test_phase_2_cost_zero_when_no_characters(tmp_path):
    """Maya-only runs (animation_piece, no Bibles being authored) report Phase 2 == $0."""
    cls = NODE_REGISTRY["cost_estimator"]
    manifest = {
        "generation": {"routing": {}},
        "phases": {"phase_5": {}, "phase_6": {}},
        # No characters: block — animation piece against already-shipped Bibles.
    }
    estimate = cls().run(_ctx(tmp_path, manifest)).outputs["estimate"]
    assert estimate.by_phase["phase_2"]["low_usd"] == 0.0
    assert estimate.by_phase["phase_2"]["median_usd"] == 0.0
    assert estimate.by_phase["phase_2"]["high_usd"] == 0.0


def test_phase_2_cost_sums_nb_pro_per_plate(tmp_path):
    """Manifest with two characters, 20 + 10 generate plates planned, returns the expected total."""
    sean_dir = tmp_path / "characters" / "sean-anchor"
    mascot_dir = tmp_path / "characters" / "claude-mascot"
    _write_plate_plan(
        sean_dir,
        [{"target_path": f"p{i}.png", "source": "generate"} for i in range(20)],
    )
    _write_plate_plan(
        mascot_dir,
        [{"target_path": f"p{i}.png", "source": "generate"} for i in range(10)],
    )

    manifest = {
        "characters": {
            "sean-anchor": {"folder": str(sean_dir), "style_register": "pencil-test-colored"},
            "claude-mascot": {"folder": str(mascot_dir), "style_register": "pixel-art-8bit"},
        },
        "phases": {"phase_5": {}, "phase_6": {}},
    }
    cls = NODE_REGISTRY["cost_estimator"]
    estimate = cls().run(_ctx(tmp_path, manifest)).outputs["estimate"]
    # 30 generate plates × $0.15 = $4.50 low.
    assert estimate.by_phase["phase_2"]["low_usd"] == 4.50
    # High = 3× retry budget per plate.
    assert estimate.by_phase["phase_2"]["high_usd"] == round(30 * 0.15 * 3, 2)
    # Median sits between low and high.
    p2 = estimate.by_phase["phase_2"]
    assert p2["low_usd"] < p2["median_usd"] < p2["high_usd"]


def test_phase_2_cost_excludes_ingest_only_plates(tmp_path):
    """A plate plan with all `source: 'ingest:...'` returns $0 for that character."""
    char_dir = tmp_path / "characters" / "all-ingested"
    _write_plate_plan(
        char_dir,
        [
            {"target_path": "turnarounds/body-front.png", "source": "ingest:source-refs/x.png"},
            {"target_path": "expressions/neutral.png", "source": "ingest:source-refs/y.png"},
        ],
    )
    manifest = {
        "characters": {
            "all-ingested": {"folder": str(char_dir), "style_register": "pencil-test-colored"},
        },
        "phases": {},
    }
    cls = NODE_REGISTRY["cost_estimator"]
    estimate = cls().run(_ctx(tmp_path, manifest)).outputs["estimate"]
    assert estimate.by_phase["phase_2"]["low_usd"] == 0.0
    assert estimate.by_phase["phase_2"]["high_usd"] == 0.0


def test_phase_2_cost_missing_plate_plan_treated_as_zero(tmp_path):
    """Bible not yet authored (no plate_generation_plan.json) → Phase 2 is $0."""
    char_dir = tmp_path / "characters" / "not-yet-authored"
    char_dir.mkdir(parents=True)
    manifest = {
        "characters": {
            "not-yet-authored": {"folder": str(char_dir), "style_register": "watercolor"},
        },
        "phases": {},
    }
    cls = NODE_REGISTRY["cost_estimator"]
    estimate = cls().run(_ctx(tmp_path, manifest)).outputs["estimate"]
    assert estimate.by_phase["phase_2"]["low_usd"] == 0.0
