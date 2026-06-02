# Em — vision-critic eval suite

A scored eval baseline for **Em**, anima's T2 vision critic. The premise this
suite retires: Em had shipped at three checkpoints but had **never been scored
against a labeled defect set**. This makes Em's quality empirical instead of
assumed.

Methodological basis: `docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md`
(error-analysis-first case design §2; precision/recall/false-pass over
raw-agreement §4; the contact sheet sees identity/style across time but NOT
motion-proper §3.5).

## Two modes (Mo's `--no-sonnet` discipline)

**1. CI-green, mocked — `runner.py`.** Proves the *scoring plumbing* works
against every real case, credential-free. Em's runners are stubbed with a fixed
verdict, so the confusion matrix is degenerate by construction — **this mode
never asserts Em's accuracy.** It asserts: every case loads and is scored, the
segmented report is well-formed, the `cites_criteria` invariant doesn't crash
the harness, and intentionally-red cases carry their `xfail` marker.

```bash
.venv/bin/pytest evals/vision_critic/runner.py -v
```

**2. Deliberate, costed, LIVE — `score.py`.** Invokes Em *for real* (gemini-3.5-flash
via the Gemini API as the default voice + Opus 4.7 via the Claude Agent SDK on
escalation, exactly as she ships — the old "Gemini 3.1 Pro via agy" label was
aspirational; agy ran the backend-default Flash, 2026-06-02 forensics) across the labeled set and writes the real
**segmented confusion matrix** to `last-run.md` + a dated trace. Mirrors Mo's
opt-in: `--stub` forces the credential-free path so the script is exercisable
in CI without making a scored claim.

```bash
.venv/bin/python -m evals.vision_critic.score          # live (agy + SDK)
.venv/bin/python -m evals.vision_critic.score --stub   # credential-free, no scored claim
```

## The metric contract (§4)

- **Precision / recall on the DEFECT class**, reported separately. A verdict in
  `{fail, borderline}` flags a defect; `pass` is clean.
- **False-pass rate front and center** — the costly error is the drifted frame
  Em lets through (`FN / labeled-defects = 1 - recall`). It hides in
  borderline→fail slippage, scored as its own signal.
- **Raw agreement is never the headline** (it flatters under class imbalance);
  **F1 is secondary** (it hides the false-pass blind spot).
- `cites_correctness`: when Em flags a defect, did she cite a *correct*
  criterion? (`None` when the verdict is `pass`.)

## Segmentation (Sean's locked decision)

The report splits the cases that Em *should* perform on from the ones she
*structurally cannot* see:

- **`performs`** = `clean` + `identity_style` — the contact sheet / a still can
  surface these. This is Em's real number.
- **`motion_proper`** = reported APART, **ships intentionally RED.** A contact
  sheet shows identity/style across time but not motion-proper (arc/jitter/
  flicker/texture-crawl); MLLMs answer video questions correctly even on
  shuffled frames (§3.5). Em is *expected to miss* these — the miss is the
  artifact, and these cases pre-stock the deferred E_warp/VBench validation set.

## Discipline

- **Ships-red is the artifact.** Do NOT tune a case until Em passes it — that
  measures the thermometer against itself (Goodhart). Editing a label is
  legitimate ONLY when the label was wrong (a validity fix), never to flatter Em.
- **Em's contract is off-limits.** The `cites_criteria` invariant and the
  verdict vocabulary in `pipeline/agents/vision_critic.py` are not to be changed
  to make a case pass. If a case seems to require it, that's a separate decision.
- **Label authority.** Sean is the single labeler (solo scale; no Cohen's κ yet
  — see `failure-modes.md` D2). The cases in `cases.yaml` are drafted from
  ground-truth metadata and **ratified by Sean at the STOP gate.** A
  disagreement between Em and a label is a fork: judge-calibration (tighten Em's
  prompt — a later workstream) vs. criteria-drift (Sean's rubric sharpened by
  grading — legitimate).

## Files

| File | Role |
|------|------|
| `scoring.py` | Pure scoring core (confusion matrix, precision/recall/false-pass, segment_report). Shared DRY across `runner.py`, `score.py`, and the bake-off. |
| `cases.yaml` | The labeled, segmented case set. Every `input` is a real committed fixture. |
| `conftest.py` | Fixtures + `make_vision_verdict` envelope builder + fake CLI/SDK responses. |
| `runner.py` | Mode 1 — CI-green mocked harness (scoring unit tests + end-to-end plumbing). |
| `score.py` | Mode 2 — deliberate live scorer; writes `last-run.md` + a dated trace. |
| `failure-modes.md` | The open-coded taxonomy (written *after* reading real frames). |
| `bakeoff_lib.py` | Shared bake-off logic (reuses Em's `_build_prompt`/`_parse`, no escalation). |
| `fixtures/` | Real frames (Act 1 approved/rejected, Cy Bible plates) + Act 2 motion contact sheets. |
| `traces/` | Dated scored baselines (incl. the pre-suite smoke traces). |
