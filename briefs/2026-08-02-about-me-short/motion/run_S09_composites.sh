#!/usr/bin/env bash
# The five S09 composites, each onto the CLEAN plate, in depth order. 5 × 8.5 = 42.5 cr.
# Every call goes through motion/composite.sh (comment-strip + byte guard). Stops on the first failure.
set -euo pipefail
cd "$(dirname "$0")/.."
PLATE=normalised/S09-room-reacts-v1.png
mkdir -p composites/S09
for c in claude codex sean gemini grok; do
  case $c in sean) ref=refs/turnaround-views/sean-v4.png;; *) ref=refs/turnaround-views/$c-v2.png;; esac
  echo "=== $c ($ref)"
  motion/composite.sh prompts/composites-S09/S09-$c.txt "$ref" "$PLATE" composites/S09/S09-$c.json
  python3 - "$c" <<'PY'
import json, sys, urllib.request
c = sys.argv[1]; j = json.load(open(f"composites/S09/S09-{c}.json")); j = j[0] if isinstance(j, list) else j
print(c, j["status"], j["id"], "prompt", len(j["params"]["prompt"]), "medias", len(j["params"]["medias"]))
assert j["status"] == "completed", j["status"]
urllib.request.urlretrieve(j["result_url"], f"composites/S09/S09-{c}-v1.png")
PY
done
echo "=== merge: matte each character off its edit onto the pristine plate, far to near"
/Users/seanwinslow/Code-Brain/anima/.venv/bin/python post/merge_edits.py "$PLATE" \
  composites/S09/S09-claude-v1.png composites/S09/S09-codex-v1.png composites/S09/S09-sean-v1.png \
  composites/S09/S09-gemini-v1.png composites/S09/S09-grok-v1.png \
  --zone 0.52,0.12,0.72,0.42 --zone 0.30,0.12,0.50,0.42 --zone 0.62,0.30,0.88,0.72 \
  --zone 0.12,0.30,0.48,0.85 --zone 0.52,0.50,0.98,1.00 \
  --debug composites/S09/masks -o composites/S09/S09-all-v1.png
echo "done — verify: post/verify_edit.py $PLATE composites/S09/S09-all-v1.png ; then normalise"
