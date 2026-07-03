# ① Brainstorm Front Door — Build Planning Prompt

**How to use:** open a fresh Claude Code session in the `anima` repo, set the model to **Opus 4.8**, and paste everything below the line. It co-plans the build with **Codex** (via the `codex` plugin) and ends by printing a **Fable 5 execution kickoff** you paste into a separate Fable-5 session. The ① design is already locked from the dry-run — **no brainstorming pass needed**; go straight to planning.

---

▼▼▼ PASTE EVERYTHING BELOW THIS LINE ▼▼▼

You are **Opus 4.8**, planning the build of anima's **① Brainstorm Front Door** — the creative concept-to-brief skill chain. Your job this session is to produce a **detailed, TDD-sliced implementation plan** that **Fable 5 will execute**, co-planned with **Codex** via the `codex` plugin. **Do NOT write implementation code this session — plan only.**

## 1. Read first (source of truth)
- `CLAUDE.md`, `PHILOSOPHY.md`, `ROADMAP.md` — the outward-turn workstream + the anti-drift contract.
- **The build plan you're implementing:** `docs/active/2026-07-02-brainstorm-front-door-build-plan.md` — the five-stage chain (EXPAND → INTERROGATE → ART-VIZ → STRESS-TEST → SYNTHESIZE), the resolved forks, the build slices.
- **The validated dry-run — your spec AND your eval fixture:** `docs/active/2026-07-02-frontdoor-dryrun-pinata-short-concept.md` + `...-studio-brief.md`. The built chain must reproduce output of this quality.
- **The output contract:** `tests/fixtures/studio_brief_seed.md` (the Studio Brief shape Maya consumes) and how `pipeline/run.py` starts a run *from* a brief dir.
- **What the chain orchestrates:** `.claude/skills/creative-director/SKILL.md`, `writing-voice-modes` (+ `pipeline/agents/prompts/sean-screenwriting-voice.md`), and the gemini image-gen skills are **in this repo**. The borrowed skills that are **NOT** in `anima/.claude/` — `sw-creative-toolkit:brainstorm` / `innovation-strategy` / `storytelling`, `pm-execution:pre-mortem` / `strategy-red-team` / `sw-creative-toolkit:problem-solving`, `voiceprint-interviewing`, the superpowers discipline skills, Matt Pocock's Grill Me (`grilling` / `to-prd` / `prototype`), and the AKCodez style-skill shape — have their **full details vendored, organized by build stage**, in:
- **⇒ [`docs/active/2026-07-02-referenced-skills-detail-reference.md`](2026-07-02-referenced-skills-detail-reference.md) — READ THIS for any referenced skill that isn't in `.claude/skills/`.** (Don't guess a skill's method from its name; the details are here.)
- `docs/architecture/fleet-ops-protocol.md` — discipline for any costed run.

## 2. Scope
Plan the **whole five-stage chain**, but sequence the build so **Slice 1 = the walking skeleton** ships first: the user-invoked orchestrator + INTERROGATE + SYNTHESIZE, emitting a concept doc + Studio Brief that `pipeline.run` accepts. Then EXPAND (adaptive-to-spark divergence), then ART-VIZ (+ a `genndy-tartakovsky` style skill, customized from the AKCodez shape but driven through the **Higgsfield MCP, not Playwright**; Flow `$0` default), then STRESS-TEST. The **piñata dry-run is the ground-truth fixture** — the skeleton must reproduce a brief of that calibre.

## 3. Co-plan with Codex
1. Draft your own detailed plan first — skill-chain architecture, the file layout in `.claude/skills/`, the orchestrator↔sub-skill contract, the artifact schemas (concept doc + Studio Brief + style refs + character seeds), per-slice TDD task lists, checkpoints. Write it to `docs/active/2026-07-02-frontdoor-build-plan-CONVERGED.md`.
2. Get Codex's **independent** plan: `/codex:rescue --background "Read docs/active/2026-07-02-brainstorm-front-door-build-plan.md plus the two dry-run docs; produce your own independent, detailed, TDD-sliced implementation plan for this five-stage brainstorming skill chain. Focus on skill-chain architecture, the orchestrator/sub-skill boundary, artifact schemas, slice sequencing, and test strategy."` — then `/codex:status`, then `/codex:result`.
3. **Reconcile** the two plans — take the stronger call on each point; record where they disagreed and why you chose.
4. **Red-team** the converged doc: `/codex:adversarial-review challenge this build plan — attack the orchestrator/sub-skill boundaries, the "expand adaptively" logic, the art-viz cost path, and whether a simpler chain ships the same value. Focus on failure modes and over-engineering.`
5. Fold Codex's red-team into the final plan.

## 4. anima discipline (bake into the plan)
- **Worktree isolation** (native or `superpowers:using-git-worktrees`) — one worktree for this build.
- **TDD** (`superpowers:test-driven-development`) — every slice stub-green first; the skills must be credential-free-testable (stub fallback) so the suite stays green in CI without keys.
- **Fleet-ops:** subscription billing only — **never `ANTHROPIC_API_KEY`**; ART-VIZ defaults to Flow (`$0`), Higgsfield MCP on demand.
- **The two md5 guards must NOT move:** `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4`; `pipeline/agents/prompts/sean-screenwriting-voice.md` = `945af824fa53b948a18ac6bf206d67ef`.
- Tests run **per-directory** from the repo root; run `superpowers:verification-before-completion` before claiming any slice done.

## 5. Deliverables (this session — no building)
1. `docs/active/2026-07-02-frontdoor-build-plan-CONVERGED.md` — the final Opus+Codex plan: architecture, `.claude/skills/` file layout, per-slice TDD task lists, checkpoints, risks, and the Codex-reconciliation notes.
2. A **Fable 5 execution kickoff** — print, at the very end, a ready-to-paste prompt for a fresh Claude Code session **set to Fable 5** that has it execute **Slice 1 only** (the walking skeleton), TDD, in the worktree, stopping at the first green checkpoint for Sean's review.

Do not start building. End by printing the Fable 5 kickoff.
