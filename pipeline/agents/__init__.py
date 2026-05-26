"""anima — AgentSpec Protocol + supporting dataclasses + node registry.

Every pipeline stage (Phase 5 frame_generate, Phase 5 audit_gate, Phase 6
seedance_motion, Phase 8 assemble — and from commit 8 onward, the T2 vision
critic Em and the T3 stack Codie/Annie/Sage/Chairman) satisfies AgentSpec.
The DAG runner in pipeline/dag.py instantiates registered nodes by name,
threads AgentContext through the graph, and reads AgentResult.outputs to
satisfy downstream nodes' inputs.

Patch is the v2-locked stage-not-auto-apply primitive. T2/T3 critics emit
proposed_patches: in AgentResult; the runner writes them to manifest.lock.yaml
as pending entries; Sean reviews them in commit 8's CLI surface.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, ClassVar, Literal, Protocol, runtime_checkable

Tier = Literal["draft", "pro"]
PatchOperation = Literal["set", "append", "delete"]


@dataclass(frozen=True)
class CostEstimate:
    """Static or dynamic cost estimate for one node invocation.

    usd: dollar cost (subscription-absorbed agents pass 0.0).
    latency_s: expected wall-clock seconds.
    confidence: 0.0–1.0; how trustworthy the estimate is. Maya's Phase 0
    cost preview aggregates these across the DAG.
    """
    usd: float
    latency_s: float
    confidence: float = 0.5


@dataclass(frozen=True)
class Patch:
    """A proposed mutation to manifest.lock.yaml from a critic.

    Per v2 lock (brainstorm-v2 §2.5, §6, §10), patches stage — never
    auto-apply. Sean reviews + accepts/rejects via pipeline/cli/patches.py
    (commit 8). The runner writes accepted patches as a new
    manifest.lock.yaml version and re-runs affected downstream nodes only.

    proposed_by carries the persona name so the museum walkthrough credits
    roll attributes the change to the specific critic, not "an agent."
    """
    target: str
    path: str
    operation: PatchOperation
    value: Any
    rationale: str
    proposed_by: str
    cites_criteria: tuple[str, ...] = ()


@dataclass
class AgentContext:
    """What every node sees when run() is called.

    run_dir: runs/{timestamp}/ — where outputs live.
    inputs: resolved by the runner from upstream node outputs + manifest config.
    manifest: parsed manifest.lock.yaml (a snapshot frozen at run start).
    criteria: parsed acceptance_criteria.json (CriteriaBundle) — None if the
              run predates the Phase 0 planner shipping (e.g., pencil-test
              reference runs).
    tier: draft | pro — passed through from manifest tiering: block (commit 5
          will make this drive auto-escalation; for commit 4 it's metadata).
    cache_dir: runs/{run_id}/.cache/ — runner-managed; nodes may write to it
               for intermediate artifacts but don't have to.
    extras: free-form dict for node-specific arguments the runner threads
            through (e.g., manual --prompt overrides).
    """
    run_dir: Path
    inputs: dict[str, Any]
    manifest: dict
    criteria: Any
    tier: Tier
    cache_dir: Path
    extras: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    """What every node returns from run().

    outputs: keyed by output port name (matches the node class's outputs:
             dict). Values are typically file paths (str) or small structured
             dicts; large blobs go through the cache layer, not this field.
    tier: which tier actually ran. Defaults to "draft". Commit 5 reads this
          to decide whether to escalate.
    proposed_patches: stage-not-apply. Always empty for non-critic nodes;
                      T2/T3 critics in commits 8 + 9 populate it.
    cites_criteria: criteria IDs this run referenced. T1 rule gates leave
                    empty; T2/T3 critics must populate when verdict is
                    fail or borderline.
    actual_cost: post-hoc fill — useful for tightening Maya's cost-estimate
                 confidence over time.
    notes: free-form provenance string surfaced in museum capture.
    """
    outputs: dict[str, Any]
    tier: Tier = "draft"
    proposed_patches: list[Patch] = field(default_factory=list)
    cites_criteria: list[str] = field(default_factory=list)
    actual_cost: CostEstimate | None = None
    notes: str = ""


@runtime_checkable
class AgentSpec(Protocol):
    """Every pipeline stage satisfies this. typing.Protocol so node classes
    don't need to inherit — they just declare the right attributes and
    methods. runtime_checkable lets the registry validate at register time.
    """
    name: ClassVar[str]
    inputs: ClassVar[dict[str, type]]
    outputs: ClassVar[dict[str, type]]
    cites_criteria: ClassVar[list[str]]

    def cost_estimate(self, ctx: AgentContext) -> CostEstimate: ...
    def run(self, ctx: AgentContext) -> AgentResult: ...


# Module-level registry. pipeline/nodes/__init__.py imports each node module
# at runtime, triggering the @register_node side-effect that populates this.
NODE_REGISTRY: dict[str, type] = {}


def register_node(name: str):
    """Class decorator. Adds the class to NODE_REGISTRY under `name`.

    Validates AgentSpec conformance at registration time so a malformed node
    is caught at import, not at runtime mid-pipeline.
    """
    def _wrap(cls: type) -> type:
        if name in NODE_REGISTRY:
            raise ValueError(
                f"Node {name!r} already registered as {NODE_REGISTRY[name]!r}"
            )
        try:
            instance = cls()
        except Exception as e:
            raise TypeError(
                f"Node class {cls.__name__} cannot be instantiated with no args: {e}"
            )
        if not isinstance(instance, AgentSpec):
            raise TypeError(
                f"Node class {cls.__name__} does not satisfy AgentSpec Protocol. "
                f"Required: name (str), inputs (dict), outputs (dict), "
                f"cites_criteria (list), cost_estimate(ctx), run(ctx)."
            )
        NODE_REGISTRY[name] = cls
        return cls
    return _wrap
