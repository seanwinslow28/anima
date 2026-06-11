# Plan — The Spark, Shared

The first time the whole fleet runs one piece end to end. Five hand-drawn keyframes, two characters, one continuous two-shot that loops: Sean draws, the mascot notices and delights, then everything settles back to the start. Small on purpose — the loop is the proof, the run is the point. Maya plans it, Flo generates it, Em and the T3 council critique it, FFmpeg assembles it, Mo captures it to the museum.

## What this run executes

Phase 2 is already in the can: both Character Bibles (sean-anchor, claude-mascot) are authored and locked in the pencil-test-colored register, so no Bible bake runs here. Phase 6 (Seedance motion) is out of scope — this is a keyframe loop on twos, not interpolated video. What runs:

| Phase | Stage | Who | Compute |
|-------|-------|-----|---------|
| 1 | Scaffold | runner | free |
| 4 | Animatic / timing lock | Sean (human) | free — see the timing decision below |
| 5 | Generate (5 keyframes) | Flo + T1 + Em (T2) | ~$0.35–$2.25 |
| 7 | Audit / route findings | runner | free |
| 8 | Assemble (GIF/WebM loop) | FFmpeg + Em (T2) | free (local) |
| 9 | QA review | Sean + creative-director | free |
| — | Museum (parallel) | Mo + T3 pre-publish gate | $0 incremental |

## Casting

Flo routes every frame to standard tier (NB2). Em reads each frame against its beat and proposes prompt diffs on anything borderline — and because identity-critical tags ride every frame, Em forces an Opus pass on the hard calls rather than trusting flash alone. The T3 council (Codie, Annie, Sage, plus an Opus chairman) takes the last look before the museum exhibit publishes. Sean holds the gate at every lock.

## The five frames

One chain, not two. F01 is the compositional anchor — built from both Bible anchors plus the A-7 pairing reference — and every later frame chains from the previous approved frame so the two identities and the shoulder placement hold. F05 is composed to return to F01 so the cycle reads continuous.

| Frame | Beat | Reads as | References |
|-------|------|----------|------------|
| SS_F01_key | Establishing two-shot | Sean three-quarter at the desk, stylus to paper; mascot perched, idle | sean-anchor + claude-mascot anchors + A-7 pairing |
| SS_F02_key | The draw | Sean's hand moves on the page; mascot turns to look | F01 + mascot `look` plate |
| SS_F03_key | The notice | Mascot perks up — alert-perk, the catch | F02 + mascot `alert` plate |
| SS_F04_key | The delight | Mascot reacts with small, real delight; Sean stays on the work | F03 + mascot `delight` expression |
| SS_F05_key | The settle | Mascot eases back to idle; Sean's hand returns to start, looping to F01 | F04, composed to match F01 |

Asset naming follows the project convention with an `SS` prefix (Spark, Shared); confirm at scaffold.

## Routing and tiering

Standard tier (NB2, gemini-3.1-flash-image-preview, $0.07/frame) on all five. Zero hero frames. The establishing frame is the anchor the chain hangs from, not an NB Pro showpiece — the brief makes that an explicit reliability call, and the routing table's `frame_count_hero: 0` already reflects it. Retry budget is three per frame; the fourth attempt stops and flags for Sean.

## Timing decision (Phase 4)

The brief specifies on twos. For a five-key reaction beat that is a fast cycle — roughly 0.83s at 12fps — and the peak (the delight) and the rest (the establish) are the two beats that usually want to breathe. The call is yours: uniform on-twos, or variable holds with F01 and F04 held longer. Either way, lock the holds and the F05->F01 return before generation; that human-authored timing constraint is the animatic for a no-motion loop.

## Cost preview

The estimator's headline is $5.75 low / $7.95 median / $18.45 high — but that carries a Phase 2 band ($5.40 / $7.02 / $16.20) for a Bible bake this run will not do, because both Bibles are already locked. The spend that will actually land is the Phase 5 line: $0.35 low / $0.93 median / $2.25 high, at full estimator confidence. Phase 6 and Phase 8 are $0 (no Seedance; local FFmpeg). The agent fleet is subscription-absorbed: $0 incremental. Plan to the median; hold the high band as the two-character-retry contingency.

## The rubric, in plain English

Fourteen locked criteria. Five are identity-critical and force an Opus read on any frame that trips them: Sean stays Sean and the mascot stays the mascot with no morph through the sequence; the mascot holds its terracotta box-creature form and palette; the stylus stays in Sean's right hand and is visible in every frame; Sean stays absorbed in the work and never acknowledges the camera or the mascot; and the mascot carries the whole emotional arc from idle through delight to settle. Those last two are the piece's narrative premise — the asymmetry of reaction is the story — so they are weighted to escalate, not to be settled at flash tier. Continuity holds the mascot perched on the shoulder at consistent scale per the A-7 pairing. Structure keeps it one continuous two-shot and closes the loop F05 to F01. Tone carries the one genuinely interpretive call — that the delight reads small and earned rather than a gag — alongside the register check that every frame reads pencil-test-colored, which decomposes into the testable pair of cream paper texture and warm graphite line, never a digital render. Technical holds 16:9 within 2%, and records the all-NB2 tier choice for the walkthrough's provenance.

## Risks Maya flagged

The full margin notes live in the production brief. The three that move the schedule:

- Two-character holds are the unproven thing. Every prior NB2 win was single-character. Generating Sean and the mascot together, holding both identities and the shoulder placement across five chained frames, is exactly what this run exists to test — and the morph-through-a-sequence failure is the one Flo-B caught in the fal models. If frames routinely exhaust retries to human review, the high cost band and the soft deadline both move. Anchor F01 hard; chain aggressively; let Em escalate to Opus on every frame.

- The delight beat may need a plate that isn't in the Bible. The mascot's authored vocabulary covers idle/look/alert/perch/hop/sleep plus six expressions; confirm `delight` exists or budget one additive plate before Phase 5.

- The clean loop has no deterministic gate. F05 to F01 is an Em-plus-Sean judgment, not a T1 rule. The Phase 9 gate needs a human look at the cycle, not just per-frame quality.

## Maya's confidence notes

The adversarial pass caught a real mis-tag, and it is fixed. The first draft folded this piece's entire narrative premise — the mascot carries the reaction while Sean stays heads-down — into a single aesthetic-tagged criterion. Aesthetic tags do not trip Em's Opus escalation, so the one thing this whole run exists to prove would have ridden on a flash-tier read alone. The premise is now split and re-weighted: `AC.identity.sean-stays-absorbed` and `AC.tone.mascot-carries-reaction` are both identity-critical, so Em forces an Opus pass on any frame where Sean looks up at the camera or the mascot, or where the mascot fails to advance its beat. The cost is real and intended — the identity-critical count goes from three to five, which will deepen escalation (and retry depth) on the two-character frames, and that is exactly the spend the premise warrants.

Only one criterion stays genuinely interpretive: whether the delight reads small and earned rather than a gag (`AC.tone.delight-small-not-gag`). Em checks the mechanical proxy — the expression changed from the alert-perk — but the small-and-real-versus-over-played call is yours at the gate, which is why that one keeps the aesthetic tag while its parent escalates. The register check sits beside it as the same kind of taste call, backed by the testable paper-and-line proxies. Cost confidence is full on Phase 5; the realized total hinges on retry depth for the two-character frames. Phase 2 is assumed complete from the Studio Brief; if the `delight` plate is missing, a small additive cost reappears that this estimate does not carry.

## The gate

This is a draft. Review the rubric, edit the production brief, and run `pipeline plan approve` to lock the criteria. Nothing generates until you do.
