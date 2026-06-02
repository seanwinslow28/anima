# tests/test_vision_critic_references_flag.py
"""A1 — references behind a flag (critics.t2.attach_references, default false).

Em runs reference-blind by DEFAULT — the safe recall-1.00 / false_pass-0.00
profile. The PR #13 reference-grounding path (Bible bundle + IR/AC criteria block)
measured as a REGRESSION in the 2026-06-02 re-baseline (false_pass 0.00->0.15),
so it is gated off pending a deterministic identity backstop (DINOv2) + a clean
re-baseline that clears the false-pass gate. Only critics.t2.attach_references: true
restores the bundle. See docs/2026-06-02-em-provenance-and-hardening-kickoff.md §A1.
"""
from __future__ import annotations

import json
from pathlib import Path

from pipeline.agents import AgentContext
from pipeline.agents.vision_critic import VisionCriticNode
from pipeline.criteria import load_criteria
from tests.helpers_vision import _FakeCLI


def _make_sean_bible(tmp_path: Path) -> Path:
    root = tmp_path / "characters"
    folder = root / "sean-anchor"
    (folder / "turnarounds").mkdir(parents=True)
    (folder / "character.yaml").write_text("character_id: sean\n", encoding="utf-8")
    (folder / "anchor.png").write_bytes(b"x")
    for n in ["head-front", "head-profile-left", "body-3quarter"]:
        (folder / "turnarounds" / f"{n}.png").write_bytes(b"x")
    return root


def _bundle(tmp_path: Path):
    data = {
        "version": "1.2", "locked": False,
        "criteria": [
            {"id": "IR.sean.face.jaw-line-angular-not-rounded",
             "description": "Jaw carries a defined angle at the mandibular corner.",
             "cites_phase": [5, 6], "cites_personas": ["em"],
             "impact_tag": "identity_critical", "character_id": "sean"},
        ],
    }
    p = tmp_path / "ac.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return load_criteria(p)


def _ctx(tmp_path, *, t2_cfg):
    img = tmp_path / "subject.png"
    img.write_bytes(b"x")
    chars = _make_sean_bible(tmp_path)
    return AgentContext(
        run_dir=tmp_path,
        inputs={
            "image_path": str(img), "beat_description": "b", "frame_id": "F",
            "impact_tags": [], "checkpoint": "phase_5_generate", "character_id": "sean",
        },
        manifest={"critics": {"t2": t2_cfg}, "characters_root": str(chars)},
        criteria=_bundle(tmp_path), tier="draft", cache_dir=tmp_path / ".cache",
    )


def _patch_capture(monkeypatch):
    captured = {}

    async def fake_gemini(*, prompt, image_paths, timeout_s=120):
        captured["paths"] = list(image_paths)
        captured["prompt"] = prompt
        return _FakeCLI(json.dumps({"verdict": "pass", "confidence": 0.95, "cites_criteria": []}))

    monkeypatch.setattr("pipeline.agents.vision_critic.run_antigravity_with_image", fake_gemini)
    return captured


def test_default_config_runs_reference_blind(monkeypatch, tmp_path):
    """Default config (no attach_references key) attaches ZERO reference images and
    omits both the reference-plate ordering block and the Bible criteria block."""
    captured = _patch_capture(monkeypatch)
    VisionCriticNode().run(_ctx(tmp_path, t2_cfg={}))
    assert len(captured["paths"]) == 1                       # subject only — reference-blind
    assert Path(captured["paths"][0]).name == "subject.png"
    low = captured["prompt"].lower()
    assert "reference plate" not in low
    assert "character bible rules" not in low


def test_attach_references_false_explicit_runs_reference_blind(monkeypatch, tmp_path):
    """An explicit attach_references: false is identical to the default."""
    captured = _patch_capture(monkeypatch)
    VisionCriticNode().run(_ctx(tmp_path, t2_cfg={"attach_references": False}))
    assert len(captured["paths"]) == 1
    assert "reference plate" not in captured["prompt"].lower()


def test_shipped_manifest_runs_em_reference_blind():
    """The shipped manifest.yaml keeps Em reference-blind (attach_references absent or
    false) until a DINOv2 backstop + a clean re-baseline clear the false-pass gate.
    Guards against an accidental flip-on of the regressing grounding path."""
    import yaml
    repo_root = Path(__file__).resolve().parents[1]
    manifest = yaml.safe_load((repo_root / "manifest.yaml").read_text(encoding="utf-8"))
    t2 = manifest.get("critics", {}).get("t2", {})
    assert t2.get("attach_references", False) is False


def test_attach_references_true_restores_bundle(monkeypatch, tmp_path):
    """attach_references: true restores the PR #13 behavior: subject + Bible refs,
    the reference-plate ordering block, and the IR/AC criteria block."""
    captured = _patch_capture(monkeypatch)
    VisionCriticNode().run(_ctx(tmp_path, t2_cfg={"attach_references": True}))
    paths = captured["paths"]
    assert Path(paths[0]).name == "subject.png"              # subject is image 1
    assert [Path(p).name for p in paths[1:]] == [
        "anchor.png", "head-front.png", "head-profile-left.png", "body-3quarter.png",
    ]
    low = captured["prompt"].lower()
    assert "image 1 is the frame under review" in low
    assert "character bible rules" in low
