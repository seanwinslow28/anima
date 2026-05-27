"""anima — CostEstimatorNode. Run-level cost preview.

Maya calls this during Phase 0 to surface a draft-vs-pro cost preview to Sean.
Commit 5's tier-escalation runtime will call it again at each tier decision.
The museum writer in commit 6 will call it during walkthrough rendering.
One node, three consumers, one source of truth for spend.

Per v2 brainstorm TOP-3 (cost estimator as its own AgentSpec, not Maya-internal
logic): separation of concerns at the protocol layer. Maya's prompt stays
focused on planning rationale; the estimator stays focused on arithmetic.

The estimator reads two manifest blocks:
  - generation.routing: per-shot-tier prices (NB Pro $0.15/frame, NB2 $0.07,
    Seedream $0.007–0.03, etc. — populated per the Flo router spec at v2 §4)
  - tiering: per-phase draft|pro defaults
And one optional input — historical-runs corpus — for tightening the median
band over time. The commit-3 baseline is conservative: no historical data,
explicit low/median/high bands per phase.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

from pipeline.agents import (
    AgentContext,
    AgentResult,
    CostEstimate,
    register_node,
)

# Subscription-absorbed via Sean's Anthropic Pro + OpenAI Plus + Google
# personal OAuth tiers (v2 brainstorm §7). Phases whose only compute is
# agent-fleet runtime cost $0 incremental.
SUBSCRIPTION_ABSORBED_PHASES = frozenset({
    "phase_0",   # Maya planning
    "phase_1",   # Scaffold (no compute)
    "phase_2",   # Cy Bible authoring (Opus + NB Pro generation priced under phase_5)
    "phase_3",   # Sam + Bea storyboard
    "phase_7",   # Audit consolidation (no model calls)
    "phase_9",   # Human QA review
})

# Phase 6 Seedance prices per the existing Fast→Pro contract.
_SEEDANCE_FAST_USD_PER_S = 0.24
_SEEDANCE_PRO_USD_PER_S = 0.50
# Phase 6 escalation-rate assumption for the median band — ~30% of clips
# escalate from Fast to Pro at the T2 critic gate. Tighten via historical
# corpus once 3+ real runs exist (commit 3b deferred item ENG4).
_PHASE_6_ESCALATION_RATE = 0.30


@dataclass(frozen=True)
class RunCostEstimate:
    """Aggregate cost preview across one run.

    low_usd: draft tier throughout, optimistic pass-rate assumption.
    median_usd: draft → pro escalation at expected pass rate.
    high_usd: worst case — every frame escalates to pro tier with retries.
    by_phase: per-phase breakdown of {low_usd, median_usd, high_usd}.
    draft_total_usd: sum across phases if everything stays at draft.
    pro_total_usd: sum across phases if everything escalates to pro.
    """
    low_usd: float
    median_usd: float
    high_usd: float
    by_phase: dict[str, dict[str, float]] = field(default_factory=dict)
    draft_total_usd: float = 0.0
    pro_total_usd: float = 0.0


@register_node("cost_estimator")
class CostEstimatorNode:
    """Reads manifest generation.routing + tiering blocks; emits RunCostEstimate.

    Three consumers per the brainstorm TOP-3: Maya at Phase 0, the DAG runner
    at each tier-escalation decision (commit 5), Mo the museum writer when
    narrating the run (commit 6). The estimator is the single source of truth
    for spend across all three; do not duplicate pricing logic elsewhere.
    """

    name: ClassVar[str] = "cost_estimator"
    inputs: ClassVar[dict[str, type]] = {"manifest": dict}
    outputs: ClassVar[dict[str, type]] = {"estimate": RunCostEstimate}
    cites_criteria: ClassVar[list[str]] = []

    def cost_estimate(self, ctx: AgentContext) -> CostEstimate:
        # The estimator itself is essentially free — pure Python arithmetic.
        return CostEstimate(usd=0.0, latency_s=0.5, confidence=1.0)

    def run(self, ctx: AgentContext) -> AgentResult:
        manifest = ctx.inputs.get("manifest") or ctx.manifest
        phases = manifest.get("phases") or {}
        by_phase: dict[str, dict[str, float]] = {}

        for phase_id in phases:
            if phase_id in SUBSCRIPTION_ABSORBED_PHASES:
                by_phase[phase_id] = {"low_usd": 0.0, "median_usd": 0.0, "high_usd": 0.0}

        by_phase["phase_5"] = self._phase_5_cost(manifest)
        by_phase["phase_6"] = self._phase_6_cost(manifest)
        by_phase["phase_8"] = {"low_usd": 0.0, "median_usd": 0.0, "high_usd": 0.0}

        low = sum(p["low_usd"] for p in by_phase.values())
        median = sum(p["median_usd"] for p in by_phase.values())
        high = sum(p["high_usd"] for p in by_phase.values())

        estimate = RunCostEstimate(
            low_usd=round(low, 2),
            median_usd=round(median, 2),
            high_usd=round(high, 2),
            by_phase=by_phase,
            draft_total_usd=round(low, 2),
            pro_total_usd=round(high, 2),
        )
        return AgentResult(
            outputs={"estimate": estimate},
            tier=ctx.tier,
            notes=f"cost_estimator phases={sorted(by_phase)} low=${low:.2f} high=${high:.2f}",
        )

    def _phase_5_cost(self, manifest: dict) -> dict[str, float]:
        """Phase 5 keyframe generation. Reads generation.routing: per Flo."""
        routing = (manifest.get("generation") or {}).get("routing") or {}
        phase_5 = (manifest.get("phases") or {}).get("phase_5") or {}
        hero_count = int(phase_5.get("frame_count_hero", 0))
        standard_count = int(phase_5.get("frame_count_standard", 0))
        hero_price = float((routing.get("hero_keyframe") or {}).get("usd_per_frame", 0.15))
        standard_price = float((routing.get("standard_keyframe") or {}).get("usd_per_frame", 0.07))

        # Low: draft throughout, single attempt, no escalation.
        low = standard_count * standard_price + hero_count * standard_price
        # High: pro throughout, 3 attempts per frame (retry budget).
        high = (hero_count + standard_count) * hero_price * 3
        # Median: hero frames always at hero tier (1 attempt); standard frames
        # split — half escalate (2 attempts at hero price), half don't.
        median = (
            hero_count * hero_price
            + standard_count * (0.5 * hero_price * 2 + 0.5 * standard_price)
        )
        return {
            "low_usd": round(low, 2),
            "median_usd": round(median, 2),
            "high_usd": round(high, 2),
        }

    def _phase_6_cost(self, manifest: dict) -> dict[str, float]:
        """Phase 6 Seedance motion. Fast tier default, Pro for hero clips."""
        phase_6 = (manifest.get("phases") or {}).get("phase_6") or {}
        clips = int(phase_6.get("clip_count", 0))
        secs = float(phase_6.get("seconds_per_clip", 5))

        low = clips * secs * _SEEDANCE_FAST_USD_PER_S
        high = clips * secs * _SEEDANCE_PRO_USD_PER_S
        # Median: (1 - escalation_rate) at Fast price + escalation_rate at Pro.
        median = clips * secs * (
            (1 - _PHASE_6_ESCALATION_RATE) * _SEEDANCE_FAST_USD_PER_S
            + _PHASE_6_ESCALATION_RATE * _SEEDANCE_PRO_USD_PER_S
        )
        return {
            "low_usd": round(low, 2),
            "median_usd": round(median, 2),
            "high_usd": round(high, 2),
        }
