# Kickoff — Sam the Scriptwriter, Phase 3a ($0 stub-green, TDD)

*Paste the block below into a fresh Claude Code session in the `anima` repo. Self-contained.
Plan of record: [`docs/2026-06-12-sam-scriptwriter-build-plan.md`](2026-06-12-sam-scriptwriter-build-plan.md).
Brainstorm + the four locked forks: [`docs/2026-06-12-sam-bea-phase3-brainstorm.md`](2026-06-12-sam-bea-phase3-brainstorm.md).*

> **⚠ Updated 2026-06-15 — read [`docs/2026-06-15-screenwriting-modes-integration-addendum.md`](2026-06-15-screenwriting-modes-integration-addendum.md) first.** Build-order step 3 below is amended: Sam loads the **full vendored voice instrument** `sean-screenwriting-voice.md` (vendor it verbatim from [`docs/2026-06-15-sam-bea-screenwriting-voice-context.md`](2026-06-15-sam-bea-screenwriting-voice-context.md)), NOT a condensed register note. Also seed the eval scaffold (step 5) with a few ships-red anti-pattern cases. Everything else in this kickoff stands.*

---

You're building **Sam**, the Phase 3 scriptwriter — the first of the two agents that complete the
named fleet. Sam reads Maya's `plan.md` + the Studio Brief and drafts a *script*: a studio-voice
`script.md` treatment and a structured `beats.json` beat sheet that the next agent (Bea) will turn
into the shot list. Sam **proposes**, the human decides — this is Phase 3, which PHILOSOPHY and the
architecture both insist is human-authored ("agents assist; they don't pick beats"). Read first, in
order: [`docs/2026-06-12-sam-scriptwriter-build-plan.md`](docs/2026-06-12-sam-scriptwriter-build-plan.md)
(the spec), `PHILOSOPHY.md`, `CLAUDE.md`, and `docs/pipeline-architecture-v1.md` §Phase 3. The code
you're cloning: `pipeline/agents/planner.py` (Maya — the AgentSpec shape), `pipeline/orchestration/shots.py`
(the validator to mirror for `beats.py`), `pipeline/cli/plan.py` (the CLI shape), `scripts/author_plan.py`
(the driver shape).

**What you build (Sam slice, standalone):** the `beats.py` Sam→Bea contract; the `scriptwriter`
node; its persona preamble; the `script` CLI; the `author_script.py` driver; the `evals/scriptwriter/`
scaffold; tests; docs.

**Out of scope:** Bea (next kickoff); wiring Phase 3 into `pipeline/run.py` (a follow-on slice after
Bea); the pairwise-preference eval harness and any model bake-off (the parked hardening campaign);
any live/costed Opus call (deferred with the parked end-to-end run). Don't touch `evals/vision_critic/`.

## Doctrine — non-negotiable

- **Verify against the tree, never trust a label — including this kickoff and the plan.**
  Re-confirm before building: that `planner.py`'s `@register_node` + `ClassVar` inputs/outputs +
  `cost_estimate()` + multi-pass `run()` shape is what you're cloning; that `shots.py:load_shots`'s
  validator idioms (slug regex, strictly-ascending ids, `cast ⊆ known_namespaces`, non-empty fields)
  are what `beats.py:load_beats` should mirror; that `invoke_opus_text` lives in
  `pipeline/agents/sdk_runners.py` and that Maya gives it a long timeout (`MAYA_CALL_TIMEOUT_S`,
  default 1200s — the 120s default silently crashed live Opus authoring; Sam needs the same, as
  `SAM_CALL_TIMEOUT_S`); that the stub fallback pattern (`sdk_runners` returns a stub when no key)
  is the one keeping CI green. Cautionary tales that earned this rule: a docstring lied about
  `agy -m`; Flo's CHANGELOG read "built" while nothing dispatched it; `--stub` silently spent real
  money via subscription OAuth a key-absent gate couldn't see.
- **Em verdict-baseline guard:** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md`
  must stay `2af75906502f1caf8857e18828ceb2e4`. Nothing in this slice reaches `evals/vision_critic/`.
- **$0 — stub-green only.** No model spend. The headline deliverable is that Sam's whole contract
  layer + CLI + driver prove end-to-end with **no key**, via the stub fallback. The real Opus
  authoring path is written and guarded, never invoked in CI.
- **TDD red→green.** Contract before agent: `beats.py` + `test_beats.py` land first and green,
  then the node, then the CLI/driver, then the eval scaffold, then docs. Small, revertible commits.

## §0 — fleet-ops gates (before any edit)

```bash
cd <anima main checkout>
git fetch origin
git log --oneline -1 origin/main                        # expect 742b629 (#51) or newer
git rev-list --left-right --count origin/main...HEAD    # expect 0 0
md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md  # 2af75906502f1caf8857e18828ceb2e4
echo "${ANTHROPIC_API_KEY:-ABSENT}"                     # expect ABSENT (Opus bills the subscription if ever run)
```

One isolated worktree off `origin/main`; ALL edits inside it. Single owner. Confirm the baseline
suite is green credential-free before touching anything:

```bash
python -m pytest tests/ -q          # expect green (576+); note any pre-existing .env-key artifacts
```

## Build order (TDD)

1. **`pipeline/orchestration/beats.py` + `tests/test_beats.py` (contract first).**
   Clone `shots.py`'s structure. `Beat(id, title, intent, emotional_beat, cast, feel="", notes="")`,
   `BeatSheet(slug, logline, beats)`, `load_beats(path, *, known_namespaces)`. Enforce: slug
   `[A-Za-z0-9_-]+`; non-empty `beats`; strictly-ascending int ids ≥ 1; non-empty
   `title`/`intent`/`emotional_beat`; non-empty `cast ⊆ known_namespaces`. Tests red→green:
   valid round-trip; non-ascending ids reject; unknown-namespace cast rejects; empty intent rejects.

2. **`pipeline/agents/scriptwriter.py` + `tests/test_scriptwriter.py` (stub path first).**
   `@register_node("scriptwriter")` `ScriptwriterNode`, `ClassVar` `name="scriptwriter"`,
   `inputs={"brief_dir": str}`, `outputs={"script_path": str, "beats_path": str}`,
   `cites_criteria=[]`, `cost_estimate → usd=0.0, latency_s≈120, confidence=0.85`. `run()` reads
   `00_studio_brief.md` (required) + `plan.md` (if present) + `ctx.manifest` characters registry
   for the cast namespaces. **Single Opus authoring pass** emitting `script.md` + `beats.json`,
   then a **deterministic structural pass** (no second LLM call): `load_beats` accepts the output,
   every `plan.md` story point maps to ≥1 beat (coverage), cast is consistent, beat count sane.
   Build the **stub fallback first** so the test is credential-free: stub emits a minimal valid
   `script.md` + `beats.json`. Tests: node emits a `beats.json` that `load_beats` accepts with the
   manifest namespaces; the structural pass **catches a coverage gap** (a beat sheet missing a
   plan story point) and passes a complete one.

3. **Opus authoring path** (guarded by the stub). Real `invoke_opus_text` with the persona
   preamble `pipeline/agents/prompts/sam-scriptwriter-context.md`, which loads
   `anima-standing-context.md` + the **full vendored voice instrument**
   `pipeline/agents/prompts/sean-screenwriting-voice.md` (vendor it verbatim from
   `docs/2026-06-15-sam-bea-screenwriting-voice-context.md` — the §8 verbatim samples are the
   load-bearing part; do NOT distill to a condensed note). Reuse Maya's envelope hardening
   (brace-balanced JSON extraction tolerating a persona preamble) and `SAM_CALL_TIMEOUT_S`
   (default 1200s). **No live call in CI** — the stub covers the test path.

4. **CLI + driver.** `pipeline/cli/script.py` — `script init/show/approve/mutate`, registered in
   `pipeline/cli/__main__.py` next to `plan`/`bible`/`patches`. `show` renders the beat-sheet tear
   sheet (clean prose on disk, box-drawing only in the renderer — Maya's rule). `approve` flips
   `locked: true` on `beats.json`, idempotent. `mutate` is the audited force-flag edit (mirror
   `plan.py`). `scripts/author_script.py <brief-dir> --run-dir … --manifest …` mirrors
   `author_plan.py` (live-Opus smoke + stub-marker guard).

5. **Eval scaffold.** `evals/scriptwriter/` — `cases.yaml` + fixtures + `runner.py` stub +
   `README.md`. Seed with the Spark beats as ground-truth: `briefs/2026-06-10-spark-shared/plan.md`
   → the expected 5-beat sheet. `runner.py` is the CI-green mocked mode (mirror
   `evals/planner/runner.py`). **Do not** build the pairwise-preference harness — campaign item.

6. **Docs.** CHANGELOG.md dated entry (what Sam is; why single-call; the deterministic-pass
   decision and its handbook rationale). CLAUDE.md Skills Map: add the Sam (`scriptwriter`) row;
   note Phase 3 is now half-built (Bea + orchestrator wiring remain). Re-assert the md5 guard.

## Acceptance (all must hold before the PR)

- `python -m pytest tests/test_beats.py tests/test_scriptwriter.py` green credential-free.
- `python -m pytest tests/` green (no regressions).
- `python -m pipeline.cli script init/show/approve` works against a brief dir; a stub-authored
  `beats.json` round-trips through `load_beats`.
- The structural pass catches a coverage gap (proven by test, not asserted).
- `md5sum …/g6.1b-criteria-attached-2026-06-08.md` == `2af75906502f1caf8857e18828ceb2e4`; nothing
  under `evals/vision_critic/` changed.
- CHANGELOG.md + CLAUDE.md updated.
- Lands as one squash PR off the isolated worktree. Clean teardown.

## When done

Report: the commits, the new test count, confirmation the full suite is green credential-free, the
md5 guard intact, and a one-paragraph field note on any seam that fought you (for the next session's
"verify against the tree" list). Then stop — Bea is the next kickoff, planned in Cowork once Sam
merges and the `beats.py` contract is proven against a real authored beat sheet.
