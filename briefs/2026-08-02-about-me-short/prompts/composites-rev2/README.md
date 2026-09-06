# Composite prompts — rev 2, the room-bible plates

Five prompts, one per character, written 2026-08-31 against the rev-2 plates in
`plates/rev2/`. Read [`../_blocks.md`](../_blocks.md) first — it carries the scale law and
the rest-pose law that these are built on.

| File | Character ref | Plate | Rolls | Result |
|---|---|---|---|---|
| `S02-sean.txt` | `refs/turnaround-views/sean-v5.png` (back) | S02 | 1 | seated in the existing chair, back to camera |
| `S03-claude.txt` | `claude-v4.png` (¾ back) | S03 | 1 | scale 0.97 of intended, the best in the set |
| `S04-codex.txt` | `codex-v3.png` (¾ back, facing right) | S04 | 2 | v2 shipped; v1 kept for its better silhouette |
| `S05-gemini.txt` | `gemini-v4.png` (¾ back) | S05 | 2 | v2 shipped; v1 kept as the record of the scale miss |
| `S06-grok.txt` | `grok-v4.png` (¾ back) | S06 | 2 | v2 shipped; v1 kept |

Superseded prompts are in `old/`, named for how they failed rather than by version number,
because the failure is the useful part.

## The recipe, and the two clauses that must never be dropped again

Per `prompt-how-much`: role-tag both refs, keep Image 2 unchanged, one scale clause, one
position clause, style token, anti-text, and **never re-describe the scene**. On top of
that, two clauses this project has already paid for once:

- **`with a soft graphite contact shadow`** — dropping it is what put Gemini on the
  baseboard. It is in all five.
- **feet, explicitly** — *"both feet flat on the floor and well clear of the baseboard."*

## Pick the view that already faces the right way

The turnaround crops in `../../refs/turnaround-views/` give five views per character. S04's
rack is at frame-right, so Codex came from `codex-v3` (¾ back facing right) rather than
asking the model to rotate `codex-v4`. One less thing for it to get wrong.

## NSFW, settled

Grok's aggressive turnaround is fine to pass as a reference image. The July refusal was on
the **prose** — "grey gremlin shape, bat ears, red eyes, fanged grin", "arm cocked back
mid-throw". `S06-grok.txt` reuses the softened wording verbatim and it passed again.
