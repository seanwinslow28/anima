"""Cy the Character Designer — eval suite runner.

Parameterized over evals/character-designer/cases.yaml. Each case becomes a
pytest test asserting Cy's output against the case's `expected:` block.
Cases marked `is_intentionally_red: true` xfail by design — the failure is
the artifact (per the v2 change-map §7 discipline + commit 3b's planner
eval pattern).

The closing-the-loop test (case 7) is the structural novelty over the
planner eval suite: it doesn't mock Em — it authors a Bible via mocked Cy
calls, then invokes Em's VisionCriticNode against the deliberately-broken
Phase 5 frame with the merged CriteriaBundle loaded. The case ships
intentionally red because Em's prompt doesn't yet load the IR.* rules; the
xfail-to-green diff in a follow-up commit is the museum content
documenting *the moment Bible authoring became contract-grounded*.

Run with: .venv/bin/pytest evals/character-designer/runner.py -v
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path

import pytest
import yaml

from pipeline.agents import AgentContext
from pipeline.agents.character_designer import CharacterDesignerNode
from pipeline.agents.nb_pro_runner import NBProResponse
from pipeline.criteria import load_all_criteria

from evals.character_designer.conftest import (
    make_character_envelope,
    make_gemini_verdict,
)

CASES = yaml.safe_load(
    (Path(__file__).parent / "cases.yaml").read_text(encoding="utf-8")
)["cases"]


@dataclass
class _FakeSDKResponse:
    text: str
    stub_fallback: bool = False
    error: str | None = None


@dataclass
class _FakeCLIResponse:
    text: str
    exit_code: int = 0
    rate_capped: bool = False
    stub_fallback: bool = False
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and not self.rate_capped and self.error is None


def _tiny_png() -> bytes:
    return (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
        b"\x00\x00\x00\rIDATx\x9cc\xf8\xcf\xc0\x00\x00\x00\x03"
        b"\x00\x01;\xa9\xb1\x9c\x00\x00\x00\x00IEND\xaeB`\x82"
    )


def _build_opus_payloads(case: dict) -> list[str]:
    payloads: list[str] = []
    for spec in case["mocked_responses"]["opus"]:
        if spec["kind"] == "pass1_envelope":
            payloads.append(make_character_envelope(
                character_id=spec["character_id"],
                style_register=spec.get("style_register", "pencil-test-colored"),
                ir_count=int(spec.get("ir_count", 5)),
                ir_categories=spec.get("ir_categories"),
                plate_count=len([
                    g for g in case["mocked_responses"].get("gemini", [])
                ]) or 1,
            ))
        else:
            raise ValueError(f"Unknown opus mocked_response kind: {spec['kind']}")
    return payloads


def _build_gemini_payloads(case: dict) -> list[str]:
    return [
        make_gemini_verdict(
            verdict=spec["kind"],
            reasoning=spec.get("reasoning", "fixture reasoning"),
        )
        for spec in case["mocked_responses"].get("gemini", [])
    ]


def _make_character_dir(tmp_path: Path, character_id: str, fixture_dir: Path) -> Path:
    """Build a hermetic character folder under tmp_path mirroring the fixture."""
    cd = tmp_path / "characters" / character_id
    for sub in (
        "turnarounds", "expressions",
        "motion_plates/walk-cycle/source", "motion_plates/walk-cycle/derived",
        "costumes/default", "props",
        "source-refs/3d-mannequin",
    ):
        (cd / sub).mkdir(parents=True, exist_ok=True)
    (cd / "anchor.png").write_bytes(_tiny_png())
    if fixture_dir.exists():
        for f in fixture_dir.iterdir():
            if f.is_file():
                shutil.copy2(f, cd / "source-refs" / f.name)
            elif f.is_dir():
                # Multi-character fixtures carry per-character subdirs.
                sub_target = cd / "source-refs" / f.name
                sub_target.mkdir(parents=True, exist_ok=True)
                for sf in f.iterdir():
                    if sf.is_file():
                        shutil.copy2(sf, sub_target / sf.name)
    # Always drop a minimal notes.md so the precondition passes.
    notes = cd / "source-refs" / "notes.md"
    if not notes.exists():
        notes.write_text(
            f"# {character_id} fixture notes\n\nMinimal source-refs voice note for the eval suite.\n",
            encoding="utf-8",
        )
    return cd


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_character_designer_case(case, tmp_path, fixtures_dir, monkeypatch, request):
    """Run Cy against a fixture; assert against the expected block."""
    if case["expected"].get("is_intentionally_red"):
        request.node.add_marker(
            pytest.mark.xfail(
                reason=f"intentionally red: {case['description']}",
                strict=False,
            )
        )

    # ---- Schema-only case (no Cy run) — exercises load_all_criteria directly ----
    if case["name"] == "schema-validates-across-style-registers":
        _run_schema_cross_register_case(tmp_path)
        return

    # ---- Closing-the-loop case — Cy authors, then Em runs for real against the broken frame ----
    if case["name"] == "closing-the-loop-em-cites-cy-rules":
        _run_closing_the_loop_case(
            case, tmp_path, fixtures_dir, monkeypatch,
        )
        return

    # ---- Standard Cy-run case ----
    fixture_dir = fixtures_dir / case["fixture_dir"]
    character_dir = _make_character_dir(tmp_path, case["character_id"], fixture_dir)
    opus_payloads = _build_opus_payloads(case)
    gemini_payloads = _build_gemini_payloads(case)
    _patch_cy_runners(monkeypatch, opus_payloads, gemini_payloads)

    ctx = AgentContext(
        run_dir=tmp_path / "runs" / case["name"],
        inputs={"character_dir": str(character_dir), "studio_brief": "fixture brief"},
        manifest={},
        criteria=None,
        tier="draft",
        cache_dir=tmp_path / "runs" / case["name"] / ".cache",
        extras={},
    )
    ctx.cache_dir.mkdir(parents=True, exist_ok=True)
    result = CharacterDesignerNode().run(ctx)
    expected = case["expected"]

    # IR rule counts.
    criteria = json.loads(Path(result.outputs["criteria_path"]).read_text(encoding="utf-8"))
    ir_count = sum(1 for c in criteria["criteria"] if c["id"].startswith("IR."))
    assert ir_count >= expected["min_ir_rules"], (
        f"{case['name']}: too few IR rules: {ir_count} < {expected['min_ir_rules']}"
    )

    # Category coverage.
    categories = {c["id"].split(".")[2] for c in criteria["criteria"] if c["id"].startswith("IR.")}
    assert len(categories) >= expected["min_ir_categories"], (
        f"{case['name']}: too few IR categories: {sorted(categories)} < "
        f"{expected['min_ir_categories']}"
    )

    # style_register.
    yaml_payload = Path(result.outputs["character_yaml_path"]).read_text(encoding="utf-8")
    assert f"style_register: {expected['style_register']}" in yaml_payload, (
        f"{case['name']}: character.yaml does not carry expected style_register"
    )

    # Human-gate plate count.
    plate_results = result.outputs["plate_results"]
    human_gate = sum(
        1 for v in plate_results.values()
        if v.get("status") == "human_gate_required"
    )
    assert human_gate == expected["plate_human_gate_count"], (
        f"{case['name']}: human_gate count: {human_gate} != "
        f"{expected['plate_human_gate_count']}"
    )

    # All plates passed (when expected).
    if expected["plate_results_all_passed"]:
        for path, status in plate_results.items():
            assert status.get("status") in ("verified", "ingested", "stub", "generated"), (
                f"{case['name']}: plate {path} status={status.get('status')} "
                f"not in {{verified, ingested, stub, generated}}"
            )


# ---------------------------------------------------------------------------
# Specialized case runners
# ---------------------------------------------------------------------------


def _run_schema_cross_register_case(tmp_path: Path) -> None:
    """Schema validates a merged bundle across the two registers (sean +
    claude-mascot). Asserts query_by_character filters correctly."""
    sean_path = tmp_path / "characters" / "sean-anchor" / "acceptance_criteria.json"
    mascot_path = tmp_path / "characters" / "claude-mascot" / "acceptance_criteria.json"

    sean_path.parent.mkdir(parents=True, exist_ok=True)
    mascot_path.parent.mkdir(parents=True, exist_ok=True)

    sean_path.write_text(json.dumps({
        "version": "1.2",
        "locked": False,
        "criteria": [
            {
                "id": "IR.sean.hair.center-cowlick",
                "description": "Center cowlick at crown.",
                "cites_phase": [5], "cites_personas": ["em"],
                "impact_tag": "identity_critical",
                "character_id": "sean",
            },
            {
                "id": "IR.sean.prop.stylus-right-hand",
                "description": "Stylus in right hand.",
                "cites_phase": [5], "cites_personas": ["em"],
                "impact_tag": "identity_critical",
                "character_id": "sean",
            },
        ],
    }), encoding="utf-8")

    mascot_path.write_text(json.dumps({
        "version": "1.2",
        "locked": False,
        "criteria": [
            {
                "id": "IR.claude-mascot.palette.limited-orange",
                "description": "Four-step indexed palette.",
                "cites_phase": [5], "cites_personas": ["em"],
                "impact_tag": "identity_critical",
                "character_id": "claude-mascot",
            },
        ],
    }), encoding="utf-8")

    manifest = {
        "criteria_sources": {
            "bibles": [str(sean_path), str(mascot_path)],
        }
    }
    bundle = load_all_criteria(manifest)
    sean_rules = bundle.query_by_character("sean")
    mascot_rules = bundle.query_by_character("claude-mascot")
    assert len(sean_rules) == 2
    assert len(mascot_rules) == 1
    # No collisions; both registers fit the same schema.
    assert all(r.id.startswith("IR.sean.") for r in sean_rules)
    assert all(r.id.startswith("IR.claude-mascot.") for r in mascot_rules)


def _run_closing_the_loop_case(
    case: dict,
    tmp_path: Path,
    fixtures_dir: Path,
    monkeypatch,
) -> None:
    """Author the sean Bible via mocked Cy, then invoke Em for real
    against the deliberately-broken Phase 5 frame with the merged
    CriteriaBundle loaded. Em must cite at least one IR.sean.* rule.

    GREEN as of the em-reference-images workstream (2026-06-01): Em's prompt
    now surfaces the merged CriteriaBundle's IR.sean.* rules
    (vision_critic._criteria_block), so the reference+criteria-loaded critic
    cites a Bible rule against the broken frame. The xfail→green diff is the
    museum content (the moment Bible authoring became contract-grounded). Both
    the Gemini default and Opus escalation paths are mocked to read the same
    prompt, since identity_critical force-escalates to Opus.
    """
    from pipeline.agents.vision_critic import VisionCriticNode

    # First — author Cy's Bible with mocked runners.
    fixture_dir = fixtures_dir / case["fixture_dir"]
    character_dir = _make_character_dir(tmp_path, case["character_id"], fixture_dir)
    opus_payloads = _build_opus_payloads(case)
    _patch_cy_runners(monkeypatch, opus_payloads, [make_gemini_verdict()])

    cy_ctx = AgentContext(
        run_dir=tmp_path / "runs" / case["name"],
        inputs={"character_dir": str(character_dir), "studio_brief": "fixture brief"},
        manifest={},
        criteria=None,
        tier="draft",
        cache_dir=tmp_path / "runs" / case["name"] / ".cache",
        extras={},
    )
    cy_ctx.cache_dir.mkdir(parents=True, exist_ok=True)
    cy_result = CharacterDesignerNode().run(cy_ctx)
    criteria_path = Path(cy_result.outputs["criteria_path"])

    # Now — invoke Em against the broken frame WITH the merged CriteriaBundle.
    manifest = {
        "criteria_sources": {
            "bibles": [str(criteria_path)],
        }
    }
    merged_bundle = load_all_criteria(manifest)
    import json as _json
    import re as _re

    broken_frame = fixtures_dir / "deliberately-broken-phase-5-frame.png"
    assert broken_frame.exists(), "deliberately-broken-phase-5-frame.png fixture missing"

    # Simulate a real reference+criteria-loaded critic: cite the first IR.sean.* rule
    # that Em's prompt actually SURFACED. If the criteria half of the fix is present,
    # the prompt carries the rule and the mock cites it (green). If it is absent, no
    # IR id is in the prompt, cites is empty on a `fail` verdict, and Em's
    # cites_criteria invariant RAISES — keeping the case honestly red. The mock can
    # only cite what was genuinely put in front of Em; it cannot fabricate grounding.
    def _fake_gemini_cites_surfaced_ir(*, prompt, image_paths, timeout_s=120):
        m = _re.search(r"IR\.sean\.[A-Za-z0-9.\-]+", prompt)
        cited = [m.group(0)] if m else []
        return _FakeCLIResponse(text=_json.dumps({
            "verdict": "fail", "confidence": 0.9,
            "reasoning": "Broken frame: proportion + stylus drift vs the Bible references.",
            "proposed_patches": [], "cites_criteria": cited,
        }))

    async def _fake_gemini(*, prompt, image_paths, timeout_s=120):
        return _fake_gemini_cites_surfaced_ir(prompt=prompt, image_paths=image_paths)

    monkeypatch.setattr(
        "pipeline.agents.vision_critic.run_antigravity_with_image", _fake_gemini,
    )

    # impact_tags carries identity_critical → Em force-escalates to the Opus path,
    # so the FINAL verdict comes from invoke_opus_vision, not the Gemini default.
    # Mock it too with the SAME prompt-reading behavior (both paths build from the
    # one prompt) so the escalated verdict also cites the surfaced IR rule. Without
    # this the unmocked Opus path returns a defensive borderline with empty cites and
    # Em's cites_criteria invariant raises — the case would never go green on the
    # Gemini mock alone. (Plan gap: Task 5 patched only the Gemini path; the escalation
    # routing means the Opus path is what actually produces this case's verdict.)
    async def _fake_opus(*, prompt, image_paths, timeout_s=120):
        return _fake_gemini_cites_surfaced_ir(prompt=prompt, image_paths=image_paths)

    monkeypatch.setattr(
        "pipeline.agents.vision_critic.invoke_opus_vision", _fake_opus,
    )

    em_ctx = AgentContext(
        run_dir=tmp_path / "runs" / case["name"],
        inputs={
            "image_path": str(broken_frame),
            "beat_description": "Sean glances down at the stylus; pencil-test register.",
            "frame_id": "F06",
            "impact_tags": ["identity_critical"],
            "checkpoint": "phase_5_generate",
            "character_id": "sean",
        },
        manifest={
            # This case exercises Em's criteria-grounding (surface the Bible's IR
            # rules into the prompt so she can cite them). That path is flag-gated
            # OFF by default since A1 (2026-06-02) — reference-blind is production —
            # so the case must opt in explicitly to test the capability it asserts.
            "critics": {"t2": {"attach_references": True}},
            "criteria_sources": {"bibles": [str(criteria_path)]},
        },
        criteria=merged_bundle,
        tier="draft",
        cache_dir=tmp_path / "runs" / case["name"] / ".cache",
        extras={},
    )

    em_result = VisionCriticNode().run(em_ctx)
    ir_citations = [c for c in em_result.cites_criteria if c.startswith("IR.sean.")]
    assert len(ir_citations) >= 1, (
        f"{case['name']}: Em did not cite any IR.sean.* rule. "
        f"All citations: {em_result.cites_criteria}. The criteria half of the "
        f"reference-images fix should surface the Bible's IR rules into Em's prompt "
        f"so she can ground a verdict; the diff that flips this green is the museum "
        f"content (the moment Bible authoring became contract-grounded)."
    )


# ---------------------------------------------------------------------------
# Shared mock-runner monkey-patcher
# ---------------------------------------------------------------------------


def _patch_cy_runners(
    monkeypatch,
    opus_payloads: list[str],
    gemini_payloads: list[str],
) -> None:
    """Patch invoke_opus_text + invoke_image_edit + run_gemini_api_with_image with
    queued responses. Mirrors the planner-suite's _patch_runners shape. (Cy's Pass-3
    verifier moved agy -> Gemini API transport 2026-06-02; A2 model-provenance fix.)"""
    opus_q = list(opus_payloads)
    gemini_q = list(gemini_payloads)

    async def fake_opus(*, prompt: str, **_kwargs) -> _FakeSDKResponse:
        if not opus_q:
            raise AssertionError("invoke_opus_text exhausted queued responses")
        return _FakeSDKResponse(text=opus_q.pop(0))

    async def fake_gemini(*, prompt: str, image_paths: list, timeout_s: int = 120):
        # Queue runs out → default to pass so the loop terminates.
        text = gemini_q.pop(0) if gemini_q else make_gemini_verdict()
        return _FakeCLIResponse(text=text)

    def fake_nb_pro(*, output_path, cache_dir, **_kwargs) -> NBProResponse:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(_tiny_png())
        return NBProResponse(
            output_path=output_path,
            cache_key="fixture",
            cache_hit=False,
            stub_fallback=True,
            exit_code=0,
        )

    monkeypatch.setattr(
        "pipeline.agents.character_designer.invoke_opus_text", fake_opus,
    )
    monkeypatch.setattr(
        "pipeline.agents.character_designer.run_gemini_api_with_image", fake_gemini,
    )
    monkeypatch.setattr(
        "pipeline.agents.character_designer.invoke_image_edit", fake_nb_pro,
    )
