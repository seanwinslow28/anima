# tests/test_sdk_runners_sonnet_vision.py
"""invoke_sonnet_vision mirrors invoke_opus_vision with the Sonnet model."""
import asyncio
from pathlib import Path

from pipeline.agents import sdk_runners
from pipeline.agents.sdk_runners import invoke_sonnet_vision, SONNET_MODEL


def test_sonnet_vision_stub_when_no_sdk(monkeypatch, tmp_path):
    # Force the no-SDK path → deterministic stub, exercisable credential-free.
    monkeypatch.setattr(sdk_runners, "_sdk_available", lambda: False)
    img = tmp_path / "x.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n")  # not parsed in stub path
    resp = asyncio.run(invoke_sonnet_vision(prompt="review", image_paths=[img]))
    assert resp.stub_fallback is True
    assert resp.text  # JSON verdict envelope
    assert "verdict" in resp.text


def test_sonnet_model_constant():
    assert SONNET_MODEL == "claude-sonnet-4-6"
