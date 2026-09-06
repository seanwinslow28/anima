#!/usr/bin/env bash
# gpt_image_2 WITH a design reference. Same comment-strip + byte guard as the other runners.
set -euo pipefail
cd "$(dirname "$0")/.."
PROMPT_FILE="$1"; REF="$2"; RATIO="$3"; OUT="$4"
CLEAN="$(mktemp)"
grep -v '^#' "$PROMPT_FILE" | awk 'NF||p{print;p=1}' > "$CLEAN"
n=$(wc -c < "$CLEAN" | tr -d ' '); echo "prompt bytes: $n"
if [ "$n" -lt 300 ]; then echo "ABORT — prompt too short, refusing to spend"; exit 1; fi
higgsfield generate create gpt_image_2 --prompt "$(cat "$CLEAN")" --image "$REF" \
  --quality high --resolution 2k --aspect_ratio "$RATIO" --json --wait --wait-timeout 15m > "$OUT"
