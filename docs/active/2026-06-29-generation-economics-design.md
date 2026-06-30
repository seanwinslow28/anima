# Generation Economics — Design Note (Direction ③)

**Date:** 2026-06-29
**Status:** Decided 2026-06-29. **Not a build** — a transport decision plus a one-month measurement. Runs in parallel with Tier-2 (the *only* parallel item; ~$0, zero drift risk).
**Session kickoff:** [`docs/active/2026-06-22-anima-vision-expansion-kickoff.md`](2026-06-22-anima-vision-expansion-kickoff.md)
**Grounding:** the live pricing pass (2026-06-29), [`docs/research/2026-06-19-seedance-2.0-access-cost-comparison.md`](../research/2026-06-19-seedance-2.0-access-cost-comparison.md), the [Higgsfield generation runbook](../anima-test-runs/2026-06-22-higgsfield-seedance-generation-runbook.md).

---

## The question

The cheapest, broadest way to generate anima's images and videos. Sean bought a Higgsfield monthly subscription (broad model access + a CLI + an MCP server + Skills, so an agent can reach many models programmatically) — it's great, but expensive. Is there a cheaper way to get similar breadth? Does the fal.ai API, or direct per-provider keys, beat Higgsfield's monthly credits?

## Locked models (Sean, 2026-06-29)

- **Video:** Seedance 2.0 and Seedance 2.0 Fast (won't switch — "don't see anything beating Seedance any time soon").
- **Images:** Nano Banana 2 (Gemini) and gpt-image (OpenAI/ChatGPT); open to open-source challengers as they emerge.

## The decision table (current June-2026, scriptable/API path)

| Stage | Model (locked) | Cheapest scriptable | $/unit | Manual path | Note |
|---|---|---|---|---|---|
| Images — character/stylized | Nano Banana 2 | direct Gemini API | **$0.067**/img (batch $0.034) | Flow $0 · HF credits | fal/Replicate don't host NB2 |
| Images — design/text/UI | gpt-image-2 | direct OpenAI API | **~$0.04–0.05**/img | HF credits | nor gpt-image |
| Images — pencil at volume | FLUX + LoRA | fal $0.025 · self-host ~$0.002 | — | — | self-host only pays off at 1000s/mo |
| Video — motion | Seedance 2.0 Fast | **Replicate $0.90** · fal $1.21 | per 5s / 720p | HF ~$1.20 (credits) | 2.0 resellers ~$0.70–0.76 (re-validate); 1.5 Pro $0.26 (declined) |
| Broad agent access | many | **fal** — hosted MCP + CLI | pay-per-use, $0 idle | HF subscription | fal = the cheapest Higgsfield-shape |

## Findings (convergent across all three sources)

- **Higgsfield's real value is breadth in one place** — it's the only option bundling NB2 + GPT Image 2 + Seedance 2.0 behind one CLI/MCP. But through the CLI it's **metered credits, not unlimited** (the runbook's Act 2 burned 147 credits; the web "unlimited Fast/Mini" perk does not reflect the metered CLI/API), credits **expire monthly**, and Ultra (~$129/mo, ~120 clips) only pays off **above ~100 Seedance clips/month**.
- **fal.ai is the cheapest like-for-like replacement for that breadth:** one key, an official hosted MCP server (`mcp.fal.ai/mcp`) + a `fal` CLI, ~1,000+ image+video models including Seedance 2.0/Fast and FLUX, pure pay-per-use, **$0 idle, no expiring credits**. The one gap: fal doesn't host NB2 or gpt-image (Google/OpenAI proprietary), so those two go-to image models want **direct Gemini + OpenAI keys**.
- **The cheapest stack is the one the pipeline already runs:** direct Gemini (NB2) + direct OpenAI (gpt-image) for images + fal for Seedance video. Higgsfield is the manual/exploratory layer on top — which is exactly what the runbook frames it as.
- **The autonomous pipeline can't use a GUI.** Flow's and Higgsfield's $0/credit convenience only applies to *manual* exploration; Flo's transports and the Motion phase call APIs directly and pay marginal cost. The true pipeline cost is the marginal-API column.
- **Two levers half-declined:** the *2.0-only* lock is the most expensive line item — Seedance 1.5 Pro is **4.7× cheaper ($0.26 vs $1.21), same fal wiring** (ruled out on quality, which is legitimate). Honoring the lock, **Replicate runs 2.0 Fast at $0.90 vs fal's $1.21** — a clean ~25% cut, same model, an endpoint swap; cheaper 2.0 resellers (~$0.70–0.76: Segmind, BytePlus, AtlasCloud) exist but need reliability and failure-billing re-validation.
- At current volume (~10 clips/act ≈ $12/run on fal Fast), the absolute dollars are tiny — so this is a **monthly-subscription decision**, not a per-asset one.

## Decision (Sean, 2026-06-29)

**Trial Higgsfield for one month; run the pipeline on fal + direct keys meanwhile; measure the real monthly Seedance clip count; decide keep/drop at month-end against the ~100-clip break-even.** Empirical and no-regret. The pipeline already runs the cheap path, so there is nothing to build.

## Cheapest next step

Baked into the trial: a small **Replicate-vs-fal Seedance reliability check** during the month (validate the $0.90 rate, failure billing, and US reliability) plus the monthly clip-count measurement. Both are ~$0 incremental and answer the keep/drop question with data.

## Where it sits in the sequence

**Parallel with Tier-2, now** — the only parallel item, because it's a decision and a measurement, not code. ~$0, zero drift risk. It is the cost spine under ① (the in-session art-viz loop) and ② (the generate and motion screens), so settling it now de-risks both downstream builds.

## Sources

- Live pricing pass, 2026-06-29 (fal, Replicate, Gemini, OpenAI, Higgsfield pricing pages; figures dated and verify-at-checkout for Higgsfield's restructured tiers).
- [`docs/research/2026-06-19-seedance-2.0-access-cost-comparison.md`](../research/2026-06-19-seedance-2.0-access-cost-comparison.md) — anima's prior Seedance access comparison (the 1.5 Pro lever, the reseller landscape, the web-app dead-end).
- [Higgsfield generation runbook](../anima-test-runs/2026-06-22-higgsfield-seedance-generation-runbook.md) — measured credit costs (Fast 720p ≈ 3.5 credits/sec; Act 2 = 147 credits; "unlimited ≠ free via CLI").
- Key external rates: [fal Seedance 2.0](https://fal.ai/models/bytedance/seedance-2.0/image-to-video), [Replicate Seedance 2.0 Fast](https://replicate.com/bytedance/seedance-2.0-fast), [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing), [fal MCP server](https://blog.fal.ai/connect-your-ai-to-1-000-models-with-the-fal-mcp-server/).
