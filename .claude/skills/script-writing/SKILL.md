---
name: script-writing
description: Screenplay format, structure, and production handoff for animated short films. Covers industry-standard screenplay format, beat sheets, short-form structural patterns (therefore/but, kishotenketsu, want engine), scene breakdowns, shot descriptions for animation handoff, and table reads. Use when asked about "write a script", "screenplay", "beat sheet", "scene breakdown", "outline a short", "animated short", "storyboard script", "shot descriptions", or "format this as a screenplay". For voice, jokes, dialogue punch-up, and how it should SOUND like Sean, pair with `screenwriting-modes`.
---

# Script Writing (Animated Shorts)

## Purpose

Write screenplays for animated short films using industry-standard format. This skill owns **format, beat structure (ORDER), and production handoff** — beat sheets, screenplay formatting, short-form structural patterns, scene breakdowns, and shot descriptions that hand off cleanly to the animation pipeline.

**This skill owns ORDER; `screenwriting-modes` owns SENTENCES.** Format and beat-order live here; voice, jokes, dialogue mechanics, taste, and Sean's signature moves live in `screenwriting-modes` (the screen twin of `writing-voice-modes`). Keeping them separate is deliberate: when a structure skill writes the actual sentences, its phrasing flattens the voice. Generate structure here, draft voice there, then format here. See **Integration with `screenwriting-modes`** below.

## When to Use

- Writing a screenplay for an animated short (1-15 minutes)
- Creating a beat sheet or outline before writing
- Formatting dialogue, action lines, and transitions
- Writing shot descriptions for storyboard/animation handoff
- Reviewing or giving notes on a script draft
- Adapting a concept into screenplay format

## Examples

**Example 1: Beat Sheet from Concept**
```
User: "I have an idea for a 3-minute animated short about a robot who learns to garden. Help me outline it."
Claude: [Uses script-writing]

## Beat Sheet: "Root Access" (est. 3 min / ~3 pages)

| # | Beat | Duration | Purpose |
|---|------|----------|---------|
| 1 | COLD OPEN: Robot powers on in abandoned greenhouse. Dead plants everywhere. | 15s | Establish world, protagonist, problem |
| 2 | DISCOVERY: Robot finds one living seedling under rubble. | 10s | Inciting incident |
| 3 | FIRST ATTEMPT: Robot waters seedling with fire hose pressure. Soil everywhere. | 20s | Comic failure, show literal thinking |
| 4 | LEARNING: Robot observes a spider watering a web with dew drops. Mimics gentleness. | 30s | Midpoint turn — observation over force |
| 5 | MONTAGE: Robot tends garden with increasing care. Seasons implied by light shifts. | 40s | Growth (literal and metaphorical) |
| 6 | SETBACK: Storm destroys greenhouse. Robot stands in rain holding one broken stem. | 20s | Low point |
| 7 | RESOLVE: Robot replants the stem outdoors. No greenhouse needed. | 15s | Theme: growth requires letting go of control |
| 8 | PAYOFF: Time-lapse — garden spreads across the ruins. Robot sits among flowers. | 20s | Emotional resolution |

Total: ~2:50 + credits
Theme: Control vs. nurture
Tone: Wordless (no dialogue), Pixar-short style

Ready to write the full screenplay from this?
```

**Example 2: Screenplay Page**
```
User: "Write the opening scene"
Claude: [Uses script-writing]

                    ROOT ACCESS

FADE IN:

EXT. ABANDONED GREENHOUSE - DAY

Cracked glass panels. Vines reclaiming steel frames.
Through the haze, a SHAPE on a workbench — inert,
dust-covered.

A POWER FLICKER. Then another. A blue LED blinks to
life behind a faceplate.

ROBOT (model: GRN-7) sits up. Servos whine. It looks
at its hands — three-fingered, industrial. Flexes them.

GRN-7 steps off the bench. CRUNCH — dead leaves
underfoot. It looks down. Looks around.

ROW AFTER ROW of dead plants in cracked pots. Brown
stalks. Dry soil spilling onto the floor.

GRN-7 tilts its head. The LED behind its faceplate
shifts from blue to amber.

It picks up a dead stem. The stem SNAPS. GRN-7 stares
at the broken halves.

A SOUND — barely audible. Dripping water.

GRN-7 follows the sound to the far corner where a
CRACK in the ceiling lets in a thin shaft of light.
Beneath it: a single GREEN SEEDLING pushing through
the rubble.

GRN-7 kneels. The faceplate LED shifts to green.

                                        CUT TO:
```

**Example 3: Dialogue Polish**
```
User: "This dialogue feels flat. Can you punch it up?"

Original:
  MAYA: I don't want to go.
  KAI: You have to. It's important.
  MAYA: Why is it important?
  KAI: Because everyone is counting on you.

Claude: [Uses script-writing]
The issue: both characters are saying exactly what they mean.
Good dialogue is oblique — characters talk around the real emotion.

Revised:
  MAYA
    (organizing a shelf that's already organized)
  I was going to reorganize the supply room today.

  KAI
  The supply room.

  MAYA
  It's a mess in there.

  KAI
    (beat)
  Eighty people, Maya.

  Maya's hand stops on a jar.

  MAYA
  I know how many.

Same information, but now: Maya deflects with busywork (shows avoidance without stating it), Kai uses a number instead of a lecture (specific > vague), and the physical action (hand stopping) replaces an emotion line.
```

## Screenplay Format Reference

### Page Elements

| Element | Format | Example |
|:--------|:-------|:--------|
| Scene Heading | ALL CAPS, `INT./EXT. LOCATION - TIME` | `INT. GREENHOUSE - NIGHT` |
| Action | Present tense, what the audience SEES and HEARS | `GRN-7 kneels beside the seedling.` |
| Character Name | ALL CAPS, centered above dialogue | `MAYA` |
| Dialogue | Under character name, narrower margins | `I know how many.` |
| Parenthetical | Under character name, before dialogue | `(sotto voce)` |
| Transition | Right-aligned, ALL CAPS | `CUT TO:` |
| CONT'D | After page breaks mid-scene | `MAYA (CONT'D)` |

### Animation-Specific Additions

Standard screenplay format works, but animation scripts benefit from:

| Addition | When | Example |
|:---------|:-----|:--------|
| **Camera direction in action** | Key compositions | `WIDE SHOT: The greenhouse stretches to the horizon.` |
| **Timing cues** | Precise comedy beats | `Beat. Then — SPLASH.` |
| **SFX notation** | Sound design is primary storytelling | `SFX: Metallic GROAN of bending steel` |
| **Visual shorthand** | Wordless sequences | `MONTAGE - SEASONS PASSING (see shot list)` |
| **Emotion indicators** | For character animators | `GRN-7's faceplate LED shifts from blue to amber.` |

### Page Timing

- **1 page ≈ 1 minute** of screen time (industry standard)
- Animation tends to run **slightly longer** per page (more visual action, less dialogue)
- A **3-minute short** = roughly **3-4 pages** of screenplay
- A **10-minute short** = roughly **10-14 pages**

## Beat Sheet Structure

A beat sheet maps the emotional arc before writing full scenes.

### For Shorts Under 5 Minutes (6-8 Beats)

| # | Beat | Function |
|:--|:-----|:---------|
| 1 | Hook | Open with a question or image that creates curiosity |
| 2 | Establish | Show the character's world and want |
| 3 | Inciting Incident | Something disrupts the status quo |
| 4 | Escalation | Character tries to solve the problem (fails or partially succeeds) |
| 5 | Crisis | The worst moment — the plan completely fails |
| 6 | Turn | Character discovers a new approach (theme crystallizes) |
| 7 | Climax | Final attempt using the new understanding |
| 8 | Resolution | New status quo (mirror the opening image, transformed) |

### For Shorts 5-15 Minutes (10-12 Beats)

Add between beats 4 and 5:
- **Midpoint Shift**: Stakes change or new information reframes the problem
- **Subplot Beat**: Secondary character or relationship gets a moment
- **False Victory/Defeat**: Looks like it's resolved, but isn't

### Beat Sheet Template

```markdown
## Beat Sheet: "[TITLE]" (est. X min / ~X pages)

**Logline:** A [CHARACTER] must [GOAL] before [STAKES/DEADLINE].
**Theme:** [One sentence — what the film is really about]
**Tone:** [e.g., wordless comedy, bittersweet, surreal, etc.]

| # | Beat | Duration | Purpose |
|---|------|----------|---------|
| 1 | | | |
| 2 | | | |
...

**Opening Image:** [First thing the audience sees]
**Closing Image:** [Last thing — mirrors/transforms the opening]
```

## Short-Form Structural Patterns

These are the structural spines for a 3–5 minute short — ORDER, not voice. Pick one as the skeleton, then draft the voice with `screenwriting-modes`.

| Pattern | Spine | Best for |
|:--------|:------|:---------|
| **Therefore/But engine** (Pixar) | Every beat connects via "therefore" (consequence) or "but" (complication) — never "and then." Want X → THEREFORE try A → BUT the flaw → THEREFORE try B → BUT catastrophic escalation → THEREFORE confront the flaw. | Causal comedy that escalates; the default propulsion engine. |
| **Want engine** (Pixar) | Give the protagonist one primal, instantly readable desire. Comedy = absurd attempts to get it; success is irrelevant. No exposition — the Want IS the character. | Wordless or near-wordless shorts; instant setups. |
| **Kishotenketsu** (Miyazaki) | Four parts, no antagonist: Ki (establish routine) → Sho (deepen, low stakes) → Ten (an unrelated chaotic non-sequitur shatters the tone) → Ketsu (character adapts to a new equilibrium). | Disruption-of-calm comedy where conflict-escalation would feel forced. |
| **Trope-autopsy spine** (Sean-native) | Stand a narrator/frame outside a cliché (the quit-your-job-for-family movie, the New-Year's-reinvention myth) and flick it across the runtime via Declare-then-Puncture. | Parody/satire shorts; pairs with the Ironic Narrator move in `screenwriting-modes`. |

**Callback payoff debt:** anything planted gets paid off before the end, preferably physically — but in Sean's work this is *reflexive, not engineered*. Structure the spine; let the callbacks emerge in the voice draft (see `screenwriting-modes`). Don't pre-plan "a setup for later."

**Choosing endings (structural):** cathartic resolution (Pixar/Waititi) vs. deflationary/ambiguous (Kaufman/Miyazaki). For Sean, the closer is almost always a **dirty victory** — a real win with the squalor still in frame — and the closing image mirrors the opening, transformed. Keep the emotional mechanics in `screenwriting-modes`; here, just make sure the beat sheet *has* a closing-image beat that earns it.

## Dialogue Craft

These are the format-level fundamentals — they keep dialogue clean and producible. The *voice* layer (how Sean's characters actually sound: register-contrast casting, status-assigned verbal fingerprints, the confession deluge, comic under-reaction) lives in `screenwriting-modes`. Use these rules to keep dialogue tight; use that skill to make it sound like him.

### Rules for Animation Dialogue

1. **Less is more** — Animation can show emotion through movement, expression, timing. Don't write dialogue for what the character can act.
2. **Voice test** — Read every line aloud. If it sounds written, rewrite it.
3. **Oblique > direct** — Characters rarely say exactly what they feel. They deflect, joke, understate.
4. **Cadence matters** — Short lines for tension. Long lines for rambling/nervous energy. Fragment sentences for naturalism.
5. **Subtext through action** — Pair dialogue with contradicting or amplifying physical action (parentheticals and action lines).

### Common Dialogue Problems

| Problem | Fix |
|:--------|:----|
| On-the-nose | Have the character talk about something else while meaning the real thing |
| Exposition dump | Break info across scenes; have characters discover things |
| All voices sound the same | Give each character a verbal tic, vocabulary level, or sentence rhythm |
| Too much dialogue | Delete every line that could be replaced by a look, gesture, or silence |
| Flat response patterns | Never let Character B directly answer Character A's question |

## Production Handoff

### From Script to Animation Pipeline

The screenplay is the input to Stage 1 of `animation-pipeline`. Handoff checklist:

1. **Scene numbering** — Every scene heading gets a number for the shot manifest
2. **Shot suggestions** — Note camera angles in action lines where critical to storytelling
3. **Timing notes** — Flag beats that require specific frame counts (comedy timing)
4. **Character list** — Appendix with character descriptions for model sheet creation
5. **SFX/Music cues** — List all sound effects and music moments for audio pre-production
6. **Dialogue isolation** — Pull all dialogue lines into a separate table for voice recording

### Script-to-Shot Breakdown Format

```markdown
## Shot Breakdown: Scene 3

| Shot | Duration | Action | Dialogue | Camera | Notes |
|------|----------|--------|----------|--------|-------|
| 3.1 | 2s | GRN-7 picks up hose | — | MS | Comic setup |
| 3.2 | 1s | Turns valve | — | CU on valve | Build anticipation |
| 3.3 | 3s | BLAST of water destroys pot | — | WIDE | Hold 6f on impact for comedy |
| 3.4 | 2s | GRN-7 blinks | — | CU faceplate | Deadpan reaction |
```

## Table Read Protocol

For reviewing a draft with fresh eyes:

1. **Cold read** — Read the entire script straight through without stopping. Note emotional reactions, confusion points, and where attention drifts.
2. **Logic pass** — Does every scene connect to the next? Any plot holes or unmotivated actions?
3. **Dialogue pass** — Read only the dialogue out loud. Does each character have a distinct voice?
4. **Trim pass** — Can any scene be cut without losing the story? (If yes, cut it.)
5. **Opening/closing mirror** — Does the final image reflect or transform the opening?

## Integration with `screenwriting-modes`

The two skills compose. This one owns format, beat order, and handoff; `screenwriting-modes` owns voice, jokes, taste, and the emotional engine.

**Order of operations:**

1. **Structure here** — pick a structural spine, build the beat sheet, lock the closing-image beat.
2. **Voice there** — draft the actual scenes/dialogue with `screenwriting-modes`, loose and fast. Sean drafts voice-first, format-second (run-on prose dialogue blocks) — that is the rule, not a mistake. Don't train the looseness out at this stage.
3. **Format here** — run the format pass over the voice draft: scene headings, character cues, parentheticals, transitions, page timing.
4. **Table read** — review with the protocol above.

**When structure and voice disagree:** a `CUT TO:` is format, structure, *and* a joke at once. If a structural beat and a voice move collide on one of these, resolve toward the joke — the cut exists because it's funny. But voice doesn't get to blow up the beat order to land a gag: compress the joke to fit the structure instead.

## Success Criteria

- [ ] Beat sheet maps emotional arc with clear purpose per beat
- [ ] Screenplay uses correct format (scene headings, action, dialogue, transitions)
- [ ] Page count matches target runtime (1 page ≈ 1 minute)
- [ ] Dialogue passes the read-aloud test (sounds spoken, not written)
- [ ] Action lines describe only what the audience sees and hears
- [ ] Animation-specific cues included (timing, SFX, visual shorthand)
- [ ] Production handoff materials ready (shot breakdown, character list, SFX list)

## Related Skills

- `screenwriting-modes` — The voice/taste twin (calibrated to Sean). Owns how dialogue and action SOUND, the six filmmaker modes, the signature-moves table, and the WHAT layer. Pair on every creative script; this skill provides the structural frame, that one provides the voice within it.
- `animation-pipeline` — Takes the finished script into production (Stage 1 input)
- `creative-director` — Project planning, critique rubrics, creative vision
- `2d-animation-principles` — Animation rules that inform shot descriptions and timing cues

## Copy/Paste Ready

```
"Help me outline a short film about [concept]"
"Write a beat sheet for a 5-minute animated short"
"Write the screenplay for scene 3"
"Pick a structural spine for this short"
"Break this script into shots for storyboarding"
"Do a table read on this draft"
"Format this as a proper screenplay"
```