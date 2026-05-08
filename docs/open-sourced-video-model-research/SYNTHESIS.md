# Open-Source Video Model Research — Synthesis

**Status:** Reference document for **post-portfolio-project testing**. Current production pipeline stays on **NB2 + Seedance 2.0** through portfolio completion.

**Sources synthesized:**
- [Perplexity Deep Research](Open-Source-Video-Generation-Models-for-Local-ComfyUI-Use-2D-animation-perplexity.md)
- [Gemini Deep Research](Open-Source-Video-Models-for-ComfyUI-Gemini.md)

---

## Top-Line Consensus

Both reports independently converge on the same top tier. High-confidence signal.

| Model | Perplexity rank | Gemini rank | Consensus role |
|---|---|---|---|
| **Wan 2.2 (14B) FLF2V** | #1 | #1 | Primary test target — closest open-source equivalent to Seedance 2.0 for start+end frame interpolation |
| **LTX-Video (13B full / 2.3)** | #4 | #2 | Speed king; best Mac option via MLX; but **variant choice matters a lot** (see disagreements) |
| **FramePack / FramePack F1** | #6 | #3 | Best for long holds and identity preservation; start+end via merged PR |
| **HunyuanVideo 1.5** | #3 | #4 | Best photoreal motion, but **both reports warn against it for pencil-test style** |

---

## Where the Reports Disagree (and which to trust)

### 1. LTX-Video's suitability for 2D/pencil-test style

- **Perplexity:** LTX-Video 13B is *the strongest* recommendation for 2D preservation. Cites a March 2025 r/StableDiffusion thread showing LTXV 0.9.5+ preserves 2D digital art and watercolor without photoreal drift.
- **Gemini:** LTX-2.3 **Distilled** washes out high-frequency detail (pencil strokes, cross-hatching) because distilled inference takes large latent steps that smooth over micro-texture.

**Resolution:** These aren't contradictions — they're about different variants.
- ✅ Test **LTX-Video 13B (non-distilled, 0.9.7+)** for pencil-test work.
- ❌ Avoid **LTX-2.3 Distilled** for anything where line-weight and cross-hatching must survive.

### 2. "Wan 3.0" and "Happy Horse 1.0"

Gemini cites both as current/imminent. Perplexity doesn't mention either.

- **Wan 3.0** — Gemini treats it as shipping alongside 2.2. Perplexity only has 2.1/2.2 plus a "Wan 2.5 preview" (API-only, no weights). **Treat Wan 3.0 as unverified / possibly a 2.5→3.0 slip.** Default to **Wan 2.2 14B FLF2V** which both reports confirm.
- **Happy Horse 1.0** — Gemini flags it itself as *not yet weight-released*. Ignore until an actual HuggingFace repo appears.

### 3. LTX end-frame (FLF) support

- **Perplexity:** confirmed via official node pack + March 2026 YouTube tutorial for LTX 2.3 I2V first+last frame.
- **Gemini:** confirms but notes Wan's dedicated FLF2V cross-attention is more robust against anatomical hallucination.

**Resolution:** For first+last frame work, **Wan 2.2 FLF2V is the default**; LTX is the fast-iteration alternative when hallucination risk is low (slow motion, small delta between start/end).

### 4. Mac Silicon story

- **Perplexity:** LTXV and FramePack are the most viable; Wan 2.2 on MPS is "20–40+ min per clip" on MacBook Pro.
- **Gemini:** LTX-2.3 via **MLX (james-see/ltx-video-mac)** bypasses PyTorch MPS bottlenecks entirely — the clear Mac winner.

**Both agree:** Mac is for light iteration; Alienware is the production rig. The MLX path Gemini names is a real repo worth testing.

---

## Agreed Points (use these as production truth when testing begins)

1. **Wan 2.2 14B FLF2V** is the open-source answer to Seedance 2.0's first-and-last-frame interpolation. Uses Apache 2.0, has Day-0 ComfyUI native support, runs fp8 on 24GB VRAM in ~3–6 min per 5s 720p clip.
2. **HunyuanVideo 1.5 is hostile to pencil-test aesthetic.** Both reports independently say it pulls hard toward photoreal. Skip for style-critical work regardless of its motion quality.
3. **FramePack is the identity-persistence tool.** Not a motion-quality competitor — it's what you use when a pose must hold for 10–30s without the character drifting.
4. **AnimateDiff (SDXL) is obsolete for new work** — only relevant if you have a specific SDXL LoRA capturing a style no DiT model can yet replicate.
5. **Step-Video-TI2V (30B) is impractical** on single consumer GPUs (80GB+). Research-only.

---

## Post-Project Test Plan (when portfolio ships)

### Phase 1 — Baseline test (1 week)
Test these three on identical start+end frame pairs from your approved NB2 keyframes:

| # | Model | Hardware | Expected role |
|---|---|---|---|
| 1 | **Wan 2.2 14B FLF2V** (fp8, kijai wrapper) | Alienware | Seedance 2.0 replacement |
| 2 | **LTX-Video 13B** (non-distilled) | Alienware + MacBook (MLX) | Fast-iteration tier |
| 3 | **FramePack F1** (kijai wrapper) | Alienware | Long-hold / identity-lock tier |

**Evaluation criteria (match your existing QA gates):**
- Does it honor the end frame? (Seedance's strength — don't regress)
- Does it preserve pencil-test aesthetic? (the real test; closed-source models don't)
- Identity drift over 5s? (CC01–CC08 continuity checks from the existing pipeline)
- Minutes-per-clip on the Alienware? (vs. Seedance API latency)

### Phase 2 — Style lock-in (2 weeks)
If Wan 2.2 or LTX-13B passes baseline, train a **pencil-test LoRA** on your approved F01–F40 frames. Wan's High-Noise / Low-Noise dual-LoRA mechanism is non-trivial — budget a week for that alone (Gemini calls this out specifically).

### Phase 3 — Watch list
Re-check these every ~6 weeks:
- **Wan 2.5 / possible 3.0** open-weight release (Perplexity: "Q2 2026 watch")
- **LTX-2** full (non-distilled) Mac MLX support maturation
- **Wan 2.2 Animate 14B** (character-animation fine-tune, Dec 2025) — most directly relevant to animation-specific work

---

## Cost Calculus (why this matters post-project)

Current Seedance 2.0 API: paid per clip, ~5s at 720p.
Wan 2.2 FLF2V local on 4090: electricity only, ~4–6 min per clip.

At >~20 clips/week, the break-even tips toward local. For a pencil-test *series* (not just this one portfolio piece), Wan 2.2 + a pencil-test LoRA is the durable pipeline.

---

## Source Repositories (bookmark now for later)

- kijai/ComfyUI-WanVideoWrapper — https://github.com/kijai/ComfyUI-WanVideoWrapper
- Wan 2.2 FLF2V official workflow — https://www.comfy.org/workflows/video_wan2_2_14B_flf2v-7016f027bcf1/
- Lightricks/ComfyUI-LTXVideo — https://github.com/Lightricks/ComfyUI-LTXVideo
- james-see/ltx-video-mac (MLX Mac build) — https://github.com/james-see/ltx-video-mac
- lllyasviel/FramePack PR #167 (start+end frame) — https://github.com/lllyasviel/FramePack/pull/167
- Kijai/WanVideo_comfy_GGUF (quants) — https://huggingface.co/Kijai/WanVideo_comfy_GGUF

---

## Research Hygiene Notes

- **Gemini hallucination risk:** it cites "Wan 3.0" and "Happy Horse 1.0" with confidence; Perplexity doesn't. When the two reports disagree on *existence* of a model, trust the more conservative source and verify at the HuggingFace / GitHub primary before committing.
- **Both reports are dated April 2026.** Re-run this research before Phase 1 testing if that's >2 months out — this space moves fast.
