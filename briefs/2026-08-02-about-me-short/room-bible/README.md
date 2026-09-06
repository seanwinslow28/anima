# The room bible

**The spatial authority for the whole film.** Built 2026-08-31 at Sean's direction,
replacing the Movement-1-only floor plan (superseded, kept at
[`../m1-guides/old/`](../m1-guides/old/)).

## Revision 2 — everyone gets a corner

> "Everything is very close together, so trying to crop out corners might look awkward.
> Sean's station is on the north wall, Claude is on the north west corner (left of Sean) and
> Grok is on the north east corner (right of Sean). Everyone should have their own respective
> sections without completely overlapping on one wall." — Sean, 2026-08-31

Rev 1 still had Claude, Sean and Grok sharing the north wall, which is a **lane** arrangement
wearing a corner's name — and lanes are exactly what killed the cut all-corners wide. Rev 2:

| Wall | Who |
|---|---|
| **North** | Sean's station alone, plus neutral office overflow at the ends |
| **West** | Claude's nook at the north end · the doorway · Codex's rack at the south end |
| **East** | Grok's dartboard at the north end · the CRT · the moodboard wrapping in |
| **South** | Gemini's moodboard, long |

S03 and S06 are now genuine **two-wall corner shots** with real depth. S04 keeps the SW
corner; S05 stays square to the south wall.

**Two more things Sean settled at the same time.** The moodboard sketches are now product and
mascot concepts — shopping bags, checkout buttons, packaging, price tags, storefront signs,
little cartoon creatures — instead of the landscapes rev 1 produced, which matters because
beat 7's wrong-build is "new brand, shop mascot." And the doorway stays dressing: the USER is
on the CRT, and **Sean asks the question at his computer**, which puts beats 2, 4, 12 and 13
all at his station and makes it the film's most-used angle.

**One consequence worth confirming.** If the question is asked at the computer rather than
spoken to someone in the room, the Sean character never speaks aloud at all — and the studio
brief's non-negotiable is *"The Sean character speaks exactly once — the question."* A wordless
protagonist may be exactly right for a VO-and-sound-effects film, but it changes a locked
line, so it should be a ruling rather than a side effect.

## One source of truth

`WALLS` in [`make_room_bible.py`](make_room_bible.py) is the **only** place a fixture is
described. The ground plan draws it from above using its depth, the elevations draw it from
the front using its height, and the bare roughs draw it for the generator. Rev 1 kept two
copies and they had already begun to disagree — the same failure mode as the plates, one
level up.

> "In 2D animation, everything is fully planned out, full extended rooms are drawn,
> character turnarounds are drawn, then the scenes, individual characters, and sectioned
> off backgrounds get drawn out and created separately and then composited."
> — Sean, 2026-08-31

## Why it exists

Corners were being generated independently and checked for continuity **afterwards**, which
makes continuity something you *catch* rather than something that is *true by construction*.
Three errors followed and they are all the same root cause:

| # | The error | What the bible does about it |
|---|---|---|
| 1 | Codex's rack and Gemini's moodboard both claimed the same end of the same wall — S05 put the CRT wall at the moodboard's frame-left, S04 put the rack there | Every fixture has ONE wall and ONE left-to-right position. The moodboard runs the south wall; its east end meets the CRT wall, its west end meets Codex's corner. **S04 is therefore mirrored** relative to the plate we had |
| 2 | The CRT was two different fixtures — near the ceiling in S05, at shelf height above a credenza in S07, and a different television in each | ONE fixture at ONE height: **sill 6′6″**, above the credenza on the east wall. The elevation draws it once |
| 3 | Gemini stood on the baseboard instead of the floor | Not a plan problem — the composite prompt had dropped the *"soft graphite contact shadow"* clause the proven S04 prompt carried. Fixed in the prompt, not here |

## The sheets

| File | What it settles |
|---|---|
| `ROOM-01-ground-plan.png` | Which wall carries what, and where every camera stands with its view cone |
| `ROOM-02-elevations.png` | Left-to-right order and every height, all four walls unrolled at one scale, with a numbered key |
| `ROOM-ELEV-{n,e,s,w}-rough.png` | The bare composition rough per wall — fixtures only, no numbers, no guides |
| `SHOT-S0X-rough.png` | **The room projected through each camera.** [`make_shot_roughs.py`](make_shot_roughs.py) puts a lens in the plan and renders what it actually contains, so a corner rough can no longer disagree with the plan it came from — hand-drawn roughs could, and did |
| `elevations/ELEV-{north,west,east,south}-v2.png` | **The drawn room**, rev 2. Pencil-test register, flat straight-on, canonical cream. East is `-v3` (its moodboard wrap re-rolled to match the south wall). Rev 1 preserved at `elevations/old/` |

## The shot roughs solve their own cameras

[`make_shot_roughs.py`](make_shot_roughs.py) takes a camera **position**, the fixtures the shot
is **about**, and how much of the frame they should **fill** — then solves heading, pitch and
field of view. Three things had to be learned the hard way and are worth keeping:

1. **Clip, never clamp.** Geometry behind the lens has to be near-plane clipped. Clamping depth
   to a small positive number made every box with a corner behind the camera project to
   something enormous — six frames of solid grey.
2. **`up = forward × right`, not the other way round.** The other order renders the room upside
   down, which looks like a projection bug and is really a handedness bug.
3. **Pitch has to be solved too.** From 10 ft away with the lens at 5′6″, keeping the foot of a
   wall in frame needs either an 89° lens or a camera that tilts like a real one. Two passes
   tried to fix that with field of view alone — one produced shots that were all crop, the next
   produced shots that were all wide-angle.

Re-cameraing a shot is now a one-line edit. Change the position or the subject, re-run, $0.

## The order of operations, and it does not vary

1. Ground plan → 2. elevations → 3. **rendered elevations** → 4. corner plates generated
against their wall → 5. characters composited from the real turnarounds → 6. motion →
7. timing. Nothing jumps the queue.

**Steps 1-5 are done as of 2026-08-31.** All six Movement 1 setups carry their character;
the composites are at `../composites/rev2/`, normalised into `../normalised/`. Step 6 does
not start until Sean has approved the frames, and timing is not discussed until then.

## The rendered elevations are the new style bible

They replace `probe-205/U-codex-corner.png`, and the measurement says why. Plates generated
against the old S04 bible needed paper gains of **1.08–1.27** to reach canonical. The four
elevations, generated against the normalised S02, came back needing **1.01–1.03**. The bible
was the drift; changing it fixed the drift at source rather than in post.

## Character turnarounds — use them

Five-view sheets for all four mascots have existed since 2026-06-30 at
`runs/Act-Rework-Backlog/02-AI-company-character-refs/`. They went unused for two months,
and three Gemini composites were spent asking a model to invent a back view that was
already drawn. **They are now the composite source.** The five views of each sheet, plus
Sean's, are cut out at `../refs/turnaround-views/` (segmented by ink-column valley,
upscaled 3x) — pick the view that already faces the way the shot needs rather than making
the model rotate one.

## Room states

The set is not one thing across the film. Movement-2 additions are drawn **in red** on both
sheets so no later beat has to invent a fixture the room never had.

| State | When | What is different |
|---|---|---|
| **A · quiet** | M1, beats 1–3 | the room as drawn |
| **B · chaos** | M2, beats 5–9 | paper everywhere; the CODE WALL lit above Codex's counter (beat 6); concepts taped over every surface (beat 7); **THE HOLE** blown in the north-east wall with the half-built rocket leaning out of it (beat 8); the SHIP IT bell and confetti cannon firing hollow (beat 9) |
| **C · after** | M3 | still wrecked, but calm. The wreckage is the joke's evidence |

## The S07 re-roll — what was wrong and what fixed it

Sean, 2026-08-31: *"I'd want to re-roll the CRT alarm wall. There isn't a line where the
corner should be and some objects are facing right while a couple of others face left."*

He was right and the geometry agreed: the SE corner bears 28.6 degrees against a 41.2
degree half-angle, so it is 88% of the way to the right edge and firmly in frame, and
`SHOT-S07-rough.png` draws its seam. The plate came back with no seam at all and the
sketch wall on the same flat plane as the credenza.

**The camera was never the problem** — Sean approved the rough, and it was not touched.
Three things in the prompt were, and the re-roll landed on the first roll:

1. **Two elevations, not one.** S07 was the only rev-2 plate given a single elevation.
   Every corner that came back correct — S03, S04, S06 — had two. A flat reference plus a
   nearly-square rough look alike to the model, and the elevation's orthographic camera
   wins.
2. **The perspective stated in words** — where the vanishing point sits, which side of it
   shows a right-hand face, and that the baseboard is not a level line.
3. **The VISIBLE list made to agree with the rough.** The failed prompt listed the
   dartboard as OUT OF FRAME while the rough puts it in the left third. A VISIBLE list
   that contradicts the rough is a contradiction, and the model resolved it by copying
   the elevation. The rough solves the frame; read the frame off it.

Full wording and the general rule: [`../prompts/_blocks.md`](../prompts/_blocks.md).

## Known, and not yet fixed

- **The coat rack landed beside the bell** rather than above the storage bench on the north
  wall. Cosmetic; nothing crops there.
- Rev 1's landscape sketches are fixed on both the south wall and the east wall's wrap. If a
  later re-roll of either wall drops the concept-sketch clause, they will come back.
