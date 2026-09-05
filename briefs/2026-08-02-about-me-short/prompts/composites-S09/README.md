# S09 composites — five characters into the CRT-POV plate (beat 3½)

Written 2026-09-03 at Sean's ask, $0. Five edits, **each onto the CLEAN plate**
`normalised/S09-room-reacts-v1.png`, never onto each other — then a deterministic merge
(`post/merge_edits.py`) lifts each character off its edit by difference against the plate and
lays all five onto the pristine plate. Why not chain: five chained edits compound whatever each
one drifts, and Codex and Gemini (the same colour family, corrupted 4/4 in July) would have to
sit in one pass. Independent edits keep the plate byte-true and keep them apart. This is also
the first real run of the matte-and-relay idea (open item 8), in still form — **and the matte is
proven**: calibrated 2026-09-03 on the S10 Sean composite, it lifts the figure and chair whole
(13% of frame) and pastes nothing else; the merge is seamless by eye. Zones per character are in
`motion/run_S09_composites.sh`.

| Order | File | Character ref | Where | Scale anchor |
|---|---|---|---|---|
| 1 | `S09-claude.txt` | `claude-v2.png` (¾ front) | far wall, foot of the paper towers | the tall tower (5′6″) |
| 2 | `S09-codex.txt` | `codex-v2.png` (¾ front) | far wall, foot of the server rack | the rack (7′5″) |
| 3 | `S09-sean.txt` | `sean-v4.png` (¾ back) | in the chair at the desk, right wall | the desk / monitors |
| 4 | `S09-gemini.txt` | `gemini-v2.png` (¾ front) | left, on the floor by the worktable | the wall of sketches |
| 5 | `S09-grok.txt` | `grok-v2.png` (¾ front) | near right, on the open floor | the desk top |

Order is depth: far first, near last, so the merge resolves any overlap correctly.

**Rest poses, all of them** — nobody is reacting yet. The clip does the reaction
(`prompts/motion/21-M2-S09-room-reacts-DRAFT.txt`). Every mascot is ¾ front to us with its eyes
on its own task (the facing law); Sean is at the keyboard with his back ¾ to us, so that his
chair-spin to the lens is the biggest visible action at his scale.

**Known deviation, recorded:** the plate's chair came back turned to the room. `S09-sean.txt`
asks the edit to seat him facing the desk in that chair, which means redrawing the chair in
place. If that fails, the fallback is Sean seated as the chair is, already turned — and event 1
of the clip loses his spin.

```
motion/run_S09_composites.sh            # five edits off the clean plate, 42.5 cr, spend guard on each
python post/merge_edits.py normalised/S09-room-reacts-v1.png composites/S09/S09-claude-v1.png ... -o composites/S09/S09-all-v1.png
```


## Run 2026-09-03 — 42.5 cr, five first-roll landings, merge pass

All five edits completed; the merge pasted 0.25 / 1.16 / 2.50 / 0.89 / 2.39 % of the frame
(Claude / Codex / Sean / Gemini / Grok) and `verify_edit` on the merged frame against the plate
reads **phase 0.784 · edge keep 0.954 · shift (0,0) · pass** — the plate is byte-true outside the
five figures, which is the whole point of the route. Normalised (gain 1.000–1.004).
`composites/S09/S09-all-v1.png` → `normalised/S09-all-v1.png`. Per-character results in each
prompt header; masks in `composites/S09/masks/`.

## 2026-09-04 — Sean: "Grok looks like you photoshopped it in." Diagnosis, and the A/B

Two causes, both real, checked against the raw Grok edit side by side with the merged frame:

1. **The matte clipped him.** At threshold 18 / dilate 10 the mask missed the thin extremities
   — the outer tip of his right ear and the end of his tail are cut flat in `S09-all-v1.png`
   but whole in the raw edit. Re-merged at threshold 12 / dilate 22 as `S09-all-v1b.png`, $0;
   the tool's docstring now says so.
2. **The model drew him differently from the other four.** Bare graphite, no coloured-pencil
   wash, a heavier contour, and the sneer. That is the edit itself, not the paste — the raw edit
   shows the same drawing. The single-character prompt never said "wash"; the one-pass prompt
   does, for all five.

The A/B: `S09-all-onepass.txt` puts the plate and all five character views into ONE
`gpt_image_2` call (8.5 cr) and lets the model integrate them itself, no matte. Whichever of
one-pass / matte Sean's eye picks becomes the S09 route — and the answer generalises to every
ensemble beat left in the film (15, 16).

### The A/B result, 2026-09-04

| | matte (`S09-all-v1b.png`) | one-pass (`S09-all-onepass-v1.png`) |
|---|---|---|
| Grok | sneer, bare graphite, no wash | **cheerful, on-model, washed** |
| Codex | **bracket-and-dash face held** | grew round eyes + a mouth |
| Sean / Claude / Gemini | landed | landed, with wash |
| plate vs clean plate | **0.784 / 0.954 pass** | 0.091 / 0.580 (whole-frame re-render) |
| integration | figures read slightly cut-in | figures sit in the drawing |

Neither wins outright. The one-pass integrates better and the matte holds identity better —
which is the July finding in miniature: the more characters in one call, the more the
same-colour-family pair bleeds. Sean's eye decides; the next roll is one of two 8.5-cr fixes
(one-pass re-roll with a hard Codex face lock, or a Grok-only single edit with the v2 eyes +
wash, re-merged).

### v2 one-pass, reference-only (Sean's question: are the words competing with the reference?)

Ran it. **Negative, and decisive.** Without the description lines Codex and Gemini were conflated
(a star-ish thing at the rack, a cloud at the worktable, each wearing the other's face) and Grok
went back to the sneer. The description line is an identity LOCK, not a competitor — with it, the
one-pass held Grok's mood and kept the pair apart; without it, the two lavender references bled
into each other. The failure is structural to five references in one call (the July finding,
now on gpt_image_2), so:

**Route ruled by evidence: singles onto the clean plate + matte** (identity held 5/5), with the
one thing the one-pass taught folded back into the singles — say "light coloured-pencil wash"
and give Grok the v2 eyes. `S09-grok-v2.txt` is that roll: 8.5 cr, re-merge at $0.

### S09 closed, 2026-09-04 — `normalised/S09-all-v2.png`

Reference fixed first (`prompts/refs/grok-v2-friendly.txt` → `refs/turnaround-views/grok-v2-friendly.png`,
8.5 cr, first roll), then Grok re-rolled as a single off it (`S09-grok-v2.txt`, 8.5 cr, first roll) and
re-merged with the four v1 singles: **phase 0.694 · edge keep 0.915 · pass**. All five on-model, all
five washed, Codex's face intact, Grok on the affection side. Day's S09 route-finding: 34 credits for
four generations, all first roll; the two one-pass A/Bs are kept as the negative evidence.

### REJECTED by Sean, 2026-09-04: "Codex is cut off and Grok looks like an anime character."

Checked: **the Codex single edit is whole** (`S09-codex-v1.png`, standing in front of the rack's
left edge). **The matte cut him** — where his body overlaps the rack, the difference against the
plate fell under threshold and the plate's rack was kept over his right half. Second matte
failure of the day, different from the first (thin extremities). The merge tool is not
trustworthy where a figure overlaps a dark fixture; the singles are. Grok off the fixed
reference came back with glossy highlighted eyes — anime, not pencil-test. Sean is taking the
composite to the web app; every input is listed in the session hand-off below.

### CLOSED by Sean in the web app, 2026-09-04 — `normalised/S09-all-webapp-v1.png` ✓S

Sean took the kit (plate, the five views, the DESCRIBED one-pass prompt) to the ChatGPT web app and
finished it in a few rounds: **`composites/S09/S09-all-webapp-v1.png`** (1672×941, normalised at
gains 1.008–1.022). Intermediates kept at `composites/S09/webapp/`. Two design decisions he made
on the way, both now on disk as turnaround sheets in `refs/turnaround-sheets/` with the five
views cut into `refs/turnaround-views/`:

- **Claude sits and writes on a sheet of paper** (`claude-sitting-writing-turnaround.png` →
  `claude-sitting-v1..5`) — because that is what it was doing in the locked M1 beat-2 clip.
  Continuity of action across the cut, not just of design.
- **A new friendly Grok**, drawn as a whole turnaround rather than a one-view patch
  (`grok-friendly-turnaround-with-dart.png` / `-without-dart.png` → `grok2-dart-v1..5`,
  `grok2-v1..5`). Round red-orange eyes, brows up, the sawtooth grin kept. This SUPERSEDES
  `grok-v2-friendly.png` (my single-view fix, which came back anime-eyed) and `grok-v2.png` as
  the Grok composite reference. Use `grok2-v2` (¾ front) from here.

The CLI route's five singles and both one-pass A/Bs stay on disk as the record of what the
model does on its own; the shot itself was closed by hand-in-the-loop in the web app.
