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

**Known open risk:** background drift measures **~22–24%** on prop-dense plates at every
tier and duration tried. Untested candidates: first+last keyframes composed from the same
plate; or matting characters out of the animated clip and re-laying them on the pristine
plate.

---

## Spatial placement map (art-department DR #20)

The room read from the master angle **S02**. Every corner setup is this same room with the
camera turned to that zone. **Nothing moves between shots.**

```
   far left        left          CENTRE          right         far right
   doorway   →   Claude    →    Codex    →      SEAN     →   Gemini   →   Grok
  (the USER)      nook           rack           desk         moodboard    dartboard
   west wall    paper tower   server rack    3 monitors     CRT HIGH above   hole in wall
                                             back to cam    string lights    + rocket
```

- **Ground line is y=700 in every guide** so cuts never jump the horizon.
- **Cast scale ratios** (from `cast-scale-lineup.png`): Sean 1.00 · Grok 0.42 · Codex 0.36 ·
  Gemini 0.30 · Claude 0.26. Scale is the thing that drifts in generated video — state it in
  words in every prompt, never leave it inferred.
- The **CRT is high on the right wall above Gemini's moodboard**, so beat 3's alarm can cut
  from any corner and stay oriented.
- The **doorway is west, screen-left**, and stays **empty set dressing**. Sean ruled
  2026-08-30 that a figure standing in it read wrong: **the USER does not appear in the room
  at all.** The USER is introduced **on the CRT** — the TV flashes `PROBLEM!`, then cuts to
  the USER *in* the television. No plate places a figure in the doorway.

---

## Shots

Guides: [`m1-guides/`](m1-guides/) — Python-generated composition roughs
([`make_m1_guides.py`](m1-guides/make_m1_guides.py)), FIRST LICKS idiom, $0 and re-runnable.
Each doubles as the monochrome composition rough for a re-angle and as the placement
authority for the character-into-plate edit.

| # | Setup | Beat | Mechanism | Guide | Plate | Composite | Motion | Notes |
|---|---|---|---|---|---|---|---|---|
| S01 | Title card — HOW TO SOLVE A PROBLEM | 1 | typography, **not** Seedance | ✓ | — | n/a | — | The straight man: it must not move, so the alarm has something to break |
| S02 | **Sean at his desk — MEDIUM, from behind** | 2 | full-scene | ✓ | **✓** | n/a | — | **The all-corners wide was CUT 2026-08-30.** In it the mascots clustered near centre and all faced camera, contradicting the per-corner premise it was meant to establish. The film opens on Sean typing and cuts out to each corner. Plate `S02-sean-desk-v1.png` |
| S03 | Claude's tidy nook | 2 | full-scene | ✓ | **✓** | n/a | — | Plate `S03-claude-nook-v1.png`. Wall passes the re-based cream at delta 2/3/2. Facing stated and honoured — he faces away, never at camera |
| S04 | Codex's humming rack | 2 | plate + edit | ✓ | **✓** | **✓** | **✓** | **Proven end to end in probe-205.** Plate `U-codex-corner.png`, 7s clip `W-single-7s.mp4` |
| S05 | Gemini's string-lit moodboard | 2 | plate + edit | ✓ | — | — | — | Mid-bit: taping up another concept, already bouncing to the next |
| S06 | Grok's dartboard | 2 | plate + edit | ✓ | — | — | — | Darts in the **wall around** the board. The misses are the joke and they land before he throws |
| S07 | The CRT alarm — PROBLEM! | 3 | plate + edit | ✓ | — | — | — | Dead-stop hold → burst. Falling CHECKOUT COMPLETIONS graph |

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

## Open before generation starts

1. ~~**Plate palette continuity.**~~ **CLOSED 2026-08-30** — measured (hero frame paper
   **#e5d7c2** vs probe plate **#d5be99**, a 37-level red spread) and the binding clause is
   written at [`environment-style.md`](environment-style.md). Every plate and composite
   prompt carries it verbatim; tolerance ±8 levels per channel or re-roll.
2. **Codex's face at scale.** It went off-model in every `fast` generation. At corner-shot
   scale it is small enough not to read, but S04's clip should get Sean's eye on that
   specifically before the rest of the corners generate to the same recipe.
3. **Title-card typography** — not decided. It is the one setup Seedance does not touch.
