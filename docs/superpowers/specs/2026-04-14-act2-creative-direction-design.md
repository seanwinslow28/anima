# Act 2 Creative Direction — Design Spec

**Date:** 2026-04-14
**Status:** Approved design, pending implementation plan
**Branch:** `ultraplan/seedance-pipeline`

---

## Thesis

A creative technologist's career told through hand-drawn animation — where every chapter of his life (animation, games, AI) is drawn in pencil on the same cream paper, because the craft is the thread that connects it all.

The meta-thesis: this entire piece was made with AI tools, but it looks and feels hand-drawn. Viewers should have no idea this was an AI workflow until they explore the case study breakdown. The medium IS the message.

## Audience

- **Primary:** Portfolio visitors — hiring managers, creative directors, collaborators. They should understand what Sean does in under 30 seconds.
- **Secondary:** AI film festival submissions. The human-AI collaboration narrative + genuine animation quality (not "AI slop") gives solo animators/storytellers hope that they can create work with real style using AI tools without thousands of dollars.

## Narrative Structure

**The Walk.** Sean walks right through pencil-drawn career zones. The entire piece stays in pencil test style throughout — only the subject matter of the drawings shifts between zones. Act 1 lulls viewers into thinking this is a simple static pencil test. Act 2 breaks the loop and opens into a cinematic journey with camera movements, pans, angle changes, and playful transitions.

### The Sprite's Role

The RPG warrior sprite is the **catalyst**, not a tour guide. After the Act 1 nod, the sprite zooms off Sean's shoulder (as proven in the Seedance test: `Act-1-Test-Seedance-2.0.mp4`), flying off in a direction that Sean follows. The sprite exits the narrative during the zone walk. It returns at the end, riding the AI companion as it hovers into frame — connecting Sean's creative past (the sprite he drew) with his present tool (the AI companion).

### Zone Map

| Zone | Chapter | What It Represents | Visual World |
|------|---------|-------------------|--------------|
| 1 | Animation / Storytelling | The origin — film school, drawing, YouTube shorts, the love of narrative and craft | Pencil-drawn storyboards, animation desk, character sheets, gesture drawings, light box, film elements (clapperboard, script pages) |
| 2 | Games / Interactive | Applying animation craft to interactive worlds | Pencil-drawn blocky game landscape — platforms, health bars, XP counters, inventory grids, all in graphite on cream paper |
| 3 | AI / Career Pivot | The obsession — discovering AI, everything changes | Pencil-drawn terminal screens, code blocks, neural network diagrams, chat interfaces, floating API diagrams |
| 4 | Creative Technologist (Present Day) | Convergence — all threads woven together | Elements from ALL previous zones combined — animation thumbnails as Kanban cards, game sprites as task icons, terminals next to storyboard panels. AI companion lives here. |

### Transitions Between Zones

Transitions are **playful and specific to each world** — not generic wipes or hard cuts. A mix of gradual blending and silly animation moments. Examples explored during brainstorming:

- Falling through a hole into another realm
- Wireframe lines reaching out and hooking/dragging Sean into the next scene
- Walking off the edge of a "page"
- Game portal pulling Sean in
- Elements from the next zone bleeding into the current one

**Specific transitions will be determined visually** — we generate 2-3 concept versions of each transition and let the images decide what works.

### The Closer

Camera pulls back to reveal the entire journey — all four zones visible in one wide pencil-drawn panorama stretching behind Sean. The AI companion hovers nearby with the sprite riding on its back. Sean faces the viewer. Hold.

Title card: "Sean Winslow — Creative Technologist" in hand-drawn pencil lettering. Page lifts off the peg bar, revealing the portfolio site beneath.

### AI Companion Character

- Visual inspiration: Claude Code mascot energy — friendly, geometric but warm
- Drawn in pencil test style (same as everything else — not a different aesthetic)
- Hovers/floats (doesn't walk) — contrasts Sean's grounded movement
- Appears in Zone 4 (present day)
- The sprite rides the companion when it enters — visual payoff connecting past and present
- Sean and the companion collaborate — building, organizing, creating together
- Callback to Act 1: Sean and companion share a nod

## Aesthetic Rules

- **Everything stays pencil test.** Every zone, every element, every character is hand-drawn graphite on cream animation paper. The "pixel zone" is pencil-drawn blocky game elements. The "AI zone" is pencil-drawn terminals and code.
- **The paper is constant.** Cream animation paper with hole-punch marks and production labels throughout.
- **Style consistency with Act 1.** Same line weight, same construction line visibility, same A-2 character identity.
- **Cinematic ambition is a feature.** Camera movements, dynamic framing, and motion graphics energy — executed in 2D pencil test style — are the surprise. This subverts expectations of what "hand-drawn" animation can feel like.

## Pacing

**Let it find its length.** No duration commitment until we lock visuals. Start with ~4-6 anchor keyframes per zone, assemble rough timing tests, adjust from there. Act 1 is 3.5 seconds. The original storyboard estimated 15-25 seconds for Act 2. The actual length will be determined by what the images and Seedance clips tell us feels right.

## Production Approach: Explore, Then Commit

Four rounds of visual exploration, each building on the last. Sean's creative process is visual — he needs to see options in pencil, not read descriptions. Generate, react, refine.

### Round 1: Zone Establishing Shots (~8-12 NB2 generations)

Generate 2-3 concept images per zone showing what each world looks like with Sean in it. No animation yet — just establishing the visual identity of each zone.

- Zone 1: Sean among pencil-drawn storyboards, animation desk, character sheets
- Zone 2: Sean in a pencil-drawn blocky game landscape with health bars, platforms
- Zone 3: Sean at a pencil-drawn terminal, floating code/AI diagrams
- Zone 4: Sean surrounded by elements from all zones + AI companion placeholder

**Goal:** Lock the visual identity of each zone.

### Round 2: Transition Experiments (~6-9 NB2 generations)

Generate transition moment concepts — multiple ideas for how Sean moves between zones. The silly/playful ideas: falling through a hole, getting hooked by wireframe lines, walking off a page edge, game portal, etc.

Generate 2-3 versions of each transition. Pick the ones that spark excitement.

**Goal:** Find the transitions that have personality.

### Round 3: AI Companion Character Design (~4-6 NB2 generations)

Design the AI companion character. Claude Code mascot energy in pencil test style. Character sheet options — different sizes, expressions, hover poses. Also: the sprite riding the companion.

**Goal:** Lock the companion design.

### Round 4: Anchor Keyframes + Seedance Test (~12-18 NB2 generations + Seedance clips)

Once zones, transitions, and companion are locked, generate proper anchor keyframes (start/end frames for each Seedance clip). Run the first Seedance 2.0 test on the simplest zone transition.

**Goal:** Prove the Seedance pipeline works for Act 2 material.

## Pipeline Integration

### Generation Tools

| Tool | Role in Act 2 |
|------|---------------|
| Gemini Nano Banana 2 | All concept art and anchor keyframe generation |
| Seedance 2.0 (fal.ai) | Motion interpolation between anchor keyframes |
| NB2 redraw | Clean up Seedance-extracted frames to restore pencil test fidelity |
| Procreate | Manual cleanup, sprite tracing, special elements |
| FFmpeg | Frame extraction from Seedance, assembly, export |

### Seedance Approach

Same philosophy as Act 1: **Seedance finds the motion, NB2 protects the aesthetic.**

1. Seedance generates fluid motion between approved NB2 anchor keyframes
2. Extract frames at 12fps
3. Review and select frames with best timing, arcs, acting
4. NB2 redraws selected frames to restore pencil test fidelity
5. Procreate traces for special elements (sprite motion, companion)

### QA Gates

Same gates as the existing `docs/seedance-production-plan.md`:
- Identity match to A-2 (blocker)
- Pencil test style preservation (blocker)
- Motion smoothness at 12fps (blocker)
- Stylus in right hand (blocker in zones where Sean holds it; may be pocketed/absent in zones where he interacts with other objects — e.g., typing at a terminal, flipping pages)
- Paper texture, construction lines, frame continuity, hand anatomy (warnings)

### Directory Structure

```
runs/{run_id}/
├── concepts/                    # Round 1-3 exploration
│   ├── zone1/                   # Zone establishing shots
│   ├── zone2/
│   ├── zone3/
│   ├── zone4/
│   ├── transitions/             # Transition experiments
│   └── companion/               # AI companion character design
├── candidates/                  # Round 4+ production candidates
│   └── F{##}/
├── approved/                    # Approved anchor keyframes
├── seedance/                    # Seedance clip outputs
├── audit/
└── export/
```

## Engine Truth (unchanged)

> If the loop plays smoothly at 12fps and the character is recognizably Sean in pencil test style on cream animation paper, it ships.

Extended for Act 2: if the full piece tells Sean's career story through pencil-drawn worlds, and viewers believe it's hand-drawn until they learn otherwise, the thesis holds.

## Open Questions (to be resolved visually)

- Exact signature moments in each zone (determined in Round 1)
- Specific transition gags between zones (determined in Round 2)
- AI companion exact design (determined in Round 3)
- Duration and frame count per zone (determined in Round 4)
- Whether the closer panorama is one wide frame or a camera pan across multiple frames
- Title card lettering style and page-lift timing (deferred to compositing phase)
