# CONTINUATION — 2026-08-30 · About-Me short, Movement 1

Hand-off from the session that boarded Movement 1 and proved the production route.
**Read this, then `M1-STORYBOARD.md` and `environment-style.md`, before generating anything.**

Ticket: [#212](https://github.com/seanwinslow28/code-brain/issues/212) (boarding) ·
Probe: [#205](https://github.com/seanwinslow28/code-brain/issues/205) (four rounds of findings) ·
Map: [#204](https://github.com/seanwinslow28/code-brain/issues/204) · Research: [#209](https://github.com/seanwinslow28/code-brain/issues/209)

---

## What we are making

A **~90-second animated short** for Sean's portfolio: a PM and four AI-mascot sidekicks in a
break-room HQ. An alarm fires, each sidekick builds a brilliant *wrong* solution, Sean steps
back, asks the user one question, and the same team ships the tiny right fix. Pencil-test
register, 1950s Goofy "How To" grammar. The locked brief is
[`00_studio_brief.md`](00_studio_brief.md); its non-negotiables are **binding and not
re-litigated**. The 20-beat sheet is [`beats-v1.md`](beats-v1.md); the two locked lines are
[`lines-v1.md`](lines-v1.md).

**Movement 1 "Quiet Morning" is the current scope** — beats 1–3, ~15 seconds, seven setups.
It is also the **fallback deliverable**: stripped of narration it becomes Anima's project-tile
piece if the full film is deferred. Either way its output ships.

**The 4-hour bar** (set before any work, so sunk cost cannot move it): if Movement 1 lands
inside ≤4 hours of Sean's gate time, beats 4–20 are greenlit. Past it, Movement 1 ships as
the tile piece and the film becomes a separate effort. **Instrument as you go** — wall-clock
per beat, gate count, retries, credits. The Spark post-mortem recorded spend but never time,
which is why this bar had no prior basis.

---

## The production route — settled, do not re-derive

**Plates first → characters edited in → Seedance animates the composed still.**

| Step | Tool | Notes |
|---|---|---|
| Plate generation | `gpt_image_2`, 2k, quality `high` | Won the register test outright |
| Character into plate | `gpt_image_2` **edit**, refs = lineup + plate | Phase-corr **0.42** vs NB2's **0.077** |
| Re-angles of the set | **NOT** `gpt_image_2` | It cannot re-camera from an edit. Use NB2-via-edit, or GPT with the reconstruction pattern |
| Motion | `seedance_2_0`, **`mode: fast`**, **7s**, 720p, `generate_audio: false` | `std` **stutters and looks broken** — Sean rejected it outright |
| Post look | in POST, never in generation | FIRST LICKS DR #41; every plate generates CLEAN |

**Two routes were tried and killed — do not resurrect them.**
1. **All-compositing** (characters generated separately, pasted over plates). [#209](https://github.com/seanwinslow28/code-brain/issues/209) found Sean had already built and rejected this in July: *"the cutouts read pasted-on."*
2. **Green-screen characters.** Won on pixel stability (0.0% background drift vs 27% in-scene) and lost on staging — characters keyed on green **gesture at nothing**. Codex patting empty air where a rack should be is worse than Codex patting a rack.

### Prompt laws, each paid for

- **Seedance takes NO negative prompts.** `NO MOUTH` does nothing. State locks **positively**: *"its face stays a pale chevron, one dot eye and a short underscore bar."*
- **Damping words dampen.** "feet planted / light taps / small bounce" produced timid acting. Genre anchor + vivid verbs + zero negation gave **+55% motion energy with slightly less drift**. Liveliness and stability are not in tension.
- **Single-character plates cut drift ~18%** vs two characters. A single plate can carry a whole beat — the 7s clip does type → peer → triumph from one still.
- **Composite prompts ≤70 words, and never re-describe the scene.** An 85-word prompt cost NB2 the entire plate.
- **State SCALE and FACING in words.** Neither is ever inferred. The all-corners wide failed because facing was unstated and every character addressed the lens.
- **`nano_banana_2` now routes to `nano_banana_flash`** — July's "it is the forbidden Pro model" note is **stale**, verified 2026-08-30.

---

## The palette clause — binding

Canonical cream is **#f5e8d1** (245, 232, 209), re-based 2026-08-30 to what GPT Image 2
actually produces rather than to the hero frame it kept missing. Validated: S03 came back at
delta **2/3/2**. The clause itself is in [`environment-style.md`](environment-style.md) and
goes **verbatim** into every plate and composite prompt.

**The floor target (#e8d6bc) is PROVISIONAL — do not enforce it.** It was measured from the
cut all-corners wide, a furnished room with a rug, and it flags sparse plates that are
visually correct. Re-base it once S05 and S06 give two more samples.

**Verify edits with edge-diff + FFT phase correlation, never frame-delta means** — FIRST
LICKS retired that signature because it scales with plate texture.

---

## ⚠ The most recent ruling — read before generating S05/S06/S07

**Sean reverted the bare-wall look on 2026-08-30**, after S03 came back sparse:

> *"I'm not liking the lack of props and office supplies in these shots… it feels naked and
> weird. Like they're in an extremely clean museum and not a workspace."*

The prior session had over-applied *Goofy Gymnastics*' empty walls. **Goofy's set is sparse
because it is a gym.** This HQ is lived-in, and the clutter is characterisation — the tidy
nook, the humming rack, the fifty taped concepts, the darts in the wall are each a
character's portrait. **Corners are prop-rich: supplies, boxes, binders, loose paper.**

**Keep from the Goofy read:** the character owns the frame, and facing is always stated.
**Drop:** bare walls.

**S03 must be re-generated prop-rich.** Its guide is already rebuilt
(`m1-guides/M1-S03-claude-nook-guide.png`); the existing plate `S03-claude-nook-v1.png` is
the superseded sparse version — **keep it, do not delete it** (preservation law: superseded
plates move to `old/`, never overwritten).

**Cost of the reversal, plan for it:** prop-dense plates are exactly what Seedance
re-invents — the 22–27% drift was measured on the busiest wall in the room. Mitigations:
single-character plates, 7s, locked camera stated positively, and the untested option of
**matting the character out of the animated clip and re-laying it over the pristine plate**,
which would make plate drift structurally impossible. That test is the highest-value thing
still unrun.

---

## State of the seven setups

| # | Setup | Guide | Plate | Motion | Next action |
|---|---|---|---|---|---|
| S01 | Title card | ✓ | — | n/a | **Card D approved** (`titlecards/cardD-sean-thinking.png`). Card A liked but Sean reads too small — may regenerate later, not now |
| S02 | **Sean at his desk, medium** | ✓ | **✓** | — | Approved. `S02-sean-desk-v1.png`. The all-corners wide was CUT |
| S03 | Claude's nook | ✓ rebuilt | superseded | — | **Re-generate prop-rich** |
| S04 | Codex's rack | ✓ | ✓ | ✓ | Proven end to end in probe-205 |
| S05 | Gemini's moodboard | ✓ | — | — | Generate prop-rich |
| S06 | Grok's dartboard | ✓ | — | — | Generate prop-rich. Darts in the **wall around** the board |
| S07 | The CRT alarm | ✓ | — | — | Generate |

**Guides** are Python-generated in the FIRST LICKS idiom —
[`m1-guides/make_m1_guides.py`](m1-guides/make_m1_guides.py), 1536×864, flat greyscale,
headless-Chrome render, red captions carrying shot id **and dramatic intent**. $0 and
re-runnable. Each doubles as the composition rough a generation needs.

### Standing rulings that bind the remaining shots

- **The USER never appears in the room.** The doorway stays empty set dressing. The USER is introduced **on the CRT** — the TV flashes `PROBLEM!`, then cuts to the USER *in* the television. This makes S07's set a heavier fixture than the alarm alone; Movement 3's payoff lands there too.
- **There is no establishing wide.** The audience never sees the whole room, so continuity rests entirely on the corner plates matching each other. Every corner carries the same signature — same paper, same floor, same baseboard, same light. **Reference the previous plate as the style bible**, not the hero frame; matching plate-to-plate is stronger than matching both to a third image.
- **Codex and Gemini are the same colour family** and NB2 corrupted one with the other 4/4 in July. They are in separate setups, which sidesteps it. If a later shot needs both, split the passes.
- **Codex's face goes off-model in `fast` motion** — it grows a mouth. At corner-shot scale it may not read; `std` holds the face but stutters, so it is not the answer. Get Sean's eye on this before the remaining corners generate to the same recipe.

### Open art-direction question, not yet decided

**Sean renders more finished than the mascots** — real hair, real forearms — while Codex and
Gemini are flat cartoon shapes. Visible in Card D and the S02 medium. That gap is defensible
as a design idea (a real man among cartoon sidekicks, which the hero frame already does) but
it should be a **decision**, not drift, because it shows most when they share a frame in
Movements 2 and 3.

---

## Gate still owed

The **stopwatch table-read** ([#206](https://github.com/seanwinslow28/code-brain/issues/206))
is Sean-only, $0, and blocks Movement 2 boarding — not Movement 1, since its two outputs (the
runtime laps and the "He speaks" contradiction) both land in Movement 2. Also owed before any
full-production spend: **R4**, a blind-judged 30s scratch narration
([#207](https://github.com/seanwinslow28/code-brain/issues/207)).

## Working discipline

Sean directs; propose with a stated lean and let his eye decide. Measure rather than assert —
several premises in this effort survived until they were measured and then did not. When a
ruling reverses an earlier one, **record why**, keep the superseded artifact, and say plainly
what it costs.
