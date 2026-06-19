# Agent Fleet — Architecture Brainstorm v2

**Date:** 2026-05-26
**Supersedes:** [`docs/2026-05-25-agent-fleet-brainstorm.md`](2026-05-25-agent-fleet-brainstorm.md) (v1, REVISION PENDING). v1's 18-idea ideation pass and converged top-5 remain valid as historical context; v2 lands the corrections from Sean's 2026-05-26 review pass and the empirical findings from three commissioned research outputs.
**Grounded in:**
- [`docs/research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md`](../../research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md) — cross-source synthesis of three independent research outputs (Gemini DR Max, Perplexity DR, LLM Council premium-profile with Opus 4.7 chairman). Read this first; v2 lands its decisions.
- [`docs/Image-Model-DR-2026/SYNTHESIS.md`](../../Image-Model-DR-2026/SYNTHESIS.md) — Phase 5 image-model router source.
- [`docs/pipeline-architecture-v1.md`](../../architecture/pipeline-architecture-v1.md) — 10-phase architecture (unchanged).
- [`PHILOSOPHY.md`](../../../PHILOSOPHY.md) — load-bearing intent (unchanged).
**Status:** LOCKED. v2 is the agent-fleet decision artifact. Implementation lands via [`docs/2026-05-26-agent-fleet-implementation-prompt-v2.md`](2026-05-26-agent-fleet-implementation-prompt-v2.md). Three split decisions reserved for empirical bake-off; everything else is decided.

---

## 1. What v2 changes from v1

Five corrections from Sean's 2026-05-26 review pass, ratified by the cross-source synthesis:

1. **Claude Agent SDK IS subscription-absorbed** on Sean's Anthropic plan. v1's "cap T3 at two voices for $0-incremental" rationale is wrong. T3 grows to three peers (Codie + Annie + Sage) plus a separate **Opus 4.7 chairman** synthesis call. All four subscription-absorbed.
2. **Best models on pinnacle phases.** Re-tier from v1's conservative cost ceilings. The synthesis converged on Opus 4.7 in five distinct roles, not just the chairman: Planner (Phase 0), Character Designer (Phase 2), Scriptwriter (Phase 3), T3 Sage peer, T3 Chairman.
3. **Character Designer (Phase 2) is the headline finding.** Three of four LLM Council voices + both DR outputs identified Cy as the *most under-recognized* Opus seat — *not* the third T3 voice. v1 had Cy on NB2 with no model awareness for the Bible authoring itself. v2 makes Cy = Opus 4.7 authors the Bible's identity rules + Gemini 3.1 Pro visually verifies generated turnarounds/expressions.
4. **Phase 3 Storyboard un-defers.** Two new personas: **Sam** (Scriptwriter, Opus 4.7 with screenwriting-modes skill) and **Bea** (Storyboard Artist, Sonnet 4.6 default with Opus escalation on script↔board conflict). v1 had Storyboard marked "deferred — Sean mostly authors"; the synthesis confirms this is a brainstorm-pattern collab role.
5. **Phase 5 Generate is a routed pipeline.** New persona **Flo** consults `manifest.yaml`'s `generation.routing:` block per [`docs/Image-Model-DR-2026/SYNTHESIS.md`](../../Image-Model-DR-2026/SYNTHESIS.md). Hero keyframes → NB Pro; standard keyframes → NB2/GPT-Image-2; cheap in-between edits → Seedream 4.0/SeedEdit 3.0; mid in-betweens → Qwen-Image-Edit-2511 on fal.ai; self-hosted → FLUX.1 Kontext [dev] + char LoRA + Shakker sketch LoRA + PuLID. v1 was single-model assumption.

The 10-phase architecture lock from 2026-05-24 is untouched. v2 changes *who fills which slot*, not the shape.

---

## 2. The Five Things That Change the Plan

Restated from the synthesis §1 because they earn the headline space. Each is supported by independent agreement across at least two of three research outputs.

### 2.1 The Character Designer is the missed pinnacle phase

The cost-ceiling correction's biggest unlock is upstream of T3. The Bible is the cross-phase invariant; every one of Phase 5's 10–50 vision critiques is implicitly evaluating against it. A Sonnet-authored Bible looks complete and silently fails to constrain — turnarounds won't actually pin the front pose, the expression sheet will blur tonally. *Validators cannot recover taste that was absent at generation time.*

**v2 lock:** Cy = Opus 4.7 authors the Bible (anchor, turnarounds, expressions, costumes, identity-drift triggers, palette, proportion rules) + Gemini 3.1 Pro visually verifies generated assets against it. NB Pro produces the actual images per the Phase 5 routing table.

### 2.2 Architectural diversity at the highest-frequency interaction

The orchestrator and the T2 vision critic together hold the per-frame Generate checkpoint — the busiest interaction in the fleet, 10–50 calls per piece. If both are Claude, correlated blind spots: the orchestrator's "valid output" aligns with the critic's "acceptable frame," and silent failures slip through.

**v2 lock:** Sonnet orchestrator + Gemini T2 critic. Different model families at the highest-frequency interaction by construction.

### 2.3 Planner and Chairman share a rubric, not a call

Planner emits an immutable `acceptance_criteria.json` at Phase 0. T2 and T3 critics cite criteria IDs when blocking. Chairman resolves disputes against those criteria. Museum Writer narrates changes in their terms. This prevents the local-optimization-drift failure mode where every phase ships "better" output that no longer matches the approved brief.

**v2 lock:** Phase 0 planner output schema includes `acceptance_criteria: [...]` with stable IDs. All critic outputs include `cites_criteria: [id, id, ...]`. Manifest schema grows a `criteria_locked: true` flag post-approval.

### 2.4 T3 is three peers from three vendors plus a distinct chairman call

Heterogeneous beats homogeneous. Three orthogonal error surfaces (production / visual / narrative), each from a different vendor, with a separate Opus 4.7 chairman that synthesizes consensus + dissent without becoming a fourth peer. Promoted-peer chairmen suffer self-favoring bias.

**v2 lock:** Codie (gpt-5.5 / Codex CLI) + Annie (Gemini 3.1 Pro / Anti-Gravity CLI) + Sage (Opus 4.7 / Claude SDK) as peers; separate Opus 4.7 call for chairman. Four model calls per gate, all subscription-absorbed.

### 2.5 Cheap judges fail in named ways; the defenses are documented

Sycophancy at 58.19% base rate ([SycEval](https://arxiv.org/html/2502.08177v2)). Self-preference bias up to +90% ([Chen et al. 2024](https://arxiv.org/abs/2410.02736)). Length bias, position bias, miscalibrated confidence, normalized style drift, false-positive pass-throughs on style-conforming-but-quality-deficient output. The architectural defenses are concrete: cross-provider ensemble, task-specific criteria injection (+3pp at zero cost), ensemble scoring (+9.8pp), pairwise tournament for relative-quality signal.

**v2 lock:** T3 stack ships with all defenses by construction — cross-provider ensemble (3 vendors), criteria injection (the planner's `acceptance_criteria.json`), separate chairman synthesis (not promoted peer), `proposed_patches:` staged-not-auto-applied.

---

## 3. The Persona Roster

Each phase that runs an agent gets a named persona. Personas are decorative if you strip them and load-bearing if you keep them — the role-shapes survive a name change but the credits-roll vibe is a real museum artifact.

| Phase | Persona | Role | Model | Why |
|-------|---------|------|-------|-----|
| 0 — Brief & Plan | **Maya** | Line producer | Opus 4.7 → Sonnet 4.6 validation → human gate | Compounding-error phase; cost-estimation accuracy matters; emits `acceptance_criteria.json` |
| 2 — Character Bible | **Cy** | Character designer | Opus 4.7 authors + Gemini 3.1 Pro visually verifies + NB Pro generates | Bible is cross-phase invariant; the missed pinnacle phase |
| 3 — Storyboard / Script | **Sam** | Scriptwriter | Opus 4.7 with screenwriting-modes skill | Stylistic-mechanism modeling, not surface pastiche |
| 3 — Storyboard / Script | **Bea** | Storyboard artist | Sonnet 4.6 default, Opus 4.7 escalation on script↔board conflict | Iterative brainstorm-loop latency matters; lowest-confidence assignment (65%), bake-off candidate |
| 5 — Generate | **Flo** | Frame generator | Model router per `manifest.yaml` `generation.routing:` — see §4 | NB Pro / NB2 / GPT-Image-2 / Seedream / Qwen-IE / FLUX+LoRA depending on shot tier |
| 5 — Per-frame T2 gate | **Em** | Script supervisor (vision critic) | Gemini 3.1 Pro (Anti-Gravity CLI) default, Opus 4.7 escalation on borderline / high-impact | Native multimodal grounding on 2D animation failure modes; architectural-diversity partner for Sonnet orchestrator |
| 6 — Motion T2 gate | **Em** | Same as Phase 5 | Same | Same critic, different artifact type |
| 4 → 5 — Animatic T3 gate | **Codie + Annie + Sage** | Production / visual / narrative peer critics | gpt-5.5 (Codex CLI) + Gemini 3.1 Pro (Anti-Gravity CLI) + Opus 4.7 (Claude SDK) | Heterogeneous T3 peers |
| 4 → 5 — Animatic T3 gate | **(Chairman)** | Synthesis | Opus 4.7 (Claude SDK), fixed | Distinct fourth call; no peer rotation |
| 8 — Assemble T2 gate | **Em** | Same as Phase 5 | Same | Loop coherence + pacing across the whole cut |
| pre-Museum T3 gate | **Codie + Annie + Sage + (Chairman)** | Same as Animatic T3 | Same | Public-facing artifact gets multi-CLI variance read |
| Museum (orthogonal) | **Mo** | Museum writer | Sonnet 4.6 live, optional Opus 4.7 final polish | Fluent expository on already-structured input — competent docent, not poet |
| Orchestrator (cross-phase) | (no persona) | DAG state, routing, retry ladder | Sonnet 4.6 (Claude SDK) default, Opus 4.7 escalation hatch for state conflicts | Instruction-following + JSON discipline + latency wins over deep reasoning |

Seven personas (Maya, Cy, Sam, Bea, Flo, Em, Mo) + two T3 council collectives (Codie/Annie/Sage + Chairman). One orchestrator without a persona. Sean is the conductor.

---

## 4. Phase 5 Generation Routing (Flo)

Per [`docs/Image-Model-DR-2026/SYNTHESIS.md`](../../Image-Model-DR-2026/SYNTHESIS.md) §2 + §5. Flo consults `manifest.yaml`'s new `generation.routing:` block per shot, with the routing table tagged by shot type.

| Shot type | Model | Cost/frame | When |
|-----------|-------|-----------:|------|
| Hero keyframe (portfolio) | **Nano Banana Pro** (NB Pro) | ~$0.15 | Phase 5 keyframes that ship as portfolio anchors |
| Standard keyframe | **NB2** or **GPT-Image-2** | ~$0.07 | Phase 5 keyframes that anchor downstream Seedance shots |
| In-between (cheap edit) | **Seedream 4.0 / SeedEdit 3.0** on fal.ai | $0.007–0.03 | Routine in-between cleanups (80% cost cut vs NB2) |
| In-between (mid quality) | **Qwen-Image-Edit-2511** on fal.ai | $0.021 | When Seedream slicks the pencil aesthetic |
| In-between (self-hosted, 24GB) | **FLUX.1 Kontext [dev] FP8** + character LoRA + Shakker sketch LoRA + PuLID-FLUX | $0 marginal after training | Steady-state production once Sean ships a custom LoRA |
| Mask-precise edit | **GPT-Image-2 `/images/edits`** | ~$0.21 | Targeted region work where Seedream's instruction-edit isn't precise enough |
| Aesthetic propagation | **EbSynth 2.0** | $0 | Boiling-grain fix; propagate hero pencil look across generative motion frames |

Maya's Phase 0 cost preview reads this routing table to compute the run's accurate generation budget. Flo's per-frame escalation ladder (Seedream → Qwen-IE → NB Pro) is configured per shot tier in the manifest. The pencil-aesthetic risk layer (style-lock LoRA always, aggressive negative prompting, Qwen denoise 0.78–0.82, EbSynth propagation) lives in Flo's standing-context preamble.

---

## 5. Three Structural Patterns to Adopt Regardless of Bake-Off Outcomes

These show up across all three research outputs. They're load-bearing.

**Pattern A — Architectural diversity at the highest-frequency interaction.** Orchestrator (Sonnet) and T2 critic (Gemini) come from different model families. Correlated blind spots are the most dangerous failure mode at scale. Validated in v2's assignment by construction.

**Pattern B — Planner-Chairman shared rubric, distinct calls.** `acceptance_criteria.json` is the structural fix for local-optimization drift. Planner emits it; T2 and T3 critics cite it by ID when blocking; Chairman resolves against it; Museum Writer narrates in its terms. Manifest schema grows `criteria_locked: true` post-approval.

**Pattern C — Chairman is a distinct fourth call, not a promoted peer.** Promoted-peer chairmen suffer self-favoring bias when synthesizing critiques that include their own. Stable Opus chairman. Periodic shadow-chair bake-off for calibration (not rotation).

---

## 6. Per-Role Recommendation Table (Locked + Open)

From the synthesis chairman, restated with v2's full persona context. Confidence reflects cross-source agreement.

| Role | Persona | Model | Confidence | Status |
|------|---------|-------|-----------:|--------|
| Orchestrator | — | Sonnet 4.6, Opus escalation hatch | 80% | **Locked** with bake-off (Open Q1) |
| Phase 0 Planner | Maya | Opus 4.7 → Sonnet 4.6 validation → human gate | 90% | **Locked** |
| Phase 2 Character Designer | Cy | Opus 4.7 lead + Gemini 3.1 Pro visual verify + NB Pro generate | 92% | **Locked** |
| Phase 3 Scriptwriter | Sam | Opus 4.7 with screenwriting-modes skill | 90% | **Locked** |
| Phase 3 Storyboard Artist | Bea | Sonnet 4.6 default, Opus escalation on conflict | 65% | **Locked** with bake-off (Open Q3) |
| Phase 5 Generator | Flo | Model router per §4 | n/a (routing decision, not model decision) | **Locked** |
| T2 Vision Critic (5, 6, 8) | Em | Gemini 3.1 Pro (Anti-Gravity), Opus escalation | 75% | **Locked** with bake-off (Open Q1 cont.) |
| T3 Peer — production | Codie | gpt-5.5 (Codex CLI) | 90% | **Locked** |
| T3 Peer — visual | Annie | Gemini 3.1 Pro (Anti-Gravity CLI) | 90% | **Locked** |
| T3 Peer — narrative | Sage | Opus 4.7 (Claude SDK) | 75% | **Locked** with bake-off (Open Q2) |
| T3 Chairman | — | Opus 4.7, fixed not rotated | 95% | **Locked** |
| Museum Writer | Mo | Sonnet 4.6, optional Opus polish | 92% | **Locked** |

---

## 7. Cost Ceiling v2

Subscription-absorbed across Claude SDK, Codex CLI, Anti-Gravity CLI. Baseline subscription cost ~$60/mo (Pro tiers across Anthropic + OpenAI + Google). Remaining spend lives in **image generation + Seedance + bake-off side costs**, not in the agent fleet runtime.

| Cost source | Estimate per piece | Notes |
|-------------|-------------------:|-------|
| Agent fleet runtime (all Claude/Codex/Anti-Gravity calls) | $0 incremental | Subscription-absorbed |
| Phase 2 Cy Bible authoring (NB Pro for full Bible) | ~$2–5 | Hero-grade Bible costs ~$0.15 × 20–30 generations |
| Phase 5 Flo generation (mixed routing) | $5–40 | Depends on hero/standard/in-between mix; dominant variable cost |
| Phase 6 Seedance motion | ~$10–20 | Fast tier default; Pro tier reserved per draft→pro |
| Phase 8 FFmpeg assembly | $0 | Pure local |
| **T2 bake-off (Gemini vs Sonnet vs Opus, 200-frame defect set)** | ~$5 | One-time per bake-off run |
| **Sage tier ablation (Opus vs Sonnet, held-constant chairman)** | $0 incremental | Subscription |
| **Storyboard three-way bake-off** | $0 incremental | Subscription |

Subscription rate-limit pressure is the real constraint, not dollar spend. Opus 4.7 has heavy latency (4× Sonnet on equivalent calls) and rate caps tighter on Anthropic Pro than Codex Plus or Google personal OAuth. v2's defaults reserve Opus for low-frequency, high-leverage roles (Planner once per piece, Chairman 3–5× per piece, Cy once per piece, Sam during script generation) to stay under rate ceilings.

---

## 8. Empirical Refinement Plan (Bake-Off Sequence)

Per the synthesis §6. Run after commits 4 / 8 / 9 land so the bake-offs run against shipped behavior. Each ablation lands its results under `evals/bakeoffs/2026-MM-DD-{ablation-name}/` per the existing pattern.

**Priority order (highest expected information gain first):**

1. **T2 critic shoot-out** — Gemini vs Sonnet vs Opus on a 200-frame defect set drawn from Act 1 + Act 2. Resolves the deepest cross-council split and the highest-frequency role. ~1 evening.
2. **Sage tier ablation** — Opus-Sage vs Sonnet-Sage with Opus chairman held constant. Measure dissent-map richness, chairman synthesis quality. ~1 evening.
3. **Planner downgrade ablation** — Opus → Sonnet after first short is planned. Measures whether the human gate absorbs the risk. ~3 pieces' worth of runs.
4. **Orchestrator drift test** — run Sonnet orchestrator for 20 pieces, measure restart rate against Grok-CM1's 19% claim on Sean's specific scaffolding (content-addressed cache + retry ladder).
5. **Storyboard three-way** — same 8-shot board, three configs (Sonnet vs Gemini vs Codex), blind Sean preference + revision count.

**Metrics across all bake-offs:** creator revision minutes, blind-preference scores, character consistency (CLIP + human), critic disagreement volume per phase, total wall time, `proposed_patches:` accept-rate, `acceptance_criteria.json` citation density.

Bake-off results fold into a future v2.1 brainstorm revision. No commits block on them.

---

## 9. Open Questions Reserved for Empirical Tests

Three split decisions stayed split across the synthesis sources. v2 ships with defaults but flags them for empirical refinement.

**Open Q1 — Orchestrator: Sonnet 4.6 default vs Opus 4.7 state-guardian.** Resolved by Bake-off 4 (Orchestrator drift test). Default is Sonnet with Opus escalation hatch. If restart rate exceeds 10% on Sean's specific scaffolding, promote to Opus state-guardian.

**Open Q2 — Sage tier at T3: Opus 4.7 vs Sonnet 4.6.** Resolved by Bake-off 2 (Sage tier ablation). Default is Opus. If chairman synthesis quality and dissent-map richness don't degrade with Sonnet-Sage, save Opus rate-limit budget by demoting.

**Open Q3 — Storyboard Artist: Sonnet vs Gemini vs Codex.** Resolved by Bake-off 5 (Storyboard three-way). Default is Sonnet with Opus escalation on conflict.

Three other open questions are kept from v1 because the synthesis doesn't bear on them:

**Open Q4 — Codex CLI + Anti-Gravity CLI multimodal input.** Verify both accept image/video input at anima's resolutions in commit 9's first hour. Pending until commits land.

**Open Q5 — `proposed_patches:` UX.** Stage-first by default; director's chair review surface comes later when the queue grows past one-screen.

**Open Q6 — Bibles authored vs consumed.** Cy as Project-Type for authoring lands later; consuming-only lands in commit 2.

---

## 10. What v2 Doesn't Change

To prevent scope creep, v2 explicitly does NOT alter these from v1 or from earlier locks:

- The 10-phase architecture lock (2026-05-24). Untouched.
- PHILOSOPHY.md's six load-bearing beliefs. Untouched.
- Animatic Phase 4 ingestion contract (Procreate Dreams + Procreate PNG sequences). Locked in v1.
- Manifest schema's six additive blocks from commit 1 (`phases:`, `tiering:`, `critics:`, `characters:`, `museum:`, `brief:`). Still additive; v2 adds two more blocks (`generation.routing:` for Flo, `acceptance_criteria:` for Maya's output schema).
- Museum capture's Astro content-collection publishing target (`sw-ai-pm-portfolio`).
- The pencil-test reference implementation (Act 2 Seedance work in flight). Continues unchanged on v1 manifest blocks.

---

## 11. Architecture Implied by v2 (Strawman)

The 10-phase architecture decorated with v2 personas + their models, locked.

```
Phase 0   BRIEF & PLAN       Maya (Opus 4.7 → Sonnet 4.6 validation) → human approval gate
                             emits acceptance_criteria.json
Phase 1   SCAFFOLD           orchestrator-only (Sonnet 4.6)
Phase 2   CHARACTER BIBLE    Cy (Opus 4.7 authors + Gemini 3.1 Pro visual verify + NB Pro generates)
Phase 3   STORYBOARD         Sam (Opus 4.7, screenwriting-modes) + Bea (Sonnet 4.6, Opus escalation)
                             brainstorm-pattern collab with Sean
Phase 4   ANIMATIC           Sean-authored shape-block (Procreate Dreams / PNG)
                             ⚖ T3 — Codie (gpt-5.5) + Annie (Gemini 3.1 Pro) + Sage (Opus 4.7) → Opus chairman
Phase 5   GENERATE           Flo (model router per generation.routing:)
                             ⚖ T1 rule gates + T2 — Em (Gemini 3.1 Pro, Opus escalation)
                             T2 outputs proposed_patches: into manifest.lock.yaml
Phase 6   MOTION             Seedance Fast → Pro
                             ⚖ T2 — Em reviews motion arc + identity drift in video
Phase 7   AUDIT              orchestrator consolidation; routes critic findings to retry ladder
Phase 8   ASSEMBLE           FFmpeg, comparison GIFs, museum hooks fire
                             ⚖ T2 — Em reviews loop coherence + pacing
Phase 9   QA REVIEW          human + creative-director skill

(parallel)  MUSEUM            Mo (Sonnet 4.6) drafts walkthrough as nodes complete
                              ⚖ T3 — Codie + Annie + Sage → Opus chairman before publish

(cross-phase)  ORCHESTRATOR  Sonnet 4.6 (Claude SDK), Opus 4.7 escalation hatch
                             holds DAG state, content-addressed cache, retry ladder,
                             criteria_locked enforcement, proposed_patches staging
```

Seven personas + two T3 council collectives + one orchestrator + one human (Sean). Eleven model assignments locked, three flagged for empirical refinement, zero re-decided after this artifact ships.

---

## 12. What's Next

Implementation handoff: [`docs/2026-05-26-agent-fleet-implementation-prompt-v2.md`](2026-05-26-agent-fleet-implementation-prompt-v2.md) — paste-ready continuation prompt for the next Claude Code session. Commits 4 → 8 → 9 implement against v2 assignments. Bake-offs commission post-v2.

The pressure-test session (kickoff Option A from the 2026-05-25 Cowork start) stays on the board for after commits 4 / 8 / 9 ship — doing it before is too early to find the interesting failure modes; doing it after means the critique lands against shipped behavior rather than schema-only intent.

---

*v2 lands the synthesis decisions. The fleet has names, contracts, cost ceilings, structural patterns, and empirical refinement targets. Implementation begins with commit 4.*
