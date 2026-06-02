"""Em's vision transport is config-selectable: critics.t2.transport routes the
Gemini call to agy (default, today's behavior) or the Gemini API. References,
criteria, and the Opus escalation are unaffected — only the Gemini delivery
path changes."""
from __future__ import annotations

import json

import pytest

from pipeline.agents import AgentContext
from pipeline.agents.vision_critic import VisionCriticNode
from tests.helpers_vision import _FakeCLI


def _ctx(tmp_path, transport=None):
    img = tmp_path / "s.png"
    img.write_bytes(b"x")
    t2 = {} if transport is None else {"transport": transport}
    return AgentContext(
        run_dir=tmp_path,
        inputs={"image_path": str(img), "beat_description": "b", "frame_id": "F",
                "impact_tags": [], "checkpoint": "phase_5_generate"},
        manifest={"critics": {"t2": t2}},
        criteria=None, tier="draft", cache_dir=tmp_path / ".cache",
    )


def _patch_both(monkeypatch):
    calls = {"agy": 0, "gemini": 0}
    payload = json.dumps({"verdict": "pass", "confidence": 0.95, "cites_criteria": []})

    async def fake_agy(*, prompt, image_paths, timeout_s=120):
        calls["agy"] += 1
        return _FakeCLI(payload)

    async def fake_gemini(*, prompt, image_paths, timeout_s=120):
        calls["gemini"] += 1
        return _FakeCLI(payload)

    monkeypatch.setattr("pipeline.agents.vision_critic.run_antigravity_with_image", fake_agy)
    monkeypatch.setattr("pipeline.agents.vision_critic.run_gemini_api_with_image", fake_gemini)
    return calls


def test_default_transport_is_agy(monkeypatch, tmp_path):
    calls = _patch_both(monkeypatch)
    VisionCriticNode().run(_ctx(tmp_path))  # no transport key
    assert calls["agy"] == 1 and calls["gemini"] == 0


def test_transport_gemini_api_routes_to_gemini(monkeypatch, tmp_path):
    calls = _patch_both(monkeypatch)
    VisionCriticNode().run(_ctx(tmp_path, transport="gemini_api"))
    assert calls["gemini"] == 1 and calls["agy"] == 0


def test_unknown_transport_raises(monkeypatch, tmp_path):
    _patch_both(monkeypatch)
    with pytest.raises(ValueError):
        VisionCriticNode().run(_ctx(tmp_path, transport="banana"))
