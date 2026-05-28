"""Tests for pipeline.agents.character_designer — Cy's three-phase AgentSpec.

Cy's three-phase loop:
  Pass 1 — Opus authors character.yaml + IR.* graph + risk-bible.md +
           cy-confidence-notes.md + plate_generation_plan.json (text-only).
  Pass 2 — NB Pro generates plates per the plan (per-plate cache; ingest
           or generate per plate.source value).
  Pass 3 — Gemini 3.1 Pro verifies every plate against cited IR.* rules;
           three-attempt ceiling per plate with reject_reason threaded
           into NB Pro on regeneration.

These tests mock invoke_opus_text + invoke_nb_pro + run_antigravity_with_image
so the AgentSpec contract is exercised without burning API calls.
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

from pipeline.agents import AgentContext, AgentResult
from pipeline.agents.character_designer import CharacterDesignerNode
from pipeline.agents.nb_pro_runner import NBProResponse


# ---------------------------------------------------------------------------
# Fixtures + builders
# ---------------------------------------------------------------------------


@dataclass
class _FakeSDKResponse:
    text: str
    stub_fallback: bool = False
    error: str | None = None
    duration_s: float = 0.0
    tokens: int | None = None


@dataclass
class _FakeCLIResponse:
    text: str
    exit_code: int = 0
    rate_capped: bool = False
    stub_fallback: bool = False
    error: str | None = None
    duration_s: float = 0.0
    tokens: int | None = None
    cli: str = "antigravity"

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and not self.rate_capped and self.error is None


def _make_pass1_envelope(
    *,
    character_id: str = "test-char",
    style_register: str = "pencil-test-colored",
    ir_entries: list[dict] | None = None,
    plates: list[dict] | None = None,
    risk_bible_md: str = "## Test risk bible\n\nThe Bible covers the front, 3-quarter, and profile views.",
    cy_confidence_notes_md: str = "## Test confidence notes\n\nCy hedged on the back angle.",
) -> dict:
    """Build a Pass-1 envelope shaped like Cy's contract."""
    if ir_entries is None:
        ir_entries = [
            {
                "id": f"IR.{character_id}.hair.center-cowlick",
                "description": "Center cowlick visible at the crown.",
                "cites_phase": [5, 6],
                "cites_personas": ["em"],
                "impact_tag": "identity_critical",
                "character_id": character_id,
                "derived_from": [f"characters/{character_id}/anchor.png#region:hair"],
            },
            {
                "id": f"IR.{character_id}.prop.stylus-right-hand",
                "description": "Stylus stays in right hand.",
                "cites_phase": [5],
                "cites_personas": ["em"],
                "impact_tag": "identity_critical",
                "character_id": character_id,
                "derived_from": [f"characters/{character_id}/anchor.png#region:right-hand"],
            },
        ]
    if plates is None:
        plates = [
            {
                "target_path": "turnarounds/body-front.png",
                "source": "generate",
                "prompt": "test character, body front view, pencil-test colored",
                "reference_images": ["anchor.png"],
                "cites_identity_rules": [f"IR.{character_id}.hair.center-cowlick"],
            },
        ]
    return {
        "character_yaml": {
            "character_id": character_id,
            "display_name": "Test Character",
            "style_register": style_register,
            "palette": [{"name": "cream", "hex": "#FAF5E8", "role": "paper-base"}],
            "proportions": {"head_to_body": "1:7", "shoulder_to_hip": "1.2:1", "notes": ""},
            "identity_rules_pointer": "./acceptance_criteria.json",
            "cy_confidence_notes": "(see cy-confidence-notes.md)",
            "flux_lora_seed_plates": ["anchor.png", "turnarounds/body-front.png"],
            "risks": "./risk-bible.md",
            "source_refs_consumed": ["source-refs/notes.md"],
        },
        "ir_entries": ir_entries,
        "risk_bible_md": risk_bible_md,
        "cy_confidence_notes_md": cy_confidence_notes_md,
        "plate_generation_plan": {"plates": plates},
    }


def _make_gemini_verdict(
    verdict: str = "pass",
    confidence: float = 0.95,
    reasoning: str = "The plate honors the cited IR rules.",
    cites: list[str] | None = None,
) -> str:
    """Build a Gemini verdict envelope JSON string."""
    return json.dumps({
        "verdict": verdict,
        "confidence": confidence,
        "reasoning": reasoning,
        "cites_identity_rule": cites or [],
    })


@pytest.fixture
def character_dir(tmp_path):
    """A scaffolded characters/{character_id}/ folder ready for Cy."""
    char_dir = tmp_path / "characters" / "test-char"
    for sub in (
        "turnarounds", "expressions",
        "motion_plates/walk-cycle/source", "motion_plates/walk-cycle/derived",
        "costumes/default", "props",
        "source-refs/3d-mannequin",
    ):
        (char_dir / sub).mkdir(parents=True, exist_ok=True)
    # Anchor + at least one source-ref file so preconditions pass.
    (char_dir / "anchor.png").write_bytes(_tiny_png())
    (char_dir / "source-refs" / "anchor-ref.png").write_bytes(_tiny_png())
    (char_dir / "source-refs" / "notes.md").write_text("Test character voice notes.")
    return char_dir


@pytest.fixture
def base_ctx(tmp_path, character_dir):
    """An AgentContext shaped for Cy with reasonable defaults."""
    run_dir = tmp_path / "runs" / "test-run"
    cache_dir = run_dir / ".cache"
    cache_dir.mkdir(parents=True)
    return AgentContext(
        run_dir=run_dir,
        inputs={
            "character_dir": str(character_dir),
            "studio_brief": "# Studio Brief\n\nA test character.",
        },
        manifest={},
        criteria=None,
        tier="draft",
        cache_dir=cache_dir,
        extras={},
    )


def _tiny_png() -> bytes:
    return (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
        b"\x00\x00\x00\rIDATx\x9cc\xf8\xcf\xc0\x00\x00\x00\x03"
        b"\x00\x01;\xa9\xb1\x9c\x00\x00\x00\x00IEND\xaeB`\x82"
    )


def _patch_runners(
    monkeypatch,
    *,
    opus_envelope: dict | None = None,
    gemini_verdicts: list[str] | None = None,
    nb_pro_responses: list[NBProResponse] | None = None,
):
    """Monkey-patch Cy's three model dependencies with controlled fakes."""
    opus_envelope = opus_envelope or _make_pass1_envelope()
    gemini_verdicts = gemini_verdicts or [_make_gemini_verdict("pass")]
    gemini_iter = iter(gemini_verdicts)

    async def fake_opus(*, prompt: str, **kwargs) -> _FakeSDKResponse:
        return _FakeSDKResponse(
            text="```json\n" + json.dumps(opus_envelope) + "\n```"
        )

    async def fake_gemini(*, prompt: str, image_paths: list, timeout_s: int = 120):
        try:
            verdict_text = next(gemini_iter)
        except StopIteration:
            verdict_text = _make_gemini_verdict("pass")
        return _FakeCLIResponse(text=verdict_text)

    nb_iter = iter(nb_pro_responses or [])

    def fake_nb_pro(*, output_path, cache_dir, **kwargs):
        try:
            response = next(nb_iter)
            # Reuse the response but write to the requested output_path so
            # downstream tests find the file where they expect.
            if response.output_path != output_path:
                output_path.write_bytes(_tiny_png())
                return NBProResponse(
                    output_path=output_path,
                    cache_key=response.cache_key,
                    cache_hit=response.cache_hit,
                    stub_fallback=response.stub_fallback,
                    exit_code=response.exit_code,
                )
            return response
        except StopIteration:
            output_path.write_bytes(_tiny_png())
            return NBProResponse(
                output_path=output_path,
                cache_key="default-cache-key",
                cache_hit=False,
                stub_fallback=True,
                exit_code=0,
            )

    monkeypatch.setattr(
        "pipeline.agents.character_designer.invoke_opus_text", fake_opus
    )
    monkeypatch.setattr(
        "pipeline.agents.character_designer.run_antigravity_with_image", fake_gemini
    )
    monkeypatch.setattr(
        "pipeline.agents.character_designer.invoke_nb_pro", fake_nb_pro
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_three_phase_clean_path_emits_five_artifacts(
    base_ctx, character_dir, monkeypatch
):
    """Clean Pass-3 across all plates → AgentResult with five output port paths populated."""
    _patch_runners(monkeypatch)
    node = CharacterDesignerNode()
    result = node.run(base_ctx)

    assert isinstance(result, AgentResult)
    # Five output ports must be present and point at existing files.
    for key in (
        "character_yaml_path",
        "criteria_path",
        "risk_bible_path",
        "cy_confidence_notes_path",
        "plate_generation_plan_path",
    ):
        path = Path(result.outputs[key])
        assert path.exists(), f"{key} → {path} should exist"
    # plate_results dict is present.
    assert "plate_results" in result.outputs
    assert isinstance(result.outputs["plate_results"], dict)


def test_pass1_emits_valid_v1_2_criteria_file(base_ctx, character_dir, monkeypatch):
    """The acceptance_criteria.json Cy writes validates against the v1.2 schema."""
    from pipeline.criteria import load_criteria

    _patch_runners(monkeypatch)
    node = CharacterDesignerNode()
    result = node.run(base_ctx)
    criteria_path = Path(result.outputs["criteria_path"])

    bundle = load_criteria(criteria_path)
    assert bundle.version == "1.2"
    assert bundle.locked is False
    assert len(bundle.criteria) >= 2
    # Every IR.* entry's character_id matches the parsed prefix (load_criteria
    # already enforces this; loading without raising IS the assertion).
    for c in bundle.criteria:
        if c.id.startswith("IR."):
            assert c.character_id is not None


def test_cites_criteria_populated_with_ir_ids(base_ctx, monkeypatch):
    """AgentResult.cites_criteria carries the IR.* IDs Cy emitted."""
    _patch_runners(monkeypatch)
    node = CharacterDesignerNode()
    result = node.run(base_ctx)
    assert len(result.cites_criteria) >= 2
    assert all(c.startswith("IR.test-char.") for c in result.cites_criteria)


def test_missing_source_refs_raises_precondition_error(tmp_path):
    """Empty source-refs/ directory → precondition error before any Opus call."""
    bare_dir = tmp_path / "characters" / "bare"
    (bare_dir / "source-refs").mkdir(parents=True)
    # No files in source-refs at all.
    (bare_dir / "anchor.png").write_bytes(_tiny_png())

    ctx = AgentContext(
        run_dir=tmp_path / "runs" / "x",
        inputs={"character_dir": str(bare_dir), "studio_brief": "x"},
        manifest={},
        criteria=None,
        tier="draft",
        cache_dir=tmp_path / "cache",
        extras={},
    )
    node = CharacterDesignerNode()
    with pytest.raises(FileNotFoundError, match="source-refs"):
        node.run(ctx)


def test_box_characters_forbidden_in_risk_bible_md(base_ctx, monkeypatch):
    """Opus emitting box characters in risk_bible_md raises ValueError."""
    envelope = _make_pass1_envelope(
        risk_bible_md="╔══════╗\n║ box  ║\n╚══════╝\n",
    )
    _patch_runners(monkeypatch, opus_envelope=envelope)
    node = CharacterDesignerNode()
    with pytest.raises(ValueError, match="box-drawing characters"):
        node.run(base_ctx)


def test_box_characters_forbidden_in_confidence_notes(base_ctx, monkeypatch):
    """Opus emitting box characters in cy_confidence_notes_md also raises."""
    envelope = _make_pass1_envelope(
        cy_confidence_notes_md="┌─ note ─┐\n│ hedge │\n└────────┘\n",
    )
    _patch_runners(monkeypatch, opus_envelope=envelope)
    node = CharacterDesignerNode()
    with pytest.raises(ValueError, match="box-drawing characters"):
        node.run(base_ctx)


def test_gemini_fail_triggers_regeneration_with_reject_reason(
    base_ctx, character_dir, monkeypatch
):
    """First Gemini verdict 'fail' → NB Pro re-called with reject_reason; second 'pass'."""
    # Two Gemini calls: first fail, second pass.
    gemini_verdicts = [
        _make_gemini_verdict("fail", confidence=0.3, reasoning="hair drift on cowlick"),
        _make_gemini_verdict("pass", confidence=0.92, cites=["IR.test-char.hair.center-cowlick"]),
    ]

    # Track NB Pro calls to verify reject_reason gets threaded in.
    nb_pro_calls: list[dict] = []
    original_nb_pro = None

    def tracking_nb_pro(*, output_path, cache_dir, **kwargs):
        nb_pro_calls.append(dict(kwargs))
        output_path.write_bytes(_tiny_png())
        return NBProResponse(
            output_path=output_path,
            cache_key=f"key-{len(nb_pro_calls)}",
            cache_hit=False,
            stub_fallback=False,
            exit_code=0,
        )

    envelope = _make_pass1_envelope()  # one plate, single generate
    async def fake_opus(*, prompt: str, **kwargs):
        return _FakeSDKResponse(text="```json\n" + json.dumps(envelope) + "\n```")

    gemini_iter = iter(gemini_verdicts)
    async def fake_gemini(*, prompt: str, image_paths: list, timeout_s: int = 120):
        return _FakeCLIResponse(text=next(gemini_iter))

    monkeypatch.setattr("pipeline.agents.character_designer.invoke_opus_text", fake_opus)
    monkeypatch.setattr(
        "pipeline.agents.character_designer.run_antigravity_with_image", fake_gemini
    )
    monkeypatch.setattr(
        "pipeline.agents.character_designer.invoke_nb_pro", tracking_nb_pro
    )

    node = CharacterDesignerNode()
    result = node.run(base_ctx)

    # NB Pro called twice: once for initial generation, once for regen with reject_reason.
    assert len(nb_pro_calls) == 2
    assert nb_pro_calls[0].get("reject_reason") is None
    assert "hair drift" in (nb_pro_calls[1].get("reject_reason") or "")

    # Final plate status is pass (after the regen).
    plate_results = result.outputs["plate_results"]
    assert any(
        v.get("gemini_verdict") == "pass" and v.get("attempts", 0) == 2
        for v in plate_results.values()
    )


def test_three_attempt_ceiling_surfaces_human_gate(
    base_ctx, character_dir, monkeypatch
):
    """Three consecutive Gemini fails on the same plate → status = human_gate_required."""
    gemini_verdicts = [
        _make_gemini_verdict("fail", reasoning=f"fail attempt {i}") for i in range(1, 4)
    ]
    envelope = _make_pass1_envelope()
    nb_pro_call_count = 0

    def counting_nb_pro(*, output_path, cache_dir, **kwargs):
        nonlocal nb_pro_call_count
        nb_pro_call_count += 1
        output_path.write_bytes(_tiny_png())
        return NBProResponse(
            output_path=output_path,
            cache_key=f"k{nb_pro_call_count}",
            cache_hit=False,
            stub_fallback=False,
            exit_code=0,
        )

    async def fake_opus(*, prompt: str, **kwargs):
        return _FakeSDKResponse(text="```json\n" + json.dumps(envelope) + "\n```")

    gemini_iter = iter(gemini_verdicts)
    async def fake_gemini(*, prompt: str, image_paths: list, timeout_s: int = 120):
        return _FakeCLIResponse(text=next(gemini_iter))

    monkeypatch.setattr("pipeline.agents.character_designer.invoke_opus_text", fake_opus)
    monkeypatch.setattr(
        "pipeline.agents.character_designer.run_antigravity_with_image", fake_gemini
    )
    monkeypatch.setattr(
        "pipeline.agents.character_designer.invoke_nb_pro", counting_nb_pro
    )

    node = CharacterDesignerNode()
    result = node.run(base_ctx)

    plate_results = result.outputs["plate_results"]
    target = list(plate_results.values())[0]
    assert target["status"] == "human_gate_required"
    assert target["attempts"] == 3
    assert nb_pro_call_count == 3  # initial + 2 regens before the ceiling


def test_ingested_plate_still_runs_gemini_verification(
    base_ctx, character_dir, monkeypatch
):
    """A plate with source: 'ingest:...' copies the file AND runs Gemini Pass 3."""
    # Drop a source-refs file the plate can ingest.
    src = character_dir / "source-refs" / "ingest-source.png"
    src.write_bytes(_tiny_png())

    plates = [{
        "target_path": "expressions/neutral.png",
        "source": "ingest:source-refs/ingest-source.png",
        "cites_identity_rules": ["IR.test-char.hair.center-cowlick"],
    }]
    envelope = _make_pass1_envelope(plates=plates)
    gemini_calls: list[str] = []

    async def fake_opus(*, prompt: str, **kwargs):
        return _FakeSDKResponse(text="```json\n" + json.dumps(envelope) + "\n```")

    async def fake_gemini(*, prompt: str, image_paths: list, timeout_s: int = 120):
        gemini_calls.append(str(image_paths[0]) if image_paths else "")
        return _FakeCLIResponse(text=_make_gemini_verdict("pass"))

    # NB Pro should NOT be called for an ingested plate.
    nb_called: list[bool] = []
    def fail_if_nb_pro(*, output_path, cache_dir, **kwargs):
        nb_called.append(True)
        output_path.write_bytes(_tiny_png())
        return NBProResponse(
            output_path=output_path, cache_key="x", cache_hit=False,
            stub_fallback=False, exit_code=0,
        )

    monkeypatch.setattr("pipeline.agents.character_designer.invoke_opus_text", fake_opus)
    monkeypatch.setattr(
        "pipeline.agents.character_designer.run_antigravity_with_image", fake_gemini
    )
    monkeypatch.setattr(
        "pipeline.agents.character_designer.invoke_nb_pro", fail_if_nb_pro
    )

    node = CharacterDesignerNode()
    result = node.run(base_ctx)

    # The ingested plate exists at the target.
    target = character_dir / "expressions" / "neutral.png"
    assert target.exists()
    # Gemini was called for the ingested plate.
    assert len(gemini_calls) == 1
    # NB Pro was NOT called.
    assert nb_called == []
    # plate_results records the ingest.
    plate_results = result.outputs["plate_results"]
    assert plate_results["expressions/neutral.png"]["status"] == "ingested"
