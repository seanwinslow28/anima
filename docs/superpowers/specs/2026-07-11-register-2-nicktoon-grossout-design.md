# Design — author register #2 (`90s-nicktoon-grossout`) + batch the primal transport change

**Date:** 2026-07-11 · **Workstream:** animation-vocabulary-expansion (within the active outward turn — a production unblock, not a new workstream) · **Branch:** `anim-vocab-register-2-nicktoon` (worktree off local `main`) · **Build engine:** Fable 5, TDD, stub-green, stop at first green.

## Goal (one sentence)

Wire the already-researched, already-look-ratified `90s-nicktoon-grossout` register into the closed vocabulary via the doctrine drill, and — batched in the same build — set `primal-sketch-grit`'s generation transport to `gpt-image-2` with a fail-loud guard so an unwired transport can never silently fall back to Gemini/NB2.

## Where this sits (verified against main)

- The register is **CANDIDATE** — `registers/90s-nicktoon-grossout/research.md` is wire-ready (§1 draft `RegisterSpec`, §2 Cy block, §4 transport **NB2 GO**, §7 genericization), 6 confirmed exemplars in `refs/`, but `pipeline/registers.py` has 7 registers and no `90s-nicktoon-grossout`.
- `primal-sketch-grit.generation_model` is still `NB2_FLASH`; fork #1 (batch → gpt-image) is unbuilt.
- Both decisions are Sean-ratified: **NB2 GO** for nicktoon; **batch primal → gpt-image** as its own tiny TDD change in this build.
- Process weight (Sean's call): **lean** — the register-authoring is a mechanical, already-converged drill (converged plan `docs/active/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md` was Opus→Codex→red-team); skip re-running full converged machinery, but send **only the new fail-loud guard** to a Codex adversarial pass before finalizing it.

## Section A — Register #2 authoring (the mechanical drill, §1.3 of the converged plan)

Sourced entirely from `registers/90s-nicktoon-grossout/research.md` §§0–2, §7. The load-bearing craft correction (research §0): **the default register is the appealing, warm, clean cel-cartoon human (~90% of frames); the grotesque "gross-up" is sparse comedic punctuation (1–2 beats), never the lead's resting state.** The `style_token` is authored appealing-default-forward, gross-up as the reserved move.

1. **`RegisterSpec` entry** appended last in `REGISTRY` (`pipeline/registers.py`):
   - `name="90s-nicktoon-grossout"`, `summary` / `identity_lock` / `preserve` / `style_token` from research §1 (construction-then-break volume-preserving identity; weight-hierarchy ink, self-colored edges, grimy-ground-one-lurid-accent, hue-turned shadows, the *quarantined* hyper-rendered gross-up ECU).
   - `generation_model=NB2_FLASH`, `final_model=NB_PRO` (painterly-final seam convention, mirrors watercolor/photoreal/3d/primal).
   - `markers` = unique load-bearing tells (e.g. `hyper-rendered gross-out insert`, `flat cel hard shadow shapes`, `desaturated ground one lurid accent`, `hue-turned saturated shadow`, `solid-construction-then-broken`, `self-colored swelling ink line`, + the register name) — **collision-checked** against all other registers by the per-register test.
   - `stub_keywords=("nicktoon", "grossout")` — appended **after** the legacy six + primal, so `_STUB_STYLE_REGISTER_BY_KEYWORD` precedence is preserved.
   - **Attribute-only negatives only.** No named-source negatives in `preserve` (naming a neighbor register can evoke it in the image model — research §1); drift policing lives in the Cy risk-bible.
2. **Cy example block** — `### Example D — kid (style_register: 90s-nicktoon-grossout)` under `## What good looks like` in `pipeline/agents/prompts/cy-character-designer-context.md`, from research §2 (the load-bearing IR trio: `construction.forms-wrap-not-flat`, `distortion.volume-conserved-through-extreme`, `palette.grimy-ground-one-lurid-accent` + a 4-para risk-bible excerpt). Plus adding the register name to the **two** closed-vocab enumeration lines (the `character.yaml` field description and the closed-vocab reminder).
3. **Template comment line** in `templates/bible/character.yaml.template` after the primal line.
4. **Per-register test** `tests/test_90s_nicktoon_grossout.py`, mirroring `tests/test_primal_sketch_grit.py`: registered · plate prompt carries register clauses + no pencil-vocabulary leak · routing is NB2 (gen) + NB Pro (final) · stub-keyword inference with appended-last precedence · stub-envelope no pencil coercion · markers don't collide.

**Genericization is doubly load-bearing** (research §7): IP *and* the creator's name. No show, artist, tool, or creator name in any clause, marker, comment, or example — the register is *a school of grotesque cel animation*, attribute-only.

## Section B — Primal transport change + fail-loud guard (the only new code)

**Decision (Sean): the guard lives in `invoke_image_edit`, allowlist `gemini-` prefix.** All options keep `gpt-image-2` as the honest value in the registry's "which model for which style" map; they differ only in where "no runner for this model" raises.

- **`pipeline/registers.py`:** add module constant `GPT_IMAGE = "gpt-image-2"` (pinned against the `openai-image-gen` skill — the GA flagship id; capabilities doc `.claude/skills/openai-image-gen/references/openai-image-capabilities.md`). Set `primal-sketch-grit.generation_model = GPT_IMAGE`. `final_model` stays `NB_PRO` — **fork #1 scopes only `generation_model`**; `final_model` has no consumer (documented dormant seam). The generate-on-gpt-image / final-on-NB-Pro split is a deliberate scope boundary, flagged for review (see Codex point 6).
- **`pipeline/agents/nb_pro_runner.py`:** new `UnwiredTransportError`; at the **top** of `invoke_image_edit`, before the stub/no-key check, raise it when `model` is not a `gemini-` slug (allowlist — the runner only drives the Gemini skill). Message names the model and points at the missing runner (e.g. wire gpt-image via the `openai-image-gen` skill). Firing before the stub check means it raises in **all modes** (credential-free CI included) — an unwired transport can't be stubbed, there is nothing to stand in for — and is testable with no key. Gemini models pass straight through to today's behavior, untouched.
- **`_resolve_plate_model` is NOT touched** — it still returns the honest model string; the guard lives only at the transport boundary. So `tests/test_register_characterization.py` (6 registers, byte-identical) is untouched, and `_resolve_plate_model("primal-sketch-grit") == "gpt-image-2"` is correct.
- **Update `tests/test_primal_sketch_grit.py`:** the one broken assertion (`_resolve_plate_model(_PRIMAL, {}) == "gemini-3.1-flash-image-preview"`) → `== "gpt-image-2"`. The `final=True` assertion (NB Pro) is unchanged. **Update `registers/primal-sketch-grit/research.md`** §4/§9 transport lines → "RESOLVED — gpt-image (unwired; fails loud until a runner is wired)".

### Grounded facts that de-risk Section B (verified on main)

- The primal change breaks **exactly one** existing assertion (`test_primal_sketch_grit.py:61`). Nothing else asserts primal NB2 routing.
- `primal-sketch-grit` is register **#7** — NOT in `test_register_characterization.py`'s 6 byte-identical set. Its model change touches nothing locked.
- `_build_stub_envelope` builds a pure dict and **never calls `invoke_image_edit`** → the guard cannot break the primal (or nicktoon) stub-envelope test.
- No code path passes a non-Gemini model to `invoke_image_edit` today except a *real* primal generation (the deferred/unwired case). (Re-grep at build time to confirm no new caller.)

## Section C — TDD order, verification, Codex red-team

**Red → green order** (Fable 5, this worktree, stub-green throughout, no live model/MCP call in tests):

1. Write `tests/test_90s_nicktoon_grossout.py` (RED — register absent) → add the `RegisterSpec` (completeness still red) → add Cy example block + closed-vocab lines + template line → **green**.
2. Write the guard test (`invoke_image_edit(model="gpt-image-2")` raises `UnwiredTransportError`; a `gemini-` model proceeds to the existing stub/placeholder path) (RED) → add the guard → **green**.
3. Flip `primal-sketch-grit.generation_model` → `GPT_IMAGE`; update the one primal assertion + `research.md` → **green**.

**Codex red-team (lean pick):** an adversarial `/codex:rescue --background` pass over **just the guard design** (Section B), launched at the start of the build, folded before the guard code is finalized. `-m`/flags/angle-brackets spelled out in prose per the companion gotcha.

**Verification gate (converged plan §8) — every "done" runs:**
- `python -m pytest tests/` green (per-directory from repo root) · `python -m pytest pipeline/tests/` green
- characterization (6 registers byte-identical) · completeness (incomplete register → red) · neutrality green
- **both frozen md5 guards unchanged** — `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4`; `pipeline/agents/prompts/sean-screenwriting-voice.md` = `945af824fa53b948a18ac6bf206d67ef` (neither touched by register work)
- stub-green Cy smoke ($0, no keys) · `superpowers:verification-before-completion`
- CHANGELOG.md entry + CLAUDE.md registry rows updated.

**Subscription billing only; no `ANTHROPIC_API_KEY` (GEMINI_API_KEY for image gen is fine but no live call runs in this $0 build). Stop at the first green checkpoint for Sean's review.**

## Out of scope (stays deferred / gated)

- Wiring an actual gpt-image *runner* + the across-edit identity validation — gated on Sean building GRANDMASTER.
- `samurai-jack-s5` register + the register-family (`family: tartakovsky`) question — greenlit-authoring-session work.
- `warm-storybook-pencil` candidate.
- Any change to the mascot eval corpus / Em (frozen).

## References

- `registers/90s-nicktoon-grossout/research.md` — the wire-ready source of truth for Section A.
- `docs/active/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md` §1.3 (drill), §5 Checkpoint 2 (the template these tasks mirror), §8 (verification).
- `docs/active/2026-07-04-register-backlog-and-transport-findings.md` §1, §7 (the pending primal change + roster).
- `tests/test_primal_sketch_grit.py` — the per-register test template.
- `docs/architecture/prompt-style-neutrality-doctrine.md` — the drill (already corrected to point at `registers.py`).
