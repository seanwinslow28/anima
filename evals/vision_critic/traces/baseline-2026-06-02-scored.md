# Em — scored baseline (2026-06-02 19:42 UTC)

Model: **production: gemini-3.5-flash@gemini_api + opus-4.7-escalation**  ·  cases: 24

Metric contract: precision/recall on the defect class; **false-pass rate front and center** (the costly error). Raw agreement is NOT the headline (class imbalance); F1 is secondary. Segmented per Sean's call: identity/style+clean ('performs') reported apart from motion-proper (expected-red — the contact sheet structurally can't see motion).

### Performs (identity/style + clean)  (n=23)

- confusion: TP=11 FP=4 FN=2 TN=6
- **precision=0.73  recall=0.85**  (recall ±0.10)
- **false_pass_rate=0.15**  (false passes: proportion-eyes-body-profile-right, stylus-hand-f13-cc01)
- 3-way exact agreement=0.65
- borderline->fail slippages: proportion-jaw-body-profile-left, proportion-eyes-body-profile-right, stylus-hand-f13-cc01
- cites-correct: 0.80
- mean wall: 75.9s

### Motion-proper (expected red)  (n=1)

- confusion: TP=1 FP=0 FN=0 TN=0
- **precision=1.00  recall=1.00**  (recall ±0.00)
- **false_pass_rate=0.00**  (false passes: none)
- 3-way exact agreement=1.00
- borderline->fail slippages: none
- cites-correct: 0.00
- mean wall: 98.6s

### Overall  (n=24)

- confusion: TP=12 FP=4 FN=2 TN=6
- **precision=0.75  recall=0.86**  (recall ±0.09)
- **false_pass_rate=0.14**  (false passes: proportion-eyes-body-profile-right, stylus-hand-f13-cc01)
- 3-way exact agreement=0.67
- borderline->fail slippages: proportion-jaw-body-profile-left, proportion-eyes-body-profile-right, stylus-hand-f13-cc01
- cites-correct: 0.75
- mean wall: 76.9s


## Intentionally NOT live-scored (segment scoping)

- `motion-w2-jitter` (motion_proper)
- `motion-s0-flicker` (motion_proper)
- `motion-tr-texture-crawl` (motion_proper)
- `motion-t2-arc` (motion_proper)
- `motion-rev-jitter` (motion_proper)

_5 motion_proper case(s) excluded from this live run. A still-image contact sheet structurally cannot score motion-proper (eval-strategy §3.5); these are the deferred E_warp/VBench validation set, not a live-Em measurement. One motion case WAS run live as a phase-6 reference-attach smoke check. This is scoping, not truncation._
