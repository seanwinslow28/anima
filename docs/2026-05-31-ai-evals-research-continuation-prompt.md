# Continuation prompt — research: AI evals in 2026, and how to evaluate the anima agent fleet

*Paste everything below the divider into a **fresh Cowork session** opened at `/Users/seanwinslow/Code-Brain/anima`. This session does **research, then synthesis** — it does NOT write pipeline code. Its product is a single durable findings doc, and then a surgical fold of those findings back into the critic-spine kickoff. The research is the load-bearing part; treat it as a real investigation, not a listicle. Use AskUserQuestion if scope or depth is genuinely Sean's call.*

---

You are continuing the **anima pipeline-completion program**. Context, in one breath: anima is a human-and-agent 2D animation pipeline; its infrastructure has outrun its art (Act 2 has never rendered), so the current priority is **finishing the pipeline and making every agent 100% solid before running Act 2 through it end-to-end as the capstone**. The first chosen workstream is **hardening the critic spine** — building Em (the T2 vision critic) a real eval suite, giving her a way to see motion, and running the #1 T2 bake-off. That kickoff is written: [`docs/2026-05-31-critic-spine-hardening-kickoff.md`](2026-05-31-critic-spine-hardening-kickoff.md).

**Before that kickoff executes, Sean wants the eval foundations researched properly.** The kickoff currently assumes eval competence — what a good case is, what metrics matter, how to calibrate an LLM judge — that should be grounded in current best practice, not improvised. *"Empirical, not vibes"* is one of anima's six load-bearing beliefs ([`PHILOSOPHY.md`](../PHILOSOPHY.md)); this session makes the eval methodology itself empirical before the fleet is judged by it.

**Read these first, to ground the research in anima's actual shape:**

1. [`PHILOSOPHY.md`](../PHILOSOPHY.md) — esp. "empirical, not vibes" and "the critic earns its keep when it proposes fixes." Evals serve these.
2. [`docs/2026-05-31-critic-spine-hardening-kickoff.md`](2026-05-31-critic-spine-hardening-kickoff.md) — the workstream the findings fold into; carries the full completion-program map in its header (the three buckets, the per-agent roster).
3. [`docs/2026-05-26-agent-fleet-brainstorm-v2.md`](2026-05-26-agent-fleet-brainstorm-v2.md) §2.5 (the named cheap-judge failure modes — sycophancy 58%, self-preference +90%, position/length bias — and the documented defenses) + §8 (the bake-off sequence + its metric list). The research must deepen and pressure-test these, not just restate them.
4. [`docs/2026-05-24-pipeline-v2-change-map.md`](2026-05-24-pipeline-v2-change-map.md) §7 — the evals workstream: the `code-brain/evals/vault-synthesizer/` pattern anima already committed to (ships intentionally red, cases grounded in real production logs, "no agent ships without a baseline trace," the Hamel Husain / Shreya Shankar / Anthropic "Demystifying Agent Evals" canon already cited). The research extends this lineage; honor it.
5. The fleet you're designing evals *for* (from the brainstorm §3 roster): **Maya** (planner, Opus), **Cy** (character designer — Opus authors + Gemini verifies + NB2 generates), **Em** (T2 vision critic, Gemini/Opus), **Mo** (museum writer, Sonnet), **Flo** (Phase 5 model router), **Sam** (scriptwriter, Opus), **Bea** (storyboard, Sonnet), the **T3 council** (Codie/Annie/Sage + Opus chairman), and the **Sonnet orchestrator**. These are *different evaluation problems* — a planner, a vision critic, a prose writer, a router, and a multi-CLI council do not get judged the same way. The research's payoff is a per-agent-type eval strategy, not one generic rubric.

---

## The research mandate

Investigate the state of AI/agent evaluation as of 2026, then translate it into anima's context. Organize the investigation around these questions — go deep, cite sources, and prefer primary/practitioner material (Hamel Husain, Shreya Shankar, Anthropic, OpenAI, the Inspect/Braintrust/LangSmith/promptfoo ecosystems, recent arXiv on LLM-as-judge calibration) over blog-spam:

**A. First principles — what makes an eval good vs bad.**
- Error analysis / open coding / "look at your data" as the starting point; why eval suites grounded in real failure traces beat synthetic ones.
- Binary, specific, assertable cases vs vague Likert scores; the right granularity.
- The thermometer trap: never tune cases until the agent passes; what "ships intentionally red" actually buys.
- Sample size, class balance, leakage, inter-rater reliability; how many cases is "enough" at solo-creator scale.
- Outcome vs process (trajectory) evals; when each is appropriate.

**B. LLM-as-judge — the load-bearing problem for anima's critics (Em, the T3 council).**
- How to calibrate a judge against human labels; agreement metrics (Cohen's κ, etc.); the "who evals the judge" meta-eval.
- The documented biases (sycophancy, self-preference, position, length, verbosity, self-consistency) and the *concrete, current* defenses — cross-provider ensembles, criteria injection, pairwise/tournament scoring, rubric decomposition, reference-guided judging. Quantify the deltas where the literature does.
- For a **vision** judge specifically (Em on frames + motion): multimodal eval methods, identity-consistency metrics (CLIP/DINOv2 — anima already uses these in Cy's similarity gate), and how to score "motion arc / drift / texture-crawl" — failure modes a still-image judge can't see.
- For a **multi-agent council** (T3): measuring agreement/dissent richness, ensemble value-add over a single judge, chairman synthesis quality.

**C. Metrics & tracking — what to log and watch over time.**
- The metric set per agent *type*: e.g. for a critic, precision/recall on defect detection and **false-pass rate as the dangerous one**; for a generator, faithfulness/hallucination + aesthetic-hold; for a planner, plan-validity + cost-estimate accuracy; for a router (Flo), routing-correctness + cost realized vs predicted.
- Regression suites in CI vs dated bake-offs vs drift monitoring across model-version churn (the "artifacts are durable; model choices are not" belief — how do you notice when a model upgrade silently regresses a critic?).
- Baseline traces, the dated-bake-off-as-portfolio-artifact pattern, and what a healthy eval dashboard surfaces for a solo creator (not an enterprise).

**D. Tooling — borrow vs build.**
- The 2026 landscape (Inspect, Braintrust, LangSmith, promptfoo, OpenAI Evals, DeepEval, etc.): what each is good at.
- anima locked **hand-rolled** for the pipeline/DAG (change-map §6) and uses a hand-rolled pytest-style eval harness (`code-brain/evals/`). The research should advise *what patterns to borrow* (scoring idioms, judge templates, dataset formats) without taking on a framework — and flag anything genuinely worth a dependency.

**E. anima-specific synthesis — the actual deliverable's spine.**
- A per-agent-type eval strategy table for the full fleet (Maya / Cy / Em / Mo / Flo / Sam / Bea / T3 / orchestrator): the failure modes that matter for each, the case-design approach, the metrics, and where an LLM judge is appropriate vs where deterministic/metric checks suffice.
- What anima should track run-over-run to know the fleet is — and stays — "100% solid."

---

## Research tooling, routing, and spend discipline

Use the heaviest appropriate tool per question; don't grind a local model on a compound topic.

- **The `deep-research` skill** (this Cowork session) for the fan-out web research + adversarial verification + cited synthesis. This is the primary engine for the mandate above.
- **OpenRouter research models via Claude Code** — Sean noted the OpenRouter key is available; a parallel Claude Code session can route the deepest sub-questions (LLM-as-judge calibration literature, multimodal eval methods) to a research-grade model. If you go this route, hand off a tight sub-question list, not the whole mandate.
- **Gemini Deep Research** via code-brain (`agents-sdk/scripts/gemini_dr.py` / the `gemini-deep-research` skill) is available for a compounding multi-target sweep — but mind the caps (code-brain: $7/task, $20/day, tracked in `vault/health/`). Route a single heavy compound topic there if web search isn't enough; keep single-shape questions on the cheaper path.
- **Verify before trusting.** The deep-research discipline (adversarial claim-checking, primary sources) is non-negotiable for the LLM-as-judge numbers especially — the brainstorm already cites specific figures (58% sycophancy, +90% self-preference); confirm or update them with current sources rather than copying forward.

Whatever the routing, the *synthesis* lands in this Cowork session as one doc.

---

## The output — the findings doc

Write **one** durable research doc: `docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md` (adjust date if the session runs later). Studio-manual voice — prose where prose works, tables only for genuine reference data (the per-agent eval-strategy matrix is the one table that earns its place). It should read like a studio's eval handbook, not a survey paper. Suggested spine:

1. **Executive summary** — the 5–7 load-bearing takeaways, anima-framed.
2. **Eval first principles** (mandate A) — good vs bad, grounded in citations.
3. **LLM-as-judge calibration** (mandate B) — the deepest section; this is where Em and the T3 council live or die. Include the bias deltas and the concrete defenses, and a recommended judge-calibration procedure anima can actually run (judge vs human-label agreement on a labeled set).
4. **Metrics & tracking** (mandate C) — the per-type metric set, regression vs bake-off vs drift, what to log.
5. **Tooling: borrow vs build** (mandate D) — honoring the hand-rolled lock.
6. **The anima fleet eval strategy** (mandate E) — the per-agent-type matrix + the run-over-run health signals. This section is what the rest of the program builds on.
7. **Sources** — primary/practitioner, with what each supports.

Capture genuine uncertainty honestly (where the field disagrees, say so) — that's more useful than false confidence, and it matches the "empirical, not vibes" contract.

🚦 **STOP — present the findings doc to Sean** before folding anything into the kickoff. The research is its own deliverable and Sean will want to read it on its own terms first.

---

## The fold-back — integrating findings into the critic-spine kickoff

Only after Sean has the findings doc: **surgically update** [`docs/2026-05-31-critic-spine-hardening-kickoff.md`](2026-05-31-critic-spine-hardening-kickoff.md) so the critic-spine work executes against researched method, not improvisation. Likely touch points (let the research determine the specifics):

- **Phase 0 (Em's eval suite)** — sharpen with the researched case-design discipline: how many cases, class balance, how to label, inter-rater reliability if Sean isn't the only labeler, and the precise metric set (false-pass rate front and center for a critic).
- **Phase 1 (motion-sight)** — fold in the multimodal/motion eval methods and identity/drift metrics the research surfaces.
- **Phase 2 (the T2 bake-off)** — replace the provisional metric list with the researched judge-calibration + bias-defense procedure; add a judge-vs-human-label calibration step if the research says the bake-off needs one to be trustworthy.
- Add a one-line pointer from the kickoff to the findings doc as its methodological basis.

Keep the kickoff's shape and discipline intact — this is a sharpening pass, not a rewrite. Add a CHANGELOG entry covering both the new findings doc and the kickoff fold-back, and (if the findings change how anima should track agents generally) note whether the fleet-wide eval strategy warrants its own source-of-truth doc or a `CLAUDE.md` pointer — surface that to Sean rather than deciding it silently.

## Working discipline

- **Research first, synthesize, STOP, then fold.** Don't touch the kickoff until the findings doc exists and Sean has seen it.
- **No pipeline code this session.** This is research + docs. The eval *suite* gets built in the critic-spine execution session that follows, against the method this one establishes.
- **Cite primary sources; verify the load-bearing numbers.** Especially the LLM-as-judge bias figures and any "best practice" claim the fleet will be held to.
- **Honor the locks:** hand-rolled harness (change-map §6), the `code-brain/evals/` lineage, ships-intentionally-red, "no agent ships without a baseline."
- **Studio voice, clean markdown.** The doc is a portfolio artifact in its own right — the eval handbook for a human-and-agent studio.

## Out of scope (do NOT start here)

- Building Em's eval suite / the bake-off harness — that's the critic-spine execution session, after this research lands.
- The other completion-program workstreams (Phase 6 integration, Flo, T3 council, Act 2 re-expression).
- Re-running the bake-off sequence or touching any agent code.

**The throughline:** anima is about to judge its whole fleet by its evals. This session makes sure the ruler is calibrated before anyone measures with it — so "100% solid" means something specific, current, and defensible, not just "the tests are green."
