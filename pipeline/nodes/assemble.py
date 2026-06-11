"""Phase 8 assembly — wraps pipeline/assemble.sh.

Shells to the FFmpeg recipe. Output is the export/ directory contents
(GIF + WebM + MP4). Byte-identical to direct invocation; that's the
verification step §Verification depends on.

Optional `slug` / `sequence_file` inputs (#13) thread a per-piece sequence
spec + output slug to the assembler so Slice 2's orchestrator can drive an
arbitrary piece; absent → the legacy PT_A1 default (byte-identical).
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from pipeline.agents import (
    AgentContext,
    AgentResult,
    CostEstimate,
    register_node,
)


@register_node("assemble")
class AssembleNode:
    name = "assemble"
    inputs: dict = {
        "run_dir": str,
        # Optional (#13): per-piece sequence spec + output slug. Absent → the
        # assembler's embedded PT_A1 default (byte-identical legacy behavior).
        "slug": str,
        "sequence_file": str,
    }
    outputs: dict = {
        "gif_path": str,
        "webm_path": str,
        "mp4_path": str,
    }
    cites_criteria: list[str] = []

    def cost_estimate(self, ctx: AgentContext) -> CostEstimate:
        return CostEstimate(usd=0.0, latency_s=30.0, confidence=0.95)

    def run(self, ctx: AgentContext) -> AgentResult:
        run_dir = Path(str(ctx.inputs["run_dir"]))
        cmd = ["bash", "pipeline/assemble.sh", str(run_dir)]
        slug = ctx.inputs.get("slug")
        if slug:
            cmd += ["--slug", str(slug)]
        sequence_file = ctx.inputs.get("sequence_file")
        if sequence_file:
            cmd += ["--sequence-file", str(sequence_file)]
        subprocess.run(cmd, check=True)
        export = run_dir / "export"
        gif = next(export.glob("*.gif"), None)
        webm = next(export.glob("*.webm"), None)
        mp4 = next(export.glob("*.mp4"), None)
        return AgentResult(
            outputs={
                "gif_path": str(gif) if gif else "",
                "webm_path": str(webm) if webm else "",
                "mp4_path": str(mp4) if mp4 else "",
            },
            tier=ctx.tier,
            notes="Assembled via legacy assemble.sh",
        )
