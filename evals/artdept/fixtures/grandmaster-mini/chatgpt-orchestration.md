# ChatGPT orchestration (condensed) — GRANDMASTER

Full source (gitignored): `runs/2026-07-14-grandmaster-kid-design/ORCHESTRATION-PROMPT-FOR-CHATGPT.md`.

## The golden rule — character consistency (three prompt kinds)

1. **FRESH (no reference)** — full description + a "research the show" style
   line. Generate from text + web search. These establish identity.
2. **EDIT (one reference)** — the prompt gives only the *change* (pose /
   angle / age / added prop). Always edit the already-generated anchor of
   that same character in that same style, so identity + style carry. Never
   regenerate from scratch, never re-describe the character or the style.
3. **COMPOSITE (two references)** — feed both named anchor images; command
   scale + position; keep the background unchanged.

## Never cross styles

Two style folders (`primal grit/`, `samurai jack s5/`). A Samurai-jack
edit/turnaround/composite must reference **only** Samurai-jack anchors; a
Primal edit must reference **only** Primal anchors.

## Dependency map (applies to EACH style)

- Wimpy boy anchor → FRESH. Trained boy anchor → EDIT of the wimpy anchor.
- Old-grandma anchor → FRESH. Young grandma → EDIT of the old-grandma anchor.
- Wide/medium scenes → FRESH (placeholder boy baked in).
- Turnaround sheet → EDIT, run once per anchor (wimpy, trained, old-grandma,
  young-grandma).
- Grandma reveal snapshot → EDIT of the young-grandma output.
- Grandma + boy keepsake photo → COMPOSITE (wimpy boy anchor + old-grandma
  anchor).

## Checkpointed batches

Work in small batches: generate one batch, save the files, show results, wait
for explicit "continue" before the next batch. Order: fresh foundations →
boys (trained anchor + turnarounds) → grandma (young + turnarounds + reveal)
→ composites.
