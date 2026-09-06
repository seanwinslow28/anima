#!/usr/bin/env bash
# Strip the comment header, guard against an empty prompt, generate.
# The spend guard exists because a sed error once emptied a prompt file after `>` had
# truncated it and the CLI accepted "" as satisfying a required string — 49 credits, two
# null clips. Never remove the byte check.
set -euo pipefail
cd "$(dirname "$0")/.."
PROMPT_FILE="$1"; START_IMAGE="$2"; OUT="$3"; DURATION="${4:-7}"
# Wave 3b (2026-09-06): optional 4th arg = seconds (default 7). seedance_2_0 fast ≈ 3.5 cr/s: 5s ≈ 17.5, 10s ≈ 35.
CLEAN="$(mktemp)"
grep -v '^#' "$PROMPT_FILE" | awk 'NF||p{print;p=1}' > "$CLEAN"
n=$(wc -c < "$CLEAN" | tr -d ' ')
echo "prompt bytes: $n  duration: ${DURATION}s"
if [ "$n" -lt 400 ]; then echo "ABORT — prompt too short, refusing to spend"; exit 1; fi
echo "--- prompt sent ---"; cat "$CLEAN"; echo "--- end ---"
higgsfield generate create seedance_2_0 --prompt "$(cat "$CLEAN")" \
  --start-image "$START_IMAGE" \
  --mode fast --duration "$DURATION" --resolution 720p --aspect_ratio 16:9 \
  --generate_audio false --json --wait --wait-timeout 20m > "$OUT"
echo "job json -> $OUT"
