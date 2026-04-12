# Pencil Animation Prompt Templates

> **When to read:** Always read this file when generating pencil animation-style artwork. Contains ready-to-use prompt templates structured with the 7-Layer Prompt Framework from the `image-generator-prompt-science` skill. Every template reproduces the specific aesthetic of traditional animation pencil test / production drawings.

---

## Pencil Animation Style Cluster (Include in Every Prompt)

Copy this style block into every prompt, or reference it by name. This is the visual DNA of the target aesthetic, derived from the reference image.

```
STYLE CLUSTER — PENCIL ANIMATION:

Style: Traditional animation pencil test drawing. Hand-drawn graphite pencil lines
on warm cream animation paper. Lines are warm gray (NOT black) with natural
stroke-weight variation — thicker on contour outlines (~2-3px equivalent),
thinner on interior details (~1px equivalent). Visible construction line
artifacts beneath the final drawing. Subtle cross-hatching and directional
pencil strokes for shading on clothing folds, under chin, and shadow areas.
Line confidence suggests a professional animator's hand — fluid, gestural
strokes, not stiff or mechanical.

Color: Extremely limited, desaturated flat color fills layered OVER the pencil
drawing. Pencil lines remain visible through and on top of color. Colors are
muted and natural — no saturated or vibrant tones. Think marker or digital
flat-color over a pencil sketch. Example palette: dark navy (shirt), cool
gray (jeans), warm skin tones, muted sandy blonde (hair).

Paper: Warm cream/off-white background (#FAF5E8 approximate) with visible paper
grain texture. Subtle aging/wear marks — slight scuffs, dust specks. Three
hole-punch marks at the bottom edge (authentic animation paper detail). A
hand-written production label in the top-left corner in a circle (e.g.,
"A-[NUMBER]") — standard animation sheet numbering convention.

Character proportions: Slightly stylized (Disney/Pixar pre-production adjacent).
Head slightly larger than realistic, expressive features, appealing proportions.
Warm, approachable character design language. Clean silhouette readability —
identity clear from outline alone. NOT hyper-realistic, NOT anime, NOT
exaggerated cartoon.

Overall feel: "Animation pre-production character design sketch" — like a page
from a Disney animator's sketchbook or a "making of" art book. The aesthetic
communicates "this is a drawing by a skilled human animator," not
"this is a computer-generated image." Warm, crafted, analog quality.

NEGATIVES: No vector-clean lines. No solid black outlines. No cel shading. No
anime style. No heavy color saturation. No digital painting look. No gradient
shading. No airbrush effects. No pure white background. No pure black lines.
Must look hand-drawn by a professional animator, not computer-generated.
```

---

## Template 1: Character Design from Reference Photo

**Use when:** Generating a pencil animation-style character based on a real person's photo. The script's `--reference` flag should be used to pass the photo for identity locking.

**Recommended aspect ratio:** `3:4` or `4:5`

```
[TASK DECLARATION]
Create a full-body character design drawing of the person in the reference photo,
rendered as a traditional animation pencil test sketch on animation paper.

[CONTEXT FOUNDATION]
Present this as a single character study on a sheet of warm cream animation paper.
The paper has visible grain texture, subtle aging marks, three hole-punch marks at
the bottom edge, and a hand-written production label circled in the top-left corner
(e.g., "A-1"). The character stands in a relaxed, natural pose — slightly angled
3/4 view to show personality.

[STYLE DEFINITION — include full Style Cluster above, then add:]
Capture the key distinguishing features of the person in the reference photo and
translate them into slightly stylized animation proportions:
- Hair: [COLOR, STYLE, LENGTH — describe from photo]
- Build: [GENERAL body type — describe from photo]
- Clothing: [DESCRIBE what they're wearing, or assign an outfit]
- Defining features: [GLASSES, BEARD, FRECKLES, etc. — 2-3 signature traits]

The character should be immediately recognizable as this person to someone who
knows them, while feeling like a professional animator's interpretation — slightly
idealized, appealing proportions, expressive.

[COMPOSITIONAL LAYOUT]
Single full-body figure, centered on the page. Character occupies roughly 60-70%
of the vertical canvas height. Feet visible, some space above the head. Slight
negative space around the figure — this is a character study, not a tight crop.

[CONSISTENCY CONSTRAINTS]
Maintain consistent pencil weight throughout the drawing. Contour outlines are
the heaviest strokes. Interior detail lines (clothing seams, hair strands, facial
features) are lighter. Construction lines visible beneath the final drawing should
be faintest. The character's proportions should feel balanced and structurally sound.

[TECHNICAL UNIFORMITY]
Lighting is soft and even — no dramatic directional light. Shadows are achieved
through cross-hatching and pencil density, not through color. The limited color
fills are flat and uniform within each region (shirt is one flat navy tone, jeans
are one flat gray tone). No color gradients.

[OUTPUT SPECS + NEGATIVES]
Output a warm, analog-feeling character design sketch. The image should look like
a high-resolution scan of an animator's pencil drawing on real paper.
No vector-clean lines. No solid black outlines. No cel shading. No anime style.
No heavy color saturation. No digital painting look. No gradient shading.
No pure white background. No pure black lines.
```

---

## Template 2: Expression Sheet

**Use when:** Creating a single sheet with 6-9 facial expressions of the same character, useful for establishing a character's emotional range.

**Recommended aspect ratio:** `1:1` or `4:3`

```
[TASK DECLARATION]
Create an expression sheet showing 9 different facial expressions of the same
character, rendered as traditional animation pencil test sketches on a single
sheet of animation paper.

[CONTEXT FOUNDATION]
Present as a professional character expression study — the kind of reference sheet
an animation studio creates during pre-production. Warm cream animation paper with
visible grain texture, three hole-punch marks at the bottom edge, and a hand-written
production label circled in the top-left corner (e.g., "A-3 EXPRESSIONS").

[STYLE DEFINITION — include full Style Cluster, then add:]
Character identity: [DESCRIBE the character — hair, features, defining traits].
Each expression is a head-and-shoulders portrait (bust shot). The pencil work
should capture subtle muscle movement in the face — raised eyebrows, squinted
eyes, open mouth shapes. Expression acting should feel genuine and specific,
not generic emoji faces.

[COMPOSITIONAL LAYOUT]
Arrange the 9 expressions in a 3x3 grid with comfortable spacing between each
bust. Each bust is roughly the same size. Leave space for small handwritten
expression labels beneath each one (the kind an animator would jot down).

The expressions, in order (left to right, top to bottom):
1. Neutral / resting face — the character's default state
2. Happy / warm smile — genuine, eyes engaged
3. Thinking / contemplative — eyes looking up or to the side, slight frown
4. Surprised — eyebrows raised, mouth open
5. Frustrated / annoyed — furrowed brow, tight lips
6. Determined / focused — narrowed eyes, set jaw
7. Laughing — open mouth, squinted eyes, head tilted
8. Skeptical / one eyebrow raised — asymmetric expression
9. Sad / concerned — downturned mouth, soft eyes

[CONSISTENCY CONSTRAINTS]
CRITICAL: The character must be immediately recognizable as the SAME PERSON in
all 9 expressions. Hair style, hair color, face shape, nose shape, ear position,
and neck proportions must remain identical across every bust. Only the facial
muscles and mouth shape change between expressions. Consistent head size across
all 9 panels.

[TECHNICAL UNIFORMITY]
Same pencil weight and paper texture across all 9 busts. Same level of color
application (limited, desaturated flat fills — skin tone and hair color only).
Same lighting angle on every expression. Pencil construction lines visible
beneath each expression at the same faint level.

[OUTPUT SPECS + NEGATIVES]
Output a cohesive expression study sheet that reads as one unified page of
animator reference art. No vector lines. No solid black outlines. No cel shading.
No anime style. No saturated colors. No digital painting effects.
```

---

## Template 3: Pose Study / Action Sheet

**Use when:** Generating multiple full-body poses of the same character on one sheet to establish body language and movement vocabulary.

**Recommended aspect ratio:** `16:9` or `3:2`

```
[TASK DECLARATION]
Create a pose study sheet showing 5-6 different full-body poses of the same
character, rendered as traditional animation pencil test sketches on a single
sheet of animation paper.

[CONTEXT FOUNDATION]
Present as a character action/pose reference — the kind animators use to
understand how a character moves and carries themselves. Warm cream animation
paper with visible grain, three hole-punch marks at the bottom edge, and a
hand-written production label circled in the top-left corner (e.g., "A-4 POSES").

[STYLE DEFINITION — include full Style Cluster, then add:]
Character identity: [DESCRIBE the character — hair, build, clothing, defining traits].
Each pose should show the full body from head to feet. The poses should feel
natural and character-specific — they reveal personality through body language.
Lines should be loose and gestural with visible energy, not stiff posed mannequins.

[COMPOSITIONAL LAYOUT]
Arrange 5-6 full-body poses in a horizontal lineup across the sheet. Characters
share the same ground line. Vary the spacing slightly — some poses are wider
(arms outstretched), some narrower (standing with arms crossed). Leave room
for small handwritten pose labels beneath each figure.

The poses, left to right:
1. Relaxed standing — weight on one leg, casual posture, hands in pockets or at sides
2. Walking — mid-stride, natural gait, arms swinging
3. Sitting — on a chair or stool, leaning forward slightly, engaged
4. Typing / working at a desk — seated, hands on keyboard, focused posture
5. Leaning — against a wall or doorframe, arms crossed, casual
6. Pointing or gesturing — one arm extended, explaining something, expressive hand

[CONSISTENCY CONSTRAINTS]
The character must be the SAME PERSON in every pose. Identical clothing, hair,
build, and proportions. Head height should be consistent across standing poses.
Clothing wrinkles and folds should respond naturally to each pose but the outfit
itself stays the same. The character's personality should come through in every
pose — they all feel like the same individual.

[TECHNICAL UNIFORMITY]
Consistent pencil weight across all poses. Cross-hatching density should be
similar. Color application (limited flat fills) is uniform. Paper texture is
consistent. Some poses may show more construction lines than others (the more
dynamic the pose, the more visible the underlying structure).

[OUTPUT SPECS + NEGATIVES]
Output a dynamic, appealing pose study that demonstrates the character's range
of movement and personality. No vector lines. No solid black outlines. No cel
shading. No anime style. No saturated colors. No digital effects.
```

---

## Template 4: Turnaround Sheet

**Use when:** Creating front, 3/4, side profile, 3/4 back, and back views of a character in a horizontal lineup for consistency reference.

**Recommended aspect ratio:** `16:9` or `21:9`

```
[TASK DECLARATION]
Create a character turnaround sheet showing 5 views of the same character in a
horizontal lineup, rendered as traditional animation pencil test sketches on
animation paper.

[CONTEXT FOUNDATION]
Present as a professional character turnaround — the essential reference sheet
animators use to draw a character consistently from any angle. Warm cream
animation paper with visible grain, three hole-punch marks at the bottom edge,
and a hand-written production label circled in the top-left corner
(e.g., "A-5 TURNAROUND"). Include faint horizontal guide lines across the sheet
marking the character's head height, shoulder line, waist, and feet — the
standard turnaround alignment guides.

[STYLE DEFINITION — include full Style Cluster, then add:]
Character identity: [DESCRIBE the character — hair, build, clothing, defining traits].
Each view shows the full body in a neutral standing pose (arms slightly away
from the body so the silhouette is clear). The character's weight is evenly
distributed. This is a technical reference — poses are neutral and consistent,
not dynamic or expressive.

[COMPOSITIONAL LAYOUT]
Arrange 5 full-body views in a horizontal row, evenly spaced, all standing on
the same ground line. Faint horizontal guide lines run across all 5 views at
key anatomical landmarks (top of head, chin, shoulders, waist, knees, feet).

The views, left to right:
1. Front view — facing the viewer directly
2. 3/4 front view — turned approximately 45 degrees to the viewer's right
3. Side profile — facing right, pure 90-degree profile
4. 3/4 back view — turned approximately 135 degrees
5. Back view — facing directly away from the viewer

[CONSISTENCY CONSTRAINTS]
CRITICAL: Proportions, height, and details must match EXACTLY across all 5 views.
The horizontal guide lines must align precisely — the top of the head is at the
same height in every view. Shoulder width, arm length, leg length, and torso
proportions are identical. Clothing details (seams, pockets, collar, shoes) must
be consistent and logically correct from each angle. Hair volume and style must
be recognizable from every direction.

[TECHNICAL UNIFORMITY]
Identical pencil weight across all 5 views. Same level of detail — no view should
be more or less finished than the others. Same cross-hatching density for shading.
Same flat color fills applied uniformly. Construction lines visible at the same
faint level beneath each view. The guide lines are the lightest marks on the sheet.

[OUTPUT SPECS + NEGATIVES]
Output a clean, professional turnaround reference that an animator could use to
draw this character from any angle. No vector lines. No solid black outlines.
No cel shading. No anime style. No saturated colors. No digital painting effects.
No perspective distortion — all views are at the same neutral eye level.
```

---

## Template 5: Scene Composition Sketch

**Use when:** Creating a full scene with one or more characters in an environment, still in the pencil test style. More illustrative than the other templates.

**Recommended aspect ratio:** `16:9` or `3:2`

```
[TASK DECLARATION]
Create a scene composition sketch showing [DESCRIBE SCENE — e.g., "two characters
having coffee at a small cafe table" or "a character working alone at a desk in
a command center"], rendered as a traditional animation pencil test drawing on
animation paper.

[CONTEXT FOUNDATION]
Present as a scene layout / composition sketch — the kind an animation director
would draw to plan a shot before it goes to the animation team. Warm cream
animation paper with visible grain, three hole-punch marks at the bottom edge,
and a hand-written production label circled in the top-left corner
(e.g., "A-6 SC.12"). The environment is suggested with minimal line work —
enough to establish the space without overwhelming the characters.

[STYLE DEFINITION — include full Style Cluster, then add:]
Character(s): [DESCRIBE each character — identifying features, clothing, posture].
Environment: [DESCRIBE the setting briefly — "small coffee shop interior",
"industrial command center with multiple screens", "park bench under a tree"].

The characters are the focal point. The environment is sketched with looser,
lighter pencil work than the characters — architectural lines are thinner,
furniture is suggested rather than fully rendered. This creates a natural depth
hierarchy: characters are "finished," environment is "sketched in."

[COMPOSITIONAL LAYOUT]
[DESCRIBE the spatial arrangement]:
- Where are the characters positioned? (e.g., "Character A sits on the left side
  of the frame at a small round table. Character B stands to the right, leaning
  on the back of a chair.")
- What is the camera angle? (e.g., "Medium shot from roughly eye level, slight
  3/4 angle to show depth in the space.")
- What environmental elements frame the scene? (e.g., "A window on the left wall
  lets in ambient light. A counter and shelves are visible in the background,
  loosely sketched.")

[CONSISTENCY CONSTRAINTS]
If multiple characters appear, each maintains their established design identity.
Proportions are consistent between characters and with the environment (a table
should be table-height relative to the characters, a door should be door-height).
The pencil style is consistent across the entire drawing — characters don't look
like they were pasted into the environment.

[TECHNICAL UNIFORMITY]
Character pencil work is the densest and most detailed. Environmental elements
use progressively lighter, sketchier lines as they recede from the focal point.
Color is applied primarily to the characters — the environment may have little
to no color, or just a light wash to suggest tone. Cross-hatching is used
selectively for shadow areas that establish the scene's lighting.

[OUTPUT SPECS + NEGATIVES]
Output a warm, atmospheric scene sketch that feels like a page from an animation
production's storyboard or layout department. No vector lines. No solid black
outlines. No cel shading. No anime style. No saturated colors. No digital
painting effects. No fully rendered backgrounds — the environment should feel
sketched, not finished.
```

---

## Template 6: Character Comparison Lineup

**Use when:** Designing a cast of characters and needing to compare heights, proportions, and visual distinctness side-by-side.

**Recommended aspect ratio:** `16:9` or `21:9`

```
[TASK DECLARATION]
Create a character comparison lineup showing [NUMBER] different characters standing
side-by-side for height and proportion comparison, rendered as traditional
animation pencil test sketches on animation paper.

[CONTEXT FOUNDATION]
Present as a cast lineup / height comparison chart — the reference sheet animation
studios use to ensure characters are visually distinct and properly scaled relative
to each other. Warm cream animation paper with visible grain, three hole-punch
marks at the bottom edge, and a hand-written production label circled in the
top-left corner (e.g., "A-7 LINEUP"). Include a faint horizontal measurement
grid in the background marking height increments.

[STYLE DEFINITION — include full Style Cluster, then add:]
Characters (left to right):
1. [NAME/LABEL]: [HEIGHT relative to others, BUILD, HAIR, CLOTHING, DEFINING FEATURES]
2. [NAME/LABEL]: [HEIGHT relative to others, BUILD, HAIR, CLOTHING, DEFINING FEATURES]
3. [NAME/LABEL]: [HEIGHT relative to others, BUILD, HAIR, CLOTHING, DEFINING FEATURES]
[... add more as needed]

Each character should have a clearly distinct silhouette — if you filled them all
in solid black, you could still tell them apart by outline alone. Vary body types,
heights, hair silhouettes, and posture to maximize visual contrast.

[COMPOSITIONAL LAYOUT]
All characters stand on the same ground line in a horizontal row, evenly spaced.
All face forward (front view) in a neutral standing pose. A faint measurement
grid behind them shows relative heights. Small handwritten name/label tags
beneath each character. Tallest characters should not be cropped — the canvas
must accommodate the full range.

[CONSISTENCY CONSTRAINTS]
All characters share the same art style, pencil weight, and level of finish.
The slight stylization (Disney/Pixar pre-production adjacent) must be consistent
across all characters — they should look like they belong in the same project.
Height differences must be proportional and clear (if Character A is meant to be
shorter, it should be visibly shorter, not ambiguously close).

[TECHNICAL UNIFORMITY]
Same pencil technique applied to every character. Same flat color application
(each character has their own limited palette, but the application method is
identical). Same cross-hatching density for shading. Same paper texture
throughout. The measurement grid is the lightest element on the sheet.

[OUTPUT SPECS + NEGATIVES]
Output a clean cast comparison that immediately communicates each character's
relative size and visual identity. No vector lines. No solid black outlines.
No cel shading. No anime style. No saturated colors. No digital effects.
```

---

## Prompt Refinement Tips

Common issues when generating pencil animation art with Gemini, and how to fix them:

### If the output looks too digital / clean
The most common failure mode. Reinforce the hand-drawn quality:
```
Add: "The lines must have natural irregularity — slight wobble, varying pressure,
occasional overlap where the pencil retraced a stroke. This should look like it
was drawn with a real graphite pencil on real paper by a human hand, not generated
by software. Include visible eraser marks and construction line ghosts beneath
the final drawing."
```

### If the lines are too black / heavy
Gemini defaults to high-contrast ink lines. Push toward warm gray graphite:
```
Add: "The pencil lines are WARM GRAY graphite, NOT black ink. Think HB to 2B pencil
on cream paper — the darkest strokes are a rich charcoal gray (#4A4A4A approximate),
never reaching true black. Lighter construction lines are barely visible
(#B0B0A8 approximate). The line color has a slight warm undertone."
```

### If the colors are too saturated
Gemini tends to over-saturate. Constrain explicitly:
```
Add: "Colors are EXTREMELY muted and desaturated. Imagine the color was applied
with dried-out markers — low opacity, no vibrancy. A 'red' shirt would be a dusty
terra cotta. A 'blue' shirt would be a washed-out navy. Saturation values should
be below 40%. The pencil drawing dominates; color is secondary and subtle."
```

### If the paper texture is missing
Without explicit instruction, Gemini generates a flat white background:
```
Add: "The background is warm cream animation paper (#FAF5E8) with VISIBLE paper
grain texture — you can see the tooth of the paper in the lighter areas. Include
three evenly-spaced hole-punch marks at the bottom edge of the paper (these are
the registration holes on standard animation paper). Add a hand-written production
label in a hand-drawn circle in the top-left corner showing a frame number
(e.g., 'A-2'). Include subtle dust specks and slight aging marks on the paper."
```

### If the character looks like anime / cartoon
Anchor to the correct style family:
```
Add: "The character design style is Disney/Pixar PRE-PRODUCTION adjacent — the
kind of sketch you'd find in a 'The Art of...' book. This is NOT anime (no giant
eyes, no pointed chins, no speed lines). This is NOT exaggerated cartoon (no
rubberhose limbs, no oversized heads). Proportions are roughly 7-7.5 heads tall
with a SLIGHTLY larger head than photorealistic. The style communicates 'appealing
realism' — recognizable as a real person but with the warmth and appeal of
animation character design."
```

### If construction lines are missing
Construction lines are key to the authentic pencil test look:
```
Add: "Show VISIBLE construction guide lines beneath the final drawing — the kind
an animator draws before committing to the final lines. These include: a faint
vertical center line through the face and torso, horizontal eye-line and mouth-line
on the face, rough oval for the head shape, gesture line through the spine, and
rough circles at the joints (shoulders, elbows, hips, knees). These construction
marks should be lighter than the final lines but clearly visible — they show the
animator's process."
```

### If the production label / hole-punches are missing
These details sell the animation paper authenticity:
```
Add: "In the top-left corner of the paper, draw a small hand-written alphanumeric
label inside a loosely drawn circle — e.g., 'A-2' or 'B-7'. This is the animation
production frame/sheet number, written by hand with the same pencil. At the
bottom edge of the paper, centered, show three evenly-spaced circular hole-punch
marks (the registration peg holes on animation paper). These details are essential
to the authentic animation production art feel."
```

---

## Generation Workflow for a Complete Character Package

Generate assets in this order for best results:

1. **Character design first (Template 1)** — Establish the character from a reference photo. Get the proportions, features, and style right before anything else. This is the foundation everything else references.

2. **Turnaround sheet (Template 4)** — Once the character design is approved, generate the turnaround to lock proportions from all angles. Reference the approved design in your prompt.

3. **Expression sheet (Template 2)** — With the face established from Template 1, generate the full range of expressions. Reference the approved character design.

4. **Pose study (Template 3)** — With proportions locked from the turnaround, generate action poses. Reference the approved turnaround.

5. **Scene compositions (Template 5)** — Place the established character(s) in environments. Reference approved character designs for consistency.

6. **Cast lineup (Template 6)** — Once multiple characters exist, create the comparison lineup to verify visual distinctness and relative scale.

### Post-Generation Checklist

- [ ] Paper is warm cream with visible grain (not flat white or gray)
- [ ] Lines are warm gray graphite, not black ink
- [ ] Construction line artifacts visible beneath final drawing
- [ ] Cross-hatching present in shadow areas
- [ ] Colors are limited, desaturated, flat — pencil lines visible through them
- [ ] Three hole-punch marks at bottom edge
- [ ] Production label (e.g., "A-1") in top-left corner
- [ ] Character proportions are slightly stylized (Disney/Pixar pre-production feel)
- [ ] Overall image feels like a scanned page from an animator's sketchbook
- [ ] No digital artifacts — no vector lines, no gradients, no airbrush effects
