# Hermes Agent + DeepSeek V4 Flash — Evaluation for anima

**Date:** 2026-05-26
**Question:** Sean asked for an honest, unbiased read on whether Hermes Agent (Nous Research) makes sense as anima's orchestration harness — and whether DeepSeek V4 Flash is worth adding to the stack now that it's free inside Hermes via Nous Portal subscription.
**Sources:**
- [Hermes Agent docs](https://hermes-agent.nousresearch.com/docs/)
- [Hermes Agent Features Overview](https://hermes-agent.nousresearch.com/docs/user-guide/features/overview)
- [Hermes Agent Configuring Models](https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models)
- [Nous Portal integration docs](https://hermes-agent.nousresearch.com/docs/integrations/nous-portal)
- [Hermes Agent GitHub](https://github.com/nousresearch/hermes-agent)
- [DeepSeek V4 Flash on Artificial Analysis](https://artificialanalysis.ai/models/deepseek-v4-flash)
- Teknium tweet announcing DeepSeek V4 Flash is back free on Nous Portal for Hermes Agent
- Existing prior context: Gemini DR Max research (2026-05-26) noted Higgsfield Supercomputer uses Hermes Agent as its creative-pipeline orchestrator
**Verdict (one line):** Don't adopt Hermes Agent as anima's orchestrator. Don't add DeepSeek V4 Flash as a default model. Do steal three specific Hermes patterns. Do consider DeepSeek V4 Flash as an optional fourth T3 peer voice in a post-implementation bake-off.

---

## 1. What Hermes Agent actually is

An open-source autonomous AI agent CLI/toolkit from Nous Research, released February 2026, currently v0.14, MIT-licensed. Important distinction: **it's not just a model wrapper.** It has its own agent loop, tool registration system, session/memory model, hook architecture, and provider routing layer. Capabilities map roughly:

- Persistent memory via `MEMORY.md` and `USER.md`
- Skills system compatible with the [agentskills.io](https://agentskills.io/specification) open standard
- Context files (`.hermes.md`, `AGENTS.md`, `CLAUDE.md`, `SOUL.md`, `.cursorrules`) — auto-discovered and loaded
- Subagent delegation via `delegate_task` tool — three concurrent by default, configurable
- Code execution via `execute_code` tool — Python in sandboxed RPC, collapses multi-step workflows into single inference turn
- Event hooks (gateway hooks + plugin hooks) for logging, alerts, webhooks, tool interception, metrics, guardrails
- MCP integration (stdio + HTTP transport, per-server tool filtering, sampling support)
- Provider routing with fallback providers + credential pools + automatic key rotation on rate limits
- Built-in cross-session 1-hour prefix cache for Claude (Nous Portal, OpenRouter, native Anthropic)
- OpenAI-compatible API server (`hermes serve`) — connect any frontend that speaks OpenAI format
- ACP editor integration (VS Code, Zed, JetBrains)
- Plugin system for custom tools, hooks, integrations — three plugin types (general, memory providers, context engines)
- Profiles for running multiple agents
- Scheduled tasks (cron, natural language)
- Vision (image paste from clipboard)
- Image generation via FAL (nine models including NB Pro)
- Voice mode (Edge TTS, ElevenLabs, OpenAI TTS, MiniMax, Mistral Voxtral, Google Gemini, xAI, NeuTTS, KittenTTS, Piper)
- Browser automation (Browserbase, Browser Use, local Chrome/Brave/Chromium/Edge via CDP)
- Checkpoints + rollback (snapshots working dir before file changes)
- Batch processing (ShareGPT-format trajectory data for training)
- RL trajectory data generation

**Important caveat from Hermes's own docs:** Nous Research's Hermes 4 family (Hermes-4-70B / 405B) is *not recommended for use inside Hermes Agent.* Their docs explicitly say so — Hermes 4 is tuned for chat and reasoning, not for the rapid-fire tool-calling loop the agent relies on. Recommended models inside Hermes Agent are Claude Sonnet 4.6, GPT-5.4, Gemini 2.5 Pro, or DeepSeek V3.2. **The same model choices anima's v2 already locked.**

**Higgsfield Supercomputer uses Hermes Agent.** From the Gemini DR Max research earlier in this session: powered by the "Hermes Agent" (a fine-tuned logic engine based on Nous Research's Hermes 3), Higgsfield recursively routes tasks between 40+ visual tools with three-layer memory. That's a real production example — but it's an opaque-cloud-orchestrator-of-many-tools use case, not an open-source-pipeline-as-portfolio use case.

---

## 2. What DeepSeek V4 Flash actually is

- Released April 24, 2026 as preview
- 284B total parameters, 13B active per token (MoE), 1M token context window, MIT licensed
- $0.14 / $0.28 per 1M tokens — very cheap
- **Reasoning model with "Max Effort" mode** — extended chain-of-thought
- Intelligence Index 47 (#6/76 on Artificial Analysis Intelligence Index, well above open-weight median of 28)
- **84.7 tokens/sec output speed** (above the open-weight median of 52)
- **1.00s time to first token** (very competitive vs median 2.04s)
- **Very verbose** — 240M tokens to run the Intelligence Index (median 43M, 5.6× heavier than median)
- **Text-only — NOT multimodal** — no vision input support
- On coding: within 1.6 percentage points of V4 Pro (1.6T parameters)
- On HLE (Humanity's Last Exam): below both Gemini 3.1 Pro (44.4%) and Claude Opus 4.7 (46.9%)
- **Free inside Hermes Agent via Nous Portal subscription** (per the Teknium tweet — Nous added it back to the portal catalog)

The headline: it's a strong, cheap, fast reasoning model in the open-weight tier. It's not at the Opus 4.7 / GPT-5.5 / Gemini 3.1 Pro frontier on the synthesis benchmarks anima cares about. It's text-only, which closes the door on the highest-value anima role (T2 vision critic).

---

## 3. The case FOR adopting Hermes Agent as anima's orchestrator

Five arguments worth taking seriously:

**3.1 Feature overlap with anima's roadmap is real.** Hermes Agent already ships: skills system, MCP integration, subagent delegation, code execution, event hooks, persistent memory, plugin system, checkpoints/rollback, scheduled tasks, image generation routing. Several of these map onto anima's commit-4-through-commit-9 plan (DAG runner + hooks + skill packaging + museum capture). Adopting Hermes would shortcut the engineering for those features.

**3.2 The Tool Gateway is genuinely useful.** Firecrawl web search, FAL image gen (nine models including NB Pro), Browser Use cloud browser, OpenAI TTS — five separate provider integrations collapsed into one subscription. That's real friction-reduction.

**3.3 DeepSeek V4 Flash via Nous Portal is free.** Adds a vendor voice at $0 incremental. Subscription absorption matches anima's existing cost-discipline philosophy.

**3.4 Conceptual alignment.** SOUL.md, MEMORY.md, USER.md, skills as on-demand documents — Sean already uses these patterns in code-brain via the operating-model artifact loader. Hermes treats them as first-class. The vocabulary matches.

**3.5 Higgsfield uses it in production.** Real precedent for "Hermes Agent as creative-pipeline orchestrator." Anima isn't venturing into uncharted territory.

---

## 4. The case AGAINST adopting Hermes Agent as anima's orchestrator

Eight arguments, in roughly descending strength:

**4.1 The portfolio thesis works against it.** From PHILOSOPHY.md: *"Read like a studio, not a terminal."* From the change-map's DAG-library rationale (locked 2026-05-24): *"the museum's job is to show the work, which means the work has to be readable: hand-rolled code is portfolio gold, 'I configured Prefect' is not."* Hermes Agent is a heavier framework than Prefect. Adopting it turns anima from *"I built this from scratch and the museum shows how"* into *"I configured Hermes to do this."* That's a material loss of portfolio signal, and the synthesis just spent paragraphs naming subscription-absorbed multi-provider council as a differentiating practice — the differentiation is in the *bespoke* construction, not the *off-the-shelf* one.

**4.2 anima's session model doesn't match Hermes's session model.** Hermes Agent is built around a long-running conversational agent with persistent memory across sessions, a stateful tool gateway, and a unified chat surface. Anima is built around per-piece runs with frozen manifests, per-run directories, content-addressed caching scoped to a single piece's DAG. These are different abstractions. Running anima inside Hermes means either losing anima's per-run discipline or fighting Hermes's persistent-memory assumptions.

**4.3 The T3 multi-CLI critic pattern doesn't transplant cleanly.** anima's T3 uses `asyncio.gather` to fan out to Codex CLI + Anti-Gravity CLI + Claude Agent SDK in parallel (the `vault_critic.py` pattern). Hermes runs as a single agent loop. It supports subagents via `delegate_task`, but those subagents are Hermes subagents inside Hermes's tool system — not direct CLI shell-outs with their own subscription-absorbed model routing. Adopting Hermes means rewriting the T3 stack to fit Hermes's delegation model, which loses the architectural-diversity property the synthesis named load-bearing (the orchestrator and the T2 critic must come from different model families — if both run through Hermes's OpenRouter-based routing layer, you've introduced a new correlation surface).

**4.4 The `acceptance_criteria.json` shared-rubric pattern has no home in Hermes.** anima's v2 structural fix for local-optimization drift is the planner's immutable criteria file that downstream critics cite by ID. Hermes doesn't have this concept — Hermes's memory is conversational accumulation, not contractual rubric. Building the rubric pattern on top of Hermes means fighting the framework.

**4.5 The typed `AgentSpec` Protocol contract has no home either.** anima's v2 commit 4 lands a typed Protocol that every agent declares (`inputs`, `outputs`, `cost_estimate`, `cites_criteria`, `run(ctx) -> AgentResult`). Hermes's tool registration is a different shape — tools are functions registered with the agent loop, not typed contracts. Force-fitting anima's Protocol onto Hermes's tool registration creates impedance for no benefit.

**4.6 Hermes Agent's own recommendation is the same model set anima already locked.** Per the Nous Portal integration docs, the recommended models inside Hermes Agent are Claude Sonnet 4.6, GPT-5.4, Gemini 2.5 Pro, or DeepSeek V3.2 — the same set the synthesis converged on (with Opus 4.7 added for pinnacle phases). So adopting Hermes doesn't unlock different models; it just changes the wrapper around the same models.

**4.7 The DAG runner is anima's most teachable piece.** Commit 4 is ~7-10 evenings of work and produces 300–500 LOC of hand-rolled Python. That's the kind of artifact the museum walkthrough renders proudly. Replacing it with `hermes setup --portal` is faster but produces nothing for the museum to show.

**4.8 DeepSeek V4 Flash is the wrong tool for anima's pinnacle phases.** Text-only (closes Em). Verbose (5.6× median token usage at peak intelligence — latency drag at 10–50 calls per piece). Below Opus 4.7 / Gemini 3.1 Pro on HLE (closes the pinnacle phases the synthesis already locked). It's a credible cheap-tier reasoning model in the open-weight category, but anima's challenge isn't *finding a cheap-tier reasoning model* — it's *getting top-tier models on the pinnacle phases*. V4 Flash doesn't move that needle.

---

## 5. What to do instead

**5.1 Don't adopt Hermes Agent as anima's orchestrator.** v2's locks stand. Sonnet 4.6 via Claude Agent SDK with Opus escalation hatch is the right primitive for anima's architecture, scale, and portfolio thesis.

**5.2 Don't add DeepSeek V4 Flash as a default model anywhere in v2.** None of the locked roles improve by swapping in V4 Flash. Opus 4.7 wins on the pinnacle phases. Gemini 3.1 Pro wins on T2 vision. The three T3 peer slots are already filled by distinct vendors. V4 Flash isn't displacing anything.

**5.3 Do steal three Hermes patterns explicitly.** Not by adopting Hermes — by reading its source and stealing the patterns into anima's own implementation:

- **agentskills.io open standard for skill packaging.** Sean's existing skills (writing-voice-modes, screenwriting-modes, animation-pipeline, seedance-prompting, gemini-pencil-animation-image-gen) could be made compatible with the agentskills.io spec, which would let them load identically into Hermes Agent, Claude Code, or anima's runner. Cross-tool skill portability is real signal — and the open standard is well-documented.
- **MEMORY.md / USER.md / SOUL.md pattern at the run level.** Sean already uses this in code-brain via operating-model artifacts. Anima could mirror it per-run: `runs/{run_id}/MEMORY.md` accumulates decisions across phases as the orchestrator routes through Maya → Cy → Sam → Bea → Flo → Em → Codie+Annie+Sage+Chairman → Mo. Becomes part of the museum capture layer naturally.
- **The gateway-hooks-plus-plugin-hooks architecture.** Hermes splits observer-pattern hooks into two layers — gateway hooks (logging, alerts, webhooks fired at the infrastructure boundary) vs plugin hooks (tool interception, metrics, guardrails fired at the agent-internal boundary). anima's commit 6 (museum capture) wants exactly this split: gateway hooks fire museum-write events; plugin hooks enforce `acceptance_criteria.json` citation requirements. Worth reading Hermes's hook implementation as a reference.

**5.4 Do consider DeepSeek V4 Flash as a candidate fourth T3 peer voice — but only in a post-implementation bake-off.** anima's v2 §9 already reserves three open questions for empirical resolution. Adding a fourth (Open Q7: does extending T3 from three to four vendors improve dissent-map richness?) is a clean extension of the existing bake-off plan. Test cases: same three-peer baseline vs four-peer (Codie + Annie + Sage + Deva, where Deva = DeepSeek V4 Flash via Nous Portal). Hold Opus chairman constant. Measure agreement rate, dissent-map richness, chairman synthesis quality, latency cost. If Deva adds material value, lock it into a future v2.1. If not, three peers stays the lock.

**5.5 Do use Hermes Agent for what it's good at — outside anima.** Sean already uses Claude Code, Codex CLI, Anti-Gravity CLI for different workflows. Hermes Agent is a fourth shell that's particularly strong on: scheduled tasks ("daily Discord summary"), batch processing ("run this prompt across 200 inputs"), voice mode, browser automation, cross-platform Windows. Not anima's primary, but a useful tool in Sean's broader fleet. Worth installing and learning the surface — just don't make anima depend on it.

---

## 6. The honest, unbiased opinion

Hermes Agent is a genuinely impressive piece of software, and the Nous Portal subscription model is a clever consolidation of fragmented provider billing. If Sean were starting anima from zero with no existing portfolio thesis and no synthesis decisions, Hermes Agent would be worth a real evaluation as the orchestrator primitive.

But anima isn't starting from zero. The PHILOSOPHY locks hand-rolled, museum-quality, transparent. The synthesis locks specific model assignments + structural patterns (`acceptance_criteria.json`, typed AgentSpec, architectural diversity). The change-map locks hand-rolled DAG with explicit framework-aversion rationale. v2 just shipped, naming subscription-absorbed multi-provider council as the differentiating practice.

Adopting Hermes Agent now would invalidate ~70% of the architectural decisions anima just locked. The features Hermes provides that anima needs are either already planned (hooks, skills, MCP, persistent memory) or are general-purpose features anima doesn't actually need for a per-run animation pipeline (voice mode, browser automation, scheduled tasks). The portfolio loss is real — anima becomes "I configured Hermes" instead of "I built this from scratch."

DeepSeek V4 Flash is a good model, free via Nous Portal, but it doesn't slot into anima's pinnacle phases (text-only, verbose, below Opus/Gemini on HLE). It's a candidate fourth T3 peer voice for a future bake-off — not a v2 lock.

**Recommendation:** Proceed with prompting Claude Code against v2's implementation prompt unchanged. Steal three Hermes patterns into anima's own implementation (agentskills.io skill standard, run-level MEMORY.md, gateway/plugin hook split). Add DeepSeek V4 Flash to the post-implementation bake-off list as a candidate fourth T3 peer (Open Q7). Don't switch orchestrator frameworks.

If anima ever outgrows the hand-rolled DAG and Sean genuinely wants the broader features Hermes provides (cross-platform Windows, voice mode, batch trajectory data for RL training), that's a future-anima decision worth re-evaluating when those needs are concrete and the museum walkthrough already has the bespoke-architecture-as-portfolio chapter shipped. Today, Hermes is the wrong primitive for the right reasons.

---

## 7. What this analysis is NOT saying

To avoid being misread:

- **Not saying Hermes Agent is bad.** It's good. Just not the right primitive for anima.
- **Not saying DeepSeek V4 Flash is bad.** It's a strong cheap-tier reasoning model. Just doesn't displace anima's locked assignments.
- **Not saying Nous Research is wrong.** They built a thoughtful product. The integration philosophy (one OAuth, 300+ models, unified billing) is well-designed.
- **Not saying Higgsfield's adoption proves Hermes is right for everyone.** Higgsfield is a cloud SaaS orchestrating 30+ visual tools with three-layer persistent memory. Anima is an open-source per-run pipeline with manifest-frozen content-addressed caching. Different shapes.
- **Not saying skip the agentskills.io spec.** Sean should adopt that standard explicitly — it's a real win for skill portability across his fleet.

---

*Final note: the question Sean asked — "Is it worth incorporating as the agentic harness for this workflow?" — has a clean answer. No, not as the harness. Yes, as a source of patterns to steal. Yes, as a tool to use outside anima for other workflows. Yes for DeepSeek V4 Flash as a future fourth T3 peer in a bake-off. v2 ships unchanged.*
