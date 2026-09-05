#!/usr/bin/env bash
# gpt_image_2 with ANY number of role-split refs, 16:9 2k high. Same comment-strip +
# byte guard as every other runner. Usage: gen_image_refs.sh <prompt> <out.json> <ref>...
set -euo pipefail
cd "$(dirname "$0")/.."
P="$1"; OUT="$2"; shift 2
C="$(mktemp)"; grep -v '^#' "$P" | awk 'NF||p{print;p=1}' > "$C"
n=$(wc -c < "$C" | tr -d ' '); echo "prompt bytes: $n"
if [ "$n" -lt 300 ]; then echo "ABORT — prompt too short, refusing to spend"; exit 1; fi
ARGS=(); for r in "$@"; do [ -f "$r" ] || { echo "ABORT — missing ref $r"; exit 1; }; ARGS+=(--image "$r"); done
echo "--- prompt sent ---"; cat "$C"; echo "--- end ---"; echo "refs: $*"
higgsfield generate create gpt_image_2 --prompt "$(cat "$C")" "${ARGS[@]}" \
  --quality high --resolution 2k --aspect_ratio 16:9 --json --wait --wait-timeout 15m > "$OUT"
echo "job json -> $OUT"
