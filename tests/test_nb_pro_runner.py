"""Tests for pipeline.agents.nb_pro_runner — NB Pro plate-generation wrapper.

Cy's Pass 2 plate generation shells out to the existing pencil-animation skill
script (.claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py),
which already handles the google-genai API call + reference images + aspect
ratio. The wrapper layers in:

- Content-addressed cache keyed by (prompt + reference-image content hashes
  + cites_identity_rules + reject_reason + model). Same inputs → cache hit;
  any input changes → fresh generation. The reject_reason field is what makes
  `cy iterate` regenerations invalidate the cache.
- Stub fallback ladder: real subprocess on success path; clean failure on
  subprocess non-zero; tiny PNG placeholder when GEMINI_API_KEY is absent so
  tests don't need the real API.
- NBProResponse envelope matching the AgentSpec/Patch-shaped contract Cy's
  Pass 2 consumes.
"""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from pipeline.agents.nb_pro_runner import (
    NBProResponse,
    _build_skill_cmd,
    _compute_cache_key,
    invoke_image_edit,
)

# Pre-Flo-C cache key for a deterministic no-reference input. Locks the
# byte-identity of the cache key when aspect_ratio is None — the regression
# guard that keeps Cy's locked-Bible plate generation (which passes no
# aspect_ratio) cache-stable across the HF01 fix.
_GOLDEN_KEY_ASPECT_NONE = (
    "7a84b9130f7bb71ff37bbdcf95bc45cbdf951ca05fa0031e828a7c3281d4258d"
)


@pytest.fixture(autouse=True)
def _isolate_env_file(monkeypatch, tmp_path_factory):
    """Repoint the runner's .env source at a guaranteed-empty path.

    The runner's GEMINI_API_KEY gate honors both the live process env AND
    the project .env file (the skill script's --env-file source). Tests
    that monkeypatch.delenv('GEMINI_API_KEY') would silently fail to land
    on the stub path if the real .env file at the repo root carried the
    key — which it does during a developer's live run. This fixture
    repoints _ENV_FILE at a never-existing path so tests express their
    intent ('no key available → stub fallback') correctly.
    """
    sentinel = tmp_path_factory.mktemp("nb_pro_env_isolation") / "absent.env"
    monkeypatch.setattr(
        "pipeline.agents.nb_pro_runner._ENV_FILE", sentinel
    )


@pytest.fixture
def fake_reference_image(tmp_path):
    """A tiny PNG file used as a stand-in reference image."""
    path = tmp_path / "reference.png"
    # Minimal valid PNG: 1x1 transparent. Content matters for hashing,
    # but the bytes themselves are arbitrary — we just need a real file.
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
        b"\x00\x00\x00\rIDATx\x9cc\xf8\xcf\xc0\x00\x00\x00\x03"
        b"\x00\x01;\xa9\xb1\x9c\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    return path


@pytest.fixture
def cache_dir(tmp_path):
    """Per-test cache directory."""
    d = tmp_path / "cache" / "nb_pro"
    d.mkdir(parents=True)
    return d


# ---------------------------------------------------------------------------
# Stub fallback behavior — what every test below relies on
# ---------------------------------------------------------------------------


def test_missing_api_key_returns_stub_placeholder(
    monkeypatch, tmp_path, fake_reference_image, cache_dir
):
    """No GEMINI_API_KEY → stub fallback writes a placeholder PNG, no subprocess."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    output = tmp_path / "out.png"
    response = invoke_image_edit(
        prompt="test plate",
        reference_images=[fake_reference_image],
        output_path=output,
        cache_dir=cache_dir,
        cites_identity_rules=("IR.test.hair.x",),
    )
    assert response.ok
    assert response.stub_fallback is True
    assert response.output_path.exists()
    # Placeholder should be a real PNG with non-trivial bytes (not zero).
    assert response.output_path.stat().st_size > 0


# ---------------------------------------------------------------------------
# Content-addressed cache key
# ---------------------------------------------------------------------------


def test_cache_hit_skips_subprocess(
    monkeypatch, tmp_path, fake_reference_image, cache_dir
):
    """Second call with identical inputs hits cache; subprocess not invoked."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    output_1 = tmp_path / "out1.png"
    response_1 = invoke_image_edit(
        prompt="same prompt",
        reference_images=[fake_reference_image],
        output_path=output_1,
        cache_dir=cache_dir,
    )
    assert response_1.cache_hit is False  # first call: generates (stub or real)

    # Second call: same inputs, different output path. Should be a cache hit.
    output_2 = tmp_path / "out2.png"
    response_2 = invoke_image_edit(
        prompt="same prompt",
        reference_images=[fake_reference_image],
        output_path=output_2,
        cache_dir=cache_dir,
    )
    assert response_2.cache_hit is True
    assert response_2.output_path.exists()
    # Content is preserved from cache.
    assert response_1.output_path.read_bytes() == response_2.output_path.read_bytes()


def test_reject_reason_invalidates_cache(
    monkeypatch, tmp_path, fake_reference_image, cache_dir
):
    """Same inputs + reject_reason → different cache key → fresh generation."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    response_1 = invoke_image_edit(
        prompt="same prompt",
        reference_images=[fake_reference_image],
        output_path=tmp_path / "out1.png",
        cache_dir=cache_dir,
    )
    response_2 = invoke_image_edit(
        prompt="same prompt",
        reference_images=[fake_reference_image],
        output_path=tmp_path / "out2.png",
        cache_dir=cache_dir,
        reject_reason="too cartoonish",
    )
    assert response_1.cache_key != response_2.cache_key
    assert response_2.cache_hit is False  # different key, not a cache hit


def test_cites_identity_rules_change_cache_key(
    monkeypatch, tmp_path, fake_reference_image, cache_dir
):
    """Different cites_identity_rules tuples produce different cache keys."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    response_1 = invoke_image_edit(
        prompt="same",
        reference_images=[fake_reference_image],
        output_path=tmp_path / "out1.png",
        cache_dir=cache_dir,
        cites_identity_rules=("IR.test.hair.cowlick",),
    )
    response_2 = invoke_image_edit(
        prompt="same",
        reference_images=[fake_reference_image],
        output_path=tmp_path / "out2.png",
        cache_dir=cache_dir,
        cites_identity_rules=("IR.test.hair.cowlick", "IR.test.prop.stylus"),
    )
    assert response_1.cache_key != response_2.cache_key


def test_cache_key_stable_across_image_path_with_same_content(
    monkeypatch, tmp_path, fake_reference_image, cache_dir
):
    """Same image content at different paths → same cache key (content-hash, not path)."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    # Copy the reference to a different path with identical bytes.
    other_path = tmp_path / "copied-reference.png"
    other_path.write_bytes(fake_reference_image.read_bytes())

    response_1 = invoke_image_edit(
        prompt="same",
        reference_images=[fake_reference_image],
        output_path=tmp_path / "out1.png",
        cache_dir=cache_dir,
    )
    response_2 = invoke_image_edit(
        prompt="same",
        reference_images=[other_path],
        output_path=tmp_path / "out2.png",
        cache_dir=cache_dir,
    )
    assert response_1.cache_key == response_2.cache_key


def test_model_parameter_changes_cache_key(
    monkeypatch, tmp_path, fake_reference_image, cache_dir
):
    """Different model parameter → different cache key (so NB Pro / NB2 don't collide)."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    response_pro = invoke_image_edit(
        prompt="same",
        reference_images=[fake_reference_image],
        output_path=tmp_path / "out_pro.png",
        cache_dir=cache_dir,
        model="nano-banana-pro",
    )
    response_flash = invoke_image_edit(
        prompt="same",
        reference_images=[fake_reference_image],
        output_path=tmp_path / "out_flash.png",
        cache_dir=cache_dir,
        model="gemini-3.1-flash-image-preview",
    )
    assert response_pro.cache_key != response_flash.cache_key


def test_default_model_is_nb2_flash(monkeypatch, tmp_path, fake_reference_image, cache_dir):
    """The editing/consistency default is NB2 Flash, not NB Pro (Amendment B:
    NB2 holds identity better for editing, costs half, 4x faster, and dodges NB
    Pro's multi-reference downsampling regression). The default must equal an
    explicit NB2 call's cache key, and differ from an explicit NB-Pro call's."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    default_resp = invoke_image_edit(
        prompt="same",
        reference_images=[fake_reference_image],
        output_path=tmp_path / "out_default.png",
        cache_dir=cache_dir,
    )
    explicit_nb2 = invoke_image_edit(
        prompt="same",
        reference_images=[fake_reference_image],
        output_path=tmp_path / "out_nb2.png",
        cache_dir=cache_dir,
        model="gemini-3.1-flash-image-preview",
    )
    explicit_pro = invoke_image_edit(
        prompt="same",
        reference_images=[fake_reference_image],
        output_path=tmp_path / "out_pro.png",
        cache_dir=cache_dir,
        model="gemini-3-pro-image-preview",
    )
    assert default_resp.cache_key == explicit_nb2.cache_key
    assert default_resp.cache_key != explicit_pro.cache_key


# ---------------------------------------------------------------------------
# HF01 — aspect ratio on the NB Pro path (Flo-C)
# ---------------------------------------------------------------------------


def test_build_skill_cmd_omits_aspect_ratio_when_none(tmp_path):
    """Regression-lock Cy's path: no aspect_ratio → argv carries no
    --aspect-ratio flag (byte-identical to the pre-Flo-C command)."""
    cmd = _build_skill_cmd(
        prompt="p",
        reference_images=[],
        output_path=tmp_path / "o.png",
        model="gemini-3.1-flash-image-preview",
    )
    assert "--aspect-ratio" not in cmd


def test_build_skill_cmd_includes_aspect_ratio_when_set(tmp_path):
    """HF01 fix: aspect_ratio='16:9' → argv carries --aspect-ratio 16:9."""
    cmd = _build_skill_cmd(
        prompt="p",
        reference_images=[],
        output_path=tmp_path / "o.png",
        model="gemini-3.1-flash-image-preview",
        aspect_ratio="16:9",
    )
    assert "--aspect-ratio" in cmd
    assert cmd[cmd.index("--aspect-ratio") + 1] == "16:9"


def test_cache_key_byte_identical_when_aspect_ratio_none():
    """aspect_ratio=None (and omitted) must leave the cache key byte-identical
    to the pre-Flo-C digest — Cy's locked-Bible plates stay cache-stable."""
    omitted = _compute_cache_key(
        prompt="lock", reference_images=[], cites_identity_rules=(),
        reject_reason=None, model="gemini-3.1-flash-image-preview",
    )
    explicit_none = _compute_cache_key(
        prompt="lock", reference_images=[], cites_identity_rules=(),
        reject_reason=None, model="gemini-3.1-flash-image-preview",
        aspect_ratio=None,
    )
    assert omitted == _GOLDEN_KEY_ASPECT_NONE
    assert explicit_none == _GOLDEN_KEY_ASPECT_NONE


def test_aspect_ratio_changes_cache_key_when_set():
    """A non-None aspect_ratio perturbs the cache key (so a 16:9 keyframe and a
    square plate from otherwise-identical inputs don't collide)."""
    none_key = _compute_cache_key(
        prompt="lock", reference_images=[], cites_identity_rules=(),
        reject_reason=None, model="gemini-3.1-flash-image-preview",
        aspect_ratio=None,
    )
    set_key = _compute_cache_key(
        prompt="lock", reference_images=[], cites_identity_rules=(),
        reject_reason=None, model="gemini-3.1-flash-image-preview",
        aspect_ratio="16:9",
    )
    assert none_key != set_key


# ---------------------------------------------------------------------------
# Response envelope shape
# ---------------------------------------------------------------------------


def test_response_envelope_carries_required_fields(
    monkeypatch, tmp_path, fake_reference_image, cache_dir
):
    """NBProResponse carries the AgentSpec-compatible contract fields."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    response = invoke_image_edit(
        prompt="test",
        reference_images=[fake_reference_image],
        output_path=tmp_path / "out.png",
        cache_dir=cache_dir,
    )
    assert isinstance(response, NBProResponse)
    assert hasattr(response, "output_path")
    assert hasattr(response, "cache_key")
    assert hasattr(response, "cache_hit")
    assert hasattr(response, "stub_fallback")
    assert hasattr(response, "exit_code")
    assert hasattr(response, "ok")
    # Cache key is a stable hex digest, not None.
    assert isinstance(response.cache_key, str)
    assert len(response.cache_key) >= 16  # at least 16 hex chars (SHA-256 truncated is fine)
