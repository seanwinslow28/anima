"""Maya the Planner — eval suite runner.

Parameterized over evals/planner/cases.yaml. Each case becomes a pytest test
asserting Maya's output against the case's `expected:` block. Cases marked
`is_intentionally_red: true` are documented failure modes — they xfail by
design and the failure is the artifact (per the v2 change-map §7 discipline).

Lift the eval-suite template that 8b (vision-critic) and 9b (cli-critic)
will mirror — case schema, fixture loading, mocked-runner pattern, the
red/green discipline.

Run with: .venv/bin/pytest evals/planner/runner.py -v
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pytest
import yaml

from pipeline.agents import AgentContext, NODE_REGISTRY
import pipeline.nodes  # noqa: F401 — registers planner + cost_estimator

from evals.planner.conftest import make_planning_envelope, make_sonnet_response

CASES = yaml.safe_load(
    (Path(__file__).parent / "cases.yaml").read_text(encoding="utf-8")
)["cases"]


@dataclass
class _FakeResp:
    text: str
    ok: bool = True
    stub_fallback: bool = False
    error: str | None = None


def _patch_runners(monkeypatch, opus_payloads: list[str], sonnet_payloads: list[str]):
    """Patch invoke_opus_text + invoke_sonnet_text with queued responses.

    Returns a counts dict so cases can assert exact call counts per branch.
    """
    opus_q = list(opus_payloads)
    sonnet_q = list(sonnet_payloads)
    counts = {"opus": 0, "sonnet": 0}

    async def fake_opus(**_kwargs):
        counts["opus"] += 1
        if not opus_q:
            raise AssertionError("invoke_opus_text exhausted queued responses")
        return _FakeResp(text=opus_q.pop(0))

    async def fake_sonnet(**_kwargs):
        counts["sonnet"] += 1
        if not sonnet_q:
            raise AssertionError("invoke_sonnet_text exhausted queued responses")
        return _FakeResp(text=sonnet_q.pop(0))

    monkeypatch.setattr("pipeline.agents.planner.invoke_opus_text", fake_opus)
    monkeypatch.setattr("pipeline.agents.planner.invoke_sonnet_text", fake_sonnet)
    return counts


def _build_responses(case: dict) -> tuple[list[str], list[str]]:
    """Translate cases.yaml mocked_responses into raw JSON strings."""
    opus_payloads = []
    for spec in case["mocked_responses"]["opus"]:
        if spec["kind"] == "planning_envelope":
            opus_payloads.append(make_planning_envelope(
                criteria_categories=spec.get("criteria_categories", []),
                revised=spec.get("revised", False),
            ))
        else:
            raise ValueError(f"Unknown opus mocked_response kind: {spec['kind']}")

    sonnet_payloads = []
    for spec in case["mocked_responses"]["sonnet"]:
        sonnet_payloads.append(make_sonnet_response(
            kind=spec["kind"],
            flag_text=spec.get("flag_text", ""),
        ))
    return opus_payloads, sonnet_payloads


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_planner_case(case, tmp_path, fixtures_dir, monkeypatch, request):
    """Run Maya against a fixture brief + manifest; assert against expected block."""
    if case["expected"].get("is_intentionally_red"):
        request.node.add_marker(
            pytest.mark.xfail(
                reason=f"intentionally red: {case['description']}",
                strict=False,
            )
        )

    brief_dir = tmp_path / "briefs" / case["name"]
    brief_dir.mkdir(parents=True)
    brief_src = fixtures_dir / case["fixture_brief"]
    (brief_dir / "00_studio_brief.md").write_text(
        brief_src.read_text(encoding="utf-8"), encoding="utf-8",
    )

    manifest = yaml.safe_load(
        (fixtures_dir / case["fixture_manifest"]).read_text(encoding="utf-8")
    )
    opus_payloads, sonnet_payloads = _build_responses(case)
    counts = _patch_runners(monkeypatch, opus_payloads, sonnet_payloads)

    ctx = AgentContext(
        run_dir=tmp_path,
        inputs={"brief_dir": str(brief_dir)},
        manifest=manifest,
        criteria=None,
        tier="draft",
        cache_dir=tmp_path / ".cache",
    )

    result = NODE_REGISTRY["planner"]().run(ctx)
    expected = case["expected"]

    # Plan emission.
    if expected.get("plan_emitted"):
        assert (brief_dir / "plan.md").exists(), \
            f"{case['name']}: plan.md not emitted"
        assert (brief_dir / "acceptance_criteria.json").exists(), \
            f"{case['name']}: criteria.json not emitted"
        assert (brief_dir / "01_production_brief.md").exists(), \
            f"{case['name']}: production brief not emitted"

    # Criteria count + category coverage.
    criteria = json.loads(
        (brief_dir / "acceptance_criteria.json").read_text(encoding="utf-8")
    )
    if "criteria_min_count" in expected:
        assert len(criteria["criteria"]) >= expected["criteria_min_count"], \
            f"{case['name']}: too few criteria: {len(criteria['criteria'])} < {expected['criteria_min_count']}"

    if "criteria_must_include_categories" in expected:
        present_cats = {c["id"].split(".")[1] for c in criteria["criteria"]}
        for required in expected["criteria_must_include_categories"]:
            assert required in present_cats, \
                f"{case['name']}: missing required category {required!r} (present: {sorted(present_cats)})"

    # Cost band.
    if "cost_estimate_in_range" in expected:
        low, high = expected["cost_estimate_in_range"]
        est = result.outputs["cost_estimate"]
        assert low <= est["median_usd"] <= high, \
            f"{case['name']}: cost ${est['median_usd']:.2f} outside [{low}, {high}]"

    # Call counts.
    if "opus_call_count" in expected:
        assert counts["opus"] == expected["opus_call_count"], \
            f"{case['name']}: opus called {counts['opus']} times, expected {expected['opus_call_count']}"
    if "sonnet_call_count" in expected:
        assert counts["sonnet"] == expected["sonnet_call_count"], \
            f"{case['name']}: sonnet called {counts['sonnet']} times, expected {expected['sonnet_call_count']}"

    # plan.md is always clean markdown (the planner's contract enforces this,
    # but we re-verify here as an eval-level assertion).
    plan = (brief_dir / "plan.md").read_text(encoding="utf-8")
    for ch in "╔═╗║╚╝┌─┐│└┘":
        assert ch not in plan, f"{case['name']}: plan.md contains box char {ch!r}"
