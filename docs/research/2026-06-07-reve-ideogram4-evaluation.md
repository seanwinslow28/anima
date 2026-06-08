# Reve & Ideogram 4 — evaluation for anima's editing layer

*2026-06-07. Desk research only — no paid API calls, no local inference. Two newly-released image models came across the transom as possible adoptions into anima's editing layer (Phase 5 Generate, Phase 6 Motion cleanup, and Cy's Phase 2 Character Bible work). The incumbent they'd have to beat is **NB2** — `gemini-3.1-flash-image-preview`, called through `invoke_image_edit` — which holds identity better, costs half, and runs ~4× faster than NB Pro for exactly the editing work Cy does ([anima's own NB2 editing doc](2026-05-30-nb2-editing-character-consistency-template.md)). This report leads with the editing lens because that is the decision driver, then cost, then local feasibility, then a per-use-case verdict and a test protocol Sean can run next.*

*Sourcing note: every external claim carries an inline link. Two source classes are weaker than I'd like and are flagged in place — (1) Reve's first-party **console docs** at `api.reve.com/console/.../docs/{edit,remix}` are a client-rendered, account-scoped SPA that returns only a meta-shell to a server-side fetch, so first-party API detail here leans on the **pricing screenshots Sean supplied** plus third-party API mirrors (Replicate, fal, AIMLAPI); (2) Reve's character-consistency quality is **vendor-and-reseller claimed, not independently benchmarked** — treated skeptically throughout.*

---

## ⚠️ Authenticity & safety callout — Ideogram 4

> **Verdict: authentic, safe to read, but its *license* and *shape* make it the wrong tool — not a fraud, a mismatch.**
>
> **Provenance — genuine Ideogram, Inc. release.** The `ideogram-oss/ideogram4` GitHub org is **not** a name-squat or community reimplementation. It interlocks with Ideogram's real corporate identity at four independent points: the weights live under the official **`ideogram-ai`** Hugging Face org ([nf4](https://huggingface.co/ideogram-ai/ideogram-4-nf4), [fp8](https://huggingface.co/ideogram-ai/ideogram-4-fp8)) with the official [Ideogram 4 collection](https://huggingface.co/collections/ideogram-ai/ideogram-4); the README cites the company blog at [ideogram.ai/blog/ideogram-4.0/](https://ideogram.ai/blog/ideogram-4.0/); the license is a coherent legal agreement naming **"Ideogram, Inc."**; and the repo's hiring link points to Ideogram's real [Ashby board](https://jobs.ashbyhq.com/ideogram). The `-oss` GitHub org / `-ai` HF org split is a normal corporate pattern, not a red flag. The "Ideogram historically ships closed" prior is correct but outdated — this is their **first** open-weight release, dated **2026-06-03** ([repo README](https://github.com/ideogram-oss/ideogram4), [ComfyUI day-0 post](https://blog.comfy.org/p/ideogram-4-day-0-support-in-comfyui)).
>
> **Weights are published and real.** 9.3B-param flow-matching DiT, fp8 and nf4 checkpoints, gated behind a click-through license on HF, Diffusers-integrated (`Ideogram4Pipeline`). Text encoder is [Qwen3-VL-8B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct) — a known, legitimate model.
>
> **No malware signals.** Install is standard `pip install .` from the cloned repo; no obfuscated scripts, no unsigned binaries, no suspicious telemetry in the documented path. Two caveats worth naming, neither disqualifying: the default inference path **phones home** to Ideogram's hosted "magic-prompt" API (`IDEOGRAM_API_KEY`) to expand prompts, and optionally to [Hive](https://thehive.ai/) for safety moderation — both are documented and swappable for self-hosted equivalents, but it means "local inference" is not air-gapped out of the box.
>
> **The two facts that disqualify it for anima:**
> 1. **License — Non-Commercial only.** The weights ship under the [Ideogram 4 Non-Commercial Model Agreement](https://github.com/ideogram-oss/ideogram4/blob/main/model_licenses/LICENSE-IDEOGRAM-4-NON-COMMERCIAL) (the inference *code* is separately Apache-2.0 — [evolink summary](https://evolink.ai/blog/ideogram-4-0-what-developers-should-know)). "Non-Commercial Purposes" explicitly excludes *"generating Output to include in, or to advertise or promote, revenue-generating products or services."* anima's output feeds a **job-hunt portfolio** whose entire purpose is professional/commercial advantage — that is squarely outside the grant, or at best a gray zone no one should bet a public portfolio on without a paid commercial license.
> 2. **Shape — it's text-to-image, not an editor.** Every capability the model documents is T2I: structured-JSON prompts, bounding-box layout, color-palette conditioning, best-in-class text rendering. The Diffusers usage is `pipe(prompt)` — no image input, no reference conditioning, no inpaint, no identity-preserving edit. anima's job is **editing** (image + instruction → image) and **multi-reference identity hold**. There is no documented native path for either in the open release.

---

## 1. TL;DR recommendation

**Reve — supplement (pilot it), don't yet adopt.** Reve is the right *shape*: a genuine instruction-editing + multi-reference remix model (closed API), 16:9 native, up to 6 references first-party, ~2K resolution, with full commercial rights and user-owned outputs ([Reve API License](https://app.reve.com/terms/api), [Replicate/reve](https://replicate.com/reve/remix)). On cost it is the headline win — Reve's cheap "Fast" tier runs **~$0.007/edit** against NB2's **~$0.067/image at 1024px**, roughly a **10× per-image saving**, independently corroborated at the bulk level (~$667 vs ~$6,700 per 100k images, [Atlas Cloud benchmark](https://www.atlascloud.ai/blog/guides/2026-ai-image-api-benchmark-gpt-image-2-vs-nano-banana-2-pro-vs-seedream-5-0)). The reason it's "supplement, not adopt" is that the **one thing that demoted NB Pro — multi-reference downsampling / identity loss — is exactly the thing no independent source has measured on Reve.** Its consistency claims are vendor marketing. Pilot it head-to-head against NB2 on the Sean anchor before trusting it with identity-critical keyframes.

**Ideogram 4 — pass, on all three use cases.** Authentic and well-engineered, but non-commercial-licensed and text-to-image only, with no editing or reference-conditioning path. Even setting the license aside, it cannot do Cy's job. And the local-inference dream runs into a wall: the 9.3B DiT plus its 8B Qwen3-VL text encoder is officially a **24GB-class** model — marginal-to-infeasible on the RTX 5080's 16GB without aggressive text-encoder GGUF offload, on top of the RTX 50-series (Blackwell `sm_120`) PyTorch-wheel friction that is still not in stable builds ([pytorch#164342](https://github.com/pytorch/pytorch/issues/164342)).

**Headline cost answer.** Reve is *strictly* cheaper per image than NB2 at every tier, so there's no break-even crossover — the question is absolute scale, not a threshold. At anima's current hobby-scale volume the saving is real but modest (single-digit to low-tens of dollars per month); it only becomes material if still-frame in-between volume scales up. Ideogram 4 local would be near-zero marginal cost (electricity), but that number is irrelevant because it can't do the work and can't be licensed for it.

---

## 2. Decision table

| Model | Use case | Verdict | Cost vs NB2 (`gemini-3.1-flash-image-preview`) |
|---|---|---|---|
| **Reve** | Keyframe generation (identity-critical hero poses) | **Supplement — pilot, gate on identity test** | Edit/Remix ~$0.04, Fast ~$0.007 vs NB2 ~$0.067/1K → **~40–90% cheaper** |
| **Reve** | In-between generation (between two approved anchors; speed + consistency) | **Supplement — strongest fit; Fast tier is built for this** | Remix Fast ~$0.007 vs NB2 ~$0.067 → **~10× cheaper** |
| **Reve** | Cy Bible editing (Phase 2 plates) | **Supplement — promising, but multi-ref fidelity unproven** | Edit/Remix ~$0.04 vs NB2 ~$0.067 → **~40% cheaper** |
| **Ideogram 4** | Keyframe generation | **Pass** — no editing/identity-conditioning; non-commercial license | n/a (local ~$0; capability- and license-blocked) |
| **Ideogram 4** | In-between generation | **Pass** — T2I only, cannot interpolate between anchors | n/a |
| **Ideogram 4** | Cy Bible editing | **Pass** — cannot do image+instruction edits | n/a |

NB2 baseline: $60.00 / 1M image-output tokens → **~$0.045 (512px) / ~$0.067 (1024px) / ~$0.101 (2K)** per image; batch mode ~50% off ([Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing), [per-resolution breakdown](https://www.aifreeapi.com/en/posts/gemini-flash-image-generation-pricing)).

---

## A. Image editing + character consistency (primary lens)

This is the lens that decides everything, because editing is the whole job: Cy authors a Bible plate by handing a model the anchor and a one-line "same person, new angle/expression, keep the identity" instruction and reading back a plate — an *editing* operation, not text-to-image. anima's bars for that operation are **SF02** (identity: face/hair/jaw must match the anchor), **SF01** (style: line weight, construction lines, the closed `pencil-test-colored` register), **16:9**, and the per-character `IR.*` rules.

### Ideogram 4 — fails the lens on capability, before quality even matters

Ideogram 4 is a **text-to-image** model. The README and HF card document structured-JSON prompting, bounding-box layout, color-palette conditioning, and best-in-class in-image text rendering — and nothing else ([repo](https://github.com/ideogram-oss/ideogram4), [HF nf4 card](https://huggingface.co/ideogram-ai/ideogram-4-nf4)). The Diffusers entry point is `pipe(prompt).images[0]`: a prompt in, an image out, no image conditioning. There is **no documented inpaint, img2img, instruction-edit, or reference/identity path** in the open release. A handful of secondary write-ups gesture at "inpainting and reference workflows via ComfyUI," but that thread is thin and appears to conflate Ideogram's *hosted product* features with the *open weights* — I could not substantiate any native editing capability in the released checkpoints, and the architecture as described (a from-scratch generative DiT with a VLM text encoder) has no reference-conditioning branch ([model summary, repo](https://github.com/ideogram-oss/ideogram4)).

For anima this is dispositive. Cy can't edit with it, Phase 5 can't re-anchor keyframes with it, and Phase 6 can't clean up motion with it. Its genuine strength — typographic/layout/poster design with flawless text rendering — is orthogonal to anima's pencil-test character work. **Mapped to the bars: it cannot be evaluated on SF02 or SF01 at all, because it never sees the anchor.**

One honest aside: Ideogram 4 leads open-weight *text rendering* and *design* benchmarks (top open model on [Design Arena](https://www.designarena.ai/), #2 overall on Ideogram's internal eval behind GPT Image 2; the repo's [ContraLabs](https://contralabs.com/research) chart even shows it beating NB2 on typography preference). None of that is anima's job. Filed, not actioned.

### Reve — the right shape; consistency *claimed* strong, *not* independently proven

Reve is built for this lens. It exposes three relevant operations ([Reve console pricing](https://api.reve.com/console/pricing), screenshots; [Replicate](https://replicate.com/reve/remix), [fal](https://blog.fal.ai/reve-is-now-available-on-fal/)):

- **Edit** — one image + a natural-language instruction → one edited image. Conversational, "maintains full context across multiple edits ... without losing character consistency or composition" ([AIMLAPI reve-edit](https://aimlapi.com/models/reve-edit-image)). This is the direct NB2 `invoke_image_edit` analogue.
- **Remix** — **1–6 reference images** (first-party, per Sean's console screenshot) + a prompt → one composited image, with the model resolving "spatial relationships, proportions, and lighting direction across your reference images" ([Replicate reve/remix README](https://replicate.com/reve/remix)). This is the direct analogue to anima's multi-reference plates (anchor + turnaround + pose target) and the place the NB-Pro regression would show up if Reve shares it.
- **Test-time scaling** — spend more compute for a better image, priced as a multiple of base cost (screenshot). Conceptually anima's draft→pro escalation, baked into the model.

What maps cleanly to anima's bars from documented spec:

| anima bar | Reve evidence | Source |
|---|---|---|
| **16:9** | `aspect_ratio` enum includes `16:9` (also 9:16, 3:2, 2:3, 4:3, 3:4, 1:1); independent of resolution | [AIMLAPI Reve remix-edit schema](https://docs.aimlapi.com/api-references/image-models/reve/reve-remix-edit-image) |
| **Max resolution** | Native ~2048×2048, optional upscale to 4K (4096²); separate `upscale` op at ~$0.002/MP | [AIMLAPI reve-edit](https://aimlapi.com/models/reve-edit-image), console screenshot |
| **Multi-reference** | 1–6 refs first-party (1–4 via Replicate/AIMLAPI mirrors — note the discrepancy) | console screenshot vs [Replicate](https://replicate.com/reve/remix) / [AIMLAPI schema](https://docs.aimlapi.com/api-references/image-models/reve/reve-remix-edit-image) |
| **Prompt adherence** | Reve's consistent reputational strength is prompt adherence + text rendering; converts images to an "internal structured format" for spatial grounding | [Replicate README](https://replicate.com/reve/remix), [trilogy review](https://trilogyai.substack.com/p/reve-20s-innovation-in-image-generation) |
| **SF02 identity hold** | **Claimed** ("maintaining consistency when working with multiple references") — **no independent benchmark found** | vendor/reseller copy only |
| **SF01 style / register fidelity** | No register-level evidence either way; pencil-test register fidelity is untested | — |

The skeptic's read, which is the one that matters: the **multi-reference downsampling failure that demoted NB Pro** in anima — references aggressively downsampled, fine identity detail lost, generic output ([Google AI Dev Forum, the primary regression report](https://discuss.ai.google.dev/t/gemini-3-0-pro-image-preview-inconsistent-performance-with-multiple-reference-images-since-3-1-launch/128648)) — is a *structural risk for any multi-reference model*, and **no source I found has tested whether Reve suffers it.** Worse for the marketing claims: in the one place 2026 reviewers *did* rank reference-driven character consistency independently, the finding was that **GPT Image 2 > NB2** and that NB Pro's 14-image identity-lock is the genuinely strong option — Reve was not even in that comparison ([NB2 vs GPT Image 2 reviews](https://decrypt.co/366408/openai-gpt-image-2-vs-google-nano-banana-2-review)). So Reve's identity hold is an **open empirical question**, and it's precisely the question anima cares about most. That's why the verdict is *pilot*, not *adopt* — and why the test protocol in §5 is built around it.

**Use-case split:**
- **Keyframes (identity-critical):** highest bar, least proven. Reve must beat NB2 on SF02 head-to-head before it touches a hero pose. Pilot-gated.
- **In-betweens (consistency + speed between two approved anchors):** the *strongest* fit. This is exactly what Remix-between-two-references is for, the Fast tier makes it ~10× cheaper, and a mild identity wobble on an in-between is far less costly than on a keyframe. If Reve passes anywhere first, it's here.
- **Cy Bible plates:** promising — Edit/Remix is the NB2 analogue — but gated on the same multi-ref fidelity question, since Bible authoring leans on anchor + view-reference pairs.

---

## B. Cost

**Baseline — NB2 (`gemini-3.1-flash-image-preview`), the anima default.** Google prices Gemini image output at **$60.00 / 1M image-output tokens** ([Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing)). Per finished image that lands at roughly **$0.045 (512px) / $0.067 (1024px) / $0.101 (2K) / $0.151 (4K)**, with batch mode about 50% off (~$0.034 at 1K) ([per-resolution breakdown](https://www.aifreeapi.com/en/posts/gemini-flash-image-generation-pricing), [pricepertoken](https://pricepertoken.com/pricing-page/model/google-gemini-3-flash-preview)). Reference images fed into an edit cost input tokens — negligible, ~$0.0003 each. anima's editing work sits around the 1K tier, so **~$0.067/edit** is the honest baseline number; **~$0.10** if work moves to 2K.

**Reve — first-party console pricing** (from Sean's screenshots of `api.reve.com/console/pricing`; 1 credit ≈ $0.00133):

| Reve op | Credits | ~USD | anima analogue |
|---|---|---|---|
| Create (T2I) | 18 | $0.024 | (not anima's use) |
| **Edit** (1 img + instruction) | 30 | **$0.040** | NB2 single-ref edit |
| **Remix** (1–6 imgs + prompt) | 30 | **$0.040** | NB2 multi-ref plate |
| **Edit Fast** | 5 | **$0.007** | cheap iteration |
| **Remix Fast** | 5 | **$0.007** | in-between generation |
| Upscale | variable (2+) | ~$0.002/MP | post-process |
| removeBackground | variable (2+) | ~$0.002/MP | cutout/alpha |
| Test-time scaling | multiples of base | ~$0.01+ | draft→pro in-model |

Independent corroboration of the magnitude: a 2026 API benchmark puts Reve at **~$667 per 100,000 images** vs NB2-1K at **~$6,700** — the ~10× gap, from a non-Reve source ([Atlas Cloud](https://www.atlascloud.ai/blog/guides/2026-ai-image-api-benchmark-gpt-image-2-vs-nano-banana-2-pro-vs-seedream-5-0)).

**Ideogram 4 local — electricity + Sean's time.** The RTX 5080 board draws ~360W; an image at ~15–30s is ~0.0015–0.003 kWh ≈ **~$0.0003–0.0005/image** at typical rates — effectively free per unit. But that number is a mirage: the model is non-commercial-licensed and can't do editing, so the real cost is **setup labor** (Blackwell wheels + GGUF text-encoder offload, §C) against **zero usable output for anima's job**. Not a contender.

**Side-by-side at modeled anima volume.** Two months, deliberately bracketing:
- *Light* (~150 edits): Bible touch-ups + one act's keyframes with the retry ladder.
- *Heavy* (~600 edits): full Bible authoring + two acts of keyframes + still in-between batches.

| Engine | Per edit | Light (~150) | Heavy (~600) |
|---|---|---|---|
| NB2 @ 1024px | $0.067 | **$10.05** | **$40.20** |
| NB2 batch @ 1024px | $0.034 | $5.10 | $20.40 |
| Reve Edit/Remix (std) | $0.040 | $6.00 | $24.00 |
| **Reve Edit/Remix Fast** | $0.007 | **$1.05** | **$4.20** |
| Ideogram 4 local | ~$0.0004 | ~$0.06 | ~$0.24 |

**Are we saving money, and at what volume does it break even?** Reve is cheaper than NB2 *per image at every tier*, so there is **no break-even threshold to cross** — Reve wins on unit cost from image #1. What scales with volume is the *absolute* saving: ~$5/mo light, ~$36/mo heavy at the Fast tier vs NB2 standard. At anima's hobby-scale cadence that's a real but modest win — not the thing that justifies adoption on its own. The cost case becomes compelling only if (a) still-frame in-between volume climbs into the thousands/month, or (b) Reve's quality proves *at least as good* as NB2, at which point taking a 10× unit-cost cut for equal output is a clean yes. **Cost is a tailwind, not the decision; quality (§A) is the decision.**

---

## C. Local feasibility + integration plan — Ideogram 4

Sean asked for this conditionally — "only if Step-0 authenticity passes." Authenticity passed; **feasibility and license both fail**, so this section documents *why local is a dead end* rather than how to wire it. Worth recording so the question stays answered.

**Does it fit 16GB?** Officially, no — it's a 24GB-class model. The Model Zoo lists nf4 (CUDA, Diffusers-supported) and fp8, and the surrounding coverage is explicit that **the nf4 variant targets a single 24GB GPU** ([buildfastwithai](https://www.buildfastwithai.com/blogs/ideogram-4-open-weight-image-model), [HF nf4 card](https://huggingface.co/ideogram-ai/ideogram-4-nf4)). The reason is the text encoder: Ideogram 4 doesn't use a small T5/CLIP — it uses **Qwen3-VL-8B-Instruct**, a full 8B vision-language model, pulling hidden states from 13 layers. That encoder is a heavy VRAM tenant on its own, on top of the 9.3B DiT and 2K-resolution activations. The community is already chasing the obvious mitigation — GGUF-quantizing the text encoder to offload it — which is an open ask, not a solved path ([city96/ComfyUI-GGUF #452: "support qwen3vl_8b gguf (Ideogram-4) text encoder"](https://github.com/city96/ComfyUI-GGUF/issues/452); [Civitai "Ideogram 4 (LOW VRAM) — fp8/4"](https://civitai.com/models/2673990/ideogram-4-low-vram)).

**Realistic precision/runtime on a 5080:** nf4 (4-bit) DiT + a GGUF-quantized, CPU-offloaded text encoder + sequential offloading is the only plausible 16GB path, and even then 2K inference is unproven and slow; expect heavy offload-thrash and tens of seconds per image at best. 2K-specific VRAM isn't community-benchmarked yet. Quality cost of that quant stack is unmeasured.

**The Blackwell tax — verified, and it's real.** The RTX 5080 is `sm_120`, which **still isn't in stable PyTorch builds** as of 2026 — you're on nightly cu128/cu129 or a custom-compiled wheel ([pytorch#164342 "Official support for sm_120"](https://github.com/pytorch/pytorch/issues/164342); [PyTorch Forums: RTX 5080 incompatibility](https://discuss.pytorch.org/t/compatibility-issue-between-pytorch-and-nvidia-geforce-rtx-5080/222981); [community custom-build repo](https://github.com/kentstone84/pytorch-rtx5080-support)). That's hours of toolchain yak-shaving before the first image renders, on a model that still can't edit.

**The integration plan that *would* apply, if a future local *editing* model cleared these bars.** anima already has the precedent — the **Tier C Alienware route** in code-brain's `hybrid_router.py`: `gemma4_26b` on the same RTX-class box via an Ollama-style HTTP endpoint at `192.168.68.201:11434`, exposed as a `task_map` route with `fallback="none"` (an off-hours miss raises `RouteUnavailable` rather than silently failing over to a paid API — the cost-safety invariant), and **Pattern-E availability-gated**: the box is manually woken and reachable ~7am–5pm only, remote wake architecturally impossible. A local image node would mirror that exactly: a small HTTP inference server on the Alienware exposing an `invoke_image_edit`-compatible contract, registered as a draft-tier route with `fallback="none"`, gated to the same wake window. **And that's the honest ceiling: the 7am–5pm manual-wake constraint caps any local node at batch/experimental status** — it can never be the interactive default Cy reaches for mid-session, because half of Sean's working hours the box is asleep and remote wake doesn't exist. Tier C's own soak closeout reached the same conclusion: "no auto-consumer wired — manual/opt-in route." A local image node inherits that ceiling.

**Net:** even in the counterfactual where Ideogram 4 could edit and were commercially licensed, the 5080 makes it a marginal-VRAM, Blackwell-taxed, batch-only experiment. With the actual non-commercial + T2I-only reality, it's a no-go. **Recommendation: do not run this locally for anima.**

---

## D. Fit verdict + everything-else-relevant

| Model | Keyframe gen | In-between gen | Cy Bible editing |
|---|---|---|---|
| **Reve** | **Supplement** — pilot, gate on SF02 head-to-head vs NB2 | **Supplement** — best fit; Fast tier is built for it | **Supplement** — promising; gate on multi-ref fidelity |
| **Ideogram 4** | **Pass** | **Pass** | **Pass** |

**Reve, the things beyond quality and cost that bear on anima:**
- **Licensing / output ownership — green, and a real edge over Ideogram 4.** Reve grants full commercial rights with **user-owned outputs**, reportedly even on the free tier ([Reve API License Agreement](https://app.reve.com/terms/api); reseller summaries concur). For a public job-hunt portfolio that is exactly the posture anima needs — the opposite of Ideogram 4's non-commercial wall. (Standard caveat in the terms: outputs may not be unique and aren't warranted free of third-party IP — boilerplate, not a blocker.)
- **Watermarking — unverified, flag before adoption.** No source confirms whether Reve API outputs carry a *visible* watermark or only invisible C2PA/Content-Credentials metadata. Invisible C2PA wouldn't hurt a portfolio; a visible mark would. **Must confirm on the first real API call** (inspect a returned image + its metadata).
- **Content filters — low risk.** Reve enforces a Usage Policy and moderates ([terms](https://app.reve.com/terms/api)); the pencil-test register is benign subject matter, so false-positive blocking is unlikely. Worth a single confirmatory run, not a worry.
- **API stability — caution: it's beta.** The console literally titles itself "Reve API (beta)." Treat schema and pricing as moving targets, and don't make Reve a hard dependency of any pipeline phase until it's GA. Wrap it behind the same `fallback`-aware routing anima uses elsewhere so an outage degrades to NB2, never to a dead node.
- **Rate limits / latency — unconfirmed first-party.** The Edit/Remix **Fast vs standard** split implies a latency tier (Fast = lower latency, lower cost), but exact per-key rate limits and p50 latencies aren't in any source I found; the third-party mirrors (Replicate, fal, AIMLAPI) impose their *own* limits that wouldn't apply to direct first-party use. Measure during the pilot.
- **First-party vs third-party divergence — pick one and pin it.** First-party Reve advertises up to **6** references; the Replicate/AIMLAPI mirrors cap at **4** and add their own pricing margins. For anima, go **first-party** (`api.reve.com`) to get the 6-ref ceiling and the real prices — the mirrors are useful for reading the API schema, not for production.

**Ideogram 4** — covered in the callout and §A/§C. Net: authentic, safe, genuinely good at design/typography, and entirely wrong for anima on license (non-commercial) and shape (T2I, no editing). Keep it on the radar *only* if Ideogram later ships an open **editing/reference** variant under a commercial license — that would change the analysis, nothing short of it does.

---

## 5. Hands-on test protocol (run this next)

The goal is one decision: **does Reve hold Sean's identity under a real multi-reference edit at least as well as NB2 — well enough to clear SF02/SF01 — and does it suffer the NB-Pro downsampling failure?** Everything below is structured to answer that with the least spend. Run first-party (`api.reve.com`) so you get the 6-ref ceiling and true pricing. Keep NB2 (`invoke_image_edit`) as the side-by-side control on every prompt.

**Fixtures (all already in-repo):**
- Anchor: `characters/sean-anchor/anchor.png` (the SF02 ground truth — face, hair, jaw, palette, 1:7 proportions).
- View reference: a `characters/sean-anchor/turnarounds/` plate (e.g. `three-quarter`) for the angle tests.
- Multi-reference pairing: `characters/sean-anchor/anchor.png` + `characters/claude-mascot/anchor.png` + the **A-7 pairing** `characters/claude-mascot/source-refs/sean-with-claude-mascot.png` — this is the known two-character edit that stresses the exact multi-ref path NB Pro failed.
- Register target: `pencil-test-colored` (graphite line, flat color fills, cross-hatch, warm cream paper, 16:9).

**Test 1 — single-reference expression edit (SF02 + SF01, the floor).**
Prompt, Reve **Edit** and NB2, identical instruction: *"Same person as the reference. Change only the expression to focused — brow slightly down, eyes on the work, mouth set. Keep the face, hair, full color palette, and proportions exactly. Warm pencil-test render: graphite line, flat color fills, cross-hatch shadow, cream paper. 16:9. No text or watermarks."* Run 5× each.
**Pass:** ≥4/5 recognizably Sean (SF02), register held (SF01 — graphite line, cream paper, *not* monochrome, not photoreal), 16:9 exact. This is the `focused`-plate trap from the production bake — watch specifically for the monochrome/identity slide.

**Test 2 — multi-reference angle edit (the NB-Pro downsampling probe — the decisive one).**
Reve **Remix** with `anchor.png` (identity) + the three-quarter turnaround (angle target), vs NB2 multi-ref. Instruction: *"Identity from image 1, viewing angle from image 2. Render Sean at a three-quarter front view, head turned slightly left. Match face, hair, palette, proportions of image 1 exactly. Pencil-test register, cream paper, 16:9."* Run 5× each.
**Pass:** identity from image 1 survives (no generic-face drift), angle follows image 2, **fine detail not washed out** (the NB-Pro tell — if Reve returns a soft, generic, downsampled face, it shares the regression and is disqualified for multi-ref keyframes). Then **escalate to the 3-reference A-7 pairing** (Sean + mascot + pairing ref) and look for attribute bleed between the two characters.

**Test 3 — in-between consistency run (the best-fit case).**
Take two already-approved adjacent anchors. Use Reve **Remix Fast** to generate the mid-pose between them (both as references), 5×. Compare against an NB2 in-between.
**Pass:** the generated frame reads as the same character mid-motion, register held, and — the point of Fast tier — it's ~10× cheaper and fast enough to make the retry ladder cheap. A mild wobble is more tolerable here than in Test 1.

**Test 4 — operational confirmations (one run each, cheap):**
- Inspect a returned image + metadata → **is there a visible watermark or only C2PA?**
- Confirm the pencil-test prompt isn't content-filtered.
- Note observed latency (Fast vs standard) and any rate-limit headers.

**Scoring.** Run each side-by-side through **Em (T2 vision critic)** the same way production frames are scored — reference-blind default, the G5-baseline config (gemini-3.5-flash pinned, N=5 majority) — and read SF02/SF01 verdicts off Em's output, not by eye alone. That keeps the bake-off empirical and on anima's own rails (PHILOSOPHY: *empirical, not vibes*). Log it as a dated bake-off under `evals/bakeoffs/2026-MM-DD-reve-vs-nb2-editing/`, mirroring the existing T2 model bake-off, so the result becomes museum-eligible portfolio evidence rather than a throwaway.

**Decision rule.** Reve **adopts for in-betweens** if Test 3 passes and Test 2 shows no downsampling regression. Reve **adopts for keyframes/Bible** only if Test 1 and the multi-ref half of Test 2 *match or beat NB2* on SF02. If Test 2 reveals NB-Pro-style downsampling, Reve stays a single-reference Edit tool at most, and never touches multi-reference keyframes.

---

## 6. Open questions (couldn't source from desk research)

1. **Reve multi-reference identity fidelity** — does it suffer NB-Pro-style downsampling? No independent data exists. *Only Test 2 answers this.* The single most important unknown.
2. **Reve watermarking** — visible mark, invisible C2PA, or none on API outputs? Unconfirmed. Matters for a public portfolio.
3. **Reve rate limits + p50/p99 latency, first-party** — not published in any source found; Fast-vs-standard latencies unmeasured.
4. **Reve register fidelity** — can it hold the `pencil-test-colored` register (graphite line, cream paper, cross-hatch) as faithfully as NB2's tuned prompt template? Untested.
5. **Reve console-doc specifics** — `api.reve.com/console/.../docs/{edit,remix}` is an auth-gated, JS-rendered SPA; exact first-party params, the real 6-ref handling, max prompt length, and seed control are inferred from third-party mirrors (which cap at 4 refs and may diverge). Confirm against the live console when authenticated.
6. **Reve underlying model version + provenance of training data** — "internal structured format," small research team; no model card depth, no training-data disclosure. Standard closed-model opacity; note for IP-sensitivity on a public piece.
7. **Ideogram 4 hosted-API editing** — the *hosted* Ideogram product may offer edit/remix features the *open weights* don't; if a future open release adds reference-conditioning under a commercial license, re-evaluate. Out of scope here (open-weights focus).
8. **Ideogram 4 16GB path** — whether a GGUF text-encoder + nf4 DiT actually fits and renders 2K on a 5080 is unbenchmarked by the community as of this writing; moot given license + capability, but technically unresolved.

---

## Sources

**Ideogram 4 — authenticity, license, weights, capability**
- [github.com/ideogram-oss/ideogram4](https://github.com/ideogram-oss/ideogram4) — repo, README, model zoo, architecture, safety/Hive screening
- [Ideogram 4 Non-Commercial Model Agreement (license text)](https://github.com/ideogram-oss/ideogram4/blob/main/model_licenses/LICENSE-IDEOGRAM-4-NON-COMMERCIAL)
- [ideogram-ai/ideogram-4-nf4 (HF, gated, official org)](https://huggingface.co/ideogram-ai/ideogram-4-nf4) · [ideogram-4-fp8](https://huggingface.co/ideogram-ai/ideogram-4-fp8) · [Ideogram 4 collection](https://huggingface.co/collections/ideogram-ai/ideogram-4)
- [Ideogram 4.0 technical blog](https://ideogram.ai/blog/ideogram-4.0/) · [ComfyUI day-0 support](https://blog.comfy.org/p/ideogram-4-day-0-support-in-comfyui)
- [buildfastwithai — Ideogram 4 open-weight](https://www.buildfastwithai.com/blogs/ideogram-4-open-weight-image-model) · [evolink — what developers should know (license nuance)](https://evolink.ai/blog/ideogram-4-0-what-developers-should-know)
- [Qwen3-VL-8B-Instruct (text encoder)](https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct)

**Ideogram 4 — local feasibility / Blackwell**
- [pytorch#164342 — sm_120 stable support](https://github.com/pytorch/pytorch/issues/164342) · [PyTorch Forums — RTX 5080 compat](https://discuss.pytorch.org/t/compatibility-issue-between-pytorch-and-nvidia-geforce-rtx-5080/222981) · [community custom build](https://github.com/kentstone84/pytorch-rtx5080-support)
- [city96/ComfyUI-GGUF #452 — Qwen3-VL-8B GGUF text encoder](https://github.com/city96/ComfyUI-GGUF/issues/452) · [Civitai — Ideogram 4 LOW VRAM fp8/4](https://civitai.com/models/2673990/ideogram-4-low-vram)

**Reve — capability, schema, pricing, terms**
- [Reve API console pricing](https://api.reve.com/console/pricing) (Sean's screenshots — first-party) · [Reve app pricing](https://app.reve.com/pricing) · [Reve API License Agreement](https://app.reve.com/terms/api)
- [Replicate — reve/remix (official, 40.8K runs)](https://replicate.com/reve/remix) · [Reve on fal](https://blog.fal.ai/reve-is-now-available-on-fal/)
- [AIMLAPI — reve/remix-edit-image schema (aspect ratios, refs, params)](https://docs.aimlapi.com/api-references/image-models/reve/reve-remix-edit-image) · [AIMLAPI — reve-edit-image](https://aimlapi.com/models/reve-edit-image)
- [trilogy — Reve 2.0 innovation](https://trilogyai.substack.com/p/reve-20s-innovation-in-image-generation)

**Cost baselines + comparative**
- [Gemini API pricing (official, $60/1M image-output tokens)](https://ai.google.dev/gemini-api/docs/pricing) · [Gemini 3.1 Flash Image per-resolution breakdown](https://www.aifreeapi.com/en/posts/gemini-flash-image-generation-pricing) · [pricepertoken — Gemini 3 Flash](https://pricepertoken.com/pricing-page/model/google-gemini-3-flash-preview)
- [Atlas Cloud — 2026 image API benchmark (Reve ~$667 vs NB2 ~$6,700 / 100k)](https://www.atlascloud.ai/blog/guides/2026-ai-image-api-benchmark-gpt-image-2-vs-nano-banana-2-pro-vs-seedream-5-0)
- [Decrypt — GPT Image 2 vs NB2 (independent consistency read)](https://decrypt.co/366408/openai-gpt-image-2-vs-google-nano-banana-2-review)

**anima internal**
- [2026-05-30 NB2 editing / character-consistency template](2026-05-30-nb2-editing-character-consistency-template.md) — NB2-over-NB-Pro routing, the multi-reference downsampling regression, the five-slot emitter
- [Google AI Dev Forum — NB Pro multi-reference regression (primary)](https://discuss.ai.google.dev/t/gemini-3-0-pro-image-preview-inconsistent-performance-with-multiple-reference-images-since-3-1-launch/128648)
