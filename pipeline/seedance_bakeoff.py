"""Seedance prompt template bake-off orchestrator.

Iterates: variant × shot × seed -> Seedance API submission, polling, download.
Mirrors the async-batch pattern from seedance_generate.py --all so multiple
generations run concurrently on fal.ai.

CLI:
    # Full bake-off (9 variants × 2 shots × 2 seeds = 36 generations):
    python3 pipeline/seedance_bakeoff.py

    # Smoke test (single cell):
    python3 pipeline/seedance_bakeoff.py --variants V00 --shots W1 --seeds 42

    # Resume an in-progress run dir (refuses to overwrite existing MP4s):
    python3 pipeline/seedance_bakeoff.py --run-dir runs/seedance-bakeoff-2026-05-09

Outputs (per cell):
    {run_dir}/V{NN}_{name}/{shot_id}/seed_{NNNN}/output.mp4
    {run_dir}/V{NN}_{name}/{shot_id}/seed_{NNNN}/meta.json
    {run_dir}/anchor_urls.json                  (cache — reused across cells)
    {run_dir}/audit/bakeoff_log.jsonl           (submit + generated events)
    {run_dir}/manifest.lock.yaml                (frozen run config)
    {run_dir}/scoring.csv                       (empty rubric template)
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

# Project-local imports
sys.path.insert(0, str(Path(__file__).parent))
from seedance_lib import (
    load_bakeoff_variants,
    load_env,
    load_shotlist,
    log_event,
    make_bakeoff_run_dir,
    upload_anchor,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_MODEL_IDS = {
    "fast": "bytedance/seedance-2.0/fast/image-to-video",
    "standard": "bytedance/seedance-2.0/image-to-video",
}
_API_MIN_DURATION = 4
_COST_PER_SECOND = {"fast": 0.24, "standard": 0.48}

# 5 binary scoring criteria — matches design spec §4.4
_SCORING_CRITERIA = [
    "c1_style",       # style preservation
    "c2_identity",    # identity preservation
    "c3_motion",      # motion plausibility
    "c4_artifacts",   # absence of artifacts
    "c5_anchor",      # anchor adherence
]


# ---------------------------------------------------------------------------
# Cell-path helpers
# ---------------------------------------------------------------------------

def _variant_dir_name(variant: dict) -> str:
    """Return the per-variant subdir name, e.g. 'V00_v3_control'."""
    return f"{variant['id']}_{variant['name']}"


def _cell_dir(run_dir: Path, variant: dict, shot_id: str, seed: int) -> Path:
    """Return the directory for a single (variant, shot, seed) cell."""
    return run_dir / _variant_dir_name(variant) / shot_id / f"seed_{seed:04d}"


# ---------------------------------------------------------------------------
# Manifest + scoring template generation
# ---------------------------------------------------------------------------

def write_manifest(
    run_dir: Path,
    variants_data: dict,
    cli_args: argparse.Namespace,
) -> None:
    """Write {run_dir}/manifest.lock.yaml with the frozen run config."""
    import yaml

    manifest = {
        "run_started_at": datetime.now().isoformat(timespec="seconds"),
        "variants_file": str(Path(cli_args.variants_file).resolve()),
        "shotlist_file": str(Path(cli_args.shotlist).resolve()),
        "tier": cli_args.tier,
        "resolution": cli_args.resolution,
        "selected_variants": cli_args.variants or [v["id"] for v in variants_data["variants"]],
        "selected_shots": cli_args.shots or variants_data["test_shots"],
        "selected_seeds": cli_args.seeds or variants_data["seeds"],
    }
    (run_dir / "manifest.lock.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False))


def write_scoring_template(run_dir: Path, cells: list[dict]) -> None:
    """Write empty scoring.csv with one row per cell.

    Refuses to overwrite an existing file (preserves manual scores between runs).
    """
    csv_path = run_dir / "scoring.csv"
    if csv_path.exists():
        print(f"  Scoring template already exists at {csv_path} — keeping existing scores.")
        return

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["variant_id", "variant_name", "shot", "seed"]
            + _SCORING_CRITERIA
            + ["total", "notes"]
        )
        for cell in cells:
            writer.writerow(
                [cell["variant"]["id"], cell["variant"]["name"], cell["shot_id"], cell["seed"]]
                + ["" for _ in _SCORING_CRITERIA]
                + ["", ""]
            )
    print(f"  Wrote scoring template: {csv_path}")


# ---------------------------------------------------------------------------
# Cell submission + polling (mirrors seedance_generate.py async-batch)
# ---------------------------------------------------------------------------

def _build_arguments(prompt: str, start_url: str, end_url: str, resolution: str, seed: int) -> dict:
    return {
        "prompt": prompt,
        "image_url": start_url,
        "end_image_url": end_url,
        "resolution": resolution,
        "duration": str(_API_MIN_DURATION),
        "generate_audio": False,
        "seed": seed,
    }


def _submit_cell(
    cell: dict,
    shot: dict,
    model_id: str,
    run_dir: Path,
    cache_path: Path,
    resolution: str,
    tier: str,
) -> dict:
    """Submit one cell to fal.ai. Returns in-flight job dict."""
    import fal_client  # deferred

    variant = cell["variant"]
    shot_id = cell["shot_id"]
    seed = cell["seed"]
    prompt = variant["prompts"][shot_id]

    start_url = upload_anchor(shot["start"], cache_path)
    end_url = upload_anchor(shot["end"], cache_path)

    arguments = _build_arguments(prompt, start_url, end_url, resolution, seed)

    log_event(
        run_dir,
        {
            "event": "bakeoff_submit",
            "variant_id": variant["id"],
            "variant_name": variant["name"],
            "shot": shot_id,
            "seed": seed,
            "tier": tier,
            "resolution": resolution,
            "model": model_id,
            "anchor_urls": {"start": start_url, "end": end_url},
        },
    )

    handler = fal_client.submit(model_id, arguments=arguments)
    return {
        "cell": cell,
        "shot": shot,
        "model_id": model_id,
        "handler": handler,
        "request_id": handler.request_id,
        "arguments": arguments,
        "anchor_urls": {"start": start_url, "end": end_url},
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "wall_start": datetime.now(),
        "status": "PENDING",
    }


def _download_mp4(video_url: str, local_mp4: Path) -> None:
    try:
        urllib.request.urlretrieve(video_url, local_mp4)
    except Exception as exc:
        print(f"  urlretrieve failed ({exc}), trying urlopen fallback …")
        with urllib.request.urlopen(video_url) as resp:
            local_mp4.write_bytes(resp.read())


def _handle_completion(job: dict, run_dir: Path, tier: str) -> tuple[bool, str]:
    """Process a Completed result for one job. Returns (succeeded, message)."""
    import fal_client

    cell = job["cell"]
    variant = cell["variant"]
    shot_id = cell["shot_id"]
    seed = cell["seed"]
    request_id = job["request_id"]

    cell_path = _cell_dir(run_dir, variant, shot_id, seed)
    cell_path.mkdir(parents=True, exist_ok=True)
    local_mp4 = cell_path / "output.mp4"

    if local_mp4.exists():
        return False, f"refusing to overwrite {local_mp4}"

    try:
        result = fal_client.result(job["model_id"], request_id)
        video_url = result["video"]["url"]
        returned_seed = result.get("seed")
        completed_at = datetime.now().isoformat(timespec="seconds")
        wall_s = (datetime.now() - job["wall_start"]).total_seconds()

        _download_mp4(video_url, local_mp4)
        size_mb = local_mp4.stat().st_size / (1024 * 1024)

        meta = {
            "variant_id": variant["id"],
            "variant_name": variant["name"],
            "isolates_axis": variant.get("isolates_axis"),
            "shot_id": shot_id,
            "seed_requested": seed,
            "seed_returned": returned_seed,
            "tier": tier,
            "resolution": job["arguments"]["resolution"],
            "duration_s": _API_MIN_DURATION,
            "model_id": job["model_id"],
            "prompt": variant["prompts"][shot_id],
            "anchor_urls": job["anchor_urls"],
            "anchor_paths": {"start": job["shot"]["start"], "end": job["shot"]["end"]},
            "fal_request_id": request_id,
            "video_url": video_url,
            "video_size_bytes": local_mp4.stat().st_size,
            "started_at": job["started_at"],
            "completed_at": completed_at,
            "wall_clock_s": round(wall_s, 1),
        }
        (cell_path / "meta.json").write_text(json.dumps(meta, indent=2))

        log_event(
            run_dir,
            {
                "event": "bakeoff_generated",
                "variant_id": variant["id"],
                "shot": shot_id,
                "seed": seed,
                "video_path": str(local_mp4),
                "video_size_bytes": local_mp4.stat().st_size,
                "fal_request_id": request_id,
                "wall_clock_s": round(wall_s, 1),
            },
        )

        cost = _API_MIN_DURATION * _COST_PER_SECOND[tier]
        return True, f"{size_mb:.2f} MB, ~${cost:.2f}, {wall_s:.0f}s"
    except Exception as exc:
        log_event(
            run_dir,
            {
                "event": "bakeoff_failed",
                "variant_id": variant["id"],
                "shot": shot_id,
                "seed": seed,
                "fal_request_id": request_id,
                "error": str(exc),
            },
        )
        return False, str(exc)


# ---------------------------------------------------------------------------
# Main run loop
# ---------------------------------------------------------------------------

def _build_cells(
    variants_data: dict,
    selected_variants: list[str] | None,
    selected_shots: list[str] | None,
    selected_seeds: list[int] | None,
) -> list[dict]:
    """Compose the (variant, shot, seed) cell list, filtered by CLI selections."""
    variants = variants_data["variants"]
    if selected_variants:
        variants = [v for v in variants if v["id"] in selected_variants]
    shots = selected_shots or variants_data["test_shots"]
    seeds = selected_seeds or variants_data["seeds"]

    cells: list[dict] = []
    for variant in variants:
        for shot_id in shots:
            for seed in seeds:
                cells.append({"variant": variant, "shot_id": shot_id, "seed": seed})
    return cells


def run_bakeoff(args: argparse.Namespace) -> None:  # noqa: C901
    """Submit all cells, poll until done, write outputs + scoring template."""
    import fal_client
    from fal_client.client import Completed, InProgress, Queued

    load_env(".env")
    variants_data = load_bakeoff_variants(args.variants_file)
    shotlist = load_shotlist(args.shotlist)
    shots_by_id: dict[str, dict] = {s["id"]: s for s in shotlist.get("shots", [])}

    # Resolve run dir
    if args.run_dir:
        run_dir = Path(args.run_dir)
        if not run_dir.exists():
            sys.exit(f"--run-dir '{run_dir}' does not exist. Omit to auto-create.")
        (run_dir / "audit").mkdir(exist_ok=True)
    else:
        run_dir = make_bakeoff_run_dir()
        (run_dir / "audit").mkdir(exist_ok=True)

    cache_path = run_dir / "anchor_urls.json"
    write_manifest(run_dir, variants_data, args)

    # Scoring CSV must always cover the full 9×2×2 matrix, even on filtered runs.
    # (Otherwise a smoke run with --variants V00 would leave a 1-row CSV that
    # the next full run won't overwrite, since write_scoring_template refuses to clobber.)
    full_matrix_cells = _build_cells(variants_data, None, None, None)
    write_scoring_template(run_dir, full_matrix_cells)

    # Compose this invocation's cells (filtered by CLI), then drop any whose MP4
    # already exists so reruns and resumes work cleanly.
    filtered_cells = _build_cells(variants_data, args.variants, args.shots, args.seeds)
    cells_to_run: list[dict] = []
    pre_existing: list[str] = []
    for cell in filtered_cells:
        if cell["shot_id"] not in shots_by_id:
            sys.exit(
                f"Shot '{cell['shot_id']}' not found in {args.shotlist}. "
                f"Available: {list(shots_by_id)}"
            )
        local_mp4 = _cell_dir(run_dir, cell["variant"], cell["shot_id"], cell["seed"]) / "output.mp4"
        if local_mp4.exists():
            pre_existing.append(f"{cell['variant']['id']}/{cell['shot_id']}/seed_{cell['seed']}")
            continue
        cells_to_run.append(cell)

    if not cells_to_run:
        print("\nNo cells to run (all already complete).")
        return

    print(f"\nRun dir:      {run_dir}")
    print(f"Tier:         {args.tier}  (${_COST_PER_SECOND[args.tier]}/s)")
    print(f"Resolution:   {args.resolution}")
    print(f"Cells to run: {len(cells_to_run)}")
    print(f"Pre-existing: {len(pre_existing)} (will skip)")
    print(f"Est. cost:    ~${len(cells_to_run) * _API_MIN_DURATION * _COST_PER_SECOND[args.tier]:.2f}")
    print()

    model_id = _MODEL_IDS[args.tier]

    # Pre-upload all unique anchors (idempotent via cache)
    print("=== Uploading anchors ===")
    unique_anchors: set[str] = set()
    for cell in cells_to_run:
        s = shots_by_id[cell["shot_id"]]
        unique_anchors.add(s["start"])
        unique_anchors.add(s["end"])
    for anchor in sorted(unique_anchors):
        upload_anchor(anchor, cache_path)
        print(f"  cached: {anchor}")
    print()

    # Submit all cells
    print("=== Submitting jobs ===")
    in_flight: list[dict] = []
    batch_start = datetime.now()

    for cell in cells_to_run:
        cid = f"{cell['variant']['id']}/{cell['shot_id']}/seed_{cell['seed']}"
        try:
            job = _submit_cell(
                cell=cell,
                shot=shots_by_id[cell["shot_id"]],
                model_id=model_id,
                run_dir=run_dir,
                cache_path=cache_path,
                resolution=args.resolution,
                tier=args.tier,
            )
            in_flight.append(job)
            print(f"  submitted {cid}  request_id={job['request_id']}")
        except Exception as exc:
            print(f"  ❌ {cid} SUBMIT FAILED: {exc}")
            log_event(run_dir, {"event": "bakeoff_submit_failed", "cell": cid, "error": str(exc)})

    print(f"\n{len(in_flight)} jobs in flight. Polling every 15s …\n")

    # Poll until done
    pending = list(in_flight)
    generated: list[str] = []
    failed: list[tuple[str, str]] = []

    while pending:
        time.sleep(15)
        elapsed = (datetime.now() - batch_start).total_seconds()
        elapsed_str = f"{int(elapsed // 60):02d}:{int(elapsed % 60):02d}"

        still_pending: list[dict] = []
        progress: list[str] = []

        for job in pending:
            cell = job["cell"]
            cid = f"{cell['variant']['id']}/{cell['shot_id']}/seed_{cell['seed']}"
            try:
                st = fal_client.status(job["model_id"], job["request_id"])
            except Exception as exc:
                progress.append(f"{cid}=ERR")
                still_pending.append(job)
                continue

            if isinstance(st, Queued):
                progress.append(f"{cid}=Q{st.position}")
                still_pending.append(job)
            elif isinstance(st, InProgress):
                progress.append(f"{cid}=IP")
                still_pending.append(job)
            elif isinstance(st, Completed):
                if st.error:
                    progress.append(f"{cid}=FAIL")
                    failed.append((cid, f"{st.error} (type={st.error_type})"))
                    log_event(run_dir, {
                        "event": "bakeoff_failed",
                        "cell": cid,
                        "error": str(st.error),
                    })
                else:
                    progress.append(f"{cid}=OK")
                    ok, msg = _handle_completion(job, run_dir, args.tier)
                    if ok:
                        generated.append(cid)
                        print(f"\n  ✅ {cid}  {msg}")
                    else:
                        failed.append((cid, msg))
                        print(f"\n  ❌ {cid}  {msg}")
            else:
                progress.append(f"{cid}=?")
                still_pending.append(job)

        # Compact status line — chunk to keep it readable
        chunks = [progress[i:i + 6] for i in range(0, len(progress), 6)]
        for chunk in chunks:
            print(f"[{elapsed_str}] {' | '.join(chunk)}")
        pending = still_pending

    # Summary
    total_wall = (datetime.now() - batch_start).total_seconds()
    total_cost = len(generated) * _API_MIN_DURATION * _COST_PER_SECOND[args.tier]

    print("\n=== Bake-off complete ===")
    print(f"✅ Generated: {len(generated)}/{len(in_flight)}")
    print(f"❌ Failed:    {len(failed)}")
    print(f"Total wall-clock: {int(total_wall // 60)}m {int(total_wall % 60)}s")
    print(f"Total cost:       ~${total_cost:.2f}")
    print(f"Run dir:          {run_dir}")
    print(f"Scoring CSV:      {run_dir}/scoring.csv  (open in any spreadsheet tool)")
    if failed:
        print("\nFailed cells (re-run with --variants/--shots/--seeds to retry):")
        for cid, msg in failed:
            print(f"  {cid}: {msg}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="seedance_bakeoff.py",
        description="Run the 9-variant Seedance prompt template bake-off.",
    )
    p.add_argument(
        "--variants-file",
        default="pipeline/seedance_bakeoff_variants.yaml",
        help="Path to bake-off variants YAML.",
    )
    p.add_argument(
        "--shotlist",
        default="pipeline/seedance_shotlist.yaml",
        help="Path to shot-list YAML (anchors come from here by shot ID).",
    )
    p.add_argument(
        "--variants",
        nargs="+",
        default=None,
        metavar="ID",
        help="Subset of variant IDs to run (e.g. V00 V01). Default: all.",
    )
    p.add_argument(
        "--shots",
        nargs="+",
        default=None,
        metavar="ID",
        help="Subset of shot IDs to run (default: all from variants YAML).",
    )
    p.add_argument(
        "--seeds",
        nargs="+",
        type=int,
        default=None,
        metavar="N",
        help="Subset of seeds (default: all from variants YAML).",
    )
    p.add_argument(
        "--tier",
        choices=["fast", "standard"],
        default="fast",
    )
    p.add_argument(
        "--resolution",
        choices=["480p", "720p"],
        default="720p",
    )
    p.add_argument(
        "--run-dir",
        default=None,
        help="Reuse an existing run dir (resumes — skips cells whose MP4 exists).",
    )
    return p


def main() -> None:
    args = build_parser().parse_args()
    run_bakeoff(args)


if __name__ == "__main__":
    main()
