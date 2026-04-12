# Kimodo Motion Pipeline — Setup Guide & Status

**Created:** 2026-04-12
**Status:** Llama 3 access APPROVED 2026-04-12. Ready to run.

---

## What We're Doing

Using [Kimodo](https://github.com/nv-tlabs/kimodo) (NVIDIA's motion diffusion model) to generate physically accurate 3D motion sequences from text prompts and sparse keyframe constraints. The motion gets exported as BVH, rendered flat in Blender, and fed to NB2 as pose reference for pencil-test frame generation.

### The Full Workflow

```
1. Kimodo generates 3D motion from text + keyframe constraints
2. Export as BVH
3. Blender imports BVH, renders orthographic frames at 12fps (pipeline/blender_render_bvh.py)
4. Each rendered frame + A-2 reference → NB2 → pencil-test drawing
5. Existing audit pipeline (Phase C-E) handles QA, assembly, export
```

### Proof of Concept (VALIDATED 2026-04-12)

Three 3D mannequin poses were successfully converted to pencil-test style via NB2:
- `runs/pose_reference_test/thinking_pose.png` — hand on chin, contemplative
- `runs/pose_reference_test/waving_pose.png` — wide stance, arm raised
- `runs/pose_reference_test/fighting_pose.png` — boxing guard stance

All three maintained character identity, pencil-test style, and pose accuracy. No 3D aesthetic bleedthrough.

---

## RunPod Setup (What We Did)

### Pod Configuration

| Setting | Value |
|---------|-------|
| GPU | RTX 3090 (24GB VRAM) |
| Template | Runpod Pytorch 2.4.0 (`runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04`) |
| Pod name | `kimodo-motion` |
| Container disk | 30 GB |
| Storage | Network volume (persists across pod terminations) |
| HTTP ports | 8080, 8888 |
| TCP ports | 22 |
| Pricing | On-Demand $0.46/hr |

### Installation Commands (In Order)

The install hit several build issues. Here's the **working sequence** that avoids all of them:

```bash
# 1. Navigate to workspace
cd /workspace

# 2. Clone Kimodo
git clone https://github.com/nv-tlabs/kimodo.git
cd kimodo

# 3. Install cmake and Python dev headers FIRST (required for C extension build)
apt-get update && apt-get install -y cmake python3.11-dev

# 4. Install all dependencies WITHOUT building the C extension
#    The MotionCorrection C extension fails due to CMake finding the wrong Python.
#    It's only used for foot-skate cleanup and is NOT needed for generation + BVH export.
pip install hydra-core omegaconf scipy "transformers==5.1.0" urllib3 boto3 peft einops \
  tqdm pydantic "filelock>=3.20.3" "gradio>=6.8.0" gradio_client trimesh scenepic pillow \
  "av>=16.1.0" bvhio "viser @ git+https://github.com/nv-tlabs/kimodo-viser.git" \
  numpy accelerate

# 5. Add Kimodo to Python path
export PYTHONPATH=/workspace/kimodo:$PYTHONPATH

# 6. Log into Hugging Face (required for Llama 3 text encoder)
hf auth login
# Paste your HF token when prompted

# 7. Verify installation
python -c "from kimodo.demo import app; print('Kimodo ready')"
```

### Build Issues We Hit (And Solutions)

| Issue | Error | Solution |
|-------|-------|----------|
| Missing CMake | `FileNotFoundError: cmake` | `apt-get install -y cmake` |
| Wrong Python found by CMake | `Could NOT find Python3 (missing: Python3_INCLUDE_DIRS)` found 3.10 instead of 3.11 | `apt-get install -y python3.11-dev` |
| `--no-build-isolation` broke viser | `ModuleNotFoundError: No module named 'hatchling'` | Don't use `--no-build-isolation` |
| C extension still fails | CMake `FindPython3` insists on system Python 3.10 | **Skip it.** Install deps separately without building kimodo as a package. The MotionCorrection extension is optional (foot-skate cleanup only). |
| Wrong directory | `Directory '.[demo]' is not installable` | Must be in `/workspace/kimodo`, not `/workspace` |

### What `pip install ".[demo]"` SHOULD Do (If Build Worked)

The "correct" install builds a C++ extension called MotionCorrection via CMake. It fails because RunPod's container has Python 3.10 system-wide and Python 3.11 in the pip environment, and CMake's FindPython3 picks up 3.10. This is a container packaging issue, not a Kimodo bug. The workaround (install deps separately) works because the MotionCorrection module is only used for optional post-processing.

---

## Current Blockers

### Blocker 1: Llama 3 Model Access (PENDING)

Kimodo's text encoder uses [Meta-Llama-3-8B-Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct), which is a **gated model** requiring Meta's approval.

**Status:** Access requested and APPROVED 2026-04-12.

**To check:** Go to https://huggingface.co/settings/gated-repos — when it changes from "PENDING" to "APPROVED", you're good.

**What to do once approved:**
1. Start the RunPod pod (or create a new one with the same setup)
2. Run the install commands above
3. Run the generate command:
```bash
export PYTHONPATH=/workspace/kimodo:$PYTHONPATH
python -m kimodo.scripts.generate \
  "person standing relaxed, looks down at hand, then looks up with surprise and excitement" \
  --model Kimodo-SOMA-RP-v1 \
  --duration 3.5 \
  --bvh \
  --output /workspace/act1_test \
  --seed 42
```

**First run will download ~16GB** of Llama 3 weights. Subsequent runs use cache.

### Blocker 2: RunPod Cost While Waiting

Pod was terminated to avoid burning $0.46/hr while Llama access is pending. Network volume persists but container disk (with installed packages) does not. Reinstall needed on next pod creation.

---

## Can the Alienware Run Kimodo Locally?

### Alienware Specs

| Component | Spec |
|-----------|------|
| GPU | NVIDIA RTX 5080 **16GB** GDDR7 |
| CPU | Intel Core Ultra 9 285 (24-core, 76MB cache) |
| RAM | 64GB DDR5 5200 MT/s |
| Storage | 1TB NVMe M.2 PCIe SSD |
| OS | Windows (assumed) |

### VRAM Assessment

Kimodo needs **~17GB VRAM** primarily for the text encoder (Llama-3-8B loaded via LLM2Vec). Your RTX 5080 has **16GB** — 1GB short.

**Options to make it work on the Alienware:**

1. **CPU offload the text encoder** — Encode text on CPU (slow but works with 64GB RAM), run diffusion on GPU. Kimodo may support this via `accelerate` device_map. Would need to test.

2. **Quantize the text encoder** — Load Llama-3-8B in 4-bit or 8-bit quantization. Cuts VRAM roughly in half. Requires modifying Kimodo's LLM2Vec wrapper to pass `load_in_4bit=True`.

3. **Use the remote text encoder** — Kimodo has a `run_text_encoder_server.py` script. You could run the text encoder on CPU as a separate process, and the main model on GPU.

4. **Generate on RunPod, render locally** — Use the cloud GPU only for the ~30 minutes of motion generation, export BVH, then do all Blender rendering and NB2 generation locally. This is the simplest option.

**Recommendation:** Option 4 is the path of least resistance. The Alienware is overkill for Blender rendering and NB2 generation — those don't need heavy GPU. Use RunPod ($1-2 total) for the one step that needs 24GB VRAM.

If you want to try running Kimodo locally anyway, we can attempt it with CPU offloading (option 1) since you have 64GB RAM, which is plenty for the text encoder. But it'll be slower for the text encoding step.

---

## Generate Command Reference

### Single motion
```bash
python -m kimodo.scripts.generate \
  "your text prompt here" \
  --model Kimodo-SOMA-RP-v1 \
  --duration 3.5 \
  --bvh \
  --output /workspace/output_name \
  --seed 42
```

### Multi-prompt sequence (different actions chained)
```bash
python -m kimodo.scripts.generate \
  "person looks down at hand. person looks up with surprise. person raises arm in a sweeping gesture" \
  --model Kimodo-SOMA-RP-v1 \
  --duration "1.0 1.5 1.5" \
  --bvh \
  --output /workspace/act1_full \
  --seed 42
```

### Key flags
| Flag | Purpose |
|------|---------|
| `--model Kimodo-SOMA-RP-v1` | SOMA skeleton (77 joints, BVH export supported) |
| `--duration 3.5` | Length in seconds |
| `--bvh` | Export BVH alongside NPZ |
| `--output` | Output file stem (creates .npz and .bvh) |
| `--seed` | Reproducible results |
| `--constraints` | Path to saved constraint JSON from viser demo |
| `--no-postprocess` | Skip foot-skate cleanup (we're skipping the C extension anyway) |

### Interactive demo (viser web UI)
```bash
python -m kimodo.demo.app --host 0.0.0.0 --port 8080
```
Access via RunPod's HTTP proxy URL: `https://{pod-id}-8080.proxy.runpod.net`

---

## Prompt Engineering

### What works

- **Start with "A person..."** — aligned with training data. Variations like "An old person...", "A drunk person...", "A child..." modulate style.
- **7-20 words, 1-2 behaviors per prompt.** Medium detail. Don't describe each body part; don't be too vague.
- **Each prompt must be self-contained.** In multi-prompt mode, don't reference previous actions. Instead of "then the person stops" say "a person carrying a box comes to a stop."
- **Action verbs, not emotions.** "A person raises both arms overhead and waves" works. "A person feels excited" doesn't produce visible motion.

### What the model knows (training data coverage)

- Locomotion (walk, run, jog, stride, backward walk)
- Gestures (wave, point, shrug)
- Everyday activities (pick up, set down, sit, stand)
- Object interactions (carry, push, pull)
- Stylized movement (tired, angry, happy, sad, scared, drunk, injured, stealthy)
- Dancing
- Videogame-style combat

### What it doesn't know

- Sports-specific actions (baseball swing, tennis serve)
- Highly specialized/technical motions outside mocap training data
- Facial expressions or finger articulation (separate from body motion)

### Prompt examples from the repo

| Prompt | Duration |
|--------|----------|
| "A person walks forward while carrying a box" | 5.2s |
| "A person sets a box down onto the ground" | 4.1s |
| "A person walks diagonally to the left and waves at someone on their right" | 5.0s |
| "A person walking forward picks up something off the ground" | 5.0s |
| "Initially standing still and calm, the person then starts jogging in a counterclockwise arc" | 6.0s |

### Why our Test Run 1 prompt failed

Our prompt was: *"person standing relaxed, slowly looks down at something in their right hand. person quickly snaps head up with surprise and excitement, eyebrows raise"*

Problems:
1. **Two sentences = multi-prompt mode.** The period split it into two prompts, but we only passed one duration (3.5s). This likely caused the model to allocate ~1.75s per prompt — too short for each.
2. **"looks down" and "eyebrows raise" are subtle actions.** Not enough body movement for the model to produce visible skeleton changes.
3. **"excitement" is an emotion, not an action.** No visible body motion maps to "excitement" in the training data.
4. **Missing "A person" prefix.** Our prompts started with "person" instead.

---

## Classifier-Free Guidance (CFG)

CFG controls how strongly the model follows text and/or constraints. This is the **only lever for motion expressiveness**.

### Separated CFG (default, recommended)

```bash
python -m kimodo.scripts.generate \
  "A person raises both arms overhead" \
  --cfg_type separated --cfg_weight 2.5 1.5 \
  --model Kimodo-SOMA-RP-v1.1 --duration 3.0 --bvh \
  --output /workspace/test
```

Two weights: `[text_weight, constraint_weight]`
- **Higher text weight** → more dramatic interpretation of the prompt
- **Higher constraint weight** → stricter adherence to spatial constraints
- Default range: 1.0-2.5 for both
- Try `--cfg_weight 3.0 1.0` for maximum prompt expressiveness with no constraints

### Regular CFG

```bash
--cfg_type regular --cfg_weight 2.5
```
Single weight that increases adherence to both text and constraints together.

### No CFG (fastest, most random)

```bash
--cfg_type nocfg
```

---

## Constraint System

The viser UI lets you author 5 types of constraints, saved as JSON and passed via `--constraints`:

| Type | What it controls | Use case |
|------|-----------------|----------|
| **Root 2D Waypoints** | Ground-plane XZ positions | Path the character walks |
| **Root 2D Paths** | Dense ground-plane trajectory | Precise locomotion paths |
| **Full-Body Keyframes** | All joint positions at specific frames | Pin exact poses at exact times |
| **End-Effector Constraints** | Individual hand/foot positions + rotations | "Right hand reaches here at frame 30" |
| **Foot Contacts** | Heel/toe contact patterns | Grounding (model-supported, not yet in UI) |

### Using constraints

1. Run the interactive demo: `python -m kimodo.demo.app --host 0.0.0.0 --port 8080`
2. Use the viser UI to pose the character and add constraints at specific frames
3. Click "Save Constraints" to export JSON
4. Pass to CLI: `--constraints /path/to/constraints.json`

### Constraint limits

- Max ~20 keyframes per constraint type
- Conflicting constraints (pinned feet + "jump" prompt) cause artifacts
- Post-processing smoothly adjusts motion to hit constraints exactly

### Coordinate space

- Y-up, meters
- Ground plane = XZ
- Character starts at XZ=(0,0) at frame 0
- Hip height ~0.9m for standing

---

## Multi-Prompt Mode

Chain distinct actions by separating prompts with periods and matching durations:

```bash
python -m kimodo.scripts.generate \
  "A person walks forward while carrying a box. A person sets a box down onto the ground." \
  --duration "3.5 4.1" \
  --model Kimodo-SOMA-RP-v1.1 --bvh \
  --output /workspace/multi_test
```

### How transitions work

- Prompts separated by periods in the text string
- Each duration (space-separated) maps to one prompt
- **Number of durations must match number of prompts**
- The second motion is conditioned on the last N frames of the first (default: 5 transition frames via `--num_transition_frames`)
- Second prompt "spends" some of its time transitioning — less effective time for new content
- Each prompt must have full context (don't reference previous prompts)

---

## Model Variants

| Model | Data | Notes |
|-------|------|-------|
| **Kimodo-SOMA-RP-v1.1** | 700 hrs commercial mocap | **Best available.** Updated Apr 10, 2026 |
| Kimodo-SOMA-RP-v1 | 700 hrs commercial mocap | Original release (what we tested) |
| Kimodo-SOMA-SEED-v1.1 | 288 hrs public data | Public data only, lower quality |
| Kimodo-SOMA-SEED-v1 | 288 hrs public data | Original public release |
| Kimodo-SMPLX-RP-v1 | 700 hrs commercial mocap | 22-joint SMPL-X skeleton (body+hands+face) |
| Kimodo-G1-RP-v1 | 700 hrs commercial mocap | Unitree G1 robot skeleton (34 joints) |
| Kimodo-G1-SEED-v1 | 288 hrs public data | Robot on public data |

**We should use `Kimodo-SOMA-RP-v1.1`** — same skeleton as v1 but improved quality.

---

## Duration and Frame Rate

- **Fixed 30 FPS** throughout
- `num_frames = int(duration_seconds * 30)`
- **Maximum: 10 seconds per prompt** (300 frames)
- Our test: 3.5s should produce 105 frames. We got 210 frames (7s) — the period in our prompt split it into two prompts, each getting 3.5s.

---

## Known Limitations

- **Max 10 seconds per prompt** (chain multi-prompt for longer)
- **Max ~20 constraints per type**
- **No amplitude/temperature control** — CFG is the only expressiveness lever
- **Foot skating possible** — post-processing helps but isn't perfect
- **Training bias** — no sports, no out-of-distribution specialized actions
- **Multi-prompt transition overhead** — second prompt loses time to blending
- **Head/face motion is body-level only** — no eyebrow, jaw, or eye animation in SOMA skeleton

---

## Storyboard → Kimodo Prompt Mapping (Revised)

Based on prompt engineering research, here are revised prompts using proper formatting:

| Beat | Kimodo Prompt | Duration | Notes |
|------|---------------|----------|-------|
| Beat 1 (combined) | "A person standing still slowly looks down at their right hand, then quickly snaps their head up with wide eyes" | 3.5s | Single prompt, avoid period split |
| Beat 2 | "A person raises their right arm and sweeps it in a wide confident arc from left to right" | 2.0s | Action verb, clear direction |
| Beat 3 | "A person turns their head to look over their left shoulder and gives a small satisfied nod" | 2.0s | Combined turn + nod |
| Beat 3b | "A person slowly returns to a relaxed standing position" | 1.5s | Simple return-to-idle |

### Multi-prompt version (for full Act 1 sequence)
```bash
python -m kimodo.scripts.generate \
  "A person standing still slowly looks down at their right hand, then quickly snaps their head up. A person raises their right arm and sweeps it in a wide confident arc from left to right. A person turns their head to look over their left shoulder and nods" \
  --duration "3.5 2.0 2.0" \
  --model Kimodo-SOMA-RP-v1.1 \
  --cfg_type separated --cfg_weight 3.0 1.0 \
  --bvh \
  --output /workspace/act1_full \
  --seed 42
```

### Next test plan
1. **Test with v1.1 model** (improved quality over v1)
2. **Use high text CFG** (`--cfg_weight 3.0 1.0`) for maximum prompt expressiveness
3. **Try extreme action first** — "A person jumps high into the air" to verify amplitude ceiling
4. **Try the viser demo** for visual constraint authoring — pin start/end poses
5. **Compare single vs multi-prompt** for the same action sequence

---

## Test Run 1 — Results (2026-04-12)

### What we ran
- **Prompt:** "person standing relaxed, slowly looks down at something in their right hand. person quickly snaps head up with surprise and excitement, eyebrows raise"
- **Model:** Kimodo-SOMA-RP-v1
- **Duration:** 3.5s (actual output: 210 frames at 30fps = 7s — model generated longer than requested)
- **Seed:** 42
- **Flags:** `--bvh --no-postprocess`
- **RunPod cost:** ~$0.46/hr × ~30 min = ~$0.23 (plus ~$0.50 idle during install/download)

### BVH output
- File: `runs/kimodo_motion/act1_beat1_test.bvh` (478KB)
- SOMA skeleton: 78 joints (full body including individual fingers, eyes, jaw)
- 210 frames at 30fps

### Motion quality assessment
- **Subtle to a fault.** The "look down" and "snap up" motions are barely perceptible in the skeleton preview. The figure mostly stands still with very minor upper body shifts.
- **No dramatic pose changes.** The prompt described sudden, expressive motion (snap up, eyebrows raise) but the output is gentle, ambient idle motion.
- **Physically accurate but boring.** Gravity, weight, and balance are correct — it looks natural. But "natural subtle idle" is not what we asked for.

### Verdict
The pipeline works end-to-end (generate → download → render → preview) but the motion output was not worth generating pencil-test frames from. **No NB2 frames generated from this test.**

### Questions for next test
1. Does Kimodo respond better to shorter, more extreme prompts? ("person jumps" vs long descriptive sentences)
2. Does the `--constraints` flag (keyframe constraints from viser UI) give more control?
3. Does multi-prompt mode (`--duration "1.0 1.5"`) help segment distinct actions?
4. Is SOMA-RP-v1 the right model for expressive motion, or is there a more dynamic variant?
5. What's the actual relationship between `--duration` and output frame count? (requested 3.5s, got 7s)

---

## Blender BVH Rendering — What We Learned

### The problem
BVH files contain only bone hierarchy and animation data — no mesh geometry. Blender imports BVH as an armature (skeleton), but armature display modes (stick, wire, etc.) are **viewport overlays** that don't appear in rendered output.

### Approaches tried and failed

| Approach | Engine | Result |
|----------|--------|--------|
| Armature display: STICK | EEVEE | Invisible — overlays don't render |
| Armature display: STICK | Workbench | Invisible in background mode — overlays still viewport-only |
| Skin modifier on edge mesh | Workbench | Visible but created triangular webbing at branching joints (fingers, spine) |
| Skin modifier with thin radius | Workbench | Better but still messy at branch points |

### Additional issues
- **Blender 5.1 renamed `BLENDER_EEVEE_NEXT` to `BLENDER_EEVEE`** — the render engine constant changed between versions
- **SOMA skeleton uses centimeter units** — bone offsets range 5-100, so camera presets designed for meter-scale scenes were wildly wrong
- **Auto-framing unreliable** — bounding box calculation for bone-only armatures gave inconsistent ortho_scale values

### What worked: PIL-based 2D renderer
Bypassed Blender entirely. `pipeline/render_bvh_2d.py` uses `bvhio` to parse the BVH, implements forward kinematics with `pyglm` quaternions, and projects 3D joint positions to 2D using PIL.

- **Coordinate system:** BVH uses Y-up. Projection maps X→screen X, Y→screen Y (negated).
- **View presets:** front, side, front-3/4 (30° rotation combining X and Z)
- **Joint filtering:** Skips finger bones, eye/jaw end-sites for cleaner stick figures
- **Joint emphasis:** Head and Hips get larger dots for landmark visibility
- **Output:** Green-screen background, dark gray bones/joints, configurable line width and joint radius

### Render command
```bash
python3 pipeline/render_bvh_2d.py \
  --bvh runs/kimodo_motion/act1_beat1_test.bvh \
  --output-dir runs/kimodo_motion/pose_frames/ \
  --fps 12 --view front-3/4 --background green
```

### Dependencies
```bash
pip install bvhio Pillow  # bvhio pulls in pyglm, spatial-transform
```

### Blender script status
`pipeline/blender_render_bvh.py` still exists but is not reliable for BVH-only armatures. Kept for reference — could work if a mesh rig (FBX/GLTF) is imported instead of raw BVH.

---

## Files Created

| File | Purpose |
|------|---------|
| `pipeline/blender_render_bvh.py` | Blender BVH render script (unreliable for bone-only BVH — see notes above) |
| `pipeline/render_bvh_2d.py` | **Working** PIL-based 2D stick figure renderer for BVH files |
| `runs/kimodo_motion/act1_beat1_test.bvh` | Test run BVH output (Beat 1, 7s, subtle motion) |
| `runs/kimodo_motion/pose_frames/` | 105 rendered stick figure PNGs at 12fps |
| `runs/kimodo_motion/pose_preview.gif` | Preview animation (456KB, 8.75s) |
| `runs/pose_reference_test/*.png` | NB2 pose-from-reference proof of concept (3 test frames, earlier session) |
| `docs/kimodo-setup-guide.md` | This file |

---

## Decision: Is This Worth It?

### What Kimodo gives you
- Physically accurate motion (gravity, momentum, natural arcs, proper timing/spacing)
- Automatic in-betweens from sparse keyframes
- Text-based pose control — describe the motion, don't manually position every joint
- BVH export for any animation tool

### What it costs
- ~$1-2 on RunPod per full generation session
- Setup friction (gated models, build issues, cloud GPU management)
- Adds a pipeline step (Kimodo → render → NB2 instead of just NB2)

### What we learned from Test Run 1
- The pipeline works but Kimodo's text-to-motion may not produce expressive enough movement for animation key poses
- Subtle, physically-grounded idle motion is Kimodo's strength — dramatic acting poses may need the viser constraint UI or different prompting strategies
- The Blender rendering step was the biggest time sink; the PIL renderer is the right tool for this job
- **Need to research:** Kimodo's prompt engineering, constraint system, and model variants before next test

### The alternative (what's already working)
- Manually pose 3D mannequins for each key pose and in-between
- Feed directly to NB2 with A-2 reference
- No cloud GPU, no Llama access, no build issues
- Works right now, today, on your Mac

### Bottom line
Pipeline validated but motion quality needs investigation. Next test should use **extreme, dynamic prompts** (jumping, throwing, turning) to see if Kimodo can produce motion with enough amplitude for animation reference. The $29 remaining RunPod credit gives plenty of room for experimentation — research the model first, then run targeted tests.
