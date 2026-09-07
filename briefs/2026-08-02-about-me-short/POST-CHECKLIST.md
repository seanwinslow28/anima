# POST CHECKLIST — HOW TO SOLVE A PROBLEM

*2026-09-07. Post owns everything below. The picture is locked (`_LOCKED-M1/01–07`, `_LOCKED-M2/08–15`, `_LOCKED-M3/16–36`);
the edit trims, it never re-generates. The first assembly is `motion/film-roughcut/FILM-roughcut-v7.mp4` (the film as
cut today, 117.4s) and `…-v8-trim-lean.mp4` (the proposed trims, 102.1s), both from `post/film_roughcut.py`, whose two SHOTS
tables are the edit's source of truth; re-run after any change. Beat tables sit beside the mp4s as `.beats.md`.*

## 0. Delivery spec (first decision)

| | Spec | Note |
|---|---|---|
| Frame | 16:9, **1920×1080**, 24fps | Every clip is 1280×720 24fps (all 34 verified, incl. Sean's wide); 1.5× Lanczos upscale, no AI upscaler (it re-draws the line). Stills (2688×1520) downscale. Fallback: native 720p master if the upscale softens the chat box / SHIP key lettering — test those two first |
| Codecs | H.264 CRF 16 MP4 (archival + About page) · VP9 WebM (web) | muted-autoplay assumed on the page; the file still carries the mix |
| Audio | stereo 48 kHz, −16 LUFS integrated, true peak −1 dB | VO centred; SFX and music wide |
| Captions | **baked in**; one family with the on-screen hand-lettering; lower third; cream card on paper | text in `VO-SCRIPT-v1.md` § Captions; diegetic text never re-captioned |
| Ceiling | ≤ 2:00 | v7 is 1:57.4 (too tight for a real VO read); v8 is 1:42.1 |

## 1. Holds, floors and out-points per beat (the cut's laws)

| Beat | Rule | Source |
|---|---|---|
| 1 | Title card ≥ the L1 read (3.9–4.5s); 4.5s in both cuts | VO length |
| 2 | Five corners, equal length, in the beat sheet's order (Claude, Codex, Gemini, Grok, Sean); L2 must end before the alarm | beat sheet; the alarm is silent |
| 3 | S07: screen snaps on at 1.8s of the clip; the push-in starts at 4.54s and Sean pulls it to ~3s in the cut (two pieces: 1.0–2.6 + 4.3–5.3). Red flood + frame shake are post (opacity keyframe for the screen blink, per the M1 README) | M1 README |
| 3½ → 4 | S09 ends on Sean turned to the mascots, S10 opens on him facing the room: **cut on his look** (S09 0.2–1.5 heads up, 5.0–6.5 to Sean; S10 3.8–6.6 flick + swivel to the desk) | M2 README |
| 5–8 | The four wrong-builds escalate one per beat; each holds long enough for its full event (Codex's screen pop at 1.0s, Gemini's two whirls 0.5–2.5 and 3.8–5.2, Grok's smash at 0.8–1.5 and the haul at ~4.5). Below ~4s each they read as montage, not escalation | story check |
| 9 | Key slam at 2.5s of the clip; cannon fires and **topples**; bell sags; the slump by ~6s. L8's "solved" lands on the slam | `14` |
| 10 | Alarm #2: flash at 1.25s, PROBLEM (STILL!) + rattle 2.5–5.3s. Red flood + extra shake are post, **bigger than alarm #1** (mute-parity variation) | brief |
| 10.5 | Fists ~1s, then the snap and the confused hold; 1.8–2.6s total | 3b packet |
| 11 | The wide from **3.0s** (the first real motion) to ~7.8s, then the **freeze frame still** 1.2–1.5s; record scratch on the first frozen frame; music out dead | GAPS #5 |
| 12 | **THE SWIVEL — 0.5s in, out at ≤ 5.60s** (the eyes begin opening at 5.70s). 5.1s held, the breath complete. Never the compression victim; no caption, no music, no SFX but the chair | GAPS #4; brief |
| 13.1 | The turn 0.5–1.75s, the eyes open ~3.2s, the nod ~5.5s; L9 lands as the eyes open | `19` |
| 13.2 | 1.6–2.4s of keys; the typing SFX starts here and continues into 13.3 | |
| 13.3 | Full 4.67s (typing to 3.17s + **1.5s hold**); crop-in in CapCut: slow push during the typing, ≤ ~1.6× at 720, the hold survives entire | GAPS #6 |
| 14 | **THE REPLAY ≥ 5s** (6.0 in both cuts); optional slow push-in on the CRT so the tiny buy button reads; L10 at the head only | brief floor |
| 15 | Four relief sighs, ~1.1s each, in Claude/Codex/Gemini/Grok order; the sigh SFX carries the cut | |
| 16 | The delegation 5.2–7.4s (the 10s clip has four point-and-nods + the settle; keep at least three points); L11 at the head | `27` |
| 16.5 | **PIT STOP ≤ 5s total: ≤ 1.25s per mascot** (4×1.2 = 4.8s). Every micro-task completes inside ~1.5s of its clip (law 17). Grok from 0.4s | brief floor; GAPS |
| 17 | SHIP key: the press at 2.0s of the clip (window 1.4–3.4); the bell's second ring is Sean's call (GAPS #2) | |
| 18 | Colorize: grey → green travels up the cable → grin + thumb; 3.2–4.0s; the smile must be seen before 18.5 | blind-reader note |
| 18.5 | The cheer 2.6–3.2s (arms up together at ~2.5s of the clip); the smiles must read genuine — body language carries it at this scale | blind-reader note |
| 19 | **THE BUTTON hold = the recorded take's length** (4.8–5.5s at the two paces) minus the sting's 0.6s of green; the still holds until the alarm | VO |
| 20 | The sting clip from 0.9s: 0.6s green → white flash at 1.5s (**the alarm and the caption's death are on this frame**) → ANOTHER PROBLEM! from 2.0s, held ≥ 0.5s so it reads → red flood 0.15s → **black, instant, ≥ 1.0s**, no linger on the smile | `36`; blind-reader note |

## 2. SFX list (24 cues; post sources them; $0 until a library is chosen)

| # | Beat | Cue | Note |
|---|---|---|---|
| 1 | 3 | CRT power-on click + **ALARM #1** (a klaxon, mid-size) | the screen blink is an opacity keyframe; the alarm starts on the snap-on |
| 2 | 3 | the push-in whoosh (light) | under the zoom at 4.54s of the clip |
| 3 | 4 | chair swivel + the finger flick (two tiny snaps) | the GO |
| 4 | 5 | pencil scribble at speed + pages fluttering | Claude |
| 5 | 6 | rack thump, screen-arm pop, hammer-typing, the code-flood zip | Codex |
| 6 | 7 | the whirl (a Tasmanian-devil spin), sketches slapping | Gemini |
| 7 | 8 | hammer hoist, wall smash + rubble, the rocket dragged, one pat | Grok |
| 8 | 9 | key slam, cannon POP (misfire), **the cannon's topple + clatter**, the bell's **hollow** clank | the hollow ring is the sound design's first twin |
| 9 | 10 | CRT click + **ALARM #2, louder**, the set's rattle | bigger than #1 in every way |
| 10 | 10.5 | (room tone only; the fists' small shake) | |
| 11 | 11 | the chaos at full (a bed of 4–7 layered thin) → **RECORD SCRATCH** → **silence** | the silence is a designed hole; nothing but room tone until 13.2 |
| 12 | 12 | one slow chair swivel; a breath is NOT recorded (the shoulders are the breath) | protected |
| 13 | 13.1 | the chair swivels back (the other direction) | |
| 14 | 13.2–13.3 | keys (single presses, a pause, three more, Enter) → **typewriter** letters on the reveal → a soft return per line → **send** | the typewriter is the question's only "voice" |
| 15 | 14 | the CRT's replay hum + the **cursor's mouse-move loop** (three circles) | loopable; the button is never clicked |
| 16 | 15 | four **sighs of relief** (whoosh, brow-wipe, hop-land, a happy exhale) | one per mascot |
| 17 | 16 | (room tone; four small point gestures if anything) | L11 carries it |
| 18 | 16.5 | **pit-stop snaps**: one pencil stroke + sheet snap (Claude), one key tap + hop (Codex), one sketch slap + corner nudge (Gemini), **hammer + BUY-button smash + dust** (Grok) | F1 precision: each cue on its cut |
| 19 | 17 | the SHIP key press (one clean click) + **the bell, earned** (Sean's call, GAPS #2) | |
| 20 | 18 | the green travelling up the cable (a soft rising tone) + the grin/thumb snap | |
| 21 | 18.5 | **crowd cheer** (five voices' worth, not a stadium) + a chair spin | genuine, not triumphant-ironic |
| 22 | 19 | room tone under the button line | nothing else |
| 23 | 20 | CRT flash + **ALARM #3** (cuts the narrator on "quiet") + the set's rock and the cable swing | the alarm's transient is the edit point |
| 24 | 20 | the black: **silence** (no tail, no sting music) | ≥ 1.0s |

Zero dialogue anywhere. No mascot voices (the brief's optional "voiced personalities" layer is unbuilt; Sean's call — lean: leave it out).

## 3. Music — temp-track brief

A light 1950s library-cue feel (strings, woodwind, brisk, brochure-pleasant; the Goofy shorts' music room), never
comedic on its own. **In** under the title and Movement 1; **stays** under Movement 2, thin, letting the SFX punch;
**out dead** on the record scratch (11) and absent through the swivel, the turn back, the question and the replay;
**back thin** under the relief sighs; **builds** under the pit stop (the film's one flourish); **holds** under the ship,
the colorize and the cheer; **gone before the button line** so the third alarm is the only sound that cuts him; nothing
under the black. Source: royalty-free library or a generated cue; spend is Sean's call.

## 4. Captions

Full text per line in `VO-SCRIPT-v1.md` § Mute-parity captions. Rules: one family with the on-screen lettering; appear with
the first word, clear with the last; no caption on any silent beat (the swivel carries no text); diegetic text never
doubled; L12's caption **dies on the em-dash on the flash frame**, cut not faded.

## 5. The scratch-narration gate (owed; brief non-negotiable)

Blind-judge L1–L8 assembled over the first 40s of v8. Pass = a fresh listener hears a straight-man narrator, not a guy with
a mic. Fallback named: an ElevenLabs stock mid-century newsreel voice reading the same script. Blocks the final mix, not
the assembly.

## 6. Open rulings (Sean)

1. The end — black only (lean) / a title-twin card after ≥1s of black / the loop back to the title.
2. The bell's second ring over the SHIP key — audio rhyme on (lean) / silent-but-for-the-key.
3. The cannon in beat 16 — $0 matte paste (lean) / accept / 41.5 cr re-roll.
4. The 60-second bar — take v8 and re-read the bar as "the step-back by 0:60, the question by 1:05" (lean) / cut Movements 1–2 harder.
5. The fix that the picture implies but never shows (see the story page) — accept (lean for now) / a 6.5 cr "page, fixed" still after the SHIP key.
6. Mascot voices — none (lean).
7. Music source and spend.

## 7. Files post reads

`VO-SCRIPT-v1.md` · `beats-v1.md` (RESULTS filled) · `GAPS-2026-09-07.md` · `post/film_roughcut.py` (+ the two `.beats.md`) ·
`_LOCKED-M*/README.md` · `post/typewriter_reveal.py`, `post/cursor_overlay.py` (the two $0 post clips' sources).
