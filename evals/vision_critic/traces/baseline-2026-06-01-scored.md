# Em — scored baseline (2026-06-01 11:01 UTC)

Model: **production: gemini-3.1-pro@agy + opus-4.7-escalation**  ·  cases: 29

Metric contract: precision/recall on the defect class; **false-pass rate front and center** (the costly error). Raw agreement is NOT the headline (class imbalance); F1 is secondary. Segmented per Sean's call: identity/style+clean ('performs') reported apart from motion-proper (expected-red — the contact sheet structurally can't see motion).

### Performs (identity/style + clean)  (n=23)

- confusion: TP=13 FP=8 FN=0 TN=2
- **precision=0.62  recall=1.00**  (recall ±0.00)
- **false_pass_rate=0.00**  (false passes: none)
- 3-way exact agreement=0.57
- borderline->fail slippages: proportion-eyes-body-profile-right
- cites-correct: 0.43
- mean wall: 34.9s

### Motion-proper (expected red)  (n=6)

- confusion: TP=6 FP=0 FN=0 TN=0
- **precision=1.00  recall=1.00**  (recall ±0.00)
- **false_pass_rate=0.00**  (false passes: none)
- 3-way exact agreement=0.00
- borderline->fail slippages: motion-w1-arc, motion-w2-jitter, motion-s0-flicker, motion-tr-texture-crawl, motion-t2-arc, motion-rev-jitter
- cites-correct: 0.00
- mean wall: 57.1s

### Overall  (n=29)

- confusion: TP=19 FP=8 FN=0 TN=2
- **precision=0.70  recall=1.00**  (recall ±0.00)
- **false_pass_rate=0.00**  (false passes: none)
- 3-way exact agreement=0.45
- borderline->fail slippages: proportion-eyes-body-profile-right, motion-w1-arc, motion-w2-jitter, motion-s0-flicker, motion-tr-texture-crawl, motion-t2-arc, motion-rev-jitter
- cites-correct: 0.33
- mean wall: 39.5s
