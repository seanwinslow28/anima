"""Tests for pipeline.agents.cli_runners — Anti-Gravity CLI wrapper + stub fallback."""

from __future__ import annotations

import asyncio
import json


def test_cli_response_ok_property():
    from pipeline.agents.cli_runners import CLIResponse

    ok = CLIResponse(
        cli="antigravity", text="{}", tokens=None, duration_s=0.0,
        exit_code=0, rate_capped=False, error=None,
    )
    assert ok.ok is True

    rate_capped = CLIResponse(
        cli="antigravity", text="", tokens=None, duration_s=0.0,
        exit_code=0, rate_capped=True, error=None,
    )
    assert rate_capped.ok is False

    bad_exit = CLIResponse(
        cli="antigravity", text="", tokens=None, duration_s=0.0,
        exit_code=1, rate_capped=False, error="boom",
    )
    assert bad_exit.ok is False


def test_stub_fallback_when_binary_missing(tmp_path, monkeypatch):
    """No anti-gravity on PATH → stub returns deterministic structured JSON."""
    from pipeline.agents.cli_runners import run_antigravity_with_image

    monkeypatch.setenv("PATH", "")  # nothing on PATH at all
    img = tmp_path / "frame.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n")

    resp = asyncio.run(run_antigravity_with_image(
        prompt="describe this frame",
        image_paths=[img],
        timeout_s=5,
    ))

    assert resp.cli == "antigravity"
    assert resp.exit_code == 0
    assert resp.rate_capped is False
    assert resp.ok is True

    payload = json.loads(resp.text)
    assert payload["verdict"] in {"pass", "borderline", "fail"}
    assert 0.0 <= payload["confidence"] <= 1.0
    assert isinstance(payload["reasoning"], str) and payload["reasoning"]
    assert isinstance(payload["proposed_patches"], list)
    assert isinstance(payload["cites_criteria"], list)
    assert resp.stub_fallback is True
    assert "STUB FALLBACK" in payload["reasoning"]


def test_stub_fallback_handles_empty_image_paths(tmp_path, monkeypatch):
    """Stub returns valid response even when called with no images (defensive)."""
    from pipeline.agents.cli_runners import run_antigravity_with_image

    monkeypatch.setenv("PATH", "")
    resp = asyncio.run(run_antigravity_with_image(
        prompt="describe nothing",
        image_paths=[],
        timeout_s=5,
    ))
    assert resp.ok is True
    payload = json.loads(resp.text)
    assert payload["verdict"] in {"pass", "borderline", "fail"}
