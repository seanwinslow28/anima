# CONTINUATION — 2026-09-07 · POST KICKOFF: the VO script for ElevenLabs, the gap check, the story check, the hand-off to post

**Start the next session by invoking `/creative-director`** (Phase 0 only — ground; do not re-plan, do not re-interview, do not re-open a lock),
then read this file top to bottom, then [`00_studio_brief.md`](00_studio_brief.md) (the non-negotiables + the 08-31 amendment), [`concept.md`](concept.md)
(the narrator rules, §Timing bible), [`lines-v1.md`](lines-v1.md) (the two LOCKED lines, verbatim), [`beats-v1.md`](beats-v1.md) (the beat sheet with its
SCRATCH VO lines + the stopwatch protocol #206), the three `_LOCKED-M*/README.md` files, and the M3 tables at the foot of [`M1-STORYBOARD.md`](M1-STORYBOARD.md).
`prompts/_blocks.md` laws 1–39 are the production record; post does not need them but the story check does (what each shot actually contains).

Working directory: `/Users/seanwinslow/Code-Brain/anima/briefs/2026-08-02-about-me-short` · branch `about-me-short/m3-wave-3` (Sean squash-merges).

## Where the film is

**Every shot of all three movements is generated and Sean-locked.** Nothing in the picture is owed a generation. Movement 3 closed 2026-09-07 16:03
(13.1 v3 + Sean's own S15 wide). The movement rough cuts are `motion/m1-*`, `motion/m2-*` (see their READMEs) and **`motion/m3-roughcut/M3-roughcut-v6.mp4`**
(64.7s raw M3; the SHOTS table in `post/m3_roughcut.py` is the M3 edit's first guess). Balance 1,174.5 (2026-09-07 16:03).

## The locked material, in running order (raw lengths; the cut trims)

| # | File | Beat | Setup | Raw length |
|---|---|---|---|---|
| 01 | `_LOCKED-M1/01_beat1_S01_title-card.png` | 1 | S01 | still |
| 02 | `_LOCKED-M1/02_beat2_S03_claude-writing-loop.mp4` | 2 | S03 | 7.0s |
| 03 | `_LOCKED-M1/03_beat2_S04_codex-study-fix.mp4` | 2 | S04 | 7.0s |
| 04 | `_LOCKED-M1/04_beat2_S05_gemini-one-more.mp4` | 2 | S05 | 7.0s |
| 05 | `_LOCKED-M1/05_beat2_S06_grok-throw.mp4` | 2 | S06 | 7.0s |
| 06 | `_LOCKED-M1/06_beat2_S02_sean-coffee.mp4` | 2 | S02 | 7.0s |
| 07 | `_LOCKED-M1/07_beat3_S07_alarm-pushin.mp4` | 3 | S07 | 7.0s |
| 08 | `_LOCKED-M2/08_beat3h_S09_room-reacts.mp4` | 3½ | S09 | 7.0s |
| 09 | `_LOCKED-M2/09_beat4_S10_silent-go.mp4` | 4 | S10 | 7.0s |
| 10 | `_LOCKED-M2/10_beat5_S12_claude-canyon.mp4` | 5 | S12 | 7.0s |
| 11 | `_LOCKED-M2/11_beat6_S13_codex-screen-pop.mp4` | 6 | S13 | 7.0s |
| 12 | `_LOCKED-M2/12_beat7_S14_gemini-whirlwind.mp4` | 7 | S14 | 7.0s |
| 13 | `_LOCKED-M2/13_beat8_S06B_grok-demolition.mp4` | 8 | S06B | 7.0s |
| 14 | `_LOCKED-M2/14_beat9_S02_hollow-ship-it.mp4` | 9 | S02 | 7.0s |
| 15 | `_LOCKED-M2/15_beat10_S08_alarm2.mp4` | 10 | S08 | 7.0s |
| 16 | `_LOCKED-M3/16_beat10.5_S19_sean-notices.mp4` | 10.5 | S19 | 7.0s |
| 17 | `_LOCKED-M3/17_beat11_S15_the-wide.mp4` | 11 | S15 | 13.0s |
| 18 | `_LOCKED-M3/18_beat12_S10_the-swivel.mp4` | 12 | S10 | 7.0s |
| 19 | `_LOCKED-M3/19_beat13.1_S16_the-turn-back.mp4` | 13.1 | S16 | 7.0s |
| 20 | `_LOCKED-M3/20_beat13.2_S17_the-hands.mp4` | 13.2 | S17 | 7.0s |
| 21 | `_LOCKED-M3/21_beat13.3_S11_chat-typewriter.mp4` | 13.3 | S11 | 4.7s |
| 22 | `_LOCKED-M3/22_beat14_S08_replay-cursor.mp4` | 14 | S08 | 7.0s |
| 23 | `_LOCKED-M3/23_beat15_S03_claude-relief.mp4` | 15 | S03 | 5.0s |
| 24 | `_LOCKED-M3/24_beat15_S04_codex-relief.mp4` | 15 | S04 | 5.0s |
| 25 | `_LOCKED-M3/25_beat15_S05_gemini-relief.mp4` | 15 | S05 | 5.0s |
| 26 | `_LOCKED-M3/26_beat15_S06B_grok-relief.mp4` | 15 | S06B | 5.0s |
| 27 | `_LOCKED-M3/27_beat16_S02_the-delegation.mp4` | 16 | S02 | 10.0s |
| 28 | `_LOCKED-M3/28_beat16.5_S03_claude-pitstop.mp4` | 16.5 | S03 | 7.0s |
| 29 | `_LOCKED-M3/29_beat16.5_S04_codex-pitstop.mp4` | 16.5 | S04 | 7.0s |
| 30 | `_LOCKED-M3/30_beat16.5_S05_gemini-pitstop.mp4` | 16.5 | S05 | 7.0s |
| 31 | `_LOCKED-M3/31_beat16.5_S06B_grok-pitstop.mp4` | 16.5 | S06B | 7.0s |
| 32 | `_LOCKED-M3/32_beat17_S18_the-ship-key.mp4` | 17 | S18 | 7.0s |
| 33 | `_LOCKED-M3/33_beat18_S08_user-colorizes.mp4` | 18 | S08 | 7.0s |
| 34 | `_LOCKED-M3/34_beat18.5_S09_team-celebrates.mp4` | 18.5 | S09 | 7.0s |
| 35 | `_LOCKED-M3/35_beat19_S08_the-button-hold.png` | 19 | S08 | still |
| 36 | `_LOCKED-M3/36_beat20_S08_sting-transition.mp4` | 20 | S08 | 5.0s |

**Raw locked motion ≈ 236s across 34 clips + 2 stills; the film's ceiling is 2:00 and the beat sheet's target ≈ 1:27.** Every clip is 7s of
raw material unless noted (the sighs 5s, the delegation 10s, the sting 5s, the wide 13s) — *"the timing comes down in the edit, not the generations"*
(Sean, law 6). Two hard floors: **the pit stop ≤5s total**, **the replay ≥5–6s**. The swivel (beat 12) is held *past comfort* and is never the compression victim.

## JOB 1 — the VO script for ElevenLabs

**The narrator is Sean's own voice** (the brief: *"real Sean, self-recorded"*; the Goofy "How To" 1952-serene instructional read; *"the narrator's
composure never breaks — he never acknowledges the chaos"*; *"narrator sets up, picture punches"*; *"the gap closes at the step-back and stays closed"*).
Sean is recording (or cloning) in ElevenLabs. Write **`VO-SCRIPT-v1.md`**:

1. **One line per VO beat, in running order, with the beat number, the shot it plays over, a target timecode window and a target duration**
   (read at 1952-serene pace — count it; ~2.3 words/s). The SCRATCH lines in `beats-v1.md` are placeholders *in the right register* — rewrite them
   where they can be better, keep the "Step N:" spine, keep every silent beat silent (3, 10, 11, 12's first half, 13.3, 14's first beat, 15, 17, 18, 20).
2. **The two LOCKED lines are verbatim and untouchable:** the question is TYPED, never voiced (*"Can you show me what happened the last time you
   tried to check out?"*), and the button is **NARRATOR: "Which brings us back to where every problem begins: a quiet—"** cut by the alarm. Mark the
   cut-off word and that the caption dies on the em-dash.
3. **Delivery notes per line** for the ElevenLabs read: pace, the serene flatness, where a breath goes, what NOT to lean on (no wink, no
   acknowledging the picture). Include the one exception — the step-back line (*"Sometimes, the next step… is a step back."*) is *quiet and
   agreeing*, the only line where narration and picture agree, and it lands **after** the held breath, not over it.
4. **A pronunciation / emphasis block** and a **take list** (2–3 alternates for the button line's cadence so the alarm can cut a natural word).
5. **The mute-parity captions**: the caption text for every VO line as it should appear on screen (the film must play silent — brief non-negotiable);
   the sting caption dies on the em-dash.

Then a **table-read**: read the whole script aloud against the rough cuts with a stopwatch (protocol #206 in `beats-v1.md`, ×2) and fill the
RESULTS table there. **This read has never been performed.** If the question completes after 0:60 or the total passes 2:00, say which movement
gives — the swivel never does.

## JOB 2 — the gap check (things that might be lingering)

Verify each; report straight; do not fix silently:

- **The scratch-narration gate** (brief non-negotiable: *"No full production spend before a blind-judged 30-second scratch narration passes; the
  narrator fallback path is named in writing"*). Production spend happened. Was the 30s scratch ever judged? Is the fallback named? If not, name it
  now (an ElevenLabs stock 1950s-newsreel voice as the fallback if Sean's own read isn't 1952-serene) and put the blind judge on the post list.
- **The SHIP IT bell's sound.** Beat 9 rings it hollow; the beat sheet's "earned bell, full swing" in beat 17 became **the SHIP key press** (Sean's ruling).
  Does the bell still *sound* over the key press (SFX rhyme) or is the earned ship silent-but-for-the-key? Sean's call; put both on the SFX list.
- **The cannon.** Beat 9 topples it (locked v2). Beat 16's start frame has it upright (`_LOCKED-M3/27_…_start-frame.png`). Continuity nit or a 6.5 edit — Sean's call.
- **Beat 12's out-point** must fall BEFORE his eyes open (answer 4); the eyes open once, in 13.1. The FACE sheet marks ~6.2s.
- **The freeze.** Sean's wide ends on the freeze (`_LOCKED-M3/17_…_freeze-frame.png`); the record-scratch hold is a post still + SFX. Confirm its length in the read.
- **13.3's crop-in** (Sean: *"I'll crop in using CapCut"*) — the typewriter clip is 4.7s; the hold after the last word must survive the crop.
- **The end.** The beat sheet ends on black after the sting. There is **no end card / credits / handle** anywhere in the plan. Ask Sean; the title card's
  design (`_LOCKED-M1/01`) is the obvious twin if he wants one.
- **Music.** Nothing is chosen. The brief names the Goofy-short grammar (serene narrator, music, SFX). A temp-track brief for post at minimum.
- **The SFX list** (post owns): alarm ×3 (3, 10, 20 — the third cuts the narrator), the record scratch (11), the bell (9, and 17?), the confetti cannon (9),
  keys (13.2, 17), the typewriter (13.3), the cursor loop (14), the four sighs (15), the pit-stop snaps (16.5), the hammer + button smash (16.5 Grok),
  the crowd cheer (18.5), the CRT flash + rattle (20). Zero dialogue: Sean never speaks aloud; the mascots' "voiced personalities" in the brief are an
  *optional* comedy layer — Sean rules whether any mascot sound exists.
- **Captions / mute-parity** for every VO line (Job 1.5) and the on-screen text that IS the plot: PROBLEM!, PROBLEM (STILL!), ANOTHER PROBLEM!, the
  typed question, SHIP, BUY, USER.
- **Two unused assets, on purpose:** the S15-B plate (`normalised/S15-B-plate-v1.png`, chain unspent) and the beat-13 typing clip + both old beat-17
  clips (released, kept). No action.
- **Aspect / resolution / rate:** every clip is 1280×720 24fps except Sean's own wide (confirm) and the post stills at 2688×1520; the delivery spec
  (16:9, 1080p upscale or native 720p, 24fps) is post's first decision.

## JOB 3 — the story check

Watch the three rough cuts in order as a viewer who has never read a doc, then answer in one page: does the spine read (Therefore/But: wrong-ship →
re-alarm → step back → the question → the replay → the tiny fix → the earned ship → the user smiles → *another* problem)? Does the narrator/picture gap
open in cycle 1 and close at the swivel? Is the step-back protected (no gag)? Does the sting read as cyclicality, not cynicism (the team's smiles genuine
in 18.5)? Does anyone need a line they don't have? Name any beat that is doing story work the picture does not carry — that is where a VO line or a
caption is owed. Then propose, with a stated lean, the two or three trims that bring M3 from ~65s toward ~40s without touching the floors.

## Deliverables

`VO-SCRIPT-v1.md` (Job 1, incl. the caption text + take list) · the filled stopwatch RESULTS table in `beats-v1.md` · `POST-CHECKLIST.md` (the SFX
list, the captions, the holds/floors/out-points per beat, the delivery spec, the end-card question) · `GAPS-2026-09-07.md` (Job 2, each item
verified/open/Sean's-call) · the one-page story check appended to the review packet. Update the tracker, `CHANGELOG.md`, and leave a review
packet the way the wave-3b one did. **$0 unless Sean rules a fix; announce any spend first.**
