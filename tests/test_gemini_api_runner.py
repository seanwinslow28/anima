"""Gemini-API vision transport: same contract as the agy wrapper — a quota-out
or empty response RAISES RateCapExhausted (never silently borderline); a
non-quota error becomes an honest errored response; absent lib/key → deterministic
stub so CI stays green credential-free."""
from __future__ import annotations

import asyncio
import json

import pytest

from pipeline.agents import gemini_api_runner as gar
from pipeline.agents.gemini_api_runner import (
    GEMINI_VISION_MODEL,
    RateCapExhausted,
    run_gemini_api_with_image,
)


def _force_real(monkeypatch):
    monkeypatch.setattr(gar, "_genai_available", lambda: True)
    monkeypatch.setattr(gar, "_has_gemini_api_key", lambda: True)


def test_stub_fallback_when_genai_absent(monkeypatch):
    monkeypatch.setattr(gar, "_genai_available", lambda: False)
    resp = asyncio.run(run_gemini_api_with_image(prompt="p", image_paths=[]))
    assert resp.ok and resp.stub_fallback
    assert json.loads(resp.text)["verdict"] == "borderline"
    assert json.loads(resp.text)["cites_criteria"] == ["AC01"]


def test_stub_fallback_when_key_absent(monkeypatch):
    monkeypatch.setattr(gar, "_genai_available", lambda: True)
    monkeypatch.setattr(gar, "_has_gemini_api_key", lambda: False)
    resp = asyncio.run(run_gemini_api_with_image(prompt="p", image_paths=[]))
    assert resp.stub_fallback


def test_empty_response_raises_ratecap(monkeypatch):
    _force_real(monkeypatch)
    # _generate returns (text, served_model) — A2 read-back contract.
    monkeypatch.setattr(gar, "_generate", lambda prompt, image_paths: ("   \n", GEMINI_VISION_MODEL))
    with pytest.raises(RateCapExhausted):
        asyncio.run(run_gemini_api_with_image(prompt="p", image_paths=[]))


def test_quota_exception_raises_ratecap(monkeypatch):
    _force_real(monkeypatch)

    def boom(prompt, image_paths):
        raise RuntimeError("429 RESOURCE_EXHAUSTED: quota exceeded")

    monkeypatch.setattr(gar, "_generate", boom)
    with pytest.raises(RateCapExhausted):
        asyncio.run(run_gemini_api_with_image(prompt="p", image_paths=[]))


def test_non_quota_error_returns_errored_not_raise(monkeypatch):
    _force_real(monkeypatch)

    def boom(prompt, image_paths):
        raise RuntimeError("transient network blip")

    monkeypatch.setattr(gar, "_generate", boom)
    resp = asyncio.run(run_gemini_api_with_image(prompt="p", image_paths=[]))
    assert not resp.ok and resp.error and not resp.text.strip()


def test_valid_text_passthrough(monkeypatch):
    _force_real(monkeypatch)
    monkeypatch.setattr(
        gar, "_generate",
        lambda prompt, image_paths: ('{"verdict":"pass","confidence":0.9}', GEMINI_VISION_MODEL),
    )
    resp = asyncio.run(run_gemini_api_with_image(prompt="p", image_paths=[]))
    assert resp.ok and "pass" in resp.text and resp.model == GEMINI_VISION_MODEL


def test_generate_pins_model_and_orders_subject_first(monkeypatch, tmp_path):
    # google-genai is installed, so `from google import genai` succeeds; we mock
    # only the network call, proving the pinned model + prompt-then-images ordering.
    from google import genai

    captured = {}

    class _FakeModels:
        def generate_content(self, *, model, contents):
            captured["model"] = model
            captured["n_contents"] = len(contents)
            captured["first_is_text"] = isinstance(contents[0], str)
            return type("R", (), {"text": '{"verdict":"pass"}'})()

    monkeypatch.setattr(genai, "Client", lambda *a, **k: type("C", (), {"models": _FakeModels()})())
    monkeypatch.setattr(gar, "_resolve_gemini_key", lambda: "fake-key")

    img = tmp_path / "subject.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n")
    text, served = gar._generate("the prompt", [img])

    assert captured["model"] == GEMINI_VISION_MODEL
    assert captured["n_contents"] == 2          # prompt + 1 image
    assert captured["first_is_text"] is True    # prompt first, then images (matches Opus path)
    assert "pass" in text
    # The fake response carries no model_version, so _generate falls back to the
    # requested constant — an explicit pin, never a silent backend-default (A2).
    assert served == GEMINI_VISION_MODEL
