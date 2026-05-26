"""Phase 5 frame generation — wraps pipeline/generate.py.

Reads a prompt + reference list, shells to the existing generate_image.py
via the legacy module's generate_frame() helper. No inner-logic changes;
this is the contract layer the DAG runner expects.
"""

from __future__ import annotations

from pipeline.agents import (
    AgentContext,
    AgentResult,
    CostEstimate,
    register_node,
)
from pipeline.generate import generate_frame


@register_node("frame_generate")
class FrameGenerateNode:
    name = "frame_generate"
    inputs: dict = {
        "frame_num": int,
        "prompt": str,
        "references": list,
    }
    outputs: dict = {
        "candidate_path": str,
    }
    cites_criteria: list[str] = []  # T1 rule-gate cites criteria, not generator

    def cost_estimate(self, ctx: AgentContext) -> CostEstimate:
        # NB2 keyframe ~ $0.067 per call (per Image-Model-DR-2026 SYNTHESIS).
        # Latency varies widely; 15s is a reasonable median.
        return CostEstimate(usd=0.067, latency_s=15.0, confidence=0.6)

    def run(self, ctx: AgentContext) -> AgentResult:
        frame_num = int(ctx.inputs["frame_num"])
        prompt = str(ctx.inputs["prompt"])
        references = [str(r) for r in ctx.inputs.get("references", [])]
        candidate = generate_frame(
            frame_num=frame_num,
            prompt=prompt,
            references=references,
            manifest=ctx.manifest,
            run_dir=ctx.run_dir,
        )
        if candidate is None:
            raise RuntimeError(
                f"frame_generate F{frame_num:02d} returned no candidate"
            )
        return AgentResult(
            outputs={"candidate_path": str(candidate)},
            tier=ctx.tier,
            notes=f"F{frame_num:02d} generated via legacy generate_frame()",
        )
