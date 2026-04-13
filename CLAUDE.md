# Pencil Test — Sean Winslow

A manifest-driven animation production pipeline for generating a pencil test animation portfolio hero piece. Hand-drawn 2D character on vintage animation production paper, orchestrated with Python scripts and Claude Code.

## Start Here

**Always check `docs/production-checklist.md` first.** It tracks what's been completed, what's in progress, and what's blocked across all production phases. Update it as work is completed.

## Source of Truth Documents

| Document | Path | Role |
|----------|------|------|
| **Production Checklist** | `docs/production-checklist.md` | **Check first every session** — current status of all phases, frames, and assets |
| Storyboard | `docs/pencil-test-storyboard.md` | Complete production storyboard — 7 beats, 2 acts, frame counts, key pose descriptions |
| Keyframe Prompts | `docs/act1-keyframe-prompts.md` | 6 ready-to-run Gemini prompts for Act 1 key poses with post-generation checklist |
| A-2 Anchor | `images/2D-Character-Sketch-Sean-v1.png` | Identity reference — all generated frames must match this character |
| Manifest | `manifest.yaml` | Pipeline configuration — single source of truth for generation, audit, and export settings |
| Seedance Research | `docs/seedance-research-findings.md` | Seedance 2.0 capabilities, API specs, prompting guide, style preservation strategies |
| Seedance Production Plan | `docs/seedance-production-plan.md` | Beat-by-beat Seedance prompts, frame extraction maps, QA gates, cost estimates |
| Changelog | `CHANGELOG.md` | Decision history — what changed, why, and lessons learned for prompt engineering |
| Original Pipeline | `docs/Sprite-Sheet-Automation-Project_OG-Workflow-Summary.md` | Architectural reference (manifest-driven design, audit loop, retry ladder) |

## Pipeline Architecture

```
Phase A          Phase B           Phase B.5          Phase C          Phase D          Phase E
SCAFFOLD    -->  GENERATE     -->  MOTION         -->  AUDIT       -->  ASSEMBLE    -->  QA REVIEW
                                                    
manifest.yaml    generate.py       Seedance 2.0       audit.py         assemble.sh      creative-director
directory        Gemini API        Fal.ai API         Claude vision     FFmpeg           critique rubric
structure        frame chaining    start+end frame    hard/soft fails   hold timing      2d-animation QA
                                   extract → NB2      retry ladder      GIF/WebM/MP4     "done" checklist
```

### Seedance Pipeline (Phase B.5)

**Philosophy: Seedance finds the motion, NB2 protects the aesthetic.**

1. Seedance 2.0 generates fluid motion video between approved NB2 anchor keyframes
2. Extract frames at 12fps from Seedance output
3. Review and select frames with best timing, arcs, and acting
4. NB2 redraws selected frames to restore full pencil test fidelity
5. Procreate traces for sprite motion and special elements

### Core Loop (adapted from sprite pipeline)

```
Generate frame --> Audit (hard fails? reject) --> Soft fails? --> Retry (max 3) --> Approve
                                                                                      |
                                                                           Copy to approved/
```

## Skills Map

| Skill | Pipeline Phase | Role |
|-------|---------------|------|
| `gemini-pencil-animation-image-gen` | B (Generation) | Primary keyframe generator — pencil test style via Gemini Nano Banana 2 API |
| `image-generator-prompt-science` | B (Generation) | 7-Layer prompt framework, refinement tips for retries |
| `animation-pipeline` | A-E (All phases) | Pipeline orchestration — manifest-driven generation, frame chaining, QA gates (HF/SF/CC), assembly |
| `2d-animation-principles` | C (Audit), D (Assembly) | Animation physics, timing/spacing validation, expression arc (CC08), hold duration, AI frame validation |
| `creative-director` | E (QA Review) | Critique rubric (Identity/Style/Composition/Continuity/Technical), prompt refinement as art direction |
| `comfyui-workflows` | B (In-betweens) | OpenPose ControlNet in-between generation, IPAdapter identity lock, video model node integration |
| `video-animation-production` | D (Assembly) | FFmpeg frame sequence assembly, two-pass GIF optimization, WebM/MP4 export |
| `gemini-image-gen` | B (Generation, Act 2) | Non-pencil assets — zone backgrounds, props (deferred to Act 2) |
| `video-animation-production` | B.5 (Motion), D (Assembly) | Seedance frame extraction, FFmpeg assembly, format conversion |

## Directory Structure

```
sw-portfolio-animation-pipeline/
├── CLAUDE.md                         # This file — project manual
├── manifest.yaml                     # Pipeline source of truth
├── docs/                             # Source of truth documents
│   ├── pencil-test-storyboard.md
│   ├── act1-keyframe-prompts.md
│   └── Sprite-Sheet-Automation-Project_OG-Workflow-Summary.md
├── images/                           # Reference assets
│   └── 2D-Character-Sketch-Sean-v1.png   # A-2 anchor character
├── pipeline/                         # Pipeline scripts
│   ├── generate.py                   # Generation orchestrator with frame chaining
│   ├── audit.py                      # QA gate checker (PIL + structured vision prompts)
│   └── assemble.sh                   # FFmpeg assembly commands
└── runs/                             # Per-run output (gitignored)
    └── {run_id}/                     # e.g., run_2026-04-04_001
        ├── manifest.lock.yaml        # Frozen config snapshot
        ├── candidates/               # All generated candidates (preserved)
        │   └── F{##}/                # Per-frame candidate directory
        │       ├── attempt_01.png
        │       └── attempt_02.png
        ├── approved/                 # Approved keyframes
        │   ├── PT_A1_F01_key.png
        │   └── PT_A1_F06_key.png
        ├── rejected/                 # Rejected frames with failure codes
        │   └── F{##}_attempt_{##}_{FAIL_CODE}.png
        ├── audit/                    # Audit logs
        │   ├── audit_log.jsonl
        │   └── run_summary.json
        └── export/                   # Final outputs
            ├── pencil-test-act1.gif
            ├── pencil-test-act1.webm
            └── pencil-test-act1.mp4
```

## Asset Naming Convention

Adapted from `animation-pipeline` skill's `{SequenceID}_{SceneID}_{ShotID}_{Layer}_{FrameNumber}.{ext}` pattern:

```
PT_{ActID}_{FrameNumber}_{AssetType}.{ext}
```

| Example | Meaning |
|---------|---------|
| `PT_A1_F06_key.png` | Pencil Test, Act 1, Frame 6, keyframe |
| `PT_A1_F18_key.png` | Pencil Test, Act 1, Frame 18, keyframe |
| `PT_A2_F97_key.png` | Pencil Test, Act 2, Frame 97, keyframe |

Candidates: `F{##}/attempt_{##}.png` (e.g., `F06/attempt_01.png`)
Rejected: `F{##}_attempt_{##}_{FAIL_CODE}.png` (e.g., `F06_attempt_01_SF01.png`)

## Manifest Schema

The `manifest.yaml` file is the pipeline's single source of truth. See `manifest.yaml` for the full config. Key sections:

- **project** — Name, version, description
- **anchor** — Path to A-2 character reference, label, description
- **style** — Aesthetic constraints: paper color, line color, required elements, negatives
- **generation** — Model, aspect ratio, script path, max retries
- **act1** — Keyframe list with frame numbers, labels, poses, references (for chaining), hold durations
- **audit** — Hard fails (HF01-HF05), soft fails (SF01-SF05), retry ladder
- **export** — Output format specs (GIF, WebM, MP4)

## QA Gates

### Hard Fails (Blocking — instant reject)

| Code | Name | Test |
|------|------|------|
| HF01 | Wrong aspect ratio | Image is not 16:9 (within 2% tolerance). Checked via PIL. |
| HF02 | Missing paper texture | Background is pure white, gray, or lacks cream paper grain |
| HF03 | Wrong direction | Character orientation doesn't match storyboard beat |
| HF04 | Wrong pose | Pose doesn't match storyboard description (e.g., arms down when should be raised) |
| HF05 | Wrong aesthetic | Digital/anime/3D render look instead of pencil test drawing |

### Soft Fails (Trigger retry with corrections)

| Code | Name | Test | Retry Strategy |
|------|------|------|----------------|
| SF01 | Style drift | Line weight inconsistent, construction lines absent, cross-hatching missing | Re-anchor with A-2 + style refinement prompt |
| SF02 | Identity drift | Facial features don't match Sean (hair, jaw, eyes differ from A-2) | Re-anchor + explicit identity corrections |
| SF03 | Proportion drift | Head-to-body ratio, arm length, height inconsistent with A-2 | Add proportion constraints referencing A-2 |
| SF04 | Paper texture | Wrong grain, missing hole-punch marks or production label | Add paper texture refinement block |
| SF05 | Expression mismatch | Expression doesn't match storyboard beat description | Add explicit expression direction |

### Retry Ladder

1. **Attempt 1:** Original prompt from `act1-keyframe-prompts.md`
2. **Attempt 2:** Re-anchor from A-2 + specific correction notes based on failure
3. **Attempt 3:** Tighten prompt with refinement tips from `pencil-animation-prompt-templates.md`
4. **Attempt 4:** STOP — flag for human review with diagnostic report

## Key Commands

### Generation

Generate a single keyframe (example: F06):
```bash
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "[PROMPT]" \
  --output runs/{run_id}/candidates/F06/attempt_01.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png \
  --env-file .env
```

With frame chaining (example: F10 references A-2 + approved F06):
```bash
python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py \
  "[PROMPT]" \
  --output runs/{run_id}/candidates/F10/attempt_01.png \
  --aspect-ratio 16:9 \
  --reference images/2D-Character-Sketch-Sean-v1.png runs/{run_id}/approved/PT_A1_F06_key.png \
  --env-file .env
```

### Orchestrated generation run
```bash
python3 pipeline/generate.py --manifest manifest.yaml
```

### Audit
```bash
python3 pipeline/audit.py --run-dir runs/{run_id} --frame F06 --attempt 1
```

### Assembly
```bash
bash pipeline/assemble.sh runs/{run_id}
```

### Frame Sequence (12fps, Act 1 hero loop)
```bash
# MP4 (archival)
ffmpeg -framerate 12 -i frame_%04d.png -c:v libx264 -crf 18 -pix_fmt yuv420p pencil-test-act1.mp4

# WebM (web)
ffmpeg -i pencil-test-act1.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 pencil-test-act1.webm

# GIF (hero loop, two-pass palette, <5MB)
ffmpeg -i pencil-test-act1.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" pencil-test-act1.gif
```

## Generation Chains

Act 1 has two independent generation chains. Each frame in a chain depends on the previous frame being approved first.

- **Chain 1:** F06 → F10 → F13 → F18 (Beat 1-2: idle through mid-gesture)
- **Chain 2:** F31 → F36 (Beat 3: sprite lands through nod)

Chains 1 and 2 are independent and can run in parallel.

F01 and F40 use the A-2 anchor directly (no generation needed).

## Continuity Audit

Run after a full generation pass to catch frame-to-frame continuity errors:

```bash
python3 pipeline/continuity_audit.py --run-dir runs/{run_id}
```

Checks 8 continuity dimensions across all consecutive frame pairs:

| Check | Severity | What it catches |
|-------|----------|----------------|
| CC01 — Stylus hand | Blocker | Stylus must stay in character's RIGHT hand |
| CC02 — Stylus presence | Blocker | Stylus must be visible in every frame |
| CC03 — Clothing | Blocker | Same outfit in every frame |
| CC04 — Facing direction | Warning | General body orientation consistency |
| CC05 — Scale/position | Warning | Character height and ground plane |
| CC06 — Hair | Warning | Shape, volume, part direction |
| CC07 — Foot position | Warning | Ground plane and stance width |
| CC08 — Expression arc | Warning | Emotional progression follows storyboard |

Log findings: `python3 pipeline/continuity_audit.py --run-dir runs/{run_id} --log-finding CC01 F13 "description"`

## Seedance Generation

Generate a Seedance 2.0 video with start+end frame interpolation:
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
video_url = result["video"]["url"]
```

Extract frames at 12fps from Seedance output:
```bash
ffmpeg -i seedance_output.mp4 -vf fps=12 frame_%04d.png
```

**Seedance prompting rules:**
- 60–80 words, action-focused (WHAT happens, not body mechanics)
- Always include: "fixed camera, locked tripod" and "stylus in right hand"
- Never use: "cinematic", "4K", "glow", "epic", unqualified "fast"
- Don't re-describe the character — the start/end frames provide that
- See `docs/seedance-research-findings.md` for full prompting guide

## Dependencies

```bash
pip install pyyaml Pillow google-genai fal-client
```

- **PyYAML** — manifest parsing in generate.py
- **Pillow** — aspect ratio check in audit.py (HF01)
- **google-genai** — Gemini API calls in generate_image.py
- **fal-client** — Seedance 2.0 API calls via fal.ai
- **FFmpeg** — frame assembly in assemble.sh (`brew install ffmpeg`)
- **bc** — GIF size calculation in assemble.sh (pre-installed on macOS)

Environment variables (in `.env`):
- `GEMINI_API_KEY` — Google Gemini API key
- `FAL_KEY` — Fal.ai API key for Seedance 2.0

## Prompt Files

Individual prompt text files live in `prompts/F{##}.txt` (e.g., `prompts/F06.txt`). These are the 7-Layer formatted prompts extracted from `docs/act1-keyframe-prompts.md`.

The generate.py orchestrator auto-loads prompts from this directory. Override with `--prompt "..."` or `--prompt-file path.txt`.

## Engine Truth

> If the loop plays smoothly at 12fps and the character is recognizably Sean in pencil test style on cream animation paper, it ships.

This is the project's north star — adapted from the original sprite pipeline's "if it plays cleanly in Phaser, it ships." The final animation in its target medium (browser GIF/WebM loop) is the ultimate arbiter of quality.
