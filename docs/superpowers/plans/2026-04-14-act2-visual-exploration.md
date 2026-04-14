# Act 2 Visual Exploration — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate concept art for all four Act 2 career zones, explore transition ideas, design the AI companion character, and produce the first Seedance 2.0 test clip — all in pencil test style using NB2.

**Architecture:** Four rounds of visual exploration, each building on the last. Round 1 establishes zone visual identity. Round 2 explores transitions. Round 3 designs the AI companion. Round 4 generates anchor keyframes and tests Seedance. Sean reviews after each round and directs refinement.

**Tech Stack:** Gemini Nano Banana 2 (image gen), Seedance 2.0 via fal.ai (motion), FFmpeg (extraction), A-2 anchor reference image.

**Spec:** `docs/superpowers/specs/2026-04-14-act2-creative-direction-design.md`

---

## Setup

### Task 0: Create Run Directory and Prompt Files

**Files:**
- Create: `runs/act2-exploration/concepts/zone1/`
- Create: `runs/act2-exploration/concepts/zone2/`
- Create: `runs/act2-exploration/concepts/zone3/`
- Create: `runs/act2-exploration/concepts/zone4/`
- Create: `runs/act2-exploration/concepts/transitions/`
- Create: `runs/act2-exploration/concepts/companion/`
- Create: `prompts/act2/` (all concept prompts)

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p runs/act2-exploration/concepts/{zone1,zone2,zone3,zone4,transitions,companion}
mkdir -p runs/act2-exploration/{candidates,approved,seedance,audit,export}
mkdir -p prompts/act2
```

- [ ] **Step 2: Verify A-2 anchor and generation script exist**

```bash
ls -la images/2D-Character-Sketch-Sean-v1.png
ls -la .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py
```

- [ ] **Step 3: Verify .env has GEMINI_API_KEY**

```bash
grep GEMINI_API_KEY .env
```

- [ ] **Step 4: Commit setup**

```bash
git add runs/act2-exploration/.gitkeep prompts/act2/
git commit -m "scaffold: Act 2 exploration directory structure"
```

---

## Round 1: Zone Establishing Shots

Goal: Generate 2-3 concept images per zone to lock visual identity. Each image shows Sean standing in or walking through the zone's world. All pencil test style, all on cream animation paper.

### Prompt Template — Zone Concepts

Every zone prompt uses this structure (adapted from the Act 1 7-Layer framework). The `[ZONE DESCRIPTION]` and `[SEAN'S POSE/ACTION]` blocks change per image. The style/paper/identity blocks stay constant.

```
Using the uploaded character sketch as the EXACT style and character reference, create a wide establishing shot of this same character in a pencil-drawn environment. This is a concept frame for Act 2 of a pencil test animation — the character walks through different worlds representing chapters of his career.

ENVIRONMENT: [ZONE DESCRIPTION — what fills the world around Sean]

Present on warm cream animation paper (#FAF5E8 approximate). The paper has visible grain texture, subtle aging marks, three hole-punch marks centered at the bottom edge. The environment elements fill the frame — this is a WIDE SHOT showing the character at roughly 40-50% of vertical canvas height with the zone world surrounding him.

[SEAN'S POSE/ACTION — what Sean is doing in this zone]

Match the uploaded reference EXACTLY in character style: traditional animation pencil test drawing with hand-drawn graphite pencil lines. Lines are warm gray (NOT black ink) with natural stroke-weight variation. Visible construction lines beneath the final drawing. Cross-hatching for shading.

CRITICAL: The environment elements (storyboards, game platforms, terminals, etc.) MUST also be drawn in pencil test style — same graphite lines, same cream paper, same hand-drawn quality. Everything in the frame looks like it was drawn by the same animator on the same paper. No style changes between character and environment.

Color is extremely limited and desaturated: dark navy t-shirt, cool gray jeans, warm skin tones, sandy blonde hair. Environment elements are primarily graphite with minimal color accents where needed. Pencil lines visible through all color fills.

Character proportions: Disney/Pixar pre-production adjacent, roughly 7-7.5 heads tall. NOT anime, NOT hyper-realistic.

Lighting is soft and even. Shadows via cross-hatching and pencil density. No dramatic directional light.

No vector-clean lines. No solid black outlines. No cel shading. No anime style. No heavy color saturation. No digital painting look. No gradient shading. No airbrush effects. No pure white background. No pure black lines. No photorealism. No 3D rendering.
```

### Task 1: Zone 1 — Animation / Storytelling Concepts

**Files:**
- Create: `prompts/act2/zone1_concept_A.txt`
- Create: `prompts/act2/zone1_concept_B.txt`
- Create: `prompts/act2/zone1_concept_C.txt`
- Output: `runs/act2-exploration/concepts/zone1/concept_A.png`
- Output: `runs/act2-exploration/concepts/zone1/concept_B.png`
- Output: `runs/act2-exploration/concepts/zone1/concept_C.png`

- [ ] **Step 1: Write Zone 1 Concept A prompt — The Animator's Studio**

Write to `prompts/act2/zone1_concept_A.txt` using the template above with:

**ZONE DESCRIPTION:**
```
A pencil-drawn animator's workspace surrounds the character. An animation desk with a light box glowing faintly sits to the left. Stacked animation paper beside it. On the right, character sheets and gesture drawings are pinned to a wall — loose, expressive pencil sketches of various characters. A film clapperboard leans against the desk. Storyboard panels are taped to the wall above. A pencil-drawn film reel sits on a shelf. Script pages are scattered on the floor. Everything is drawn in the same graphite pencil style as the character — these are drawings within a drawing.
```

**SEAN'S POSE/ACTION:**
```
The character walks through the space from left to right, mid-stride, looking around with fond recognition — like someone revisiting a place they loved. Right hand relaxed at his side (no stylus — it's in his pocket or behind his ear for this zone). Left hand slightly raised, fingers brushing past a hanging character sheet as he passes. Expression: warm half-smile, eyes scanning the drawings around him. Weight on front foot, casual confident walk.
```

- [ ] **Step 2: Write Zone 1 Concept B prompt — The Storyboard Wall**

Write to `prompts/act2/zone1_concept_B.txt` with:

**ZONE DESCRIPTION:**
```
A vast pencil-drawn storyboard wall stretches across the frame. Dozens of small rectangular panels arranged in rows, each containing a tiny pencil sketch — action scenes, character moments, establishing shots. Some panels have pencil arrows between them showing narrative flow. Sticky notes with handwritten annotations. A few panels are blank, waiting to be filled. Below the wall, an animation desk with a stack of paper and a pencil cup. A director's chair sits to one side with "SEAN" roughly penciled on the back.
```

**SEAN'S POSE/ACTION:**
```
The character stands facing the storyboard wall at a slight 3/4 angle, left hand reaching up to touch one of the storyboard panels. His head is tilted up, studying the wall. Expression: focused, contemplative — an artist reviewing his work. Right hand in pocket. Feet planted, weight slightly back — he's pausing mid-walk to look at this.
```

- [ ] **Step 3: Write Zone 1 Concept C prompt — Walking Through Drawings**

Write to `prompts/act2/zone1_concept_C.txt` with:

**ZONE DESCRIPTION:**
```
The character walks through a surreal space where oversized pencil drawings float around him — giant gesture drawings of human figures, an animation flip book fanning open mid-air, storyboard panels drifting like leaves, pencil-drawn film frames suspended in space. A large pencil-drawn camera on a tripod sits in the background. Everything floats on the cream paper like a dream sequence of an animator's memory. Faint pencil construction lines connect the floating elements like constellation lines.
```

**SEAN'S POSE/ACTION:**
```
The character walks confidently from left to right through the floating drawings, mid-stride. His head is turned slightly upward, watching a floating gesture drawing drift past. Right hand at his side. Left arm swings naturally with his walk. Expression: a quiet, knowing smile — these are his creations floating around him. The character is grounded (feet on a subtle ground plane) while the environment floats.
```

- [ ] **Step 4: Generate all three Zone 1 concepts**

```bash
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/zone1_concept_A.txt)" \
  --output runs/act2-exploration/concepts/zone1/concept_A.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env

python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/zone1_concept_B.txt)" \
  --output runs/act2-exploration/concepts/zone1/concept_B.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env

python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/zone1_concept_C.txt)" \
  --output runs/act2-exploration/concepts/zone1/concept_C.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env
```

- [ ] **Step 5: Review all three Zone 1 concepts with Sean**

Read each generated image. Present to Sean for feedback:
- Which concept best captures "Animation / Storytelling" zone?
- Does Sean's character look right? Identity match to A-2?
- Does the environment read as pencil test (not digital)?
- What elements to keep, drop, or combine?

- [ ] **Step 6: Commit Zone 1 concepts**

```bash
git add prompts/act2/zone1_*.txt
git commit -m "art: Zone 1 (Animation/Storytelling) concept explorations"
```

---

### Task 2: Zone 2 — Games / Interactive Concepts

**Files:**
- Create: `prompts/act2/zone2_concept_A.txt`
- Create: `prompts/act2/zone2_concept_B.txt`
- Create: `prompts/act2/zone2_concept_C.txt`
- Output: `runs/act2-exploration/concepts/zone2/concept_{A,B,C}.png`

- [ ] **Step 1: Write Zone 2 Concept A prompt — The Platformer World**

Write to `prompts/act2/zone2_concept_A.txt` using the zone template with:

**ZONE DESCRIPTION:**
```
A pencil-drawn side-scrolling game landscape. Blocky platforms at various heights, drawn with heavy graphite outlines and cross-hatched shading — they look like rough game design sketches on animation paper. A pencil-drawn health bar floats in the upper left corner, partially filled. An XP counter in the upper right shows "LVL 12" in hand-lettered text. Small pencil-drawn coins float above platforms. A tiny inventory grid with pencil-sketched items (sword icon, shield icon, potion icon) sits in the lower right. Ground tiles are drawn as rough squares with pencil texture. Everything has the quality of a game designer's sketchbook — functional but charming.
```

**SEAN'S POSE/ACTION:**
```
The character stands on one of the platforms, looking around the game world with a knowing expression — he built this. Right hand on hip, left hand gesturing casually toward the health bar as if acknowledging it. Expression: slight smirk, raised eyebrow — recognition mixed with pride. His stance is confident, feet shoulder-width apart on the platform edge. He looks like he belongs in this world because he made it.
```

- [ ] **Step 2: Write Zone 2 Concept B prompt — Inside the Game Screen**

Write to `prompts/act2/zone2_concept_B.txt` with:

**ZONE DESCRIPTION:**
```
The frame is composed like looking INTO a pencil-drawn game screen. A thick pencil-drawn border frames the scene like a monitor or TV. Inside, a pencil-drawn 2D game world — rolling hills made of cross-hatched terrain, blocky castle in the background, pixel-style trees drawn in graphite (square canopies, rectangular trunks). Game UI elements are drawn directly on the frame border: health hearts, a minimap, a score counter. The RPG warrior sprite from Act 1 is visible as a tiny pencil figure on a distant platform — a callback. Everything is graphite on cream paper, but arranged like a game screenshot.
```

**SEAN'S POSE/ACTION:**
```
The character walks into the game screen from the left edge, one foot already inside the border, one still outside — he's entering his own creation. Head turned toward the game world inside, expression of delighted surprise. Left hand reaching forward as if stepping through a doorway. Right hand trails behind him, fingers just leaving the edge of the border frame.
```

- [ ] **Step 3: Write Zone 2 Concept C prompt — The Game Design Desk**

Write to `prompts/act2/zone2_concept_C.txt` with:

**ZONE DESCRIPTION:**
```
A pencil-drawn game design workspace merging with a game world. On the left, a desk with graph paper covered in hand-drawn level designs — top-down dungeon maps, side-view platform layouts, enemy concept sketches. On the right, those designs come alive — the drawn platforms extend off the paper and into the space, game characters step out of the sketches. A pencil-drawn game controller sits on the desk. Post-it notes with game mechanic ideas ("DOUBLE JUMP?", "COMBO SYSTEM") are stuck to the edges. The boundary between design document and game world is blurred — drawings becoming playable.
```

**SEAN'S POSE/ACTION:**
```
The character sits on the edge of the desk, one leg dangling, looking at the game world emerging from his designs. Relaxed, satisfied posture — leaning back slightly on his hands. Expression: the same warm recognition as Zone 1 but with more energy — this is where his animation skills became interactive. No stylus visible — hands are occupied supporting his seated lean.
```

- [ ] **Step 4: Generate all three Zone 2 concepts**

```bash
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/zone2_concept_A.txt)" \
  --output runs/act2-exploration/concepts/zone2/concept_A.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env

python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/zone2_concept_B.txt)" \
  --output runs/act2-exploration/concepts/zone2/concept_B.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env

python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/zone2_concept_C.txt)" \
  --output runs/act2-exploration/concepts/zone2/concept_C.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env
```

- [ ] **Step 5: Review Zone 2 concepts with Sean**

Present all three. Key questions:
- Does the "blocky game world in pencil" read correctly?
- Is the game aesthetic pencil-first (not pixel-art-first)?
- Which concept captures "Games / Interactive" best?
- Any real game projects to reference for accuracy?

- [ ] **Step 6: Commit Zone 2 concepts**

```bash
git add prompts/act2/zone2_*.txt
git commit -m "art: Zone 2 (Games/Interactive) concept explorations"
```

---

### Task 3: Zone 3 — AI / Career Pivot Concepts

**Files:**
- Create: `prompts/act2/zone3_concept_A.txt`
- Create: `prompts/act2/zone3_concept_B.txt`
- Create: `prompts/act2/zone3_concept_C.txt`
- Output: `runs/act2-exploration/concepts/zone3/concept_{A,B,C}.png`

- [ ] **Step 1: Write Zone 3 Concept A prompt — The Terminal Discovery**

Write to `prompts/act2/zone3_concept_A.txt` using the zone template with:

**ZONE DESCRIPTION:**
```
A pencil-drawn AI workspace. A large hand-drawn terminal window dominates the center-right of the frame — its border drawn with ruler-straight graphite lines, but the text inside is hand-lettered in a monospace style. The terminal shows a prompt/response exchange: a hand-written ">" prompt with a question, and below it a flowing paragraph of generated text. Floating around the terminal are pencil-sketched concept diagrams — a simple neural network (circles connected by lines), chat bubble shapes, a flowchart showing "INPUT → PROCESS → OUTPUT". Pencil-drawn code snippets float like thought bubbles. Everything has the quality of someone's excited whiteboard sketches after discovering something mind-blowing.
```

**SEAN'S POSE/ACTION:**
```
The character stands in front of the terminal, body angled toward it, both hands raised with palms up in a "whoa" gesture — the moment of discovery. Head tilted slightly back, eyes wide, mouth open in an excited half-smile. This is the "spark" moment echoing Beat 1 of Act 1, but bigger — this isn't a small creative idea, this is a career-changing revelation. Weight forward on his toes, energy leaning into the screen. No stylus — both hands are free and expressive.
```

- [ ] **Step 2: Write Zone 3 Concept B prompt — The Connection Web**

Write to `prompts/act2/zone3_concept_B.txt` with:

**ZONE DESCRIPTION:**
```
The character is surrounded by floating pencil-drawn concepts connected by hand-drawn lines — like a mind map exploding outward. At the center: a pencil-drawn laptop with a glowing screen (the glow suggested by lighter pencil strokes radiating outward). Connected by pencil lines to: a chat interface sketch, a code block, a robot face outline, a brain diagram, an API endpoint diagram ("POST /generate"), a pencil-drawn Claude logo (simple geometric shapes), data flow arrows. The connections multiply outward, filling the frame. Some connections loop back to elements from Zone 1 (a storyboard panel) and Zone 2 (a game sprite) — showing how AI connects to his past work.
```

**SEAN'S POSE/ACTION:**
```
The character reaches out with both hands, touching two of the floating connection nodes — physically connecting ideas. One hand reaches toward the chat interface, the other toward a storyboard panel from Zone 1. His body is in motion — torso rotated, weight shifting — he's actively making connections, not passively observing. Expression: intense focus with excitement underneath — the look of someone who sees how everything fits together. Feet planted wide for stability as he reaches.
```

- [ ] **Step 3: Write Zone 3 Concept C prompt — Typing Into the Future**

Write to `prompts/act2/zone3_concept_C.txt` with:

**ZONE DESCRIPTION:**
```
A pencil-drawn workspace in transition. On the left side: remnants of the previous zones — a storyboard corner, a game controller sketch — fading into lighter pencil strokes. On the right: a bold, detailed pencil drawing of a modern desk setup — laptop open with terminal visible, a second monitor showing a pencil-drawn chat interface, code editor sketched on a tablet. Hand-drawn sticky notes surround the monitors with words like "AGENTS", "PIPELINE", "GENERATE". A pencil-drawn coffee cup steams next to the laptop. The scene feels like an animator's desk that evolved into a technologist's desk — same person, new tools.
```

**SEAN'S POSE/ACTION:**
```
The character sits at the desk, hands hovering over a pencil-drawn keyboard, fingers mid-type. His posture is engaged — leaning slightly forward, shoulders active. He's looking at the terminal screen with the same concentrated expression an animator has when drawing — but now the tool is a keyboard instead of a pencil. Expression: focused determination with a slight smile — he's found his new medium. Chair drawn at a 3/4 angle so we see his profile and the screen content.
```

- [ ] **Step 4: Generate all three Zone 3 concepts**

```bash
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/zone3_concept_A.txt)" \
  --output runs/act2-exploration/concepts/zone3/concept_A.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env

python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/zone3_concept_B.txt)" \
  --output runs/act2-exploration/concepts/zone3/concept_B.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env

python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/zone3_concept_C.txt)" \
  --output runs/act2-exploration/concepts/zone3/concept_C.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env
```

- [ ] **Step 5: Review Zone 3 concepts with Sean**

Present all three. Key questions:
- Does "AI discovery" come through in pencil test style?
- Does the terminal/code content read as hand-drawn (not digital)?
- Which concept captures the career pivot moment best?
- Is the "spark" callback to Act 1 Beat 1 landing?

- [ ] **Step 6: Commit Zone 3 concepts**

```bash
git add prompts/act2/zone3_*.txt
git commit -m "art: Zone 3 (AI/Career Pivot) concept explorations"
```

---

### Task 4: Zone 4 — Creative Technologist Convergence Concepts

**Files:**
- Create: `prompts/act2/zone4_concept_A.txt`
- Create: `prompts/act2/zone4_concept_B.txt`
- Create: `prompts/act2/zone4_concept_C.txt`
- Output: `runs/act2-exploration/concepts/zone4/concept_{A,B,C}.png`

- [ ] **Step 1: Write Zone 4 Concept A prompt — The Convergence Workspace**

Write to `prompts/act2/zone4_concept_A.txt` using the zone template with:

**ZONE DESCRIPTION:**
```
A pencil-drawn workspace where ALL previous zones converge into one space. A hand-drawn Kanban board dominates the background — but its cards are animation storyboard thumbnails and game design sketches. A pencil-drawn terminal window sits to one side, showing a chat exchange. Floating near the top: game UI elements (health bar, XP counter) repurposed as project status indicators. A storyboard panel from Zone 1 is pinned next to a code snippet from Zone 3. A pencil-drawn game sprite sits on top of the Kanban board like a mascot. Everything from Sean's journey is present, organized, and working together. A small hovering shape (placeholder for the AI companion) floats near Sean's right shoulder — simple geometric form, pencil-drawn, friendly.
```

**SEAN'S POSE/ACTION:**
```
The character stands confidently in the center of this convergence space, surveying everything around him. Stylus back in his right hand — held up casually, not drawing with it, just holding it like a conductor's baton. Left hand rests on the edge of the Kanban board. Expression: quiet satisfaction — the look of someone who sees how every chapter of their life led to this moment. Stance is grounded and open — weight evenly distributed, shoulders relaxed, chest open. He owns this space.
```

- [ ] **Step 2: Write Zone 4 Concept B prompt — The Collaboration Moment**

Write to `prompts/act2/zone4_concept_B.txt` with:

**ZONE DESCRIPTION:**
```
A pencil-drawn creative workspace focused on the collaboration between Sean and his AI companion. The AI companion is a friendly pencil-drawn character — round head about 20% the size of Sean's, two expressive dot eyes, a subtle curved line mouth, simple geometric body. It hovers at Sean's shoulder height, drawn with slightly lighter pencil strokes to suggest it floats. Between them: a pencil-drawn card or document they're both reaching toward — Sean from the left, the companion gesturing from the right. Behind them: a simplified version of the convergence workspace — Kanban board, terminal, storyboard elements, but softer and less detailed so the focus stays on the two characters. The RPG warrior sprite from Act 1 sits on top of the companion's head, tiny and content.
```

**SEAN'S POSE/ACTION:**
```
The character reaches toward the shared card/document with his right hand (stylus held between fingers like a pen). His body is angled toward the companion — an open, collaborative posture. Head tilted slightly, making eye contact with the companion with a warm expression. This mirrors the nod from Act 1 Beat 3, but directed at a new partner. Left hand relaxed at his side. The body language says "let's build this together."
```

- [ ] **Step 3: Write Zone 4 Concept C prompt — The Wide Panorama**

Write to `prompts/act2/zone4_concept_C.txt` with:

**ZONE DESCRIPTION:**
```
An ultra-wide pencil-drawn panorama showing Sean's entire journey in a single frame. From left to right: Zone 1 elements (animation desk, storyboards, film elements) blend gradually into Zone 2 (game platforms, health bars, pixel-style terrain) which blend into Zone 3 (terminals, code, AI diagrams) which arrive at Zone 4 (the convergence workspace with Kanban board). The zones share the same cream paper and pencil style throughout — the transitions are in subject matter, not aesthetic. The panorama reads like a timeline drawn by an animator. Faint dotted pencil lines trace the path through all zones, showing the journey.
```

**SEAN'S POSE/ACTION:**
```
The character stands at the far right of the panorama (in the Zone 4 convergence area), turned to face LEFT — looking back at his entire journey stretching behind him. The AI companion hovers at his right shoulder. The RPG warrior sprite sits on the companion. Stylus held up in right hand — not drawing, just holding it like a painter stepping back from the canvas. Expression: quiet pride, slight smile, eyes scanning the full panorama. This is the final hold pose — the moment before the title card.
```

- [ ] **Step 4: Generate all three Zone 4 concepts**

```bash
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/zone4_concept_A.txt)" \
  --output runs/act2-exploration/concepts/zone4/concept_A.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env

python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/zone4_concept_B.txt)" \
  --output runs/act2-exploration/concepts/zone4/concept_B.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env

python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/zone4_concept_C.txt)" \
  --output runs/act2-exploration/concepts/zone4/concept_C.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env
```

- [ ] **Step 5: Review Zone 4 concepts with Sean**

Present all three. Key questions:
- Does the convergence concept work — elements from all zones in one space?
- Does the AI companion placeholder design feel right? (Full design in Round 3)
- Does the wide panorama composition work for the closer?
- Does the sprite-on-companion visual payoff land?

- [ ] **Step 6: Commit Zone 4 concepts**

```bash
git add prompts/act2/zone4_*.txt
git commit -m "art: Zone 4 (Creative Technologist convergence) concept explorations"
```

---

### Task 5: Round 1 Review Checkpoint

- [ ] **Step 1: Assemble all 12 concepts for side-by-side review**

Read all 12 generated images and present them organized by zone. Ask Sean:

1. **Per zone:** Which concept (A/B/C) is the strongest? Any to combine?
2. **Across zones:** Does the visual progression feel like a career journey?
3. **Style consistency:** Do all zones feel like the same pencil test universe?
4. **Identity:** Is Sean recognizable and consistent across all concepts?
5. **What's missing?** Any elements from his real career that should be in here?

- [ ] **Step 2: Document Round 1 decisions**

Create `runs/act2-exploration/concepts/round1-decisions.md` with:
- Selected concept per zone (or hybrid description)
- Elements to keep/drop/refine
- Notes for transition exploration (Round 2)
- Any prompt adjustments needed

- [ ] **Step 3: Commit decisions**

```bash
git add runs/act2-exploration/concepts/round1-decisions.md
git commit -m "review: Round 1 zone concept selections and feedback"
```

---

## Round 2: Transition Experiments

Depends on Round 1 completion and Sean's selections. Generate 2-3 transition concepts for each zone boundary.

### Task 6: Zone 1→2 Transition Concepts

**Files:**
- Create: `prompts/act2/trans_z1_to_z2_A.txt`
- Create: `prompts/act2/trans_z1_to_z2_B.txt`
- Create: `prompts/act2/trans_z1_to_z2_C.txt`
- Output: `runs/act2-exploration/concepts/transitions/z1_to_z2_{A,B,C}.png`

- [ ] **Step 1: Write 3 transition prompts**

Each prompt shows the MOMENT of transition — Sean between zones. Use the selected Zone 1 and Zone 2 concepts from Round 1 as context. Three different transition ideas:

**Concept A — The Drawing Comes Alive:** Sean's animation drawing morphs into a game character, pulling Sean through the paper into the game world. The frame shows the moment of transformation — half-animation, half-game.

**Concept B — The Flip Book Portal:** Sean flips through an animation flip book that becomes a game screen. The pages fan out and Sean walks through the gap between pages into the game zone.

**Concept C — Gradual Blend:** The left side of frame is pure Zone 1, the right side is pure Zone 2, and the middle is a natural blend — animation desk elements gradually becoming game platforms. Sean walks through the blend zone. No gag, just elegant transition.

Write full prompts using the zone template, customizing ZONE DESCRIPTION to show the transitional moment and SEAN'S POSE/ACTION to show Sean in the act of crossing between worlds.

- [ ] **Step 2: Generate all three transition concepts**

```bash
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/trans_z1_to_z2_A.txt)" \
  --output runs/act2-exploration/concepts/transitions/z1_to_z2_A.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env

python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/trans_z1_to_z2_B.txt)" \
  --output runs/act2-exploration/concepts/transitions/z1_to_z2_B.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env

python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/trans_z1_to_z2_C.txt)" \
  --output runs/act2-exploration/concepts/transitions/z1_to_z2_C.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env
```

- [ ] **Step 3: Review with Sean and commit**

```bash
git add prompts/act2/trans_z1_to_z2_*.txt
git commit -m "art: Zone 1→2 transition concept explorations"
```

---

### Task 7: Zone 2→3 Transition Concepts

**Files:**
- Create: `prompts/act2/trans_z2_to_z3_A.txt`
- Create: `prompts/act2/trans_z2_to_z3_B.txt`
- Create: `prompts/act2/trans_z2_to_z3_C.txt`
- Output: `runs/act2-exploration/concepts/transitions/z2_to_z3_{A,B,C}.png`

- [ ] **Step 1: Write 3 transition prompts**

Three ideas for Game→AI transition:

**Concept A — Falling Down the Rabbit Hole:** The game ground breaks open and Sean falls through — the hole is lined with pencil-drawn code and neural network diagrams. Sean is mid-fall, surprised but thrilled, arms spread. Below him: the AI zone opening up.

**Concept B — Game Over → New Game:** A pencil-drawn "GAME OVER" screen appears, then glitches/transforms into a terminal prompt cursor blinking. Sean watches the transformation, then starts typing. The game world dissolves into code around him.

**Concept C — The Level-Up:** Sean hits a pencil-drawn level-up portal in the game zone. Instead of the next game level, the portal opens into the AI workspace. Game UI elements morph into terminal UI. The health bar becomes a progress bar. XP counter becomes a token counter.

Write full prompts for each.

- [ ] **Step 2: Generate all three and review with Sean**

Same generation commands as Task 6, adjusted for z2_to_z3 paths.

- [ ] **Step 3: Commit**

```bash
git add prompts/act2/trans_z2_to_z3_*.txt
git commit -m "art: Zone 2→3 transition concept explorations"
```

---

### Task 8: Zone 3→4 Transition Concepts

**Files:**
- Create: `prompts/act2/trans_z3_to_z4_A.txt`
- Create: `prompts/act2/trans_z3_to_z4_B.txt`
- Create: `prompts/act2/trans_z3_to_z4_C.txt`
- Output: `runs/act2-exploration/concepts/transitions/z3_to_z4_{A,B,C}.png`

- [ ] **Step 1: Write 3 transition prompts**

Three ideas for AI→Convergence transition:

**Concept A — The Wireframe Hook:** Clean geometric wireframe lines reach out from Zone 4 and literally lasso/hook Sean, pulling him forward. The lines wrap around his waist playfully — not threatening, more like a friendly tug. Sean leans into it, grinning. The AI companion is visible in the distance, the source of the lines.

**Concept B — The Companion Beckons:** The AI companion materializes at the edge of Zone 3, hovering and gesturing "follow me." It floats backward into Zone 4, leaving a trail of pencil-drawn connection lines. Sean follows, walking through a curtain of floating code that dissolves into the convergence workspace.

**Concept C — Everything Converges:** Elements from all previous zones start drifting toward a central point ahead of Sean — storyboard panels, game sprites, code blocks, all floating and assembling into the convergence workspace. Sean walks toward this gravitational center as his entire journey reassembles around him.

Write full prompts for each.

- [ ] **Step 2: Generate all three and review with Sean**

Same generation pattern.

- [ ] **Step 3: Commit**

```bash
git add prompts/act2/trans_z3_to_z4_*.txt
git commit -m "art: Zone 3→4 transition concept explorations"
```

---

### Task 9: Round 2 Review Checkpoint

- [ ] **Step 1: Review all 9 transition concepts with Sean**

Present organized by zone boundary. Key questions:
1. Which transition style per boundary? Silly gag, elegant blend, or something else?
2. Do the transitions feel consistent in tone or should each be different?
3. Any new ideas sparked by seeing these?

- [ ] **Step 2: Document Round 2 decisions**

Create `runs/act2-exploration/concepts/round2-decisions.md`.

- [ ] **Step 3: Commit**

```bash
git add runs/act2-exploration/concepts/round2-decisions.md
git commit -m "review: Round 2 transition selections and feedback"
```

---

## Round 3: AI Companion Character Design

### Task 10: Companion Character Concepts

**Files:**
- Create: `prompts/act2/companion_concept_A.txt`
- Create: `prompts/act2/companion_concept_B.txt`
- Create: `prompts/act2/companion_concept_C.txt`
- Create: `prompts/act2/companion_with_sprite.txt`
- Output: `runs/act2-exploration/concepts/companion/concept_{A,B,C}.png`
- Output: `runs/act2-exploration/concepts/companion/with_sprite.png`

- [ ] **Step 1: Write Companion Concept A prompt — The Geometric Friend**

Write to `prompts/act2/companion_concept_A.txt`:

```
Using the uploaded character sketch as the style reference, create a CHARACTER DESIGN SHEET for an AI companion character in pencil test animation style. The sheet shows 3-4 views of the same character on warm cream animation paper (#FAF5E8) with pencil grain texture and hole-punch marks.

THE AI COMPANION CHARACTER: A friendly, geometric character inspired by AI assistant mascots. Round head (circle), approximately 20% the size of the human character's head in the reference. Two large expressive dot eyes — simple but capable of conveying emotion through position and size. A subtle curved line for a mouth that can smile. Simple geometric body — rounded rectangle or oval torso, no legs (it hovers). Small simple arms/appendages that can gesture. Drawn in the same graphite pencil style as the human character — warm gray lines, construction marks visible, cross-hatching for shading.

KEY TRAITS: The companion should feel warm and approachable, not cold or mechanical. The lines have slight thickness variation — drawn with care, not ruler-perfect. It "breathes" through subtle size/opacity changes in its idle state. Despite being geometric, it has personality and expressiveness.

VIEWS TO SHOW:
1. Front-facing neutral hover pose
2. Side view showing depth/dimensionality
3. Excited/happy expression (eyes wider, slight bounce up)
4. Thinking/focused expression (eyes narrowed slightly, tilted)

Hand-written labels in pencil: "AI COMPANION — v1", character height comparison next to a small sketch of the human character for scale.

Same pencil test aesthetic as the reference. No vector lines. No solid black. No digital look. No anime. No photorealism. Warm, hand-drawn, alive.
```

- [ ] **Step 2: Write Companion Concepts B and C with variations**

**Concept B — The Cody Mascot Style:** More angular, star-shaped or diamond-shaped head. Bigger personality, more expressive limbs. Think Claude Code's terminal cursor given a face and arms. Write to `prompts/act2/companion_concept_B.txt` using the same character sheet structure as Concept A — 4 views, scale comparison, pencil test style — but replace the round-head geometric description with angular/star-shaped geometry.

**Concept C — The Minimal Orb:** Even simpler — just a hovering circle with two dots for eyes. Personality comes entirely from movement and context, not from design complexity. Like a pencil-drawn Navi. Write to `prompts/act2/companion_concept_C.txt` using the same character sheet structure as Concept A — 4 views, scale comparison — but describe a minimal hovering orb/sphere with dot eyes and no limbs. Expressiveness comes from eye position and body tilt only.

- [ ] **Step 3: Generate all three companion concepts**

```bash
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/companion_concept_A.txt)" \
  --output runs/act2-exploration/concepts/companion/concept_A.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env

python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/companion_concept_B.txt)" \
  --output runs/act2-exploration/concepts/companion/concept_B.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env

python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/companion_concept_C.txt)" \
  --output runs/act2-exploration/concepts/companion/concept_C.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env
```

- [ ] **Step 4: Review companion concepts with Sean, select design**

- [ ] **Step 5: Generate sprite-riding-companion image**

After companion design is selected, write `prompts/act2/companion_with_sprite.txt` showing the RPG warrior sprite sitting on top of the companion as it hovers. Use the approved companion design + existing sprite reference (`candidates/sprite/turnaround_01.png`).

```bash
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/companion_with_sprite.txt)" \
  --output runs/act2-exploration/concepts/companion/with_sprite.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png runs/run_2026-04-04_174805/candidates/sprite/turnaround_01.png \
  --env-file .env
```

- [ ] **Step 6: Review and commit**

```bash
git add prompts/act2/companion_*.txt
git commit -m "art: AI companion character design explorations"
```

---

### Task 11: Round 3 Review Checkpoint

- [ ] **Step 1: Final companion review with Sean**

- Does the companion feel like a natural part of the pencil test world?
- Does the sprite-on-companion visual payoff land?
- Any design adjustments before moving to anchor keyframes?

- [ ] **Step 2: Document Round 3 decisions**

Create `runs/act2-exploration/concepts/round3-decisions.md`.

- [ ] **Step 3: Commit**

```bash
git add runs/act2-exploration/concepts/round3-decisions.md
git commit -m "review: Round 3 companion design selection and feedback"
```

---

## Round 4: Anchor Keyframes + Seedance Test

Depends on Rounds 1-3 being complete with approved zone looks, transitions, and companion design. Tasks here will be refined based on Round 1-3 decisions.

### Task 12: Generate Act 2 Anchor Keyframes

Based on approved zone concepts and transitions from Rounds 1-3, generate proper start/end frame anchors for each Seedance clip. The exact frames depend on decisions made in earlier rounds.

- [ ] **Step 1: Define anchor frame list based on Round 1-3 decisions**

Create `runs/act2-exploration/anchor-frame-plan.md` mapping:
- Each zone's entry pose, signature moment pose, and exit pose
- Each transition's start and end frame
- The closer panorama composition

- [ ] **Step 2: Write anchor prompts and generate**

Write prompts to `prompts/act2/anchor_F{##}.txt` following the Act 1 keyframe prompt pattern (full 7-layer framework with identity constraints). Generate each anchor with A-2 reference.

- [ ] **Step 3: Review anchors for QA gates**

Check each anchor against:
- Identity match to A-2 (blocker)
- Pencil test style (blocker)
- Correct aspect ratio 16:9 (blocker)
- Paper texture present (blocker)

- [ ] **Step 4: Commit approved anchors**

```bash
git add prompts/act2/anchor_*.txt
git commit -m "art: Act 2 anchor keyframes for Seedance pipeline"
```

---

### Task 13: First Seedance 2.0 Test

- [ ] **Step 1: Host anchor frames for Seedance API**

Upload approved start/end frames to accessible URLs (fal.ai upload or public hosting).

- [ ] **Step 2: Run Seedance on simplest zone clip**

Pick the zone with the least complex motion (likely Zone 1 — Sean walking through animation studio). Use the Seedance prompt template from `docs/seedance-production-plan.md`:

```python
import fal_client, os
os.environ["FAL_KEY"] = os.getenv("FAL_KEY")

result = fal_client.subscribe(
    "bytedance/seedance-2.0/image-to-video",
    arguments={
        "prompt": "[COMPRESSED ACTION PROMPT — 60-80 words]",
        "image_url": "[START FRAME URL]",
        "end_image_url": "[END FRAME URL]",
        "resolution": "720p",
        "duration": "5",
        "generate_audio": False,
    },
)
```

- [ ] **Step 3: Extract frames and review**

```bash
ffmpeg -i seedance_output.mp4 -vf fps=12 runs/act2-exploration/seedance/test_clip/frame_%04d.png
```

Review extracted frames:
- Does pencil test aesthetic survive Seedance interpolation?
- Is Sean's identity maintained throughout?
- Does the zone environment hold up in motion?
- Any artifacts, ghosting, or style drift?

- [ ] **Step 4: Document Seedance test results**

Create `runs/act2-exploration/seedance/test-results.md` with findings and GO/NO-GO decision for proceeding with full Act 2 Seedance pipeline.

- [ ] **Step 5: Commit**

```bash
git add runs/act2-exploration/seedance/test-results.md
git commit -m "test: first Act 2 Seedance 2.0 clip — results and findings"
```

---

## Summary

| Round | Tasks | NB2 Generations | Goal |
|-------|-------|----------------|------|
| Setup | 0 | 0 | Directory structure |
| 1: Zone Shots | 1-5 | ~12 | Lock zone visual identity |
| 2: Transitions | 6-9 | ~9 | Find playful transition moments |
| 3: Companion | 10-11 | ~4-6 | Lock AI companion design |
| 4: Anchors + Seedance | 12-13 | ~12-18 + Seedance | Prove Act 2 pipeline works |
| **Total** | **13 tasks** | **~37-45** | **Visual direction locked, Seedance validated** |

Each round ends with a review checkpoint where Sean directs the next round. The plan is intentionally flexible after Round 1 — exact prompts for Rounds 2-4 will be informed by what we learn in earlier rounds.
