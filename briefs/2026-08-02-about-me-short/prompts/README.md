# Prompts — the About-Me short

Every prompt that generated an image or a clip for this film, verbatim, with its result and
**why it won or lost**.

**Two sets live here, written by two sessions.**

- **`probe-205/`, `plates/`, `titlecards/`, `motion/`** — the *route-finding* record, recovered
  2026-08-31 from the 2026-08-30 session transcript and the Higgsfield job records (which echo
  `params.prompt` back on every call). These carry job ids and the measured verdicts that
  settled the production route. Several are kept **because they failed**.
- **`S0X-*.txt` at the top level + [`_blocks.md`](_blocks.md)** — the *production* prompts,
  written the same night by the following session, which generated the S03 v2 / S05 / S06 / S07
  plates and their composites. **`_blocks.md` is the authority** on the shared palette and
  register blocks and on the reference-role split; read it before writing a new plate prompt.

Where the two disagree, `_blocks.md` and the top-level `S0X` files are newer and win.

**These are working documents, not an archive.** The header comment on each file is the
useful part — a prompt that failed is often more instructive than one that worked, and the
failures are kept deliberately rather than deleted.

Per `prompt-how-much`: keep prompts in `.txt` and pass them as
`--prompt "$(cat p.txt)"` — apostrophes break inline.

---

## Index

### `plates/` — the film's shots

| File | Job | State |
|---|---|---|
| `S02-sean-desk-medium-APPROVED.txt` | `7f76489b` | **Approved — the opening shot** |
| `S02-hq-wide-CUT.txt` | `c3367ac0` | **Cut.** Kept as the reference implementation of the re-angle reconstruction pattern |
| `S03-claude-nook-SPARSE-superseded.txt` | `9a517bac` | **Superseded.** Its bare-wall paragraph is the one Sean reverted. Already re-done — see `../S03-claude-nook-plate.txt` and `plates/S03-claude-nook-v2.png` |

### Top level — the production prompts (newer, and the ones to copy)

| File | Produces | State |
|---|---|---|
| [`_blocks.md`](_blocks.md) | — | **Read first.** Shared palette + register blocks, the ref-role split, and a session log with per-edit phase-corr scores |
| `S03-claude-nook-plate.txt` | `plates/S03-claude-nook-v2.png` | The prop-rich re-do after Sean's reversal |
| `S05-gemini-moodboard-plate.txt` | `plates/S05-gemini-moodboard-v1.png` | |
| `S06-grok-dartboard-plate.txt` | `plates/S06-grok-dartboard-v1.png` | |
| `S07-alarm-plate.txt` | `plates/S07-alarm-v1.png` | |
| `S03-claude-composite.txt` | `composites/S03-…-composite-v1.png` | phase-corr 0.52 |
| `S05-gemini-composite.txt` | `composites/S05-…-composite-v1/v2/v3.png` | **v3 is the lean** |
| `S06-grok-composite.txt` | `composites/S06-…-composite-v1.png` | phase-corr 0.47 |
| `S07-alarm-off.txt` | `composites/S07-alarm-screenoff-v1.png` | Screen-dark keyframe, phase-corr 0.47 |

### `titlecards/`

| File | Job | State |
|---|---|---|
| `cardD-sean-thinking-APPROVED.txt` | `3744d9e3` | **Approved** |
| `cardA-gang-in-letters.txt` | `b8939f2e` | Not selected. One change needed if revisited: Sean's scale |

### `motion/` — Seedance

| File | Job | State |
|---|---|---|
| `04-single-character-7s-ADOPTED.txt` | `4784e9ae` | **The adopted recipe.** Sean: *"very cartoony… beautiful motion"* |
| `05-single-character-4s.txt` | `26ea565b` | Duration control for 04 |
| `06-single-character-7s-STD-REJECTED.txt` | `52555e19` | **Rejected** — std stutters |
| `03-inscene-4s-LIVELY-rebuilt.txt` | `0927d4a7` | The rebuild: +55% energy, no drift cost |
| `01-inscene-4s-TIMID-do-not-copy.txt` | `0dd48945` | **Counter-example.** ~40% negation + damping words |
| `02-green-field-4s.txt` | `dcb1e9e9` | Green-screen route, withdrawn |

### `probe-205/` — the route-finding experiments

| File | Job | What it settled |
|---|---|---|
| `B-gpt-with-cast-reference.txt` | `071eaecf` | **GPT + refs holds identity AND keeps the tooth** |
| `A-gpt-textonly.txt` | `45d96bc1` | Text-only drifts — why every plate carries the lineup |
| `C-nano-banana-with-reference.txt` | `4597be95` | NB2 is cleaner and flatter; also proved the stale naming trap |
| `U-codex-corner-single-character.txt` | `6505a009` | **The prompt shape to copy** for character-into-plate |
| `F-composite-INTO-plate-gpt.txt` | `bdb29698` | GPT wins the edit — phase-corr 0.412 |
| `G-composite-INTO-plate-nano-banana.txt` | `6b6c00cb` | NB2 re-renders — phase-corr 0.077 |
| `D-clean-plate-empty-room.txt` | `2a775770` | The composite destination |
| `E-characters-on-green.txt` | `6c79ecd0` | Green measured studio-flat; route still withdrawn |

---

## The laws these prompts encode

Each was paid for. Full reasoning in
[`CONTINUATION-2026-08-30-movement-1.md`](../CONTINUATION-2026-08-30-movement-1.md).

1. **Seedance takes NO negative prompts.** `NO MOUTH` does nothing. State locks
   **positively**: *"its face stays a pale chevron, one dot eye and a short underscore bar."*
2. **Damping words dampen.** "light taps", "small bounce", "feet planted" produced timid
   acting. Genre anchor + vivid verbs + zero negation gave **+55% motion energy with slightly
   less drift.** Liveliness and stability are not in tension.
3. **State SCALE and FACING in words.** Neither is ever inferred. The wide was cut because
   facing went unstated and every character addressed the lens.
4. **Composite prompts ≤70 words, and never re-describe the scene.** An 85-word prompt cost
   NB2 the entire plate; the 65-word version scored the best plate preservation of the run.
5. **Reference the previous plate as the style bible**, not the hero frame. Plate-to-plate
   matching beats matching both to a third image — and it matters more than usual here,
   because the film has **no establishing wide** to orient from.
6. **The palette clause goes in verbatim.** Canonical cream **#f5e8d1**, re-based to what GPT
   Image 2 actually produces. The floor target is **provisional** — do not enforce it.
7. **Post look lives in post.** Every plate and composite generates CLEAN.
8. **Use SINGLE-CHARACTER refs for composites, not the five-character lineup** — added by the
   production session. `refs/char-{claude,gemini,grok}.png` are 3×-upscaled crops of the
   lineup. Handing an edit all five characters invites the Codex/Gemini colour-family confusion
   that corrupted four July generations; one character per ref removes the question. The
   lineup stays correct for *plate* and *title-card* generation, where the whole cast is wanted.
9. **Grok's description can trip an NSFW refusal.** "Bat ears, red eyes, fanged grin" plus
   "arm cocked back mid-throw" returned `status: nsfw` with no image. The same character and
   action as "a round grey cartoon creature with big pointed ears, a wide friendly cartoon
   grin", "one arm drawn back holding a small dart, cheerful and mid-play" passed first time.
   `S06-grok-composite.txt` carries the wording that works.

## Standing model routing

| Job | Model | Note |
|---|---|---|
| Plates, composites, title cards | `gpt_image_2` 2k / `high` | |
| Re-angles of the set | **not** `gpt_image_2` | It cannot re-camera from an edit |
| Motion | `seedance_2_0` **`fast`**, 7s, 720p, `generate_audio:false` | `std` stutters |

## State of Movement 1 as of 2026-08-31

Plates exist for **S02, S03 v2, S04, S05, S06, S07**; composites for **S03, S05 (v1–v3),
S06, S07-off**; title card **D** approved. **S01's typography and all motion beyond S04's
proven 7s clip are the open work.** `M1-STORYBOARD.md` is the live tracker — this file only
covers prompts.
