"""Tests for pipeline.agents.similarity_gate — Cy's Pass-2.5 pixel gate.

The gate computes an identity-similarity score between a generated plate and a
reference (the anchor) BEFORE Gemini's prose Pass-3 fires, so drift that
satisfies the prose rules but doesn't look like the character is surfaced
numerically rather than masked (visual-fidelity post-mortem §2.3).

The method ladder prefers DINOv2 > CLIP embeddings when their (heavy) deps are
installed, and falls back to a pure-PIL perceptual metric that is always
available. These tests exercise the always-on PIL path so CI needs no new deps.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from pipeline.agents import similarity_gate
from pipeline.agents.similarity_gate import compute_similarity, SimilarityResult


@pytest.fixture
def force_pil(monkeypatch):
    """Force the PIL-perceptual tier regardless of whether torch is installed.

    Several tests assert the PIL color/structure metric's specific behavior
    (a red vs blue solid scores low; the method label is 'pil-perceptual').
    Those assertions are tier-specific, so they must not depend on whether the
    machine happens to have torch + the DINOv2 weights. This disables the two
    embedding rungs so compute_similarity deterministically uses PIL."""
    monkeypatch.setattr(similarity_gate, "_dinov2_similarity", lambda a, b: None)
    monkeypatch.setattr(similarity_gate, "_clip_similarity", lambda a, b: None)


def _dinov2_available() -> bool:
    try:
        import torch  # noqa: F401
        import torchvision  # noqa: F401
        from transformers import AutoImageProcessor, AutoModel  # noqa: F401
    except ImportError:
        return False
    return True


def _solid(path: Path, color: tuple[int, int, int], size: int = 128) -> Path:
    Image.new("RGB", (size, size), color).save(path)
    return path


def _gradient(path: Path, size: int = 128) -> Path:
    img = Image.new("RGB", (size, size))
    px = img.load()
    for y in range(size):
        for x in range(size):
            px[x, y] = (x * 2 % 256, y * 2 % 256, (x + y) % 256)
    img.save(path)
    return path


def test_identical_images_score_near_one(tmp_path):
    a = _gradient(tmp_path / "a.png")
    b = _gradient(tmp_path / "b.png")  # byte-identical content
    result = compute_similarity(a, b)
    assert isinstance(result, SimilarityResult)
    assert result.score >= 0.95, f"identical images should score ~1, got {result.score}"
    assert 0.0 <= result.score <= 1.0


def test_full_color_vs_grayscale_scores_lower_than_identical(tmp_path):
    """A full-color image vs its own grayscale conversion must score strictly
    below an identical comparison — this is the monochrome-drift signal that
    Gemini's prose pass was blind to (the romance-hero head-front was rendered
    monochrome against a full-color anchor)."""
    color = _gradient(tmp_path / "color.png")
    gray_path = tmp_path / "gray.png"
    Image.open(color).convert("L").convert("RGB").save(gray_path)

    identical = compute_similarity(color, color).score
    mono = compute_similarity(color, gray_path).score
    assert mono < identical, "color-vs-grayscale must score below identical"


def test_different_palette_scores_low(tmp_path, force_pil):
    """A red plate vs a blue plate — a wholesale palette collapse — scores low
    on the PIL color metric. (DINOv2 embeds two featureless solids similarly, so
    this is a PIL-tier-specific assertion; force_pil makes it deterministic.)"""
    red = _solid(tmp_path / "red.png", (200, 30, 30))
    blue = _solid(tmp_path / "blue.png", (30, 30, 200))
    result = compute_similarity(red, blue)
    assert result.method == "pil-perceptual"
    assert result.score < 0.6, f"different palettes should score low, got {result.score}"


def test_result_carries_method_label(tmp_path):
    a = _gradient(tmp_path / "a.png")
    result = compute_similarity(a, a)
    # The label must always name a known tier; which one depends on installed deps.
    assert result.method in {"dinov2", "clip", "pil-perceptual"}


def test_method_label_is_pil_when_embeddings_unavailable(tmp_path, force_pil):
    """With the embedding rungs disabled, the gate names the PIL fallback."""
    a = _gradient(tmp_path / "a.png")
    assert compute_similarity(a, a).method == "pil-perceptual"


# ---------------------------------------------------------------------------
# DINOv2 regression eval — recovered must score above drifted on each register.
# Fixtures + measured scores: evals/similarity-gate/. Skipped without torch.
# ---------------------------------------------------------------------------

_EVAL_FIXTURES = Path(__file__).resolve().parents[1] / "evals" / "similarity-gate" / "fixtures"


@pytest.mark.skipif(not _dinov2_available(), reason="DINOv2 deps (torch/torchvision/transformers) not installed")
@pytest.mark.parametrize("register", ["sean", "mascot"])
def test_dinov2_regression_recovered_above_drifted(register):
    """The gate must rank the recovered plate above the drifted plate vs the
    anchor, on BOTH the pencil and pixel registers — including the mascot
    register where the PIL tier inverted (post-mortem / fix-session §3.5). This
    is the guard that makes the DINOv2 tier trustworthy enough to persist."""
    anchor = _EVAL_FIXTURES / f"{register}-anchor.png"
    recovered = _EVAL_FIXTURES / f"{register}-recovered.png"
    drifted = _EVAL_FIXTURES / f"{register}-drifted.png"
    for f in (anchor, recovered, drifted):
        assert f.exists(), f"missing eval fixture: {f}"

    rec = compute_similarity(recovered, anchor)
    dft = compute_similarity(drifted, anchor)
    if rec.method != "dinov2":
        # torch imports but the model couldn't load (e.g. offline, no weights):
        # that is an environment limitation, not a regression — skip, don't fail.
        pytest.skip(f"DINOv2 tier did not engage (method={rec.method}); skipping regression")
    assert rec.score > dft.score, (
        f"[{register}] recovered ({rec.score:.4f}) must score above "
        f"drifted ({dft.score:.4f}) vs anchor"
    )
