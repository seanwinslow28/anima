# Seedance 2.0 Pipeline — Session Prompt


You are helping me build a complete animation production pipeline using Seedance 2.0 as the motion generation engine and Google Gemini Nano Banana 2 (NB2) as the cleanup/final render engine. This is for a portfolio hero animation — a pencil test of myself (Sean) as a hand-drawn 2D character on vintage cream animation paper.

## Your approach

Work through this session in three phases. Do NOT skip ahead — complete each phase before moving to the next.

<phase1>
## Phase 1: Creative Interview + Storyboard Alignment

Before any research or planning, interview me about the storyboard and creative vision. Read `docs/pencil-test-storyboard.md` and the project's `CLAUDE.md` first, then ask me questions to understand:

- What is the emotional arc I want the viewer to feel across Act 1 and Act 2?
- Which beats are most important to me and which have flexibility?
- What does "success" look like for the final piece — portfolio impression? Festival submission? Both?
- Are there any storyboard beats I've reconsidered or want to adjust now that we've seen what video models can do?
- What's my quality bar — where am I willing to accept "good enough" motion vs. where do I need frame-perfect cleanup?
- The sprite element (Beat 2) and AI companion (Beat 5-6) — are these still composited separately, or could Seedance handle them inline?
- Act 2 scope — am I targeting the full 250-frame piece or a shorter cut?

Ask these as a natural conversation, not a checklist. Listen to my answers and ask follow-up questions. When you feel you understand the creative vision well enough to make good judgment calls throughout the rest of the session, summarize what you've learned and confirm alignment before moving to Phase 2.
</phase1>

<phase2>
## Phase 2: Seedance 2.0 Deep Research

Research Seedance 2.0 thoroughly. I need you to understand this model inside and out so we can make informed decisions about our pipeline. Investigate:

### Model Capabilities
- What are Seedance 2.0's core capabilities? (start frame, end frame, text-to-video, image-to-video, etc.)
- What resolution and duration options does it support?
- What frame rates does it output at?
- How does its start-frame/end-frame interpolation actually work?
- What are its known strengths and limitations?

### Prompting Strategies
- What prompting approaches produce the best results with Seedance 2.0?
- How detailed should prompts be? (We already learned that compressed prompts work better than detailed ones with video models — verify this holds for Seedance specifically)
- Are there Seedance-specific prompt formats, keywords, or techniques that improve output?
- How does it handle style consistency across generations?
- What are common failure modes and how do you avoid them?

### API Access
- How does Seedance 2.0 work through the Fal.ai API?
- What are the API parameters (model ID, inference settings, pricing)?
- Can we script batch generation, or is manual generation through the web UI better for our use case?
- What's the generation time per video?

### For Our Specific Use Case
- How well does Seedance handle hand-drawn/illustrated styles vs. photorealistic?
- Will it preserve the pencil-on-paper aesthetic, or will it drift toward digital/clean styles?
- How does it handle character consistency across multiple video segments?
- Can we chain multiple Seedance generations (output of one becomes input to next)?

Use web search, documentation, community posts, and any available resources. Be thorough — this research will drive every decision in Phase 3. Present your findings organized by the categories above, with specific recommendations for our project.
</phase2>

<phase3>
## Phase 3: Full Production Plan

Based on the creative interview (Phase 1) and Seedance research (Phase 2), create a detailed production plan covering the entire storyboard — Act 1 AND Act 2.

### Plan Structure

For each storyboard beat (Beats 1-7), define:

1. **Start/End Frame Strategy** — Which frames need to be generated with NB2 as anchor images for Seedance? Map every start-frame/end-frame pair needed.

2. **NB2 Generation Prompts** — Write the actual prompts for generating each start/end frame using the `gemini-pencil-animation-image-gen` skill. These frames must be high-quality because they anchor the video generation.

3. **Seedance Prompts** — Write the compressed, action-focused video prompts for each segment. Follow the lesson we learned: describe WHAT happens, not HOW each body part moves. Let the model fill in the motion.

4. **Frame Extraction Plan** — After Seedance generates each video segment, which frames do we extract? Map extracted frames to the storyboard's key pose numbers (F1, F6, F10, F13, etc.).

5. **NB2 Cleanup Pass** — For each extracted frame, what needs to be regenerated/cleaned? Typical issues: morphing artifacts, hand anatomy, identity drift, stylus continuity. Write the cleanup prompts that use the extracted Seedance frame as a composition/pose reference + the A-2 anchor for identity lock.

6. **Assembly Order** — How do the cleaned frames sequence together? What's the final frame count and timing?

### Key Decisions to Address
- Should we generate Act 1 and Act 2 as separate Seedance runs or try to chain them?
- The zone transitions in Act 2 (pencil → pixel → wireframe) — can Seedance handle style transitions, or do we need to composite those?
- The sprite element and AI companion — inline generation vs. separate composite layers?
- How many Seedance generations do we expect to need per beat (accounting for retries)?
- What's our QA gate for accepting vs. rejecting a Seedance generation?

### Deliverable
A step-by-step production checklist I can execute, with all prompts written and ready to run. Organize it so I can work through it sequentially, with clear "checkpoint" moments where I should review results before proceeding.
</phase3>

## Project Context

- The character reference (A-2 anchor) is at `images/2D-Character-Sketch-Sean-v1.png`
- A successful Seedance 2.0 test already exists at `runs/run_2026-04-04_174805/export/seedance-2.0-output/Act-1-Test-Seedance-2.0.mp4` — look at it for quality reference
- The start/end frames used for that test are in `runs/run_2026-04-04_174805/export/sequence/frame_0001.png` and `frame_0033.png`
- NB2 generation uses the script at `.claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py`
- Read `CLAUDE.md` for the full project manual, pipeline architecture, and QA gates
- Read `docs/pencil-test-storyboard.md` for the complete storyboard
- Check `docs/production-checklist.md` for current production status

## Critical Constraints

- **Video model prompting rule:** Compressed, action-focused prompts outperform detailed ones. Describe the action arc, not frame-by-frame body mechanics. This was validated through testing.
- **Identity consistency:** Every frame must be recognizably Sean matching the A-2 anchor. This is the #1 quality gate.
- **Style consistency:** Hand-drawn graphite pencil on cream animation paper. If it looks digital, clean, or 3D at any point, it fails.
- **Engine truth:** "If the loop plays smoothly at 12fps and the character is recognizably Sean in pencil test style on cream animation paper, it ships."
