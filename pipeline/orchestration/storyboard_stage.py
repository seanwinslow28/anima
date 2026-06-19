"""STORYBOARD stage — drive Bea, stop at the curation gate; approve enters GENERATE.

The Phase-3b half of the authoring chain (mirrors plan_stage.py). Bea
(StoryboardArtistNode) reads Sam's approved beats.json (+ the brief) and
PROPOSES a studio-voice storyboard.md + a DRAFT shots.yaml (born unlocked) — the
GENERATE stage's machine input. Sean curates the draft shots.yaml between the
stage running and the approve.

run_storyboard_stage drafts and establishes state["shots_path"]. The approve is
the CURATION GATE: it re-validates the (human-edited) shots.yaml against
beats.json — load_shots + storyboard_validate (coverage, no orphans, the
beat.cast subset-of shot.cast conflict check) — and refuses to lock a broken
board. On a pass it locks the board, re-wires the brief criteria in-memory +
rebuilds the bundle (this gate runs in a separate process from the plan gate),
and hands off to generate_stage.enter_generate.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pipeline.agents import AgentContext
from pipeline.agents.storyboard_artist import StoryboardArtistNode  # registers the node
from pipeline.cli.storyboard import approve_storyboard as _validate_and_lock_board
from pipeline.criteria import load_all_criteria
from pipeline.orchestration import generate_stage, guards
from pipeline.orchestration import state as st


def run_storyboard_stage(state: dict, manifest: dict, run_dir: Path, *, stub: bool) -> int:
    run_dir = Path(run_dir)
    # Fail before spend — smoke the live Sonnet path before Bea authors (mirrors
    # run_plan_stage). A broken auth fails here, not after a silent stub returns.
    if not stub:
        try:
            guards.smoke_live_sonnet()
        except guards.GuardError as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
    print(f"\nDriving Bea — Phase 3b storyboard for "
          f"{Path(state.get('brief_src') or state['brief_dir']).name}")
    print("  Sonnet 4.6 single authoring call -> deterministic validation pass")
    ctx = AgentContext(
        run_dir=run_dir,
        inputs={"brief_dir": state["brief_dir"]},
        manifest=manifest,
        criteria=None,
        tier="draft",
        cache_dir=run_dir / ".cache",
        extras={},
    )
    result = StoryboardArtistNode().run(ctx)

    marker = guards.scan_stub_marker(
        [Path(result.outputs["storyboard_path"]), Path(result.outputs["shots_path"])]
    )
    if marker and not stub:
        print(
            "error: Bea's emitted artifacts contain the STUB FALLBACK marker — the\n"
            "  board was NOT really authored. Do not approve it. Fix the SDK/auth and\n"
            "  re-run (or pass --stub for an explicit $0 smoke).",
            file=sys.stderr,
        )
        return 1
    if marker:
        print(
            "WARNING: stub-transport board (--stub) — artifacts carry the STUB\n"
            "  FALLBACK marker. Fine for smokes; never approve as a real board."
        )

    # Authoring mode establishes shots_path here — the board didn't exist at start.
    state["shots_path"] = result.outputs["shots_path"]
    state["storyboard"] = {
        "status": "drafted",
        "storyboard_path": result.outputs["storyboard_path"],
        "shots_path": result.outputs["shots_path"],
        "stub": marker,
    }
    st.save_state(run_dir, state)

    print("\nstoryboard drafted:")
    print(f"  board:   {result.outputs['storyboard_path']}")
    print(f"  shots:   {result.outputs['shots_path']}")
    print("\nHUMAN GATE (curation) — edit the draft shots.yaml as you like, then:")
    print(f"  curate:  {result.outputs['shots_path']}")
    print(f"  python -m pipeline.run --resume {run_dir} --approve-storyboard")
    return 0


def approve_storyboard_gate(state: dict, manifest: dict, run_dir: Path) -> int:
    if state.get("storyboard", {}).get("status") != "drafted":
        print(
            f"error: storyboard status is "
            f"{state.get('storyboard', {}).get('status')!r} — nothing to approve.",
            file=sys.stderr,
        )
        return 2

    # The curation gate: re-validate the human-edited shots.yaml against beats.json
    # (coverage + no-orphans + beat.cast subset-of shot.cast) and lock only if it
    # passes. A broken board is NOT locked. Reuses Bea's own validator.
    rc = _validate_and_lock_board(state["brief_dir"], state["manifest_path"])
    if rc != 0:
        return 2

    state["storyboard"]["status"] = "approved"

    # Phase 4 fork: with animatic enabled, the board is locked but generation
    # waits on the human placement pass — advance to ANIMATIC and pause. Criteria
    # wiring + the GENERATE entry move to the animatic-approve gate. Default off:
    # straight to GENERATE, byte-identical to pre-Phase-4.
    if state.get("animatic_enabled"):
        from pipeline.orchestration import animatic_stage

        st.advance_stage(state, "ANIMATIC")
        st.save_state(run_dir, state)
        print("storyboard approved — board validated + locked; entering ANIMATIC "
              "(placement gate)")
        return animatic_stage.run_animatic_stage(state, manifest, run_dir)

    # Separate process from the plan gate: re-wire the brief criteria override
    # in-memory and rebuild the merged bundle before entering GENERATE. Imported
    # lazily to avoid a plan_stage -> script_stage -> storyboard_stage cycle.
    from pipeline.orchestration.plan_stage import wire_brief_criteria

    wire_brief_criteria(manifest, state["brief_dir"])
    bundle = load_all_criteria(manifest)
    st.save_state(run_dir, state)
    print("storyboard approved — board validated + locked; entering GENERATE")
    return generate_stage.enter_generate(state, manifest, bundle, run_dir)
