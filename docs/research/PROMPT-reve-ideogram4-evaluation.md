# Coworker Session Prompt — Evaluate Reve + Ideogram4 for anima

> Paste everything below the line into a fresh Cowork session with the `anima` folder connected.
> It is written to be self-contained.

---

You are evaluating two newly-released image models for possible adoption into **anima**, my 2D-animation pipeline. I need a rigorous, cited research report. **Use the `deep-research` skill** to run this — fan out across sources, fetch primary docs, adversarially verify claims, and synthesize. This is **desk research only**: read docs, pricing, benchmarks, GitHub, license files, and community reports. **Do not make paid API calls or spin up local inference** — instead, hand me a concrete test plan I can run myself afterward.

## Step 0 — Load anima's context first

Before researching anything external, read these so your evaluation is grounded in how anima actually works:

- `/Users/seanwinslow/Code-Brain/anima/CLAUDE.md` — especially the **Cy (character_designer)** and **Em (vision_critic)** skill-map rows, the **layer-ownership map**, the **Draft → Pro escalation** section, the **Character Bible primitive**, and the **QA gates** (HF01–HF05 / SF01–SF05).
- `/Users/seanwinslow/Code-Brain/anima/PHILOSOPHY.md` — the intent.
- `/Users/seanwinslow/Code-Brain/anima/docs/pipeline-architecture-v1.md` — the 10-phase spec, focus on **Phase 5 Generate** and **Phase 6 Motion**.
- `/Users/seanwinslow/Code-Brain/anima/docs/research/2026-05-30-nb2-editing-character-consistency-template.md` — the current NB2 editing template + the five-slot prompt emitter and six closed style registers.

**Key facts you must hold onto from that context:**
- Today's incumbent **image-editing engine is NB2 = `gemini-3.1-flash-image-preview`** (called via `invoke_image_edit`). Cy uses it to generate/edit every character-Bible plate; NB Pro is reserved for painterly finals only.
- NB Pro was *demoted* because of a **multi-reference downsampling regression** — when given several reference images it downsamples and loses identity. NB2 holds identity better, is ~½ the cost, ~4× faster. **Any candidate model must be judged against this same multi-reference behavior.**
- anima's quality bars that matter for editing: **SF02 identity drift** (face/hair/jaw must match the anchor), **SF01 style drift** (line weight, construction lines), **six closed style registers** (the production work is in a "pencil-test-colored" register), **16:9 aspect**, and per-character `IR.*` rules.
- The pipeline already runs a **Tier C batch route on this same Alienware** (`gemma4_26b` via Ollama at `192.168.68.201:11434`, exposed through `hybrid_router.py`, **Pattern-E-gated**: the box is manually woken and reachable ~7am–5pm only, remote wake is impossible). This is the architectural precedent for any local image node — read how it's wired before proposing integration.

## The two models

### 1. Reve (closed-source, API)
- Edit API docs: https://api.reve.com/console/e1502091-288d-454a-9244-809a32a9fece/docs/edit
- Remix API docs: https://api.reve.com/console/e1502091-288d-454a-9244-809a32a9fece/docs/remix
- These console URLs may be auth-gated and show only partial public docs — if so, **flag that explicitly** and fall back to Reve's public marketing site, pricing page, model cards, and third-party coverage. Don't fabricate spec values you can't source.

### 2. Ideogram4 (claimed open-source)
- Repo: https://github.com/ideogram-oss/ideogram4.git
- **⚠️ Authenticity is suspect and is your first task.** Ideogram the company has historically shipped a *closed, commercial* model with no open weights. An `ideogram-oss/ideogram4` repo does not obviously correspond to an official release. **Before evaluating capabilities, verify provenance:** Who owns the org? Is it affiliated with Ideogram Inc. or a community reimplementation / name-squat? Are real model weights published (HF link, size, hash) or is it just scaffolding? What's the **license** (commercial use allowed? redistribution? output ownership)? Any **safety red flags** (obfuscated install scripts, telemetry, unsigned binaries, suspicious dependencies)? If it's not a credible, safe, properly-licensed release, say so plainly and stop the local-feasibility work — a verdict of "do not run this" is a valid and valuable outcome.

## What I need answered

Organize the report around these. Lead with the editing-focused criteria — that's the decision driver.

**A. Image editing + character consistency (primary lens).** For each model, assess: instruction-based **image editing** quality (inpaint / localized edit / global restyle), **identity hold across edits** (does a character stay itself after an edit), **multi-reference support** (and whether it suffers NB2-Pro-style downsampling), **prompt adherence on edits**, max resolution, supported aspect ratios, and how it handles a consistent character across many poses/expressions. Map each finding to anima's bars: **SF02 identity**, **SF01 style**, **16:9**, **register fidelity**. Judge specifically for my two use cases: **(1) keyframes** (hero poses that must nail identity) and **(2) in-betweens** (frames generated between two approved anchors — consistency and speed matter most here).

**B. Cost.** Establish the **baseline** = current NB2 (`gemini-3.1-flash-image-preview`) per-image cost (find Google's current published price; note anima treats Gemini-API editing as the default). Then for **Reve**, get current API pricing per edit/generation and model a realistic anima monthly volume (Bible authoring + keyframes + in-betweens across acts). For **Ideogram4 local**, cost is electricity + my time — estimate it and compare. Output a **side-by-side cost table** with a clear "are we saving money, and at what volume does it break even" answer.

**C. Local feasibility + integration plan for Ideogram4** (only if Step-0 authenticity passes). My hardware for local inference is the **Alienware Aurora** (the only CUDA box I own):
- GPU: **NVIDIA RTX 5080, 16GB GDDR7** (Blackwell, sm_120 — verify current PyTorch/CUDA wheel support for 50-series, this has been a real pain point)
- CPU: Intel Core Ultra 9 285 (24-core) · RAM: **64GB DDR5** · Storage: 1TB NVMe · OS: **Windows 11**
- (Macs — M4 Pro MBP 48GB, M4 Pro Mac Mini 24GB — cannot run CUDA; note if there's any MPS/GGUF path but assume Alienware is the host.)

Answer: Does Ideogram4 fit in **16GB VRAM**? At what precision (fp16/bf16/fp8/int4) and via what runtime (diffusers, ComfyUI, native)? What **quantization** is needed and what's the quality cost? Realistic **seconds-per-image** estimate on a 5080. Then — assuming it runs — give a **concrete integration plan** to expose it as a networked anima node, modeled on the existing **Tier C Alienware route** (`hybrid_router.py`, Ollama-style HTTP endpoint, `fallback="none"` cost-safety, **Pattern-E availability gating**). Be honest about whether the 7am–5pm manual-wake constraint makes it viable as anything more than a batch/experimental node.

**D. Fit verdict.** For each model and each of {keyframe generation, in-between generation, Cy Bible editing}: **adopt / supplement / pass**, with rationale. Call out anything else relevant to anima — output licensing/ownership for a public portfolio piece, watermarking, content filters that might block the pencil-test style, latency, rate limits, API stability.

## Deliverable

Write a cited markdown report to **`/Users/seanwinslow/Code-Brain/anima/docs/research/2026-06-07-reve-ideogram4-evaluation.md`** with:
1. **TL;DR recommendation** (3–5 sentences: adopt/supplement/pass for each, and the headline cost answer).
2. A **decision table** (model × use-case × verdict × cost-vs-NB2).
3. Sections A–D above, every external claim carrying an inline source link.
4. An **"Authenticity & safety" callout box** for Ideogram4 up top.
5. A **hands-on test protocol** I can run next (specific prompts using my Sean anchor + a known multi-reference edit, the exact comparisons to make against NB2, and what "pass" looks like for SF01/SF02).
6. An **open-questions** list for anything you couldn't source.

Follow anima's `CHANGELOG.md` convention — add a dated entry noting the research doc was created and why. Be skeptical, cite everything, and don't paper over gaps — an honest "couldn't verify" beats a confident guess.
