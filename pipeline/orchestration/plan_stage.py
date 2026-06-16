"""PLAN stage — drive Maya, stop at the plan gate; approve locks criteria.

Generalizes scripts/author_plan.py (seam #1): the guards (live-Opus smoke +
stub-marker scan) live in orchestration.guards; PlannerNode is driven
directly (no Runner — Phase 0 has no criteria yet, no caching wanted, the
three-call ceiling is Maya's own).

approve_plan_gate is seam #8: lock the brief criteria (the same code path as
`pipeline.cli plan approve`), wire criteria_sources.brief_file IN-MEMORY from
the run's brief dir (manifest.yaml on disk is never edited — it stays pinned
to whatever piece it ships with), build the merged bundle once via
load_all_criteria, persist the shot list into state, and enter GENERATE.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pipeline.agents.cost_estimator  # noqa: F401 — registers cost_estimator (Maya calls it)
from pipeline.agents import AgentContext
from pipeline.agents.planner import PlannerNode
from pipeline.cli.plan import approve_plan as _lock_brief_criteria
from pipeline.criteria import load_all_criteria
from pipeline.orchestration import generate_stage, guards
from pipeline.orchestration import state as st


def run_plan_stage(state: dict, manifest: dict, run_dir: Path, *, stub: bool, skip_smoke: bool) -> int:
    if not (stub or skip_smoke):
        try:
            guards.smoke_live_opus()
        except guards.GuardError as e:
            print(f"error: {e}", file=sys.stderr)
            return 1

    print(f"\nDriving Maya — Phase 0 planning for "
          f"{Path(state.get('brief_src') or state['brief_dir']).name}")
    print("  Opus primary -> Sonnet adversarial -> resolve (3-call ceiling)")
    ctx = AgentContext(
        run_dir=Path(run_dir),
        inputs={"brief_dir": state["brief_dir"]},
        manifest=manifest,
        criteria=None,
        tier="draft",
        cache_dir=Path(run_dir) / ".cache",
        extras={},
    )
    result = PlannerNode().run(ctx)

    marker = guards.scan_stub_marker(
        [Path(result.outputs["plan_path"]), Path(result.outputs["production_brief_path"])]
    )
    if marker and not stub:
        print(
            "error: Maya's emitted artifacts contain the STUB FALLBACK marker — the\n"
            "  plan was NOT really authored. Do not approve it. Fix the SDK/auth and\n"
            "  re-run (or pass --stub for an explicit $0 smoke).",
            file=sys.stderr,
        )
        return 1
    if marker:
        print(
            "WARNING: stub-transport plan (--stub) — artifacts carry the STUB FALLBACK\n"
            "  marker. Fine for smokes; never approve as a real plan."
        )

    state["plan"] = {
        "status": "drafted",
        "plan_path": result.outputs["plan_path"],
        "criteria_path": result.outputs["criteria_path"],
        "production_brief_path": result.outputs["production_brief_path"],
        "cost_estimate": result.outputs["cost_estimate"],
        "stub": marker,
    }
    st.save_state(run_dir, state)

    ce = result.outputs["cost_estimate"]
    print("\nplan drafted:")
    print(f"  plan:     {result.outputs['plan_path']}")
    print(f"  criteria: {result.outputs['criteria_path']}")
    print(
        f"  cost:     low ${ce['low_usd']:.2f} / median ${ce['median_usd']:.2f} "
        f"/ high ${ce['high_usd']:.2f}"
    )
    print(f"\nHUMAN GATE — review the plan, then:")
    print(f"  python -m pipeline.run --resume {run_dir} --approve-plan")
    return 0


def wire_brief_criteria(manifest: dict, brief_dir: str) -> None:
    """In-memory criteria_sources.brief_file override — re-applied every invocation."""
    sources = manifest.setdefault("criteria_sources", {})
    sources["brief_file"] = str(Path(brief_dir) / "acceptance_criteria.json")


def approve_plan_gate(state: dict, manifest: dict, run_dir: Path) -> int:
    if state["plan"]["status"] != "drafted":
        print(
            f"error: plan status is {state['plan']['status']!r} — nothing to approve.",
            file=sys.stderr,
        )
        return 2

    rc = _lock_brief_criteria(state["brief_dir"])
    if rc != 0:
        return 2

    wire_brief_criteria(manifest, state["brief_dir"])
    bundle = load_all_criteria(manifest)
    state["plan"]["status"] = "approved"

    # Back-compat (a brief that carries a shots.yaml): enter GENERATE now. The
    # authoring branch (needs_storyboard) lands in step 3 — SCRIPT then STORYBOARD,
    # with enter_generate reached at the storyboard gate instead.
    print("plan approved — criteria locked; entering GENERATE")
    return generate_stage.enter_generate(state, manifest, bundle, run_dir)
