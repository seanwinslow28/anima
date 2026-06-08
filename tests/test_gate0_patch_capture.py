# tests/test_gate0_patch_capture.py
"""G6.9 Gate 0 — Em's proposed_patches must survive capture into the eval harness.

Today the eval DISCARDS the diffs: score.py builds CaseScore from the AgentResult
but never reads result.proposed_patches, and CaseScore has no field to hold them.
This suite locks the wiring end-to-end:
  - CaseScore carries proposed_patches with a safe default,
  - the asdict<->CaseScore(**) subprocess round-trip preserves them,
  - a (stubbed) defect verdict actually populates them through _score_one,
  - the N-run consensus collapse carries them from the verdict-winning run,
  - the pure diff cite precision/recall scorer behaves (P AND R, leaf-normalized).

Credential-free: every Em transport is stubbed, no model call, no GEMINI key.
"""
from __future__ import annotations

import json
from dataclasses import asdict

import pytest
import yaml
from pathlib import Path

from pipeline.agents import AgentContext
from pipeline.agents.vision_critic import VisionCriticNode
from evals.vision_critic.conftest import (
    make_vision_verdict, _FakeCLIResponse, _FakeSDKResponse,
    eval_manifest, merged_criteria,
)
from evals.vision_critic.scoring import CaseScore, diff_cite_precision_recall
from evals.vision_critic.score import consensus_scores, _score_one

_CASES = yaml.safe_load(
    (Path(__file__).resolve().parents[1] / "evals/vision_critic/cases.yaml").read_text(encoding="utf-8")
)["cases"]


def _stub_transports(monkeypatch, verdict_json: str) -> None:
    async def fake_gemini(*, prompt, image_paths, timeout_s=120):
        return _FakeCLIResponse(text=verdict_json)

    async def fake_opus(*, prompt, image_paths, timeout_s=120):
        return _FakeSDKResponse(text=verdict_json)

    monkeypatch.setattr("pipeline.agents.vision_critic.run_antigravity_with_image", fake_gemini)
    monkeypatch.setattr("pipeline.agents.vision_critic.run_gemini_api_with_image", fake_gemini)
    monkeypatch.setattr("pipeline.agents.vision_critic.invoke_opus_vision", fake_opus)


# --------------------------------------------------------------------------- #
# Field + round-trip
# --------------------------------------------------------------------------- #
def test_casescore_has_patches_field_defaulting_empty():
    cs = CaseScore(name="x", case_class="identity_style",
                   expected_verdict="fail", predicted_verdict="fail")
    assert cs.proposed_patches == []


def test_asdict_casescore_roundtrip_preserves_patches():
    """The subprocess boundary serializes asdict(cs) -> JSON -> CaseScore(**...).
    A patch (a plain dict, never a frozen Patch) must survive byte-for-byte."""
    patch = {
        "target": "manifest.lock.yaml", "path": "generation.prompt_clause",
        "operation": "set", "value": "navy-blue crew-neck t-shirt",
        "rationale": "shirt color drifted to red", "proposed_by": "em-vision-critic",
        "cites_criteria": ["IR.sean.costume.navy-tee-cool-gray-jeans"],
    }
    cs = CaseScore(name="palette-pad2", case_class="identity_style",
                   expected_verdict="fail", predicted_verdict="fail",
                   proposed_patches=[patch])
    revived = CaseScore(**json.loads(json.dumps(asdict(cs))))
    assert revived.proposed_patches == [patch]


# --------------------------------------------------------------------------- #
# Production capture path (_score_one) — the site that drops diffs today
# --------------------------------------------------------------------------- #
def test_score_one_captures_diffs_from_defect_verdict(monkeypatch):
    case = next(c for c in _CASES
                if c["case_class"] == "identity_style" and c["expected_verdict"] == "fail")
    stub = make_vision_verdict(verdict="fail", cites=case.get("expected_cites") or None)
    _stub_transports(monkeypatch, stub)
    manifest = eval_manifest()
    criteria = merged_criteria(manifest)

    cs = _score_one(case, manifest, criteria)

    assert cs.proposed_patches, "Em's diff was dropped on the floor (Gate 0 regression)"
    diff = cs.proposed_patches[0]
    assert isinstance(diff, dict) and diff.get("value")
    assert diff.get("cites_criteria")  # a grounded diff carries its citation


def test_pass_verdict_captures_no_diff(monkeypatch):
    case = next(c for c in _CASES if c["case_class"] == "clean")
    _stub_transports(monkeypatch, make_vision_verdict(verdict="pass"))
    manifest = eval_manifest()
    cs = _score_one(case, manifest, merged_criteria(manifest))
    assert cs.proposed_patches == []


# --------------------------------------------------------------------------- #
# N-run consensus collapse carries the diffs from the verdict-winning run
# --------------------------------------------------------------------------- #
def test_consensus_carries_patches_from_winning_run():
    winner_patch = [{"target": "manifest.lock.yaml", "path": "p", "operation": "set",
                     "value": "fix", "rationale": "r", "proposed_by": "em-vision-critic",
                     "cites_criteria": ["IR.sean.palette.x"]}]

    def cs(verdict, patches):
        return CaseScore(name="case-1", case_class="identity_style",
                         expected_verdict="fail", predicted_verdict=verdict,
                         proposed_patches=patches)

    runs = [
        [cs("fail", winner_patch)],   # majority verdict (fail) — its patch must win
        [cs("fail", winner_patch)],
        [cs("borderline", [])],       # loser run — its (empty) patches must NOT win
    ]
    out = consensus_scores(runs)
    assert len(out) == 1
    assert out[0].predicted_verdict == "fail"
    assert out[0].proposed_patches == winner_patch


# --------------------------------------------------------------------------- #
# Pure diff cite precision/recall (distinct from the recall-only verdict scorer)
# --------------------------------------------------------------------------- #
def test_diff_cite_precision_recall_exact_match():
    r = diff_cite_precision_recall(
        predicted_cites=["IR.sean.proportion.head-to-body-1-to-7"],
        expected_cites=["IR.sean.proportion.head-to-body-1-7"])  # format drift recovers
    assert r["precision"] == 1.0 and r["recall"] == 1.0 and r["tp"] == 1


def test_diff_cite_precision_penalizes_irrelevant_cites():
    """A diff citing the 1 right rule + 1 irrelevant rule keeps recall but loses
    precision — the whole reason this scorer is P AND R, not recall-only."""
    r = diff_cite_precision_recall(
        predicted_cites=["IR.sean.proportion.head-to-body-1-to-7", "IR.sean.style.cream-paper"],
        expected_cites=["IR.sean.proportion.head-to-body-1-to-7"])
    assert r["recall"] == 1.0
    assert r["precision"] == 0.5


def test_diff_cite_no_prediction_is_zero_precision_zero_recall():
    r = diff_cite_precision_recall(predicted_cites=[],
                                   expected_cites=["IR.sean.palette.x"])
    assert r["precision"] == 0.0 and r["recall"] == 0.0


def test_diff_cite_recall_none_when_no_expected():
    r = diff_cite_precision_recall(predicted_cites=["IR.sean.palette.x"], expected_cites=[])
    assert r["recall"] is None
