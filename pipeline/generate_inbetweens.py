#!/usr/bin/env python3
"""Generate in-between frames using ComfyUI OpenPose ControlNet.

Automates the full pipeline:
1. Copy keyframes to ComfyUI input
2. Extract DWPose skeletons from keyframes
3. Blend skeletons at Odd Rule ratios
4. Generate in-between frames with ControlNet + IPAdapter
5. Copy results back to pipeline approved/ directory

Requires ComfyUI running at http://127.0.0.1:8188
"""

import json
import time
import shutil
import argparse
import requests
from pathlib import Path

COMFYUI_URL = "http://127.0.0.1:8000"
COMFYUI_DIR = Path("/Users/seanwinslow/Code-Brain/Comfy-UI")
PIPELINE_DIR = Path("/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline")

# Odd Rule blend ratios for easing
# Cumulative ratios from 1:3:5:7 displacement pattern
EASING = {
    "ease_out_3": [0.14, 0.43, 0.71],     # 1/7, 3/7, 5/7 — slow start, fast end
    "ease_in_3": [0.14, 0.43, 0.71],      # same ratios, arc trajectory bakes the ease-in
    "ease_in_2": [0.29, 0.71],             # 2/7, 5/7 — fast start, slow end
    "linear_2": [0.33, 0.67],             # even spacing
    "linear_1": [0.50],                    # single midpoint
    "pop": [],                             # no in-betweens (snap)
}

# Transition definitions: (start_frame, end_frame, easing_type)
TRANSITIONS = [
    ("F01", "F06", "ease_out_3"),   # Slow settle — head glance down
    ("F06", "F10", "linear_1"),     # Head snap up — single in-between or pop
    ("F10", "F13", "linear_1"),     # Weight shift to ready pose
    ("F13", "F18", "ease_in_3"),    # Arm sweep arc — requires manual skeleton editing (not linear blend)
    # F18→F31 SKIP — transformation sequence F20-F28 exists
    ("F31", "F36", "linear_2"),     # Nod down
    ("F36", "F40", "ease_in_2"),    # Settle to idle (loop closure)
]


def copy_outputs_to_input(pattern: str):
    """Copy matching files from ComfyUI output/ to input/ so LoadImage can find them."""
    output_dir = COMFYUI_DIR / "output"
    input_dir = COMFYUI_DIR / "input"
    for f in output_dir.glob(pattern):
        dst = input_dir / f.name
        if not dst.exists():
            shutil.copy2(f, dst)


def queue_workflow(workflow: dict) -> str:
    """Queue a workflow and return the prompt_id."""
    resp = requests.post(f"{COMFYUI_URL}/prompt", json={"prompt": workflow})
    if not resp.ok:
        print(f"  ERROR {resp.status_code}: {resp.text[:500]}")
    resp.raise_for_status()
    return resp.json()["prompt_id"]


def wait_for_completion(prompt_id: str, timeout: int = 120) -> dict:
    """Poll until job completes, return history entry."""
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(f"{COMFYUI_URL}/history/{prompt_id}")
        if resp.ok:
            data = resp.json()
            if prompt_id in data:
                return data[prompt_id]
        time.sleep(2)
    raise TimeoutError(f"Job {prompt_id} did not complete within {timeout}s")


def copy_keyframes_to_comfyui(run_dir: Path, frames: list[str]):
    """Copy approved keyframes to ComfyUI input directory."""
    input_dir = COMFYUI_DIR / "input"
    for frame in frames:
        src = run_dir / "approved" / f"PT_A1_{frame}_key.png"
        if src.exists():
            dst = input_dir / f"PT_A1_{frame}_key.png"
            if not dst.exists():
                shutil.copy2(src, dst)
                print(f"  Copied {src.name} -> ComfyUI/input/")

    # Also copy A-2 anchor
    anchor = PIPELINE_DIR / "images" / "2D-Character-Sketch-Sean-v1.png"
    anchor_dst = input_dir / "2D-Character-Sketch-Sean-v1.png"
    if anchor.exists() and not anchor_dst.exists():
        shutil.copy2(anchor, anchor_dst)
        print(f"  Copied A-2 anchor -> ComfyUI/input/")


def extract_skeleton(frame: str) -> str:
    """Extract DWPose skeleton from a keyframe. Returns prompt_id."""
    workflow_path = PIPELINE_DIR / "workflows" / "skeleton_extract.json"
    with open(workflow_path) as f:
        workflow = json.load(f)

    # Set input image and output prefix
    workflow["1"]["inputs"]["image"] = f"PT_A1_{frame}_key.png"
    workflow["4"]["inputs"]["filename_prefix"] = f"skeleton_{frame}"

    print(f"  Extracting skeleton from {frame}...")
    return queue_workflow(workflow)


def blend_skeletons(frame_a: str, frame_b: str, blend_factor: float, ib_num: int) -> str:
    """Blend two skeleton images. Returns prompt_id."""
    workflow_path = PIPELINE_DIR / "workflows" / "skeleton_blend.json"
    with open(workflow_path) as f:
        workflow = json.load(f)

    # Find the skeleton images in ComfyUI output
    # SaveImage adds _00001 suffix, so we reference the output filename
    workflow["1"]["inputs"]["image"] = f"skeleton_{frame_a}_00001_.png"
    workflow["2"]["inputs"]["image"] = f"skeleton_{frame_b}_00001_.png"
    workflow["3"]["inputs"]["blend_factor"] = blend_factor
    workflow["5"]["inputs"]["filename_prefix"] = f"skeleton_{frame_a}to{frame_b}_IB{ib_num:02d}"

    print(f"  Blending skeletons {frame_a}+{frame_b} at {blend_factor:.2f} -> IB{ib_num:02d}")
    return queue_workflow(workflow)


def generate_inbetween(frame_a: str, frame_b: str, ib_num: int, seed: int = 42) -> str:
    """Generate an in-between frame from an interpolated skeleton. Returns prompt_id."""
    workflow_path = PIPELINE_DIR / "workflows" / "openpose_inbetween.json"
    with open(workflow_path) as f:
        workflow = json.load(f)

    # Set the interpolated skeleton image
    skeleton_name = f"skeleton_{frame_a}to{frame_b}_IB{ib_num:02d}_00001_.png"
    workflow["6"]["inputs"]["image"] = skeleton_name

    # Set seed and output prefix
    workflow["13"]["inputs"]["seed"] = seed
    workflow["16"]["inputs"]["filename_prefix"] = f"PT_A1_{frame_a}to{frame_b}_IB{ib_num:02d}"

    print(f"  Generating in-between {frame_a}→{frame_b} IB{ib_num:02d} (seed={seed})...")
    return queue_workflow(workflow)


def run_transition(frame_a: str, frame_b: str, easing_type: str, seed_base: int = 42):
    """Run the full pipeline for one transition."""
    ratios = EASING[easing_type]
    if not ratios:
        print(f"\n[{frame_a}→{frame_b}] Pop transition — no in-betweens needed")
        return

    print(f"\n[{frame_a}→{frame_b}] {len(ratios)} in-betweens ({easing_type})")

    # Step 1: Extract skeletons (if not already done)
    skel_a_id = extract_skeleton(frame_a)
    skel_b_id = extract_skeleton(frame_b)
    wait_for_completion(skel_a_id)
    wait_for_completion(skel_b_id)
    # Copy skeleton outputs to input/ so blend workflow can LoadImage them
    copy_outputs_to_input("skeleton_*.png")
    print(f"  Skeletons extracted.")

    # Step 2: Blend skeletons
    blend_ids = []
    for i, ratio in enumerate(ratios, 1):
        pid = blend_skeletons(frame_a, frame_b, ratio, i)
        blend_ids.append(pid)

    for pid in blend_ids:
        wait_for_completion(pid)
    # Copy blended skeletons to input/ for generation workflow
    copy_outputs_to_input("skeleton_*IB*.png")
    print(f"  Skeleton interpolation complete.")

    # Step 3: Generate in-betweens
    gen_ids = []
    for i in range(1, len(ratios) + 1):
        pid = generate_inbetween(frame_a, frame_b, i, seed=seed_base + i)
        gen_ids.append(pid)

    for pid in gen_ids:
        wait_for_completion(pid, timeout=180)
    print(f"  In-between generation complete!")


def main():
    parser = argparse.ArgumentParser(description="Generate in-between frames via ComfyUI")
    parser.add_argument("--run-dir", type=Path,
                        default=PIPELINE_DIR / "runs" / "run_2026-04-04_174805",
                        help="Path to the run directory with approved keyframes")
    parser.add_argument("--transition", type=str, default=None,
                        help="Run a single transition, e.g. 'F01-F06'")
    parser.add_argument("--seed", type=int, default=42,
                        help="Base seed for generation")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print plan without executing")
    args = parser.parse_args()

    # Collect all unique frames
    all_frames = set()
    transitions = TRANSITIONS
    if args.transition:
        parts = args.transition.split("-")
        transitions = [(parts[0], parts[1],
                        next(t[2] for t in TRANSITIONS if t[0] == parts[0] and t[1] == parts[1]))]
    for t in transitions:
        all_frames.add(t[0])
        all_frames.add(t[1])

    print("=" * 60)
    print("ComfyUI In-Between Generation Pipeline")
    print("=" * 60)
    print(f"\nTransitions: {len(transitions)}")
    total_ibs = sum(len(EASING[t[2]]) for t in transitions)
    print(f"Total in-betweens to generate: {total_ibs}")
    print(f"Keyframes needed: {sorted(all_frames)}")

    if args.dry_run:
        print("\n[DRY RUN] Would generate:")
        for fa, fb, easing in transitions:
            ratios = EASING[easing]
            print(f"  {fa}→{fb}: {len(ratios)} frames, ratios={ratios} ({easing})")
        return

    # Check ComfyUI is running
    try:
        requests.get(f"{COMFYUI_URL}/system_stats", timeout=5)
    except requests.ConnectionError:
        print("\nERROR: ComfyUI is not running at", COMFYUI_URL)
        print("Please start ComfyUI Desktop and try again.")
        return

    # Copy keyframes to ComfyUI input
    print("\nCopying keyframes to ComfyUI input...")
    copy_keyframes_to_comfyui(args.run_dir, sorted(all_frames))

    # Run each transition
    for frame_a, frame_b, easing in transitions:
        run_transition(frame_a, frame_b, easing, seed_base=args.seed)

    print("\n" + "=" * 60)
    print("All in-betweens generated!")
    print(f"Check ComfyUI/output/ for results.")
    print("Run audit.py on each output before approving.")
    print("=" * 60)


if __name__ == "__main__":
    main()
