"""Tests for the selection.md parser/validator."""
from pathlib import Path

import pytest

from pipeline.seedance_v2_select import (
    SelectionRow,
    parse_selection_md,
    validate_selection,
)


SAMPLE_MD = """
# Test Selection

**Source MP4:** path/to/x.mp4
**Extraction:** path/to/raw_24fps/frame_NNNN.png

## Beat 1: Idle — cadence: 12fps

| Slot | Source frame | Cadence | Decision | A-N anchors | Rationale |
|---|---|---|---|---|---|
| 001 | frame_0001.png | 12fps | KEEP | approved/PT_A1_F01_key.png, approved/PT_A1_F40_key.png | First idle |
| —   | frame_0002.png – frame_0008.png | — | HOLD-COLLAPSE | — | Redundant |
| 002 | frame_0009.png | 12fps | KEEP | approved/PT_A1_F01_key.png | Breath |

## Summary

| Metric | Value |
|---|---|
| KEEP decisions | 2 |
"""


def test_parse_keep_rows(tmp_path):
    p = tmp_path / "selection.md"
    p.write_text(SAMPLE_MD)
    rows = parse_selection_md(p)
    keep = [r for r in rows if r.decision == "KEEP"]
    assert len(keep) == 2
    assert keep[0].slot == 1
    assert keep[0].source_frame == "frame_0001.png"
    assert keep[0].cadence == "12fps"
    assert keep[0].anchors == [
        "approved/PT_A1_F01_key.png",
        "approved/PT_A1_F40_key.png",
    ]


def test_parse_hold_collapse_rows(tmp_path):
    p = tmp_path / "selection.md"
    p.write_text(SAMPLE_MD)
    rows = parse_selection_md(p)
    hold = [r for r in rows if r.decision == "HOLD-COLLAPSE"]
    assert len(hold) == 1
    assert hold[0].source_frame == "frame_0002.png – frame_0008.png"


def test_validate_detects_duplicate_slot(tmp_path):
    bad = SAMPLE_MD.replace("| 002 |", "| 001 |")
    p = tmp_path / "selection.md"
    p.write_text(bad)
    rows = parse_selection_md(p)
    errors = validate_selection(rows, anchor_root=tmp_path)
    assert any("duplicate slot" in e.lower() for e in errors)


def test_validate_detects_missing_anchor(tmp_path):
    p = tmp_path / "selection.md"
    p.write_text(SAMPLE_MD)
    rows = parse_selection_md(p)
    errors = validate_selection(rows, anchor_root=tmp_path)
    # All referenced anchors don't exist under tmp_path
    assert any("not found" in e.lower() for e in errors)


def test_validate_accepts_valid_selection(tmp_path):
    (tmp_path / "approved").mkdir()
    (tmp_path / "approved" / "PT_A1_F01_key.png").touch()
    (tmp_path / "approved" / "PT_A1_F40_key.png").touch()
    p = tmp_path / "selection.md"
    p.write_text(SAMPLE_MD)
    rows = parse_selection_md(p)
    errors = validate_selection(rows, anchor_root=tmp_path)
    assert errors == []
