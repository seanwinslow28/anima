#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
P="$1"; CHAR="$2"; SCENE="$3"; OUT="$4"
C="$(mktemp)"; grep -v '^#' "$P" | awk 'NF||p{print;p=1}' > "$C"
n=$(wc -c < "$C" | tr -d ' '); echo "prompt bytes: $n"
if [ "$n" -lt 300 ]; then echo "ABORT"; exit 1; fi
higgsfield generate create gpt_image_2 --prompt "$(cat "$C")" --image "$CHAR" --image "$SCENE" \
  --quality high --resolution 2k --aspect_ratio 16:9 --json --wait --wait-timeout 15m > "$OUT"
