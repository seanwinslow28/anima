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

from PIL import Image

from pipeline.agents.similarity_gate import compute_similarity, SimilarityResult


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


def test_different_palette_scores_low(tmp_path):
    """A red plate vs a blue plate — a wholesale palette collapse — scores low."""
    red = _solid(tmp_path / "red.png", (200, 30, 30))
    blue = _solid(tmp_path / "blue.png", (30, 30, 200))
    result = compute_similarity(red, blue)
    assert result.score < 0.6, f"different palettes should score low, got {result.score}"


def test_result_carries_method_label(tmp_path):
    a = _gradient(tmp_path / "a.png")
    result = compute_similarity(a, a)
    # On a deps-free machine this is the PIL fallback; the label must name it.
    assert result.method in {"dinov2", "clip", "pil-perceptual"}
    assert result.method == "pil-perceptual"
