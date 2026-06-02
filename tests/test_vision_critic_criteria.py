# tests/test_vision_critic_criteria.py
"""Em surfaces the character's IR.*/AC.* rules from ctx.criteria so she can cite
them. Graceful when the bundle is None (legacy) or the phase intersection is empty."""
from __future__ import annotations

import json
from pathlib import Path

from pipeline.agents import AgentContext
from pipeline.agents.vision_critic import VisionCriticNode
from pipeline.criteria import load_criteria


def _bundle(tmp_path: Path, cites_phase: list[int]):
    """Write + load a minimal v1.2 bundle with two IR.sean.* rules."""
    data = {
        "version": "1.2", "locked": False,
        "criteria": [
            {"id": "IR.sean.face.jaw-line-angular-not-rounded",
             "description": "Jaw carries a defined angle at the mandibular corner.",
             "cites_phase": cites_phase, "cites_personas": ["em"],
             "impact_tag": "identity_critical", "character_id": "sean"},
            {"id": "IR.sean.prop.stylus-right-hand-always",
             "description": "Stylus stays in the right hand in every frame.",
             "cites_phase": cites_phase, "cites_personas": ["em"],
             "impact_tag": "identity_critical", "character_id": "sean"},
        ],
    }
    p = tmp_path / "ac.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return load_criteria(p)


def _ctx(criteria, *, checkpoint="phase_5_generate", character_id="sean"):
    return AgentContext(
        run_dir=Path("/tmp/x"),
        inputs={"image_path": "/tmp/x.png", "beat_description": "b", "frame_id": "F",
                "impact_tags": [], "checkpoint": checkpoint, "character_id": character_id},
        manifest={"critics": {"t2": {}}}, criteria=criteria, tier="draft",
        cache_dir=Path("/tmp/x/.cache"),
    )


def test_surfaces_phase5_ir_rules(tmp_path):
    prompt = VisionCriticNode()._build_prompt(_ctx(_bundle(tmp_path, [5, 6])), {})
    assert "Character Bible rules" in prompt
    assert "IR.sean.face.jaw-line-angular-not-rounded" in prompt
    assert "IR.sean.prop.stylus-right-hand-always" in prompt


def test_no_block_when_bundle_none():
    prompt = VisionCriticNode()._build_prompt(_ctx(None), {})
    assert "Character Bible rules" not in prompt


def test_no_block_when_character_id_absent(tmp_path):
    ctx = _ctx(_bundle(tmp_path, [5, 6]))
    ctx.inputs["character_id"] = None
    assert "Character Bible rules" not in VisionCriticNode()._build_prompt(ctx, {})


def test_empty_intersection_no_block(tmp_path):
    # Rules cite only phase 6; checkpoint phase_8_assemble → empty intersection → no block.
    ctx = _ctx(_bundle(tmp_path, [6]), checkpoint="phase_8_assemble")
    assert "Character Bible rules" not in VisionCriticNode()._build_prompt(ctx, {})
