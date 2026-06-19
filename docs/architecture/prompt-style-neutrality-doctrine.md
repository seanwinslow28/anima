# Prompt style-neutrality doctrine

*One-page doctrine. Read this before adding a new style register, before editing a standing-context preamble, before adding a new agent role addendum to the fleet.*

---

## The principle

anima is a 2D animation pipeline, not a pencil-test pipeline. The pencil-test work is the first reference implementation — the proof that the pipeline ships — not the project's identity. Sean's portfolio thesis depends on this distinction: the pipeline ships a *working method* that handles whatever 2D character Sean (or anyone using anima) decides to make.

The closed `style_register` vocabulary on `character.yaml` is the structural commitment to that breadth:

  - `pencil-test-colored`
  - `pixel-art-8bit`
  - `line-art-only`
  - `watercolor`
  - `photoreal`
  - `3d-rendered`

Every prompt that drives an agent's behavior must work for every register in this vocabulary. The engine truth — *"if the loop plays smoothly and the character is recognizably itself in its intended medium, it ships"* — is style-agnostic by design. The medium is whatever the Studio Brief declared, not pencil-test by default.

---

## The bias the doctrine guards against

The Task 1.4.5 audit found four prompt files carrying pencil-test as the implicit default register. Pencil-test was the default register, the default failure mode, and the default "what good looks like" example. A pixel-art Bible authoring run would inherit "watch for cross-hatching smoothing out" as a structural concern — incoherent against the register and a silent contract failure.

The bias is subtle. The architecture supports six registers; the schema validates against six registers; the routing reads `style_register` to dispatch to six different generators. But if the prompts that *drive* the agents teach them to think in one register's vocabulary, the rest of the architecture is decorative. *Validators cannot recover taste that was absent at generation time* — the v2 synthesis §5 thesis — applies to prompts as much as to character Bibles.

---

## The test

`tests/test_prompt_style_neutrality.py` enforces the principle at CI time. It audits the four standing-context preambles (`anima-standing-context.md`, `cy-character-designer-context.md`, `em-vision-critic-context.md`, `maya-planner-context.md`) for two failure modes:

**1. Single-register markers in load-bearing sections.** When register-specific markers (`cross-hatching`, `integer-pixel grid`, `pigment-pool`, `lit volume`, etc.) appear in a load-bearing section — the "what you must not do" / "the lens you bring" / failure-mode prose — at least one cross-register marker must also appear in the same section. The language must read as comparative, not default-anchored.

**2. Implicit register defaults in failure-mode prose.** When a failure-mode section mentions style-register drift / template-trap / aesthetic drift, it must name at least two distinct style registers by literal name (`pencil-test-colored`, `pixel-art-8bit`, etc.). Failure-mode prose that mentions drift but names only one register is structurally biased.

The test deliberately allows single-register content inside `## What good looks like — {register}` / `### Example A — sean-anchor (...)` style scaffolded example blocks. Examples carry single-register content by definition; the scope is named at the boundary, so the bias-prevention need is satisfied.

---

## Adding a new style register

The closed vocabulary is extended deliberately, not inline. Three steps:

  1. **Extend the vocabulary in `pipeline/criteria.py`** (or wherever the validator lives) and add the value to `templates/bible/character.yaml.template`'s comment. The schema-level commitment is what makes the new register first-class.

  2. **Add a `## What good looks like — {register}` example block** to `cy-character-designer-context.md` showing three sample `IR.{character_id}.*` entries and a four-paragraph risk-bible excerpt in the new register's vocabulary. The new example sits alongside the existing pencil-test-colored and pixel-art-8bit blocks under the `What good looks like` heading.

  3. **Update `_STYLE_REGISTERS` in `tests/test_prompt_style_neutrality.py`** and add the new register's marker phrases to `_REGISTERS_TO_MARKERS`. The marker set should include the load-bearing visual markers a downstream agent (Em, mostly) would cite in a verdict against the new register's failure modes.

Commit with a message naming the new register and the rationale (which downstream piece needed it, which Bible was authored against it). Update `CHANGELOG.md`.

---

## Adding a new prompt file or editing an existing one

Before commit, re-read every load-bearing section (the "what you must not do" / "the lens you bring" / non-negotiables blocks) with this question:

> Would this prompt make sense to a pixel-art Bible author? A watercolor Bible author? A 3d-rendered Bible author? A photoreal Bible author? A line-art-only Bible author?

If the answer is no for any of the six registers, the prompt carries default-register bias — generalize it. Cite the registers comparatively, not as exceptions to a default.

The test catches obvious bias (single-register markers in load-bearing sections). The question catches subtler bias the test misses (implicit assumptions about the kind of work the agent is critiquing, default vocabulary in interactive prose). Both layers matter; the test is a backstop, not a substitute for reading the prompt with the question in mind.

---

## What this doctrine does NOT apply to

The Pencil Test reference implementation — Act 1 (shipped) and Act 2 (in flight) — is allowed to be pencil-test-specific in its **run-specific artifacts**:

  - Studio Briefs and Production Briefs for Pencil Test pieces (the briefs name pencil-test as the register and pencil-test-specific tone)
  - Run-specific manifests (`brief: active_dir:` pointing at a pencil-test brief directory)
  - Run notes and CHANGELOG entries describing pencil-test work
  - `manifest.yaml`'s top-level `style:` block (carries the pencil-test reference implementation's style block; it is a *piece's* style declaration, not the *pipeline's*)

The doctrine governs **reusable infrastructure**:

  - The standing-context preambles (`pipeline/agents/prompts/*.md`)
  - Templates (`templates/brief/`, `templates/bible/`)
  - Schemas (`pipeline/criteria.py`'s closed vocabularies)
  - The test suite that asserts against agent contracts

The pencil-test reference implementation is a *piece*; anima is a *pipeline*. The doctrine is the discipline that keeps the pipeline general while letting each piece carry its own register-specific voice.

---

## See also

  - `PHILOSOPHY.md` § *Load-bearing beliefs* — the engine truth that drove this doctrine.
  - `docs/2026-05-27-cy-character-bible-brainstorm.md` — where the closed `style_register` vocabulary was locked.
  - `tests/test_prompt_style_neutrality.py` — the enforcement mechanism this doctrine documents.
  - Task 1.4.5 commit — the audit + defang that surfaced the bias before the claude-mascot Bible run would have caught it the hard way.

---

*The architecture supports arbitrary 2D styles. The prompts now match. The guardrail catches regression. anima ships as a 2D animation pipeline — which is what it was always supposed to be.*
