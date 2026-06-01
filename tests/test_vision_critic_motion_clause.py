"""Em's prompt must be honest about what a contact sheet can and cannot show."""
from __future__ import annotations

from pathlib import Path

from pipeline.agents import AgentContext
from pipeline.agents.vision_critic import VisionCriticNode


def _ctx(checkpoint: str) -> AgentContext:
    return AgentContext(
        run_dir=Path("/tmp/x"),
        inputs={
            "image_path": "/tmp/x.png",
            "beat_description": "Sean walks left to right.",
            "frame_id": "W1",
            "impact_tags": [],
            "checkpoint": checkpoint,
        },
        manifest={"critics": {"t2": {}}},
        criteria=None,
        tier="draft",
        cache_dir=Path("/tmp/x/.cache"),
    )


def test_motion_clause_present_for_phase_6():
    node = VisionCriticNode()
    prompt = node._build_prompt(_ctx("phase_6_motion"), {})
    low = prompt.lower()
    assert "contact sheet" in low
    assert "cannot" in low  # the explicit can't-see instruction
    # Names at least one motion-proper artifact it must defer on.
    assert any(t in low for t in ("jitter", "flicker", "texture-crawl", "smoothness"))


def test_motion_clause_absent_for_phase_5():
    node = VisionCriticNode()
    prompt = node._build_prompt(_ctx("phase_5_generate"), {})
    assert "contact sheet" not in prompt.lower()
