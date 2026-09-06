# CONTINUATION — Movement 2, through a creative-director lens

**Start this session by invoking the skill:**

```
/Users/seanwinslow/Code-Brain/anima/.claude/skills/creative-director/SKILL.md
```

Sean asked for it by name. Its job here: **review the remaining Movement 2 beats and work out how
to explore the room and stage each character's action** — not to plan a pipeline that already
exists.

### The skill was rewritten on 2026-09-03 — invoke it and let it work

An earlier version of this prompt warned that the skill's tool references were from a
different pipeline and had to be mentally translated. **That is no longer true.** The skill
is now project-neutral: it carries no fixed pipeline, register, naming convention or failure
codes, and its **Phase 0** does the grounding for you — it reads this brief, the storyboard,
[`prompts/_blocks.md`](prompts/_blocks.md) and the rejected-prompt archive, then states back
the register, the route, the per-unit cost and the standing laws before proposing anything.

So: **invoke it and let Phase 0 run.** Do not pre-translate anything, and do not re-answer
the discovery interview from zero — five of its six North Star points are already locked in
[`00_studio_brief.md`](00_studio_brief.md), [`beats-v1.md`](beats-v1.md) and
[`lines-v1.md`](lines-v1.md), and Phase 0 is built to find them.

Three of the laws listed further down now also exist as **visual guides** the skill loads
when it critiques — `rest-pose-vs-mid-action.png`, `scale-anchor-tall-object.png` and
`smear-from-repeated-motion.png`, at `.claude/skills/creative-director/references/visual-guides/`.
They were built from this project's own measured failures, so a critique that cites them is
citing evidence rather than opinion.

Then read, in order:

1. [`M1-STORYBOARD.md`](M1-STORYBOARD.md) — production state, ruled settings, standing laws
2. [`prompts/_blocks.md`](prompts/_blocks.md) — every law, including the two amended 2026-09-01
3. [`room-bible/README.md`](room-bible/README.md) + `make_room_bible.py`'s docstring
4. [`beats-v1.md`](beats-v1.md) — beats 4–20
5. `prompts/motion/` — the REJECTED and DO-NOT-COPY files are the most useful in the directory
6. The production map: <https://claude.ai/code/artifact/f73f288d-a0e5-4048-9b58-545e892e67d8>
   **Current as of 2026-09-03** — revised for ruling 1, so beats 5, 6 and 7 already carry a
   `Re-decide` status and the new reaction beat is on the board as 3½.

Working directory: `/Users/seanwinslow/Code-Brain/anima/briefs/2026-08-02-about-me-short`

---

## The film

A **~90-second animated short** for Sean's portfolio: a PM and four AI-mascot sidekicks in a
break-room HQ. An alarm fires, each sidekick builds a brilliant *wrong* solution, Sean steps
back, asks the user one question, and the same team ships the tiny right fix. Pencil-test
register, 1950s Goofy "How To" grammar. Runtime target 1:27, ceiling 2:00.

**Movement 1 (beats 1–3) is shot, approved and assembled in CapCut.** Seven clips in
[`_LOCKED-M1/`](_LOCKED-M1/) with a README. This session is **Movement 2, beats 4–10**.

---

## SEAN'S THREE NEW RULINGS — 2026-09-02, and they are the reason this session exists

### 1. No cutting back to the same angle without chaos

> *"I'd like to redo beat 6 because I don't want to cut back to each character in the same
> angle/frame. If it is in the same angle/frame, we need to have completely chaotic motion with
> some added mess into the frame."*

This generalises past beat 6. **Beats 5, 6, 7 and 8 all revisit corners the audience met in
beat 2**, and the earlier plan — reuse all seven setups, add the wrong-build by surgical edit —
is now overruled. It also supersedes an earlier ruling of his that only half-said this:

> *"We can use the same angles in some scenes, but I don't want this short to just be cuts into
> the same corners throughout. We'll get creative with what we can do in this room."*

**The consequence to carry into the routes:** each of the four wrong-build beats needs an
explicit decision — **a new camera on that corner, or the same camera with the frame visibly
wrecked and the motion genuinely chaotic.** Probably a mix. That is the central creative
question of this session.

**And it puts both "banked" clips back in play.** The production map called beats 6 and 7 free
because two approved clips already exist:

| clip | beat | why it is now conditional |
|---|---|---|
| `motion/ab-codex/armA.mp4` | 6 · Codex | Same S04 camera as the locked M1 Codex clip. Sean has named this one for redo. |
| `motion/m1-beat2/S05-gemini-one-more-v1.mp4` | 7 · Gemini | Same S05 camera as the locked M1 Gemini clip. Not yet ruled on, but it falls under the same rule — **raise it.** |

Neither is wasted; both are good clips. The question is whether the same framing twice is a cut
the film can afford, and Sean's instinct is that it is not.

### 2. A new beat before beat 4 — the room reacts, from the CRT's point of view

> *"I also think we might need a beat before beat 4 'the wordless go'. I was thinking a super
> wide angle/birds eye shot from the CRT's POV of the whole room and everyone turns and enters
> into frame at various scales depending on how close they are to the CRT, but we can explore
> what to do there. I feel like we should have a reaction from everyone and then we go to the
> wordless go."*

**This is an invitation to explore, not a spec.** Bring routes.

**Flag this honestly, because it reverses a documented cut:** M1-STORYBOARD records *"There is
no establishing wide at all — Sean cut it 2026-08-30,"* and the reasons were real (the cut wide
failed on facing, and the busiest wall in the room produced the worst measured drift). But what
he is proposing is **not** the shot he cut. That one was a neutral establishing wide. This is a
**motivated POV** — the alarm's own view of the room, at the exact moment the room turns to look
back at it. Different shot, different job, and it earns the width. Say so, and note the drift
risk it inherits.

The staging idea worth protecting: **scale as distance.** Characters nearer the CRT enter huge,
characters further away enter small. That is a real depth cue, it is free in a single frame, and
it is the sort of thing this pencil register does well.

### 3. He cannot judge this from prose

> *"it's tough without seeing the images to see how they all come together."*

**So this session's output is pictures, not paragraphs.** The $0 rough machinery below exists
exactly for this. Rough every candidate angle before proposing it, put the roughs in front of
him, and let his eye choose. Do not write him a list of camera options in words.

---

## THE TWO THINGS THAT MAKE THIS AFFORDABLE

### The room bible already models Movement 2

`room-bible/make_room_bible.py` defines three room states, and **the Movement-2 additions are
already positioned in the one-source-of-truth `WALLS` table, drawn in red:**

```
A QUIET  M1 beats 1-3   the room as drawn
B CHAOS  M2 beats 5-9   code wall lit, concepts everywhere, THE HOLE at the NE
                        corner with the rocket leaning out, the bell rung hollow
C AFTER  M3             still wrecked, but calm
```

Two fixtures are already placed with real coordinates:

- **`THE CODE WALL`** — west wall, `x 13.1–15.6`, height 2.6, sill 4.2 — *"M2 beat 6 · scrolling code"*
- **`THE HOLE`** — east wall, `x 0.0–2.0`, height 6.4, sill 0 — *"M2 beat 8 · the rocket leans out"*

**Beat 8's hole is not an open design question. Its position is decided.** That was the beat the
production map called the riskiest, and it is substantially de-risked — what remains is drawing
it, not deciding where it goes.

### New camera angles cost $0 to rough

`room-bible/make_shot_roughs.py` solves any camera against the room. Its own docstring:
*"Re-cameraing a shot is a one-line edit. Change the yaw, re-run, $0."*

The `SHOTS` dict takes:

```python
"S07": dict(pos=(15.0, 12.0), pitch=1, eye=5.2, fill=0.74,
            on=["BINDER SHELVING", "credenza", "THE CRT"],
            title="THE CRT ALARM"),
```

`pos` = floor position in feet · `eye` = camera height · `pitch` = degrees · `fill` = how much of
frame the named subjects occupy · `on` = the fixtures to aim at. **Room is 26′ × 18′ × 10′, eye
level 5′6″ is the horizon every plate sits on, CRT sill is 6′6″.**

**Add entries, re-run, look.** That is how to explore the room for free, and it is how to answer
ruling 2 with a picture instead of a paragraph.

A starting guess for the CRT-POV bird's-eye, to be solved rather than trusted: `pos` near the
CRT on the east wall (roughly `(21.5, 9.6)`), `eye` around 7.0 (above the 6′6″ sill), a strongly
negative `pitch`, a low `fill` so the whole room reads, and `on` listing every corner.

**The rough is also the plate's camera reference.** Per `_blocks.md`, `gpt_image_2` will not
re-camera from an edit — every new angle is a reconstruction with role-split refs: an existing
plate as fixture/style bible with an explicit *"do NOT copy its camera,"* plus the rough as the
camera. This is the pattern that made all seven M1 plates and today's S08 closeup work.

---

## WHAT IS LOCKED — do not re-litigate any of it

| Asset | State |
|---|---|
| Movement 1, seven clips | **Locked**, in `_LOCKED-M1/`, assembled in CapCut |
| S02–S07 plates (rev 2) + composites | **Locked**, in `plates/rev2/` and `normalised/` |
| **S08 · CRT closeup plate** | **Locked** — `plates/rev2/S08-crt-closeup-v1.png`, screen dark |
| **The USER, grey** | **Locked** — design `refs/user-looktest/D-filled-grey.png`, turnaround `F-turnaround.png` |
| **The USER, green + grin + thumbs-up** | **Locked** — design `H-green-smile.png`, turnaround `I-turnaround-green.png` |
| **The USER on the CRT, both states** | **Locked** — `S08-grey-v2.png` and `S08-green-v2.png` |

**The USER design, settled 2026-09-02:** a solid grey figure with the animator's construction
lines left on top — joint circles, a crosshair on the blank head, a searching contour gone over
two or three times — and `USER` across the chest in much darker graphite than the fill. It is
the one character the animator never finished drawing. Beat 18 finishes it: green, one enormous
grin on an otherwise blank head, thumbs up, action lines. **The fill is load-bearing** — the
open-line version was the better idea and it dissolved at 32px, which is the size a chat avatar
plays at. Full record in `prompts/user-design/`.

**Beat 18 is one clip from done:** both keyframes exist on the same plate, same framing,
differing only in the figure — exactly the two-keyframe condition, same arm-B route as the S07
alarm.

---

## THE STANDING LAWS — all of them earned, several the hard way

### Motion

1. **The register block and the vocabulary block are CONSTANT.** Verbatim at the top and bottom
   of every motion prompt, never edited per beat. Vary the action, never the energy.
   **There is no "calm" register.** Calm is a small action at full snap.
2. **Fill the seven seconds** (Sean, 09-01): *"the timing comes down in the edit, not the
   generations."* Three events is a floor, not a target. A **loop** is the ideal shape — it
   cannot degenerate into one action stretched over 7s, which is what slow motion is.
3. **The feet law is REPEALED** (Sean, 09-01). Jumps are fine. The rejected clip's defect was
   timing shape, not altitude — and the approved Codex clip already contains a jump. What
   replaces it: **speed verbs on every vertical** (springs, snaps, drops, slams) and a **landing
   constant** stated through time.
4. **Zero negation.** Seedance has no negative-prompt support; every negation is wasted tokens.
5. **Locks are per-frame constants, never rest states.** *"Its face is exactly two dot eyes and
   two brows, the same two eyes and two brows in every frame"* holds. *"Its face stays…"* loses.
6. **Never pass character references to `seedance_2_0`.** Measured: refs overrode the start
   frame's composition at frame zero — layout 0.273 vs 0.988. They are subject-*presentation*
   references, not identity references.
7. **Deleting an EVENT moves a beat earlier; shortening a sentence does not.** Measured on S07:
   compressing wording bought 0.5s, deleting the white flare bought 1.5s. And **a described hold
   is itself an event** — write it as a state.
8. **`seedance_2_0` does not honour an absolute time cue.** Negative finding, measured. Do not
   buy it again.
9. **A one-way translation is not smearable from the prompt.** Two independent levers failed.
   Smears come from repeated or rotational action.

### Stills

10. **The still holds a REST pose. Seedance supplies the movement.** Held positions are fine
    (hands on a keyboard); instants are not (mid-throw, mid-reach).
11. **¾ FRONT facing** — whole face, whole body. *"I don't want Seedance trying to invent what
    the other halves look like."* Body to camera, eyeline to the prop.
12. **The scale law: anchor to a TALL prop and state a ceiling.** A knee-high anchor reads as a
    floor, not a ceiling, and came back ~2× twice. Shout the direction, give a human yardstick,
    ratio it against a tall fixture, negate the failure.
13. **A FRAMING clause silently deletes whatever falls outside the frame it names** (found
    2026-09-02). *"Head and shoulders only"* did not fail to include the raised arm — it
    instructed the model to remove it. When a pose lives in the limbs, write the framing clause
    around the pose.
14. **The look lives in post.** Every plate and composite generates CLEAN.
15. **Normalise every frame** — `post/normalize_paper.py` → `normalised/`, the working set.
    Canonical cream `#f5e8d1` ±8.
16. **Preserve superseded work.** Move to `old/`, never overwrite.

### NSFW wording hazard — do not paraphrase Grok

The first S06 prompt was refused `status: nsfw` for *"grey gremlin shape, bat ears, red eyes,
fanged grin."* The wording on record as passing: **"a round grey cartoon creature with big
pointed ears and a wide friendly cartoon grin."** Reuse verbatim. It is also the comedy-boundary
guardrail — the caricature stays on the affection side of the affection/snide line.

---

## ROUTE + SETTINGS — settled, do not re-derive

| Step | Setting |
|---|---|
| Stills | `gpt_image_2`, quality `high`, resolution `2k`, aspect per shot. **8.5 cr** |
| Motion | `seedance_2_0`, mode **`fast`**, **7s**, 720p, 16:9, `--generate_audio false`. **24.5 cr** |
| Two-keyframe | `--start-image` + `--end-image`. Ratified on S07; the route for beat 18 |
| Refs | Role-split, always. Never character refs to Seedance |
| **Balance** | **4,370 credits** at session end 2026-09-02 |

Runners, all with the byte guard built in:

```
motion/gen_image.sh      <prompt> <ratio> <out.json>              # from scratch
motion/gen_image_ref.sh  <prompt> <ref> <ratio> <out.json>        # one design ref
motion/composite.sh      <prompt> <char> <scene> <out.json>       # character into scene
motion/composite2.sh     <prompt> <bible> <rough> <out.json>      # re-angle reconstruction
motion/generate.sh       <prompt> <start> <out.json>              # motion, one keyframe
motion/generate2kf.sh    <prompt> <start> <end> <out.json>        # motion, two keyframes
```

**The spend guard is not optional.** A `sed` error once emptied a prompt file and the CLI
accepted `""` as satisfying a required string — 49 credits on two null clips. Every runner
strips the `#` comment header, refuses to spend under 400 bytes, and the job JSON's
`params.prompt` should be read back to confirm the prompt landed.

---

## MEASUREMENT — $0, and it is a tripwire, never a verdict

```
post/layout_hold.py  <start.png> <clip.mp4>        # re-camera / plate loss. 1.00 = identical
post/analyze_clip.py <box> <clip.mp4>              # motion energy, bg drift, travel
post/beat_times.py   <screenbox> <clip.mp4>        # when things happen, at 24fps
post/verify_edit.py  <plate> <edit> [...]          # FFT phase + edge keep. floors: 0.15 / 0.7
post/make_closeup.py <src> <cx,cy,w,h> <out>       # crop a push-in target or a camera rough
post/normalize_paper.py                            # → normalised/, the working set
```

**Read this before trusting any number.** The rejected slow-motion Claude clip holds this
project's *best ever* layout hold (0.990/0.991) and is still a bad clip. Sean's eye has caught
what the metrics could not at least four times now. Measure to catch re-cameras and plate loss.
**Use the eye for everything else, and put the picture in front of him rather than describing
it.** Two measurement traps found on 2026-09-02, both worth remembering: a camera-move detector
measured over the whole frame is tripped by a screen flash, and a correlation threshold loose
enough to catch a push-in is also tripped by a hopping mug.

---

## OPEN, and none of it blocks this session

1. **The green-state turnaround has a mirrored thumbs-up** in its two back views — seen from
   behind, its right hand should appear on the viewer's right. One roll.
2. **S07's screen never blinks** — three prompt phrasings failed; it is an opacity keyframe in
   post. Same pass should pull the screen from pale blue back to cream.
3. **The confetti cannon on S02 reads as a telescope.** Beat 9 is the first beat that needs it.
4. **Beat 14's replay is an asset class nobody has designed** — a drawn checkout page with a
   cursor circling, in pencil-test register, carrying the film's only hard legibility floor.
5. **Beat 12 needs Sean's face in this room**, which has never been drawn — every S02 asset is
   the back of his head. It is the film's protected beat: held past comfort, no gag.
6. **A monitor closeup (S09)** is probably owed for beat 13's typed question, by the same
   argument that earned S08 its closeup.
7. **The stopwatch table-read** ([#206](https://github.com/seanwinslow28/code-brain/issues/206))
   — $0, Sean-only, still unrun. Defused but not closed by the timing-in-the-edit ruling.
8. **The matte-and-relay drift test** is still unrun. The two-keyframe route did **not** replace
   it — S07 measured that two keyframes cost some camera hold rather than buying it.

---

## WORKING DISCIPLINE

**Sean directs. Propose with a stated lean and let his eye decide. Lock nothing on your own
judgment.** Push every proposal to a named specific — *"squares the stack, finds it already
square, squares it again"* locks; *"tidies up"* does not.

**Show him the picture.** He has said plainly he cannot judge staging from prose. Rough it, or
generate it cheap, before asking.

**Instrument as you go** — credits per roll against the running balance, rolls per shot,
wall-clock. Announce cost before spending it.

**When a ruling reverses an earlier one, record why, keep the superseded artifact, and say
plainly what it costs.** This project's prompt files are its memory; every one carries its own
result, metrics and diagnosis in a comment header, and the rejected ones are the most useful
files in the directory.

**Report failure straight.** Two clips have been overclaimed in this project's history and both
were caught by Sean, not by instrumentation. If a roll comes back worse, say so in the first
sentence and say why before proposing the next move.
