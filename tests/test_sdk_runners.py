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


# ---------------------------------------------------------------------------
# Text-only invocations — Maya planner (commit 3)
# ---------------------------------------------------------------------------


def test_invoke_opus_text_stub_returns_planning_envelope(monkeypatch):
    """No SDK → invoke_opus_text returns Maya's planning-envelope shape."""
    from pipeline.agents import sdk_runners

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(sdk_runners, "_sdk_available", lambda: False)
    resp = asyncio.run(sdk_runners.invoke_opus_text(
        prompt="draft a plan",
        timeout_s=5,
    ))
    assert resp.ok is True
    assert resp.stub_fallback is True
    payload = json.loads(resp.text)
    assert "production_brief_md" in payload
    assert "criteria_json" in payload
    assert "plan_md" in payload
    assert payload["criteria_json"]["version"] == "1.1"
    # Stub plan_md must be clean markdown — no box characters.
    for ch in "╔═╗║╚╝┌─┐│└┘":
        assert ch not in payload["plan_md"], f"stub plan_md contains {ch!r}"


def test_invoke_sonnet_text_stub_returns_adversarial_envelope(monkeypatch):
    """No SDK → invoke_sonnet_text returns the adversarial-validation shape."""
    from pipeline.agents import sdk_runners

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(sdk_runners, "_sdk_available", lambda: False)
    resp = asyncio.run(sdk_runners.invoke_sonnet_text(
        prompt="adversarial validation",
        timeout_s=5,
    ))
    assert resp.ok is True
    assert resp.stub_fallback is True
    assert resp.model == "stub-fallback"
    payload = json.loads(resp.text)
    assert "flag" in payload
    assert "low_signal" in payload
    # The stub flags low_signal so Maya's second-Opus escalation path fires.
    assert payload["low_signal"] is True


def test_invoke_sonnet_text_accepts_custom_stub_fn(monkeypatch):
    """A caller (e.g. Bea) can override stub_fn so the credential-free stub
    round-trips through its own parser, just like Sam does on invoke_opus_text."""
    from pipeline.agents import sdk_runners

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(sdk_runners, "_sdk_available", lambda: False)

    def _custom_stub(prompt: str) -> sdk_runners.SDKResponse:
        return sdk_runners.SDKResponse(
            model=sdk_runners.STUB_MODEL,
            text=json.dumps({"bea_shaped": True}),
            duration_s=0.0,
            exit_code=0,
            error=None,
            stub_fallback=True,
        )

    resp = asyncio.run(sdk_runners.invoke_sonnet_text(
        prompt="board the beats",
        timeout_s=5,
        stub_fn=_custom_stub,
    ))
    assert resp.stub_fallback is True
    assert json.loads(resp.text) == {"bea_shaped": True}
