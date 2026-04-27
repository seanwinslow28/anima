"""Seedance orchestrator — sync test-shot mode for Task 3; async batch mode lands in Task 4.

CLI:
    # Sync single shot (Task 3):
    python3 pipeline/seedance_generate.py \\
        --shotlist pipeline/seedance_shotlist.yaml \\
        --shot T2 \\
        --tier fast \\
        --resolution 720p

    # Batch all shots (Task 4 — not yet implemented):
    python3 pipeline/seedance_generate.py \\
        --shotlist pipeline/seedance_shotlist.yaml \\
        --all \\
        --tier fast \\
        --resolution 720p

Outputs per shot:
    {run_dir}/seedance/{shot_id}_attempt_{NN}.mp4
    {run_dir}/seedance/{shot_id}_attempt_{NN}.meta.json
    {run_dir}/anchor_urls.json           (cache — reused across attempts/shots)
    {run_dir}/audit/seedance_log.jsonl   (submit + generated events per shot)
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

# Seedance shared helpers — all in the same directory.
sys.path.insert(0, str(Path(__file__).parent))
from seedance_lib import (
    load_env,
    load_shotlist,
    log_event,
    make_run_dir,
    upload_anchor,
)


# ---------------------------------------------------------------------------
# Model ID resolution
# ---------------------------------------------------------------------------

_MODEL_IDS = {
    "fast": "bytedance/seedance-2.0/fast/image-to-video",
    "standard": "bytedance/seedance-2.0/image-to-video",
}


def _model_id(tier: str) -> str:
    if tier not in _MODEL_IDS:
        raise ValueError(f"Unknown tier '{tier}'. Choose: {list(_MODEL_IDS)}")
    return _MODEL_IDS[tier]


# ---------------------------------------------------------------------------
# Sync single-shot flow
# ---------------------------------------------------------------------------

def run_shot_sync(
    shot: dict,
    run_dir: Path,
    tier: str,
    resolution: str,
    attempt: int,
    seed: int | None,
) -> None:
    """Execute a single Seedance job synchronously via fal_client.subscribe."""
    import fal_client  # deferred — mirrors seedance_lib pattern

    model_id = _model_id(tier)
    cache_path = run_dir / "anchor_urls.json"

    # --- Upload / retrieve anchor URLs ---
    print(f"  Uploading/caching start anchor: {shot['start']}")
    start_url = upload_anchor(shot["start"], cache_path)
    print(f"    -> {start_url[:72]}...")

    print(f"  Uploading/caching end anchor:   {shot['end']}")
    end_url = upload_anchor(shot["end"], cache_path)
    print(f"    -> {end_url[:72]}...")

    # --- Resolve effective duration ---
    # Seedance 2.0 API minimum is 4s; durations 4–15 or "auto" are accepted.
    # If the shotlist specifies < 4s (e.g. T2 at 3s), clamp to 4 with a warning.
    raw_duration = shot["duration"]
    _API_MIN_DURATION = 4
    if raw_duration < _API_MIN_DURATION:
        effective_duration = _API_MIN_DURATION
        print(
            f"  WARNING: shot '{shot['id']}' duration {raw_duration}s is below "
            f"API minimum {_API_MIN_DURATION}s. Clamping to {_API_MIN_DURATION}s. "
            f"The extra second will be trimmed in assembly."
        )
    else:
        effective_duration = raw_duration

    # --- Build fal.ai arguments ---
    arguments: dict = {
        "prompt": shot["prompt"],
        "image_url": start_url,
        "end_image_url": end_url,
        "resolution": resolution,
        "duration": str(effective_duration),
        "generate_audio": False,
    }
    if seed is not None:
        arguments["seed"] = seed

    # --- Log submission ---
    log_event(
        run_dir,
        {
            "event": "seedance_submit",
            "shot": shot["id"],
            "attempt": attempt,
            "tier": tier,
            "resolution": resolution,
            "model": model_id,
            "anchor_urls": {"start": start_url, "end": end_url},
        },
    )

    print(f"\n  Submitting to {model_id} …")
    print(f"  (Blocking until fal.ai responds — expected 60–180s for a {shot['duration']}s clip)")
    started_at = datetime.now().isoformat(timespec="seconds")
    wall_start = datetime.now()

    # --- Block until result ---
    result = fal_client.subscribe(model_id, arguments=arguments)

    completed_at = datetime.now().isoformat(timespec="seconds")
    elapsed_s = (datetime.now() - wall_start).total_seconds()

    # --- Extract result fields ---
    video_url: str = result["video"]["url"]
    returned_seed = result.get("seed")
    request_id = result.get("request_id")

    # --- Download MP4 ---
    attempt_str = f"{attempt:02d}"
    seedance_dir = run_dir / "seedance"
    seedance_dir.mkdir(exist_ok=True)

    local_mp4 = seedance_dir / f"{shot['id']}_attempt_{attempt_str}.mp4"
    print(f"\n  Downloading MP4 -> {local_mp4}")
    try:
        urllib.request.urlretrieve(video_url, local_mp4)
    except Exception as exc:
        # Fallback: read-and-write manually
        print(f"  urlretrieve failed ({exc}), trying urlopen fallback …")
        with urllib.request.urlopen(video_url) as resp:
            local_mp4.write_bytes(resp.read())

    video_size_bytes = local_mp4.stat().st_size

    # --- Write meta JSON ---
    meta_path = seedance_dir / f"{shot['id']}_attempt_{attempt_str}.meta.json"
    meta = {
        "shot_id": shot["id"],
        "attempt": attempt,
        "tier": tier,
        "resolution": resolution,
        "duration_s": shot["duration"],        # requested duration from shotlist
        "effective_duration_s": effective_duration,  # actual duration sent to API
        "model_id": model_id,
        "prompt": shot["prompt"],
        "anchor_urls": {"start": start_url, "end": end_url},
        "anchor_paths": {"start": shot["start"], "end": shot["end"]},
        "fal_request_id": request_id,
        "seed": returned_seed,
        "video_url": video_url,
        "video_size_bytes": video_size_bytes,
        "started_at": started_at,
        "completed_at": completed_at,
        "wall_clock_s": round(elapsed_s, 1),
    }
    meta_path.write_text(json.dumps(meta, indent=2))

    # --- Log completion ---
    log_event(
        run_dir,
        {
            "event": "seedance_generated",
            "shot": shot["id"],
            "attempt": attempt,
            "video_path": str(local_mp4),
            "video_size_bytes": video_size_bytes,
            "fal_request_id": request_id,
            "seed": returned_seed,
            "wall_clock_s": round(elapsed_s, 1),
        },
    )

    # --- Estimate cost ---
    cost_per_s = 0.24 if tier == "fast" else 0.48
    est_cost = effective_duration * cost_per_s
    size_mb = video_size_bytes / (1024 * 1024)

    # Relative paths for display (relative to project root)
    rel_mp4 = local_mp4.relative_to(Path.cwd()) if local_mp4.is_absolute() else local_mp4
    rel_meta = meta_path.relative_to(Path.cwd()) if meta_path.is_absolute() else meta_path

    print(f"\n  {shot['id']} attempt {attempt_str} generated")
    print(f"     MP4:    {rel_mp4} ({size_mb:.2f} MB)")
    print(f"     Meta:   {rel_meta}")
    print(f"     Seed:   {returned_seed}")
    print(f"     ReqID:  {request_id}")
    print(f"     Cost:   ~${est_cost:.2f} ({effective_duration}s x ${cost_per_s}/s {tier} tier)")
    print(f"     Time:   {elapsed_s:.0f}s wall-clock")
    print(f"     Open:   open {rel_mp4}")


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="seedance_generate.py",
        description="Seedance 2.0 orchestrator. Task 3: --shot sync mode. Task 4: --all batch mode.",
    )
    p.add_argument(
        "--shotlist",
        default="pipeline/seedance_shotlist.yaml",
        help="Path to the shot-list YAML (default: pipeline/seedance_shotlist.yaml)",
    )

    mode = p.add_mutually_exclusive_group()
    mode.add_argument(
        "--shot",
        metavar="ID",
        help="Shot ID to generate (sync mode — runs one shot, blocks until done)",
    )
    mode.add_argument(
        "--all",
        action="store_true",
        help="Generate all shots in the shot list (async batch mode — Task 4, not yet implemented)",
    )

    p.add_argument(
        "--tier",
        choices=["fast", "standard"],
        default="fast",
        help="Fal.ai tier: fast ($0.24/s) or standard ($0.48/s). Default: fast.",
    )
    p.add_argument(
        "--resolution",
        choices=["480p", "720p"],
        default="720p",
        help="Output resolution. Default: 720p.",
    )
    p.add_argument(
        "--attempt",
        type=int,
        default=1,
        metavar="N",
        help="Attempt number (default 1). Use --attempt 2 for a re-run with a fresh seed.",
    )
    p.add_argument(
        "--seed",
        type=int,
        default=None,
        metavar="S",
        help="Optional seed for reproducibility. If absent, fal.ai picks one (recorded in meta).",
    )
    p.add_argument(
        "--run-dir",
        metavar="PATH",
        default=None,
        help="Reuse an existing run dir instead of creating a new one today.",
    )
    return p


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # --- --all is Task 4 (not yet implemented) ---
    if args.all:
        raise NotImplementedError(
            "--all async batch mode is not yet implemented (Task 4). "
            "Use --shot <ID> to generate a single shot synchronously."
        )

    # --- --shot is required for sync mode ---
    if not args.shot:
        parser.error("--shot <ID> is required (or --all for batch mode, pending Task 4).")

    # --- Load environment ---
    load_env(".env")

    # --- Load shot list ---
    shotlist = load_shotlist(args.shotlist)

    # --- Resolve shot by id ---
    shots: list[dict] = shotlist.get("shots", [])
    shot = next((s for s in shots if s["id"] == args.shot), None)
    if shot is None:
        available = [s["id"] for s in shots]
        sys.exit(
            f"Shot '{args.shot}' not found in {args.shotlist}.\n"
            f"Available shot IDs: {available}"
        )

    # --- Resolve / create run dir ---
    if args.run_dir:
        run_dir = Path(args.run_dir)
        if not run_dir.exists():
            sys.exit(f"--run-dir '{run_dir}' does not exist. Omit to auto-create.")
        # Ensure standard subdirs exist in the provided dir.
        for sub in ("seedance", "extracted", "cleanup", "shots", "audit", "export"):
            (run_dir / sub).mkdir(exist_ok=True)
    else:
        run_dir = make_run_dir(prefix="act2-seedance")

    print(f"\nRun dir:    {run_dir}")
    print(f"Shot:       {shot['id']}  ({shot['duration']}s, {shot['risk']} risk)")
    print(f"Tier:       {args.tier}")
    print(f"Resolution: {args.resolution}")
    print(f"Attempt:    {args.attempt}")
    print()

    # --- Run sync shot ---
    run_shot_sync(
        shot=shot,
        run_dir=run_dir,
        tier=args.tier,
        resolution=args.resolution,
        attempt=args.attempt,
        seed=args.seed,
    )

    print("\nDone. Human gate: play the MP4, check materialization + aesthetic + identity.")
    print("If it passes -> Task 4 batch. If it fails -> --attempt 2 with a refined prompt or new seed.")


if __name__ == "__main__":
    main()
