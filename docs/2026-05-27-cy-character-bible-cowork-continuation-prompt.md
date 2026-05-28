# Cowork Continuation Prompt — Cy the Character Designer Brainstorm

**Created:** 2026-05-27
**For:** A fresh Cowork session that picks up commit 2 (Character Bible + Cy persona) — workstream B from the 2026-05-26 Cowork brainstorm options.
**Reads as:** Studio-manual voice, prose where reasonable. Sean's tonal directive — *"we're making art. It should feel free."*

---

You're picking up the anima project mid-execution. anima is a reusable human + AI 2D animation production pipeline at `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/`. The architecture and agent fleet are locked in v2; Claude Code is actively building the implementation. Three things happened that this Cowork session needs to address.

First, **commits 8 + 8.1 + 8.1a + 3 + 3b all shipped** on a feature branch `feature/maya-planner-and-em-live` (13 commits since `8fd0ca2`). Em (T2 vision critic) talks to real Gemini 3.1 Pro via the corrected `agy --dangerously-skip-permissions --add-dir <parent> -p ...` incantation — verified at 27.4s per Act 1 F06 keyframe at confidence 1.0 with concrete pencil-test-aesthetic critique. Maya (Phase 0 planner) shipped with the three-phase Opus-primary → Sonnet-adversarial → resolution loop, the v1.1 graph-shaped `acceptance_criteria.json` schema, the `CostEstimatorNode` AgentSpec, the ASCII-boxes-in-renderer / clean-markdown-on-disk split for `pipeline plan show`, and the audited mutation contract. The `.venv` picked up `claude-agent-sdk` v0.2.87 + `anthropic` v0.104.1; the `sdk_runners.py` wrapper got refactored against the actual claude-agent-sdk v0.2.x API (the original commit-8 version had been written against speculation that would have raised TypeError on every real invocation). Test suite stands at 90 green + 5 passing / 1 xfailed in `evals/planner/`. Maya's Opus + Sonnet paths verified live (6.8s + 4.5s respectively). The contract layer is now real all the way down.

Second, **commit 2 — Character Bible migration + Cy persona — is the next implementation gate**, and the v2 brainstorm explicitly named it as needing its own brainstorm pass before code lands. Per the cross-source synthesis at `docs/research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md` §5: *"Sean is about to spend his unlocked Opus budget on a third T3 peer voice and stop there. That's a real upgrade, but it isn't the pinnacle. Three of four council members independently identified Character Designer (Phase 2) as the under-recognized Opus seat. The Bible is the cross-phase invariant; every one of his 10-50 T2 vision critiques is implicitly evaluating against it. A Sonnet-authored Bible looks complete and silently fails to constrain — turnarounds won't actually pin the front pose, the expression sheet will blur tonally. Validators cannot recover taste that was absent at generation time."* That's the headline. Cy is the highest-confidence non-Chairman role in v2's per-role table (92%) precisely because the council converged on this finding from independent angles. The Bible is the structural fix at the source.

Third, **the input material already exists.** Sean committed seven character-reference images under `images/NEW-ANIMATION-PIPELINE/` that look like Cy's first real run inputs: `anchor-1.png`, `Original-Headturn.png`, `Original-Walk-Cycle.png`, `sean-character-turnaround-2.png`, `sean-head-turn-1.png`, `sean-walk-cycle.png`, `sean-walk-cycle-2.png`. The existing pencil-test anchor at `images/2D-Character-Sketch-Sean-v1.png` is the v1 single-anchor reference that needs migrating to `characters/sean-anchor/anchor.png` with a back-compat symlink. There are additional character-adjacent folders worth examining: `images/Claude-Mascot/`, `images/Sprite-reference/`, `images/3D-Character-Reference-Test/`, `images/head-turn/`, and `references/visual-guides/`. The Bible authoring brainstorm should consider what's already on disk before designing the schema.

## Read these binding docs first, in this order

Philosophy before architecture before tactical brainstorm output. Don't skip ahead.

1. [`PHILOSOPHY.md`](PHILOSOPHY.md) — the load-bearing intent doc, six load-bearing beliefs. Sean's quotes on tone (*"we're making art, it should feel free"*) and on the critic (*"a judge agent will be a staple in all of my agentic workflows from here on out"*) preserved verbatim. Both load-bearing for this session.
2. [`CLAUDE.md`](CLAUDE.md) — anima project manual, current state post-commits 3 + 3b + 8.1a.
3. [`docs/2026-05-26-agent-fleet-brainstorm-v2.md`](docs/2026-05-26-agent-fleet-brainstorm-v2.md) — the v2 architecture lock. Critical sections for Cy: §2.1 (Character Designer as the headline finding — "the missed pinnacle phase"), §3 (persona roster with Cy's model assignment), §6 (per-role table with Cy at 92% confidence — highest non-Chairman), §11 (architecture-implied strawman with Phase 2 wiring).
4. [`docs/research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md`](docs/research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md) — cross-source synthesis grounding v2's decisions. §5 names Cy as the single most important decision Sean was about to get wrong if he shipped v1. Read for *why* the Bible-as-cross-phase-invariant thesis earned the headline.
5. [`docs/Image-Model-DR-2026/SYNTHESIS.md`](docs/Image-Model-DR-2026/SYNTHESIS.md) — Phase 5 image-model routing source. NB Pro for hero shots is named explicitly; Cy uses NB Pro for Bible generation per v2 §6.
6. [`docs/pipeline-architecture-v1.md`](docs/pipeline-architecture-v1.md) — canonical 10-phase architecture lock. Phase 2 spec.
7. [`docs/2026-05-24-pipeline-v2-change-map.md`](docs/2026-05-24-pipeline-v2-change-map.md) §2 TOP-5 (Character Bible migration scope, M effort, change-map's original sketch of the `characters/{character_id}/` shape) + §4 (Commit 2 in the sequence — independent of DAG, low-risk, immediately useful for any new character work).
8. [`docs/2026-05-26-maya-planner-brainstorm.md`](docs/2026-05-26-maya-planner-brainstorm.md) — the brainstorm artifact that just shipped. Read for the *shape* of how a brainstorm landed: 20 ideas across PM / Designer / Engineer + anti-bias rotation pass, converged top-5 with selection rationale + assumptions to validate, deferred items with promotion triggers. This session's output should follow the same shape.
9. [`docs/2026-05-26-maya-planner-implementation-prompt.md`](docs/2026-05-26-maya-planner-implementation-prompt.md) — the implementation prompt that landed commit 3 cleanly. Read for the *handoff format* the Cy implementation prompt will follow at end of session.
10. [`docs/research/2026-05-26-anti-gravity-cli-findings.md`](docs/research/2026-05-26-anti-gravity-cli-findings.md) — Antigravity CLI findings doc with the verification addendum. Cy's visual-verification path uses Gemini 3.1 Pro via the same `agy` wrapper Em uses; the corrected flag shape applies directly.
11. [`CHANGELOG.md`](CHANGELOG.md) — recent entries (top of the file).
12. [`PORTFOLIO-GOLD.md`](PORTFOLIO-GOLD.md) — Sean's private portfolio-grade-moments ledger. Gitignored; read for the verification-addendum pattern (which Cy's brainstorm should be ready to apply if its own speculation gets contradicted by reality).

## Reference implementations to ground every contract against

* `pipeline/agents/planner.py` — Maya's three-phase loop (Opus primary → Sonnet adversarial → resolution). Cy's authoring half follows a similar shape (Opus authors identity rules; Gemini verifies generated assets; possibly a Sonnet adversarial sweep on the rules).
* `pipeline/agents/vision_critic.py` — Em's visual critique with structured JSON output + cites_criteria invariant. Cy's verification half is structurally adjacent — Cy reads a generated turnaround/expression and emits a structured verdict against the Bible's identity rules.
* `pipeline/agents/cli_runners.py` — the corrected `agy` wrapper. Cy's Gemini visual-verify path inherits the working incantation directly.
* `pipeline/agents/sdk_runners.py` — `invoke_opus_text` / `invoke_opus_vision` / `invoke_sonnet_text` / `invoke_sonnet_vision` (latter to confirm exists). Cy needs `invoke_opus_vision` for the authoring half if she reads input references; `invoke_opus_text` if she emits identity rules from prose alone.
* `pipeline/criteria.py` — the v1.1 graph-shaped `acceptance_criteria.json` schema. Cy's identity rules may extend the graph as `AC.identity.*` nodes — that's a brainstorm decision.
* `pipeline/agents/prompts/anima-standing-context.md` + `pipeline/agents/prompts/em-vision-critic-context.md` + `pipeline/agents/prompts/maya-planner-context.md` — the standing-context preamble pattern. Cy gets her own role addendum in the same shape.
* `pipeline/cli/plan.py` — Maya's `plan init / show / approve / mutate` subcommand template. Cy may want an analogous `bible init / show / approve / mutate` surface.
* `images/2D-Character-Sketch-Sean-v1.png` — the existing v1 single-anchor reference.
* `images/NEW-ANIMATION-PIPELINE/` — the input material Sean committed; Cy's first real run will likely consume these.

## Working pattern

Sean uses `/pm-product-discovery:brainstorm-ideas-existing` in Cowork (multi-perspective ideation, AskUserQuestion-driven decisions, structured artifact output), then executes in Claude Code (plan mode, multi-file edits, git). This Cowork session is a single-phase brainstorm — no time-pressure preamble like the Antigravity CLI migration from the previous session. End-of-session deliverables: (a) a new brainstorm doc saved to `docs/` as a dated markdown artifact for Cy, and (b) a continuation prompt for the next Claude Code execution session that mirrors the structure of `docs/2026-05-26-maya-planner-implementation-prompt.md`.

## Your job this session

A single phase. Brainstorm Cy and ship the artifacts.

### Phase 1 — Survey the input material (15 minutes)

Before the brainstorm proper, audit what's already on disk so the design pass references reality, not speculation. The change-map's TOP-5 sketch of the `characters/{character_id}/` shape (anchor, turnarounds, expressions, costumes, props, character.yaml) was written before Sean's input material landed; the brainstorm should ground against what's actually committed.

**Tasks.**
1. List `images/NEW-ANIMATION-PIPELINE/` and read filenames. Open any whose role isn't obvious from the name.
2. List the adjacent reference folders: `images/Claude-Mascot/`, `images/Sprite-reference/`, `images/3D-Character-Reference-Test/`, `images/head-turn/`, `references/visual-guides/`. Note which are Sean-character-specific vs. cross-character reference material.
3. Read the existing pencil-test anchor at `images/2D-Character-Sketch-Sean-v1.png` (the v1 single-anchor that needs migrating).
4. Identify any character-reference material that doesn't fit the v1 sketch's folder shape (anchor / turnarounds / expressions / costumes / props) — Sean's walk cycles, head turns, and "Original-*" naming suggest the Bible may need a sixth sub-folder (motion references? source/derived split?). Flag for the brainstorm.

### Phase 2 — Run the brainstorm pass for Cy (45 minutes)

Invoke `pm-product-discovery:brainstorm-ideas-existing` against Cy.

**Topic framing for the brainstorm.** Cy is anima's Character Designer. v2 locks the model assignment (Opus 4.7 authors identity rules + Gemini 3.1 Pro visually verifies generated assets + NB Pro produces images per Phase 5 routing). What's open for the brainstorm:

* **The `characters/{character_id}/` folder structure** — anchor / turnarounds / expressions / costumes / props was the v1 sketch; does Sean's actual input material want a different shape? Motion references (walk cycles, head turns) don't fit cleanly into the v1 sub-folders.
* **The `character.yaml` schema** — palette, proportions, identity-drift triggers, the closed vocabulary for trigger types. How does Cy emit it? What does Em read from it during T2 verification?
* **The Bible-authoring workflow** — Cy-leads-with-Sean-review vs Sean-leads-with-Cy-assist vs hybrid. How does the brief connect to Cy (does Maya's `00_studio_brief.md` seed Cy's identity-rule authoring, or does Cy consume a separate `02_character_brief.md`)?
* **The migration from `images/2D-Character-Sketch-Sean-v1.png` → `characters/sean-anchor/anchor.png`** — symlink for back-compat through which commits? When does the symlink come down?
* **Cy as Project-Type** — Sean's Open Q6 from v1: does Cy support Bible *authoring* as a project type (the pipeline produces the Bible) or only Bible *consuming* (the pipeline reads a hand-authored Bible)? v2 §10's "Open Q6 — Bibles authored vs consumed" deferred this; commit 2 may want to resolve it.
* **How Cy's identity rules connect to `acceptance_criteria.json`** — does Cy emit `AC.identity.*` nodes into the existing graph, or does she emit a separate `identity_rules.json` that Em loads alongside the criteria? The synthesis names "validators cannot recover taste that was absent at generation time" — Cy's emission shape is how that taste enters the contract layer.
* **The verification half** — when Cy generates a turnaround via NB Pro, what's the verification loop? Does Gemini 3.1 Pro emit a structured `{verdict, reasoning, confidence, cites_identity_rule}` envelope (mirroring Em's contract)? Is there a Cy-specific impact_tag vocabulary (`identity_critical / proportion_critical / pose_critical / style_critical`)?
* **Multi-character pieces** — the v1 sketch assumed `characters/{character_id}/` per character; does anything cross-character (shared palette? shared style?) live higher up? Where do supporting characters (Claude Mascot if it appears in a piece) get their own folders vs reuse Sean's?

**Brainstorm protocol** (per the skill, mirroring the Maya session):
- 5 ideas per perspective (PM / Designer / Engineer) = 15 minimum
- Anti-bias rotation pass after the initial 15 to pull suppressed-by-role ideas
- Converge on top 5 with: name + one-sentence description + selection rationale + assumptions to validate
- Save artifact as `docs/2026-05-DD-cy-character-bible-brainstorm.md` matching the pattern of the Maya brainstorm verbatim

### Phase 3 — Draft the implementation prompt (15 minutes)

At session end, write `docs/2026-05-DD-cy-character-bible-implementation-prompt.md` mirroring the structure of `docs/2026-05-26-maya-planner-implementation-prompt.md`. Three-phase work plan: any small warmup (likely the sean-anchor migration with the symlink), the commit 2 main event, the commit 2b eval suite (Cy emits identity rules; commit 2b's eval verifies that Em can cite them during a T2 critique — the closing-the-loop test).

### Phase 4 — CHANGELOG entry + artifact presentation (10 minutes)

Append a CHANGELOG entry covering the brainstorm + implementation prompt. Present all artifacts via `mcp__cowork__present_files`. Update `PORTFOLIO-GOLD.md` if anything in this session has portfolio-grade-moment shape (the brainstorm doc itself might qualify if it produces a structural insight worth pointing at later — Sean's call).

## Tonal directive (load-bearing)

Sean's exact words: *"I don't like it when the docs feel like it was strictly made for the terminal. We're making art. It should feel free."* Studio-manual voice, prose over tables where reasonable, no terminal-aesthetic. Applies to chat output and every artifact saved to disk.

The Maya brainstorm at `docs/2026-05-26-maya-planner-brainstorm.md` is the calibrated example of this voice — match its register.

## Constraints

* **v2's architecture decisions are LOCKED.** Cy's model assignment (Opus 4.7 authors + Gemini 3.1 Pro visually verifies + NB Pro generates) is 92% confidence — *not for redecision*. The brainstorm decides workflow, schema, folder structure, and integration shape; it does not re-tier Cy's models.
* **This is a brainstorm session, not implementation.** Don't touch `pipeline/*.py`, `pipeline/*.sh`, `manifest.yaml`, or anything that runs code. Doc artifacts only. The implementation prompt is for the *next* Claude Code session.
* **The pencil-test Act 2 work is still in flight.** The existing `images/2D-Character-Sketch-Sean-v1.png` must keep working through whatever back-compat window the brainstorm decides. The migration to `characters/sean-anchor/anchor.png` is part of commit 2; the symlink convention is the design knob.
* **No new commits during this session.** All work is on disk in `docs/`; commits land in the implementation session that follows.
* **Mirror, don't reinvent.** The Maya brainstorm + implementation prompt are the templates. Brief and to the point. Studio voice throughout.

## End-of-session deliverables

1. `docs/2026-05-DD-cy-character-bible-brainstorm.md` — the brainstorm artifact (20 ideas + anti-bias rotation + top 5 + deferred items)
2. `docs/2026-05-DD-cy-character-bible-implementation-prompt.md` — the paste-ready continuation prompt for the next Claude Code execution session
3. CHANGELOG entry covering both
4. Optional: a new `PORTFOLIO-GOLD.md` entry if the session produces a portfolio-grade moment (e.g., a structural insight about Bible authoring that's transferable beyond anima)
5. All artifacts presented via `mcp__cowork__present_files`

## Remaining work after this session (for context)

The post-commit-3 implementation backlog:

* **Commit 2 + 2b** — Cy + Character Bible + eval suite. This session designs it; the next Claude Code session implements it.
* **Commit 9 + 9b** — Codie + Annie + Sage + Chairman at T3 + eval suite. Annie's wrapper inherits commit 8.1a's `agy` flag shape directly. Three of four T3 surfaces (Codie/Sage/Chairman) are migration-free.
* **Commit 5** — Draft → Pro tier escalation wired into the DAG runner. Unblocked by commit 3's CostEstimatorNode (shipped).
* **Commit 6 + Mo persona** — Museum capture layer + Astro content-collection in `sw-ai-pm-portfolio`. Workstream D from the 2026-05-26 options; pending its own brainstorm.
* **Commit 7** — Animatic ingestion (Procreate Dreams + Procreate PNG sequences).
* **First real Maya planning run** — once Cy authors the Bible (or before, against the pencil-test reference), Maya plans a real piece. Portfolio-grade first Phase 0 ceremony.

Post-implementation bake-offs (from v2 §8) — not gating commit 2, but informing future tuning:

1. T2 critic shoot-out (Gemini vs Sonnet vs Opus on 200-frame defect set)
2. Sage tier ablation
3. Planner downgrade ablation
4. Orchestrator drift test
5. Storyboard three-way
6. DeepSeek V4 Flash as candidate fourth T3 peer (from the Hermes evaluation)

## Start

1. Read the binding docs in the listed order.
2. Phase 1 — survey the input material at `images/NEW-ANIMATION-PIPELINE/` and the adjacent reference folders. ~15 minutes.
3. Phase 2 — invoke `/pm-product-discovery:brainstorm-ideas-existing` against Cy. ~45 minutes. Use `AskUserQuestion` for any cross-decision that splits two ways — workflow choice, migration timing, Cy-as-Project-Type resolution.
4. Phase 3 — draft the implementation prompt mirroring Maya's. ~15 minutes.
5. Phase 4 — CHANGELOG + present artifacts. ~10 minutes.

Net wall-clock estimate: 60–90 minutes for the brainstorm + artifact writes.

---

*The Bible is the cross-phase invariant. Cy is how taste enters the contract layer before generation, not after. This session designs the shape.*
