"""Tests for pipeline.dag — topological sort, cache key, runner, hooks."""

from pathlib import Path

import pytest

from pipeline.agents import (
    AgentResult,
    CostEstimate,
    NODE_REGISTRY,
    register_node,
)
from pipeline.dag import (
    CycleDetected,
    Edge,
    Graph,
    Node,
    Runner,
    cache_key,
    topological_sort,
)


def _make_passthrough_node(node_name: str, input_port: str, output_port: str):
    NODE_REGISTRY.pop(node_name, None)

    @register_node(node_name)
    class _N:
        name = node_name
        inputs = {input_port: str}
        outputs = {output_port: str}
        cites_criteria: list[str] = []

        def cost_estimate(self, ctx):
            return CostEstimate(usd=0.0, latency_s=0.001)

        def run(self, ctx):
            return AgentResult(outputs={output_port: ctx.inputs[input_port].upper()})

    return _N


# ---- Topological sort ----

def test_topological_sort_orders_linear_chain():
    a = Node(id="a", node_name="x", config={})
    b = Node(id="b", node_name="x", config={})
    c = Node(id="c", node_name="x", config={})
    g = Graph(
        nodes=[a, b, c],
        edges=[Edge(from_id="a", to_id="b"), Edge(from_id="b", to_id="c")],
    )
    order = topological_sort(g)
    assert [n.id for n in order] == ["a", "b", "c"]


def test_topological_sort_handles_parallel_branches():
    a = Node(id="a", node_name="x", config={})
    b1 = Node(id="b1", node_name="x", config={})
    b2 = Node(id="b2", node_name="x", config={})
    c = Node(id="c", node_name="x", config={})
    g = Graph(
        nodes=[a, b1, b2, c],
        edges=[
            Edge("a", "b1"), Edge("a", "b2"),
            Edge("b1", "c"), Edge("b2", "c"),
        ],
    )
    order = [n.id for n in topological_sort(g)]
    assert order.index("a") < order.index("b1")
    assert order.index("a") < order.index("b2")
    assert order.index("b1") < order.index("c")
    assert order.index("b2") < order.index("c")


def test_topological_sort_raises_on_cycle():
    g = Graph(
        nodes=[Node("a", "x", {}), Node("b", "x", {})],
        edges=[Edge("a", "b"), Edge("b", "a")],
    )
    with pytest.raises(CycleDetected, match="a.*b|b.*a"):
        topological_sort(g)


# ---- Cache key derivation ----

def test_cache_key_changes_when_input_content_changes(tmp_path):
    f1 = tmp_path / "in.txt"
    f1.write_text("hello")
    key1 = cache_key(
        node_name="x", config={}, inputs={"src": str(f1)},
        tier="draft", criteria_hash="abc123",
    )
    f1.write_text("world")
    key2 = cache_key(
        node_name="x", config={}, inputs={"src": str(f1)},
        tier="draft", criteria_hash="abc123",
    )
    assert key1 != key2


def test_cache_key_changes_when_tier_changes(tmp_path):
    f1 = tmp_path / "in.txt"
    f1.write_text("hello")
    key_draft = cache_key(
        node_name="x", config={}, inputs={"src": str(f1)},
        tier="draft", criteria_hash="abc",
    )
    key_pro = cache_key(
        node_name="x", config={}, inputs={"src": str(f1)},
        tier="pro", criteria_hash="abc",
    )
    assert key_draft != key_pro


def test_cache_key_changes_when_criteria_hash_changes(tmp_path):
    f1 = tmp_path / "in.txt"
    f1.write_text("hello")
    k1 = cache_key(
        node_name="x", config={}, inputs={"src": str(f1)},
        tier="draft", criteria_hash="abc",
    )
    k2 = cache_key(
        node_name="x", config={}, inputs={"src": str(f1)},
        tier="draft", criteria_hash="xyz",
    )
    assert k1 != k2


def test_cache_key_stable_across_dict_iteration_order():
    config_a = {"foo": 1, "bar": 2}
    config_b = {"bar": 2, "foo": 1}
    k1 = cache_key(
        node_name="x", config=config_a, inputs={}, tier="draft", criteria_hash="abc",
    )
    k2 = cache_key(
        node_name="x", config=config_b, inputs={}, tier="draft", criteria_hash="abc",
    )
    assert k1 == k2


# ---- Runner ----

def test_runner_executes_linear_chain(tmp_path):
    _make_passthrough_node("upper_a", "src", "mid")
    _make_passthrough_node("upper_b", "mid", "dst")
    try:
        g = Graph(
            nodes=[
                Node("a", "upper_a", {}, input_bindings={"src": "literal:hello"}),
                Node("b", "upper_b", {}, input_bindings={"mid": "node:a.mid"}),
            ],
            edges=[Edge("a", "b")],
        )
        runner = Runner(run_dir=tmp_path, manifest={}, criteria=None)
        results = runner.execute(g)
        assert results["a"].outputs["mid"] == "HELLO"
        assert results["b"].outputs["dst"] == "HELLO"
    finally:
        NODE_REGISTRY.pop("upper_a", None)
        NODE_REGISTRY.pop("upper_b", None)


def test_runner_serves_from_cache_on_unchanged_inputs(tmp_path):
    NodeCls = _make_passthrough_node("upper_c", "src", "dst")
    call_count = {"n": 0}
    original_run = NodeCls.run

    def counting_run(self, ctx):
        call_count["n"] += 1
        return original_run(self, ctx)

    NodeCls.run = counting_run
    try:
        g = Graph(
            nodes=[Node("a", "upper_c", {}, input_bindings={"src": "literal:hello"})],
            edges=[],
        )
        runner = Runner(run_dir=tmp_path, manifest={}, criteria=None)
        runner.execute(g)
        # Re-instantiate to confirm cache is keyed by content, not by Runner identity:
        runner2 = Runner(run_dir=tmp_path, manifest={}, criteria=None)
        runner2.execute(g)
        assert call_count["n"] == 1, "Second execute should have hit cache"
    finally:
        NODE_REGISTRY.pop("upper_c", None)


def test_runner_fires_post_run_hooks(tmp_path):
    _make_passthrough_node("upper_d", "src", "dst")
    try:
        seen: list[tuple[str, AgentResult]] = []

        def hook(node_id, result):
            seen.append((node_id, result))

        g = Graph(
            nodes=[Node("a", "upper_d", {}, input_bindings={"src": "literal:hello"})],
            edges=[],
        )
        runner = Runner(run_dir=tmp_path, manifest={}, criteria=None)
        runner.add_hook("post_run", hook)
        runner.execute(g)
        assert len(seen) == 1
        assert seen[0][0] == "a"
        assert seen[0][1].outputs["dst"] == "HELLO"
    finally:
        NODE_REGISTRY.pop("upper_d", None)
