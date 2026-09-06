# A/B — does giving Seedance the turnaround help? Codex, 2026-08-31

**One variable.** Same start frame (`normalised/S04-codex-composite-frontal-v1.png`), same
prompt (`../../prompts/motion/04-single-character-7s-ADOPTED.txt`, verbatim, comment header
stripped — 752 characters, confirmed identical in both job records), same
`seedance_2_0 · fast · 7s · 720p · 16:9 · generate_audio false`.

- **Arm A** — start frame only. 1 media.
- **Arm B** — start frame **+ three single-character turnaround views** as `image_references`:
  `codex-v1` (front), `codex-v3` (profile), `codex-v5` (back). 4 media. **Same 24.5 credits.**

## Result

| | arm A · no refs | arm B · + 3 refs |
|---|---|---|
| layout vs the start frame, frame 0 | **0.988** | **0.273** |
| background drift | **7.1%** | 19.3% |
| whole-frame motion energy | 1.21 | 6.91 |
| face holds the chevron/dot/dash | **no** | **no** |

### 1. References override the start frame. This is the headline.

Arm B's **first frame is already a different shot** — the camera has pushed in, Codex fills
half the frame and the room is cropped away. Not drift over seven seconds; frame zero.

On `seedance_2_0`, `image_references` are **subject-presentation references, not identity-only
references.** Handed three portraits of a character standing large and centred against plain
paper, the model composed the clip that way and discarded the plate's framing. The higher
motion-energy number is mostly that — a bigger subject moves more pixels.

**So: do not pass character references to `seedance_2_0` for a shot that has to match a plate.**
The plate is the continuity, and this costs it.

### 2. Neither arm fixed the mouth. The ¾-front still did not fix it either.

Both clips grow a second round eye and an open, teeth-showing grin by about 5s. The defect
predates this test and survived both changes, so it is **not** an unseen-face problem — the
model had the face, from the still in arm A and from three views in arm B.

Read: it is a **prompt** problem. The lock

> Its face stays a pale chevron, one dot eye and a short underscore bar with small brows.

says what the face *is at rest* and nothing about what it does through the beat, while the
beat ends on *"throws both arms overhead in triumph"* inside a *"1950s theatrical cartoon
slapstick"* genre anchor. Triumph in that idiom has an open laughing mouth. The model is
resolving a conflict the prompt sets up, and it resolves it against the lock.

Next thing to try, and it is a prompt edit, not a route change: state the mouth as a constant
through time rather than as a rest state — *"its mouth is the same short straight white dash in
every frame"* — the way `"Its feet return to the floor on every landing"` already works.

### 3. Arm A is otherwise the best clip this project has produced.

Locked camera, plate held at 7.1% drift, and a genuine three-part beat out of a still where
Codex was merely standing: it springs up to the rack, works, drops, and finishes arms-overhead.

## If the turnaround is still wanted

`seedance_2_5`'s **`omni_reference`** mode is the one designed to separate reference-identity
from start-frame composition — and `start_image` is *only* legal in that mode, which is a
strong hint that this is the failure it exists to prevent. 45.5 cr vs 24.5, and it is a
different model with no `fast`/`std`, so nothing measured on 2.0 carries over to it.

## Cost, honestly

98 credits for this experiment, not 49. The first pair ran with an **empty prompt** — a `sed`
error emptied the prompt file after `>` had already truncated it, and the CLI accepted `""` as
satisfying a required string. Those two clips are kept at `empty-prompt-control/` because they
are a real datapoint about how much of the result is the prompt: with no prompt at all the
plate came apart completely (87.9% drift against arm A's 7.1%).

**Guard added:** build the prompt file, assert its byte count, print it, and only then spend.
