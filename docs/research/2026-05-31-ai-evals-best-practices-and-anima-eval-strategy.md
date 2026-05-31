# AI Evals — Best Practice (2026) and the anima Fleet Eval Strategy

**Date:** 2026-05-31
**Status:** Research findings. Methodological basis for the critic-spine hardening kickoff ([`2026-05-31-critic-spine-hardening-kickoff.md`](../2026-05-31-critic-spine-hardening-kickoff.md)) and for every agent eval suite that follows it.
**Grounded in:** [`PHILOSOPHY.md`](../../PHILOSOPHY.md) ("empirical, not vibes"; "the critic earns its keep when it proposes fixes") · [`2026-05-26-agent-fleet-brainstorm-v2.md`](../2026-05-26-agent-fleet-brainstorm-v2.md) §2.5, §8 · [`2026-05-24-pipeline-v2-change-map.md`](../2026-05-24-pipeline-v2-change-map.md) §7 · the `code-brain/evals/vault-synthesizer/` lineage.
**Scope note:** This is a research doc, not a build plan. It establishes the *method* anima judges its fleet by. No pipeline code is touched here; the eval suites get built against this method in the sessions that follow. Where the field genuinely disagrees, this doc says so rather than papering over it — that is the "empirical, not vibes" contract applied to the ruler itself.

---

## 1. Executive summary — the load-bearing takeaways

Anima is about to judge its whole fleet by its evals. Before anyone measures with the ruler, here is what current best practice says the ruler must be made of — seven things, anima-framed.

**1. Error analysis on real traces is the whole game; everything else is downstream.** The single highest-ROI activity in any eval program is a human reading actual outputs and writing open-ended notes on what went wrong — *before* writing a single metric. Hamel Husain calls skipping it the #1 mistake teams make. anima's existing instinct — cases "grounded in real anima output, labeled by the actual defect" — is exactly right and is the canon. Synthetic fixtures are a cold-start crutch, never the goal.

**2. Binary, specific, assertable cases beat Likert scores — and anima already does this.** Every serious practitioner (Hamel, Eugene Yan, Shankar's SPADE/EvalGen line) converges on pass/fail with a written critique over 1–5 scales. The nuance lives in the critique text, not in a number nobody can calibrate. anima's `verdict: pass | borderline | fail` + `reasoning` paragraph is the right shape; the one refinement is to treat `borderline` carefully, since three-way verdicts reintroduce the boundary ambiguity binary was meant to kill.

**3. "Ships intentionally red" is not a quirk — it is the textbook capability-eval pattern.** Anthropic's "Demystifying Agent Evals" explicitly distinguishes *capability evals* (should start at a low pass rate — "a clear hill to climb") from *regression evals* (should sit near 100%). anima's vault-synthesizer suite shipping 1/10 and climbing to 7/10 is this pattern done correctly. The discipline is: a red case is a finding, never a bug to paper over, and you do **not** tune cases until the agent passes — that is measuring the thermometer against itself.

**4. For Em and the T3 council, the dangerous error is the false pass, not the false fail — and the metric must reflect that.** A critic that lets a drifted frame through (false negative) costs far more than one that re-flags a good frame (the retry ladder absorbs a false alarm cheaply). Report **precision and recall on the defect class separately**, never raw agreement or F1 — both hide the false-pass rate under class imbalance. Tune the gate for high recall on defects.

**5. Three of the project's load-bearing judge-bias numbers needed correction.** The sycophancy figure holds; the self-preference "+90%" and the ensemble "+9.8pp" were misattributed or misquoted, and the "criteria injection +3pp" has no clean source. §3.3 carries the corrected ledger. This is precisely the kind of verification "empirical, not vibes" exists to force — the brainstorm's numbers were directionally right and specifically wrong, and a fleet held to them should be held to the corrected ones.

**6. A frame-grid contact sheet lets Em see *identity and content* across a clip — but it does not let her see *motion*.** The decisive finding for Phase 1 of the critic-spine work: multimodal LLMs frequently answer video questions correctly even when the frames are *shuffled*. A contact-sheet judge that appears to assess motion is very likely reading static content and ignoring time. So the contact sheet is the right cheap path for identity-drift and style-drift across a clip — but motion-arc, jitter, flicker, and texture-crawl need either dedicated low-level metrics (warping error, VBench motion-smoothness) or an honest "Em can't see this; a human takes the look" seam. Building the contact sheet and *claiming* motion coverage would be the trap.

**7. Stay hand-rolled. Borrow three idioms; consider exactly one dependency.** The hand-rolled-harness lock (change-map §6) is correct for solo scale and is itself portfolio gold. Borrow Inspect's scorer-returns-{score, rationale} contract and its reducer-for-stacking-critics pattern, borrow `stderr()`-on-every-metric so run-over-run deltas are distinguishable from noise, and keep the YAML case-file format anima already uses. The only dependency genuinely worth considering is **DeepEval**, and only because it extends pytest rather than replacing it — and only if anima ever wants pre-built faithfulness/hallucination scorers instead of hand-writing them.

---

## 2. Eval first principles — what makes an eval good vs bad

### Look at your data first

The foundational move, repeated across every primary source, is *error analysis*: a human reads real traces and writes open-ended notes on the first thing that went wrong in each, then groups those notes into a failure taxonomy and counts which modes dominate. Hamel Husain calls this "the single most valuable activity in AI development and consistently the highest-ROI activity," and names skipping it — going "tools first," building architecture and dashboards before looking at outputs — as the most common failure pattern. The canonical case study: an AI assistant that failed date handling 66% of the time, invisible until someone annotated the transcripts; fixing that one mode took success from 33% to 95%, and three failure categories accounted for over 60% of all problems.

The workflow is borrowed wholesale from qualitative research: **open coding** (annotate each trace with free-text notes, "akin to journaling," tagging the *first* failure since upstream errors cascade), then **axial coding** (group the notes into a taxonomy and count — "this is the most important step"). Bottom-up beats top-down: starting from generic metrics like "hallucination" or "toxicity" misses the domain-specific failures that actually matter; letting the categories emerge from real data finds them.

This is *why* anima's eval cases are "grounded in real anima output, labeled by the actual defect" rather than imagined. It is also why the vault-synthesizer suite's failure taxonomy (six named modes, open-coded from 17 days of real logs) is the right artifact, not an afterthought. The implication for the critic-spine work: Em's eval cases should come from open-coding the real Act 1 / Act 2 / Cy-run frames — read them, note what's actually wrong, let the failure taxonomy emerge — not from a list of failure modes written in advance.

### Real traces beat synthetic; synthetic is a cold-start crutch

Anthropic's guidance is to source eval tasks from what you already test manually, your bug tracker, your support queue — "converting user-reported failures into test cases ensures your suite reflects actual usage." Synthetic data is legitimate *only* as a bootstrap when you have no production data yet, and even then it must be grounded in real system constraints (real IDs, real schedules, real business rules) and should generate *inputs* not *outputs* (so the data doesn't inherit the model's own biases). No source claims synthetic beats real once real exists. anima's `deliberately-broken-phase-5-frame.png` fixture is the correct use of synthetic — a deliberately constructed negative case — but the bulk of Em's cases should be real frames.

### Binary and assertable, not Likert

The consensus against 1–5 Likert scales is near-universal. The argument: on a 5-point scale, annotators can't reliably distinguish a 3 from a 4, "introducing inconsistency and subjectivity," and teams inevitably end up asking "where's the line for good enough?" — forcing a binary decision anyway. A 10% increase in passing outputs is immediately meaningful; a 0.5-point shift on a 5-point scale requires interpretation. The recommended shape is **binary pass/fail paired with a written critique** — the nuance moves into the prose, which also forces domain experts to externalize implicit knowledge ("doesn't sound right" → a specific citation-format rule). Including those critiques as few-shot examples in a judge prompt has been reported to lift human-judge agreement 15–20 points.

Eugene Yan adds the one defensible non-binary carve-out: for inherently *subjective comparative* qualities (tone, conciseness, persuasiveness), **pairwise win/lose/tie** is more stable than absolute scoring — with an explicit *tie* option, because forcing a winner between near-identical outputs injects noise. Both Hamel and Yan reject Likert as the default; they differ only on whether subjective dimensions get binary-plus-critique (Hamel) or pairwise (Yan).

For anima this validates Em's verdict vocabulary, with one caution: `borderline` is a third bucket, and three-way verdicts smuggle back the boundary ambiguity that binary was meant to eliminate. Em's contract already handles this well by *forcing a citation* on `borderline` (and `fail`) — the `cites_criteria` invariant is what keeps `borderline` honest. The eval suite should score `borderline` against expected-verdict carefully, and probably treat "should this have been a fail?" as its own labeled question.

### The thermometer trap, and what shipping red buys

Goodhart's law — when a measure becomes a target it stops being a good measure — is the reason you never tune cases until the agent passes. The legitimate reason to edit a case is that the *case or grader is broken or unfair* (a validity fix); editing it so the agent passes is gaming. Anthropic makes the distinction operational: a 0% or 100% pass rate is usually a signal about the *eval*, not the agent — they don't trust an eval score "until someone digs into the details and reads some transcripts." (Their worked example: Opus 4.5 scored 42% on a benchmark until a researcher found the grader was penalizing "96.12" vs "96.124991"; fixing the grader raised it to 95% — a validity fix, not a Goodhart edit.)

What a suite that "ships intentionally red" buys is a *clear hill to climb*: capability evals "should start at a low pass rate," and the climb from red to green is the documentation of what a fix actually accomplished. anima's 1/10 → 7/10 vault-synthesizer arc is exactly this. The discipline the critic-spine kickoff already states — "a red case is the artifact, not a bug to paper over" — is the textbook position, not an anima eccentricity.

One subtlety worth holding: criteria *legitimately* evolve. Shankar et al.'s "Who Validates the Validators" documents that "it is impossible to completely determine evaluation criteria prior to human judging of LLM outputs" — grading outputs is *how* you discover your criteria. So a case set is a living document, and refining a criterion because grading taught you what you actually meant is legitimate; refining it so the agent passes is not. The line between the two is the whole game, and it is a judgment call every time.

### How many cases is enough

Two different numbers for two different artifacts, often confused:

- **Error-analysis trace review:** aim for *at least 100 traces*, and stop at "theoretical saturation" — when ~20 new traces stop revealing new failure modes (Hamel).
- **The eval task suite itself:** *20–50 tasks drawn from real failures is a great start* (Anthropic). The rationale is statistical: early on, each fix has a large, obvious effect, so small samples suffice to detect it; only a mature agent chasing small improvements needs hundreds of cases.

This is the directly-relevant guidance for solo scale, and it means Em's first suite does not need to be large — a few dozen well-chosen, real, labeled cases is a legitimate v1. What matters more than count is **class balance**: test both the cases where a defect should be flagged *and* the cases where a clean frame should pass. "One-sided evals create one-sided optimization" — a critic suite that's all defects will reward a critic that flags everything. The brainstorm's "200-frame defect set" framing should be read as an aspiration, not a v1 gate; 30–60 balanced, real, labeled cases is the honest starting line, with the set growing as the fleet matures.

Two more hygiene rules: **isolate trials** (clean state per run — Anthropic observed a model gaining an unfair advantage by reading git history from prior trials, the canonical leakage example), and at solo scale prefer a **single "benevolent dictator" annotator** (Sean). Hamel: "if you feel like you need five subject matter experts to judge a single interaction, your product scope might be too broad." Inter-rater reliability metrics (Cohen's κ) only matter once there's more than one labeler — which for anima is a "later, if ever" concern, noted in §3.2 for completeness.

### Outcome vs trajectory

Grade *what the agent produced*, not *the path it took*, by default. Checking that an agent followed a specific sequence of steps "results in overly brittle tests, as agents regularly find valid approaches that eval designers didn't anticipate." But once outcome tests exist, it's useful to *also* grade the trajectory for different reasons — efficiency, tool-use quality, interaction quality — and to build in **partial credit** for multi-step tasks (an agent that gets 3 of 4 steps is meaningfully better than one that fails immediately). For anima: a critic's *verdict* is the outcome to grade (did Em catch the defect?); but Em's *reasoning* and *cites_criteria* are trajectory signals worth grading too (did she catch it for the *right* reason, citing the right rule?). A critic that's right by accident is a latent regression.

---

## 3. LLM-as-judge calibration — where Em and the T3 council live or die

This is the deepest section because it is the load-bearing one. Em is an LLM judge. The T3 council is four LLM judges. Everything anima trusts downstream of a critic gate inherits whatever the judge's calibration is — and an uncalibrated judge that *looks* confident is worse than no judge, because it launders a guess into a verdict.

### 3.1 How to calibrate a judge against human labels

The canonical loop (Hamel's "Critique Shadowing," distilled from 30+ implementations) is: find *the* one principal domain expert (Sean), build a diverse dataset, have the expert make **binary pass/fail** calls plus a free-text critique, fix obvious system bugs you find along the way, then build the judge prompt *seeded with the expert's critiques as few-shot examples* and iterate the prompt while tracking agreement until it converges. The expert's critiques — not the final judge — are the real artifact; Hamel describes the judge as "a nice hack I use to trick people into carefully looking at their data."

Convergence can be fast on a well-scoped task: Hamel's Honeycomb judge reached **>90% agreement with the domain expert in three prompt iterations**. But that was a *balanced* dataset (~50% failures), which is what made raw agreement a usable metric — see the imbalance caveat below. Shankar's EvalGen formalizes the mixed-initiative version: generate candidate evaluators, have the human grade a subset, select the implementations that best align with the human grades (it hit 0.73 defect recall vs SPADE's 0.49 on a product task).

The procedure anima can actually run for Em: take the Phase 0 labeled case set (Sean's verdicts are the ground truth), run Em across it, and measure her agreement with Sean's labels — not as a smoke test but as a scored confusion matrix. That *is* the baseline trace. If Em and Sean disagree on a case, that disagreement is either a judge-calibration problem (tighten Em's prompt) or a criteria-drift discovery (Sean's rubric sharpened) — and distinguishing the two is the work.

### 3.2 Agreement metrics and what counts as "good"

The headline result the whole field rests on: **GPT-4-as-judge reaches >80% agreement with humans on MT-Bench — the same level humans agree with each other** (Zheng et al. 2023, the foundational "LLM-as-a-Judge" paper). That is the encouraging number. The sobering qualifications:

- **Raw agreement misleads under class imbalance.** Hamel's own warning, attached to his >90% Honeycomb result: "using raw agreement is generally not recommended and can be misleading when classes are imbalanced... measure precision and recall separately." His result was only trustworthy because his data was balanced. Em's defect data will *not* be balanced (most frames are fine), so **Em's baseline must report precision/recall on the defect class, not raw agreement.**
- **Chance-corrected agreement is much lower than raw agreement on the same labels.** Cohen's κ (which corrects for chance) typically lands in the 0.3–0.5 "fair-to-moderate" range on summarization-quality tasks where rank correlations on the *identical* labels run 0.8–0.9. κ is deliberately conservative. The standard threshold rubric (Landis & Koch): 0.21–0.40 *fair*, 0.41–0.60 *moderate*, 0.61–0.80 *substantial*, 0.81–1.0 *near-perfect*. A reasonable bar for a binary judge is **κ ≥ 0.6 (substantial)**; ≥ 0.8 is near-perfect and rare against subjective labels.
- **The ceiling is human-human agreement, and matching it beats exceeding it.** Averaged-human vs single-human correlation runs ~0.8–0.9; LLM-judge vs human runs ~0.3–0.6. You cannot expect a judge to beat the human ceiling, and you shouldn't want to. NVIDIA's 2025 "Judge's Verdict" benchmark reframes the target as matching human *variance*: a judge within |z| < 1 of human-human agreement is "human-like" and ideal; a "super-consistent" judge that *exceeds* human agreement (z > 1) is a different, often *worse* thing — too rigid, not better. This is a genuine and useful reframe: for Em on subjective aesthetic calls, the goal is to reproduce Sean's judgment *including its variance*, not to be mechanically more consistent than Sean.

For anima: report Em's baseline as a confusion matrix (precision/recall/false-pass rate on the defect class) plus, if Sean ever co-labels with a second annotator, Cohen's κ. Raw agreement can be the headline only if a case set is deliberately balanced — and even then, carry precision/recall alongside it.

### 3.3 The documented biases — verified ledger

The brainstorm §2.5 cites specific figures. Verifying them against primary sources was a core mandate of this research. The result: **one holds, three need correction.** This ledger is the corrected version the fleet should be held to.

| Claim (as cited) | Verdict | What the source actually says |
|---|---|---|
| Sycophancy **58.19%** base rate — SycEval, arXiv 2502.08177 | **CONFIRMED** (with context) | 58.19% of cases showed sycophantic behavior across ChatGPT-4o / Claude-Sonnet / Gemini-1.5-Pro on math (AMPS) + medical (MedQuad) *when the user pushes back with a rebuttal*. Split: **progressive 43.52%** (flips toward the correct answer), **regressive 14.66%** (flips toward wrong). Persistence once triggered: 78.5%. Cite it as "sycophancy under rebuttal," not an unprompted base rate. |
| Self-preference **up to +90%** — "Chen et al. 2024, arXiv 2410.02736" | **CORRECTED — drop the +90%** | 2410.02736 is *"Justice or Prejudice? / CALM"* (Ye et al., ICLR 2025), not "Chen et al." The "+90%" is **not in it** — the only "90%" is a *bandwagon-bias prompt-template example* ("90% believe R1 is better"). The canonical self-preference paper is **Panickssery, Bowman & Feng, arXiv 2404.13076**, which documents the *mechanism* (self-recognition ability linearly correlates with self-preference strength), **not a +90% magnitude**. Use 2404.13076 for the mechanism; CALM for cross-model quantification (reported as an error/robustness rate, not "+90%"). |
| Criteria injection **+3pp** agreement | **UNSUPPORTED** | No primary source found for this exact figure. Rubric specificity clearly helps, but the clean general-vs-specific "+3pp" is uncited. The *strong* rubric result to cite instead: **Databricks "Grading Notes"** — adding brief per-task rubric notes cut judge-human misalignment **67.5% for GPT-4o (→93.1% aligned) and 85% for Llama3 (→96.3%)**. PoLL's prompt ablation moves κ by only ±0.01–0.07 from prompt structure. Soften "criteria injection +3pp" to "decomposed/specific rubrics improve agreement; the largest documented gain is Databricks Grading Notes." |
| Ensemble scoring **+9.8pp** | **CORRECTED — restate in κ** | The direction is solid (panels beat single judges) but the metric is wrong. The canonical source, **PoLL (Verga et al., arXiv 2404.18796)**, reports **Cohen's κ +0.136 (0.627 → 0.763 on KILT-NQ)** vs a single GPT-4 judge — and is **7× cheaper** with lower intra-model bias. Not "+9.8pp." Restate as the κ delta. |
| Position bias | **CONFIRMED** | FairEval (Wang et al., arXiv 2305.17926): simply swapping response order let a weaker model (Vicuna-13B) beat a stronger one (ChatGPT) on **66 of 80 queries** with ChatGPT as judge. Position bias is real, non-random, and worse when candidates are close in quality (arXiv 2406.07791). |
| Length / verbosity bias | **CONFIRMED** | Judges systematically prefer longer outputs regardless of added value (Saito et al., arXiv 2310.10076). Mitigated by length-controlled scoring (AlpacaEval 2.0 LC). |

The lesson is not that the brainstorm was careless — its numbers were directionally correct and the defenses it named are real. The lesson is that "empirical, not vibes" cuts both ways: the project's own cited figures get verified too, and three of five needed a fix. The corrected ledger above is what the critic-spine kickoff should reference.

### 3.4 The concrete defenses (and how much they buy)

The defenses anima's brainstorm names are real and well-supported; here they are with verified effect sizes where the literature provides them:

- **Cross-provider ensemble / panel of judges (PoLL).** The strongest single defense. A panel of smaller models from *different* families beats one large judge (+0.136 κ on KILT-NQ), at 7× lower cost, with less intra-family bias. This is exactly the T3 council's design (Codie/gpt-5.5 + Annie/Gemini + Sage/Opus, three vendors) — the architecture is validated by construction. The cross-provider point also defends the Em/orchestrator pairing (Gemini critic + Sonnet orchestrator) against correlated blind spots.
- **Separate generator from evaluator.** Self-preference scales with self-recognition (2404.13076), so a model judging its own family's output is the channel to close. anima's "Sonnet orchestrator + Gemini T2 critic" and the three-vendor T3 both close it by design.
- **Position-swapping + aggregate (Balanced Position Calibration).** Run each pairwise comparison twice with order flipped; only trust a verdict that survives the swap. Directly relevant *if* anima ever runs Em or the council in pairwise mode (A-vs-B frame comparison) — and §4 argues it should, because MLLM judges are far more reliable pairwise than absolute.
- **Decomposed / specific rubrics (criteria injection).** Em's `cites_criteria` invariant is this defense — forcing the judge to ground every blocking verdict in a specific `AC*`/`IR*`/`SF*` criterion ID is rubric injection made structural. The Databricks Grading Notes result (misalignment cut 67–85%) is the evidence this is high-ROI.
- **Reference-guided judging.** Anchor the judge to a gold reference. For Em this is the Bible anchor and the prior approved frame; the contract already leans on "vs the A-2 anchor, vs F18."
- **Don't trust the judge's self-reported confidence.** Verbalized LLM confidence is badly overconfident — ECE > 0.377 across GPT-3/3.5/Vicuna, and even GPT-4 only reaches ~63% AUROC distinguishing its own correct from incorrect answers (barely above chance). This matters for Em: her `confidence` field drives escalation to Opus (`escalation_threshold: 0.7`), and a self-reported confidence is a weak signal. The better uncertainty signal is **sampling consistency** — run the judge a few times and measure agreement/entropy; disagreement across samples tracks correctness far better than a single verbalized number. A cheap upgrade for Em's escalation logic worth flagging (not building) here: escalate on *sample disagreement*, not just on a low self-reported confidence.

### 3.5 The vision-judge problem — what a still-image judge cannot see

Em is a *vision* judge, and the still-vs-motion distinction is the most important technical finding in this research.

**Identity consistency (stills, and across a clip).** The right primary metric is **DINOv2 cosine similarity**, not CLIP. DreamBooth introduced the DINO score precisely because DINO/DINOv2 is self-supervised to distinguish *individual* instances, so it penalizes fine identity drift; CLIP-I encodes class-level semantics and "cannot distinguish certain identity-specific details" — two different people can score high CLIP-I but low DINO. anima's similarity_gate ladder (DINOv2 → CLIP → PIL) is ordered correctly. Three cautions the literature adds, all of which anima has independently hit:

- **DINO over-rewards copying.** A frame that photocopies the anchor scores highest. So DINOv2 is a good *drift detector* but a bad standalone *"good frame"* gate — pair it with a beat-fidelity axis so you don't reward a frame that just clones the anchor.
- **No universal threshold; use per-view anchors.** "Good" DINO values are only meaningful relative to a baseline on the same setup. The known fix for anima's exact observed problem (legitimate pose/expression variation overlapping drift against a single front anchor) is **per-view reference anchors**, not a tuned single-anchor threshold. This confirms the similarity-gate's "record-only, not hard-reject" decision was correct, and names the real fix.
- **Count breaches per-plate, don't average.** The 2026 "Subject Collapse Rate" pattern: report the *proportion of plates whose similarity falls below threshold*, not a mean — a mean hides one catastrophic drift among many fine plates.

**Motion — the trap.** The decisive finding: **multimodal LLMs frequently answer video questions correctly even when the frames are shuffled** (arXiv 2505.14321). They read static content and ignore temporal order. A frame-grid contact-sheet judge that *appears* to assess motion is very likely not seeing time at all. Corroborating: models without explicit temporal tokens significantly *overestimate* the quality of stuttery video. So:

- A contact sheet is the **right cheap path for identity-drift and style-drift across a clip** (does Sean stay Sean frame-to-frame; does the line weight hold) — these are content questions the "Image Grid Can Be Worth a Video" work shows VLMs handle zero-shot.
- A contact sheet is the **wrong tool for motion-arc, jitter, flicker, and texture-crawl**. Those need either dedicated low-level metrics or a human. The honest options: **warping error / E_warp** (optical-flow frame-to-frame residual — cheap, targets flicker/boiling directly), **VBench's motion-smoothness + temporal-flickering + dynamic-degree as a set** (and you *must* include a dynamism axis or you reward frozen clips — VBench documents the consistency↔dynamic-degree trade-off where a near-static video trivially maximizes "consistency"), and **FVMD** for motion-arc consistency. **Avoid FVD** as a temporal-artifact detector — it's biased toward per-frame image quality and is nearly blind to temporal corruption (severe frame-shuffling can paradoxically *improve* FVD).

There's a pencil-test-specific wrinkle the metrics literature flags directly: flicker-minimizing temporal metrics will *fight* the intentional line "boil" that is part of the hand-drawn aesthetic. Distinguishing stylistic boil (wanted) from artifact boil (unwanted) is genuinely hard for automated metrics — a strong candidate for a human look or a carefully-prompted T3, not a deterministic gate.

**MLLM-as-judge reliability for images.** Where MLLM judges are trustworthy: **pairwise A-vs-B comparison** (GPT-4V is human-like on pair comparison but diverges significantly on absolute scoring and batch ranking — MLLM-as-a-Judge benchmark, arXiv 2402.04788). Where they're weak: **low-level visual quality** (Q-Bench finds MLLMs only "preliminary and imprecise" on distortion/blur/artifact assessment — which is why anima's T1 deterministic rule gates and DINOv2 stay essential). And the same benchmark documents MLLM judges carry **egocentric, position, length bias + hallucination** — defended by swapping option order, not self-judging, and constraining to visible evidence (which Em's stage-don't-decide pattern and Mo's never-invent contract already do).

The synthesis for Em: ask her for **pairwise verdicts where possible** ("is plate A or B closer to the anchor/beat?"), feed her **real sampled frames** (not a text description — VideoJudge shows real frames beat even long chain-of-thought reasoning over a text summary, and a small specialist judge with frames beats a big general model without them), use **DINOv2 + T1 rules** for the things she's weak at (identity drift, low-level artifacts), and **do not let her claim motion coverage from a contact sheet** without a dedicated motion metric or a human seam behind it.

### 3.6 The multi-agent council (T3)

For the T3 council the eval questions are different: not "is one judge calibrated" but "does the *panel* add value over a single judge, and is the chairman's synthesis good?" The PoLL result (panel beats single judge by +0.136 κ, 7× cheaper, lower intra-model bias) is the value-add evidence, and it depends on the peers being from *different* vendors — which the Codie/Annie/Sage design satisfies. Two council-specific things to measure: **dissent richness** (does the panel surface genuinely orthogonal critiques, or do the three voices collapse into agreement — agreement is cheap, the value is in the disagreement) and **chairman synthesis quality** (does the Opus chairman faithfully represent both consensus *and* dissent without self-favoring — the reason the chairman is a distinct call, not a promoted peer, since promoted-peer chairmen self-favor when synthesizing critiques that include their own). These are bake-off questions, sequenced as priority #2 (the Sage tier ablation) in the brainstorm §8.

---

## 4. Metrics & tracking — what to log and watch over time

### The metric set is different per agent type

The single most important framing in this research: **a planner, a critic, a generator, and a router are different evaluation problems and do not get the same metric.** The per-agent matrix in §6 makes this concrete; the principles:

- **Critic / judge (Em, T3):** precision and recall on the defect class, reported separately — never raw agreement (misleads under imbalance) and never F1 alone (F1 ignores true negatives and so hides the false-pass blind spot exactly where it matters). The costly error is the **false pass** (a defect let through); tune for high recall on defects and let the retry ladder absorb false fails. Advanced but worth knowing: once you know a judge's true-positive and true-negative rates on a calibration set, you can *bias-correct* its reported defect rate algebraically — the judge's error is a measurement bias you back out, not noise (arXiv 2511.21140; balanced-accuracy argument in 2512.08121).
- **Generator (Cy, Flo's output, Sam, Bea):** faithfulness/groundedness + hallucination rate, *and* style/consistency adherence as a separate axis ("is it the right thing" vs "is it in the right register" — anima's HF05-wrong-aesthetic vs SF01-style-drift split). For the *visual* generator, DINOv2-vs-anchor *is* the visual groundedness metric.
- **Planner (Maya):** plan validity as two separable checks — *schema-valid + executable* (the `acceptance_criteria.json` graph loads and the phases run) and *the right steps were chosen* — plus **cost-estimate accuracy**. The natural estimate metric is MAPE (mean absolute % error), with two caveats that bite anima's `CostEstimatorNode` directly: MAPE breaks on zero actuals (a cached/skipped phase that costs $0) and penalizes over- and under-estimation asymmetrically. Track MAPE on non-zero phases *plus* a "% of runs within budget" companion to catch the systematic-underestimate bias a cost gate actually cares about.
- **Router (Flo):** routing as m-way classification — routing accuracy/correctness — jointly with **cost realized-vs-predicted**, on a quality-retained-vs-cost-saved curve (RouterEval frames it this way; tier routers report 40–70% cost savings at <2% quality loss). For anima's draft→pro escalation specifically: did draft-tier acceptance correctly predict that no pro escalation was needed (precision/recall on the escalate decision), and did realized spend track the estimate (which ties back to Maya's cost-estimate accuracy).

### Regression suites vs dated bake-offs vs drift monitoring

Three distinct instruments for three distinct jobs:

- **Regression suite (CI, every change):** the green suite that must stay green — "does it still handle what it used to." Anima's `pytest tests/ -q` credential-free harness is this. Every production failure you fix becomes a permanent "golden" case (fix → freeze).
- **Dated bake-off (occasional, costed):** the model head-to-head, run deliberately and dated, landing under `evals/bakeoffs/`. This is both an empirical model-selection tool *and* a portfolio artifact — the dated record of *why* a given model is in production. The T2 shoot-out is exactly this.
- **Drift monitoring (the silent-regression catcher):** the instrument anima most lacks today. **Model churn is the exposure.** Providers update model weights on a schedule; an improvement for the average user can be a regression for *your* specific prompts, with zero change on your side. The defense is two-part: **pin to dated snapshots** (`gpt-4o-2024-08-06`, not floating `gpt-4o` — "a prompt version is meaningless without the model it was tested against"), and **re-run the bake-off against a new snapshot before migrating to it.** This is anima's single biggest silent-regression exposure: Em shells out to Codex CLI (gpt-5.5) and Anti-Gravity CLI (Gemini 3.1 Pro), neither version-pinned, so a provider update could silently shift critic verdicts with no signal. The dated baseline trace is the snapshot that would catch it — which is another reason the baseline-trace discipline ("no agent ships without a baseline") is load-bearing, not ceremonial.

### What a solo creator should actually track

Start in a spreadsheet, not a platform. For a one-person project the worth-tracking-run-over-run set is small: per-metric scores on the golden set, the **judge's TPR/TNR over time** (the drift signal), and **realized-vs-estimated cost**. The enterprise observability stack — human-annotation queues, 1M-span tracing, stakeholder dashboards — is division-of-labor for *teams* and is over-engineering for solo. The named anti-pattern (Eugene Yan, "An LLM-as-Judge Won't Save the Product — Fixing Your Process Will"): treating the dashboard as the deliverable. Evals are a *practice* — the scientific method applied to a prompt — not a static artifact. For anima, the `last-run.md` + dated baseline traces + the bake-off reports already *are* the right lightweight dashboard; the museum walkthrough is the human-readable surface over them.

---

## 5. Tooling — borrow vs build

The change-map §6 hand-rolled lock is correct for solo scale, and the reasoning there ("stack traces beat framework magic… hand-rolled code is portfolio gold, 'I configured Prefect' is not") applies equally to evals. The advice from this research: **borrow idioms, take on essentially no framework, and consider exactly one dependency.**

**Borrow these three idioms (no dependency):**

1. **Inspect's (UK AISI) `Scorer → {score, rationale}` contract and its reducer pattern.** Inspect's pipeline is `dataset → Task → Solver → Scorer`, where each scorer emits a score *plus* a rationale and `accuracy()`/`stderr()` metrics, and multiple scorers aggregate via a **reducer**. anima's T1+T2+T3 stacking *is* a reducer over multiple scorers — the abstraction is worth copying even though the framework isn't. Its `model_graded_qa` scorer is the canonical judge-prompt template to read and adapt for Em.
2. **`stderr()` on every metric.** So a run-over-run delta is distinguishable from noise — you know whether Em's pass-rate moving from 0.71 to 0.78 is signal or sampling jitter. Cheap to compute, and it's the difference between "the bake-off found something" and "the bake-off found nothing and we shipped a coin flip."
3. **The declarative YAML case file.** anima already has this (`cases.yaml`) — keep it. Cases as *data*, not code, is the borrowable idiom from promptfoo and OpenAI Evals' `modelgraded/*.yaml` templates; copy the format, skip the engine.

**The one dependency worth considering: DeepEval.** It is the only framework that *extends* pytest rather than replacing it — its metrics are typed objects you `assert` inside test functions, so it drops into anima's existing pytest harness without changing the runner. The reason to consider it is narrow: if anima ever wants pre-built faithfulness/hallucination/G-Eval scorers (relevant to Mo and to any text-generation gate) rather than hand-writing them. The OSS core is free; the SaaS is optional. Until that need is concrete, hand-rolled remains correct. (An even thinner option if all you want is result aggregation: `pytest-evals`, a pytest plugin that collects and aggregates eval results without imposing metrics.)

**Skip the SaaS platforms.** Braintrust, LangSmith, and W&B Weave are SaaS-first team tools (live-traffic scoring, annotation queues, stakeholder dashboards) — over-engineered for solo, and a dependency on someone else's cloud for a project whose whole thesis is showing readable work. Arize Phoenix and Langfuse are self-hostable OSS if anima ever wants a local trace UI, but neither is needed for CI gating. The vendor-authored "you need two tools (CI harness + SaaS platform)" advice is exactly that — vendor-aligned; the solo reality is one OSS pytest harness plus a golden set until team-scale annotation is genuinely needed.

---

## 6. The anima fleet eval strategy

This is the section the rest of the program builds on. The fleet is not one evaluation problem; it is nine. The matrix below is the per-agent-type strategy: the failure modes that matter, the case-design approach, the metrics, and — the load-bearing column — **where an LLM judge is appropriate vs where a deterministic or metric check suffices or is required.**

The governing principle from §4: match the instrument to the agent. A judge gets precision/recall on defects; a generator gets faithfulness + style-hold; a planner gets validity + estimate-accuracy; a router gets routing-correctness + cost-realized. And from §3.5: for anything visual, deterministic metrics (DINOv2, T1 rules, warping error) carry the load an MLLM judge can't, and the MLLM judge is trustworthy mainly *pairwise*.

| Agent | Type | Failure modes that matter | Case-design approach | Core metrics | LLM judge vs deterministic |
|---|---|---|---|---|---|
| **Maya** (planner, Opus) | Planner | Invalid/unloadable `acceptance_criteria.json`; un-executable plan; **systematic cost under-estimate**; over-scoping | Real briefs → expected manifest shape (anima already has 10 grounded cases). Include under-spec + ambiguous-tone briefs. | Plan-validity (schema-valid + executable) = **deterministic**. Cost-estimate accuracy = **MAPE on non-zero phases + % within budget**. | Mostly **deterministic** (schema validation, executability). LLM judge only for "did it choose sensible phases" — and the human approval gate already absorbs much of this. |
| **Cy** (character designer, Opus+Gemini+NB2) | Generator + verifier | Identity drift from anchor; style-register drift; plate that photocopies anchor (no variation); under-specified Bible silently failing to constrain | Reproduce the two real Bibles; deliberately-broken plate; under-spec source-refs (intentionally red). anima has this. | **DINOv2 cosine vs per-view anchor (deterministic)**; Subject-Collapse-Rate-style per-plate threshold count, not mean; IR-rule coverage. | **Deterministic-first** (DINOv2 + T1). Gemini's Pass-3 prose verify is the LLM layer — best framed **pairwise** (plate vs anchor) per §3.5. Never DINO alone as "good" gate. |
| **Em** (T2 vision critic, Gemini/Opus) | Critic (judge) | **False pass** (drifted frame let through) — the costly one; missing motion defects; citing wrong/no criterion; verbose-bias, position-bias | Real Act 1/2 + Cy frames, **balanced** (defects *and* clean frames), labeled by actual defect + expected `cites_criteria`. Ships red. | **Precision/recall on defect class + false-pass rate** (never raw agreement / F1 alone). `cites_criteria` density + correctness. Wall-time. | **LLM judge is the agent under test** — so calibrate it against Sean's labels (§3.1–3.2). Identity drift → back with **DINOv2**; low-level artifacts → **T1 rules**; **motion → dedicated metric or human, NOT contact sheet alone**. Prefer pairwise. |
| **Mo** (museum writer, Sonnet) | Generator (prose) | Inventing facts the exhibit doesn't carry; narrating a thin exhibit as rich; tonal drift | Real exhibits (incl. deliberately thin ones) → expected: faithful, honestly-sparse prose. | **Faithfulness / hallucination rate** (every claim grounded in the exhibit) = primary. Style-adherence secondary. | **LLM judge appropriate** for faithfulness (or DeepEval's faithfulness scorer) — but a **deterministic check** that Mo invents no entity absent from the structured exhibit is cheaper and catches the load-bearing failure. |
| **Flo** (Phase 5 router) | Router | Wrong-tier routing (hero sent cheap / in-between sent to NB Pro); cost over/under-run; missed escalation | Shot specs → expected model/tier. Grounded in real routing-table decisions. | **Routing accuracy (m-way classification)** + **cost realized-vs-predicted** + escalate-decision precision/recall. | **Deterministic** — routing is a classification check against expected tier; cost is arithmetic. No LLM judge needed. |
| **Sam** (scriptwriter, Opus) | Generator (creative) | Surface pastiche vs real stylistic-mechanism modeling; beat/structure failures; voice drift | Few, hand-labeled, real script attempts; **pairwise** preference (this draft vs that). Subjective → small set. | **Pairwise win/lose/tie** preference (Sean) + structural checks (beat coverage). | **LLM judge weak/secondary** for creative quality (subjective, self-preference risk). Lean on **Sean's pairwise preference**; LLM judge only for mechanical structure checks. |
| **Bea** (storyboard, Sonnet) | Generator | Script↔board conflict; shot-coverage gaps; composition errors | Real boards vs script; conflict cases. Lowest-confidence assignment (65%) → bake-off candidate. | Coverage/consistency checks + **blind Sean preference + revision count** (the brainstorm §8 metric). | **Mixed** — deterministic coverage checks; **human preference** for composition quality. Three-way bake-off (Sonnet/Gemini/Codex) is sequenced. |
| **T3 council** (Codie/Annie/Sage + chairman) | Multi-judge panel | Voices collapsing into agreement (no dissent value); chairman self-favoring / dropping dissent; correlated blind spots | Phase-transition artifacts with known issues; measure panel vs single-judge. | **Panel value-add over single judge** (PoLL: κ delta); **dissent richness**; **chairman synthesis fidelity** (represents consensus *and* dissent). | **LLM judges by definition** — defend by cross-vendor construction (already done), position-swap, distinct chairman call. Sage-tier ablation sequenced as bake-off #2. |
| **Orchestrator** (Sonnet) | Controller | DAG state errors; restart/retry-loop rate; criteria-lock enforcement failures | Real run traces; drift test over N pieces (brainstorm §8 bake-off #4). | **Restart rate** (promote to Opus if >10%); cache-correctness; criteria-lock enforcement = **deterministic**. | **Deterministic** — state/JSON discipline checks, not LLM-judged. |

### What anima should track run-over-run to know the fleet is — and stays — "100% solid"

"100% solid" is an empirical claim, and the signals that keep it true at solo scale are few and cheap:

1. **Per-agent baseline trace, scored, dated.** No agent ships without one. The pass-rate (and for critics, the confusion matrix) on the golden set, captured in `last-run.md` + `traces/baseline-*.md`. This is already the discipline; the only gap is that some agents (Mo, Em) shipped with smoke traces instead of scored ones — which the critic-spine session closes for Em.
2. **For every critic, the false-pass rate over time.** The one number that, drifting up silently, means the fleet is rotting from the gate inward. Watch it specifically; it will not show up in a pass-rate.
3. **Cost realized-vs-estimated per run.** Maya's estimate vs Flo's actual spend — the drift signal for both the planner and the router, and a cheap honesty check on the whole pipeline's cost model.
4. **Model-snapshot pin + re-baseline-before-bump.** The silent-regression catcher. Pin Codex/Anti-Gravity/SDK model versions; when a provider bumps, re-run the relevant bake-off against the new snapshot *before* migrating. This is the discipline anima most lacks today and the one most likely to cause a silent critic regression.
5. **Dated bake-offs as the empirical record.** Every model choice in the fleet should have a dated bake-off behind it under `evals/bakeoffs/` — the artifact that answers "why this model" with evidence, and doubles as museum content.

Open question worth surfacing to Sean (not deciding here): the per-agent matrix above and the run-over-run signals arguably warrant their own source-of-truth doc or a `CLAUDE.md` pointer, so the fleet-wide eval strategy doesn't live only inside a dated research file. Flagged for Sean's call during the fold-back.

---

## 7. Sources

Primary/practitioner sources preferred throughout. Each note says what the source supports.

**Eval first principles (mandate A)**
- Hamel Husain, *A Field Guide to Rapidly Improving AI Products* — https://hamel.dev/blog/posts/field-guide/ — error analysis as #1 activity; binary-over-Likert; synthetic-data rules; data-viewer.
- Hamel Husain, *AI Evals FAQ* (error analysis; how many annotators) — https://hamel.dev/blog/posts/evals-faq/ — ~100-trace / theoretical-saturation rule; benevolent-dictator annotation.
- Anthropic, *Demystifying Evals for AI Agents* (2026-01-09) — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents — capability vs regression evals; 20–50 tasks to start; class balance; trial isolation/leakage; outcome-vs-trajectory; pass@k vs pass^k; "don't trust a green score."
- Eugene Yan, *Evaluating the Effectiveness of LLM-Evaluators* — https://eugeneyan.com/writing/llm-evaluators/ — binary + classification metrics; pairwise-with-tie for subjective; human-human agreement ceiling; κ conservatism.
- Eugene Yan, *Product Evals in Three Simple Steps* — https://eugeneyan.com/writing/product-evals/ — spreadsheet-first; data-before-criteria.
- Shankar et al., *Who Validates the Validators?* (UIST 2024) — arXiv:2404.12272 — criteria drift; EvalGen; you can't fully specify criteria before grading.

**LLM-as-judge calibration & biases (mandate B)**
- Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* (NeurIPS 2023) — arXiv:2306.05685 — GPT-4 judge >80% human agreement = human-human level (the foundational result); position/verbosity/self-enhancement bias named.
- *SycEval: Evaluating LLM Sycophancy* (AIES 2025) — arXiv:2502.08177 — **confirms 58.19%** sycophancy-under-rebuttal; 43.52% progressive / 14.66% regressive / 78.5% persistence.
- Ye et al., *Justice or Prejudice? / CALM* (ICLR 2025) — arXiv:2410.02736 — **corrects the misattributed "+90%"**; quantifies biases via robustness/error rate, not "+90%."
- Panickssery, Bowman & Feng, *LLM Evaluators Recognize and Favor Their Own Generations* — arXiv:2404.13076 — the real self-preference paper; mechanism (self-recognition → self-preference), not a +90% magnitude.
- Verga et al., *Replacing Judges with Juries (PoLL)* — arXiv:2404.18796 — **corrects "+9.8pp"** to κ +0.136 (0.627→0.763), 7× cheaper; the cross-provider-panel defense.
- Wang et al., *Large Language Models are not Fair Evaluators (FairEval)* — arXiv:2305.17926 — position bias: order-swap flipped 66/80 verdicts; balanced-position-calibration defense.
- Shi et al., *Judging the Judges: Position Bias* (AACL 2025) — arXiv:2406.07791 — position bias systematic study; worse for close-quality pairs.
- Saito et al., *Verbosity Bias in Preference Labeling* — arXiv:2310.10076 — length/verbosity bias.
- Databricks, *Enhancing LLM-as-a-Judge with Grading Notes* — https://www.databricks.com/blog/enhancing-llm-as-a-judge-with-grading-notes — rubric injection cut misalignment 67.5% (GPT-4o) / 85% (Llama3) — the strong rubric-injection evidence.
- *Judge's Verdict* (NVIDIA, 2025) — arXiv:2510.09738 — match human variance, not maximize agreement; |z|<1 human-like vs super-consistent.
- *Overconfidence in LLM-as-a-Judge* — arXiv:2508.06225; calibration survey — verbalized confidence badly miscalibrated (ECE>0.377; GPT-4 AUROC ~63%); use sampling consistency.
- Hamel Husain, *Using LLM-as-a-Judge: A Complete Guide* — https://hamel.dev/blog/posts/llm-judge/ — Critique Shadowing; >90% agreement in 3 iterations; raw-agreement-under-imbalance warning.

**Vision / video eval (mandate B, vision)**
- Ruiz et al., *DreamBooth* — arXiv:2208.12242 — DINO score; DINO > CLIP-I for identity; DINO over-rewards copying.
- Huang et al., *VBench* (CVPR 2024) — arXiv:2311.17982 — subject/background consistency, temporal flickering, motion smoothness, dynamic degree; consistency↔dynamism trade-off; per-dimension human validation. (++ arXiv:2411.13503; 2.0 arXiv:2503.21755.)
- Ge et al., *On the Content Bias in FVD* (CVPR 2024) — arXiv:2404.12391 — FVD blind to temporal corruption; avoid for motion artifacts.
- *Fréchet Video Motion Distance (FVMD)* — arXiv:2407.16124 — motion-consistency metric.
- Lai et al., *Learning Blind Video Temporal Consistency* (ECCV 2018) — arXiv:1808.00449 — warping error / E_warp.
- *Breaking Down Video LLM Benchmarks* — arXiv:2505.14321 — **the load-bearing finding: MLLMs pass shuffled frames** → frame-grid judges don't see motion.
- Kim et al., *An Image Grid Can Be Worth a Video* — arXiv:2403.18406 — contact-sheet works for content/identity QA (not motion).
- *VideoJudge* — arXiv:2509.21451 — real frames > text-description reasoning; small specialist > big generalist.
- Chen et al., *MLLM-as-a-Judge* (ICML 2024) — arXiv:2402.04788 — pairwise > absolute scoring; egocentric/position/length bias + hallucination.
- *Q-Bench* (ICLR 2024) — https://q-future.github.io/Q-Bench/ — MLLMs weak on low-level visual quality → keep T1 + DINOv2.
- *Subject Collapse / multi-subject stress test* — arXiv:2603.26078 — per-plate threshold-count (SCR) over mean; per-view anchors.

**Metrics & tracking (mandate C)**
- Hamel/Shankar, *LLM Evals: Everything You Need to Know* — https://hamel.dev/blog/posts/evals-faq/ — TPR/TNR over raw agreement; bias-correct the judge's reported rate.
- *How to Correctly Report LLM-as-a-Judge Evaluations* — arXiv:2511.21140 — bias-corrected defect-rate estimator.
- *Balanced Accuracy for LLM Judges* — arXiv:2512.08121 — F1 hides true negatives; report the full confusion matrix.
- RouterEval / LLMRouterBench — https://www.emergentmind.com/topics/llmrouterbench — routing as m-way classification + cost curve; 40–70% savings at <2% quality loss.
- Prompt-regression / model-churn practice — https://promptbuilder.cc/blog/prompt-testing-versioning-ci-cd-2025 — pin dated snapshots ("gpt-4o is not a version; gpt-4o-2024-08-06 is"); re-baseline before bump.
- Eugene Yan, *An LLM-as-Judge Won't Save the Product — Fixing Your Process Will* — https://eugeneyan.com/writing/eval-process/ — evals are a practice, not a dashboard.

**Tooling (mandate D)**
- Inspect (UK AISI) — https://inspect.aisi.org.uk/ (+ scorers https://inspect.aisi.org.uk/scorers.html) — Task/Solver/Scorer; reducer; stderr()-on-metrics; model_graded_qa template.
- DeepEval (Confident AI) — https://github.com/confident-ai/deepeval — pytest-native; 50+ scorers; the one dependency worth considering.
- promptfoo — YAML case files + CI gating + red-teaming. OpenAI Evals — https://github.com/openai/evals — `modelgraded/*.yaml` judge templates.
- Braintrust / LangSmith / W&B Weave — SaaS team tools; skip for solo. Arize Phoenix, Langfuse — self-hostable OSS trace UIs if ever needed.

**Source-quality caveats.** The judge-bias and vision findings are peer-reviewed/primary (high confidence). The motion-failure *taxonomy terms* (boiling, texture-crawl, skating) are industry-standard but their tidiest write-ups are non-peer-reviewed teardowns — the underlying claims are corroborated by the primary temporal-metric papers cited. The exact DreamBooth DINO/CLIP-I table values weren't extractable from the PDF in-session; that source is cited for its *definitions and stated rationale*, confirmed in search excerpts. "Criteria injection +3pp" remains uncited — treated as directionally-plausible-but-unsupported, with Databricks Grading Notes substituted as the real evidence.

---

*Findings doc. The ruler, calibrated, before the fleet is measured by it. Next step per the program: present to Sean on its own terms, then — only after — fold the verified method into the critic-spine kickoff (Phase 0 case-design discipline, Phase 1 motion-sight honesty, Phase 2 judge-calibration + bias-defense procedure).*
