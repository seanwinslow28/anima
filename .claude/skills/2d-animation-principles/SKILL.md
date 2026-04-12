---
name: 2d-animation-principles
description: 2D animation physics, timing, and production rules for evaluating and planning animation. Covers gravity spacing (Odd Rule), arcs, smear synthesis, style modes (Rubber Hose through Spider-Verse), acting engine (twinning, eye lead, blink asymmetry), TV/limited optimization, and QA gates. Use when evaluating AI-generated pencil test keyframes, planning hold durations, validating in-between frame spacing, reviewing timing and expression arcs, choosing smear types, or diagnosing animation that feels "floaty", "robotic", or "snappy".
---

# 2D Animation Principles

## Purpose

Apply deterministic, physics-based animation rules when generating or evaluating 2D animation. Replace vague artistic direction with testable constraints derived from the physics of motion and production pipeline requirements. Operate in two modes: Pose-to-Pose (structured keyframe planning for acting and mechanics) and Straight-Ahead (sequential frame generation for fluid dynamics like fire, water, hair).

## When to Use

- Evaluating timing and spacing of AI-generated pencil test keyframes
- Planning hold durations for manifest-driven frame sequences
- Validating in-between frame spacing from ComfyUI ControlNet or video model interpolation
- Reviewing the expression arc across a keyframe sequence (CC08 continuity check)
- Choosing smear types for fast motion in in-between generation
- Adapting animation style to a specific era (Rubber Hose, Golden Age, Spider-Verse)
- Optimizing animation for limited budgets (reducing drawing count, hold-frame strategy)
- Reviewing animation for twinning, dead holds, or physics violations
- Diagnosing why a frame sequence feels "floaty", "robotic", or "snappy"

## Examples

**Example 1: Evaluating keyframe transition timing**
```
User: "Is the timing right for the F06→F10 transition in my pencil test?"
Claude: [Uses 2d-animation-principles] Analyzes the transition:
- F06 (glance down) holds 4 frames at 12fps = 0.33s — good for a contemplative beat
- F10 (the spark) is a head snap — fast reaction (2-4 frames at 24fps = 1-2 on Twos)
- The 4-frame hold on F06 provides breathing space before the pop at F10
- Physics: No gravity involved — this is an acting transition
- Acting: Eye lead should precede head turn by 2-3 frames in in-between generation
- Recommendation: Generate 1-2 in-betweens max. Favor the "pop" over smooth interpolation.
```

**Example 2: Evaluating animation quality**
```
User: "This walk cycle feels off — what's wrong?"
Claude: [Uses 2d-animation-principles] Runs QA gates:
- Physics Gate: Spacing is linear for 8 frames — FAIL (apply ease-in/out)
- Acting Gate: Left and right arms swing identically — FAIL (twinning, offset by 2 frames)
- Production Gate: Character static for 36 frames between steps — FAIL (add moving hold with 1-2% drift)
```

**Example 3: Choosing a smear type for in-betweens**
```
User: "What smear type for the stylus gesture at F13→F18?"
Claude: [Uses 2d-animation-principles] Diagnoses the motion:
- F13→F18 is an arm sweep — ballistic arc, large displacement
- Displacement exceeds arm width = smear needed for in-between frames
- Style is pencil test (hand-drawn aesthetic) = Drybrush Smear most appropriate
- Duration: strictly 1 frame in the in-between sequence
- Note: The pencil trail effect at F18 is a COMPOSITING layer, separate from the smear
For the complete smear taxonomy (30 types), see references/smear-taxonomy.md.
```

## The Operating Loop

Every animation task follows Plan, Implement, Verify.

### Phase 1: PLAN (Configuration)

1. **Parse constraints**: Detect budget mode (TV vs Feature) and style profile (Rubber Hose, Golden Age, Spider-Verse, etc.)
2. **Asset strategy**: If budget mode is LIMITED_TV, check for existing cycles before generating new frames
3. **Audio sync**: If audio exists, extract phonemes and map to viseme library (7-9 mouth shapes). Visual accents lead audio hits by 2 frames
4. **Output**: An AnimationClipSpec defining FPS, exposure rate, style profile, and action beats

### Phase 2: IMPLEMENT (Synthesis)

1. **Blocking**: Generate Key Poses ensuring readable silhouettes (limbs occlude less than 30% of torso)
2. **Splining**: Interpolate between keys using physics rules (see Physics Engine below)
3. **Smear synthesis**: If displacement > object width, generate a smear frame (see `references/smear-taxonomy.md`)
4. **Layer optimization** (TV mode only): Separate static body from active mouth/eyes (cel stacking)
5. **AI generation validation**: If frames are AI-generated (Gemini, ComfyUI, video model), validate that spacing between keyframes follows the intended easing curve. AI interpolation models (RIFE/FILM/Veo/Wan) default to linear spacing — post-validate with explicit ease curves or reject and re-prompt.

### Phase 3: VERIFY (QA Gates)

Run all three gates before finalizing. Any failure blocks output.

| Gate | Check | Fail Condition | Fix |
|------|-------|---------------|-----|
| Physics | Spacing linearity | Linear spacing for >6 frames | Apply ease-in/out |
| Physics | Volume conservation | Scale_X * Scale_Y != ~1.0 during squash | Scale_perp = 1/sqrt(Scale_parallel) |
| Physics | Arc compliance | End effector follows linear path | Add arc breakdown |
| Acting | Twinning (pose) | L_Rot == R_Rot (tolerance <5%) | Offset one side by 2-4 frames |
| Acting | Twinning (timing) | Start_Frame_L == Start_Frame_R | Offset one limb start by 2 frames |
| Acting | Dead hold | Pixel variance == 0 for >12 frames | Add moving hold (1-2% drift) |
| Acting | Eye lead | Head turns before or with eyes | Eyes move 2-3 frames before head |
| Acting | Blink asymmetry | Close duration == Open duration | Close: 3fr, Hold: 1fr, Open: 4+fr |
| Production | Strobing | Displacement > width without smear | Add appropriate smear type |
| Production | Readability | Key pose held <3 frames | Extend to minimum 6 frames |
| Acting | Expression arc | Emotion jumps between consecutive keyframes without transition | Add intermediate expression in-between or adjust prompt (CC08) |
| Production | Hold duration | Key pose held <3 frames in manifest.yaml | Extend hold_frames value in manifest |
| Production | Loop continuity | F40 doesn't visually match F01 for seamless loop | Regenerate F40 with A-2 anchor reference |

## Physics Engine

### Gravity (The Odd Rule)

Gravity is acceleration, not speed. Displacement from a stop increases in odd number ratios: 1, 3, 5, 7.

```
Y_Pos[t] = Y_Pos[t-1] - (Unit_Dist * (2t - 1))
```

If spacing between frames is constant (linear), the motion looks "floaty". This is the most common physics failure.

### Arcs (Fourth Down Rule)

For organic motion, the breakdown pose at 50% time must be at 25% of the vertical distance from the apex. This creates the slow-out feel at the top of a jump or throw.

### Timing vs Spacing

- **Timing** = duration (frame count). "How long does the action take?"
- **Spacing** = rhythm (displacement per frame). "How does the speed change within that duration?"
- Never use linear spacing for organic characters. Always ease in and out.

### Follow-Through and Overlap

Child joints lag behind parent joints. Offset hierarchy:

```
Shoulder (t) -> Elbow (t+2) -> Wrist (t+4) -> Fingers (t+6)
```

For complete timing defaults, JSON schemas, and pseudocode patterns, see `references/timing-spacing.md`.

## Style Mode Switcher

Switch physics parameters based on the target style. Each style overrides interpolation, smear type, and framerate.

| Style | FPS | Interpolation | Smear Type | Squash/Stretch |
|-------|-----|---------------|------------|----------------|
| Rubber Hose (1920s) | Sync to BPM | Linear (constant) | Speed lines | High (rubber) |
| Golden Age (1930s) | 24 (Ones) or 12 (Twos) | Cubic bezier | Drybrush texture | Moderate (volume locked) |
| Screwball (1940s) | 24 (Ones) for zips | Zip (1-frame transit) | Elongated mesh | Extreme (volume broken) |
| Limited TV (1960s) | 12 (Twos) or 8 (Threes) | Step (hold-to-pop) | Abstract blur | Low (muzzle only) |
| Spider-Verse | 12 (Twos) forced | Stepped (no splines) | CMYK offset | Low (rigid) |
| Genndy 3D | 24 (Ones) | Snappy (sharp curves) | Geo blend (sub-frame) | Extreme (cartoony) |

For the full parameter override matrix and per-style verification tests, see `references/style-profiles.md`.

## Acting Engine

### Twinning Detection

If left and right limbs have identical rotation or timing, the character looks robotic. Always offset one side.

- **Pose twinning**: L_Limb_Rot == R_Limb_Rot at same frame. Fix: offset angle.
- **Timing twinning**: Both limbs start moving on same frame. Fix: offset start by 2 frames.

### The Acting Beat Pattern

Every significant action follows: Thought, Anticipation, Action, Overshoot, Settle.

1. **Thought**: Eyes move to target 2-3 frames before head turns. Processing pause: 6-12 frames.
2. **Anticipation**: Move opposite to intended direction. Duration: 4-8 frames (standard), 1-2 frames (shock).
3. **Action**: The main movement. Use Ones for fast, Twos for normal.
4. **Overshoot**: Extremities pass the target. Return: 3-5 frames (rigid), 6+ frames (soft).
5. **Settle**: Decelerate into final pose with dampened oscillation or ease-out.

### Duration Defaults (at 24fps)

| Action Type | Frame Range | Example |
|-------------|-------------|---------|
| Fast reaction | 2-4 frames | Surprise, impact, shock |
| Normal gesture | 8-12 frames | Conversation, pointing |
| Heavy effort | 16-24 frames | Lifting, pushing |
| Golden key hold | 6-12 frames | Readable attitude pose |
| Readability floor | 3 frames minimum | Anything less is invisible |

## TV/Limited Optimization

When budget mode is LIMITED_TV:

- **80/20 Rule**: 80% of screen pixels must be static. Only 20% (mouths, eyes, arms) update per frame.
- **Cel Stacking**: Separate character into Level_1_Body (static) and Level_2_Mouth (active). Mask seam with collar/necktie.
- **Exposure**: Default to Twos (12fps). Switch to Ones only if camera pans (prevents background strobing).
- **Bank First**: Query asset library for existing cycles before generating new frames.
- **Moving Holds**: If pose holds >24 frames, add 1-2% drift to prevent "dead" look.
- **Background Syncopation**: Use A-B-A-C patterns, not A-A-A repetition (prevents "Flintstones Effect").

### Pencil Test Pipeline Application

This project uses Limited principles at 12fps on Twos:
- Keyframes are held for their `hold_frames` value from manifest.yaml
- Static holds >12 frames should add 1-2% drift for moving hold effect (F18 holds for 13 frames — candidate for moving hold in in-between pass)
- The 80/20 rule applies to sprite compositing: Sean's body is mostly static while the sprite is the active element
- Bank reuse: F01 and F40 share the same A-2 anchor pose for seamless loop

## Walk Cycle Reference

Standard bipedal walk cycle on Twos (12fps):

| Frame | Pose | Notes |
|-------|------|-------|
| 1 | Contact | Heel strike, arms at extremes |
| 4 | Down | Lowest point, weight absorb |
| 7 | Passing | Vertical leg, arms cross center |
| 10 | Up | Highest point, push-off |
| 13 | Contact (mirror) | Opposite leg, loop start |

For curated instruction-output examples across all 6 modules, see `references/training-examples.md`.

## AI-Generated Frame Validation

When frames are generated by AI models (Gemini for keyframes, ComfyUI for in-betweens, Veo/Wan/Kling for interpolation), apply these additional checks:

### Spacing Drift
AI interpolation models default to linear spacing between keyframes, producing "floaty" motion. Post-validate:
- Extract positions of key features (head, hand, stylus tip) across interpolated frames
- Plot displacement per frame — should show ease-in/ease-out curves, not linear
- If linear: re-run with explicit timing hints, or post-process frame selection to simulate easing (drop frames near middle, keep more near extremes)

### Identity Drift in Interpolation
Video models (Veo 3.1, Wan 2.2, Kling 3.0) may drift character identity between start and end frames. Cross-check interpolated frames against A-2 anchor using SF02 (identity drift) criteria from the audit system.

### Smear vs AI Artifact
AI models may produce unintended smear-like artifacts (ghosting, double exposure, blurred limbs). Distinguish:
- **Intentional smear**: 1 frame only, follows motion vector, maintains volume
- **AI artifact**: Persists across multiple frames, random direction, breaks volume
If artifact: reject the interpolation and retry with different seed/parameters.

For full pipeline QA codes (HF/SF/CC), see `shared/references/pencil-test-pipeline-context.md`.

## Visual Reference Guides

When auditing frames or planning timing, load the relevant visual guide from `references/visual-guides/` for comparison. These are educational diagrams — use them as ground truth when evaluating AI-generated frames.

| Guide | File | Use When |
|-------|------|----------|
| Left/Right Body Map | `references/visual-guides/left-right-body-map.png` | Checking CC01 (stylus hand), any left/right orientation audit |
| Ease In/Out Spacing | `references/visual-guides/spacing-ease-in-out.png` | Diagnosing "floaty" motion, validating in-between spacing |
| Odd Rule Gravity | `references/visual-guides/spacing-odd-rule.png` | Validating falling/jumping arcs, gravity-based motion |
| Drybrush Smear | `references/visual-guides/smear-drybrush-example.png` | Evaluating smear frames in pencil test style (F13→F18 IB02) |
| Speed Lines | `references/visual-guides/smear-speedlines-example.png` | Evaluating directional motion indicators |
| Acting Beat Pattern | `references/visual-guides/anticipation-action-settle.png` | Planning acting transitions, validating anticipation/overshoot |
| Eye Lead | `references/visual-guides/eye-lead-head-turn.png` | Checking eye-before-head timing in head turn transitions |
| Follow-Through | `references/visual-guides/follow-through-overlap.png` | Evaluating hair/clothing drag, joint hierarchy lag |
| Squash & Stretch | `references/visual-guides/squash-and-stretch.png` | Validating volume conservation during bounces/impacts (F28 sprite) |
| Arc Paths | `references/visual-guides/arc-paths.png` | Checking in-between positions follow curves, not linear paths (F13→F18) |
| Staging / Silhouette | `references/visual-guides/staging-silhouette-test.png` | Evaluating pose readability — does it read in thumbnail? |
| Twinning Detection | `references/visual-guides/twinning-detection.png` | Checking for robotic symmetry in pose and timing |
| Line of Action | `references/visual-guides/line-of-action.png` | Evaluating pose energy and dynamism (S-curve vs stiff) |

**Usage protocol:** Before scoring a QA gate that has a matching visual guide, `Read` the guide image to calibrate your judgment. Compare the AI-generated frame against the guide's correct example.

## Success Criteria

- [ ] Gravity uses Odd Rule spacing (1:3:5:7), not linear
- [ ] Volume is conserved during squash/stretch (Scale_X * Scale_Y ~ 1.0)
- [ ] No twinning: left/right limbs offset in pose and timing
- [ ] Smears last exactly 1 frame (never held longer)
- [ ] Key poses held minimum 3 frames (6+ for narrative beats)
- [ ] Style profile parameters match the target era
- [ ] TV mode: active pixels under 20% of screen area
- [ ] Eyes lead head turns by 2-3 frames
- [ ] Arcs follow Fourth Down Rule (breakdown at 25% from apex at 50% time)

## Copy/Paste Ready

```
"Is the timing right for the F06→F10 transition?"
"What in-between strategy for the head snap at F10?"
"Review the expression arc across Act 1 keyframes"
"What smear type for the arm sweep at F18?"
"How many hold frames should F18 have?"
"Why does this frame sequence feel floaty?"
"Plan timing for a surprise reaction"
"Adapt this to Spider-Verse style"
```
