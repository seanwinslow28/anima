"""ASSEMBLE stage — the loop tail.

Writes export/sequence.txt from state (frame_order + holds, the generalized
assembler's full-basename KEY:hold line format), then drives assemble.sh (#13)
through the Runner via the AssembleNode (--slug + --sequence-file), consuming
the #12-normalized approved PNGs. Runs automatically after the last frame
approval; `--resume <run-dir> --assemble` re-runs a failed tail (idempotent —
the assemble node is content-addressed on the sequence file).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pipeline.nodes  # noqa: F401  (registers "assemble")
from pipeline.dag import Graph, Node, Runner
from pipeline.orchestration import state as st


def write_sequence_file(state: dict, run_dir: Path) -> Path:
    export = Path(run_dir) / "export"
    export.mkdir(parents=True, exist_ok=True)
    lines = [
        f"{state['slug']}_F{n:02d}_key:{st.get_hold(state, n)}"
        for n in state["frame_order"]
    ]
    seq = export / "sequence.txt"
    seq.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return seq


def run_assemble_stage(state: dict, manifest: dict, bundle, run_dir: Path) -> int:
    from pipeline.orchestration.generate_stage import combined_criteria_hash

    run_dir = Path(run_dir)
    if state["stage"] != "ASSEMBLE":
        print(
            f"error: assemble only applies in the ASSEMBLE stage (run is at {state['stage']}).",
            file=sys.stderr,
        )
        return 2

    seq = write_sequence_file(state, run_dir)
    state["assemble"]["sequence_file"] = str(seq)
    st.save_state(run_dir, state)

    runner = Runner(
        run_dir=run_dir,
        manifest=manifest,
        criteria=None,
        criteria_bundle=bundle,
        criteria_hash=combined_criteria_hash(manifest),
    )
    node = Node(
        id="assemble_loop",
        node_name="assemble",
        config={},
        input_bindings={
            "run_dir": f"literal:{run_dir}",
            "slug": f"literal:{state['slug']}",
            "sequence_file": f"literal:{seq}",
        },
    )
    try:
        results = runner.execute(Graph(nodes=[node], edges=[]))
    except Exception as e:
        print(f"error: assemble failed: {e}", file=sys.stderr)
        print(f"  re-run with: python -m pipeline.run --resume {run_dir} --assemble",
              file=sys.stderr)
        return 1

    out = results["assemble_loop"].outputs
    state["assemble"]["gif"] = out["gif_path"] or None
    state["assemble"]["webm"] = out["webm_path"] or None
    state["assemble"]["mp4"] = out["mp4_path"] or None
    st.advance_stage(state, "DONE")
    st.save_state(run_dir, state)

    print("\nloop assembled:")
    for kind in ("gif", "webm", "mp4"):
        if state["assemble"][kind]:
            print(f"  {kind}: {state['assemble'][kind]}")
    print("\nrun DONE — Engine Truth is the arbiter: open the loop and watch it play.")
    return 0
