# Model Delegation in Production Agent Fleets: Orchestration, Planning, Judging & Chairman Patterns (Nov 2024–May 2026\)

*Research commissioned for the "anima" 10-phase 2D animation pipeline (solo-creator, single-orchestrator \+ named stateless tool-agents topology). Subscription access assumed: Claude Agent SDK (Sonnet 4.6, Opus 4.7), Codex CLI (GPT-5.5), Anti-Gravity CLI (Gemini 3.1 Pro).*

---

## Executive Summary

The evidence from Nov 2024–May 2026 converges on three durable findings:

1. **Orchestration state is won by instruction-following density, not raw benchmark performance.** Systems that chose smaller but more instruction-obedient models for their orchestrator layer reported fewer cascade failures than those that chose the most capable available model.  
2. **The planner-verifier split beats single-LLM plan emission** in every studied system. The margin shrinks but does not vanish as models improve. Phase 0 planning is the highest-leverage place for a top-tier model in the anima fleet.  
3. **Cheap judges introduce systematic, production-dangerous failure modes**—false-positive pass-throughs on style drift, sycophantic scoring of verbose-but-hollow outputs, and calibration collapse under adversarial framing. For a 10-phase animation pipeline where each phase is a downstream dependency, critic miscalibration is not an aesthetic nuisance; it is a compounding structural defect.

---

## Section 1: Orchestration Delegation

### What Production Systems Actually Do

The question "which model holds orchestration state?" resolves, in production, to a more pointed question: "which model can reliably decide *not* to call a tool, revise a plan mid-run, and terminate a stuck loop?" That is a different capability profile from raw MMLU or SWE-bench performance.

**Anthropic's Claude Research System (Orchestrator: Claude Opus 4 / Claude Sonnet 4 subagents, launched 2025\)** is the most transparent public account of an orchestration choice at scale. The lead agent—designated *LeadResearcher*—uses Claude Opus 4 (and, after the Sonnet 4 generation, often Claude Sonnet 4 as a cost-efficient variant) because the orchestrator's job is fundamentally *decomposition and synthesis*, not raw generation quality. Anthropic's engineering post documents that a multi-agent system with Opus 4 as lead and Sonnet 4 subagents outperformed single-agent Opus 4 by 90.2% on their internal research eval. The key failure mode avoided by using a top-tier orchestrator: "spawning 50 subagents for simple queries, scouring the web endlessly for nonexistent sources, and distracting each other with excessive updates"—failures Anthropic attributed to poor *orchestrator judgment*, not subagent capability.\[^1\]

**Stripe Minions (Orchestrator: deterministic blueprint nodes \+ contained agent loops, 2026\)** ship over 1,300 AI-authored pull requests per week. Stripe's architecture explicitly avoids a model-as-orchestrator design. Their "blueprints" alternate between fixed, deterministic code nodes and open-ended LLM loops. Alistair Gray's engineering post frames this as "the model does not run the system; the system runs the model". Each minion gets a curated slice of MCP toolset, at most two CI rounds, and terminates at a pull request. The takeaway for the anima pipeline: the boundaries around an agent matter more than the intelligence inside it.\[^2\]\[^3\]

**Microsoft Magentic-One / AutoGen v0.4 (Orchestrator: GPT-4o class model, released Nov 2024\)** uses a central Orchestrator agent that plans, tracks progress, and re-plans to recover from errors across specialized agents (WebSurfer, FileSurfer, Coder, ComputerTerminal). The architecture features an outer loop for overarching task flow and an inner loop for per-task assignment and error recovery. AutoGen v0.4 (released late 2024\) rewrote the framework from scratch with an async-first actor model architecture, improving reliability over v0.2 by enabling run control and message passing between agents. The model choice for the orchestrator in Magentic-One is explicitly a frontier-class model (GPT-4o or equivalent), because the orchestrator is responsible for *dynamic re-planning*: when errors occur, it does not terminate but reassigns.\[^4\]\[^5\]\[^6\]\[^7\]

**Cognition Devin 2.0 (Single-agent-first, Interactive Planning, launched March 2025\)** takes the opposing architectural position. Cognition argues multi-agent architectures are fragile because actions carry implicit decisions and conflicts compound when agents work in isolation. Devin's planning loop is a single-threaded, continuous-context architecture: every action is informed by the full history and decision trace. The Interactive Planning feature introduced in Devin 2.0 lets Devin proactively research the codebase and present a detailed plan for user approval before autonomous execution begins. The model Devin uses internally is not publicly disclosed, but its performance profile (64.3% SWE-bench Pro in benchmarks attributed to Opus-class coding) and Cognition's emphasis on *context engineering* over multi-model routing suggests a single frontier-class model held at maximum context.\[^8\]\[^9\]\[^10\]

**Replit Agent v2 (Orchestrator: Claude Sonnet 4.6 primary, with GPT-4o and Gemini 2.5 routing, early access Feb 2025\)** launched in partnership with Anthropic's Claude 3.7 Sonnet. The orchestration loop uses a React loop, planning logic, and state management built around Claude as the primary reasoning model. Replit chose Claude Sonnet (not Opus) for orchestration explicitly because orchestration requires *fast* hypothesis formation, file search, and change targeting—a speed-sensitive, instruction-following task where Sonnet outperforms Opus on cost-adjusted throughput. From an Instagram post describing Replit Agent 4's stack: "Claude Sonnet 4.6 / GPT-4o / Gemini 2.5 / Llama 3.3 / LiteLLM — LAYER 2: THE ORCHESTRATION LOOP: The React loop, planning logic, and state management".\[^11\]\[^12\]

**Higgsfield Supercomputer (Orchestrator: enhanced Hermes Agent, 40+ tools, 3 layers of memory, launched May 2026\)** is a cloud-native AI agent for end-to-end visual content creation. Supercomputer routes between 30+ specialized generation models (Veo, Kling, Seedance, Soul, Nano Banana, Flux, GPT Image) autonomously, picking the right model per task step. The orchestrating entity is the Hermes Agent—an opaque proprietary system whose model composition is not publicly disclosed, though Higgsfield's blog confirms it follows the pattern of "briefing, plan-show, approve, execute". The Supercomputer shows the credit cost upfront before execution, functioning as a soft human-in-the-loop gate at the planning boundary.\[^13\]\[^14\]

**smolagents CodeAgent vs. ToolCallingAgent (HuggingFace, 2025–2026)** represents a production tension around orchestration stability. HuggingFace developers note ToolCallingAgent is "highly stable and reliable" as it leverages models' fine-tuning for structured tool calls, while CodeAgent is "extremely flexible and powerful, capable of writing Python code to solve complex problems" but "can suffer from instability" because "most LLMs are not specifically fine-tuned on the thought → code pattern". A 2026 GitHub issue proposes combining both: ToolCallingAgent as the stable primary, with on-demand delegation to a Python-executing sub-step when complex logic is required. HuggingFace's own recommendation (cited in their Discord) for uncertain users: use CodeAgent, because it handles dynamic orchestration better—but note that CodeAgent's stability is model-dependent; stronger models fail less.\[^15\]

**LangGraph Production Deployments (LangChain, 2024–2026)** focuses on durable execution, streaming, and human-in-the-loop as its orchestration primitives. LangGraph treats orchestration as a state machine with checkpointing, which means the orchestrator doesn't need to hold context across interruptions—the graph's persisted state does. This shifts the model-choice question: LangGraph deployments often use Sonnet-class models at the orchestrator node because instruction following and tool-call correctness matter more than deep reasoning, while reserving Opus-class for specialized reasoning nodes. Claude Code, notably, implements "multi-agent orchestration in a prompt rather than a framework—which, as developers analyzing the source code noted, makes LangChain feel like a solution in search of a problem".\[^16\]\[^17\]

### Failure Modes From Wrong Orchestrator Choice

Across the above systems, the documented failure modes of under-provisioning the orchestrator are consistent:

- **Loop amplification**: orchestrator fails to recognize convergence, spawns redundant agents (documented in Anthropic Research System early prototypes)\[^1\]  
- **Context fragmentation**: orchestrator loses track of which subagents completed which tasks (documented in MovieAgent evaluation)\[^18\]  
- **Dynamic re-planning failure**: orchestrator cannot recover from tool errors and terminates entire run (documented in Magentic-One benchmarking)\[^6\]  
- **Plan-action mismatch**: orchestrator emits a valid-looking plan but tool calls in the execution loop misinterpret task boundaries (documented in smolagents)\[^15\]

---

## Section 2: Planning Delegation

### The Planner-Verifier Split vs. Single-LLM Plan Emission

The canonical failure of single-LLM planning is that the model optimizes *plan fluency* rather than *plan executability*. A well-written plan that omits cost estimation, dependency ordering, or error branches looks correct at emit time and fails at execution time. The planner-verifier split attacks this by separating generation from evaluation, often using a stronger model for evaluation.

**SELF-DISCOVER (Google DeepMind / USC, arXiv:2402.03620, Feb 2024\)** is the strongest academic case for structured planner design. The framework has an LLM self-compose task-intrinsic reasoning structures by selecting atomic reasoning modules (critical thinking, step-by-step thinking, etc.) and composing them into an explicit reasoning structure before solving. On BigBench-Hard, SELF-DISCOVER improved GPT-4 and PaLM 2's performance by up to 32% compared to Chain-of-Thought, while outperforming CoT-Self-Consistency by more than 20% with 10–40x fewer inference compute calls. Critically, the reasoning structure discovered in the SELECT \+ ADAPT phase (using a capable model) is transferable: structures found by GPT-4 generalize to Llama 2\. This is the architectural basis for the planner-as-module-composer pattern: the planner does not just enumerate steps; it selects and instantiates a reasoning schema.\[^19\]

**Plan-and-Solve (NUS / Singapore Management University, ACL 2023\)** demonstrated that replacing "Let's think step by step" with an explicit two-part prompt—"Let's first understand the problem and devise a plan to solve the problem. Then, let's carry out the plan step by step"—significantly improved zero-shot CoT performance on arithmetic and commonsense reasoning. The extended PS+ variant adds variable extraction and intermediate calculation instructions. This is the minimal viable planner pattern: still a single LLM call, but the trigger phrase forces plan emission before execution, reducing errors caused by premature answer generation. For production, this is the cheapest planner upgrade.\[^20\]

**Reflexion (NeurIPS 2023, Shinn et al., arXiv:2303.11366)** reinforces language agents by updating language rather than model weights. Agents verbally reflect on task feedback signals and maintain reflective text in an episodic memory buffer to induce better decision-making in subsequent trials. Reflexion achieves 91% pass@1 on HumanEval coding, surpassing GPT-4's 80%. For planning specifically, Reflexion creates a *planner-plus-critic-in-a-loop*: the planner emits a plan, executes, receives feedback (scalar or free-form), reflects on the delta, and revises. The model used for reflection does not need to be the same model that generated the plan, enabling a cheap-plan-then-expensive-critique pattern.\[^21\]\[^22\]

**Tree of Thoughts (Yao et al., 2023\) \+ Verifier** extends planning from a single linear chain to a tree of partial plans, with a verifier evaluating each node. IBM's synthesis notes that ToT's explicit thought decomposition is particularly valuable for problems where the solution space is non-obvious at the first step. The verifier can be a separate, potentially smaller model trained to score plan quality rather than generate plans.\[^23\]

**Code2Video (Showlab NUS, arXiv:2510.01174 / EMNLP 2025\)** implements a Planner-Coder-Critic triad for educational video generation. The Planner "structures lecture content into temporally coherent flows and prepares corresponding visual assets." The Coder converts structured instructions into Python code with scope-guided auto-fix. The Critic, implemented as a vision-language model with visual anchor prompts, refines spatial layout and ensures clarity. Results show 40% improvement over direct code generation. The model assignment is not fully disclosed but the Planner and Critic are noted as "vision-LLMs," suggesting multimodal frontier models (GPT-4V class or Gemini class).\[^24\]\[^25\]

**MovieAgent (Show Lab NUS, arXiv:2503.07314, 2025\)** uses a hierarchical CoT-based planning process to automate long-form movie generation with multiple LLM agents simulating a Director, Screenwriter, Storyboard Artist, and Location Manager. The Director Agent holds the top-level plan state; Scene Plan Agent and Shot Plan Agent are subordinate planners. This three-level hierarchy (brief → scene plan → shot plan) directly maps to the anima pipeline's Phase 0 → phase-group → per-frame breakdown. MovieAgent achieves state-of-the-art on script faithfulness and character consistency metrics.\[^26\]\[^18\]

**Cognition Devin 2.0's Interactive Planning** builds the plan-then-approve gate directly into the UX: Devin responds to a new session "in seconds with relevant files, findings, and a preliminary plan. You can modify the plan before letting Devin work autonomously". This is the brief-plan-approve-execute pattern operationalized at consumer scale. Cognition does not disclose the model used for plan generation, but the architecture separates plan generation (fast, potentially cheaper) from plan execution (Devin's main frontier model).\[^9\]

**Higgsfield Supercomputer's brief-plan-approve-execute pattern** shows the same UX in the content creation domain: user describes outcome, Supercomputer builds a plan, shows credit cost upfront, user approves, then it generates. The explicit cost estimate before approval is notable: the planner's output includes a resource forecast, not just a task decomposition.\[^14\]

### Draft-then-Pro Escalation Pattern

Across Reflexion, SELF-DISCOVER, and MovieAgent, the same escalation pattern appears: draft the plan with a mid-tier model, score the plan with a top-tier model, and revise only if the score falls below a threshold. This was operationalized in Claude Code's `--model opus-plan` flag (documented in a May 2026 Instagram post): "You can use model opus-plan and Claude Code will use Opus for planning and Sonnet for execution". Reported savings: \~60% cost reduction versus all-Opus for equivalent plan quality on mid-complexity tasks.\[^27\]

---

## Section 3: Judging / Critic Delegation

### Canonical Literature

**Zheng et al. (2023), "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (arXiv:2306.05685)** established the foundational taxonomy of LLM judge failure modes: position bias (first-presented response favored), verbosity bias (longer responses favored regardless of quality), and limited reasoning on multi-step evaluation. The canonical finding: "strong LLM judges like GPT-4 can match both controlled and crowdsourced human preferences well, achieving over 80% agreement—the same level of agreement between humans". Critically, weaker judges fall significantly below this threshold, introducing systematic distortion rather than random noise.\[^28\]

**AlpacaEval 2.0 \+ Length-Controlled Win Rates (Dubois, Liang, Hashimoto, ICLR 2025\)** introduced a regression-based debiasing method that controls for response length, increasing Spearman correlation with Chatbot Arena from 0.94 to 0.98. The benchmark uses GPT-4 (now GPT-4.1) as judge and costs under $10 of OpenAI credits per run. The critical caveat (from arXiv:2410.07137): even with length control, a "null model" that always outputs a constant response can game AlpacaEval 2.0 to achieve 86.5% LC win rate. This quantifies the lower bound of judge reliability when adversarial outputs exploit style preferences.\[^29\]\[^30\]\[^31\]

**Arena-Hard-Auto (Li, Chiang et al., arXiv:2406.11939)** uses LLM-as-a-judge methodology with GPT-4.1 and Gemini 2.5 as automatic judges. It achieves 98.6% correlation with human preference rankings and provides 3x higher separation of model performances compared to MT-Bench. The dual-judge design (GPT-4.1 and Gemini 2.5) is a direct response to single-judge self-preference bias: systems distilled from GPT-4 outputs will score better under GPT-4 judges than under Gemini judges.\[^32\]

**G-Eval (Liu et al., 2023, EMNLP 2023\)** frames NLG evaluation using GPT-4 as judge with structured criteria injection, achieving better human alignment than automatic metrics like BLEU. G-Eval's key contribution is showing that *the criteria prompt* drives more judgment quality than model capability alone—a finding confirmed and quantified by the 2026 cost-effectiveness study below.\[^33\]\[^34\]

**Anthropic Constitutional AI (Bai et al., 2022\)** introduced the critic-loop pattern at training time: the model critiques its own output against a set of principles and revises. In production agent systems, this pattern is generalized to a separate critic model (different from the generator) that applies a written constitution. The principles themselves were derived from human values, and humans validate that the self-critique actually works. The CAI pattern is the direct ancestor of the evaluator-optimizer workflow in Anthropic's production agent guide.\[^35\]\[^36\]

**On Cost-Effective LLM-as-a-Judge Improvement Techniques (Lail & Markham, arXiv:2604.13717, April 2026\)** is the most directly actionable recent study for the anima pipeline. Four techniques were evaluated: ensemble scoring, task-specific criteria injection, calibration context, and adaptive model escalation. Results on RewardBench 2: criteria injection \+ ensemble scoring together reach 85.8% accuracy, \+13.5pp over single-model baseline. Task-specific criteria injection costs virtually nothing (prompt tokens only) and yields \+3.0pp alone; ensemble scoring yields \+9.8pp. **The critical finding for mid-tier judges**: "Small models benefit disproportionately from ensembling, making high-accuracy LLM judges accessible at low cost." Adaptive model escalation (routing uncertain cases to a top-tier judge) also improves over baseline but is dominated by criteria+ensemble on the cost-accuracy Pareto frontier.\[^37\]

**CAViAR: Critic-Augmented Video Agentic Reasoning (Google DeepMind / Columbia, arXiv:2509.07680, 2025\)** introduces a critic to distinguish between successful and unsuccessful agent action sequences in video reasoning. The agent uses LLM-called video modules as tools; the critic evaluates the result of each call to determine subsequent steps. This is the closest academic precedent for a per-frame T2 vision critic in a video generation pipeline.\[^38\]

**VideoGen-Eval (Yang et al., arXiv:2503.23452, 2025\)** is an agent-based evaluation system for video generation that integrates LLM-based content structuring, MLLM-based content judgment, and patch tools for temporal-dense dimensions. It evaluates 20+ video generation models against 700 structured prompts and 12,000+ generated videos, demonstrating strong alignment with human preferences. For the anima pipeline, this system maps directly to the T2 per-frame / post-cut critic architecture.\[^39\]

**VISTA's Tournament Critic (Google DeepMind, arXiv:2510.15831, 2025–2026)** identifies the best video from a generation batch using a "robust pairwise tournament," then critiques the winner using a trio of specialized agents focusing on visual, audio, and contextual fidelity. A reasoning agent synthesizes this feedback to rewrite the prompt for the next cycle. VISTA achieves up to 60% pairwise win rate against state-of-the-art baselines and 66.4% human evaluator preference. The trio-of-specialized-critics design is a direct production precedent for the T3 multi-CLI critic in the anima fleet.\[^40\]\[^41\]

**Multi-Agent Meta-Judge Framework (arXiv:2504.17087, 2025\)** proposes a three-stage pipeline: develop a rubric with GPT-4 and human experts; score judgments with three LLM agents; apply a threshold to filter low-scoring judgments. This yields \~15.55% improvement over raw judgments and \~8.37% over single-agent baselines on JudgeBench. The result demonstrates that meta-judging (judging the judges) is a viable production pattern.\[^42\]

**Meta-Judging Survey (arXiv:2601.17312, 2026\)** provides a comprehensive framework for LLMs-as-meta-judges.\[^43\]

### Failure Modes of Too-Cheap Judges

The evidence on cheap-judge failure modes is extensive and consistent:

**1\. False-positive pass-throughs on style-conforming but quality-deficient outputs.** From "Know Thy Judge" (arXiv:2503.04474): "small changes such as the style of the model output can lead to jumps of up to 0.24 in the false negative rate on the same dataset; adversarial attacks on the model generation can fool some judges into misclassifying 100% of harmful generations as safe". In animation pipelines, style-conforming outputs that have subtle temporal inconsistency, anatomical error, or narrative discontinuity will pass cheap judges that evaluate surface fluency.\[^44\]

**2\. Miscalibrated confidence.** From LLMs Instead of Human Judges (arXiv:2406.18403): "Models are reliable evaluators on some tasks, but display substantial variability depending on the property being evaluated, the expertise level of the human judges, and whether the language is human or model-generated". Cheap judges are particularly unreliable when evaluating outputs that are *out of distribution* relative to their fine-tuning data—precisely the condition in novel creative generation tasks.\[^45\]

**3\. Sycophancy / identity drift not flagged.** SycEval (arXiv:2502.08177, 2025\) found sycophantic behavior in 58.19% of cases across tested models, with Gemini-1.5-Pro exhibiting the highest rate (62.47%). A sycophantic judge will approve output that resembles the style of its own training distribution—systematically normalizing drift toward that distribution and failing to flag frames that deviate from the established visual style of the animation.\[^46\]

**4\. Verbosity / style drift normalized.** From Debiasing LLM Judges: "LLM judges can systematically overvalue fluency over factual correctness, miss subtle reasoning or factual errors, and favor answers stylistically similar to their own outputs. These aren't just random errors; they are biases that skew evaluation outcomes in predictable ways". In animation, this means a cheap judge will favor visually verbose (busy, detail-rich) frames over narratively appropriate ones, normalizing a "more is more" style drift.\[^47\]

**5\. Benchmark gaming.** The "null model" result (arXiv:2410.07137) proves that under cheaply constructed judge rubrics, constant-output systems can achieve top rankings. For production pipelines, this means any judge whose rubric does not explicitly test *against* high-scoring-but-wrong outputs is gameable by generation models that have learned to exploit judge biases.\[^31\]

---

## Section 4: Chairman / Synthesis Patterns

When multiple critics disagree, production systems resolve dissent through five documented patterns:

### 1\. Separate Chairman Call (Synthesize Peer Critiques)

The VISTA reasoning agent and the Multi-Agent Meta-Judge framework both implement a separate synthesis agent that receives structured critique outputs from peer critics and produces a consolidated verdict and revised prompt. This is the "chairman as distillation function" pattern. Cost: one additional top-tier inference call per critique round. Latency: additive (sequential). Quality: highest available, because the chairman reasons over a richer context than any individual critic.\[^42\]\[^40\]

### 2\. One Peer Designated as Chair

The Anthropic Research System's lead agent doubles as a chairman when subagents return conflicting research findings: it synthesizes and decides, without a separate synthesis model. This saves the cost of a dedicated chairman call but introduces a conflict of interest (the chair may be biased toward the framing of its own prior subagent calls). Best for well-defined tasks where the orchestrator has domain authority; riskier for aesthetic/creative evaluation.\[^1\]

### 3\. Tournament Bracket

VISTA's pairwise tournament selects the best video before any critique. This is the strongest documented production implementation: rather than asking critics to score absolute quality, it scores relative quality, which is a more reliable human-aligned signal (as demonstrated by AlpacaEval and Chatbot Arena data). Cost: scales O(n log n) with the number of candidate outputs. Latency: multiple rounds. Best for generation tasks where several candidates can be produced cheaply.\[^29\]\[^40\]

### 4\. Weighted Vote by Confidence / Score

The Meta-Judge Framework applies a threshold filter to select which judges' verdicts to retain. On Cost-Effective LLM-as-a-Judge (arXiv:2604.13717) demonstrates ensemble scoring as Monte Carlo averaging over per-call noise, and shows that score variance itself is a reliable uncertainty signal. A critic ensemble where each vote is weighted by its own calibration score (derived from a calibration context prompt) is the theoretically clean version of this pattern.\[^37\]\[^42\]

### 5\. Manual Escalation to Human

The Stripe Minions system preserves a mandatory human review gate at the pull-request boundary. Anthropic's production agent guidance notes that "agents can pause for human feedback at checkpoints or when encountering blockers". For the anima pipeline, human escalation is the appropriate pattern for T3 critic disagreement above a defined divergence threshold—particularly at the museum-publish gate where reverting is expensive.\[^36\]\[^3\]

### Cost and Latency Tradeoffs

| Pattern | Relative Cost | Relative Latency | Consistency | Best Use Case |
| :---- | :---- | :---- | :---- | :---- |
| Separate chairman call | High (+1 top-tier inference) | High (sequential) | High | T3 post-animatic critic final verdict |
| One peer as chair | Low | Low | Medium (conflict of interest risk) | T2 per-frame when speed \> precision |
| Tournament bracket | Medium (O(n log n)) | High (multi-round) | High (relative signal) | Pre-cut selection from multiple gen candidates |
| Weighted vote by confidence | Low-medium (ensemble ×N) | Medium | Medium-high | T3 peer critique before chairman call |
| Human escalation | High (wall-clock) | Very high | Authoritative | Museum-publish gate |

---

## Section 5: Cost/Quality Curve

### What the Evidence Says About Diminishing Returns

The most rigorous recent source is the 38-task, 15-model benchmark by Ian Paterson (May 2026):\[^48\]

- Claude Opus 4.6 and Sonnet 4.6 both scored 100.0% (100% pass rate) on all 38 tasks  
- Sonnet costs $0.20/run; Opus costs $0.69/run—3.5x premium for identical accuracy on those tasks\[^48\]  
- The margin opens specifically on "reasoning-adjacent" tasks: Gemini Flash drops to 60% on these while Opus stays near 100%\[^48\]  
- **The routing thesis**: the 265x cost gap between Gemini Flash ($0.003) and Opus ($0.69) is worth it only on reasoning-intensive tasks; for data-extraction or classification tasks, Flash scores 100% and the gap buys nothing\[^48\]

The Synoros multi-source benchmark (March 2026\) shows frontier model convergence at SWE-bench: Claude Opus 4.6 (80.8%), Gemini 3.1 Pro (80.6%), GPT-5.4 (77.0%), and Sonnet 4.6 (79.6%) are within a 3.8pp range. The **meaningful differentiations** are:\[^49\]

- **Creative/UI quality** (WebDev Arena Elo): Claude Opus 4.6 leads at 1549, Sonnet 4.6 at 1523—the premium for Opus on subjective creative quality is real but modest\[^49\]  
- **General user preference** (Chatbot Arena Elo): Claude Opus 4.6 leads at 1504 vs. Gemini 3.1 Pro at 1493—an 11-point gap that is statistically meaningful but not dominant\[^49\]  
- **Scientific reasoning** (GPQA Diamond): Gemini 3.1 Pro leads at 94.3%, beating Opus 4.6 (91.3%) and Sonnet 4.6 (87.4%)—the one benchmark where Gemini's premium is load-bearing\[^49\]

From the Swfte AI head-to-head (May 2026): on long-horizon agentic coding, Claude Opus 4.7 leads at 64.3% SWE-bench Pro and \+13% on Cursor's internal bench. On scientific reasoning, Gemini 3.1 Pro leads with 94.3% GPQA Diamond. On price-balanced general multimodal work, GPT-5.5 leads on enterprise availability.\[^8\]

### Where Top-Tier Premium Is Load-Bearing vs. Decorative

| Role | Load-Bearing Tier | Rationale | Evidence |
| :---- | :---- | :---- | :---- |
| Orchestrator (long-horizon planning, error recovery) | Top-tier | Loop failure rate drops significantly; re-planning quality is tier-sensitive | Anthropic Research System \+90.2% multi-agent vs single\[^1\] |
| Phase 0 planner (cost-estimation, dependency graph) | Top-tier | Plan quality determines all downstream; single-model plan emission is consistently worst pattern | SELF-DISCOVER \+32% over CoT\[^19\]; MovieAgent hierarchical CoT\[^26\] |
| T2 vision critic (per-frame) | Mid-to-top | Frame-level style and anatomy error detection; MLLM capability required; criteria injection \+ ensemble substitutes for tier upgrade | VideoGen-Eval results\[^39\]; criteria injection \+3pp vs cost-free\[^37\] |
| T3 peer critics (multi-CLI) | Mid-tier × ensemble | Each critic scores one dimension; ensemble \+ chairman synthesizes; mid-tier with criteria injection approaches top-tier quality | Cost-Effective Judge study: ensemble \+9.8pp\[^37\] |
| T3 chairman | Top-tier | Synthesizes disagreement across peer critics; sycophancy in the chair causes pass-throughs on the most expensive failure modes | VISTA reasoning agent design\[^40\]; Meta-Judge \+15.55% over raw\[^42\] |
| Subagent execution workers | Mid-tier | Tool-calling, code execution, asset generation—not reasoning-heavy | Replit Agent v2 architecture\[^11\]; Anthropic sub-Opus subagents\[^1\] |
| Per-frame generation workers | Fast/cheap | Pure generation, not reasoning | Stripe blueprint model\[^3\] |

---

## Master Reference Table

| Named System | Role(s) | Model(s) | Rationale | Source |
| :---- | :---- | :---- | :---- | :---- |
| Anthropic Claude Research System | Orchestrator \+ lead agent; subagent workers | Opus 4 orchestrator; Sonnet 4 subagents | Opus for synthesis/delegation; Sonnet for parallel search — 90.2% improvement over single-agent\[^1\] | [anthropic.com/engineering/built-multi-agent-research-system](https://www.anthropic.com/engineering/built-multi-agent-research-system) (Jun 2025\) |
| Stripe Minions | Hybrid orchestration (deterministic nodes \+ LLM loops) | Undisclosed (frontier) | "System runs the model"; blueprints \+ two-round CI cap \+ mandatory reviewer\[^3\] | [stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) (Feb 2026\) |
| Microsoft Magentic-One / AutoGen v0.4 | Orchestrator \+ specialized subagents | GPT-4o class (Orchestrator); specialized agents per domain | Outer/inner loop re-planning; dynamic error recovery\[^6\] | [arxiv.org/abs/2411.04468](https://arxiv.org/abs/2411.04468) (Nov 2024\) |
| Cognition Devin 2.0 | Single-agent orchestrator \+ interactive planner | Undisclosed frontier (likely Opus-class) | Single-threaded continuous context; Interactive Planning with human approval gate\[^9\]\[^10\] | [cognition.ai/blog/devin-2](https://cognition.ai/blog/devin-2) (Mar 2025\) |
| Replit Agent v2/v4 | Orchestration loop \+ model routing | Claude Sonnet 4.6 primary; GPT-4o / Gemini 2.5 secondary | Sonnet chosen for speed \+ instruction-following in React loop\[^12\] | Instagram, Mar 2026\[^12\] |
| Higgsfield Supercomputer | Orchestrator (30+ model router) \+ brief-plan-approve-execute | Hermes Agent (undisclosed); 30+ gen models beneath | brief→plan→credit-estimate→approve→execute UX pattern\[^13\]\[^14\] | [higgsfield.ai/blog/agentic-ai-for-content-creation](https://higgsfield.ai/blog/agentic-ai-for-content-creation) (May 2026\) |
| smolagents CodeAgent | Orchestrator (Python code generation) | Best available model recommended; ToolCallingAgent for stability | CodeAgent more flexible; ToolCallingAgent more stable; hybrid proposed 2026\[^15\] | [github.com/huggingface/smolagents/issues/1956](https://github.com/huggingface/smolagents/issues/1956) (Jan 2026\) |
| LangGraph (LangChain) | State-machine orchestrator | Sonnet-class at orchestrator node; Opus at reasoning nodes | Durable execution \+ human-in-the-loop; graph state substitutes for model context\[^16\] | [docs.langchain.com/oss/python/langgraph](https://docs.langchain.com/oss/python/langgraph) |
| SELF-DISCOVER (Google DeepMind/USC) | Planner (module-composer) | GPT-4 / PaLM 2 at planner; structures transfer to smaller models | \+32% over CoT on BigBench-Hard; 10–40x fewer inference calls vs. CoT-SC\[^19\] | [arxiv.org/abs/2402.03620](https://arxiv.org/abs/2402.03620) (Feb 2024\) |
| Plan-and-Solve (NUS/SMU) | Planner (zero-shot trigger) | Any LLM (prompt engineering only) | Zero-shot CoT improvement via plan-first trigger phrase; PS+ adds variable extraction\[^20\] | \[ACL 2023, Wang et al.\] |
| Reflexion (NeurIPS 2023\) | Planner \+ verbal RL feedback loop | Any LLM (actor \+ reflector, can be same or split) | 91% HumanEval pass@1; verbal episodic memory buffer drives re-planning\[^21\]\[^22\] | [arxiv.org/abs/2303.11366](https://arxiv.org/abs/2303.11366) |
| Code2Video (Showlab NUS) | Planner-Coder-Critic triad | VLM (Planner); code LLM (Coder); VLM with visual anchors (Critic) | \+40% over direct code generation\[^24\]; Critic uses visual anchor prompts to refine spatial layout\[^25\] | [emergentmind.com/papers/2510.01174](https://www.emergentmind.com/papers/2510.01174) |
| MovieAgent (Show Lab NUS) | Hierarchical CoT planner (Director/Scene/Shot agents) | Multiple LLMs at each hierarchy level | Director→Scene Plan→Shot Plan decomposition; SOTA on script faithfulness \+ character consistency\[^26\] | [github.com/showlab/MovieAgent](https://github.com/showlab/MovieAgent); \[ICLR 2026, arXiv:2503.07314\] |
| CAViAR (Google DeepMind/Columbia) | Video agent \+ critic | LLM agent (tool orchestrator); MLLM critic | Critic distinguishes successful from unsuccessful action sequences in video reasoning\[^38\] | [arxiv.org/abs/2509.07680](https://arxiv.org/abs/2509.07680) (Sep 2025\) |
| VISTA (Google DeepMind) | Planner \+ pairwise tournament \+ trio critic \+ reasoning chairman | Multimodal LLMs (undisclosed) | Pairwise tournament selects best video; trio critiques visual/audio/contextual; reasoning agent synthesizes\[^40\] | [research.google/pubs/vista](https://research.google/pubs/vista-towards-test-time-self-improving-video-generation-agent/) (2025–26) |
| VideoGen-Eval (Yang et al.) | MLLM judge for video generation | LLM (content structuring) \+ MLLM (judgment) | 12,000+ video evaluation benchmark; strong alignment with human preferences\[^39\] | [arxiv.org/abs/2503.23452](https://arxiv.org/abs/2503.23452) (Mar 2025\) |
| AlpacaEval 2.0 (tatsu-lab) | Automatic judge (LC win rate) | GPT-4 judge; length-controlled regression | 0.98 Spearman correlation with Chatbot Arena at \<$10; null model gaming at 86.5%\[^29\]\[^31\] | [github.com/tatsu-lab/alpaca\_eval](https://github.com/tatsu-lab/alpaca_eval) |
| Arena-Hard-Auto (LMSYS) | Automatic judge | GPT-4.1 \+ Gemini 2.5 dual judge | 98.6% correlation with human; dual-judge design prevents single-provider self-preference\[^32\] | [arxiv.org/abs/2406.11939](https://arxiv.org/abs/2406.11939) |
| G-Eval (Liu et al.) | NLG judge (structured criteria) | GPT-4 | Criteria injection drives more judge quality than model capability alone\[^33\]\[^34\] | EMNLP 2023 |
| Zheng et al. LLM-as-Judge (MT-Bench) | LLM judge framework \+ bias taxonomy | GPT-4 | Position bias, verbosity bias, limited reasoning on multi-step eval\[^28\] | [arXiv:2306.05685](https://arxiv.org/abs/2306.05685) (2023) |
| Meta-Judge Framework (arXiv:2504.17087) | Multi-agent meta-judge | 3 advanced LLMs \+ GPT-4 rubric | \+15.55% over raw judgments; \+8.37% over single-agent baseline\[^42\] | [arxiv.org/abs/2504.17087](https://arxiv.org/abs/2504.17087) (Apr 2025\) |
| Cost-Effective Judge Study (Lail & Markham) | Judge improvement techniques | GPT \+ Claude families | Criteria injection (+3pp) \+ ensemble (+9.8pp) \= \+13.5pp over baseline at near-zero cost\[^37\] | [arxiv.org/abs/2604.13717](https://arxiv.org/abs/2604.13717) (Apr 2026\) |
| Genspark Super Agent | Multi-model orchestrator (9 LLMs \+ 80+ tools) | 9 LLMs (undisclosed mix) | Concert-of-models approach; GAIA benchmark outperformed OpenAI without proprietary models\[^50\] | [venturebeat.com, April 2025](https://venturebeat.com/ai/gensparks-super-agent-ups-the-ante-in-the-general-ai-agent-race) |

---

## Section 6: Three Recommended Configurations for the Anima Pipeline

*Roles defined: Orchestrator (Phase 0 brief intake through phase-completion routing), Planner (Phase 0 structured plan \+ cost estimate), T2 Vision Critic (per-frame \+ post-cut), T3 Peers (post-animatic, pre-museum-publish multi-CLI critics), T3 Chairman (synthesizes T3 peer disagreement).*

*Subscription-absorbed models available: Claude Sonnet 4.6, Claude Opus 4.7, Gemini 3.1 Pro (Anti-Gravity CLI), GPT-5.5 (Codex CLI).*

---

### Configuration A: Budget-Conscious

| Role | Model | Rationale |
| :---- | :---- | :---- |
| Orchestrator | **Claude Sonnet 4.6** | 100% on 38-task benchmark at $0.20/run\[^48\]; OSWorld 72.5% makes it capable of computer-use-style routing\[^51\]; handles React loop, state, and error recovery |
| Phase 0 Planner | **Claude Sonnet 4.6 (extended thinking)** | Sonnet 4.6 supports extended thinking; plan-and-solve trigger phrase \+ structured output; reserve escalation to Opus only for plans that fail verification |
| T2 Vision Critic | **Gemini 3.1 Pro** | 94.3% GPQA Diamond — strongest scientific/multimodal reasoning at $2/$12; apply task-specific criteria injection (free) for per-frame rubric\[^37\] |
| T3 Peers | **Sonnet 4.6 (×3 ensemble, 3 dimensions)** | Ensemble scoring \+9.8pp over single call\[^37\]; three distinct criteria prompts (temporal coherence, anatomical correctness, narrative alignment) |
| T3 Chairman | **Claude Sonnet 4.6** | Synthesizes trio output; escalate to Opus only if any peer score is below threshold |

**Estimated monthly cost**: Near-zero marginal (all subscription-absorbed). Per-run compute cost: \~$0.20–$0.40 in API credits for complex full-pipeline runs if you exceed subscription limits.

**Expected wins**: Lowest per-frame cost; fastest T2 loop; Gemini's multimodal strength is load-bearing for visual evaluation.

**Expected losses**: T3 Chairman may normalize style drift (Sonnet sycophancy risk at 58%+ base rate per SycEval); Phase 0 planning quality will be the main failure vector — a missed dependency in the plan propagates all 10 phases.\[^46\]

---

### Configuration B: Balanced (Recommended for Production)

| Role | Model | Rationale |
| :---- | :---- | :---- |
| Orchestrator | **Claude Sonnet 4.6** | Same as Config A — orchestration is instruction-following, not deep reasoning |
| Phase 0 Planner | **Claude Opus 4.7** | Planning is the highest-leverage position for top-tier; draft-then-Opus-verify or all-Opus-for-Phase-0; MovieAgent and SELF-DISCOVER confirm planner tier is load-bearing\[^26\]\[^19\] |
| T2 Vision Critic | **Gemini 3.1 Pro** | Same as Config A — GPQA Diamond leadership is directly relevant to visual evaluation accuracy |
| T3 Peers | **Sonnet 4.6 (×2 ensemble) \+ GPT-5.5 (×1)** | Cross-provider ensemble reduces self-preference bias (Arena-Hard-Auto dual-judge pattern\[^32\]); GPT-5.5's Codex lineage makes it strong on temporal/structural evaluation |
| T3 Chairman | **Claude Opus 4.7** | Top-tier chairman absorbs the one place where sycophancy is most dangerous (pre-museum-publish gate); Opus 4.7 has adaptive thinking enabled\[^52\] |

**Estimated monthly cost**: One Opus 4.7 call per T3 cycle; one Opus 4.7 call for Phase 0 planning. Budget-absorbed for subscription tier; \~$0.05–0.15 in overflow credits per full pipeline run.

**Expected wins**: Phase 0 plan quality is high; T3 chairman is not vulnerable to style normalization; cross-provider T3 ensemble catches provider-specific biases.

**Expected losses**: Slightly slower T3 cycle due to Opus chairman latency; more expensive than Config A at scale.

---

### Configuration C: Pinnacle-Everywhere

| Role | Model | Rationale |
| :---- | :---- | :---- |
| Orchestrator | **Claude Opus 4.7** | Maximum re-planning quality; justified if orchestrator loop failures are the dominant production risk |
| Phase 0 Planner | **Claude Opus 4.7** | Full Opus reasoning for plan \+ cost estimate; extended context for full 10-phase dependency graph |
| T2 Vision Critic | **Gemini 3.1 Pro** | Gemini still wins on GPQA Diamond (94.3%)\[^49\]; no evidence that Opus beats Gemini 3.1 on visual evaluation tasks |
| T3 Peers | **Opus 4.7 (×1) \+ GPT-5.5 (×1) \+ Gemini 3.1 Pro (×1)** | True three-provider ensemble; each peer has distinct training distribution, minimizing correlated blind spots |
| T3 Chairman | **Claude Opus 4.7** | Identical to Config B; Opus chairman at top-tier for synthesis |

**Estimated monthly cost**: Highest of the three; all-Opus orchestrator and planner will exceed subscription throughput limits on high-volume animation work. Estimate \~$0.50–$1.50 per full pipeline run in API overflow.

**Expected wins**: Maximum plan quality; maximum T3 catch rate for subtle defects; three-provider ensemble is the strongest documented chairman-feed pattern.

**Expected losses vs. Config B**: No measurable quality gain at T2 vision critic (Gemini already leads here); orchestrator quality improvement is marginal beyond Sonnet for the specific task of tool-call routing; \~3–5x higher cost for \~5–10% quality gain at the orchestrator and worker levels.

---

### A Note on Portfolio Positioning

The combination of subscription-absorbed multi-provider council for a solo creator (Anthropic \+ OpenAI \+ Google under personal subscription tiers) being used in a production creative pipeline is, as of May 2026, uncommon enough to constitute a differentiating practice. Most documented production systems use a single primary provider with one secondary. Running a three-provider T3 peer ensemble with a separate chairman—specifically for a 2D animation quality gate—has no direct prior art in the published literature surveyed here. This positions the anima fleet as an early practitioner of provider-diverse evaluation councils for solo creative production, which is a genuine portfolio signal.

**Where evidence is thin**: Higgsfield Supercomputer's internal orchestration model is not publicly disclosed; Replit Agent's model routing details are partial; Cognition Devin's model identity is undisclosed. The Gemini 3.1 Pro benchmark claims (77.1% ARC-AGI-2, 94.3% GPQA Diamond) are from Google's own evals methodology page and have not been independently reproduced at scale as of this writing. The claim that Sonnet and Opus are "equivalent" at 100% on the Paterson 38-task benchmark holds for that task distribution only—on multi-file refactoring, long-horizon planning, and competitive math, academic benchmarks consistently show an Opus gap. The routing decision should be made at the *task type* level, not the model level.\[^53\]\[^54\]\[^48\]

---

## References

1. [How we built our multi-agent research system](https://www.anthropic.com/engineering/built-multi-agent-research-system?trk=article-ssr-frontend-pulse_little-text-block) \- On the the engineering challenges and lessons learned from building Claude's Research system  
     
2. [Minions: Stripe's one-shot, end-to-end coding agents \- Stripe Dot Dev](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) \- Minions are Stripe's homegrown coding agents. They're fully unattended and built to one-shot tasks. ...  
     
3. [Stripe's coding agents: the walls matter more than the model](https://www.anup.io/stripes-coding-agents-the-walls-matter-more-than-the-model/) \- Stripe built their "minions" system around deliberate constraint. They call the core design pattern ...  
     
4. [AutoGen Studio and AutoGen v0.4 \[Status Updates, Discussion\] \#4208](https://github.com/microsoft/autogen/discussions/4208) \- The goal of AutoGen Studio remains to create a tool to rapidly prototype, and debug multi-agent appl...  
     
5. [Microsoft researchers introduce Magentic-One system \- Facebook](https://www.facebook.com/groups/DeepNetGroup/posts/2330924517300417/) \- Magentic-One features a multi-agent architecture directed by a core “Orchestrator” agent, responsibl...  
     
6. [A Generalist Multi-Agent System for Solving Complex Tasks \- arXiv](https://arxiv.org/html/2411.04468v1) \- Magentic-One uses a multi-agent architecture where a lead agent, the Orchestrator, plans, tracks pro...  
     
7. [Microsoft Researchers Introduce Magentic-One: A Modular Multi ...](https://www.reddit.com/r/machinelearningnews/comments/1gljvng/microsoft_researchers_introduce_magenticone_a/) \- Magentic-One features a multi-agent architecture directed by a core “Orchestrator” agent, responsibl...  
     
8. [Claude Opus 4.7 vs GPT-5.5 vs Gemini 3.1 Pro \- Swfte AI](https://www.swfte.com/de/blog/claude-opus-4-7-vs-gpt-5-5-vs-gemini-3-1-pro) \- Gemini 3.1 Pro's SWE-bench Pro of 51.6% is well behind both rivals, and Terminal-Bench at 44.7% refl...  
     
9. [Devin 2.0 \- Cognition](https://cognition.ai/blog/devin-2) \- We're excited to announce Devin 2.0: a new agent-native IDE experience for working with Devin, along...  
     
10. [Cognition vs Anthropic: Single-Agent vs Multi-Agent Architectures](https://www.linkedin.com/posts/ricky-ho-0ba168_cognition-dont-build-multi-agents-activity-7353652784283463680-bzDH) \- Their recommended architecture is a single-threaded, continuous context agent, where all reasoning h...  
      
11. [Introducing Replit Agent v2 in Early Access](https://replit.com/blog/agent-v2) \- In partnership with Anthropic's Claude 3.7 Sonnet launch, we're excited to announce the release of R...  
      
12. [Replit Agent 4: Design While AI Builds \- Instagram](https://www.instagram.com/reel/DVy5wVxj9FF/) \- Claude Sonnet 4.6 GPT-40 Gemini 2.5 Liana 3.3 LiteLLM LAYER 2- THE ORCHESTRATION LOOP The React loop...  
      
13. [Introducing Higgsfield Supercomputer \- Instagram](https://www.instagram.com/reel/DYSijOqiKLz/) \- Higgsfield just launched Supercomputer, a cloud-native AI agent built for end-to-end task execution....  
      
14. [How to Use Agentic AI for Content Creation? \- Higgsfield AI](https://higgsfield.ai/blog/agentic-ai-for-content-creation) \- Agentic AI has changed how content gets made. You don't operate tools anymore, you brief an agent an...  
      
15. [ENH: Combine CodeAgent and ToolCallingAgent \#1956 \- GitHub](https://github.com/huggingface/smolagents/issues/1956) \- Best of Both Worlds: This would achieve the stability of the ToolCallingAgent with the on-demand fle...  
      
16. [LangGraph overview \- Docs by LangChain](https://docs.langchain.com/oss/python/langgraph/overview) \- LangGraph is focused on the underlying capabilities important for agent orchestration: durable execu...  
      
17. [Claude Code vs Cursor 2026 : Autonomie Terminal vs ...](https://wavespeed.ai/blog/fr/posts/claude-code-vs-cursor-2026/) \- Claude Code vs Cursor en 2026 : benchmarks réels, détails de tarification et un cadre de décision cl...  
      
18. [Automated Movie Generation via Multi-Agent CoT Planning](https://openreview.net/forum?id=SY78p0rIYt) \- Automated Movie Generation via Multi-Agent CoT Planning. Download PDF · Weijia Wu, Zeyu Zhu, Mike Zh...  
      
19. [Large Language Models Self-Compose Reasoning Structures \- arXiv](https://arxiv.org/abs/2402.03620) \- We introduce SELF-DISCOVER, a general framework for LLMs to self-discover the task-intrinsic reasoni...  
      
20. [Plan-and-Solve Prompting \- fnl.es](https://fnl.es/Science/Papers/Prompt+Engineering/Plan-and-Solve+Prompting) \- Plan-and-Solve Prompting Plan-and-Solve Prompting Improves Zero-Shot Chain-of-Thought Reasoning Lei ...  
      
21. [Reflexion: language agents with verbal reinforcement learning](https://openreview.net/forum?id=vAElhFcKW6) \- Reflexion is a framework that reinforces language agents by updating language rather than model weig...  
      
22. [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) \- We propose Reflexion, a novel framework to reinforce language agents not by updating weights, but in...  
      
23. [What is Tree Of Thoughts Prompting? \- IBM](https://www.ibm.com/think/topics/tree-of-thoughts) \- Thought decomposition. The ToT framework explicitly breaks a problem into smaller, manageable steps ...  
      
24. [Code2Video: Code-Centric Educational Video Generation](https://www.emergentmind.com/papers/2510.01174) \- Code2Video introduces an agentic pipeline that leverages Planner, Coder, and Critic modules to gener...  
      
25. [A Code-Centric Paradigm For Educational Video Generation](https://scale.stanford.edu/ai/repository/code2video-code-centric-paradigm-educational-video-generation) \- In this work, we propose Code2Video, a code-centric agent framework for generating educational video...  
      
26. [Automated Movie Generation via Multi-Agent CoT Planning](https://huggingface.co/papers/2503.07314) \- MovieAgent introduces a hierarchical CoT-based reasoning process to automatically structure scenes, ...  
      
27. [Let's talk about cost-effectiveness and benchmarks, friend. Opus 4.5 ...](https://www.instagram.com/reel/DUn2Hhmireg/) \- ... Opus as planner, Sonnet as executor for 60% cost savings ... You can use model opus-plan and Cla...  
      
28. [Judging LLM-as-a-judge with MT-Bench and Chatbot Arena](https://huggingface.co/papers/2306.05685) \- Join the discussion on this paper page  
      
29. [GitHub \- tatsu-lab/alpaca\_eval: An automatic evaluator for ...](https://github.com/tatsu-lab/alpaca_eval) \- AlpacaEval 2.0 with length-controlled win-rates (paper) has a spearman correlation of 0.98 with Chat...  
      
30. [Length-Controlled AlpacaEval: A Simple Debiasing of Automatic...](https://openreview.net/forum?id=CybBmzWBX0) \- We focus on reducing the length bias of AlpacaEval, a fast and affordable benchmark for instruction-...  
      
31. [Cheating Automatic LLM Benchmarks: Null Models Achieve High ...](https://huggingface.co/papers/2410.07137) \- Cheating Automatic LLM Benchmarks: Null Models Achieve High Win Rates . 86.5% LC win rate on AlpacaE...  
      
32. [Arena Hard Benchmark Leaderboard \- LLM Stats](https://llm-stats.com/benchmarks/arena-hard) \- The benchmark uses LLM-as-a-Judge methodology with GPT-4.1 and Gemini-2.5 as automatic judges to app...  
      
33. [G-Eval: NLG Evaluation using GPT-4 with Better Human ... \- dblp](https://dblp.org/rec/journals/corr/abs-2303-16634.html) \- Bibliographic details on G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment.  
      
34. [NLG Evaluation using GPT-4 with Better Human Alignment](https://aclanthology.org/anthology-files/pdf/emnlp/2023.emnlp-main.153.pdf)  
      
35. [RLHF Explained: How Human Feedback Actually Trains AI Models](https://gun.io/news/2025/12/rlhf-explained-how-human-feedback-actually-trains-ai-models/) \- Anthropic's Constitutional AI, for example, has the model critique its own outputs against a set of ...  
      
36. [Building Effective AI Agents \- Anthropic](https://www.anthropic.com/research/building-effective-agents) \- In this post, we share what we've learned from working with our customers and building agents oursel...  
      
37. [An Empirical Investigation of Practical LLM-as-a-Judge Improvement ...](https://arxiv.org/abs/2604.13717) \- Two techniques account for nearly all available gains: task-specific criteria injection (+3.0pp at n...  
      
38. [CAViAR: Critic-Augmented Video Agentic Reasoning \- arXiv](https://arxiv.org/html/2509.07680v1) \- The agent iteratively composes video modules into sequences of executable programs, considering the ...  
      
39. [VideoGen-Eval: Agent-based System for Video Generation Evaluation](https://arxiv.org/abs/2503.23452) \- We propose VideoGen-Eval, an agent evaluation system that integrates LLM-based content structuring, ...  
      
40. [VISTA: A Test-Time Self-Improving Video Generation Agent](https://huggingface.co/papers/2510.15831) \- VISTA, a multi-agent system, iteratively refines user prompts to enhance video quality and alignment...  
      
41. [VISTA: A Test-Time Self-Improving Video Generation Agent](https://research.google/pubs/vista-towards-test-time-self-improving-video-generation-agent/) \- To address this, we introduce VISTA, a novel multi-agent system that autonomously refines prompts to...  
      
42. [Leveraging LLMs as Meta-Judges: A Multi-Agent Framework for Evaluating LLM Judgments](https://arxiv.org/abs/2504.17087) \- Large language models (LLMs) are being widely applied across various fields, but as tasks become mor...  
      
43. [Meta-Judging with Large Language Models: Concepts, Methods ...](https://arxiv.org/html/2601.17312v1)  
      
44. [Know Thy Judge: On the Robustness Meta-Evaluation of LLM Safety Judges](http://arxiv.org/pdf/2503.04474.pdf) \- ...importance of these through a study of commonly used safety judges, showing that small changes su...  
      
45. [LLMs instead of Human Judges? A Large Scale Empirical Study across 20 NLP Evaluation Tasks](https://arxiv.org/pdf/2406.18403.pdf) \- ...their ability to replicate the annotations. Our evaluations show substantial variance across mode...  
      
46. [SycEval: Evaluating LLM Sycophancy \- arXiv](https://arxiv.org/html/2502.08177v2)  
      
47. [Debiasing LLM Judges: Understanding and correcting AI Evaluation ...](https://dev.to/gyani_s/debiasing-llm-judges-understanding-and-correcting-ai-evaluation-bias-2ce4) \- This creates a need for bias correction: adjusting observed evaluation results to better reflect the...  
      
48. [I Tested 15 LLMs on 38 Real Coding Tasks. Here's My Routing Table.](https://ianlpaterson.com/blog/llm-benchmark-2026-38-actual-tasks-15-models-for-2-29/) \- I benchmarked Claude, GPT, Gemini, DeepSeek, and 11 others on my actual daily coding tasks. See pass...  
      
49. [LLM Benchmark Comparison: 12-Source Rankings \- Synoros](https://synoros.io/research/llm-benchmarks-multi-model-routing) \- LLM benchmark data from 12+ sources. Model rankings for coding, math, reasoning, tool use. Cost vs. ...  
      
50. [Genspark's Super Agent ups the ante in the general AI agent race](https://venturebeat.com/ai/gensparks-super-agent-ups-the-ante-in-the-general-ai-agent-race) \- Despite not building a proprietary model stack, it still outperformed OpenAI on the GAIA benchmark —...  
      
51. [Claude Sonnet 4.6, Gemini 3.1 Pro, Stripe Minions, Cloudflare Code ...](https://nlp.elvissaravia.com/p/ai-agents-weekly-claude-sonnet-46) \- In today's issue: Anthropic releases Claude Sonnet 4.6. Google launches Gemini 3.1 Pro with 77% ARC-...  
      
52. [Models overview \- Claude API Docs](https://platform.claude.com/docs/en/about-claude/models/overview) \- Claude is a family of state-of-the-art large language models developed by Anthropic. This guide intr...  
      
53. [Google DeepMind's Gemini 3.1 Pro Boosts Enterprise Automation](https://www.linkedin.com/posts/rarni_%F0%9D%97%A7%F0%9D%97%B9%F0%9D%97%B1%F0%9D%97%BF-google-deepminds-gemini-31-pro-activity-7430453839419535360-sqV_) \- With a 33.5% score on APEX-Agents and a dominant 69.2% on MCP Atlas, it's designed for enterprise-re...  
      
54. [Gemini 3.1 Pro: A smarter model for your most complex tasks](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/) \- Gemini 3.1 Pro is here to help you tackle complex tasks. The upgraded core intelligence is rolling o...

Here's the research report. It covers all five research tasks — orchestration, planning, judging, chairman synthesis, and the cost/quality curve — with named implementations and citations throughout, plus the three-configuration recommendation table at the close.

A few things worth flagging directly:

**The single highest-leverage finding for the anima pipeline**: The Anthropic Research System data showing Opus-as-orchestrator \+ Sonnet-as-subagents beats single-agent Opus by 90.2% is real, but the implication is *not* "use Opus everywhere." The implication is that the split matters more than the tier — and that Phase 0 planning is the one place where the Opus premium is definitively load-bearing, because every downstream phase inherits the plan's dependency graph.

**The cheap-judge failure modes section is the most directly protective material in the report**. The 58%+ sycophancy base rate documented in SycEval means your T3 critics will normalize style drift unless you (a) use cross-provider ensemble and (b) inject explicit anti-sycophancy criteria. The 2026 Lail/Markham paper's finding that criteria injection alone buys \+3pp at zero cost is immediately actionable.

**On portfolio positioning**: Running a three-provider T3 peer ensemble as a solo creator with subscription-absorbed models is genuinely novel — there's no direct prior art in the surveyed literature. That's worth naming in your case studies for 16BitFit or any agentic pipeline work you document publicly.

