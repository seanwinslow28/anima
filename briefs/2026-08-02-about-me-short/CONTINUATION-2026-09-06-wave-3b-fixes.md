# CONTINUATION — Movement 3, wave 3b: Sean's rulings on the wave-3 packages, and the beats still owed

**Start this session by invoking the skill:**

```
/Users/seanwinslow/Code-Brain/anima/.claude/skills/creative-director/SKILL.md
```

Sean asked for it by name. Its job here: **help him execute his rulings below on Movement 3 — beats 11 through 20 — with a
2D animation director's creative taste and timing.** Not to re-plan the pipeline, not to re-open anything ruled, not to re-run
the interview. Let **Phase 0** run: it reads this brief, the Movement 3 table at the foot of [`M1-STORYBOARD.md`](M1-STORYBOARD.md),
[`CONTINUATION-2026-09-06-wave-3-review.md`](CONTINUATION-2026-09-06-wave-3-review.md) (what was built and what each number
means), [`prompts/_blocks.md`](prompts/_blocks.md) (**laws 1–25**, all paid for; 15–25 are this movement's), and the M3 prompt
headers `prompts/motion/39–51` (each carries its result + diagnosis). Then it states back the register, the route, the per-unit
cost and the standing laws before proposing anything. Then **Phase 2**: for each open item below, 2–3 routes with a named
specific, a cost in credits, and a stated lean — **shown, not described** (rough it at $0 with the room bible, crop it, roll a
look-test) because Sean cannot judge staging from prose.

The visual guides at `.claude/skills/creative-director/references/visual-guides/` are the calibration. This wave leans on
`staging-silhouette-test.png` and `line-of-action.png` (the beat-16 delegation is a pointing pose that must read across a
room), `eye-lead-head-turn.png` (13.1 is a head turn + an eye open), `anticipation-action-settle.png` (every sigh of relief is
one whole beat; the SHIP key press is one whole beat), and `rest-pose-vs-mid-action.png` (every new still is a destination).

Working directory: `/Users/seanwinslow/Code-Brain/anima/briefs/2026-08-02-about-me-short`

**Git, at the start:** branch `about-me-short/m3-wave-3` carries three commits (record `3c2ba97`, `ca79953`; media `5abcc03`)
on top of `main`'s `a5ddbef`. **Stay on that branch** (or branch `about-me-short/m3-wave-3b` off it), commit record and media
separately, expect Sean to squash-merge. Unrelated edits under `briefs/2026-07-02-grandmaster/` and two skill folders are not
this project's — leave them out. **Balance 2,860.5** (measured 2026-09-06 06:41) — confirm with `higgsfield account status`.

**Prices, measured this wave (law 24):** `gpt_image_2` 2k high = **6.5** cr/image (not the 8.5 older docs carry);
`seedance_2_0` fast 720p = **24.5** for 7s (≈3.5 cr/s — so 5s ≈ 17.5, 10s ≈ 35; confirm the per-second rate on the first roll).
**The runners (`motion/generate.sh`, `generate2kf.sh`) hardcode `--duration 7`** — add a duration argument (default 7) before
rolling the 5s sighs or the 10s delegation. `higgsfield model get seedance_2_0` lists `duration` as an integer (default 5);
**read the allowed range off it before promising 10s.**

---

## ASSUMPTIONS TO CONFIRM WITH SEAN FIRST (five; each changes the work)

1. **Beat 11 — where is Sean in the wide?** Lean **A**: at his desk, back to the room, frozen like everyone; the swivel stays
   beat 12. (**B**: the wide IS the inspiration — Sean already turned, eyes closed, palms out — and beat 12 becomes the
   close-up of that pose with the swivel clip's opening turn trimmed.)
2. **Beat 11 — staging.** The inspiration's camera is on the SOUTH wall looking north (doorway left, CRT + hole right), which
   puts Codex's rack and Gemini's board BEHIND the lens. The inspiration solves it by crowding everyone into the middle around
   Sean's desk mid-chaos. Lean: **that** — chaos spilled to the centre, each mascot carrying its own wreck (pages, a popped
   screen, sketches, the hammer) — rather than a wider-than-real lens. Rough both from the room bible; Sean picks.
3. **Two ensemble wides, two web-app kits.** Beat 11 (new south-wall camera, frozen) and beat 18.5 (the S09 CRT camera, state
   C, celebrating) each need all five characters; the proven five-character route is Sean's web-app pass on a kit
   (`prompts/composites-S09/README.md` — singles + matte failed twice, one-pass conflated). Lean: keep both (18.5 rhyming with
   the 3½ reaction shot is worth it). Build both kits; hand them over.
4. **Beat 12's cut point.** With 13.1 being "he opens his eyes on the monitors", end beat 12 BEFORE his eyes open (the clip's
   last ~1s), so the eyes open once, on the screen, as the decision. Lean: yes.
5. **Beat 16 at 10s.** Confirm the model's max duration from the CLI; write the delegation as FOUR distinct point-and-nod beats
   (Claude, Codex, Gemini, Grok) so 10s cannot stretch into slow motion (law: one action given 7s gets spread across 7s).

---

## SEAN'S RULINGS — 2026-09-06 10:51, verbatim where it matters. Do not re-litigate.

| Beat | Ruling | State |
|---|---|---|
| **11** record scratch | *"recreate the inspiration for this whole short"* — [`art-viz/route-c--gpt-ref.png`](art-viz/route-c--gpt-ref.png): **a super wide of the WRECKED room, NOT from the CRT alarm POV.** *"We would just have to map out how everyone is positioned in the room before generating anything."* | **OPEN** — a new camera (propose id **S15**), solved in the room bible at $0 first; then the state-C plate; then the kit |
| **12** THE SWIVEL | *"The swivel looks good. We'll keep that."* | **✓S** `motion/m3-beat12/S10-sean-swivel-v1.mp4` (start `normalised/S10-sean-swivel-v1.png`). Telescope nit unaddressed — Sean did not raise it |
| **13** the question | *"We're not using [the typing clip]. We need this to be more calm with close up shots in between this moment and Beat 14 … This is the moment that Sean keeps his composure."* Three shots: **13.1** Sean's-computer-monitors-POV MEDIUM — Sean turns round with the calm still on his face, opens his eyes, looks at the camera (= the monitors). **13.2** EXTREME CLOSE-UP of Sean's hands typing on the keyboard. **13.3** the chat box (`normalised/S11-chat-box-v1.png` + `motion/m3-beat13/S11-chat-typewriter-v1.mp4`) *"is perfect. I'll crop in using CapCut so we don't see his desk."* | 13.3 **✓S**. 13.1 + 13.2 **OPEN** (two new setups). `S02-sean-types-v1.mp4` **released** (kept on disk) |
| **14** THE REPLAY | *"This works perfectly. This is locked."* | **✓S** `normalised/S08-replay-page-v1.png` + `motion/m3-beat14/S08-replay-cursor-v1.mp4` |
| **15** the sigh | *"All of those look great and I want to keep them because I might add them as a beat 10.5 as sighs of DISTRESS … this is meant to be a sigh of RELIEF. They're all supposed to look happy, not upset. Re-roll all of them using Seedance 2.0 fast at 5 seconds for each character. I'll cut them down in post."* | the four v1 clips **banked as beat-10.5 candidates** (do not delete). **OPEN**: four RELIEF re-rolls, **5s**, same state-C start frames |
| **16** the delegation | *"a medium shot of the Sean character smiling and approving. He understands what to do now. It's time for him to properly delegate tasks to each mascot. Sean points at each character assigning their roles."* Framing: [`plates/S02-sean-desk-v2-dressed.png`](plates/S02-sean-desk-v2-dressed.png) — *"We just need to have the Sean character facing towards the camera and make it so that it matches what his desk looks like now. This will be set to 10 seconds so we have room to breathe."* | **OPEN** — a new composite on the S02 framing (the rev-2 desk + the fixed cannon = "now"; the old dressed plate still shows the telescope) + a 10s clip |
| **16.5** the pit stop | *"I've reviewed the pitstops and they're perfect, so no need to re-roll Claude, Gemini, and Codex. For Grok, Yes, I like the idea for Q3. Roll that."* | Claude/Codex/Gemini **✓S** (`motion/m3-beat16/`). **Grok OPEN → ROLL**: `prompts/edits/S06B-old-button-START.txt` → `-END.txt` → `prompts/motion/49` (2kf). 13 + 24.5 |
| **17** the earned SHIP IT | *"We won't go with the twin. It feels off. I think we do one extreme closeup of Sean's keyboard. The key on the keyboard says 'SHIP' — the motion is Sean's finger presses down on it. We can generate a start frame and end frame."* | **OPEN** — a new insert setup (start: finger resting beside/over the SHIP key; end: the key pressed down) + a 2kf clip. The graph clip + the earned-ship-it clip are **released** (kept) |
| **18** the USER colorizes | *"Locked."* | **✓S** `motion/m3-beat18/S08-user-colorizes-v1.mp4` (+ the two locked stills) |
| **18.5** the celebration | *"Visual twin of `normalised/S09-all-webapp-v2.png` — but the room is looking like the big mess they just created … each character's corner is the way they were within the chaos of wave 3. The motion: the whole team celebrating and cheering in their corners."* | **OPEN** — the S09 plate re-dressed to **state C** (an edit of `normalised/S09-room-reacts-v1.png`, law 1) → the five-character kit for Sean's web app → one 7s clip |
| **19** THE BUTTON | *"Back to the User smiling and the VO."* | **✓S** a hold on `refs/user-looktest/S08-green-v2.png` — post |
| **20** the sting | *"Regenerate an image that says ANOTHER PROBLEM! in the same frame. Then we cut to black."* | **OPEN → ROLL**: an S08 edit, `ANOTHER PROBLEM!` in the beat-3 design; `S08-alarm3-v1.png` (PROBLEM!) is superseded, kept |

**Released, kept on disk with their diagnoses:** `motion/m3-beat13/S02-sean-types-v1.mp4`, `motion/m3-beat17/S08-graph-rockets-v1.mp4`,
`motion/m3-beat17/S02-earned-ship-it-v1.mp4`, `normalised/S08-graph-rockets-v1.png`, `normalised/S08-alarm3-v1.png`. Their prompt headers
get a `# RELEASED 2026-09-06 (Sean): …` line.

---

## THE ORDER OF WORK — a 30 / 60 / 90 for wave 3b

**0% — the locks and the record ($0, first).** Create `_LOCKED-M3/` and copy in what Sean approved: beat 12 (clip + start still),
13.3 (chat still + typewriter clip), 14 (page still + cursor clip), 16.5 ×3 (clips + start stills), 18 (clip + both stills), 19 (the
green still). **Naming:** the M1/M2 running numbers break on sub-beats (13.1, 16.5, 18.5) — propose `NN_beatB.B_Sxx_slug` with NN
continuing from 16 in playback order and leave gaps for the open beats; write the README the way `_LOCKED-M2/README.md` is written;
say the scheme changed and why. Update every ✓S row in the tracker. Mark the four v1 sighs as beat-10.5 candidates.

**30% — Rough ($0 then cheap).** Two things prove the wave:
1. **Beat 11's camera, mapped before anything is generated** (Sean's explicit condition). Extend `room-bible/m2_candidates.py` /
   `make_shot_roughs.py` with 2–3 south-wall super-wide candidates (S15-A/B/C: centre of the south wall at eye level; a high
   south-east corner; a low south-west corner), each rendering a plate rough AND a cast rough with the five figures placed
   **per assumption 2** (crowded to the centre around the desk, each with its wreck) — the green blocks are the "map out how everyone
   is positioned" Sean asked for. Sheet them; Sean picks; **then** the state-C plate (ELEV-north + ELEV-east + ELEV-west as bibles +
   the chosen rough as camera; the wreck described from the three state-C corner plates + the NE bible; 6.5) and the kit.
2. **The Grok pit stop** (Q3 is a yes): START edit → END edit → 2kf. 37.5. Proves the two-keyframe prop-destruction shape.

**60% — Structure.** The three new Sean setups, all destination stills first (rest-pose + facing laws), then one clip each:
- **13.1 — the monitors' POV medium (propose S16):** camera at desk height between the monitors looking at Sean's face; a new plate
  (the S02 plate as bible, a `make_closeup.py` crop of the S10 composite as a camera hint will NOT do — it is a re-angle; use the room
  bible + a rough). Still: Sean in the chair **already facing the lens, eyes closed, calm** (the beat-12 trick, law 16); clip: the
  last degrees of the turn, then his eyes open on the lens. Zero typing. 6.5 + 6.5 + 24.5.
- **13.2 — the hands (propose S17):** an extreme close-up insert of the keyboard with both hands at rest on the keys (a rest pose);
  clip: slow, deliberate typing — a few keys, a pause, a few keys, one soft Enter. **Calm is the note.** Hands are a model risk:
  keep the hands still in the still, ask for "slow" via few events (law: fewer events = slower), never "slowly". 6.5 + 24.5.
- **16 — the delegation (S02 framing, Sean facing us):** the composite is a NEW Sean pose on the rev-2 S02 plate (`normalised/S02-plate-v1.png`
  + the fixed cannon from `S02-cannon-fix-v1` if the frame includes it): chair turned to us, smiling, calm, one hand resting — the
  pointing happens in the clip. Facing law: a front view from the S02 camera means his face carries a 10s clip — the S10 face
  look-test is the precedent that it can. Clip: four distinct point-and-nod beats (left, far-left, right, far-right — map them to
  where each mascot's corner is FROM THIS CAMERA: Claude NW = frame-left/far, Codex SW = behind-left, Gemini S = behind-right,
  Grok NE = frame-right/far), a small approving nod after each. 6.5 + ~35.
- **15 — the four relief sighs at 5s:** same start frames (`normalised/S0{3,4,5}-*-stateC-v1.png`, `_LOCKED-M2/13_beat8_S06B_end-frame.png`).
  The acting is the OPPOSITE arc from v1: shoulders up (the held breath) → a big happy exhale, shoulders drop, eyes close, a smile →
  a little hop or a brow-wipe → beam. Happy faces stated as constants. ~17.5 each.
- **17 — the SHIP key (propose S18):** an extreme close-up insert of a keyboard whose one big key reads SHIP; START: a finger resting
  beside it; END: the key pressed down under the finger (a `screen_swap`-style END built from the START so only the key changes —
  law 10 + the S07 lesson). 6.5 + 6.5 + 24.5.
- **20 — ANOTHER PROBLEM!:** an S08 edit; 6.5.

**90% — Polish.** Beat 18.5: the S09 state-C plate (edit of the locked S09 plate — the code wall/popped screen, the canyon, the fifty
on the left wall, Grok's rubble at the right edge; 6.5) → the five-view kit for Sean's web app (the S09 kit precedent, incl. the
DESCRIBED one-pass prompt) → after his composite lands, one 7s clip: five characters cheering in place, each a whole beat, faces as
constants. Then re-run `post/m3_roughcut.py` with the real beats 11, 13.1/13.2, 15, 16, 17, 18.5, 20 and the trims Sean's CapCut cut
implies, and the stopwatch table-read (#206) against the 2:00 ceiling with the 5s pit stop and the 6s replay as the hard floors.

**Every wrong-build corner still starts from a rest pose, ¾ front, face visible, eyeline on the task, one face constant per
character in the "the same … in every frame" form. The Grok identity line is verbatim. Zero negation. Register and vocabulary
blocks verbatim. New this wave: a duration argument on the runners; a happy face is a constant like any other.**

## MEASUREMENT — $0, a tripwire, never a verdict

```
post/layout_hold.py  <start.png> <clip.mp4>     # ≥0.95 both ends is the bar; run vs BOTH keyframes on a 2kf clip
                                                #   (law 23: reads ~0.87 on the sketch-buried S05 plate — not a re-camera)
post/verify_edit.py  <plate> <edit>             # a wreck-edit reads CHECK by construction (law 1)
post/normalize_paper.py <png>                   # → normalised/ (repo venv). Law 23: a closeup with NO WALL in the top band
                                                #   (S11, any keyboard/hands insert) over-gains — use the raw plate, say so
post/fetch_result.py <job.json> <out>           # refuses an empty [] (law 5: a dropped wait, not a failed job)
post/m3_roughcut.py  <out.mp4>                  # the SHOTS table is the edit
ffmpeg -i clip.mp4 -vf "fps=12/7,scale=480:-1,tile=4x3" -frames:v 1 sheet.png   # the contact sheet Sean reads (adjust fps=12/<dur>)
```

Sean's eye has now overruled the metrics **eight** times on this project (the S05 layout reads this wave). Put the picture in
front of him — the contact sheet plus the mp4 path — before writing a verdict.

## WORKING DISCIPLINE

**Sean directs. Propose with a stated lean and let his eye decide. Lock nothing on your own judgment.** Push every proposal to a
named specific. **Show him the picture** — rough it at $0, sheet every clip, send the file (the mp4 upload to the remote viewer
has failed twice on a socket error; say when a file is desktop-only). **Announce cost before spending it**, keep a running total,
reconcile against `account status` at the end. **Report failure straight, in the first sentence.** Check the reference before
calling identity drift. When a ruling reverses an earlier one, record why, keep the superseded artifact, say what it costs.
**After two CLI misses on the same frame, build the kit and hand it to Sean for the web app** (ensembles go straight to the kit).
Update the tracker on every generation and approval; every prompt file carries its result and diagnosis in its header; append the
laws this wave earns to `_blocks.md` and the day's entry to the root `CHANGELOG.md`. Leave a review packet at the end the way
`CONTINUATION-2026-09-06-wave-3-review.md` did.
