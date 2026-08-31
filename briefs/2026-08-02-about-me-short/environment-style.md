# Environment style — the About-Me short

The binding look of the HQ set, and the **palette clause** every plate prompt carries
verbatim. Written 2026-08-30 before any Movement 1 plate generated, because plates
generated per-angle drift apart otherwise — and that drift is measured, not feared.

## The measured problem

Three existing assets, three different creams:

| Asset | Paper | Floor |
|---|---|---|
| `art-viz/route-c--gpt-ref.png` — **the hero-frame anchor** | **#e5d7c2** | #dbccb9 |
| `probe-205/D-clean-plate.png` | #d5be99 | #9f7862 |
| `cast-scale-lineup.png` (model sheet, not a scene) | #faf0db | — |

A **37-level spread in red and 66 in blue** between the lightest and darkest. Cut two of
these together and the room changes colour on the cut. The hero frame is canonical — the
studio brief names it the hero-frame anchor — so every plate matches **it**, not the probe
plate.

---

## THE PALETTE CLAUSE — paste verbatim into every plate and composite prompt

> Warm cream drawing paper throughout, a light putty cream (#e5d7c2), never white and never
> yellow. The floor is the same cream a half-step darker (#dbccb9). Walls and floor are
> flat, quiet, and low-contrast — the room is a pale ground, and colour lives only on the
> characters and on small props. Graphite line and cross-hatch shadow carry all the form.
> Overall value stays high-key and even: no dark corners, no pooled shadow, no colour cast,
> no vignette, no dramatic lighting.

**Never edit the clause per shot.** If a shot genuinely needs a different key — a night
beat, the alarm's red flood — that is a **post** treatment, not a generation change
(FIRST LICKS DR #41: the look lives in post; every plate generates CLEAN).

## Verifying a plate against the clause

Sample the upper wall and the floor and compare to the canonical pair. Tolerance **±8
levels per channel**; past that, re-roll rather than accept. Frame-delta means are not a
valid signature here (FIRST LICKS retired them — they scale with plate texture); for
checking a *surgical edit* preserved a plate, use an edge-diff heatmap and FFT phase
correlation instead.

```
sample upper wall  → target #e5d7c2  (229, 215, 194)  ±8
sample floor       → target #dbccb9  (219, 204, 185)  ±8
```

---

## Spatial placement map

See [`M1-STORYBOARD.md`](M1-STORYBOARD.md) for the full map. Summary, west→east:
doorway · Claude's nook · Codex's rack · **Sean's desk, centre** · Gemini's moodboard with
the **CRT high above it** · Grok's dartboard and hole in the wall. Ground line y=700 in
every guide.

**The USER does not appear in the room.** Ruled by Sean 2026-08-30: a figure standing in
the doorway read wrong. The USER is introduced **on the CRT screen** instead — the TV
flashes `PROBLEM!`, then cuts to the USER *in* the television. The doorway stays as set
dressing only, and no plate places a figure in it.

---

## Framing and motion grammar — from *Goofy Gymnastics* (1949)

Watched 2026-08-30 at Sean's direction. The short's actual grammar, and it contradicts
Movement 1's first boarding in one important way.

**1. Establish once, then abandon the set.** There is exactly one wide of the full gym
(≈1:29). Every gag after it plays against a **near-empty flat wall** — one baseboard line,
one prop, nothing else. The room is established so it can be *left*.

**2. The character owns the frame.** In gag shots Goofy fills 60–90% of frame height. He is
never a small figure in a furnished room.

**3. Shot scale swings hard.** Wide → full figure → medium → tight low-angle (the chin-up
is shot from below with only a blank wall behind). Cutting between scales *is* the comedy
rhythm.

**4. One recurring anchor prop carries the joke.** The muscle-man chart is returned to
again and again, always with Goofy collapsed at the bottom of it. Our equivalent is the
CRT.

**5. Backgrounds are flat colour fields.** No texture, no clutter, no detail competing with
the character.

### What this changes

Movement 1 was first boarded with **knee-high mascots in furnished corners** — the opposite
of this grammar. The corner shots should push in so the mascot **owns the frame**, against a
**much emptier wall**.

This also happens to solve a measured engineering problem. Probe-205's background drift of
**22–27%** was measured on the busiest surface in the room — a moodboard wall of dozens of
small sketches. A flat wall has almost nothing for the model to re-invent. **The Goofy
grammar and the drift fix are the same move: emptier backgrounds, bigger characters.**
