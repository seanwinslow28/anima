# CONTINUATION — Movement 3, wave 3: beats 11–20, through a 2D animation director's eye

**Start this session by invoking the skill:**

```
/Users/seanwinslow/Code-Brain/anima/.claude/skills/creative-director/SKILL.md
```

Sean asked for it by name. Its job here: **help him map out and then execute Movement 3 — the step
back, the question, the replay, the pit stop, the earned ship, the USER turning green, and the
sting — with a 2D animation director's creative taste and timing.** Not to re-plan the pipeline,
not to re-open anything ruled below, not to re-run the interview. Let **Phase 0** run: it reads
this brief, the tracker, [`prompts/_blocks.md`](prompts/_blocks.md) (fourteen wave-2 laws at the
bottom, all paid for) and the rejected-prompt archive, then states back the register, the route,
the per-unit cost and the standing laws before proposing anything. Then **Phase 2**: for each
open question below, 2–3 routes with a named specific, a cost in credits, and a stated lean —
and **show it before asking for a decision** (rough it at $0, crop it, roll a look-test) because
Sean has said plainly he cannot judge staging from prose.

The visual guides at `.claude/skills/creative-director/references/visual-guides/` are the
calibration. This movement leans on `anticipation-action-settle.png` (every pit-stop micro-task
is one whole beat), `eye-lead-head-turn.png` and `rest-pose-vs-mid-action.png` (beat 12 is a
held face), `staging-silhouette-test.png` (the sigh reads in silhouette or not at all), and
`smear-from-repeated-motion.png` (the pit stop's speed). Load them before critiquing a clip.

Then read, in order:

1. [`M1-STORYBOARD.md`](M1-STORYBOARD.md) — the Movement 2 tables (wave 2, rounds 1 and 2) are the
   nearest precedent for everything below: how a beat became plate → start frame → clip, what
   each cost, what Sean said
2. [`_LOCKED-M2/README.md`](_LOCKED-M2/README.md) — Movement 2 is **fully locked, 08–15**
3. [`prompts/_blocks.md`](prompts/_blocks.md) — every law, especially **§ Wave 2 findings 1–14**
4. `prompts/motion/25–38` — the wave-2 prompts; the headers carry the diagnoses. `34` (the
   chair spin that invented Sean's face) and `38` (the whirl that left the floor) are the most
   useful for this movement
5. [`CONTINUATION-2026-09-05-wave-2-review.md`](CONTINUATION-2026-09-05-wave-2-review.md) — the
   surviving open items, at the bottom
6. [`beats-v1.md`](beats-v1.md) § Movement 3 and [`lines-v1.md`](lines-v1.md) § PICKS — the beats,
   the two locked lines, the timing floors

Working directory: `/Users/seanwinslow/Code-Brain/anima/briefs/2026-08-02-about-me-short`

**Git, at the start:** `main` is clean at the squash of #122 (`a5ddbef`, everything through the
Movement 2 lock). The false-divergence trap in the project manual was hit and cleared on
2026-09-05 evening (local main reset to origin by content check; branch retired). **Branch first**
for this wave's PR (`about-me-short/m3-wave-3`), commit the record and the media as separate
commits (the media trail was ~1.3 GB last time; keep it droppable), and expect Sean to
squash-merge. Unrelated uncommitted edits under `briefs/2026-07-02-grandmaster/` and two skill
folders are not this project's — leave them out of the PR.

---

## The film, where it stands

A **~90-second animated short** for Sean's portfolio: a PM and four AI-mascot sidekicks in a
break-room HQ. Pencil-test register, 1950s Goofy "How To" grammar — **the narrator is deadpan and
the picture is the joke.** Runtime target 1:27, ceiling 2:00. **Movements 1 and 2 (beats 1–10)
are locked** in `_LOCKED-M1/` (01–07) and `_LOCKED-M2/` (08–15). This session is **Movement 3,
beats 11–20 — the last ten, ~37 seconds, the ones the whole film has been building to.**

The emotional engine, from the brief, is the thing to protect: *judgement is not being above the
chaos — it's the practiced act of stepping back out of it.* Movement 2 was loud on purpose.
Movement 3 is where the narrator and the picture finally agree, and it has the film's only
quiet beat, its only spoken line, and its only hard legibility floor.

---

## WHAT IS LOCKED — do not re-litigate any of it

| Asset | State |
|---|---|
| Beats 1–10, fifteen clips | **Locked**, `_LOCKED-M1/` + `_LOCKED-M2/`, each with its start (and end) frame |
| **The question, Sean's only line** | **Locked (lines-v1):** *"Can you show me what happened the last time you tried to check out?"* |
| **The button, the narrator's last line** | **Locked:** *"Which brings us back to where every problem begins: a quiet—"* — the alarm cuts the word; smash to black, zero linger; the caption dies on the em-dash |
| **The USER, grey and green** | **Locked** — `refs/user-looktest/S08-grey-v2.png` and `S08-green-v2.png`: the same S08 closeup plate, the same framing, the figure differing only in colour. **Beat 18 is one two-keyframe roll away** |
| **S08 · the CRT closeup** | **Locked** — `normalised/S08-crt-closeup-v1.png` (dark) and `normalised/S08-alarm2-v1.png` (PROBLEM (STILL!)). The screen edits for beats 14, 17 and 20 land on the dark one |
| **S02 · Sean's station** | **Locked** — `normalised/S02-cannon-fix-v1.png` (the redesigned cannon) is beat 17's start frame: beat 9's twin fires clean from the same frame |
| **S10 · Sean from the room** | **Locked** camera `B4-A` (mascot height, tipped up); `normalised/S10-sean-composite-v2.png` has his calm face, eyes down. Beat 12's new pose is a new composite on the same plate |
| **The wrecked NE corner** | **Locked** — `_LOCKED-M2/13_beat8_S06B_end-frame.png` is **the NE corner's bible for Movement 3 (DR #20)**. Every M3 angle on that wall inherits it |
| **Beat 12's gesture** | **Locked in the seeds:** chair turned away from the monitors to face camera, eyes closed, deep breath, **both palms pressed gently downward at chest height** — small, bent elbows. The raised-arm pose was retired for silhouette risk |
| **Sean's acting scale** | **Ruling 6, wave 2:** a leader's GO is a look, a breath, a nod, one small gesture. Beat 12 is the same restraint, longer. Beat 17's joy is *genuine* and still small |
| **Route and settings** | `gpt_image_2` 2k high (8.5 cr) · `seedance_2_0` fast 7s 720p (24.5 cr) · two-keyframe via `motion/generate2kf.sh` · single characters on the CLI, ensembles → Sean's web-app kit |

---

## THE RULINGS THAT SHAPE MOVEMENT 3 — carried forward, not re-opened

1. **The angle budget (raised in wave 2, now due).** Each corner is visited three times: M1 intro
   (original camera), M2 wrong-build (new camera), M3 sigh + pit stop. Sean's rule allows a
   same-angle return only when the frame is visibly wrecked and the motion is chaotic. **So
   M3's corner returns should be the ORIGINAL M1 cameras (S03–S06) with the wreck dressed in** —
   the "what have we done" reveal in the framing the audience knows. Room state **C = state B,
   calm** ("still wrecked, but calm" — `room-bible/make_room_bible.py`). Beat 8's breach is the
   first of those four plates and already exists; the other three (the canyon in the S03 frame,
   the popped screen in the S04 frame, the fifty in the S05 frame) are edits of the locked M1
   plates — the wreck-as-edit route proved on beat 8 (law 1).
2. **Sean asks the question at his computer, not at a door** (Sean, 2026-08-31 — "fits better
   with the theme of no dialogue and just VO, music, and sound effects"). Beat 13 plays at S02.
   **The unresolved half:** the brief's non-negotiable says *"the Sean character speaks exactly
   once — the question."* If it is typed, he never speaks aloud. The tracker has carried
   "confirm or override" since 08-31. **Settle it first — it decides beat 13's assets.**
3. **A monitor closeup for beat 13 — S11 — is owed** by the same argument that earned S08: the
   question has to be legible, and the centre monitor on the S02 wide is small. Built like S08:
   the S02 wide as fixture bible, a `post/make_closeup.py` crop as the camera rough.
4. **The replay is an asset class nobody has designed.** A pencil-drawn checkout page with a
   cursor that circles and never finds the buy button. Design it before buying a roll of it.
5. **The blink is post. The red flood is post. The shake is post.** Three phrasings failed to
   make S07 blink; beat 10's set-rattle was the model's own jolt. Beat 20's sting is a post job
   on a still unless a clip earns its 24.5.
6. **Two keyframes whenever the SET changes or a prop has to APPEAR** (law 10). Beat 8 did the
   whole demolition that way; beat 6's screen popped out that way. Beat 18 (grey → green) and
   beat 17 (falling graph → rocketing graph) are the same shape.
7. **The facing law applies to every rotation** (law 13). Beat 9 v3's chair spin turned Sean to
   the lens and the model invented his face. Beat 12 must start from a still where his face is
   already visible and eyes are already closed; the swivel finishes in the clip, it does not
   begin from his back.
8. **Deleting an event beats rephrasing a constant** (S07, S10). The closed-mouth constant does
   not survive a breath on Sean's face — two phrasings failed. Beat 12's breath is the beat, so
   plan for it: shoulders-only, eyes closed, or let post breathe the still.

---

## THE REMAINING BEATS — 11 through 20, and the director's question each one asks

| Beat | Picture (beats-v1) | Setup | What has to exist | First-roll cost | The director's question |
|---|---|---|---|---|---|
| **11** record scratch, 2s | The chaos dead-stops mid-frame; move → hold | *open* | Nothing, if the freeze is the last frame of beat 10 or 9. **Or** one plate: the S09 CRT-POV wide re-dressed to state B (canyon, screen, fifty, hole in one frame — the sum of the chaos, frozen) + the five figures (Sean's web-app kit) | 0 — or 8.5 + kit | **What is on screen when the needle scratches?** A freeze on Sean's arms-up back (beat 9's tail), on the alarm closeup, or the one wide where all four wrong-builds are visible at once. The wide is the 2D-director answer and it is also a candidate for beat 15's sigh |
| **12** THE SWIVEL, 4s, **protected** | Chair turned away from the monitors, eyes closed, deep breath, palms down. Held 2–3s past comfort. No gag | S10 | One composite: Sean seated facing us on the S10 plate, **eyes closed, palms pressed down at chest height** — a held pose, so the rest-pose law is satisfied by construction. One clip | 8.5 + 24.5 | **How much moves?** Lean: the chair finishes its last few degrees of turn, one slow shoulder breath, then stillness — and the "past comfort" is the cut holding the last frame. Watch the mouth (law 3); if it opens, delete the breath and let post breathe the still |
| **13** the question, 4s | Typed in a chat box on the centre screen; the grey USER is the avatar | S02 + **S11** (new) | S11 plate (8.5) → chat-box edit with the grey USER avatar and the locked question, legible (8.5; the one place the film needs a full sentence of text — the S07/S08 edits prove caps land; test a sentence) → a typing clip on S02 (his back, the coffee-clip precedent) and either a two-keyframe reveal on S11 or a post typewriter reveal on the still | 17 + 24.5 (+24.5) | **Typed or spoken** (ruling 2). Then: does the text appear by keyframes or by post? Post is exact and $0; a clip gives the room's flicker |
| **14** THE REPLAY, 6s, **floor 5–6s** | A screen recording on the big TV: cursor circling, never finding the buy button. The room watches, still | S08 | A designed checkout page (pencil, on cream: product, price, clutter, the buy button absent or hidden) as an S08 screen edit (8.5) → **the cursor as a post overlay** (a sprite on a path: exact, loopable, $0) — or a Seedance clip with the UI as a plate-loss risk | 8.5 (+24.5) | **Design the page first** — what does "can't find the buy button" look like in one drawing? Lean: post moves the cursor; the model has never had to hold a UI |
| **15** the cast sighs, 3s | Everyone deflates at once; the fix is comically small | S03–S06 **state C** | Three new wrecked-corner plates as edits of the locked M1 plates (canyon / screen / fifty; the NE breach exists) → four composites (each mascot at rest in its wrecked corner, ¾ front) → four short clips, cut together | 25.5 + 34 + 98 | **Four cuts or one wide?** The cuts pay off the M1 introductions and satisfy the angle rule by dressing; the S09 state-B wide (beat 11's candidate) would do it in one frame via the web-app kit. Lean: the four corners — they double for beat 16 |
| **16** THE PIT STOP, **≤5s hard** | Codex one line · Gemini makes it pretty · Claude confirmation copy · Grok demolishes the old button. Flawless, tiny, F1 | the same four state-C composites | Four clips from the same start frames as 15 — one micro-task each, full snap, one whole acting beat per clip (anticipation / action / settle), the cut takes ~1s of each | 98 | **What is "the old button"?** A named prop for Grok to demolish (a big drawn BUY button? the wrecked wall's rocket?). And: the five-second ceiling is an edit constraint, but each clip must carry a complete beat in its first two seconds — say so in the prompt |
| **17** the earned SHIP IT, 4s | The graph rockets. Bell full swing, clean cannon — beat 9's twin | S08 + S02 | S08 screen edit: the graph rocketing (8.5) + a two-keyframe clip (falling → rocketing, 24.5); the S02 clip from `S02-cannon-fix-v1.png`: full swing, a huge clean burst, Sean's genuine small joy (24.5) | 8.5 + 49 | **Same frame, opposite result** — write beat 9's prompt with the props answering true. Sean's joy at the GO's scale |
| **18** the USER colorizes, 4s | Grey becomes green, beaming, thumbs up, faceless | S08 | **One two-keyframe clip** from the two locked stills | 24.5 | The cheapest, surest beat on the board and the emotional payoff — **roll it first** (it also proves colour-change by keyframes). The mirrored thumbs-up in the back views is the one open nit |
| **19** THE BUTTON, 4s | The line over the green smile | — | Nothing — a hold on beat 18's last frame while the VO runs | 0 | Post |
| **20** the sting, ~1s | The alarm cuts the word; smash to black, instant | S08 | The alarm screen on the closeup — which design? — held for frames, red flood, black | 0 – 8.5 | **PROBLEM! or PROBLEM (STILL!)?** Lean: PROBLEM! — the film's last image rhymes with its first, the loop restarting. A still + post, no clip |

**Rough total for the wave:** ~430–520 credits at first-roll rates; ~650 with the re-rolls the
last two waves needed. **Balance 3,232.5** (measured 2026-09-05 20:00) — confirm at session
start with `higgsfield account status`.

### The four questions to settle before spending — with leans, so Sean can just say yes or no

1. **Typed or spoken** (beat 13). Lean: typed, per Sean's 08-31 ruling — and then the brief's
   "speaks exactly once" is satisfied in *text*, which is also mute-parity's preference.
2. **What freezes at the record scratch** (beat 11). Lean: the S09 wide re-dressed to state B —
   all four wrong-builds in one frame, dead still — because it is the only shot that shows the
   sum of the chaos, and it reuses a locked camera under the wrecked-frame exception.
3. **"The old button"** (beat 16). Needs a named prop. Lean: a big pencil-drawn BUY button,
   person-sized, that Grok reduces to splinters with the hammer already in his hands.
4. **The third alarm's text** (beat 20). Lean: PROBLEM!.

---

## THE ORDER OF WORK — a 30 / 60 / 90 for the wave

**30% — Rough.** Roll **beat 18** first: two locked keyframes, one 24.5 clip, the emotional
payoff, and it proves a colour change by keyframes on this route. Then **beat 12**: the eyes-closed
palms-down composite and one clip. If those two land, the movement's two emotional poles exist
and everything else is production. Cost ~66.

**60% — Structure.** The set: three **state-C corner plates** as edits of the locked M1 plates
(the breach already exists), four composites, then the **eight clips** for beats 15 and 16 from
the same start frames. Settle question 3 before Grok's. Cost ~260. Then S11 + beat 13 (question 1
first), and the replay page design (beat 14) — the page as a still, the cursor in post.

**90% — Polish.** Beats 17 (two clips + a screen edit), 20 (a still), the S09 state-B wide if
question 2 says so, and the assembly pass: hand every clip to the cut with its 7s intact, and
run the stopwatch table-read (#206) against the 2:00 ceiling with the five-second pit stop and
the six-second replay as the two hard floors.

**Every clip is 7s at fast; the timing comes down in the edit.** Every wrong-build corner in M3
starts from a **rest pose, ¾ front, face visible, eyeline on the task**, and carries **one face
constant per character** in the "the same … in every frame" form. The Grok identity line is
verbatim and never paraphrased. Zero negation. Register and vocabulary blocks verbatim.

---

## MEASUREMENT — $0, a tripwire, never a verdict

```
post/layout_hold.py  <start.png> <clip.mp4>     # 1.00 identical; ≥0.95 both ends is the bar; run vs BOTH keyframes on a 2kf clip
post/analyze_clip.py <box> <clip.mp4> ...       # motion energy, bg drift, travel
post/verify_edit.py  <plate> <edit> [...]       # FFT phase + edge keep; a wreck-edit reads CHECK by construction (law 1)
post/normalize_paper.py <png>                   # → normalised/, the working set (use the repo venv)
post/make_closeup.py                            # the S08 crop route — S11's camera rough
ffmpeg -i clip.mp4 -vf "fps=12/7,scale=480:-1,tile=4x3" -frames:v 1 sheet.png   # the contact sheet Sean reads
```

Runners: `motion/gen_image.sh`, `gen_image_ref.sh` (one design ref — every edit), `gen_image_refs.sh`
(role-split refs — every new plate), `composite.sh` (one character into a plate), `generate.sh`
(one keyframe), `generate2kf.sh` (two keyframes). Job json is a one-element list. **An empty
`[]` json is a dropped wait, not a failed job** (law 5): check `higgsfield generate list` and
recover with `generate wait <id> --json` before spending again.

Sean's eye has now overruled the metrics **seven** times on this project. Put the picture in
front of him — the contact sheet plus the mp4 path — before writing a verdict.

---

## WORKING DISCIPLINE

**Sean directs. Propose with a stated lean and let his eye decide. Lock nothing on your own
judgment** — approval is his word, and when a beat has more than one approved take, the pick
between them is his too (wave 2 closed exactly that way). Push every proposal to a named
specific. **Show him the picture** — rough it at $0, sheet every clip, send the file. **Announce
cost before spending it**, keep a running total, and reconcile it against `account status` at
the end. **Report failure straight, in the first sentence.** Check the reference before calling
identity drift (wave 2 bought two re-rolls against Sean's own turnarounds). When a ruling
reverses an earlier one, record why, keep the superseded artifact, and say what it costs.
**After two CLI misses on the same frame, build the kit and hand it to Sean for the web app.**
Update the tracker on every generation and every approval; every prompt file carries its result
and diagnosis in its header; append the laws this wave earns to `_blocks.md` and the day's entry
to the root `CHANGELOG.md`. Leave a review packet at the end of the session the way
`CONTINUATION-2026-09-05-wave-2-review.md` did.
