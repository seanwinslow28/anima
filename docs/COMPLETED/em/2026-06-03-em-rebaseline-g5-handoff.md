# Em Re-Baseline (G5) — Claude Code Run Brief

*2026-06-03. Handoff from the Cowork eval-foundation-reset session (part 2). This is the
G5 gate of `docs/2026-06-03-eval-foundation-reset-plan.md` §6 — the first Em baseline on
a trustworthy foundation. The number this run produces REPLACES the void contaminated
figures (precision 0.62 / recall 1.00 / false_pass 0.15) and is the resume gate for all
G6 work (SF03 build, the references question, DINOv2). Do not start G6 work in this run.*

**Standing doctrine: verify against the tree, never trust a label — including this brief.**

---

## What you are baselining

`evals/vision_critic/cases.yaml` (rebuilt 2026-06-03, Sean-ratified):

- **50 cases**: 16 clean + 28 single-axis defect/borderline (the `identity_style`
  performs-segment) + 6 `motion_proper` ships-red (report APART, expected misses).
- Six ratified classes, one `defect_label` per case: proportion, view-correctness,
  anatomy-count, palette, construction-lines, shading-register.
- Fixtures: `evals/vision_critic/fixtures/frames/*.jpeg` (44, uniform 1376x768),
  authored by Sean in Google Flow, independence enforced by
  `tests/test_fixture_contamination.py`.
- **Two corpus slots are pending Sean re-rolls** (P-B1, PA-D4 — staged at
  `images/sean-character-dataset/_pending-reroll/`, excluded from cases.yaml). The
  baseline runs WITHOUT them; when they land, the delta is two added cases, not a
  re-baseline.
- View-correctness trick: the image is a clean drawing of the WRONG view — the defect
  lives in the case's declared view. Do not "fix" these cases if Em misses them; a miss
  is signal.

## Pre-flight (all must pass before any costed call)

1. `python -m pytest tests/test_fixture_contamination.py -q` → 3 passed.
2. `python -m pytest evals/vision_critic/runner.py -q` → green (mocked plumbing).
3. Verify case counts: 50 total / 16 clean / 28 identity_style / 6 motion_proper.
4. **Fleet-ops discipline** (`docs/fleet-ops-protocol.md`): `ANTHROPIC_API_KEY` ABSENT
   (subscription SDK only — Em's default transport doesn't need Claude anyway);
   `GEMINI_API_KEY` present from `.env` (bounded key); isolated worktree; singleton
   pre-flight + own-PID resolution; single owner; clean teardown — do NOT
   `start_new_session` the costed worker.
5. Config: `critics.t2.transport: gemini_api`, **`critics.t2.attach_references: false`**
   (reference-blind is the shipped default; the flag stays OFF — flipping it is G6 work
   gated on DINOv2 + a clean re-baseline). Model pinned **gemini-3.5-flash** by ID via
   `pipeline/agents/gemini_api_runner.py`; read the served model back from
   `resp.model_version` and assert it matches. Never call `agy` without `-m` (the
   2026-06-02 model-provenance incident).

## The run

```bash
python -m evals.vision_critic.score          # live; writes last-run.md + a dated trace
```

**Replication protocol (the postmortem's scorer-replication standard,
`docs/anima-test-runs/2026-06-02-em-gemini-transport-rebaseline-postmortem.md`):**

- **N=5 full replications** of the suite, majority-vote verdict per case
  (3-of-5; a 2-2-1 verdict split resolves to the worse verdict — conservative).
- Report per-replication AND majority-vote metrics. Flag any case whose verdict
  flips across replications (the old stylus-case instability is the known failure
  shape; per-class n of 4-5 exists exactly so one flip doesn't swamp a class).
- Headline metrics on the identity_style segment: **precision / recall / false_pass**
  on the defect class (borderline counts as flagged, per scoring.py). Never raw
  agreement, never F1 alone.
- Segment the report: per-class confusion (6 classes), clean false-flag rate,
  borderline handling (4 borderline cases), motion_proper reported apart (expected
  0 catches; an Em catch there is a finding, not a win).

## Cost expectation

~50 cases × 5 replications = 250 gemini-3.5-flash calls (~$0.01–0.05 each → roughly
$2.50–12.50, plus retries). Bounded key; abort if quota-throttling forces partial
replications — a partial N is not a baseline (the 429-walled agy attempt is the
cautionary precedent).

## What comes out

1. `evals/vision_critic/last-run.md` + dated trace under `evals/vision_critic/traces/`.
2. A dated field report in `docs/anima-test-runs/` with the majority-vote matrix —
   THE new baseline numbers.
3. CHANGELOG entry. CLAUDE.md Em row update (baseline figures) once Sean ratifies the
   numbers.

## Resume gates this unlocks (G6 — NOT this run)

- SF03 proportion-gate build (Approach A armature probe → A or B).
- The references question, re-tested on the clean corpus (flag flip gated on DINOv2
  backstop + clearing the false-pass gate).
- DINOv2 deterministic identity backstop.
- Deferred identity modes (hair/jaw/eye) corpus extension; mascot corpus (needs its
  own turnaround sheet first).

## Ships-red discipline

Do not tune any case to flatter Em. A label edit is legitimate only as a validity fix,
and every label here is Sean-ratified 2026-06-03 — propose fixes to him; never lock
unilaterally.
