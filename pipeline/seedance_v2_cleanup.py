#!/usr/bin/env python3
"""Drive Nano Banana 2 cleanup on Seedance v2 frames per selection.md.

For each KEEP row in selection.md:
  - Build the per-frame reference list (A-2 + beat-matched A-N + Seedance source + optional prev-cleaned).
  - Invoke the gemini-pencil-animation-image-gen generate_image.py with the universal cleanup prompt.
  - Post-process: re-encode through PIL (fix JPEG-as-PNG), resize to 1376x768.
  - Hand off to the audit step (caller decides what to do with the verdict).
  - Retry ladder (attempts 1-3) on soft fails; stop at attempt 4 and flag.

Usage:
    python3 pipeline/seedance_v2_cleanup.py \\
        --selection runs/{run_id}/seedance_frames/selection.md \\
        --source-dir runs/{run_id}/seedance_frames/raw_24fps \\
        --clean-dir runs/{run_id}/seedance_clean_v2 \\
        --run-dir runs/{run_id} \\
        --slot-range 029-068    # for the spike; omit for full batch
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

from pipeline.seedance_v2_select import SelectionRow, parse_selection_md, validate_selection


UNIVERSAL_PROMPT = (
    "Restore this frame to traditional hand-drawn pencil animation on cream "
    "paper #FAF5E8. Match the line weight, graphite shading, paper grain, "
    "hole-punch marks, and construction-mark style of the A-2 reference. "
    "Keep the character's pose, position, expression, and gesture EXACTLY "
    "as shown in the input frame — only redraw it in pencil-test fidelity. "
    "The stylus must remain in the character's RIGHT hand. The orange "
    "creature companion, if present, stays in its exact position with its "
    "exact shape and color — do not redraw it as a pixel sprite or armored "
    "figure.\n\n"
    "NEGATIVES: no vector lines, no black outlines, no cel shading, no "
    "anime style, no saturation other than the orange of the companion, no "
    "digital painting, no gradients, no airbrush, no pure white background, "
    "no pure black lines, no pixel art, no armored or spiky humanoid figures."
)

ATTEMPT_2_ADDENDUM = (
    "\n\nIDENTITY CORRECTION: The face must match the A-2 reference exactly — "
    "same jaw shape, same hair part, same eye spacing, same brow line."
)

ATTEMPT_3_ADDENDUM = (
    "\n\nPAPER TEXTURE: Visible cream paper grain across the full background, "
    "with subtle hole-punch marks along the lower edge and a small production "
    "label in the upper-left corner. Construction marks and graphite "
    "smudging visible around the figure."
)

GENERATE_IMAGE_SCRIPT = (
    ".claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py"
)


def retry_attempt_prompt(attempt: int) -> str:
    if attempt == 1:
        return UNIVERSAL_PROMPT
    if attempt == 2:
        return UNIVERSAL_PROMPT + ATTEMPT_2_ADDENDUM
    if attempt == 3:
        return UNIVERSAL_PROMPT + ATTEMPT_2_ADDENDUM + ATTEMPT_3_ADDENDUM
    raise ValueError(f"No prompt defined for attempt {attempt}")


def parse_slot_range(spec: str | None) -> range | None:
    """Parse '029-068' → range(29, 69). Returns None if spec is None."""
    if spec is None:
        return None
    lo, hi = spec.split("-")
    return range(int(lo), int(hi) + 1)


def build_references(
    row: SelectionRow,
    *,
    source_dir: Path,
    anchor_root: Path,
    a2_anchor: str,
    prev_cleaned: Path | None,
) -> list[Path]:
    """Build the ordered reference list for this row's NB2 cleanup call."""
    refs: list[Path] = [anchor_root / a2_anchor]
    for a in row.anchors:
        candidate = anchor_root / a
        if candidate == anchor_root / a2_anchor:
            continue  # don't duplicate A-2
        refs.append(candidate)
    refs.append(source_dir / row.source_frame)
    if row.cadence == "24fps" and prev_cleaned is not None:
        refs.append(prev_cleaned)
    return refs


def reencode_and_resize(path: Path, target_size: tuple[int, int] = (1376, 768)) -> None:
    """Fix JPEG-as-PNG codec issue and normalize to existing approved-frame size."""
    im = Image.open(path).convert("RGB").resize(target_size, Image.LANCZOS)
    im.save(path, "PNG")


def run_cleanup_for_slot(
    row: SelectionRow,
    *,
    run_dir: Path,
    source_dir: Path,
    clean_dir: Path,
    anchor_root: Path,
    a2_anchor: str,
    prev_cleaned: Path | None,
    attempt: int,
) -> Path:
    """Run a single NB2 cleanup attempt. Returns the output path."""
    out_name = f"PT_A1_v2_slot{row.slot:03d}_attempt_{attempt:02d}.png"
    out_path = clean_dir / out_name
    clean_dir.mkdir(parents=True, exist_ok=True)
    refs = build_references(
        row,
        source_dir=source_dir,
        anchor_root=anchor_root,
        a2_anchor=a2_anchor,
        prev_cleaned=prev_cleaned,
    )
    cmd = [
        "python3",
        GENERATE_IMAGE_SCRIPT,
        retry_attempt_prompt(attempt),
        "--output",
        str(out_path),
        "--aspect-ratio",
        "16:9",
        "--reference",
        *[str(r) for r in refs],
        "--env-file",
        ".env",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(
            f"generate_image.py failed for slot {row.slot} attempt {attempt}:\n"
            f"stderr: {result.stderr}"
        )
    if not out_path.exists():
        raise RuntimeError(
            f"generate_image.py exited 0 but did not write {out_path} for slot {row.slot} attempt {attempt}"
        )
    reencode_and_resize(out_path)
    return out_path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selection", type=Path, required=True)
    ap.add_argument("--source-dir", type=Path, required=True)
    ap.add_argument("--clean-dir", type=Path, required=True)
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument(
        "--anchor-root",
        type=Path,
        default=None,
        help="Root for resolving anchor paths in selection.md (default: derived from --selection path)",
    )
    ap.add_argument(
        "--a2-anchor",
        default="approved/PT_A1_F01_key.png",
        help="Path (under anchor-root) to the A-2 anchor; always reference #1",
    )
    ap.add_argument(
        "--slot-range",
        default=None,
        help="Inclusive range of slots to run, e.g. '029-068' for the spike",
    )
    ap.add_argument(
        "--first-attempt-only",
        action="store_true",
        help="Skip retry ladder (used for the rough-cut pass)",
    )
    args = ap.parse_args()

    anchor_root = args.anchor_root if args.anchor_root is not None else args.selection.parent.parent
    args.clean_dir.mkdir(parents=True, exist_ok=True)

    rows = parse_selection_md(args.selection)
    errors = validate_selection(rows, anchor_root)
    if errors:
        for e in errors:
            print(f"  ERROR: {e}", file=sys.stderr)
        return 1

    slot_filter = parse_slot_range(args.slot_range)
    keep_rows = [
        r
        for r in rows
        if r.decision == "KEEP"
        and (slot_filter is None or r.slot in slot_filter)
    ]
    print(f"Running cleanup on {len(keep_rows)} slot(s)")

    prev_cleaned: Path | None = None
    prev_cadence: str | None = None
    failures: list[int] = []
    for row in keep_rows:
        # Reset chained-ref at cadence boundaries: a 24fps run starts fresh
        # when the previous frame was 12fps (a different beat).
        if row.cadence != prev_cadence:
            prev_cleaned = None
        success = False
        chosen_attempt: int | None = None
        for attempt in (1, 2, 3):
            try:
                out_path = run_cleanup_for_slot(
                    row,
                    run_dir=args.run_dir,
                    source_dir=args.source_dir,
                    clean_dir=args.clean_dir,
                    anchor_root=anchor_root,
                    a2_anchor=args.a2_anchor,
                    prev_cleaned=prev_cleaned,
                    attempt=attempt,
                )
            except (RuntimeError, subprocess.TimeoutExpired) as e:
                print(f"  Slot {row.slot:03d} attempt {attempt}: ERROR — {e}", file=sys.stderr)
                continue
            print(f"  Slot {row.slot:03d} attempt {attempt}: {out_path}")
            # In rough-cut mode, accept attempt 1 unconditionally.
            if args.first_attempt_only:
                success = True
                chosen_attempt = attempt
                break
            # The retry loop above only re-iterates on subprocess failures
            # (RuntimeError / TimeoutExpired). Soft-fail retries (style drift,
            # identity drift, etc.) are NOT driven by this script — they are
            # invoked manually for flagged slots via direct library calls to
            # run_cleanup_for_slot(...attempt=2 or 3...) per Task 7 Step 7.
            # `args.first_attempt_only` is preserved for the rough-cut pass
            # described in Task 7 Step 2; both branches currently do the same
            # thing because soft-fail audit is run separately.
            success = True
            chosen_attempt = attempt
            break
        if success and chosen_attempt is not None:
            # Promote chosen attempt to the stable filename for assembly to consume.
            chosen = args.clean_dir / f"PT_A1_v2_slot{row.slot:03d}_attempt_{chosen_attempt:02d}.png"
            stable = args.clean_dir / f"PT_A1_v2_slot{row.slot:03d}.png"
            if chosen.exists():
                shutil.copy(chosen, stable)
                prev_cleaned = stable
                prev_cadence = row.cadence
        else:
            failures.append(row.slot)

    if failures:
        print(f"\n{len(failures)} slot(s) failed cleanup: {failures}", file=sys.stderr)
        return 1
    print(f"\nCompleted cleanup on {len(keep_rows)} slot(s); outputs in {args.clean_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
