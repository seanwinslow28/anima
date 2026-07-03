---
name: storytelling-architecture
description: Story shape that makes someone keep reading. Designs the narrative spine, the beat order, the open loops, and the tension arc BEFORE any sentence is written. Outputs a beat map (a step-outline), never finished prose. Use when asked to "make this addictive", "structure this story", "fix the hook", "why won't people finish this", "outline this essay/post/case study", "shape the narrative", "add tension", "this drags", or as the first stage of the Substack chain (pairs with substack-value-engine, then writing-voice-modes, then writing-humanity-pass). Reusable for essays, talks, and case studies, not just newsletters.
---

# Storytelling Architecture

## Purpose

Own the WHAT-order and WHAT-shape of a story so a reader cannot stop. This skill decides the beat sequence, where loops open and close, and how tension escalates. It does NOT write sentences. Its output is a **beat map**: a McKee-style step-outline (one or two lines per beat saying what happens and how it turns), handed downstream to the voice layer that writes the actual prose.

The load-bearing rule (from the research, McKee/Truby/the broetry failure): **structure owns ORDER, voice owns SENTENCES.** If this skill writes finished sentences, its default phrasing survives into the final draft and flattens the writer's voice. So it emits beats, never lines.

## When to Use

- First stage of the Substack chain, before `substack-value-engine` adds the value gate and `writing-voice-modes` writes the prose.
- "Make this addictive", "fix the hook", "why won't people finish this", "this drags", "shape the narrative", "outline this".
- Structuring essays, conference talks, case studies, post-mortems, threads: anywhere a reader needs to be pulled forward.

## The Output: A Beat Map (never prose)

A beat map is a numbered list of beats. Each beat is one or two plain lines: what happens, how it turns (the but/therefore), and any loop it opens or closes. Mark the hook, the turn, and the payoff. Example shape (content is illustrative, not a template to fill):

```
BEAT MAP: working title
1. COLD OPEN [opens loop L1]: drop reader into the concrete moment of failure. Raises the question: why did this break?
2. THEREFORE: the stakes, what this failure cost / threatened.
3. BUT: the first fix fails / makes it worse. Escalate. [L1 still open]
4. THEREFORE: the real diagnosis surfaces. The turn.
5. PAYOFF [closes L1]: the fix that worked.
6. SO-CAN-YOU: hand-off point where value-engine's Transfer lands.
```

Do not write the sentences. Write the beats. The voice layer authors every line fresh against this map.

## The Six Enforced Mechanics

Each is a gate. Run the beat map against all six.

1. **But/Therefore beat test.** Between any two adjacent beats you must be able to insert *but* (conflict) or *therefore* (consequence). If only *and then* fits, the seam is dead: merge the beats, cut one, or add a reversal/consequence. Flag additive-only logic ("Also", "Additionally", "Next", "And then").

2. **Cold open / in medias res.** Open on a concrete moment, scene, or live tension. Never on context, definitions, or "In this piece I'll...". The first beat raises ONE specific unanswered question. Throat-clearing openings are a fail.

3. **Open-loop budget.** Every loop the map opens must be closed by a later beat. In short form, a loop closes within ~1-3 beats/paragraphs or the reader disengages from frustration. Track each loop; flag any left open at the end. (Justify loops by *motivational tension*, not memory. The Zeigarnik "you'll remember it" claim fails replication: see `references/story-mechanics.md`.)

4. **Closeable gap, not chasm.** The hook promises a payoff that feels imminent and attainable ("the one line that broke the build"), not vast and vague ("the secret of great writing"). Flag hooks that promise more than the beats can pay off.

5. **Withhold the rescue.** Don't resolve the central tension in the first beat and then merely explain. Escalate (progressive complication) before the payoff. The opening question must outlive its introduction.

6. **Slippery-slide section ends.** The last beat of each section creates forward pull (a teased turn, a withheld answer), not a clean summary that gives the reader permission to stop. (When the voice layer realizes this, the natural punctuation is an em dash, which is banned downstream. Note it as "forward-pull line"; let `writing-humanity-pass` enforce the punctuation. Don't pre-solve it.)

## Story Scaffolds (pick one, apply as form not formula)

These set beat ORDER. Treat them as a checklist of pressures the piece should satisfy, never as slots to fill with canonical connective tissue ("and that's when I realized..."). If a beat can only be hit one canonical way, it has become formula. See `references/story-mechanics.md` for the full set and when each fits.

- **Problem-Struggle-Fix** (default for maker/technical posts): the real problem, the failed attempts, the fix that worked. Maps cleanly onto a post-mortem.
- **Before-After-Bridge**: the painful before, the better after, the bridge that connects them (the bridge is the value).
- **In-Medias-Res Quest**: cold open mid-crisis, backfill context in fragments, resolve.
- **Pixar (Once / Every day / Until one day / Because / Until finally)**: for arc-heavy personal narratives.

## Anti-Formula Guard (the seam must stay invisible)

The failure mode is structure leaking into the surface until a reader can name your template (the LinkedIn broetry trap). Two checks, applied to the beat map:

- **Specificity check (McKee archetype vs stereotype):** each beat carries a detail specific to THIS story, not a generality any template would produce. Generic beat = formula has leaked. Concrete, lived, idiosyncratic beat = sound.
- **Nameable-template check:** if the beat order is the obvious canonical shape with nothing bent, vary it (start later, reorder a reveal, fold two beats). The reader should *feel* the structure, never name it.

## The Chain Contract (what this skill must NOT do)

```
storytelling-architecture → substack-value-engine → writing-voice-modes → writing-critique → writing-humanity-pass
   (beat SHAPE + order)       (value GATE + payoff)    (every SENTENCE)      (RED-TEAM, advisory)  (scrub + no em dash)
```

- This skill emits a beat map. It is **forbidden from writing finished sentences** or specifying how a beat is phrased.
- `substack-value-engine` annotates the same map with the value gate (Itch / Solution / Transfer) and the narrative-to-value seam. Still not prose.
- `writing-voice-modes` writes 100% of the sentences fresh against the beats. It must never reorder beats.
- `writing-humanity-pass` runs last.

Handoff is in-context: the beat map flows to the next stage in the working context, not as a saved file.

## Related Skills

- `substack-value-engine`: the next stage. Adds the value gate and the narrative-to-value seam to the beat map. Story makes them read; value-engine makes it worth their time.
- `writing-voice-modes`: writes every sentence against this beat map. This skill owns ORDER; voice owns SENTENCES. Never let voice reorder beats; never let this skill phrase a line.
- `writing-critique`: red-teams the voiced draft between voice and humanity-pass. It critiques structural execution (hook, but/therefore seams, loop closure) but never re-litigates the beat map this skill committed.
- `writing-humanity-pass`: the final scrub. Realizes forward-pull lines without em dashes.
- `creative-writing`: owns format/word-count/platform constraints. Beat maps fit within those.

## References

- `references/story-mechanics.md`: the full mechanic catalog with cited sources, the four scaffolds and when each fits, the evidence floor (what's science vs craft vs lore), and the Zeigarnik honesty note. Read when designing a non-obvious arc or debugging why a structure feels flat.

## Success Criteria

- [ ] Output is a beat map (step-outline), not prose.
- [ ] Every adjacent beat passes the but/therefore test (no and-then seams).
- [ ] Cold open raises one specific question; no throat-clearing.
- [ ] Every opened loop closes; short-form loops close within ~1-3 beats.
- [ ] The hook's gap is closeable, and the central tension is withheld then escalated.
- [ ] Each section ends on forward pull, not a summary.
- [ ] Specificity check passes (no generic beats); template is not nameable.

## Copy/Paste Ready

```
"Build a beat map for this post"
"Make this story addictive, structure only"
"Fix the hook and the tension arc"
"Why won't people finish this? Restructure it"
"Outline this as a problem-struggle-fix"
"Run the storytelling chain on this idea"
```
