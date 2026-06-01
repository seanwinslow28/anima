# Em — scored baseline (2026-06-01 14:44 UTC)

Model: **claude-opus-4-7-via-sdk**  ·  cases: 29

Metric contract: precision/recall on the defect class; **false-pass rate front and center** (the costly error). Raw agreement is NOT the headline (class imbalance); F1 is secondary. Segmented per Sean's call: identity/style+clean ('performs') reported apart from motion-proper (expected-red — the contact sheet structurally can't see motion).

### Performs (identity/style + clean)  (n=23)

- confusion: TP=12 FP=6 FN=1 TN=4
- **precision=0.67  recall=0.92**  (recall ±0.07)
- **false_pass_rate=0.08**  (false passes: stylus-hand-f13-cc01)
- 3-way exact agreement=0.61
- borderline->fail slippages: proportion-eyes-body-profile-right, stylus-hand-f13-cc01, jaw-drift-head-turn-09
- cites-correct: 0.33
- mean wall: 46.3s

### Motion-proper (expected red)  (n=6)

- confusion: TP=6 FP=0 FN=0 TN=0
- **precision=1.00  recall=1.00**  (recall ±0.00)
- **false_pass_rate=0.00**  (false passes: none)
- 3-way exact agreement=0.00
- borderline->fail slippages: motion-w1-arc, motion-w2-jitter, motion-s0-flicker, motion-tr-texture-crawl, motion-t2-arc, motion-rev-jitter
- cites-correct: 0.00
- mean wall: 34.4s

### Overall  (n=29)

- confusion: TP=18 FP=6 FN=1 TN=4
- **precision=0.75  recall=0.95**  (recall ±0.05)
- **false_pass_rate=0.05**  (false passes: stylus-hand-f13-cc01)
- 3-way exact agreement=0.48
- borderline->fail slippages: proportion-eyes-body-profile-right, stylus-hand-f13-cc01, jaw-drift-head-turn-09, motion-w1-arc, motion-w2-jitter, motion-s0-flicker, motion-tr-texture-crawl, motion-t2-arc, motion-rev-jitter
- cites-correct: 0.25
- mean wall: 43.9s
