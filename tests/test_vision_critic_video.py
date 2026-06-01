# tests/test_vision_critic_video.py
from __future__ import annotations

import pytest
from pathlib import Path
from unittest.mock import MagicMock

from pipeline.agents import AgentContext
from pipeline.agents.vision_critic import VisionCriticNode


def test_video_input_creates_and_cleans_up_contact_sheet(tmp_path, monkeypatch):
    # Mock build_contact_sheet to write a dummy file
    mock_build = MagicMock()
    def side_effect(source, out_path, **kwargs):
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(b"dummy_png_bytes")
    mock_build.side_effect = side_effect
    monkeypatch.setattr("pipeline.contact_sheet.build_contact_sheet", mock_build)

    # Mock model runners
    async def mock_runner(*args, **kwargs):
        return MagicMock(text='{"verdict": "pass", "confidence": 0.95, "cites_criteria": []}')
    monkeypatch.setattr("pipeline.agents.vision_critic.run_antigravity_with_image", mock_runner)
    monkeypatch.setattr("pipeline.agents.vision_critic.invoke_opus_vision", mock_runner)

    # Setup dummy video file
    video_path = tmp_path / "test_clip.mp4"
    video_path.touch()

    ctx = AgentContext(
        run_dir=tmp_path / "run",
        inputs={
            "image_path": str(video_path),
            "beat_description": "Sean walks.",
            "frame_id": "W1",
            "impact_tags": [],
            "checkpoint": "phase_6_motion",
        },
        manifest={"critics": {"t2": {}}},
        criteria=None,
        tier="draft",
        cache_dir=tmp_path / "cache",
    )

    node = VisionCriticNode()
    
    # Run node and verify that it completes successfully
    result = node.run(ctx)
    assert result.outputs["verdict"] == "pass"

    # Assert build_contact_sheet was called with expected args
    mock_build.assert_called_once()
    kwargs = mock_build.call_args[1]
    assert kwargs["source"] == video_path
    
    temp_sheet = kwargs["out_path"]
    assert temp_sheet.parent == tmp_path / "run" / "temp_contact_sheets"
    assert temp_sheet.name == "contact_sheet_W1.png"

    # Verify that the temporary file was cleaned up (does not exist)
    assert not temp_sheet.exists()
