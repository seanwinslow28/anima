# Research Prompts — Orchestrator, Planner, and Judge Delegation Patterns

**Date:** 2026-05-26
**Purpose:** Two paste-ready research prompts that gate the next revision of [`docs/2026-05-25-agent-fleet-brainstorm.md`](../2026-05-25-agent-fleet-brainstorm.md) and [`docs/2026-05-25-agent-fleet-implementation-prompt.md`](../2026-05-25-agent-fleet-implementation-prompt.md). The brainstorm doc cost-tiered Phase 0 planning and the T2/T3 critic stack toward conservative model choices. Sean's correction: pinnacle phases (orchestration, planning, judging) deserve top-tier models, not bargain-tier ones. Run these to find how production fleets actually structure that delegation before revising the doc.
**Recipients:** Prompt A runs via the `gemini-deep-research` skill in `code-brain` (Gemini DR tier $2 predicted; DR Max tier $5–7 predicted; ~60 min wall-clock). Prompt B runs via the `llm-council` skill in `code-brain` (premium profile, four-vendor cross-ranking + chairman synthesis, ~$0.29/run; variance profile ~$0.14/run).
**Outputs land at:** `docs/research/2026-MM-DD-orchestrator-judge-delegation-{gemini-dr,llm-council}.md`.

---

## Prompt A — Gemini Deep Research / DR Max

```
ROLE
You are a research analyst surveying how production AI agent fleets — built by
solo creators, small teams, and companies — delegate three specific kinds of
tasks to large language models: (1) orchestration (the agent or controller that
holds run state and routes calls), (2) planning (agents that translate intent
into a structured plan + cost estimate before any compute is spent), and (3)
judging (agents that critique other agents' output and propose fixes).

CONTEXT
The reader is building a 10-phase 2D animation pipeline ("anima") with a single-
orchestrator-plus-named-stateless-tool-agents topology. The fleet includes a
planner agent (Phase 0), a T2 vision critic (per-frame and post-cut), and a T3
multi-CLI critic (post-animatic, pre-museum-publish). Reader has personal-
subscription access to Codex CLI (gpt-5.5), Anti-Gravity CLI (Gemini 3.1 Pro),
and Claude Agent SDK (Sonnet 4.6, Opus 4.7) — so the question is not "what can
we afford" but "where do top-tier models actually earn their keep, and what
goes wrong when teams cheap out on these specific phases?"

RESEARCH TASKS
Conduct deep research across academic literature (arXiv, ACL, ICML, NeurIPS),
practitioner sources (engineering blogs, GitHub repos, postmortems), and
production case studies dated November 2024 through May 2026. Surface specific
implementations by name with citations. Do not give field-level summaries; cite
named systems and the people who built them.

1. ORCHESTRATION DELEGATION
   - How do production agent fleets decide which model holds run state and
     routes calls between tools? Survey: Higgsfield Supercomputer, OpenAI
     Operator / Computer-Using Agent, Anthropic Computer Use, Cognition Labs
     Devin, Replit Agent, Cursor's multi-file edit orchestrator, LangGraph
     production deployments, AutoGen v0.4+, smolagents, Claude Agent SDK
     production deployments. For each: which model holds orchestration state,
     why that model and not a cheaper one, what failure modes the choice
     prevents.
   - Cite at least 8 named systems with sources.

2. PLANNING DELEGATION
   - What's the planner-agent design pattern that beats "single LLM emits a
     plan"? Survey: Self-Discover (Google DeepMind), Plan-and-Solve (NUS),
     Tree of Thoughts + verifier, Reflexion + planner, planner-worker-critic
     architectures from CAViAR / VISTA / Code2Video papers, Cognition's
     planning loop in Devin, Higgsfield's brief-plan-approve-execute. For
     each: model choice for the planner role, draft-then-pro escalation
     pattern (if any), cost-estimation accuracy targets, human-in-the-loop
     gate design.
   - Cite at least 6 named systems with sources.

3. JUDGING / CRITIC DELEGATION
   - How do production fleets choose which model judges other models? Survey:
     LLM-as-Judge canonical literature (Zheng et al. 2023, Chen et al. 2024,
     Anthropic Constitutional AI), G-Eval, Constitutional AI critic loops,
     AlpacaEval 2, ArenaHard, multi-model "council" patterns (Karpathy's
     llm-council, OpenAI's o-series reasoning-as-judge, Anthropic's reward
     modeling). When do production teams pick top-tier judges vs cheaper
     judges? What does the cost/quality curve look like? What specific
     failure modes does using a too-cheap judge introduce — false-positive
     pass-throughs, miscalibrated confidence, identity drift not flagged,
     style drift normalized?
   - Cite at least 8 named systems with sources.

4. CHAIRMAN / SYNTHESIS PATTERNS
   - When a fleet has multiple critics (vault-critic, llm-council, ensemble
     judges), how does it resolve dissent? Survey patterns: separate chairman
     call (synthesizes peer critiques), one peer designated as chair, tournament
     bracket, weighted vote by confidence, manual escalation to human. Cost
     and latency tradeoffs for each. Specific implementations with citations.
   - Cite at least 5 named systems.

5. COST/QUALITY CURVE
   - What does the published evidence say about diminishing returns when
     escalating from mid-tier to top-tier on orchestration / planning /
     judging specifically? Cite specific benchmark deltas where Opus/GPT-4.5/
     Gemini 3 Pro beat Sonnet/GPT-4o-mini/Gemini Flash on judge tasks (or
     don't). Where the top-tier premium is load-bearing vs decorative.

OUTPUT FORMAT
- Section per research task (1-5) with named implementations + citations
- Comparison table: "named system | role(s) | model(s) | rationale | source URL"
- Closing section: "Three recommended configurations for a solo-creator agent
  fleet with subscription-absorbed Claude + Codex + Anti-Gravity access" —
  budget-conscious / balanced / pinnacle-everywhere. For each: which model
  fills which role (orchestrator / planner / T2 critic / T3 peers / T3 chairman),
  estimated monthly cost on the subscription tier, expected wins/losses vs
  the other two configurations.
- All claims cite specific URLs + dates. No unsourced opinion. Where evidence
  is thin or contested, say so explicitly.

HARD RULES
- Cite URLs, paper titles, and publication dates for every named system.
- Do not recommend tools the reader already uses heavily as if novel: Claude
  Agent SDK, Codex CLI, Anti-Gravity CLI, MCP, Obsidian, Claude Code.
- Where reader is among the first practitioners (e.g., subscription-absorbed
  multi-vendor council for solo creators), say so — that's a portfolio
  positioning signal.
```

---

## Prompt B — LLM Council (premium profile)

Use the `premium` profile (Opus 4.7 chairman + GPT-5.5 + Gemini Pro + Grok 4.20 council). Per-query cap $1.00, daily $7, monthly $40 per `tools/llm-council/council/` config.

```
ROLE
Council members: each of you is a senior staff engineer who has built and
shipped production AI agent fleets at a company that values empirical model
selection. You have opinions about which models earn their keep at orchestration,
planning, and judging — and where teams waste money by over-tiering or
introduce silent quality failures by under-tiering.

QUESTION FOR THE COUNCIL
A solo creator is building a 10-phase 2D animation pipeline with a single-
orchestrator-plus-named-stateless-tool-agents topology. They have personal-
subscription access (no per-token billing constraint) to:
- Claude Agent SDK (Sonnet 4.6, Opus 4.7)
- Codex CLI (gpt-5.5)
- Anti-Gravity CLI (Gemini 3.1 Pro)
- ChatGPT Plus
- Google personal OAuth

They are choosing which model fills each role in the fleet:

1. ORCHESTRATOR — holds DAG state, routes calls between named-tool agents,
   manages content-addressed cache + tier escalation + retry ladder
2. PLANNER (Phase 0) — reads a free-text brief, emits a structured plan +
   cost estimate, gates compute spend on human approval
3. T2 VISION CRITIC — reviews per-frame image generation, post-Motion video,
   post-Assemble cut. Returns {verdict, reasoning, prompt_diff, confidence}.
   Runs ~10-50 times per shipped piece.
4. T3 PEER CRITICS (Codie via Codex, Annie via Anti-Gravity, Sage via Claude
   SDK) — independent variance critique at phase transitions. Run ~3-5 times
   per shipped piece.
5. T3 CHAIRMAN — synthesizes the three peer critiques into one merged finding
   with consensus + dissent map.
6. CHARACTER DESIGNER (Phase 2) — authors / refreshes Character Bible folders
   (anchor + turnarounds + expressions + costumes).
7. SCRIPTWRITER + STORYBOARD ARTIST (Phase 3) — brainstorm-pattern collab
   with the creator. Scriptwriter consumes a screenwriting-modes skill
   (Kaufman / Waititi / Miyazaki / Gerwig / Burnham mechanics). Storyboard
   Artist consumes the script + Bible.
8. MUSEUM WRITER — drafts the run's public-facing walkthrough as nodes
   complete.

CRITICAL TENSION
The creator's prior reasoning capped T3 at two peer voices because they
mistakenly assumed Claude SDK was not subscription-absorbed. With that
correction, T3 grows. The new question: where else is the cost ceiling
suppressing the right model choice on a pinnacle phase?

YOUR JOB
Each council member writes ~1500 words proposing the model assignment per
role above, with rationale. Explicitly call out:
- Where you would put Opus 4.7 and where Sonnet 4.6 is sufficient
- Where a CLI (Codex / Anti-Gravity) earns its keep over the SDK
- What goes wrong with under-tiering on each role
- Where the literature you've read or systems you've shipped contradict
  another council member's recommendation
- One non-obvious cross-role pattern (e.g., should the planner also act as
  the orchestrator? Should the chairman role rotate?)

CHAIRMAN'S ROLE (Opus 4.7)
After the council writes, synthesize into:
- Per-role recommendation with stated confidence
- Consensus map (where the council agrees) + Dissent map (where it splits)
- One paragraph identifying the single most important decision the creator
  is about to get wrong if they ship what's in the current brainstorm doc
- One paragraph on what the council would test empirically before locking
  the assignments (bake-off cases, ablation runs, etc.)
- Final config table: "role | recommended model | confidence | dissenting view"

NO TOOL-EVANGELISM
The creator already uses Claude Code, Codex CLI, Anti-Gravity CLI, MCP,
Obsidian, Claude Agent SDK heavily. Do not list these as recommendations
unless you're saying something specific about their use. New tools welcome
if they actually beat what's listed.
```

---

## After running

Both outputs land under `docs/research/`. The brainstorm doc and implementation prompt revisions read them before editing. The synthesis pattern from `docs/Image-Model-DR-2026/SYNTHESIS.md` is the model — cross-source SYNTHESIS doc at `docs/research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md` integrates both research outputs into one decision artifact.

What the revision will land:

1. T3 grows from 2 peers to 3 peers (Codie + Annie + Sage) + Opus 4.7 chairman — locked in this discussion, research confirms or refutes the chairman-vs-no-chairman question
2. Re-tier across pinnacle phases — Opus 4.7 candidates: Planner (Maya) pro tier, T2 Vision Critic (Em) bake-off rival, T3 Chairman. Research informs whether Opus is overkill anywhere or under-allocated anywhere else.
3. Phase 3 grows two personas: Sam (Scriptwriter) + Bea (Storyboard Artist). Research informs which model each gets.
4. Phase 5 Generate grows a model-router contract (Flo persona) consulting `manifest.yaml`'s `generation.routing:` block per [`docs/Image-Model-DR-2026/SYNTHESIS.md`](../Image-Model-DR-2026/SYNTHESIS.md) §2 + §5. Hero keyframes route to NB Pro; standard keyframes to NB2/GPT-Image-2; in-betweens to Seedream/SeedEdit/Qwen-IE/FLUX+LoRA per shot tag.
5. Cost ceiling table at brainstorm §6 rewrites — agent-fleet runtime is $0 incremental on Claude side; remaining spend lives in Phase 5 image gen + Phase 6 Seedance + Phase 2 Bible authoring + the Gemini-3-Pro side of Em's bake-off.
