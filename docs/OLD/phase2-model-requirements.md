# Phase 2: Model Requirements — ComfyUI In-Between Generation

## Base Setup

- **ComfyUI:** v1.41.21 (Mac Desktop app)
- **Data directory:** `/Users/seanwinslow/Code-Brain/Comfy-UI`
- **Platform:** macOS Apple Silicon (MPS backend)
- **Base model:** Stable Diffusion 1.5 (chosen over SDXL for mature ControlNet support and lower memory)

## Required Models (~7.5 GB)

All files go into `/Users/seanwinslow/Code-Brain/Comfy-UI/models/`

| # | File | Directory | Size | Source |
|---|------|-----------|------|--------|
| 1 | `v1-5-pruned-emaonly.safetensors` | `checkpoints/` | 4.3 GB | `huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5` |
| 2 | `control_v11p_sd15_openpose.pth` | `controlnet/` | 1.45 GB | `huggingface.co/lllyasviel/ControlNet-v1-1` |
| 3 | `ip-adapter_sd15.safetensors` | `ipadapter/` | 44 MB | `huggingface.co/h94/IP-Adapter/models/` |
| 4 | `sd1.5_model.safetensors` (CLIP Vision ViT-H) | `clip_vision/` | 1.2 GB | `huggingface.co/h94/IP-Adapter/models/image_encoder/` |
| 5 | `vae-ft-mse-840000-ema-pruned.safetensors` | `vae/` | 335 MB | `huggingface.co/stabilityai/sd-vae-ft-mse` |

## Required Custom Nodes

Install via ComfyUI Manager (launch app → Manager → Install):

| Node Pack | Author | Provides | Auto-downloads |
|-----------|--------|----------|---------------|
| `comfyui_controlnet_aux` | Fannovel16 | DWPose skeleton extraction | ~350 MB (pose models on first use) |
| `ComfyUI_IPAdapter_plus` | cubiq | IPAdapter identity lock nodes | None (models downloaded above) |

## Optional (Add If Needed)

| File | When to add | Size |
|------|-------------|------|
| Pencil-sketch LoRA (e.g., `pencil_sketch_v2.safetensors`) | If pencil test style doesn't hold with prompt alone | 50-200 MB |
| `ComfyUI-Impact-Pack` custom node | If batch processing utilities are needed | ~10 MB |

## Generation Settings

| Parameter | Value | Notes |
|-----------|-------|-------|
| Resolution (generate) | 768×432 | SD 1.5 extended, 16:9 |
| Resolution (output) | 1376×768 | Lanczos upscale to match keyframes |
| ControlNet strength | 0.90 | High — pose must match skeleton |
| ControlNet end_percent | 0.85 | Allow creative freedom in final steps |
| IPAdapter weight | 0.65 | Identity reference, not style override |
| Steps | 28 | |
| CFG | 7.5 | |
| Sampler | euler_ancestral | |
| Scheduler | normal | |

## Workflow Files

| Workflow | Purpose | Location |
|----------|---------|----------|
| `skeleton_extract.json` | Extract DWPose skeleton from keyframe | `workflows/` |
| `skeleton_blend.json` | Blend two skeletons at specified ratio | `workflows/` |
| `openpose_inbetween.json` | Generate in-between from interpolated skeleton | `workflows/` |
