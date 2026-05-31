from pathlib import Path

import pytest

from pipeline.agents import NODE_REGISTRY, AgentSpec, AgentResult
from pipeline.museum.schema import Exhibit, Decision, Verdict
from pipeline.agents.museum_writer import narrate


def _rich() -> Exhibit:
    return Exhibit(
        exhibit_id="06-expr-neutral", project_slug="character-bible",
        run_slug="2026-05-30-cy-claude-mascot-pencil-bake",
        title="Plate — expressions/neutral.png", kind="plate_verdict",
        persona="cy", date="2026-05-30",
        decision=Decision(outcome="human_gate_required", attempts=3,
                          rationale="NB2 invented a hair tuft; no-hair invariant violated.",
                          rationale_source="plate_verdicts.jsonl"),
        verdict=Verdict(method="dinov2", score=0.8975, model_verdict="fail"),
        cites_criteria=["IR.claude-mascot.anatomy.no-hair"], evidence_completeness="rich")


def _thin() -> Exhibit:
    return Exhibit(
        exhibit_id="approved-keyframes", project_slug="pencil-test",
        run_slug="run_2026-04-04_174805",
        title="Approved keyframes (29)", kind="frame_keyframe",
        persona="human", date="2026-04-04",
        decision=Decision(outcome="approved", rationale="", rationale_source=None),
        evidence_completeness="thin")


def test_museum_writer_registered_and_satisfies_agentspec():
    assert "museum_writer" in NODE_REGISTRY
    assert isinstance(NODE_REGISTRY["museum_writer"](), AgentSpec)


def test_narrate_stub_is_deterministic_and_credential_free(monkeypatch):
    from pipeline.agents import sdk_runners
    monkeypatch.setattr(sdk_runners, "_sdk_available", lambda: False)
    prose1, stub1 = narrate(_rich())
    prose2, stub2 = narrate(_rich())
    assert stub1 and stub2                      # stub path fired (no creds)
    assert prose1 == prose2 and prose1.strip()  # deterministic, non-empty
    # Faithful: it may surface facts the exhibit carries.
    assert "0.8975" in prose1 or "no-hair" in prose1 or "Cy" in prose1


def test_narrate_thin_exhibit_does_not_manufacture_rationale(monkeypatch):
    from pipeline.agents import sdk_runners
    monkeypatch.setattr(sdk_runners, "_sdk_available", lambda: False)
    prose, _ = narrate(_thin())
    # Honest about sparsity; invents no reason.
    assert "sparse" in prose.lower() or "no rationale" in prose.lower() or "not recorded" in prose.lower()
    # Must not fabricate a similarity score or a motive the exhibit lacks.
    assert "0." not in prose                     # no invented decimal score
    assert "because" not in prose.lower()        # no invented causal claim


def test_museum_writer_node_run_returns_agentresult(tmp_path, monkeypatch):
    from pipeline.agents import sdk_runners
    monkeypatch.setattr(sdk_runners, "_sdk_available", lambda: False)
    from pipeline.museum.schema import write_exhibit
    ex = _rich()
    write_exhibit(tmp_path, ex)
    node = NODE_REGISTRY["museum_writer"]()
    result = node.run(_ctx(tmp_path, ex))
    assert isinstance(result, AgentResult)
    assert result.outputs["narrative_path"].endswith("exhibit.md")


def _ctx(tmp_path: Path, ex: Exhibit):
    from pipeline.agents import AgentContext
    return AgentContext(
        run_dir=tmp_path, inputs={"museum_root": str(tmp_path), "exhibit": ex.to_json_dict()},
        manifest={}, criteria=None, tier="draft", cache_dir=tmp_path / ".cache")
