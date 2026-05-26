"""anima — hand-rolled DAG runner with content-addressed cache + hooks.

Per docs/2026-05-24-pipeline-v2-change-map.md §6: ~300–500 LOC, no Prefect/
Dagster. The runner instantiates nodes from pipeline.agents.NODE_REGISTRY,
threads AgentContext through the graph, caches outputs at runs/{run_id}/
.cache/{sha256}.json sidecars, and fires post-run hooks for museum capture
+ eval recorders (which land in commits 6 / 8b / 9b — this commit ships the
hook system; nothing subscribes yet).

The graph itself is declared in manifest.yaml's phases.{phase}.nodes: block
(commit 4 schema). The runner loads it via load_graph_from_manifest().

Input bindings: each Node declares input_bindings — a dict mapping input
port name to a source spec. Three spec forms:

  - "literal:foo"                     → the literal string "foo"
  - "node:a.mid"                      → output port "mid" of node "a"
  - "manifest:generation.aspect_ratio" → manifest.lock.yaml dotted-path lookup
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import yaml

from pipeline.agents import (
    AgentContext,
    AgentResult,
    NODE_REGISTRY,
    Tier,
)
from pipeline.criteria import load_criteria


# ---------- Graph types ----------

@dataclass(frozen=True)
class Edge:
    from_id: str
    to_id: str


@dataclass
class Node:
    id: str
    node_name: str
    config: dict
    input_bindings: dict[str, str] = field(default_factory=dict)
    tier: Tier = "draft"


@dataclass
class Graph:
    nodes: list[Node]
    edges: list[Edge]

    def by_id(self) -> dict[str, Node]:
        return {n.id: n for n in self.nodes}


class CycleDetected(RuntimeError):
    """Raised when topological_sort finds a cycle. Message names the unresolved set."""


# ---------- Topological sort (Kahn's algorithm) ----------

def topological_sort(graph: Graph) -> list[Node]:
    incoming: dict[str, int] = {n.id: 0 for n in graph.nodes}
    successors: dict[str, list[str]] = defaultdict(list)
    for e in graph.edges:
        successors[e.from_id].append(e.to_id)
        incoming[e.to_id] += 1

    by_id = graph.by_id()
    ready = deque(sorted(nid for nid, c in incoming.items() if c == 0))
    out: list[Node] = []
    while ready:
        nid = ready.popleft()
        out.append(by_id[nid])
        for s in sorted(successors[nid]):
            incoming[s] -= 1
            if incoming[s] == 0:
                ready.append(s)
    if len(out) != len(graph.nodes):
        unresolved = [nid for nid, c in incoming.items() if c > 0]
        raise CycleDetected(
            f"DAG contains a cycle involving: {', '.join(sorted(unresolved))}"
        )
    return out


# ---------- Cache key derivation ----------

def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def cache_key(
    *,
    node_name: str,
    config: dict,
    inputs: dict[str, Any],
    tier: Tier,
    criteria_hash: str,
) -> str:
    """Deterministic key for one node invocation. SHA-256 over:

      - node_name
      - config (sorted JSON)
      - resolved inputs (sorted JSON; file paths replaced with content hash)
      - tier (draft|pro)
      - criteria_hash (sha256 of acceptance_criteria.json or "" if none)

    Changing any of these invalidates the cache for this node AND every
    downstream node (because downstream sees a different input value too).
    """
    h = hashlib.sha256()
    h.update(node_name.encode("utf-8"))
    h.update(b"\x00")
    h.update(json.dumps(config, sort_keys=True, default=str).encode("utf-8"))
    h.update(b"\x00")

    normalized_inputs: dict[str, str] = {}
    for k in sorted(inputs):
        v = inputs[k]
        try:
            is_file = isinstance(v, (str, Path)) and Path(v).is_file()
        except (OSError, ValueError):
            is_file = False
        if is_file:
            normalized_inputs[k] = f"file_sha256:{_hash_file(Path(v))}"
        else:
            normalized_inputs[k] = json.dumps(v, sort_keys=True, default=str)
    h.update(json.dumps(normalized_inputs, sort_keys=True).encode("utf-8"))
    h.update(b"\x00")
    h.update(tier.encode("utf-8"))
    h.update(b"\x00")
    h.update(criteria_hash.encode("utf-8"))
    return h.hexdigest()


def hash_criteria_file(path: Path | None) -> str:
    if path is None or not Path(path).exists():
        return ""
    return _hash_file(Path(path))


# ---------- Input binding resolution ----------

def _resolve_bindings(
    bindings: dict[str, str],
    upstream_results: dict[str, AgentResult],
    manifest: dict,
) -> dict[str, Any]:
    resolved: dict[str, Any] = {}
    for port, spec in bindings.items():
        if spec.startswith("literal:"):
            resolved[port] = spec[len("literal:"):]
        elif spec.startswith("node:"):
            node_id, _, output_port = spec[len("node:"):].partition(".")
            if node_id not in upstream_results:
                raise ValueError(
                    f"Binding {spec!r} references unknown upstream {node_id!r}"
                )
            resolved[port] = upstream_results[node_id].outputs[output_port]
        elif spec.startswith("manifest:"):
            dotted = spec[len("manifest:"):]
            cursor: Any = manifest
            for part in dotted.split("."):
                cursor = cursor[part]
            resolved[port] = cursor
        else:
            raise ValueError(
                f"Binding spec {spec!r} must start with literal:, node:, or manifest:"
            )
    return resolved


# ---------- Runner ----------

HookName = str
HookFn = Callable[[str, AgentResult], None]


class Runner:
    def __init__(
        self,
        *,
        run_dir: Path,
        manifest: dict,
        criteria: Path | None = None,
        max_workers: int = 4,
    ):
        self.run_dir = Path(run_dir)
        self.manifest = manifest
        self.criteria_path = criteria
        self.cache_dir = self.run_dir / ".cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.max_workers = max_workers
        self._criteria_bundle = load_criteria(criteria) if criteria else None
        self._criteria_hash = hash_criteria_file(criteria)
        self._hooks: dict[HookName, list[HookFn]] = defaultdict(list)

    def add_hook(self, name: HookName, fn: HookFn) -> None:
        self._hooks[name].append(fn)

    def _fire(self, name: HookName, node_id: str, result: AgentResult) -> None:
        for fn in self._hooks[name]:
            try:
                fn(node_id, result)
            except Exception as e:
                # Hooks are observers — they must not crash the run.
                # Museum capture or eval recorders failing should log, not abort.
                print(
                    f"[dag] hook {fn.__name__!r} for {node_id!r} failed: {e}",
                    file=sys.stderr,
                )

    def execute(self, graph: Graph) -> dict[str, AgentResult]:
        results: dict[str, AgentResult] = {}
        topological_sort(graph)  # validate (raises CycleDetected if bad)
        pred: dict[str, set[str]] = defaultdict(set)
        for e in graph.edges:
            pred[e.to_id].add(e.from_id)

        remaining = list(graph.nodes)
        completed: set[str] = set()
        while remaining:
            ready = [n for n in remaining if pred[n.id].issubset(completed)]
            if not ready:
                raise RuntimeError(
                    f"Runner stuck: remaining={[n.id for n in remaining]}"
                )
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=min(self.max_workers, len(ready))
            ) as pool:
                futures = {
                    pool.submit(self._run_one, n, results): n
                    for n in ready
                }
                for fut in concurrent.futures.as_completed(futures):
                    n = futures[fut]
                    results[n.id] = fut.result()
                    completed.add(n.id)
            remaining = [n for n in remaining if n.id not in completed]
        return results

    def _run_one(
        self, n: Node, upstream: dict[str, AgentResult]
    ) -> AgentResult:
        node_cls = NODE_REGISTRY[n.node_name]
        inputs = _resolve_bindings(n.input_bindings, upstream, self.manifest)
        key = cache_key(
            node_name=n.node_name, config=n.config, inputs=inputs,
            tier=n.tier, criteria_hash=self._criteria_hash,
        )
        sidecar = self.cache_dir / f"{key}.json"
        if sidecar.exists():
            cached = json.loads(sidecar.read_text(encoding="utf-8"))
            result = AgentResult(
                outputs=cached["outputs"],
                tier=cached.get("tier", "draft"),
                cites_criteria=cached.get("cites_criteria", []),
                notes=cached.get("notes", "[cache hit]"),
            )
            self._fire("post_run", n.id, result)
            return result

        ctx = AgentContext(
            run_dir=self.run_dir,
            inputs=inputs,
            manifest=self.manifest,
            criteria=self._criteria_bundle,
            tier=n.tier,
            cache_dir=self.cache_dir,
        )
        result = node_cls().run(ctx)
        sidecar.write_text(
            json.dumps(
                {
                    "outputs": result.outputs,
                    "tier": result.tier,
                    "cites_criteria": result.cites_criteria,
                    "notes": result.notes,
                },
                default=str,
                indent=2,
            ),
            encoding="utf-8",
        )
        self._fire("post_run", n.id, result)
        return result


# ---------- Manifest → Graph ----------

def load_graph_from_manifest(manifest: dict) -> Graph:
    """Reads manifest['phases'][*]['nodes'] and assembles a Graph.

    Each node entry:
      - id: str (unique across the whole manifest)
      - node: str (NODE_REGISTRY key)
      - config: dict (optional, default {})
      - inputs: dict of port → binding spec (optional, default {})
      - depends_on: list of upstream node ids (optional, default [])
      - tier: draft | pro (optional, default "draft")

    Phase membership is metadata only at runtime; the DAG is the source of truth.
    """
    nodes: list[Node] = []
    edges: list[Edge] = []
    seen_ids: set[str] = set()
    phases = manifest.get("phases", {}) or {}
    for phase_key, phase_block in phases.items():
        if phase_key == "enabled" or not isinstance(phase_block, dict):
            continue
        for entry in phase_block.get("nodes", []) or []:
            nid = entry["id"]
            if nid in seen_ids:
                raise ValueError(f"Duplicate node id {nid!r}")
            seen_ids.add(nid)
            nodes.append(
                Node(
                    id=nid,
                    node_name=entry["node"],
                    config=entry.get("config", {}) or {},
                    input_bindings=entry.get("inputs", {}) or {},
                    tier=entry.get("tier", "draft"),
                )
            )
            for upstream in entry.get("depends_on", []) or []:
                edges.append(Edge(from_id=upstream, to_id=nid))
    return Graph(nodes=nodes, edges=edges)


# ---------- CLI ----------

def _make_run_dir() -> Path:
    p = Path("runs") / f"run_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}"
    p.mkdir(parents=True, exist_ok=True)
    return p


def run_from_legacy_cli(node_id: str, argv: list[str]) -> int:
    """Shim called by pipeline/generate.py main() etc. when USE_DAG_RUNNER=1.

    Loads manifest, builds graph, runs everything declared. Surgical
    target selection (single-node + upstream) is a commit-5 refinement;
    for commit 4 we run the whole declared graph.
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--manifest", default="manifest.yaml")
    parser.add_argument("--run-dir", default=None)
    parser.add_argument(
        "--force-criteria-mutation",
        action="store_true",
        help="Allow mutating a locked acceptance_criteria.json. Audited.",
    )
    args, _unknown = parser.parse_known_args(argv)
    # Import nodes so the @register_node decorators populate NODE_REGISTRY
    # before load_graph_from_manifest tries to resolve node names.
    import pipeline.nodes  # noqa: F401

    manifest = yaml.safe_load(Path(args.manifest).read_text(encoding="utf-8"))
    run_dir = Path(args.run_dir) if args.run_dir else _make_run_dir()
    criteria_path: Path | None = None
    ac_block = manifest.get("acceptance_criteria") or {}
    if ac_block.get("path"):
        cp = Path(ac_block["path"])
        if cp.exists():
            criteria_path = cp
    runner = Runner(run_dir=run_dir, manifest=manifest, criteria=criteria_path)
    graph = load_graph_from_manifest(manifest)
    runner.execute(graph)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pipeline.dag")
    sub = parser.add_subparsers(dest="cmd", required=True)
    run_p = sub.add_parser("run", help="Execute the DAG declared in the manifest.")
    run_p.add_argument("--manifest", default="manifest.yaml")
    run_p.add_argument("--run-dir", default=None)
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])
    if args.cmd == "run":
        return run_from_legacy_cli(node_id="", argv=sys.argv[1:])
    return 1


if __name__ == "__main__":
    sys.exit(main())
