#!/usr/bin/env python3
"""
Pencil Test Animation — Generation Orchestrator

Reads manifest.yaml, initializes a run directory, and orchestrates keyframe
generation with frame chaining. Each frame is generated via the Gemini API
using generate_image.py, with the A-2 anchor + previous approved frame as
reference images.

Usage:
    python3 pipeline/generate.py --manifest manifest.yaml
    python3 pipeline/generate.py --manifest manifest.yaml --frame F06
    python3 pipeline/generate.py --manifest manifest.yaml --chain 1
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml


def load_manifest(manifest_path: str) -> dict:
    with open(manifest_path) as f:
        return yaml.safe_load(f)


def create_run_dir(base_dir: str = "runs") -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    run_dir = Path(base_dir) / f"run_{timestamp}"
    for subdir in ["candidates", "approved", "rejected", "audit", "export"]:
        (run_dir / subdir).mkdir(parents=True, exist_ok=True)
    return run_dir


def find_latest_run(base_dir: str = "runs") -> Path | None:
    runs_path = Path(base_dir)
    if not runs_path.exists():
        return None
    run_dirs = sorted(runs_path.glob("run_*"), reverse=True)
    return run_dirs[0] if run_dirs else None


def lock_manifest(manifest_path: str, run_dir: Path) -> Path:
    lock_path = run_dir / "manifest.lock.yaml"
    shutil.copy2(manifest_path, lock_path)
    return lock_path


def copy_anchor_frames(manifest: dict, run_dir: Path):
    anchor_path = Path(manifest["anchor"]["path"])
    if not anchor_path.exists():
        print(f"Error: Anchor image not found: {anchor_path}", file=sys.stderr)
        sys.exit(1)

    # F01 and F40 use anchor directly
    for frame_num in [1, 40]:
        dest = run_dir / "approved" / f"PT_A1_F{frame_num:02d}_key.png"
        shutil.copy2(anchor_path, dest)
        print(f"  Copied anchor -> {dest.name}")


def resolve_references(keyframe: dict, manifest: dict, run_dir: Path) -> list[str]:
    refs = []
    anchor_path = Path(manifest["anchor"]["path"])

    if keyframe.get("source") == "anchor":
        return []  # No generation needed

    for ref in keyframe.get("references", []):
        if ref == "anchor":
            refs.append(str(anchor_path))
        elif ref.startswith("F"):
            frame_num = int(ref[1:])
            approved_path = run_dir / "approved" / f"PT_A1_F{frame_num:02d}_key.png"
            if approved_path.exists():
                refs.append(str(approved_path))
            else:
                print(f"  Warning: Reference {ref} not yet approved at {approved_path}")
    return refs


def get_attempt_number(candidates_dir: Path) -> int:
    existing = list(candidates_dir.glob("attempt_*.png"))
    return len(existing) + 1


def generate_frame(
    frame_num: int,
    prompt: str,
    references: list[str],
    manifest: dict,
    run_dir: Path,
) -> Path:
    gen_config = manifest["generation"]
    script_path = gen_config["script"]
    aspect_ratio = gen_config["aspect_ratio"]
    env_file = gen_config["env_file"]

    candidates_dir = run_dir / "candidates" / f"F{frame_num:02d}"
    candidates_dir.mkdir(parents=True, exist_ok=True)

    attempt = get_attempt_number(candidates_dir)
    output_path = candidates_dir / f"attempt_{attempt:02d}.png"

    cmd = [
        sys.executable, script_path,
        prompt,
        "--output", str(output_path),
        "--aspect-ratio", aspect_ratio,
        "--env-file", env_file,
    ]

    if references:
        cmd.extend(["--reference"] + references)

    print(f"\n{'='*60}")
    print(f"Generating F{frame_num:02d} (attempt {attempt})")
    print(f"  References: {references}")
    print(f"  Output: {output_path}")
    print(f"{'='*60}")

    result = subprocess.run(cmd, capture_output=False, text=True)

    if result.returncode != 0:
        print(f"Error: Generation failed for F{frame_num:02d} attempt {attempt}", file=sys.stderr)
        return None

    if output_path.exists():
        print(f"  Generated: {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")
        return output_path
    else:
        print(f"  Error: Output file not created", file=sys.stderr)
        return None


def approve_frame(frame_num: int, candidate_path: Path, run_dir: Path) -> Path:
    approved_path = run_dir / "approved" / f"PT_A1_F{frame_num:02d}_key.png"
    shutil.copy2(candidate_path, approved_path)

    log_entry = {
        "frame": f"F{frame_num:02d}",
        "action": "approved",
        "source": str(candidate_path),
        "destination": str(approved_path),
        "timestamp": datetime.now().isoformat(),
    }

    audit_log = run_dir / "audit" / "audit_log.jsonl"
    with open(audit_log, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"  Approved: {approved_path.name}")
    return approved_path


def reject_frame(frame_num: int, candidate_path: Path, fail_code: str, run_dir: Path):
    attempt = candidate_path.stem.split("_")[-1]
    rejected_name = f"F{frame_num:02d}_attempt_{attempt}_{fail_code}.png"
    rejected_path = run_dir / "rejected" / rejected_name
    shutil.copy2(candidate_path, rejected_path)

    log_entry = {
        "frame": f"F{frame_num:02d}",
        "action": "rejected",
        "fail_code": fail_code,
        "source": str(candidate_path),
        "destination": str(rejected_path),
        "timestamp": datetime.now().isoformat(),
    }

    audit_log = run_dir / "audit" / "audit_log.jsonl"
    with open(audit_log, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"  Rejected: {rejected_name}")


def get_frames_to_generate(manifest: dict, chain: int | None = None, frame: str | None = None) -> list[dict]:
    keyframes = manifest["act1"]["keyframes"]

    if frame:
        frame_num = int(frame.replace("F", ""))
        return [kf for kf in keyframes if kf["frame"] == frame_num and kf.get("source") != "anchor"]

    if chain is not None:
        chain_key = f"chain_{chain}"
        chain_frames = manifest["act1"]["generation_chains"].get(chain_key, [])
        frame_nums = [int(f.replace("F", "")) for f in chain_frames]
        return [kf for kf in keyframes if kf["frame"] in frame_nums]

    # All non-anchor frames
    return [kf for kf in keyframes if kf.get("source") != "anchor"]


def main():
    parser = argparse.ArgumentParser(description="Pencil Test — Generation Orchestrator")
    parser.add_argument("--manifest", default="manifest.yaml", help="Path to manifest.yaml")
    parser.add_argument("--frame", help="Generate a specific frame (e.g., F06)")
    parser.add_argument("--chain", type=int, help="Generate a specific chain (1 or 2)")
    parser.add_argument("--run-dir", help="Use existing run directory instead of creating new one")
    parser.add_argument("--prompt", help="Override prompt (for retries with corrections)")
    parser.add_argument("--prompt-file", help="Read prompt from a text file")
    parser.add_argument("--approve", action="store_true", help="Approve the latest candidate for the specified frame")
    parser.add_argument("--reject", help="Reject with fail code (e.g., SF01, HF02)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated without running")
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)

    # Initialize or resume run
    if args.run_dir:
        run_dir = Path(args.run_dir)
        if not run_dir.exists():
            print(f"Error: Run directory not found: {run_dir}", file=sys.stderr)
            sys.exit(1)
    else:
        run_dir = create_run_dir()
        lock_manifest(args.manifest, run_dir)
        copy_anchor_frames(manifest, run_dir)
        print(f"Initialized run: {run_dir}")

    # Handle approve/reject actions on existing run
    if args.approve and args.frame:
        frame_num = int(args.frame.replace("F", ""))
        candidates_dir = run_dir / "candidates" / f"F{frame_num:02d}"
        latest = sorted(candidates_dir.glob("attempt_*.png"))
        if not latest:
            print(f"Error: No candidates for {args.frame}", file=sys.stderr)
            sys.exit(1)
        approve_frame(frame_num, latest[-1], run_dir)
        return

    if args.reject and args.frame:
        frame_num = int(args.frame.replace("F", ""))
        candidates_dir = run_dir / "candidates" / f"F{frame_num:02d}"
        latest = sorted(candidates_dir.glob("attempt_*.png"))
        if not latest:
            print(f"Error: No candidates for {args.frame}", file=sys.stderr)
            sys.exit(1)
        reject_frame(frame_num, latest[-1], args.reject, run_dir)
        return

    frames = get_frames_to_generate(manifest, chain=args.chain, frame=args.frame)

    if not frames:
        print("No frames to generate.")
        return

    frame_labels = [f"F{kf['frame']:02d}" for kf in frames]
    print(f"\nFrames to generate: {frame_labels}")

    if args.dry_run:
        for kf in frames:
            fnum = kf["frame"]
            refs = resolve_references(kf, manifest, run_dir)
            print(f"  F{fnum:02d} ({kf['label']}): {kf['pose']}")
            print(f"    References: {refs}")
        return

    # Generate each frame in order
    for kf in frames:
        frame_num = kf["frame"]
        references = resolve_references(kf, manifest, run_dir)

        # Load prompt: --prompt flag > --prompt-file > placeholder
        if args.prompt:
            prompt = args.prompt
        elif args.prompt_file:
            prompt = Path(args.prompt_file).read_text().strip()
        else:
            prompt_file = Path(f"prompts/F{frame_num:02d}.txt")
            if not prompt_file.exists():
                prompt_file = Path(f"prompts/COMPLETED/F{frame_num:02d}.txt")
            if prompt_file.exists():
                prompt = prompt_file.read_text().strip()
            else:
                print(f"  No prompt found. Provide --prompt, --prompt-file, or create prompts/F{frame_num:02d}.txt or prompts/COMPLETED/F{frame_num:02d}.txt")
                continue

        candidate = generate_frame(frame_num, prompt, references, manifest, run_dir)

        if candidate:
            print(f"\n  F{frame_num:02d} generated. Review the image and then:")
            print(f"    Approve: python3 pipeline/generate.py --manifest {args.manifest} --run-dir {run_dir} --frame F{frame_num:02d} --approve")
            print(f"    Reject:  python3 pipeline/generate.py --manifest {args.manifest} --run-dir {run_dir} --frame F{frame_num:02d} --reject SF01")

    print(f"\nRun directory: {run_dir}")
    print(f"Review candidates in: {run_dir}/candidates/")


if __name__ == "__main__":
    main()
