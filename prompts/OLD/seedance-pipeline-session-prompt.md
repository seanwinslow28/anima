# Seedance 2.0 Pipeline — Kickoff Session Prompt

> Copy-paste this into a new Claude Code thread to start the Seedance production session. Make sure `FAL_KEY` is set in `.env` before starting.

---

## The Prompt

```
You are helping me execute a Seedance 2.0 motion generation pipeline for my pencil test animation project. This is a production session — we're generating video, extracting frames, and cleaning them up.

## Read These First

Before doing anything, read these files in order:
1. `CLAUDE.md` — full project manual, pipeline architecture, QA gates
2. `docs/production-checklist.md` — current production status
3. `docs/seedance-research-findings.md` — Seedance 2.0 capabilities, API specs, prompting guide
4. `docs/seedance-production-plan.md` — beat-by-beat production plan with all prompts written
5. `docs/pencil-test-storyboard.md` — the creative storyboard

## Creative Context

**North star:** "This person bridges traditional craft and modern tools." The animation should feel hand-drawn. Viewers shouldn't realize it's an AI workflow.

**Pipeline philosophy — Seedance finds the motion, NB2 protects the aesthetic:**
1. Seedance 2.0 generates fluid motion video between approved NB2 anchor keyframes
2. We extract frames at 12fps from Seedance output
3. Review and select frames with best timing/arcs/acting
4. NB2 redraws selected frames to restore full pencil test fidelity
5. Procreate traces for sprite motion

**Quality bar:** Every frame must read as hand-drawn pencil on cream animation paper — in motion AND in isolation. If it looks digital, it fails.

## What To Do

### Step 1: Setup Verification
- Verify `FAL_KEY` exists in `.env`
- Install `fal-client` if needed: `pip install fal-client`
- Confirm approved keyframes exist in `runs/run_2026-04-04_174805/approved/`
- The keyframes need to be hosted at accessible URLs for the fal.ai API. Help me figure out the best approach (fal.ai file upload, temporary hosting, or base64).

### Step 2: Test Run — Clip 1A (F01 → F06)
This is our proof of concept. Generate the simplest transition first.

**Start frame:** `runs/run_2026-04-04_174805/approved/PT_A1_F01_key.png` (A-2 idle)
**End frame:** `runs/run_2026-04-04_174805/approved/PT_A1_F06_key.png` (glance down)

Use the Seedance prompt from `docs/seedance-production-plan.md` for Clip 1A. Start with Fast tier at 480p/4s to validate the aesthetic survives, then scale to 720p if it looks good.

**After generation:**
1. Download the output video
2. Extract frames at 12fps: `ffmpeg -i output.mp4 -vf fps=12 frame_%04d.png`
3. Show me the extracted frames for review
4. Compare against existing approved in-betweens in `approved/`

### Step 3: Go/No-Go Decision
Based on the test results, I'll decide:
- Does the pencil test aesthetic survive Seedance interpolation?
- Is the motion quality worth the NB2 cleanup pass?
- Do we proceed with remaining Act 1 clips or adjust approach?

If GO → proceed through the remaining Act 1 clips (1B, 2A, 3A, 3B) from the production plan.
If the sprite transformation looks promising → test the Seedance approach for Beat 2 sprite motion.

### Step 4: Frame Selection + NB2 Cleanup (if we proceed)
For each approved Seedance clip:
1. Extract all frames at 12fps
2. I'll identify which frames to keep for proper animation timing
3. Use `gemini-pencil-animation-image-gen` to redraw selected frames with full pencil test fidelity
4. The Seedance frame becomes the POSE reference, A-2 becomes the STYLE/IDENTITY reference

## Critical Rules

- **Seedance prompts must be SHORT** — 60-80 words, action-focused. See the research findings doc.
- **Always include in every prompt:** "fixed camera, locked tripod" and "stylus in right hand"
- **Never use:** "cinematic", "4K", "glow", "epic", unqualified "fast"
- **Don't re-describe the character** in Seedance prompts — the start/end frames provide that
- **Identity match to A-2 anchor is the #1 blocker** — if Sean isn't recognizable, reject
- **Style preservation is the #2 blocker** — if it looks digital/clean/3D, reject
- **Test cheap first:** Fast tier, 480p, 4 seconds. Only scale up after validating.

## Key Files

| File | Purpose |
|------|---------|
| `images/2D-Character-Sketch-Sean-v1.png` | A-2 anchor — identity/style reference for NB2 cleanup |
| `runs/run_2026-04-04_174805/approved/` | All 31 approved frames (keyframes + in-betweens) |
| `runs/run_2026-04-04_174805/export/seedance-2.0-output/Act-1-Test-Seedance-2.0.mp4` | Existing Seedance test — quality reference |
| `docs/seedance-production-plan.md` | All prompts written and ready |
| `.env` | Contains GEMINI_API_KEY and FAL_KEY |

Let's start with Step 1. Verify the setup and help me get the keyframe images hosted for the API.
```
