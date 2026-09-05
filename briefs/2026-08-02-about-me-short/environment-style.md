# Environment style — the About-Me short

The binding look of the HQ set, and the **palette clause** every plate prompt carries
verbatim. Written 2026-08-30 before any Movement 1 plate generated, because plates
generated per-angle drift apart otherwise — and that drift is measured, not feared.

## The measured problem, and the re-base

Three existing assets came back with three different creams — a **37-level spread in red**
between lightest and darkest. The first clause targeted the hero frame (#e5d7c2). Two plates
generated against it then came back **consistently lighter**, in the same direction both
times:

| Plate | Wall measured | Delta vs #e5d7c2 |
|---|---|---|
| S02 all-corners wide (cut) | (235, 218, 194) | +6 / +3 / 0 — pass |
| S02 desk medium | (245, 232, 209) | **+16 / +17 / +15** — fail |

**Ruled by Sean 2026-08-30: re-base the canonical cream to what the model actually
produces.** Fighting a consistent bias on every generation costs a re-roll each time and
buys nothing; consistency across twenty-odd plates matters more than matching the hero
frame, which was a style test and never appears in the film. Both new values are **measured
from real GPT Image 2 output**, not derived.

| | Canonical | RGB | Source |
|---|---|---|---|
| **Paper / wall** | **#f5e8d1** | (245, 232, 209) | the S02 desk medium |
| **Floor** | **#e8d6bc** | (232, 214, 188) | the S02 wide |

*Superseded: #e5d7c2 / #dbccb9 (hero frame). Kept here as the record, not as the target.*

---

## THE PALETTE CLAUSE — paste verbatim into every plate and composite prompt

> Warm cream drawing paper throughout, a pale putty cream, never white and never yellow. The
> floor is the same cream a half-step darker. Walls and floor are flat, quiet, and
> low-contrast — the room is a pale ground, and colour lives only on the characters and on
> small props. Graphite line and cross-hatch shadow carry all the form. Overall value stays
> high-key and even: no dark corners, no pooled shadow, no colour cast, no vignette, no
> dramatic lighting.

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
sample upper wall  → target #f5e8d1  (245, 232, 209)  ±8
sample floor       → target #e8d6bc  (232, 214, 188)  ±8   ← PROVISIONAL, see below
```

**The wall target is validated.** S03 measured (247, 235, 211) against it — delta 2/3/2, a
clean pass on the first plate generated after the re-base.

**The floor target is not, and should not be enforced yet.** It was measured from the CUT
all-corners wide — a furnished room with a rug, which is not what a sparse plate looks like.
S03's floor came back (242, 227, 201), 10–13 levels lighter, and **the plate is correct**:
in a bare Goofy-style setup the floor is barely a separate surface from the wall, which is
the look we want. The tolerance flagged a wrong target, not a defective plate. **Re-base the
floor once S05 and S06 give two more sparse samples** — do not re-roll good plates to hit a
number derived from an unrepresentative source.

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

### What this changes — and what Sean REVERTED

**Adopted: the character owns the frame.** Corner shots push in so the mascot fills a large
share of frame height, and every character's **facing** is stated (absorbed in its own task,
never addressing the lens). This is load-bearing — the all-corners wide failed precisely
because facing was unstated.

**REVERTED 2026-08-30: the bare wall.** S03 was first generated sparse, one prop against an
empty wall, and Sean ruled it out — *"it feels naked and weird. Like they're in an extremely
clean museum and not a workspace."* He is right and the reasoning was mine to get wrong:
**Goofy's set is sparse because it is a gym.** A break-room HQ where four agents are mid-
chaos is LIVED IN, and the clutter is characterisation — the tidy nook, the humming rack,
the fifty taped concepts, the darts in the wall are each a character's *portrait*. Strip them
and the corners say nothing.

**So the corners are prop-rich: supplies, boxes, binders, loose paper, the junk of a real
workspace.** Bare walls are not the house style.

**This re-opens a measured cost, and it should be planned for rather than rediscovered.**
Probe-205's background drift of **22–27%** was measured on the busiest surface in the room. A
prop-dense plate is exactly the condition Seedance re-invents. The drift mitigations
therefore carry more weight now: single-character plates (−18%), 7s duration, a locked
camera stated positively, and — still untested — matting the character out of the animated
clip and re-laying it over the pristine plate, which would make plate drift structurally
impossible.

---

## RULED 2026-08-31: normalise the paper in post. Every frame.

Sean: *"Normalize each in post. It makes the characters stand out more. They all seem to
blend or just not look right with the tan. They still look great, but it could get messy
down the line."*

**What had happened.** The four prop-rich plates all came back warmer and darker than
canonical `#f5e8d1` — by the same amount, in the same direction, within four levels of each
other. Not scatter: agreement with the wrong reference. They were the first plates generated
with the **S04 rack plate as their world/style bible**, and S04 predates this clause; its own
paper sits at **(218, 191, 152)**, some 27 / 41 / 57 levels warm of canonical. The clause and
the reference pulled opposite ways and the reference won about two thirds of the argument.

| Frame | Wall as generated | Gain applied | Wall after |
|---|---|---|---|
| S01 title card D | (247, 235, 212) | 0.99 / 0.99 / 0.99 | (245, 232, 209) |
| S02 desk, dressed | (241, 225, 204) | 1.02 / 1.03 / 1.03 | (245, 232, 208) |
| S03 nook plate | (230, 210, 178) | 1.06 / 1.10 / 1.18 | (244, 232, 208) |
| S04 rack (probe) | (226, 203, 165) | 1.09 / 1.14 / 1.27 | (244, 232, 209) |
| S05 moodboard + CRT | (226, 205, 176) | 1.09 / 1.13 / 1.19 | (244, 232, 208) |
| S06 dartboard | (228, 210, 180) | 1.08 / 1.11 / 1.16 | (244, 232, 208) |
| S07 alarm | (236, 218, 186) | 1.04 / 1.06 / 1.12 | (244, 232, 208) |

**The correction is a per-channel gain, not an offset** — paper is a multiplicative tint, and
a gain leaves the graphite blacks black instead of lifting them to grey. Clipping stays under
0.4% of pixels even on S04, the heaviest lift.

**The pipeline step is [`post/normalize_paper.py`](post/normalize_paper.py)**, $0, deterministic
and idempotent; output lands in [`normalised/`](normalised/) and **that directory is the
working set from here on** — motion, edit and delivery all read from it. Re-run it after any
new generation. It finds the wall by sweeping small patches across the upper band and taking
the flattest pale ones, rather than by hand-tuned sample points; only the S04 rack plate needs
a steering window, because its upper band is server rack on one side and moodboard on the
other and the sweep otherwise scores a fixture as paper.

**Generation still carries the palette clause.** Normalising is a safety net for reference
drift, not a licence to stop asking. A plate that generates near-canonical needs a gain near
1.0, and that is the cheapest signal that a new reference has not dragged the paper again.

**The floor target is retired, not re-based.** Floors in these plates run 10–20 levels under
their own walls and vary with how much floor a setup shows. The wall is the control surface;
normalising to it brings the floor with it. Stop enforcing a separate floor number.
