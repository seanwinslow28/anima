"""A2 — model provenance: pin by ID, log the model that actually fired, and never
let a costed runner silently fall back to a backend-default model.

The 2026-06-02 forensics found the agy wrapper ran `agy -p` with NO -m flag, so the
Antigravity backend silently chose gemini-3.5-flash on 272/272 Em-sized calls while
every label claimed gemini-3.1-pro. Cy's Pass-3 verification used the same wrapper,
so its two locked Bibles were Flash-verified, not Pro. These tests give the lesson
code teeth:
  - the Gemini API transport reads the SERVED model back from the response and logs
    it (verify-it-fired, not pin-by-label);
  - the agy wrapper REFUSES a real call without an explicit -m pin (no silent
    backend-default ever again);
  - a costed runner never returns a successful, non-stub response with an empty model.
See docs/2026-06-02-em-provenance-and-hardening-kickoff.md §A2.
"""
from __future__ import annotations

import asyncio
import logging

import pytest

from pipeline.agents import cli_runners, gemini_api_runner as gar
from pipeline.agents.cli_runners import run_antigravity_with_image
from pipeline.agents.gemini_api_runner import GEMINI_VISION_MODEL, run_gemini_api_with_image


# --------------------------------------------------------------------------- #
# Gemini API transport: read the SERVED model back from the response.
# --------------------------------------------------------------------------- #

def _force_real_api(monkeypatch):
    monkeypatch.setattr(gar, "_genai_available", lambda: True)
    monkeypatch.setattr(gar, "_has_gemini_api_key", lambda: True)


def test_gemini_api_records_served_model_from_response(monkeypatch):
    """resp.model is the model the API SERVED (resp.model_version), read back — not
    the pinned constant echoed blindly. A served version != the bare constant proves
    the read-back path."""
    from google import genai
    served = "gemini-3.5-flash-002"

    class _FakeModels:
        def generate_content(self, *, model, contents):
            return type("R", (), {"text": '{"verdict":"pass","confidence":0.9}',
                                   "model_version": served})()

    monkeypatch.setattr(genai, "Client", lambda *a, **k: type("C", (), {"models": _FakeModels()})())
    monkeypatch.setattr(gar, "_resolve_gemini_key", lambda: "fake-key")
    _force_real_api(monkeypatch)

    resp = asyncio.run(run_gemini_api_with_image(prompt="p", image_paths=[]))
    assert resp.ok and not resp.stub_fallback
    assert resp.model == served


def test_gemini_api_logs_the_model_that_fired(monkeypatch, caplog):
    """The model is logged so the provenance lives in the run logs, not just source."""
    served = "gemini-3.5-flash-002"
    _force_real_api(monkeypatch)
    monkeypatch.setattr(gar, "_generate", lambda prompt, image_paths: ('{"verdict":"pass"}', served))
    with caplog.at_level(logging.INFO):
        asyncio.run(run_gemini_api_with_image(prompt="p", image_paths=[]))
    assert any(served in r.getMessage() for r in caplog.records)


def test_costed_api_success_always_records_a_model(monkeypatch):
    """The headline guard: a successful, non-stub costed response MUST carry a
    non-empty model id (gemini_api is Cy's Pass-3 transport and Em's default)."""
    _force_real_api(monkeypatch)
    monkeypatch.setattr(gar, "_generate", lambda prompt, image_paths: ('{"verdict":"pass"}', "gemini-3.5-flash"))
    resp = asyncio.run(run_gemini_api_with_image(prompt="p", image_paths=[]))
    assert resp.ok and not resp.stub_fallback
    assert resp.model  # never empty/None on a costed success


# --------------------------------------------------------------------------- #
# agy wrapper: a real call REQUIRES an explicit model pin.
# --------------------------------------------------------------------------- #

def _agy_present(monkeypatch, *, stdout=b'{"verdict":"pass"}', capture=None):
    monkeypatch.setattr(cli_runners.shutil, "which", lambda _b: "/usr/local/bin/agy")
    monkeypatch.setattr(cli_runners, "_read_agy_log", lambda: "")

    class _FakeProc:
        returncode = 0
        async def communicate(self):
            return stdout, b""

    async def fake_exec(*args, **_k):
        if capture is not None:
            capture["argv"] = list(args)
        return _FakeProc()

    monkeypatch.setattr(cli_runners.asyncio, "create_subprocess_exec", fake_exec)


def test_agy_real_call_without_model_raises(monkeypatch):
    """A real (binary-present) agy call with no model= refuses — the silent
    backend-default that mislabeled 272 calls can never recur unnoticed."""
    _agy_present(monkeypatch)
    with pytest.raises(ValueError, match="model"):
        asyncio.run(run_antigravity_with_image(prompt="p", image_paths=[]))


def test_agy_records_and_passes_pinned_model(monkeypatch):
    """With an explicit model=, agy records it on the response and passes -m on the CLI."""
    capture: dict = {}
    _agy_present(monkeypatch, capture=capture)
    resp = asyncio.run(run_antigravity_with_image(
        prompt="p", image_paths=[], model="gemini-3.5-flash"))
    assert resp.model == "gemini-3.5-flash"
    assert "-m" in capture["argv"] and "gemini-3.5-flash" in capture["argv"]


def test_agy_logs_the_model_that_fired(monkeypatch, caplog):
    _agy_present(monkeypatch)
    with caplog.at_level(logging.INFO):
        asyncio.run(run_antigravity_with_image(prompt="p", image_paths=[], model="gemini-3.5-flash"))
    assert any("gemini-3.5-flash" in r.getMessage() for r in caplog.records)


def test_agy_stub_does_not_require_a_model(monkeypatch):
    """The credential-free stub path (binary absent) is not a costed call, so it
    needs no model pin — CI stays green without one."""
    monkeypatch.setattr(cli_runners.shutil, "which", lambda _b: None)
    resp = asyncio.run(run_antigravity_with_image(prompt="p", image_paths=[]))
    assert resp.ok and resp.stub_fallback
