# Claude Mascot — NB2 pose-sheet edit prompts (exploration)

*Companion to [`motion-direction.md`](motion-direction.md). Six prompts — one per motion —
each asking Nano Banana 2 to produce a single 16:9 model sheet with all that motion's keys
in a row, laid out like the C-1 turnaround. Built on the editing template in
[`../../../docs/research/2026-05-30-nb2-editing-character-consistency-template.md`](../../../docs/research/2026-05-30-nb2-editing-character-consistency-template.md):
name the anchor, lock identity by enumerated markers, state the change, name what stays,
apply the register last.*

**These are scratch exploration, not Bible plates.** Per PHILOSOPHY.md the human owns
timing — your hand-drawn keys remain the source of truth that ingests zero-drift via
`bible add`. NB2 output is *not* zero-drift; it would have to pass the similarity gate to
land. Use these sheets for two things: (1) a fast read on whether the poses *work* before
you commit them in pencil, and (2) possible rough reference. The pencil keys are still the
deliverable.

## Setup (do this once, every generation)

- **Use Nano Banana 2** (Gemini 3.1 Flash Image), **not** NB Pro. The research is decisive
  that NB2 holds identity better across multiple references and edits — NB Pro currently has
  a multi-reference downsampling regression that's the wrong tool for exactly this job.
- **Attach two references, in this order:**
  1. `characters/claude-mascot/anchor.png` — the identity anchor (Image 1)
  2. `characters/claude-mascot/source-refs/turnaround-c1.png` — the view sheet (Image 2)
- **Re-attach both on every run.** Never feed a generated sheet back in as the reference —
  chaining off a generated frame is what propagates drift (degrades after ~5–10 turns).
- **No text labels by design.** The prompts forbid rendered text (models garble it). Poses
  are in a known left-to-right order; hand-label your printout if you want names.

## How to read the prompts

Each block is copy-paste ready. The **identity-lock, preserve/negative, and style-register
sections are identical across all six** — that verbatim repetition is the trait-lock
discipline (the thing that keeps "terracotta box" from becoming "orange blob" between
sheets). Only the **POSES** line and the **layout** change per motion. Paste the whole
block as one prompt.

---

## Prompt 1 — Idle / settle loop (¾-front, 3 poses)

```
Image 1 is the identity anchor — the canonical reference for this creature (a small
terracotta box-creature, ¾-front hero portrait). Image 2 is its turnaround sheet — use it
to match correct viewing angles; identity always comes from Image 1.

Match the creature in Image 1 exactly: a single rounded-box body (a rounded cube, slightly
taller than wide ~1:1.2, generously radiused corners, NO separate head — the face sits on
the upper-front face); warm terracotta-orange flat fill; exactly two short rounded ear/arm
nubs projecting from the left and right faces at mid-height; exactly four short stub legs
set close together under the body; two small graphite dot eyes with short curved brows,
riding a faint pencil construction cross-line (a horizontal midline and a soft vertical
centerline); at most a tiny mouth line. Keep its proportions and small shoulder-companion
scale.

POSES — render three poses of a gentle breathing/settle cycle, all in ¾-front view
(matching Image 1's angle): (1) SETTLED — sitting low, the box gently compressed and a
touch wider, legs gathered close, nubs neutral, eyes calm; (2) MID-RISE — halfway up; (3)
RISEN — a breath taller, the box gently decompressed and a touch narrower, nubs lifted
slightly. Volume stays constant: as the box lowers it widens, as it rises it narrows.
Change ONLY this breathing pose across the three; keep everything else identical to Image 1.

Keep the warm cream paper (#F2E6CC) with visible grain, the soft scribbled cast shadow
beneath the body, the cross-hatch shadow on the far and under planes, and the full
terracotta color of Image 1 — identical identity in every pose, only the pose changing.
Do NOT give the creature arms or hands — the nubs never extend, reach, bend, or grasp. Do
NOT add hair, a tuft, or anything breaking the clean top edge of the box. Keep the eyes as
small graphite dots, never large glossy cartoon eyes. Keep the four legs short and close
together (no wide-splayed or biped stance). Do not split the box into a separate head and
body. Do not render any text, captions, labels, numbers, or watermarks.

Warm pencil-test render: warm-graphite line (not vector black, not pure black), flat color
fills, cross-hatch shadow, warm cream paper, hole-punch production marks — the same
hand-drawn medium as Image 1 and Image 2.

16:9. A single horizontal model sheet: three poses of the same creature in a row, evenly
spaced, all standing on one shared horizon line, even diffuse lighting, consistent size
across the row. Left to right: settled, mid-rise, risen.
```

---

## Prompt 2 — Head/body-tilt look (front, 4 poses)

```
Image 1 is the identity anchor — the canonical reference for this creature (a small
terracotta box-creature, ¾-front hero portrait). Image 2 is its turnaround sheet — use it
to match correct viewing angles; identity always comes from Image 1.

Match the creature in Image 1 exactly: a single rounded-box body (a rounded cube, slightly
taller than wide ~1:1.2, generously radiused corners, NO separate head — the face sits on
the upper-front face); warm terracotta-orange flat fill; exactly two short rounded ear/arm
nubs projecting from the left and right faces at mid-height; exactly four short stub legs
set close together under the body; two small graphite dot eyes with short curved brows,
riding a faint pencil construction cross-line (a horizontal midline and a soft vertical
centerline); at most a tiny mouth line. Keep its proportions and small shoulder-companion
scale.

POSES — render four poses of a curious whole-body tilt, all in FRONT view: (1) NEUTRAL —
upright, eyes forward; (2) EYE-LEAD — body still upright but both dot eyes have darted to
the left toward something off-frame; (3) TILT-LEFT — the whole box canted about 15° to the
left (a lean, NOT a head-turn — there is no neck; the construction cross-line cants WITH
the box), the left nub raised and the right nub held lower; (4) TILT-RIGHT — the mirror,
canted right. Change ONLY the tilt and eye-direction across the row; keep everything else
identical to Image 1.

Keep the warm cream paper (#F2E6CC) with visible grain, the soft scribbled cast shadow
beneath the body, the cross-hatch shadow on the far and under planes, and the full
terracotta color of Image 1 — identical identity in every pose, only the pose changing.
Do NOT give the creature arms or hands — the nubs never extend, reach, bend, or grasp. Do
NOT add hair, a tuft, or anything breaking the clean top edge of the box. Keep the eyes as
small graphite dots, never large glossy cartoon eyes. Keep the four legs short and close
together (no wide-splayed or biped stance). Do not split the box into a separate head and
body. Do not render any text, captions, labels, numbers, or watermarks.

Warm pencil-test render: warm-graphite line (not vector black, not pure black), flat color
fills, cross-hatch shadow, warm cream paper, hole-punch production marks — the same
hand-drawn medium as Image 1 and Image 2.

16:9. A single horizontal model sheet: four poses of the same creature in a row, evenly
spaced, all standing on one shared horizon line, even diffuse lighting, consistent size
across the row. Left to right: neutral, eye-lead, tilt-left, tilt-right.
```

---

## Prompt 3 — Perch-settle (¾-front, 4 poses)

```
Image 1 is the identity anchor — the canonical reference for this creature (a small
terracotta box-creature, ¾-front hero portrait). Image 2 is its turnaround sheet — use it
to match correct viewing angles; identity always comes from Image 1.

Match the creature in Image 1 exactly: a single rounded-box body (a rounded cube, slightly
taller than wide ~1:1.2, generously radiused corners, NO separate head — the face sits on
the upper-front face); warm terracotta-orange flat fill; exactly two short rounded ear/arm
nubs projecting from the left and right faces at mid-height; exactly four short stub legs
set close together under the body; two small graphite dot eyes with short curved brows,
riding a faint pencil construction cross-line (a horizontal midline and a soft vertical
centerline); at most a tiny mouth line. Keep its proportions and small shoulder-companion
scale.

POSES — render four poses of the creature settling down onto a perch, all in ¾-front view:
(1) CONTACT — body stretched slightly tall, the four legs reaching downward as it arrives;
(2) IMPACT-SQUASH — the box compressed and a touch wider as weight lands, legs briefly
splayed to absorb, the cast shadow tightened and darker; (3) OVERSHOOT — a small bounce
back up, just past the resting height; (4) SETTLE — resolved back to the low resting pose,
leaning very slightly to one side as if resting against something, legs gathered close
again. The leg splay in pose 2 is brief — legs return close together by pose 4. Change ONLY
this settling pose across the row; keep everything else identical to Image 1.

Keep the warm cream paper (#F2E6CC) with visible grain, the soft scribbled cast shadow
beneath the body, the cross-hatch shadow on the far and under planes, and the full
terracotta color of Image 1 — identical identity in every pose, only the pose changing.
Do NOT give the creature arms or hands — the nubs never extend, reach, bend, or grasp. Do
NOT add hair, a tuft, or anything breaking the clean top edge of the box. Keep the eyes as
small graphite dots, never large glossy cartoon eyes. Keep the four legs short and close
together (no permanently wide-splayed or biped stance). Do not split the box into a separate
head and body. Do not render any text, captions, labels, numbers, or watermarks.

Warm pencil-test render: warm-graphite line (not vector black, not pure black), flat color
fills, cross-hatch shadow, warm cream paper, hole-punch production marks — the same
hand-drawn medium as Image 1 and Image 2.

16:9. A single horizontal model sheet: four poses of the same creature in a row, evenly
spaced, all on one shared horizon line, even diffuse lighting, consistent size across the
row. Left to right: contact, impact-squash, overshoot, settle.
```

---

## Prompt 4 — Alert-perk (front, 3 poses)

```
Image 1 is the identity anchor — the canonical reference for this creature (a small
terracotta box-creature, ¾-front hero portrait). Image 2 is its turnaround sheet — use it
to match correct viewing angles; identity always comes from Image 1.

Match the creature in Image 1 exactly: a single rounded-box body (a rounded cube, slightly
taller than wide ~1:1.2, generously radiused corners, NO separate head — the face sits on
the upper-front face); warm terracotta-orange flat fill; exactly two short rounded ear/arm
nubs projecting from the left and right faces at mid-height; exactly four short stub legs
set close together under the body; two small graphite dot eyes with short curved brows,
riding a faint pencil construction cross-line (a horizontal midline and a soft vertical
centerline); at most a tiny mouth line. Keep its proportions and small shoulder-companion
scale.

POSES — render three poses of a startle/alert, all in FRONT view: (1) RELAXED — the low
resting pose, calm; (2) DIP — a quick small compression downward (a fast wind-up); (3) PERK
— the box snapped upright and tall, the two ear/arm nubs raised up-and-forward (alert), the
dot eyes widened but STILL small graphite dots, brows lifted, legs planted. Change ONLY this
alert pose across the row; keep everything else identical to Image 1.

Keep the warm cream paper (#F2E6CC) with visible grain, the soft scribbled cast shadow
beneath the body, the cross-hatch shadow on the far and under planes, and the full
terracotta color of Image 1 — identical identity in every pose, only the pose changing.
Do NOT give the creature arms or hands — the nubs raise but never extend into arms, reach,
or grasp. Do NOT add hair, a tuft, or anything breaking the clean top edge of the box. Keep
the eyes as small graphite dots, never large glossy cartoon eyes. Keep the four legs short
and close together (no wide-splayed or biped stance). Do not split the box into a separate
head and body. Do not render any text, captions, labels, numbers, or watermarks.

Warm pencil-test render: warm-graphite line (not vector black, not pure black), flat color
fills, cross-hatch shadow, warm cream paper, hole-punch production marks — the same
hand-drawn medium as Image 1 and Image 2.

16:9. A single horizontal model sheet: three poses of the same creature in a row, evenly
spaced, all on one shared horizon line, even diffuse lighting, consistent size across the
row. Left to right: relaxed, dip, perk.
```

---

## Prompt 5 — Hop (side / profile, 5 poses)

*This is the one where Image 2 earns its keep — the model gets the real SIDE view instead
of inventing a profile from the ¾-front anchor. It's also the hardest sheet (5 panels); if
identity drifts, fall back to one pose per image (below).*

```
Image 1 is the identity anchor — the canonical reference for this creature (a small
terracotta box-creature, ¾-front hero portrait). Image 2 is its turnaround sheet — use the
SIDE view in Image 2 for the profile; identity always comes from Image 1.

Match the creature in Image 1 exactly: a single rounded-box body (a rounded cube, slightly
taller than wide ~1:1.2, generously radiused corners, NO separate head — the face sits on
the upper-front face); warm terracotta-orange flat fill; exactly two short rounded ear/arm
nubs; exactly four short stub legs set close together under the body; two small graphite dot
eyes with short curved brows, riding a faint pencil construction cross-line; at most a tiny
mouth line. Keep its proportions and small shoulder-companion scale. In SIDE/profile view
the near ear/arm nub is seen end-on as a small circular disc on the side face (the "side
swirl" in Image 2's SIDE panel) — keep this disc, and add NO other circle, navel, or emblem
anywhere on the body.

POSES — render five poses of a single hop, all in SIDE / profile view, arranged along a
shallow arc (low at the ends, peak in the middle): (1) CROUCH — gathered and compressed
down, legs bunched (wind-up); (2) TAKEOFF — the box stretched up and forward, legs extending
then trailing as it leaves the ground; (3) APEX — at the top of the arc, body neutral, legs
tucked; (4) LANDING — the box compressed as it touches down, legs reaching then splayed to
absorb, cast shadow tight; (5) RECOVER — back to the low resting pose. Change ONLY this hop
pose across the row; keep everything else identical to Image 1.

Keep the warm cream paper (#F2E6CC) with visible grain, the soft scribbled cast shadow, the
cross-hatch shadow on the far and under planes, and the full terracotta color of Image 1 —
identical identity in every pose, only the pose changing. Do NOT give the creature arms or
hands — the nubs may trail slightly but never extend into arms, reach, or grasp. Do NOT add
hair, a tuft, or anything breaking the clean top edge of the box. Keep the eyes as small
graphite dots, never large glossy cartoon eyes. Keep the four legs short stubs (no springy
limbs; close together on landing). Do not split the box into a separate head and body. Do
not render any text, captions, labels, numbers, or watermarks.

Warm pencil-test render: warm-graphite line (not vector black, not pure black), flat color
fills, cross-hatch shadow, warm cream paper, hole-punch production marks — the same
hand-drawn medium as Image 1 and Image 2.

16:9. A single horizontal model sheet: five poses of the same creature in profile, arranged
along a shallow arc (low–rising–peak–falling–low), even diffuse lighting, consistent size.
Left to right: crouch, takeoff, apex, landing, recover.
```

---

## Prompt 6 — Sleep-settle (¾-front, 3 poses)

```
Image 1 is the identity anchor — the canonical reference for this creature (a small
terracotta box-creature, ¾-front hero portrait). Image 2 is its turnaround sheet — use it
to match correct viewing angles; identity always comes from Image 1.

Match the creature in Image 1 exactly: a single rounded-box body (a rounded cube, slightly
taller than wide ~1:1.2, generously radiused corners, NO separate head — the face sits on
the upper-front face); warm terracotta-orange flat fill; exactly two short rounded ear/arm
nubs projecting from the left and right faces at mid-height; exactly four short stub legs
set close together under the body; two small graphite dot eyes with short curved brows,
riding a faint pencil construction cross-line (a horizontal midline and a soft vertical
centerline); at most a tiny mouth line. Keep its proportions and small shoulder-companion
scale.

POSES — render three poses of falling asleep, all in ¾-front view: (1) AWAKE — the low
resting pose, eyes open dots; (2) DROOP — the box slumped a little lower and softer, eyes
lowered toward the construction midline, nubs drooping, brows soft; (3) ASLEEP — fully
settled at its lowest and softest, the eyes CLOSED and drawn as two small downward graphite
arcs riding the midline (the closed state of the dot eyes, not a new eye style), nubs at
rest. Change ONLY this sleep pose across the row; keep everything else identical to Image 1.

Keep the warm cream paper (#F2E6CC) with visible grain, the soft scribbled cast shadow
beneath the body, the cross-hatch shadow on the far and under planes, and the full
terracotta color of Image 1 — identical identity in every pose, only the pose changing.
Do NOT give the creature arms or hands — the nubs never extend, reach, bend, or grasp. Do
NOT add hair, a tuft, or anything breaking the clean top edge of the box. Keep the eyes as
small graphite dots (closed arcs when asleep), never large glossy cartoon eyes. Keep the
four legs short and close together (no wide-splayed or biped stance). Do not split the box
into a separate head and body. Do not render any text, captions, labels, numbers, or
watermarks.

Warm pencil-test render: warm-graphite line (not vector black, not pure black), flat color
fills, cross-hatch shadow, warm cream paper, hole-punch production marks — the same
hand-drawn medium as Image 1 and Image 2.

16:9. A single horizontal model sheet: three poses of the same creature in a row, evenly
spaced, all on one shared horizon line, even diffuse lighting, consistent size across the
row. Left to right: awake, droop, asleep.
```

---

## When a sheet drifts — the one-pose-per-image fallback

If a sheet comes back with identity wandering across the panels (most likely on the 4- and
5-pose sheets — perch, hop), switch to the template's native mode: **one pose per 16:9
image, one variable changed.** This is what the research says NB2 is actually best at, and
it re-anchors cleanly. Keep the same two references attached. Replace the POSES line and the
layout line with a single pose, e.g. for the hop apex:

```
POSES — render ONE pose: the creature at the apex of a hop, SIDE / profile view, body
neutral and floating at the top of its arc, the four stub legs tucked, the near nub showing
its end-on disc. Change ONLY the pose; keep everything else identical to Image 1.
...
16:9. The single creature centered in profile, on warm cream paper, soft cast shadow below.
```

Then generate the five hop keys as five separate images and lay them out yourself. Slower,
but it's the mode that holds identity — and it's closer to how the real pipeline runs
(one anchor pair → one Seedance clip).

## Trying it in ChatGPT too

The same prompts work in ChatGPT's image edit — attach the same two references and paste the
same block. Two caveats: ChatGPT tends to be weaker at multi-reference identity lock and at
multi-panel sheets, so expect to lean on the one-pose-per-image fallback sooner, and it's
more likely to "prettify" toward a clean digital look — watch for the cross-hatch and the
construction cross-line getting cleaned away (that's the SF01 style-drift / register
violation). Run the same pose in both NB2 and ChatGPT and compare; it's a useful bake-off on
which holds the pencil register better.

---

*Reminder: these sheets are exploration. The Bible's motion plates come from your pencil
keys (Phase 4, human-owned timing) and ingest zero-drift via `bible add`. If an NB2 pose is
good enough to keep, it still has to clear the similarity gate against the anchor before it
could land — treat the model as a sketch partner here, not the source of truth.*
