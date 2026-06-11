"""P2 — the Runner's pre-built criteria-bundle extension (additive, back-compat).

Runner historically took a single criteria Path (one file). The orchestrator's
per-frame fan needs the MERGED bundle (brief AC.* + every Bible's IR.*) inside
each node's ctx.criteria, plus a combined hash over all source files so a
mutation in ANY of them invalidates the cache. The two new kwargs win when
provided; the single-path behavior is unchanged otherwise.
"""

from __future__ import annotations

import json

from pipeline.agents import AgentResult, CostEstimate, NODE_REGISTRY, register_node
from pipeline.criteria import CriteriaBundle, AcceptanceCriterion, load_criteria
from pipeline.dag import Graph, Node, Runner


def _probe_node(seen: list):
    NODE_REGISTRY.pop("criteria_probe", None)

    @register_node("criteria_probe")
    class _Probe:
        name = "criteria_probe"
        inputs = {"x": str}
        outputs = {"y": str}
        cites_criteria: list[str] = []

        def cost_estimate(self, ctx):
            return CostEstimate(usd=0.0, latency_s=0.001)

        def run(self, ctx):
            seen.append(ctx.criteria)
            return AgentResult(outputs={"y": "ok"})

    return _Probe


def _graph():
    return Graph(
        nodes=[Node(id="p", node_name="criteria_probe", config={},
                    input_bindings={"x": "literal:hi"})],
        edges=[],
    )


def test_runner_accepts_prebuilt_bundle(tmp_path):
    seen: list = []
    _probe_node(seen)
    bundle = CriteriaBundle(
        version="1.2", locked=True,
        criteria=[AcceptanceCriterion(id="IR.al.style.line-weight", description="x",
                                      cites_phase=(5,), cites_personas=("em",),
                                      character_id="al")],
    )

    runner = Runner(run_dir=tmp_path, manifest={}, criteria=None,
                    criteria_bundle=bundle, criteria_hash="abc123")
    results = runner.execute(_graph())

    assert results["p"].outputs["y"] == "ok"
    assert seen[0] is bundle  # the merged bundle reaches ctx.criteria untouched


def test_runner_criteria_hash_override_changes_cache_key(tmp_path):
    seen: list = []
    _probe_node(seen)
    bundle = CriteriaBundle(version="1.2", locked=True, criteria=[])

    for h in ("hash-one", "hash-two", "hash-one"):
        runner = Runner(run_dir=tmp_path, manifest={}, criteria=None,
                        criteria_bundle=bundle, criteria_hash=h)
        runner.execute(_graph())

    # two distinct hashes -> two sidecars; the third run cache-hits the first
    sidecars = list((tmp_path / ".cache").glob("*.json"))
    assert len(sidecars) == 2
    assert len(seen) == 2  # only two live runs


def test_runner_backcompat_single_path_param_unchanged(tmp_path):
    seen: list = []
    _probe_node(seen)
    criteria_path = tmp_path / "acceptance_criteria.json"
    criteria_path.write_text(json.dumps({
        "version": "1.1", "locked": False,
        "criteria": [{"id": "AC.technical.aspect-ratio-16-9", "description": "x",
                      "cites_phase": [5], "cites_personas": ["em"]}],
    }))

    runner = Runner(run_dir=tmp_path, manifest={}, criteria=criteria_path)
    runner.execute(_graph())

    expected = load_criteria(criteria_path)
    assert [c.id for c in seen[0].criteria] == [c.id for c in expected.criteria]

    # and criteria=None still means no bundle
    seen2: list = []
    _probe_node(seen2)
    Runner(run_dir=tmp_path / "r2", manifest={}, criteria=None).execute(_graph())
    assert seen2[0] is None
