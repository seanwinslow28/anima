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

## MEASURED 2026-08-30, after the four prop-rich plates: the set has split into two creams

The four plates generated tonight (S03 v2, S05, S06, S07) all came back **warmer and
darker than canonical, by the same amount and in the same direction**:

| Plate | Wall as generated | Δ vs #f5e8d1 |
|---|---|---|
| S03 Claude's nook v2 | (227, 206, 172) | −18 / −26 / −37 |
| S05 Gemini's moodboard | (227, 207, 175) | −18 / −25 / −34 |
| S06 Grok's dartboard | (226, 208, 177) | −19 / −24 / −32 |
| S07 the alarm | (213–223, 189–199, 157–164) | −22 to −32 / −33 to −43 / −45 to −52 |

**The cause is mechanical and was found by measuring the reference, not the output.** These
four are the first plates generated with the **S04 plate as the world/style bible**, and
S04's own paper measures **(218, 191, 152)** — 27 / 41 / 57 levels off canonical, because
S04 was generated in probe-205 *before* the palette clause existed. The clause and the
reference pulled in opposite directions and the reference won about two thirds of the
argument. Every new plate landed between the two, within 4 levels of its siblings.

So the room is now split into two consistent groups, not scattered:

| Group | Wall | Members |
|---|---|---|
| **Canonical cream** | ≈ (245, 232, 209) | S02 desk medium (Sean-approved), S03 sparse (superseded) |
| **Bible tan** | ≈ (225, 205, 172) | S04 rack (banked + only clip proven end to end), S03 v2, S05, S06, S07 |

**This is a ruling for Sean, not a re-roll.** Both groups are internally consistent, and the
fix is free either way: a flat per-channel gain on the paper tone matches one group to the
other exactly, costs $0, is reversible, and is a **post** operation — which is where
FIRST LICKS DR #41 already says the look lives. Normalised copies of every plate and
composite are banked at [`plates/normalised/`](plates/normalised/) (gains ≈ 1.08 / 1.13 /
1.21) so the comparison can be made by eye rather than by argument.

**Do not re-roll good plates over this.** The tolerance was doing its job — it caught a
reference conflict, which is exactly what it is for.

**Floor target still PROVISIONAL.** The three new sparse-to-mid floors measured
(207–218, 186–196, 155–159), all far from #e8d6bc, but they inherit the same bible tan, so
they cannot re-base the floor until the paper question is settled first.
