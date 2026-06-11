---
piece_id: the-spark-shared
phases_enabled: [1, 4, 5, 7, 8, 9]
characters_loaded: [sean-anchor, claude-mascot]
target_medium: looping browser GIF / WebM (two-character loop on twos)
target_runtime_s: 0.83
deadline: soft
routing_tier_defaults: standard
retry_budget_per_frame: 3
---

# Production Brief — The Spark, Shared

## Production notes

The first integrated run of the whole fleet on one piece. Deliberately small: five hand-drawn keyframes, two locked characters, one continuous shoulder two-shot that loops. Phase 2 is already in the can — both Bibles (sean-anchor, claude-mascot) are authored and locked in the pencil-test-colored register — so no Bible bake runs here. Phase 6 (Seedance) is out of scope; this is a keyframe loop on twos, not interpolated video.

One generation chain, not two. F01 is the compositional anchor, built from both Bible anchors plus the A-7 pairing reference; every later frame chains from the previous approved frame so both identities and the shoulder placement hold. F05 is composed to return to F01 so the cycle reads continuous.

The whole run exists to prove one thing: that NB2 can hold two characters together — Sean and the mascot, both identities, the shoulder placement — across five chained frames, in the pencil-test-colored register, with the reaction living entirely on the mascot while Sean stays heads-down. Every prior NB2 win was single-character. That asymmetry is both the story and the bet.

## Per-phase routing overrides

Standard tier (NB2, gemini-3.1-flash-image-preview, $0.07/frame) on all five frames. Zero hero frames — the establishing frame anchors the chain rather than routing to NB Pro, a deliberate reliability call the brief makes explicit. Retry budget is three per frame; the fourth attempt stops and flags for Sean. Em escalates to Opus on every frame that trips an identity-critical criterion, and after the adversarial review there are now five of those (see Risks). No Phase 6 routing. Phase 8 assembles locally in FFmpeg.

## Risks Maya flagged

- Two-character holds are the unproven thing. Generating Sean and the mascot together and holding both identities plus the shoulder placement across five chained frames is exactly what this run tests — and the morph-through-a-sequence failure is the one Flo-B caught in the fal models. If frames routinely exhaust retries to human review, the high cost band and the soft deadline both move. Mitigation: anchor F01 hard, chain aggressively, let Em escalate to Opus on every identity-critical trip.

- The delight beat may need a plate the Bible does not carry. The mascot's authored vocabulary covers idle / look / alert / perch / hop / sleep plus six expressions; confirm a `delight` plate exists or budget one additive plate before Phase 5. If it is missing, a small additive cost reappears that the headline estimate does not carry.

- The clean loop has no deterministic gate. F05 to F01 is an Em-plus-Sean judgment, not a T1 rule. The Phase 9 gate needs a human look at the cycle playing, not just per-frame quality.

- Tone mis-tag — caught and resolved in adversarial review. The first criteria draft folded the piece's narrative premise (mascot reacts, Sean stays absorbed) into one aesthetic-tagged criterion, which would not have tripped Em's Opus escalation — leaving the one thing this run exists to prove riding on a flash-tier read. The premise is now split into `AC.identity.sean-stays-absorbed` and `AC.tone.mascot-carries-reaction`, both identity_critical; only the genuinely interpretive taste call (`AC.tone.delight-small-not-gag`) stays aesthetic. This raises the identity-critical count from three to five, which is intended — it is the cost of guarding the premise at the right tier, and it will raise expected retry depth on the two-character frames.

- Cost realism. The estimator headline carries a Phase 2 Bible-bake band this run will not spend (both Bibles are locked). Plan to the Phase 5 median ($0.93); hold the high band ($2.25) as the two-character-retry contingency. The realized total hinges entirely on retry depth.
