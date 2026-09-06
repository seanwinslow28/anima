#!/usr/bin/env bash
# gpt_image_2 with TWO role-split refs (bible + camera rough), 16:9.
set -euo pipefail
cd "$(dirname "$0")/.."
P="$1"; R1="$2"; R2="$3"; OUT="$4"
C="$(mktemp)"; grep -v '^#' "$P" | awk 'NF||p{print;p=1}' > "$C"
n=$(wc -c < "$C" | tr -d ' '); echo "prompt bytes: $n"
if [ "$n" -lt 300 ]; then echo "ABORT"; exit 1; fi
higgsfield generate create gpt_image_2 --prompt "$(cat "$C")" --image "$R1" --image "$R2" \
  --quality high --resolution 2k --aspect_ratio 16:9 --json --wait --wait-timeout 15m > "$OUT"
