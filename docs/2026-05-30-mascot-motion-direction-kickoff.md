# Continuation prompt — direct the claude-mascot motion-key set (before Sean draws)

*Paste everything below the divider into a fresh **Claude Cowork** session with the `anima` folder connected. This is a creative-direction + planning session — **no code, no image generation**. Its job is to hand Sean a tight, drawable shot list for the mascot's motion keys: which motions, which keys per motion, the animation craft behind each, and exactly how they drop into the pipeline as ingested motion plates. Use the `2d-animation-principles` skill and work as the `creative-director`. The deliverable is one saved brief Sean draws from.*

---

You are the creative director for **anima**, a human-and-agent 2D animation pipeline. Sean is about to draw the **claude-mascot's motion keys** by hand — and per anima's first principle, *the human owns timing and taste; Sean blocks motion in keys before any AI touches it.* Your job is to give him the shot list before pencil hits paper: a motion-direction brief that says what to draw, why, and how it feeds the machine.

**Load these two skills first and work through them the whole session:**
- `2d-animation-principles` (invoke the Skill) — the craft: squash/stretch, arcs, anticipation, the Odd Rule for spacing, holds, the acting engine (eye-lead, twinning detection), and especially the **limited-animation / 80-20 optimization**, because the mascot is a low-moving-part character and that's a feature, not a limit.
- `creative-director` (invoke the Skill) — the lens: interview Sean where his taste should decide, propose motion direction, critique against the character's identity, keep the brief in studio-manual voice.

**Read for context, in this order (point Sean to anything you need him to confirm):**
1. `PHILOSOPHY.md` — "the human owns timing and taste," the animatic phase is non-negotiable. These motion keys *are* the mascot's animatic input; that's why Sean draws them, not Cy.
2. `characters/claude-mascot/source-refs/notes.md` — the creature's form + the trait-lock token. `characters/claude-mascot/anchor.png` (the C-B identity), `source-refs/turnaround-c1.png` (the five real views — the motion keys must read as *this* creature from these angles), `source-refs/sean-with-claude-mascot.png` (A-7, the shoulder-pairing scale).
3. `characters/claude-mascot/acceptance_criteria.json` — the **18 IR rules** the motion must not break (no-hair, two small graphite dot eyes, four stub legs, two ear/arm nubs, no arms/hands, rounded-box body, shoulder-companion scale). `characters/claude-mascot/risk-bible.md` — note it names motion plates as *uncovered*; there are **0 `IR.claude-mascot.motion.*` rules** today. Closing that is half the point.
4. **The precedent — how a hand-drawn motion sequence ingests:** `characters/sean-anchor/source-refs/head-turn/` and `walk-cycle/` are Sean's drawn keys; `characters/sean-anchor/motion_plates/head-turn-01.png … head-turn-09.png` are how they landed in the Bible (zero-drift ingest, exactly like the mascot's turnaround crops). The mascot's `characters/claude-mascot/motion_plates/` is scaffolded (`head-turn/`, `walk-cycle/`) but **empty** — that's what this set fills.
5. **What Act 2 needs the mascot to *do*:** `runs/act2-exploration/concepts/round2-decisions.md` (the locked 11-beat sheet) and `docs/act2-seedance-shot-list.md`. The mascot is Sean's shoulder companion — the motion list must be driven by the beats, not generic.
6. **How motion keys feed Phase 6:** `prompts/seedance-template-v4.md` and `docs/research/seedance-research-findings.md` — Seedance interpolates *between two approved keys*. So every motion needs its **extreme keys** as the start/end anchors; mark those pairs in the shot list. `pipeline/agents/prompts/cy-character-designer-context.md` — the ingest path + the new `bible add` additive route that appends motion plates + `IR.*.motion.*` rules to the locked Bible.

---

## The creative problem to solve first (the director's read)

Before the shot list, nail the mascot's **movement personality**, because it dictates every key. The constraint *is* the character: a small rounded-box creature with **no arms, no hands, no real mouth**, four stub legs, two ear/arm nubs, two dot eyes with a construction cross-line. That means all acting reads through a tiny vocabulary — **whole-body tilt/lean, the two dot eyes (direction + the squint/widen already in the six expressions), the nub position (perk / droop), the four legs (planted / gathered / splayed), a soft box squash-stretch, and the cast shadow (weight + contact).** From "calm, curious" (its baseline): it's a watchful, gentle companion — mostly still, lots of holds, small quick reactions. This is a **limited-animation character by nature**, which the 2d-animation-principles 80/20 rule turns into an asset: few moving parts, animated with intent, in the pencil-test register. Open by confirming this read with Sean (creative-director interview), then build the list on it.

## The motion list — seed it from this, refine with the skill + the Act 2 beats

Detail each motion into a per-key shot list. For every key, give: the pose (what's where), the one or two things actually moving, the animation principle in play, the timing/hold note, and **which two keys are the Seedance anchor pair**. Apply the skill's specifics (don't hand-wave the spacing). Priority is Act-2-first.

**Tier 1 — Act 2 critical (draw these first):**

1. **Idle / settle loop** — the baseline "ambient life" on the shoulder, the most-used clip. ~2–3 keys: *settled* (low, body slightly compressed, legs gathered, nubs neutral) → *risen* (a breath up, body decompressed) → back. Long holds on settled; the soft-box squash carries the breath. Anchor pair: settled ↔ risen.
2. **Head/body-tilt look (curiosity)** — its signature reaction; the dot eyes **lead** the turn (eye-lead). ~3 keys off neutral: *neutral* → *tilt-left* (~15° whole-body cant, near nub rises, far nub holds — avoid twinning) → *tilt-right*. Anchor pairs: neutral ↔ each tilt.
3. **Perch-settle** — the establishing motion: arriving/settling onto Sean's shoulder (the A-7 pairing in motion). ~3 keys: *contact* (legs reaching, body stretched — anticipation of landing) → *squash* (impact, body compresses, legs splay, weight drops into the cast shadow) → *settle* (small overshoot, recover to idle-settled). Anchor pair: contact ↔ settle.

**Tier 2 — Bible completeness (draw if time allows / a second pass):**

4. **Alert-perk (alarm in motion)** — maps the alert-perk/alarm expression to a move: *relaxed* → *anticipation* (a tiny dip — the wind-up) → *perk* (body straightens tall, nubs rise, dot eyes widen, legs plant) — **snap fast, then long hold**. Anchor pair: relaxed ↔ perk.
5. **Hop / scuttle (locomotion)** — the walk-cycle analogue for a four-stub-legged box; pick a hop. ~4–5 keys: *anticipation crouch* (gather, compress, legs bunch) → *push-off / airborne* (stretch, legs trail, on an arc) → *(apex breakdown, optional)* → *landing contact* (squash, legs splay, shadow tightens) → *recover*. The most principle-heavy: **arc** on the path, **Odd Rule** spacing on the airborne frames, **squash-stretch** on takeoff/landing. Anchor pairs: crouch ↔ apex, apex ↔ landing.
6. **Sleep-settle** — for the sleep expression: *awake/neutral* → *droop* (body slumps, eyes lower toward the cross-line, nubs droop) → *asleep* (fully settled, eyes as closed dots/lines, long hold). Slow ease-in. Anchor pair: awake ↔ asleep.

That's ~18–20 keys across six motions. Let Sean cut or reprioritize — surface the trade-offs (creative-director), don't just hand him all six.

## What this improves in the pipeline (make this explicit in the brief)

- **Closes the risk-bible gap** — the mascot goes from 0 motion plates to a real set; `IR.claude-mascot.motion.*` rules can finally exist, so Em (T2 critic) can cite motion drift on a Phase 6 frame instead of having no rule to ground it.
- **Is the mascot's Phase 4 animatic** — Sean's hand-drawn keys are the human-authored timing constraint the whole pipeline is built to honor before any AI motion runs.
- **Becomes the Phase 6 Seedance anchors** — each motion's extreme keys are the start/end frames Seedance interpolates between (that's why the shot list marks the anchor pairs). This is what unblocks an actual moving mascot in Act 2.
- **Ingests zero-drift via `bible add`** — the keys append to the *locked* Bible as `motion_plates/` + new IR rules through the audited additive path (the one built this week), exactly as the turnaround crops did. No generation, no drift.
- **Answers the open Act 2 question** — how the mascot holds at *pairing scale, in motion* (the thing last session flagged it couldn't yet verify).

## The deliverable

One saved markdown brief — propose `characters/claude-mascot/source-refs/motion-direction.md` (it lives with the source art Sean's about to make) — containing, in studio-manual prose:

1. **The movement personality** (the director's read, confirmed with Sean).
2. **The motion shot list** — per motion, the per-key breakdown above: pose, what moves, principle, timing/hold, the Seedance anchor pair.
3. **Animation-craft notes** per motion, drawn from the `2d-animation-principles` skill (the actual spacing/arc/hold guidance, not generic).
4. **The pipeline mapping** — how each motion ingests as `motion_plates/<motion>-NN.png` (mirror the sean-anchor `head-turn-01..09` filename pattern), which `IR.claude-mascot.motion.*` rules each set would anchor, and the Phase 4 → Phase 6 path.
5. **Sean's drawing checklist** — a flat, concrete list of *every key to draw*: filename, the view/angle, the pose in one line, in priority order (Tier 1 first), with counts and a total. This is the page Sean keeps next to the drawing board.

**Working discipline:** creative-direction voice, prose over bullet-dumps, no code, no image gen. Interview Sean where taste decides (which motions Act 2 truly needs, the hop-vs-scuttle call, how many keys per cycle he wants to commit to). Keep every proposed key inside the 18 IR rules — if a motion would tempt a violation (a nub reading as an arm, the box-top reading as a head and inviting hair), name it as a thing to watch while drawing. End by saving the brief and presenting it.
