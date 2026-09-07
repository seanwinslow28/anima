# CONTINUATION — Movement 3, wave 3b: Sean's rulings on the wave-3 packages, and the beats still owed

**Start this session by invoking the skill:**

```
/Users/seanwinslow/Code-Brain/anima/.claude/skills/creative-director/SKILL.md
```

Sean asked for it by name. Its job here: **help him execute his rulings below on Movement 3 — beats 10.5 through 20 — with a
2D animation director's creative taste and timing.** Not to re-plan the pipeline, not to re-open anything ruled, not to re-run
the interview. Let **Phase 0** run: it reads this brief, the Movement 3 table at the foot of [`M1-STORYBOARD.md`](M1-STORYBOARD.md),
[`CONTINUATION-2026-09-06-wave-3-review.md`](CONTINUATION-2026-09-06-wave-3-review.md) (what was built, what each number means),
[`prompts/_blocks.md`](prompts/_blocks.md) (**laws 1–25**, all paid for; 15–25 are this movement's), the M3 prompt headers
`prompts/motion/39–51` (each carries its result + diagnosis), and [`prompts/composites-S09/README.md`](prompts/composites-S09/README.md)
(the five-character route's history). Then it states back the register, the route, the per-unit cost and the standing laws before
proposing anything. Then **Phase 2**: for each open item, 2–3 routes with a named specific, a cost in credits, and a stated lean —
**shown, not described** (rough it at $0 with the room bible, crop it, roll a look-test) because Sean cannot judge staging from prose.

The visual guides at `.claude/skills/creative-director/references/visual-guides/` are the calibration. This wave leans on
`staging-silhouette-test.png` and `line-of-action.png` (the beat-16 delegation is a pointing pose that must read across a room),
`eye-lead-head-turn.png` (10.5 and 13.1 are head turns + a look), `anticipation-action-settle.png` (every relief sigh and the SHIP
key press is one whole beat), `smear-from-repeated-motion.png` (Gemini's spin in the wide), and `rest-pose-vs-mid-action.png`
(every new still is a destination — except the one still in the film that never animates).

Working directory: `/Users/seanwinslow/Code-Brain/anima/briefs/2026-08-02-about-me-short`

**Git, at the start:** branch `about-me-short/m3-wave-3` carries four commits (record `3c2ba97`, `ca79953`, `7bfe957`; media `5abcc03`)
on top of `main`'s `a5ddbef`. **Stay on that branch** (or branch `about-me-short/m3-wave-3b` off it), commit record and media
separately, expect Sean to squash-merge. Unrelated edits under `briefs/2026-07-02-grandmaster/` and two skill folders are not
this project's — leave them out. **Balance 2,860.5** (measured 2026-09-06 06:41) — confirm with `higgsfield account status`.
Sean: *"That's fine on the credits, we have plenty to work with and I want to get this nailed down perfectly."*

**Prices, measured (law 24):** `gpt_image_2` 2k high = **6.5** cr/image; `seedance_2_0` fast 720p = **24.5** for 7s (≈3.5 cr/s —
5s ≈ 17.5, 10s ≈ 35; confirm the per-second rate on the first non-7s roll). **The runners (`motion/generate.sh`, `generate2kf.sh`)
hardcode `--duration 7`** — add a duration argument (default 7) before the 5s sighs or the 10s delegation. Sean: Seedance 2.0 goes
to **15s**; `higgsfield model get seedance_2_0` lists `duration` as an integer — read the range off it anyway.

---

## SEAN'S ANSWERS — 2026-09-06 13:53. These settle the five assumptions; do not re-open them.

1. **Beat 11 = the wide, Sean at his desk, back to the room — and beats 11 + 12 are now ONE sequence with a NEW beat 10.5 before them.**
   Sean: *"For Beat 10, the CRT displays PROBLEM (STILL!). For Beat 10.5 Sean is the only one that notices. He quickly looks up at
   the CRT screen … a close up angle of Sean from `normalised/S09-all-webapp-v2.png` so we can see his face look up at the screen,
   but I'll take recommendations — we'd need to generate a before and an after image. The before is the side angle of him
   celebrating the false SHIPPED celebration in Beat 9 (fists up — see `m3-roughs/B10.5-before-pose-candidates.png`, frames of
   `_LOCKED-M2/14_beat9_S02_hollow-ship-it.mp4` at 3.6/4.2/4.8s). The after is him looking up at the CRT alarm looking confused.
   For beat 11, we'd now mix it with beat 12. We cut to that extreme wide shot. Sean swivels around and looks at all of the chaos
   happening around him. The record scratch happens. Everyone freezes mid-chaotic motion. Sean takes a deep breath in, then he turns
   around and we go to 13.1, 13.2, 13.3."*
2. **Beat 11 staging — build BOTH and let his eye pick.** Sean: *"I'm leaning towards a wider than real lens, but we should also generate
   one that has the chaos spilling into the center. Codex can be tugging on a wire from the computer tower on the left and Gemini can be
   doing the crazy Tasmanian Devil spin from `_LOCKED-M2/12_beat7_S14_gemini-whirlwind.mp4` all the way to the right. Everyone should be
   properly proportioned to where they are in the room."*
3. **Ensembles: try Higgsfield first, Sean's own GPT-Image-2 workflow, one character at a time.** Sean: *"I started off by cropping out
   the character in the pose they were going to be in from a previously generated image that we already have, then creating a turnaround
   sheet like `runs/Act-Rework-Backlog/02-AI-company-character-refs/claude-turnaround.jpeg` using `prompts/turnaround-sheet/turnaround-sheet-prompt.txt`
   — then I would use GPT Image 2 to edit each character in the frame one at a time. If that doesn't work, I'll do it myself in the web app."*
   **So the route is CHAINED single-character edits** (plate → +char 1 → +char 2 …), each verified by eye before the next, with a pose-true
   turnaround view as the character ref — NOT the singles-onto-the-clean-plate + matte merge that failed twice on S09, and NOT a one-pass.
   Chaining was never tried on the CLI; the web app closed S09 exactly this way. Two misses on one character → hand Sean the kit.
4. **Beat 12's cut: yes** — end the S10 swivel clip before his eyes open; the eyes open once, on the monitors, in 13.1.
5. **Beat 16 at 10s: yes**, and *"please check the 10s is good and won't go in slow motion."* Four distinct point-and-nod beats; if the
   10s roll spreads, the honest fallback is the same events at 7s, not a rewrite.

---

## SEAN'S RULINGS — 2026-09-06 10:51, verbatim where it matters. Do not re-litigate.

| Beat | Ruling | State |
|---|---|---|
| **10.5** (NEW) Sean alone notices | A side-angle close-up of Sean at his desk, face visible: BEFORE = the beat-9 fists-up celebration seen from the side; AFTER = he looks up at the CRT, confused. Two stills → one two-keyframe clip | **OPEN** — a new setup (propose **S19**): the S09 camera's direction (from the CRT's side of the room) pushed in on Sean's desk; roughs first |
| **11 + 12** the wide, the swivel, the scratch | *"recreate the inspiration for this whole short"* — [`art-viz/route-c--gpt-ref.png`](art-viz/route-c--gpt-ref.png): **a super wide of the WRECKED room, NOT from the CRT alarm POV**; Sean swivels round to face the chaos; record scratch; everyone freezes mid-motion; he breathes in; he turns back → 13.1. The S10 swivel (*"looks good, we'll keep that"*) is the close-up of the breath, cut in after the freeze, trimmed to end before his eyes open | **OPEN** — new camera (propose **S15**), mapped in the room bible at $0 first, two stagings roughed (answer 2), then the state-C plate, the chained ensemble, and ONE 7s clip. **S10 swivel ✓S** |
| **13** the question | Three calm shots; *"This is the moment that Sean keeps his composure."* **13.1** monitors-POV MEDIUM — Sean turns round calm, opens his eyes, looks at the camera (the monitors). **13.2** EXTREME CLOSE-UP of his hands typing. **13.3** the chat box + typewriter *"is perfect. I'll crop in using CapCut."* | 13.3 **✓S**. 13.1 + 13.2 **OPEN** (propose **S16**, **S17**). The typing clip `S02-sean-types-v1.mp4` **released**, kept |
| **14** THE REPLAY | *"This works perfectly. This is locked."* | **✓S** page still + post cursor |
| **15** the sigh | *"…I might add them as a beat 10.5 as sighs of distress … this is meant to be a sigh of RELIEF. They're all supposed to look happy, not upset. Re-roll all of them using Seedance 2.0 fast at 5 seconds for each character."* (The distress sighs are a separate idea from the new 10.5 above — bank them as **"beat 10.x distress"** candidates and let Sean place them.) | four v1 clips **banked**, not deleted. **OPEN**: four RELIEF re-rolls, **5s**, same state-C start frames |
| **16** the delegation | *"a medium shot of the Sean character smiling and approving … Sean points at each character assigning their roles."* Framing: `plates/S02-sean-desk-v2-dressed.png` — *"Sean facing towards the camera … matches what his desk looks like now. 10 seconds so we have room to breathe."* | **OPEN** — a new composite on the rev-2 S02 framing (`normalised/S02-plate-v1.png` + the fixed cannon = "now"; the old dressed plate still shows the telescope) + a **10s** clip |
| **16.5** the pit stop | *"they're perfect, so no need to re-roll Claude, Gemini, and Codex. For Grok, Yes, I like the idea for Q3. Roll that."* | Claude/Codex/Gemini **✓S**. **Grok → ROLL**: `prompts/edits/S06B-old-button-START.txt` → `-END.txt` → `prompts/motion/49` (2kf). 13 + 24.5 |
| **17** the SHIP key | *"We won't go with the twin. It feels off. One extreme closeup of Sean's keyboard. The key says SHIP — Sean's finger presses down on it. Start frame and end frame."* | **OPEN** (propose **S18**): START = a finger resting beside the SHIP key; END = the key pressed down under it; 2kf clip. Both beat-17 clips + the graph edit **released**, kept |
| **18** the USER colorizes | *"Locked."* | **✓S** |
| **18.5** the celebration | *"Visual twin of `normalised/S09-all-webapp-v2.png` — but the room is looking like the big mess they just created … each character's corner the way they were within the chaos of wave 3. The motion: the whole team celebrating and cheering in their corners."* | **OPEN** — the S09 plate re-dressed to **state C** (edit of `normalised/S09-room-reacts-v1.png`, law 1) → the chained ensemble (answer 3) → one 7s clip |
| **19** THE BUTTON | *"Back to the User smiling and the VO."* | **✓S** the green hold — post |
| **20** the sting | *"Regenerate an image that says ANOTHER PROBLEM! in the same frame. Then we cut to black."* | **OPEN → ROLL**: an S08 edit; `S08-alarm3-v1.png` (PROBLEM!) superseded, kept |

**Released, kept on disk with their diagnoses:** `motion/m3-beat13/S02-sean-types-v1.mp4`, `motion/m3-beat17/S08-graph-rockets-v1.mp4`,
`motion/m3-beat17/S02-earned-ship-it-v1.mp4`, `normalised/S08-graph-rockets-v1.png`, `normalised/S08-alarm3-v1.png`. Each prompt header
gets a `# RELEASED 2026-09-06 (Sean): …` line.

**The M3 running order is now:** 9 → 10 (CRT, PROBLEM (STILL!)) → **10.5** (Sean looks up, side) → **11/12** (the wide: swivel, scratch, freeze) →
**12** (S10 close: eyes closed, the breath) → **13.1** (monitors POV: turns back, eyes open on us) → **13.2** (hands) → **13.3** (the chat box) →
14 → **15** (four relief sighs) → **16** (delegation, 10s) → **16.5** (four pit stops) → **17** (SHIP key) → 18 → **18.5** (celebration wide) → 19 → 20.

---

## THE ORDER OF WORK — a 0 / 30 / 60 / 90 for wave 3b

**0% — the locks and the record ($0, first).** Create `_LOCKED-M3/` and copy in what Sean approved: beat 12 (clip + start still), 13.3 (chat
still + typewriter clip), 14 (page still + cursor clip), 16.5 ×3 (clips + start stills), 18 (clip + both stills), 19 (the green still).
**Naming:** the M1/M2 running numbers break on sub-beats — propose `NN_beatB.B_Sxx_slug` with NN continuing from 16 in playback order and
gaps left for the open beats; write the README the way `_LOCKED-M2/README.md` is written; say the scheme changed and why. Update every
✓S row in the tracker. Mark the four v1 sighs as distress-sigh candidates. Add the duration argument to the runners.

**30% — Rough. The two things that prove the wave, both cheap:**
1. **The S15 wide, mapped before anything is generated** (Sean's explicit condition). Extend `room-bible/m2_candidates.py` +
   `make_shot_roughs.py` with the candidates and render each as a plate rough AND a cast rough (the green blocks = the map):
   - **A · wider than real (Sean's lean):** the camera pulled back THROUGH the south wall as a cutaway (the wall removed — the cartoon
     convention the inspiration uses), everyone in their true corner: Claude NW far-left, Codex SW near-left at the rack/tower, Grok NE
     far-right at the hole, Sean centre at the north wall, Gemini in front of where her (removed) south wall would be, spinning at the right.
     The solver caps at 86°; the cutaway is drawn with the lens behind the wall plane so the true corners fit. Say plainly it is an
     impossible camera and that the inspiration is one too.
   - **B · chaos spilled to the centre:** a real lens from the south wall's centre; Codex tugging a wire from the computer tower at LEFT of
     the desk, Gemini's spin at RIGHT, Claude's pages and Grok's rubble pulled into the middle — the inspiration's arrangement.
   - (**C**, if useful: a high SE-corner lens ~110°, the compromise.)
   Sheet them; **Sean picks**; then the S15 state-C plate (ELEV-north + -east + -west as bibles + the chosen rough as camera; the wreck
   described from the three state-C corner plates and the NE bible; 6.5). Then the ensemble by answer 3: for each mascot, crop its
   pose from an existing generated frame (Gemini's spin from the locked whirl clip; Codex, Claude, Grok from their state-C composites),
   run the turnaround-sheet prompt on the crop (6.5 each; skip where `refs/turnaround-views/` already has the pose), then CHAIN the edits
   one character at a time onto the S15 plate, verifying each by eye (5 × 6.5). Sean's start still = at the desk, back to the room, hands
   on the keyboard (the coffee-clip rest pose). **The still is a rest pose for everyone** (law 21's exemption is for a still that never
   animates; this one does). Then ONE 7s clip: the four wrong-builds at full chaos + Sean's chair swivels round to face the room and he
   looks across it; the freeze is post on the most chaotic frame; the breath is beat 12's S10 close.
2. **The Grok pit stop** (Q3 = yes): START edit → END edit → 2kf. 37.5.

**60% — Structure. The new Sean setups, destination stills first (rest-pose + facing laws), then one clip each:**
- **10.5 — S19, the side close-up:** camera on the CRT's side of the room, pushed in on Sean's desk so his face reads in ¾/profile with
  the monitors behind and the CRT direction up-right of frame. Rough it from the bible (the S09 lens moved toward the desk). BEFORE still:
  fists up, arms overhead, seen from the side (the beat-9 pose from `m3-roughs/B10.5-before-pose-candidates.png`) — a HELD pose, fine
  as a start. AFTER still: arms down, head turned and tipped UP toward the CRT, brows up, mouth a small o — confused, not alarmed.
  2kf clip: the arms drop, the head snaps up, he holds. 6.5 (plate) + 6.5 + 6.5 + 24.5.
- **13.1 — S16, the monitors' POV medium:** camera at desk height between the monitors looking at Sean's face. New plate (S02 plate as
  bible + a rough as camera). Still: Sean in the chair **already facing the lens, eyes closed, calm** (law 16); clip: the last degrees of
  the turn, then his eyes open on the lens, a small settled nod. Zero typing. 6.5 + 6.5 + 24.5.
- **13.2 — S17, the hands:** an extreme close-up insert of the keyboard with both hands at rest on the keys; clip: a few slow keys, a pause,
  a few more, one soft Enter. **Calm is the note** — fewer events = slower (never "slowly"). Hands are a model risk; keep them still in
  the still. 6.5 + 24.5.
- **15 — the four relief sighs at 5s:** same start frames. The OPPOSITE arc from v1: shoulders up (the held breath) → a big happy exhale,
  shoulders drop, eyes close, a smile → a little hop or a brow-wipe → beam. Happy face stated as a constant. ~17.5 each.
- **16 — the delegation on the S02 framing, Sean facing us:** the composite is a NEW Sean pose on the rev-2 S02 plate (+ the fixed cannon):
  chair turned to us, smiling, calm, hands resting — the pointing lives in the clip. Front view from this camera means his face carries
  10s; the S10 face look-test is the precedent. Clip, 10s: four distinct point-and-nod beats mapped to where each corner is FROM THIS
  CAMERA (Claude NW = frame-left/far, Codex SW = behind-left, Gemini S = behind-right, Grok NE = frame-right/far), a small approving nod
  after each. 6.5 + ~35. **Check the sheet for spreading; fall back to 7s with the same events.**
- **17 — S18, the SHIP key:** an extreme close-up insert of a keyboard whose one big key reads SHIP. START: a finger resting beside it;
  END: the key pressed down under the finger, built from the START so only the key changes (`post/screen_swap.py`-style; law 10 + the
  S07 lesson). 6.5 + 6.5 + 24.5.
- **20 — ANOTHER PROBLEM!:** an S08 edit; 6.5.

**90% — Polish.** **18.5:** the S09 state-C plate (edit of the locked S09 plate — the popped screen at the rack, the canyon, the fifty on
the left wall, Grok's rubble at the right edge; 6.5) → the chained ensemble (answer 3; the S09 cast at rest in their corners, ¾ front) →
one 7s clip: five characters cheering in place, each a whole beat, faces as constants. Then re-run `post/m3_roughcut.py` with the new
running order and Sean's trims, and the stopwatch table-read (#206) against the 2:00 ceiling with the 5s pit stop and the 6s replay as
the hard floors.

**Every corner still starts from a rest pose, ¾ front, face visible, eyeline on the task, one face constant per character in the
"the same … in every frame" form. The Grok identity line is verbatim. Zero negation. Register and vocabulary blocks verbatim.
New this wave: a duration argument on the runners; a happy face is a constant like any other; chained ensemble edits are verified
one character at a time.**

## MEASUREMENT — $0, a tripwire, never a verdict

```
post/layout_hold.py  <start.png> <clip.mp4>     # ≥0.95 both ends is the bar; run vs BOTH keyframes on a 2kf clip
                                                #   (law 23: ~0.87 on the sketch-buried S05 plate is line boil, not a re-camera)
post/verify_edit.py  <plate> <edit>             # a wreck-edit reads CHECK by construction (law 1); chained edits: verify vs the PREVIOUS step
post/normalize_paper.py <png>                   # → normalised/ (repo venv). Law 23: a closeup with NO WALL in the top band
                                                #   (S11, S16, S17, S18) over-gains — use the raw plate, say so
post/fetch_result.py <job.json> <out>           # refuses an empty [] (law 5: a dropped wait, not a failed job)
post/m3_roughcut.py  <out.mp4>                  # the SHOTS table is the edit
ffmpeg -i clip.mp4 -vf "fps=12/<dur>,scale=480:-1,tile=4x3" -frames:v 1 sheet.png   # the contact sheet Sean reads
```

Sean's eye has now overruled the metrics **eight** times on this project. Put the picture in front of him — the contact sheet plus
the mp4 path — before writing a verdict.

## WORKING DISCIPLINE

**Sean directs. Propose with a stated lean and let his eye decide. Lock nothing on your own judgment.** Push every proposal to a named
specific. **Show him the picture** — rough it at $0, sheet every clip, send the file (the mp4 upload to the remote viewer has failed
twice on a socket error; say when a file is desktop-only). **Announce cost before spending it**, keep a running total, reconcile
against `account status` at the end. **Report failure straight, in the first sentence.** Check the reference before calling identity
drift. When a ruling reverses an earlier one, record why, keep the superseded artifact, say what it costs. **After two CLI misses on
the same character, build the kit and hand it to Sean for the web app.** Update the tracker on every generation and approval; every
prompt file carries its result and diagnosis in its header; append the laws this wave earns to `_blocks.md` and the day's entry to the
root `CHANGELOG.md`. Leave a review packet at the end the way `CONTINUATION-2026-09-06-wave-3-review.md` did.
