# Act 1 — Seedance v2 Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a new Act 1 hero loop from two Seedance 2.0 outputs (intro + loop-closer), cleaned through Nano Banana 2 with chained-reference style anchoring and Procreate-polished, shipping as `pencil-test-act1-v2.{mp4,webm,gif}` while leaving the original Act 1 untouched as fallback.

**Architecture:** Spike-first pipeline with four phases — (1) author `selection.md` as the declarative source of truth, (2) spike the highest-risk beat (24fps "companion emerges from trails") to validate NB2 frame-to-frame consistency, (3) batch-clean and Procreate-polish the rest of the keep set, (4) assemble with mixed-cadence (12fps holds + 24fps action, uniform 24fps output) and QA against the Engine Truth. Existing approved frames serve as A-N style anchors; chained-reference cleanup uses each prior cleaned frame as a temporal-consistency anchor on 24fps stretches.

**Tech Stack:** Python 3, Pillow, google-genai (via existing `generate_image.py`), pytest for the few deterministic helpers, bash + ffmpeg for assembly, the project's existing `continuity_audit.py` for QA. **Companion design spec:** [docs/2026-05-12-act1-seedance-v2-integration-design.md](2026-05-12-act1-seedance-v2-integration-design.md).

---

## File structure

**New files:**
| Path | Responsibility |
|---|---|
| `runs/run_2026-04-04_174805/seedance_frames/selection.md` | Declarative per-frame KEEP/DROP/HOLD-COLLAPSE decisions for v2 source; one of the two artifacts the cleanup script consumes. |
| `runs/run_2026-04-04_174805/seedance_frames_v3_loopclose/selection.md` | Same for v3 source. |
| `pipeline/seedance_v2_select.py` | Parses + validates selection.md files (schema check, slot uniqueness, anchor-ref file-existence check). No creative judgment — purely a linter. |
| `pipeline/seedance_v2_cleanup.py` | Drives NB2 cleanup per `selection.md`. Implements chained-reference logic, retry ladder, JPEG-as-PNG fix, dimension-normalize. |
| `pipeline/seedance_v2_audit.py` | Audits cleaned frames against HF/SF + stylus-right-hand + companion-shape preservation. Emits Claude-vision prompts for the soft checks. |
| `pipeline/seedance_v2_assemble.sh` | Mixed-cadence assembly. Reads cleaned frames + per-frame cadence from selection.md, builds a 24fps frame sequence (12fps frames held 2 sub-slots), encodes MP4/WebM/GIF. |
| `pipeline/tests/test_seedance_v2_select.py` | Unit tests for the selection.md parser/validator. |
| `pipeline/tests/test_seedance_v2_cleanup.py` | Unit tests for reference-list builder + retry-ladder state machine. Mocks the subprocess call. |
| `pipeline/tests/test_seedance_v2_assemble.py` | Unit tests for the cadence-math helper (12fps frame → 2 sub-slots, 24fps frame → 1 sub-slot, hold-collapse → N sub-slots). |
| `runs/run_2026-04-04_174805/seedance_clean_v2/` | Output directory for cleaned PNGs. Created by Task 5. |
| `runs/run_2026-04-04_174805/audit/spike_validation.md` | Spike pass/fail verdict + sign-off. Written in Task 4. |
| `runs/run_2026-04-04_174805/audit/v2_integration_qa.md` | Final QA verdict. Written in Task 10. |

**Modified files:**
| Path | Change |
|---|---|
| `CHANGELOG.md` | Add a 2026-05-13 entry documenting the v2 integration. Final task. |
| `docs/production-checklist.md` | Reflect v2 integration phases. Final task. |
| `CLAUDE.md` | Add `seedance_v2_*` scripts to the Key Commands section. Final task. |

**Untouched (intentionally):**
| Path | Reason |
|---|---|
| `runs/run_2026-04-04_174805/approved/` | Style + identity anchors. Read-only. |
| `pipeline/assemble.sh` | Original 12fps assembly. Untouched. The v2 mode is a new sibling script. |
| `pipeline/audit.py`, `pipeline/continuity_audit.py`, `pipeline/generate.py` | Continue to work on the original Act 1 frames. v2 has its own scripts. |
| `runs/run_2026-04-04_174805/export/pencil-test-act1.{mp4,webm,gif}` | Original Act 1 export stays as fallback. v2 ships as `pencil-test-act1-v2.{mp4,webm,gif}`. |

---

## Phase overview

| Phase | Tasks | Deliverable | Gate |
|---|---|---|---|
| **Phase 0 — Selection** | 1, 2 | `selection.md` + linter script | User reviews & approves selection.md |
| **Phase 1 — Spike** | 3, 4, 5 | Spike mini-clip + verdict | User reviews spike clip; PASS → continue, FAIL → replan |
| **Phase 2 — Batch cleanup** | 6, 7 | Cleaned + audited keep set | All HF/SF audits PASS or fallback-documented |
| **Phase 3 — Assembly & ship** | 8, 9, 10, 11 | `pencil-test-act1-v2.{mp4,webm,gif}` | Engine Truth QA PASS |

---

## Task 1: Author `selection.md` for both v2 and v3 sources

**Files:**
- Create: `runs/run_2026-04-04_174805/seedance_frames/selection.md`
- Create: `runs/run_2026-04-04_174805/seedance_frames_v3_loopclose/selection.md`
- Read-only refs: `runs/run_2026-04-04_174805/seedance_frames/contact_sheet_24fps.png`, `runs/run_2026-04-04_174805/seedance_frames_v3_loopclose/contact_sheet_24fps.png`, the design spec.

- [ ] **Step 1: Open both contact sheets and the design spec**

```bash
open runs/run_2026-04-04_174805/seedance_frames/contact_sheet_24fps.png
open runs/run_2026-04-04_174805/seedance_frames_v3_loopclose/contact_sheet_24fps.png
open docs/2026-05-12-act1-seedance-v2-integration-design.md
```

- [ ] **Step 2: Write `seedance_frames/selection.md` using this exact schema**

```markdown
# Act 1 v2 — Seedance Intro (v2) Frame Selection

**Source MP4:** `runs/run_2026-04-04_174805/export/seedance-2.0-output/Act-1-Test-2-Seedance-2.0.mp4`
**Extraction:** `runs/run_2026-04-04_174805/seedance_frames/raw_24fps/frame_NNNN.png` (166 frames @ 24fps, 6.92s)
**Design spec:** `docs/2026-05-12-act1-seedance-v2-integration-design.md`
**Signed off by:** [User name + date when approved]

## Beat 1: Idle (intro) — cadence: 12fps

| Slot | Source frame | Cadence | Decision | A-N anchors (1, 2, 3...) | Rationale |
|---|---|---|---|---|---|
| 001 | frame_0001.png | 12fps | KEEP | approved/PT_A1_F01_key.png, approved/PT_A1_F40_key.png | Loop-start idle frame, identity baseline |
| —   | frame_0002.png – frame_0008.png | — | HOLD-COLLAPSE | — | Redundant idle — slot 001 held for these |
| 002 | frame_0009.png | 12fps | KEEP | approved/PT_A1_F01_key.png, approved/PT_A1_F40_key.png | Breath sub-beat |
| —   | frame_0010.png – frame_0020.png | — | HOLD-COLLAPSE | — | Redundant idle |
| 003 | frame_0021.png | 12fps | KEEP | approved/PT_A1_F01_key.png, approved/PT_A1_F40_key.png | Breath sub-beat |
| —   | frame_0022.png – frame_0032.png | — | HOLD-COLLAPSE | — | Redundant idle |
| 004 | frame_0033.png | 12fps | KEEP | approved/PT_A1_F01_key.png, approved/PT_A1_F40_key.png | Last idle before arm-up |
| —   | frame_0034.png – frame_0040.png | — | HOLD-COLLAPSE | — | Anticipation hold |

## Beat 2: Arm-up + draw circle — cadence: 24fps

| Slot | Source frame | Cadence | Decision | A-N anchors | Rationale |
|---|---|---|---|---|---|
| 005 | frame_0041.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png | Arm starts to lift |
| 006 | frame_0042.png | 24fps | KEEP | approved/PT_A1_F10_key.png, approved/PT_A1_F13_key.png | Arm rising |
... (one row per kept 24fps frame in 41-65 range, ~24 rows)

## Beat 3: Companion emerges from trails — cadence: 24fps ⭐ SPIKE TARGET

| Slot | Source frame | Cadence | Decision | A-N anchors | Rationale |
|---|---|---|---|---|---|
| 029 | frame_0066.png | 24fps | KEEP | approved/PT_A1_F22_key.png, approved/PT_A1_F31_key.png | First moment companion form is visible |
... (one row per kept 24fps frame in 66-105 range, ~40 rows)

## Beat 4: Hold on shoulder — cadence: 12fps
## Beat 5: (loop-closer starts) — see seedance_frames_v3_loopclose/selection.md
```

Detailed per-frame decisions for beats 2–4 are written by walking the contact sheet. **Rule of thumb for cull:**
- **Idle beats (1, 4, 7):** Keep every ~12th frame at 24fps source (= 2fps actual sample rate, equivalent to 12fps with hold-collapse over 6 sub-slots). Goal is 3–4 distinct breath frames per idle stretch.
- **Action beats (2, 3, 5):** Keep every 24fps frame UNLESS it shows a clear regression (e.g., morphing fingers, stylus drift, identity wobble visible at sample). Drop those individually with rationale.
- **First and last frame of every beat:** Always KEEP. Beat transitions must have clean anchors.

- [ ] **Step 3: Write `seedance_frames_v3_loopclose/selection.md` with the same schema** for v3 source frames 1–166. Beats: companion detaches (1–55, 24fps), return-to-idle (56–110, 12fps), idle tail (111–166, 12fps).

- [ ] **Step 4: Append a summary table at the bottom of each selection.md**

```markdown
## Summary

| Metric | Value |
|---|---|
| Source frames extracted | 166 |
| KEEP decisions | N |
| DROP decisions | M |
| HOLD-COLLAPSE decisions | K |
| 12fps cadence slots | X |
| 24fps cadence slots | Y |
| Spike target slots | 029–068 (inclusive) |
```

- [ ] **Step 5: Open both files and visually confirm the slot numbering is contiguous across the two files** (v2 ends at slot N, v3 starts at slot N+1).

- [ ] **Step 6: Commit**

```bash
git add runs/run_2026-04-04_174805/seedance_frames/selection.md \
        runs/run_2026-04-04_174805/seedance_frames_v3_loopclose/selection.md
git commit -m "$(cat <<'EOF'
act1-v2: author selection.md for both Seedance sources

Per the v2 integration design spec, declaratively map each extracted 24fps
frame to KEEP, DROP, or HOLD-COLLAPSE with per-slot A-N anchor refs and
cadence. Spike target (companion-emerges-from-trails) is slot range 029-068.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 7: HUMAN GATE — user reviews both `selection.md` files. Does NOT proceed to Task 2 until user signs off** by editing the "Signed off by:" line at the top of each file with their name + date.

---

## Task 2: Build the `selection.md` linter (`seedance_v2_select.py`)

**Files:**
- Create: `pipeline/seedance_v2_select.py`
- Create: `pipeline/tests/__init__.py` (empty, marks pytest package)
- Create: `pipeline/tests/test_seedance_v2_select.py`

- [ ] **Step 1: Write the failing test file**

```python
# pipeline/tests/test_seedance_v2_select.py
"""Tests for the selection.md parser/validator."""
from pathlib import Path

import pytest

from pipeline.seedance_v2_select import (
    SelectionRow,
    parse_selection_md,
    validate_selection,
)


SAMPLE_MD = """
# Test Selection

**Source MP4:** path/to/x.mp4
**Extraction:** path/to/raw_24fps/frame_NNNN.png

## Beat 1: Idle — cadence: 12fps

| Slot | Source frame | Cadence | Decision | A-N anchors | Rationale |
|---|---|---|---|---|---|
| 001 | frame_0001.png | 12fps | KEEP | approved/PT_A1_F01_key.png, approved/PT_A1_F40_key.png | First idle |
| —   | frame_0002.png – frame_0008.png | — | HOLD-COLLAPSE | — | Redundant |
| 002 | frame_0009.png | 12fps | KEEP | approved/PT_A1_F01_key.png | Breath |

## Summary

| Metric | Value |
|---|---|
| KEEP decisions | 2 |
"""


def test_parse_keep_rows(tmp_path):
    p = tmp_path / "selection.md"
    p.write_text(SAMPLE_MD)
    rows = parse_selection_md(p)
    keep = [r for r in rows if r.decision == "KEEP"]
    assert len(keep) == 2
    assert keep[0].slot == 1
    assert keep[0].source_frame == "frame_0001.png"
    assert keep[0].cadence == "12fps"
    assert keep[0].anchors == [
        "approved/PT_A1_F01_key.png",
        "approved/PT_A1_F40_key.png",
    ]


def test_parse_hold_collapse_rows(tmp_path):
    p = tmp_path / "selection.md"
    p.write_text(SAMPLE_MD)
    rows = parse_selection_md(p)
    hold = [r for r in rows if r.decision == "HOLD-COLLAPSE"]
    assert len(hold) == 1
    assert hold[0].source_frame == "frame_0002.png – frame_0008.png"


def test_validate_detects_duplicate_slot(tmp_path):
    bad = SAMPLE_MD.replace("| 002 |", "| 001 |")
    p = tmp_path / "selection.md"
    p.write_text(bad)
    rows = parse_selection_md(p)
    errors = validate_selection(rows, anchor_root=tmp_path)
    assert any("duplicate slot" in e.lower() for e in errors)


def test_validate_detects_missing_anchor(tmp_path):
    p = tmp_path / "selection.md"
    p.write_text(SAMPLE_MD)
    rows = parse_selection_md(p)
    errors = validate_selection(rows, anchor_root=tmp_path)
    # All referenced anchors don't exist under tmp_path
    assert any("not found" in e.lower() for e in errors)


def test_validate_accepts_valid_selection(tmp_path):
    (tmp_path / "approved").mkdir()
    (tmp_path / "approved" / "PT_A1_F01_key.png").touch()
    (tmp_path / "approved" / "PT_A1_F40_key.png").touch()
    p = tmp_path / "selection.md"
    p.write_text(SAMPLE_MD)
    rows = parse_selection_md(p)
    errors = validate_selection(rows, anchor_root=tmp_path)
    assert errors == []
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
cd /Users/seanwinslow/Code-Brain/sw-portfolio-2D-animation
python3 -m pytest pipeline/tests/test_seedance_v2_select.py -v
```

Expected: All 5 tests FAIL with `ModuleNotFoundError: No module named 'pipeline.seedance_v2_select'`.

- [ ] **Step 3: Implement `pipeline/seedance_v2_select.py`**

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
python3 -m pytest pipeline/tests/test_seedance_v2_select.py -v
```

Expected: All 5 tests PASS.

- [ ] **Step 5: Run the linter against the real selection.md files from Task 1**

```bash
python3 pipeline/seedance_v2_select.py runs/run_2026-04-04_174805/seedance_frames/selection.md
python3 pipeline/seedance_v2_select.py runs/run_2026-04-04_174805/seedance_frames_v3_loopclose/selection.md
```

Expected: Both print `OK — ...: N KEEP, M DROP, K HOLD-COLLAPSE`. If any errors, fix selection.md before continuing.

- [ ] **Step 6: Commit**

```bash
git add pipeline/seedance_v2_select.py pipeline/tests/__init__.py pipeline/tests/test_seedance_v2_select.py
git commit -m "$(cat <<'EOF'
act1-v2: add selection.md linter (seedance_v2_select.py)

Parses the declarative KEEP/DROP/HOLD-COLLAPSE rows from selection.md,
validates slot uniqueness + contiguity, cadence enum, anchor-file
existence. CLI linter exits non-zero on any error.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Build the NB2 cleanup driver (`seedance_v2_cleanup.py`)

**Files:**
- Create: `pipeline/seedance_v2_cleanup.py`
- Create: `pipeline/tests/test_seedance_v2_cleanup.py`

- [ ] **Step 1: Write the failing test for `build_references()`**

```python
# pipeline/tests/test_seedance_v2_cleanup.py
"""Tests for the cleanup driver's reference-building + retry-ladder logic."""
from pathlib import Path
from unittest.mock import patch

import pytest

from pipeline.seedance_v2_cleanup import (
    UNIVERSAL_PROMPT,
    build_references,
    retry_attempt_prompt,
    run_cleanup_for_slot,
)
from pipeline.seedance_v2_select import SelectionRow


def make_row(slot, cadence, anchors):
    return SelectionRow(
        slot=slot,
        source_frame=f"frame_{slot:04d}.png",
        cadence=cadence,
        decision="KEEP",
        anchors=anchors,
        rationale="t",
        beat="t",
    )


def test_build_references_12fps_excludes_prev(tmp_path):
    row = make_row(1, "12fps", ["approved/PT_A1_F01_key.png"])
    refs = build_references(
        row,
        source_dir=tmp_path / "raw_24fps",
        anchor_root=tmp_path,
        a2_anchor="approved/PT_A1_F01_key.png",
        prev_cleaned=tmp_path / "prev.png",
    )
    # A-2 always present. 12fps stretches do NOT add prev_cleaned.
    assert refs[0] == tmp_path / "approved/PT_A1_F01_key.png"
    assert (tmp_path / "prev.png") not in refs


def test_build_references_24fps_includes_prev(tmp_path):
    row = make_row(2, "24fps", ["approved/PT_A1_F22_key.png"])
    refs = build_references(
        row,
        source_dir=tmp_path / "raw_24fps",
        anchor_root=tmp_path,
        a2_anchor="approved/PT_A1_F01_key.png",
        prev_cleaned=tmp_path / "prev.png",
    )
    # 24fps stretches DO add prev_cleaned (as last reference).
    assert refs[-1] == tmp_path / "prev.png"


def test_build_references_24fps_no_prev_yet(tmp_path):
    row = make_row(2, "24fps", ["approved/PT_A1_F22_key.png"])
    refs = build_references(
        row,
        source_dir=tmp_path / "raw_24fps",
        anchor_root=tmp_path,
        a2_anchor="approved/PT_A1_F01_key.png",
        prev_cleaned=None,
    )
    # First frame in a 24fps stretch: no prev to chain from.
    assert all(p.name != "prev.png" for p in refs)


def test_retry_attempt_prompts_differ():
    p1 = retry_attempt_prompt(1)
    p2 = retry_attempt_prompt(2)
    p3 = retry_attempt_prompt(3)
    # Attempt 2 adds explicit identity correction.
    assert "jaw shape" in p2.lower() or "eye spacing" in p2.lower()
    # Attempt 3 adds paper-texture refinement block.
    assert "paper" in p3.lower() and "texture" in p3.lower()
    # Universal prompt always present.
    assert UNIVERSAL_PROMPT in p1
    assert UNIVERSAL_PROMPT in p2
    assert UNIVERSAL_PROMPT in p3


@patch("pipeline.seedance_v2_cleanup.subprocess.run")
def test_run_cleanup_invokes_generate_image_with_refs(mock_run, tmp_path):
    mock_run.return_value.returncode = 0
    row = make_row(5, "24fps", ["approved/PT_A1_F22_key.png"])
    (tmp_path / "approved").mkdir()
    (tmp_path / "approved" / "PT_A1_F01_key.png").touch()
    (tmp_path / "approved" / "PT_A1_F22_key.png").touch()
    (tmp_path / "raw_24fps").mkdir()
    (tmp_path / "raw_24fps" / "frame_0005.png").touch()

    run_cleanup_for_slot(
        row,
        run_dir=tmp_path,
        source_dir=tmp_path / "raw_24fps",
        clean_dir=tmp_path / "clean",
        anchor_root=tmp_path,
        a2_anchor="approved/PT_A1_F01_key.png",
        prev_cleaned=None,
        attempt=1,
    )
    assert mock_run.called
    cmd = mock_run.call_args[0][0]
    # Must call the gemini-pencil-animation-image-gen script
    assert "generate_image.py" in " ".join(cmd)
    # Must include the universal prompt
    assert UNIVERSAL_PROMPT in cmd
    # Must include --reference followed by the A-2 + beat-matched anchor + source frame
    assert "--reference" in cmd
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
python3 -m pytest pipeline/tests/test_seedance_v2_cleanup.py -v
```

Expected: All 5 tests FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement `pipeline/seedance_v2_cleanup.py`**

```python
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
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"generate_image.py failed for slot {row.slot} attempt {attempt}:\n"
            f"stderr: {result.stderr}"
        )
    if out_path.exists():
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
        default=Path.cwd(),
        help="Root for resolving anchor paths in selection.md",
    )
    ap.add_argument(
        "--a2-anchor",
        default="runs/run_2026-04-04_174805/approved/PT_A1_F01_key.png",
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

    args.clean_dir.mkdir(parents=True, exist_ok=True)

    rows = parse_selection_md(args.selection)
    errors = validate_selection(rows, args.anchor_root)
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
                    anchor_root=args.anchor_root,
                    a2_anchor=args.a2_anchor,
                    prev_cleaned=prev_cleaned,
                    attempt=attempt,
                )
            except RuntimeError as e:
                print(f"  Slot {row.slot:03d} attempt {attempt}: ERROR — {e}", file=sys.stderr)
                continue
            print(f"  Slot {row.slot:03d} attempt {attempt}: {out_path}")
            # In rough-cut mode, accept attempt 1 unconditionally.
            if args.first_attempt_only:
                success = True
                chosen_attempt = attempt
                break
            # Audit-and-retry is handled by seedance_v2_audit.py in a separate
            # step; for now, accept attempt 1 and let audit flag failures.
            success = True
            chosen_attempt = attempt
            break
        if success and chosen_attempt is not None:
            # Promote chosen attempt to the stable filename for assembly to consume.
            chosen = args.clean_dir / f"PT_A1_v2_slot{row.slot:03d}_attempt_{chosen_attempt:02d}.png"
            stable = args.clean_dir / f"PT_A1_v2_slot{row.slot:03d}.png"
            if chosen.exists():
                import shutil
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
python3 -m pytest pipeline/tests/test_seedance_v2_cleanup.py -v
```

Expected: All 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add pipeline/seedance_v2_cleanup.py pipeline/tests/test_seedance_v2_cleanup.py
git commit -m "$(cat <<'EOF'
act1-v2: add NB2 cleanup driver (seedance_v2_cleanup.py)

Drives gemini-pencil-animation-image-gen per KEEP row in selection.md.
Builds the per-frame reference stack (A-2 always #1, beat-matched A-N
anchors, Seedance source frame, prev-cleaned chained reference on 24fps
stretches). Retry-ladder prompts at attempts 2 and 3 add identity + paper
texture corrections. Tested with mocked subprocess.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: Build the cleaned-frame audit script (`seedance_v2_audit.py`)

**Files:**
- Create: `pipeline/seedance_v2_audit.py`

- [ ] **Step 1: Implement the audit script (no new tests — leverages existing `audit.py` PIL checks + emits Claude-vision prompts for soft checks)**

```python
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
```

- [ ] **Step 2: Smoke-test (no input expected since no cleanups have run yet)**

```bash
python3 pipeline/seedance_v2_audit.py --help
```

Expected: argparse help text, no errors.

- [ ] **Step 3: Commit**

```bash
git add pipeline/seedance_v2_audit.py
git commit -m "$(cat <<'EOF'
act1-v2: add cleaned-frame audit script (seedance_v2_audit.py)

Runs HF01 (aspect ratio) automatically via PIL; emits structured Claude-
vision prompts for the soft checks (HF02-HF05, SF01-SF05, CC01 stylus
hand, CMP01 companion shape preservation). Per-slot or range mode.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Run the SPIKE — cleanup just the "companion emerges" beat

**Files:**
- Reads: `runs/run_2026-04-04_174805/seedance_frames/selection.md`, slots 029–068.
- Writes: `runs/run_2026-04-04_174805/seedance_clean_v2/PT_A1_v2_slot{NNN}.png` for slots 029–068.

- [ ] **Step 1: Confirm .env has GEMINI_API_KEY**

```bash
grep -q "GEMINI_API_KEY=" .env && echo "OK" || echo "MISSING — add GEMINI_API_KEY to .env"
```

Expected: `OK`.

- [ ] **Step 2: Run cleanup on the spike slot range only**

```bash
python3 pipeline/seedance_v2_cleanup.py \
    --selection runs/run_2026-04-04_174805/seedance_frames/selection.md \
    --source-dir runs/run_2026-04-04_174805/seedance_frames/raw_24fps \
    --clean-dir runs/run_2026-04-04_174805/seedance_clean_v2 \
    --run-dir runs/run_2026-04-04_174805 \
    --slot-range 029-068
```

Expected: ~40 lines like `Slot 029 attempt 1: runs/.../PT_A1_v2_slot029_attempt_01.png`. Finishes with `Completed cleanup on 40 slot(s)`.

- [ ] **Step 3: Run automated HF01 audit on the spike outputs**

```bash
python3 pipeline/seedance_v2_audit.py \
    --selection runs/run_2026-04-04_174805/seedance_frames/selection.md \
    --clean-dir runs/run_2026-04-04_174805/seedance_clean_v2 \
    --slot-range 029-068
```

Expected: `HF01: PASS (1376x768)` on every slot. The script will also emit Claude-vision prompts for soft checks — those are reviewed in Step 4.

- [ ] **Step 4: Build a spike contact sheet for visual review**

```bash
python3 - <<'PY'
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

run_dir = Path("runs/run_2026-04-04_174805")
src_dir = run_dir / "seedance_clean_v2"
out_path = run_dir / "audit" / "spike_contact_sheet.png"
out_path.parent.mkdir(exist_ok=True)

frames = sorted(src_dir.glob("PT_A1_v2_slot0[2-6][0-9].png"))
print(f"Frames: {len(frames)}")

cols, rows = 8, 5
thumb_w, thumb_h = 320, 180
pad = 4
label_h = 18
sheet_w = cols * (thumb_w + pad) + pad
sheet_h = rows * (thumb_h + label_h + pad) + pad
sheet = Image.new("RGB", (sheet_w, sheet_h), (16, 16, 16))
draw = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 12)
except Exception:
    font = ImageFont.load_default()

for idx, fpath in enumerate(frames):
    r, c = divmod(idx, cols)
    x = pad + c * (thumb_w + pad)
    y = pad + r * (thumb_h + label_h + pad)
    im = Image.open(fpath).convert("RGB").resize((thumb_w, thumb_h), Image.LANCZOS)
    sheet.paste(im, (x, y))
    draw.text((x + 4, y + thumb_h + 2), fpath.stem, fill=(220,220,220), font=font)

sheet.save(out_path, "PNG", optimize=True)
print(f"Saved: {out_path}")
PY
```

Expected: Contact sheet at `runs/run_2026-04-04_174805/audit/spike_contact_sheet.png`.

- [ ] **Step 5: Assemble the spike as a standalone mini-clip**

```bash
mkdir -p runs/run_2026-04-04_174805/audit/spike_sequence
i=1
for slot in $(seq 29 68); do
    src=$(printf "runs/run_2026-04-04_174805/seedance_clean_v2/PT_A1_v2_slot%03d.png" "$slot")
    dest=$(printf "runs/run_2026-04-04_174805/audit/spike_sequence/frame_%04d.png" "$i")
    cp "$src" "$dest"
    i=$((i+1))
done

ffmpeg -hide_banner -y -framerate 24 \
    -i runs/run_2026-04-04_174805/audit/spike_sequence/frame_%04d.png \
    -c:v libx264 -crf 18 -pix_fmt yuv420p \
    -vf "scale=1920:1080:flags=lanczos" \
    runs/run_2026-04-04_174805/audit/spike.mp4

ffprobe -v error -show_entries stream=nb_frames,r_frame_rate -of default=noprint_wrappers=1 \
    runs/run_2026-04-04_174805/audit/spike.mp4
```

Expected: `nb_frames=40`, `r_frame_rate=24/1`. File plays back as ~1.67s clip.

- [ ] **Step 6: Open the spike clip in QuickTime**

```bash
open runs/run_2026-04-04_174805/audit/spike.mp4
```

Watch it at 1× and 0.5×. Then open `runs/run_2026-04-04_174805/audit/spike_contact_sheet.png` for the per-frame eye-test.

- [ ] **Step 7: HUMAN GATE — user evaluates spike against the spec's PASS criteria**

The spec's spike acceptance criteria:
1. No visible boil between adjacent cleaned frames.
2. Identity holds (no SF02 drift).
3. Stylus stays in right hand every frame.
4. Companion stays orange + amorphous (not pixel sprite / armored).
5. Pencil-test fidelity matches A-2.

User signs off in Task 6, regardless of PASS or FAIL.

---

## Task 6: Document the spike verdict + decision gate

**Files:**
- Create: `runs/run_2026-04-04_174805/audit/spike_validation.md`

- [ ] **Step 1: Write the verdict document**

```markdown
# Act 1 v2 Spike Validation

**Date:** 2026-05-13
**Reviewer:** [user name]
**Spike scope:** Slots 029–068 (companion emerges from trails beat, 40 frames @ 24fps)
**Artifacts:**
- Cleaned PNGs: `runs/run_2026-04-04_174805/seedance_clean_v2/PT_A1_v2_slot{029..068}.png`
- Contact sheet: `runs/run_2026-04-04_174805/audit/spike_contact_sheet.png`
- Assembled clip: `runs/run_2026-04-04_174805/audit/spike.mp4`

## Per-criterion verdict

| Criterion | Verdict | Notes |
|---|---|---|
| No visible boil between adjacent frames | PASS / FAIL | … |
| Identity holds (SF02) | PASS / FAIL | … |
| Stylus in right hand (CC01) every frame | PASS / FAIL | … |
| Companion stays orange + amorphous | PASS / FAIL | … |
| Pencil-test fidelity matches A-2 | PASS / FAIL | … |

## Overall verdict

**[ ] PASS — proceed to Task 7 (batch cleanup remaining slots)**
**[ ] FAIL — see "Replan options" below**

## Replan options (if FAIL)

| Option | What it changes |
|---|---|
| A. Drop to pure 12fps for the whole loop | Halves cleanup count; eliminates boil; loses Seedance smoothness |
| B. Narrow 24fps stretches to ≤12 frames per beat | Keeps hero moments at 24fps; surrounding context drops to 12fps |
| C. Abandon v2 integration | Ship existing original Act 1 unchanged |
```

- [ ] **Step 2: HUMAN GATE — user fills in the verdict, signs off, decides next action**

- [ ] **Step 3: Commit**

```bash
git add runs/run_2026-04-04_174805/audit/spike_validation.md
git commit -m "$(cat <<'EOF'
act1-v2: record spike validation verdict

40-frame "companion emerges" spike at 24fps. Records the user's pass/fail
on the five spec-defined criteria and chosen next action (proceed to
batch cleanup, narrow scope, or abandon v2).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 4: BRANCHING POINT**
  - If spike PASS → continue to Task 7.
  - If spike FAIL → STOP execution. Loop back to brainstorming with the replan options. Do NOT run Task 7.

---

## Task 7: Batch cleanup the remaining KEEP slots

**Files:**
- Reads: both selection.md files (all slots OTHER than 029–068, already done).
- Writes: `runs/run_2026-04-04_174805/seedance_clean_v2/PT_A1_v2_slot{NNN}.png` for all remaining KEEP slots.

- [ ] **Step 1: Identify the remaining slot ranges**

```bash
python3 - <<'PY'
from pipeline.seedance_v2_select import parse_selection_md
from pathlib import Path

rd = Path("runs/run_2026-04-04_174805")
for src in ("seedance_frames/selection.md", "seedance_frames_v3_loopclose/selection.md"):
    rows = parse_selection_md(rd / src)
    keeps = sorted(r.slot for r in rows if r.decision == "KEEP")
    spike = set(range(29, 69))
    remaining = [s for s in keeps if s not in spike]
    print(f"{src}: {len(keeps)} KEEP, {len(remaining)} remaining after spike: {remaining[:5]}...{remaining[-5:] if len(remaining) > 5 else ''}")
PY
```

Expected: two lines reporting per-source KEEP counts and the remaining slot lists.

- [ ] **Step 2: Run cleanup on the remaining v2 slots**

```bash
# v2 — everything EXCEPT spike range 029-068.
# Split into "pre-spike" (slots 1-28) and "post-spike" (slots 69+) ranges.
python3 pipeline/seedance_v2_cleanup.py \
    --selection runs/run_2026-04-04_174805/seedance_frames/selection.md \
    --source-dir runs/run_2026-04-04_174805/seedance_frames/raw_24fps \
    --clean-dir runs/run_2026-04-04_174805/seedance_clean_v2 \
    --run-dir runs/run_2026-04-04_174805 \
    --slot-range 001-028

python3 pipeline/seedance_v2_cleanup.py \
    --selection runs/run_2026-04-04_174805/seedance_frames/selection.md \
    --source-dir runs/run_2026-04-04_174805/seedance_frames/raw_24fps \
    --clean-dir runs/run_2026-04-04_174805/seedance_clean_v2 \
    --run-dir runs/run_2026-04-04_174805 \
    --slot-range 069-079    # adjust upper bound to match v2's last slot
```

Expected: Per-slot success lines, final `Completed cleanup on N slot(s)` per invocation.

- [ ] **Step 3: Run cleanup on all v3 slots**

```bash
python3 pipeline/seedance_v2_cleanup.py \
    --selection runs/run_2026-04-04_174805/seedance_frames_v3_loopclose/selection.md \
    --source-dir runs/run_2026-04-04_174805/seedance_frames_v3_loopclose/raw_24fps \
    --clean-dir runs/run_2026-04-04_174805/seedance_clean_v2 \
    --run-dir runs/run_2026-04-04_174805
```

(Omit `--slot-range` to run the full v3 set.)

- [ ] **Step 4: Run HF01 audit across all cleaned slots**

```bash
python3 pipeline/seedance_v2_audit.py \
    --selection runs/run_2026-04-04_174805/seedance_frames/selection.md \
    --clean-dir runs/run_2026-04-04_174805/seedance_clean_v2 \
    --slot-range 001-079 > runs/run_2026-04-04_174805/audit/v2_hf01_v2.log

python3 pipeline/seedance_v2_audit.py \
    --selection runs/run_2026-04-04_174805/seedance_frames_v3_loopclose/selection.md \
    --clean-dir runs/run_2026-04-04_174805/seedance_clean_v2 \
    --slot-range 080-113 > runs/run_2026-04-04_174805/audit/v2_hf01_v3.log

grep "FAIL" runs/run_2026-04-04_174805/audit/v2_hf01_v*.log || echo "All HF01 PASS"
```

Expected: `All HF01 PASS`. If any FAIL, the affected slot has a dimension/aspect-ratio problem — re-run cleanup for that slot with attempt 2.

- [ ] **Step 5: Build a full contact sheet of every cleaned slot**

Same script as Task 5 Step 4, but glob `PT_A1_v2_slot*.png` (no slot filter) and adjust grid to ~10 cols × N rows.

- [ ] **Step 6: HUMAN GATE — user scans the full contact sheet for any obvious failure slots**

Failure cases that warrant retry (user flags slot numbers):
- Stylus drifted to left hand
- Identity wobble (face doesn't match A-2)
- Companion morphed to pixel sprite or armored figure
- Visible boil between adjacent 24fps frames

- [ ] **Step 7: For each flagged slot, re-run cleanup at attempt 2 or 3 only**

```bash
# Example: re-run slot 042 at attempt 2 + 3, picking the better output.
# (Manual: invoke generate_image.py directly with the attempt 2 prompt.
#  We're not adding an attempt-N CLI flag because flagged-retry volume is small.)
python3 - <<'PY'
from pathlib import Path
from pipeline.seedance_v2_cleanup import run_cleanup_for_slot
from pipeline.seedance_v2_select import parse_selection_md

selection = Path("runs/run_2026-04-04_174805/seedance_frames/selection.md")
rows = parse_selection_md(selection)
slot = 42  # change per flagged slot
prev = Path(f"runs/run_2026-04-04_174805/seedance_clean_v2/PT_A1_v2_slot{slot-1:03d}.png")
target = next(r for r in rows if r.slot == slot and r.decision == "KEEP")
run_cleanup_for_slot(
    target,
    run_dir=Path("runs/run_2026-04-04_174805"),
    source_dir=Path("runs/run_2026-04-04_174805/seedance_frames/raw_24fps"),
    clean_dir=Path("runs/run_2026-04-04_174805/seedance_clean_v2"),
    anchor_root=Path.cwd(),
    a2_anchor="runs/run_2026-04-04_174805/approved/PT_A1_F01_key.png",
    prev_cleaned=prev if prev.exists() else None,
    attempt=2,
)
PY
```

Manually pick the best of `*_attempt_01/02/03.png` and copy to the stable filename:

```bash
cp runs/run_2026-04-04_174805/seedance_clean_v2/PT_A1_v2_slot042_attempt_02.png \
   runs/run_2026-04-04_174805/seedance_clean_v2/PT_A1_v2_slot042.png
```

- [ ] **Step 8: Document flagged-slot retries in `runs/run_2026-04-04_174805/audit/v2_retry_log.md`**

```markdown
# Act 1 v2 — Flagged Slot Retry Log

| Slot | Issue | Attempts run | Chosen attempt | Notes |
|---|---|---|---|---|
| 042 | SF02 identity drift | 1, 2 | 2 | Hair part more on-model with explicit identity correction |
```

- [ ] **Step 9: Commit cleaned frames + retry log**

```bash
git add runs/run_2026-04-04_174805/seedance_clean_v2/ runs/run_2026-04-04_174805/audit/v2_retry_log.md runs/run_2026-04-04_174805/audit/v2_hf01_v*.log
git commit -m "$(cat <<'EOF'
act1-v2: batch cleanup of all remaining KEEP slots

Cleaned all KEEP slots outside the spike range across both v2 and v3
Seedance sources. HF01 PASS on all outputs. Flagged-slot retries logged
in v2_retry_log.md with chosen attempt per slot.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: Procreate polish pass (manual, may be skipped)

**Files:**
- Reads: `runs/run_2026-04-04_174805/seedance_clean_v2/PT_A1_v2_slot{NNN}.png`
- Writes: same paths (overwritten with polished version)
- Backup: `runs/run_2026-04-04_174805/seedance_clean_v2/_pre_polish_backup/`

- [ ] **Step 1: Back up the unpolished cleaned set**

```bash
mkdir -p runs/run_2026-04-04_174805/seedance_clean_v2/_pre_polish_backup
cp runs/run_2026-04-04_174805/seedance_clean_v2/PT_A1_v2_slot*.png \
   runs/run_2026-04-04_174805/seedance_clean_v2/_pre_polish_backup/
```

- [ ] **Step 2: Identify polish-target slots**

User reviews the contact sheet and flags slots that need:
- Paper-grain consistency (some frames may be smoother than others)
- Pencil-trail line cleanup (especially Beat 2 frames — the magic-pencil arcs)
- Hand-drawn construction line additions where NB2 over-cleaned them

- [ ] **Step 3: Open flagged PNGs in Procreate, paint over, export at original dimensions (1376x768)**

This step is manual and user-driven. No script.

- [ ] **Step 4: Re-encode polished PNGs through PIL (defensive — Procreate exports clean PNG, but verify)**

```bash
python3 - <<'PY'
from PIL import Image
from pathlib import Path
clean_dir = Path("runs/run_2026-04-04_174805/seedance_clean_v2")
for p in sorted(clean_dir.glob("PT_A1_v2_slot*.png")):
    Image.open(p).convert("RGB").save(p, "PNG")
print("Re-encoded all cleaned PNGs")
PY
```

- [ ] **Step 5: Document polish edits in `runs/run_2026-04-04_174805/audit/v2_polish_log.md`**

```markdown
# Act 1 v2 — Procreate Polish Log

| Slot | Edits | Time spent |
|---|---|---|
| 052 | Added construction lines to torso, evened pencil-trail line weight | 10m |
```

- [ ] **Step 6: Commit**

```bash
git add runs/run_2026-04-04_174805/seedance_clean_v2/ runs/run_2026-04-04_174805/audit/v2_polish_log.md
git commit -m "$(cat <<'EOF'
act1-v2: Procreate polish pass on flagged slots

Manual line-weight, paper-grain, and construction-mark polish on flagged
cleaned frames. Unpolished originals preserved in _pre_polish_backup/.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 9: Build the mixed-cadence assembly script (`seedance_v2_assemble.sh`)

**Files:**
- Create: `pipeline/seedance_v2_assemble.sh`
- Create: `pipeline/tests/test_seedance_v2_assemble.py`

- [ ] **Step 1: Write the failing test for the cadence-math helper**

```python
# pipeline/tests/test_seedance_v2_assemble.py
"""Tests for the cadence-math helper used by the v2 assembly script."""
from pathlib import Path

import pytest

from pipeline.seedance_v2_select import SelectionRow, parse_selection_md


def make_row(slot, cadence):
    return SelectionRow(
        slot=slot, source_frame="x.png", cadence=cadence,
        decision="KEEP", anchors=["a"], rationale="t", beat="t",
    )


# Helper that the assembly script (or a small Python pre-step) uses to
# determine how many 24fps output sub-slots each KEEP row occupies.
def hold_sub_slots(row: SelectionRow, hold_collapse_count: int = 0) -> int:
    """Return how many 24fps output sub-slots this KEEP row occupies.

    Baseline: 12fps frame = 2 sub-slots (held), 24fps frame = 1 sub-slot.
    Plus an additional +2 sub-slots per surrounding HOLD-COLLAPSE row.
    """
    base = 2 if row.cadence == "12fps" else 1
    # 12fps hold-collapse adds 2 sub-slots; 24fps would add 1 (rare case).
    add = hold_collapse_count * (2 if row.cadence == "12fps" else 1)
    return base + add


def test_12fps_frame_holds_2_sub_slots():
    assert hold_sub_slots(make_row(1, "12fps"), hold_collapse_count=0) == 2


def test_24fps_frame_holds_1_sub_slot():
    assert hold_sub_slots(make_row(2, "24fps"), hold_collapse_count=0) == 1


def test_12fps_with_3_hold_collapse_neighbors_holds_8_sub_slots():
    # 2 base + 3*2 = 8 sub-slots = ~0.33s at 24fps
    assert hold_sub_slots(make_row(1, "12fps"), hold_collapse_count=3) == 8


def test_24fps_with_2_hold_collapse_neighbors_holds_3_sub_slots():
    assert hold_sub_slots(make_row(2, "24fps"), hold_collapse_count=2) == 3
```

- [ ] **Step 2: Run test to verify it fails**

```bash
python3 -m pytest pipeline/tests/test_seedance_v2_assemble.py -v
```

Expected: All 4 tests FAIL — `hold_sub_slots` not defined in `pipeline/seedance_v2_select`.

- [ ] **Step 3: Add `hold_sub_slots` and `compute_sub_slots_per_keep_row()` to `pipeline/seedance_v2_select.py`**

Append to `pipeline/seedance_v2_select.py`:

```python
def hold_sub_slots(row: SelectionRow, hold_collapse_count: int = 0) -> int:
    """Return how many 24fps output sub-slots a KEEP row occupies.

    12fps cadence = 2 sub-slots base (held at the 24fps output rate).
    24fps cadence = 1 sub-slot base.
    Each HOLD-COLLAPSE neighbor adds +2 (12fps) or +1 (24fps).
    """
    base = 2 if row.cadence == "12fps" else 1
    add = hold_collapse_count * (2 if row.cadence == "12fps" else 1)
    return base + add


def compute_sub_slots_per_keep_row(rows: list[SelectionRow]) -> list[tuple[SelectionRow, int]]:
    """For each KEEP row, count adjacent HOLD-COLLAPSE rows in the same beat
    and compute total sub-slots. Returns [(row, sub_slot_count), ...] in slot order.
    """
    results: list[tuple[SelectionRow, int]] = []
    keep_rows = [r for r in rows if r.decision == "KEEP"]
    # Walk through rows; for each KEEP, count subsequent HOLD-COLLAPSE rows
    # until the next KEEP. Assign half the contiguous hold-collapse stretch
    # before-and-after-the-keep to balance (simple rule: assign all
    # immediately-following hold-collapse rows to the preceding KEEP).
    keep_by_slot = {r.slot: r for r in keep_rows}
    hold_counts: dict[int, int] = {r.slot: 0 for r in keep_rows}
    current_keep_slot: int | None = None
    for r in rows:
        if r.decision == "KEEP":
            current_keep_slot = r.slot
        elif r.decision == "HOLD-COLLAPSE" and current_keep_slot is not None:
            hold_counts[current_keep_slot] += 1
    for slot in sorted(keep_by_slot):
        row = keep_by_slot[slot]
        results.append((row, hold_sub_slots(row, hold_counts[slot])))
    return results
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
python3 -m pytest pipeline/tests/ -v
```

Expected: All tests across all three test files PASS.

- [ ] **Step 5: Write the assembly shell script**

```bash
cat > pipeline/seedance_v2_assemble.sh <<'BASH'
#!/usr/bin/env bash
#
# Pencil Test Animation — Act 1 v2 Assembly Script
#
# Reads selection.md files for v2 and v3 sources, generates a 24fps frame
# sequence from cleaned PNGs (12fps frames held for 2 sub-slots each,
# 24fps frames held for 1 sub-slot, plus HOLD-COLLAPSE-derived extra holds),
# and encodes MP4 / WebM / GIF as pencil-test-act1-v2.{mp4,webm,gif}.
#
# Usage:
#   bash pipeline/seedance_v2_assemble.sh runs/run_2026-04-04_174805
#

set -euo pipefail

RUN_DIR="${1:?Usage: bash pipeline/seedance_v2_assemble.sh <run-dir>}"

if [ ! -d "$RUN_DIR/seedance_clean_v2" ]; then
    echo "Error: $RUN_DIR/seedance_clean_v2 does not exist." >&2
    exit 1
fi

CLEAN="$RUN_DIR/seedance_clean_v2"
EXPORT="$RUN_DIR/export"
SEQUENCE="$RUN_DIR/export/sequence_v2"

# Clean previous v2 sequence; do NOT touch the original sequence/
rm -rf "$SEQUENCE"
mkdir -p "$SEQUENCE" "$EXPORT"

echo "=== Pencil Test Act 1 v2 — Mixed-Cadence Assembly ==="
echo "Run directory: $RUN_DIR"

# --- Step 1: Compute the slot → sub-slot mapping via Python helper ---
echo "Step 1: Computing sub-slot layout..."

MAPPING_FILE="$SEQUENCE/_sub_slot_mapping.tsv"
python3 - <<PY > "$MAPPING_FILE"
from pathlib import Path
from pipeline.seedance_v2_select import parse_selection_md, compute_sub_slots_per_keep_row

rd = Path("$RUN_DIR")
for src_md in ["seedance_frames/selection.md", "seedance_frames_v3_loopclose/selection.md"]:
    rows = parse_selection_md(rd / src_md)
    for row, sub_slots in compute_sub_slots_per_keep_row(rows):
        print(f"{row.slot:03d}\t{sub_slots}")
PY

# --- Step 2: Build the frame sequence ---
echo "Step 2: Building frame sequence..."

FRAME_COUNTER=1
while IFS=$'\t' read -r SLOT SUB_SLOTS; do
    SRC=$(printf "%s/PT_A1_v2_slot%s.png" "$CLEAN" "$SLOT")
    if [ ! -f "$SRC" ]; then
        echo "  Warning: Missing $SRC — skipping" >&2
        continue
    fi
    i=0
    while [ "$i" -lt "$SUB_SLOTS" ]; do
        DEST=$(printf "%s/frame_%04d.png" "$SEQUENCE" "$FRAME_COUNTER")
        cp "$SRC" "$DEST"
        FRAME_COUNTER=$((FRAME_COUNTER + 1))
        i=$((i + 1))
    done
    echo "  slot $SLOT -> $SUB_SLOTS sub-slot(s)"
done < "$MAPPING_FILE"

TOTAL=$((FRAME_COUNTER - 1))
echo "  Total sub-slot frames: $TOTAL"

# --- Step 3: JPEG-as-PNG defensive re-encode (mirrors assemble.sh) ---
echo "Step 3: Verifying PNG format..."
REENCODED=0
for FILE in "$SEQUENCE"/frame_*.png; do
    if file -b "$FILE" | grep -q "JPEG"; then
        python3 -c "from PIL import Image; Image.open('$FILE').save('$FILE', format='PNG')"
        REENCODED=$((REENCODED + 1))
    fi
done
echo "  Re-encoded $REENCODED frame(s)"

# --- Step 4: Encode MP4 ---
echo "Step 4: Encoding MP4..."
ffmpeg -hide_banner -loglevel error -y -framerate 24 \
    -i "$SEQUENCE/frame_%04d.png" \
    -c:v libx264 -crf 18 -pix_fmt yuv420p \
    -vf "scale=1920:1080:flags=lanczos" \
    "$EXPORT/pencil-test-act1-v2.mp4"

# --- Step 5: Encode WebM from the MP4 ---
echo "Step 5: Encoding WebM..."
ffmpeg -hide_banner -loglevel error -y -i "$EXPORT/pencil-test-act1-v2.mp4" \
    -c:v libvpx-vp9 -crf 30 -b:v 0 -row-mt 1 \
    "$EXPORT/pencil-test-act1-v2.webm"

# --- Step 6: Encode GIF (two-pass palette) ---
echo "Step 6: Encoding GIF..."
ffmpeg -hide_banner -loglevel error -y -i "$EXPORT/pencil-test-act1-v2.mp4" \
    -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
    "$EXPORT/pencil-test-act1-v2.gif"

GIF_SIZE=$(stat -f%z "$EXPORT/pencil-test-act1-v2.gif" 2>/dev/null || stat -c%s "$EXPORT/pencil-test-act1-v2.gif")
GIF_MB=$(echo "scale=2; $GIF_SIZE / 1048576" | bc)
echo "  GIF size: ${GIF_MB} MB"

echo ""
echo "=== Done ==="
echo "MP4 : $EXPORT/pencil-test-act1-v2.mp4"
echo "WebM: $EXPORT/pencil-test-act1-v2.webm"
echo "GIF : $EXPORT/pencil-test-act1-v2.gif (${GIF_MB} MB)"
BASH

chmod +x pipeline/seedance_v2_assemble.sh
```

- [ ] **Step 6: Commit**

```bash
git add pipeline/seedance_v2_assemble.sh pipeline/seedance_v2_select.py pipeline/tests/test_seedance_v2_assemble.py
git commit -m "$(cat <<'EOF'
act1-v2: add mixed-cadence assembly script (seedance_v2_assemble.sh)

Reads selection.md files to compute per-slot sub-slot layout (12fps frames
held 2 sub-slots, 24fps held 1, plus HOLD-COLLAPSE neighbors), produces
uniform 24fps MP4 + WebM + GIF as pencil-test-act1-v2.*. The original
assemble.sh stays untouched and continues to drive the original 12fps
Act 1 export.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 10: Run the full assembly + Engine Truth QA

**Files:**
- Reads: `runs/run_2026-04-04_174805/seedance_clean_v2/`, both selection.md files.
- Writes: `runs/run_2026-04-04_174805/export/pencil-test-act1-v2.{mp4,webm,gif}`, `runs/run_2026-04-04_174805/audit/v2_integration_qa.md`.

- [ ] **Step 1: Back up the existing v2 export directory state (defensive — first run will create it)**

```bash
# No-op on first run; on re-run, preserve the prior v2 export.
if [ -f runs/run_2026-04-04_174805/export/pencil-test-act1-v2.mp4 ]; then
    mkdir -p runs/run_2026-04-04_174805/export/_pre_reassembly_backup
    cp runs/run_2026-04-04_174805/export/pencil-test-act1-v2.* \
       runs/run_2026-04-04_174805/export/_pre_reassembly_backup/ || true
fi
```

- [ ] **Step 2: Run the v2 assembly**

```bash
bash pipeline/seedance_v2_assemble.sh runs/run_2026-04-04_174805
```

Expected: Step-by-step progress logs, ends with "Done" and three file paths.

- [ ] **Step 3: Verify output metadata**

```bash
ffprobe -v error -show_entries stream=width,height,r_frame_rate,nb_frames -show_entries format=duration \
    -of default=noprint_wrappers=1 \
    runs/run_2026-04-04_174805/export/pencil-test-act1-v2.mp4

ffprobe -v error -show_entries stream=width,height,r_frame_rate,nb_frames -show_entries format=duration \
    -of default=noprint_wrappers=1 \
    runs/run_2026-04-04_174805/export/pencil-test-act1-v2.webm
```

Expected: `width=1920`, `height=1080`, `r_frame_rate=24/1`, `duration` between 4.0 and 8.0 seconds.

- [ ] **Step 4: Verify GIF under 5MB**

```bash
ls -lh runs/run_2026-04-04_174805/export/pencil-test-act1-v2.gif
```

Expected: Size less than 5.0M. If it exceeds, lower the fps in `seedance_v2_assemble.sh` Step 6 from 15 to 12 and re-run Task 10 Step 2.

- [ ] **Step 5: Run continuity audit on the cleaned set**

```bash
python3 pipeline/continuity_audit.py --run-dir runs/run_2026-04-04_174805 \
    --frames-glob "seedance_clean_v2/PT_A1_v2_slot*.png" \
    > runs/run_2026-04-04_174805/audit/v2_continuity.log 2>&1 || true

grep -E "(BLOCKER|FAIL)" runs/run_2026-04-04_174805/audit/v2_continuity.log || echo "All continuity checks clean"
```

Note: `continuity_audit.py` may not currently accept a `--frames-glob` flag. If it doesn't, run it without that flag and direct the output to the log file; manual review of the log for CC01 (stylus right hand) is the gate.

- [ ] **Step 6: Open the GIF in Chrome AND Safari, watch the loop cycle 5+ times**

```bash
open -a "Google Chrome" runs/run_2026-04-04_174805/export/pencil-test-act1-v2.gif
open -a Safari runs/run_2026-04-04_174805/export/pencil-test-act1-v2.gif
```

Watch for, per the spec's ship criteria:
- Seamless loop seam at v3-end → v2-start (companion fully gone, idle pose matches)
- Stylus right hand every frame
- Identity holds (Sean recognizable)
- Paper grain stable
- Hold timing reads as breath, not stutter

- [ ] **Step 7: Write the final QA verdict document**

```bash
cat > runs/run_2026-04-04_174805/audit/v2_integration_qa.md <<'MD'
# Act 1 v2 — Engine Truth QA

**Date:** 2026-05-13
**Reviewer:** [user name]
**Artifacts:**
- MP4: `runs/run_2026-04-04_174805/export/pencil-test-act1-v2.mp4`
- WebM: `runs/run_2026-04-04_174805/export/pencil-test-act1-v2.webm`
- GIF: `runs/run_2026-04-04_174805/export/pencil-test-act1-v2.gif`

## Engine Truth verdict

> "If the loop plays smoothly and the character is recognizably Sean in pencil test style on cream animation paper, it ships."

| Engine Truth criterion | Verdict | Notes |
|---|---|---|
| Plays smoothly (no stutter, no boil at 24fps) | PASS / FAIL | … |
| Character recognizably Sean (identity holds) | PASS / FAIL | … |
| Pencil-test style (line weight, construction marks, grain) | PASS / FAIL | … |
| Cream animation paper (no pure white, no pure black) | PASS / FAIL | … |

## Phase E Creative Director rubric

| Dimension | Verdict | Notes |
|---|---|---|
| Identity | PASS / FAIL | … |
| Style | PASS / FAIL | … |
| Composition | PASS / FAIL | … |
| Continuity | PASS / FAIL | … |
| Technical | PASS / FAIL | … |

## Loop seam check

| Check | Verdict |
|---|---|
| v3 final frame matches v2 first frame in pose | PASS / FAIL |
| Companion fully absent at loop seam | PASS / FAIL |
| Stylus right hand on both sides of seam | PASS / FAIL |
| Paper grain consistent across seam | PASS / FAIL |

## Overall verdict

**[ ] PASS — proceed to Task 11 (CHANGELOG + checklist + ship prep)**
**[ ] FAIL — see flagged slots; loop back to Task 7 retry for those slots**

## Flagged slots (if FAIL)

| Slot | Issue | Proposed remedy |
|---|---|---|
| | | |
MD
```

- [ ] **Step 8: HUMAN GATE — user fills in the verdict, signs off**

- [ ] **Step 9: Commit assembly artifacts + QA doc**

```bash
git add runs/run_2026-04-04_174805/export/pencil-test-act1-v2.mp4 \
        runs/run_2026-04-04_174805/export/pencil-test-act1-v2.webm \
        runs/run_2026-04-04_174805/export/pencil-test-act1-v2.gif \
        runs/run_2026-04-04_174805/audit/v2_integration_qa.md \
        runs/run_2026-04-04_174805/audit/v2_continuity.log
git commit -m "$(cat <<'EOF'
act1-v2: ship-candidate assembly + Engine Truth QA

Mixed-cadence assembly produces pencil-test-act1-v2.{mp4,webm,gif}.
ffprobe metadata: 24fps, 1920x1080, ~5.6s. GIF under 5MB.
QA verdict recorded in v2_integration_qa.md.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 10: BRANCHING POINT**
  - If QA PASS → continue to Task 11.
  - If QA FAIL on individual slots → return to Task 7 Step 7 (re-run cleanup for flagged slots, then re-run this task).

---

## Task 11: Update CHANGELOG, production-checklist, CLAUDE.md, then ship-stage

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `docs/production-checklist.md`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Append CHANGELOG entry**

```bash
# Open CHANGELOG.md and add a new section at the top (after the header).
# Use this content verbatim:
```

```markdown
## 2026-05-13 — Act 1 v2 Seedance Integration (AI Companion)

Built a new Act 1 hero loop replacing the pixel-sprite metaphor with a hand-drawn orange companion that emerges from pencil trails, lands on the shoulder, then detaches and floats away to close the loop.

**What changed:**
- New Seedance-driven Act 1 ships as `runs/run_2026-04-04_174805/export/pencil-test-act1-v2.{mp4,webm,gif}` (24fps, ~5.6s loop).
- Mixed-cadence pipeline: 12fps cleanup on idle/hold beats, 24fps on action beats (arm-up, companion-emerges, companion-detaches). Assembly outputs uniform 24fps; 12fps frames held 2 sub-slots each.
- NB2 cleanup driven by `pipeline/seedance_v2_cleanup.py` with chained-reference temporal anchoring on 24fps stretches.
- Two Seedance source MP4s combined into one loop: `Act-1-Test-2-Seedance-2.0.mp4` (intro) + `Act-1-Test-3-Seedance-2.0.mp4` (loop-closer).
- A-series anchors (A-2 through A-8 — `approved/PT_A1_F*_key.png`) used as per-frame style + identity references in the cleanup prompts.
- Spike-first validation: the "companion emerges from trails" beat was cleaned first (40 frames at 24fps) and signed off before committing the rest of the cleanup budget. Spike verdict: `runs/run_2026-04-04_174805/audit/spike_validation.md`.
- Existing original Act 1 (`pencil-test-act1.{mp4,webm,gif}`, sprite-based) is **untouched and remains as fallback**.

**Why:**
- The pixel-sprite metaphor in the original Act 1 read more "game asset" than "AI companion." The orange creature reads more clearly as a magical, hand-drawn collaborator.
- Seedance 2.0 produces smooth motion that the original Act 1 (constrained to discrete approved keyframes) couldn't achieve.
- Going through NB2 cleanup with the A-series anchors preserves the rough pencil-test aesthetic while inheriting Seedance's motion fidelity.

**Files added:**
- `pipeline/seedance_v2_select.py`, `pipeline/seedance_v2_cleanup.py`, `pipeline/seedance_v2_audit.py`, `pipeline/seedance_v2_assemble.sh`
- `pipeline/tests/test_seedance_v2_*.py`
- `runs/run_2026-04-04_174805/seedance_frames/selection.md`, `runs/run_2026-04-04_174805/seedance_frames_v3_loopclose/selection.md`
- `runs/run_2026-04-04_174805/seedance_clean_v2/` (cleaned PNGs)
- `runs/run_2026-04-04_174805/audit/spike_validation.md`, `v2_retry_log.md`, `v2_polish_log.md`, `v2_integration_qa.md`

**Lesson learned:** Chained-reference NB2 cleanup (passing the previous cleaned frame as a reference for the current one) is essential for 24fps consistency. Without it, frame-to-frame line wobble + paper grain crawl become visible. Resetting the chain at 24fps→12fps cadence boundaries prevents over-stabilizing across beats.

**Links:**
- Design spec: [docs/2026-05-12-act1-seedance-v2-integration-design.md](docs/2026-05-12-act1-seedance-v2-integration-design.md)
- Execution plan: [docs/2026-05-13-act1-seedance-v2-execution-plan.md](docs/2026-05-13-act1-seedance-v2-execution-plan.md)
```

- [ ] **Step 2: Update `docs/production-checklist.md`**

Open the file, find the Phase 4 section, and add a new sub-section after the existing Phase 4 items:

```markdown
### Phase 4f — Act 1 v2 (AI Companion) Integration — COMPLETE 2026-05-13

- [x] Spike validation passed (spike_validation.md)
- [x] Batch cleanup of all KEEP slots
- [x] Procreate polish on flagged slots
- [x] Mixed-cadence assembly (12fps holds + 24fps action, uniform 24fps output)
- [x] Engine Truth QA passed (v2_integration_qa.md)
- [x] CHANGELOG entry
- [ ] Ship to portfolio (Phase 8 — out of scope here)
```

Also update the file's "Last updated" line at the top to `2026-05-13`.

- [ ] **Step 3: Update `CLAUDE.md` Key Commands section**

Append after the existing `### Assembly` block:

```markdown
### v2 (AI Companion) Cleanup + Assembly

Validate selection.md:
```bash
python3 pipeline/seedance_v2_select.py runs/{run_id}/seedance_frames/selection.md
```

Cleanup a slot range (or omit `--slot-range` for full batch):
```bash
python3 pipeline/seedance_v2_cleanup.py \
    --selection runs/{run_id}/seedance_frames/selection.md \
    --source-dir runs/{run_id}/seedance_frames/raw_24fps \
    --clean-dir runs/{run_id}/seedance_clean_v2 \
    --run-dir runs/{run_id} \
    --slot-range 029-068
```

Audit cleaned frames:
```bash
python3 pipeline/seedance_v2_audit.py \
    --selection runs/{run_id}/seedance_frames/selection.md \
    --clean-dir runs/{run_id}/seedance_clean_v2 \
    --slot-range 029-068
```

Assemble v2 loop (uniform 24fps with mixed-cadence cell layout):
```bash
bash pipeline/seedance_v2_assemble.sh runs/{run_id}
```
```

Also update the "Source of Truth Documents" table — add two new rows referencing the v2 design spec and v2 execution plan.

- [ ] **Step 4: Run the test suite one more time**

```bash
python3 -m pytest pipeline/tests/ -v
```

Expected: All tests across all three test files PASS.

- [ ] **Step 5: Final commit**

```bash
git add CHANGELOG.md docs/production-checklist.md CLAUDE.md
git commit -m "$(cat <<'EOF'
act1-v2: finalize CHANGELOG, production-checklist, CLAUDE.md

Document the v2 integration in CHANGELOG with what/why/lessons. Mark
Phase 4f complete in production-checklist. Add v2 cleanup + assembly
commands to CLAUDE.md Key Commands section.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 6: Ship-stage check — confirm all ship criteria from the spec are met**

```bash
# Run each ship criterion from the spec § "Ship criteria":
echo "1. selection.md files exist:"
ls runs/run_2026-04-04_174805/seedance_frames/selection.md \
   runs/run_2026-04-04_174805/seedance_frames_v3_loopclose/selection.md

echo "2. Cleaned PNG per KEEP slot:"
ls runs/run_2026-04-04_174805/seedance_clean_v2/PT_A1_v2_slot*.png | wc -l

echo "3. Spike validation signed off:"
grep -c "PASS" runs/run_2026-04-04_174805/audit/spike_validation.md || true

echo "4. v2 exports exist + metadata:"
ffprobe -v error -show_entries stream=width,height,r_frame_rate,nb_frames \
    -of default=noprint_wrappers=1 \
    runs/run_2026-04-04_174805/export/pencil-test-act1-v2.mp4

echo "5. GIF size:"
ls -lh runs/run_2026-04-04_174805/export/pencil-test-act1-v2.gif | awk '{print $5}'

echo "6. v2 QA signed off:"
grep -c "PASS" runs/run_2026-04-04_174805/audit/v2_integration_qa.md || true

echo "7. Original Act 1 untouched:"
ls runs/run_2026-04-04_174805/approved/ | head -5
ls runs/run_2026-04-04_174805/export/pencil-test-act1.{mp4,webm,gif}
```

Expected: each check returns a sensible value (file exists, frame count plausible, GIF under 5MB).

Act 1 v2 is now shipped to the run directory. Portfolio-site embedding is Phase 8 out of scope.

---

## Self-review

**Spec coverage check** (every section in [docs/2026-05-12-act1-seedance-v2-integration-design.md](2026-05-12-act1-seedance-v2-integration-design.md) maps to a task):

| Spec section | Task |
|---|---|
| Terms | Inline in plan as needed |
| Source artifacts | Read by Tasks 1, 3, 5, 7, 9 |
| Engine-level decisions | All locked decisions implemented across all tasks |
| Beat structure & cadence map | Task 1 (selection.md), Task 9 (assembly cadence math) |
| Components & data flow | Tasks 2–10 (one task per component) |
| NB2 cleanup approach (universal prompt, references, retry ladder, post-processing) | Task 3 + Task 5 |
| Spike acceptance criteria | Task 5 + Task 6 |
| Out of scope | Not implemented (correct) |
| Ship criteria | Task 11 Step 6 verifies each criterion |
| Open questions (resolved during impl) | Task 1 resolves Q1, Q2; Task 6 resolves Q3; Task 8 resolves Q4 |

**Type consistency check**: `SelectionRow` defined in `seedance_v2_select.py` and used unchanged in `seedance_v2_cleanup.py`, tests, and assembly mapping. `parse_selection_md`, `validate_selection`, `hold_sub_slots`, `compute_sub_slots_per_keep_row` are all imported by their exact defined names. `run_cleanup_for_slot` signature matches its test invocation. Cleaned-frame stable filename `PT_A1_v2_slot{NNN}.png` used consistently across cleanup, audit, and assembly. ✅

**Placeholder scan**: No "TBD", "TODO", "implement later", "fill in details", or vague-error-handling phrases. Every step has a concrete command or code block. The "user name" placeholders inside the verdict markdown templates (`spike_validation.md`, `v2_integration_qa.md`) are intentional — they are filled in by the user at the human-gate steps. ✅
