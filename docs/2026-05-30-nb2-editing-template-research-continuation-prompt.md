# Continuation prompt — NB2 editing-mode template research (fresh Cowork session)

*Paste everything below the divider into a fresh Cowork session. It's self-contained: the new session has zero memory of the prior conversation. Goal: extensive research on Nano Banana 2's **editing** capabilities for character consistency, distilled into a register-agnostic, plug-and-play prompt template for Cy (Bible authoring) and future storyboarding — then wired into the existing Claude Code kickoff. Context-safety: this is research-heavy, so delegate the web sweeps to subagents/skills and keep your main thread lean.*

---

You are working on **anima**, a reusable pipeline for 2D animation made by a human and a fleet of agents, located at `/Users/seanwinslow/Code-Brain/anima` (you have folder access). Your job this session is research + synthesis + planning — **no production code changes**. You will produce a register-agnostic Nano Banana 2 editing-prompt template and fold it into an existing implementation kickoff. The human is Sean — a PM, comfortable with code, who wants the "why" and dislikes terminal-flavored docs (studio-manual voice, prose over bullet-dumps).

## The mandate, in one paragraph

Cy (anima's character-designer agent) generates character Bible plates — turnarounds, expressions, poses — by calling an image model with reference images + a text prompt. The current prompting is tuned ad hoc and skews pencil-test. Sean wants a **rock-solid, register-agnostic template** built specifically around **Nano Banana 2's editing mode** (image-to-image / multi-reference editing: "here is the character, render it in a new pose/angle/expression, keep identity") — a template that plugs into *any* 2D art style (pencil-test, pixel-art, anime, flat-color, watercolor, etc.) and serves both **Bible authoring** and **storyboarding** (the same character across many shots). The deliverable is the template + the research behind it + amendments to a kickoff prompt that already exists.

## Step 1 — Understand anima and how Cy works (read in this order)

1. `PHILOSOPHY.md` — the load-bearing intent. "If the loop plays smoothly and the character is recognizably itself in its intended medium, it ships." Human owns taste; agents propose, humans decide.
2. `CLAUDE.md` — project manual, current state, the 10-phase pipeline, the critic stack, the Character Bible primitive.
3. `docs/pipeline-architecture-v1.md` — the architecture lock (Phase 2 Character Bible, Phase 5 Generate, the draft→pro and critic concepts).
4. `docs/2026-05-27-cy-character-bible-brainstorm.md` — Cy's design lock (why a character is a folder, the `style_register` closed vocabulary, the §5 thesis "validators cannot recover taste absent at generation time").

Then analyze **how Cy actually prompts the model** (this is the surface your template plugs into — read the code, don't guess):

5. `pipeline/agents/character_designer.py` — especially `_run_plate` (~495), `_resolve_generate_references` (~877, the runner-owned anchor injection + no-chaining policy), `_build_nb_pro_prompt` (~911, the current role-tag framing) and `_build_prop_prompt` (the isolated-object exception), `_classify_reference` (~837), `_score_plate_identity` (~644, the DINOv2/CLIP/PIL similarity gate).
6. `pipeline/agents/nb_pro_runner.py` — `invoke_nb_pro`, `_build_skill_cmd`, the model slug (currently `gemini-3-pro-image-preview` = NB Pro). Note where the model is chosen.
7. `.claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py` — how references actually reach the API (`types.Part.from_bytes`, contents-list order, the default slug `gemini-3.1-flash-image-preview` = **NB2**). This is the editing call site.
8. `pipeline/agents/prompts/cy-character-designer-context.md` — Cy's role addendum: the JSON envelope schema, the per-plate `prompt` + `reference_images` contract, the "what good looks like" examples. **Your template will likely amend this file's contract.**

Then read the prior learning so you build on it, don't repeat it:

9. `docs/research/2026-05-30-nb-pro-nb2-prompting-for-pixel-and-angle-expansion.md` — the prior research pass (multi-view "photogrammetric inference," pixel-grid is a post-process problem, NB2-may-beat-Pro-for-consistency). **Build on this; do not re-derive it.**
10. `docs/anima-test-runs/2026-05-29-production-bake-and-gate-hardening.md` — the field report. Key lessons your template must respect: **prompt-dominance** (verbose prose beats the reference and drifts — `focused` went monochrome), **the runner owns framing** (identity injection is centralized), **reference-gap vs prompt-dominance are different drifts with different fixes**, and the similarity gate is record-only (per-view-reference is the unsolved hard-gate problem).
11. `docs/2026-05-30-claude-mascot-pencil-register-pivot-kickoff.md` — **the kickoff you will amend.** It re-authors the claude-mascot Bible in pencil-test using a multi-view turnaround. Your template generalizes its prompting beyond pencil-test.

## Step 2 — The research (delegate the web sweeps; keep your main context lean)

**Context safety:** do NOT run dozens of WebSearch/web_fetch calls in your main thread. Use the `deep-research` skill, or spawn `general-purpose`/`Explore` subagents, to fan out the web research and return only synthesized findings + citations. Today is mid-2026; NB2 = `gemini-3.1-flash-image-preview`, NB Pro = `gemini-3-pro-image-preview`. Research must be current (search, don't rely on training priors).

Research questions — **editing-focused and register-agnostic** (Sean explicitly does NOT want a pencil-test-only answer):

1. **NB2 editing mechanics.** How does NB2's image+text editing actually work for "same character, new pose/angle/expression, preserve identity"? Single-shot vs iterative/chained edits. How it weights reference pixels vs the text instruction. Optimal reference count and the role-assignment pattern ("Image A = identity, Image B = pose target, Image C = style").
2. **The identity/variation/style decomposition.** Find the canonical template structure practitioners converge on for editing — separating what's LOCKED (identity from the reference) from what CHANGES (pose/angle/expression/camera) from the STYLE register. What "preserve" / "keep unchanged" / "only change X" phrasing actually holds identity in NB2 editing.
3. **Register-agnosticism.** Verify the template holds across art styles — pencil-test, pixel-art, anime/cel, flat-vector, watercolor, 3D-render-look. Where does editing-mode identity preservation behave differently per register, and what parameterizes cleanly vs what needs per-register handling?
4. **Storyboarding application.** Generating one character across many shots/poses for a storyboard: sequential editing, holding identity across a shot sequence, shot/camera/framing language (wide/medium/close, eye-level/low/high, lens), and how to keep continuity across a beat sheet.
5. **NB2 vs NB Pro for editing specifically** (not just generation). Which is the better identity-preserving editor in mid-2026, given the documented NB-Pro multi-reference downsampling regression. Should anima route editing/consistency work to NB2 and reserve NB Pro for texture-rich finals?
6. **Editing failure modes + mitigations.** Identity drift on large pose deltas, attribute bleed, the "model invents what the reference doesn't contain" reference-gap, caption/text rendering. Map each to a template clause that prevents it.

## Step 3 — Deliverables

1. **`docs/research/2026-05-30-nb2-editing-character-consistency-template.md`** — studio-manual voice, cited. The research synthesis (Step 2) PLUS the headline artifact: **the register-agnostic NB2 editing prompt template.** Present the template as a parameterized structure (identity-lock block / variation block / style-register block / preserve-and-negative block / output-spec block) with the exact slot names. Include **three worked examples in three different registers** (e.g. pencil-test sean-anchor, pixel-art 16BitFit humanoid, one anime/flat-color) proving it's plug-and-play. Add a **storyboard variant** of the template (same character, multi-shot).
2. **Amendments to `docs/2026-05-30-claude-mascot-pencil-register-pivot-kickoff.md`** — either edit it directly or write a companion `…-kickoff-amendments.md`. Wire the template into Cy's plate-prompt construction: a concrete recommendation on whether `_build_nb_pro_prompt` / the Cy addendum (`cy-character-designer-context.md`) should be refactored to emit the template structure, and the NB2-vs-Pro routing decision per register (with the per-register model assignment in `manifest.yaml`). Keep it as a *plan* — no code edits this session.
3. A short **"how this generalizes to storyboarding"** section pointing at where Phase 3 (Storyboard) of the pipeline would consume the same template — so the template is recognized as a pipeline-wide primitive, not a Cy-only helper.

## Working pattern (Cowork)

- Open with a `TaskCreate` task list for the phases (read → research → template → amend kickoff). Mark progress.
- Use `AskUserQuestion` if a real fork surfaces (e.g. "refactor `_build_nb_pro_prompt` now vs. keep the template as a Cy-addendum contract only," or "route ALL registers to NB2 vs. per-register split") — Sean decides those.
- Delegate web research to the `deep-research` skill or subagents; synthesize, don't dump raw results into your context.
- Present final files with `present_files`. Studio-manual voice throughout. Cite sources.

## Guardrails

- **No production code changes** — this is research + a template + a plan. The next Claude Code session implements.
- **Build on, don't repeat,** `docs/research/2026-05-30-nb-pro-nb2-prompting-for-pixel-and-angle-expansion.md`.
- **Register-agnostic is the whole point** — if the template only works for pencil-test, it failed. Prove it across registers.
- **Respect the hard-won lessons:** terse-intent-plus-strong-reference beats verbose prose (prompt-dominance); the runner owns identity framing; editing ≠ generation. The template should encode these, not fight them.
- Don't touch the rename, the sean-anchor Bible, or the 16BitFit pixel pass (deferred).
