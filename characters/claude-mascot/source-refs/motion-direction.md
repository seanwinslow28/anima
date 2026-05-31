# Claude Mascot — Motion Direction

*The shot list before pencil hits paper. Sean draws these keys by hand — they are the
mascot's Phase 4 animatic, the human-authored timing constraint the whole pipeline is
built to honor before any AI motion runs. This brief says what to draw, why, and how it
feeds the machine. Keep it next to the drawing board.*

**Register:** pencil-test-colored, the same medium as sean-anchor — warm-graphite line,
flat terracotta fill, cross-hatch shadow, cream paper #F2E6CC, hole-punch marks.
**Frame rate:** 12fps on twos (the project's limited-animation register).
**Authority refs:** `anchor.png` (C-B, ¾-front identity), `source-refs/turnaround-c1.png`
(the five real views), `source-refs/sean-with-claude-mascot.png` (A-7, shoulder scale).
**Rules the motion must not break:** the 18 locked IR rules in `acceptance_criteria.json`.

---

## 1. Movement personality (the director's read — confirmed)

Look at C-B and the C-1 turnaround together and the movement writes itself. This is a
creature with almost nothing that moves: no arms to gesture, no hands to reach, no real
mouth to talk. Four stub legs tucked close under a rounded terracotta box, two nub stubs
at the midline, two graphite dot eyes riding a construction cross-line, and a soft
scribbled shadow holding it to the paper. That is the entire instrument.

So the personality is **a watchful, gentle companion that is mostly still and reacts
small — with a touch more bounce than reserve.** It lives in holds. Its acting is a
whole-body tilt, the two dot eyes leading a look, a nub that perks or droops, the legs
gathering or planting, and a soft squash of the box as it breathes or lands. The cast
shadow does the weight. Per Sean's call, we give the squash a little more amplitude and
let actions overshoot slightly before they settle — playful, not inert — but the baseline
is still stillness. This is a **limited-animation character by nature**, and the 80/20
rule turns that into an asset: very few moving parts, animated with deliberate intent.
It earns its charm by *not* over-moving.

**The standing drift warning — true of every key below.** The moment we ask this creature
to *do* something, a generator reaches for an arm, sprouts hair on the box-top because it
reads the box as a head, or balloons the dot eyes into glossy cartoon eyes. Your
hand-drawn keys are exactly what prevents that downstream. Three things to hold in your
hand on *every* drawing:

- **No arms, ever.** Nubs may lag or trail for follow-through; they never extend, reach,
  grasp, point, or balance like arms. (IR.anatomy.no-arms-no-hands)
- **No hair, ever.** The box-top stays a clean unbroken edge through every pose — no tuft,
  no sprig, nothing breaking the silhouette. (IR.anatomy.no-hair)
- **Eyes stay small graphite dots.** They widen, squint, arc, and close — but never become
  big glossy cartoon eyes. (IR.face.two-dot-eyes-with-brows + the expression rules)

---

## 2. The motion shot list

Six motions, ~22 keys, drawn Tier 1 first. Three of those keys reuse one rest pose:
**idle-01 (settled) is the canonical rest pose**, and `alert-01`, `sleep-01`, and
`hop-05` all return to it — so the truly *new* poses to invent number ~19.

Seedance interpolates between **exactly two approved keys**. For a two-extreme motion that
is one clip. For a motion with a load-bearing breakdown — the perch impact-squash, the hop
apex — you **chain two clips through the breakdown** (e.g. contact→impact, then
impact→settle), because Seedance can't be trusted to invent a squash or hold an arc apex
on its own; left to itself it interpolates linearly and the motion goes floaty. The
breakdown keys aren't decoration — they are what forces Seedance onto the right spacing.
Anchor pairs are marked **▸** below.

### Tier 1 — Act 2 critical (draw first)

**1. Idle / settle loop** — view: ¾ front. *The most-used clip: ambient life on Sean's
shoulder.* A slow breath. The box sinks and softens, then rises and lengthens, then sinks
again — a loop.

- `idle-01` **settled** (low extreme): body slightly compressed, sitting low; legs gathered
  close; nubs neutral; eyes calm. The longest hold.
- `idle-02` **mid-rise** (breakdown): halfway up, locking the ease curve so the breath
  isn't linear.
- `idle-03` **risen** (high extreme): a breath up; body decompressed and a touch taller;
  nubs lift a hair.
- ▸ **Anchor pair:** `idle-01` ↔ `idle-03` (Seedance runs it both directions to loop).

**2. Head/body-tilt look (curiosity)** — view: front. *Its signature reaction.* The eyes
dart to the target first; then the whole creature cants toward it. No neck exists, so this
is a whole-body lean, not a head turn.

- `look-01` **neutral**: upright, eyes forward.
- `look-02` **eye-lead** (breakdown): box still upright, but the two dot eyes have already
  shifted toward the target. This is the key that makes the look read as *thought*.
- `look-03` **tilt-left**: ~15° whole-body cant; the near (left) nub rises with the cant,
  the far nub holds or drops slightly; the construction cross-line cants *with* the box.
- `look-04` **tilt-right**: the mirror — *redraw it, don't flip the file*; the cross-line
  and the far-nub lag differ left-to-right.
- ▸ **Anchor pairs:** `look-01` ↔ `look-03`, and `look-01` ↔ `look-04`. `look-02` is the
  breakdown that sits just inside the start of each.

**3. Perch-settle** — view: ¾ front. *The establishing motion: arriving onto Sean's
shoulder — the A-7 pairing in motion.* Principle-heavy, so it gets four keys.

- `perch-01` **contact/reach**: body stretched tall, legs reaching down toward the shoulder
  — the anticipation of landing.
- `perch-02` **impact-squash** (breakdown): body compresses; legs splay *transiently* to
  take the weight; the cast shadow tightens and darkens; nubs splay a touch for balance.
- `perch-03` **overshoot** (breakdown): a small bob back up past the rest line — this is
  the bounce Sean asked for.
- `perch-04` **settle**: recover to the idle-settled read, leaning lightly toward Sean's
  jaw and cheek per the canonical pairing; legs regathered close.
- ▸ **Anchor pair (outer):** `perch-01` ↔ `perch-04`. **Chain through the breakdown:**
  `perch-01`→`perch-02`, then `perch-02`→`perch-04` (overshoot folded into the second
  segment) — the squash must not be left to Seedance to invent.

### Tier 2 — Bible completeness

**4. Alert-perk (alarm in motion)** — view: front. *Maps the alert-perk / alarm expression
to a move.* A quick wind-up, a fast snap up, then a long held stare.

- `alert-01` **relaxed**: the idle-settled baseline.
- `alert-02` **anticipation dip** (breakdown): a tiny, *fast* downward compress — the
  wind-up. Shock anticipation is short (1–2 frames), not a slow crouch.
- `alert-03` **perk**: body snaps straight and tall; the two nubs project up-and-forward;
  dot eyes widen (still small dots); brows lift; legs plant. Then it *holds*, dead still.
- ▸ **Anchor pair:** `alert-01` ↔ `alert-03`. (A recover-back-to-relaxed key is optional;
  in Act 2 alert usually holds and then cuts, so we defer it.)

**5. Hop (locomotion)** — view: **side**. *The walk-cycle analogue for a four-stub-legged
box.* Sean chose the hop over a scuttle — it reads more charming on a box creature and is
the richest motion in the set for animation principle. Five keys.

- `hop-01` **anticipation crouch**: gather and compress down; legs bunch; the wind-up.
- `hop-02` **takeoff**: body stretches up and forward; legs extend then trail; leaves the
  ground.
- `hop-03` **apex** (breakdown): top of the arc. Body neutral, legs tucked. Per the
  Fourth-Down Rule this key sits *high* in the arc — it carries the hang.
- `hop-04` **landing contact**: squash; legs reach down then splay to absorb; shadow
  tightens.
- `hop-05` **recover**: back to the idle-settled rest pose.
- ▸ **Anchor pairs:** `hop-01` ↔ `hop-03` (launch arc), then `hop-03` ↔ `hop-04`
  (descent + impact). Two chained clips — the apex is the pivot.

**6. Sleep-settle** — view: ¾ front. *For the sleep expression.* The slowest motion in the
set — everything decelerates into rest.

- `sleep-01` **awake**: the idle-settled baseline, eyes open.
- `sleep-02` **droop** (breakdown): body slumps and settles lower; eyes lower toward the
  cross-line; nubs droop; brows soften.
- `sleep-03` **asleep**: fully settled, body at its lowest and softest; eyes closed as two
  small downward graphite arcs riding the construction midline; nubs at rest. A long hold —
  the idle breath can layer faintly on top of this.
- ▸ **Anchor pair:** `sleep-01` ↔ `sleep-03`.

---

## 3. Animation-craft notes (from the 2d-animation-principles skill)

Not generic — the actual spacing, arcs, and holds for *this* creature.

**Idle / settle.** This is a **moving hold** — its whole job is to keep a long static beat
from going dead (the dead-hold rule: anything static beyond ~12 frames at 12fps reads as
frozen). The breath *is* the 1–2% drift that prevents that. Ease in and out at both ends —
a breath is sinusoidal, never linear, or it floats. **Conserve volume** in the squash: as
the box sinks it widens slightly, as it rises it narrows (Scale_X × Scale_Y ≈ 1). Let one
nub lag the other by a frame so the symmetric breath doesn't read mechanical
(follow-through). Hold `idle-01` longest; a full cycle is ~30–36 frames.

**Head/body-tilt look.** **Eye-lead is the whole point** — the eyes reach the target 2–3
frames before the body cants. That's what `look-02` exists to capture. The cant travels on
a **shallow arc**, not a straight lean (the box-top traces a curve). **Anti-twinning:** the
two nubs must not do the same thing — near nub up, far nub holds; offset them. Hold the
tilt extreme 6–12 frames (a readable attitude), then settle back with a small overshoot.

**Perch-settle.** The acting beat in full: **anticipation** (the stretch/reach of
`perch-01`) → **action** (the drop) → **squash** (`perch-02`, volume conserved, box widens
as it compresses) → **overshoot** (`perch-03`, 3–5 frames) → **settle**. The **cast shadow
carries the weight** — draw it tightening and darkening at impact, loosening as it settles.
The leg splay at `perch-02` is **transient** — legs gather back close by `perch-04`. A
permanently wide stance is an IR violation (see §5).

**Alert-perk.** **Shock anticipation is fast** — the `alert-02` dip is 1–2 frames, not the
4–8 of a normal wind-up. The snap to `alert-03` is a fast reaction (2–4 frames, effectively
on ones). Then a **long dead-still hold** — the held breath after a start. The contrast
between the snap and the hold is the read.

**Hop.** The most principle-heavy key in the set — slow down and get these right:
- **Arc:** the whole box follows a clean parabolic arc. Plot the path first, then place the
  keys on it.
- **Gravity (Odd Rule):** airborne spacing follows 1 : 3 : 5 : 7 — wide spacing low,
  tightening toward the apex, widening again on the way down. Even spacing = floaty.
- **Fourth-Down hang:** `hop-03` (the 50%-time apex) sits at ~25% of the height *down* from
  the very peak — that's what gives the satisfying hang at the top.
- **Squash & stretch:** compress at `hop-01` and `hop-04`, stretch at `hop-02`, volume
  conserved throughout.
- Legs **trail** in the air and **regather** on landing — they never become springy limbs.

**Sleep-settle.** A pure **slow ease-in** — the opposite of the alert snap. Long,
decelerating spacing into `sleep-03`, optionally with one tiny dampened secondary sink
(the body settling twice, lightly). The closed eyes are **two downward arcs on the
midline** — the sleep state of the dot eyes, not a new eye style, not Xs, not lashes.

---

## 4. Pipeline mapping — how these keys feed the machine

**The ingest (zero-drift, mirroring the turnaround crops).** Sean's line-art scans land
under `source-refs/<motion>/<motion>-N.png` (mirroring sean-anchor's
`source-refs/head-turn/head-turn-1.png`), and the baked Bible plates take the flat name
`motion_plates/<motion>-NN.png` (mirroring `motion_plates/head-turn-01.png`). No
generation, no drift — the same pixel-layer ingest as the C-1 turnaround crops.

| Motion | Baked plates | Seedance anchor pair(s) |
|---|---|---|
| Idle | `motion_plates/idle-01..03.png` | idle-01 ↔ idle-03 |
| Head-tilt look | `motion_plates/look-01..04.png` | look-01 ↔ look-03; look-01 ↔ look-04 |
| Perch-settle | `motion_plates/perch-01..04.png` | perch-01 ↔ perch-04 (chain via perch-02) |
| Alert-perk | `motion_plates/alert-01..03.png` | alert-01 ↔ alert-03 |
| Hop | `motion_plates/hop-01..05.png` | hop-01 ↔ hop-03; hop-03 ↔ hop-04 |
| Sleep-settle | `motion_plates/sleep-01..03.png` | sleep-01 ↔ sleep-03 |

**The new rules these keys would anchor.** The risk-bible names motion plates as the
load-bearing gap: there are **0 `IR.claude-mascot.motion.*` rules today**, so Em (the T2
vision critic) cannot ground a motion-drift verdict on a Phase 6 frame. These keys let
seven motion rules finally exist:

- `IR.claude-mascot.motion.idle-breath-volume` — the breath squash conserves volume; the
  loop holds identity end to end.
- `IR.claude-mascot.motion.tilt-is-whole-body` — the look is a whole-body cant with the
  cross-line canting *with* the box; the box-top never reads as a head on a neck; eyes lead;
  nubs offset (no twinning).
- `IR.claude-mascot.motion.perch-weight-and-squash` — weight reads through squash + cast-
  shadow tightening; leg splay is transient; lands leaning toward Sean's jaw (canonical
  pairing).
- `IR.claude-mascot.motion.alert-snap-eyes-stay-dots` — a fast snap into a long hold; eyes
  widen but stay small graphite dots; nubs perk without becoming arms.
- `IR.claude-mascot.motion.hop-arc-and-gravity` — parabolic arc, Odd-Rule spacing,
  Fourth-Down apex; legs trail and regather, never spring; side-view keys preserve the
  near-nub end-cap disc.
- `IR.claude-mascot.motion.sleep-ease-in` — slowest ease-in; eyes close to two downward
  arcs on the midline.
- `IR.claude-mascot.motion.no-arms-in-motion` — the cross-cutting reinforcement: nubs may
  lag/trail but never reach, in any frame of any cycle.

**The Phase 4 → Phase 6 path.** These hand-drawn keys *are* the mascot's Phase 4 animatic.
They ingest into the **locked** Bible through the audited additive route — `bible add` —
which appends the new `motion_plates/` and the new `IR.*.motion.*` rules and bumps the
content version (the Bible stays locked; nothing is re-authored), exactly as the turnaround
crops landed. Then Phase 6: each anchor pair becomes a Seedance start/end frame; the
breakdown-bearing motions (perch, hop) chain segments through their breakdown. With the
rules in place, Em can finally cite motion drift on a Phase 6 mascot frame instead of
treating it as Bible silence. This also answers the open Act 2 question from last session —
how the mascot holds at pairing scale, *in motion*.

---

## 5. Sean's drawing checklist

Flat list, Tier 1 first. **22 keys total** (~19 distinct poses — `alert-01`, `sleep-01`,
and `hop-05` reuse the `idle-01` settled rest pose). Each baked plate is
`motion_plates/<filename>.png`; raw scans go to `source-refs/<motion>/`.

**Watch-list while drawing (IR rules a motion tempts):**
- **Perch `perch-02` & hop `hop-04`:** the leg splay at impact is *transient*. Don't lock a
  wide stance — four legs sit close together (IR.anatomy.four-stub-legs).
- **Alert `alert-03`:** nubs perk up-and-forward — they must *not* extend into arms
  (IR.anatomy.no-arms-no-hands); eyes widen but stay small dots, never glossy.
- **Hop (side view):** keep the near-nub **end-cap disc** ("the C-1 side swirl") visible —
  it's the nub seen end-on, not a navel or emblem, and never cleaned away
  (IR.anatomy.nub-side-view-endcap). Don't invent any new circle on a face.
- **Every key:** clean box-top — no hair/tuft (IR.anatomy.no-hair); the box never splits
  into head-and-body (IR.proportion.rounded-box-silhouette); the construction cross-line
  stays visible and cants with the box.

### Tier 1 (8 keys) — Act 2 critical

| # | Filename | View | Pose (one line) |
|---|---|---|---|
| 1 | `idle-01` | ¾ front | Settled low, body compressed, legs gathered, nubs neutral, eyes calm — the rest pose |
| 2 | `idle-02` | ¾ front | Mid-rise breakdown — halfway up, locking the breath ease |
| 3 | `idle-03` | ¾ front | Risen — a breath up, body taller, nubs lift slightly |
| 4 | `look-01` | front | Neutral, upright, eyes forward |
| 5 | `look-02` | front | Eye-lead — box upright, dot eyes already darted to target |
| 6 | `look-03` | front | Tilt-left ~15° whole-body cant, near nub up, far nub holds, cross-line cants with box |
| 7 | `perch-01` | ¾ front | Contact/reach — body stretched tall, legs reaching down (anticipation of landing) |
| 8 | `perch-04` | ¾ front | Settle — recovered, leaning lightly toward Sean's jaw, legs regathered |

*(Plus the perch breakdowns in Tier-1-extended below — draw them in the same sitting.)*

### Tier 1 extended (3 keys) — finish the criticals

| # | Filename | View | Pose (one line) |
|---|---|---|---|
| 9 | `look-04` | front | Tilt-right — mirror of look-03, redrawn (not flipped) |
| 10 | `perch-02` | ¾ front | Impact-squash breakdown — body compresses, legs splay transiently, shadow tightens |
| 11 | `perch-03` | ¾ front | Overshoot breakdown — small bob up past the rest line |

### Tier 2 (11 keys) — Bible completeness

| # | Filename | View | Pose (one line) |
|---|---|---|---|
| 12 | `alert-01` | front | Relaxed (= idle-settled baseline) |
| 13 | `alert-02` | front | Anticipation dip — fast tiny downward compress (wind-up) |
| 14 | `alert-03` | front | Perk — body snaps tall, nubs up-and-forward, dot eyes widen, brows lift, legs plant, then holds |
| 15 | `hop-01` | side | Anticipation crouch — gather and compress down, legs bunch |
| 16 | `hop-02` | side | Takeoff — body stretches up/forward, legs extend then trail, leaves ground |
| 17 | `hop-03` | side | Apex breakdown — top of arc, body neutral, legs tucked, sits high (Fourth-Down hang) |
| 18 | `hop-04` | side | Landing contact — squash, legs reach then splay to absorb, shadow tightens |
| 19 | `hop-05` | side | Recover — back to idle-settled rest pose |
| 20 | `sleep-01` | ¾ front | Awake (= idle-settled baseline), eyes open |
| 21 | `sleep-02` | ¾ front | Droop breakdown — body slumps lower, eyes lower toward cross-line, nubs droop |
| 22 | `sleep-03` | ¾ front | Asleep — lowest/softest, eyes closed as two downward arcs on the midline, long hold |

**Total: 22 keys** — 8 Tier 1, 3 Tier 1 extended, 11 Tier 2. Anchor pairs (the Seedance
start/end frames) are marked **▸** in §2; the perch and hop chain through their breakdowns.

---

*Drawn keys → `bible add` (zero-drift ingest) → `IR.*.motion.*` rules exist → Em can cite
motion drift → Seedance interpolates the anchor pairs. The human owns the timing; the
machine fills the in-betweens. That's the whole point.*
