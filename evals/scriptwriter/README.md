# Scriptwriter (Sam) — eval suite

Scaffold-stage eval suite for **Sam**, the Phase-3a scriptwriter. Mirrors
`evals/planner/`. Two kinds of case, both seeded from real Sean-ratified material.

## What it checks (and deliberately doesn't)

**Positive cases** validate that a ground-truth beat sheet round-trips through
`pipeline/orchestration/beats.py:load_beats` **and** passes Sam's deterministic
structural pass (`pipeline.agents.scriptwriter.structural_validate` — cast-coverage
+ sanity, Decision #1). This is the brief→beats plumbing/coverage contract.

- `spark-shared-plumbing` — the real "Spark, Shared" anima brief (wordless,
  two-character). The plumbing/coverage case.
- `figgy-pudding-voice` — the 2026-06-15 Sean-ratified voice dry-run (dialogue-heavy,
  synthetic cast `greta`/`doug`). Additive voice exemplar; only its **structure** is
  asserted here.

**Ships-red cases** are by-ear voice defects that v1's deterministic pass does
**not** catch — and shouldn't (the AI-evals handbook bars LLM aesthetic judges on
creative quality; they're weak and self-preferring). They are **seed material for
the deferred pairwise-preference harness**:

| Case | Detector | Result |
|------|----------|--------|
| `sr-1-narrator-quip-in-dialogue` | none | `xfail` (by-ear) |
| `sr-2-register-collapse` | none | `xfail` (by-ear) |
| `anti-pattern-recycled-coffee-prop` | `default_prop` | **green** (caught by `default_prop_lint`) |
| `anti-pattern-theme-spoken` | none | `xfail` (by-ear) |
| `anti-pattern-naked-tender-pivot` | none | `xfail` (by-ear) |
| `anti-pattern-clean-catharsis` | none | `xfail` (by-ear) |

`default_prop_lint` (in `checks.py`) is the one genuinely-deterministic ships-red —
it flags the literal default-prop reach (coffee) the voice instrument calls out by
name. It is **eval-side only**, never a production gate.

## Why "story-point coverage" is NOT here

The original framing checked beats against "plan.md story points." That needs an LLM
to parse free prose — which v1 bars. Per Decision #1 (2026-06-15, ratified), the
deterministic red failure class is a **cast-coverage gap** (a loaded character with
no beat), not prose story-point matching. Narrative fidelity is the human gate's call.

## NOT built (campaign item)

The **pairwise-preference harness** — the rig that would actually judge voice quality
(blind Sean-preference, revision count) — is deferred per the build plan. These cases
are the corpus it will consume.

## Run

```bash
# Scaffold suite (CI-green; ships-red by-ear cases report xfailed):
python -m pytest evals/scriptwriter/runner.py -v
```

Credential-free: no model is called — the runner validates the committed ground-truth
corpus and documents the by-ear gaps.
