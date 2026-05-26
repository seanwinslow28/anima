#!/usr/bin/env python3
"""
Pencil Test Animation — Audit Script

Performs QA checks on generated keyframe candidates:
- HF01 (aspect ratio): Automated PIL check — 16:9 within 2% tolerance
- HF02-HF05, SF01-SF05: Outputs structured prompts for Claude Code vision review

Usage:
    python3 pipeline/audit.py --run-dir runs/run_2026-04-04_001 --frame F06 --attempt 1
    python3 pipeline/audit.py --run-dir runs/run_2026-04-04_001 --frame F06 --attempt 1 --approve
    python3 pipeline/audit.py --run-dir runs/run_2026-04-04_001 --frame F06 --attempt 1 --reject SF01
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


def check_aspect_ratio(image_path: Path, target_ratio: float = 16 / 9, tolerance: float = 0.02) -> dict:
    """HF01: Check image aspect ratio via PIL."""
    try:
        from PIL import Image
    except ImportError:
        return {
            "code": "HF01",
            "name": "Wrong aspect ratio",
            "result": "SKIP",
            "notes": "PIL not installed — run: pip install Pillow",
        }

    img = Image.open(image_path)
    width, height = img.size
    actual_ratio = width / height
    deviation = abs(actual_ratio - target_ratio) / target_ratio

    passed = deviation <= tolerance
    return {
        "code": "HF01",
        "name": "Wrong aspect ratio",
        "result": "PASS" if passed else "HARD_FAIL",
        "dimensions": f"{width}x{height}",
        "actual_ratio": round(actual_ratio, 4),
        "target_ratio": round(target_ratio, 4),
        "deviation": f"{deviation:.2%}",
    }


def get_vision_review_prompt(frame_num: int, pose_description: str, anchor_path: str) -> str:
    """Generate a structured prompt for Claude Code vision review."""
    return f"""## Vision Audit — F{frame_num:02d}

Review this generated keyframe against the A-2 anchor and storyboard requirements.

**Expected pose:** {pose_description}
**Anchor reference:** {anchor_path}

### Hard Fail Checks (any = reject immediately)

- [ ] **HF02 — Paper texture:** Is the background warm cream (#FAF5E8 approximate) with visible paper grain? (FAIL if pure white, gray, or flat)
- [ ] **HF03 — Direction:** Does the character face the correct direction per the storyboard?
- [ ] **HF04 — Pose:** Does the pose match "{pose_description}"? (FAIL if fundamentally wrong — e.g., arms down when should be raised)
- [ ] **HF05 — Aesthetic:** Does this look like a pencil test drawing? (FAIL if digital, anime, 3D render, or cel-shaded)

### Soft Fail Checks (any = trigger retry with corrections)

- [ ] **SF01 — Style drift:** Are line weights consistent with A-2? Construction lines visible? Cross-hatching present in shadows?
- [ ] **SF02 — Identity drift:** Does Sean's face match A-2? Check: hair shape, jaw angle, eye spacing, nose.
- [ ] **SF03 — Proportion drift:** Is head-to-body ratio consistent with A-2? Check arm length, overall height, shoulder width.
- [ ] **SF04 — Paper texture:** Are hole-punch marks at bottom? Production label (A-#) in top-left? Paper grain visible?
- [ ] **SF05 — Expression:** Does the facial expression match the beat description?

### Verdict

Rate each check PASS or FAIL, then provide overall verdict:
- **APPROVE** — All hard checks pass, no more than 1 minor soft fail
- **RETRY** — Hard checks pass but soft fails need correction (list which SF codes)
- **REJECT** — Any hard fail (list which HF codes)
"""


def log_audit(run_dir: Path, frame: str, attempt: int, result: str,
              hard_fails: list = None, soft_fails: list = None, notes: str = ""):
    entry = {
        "frame": frame,
        "attempt": attempt,
        "timestamp": datetime.now().isoformat(),
        "hard_fails": hard_fails or [],
        "soft_fails": soft_fails or [],
        "notes": notes,
        "result": result,
    }

    audit_log = run_dir / "audit" / "audit_log.jsonl"
    with open(audit_log, "a") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"  Logged: {result} for {frame} attempt {attempt}")
    return entry


def approve_frame(run_dir: Path, frame: str, attempt: int):
    frame_num = int(frame.replace("F", ""))
    candidate = run_dir / "candidates" / f"F{frame_num:02d}" / f"attempt_{attempt:02d}.png"

    if not candidate.exists():
        print(f"Error: Candidate not found: {candidate}", file=sys.stderr)
        sys.exit(1)

    approved = run_dir / "approved" / f"PT_A1_F{frame_num:02d}_key.png"
    shutil.copy2(candidate, approved)
    log_audit(run_dir, frame, attempt, "APPROVED", notes="Manual approval")
    print(f"  Approved: {candidate.name} -> {approved.name}")


def reject_frame(run_dir: Path, frame: str, attempt: int, fail_code: str):
    frame_num = int(frame.replace("F", ""))
    candidate = run_dir / "candidates" / f"F{frame_num:02d}" / f"attempt_{attempt:02d}.png"

    if not candidate.exists():
        print(f"Error: Candidate not found: {candidate}", file=sys.stderr)
        sys.exit(1)

    rejected_name = f"F{frame_num:02d}_attempt_{attempt:02d}_{fail_code}.png"
    rejected = run_dir / "rejected" / rejected_name
    shutil.copy2(candidate, rejected)

    is_hard = fail_code.startswith("HF")
    hard_fails = [fail_code] if is_hard else []
    soft_fails = [fail_code] if not is_hard else []
    result = "REJECTED" if is_hard else "RETRY"

    log_audit(run_dir, frame, attempt, result, hard_fails=hard_fails, soft_fails=soft_fails)
    print(f"  {result}: {candidate.name} -> {rejected_name}")


def generate_run_summary(run_dir: Path):
    audit_log = run_dir / "audit" / "audit_log.jsonl"
    if not audit_log.exists():
        print("No audit log found.")
        return

    entries = []
    with open(audit_log) as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))

    def get_result(e):
        return e.get("result", e.get("action", "unknown")).upper()

    total = len(entries)
    approved = sum(1 for e in entries if get_result(e) == "APPROVED")
    retries = sum(1 for e in entries if get_result(e) == "RETRY")
    rejected = sum(1 for e in entries if get_result(e) == "REJECTED")

    all_hard = []
    all_soft = []
    for e in entries:
        all_hard.extend(e.get("hard_fails", []))
        all_soft.extend(e.get("soft_fails", []))

    summary = {
        "run_dir": str(run_dir),
        "timestamp": datetime.now().isoformat(),
        "total_evaluations": total,
        "approved": approved,
        "retries": retries,
        "rejected": rejected,
        "top_hard_fails": {code: all_hard.count(code) for code in set(all_hard)},
        "top_soft_fails": {code: all_soft.count(code) for code in set(all_soft)},
    }

    summary_path = run_dir / "audit" / "run_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nRun Summary:")
    print(f"  Total evaluations: {total}")
    print(f"  Approved: {approved}")
    print(f"  Retries: {retries}")
    print(f"  Rejected: {rejected}")
    if all_hard:
        print(f"  Top hard fails: {summary['top_hard_fails']}")
    if all_soft:
        print(f"  Top soft fails: {summary['top_soft_fails']}")


def main():
    if os.environ.get("USE_DAG_RUNNER") == "1":
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        from pipeline.dag import run_from_legacy_cli
        return run_from_legacy_cli(node_id="audit_gate", argv=sys.argv[1:])
    parser = argparse.ArgumentParser(description="Pencil Test — Audit Script")
    parser.add_argument("--run-dir", required=True, help="Path to run directory")
    parser.add_argument("--frame", help="Frame to audit (e.g., F06)")
    parser.add_argument("--attempt", type=int, default=1, help="Attempt number to audit")
    parser.add_argument("--approve", action="store_true", help="Approve the frame")
    parser.add_argument("--reject", help="Reject with fail code (e.g., SF01, HF02)")
    parser.add_argument("--summary", action="store_true", help="Generate run summary")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    if not run_dir.exists():
        print(f"Error: Run directory not found: {run_dir}", file=sys.stderr)
        sys.exit(1)

    if args.summary:
        generate_run_summary(run_dir)
        return

    if not args.frame:
        print("Error: --frame is required (e.g., --frame F06)", file=sys.stderr)
        sys.exit(1)

    if args.approve:
        approve_frame(run_dir, args.frame, args.attempt)
        return

    if args.reject:
        reject_frame(run_dir, args.frame, args.attempt, args.reject)
        return

    # Default: run automated checks and print vision review prompt
    frame_num = int(args.frame.replace("F", ""))
    candidate = run_dir / "candidates" / f"F{frame_num:02d}" / f"attempt_{args.attempt:02d}.png"

    if not candidate.exists():
        print(f"Error: Candidate not found: {candidate}", file=sys.stderr)
        sys.exit(1)

    print(f"Auditing: {candidate}")
    print()

    # HF01: Automated aspect ratio check
    hf01 = check_aspect_ratio(candidate)
    print(f"HF01 ({hf01['name']}): {hf01['result']}")
    if hf01.get("dimensions"):
        print(f"  Dimensions: {hf01['dimensions']}, Ratio: {hf01['actual_ratio']}, Deviation: {hf01['deviation']}")

    if hf01["result"] == "HARD_FAIL":
        print(f"\n  HARD FAIL — Wrong aspect ratio. Reject this candidate.")
        log_audit(run_dir, args.frame, args.attempt, "REJECTED",
                  hard_fails=["HF01"], notes=f"Aspect ratio: {hf01.get('dimensions', 'unknown')}")
        return

    # Print vision review prompt for remaining checks
    # (Claude Code will read the image and evaluate)
    print(f"\n{'='*60}")
    print("VISION REVIEW REQUIRED")
    print(f"{'='*60}")
    print(f"\nRead the candidate image at: {candidate}")
    print(f"Compare against anchor at: images/2D-Character-Sketch-Sean-v1.png")
    print()

    # Find pose description from manifest
    try:
        import yaml
        with open("manifest.yaml") as f:
            manifest = yaml.safe_load(f)
        keyframes = manifest["act1"]["keyframes"]
        pose = next((kf["pose"] for kf in keyframes if kf["frame"] == frame_num), "unknown")
    except Exception:
        pose = "see storyboard"

    print(get_vision_review_prompt(frame_num, pose, "images/2D-Character-Sketch-Sean-v1.png"))


if __name__ == "__main__":
    main()
