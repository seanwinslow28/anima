"""Phase 5 T1 audit gate — wraps pipeline/audit.py.

Runs the automated HF01 aspect-ratio check via PIL. The vision-review
checks (HF02-HF05, SF01-SF05) are deferred to Em (commit 8); this node
emits the structured review prompt the Em agent will consume.
"""

from __future__ import annotations

from pathlib import Path

from pipeline.agents import (
    AgentContext,
    AgentResult,
    CostEstimate,
    register_node,
)
from pipeline.audit import check_aspect_ratio, get_vision_review_prompt


@register_node("audit_gate")
class AuditGateNode:
    name = "audit_gate"
    inputs: dict = {
        "candidate_path": str,
        "frame_num": int,
        "pose_description": str,
    }
    outputs: dict = {
        "verdict": str,
        "fail_codes": list,
        "vision_review_prompt": str,
    }
    cites_criteria: list[str] = []  # T1 deterministic gate

    def cost_estimate(self, ctx: AgentContext) -> CostEstimate:
        return CostEstimate(usd=0.0, latency_s=0.1, confidence=0.99)

    def run(self, ctx: AgentContext) -> AgentResult:
        candidate = Path(ctx.inputs["candidate_path"])
        hf01 = check_aspect_ratio(candidate)
        if hf01["result"] == "HARD_FAIL":
            return AgentResult(
                outputs={
                    "verdict": "hard_fail",
                    "fail_codes": ["HF01"],
                    "vision_review_prompt": "",
                },
                tier=ctx.tier,
                notes=f"HF01 hard fail: {hf01.get('dimensions', 'unknown')}",
            )
        anchor_path = ctx.manifest.get("anchor", {}).get("path", "")
        prompt = get_vision_review_prompt(
            frame_num=int(ctx.inputs["frame_num"]),
            pose_description=str(ctx.inputs["pose_description"]),
            anchor_path=anchor_path,
        )
        return AgentResult(
            outputs={
                "verdict": "needs_vision_review",
                "fail_codes": [],
                "vision_review_prompt": prompt,
            },
            tier=ctx.tier,
            notes="HF01 passed; vision review prompt emitted for Em (commit 8).",
        )
