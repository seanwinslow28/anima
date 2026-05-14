# Pencil Test — Sean Winslow

A manifest-driven animation production pipeline for generating a pencil test animation portfolio hero piece. Hand-drawn 2D character on vintage animation production paper, orchestrated with Python scripts and Claude Code.

## Start Here

**Always check `docs/production-checklist.md` first.** It tracks what's been completed, what's in progress, and what's blocked across all production phases. Update it as work is completed.

## Maintenance Conventions

These rules apply to **every** Claude Code session working in this project. They override default behavior — keep CLAUDE.md and CHANGELOG.md trustworthy, or future sessions start from a wrong premise.

- **CHANGELOG.md — update on every change.** Whenever you add, modify, remove, refactor, or reorganize anything (code, docs, prompts, manifest, repo structure, conventions), append a CHANGELOG entry. Capture **what changed and why** so future sessions understand the rationale and don't undo intentional decisions. Date the entry. Group related changes under one heading. The CHANGELOG is the project's decision log — not a release-note tally.

- **CLAUDE.md — update on significant project changes.** When the project's structure, pipeline phases, conventions, source-of-truth documents, naming, or active phase shifts, update CLAUDE.md so it reflects the **current** state. CLAUDE.md is what every future session reads first; if it points at the wrong files or describes a stale architecture, the session starts wrong.
  - "Significant" = anything that changes how someone works on the project: new pipeline phase, new directory layout, new source-of-truth doc, new tools/dependencies, document moves, new conventions.
  - Routine code edits, single-file content tweaks, small bug fixes do NOT require a CLAUDE.md update — only a CHANGELOG entry.

- **Archive convention — `COMPLETED/` and `OLD/` subfolders.** Within `docs/` and `prompts/`, completed (shipped, done) and old (superseded) artifacts live in `COMPLETED/` and `OLD/` subdirectories respectively. The roots stay focused on what's active. When you finish a phase or supersede a doc, move it into the correct archive folder rather than leaving it in the root. Use `git mv` so renames are tracked.

## Source of Truth Documents

| Document | Path | Role |
|----------|------|------|
| **Production Checklist** | `docs/production-checklist.md` | **Check first every session** — current status of all phases, frames, and assets |
| Storyboard | `docs/pencil-test-storyboard.md` | Complete production storyboard — 7 beats, 2 acts, frame counts, key pose descriptions |
| Keyframe Prompts (Act 1, archived) | `docs/COMPLETED/act1-keyframe-prompts.md` | 6 Gemini prompts that produced the Act 1 key poses (Act 1 hero loop has shipped — kept for re-runs) |
| A-2 Anchor | `images/2D-Character-Sketch-Sean-v1.png` | Identity reference — all generated frames must match this character |
| Manifest | `manifest.yaml` | Pipeline configuration — single source of truth for generation, audit, and export settings |
| Seedance Research | `docs/research/seedance-research-findings.md` | Seedance 2.0 capabilities, API specs, prompting guide, style preservation strategies |
| **Seedance Prompt Template (v4)** | `prompts/seedance-template-v4.md` | **Canonical Seedance 2.0 prompt template — copy/fill for every new shot.** Locked 2026-05-10 from a 9-variant bake-off. Use Fast tier as the production default. Also packaged as the portable `seedance-prompting` skill at `~/.claude/skills/seedance-prompting/SKILL.md` (auto-loads in any project). Supersedes v3 (`docs/2026-05-02-act2-seedance-prompts-v3-conversation-style.md`). |
| **Act 2 Seedance Shot List** | `docs/act2-seedance-shot-list.md` | **Current source of truth for Act 2 Seedance work.** 10 clips + 4 holds, anchor frame paths, draft Seedance prompts, fallback strategies (Round 3 deliverable, 2026-04-26) |
| **Act 2 Seedance Execution Plan** | `docs/2026-04-27-act2-seedance-execution-plan.md` | **Approved 12-task implementation plan for the Seedance generation phase.** New scripts (`seedance_generate.py`, `seedance_extract.py`, `seedance_cleanup.py`, `seedance_audit.py`, `seedance_assemble.sh`, `seedance_lib.py`), tiered NB2 cleanup, Procreate gate, two-milestone delivery (rough cut → full-fidelity cut). Pick this up to start execution. |
| Round 2 Beat Decisions | `runs/act2-exploration/concepts/round2-decisions.md` | Locked Act 2 11-beat sheet (transition pick, revelation pick, panorama pick) — feeds the Act 2 shot list |
| Seedance Production Plan (archived) | `docs/OLD/seedance-production-plan.md` | ⚠️ **SUPERSEDED for Act 2** by `act2-seedance-shot-list.md`. Act 1 sections still valid as historical reference. |
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
├── docs/                             # Active source-of-truth documents
│   ├── pencil-test-storyboard.md
│   ├── act2-seedance-shot-list.md            # Current Act 2 spec
│   ├── 2026-04-27-act2-seedance-execution-plan.md  # Current Act 2 plan
│   ├── production-checklist.md
│   ├── Sprite-Sheet-Automation-Project_OG-Workflow-Summary.md
│   ├── research/                     # External research notes (Seedance findings, query packets)
│   ├── COMPLETED/                    # Shipped/done plans + prompts (e.g. Act 1)
│   └── OLD/                          # Superseded docs (do not act on)
├── prompts/                          # Active prompts only
│   ├── act2/                         # Current Act 2 prompts
│   ├── COMPLETED/                    # Shipped Act 1 prompts, in-betweens, completed handoffs
│   └── OLD/                          # Superseded handoffs / session prompts
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

1. **Attempt 1:** Original prompt from `docs/COMPLETED/act1-keyframe-prompts.md`
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
- **For all new shots, use the v4 template at `prompts/seedance-template-v4.md`.** Fill the `[BRACKETED]` placeholders; do not modify the structural scaffolding. Run at Fast tier as the production default.
- See `docs/research/seedance-research-findings.md` for full prompting guide

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

Active Act 2 prompts live under `prompts/act2/`. Shipped Act 1 keyframe + transition + sprite prompts are archived at `prompts/COMPLETED/F{##}.txt` (e.g. `prompts/COMPLETED/F06.txt`) — extracted from `docs/COMPLETED/act1-keyframe-prompts.md`.

`pipeline/generate.py` auto-loads `prompts/F{##}.txt` first, then falls back to `prompts/COMPLETED/F{##}.txt`. Override with `--prompt "..."` or `--prompt-file path.txt`.

## Engine Truth

> If the loop plays smoothly at 12fps and the character is recognizably Sean in pencil test style on cream animation paper, it ships.

This is the project's north star — adapted from the original sprite pipeline's "if it plays cleanly in Phaser, it ships." The final animation in its target medium (browser GIF/WebM loop) is the ultimate arbiter of quality.
