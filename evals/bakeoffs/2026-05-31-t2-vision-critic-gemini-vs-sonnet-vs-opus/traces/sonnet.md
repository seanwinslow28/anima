# Em — scored baseline (2026-06-01 14:40 UTC)

Model: **claude-sonnet-4-6-via-sdk**  ·  cases: 29

Metric contract: precision/recall on the defect class; **false-pass rate front and center** (the costly error). Raw agreement is NOT the headline (class imbalance); F1 is secondary. Segmented per Sean's call: identity/style+clean ('performs') reported apart from motion-proper (expected-red — the contact sheet structurally can't see motion).

### Performs (identity/style + clean)  (n=23)

- confusion: TP=13 FP=10 FN=0 TN=0
- **precision=0.57  recall=1.00**  (recall ±0.00)
- **false_pass_rate=0.00**  (false passes: none)
- 3-way exact agreement=0.48
- borderline->fail slippages: proportion-eyes-body-profile-right, stylus-hand-f13-cc01
- cites-correct: 0.48
- mean wall: 58.1s

### Motion-proper (expected red)  (n=6)

- confusion: TP=6 FP=0 FN=0 TN=0
- **precision=1.00  recall=1.00**  (recall ±0.00)
- **false_pass_rate=0.00**  (false passes: none)
- 3-way exact agreement=0.17
- borderline->fail slippages: motion-w2-jitter, motion-s0-flicker, motion-tr-texture-crawl, motion-t2-arc, motion-rev-jitter
- cites-correct: 0.00
- mean wall: 83.2s

### Overall  (n=29)

- confusion: TP=19 FP=10 FN=0 TN=0
- **precision=0.66  recall=1.00**  (recall ±0.00)
- **false_pass_rate=0.00**  (false passes: none)
- 3-way exact agreement=0.41
- borderline->fail slippages: proportion-eyes-body-profile-right, stylus-hand-f13-cc01, motion-w2-jitter, motion-s0-flicker, motion-tr-texture-crawl, motion-t2-arc, motion-rev-jitter
- cites-correct: 0.38
- mean wall: 63.3s
