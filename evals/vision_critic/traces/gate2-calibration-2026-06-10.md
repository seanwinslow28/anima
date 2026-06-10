# Trace — Em Gate-2 golden-agreement judge calibration (2026-06-10)

Judge: **opus** (`diff_eval.opus_judge` → `invoke_opus_text`, subscription) · **N=5 per pair, majority vote** · positive class = **match**.
Set: [`calibration_set_2026-06-09.jsonl`](../calibration/calibration_set_2026-06-09.jsonl) (54 pairs) · Labels: [`labeling_sheet_2026-06-09.yaml`](../calibration/labeling_sheet_2026-06-09.yaml) (Sean, 53 labeled + 1 no-candidate null).
Raw payload: [`../calibration/score_2026-06-10_iter1.json`](../calibration/score_2026-06-10_iter1.json). Iterations: **1** (passed first pass).
Verdict baseline guard: `traces/g6.1b-criteria-attached-2026-06-08.md` md5 `2af75906502f1caf8857e18828ceb2e4` — byte-identical before AND after (calibration is additive).

## Headline — PASS (bar: κ ≥ 0.6 AND FPR ≤ 0.10)

| Metric | Value | Note |
|---|---|---|
| **Cohen's κ** | **0.885** | substantial→near-perfect (bar ≥ 0.60) |
| **FPR** (judge over-calls match) | **0.067** | 2/30 true non-matches (bar ≤ 0.10) — the dangerous error, contained |
| precision (match) | 0.917 ± 0.056 | |
| recall (match) | 0.957 ± 0.043 | |
| raw agreement | 0.943 | reported, NOT the headline (imbalance-sensitive) |
| confusion (positive=match) | tp 22 / fp 2 / fn 1 / tn 28 | n_scored 53 (+1 no-proposal excluded) |

## Per defect class

| Class | cm (tp/fp/fn/tn) | κ | FPR | note |
|---|---|---|---|---|
| anatomy-count | 3/0/0/4 | 1.00 | 0.00 | perfect (+1 no-proposal) |
| construction-lines | 5/0/0/4 | 1.00 | 0.00 | perfect |
| proportion | 5/0/0/4 | 1.00 | 0.00 | perfect |
| shading-register | 5/0/0/4 | 1.00 | 0.00 | perfect |
| **palette** | 4/**2**/0/4 | 0.62 | **0.33** | the residual — judge over-calls *partial/related* palette fixes (see FP1, FP2) |
| view-correctness | 0/0/1/8 | 0.00 | **0.00** | κ degenerate (only 1 positive case, missed safely); **FPR 0.00 — judge correctly rejects Em's wrong-target-view fixes** |

Per-class κ is small-N noisy (≤10 pairs each); the **overall κ=0.885 is the trustworthy figure**. The palette and view rows are diagnostic, not standalone verdicts.

## The 3 disagreements (judge vs Sean)

**FN (safe — judge stricter than Sean), unanimous 0/5** — `real::view-vb1-borderline-60deg`
- Judge: candidate steers to ~45° three-quarter, golden targets ~60° → no-match.
- Sean: "45 vs 60 degrees is the same turned-toward-profile pose family … the exact degree is not what I'm scoring" → match.
- Under-calling match doesn't inflate Em's fix-rate. Borderline-view degree nuance; the conservative call.

**FP1 (dangerous — judge over-called match), unanimous 5/5** — `real::palette-pad6-brown-hair-beard`
- Judge: both steer hair toward dirty-blonde, the same palette correction → match.
- Sean: "anchor has dirty-blonde hair AND stubble. Candidate fixes the hair and is silent on the stubble; half a fix is not the same fix" → no-match.
- **Bias: the judge under-weights COMPLETENESS** — a partial fix reads as a match.

**FP2 (dangerous), split 3/5** — `cross::palette-pad1-monochrome__vs__shading-shd1-photographic`
- Judge: candidate's desaturated wash ≈ restoring the palette → match (but only 3/5 — genuine uncertainty).
- Sean: golden requires the *full reference color palette*; the candidate (a shading clause) "only mentions a desaturated wash, not the full palette" → no-match.
- Same completeness/relatedness over-call; the N=5 spread correctly exposed the ambiguity.

## N-vote stability
51/53 scored pairs were **unanimous** (5/0 or 0/5). Only 2 split: `construction-cld3` (4/5→match, agrees Sean) and the FP2 cross-palette (3/5→match, the one genuine ambiguity). The N=5 majority earns its keep precisely on the borderline FP.

## Reading
The proxy **agrees with Sean strongly enough to track Em's fix-rate between costed Gate-3 runs** (κ 0.885, FPR 0.067). Both dangerous over-calls are **palette completeness** misjudgments (partial/related fix scored as match); everywhere else the judge is exact, and critically it is **safe on view-correctness** (FPR 0.00 — it does not launder Em's wrong-target-view fixes into matches, the very axis Gate-3 flagged as Em's weakest). Residual + re-open conditions in the [field report](../../docs/anima-test-runs/2026-06-10-em-gate2-judge-calibration.md).

## Aggregate JSON (excerpt)
```json
{
  "bar": {"kappa_min": 0.6, "fpr_max": 0.1}, "pass": true, "judge": "opus", "n": 5,
  "overall": {"cm": {"tp": 22, "fp": 2, "fn": 1, "tn": 28},
              "precision": 0.917, "recall": 0.957, "fpr": 0.067,
              "raw_agreement": 0.943, "kappa": 0.885, "n_scored": 53, "n_no_proposal": 1}
}
```
Full per-class + per-pair (judge_match / sean_match / vote spread / why) in `../calibration/score_2026-06-10_iter1.json`.
