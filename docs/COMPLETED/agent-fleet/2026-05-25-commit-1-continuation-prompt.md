# Continuation Prompt — anima Commit 1 (CLAUDE.md Rewrite + Architecture v1 Spec)

**For:** Fresh Claude Code session, 2026-05-25 (or whenever Sean picks this up)
**Recommended environment:** Claude Code (over Cowork) — see rationale at end
**Source session:** 2026-05-24 brainstorm + change-map + lock session

---

## How to use

Paste the prompt block below into a new Claude Code session opened in `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/`. The new session has zero memory of the prior conversation; the prompt is self-contained.

---

## Prompt to paste

> You're picking up a planning project mid-execution. Read three binding documents first — they're the locked context for everything that follows. Don't act before reading them.
>
> 1. `docs/2026-05-24-pipeline-v2-brainstorm.md` — 15-idea PM/Designer/Engineer brainstorm. 5 architectural decisions locked (Animatic Phase, Brief→Plan gate, Museum auto-capture, DAG refactor, Character Bible) + 2 principles locked (Critic Stack T1/T2/T3, Draft→Pro escalation). All 6 open questions resolved at §8.
> 2. `docs/2026-05-24-pipeline-v2-change-map.md` — current-state ground truth, change map per decision, 9-commit recommended sequence, DAG library rationale at §6 (hand-rolled ~300-500 LOC, not Prefect/Dagster/Luigi), evals workstream scope at §7.
> 3. `CHANGELOG.md` — the 2026-05-24 entry at the top captures the full lock state in two paragraphs.
>
> ### Project rename
>
> The project is now `anima` (Latin: breath/soul). The directory `sw-portfolio-animation-pipeline/` stays for now; the project *name* in CLAUDE.md, manifest.yaml, and CHANGELOG ships as `anima`. Directory rename happens at public-repo creation time.
>
> ### Your task: execute commit 1 — doc-only foundation
>
> Per change-map §3, commit 1 is doc-only, additive, zero risk to existing pencil-test workflows. Four files:
>
> **1. Rewrite `CLAUDE.md`** as the anima project manual.
>
> - New project name + one-line philosophy: human + AI as co-creators (not user/assistant). The pipeline is where they meet.
> - New 10-phase pipeline diagram (Phase 0 Brief & Plan → Phase 9 QA Review, plus orthogonal Museum capture). Critic checkpoint annotations inline (⚖ T1 / T2 / T3) — match the strawman in brainstorm §7.
> - New critic stack section — T1 rule gates / T2 vision critic / T3 multi-CLI variance. **Placement only**; implementation defers to the agent-fleet session. Reference brainstorm §5 and change-map §2.
> - New draft→pro escalation principle section — reference brainstorm §6. 7 of 10 phases participate.
> - Character Bible primitive replaces single-anchor pattern — reference brainstorm TOP-5 and change-map §2.
> - Source-of-truth document table refreshed: brainstorm + change-map + new pipeline-architecture-v1.md (below) promoted to first-class artifacts; old Act 1 / Act 2 docs stay but are clearly framed as the *first reference implementation*, not the whole project.
> - Skills map updated to reflect the 10-phase architecture.
> - Existing structural sections that work (Maintenance Conventions, Asset Naming, Directory Structure, Generation Chains, Seedance Generation, Dependencies, Engine Truth) should be preserved with anima-appropriate updates where needed.
>
> **Tonal directive — load-bearing.** Sean's exact words: *"I don't like it when the docs feel like it was strictly made for the terminal. We're making art. It should feel free."* Write in prose where prose works. Use tables only for genuine reference data (file paths, command syntax, schema fields, model parameter tables). Studio-manual voice over CLI-reference voice. If `.claude/skills/writing-voice-modes` exists in this project, use it to calibrate. As a secondary tone reference, `/Users/seanwinslow/Code-Brain/sw-ai-pm-portfolio/CLAUDE.md` describes Sean's preferred voice modes (Sedaris / Vonnegut / Sean Mode hybrid) — worth a one-minute skim.
>
> **2. Draft new `docs/pipeline-architecture-v1.md`** as the canonical lock document.
>
> - This is the source-of-truth going forward. Future Claude sessions read this, not the brainstorm or change-map (those are historical artifacts).
> - Self-contained — a new session reading only this file should understand the full 10-phase architecture without back-references.
> - Suggested sections: Philosophy · 10-phase pipeline (per-phase: purpose, draft/pro tiers, critic checkpoints, inputs, outputs) · Critic stack (full 3-tier table with cost/latency) · Draft→Pro coverage by phase · Character Bible primitive · Museum capture layer · Open questions reserved for future sessions (agent-fleet T2/T3 implementation, multimodal vault/RAG, museum format details).
>
> **3. Extend `manifest.yaml`** with additive, optional schema blocks.
>
> - New optional top-level blocks: `phases:`, `tiering:`, `critics:`, `characters:`, `museum:`, `brief:`
> - **Current `project:`, `anchor:`, `style:`, `generation:`, `act1:`, `audit:`, `export:` blocks stay completely intact.** Act 2 work in progress depends on them. The only allowed edit to existing fields is `project.name: "anima"` (project rename) — keep description as a sub-field if you want to preserve "Pencil Test — Sean Winslow" as the first reference implementation under the anima umbrella.
> - Each new block gets a short comment header explaining its purpose and pointing to `docs/pipeline-architecture-v1.md`.
> - Sensible defaults: `tiering.default_tier: draft`, `museum.publishing_target: sw-ai-pm-portfolio`, `critics.placement` mapping each of the 5 named checkpoints to a tier (`post_animatic: T3`, `per_frame_generate: [T1, T2]`, `post_motion: T2`, `post_assemble: T2`, `pre_museum_publish: T3`).
> - Schema extension only. Do not remove or restructure existing fields.
>
> **4. Add a CHANGELOG entry** dated 2026-05-25 covering commit 1 specifically (CLAUDE.md rewrite, new pipeline-architecture-v1.md, manifest schema extension). Append above the existing 2026-05-24 anima-lock entry. Match the existing format: `## YYYY-MM-DD — title` + **What changed:** paragraph + **Why:** paragraph + `---`.
>
> ### Acceptance criteria
>
> - Existing pencil-test workflows still run unchanged. Verify by reading the current `act1:` block end-to-end after the schema extension and confirming no existing field was touched (only `project.name` may change).
> - CLAUDE.md reads as studio-manual prose, not terminal-aesthetic.
> - `pipeline-architecture-v1.md` is self-contained — a new Claude session reading only that file understands the 10-phase architecture.
> - Critic stack and draft→pro principle each have their own named sections in both CLAUDE.md and pipeline-architecture-v1.md.
> - New manifest blocks have inline comment documentation pointing to pipeline-architecture-v1.md.
> - Source-of-truth table in CLAUDE.md points at the right docs in their new roles.
>
> ### Recommended approach
>
> 1. **Use plan mode first.** Shift+Tab twice to enter plan mode. Lay out the full edit plan before touching files. Surface any structural questions to Sean before proceeding.
> 2. Read the three binding docs (brainstorm, change-map, CHANGELOG top entry) and the current `CLAUDE.md` + `manifest.yaml` end-to-end. The rewrite should respect what's structurally working (source-of-truth tables, skills map, directory structure section, asset naming convention, generation chains, Seedance section, dependencies, engine truth) and replace what's outdated (project identity, 6-phase pipeline diagram, single-anchor primitive).
> 3. Draft in order: `CLAUDE.md` → `docs/pipeline-architecture-v1.md` → `manifest.yaml` extension → `CHANGELOG.md` entry.
> 4. After all four files draft, do one quality pass for voice consistency and cross-references.
> 5. Mark Task #4 complete at the end. The next task (Task #5 pressure-test) is for a separate session.
>
> ### Open task list (from prior session)
>
> The TaskCreate/TaskUpdate tools may not have carried task state across sessions. Recreate the task list at the start of this session:
>
> - **Task #4 — this session:** Draft pipeline-architecture-v1 spec + CLAUDE.md rewrite + manifest extension + CHANGELOG entry (commit 1)
> - Task #5 — pressure-test the architecture against template trap + over-engineering. Use a general-purpose subagent for an independent read. Separate session after #4 ships.
> - Task #6 — scaffold evals + traces workstream mirroring `code-brain/evals/vault-synthesizer/`. Defer until commit 3 (planner agent) work begins per change-map §7 sequencing.
>
> ### Important constraint
>
> **The architecture decisions are LOCKED.** Do not re-decide them. If you find a structural question that wasn't anticipated, surface it to Sean rather than deciding silently. Specifically locked:
>
> - Project name: `anima`
> - 10-phase pipeline shape (Phase 0 Brief & Plan → Phase 9 QA Review + orthogonal Museum)
> - 5 architectural ideas: Animatic Phase, Brief→Plan gate, Museum auto-capture, DAG refactor with content-hashed caching, Character Bible
> - 2 principles: Critic Stack T1/T2/T3 at 5 named checkpoints; Draft→Pro escalation across 7 of 10 phases
> - DAG library: hand-rolled minimal runner (~300-500 LOC, not Prefect/Dagster/Luigi)
> - Animatic format: Procreate Dreams + Procreate PNG sequences
> - Brief format: free-text markdown
> - Museum target: Astro content collection in `sw-ai-pm-portfolio`
> - Character Bible authoring: both consumed and authored, authoring-first as a Project-Type
> - Evals: mirror `code-brain/evals/vault-synthesizer/` pattern, intentionally-red baseline, per-agent suites gating each agent commit, bake-offs as first-class artifacts under `evals/bakeoffs/`
>
> If anything in the brainstorm or change-map seems wrong on fresh reading, flag it as a question — don't silently correct it.
>
> Start by entering plan mode and reading the binding docs. When the plan is ready, present it for Sean's approval before any edits.

---

## Why Claude Code over Cowork for this session

- **The CLAUDE.md being written is *for* Claude Code sessions** to auto-load. Better the author tool match the consumer tool.
- **Plan mode (Shift+Tab×2)** is the right structure for a 4-file, multi-section rewrite. Catches structural issues before the writing starts.
- **`.claude/skills/`** (including `writing-voice-modes` if installed) auto-loads in Claude Code. Tonal calibration matters here.
- **Multi-file editing** is faster and more precise in Claude Code with native diff tooling.
- **Git operations** (eventual commit for this work) are native to Claude Code.

Bring the next session back to Cowork if Task #5 (pressure-test) wants the multi-perspective brainstorm tooling — that's a Cowork-shaped task.

## What gets carried over

- Three binding docs already exist in the repo: brainstorm, change-map, CHANGELOG top entry
- `manifest.yaml` is currently in pencil-test shape; extension is additive
- `CLAUDE.md` is currently in pencil-test shape; rewrite preserves the structurally-working sections
- All architectural decisions are locked; no re-deciding

## What's deliberately left for later sessions

- Task #5 pressure-test (separate session, ideally with multi-perspective tooling)
- Task #6 evals scaffolding (lands with commit 3 per the change-map sequencing)
- Agent-fleet brainstorm (Claude SDK + Anti-Gravity + Codex topology, named roles inspired by OiiOii's 7-agent crew) — gates commits 8-9
- Multimodal vault/RAG brainstorm (Gemini Embedding 2 vs OpenRouter alternatives, Obsidian integration)
- Museum showcase format brainstorm
- Public GitHub repo creation + directory rename
