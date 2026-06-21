"""Tests for pipeline.agents.planner — Maya, anima's Phase 0 line producer."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pytest

from pipeline.agents import (
    AgentContext,
    AgentResult,
    AgentSpec,
    NODE_REGISTRY,
)

# Trigger @register_node side-effects for both planner + cost_estimator.
import pipeline.agents.planner  # noqa: F401
import pipeline.agents.cost_estimator  # noqa: F401

FIXTURES = Path(__file__).parent / "fixtures"
SEED_STUDIO_BRIEF = (FIXTURES / "studio_brief_seed.md").read_text(encoding="utf-8")


@dataclass
class _FakeResp:
    """Stand-in for SDKResponse during tests. Carries .text + .ok."""

    text: str
    ok: bool = True
    stub_fallback: bool = False
    error: str | None = None


def _planning_envelope(*, criteria: list[dict] | None = None, plan_md: str | None = None) -> str:
    payload = {
        "production_brief_md": (
            "---\npiece_id: \"test-piece\"\nphases_enabled: [0, 5, 6, 8]\n---\n\n"
            "# Production Brief\n\nDrafted by Maya for the test piece.\n"
        ),
        "criteria_json": {
            "version": "1.1",
            "locked": False,
            "criteria": criteria if criteria is not None else [
                {
                    "id": "AC.identity.stylus-right-hand",
                    "description": "Stylus stays in the character's right hand in every frame.",
                    "cites_phase": [5, 6, 8],
                    "cites_personas": ["em", "cy"],
                    "impact_tag": "identity_critical",
                    "parent_id": None,
                    "derived_from": ["studio_brief.non_negotiables"],
                },
                {
                    "id": "AC.technical.aspect-ratio-16-9",
                    "description": "Every frame is 16:9 within 2% tolerance.",
                    "cites_phase": [5],
                    "cites_personas": [],
                    "impact_tag": "structural",
                    "parent_id": None,
                    "derived_from": ["production_brief.target_medium"],
                },
            ],
        },
        "plan_md": plan_md if plan_md is not None else (
            "# Plan\n\n## Cost preview\n\nLow $0.42 / median $0.85 / high $2.40.\n\n"
            "## Phases\n\nPhase 5 keyframes, Phase 6 Seedance, Phase 8 assemble.\n"
        ),
    }
    return "```json\n" + json.dumps(payload) + "\n```"


def _sonnet_clean() -> str:
    return json.dumps({"flag": None, "low_signal": False})


def _sonnet_low_signal() -> str:
    return json.dumps({"flag": None, "low_signal": True})


def _sonnet_flag(flag_text: str) -> str:
    return json.dumps({"flag": flag_text})


def _ctx(tmp_path: Path, brief_dir: Path) -> AgentContext:
    return AgentContext(
        run_dir=tmp_path,
        inputs={"brief_dir": str(brief_dir)},
        manifest={
            "generation": {
                "routing": {
                    "hero_keyframe": {"usd_per_frame": 0.15},
                    "standard_keyframe": {"usd_per_frame": 0.07},
                }
            },
            "tiering": {"phase_5": "draft", "phase_6": "draft"},
            "phases": {
                "phase_5": {"frame_count_hero": 2, "frame_count_standard": 6},
                "phase_6": {"clip_count": 4, "seconds_per_clip": 5},
                "phase_8": {},
            },
        },
        criteria=None,
        tier="draft",
        cache_dir=tmp_path / ".cache",
    )


@pytest.fixture
def brief_dir(tmp_path: Path) -> Path:
    bd = tmp_path / "briefs" / "2026-05-27-test-piece"
    bd.mkdir(parents=True)
    (bd / "00_studio_brief.md").write_text(SEED_STUDIO_BRIEF, encoding="utf-8")
    return bd


def _patch_runners(monkeypatch, opus_responses: list[str], sonnet_responses: list[str]):
    """Patch invoke_opus_text + invoke_sonnet_text to return queued responses."""
    opus_q = list(opus_responses)
    sonnet_q = list(sonnet_responses)
    calls = {"opus": 0, "sonnet": 0}

    async def fake_opus(**_kwargs):
        calls["opus"] += 1
        if not opus_q:
            raise AssertionError("invoke_opus_text called more times than queued responses")
        return _FakeResp(text=opus_q.pop(0))

    async def fake_sonnet(**_kwargs):
        calls["sonnet"] += 1
        if not sonnet_q:
            raise AssertionError("invoke_sonnet_text called more times than queued responses")
        return _FakeResp(text=sonnet_q.pop(0))

    monkeypatch.setattr("pipeline.agents.planner.invoke_opus_text", fake_opus)
    monkeypatch.setattr("pipeline.agents.planner.invoke_sonnet_text", fake_sonnet)
    return calls


# ---- Contract conformance ----


def test_planner_registered_and_satisfies_agentspec():
    cls = NODE_REGISTRY["planner"]
    assert isinstance(cls(), AgentSpec)


# ---- Four-artifact emission ----


def test_planner_emits_four_artifacts(tmp_path, brief_dir, monkeypatch):
    _patch_runners(monkeypatch, [_planning_envelope()], [_sonnet_clean()])
    cls = NODE_REGISTRY["planner"]
    result = cls().run(_ctx(tmp_path, brief_dir))

    assert isinstance(result, AgentResult)
    assert (brief_dir / "01_production_brief.md").exists()
    assert (brief_dir / "acceptance_criteria.json").exists()
    assert (brief_dir / "plan.md").exists()
    assert "cost_estimate" in result.outputs
    assert result.outputs["cost_estimate"]["low_usd"] >= 0


# ---- Three-phase loop branches ----


def test_clean_sonnet_ships_to_human_gate_with_two_calls(tmp_path, brief_dir, monkeypatch):
    """Sonnet returns flag=null + low_signal=false → ship as-is. Two model calls total."""
    calls = _patch_runners(monkeypatch, [_planning_envelope()], [_sonnet_clean()])
    cls = NODE_REGISTRY["planner"]
    cls().run(_ctx(tmp_path, brief_dir))
    assert calls["opus"] == 1
    assert calls["sonnet"] == 1


def test_adversarial_flag_triggers_revision(tmp_path, brief_dir, monkeypatch):
    """Sonnet returns a real flag → second-Opus pass revises the plan. 3 calls total."""
    revised_plan = _planning_envelope(
        plan_md="# Plan (revised)\n\n## Cost preview\n\nTightened estimates.\n",
    )
    calls = _patch_runners(
        monkeypatch,
        [_planning_envelope(), revised_plan],
        [_sonnet_flag("AC.tone.melancholy — interpretive without grounding")],
    )
    cls = NODE_REGISTRY["planner"]
    cls().run(_ctx(tmp_path, brief_dir))
    assert calls["opus"] == 2
    assert calls["sonnet"] == 1
    plan = (brief_dir / "plan.md").read_text(encoding="utf-8")
    assert "revised" in plan


def test_low_signal_triggers_second_opus_as_validator(tmp_path, brief_dir, monkeypatch):
    """Sonnet returns low_signal=true → second-Opus pass acts as validator. 3 calls total."""
    # Second Opus returns a clean adversarial result (no flag) — plan ships as-is.
    calls = _patch_runners(
        monkeypatch,
        [_planning_envelope(), _sonnet_clean()],
        [_sonnet_low_signal()],
    )
    cls = NODE_REGISTRY["planner"]
    cls().run(_ctx(tmp_path, brief_dir))
    assert calls["opus"] == 2
    assert calls["sonnet"] == 1


def test_low_signal_with_second_opus_flag_injects_confidence_note(
    tmp_path, brief_dir, monkeypatch,
):
    """If both Sonnet flags low-signal AND second-Opus surfaces a flag, plan.md
    gets a confidence-notes section naming the unresolved concern."""
    calls = _patch_runners(
        monkeypatch,
        [_planning_envelope(), _sonnet_flag("AC.timing.beat3 — untestable")],
        [_sonnet_low_signal()],
    )
    cls = NODE_REGISTRY["planner"]
    cls().run(_ctx(tmp_path, brief_dir))
    assert calls["opus"] == 2
    plan = (brief_dir / "plan.md").read_text(encoding="utf-8")
    assert "Maya's confidence notes" in plan
    assert "AC.timing.beat3" in plan


# ---- Contract invariants ----


def test_plan_md_contains_no_box_chars(tmp_path, brief_dir, monkeypatch):
    """plan.md must be clean markdown. Box characters are a contract violation."""
    _patch_runners(monkeypatch, [_planning_envelope()], [_sonnet_clean()])
    cls = NODE_REGISTRY["planner"]
    cls().run(_ctx(tmp_path, brief_dir))
    plan = (brief_dir / "plan.md").read_text(encoding="utf-8")
    for ch in "╔═╗║╚╝┌─┐│└┘├┤┬┴┼":
        assert ch not in plan, f"plan.md contains box char {ch!r}"


def test_planner_rejects_box_chars_in_opus_output(tmp_path, brief_dir, monkeypatch):
    """If Opus emits box chars in plan.md, the planner raises ValueError before write."""
    dirty_plan = (
        "# Plan\n\n╔═══════╗\n║ COST  ║\n╚═══════╝\n\nThis plan has boxes.\n"
    )
    _patch_runners(
        monkeypatch,
        [_planning_envelope(plan_md=dirty_plan)],
        [_sonnet_clean()],
    )
    cls = NODE_REGISTRY["planner"]
    with pytest.raises(ValueError, match="box-drawing characters"):
        cls().run(_ctx(tmp_path, brief_dir))


def test_planner_rejects_illegal_impact_tag_at_authoring(tmp_path, brief_dir, monkeypatch):
    """An illegal impact_tag — a category word like 'timing' stamped as a tag —
    raises at authoring, not four gates later. Mirrors the box-char guard.

    This is the cancelled-run failure (2026-06-21): Maya emitted
    `impact_tag: "timing"` on AC.timing.on-twos; it locked clean and ValueError'd
    at the animatic gate. The guard now fails fast inside run()."""
    bad_criteria = [
        {
            "id": "AC.timing.on-twos",
            "description": "Animate on twos; enforcement is structural, not perceptual.",
            "cites_phase": [4, 8],
            "cites_personas": [],
            "impact_tag": "timing",  # illegal — 'timing' is a category, not an impact_tag
            "parent_id": None,
            "derived_from": ["studio_brief.timing"],
        },
    ]
    _patch_runners(monkeypatch, [_planning_envelope(criteria=bad_criteria)], [_sonnet_clean()])
    cls = NODE_REGISTRY["planner"]
    with pytest.raises(ValueError, match="impact_tag"):
        cls().run(_ctx(tmp_path, brief_dir))


def test_planner_accepts_timing_criterion_tagged_structural(tmp_path, brief_dir, monkeypatch):
    """The correct labeling for a timing criterion is `impact_tag: structural` —
    it authors cleanly (the fix is correct labeling, not a wider vocabulary)."""
    good_criteria = [
        {
            "id": "AC.timing.on-twos",
            "description": "Animate on twos; enforcement is structural, not perceptual.",
            "cites_phase": [4, 8],
            "cites_personas": [],
            "impact_tag": "structural",
            "parent_id": None,
            "derived_from": ["studio_brief.timing"],
        },
    ]
    _patch_runners(monkeypatch, [_planning_envelope(criteria=good_criteria)], [_sonnet_clean()])
    cls = NODE_REGISTRY["planner"]
    cls().run(_ctx(tmp_path, brief_dir))  # no raise
    crit = json.loads((brief_dir / "acceptance_criteria.json").read_text())
    assert crit["criteria"][0]["impact_tag"] == "structural"


def test_criteria_json_has_v1_1_graph_shape(tmp_path, brief_dir, monkeypatch):
    """acceptance_criteria.json is v1.1 with mnemonic IDs + impact_tags."""
    _patch_runners(monkeypatch, [_planning_envelope()], [_sonnet_clean()])
    cls = NODE_REGISTRY["planner"]
    cls().run(_ctx(tmp_path, brief_dir))
    crit = json.loads((brief_dir / "acceptance_criteria.json").read_text())
    assert crit["version"] == "1.1"
    for c in crit["criteria"]:
        assert c["id"].startswith("AC."), f"non-mnemonic id: {c['id']}"
        assert "cites_phase" in c
        assert "impact_tag" in c


def test_planner_raises_when_studio_brief_missing(tmp_path, monkeypatch):
    """Maya requires 00_studio_brief.md to exist before running."""
    empty_brief_dir = tmp_path / "briefs" / "empty"
    empty_brief_dir.mkdir(parents=True)
    cls = NODE_REGISTRY["planner"]
    with pytest.raises(FileNotFoundError, match="Studio Brief not found"):
        cls().run(_ctx(tmp_path, empty_brief_dir))


def test_planner_cites_criteria_lists_all_emitted_ids(tmp_path, brief_dir, monkeypatch):
    """AgentResult.cites_criteria reflects every criterion Maya emitted."""
    _patch_runners(monkeypatch, [_planning_envelope()], [_sonnet_clean()])
    cls = NODE_REGISTRY["planner"]
    result = cls().run(_ctx(tmp_path, brief_dir))
    assert "AC.identity.stylus-right-hand" in result.cites_criteria
    assert "AC.technical.aspect-ratio-16-9" in result.cites_criteria


# ---- project_type routing (Task 1.9) ----


def test_bible_authoring_plan_omits_phases_3_through_9(tmp_path, brief_dir, monkeypatch):
    """When project_type=bible_authoring, plan.md scopes to Phase 0 + Phase 2 only."""
    # Sean scaffolded the production brief with project_type=bible_authoring.
    (brief_dir / "01_production_brief.md").write_text(
        "---\n"
        "piece_id: \"sean-anchor-bake\"\n"
        "project_type: bible_authoring\n"
        "phases_enabled: [0, 2]\n"
        "characters_loaded:\n"
        "  - sean-anchor\n"
        "target_medium: museum-walkthrough\n"
        "---\n\n"
        "# Production Brief\n\nBible authoring run for sean-anchor.\n",
        encoding="utf-8",
    )
    _patch_runners(monkeypatch, [_planning_envelope()], [_sonnet_clean()])
    cls = NODE_REGISTRY["planner"]
    cls().run(_ctx(tmp_path, brief_dir))
    plan = (brief_dir / "plan.md").read_text(encoding="utf-8")
    # Scope marker present.
    assert "Phase scope (bible_authoring)" in plan
    assert "Phase 0 — Brief & Plan" in plan
    assert "Phase 2 — Character Bible" in plan
    # Out-of-scope phases NOT in the scope block. The body that Maya's Opus
    # mock emits is generic and may name Phase 5/6/8; the structural marker
    # is what downstream readers pattern-match against.
    scope_start = plan.index("Phase scope (bible_authoring)")
    scope_end = plan.index("\n## ", scope_start + 1) if "\n## " in plan[scope_start + 1:] else len(plan)
    scope_block = plan[scope_start:scope_end]
    for excluded in ("Phase 4", "Phase 5", "Phase 6", "Phase 7", "Phase 8", "Phase 9"):
        assert excluded not in scope_block, (
            f"{excluded} should not appear in the bible_authoring scope block"
        )


def test_animation_piece_default_unchanged(tmp_path, brief_dir, monkeypatch):
    """project_type=animation_piece (default) leaves plan.md unchanged."""
    # No 01_production_brief.md → defaults to animation_piece.
    _patch_runners(monkeypatch, [_planning_envelope()], [_sonnet_clean()])
    cls = NODE_REGISTRY["planner"]
    cls().run(_ctx(tmp_path, brief_dir))
    plan = (brief_dir / "plan.md").read_text(encoding="utf-8")
    # No bible_authoring scope block was prepended.
    assert "Phase scope (bible_authoring)" not in plan


def test_explicit_animation_piece_in_frontmatter_also_unchanged(
    tmp_path, brief_dir, monkeypatch
):
    """Explicit `project_type: animation_piece` reads as the default (no scope block)."""
    (brief_dir / "01_production_brief.md").write_text(
        "---\n"
        "piece_id: \"test-piece\"\n"
        "project_type: animation_piece\n"
        "---\n\n"
        "# Production Brief\n",
        encoding="utf-8",
    )
    _patch_runners(monkeypatch, [_planning_envelope()], [_sonnet_clean()])
    cls = NODE_REGISTRY["planner"]
    cls().run(_ctx(tmp_path, brief_dir))
    plan = (brief_dir / "plan.md").read_text(encoding="utf-8")
    assert "Phase scope (bible_authoring)" not in plan


# --- envelope parser robustness (first integrated run, 2026-06-11) -----------
# Opus 4.8 reliably prefaces its planning envelope with persona prose
# ("Maya here — Pass 1 ..."), so the response is neither bare JSON nor a fully
# anchored ```json fence. The parser must extract the JSON object out of the
# surrounding prose, and must not be confused by braces / backticks inside the
# envelope's own markdown string values (plan_md / production_brief_md).

from pipeline.agents.planner import _parse_json_envelope  # noqa: E402


def test_parse_envelope_bare_json():
    out = _parse_json_envelope('{"production_brief_md":"a","criteria_json":{},"plan_md":"b"}')
    assert out["plan_md"] == "b"


def test_parse_envelope_fully_fenced():
    out = _parse_json_envelope(
        '```json\n{"production_brief_md":"a","criteria_json":{},"plan_md":"b"}\n```'
    )
    assert out["plan_md"] == "b"


def test_parse_envelope_persona_preamble_and_fence():
    """Persona preamble + ```json fence + postamble — the live Opus 4.8 shape."""
    text = (
        "Maya here — Pass 1 primary planning for the integrated run.\n\n"
        "```json\n"
        '{"production_brief_md": "x", "criteria_json": {"version": "1.1"}, "plan_md": "y"}\n'
        "```\n\n"
        "That is my plan — ready for Sean."
    )
    out = _parse_json_envelope(text)
    assert out["criteria_json"]["version"] == "1.1"
    assert out["plan_md"] == "y"


def test_parse_envelope_internal_braces_and_fences_in_strings():
    """Braces and nested ``` fences inside the JSON string values don't truncate."""
    text = (
        "Maya here — planning.\n\n```json\n"
        '{"production_brief_md": "Use `code` and a {placeholder}.",'
        ' "criteria_json": {"criteria": []},'
        ' "plan_md": "# Plan\\n\\n```bash\\necho hi\\n```\\nDone."}\n```\n'
    )
    out = _parse_json_envelope(text)
    assert "{placeholder}" in out["production_brief_md"]
    assert "echo hi" in out["plan_md"]


def test_parse_envelope_empty_raises():
    with pytest.raises(ValueError):
        _parse_json_envelope("   ")
