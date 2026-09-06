#!/usr/bin/env bash
# Two-keyframe variant of motion/generate.sh — same comment-strip and byte guard.
set -euo pipefail
cd "$(dirname "$0")/.."
PROMPT_FILE="$1"; START="$2"; END="$3"; OUT="$4"
CLEAN="$(mktemp)"
grep -v '^#' "$PROMPT_FILE" | awk 'NF||p{print;p=1}' > "$CLEAN"
n=$(wc -c < "$CLEAN" | tr -d ' '); echo "prompt bytes: $n"
if [ "$n" -lt 400 ]; then echo "ABORT — prompt too short, refusing to spend"; exit 1; fi
higgsfield generate create seedance_2_0 --prompt "$(cat "$CLEAN")" \
  --start-image "$START" --end-image "$END" \
  --mode fast --duration 7 --resolution 720p --aspect_ratio 16:9 \
  --generate_audio false --json --wait --wait-timeout 20m > "$OUT"
echo "job json -> $OUT"
