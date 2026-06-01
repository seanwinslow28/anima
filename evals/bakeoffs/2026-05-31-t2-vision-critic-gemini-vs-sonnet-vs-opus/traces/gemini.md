# Em — scored baseline (2026-06-01 14:32 UTC)

Model: **gemini-3.1-pro-via-anti-gravity**  ·  cases: 29

Metric contract: precision/recall on the defect class; **false-pass rate front and center** (the costly error). Raw agreement is NOT the headline (class imbalance); F1 is secondary. Segmented per Sean's call: identity/style+clean ('performs') reported apart from motion-proper (expected-red — the contact sheet structurally can't see motion).

### Performs (identity/style + clean)  (n=23)

- confusion: TP=13 FP=10 FN=0 TN=0
- **precision=0.57  recall=1.00**  (recall ±0.00)
- **false_pass_rate=0.00**  (false passes: none)
- 3-way exact agreement=0.17
- borderline->fail slippages: proportion-drift-body-3quarter, proportion-jaw-body-profile-left, proportion-eyes-body-profile-right, proportion-costume-body-back, sprite-scale-f31-bad, stylus-hand-f13-cc01, proportion-walk-cycle-source, identity-head-turn-01, jaw-drift-head-turn-09
- cites-correct: 0.00
- mean wall: 2.2s

### Motion-proper (expected red)  (n=6)

- confusion: TP=6 FP=0 FN=0 TN=0
- **precision=1.00  recall=1.00**  (recall ±0.00)
- **false_pass_rate=0.00**  (false passes: none)
- 3-way exact agreement=0.00
- borderline->fail slippages: motion-w1-arc, motion-w2-jitter, motion-s0-flicker, motion-tr-texture-crawl, motion-t2-arc, motion-rev-jitter
- cites-correct: 0.00
- mean wall: 1.9s

### Overall  (n=29)

- confusion: TP=19 FP=10 FN=0 TN=0
- **precision=0.66  recall=1.00**  (recall ±0.00)
- **false_pass_rate=0.00**  (false passes: none)
- 3-way exact agreement=0.14
- borderline->fail slippages: proportion-drift-body-3quarter, proportion-jaw-body-profile-left, proportion-eyes-body-profile-right, proportion-costume-body-back, sprite-scale-f31-bad, stylus-hand-f13-cc01, proportion-walk-cycle-source, identity-head-turn-01, jaw-drift-head-turn-09, motion-w1-arc, motion-w2-jitter, motion-s0-flicker, motion-tr-texture-crawl, motion-t2-arc, motion-rev-jitter
- cites-correct: 0.00
- mean wall: 2.1s
