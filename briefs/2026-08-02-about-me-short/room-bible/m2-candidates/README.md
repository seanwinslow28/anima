# Movement 2 — candidate cameras (2026-09-03)

**Why this folder exists.** Sean's ruling of 2026-09-02: *no cutting back to a corner in the
same angle unless the frame is visibly wrecked and the motion is chaotic.* Beats 5, 6, 7 and
8 all revisit corners the audience met in beat 2, so each needs a camera decision — and he
has said plainly he cannot judge staging from prose. So the session roughed every candidate
angle at $0 with [`../make_shot_roughs.py`](../make_shot_roughs.py) and put the pictures in
front of him. **Nothing here is ratified.** The cameras live in
[`../m2_candidates.py`](../m2_candidates.py); the sheets are built by
[`make_sheets.py`](make_sheets.py).

```
python3 ../make_shot_roughs.py m2     # re-rough the candidates only (M1 roughs untouched)
python3 make_sheets.py                # rebuild the five contact sheets + the camera map
```

## What the roughs show, and what they do not

- **Grey blocks** are fixtures from the one-source-of-truth `WALLS` table, exactly as the M1
  roughs draw them. **Red blocks** are the Movement-2 additions already placed in that table
  (THE CODE WALL, THE HOLE). **Green blocks** are the cast standing at their real heights
  (Sean 6.0 ft; Grok 0.42 / Codex 0.36 / Gemini 0.30 / Claude 0.26 of him) — silhouettes for
  scale and placement, never drawings.
- The solver caps the lens at 86° horizontal. Every wide here hits that cap, which is honest:
  a 26′ room from one wall is a wide lens or a crop, there is no third option.
- Beat 3½ draws **room state A** — the room reacts before anything is wrecked.
- The six M1 roughs were regenerated with the extended solver and are **byte-identical**
  (md5-checked 2026-09-03), so nothing M1 was generated against has moved.

## The candidates

| Beat | Sheet | A | B | C | Lean |
|---|---|---|---|---|---|
| 3½ the room reacts | `sheets/B3h-sheet.jpg` | THE ALARM LOOKS BACK — lens at the CRT glass, 7′9″ up | BIRD'S EYE from just above the CRT | THE HIGH CORNER — not a POV, the room's long diagonal | **A** |
| 4 the silent GO | `sheets/B4-sheet.jpg` | FROM THEIR HEIGHT — lens at a mascot's eye level, 2′3″, looking up at Sean | EYE LEVEL medium | OVER THEIR SHOULDERS — Grok and Claude's backs in frame | **A** — Sean ruled 2026-09-03 |
| 5 Claude | `sheets/B5-sheet.jpg` | WORM'S EYE up the tower | HIGH DOWN into the nook | RAKING north along the west wall | **A** |
| 6 Codex | `sheets/B6-sheet.jpg` | SQUARE ON the code wall | LOW up the rack | HIGH DOWN on the counter | **A** |
| 7 Gemini | `sheets/B7-sheet.jpg` | THE WRAP corner | RAKING east along the board | HIGH DOWN on the worktable | **B** |
| 8 Grok | `sheets/B8-sheet.jpg` | THE S06 CAMERA, wrecked | LOW and square to the hole | HIGH DOWN on the rubble | **A** |

`sheets/camera-map.jpg` puts every lens on the ground plan with its solved field of view.

**Ruled 2026-09-03 (Sean):** every lean above taken; 3½ is **A** and locked; beat 4 is **B4-A**
with the silent GO (nod → finger-twirl → slam back to the keyboard). Both turns — the room to
the CRT, the mascots to Sean — happen inside the 3½ clip; the cut lands on Sean's face.
Proposed setup names, not yet ratified: **S09** = the CRT-POV reaction, **S10** = Sean from
the room (serves beats 4, 12 and 13). Prompts: `../../prompts/plates-rev2/S09-room-reacts.txt`,
`S10-sean-front.txt`, `../../prompts/composites-frontal/S10-sean.txt` (the face look-test),
`../../prompts/motion/20-…-DRAFT.txt` and `21-…-DRAFT.txt`.

**Plate roughs.** Every candidate also renders as `SHOT-<id>-plate-rough.png`: the identical
solved camera with the cast NOT drawn. That is the file a plate prompt hands to the generator;
the green blocks never reach a model.

## Two things tried and dropped, recorded so they are not re-bought

1. **A lens inside the CRT box.** The first CRT-POV roughs put the camera at x 25.4, inside
   the television's own 1.4 ft depth, and rendered solid grey. The screen face is x 24.6;
   the lens sits just in front of it.
2. **A raking angle on the code wall from the doorway.** The server rack stands between the
   doorway and the code wall and hides it completely from anywhere north of it. Beat 6's
   subject is the wall, so the raking angle cannot serve it; replaced with a high angle.

## From rough to plate

Each chosen rough is the plate's camera reference, per `../../prompts/_blocks.md`: role-split
refs — the two wall elevations of the shot as fixture/style bible with *"do NOT copy its flat
orthographic camera"*, the rough last as the camera, a PERSPECTIVE paragraph, a THE CORNER
paragraph for two-wall shots, and a VISIBLE list that agrees with the rough. State B plates
also need the wreck described (the red fixtures are drawn, the mess is not).
