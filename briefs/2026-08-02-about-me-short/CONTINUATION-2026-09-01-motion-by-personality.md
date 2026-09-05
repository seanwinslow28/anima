# CONTINUATION — 2026-09-01 · motion, one move per personality

Hand-off from the session that finished the Movement 1 frames and then got motion wrong twice.
**Read this whole file before generating anything.** Then read, in order:

1. [`prompts/motion/06-single-character-7s-STD-REJECTED.txt`](prompts/motion/06-single-character-7s-STD-REJECTED.txt)
   — **Sean named this as the file to work off.** Not because `std` was right (it was rejected),
   but because its four-block shape and its opening line are the foundation.
2. The `prompt-how-much` skill — the video half. Sean named it.
3. The `art-department` skill — Sean named it. Its MICRO-EXPAND discipline is the method for
   this session: *the design is the personality made visible.* We are applying that to **motion**.
4. [`prompts/_blocks.md`](prompts/_blocks.md) — the laws, including the ones written yesterday.

Working directory: `/Users/seanwinslow/Code-Brain/anima/briefs/2026-08-02-about-me-short`

---

## The film

A **~90-second animated short** for Sean's portfolio: a PM and four AI-mascot sidekicks in a
break-room HQ. An alarm fires, each sidekick builds a brilliant *wrong* solution, Sean steps
back, asks the user one question, and the same team ships the tiny right fix. Pencil-test
register, 1950s Goofy "How To" grammar.

Locked brief: [`00_studio_brief.md`](00_studio_brief.md) (amended 2026-08-31 — read the
amendment at its foot). 20-beat sheet: [`beats-v1.md`](beats-v1.md). Locked lines:
[`lines-v1.md`](lines-v1.md). Storyboard: [`M1-STORYBOARD.md`](M1-STORYBOARD.md).

**Movement 1 "Quiet Morning" is the current scope** — beats 1–3, ~15 seconds, seven setups.
Stripped of narration it becomes Anima's project-tile piece, so it is also the fallback
deliverable.

---

## Where we are in the order of work

    ground plan → elevations → rendered elevations → shot roughs → PLATES →
    CHARACTERS COMPOSITED → MOTION → timing

**Steps 1–6 are done and approved.** Step 7, motion, is where this session lives.
**Do not raise timing until every clip is approved** — that is a standing instruction.

### The approved stills — these are the start frames, do not regenerate them

All normalised to canonical cream and verified against their plates. **The four mascots face
the camera three-quarters front** — whole face, whole body — because Sean ruled *"I don't want
Seedance trying to invent what the other halves look like."*

| Setup | Start frame | Character |
|---|---|---|
| S02 | `normalised/S02-sean-composite-v1.png` | Sean, seated, back to camera, hands on the keyboard |
| S03 | `normalised/S03-claude-composite-frontal-v1.png` | Claude at the paper tower, NW corner |
| S04 | `normalised/S04-codex-composite-frontal-v1.png` | Codex at the server rack, SW corner |
| S05 | `normalised/S05-gemini-composite-frontal-v1.png` | Gemini at the moodboard, south wall |
| S06 | `normalised/S06-grok-composite-frontal-v1.png` | Grok at the dartboard, NE corner |
| S07 | `normalised/S07-plate-v2.png` | The CRT, screen dark. No character — the alarm is the movement |

Review console for all of it: <https://claude.ai/code/artifact/7c73caa6-b977-46dd-8ef5-fa1d36d1f2f4>

---

## THIS SESSION'S JOB, in Sean's words

> *"We should work on brainstorming the moves that each character makes based on their
> personalities. Each character will have their own unique action based on the personality of
> their character."*

So the work is, in order:

1. **Brainstorm the move, per character, from the personality.** This is the whole first half of
   the session and it happens *with Sean*, not before him. Artie's rule applies: **propose with
   a stated lean, Sean's eye decides, and lock nothing on your own judgment.** Push every move to
   a named specific — *"squares the stack, finds it already square, squares it again"* locks;
   *"tidies up"* does not.
2. **Write the prompt** for the agreed move, on the locked skeleton below.
3. **Generate, measure, look.** One character at a time. Sean wants to work through them together.

---

## WHY WE ARE REDOING THIS — two rejected clips, and the diagnosis

Both are Sean's calls and both are correct.

### Codex — `motion/ab-codex/armA.mp4`

> *"I thought the Codex output was a prompt test, not the final output."*

He is right, and the previous session overclaimed it as "the best clip this project has
produced." It is not a Movement 1 beat at all. Its action — frantic typing → peer at a blinking
light → arms overhead in triumph — is **beat 6, Codex's Movement 2 wrong-build.** Keep the clip
as a banked M2 asset; it is not the M1 beat and never was.

### Claude — `motion/m1-beat2/S03-claude-tidy-v1.mp4`

> *"The Claude mascot jumps up in slow motion, touches the paper stack, and slowly falls back
> to the ground."*

Exactly right, and the previous session under-called it as "airborne with no visible contact."
The real defect is **slow motion**. Three causes, all in the prompt, all avoidable:

1. **Damping words.** The prompt's closing block said *"unhurried timing, a slow ease into each
   pose, small held moments, the gentlest overshoot."* This is the mistake
   [`01-inscene-4s-TIMID-do-not-copy.txt`](prompts/motion/01-inscene-4s-TIMID-do-not-copy.txt)
   already recorded — *"light taps", "one small bounce", "feet planted" are DAMPING words. They
   dampen* — re-made with better manners. `prompt-how-much` says the same thing.
2. **One action stretched over seven seconds.** 04's three-part beat fills 7s with three distinct
   events. A single action given 7s gets spread across 7s, and spreading is slow motion.
3. **A vertical move.** Both failures involve a character leaving the floor. Seedance has no
   gravity model, and a jump is exactly where that shows: its readability lives entirely in its
   timing shape, so any uniform slowing turns it into moon gravity.

---

## THE LAWS FOR THIS SESSION

### 1. The register block is CONSTANT. Vary the ACTION, never the ENERGY.

Sean quoted this line and it is the foundation. It goes at the top of **every** character's
prompt, unchanged, forever:

> `1950s theatrical cartoon slapstick, hand-drawn colored-pencil pencil-test animation on cream paper, held on twos with visible line boil. Fixed camera, locked tripod, one continuous shot.`

**There is no "calm" register and no "quiet" register.** Movement 1's narration calls the room
*"a calm, well-organized workplace"* — that is the Goofy joke, narration against picture. The
picture is slapstick from frame one. The previous session tried to earn "calm" by slowing the
animation and got slow motion, which is the failure above.

**Calm is a SMALL ACTION AT FULL SNAP, not a big action slowed down.** Timing and spacing are
what sell weight; damping them destroys weight. Every character's closing block keeps the full
slapstick vocabulary:

> `Squash and stretch on every accent, smear frames through the fast arcs, snappy timing, elastic overshoot, comic energy.`

### 2. Three events, not one. Duration ÷ events sets the tempo.

At 7s, aim for **three distinct beats, roughly 2–2.5s each**. That is what 04 did and why it
moved. One event over 7s is the slow-motion trap. If a shorter clip is wanted, drop the duration
rather than the event count — 05 proved duration is the dial (7s → 4s cost 20% of the motion
energy) but the event count is what sets the *tempo*.

### 3. Keep them on the ground unless the gag is the air.

Both rejects left the floor. Prefer horizontal, grounded business. **Stage the action within the
character's own reach** — Claude does not need the top of a five-foot tower; the base of the
stack is at its own head height. Where a character must leave the ground, give the jump its
timing shape explicitly (fast up, a *short* hang, fast down) rather than describing it neutrally.

### 4. Positive locks, stated as CONSTANTS THROUGH TIME. Zero negation.

Seedance has **no negative-prompt support** — every negation is wasted tokens (01 wasted ~40% of
its prompt this way). State what IS true, in every frame.

The one thing the rejected Claude prompt got right, and it worked first roll:

> `Its face is exactly two small dark dot eyes and two short brows, the same two eyes and two brows in every frame.`

Compare the phrasing that **fails** — 04/06's *"Its face stays a pale chevron…"*, which describes
a rest state and loses to the beat, and Codex grew a mouth. The grounding lock that works has the
same shape: *"Its feet return to the floor on every landing."* **Write every lock as a per-frame
or per-event constant.**

Sean has ruled the Codex mouth is **fine and he likes it** — do not spend rolls chasing it. The
lesson here is about phrasing, not about that defect.

### 5. Never pass character references to `seedance_2_0`.

Measured 2026-08-31, A/B on Codex, same start frame and same prompt: passing turnaround views as
`image_references` **overrode the start frame's composition.** Arm B's *first frame* was already a
different shot — layout correlation to the start frame 0.273 vs arm A's 0.988, drift 19.3% vs
7.1%. On 2.0 they are subject-*presentation* references, not identity references, and they cost
the plate. Full record: [`motion/ab-codex/README.md`](motion/ab-codex/README.md).

If a reference is ever genuinely needed, `seedance_2_5`'s `omni_reference` mode is the one built
to separate reference-identity from start-frame composition (45.5 cr, different model, no
`fast`/`std` — nothing measured on 2.0 carries over).

---

## THE LOCKED SKELETON

Four blocks, in this order. Blocks 1 and 4 are constant across all five characters; blocks 2 and
3 are what this session writes.

```
[1 · REGISTER — verbatim, never edited]
1950s theatrical cartoon slapstick, hand-drawn colored-pencil pencil-test animation on cream
paper, held on twos with visible line boil. Fixed camera, locked tripod, one continuous shot.

[2 · THE MOVE — three events, vivid verbs, this character's personality made physical]
<~60-80 words. Name the character by its drawn description, not its name. Three beats separated
by full stops. Every verb concrete and fast.>

[3 · THE LOCKS — positive, per-frame, no negation]
<Its face is exactly ... the same ... in every frame.>
<Its feet return to the floor on every landing.>
<It stays <size> against <a named prop in this shot>, in every frame.>

[4 · VOCABULARY — verbatim, never edited]
Squash and stretch on every accent, smear frames through the fast arcs, snappy timing, elastic
overshoot, comic energy.
```

---

## RAW MATERIAL FOR THE BRAINSTORM

From [`character_seeds.yaml`](character_seeds.yaml) and [`beats-v1.md`](beats-v1.md). **These are
starting points for the session with Sean, not proposals to run.** Each character's Movement 1
move should plant its Movement 2 wrong-build without performing it yet.

| Character | Personality, verbatim from the seeds | M2 wrong-build it should plant | Its verb |
|---|---|---|---|
| **Claude** · terracotta cube | *"earnest, over-caveating, gentle voice"*; tidy reading-nook, squared stacks, sticky-flags, a well-watered plant | beat 5 — a 40-page sticky-flagged strategy doc, **still growing** | hedging · re-checking · never quite done |
| **Codex** · lavender cloud, `>_` face | *"terse build-monotone voice… short build statements"*; ship-it energy | beat 6 — silently rebuilds the whole checkout stack, ten thousand lines, **nobody asked** | executing · no wind-up, no flourish |
| **Gemini** · blue-purple star | *"bubbly option-overload voice… always offering one more option"*; *"reads sweet, moves fast"* | beat 7 — fifty gorgeous concepts taped over every surface | offering · one more, and one more |
| **Grok** · grey gremlin | *"feral edgelord voice, chaos energy played affectionate, never contemptuous"* | beat 8 — sledgehammers the checkout wall, builds a rocket | committing hard · missing completely · unbothered |
| **Sean** · seated, back to camera | *"cycle-1 'egging them on' energy vs post-step-back conductor calm — same character, two tempos"* | beat 4 — the wordless GO gesture | typing · the M1 tempo is the busy one |

**The comedy boundary is a guardrail, not a note:** Grok's caricature stays on the *affection*
side of the affection/snide line. Brilliant, only misaimed.

**Two staging facts worth using.** Grok's dartboard has every dart in the wall *around* it and
the board face is clean — the miss already happened, so his M1 move can be the next one. Gemini
is composited looking *down* at loose sketches on the floor at its feet, which is a real task and
gives a move somewhere to start.

---

## ROUTE — settled, do not re-derive

| Step | Setting |
|---|---|
| Model | `seedance_2_0` |
| Mode | **`fast`** — standing ruling. `std` fixes the face and drifts less but Sean: *"it stutters and looks broken."* |
| Duration | 7s (the dial: 4s costs ~20% motion energy) |
| Resolution | 720p · aspect 16:9 · `--generate_audio false` |
| Refs | `--start-image` **only**. No `--image` refs — see law 5 |
| Cost | **24.5 credits per clip.** Balance was ~4,850 at the end of the last session |

```bash
higgsfield generate create seedance_2_0 --prompt "$(cat p.txt)" \
  --start-image normalised/<setup>.png \
  --mode fast --duration 7 --resolution 720p --aspect_ratio 16:9 \
  --generate_audio false --json --wait --wait-timeout 20m
```

### The spend guard — added because it was needed

A `sed` error emptied a prompt file after `>` had truncated it, and **the CLI accepted `""` as
satisfying a required string** — 49 credits on two null clips. Always:

```bash
n=$(wc -c < prompt.txt); echo "$n"; [ "$n" -lt 400 ] && { echo ABORT; exit 1; }
```

…and confirm the prompt actually landed by reading `params.prompt` back out of the job JSON.

---

## MEASUREMENT — $0, run it on every clip

```bash
.venv/bin/python3 post/analyze_clip.py <x0,y0,x1,y1> clip.mp4     # motion energy, bg drift, travel
```

Plus the layout check that catches a re-camera, on a 160×90 reduction of frame 0 and the last
frame against the start image — **1.00 is an identical layout**. Reference numbers from clips
that have been looked at:

| Clip | layout f0 | layout last | drift | motion |
|---|---|---|---|---|
| Claude tidy (rejected — slow motion) | 0.985 | **0.987** | 9.7% | 1.11 |
| Codex arm A (M2 asset) | 0.988 | — | 7.1% | 1.21 |
| Codex arm B (refs — plate lost) | **0.273** | — | 19.3% | 6.91 |
| Empty-prompt control | — | — | **87.9%** | 13.49 |

**The metrics cannot see the defect Sean saw.** The rejected Claude clip has the *best* layout
hold ever measured on this project and it is still a bad clip, because slow motion is not a
number in this table. Measure to catch re-cameras and plate loss; **use the eye for everything
else, and put the clip in front of Sean rather than describing it.**

---

## WHAT GOOD LOOKS LIKE

A Movement 1 clip is finished when all of these are true:

- [ ] **It reads as that character and no other.** Someone who has not seen the film could match
      the clip to the personality line in the table above.
- [ ] **It has weight.** No floating, no moon gravity, no slow motion. Things accelerate and
      land. Feet hit the floor.
- [ ] **Three distinct events** land inside the 7 seconds, at full slapstick snap.
- [ ] **The plate holds.** Layout ≥ ~0.95 at frame 0 *and* at the last frame — it has to end where
      it started, because Movement 2 cuts back to this same corner.
- [ ] **Identity holds** — the face design is the one in the start frame, and the scale against
      its named prop does not grow.
- [ ] **It plants the Movement 2 wrong-build** without performing it.
- [ ] **Sean says so.** He is the gate. Every metric above has already been passed by a clip he
      rejected.

Then, and only then: assemble, and raise timing.

---

## STANDING LAWS FROM THE WHOLE PROJECT

| Law | Where it lives |
|---|---|
| **Normalise every frame in post** — `post/normalize_paper.py` → `normalised/`, the working set. Canonical cream `#f5e8d1` ±8 | [`environment-style.md`](environment-style.md) |
| **One source of truth** — `WALLS` in `room-bible/make_room_bible.py` is the only description of the set | [`room-bible/README.md`](room-bible/README.md) |
| **The still holds a rest pose; Seedance supplies the movement** — held is fine, mid-action is not | [`prompts/_blocks.md`](prompts/_blocks.md) |
| **The look lives in post** — every plate and composite generates CLEAN | FIRST LICKS DR #41 |
| **Preserve superseded work** — move to `old/`, never overwrite | throughout |
| **Anchor scale to a TALL named prop**, never a percentage of frame | the scale law in `_blocks.md` |
| **Body to camera, eyeline to the prop** — absorbed in its own task, never addressing the lens | the facing law in `_blocks.md` |

---

## OPEN, and none of it blocks the motion work

1. **S07's corner seam sits at 93% across** — geometrically correct, but it reads as an edge
   detail. Moving it inward is a one-line camera change in `make_shot_roughs.py`, a free
   re-render, then one plate roll.
2. **Claude's composite is 0.84 of intended scale**, the loosest of the four. One roll to fix.
3. **The S02 confetti cannon reads as a telescope.** One surgical edit; only matters from beat 9.
4. **S02 needs its Movement 3 state** — a chat box on the centre monitor with the faceless USER
   in it. Not a Movement 1 frame.
5. **Title-card typography** (S01) — the one setup Seedance never touches.
6. **The matte-and-relay drift test** is still unrun: matte the character out of the clip and
   re-lay it on the pristine plate, which would make plate drift structurally impossible.
7. **The stopwatch table-read** ([#206](https://github.com/seanwinslow28/code-brain/issues/206))
   — $0, Sean-only, and it settles whether beat 2's 8 seconds can hold five setups.

---

## WORKING DISCIPLINE

Sean directs; **propose with a stated lean and let his eye decide.** Measure rather than assert —
and remember that on this project the eye has twice caught what the metrics could not, so a good
number is never a verdict. **Show him the clip.**

When a ruling reverses an earlier one, record why, keep the superseded artifact, and say plainly
what it costs. Instrument as you go: wall-clock, rolls per shot, credits.

**Two misses from the last session, recorded so they are not repeated:** an assistant called a
route-test clip "the best clip this project has produced" when it was neither final nor the right
beat, and then re-made the documented `01` damping mistake while believing it was designing a
quiet register. Both were caught by Sean, not by the instrumentation. Read the failure files in
`prompts/motion/` before writing a new one — **the ones marked REJECTED and DO-NOT-COPY are the
most useful files in the directory.**
