# tests/test_vision_critic_criteria.py
"""Em surfaces the character's IR.*/AC.* rules from ctx.criteria so she can cite
them. Graceful when the bundle is None (legacy) or the phase intersection is empty.

The criteria block is flag-gated OFF by default (A1, 2026-06-02); these tests pass
critics.t2.attach_references: true as the t2_cfg so each isolates its intended
condition (bundle-None / character-absent / empty-intersection) rather than passing
because the flag is off. Default-blind is covered in test_vision_critic_references_flag.py."""
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
    prompt = VisionCriticNode()._build_prompt(_ctx(_bundle(tmp_path, [5, 6])), {"attach_references": True})
    assert "Character Bible rules" in prompt
    assert "IR.sean.face.jaw-line-angular-not-rounded" in prompt
    assert "IR.sean.prop.stylus-right-hand-always" in prompt


def test_block_forbids_reason_code_substitution(tmp_path):
    """G6.1: the block must make the exact IR handles salient and explicitly tell
    Em NOT to substitute a generic HF/SF reason-code — the cite-grounding fix for
    construction/shading reason-code substitution (2026-06-04 mini-run, Q1)."""
    prompt = VisionCriticNode()._build_prompt(_ctx(_bundle(tmp_path, [5, 6])), {"attach_references": True})
    # Names the QA reason-code families it is forbidding.
    assert "HF01-HF05" in prompt and "SF01-SF05" in prompt
    # Instructs copy-the-handle, not substitute.
    assert "do not substitute" in prompt.lower()


def test_no_block_when_bundle_none():
    prompt = VisionCriticNode()._build_prompt(_ctx(None), {"attach_references": True})
    assert "Character Bible rules" not in prompt


def test_no_block_when_character_id_absent(tmp_path):
    ctx = _ctx(_bundle(tmp_path, [5, 6]))
    ctx.inputs["character_id"] = None
    assert "Character Bible rules" not in VisionCriticNode()._build_prompt(ctx, {"attach_references": True})


def test_empty_intersection_no_block(tmp_path):
    # Rules cite only phase 6; checkpoint phase_8_assemble → empty intersection → no block.
    ctx = _ctx(_bundle(tmp_path, [6]), checkpoint="phase_8_assemble")
    assert "Character Bible rules" not in VisionCriticNode()._build_prompt(ctx, {"attach_references": True})


# --- G6.1b: the criteria-text decoupling guarantee (the anti-repeat guard) ---------
#
# The 2026-06-07 re-baseline measured nothing because the criteria block shared the
# attach_references gate, which was OFF — so the authored G6.1 handles never reached
# Em and her prompt was byte-identical to G5. These tests would have caught that: they
# assert the criteria-text lever surfaces the block (with a real new G6.1 handle) WHILE
# attaching zero reference images, and that the blind control attaches neither.

def _view_bundle(tmp_path: Path):
    """A bundle carrying a NET-NEW G6.1 view handle, so the anti-repeat test asserts on
    a rule that did not exist before this workstream (not the legacy jaw/stylus rules)."""
    data = {
        "version": "1.2", "locked": False,
        "criteria": [
            {"id": "IR.sean.view.declared-view-matches-drawn",
             "description": "The drawn view matches the declared camera view.",
             "cites_phase": [5, 6], "cites_personas": ["em"],
             "impact_tag": "identity_critical", "character_id": "sean"},
        ],
    }
    p = tmp_path / "view.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return load_criteria(p)


def test_criteria_text_attaches_block_without_images(tmp_path):
    """attach_criteria_text=True, attach_references=False ⇒ the criteria block (sentinel
    + a real new handle) IS in the prompt, AND zero reference images are attached.
    The two halves are the decoupling guarantee and the anti-repeat coverage."""
    node = VisionCriticNode()
    t2_cfg = {"attach_criteria_text": True}  # attach_references absent → False

    # Gate-level decoupling: criteria-text ON, references OFF. run() computes
    # references=[] when _attach_references is False, so n_references == 0 (zero images).
    assert node._attach_criteria_text(t2_cfg) is True
    assert node._attach_references(t2_cfg) is False

    prompt = node._build_prompt(_ctx(_view_bundle(tmp_path)), t2_cfg, n_references=0)
    # (a) the criteria block is present — the thing the prior run silently missed.
    assert "CITE THESE EXACT IDs" in prompt
    assert "IR.sean.view.declared-view-matches-drawn" in prompt
    # (b) zero reference images ⇒ no "Reference plates" section (decoupling guarantee).
    assert "Reference plates" not in prompt


def test_no_block_when_both_flags_off(tmp_path):
    """The blind control: neither flag set ⇒ no criteria block (production default)."""
    prompt = VisionCriticNode()._build_prompt(_ctx(_view_bundle(tmp_path)), {}, n_references=0)
    assert "Character Bible rules" not in prompt
    assert "CITE THESE EXACT IDs" not in prompt
