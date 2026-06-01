# evals/vision_critic/bakeoff_lib.py
"""Shared bake-off logic: route a case through one critic config, score it.

Reuses Em's exact _build_prompt + _parse so the ONLY variable across configs
is the model. No escalation — each base model is scored alone.
"""
from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from pathlib import Path

from pipeline.agents import AgentContext
from pipeline.agents.vision_critic import VisionCriticNode
from pipeline.agents.cli_runners import run_antigravity_with_image
from pipeline.agents.sdk_runners import invoke_sonnet_vision, invoke_opus_vision
from evals.vision_critic.scoring import CaseScore

_RUNNERS = {
    "antigravity": run_antigravity_with_image,
    "sonnet_vision": invoke_sonnet_vision,
    "opus_vision": invoke_opus_vision,
}


def resolve_runner(name: str):
    return _RUNNERS[name]


async def score_config_async(*, variant: dict, cases: list[dict], fixtures: Path,
                             manifest: dict) -> list[CaseScore]:
    """Run every case through one config's runner, scored with Em's parser (concurrently)."""
    node = VisionCriticNode()
    runner = resolve_runner(variant["runner"])
    sem = asyncio.Semaphore(5)  # limit concurrency to avoid rate limits

    async def score_one(case: dict) -> CaseScore:
        async with sem:
            ctx = AgentContext(
                run_dir=Path("/tmp/t2-bakeoff"),
                inputs={
                    "image_path": str(fixtures / case["input"]),
                    "beat_description": case["beat_description"],
                    "frame_id": case["name"],
                    "impact_tags": case.get("impact_tags", []),
                    "checkpoint": case["checkpoint"],
                },
                manifest=manifest, criteria=None, tier="draft",
                cache_dir=Path("/tmp/t2-bakeoff/.cache"),
            )
            prompt = node._build_prompt(ctx, node._t2_config(ctx))
            img = Path(ctx.inputs["image_path"])
            start = datetime.now(timezone.utc)
            resp = await runner(prompt=prompt, image_paths=[img], timeout_s=120)
            wall = (datetime.now(timezone.utc) - start).total_seconds()
            parsed = node._parse(resp.text, default_verdict="borderline")
            return CaseScore(
                name=case["name"], case_class=case["case_class"],
                expected_verdict=case["expected_verdict"],
                predicted_verdict=parsed["verdict"],
                expected_cites=case.get("expected_cites", []),
                actual_cites=list(parsed.get("cites_criteria", [])),
                confidence=parsed["confidence"], wall_s=wall,
            )

    tasks = [score_one(c) for c in cases]
    return await asyncio.gather(*tasks)


def score_config(*, variant: dict, cases: list[dict], fixtures: Path,
                 manifest: dict) -> list[CaseScore]:
    """Run every case through one config's runner, scored with Em's parser."""
    return asyncio.run(score_config_async(variant=variant, cases=cases, fixtures=fixtures, manifest=manifest))
