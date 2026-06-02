"""agy rate-cap detection: a quota-exhausted/empty response must RAISE a distinct
RateCapExhausted, never silently borderline. The empty-vs-malformed distinction is
load-bearing — a malformed-but-non-empty response is the documented defensive-
borderline mode (postmortem Failure 1), NOT a throttle."""
from __future__ import annotations

import asyncio

import pytest

from pipeline.agents import cli_runners
from pipeline.agents.cli_runners import RateCapExhausted, run_antigravity_with_image


class _FakeProc:
    def __init__(self, stdout: bytes, stderr: bytes, returncode: int):
        self._stdout, self._stderr, self.returncode = stdout, stderr, returncode

    async def communicate(self):
        return self._stdout, self._stderr


def _patch_agy(monkeypatch, *, stdout: bytes, stderr: bytes = b"",
               returncode: int = 0, log_text: str = ""):
    """Make agy 'present' and return a controlled process result + log tail."""
    monkeypatch.setattr(cli_runners.shutil, "which", lambda _b: "/usr/local/bin/agy")
    monkeypatch.setattr(cli_runners, "_read_agy_log", lambda: log_text)

    async def fake_exec(*_args, **_kwargs):
        return _FakeProc(stdout, stderr, returncode)

    monkeypatch.setattr(cli_runners.asyncio, "create_subprocess_exec", fake_exec)


def test_empty_stdout_exit_zero_raises(monkeypatch):
    _patch_agy(monkeypatch, stdout=b"   \n", returncode=0)
    with pytest.raises(RateCapExhausted):
        asyncio.run(run_antigravity_with_image(prompt="p", image_paths=[], model="gemini-3.5-flash"))


def test_429_in_stderr_raises(monkeypatch):
    _patch_agy(monkeypatch, stdout=b'{"verdict":"pass"}',
               stderr=b"RESOURCE_EXHAUSTED (code 429): Individual quota reached")
    with pytest.raises(RateCapExhausted):
        asyncio.run(run_antigravity_with_image(prompt="p", image_paths=[], model="gemini-3.5-flash"))


def test_429_in_log_file_raises(monkeypatch):
    # agy writes the 429 to its LOG, not stderr — the exact production bug.
    _patch_agy(monkeypatch, stdout=b'{"verdict":"pass"}', stderr=b"",
               log_text="2026-06-01 ... RESOURCE_EXHAUSTED (code 429): quota reached")
    with pytest.raises(RateCapExhausted):
        asyncio.run(run_antigravity_with_image(prompt="p", image_paths=[], model="gemini-3.5-flash"))


def test_nonempty_unparseable_does_NOT_raise(monkeypatch):
    # Malformed but non-empty → stays on the defensive-borderline path, NOT a rate cap.
    _patch_agy(monkeypatch, stdout=b"I think this frame looks fine; no JSON here.")
    resp = asyncio.run(run_antigravity_with_image(prompt="p", image_paths=[], model="gemini-3.5-flash"))
    assert resp.ok
    assert "looks fine" in resp.text


def test_valid_response_passes_through(monkeypatch):
    _patch_agy(monkeypatch, stdout=b'{"verdict":"pass","confidence":0.9}')
    resp = asyncio.run(run_antigravity_with_image(prompt="p", image_paths=[], model="gemini-3.5-flash"))
    assert resp.ok and "pass" in resp.text
    assert resp.model == "gemini-3.5-flash"   # the pinned model is recorded (A2)


def test_stub_fallback_unaffected(monkeypatch):
    # Binary absent → deterministic stub, never a rate cap.
    monkeypatch.setattr(cli_runners.shutil, "which", lambda _b: None)
    resp = asyncio.run(run_antigravity_with_image(prompt="p", image_paths=[]))
    assert resp.ok and resp.stub_fallback
