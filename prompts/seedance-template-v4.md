# Seedance 2.0 Prompt Template — v4

> **Status:** Locked 2026-05-10 — winning structure from the prompt bake-off (Variant V08 combined_best, score 12/20).
> **Supersedes:** [docs/2026-05-02-act2-seedance-prompts-v3-conversation-style.md](../docs/2026-05-02-act2-seedance-prompts-v3-conversation-style.md) (v3)
> **Evidence:** [docs/2026-05-09-seedance-prompt-bakeoff-results.md](../docs/2026-05-09-seedance-prompt-bakeoff-results.md)
> **Design spec:** [docs/2026-05-09-seedance-prompt-bakeoff-design.md](../docs/2026-05-09-seedance-prompt-bakeoff-design.md)

## When to use this template

For all Seedance 2.0 image-to-video generations on hand-drawn pencil-test aesthetic content. Fill in the `[BRACKETED]` placeholders with shot-specific content; leave the structural scaffolding alone.

## The template

```
Traditional 2D animation pencil test in the style of classic Disney rough animation. Starting with [SHOT START STATE], transitioning through [SHOT MIDDLE BEAT — include animation-timing language: anticipation / weight shift / delayed follow-through / hold / settle], ending [SHOT END STATE]. [SHOT-SPECIFIC CONTINUITY REMINDER — clean-shaven / stubble / no stylus / wardrobe note / what stays static].

CAMERA: Locked tripod, micro push-in 2%, 50mm look.

STYLE: Graphite on cream paper, organic line wavering, warm ivory tone.

Duration: [N] seconds.
```

## Locked rules (do NOT relax)

These are baked in by the research priors and the bake-off evidence. Modifying them invalidates the template.

1. **Word count target: 80–100 words.** Hard cap 100. <30 hallucinates, >150 attention-collapses. V08 winning prompt is ~91 words.
2. **No in-prompt negation.** Never write "no X." Replace every negative with an affirmative descriptor. (Per Phase 1 research; V00 control violated this and lost to V01 by 2 points.)
3. **Banned words.** Never use: `cinematic`, `4K`, `8K`, `ultra high res`, `sharp focus`, `polished`, `smooth`, `highly detailed`, `studio-quality`, `masterpiece`, `lens` (standalone), `anime` (unqualified).
4. **Don't redescribe the frames.** The start/end anchors carry composition, pose, line quality, paper grain. Don't restate.
5. **Single camera instruction.** Multiple camera directives produce jitter. The locked V08 line is `Locked tripod, micro push-in 2%, 50mm look.` — do not add additional camera modifiers.
6. **Affirmative material descriptors only.** "Graphite on cream paper, organic line wavering, warm ivory tone" — what you DO want, never what you don't.
7. **Genre anchor is load-bearing.** Always lead with `Traditional 2D animation pencil test in the style of classic Disney rough animation.` Removing it crashed V06's score by 8 points.
8. **No AUDIO line.** V04's audio cues crushed scores by 8 points even with `generate_audio: False` — in-prompt audio descriptors leak into the visual generation as confounds.

## Per-axis verdicts (from the bake-off)

- **Genre anchor (Axis A):** KEEP. Removing it dropped V06 to 4/20 (vs V01's 12/20). The "classic Disney rough animation" anchor is load-bearing on Seedance.
- **Action framing (Axis B):** USE TRANSITION-ARC for start+end frame mode. V02 outscored V01 on the identity-stress S0 shot by 2 points by switching to "Starting with X, transitioning through Y, ending Z" framing.
- **Animation-timing language (Axis C):** USE WHEN THE ACTION IS LOCOMOTION. V03 helped W1 (motion shot) but hurt S0 (transition shot) by 2 points. The "anticipation/weight shift/follow-through" vocabulary works for physical motion; for abstract transitions, stay descriptive instead.
- **Audio cues (Axis D):** NEVER USE. V04 = 4/20. The AUDIO line crushes results across both shots even with `generate_audio: False`.
- **Canonical camera "micro push-in 2%, 50mm look" (Axis E):** USE INSIDE THE V08 STACK ONLY. Standalone (V05), it dropped scores by 4. In the V08 combination it didn't break things — likely because the surrounding stack absorbs the noise. The locked template includes it because V08 won; if you ever simplify the template, swap to "Completely static, locked tripod" instead.
- **Style block density (Axis F):** USE THE TRIMMED 3-DESCRIPTOR FORM. V07 standalone scored 6/20, but V08 with the same trimmed style won. Trimming alone removes too much guidance, but the rest of the V08 stack carries the load. Keep it: "Graphite on cream paper, organic line wavering, warm ivory tone."
- **Stack (V08 combined-best):** Stacks cleanly. Combining transition-arc + animation-timing + canonical camera + trimmed style hits the same 12/20 ceiling as the best single-axis variants but produces 2 "great" picks (most of any variant). Stack provides the cleanest reusable structural template.

## Filling out the template

For a new shot:

1. Identify the **start state**, **middle beat**, and **end state** (transition-arc framing requires you to think in 3 beats — what's in the start anchor, what action happens, what's in the end anchor).
2. For the middle beat, embed animation-timing terms when the action is physical (walking, sitting, gesturing). For abstract transitions (props materializing, scene shifts), keep the middle beat descriptive without the anticipation/follow-through vocabulary.
3. Identify the **continuity reminder** for that shot (clean-shaven / stubble / stylus presence / what stays static / wardrobe).
4. Adjust the duration if the shot isn't 4s. (Seedance API minimum is 4s; if your shot is 3s, clamp to 4 and trim in assembly.)
5. Drop the filled prompt into the API call. Use the `seedance_generate.py` script with `--shot <ID>` if your shot is registered in `seedance_shotlist.yaml`.
6. Run with two seeds (e.g. 42 and 1337) and pick the better output. Single-seed runs are not reliable — even the bake-off winner only had 2/4 cells declared "great".

## Example fills (from Act 2 production)

### W1 — Walk Film (winning V08 W1 prompt, ~91 words)

```
Traditional 2D animation pencil test in the style of classic Disney rough animation. Starting with Sean stepping into frame from the left amid floating Film props, transitioning through a steady walk cycle with anticipation in his forward weight shift and a slight delayed follow-through as his head turns to take in the props, ending as he approaches the right edge. The props stay stationary; only Sean moves. Sean is clean-shaven throughout.

CAMERA: Locked tripod, micro push-in 2%, 50mm look.

STYLE: Graphite on cream paper, organic line wavering, warm ivory tone.

Duration: 4 seconds.
```

### S0 — Stubble grow-in / desk transition (winning V08 S0 prompt)

```
Traditional 2D animation pencil test in the style of classic Disney rough animation. Starting with Sean mid-stride amid floating AI news headlines, transitioning through a slow-down anticipation and chair-bend with weight shift settling into a seated pose as the desk, laptop, monitor, coffee mug, and chair materialize, ending in held seated working pose with subtle 5-o'clock shadow stubble grown in.

CAMERA: Locked tripod, micro push-in 2%, 50mm look.

STYLE: Graphite on cream paper, organic line wavering, warm ivory tone.

Duration: 4 seconds.
```

(Append additional concrete fills here as Act 2 shots are written.)
