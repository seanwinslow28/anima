"""Tests for pipeline.agents — AgentSpec Protocol + supporting dataclasses."""

from dataclasses import is_dataclass

from pipeline.agents import (
    AgentContext,
    AgentResult,
    AgentSpec,
    CostEstimate,
    NODE_REGISTRY,
    Patch,
    register_node,
)


def test_agentresult_defaults_to_draft_tier_and_empty_patches():
    result = AgentResult(outputs={"frame": "/tmp/f.png"})
    assert result.tier == "draft"
    assert result.proposed_patches == []
    assert result.cites_criteria == []


def test_patch_dataclass_round_trips():
    patch = Patch(
        target="manifest.lock.yaml",
        path="generation.prompt_source",
        operation="set",
        value="prompts/F06_revised.txt",
        rationale="Em flagged style drift on F06; tightening prompt.",
        proposed_by="em-vision-critic",
    )
    assert is_dataclass(patch)
    assert patch.operation in {"set", "append", "delete"}


def test_register_node_populates_registry():
    NODE_REGISTRY.pop("test_dummy", None)

    @register_node("test_dummy")
    class DummyNode:
        name = "test_dummy"
        inputs = {"x": str}
        outputs = {"y": str}
        cites_criteria: list[str] = []

        def cost_estimate(self, ctx):
            return CostEstimate(usd=0.0, latency_s=0.0)

        def run(self, ctx):
            return AgentResult(outputs={"y": ctx.inputs["x"]})

    assert "test_dummy" in NODE_REGISTRY
    assert NODE_REGISTRY["test_dummy"] is DummyNode
    NODE_REGISTRY.pop("test_dummy")


def test_agentspec_is_runtime_checkable():
    class GoodNode:
        name = "good"
        inputs: dict = {}
        outputs: dict = {}
        cites_criteria: list[str] = []

        def cost_estimate(self, ctx):
            return CostEstimate(usd=0.0, latency_s=0.0)

        def run(self, ctx):
            return AgentResult(outputs={})

    assert isinstance(GoodNode(), AgentSpec)

    class BadNode:
        name = "bad"
        # missing inputs/outputs/cites_criteria/cost_estimate/run

    assert not isinstance(BadNode(), AgentSpec)


def test_agentcontext_holds_run_state(tmp_path):
    ctx = AgentContext(
        run_dir=tmp_path,
        inputs={"x": 1},
        manifest={"project": {"name": "anima"}},
        criteria=None,
        tier="draft",
        cache_dir=tmp_path / ".cache",
    )
    assert ctx.run_dir == tmp_path
    assert ctx.inputs == {"x": 1}
    assert ctx.criteria is None
    assert ctx.tier == "draft"
    assert ctx.extras == {}
