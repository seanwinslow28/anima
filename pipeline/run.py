"""python -m pipeline.run — the one-command run orchestrator (Slice 2).

A resumable stage machine over the existing, proven nodes. Each invocation
reads runs/<id>/run_state.json, advances to the next human gate, prints what
to look at, and exits:

  python -m pipeline.run --brief <dir> [--slug S] [--run-dir <dir>] [--stub]
      # start: derive cast, run PLAN (drive Maya), stop at the plan gate.
      # A brief WITHOUT a shots.yaml is an authoring run (Sam -> Bea draft the
      # board); --slug is required there. A brief WITH a shots.yaml is back-compat.
  python -m pipeline.run --resume <run-dir> --approve-plan
      # back-compat: lock criteria, enter GENERATE. authoring: enter SCRIPT (Sam).
  python -m pipeline.run --resume <run-dir> --approve-script
      # authoring: lock beats.json, run Bea, stop at the storyboard curation gate.
  python -m pipeline.run --resume <run-dir> --approve-storyboard
      # authoring: validate + lock the curated shots.yaml, enter GENERATE.
  python -m pipeline.run --resume <run-dir> --approve-frame N [--attempt K]
      # lock attempt -> approved/, chain + generate N+1 (or assemble if last).
  python -m pipeline.run --resume <run-dir> --retry-frame N --note "<correction>"
      # re-roll frame N with the note appended; stop at its eye gate again.
  python -m pipeline.run --resume <run-dir> --status
      # print state, no advance.

Generalizes the first-integrated-run prototypes (scripts/author_plan.py +
scripts/spark_frame.py) — see docs/2026-06-11-orchestrator-core-build-plan.md.
Run from the repo root: manifest paths, pipeline/assemble.sh, and Em's context
files all resolve CWD-relative. Museum capture is Slice 3.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from datetime import date
from pathlib import Path

import yaml

from pipeline.criteria import load_all_criteria
from pipeline.orchestration import (
    animatic_stage,
    generate_stage,
    plan_stage,
    script_stage,
    storyboard_stage,
)
from pipeline.orchestration import state as st
from pipeline.orchestration.cast import derive_cast
from pipeline.orchestration.shots import read_slug

RUN_SUBDIRS = ("candidates", "approved", "rejected", "audit", "export", ".cache")

# Exported for the dynamic extent of a --stub invocation; every model transport
# gate (sdk_runners, gemini_api_runner, cli_runners) honors it, so a $0 stub
# run can never silently spend — even with the SDK importable, agy on PATH, or
# a populated .env.
FORCE_STUB_ENV = "ANIMA_FORCE_STUB"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m pipeline.run",
        description="Run orchestrator: brief -> plan gate -> per-frame eye gates -> loop.",
    )
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--brief", metavar="DIR",
                      help="Brief dir holding 00_studio_brief.md + shots.yaml — starts a new run.")
    mode.add_argument("--resume", metavar="RUN_DIR",
                      help="Existing run dir holding run_state.json.")
    p.add_argument("--slug", help="Override shots.yaml's slug (recorded at run init).")
    p.add_argument("--run-dir", help="Run output dir (default: runs/{date}-{slug}-run).")
    p.add_argument("--manifest", default="manifest.yaml", help="Manifest path (default manifest.yaml).")
    p.add_argument("--stub", action="store_true",
                   help="Stub-transport run: skip the live-Opus smoke; record plan.stub=true. $0, for tests/smokes.")
    p.add_argument("--animatic", action="store_true",
                   help="Insert the opt-in ANIMATIC placement gate between STORYBOARD and "
                        "GENERATE (also enabled by manifest animatic.enabled). Default off.")
    p.add_argument("--frames", type=int, metavar="N",
                   help="Target loop length: Bea boards N frames and the storyboard gate "
                        "refuses to lock a board that isn't exactly N (the human owns the "
                        "count). Authoring runs only. Absent -> Bea's natural count, "
                        "byte-identical.")
    p.add_argument("--skip-smoke", action="store_true",
                   help="Skip the pre-run live-Opus smoke call (not recommended for costed runs).")
    p.add_argument("--allow-api-key", action="store_true",
                   help="Permit ANTHROPIC_API_KEY set (bills the API, not the subscription). Default: refuse.")
    # --resume actions (exactly one required)
    p.add_argument("--approve-plan", action="store_true",
                   help="Approve the drafted plan: lock criteria, enter GENERATE (or SCRIPT, authoring).")
    p.add_argument("--approve-script", action="store_true",
                   help="Approve the drafted script: lock beats.json, run Bea, enter STORYBOARD.")
    p.add_argument("--approve-storyboard", action="store_true",
                   help="Approve the curated board: validate + lock shots.yaml, enter GENERATE "
                        "(or ANIMATIC, when animatic is enabled).")
    p.add_argument("--approve-animatic", action="store_true",
                   help="Ingest the dropped placement roughs + holds sidecar, then enter GENERATE.")
    p.add_argument("--approve-frame", type=int, metavar="N",
                   help="Approve frame N's attempt (Sean's eye said go).")
    p.add_argument("--attempt", type=int, metavar="K",
                   help="Attempt to approve (default: the latest).")
    p.add_argument("--retry-frame", type=int, metavar="N",
                   help="Re-roll frame N with --note appended to the prompt.")
    p.add_argument("--note", help="Correction note for --retry-frame (required with it). "
                   "Write it as the desired end-state (a positive identity-lock), not the "
                   "defect — it's appended to the prompt, so naming the flaw reinforces it.")
    p.add_argument("--escalate", action="store_true",
                   help="Force Em's Opus read (identity_critical) on the generated attempt.")
    p.add_argument("--assemble", action="store_true",
                   help="(Re-)run the ASSEMBLE tail (it auto-runs after the last approval; "
                        "this retries a failed tail).")
    p.add_argument("--status", action="store_true", help="Print run state; no advance.")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    prior = os.environ.get(FORCE_STUB_ENV)
    try:
        if args.brief:
            return _start(args)
        return _resume(args)
    finally:
        # Scope the force-stub export to this invocation (in-process callers,
        # e.g. tests, must not leak it).
        if prior is None:
            os.environ.pop(FORCE_STUB_ENV, None)
        else:
            os.environ[FORCE_STUB_ENV] = prior


def _api_key_guard(args: argparse.Namespace) -> int:
    # Fleet-ops §0: subscription billing via the claude CLI OAuth, never the API key.
    if os.environ.get("ANTHROPIC_API_KEY") and not args.allow_api_key:
        print(
            "error: ANTHROPIC_API_KEY is set — this would bill the Anthropic API, not\n"
            "  the subscription. Unset it (fleet-ops §1) or pass --allow-api-key.",
            file=sys.stderr,
        )
        return 1
    return 0


def _load_manifest(state: dict) -> dict | None:
    manifest_path = Path(state["manifest_path"])
    if not manifest_path.exists():
        print(
            f"error: manifest not found at {manifest_path} — run from the repo root "
            "(manifest, assemble.sh, and Em's context files resolve CWD-relative).",
            file=sys.stderr,
        )
        return None
    return yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}


def _start(args: argparse.Namespace) -> int:
    rc = _api_key_guard(args)
    if rc:
        return rc
    if args.stub:
        os.environ[FORCE_STUB_ENV] = "1"  # $0 contract: no transport goes live

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(
            f"error: manifest not found at {manifest_path} — run from the repo root "
            "(paths are CWD-relative).",
            file=sys.stderr,
        )
        return 2
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}

    brief_dir = Path(args.brief)
    if not (brief_dir / "00_studio_brief.md").exists():
        print(f"error: Studio Brief not found at {brief_dir / '00_studio_brief.md'}",
              file=sys.stderr)
        return 2
    # Auto-detect mode: a brief carrying a shots.yaml is back-compat (PLAN ->
    # GENERATE); without one it's an authoring run (PLAN -> SCRIPT -> STORYBOARD,
    # Sam + Bea draft the board). The slug names the run dir, fixed once at start.
    src_shots = brief_dir / "shots.yaml"
    needs_storyboard = not src_shots.exists()
    slug = args.slug or (read_slug(src_shots) if src_shots.exists() else None)
    if not slug:
        print(
            "error: no slug — an authoring brief (no shots.yaml) requires --slug; "
            f"a back-compat brief needs a slug: in {src_shots}.",
            file=sys.stderr,
        )
        return 2

    try:
        cast_table = derive_cast(manifest)
    except (ValueError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    run_dir = (
        Path(args.run_dir)
        if args.run_dir
        else Path("runs") / f"{date.today().isoformat()}-{slug.lower()}-run"
    )
    if (run_dir / st.STATE_FILENAME).exists():
        print(f"error: {run_dir} already holds a run — use --resume {run_dir}.",
              file=sys.stderr)
        return 2
    for sub in RUN_SUBDIRS:
        (run_dir / sub).mkdir(parents=True, exist_ok=True)

    # Snapshot the brief into the run (Slice 2.1 Fix B): the PLAN stage writes
    # plan.md/criteria into brief_dir and --approve-plan locks the criteria —
    # those must hit the run-local copy, never the committed brief.
    brief_src = brief_dir
    brief_dir = run_dir / "brief"
    shutil.copytree(brief_src, brief_dir, dirs_exist_ok=True)
    shots_path = brief_dir / "shots.yaml"

    state = st.new_state(
        run_id=run_dir.name,
        brief_dir=str(brief_dir),
        brief_src=str(brief_src),
        manifest_path=str(manifest_path),
        shots_path=str(shots_path),
        slug=str(slug),
        stub=bool(args.stub),
        cast=cast_table,
        needs_storyboard=needs_storyboard,
        # Opt-in placement gate: the --animatic flag OR manifest animatic.enabled.
        # Only consulted on the authoring path (the storyboard gate); a back-compat
        # brief goes PLAN -> GENERATE and never reads it.
        animatic_enabled=bool(args.animatic) or bool((manifest.get("animatic") or {}).get("enabled")),
        # Fix B: the human owns the loop length. Threaded to Bea (target) and
        # enforced at the storyboard gate (exact-count check). Authoring only.
        target_frames=args.frames,
    )
    st.save_state(run_dir, state)
    return plan_stage.run_plan_stage(
        state, manifest, run_dir, stub=args.stub, skip_smoke=args.skip_smoke
    )


def _resume(args: argparse.Namespace) -> int:
    actions = [
        bool(args.approve_plan),
        bool(args.approve_script),
        bool(args.approve_storyboard),
        bool(args.approve_animatic),
        args.approve_frame is not None,
        args.retry_frame is not None,
        bool(args.assemble),
        bool(args.status),
    ]
    if sum(actions) != 1:
        print(
            "error: --resume requires exactly one of "
            "--approve-plan | --approve-script | --approve-storyboard | "
            "--approve-animatic | --approve-frame N | --retry-frame N --note | "
            "--assemble | --status",
            file=sys.stderr,
        )
        return 2
    if args.retry_frame is not None and not args.note:
        print('error: --retry-frame requires --note "<correction>" (the retry ladder).',
              file=sys.stderr)
        return 2

    run_dir = Path(args.resume)
    try:
        state = st.load_state(run_dir)
    except st.StateError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if state.get("stub"):
        os.environ[FORCE_STUB_ENV] = "1"  # a stub run stays $0 across resumes

    if args.status:
        print(st.render_status(state))
        return 0

    if args.approve_plan and state["stage"] != "PLAN":
        print(
            f"error: --approve-plan only applies in the PLAN stage (run is at {state['stage']}).",
            file=sys.stderr,
        )
        return 2
    if args.approve_script and state["stage"] != "SCRIPT":
        print(
            f"error: --approve-script only applies in the SCRIPT stage (run is at {state['stage']}).",
            file=sys.stderr,
        )
        return 2
    if args.approve_storyboard and state["stage"] != "STORYBOARD":
        print(
            "error: --approve-storyboard only applies in the STORYBOARD stage "
            f"(run is at {state['stage']}).",
            file=sys.stderr,
        )
        return 2
    if args.approve_animatic and state["stage"] != "ANIMATIC":
        print(
            "error: --approve-animatic only applies in the ANIMATIC stage "
            f"(run is at {state['stage']}).",
            file=sys.stderr,
        )
        return 2
    if (args.approve_frame is not None or args.retry_frame is not None) \
            and state["stage"] != "GENERATE":
        print(
            "error: --approve-frame/--retry-frame only apply in the GENERATE stage "
            f"(run is at {state['stage']}).",
            file=sys.stderr,
        )
        return 2
    if args.assemble and state["stage"] != "ASSEMBLE":
        print(
            f"error: --assemble only applies in the ASSEMBLE stage (run is at {state['stage']}).",
            file=sys.stderr,
        )
        return 2

    if args.approve_plan:
        return _do_approve_plan(args, state, run_dir)
    if args.approve_script:
        return _do_approve_script(args, state, run_dir)
    if args.approve_storyboard:
        return _do_approve_storyboard(args, state, run_dir)
    if args.approve_animatic:
        return _do_approve_animatic(args, state, run_dir)
    if args.approve_frame is not None:
        return _do_approve_frame(args, state, run_dir)
    if args.assemble:
        return _do_assemble(args, state, run_dir)
    return _do_retry_frame(args, state, run_dir)


def _do_approve_plan(args: argparse.Namespace, state: dict, run_dir: Path) -> int:
    rc = _api_key_guard(args)
    if rc:
        return rc
    manifest = _load_manifest(state)
    if manifest is None:
        return 2
    return plan_stage.approve_plan_gate(state, manifest, run_dir)


def _do_approve_script(args: argparse.Namespace, state: dict, run_dir: Path) -> int:
    rc = _api_key_guard(args)
    if rc:
        return rc
    manifest = _load_manifest(state)
    if manifest is None:
        return 2
    return script_stage.approve_script_gate(state, manifest, run_dir)


def _do_approve_storyboard(args: argparse.Namespace, state: dict, run_dir: Path) -> int:
    rc = _api_key_guard(args)
    if rc:
        return rc
    manifest = _load_manifest(state)
    if manifest is None:
        return 2
    return storyboard_stage.approve_storyboard_gate(state, manifest, run_dir)


def _resume_manifest_and_bundle(state: dict) -> tuple[dict | None, object | None]:
    """Manifest + the merged criteria bundle, with the brief_file override
    re-applied from state on EVERY invocation (seam #8 — manifest.yaml on disk
    stays pinned to whatever piece it ships with)."""
    manifest = _load_manifest(state)
    if manifest is None:
        return None, None
    plan_stage.wire_brief_criteria(manifest, state["brief_dir"])
    return manifest, load_all_criteria(manifest)


def _do_approve_animatic(args: argparse.Namespace, state: dict, run_dir: Path) -> int:
    rc = _api_key_guard(args)
    if rc:
        return rc
    manifest = _load_manifest(state)
    if manifest is None:
        return 2
    return animatic_stage.approve_animatic_gate(state, manifest, run_dir)


def _do_approve_frame(args: argparse.Namespace, state: dict, run_dir: Path) -> int:
    rc = _api_key_guard(args)
    if rc:
        return rc
    manifest, bundle = _resume_manifest_and_bundle(state)
    if manifest is None:
        return 2
    return generate_stage.approve_frame(
        state, manifest, bundle, run_dir, args.approve_frame, args.attempt
    )


def _do_assemble(args: argparse.Namespace, state: dict, run_dir: Path) -> int:
    from pipeline.orchestration import assemble_stage

    manifest, bundle = _resume_manifest_and_bundle(state)
    if manifest is None:
        return 2
    return assemble_stage.run_assemble_stage(state, manifest, bundle, run_dir)


def _do_retry_frame(args: argparse.Namespace, state: dict, run_dir: Path) -> int:
    rc = _api_key_guard(args)
    if rc:
        return rc
    manifest, bundle = _resume_manifest_and_bundle(state)
    if manifest is None:
        return 2
    return generate_stage.retry_frame(
        state, manifest, bundle, run_dir, args.retry_frame, args.note, args.escalate
    )


if __name__ == "__main__":
    sys.exit(main())
