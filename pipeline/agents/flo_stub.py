"""Flo's offline stand-in — the --stub image placeholder (Slice 2.1 Fix A).

A real 1376x768 PNG, $0, no key: the audit gate PIL-opens candidates uncaught,
and Em's no-key stub critiques whatever bytes exist. Bytes vary per attempt so
a re-roll yields fresh content (and fresh Em cache keys) — mirrors
tests/orch_fixtures.fake_flo_generate. Dispatched by generate_stage.run_frame_fan
when state["stub"] is set; the real `flo` node is untouched.
"""

from __future__ import annotations

from PIL import Image

from pipeline import generate as _legacy_generate
from pipeline.agents import AgentContext, AgentResult, CostEstimate, register_node


@register_node("flo_stub")
class FloStubNode:
    """Offline Phase-5 placeholder generator for --stub runs."""

    name = "flo_stub"
    inputs: dict = {"frame_num": int, "prompt": str, "references": list}
    outputs: dict = {"candidate_path": str}
    cites_criteria: list[str] = []

    def cost_estimate(self, ctx: AgentContext) -> CostEstimate:
        return CostEstimate(usd=0.0, latency_s=0.1, confidence=1.0)

    def run(self, ctx: AgentContext) -> AgentResult:
        frame_num = int(ctx.inputs["frame_num"])
        candidates_dir = ctx.run_dir / "candidates" / f"F{frame_num:02d}"
        candidates_dir.mkdir(parents=True, exist_ok=True)
        attempt = _legacy_generate.get_attempt_number(candidates_dir)
        out = candidates_dir / f"attempt_{attempt:02d}.png"
        Image.new(
            "RGB", (1376, 768), (200 - attempt * 3, 180, 100 + frame_num % 100)
        ).save(out, format="PNG")
        return AgentResult(
            outputs={"candidate_path": str(out)},
            tier=ctx.tier,
            notes=f"F{frame_num:02d} STUB placeholder (offline --stub run, $0)",
        )
