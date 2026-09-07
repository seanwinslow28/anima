# CONTINUATION — 2026-09-07 · POST KICKOFF REVIEW: the VO script, the read, the gaps, the story check — and the cut, watched whole for the first time

**Start the next session by invoking `/creative-director`** (Phase 0 only), then read this file, then `VO-SCRIPT-v1.md`,
`GAPS-2026-09-07.md`, `POST-CHECKLIST.md`, and the RESULTS table at the foot of `beats-v1.md`.

Working directory: `/Users/seanwinslow/Code-Brain/anima/briefs/2026-08-02-about-me-short` · branch `about-me-short/post-kickoff`
(record commit + a media commit; Sean squash-merges). **$0 spent.** Balance unchanged at 1,174.5.

## What happened on 2026-09-07 (evening)

The post-kickoff continuation ran end to end under `/creative-director`: Phase 0 grounded (the brief + amendment, the concept's
timing bible, the two locked lines and their cold-read record, the beat sheet's stopwatch protocol, the three locked READMEs, the
M3 tracker, laws 1–39); every locked clip probed (all 34 are 1280×720 24fps, video-only, including Sean's wide); the beats that
carry an out-point or a floor measured on their frames (beat 12's eyes, the wide's freeze, the typewriter's hold, the sting's flash,
the cannon in 9 and 16, the SHIP press). Then the three jobs.

**Watch these first:**
- `motion/film-roughcut/FILM-roughcut-v7.mp4` (+ `-sheet.png`) — **the whole film, first assembly**, 1:57.4: Movements 1 and 2 cut
  for the first time at the beat sheet's timings, Movement 3 as the rough cut v6 with two fixes (below). Every segment is labelled
  with its running timecode, so a frame grab is a stopwatch lap.
- `motion/film-roughcut/FILM-roughcut-v8-trim-lean.mp4` (+ `-sheet.png`) — **the trim lean**, 1:42.1. Same clips, Movement 2 and
  the head of Movement 3 shortened, the floors untouched. This is the edit the story check argues for.
- `post/film_roughcut.py` builds both; its two SHOTS tables are the edit. `*.beats.md` beside each mp4 is the beat table.

## The deliverables

| Job | File | One line |
|---|---|---|
| 1 | `VO-SCRIPT-v1.md` | 12 VO lines (87 words), every silent beat silent, both locked lines verbatim, timecode windows off both cuts, delivery notes, pronunciation, a take list (three cadences for the button so the alarm cuts a natural word), the mute-parity caption text |
| 1 | `beats-v1.md` § RESULTS | the stopwatch table-read, performed against the assembled cut at the two paces — filled for the first time |
| 2 | `GAPS-2026-09-07.md` | the twelve gap items, each verified / open / Sean's call, with the picture where the ruling is his |
| 2 | `POST-CHECKLIST.md` | delivery spec, the per-beat holds/floors/out-points, the 24-cue SFX list, the temp-track brief, captions, the scratch gate, the seven open rulings |
| 3 | this file § The story check | the one-page read + the trims with a lean |

## Two things the picture corrected, both already in `film_roughcut.py`

1. **Beat 12's out-point.** The eyes begin to open at **~5.70s** of the locked clip, not the FACE sheet's ~6.2s; the M3 rough cut v6
   cut at 5.9s and caught them opening. Now **5.6s**. (Frame crops every 3 frames from 5.3s: shut to 5.63, opening at 5.70, open by 5.9.)
2. **The pit stop was 5.3s** in v6 (1.3+1.3+1.3+1.4), over the ≤5s floor. Now 4×1.2 = **4.8s**; every micro-task completes inside
   ~1.5s of its clip, so 1.2s still shows the task.

Also measured, no change needed: the wide's real motion is 3.0–7.6s and it is frozen from ~7.7s to its end (so the cut opens it at
3.0s, not v6's 2.0s); the typewriter finishes at 3.17s and holds 1.5s; the sting's flash is at 1.5s of its clip (the alarm frame).

## THE THINGS OWED BY SEAN (in the order they block post)

| # | Ruling | The picture | Lean |
|---|---|---|---|
| 1 | **The 60-second bar.** In the film as cut the swivel *starts* at 1:00.8 and the question completes at 1:16.7; in the trim lean the step-back lands 0:51–0:56 and the question at 1:04.9. Take v8 and re-read the bar, or cut Movements 1–2 harder (another ~5s: corners to 1.2s, builds to 3.5s) | the two rough cuts, side by side; their `.beats.md` | **v8, bar re-read as "step-back by 0:60, question by 1:05."** The sheet's 60 assumed a 10s Movement-3 head; the locked head is 21.6s because the held beat, the turn back and the hands *exist now*. The protocol's own rule: the sheet loses, not the held beat |
| 2 | **The end.** No card / a title-twin card after ≥1s of black / a loop to the title | `_LOCKED-M1/01` is the twin | black only for the master; test the loop on the staging page at $0 |
| 3 | **The bell over the SHIP key** — ring it off screen, or silent-but-for-the-key | `32` (no bell in frame) | ring it (the audio rhyme is free; the picture's twin is press vs. slam) |
| 4 | **The cannon** upright in 16 after toppling in 9 | `_LOCKED-M2/14` last frame vs `_LOCKED-M3/27_…_start-frame.png` | $0 matte of the fallen cannon over the static tripod region; else accept |
| 5 | **The implied fix** (story check, below): the pit stop never shows the *new* button; the graph-rockets twin was released | `22_…_replay-page-still.png` (the tiny button) | accept for now; if the blind story read stumbles here, a 6.5 cr "page, fixed" still after the SHIP key |
| 6 | Mascot voices — none (lean) · music source · the scratch-narration gate (owed; fallback named) | — | — |

## Corrections and caveats, reported straight

- **The stopwatch read is a desk read.** The protocol wants a person reading aloud with a stopwatch; what exists is the assembled
  cut plus the script's lines timed at 2.3 and 2.0 words/s. The silent beats are the cut's own durations, so the numbers are honest
  about the picture and provisional about the voice. Sean's own read is the third pass and replaces these.
- **The 30s scratch-narration gate was never run** and production spend proceeded past it. Recorded in GAPS #1 with the fallback
  now named; it blocks the final mix, not the assembly.
- **The kickoff doc pointed at `motion/m1-*` and `motion/m2-*` rough cuts "and their READMEs".** Neither existed — only the M3 rough
  cut did. `film_roughcut.py` is the first M1/M2 cut and the first whole-film assembly; the M1/M2 trims are a first guess for Sean to
  argue with, like v1 of the M3 rough was.
- **Nothing was generated, edited or re-rolled.** The two rough cuts are trims of locked material; the freeze still and the two
  post clips are the existing $0 artifacts.
- I did not open the browser or any external service; the visual-guides directory is present (`references/visual-guides/`, 10 guides)
  and none were needed for a cut-only pass.

---

## THE STORY CHECK — one page, as a viewer who has read nothing

*Watched: `FILM-roughcut-v7.mp4` and `-v8-trim-lean.mp4`, whole, with the VO lines read against them at the target pace.*

**Does the spine read?** Yes, and it reads without a single word of the docs. Title → five corners doing their thing → the CRT
snaps on with PROBLEM! and a falling graph → the room looks up, then at Sean → Sean's silent go → four escalating builds (paper
canyon, a screen of code, a wall of fifty, a hole in the wall with a rocket in it) → Sean slams a key, arms up, the cannon falls
over, the bell sags → PROBLEM (STILL!) → Sean alone notices → the whole wrecked room, and Sean turning in the middle of it → the
record-scratch freeze → **Sean, eyes closed, still** → he turns back, opens his eyes → hands → a question types itself → a cursor
circling a shop page, never touching the tiny button → four sighs → Sean pointing, four quick tasks, Grok smashing a person-sized
BUY → SHIP → the grey figure on the CRT turns green and grins → the team cheers in the wreck → the narrator starts a serene
closing thought → ANOTHER PROBLEM! → black. Therefore / But holds at every joint. A viewer gets: they built the wrong things
brilliantly, he stopped, he asked, he watched, they fixed the small real thing, the user was happy, and then it started again.

**Does the narrator/picture gap open in cycle 1 and close at the swivel?** It opens on Step one ("a team that knows its job" over
Grok missing the dartboard and Sean chugging blind) and widens exactly one notch per build — the script's Step four ("change only
what needs changing") over Codex rebuilding everything is the widest point, which is where it should be. "And just like that:
problem solved" over the cannon falling over is the cycle's punchline and the last time the voice and the picture disagree. Then
the alarm, then silence for 15 seconds (10 → 10.5 → the wide → the freeze → the swivel): the narrator does not speak again until
the step-back line, and that line is the first time he and the picture say the same thing. **The gap closes where it should and
stays closed** — Step seven ("watch") and Step eight ("solve it. Together") describe what we see. The button line then re-opens it
one inch on the way out, which is the joke.

**Is the step-back protected?** Yes. It is the only shot in the film where nothing happens for five seconds, it has no caption, no
music, no gag; the cut now leaves before his eyes open, so the eyes open once, on us, in 13.1, and the line lands on that. One risk:
in the wide before it, Sean's swivel is small at 720 (the swivel *in the wide* is a foreshadow, not the beat) — the freeze and the
record scratch do the work of stopping the film, and the close-up does the work of the beat. That division is right.

**Does the sting read as cyclicality, not cynicism?** Yes, provided three things post already owns: the USER's grin is *seen*
(18 holds on it for 3–4s), the cheer in 18.5 reads as genuine (at this scale the faces are unreadable; arms up together at 2.5s
of the clip carries it, so hold through that frame), and the black is instant. The narrator being cut off is what keeps it a
loop rather than a moral; the blind readers said the same thing about the line before a frame existed, and the picture agrees.

**Does anyone need a line they don't have?** Two places, and only one is a gap.
1. **Beat 16.5 → 17: the fix is implied, never shown.** The replay tells us the user can't find the buy button. The pit stop then
   shows Claude writing one stroke, Codex one tap, Gemini one sketch slapped dead-centre, Grok demolishing a person-sized BUY —
   and then SHIP, and then the user is green. The *new* button, or the *fixed page*, never appears; the falling-graph → rocketing-
   graph twin was released with the old beat 17. A viewer who has read nothing still gets "they fixed something small and the user
   is happy" — the green does the telling — but they do not get *what*. This is the one beat doing story work the picture does not
   fully carry. The cheapest honest fix is **not a VO line** (the narrator describing the fix would break "picture punches"); it is
   a **$0 caption-free insert** we don't have, or a **6.5 cr still**: the replay page with a big BUY button dead-centre, held ~1s
   after the SHIP key. Lean: leave it for the blind story read; buy the still only if a fresh viewer asks "what did they change?"
2. **Beat 10.5 (Sean alone notices)** is doing pure story work — it is the hinge where *he* changes — and it has no line. It should
   have none: the silence from alarm #2 to the step-back line is the film's second engine. Not a gap.

**The trims (Movement 3, ~65s → ~40s), floors untouched.** Movement 3 as cut in v7 is 66.5s (beats 10.5–20). v8 takes it to
58.8s and the whole film to 1:42. Three trims, in the order I'd take them:
- **Trim A — the head, before the swivel (−4.3s).** 10.5 from 2.6 → 1.8 (fists ~0.8s, the snap, the hold); the wide from 5.8 → 4.8
  by opening at its first real motion (3.0s of the clip, not 2.0); the freeze 1.5 → 1.2; 13.1 from 5.2 → 3.9 (the turn, the eyes
  open, out before the nod — the nod is nice but the line has landed); the hands 2.4 → 1.6. The swivel stays 5.1. **Lean: take it whole.**
- **Trim B — the delegation (−2.2s).** 7.4 → 5.2: three point-and-nods and the settle instead of four. The fourth point is the
  same beat a third time. **Lean: take it.**
- **Trim C — the tail (−1.4s).** The colorize 4.0 → 3.2 (the green has travelled and the grin is on by 3.0s of the clip); the
  cheer 3.2 → 2.6 (out after arms-up-together). **Lean: take the colorize trim, keep the cheer at 3.2** if the genuineness read
  in 18.5 needs the extra frames — the blind readers flagged that smile as load-bearing.
- **Not trimmed:** the swivel (5.1), the replay (6.0), the pit stop (4.8), the button hold (set by the take), the black (1.0).
  M3 cannot reach ~40s without cutting the replay or the swivel, and it shouldn't: **~55–59s is Movement 3's honest length**, and
  the film's length problem is Movement 2's (35.8 → 27.6 in v8, the builds at 4.0–4.4s each, still escalating).

**One thing I'd change in the script after watching, and did:** Step four is now "change only what needs changing" — the scratch
"gather your team's input" wasn't a setup for anything Codex does, and the widest gap in the film deserves the straightest line.

---

## What the next session does

1. Sean rules the six items above (the bar, the end, the bell, the cannon, the implied fix, mascot voices) and picks the cut (v8, or
   a v9 with his own trims — edit the SHOTS table in `post/film_roughcut.py` and re-run).
2. Sean records or clones the narrator in ElevenLabs from `VO-SCRIPT-v1.md` (one line per generation, the take list), drops the WAVs
   in `post/vo/`, and the scratch gate is judged blind on L1–L8 over the first 40s.
3. Post assembly proper (CapCut or the script): the crop-ins (13.3, and the replay if ruled), the alarm floods and shakes, the
   captions, the SFX pass off the 24-cue list, a temp track, the button hold set to the take, the sting's instant black. Then the
   1080p master + WebM and a staging About page for the mute-autoplay test.
