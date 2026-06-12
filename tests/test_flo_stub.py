"""Fix A — the offline flo_stub node ($0 --stub image placeholder, Slice 2.1).

A --stub run dispatches flo_stub instead of flo, so the whole CLI chain walks
offline with no GEMINI_API_KEY. The node writes a REAL 1376x768 PNG (the audit
gate PIL-opens candidates uncaught) at the same candidates/F{n}/attempt_{k}.png
path the real route uses.
"""

from __future__ import annotations

from pathlib import Path

# Registration is an import side effect on the orchestrator's path.
import pipeline.orchestration.generate_stage  # noqa: F401
from pipeline import audit
from pipeline.agents import NODE_REGISTRY, AgentContext, AgentResult


def _ctx(tmp_path, frame_num=1):
    return AgentContext(
        run_dir=tmp_path,
        inputs={
            "frame_num": frame_num,
            "prompt": "a test beat",
            "references": ["characters/x/anchor.png"],
            "shot_type": "standard_keyframe",
            "character_id": "x",
        },
        manifest={},
        criteria=None,
        tier="draft",
        cache_dir=tmp_path / ".cache",
    )


def test_flo_stub_registered_and_satisfies_contract():
    assert "flo_stub" in NODE_REGISTRY
    cls = NODE_REGISTRY["flo_stub"]
    assert cls.outputs == {"candidate_path": str}


def test_flo_stub_emits_16_9_candidate_clearing_hf01(tmp_path):
    result = NODE_REGISTRY["flo_stub"]().run(_ctx(tmp_path))
    assert isinstance(result, AgentResult)
    cand = Path(result.outputs["candidate_path"])
    assert cand.exists()
    assert cand == tmp_path / "candidates" / "F01" / "attempt_01.png"
    assert audit.check_aspect_ratio(cand)["result"] == "PASS"


def test_flo_stub_attempts_increment_and_bytes_differ(tmp_path):
    node = NODE_REGISTRY["flo_stub"]()
    a1 = Path(node.run(_ctx(tmp_path)).outputs["candidate_path"])
    a2 = Path(node.run(_ctx(tmp_path)).outputs["candidate_path"])
    assert a2.name == "attempt_02.png"
    assert a1.read_bytes() != a2.read_bytes()  # fresh Em cache keys on re-roll
