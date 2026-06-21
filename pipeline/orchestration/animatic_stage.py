"""ANIMATIC stage — the opt-in placement gate between STORYBOARD and GENERATE.

PHILOSOPHY's one non-negotiable belief made structural: the human blocks
placement (where everyone stands, which way they face, scale, leg count) and
timing (holds) by hand, in rough shapes, BEFORE a frame is drawn. The 2026-06-18
kickflip spike proved the bet (a placement rough makes NB2 respect placement
while identity holds) — see docs/anima-test-runs/2026-06-18-animatic-spike-field-report.md.

This is a human author-and-ingest gate, structurally a twin of the storyboard
curation gate but with NO LLM call — Sean draws the roughs:

  storyboard-approve (board locked, animatic_enabled)
     -> ANIMATIC: run_animatic_stage pauses; makes runs/<id>/animatic/
          -> Sean drops frame-named roughs (F01.png ...) + an optional holds.json
     -> approve-animatic: ingest_animatic validates each rough names a real frame
          + the sidecar parses; populates run-state refs + holds (the LOCKED board
          is never mutated); -> the shared generate_stage.enter_generate

Opt-in, default off. A run without it goes STORYBOARD -> GENERATE byte-identical
to today; a back-compat brief (carrying shots.yaml) never enters ANIMATIC.

DEFERRED (design lock): the `post_animatic` T3 critic gate. Its job is to validate
a TIMING arc before tens of dollars of downstream Seedance burn — but v1 has no
orchestrated Motion (no burn to protect) and the human just authored + eyed the
roughs. The manifest seam (critics.placement.post_animatic: T3) stays declared
and the hook point is marked below; PROMOTION TRIGGER: when the timing animatic
feeds an orchestrated Motion phase. The deterministic ingest below is plumbing,
not a critic, and runs at the gate regardless.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from pipeline.criteria import load_all_criteria
from pipeline.orchestration import generate_stage
from pipeline.orchestration import state as st

# Frame-named placement rough: F<id>.<ext>, padding-insensitive (F1 == F01).
_ROUGH_RE = re.compile(r"^F(\d+)\.(png|jpg|jpeg)$", re.IGNORECASE)
_HOLDS_SIDECAR = "holds.json"


def ingest_animatic(shot_ids: set[int], animatic_dir: Path) -> tuple[dict[str, str], dict[str, int]]:
    """Deterministic ingest of a run's animatic directory.

    Returns (refs, holds): refs maps str(frame_id) -> rough path (per-frame
    optional — a frame with no rough is simply absent); holds maps str(frame_id)
    -> hold int from the optional holds.json sidecar. Raises ValueError on a
    rough/hold that names a frame not in the board, a malformed sidecar, or a
    non-positive hold. Never mutates anything — the caller persists into run-state.
    """
    animatic_dir = Path(animatic_dir)
    refs: dict[str, str] = {}
    for p in sorted(animatic_dir.iterdir()):
        if not p.is_file() or p.name == _HOLDS_SIDECAR:
            continue
        m = _ROUGH_RE.match(p.name)
        if not m:
            # Tolerate stray files (notes, source roughs) but warn on image files
            # that miss the convention — a likely naming typo.
            if p.suffix.lower() in (".png", ".jpg", ".jpeg"):
                print(f"  note: ignoring {p.name} — not a frame-named rough "
                      f"(expected F<id>.png, e.g. F01.png)")
            continue
        fid = int(m.group(1))
        if fid not in shot_ids:
            raise ValueError(
                f"animatic rough {p.name} names frame {fid}, which is not in the "
                f"board (frames: {sorted(shot_ids)})"
            )
        refs[str(fid)] = str(p)

    holds: dict[str, int] = {}
    sidecar = animatic_dir / _HOLDS_SIDECAR
    if sidecar.exists():
        try:
            data = json.loads(sidecar.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise ValueError(f"animatic holds sidecar {sidecar} is not valid JSON: {e}") from e
        if not isinstance(data, dict):
            raise ValueError(
                f"animatic holds sidecar {sidecar} must be a JSON object mapping "
                f"frame id -> hold int"
            )
        for k, v in data.items():
            try:
                fid = int(k)
            except (TypeError, ValueError):
                raise ValueError(f"animatic holds sidecar: key {k!r} is not a frame id") from None
            if fid not in shot_ids:
                raise ValueError(
                    f"animatic holds sidecar names frame {fid}, not in the board "
                    f"(frames: {sorted(shot_ids)})"
                )
            if not isinstance(v, int) or isinstance(v, bool) or v < 1:
                raise ValueError(
                    f"animatic holds sidecar: hold for frame {fid} must be an int >= 1, "
                    f"got {v!r}"
                )
            holds[str(fid)] = v
    return refs, holds


def _board_shot_ids(state: dict) -> set[int]:
    known = {m["ir_namespace"] for m in state["cast"] if m["ir_namespace"]}
    shot_list = generate_stage.load_shots(Path(state["shots_path"]), known_namespaces=known)
    return {s.id for s in shot_list.frames}


def run_animatic_stage(state: dict, manifest: dict, run_dir: Path) -> int:
    """Pause for human authoring. No model call — Sean draws the roughs.

    Makes the run's animatic/ drop directory and prints the author instructions.
    Caller (the storyboard gate) has already advanced the stage to ANIMATIC.
    """
    run_dir = Path(run_dir)
    adir = run_dir / "animatic"
    adir.mkdir(parents=True, exist_ok=True)
    state["animatic"] = {"status": "awaiting", "dir": str(adir), "refs": {}, "holds": {}}
    st.save_state(run_dir, state)

    try:
        ids = sorted(_board_shot_ids(state))
    except (ValueError, OSError):
        ids = []

    print("\nANIMATIC (placement) — human author gate. PHILOSOPHY: the human owns "
          "placement + timing.")
    # Surface the board COUNT explicitly (Fix B): a rough/board mismatch (the
    # 2026-06-21 7-roughs-vs-5-board) is visible BEFORE dropping, not after.
    print(f"  Board has {len(ids)} frame(s).")
    print(f"  Drop one rough per keyframe you want to pin into:\n    {adir}")
    print(f"  Name them by frame id: " + (", ".join(f"F{n:02d}.png" for n in ids[:6]) or "F01.png ...")
          + ("  ..." if len(ids) > 6 else ""))
    print("  Recommended form: a STRIPPED SILHOUETTE (cleaner than a colored rough — "
          "spike 2026-06-18); a colored rough works too. Per-frame OPTIONAL.")
    print("  Optional timing: a holds.json sidecar mapping frame id -> on-twos hold "
          'count, e.g. {"1": 5, "3": 4} (overrides the board holds at ASSEMBLE).')
    print("\nHUMAN GATE — after dropping the roughs:")
    print(f"  python -m pipeline.run --resume {run_dir} --approve-animatic")
    return 0


def approve_animatic_gate(state: dict, manifest: dict, run_dir: Path) -> int:
    run_dir = Path(run_dir)
    if state.get("animatic", {}).get("status") != "awaiting":
        print(
            f"error: animatic status is "
            f"{state.get('animatic', {}).get('status')!r} — nothing to approve.",
            file=sys.stderr,
        )
        return 2

    adir = Path(state["animatic"]["dir"])
    try:
        shot_ids = _board_shot_ids(state)
    except (ValueError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    try:
        refs, holds = ingest_animatic(shot_ids, adir)
    except ValueError as e:
        print(f"error: animatic ingest failed: {e}", file=sys.stderr)
        print(f"  fix the roughs/sidecar in {adir} and re-run --approve-animatic.",
              file=sys.stderr)
        return 2

    if not refs and not holds:
        print("WARNING: no roughs or holds ingested — ANIMATIC is a no-op this run "
              "(generation proceeds exactly as without it).")

    # --- post_animatic T3 critic gate: SEAM (DEFERRED — see module docstring). ---
    # The chairman+council would adjudicate the timing arc here, before any Motion
    # burn exists to protect. Not wired in v1; promote when timing feeds Motion.
    # (No-op placement marker — do NOT wire the council here.)

    state["animatic"]["refs"] = refs
    state["animatic"]["holds"] = holds
    state["animatic"]["status"] = "ingested"

    # Mirror the storyboard gate: re-wire the brief criteria override in-memory +
    # rebuild the merged bundle before entering GENERATE (separate process).
    from pipeline.orchestration.plan_stage import wire_brief_criteria

    wire_brief_criteria(manifest, state["brief_dir"])
    bundle = load_all_criteria(manifest)
    st.save_state(run_dir, state)
    n_refs, n_holds = len(refs), len(holds)
    print(f"animatic approved — ingested {n_refs} placement rough(s) + "
          f"{n_holds} hold override(s); entering GENERATE")
    return generate_stage.enter_generate(state, manifest, bundle, run_dir)
