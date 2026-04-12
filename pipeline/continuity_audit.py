#!/usr/bin/env python3
"""
Pencil Test Animation — Continuity Audit

Post-run review that checks frame-to-frame continuity across the full
approved keyframe set. Designed to be run by Claude Code using vision
capabilities — outputs structured review prompts for each continuity
dimension.

Usage:
    python3 pipeline/continuity_audit.py --run-dir runs/run_2026-04-04_174805

This script:
1. Verifies all expected approved frames exist
2. Outputs a structured continuity review checklist for Claude Code vision
3. Logs continuity findings to audit/continuity_log.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


# Continuity dimensions to check between consecutive frames
CONTINUITY_CHECKS = [
    {
        "id": "CC01",
        "name": "Prop tracking — stylus hand",
        "description": "Which hand holds the stylus? Must be the CHARACTER'S RIGHT HAND in every frame unless the storyboard explicitly describes a hand switch.",
        "severity": "blocker",
        "ground_truth": "The stylus is in Sean's RIGHT hand (the hand on the LEFT side of the image when the character faces camera) in the A-2 anchor. It must stay in the RIGHT hand throughout Act 1.",
    },
    {
        "id": "CC02",
        "name": "Prop tracking — stylus presence",
        "description": "Is the stylus visible in every frame? It should be present in all Act 1 frames.",
        "severity": "blocker",
    },
    {
        "id": "CC03",
        "name": "Clothing consistency",
        "description": "Same dark navy crew-neck t-shirt, same slim jeans with cuffed ankles, same casual sneakers in every frame. No clothing changes, additions, or removals.",
        "severity": "blocker",
    },
    {
        "id": "CC04",
        "name": "Character facing direction",
        "description": "Character should maintain general 3/4 facing direction (slightly angled toward camera) across the sequence. Only the head turns — the torso should not flip orientation between frames unless the storyboard describes it.",
        "severity": "warning",
    },
    {
        "id": "CC05",
        "name": "Character scale and position",
        "description": "Character should be approximately the same height and occupy the same vertical region of the frame across all keyframes. Significant size jumps between consecutive frames indicate a proportion error.",
        "severity": "warning",
    },
    {
        "id": "CC06",
        "name": "Hair consistency",
        "description": "Hair shape, volume, color, and part direction should be consistent. Sandy blonde, swept to the character's right. Minor dynamic variations (bounce on F10) are expected but the base shape shouldn't change.",
        "severity": "warning",
    },
    {
        "id": "CC07",
        "name": "Foot position and ground plane",
        "description": "Feet should be on a consistent ground plane. The character shouldn't appear to float or sink between frames. Stance width should be consistent unless the pose calls for a shift.",
        "severity": "warning",
    },
    {
        "id": "CC08",
        "name": "Expression arc continuity",
        "description": "The expression should follow the emotional arc: neutral (F01) → contemplative (F06) → excited (F10) → focused (F13) → joyful (F18) → satisfied (F31) → nod (F36) → neutral (F40). No emotional jumps that break the sequence logic.",
        "severity": "warning",
    },
]

# Expected frame sequence for Act 1
ACT1_FRAMES = [
    {"frame": 1, "label": "A-2", "pose": "idle hold", "beat": "anchor"},
    {"frame": 6, "label": "A-3", "pose": "glance down", "beat": "contemplative"},
    {"frame": 10, "label": "A-4", "pose": "the spark", "beat": "excited"},
    {"frame": 13, "label": "A-5", "pose": "wind up", "beat": "focused anticipation"},
    {"frame": 18, "label": "A-6", "pose": "mid-gesture", "beat": "joyful action"},
    {"frame": 31, "label": "A-7", "pose": "sprite lands", "beat": "quiet pride"},
    {"frame": 36, "label": "A-8", "pose": "the nod", "beat": "satisfied nod"},
    {"frame": 40, "label": "A-9", "pose": "return to idle", "beat": "settled"},
]


def check_approved_frames(run_dir: Path) -> list[dict]:
    """Verify all expected approved frames exist."""
    approved_dir = run_dir / "approved"
    results = []
    for frame_info in ACT1_FRAMES:
        fnum = frame_info["frame"]
        path = approved_dir / f"PT_A1_F{fnum:02d}_key.png"
        results.append({
            "frame": f"F{fnum:02d}",
            "label": frame_info["label"],
            "path": str(path),
            "exists": path.exists(),
            "size_kb": round(path.stat().st_size / 1024, 1) if path.exists() else 0,
        })
    return results


def generate_continuity_review_prompt(run_dir: Path) -> str:
    """Generate a structured prompt for Claude Code to perform the continuity review."""
    approved_dir = run_dir / "approved"

    frame_paths = []
    for fi in ACT1_FRAMES:
        fnum = fi["frame"]
        path = approved_dir / f"PT_A1_F{fnum:02d}_key.png"
        if path.exists():
            frame_paths.append(f"- F{fnum:02d} ({fi['label']}, {fi['pose']}): `{path}`")

    frames_list = "\n".join(frame_paths)

    checks_list = ""
    for check in CONTINUITY_CHECKS:
        severity_tag = "BLOCKER" if check["severity"] == "blocker" else "WARNING"
        checks_list += f"\n### {check['id']} — {check['name']} [{severity_tag}]\n"
        checks_list += f"{check['description']}\n"
        if "ground_truth" in check:
            checks_list += f"\n**Ground truth:** {check['ground_truth']}\n"
        checks_list += "\n| Transition | Result | Notes |\n|------------|--------|-------|\n"
        for i in range(len(ACT1_FRAMES) - 1):
            f_from = ACT1_FRAMES[i]
            f_to = ACT1_FRAMES[i + 1]
            checks_list += f"| F{f_from['frame']:02d} → F{f_to['frame']:02d} | ___ | |\n"
        checks_list += "\n"

    return f"""# Continuity Audit — Act 1 Keyframes

## Instructions

Review ALL approved keyframes in sequence. For each continuity dimension below,
check every frame-to-frame transition and mark PASS, FAIL, or N/A.

**Read each frame image** in order before filling out the checks.

## Approved Frames

{frames_list}

## Continuity Checks
{checks_list}

## Summary

After completing all checks:

1. List any BLOCKER failures (must be fixed before assembly)
2. List any WARNING failures (note for future improvement)
3. For each failure, specify:
   - Which frame(s) are affected
   - What the error is
   - Whether to REGENERATE the frame or accept with notes
4. If regenerating, specify what the corrected prompt should emphasize

## Verdict

- **PASS** — No blocker failures, acceptable continuity
- **CONDITIONAL PASS** — Warnings only, can ship with notes
- **FAIL** — Blocker failures found, must regenerate affected frames
"""


def generate_pairwise_review(run_dir: Path) -> str:
    """Generate a more compact pairwise review prompt."""
    approved_dir = run_dir / "approved"

    prompt = "# Continuity Audit — Pairwise Frame Review\n\n"
    prompt += "For each consecutive pair, read BOTH images and check:\n"
    prompt += "1. **Stylus hand** — same hand (character's RIGHT) in both frames?\n"
    prompt += "2. **Stylus visible** — present in both?\n"
    prompt += "3. **Clothing** — same outfit, no changes?\n"
    prompt += "4. **Scale/position** — similar height, ground plane?\n"
    prompt += "5. **Hair** — same shape, part, color?\n\n"

    for i in range(len(ACT1_FRAMES) - 1):
        f_from = ACT1_FRAMES[i]
        f_to = ACT1_FRAMES[i + 1]
        path_from = approved_dir / f"PT_A1_F{f_from['frame']:02d}_key.png"
        path_to = approved_dir / f"PT_A1_F{f_to['frame']:02d}_key.png"
        prompt += f"## F{f_from['frame']:02d} ({f_from['pose']}) → F{f_to['frame']:02d} ({f_to['pose']})\n"
        prompt += f"Read: `{path_from}` and `{path_to}`\n\n"

    return prompt


def save_continuity_log(run_dir: Path, findings: list[dict]):
    """Save continuity findings to the audit directory."""
    log_path = run_dir / "audit" / "continuity_log.json"
    log_data = {
        "run_dir": str(run_dir),
        "timestamp": datetime.now().isoformat(),
        "total_checks": len(CONTINUITY_CHECKS),
        "findings": findings,
    }
    with open(log_path, "w") as f:
        json.dump(log_data, f, indent=2)
    print(f"Continuity log saved: {log_path}")


def main():
    parser = argparse.ArgumentParser(description="Pencil Test — Continuity Audit")
    parser.add_argument("--run-dir", required=True, help="Path to run directory")
    parser.add_argument("--pairwise", action="store_true",
                        help="Generate compact pairwise review instead of full checklist")
    parser.add_argument("--log-finding", nargs=3, metavar=("CHECK_ID", "FRAMES", "NOTES"),
                        help="Log a finding: --log-finding CC01 F13 'stylus in wrong hand'")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    if not run_dir.exists():
        print(f"Error: Run directory not found: {run_dir}", file=sys.stderr)
        sys.exit(1)

    # Log a specific finding
    if args.log_finding:
        check_id, frames, notes = args.log_finding
        log_path = run_dir / "audit" / "continuity_log.json"
        if log_path.exists():
            with open(log_path) as f:
                log_data = json.load(f)
        else:
            log_data = {"run_dir": str(run_dir), "timestamp": datetime.now().isoformat(),
                        "total_checks": len(CONTINUITY_CHECKS), "findings": []}

        log_data["findings"].append({
            "check_id": check_id,
            "frames": frames,
            "notes": notes,
            "timestamp": datetime.now().isoformat(),
        })
        with open(log_path, "w") as f:
            json.dump(log_data, f, indent=2)
        print(f"Logged finding: {check_id} on {frames} — {notes}")
        return

    # Check all frames exist
    print("=== Continuity Audit ===")
    print(f"Run: {run_dir}\n")

    frame_status = check_approved_frames(run_dir)
    all_present = all(f["exists"] for f in frame_status)

    print("Approved frames:")
    for f in frame_status:
        status = "OK" if f["exists"] else "MISSING"
        print(f"  {f['frame']} ({f['label']}): {status} ({f['size_kb']} KB)")

    if not all_present:
        missing = [f["frame"] for f in frame_status if not f["exists"]]
        print(f"\nError: Missing frames: {missing}. Cannot run continuity audit.", file=sys.stderr)
        sys.exit(1)

    print(f"\nAll {len(frame_status)} frames present.\n")

    # Output review prompt
    print("=" * 60)
    print("CONTINUITY REVIEW — VISION CHECK REQUIRED")
    print("=" * 60)
    print()

    if args.pairwise:
        print(generate_pairwise_review(run_dir))
    else:
        print(generate_continuity_review_prompt(run_dir))

    print("\nTo log findings:")
    print(f'  python3 pipeline/continuity_audit.py --run-dir {run_dir} --log-finding CC01 F13 "stylus in wrong hand"')


if __name__ == "__main__":
    main()
