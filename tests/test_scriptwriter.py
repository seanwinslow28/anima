"""Tests for pipeline/agents/scriptwriter.py — Sam, the Phase-3a scriptwriter.

Credential-free: the stub-run tests force ANIMA_FORCE_STUB so invoke_opus_text
returns Sam's deterministic stub envelope — no model spend, $0. The structural
pass is exercised directly (cast-coverage is the deterministic red failure class
per Decision #1 — proven by test, not asserted).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.agents import AgentContext, CostEstimate, NODE_REGISTRY
import pipeline.agents.scriptwriter  # noqa: F401 — registers "scriptwriter"
from pipeline.agents.scriptwriter import ScriptwriterNode, structural_validate
from pipeline.orchestration.beats import Beat, BeatSheet, load_beats
from pipeline.orchestration.cast import derive_cast


def _manifest() -> dict:
    # Real committed Bibles → derive_cast yields IR namespaces {sean, claude-mascot}.
    return {
        "characters": {
            "sean-anchor": {"folder": "characters/sean-anchor/", "style_register": "pencil-test-colored"},
            "claude-mascot": {"folder": "characters/claude-mascot/", "style_register": "pencil-test-colored"},
        }
    }


def _ctx(tmp_path: Path, brief_dir: Path) -> AgentContext:
    return AgentContext(
        run_dir=tmp_path,
        inputs={"brief_dir": str(brief_dir)},
        manifest=_manifest(),
        criteria=None,
        tier="draft",
        cache_dir=tmp_path / ".cache",
    )


def _beat(bid: int, cast: list[str], emo: str = "x") -> Beat:
    return Beat(id=bid, title=f"B{bid}", intent="does a thing", emotional_beat=emo, cast=cast)


# ----- contract -----

def test_node_registered_and_contract():
    assert "scriptwriter" in NODE_REGISTRY
    node = NODE_REGISTRY["scriptwriter"]()
    assert isinstance(node, ScriptwriterNode)
    assert node.name == "scriptwriter"
    assert node.inputs == {"brief_dir": str}
    assert node.outputs == {"script_path": str, "beats_path": str}
    assert node.cites_criteria == []
    est = node.cost_estimate(None)
    assert isinstance(est, CostEstimate)
    assert est.usd == 0.0


def test_missing_studio_brief_raises(tmp_path):
    brief_dir = tmp_path / "brief"
    brief_dir.mkdir()
    node = ScriptwriterNode()
    with pytest.raises(FileNotFoundError, match="Studio Brief"):
        node.run(_ctx(tmp_path, brief_dir))


# ----- stub authoring path (credential-free) -----

def test_stub_run_emits_script_and_valid_beats(tmp_path, monkeypatch):
    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")
    brief_dir = tmp_path / "brief"
    brief_dir.mkdir()
    (brief_dir / "00_studio_brief.md").write_text(
        "# Brief\nSean draws; the mascot notices and delights; the loop returns.\n",
        encoding="utf-8",
    )
    result = ScriptwriterNode().run(_ctx(tmp_path, brief_dir))

    script_path = Path(result.outputs["script_path"])
    beats_path = Path(result.outputs["beats_path"])
    assert script_path.exists()
    assert beats_path.exists()

    # The emitted beats.json round-trips through the real load_beats with the
    # real manifest's known namespaces — the Sam→Bea contract, proven.
    known = {m["ir_namespace"] for m in derive_cast(_manifest()) if m["ir_namespace"]}
    sheet = load_beats(beats_path, known_namespaces=known)
    assert len(sheet.beats) >= 3

    # The stub marker is present so author_script.py's guard can refuse it.
    assert "STUB FALLBACK" in script_path.read_text(encoding="utf-8")
    assert result.notes  # provenance recorded


# ----- prompt assembly (the Opus authoring path wiring) -----

def test_prompt_loads_voice_instrument_and_context():
    # Guards the wiring: a renamed/dropped prompt file would silently strip the
    # voice. Assert the load-bearing §8 verbatim samples + a CORE move + Sam's
    # contract + the task payload all reach the prompt.
    prompt = ScriptwriterNode()._build_prompt(
        "STUDIO_BRIEF_BODY", "PLAN_BODY", {"sean", "claude-mascot"}
    )
    assert "§8 Voice Samples" in prompt          # the instrument's header
    assert "bedtime juice" in prompt              # a verbatim §8 sample fragment
    assert "Declare-then-Puncture" in prompt      # a CORE move
    assert "You are Sam" in prompt                # Sam's role addendum
    assert "STUDIO_BRIEF_BODY" in prompt          # the brief
    assert "PLAN_BODY" in prompt                  # the plan
    assert "claude-mascot" in prompt              # the cast namespaces


def test_prompt_omits_plan_section_when_absent():
    prompt = ScriptwriterNode()._build_prompt("BRIEF_ONLY", "", {"sean"})
    assert "BRIEF_ONLY" in prompt
    assert "Maya's plan.md" not in prompt          # no empty plan section


# ----- deterministic structural pass (Decision #1) -----

def test_structural_pass_catches_cast_coverage_gap():
    # claude-mascot is loaded but appears in no beat → the red failure class.
    sheet = BeatSheet(
        slug="t", logline="l",
        beats=[_beat(1, ["sean"], "a"), _beat(2, ["sean"], "b"), _beat(3, ["sean"], "c")],
    )
    with pytest.raises(ValueError, match="cast-coverage gap"):
        structural_validate(sheet, known_namespaces={"sean", "claude-mascot"})


def test_structural_pass_accepts_complete_sheet():
    sheet = BeatSheet(
        slug="t", logline="l",
        beats=[
            _beat(1, ["sean", "claude-mascot"], "a"),
            _beat(2, ["sean"], "b"),
            _beat(3, ["claude-mascot"], "c"),
        ],
    )
    structural_validate(sheet, known_namespaces={"sean", "claude-mascot"})  # no raise


def test_structural_pass_rejects_too_few_beats():
    sheet = BeatSheet(slug="t", logline="l", beats=[_beat(1, ["sean"], "a"), _beat(2, ["sean"], "b")])
    with pytest.raises(ValueError, match="beat count"):
        structural_validate(sheet, known_namespaces={"sean"})


def test_structural_pass_rejects_flat_arc():
    sheet = BeatSheet(
        slug="t", logline="l",
        beats=[_beat(1, ["sean"], "same"), _beat(2, ["sean"], "same"), _beat(3, ["sean"], "same")],
    )
    with pytest.raises(ValueError, match="arc"):
        structural_validate(sheet, known_namespaces={"sean"})
