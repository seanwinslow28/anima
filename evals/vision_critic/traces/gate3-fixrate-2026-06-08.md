# Gate 3 fix-rate baseline — Em constructive axis (2026-06-08)

Raw trace for the G6.9 Gate-3 costed run. Config: `patch_efficacy --arm both+null --sample 12 --rerolls 3`, LIVE, gemini-3.5-flash T2 + Opus-4.7 escalation (subscription), `_PER_CASE_TIMEOUT_S=1800`. Sample = 2 cases/class × 6 classes; 3 re-rolls × 3 arms (em / golden control / null placebo). **N = 6 binary outcomes per class per arm** (2 cases × 3 re-rolls).

- **Run:** 12/12 cases completed `ok`, **0 errored gaps**. Wall **8833s (2.45 hr)**. proposal_rate **1.00** (Em proposed a diff on every case; no `skipped_no_proposal`).
- **Estimate vs actual:** estimate **$7.80** (nb2=90, em=120 incl. 12 captures); actual ≈ estimate (full matrix ran, no extra calls; tmp cache cleared pre-run so no cross-run hits; Opus escalation subscription-absorbed, outside the $).
- **Lift = (em − null)/(golden − null)** per Sean's attribution lock. `discriminative: false` ⇒ golden ≈ null (no instrument power). All six classes were **discriminative: true** this run.
- Field report: [`docs/anima-test-runs/2026-06-08-em-g6.9-gate3-fixrate.md`](../../../docs/anima-test-runs/2026-06-08-em-g6.9-gate3-fixrate.md). Raw `runs/gate3-baseline.json` (gitignored) is embedded below.

## Headline — normalized lift per class

| class | em | golden | null | **lift** | discriminative | read |
|---|---|---|---|---|---|---|
| anatomy-count | 0.67 | 0.50 | 0.33 | **+2.00** | yes | em ≥ golden |
| shading-register | 0.33 | 0.17 | 0.00 | **+2.00** | yes | em ≥ golden |
| proportion | 0.33 | 0.33 | 0.00 | **+1.00** | yes | em = golden |
| palette | 0.33 | 0.50 | 0.17 | **+0.50** | yes | em < golden, > placebo |
| construction-lines | 0.33 | 0.67 | 0.17 | **+0.33** | yes | em < golden, > placebo |
| view-correctness | 0.00 | 0.50 | 0.00 | **+0.00** | yes | **em cleared 0/6** (golden 3/6) |
| **overall** | **0.333** | **0.444** | **0.111** | **0.667** | yes | em ≈ ⅔ of golden's lift over the floor |

**Reading.** Em's proposed fixes recover **~⅔ of the golden's lift over the placebo floor** overall, and clear meaningfully better than the placebo on every class but one. Strong on anatomy / shading / proportion (em ≥ golden at this N); mid on palette / construction; the one clear miss is **view-correctness, where Em's declared-view-correction clauses cleared nothing** (the no-regen label-side path — re-critique the same fixture under a corrected declared view — and Em's view diffs do not move it, while Sean's golden does 3/6).

## Caveats (read before quoting any single number)

- **Small N.** 6 binary outcomes per class per arm → wide bands (per-class stderr ≈ 0.33). The per-class lifts are **directional, not precise** — especially the `+2.00`s, which ride on small golden−null denominators (e.g. shading golden 0.17 − null 0.00 = 0.17; em 0.33 ⇒ lift 2.0). `lift > 1` means "em cleared at a higher rate than the golden over the floor **at this N**," not a calibrated 2× — don't over-read the magnitude. The runbook scoped 12×3 as "the affordable first read"; the fuller **30×5** characterization is the deferred next run.
- **Per-reroll granularity not serialized.** `main()` emits only the per-class aggregate + lift (not the per-case/per-reroll `effs`). The per-class bands below are the trace-grade record; surfacing raw per-reroll outcomes is a cheap future enhancement to the output JSON.
- **Ships-red / no relabel.** No case was relabeled to flatter Em; `clean-c06` and the 6 motion cases are untouched (outside this defect-only sample).

## Per-class bands (mean [min,max], stderr) — all three arms

```
                       em                     golden                  null
anatomy-count      0.667 [0.33,1.00] 0.33   0.500 [0.33,0.67] 0.35   0.333 [0.00,0.67] 0.33
construction-lines 0.333 [0.00,0.67] 0.33   0.667 [0.67,0.67] 0.33   0.167 [0.00,0.33] 0.26
palette            0.333 [0.00,0.67] 0.33   0.500 [0.33,0.67] 0.35   0.167 [0.00,0.33] 0.26
proportion         0.333 [0.33,0.33] 0.33   0.333 [0.33,0.33] 0.33   0.000 [0.00,0.00] 0.00
shading-register   0.333 [0.00,0.67] 0.33   0.167 [0.00,0.33] 0.26   0.000 [0.00,0.00] 0.00
view-correctness   0.000 [0.00,0.00] 0.00   0.500 [0.33,0.67] 0.35   0.000 [0.00,0.00] 0.00
overall            0.333 [0.00,1.00] 0.14   0.444 [0.00,0.67] 0.14   0.111 [0.00,0.67] 0.09
```

## Raw output (embedded — `runs/gate3-baseline.json` is gitignored)

```json
{
  "aggregate": {
    "proposal_rate": 1.0,
    "by_arm": {
      "em":     { "overall": { "n_cases": 12, "fix_rate_mean": 0.3333, "band": {"min":0.0,"max":1.0,"stderr":0.1361} } },
      "golden": { "overall": { "n_cases": 12, "fix_rate_mean": 0.4444, "band": {"min":0.0,"max":0.6667,"stderr":0.1434} } },
      "null":   { "overall": { "n_cases": 12, "fix_rate_mean": 0.1111, "band": {"min":0.0,"max":0.6667,"stderr":0.0907} } }
    }
  },
  "normalized_lift": {
    "overall":            { "em": 0.3333, "golden": 0.4444, "null": 0.1111, "lift": 0.667, "discriminative": true },
    "by_label": {
      "anatomy-count":      { "em": 0.6667, "golden": 0.5000, "null": 0.3333, "lift": 2.000, "discriminative": true },
      "construction-lines": { "em": 0.3333, "golden": 0.6667, "null": 0.1667, "lift": 0.333, "discriminative": true },
      "palette":            { "em": 0.3333, "golden": 0.5000, "null": 0.1667, "lift": 0.500, "discriminative": true },
      "proportion":         { "em": 0.3333, "golden": 0.3333, "null": 0.0000, "lift": 1.000, "discriminative": true },
      "shading-register":   { "em": 0.3333, "golden": 0.1667, "null": 0.0000, "lift": 2.000, "discriminative": true },
      "view-correctness":   { "em": 0.0000, "golden": 0.5000, "null": 0.0000, "lift": 0.000, "discriminative": true }
    }
  },
  "errored": []
}
```

## Guard

Verdict baseline `traces/g6.1b-criteria-attached-2026-06-08.md` (`md5 2af75906502f1caf8857e18828ceb2e4`) stayed byte-identical through this run (confirmed before and after). G6.9 is additive — the constructive axis, never a re-score of the verdict baseline.
