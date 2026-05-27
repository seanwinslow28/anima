# Continuation Prompt — anima Next-Step Brainstorm (Cowork Session)

**For:** Fresh Claude Cowork session, 2026-05-26 (or whenever Sean picks this up)
**Recommended environment:** Cowork (brainstorm half of the workflow; Claude Code is the implementation half)
**Source sessions:**
- 2026-05-24 — Cowork brainstorm + change-map + architecture lock
- 2026-05-25 — Claude Code execution of commit 1 (CLAUDE.md rewrite + pipeline-architecture-v1 spec + manifest extension + CHANGELOG entry)

---

## How to use

Open a fresh Cowork session with access to these folders:

- `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/` — the anima project itself
- `/Users/seanwinslow/Code-Brain/code-brain/` — reference for evals/vault-synthesizer pattern, agents-sdk patterns, vault-critic CLI pattern, LLM Council
- `/Users/seanwinslow/Code-Brain/sw-ai-pm-portfolio/` — the museum publishing target
- `/Users/seanwinslow/Code-Brain/sprite-sheet-automation-2026/` — older sister project, architectural ancestor

Then paste the prompt block below into chat. The new session has zero memory of prior conversations; the prompt is self-contained.

---

## Prompt to paste

> You're picking up the anima project mid-execution. anima is a reusable human+AI 2D animation production pipeline at `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/`. The 2026-05-24 Cowork session produced a brainstorm + change-map locking the v2 architecture (project rename from "sw-portfolio-animation-pipeline" to "anima", 10 phases up from 6, 2 promoted principles, 9-commit sequence). The 2026-05-25 Claude Code session executed commit 1 — doc-only foundation — landing the CLAUDE.md rewrite + new `docs/pipeline-architecture-v1.md` + `manifest.yaml` schema extensions + CHANGELOG entry. Those files are on disk; Sean may or may not have committed them to git yet.
>
> ### Read these binding docs first before acting
>
> In this order:
>
> 1. `CLAUDE.md` — the anima project manual, fresh from commit 1. Your primary orientation.
> 2. `docs/pipeline-architecture-v1.md` — canonical 10-phase architecture lock document.
> 3. `docs/2026-05-24-pipeline-v2-brainstorm.md` — 15-idea brainstorm output, 5 architectural decisions locked, 2 principles locked, all 6 open questions resolved at §8.
> 4. `docs/2026-05-24-pipeline-v2-change-map.md` — 9-commit sequence at §4, DAG library rationale at §6, evals workstream scope at §7.
> 5. `CHANGELOG.md` — top two entries (2026-05-25 commit-1 + 2026-05-24 anima-lock).
>
> ### Working pattern
>
> Sean brainstorms in Cowork (multi-perspective ideation, AskUserQuestion-driven decisions, structured artifact output), then executes in Claude Code (plan mode, multi-file edits, git). **This session is the brainstorm half.** Your end-of-session deliverable is twofold: (a) a brainstorm doc saved to `docs/` as a dated markdown artifact, and (b) a continuation prompt for the next Claude Code execution session that picks up the implementation work. Mirrors how the 2026-05-24 → 2026-05-25 handoff worked.
>
> ### Your job this session
>
> Two phases.
>
> #### Phase 1 — Converge on which workstream is next
>
> Five candidates surfaced from the prior sessions. Use the AskUserQuestion tool to let Sean confirm which one is the focus of this session.
>
> **A. Pressure-test the locked architecture (Task #5).** Use multi-perspective critique to find what we missed before any more building. Independent read on whether the architecture drifts toward generic "AI pipeline" template, over-engineers for a solo workflow, or has hidden coupling. Verification gate. One-session work.
>
> **B. Agent fleet brainstorm (recommended).** The biggest deferred topic. Decides T2 vision critic + T3 multi-CLI critic implementations, plus the broader question of named agent roles (Director, Character Designer, Storyboard Artist, etc.) vs orchestrator + tools. References to bake against:
> - OiiOii's 7-agent crew (Art Director, Scriptwriter, IP Designer, Character Designer, Scene Designer, Storyboard Artist, Sound Director)
> - Higgsfield Supercomputer's 1 orchestrator + 30 model routes
> - Krea Node Agent's DAG + 1 planner
> - Sean's existing vault-critic pattern in code-brain (`/Users/seanwinslow/Code-Brain/code-brain/agents-sdk/agents/vault_critic.py` — Codex CLI + Anti-Gravity CLI parallel critique, $0 incremental on subscriptions, with standing-context preamble pattern at `agents-sdk/prompts/vault-critic-standing-context.md`)
> - Sean's LLM Council pattern in code-brain (`tools/llm-council/council/` — two profiles: premium 4-model Opus chairman ~$0.29/run, variance 4-model Sonnet chairman ~$0.14/run)
>
> Unblocks commits 8-9 in the 9-commit sequence. Rich enough that brainstorm-ideas-existing earns its keep.
>
> **C. Character Bible scaffolding brainstorm.** Smaller scope than agent fleet. Defines the `characters/sean-anchor/` migration from the single anchor PNG, the `character.yaml` schema, the turnarounds/expressions/costumes folder conventions, sample sheet authoring workflow. Unblocks commit 2.
>
> **D. Multimodal vault / RAG brainstorm.** The Gemini Embedding 2 vs OpenRouter question, Obsidian vault integration for semantic retrieval across past frames/characters/decisions. Reference URLs Sean cited in the original kickoff:
> - https://ai.google.dev/gemini-api/docs/models/gemini-embedding-2
> - https://developers.googleblog.com/building-with-gemini-embedding-2/
> - https://openrouter.ai/models?output_modalities=embeddings
>
> May be premature without seeing what the pipeline actually needs in production. Worth surfacing as an option anyway.
>
> **E. Museum showcase format brainstorm.** The Astro content-collection integration with `/Users/seanwinslow/Code-Brain/sw-ai-pm-portfolio/`. Defines what an anima production's museum walkthrough looks like as a public artifact — comparison-GIF format, decision-ledger rendering, narrative structure, before/after presentation. Less urgent because Museum is commit 6 in the sequence, but informs how capture hooks should write (which lands earlier).
>
> **Recommended pick: B (Agent fleet).** Biggest deferred topic, explicitly named "next session" in both binding docs, unblocks the critic implementation that Sean elevated to a staple in his agentic workflows, and gates 2 of the remaining 8 commits. Use AskUserQuestion to let Sean confirm or override. Show all 5 options.
>
> #### Phase 2 — Run the chosen brainstorm
>
> Invoke `/pm-product-discovery:brainstorm-ideas-existing` on the chosen workstream. Full PM/Designer/Engineer ideation pass with anti-bias rotation. Aim for 15+ ideas before converging on top 5. Each top-5 entry gets a clear name, one-sentence description, selection reasoning, and key assumptions to validate. Save the output as a dated markdown artifact in `docs/` matching the pattern: `2026-MM-DD-{workstream-name}-brainstorm.md`.
>
> If Sean picks **B (Agent fleet)**, scope the brainstorm around these specific questions:
>
> - **Topology shape:** OiiOii's 7-agent crew vs Higgsfield's 1-orchestrator-many-routes vs Krea's DAG-with-planner. Which fits anima's solo-creator scale and the 10-phase architecture?
> - **T2 vision critic implementation:** Which model handles vision critique at the Generate / Motion / Assemble checkpoints? Claude Sonnet 4.6 vs Gemini 3 Pro vs something else. Single model or ensemble?
> - **T3 multi-CLI critic wiring:** How do Codex CLI + Anti-Gravity CLI wire into the pipeline runner for the Animatic→Generate and pre-Museum-publish checkpoints? Standing-context preamble pattern (mirroring vault-critic)?
> - **Named agents beyond critics:** Does anima need a Planner agent (Phase 0)? A Character Designer agent (Phase 2 bible authoring)? A Storyboard Artist agent (Phase 3)? Or keep it minimal — one orchestrator + critic tier — and let Sean play the missing roles?
> - **Skill packaging:** Each agent gets its own skill in `.claude/skills/` (like how `seedance-prompting` was extracted), or stays internal to anima?
> - **Cost discipline:** What spend caps, daily limits, monthly limits per agent? (vault-critic = $0 subscription-absorbed; vault-synthesizer = local Qwen3-14B $0/run; LLM Council premium = ~$0.29/run, cap $1.00/query.)
>
> If Sean picks any of A / C / D / E, scope the brainstorm appropriately and reference the existing patterns in `/Users/seanwinslow/Code-Brain/code-brain/` for inspiration.
>
> ### Tonal directive (load-bearing)
>
> Sean's exact words from the prior session: *"I don't like it when the docs feel like it was strictly made for the terminal. We're making art. It should feel free."* Studio-manual voice, prose over tables where reasonable, no terminal-aesthetic. Applies to your chat output and the brainstorm doc you produce.
>
> ### Constraints
>
> - The architecture decisions from 2026-05-24 are LOCKED. Don't re-decide them. If something seems wrong on fresh reading, flag it as a question — don't silently correct it.
> - This is a brainstorm session, not implementation. Don't touch `pipeline/*.py`, `pipeline/*.sh`, or anything that runs code. Doc artifacts only.
> - End-of-session deliverable: (1) brainstorm doc at `docs/2026-MM-DD-{workstream}-brainstorm.md`, (2) continuation prompt for next Claude Code session at `docs/2026-MM-DD-{workstream}-implementation-prompt.md`. Match the pattern of the prior 2026-05-24 / 2026-05-25 artifact pair.
>
> ### Remaining work after this session (for context)
>
> From change-map §4 + new tasks:
>
> - Task #5 — pressure-test (separate session if not done this session)
> - Commit 2 — Character Bible migration
> - Commit 3 — Brief→Plan planner wrapper (+ Commit 3b evals scaffold)
> - Commit 4 — DAG runner refactor (foundational; gates everything downstream)
> - Commit 5 — Draft→Pro tier escalation in DAG
> - Commit 6 — Museum capture layer
> - Commit 7 — Animatic ingestion
> - Commit 8 — T2 vision critic (+ Commit 8b evals + bake-off) — depends on agent-fleet brainstorm
> - Commit 9 — T3 multi-CLI critic (+ Commit 9b evals) — depends on agent-fleet brainstorm
>
> Brainstorms that should happen along the way: agent fleet (gates 8-9), multimodal vault/RAG, museum format (informs commit 6).
>
> ### Start
>
> Begin by reading the five binding docs. Then use AskUserQuestion to confirm which of the 5 workstreams is the focus of this session (recommend B but let Sean override). Then invoke `/pm-product-discovery:brainstorm-ideas-existing` and run the full ideation pass. Save artifacts at the end.

---

## Why Cowork over Claude Code for this session

- **Brainstorm tooling.** The `pm-product-discovery:brainstorm-ideas-existing` skill is the prior session's proven workflow for multi-perspective ideation. Cowork is its native habitat.
- **AskUserQuestion for the workstream decision.** Phase 1 is a structured decision among 5 options — exactly what AskUserQuestion is for.
- **Cross-project read.** This session benefits from reading `code-brain/agents-sdk/`, `code-brain/tools/llm-council/`, and `code-brain/evals/vault-synthesizer/` as references. Cowork's mounted folder model handles this cleanly.
- **No git work needed.** Cowork doesn't have native git integration but this session is doc-only — no commits, no branches, no diffs.

Bring it back to Claude Code for the implementation half (whichever commit follows from the chosen brainstorm).

## Folders this session needs access to

| Folder | Purpose |
|---|---|
| `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/` | The anima project itself (read + write) |
| `/Users/seanwinslow/Code-Brain/code-brain/` | Reference for vault-critic, LLM Council, evals/vault-synthesizer, agents-sdk patterns (read-only) |
| `/Users/seanwinslow/Code-Brain/sw-ai-pm-portfolio/` | Museum publishing target — Astro content-collection schema, voice-modes reference (read-only) |
| `/Users/seanwinslow/Code-Brain/sprite-sheet-automation-2026/` | Architectural ancestor — original manifest-driven pipeline design (read-only, optional) |

## What this session produces

Two artifacts, matching the 2026-05-24 / 2026-05-25 pattern:

1. **`docs/2026-MM-DD-{workstream}-brainstorm.md`** — the brainstorm output (15+ ideas → top 5 prioritized → key assumptions to validate → open questions)
2. **`docs/2026-MM-DD-{workstream}-implementation-prompt.md`** — the continuation prompt for the next Claude Code session to execute against

Plus a CHANGELOG entry capturing the session's locked decisions.
