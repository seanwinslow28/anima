"""Tests for pipeline/agents/fal_runner.py — fal.ai Seedream/Qwen transports.

Mirrors the reve_runner contract: self-stubs when FAL_KEY is absent (placeholder
PNG, stub_fallback=True), content-addressed cache, and a real path that REFUSES an
unverified endpoint rather than silently calling the wrong fal model (the reve
schema-was-wrong lesson — STEP B0 verifies + flips the endpoints to verified).

All tests are credential-free: the real fal network path is never reached —
FAL_KEY absent → stub; FAL_KEY present + endpoint unverified → raise BEFORE any
fal_client import or network call.
"""
from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from pipeline.agents.fal_runner import (
    FalResponse,
    _write_placeholder_png,
    invoke_fal_qwen,
    invoke_fal_seedream,
)


def _refs(tmp_path: Path, n: int = 2) -> list[Path]:
    """n tiny, distinct PNG references (in-betweens use both endpoints)."""
    paths = []
    for i in range(n):
        p = tmp_path / f"ref{i}.png"
        Image.new("RGB", (8, 8), (10 + i * 40, 0, 0)).save(p, "PNG")
        paths.append(p)
    return paths


@pytest.fixture(autouse=True)
def _keyless(monkeypatch):
    """Default every test to keyless so the real fal path is never hit by accident."""
    monkeypatch.delenv("FAL_KEY", raising=False)


def test_seedream_stubs_when_no_fal_key(tmp_path):
    out = tmp_path / "out.png"
    resp = invoke_fal_seedream(
        prompt="in-between pose midway", reference_images=_refs(tmp_path),
        output_path=out, cache_dir=tmp_path / ".cache",
    )
    assert resp.stub_fallback is True
    assert resp.endpoint == "stub"
    assert resp.ok
    assert out.exists()
    assert resp.cost_usd > 0


def test_qwen_stubs_when_no_fal_key(tmp_path):
    out = tmp_path / "out.png"
    resp = invoke_fal_qwen(
        prompt="in-between pose midway", reference_images=_refs(tmp_path),
        output_path=out, cache_dir=tmp_path / ".cache",
    )
    assert resp.stub_fallback is True
    assert resp.endpoint == "stub"
    assert resp.ok
    assert out.exists()
    assert resp.cost_usd > 0


def test_stub_placeholder_is_1376x768(tmp_path):
    out = tmp_path / "ph.png"
    _write_placeholder_png(out)
    with Image.open(out) as im:
        assert im.size == (1376, 768)


def test_cache_hit_on_second_call(tmp_path):
    cache = tmp_path / ".cache"
    refs = _refs(tmp_path)
    r1 = invoke_fal_seedream(prompt="p", reference_images=refs,
                             output_path=tmp_path / "a.png", cache_dir=cache)
    assert r1.cache_hit is False
    r2 = invoke_fal_seedream(prompt="p", reference_images=refs,
                             output_path=tmp_path / "b.png", cache_dir=cache)
    assert r2.cache_hit is True
    assert r2.ok


def test_cache_key_changes_with_prompt(tmp_path):
    cache = tmp_path / ".cache"
    refs = _refs(tmp_path)
    r1 = invoke_fal_seedream(prompt="alpha", reference_images=refs,
                             output_path=tmp_path / "a.png", cache_dir=cache)
    r2 = invoke_fal_seedream(prompt="beta", reference_images=refs,
                             output_path=tmp_path / "b.png", cache_dir=cache)
    assert r1.cache_key != r2.cache_key


def test_seedream_refuses_unverified_endpoint_when_key_present(tmp_path, monkeypatch):
    """The reve lesson: never silently call an unverified fal endpoint. With a key
    present (stub path skipped) and the endpoint not yet B0-verified, RAISE before
    any network call."""
    monkeypatch.setenv("FAL_KEY", "dummy-not-used")
    with pytest.raises(RuntimeError, match="verif"):
        invoke_fal_seedream(
            prompt="p", reference_images=_refs(tmp_path),
            output_path=tmp_path / "out.png", cache_dir=tmp_path / ".cache",
        )


def test_qwen_refuses_unverified_endpoint_when_key_present(tmp_path, monkeypatch):
    monkeypatch.setenv("FAL_KEY", "dummy-not-used")
    with pytest.raises(RuntimeError, match="verif"):
        invoke_fal_qwen(
            prompt="p", reference_images=_refs(tmp_path),
            output_path=tmp_path / "out.png", cache_dir=tmp_path / ".cache",
        )


def test_fal_response_ok_property(tmp_path):
    out = tmp_path / "x.png"
    _write_placeholder_png(out)
    ok_resp = FalResponse(output_path=out, cache_key="k", cache_hit=False,
                          stub_fallback=True, endpoint="stub", cost_usd=0.02)
    assert ok_resp.ok is True
    missing = FalResponse(output_path=tmp_path / "nope.png", cache_key="k",
                          cache_hit=False, stub_fallback=True, endpoint="stub", cost_usd=0.02)
    assert missing.ok is False
    err = FalResponse(output_path=out, cache_key="k", cache_hit=False,
                      stub_fallback=False, endpoint="seedream", cost_usd=0.02, exit_code=1)
    assert err.ok is False
