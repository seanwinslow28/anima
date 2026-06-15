"""Tests for pipeline/orchestration/guards.py — the silent-stub guards.

Credential-free: with no SDK available the smoke calls return a STUB envelope,
so smoke_live_sonnet must raise GuardError (the costed path is not really live).
"""

from __future__ import annotations

import pytest

from pipeline.agents import sdk_runners
from pipeline.orchestration.guards import GuardError, smoke_live_sonnet, scan_stub_marker


def test_smoke_live_sonnet_raises_on_stub(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(sdk_runners, "_sdk_available", lambda: False)
    with pytest.raises(GuardError, match="STUB"):
        smoke_live_sonnet()


def test_scan_stub_marker_detects(tmp_path):
    good = tmp_path / "a.md"
    good.write_text("clean board\n", encoding="utf-8")
    bad = tmp_path / "b.md"
    bad.write_text("# Storyboard (STUB)\n\nSTUB FALLBACK — no SDK\n", encoding="utf-8")
    assert scan_stub_marker([good]) is False
    assert scan_stub_marker([good, bad]) is True
