#!/usr/bin/env python3
"""Parse + validate selection.md files for the Seedance v2 integration.

selection.md is the declarative source of truth for which extracted
Seedance frames get cleaned, dropped, or hold-collapsed, plus their
cadence and per-frame A-N anchor references.

Usage as a CLI linter:
    python3 pipeline/seedance_v2_select.py runs/{run_id}/seedance_frames/selection.md

Usage as a library:
    from pipeline.seedance_v2_select import parse_selection_md, validate_selection
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

DECISIONS = {"KEEP", "DROP", "HOLD-COLLAPSE"}
CADENCES = {"12fps", "24fps", "—"}


@dataclass
class SelectionRow:
    slot: int | None
    source_frame: str
    cadence: str
    decision: str
    anchors: list[str] = field(default_factory=list)
    rationale: str = ""
    beat: str = ""


def parse_selection_md(path: Path) -> list[SelectionRow]:
    """Parse selection.md and return the row list (KEEP + DROP + HOLD-COLLAPSE)."""
    text = path.read_text()
    rows: list[SelectionRow] = []
    current_beat = ""
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("## "):
            current_beat = line.lstrip("# ").strip()
            continue
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 6:
            continue
        # Skip header + separator rows
        if cells[0].lower() == "slot" or set(cells[0]) <= set("-: "):
            continue
        slot_raw, source, cadence, decision, anchors_raw, rationale = cells[:6]
        if decision.upper() not in DECISIONS:
            continue
        slot = None if slot_raw == "—" else int(slot_raw)
        anchors = []
        if anchors_raw != "—":
            anchors = [a.strip() for a in anchors_raw.split(",") if a.strip()]
        rows.append(
            SelectionRow(
                slot=slot,
                source_frame=source,
                cadence=cadence,
                decision=decision.upper(),
                anchors=anchors,
                rationale=rationale,
                beat=current_beat,
            )
        )
    return rows


def validate_selection(rows: list[SelectionRow], anchor_root: Path) -> list[str]:
    """Return a list of validation error strings; empty list means valid."""
    errors: list[str] = []
    seen_slots: set[int] = set()
    for r in rows:
        # Decision-specific checks
        if r.decision == "KEEP":
            if r.slot is None:
                errors.append(f"KEEP row missing slot number: {r.source_frame}")
            elif r.slot in seen_slots:
                errors.append(f"duplicate slot: {r.slot}")
            else:
                seen_slots.add(r.slot)
            if r.cadence not in {"12fps", "24fps"}:
                errors.append(
                    f"KEEP slot {r.slot}: invalid cadence {r.cadence!r}"
                )
            if not r.anchors:
                errors.append(f"KEEP slot {r.slot}: no A-N anchors specified")
            for a in r.anchors:
                if not (anchor_root / a).exists():
                    errors.append(
                        f"KEEP slot {r.slot}: anchor file not found: {a}"
                    )
        elif r.decision == "HOLD-COLLAPSE":
            if r.slot is not None:
                errors.append(
                    f"HOLD-COLLAPSE row has slot {r.slot}; must be —"
                )
    # Slot numbering should be contiguous starting at 1
    if seen_slots:
        expected = set(range(min(seen_slots), max(seen_slots) + 1))
        missing = expected - seen_slots
        if missing:
            errors.append(f"non-contiguous slots; missing: {sorted(missing)}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("selection_md", type=Path)
    ap.add_argument(
        "--anchor-root",
        type=Path,
        default=Path.cwd(),
        help="Root for resolving anchor paths (default: cwd)",
    )
    args = ap.parse_args()

    rows = parse_selection_md(args.selection_md)
    errors = validate_selection(rows, args.anchor_root)
    if errors:
        for e in errors:
            print(f"  ERROR: {e}", file=sys.stderr)
        print(f"\n{len(errors)} validation error(s) in {args.selection_md}", file=sys.stderr)
        return 1
    keep = sum(1 for r in rows if r.decision == "KEEP")
    drop = sum(1 for r in rows if r.decision == "DROP")
    hold = sum(1 for r in rows if r.decision == "HOLD-COLLAPSE")
    print(f"OK — {args.selection_md}: {keep} KEEP, {drop} DROP, {hold} HOLD-COLLAPSE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
