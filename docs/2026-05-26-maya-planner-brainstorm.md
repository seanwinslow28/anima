# Maya the Planner — Phase 0 Brainstorm

**Date:** 2026-05-26
**Workstream:** Commit 3 — Phase 0 Brief & Plan (gating the `acceptance_criteria.json` schema, the brief.md template, the cost-estimator algorithm, and the human-approval UX)
**Skill invoked:** `pm-product-discovery:brainstorm-ideas-existing` — multi-perspective product trio (PM + Designer + Engineer), 5 ideas per perspective, anti-bias rotation pass, converge on top 5.
**Grounded in:** [`docs/2026-05-26-agent-fleet-brainstorm-v2.md`](2026-05-26-agent-fleet-brainstorm-v2.md) §2.3 (Pattern B — Planner-Chairman shared rubric), §6 (Maya = Opus 4.7 → Sonnet 4.6 validation → human gate, confidence 90%), §7 (cost ceiling), [`docs/research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md`](research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md) §1.3 (acceptance_criteria as structural fix for local-optimization drift), [`docs/2026-05-24-pipeline-v2-change-map.md`](2026-05-24-pipeline-v2-change-map.md) §3 TOP-2 + §4 Commit 3 sequencing, [`PHILOSOPHY.md`](../PHILOSOPHY.md) (the critic earns its keep by proposing fixes; iteration must be cheap; read like a studio).
**Status:** Brainstorm complete. Five ideas locked for commit 3 + commit 3b implementation. Eight ideas deferred with explicit promotion triggers. The criteria contract is concrete enough to write code against.

---

## 1. The Maya role, in one paragraph

Maya is anima's line producer. She reads a free-text brief, asks the structural questions the brief left implicit, drafts a production plan that names every phase the run will touch, prices the compute spend against Flo's routing table, and emits an immutable `acceptance_criteria.json` that every downstream critic cites by ID. She is the single agent in the fleet whose output gates spend; nothing burns model time until Sean approves her plan. She runs once per piece and her assignment is locked at Opus 4.7 primary → Sonnet 4.6 validation pass → human gate. The four artifacts she ships — `00_studio_brief.md` (Sean-authored), `01_production_brief.md` (Sean-or-Maya-authored), `acceptance_criteria.json` (Maya-authored), and `plan.md` (Maya-authored, Sean-approved) — are commit 3's scope. The schema and shape of each is what this brainstorm exists to crack.

What's locked already:
- Maya's persona name and model assignment (v2 §6, confidence 90% — *not for redecision*)
- Brief format is free-text markdown (change-map §5 Q2 resolved)
- Cost preview reads Flo's `generation.routing:` block (Image-Model-DR SYNTHESIS §2)
- Criteria emission is the structural fix for local-optimization drift (synthesis §1.3)
- The `criteria_locked: true` manifest flag and the enforcement layer ship in commit 4 (already shipped as `fcf28cd`)

What this brainstorm decides:
- The schema and shape of `acceptance_criteria.json` (Sean's primary structural question)
- The `brief.md` template — what's anchored vs free, what's required vs optional
- The cost estimator's algorithm and surface
- The human-gate UX — how Sean reviews, approves, and edits
- The `plan.md` output schema

The product trio frame: Sean (PM) + Sean (Designer) + Sean (Engineer) + Claude. Three independent reads of the problem from three lenses, then a convergence pass.

---

## 2. PM Perspective — Business value, strategic alignment, customer impact

The Maya brief from a product-management lens is *"the structural fix for the 60-percent-of-indie-projects-die-mid-flight failure mode."* Every PM idea below targets a specific failure surface from the v2 synthesis.

**PM1. Two-tier brief — Studio Brief plus Production Brief.** Maya consumes two markdown files at run start: `00_studio_brief.md` (story, character, audience, tone, non-negotiables — the things only Sean knows) and `01_production_brief.md` (phases, characters loaded, target medium, deadline — the things Maya can validate against the manifest). The Studio Brief sources taste-blocking criteria; the Production Brief sources spec-blocking criteria. Two-tier separation prevents conflating "this doesn't match the story" with "this doesn't meet the spec," which the synthesis §5 names as the load-bearing failure mode for indie creators. Cy reads the Studio Brief during Phase 2 Bible authoring; the orchestrator reads the Production Brief when scheduling.

**PM2. Cost preview surfaces draft vs pro as a side-by-side comparison.** Maya's plan.md cost section renders two columns: "draft tier throughout the pipeline" + "draft → pro escalation at the expected critic-pass rate." Sean approves the higher number, but actual spend tracks lower because draft-tier nodes that pass the critic don't re-run. The side-by-side surfaces the iteration savings the project's draft→pro principle (philosophy §3, change-map §7) depends on. It's also the frame Sean has been thinking in already for Seedance Fast → Pro.

**PM3. Acceptance criteria carry impact tags inline.** Each AC entry includes `impact_tag: hero | identity_critical | continuity | aesthetic | structural`. Em's escalation hatch (already wired in commit 8) keys off impact tag, not just shot ID. Aligns critic effort with criterion importance and operationalizes the synthesis §5 thesis that validators cannot recover taste that was absent at generation time — by making the *taste signal* travel with the criterion through every downstream consumer.

**PM4. Maya emits a risks-if-rejected memo alongside the plan.** A second markdown file, `risks-if-rejected.md`, names what stays unfunded if Sean walks the plan. Forces Maya to defend the plan rather than just request approval, and reads on the museum side as deliberate, considered process — not "Sean approved whatever Maya asked for." The memo also surfaces second-order risks the brief left implicit ("if we don't fund Phase 6 motion for Beat 3, the cut reads as a slideshow") that catch Sean before they catch the audience.

**PM5. Approval ceremonies are timestamped and signed via git commit.** Plan approval lands as a git commit on the manifest with a `criteria_locked: 2026-MM-DD-HH-MM-SS` frontmatter field and Sean's user.email. The audit trail is git-native, not a separate ledger. The synthesis §8 portfolio-positioning angle ("running a three-provider T3 peer ensemble for a 2D animation quality gate has no direct prior art") needs structured records to defend, and the approval ceremony is the structured record. Bonus: `git blame` on a criterion answers "when did this criterion get added, and who authored it."

---

## 3. Designer Perspective — User experience, usability, delight

The Maya brief from a design lens is *"how does the studio-manual voice live at the artifact level."* Every Designer idea targets the philosophy §6 "read like a studio" directive applied to the planning artifact itself.

**DES1. Plan.md renders as a tear sheet, not a dump — and the tear sheet lives in the renderer, not the file.** Maya emits plan.md as clean markdown; `pipeline plan show` is a Python rendering layer that reads the markdown and post-processes the key sections (cost preview, criteria summary, character box, beat strip, routing legend) into ASCII box-drawn views for terminal review. The file on disk stays plain. Sean reviews plans the way a director reviews a board — visually, fast, holistically — but downstream consumers (Cy, Em, Sage, chairman, museum writer) read clean markdown and clean JSON. Their context windows never see a box character. Box-drawing costs zero LLM tokens because boxes are Python string operations, not Opus output. The dense-table-of-fields shape that planning tools default to is exactly the terminal-aesthetic philosophy §6 refuses, and the renderer-as-separate-layer is how the studio voice ships without polluting the agent fleet's context.

**DES2. AC IDs are mnemonic, not numeric.** Not `AC01, AC02, AC03` but `AC.identity.front-pose`, `AC.timing.beat3-hold`, `AC.tone.melancholy-not-grief`. When Em cites `AC.tone.melancholy-not-grief` in a borderline verdict, Sean reads the criticism in plain English without cross-referencing a key. Mnemonic IDs cost zero performance and gain readability everywhere they surface — in plan.md, in critic logs, in the museum walkthrough, in `git blame`. The pattern is `AC.{category}.{specific-handle}` with category drawn from a short closed vocabulary (`identity / proportion / continuity / timing / tone / structural / technical`).

**DES3. Approval gate is a single Y/N plus an optional inline edit pane.** Not a multi-step wizard, not a CLI dialog tree. Sean runs `pipeline plan show` and gets a single rendered tear sheet on the terminal. `pipeline plan approve` is one command; `pipeline plan edit AC.timing.beat3-hold` opens the inline edit. Single-shot ceremonies match how Sean works — solo, deliberate, fast. The interaction surface is the studio-manual voice at the UX level: minimal ceremony, maximum signal.

**DES4. Maya names what she's uncertain about.** Plan.md includes a "Maya's confidence notes" section: where the cost estimator hedged, where the criteria are interpretive (`AC.tone.melancholy-not-grief` is interpretive; `AC.technical.aspect-ratio-16-9` is not), where she'd flag a brief reread before approval. Visible-confidence is the studio-manual voice (philosophy §6) applied to the planner's own self-awareness. Mirrors how a film line producer flags risks in the budget walkaround — not buried in the addenda, surfaced in the headline review.

**DES5. Brief.md template is anchored, not blank.** `pipeline plan init` creates `briefs/2026-MM-DD-{slug}/00_studio_brief.md` pre-filled with seven structural prompts (story / character / tone / format / medium / deadline / non-negotiables) phrased as questions Sean fills in. The blank-page tax that kills solo-creator velocity gets paid by the scaffold, not by Sean. Mirrors how `git init` and `gh repo create` work — opinionated defaults that the user can edit but doesn't have to author from scratch.

---

## 4. Engineer Perspective — Technical possibilities, data leverage, scalable solutions

The Maya brief from an engineering lens is *"how does the contract layer look such that every downstream consumer reads from it without needing to know about it."* Every Engineer idea targets the typed-Protocol shape from commit 4's `AgentSpec`.

**ENG1. acceptance_criteria.json is a JSON-LD-flavored graph, not a flat list.** Each AC entry has `id`, `description`, `cites_phase: [4, 5, 6]` (which phases it gates), `cites_personas: [em, cy, codie]` (which agents must reference it during their respective passes), `impact_tag`, `parent_id` (for derived criteria), `derived_from: [studio_brief.tone, philosophy.engine-truth]` (provenance pointer). The graph shape beats a flat list when 200-plus criteria exist across a multi-character piece, and it makes the criteria queryable: "show me every AC Cy must satisfy" or "show me every AC derived from the Studio Brief's tone section" become single-line filters.

**ENG2. Cost estimator is its own AgentSpec, not Maya-internal logic.** A new `CostEstimatorNode` reads Flo's routing table, the production brief, the manifest's `tiering:` block, and any historical-run data, then emits a structured `CostEstimate` with low/median/high bands. Maya consumes it through the same Protocol-typed interface as everyone else; the estimator's logic stays auditable and unit-testable in isolation. Commit 5's draft → pro tier escalation in the DAG runner reads from the same estimator. Maya doesn't need to know how the estimator works; she just calls it. Separation of concerns at the node-protocol layer.

**ENG3. Plan-mutation requires force-flag plus actor plus reason, audited to a JSONL stream.** Mirrors commit 4's `criteria_locked` enforcement verbatim. `pipeline.cli plan mutate --force --actor sean --reason "Sage flagged AC.identity.proportion drift, broaden tolerance"` writes one line to `runs/{id}/plan_audit.jsonl` and re-emits plan.md with a delta block. The contract reads: "you can't quietly change your mind after spend started." Same pattern Sean's already comfortable with from the criteria audit layer. The museum surfaces the audit log as a portfolio artifact — the cuts that didn't happen are evidence the cuts that did were considered.

**ENG4. Maya's prompt loads the brief, philosophy.md, AND the historical-plan corpus.** Past approved plans live in `runs/*/plan.md`. Maya's standing-context preamble includes a corpus of three representative prior plans (or until commit 3 ships, a synthetic seed set written by Sean). Few-shot grounding solves the cold-start problem; plans converge on Sean's actual voice and rhythm faster than zero-shot generation. The pattern lifts directly from the Code-Brain `vault-critic-standing-context.md` preamble — proven in the 2026-05-24 ablation runs to cut the generic-recommendation failure mode by a measurable margin.

**ENG5. Sonnet validation pass is an adversarial criteria critique, not echo confirmation.** The Sonnet 4.6 validation pass v2 §2 locks runs as a *devil's-advocate* sweep against Maya's criteria: "find one criterion that's untestable; find one cost line that's under-estimated; find one impact_tag that's wrong." If Sonnet returns nothing, the validation flags itself low-signal and bumps to a second Opus pass for cross-check. Mirrors the cheap-judge defense ladder from synthesis §1.5 (sycophancy at 58.19% baseline, miscalibrated confidence, self-preference bias) — applied at the planning layer instead of just the critic layer. Cheap to instrument, hard to skip once it's in the pipeline.

---

## 5. Anti-Bias Rotation Pass — What each role's prior suppressed

Per the brainstorm skill protocol, after the initial fifteen ideas, re-read with each role's prior off and ask what the other roles would notice. The rotation surfaces ideas that fall in the gaps between role lenses.

**ROT1 (Engineer thinking with a PM hat). Maya emits two plans — one for Sean to ship, one for Sean to learn from.** Alongside the approval-track plan, Maya emits a `plan-shadow.md` exploring two or three alternative production approaches at lower fidelity (different routing splits, different character-loading depth, different critic configurations). The shadow plan isn't run; it's the museum content showing the path not taken. The portfolio-positioning angle from synthesis §8 — anima as early practitioner of provider-diverse evaluation councils — needs *visible alternatives* to demonstrate the choices were deliberate. The shadow plan IS that evidence.

**ROT2 (Designer thinking with an Engineer hat). The approval CLI lives inside the brief.md, not outside it.** Sean can edit `criteria_locked: 2026-MM-DD` directly in the YAML frontmatter of brief.md and commit it. No separate `pipeline plan approve` command. The brief and the lock live in one file. Solves the "approval ceremony as separate UX surface" complication by collapsing two artifacts into one. Mirrors how Astro content-collection frontmatter works — the file IS the record.

**ROT3 (PM thinking with a Designer hat). Cost estimator outputs are images, not tables.** A horizontal stacked bar showing draft vs pro spend by phase, color-coded by Flo's routing tier. Renders to `runs/{id}/cost-preview.png` and surfaces in the museum walkthrough as a visual artifact, not a CSV. The film-tear-sheet metaphor extends to the cost layer. Bonus: Sean's already shipping Pillow + matplotlib in the data viz pipeline; the render is one library call away.

**ROT4 (Engineer thinking with a Designer hat). The brief template ships an inline anti-template-trap rubric.** The `00_studio_brief.md` template's "tone" section includes a "what this is NOT" subsection lifted directly from the `sw-ai-pm-portfolio` template-trap doctrine. Sean writes "this is not glossy, this is pencil-test rough" before Maya sees it. The taste vector is front-loaded at brief authoring time, not patched at critic time. Solves the synthesis §5 problem at the earliest possible upstream point.

**ROT5 (PM thinking with an Engineer hat). acceptance_criteria.json is versioned alongside the brief, not the manifest.** The criteria file lives at `briefs/2026-MM-DD-{slug}/acceptance_criteria.json` rather than at the manifest root. Mutation lands as a new versioned file (semver in the name) and the manifest references the active version by symlink or path. Solves the "criteria_locked but I need to change one thing" tension by making mutation observable as a new artifact rather than an audit-log entry. Subordinate to ENG3 if both ship — pick one.

---

## 6. Converged Top 5 — What Commit 3 Builds

Twenty ideas surfaced. Five converged. The selection criteria, in priority order: (a) strategic alignment with v2's Pattern B, (b) impact on Sean's iteration speed, (c) studio-manual readability, (d) feasibility for commit 3 + commit 3b, (e) portfolio-museum value. The ideas below are written as commit-ready specifications.

### TOP-1 — Two-tier brief: Studio Brief and Production Brief (PM1)

**What ships.** `pipeline plan init` scaffolds two markdown files into `briefs/2026-MM-DD-{slug}/`:

- `00_studio_brief.md` — Sean-authored, free-text, anchored by seven structural prompts (story / character / tone / format / medium / deadline / non-negotiables). This is the artifact Cy reads in Phase 2 when authoring the Character Bible; Em reads in Phase 5 when evaluating against tone; the chairman reads at T3 gates when synthesizing disputes. Mnemonic name: *the brief that says what this is for.*
- `01_production_brief.md` — Maya-drafted from the Studio Brief + the manifest, Sean-editable, structured (YAML-frontmatter + markdown body). Names the phases the run will touch, the characters loaded per shot, the target medium (GIF / WebM / museum walkthrough), the deadline, the routing tier defaults. The artifact the orchestrator reads when scheduling. Mnemonic name: *the brief that says how we'll make it.*

**Why it was selected.** The synthesis §5 single-most-important-decision argues taste must be present at generation time — that critics cannot recover what wasn't there. Two-tier separation is the structural fix at the source: critics that block on Studio Brief criteria are blocking on taste; critics that block on Production Brief criteria are blocking on spec. The two failure modes never get conflated, which means the retry ladder routes correctly and Sean reads the right kind of criticism when he reviews. v2's per-role table reads the Studio Brief for Cy, Sam, Em (tone passes); reads the Production Brief for the orchestrator, the cost estimator, Annie (continuity passes).

**Key assumptions to validate.**
- Sean is willing to author two files per piece instead of one. (Plausible — the Studio Brief is short, opinionated, anchored by prompts; the Production Brief is mostly Maya-drafted.)
- The Studio Brief stays under one page at typical piece complexity (one or two characters, one act, one minute of finished motion). (Plausible per the pencil-test reference.)
- Cy, Em, and the chairman can be prompted to read different sections of the two-file set without confusing them. (Validated by the standing-context preamble pattern from vault_critic.)

### TOP-2 — `acceptance_criteria.json` as a graph with mnemonic IDs and impact tags (ENG1 + DES2 + PM3 merged)

**What ships.** A single JSON file at `briefs/2026-MM-DD-{slug}/acceptance_criteria.json`. Each entry:

```json
{
  "id": "AC.tone.melancholy-not-grief",
  "description": "Beat 3's hold reads as melancholic, not grieving. Adult registers, not childlike.",
  "cites_phase": [4, 5, 6, 8],
  "cites_personas": ["em", "cy", "sage", "chairman"],
  "impact_tag": "aesthetic",
  "parent_id": null,
  "derived_from": ["studio_brief.tone", "philosophy.engine-truth"]
}
```

Mnemonic IDs follow `AC.{category}.{specific-handle}`. The category vocabulary is closed and short — `identity / proportion / continuity / timing / tone / structural / technical`. `cites_phase` and `cites_personas` are typed lists; the orchestrator routes criteria to the right consumers based on them. `impact_tag` drives Em's escalation hatch (already wired in commit 8's `_DEFAULT_ESCALATION_TAGS`). `derived_from` is a pointer back to the brief section the criterion came from — the provenance trail the museum surfaces.

**Why it was selected.** This is v2 Pattern B made concrete. The synthesis §1.3 names this the structural fix for local-optimization drift, the failure mode estimated to kill 60-plus percent of long-running indie animation projects. The graph shape is necessary because 200-plus criteria across a multi-character piece would be unreadable as a flat list, and the cross-phase / cross-persona citations are the load-bearing edges. Mnemonic IDs make every downstream surface (plan.md, critic logs, museum walkthrough, `git blame`) human-readable. Impact tags ship the taste-signal alongside the criterion, which is the synthesis §5 fix delivered at the contract layer.

**Key assumptions to validate.**
- Closed category vocabulary holds across diverse pieces (single-character, multi-character, mixed-style). (Will be tested by writing criteria for one or two real Acts after commit 3 ships.)
- The `cites_phase` and `cites_personas` lists are sufficient to drive orchestrator routing without additional metadata. (Plausible per the Em escalation pattern; will be tightened in commit 3b's eval suite.)
- Provenance pointers (`derived_from`) stay reliable when Sean edits the brief mid-flight. (Resolved by TOP-4 below.)

### TOP-3 — Cost estimator is its own AgentSpec (ENG2)

**What ships.** A new `CostEstimatorNode` at `pipeline/agents/cost_estimator.py`, implementing the `AgentSpec` Protocol from commit 4. Inputs: the Production Brief, the manifest's `generation.routing:` block, the manifest's `tiering:` block, and an optional historical-runs corpus. Outputs: a structured `CostEstimate` with low / median / high bands, broken down by phase, separated into "draft tier throughout" vs "draft → pro escalation at expected pass rate" columns. Renders to a `cost-preview` block in plan.md and to an optional `runs/{id}/cost-preview.png` for museum surfacing (the ROT3 idea folded in as a non-blocking enhancement).

Maya consumes the estimator through the same `AgentContext` / `AgentResult` interface as everyone else. The estimator's logic — pricing per-frame draft + pro tier, applying historical pass-rate as a probability weight, summing across phases — lives in a single file with its own unit tests. Commit 5's draft → pro escalation runtime reads from the same estimator. PM2's side-by-side framing is the surface; ENG2 is the implementation.

**Why it was selected.** Separation of concerns at the protocol layer. Maya's prompt stays focused on planning rationale; the estimator stays focused on arithmetic. The estimator becomes the first true tool-agent in the fleet (called by Maya at Phase 0, by the orchestrator at every tier-escalation decision in commit 5+, by the museum writer when narrating the run). One node, three consumers, one source of truth for spend. Auditable, unit-testable, replaceable.

**Key assumptions to validate.**
- The routing-table-driven cost computation matches actual spend within ±20% for the pencil-test reference implementation. (Will be measured against Act 1's already-shipped spend logs.)
- Historical pass-rate weighting beats naive worst-case estimation by a margin that justifies the complexity. (Validated by the first three real planning runs after commit 3 ships.)
- The Pillow + matplotlib render for the museum surfacing is light enough to not block plan generation. (Plausible — same stack already in use in `pipeline/audit.py`.)

### TOP-4 — Plan mutation is force-flag plus actor plus reason, audited to JSONL (ENG3)

**What ships.** Two CLI subcommands:

- `pipeline plan show [--run-dir RUN]` — Python rendering layer that reads plan.md (clean markdown on disk) and paints it on the terminal as a tear sheet with ASCII box-drawing around the cost preview, criteria summary, character box, beat strip, and routing legend. The boxes live in the renderer; the file stays prose. Zero LLM tokens spent on box characters. (DES1 folded in.)
- `pipeline plan mutate --force --actor sean --reason "Sage flagged AC.identity.proportion drift, broaden tolerance" --target AC.identity.proportion --field tolerance --value 0.15`

The mutation command refuses to run without `--force` + `--actor` + `--reason`. On success, writes one line to `runs/{id}/plan_audit.jsonl`:

```json
{"ts":"2026-05-27T14:32:11Z","actor":"sean","reason":"Sage flagged AC.identity.proportion drift, broaden tolerance","target":"AC.identity.proportion","field":"tolerance","old_value":0.10,"new_value":0.15,"plan_version":"1.1.0"}
```

Then re-emits plan.md with a delta block at the top (`## Plan changes since approval (1)`). The criteria file gets semver-bumped per ROT5's variant — `acceptance_criteria.json` becomes `acceptance_criteria-1.1.0.json` and the symlink at `acceptance_criteria.json` re-points. Sean's git workflow surfaces the diff naturally.

**Why it was selected.** Mirrors commit 4's `criteria_locked` enforcement exactly; Sean already knows the pattern. The contract reads "you can't quietly change your mind after spend started" — which is the museum's portfolio thesis (the iterations are deliberate; the changes are auditable) made operational. The JSONL stream is portfolio-grade content: when Sean ships the next short, the museum walkthrough can render "Here are the three criteria mutations during this production, and why each one happened." That's the synthesis §8 portfolio-positioning angle delivered as a structured artifact.

**Key assumptions to validate.**
- The mutation surface is small enough that Sean doesn't reach for "just edit the JSON file by hand." (Plausible if `plan mutate` is one command with sane defaults.)
- The audit log stays human-readable as it accumulates 5+ mutations on a single run. (Will be measured by tail-reading after the first three real runs.)
- Re-running downstream nodes after a mutation triggers the right cache invalidations from commit 4's content-addressed cache. (Will be wired into the mutation command's post-hook.)

### TOP-5 — Sonnet validation pass is adversarial, not echo (ENG5)

**What ships.** Maya's commit 3 flow runs in three phases:

1. **Opus 4.7 primary pass.** Reads the two-tier brief, drafts the production plan, emits the acceptance_criteria.json graph and the plan.md tear sheet.
2. **Sonnet 4.6 adversarial validation pass.** Receives Maya's output plus an explicit devil's-advocate prompt: "Find one criterion in this list that's untestable. Find one cost line that's under-estimated. Find one impact_tag that's wrong. If you cannot find any, flag the validation as low-signal and we'll escalate."
3. **Resolution.** If Sonnet surfaces a flag, Maya re-runs Opus on the named concerns and produces a revised plan. If Sonnet returns clean *and* doesn't flag low-signal, the plan ships to the human gate. If Sonnet flags low-signal (returns nothing AND notes uncertainty), Maya runs a second Opus pass with the same prompt and uses the second-Opus output as the validator. Three-call ceiling per plan.

**Why it was selected.** The synthesis §1.5 named defenses against cheap-judge failure modes — sycophancy at 58.19% baseline, miscalibrated confidence, self-preference bias — typically get applied at the critic layer. ENG5 applies them at the planning layer too, which is where they're cheapest to instrument and highest-leverage (planning happens once; critique happens 10-50 times). Adversarial framing solves the validator-as-echo failure mode by construction: Sonnet's job is explicitly to find one problem, not to confirm the plan.

**Key assumptions to validate.**
- The adversarial prompt produces useful flags more than 50% of the time on real plans. (Will be measured in commit 3b's eval suite against five seed briefs.)
- Sonnet's low-signal detection is reliable enough that the second-Opus escalation doesn't fire on every plan. (Will be tuned during commit 3 prompt iteration.)
- Three-call ceiling is sufficient for plan convergence; planning loops don't blow past it. (Plausible per the synthesis recommendation; will be verified empirically.)

---

## 7. Deferred Ideas (Not Rejected — Promotion Triggers)

| Idea | Why deferred | Promotion trigger |
|------|--------------|-------------------|
| DES1 — Plan.md as tear sheet (rendering layer) | Folded into TOP-4's `plan show` command — the rendering is the surface; the contract is what commit 3 ships | Already promoted; lands as part of TOP-4 |
| DES3 — Single Y/N approval gate | UX refinement; commit 3 ships the CLI first, the polish lands as a quality-of-life pass after the first three real runs | After three real planning runs |
| DES4 — Maya names her uncertainty | Emerges from prompt iteration in commit 3; not a schema decision | When commit 3 prompts stabilize |
| DES5 — Anchored brief template | Folded into TOP-1's `pipeline plan init` scaffold | Already promoted; lands as part of TOP-1 |
| PM4 — Risks-if-rejected memo | Surfaces as a section inside plan.md rather than a separate file; commit 3 prompt iteration | When plan.md sections settle |
| PM5 — Git commit ceremony | Natural extension of TOP-4's audit trail — the JSONL is the receipt, the git commit is the meta-receipt | Lands during commit 3 implementation as a final-step polish |
| ENG4 — Historical plan corpus | Needs ≥3 real runs first to seed the corpus; pre-corpus, Maya runs zero-shot with a synthetic seed plan written by Sean | After three approved plans exist |
| ROT1 — Shadow plans for museum content | Museum content, commit 6 not commit 3 | When commit 6 (museum) lands |
| ROT2 — Approval lives in brief frontmatter | Variant of TOP-4 with smaller surface; pick one — TOP-4 wins on auditability | Reopen if TOP-4's separate audit log feels heavy after three runs |
| ROT3 — Cost as image | Folded into TOP-3's optional `cost-preview.png` render as a non-blocking enhancement | Already promoted; lands as part of TOP-3 |
| ROT4 — Anti-template-trap rubric in brief template | Folds into TOP-1's anchored Studio Brief template — the "tone" section's "what this is NOT" subsection | Already promoted; lands as part of TOP-1 |
| ROT5 — Versioned criteria file | Folded into TOP-4's mutation contract — semver-bumped criteria files with symlink | Already promoted; lands as part of TOP-4 |

Twelve deferred items, eight of which are already absorbed into the top five as sub-components. The brainstorm produced more material than the converged five would suggest — the convergence is about which artifacts ship in commit 3, not which ideas get used.

---

## 8. What Commit 3 Looks Like

Concrete shape of the implementation handoff, ready for the next Claude Code execution session to pick up:

**Files touched (commit 3):**
- NEW `pipeline/agents/planner.py` — Maya's `AgentSpec` implementation, three-phase Opus → Sonnet adversarial → resolution flow
- NEW `pipeline/agents/cost_estimator.py` — TOP-3's `CostEstimatorNode`
- NEW `pipeline/agents/prompts/maya-planner-context.md` — standing-context preamble (mirror of `em-vision-critic-context.md`)
- NEW `pipeline/cli/plan.py` — `pipeline plan init / show / approve / mutate` subcommands
- NEW `pipeline/criteria.py` updates — graph-shaped criteria parsing per TOP-2 (extending commit 4's existing criteria.py)
- NEW `templates/brief/00_studio_brief.md` + `templates/brief/01_production_brief.md` — TOP-1's anchored templates
- NEW `runs/{id}/plan_audit.jsonl` convention — TOP-4's audit stream

**Files touched (commit 3b — evals):**
- NEW `evals/planner/cases.yaml` — 5–10 seed briefs paired with expected plan shape
- NEW `evals/planner/runner.py` — pytest harness (template for commits 8b/9b)
- NEW `evals/planner/conftest.py`
- NEW `evals/planner/last-run.md` — baseline trace

**Out of scope for commit 3:**
- Cy persona (commit 2 — Character Bible workstream)
- DAG runner refactor of generate.py/audit.py (commit 4 — already shipped)
- Draft → pro escalation runtime (commit 5)
- Museum capture (commit 6)
- The Anti-Gravity CLI rename patch (commit 8.1 — separate small follow-up per [`docs/research/2026-05-26-anti-gravity-cli-findings.md`](research/2026-05-26-anti-gravity-cli-findings.md))

**Effort estimate:** 4–6 evenings for commit 3 + 1 evening for commit 3b. Commit 3 is M–L on the change-map scale; the prompt-iteration variable is the biggest unknown, mitigated by ENG4's deferred historical corpus seeding.

**Dependencies:** Commit 4 is shipped (the `AgentSpec` Protocol, the typed `AgentContext` / `AgentResult`, the criteria.py enforcement layer). Nothing else blocks commit 3.

---

## 9. What This Brainstorm Doesn't Decide

To prevent scope creep:

- **The exact YAML frontmatter fields for plan.md.** Commit 3 prompt-iteration territory.
- **Whether Maya should re-run on brief edits or wait for an explicit `plan regenerate` command.** Defer to first real-run observation.
- **The closed category vocabulary for AC IDs.** Starting set is `identity / proportion / continuity / timing / tone / structural / technical`; will tighten or expand based on real briefs.
- **The Sonnet adversarial prompt's exact wording.** Commit 3 implementation detail; the *contract* (must find one problem or flag low-signal) is what this brainstorm locks.
- **The render template for `cost-preview.png`.** Optional enhancement; ship a placeholder if the matplotlib render slows iteration.

---

*The criteria contract is concrete. The brief shape is decided. The cost estimator has a home. The approval ceremony has an audit trail. The Sonnet validator has a teeth. Commit 3 has its specification.*
