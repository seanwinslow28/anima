"""Tests for pipeline.agents.vision_critic — Em, anima's T2 vision critic."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from pipeline.agents import (
    AgentContext,
    AgentResult,
    AgentSpec,
    NODE_REGISTRY,
    Patch,
)

# Trigger @register_node("vision_critic") side-effect:
import pipeline.agents.vision_critic  # noqa: F401


@dataclass
class _FakeResp:
    """Stand-in for both CLIResponse and SDKResponse during tests."""

    text: str
    ok: bool = True
    stub_fallback: bool = False
    error: str | None = None


def _payload(
    *,
    verdict: str = "pass",
    confidence: float = 0.9,
    reasoning: str = "looks fine",
    patches: list[dict] | None = None,
    cites: list[str] | None = None,
) -> str:
    return json.dumps({
        "verdict": verdict,
        "confidence": confidence,
        "reasoning": reasoning,
        "proposed_patches": patches or [],
        "cites_criteria": cites or [],
    })


def _ctx(
    tmp_path: Path,
    *,
    image_path: Path | None = None,
    impact_tags: list[str] | None = None,
    threshold: float = 0.7,
    escalation_tags: list[str] | None = None,
) -> AgentContext:
    img = image_path or (tmp_path / "frame.png")
    if not img.exists():
        img.write_bytes(b"\x89PNG\r\n\x1a\n")
    return AgentContext(
        run_dir=tmp_path,
        inputs={
            "image_path": str(img),
            "beat_description": "F06: glance down, eyes on stylus",
            "frame_id": "F06",
            "impact_tags": impact_tags or [],
            "checkpoint": "phase_5_generate",
        },
        manifest={
            "anchor": {"path": "images/2D-Character-Sketch-Sean-v1.png"},
            "style": {"aesthetic": "pencil test"},
            "critics": {"t2": {
                "default_model": "gemini-3.1-pro-via-anti-gravity",
                "escalation_model": "claude-opus-4-7-via-sdk",
                "escalation_threshold": threshold,
                "escalation_tags": escalation_tags or ["hero", "identity_critical"],
                "default_context_files": [],
                "auto_apply": False,
                "per_call_timeout_s": 10,
                "wall_budget_s": 30,
            }},
        },
        criteria=None,
        tier="draft",
        cache_dir=tmp_path / ".cache",
    )


# ---- Contract conformance ----


def test_vision_critic_registered_and_satisfies_agentspec():
    cls = NODE_REGISTRY["vision_critic"]
    assert isinstance(cls(), AgentSpec)


def test_vision_critic_stub_path_returns_borderline_with_cites_criteria(
    tmp_path, monkeypatch,
):
    """Real stub fallback (no patching of internal calls). Stub paths populate
    cites_criteria with AC01 so the invariant check passes end-to-end."""
    from pipeline.agents import sdk_runners

    monkeypatch.setenv("PATH", "")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(sdk_runners, "_sdk_available", lambda: False)

    cls = NODE_REGISTRY["vision_critic"]
    result = cls().run(_ctx(tmp_path))

    assert isinstance(result, AgentResult)
    assert result.outputs["verdict"] in {"pass", "borderline", "fail"}
    if result.outputs["verdict"] in {"fail", "borderline"}:
        assert result.cites_criteria, (
            "cites_criteria must be non-empty when verdict is fail or borderline"
        )
    # Stub Gemini returns borderline at confidence 0.65; below default threshold 0.7
    # so escalation should fire and Opus stub returns confidence 0.78.
    assert result.outputs["confidence"] == pytest.approx(0.78)
    assert "(escalated)" in result.notes


# ---- Escalation routing ----


def test_low_confidence_triggers_opus_escalation(tmp_path, monkeypatch):
    seen: list[str] = []

    async def gemini_low(**_kw):
        seen.append("gemini")
        return _FakeResp(text=_payload(verdict="borderline", confidence=0.55, cites=["AC01"]))

    async def opus_high(**_kw):
        seen.append("opus")
        return _FakeResp(text=_payload(verdict="fail", confidence=0.92,
                                       cites=["AC01", "AC02"]))

    monkeypatch.setattr(
        "pipeline.agents.vision_critic.run_antigravity_with_image", gemini_low
    )
    monkeypatch.setattr(
        "pipeline.agents.vision_critic.invoke_opus_vision", opus_high
    )

    cls = NODE_REGISTRY["vision_critic"]
    result = cls().run(_ctx(tmp_path, threshold=0.7))

    assert seen == ["gemini", "opus"]
    # Opus result must win
    assert result.outputs["verdict"] == "fail"
    assert result.outputs["confidence"] == pytest.approx(0.92)
    assert "(escalated)" in result.notes


def test_high_confidence_does_not_escalate(tmp_path, monkeypatch):
    seen: list[str] = []

    async def gemini_high(**_kw):
        seen.append("gemini")
        return _FakeResp(text=_payload(verdict="pass", confidence=0.92))

    async def opus_should_not_fire(**_kw):
        seen.append("opus")
        return _FakeResp(text=_payload(verdict="fail", confidence=0.99))

    monkeypatch.setattr(
        "pipeline.agents.vision_critic.run_antigravity_with_image", gemini_high
    )
    monkeypatch.setattr(
        "pipeline.agents.vision_critic.invoke_opus_vision", opus_should_not_fire
    )

    cls = NODE_REGISTRY["vision_critic"]
    result = cls().run(_ctx(tmp_path, threshold=0.7))

    assert seen == ["gemini"], "Opus must NOT fire when confidence ≥ threshold and no impact tag"
    assert result.outputs["verdict"] == "pass"
    assert "(gemini)" in result.notes


def test_impact_tag_forces_opus_escalation_regardless_of_confidence(
    tmp_path, monkeypatch,
):
    seen: list[str] = []

    async def gemini_super_confident(**_kw):
        seen.append("gemini")
        return _FakeResp(text=_payload(verdict="pass", confidence=0.99))

    async def opus_force_called(**_kw):
        seen.append("opus")
        return _FakeResp(text=_payload(verdict="borderline", confidence=0.81,
                                       cites=["AC02"]))

    monkeypatch.setattr(
        "pipeline.agents.vision_critic.run_antigravity_with_image", gemini_super_confident
    )
    monkeypatch.setattr(
        "pipeline.agents.vision_critic.invoke_opus_vision", opus_force_called
    )

    cls = NODE_REGISTRY["vision_critic"]
    result = cls().run(_ctx(
        tmp_path,
        impact_tags=["hero"],
        threshold=0.7,
        escalation_tags=["hero", "identity_critical"],
    ))

    assert seen == ["gemini", "opus"], "Hero tag must force Opus escalation"
    assert result.outputs["verdict"] == "borderline"
    assert "(escalated)" in result.notes


# ---- cites_criteria invariant ----


def test_fail_verdict_with_empty_cites_criteria_raises(tmp_path, monkeypatch):
    async def gemini_uncited_fail(**_kw):
        return _FakeResp(text=_payload(
            verdict="fail", confidence=0.92, cites=[]
        ))

    async def opus_unused(**_kw):  # pragma: no cover — shouldn't fire
        return _FakeResp(text=_payload(verdict="fail", confidence=0.99))

    monkeypatch.setattr(
        "pipeline.agents.vision_critic.run_antigravity_with_image",
        gemini_uncited_fail,
    )
    monkeypatch.setattr(
        "pipeline.agents.vision_critic.invoke_opus_vision", opus_unused
    )

    cls = NODE_REGISTRY["vision_critic"]
    with pytest.raises(ValueError, match="cites_criteria"):
        cls().run(_ctx(tmp_path, threshold=0.7))


def test_borderline_verdict_with_empty_cites_criteria_raises(tmp_path, monkeypatch):
    async def gemini_uncited_borderline(**_kw):
        return _FakeResp(text=_payload(
            verdict="borderline", confidence=0.91, cites=[]
        ))

    async def opus_unused(**_kw):  # pragma: no cover
        return _FakeResp(text=_payload(verdict="borderline", confidence=0.99))

    monkeypatch.setattr(
        "pipeline.agents.vision_critic.run_antigravity_with_image",
        gemini_uncited_borderline,
    )
    monkeypatch.setattr(
        "pipeline.agents.vision_critic.invoke_opus_vision", opus_unused
    )

    cls = NODE_REGISTRY["vision_critic"]
    with pytest.raises(ValueError, match="cites_criteria"):
        cls().run(_ctx(tmp_path, threshold=0.7))


def test_pass_verdict_with_empty_cites_criteria_is_fine(tmp_path, monkeypatch):
    async def gemini_uncited_pass(**_kw):
        return _FakeResp(text=_payload(
            verdict="pass", confidence=0.95, cites=[]
        ))

    async def opus_unused(**_kw):  # pragma: no cover
        return _FakeResp(text=_payload(verdict="pass", confidence=0.99))

    monkeypatch.setattr(
        "pipeline.agents.vision_critic.run_antigravity_with_image",
        gemini_uncited_pass,
    )
    monkeypatch.setattr(
        "pipeline.agents.vision_critic.invoke_opus_vision", opus_unused
    )

    cls = NODE_REGISTRY["vision_critic"]
    result = cls().run(_ctx(tmp_path, threshold=0.7))
    assert result.outputs["verdict"] == "pass"
    assert result.cites_criteria == []


# ---- Patch shape ----


def test_proposed_patches_carry_proposed_by_em(tmp_path, monkeypatch):
    patches_payload = [
        {
            "target": "manifest.lock.yaml",
            "path": "act1.keyframes[2].pose",
            "operation": "set",
            "value": "head tilts ~15deg, varied line weight 1-3px",
            "rationale": "Em: line weight homogenized in attempt_01",
            "cites_criteria": ["AC01"],
        }
    ]

    async def gemini_with_patches(**_kw):
        return _FakeResp(text=_payload(
            verdict="borderline", confidence=0.91,
            patches=patches_payload, cites=["AC01"],
        ))

    async def opus_unused(**_kw):  # pragma: no cover
        return _FakeResp(text=_payload(verdict="pass", confidence=0.99))

    monkeypatch.setattr(
        "pipeline.agents.vision_critic.run_antigravity_with_image",
        gemini_with_patches,
    )
    monkeypatch.setattr(
        "pipeline.agents.vision_critic.invoke_opus_vision", opus_unused
    )

    cls = NODE_REGISTRY["vision_critic"]
    result = cls().run(_ctx(tmp_path, threshold=0.7))

    assert len(result.proposed_patches) == 1
    patch = result.proposed_patches[0]
    assert isinstance(patch, Patch)
    assert patch.proposed_by == "em-vision-critic"
    assert patch.path == "act1.keyframes[2].pose"
    assert patch.operation == "set"
    assert "AC01" in patch.cites_criteria


# ---- Prompt assembly ----


def test_prompt_includes_standing_context_and_em_addendum(tmp_path, monkeypatch):
    seen_prompts: list[str] = []

    async def gemini_capture(**kw):
        seen_prompts.append(kw["prompt"])
        return _FakeResp(text=_payload(verdict="pass", confidence=0.95))

    async def opus_unused(**_kw):  # pragma: no cover
        return _FakeResp(text=_payload(verdict="pass", confidence=0.99))

    monkeypatch.setattr(
        "pipeline.agents.vision_critic.run_antigravity_with_image", gemini_capture
    )
    monkeypatch.setattr(
        "pipeline.agents.vision_critic.invoke_opus_vision", opus_unused
    )

    cls = NODE_REGISTRY["vision_critic"]
    cls().run(_ctx(tmp_path, threshold=0.7))

    assert seen_prompts, "Gemini wrapper must have been called"
    prompt = seen_prompts[0]
    # The anima preamble must be present
    assert "About anima" in prompt
    # The Em addendum must be present
    assert "script supervisor" in prompt.lower() or "Em" in prompt
    # The frame brief must be present
    assert "F06" in prompt
    assert "glance down" in prompt


# ---- Malformed JSON tolerance ----


def test_parses_code_fenced_json(tmp_path, monkeypatch):
    """LLM responses frequently wrap JSON in ```json fences. Tolerate it."""
    fenced = "```json\n" + _payload(verdict="pass", confidence=0.92) + "\n```"

    async def gemini_fenced(**_kw):
        return _FakeResp(text=fenced)

    async def opus_unused(**_kw):  # pragma: no cover
        return _FakeResp(text=_payload(verdict="pass", confidence=0.99))

    monkeypatch.setattr(
        "pipeline.agents.vision_critic.run_antigravity_with_image", gemini_fenced
    )
    monkeypatch.setattr(
        "pipeline.agents.vision_critic.invoke_opus_vision", opus_unused
    )

    cls = NODE_REGISTRY["vision_critic"]
    result = cls().run(_ctx(tmp_path, threshold=0.7))
    assert result.outputs["verdict"] == "pass"
