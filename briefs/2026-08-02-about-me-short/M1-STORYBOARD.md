# Movement 1 — "Quiet Morning" · storyboard & production tracker

*The living per-shot state of Movement 1: what's boarded, plated, generated, motioned and
Sean-approved. **Update on every generation and every approval** — this file is only useful
if true. Story content lives in [`beats-v1.md`](beats-v1.md) and
[`00_studio_brief.md`](00_studio_brief.md); this tracks production state against them.*

**Status legend:** `—` not started · `draft` exists, not ratified · `✓` done/banked ·
`✓S` Sean-approved · `RE` needs regeneration (reason in Notes)

**Framing grammar (from *Goofy Gymnastics*, watched 2026-08-30):** play every shot against a
near-empty flat wall with the character owning 60–90% of frame height. **There is no
establishing wide at all** — Sean cut it 2026-08-30. The consequence is explicit: the
audience never sees the whole room, so continuity rests entirely on the corner plates
matching each other. Every corner must carry the same signature — same paper, same floor,
same baseboard, same light.

**State FACING, not just position.** The cut wide failed partly because facing was never
specified and everything defaulted to addressing the lens. Each mascot's attention direction
goes in its prompt: absorbed in its own task, never looking at camera. See [`environment-style.md`](environment-style.md) — **this revises the first
boarding**, which had knee-high mascots in furnished corners. It is also the drift fix: the
22–27% background drift was measured on the busiest wall in the room.

**Runtime:** 0:00–0:15, three beats, seven setups. Beat 2's *"slow pan of the HQ"* is
**not** one continuous wide — Sean ruled 2026-08-30 that it is the establishing angle plus
a cut to each mascot's own corner.

**Gate owed before Movement 2 boards:** the stopwatch table-read
([#206](https://github.com/seanwinslow28/code-brain/issues/206)). Its two outputs — the
runtime laps and the "He speaks" contradiction — both land in Movement 2, so Movement 1
boards ahead of it without pre-empting anything.

---

## Ruled production settings (probe-205, 2026-08-30)

| Setting | Value | Why |
|---|---|---|
| Plate generation | `gpt_image_2`, 2k, quality `high` | Won the register test; holds cast identity from the lineup reference |
| Character into plate | `gpt_image_2` **edit**, 2 refs (lineup + plate) | Phase-corr **0.42** vs NB2's **0.077**; surgical-only is the property we want |
| Re-angles of the set | **NOT** `gpt_image_2` | It will not re-camera from an edit. Use NB2-via-edit, or GPT with world-bible + composition rough |
| Motion | `seedance_2_0`, **`mode: fast`**, **7s**, 720p, `generate_audio: false` | `std` **stutters and looks broken** (Sean, 2026-08-30). 7s carries a whole beat; single-character cuts drift ~18% |
| Composite prompt | ≤70 words, never re-describe the scene | An 85-word prompt cost NB2 the whole plate |
| Motion prompt | Genre anchor · vivid verbs · **zero negation** · positive identity lock · positive grounding clause | Seedance takes no negatives; damping words dampen |
| Post look | **Post, not generation** | FIRST LICKS DR #41 — every plate and composite generates CLEAN |
| **Pose in the still** | **REST, never mid-action** | Sean 2026-08-31: *"whenever we generate images where the subject is already performing an action, it looks awkward in Seedance motion because we're prompting the model to generate the action that the character is already in the middle of performing."* The still holds the character standing, arms down, facing its task; **Seedance supplies the movement.** Distinguish transient poses (mid-throw, arm extended mid-reach) from held ones — hands resting on a keyboard is a rest pose |
| **Paper** | **normalise every frame in post** | Sean 2026-08-31. `post/normalize_paper.py` → `normalised/`, which is the working set. The tan ground was swallowing the mascots |

**Known open risk:** background drift measures **~22–24%** on prop-dense plates at every
tier and duration tried. Untested candidates: first+last keyframes composed from the same
plate; or matting characters out of the animated clip and re-laying them on the pristine
plate.

---

## Spatial authority — [`room-bible/`](room-bible/)

**Superseded 2026-08-31.** The Movement-1 floor plan is retired to
[`m1-guides/old/`](m1-guides/old/) and the room is now planned for the **whole film** in
[`room-bible/`](room-bible/): a ground plan, unrolled wall elevations for all four walls, and
those elevations **drawn** in the pencil-test register. Read
[`room-bible/README.md`](room-bible/README.md) before touching any plate.

Sean's ruling, and it changes the order of work rather than one drawing:

> "We have to treat this like a sculpture that we chip away at one piece at a time. In 2D
> animation, everything is fully planned out, full extended rooms are drawn, character
> turnarounds are drawn, then the scenes, individual characters, and sectioned off
> backgrounds get drawn out and created separately and then composited."

**The order does not vary:** ground plan → elevations → rendered elevations → corner plates
generated *against their wall* → characters composited *from the real turnarounds* → motion →
timing.

**Every Movement 1 corner plate is therefore being redrawn**, S04 included. Three continuity
errors made that necessary and the room bible's README carries the diagnosis; the short
version is that the rack and the moodboard were claiming the same end of the same wall, the
CRT was two different fixtures at two different heights, and Gemini was standing on the
baseboard. The first two are geometry and are now settled by construction. **S04 comes back
mirrored** relative to the banked plate.

**Cast scale ratios** (from `cast-scale-lineup.png`): Sean 1.00 · Grok 0.42 · Codex 0.36 ·
Gemini 0.30 · Claude 0.26. State scale in words in every prompt; it is never inferred.
**Eye level is 5′6″** and it is the horizon every corner plate sits on.

**The USER does not appear in the room.** The doorway stays empty set dressing; the USER is
introduced on the CRT — and **Sean asks the question at his computer**, not at a door (Sean,
2026-08-31: *"that fits better with the theme of no dialogue and just VO, music, and sound
effects anyway"*). That restages beat 13 onto the S02 setup, so beats 2, 4, 12 and 13 all play
at Sean's station. **Flagged, not absorbed:** if the question is typed rather than spoken, the
Sean character never speaks aloud, and the brief's non-negotiable is *"The Sean character
speaks exactly once — the question."* Confirm or override.

## Shots

Guides: [`m1-guides/`](m1-guides/) — Python-generated composition roughs
([`make_m1_guides.py`](m1-guides/make_m1_guides.py)), FIRST LICKS idiom, $0 and re-runnable.
Each doubles as the monochrome composition rough for a re-angle and as the placement
authority for the character-into-plate edit.

| # | Setup | Beat | Camera (from the ground plan) | Plate | Composite | Motion | Notes |
|---|---|---|---|---|---|---|---|
| S01 | Title card | 1 | n/a — typography, **not** Seedance | **✓S** | n/a | n/a | Card D approved and normalised. Typography still undecided |
| S02 | **Sean's station** | 2 · 4 · 12 · 13 | inside the room, straight at the north wall | **✓ rev2** | **✓S** | **✓S** | The most-used angle in the film now that the question is typed at his computer. `plates/rev2/S02-plate-v1.png` · **Motion 2026-09-01:** v1 `S02-sean-coffee-v1.mp4` + v2 `S02-sean-coffee-v2.mp4` (the chug landed, the smears did not). **v3 `S02-sean-coffee-v3.mp4` regressed on every axis and lost the drink entirely** — the smear is now a closed question, see prompt 15. **v1 LOCKED 2026-09-01** — Sean: "it's still good and makes him feel more human" |
| S03 | **Claude's nook** | 2 | into the **NW corner** | **✓ rev2** | **✓S** | **✓S** | Two walls meeting: the nook on the west wall, the filing cabinet on the north · **Motion 2026-09-01: LOCKED.** `S03-claude-writing-loop-v1.mp4` — the writing loop, first roll. Seedance invented the paper pile; the still never needed re-generating |
| S04 | **Codex's rack** | 2 | into the **SW corner** | **✓ rev2** | **✓S** | **✓S** | The moodboard's west end at frame-left, the rack at frame-right. Mirrored from the banked probe plate, as the plan required · **Motion 2026-09-01:** `S04-codex-study-fix-v1.mp4` — study/climb/coil loop, first roll. Layout 0.992/0.989, the tightest on the project — **LOCKED 2026-09-01** |
| S05 | **Gemini's moodboard** | 2 | square to the south wall | **✓ rev2** | **✓S** | **✓S** | The CRT is genuinely **out of frame** under rev 2 — measured off the plan, not guessed. The S05↔S07 landmark is the moodboard wrap instead · **Motion 2026-09-01: RE.** `S05-gemini-one-more-v1.mp4` starts with the moodboard wall BARE (layout f0 0.875) and rebuilds it. Prompt fault — 'growing sideways across the wall'. Banked as a beat-7 asset. **v2 `S05-gemini-one-more-v2.mp4` fixes it** — f0 0.957, drift 11.6% — at the cost of legibility; **Sean picked v2, LOCKED 2026-09-01**; v1 kept as the beat-7 asset |
| S06 | **Grok's dartboard** | 2 | into the **NE corner** | **✓ rev2** | **✓S** | **✓S** | Board face clean, every dart in the plaster · **Motion 2026-09-01:** `S06-grok-throw-v1.mp4` — throw / miss / airborne triumph / throw again, first roll, no nsfw refusal on the video path either — **LOCKED 2026-09-01** |
| S07 | **The CRT alarm** | 3 | at the east wall | **✓ rev2** | n/a | **✓S** | Screen **dark** — the alarm is the movement (rest-pose law). The PROBLEM! frame is a surgical edit on top · **Motion 2026-09-01:** the project's first TWO-KEYFRAME and first FREE-CAMERA shot. Route ratified as **arm B** (start = `S07-plate-v2`, end = `S07-alarm-closeup-v1`, a $0 crop via `post/make_closeup.py`) — arm A with no end frame redrew the screen with a lightning bolt, which Sean rejected as "comic book and less pencil test". **LOCKED 2026-09-01: `S07-pushin-armB.mp4` (arm B v1)** — Sean took the fallback and cuts the timing in post. v3 hit the requested 3.08s zoom and still lost; the number was never the problem. **The screen never blinks and that is now a POST job** — three phrasings failed. Sean's final pick between v3 and v1 pending |

**All six plates are regenerated from the room bible**, normalised, and needing paper gains of
1.005–1.056. Every earlier plate is superseded; `plates/` and `composites/` hold the old ones.

**Aliasing hazard on this movement:** Codex (lavender cloud) and Gemini (blue-purple star)
are the same colour family, and NB2 corrupted one with the other **4/4** in July. They are in
**separate setups** here (S04, S05), which sidesteps it entirely — keep them apart, and if a
later shot needs both in frame, split the generation passes.

---

## What beats 4–20 inherit

- **The whole set.** S02 fixes every zone's position; Movements 2 and 3 re-angle rather than
  re-invent. **When a later angle invents a new zone, ratify that plate before any other
  angle showing the same zone** — it becomes that zone's bible (DR #20).
- **The four corner plates** (S03–S06) are the wrong-build beats' locations: Claude's 40-page
  document, Codex's full rebuild, Gemini's fifty concepts, Grok's wall-demolition rocket all
  happen in these same corners, escalated.
- **The CRT** (S07) fires again at beat 10 — *PROBLEM (STILL!)*, visually bigger, frame shake
  and red flood — and a third time as the closing sting. Same fixture, same wall.
- **The CRT is now the USER's stage.** Sean's ruling moves the USER's introduction from the doorway onto the screen, so S07's television is carrying more than the alarm — Movement 3's reveal happens in that same fixture.

## Production log — 2026-08-30 evening

Instrumented against the **4-hour bar**. Clock started 21:29; four plates, four composites
and two re-rolls done by 21:47 — **~18 minutes of wall-clock for six of the seven setups'
still-images**, 9 `gpt_image_2` calls at 8.5 credits each (~76 credits). One NSFW refusal
(S06, first wording) and three rolls on S05. No motion generated yet — that gate is Sean's.

**Route note, and it is a change of mechanism for S03.** The storyboard had S03 as
`full-scene`; it was generated as a **clean plate + character edit** like the others, so
every corner now has a character-free plate on file. That is what keeps the
matte-the-character-out-and-re-lay-it-on-the-pristine-plate mitigation available for S03
too, and it costs one extra generation. Say so if you would rather have had the single pass.

**The re-angle reconstruction pattern is what made these work.** `gpt_image_2` will not
re-camera from an edit, so each plate role-split two references: the S04 plate as
world/style/fixture bible with an explicit *"do not copy its camera"* clause, and the shot's
own character-free composition rough for the camera. Every plate followed its rough. The
character-free roughs are new, emitted by `make_m1_guides.py` as
`M1-S0X-…-plate-rough.png` — same shot, characters and red guide marks stripped, $0.

**Prompts are now on disk.** The previous session's plate prompts were not saved and could
not be recovered; [`prompts/`](prompts/) holds every prompt used tonight plus the shared
blocks, so a re-roll is a re-run rather than a reconstruction.

## Production log — 2026-08-31 morning

Second working session, ~25 minutes, 6 generations (~51 credits) and one $0 Python artifact.
Sean's five rulings and what each cost:

1. **Normalise every frame in post.** Done, and it is now a pipeline step rather than a
   one-off: [`post/normalize_paper.py`](post/normalize_paper.py) → [`normalised/`](normalised/),
   **which is the working set from here on.** Eleven frames, all inside ±8 of canonical after
   correction, clipping under 0.4% on the heaviest lift. The measured table is in
   [`environment-style.md`](environment-style.md).
2. **Gemini v1.** Taken, and the reasoning generalised into the rest-pose law above — v2 and v3
   are superseded by the rule, not by their execution.
3. **The floor plan.** Built at [`m1-guides/make_floor_plan.py`](m1-guides/make_floor_plan.py),
   $0 and re-runnable in the same idiom as the shot guides. It found the CRT hole as geometry
   rather than as a worry, and the fix shipped in the same session.
4. **Re-roll S02.** Done as a surgical edit of the approved plate, which is the cheaper and
   safer move than re-generating a shot Sean had already signed off.
5. **The recovered prompt archive.** `prompts/motion/04-single-character-7s-ADOPTED.txt` is the
   motion recipe for every corner. Note what it proves: the S04 still holds Codex standing with
   one arm raised, and the clip gets hammer-typing → peer → triumph out of it. That is the
   rest-pose law's evidence, not just its rationale.

## Open before motion starts

1. **Title-card typography** (S01) — still not decided. It is the one setup Seedance never touches.
2. **The CHECKOUT COMPLETIONS label** on S07's falling graph. Left off deliberately so the plate
   would not sprout captions; it is one edit away if Sean wants the specificity.
3. **Codex's face at scale.** It went off-model in every `fast` generation — it grows a mouth.
   At corner-shot scale it may not read, and `std` holds the face but stutters, so it is not the
   answer. This is the one thing still owed Sean's eye before the remaining corners animate.
4. **The matte-and-relay drift test** — matting the character out of the animated clip and
   re-laying it over the pristine plate, which would make plate drift structurally impossible.
   Still unrun, and now worth more than when it was proposed: prop-dense corners are exactly the
   condition that produced the measured 22–27% background drift.


---

## Movement 2 setups — started 2026-09-03 (tracked here until an M2 board file exists)

Camera decisions ruled by Sean 2026-09-03 from the $0 roughs in
[`room-bible/m2-candidates/`](room-bible/m2-candidates/README.md). Setup ids **S09/S10 are
proposed**, not ratified (the monitor closeup pencilled as S09 in the open list moves to S11).

| # | Setup | Beat | Camera | Plate | Composite | Motion | Notes |
|---|---|---|---|---|---|---|---|
| S09 | **The room reacts** — the CRT's POV | 3½ | `B3h-A`: lens at the CRT glass (24.4, 11.8), 7′9″ up, state A | **✓ v1** (first roll, 8.5 cr) | **✓S** — CLI route rejected (matte cut Codex; single-view Grok fix came back anime-eyed); **Sean finished it in the web app: `normalised/S09-all-webapp-v1.png`** (1672×941). **Motion v1 (24.5 cr, first roll): `motion/m2-beat3h/S09-room-reacts-v1.mp4`** — all three events, layout 0.989/0.977, Sean's eye owed. Claude sits writing (as in beat 2); new friendly Grok turnaround supersedes every earlier Grok ref (`refs/turnaround-sheets/`, views `grok2-v*`, `claude-sitting-v*`) | — | `plates/rev2/S09-room-reacts-v1.png`, normalised. Two plan misses on the right wall (printer bench drawn near-right in the storage bench's spot; chair turned to the room) — Sean's call: edit or accept. **✓ all five, v1** (42.5 cr, five first-roll landings, matted onto the clean plate by `post/merge_edits.py`; verify 0.784 / 0.954 pass) → `normalised/S09-all-v1.png`. Grok came back a sneer; Sean asked why he looked pasted → matte clipped his ear/tail (re-merged wider, `S09-all-v1b.png`, $0) AND the edit drew him without wash. **A/B run 2026-09-04:** one-pass six-ref edit (8.5 cr) `S09-all-onepass-v1.png` — Grok fixed and everyone washed, but **Codex grew eyes and a mouth** and the plate re-rendered (0.091/0.580). Sean asked whether the description lines compete with the references → **reference-only one-pass v2 (8.5 cr): NEGATIVE** — Codex and Gemini conflated, Grok back to the sneer; the description is an identity lock, and five refs in one call is the structural failure. **Route ruled by evidence: singles + matte.** **Reference fixed** (`grok-v2-friendly.png`, 8.5) → Grok single v2 (8.5, first roll) → re-merged: **`normalised/S09-all-v2.png` is the S09 still** (0.694 / 0.915 pass). Motion draft: `prompts/motion/21-M2-S09-room-reacts-DRAFT.txt` |
| S10 | **Sean from the room**, low | 4 · 12 · 13 | `B4-A`: (13.5, 7.6), lens 2′3″, tipped up | **✓ v1** (first roll, 8.5 cr) | **✓ v1 + v2** — the face look-test landed first roll (8.5 cr) and Sean kept it; v2 (eyes DOWN to the mascots, 8.5 cr, first roll) added at his ask; both at `composites/rev2/S10-sean-composite-v{1,2}.png`, normalised; verify_edit CHECK on both (≈0.10 / 0.57) read as figure coverage, not plate loss. Sean picked v2. **Motion v1 (24.5 cr): `motion/m2-beat4/S10-silent-go-v1.mp4`** — the GO landed (twirl, jab, slam round) but my word "glowing" turned the screens white after the spin (layout last 0.828); **v2 prompt 22 written** (screens locked dark), awaiting the go | **v2 STANDS** — v1 rejected (clown twirl); v2 = Sean's own action text, 0.979/0.911, `motion/m2-beat4/S10-silent-go-v2.mp4`, "solid, still kind of off, usable"; v3 on prompt-how-much levers came back WORSE (mouth opens wider, chair slides more, 0.958/0.884). Closed-mouth constant failed two phrasings; next lever is deleting the breath event. **LOCKED 2026-09-05: `motion/m2-beat4/S10-silent-go-v4.mp4`** (Sean's roll; the two-finger flick lands, chair stays at the desk) → `_LOCKED-M2/09_beat4_S10_silent-go.mp4` | `plates/rev2/S10-sean-front-v1.png`, normalised. Low angle half-landed — reads as a medium a little below eye level. Sean's call: accept or re-roll. Cannon still a telescope. Motion draft: `prompts/motion/20-M2-S10-sean-silent-go-DRAFT.txt` |
| **S06B** (proposed id) | **Grok's corner, WRECKED** — room state B | 8 | `B8-A` = the S06 camera, wrecked (ruled) | **✓ v1** — a surgical EDIT of the locked S06 plate, not a re-angle (same camera; the wrecked-return rule works because the audience knows the drawing). Two answers to Sean's "how much is gone?" rolled side by side (17 cr): **A THE BREACH** `normalised/S06B-breach-v1.png` (the lean — seam, dartboard, bench, shelf survive for M3's return; hole to blank paper, rocket nose-into-the-hole, rubble fan, hammer on the crates) and **B THE CORNER IS GONE** `normalised/S06B-corner-gone-v1.png` (bigger; kills the seam). Sheet `plates/rev2/S06B-AB-sheet.jpg`. Both whole-frame re-renders (fixtures in place, texture regrown) — verify CHECK by construction. **Sean's eye owed; this plate is the NE corner's bible for M3 (DR #20)** | **✓ v1** onto A — `normalised/S06B-grok-v1.png` (8.5, first roll): `grok2-v2` at the foot of the rocket, ¾ front, hammer head on the floor, eyes up at the nose cone, plate hammer removed | **v1 (24.5, first roll): `motion/m2-beat8/S06B-grok-demolition-v1.mp4`** — swing / plaster burst / lean on the rocket / swing again, all on the sheet; layout 0.986/0.949, drift 11.9%, motion 2.26. Sean's eye owed | Prompts `prompts/plates-rev2/S06B-*.txt`, `prompts/composites-M2/S06B-grok.txt`, `prompts/motion/25`. Beat 8 is the first beat with a whole package in front of Sean |
| **S12** (proposed id) | **Claude's paper canyon** | 5 | `B5-A` worm's eye up the tower (ruled) | **✓ v1** `normalised/S12-claude-canyon-v1.png` (8.5, first roll; ELEV-west + ELEV-north + B5-A plate rough) — three-point perspective, three stacks out the top of frame, flags fringing upward, the shelf looming | **v1** `normalised/S12-claude-v1.png` (8.5): `claude-sitting-v2` at the foot of the tower, writing, ¾ front, verify PASS 0.223/0.749 — eyes RED = on-model to Sean's sheet; **two pencils = a miss → v2 rolling** (pencil count locked) | **v1 (24.5, first roll): `motion/m2-beat5/S12-claude-canyon-v1.mp4`** — write / spring up the canyon to the top of frame in a page shower / drop / land / write / leap again with a real smear frame; layout 0.980/0.973, drift 10.8%. Driven from composite **v2** (one pencil). Sean's eye owed | Prompt `26` |
| **S13** (proposed id) | **The code wall** | 6 | `B6-A` square on the code wall (ruled) | **✓ v1** `normalised/S13-codex-code-wall-v1.png` (8.5, first roll; ELEV-west + B6-A plate rough) — the big screen of dash-code (reads as code, zero letters — my call on the text question, one roll from legible if Sean wants it), cabled into the rack | **v1** `normalised/S13-codex-v1.png` (8.5): position/scale/wash landed, **grew an EYE** (a dot beside the chevron — the S09 failure on a single; my facing clause said "its eyes", on a character with none) **→ v2 rolling** with an eye-less face lock | **v1 (24.5, first roll): `motion/m2-beat6/S13-codex-code-wall-v1.mp4`** — spring onto the counter / hammer-type / peer / triumph / again; the code wall measurably scrolls while he hammers (downward — a nit); bracket-and-dash face held; layout 0.990/0.973, drift 10.9%. Driven from composite **v1** — the composite's "eye dot" is ON-MODEL (Sean's ¾ sheet has it; my v2 re-roll was an unnecessary 8.5). Sean's eye owed | Prompt `27`. `motion/ab-codex/armA.mp4` stays the fallback |
| **S14** (proposed id) | **Gemini's fifty, raking** | 7 | `B7-B` raking east along the board (ruled) | **✓ v1** `normalised/S14-gemini-fifty-v1.png` (8.5, first roll; ELEV-south + ELEV-east + B7-B plate rough) — the wall recedes to a vanishing point, sketches three-deep, the spill on the table, the floor, the cartons, the far wall's binders | **✓ v1** `normalised/S14-gemini-v1.png` (8.5, first roll): `gemini-v2` foreground left of the worktable, ¾ front, all five points, eyes up at the wall | **v1 (24.5, first roll): `motion/m2-beat7/S14-gemini-fifty-v1.mp4`** — slap / spring up the wall to slap higher / drop / slap / arms wide; wall full from frame 0; layout 0.982/0.944, drift 13.4%. Nits: eyes squint shut in a couple of frames; the wall-climb is a big vertical. **The CLI's wait dropped on a 503 and wrote an empty json while the job ran** — recovered by id, no re-roll. Sean's eye owed | `S05-gemini-one-more-v1.mp4` released |
| S02 | **The hollow SHIP IT** | 9 (twin: 17) | S02 (locked) | — | **✓ v1** `normalised/S02-cannon-fix-v1.png` (8.5, first roll): the telescope is now a short fat striped confetti mortar on the same tripod with a pull-cord ring, Sean and everything else untouched. **Continuity flag:** the locked beat-2 clip still shows the telescope (frame-edge, 720p, two movements apart; 24.5 to re-roll if Sean wants) | **v1 (24.5, first roll): `motion/m2-beat9/S02-hollow-ship-it-v1.mp4`** — key slam / arms up / the cannon coughs a small burst / the bell swings / a ~3s arms-up hold (the cut trims) / arms drop / he slumps face-down on the desk; layout 0.990/0.978, drift 8.7%. Sean's eye owed | Both prop states designed on one start frame: rest here, sag/misfire in 9, full swing/clean burst in 17 |
| S08 | **ALARM #2 — PROBLEM (STILL!)** | 10 | S08 closeup (locked) | `normalised/S08-crt-closeup-v1.png` (normalised today, $0) | **✓ v1** `normalised/S08-alarm2-v1.png` (8.5, first roll): PROBLEM filling the screen's width, (STILL!) beneath, the jagged line steeper (it stops inside the screen rather than running off the bottom — fine) | **v1 (24.5, first roll, two-keyframe): `motion/m2-beat10/S08-alarm2-v1.mp4`** — dark two beats / white flash / PROBLEM (STILL!) bangs on and holds / the set rattles on its shelf, sketches flutter, cable whips / settles; layout 0.994 vs start, 0.991 vs end. Sean's eye owed | My lean on "where is Sean": the closeup alone; his freeze = a post freeze-frame on the tail of beat 9's clip (his back, arms up), which beat 11's record scratch then holds. Sean's call |

### Wave 2, round 2 — Sean's rulings on the v1 packages (2026-09-05, 15:46), and what each cost

Sean, on the six v1 packages: *"These are all looking great so far, but we need to make it MORE chaotic."* Per beat:

| Beat | Sean's ruling | What was made | State |
|---|---|---|---|
| **5** Claude | *"Papers flying everywhere … rapidly writing as much as possible. Claude's bouncy squash and stretch movement is perfect though."* | **v2** `motion/m2-beat5/S12-claude-canyon-v2.mp4` (3–6 pages a frame, 0.987/0.971) and **v3** `…-v3.mp4` (5–8 pages, pages flung over the shoulder, 0.978/0.955, motion 1.97). Same start frame; the bounce wording untouched | **Sean picks the level.** Three densities of wording gave 1-3 / 3-6 / 5-8 pages; the model tops out short of a blizzard. A paper-particle overlay in POST is the next lever, not a fourth roll |
| **6** Codex | Continuity error: the locked M1 frame has **no screen and no water cooler**. Keep the angle; regenerate the background to S04's items; cooler removed. Motion: *"Codex should hit the computer tower, the screen pops out from the side with lines of code and Codex then codes at max speed. The screen flashes and floods with code."* | **Plate v2** `normalised/S13-codex-corner-v2.png` (the S04 corner from B6-A: cartons + sketches, seam, bare wall, counter, rack, doorway; first roll) → **composite** `normalised/S13-v2-codex-v1.png` (pass 0.199/0.783) → **END frame** `normalised/S13-v2-screen-popped-v1.png` (the screen out of the rack's side on a hinged arm, flooded with dash-code; pass 0.281/0.850) → **clip v2, two keyframes** `motion/m2-beat6/S13-codex-screen-pop-v2.mp4` | **LANDED, first roll:** hit / the screen bangs out white / springs onto the counter / hammer-types / the screen floods, flashes, floods / drops to the floor. **0.987 vs start, 0.988 vs end.** One register slip: the first flood is GREEN-phosphor code for ~2s before settling to graphite dash-code — Sean's eye. The v1 plate + clip (code wall + cooler) are superseded, kept as the record. My v1 fault: a VISIBLE list that contradicted the rough (the cooler) |
| **7** Gemini | *"The framing is perfect. We just need Gemini going at a very fast speed as if it was the Tasmanian devil."* | **v2** `motion/m2-beat7/S14-gemini-fifty-v2.mp4` (a true rotation with a spin-smear ring; she BALLOONS ~3x on the first whirl, true size on the second; 0.974/0.921, motion 2.93) and **v3** `…-v3.mp4` (whirl locked to her size — held — but it LIFTS off the floor and drifts left; 0.982/0.929) | **Stopped at two rolls** (the S07/S10 discipline). Sean chooses v2 / v3, or directs a v4 with a feet-on-the-floor constant |
| **8** Grok | *"The rocket looks great, but Grok is supposed to take the hammer, smash the wall, pull the rocket into the room from the other side of the wall, and pat it."* | **START frame** `normalised/S06-grok-hammer-v1.png` (the intact S06 corner + Grok holding the hammer at rest; pass 0.226/0.817) → **clip v2, two keyframes** (start → the breach composite as END) `motion/m2-beat8/S06B-grok-demolition-v2.mp4` — hoist / smash / table over / second swing / hammer down / leans in through the hole / hauls the rocket in / pats it. **0.988 vs start, 0.987 vs end**, first roll | **Supersedes v1.** Sean's eye owed. Hammer starts in hand (pickup fails on this project) |
| **9** Sean | *"A good start. Let's re-roll to have a variety."* | **v2** (same prompt) `motion/m2-beat9/S02-hollow-ship-it-v2.mp4` — a different gag: the cannon fires, then TOPPLES off its tripod trailing a streamer; back to us (0.986/0.949). **v3** (chair-spin variant) `…-v3.mp4` — lively, but the spin turns him to the lens and Seedance INVENTS his face mid-cheer, mouth open (0.976/0.966) | Three takes on disk. **Lean: v2** (funniest hollow, obeys the facing law); v3 flagged — the exorcist risk from 3½ |
| **10** | No note | — | v1 stands |

**Round-2 spend: 230 cr, measured** (balance 3,462.5 → **3,232.5**), 17 generations, 17 landings. Day total **487.5 cr**.

**✓S — Sean, 2026-09-05 17:38: *"These are all PERFECT. Great job."*** Beats **6, 8, 10** (one candidate each) are copied into
`_LOCKED-M2/` as 11 / 13 / 15 with their keyframes. **20:08 — Sean picked: beat 5 v3, beat 7 v2, beat 9 v2** → locked as 10 / 12 / 14 with their start
frames. **Movement 2 is fully locked, `_LOCKED-M2/` 08–15.** Committed and pushed on branch `about-me-short/m2-wave-2`.

**Spend 2026-09-03:** 76.5 credits (two plates, two face composites, five S09 composites — nine generations, nine first-roll landings). **2026-09-04:** +83 (two one-pass A/Bs, the Grok reference fix, the Grok single v2, then the two Movement-2 clips at 24.5 each). **2026-09-05:** +73.5 (the v2 pair, then GO v3 which lost to v2); Sean's own rolls (v3–v5 of both beats) took the balance to **3,720 at the wave-2 session start (measured, `higgsfield account status`)**. **Wave 2 (2026-09-05 afternoon): 257.5 cr, measured** — two beat-8 plate variants (17), beats 5/6/7 plates (25.5), five composites incl. two re-rolls (42.5), the S08 alarm-2 edit (8.5), the S02 cannon fix (8.5), six clips (147). 23 generations, 23 first-roll landings, 0 refusals. **Balance 3,462.5** (`higgsfield account status`, matches the running total to the credit). Everything owed Sean's eye; nothing locked.
**Normaliser note:** `post/normalize_paper.py` needs numpy — run it with the repo venv,
`/Users/seanwinslow/Code-Brain/anima/.venv/bin/python`, not the bare `python3` (3.14, no numpy).

---

## Movement 3 setups — wave 3, 2026-09-06 (beats 11–20; tracked here until an M3 board file exists)

Session run under `/creative-director` from [`CONTINUATION-2026-09-05-movement-3-wave-3.md`](CONTINUATION-2026-09-05-movement-3-wave-3.md).
**33 generations, 33 first-roll landings, 0 refusals, 0 re-rolls — 372 cr measured** (balance 3,232.5 → **2,860.5**, `higgsfield account status`,
matches to the credit). **Price correction:** `gpt_image_2` 2k high billed **6.5 cr** per image this session, not the 8.5 every doc carries;
seedance fast 7s 720p is still 24.5. **Nothing is locked** — every package below is owed Sean's eye. The whole movement is assembled at $0
as a labelled rough cut: **`motion/m3-roughcut/M3-roughcut-v1.mp4`** (43.6s vs the 37s target; trims are a first guess) + `-sheet.png`.

**Phase 0 catch:** question 1 (typed or spoken) is not open — the studio brief's own non-negotiable was amended 2026-08-31 to *"never speaks
aloud"*; the "confirm or override" flag above (§ Spatial authority) is stale. Typed. **Geometry catch:** the NE hole is BEHIND the S09 lens
(ground plan), so a beat-11 S09 wide can carry three of the four wrecks, not four.

| Beat | Setup | Still(s) | Motion | State / the question for Sean |
|---|---|---|---|---|
| **11** record scratch | *open* — Q2 | $0 roughs: `m3-roughs/Q2-A-freeze-cut.jpg` (route A: four locked mid-action frames cut scratch-scratch-scratch, $0) · `m3-roughs/Q2-B-S09-stateB-annotated.jpg` (route B: the S09 wide re-dressed to state B, everyone frozen mid-action — a still that is never animated is exempt from the rest-pose law; 6.5 + Sean's web-app kit) | route A plays in the rough cut as the placeholder | **Lean: B** — the only shot that shows the SUM; A is the honest $0 fallback and is already cut in. Sean picks |
| **12** THE SWIVEL | S10 | **✓ v1** `normalised/S10-sean-swivel-v1.png` (6.5, first roll): eyes closed, small closed mouth, palms down over the armrests, feet flat. $0 push-in alternative that drops the telescope: `m3-roughs/B12-swivel-pushin-crop.png` | **✓ v1** `motion/m3-beat12/S10-sean-swivel-v1.mp4` (24.5, first roll): opens side-on with the face already in profile, eyes shut → rotates square → holds ~4.5s → shoulders lift/sink → eyes OPEN on the last beat looking at the crew. **Mouth held closed throughout** (`-FACE-sheet.png`). Layout f0 0.891 (the turn) / last 0.987 | Prompts `composites-M3/S10-sean-swivel-eyes-closed.txt`, `motion/41`. **Telescope nit** at frame right (accept / 6.5 edit / the $0 crop). Sean's eye owed |
| **13** the question | S02 + **S11** (new) | **✓ S11 plate** `normalised/S11-monitor-closeup-v1.png` (6.5; S02 bible + `m3-roughs/S11-crop-w1000.png` as the camera rough; no chair; the normaliser over-gains it — raw plate used) → **✓ chat box** `normalised/S11-chat-box-v1.png` (6.5, first roll): **the full sentence landed**, hand-lettered, USER avatar in the header, cursor in the entry box | **✓** `motion/m3-beat13/S02-sean-types-v1.mp4` (24.5, first roll; 0.981/0.982 — one nit: his head turns towards profile mid-clip) + **$0 post typewriter** `motion/m3-beat13/S11-chat-typewriter-v1.mp4` (`post/typewriter_reveal.py`, 3.2s + 1.5s hold) | Prompts `plates-rev2/S11-monitor-closeup.txt`, `edits/S11-chat-box-the-question.txt`, `motion/40`. Sean's eye owed |
| **14** THE REPLAY | S08 | $0 layout rough `m3-roughs/B14-replay-page-rough.png` → **✓** `normalised/S08-replay-page-v1.png` (6.5, first roll): the cluttered shop page in dash-text, the TINY grey buy button bottom-right; the model dropped the cookie bar | **$0 post cursor** `motion/m3-beat14/S08-replay-cursor-v1.mp4` (`post/cursor_overlay.py`: a drawn arrow on a 10-waypoint path with three circling loops, held on twos, never enters the bottom-right corner; 7s, loopable) | Prompt `edits/S08-replay-checkout-page.txt`. The page design answers "what does *can't find the buy button* look like": all clutter, the button tiny. Sean's eye owed |
| **15** the sigh | S03/S04/S05 **state C** + the NE bible | **✓ three state-C plates** as edits of the locked M1 plates (`normalised/S0{3,4,5}-stateC-v1.png`, 6.5 each, first roll; law 1) → **✓ three composites** `normalised/S0{3,4,5}-{claude,codex,gemini}-stateC-v1.png` (6.5 each, first roll; Claude sitting writing, one pencil; Codex face tipped up; Gemini beside the buried table). Grok's start = `_LOCKED-M2/13_beat8_S06B_end-frame.png`, $0 | **✓ four clips** `motion/m3-beat15/S0{3,4,5,6B}-*-sigh-v1.mp4` (98, all first roll): each a puff-up → puddle-slump → bob → grin. **Grok's is the best acting of the wave** (a real sad face over the hammer). Layouts 0.989/0.984 · 0.988/0.989 · 0.865/0.865 (Gemini's busy plate defeats the correlation, not a re-camera) · 0.990/0.990 | Prompts `plates-rev2/S0{3,4,5}-stateC-*.txt`, `composites-M3/S0{3,4,5}-*-stateC.txt`, `motion/42–45`. Sean's eye owed |
| **16** THE PIT STOP | the same four start frames | Grok's **old button** START/END edits written and **HELD for Q3** (`edits/S06B-old-button-{START,END}.txt`; rough `m3-roughs/Q3-old-button-rough.jpg`) | **✓ three clips** `motion/m3-beat16/S0{3,4,5}-*-pitstop-v1.mp4` (73.5, all first roll): the micro-task is the FIRST event, one snap, settle, repeat — complete inside ~1.5s without an absolute time cue. Grok's 2kf (`motion/49`) written, **held** | **Lean for Q3: the person-sized BUY button** (the replay's tiny button blown up into a thing you can hit). Sean says yes → 13 cr + 24.5. Sean's eye owed on the three |
| **17** the earned SHIP IT | S08 + S02 | **✓** `normalised/S08-graph-rockets-v1.png` (6.5, first roll): the line rockets off the top right, no words | **✓** `motion/m3-beat17/S08-graph-rockets-v1.mp4` (24.5, 2kf, first roll; 0.995 vs dark / 0.993 vs rocket — the beat-10 twin) + **✓** `motion/m3-beat17/S02-earned-ship-it-v1.mp4` (24.5, first roll; a fountain of confetti, the bell swings, his back to us; 0.985/0.961) | Prompts `edits/S08-graph-rockets.txt`, `motion/50`, `motion/51`. Sean's eye owed |
| **18** the USER colorizes | S08 | the two locked stills | **✓** `motion/m3-beat18/S08-user-colorizes-v1.mp4` (24.5, 2kf, first roll): grey holds → **the green travels up the CABLE into the set** (the model's own gag) → the figure floods green → grin + thumb SNAP on → beams. 0.982/0.972 vs grey, 0.965/0.983 vs green. **Colour change by keyframes is proven on this route** | Prompt `motion/39`. **Rolled first, as the doc ordered.** The green cable: charming or a nit — Sean's call |
| **19** THE BUTTON | — | hold on `refs/user-looktest/S08-green-v2.png` | post (the rough cut holds it 4s) | nothing to generate |
| **20** the sting | S08 | **✓** `normalised/S08-alarm3-v1.png` (6.5, first roll): **PROBLEM!** on the S08 framing (Q4's lean, taken; `(STILL!)` exists at $0 if overruled) | post: still 0.4s → red flood 0.15s → black (the rough cut does a first pass) | Prompt `edits/S08-alarm3-problem-sting.txt` |

**$0 tools this wave:** `post/fetch_result.py` (job json → file; refuses an empty `[]`), `post/cursor_overlay.py`, `post/typewriter_reveal.py`,
`post/m3_roughcut.py` (the SHOTS table is the edit; re-run after any change).

### Sean's rulings on wave 3 — 2026-09-06 10:51 (recorded; the next session executes from `CONTINUATION-2026-09-06-wave-3b-fixes.md`)

**✓S:** beat 12 (the swivel v1), 13.3 (the chat box + typewriter; Sean crops in CapCut), 14 (the replay page + post cursor), 16.5 ×3 (Claude /
Codex / Gemini pit stops), 18 (the colorize), 19 (the green hold). **Released, kept:** the beat-13 typing clip; both beat-17 clips + the graph
edit; the PROBLEM! sting still. **Banked elsewhere:** the four v1 sighs → beat-10.5 "sighs of distress" candidates. **Re-do:** beat 15 as
RELIEF, 5s each. **New:** beat 11 = a super wide of the wrecked room recreating `art-viz/route-c--gpt-ref.png` (not the CRT POV; map the
cast first); 13.1 monitors-POV medium (calm turn, eyes open on the lens); 13.2 extreme close-up of the hands typing; 16 = Sean facing us on
the S02 framing, smiling, delegating by pointing, 10s; 17 = an extreme close-up of a SHIP key pressed (start + end frame); 18.5 = the S09
wide in state C, the team cheering in their corners; 20 = ANOTHER PROBLEM!. **Q3 = yes** (roll the old button). Five assumptions to confirm
are listed at the top of the 3b continuation.

## Movement 3 setups — wave 3b, 2026-09-06 (beats 10.5–20 executed from Sean's 10:51 rulings + 13:53 answers)

Session run under `/creative-director` from [`CONTINUATION-2026-09-06-wave-3b-fixes.md`](CONTINUATION-2026-09-06-wave-3b-fixes.md). **`_LOCKED-M3/` created**
(the ✓S packages copied in; numbering `NN_beatB.B_Sxx_slug` from 16, gaps reserved — see its README). The duration argument landed on both runners
(`generate.sh <prompt> <start> <out.json> [secs]`, `generate2kf.sh … [secs]`); **3.5 cr/s confirmed at 5s (17.5) and 10s (35)**. The three new Sean
cameras were roughed at $0 first ([`room-bible/m3-candidates/sheets/`](room-bible/m3-candidates/sheets/) — S15 A/B/C, S19 A/B, S16 A/B). **The S15 pick
(A cutaway vs B spilled-centre) is Sean's gate; everything else ran on the A leans.** Prices: gpt_image_2 6.5, seedance fast 3.5 cr/s.

| Beat | Setup | Still(s) | Motion | State / the question for Sean |
|---|---|---|---|---|
| **10.5** Sean alone notices | **S19** (new: the S09 line pushed in, camera A) | **✓ plate** `normalised/S19-side-closeup-v1.png` (6.5, first roll) → **✓ BEFORE** `normalised/S19-sean-before-v1.png` (fists up, ¾ back; 6.5, first roll) → **AFTER** `normalised/S19-sean-after-v1.png` (looks up-right at the CRT, confused; 6.5) | 2kf clip `motion/m3-beat10h/S19-sean-notices-v1.mp4` (`motion/59`, 24.5) | **✓S 17:55 → `_LOCKED-M3/16`** (*"This is great, Locked."*). Prompts `plates-rev2/S19-side-closeup.txt`, `composites-M3/S19-sean-BEFORE-fists-up.txt`, `edits/S19-sean-AFTER-looks-up.txt` |
| **11/12** the super wide | **S15** (new) | $0 roughs A / B / C sheeted; **plate prompt written for A** (`plates-rev2/S15-A-super-wide-cutaway.txt`, held) | — | **Sean 17:55: "I agree with A, but generate B as well … I would like to see both."** **✓ both plates** `normalised/S15-A-plate-v1.png` (the cutaway) + `S15-B-plate-v1.png` (the real lens), 6.5 each, first roll. The chain runs on A (`prompts/composites-S15/S15-A-1..5`): Claude ✓ → Grok → Sean → Codex → Gemini → the 7s clip. B held. **S10 swivel ✓S → `_LOCKED-M3/18`** |
| **13.1** turns back, eyes open on us | **S16** (new: the monitors' POV, camera A) | **✓ plate** `normalised/S16-monitors-pov-v1.png` (6.5, first roll — the keyboard along the bottom, the wreck behind) → **✓ still** `normalised/S16-sean-eyes-closed-v1.png` (square to the lens, eyes shut, hands on the armrests; 6.5, first roll) | clip `motion/m3-beat13/S16-sean-eyes-open-v1.mp4` (`motion/58`, 24.5) | **Sean 17:55: "looking great" — approved PENDING one composite:** once the 11/12 freeze frame is chosen, the mascots visible from this lens (Gemini at the far wall, Codex at the rack) must be FROZEN in the background in the same poses as the freeze — an edit of the S16 still, then a re-roll of the clip off it. Prompts `plates-rev2/S16-monitors-pov.txt`, `composites-M3/S16-sean-eyes-closed-facing-lens.txt` |
| **13.2** the hands | **S17** (new insert) | **✓** `normalised/S17-hands-closeup-v1.png` (6.5, first roll; hands at rest, blank keys) | **✓** `motion/m3-beat13/S17-hands-v1.mp4` (24.5, first roll; 0.979/0.980): a few keys, a pause, a few more, one Enter reach — calm | **✓S 17:55 → `_LOCKED-M3/20`** (*"perfect. Locked."*) |
| **13.3** the chat box | S11 | ✓S → `_LOCKED-M3/21` | ✓S (typewriter) | locked |
| **14** THE REPLAY | S08 | ✓S → `_LOCKED-M3/22` | ✓S (cursor) | locked |
| **15** the RELIEF sighs | S03/S04/S05 state C + S06B | the same four start frames | **✓ four 5s clips** `motion/m3-beat15/S0{3,4,5,6B}-*-relief-v2.mp4` (17.5 each, all first roll): the held breath → the whoosh → brow-wipe → hop → beam. Layouts 0.987/0.976 · 0.992/0.993 · 0.901/0.902 (busy plate) · 0.990/0.991 | Prompts `motion/52–55`. **✓S 17:55 → `_LOCKED-M3/23–26`** (*"all are great. Locked."*; the Codex balloon accepted). The v1 distress sighs stay banked in the same folder |
| **16** the delegation | S02 rev-2 (the cannon-fix frame) | **✓** `normalised/S02-sean-delegation-v1.png` (6.5, first roll — the chair TURNED with him, smiling, hands on the armrests) | **✓ 10s** `motion/m3-beat16/S02-sean-delegation-v1.mp4` (35, first roll; 0.983/0.983): four distinct point-and-nods (far-left / down-left / at the lens / far-right) + the open-hands settle — **no slow motion on the sheet** | **Sean 17:55: re-roll — the face must follow the finger and the lips must move (mime).** Two re-rolls on disk: **v2** `motion/m3-beat16/S02-sean-delegation-v2-mime.mp4` (the calm still + the mime prompt `motion/56b`; 35, first roll; 0.972/0.972 — the face alive, mouth open at every point, grin at the settle) and **v2b** `…-v2b-determined-mime.mp4` (the determined still `normalised/S02-sean-delegation-determined-v1.png`, 6.5, + the same prompt; 35, first roll; 0.977/0.977). Sean picks; route C (dialogue with audio on, cut in post) unspent. The cannon-upright continuity question stands |
| **16.5** the pit stops | S03/S04/S05 + **S06B** | Claude/Codex/Gemini ✓S → `_LOCKED-M3/28–30`. **Grok: ✓ BUY button START** `normalised/S06B-old-button-start-v1.png` + **✓ END** `-end-v1.png` (6.5 each, first roll) | **✓** `motion/m3-beat16/S06B-grok-pitstop-v1.mp4` (24.5, 2kf, first roll; 0.986 / 0.989): hoist, smash, dust, B U Y, hop, dusts hands | **✓S 17:55 → `_LOCKED-M3/31`** (*"Looks perfect. Locked."*) |
| **17** the SHIP key | **S18** (new insert) | **✓ START** `normalised/S18-ship-key-start-v1.png` (6.5; recovered by job ID after a 503 on create) + **✓ END** `normalised/S18-ship-key-end-v1.png` (6.5; the edit re-rendered the key cluster, so the screen_swap paste was skipped) | 2kf clip `motion/m3-beat17/S18-ship-key-v1.mp4` (`motion/60`, 24.5) | **✓S 17:55 → `_LOCKED-M3/32`** = the single-image v2 (the packet's lean; the 2kf v1 kept in `motion/m3-beat17/`). Both old beat-17 clips released, kept |
| **18** the USER colorizes | S08 | ✓S → `_LOCKED-M3/33` | ✓S | locked |
| **18.5** the celebration | S09 state C | **✓ state-C plate** `normalised/S09-stateC-v1.png` (6.5, first roll; the chained-route base, unused) → **✓ the twin, route (a)** `normalised/S09-webapp-stateC-v1.png` (6.5, first roll): the locked five-character composite with the room wrecked around them — the five held by eye | clip `motion/m3-beat18h/S09-team-celebrates-v1.mp4` (`motion/61`, 24.5) | Prompts `plates-rev2/S09-stateC-wreck.txt`, `plates-rev2/S09-webapp-stateC-twin.txt`. Route (a) = one edit of Sean's own composite instead of five chained edits. **✓S 17:55 → `_LOCKED-M3/34`** (*"perfect! Locked."*) |
| **19** THE BUTTON | S08 | ✓S → `_LOCKED-M3/35` | post | locked |
| **20** the sting | S08 | **✓** `normalised/S08-alarm4-v1.png` (6.5, first roll): **ANOTHER PROBLEM!** | post: still → red flood → black | **Sean 17:55: the still is great; transition from the green USER with a flash + shake like beat 3.** **✓** `motion/m3-beat20/S08-sting-transition-v1.mp4` (`motion/62`, 2kf green → ANOTHER PROBLEM!, 5s, 17.5, first roll; 0.991/0.991): holds, one white flash, bangs on, the set rocks, the cable swings, holds. Instant black is post. Prompt `edits/S08-alarm4-another-problem.txt`. PROBLEM! superseded, kept |
