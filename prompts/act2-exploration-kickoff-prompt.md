# Act 2 Visual Exploration — Kickoff Session Prompt

> Copy-paste the prompt below into a new Claude Code session to begin Round 1 concept art generation. Make sure `GEMINI_API_KEY` is set in `.env` before starting.

---

## The Prompt

```
You are helping me execute Round 1 of the Act 2 visual exploration for my pencil test animation project. We're generating concept art with Gemini Nano Banana 2 to establish the visual identity of four career zones before committing to production.

## Read These First

Before doing anything, read these files in this exact order:

1. `CLAUDE.md` — full project manual, pipeline architecture, skills map, QA gates
2. `docs/production-checklist.md` — current production status (Act 1 complete, Act 2 planning)
3. `docs/superpowers/specs/2026-04-14-act2-creative-direction-design.md` — the creative direction spec (thesis, zones, aesthetic rules, production approach)
4. `docs/superpowers/plans/2026-04-14-act2-visual-exploration.md` — the full implementation plan with all prompts written out
5. `docs/act1-keyframe-prompts.md` — Act 1's prompt structure for style reference (7-Layer framework)
6. `prompts/F06.txt` — read one Act 1 prompt to understand the exact prompt voice and structure

Also read the A-2 anchor image so you know what Sean looks like:
- `images/2D-Character-Sketch-Sean-v1.png` — this is the character identity reference for ALL generations

## Creative Context

<context>
  <thesis>A creative technologist's career told through hand-drawn animation — every chapter drawn in pencil on the same cream paper, because the craft is the thread that connects it all.</thesis>

  <meta_thesis>This entire piece was made with AI tools, but it looks and feels hand-drawn. Viewers should have no idea this was an AI workflow until they explore the case study breakdown.</meta_thesis>

  <narrative>The Walk — Sean walks right through pencil-drawn career zones. Everything stays pencil test style throughout. Only the subject matter shifts between zones. Act 1 is a simple static pencil test loop. Act 2 breaks the loop and opens into a cinematic journey.</narrative>

  <aesthetic_rules>
    - Everything is hand-drawn graphite on cream animation paper (#FAF5E8)
    - Paper texture, hole-punch marks, and production labels throughout
    - Same line weight and construction line visibility as Act 1
    - Environment elements drawn in the SAME pencil style as Sean — no style changes between character and background
    - Color is extremely limited: dark navy t-shirt, cool gray jeans, warm skin, sandy blonde hair, graphite environments
    - 10 explicit negatives: no vector lines, no black outlines, no cel shading, no anime, no saturation, no digital painting, no gradients, no airbrush, no pure white BG, no pure black lines
  </aesthetic_rules>
</context>

<zones>
  <zone id="1" name="Animation / Storytelling" theme="The origin">
    Film school, drawing, YouTube shorts, the love of narrative and craft. Visual world: pencil-drawn storyboards, animation desk, character sheets, gesture drawings, light box, film elements (clapperboard, script pages).
  </zone>

  <zone id="2" name="Games / Interactive" theme="Craft applied">
    Applying animation skills to interactive worlds. Visual world: pencil-drawn blocky game landscape — platforms, health bars, XP counters, inventory grids, all in graphite on cream paper. Like a game designer's sketchbook.
  </zone>

  <zone id="3" name="AI / Career Pivot" theme="The obsession">
    Discovering AI, everything changes. Visual world: pencil-drawn terminal screens, code blocks, neural network diagrams, chat interfaces, floating API diagrams. The excitement of discovery.
  </zone>

  <zone id="4" name="Creative Technologist" theme="Convergence">
    All threads woven together. Visual world: elements from ALL previous zones combined — animation thumbnails as Kanban cards, game sprites as task icons, terminals next to storyboard panels. The AI companion (Claude Code mascot style, pencil-drawn, hovers) lives here.
  </zone>
</zones>

## What To Do

You are executing Tasks 0 through 5 from the implementation plan. Follow the plan exactly.

### Step 1: Setup (Task 0)

Create the directory structure:

```bash
mkdir -p runs/act2-exploration/concepts/{zone1,zone2,zone3,zone4,transitions,companion}
mkdir -p runs/act2-exploration/{candidates,approved,seedance,audit,export}
mkdir -p prompts/act2
```

Verify the A-2 anchor image and generation script exist:

```bash
ls -la images/2D-Character-Sketch-Sean-v1.png
ls -la .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py
grep GEMINI_API_KEY .env
```

### Step 2: Generate Zone Concepts (Tasks 1-4)

For each zone, the plan contains 3 complete prompts (Concepts A, B, C). Execute them in this order:

1. Write the prompt text files to `prompts/act2/` exactly as specified in the plan
2. Generate each image using this command pattern:

```bash
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/{prompt_file}.txt)" \
  --output runs/act2-exploration/concepts/{zone}/{concept}.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env
```

3. After generating each image, READ the output image and check:
   - Does Sean match the A-2 anchor? (identity)
   - Is the style pencil test on cream paper? (aesthetic)
   - Are environment elements drawn in pencil too? (style consistency)
   - Does the zone's subject matter come through clearly? (concept)
4. Show me each generated image and tell me what you see

Generate ALL 4 zones (12 images total) before stopping for review. Zones are independent — if one zone's generation fails, continue with the others and retry the failed one after.

### Step 3: Review Checkpoint (Task 5)

After all 12 concepts are generated, present them organized by zone and ask me:

1. Which concept (A/B/C) is strongest per zone?
2. Does the visual progression feel like a career journey?
3. Style consistency across zones?
4. What to keep, drop, combine, or redo?

Document my feedback in `runs/act2-exploration/concepts/round1-decisions.md`.

## Critical Rules

<rules>
  <rule priority="blocker">Identity match to A-2 anchor is the #1 requirement. Sean must be immediately recognizable in every image. Same hair, jaw, eye spacing, nose, proportions, clothing.</rule>

  <rule priority="blocker">Everything must look hand-drawn on cream paper. If ANY element looks digital, clean, or AI-generated, the image fails. Environment elements must match the pencil test aesthetic — not just the character.</rule>

  <rule priority="important">Use the FULL prompt text from the implementation plan. Do not shorten or summarize the prompts. The Act 1 prompts succeeded because they were detailed and specific — Act 2 prompts must be equally thorough.</rule>

  <rule priority="important">The stylus can be absent, pocketed, or behind Sean's ear in Act 2 zones where he interacts with other objects. Each prompt specifies what his hands are doing — follow it.</rule>

  <rule priority="important">16:9 aspect ratio for all generations. These are wide establishing shots showing Sean in his environment.</rule>

  <rule priority="workflow">Generate the image, then READ it to verify quality before moving to the next. If an image clearly fails (wrong style, identity drift, wrong aspect ratio), retry once with the same prompt before moving on.</rule>

  <rule priority="workflow">Commit prompt files after each zone is complete. Do not batch all commits to the end.</rule>
</rules>

## Key Files

| File | Purpose |
|------|---------|
| `images/2D-Character-Sketch-Sean-v1.png` | A-2 anchor — identity/style reference for ALL generations |
| `prompts/F06.txt` | Act 1 prompt example — voice and structure reference |
| `docs/superpowers/plans/2026-04-14-act2-visual-exploration.md` | Full plan with all prompt text |
| `docs/superpowers/specs/2026-04-14-act2-creative-direction-design.md` | Creative direction spec |
| `.env` | Contains GEMINI_API_KEY |
| `runs/act2-exploration/concepts/` | Output directory for all concept art |

## Skill Usage

Use the `gemini-pencil-animation-image-gen` skill for generation guidance. Use `image-generator-prompt-science` if you need to refine a failing prompt. Use `creative-director` if you need to evaluate a generated image against the project's critique rubric.

Let's start with Step 1 — verify the setup, then begin generating Zone 1 concepts.
```
