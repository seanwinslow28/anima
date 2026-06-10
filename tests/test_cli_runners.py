"""Tests for pipeline.agents.cli_runners — Anti-Gravity + Codex CLI wrappers + stub fallback."""

from __future__ import annotations

import asyncio
import json

import pytest


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


# --------------------------------------------------------------------------- #
# Codex transport (Codie — T3 production peer). Mirrors the agy wrapper:       #
# async subprocess, deterministic stub when the binary is absent, RateCap-     #
# Exhausted on quota/empty-stdout, CLIResponse(cli="codex"). codex is NOT      #
# installed on dev/CI machines, so the stub path is the CI-green default; the  #
# mocked-subprocess tests below exercise the real-binary branch deterministically.
# --------------------------------------------------------------------------- #


class _FakeProc:
    """Minimal stand-in for an asyncio subprocess in the codex real-binary path."""

    def __init__(self, *, stdout: bytes = b"", stderr: bytes = b"", returncode: int = 0):
        self._stdout = stdout
        self._stderr = stderr
        self.returncode = returncode

    async def communicate(self):
        return self._stdout, self._stderr

    def kill(self):  # pragma: no cover - only the timeout path calls this
        pass


def _force_binary_present(monkeypatch, proc: _FakeProc):
    """Make the wrapper take the real-binary branch with a fake subprocess."""
    from pipeline.agents import cli_runners

    monkeypatch.setattr(cli_runners.shutil, "which", lambda _b: "/opt/homebrew/bin/codex")

    async def _fake_exec(*_a, **_k):
        return proc

    monkeypatch.setattr(cli_runners.asyncio, "create_subprocess_exec", _fake_exec)


def test_codex_response_ok_property():
    from pipeline.agents.cli_runners import CLIResponse

    ok = CLIResponse(
        cli="codex", text="{}", tokens=None, duration_s=0.0,
        exit_code=0, rate_capped=False, error=None,
    )
    assert ok.ok is True

    bad = CLIResponse(
        cli="codex", text="", tokens=None, duration_s=0.0,
        exit_code=1, rate_capped=False, error="boom",
    )
    assert bad.ok is False


def test_codex_stub_fallback_when_binary_missing(tmp_path, monkeypatch):
    """No codex on PATH → deterministic structured stub, CI-green."""
    from pipeline.agents.cli_runners import run_codex_with_image

    monkeypatch.setenv("PATH", "")
    img = tmp_path / "frame.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n")

    resp = asyncio.run(run_codex_with_image(
        prompt="critique this frame",
        image_paths=[img],
        timeout_s=5,
    ))

    assert resp.cli == "codex"
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


def test_codex_stub_handles_empty_image_paths(monkeypatch):
    from pipeline.agents.cli_runners import run_codex_with_image

    monkeypatch.setenv("PATH", "")
    resp = asyncio.run(run_codex_with_image(
        prompt="text only",
        image_paths=[],
        timeout_s=5,
    ))
    assert resp.cli == "codex"
    assert resp.ok is True
    payload = json.loads(resp.text)
    assert payload["verdict"] in {"pass", "borderline", "fail"}


def test_codex_success_returns_response(monkeypatch):
    """Real-binary branch: non-empty stdout, exit 0 → ok CLIResponse(cli=codex)."""
    from pipeline.agents import cli_runners

    body = '{"verdict":"pass","confidence":0.9,"reasoning":"ok","proposed_patches":[],"cites_criteria":["AC01"]}'
    _force_binary_present(monkeypatch, _FakeProc(stdout=body.encode(), stderr=b"tokens used\n  123\n", returncode=0))

    resp = asyncio.run(cli_runners.run_codex_with_image(prompt="x", image_paths=[], timeout_s=5))
    assert resp.cli == "codex"
    assert resp.ok is True
    assert resp.exit_code == 0
    assert resp.stub_fallback is False
    assert json.loads(resp.text)["verdict"] == "pass"


def test_codex_empty_stdout_exit0_raises_ratecap(monkeypatch):
    """Empty stdout on exit-0 is the observed quota signal → RateCapExhausted, never a silent verdict."""
    from pipeline.agents import cli_runners

    _force_binary_present(monkeypatch, _FakeProc(stdout=b"   \n", stderr=b"", returncode=0))
    with pytest.raises(cli_runners.RateCapExhausted):
        asyncio.run(cli_runners.run_codex_with_image(prompt="x", image_paths=[], timeout_s=5))


def test_codex_quota_signal_in_stderr_raises_ratecap(monkeypatch):
    """Explicit quota signal in stderr → RateCapExhausted even with non-empty stdout."""
    from pipeline.agents import cli_runners

    _force_binary_present(monkeypatch, _FakeProc(stdout=b"partial", stderr=b"Error: 429 RESOURCE_EXHAUSTED", returncode=0))
    with pytest.raises(cli_runners.RateCapExhausted):
        asyncio.run(cli_runners.run_codex_with_image(prompt="x", image_paths=[], timeout_s=5))


def test_codex_timeout_returns_124(monkeypatch):
    """A hung call surfaces as exit 124 / not-ok, never a raise into the caller."""
    from pipeline.agents import cli_runners

    _force_binary_present(monkeypatch, _FakeProc(stdout=b"", stderr=b"", returncode=0))

    async def _raise_timeout(_coro, timeout):  # noqa: ARG001
        if asyncio.iscoroutine(_coro):
            _coro.close()
        raise asyncio.TimeoutError

    monkeypatch.setattr(cli_runners.asyncio, "wait_for", _raise_timeout)
    resp = asyncio.run(cli_runners.run_codex_with_image(prompt="x", image_paths=[], timeout_s=1))
    assert resp.cli == "codex"
    assert resp.exit_code == 124
    assert resp.ok is False
