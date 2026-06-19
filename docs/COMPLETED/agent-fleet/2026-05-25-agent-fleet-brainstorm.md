# Agent Fleet — Architecture Brainstorm

**Date:** 2026-05-25
**Skill:** `pm-product-discovery:brainstorm-ideas-existing`
**Scope:** The agents that fill anima's 10-phase architecture. Topology, named roles, T2 vision critic, T3 multi-CLI critic, prompt scaffolding, skill packaging, cost discipline. Out of scope: anything that modifies pipeline code, anything that re-decides the locked architecture.
**Inputs:** [`PHILOSOPHY.md`](../../../PHILOSOPHY.md), [`CLAUDE.md`](../../../CLAUDE.md), [`docs/pipeline-architecture-v1.md`](../../architecture/pipeline-architecture-v1.md), [`docs/2026-05-24-pipeline-v2-brainstorm.md`](../pipeline-v2/2026-05-24-pipeline-v2-brainstorm.md), [`docs/2026-05-24-pipeline-v2-change-map.md`](../pipeline-v2/2026-05-24-pipeline-v2-change-map.md), and the working code-brain references: [`agents-sdk/agents/vault_critic.py`](file:///Users/seanwinslow/Code-Brain/code-brain/agents-sdk/agents/vault_critic.py), [`agents-sdk/prompts/vault-critic-standing-context.md`](file:///Users/seanwinslow/Code-Brain/code-brain/agents-sdk/prompts/vault-critic-standing-context.md), and `agents-sdk/config.toml` (vault_critic + LLM Council blocks).

---

> ## ⚠ SUPERSEDED BY V2 (2026-05-26)
>
> **This document is the v1 draft. v2 lands the synthesis decisions at [`docs/2026-05-26-agent-fleet-brainstorm-v2.md`](2026-05-26-agent-fleet-brainstorm-v2.md).** Read v2 first for the current architecture lock. v1 is retained for historical context — the 18-idea ideation pass and the convergence to top-5 produced the structural decisions that v2 inherits. Do not implement against v1 unmodified.
>
> The corrections v2 lands — summarized below — were ratified by three research outputs ([Gemini DR Max](../../research/2026-05-26-Anima-Deep-Research-Gemini-DR-Max.md), [Perplexity DR](../../research/2026-05-26-Anima-Deep-Research-Perplexity-Deep-Research.md), [LLM Council premium](../../research/2026-05-26-orchestrator-judge-delegation-llm-council.md)) and a cross-source [synthesis](../../research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md).
>
> **What's wrong in v1, what changes in v2:**
>
> 1. **T3 critic stack — 2 voices → 3 peers + Opus chairman.** §3 TOP-5 incorrectly claims adding a third T3 voice "breaks the $0-incremental property because Claude SDK isn't subscription-absorbed." Sean's Anthropic subscription covers Claude Agent SDK use. T3 grows to *Codie (Codex / gpt-5.5) + Annie (Anti-Gravity / Gemini 3.1 Pro) + Sage (Claude SDK / Sonnet 4.6)* as peers, plus an *Opus 4.7 chairman* synthesis call. All four subscription-absorbed. Mirrors `tools/llm-council/council/`'s premium-profile chairman pattern.
> 2. **Best models on pinnacle phases — re-tier the cost ceiling table at §6.** Sean's directive: orchestration, planning, and judging phases deserve top-tier models, not bargain-tier. Planner (Maya) pro-tier becomes Opus 4.7, not Sonnet. T2 vision critic (Em) bake-off becomes three-way (Sonnet 4.6 vs Gemini 3 Pro vs Opus 4.7), not two-way. Cost picture inverts: agent-fleet runtime is mostly $0 incremental on Claude side; remaining spend lives in image gen + Seedance + Bible authoring + the Gemini-3-Pro side of Em's bake-off.
> 3. **Phase 3 Storyboard un-defers — two new personas: Sam (Scriptwriter) + Bea (Storyboard Artist).** §3 TOP-5's persona table marks Storyboard Artist "deferred — Sean mostly authors." Sean corrects: Phase 3 is a team effort, brainstorm-pattern collaboration. Sam uses the in-progress `script-writing` skill (Kaufman / Waititi / Miyazaki / Gerwig / Burnham masters per the [skill upgrade plan](file:///Users/seanwinslow/Code-Brain/code-brain/vault/40_knowledge/references/screenwriting-skill-building/voice-modes-integration-and-upgrade-plan.md)). Bea consumes Sam's draft + the Character Bible and produces shot composition + camera + visual blocking.
> 4. **Phase 5 Generate is a routed pipeline, not a single-model contract.** Add persona Flo (frame generator) that consults a `manifest.yaml` `generation.routing:` block. Hero keyframes → NB Pro (~$0.15). Standard keyframes → NB2 or GPT-Image-2 (~$0.07). Cheap in-between edits → Seedream 4.0 / SeedEdit 3.0 on fal.ai (~$0.007–0.03, 80% cost cut). Mid in-betweens → Qwen-Image-Edit-2511 ($0.021/img on fal.ai). Self-hosted (24GB) → FLUX.1 Kontext [dev] FP8 + character LoRA + Shakker sketch LoRA + PuLID-FLUX. Routing source: [`docs/Image-Model-DR-2026/SYNTHESIS.md`](../../Image-Model-DR-2026/SYNTHESIS.md) §2 + §5.
> 5. **Research pass completed 2026-05-26.** Three outputs landed: Gemini DR Max (278 lines, 90 sources), Perplexity DR (408 lines, production-case-study density), LLM Council premium-profile with Opus 4.7 chairman synthesis ($0.52 / 286s / 29K input tokens). Cross-source [synthesis doc](../../research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md) integrates them. v2 brainstorm doc lands the decisions.
>
> Everything else in v1 is correct as written. Do not re-implement v1; v2 at [`docs/2026-05-26-agent-fleet-brainstorm-v2.md`](2026-05-26-agent-fleet-brainstorm-v2.md) is the current artifact. Implementation handoff at [`docs/2026-05-26-agent-fleet-implementation-prompt-v2.md`](2026-05-26-agent-fleet-implementation-prompt-v2.md).

---

## 1. Opportunity Frame

The architecture lock (commit 1) declares where critics live, what they cost, and what they produce. It does not say *who* runs at each checkpoint, what their voice is, how they're wired into the runner, or how they share context with each other. Five named checkpoints sit empty. Two of the nine commits (8 + 9) wait on this brainstorm to decide what fills them.

The question isn't "what models do we use." That gets decided by eval bake-offs under `evals/bakeoffs/`. The question is the shape *around* the models — the topology, the personas, the contracts, the cost ceilings, the standing context every agent carries with it. Pick a shape too rigid and the fleet calcifies the first time a new model lands. Pick a shape too loose and every agent has its own contract and the DAG can't compose them.

Three pre-existing patterns are the source material:

- **Higgsfield Supercomputer's brief-plan-approve-execute** — one orchestrator that holds state, many stateless routes called when needed. Already cited in `PHILOSOPHY.md` as the Phase 0 ancestor.
- **OiiOii's 7-agent crew** — Art Director, Scriptwriter, IP Designer, Character Designer, Scene Designer, Storyboard Artist, Sound Director. Named roles with credits-roll vibe. Output sits closer to "the work feels like it had a crew" than to "the orchestrator picked routes."
- **Krea Node Agent's DAG with a single planner** — content-addressed node graph, one planner agent, surgical re-runs. Already absorbed into anima's commit 4 plan.

And — equally load-bearing — Sean's own two patterns from `code-brain` that the kickoff prompt called out by name:

- **`vault_critic.py`** — asyncio parallel fan-out to Codex CLI (gpt-5.5) and Anti-Gravity CLI (Gemini 3.1 Pro), $0 incremental on personal subscriptions, standing-context preamble + per-target supporting-doc injection, status promotion semantics (ok / partial / success-empty / error), manual-mode bypass. The single most directly transferable artifact in this brainstorm.
- **`llm-council`** — multi-vendor cross-ranking with chairman synthesis. Two profiles (premium ~$0.29/run, variance ~$0.14/run). Per-query / daily / monthly caps. The shape T3 wants to grow into eventually if subscriptions stop being the right primitive.

The opportunity frame: take the patterns that already work in code-brain, transplant them into anima with the right named-role packaging, and lock the typed contracts now so commits 4 through 9 wire against a stable target.

---

## 2. Ideation — Three Perspectives, 18 Ideas

Five per perspective floor, plus a small anti-bias rotation pass at the end to catch ideas the role-priors suppressed. Tables for the inventory; prose for the ones that win or earn promotion.

### Product Manager perspective — business value, strategic alignment, customer impact

| # | Idea | One-line |
|---|------|----------|
| PM-1 | **Critic-as-skill-package** | Every critic ships as a standalone skill under `.claude/skills/` mirroring how `seedance-prompting` was extracted. The fleet's parts are independently invokable; future projects use the critics without the full anima runner. |
| PM-2 | **Bake-off-as-portfolio-content** | Each model decision (Sonnet vs Gemini 3 Pro for T2, Codex vs Anti-Gravity for T3, possible Claude SDK as a third T3 voice) ships a dated bake-off under `evals/bakeoffs/` that becomes museum content. The empirical record is the portfolio asset, not the model winner. |
| PM-3 | **Standing-context preamble per agent** | Lift the vault-critic standing-context pattern wholesale. Each anima agent (planner, vision critic, CLI critic, character designer, storyboard artist) gets a 1–2 page preamble: what anima is, who Sean is, what's already locked, the failure modes to avoid. Cuts the generic-recommendation collapse Sean already hit in code-brain. |
| PM-4 | **Budget gate as a manifest field** | Every agent declares per-call / daily / monthly USD cap in `manifest.yaml`. Planner uses these to compute the Phase 0 cost preview. Runtime enforcement marks over-cap runs `status: budget-deferred` and surfaces them in the museum's decision log. |
| PM-5 | **Single orchestrator + named-tool agents** | The fleet is one orchestrator (the DAG runner from commit 4) calling N named-but-stateless tools. Critics are tools. Planner is a tool. Character Designer is a tool. No inter-agent messaging. Sean conducts; the agents play section. |

### Product Designer perspective — UX/delight (Sean as user of his own tool)

| # | Idea | One-line |
|---|------|----------|
| DES-1 | **Prompt-diff cards, not pass/fail badges** | Every T2 critic finding renders in the museum as a card: original prompt + proposed diff (red-strike + green-add) + reasoning + accepted/rejected state. Pass/fail is the failure mode the philosophy explicitly names — this is the structural fix. |
| DES-2 | **Named-role personas with voices** | Each agent has a name and a voice. The Planner is *Maya, line producer*. The Character Designer is *Cy*. The Vision Critic is *Em, script supervisor*. The CLI Critics are *Codie and Annie* (sister-critics, different schools). Sean's `writing-voice-modes` skill is the empirical proof that named voices change output. Risk: cute-naming-trap — mitigated by tying each voice to a single concrete function. |
| DES-3 | **Director's chair UX — one approval surface** | All gates (brief approval, animatic, per-frame, per-shot, full cut, final) queue into a single review surface (terminal-based to start, an Astro mini-page later). Sean clears them in batches instead of context-switching between phases. |
| DES-4 | **Critic dissent as a feature** | When T3's two CLI critics disagree, the museum surfaces both critiques side by side as a *split decision* card. Disagreement isn't noise — it's where the most interesting taste calls happen. Mirrors LLM Council's variance surfacing. |
| DES-5 | **Fleet introspection sketch** | A `fleet status` command (or meta-agent) renders the current run's agent activity as a Steadman-style sketch: who's running, who's done, who's blocked, what each just said. Sean glances at it the way he glances at his daily-driver morning brief. |

### Software Engineer perspective — technical possibilities, scale, data leverage

| # | Idea | One-line |
|---|------|----------|
| ENG-1 | **T3 via subprocess CLI shell-out (vault-critic pattern transplanted)** | Codex CLI + Anti-Gravity CLI via `asyncio.gather` subprocess fan-out. $0 incremental on subscriptions. Per-CLI 120s timeout, 600s wall budget, both-rate-capped → `status: partial`. Adapts directly from `agents-sdk/agents/vault_critic.py`. |
| ENG-2 | **T2 vision critic via Claude SDK, multimodal input** | Single agent. Accepts image + beat description + style guide. Returns `{verdict, reasoning, prompt_diff, confidence}`. Sonnet 4.6 default; Gemini 3 Pro as commit 8b bake-off rival. Cost target ~$0.01–0.05/call. |
| ENG-3 | **Typed `AgentSpec` Protocol** | Every agent declares inputs/outputs/cost-estimate/run signature so the DAG runner can wire critics, planner, character designer the same way. Tier (`draft \| pro`) is a field on `AgentResult`. Replaces ad-hoc scripts with a teachable, testable shape. |
| ENG-4 | **Local-first routing per agent (HybridRouter)** | Borrow code-brain's `lib/hybrid_router.py`. Each agent declares preferred local model (e.g. `qwen3-14b` for planner draft, `qwen3-vl:8b` for cheap vision pre-screening). Cloud fallback configurable; `fallback_disabled=true` for cost-strict workflows. Museum badges show "we ran this locally" where it ran. |
| ENG-5 | **`proposed_patches` feedback loop into manifest** | When T2 proposes a prompt diff, the patch lands in `manifest.lock.yaml` as a pending `proposed_patches: [...]` entry. Sean reviews via DES-3 director's chair, accepts/rejects. Accepted patches mutate manifest + trigger surgical DAG re-run on affected nodes only (content-hashed cache keeps the rest warm). |

### Anti-bias rotation — three more, with role assumptions inverted

The first 15 ideas land in obvious lanes. The PM thought about value, the Designer thought about UX, the Engineer thought about contracts. That bias suppresses ideas that bridge lanes. Three more, intentionally cross-cast:

**ENG-6 — Hooks system on the DAG runner for capture + eval triggers.** Borrow the Claude Code hook pattern (PreToolUse / PostToolUse). Every agent fires `post_run` events; subscribers include museum capture, eval recorders, the orchestrator. Avoids hardcoding museum-write logic inside each agent — architecturally cheaper than wiring every agent to the museum by hand, and the only sane way to add future subscribers (Slack notifications, Spotify-handoff TTS, etc.) without surgery.

**PM-6 — Skill optimizer against each agent's prompt template.** Borrow `agents-sdk/agents/skill_optimizer.py` — Opus 4.7 generator + Qwen3-14B local judge with periodic Sonnet check, hard cap $200/run. Run it against each anima agent's prompt template every N weeks. Closed-loop quality improvement that survives model swaps; produces a dated eval trace as a museum artifact each time. Worth naming now, build later.

**DES-6 — Vibe-check meta-agent on the museum itself.** A small Haiku-or-local agent reads the finished museum walkthrough and flags moments where the AI output won and the manual reference lost, or vice versa, for Sean's review. Not a critic *at the production pipeline* — a critic *at the meta-pipeline*. Trains Sean's own taste articulation by surfacing cases that contradict his prior. Cute and probably premature; logged for completeness.

Eighteen ideas total. Anti-bias rotation pulled the hook system, skill-optimizer reuse, and meta-museum vibe-check out of the suppressed-by-role bucket — none of them would have surfaced from inside their original lanes.

---

## 3. Prioritized Top 5

Scored on alignment with the human + AI partnership thesis · impact on commits 8 and 9 unblock · feasibility at solo scale · differentiation from generic AI-pipeline patterns. Each winner gets a name, a paragraph, a selection rationale, and the assumptions that have to hold for it to ship.

### **TOP-1 — T3 multi-CLI critic via subprocess shell-out (from ENG-1)**

The vault-critic pattern transplanted: `pipeline/critics/cli_critic.py` runs Codex CLI (gpt-5.5) and Anti-Gravity CLI (Gemini 3.1 Pro) in parallel via `asyncio.gather`, with per-CLI 120s timeout and a 600s wall budget. Inputs are the artifact under critique (the animatic shape-block at the 4→5 checkpoint; the rendered museum walkthrough at the pre-publish gate), the standing-context preamble, and any supporting-doc injections from `manifest.yaml`'s `critics.t3.default_context_files` list. Outputs are two structured critiques + an agreement score + an adjudication note, written as a comparison-card under `museum/{project_slug}/critics/` and as a `proposed_patches:` entry on the run's manifest. Status promotion mirrors vault-critic verbatim: `ok` / `partial` / `success-empty` / `error`.

**Why selected.** This is the spine of commit 9 and it's already working in code-brain — the only adaptation work is that targets become images and videos instead of markdown, and the output format becomes prompt-diff cards instead of expansion files. $0 incremental on Sean's existing ChatGPT Plus + Google personal OAuth. Proven pattern Sean already trusts at the daily-cron level. Differentiation move: every other AI animation pipeline uses one critic; T3 surfaces *variance between independent eyes* as the most useful artifact, which is the strongest read on whether anima's museum claims hold up under independent scrutiny.

**Key assumptions to validate.**
- Codex CLI + Anti-Gravity CLI both accept image/video input with a usable resolution ceiling (Codex's multimodal path works; Anti-Gravity's vision routing needs verification before commit 9 starts).
- Per-CLI 120s timeout holds for vision-input prompts at the animatic and museum-walkthrough scale (markdown critique runs ~30–60s today; image critique may extend).
- Status `partial` is acceptable as the most common outcome during early ship — Sean's already used to it from vault-critic, so this is mostly an expectations note for the museum's reliability framing.

---

### **TOP-2 — T2 vision critic via Claude SDK with multimodal input (from ENG-2)**

A single agent, `pipeline/critics/vision_critic.py`, that accepts a frame (or a Seedance shot's representative frame, or a full assembled cut's keyframes) plus the beat description, the style guide, and the relevant Character Bible sheets. Returns a structured `{verdict: pass | borderline | fail, reasoning, prompt_diff: list[str], confidence: float}`. Runs at every per-frame Generate checkpoint, every post-Motion gate, and every post-Assemble gate. Sonnet 4.6 is the production default; commit 8b ships a dated bake-off against Gemini 3 Pro under `evals/bakeoffs/2026-MM-DD-sonnet-vs-gemini-vision-critic/`. The prompt-diff list is the critic's *proposed fix*, not a verdict — pass/fail without proposed fixes is the failure mode the philosophy explicitly forbids.

**Why selected.** Commit 8. Without this, T2 is a flag-raiser, which the philosophy refuses. Three checkpoints depend on it (per-frame Generate, post-Motion, post-Assemble) — without T2, Phase 6 Motion has the gap the architecture doc names by hand: *"Seedance motion currently isn't QA'd beyond visual review."* Empirical model selection (the bake-off) is itself portfolio content; the loser's failure modes are part of the museum.

**Key assumptions to validate.**
- Sonnet 4.6 multimodal latency at the per-frame scale is ≤15s/call and cost is ≤$0.05/call. Code-brain's vault-synthesizer already ships at Sean's volume with Sonnet — vision adds tokens but probably not catastrophically.
- A structured prompt-diff is mergeable into a Gemini NB2 prompt without a separate diff-applier — i.e., the critic's diff format and NB2's prompt format align well enough that a programmatic patch works. If not, the diff degrades to "rewrite proposal" and the loop gets one step longer.
- Gemini 3 Pro accepts the same prompt shape — required for the bake-off to be apples-to-apples. Verify in the first hour of commit 8.

---

### **TOP-3 — Named-role personas + standing-context preamble per agent (combined from PM-3 + DES-2)**

PM-3 and DES-2 share an artifact, so they merge. Each agent gets a 1–2 page preamble at `agents-sdk/prompts/{role}-standing-context.md` (or, for anima specifically, `pipeline/agents/prompts/{role}-standing-context.md`). The preamble carries: *who you are* (named-role persona — Maya the line producer; Cy the character designer; Em the script supervisor; Codie and Annie the sister-critics), *what anima is* (the philosophy's load-bearing claims, condensed), *who Sean is* (the writer-director, not the prompter), *what's already locked* (the 10-phase architecture, the critic stack, the Character Bible primitive), and *the failure modes to avoid* (generic recommendation collapse, template-trap drift, recommending tools Sean already uses). Every agent prompt auto-prepends its preamble; per-target supporting-doc injection (the relevant phase doc, the beat description, the Character Bible folder contents) layers on top — same pattern as `default_context_files` in vault-critic's config block.

**Why selected.** Sean has empirical evidence from two places that named voices change output quality: the `writing-voice-modes` skill (five disciplined modes producing measurably distinct prose) and the vault-critic Round 3 enrichment (preamble + supporting docs cut the generic-recommendation failure mode that ablation runs confirmed). Differentiation move: every other AI animation pipeline treats agents as anonymous LLM calls; anima credits them like a film crew, and the credits affect output quality. The museum walkthrough renders the credits roll as a real artifact — "Animatic critique by Codie & Annie; vision QA by Em; line production by Maya" — turning the agent fleet from infrastructure into part of the story.

**Key assumptions to validate.**
- Named-role personas produce *better* output, not just *cuter* output. Worth running a small ablation early — same prompt with and without the persona framing, scored by Sean on three real frames.
- The preamble + supporting-doc token budget stays under ~12K tokens combined (vault-critic's ceiling sits at ~10K; anima's preambles will be slightly longer because the architecture is richer). If it blows past 16K, prune supporting docs aggressively.
- Sean's tolerance for the cute-naming-trap holds. If the personas feel forced six weeks in, the names retire and the role-shapes stay. The architecture must survive a name change.

---

### **TOP-4 — Typed `AgentSpec` Protocol with `proposed_patches` feedback loop (combined from ENG-3 + ENG-5)**

ENG-3 and ENG-5 are two halves of the same contract, so they merge. Every agent declares a typed `AgentSpec` (a Python `Protocol`): `inputs: dict`, `outputs: dict`, `cost_estimate: CostEstimate`, `run(ctx) -> AgentResult`. Tier (`draft | pro`) is a field on `AgentResult`. The DAG runner from commit 4 only knows about `AgentSpec` — it doesn't care whether the agent inside is a Claude SDK call, a Codex CLI shell-out, a local Ollama probe, or a tiny pure-Python rule check. Critics, planner, character designer, storyboard-artist, museum-writer all wire the same way. When a T2 critic proposes a prompt diff, the patch lands in `manifest.lock.yaml` as a pending `proposed_patches: [...]` entry; Sean reviews via the director's chair (DES-3, deferred but on the roadmap); accepted patches mutate the manifest and trigger surgical DAG re-runs on affected nodes only (content-hashed cache keeps the rest warm). Closes the loop the philosophy promised: *the critic earns its keep when it proposes fixes*.

**Why selected.** Foundation pattern that makes commits 8 and 9 wire cleanly into commits 4 and 5. Without this, each agent has its own contract and the DAG can't compose them — every agent becomes a special case in the runner. With this, agents become teachable, swappable, evaluable, and the runner stays simple. The `proposed_patches` loop is the structural answer to "critic proposes fixes": it gives critic findings a real home in the manifest rather than a log line that decays.

**Key assumptions to validate.**
- A single `AgentSpec` Protocol can express both fast deterministic agents (T1 rule gates, ~100ms) and slow multimodal agents (T2 vision, ~15s) without bloating the contract. The Protocol pattern in Python is structurally typed — runtime overhead is zero, design overhead is real but bounded.
- `proposed_patches` as a YAML list entry doesn't conflict with the existing manifest schema (it doesn't — it's additive, lands inside the `critics:` block as a sub-key).
- Sean's review tempo on `proposed_patches` is realistic — i.e., he actually clears the queue rather than letting it grow into a graveyard. Director's chair UX (DES-3) addresses this when it ships.

---

### **TOP-5 — Single orchestrator + named-tool agents, Krea topology + OiiOii credits-roll + Higgsfield runtime (from PM-5)**

The topology question gets a synthesis answer. The runtime shape is Higgsfield's: one orchestrator (the DAG runner from commit 4) holds the manifest + DAG state and calls N named-but-stateless tools. The graph shape is Krea's: typed nodes, content-addressed cache, partial re-runs. The credits-roll shape is OiiOii's: every named role gets billing in the museum walkthrough. There is no inter-agent messaging. Critics don't talk to each other; the orchestrator routes between them. Maya doesn't message Cy; the orchestrator calls each in turn. Sean is the only conductor; the agents are the section players. The full named-role roster, taken from the 10-phase architecture rather than from OiiOii's catalogue:

| Phase | Role | Persona |
|-------|------|---------|
| 0 — Brief & Plan | Planner | Maya, line producer |
| 2 — Character Bible | Character Designer | Cy |
| 3 — Storyboard | Storyboard Artist | (deferred — Sean mostly authors) |
| 4 → 5 — Animatic gate | CLI Critics (T3) | Codie + Annie |
| 5 — Generate | Vision Critic (T2) | Em, script supervisor |
| 6 — Motion | Vision Critic (T2) | Em |
| 8 — Assemble | Vision Critic (T2) | Em |
| pre-publish — Museum | CLI Critics (T3) | Codie + Annie |
| (orthogonal) | Museum Writer | Mo |

**Why selected.** Locks the topology question explicitly. NOT a 7-agent crew with inter-agent state — that's coordination overhead Sean's solo workflow can't absorb. NOT a pure DAG with no agent layer — that's anonymous and the museum loses its credits roll. The synthesis matches Sean's actual coordination capacity (one human, one conductor surface, many named players) and survives model swaps cleanly (the persona stays; the model behind it changes). The persona names are decoration if you strip them; the role-shapes are load-bearing if you keep them. Both are right.

**Key assumptions to validate.**
- The orchestrator-plus-tools topology survives the moment one agent's output needs to be consumed by another (e.g., the Character Designer's Bible feeds the Vision Critic). This is fine as long as the orchestrator threads outputs through the manifest, which the DAG runner already does. No inter-agent state.
- Two T3 CLI critics is the right number. One is too brittle (single point of failure on a $0-budget agent); three (adding Claude SDK as a third voice) breaks the $0-incremental property because Claude SDK isn't subscription-absorbed. Two stays.
- The deferred Storyboard Artist persona is the right call. Sean's brainstorm notes already flag storyboarding as mostly human-authored. If the persona is needed later, the role-shape exists; for now, the Storyboard phase has no named agent and that's fine.

---

## 4. Deferred, Not Rejected

| Idea | Why deferred |
|------|--------------|
| DES-3 Director's chair UX | Promote when the manifest of pending gates grows past one-screen; for early commits 8–9, a terminal print-and-prompt covers it |
| DES-4 Critic dissent surfacing | Comes for free out of TOP-1 if the museum walkthrough is set up right — DES-4 is the rendering, TOP-1 is the data |
| DES-5 Fleet introspection sketch | Wait for the fleet to exist; meta-agent comes second |
| DES-6 Vibe-check meta-agent | Premature optimization; revisit after the first museum walkthrough ships |
| PM-1 Critic-as-skill-package | Nice eventually; not gating commits 8–9. Land after the patterns settle and one critic clearly wants to live outside anima |
| PM-2 Bake-off-as-portfolio-content | Happens automatically inside commit 8b if TOP-2 ships clean — promoted to *expected output*, not separate work |
| PM-4 Budget gate manifest field | Schema lands here in this brainstorm; runtime enforcement is a follow-up after the agents exist to be gated |
| PM-6 Skill optimizer for prompt evolution | $200/run cap is too expensive for this stage; revisit post-MVP when the museum has enough runs to evaluate the optimizer's wins |
| ENG-4 Local-first routing | Promote when latency or cost becomes a real pinch; cloud Sonnet is fine for commits 8–9. The HybridRouter pattern is available when needed |
| ENG-6 Hooks system on DAG | Depends on commit 4 (DAG runner); land it alongside or just after |

---

## 5. Topology — Locked

The kickoff prompt asked for an explicit locked answer on topology. Here it is, written down so future sessions don't re-litigate it.

**The fleet is one orchestrator calling N named-but-stateless tools.** The orchestrator is the DAG runner from commit 4 — it holds the manifest, the DAG state, the content-addressed cache, the museum's hook subscribers. The tools are agents that declare typed `AgentSpec` contracts and otherwise know nothing about each other. Inter-agent messaging is forbidden by construction; the orchestrator routes between them. Every agent gets a named persona for museum credits-roll purposes and a standing-context preamble that loads its role-specific framing. Tier escalation (`draft → pro`) is a field on `AgentResult`, evaluated by the orchestrator against the manifest's `tiering:` block.

This is Higgsfield's runtime shape, Krea's graph shape, OiiOii's credits-roll shape, and Sean's vault-critic data contract — fused. None of them alone is correct at anima's scale; the fusion is.

What this rules out:
- **No multi-agent collaborations.** Maya does not call Cy. The orchestrator calls Maya, then calls Cy, threading outputs through the manifest.
- **No inter-agent state.** Each agent run is stateless. State lives in the manifest, the run directory, and the cache.
- **No agent-of-agents pattern.** There is no super-orchestrator that runs sub-orchestrators. One layer.

What this leaves open for future work:
- **Adding agents.** A new named role (e.g., Color Director, Sound Designer when audio enters the pipeline) is a new `AgentSpec` + a new persona file + a new manifest entry. No structural change required.
- **Swapping models.** A persona stays; the model behind it changes through a bake-off; the museum logs the swap with a dated entry.
- **Tier promotion.** A T2 agent can become a T1+T2 agent without runtime changes (it just gains a deterministic-rule sibling at the same checkpoint).

---

## 6. Cost Discipline — Schema, Locked

The kickoff asked for explicit cost ceilings per agent. Schema lives in `manifest.yaml`'s `critics:` block now; the values below are the proposed defaults the implementation commits should ship with. Runtime enforcement (the `status: budget-deferred` path) is a follow-up commit; for commits 8–9 the values exist to constrain bake-off design and to surface in Phase 0's cost preview.

| Agent | Tier | Cost per call | Daily cap | Monthly cap | Notes |
|-------|------|---------------|-----------|-------------|-------|
| T1 rule gates | T1 | $0 | $0 | $0 | Deterministic; no model |
| Vision Critic (Em) | T2 | ≤$0.05 | $5 | $40 | Sonnet 4.6 default; Gemini 3 Pro bake-off |
| CLI Critics (Codie + Annie) | T3 | $0 incremental | $0 incremental | $0 incremental | Subscription-absorbed (ChatGPT Plus + Google personal OAuth) |
| Planner (Maya) | draft | ≤$0.02 | $1 | $10 | Haiku |
| Planner (Maya) | pro | ≤$0.20 | $2 | $20 | Sonnet |
| Character Designer (Cy) | draft | ≤$0.10 | $2 | $15 | NB2 calls, 2–3 anchor angles |
| Character Designer (Cy) | pro | ≤$0.50 | $5 | $30 | NB2 calls, full Bible authoring |
| Museum Writer (Mo) | — | ≤$0.05 | $2 | $15 | Sonnet, run-end synthesis only |

Total monthly ceiling at full pro tier across all agents: ~$130/month. Below the LLM Council premium-profile's $40/month cap as a single point of reference. Well within Sean's existing tolerance for the daily-driver fleet (~$27/month cap on the morning agent alone).

The T3 CLI critics' $0-incremental property is what justifies running them on every phase-transition gate without rationing. Two voices on every gate, $0/run, ~120s wall-clock — same envelope as the vault-critic nightly cron.

---

## 7. Architecture Implied by Top 5 (Strawman)

The 10-phase architecture stays untouched. What changes is *who fills which slot*. Decorated diagram, with personas in their role-positions:

```
Phase 0   BRIEF & PLAN       Maya (Planner, Haiku draft / Sonnet pro) → human approval gate
Phase 1   SCAFFOLD           orchestrator-only
Phase 2   CHARACTER BIBLE    Cy (Character Designer, NB2 draft / pro)
Phase 3   STORYBOARD         human-authored; orchestrator-only on the agent side
Phase 4   ANIMATIC           human-authored shape-block
                             ⚖ T3 — Codie + Annie review timing arc before downstream burn
Phase 5   GENERATE           NB2 stills, DAG-orchestrated
                             ⚖ T1 (rule gates) + T2 — Em proposes prompt diffs per frame
Phase 6   MOTION             Seedance Fast→Pro
                             ⚖ T2 — Em reviews motion arc + identity drift in video
Phase 7   AUDIT              orchestrator consolidation; routes critic findings to retry ladder
Phase 8   ASSEMBLE           FFmpeg, comparison GIFs, museum hooks fire
                             ⚖ T2 — Em reviews loop coherence + pacing
Phase 9   QA REVIEW          human; creative-director skill assists

(parallel)  MUSEUM            Mo (Museum Writer) drafts walkthrough as nodes complete
                              ⚖ T3 — Codie + Annie review narrative + comparison artifacts before publish
```

Five named personas (Maya, Cy, Em, Codie, Annie, Mo — okay, six). One orchestrator. Zero inter-agent messages. Standing-context preamble per role. `proposed_patches` feedback loop into the manifest. $0 incremental on every T3 gate. The 10-phase architecture lock holds; the agent fleet now has names, contracts, and cost ceilings.

---

## 8. Open Questions Reserved for Implementation Sessions

These are *not* for this brainstorm to decide. They live in the commits that implement Top-1 through Top-5.

**Q1 — Which model wins T2?** Decided by commit 8b's dated bake-off. Sonnet 4.6 ships as the default while the bake-off runs. The bake-off is the artifact; the winner is a footnote.

**Q2 — When a T2 prompt diff is accepted, does it auto-merge into the manifest or stage as a `proposed_patches:` entry first?** Default to staging. Auto-merge becomes an option later via a per-checkpoint `auto_apply: true` field in the manifest's `critics:` block. Stage-first preserves Sean's veto.

**Q3 — Where do Codie and Annie's CLIs run?** Codex CLI uses Sean's ChatGPT Plus account; Anti-Gravity CLI uses his Google personal OAuth. Same setup as `code-brain/agents-sdk`. Likely the existing config transfers; verify in commit 9's first hour.

**Q4 — One shared `anima-standing-context.md` or per-role files?** Hybrid. One shared anima-wide preamble (`pipeline/agents/prompts/anima-standing-context.md`) + per-role addendum (`pipeline/agents/prompts/{role}-standing-context.md`). The shared file carries the philosophy + locked architecture; the addendum carries role-specific framing. Same pattern code-brain already uses for vault-critic's `standing-context.md` + `default_context_files`.

**Q5 — Status promotion semantics for anima agents.** Bring `vault_critic.py`'s vocabulary over verbatim — `ok` / `partial` / `success-empty` / `error`. Add one anima-specific: `budget-deferred` for over-cap runs (PM-4 follow-up).

**Q6 — Per-agent eval suite under `evals/`.** Each commit lands its agent's eval suite alongside (commits 3b, 8b, 9b). Cases grounded in real production logs (Act 2 Seedance run is the corpus to mine). The discipline from `code-brain/evals/vault-synthesizer/` transfers: intentionally-red baseline + pre/post-fix delta + portfolio-grade README. No agent ships without a baseline trace in `evals/{agent}/traces/baseline-*.md`.

**Q7 — Animatic critic inputs.** When Codie + Annie review the animatic at the 4→5 gate, do they get raw shape-block frames, an assembled animatic video, or both? Both. Codie reads the assembled animatic clip; Annie reads the per-frame shape-block PNG sequence. Different inputs surface different failure modes, which is exactly the variance T3 exists to capture.

---

## 9. What's Next

Implementation handoff: [`docs/2026-05-25-agent-fleet-implementation-prompt.md`](2026-05-25-agent-fleet-implementation-prompt.md) — paste-ready continuation prompt for the next Claude Code session.

Commit dependencies after this brainstorm:

- **Commit 4 (DAG runner)** — lands the `AgentSpec` Protocol from TOP-4. Foundation for everything downstream.
- **Commit 8 + 8b (T2 vision critic + bake-off)** — implements TOP-2 against the `AgentSpec` from commit 4. Persona file for Em lands here (TOP-3). `proposed_patches` writeback (TOP-4) wires here.
- **Commit 9 + 9b (T3 CLI critics + eval)** — implements TOP-1. Persona files for Codie + Annie land here. Same `AgentSpec` contract as Em.

Brainstorms that should happen along the way:
- **Character Bible scaffolding** (gates commit 2) — Cy's persona + character.yaml schema + authoring workflow
- **Multimodal vault / RAG** — embedding model choice (Gemini Embedding 2 vs OpenRouter), Obsidian integration, content-addressed asset store
- **Museum showcase format** — Mo's persona + Astro content-collection MDX schema + comparison-GIF rendering

The pressure-test session (kickoff Option A) is also still on the table — multi-perspective critique of the architecture lock before more building. Worth doing once Top-1 through Top-5 ship and the architecture has real agents inside it; doing it before is too early to find the interesting failure modes.

---

*Last updated 2026-05-25. The architecture is locked; the agent fleet now has names, contracts, and cost ceilings. Implementation begins with commits 4 → 8 → 9.*
