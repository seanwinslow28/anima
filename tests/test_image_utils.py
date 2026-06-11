"""Tests for pipeline.agents.image_utils.normalize_to_png.

#12: the Gemini pencil skill writes JPEG bytes into an `attempt_NN.png` path;
ffmpeg's PNG decoder rejects them. normalize_to_png re-encodes a mislabeled
candidate to a real PNG in place, at the source (the FloNode return boundary).
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from pipeline.agents.image_utils import normalize_to_png


def _png_bytes_format(path: Path) -> str:
    with Image.open(path) as img:
        return img.format


def test_normalize_jpeg_as_png_rewrites_to_real_png(tmp_path):
    """JPEG bytes saved under a .png name → re-encoded to a real PNG; returns True."""
    p = tmp_path / "attempt_01.png"
    Image.new("RGB", (8, 8), color=(123, 45, 67)).save(p, "JPEG")
    assert _png_bytes_format(p) == "JPEG"  # the bug, reproduced

    rewrote = normalize_to_png(p)

    assert rewrote is True
    assert _png_bytes_format(p) == "PNG"


def test_normalize_already_png_is_idempotent_noop(tmp_path):
    """An already-PNG file is left byte-identical and returns False (no needless rewrite)."""
    p = tmp_path / "frame.png"
    Image.new("RGB", (8, 8), color=(10, 20, 30)).save(p, "PNG")
    before = p.read_bytes()

    rewrote = normalize_to_png(p)

    assert rewrote is False
    assert p.read_bytes() == before  # untouched, not re-saved


def test_normalize_non_image_left_untouched_no_crash(tmp_path):
    """A file PIL can't open is left as-is and returns False — the per-frame
    return boundary must not crash on a malformed transport output."""
    p = tmp_path / "bogus.png"
    p.write_bytes(b"png")  # not a real image

    rewrote = normalize_to_png(p)

    assert rewrote is False
    assert p.read_bytes() == b"png"
