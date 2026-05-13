"""Tests for the cleanup driver's reference-building + retry-ladder logic."""
from pathlib import Path
from unittest.mock import patch

import pytest

from pipeline.seedance_v2_cleanup import (
    UNIVERSAL_PROMPT,
    build_references,
    retry_attempt_prompt,
    run_cleanup_for_slot,
)
from pipeline.seedance_v2_select import SelectionRow


def make_row(slot, cadence, anchors):
    return SelectionRow(
        slot=slot,
        source_frame=f"frame_{slot:04d}.png",
        cadence=cadence,
        decision="KEEP",
        anchors=anchors,
        rationale="t",
        beat="t",
    )


def test_build_references_12fps_excludes_prev(tmp_path):
    row = make_row(1, "12fps", ["approved/PT_A1_F01_key.png"])
    refs = build_references(
        row,
        source_dir=tmp_path / "raw_24fps",
        anchor_root=tmp_path,
        a2_anchor="approved/PT_A1_F01_key.png",
        prev_cleaned=tmp_path / "prev.png",
    )
    # A-2 always present. 12fps stretches do NOT add prev_cleaned.
    assert refs[0] == tmp_path / "approved/PT_A1_F01_key.png"
    assert (tmp_path / "prev.png") not in refs


def test_build_references_24fps_includes_prev(tmp_path):
    row = make_row(2, "24fps", ["approved/PT_A1_F22_key.png"])
    refs = build_references(
        row,
        source_dir=tmp_path / "raw_24fps",
        anchor_root=tmp_path,
        a2_anchor="approved/PT_A1_F01_key.png",
        prev_cleaned=tmp_path / "prev.png",
    )
    # 24fps stretches DO add prev_cleaned (as last reference).
    assert refs[-1] == tmp_path / "prev.png"


def test_build_references_24fps_no_prev_yet(tmp_path):
    row = make_row(2, "24fps", ["approved/PT_A1_F22_key.png"])
    refs = build_references(
        row,
        source_dir=tmp_path / "raw_24fps",
        anchor_root=tmp_path,
        a2_anchor="approved/PT_A1_F01_key.png",
        prev_cleaned=None,
    )
    # First frame in a 24fps stretch: no prev to chain from.
    assert all(p.name != "prev.png" for p in refs)


def test_retry_attempt_prompts_differ():
    p1 = retry_attempt_prompt(1)
    p2 = retry_attempt_prompt(2)
    p3 = retry_attempt_prompt(3)
    # Attempt 2 adds explicit identity correction.
    assert "jaw shape" in p2.lower() or "eye spacing" in p2.lower()
    # Attempt 3 adds paper-texture refinement block.
    assert "paper" in p3.lower() and "texture" in p3.lower()
    # Universal prompt always present.
    assert UNIVERSAL_PROMPT in p1
    assert UNIVERSAL_PROMPT in p2
    assert UNIVERSAL_PROMPT in p3


@patch("pipeline.seedance_v2_cleanup.subprocess.run")
def test_run_cleanup_invokes_generate_image_with_refs(mock_run, tmp_path):
    def fake_subprocess(cmd, *args, **kwargs):
        # Find the --output path and touch it so reencode_and_resize succeeds
        out_idx = cmd.index("--output") + 1
        out_path = Path(cmd[out_idx])
        out_path.parent.mkdir(parents=True, exist_ok=True)
        # Touch with valid PNG so reencode_and_resize doesn't crash.
        # The simplest cross-platform approach is to write a 1x1 PNG.
        from PIL import Image
        Image.new("RGB", (10, 10), (255, 255, 255)).save(out_path, "PNG")
        mock_result = type("Result", (), {"returncode": 0, "stderr": ""})
        return mock_result()
    mock_run.side_effect = fake_subprocess
    row = make_row(5, "24fps", ["approved/PT_A1_F22_key.png"])
    (tmp_path / "approved").mkdir()
    (tmp_path / "approved" / "PT_A1_F01_key.png").touch()
    (tmp_path / "approved" / "PT_A1_F22_key.png").touch()
    (tmp_path / "raw_24fps").mkdir()
    (tmp_path / "raw_24fps" / "frame_0005.png").touch()

    run_cleanup_for_slot(
        row,
        run_dir=tmp_path,
        source_dir=tmp_path / "raw_24fps",
        clean_dir=tmp_path / "clean",
        anchor_root=tmp_path,
        a2_anchor="approved/PT_A1_F01_key.png",
        prev_cleaned=None,
        attempt=1,
    )
    assert mock_run.called
    cmd = mock_run.call_args[0][0]
    # Must call the gemini-pencil-animation-image-gen script
    assert "generate_image.py" in " ".join(cmd)
    # Must include the universal prompt
    assert UNIVERSAL_PROMPT in cmd
    # Must include --reference followed by the A-2 + beat-matched anchor + source frame
    assert "--reference" in cmd
