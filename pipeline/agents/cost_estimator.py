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

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from pipeline.agents import (
    AgentContext,
    AgentResult,
    CostEstimate,
    register_node,
)

# Subscription-absorbed via Sean's Anthropic Pro + OpenAI Plus + Google
# personal OAuth tiers (v2 brainstorm §7). Phases whose only compute is
# agent-fleet runtime cost $0 incremental. Phase 2 is NOT in this set as of
# commit 2 / Task 1.6 — Cy's NB Pro plate generation is real variable spend
# (~$0.15 per generate plate); _phase_2_cost(manifest) prices it from each
# character's plate_generation_plan.json on disk.
SUBSCRIPTION_ABSORBED_PHASES = frozenset({
    "phase_0",   # Maya planning
    "phase_1",   # Scaffold (no compute)
    "phase_3",   # Sam + Bea storyboard
    "phase_7",   # Audit consolidation (no model calls)
    "phase_9",   # Human QA review
})

# Phase 2 NB Pro plate price (Image-Model-DR SYNTHESIS §2 hero tier).
# Authoritative cost source: Cy's plate_generation_plan.json files on disk
# under each character folder. Ingested plates contribute $0.
_NB_PRO_USD_PER_PLATE = 0.15
# Per-plate three-attempt ceiling drives the high band: every generate plate
# may regenerate twice before surfacing to the human gate.
_PHASE_2_HIGH_MULTIPLIER = 3.0
# Median band assumption: ~30% of plates trigger a single regeneration on
# Gemini-flagged Pass 3 verdicts. Tighten via the eval suite's bake-off data
# (commit 2b's failure-modes.md baseline) once 2+ real Bibles exist.
_PHASE_2_MEDIAN_MULTIPLIER = 1.30

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

        by_phase["phase_2"] = self._phase_2_cost(manifest)
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

    def _phase_2_cost(self, manifest: dict) -> dict[str, float]:
        """Phase 2 Cy Bible authoring spend.

        Reads each registered character's plate_generation_plan.json (if
        present on disk) and prices every `generate` plate at NB Pro's
        per-plate rate. Ingested plates contribute $0 (the pixel comes from
        Sean's source-refs, not from a generation call).

        When the manifest has no `characters:` block or the block is empty,
        Phase 2 spend is $0 — animation-piece runs against already-authored
        Bibles don't re-pay NB Pro to load the Bible. When the registry has
        characters but their plate plans don't yet exist on disk (Bible
        hasn't been authored yet), spend is also $0 — surfaces the unknown
        as zero rather than guessing a budget envelope.
        """
        chars = manifest.get("characters")
        if not chars or not isinstance(chars, dict):
            return {"low_usd": 0.0, "median_usd": 0.0, "high_usd": 0.0}

        total_generate_plates = 0
        for cfg in chars.values():
            folder_str = (cfg or {}).get("folder") if isinstance(cfg, dict) else None
            if not folder_str:
                continue
            plan_path = Path(folder_str) / "plate_generation_plan.json"
            if not plan_path.exists():
                continue
            try:
                plan = json.loads(plan_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            for plate in plan.get("plates", []):
                source = str(plate.get("source", "generate"))
                if not source.startswith("ingest:"):
                    total_generate_plates += 1

        base = total_generate_plates * _NB_PRO_USD_PER_PLATE
        return {
            "low_usd": round(base, 2),
            "median_usd": round(base * _PHASE_2_MEDIAN_MULTIPLIER, 2),
            "high_usd": round(base * _PHASE_2_HIGH_MULTIPLIER, 2),
        }

    def _phase_5_cost(self, manifest: dict) -> dict[str, float]:
        """Phase 5 keyframe generation. Sums the FULL generation.routing: table.

        Wired keyframe routes (hero/standard) keep the escalation-ladder math.
        Declared/deferred routes (the Flo in-between + mask-edit seams) price at
        their config estimate with a widened band, and any budgeted not-wired
        route lowers the phase confidence flag — their real cost is unproven
        until Flo-B measures it.
        """
        routing = (manifest.get("generation") or {}).get("routing") or {}
        phase_5 = (manifest.get("phases") or {}).get("phase_5") or {}
        hero_count = int(phase_5.get("frame_count_hero", 0))
        standard_count = int(phase_5.get("frame_count_standard", 0))
        hero_price = float((routing.get("hero_keyframe") or {}).get("usd_per_frame", 0.15))
        standard_price = float((routing.get("standard_keyframe") or {}).get("usd_per_frame", 0.07))

        # Wired keyframe routes — existing escalation-ladder math (preserved).
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

        # Declared/deferred routes — the in-between + mask-edit seams. Not wired
        # this session, so there's no measured retry behavior: price the low band
        # at a single attempt and widen the high band to the same 3× retry ceiling
        # the wired routes carry. Any budgeted declared route lowers confidence.
        confidence = "full"
        for shot_type in ("in_between_cheap", "in_between_mid", "mask_edit"):
            count = int(phase_5.get(f"frame_count_{shot_type}", 0))
            if count == 0:
                continue
            price = float((routing.get(shot_type) or {}).get("usd_per_frame", 0.0))
            confidence = "lowered"
            low += count * price
            median += count * price * 1.5
            high += count * price * 3

        return {
            "low_usd": round(low, 2),
            "median_usd": round(median, 2),
            "high_usd": round(high, 2),
            "confidence": confidence,
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
