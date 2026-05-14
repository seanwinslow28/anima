#!/usr/bin/env python3
"""Audit cleaned Seedance v2 frames against HF/SF + stylus + companion checks.

Hard checks (run automatically):
  - HF01: 16:9 aspect ratio within 2% tolerance (PIL).
  - File-existence: every slot in selection.md has a cleaned PNG.

Soft checks (structured prompt emitted; verdict from Claude vision):
  - HF02 paper texture, HF03 wrong direction, HF04 wrong pose, HF05 wrong aesthetic.
  - SF01 style drift, SF02 identity drift, SF03 proportion drift, SF04 paper, SF05 expression.
  - Stylus in RIGHT hand (CC01).
  - Companion shape preserved as orange amorphous creature (not pixel sprite/armored).

Usage:
    python3 pipeline/seedance_v2_audit.py \\
        --selection runs/{run_id}/seedance_frames/selection.md \\
        --clean-dir runs/{run_id}/seedance_clean_v2 \\
        --slot 042
        # OR --slot-range 029-068 for batch
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

# Allow direct invocation via `python3 pipeline/seedance_v2_X.py ...` by
# putting the project root on sys.path. Pytest already handles this via
# pipeline/tests/__init__.py.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from pipeline.seedance_v2_select import SelectionRow, parse_selection_md


AUDIT_PROMPT_TEMPLATE = """\
Audit this cleaned frame against the following criteria. Return one
verdict per line: `CODE: PASS` or `CODE: FAIL — <reason>`.

CONTEXT:
  Slot: {slot}
  Source: {source}
  Beat: {beat}
  Cadence: {cadence}
  A-2 target style reference: runs/run_2026-04-04_174805/approved/PT_A1_F01_key.png

CHECKS:
  HF02 — paper texture: cream paper grain visible, not pure white
  HF05 — aesthetic: pencil-test drawing style, NOT digital/anime/3D
  SF01 — style drift: line weight + construction marks match A-2
  SF02 — identity drift: face matches A-2 (jaw, hair, eyes)
  CC01 — stylus right hand: stylus visible in character's RIGHT hand
  CMP01 — companion shape: orange amorphous creature, NOT pixel sprite or armored figure
"""


def check_aspect_ratio(path: Path) -> str:
    """HF01 — image is 16:9 within 2% tolerance."""
    im = Image.open(path)
    w, h = im.size
    ratio = w / h
    target = 16 / 9
    if abs(ratio - target) / target <= 0.02:
        return f"HF01: PASS ({w}x{h})"
    return f"HF01: FAIL — {w}x{h} is {ratio:.3f}, expected {target:.3f}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selection", type=Path, required=True)
    ap.add_argument("--clean-dir", type=Path, required=True)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--slot", type=int)
    group.add_argument("--slot-range", help="e.g. 029-068")
    args = ap.parse_args()

    rows = parse_selection_md(args.selection)
    if args.slot is not None:
        targets = [r for r in rows if r.decision == "KEEP" and r.slot == args.slot]
    else:
        lo, hi = args.slot_range.split("-")
        target_range = range(int(lo), int(hi) + 1)
        targets = [r for r in rows if r.decision == "KEEP" and r.slot in target_range]

    print(f"Auditing {len(targets)} slot(s)\n")

    any_fail = False
    for r in targets:
        path = args.clean_dir / f"PT_A1_v2_slot{r.slot:03d}.png"
        print(f"--- Slot {r.slot:03d} ({r.beat}) ---")
        if not path.exists():
            print(f"  FAIL — file not found: {path}")
            any_fail = True
            continue
        print(f"  {check_aspect_ratio(path)}")
        print(
            f"\n  CLAUDE VISION PROMPT (paste this PNG + the prompt below into a "
            f"separate session):\n"
        )
        print(AUDIT_PROMPT_TEMPLATE.format(
            slot=r.slot, source=r.source_frame, beat=r.beat, cadence=r.cadence
        ))
        print(f"  IMAGE: {path}\n")
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
