"""Seedance orchestrator — sync test-shot mode (Task 3) + async batch mode (Task 4).

CLI:
    # Sync single shot (Task 3):
    python3 pipeline/seedance_generate.py \\
        --shotlist pipeline/seedance_shotlist.yaml \\
        --shot T2 \\
        --tier fast \\
        --resolution 720p

    # Batch all shots (Task 4):
    python3 pipeline/seedance_generate.py \\
        --shotlist pipeline/seedance_shotlist.yaml \\
        --all \\
        --skip T2 \\
        --tier fast \\
        --resolution 720p

    # Batch with multiple skips:
    python3 pipeline/seedance_generate.py --all --skip T2 --skip W1 --tier fast

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
import time
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


# Seedance 2.0 API minimum duration (seconds). Shared by sync and async paths.
# Shotlist durations below this (e.g. T2=3s, TR=3s) are clamped; the extra second
# is trimmed during assembly since those shots precede hard cuts.
_API_MIN_DURATION = 4


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
    if local_mp4.exists():
        sys.exit(
            f"Refusing to overwrite existing {local_mp4}. "
            f"Use --attempt {attempt + 1} to record a new attempt, or delete the file first."
        )
    print(f"\n  Downloading MP4 -> {local_mp4}")
    try:
        try:
            urllib.request.urlretrieve(video_url, local_mp4)
        except Exception as exc:
            # Fallback: read-and-write manually
            print(f"  urlretrieve failed ({exc}), trying urlopen fallback …")
            with urllib.request.urlopen(video_url) as resp:
                local_mp4.write_bytes(resp.read())
    except Exception as exc:
        # Surface the fal.ai URL + log path so the user can recover the asset manually
        log_path = run_dir / "audit" / "seedance_log.jsonl"
        sys.exit(
            f"Download of {video_url} failed: {exc}.\n"
            f"  The clip was generated successfully on fal.ai — fetch it manually, e.g.:\n"
            f"    curl -L -o {local_mp4} '{video_url}'\n"
            f"  Or inspect {log_path} for the full submit/generate trace."
        )

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

    # Relative paths for display (relative to project root); fall back to absolute
    # if run_dir is outside cwd (e.g. user passed --run-dir to a different drive).
    def _rel(p: Path) -> Path:
        try:
            return p.relative_to(Path.cwd()) if p.is_absolute() else p
        except ValueError:
            return p
    rel_mp4 = _rel(local_mp4)
    rel_meta = _rel(meta_path)

    print(f"\n  {shot['id']} attempt {attempt_str} generated")
    print(f"     MP4:    {rel_mp4} ({size_mb:.2f} MB)")
    print(f"     Meta:   {rel_meta}")
    print(f"     Seed:   {returned_seed}")
    print(f"     ReqID:  {request_id}")
    print(f"     Cost:   ~${est_cost:.2f} ({effective_duration}s x ${cost_per_s}/s {tier} tier)")
    print(f"     Time:   {elapsed_s:.0f}s wall-clock")
    print(f"     Open:   open {rel_mp4}")


# ---------------------------------------------------------------------------
# Async batch mode (Task 4)
# ---------------------------------------------------------------------------


def _build_arguments(
    shot: dict,
    start_url: str,
    end_url: str,
    resolution: str,
) -> tuple[dict, int, int]:
    """Build fal.ai API arguments for a shot.

    Returns (arguments_dict, raw_duration, effective_duration).
    The effective_duration clamps raw_duration to _API_MIN_DURATION.
    """
    raw_duration = shot["duration"]
    if raw_duration < _API_MIN_DURATION:
        effective_duration = _API_MIN_DURATION
    else:
        effective_duration = raw_duration

    arguments: dict = {
        "prompt": shot["prompt"],
        "image_url": start_url,
        "end_image_url": end_url,
        "resolution": resolution,
        "duration": str(effective_duration),
        "generate_audio": False,
    }
    return arguments, raw_duration, effective_duration


def _download_mp4(video_url: str, local_mp4: Path, run_dir: Path) -> None:
    """Download a fal.ai video URL to local_mp4. Exits on unrecoverable failure."""
    try:
        try:
            urllib.request.urlretrieve(video_url, local_mp4)
        except Exception as exc:
            print(f"  urlretrieve failed ({exc}), trying urlopen fallback …")
            with urllib.request.urlopen(video_url) as resp:
                local_mp4.write_bytes(resp.read())
    except Exception as exc:
        log_path = run_dir / "audit" / "seedance_log.jsonl"
        # In batch mode we raise rather than exit so the caller can continue with other jobs.
        raise RuntimeError(
            f"Download of {video_url} failed: {exc}.\n"
            f"  Fetch manually: curl -L -o {local_mp4} '{video_url}'\n"
            f"  See {log_path} for the full trace."
        ) from exc


def _submit_one(
    shot: dict,
    model_id: str,
    run_dir: Path,
    tier: str,
    resolution: str,
    attempt: int,
    cache_path: Path,
) -> dict:
    """Upload anchors and submit one shot to fal.ai.  Returns the in-flight job dict."""
    import fal_client  # deferred

    key = shot["id"]

    # Upload / retrieve anchor URLs (idempotent via cache).
    start_url = upload_anchor(shot["start"], cache_path)
    end_url = upload_anchor(shot["end"], cache_path)

    arguments, raw_duration, effective_duration = _build_arguments(
        shot, start_url, end_url, resolution
    )

    if effective_duration != raw_duration:
        print(
            f"  [{key}] WARNING: duration {raw_duration}s < API minimum {_API_MIN_DURATION}s. "
            f"Clamping to {_API_MIN_DURATION}s (trim in assembly)."
        )

    # Log submission.
    log_event(
        run_dir,
        {
            "event": "seedance_submit",
            "shot": key,
            "attempt": attempt,
            "tier": tier,
            "resolution": resolution,
            "model": model_id,
            "anchor_urls": {"start": start_url, "end": end_url},
            "duration_s": raw_duration,
            "effective_duration_s": effective_duration,
        },
    )

    handler = fal_client.submit(model_id, arguments=arguments)
    request_id = handler.request_id

    log_event(
        run_dir,
        {
            "event": "seedance_submit_async",
            "shot": key,
            "attempt": attempt,
            "tier": tier,
            "resolution": resolution,
            "model": model_id,
            "anchor_urls": {"start": start_url, "end": end_url},
            "duration_s": raw_duration,
            "effective_duration_s": effective_duration,
            "fal_request_id": request_id,
        },
    )

    return {
        "shot": shot,
        "model_id": model_id,
        "handler": handler,
        "request_id": request_id,
        "arguments": arguments,
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "wall_start": datetime.now(),
        "raw_duration": raw_duration,
        "effective_duration": effective_duration,
        "anchor_urls": {"start": start_url, "end": end_url},
        "status": "PENDING",  # local tracking state
    }


def run_all_async(args: argparse.Namespace) -> None:  # noqa: C901  — accepted complexity
    """Async batch mode: submit all non-skipped shots in parallel, poll until done."""
    import fal_client
    from fal_client.client import Completed, InProgress, Queued  # status type checks

    load_env(".env")
    shotlist = load_shotlist(args.shotlist)

    # --- Resolve run dir ---
    if args.run_dir:
        run_dir = Path(args.run_dir)
        if not run_dir.exists():
            sys.exit(f"--run-dir '{run_dir}' does not exist. Omit to auto-create.")
        for sub in ("seedance", "extracted", "cleanup", "shots", "audit", "export"):
            (run_dir / sub).mkdir(exist_ok=True)
    else:
        run_dir = make_run_dir(prefix="act2-seedance")

    cache_path = run_dir / "anchor_urls.json"
    seedance_dir = run_dir / "seedance"
    seedance_dir.mkdir(exist_ok=True)
    attempt_str = f"{args.attempt:02d}"

    skip_ids: set[str] = set(args.skip or [])
    shots: list[dict] = shotlist.get("shots", [])
    tier = args.tier
    model_id = _model_id(tier)
    cost_per_s = 0.24 if tier == "fast" else 0.48

    # --- Pre-flight: identify shots to submit ---
    to_submit: list[dict] = []
    pre_skipped: list[str] = []
    for shot in shots:
        sid = shot["id"]
        if sid in skip_ids:
            print(f"  [SKIP] {sid} — in --skip list")
            continue
        # Defensive: if the MP4 already exists, skip with a warning rather than crashing later.
        local_mp4 = seedance_dir / f"{sid}_attempt_{attempt_str}.mp4"
        if local_mp4.exists():
            print(f"  [SKIP] {sid} — {local_mp4} already exists (use --attempt {args.attempt + 1} to re-run)")
            pre_skipped.append(sid)
            continue
        to_submit.append(shot)

    if not to_submit:
        print("\nNo shots to submit (all skipped or already generated).")
        return

    print(f"\nRun dir:    {run_dir}")
    print(f"Tier:       {tier}  (${cost_per_s}/s)")
    print(f"Resolution: {args.resolution}")
    print(f"Attempt:    {args.attempt}")
    print(f"Submitting: {[s['id'] for s in to_submit]}")
    print(f"Skipping:   {sorted(skip_ids | set(pre_skipped)) or '<none>'}")
    print()

    # --- Upload all anchors up front (idempotent via cache) ---
    print("=== Uploading anchors ===")
    unique_anchors: set[str] = set()
    for shot in to_submit:
        unique_anchors.add(shot["start"])
        unique_anchors.add(shot["end"])

    # Show cache HIT vs UPLOAD for each anchor so progress is observable.
    cache_before: dict[str, str] = {}
    if cache_path.exists():
        try:
            cache_before = json.loads(cache_path.read_text())
        except json.JSONDecodeError:
            cache_before = {}

    for anchor_path in sorted(unique_anchors):
        if str(Path(anchor_path)) in cache_before:
            print(f"  HIT    {anchor_path}")
        else:
            print(f"  UPLOAD {anchor_path} …")
        upload_anchor(anchor_path, cache_path)  # idempotent — returns cached URL on hit

    cache_after: dict[str, str] = json.loads(cache_path.read_text())
    print(f"\nAnchor cache: {len(cache_before)} → {len(cache_after)} entries\n")

    # --- Submit all jobs ---
    print("=== Submitting jobs ===")
    in_flight: list[dict] = []
    batch_wall_start = datetime.now()

    for shot in to_submit:
        sid = shot["id"]
        print(f"  Submitting {sid} ({shot['duration']}s, {shot['risk']} risk) …")
        try:
            job = _submit_one(
                shot=shot,
                model_id=model_id,
                run_dir=run_dir,
                tier=tier,
                resolution=args.resolution,
                attempt=args.attempt,
                cache_path=cache_path,
            )
            in_flight.append(job)
            print(f"    -> request_id={job['request_id']}")
        except Exception as exc:
            print(f"  ❌ {sid} SUBMIT FAILED: {exc}")
            log_event(run_dir, {"event": "seedance_submit_failed", "shot": sid, "error": str(exc)})
            # Track as a failed job with no handler so the summary picks it up.
            in_flight.append({
                "shot": shot,
                "model_id": model_id,
                "handler": None,
                "request_id": None,
                "arguments": {},
                "started_at": datetime.now().isoformat(timespec="seconds"),
                "wall_start": datetime.now(),
                "raw_duration": shot["duration"],
                "effective_duration": shot["duration"],
                "anchor_urls": {},
                "status": "FAILED",
                "error": str(exc),
            })

    print(f"\n{len(in_flight)} jobs in flight. Polling every 10s …\n")

    # --- Poll until all complete or fail ---
    generated: list[str] = []
    failed: list[tuple[str, str]] = []  # (shot_id, error_msg)
    warned_long: set[str] = set()

    pending = [j for j in in_flight if j["status"] == "PENDING"]

    while pending:
        time.sleep(10)
        elapsed_total = (datetime.now() - batch_wall_start).total_seconds()
        elapsed_str = f"{int(elapsed_total // 60):02d}:{int(elapsed_total % 60):02d}"

        status_parts: list[str] = []
        still_pending: list[dict] = []

        for job in pending:
            sid = job["shot"]["id"]
            request_id = job["request_id"]

            # Warn if a job has been in queue > 10 minutes.
            job_elapsed = (datetime.now() - job["wall_start"]).total_seconds()
            if job_elapsed > 600 and sid not in warned_long:
                print(f"  ⚠️  {sid} still pending after {job_elapsed:.0f}s — queue congestion?")
                warned_long.add(sid)

            try:
                st = fal_client.status(job["model_id"], request_id)
            except Exception as exc:
                status_parts.append(f"{sid}=ERROR({exc})")
                still_pending.append(job)
                continue

            if isinstance(st, Queued):
                status_parts.append(f"{sid}=IN_QUEUE(pos={st.position})")
                still_pending.append(job)

            elif isinstance(st, InProgress):
                status_parts.append(f"{sid}=IN_PROGRESS")
                still_pending.append(job)

            elif isinstance(st, Completed):
                if st.error:
                    status_parts.append(f"{sid}=FAILED")
                    job["status"] = "FAILED"
                    error_msg = f"{st.error} (type={st.error_type})"
                    print(f"\n  ❌ {sid} FAILED: {error_msg}")
                    log_event(
                        run_dir,
                        {
                            "event": "seedance_failed",
                            "shot": sid,
                            "attempt": args.attempt,
                            "fal_request_id": request_id,
                            "error": error_msg,
                        },
                    )
                    failed.append((sid, error_msg))
                else:
                    status_parts.append(f"{sid}=COMPLETED")
                    job["status"] = "COMPLETED"
                    # Fetch result and download.
                    try:
                        result = fal_client.result(job["model_id"], request_id)
                        video_url: str = result["video"]["url"]
                        returned_seed = result.get("seed")
                        completed_at = datetime.now().isoformat(timespec="seconds")
                        wall_s = (datetime.now() - job["wall_start"]).total_seconds()

                        local_mp4 = seedance_dir / f"{sid}_attempt_{attempt_str}.mp4"
                        print(f"\n  Downloading {sid} -> {local_mp4} …")
                        _download_mp4(video_url, local_mp4, run_dir)

                        video_size_bytes = local_mp4.stat().st_size
                        size_mb = video_size_bytes / (1024 * 1024)

                        # Write meta JSON.
                        meta = {
                            "shot_id": sid,
                            "attempt": args.attempt,
                            "tier": tier,
                            "resolution": args.resolution,
                            "duration_s": job["raw_duration"],
                            "effective_duration_s": job["effective_duration"],
                            "model_id": job["model_id"],
                            "prompt": job["shot"]["prompt"],
                            "anchor_urls": job["anchor_urls"],
                            "anchor_paths": {
                                "start": job["shot"]["start"],
                                "end": job["shot"]["end"],
                            },
                            "fal_request_id": request_id,
                            "seed": returned_seed,
                            "video_url": video_url,
                            "video_size_bytes": video_size_bytes,
                            "started_at": job["started_at"],
                            "completed_at": completed_at,
                            "wall_clock_s": round(wall_s, 1),
                        }
                        meta_path = seedance_dir / f"{sid}_attempt_{attempt_str}.meta.json"
                        meta_path.write_text(json.dumps(meta, indent=2))

                        log_event(
                            run_dir,
                            {
                                "event": "seedance_generated",
                                "shot": sid,
                                "attempt": args.attempt,
                                "video_path": str(local_mp4),
                                "video_size_bytes": video_size_bytes,
                                "fal_request_id": request_id,
                                "seed": returned_seed,
                                "wall_clock_s": round(wall_s, 1),
                            },
                        )

                        est_cost = job["effective_duration"] * cost_per_s
                        print(
                            f"  ✅ {sid}  {size_mb:.2f} MB  seed={returned_seed}"
                            f"  ~${est_cost:.2f}  {wall_s:.0f}s"
                        )
                        generated.append(sid)

                    except Exception as exc:
                        error_msg = str(exc)
                        print(f"\n  ❌ {sid} RESULT/DOWNLOAD FAILED: {error_msg}")
                        log_event(
                            run_dir,
                            {
                                "event": "seedance_failed",
                                "shot": sid,
                                "attempt": args.attempt,
                                "fal_request_id": request_id,
                                "error": error_msg,
                            },
                        )
                        failed.append((sid, error_msg))
            else:
                status_parts.append(f"{sid}=UNKNOWN")
                still_pending.append(job)

        print(f"[{elapsed_str}] {' | '.join(status_parts)}")
        pending = still_pending

    # Also surface any submit-time failures.
    for job in in_flight:
        if job["status"] == "FAILED" and job["shot"]["id"] not in [f for f, _ in failed]:
            failed.append((job["shot"]["id"], job.get("error", "submit failed")))

    # --- Final summary ---
    total_wall_s = (datetime.now() - batch_wall_start).total_seconds()
    total_wall_str = f"{int(total_wall_s // 60)}m {int(total_wall_s % 60)}s"
    total_effective_s = sum(
        j["effective_duration"] for j in in_flight if j["shot"]["id"] in generated
    )
    total_cost = total_effective_s * cost_per_s

    print("\n=== Batch complete ===")
    print(f"✅ Generated: {', '.join(generated) if generated else '<none>'}")
    print(f"❌ Failed:    {', '.join(f for f, _ in failed) if failed else '<none>'}")
    print(f"Total wall-clock: {total_wall_str}")
    print(
        f"Total cost: ~${total_cost:.2f}"
        f" ({total_effective_s}s × ${cost_per_s}/s {tier} tier"
        f" — does not include T2)"
    )
    print(f"Audit log: {run_dir}/audit/seedance_log.jsonl")

    # Refresh cache entry count for the summary.
    try:
        final_cache = json.loads(cache_path.read_text())
        print(f"Anchor cache: {len(final_cache)} entries")
    except Exception:
        pass

    print()
    print("Human gate (Task 4.3): Inspect each MP4 in runs/act2-seedance-2026-04-27/seedance/.")
    print("For any clearly broken clip, surface the issue — do NOT auto-retry.")
    print("Documented per-shot fallbacks (per pipeline/seedance_shotlist.yaml fallback fields):")
    print("  S0  -> 0.3s cross-fade hard cut")
    print("  T0  -> split into S1.5 + T0")
    print("  REV -> drop to 4s, then split via being_pulled.png bridge")
    print("  PB  -> 0.4s cross-fade hard cut")

    if failed:
        print(
            f"\n⚠️  {len(failed)} shot(s) failed. Re-run with: "
            f"--shot <ID> --attempt {args.attempt + 1}"
        )


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="seedance_generate.py",
        description="Seedance 2.0 orchestrator. --shot: sync single-shot. --all: async batch.",
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
        help="Generate all shots in the shot list (async batch mode)",
    )

    p.add_argument(
        "--skip",
        metavar="ID",
        action="append",
        default=None,
        help=(
            "Shot ID to skip in --all mode (repeatable: --skip T2 --skip W1). "
            "No effect in --shot mode."
        ),
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
        help=(
            "Optional seed for reproducibility (--shot mode only). "
            "Rejected in --all mode — fal.ai picks per-shot seeds, recorded in each meta JSON."
        ),
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

    # --- Validate: --seed rejected in --all mode ---
    if args.all and args.seed is not None:
        parser.error(
            "--seed is not supported in --all mode. "
            "Per-shot seeds are dangerous in batch (same seed = same motion across shots). "
            "Let fal.ai pick seeds — they are recorded in each meta JSON."
        )

    # --- Route to async batch mode ---
    if args.all:
        run_all_async(args)
        return

    # --- --shot is required for sync mode ---
    if not args.shot:
        parser.error("--shot <ID> is required (or --all for batch mode).")

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
