# Act 2 Visual Exploration — Continuation Session Prompt

> Copy everything below the divider into a fresh Claude Code thread in this repo to continue the Act 2 visual exploration. The first task is a specific re-generation; after that, the user will pick favorites from the existing concept set.

---

You are continuing the Act 2 visual exploration for a pencil test animation portfolio piece. The work is mid-flight — Round 1, Round 1.5, and Round 2 of generations are complete, but one image needs to be re-generated before the user picks final favorites.

<project_context>
This is a manifest-driven 2D animation production pipeline. Act 1 (the hero loop) is complete and shipped. Act 2 explores Sean's career journey through pencil-drawn worlds: Film origins → Animation craft → AI Discovery → Workshop/tools → Convergence/PM role.

The aesthetic is **traditional pencil test animation on cream paper (#FAF5E8)** with hand-drawn graphite lines, construction lines visible, cross-hatching for shading. Every element — characters, environments, UI, text — must be drawn in this style. No digital aesthetic.

Two character refs beyond Sean's A-2 anchor:
- **AI Companion** — terracotta-orange loaf creature with dot eyes, stubby arms/legs, small mouth. Hovers/floats.
- **RPG Warrior Sprite** — chibi warrior with spiky sandy-blonde hair, cream tunic, sheathed sword. The character Sean drew in Act 1.

Read these first to get context:
1. `CLAUDE.md` — full project manual
2. `docs/superpowers/specs/2026-04-14-act2-creative-direction-design.md` — creative direction spec
3. `prompts/act2-exploration-kickoff-prompt.md` — original kickoff that started this exploration
4. `prompts/F06.txt` — example Act 1 prompt for voice/structure reference
</project_context>

<current_status>
**Round 1 (12 concepts, completed):** Three concepts each for Zone 1-4. Located in `runs/act2-exploration/concepts/zone{1,2,3,4}/concept_{A,B,C}.png`. After review, the user dropped Zone 2 entirely and pivoted to a tighter beat sheet.

**Round 1.5 (8 revised concepts, completed):** New beat sheet generated. Files in `runs/act2-exploration/concepts/`:
- `zone1/film.png` — Beat 1a: Sean walks through floating film world
- `zone1/animation.png` — Beat 1b: Sean walks through floating animation world
- `zone1/ai_discovery.png` — Beat 1c: Sean walks through floating AI news headlines (ChatGPT/Ghibli, Karpathy, Vibe Coding, Anthropic, Gemini)
- `zone3/sit_down.png` — Beat 2: Sean sits at desk, no sticky notes
- `zone3/terminal_reveal.png` — Beat 3 (original wide shot version): Companion appears in terminal, Sean reacts
- `zone3/revelation.png` — Beat 4 (original): World opens up, companion + Sean reaching to connect ideas
- `zone4/pm_role.png` — Beat 5: Sean reaches for Kanban card, claiming PM role, companion floats nearby
- `zone4/final_panorama.png` — Beat 6: Wide journey panorama (had section labels — superseded by v3)

**Round 2 (9 variants, completed):** Tighter beat options + atmospheric variants:
- `zone3/terminal_closeup_empty.png` — straight-on close-up of laptop, terminal blinking "c:\>_ what is..." (NEEDS RE-GENERATION — see Task 1 below)
- `zone3/terminal_closeup_companion.png` — same straight-on framing, AI companion peeking out of terminal saying "hello, sean..." with stubby arms on the bottom edge
- `zone3/terminal_pov_sean.png` — reverse shot from inside the terminal, tight on Sean's surprised face with cool blue screen-light shading
- `zone3/transition_warped_zoom.png` — extreme close-up of Sean's eye, swirling vortex pulling into his iris where mind-map elements are visible
- `zone3/transition_pulled_in.png` — Sean leans dramatically forward, companion's arm reaches out of the terminal grabbing his hand
- `zone3/revelation_v2_dissolving.png` — Sean stood up, desk dissolving into mind-map, palms turning upward
- `zone3/revelation_v3_radiating.png` — Sean centered, sun-burst pencil rays, mind-map in rosette around him
- `zone3/revelation_v4_dreamspace.png` — Sean seated in floating chair in infinite cream paper dreamspace
- `zone4/final_panorama_v3_a.png`, `_v3_b.png`, `_v3_c.png` — three variants of the cleaned panorama with Sean's body in 3/4 toward camera (the v1 craftsman pose), with agentic workflow theme content (AGENT HARNESS, TOOL USE, AI AGENTS RUN WORKFLOWS, AGENT → TOOL → RESULT diagram)
</current_status>

<your_first_task priority="blocker">
**Re-generate `runs/act2-exploration/concepts/zone3/terminal_closeup_empty.png`** to match the polished style of `runs/act2-exploration/concepts/zone3/terminal_closeup_companion.png`.

**Why this matters:** The current `terminal_closeup_empty.png` was re-generated in the previous session and came back in a sketchier, looser style than the companion shot. The user wants these two frames to cut together as a continuous beat ("empty terminal blinking" → "companion appears in terminal"), so they must share the exact same visual style, framing, and laptop design — only the screen content and a few sparkle/glow effects should differ between them.

**Reference images to load:**
- `runs/act2-exploration/concepts/zone3/terminal_closeup_companion.png` — STYLE TARGET. The new empty frame should look like this minus the companion.
- `images/2D-Character-Sketch-Sean-v1.png` — A-2 anchor for any Sean fingertip details.

**The prompt to use:**

Read `prompts/act2/zone3_terminal_closeup_empty.txt`. Update it so the FIRST line emphasizes that the companion image is the visual style and composition reference, then run generation passing the companion image as a reference alongside the A-2 anchor.

Run command:
```bash
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "$(cat prompts/act2/zone3_terminal_closeup_empty.txt)" \
  --output runs/act2-exploration/concepts/zone3/terminal_closeup_empty.png \
  --aspect-ratio 16:9 \
  --reference runs/act2-exploration/concepts/zone3/terminal_closeup_companion.png images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env
```

**Acceptance criteria:**
- Same straight-on, head-on framing as the companion shot
- Same laptop body, screen border, terminal window styling, A-2 production label, coffee mug placement, paper grain
- Same polished cross-hatching and line weight (NOT sketchy/loose)
- Terminal screen reads `c:\>_ what is...` with a blinking cursor block at the end
- AI companion is NOT in the terminal (it's empty, blinking, waiting)
- Sean's fingertips visible at the bottom of the keyboard, hovering over keys
- ABSOLUTELY NO PENCIL, PEN, OR STYLUS anywhere in the image (Sean's hands are empty in the next shot)

**Validation step:** After generating, read the new image and visually compare to `terminal_closeup_companion.png`. If the line weight, cross-hatching density, or laptop design differs significantly, retry once with stronger style-match language. If it still drifts, report back to the user before doing more attempts.
</your_first_task>

<then_wait_for_user>
After Task 1 completes, present the user with the locked beat sheet and ask them to pick favorites from the existing concept set:

**Locked Beat Sheet (from Round 1.5 + Round 2):**
| Beat | Frame | Status |
|------|-------|--------|
| 1a | Walking through Film world | `zone1/film.png` (locked) |
| 1b | Walking through Animation world | `zone1/animation.png` (locked) |
| 1c | Walking through AI Discovery | `zone1/ai_discovery.png` (locked) |
| 2 | Sit down at desk | `zone3/sit_down.png` (locked) |
| 3a | Terminal blinking (empty) | `zone3/terminal_closeup_empty.png` (regenerating in Task 1) |
| 3b | Companion appears in terminal | `zone3/terminal_closeup_companion.png` (locked) |
| 3c | Sean's surprised reaction (POV) | `zone3/terminal_pov_sean.png` (locked) |
| Trans | Transition into revelation | **DECISION PENDING:** warped zoom OR pulled-in |
| 4 | The Revelation | **DECISION PENDING:** original, v2 dissolving, v3 radiating, or v4 dreamspace |
| 5 | PM Role / Kanban | `zone4/pm_role.png` (locked) |
| 6 | Final Panorama | **DECISION PENDING:** v3a, v3b, or v3c |

After the user picks, document their decisions in `runs/act2-exploration/concepts/round2-decisions.md` and commit. Then the next phase is to plan Round 3 (production keyframes for each beat — proper anchor frames for Seedance interpolation).
</then_wait_for_user>

<project_rules priority="critical">
- **Identity match to A-2 is the #1 requirement.** Sean must be immediately recognizable in every image. Same hair, jaw, eye spacing, nose, proportions, dark navy crew-neck, cool gray jeans, sneakers. Subtle 5-o'clock shadow is acceptable continuity for Act 2 frames where he's been working.
- **Everything must look hand-drawn on cream paper.** If ANY element looks digital, clean, or AI-generated, the image fails. Environment elements must match the pencil aesthetic — not just the character.
- **16:9 aspect ratio for all generations.**
- **Hand-lettered text only.** All text in the image (terminal output, headlines, Kanban columns, sticky notes, brand names) must look hand-lettered in pencil. Never typeset, never digital.
- **The 10 explicit negatives** must be in every prompt: no vector lines, no black outlines, no cel shading, no anime, no saturation, no digital painting, no gradients, no airbrush, no pure white BG, no pure black lines.
- **Use the prompt-engineering skill** when writing or refining prompts. Use the **creative-director skill** when evaluating generated images.
</project_rules>

<key_file_paths>
| What | Path |
|------|------|
| A-2 anchor (Sean) | `images/2D-Character-Sketch-Sean-v1.png` |
| AI Companion turnaround | `runs/act2-exploration/concepts/companion/turnaround_02.png` |
| AI Companion clean pose | `runs/act2-exploration/concepts/companion/concept_B.png` |
| RPG Warrior Sprite turnaround | `runs/run_2026-04-04_174805/candidates/sprite/turnaround_01.png` |
| RPG Warrior Sprite shoulder pose | `runs/run_2026-04-04_174805/candidates/sprite/sprite_shoulder_standalone_01.png` |
| Generation script | `.claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py` |
| Act 1 prompt example | `prompts/F06.txt` |
| All Act 2 prompts | `prompts/act2/` |
| Generated concepts | `runs/act2-exploration/concepts/` |
| Creative direction spec | `docs/superpowers/specs/2026-04-14-act2-creative-direction-design.md` |
| Implementation plan | `docs/superpowers/plans/2026-04-14-act2-visual-exploration.md` |
| Original kickoff prompt | `prompts/act2-exploration-kickoff-prompt.md` |
| API key | `.env` (GEMINI_API_KEY) |
</key_file_paths>

<known_persistent_issues>
- Nano Banana Pro 2 sometimes duplicates brand-name labels in the panorama (especially "Anthropic", "AGENT HARNESS"). After ~3 iterations the user accepted these will be cleaned up in Procreate during compositing rather than continuing to iterate against NB2.
- NB2 sometimes leaks stage directions from prompts as visible text annotations (e.g., "ANIMATION LIGHT BOX SUGGESTION" appeared in one panorama). Avoid parenthetical hints and instructional language in prompts. Tightly constrained "DO NOT WRITE THESE WORDS" lists help but aren't 100%.
- NB2 occasionally swaps requested words ("AI AGENTS RUN WORKFLOWS" became "AI GEMINI RUN WORKFLOWS" in one variant). Worth catching but not a blocker.
</known_persistent_issues>

<reasoning>
Start by reading CLAUDE.md, the creative direction spec, and the kickoff prompt to anchor yourself. Then examine the two terminal close-up images (companion vs empty) side by side to see the style mismatch yourself. Update the prompt to lead with the companion as the style reference. Generate. Verify. If it matches, present the beat sheet to the user for favorite-picking. If it doesn't match, retry once with stronger language, then pause and report back rather than spinning.
</reasoning>
