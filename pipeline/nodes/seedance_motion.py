"""Phase 6 Seedance motion node — shells to pipeline/seedance_generate.py.

Per the commit-4 plan (Q2 answered), the node delegates to the legacy CLI
to keep behavior byte-identical with the in-flight Act 2 work. Lifting
_submit_one to a public callable is deferred to commit 5.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from pipeline.agents import (
    AgentContext,
    AgentResult,
    CostEstimate,
    register_node,
)


@register_node("seedance_motion")
class SeedanceMotionNode:
    name = "seedance_motion"
    inputs: dict = {
        "shot_id": str,
        "start_frame_path": str,
        "end_frame_path": str,
        "prompt": str,
        "duration_s": int,
    }
    outputs: dict = {
        "mp4_path": str,
    }
    cites_criteria: list[str] = []

    def cost_estimate(self, ctx: AgentContext) -> CostEstimate:
        # Fast tier 720p ~ $0.24/sec; pencil-test default duration ~4-5s.
        # Pro tier escalates to ~$1/sec; commit 5 wires the auto-escalation.
        sec = float(ctx.inputs.get("duration_s", 4))
        rate = 0.24 if ctx.tier == "draft" else 1.00
        return CostEstimate(usd=rate * sec, latency_s=120.0, confidence=0.7)

    def run(self, ctx: AgentContext) -> AgentResult:
        shot_id = str(ctx.inputs["shot_id"])
        cmd = [
            sys.executable, "pipeline/seedance_generate.py",
            "--mode", "sync",
            "--clip-id", shot_id,
            "--run-dir", str(ctx.run_dir),
            "--tier", ctx.tier,
        ]
        subprocess.run(cmd, check=True)
        mp4 = ctx.run_dir / "seedance" / f"{shot_id}.mp4"
        return AgentResult(
            outputs={"mp4_path": str(mp4)},
            tier=ctx.tier,
            notes=f"Seedance {ctx.tier} tier submitted via legacy CLI",
        )
