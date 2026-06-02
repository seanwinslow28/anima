# tests/test_vision_critic_references.py
"""Em attaches Bible reference plates (subject = image 1) and tells the model which
is which. character_id absent → no references (graceful, no regression)."""
from __future__ import annotations

import json
from pathlib import Path

from pipeline.agents import AgentContext
from pipeline.agents.vision_critic import VisionCriticNode


def _make_sean_bible(tmp_path: Path) -> Path:
    root = tmp_path / "characters"
    folder = root / "sean-anchor"
    (folder / "turnarounds").mkdir(parents=True)
    (folder / "character.yaml").write_text("character_id: sean\n", encoding="utf-8")
    (folder / "anchor.png").write_bytes(b"x")
    for n in ["head-front", "head-profile-left", "body-3quarter"]:
        (folder / "turnarounds" / f"{n}.png").write_bytes(b"x")
    return root


def _ctx(tmp_path, *, character_id="sean", checkpoint="phase_5_generate", image="subject.png"):
    img = tmp_path / image
    img.write_bytes(b"x")
    chars = _make_sean_bible(tmp_path)
    return AgentContext(
        run_dir=tmp_path,
        inputs={
            "image_path": str(img), "beat_description": "b", "frame_id": "F",
            "impact_tags": [], "checkpoint": checkpoint, "character_id": character_id,
        },
        manifest={"critics": {"t2": {}}, "characters_root": str(chars)},
        criteria=None, tier="draft", cache_dir=tmp_path / ".cache",
    )


def _patch_capture(monkeypatch):
    captured = {}

    async def fake_gemini(*, prompt, image_paths, timeout_s=120):
        captured["paths"] = list(image_paths)
        captured["prompt"] = prompt
        from tests.helpers_vision import _FakeCLI
        return _FakeCLI(json.dumps({"verdict": "pass", "confidence": 0.95, "cites_criteria": []}))

    monkeypatch.setattr("pipeline.agents.vision_critic.run_antigravity_with_image", fake_gemini)
    return captured


def test_run_attaches_references_subject_first(monkeypatch, tmp_path):
    captured = _patch_capture(monkeypatch)
    VisionCriticNode().run(_ctx(tmp_path))
    paths = captured["paths"]
    assert Path(paths[0]).name == "subject.png"            # subject is image 1
    assert [Path(p).name for p in paths[1:]] == [
        "anchor.png", "head-front.png", "head-profile-left.png", "body-3quarter.png",
    ]


def test_references_attach_on_phase6_still(monkeypatch, tmp_path):
    # A .png at phase_6_motion → no contact sheet build; references still attach.
    captured = _patch_capture(monkeypatch)
    VisionCriticNode().run(_ctx(tmp_path, checkpoint="phase_6_motion"))
    assert len(captured["paths"]) == 5  # subject + anchor + 3


def test_no_references_when_character_id_absent(monkeypatch, tmp_path):
    captured = _patch_capture(monkeypatch)
    ctx = _ctx(tmp_path)
    ctx.inputs["character_id"] = None
    VisionCriticNode().run(ctx)
    assert len(captured["paths"]) == 1  # subject only


def test_prompt_has_ordering_block_when_references(monkeypatch, tmp_path):
    captured = _patch_capture(monkeypatch)
    VisionCriticNode().run(_ctx(tmp_path))
    low = captured["prompt"].lower()
    assert "image 1 is the frame under review" in low
    assert "reference plate" in low


def test_build_prompt_no_ordering_block_when_zero_refs():
    node = VisionCriticNode()
    ctx = AgentContext(
        run_dir=Path("/tmp/x"),
        inputs={"image_path": "/tmp/x.png", "beat_description": "b", "frame_id": "F",
                "impact_tags": [], "checkpoint": "phase_5_generate"},
        manifest={"critics": {"t2": {}}}, criteria=None, tier="draft",
        cache_dir=Path("/tmp/x/.cache"),
    )
    assert "reference plate" not in node._build_prompt(ctx, {}, n_references=0).lower()
