# Movement 1 — the locked cut material

Everything here is **Sean-approved**, numbered in beat order, and ready to import. All six
clips are **1280x720, 24fps, 7.04s, no audio**. Copies, not moves — the originals stay in
`motion/` because every prompt file and the storyboard reference them by path.

| # | File | Beat | Setup | What happens |
|---|---|---|---|---|
| 01 | `01_beat1_S01_title-card.png` | 1 | S01 | HOW TO SOLVE A PROBLEM. A still — Seedance never touched this one, and its typography is still undecided |
| 02 | `02_beat2_S03_claude-writing-loop.mp4` | 2 | S03 | Claude scribbles a page, leaps to the top of the stack, places it, drops down, does it again. Two full cycles |
| 03 | `03_beat2_S04_codex-study-fix.mp4` | 2 | S04 | Codex studies the rack, springs up, coils the cables, drops, studies, springs again. The cables stay coiled |
| 04 | `04_beat2_S05_gemini-one-more.mp4` | 2 | S05 | Gemini slaps sketches onto the covered wall, one after another after another |
| 05 | `05_beat2_S06_grok-throw.mp4` | 2 | S06 | Grok winds up, throws, misses the board by a foot, throws both arms up in triumph anyway |
| 06 | `06_beat2_S02_sean-coffee.mp4` | 2 | S02 | Sean hammers the keyboard, takes the mug up past his ear without looking, slams back into typing |
| 07 | `07_beat3_S07_alarm-pushin.mp4` | 3 | S07 | The CRT snaps on — PROBLEM! — the room jolts, and the camera smears in on the television |

## Beat 2's order is from the beat sheet, not arbitrary

`beats-v1.md` beat 2 reads: *"Claude's tidy nook, Codex's humming rack, Gemini's string-lit
moodboard, Grok's dartboard, Sean at the center desk."* Files 02-06 are in that order.

## Three things the cut owns, deliberately left out of the generations

1. **Timing.** Sean's standing rule: *"the timing comes down in the edit, not the
   generations."* Every clip is a full 7s of material to trim from — the beat sheet gives
   beat 2 eight seconds across five setups and beat 3 three seconds.
2. **The alarm's look.** The red flood and the frame shake are beat 10 and beat 20's visual
   twins and belong in post. A frame shake would also contradict the locked-tripod clause
   that every other clip in this folder was generated under.
3. **S07's screen blink and its colour.** The CRT lights once and holds; three prompt
   phrasings failed to make it blink, and it is an opacity keyframe in post. The same pass
   should watch the screen's cream.
   S07's zoom starts at **4.54s** in this clip — Sean is pulling it to ~3s in the cut.

## Provenance

Each clip's prompt, route, metrics and diagnosis live in `../prompts/motion/`, one file per
clip, results annotated in the header. Per-shot production state is in `../M1-STORYBOARD.md`.
