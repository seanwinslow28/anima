# Act 1 — Keyframe Generation Prompts
## Structured with the 7-Layer Prompt Framework

> **Prompt architecture:** Each prompt below follows the [image-generator-prompt-science](../.claude/skills/image-generator-prompt-science/SKILL.md) 7-Layer Framework and incorporates the Pencil Animation Style Cluster from [pencil-animation-prompt-templates.md](../.claude/skills/gemini-pencil-animation-image-gen/references/pencil-animation-prompt-templates.md).

**How to run:** For EVERY prompt below, upload the A-2 character sketch (`images/2D-Character-Sketch-Sean-v1.png`) as the style/character reference via `--reference`. This is your consistency anchor.

**Why individual poses instead of a sheet:** Generating each pose as its own image gives Gemini full attention budget per frame. Multi-pose sheets tend to drift on likeness and style by the 3rd-4th panel. Composite individually onto the P-32A background later.

**Pipeline command:**
```bash
python3 pipeline/generate.py --manifest manifest.yaml --frame F06 --run-dir runs/{run_id}
```
Or directly:
```bash
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/F06.txt)" \
  --output runs/{run_id}/candidates/F06/attempt_01.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env
```

**Prompt files:** Individual prompt `.txt` files are in `prompts/F{##}.txt` for pipeline automation. The full prompts are also reproduced below for reference.

**Naming convention:** Approved outputs save as `PT_A1_F{##}_key.png` in the run's `approved/` directory.

---

## 7-Layer Structure Applied to Every Prompt

Each prompt below embeds all 7 layers from the framework:

| Layer | What it covers in these prompts |
|-------|-------------------------------|
| 1. Task Declaration | "Create a single full-body character drawing... frame A-# in a pencil test animation sequence" |
| 2. Context Foundation | Warm cream animation paper (#FAF5E8), grain texture, hole-punch marks, production label, character at 60-70% canvas height |
| 3. Style Definition | Pencil Animation Style Cluster — warm gray graphite lines (NOT black), 2-3px contour / 1px detail, construction lines, cross-hatching, Disney/Pixar pre-production proportions |
| 4. Compositional Layout | Single centered full-body figure, specific pose description with quantified angles and positions |
| 5. Consistency Constraints | "Same hair shape, same jaw angle, same eye spacing, same nose, same body proportions, same clothing" — repeated per prompt |
| 6. Technical Uniformity | Soft even lighting, cross-hatching shadows, flat uniform color fills, consistent lighting angle |
| 7. Output Specs + Negatives | 10 explicit negatives: no vector lines, no black outlines, no cel shading, no anime, no saturation, no digital painting, no gradients, no airbrush, no pure white BG, no pure black lines |

### Key Techniques Applied

- **Quantified parameters over adjectives:** "15 degrees," "2-3px equivalent," "#FAF5E8," "60-70% of vertical canvas"
- **Narrative structure over keywords:** Full sentences describing pose and emotion, not comma-separated tags
- **Known reference anchoring:** "Disney/Pixar pre-production adjacent," "Milt Kahl subtlety, not Tex Avery exaggeration"
- **Repetition for emphasis:** "consistent" appears 3-4 times per prompt; identity constraints repeated each time
- **Explicit negatives in plain English:** 10 "No..." statements at the end of every prompt

---

## F1 — Idle Hold (ALREADY DONE)

This is your A-2 image. No generation needed. Copy to `approved/PT_A1_F01_key.png` and `approved/PT_A1_F40_key.png`.

---

## F6 — Glance Down

**Upload with prompt:** `images/2D-Character-Sketch-Sean-v1.png`
**Prompt file:** `prompts/F06.txt`
**Generation chain:** Chain 1, position 1 (no previous frame dependency)

```
Using the uploaded character sketch as the EXACT style and character reference,
create a single full-body character drawing of this same person in a new pose.
This is frame A-3 in a pencil test animation sequence — a contemplative beat
between idle and action.

Present as a single character study on a sheet of warm cream animation paper
(#FAF5E8 approximate). The paper has visible grain texture, subtle aging marks
and dust specks, three hole-punch marks centered at the bottom edge, and a
hand-written production label "A-3" circled in pencil in the top-left corner.
The character occupies roughly 60-70% of the vertical canvas height, centered
on the page with space above and below.

Match the uploaded reference EXACTLY in style: traditional animation pencil test
drawing with hand-drawn graphite pencil lines. Lines are warm gray (NOT black
ink, NOT solid black outlines) with natural stroke-weight variation — thicker
contour outlines at 2-3px equivalent, thinner interior details at 1px
equivalent. Visible construction line artifacts beneath the final drawing —
faint vertical center line through face and torso, horizontal eye-line, rough
oval head shape, gesture line through spine. Subtle cross-hatching and
directional pencil strokes for shading on clothing folds, under chin, and
shadow areas. Line confidence suggests a professional animator's hand — fluid,
gestural strokes, not stiff or mechanical.

Color is extremely limited and desaturated: dark navy flat fill on the
crew-neck t-shirt, cool gray flat fill on slim jeans with cuffed ankles, warm
skin tones, muted sandy blonde hair. Pencil lines remain visible through and
on top of color fills. No color gradients.

Character proportions are slightly stylized — Disney/Pixar pre-production
adjacent, roughly 7-7.5 heads tall with a slightly larger head than
photorealistic. Appealing, warm character design language. NOT anime, NOT
hyper-realistic, NOT exaggerated cartoon.

POSE CHANGE FROM REFERENCE: The character's head tilts downward approximately
15 degrees, with his eyes looking down at the stylus pen in his right hand.
His chin drops slightly toward his chest. His right shoulder dips about 1 inch
lower than the left, as if the weight of thought is pulling that side down.
The rest of the body remains in the same relaxed standing position as the
reference — same weight distribution, same left hand position, same leg
stance, same sneakers.

EXPRESSION: Contemplative. The half-smile from the reference softens to a
neutral, thoughtful expression. Mouth closed. Brow relaxes — not furrowed,
just calm focus. He is looking at his tool and considering what to make next.

Maintain perfect identity consistency with the uploaded reference. The character
must be immediately recognizable as the same person: same hair shape and
volume, same jaw angle, same eye spacing, same nose shape, same body
proportions, same clothing. Only the head angle and expression change.

Lighting is soft and even — no dramatic directional light. Shadows are achieved
through cross-hatching and pencil density, not through color. The limited color
fills are flat and uniform within each region. Same lighting angle and
intensity as the reference.

Output a warm, analog-feeling animation production drawing. The image should
look like a high-resolution scan of the next page in the same animator's
pencil test sequence — same artist, same pencil, same paper. No vector-clean
lines. No solid black outlines. No cel shading. No anime style. No heavy
color saturation. No digital painting look. No gradient shading. No airbrush
effects. No pure white background. No pure black lines.
```

---

## F10 — The Spark

**Upload with prompt:** `images/2D-Character-Sketch-Sean-v1.png` + approved F06 output
**Prompt file:** `prompts/F10.txt`
**Generation chain:** Chain 1, position 2 (depends on F06 approved)

```
Using the uploaded character sketches as style and character references, create
a single full-body character drawing of this same person in a new pose. This
is frame A-4 in a pencil test animation sequence — the moment of creative
inspiration, the "idea take."

Present as a single character study on a sheet of warm cream animation paper
(#FAF5E8 approximate). The paper has visible grain texture, subtle aging marks
and dust specks, three hole-punch marks centered at the bottom edge, and a
hand-written production label "A-4" circled in pencil in the top-left corner.
The character occupies roughly 60-70% of the vertical canvas height, centered
on the page.

Match the uploaded references EXACTLY in style: traditional animation pencil
test drawing with hand-drawn graphite pencil lines. Lines are warm gray (NOT
black ink) with natural stroke-weight variation — thicker contour outlines at
2-3px equivalent, thinner interior details at 1px equivalent. Visible
construction line artifacts beneath the final drawing — faint center lines,
head oval, gesture line through spine, rough circles at joint positions
(shoulders, elbows). Subtle cross-hatching for shading on clothing folds,
under chin, and shadow areas. The line quality on this frame should be slightly
more energetic than the reference — more confident strokes, slightly more
dynamic line weight variation — to sell the energy of the moment.

Color is extremely limited and desaturated: dark navy flat fill on the
crew-neck t-shirt, cool gray flat fill on slim jeans with cuffed ankles, warm
skin tones, muted sandy blonde hair. Pencil lines visible through color fills.
No color gradients.

Character proportions are slightly stylized — Disney/Pixar pre-production
adjacent, roughly 7-7.5 heads tall. Appealing, warm character design. NOT
anime, NOT hyper-realistic, NOT exaggerated cartoon.

POSE: The character's head has snapped upward from a previous downward glance.
His head is now tilted slightly back, about 10 degrees above neutral, as if an
idea just struck him. His chin lifts. His right hand holding the stylus has
risen about 6 inches from its resting position — the elbow bends and the
forearm comes up in a reflexive gesture of readiness. The left shoulder rises
just barely — the body language of someone about to act on an impulse. Feet
remain planted in the same position as the reference.

EXPRESSION: This is a key frame. Both eyebrows lift noticeably — not
cartoonishly high, but clearly raised with genuine surprise and excitement.
Eyes widen slightly and brighten with energy. The mouth shifts from closed to
an open half-smile showing just a hint of teeth — a genuine spark of creative
excitement. This is the classic animator's "idea take" — Milt Kahl subtlety,
not Tex Avery exaggeration.

SECONDARY MOTION: The hair on top has a slight upward bounce from the quick
head movement — a few strands lift higher than in the reference, showing the
snap of head motion.

Maintain perfect identity consistency with the uploaded references. The
character must be immediately recognizable as the same person across both
reference images: same hair shape, same jaw angle, same eye spacing, same
nose, same body proportions, same clothing. Consistent head size, consistent
arm length, consistent shoulder width.

Lighting is soft and even — no dramatic directional light. Shadows achieved
through cross-hatching and pencil density. Same lighting angle and intensity
as the references. Color fills are flat and uniform within each region.

Output a warm, analog-feeling animation production drawing that looks like the
next page in the same animator's pencil test sequence. No vector-clean lines.
No solid black outlines. No cel shading. No anime style. No heavy color
saturation. No digital painting look. No gradient shading. No airbrush
effects. No pure white background. No pure black lines.
```

---

## F13 — The Ready (A-5)

> **Revised from storyboard.** Originally "Wind Up" — a coiled anticipation pose with the right arm raised. Changed to maintain stylus-hand continuity with F18's right-arm sweep. See [CHANGELOG.md](../CHANGELOG.md) for details.

**Upload with prompt:** `images/2D-Character-Sketch-Sean-v1.png` + approved F10 output
**Prompt file:** `prompts/F13.txt`
**Generation chain:** Chain 1, position 3 (depends on F10 approved)

**Approved pose (run_2026-04-04_174805):** The character stands with weight shifted, left arm extended forward with a thumbs-up gesture — a confident "ready to go" beat. The stylus is held in the RIGHT hand, lowered at his side. Expression is focused and determined, looking toward his extended left hand. This sets up F18 where the right arm sweeps forward with the stylus in a drawing gesture.

**Continuity note:** The thumbs-up with the left hand while the right hand holds the stylus at rest creates a natural wind-up: the left arm retracts as the right arm sweeps forward in F18. This is the creative adaptation — the "ready" beat replaces the original "coil" beat.

```
[F13 prompt was manually iterated by Sean — the approved frame was generated
outside the automated pipeline. The pose described above is the source of truth.
For future regeneration, reference the approved PT_A1_F13_key.png directly
as the style/pose target alongside A-2.]
```

---

## F18 — Mid-Gesture (The Draw)

**Upload with prompt:** `images/2D-Character-Sketch-Sean-v1.png` + approved F13 output
**Prompt file:** `prompts/F18.txt`
**Generation chain:** Chain 1, position 4 (depends on F13 approved)

```
Using the uploaded character sketches as style and character references, create
a single full-body character drawing of this same person in a new dynamic
pose. This is frame A-6 in a pencil test animation sequence — the peak of a
sweeping drawing gesture, the moment of maximum motion and creative energy.

Present as a single character study on a sheet of warm cream animation paper
(#FAF5E8 approximate). The paper has visible grain texture, subtle aging marks
and dust specks, three hole-punch marks centered at the bottom edge, and a
hand-written production label "A-6" circled in pencil in the top-left corner.
The character occupies roughly 60-70% of the vertical canvas height, centered
on the page.

Match the uploaded references EXACTLY in style: traditional animation pencil
test drawing with hand-drawn graphite pencil lines. Lines are warm gray (NOT
black ink) with natural stroke-weight variation — thicker contour outlines at
2-3px equivalent, thinner interior details at 1px equivalent. Visible
construction line artifacts beneath the final drawing — faint center lines,
gesture line through the spine showing torso rotation, rough circles at
joints. Cross-hatching for shading on clothing folds and shadow areas. The
line quality on this frame should feel the most energetic and confident of the
entire sequence — bold strokes with strong variation from thin to thick. This
is the peak action frame.

Color is extremely limited and desaturated: dark navy flat fill on the
crew-neck t-shirt, cool gray flat fill on slim jeans with cuffed ankles, warm
skin tones, muted sandy blonde hair. Pencil lines visible through color fills.
No color gradients.

Character proportions are slightly stylized — Disney/Pixar pre-production
adjacent, roughly 7-7.5 heads tall. NOT anime, NOT hyper-realistic, NOT
exaggerated cartoon.

POSE — PEAK ACTION: The character has swept his right arm in a confident arc
from left to right. The right arm is now fully extended to the right side of
his body, nearly straight, with the stylus pen at the end of the sweeping
motion. The stylus tip is at roughly chest height, extended to the right. His
torso has rotated slightly to follow the arm — right shoulder forward, left
shoulder back, creating a natural twist. Weight is on the front (left) foot
with the back foot almost on its toes. The left arm has swung back behind him
for counterbalance — a natural opposite motion to the right arm sweep. The
body shows a clear line of action from the trailing left hand through the
torso to the extended right hand with the stylus. This is the most dynamic
pose in the sequence — maximum motion energy.

EXPRESSION: Joy in motion. A genuine wide smile — not forced, the natural
expression of someone in creative flow. Eyes follow the stylus tip to the
right. Hair is swept slightly from the motion — strands displaced by the
sweeping gesture.

PENCIL TRAIL DETAIL: Behind the stylus tip, draw 4-5 loose, energetic pencil
sketch lines trailing in an arc from upper-left to the stylus position. These
trailing lines are rough, overlapping, gestural — the visible trace of the
stylus movement through the air. They look like real pencil marks on the
animation paper, slightly lighter and looser than the character's own
linework. The lines arc and swirl (not straight) — they show the path of a
creative gesture.

Maintain perfect identity consistency with the uploaded references. The
character must be immediately recognizable as the same person: same hair
shape, same jaw angle, same eye spacing, same nose, same body proportions.
Consistent head size relative to body. Same clothing — identical dark navy
crew-neck t-shirt, same slim jeans, same sneakers.

Lighting is soft and even — no dramatic directional light. Shadows achieved
through cross-hatching and pencil density. Same lighting angle and intensity
as the references. Color fills flat and uniform.

Output a warm, analog-feeling animation production drawing that captures peak
creative energy. The image should look like a high-resolution scan of the most
dynamic page in the animator's pencil test sequence. No vector-clean lines. No
solid black outlines. No cel shading. No anime style. No heavy color
saturation. No digital painting look. No gradient shading. No airbrush
effects. No pure white background. No pure black lines.
```

---

## F31 — Sprite Lands on Shoulder

**Upload with prompt:** `images/2D-Character-Sketch-Sean-v1.png`
**Prompt file:** `prompts/F31.txt`
**Generation chain:** Chain 2, position 1 (no previous frame dependency — fresh anchor)

```
Using the uploaded character sketch as the EXACT style and character reference,
create a single full-body character drawing of this same person in a new pose.
This is frame A-7 in a pencil test animation sequence — a moment of quiet
satisfaction after creating something.

Present as a single character study on a sheet of warm cream animation paper
(#FAF5E8 approximate). The paper has visible grain texture, subtle aging marks
and dust specks, three hole-punch marks centered at the bottom edge, and a
hand-written production label "A-7" circled in pencil in the top-left corner.
The character occupies roughly 60-70% of the vertical canvas height, centered
on the page.

Match the uploaded reference EXACTLY in style: traditional animation pencil
test drawing with hand-drawn graphite pencil lines. Lines are warm gray (NOT
black ink) with natural stroke-weight variation — thicker contour outlines at
2-3px equivalent, thinner interior details at 1px equivalent. Visible
construction line artifacts beneath the final drawing — faint center lines,
head oval, gesture line through spine. Cross-hatching for shading on clothing
folds, under chin, and shadow areas. The energy of the linework should feel
settled and calm compared to the dynamic poses earlier in the sequence — this
is a moment of stillness.

Color is extremely limited and desaturated: dark navy flat fill on the
crew-neck t-shirt, cool gray flat fill on slim jeans with cuffed ankles, warm
skin tones, muted sandy blonde hair. Pencil lines visible through color fills.
No color gradients.

Character proportions are slightly stylized — Disney/Pixar pre-production
adjacent, roughly 7-7.5 heads tall. NOT anime, NOT hyper-realistic, NOT
exaggerated cartoon.

POSE: The character's body has returned to a relaxed standing position similar
to the reference, but with key differences. His head is turned to the LEFT,
looking at his own left shoulder. His right arm has lowered back to a natural
resting position, the stylus held loosely at his side. His left shoulder is
raised VERY slightly — about a quarter inch higher than normal — because there
is something small resting on it (a tiny sprite character, which will be
composited separately — DO NOT draw the sprite, DO NOT draw anything on the
shoulder). Weight is evenly distributed, settled and relaxed after the
energetic gesture.

EXPRESSION: Looking to his left at his own shoulder with a warm, quiet smirk —
the satisfaction of a craftsman looking at something he just created. Not a big
smile — understated, genuine pride. One eyebrow raised just slightly, as if
pleasantly surprised by what appeared.

Maintain perfect identity consistency with the uploaded reference. The
character must be immediately recognizable as the same person: same hair shape
and volume, same jaw angle, same eye spacing, same nose, same body
proportions. Consistent head size relative to body. Same clothing — identical
dark navy crew-neck t-shirt, same slim jeans, same sneakers.

Lighting is soft and even — no dramatic directional light. Shadows achieved
through cross-hatching and pencil density. Same lighting angle and intensity
as the reference. Color fills flat and uniform.

Output a warm, analog-feeling animation production drawing that captures quiet
creative satisfaction. The image should look like a high-resolution scan of
the same animator's pencil test sequence. No vector-clean lines. No solid
black outlines. No cel shading. No anime style. No heavy color saturation. No
digital painting look. No gradient shading. No airbrush effects. No pure
white background. No pure black lines.
```

---

## F36 — The Nod

**Upload with prompt:** `images/2D-Character-Sketch-Sean-v1.png` + approved F31 output
**Prompt file:** `prompts/F36.txt`
**Generation chain:** Chain 2, position 2 (depends on F31 approved)

```
Using the uploaded character sketches as style and character references, create
a single full-body character drawing of this same person in a new pose. This
is frame A-8 in a pencil test animation sequence — the emotional payoff of
the entire animation, a small definitive nod of satisfaction.

Present as a single character study on a sheet of warm cream animation paper
(#FAF5E8 approximate). The paper has visible grain texture, subtle aging marks
and dust specks, three hole-punch marks centered at the bottom edge, and a
hand-written production label "A-8" circled in pencil in the top-left corner.
The character occupies roughly 60-70% of the vertical canvas height, centered
on the page.

Match the uploaded references EXACTLY in style: traditional animation pencil
test drawing with hand-drawn graphite pencil lines. Lines are warm gray (NOT
black ink) with natural stroke-weight variation — thicker contour outlines at
2-3px equivalent, thinner interior details at 1px equivalent. Visible
construction line artifacts beneath the final drawing — faint center lines,
head oval, gesture line through spine. Cross-hatching for shading on clothing
folds, under chin, and shadow areas.

Color is extremely limited and desaturated: dark navy flat fill on the
crew-neck t-shirt, cool gray flat fill on slim jeans with cuffed ankles, warm
skin tones, muted sandy blonde hair. Pencil lines visible through color fills.
No color gradients.

Character proportions are slightly stylized — Disney/Pixar pre-production
adjacent, roughly 7-7.5 heads tall. NOT anime, NOT hyper-realistic, NOT
exaggerated cartoon.

POSE: Nearly identical to the previous shoulder-glance pose (A-7), with ONE
key change: the character's chin has dropped in a single definitive downward
nod. The head is still turned to the left (looking toward his shoulder), but
the chin has dipped 15-20 degrees below its previous position. The eyes close
partially — not fully shut, but a relaxed half-close that accompanies a
genuine nod. The rest of the body is completely still — same relaxed stance,
same lowered right arm with stylus held loosely at side, same slightly raised
left shoulder.

EXPRESSION — THE SIGNATURE GESTURE: A single, small, definitive nod that says
"yeah, that's good." Not enthusiastic — calm and confident. The kind of nod a
craftsman gives when a piece comes out right. Mouth in a closed, content
smile. The overall energy is quiet pride. In traditional animation, the nod is
one of the most character-defining gestures — this nod should feel like it
belongs to this specific character. The slight lean of the head, the degree of
the chin drop, the eye closure — these are personality.

Maintain perfect identity consistency with the uploaded references. The
character must be immediately recognizable as the same person: same hair shape
and volume, same jaw angle, same eye spacing, same nose, same body
proportions. Consistent head size relative to body. Same clothing — identical
dark navy crew-neck t-shirt, same slim jeans, same sneakers.

Lighting is soft and even — no dramatic directional light. Shadows achieved
through cross-hatching and pencil density. Same lighting angle and intensity
as the references. Color fills flat and uniform.

Output a warm, analog-feeling animation production drawing that captures the
emotional payoff of the sequence. The image should look like a high-resolution
scan of the same animator's pencil test. No vector-clean lines. No solid
black outlines. No cel shading. No anime style. No heavy color saturation. No
digital painting look. No gradient shading. No airbrush effects. No pure
white background. No pure black lines.
```

---

## F40 — Return to Idle (NO GENERATION NEEDED)

F40 must match F1 exactly for the seamless loop. Use the A-2 anchor image directly:
```bash
cp images/2D-Character-Sketch-Sean-v1.png runs/{run_id}/approved/PT_A1_F40_key.png
```
The pipeline's `generate.py` handles this automatically when initializing a run.

---

## Post-Generation Checklist

After generating all 6 keyframes, review the full set together:

- [ ] **Style consistency:** Do all frames look like the same artist drew them? Same line weight range (2-3px contour, 1px detail), same warm gray tone (not black), same paper color (#FAF5E8), same level of detail?
- [ ] **Character consistency:** Does Sean look like the same person across all poses? Check: hair shape/volume, jaw angle, eye spacing, nose shape, body proportions.
- [ ] **Pose readability:** Flip through the images quickly (like flipping animation pages). Does the motion read? Can you feel the arc from idle → spark → gesture → satisfaction → nod → idle?
- [ ] **Expression arc:** F1 (neutral) → F6 (contemplative) → F10 (excited) → F18 (joyful flow) → F31 (quiet pride) → F36 (the nod) → F40 (settled). Does the emotional journey track?
- [ ] **Proportions:** Is the character the same height/width across all frames? Check head size relative to body, arm length, leg stance width.
- [ ] **Paper elements:** Do all frames have: cream background with grain, three hole-punch marks at bottom, production label (A-#) in top-left?
- [ ] **Construction lines:** Are construction line artifacts visible beneath the final drawing in every frame?

**If any frame drifts:** Feed it back as a reference alongside A-2 with a specific correction prompt. Fix one thing at a time — "the jaw needs to be more angular" or "the hair has too much volume on the left side." Don't try to fix multiple issues in one pass. See the [refinement tips](../.claude/skills/gemini-pencil-animation-image-gen/references/pencil-animation-prompt-templates.md#prompt-refinement-tips) for common fixes.

---

## Frame Summary

| Frame | Label | Pose | Chain | References | Key Change |
|-------|-------|------|-------|------------|------------|
| F1 | A-2 | Idle hold | — | (anchor image) | Starting pose — already exists |
| F6 | A-3 | Glance down | 1.1 | anchor | Head tilts down 15°, eyes on stylus |
| F10 | A-4 | The spark | 1.2 | anchor + F06 | Head snaps up, eyebrows lift, mouth opens |
| F13 | A-5 | The ready | 1.3 | anchor + F10 | Left arm thumbs-up, stylus in right hand at side **(revised)** |
| F18 | A-6 | Mid-gesture | 1.4 | anchor + F13 | Right arm sweeps forward with stylus, pencil trail |
| F31 | A-7 | Sprite lands | 2.1 | anchor | Head turns left, looking at shoulder |
| F36 | A-8 | The nod | 2.2 | anchor + F31 | Chin drops 15-20°, eyes half-close |
| F40 | A-9 | Return to idle | — | (anchor image) | Matches F1 for seamless loop |

**Total new generations needed:** 6 poses (F6, F10, F13, F18, F31, F36)
**Already done:** F1/F40 (A-2 image)
**Note:** F24 and F28 (sprite transformation and bounce) are compositing frames — Sean's body pose holds steady from F18, and the sprite animation is a separate production layer.
