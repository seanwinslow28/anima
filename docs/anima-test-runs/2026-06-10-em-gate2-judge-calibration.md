# Field report — Em Gate-2 golden-agreement judge calibration

*2026-06-09→10. Costed Claude Code run under [`docs/fleet-ops-protocol.md`](../architecture/fleet-ops-protocol.md). Tier 1 of the [eval-suite close-out](../COMPLETED/evals-foundation/2026-06-08-tier1-eval-suite-closeout-kickoff.md). Calibrates the **Gate-2 golden-agreement proxy judge** ([`evals/vision_critic/diff_eval.py`](../../evals/vision_critic/diff_eval.py)) against a Sean-labeled sample so Em's constructive fix-rate can be tracked between the costed ~$7.80 Gate-3 runs — for pennies. Per the eval handbook (§3), a judge's numbers are not trustworthy until calibrated; this run produces that calibration, the judge-bias ledger, and the trustworthy-or-not verdict. **Additive only** — the verdict baseline ([`traces/g6.1b-criteria-attached-2026-06-08.md`](../../evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md), md5 `2af75906502f1caf8857e18828ceb2e4`) is untouched.*

## What "calibrated" buys
Gate 3 (empirical fix-rate, [field report 2026-06-08](2026-06-08-em-g6.9-gate3-fixrate.md)) is the headline constructive measure but costs ~$7.80 / ~2.5 hr. Gate 2 asks the cheap proxy question — *does Em's proposed corrective clause express the SAME fix as Sean's ratified golden?* — Opus-judged, runnable any time. If the judge agrees with Sean reliably, the proxy can stand in between costed runs. The **dangerous error** for this proxy is the judge **over-calling "match"** (Em's clause scored a match when Sean says no) — that would inflate Em's tracked fix-rate in her own favor. So MATCH is the positive class and the headline is **precision/recall on match + the false-positive rate FPR = FP/(FP+TN)**, never raw agreement (imbalance-sensitive, §3.2). Bar (Sean, 2026-06-09): **κ ≥ 0.6 AND FPR ≤ 0.10**.

## §0 evidence (assert before spend)
- Divergence `origin/main...HEAD` clean (branch ahead only); verdict baseline md5 **`2af75906502f1caf8857e18828ceb2e4`** byte-identical before AND after.
- `ANTHROPIC_API_KEY` **absent** → the Opus judge (`diff_eval.opus_judge` → `invoke_opus_text`) bills the **subscription** via the Claude Agent SDK (`claude_agent_sdk` importable). No `--allow-api-key` hatch.
- `GEMINI_API_KEY` bounded from `.env` for the Em capture only (never committed).
- Stub harness green before any model call: `tests/test_calibrate_diff_judge.py` 22 passed; full contract suite 432 + seedance 10.
- **Capture-proof (both transports real, not stubbed):** one aesthetic case (Gemini path) + one identity_critical case (Opus-escalation path) each returned a well-formed corrective clause before the full capture.
- **Judge smoke (real, not stubbed):** a 1-call Opus agreement check returned a discriminating verdict (caught a candidate omitting the golden's "color wash" technique → `match:false`).

## Method (handbook §3.1 Critique Shadowing, §3.5 sampling consistency)
1. **Capture (costed, ~$1.50 Gemini + subscription Opus).** Em run LIVE on the 30 `identity_style` defect cases via **per-case subprocess isolation** (`score.py --only <case> --dump-patches`, fresh interpreter each — dodges the exit-144 teardown race #37 a 30-case in-process Em+Opus loop would hit), incremental JSONL + per-case containment. **30/30 cases, 29 non-empty, 0 errored gaps, 0 STUB.** `anatomy-ad3-third-arm` proposed no diff → `match=None` exclusion (a real outcome, never a 0).
2. **Balanced set (54 pairs)** — [`calibration_set_2026-06-09.jsonl`](../../evals/vision_critic/calibration/calibration_set_2026-06-09.jsonl):
   - **30 real** — Em's clause vs its own golden; ground truth NOT assumed.
   - **18 cross-class negatives** — Em's clause from class B vs class A's golden (class-distinct); faithful cross-domain non-matches that keep Em's incidental overlap (the realistic FPR stress, not terse golden-vs-golden).
   - **6 hard same-class negatives** — hand-authored (within a class the ratified goldens are near-identical, so same-class case pairings would mostly *match*; these are genuine intent divergences the judge can't dismiss on domain).
   The judge is **blind to `kind`** (sees only candidate + golden + defect class).
3. **⚖ Sean labeling checkpoint** — binary match/no-match + a one-line `why` per pair (Critique Shadowing: his critiques are the real artifact). [`labeling_sheet_2026-06-09.yaml`](../../evals/vision_critic/calibration/labeling_sheet_2026-06-09.yaml), 53 labeled (1 null = the no-candidate exclusion), all with a `why`.
4. **Judge + score** — `opus_judge` **N=5 per pair, majority vote** (sampling consistency > verbalized confidence, §3.5); match-class confusion matrix vs Sean; precision/recall/FPR/raw-agreement/Cohen's κ, overall + per defect class.

## Sean's labels — distribution (the ground truth)
**23 match / 30 no-match** across 53 labeled pairs — well-balanced, ample non-matches for FPR power. By kind: real **22✓ / 7✗** (1 null); cross-negative **17✗ / 1✓**; hard-negative **6✗**.

Real-pair match rate by class (Em's constructive quality, by Sean's eye):

| Class | match | no-match | note |
|---|---|---|---|
| proportion | 5 | 0 | Em nails 1:7 proportion fixes |
| anatomy-count | 3 | 0 | (+1 no-proposal, excluded) |
| shading-register | 5 | 0 | |
| construction-lines | 4 | 1 | the miss: a pose clause, not construction lines |
| palette | 4 | 2 | misses: sneakers blanked; beard left unaddressed |
| **view-correctness** | **1** | **4** | **Em proposes the WRONG target view** — drives to ¾ when golden wants profile, mirror-flips L/R, hides the face entirely |

The **view-correctness 4/5 no-match** independently corroborates Gate-3's finding that view is Em's weak constructive axis (0.00 normalized lift there). The 1 cross-negative match is a genuine incidental overlap (a shading clause that explicitly included "construction lines beneath the final line," paired against a construction golden).

## Results (Opus judge N=5 vs Sean) — PASS, iteration 1
Full evidence: trace [`traces/gate2-calibration-2026-06-10.md`](../../evals/vision_critic/traces/gate2-calibration-2026-06-10.md); raw [`score_2026-06-10_iter1.json`](../../evals/vision_critic/calibration/score_2026-06-10_iter1.json).

| Metric (positive = match) | Value | Bar |
|---|---|---|
| **Cohen's κ** | **0.885** | ≥ 0.60 ✓ |
| **FPR** (judge over-calls match) | **0.067** (2/30 true non-matches) | ≤ 0.10 ✓ |
| precision | 0.917 ± 0.056 | — |
| recall | 0.957 ± 0.043 | — |
| raw agreement | 0.943 (reported, not headline) | — |
| confusion | tp 22 / fp 2 / fn 1 / tn 28 (n=53) | — |

Per class: anatomy / construction / proportion / shading **κ=1.00, FPR=0.00** (perfect); **palette κ=0.62, FPR=0.33** (both overall FPs); **view-correctness FPR=0.00** (κ=0.00 is a 1-positive small-N artifact, not a failure — the judge correctly rejects Em's wrong-target-view fixes). N-vote stability high: 51/53 unanimous; the 1 ambiguous over-call surfaced as a 3/5 split.

## Em-Gate-2 judge-bias ledger
| Bias / behavior | Evidence | Direction | Disposition |
|---|---|---|---|
| **Palette completeness under-weighting** | FP1 `palette-pad6` (hair fixed, stubble ignored → judge said match, 5/5); FP2 `cross palette↔shading` (desaturated wash ≈ full palette → 3/5) | **Dangerous** (over-calls match) | Both overall FPs are this; named re-open condition below. Contained at FPR 0.067 overall. |
| **Slightly stricter than Sean on borderline view degree** | FN `view-vb1` (45° vs 60°, judge said no-match 0/5; Sean: same pose family) | **Safe** (under-calls match) | Accept — conservatism here doesn't inflate fix-rate. |
| **Verbosity bias (§3.4)** | Not observed to *help* Em — the verbose palette candidates were judged on intent, and FP1's clause is terse; FP2 is the verbose one but split, not unanimous | neutral | Monitor; N=5 majority blunts it. |
| **Position bias (§3.4)** | Single-orientation prompt (candidate then reference, fixed); not order-swapped this run | unmeasured | Low risk for a same-intent binary; revisit if the proxy is reused pairwise. |
| **Sampling stability (§3.5)** | 51/53 unanimous; the lone genuine ambiguity (FP2) showed as 3/5 — exactly where N>1 earns its keep | — | N=5 validated as the right vote count. |

## Verdict — TRUSTWORTHY (track Em's fix-rate between costed Gate-3 runs)
The Gate-2 golden-agreement proxy **clears the bar on the first iteration** (κ 0.885, FPR 0.067) and is trustworthy enough to track Em's constructive quality between the ~$7.80 Gate-3 runs for pennies. No prompt iteration was run: the bar was met, and chasing the 2 subtle palette FPs on a 53-pair sample would risk overfitting the prompt to this corpus (the disciplined call per handbook §3.1 — iterate only to *reach* the bar, then stop). The two dangerous over-calls are both a single, named bias (palette **completeness** — a partial or related fix scored as match); everywhere else the judge is exact, and it is **safe on view-correctness** (FPR 0.00 — it does not launder Em's wrong-target-view fixes into matches, the very axis Gate-3 flagged as her weakest).

**Re-open condition (revisit the prompt if EITHER holds):** (a) palette diffs become a tracked production focus — then add a completeness few-shot ("a partial fix that omits an attribute the golden addresses is NOT a match") seeded with FP1/FP2 and re-validate on this set; or (b) a future Gate-3 shows the proxy's tracked palette fix-rate drifting above the empirical rate (the over-call leaking through).

## Residual caveats (standing, regardless of the number)
- **Hard-negative coverage is small (6).** The FPR's statistical power against *within-domain* over-calling rests on 6 authored pairs + the within-domain reals; a larger same-class negative set would tighten it. Stated, not hidden.
- **Calibrated on sean-anchor only.** Mascot diffs are not in this set (mascot eval corpus still deferred).
- **The proxy tracks AGREEMENT-WITH-GOLDEN, not empirical fix-rate.** It is the cheap between-runs signal; Gate 3 remains the ground-truth constructive measure. A drift in Em's *style* of proposing could move the proxy and the empirical rate apart — re-anchor against a fresh Gate-3 periodically.
