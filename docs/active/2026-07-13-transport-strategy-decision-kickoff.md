# Kickoff — transport strategy decision: direct APIs vs. Higgsfield-for-everything (fresh-session prompt)

*Paste the block below into a fresh Claude Code session in the `anima` repo. It opens a **decision + research** session on the single most consequential infrastructure call anima has open: wire up each model's native API directly, or route ALL of anima's generation through the Higgsfield CLI/MCP as one universal transport. Brainstorm-first, then a costed research pass, converging on a ratified decision doc.*

**Date:** 2026-07-13 · **Workstream:** the outward turn / animation-vocabulary-expansion (this is *infrastructure* research **within** it, not a new workstream) · **Status:** kickoff — not yet run. · **Origin:** Sean has been using the Higgsfield CLI heavily and thinks it may be the right unifying transport layer for the whole pipeline; he leans toward committing to it but wants a real brainstorm + research pass (with pricing guesstimates for both paths) before deciding.

**The live forcing function:** three registers now record `GPT_IMAGE` as UNWIRED / fails-loud (`primal-sketch-grit`, `samurai-jack-s5`, `flat-cast-painted-world`), and GRANDMASTER can't run until a gpt-image transport exists. The immediate "wire gpt-image direct via OpenAI, or via Higgsfield?" is a special case of the whole-pipeline decision — decide the general policy and the gpt-image wiring falls out of it.

---

## The pasteable kickoff prompt

> You are running a transport-strategy decision session for anima — the single most consequential infrastructure call the pipeline has open right now: **wire up each model's native API directly, OR route ALL of anima's generation through the Higgsfield CLI/MCP as one universal transport.** Sean has been using the Higgsfield CLI heavily and thinks it may be the right unifying layer for this whole pipeline. He leans toward committing to Higgsfield but wants a real brainstorm + research pass before deciding. **This is a DECISION + RESEARCH session — no production code. Output is a ratified decision doc a later build session executes.**
>
> **Invoke `superpowers:brainstorming` FIRST** (this is a design decision, one-question-at-a-time), then run a costed-research pass, then converge.
>
> **Read first (in order):**
> 1. `docs/architecture/style-register-authoring-playbook.md` §Transport — the current NB2-default → gpt-image/NB Pro/fal ladder, fail-loud when unwired.
> 2. `docs/active/2026-07-04-register-backlog-and-transport-findings.md` — the transport findings + the roster (three registers now record `GPT_IMAGE` UNWIRED: `primal-sketch-grit`, `samurai-jack-s5`, `flat-cast-painted-world`).
> 3. `docs/anima-test-runs/2026-06-22-higgsfield-seedance-generation-runbook.md` — real Higgsfield CLI costs + gotchas (Fast ≈ 3.5 cr/s; "unlimited Fast/Mini" ≠ free via CLI; auth is human-only; the nested-SDK throttle).
> 4. `docs/architecture/fleet-ops-protocol.md` — subscription billing discipline (never `ANTHROPIC_API_KEY`; costed runs need Sean's greenlight).
> 5. `docs/research/2026-05-26-anti-gravity-cli-findings.md` — **the cautionary precedent**: anima already depended on one vendor CLI (`agy`) that got sunset. Weigh single-vendor risk against that.
> 6. The current transport surface in code: `pipeline/agents/nb_pro_runner.py` (`SUPPORTED_IMAGE_MODELS`, `invoke_image_edit`, the `UnwiredTransportError` guard), `pipeline/agents/gemini_api_runner.py`, `pipeline/agents/fal_runner.py`, `pipeline/registers.py` (the `generation_model`/`final_model` per register).
>
> **The forcing function (why now):** three registers + GRANDMASTER are blocked on a wired gpt-image transport. The immediate question — "wire gpt-image direct via OpenAI, or via Higgsfield?" — is a special case of the whole-pipeline decision. Decide the general policy, then the gpt-image wiring falls out of it.
>
> **The decision space (surface the hybrids, don't force a binary):**
> - **Path A — direct native APIs:** OpenAI (gpt-image-2), Gemini API (NB2/NB Pro, already wired), fal.ai (Seedance, already wired), Anthropic (text agents). Per-call API pricing; N runners to build + maintain; each needs across-edit identity validation.
> - **Path B — Higgsfield as the universal generation transport:** one subscription/CLI/MCP fronts gpt_image_2 + nano_banana_2/pro + Seedance + Seedream + FLUX + Grok + more. One runner, one billing surface. Trade: subscription credits vs per-API; third-party-aggregator dependency; possible capability/latency/identity-hold deltas.
> - **Hybrid candidates to test:** Higgsfield for image+video *generation* (unify gpt-image + NB2 + Seedance under one sub) while keeping **Gemini API direct for Em's verification** (deterministic, pinned model, reproducible) and **Anthropic direct for text agents**.
>
> **The questions the research must answer (this is the meat):**
> 1. **Capability parity (load-bearing).** anima's Cy needs *across-edit identity hold* with anchor-first multi-reference injection — not just text-to-image. Does Higgsfield's gpt_image_2 / NB2 expose the reference-`medias` roles + editing contract `invoke_image_edit` depends on? Probe it (a small costed spike is fine, Sean-gated). If Higgsfield can't do reference-anchored editing as well as the direct API, that caps how far Path B can go.
> 2. **Pricing at anima's real volume.** Model the actual workloads — a Bible pass (N plates × 3-attempt ceiling), a per-frame generation run, a Motion pass (Seedance clips). Higgsfield credit costs per model vs direct API per-image / per-second. Where's the crossover? Include the subscription's fixed cost. Cite real numbers from the runbook + current OpenAI/Gemini/fal price sheets (research them fresh — don't guess).
> 3. **Architecture fit + reproducibility.** If Higgsfield becomes the universal runner: does `SUPPORTED_IMAGE_MODELS` collapse into one `HiggsfieldRunner`? What happens to content-addressed caching, model pinning (Higgsfield's IDs vs the pipeline's pinned Gemini/OpenAI IDs), and the **credential-free CI stub path** (every agent runner must fall back to a stub so the suite stays green with no keys)?
> 4. **Risk + lock-in.** Single-vendor dependency (the `agy` sunset precedent), rate limits, human-only auth (breaks headless/cron), the nested-SDK throttle, terms/quota changes. What's the exit cost if Higgsfield changes pricing or sunsets?
> 5. **The recommendation.** A clear call (A / B / a specific hybrid) with the reasoning, the pricing crossover, and a phased wiring plan — and specifically what it means for the three unwired gpt-image registers + GRANDMASTER.
>
> **Method:** brainstorm (surface Sean's real priorities + the axes) → **Human Checkpoint 1** (agree the decision frame + which probes are worth costing) → a research pass (fresh pricing research + capability probes; costed spikes Sean-gated, subscription billing) → **Human Checkpoint 2** (Sean ratifies the recommendation) → write a decision doc in `docs/active/` (mirror the `2026-07-11-samurai-jack-s5-register-design.md` shape: ratified decisions + rationale + the phased build plan a later session executes).
>
> **Guardrails:** no production code this session (the output is a decision doc + a research writeup, not a runner). Costed capability probes only with Sean's explicit go, subscription billing, fleet-ops discipline. This is architecture research **within** the active outward-turn workstream (it decides HOW to wire the already-deferred/gated gpt-image transport) — it does **not** open a new workstream. Sean's eye + judgment are the arbiter on the final call.
>
> Start by reading the six sources, then open the brainstorm with your sharpest single question about what Sean actually optimizes for here (cost? one-integration-simplicity? capability ceiling? avoiding lock-in?).

---

## Context notes for whoever runs this (not part of the paste)

- **Lead with the bias, don't bake it in.** Sean leans toward Higgsfield-for-everything and has real hands-on evidence it's great for this pipeline. The research must let that conclusion *earn itself* by clearing the **capability-parity** bar first — Cy's across-edit identity hold (anchor-first multi-reference editing, not just text-to-image) is the thing that could quietly cap Path B. Pricing is the second gate, not the first.
- **This decision resolves a standing ticket, not a new one.** The gpt-image runner + across-edit identity validation has been *deferred + gated* since the primal/samurai/fusion builds. This session decides the *policy* (direct vs Higgsfield vs hybrid) that governs how that gated build gets wired — it stays within the active outward-turn workstream and opens nothing new (anti-drift contract holds).
- **The MCP is already proven reachable.** The `flat-cast-painted-world` NB2 confirmation spike (2026-07-13) fired live through the Higgsfield MCP `nano_banana_2` — so the MCP transport path is real and callable from a session; the open question is *editing/identity-hold parity + pricing*, not basic reachability.
- **Don't let the CI stub path fall out of scope.** Whatever wins, every agent runner must keep its credential-free stub fallback so `python -m pytest tests/` stays green with no keys. A universal `HiggsfieldRunner` still needs a stub.
- **Output shape:** a ratified `docs/active/YYYY-MM-DD-transport-strategy-decision.md` (mirror the samurai design doc: the ratified calls + rationale + a phased build plan), plus a research writeup with the pricing model + capability-probe findings. A later session executes the build.
</content>
