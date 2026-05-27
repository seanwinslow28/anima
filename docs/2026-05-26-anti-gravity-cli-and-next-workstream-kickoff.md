# Cowork Continuation Prompt — Anti-Gravity CLI + Next Workstream Selection

**Paste this into a fresh Cowork session on this machine.** The session needs read access to four folders (Sean will mount them at session start):

- `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/` — anima project root
- `/Users/seanwinslow/Code-Brain/code-brain/` — Sean's command center; reference for `vault_critic.py`, `llm-council`, `agents-sdk/` patterns, and the screenwriting-skill research notes
- `/Users/seanwinslow/Code-Brain/sw-ai-pm-portfolio/` — museum publishing target (Astro content collection)
- `/Users/seanwinslow/Code-Brain/sprite-sheet-automation-2026/` — anima's architectural ancestor; referenced in CLAUDE.md
- Anti-Gravity CLI installation directory — Sean will locate the binary somewhere under `/Users/seanwinslow/` and mount the parent folder so the session can read its docs, `--help` output, and any release notes shipped with the install

---

You're picking up the anima project mid-execution. anima is a reusable human + AI 2D animation production pipeline at `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/`. The architecture and agent fleet are locked in v2; Claude Code is currently executing the implementation. **Two things happened that this Cowork session needs to address.**

First, **commit 4 shipped locally on main** as `fcf28cd` — the DAG runner, `AgentSpec` Protocol, `acceptance_criteria.json` enforcement, content-addressed cache, hook system. 27/27 tests green. Commit 8 (Em vision critic) is being implemented now in a parallel Claude Code session. Commits 8b / 9 / 9b follow.

Second, **Google announced the Gemini CLI is being deprecated on 2026-06-18** and migrated to the Anti-Gravity CLI. URL: https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/. The v2 agent fleet wires Em's default model path (Gemini 3.1 Pro) and Annie's T3 peer voice through Anti-Gravity CLI. Sean has the new CLI installed but hasn't validated it against anima's specific call patterns. **This is time-sensitive because commit 9 ships the T3 stack that depends on Annie, and the deprecation date is ~3 weeks out.**

## Read these binding docs first, in this order

Philosophy before architecture before tactical brainstorm output. Don't skip ahead.

1. **`PHILOSOPHY.md`** — the load-bearing intent doc, ~750 words. Six load-bearing beliefs. Sean's quotes on tone (*"we're making art, it should feel free"*) and on the critic (*"a judge agent will be a staple in all of my agentic workflows from here on out"*) preserved verbatim. Both are load-bearing for this session.
2. **`CLAUDE.md`** — anima project manual, post-commit-1 (now reflects commit 4 shipped).
3. **`docs/2026-05-26-agent-fleet-brainstorm-v2.md`** — *the current architecture lock for the fleet*. v2 supersedes v1 (2026-05-25). Per-role table at §6, three structural patterns at §5, Phase 5 routing at §4, three open splits at §9, persona roster at §3.
4. **`docs/research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md`** — cross-source synthesis grounding v2's decisions. The chairman synthesis at §5 names the headline finding ("Character Designer is the missed pinnacle phase, not the third T3 voice"). Read for *why* each v2 assignment was made.
5. **`docs/research/2026-05-26-hermes-agent-deepseek-v4-flash-evaluation.md`** — the Hermes Agent / DeepSeek V4 Flash evaluation from 2026-05-26. Verdict: don't adopt Hermes as anima's orchestrator (portfolio thesis works against it; impedance with v2's typed contracts). Steal three patterns (agentskills.io spec, run-level MEMORY.md, gateway+plugin hook split). DeepSeek V4 Flash reserved as candidate fourth T3 peer for a post-implementation bake-off.
6. **`docs/pipeline-architecture-v1.md`** — canonical 10-phase architecture lock from 2026-05-25. Untouched by v2.
7. **`docs/Image-Model-DR-2026/SYNTHESIS.md`** — Phase 5 image-model routing source (Flo's table).
8. **`docs/2026-05-24-pipeline-v2-change-map.md`** — 9-commit sequence at §4. Commits 2, 3, 5, 6, 7 remain post-this-session.
9. **`CHANGELOG.md`** — recent entries (top six: 2026-05-26 v2 lands + Hermes evaluation + research-prompts; 2026-05-25 PHILOSOPHY.md + commit 1; 2026-05-24 architecture lock + Image-Model-DR synthesis).

Reference implementations to ground every contract against:

- **`/Users/seanwinslow/Code-Brain/code-brain/agents-sdk/agents/vault_critic.py`** — the T3 pattern. asyncio parallel subprocess fan-out, status promotion vocabulary, manual-mode bypass, standing-context preamble + supporting-doc injection.
- **`/Users/seanwinslow/Code-Brain/code-brain/agents-sdk/prompts/vault-critic-standing-context.md`** — the preamble pattern.
- **`/Users/seanwinslow/Code-Brain/code-brain/agents-sdk/config.toml`** lines 176–214 — supporting-doc injection via `default_context_files`.
- **`/Users/seanwinslow/Code-Brain/code-brain/tools/llm-council/`** — the chairman synthesis pattern.

## Working pattern

Sean brainstorms in Cowork (multi-perspective ideation, AskUserQuestion-driven decisions, structured artifact output), then executes in Claude Code (plan mode, multi-file edits, git). This session is a brainstorm half with a research preamble. End-of-session deliverables: (a) Anti-Gravity CLI findings doc, (b) a new brainstorm doc saved to `docs/` as a dated markdown artifact for the chosen workstream, and (c) a continuation prompt for the next Claude Code execution session (or for the next Cowork session if the chosen workstream is still in design phase). Mirrors how every prior handoff in this project has worked.

## Your job this session

Two phases. Phase 1 grounds the brainstorm in current reality; Phase 2 chooses the next workstream and runs the ideation pass.

### Phase 1 — Anti-Gravity CLI research + integration verification

**Goal.** Confirm what the v2 agent fleet's reliance on Anti-Gravity CLI actually means in practice, given the Gemini CLI → Anti-Gravity CLI migration Google announced. Sean's Anti-Gravity CLI is installed somewhere under `/Users/seanwinslow/`; the session has read access to it.

**Specific tasks.**

1. **Locate the Anti-Gravity CLI installation.** Use shell (`find /Users/seanwinslow -name 'anti-gravity*' -type f 2>/dev/null | head`, or check `/opt/`, `/usr/local/bin/`, `~/bin/`, `~/.local/bin/`). Report the binary path, version (`anti-gravity --version`), and any shipped docs (`README`, `docs/`, `man` pages).

2. **Map the CLI's surface.** Run `anti-gravity --help` and key subcommands. Document: authentication model (OAuth flow, API key, token path), model selection (does it expose Gemini 3.1 Pro by name, or a model-routing slug?), input modalities (image input format — file path, URL, base64?), output format (structured JSON, streaming, plain text?), timeout flags, retry behavior, error codes. Compare to the vault-critic-shaped subprocess pattern anima needs.

3. **Read Google's deprecation post** at https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/. Capture: migration deadline (confirm 2026-06-18), breaking changes between Gemini CLI and Anti-Gravity CLI, model availability changes (does Gemini 3.1 Pro stay accessible, or rebrand?), authentication migration steps, anything Sean needs to do on his Google personal OAuth to maintain access.

4. **Cross-reference against v2's wiring.** v2 wires Anti-Gravity CLI in two specific places:
   - **Em (T2 vision critic)** default model: `gemini-3.1-pro-via-anti-gravity`. Em accepts `(image_or_video_path, beat_description, style_guide, character_bible_sheets, anima_standing_context, role_addendum, acceptance_criteria)` and returns structured `{verdict, reasoning, prompt_diff, confidence, cites_criteria}`. Verify Anti-Gravity CLI accepts image input at anima's resolutions and emits structured output (or that a wrapper translation is straightforward).
   - **Annie (T3 peer)** via Anti-Gravity CLI for narrative/visual critique on animatic + museum walkthrough artifacts. Verify the same input/output shapes work for the T3 use case.
   - Confirm subscription absorption stays intact through the migration (the v2 cost ceiling rests on this).

5. **Document findings.** Save to `docs/research/2026-05-26-anti-gravity-cli-findings.md`. Cross-source synthesis style — mirror the structure of `docs/research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md` even though this is a single-source survey. Sections: (1) what changes from Gemini CLI to Anti-Gravity CLI; (2) anima's specific call patterns and whether they survive the migration unchanged; (3) anything commits 8 or 9 need to adapt; (4) timeline pressure (3 weeks to deprecation); (5) recommended action items before commit 9 implementation reaches the T3 stack.

6. **If breaking changes affect commit 9.** Flag explicitly in the findings doc. Either (a) propose a v2.0.1 patch to the implementation prompt with the corrected wiring, or (b) recommend Sean's next Claude Code session pause commit 9 until verification is complete. Don't silently absorb the breakage.

### Phase 2 — Run the brainstorm pass for the next Cowork workstream

**Goal.** Pick the next workstream the project should tackle, run `pm-product-discovery:brainstorm-ideas-existing` against it, and ship the brainstorm artifact + a continuation prompt (Claude Code or next Cowork, whichever fits).

**Candidate workstreams** — surface all six via `AskUserQuestion`, let Sean confirm or override.

- **A. Anti-Gravity CLI integration deep-dive** — if Phase 1 surfaces non-trivial migration work, this becomes the brainstorm topic. PM/Designer/Engineer pass on how to wire Em (commit 8) and Annie (commit 9) against the new CLI with the migration timeline pressure. Recommended if Phase 1 finds breaking changes.
- **B. Character Bible scaffolding (gates commit 2)** — Cy persona file + `character.yaml` schema details + authoring workflow + Sean-anchor PNG migration to `characters/sean-anchor/`. v2 ratified Cy = Opus 4.7 lead + Gemini 3.1 Pro visual verify + NB Pro generate, but the scaffolding shape hasn't been brainstormed. Smaller scope; one Cowork session covers it.
- **C. Maya planner brainstorm (gates commit 3)** — `acceptance_criteria.json` schema details, brief.md template format, cost-estimator algorithm, human-gate UX. The criteria-emission contract is the structural fix v2 named; this brainstorm makes it concrete.
- **D. Museum showcase format (gates commit 6)** — Mo persona + Astro content-collection MDX schema in `sw-ai-pm-portfolio` + comparison-GIF rendering pipeline + decision-ledger surfacing in walkthrough docs. The portfolio-positioning signal from v2 lives here.
- **E. Multimodal vault / RAG** — Gemini Embedding 2 vs OpenRouter, Obsidian integration, content-addressed asset store (ENG-5 from the original pipeline-v2 brainstorm). The Image-Model-DR-2026 SYNTHESIS already covered Phase 5 image-model routing; this is the retrieval-over-past-decisions question.
- **F. Pressure-test the locked architecture** — multi-perspective critique pass against v2. The kickoff Option A from 2026-05-25 that was deferred until commits 4 / 8 / 9 had real agents inside. By the time this Cowork session runs, commit 4 has shipped + commit 8 may also be done. Worth doing once shipped behavior exists to critique, but not while implementation is mid-flight.

**Recommended order.** If Phase 1 surfaces breaking changes → A. If Phase 1 is clean → B or C, whichever Sean prioritizes for the implementation backlog. D is right after E in priority because the museum is commit 6 (later in the sequence). F is post-implementation; do it once commits 8 / 9 ship.

**Brainstorm protocol** (per `pm-product-discovery:brainstorm-ideas-existing`):

- 5 ideas per perspective (PM / Designer / Engineer) = 15 minimum
- Anti-bias rotation pass after the initial 15 to pull suppressed-by-role ideas
- Converge on top 5 with: name + one-sentence description + selection rationale + assumptions to validate
- Save artifact as `docs/2026-05-MM-{workstream-slug}-brainstorm.md` matching the pattern of v1 + v2 brainstorm docs

**Continuation prompt** — at session end, draft `docs/2026-05-MM-{workstream-slug}-implementation-prompt.md` (or `-cowork-continuation-prompt.md` if the next step is another Cowork session). Mirror the structure of this file you're reading right now.

## Tonal directive (load-bearing)

Sean's exact words: *"I don't like it when the docs feel like it was strictly made for the terminal. We're making art. It should feel free."* Studio-manual voice, prose over tables where reasonable, no terminal-aesthetic. Applies to chat output and every artifact saved to disk.

## Constraints

- **v2's architecture decisions are LOCKED.** The synthesis ratified them, three structural patterns ship regardless of bake-off outcomes, and v2's per-role table has confidence scores from cross-source agreement. Don't re-decide them. If something seems wrong on fresh reading, flag it as a question — don't silently correct.
- **This is a brainstorm session, not implementation.** Don't touch `pipeline/*.py`, `pipeline/*.sh`, `manifest.yaml`, or anything that runs code. Doc artifacts and `docs/research/` files only.
- **Anti-Gravity CLI research is on-disk reading + `--help` invocation, not modification.** Don't reconfigure Sean's installation. Document state; don't change state.
- **End-of-session deliverables.** (1) `docs/research/2026-05-26-anti-gravity-cli-findings.md`, (2) brainstorm doc at `docs/2026-05-MM-{workstream-slug}-brainstorm.md`, (3) continuation prompt at `docs/2026-05-MM-{workstream-slug}-implementation-prompt.md` (or `-cowork-continuation-prompt.md`), (4) CHANGELOG entry covering both.
- **The pencil-test Act 2 work is still in flight.** Don't disturb it. Anti-Gravity CLI verification touches the binary's surface; it doesn't touch anima's runtime against Act 2 frames.

## Remaining work after this session (for context)

The post-commit-4 implementation backlog (per change-map §4 + v2 carry-overs):

- **Commit 2** — Character Bible migration + Cy persona. Independent of agent fleet; brainstorm pending (workstream B above).
- **Commit 3 + 3b** — Maya planner + evals/planner/. Depends on `acceptance_criteria.json` schema (already in commit 4); brainstorm pending (workstream C above).
- **Commit 5** — Draft → Pro tier escalation wired into the DAG runner. Depends on commit 4 (shipped).
- **Commit 6** — Museum capture layer + Mo persona + Astro content-collection integration. Brainstorm pending (workstream D above).
- **Commit 7** — Animatic ingestion (Procreate Dreams + Procreate PNG sequences).
- **Commit 8 + 8b** — Em vision critic + bake-off. In progress now in a parallel Claude Code session.
- **Commit 9 + 9b** — Codie + Annie + Sage + Chairman + bake-off. Depends on Phase 1 of this session resolving cleanly against Anti-Gravity CLI.

Post-implementation bake-offs from v2 §8:

1. T2 critic shoot-out (Gemini vs Sonnet vs Opus on 200-frame defect set) — resolves Open Q1.
2. Sage tier ablation (Opus vs Sonnet, chairman held constant) — resolves Open Q2.
3. Planner downgrade ablation (Opus → Sonnet after first short).
4. Orchestrator drift test (Sonnet for 20 pieces, restart-rate measurement).
5. Storyboard three-way (Sonnet vs Gemini vs Codex) — resolves Open Q3.
6. (New, from Hermes evaluation) DeepSeek V4 Flash as candidate fourth T3 peer voice — Open Q7.

## Start

Begin by reading the binding docs in the listed order. Then run Phase 1 in this sequence:

1. `find /Users/seanwinslow -name 'anti-gravity*' -type f 2>/dev/null | head` plus the equivalent `find` for `antigravity*` (the rebrand may have changed the binary name). Report what you find.
2. `<found-binary> --version` and `<found-binary> --help`. Capture the surface.
3. WebFetch https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/. Read the deprecation post.
4. Cross-reference against v2's `t2.default_model: gemini-3.1-pro-via-anti-gravity` and Annie's T3 wiring. Identify any breaking changes.
5. Write `docs/research/2026-05-26-anti-gravity-cli-findings.md`.

Then enter Phase 2: use `AskUserQuestion` to confirm which workstream is next (recommend A if Phase 1 found breakage; recommend B or C otherwise — Sean's call). Run `pm-product-discovery:brainstorm-ideas-existing` on the chosen workstream. Save the brainstorm doc + the continuation prompt. Append a CHANGELOG entry. Present all artifacts via `mcp__cowork__present_files`.

Net wall-clock estimate: 60–90 minutes for Phase 1, 30–45 minutes for Phase 2's brainstorm + artifact writes. Phase 1 may compress significantly if Anti-Gravity CLI is a clean drop-in for Gemini CLI; may extend if breaking changes need a v2.0.1 patch design.

---

*Last updated 2026-05-26. This prompt is the bridge between commit 4 (shipped) and the next architectural decision the agent fleet is going to need. Phase 1 protects the commit-9 timeline; Phase 2 keeps the design pipeline ahead of the implementation pipeline.*
