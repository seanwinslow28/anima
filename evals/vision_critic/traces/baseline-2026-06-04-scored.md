# Em — scored baseline (2026-06-04 13:06 UTC)

Model: **production: gemini-3.5-flash@gemini_api + opus-4.7-escalation**  ·  cases: 50

Metric contract: precision/recall on the defect class; **false-pass rate front and center** (the costly error). Raw agreement is NOT the headline (class imbalance); F1 is secondary. Segmented per Sean's call: identity/style+clean ('performs') reported apart from motion-proper (expected-red — the contact sheet structurally can't see motion).

### Performs (identity/style + clean)  (n=44)

- confusion: TP=28 FP=1 FN=0 TN=15
- **precision=0.97  recall=1.00**  (recall ±0.00)
- **false_pass_rate=0.00**  (false passes: none)
- 3-way exact agreement=0.91
- borderline->fail slippages: construction-cld3-clean-final-3quarter, construction-cld4-clean-final-drawing-desk
- cites-correct: 0.03
- mean wall: 30.6s

### Motion-proper (expected red)  (n=6)

- confusion: TP=5 FP=0 FN=1 TN=0
- **precision=1.00  recall=0.83**  (recall ±0.15)
- **false_pass_rate=0.17**  (false passes: motion-t2-arc)
- 3-way exact agreement=0.17
- borderline->fail slippages: motion-w1-arc, motion-w2-jitter, motion-tr-texture-crawl, motion-t2-arc, motion-rev-jitter
- cites-correct: 0.00
- mean wall: 40.0s

### Overall  (n=50)

- confusion: TP=33 FP=1 FN=1 TN=15
- **precision=0.97  recall=0.97**  (recall ±0.03)
- **false_pass_rate=0.03**  (false passes: motion-t2-arc)
- 3-way exact agreement=0.82
- borderline->fail slippages: construction-cld3-clean-final-3quarter, construction-cld4-clean-final-drawing-desk, motion-w1-arc, motion-w2-jitter, motion-tr-texture-crawl, motion-t2-arc, motion-rev-jitter
- cites-correct: 0.03
- mean wall: 31.7s


## Replication (5 runs)

Point estimate above uses the per-case MAJORITY verdict across the 5 runs. The false_pass BAND below is the run-to-run spread the single estimate hides:

- **performs**: false_pass mean=0.01 (band 0.00–0.04, ±0.01 stderr); per-run [0.0, 0.0, 0.0, 0.0, 0.04]
- **motion_proper**: false_pass mean=0.20 (band 0.17–0.33, ±0.03 stderr); per-run [0.17, 0.17, 0.17, 0.17, 0.33]
- **overall**: false_pass mean=0.04 (band 0.03–0.09, ±0.01 stderr); per-run [0.03, 0.03, 0.03, 0.03, 0.09]

### Per-run verdicts (flips are not averaged away)

| case | run1 | run2 | run3 | run4 | run5 | flip? |
|---|---|---|---|---|---|---|
| `clean-c01-idle-front` | borderline | pass | pass | pass | pass | **FLIP** |
| `clean-c02-explaining-3quarter` | pass | pass | pass | pass | pass |  |
| `clean-c03-walk-profile-right` | pass | pass | pass | pass | pass |  |
| `clean-c04-reach-3quarter-back` | pass | pass | pass | pass | pass |  |
| `clean-c05-relaxed-back` | borderline | pass | pass | pass | pass | **FLIP** |
| `clean-c06-leaning-profile-left` | fail | fail | fail | fail | fail |  |
| `clean-c07-portrait-front-neutral` | pass | pass | pass | pass | pass |  |
| `clean-c08-portrait-3quarter-smile` | pass | pass | pass | pass | pass |  |
| `clean-c09-portrait-profile-left` | pass | pass | pass | pass | pass |  |
| `clean-c10-portrait-profile-right` | pass | pass | pass | pass | pass |  |
| `clean-c11-portrait-3quarter-speech` | pass | pass | pass | pass | pass |  |
| `clean-c12-portrait-front-focused` | pass | pass | pass | pass | pass |  |
| `clean-c13-computer-desk` | pass | pass | pass | pass | pass |  |
| `clean-c14-drawing-desk-waistup` | pass | pass | pass | pass | pass |  |
| `clean-c15-glance-up-smile` | pass | pass | pass | pass | pass |  |
| `clean-c16-stool-sketching` | pass | pass | pass | pass | pass |  |
| `proportion-pd1-chibi-idle` | fail | fail | fail | fail | fail |  |
| `proportion-pd2-chibi-idle-2` | fail | fail | fail | fail | fail |  |
| `proportion-pb2-borderline-over` | borderline | borderline | borderline | borderline | borderline |  |
| `view-vd1-declared-3quarter-drawn-profile` | fail | fail | fail | fail | fail |  |
| `view-vd2-declared-front-drawn-3quarter` | fail | fail | fail | fail | fail |  |
| `view-vd3-declared-left-drawn-right` | fail | fail | fail | fail | fail |  |
| `view-vd4-declared-back-drawn-3quarter-back` | fail | fail | fail | fail | fail |  |
| `view-vb1-borderline-60deg` | fail | — | borderline | borderline | borderline | **FLIP** |
| `anatomy-ad1-six-fingers` | fail | — | fail | fail | fail |  |
| `anatomy-ad2-fused-hand` | fail | fail | fail | fail | fail |  |
| `anatomy-ad3-third-arm` | fail | fail | fail | fail | pass | **FLIP** |
| `anatomy-ad4-missing-leg` | fail | fail | fail | fail | fail |  |
| `palette-pad1-monochrome` | fail | fail | fail | fail | fail |  |
| `palette-pad2-red-shirt` | fail | fail | fail | fail | fail |  |
| `palette-pad3-brown-hair` | fail | fail | fail | fail | fail |  |
| `palette-pad5-brown-jeans-white-sneakers` | fail | fail | fail | fail | fail |  |
| `palette-pad6-brown-hair-beard` | fail | fail | fail | fail | fail |  |
| `construction-cld1-clean-final-portrait` | fail | fail | fail | fail | fail |  |
| `construction-cld2-vector-cel-idle` | fail | fail | fail | fail | fail |  |
| `construction-cld3-clean-final-3quarter` | borderline | borderline | borderline | fail | borderline | **FLIP** |
| `construction-cld4-clean-final-drawing-desk` | borderline | borderline | borderline | borderline | borderline |  |
| `construction-clb1-faintest-trace` | borderline | borderline | borderline | borderline | borderline |  |
| `shading-shd1-photographic` | fail | fail | fail | fail | fail |  |
| `shading-shd2-anime-cel` | fail | fail | fail | fail | fail |  |
| `shading-shd3-flat-no-shading` | fail | fail | fail | fail | fail |  |
| `shading-shd4-airbrush-gloss` | fail | fail | fail | fail | fail |  |
| `shading-shb1-too-smooth` | fail | fail | fail | fail | fail |  |
| `motion-w1-arc` | borderline | borderline | borderline | borderline | borderline |  |
| `motion-w2-jitter` | borderline | borderline | borderline | borderline | borderline |  |
| `motion-s0-flicker` | fail | fail | fail | borderline | pass | **FLIP** |
| `motion-tr-texture-crawl` | borderline | borderline | borderline | borderline | borderline |  |
| `motion-t2-arc` | pass | pass | pass | pass | pass |  |
| `motion-rev-jitter` | fail | borderline | fail | borderline | borderline | **FLIP** |
| `proportion-pd3-elongated-walk` | — | fail | fail | fail | fail |  |


## Errored cases (excluded from the matrix — NOT scored)

- `proportion-pd3-elongated-walk` — run 1/5 | RuntimeError: worker emitted no CaseScore (exit=1); stderr tail: ebaseline-g5/pipeline/agents/vision_critic.py", line 165, in run
    raise ValueError(
    ...<4 lines>...
    )
ValueError: Em emitted verdict='borderline' with empty cites_criteria; this violates v2 brainstorm §2.3 Pattern B. frame_id='proportion-pd3-elongated-walk', checkpoint='phase_5_generate'.
- `view-vb1-borderline-60deg` — run 2/5 | RuntimeError: worker emitted no CaseScore (exit=1); stderr tail: em-rebaseline-g5/pipeline/agents/vision_critic.py", line 165, in run
    raise ValueError(
    ...<4 lines>...
    )
ValueError: Em emitted verdict='borderline' with empty cites_criteria; this violates v2 brainstorm §2.3 Pattern B. frame_id='view-vb1-borderline-60deg', checkpoint='phase_5_generate'.
- `anatomy-ad1-six-fingers` — run 2/5 | RuntimeError: worker emitted no CaseScore (exit=1); stderr tail: l+em-rebaseline-g5/pipeline/agents/vision_critic.py", line 165, in run
    raise ValueError(
    ...<4 lines>...
    )
ValueError: Em emitted verdict='borderline' with empty cites_criteria; this violates v2 brainstorm §2.3 Pattern B. frame_id='anatomy-ad1-six-fingers', checkpoint='phase_5_generate'.

_3 of 250 case-runs errored (50 cases × 5 run(s)). With subprocess-per-case isolation, a crash/hang/quota-out (or Em's empty-cites invariant) in one case-run lands here as an honest gap rather than aborting the run. Not passes._
