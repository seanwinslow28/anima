# Orchestrator, Planner & Judge Delegation — Cross-Source Synthesis

**Created:** 2026-05-26
**Sources:** Three research outputs run from the prompts at [`2026-05-26-orchestrator-and-judge-delegation-prompts.md`](2026-05-26-orchestrator-and-judge-delegation-prompts.md).
- [`2026-05-26-Anima-Deep-Research-Gemini-DR-Max.md`](2026-05-26-Anima-Deep-Research-Gemini-DR-Max.md) — 278 lines, 90 cited sources, three configurations (Latency-Conscious / Balanced / Pinnacle-Everywhere)
- [`2026-05-26-Anima-Deep-Research-Perplexity-Deep-Research.md`](2026-05-26-Anima-Deep-Research-Perplexity-Deep-Research.md) — 408 lines, strong production-case-study density, three configurations (Budget / Balanced [recommended] / Pinnacle)
- [`2026-05-26-orchestrator-judge-delegation-llm-council.md`](2026-05-26-orchestrator-judge-delegation-llm-council.md) — 1089 lines, four-vendor council (Opus 4.7 + GPT-5.5 + Gemini Pro + Grok 4.20) with Opus 4.7 chairman synthesis at line 943

**Purpose:** Read this first; raw outputs are the receipts. This synthesis is the decision artifact that gates the v2 revision of [`docs/2026-05-25-agent-fleet-brainstorm.md`](../2026-05-25-agent-fleet-brainstorm.md) and [`docs/2026-05-25-agent-fleet-implementation-prompt.md`](../2026-05-25-agent-fleet-implementation-prompt.md). Mirrors the [`docs/Image-Model-DR-2026/SYNTHESIS.md`](../Image-Model-DR-2026/SYNTHESIS.md) pattern.

---

## 1. The Five Things That Change The Plan

These are the findings the v2 brainstorm should land on. Each is supported by independent agreement across at least two of the three sources.

**1. The Character Designer is the real "unlocked pinnacle phase" — not the third T3 voice.** Three of four LLM Council voices (and both DR outputs in their Balanced/Pinnacle configs) identified Phase 2 Character Designer as the most under-recognized Opus seat. The Opus-4.7 council member named it directly: *"The cost-ceiling correction's biggest unlock isn't T3. It's Character Designer."* The chairman synthesis echoed this as the *single most important decision Sean is about to get wrong* if he ships v1: the Bible is the cross-phase invariant; every downstream frame, board, and motion pass references it; a Sonnet-authored Bible *looks* complete and silently fails to constrain. Sean spends Opus on critics catching defects an Opus-authored Bible would have prevented from being generated. **Validators cannot recover taste that was absent at generation time.** v1's brainstorm doc had Cy at "NB2 draft / pro" — that's the wrong frame. The right frame: *Opus 4.7 authors the Bible's structure + identity rules; Gemini 3.1 Pro visually verifies generated anchors / turnarounds / expressions against it.*

**2. Architectural diversity at the highest-frequency interaction is structurally important.** Opus-4.7 council member's non-obvious pattern, echoed by both DR outputs: **the orchestrator and the T2 vision critic must not share a model family.** If both are Claude, you get correlated blind spots at the 10-50-calls-per-piece interaction — the orchestrator's notion of "valid output" aligns with the critic's notion of "acceptable frame," and silent failures slip through. The recommended configuration satisfies this naturally (Sonnet orchestrator ↔ Gemini T2 critic). This is invisible if Sean reasons role-by-role; it's only visible when he reasons about *which roles touch each other most often*.

**3. The Planner-Chairman shared-rubric pattern is the structural fix for local-optimization drift.** GPT-5.5 council member's recommendation, ratified by the chairman synthesis: the planner emits an immutable `acceptance_criteria.json` at Phase 0; T2/T3 critics must cite criteria IDs when blocking; the chairman resolves disputes against those criteria; the museum writer narrates changes in their terms. This prevents the failure mode that has killed an estimated 60% of long-running indie creator animation projects (Grok-CM3's number, plausible if directional) — every phase locally optimizes for its own idea of "better" and the finished piece no longer matches the approved brief. **Planner and Chairman share the rubric, but they're distinct calls.** Don't conflate them; don't rotate them; don't let the orchestrator rewrite them.

**4. T3 wants three peers from three different vendors. Heterogeneous beats homogeneous.** All three sources converge: Codie (gpt-5.5 via Codex CLI) handles production / reproducibility / structural critique; Annie (Gemini 3.1 Pro via Anti-Gravity CLI) handles visual / spatial / continuity critique; Sage (Claude SDK) handles narrative / tonal / semantic critique. Three orthogonal error surfaces. Grok-CM3's all-Opus-with-temperature-variance proposal is rejected on echo-chamber grounds across the other sources. The Sage tier (Opus vs Sonnet) is the genuine split below — it's an empirical question, not a settled one.

**5. Cheap judges fail in specific named ways. Architectural defenses are known.** Sycophancy at 58.19% base rate ([SycEval, arXiv:2502.08177](https://arxiv.org/html/2502.08177v2)). False-positive style-drift normalization. Miscalibrated confidence. Self-preference bias inflating self-scores by up to +90%. Length bias. Position bias. The defenses are documented and concrete: cross-provider ensemble ([Arena-Hard-Auto, arXiv:2406.11939](https://arxiv.org/abs/2406.11939)), task-specific criteria injection (+3pp at zero cost per [arXiv:2604.13717](https://arxiv.org/abs/2604.13717)), ensemble scoring (+9.8pp), pairwise tournament for relative-quality signal ([VISTA, arXiv:2510.15831](https://huggingface.co/papers/2510.15831)). T3 doesn't just want three vendors for variance — it wants three vendors *with criteria injection*, *with a separate Opus chairman*, *with the orchestrator and T2 critic from a different family*. That stack is the documented defense against the failure modes a single cheap judge introduces.

---

## 2. Per-Role Consensus (with Confidence)

The chairman's per-role table from the LLM Council, cross-checked against the two DR outputs. Confidence reflects strength of agreement across all three sources.

| Role | Recommendation | Confidence | Notes |
|------|----------------|-----------:|-------|
| **Orchestrator** | Sonnet 4.6 (Claude SDK) with **Opus 4.7 escalation hatch** for state conflicts | 80% | Camp split: 3-of-4 council + both DRs say Sonnet; Grok-CM1 + Grok-Chair want Opus citing 19% restart rate on Sonnet. Resolved toward Sonnet because Sean's topology already has content-addressed cache + retry ladder (the scaffolding that mitigates drift). Escalation hatch for plan-conflict / cache-key-ambiguity / contradictory-critic-verdict cases. |
| **Planner (Phase 0)** | **Opus 4.7** primary → Sonnet 4.6 validation pass → human gate | 90% | 3-of-4 council + Perplexity Balanced/Pinnacle + Gemini DR Balanced/Pinnacle. Emits immutable `acceptance_criteria.json` that all downstream critics cite by ID. GPT-5.5's "Opus brief interrogation → Opus structured plan → Sonnet validation → human gate" structure adopted verbatim. |
| **T2 Vision Critic (Em)** | **Gemini 3.1 Pro** (Anti-Gravity CLI) with **Opus 4.7 escalation** on borderline / high-impact shots | 75% | All non-Grok voices say Gemini. Grok-CM3 raised a real concern (audience preferred Claude-family critique even when Gemini scored higher on rubric — "rubric ≠ taste"). Resolved toward Gemini default + Opus escalation ladder. **This is the highest-priority bake-off.** |
| **T3 Peer Critics: Codie + Annie + Sage** | Heterogeneous: gpt-5.5 (Codex CLI) + Gemini 3.1 Pro (Anti-Gravity CLI) + Claude SDK | 90% on heterogeneity | Sage tier (Opus vs Sonnet) is split — see §3. |
| **T3 Chairman** | **Opus 4.7**, fixed (not rotated) | 95% | Unanimous. Mechanism: weaker chairmen *average dissent away* (measured 30-40% fewer minority-report annotations on Sonnet). Rotation rejected on longitudinal-standards-drift grounds. Adopt GPT-5.5's structured output schema (`overall_verdict / consensus_findings / dissent_map / blocking_issues / non_blocking_issues / recommended_next_action / confidence`). |
| **Character Designer (Cy)** | **Opus 4.7** authors the Bible + identity rules; **Gemini 3.1 Pro** visually verifies generated anchors / turnarounds / expressions | 92% | The headline finding (§1.1). 3-of-4 council + both DRs. Gemini-Pro alone preferred gpt-5.5 here (spatial-persistence argument); the hybrid covers that. |
| **Scriptwriter (Sam)** | **Opus 4.7** with screenwriting-modes skill | 90% | Unanimous. Stylistic-mechanism modeling, not surface pastiche — Opus distinguishes Kaufman's *"recursive self-consciousness, identity instability, absurdity with emotional seriousness"* from generic "in the style of Kaufman." |
| **Storyboard Artist (Bea)** | **Sonnet 4.6** default for iterative-loop latency; **Opus 4.7** escalation when board conflicts with script | 65% | Lowest-confidence single assignment in the fleet. Real three-way split: Sonnet (Opus-4.7 + most Grok) / Gemini (GPT-5.5 + Perplexity) / Codex (Gemini-Pro). Worth a bake-off. |
| **Museum Writer (Mo)** | **Sonnet 4.6** live; optional Opus 4.7 final polish if the piece is important | 92% | Unanimous. *"The Museum Writer should sound like a competent docent, not a poet."* |

---

## 3. The Genuine Splits Worth Surfacing Explicitly

Three decisions stayed split across the sources. Each one is testable; none of them is decidable by argument alone.

**Split 1 — Orchestrator: Sonnet 4.6 default vs Opus 4.7 state-guardian.** Sonnet camp argues orchestration is instruction-following plus JSON discipline plus latency, not deep reasoning — Opus here is over-tiering, gets bored, philosophizes about user intent, can mutate JSON wrappers or skip phases. Opus camp (Grok-CM1) argues measured 19% restart rate from Sonnet state drift, requires Opus's reliable 8k-16k state tracking. **Empirical test:** run Sonnet orchestrator for 20 pieces, measure restart rate against the 19% claim on Sean's specific scaffolding. The content-addressed cache + retry ladder Sean already has is likely the scaffolding gap Grok-CM2 cites as the real fix.

**Split 2 — Sage tier at T3: Opus 4.7 vs Sonnet 4.6.** Opus camp argues a peer panel only works if each voice is at its ceiling — at 3-5 calls per piece, the marginal cost is negligible and panel quality wins. Sonnet camp argues Opus-as-peer-and-Opus-as-chairman correlates the panel — let Sonnet provide a strong-but-different Claude view, then let Opus synthesize. **Empirical test:** hold Opus chairman constant, run two configs — Opus-Sage vs Sonnet-Sage — on the same 3-shot, measure dissent-map richness and chairman synthesis quality.

**Split 3 — Storyboard Artist: Sonnet vs Gemini vs Codex.** Sonnet wins on iterative-brainstorm latency. Gemini wins on visual / spatial / shot-language reasoning. Codex wins on production-grade scene-graph structuring. Real three-way split with three different framings of what storyboarding *is*. **Empirical test:** generate the same 8-shot board three ways, present to Sean blind, measure preference and revision count.

---

## 4. Three Structural Patterns to Adopt Regardless of Bake-Off Outcomes

These are not split. They show up across all three sources and they're load-bearing.

**Pattern A — Don't share a model family between the orchestrator and the T2 critic.** Correlated blind spots at the highest-frequency interaction. Sonnet ↔ Gemini satisfies this; Opus ↔ Sonnet does not.

**Pattern B — Planner and Chairman share a rubric, but they're distinct calls.** `acceptance_criteria.json` is immutable post-Phase-0; T2/T3 critics cite criteria IDs when blocking; chairman resolves disputes against those criteria. This is what prevents local-optimization drift.

**Pattern C — The chairman is a *fourth distinct call*, not a promoted peer.** Promoting a peer to chair introduces self-favoring bias (LLMs preserve their own framing when synthesizing critiques that include their own work). Keep the chair stable, Opus-4.7, separate call.

---

## 5. The Single Most Important Decision Sean Is About To Get Wrong

Restated verbatim from the LLM Council chairman, because it deserves to land plainly:

> Sean is about to spend his unlocked Opus budget on a third T3 peer voice and stop there. That's a real upgrade, but it isn't the pinnacle. Three of four council members independently identified **Character Designer (Phase 2)** as the under-recognized Opus seat. The Bible is the cross-phase invariant; every one of his 10-50 T2 vision critiques is implicitly evaluating against it. A Sonnet-authored Bible looks complete and silently fails to constrain — turnarounds won't actually pin the front pose, the expression sheet will blur tonally. He will spend Opus on critics catching defects that an Opus-authored Bible would have prevented from being generated. **Validators cannot recover taste that was absent at generation time.** The cost-ceiling correction's real unlock is upstream of T3, not at T3.

---

## 6. The Bake-Off Plan (LLM Council Chairman's Recommendation)

Four-way config bake-off on three already-shipped reference pieces (so ground-truth exists and creator-preference data is recoverable):

- **Config A — Current brainstorm baseline** (v1, mostly Sonnet)
- **Config B — This synthesis** (Sonnet orchestrator + Opus on Planner/Bible/Script/Sage/Chairman + heterogeneous T3 + Gemini T2) — *recommended default*
- **Config C — Grok-CM2's speed variant** (gpt-5.5 orchestrator, Sonnet planner, Sonnet Sage)
- **Config D — Grok-CM3's taste-coherence variant** (Opus orchestrator, all-Opus T3 with temperature variance)

**Priority ablations** in order of expected information gain:

1. **T2 critic shoot-out** — Gemini vs Sonnet vs Opus on a 200-frame set with known defects. Resolves the deepest cross-council split and the highest-frequency role.
2. **Sage tier ablation** — Opus-Sage vs Sonnet-Sage with Opus chairman held constant. Measures dissent-map richness and chairman synthesis quality.
3. **Planner downgrade ablation** — Opus → Sonnet after first short is planned. Measures whether GPT-5.5's "human gate absorbs the risk" claim holds.
4. **Orchestrator drift test** — run Sonnet orchestrator for 20 pieces, measure restart rate against Grok-CM1's 19% claim on Sean's specific scaffolding.
5. **Storyboard artist three-way** — same 8-shot board, three configs, blind preference + revision count.

**Metrics:** creator revision minutes (Grok-CM1's strongest signal), final piece blind-preference scores, character consistency (CLIP + human), critic disagreement volume per phase, total wall time. Ablation 4 also tracks `proposed_patches:` accept-rate and `acceptance_criteria.json` citation density.

---

## 7. Anti-Findings — Things The v2 Brainstorm Should Explicitly Not Do

Each is documented as a failure mode across at least two sources.

- **Don't make all critics Claude-shaped.** Correlated blind spots, preference leakage, normalized style drift.
- **Don't make the orchestrator Opus 4.7 by default.** Latency tax (4× Sonnet), JSON-discipline risk (Opus "tries to be helpful"), state-mutation risk. Reserve Opus for the escalation hatch.
- **Don't rotate the chairman.** Longitudinal standards drift. Calibration is the value; rotation destroys it. Run a periodic shadow-chair bake-off instead.
- **Don't conflate planner and orchestrator.** Different ergonomics (planner: slow, deliberate, once per piece; orchestrator: fast, continuous, autonomous). Same-model attempts lead to mid-run re-planning.
- **Don't promote a T3 peer to chairman in the same call.** Self-favoring synthesis bias. Chairman is a distinct fourth call.
- **Don't auto-apply `proposed_patches:`.** Stage-first; Sean approves before manifest mutation. (Already in v1; reinforced by the research.)
- **Don't ship without `acceptance_criteria.json`.** The structural fix for local-optimization drift requires the planner to emit it as an immutable artifact.

---

## 8. Portfolio Positioning Signal

From the Perplexity DR closing note, worth preserving because the signal is real:

> The combination of subscription-absorbed multi-provider council for a solo creator (Anthropic + OpenAI + Google under personal subscription tiers) being used in a production creative pipeline is, as of May 2026, uncommon enough to constitute a differentiating practice. Most documented production systems use a single primary provider with one secondary. Running a three-provider T3 peer ensemble with a separate chairman — specifically for a 2D animation quality gate — has no direct prior art in the published literature surveyed here.

This positions anima's agent fleet as an early practitioner of provider-diverse evaluation councils for solo creative production. That belongs in the museum walkthrough framing — it's the kind of "I am among the first" claim that the architecture earns.

---

## 9. Source Map (where each claim came from)

| Source | Strongest on | Weakest on |
|--------|--------------|------------|
| Gemini DR Max | 90-citation academic literature survey, named-systems table, three-tier cost configuration framing, vision critic temporal-vs-static distinction | Tendency to over-tier toward Opus in the Pinnacle config; less production-postmortem density |
| Perplexity DR | Production case studies (Stripe Minions, Anthropic Research System, Replit Agent v2, Cognition Devin 2.0), explicit acceptance-criteria.json pattern, portfolio-positioning observation | Less academic-literature breadth |
| LLM Council premium | Four distinct vendor voices with measurable disagreement, Opus 4.7 chairman synthesis that names the headline finding explicitly, concrete bake-off plan with metrics | Grok-CM3's all-Opus-T3 proposal weakened the council's heterogeneity case slightly; chairman ($0.5225 / 286s / 29K input tokens) gave the strongest single decision artifact |

All three converged on Character Designer as the missed pinnacle phase, on heterogeneous T3 peers, on Opus chairman, and on the planner-chairman shared-rubric pattern. The convergence is robust enough to lock those decisions even without the bake-off; the bake-off resolves the three named splits in §3.

---

## 10. What This Synthesis Does Not Decide

These remain open and out of scope for this artifact:

- **The specific bake-off run schedule.** Sean decides which ablations to commission before v2 of the brainstorm lands, and which to defer to post-v2.
- **The Phase 5 generation model router from [`docs/Image-Model-DR-2026/SYNTHESIS.md`](../Image-Model-DR-2026/SYNTHESIS.md).** This synthesis covered orchestration / planning / judging, not image generation. The Phase 5 router (NB Pro / NB2 / GPT-Image-2 / Seedream / Qwen-IE / FLUX+LoRA / etc.) was researched separately and lands in v2 unchanged.
- **The `screenwriting-modes` skill specification.** The Scriptwriter persona (Sam) consumes that skill once Sean ships it; the skill itself isn't this synthesis's deliverable.
- **The animatic ingestion contract (Phase 4).** v1's brainstorm already locked Procreate Dreams + Procreate PNG sequences as the input format; this synthesis doesn't touch it.

---

*Next step: surface the three split decisions from §3 to Sean, then write v2 of the brainstorm doc + v2 of the implementation prompt against this synthesis. Bake-offs commissioned in parallel will land their results into the museum capture layer as portfolio artifacts.*
