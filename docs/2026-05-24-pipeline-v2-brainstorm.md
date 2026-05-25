# Pipeline v2 — Architecture Brainstorm

**Date:** 2026-05-24
**Skill:** `pm-product-discovery:brainstorm-ideas-existing`
**Scope:** Pipeline architecture only. Agent fleet, multimodal vault/RAG, and museum showcase format are scheduled for later sessions.
**Inputs:** Conversation framing from Sean (rebrand from `sw-portfolio-animation-pipeline` to a reusable human+AI 2D animation pipeline) + external research pass (Higgsfield Supercomputer, OiiOii, Krea Node Agent, Toon Boom / OpenToonz / Grease Pencil / Procreate Dreams, Code2Video / CAViAR / VISTA planner-worker-critic papers).

---

## 1. Opportunity Frame

Today's pipeline is a 6-phase manifest-driven flow optimized for one pencil-test character on cream paper:

```
Scaffold → Generate → Motion (Seedance) → Audit → Assemble → QA Review
```

It works. It shipped Act 1. It does not generalize, because:

- It assumes one anchor character. Multi-character shorts need a Character Bible primitive.
- It has no pre-production phase. Industry pipelines lock timing before frame generation (animatic); this one locks frame counts in YAML.
- It has no human-in-the-loop gate between manifest and compute. Cost surprises propagate.
- Every config change re-runs the whole chain. Iteration is expensive.
- It produces frames, not portfolio artifacts. The museum layer is bolted on after the fact.

The v2 question: **what does the pipeline shape look like when the project is "any 2D short film" instead of "this pencil test"?**

---

## 2. Ideation — Three Perspectives, 15 Ideas

### Product Manager perspective — business value, strategic alignment, customer impact

| # | Idea | One-line |
|---|------|----------|
| PM-1 | **Brief → Plan → Approval gate (Phase 0)** | Planner agent reads a brief, produces a human-readable plan + cost estimate before any model call. Higgsfield's defining pattern. |
| PM-2 | **Museum-mode auto-capture layer** | Every pipeline run auto-generates a public-ready walkthrough doc (prompt + reference + output + rationale per frame). Portfolio assets are a byproduct of production, not a separate task. |
| PM-3 | **Project-Type templates** | Manifest archetypes — "Character study" (turnarounds + variations), "Motion comparison" (manual ↔ AI side-by-side), "Short film" (full pre-pro through QA). User picks archetype, manifest scaffolds. |
| PM-4 | **Comparison-asset stage as first-class output** | Every shot ships 3 deliverables: polished frame, manual shape-block reference, comparison GIF. The portfolio's signature artifact format, produced inline. |
| PM-5 | **Decision ledger / "why" log** | Every approve/reject/retry writes a structured entry capturing rationale. Becomes the museum's narrative spine. `runs/` already half-does this; promote to first-class. |

### Product Designer perspective — UX/delight (Sean as user of his own tool)

| # | Idea | One-line |
|---|------|----------|
| DES-1 | **Animatic Phase (new Phase 0.5)** | Formal stage between storyboard and frame gen where Sean (or an agent) blocks timing with simple shapes/silhouettes. The "human sketches motion in shapes" thesis becomes a named gate, not a vibe. |
| DES-2 | **Character Bible as a project entity** | First-class folder for A-anchor + turnarounds + expression sheets + costume variants + canonical reference grid. Replaces `images/2D-Character-Sketch-Sean-v1.png` single-file pattern. |
| DES-3 | **Draft → Pro tier escalation as pipeline-wide state machine** | Every stage runs at draft tier first, Sean approves before committing full-fidelity. Already implicit in Seedance Fast→Pro; promote to pipeline-wide convention. |
| DES-4 | **Frame-level "trace overlay" debug mode** | `assemble.sh` ships a variant that renders the manual shape-block animatic semi-transparent under the AI output, frame-aligned. QA timing/arc fidelity in one playback. |
| DES-5 | **"Human moments" annotation system** | Manifest field on every stage: `human_authored: true / human_curated: true / ai_generated: true`. Surfaces in museum docs as colored badges. Kills the "is this all AI?" question by making the division visible. |

### Software Engineer perspective — technical possibilities, data leverage, scale

| # | Idea | One-line |
|---|------|----------|
| ENG-1 | **DAG refactor with content-hashed node caching** | Each pipeline stage is a typed transform. Hash inputs+config; cached node returns immediately; only downstream of an edit re-runs. Krea Node Agent pattern. Kills full-chain regen. |
| ENG-2 | **Planner agent emits manifest entries** | Claude reads a brief + storyboard, produces a draft `manifest.yaml` with phase plan, frame list, anchor refs, retry budget. Generalizes pipeline beyond hand-authored YAML. |
| ENG-3 | **Critic agent as a distinct pipeline role** | Vision-model critic reviews frames against beat description + style guide, proposes prompt diffs (not just pass/fail). Mirrors the code-brain vault-critic pattern (Codex + Anti-Gravity parallel critique, $0 incremental). |
| ENG-4 | **Manifest schema versioning + per-frame lock files** | Extend `manifest.lock.yaml`: every approved frame's section becomes immutable; manifest grows additively; re-runs from any historical lock are deterministic. |
| ENG-5 | **Content-addressed multimodal asset store** | Every approved asset filed as `{sha256}.png` + `{sha256}.json` sidecar (prompt, model, params, parents, critic notes). Foundation for the vault/RAG layer in a later session. |

---

## 3. Prioritized Top 5

Scored on: strategic alignment with the human+AI partnership thesis · impact on the "ship short films + serve as museum" outcome · feasibility (solo workflow, ~3 shorts/year) · differentiation from generic AI pipelines.

### **TOP-1 — Animatic Phase as a named pipeline stage** (from DES-1)

**Description:** Insert a formal Phase 0.5 between storyboard and frame generation. Sean blocks motion + timing with simple shapes/silhouettes (digitally, on paper, or in After Effects/Procreate Dreams); pipeline ingests the shape-block animatic as an artifact; downstream Seedance and Gemini stages reference it as a motion-and-timing constraint.

**Why selected:** This is the highest-differentiation move in the entire brainstorm. Every other AI animation pipeline starts at prompt-to-image or prompt-to-video. The animatic stage is where Sean's "human owns taste and timing" thesis becomes load-bearing instead of decorative. It's also a structural answer to the template trap — a generic AI pipeline doesn't have this stage because a generic AI pipeline doesn't have a human in the loop with skin in the game.

**Key assumptions to validate:**
- Sean will actually author animatics (it's not a chore that gets skipped under deadline).
- Shape-block animatics are usable as Seedance/NB2 motion conditioning (not just human reference). Test: feed a 2D-circle bouncing-ball animatic to Seedance with end-frame anchor, measure whether output respects the timing.
- The format spec (After Effects? Procreate Dreams? Pencil-test PNG sequence? animation-pipeline skill output?) is something Sean can live with weekly.

---

### **TOP-2 — Brief → Plan → Approval gate as Phase 0** (from PM-1)

**Description:** New Phase 0 sits in front of Scaffold. Planner agent (Claude) reads a brief.md (free-form: "I want a 12-second character intro of X doing Y in style Z"), proposes a structured plan: which phases run, how many frames, which anchors get loaded, draft Seedance/NB2 prompts, retry budget, **estimated model spend**. Sean approves (or edits) before any compute happens. The approved plan becomes the seed for the manifest.

**Why selected:** Three wins in one stage. (1) Generalizes the pipeline to any project — no more hand-authoring YAML from scratch. (2) Kills cost surprises (the Higgsfield pattern — humans hate paying for a thing they didn't sign off on). (3) Forces strategic alignment upfront — Sean argues with the agent's plan, surfaces wrong assumptions, locks intent before any frame ships. Low engineering effort (one new script + one prompt template) for a structural win.

**Key assumptions to validate:**
- A planner agent can produce a usable draft manifest from a brief, not a hallucinated one. Probably needs few-shot examples from the pencil-test manifest.
- Sean will actually edit/argue with the plan rather than rubber-stamp it. Approval UX matters — needs to surface diffs cleanly.
- Cost estimation across NB2 + Seedance + Claude is reliable enough to gate decisions (errors of ±30% are fine; ±300% defeats the purpose).

---

### **TOP-3 — Museum-mode auto-capture layer** (from PM-2, absorbs PM-4 + PM-5)

**Description:** Every approved frame, every Seedance generation, every retry decision writes structured artifacts into a parallel `museum/` tree: original prompt, references used, output, decision rationale, before/after if applicable, and a comparison GIF where a manual reference exists. A static site generator (or just markdown + a simple build script) renders `museum/` into a public walkthrough at the end of each run. The portfolio piece IS the pipeline's output, not a downstream task.

**Why selected:** This is the thesis-defining move for the rebrand. "Pipeline as portfolio" only works if portfolio content is a free byproduct, not a manual write-up. Absorbs PM-4 (comparison assets) and PM-5 (decision ledger) under one delivery system. Differentiates hard from every other AI animation tool — none of them ship a museum layer because none of them think of the *process* as the product.

**Key assumptions to validate:**
- The capture layer doesn't add meaningful friction to production (target: <5% overhead in wall-clock time per run).
- Static museum output is something Sean actually wants to publish (vs. private) — affects what gets captured and how candid the decision log can be.
- The comparison-GIF format (manual shape-block on left, AI output on right, synced) is technically straightforward via FFmpeg — likely yes, but worth a 30-min spike.

---

### **TOP-4 — DAG refactor with content-hashed node caching** (from ENG-1)

**Description:** Refactor `pipeline/generate.py` + `audit.py` + `assemble.sh` from a linear shell-orchestrated flow into a typed DAG. Each node declares inputs + config + output; the DAG runner hashes inputs+config and skips nodes whose cache hit is valid. Edit one prompt — only that node and its downstream re-run. Edit the manifest's style block — recompute everything style-dependent, leave timing alone.

**Why selected:** Solves a real engineering pain Sean already feels (a config tweak costs a full chain). Validated pattern (Krea Node Agent). Foundation for everything downstream — Planner agent (TOP-2) emits DAG nodes, Animatic stage (TOP-1) becomes one node type, Museum capture (TOP-3) hooks into node-completion events. Without this, the pipeline can't scale to short films where one run = hundreds of nodes. With this, partial iteration becomes the default working mode.

**Key assumptions to validate:**
- Python DAG libraries (Prefect 3, Dagster, or a minimal hand-rolled one) work without dragging in heavy infra. Likely hand-rolled is fine at this scale (a few hundred nodes max).
- Content hashing on multimodal inputs (image bytes + prompt text + model name) is fast enough to not dominate per-node overhead. Almost certainly yes; SHA256 a 2MB PNG is microseconds.
- The existing 6-phase mental model survives the DAG refactor — i.e., DAG nodes still group naturally into Phases A-E for human readability. Probably yes if phases become DAG subgraph tags.

---

### **TOP-5 — Character Bible as a project entity** (from DES-2)

**Description:** Replace the current single-anchor pattern (`images/2D-Character-Sketch-Sean-v1.png`) with a structured `characters/{character_id}/` folder holding: anchor pose, turnarounds (front/3-quarter/profile/back), expression sheets (8-12 emotions), costume variants, key prop attachments, line-weight reference, and a YAML `character.yaml` declaring canonical color palette, proportion rules, identity-drift triggers (SF02 conditions). Manifest references characters by ID; generator auto-loads relevant sheets based on shot needs.

**Why selected:** Without this, the pipeline can't ship anything beyond one-character pencil tests. Short films and the character-design-extension scope Sean called out (turnarounds, variations, clothes swaps) all require a richer character primitive. It also makes character work portable — the same Character Bible can drop into a new project without re-creating anchors. Modest effort: directory convention + manifest schema extension + a loader change in `generate.py`.

**Key assumptions to validate:**
- Multi-reference image conditioning in NB2 stays performant when 3-5 character sheets are loaded per call (vs. the current 1-2). Test by stacking refs and measuring identity drift / latency.
- A character's "canonical look" can be captured well enough in a Bible folder to enable consistent generation across long time gaps. Likely yes for Sean's drawn characters; uncertain for AI-original characters where the model drifts the look between sessions.
- The Bible authoring workflow (Sean producing turnarounds + expression sheets) is itself a use case the pipeline supports — meta-recursion that probably needs its own Project-Type template (PM-3).

---

## 4. Deferred, Not Rejected

These ideas are good but premature, dependent on a top-5, or scheduled for a later session:

| Idea | Why deferred |
|------|--------------|
| PM-3 Project-Type templates | Wait until TOP-2 Planner agent is real — templates become the planner's input library, not standalone. |
| PM-4 Comparison-asset stage | Absorbed into TOP-3 Museum mode. |
| PM-5 Decision ledger | Absorbed into TOP-3 Museum mode. |
| DES-3 Draft → Pro tier state machine | Already implicit in Seedance Fast→Pro; formalize after DAG refactor (TOP-4) so the state machine sits at node level. |
| DES-4 Trace overlay debug mode | Nice but not load-bearing; build after Animatic phase (TOP-1) exists. |
| DES-5 Human moments annotation | Add to manifest schema during TOP-3 Museum integration — they're the badges the museum renders. |
| ENG-2 Planner agent emits manifest | This IS TOP-2; the "emits manifest entries" framing is the implementation detail. |
| ENG-3 Critic agent | **Promoted to principle — see §5.** Implementation (which model, which CLI orchestration) still scoped for the agent-fleet session, but placement and role belong to architecture. |
| ENG-4 Manifest schema versioning | Comes for free with TOP-4 DAG (every node is content-addressed; manifest sections become node configs). |
| ENG-5 Content-addressed asset store | Scope for the **multimodal vault/RAG** session. The hashing comes from TOP-4; the vault layer wraps it. |

---

## 5. Critic-as-Principle — Promoted from Deferred

**Decision (2026-05-24, post-brainstorm):** The critic / judge / auditor role is not deferred. It is a structural principle that informs every phase of the pipeline. Per Sean: "Having a judge type of agent to solidify the output and point out any potential pitfalls or flaws will be a staple in all of my agentic workflows from here on out." Specific agent implementation (which model, which CLI orchestration) stays scoped for the agent-fleet session, but **placement and role of critic checkpoints belong to the architecture lock.**

### 5.1 Three-Tier Critic Stack

Mirroring the proven pattern in code-brain (rule-based hooks + vault-critic Codex/Anti-Gravity parallel + LLM Council variance), the v2 pipeline runs critics at three escalating tiers:

| Tier | What it is | When it runs | Cost / latency |
|------|------------|--------------|----------------|
| **T1 — Rule gates** | Current HF/SF reason codes. PIL aspect-ratio check, file format, dimension verification. Deterministic, instant. | Every frame, every node | $0, <100ms |
| **T2 — Vision critic** | Claude or Gemini reviews output against beat description + style guide + storyboard intent. **Proposes specific prompt diffs**, not just pass/fail. | Per major node output (Generate, Motion, Assemble) | ~$0.01–0.05/call, 5-15s |
| **T3 — Multi-CLI variance critic** | Codex CLI + Anti-Gravity CLI run in parallel (the vault-critic pattern, $0 incremental on subscriptions). Reserved for high-stakes stage gates. | Phase transitions only | $0 incremental, ~120s/CLI |

### 5.2 Critic Checkpoints in the Pipeline

Five named checkpoints in the v2 strawman (see §6):

1. **Post-Animatic (Phase 4 → 5)** — T3 gate. Did timing arc actually land? Worth the compute to validate before $20+ of NB2/Seedance burn downstream.
2. **Per-frame Generate (Phase 5)** — T1 + T2. Current HF/SF stays; vision critic adds beat-fidelity reads + prompt-diff proposals.
3. **Post-Motion (Phase 6 → 7)** — T2. Seedance motion currently isn't QA'd beyond visual review; vision critic flags arc/timing/identity drift in video output. This is an existing gap.
4. **Post-Assemble (Phase 8 → 9)** — T2. Loop coherence, pacing across the whole cut, not just per-frame.
5. **Pre-Museum publish (orthogonal)** — T3 gate. The museum doc is public-facing; multi-CLI variance gives the strongest read on whether narrative + comparison artifacts hold up under independent eyes.

### 5.3 Why Promote This

Sean's existing agentic workflows have proven that **the critic earns its keep when it proposes fixes, not just flags problems**. Building critics in from day one is cheaper than retrofitting them after the pipeline ships generic "AI output" with no quality conviction. It's also a structural answer to a portfolio risk: a museum that shows process needs to show *taste*, and taste means visible quality gates with reasoning attached.

### 5.4 What's Still in the Agent-Fleet Session

The architectural placement is locked here. Implementation belongs to the next session: which model handles T2 vision critique (Claude Sonnet vs Gemini 3 Pro), how the T3 Codex/Anti-Gravity CLIs wire into the pipeline runner, how critic outputs feed back into prompt iteration (auto-retry vs human-routed), and whether T3 critics share standing-context preambles the way `vault-critic` does in code-brain.

---

## 6. Draft→Pro Escalation as Principle — Promoted from Deferred

**Decision (2026-05-24, post-brainstorm):** Every expensive pipeline node declares a draft tier and a pro tier. Default behavior: run draft, present preview, escalate to pro on approval (human-routed or critic-passed). The Seedance Fast→Pro pattern already in `prompts/seedance-template-v4.md` is the prototype; this generalizes it to a pipeline-wide convention.

### 6.1 Why Promote This

Iteration speed is the load-bearing UX for a solo creator. The DAG refactor (TOP-4) cuts redundant work via caching; draft→pro escalation cuts *first-time* work via cheaper previews. Together they're the two halves of "make iteration cheap." Without the second half, every new prompt costs the full pro-tier burn — exactly the workflow Sean is trying to escape.

It also pairs with **museum-mode capture (TOP-3)**: draft outputs aren't waste, they're evidence of iteration. The museum walkthrough renders "we tried draft, here's what it showed, here's why we committed to pro" — turning a compute-cost optimization into a narrative asset.

### 6.2 Draft → Pro Coverage by Phase

| Phase | Draft tier | Pro tier | Notes |
|-------|------------|----------|-------|
| 0 BRIEF & PLAN | Haiku planner, rough cost band | Sonnet planner, fine cost estimate | Optional — long briefs only |
| 1 SCAFFOLD | n/a | n/a | File structure, no compute |
| 2 CHARACTER BIBLE | 2-3 anchor angles, no expression sheet | Full 8-angle turnaround + 8-12 expressions + costume variants | Draft answers "does this character work?"; pro is the reusable artifact |
| 3 STORYBOARD | rough beat sketches (silhouettes) | full storyboard panels (composition + camera) | Sean often hand-authors draft; agent fills pro |
| 4 ANIMATIC | circles/silhouettes timing block | cleaner shape-block with intended-pose silhouettes | Both stay human-authored; pipeline distinguishes tier for museum capture |
| 5 GENERATE | single attempt, 1-ref stack | multi-attempt, 2-ref stack with frame chaining | Maps to existing retry ladder; "draft" = lite first attempt |
| 6 MOTION | Seedance Fast, 480p | Seedance Pro, 720p+ end-frame anchor | Already implemented — this is the prototype |
| 7 AUDIT | n/a | n/a | Consolidation phase, no escalation |
| 8 ASSEMBLE | low-fps preview cut, no GIF palette opt | full export (MP4 + WebM + optimized GIF) | Draft enables fast playback review |
| 9 QA REVIEW | n/a | n/a | Single human pass |

**7 of 10 phases have meaningful draft↔pro distinction.** Cost-light or human-only phases opt out.

### 6.3 Implementation Hooks (for the Lock Session)

- Every DAG node (TOP-4) declares `tier: draft | pro` in its config; runner caches both independently keyed.
- Manifest schema gets a new top-level `tiering:` block defining default tier per phase + escalation rules ("auto-escalate to pro on critic-pass" vs "always require human approval").
- Brief→Plan cost preview (TOP-2) shows two cost lines: "draft-only run" vs "draft → pro full run". Sean sees the savings upfront.
- Museum capture (TOP-3) tags every artifact with its tier; museum doc renders draft + pro side-by-side where both exist.

### 6.4 Note on Critic Tiering Symmetry

The critic stack (§5.1) is itself a draft→pro structure applied to *critique*: T1 rules = trivial draft, T2 vision critic = draft critique, T3 multi-CLI variance = pro critique. Same pattern, same iteration-speed logic. Worth naming explicitly: **draft→pro escalation is the architectural metaphor; the critic stack and the generation stack are both expressions of it.**

---

## 7. Architecture Implied by Top 5 + Critic Checkpoints (Strawman)

```
Phase 0   BRIEF & PLAN       brief.md → planner agent → plan.md + cost estimate → human approval gate
Phase 1   SCAFFOLD           plan.md → manifest.yaml (DAG node definitions) + project structure
Phase 2   CHARACTER BIBLE    characters/{id}/ folders authored or referenced; anchor sheets validated
Phase 3   STORYBOARD         beat sheet + shot list (largely human-authored; agent assists)
Phase 4   ANIMATIC           shape-block timing pass (human-authored; pipeline ingests as constraint)
                             ⚖ T3 critic gate — timing arc validated before downstream burn
Phase 5   GENERATE           NB2 stills, DAG-orchestrated, cache-hit aware, multi-character Bible-loaded
                             ⚖ T1 + T2 critic — HF/SF rules + vision beat-fidelity per frame
Phase 6   MOTION             Seedance video between approved anchors, draft → pro tier escalation
                             ⚖ T2 critic — motion arc / identity drift in video output
Phase 7   AUDIT              consolidation phase — routes critic findings from phases 4-6 to retry ladder
Phase 8   ASSEMBLE           FFmpeg, comparison GIFs auto-rendered, museum capture hooks fire
                             ⚖ T2 critic — full-loop coherence + pacing
Phase 9   QA REVIEW          creative-director skill + final human gate

(parallel)   MUSEUM           every approve/reject/retry writes capture artifacts; static site renders at end
                              ⚖ T3 critic gate — narrative + comparison artifacts before publish
```

That's a 10-phase pipeline (0-9) with 5 named critic checkpoints across 3 tiers, plus the museum as an orthogonal capture layer. Up from 6 phases with one consolidated audit. **Phase 7 Audit changes role**: it's no longer where critique happens, it's where critique findings are *consolidated and routed* to the retry ladder.

---

## 8. Open Questions — RESOLVED (2026-05-24)

| # | Question | Answer |
|---|----------|--------|
| 1 | Animatic format | **Procreate Dreams + regular Procreate (PNG sequences).** Pipeline ingests both — Dreams as video/frame export, Procreate PNG stacks for hand-drawn keys |
| 2 | Brief format | **Free-text markdown.** Sean's rationale: *"I don't like it when the docs feel like it was strictly made for the terminal. We're making art. It should feel free."* Tonal directive across all anima docs — prose over tables where reasonable, studio-manual over CLI-reference |
| 3 | Bible authoring as project type | **Both — but authoring-first.** Mirrors current session pattern: brainstorm, propose, approve. Bible-authoring is a Project-Type template alongside short-film / character-study / motion-comparison archetypes (PM-3) |
| 4 | Museum publishing target | **`sw-ai-pm-portfolio` Astro content collection.** Standalone site only when anima outgrows the portfolio. Museum builder outputs MDX matching the portfolio's content-collection schema |
| 5 | DAG library choice | **Hand-rolled minimal runner** (~300-500 LOC). See change-map §6 for full rationale |
| 6 | Project rename | **`anima`** — "tells a story in one word." Latin root (breath/soul); short; available-sounding; threads the needle between artisan and technical |

**New decision (2026-05-24):** Eval suite + traces workstream mirroring `code-brain/evals/vault-synthesizer/` pattern. Each agent commit gated by its eval suite; model bake-offs ship as dated first-class artifacts. See [`2026-05-24-pipeline-v2-change-map.md`](2026-05-24-pipeline-v2-change-map.md) §7 for scope.

**Commit 1 is fully unblocked.**

---

## 9. What's Next

- **Next session:** Map these 5 against the current pipeline (Task #2), then lock 3-5 decisions (Task #3).
- **Following session:** Agent fleet brainstorm (Claude SDK + Anti-Gravity + Codex topology, named roles inspired by OiiOii's 7-agent crew).
- **After that:** Multimodal vault/RAG layer (Gemini Embedding 2 vs OpenRouter alternatives, Obsidian integration).
- **Then:** Museum/showcase format brainstorm.

Each of those four sessions feeds the eventual `docs/pipeline-architecture-v1.md` lock + the project rebrand.
