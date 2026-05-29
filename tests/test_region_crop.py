"""Tests for Cy's #region crop in the ingest path.

The visual-fidelity post-mortem (§2.1) found body turnarounds were byte-identical
full-sheet copies — the `#region:body-front` suffix was split off and ignored, so
the crop never executed. These tests cover the fix: a `<sheet>.regions.json`
sidecar maps region names to fractional/pixel boxes, and the ingest crops to them.
"""

from __future__ import annotations

import json

from PIL import Image

from pipeline.agents.character_designer import _crop_region, _region_box


def _two_tone_sheet(path, w=100, h=80):
    img = Image.new("RGB", (w, h))
    for x in range(w):
        for y in range(h):
            img.putpixel((x, y), (255, 0, 0) if x < w // 2 else (0, 0, 255))
    img.save(path)
    return path


def test_region_box_reads_fractional_sidecar(tmp_path):
    sheet = _two_tone_sheet(tmp_path / "sheet.png")
    (tmp_path / "sheet.regions.json").write_text(
        json.dumps({"left": [0.0, 0.0, 0.5, 1.0]})
    )
    assert _region_box(sheet, "left") == (0.0, 0.0, 0.5, 1.0)


def test_region_box_none_without_sidecar(tmp_path):
    sheet = _two_tone_sheet(tmp_path / "sheet.png")
    assert _region_box(sheet, "left") is None


def test_crop_region_crops_fractional_left_half(tmp_path):
    sheet = _two_tone_sheet(tmp_path / "sheet.png")
    (tmp_path / "sheet.regions.json").write_text(
        json.dumps({"left": [0.0, 0.0, 0.5, 1.0]})
    )
    out = tmp_path / "out.png"
    assert _crop_region(sheet, "left", out) is True
    cropped = Image.open(out)
    assert cropped.size == (50, 80)
    assert cropped.getpixel((10, 10)) == (255, 0, 0)  # all red (left half)


def test_crop_region_returns_false_when_unmappable(tmp_path):
    """No sidecar (or region absent) → caller must fall back to a full copy and
    flag it, rather than silently shipping a wrong crop."""
    sheet = _two_tone_sheet(tmp_path / "sheet.png")
    assert _crop_region(sheet, "left", tmp_path / "out.png") is False
    (tmp_path / "sheet.regions.json").write_text(json.dumps({"left": [0, 0, 0.5, 1.0]}))
    assert _crop_region(sheet, "right", tmp_path / "out2.png") is False  # region absent
