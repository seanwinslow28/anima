"""SCRIPT stage — drive Sam, stop at the script gate; approve locks the beats.

The Phase-3a half of the authoring chain (mirrors plan_stage.py). Sam
(ScriptwriterNode) reads the brief snapshot's 00_studio_brief.md (+ Maya's
plan.md) and PROPOSES a studio-voice script.md + a structured beats.json — the
Sam->Bea contract. Sean decides at the gate; the agent doesn't pick the beats.

run_script_stage drafts; approve_script_gate locks beats.json (the same code
path as `pipeline.cli script approve`), advances to STORYBOARD, and runs Bea so
the next invocation lands at the curation gate.

$0 stub-green: under --stub (ANIMA_FORCE_STUB) Sam's Opus call falls back to its
deterministic stub; the stub-marker scan refuses to present a stubbed script as
real unless this is an explicit stub run.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pipeline.agents import AgentContext
from pipeline.agents.scriptwriter import ScriptwriterNode  # registers the node
from pipeline.cli.script import approve_script as _lock_beats
from pipeline.orchestration import guards, storyboard_stage
from pipeline.orchestration import state as st


def run_script_stage(state: dict, manifest: dict, run_dir: Path, *, stub: bool) -> int:
    run_dir = Path(run_dir)
    # Fail before spend — smoke the live Opus path before Sam authors (mirrors
    # run_plan_stage). A broken auth fails here, not after a silent stub returns.
    if not stub:
        try:
            guards.smoke_live_opus()
        except guards.GuardError as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
    print(f"\nDriving Sam — Phase 3a script for "
          f"{Path(state.get('brief_src') or state['brief_dir']).name}")
    print("  Opus 4.8 single authoring call -> deterministic structural pass")
    ctx = AgentContext(
        run_dir=run_dir,
        inputs={"brief_dir": state["brief_dir"]},
        manifest=manifest,
        criteria=None,
        tier="draft",
        cache_dir=run_dir / ".cache",
        extras={},
    )
    result = ScriptwriterNode().run(ctx)

    marker = guards.scan_stub_marker(
        [Path(result.outputs["script_path"]), Path(result.outputs["beats_path"])]
    )
    if marker and not stub:
        print(
            "error: Sam's emitted artifacts contain the STUB FALLBACK marker — the\n"
            "  script was NOT really authored. Do not approve it. Fix the SDK/auth and\n"
            "  re-run (or pass --stub for an explicit $0 smoke).",
            file=sys.stderr,
        )
        return 1
    if marker:
        print(
            "WARNING: stub-transport script (--stub) — artifacts carry the STUB\n"
            "  FALLBACK marker. Fine for smokes; never approve as a real script."
        )

    state["script"] = {
        "status": "drafted",
        "script_path": result.outputs["script_path"],
        "beats_path": result.outputs["beats_path"],
        "stub": marker,
    }
    st.save_state(run_dir, state)

    print("\nscript drafted:")
    print(f"  script:  {result.outputs['script_path']}")
    print(f"  beats:   {result.outputs['beats_path']}")
    print("\nHUMAN GATE — review the script + beats, then:")
    print(f"  python -m pipeline.run --resume {run_dir} --approve-script")
    return 0


def approve_script_gate(state: dict, manifest: dict, run_dir: Path) -> int:
    if state.get("script", {}).get("status") != "drafted":
        print(
            f"error: script status is "
            f"{state.get('script', {}).get('status')!r} — nothing to approve.",
            file=sys.stderr,
        )
        return 2

    rc = _lock_beats(state["brief_dir"])  # flip locked=true on beats.json
    if rc != 0:
        return 2

    state["script"]["status"] = "approved"
    st.advance_stage(state, "STORYBOARD")
    st.save_state(run_dir, state)
    print("script approved — beats locked; entering STORYBOARD (Bea)")
    return storyboard_stage.run_storyboard_stage(
        state, manifest, run_dir, stub=state.get("stub", False)
    )
