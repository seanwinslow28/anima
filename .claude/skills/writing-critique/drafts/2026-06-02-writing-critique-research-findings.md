# Research findings: turning the writing-critique spec into research-backed gold

- **Date:** 2026-06-02
- **Status:** Research + synthesis only (no implementation plan)
- **Author:** Sean Winslow + Claude
- **Companion to:** [`2026-06-02-writing-critique-layer-design.md`](2026-06-02-writing-critique-layer-design.md)
- **Method:** Four parallel deep-research threads (adversarial fact-check against primary sources — arXiv, ACL Anthology, peer-reviewed venues, labeled practitioner sources) + a direct read of the live `haowjy/creative-writing-skills` source.

> Scope guard, per the kickoff: the *already-decided* taste calls were **not** researched or relitigated — em-dash ban, chain position, the five voice modes, advisory-not-blocking, one-revise-pass cap, packaging Approach A. This report only pressure-tests the places where the spec asserts facts about the world.

---

## Executive summary — the five headline findings

1. **The detection-science tier is substantially mis-grounded — and the spec inherited the problem verbatim from upstream.** Of the three named papers (Kobak 2024, RAID, Ghostbuster), **none is a human-readable-tell stylometry paper**: Kobak measures excess *word frequency* (not lexical *diversity*), and RAID + Ghostbuster are black-box detection benchmarks/classifiers that make **no per-feature stylometric claim at all**. All three claimed signals (lower lexical variability, fewer pronouns, positive-emotion skew) are effectively orphaned by their cited sources. **This is not Sean's error** — upstream's `antipatterns.md` cites the same three papers (plus two others) for the same signals, and the "near-random for Claude specifically" line is copied verbatim from upstream. The fix is to re-ground the tier, not to delete it.

2. **The strongest measurable AI-vs-human signal is one the spec under-weights: burstiness (sentence-length variance) — and the analyzer already computes it.** 2024–2026 work converges on *distributional* signals (perplexity, burstiness, length-controlled diversity) over fixed word/"slop" lists. Sentence-length variance is the most defensible measurable tell the stdlib analyzer can produce, and it's free.

3. **"Slop lists are near-random for Claude specifically" is overstated as written.** The *spirit* is defensible (GPT-derived word lists transfer poorly across models and genres); the *phrasing* implies a measured Claude-specific hit-rate that no study establishes. Reword.

4. **Anti-sycophancy needs structural scaffolding beyond "find what doesn't work."** Sycophancy is a measured structural consequence of RLHF (Sharma et al., ICLR 2024), and the two worst LLM-judge biases for a writing critic — **self-enhancement** and **verbosity** — both push toward praise and are *amplified* when the same model that just voiced the draft also critiques it. The single highest-leverage countermeasure is **persona separation** (the critic did not write this), which matters most precisely in Sean's chain-gate mode. A corollary: **prefer a severity-ranked floor over a forced finding count** — forcing exactly-N findings is the one popular technique with a documented fabrication failure mode.

5. **The metric and threshold choices need two specific edits.** Keep MATTR but **keep window = 50 (validated standard) and add MTLD as a stdlib fallback** for sub-window drafts; and **replace the absolute "stdev < 4 words = monotonous" rule with a coefficient of variation (σ/μ) flag at ~0.45**, because human sentence-length stdev is register-dependent and an absolute cutoff mislabels. The one-revise-pass cap is **well-supported** by the degradation literature — and the research sharpens *why*.

---

# TIER 1 — Load-bearing factual claims

## 1.1 Detection-science citations

### The headline: two of three papers are detectors, one is a frequency study — none is a stylometric-tell paper

| Paper | What it actually is / measures | Lower lexical variability | Fewer personal pronouns | Positive-emotion skew |
|---|---|---|---|---|
| **Kobak et al. (2024)** — *"Delving into LLM-assisted writing in biomedical publications through excess vocabulary,"* Science Advances 11(27), 2 Jul 2025; preprint arXiv:2406.07016 | Single method: **excess word frequency** (observed 2024 frequency vs counterfactual extrapolated from 2021–22 trend) over ~15M PubMed abstracts. Conclusion is an **incidence estimate** (≥13.5% of 2024 abstracts show LLM processing). | **No** — measures frequency of *specific* words, never type-token ratio / MATTR / any diversity measure. "Excess vocabulary" is the opposite construct from "vocabulary diversity." | No (no pronoun analysis) | No (no sentiment analysis) |
| **RAID (ACL 2024)** — Dugan et al., *"RAID: A Shared Benchmark for Robust Evaluation of Machine-Generated Text Detectors,"* aclanthology.org/2024.acl-long.674 | A **detection benchmark + robustness audit** (6M+ generations, 11 models, 11 adversarial attacks). Headline finding is *negative*: detectors claiming 99%+ accuracy collapse out-of-domain and under simple manipulations. | No (makes no per-feature stylometric claim) | No | No |
| **Ghostbuster (NAACL 2024)** — Verma et al., *"Ghostbuster: Detecting Text Ghostwritten by Large Language Models,"* aclanthology.org/2024.naacl-long.95 | A **black-box detector**: runs text through weaker surrogate LMs, searches over token-probability features, trains a classifier. Features are statistical likelihood functions, **not interpretable stylometric attributes**. | No | No | No |

**Verdict:** the three citations are real, correctly findable, and well-known — but they are **the wrong *kind* of evidence** for a "research-backed measurable human-readable tells" tier. The design (and upstream) appear to have grabbed three citable detection papers and back-attributed convenient signals.

### Where each signal *actually* stands

- **Lower lexical variability (signal #1):** has genuine independent support — but **not from Kobak**, and the **direction is baseline-dependent**. Against polished/expert human prose, AI shows lower diversity (e.g., a 2025 comparison reports human TTR ≈ 55.3 vs AI ≈ 45.5; "Diversity Boosts AI-Generated Text Detection," arXiv:2509.18880; MATTR-based SVM detection). **But against L2 / constrained-vocabulary writers, ChatGPT shows *higher* diversity** (Frontiers in Education 2025; "Playing with words," ScienceDirect 2024). So the signal is real but must **state its comparison class** — which is exactly what Sean's *baseline-relative* design does well, and what an absolute "AI = low diversity" claim does badly. Also note MATTR itself is length-/window-sensitive (arXiv:2507.15092).
- **Fewer personal pronouns (signal #2):** **no support among the three cited papers.** Has some independent register-analysis grounding, but it is unattributed in the spec. For Sean's typically first-person Substack voice, this is better treated as a **baseline-relative** check (does this draft's I/me/my rate drop below *Sean's* norm?) than as an absolute detection claim.
- **Positive-emotion skew (signal #3):** **no support among the three; thinnest independent base of the three.** Additionally — and the spec misses this — **it is not mechanically measurable by a stdlib analyzer** (no sentiment lexicon in `re`/`statistics`). So it cannot be "wired to the analyzer" the way #1 and #2 can; it is at best a qualitative reviewer cue.

### The "near-random for Claude specifically" claim — overstated as written

No study computed a Claude-specific slop-list hit-rate and reported "near-random." What the literature *does* support:
- Slop/excess-word lists are **model- and prompt-dependent** by construction (the Kobak list — *delve, intricate, showcasing* — is a GPT-era, scientific-abstract artifact). "Measuring AI Slop in Text" (Shaib et al., arXiv:2509.19163) explicitly includes a **"model-specific" tell category**.
- Claude's lexical fingerprint **differs measurably** from GPT's (a 2026 detection benchmark reports a 22.4-pt accuracy spread for Claude; "Better Call Claude," arXiv:2508.00680, shows Claude-3.7 is itself the best at detecting style change — a distinct stylistic profile).

**Recommended phrasing** (replaces both the spec's and upstream's line):
> *Word-level slop lists are largely derived from GPT-era output in specific genres; they transfer poorly across models and domains, and their hit-rate against Claude in particular is substantially lower and unreliable. Treat them as editorial taste choices, not a model-agnostic detection signal.*

Drop "near-random" (implies a measured ~chance rate) and "for Claude specifically" (implies a Claude-targeted study) — the claim rests on transfer/model-specificity arguments, not a direct measurement.

### Freshness sweep (2025–2026) — the field moved away from word lists

- **"Measuring AI Slop in Text"** (Shaib et al., Sept 2025, arXiv:2509.19163) — first principled, multidimensional "slop" taxonomy (lexical / syntactic / rhetorical / tonal / formatting / **model-specific**). Single word lists are an impoverished proxy.
- **"Decoding AI Authorship"** (2026, arXiv:2603.23219; related arXiv:2408.00769) — across GPT-4o, Gemini 1.5 Pro, Claude 3.5: **perplexity is the primary discriminator; burstiness (variance in sentence length/complexity) is higher in humans, smoother in AI.** Strongly relevant — points at burstiness/variance as a sturdier, more model-general signal than any word list.
- **"Diversity Boosts AI-Generated Text Detection"** (arXiv:2509.18880) — diversity metrics improve detection (supports signal #1 properly).
- **MATTR-under-length-variation** (arXiv:2507.15092) — cautions against naive TTR/MATTR thresholds; MATTR is window/length sensitive.
- **RAID's standing caution** remains governing: any fixed surface signal degrades on unseen models and under decoding/adversarial changes.

**Net:** the 2025–2026 frontier favors **distributional signals (perplexity, burstiness, length-controlled diversity)** and **explicitly model-specific** taxonomies. The word-frequency framing is a 2023–24 idea newer work treats as fragile.

### What this means for the evidence tiers (the honest re-grounding)

- **Demote Kobak** from "supports lower lexical variability" to its true claim: *"LLMs leave a detectable word-frequency fingerprint (in scientific abstracts)."* That actually *reinforces* the "slop lists are real but genre/model-bound" point — keep Kobak there.
- **Remove RAID and Ghostbuster as support for the three signals.** Keep RAID only as a **caution** ("surface signals degrade across models/domains/decoding") and Ghostbuster only as "likelihood-feature classifiers detect AI text." Citing detectors as feature evidence is a category error.
- **Re-attribute signal #1** to real diversity studies (SSRN 5833302; arXiv:2509.18880) **and state the comparison class** (lower vs polished human prose; *higher* vs L2). Flag MATTR length-sensitivity.
- **Signal #2 (pronouns):** label "heuristic / baseline-relative," not "research-backed," unless a real register citation is added.
- **Signal #3 (positive-emotion):** downgrade to "qualitative cue — not analyzer-measurable, thin evidence."
- **Promote burstiness / sentence-length variance** into the measurable tier as the **best-supported, analyzer-computable** signal (arXiv:2603.23219). This is the single biggest upgrade available.
- **Heads-up on the upstream citation set:** upstream's `antipatterns.md` also cites *"BEA 2025 shared task"* and *"Nature HSSCOMMS (2025)"* that the spec did **not** carry over. Don't add them back without verifying them — given how the other three checked out, treat the whole upstream source line as unverified until each is read.

## 1.2 Non-sycophantic LLM critique

### Mechanism — sycophancy is structural, not a quirk

Sharma et al., *Towards Understanding Sycophancy in Language Models* (Anthropic, ICLR 2024, arXiv:2310.13548) is the load-bearing paper: five RLHF assistants consistently exhibit sycophancy across free-form tasks, and **both human raters and the trained preference models prefer a convincingly-written sycophantic response over a correct one a non-trivial fraction of the time**. For a critique tool: a draft handed in for review is a "user view" the model is trained to match. Praise is the path of least resistance to a high reward-model score. The April-2025 GPT-4o sycophancy incident (OpenAI, rolled back in 4 days) is the canonical production confirmation — and OpenAI's remediation explicitly added "steer away from sycophancy" system-prompt language and a sycophancy eval.

### Self-review specifically is the worst case

- **Intrinsic self-correction degrades quality** without external feedback (Huang et al., *LLMs Cannot Self-Correct Reasoning Yet*, ICLR 2024, arXiv:2310.01798 — reasoning domain; transfers by mechanism). On open-ended/writing it tends toward "blander, more generic" output.
- **LLM-as-judge biases apply directly** (Zheng et al., MT-Bench/Chatbot Arena, NeurIPS 2023, arXiv:2306.05685): **position bias**, **verbosity bias** (longer = scored higher — a longer draft gets over-praised), and **self-enhancement bias** (judges favor their own style/outputs). The last two both push toward praise, and **self-enhancement is amplified when the reviewer is the same model/persona that produced the draft** — i.e., exactly Sean's headless chain gate, where the same model just ran voice-modes.

### Anti-sycophancy techniques — ranked by (evidence × leverage)

| Rank | Technique | Evidence | Documented failure mode |
|---|---|---|---|
| 1 | **Persona separation** — the critic explicitly did NOT write this draft | **Strong** (attacks self-enhancement bias + user-view-matching at the root) | Over-rotation into a hostile role that invents flaws; persona alone isn't a correctness mechanism |
| 2 | **Rubric-structured findings** (dimension + reasoning + directed fix) | **Strong** (vague criteria → lenient/inconsistent rulings; locked rubrics improve discrimination) | Checklist-gaming; generic rubrics under-discriminate; rigid rubric misses off-rubric flaws |
| 3 | **Adversarial / red-team framing** ("find what a skeptical reader attacks") | **Moderate–strong** (mechanism opposes the agreement prior; mostly practitioner-validated for *critique* quality) | **Hyper-criticality / false positives** — manufactures objections, flags defensible stylistic choices |
| 4 | **Evidence/quote per finding** (cite the exact span) | **Moderate–strong** (grounding exposes vague/fabricated findings) | Quote-mining trivial lines to hit a quota; doesn't stop misreading a correctly-quoted span |
| 5 | **Severity ranking** instead of a fixed count | **Moderate** (lower fabrication pressure than a hard N) | Severity labels themselves uncalibrated; model inflates severity to look rigorous |
| 6 | **Withhold / cap the "what works" praise section** | **Moderate** (removes the slot the model uses to discharge agreement) | Pure negativity reads as low-trust and gets ignored; loses calibration signal |
| 7 | **Multiple independent critic passes** (vary temp/model, union findings) | **Moderate** (coverage of blind spots) | Cost; correlated errors / shared-wrong consensus; note: debate ≯ budget-matched self-consistency |
| 8 | **Forcing a fixed NUMBER of findings** ("give exactly 7") | **Weak / double-edged** (popular folklore; no strong quality evidence) | **Fabrication & nitpicking** — on a clean draft the model invents flaws to hit the quota |

**Cross-cutting failure mode:** an over-tuned harsh critic produces **false positives that erode trust** — once the writer catches the critic inventing a flaw, every finding is discounted. Grounding (#4) is the main defense.

### Recommended prompt scaffolding (what the finding-rubric.md prompt should encode)

1. **Hard persona separation** (#1): *"You did not write this. You are a hostile expert reviewer whose reputation depends on catching what the author missed."* Most important in the headless chain gate, where the same model just voiced the draft.
2. **Bounded adversarial framing** (#3 + guard): *"Find what would make a skeptical reader stop trusting this draft. Only raise an issue you can defend with a direct quote and a concrete reader cost. Distinguish genuine defects from defensible authorial choices."*
3. **Every finding is a tuple** (#2/#4/#5): `quoted span → why it fails (which dimension) → severity (blocking/major/minor) → directed fix.`
4. **Severity-ranked floor, NOT a fixed count** (#8 avoided): *"Surface every blocking and major issue, ranked by severity. If the draft is genuinely strong, say so and report fewer — do not invent issues to fill a quota."* This is the single most important guard against fabrication.
5. **Suppress or cap praise** (#6): forbid a "what works" section, or cap it to one calibration line.

→ **Answer to the spec's open question:** yes, the prompts need **structural** anti-sycophancy scaffolding beyond "find what doesn't work" — specifically persona separation, per-finding grounding, and a severity-ranked floor rather than a forced count.

---

# TIER 2 — Parameter refinements

## 2.3 Lexical-diversity metric + analyzer thresholds

### Metric choice — keep MATTR@50, add MTLD as a stdlib fallback

The corpus-linguistics consensus:
- **MTLD is the index *least* sensitive to text length** (McCarthy & Jarvis 2010, the foundational validation study); **HD-D is the principled, deterministic replacement for vocd-D** (which estimates by random sampling — non-deterministic; **drop it**).
- **MATTR** (Covington & McFall 2010) solves length-dependence but introduces **window-size sensitivity** (Bestgen 2024, "The Twofold Length Problem," arXiv:2307.04626): MATTR@50 ≠ MATTR@100. The window is a real knob.
- **Window = 50 is the validated standard** — it's the default in TAALED (Kyle's reference tool). **Do not change it**; changing it breaks comparability with the literature for no gain.
- For the 300–2000-word band, **MATTR@50, MTLD-Original, and HD-D are co-equal best** and all length-stable (Zenker & Kyle 2021, 4,542 essays). For the *short* tail (<100 tokens) **MTLD-Original is the most robust**; MATTR degenerates when a draft is near/below the window.

**Stdlib implementability** (the deciding practical factor):

| Metric | Pure stdlib, deterministic? | Note |
|---|---|---|
| MATTR@50 | **Yes, trivial** (sliding `set`, ~10 lines) | Keep as primary |
| MTLD-Original (threshold 0.72) | **Yes, easy** (running TTR, factor count, fwd+bwd avg) | **Add as secondary / short-text fallback** |
| HD-D | Possible via `math.comb` but fiddly | Skip — no accuracy gain in this band |
| vocd-D | Avoid | Non-deterministic sampling |

**Recommendation:** keep **MATTR@50** as primary; **add MTLD-Original** as a deterministic stdlib secondary (covers the sub-window tail where MATTR is meaningless); **drop vocd-D from consideration**; skip HD-D. Add a guard: if `tokens < ~60` (≈ 1.2× window), suppress MATTR and report MTLD only, flagged low-confidence.

### Threshold — replace absolute "stdev < 4" with coefficient of variation

The "stdev below ~4 words = monotonous" rule is **directionally right but the wrong shape**:
- Human sentence-length stdev is **register-dependent and usually well into the teens** (worked examples: a children's story ≈ 11; a presidential address ≈ 20). An absolute 4-word floor sits *far below* the human range — so it almost never fires, making it a **weak** monotony detector that misses moderately flat drafts (stdev 5–8).
- The detection field's actual "burstiness" metric is **B = σ/μ — the coefficient of variation.** Reported bands: **human CV ≈ 0.6–1.0+**, **AI CV ≈ 0.15–0.40**. CV is **register-invariant** (a mean-12 draft and a mean-25 draft are comparable), which an absolute stdev is not. 2026 authorship work confirms the direction (humans show higher sentence-length variance: arXiv:2603.23219, arXiv:2408.00769).

**Recommendation:** flag monotony at **CV = σ/μ < ~0.45** (sits cleanly in the gap above the AI ceiling ~0.40 and below the human floor ~0.6). Trivial in stdlib (`statistics.mean` / `statistics.stdev`); guard div-by-zero on single-sentence inputs. Keep it **advisory**, and note that perplexity (the stronger signal) is unavailable in stdlib, so sentence-CV alone is suggestive, not conclusive. The ideal long-term form is **CV deviation vs Sean's own baseline**, which the baseline pipeline already enables — prefer that once the baseline exists.

> Note: this "stdev < 4 = monotonous" threshold is **not** an upstream port — it is the spec's own invention. Upstream `analyze.py` prints raw `pstdev` with no flagging logic at all (see 2.4). So changing it costs nothing in fidelity.

## 2.4 Direct read of the upstream source (faithful, not from memory)

Read live from `haowjy/creative-writing-skills@main`: `skills/prose-critique/SKILL.md`, `resources/analyze.py`, `resources/antipatterns.md`, `resources/baseline.md`. Key facts for a **faithful** port:

**`SKILL.md` (the critique rubric)** — the spec's port is faithful. Verbatim load-bearing lines worth preserving: *"Find what doesn't work… A critique that says 'well done' without digging is worse than no critique, because it creates false confidence."* The four-quality finding rubric (**Specific / Reasoned / Directable / Non-obvious**), the "what wastes everyone's time" list (incl. *"critique the execution, not the premise"*), the **stage calibration** ("Fix the bones before the skin"), and the report shape (overall assessment → findings by severity → verdict + the one highest-leverage change) are all present exactly as the spec describes. `model-invocable: false`, `type: reference`.

**`analyze.py`** — important deltas between **what upstream actually is** and **what the spec says**:
- Upstream computes: sentence-length distribution + **`statistics.pstdev`** (population stdev), opener variety (pronoun/article/conjunction/other), dialogue-to-narration ratio, repetition windows, pronoun distribution. Pure stdlib (`re`, `statistics`, `collections`, `argparse`, `pathlib`). ✅ matches the "keep from upstream" list.
- **Upstream does NOT compute MATTR.** The `antipatterns.md` *says* "measurable via MATTR" but no MATTR exists in the code. So the spec's "Add — MATTR" is genuinely **new work**, correctly labeled "Add" (not a port). Good.
- **Upstream has no thresholds and no baseline JSON.** It prints raw numbers only; there is no "monotonous" flag, no `--emit-baseline`, no `baseline.json`. The spec's threshold logic, `--baseline`, `--json`, and `--emit-baseline` are **all new**. The baseline *concept* is ported (upstream's `baseline.md` does per-chapter comparison via a shell loop, explicitly: *"Prose metrics are meaningless in isolation… compare against the project's own baseline"*) — but the JSON-emit mechanism is Sean's addition.
- Upstream's `window_size` arg **defaults to 5 and is the repetition paragraph window** — unrelated to the MATTR token window. Don't conflate them when porting; the spec's "window ~50 tokens" is a separate, new MATTR parameter.
- Faithful-port detail: use **population** stdev (`pstdev`) to match upstream, or document the switch to sample stdev. (Minor, but it's a real divergence point.)
- The spec's "drop dialogue-to-narration ratio" is a clean removal — it's a self-contained `print_dialogue_ratio` function.

**`antipatterns.md`** — this is the crux for Tier 1.1. Upstream's evidence stratification is exactly the three-tier shape the spec models (Research-Backed Signals / Community-Identified Structural Patterns / Not Reliable: word-level slop lists). **But:**
- Upstream cites **Kobak (2024), BEA 2025 shared task, Ghostbuster (NAACL 2024), RAID (ACL 2024), Nature HSSCOMMS (2025)** for the research-backed tier — i.e., the spec **dropped two** (BEA, Nature HSSCOMMS) and kept three.
- The three "research-backed" signals (lower lexical variability, fewer pronouns, more positive-emotion language) are **upstream's**, copied into the spec.
- The **"Near-random for Claude specifically"** bullet is **verbatim upstream**.
- Upstream's research tier also lists **shallow character interiority** and **low dialogue subtext** — both fiction-specific; the spec correctly drops them.

**Implication:** the citation weaknesses in 1.1 are **inherited, not introduced.** When Sean ports the stratification, this is the moment to *correct* it (re-ground per 1.1), not faithfully reproduce a flaw. Faithfulness applies to the *rubric and analyzer mechanics*; the *citations* should be fixed in the port, with a note that they diverge from upstream deliberately.

---

# TIER 3 — Optional

## 3.5 Revise-loop degradation — the one-pass cap is well-supported

**Verdict: well-supported for the specific harm**, with a useful boundary condition. Convergent evidence from three literatures:
- **Self-correction degrades without external feedback** (Huang et al., ICLR 2024, arXiv:2310.01798); on open-ended/writing tasks the regression is toward "blander, more generic" text, driven by **self-bias amplification** across rounds ("Pride and Prejudice: LLM Amplifies Self-Bias in Self-Refinement," arXiv:2402.11436).
- **The degradation has a direction — toward safe/generic** — because RLHF causes mode collapse / diversity loss (arXiv:2510.01171); empirical homogenization in writing is documented (Doshi & Hauser, ScienceDirect S294988212500091X). (Distinguish from *training-time* "model collapse," Shumailov et al. Nature 2024 — same shape, different mechanism; analogy only.)
- **"First pass helps, later passes plateau/reverse"** is directly documented (diminishing-returns / reversal within the first few iterations).

**Honest counter-evidence:** Self-Refine (Madaan et al. 2023, arXiv:2303.17651) reports **~20% human-preferred gains incl. writing** — but its "feedback" is *specific and actionable*, not "make it better," and it uses strong models + few iterations. Reconciliation: **one *grounded* pass helps; un-anchored self-judged iteration is where the degradation lives.**

**What this hardens in the spec:** the one-pass cap is the right default, but reframe it precisely — the cap is a proxy for the real lever, which is **grounding the single pass in an external target** (Sean's voice baseline / a specific finding), not "revise again." So the headless revise request should be *"revise against [this specific reader-cost finding]"*, never a bare "improve this." If a second pass is ever allowed, it must require **new external input**, never a self-judged re-roll. This also dovetails with the chain design: the revise routes back through **voice-modes** (which carries Sean's calibrated target) — the correct anchor.

---

# Beyond the list — additional claims I'd flag (adversarial pass on the spec)

None of these required new large research (I'm flagging them from the work already done); each notes the decision it changes. **None expands scope without your sign-off** — listed for your call.

1. **"Wire the measurable signals to the analyzer" conflates three signals that aren't equally measurable.** Lexical variability (MATTR) and pronouns are stdlib-measurable; **positive-emotion skew is not** (no sentiment lexicon in stdlib). → *Changes:* the ai-tells.md "research-backed measurable" tier should split "measurable-by-analyzer" (MATTR, pronouns, burstiness) from "research-cited-but-qualitative" (positive-emotion). Otherwise the SKILL.md promises a wiring that can't exist.

2. **The chain reuses one model for both generation (voice-modes) and critique** — the precise condition that maximizes self-enhancement bias (1.2). → *Changes:* the chain-gate prompt must hard-separate the critic persona, and the design should say so explicitly as a named mitigation, not leave it implicit.

3. **"Fewer personal pronouns" may be actively wrong-signed for Sean's voice.** His calibrated modes (Domestic Observer, Gonzo, Beat Flow, first-person Substack) are pronoun-heavy by design. An absolute "low pronouns = AI" check risks flagging his *most* characteristic prose. → *Changes:* make pronoun-rate strictly baseline-relative (deviation from Sean's corpus), never absolute — and possibly demote it to a community/heuristic tier.

4. **Burstiness is the best measurable tell and the spec buries it** under generic "sentence variety" prose-dimension language while elevating three weaker named signals. → *Changes:* promote sentence-length CV/burstiness to a first-class measurable signal in both analyze.py output and the ai-tells.md measurable tier (strongest 1.1 + 2.3 upgrade combined).

5. **The eval `flags_ai_flatness_with_analyzer` will encode whatever threshold you pick** — if it bakes in "stdev < 4," it locks a weak threshold into the sealed evals. → *Changes:* write that eval against the CV metric (or a baseline-relative deviation), not the absolute stdev, so the sealed eval doesn't ossify the wrong constant.

6. **MATTR's window-sensitivity belongs in the regeneration docs.** If a future voice-samples round changes corpus length, MATTR@50 stays comparable, but anyone tempted to "tune the window" would silently break baseline comparability. → *Changes:* add a one-line "window is locked at 50; do not tune" note to the baseline regeneration section.

---

# What changes in the spec — concrete edits

**`ai-tells.md` evidence upgrade (the Tier-1 heart of the change):**
1. Rename the top tier from "Research-backed measurable" to two honest buckets: **(a) Measurable + baseline-relative** (lexical variability via MATTR; pronoun rate; **burstiness / sentence-length CV**) and **(b) Research-cited, qualitative** (positive-emotion skew — note: *not* analyzer-measurable).
2. **Re-ground the citations**: keep **Kobak** but for its real claim (word-frequency fingerprint, genre/model-bound — which supports the slop-list bullet, not the diversity bullet); **move RAID and Ghostbuster out of "support" into a "detection caution" note**; **add real lexical-diversity citations** (arXiv:2509.18880; SSRN 5833302) for signal #1 **with its comparison-class caveat** (lower vs polished prose, higher vs L2). Do **not** re-import upstream's unverified BEA/Nature HSSCOMMS cites.
3. **Reword the slop-list bullet** to the recommended phrasing in 1.1 (drop "near-random" and "for Claude specifically"; keep the model/genre-transfer argument). Note explicitly this is a deliberate divergence from upstream's verbatim line.
4. **Promote burstiness** as the best-supported measurable signal (cite arXiv:2603.23219).
5. Keep the em-dash bullet as the owned taste choice (already decided — unchanged).

**`analyze.py`:**
6. Keep **MATTR@50** (window locked at 50); **add MTLD-Original (0.72)** as deterministic stdlib fallback for `tokens < ~60`; do not pursue HD-D/vocd-D.
7. **Replace the "stdev < 4 = monotonous" default with CV = σ/μ, flag < ~0.45**; guard single-sentence div-by-zero; keep advisory. (Costs no fidelity — upstream has no threshold at all.)
8. Faithful-port notes: upstream uses `pstdev` (population) — match it or document the change; the upstream `window_size=5` arg is the *repetition paragraph window*, not the MATTR token window — keep them distinct.

**`finding-rubric.md` (prompt design):**
9. Add **structural anti-sycophancy scaffolding**: hard persona separation ("you did not write this"), per-finding grounding (quote + concrete reader cost), and a **severity-ranked floor with explicit license to report fewer issues** — *not* a forced finding count. Cap/forbid the praise section.

**Chain / SKILL.md:**
10. State persona separation as a **named mitigation** for the same-model generate-then-critique path.
11. Frame the single revise pass as **"revise against [specific finding]" routed through voice-modes** (grounded), and state that any second pass would require new external input — encoding the 3.5 finding.

**evals:**
12. Write `flags_ai_flatness_with_analyzer` against the **CV / baseline-relative** signal, not the absolute stdev, so the sealed eval doesn't lock in a weak constant.

---

# Sources

**Detection science / stylometry**
- Kobak et al., *Delving into LLM-assisted writing… excess vocabulary* — https://arxiv.org/abs/2406.07016 · https://doi.org/10.1126/sciadv.adt3813
- Dugan et al., *RAID* (ACL 2024) — https://aclanthology.org/2024.acl-long.674/ · https://arxiv.org/abs/2405.07940
- Verma et al., *Ghostbuster* (NAACL 2024) — https://aclanthology.org/2024.naacl-long.95/ · https://arxiv.org/abs/2305.15047
- Shaib et al., *Measuring AI Slop in Text* (2025) — https://arxiv.org/abs/2509.19163
- *Diversity Boosts AI-Generated Text Detection* (2025) — https://arxiv.org/abs/2509.18880
- *MATTR under length variation* (2025) — https://arxiv.org/html/2507.15092v1
- *Decoding AI Authorship* (2026 / 2024) — https://arxiv.org/abs/2603.23219 · https://arxiv.org/abs/2408.00769
- *Better Call Claude* (2025) — https://arxiv.org/abs/2508.00680
- TTR human vs AI (55.3 vs 45.5) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5833302
- ChatGPT higher diversity vs L2 writers — https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1616935/full · https://www.sciencedirect.com/science/article/pii/S2666827024000781
- Stylometry detects AI (Japanese, 7 LLMs) — https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369

**Sycophancy / self-review / LLM-as-judge**
- Sharma et al., *Towards Understanding Sycophancy* (ICLR 2024) — https://arxiv.org/abs/2310.13548 · https://www.anthropic.com/research/towards-understanding-sycophancy-in-language-models
- Huang et al., *LLMs Cannot Self-Correct Reasoning Yet* (ICLR 2024) — https://arxiv.org/abs/2310.01798
- Madaan et al., *Self-Refine* (NeurIPS 2023) — https://arxiv.org/abs/2303.17651 · https://selfrefine.info/
- Zheng et al., *MT-Bench / LLM-as-a-Judge* (NeurIPS 2023) — https://arxiv.org/abs/2306.05685
- *Justice or Prejudice?* (judge biases) — https://arxiv.org/html/2410.02736v1
- *Pride and Prejudice: LLM Amplifies Self-Bias in Self-Refinement* — https://arxiv.org/abs/2402.11436
- OpenAI, *Sycophancy in GPT-4o* — https://openai.com/index/sycophancy-in-gpt-4o/ · https://openai.com/index/expanding-on-sycophancy/
- Evidently AI, LLM-as-a-judge guide — https://www.evidentlyai.com/llm-guide/llm-as-a-judge

**Lexical diversity metrics + burstiness**
- McCarthy & Jarvis 2010 (MTLD/vocd-D/HD-D validation) — https://link.springer.com/article/10.3758/BRM.42.2.381
- Covington & McFall 2010 (MATTR) — https://www.tandfonline.com/doi/abs/10.1080/09296171003643098
- Bestgen 2024, *The Twofold Length Problem* (MATTR window sensitivity) — https://arxiv.org/abs/2307.04626
- Zenker & Kyle 2021 (minimum text lengths) — https://www.sciencedirect.com/science/article/abs/pii/S1075293520300660
- TAALED (MATTR 50-word default) — https://lcr-ads-lab.github.io/TAALED/
- GPTZero, burstiness/perplexity — https://gptzero.me/news/perplexity-and-burstiness-what-is-it/

**Iterative-revision degradation**
- Verbalized Sampling / RLHF mode collapse — https://arxiv.org/html/2510.01171v3
- Doshi & Hauser (homogenization in writing) — https://www.sciencedirect.com/science/article/pii/S294988212500091X
- Shumailov et al., *model collapse* (Nature 2024; analogy only) — https://arxiv.org/abs/2410.12954

**Upstream source (read live, `haowjy/creative-writing-skills@main`)**
- prose-critique SKILL.md — https://raw.githubusercontent.com/haowjy/creative-writing-skills/main/skills/prose-critique/SKILL.md
- analyze.py — https://raw.githubusercontent.com/haowjy/creative-writing-skills/main/skills/prose-critique/resources/analyze.py
- antipatterns.md — https://raw.githubusercontent.com/haowjy/creative-writing-skills/main/skills/prose-critique/resources/antipatterns.md
- baseline.md — https://raw.githubusercontent.com/haowjy/creative-writing-skills/main/skills/prose-critique/resources/baseline.md

**Confidence notes:** the three big-three papers and the upstream source were verified at primary sources. MT-Bench bias *magnitudes* and a few 2026 arXiv items (2603.23219, and the freshness-sweep secondaries) come from search-surfaced summaries — directions are firm, treat exact figures as approximate. "Forcing N findings causes fabrication" is practitioner-reasoned + supported by analogy to the fabrication literature, not an A/B study of critique prompts — the weakest-evidenced (but most consequential) claim here.
