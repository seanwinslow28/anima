"""Tests for pipeline.agents.t3_council — the T3 multi-CLI variance council.

Three heterogeneous peers (Codie/production·Codex, Annie/visual·Gemini,
Sage/narrative·Opus) fan out in parallel; a SEPARATE Opus chairman adjudicates.
Stub-green with no credentials. A peer erroring is a contained errored gap,
never a run-abort (the Gate-3 containment lesson).
"""

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
    Patch,
)

# Trigger @register_node("t3_council"):
import pipeline.agents.t3_council  # noqa: F401
from pipeline.agents.cli_runners import RateCapExhausted


@dataclass
class _FakeResp:
    """Stand-in for CLIResponse / GeminiAPIResponse / SDKResponse in tests."""

    text: str
    ok: bool = True
    stub_fallback: bool = False
    error: str | None = None


def _verdict_json(
    *,
    verdict: str = "pass",
    confidence: float = 0.9,
    reasoning: str = "looks fine",
    patches: list[dict] | None = None,
    cites: list[str] | None = None,
) -> str:
    return json.dumps({
        "verdict": verdict,
        "confidence": confidence,
        "reasoning": reasoning,
        "proposed_patches": patches or [],
        "cites_criteria": cites or [],
    })


def _ctx(tmp_path: Path, *, artifact_paths: list[str] | None = None) -> AgentContext:
    if artifact_paths is None:
        img = tmp_path / "frame.png"
        if not img.exists():
            img.write_bytes(b"\x89PNG\r\n\x1a\n")
        artifact_paths = [str(img)]
    return AgentContext(
        run_dir=tmp_path,
        inputs={
            "artifact_paths": artifact_paths,
            "beat_description": "F06: glance down, eyes on stylus",
            "frame_id": "F06",
            "checkpoint": "pre_museum_publish",
            "gate": "pre_museum_publish",
        },
        manifest={
            "critics": {"t3": {"per_call_timeout_s": 10, "wall_budget_s": 60}},
        },
        criteria=None,
        tier="draft",
        cache_dir=tmp_path / ".cache",
    )


def _force_full_stub(monkeypatch):
    """Make every transport take its credential-free stub path."""
    from pipeline.agents import sdk_runners, gemini_api_runner

    monkeypatch.setenv("PATH", "")  # codex absent → stub
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(sdk_runners, "_sdk_available", lambda: False)
    monkeypatch.setattr(gemini_api_runner, "_genai_available", lambda: False)
    monkeypatch.setattr(gemini_api_runner, "_has_gemini_api_key", lambda: False)


def _patch_peers(monkeypatch, *, codie, annie, sage, chairman, seen=None):
    """Patch the four module globals with async stand-ins."""
    async def _mk(label, resp_or_exc):
        if isinstance(resp_or_exc, Exception):
            raise resp_or_exc
        return resp_or_exc

    def _wrap(label, value):
        async def _fn(**kw):
            if seen is not None:
                seen.append(label)
            if isinstance(value, Exception):
                raise value
            return value
        return _fn

    monkeypatch.setattr("pipeline.agents.t3_council.run_codex_with_image", _wrap("codie", codie))
    monkeypatch.setattr("pipeline.agents.t3_council.run_gemini_api_with_image", _wrap("annie", annie))
    monkeypatch.setattr("pipeline.agents.t3_council.invoke_opus_vision", _wrap("sage", sage))
    monkeypatch.setattr("pipeline.agents.t3_council.invoke_opus_text", _wrap("chairman", chairman))


# --------------------------------------------------------------------------- #
# Contract conformance                                                        #
# --------------------------------------------------------------------------- #


def test_t3_council_registered_and_satisfies_agentspec():
    cls = NODE_REGISTRY["t3_council"]
    assert isinstance(cls(), AgentSpec)


def test_full_stub_path_is_green(tmp_path, monkeypatch):
    _force_full_stub(monkeypatch)
    cls = NODE_REGISTRY["t3_council"]
    result = cls().run(_ctx(tmp_path))

    assert isinstance(result, AgentResult)
    assert result.outputs["verdict"] in {"pass", "borderline", "fail"}
    assert set(result.outputs["peer_verdicts"].keys()) == {"codie", "annie", "sage"}
    assert 0.0 <= result.outputs["agreement_score"] <= 1.0
    assert result.outputs["status"] in {"ok", "partial", "error", "success-empty"}


# --------------------------------------------------------------------------- #
# Fan-out + chairman                                                          #
# --------------------------------------------------------------------------- #


def test_fan_out_runs_all_three_peers(tmp_path, monkeypatch):
    seen: list[str] = []
    _patch_peers(
        monkeypatch, seen=seen,
        codie=_FakeResp(_verdict_json(verdict="pass")),
        annie=_FakeResp(_verdict_json(verdict="pass")),
        sage=_FakeResp(_verdict_json(verdict="pass")),
        chairman=_FakeResp(_verdict_json(verdict="pass", cites=["AC01"])),
    )
    cls = NODE_REGISTRY["t3_council"]
    result = cls().run(_ctx(tmp_path))

    assert {"codie", "annie", "sage"} <= set(seen)
    assert set(result.outputs["peer_verdicts"].keys()) == {"codie", "annie", "sage"}


def test_chairman_is_a_separate_call_with_peer_outputs(tmp_path, monkeypatch):
    chairman_prompts: list[str] = []
    chairman_calls = {"n": 0}

    async def codie(**kw):
        return _FakeResp(_verdict_json(verdict="pass", reasoning="CODIE-PRODUCTION-READ"))

    async def annie(**kw):
        return _FakeResp(_verdict_json(verdict="borderline", reasoning="ANNIE-VISUAL-READ", cites=["IR.x"]))

    async def sage(**kw):
        return _FakeResp(_verdict_json(verdict="pass", reasoning="SAGE-NARRATIVE-READ"))

    async def chairman(**kw):
        chairman_calls["n"] += 1
        chairman_prompts.append(kw["prompt"])
        return _FakeResp(_verdict_json(verdict="borderline", reasoning="adjudicated", cites=["AC01"]))

    monkeypatch.setattr("pipeline.agents.t3_council.run_codex_with_image", codie)
    monkeypatch.setattr("pipeline.agents.t3_council.run_gemini_api_with_image", annie)
    monkeypatch.setattr("pipeline.agents.t3_council.invoke_opus_vision", sage)
    monkeypatch.setattr("pipeline.agents.t3_council.invoke_opus_text", chairman)

    cls = NODE_REGISTRY["t3_council"]
    result = cls().run(_ctx(tmp_path))

    # Chairman fired exactly once, as a separate invoke_opus_text call.
    assert chairman_calls["n"] == 1
    # The chairman saw the three peer reads in its prompt (synthesis input).
    prompt = chairman_prompts[0]
    assert "CODIE-PRODUCTION-READ" in prompt
    assert "ANNIE-VISUAL-READ" in prompt
    assert "SAGE-NARRATIVE-READ" in prompt
    # The council verdict is the chairman's adjudication.
    assert result.outputs["verdict"] == "borderline"
    assert "adjudicated" in result.outputs["chairman_note"]


# --------------------------------------------------------------------------- #
# Status promotion + containment                                             #
# --------------------------------------------------------------------------- #


def test_both_clis_capped_promotes_to_partial(tmp_path, monkeypatch):
    _patch_peers(
        monkeypatch,
        codie=RateCapExhausted("codex quota"),
        annie=RateCapExhausted("gemini quota"),
        sage=_FakeResp(_verdict_json(verdict="pass")),
        chairman=_FakeResp(_verdict_json(verdict="pass", cites=["AC01"])),
    )
    cls = NODE_REGISTRY["t3_council"]
    result = cls().run(_ctx(tmp_path))

    assert result.outputs["status"] == "partial"
    assert result.outputs["peer_verdicts"]["codie"]["status"] == "error"
    assert result.outputs["peer_verdicts"]["annie"]["status"] == "error"
    assert result.outputs["peer_verdicts"]["sage"]["status"] == "ok"


def test_all_peers_error_promotes_to_error(tmp_path, monkeypatch):
    _patch_peers(
        monkeypatch,
        codie=RateCapExhausted("x"),
        annie=RuntimeError("boom"),
        sage=RuntimeError("kaboom"),
        chairman=_FakeResp(_verdict_json(verdict="pass", cites=["AC01"])),
    )
    cls = NODE_REGISTRY["t3_council"]
    result = cls().run(_ctx(tmp_path))  # must NOT raise

    assert result.outputs["status"] == "error"
    for name in ("codie", "annie", "sage"):
        assert result.outputs["peer_verdicts"][name]["status"] == "error"


def test_errored_peer_is_contained_no_raise(tmp_path, monkeypatch):
    _patch_peers(
        monkeypatch,
        codie=RuntimeError("codie blew up"),
        annie=_FakeResp(_verdict_json(verdict="pass")),
        sage=_FakeResp(_verdict_json(verdict="pass")),
        chairman=_FakeResp(_verdict_json(verdict="pass", cites=["AC01"])),
    )
    cls = NODE_REGISTRY["t3_council"]
    result = cls().run(_ctx(tmp_path))  # no raise

    assert result.outputs["peer_verdicts"]["codie"]["status"] == "error"
    assert result.outputs["status"] == "partial"


# --------------------------------------------------------------------------- #
# Patch staging + agreement                                                  #
# --------------------------------------------------------------------------- #


def test_patches_carry_proposed_by_peer_and_chairman(tmp_path, monkeypatch):
    annie_patch = [{
        "target": "manifest.lock.yaml",
        "path": "characters.sean.prop_hand",
        "operation": "set",
        "value": "right",
        "rationale": "prop jumped hands",
        "cites_criteria": ["IR.prop"],
    }]
    chairman_patch = [{
        "target": "manifest.lock.yaml",
        "path": "characters.sean.prop_hand",
        "operation": "set",
        "value": "right",
        "rationale": "council promotes Annie's fix",
        "cites_criteria": ["IR.prop"],
    }]
    _patch_peers(
        monkeypatch,
        codie=_FakeResp(_verdict_json(verdict="pass")),
        annie=_FakeResp(_verdict_json(verdict="borderline", patches=annie_patch, cites=["IR.prop"])),
        sage=_FakeResp(_verdict_json(verdict="pass")),
        chairman=_FakeResp(_verdict_json(verdict="borderline", patches=chairman_patch, cites=["IR.prop"])),
    )
    cls = NODE_REGISTRY["t3_council"]
    result = cls().run(_ctx(tmp_path))

    by = {p.proposed_by for p in result.proposed_patches}
    assert "annie" in by
    assert "chairman" in by
    for p in result.proposed_patches:
        assert isinstance(p, Patch)


def test_agreement_score_all_agree_is_one(tmp_path, monkeypatch):
    _patch_peers(
        monkeypatch,
        codie=_FakeResp(_verdict_json(verdict="pass")),
        annie=_FakeResp(_verdict_json(verdict="pass")),
        sage=_FakeResp(_verdict_json(verdict="pass")),
        chairman=_FakeResp(_verdict_json(verdict="pass", cites=["AC01"])),
    )
    cls = NODE_REGISTRY["t3_council"]
    result = cls().run(_ctx(tmp_path))
    assert result.outputs["agreement_score"] == pytest.approx(1.0)


def test_agreement_score_split_is_fractional(tmp_path, monkeypatch):
    _patch_peers(
        monkeypatch,
        codie=_FakeResp(_verdict_json(verdict="pass")),
        annie=_FakeResp(_verdict_json(verdict="pass")),
        sage=_FakeResp(_verdict_json(verdict="fail", cites=["AC01"])),
        chairman=_FakeResp(_verdict_json(verdict="borderline", cites=["AC01"])),
    )
    cls = NODE_REGISTRY["t3_council"]
    result = cls().run(_ctx(tmp_path))
    assert result.outputs["agreement_score"] == pytest.approx(2.0 / 3.0)
