#!/usr/bin/env bash
# gpt_image_2 surgical edit, same comment-strip + byte guard as motion/generate.sh.
set -euo pipefail
cd "$(dirname "$0")/.."
PROMPT_FILE="$1"; SRC="$2"; OUT="$3"
CLEAN="$(mktemp)"
grep -v '^#' "$PROMPT_FILE" | awk 'NF||p{print;p=1}' > "$CLEAN"
n=$(wc -c < "$CLEAN" | tr -d ' '); echo "prompt bytes: $n"
if [ "$n" -lt 300 ]; then echo "ABORT — prompt too short, refusing to spend"; exit 1; fi
higgsfield generate create gpt_image_2 --prompt "$(cat "$CLEAN")" --image "$SRC" \
  --quality high --resolution 2k --aspect_ratio 16:9 --json --wait --wait-timeout 15m > "$OUT"
echo "job json -> $OUT"
