"""Tests for pipeline.agents.sdk_runners — Opus escalation wrapper + stub fallback."""

from __future__ import annotations

import asyncio
import json


def test_sdk_response_ok_property():
    from pipeline.agents.sdk_runners import SDKResponse

    ok = SDKResponse(
        model="claude-opus-4-7", text="{}", duration_s=0.0,
        exit_code=0, error=None,
    )
    assert ok.ok is True

    bad = SDKResponse(
        model="claude-opus-4-7", text="", duration_s=0.0,
        exit_code=1, error="boom",
    )
    assert bad.ok is False


def test_stub_fallback_when_sdk_missing(tmp_path, monkeypatch):
    """No SDK available + no API key → stub returns deterministic structured JSON."""
    from pipeline.agents import sdk_runners

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(sdk_runners, "_sdk_available", lambda: False)

    img = tmp_path / "frame.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n")
    resp = asyncio.run(sdk_runners.invoke_opus_vision(
        prompt="describe this frame",
        image_paths=[img],
        timeout_s=5,
    ))

    assert resp.model == "stub-fallback"
    assert resp.exit_code == 0
    assert resp.ok is True
    assert resp.stub_fallback is True

    payload = json.loads(resp.text)
    assert payload["verdict"] in {"pass", "borderline", "fail"}
    # Escalation stub returns higher confidence than Gemini stub (0.65) so the
    # vision_critic.py routing logic can distinguish which branch fired.
    assert payload["confidence"] >= 0.7
    assert "STUB FALLBACK" in payload["reasoning"]
    assert isinstance(payload["cites_criteria"], list)
    assert payload["cites_criteria"], "Escalation stub must populate cites_criteria"


def test_stub_fallback_handles_empty_image_paths(monkeypatch):
    """Defensive: stub still returns a valid response with no images."""
    from pipeline.agents import sdk_runners

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(sdk_runners, "_sdk_available", lambda: False)
    resp = asyncio.run(sdk_runners.invoke_opus_vision(
        prompt="nothing",
        image_paths=[],
        timeout_s=5,
    ))
    assert resp.ok is True
    payload = json.loads(resp.text)
    assert payload["verdict"] in {"pass", "borderline", "fail"}
