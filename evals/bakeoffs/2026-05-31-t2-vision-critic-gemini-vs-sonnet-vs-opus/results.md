# T2 vision-critic bake-off — 2026-06-01

Gemini (agy) vs Sonnet (SDK) vs Opus (SDK). Only the model varies; prompt + standing context + cases held constant; no escalation.

**Model snapshots (pin these — the re-runnable baseline a future provider bump is checked against):**
- gemini: 3.1 Pro via **agy v1.0.3** (no model-pin flag — the agy binary version *is* the snapshot)
- sonnet: claude-sonnet-4-6 via claude-agent-sdk
- opus: claude-opus-4-7 via claude-agent-sdk

> ⚠ **The Gemini column below is INVALID** — Gemini's consumer-tier quota was exhausted mid-run (429 `RESOURCE_EXHAUSTED` in agy's log), so every agy call returned empty and Em's parser defaulted each to `borderline`. The 2.2s mean wall, 0.00 cites-correct, and TN=0 are the tells of a uniform-borderline degenerate, **not a model verdict**. The decision below rests on the two valid live columns (Sonnet, Opus) + the committed real Gemini-default baseline (`evals/vision_critic/last-run.md`). See the Decision.

## gemini-3.1-pro-via-anti-gravity

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


## claude-sonnet-4-6-via-sdk

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


## claude-opus-4-7-via-sdk

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

---

# Decision (2026-06-01)

**Bottom line: no change to the T2 default this session.** The live Gemini column is quota-invalid, and the whole comparison is reference-blind — neither condition can license a model swap. The valid output of this run is two *findings*, not a winner. `manifest.critics.t2.default_model` is left untouched (per the plan: no commit blocks on the outcome; a default change would be proposed to Sean as a separate decision, not silently edited).

## Validity gate (read this first)

| Variant | runner | mean wall | valid? | why |
|---|---|---|---|---|
| Gemini 3.1 Pro | agy v1.0.3 | **2.2s** | ❌ | quota 429 → empty stdout → parser default `borderline` (uniform degenerate; TN=0, cites 0.00) |
| Sonnet 4.6 | claude-agent-sdk | 58.1s | ✅ | real, differentiated verdicts + real citations |
| Opus 4.7 | claude-agent-sdk | 46.3s | ✅ | real, differentiated verdicts + real citations |

The committed real Gemini-default read is the baseline (`evals/vision_critic/last-run.md`, performs: prec **0.62** / recall **1.00** / false-pass **0.00** / cites-correct 0.43), which ran earlier today *before* the quota hit. The decision uses that as the Gemini stand-in.

## The valid comparison — Sonnet vs Opus (performs segment, the costly-error lens)

| Model | precision | recall | **false-pass** | exact-agree vs Sean | cites-correct | mean wall |
|---|---|---|---|---|---|---|
| **Sonnet 4.6** | 0.57 | **1.00** | **0.00** | 0.48 | **0.48** | 58.1s |
| **Opus 4.7** | **0.67** | 0.92 | **0.08** | **0.61** | 0.33 | 46.3s |
| *(Gemini baseline)* | *0.62* | *1.00* | *0.00* | *0.57* | *0.43* | *34.9s* |

**The right disagreements, not the fewest** (the Judge's-Verdict reframe). Opus *looks* better on the headline (higher precision 0.67, higher exact-agreement 0.61) — but that edge is bought by its willingness to *license a `pass` while reference-blind*: it passed 4 clean frames (TN=4) it could not actually verify against an anchor, and on the one case where that willingness was wrong it produced a **false pass** (`stylus-hand-f13-cc01` — a real CC01 stylus-hand defect waved through). For a critic, the false pass is the cardinal error; a drifted frame let through is far costlier than a clean frame re-queued. By that primary metric **Sonnet (false-pass 0.00) ≥ Opus (0.08)**, and Sonnet also cites best (0.48). Sonnet's profile is near-identical to the committed Gemini-default baseline (both false-pass 0.00, prec ~0.57–0.62, recall 1.00) — i.e. **Gemini-default and Sonnet are interchangeable on this suite; Opus is the outlier, and the wrong kind of outlier for a reference-blind critic.**

**This does not yet justify a default change**, because:
1. The Gemini live head-to-head is missing (quota) — the incumbent wasn't fairly on the field.
2. **All three are reference-blind** (the load-bearing finding — `docs/anima-test-runs/2026-06-01-em-reference-blindness-FINDING.md`). The over-flagging that drives every model's precision down (Sonnet & baseline-Gemini flag *all* 10 cleans, TN=0; Opus only escapes it by guessing passes it can't verify) is an *input* defect, not a model defect. No model choice fixes it. **Re-run this bake-off after references land** — that is the comparison that can actually pick a default.

## Metric-contract items

- **Confidence-vs-correctness:** not computable from this run's artifacts — `render_last_run_md` does not persist per-case confidence. Recorded as a known limit. Standing caveat (findings §3.4): verbalized confidence is miscalibrated; Em's `escalation_threshold: 0.7` therefore rests on a weak signal. Sampling-consistency-based escalation is a flagged **future** refinement — not built here.
- **Pairwise reframe (findings §3.5):** a "which of A/B reads closer to the anchor?" pairwise framing would sharpen exactly the clean-vs-drift calls reference-blindness muddles. Candidate for the reference-images workstream; not rebuilt here.
- **Pinned snapshots:** agy **v1.0.3** (corrects the harness docstring's stale `v1.0.2`; agy exposes no model-pin flag, so the binary version is the snapshot), `claude-sonnet-4-6`, `claude-opus-4-7`. A future provider bump is checked against these.

## Findings this bake-off surfaced

1. **Reference-blindness reconfirmed across models.** It is not a Gemini quirk — Sonnet shows the identical over-flag signature, and Opus only dodges it by licensing unverifiable passes (one of which became a false pass). Reinforces the locked #1 next fix: give Em the anchor + Bible plates.
2. **Latent rate-cap blind spot in `cli_runners.run_antigravity_with_image` (recorded, fix deferred to the reference-images workstream).** agy emits the 429 `RESOURCE_EXHAUSTED` to its *log file*, not stderr; the wrapper's `_RATE_CAP_SIGNALS` check only scans stderr, so a quota-exhausted **empty** response (exit 0) is reported `ok=True` and Em's parser defaults it to `borderline`. **A production live run during quota exhaustion would silently degrade every frame to `borderline` rather than erroring or escalating.** This is what invalidated the Gemini column here, and it is a real production-correctness gap. Fold the fix (treat empty-text/exit-0-with-no-JSON, and log-surfaced 429, as a rate-cap/error) into the reference-images session, which touches the same runner area.

**Deferred to the post-reference-fix session:** the complete, valid three-way bake-off (Gemini re-run after quota reset + the wrapper-bug fix + references attached). That is the run that can actually answer "does Gemini-default hold."

