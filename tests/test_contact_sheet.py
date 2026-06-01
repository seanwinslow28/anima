"""Contact-sheet builder — deterministic N-frame tiling for motion-clip review."""
from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from pipeline.contact_sheet import build_contact_sheet, sample_frame_indices


def test_sample_frame_indices_evenly_spaced():
    # 6 panels from a 100-frame clip → first, last, and 4 interior, no dupes, sorted.
    idx = sample_frame_indices(total_frames=100, n=6)
    assert idx[0] == 0
    assert idx[-1] == 99
    assert len(idx) == 6
    assert idx == sorted(idx)
    assert len(set(idx)) == 6


def test_sample_frame_indices_handles_short_clip():
    # Fewer frames than panels → return all available, no IndexError.
    idx = sample_frame_indices(total_frames=3, n=6)
    assert idx == [0, 1, 2]


def test_build_contact_sheet_from_frame_dir(tmp_path: Path):
    # Build 6 tiny solid-color frames, tile them, assert one PNG of the right shape.
    frame_dir = tmp_path / "frames"
    frame_dir.mkdir()
    for i in range(6):
        Image.new("RGB", (64, 36), (i * 40, 0, 0)).save(frame_dir / f"f_{i:04d}.png")
    out = tmp_path / "sheet.png"

    result = build_contact_sheet(
        source=frame_dir, out_path=out, n=6, cols=3, panel_width=64,
    )

    assert result == out
    assert out.exists()
    sheet = Image.open(out)
    # 3 cols × 2 rows of 64-wide panels (height scaled to aspect), plus label strip.
    assert sheet.width == 3 * 64
    assert sheet.height > 2 * 36  # rows + per-panel label strips


def test_build_contact_sheet_missing_source_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        build_contact_sheet(source=tmp_path / "nope.mp4", out_path=tmp_path / "o.png")
