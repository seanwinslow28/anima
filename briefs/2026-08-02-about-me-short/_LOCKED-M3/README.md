# Movement 3 — the locked cut material (in progress)

Everything here is **Sean-approved** (rulings of 2026-09-06 10:51), ready to import. Clips are
**1280x720, 24fps, no audio**; the two $0 post clips (typewriter, cursor) are shorter than 7s by
design. Copies, not moves — the originals stay in `motion/` and `normalised/` because the prompt
files and the tracker reference them.

## The numbering changed here, and why

`_LOCKED-M1/` and `_LOCKED-M2/` number `NN_beatB_Sxx_slug` with NN = playback order (01–15) and
one integer beat per file. Movement 3 grew sub-beats (10.5, 13.1/13.2/13.3, 16.5, 18.5) and the
integer-beat form breaks on them, so from 16 on the form is **`NN_beatB.B_Sxx_slug`** — NN still
continues in playback order, the beat field carries the decimal where there is one. **Gaps are
deliberate:** every open beat has its NN reserved below so the folder sorts into the running order
as the packages land, and nothing already locked ever renumbers.

| # | File | Beat | Setup | What happens |
|---|---|---|---|---|
| 16 | *(reserved)* | 10.5 | S19 · the side close-up | Sean alone notices: fists-up → looks up at the CRT, confused. OPEN |
| 17 | *(reserved)* | 11/12 | S15 · the super wide | The wrecked room; the swivel to the chaos; the record scratch; the freeze. OPEN |
| 18 | `18_beat12_S10_the-swivel.mp4` | 12 | S10 · Sean's station from the room | The chair rotates square, holds ~4.5s with the eyes closed, the shoulders lift and sink. **The cut ends BEFORE the eyes open** (answer 4) — the eyes open once, in 13.1. Start `18_…_start-frame.png` |
| 19 | *(reserved)* | 13.1 | S16 · the monitors' POV | Sean turns back to the lens, opens his eyes on us, a small nod. OPEN |
| 20 | *(reserved)* | 13.2 | S17 · the hands | Extreme close-up: a few calm keys, a pause, one soft Enter. OPEN |
| 21 | `21_beat13.3_S11_chat-typewriter.mp4` | 13.3 | S11 · the monitor closeup | THE QUESTION types itself into the chat box (post, `post/typewriter_reveal.py`, 3.2s + 1.5s hold). Still `21_…_chat-box-still.png`. Sean crops in on it in CapCut |
| 22 | `22_beat14_S08_replay-cursor.mp4` | 14 | S08 · the CRT closeup | THE REPLAY: the cluttered shop page, the drawn cursor circling on a 10-waypoint path, never finding the tiny grey buy button (post, `post/cursor_overlay.py`, 7s loopable). Still `22_…_replay-page-still.png` |
| 23–26 | *(reserved)* | 15 | S03/S04/S05/S06B state C | Four RELIEF sighs at 5s. OPEN (the wave-3 v1 sighs are distress-sigh candidates, banked in `motion/m3-beat15/`) |
| 27 | *(reserved)* | 16 | S02 rev-2 framing | Sean facing us, smiling, pointing the roles out, 10s. OPEN |
| 28 | `28_beat16.5_S03_claude-pitstop.mp4` | 16.5 | S03 state C | Claude writes one stroke, holds the sheet up, nods, again. Start `28_…_start-frame.png` |
| 29 | `29_beat16.5_S04_codex-pitstop.mp4` | 16.5 | S04 state C | Codex springs onto the counter, one tap, face up, nod, hops down, again. Start `29_…_start-frame.png` |
| 30 | `30_beat16.5_S05_gemini-pitstop.mp4` | 16.5 | S05 state C | Gemini snatches a sketch, flourish, slaps it dead centre, nudges a corner, nod, again. Start `30_…_start-frame.png` |
| 31 | *(reserved)* | 16.5 | S06B | Grok demolishes the person-sized BUY button (Q3 = yes). OPEN → rolling |
| 32 | *(reserved)* | 17 | S18 · the SHIP key | One finger presses the SHIP key. OPEN |
| 33 | `33_beat18_S08_user-colorizes.mp4` | 18 | S08 · the CRT closeup | Grey holds, the green travels up the cable into the set, the figure floods green, the grin + thumb snap on. Two keyframes (`33_…_start-frame.png` → `33_…_end-frame.png`) |
| 34 | *(reserved)* | 18.5 | S09 state C | The team cheering in their corners of the wreck. OPEN |
| 35 | `35_beat19_S08_the-button-hold.png` | 19 | S08 | THE BUTTON: hold on the green USER while the VO runs (post; the rough cut holds it 4s) |
| 36 | *(reserved)* | 20 | S08 | ANOTHER PROBLEM! → red flood → black. OPEN → rolling |

**Locked 2026-09-06 10:51** — Sean on the wave-3 packages: beat 12 (*"looks good, we'll keep that"*), 13.3 (*"is perfect. I'll crop in
using CapCut"*), 14 (*"This works perfectly. This is locked."*), 16.5 ×3 (*"they're perfect"*), 18 and 19 (*"Locked."*). The released
takes (the beat-13 typing clip, both beat-17 clips, the graph edit, the PROBLEM! sting) stay in `motion/m3-beat13/`, `motion/m3-beat17/` and
`normalised/` with `# RELEASED` lines in their prompt headers (`prompts/motion/40, 50, 51`; `prompts/edits/S08-graph-rockets.txt`,
`S08-alarm3-problem-sting.txt`).

## What the cut owns

Beat 12's out-point (before the eyes open — the sheet `motion/m3-beat12/S10-sean-swivel-v1-FACE-sheet.png` shows where they open, ~6.2s);
the 13.3 crop-in; beat 14's hold length (≥5s, the legibility floor); beat 19's VO hold; the beat-20 red flood + instant black.
