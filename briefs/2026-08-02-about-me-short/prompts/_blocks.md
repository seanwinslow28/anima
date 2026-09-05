# Shared prompt blocks — Movement 1

Two blocks go into every plate prompt **verbatim**. Do not edit them per shot
(FIRST LICKS DR #41: the look lives in post; every plate generates CLEAN).

## PALETTE — from `environment-style.md`, binding

Warm cream drawing paper throughout, a pale putty cream, never white and never yellow. The floor is the same cream a half-step darker. Walls and floor are flat, quiet, and low-contrast — the room is a pale ground, and colour lives only on the characters and on small props. Graphite line and cross-hatch shadow carry all the form. Overall value stays high-key and even: no dark corners, no pooled shadow, no colour cast, no vignette, no dramatic lighting.

## REGISTER — style token + anti-render clause

Hand-drawn animation pencil test: graphite line, visible construction lines, cross-hatch shadow, light coloured-pencil wash on props only, paper tooth showing — no flat vector fill, no digital gradients, no painterly rendering, no photographic lighting, no 3D.

## REF ROLES — the re-angle reconstruction pattern

These corner plates are **re-angles of one designed set**, not edits, and `gpt_image_2`
will not re-camera from an edit instruction. Every plate therefore role-splits its refs.

**Rev 2 (2026-08-31, current).** The refs are the drawn room, not another plate:

- **Images 1 (and 2) = `normalised/ELEV-{wall}-v*.png`** — the elevation of each wall in
  the shot, as FIXTURE AND STYLE BIBLE, with *"Do NOT copy its flat orthographic camera."*
  **A corner shot gets BOTH its walls.** This is not decoration: S07 was the only rev-2
  plate given one elevation, and it was the only one that came back flat — the model had a
  flat reference and a nearly-square rough, they looked alike, and the elevation's camera
  won the argument. Two elevations signal a two-wall shot before a word of the prompt does.
- **Last image = `room-bible/SHOT-S0X-rough.png`** — the room projected through that
  camera. *"Follow its camera, perspective, horizon and left-to-right placement."*

**Rev 1 (superseded).** Image 1 was `probe-205/U-codex-corner.png`, the ratified S04 plate,
used as the world bible. It predates the palette clause and dragged every plate warm — the
rev-1 set needs paper gains of 1.06-1.27 to reach canonical, the rev-2 set 1.004-1.056.

### Say the perspective in words, and name the seam

The S07 re-roll changed three things at once and the plate came back right on the first
roll, so they are recorded together rather than separated:

1. Two elevations instead of one (above).
2. **A PERSPECTIVE paragraph** — where the vanishing point sits in the frame, which side
   of it shows a right-hand face and which shows a left-hand face, and that the baseboard
   line is not level. A rough shows this; the model apparently does not read it off one.
3. **A THE CORNER paragraph** — *"one clean vertical seam runs the full height of the
   frame ... the corner seam is a line, not a gap"*, plus what is on the receding wall
   beyond it and that it is drawn smaller and packed closer.

**Also: make the VISIBLE list agree with the rough.** The failed S07 prompt listed the
dartboard under OUT OF FRAME while the rough put it squarely in the left third, and
listed the crates as the far-left object when the side table was further left. A VISIBLE
list that contradicts the rough is a contradiction the model resolves by falling back on
the flat elevation. `make_shot_roughs.py` solves the frame; read the frame off it.

---

## Session log — 2026-08-30, 21:29 → 21:52

| Prompt file | Model | Refs | Result |
|---|---|---|---|
| `S03-claude-nook-plate.txt` | gpt_image_2 2k high | S04 bible + S03 plate-rough | `plates/S03-claude-nook-v2.png` |
| `S05-gemini-moodboard-plate.txt` | gpt_image_2 2k high | S04 bible + S05 plate-rough | `plates/S05-gemini-moodboard-v1.png` |
| `S06-grok-dartboard-plate.txt` | gpt_image_2 2k high | S04 bible + S06 plate-rough | `plates/S06-grok-dartboard-v1.png` |
| `S07-alarm-plate.txt` | gpt_image_2 2k high | S04 bible + S07 plate-rough | `plates/S07-alarm-v1.png` |
| `S03-claude-composite.txt` | gpt_image_2 edit | `refs/char-claude.png` + plate | composite v1, phase-corr 0.52 |
| `S05-gemini-composite.txt` | gpt_image_2 edit | `refs/char-gemini.png` + plate | v1 / v2 / v3 — v3 is the lean |
| `S06-grok-composite.txt` | gpt_image_2 edit | `refs/char-grok.png` + plate | composite v1, phase-corr 0.47 |
| `S07-alarm-off.txt` | gpt_image_2 edit | S07 alarm plate | screen-dark keyframe, phase-corr 0.47 |

**Single-character refs beat the lineup.** `refs/char-{claude,gemini,grok}.png` are crops of
`cast-scale-lineup.png`, upscaled 3×. Handing the composite a five-character lineup invites the
Codex/Gemini colour-family confusion that corrupted four July generations; one character per ref
removes the question.

**NSFW refusal, recorded so it is not rediscovered.** The first S06 composite prompt —
"grey gremlin shape, bat ears, red eyes, fanged grin", "arm cocked back mid-throw" — came back
`status: nsfw` with no image. Same character and same action described as "a round grey cartoon
creature with big pointed ears, a wide friendly cartoon grin", "one arm drawn back holding a small
dart, cheerful and mid-play" passed first time. The saved file carries the wording that works.

**Verification method for every edit:** FFT phase correlation + edge-diff ratio against the source
plate, per `environment-style.md`. All four edits landed **0.47–0.58**, at or above the 0.42 that
ruled the GPT edit path in over NB2's 0.077. Frame-delta means stay retired.

---

## THE REST-POSE LAW — 2026-08-31, and it governs every composite from here

Sean: *"whenever we generate images where the subject is already performing an action, it
looks awkward in Seedance motion because we're prompting the model to generate the action
that the character is already in the middle of performing."*

**The still holds a rest pose. Seedance supplies the movement.** The wording that works:

> It stands still and upright at rest, both arms hanging down at its sides, both feet flat on
> the floor, turned three-quarters away from us to face <the thing it is about to act on>.

The evidence is already in the archive and predates the rule: the ADOPTED motion recipe
(`motion/04-single-character-7s-ADOPTED.txt`) drives a **whole three-part beat** — hammer-typing
with a smear frame, stop and peer at a blinking light, arms overhead in triumph — out of a still
where Codex is merely standing with one arm raised to the rack. The still did not need to
perform anything.

**Held is not the same as transient.** Hands resting on a keyboard, an arm laid on a rack: fine,
those are positions. Mid-throw, an arm extended mid-reach, a hand pressing something onto a wall:
not fine, those are instants, and the motion model then has to either repeat them or undo them.

Superseded by this rule, kept as the record: `S03-claude-composite` v1 (reaching up with a flag)
and `S06-grok-composite` v1 (arm cocked back mid-throw). Both were good images.

## S02, and when to edit rather than re-generate

`S02-sean-desk-dressed.txt` dresses the wall behind Sean without touching him. When a shot is
already approved and the note is about **what is around** the subject, a surgical edit is
strictly better than a re-generation: the approved design, the framing and the palette all
survive by construction, and there is nothing to re-approve but the change itself.

---

## THE SCALE LAW — anchor to a TALL prop, and state a ceiling. 2026-08-31.

`prompt-how-much` says to anchor a composite's scale to a named prop rather than a
percentage of frame. True, but incomplete, and the incompleteness is measurable. The five
composites in this round were prompted with the same recipe and differed only in which
prop the scale clause named:

| shot | anchor named | anchor height | intended | measured | ratio |
|---|---|---|---|---|---|
| S03 Claude | tall paper stack | **5.6 ft** | 1.56 ft | 1.51 ft | **0.97** |
| S04 Codex | server rack | **7.4 ft** | 2.16 ft | 2.82 ft | 1.31 |
| S05 Gemini | worktable | 2.4 ft | 1.80 ft | 3.20 ft | **1.78** |
| S06 Grok | round side table | 2.2 ft | 2.52 ft | 5.60 ft | **2.22** |

**A short anchor does not constrain.** Both shots anchored to a knee-high prop came back
roughly double; both anchored to a prop taller than a person came back usable. "A little
taller than that side table" reads to the model as a floor, not a ceiling, and its prior
is to draw a character at a comfortable, person-ish size.

The clause that fixed all three re-rolls in one roll each, and the shape to copy:

> SCALE — draw it SMALL: it stands only thigh-high to a grown adult. At the foot of the
> server rack the top of its head reaches barely a quarter of the way up the rack, and it
> is shorter than the coffee counter beside it is tall. It is a small creature, never
> person-sized.

Four moves, all of them doing work: **shout the direction** (`draw it SMALL`), **a human
yardstick** (thigh-high), **a ratio against a TALL fixture in the same shot**, and **an
explicit negation of the failure** (never person-sized). After the re-rolls the four
mascots land at 0.97 / 1.13 / 1.08 / 1.17 of intended — within 20% of each other, and in
the right order, which is what a cut needs.

## Verification is now a script, not a memory

`post/verify_edit.py` implements the FFT phase-correlation + edge-diff check that
`environment-style.md` has required all along and that no file implemented. Run it on
every composite against the plate it was drawn onto.

**Its numbers are not the numbers in the session log below.** That session measured by
hand, left no code, and reported 0.42-0.58; this implementation scores the same accepted
images at 0.15-0.36. One of the two is differently normalised and there is no way to tell
which, so the script's floors are calibrated from this project's own accepted composites
instead. Compare runs to each other, never to the older figures.

## Session log — 2026-08-31, 18:00 → 18:25

| Prompt | Refs | Rolls | Result |
|---|---|---|---|
| `plates-rev2/S07.txt` | ELEV-east-v3 + ELEV-south-v2 + SHOT-S07-rough | 1 | `plates/rev2/S07-plate-v2.png` — corner seam, receding wall, consistent perspective |
| `composites-rev2/S02-sean.txt` | sean-v5 (back) + S02 plate | 1 | seated in the existing chair, back to camera, hands on the keyboard |
| `composites-rev2/S03-claude.txt` | claude-v4 (¾ back) + S03 plate | 1 | scale 0.97 of intended |
| `composites-rev2/S04-codex.txt` | codex-v3 (¾ back, facing right) + S04 plate | 2 | v1 1.31 scale, v2 1.13 — **v1 has the better cloud silhouette, v2 the better scale** |
| `composites-rev2/S05-gemini.txt` | gemini-v4 (¾ back) + S05 plate | 2 | v1 1.78 scale, v2 1.08. Feet on the floor with a contact shadow — the baseboard bug is gone |
| `composites-rev2/S06-grok.txt` | grok-v4 (¾ back) + S06 plate | 2 | v1 2.22 scale, v2 1.17. No NSFW refusal: the softened wording was reused verbatim |

**9 rolls, 6 setups, ~77 credits, ~25 minutes.** Every miss was scale; nothing missed on
identity, facing, footing, contact shadow or background preservation.

**The turnaround crops are in `refs/turnaround-views/`.** Five views per mascot, cut from
the 2026-06-30 sheets by ink-column valley, upscaled 3×. Pick the view that already faces
the way the shot needs — S04's rack is at frame-right, so Codex came from `codex-v3`
(¾ back facing right) rather than making the model rotate `codex-v4`.

**One open question for Sean, not a defect.** The star's ¾-back view reads as a teardrop —
the points that make Gemini a star are hidden from behind. That is faithful to the model
sheet. If the silhouette matters more than the rest-pose law's "turned away", the fix is
`gemini-v2` at a shallower angle, and that is his call, not a measurement.

---

## THE FACING LAW — ¾ FRONT, because a video model animates what it has been shown. 2026-08-31.

Sean, after seeing the ¾-back set: *"I don't want Seedance trying to invent what the other
halves look like."*

He is describing the cause of the one unsolved defect in the project. Codex grows a mouth
under Seedance `fast` — and the still it was driven from was a **back view**. The model was
asked to animate a face it had never been shown, so it invented one. Every mascot still is
now **¾ front**: whole face, whole body, both arms, both feet.

**This does not repeal the rest-pose law, and it does not repeal "never address the lens."**
It reorders them. The wording that satisfies all three:

> FACING — this is the important part: the character is turned three-quarters TOWARDS US.
> Its whole front is visible — both eyes, its full face, its chest, both arms and both feet.
> It is NOT seen from behind and NOT in profile. Its eyes are turned off to one side towards
> <the thing it is about to act on>; it is absorbed in that and never looks into the camera.

**Body to camera, eyeline to the prop.** Stage the character *beside* its prop rather than
in front of it, so the off-camera eyeline has somewhere real to go. Gemini's is the best of
the four: it looks *down* at the loose sketches at its feet, which is a genuine task and
gives motion an opening beat — look down, then look up at the board.

**What the re-facing bought, beyond Sean's reason:**

| | ¾ back | ¾ front |
|---|---|---|
| Codex silhouette | lumpy; the cloud's scallops flattened | scalloped, on-model |
| Codex scale | 1.31 then 1.13 | **0.95** — the tightest of the four |
| Gemini | reads as a teardrop; the star is invisible | **all five points read** |
| S03 metrics | 0.140 / 0.696, both marginal | 0.218 / 0.794, both clear |

The Gemini result closes an open question outright rather than deciding it: the teardrop was
never a defect, it was just what the ¾-back view of that model sheet draws.

**Cost:** 4 rolls, 34 credits, all first-roll. Scale after re-facing: Claude 0.84 (the one
regression, from 0.97), Codex 0.95, Gemini 1.15, Grok 1.19.

## CHARACTER REFERENCES IN VIDEO — what the models actually accept

Checked against `higgsfield model get`, not assumed. All $0 to establish.

| Route | Reference support | 7s / 720p | Verdict |
|---|---|---|---|
| **`seedance_2_0`** (adopted) | up to **9 image references** counting `start_image`/`end_image`; 12 files total across images/videos/audio. No named reference mode. | **24.5 cr**, and **adding refs does not change the price** | Try it. Free. |
| `seedance_2_5` | **`omni_reference` mode** — a named multi-reference mode, up to 30 images, and `start_image`/`end_image` are *only* legal in this mode | 45.5 cr @720p, 63 @1080p | Purpose-built. 1.9× the price, and a different model — the `fast`/`std` stutter finding does **not** carry over, so it would need its own soak. |
| `higgsfield soul-id` | trains a face model from 5–20 photos of a real person | — | **Wrong tool.** Its own skill doc rules out "named-character / non-photo avatars". |

`seedance_2_5` also replaces the `mode` enum entirely — it is `t2v` / `omni_reference` /
`video_edit` / `video_extension`, with **no `fast`/`std`**. Do not read the 2.0 mode findings
across.

**The cheap half of the answer came first.** A ¾-front still removes most of the guessing
before a video model is involved at all. Test the reference on top of that, not instead of it.

**The test to run:** one A/B on Codex — same ¾-front start frame, same ADOPTED prompt, with
and without `--image refs/turnaround-views/codex-v2.png` riding alongside `--start-image`.
Two clips, 49 credits. It settles the reference question and the mouth gate in one pass.

---

## MOTION LAWS — amended 2026-09-01 by Sean. Two reversals, both his, both recorded.

The 2026-09-01 continuation shipped two motion laws that Sean has now overruled. Neither was
his; both were the previous session's reading of one bad clip
([`motion/07-M1-beat2-claude-tidy-REJECTED-SLOWMO.txt`](motion/07-M1-beat2-claude-tidy-REJECTED-SLOWMO.txt)),
and reading one failure two ways is how a diagnosis over-reaches.

### 1. THE FEET LAW IS REPEALED. Jumps are allowed.

Superseded: *"Keep them on the ground unless the gag is the air."*

Sean, verbatim: *"the feet don't HAVE to stay down. That was just an issue in the previous
session because Claude floated to the top and gently fell to the floor in slow motion. It just
looked weird. There shouldn't be any rules on them staying on the floor."*

**He is right, and the archive already proved it before the rule was written.** `armA.mp4` —
the clip he called *"very cartoony with squash and stretch. Beautiful motion"* — has Codex
**spring up to the rack, work, and drop.** A vertical, on this exact route, at full snap,
approved. The rejected Claude clip and the approved Codex clip differ in **timing shape**, not
in altitude. The old rule mistook the one variable that was constant for the one that changed.

**What replaces it** is not a restriction but two positive constants:

- **Speed verbs on every vertical.** *springs, snaps, drops, slams, whips, darts* — never a
  neutral or eased description of a jump ("rises", "comes back down", "settles"). The failure
  mode is a jump described *without* a timing shape, which the model fills with uniform easing,
  which is moon gravity.
- **A LANDING constant, stated through time**, replacing the grounding constant:
  > It lands on all four feet on the floor after every leap.

  This permits the air and demands the weight, where *"its feet return to the floor on every
  landing"* forbade the air to get the weight.

### 2. FILL THE SEVEN SECONDS. The event budget is retired as a ceiling.

Superseded: *"three distinct beats, roughly 2–2.5s each."*

Sean, verbatim: *"I would rather have more room and character personality actions to work with
as opposed to a quick cut for each. **The timing comes down in the edit, not the
generations.**"*

The generation is raw material; the cut is where duration is decided. So a prompt's job is to
give the editor **the most character per clip**, not a pre-timed three-beat package.

**Three is now a FLOOR, not a target — and a LOOP is the ideal shape.** The original finding
survives intact and is the reason a loop is safe: *one action given 7s gets spread across 7s,
and spreading is slow motion.* A repeating loop (write → leap → place → drop → write faster →
leap again) cannot degenerate into one stretched action by construction, and it fills the
duration with personality rather than with easing. Both of Sean's own moves —
[`08` Claude's writing loop](motion/08-M1-claude-writing-loop.txt) and
[`10` Codex's study-and-fix loop](motion/10-M1-codex-study-fix-loop.txt) — are loops, and that
is the point of them: *"a great way to showcase a loop and a way to show how fast and eager
Codex is."*

### What did NOT change

The register block and the vocabulary block are still **constant across every character and
never edited per beat**, damping words are still the documented failure, negation is still
wasted tokens, and locks are still stated as constants through time. Those three laws are what
the two rejected clips actually establish.


---

## ENSEMBLE COMPOSITES — three findings from the S09 five-character frame. 2026-09-04.

Measured on the CRT-POV plate with all five characters, four generations, each answering one
question Sean asked. The route that closed the shot: **one edit per character onto the CLEAN
plate, then a deterministic matte merge** (`post/merge_edits.py`, threshold 12 / dilate 22 —
the tighter defaults clip ear-tips and tails).

1. **The character line is an identity LOCK, not a competitor to the reference.** Sean asked
   whether describing the character in words on top of its reference image was what drifted
   Codex. A reference-only one-pass answered no, decisively: without the descriptions Codex and
   Gemini were assigned each other's spots and each wore the other's face, and Grok reverted to
   a sneer. Keep the line. (`prompt-how-much` calls it the identity-lock for this reason.)
2. **Five references in one `gpt_image_2` call conflates the same-colour-family pair.** With
   descriptions, the one-pass integrated beautifully (every figure washed, sitting in the
   drawing) but Codex grew round eyes and a mouth; without them, see (1). The July NB2 finding
   holds on gpt_image_2. Ensemble beats (3½, 15, 16) go singles + matte. A one-pass is fine for
   a two-character frame that keeps Codex and Gemini apart.
3. **The Grok ¾-front sheet view is drawn on the snide side.** `refs/turnaround-views/grok-v2.png`
   has narrowed red eyes, angled brows and an ear slashing across a sawtooth grin; every friendly
   Grok on screen came from the description overriding it. Fixed once, at the reference:
   **`refs/turnaround-views/grok-v2-friendly.png` was the Grok composite reference for one roll — SUPERSEDED the same day by Sean's own friendly turnaround, `refs/turnaround-sheets/grok-friendly-turnaround-without-dart.png`, cut to `refs/turnaround-views/grok2-v1..5` (use `grok2-v2` for ¾ front; `grok2-dart-v*` when he holds a dart). My single-view fix came back with anime eyes; his sheet keeps the pencil-test eyes.** (round
   red-orange eyes, raised brows, even-toothed grin, everything else unchanged). Use it for every
   Grok composite and Seedance start frame from here.

Two small things the singles should say from now on, both learned from the one-pass: ask for the
**light coloured-pencil wash** explicitly (a grey character otherwise comes back as bare graphite),
and give the eyeline a **task** (looking at the dart in its own hand) rather than a side-glance
("back towards the corner"), which reads as scheming at small sizes.

**Sean closed S09 in the web app** after the CLI route's two matte failures and the one-pass pair
conflation: `normalised/S09-all-webapp-v1.png`. Two continuity rules from how he did it: **Claude
sits writing on paper in every still where it is at rest** (it is what the locked beat-2 clip
shows — `claude-sitting-v*`), and a mascot's rest pose carries its M1 task across the cut.

---

## WAVE 2 FINDINGS — beats 5–10, 2026-09-05. 23 generations, 23 first-roll landings.

1. **A wrecked return is an EDIT of the locked plate, not a re-angle.** B8-A is the S06 camera, so the
   re-angle reconstruction pattern does not apply; `gen_image_ref.sh` with the S06 plate as the one ref
   kept the drawing the audience knows by construction. **A large edit re-renders the whole frame** —
   bench and shelf correlate 0.75–0.88 against the plate, every fixture in place, line texture regrown —
   so `verify_edit` reads CHECK by construction on a wreck. Invisible at 720p; the rule allows it. The
   corner-seam, dartboard, bench and shelf were kept ON PURPOSE: M3's return plays in this framing.
2. **Through the hole: blank paper.** Nothing drawn. On-register, and it never has to match an outside.
3. **Codex's ¾-front face HAS a dot** — the far eye, on Sean's own sheet (`codex-v2.png`). It is not the
   S09 "grew round eyes and a mouth" failure. A re-roll against it is wasted (8.5 cr, wave 2). Never write
   "its eyes" for Codex; write "its face is tipped towards …" — the S13 v1 wording landed regardless.
4. **Claude's eyes are RED on the sitting sheet** (`claude-sitting-v2.png`); a red-eyed Claude is on-model.
   The pencil COUNT is the thing to lock ("exactly ONE pencil … only one pencil anywhere in the picture").
5. **The CLI's `--wait` can die on an HTTP 503 while the job survives.** It writes `[]` to the job json and
   exits 0 (the runner's `tail` hides it). The balance is charged and `higgsfield generate list` shows the
   job `in_progress`. Recover with `higgsfield generate wait <id> --json > out.json`. **An empty job json is
   a dropped wait, not a failed job — check the list before spending again.**
6. **The staging that cuts as a set:** every wrong-builder small at the foot of its own build (Claude at the
   tower, Codex under the code wall, Gemini before the fifty, Grok beside the rocket), ¾ front, eyeline UP
   at the build. The four beats then rhyme.
7. **Code, drawn:** rows of small graphite dashes and blocks, indented like listings, zero letters — the S02
   monitors' idiom, denser. Reads as code, obeys the no-text law, and scrolls under Seedance (measured 7–12
   px per 0.25 s while Codex hammers, 0 while he peers). Real legible code is one 8.5 roll away if wanted.
8. **A worm's-eye leap "clean out of the top of frame"** came back as a leap TO the top of frame with a
   real smear frame on the repeat (the repeated-action guide, proven again). The fixed-camera clause plus an
   explicit "drops back into frame" event held the camera.
9. **The two-keyframe alarm on the closeup holds both ends** (0.994 / 0.991) and the model reads "the whole
   picture jolts" as the SET RATTLING on its shelf — a cartoon jolt; post can add its own shake or skip it.

### Round 2 (2026-09-05, after Sean's rulings) — five more, all paid for

10. **A prop that has to APPEAR mid-clip goes in the END keyframe.** Codex's screen pops out of the rack; the
    S07 arm-B route (start without it, end with it, drawn once by gpt_image_2) keeps the text-ish screen out
    of the video model's hands. Same for the wreck: **beat 8's two-keyframe clip (intact corner → breach)
    did the whole demolition and the rocket-haul in one roll, both ends 0.988 / 0.987.** When a beat changes
    the SET, drive it from both states rather than asking the model to invent the second.
11. **The model tops out on "everywhere."** Three densities of paper wording gave 1–3 / 3–6 / 5–8 pages a
    frame. Past that the lever is post (a particle overlay), not a fourth roll.
12. **A rotational whirl smears beautifully and breaks a different constant each time** — v2 the SIZE (she
    ballooned 3×), v3 the FLOOR (the size lock held; she lifted off). State the whirl's size AND its footing
    as constants together, or accept one. Do not name Taz; describe the whirl.
13. **A chair spin from a back-view still turns him to the lens and the model invents his face** (beat 9 v3)
    — the 3½ v2 exorcist, again, now with an open mouth in a film where he speaks once. The facing law
    applies to every rotation, not just head-turns.
14. **Re-rolling the same prompt is a real variety lever** (beat 9 v2: the cannon TOPPLED, unprompted). Buy
    the identical re-roll before buying a rewrite when the notes are "variety", not "wrong".
