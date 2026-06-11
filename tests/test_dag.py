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
    _resolve_bindings,
    cache_key,
    load_graph_from_manifest,
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


# ---- Input binding resolution ----

def test_resolve_bindings_literal_is_string():
    out = _resolve_bindings({"p": "literal:hello"}, {}, {})
    assert out["p"] == "hello"


def test_resolve_bindings_node_pulls_upstream_output():
    upstream = {"a": AgentResult(outputs={"mid": "X"})}
    out = _resolve_bindings({"p": "node:a.mid"}, upstream, {})
    assert out["p"] == "X"


def test_resolve_bindings_manifest_dotted_path():
    manifest = {"generation": {"aspect_ratio": "16:9"}}
    out = _resolve_bindings({"p": "manifest:generation.aspect_ratio"}, {}, manifest)
    assert out["p"] == "16:9"


def test_resolve_bindings_literal_json_list():
    # The Flo-C impedance fix: a node entry can bind a real list-valued input
    # (e.g. FloNode's `references`) inline.
    out = _resolve_bindings(
        {"refs": 'literal_json:["a.png", "b.png"]'}, {}, {}
    )
    assert out["refs"] == ["a.png", "b.png"]


def test_resolve_bindings_literal_json_int():
    out = _resolve_bindings({"n": "literal_json:6"}, {}, {})
    assert out["n"] == 6
    assert isinstance(out["n"], int)


def test_resolve_bindings_literal_json_malformed_raises():
    with pytest.raises(ValueError):
        _resolve_bindings({"x": "literal_json:[not valid json"}, {}, {})


def test_resolve_bindings_unknown_spec_raises():
    with pytest.raises(ValueError):
        _resolve_bindings({"x": "bogus:thing"}, {}, {})


# ---- Flo Phase-5 declarative dispatch (integration smoke) ----

def test_flo_phase5_graph_dispatches_via_dag(tmp_path, monkeypatch):
    """Flo-C seam: a declared phases.phase_5.nodes graph (one hero→nb_pro, one
    standard→nb2) dispatches through load_graph_from_manifest → Runner, with
    list-valued `references` bound inline via literal_json:. Stub-green — the
    nb_pro + nb2 transports are faked so no real call fires."""
    # Import here so the @register_node('flo') side effect is registered.
    import pipeline.nodes  # noqa: F401
    import pipeline.agents.frame_router as fr
    from pipeline import generate as legacy_generate
    from pipeline.agents.nb_pro_runner import NBProResponse

    nb_pro_calls: list[dict] = []

    def fake_invoke(**kwargs):
        nb_pro_calls.append(kwargs)
        out = Path(kwargs["output_path"])
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(b"png")
        return NBProResponse(
            output_path=out, cache_key="k", cache_hit=False,
            stub_fallback=True, exit_code=0,
        )

    monkeypatch.setattr(fr, "invoke_image_edit", fake_invoke)

    nb2_calls: list[dict] = []

    def fake_generate_frame(*, frame_num, prompt, references, manifest, run_dir):
        nb2_calls.append({"frame_num": frame_num, "references": references})
        out = Path(run_dir) / "candidates" / f"F{frame_num:02d}" / "attempt_01.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(b"png")
        return out

    monkeypatch.setattr(legacy_generate, "generate_frame", fake_generate_frame)

    manifest = {
        "generation": {
            "routing": {
                "hero_keyframe": {
                    "transport": "nb_pro",
                    "model": "gemini-3-pro-image-preview",
                    "usd_per_frame": 0.15,
                    "tier": "pro",
                    "status": "wired",
                },
                "standard_keyframe": {
                    "transport": "nb2",
                    "model": "gemini-3.1-flash-image-preview",
                    "usd_per_frame": 0.07,
                    "tier": "draft",
                    "status": "wired",
                },
            },
            "fallback": "nb2",
        },
        "characters": {
            "sean-anchor": {
                "folder": "characters/sean-anchor/",
                "style_register": "pencil-test-colored",
            }
        },
        "phases": {
            "phase_5": {
                "nodes": [
                    {
                        "id": "f06_flo",
                        "node": "flo",
                        "tier": "pro",
                        "inputs": {
                            "frame_num": "literal_json:6",
                            "prompt": "literal:glance down",
                            "references": 'literal_json:["characters/sean-anchor/anchor.png"]',
                            "shot_type": "literal:hero_keyframe",
                            "character_id": "literal:sean-anchor",
                        },
                    },
                    {
                        "id": "f10_flo",
                        "node": "flo",
                        "tier": "draft",
                        "inputs": {
                            "frame_num": "literal_json:10",
                            "prompt": "literal:idle hold",
                            "references": 'literal_json:["characters/sean-anchor/anchor.png"]',
                            "shot_type": "literal:standard_keyframe",
                            "character_id": "literal:sean-anchor",
                        },
                    },
                ]
            }
        },
    }

    graph = load_graph_from_manifest(manifest)
    assert {n.id for n in graph.nodes} == {"f06_flo", "f10_flo"}

    runner = Runner(run_dir=tmp_path, manifest=manifest, criteria=None)
    results = runner.execute(graph)

    # Hero → nb_pro, rendered 16:9 (HF01), references parsed as a real 1-element
    # list (literal_json) — NOT a char-iterated string.
    assert len(nb_pro_calls) == 1
    assert nb_pro_calls[0]["aspect_ratio"] == "16:9"
    assert [str(p) for p in nb_pro_calls[0]["reference_images"]] == [
        "characters/sean-anchor/anchor.png"
    ]
    assert "nb_pro" in results["f06_flo"].notes
    assert "hero_keyframe" in results["f06_flo"].notes
    assert Path(results["f06_flo"].outputs["candidate_path"]).exists()

    # Standard → nb2, references a real 1-element list, no real call fired.
    assert len(nb2_calls) == 1
    assert nb2_calls[0]["references"] == ["characters/sean-anchor/anchor.png"]
    assert "nb2" in results["f10_flo"].notes
    assert Path(results["f10_flo"].outputs["candidate_path"]).exists()
