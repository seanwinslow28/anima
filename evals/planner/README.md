# Maya — planner eval suite

A small eval suite for anima's Phase 0 line producer. Six seed cases at first
landing, grounded in the Pencil Test reference implementation and the v2
brainstorm's stated cost ceilings. Some cases ship intentionally red — the
failure is the artifact.

---

## What this evaluates

Maya the Planner runs once per piece in a three-phase loop (Opus 4.7 primary
→ Sonnet 4.6 adversarial validation → resolution) and emits four artifacts:
a production brief, a v1.1 graph-shaped `acceptance_criteria.json`, a clean
markdown `plan.md`, and an in-memory `RunCostEstimate` surfaced into the plan.

The eval suite verifies six things:

1. **Plan emission** — all four artifacts land cleanly per case.
2. **Criteria graph shape** — mnemonic IDs, closed-vocab categories, valid
   impact tags, citation edges to phases and personas.
3. **Cost band realism** — the median estimate falls within v2 §7's stated
   per-phase ranges for the case's manifest.
4. **Three-phase branching** — the clean / real-flag / low-signal Sonnet
   resolutions each route to the right Opus call count.
5. **Clean-markdown invariant** — `plan.md` carries zero box-drawing
   characters. The CLI renders ASCII boxes; Maya emits prose.
6. **Documented failure modes** — under-spec briefs xfail intentionally;
   the failure is the artifact (see [`failure-modes.md`](failure-modes.md)).

---

## Why we evaluate this

Three reasons, lifted from the eval-discipline canon Sean's been working
against (Hamel Husain's *"evals are the inner loop of agent development"*,
Shreya Shankar's *"eval-as-spec, not eval-as-test"*, Anthropic's *"Demystifying
Agent Evals"*):

1. **The criteria contract is the single biggest variable in commit-3
   correctness.** Maya emits the graph that every downstream critic cites;
   if her schema drifts or her category vocab opens up, every downstream
   verdict is built on sand. The suite is the structural backstop.

2. **The three-phase loop branches need cheap regression coverage.** Each
   branch (clean / flag / low-signal) is a different code path in
   `PlannerNode.run()`; the cases exercise all three at < 100ms each via
   mocked SDK responses.

3. **The failure-mode taxonomy is portfolio content.** Pre-fix → post-fix
   improvement against named, real-production failure modes is what the
   museum walkthrough renders — not the test suite's green count.

---

## How to run

```bash
.venv/bin/pytest evals/planner/runner.py -v
```

Expected: 5 passed, 1 xfailed. The xfail is documented in failure-modes.md §4
and is the planned outcome until Maya's prompt tightens to refuse under-spec
Studio Briefs.

For the real-model variant (Sean's Anthropic Pro absorbs Opus + Sonnet),
unset the runner mocks and re-run. The first real-model trace lands in
[`last-run.md`](last-run.md) once authenticated.

---

## What we've learned

See [`failure-modes.md`](failure-modes.md). Four named modes today:

- `criteria-too-vague-to-test` — caught by the adversarial Sonnet pass.
- `cost-line-under-estimates-by-2x+` — guarded by the `cost-undercount-trap`
  case + the Sonnet adversarial pass.
- `impact_tag-mismatch` — documented but not yet regression-tested; add a
  case when a real run surfaces one.
- `under-spec-brief-ships-thin-plan` — intentionally red; documents the gap
  between Maya's current behavior (ship a thin plan + confidence note) and
  the right behavior (refuse, ask Sean to tighten).

---

## Provenance

- **Source-of-truth spec.** [`docs/2026-05-26-maya-planner-brainstorm.md`](../../docs/2026-05-26-maya-planner-brainstorm.md) §6 (Top 5) + §8 (file map).
- **Architecture lock.** [`docs/2026-05-26-agent-fleet-brainstorm-v2.md`](../../docs/2026-05-26-agent-fleet-brainstorm-v2.md) §6 (per-role table) + §2.3 (Pattern B shared rubric).
- **Eval-suite template.** Established here in commit 3b; commit 8b
  (vision-critic) and commit 9b (cli-critic) mirror this structure. The
  schema in `cases.yaml`, the mocked-runner pattern in `runner.py`, the
  `_BOX_CHARS` invariant assertion, the red/xfail discipline — all carry
  forward unchanged.
- **Change-map sequencing.** [`docs/2026-05-24-pipeline-v2-change-map.md`](../../docs/2026-05-24-pipeline-v2-change-map.md) §7 names commit 3b as the eval-template establishment commit. Subsequent eval commits reuse `runner.py`, `conftest.py`, and `README.md` shape.
- **Discipline references.** Hamel Husain (*"Your AI Product Needs Evals"*),
  Shreya Shankar (*"Eval-Driven Development for Modern AI Systems"*),
  Anthropic engineering (*"Demystifying Agent Evals"*). The discipline is
  older than the agents — eval suites are how we tell which iteration of the
  prompt is actually better, not just newer.

---

*This README is itself a museum artifact. When commit 6 ships, the museum
walkthrough surfaces it alongside the eval suite's most recent baseline
trace as evidence that anima's agent fleet ships against a measurable
contract, not against vibes.*
