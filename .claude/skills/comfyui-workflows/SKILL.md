---
name: comfyui-workflows
description: ComfyUI workflow design, debugging, and automation for image generation, with focus on OpenPose ControlNet in-between generation for the Pencil Test animation pipeline. Covers workflow JSON structure, node wiring (KSampler, LoRA, ControlNet, IPAdapter), API queuing and polling, OpenPose pose extraction and interpolation, pencil test style generation, video model node integration, and batch generation. Use when asked about "ComfyUI workflow", "ComfyUI nodes", "LoRA setup", "ControlNet workflow", "OpenPose in-betweens", "animation in-between generation", "ComfyUI API", or "batch generate frames".
---

# ComfyUI Workflows

## Purpose

Design, debug, and automate ComfyUI workflows for image generation, with specialized support for generating animation in-between frames using OpenPose ControlNet guided by approved keyframe poses. Covers the workflow JSON format, common node patterns, API integration, and the complete OpenPose in-between generation pipeline for the Pencil Test project.

## When to Use

- Building or modifying a ComfyUI workflow
- Generating in-between frames from approved pencil test keyframes using OpenPose ControlNet
- Adding LoRA, ControlNet, or IPAdapter to an existing workflow
- Debugging a workflow that produces bad results or errors
- Automating batch generation via the ComfyUI API
- Integrating video model nodes (VHS, Wan 2.2) for frame interpolation
- Setting up IPAdapter for identity reference with the A-2 anchor

## Examples

**Example 1: Generate In-Between Frames with OpenPose**
```
User: "Generate in-between frames between F06 and F10 using OpenPose"
Claude: [Uses comfyui-workflows]

Step 1: Extract pose skeletons
  LoadImage (PT_A1_F06_key.png) -> DWPoseEstimation -> SaveImage (skeleton_F06.png)
  LoadImage (PT_A1_F10_key.png) -> DWPoseEstimation -> SaveImage (skeleton_F10.png)

Step 2: Interpolate 1 intermediate pose (50% blend)
  ImageBlend (skeleton_F06, skeleton_F10, blend=0.5) -> SaveImage (skeleton_F06to10_IB01.png)

Step 3: Generate in-between frame
  Workflow: openpose_inbetween.json
  - ControlNet: OpenPose with interpolated skeleton (strength: 0.9)
  - IPAdapter: A-2 anchor for identity lock (weight: 0.65)
  - Prompt: Pencil Animation Style Cluster
  - Negative: "vector lines, solid black, cel shading, anime, digital art"

Step 4: Audit output
  python3 pipeline/audit.py --run-dir runs/{run_id} --frame F06toF10_IB01 --attempt 1
```

**Example 2: Debug Poor Generation Quality**
```
User: "My ComfyUI outputs look blurry and washed out"
Claude: [Uses comfyui-workflows]

Common causes and fixes:

1. CFG too low -> Increase from 4-5 to 7-8
2. Steps too few -> Increase from 15 to 25-30
3. Wrong sampler -> Switch from ddim to euler_ancestral for SDXL
4. VAE mismatch -> Ensure SDXL uses sdxl_vae.safetensors (not SD 1.5 VAE)
5. Resolution wrong -> SDXL needs 1024x1024 base (not 512x512)

Let me check your workflow JSON for these issues...
```

**Example 3: Batch Generate with API**
```
User: "Generate 20 character poses with different seeds"
Claude: [Uses comfyui-workflows]

python3 scripts/comfyui_batch.py \
  --workflow workflows/character_pose_lora.json \
  --prompt "standing hero character, front view, white background" \
  --count 20 \
  --seed-start 1000 \
  --output assets/characters/hero/

Queuing 20 jobs... [--------------------] 20/20
All jobs complete. Output: assets/characters/hero/pose_1000-1019.png
```

## Workflow JSON Structure

ComfyUI workflows are JSON objects where each key is a node ID and each value defines the node.

```json
{
  "1": {
    "class_type": "CheckpointLoaderSimple",
    "inputs": {
      "ckpt_name": "sd_xl_base_1.0.safetensors"
    }
  },
  "2": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "a hero character, standing pose, white background",
      "clip": ["1", 1]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "blurry, deformed, ugly, text, watermark",
      "clip": ["1", 1]
    }
  },
  "4": {
    "class_type": "KSampler",
    "inputs": {
      "seed": 42,
      "steps": 25,
      "cfg": 7.0,
      "sampler_name": "euler_ancestral",
      "scheduler": "normal",
      "denoise": 1.0,
      "model": ["1", 0],
      "positive": ["2", 0],
      "negative": ["3", 0],
      "latent_image": ["5", 0]
    }
  },
  "5": {
    "class_type": "EmptyLatentImage",
    "inputs": {
      "width": 1024,
      "height": 1024,
      "batch_size": 1
    }
  },
  "6": {
    "class_type": "VAEDecode",
    "inputs": {
      "samples": ["4", 0],
      "vae": ["1", 2]
    }
  },
  "7": {
    "class_type": "SaveImage",
    "inputs": {
      "filename_prefix": "character",
      "images": ["6", 0]
    }
  }
}
```

**Key concepts:**
- Node connections use `["node_id", output_index]` format
- `output_index` 0 = first output, 1 = second, etc.
- CheckpointLoaderSimple outputs: [0]=MODEL, [1]=CLIP, [2]=VAE

## Common Node Patterns

### Base Pattern: Text-to-Image

```
CheckpointLoader -> CLIPTextEncode (pos) -> KSampler -> VAEDecode -> SaveImage
                 -> CLIPTextEncode (neg) /
                 -> EmptyLatentImage    /
```

### LoRA Pattern

Insert between CheckpointLoader and CLIPTextEncode:

```
CheckpointLoader -> LoraLoader -> CLIPTextEncode -> KSampler
```

```json
{
  "class_type": "LoraLoader",
  "inputs": {
    "lora_name": "style_v2.safetensors",
    "strength_model": 0.8,
    "strength_clip": 0.8,
    "model": ["1", 0],
    "clip": ["1", 1]
  }
}
```

**LoRA weight guidelines:**
| Weight | Effect |
|:-------|:-------|
| 0.5-0.6 | Subtle influence, maintains base model character |
| 0.7-0.85 | Strong style transfer, good balance (recommended) |
| 0.9-1.0 | Dominant, can overfit or produce artifacts |
| >1.0 | Experimental, often produces distortion |

### ControlNet Pattern

Add ControlNet conditioning to guide composition:

```
ControlNetLoader -> ControlNetApply -> KSampler
LoadImage (guide) /
```

```json
{
  "class_type": "ControlNetApplyAdvanced",
  "inputs": {
    "strength": 0.85,
    "start_percent": 0.0,
    "end_percent": 1.0,
    "positive": ["2", 0],
    "negative": ["3", 0],
    "control_net": ["cn_loader", 0],
    "image": ["guide_image", 0]
  }
}
```

**ControlNet models by use case:**
| Model | Input | Use Case | Pipeline Role |
|:------|:------|:---------|:-------------|
| control_v11p_sd15_canny | Edge map | Precise outlines | Style refinement pass |
| control_v11p_sd15_lineart | Line drawing | Clean lineart guidance | Alternative for pencil style |
| control_v11p_sd15_openpose | Pose skeleton | Character posing | **PRIMARY -- in-between generation** |
| control_v11f1p_sd15_depth | Depth map | Composition/perspective | Background generation |
| t2i-adapter_diffusers_xl_canny | Edge map (SDXL) | SDXL edge control | SDXL alternative |
| t2i-adapter_diffusers_xl_openpose | Pose skeleton (SDXL) | SDXL character posing | SDXL in-between alternative |

### IPAdapter Pattern (Style Reference)

Use an image as a style reference (instead of text prompt):

```
IPAdapterModelLoader -> IPAdapter -> KSampler
CLIPVisionLoader    /
LoadImage (ref)     /
```

### Upscale Pattern (Hi-Res Fix)

Two-pass generation for higher quality:

```
KSampler (base) -> LatentUpscale -> KSampler (refine, denoise=0.4) -> VAEDecode
```

## API Integration

### Queue, Poll, and Retrieve

```bash
# Queue a job
curl -s -X POST http://127.0.0.1:8188/prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": <workflow_json>}'
# Response: {"prompt_id": "abc-123-def"}

# Poll for completion (returns job details when complete, empty when processing)
curl -s http://127.0.0.1:8188/history/abc-123-def

# Images saved to ComfyUI/output/{prefix}_{counter}.png
```

### Batch Generation Script

```python
#!/usr/bin/env python3
"""Batch queue ComfyUI workflows with varying seeds."""
import json
import requests
import time
import sys

COMFYUI_URL = "http://127.0.0.1:8188"

def queue_batch(workflow_path, prompt_text, count, seed_start, output_prefix):
    with open(workflow_path) as f:
        workflow = json.load(f)

    jobs = []
    for i in range(count):
        seed = seed_start + i
        # Inject prompt and seed
        for node_id, node in workflow.items():
            if node.get("class_type") == "CLIPTextEncode" and "positive" in str(node):
                node["inputs"]["text"] = prompt_text
            if node.get("class_type") == "KSampler":
                node["inputs"]["seed"] = seed
            if node.get("class_type") == "SaveImage":
                node["inputs"]["filename_prefix"] = f"{output_prefix}_{seed}"

        resp = requests.post(f"{COMFYUI_URL}/prompt", json={"prompt": workflow})
        resp.raise_for_status()
        jobs.append(resp.json()["prompt_id"])
        print(f"Queued {i+1}/{count} (seed={seed})")

    # Poll all jobs
    for job_id in jobs:
        while True:
            resp = requests.get(f"{COMFYUI_URL}/history/{job_id}")
            if resp.ok and job_id in resp.json():
                break
            time.sleep(2)

    print(f"All {count} jobs complete.")
```

## Model Management

### Directory Structure

Models: `ComfyUI/models/{checkpoints,loras,controlnet,vae,clip_vision,ipadapter}/`
Custom nodes: `ComfyUI/custom_nodes/` | Input: `ComfyUI/input/` | Output: `ComfyUI/output/`

### Recommended Base Models

| Model | Size | Best For |
|:------|:-----|:---------|
| sd_xl_base_1.0 | 6.9 GB | General SDXL generation |
| sdxl_turbo | 6.9 GB | Fast SDXL (4 steps) |
| sd_v1-5 | 4.3 GB | SD 1.5 workflows, more LoRA support |
| animagine-xl-3.1 | 6.9 GB | Anime/illustration style |

### Pencil Test Model Selection

For the pencil test pipeline, the base model should produce:
- Soft, grainy line work (not vector-clean)
- Warm cream paper texture capability
- Good ControlNet compatibility for OpenPose

Recommended: sd_xl_base_1.0 or animagine-xl-3.1 with a pencil-texture LoRA.
SD 1.5 has better ControlNet ecosystem but lower resolution baseline.
Consider training a custom LoRA on the A-2 anchor and approved keyframes for style consistency.

## Debugging Workflows

| Symptom | Likely Cause | Fix |
|:--------|:------------|:----|
| Black image | VAE mismatch or missing connection | Check VAE is connected to VAEDecode |
| Blurry/washed out | CFG too low or steps too few | Increase cfg to 7-8, steps to 25+ |
| Wrong resolution | SDXL at 512x512 | SDXL needs 1024x1024 base |
| Style not applied | LoRA weight too low or wrong model | Increase weight, verify model compatibility |
| Artifacts/distortion | LoRA weight too high | Reduce to 0.7-0.8 |
| ControlNet ignored | Strength too low or wrong model | Increase strength, verify CN model matches base |
| "Node not found" error | Missing custom node | Install via ComfyUI Manager |
| OOM (out of memory) | Resolution too high or batch too large | Reduce resolution or batch_size to 1 |

## OpenPose In-Between Workflow

Generate animation in-between frames by interpolating OpenPose skeletons between approved keyframes and using ControlNet to generate frames matching the interpolated poses in pencil test style.

### Step 1: Extract Pose Skeletons

Use the DWPose preprocessor node to extract pose data from approved keyframes:

```
Node graph:
  LoadImage (keyframe) -> DWPoseEstimation -> SaveImage (skeleton)
```

Run this on each approved keyframe pair boundary (F06, F10, F13, F18, F31, F36).

### Step 2: Interpolate Poses

For N in-betweens between two keyframes:
- Linear blend: `pose_n = ImageBlend(pose_A, pose_B, blend_factor=n/(N+1))`
- For arced motion (per 2d-animation-principles), apply ease curves to the blend factor rather than linear interpolation
- Example: F06->F10 needs 0-1 in-betweens (fast snap), F13->F18 needs 2-3 (large arc)

See `2d-animation-principles` references/pencil-test-timing-map.md for per-transition in-between budget.

### Step 3: Generate In-Between Frame

Node graph:
```
CheckpointLoader -> LoraLoader (pencil_style) -> CLIPTextEncode (style cluster)
                                               -> CLIPTextEncode (negatives)
ControlNetLoader (openpose) -> ControlNetApplyAdvanced
LoadImage (interpolated_skeleton) /
IPAdapterModelLoader -> IPAdapter
CLIPVisionLoader /
LoadImage (A-2 anchor) /
                         \ KSampler -> VAEDecode -> SaveImage
```

Key settings:
- **ControlNet strength:** 0.85-0.95 (high -- pose must match skeleton)
- **ControlNet end_percent:** 0.8 (allow creative freedom in final denoising steps)
- **IPAdapter weight:** 0.6-0.7 (identity reference, not style override)
- **Prompt:** Full Pencil Animation Style Cluster from pencil-animation-prompt-templates.md
- **Negative:** "vector lines, solid black ink, cel shading, anime, digital art, gradient shading, pure white background, saturated colors"
- **Resolution:** 1920x1080 (match keyframe resolution)
- **Steps:** 25-30
- **CFG:** 7.0-7.5

### Step 4: Audit In-Between

Run audit.py on each generated in-between:
- HF01 (aspect ratio): PIL check -- must be 16:9
- HF05 (aesthetic): Must maintain pencil test look
- SF01 (style drift): Line weight must match keyframes
- SF02 (identity drift): Face must match A-2
- SF03 (proportion drift): Body proportions consistent

Output naming: `PT_A1_F{start}toF{end}_IB{n}.png`
Example: `PT_A1_F06toF10_IB01.png`

## Video Model Node Integration

ComfyUI custom nodes for video model-based frame interpolation (alternative to OpenPose for subtle transitions):

### VHS (Video Helper Suite)

Nodes for loading/saving video sequences:
- `VHS_LoadVideo` -- Load approved keyframe pairs as start/end frames
- `VHS_VideoCombine` -- Combine generated frame sequences
- `VHS_SplitFrames` -- Extract individual frames from video output

### ComfyUI-WanVideoWrapper (Wan 2.2)

Custom node for Wan 2.2 video generation:
- `WanVideoGenerate` -- img2vid with start_frame + end_frame
- Best for subtle transitions (F06->F10 head tilt, F31->F36 nod)
- Output: short video clip, extract frames with VHS_SplitFrames

### Frame Extraction Pipeline

After video model generates interpolation:
```
VHS_LoadVideo -> VHS_SplitFrames -> [per-frame SaveImage] -> audit.py
```

### When to Use Video Models vs OpenPose

| Transition | Recommended | Reason |
|:-----------|:-----------|:-------|
| F01->F06 (subtle head tilt) | Video model | Small motion, smooth result |
| F06->F10 (head snap) | Neither or 1 manual | Snap effect, minimal in-betweens |
| F13->F18 (arm sweep) | OpenPose ControlNet | Large motion, need pose control |
| F31->F36 (nod) | Video model | Subtle motion, identity preservation |

For the full per-transition decision matrix, see `shared/references/pencil-test-pipeline-context.md`.

## Integration with Pencil Test Pipeline

### Input

- Approved keyframes from `runs/{run_id}/approved/`
- A-2 anchor image (`images/2D-Character-Sketch-Sean-v1.png`) for IPAdapter identity lock
- Manifest.yaml for frame numbers and hold durations

### Output

- In-between frames saved to `runs/{run_id}/candidates/inbetweens/`
- Naming: `PT_A1_F{start}toF{end}_IB{n}.png`
- Each in-between goes through the same audit.py pipeline as keyframes

### Batch In-Between Generation

Adapt the batch generation script to iterate over keyframe pairs from manifest.yaml:
1. Read `generation_chains` from manifest
2. For each consecutive pair in a chain, determine in-between count from timing map
3. Extract pose skeletons from both keyframes
4. Interpolate N intermediate poses
5. Queue ComfyUI workflow for each interpolated pose
6. Run audit.py on each output

## Success Criteria

- [ ] Workflow JSON is valid and all node connections resolve
- [ ] OpenPose skeleton extraction produces clean pose data from approved keyframes
- [ ] Interpolated poses blend smoothly between keyframe skeletons
- [ ] Generated in-betweens maintain pencil test aesthetic (SF01 check)
- [ ] Identity preserved across all in-betweens (SF02 check via IPAdapter)
- [ ] API queuing and polling work reliably
- [ ] Output naming follows `PT_A1_F{start}toF{end}_IB{n}.png` convention

## Related Skills

| Skill | Relationship |
|:------|:------------|
| `animation-pipeline` | Orchestrates the pipeline that consumes ComfyUI in-between output |
| `2d-animation-principles` | Provides timing/spacing rules for in-between count and easing curves |
| `gemini-pencil-animation-image-gen` | Primary keyframe generator (ComfyUI handles in-betweens) |
| `creative-director` | Reviews generated in-betweens for quality (Phase E QA) |
| `video-animation-production` | Assembles frames with FFmpeg after ComfyUI generation |

## Copy/Paste Ready

```
"Generate in-betweens for F06->F10 using OpenPose"
"Build a ComfyUI workflow for pencil test in-betweens"
"Extract pose skeletons from approved keyframes"
"Add IPAdapter identity lock with A-2 anchor"
"Debug this ComfyUI workflow -- output is [problem]"
"Set up video model nodes for frame interpolation"
"Batch generate in-betweens for all Chain 1 transitions"
```
