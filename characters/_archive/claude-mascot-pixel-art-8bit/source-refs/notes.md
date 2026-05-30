# Claude Mascot — voice + style notes for Cy

*Cy: this is your second Bible. The first (sean-anchor) authors against the pencil-test-colored register. This one authors against pixel-art-8bit. Different register, same schema — your job is to prove the schema is style-agnostic by construction.*

---

## Style register

`pixel-art-8bit`. The mascot is a chibi-proportioned indexed-palette pixel-art character, rendered with integer-pixel-grid alignment and no anti-aliasing between palette steps. The aesthetic is *not* modern smooth-edge pixel art with smoothed gradients — it's the older 8-bit / 16-bit register where every pixel sits on a grid square and every color is one of a small closed palette.

The references in this folder show the mascot at three poses; read them as palette + proportion authority. If your output character.yaml carries any register other than `pixel-art-8bit`, the defang pass failed and you should stop and surface the failure.

## Palette

Four indexed colors. Cy: extract these from `anchor.png` and record them as named entries in `character.yaml.palette`:

  - **Primary orange** (≈ `#E89B6B`, ±10 RGB tolerance) — skin, body fill, exposed limbs. The character's dominant color across the silhouette.
  - **Cream highlight** (≈ `#F4DDB8`) — face highlight, top-of-head shine, fingertip highlights. Used sparingly; defines the lit areas.
  - **Warm brown shadow** (≈ `#A86B45`) — under-jaw shadow, fold lines, outer contour shadow side. The mid-tone between primary and the deep brown.
  - **Deep brown** (≈ `#5C3A24`) — eye dots, mouth line, accent strokes, the darkest accent in the palette.

No gradients, no anti-aliasing between palette steps, no out-of-palette colors. The palette is the load-bearing identity signal at the sub-32px display sizes where pixel-art characters typically render.

## Proportion

Chibi-leaning. Head height ≈ two-thirds of total body height (1:1.5 or 2:3 head-to-body ratio, measured crown-to-feet). Body width at shoulders ≈ 1.2× head width. The silhouette reads as a round-topped lozenge rather than a standing figure. This proportion is the load-bearing recognizability cue at sub-32-pixel display sizes — get it wrong and the mascot stops reading as the mascot.

## Style invariants

  - **Integer-pixel grid.** Every edge, every contour, every color boundary lands on an integer pixel coordinate. Diagonals render as stair-stepped pixel runs, not as smoothed sub-pixel gradients.
  - **No anti-aliasing between palette entries.** A diagonal transition from primary orange to warm brown is a stair-step of those two literal colors; not a smoothed gradient of intermediate values.
  - **Dithering pattern** (where used in shadow areas): vertical 2-pixel-spaced dots in the warm-brown shadow color over the primary orange fill. No other dither patterns are in the register's vocabulary.

## What's not covered

  - **Motion plates**: none yet. The mascot has no walk cycle, no idle animation, no head turn drawn. A Phase 6 motion shot involving the mascot needs motion plate authoring first — Cy's risk-bible should name this gap explicitly.
  - **Expressions beyond the three source references**: neutral, surprised, contemplative are the three poses the references cover. A full emotional range would need authoring before Em can cite expression-specific rules.
  - **Costume variants**: none. The mascot is its own design; no secondary costumes (hats, tools, accessories) exist in commit 2.
  - **Lit / unlit variants**: no. The mascot's palette is fixed; a "neon-lit" or "candle-lit" variant would be a style-register escalation to a separate Bible.

## Source refs in this folder

  - `anchor.png` (designated from `claude-mascot-2.png`, 2048×2048) — the canonical identity reference. Cy reads this at every Pass-1 rule emission.
  - `claude-mascot-1.png` — alternate pose / lighting study; useful for inferring the silhouette + secondary contour rules.
  - `claude-mascot-3.png` — alternate pose; useful for inferring proportion at different angles + the contour-rendering style.

---

*Cy: this is the structural validation that the architecture supports arbitrary 2D styles, not just pencil-test. If your Pass-1 output for this character carries any pencil-test vocabulary (cross-hatching, graphite line weight, cream paper texture, construction lines beneath the drawing), the defang pass failed and the rules are wrong. Cite the pixel-art vocabulary explicitly: indexed palette, integer-pixel grid, dithering pattern, sub-pixel boundary, palette-step transition.*
