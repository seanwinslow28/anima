#!/usr/bin/env bash
#
# Pencil Test Animation — Assembly Script
# anima — Phase 8 assembly. Behavior unchanged in commit 4.
# DAG-orchestrated invocation: USE_DAG_RUNNER=1 python -m pipeline.dag run
#
# Takes approved keyframes and in-betweens from a run directory, builds an
# interleaved frame sequence (42 frames for Act 1), and exports GIF, WebM, and MP4.
#
# Usage:
#   bash pipeline/assemble.sh runs/run_2026-04-04_174805
#

set -euo pipefail

RUN_DIR="${1:?Usage: bash pipeline/assemble.sh <run-dir> [--slug <name>] [--sequence-file <path>]}"
shift

# Optional generalization (#13): a per-piece sequence + output slug. The defaults
# below reproduce the PT_A1 behavior byte-identically when no flags are passed.
SLUG="pencil-test-act1"
SEQUENCE_FILE=""
while [ $# -gt 0 ]; do
    case "$1" in
        --slug)          SLUG="${2:?--slug needs a value}"; shift 2 ;;
        --sequence-file) SEQUENCE_FILE="${2:?--sequence-file needs a value}"; shift 2 ;;
        *) echo "Error: unknown argument: $1" >&2; exit 1 ;;
    esac
done

if [ ! -d "$RUN_DIR/approved" ]; then
    echo "Error: No approved/ directory in $RUN_DIR" >&2
    exit 1
fi

APPROVED="$RUN_DIR/approved"
EXPORT="$RUN_DIR/export"
SEQUENCE="$RUN_DIR/export/sequence"

# Clean previous sequence
rm -rf "$SEQUENCE"
mkdir -p "$SEQUENCE" "$EXPORT"

echo "=== Pencil Test Act 1 — Assembly (with In-Betweens) ==="
echo "Run directory: $RUN_DIR"
echo ""

# --- Step 1: Build frame sequence with in-betweens interleaved ---
#
# Frame sequence (42 frames at 12fps = 3.5s):
#
# Beat 1: The Spark (F01→F13) — 17 frames
#   F01_key       hold 3   (frames 0001-0003)  idle
#   F01toF06_IB01 hold 1   (frame  0004)       head begins to tilt
#   F01toF06_IB02 hold 1   (frame  0005)       deeper tilt
#   F01toF06_IB03 hold 1   (frame  0006)       near full glance down
#   F06_key       hold 2   (frames 0007-0008)  glance down
#   F06toF10_IB01 hold 1   (frame  0009)       head lifting
#   F10_key       hold 2   (frames 0010-0011)  the spark
#   F10toF13_IB01 hold 1   (frame  0012)       transitioning to ready
#   F13_key       hold 2   (frames 0013-0014)  ready pose
#   F13toF18_IB01 hold 1   (frame  0015)       arm begins to lift
#   F13toF18_IB02 hold 1   (frame  0016)       arm at arc apex
#   F13toF18_IB03 hold 1   (frame  0017)       arm sweeping forward
#
# Beat 2: The Draw (F18→F28) — 12 frames (transformation sequence)
#   F18_key       hold 2   (frames 0018-0019)
#   F20_key       hold 2   (frames 0020-0021)
#   F22_key       hold 2   (frames 0022-0023)
#   F24_key       hold 2   (frames 0024-0025)
#   F26_key       hold 2   (frames 0026-0027)
#   F28_key       hold 2   (frames 0028-0029)  (reduced from 3)
#
# Beat 2→3 Transition (F28→F31) — 4 frames (sprite flight, composited)
#   F28toF31_IB01_comp  hold 1  (frame  0030)  sprite mid-flight
#   F28toF31_IB02_comp  hold 1  (frame  0031)  sprite approaching shoulder
#
# Beat 3: The Nod (F31→F40) — 12 frames
#   F31_key       hold 2   (frames 0032-0033)  sprite lands (reduced from 3)
#   F31toF36_IB01 hold 1   (frame  0034)       nod begins
#   F31toF36_IB02 hold 1   (frame  0035)       deeper nod
#   F36_key       hold 2   (frames 0036-0037)  the nod
#   F36toF40_IB01 hold 1   (frame  0038)       returning to idle
#   F36toF40_IB02 hold 1   (frame  0039)       near idle
#   F40_key       hold 3   (frames 0040-0042)  return to idle (loop point)

echo "Step 1: Building frame sequence..."

# Sequence definition: "source_file:hold_count" pairs
# Keyframes use F##_key format, in-betweens use F##toF##_IB## format.
# Default (no --sequence-file): the embedded PT_A1 sequence + PT_A1_ source prefix.
# With --sequence-file: read the same KEY:hold format from disk; its keys are full
# basenames (e.g. SS_F03b_key), so the source prefix is empty.
if [ -n "$SEQUENCE_FILE" ]; then
    if [ ! -f "$SEQUENCE_FILE" ]; then
        echo "Error: sequence file not found: $SEQUENCE_FILE" >&2
        exit 1
    fi
    FRAME_SEQ="$(cat "$SEQUENCE_FILE")"
    SRC_PREFIX=""
else
    FRAME_SEQ="
F01_key:3
F01toF06_IB01:1
F01toF06_IB02:1
F01toF06_IB03:1
F06_key:2
F06toF10_IB01:1
F10_key:2
F10toF13_IB01:1
F13_key:2
F13toF18_IB01:1
F13toF18_IB02:1
F13toF18_IB03:1
F18_key:2
F20_key:2
F22_key:2
F24_key:2
F26_key:2
F28_key:2
F28toF31_IB01_comp:1
F28toF31_IB02_comp:1
F31_key:2
F31toF36_IB01:1
F31toF36_IB02:1
F36_key:2
F36toF40_IB01:1
F36toF40_IB02:1
F40_key:3
"
    SRC_PREFIX="PT_A1_"
fi

FRAME_COUNTER=1

for ENTRY in $FRAME_SEQ; do
    ASSET="${ENTRY%%:*}"
    HOLD="${ENTRY##*:}"
    SRC="$APPROVED/${SRC_PREFIX}${ASSET}.png"

    if [ ! -f "$SRC" ]; then
        echo "  Warning: Missing $SRC — skipping" >&2
        FRAME_COUNTER=$((FRAME_COUNTER + HOLD))
        continue
    fi

    i=0
    while [ "$i" -lt "$HOLD" ]; do
        DEST=$(printf "%s/frame_%04d.png" "$SEQUENCE" "$FRAME_COUNTER")
        cp "$SRC" "$DEST"
        FRAME_COUNTER=$((FRAME_COUNTER + 1))
        i=$((i + 1))
    done
    echo "  ${ASSET} -> hold ${HOLD} frames"
done

TOTAL=$((FRAME_COUNTER - 1))
echo "  Total frames: $TOTAL"
echo ""

# --- Step 2: Check all frames exist ---
MISSING=0
i=1
while [ "$i" -le "$TOTAL" ]; do
    FILE=$(printf "%s/frame_%04d.png" "$SEQUENCE" "$i")
    if [ ! -f "$FILE" ]; then
        echo "  Missing: $FILE" >&2
        MISSING=$((MISSING + 1))
    fi
    i=$((i + 1))
done

if [ "$MISSING" -gt 0 ]; then
    echo "Error: $MISSING frames missing. Generate and approve all keyframes first." >&2
    exit 1
fi

echo "Step 2: All $TOTAL frames present."
echo ""

# --- Step 2b: Re-encode any JPEG-as-PNG frames ---
# Gemini API returns JPEG data that gets saved with .png extension.
# FFmpeg's image2 demuxer expects actual PNG format and silently drops
# mismatched frames, causing missing frames in the export.
echo "Step 2b: Verifying PNG format..."
REENCODED=0
for FILE in "$SEQUENCE"/frame_*.png; do
    if file -b "$FILE" | grep -q "JPEG"; then
        python3 -c "from PIL import Image; Image.open('$FILE').save('$FILE', format='PNG')"
        REENCODED=$((REENCODED + 1))
    fi
done
if [ "$REENCODED" -gt 0 ]; then
    echo "  Re-encoded $REENCODED frames (JPEG→PNG)"
else
    echo "  All frames are valid PNGs"
fi
echo ""

# --- Step 3: Assemble MP4 (archival quality) ---
echo "Step 3: Assembling MP4..."
ffmpeg -y -framerate 12 -start_number 1 \
    -i "$SEQUENCE/frame_%04d.png" \
    -c:v libx264 -crf 18 -pix_fmt yuv420p \
    -vf "scale=1920:1080:flags=lanczos" \
    "$EXPORT/${SLUG}.mp4" \
    2>/dev/null

if [ -f "$EXPORT/${SLUG}.mp4" ]; then
    SIZE=$(du -h "$EXPORT/${SLUG}.mp4" | cut -f1)
    echo "  Created: ${SLUG}.mp4 ($SIZE)"
else
    echo "  Error: MP4 creation failed" >&2
fi
echo ""

# --- Step 4: Convert to WebM (web playback) ---
echo "Step 4: Converting to WebM..."
ffmpeg -y -i "$EXPORT/${SLUG}.mp4" \
    -c:v libvpx-vp9 -crf 30 -b:v 0 \
    -vf "scale=1920:1080:flags=lanczos" \
    "$EXPORT/${SLUG}.webm" \
    2>/dev/null

if [ -f "$EXPORT/${SLUG}.webm" ]; then
    SIZE=$(du -h "$EXPORT/${SLUG}.webm" | cut -f1)
    echo "  Created: ${SLUG}.webm ($SIZE)"
else
    echo "  Error: WebM creation failed" >&2
fi
echo ""

# --- Step 5: Create GIF (hero loop, two-pass palette, <5MB target) ---
echo "Step 5: Creating GIF (two-pass palette)..."
ffmpeg -y -i "$EXPORT/${SLUG}.mp4" \
    -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
    "$EXPORT/${SLUG}.gif" \
    2>/dev/null

if [ -f "$EXPORT/${SLUG}.gif" ]; then
    SIZE_BYTES=$(stat -f%z "$EXPORT/${SLUG}.gif" 2>/dev/null || stat -c%s "$EXPORT/${SLUG}.gif" 2>/dev/null)
    SIZE_MB=$(echo "scale=2; $SIZE_BYTES / 1048576" | bc)
    SIZE_HUMAN=$(du -h "$EXPORT/${SLUG}.gif" | cut -f1)
    echo "  Created: ${SLUG}.gif ($SIZE_HUMAN)"

    # Check 5MB limit
    if (( $(echo "$SIZE_MB > 5" | bc -l) )); then
        echo "  Warning: GIF exceeds 5MB target ($SIZE_MB MB). Consider reducing scale or fps." >&2
    else
        echo "  Size check: ${SIZE_MB}MB (under 5MB limit)"
    fi
else
    echo "  Error: GIF creation failed" >&2
fi
echo ""

# --- Summary ---
echo "=== Assembly Complete ==="
echo "Exports in: $EXPORT/"
ls -lh "$EXPORT/"*.{mp4,webm,gif} 2>/dev/null || echo "  (no exports found)"
echo ""
echo "To preview the loop: open $EXPORT/${SLUG}.gif"
