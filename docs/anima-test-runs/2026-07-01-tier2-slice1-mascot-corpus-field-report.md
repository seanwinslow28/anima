# Field report — Tier-2 Slice 1: the mascot eval corpus + reference-blind baseline

**Date:** 2026-07-01 (run completed 2026-07-01 01:29 UTC; Sean ratified 2026-07-01).
**Operator:** Claude Code (Opus 4.8), in-session, operator-driven. Sean made every taste call (baseline protocol fork, ratification) and generated + ratified the fixtures.
**Scope:** pure measurement — nothing in Em (`pipeline/agents/vision_critic.py`) changed. PR #66 (rebase-merged to main).
**Kickoff:** [`docs/active/2026-06-22-tier2-mascot-corpus-kickoff.md`](../active/2026-06-22-tier2-mascot-corpus-kickoff.md) · **design:** [`docs/active/2026-06-22-tier2-mascot-corpus-design.md`](../active/2026-06-22-tier2-mascot-corpus-design.md) · **trace:** [`evals/vision_critic/traces/mascot-baseline-2026-06-30.md`](../../evals/vision_critic/traces/mascot-baseline-2026-06-30.md).

---

## Why this slice existed

Every Em-vs-eye gap we'd measured — the 2026-06-21 finish-register borderlines, the 2026-06-18 leg-count blind spot — was on the **mascot**. But the vision-critic eval corpus was 52 cases, 100% `sean`, zero mascot. So the calibration we actually want (Slice 2) was blocked on measurement: you can't tune Em against the mascot without a ratified mascot corpus and a baseline number to gate against. Slice 1 makes the mascot measurable and nothing more. Because it changes nothing in Em, it *cannot* regress the frozen verdict-baseline md5 — the safest possible entry into Tier-2.

## What ran (the sequence)

Part 0 (verify, $0) → Part 1 (ingest close + tooling, $0, TDD) → Part 2 (the one costed baseline) → Part 3 (docs + PR). The ingest itself (46 fixtures + 46 cases) was already done in a prior Cowork session; this run verified it, added the missing tooling, ran the baseline, and shipped.

## Result — the mascot verdict baseline (ratified-with-notes)

Reference-blind, N=5 majority vote, gemini-3.5-flash pinned + Opus-4.7 escalation — sean's **G5 protocol**, run scoped to the 46 mascot cases:

| Segment | n | precision | recall | false-pass | cites-correct |
|---|---|---|---|---|---|
| **performs** (clean + identity_style) | 46 | **0.93** | **0.90** | **0.10** | 0.17 |

0 errored gaps, ~25s/case mean wall. TP=27 FP=2 FN=3 TN=14. False-pass band across the 5 runs: 0.07–0.10 (±0.01). (Motion segment n=0 — the mascot corpus authored no motion_proper cases, correctly; motion-sight stays a sean-only concern.)

**vs sean's G5 (0.97 / 1.00 / 0.00) the mascot is measurably weaker — and that gap is the deliverable, not a defect to fix here.** Per ships-red discipline, nothing was tuned to flatter Em.

### The seam (the Slice-2 signal)

The weakness is not spread across classes — it is **concentrated in one class**:

- **All 3 false-passes are the construction-lines-absent class** (`cld1/cld2/cld3-cleaned-*`). Reference-blind, Em passes a cleaned-up final that has no visible pencil under-drawing. Critically, on the *runs where she does catch it* she cites `IR.claude-mascot.face.construction-cross-line` **correctly** (0.98–1.00 conf) — so this is a **detection-sensitivity gap, not a grounding gap.** The majority verdict lands on pass because the "absence of a faint feature" is a low-salience read for a still-image MLLM. This is exactly the finish-register drift the 2026-06-21 driven run flagged by eye. **Construction-lines detection is the priority Slice-2 target.**
- **2 clean false-positives** — `clean-c02-curious-3q` and `clean-c07-face-front-neutral`, borderline in all 5 runs. Sean's ratification call: **accepted red — Em over-caution, not tuned** (ships-red; revisit in Slice-2 calibration, not now).
- **cites-correct 0.17** is the expected reference-blind citation floor (sean's blind G5 was 0.03). The view-correctness class cites a **seam handle** — the mascot Bible has no `view` category (sean got 5 `IR.sean.view.*` in G6.1; the mascot never did) — and the geometry classes lack citeable rules. The criteria-text lever (held OFF here for G5-comparability) is the obvious Slice-2 experiment against this blind floor.

## Candid seams in the *process* (what future sessions should read first)

1. **The kickoff was wrong about a load-bearing fact — the tree caught it, the label didn't.** The kickoff (and my own approved plan) stated "both attach flags default OFF — reference-blind confirmed." False: **G6.1b flipped `critics.t2.attach_criteria_text: true` in the production manifest** (2026-06-08, *after* sean's G5). The "confirmed" came from reading the argparse defaults, not the manifest value. A default `score` run today is criteria-text mode, not blind. Caught only by checking the manifest against the tree at spend-time. **Lesson: verify the manifest state against the tree even when the kickoff says "confirmed" — especially for anything the production config could have moved since the doc was written.**

2. **`store_true` flags can't force a lever OFF.** `--attach-references` / `--attach-criteria-text` can only turn levers on. To run blind against a manifest that ships criteria-text on, a new `--reference-blind` override had to exist — forcing both levers off through the single `_apply_attach_flags` point and **propagating to every per-case worker** (the worker re-reads manifest.yaml from disk, so without forwarding, criteria text would silently re-attach — the exact 2026-06-07 "measured nothing because a flag was silently on" failure mode). This was a third, unplanned-but-necessary tooling add; Sean chose reference-blind per the kickoff knowing it required it.

3. **The C02/C03 byte-identical dupe the contamination guard couldn't see.** Two "distinct" clean fixtures came out of Flow byte-identical (C03's declared left-side view *was* C02's three-quarter). The existing guard only checks fixture-vs-`characters/`/`images/` — it is blind to fixture-vs-fixture. Sean re-rolled C03 ($0 in Flow); the new **intra-corpus dupe guard** (no two fixtures share a SHA-256) closes the class. Verified failing on a planted dupe, passing clean.

4. **The working tree was a three-body mess.** The ingest was intermixed with two unrelated prior-session WIP bodies (a Higgsfield Seedance pass; the 2026-06-29 vision-expansion scoping), including intermixed hunks in the *same* CHANGELOG/ROADMAP files, with `git add -p` unavailable. Resolution (Sean's call: "commit unrelated WIP first"): two isolation commits, splitting the shared-file hunks via `git diff` → patch-file surgery → `git apply --cached` so each body became its own commit. The mascot slice then built on a clean tree. **The 4-hour-earlier Explore inspection was stale** — it reported C02/C03 still identical and cases still `AWAITING`, but the tree at spend-time showed Sean's re-roll + ratification had landed. Re-verifying at the gate (not trusting the earlier read) is what caught it.

5. **A live smoke before the 2.5-hour burn paid off.** A `--limit 2` reference-blind live run confirmed the label flipped to `blind (attach_references off)` and that the Opus-4.7 escalation ran at 65s under the env-strip — not the ~94s nested-SDK throttle (seam #4). Without the env-strip, the escalation path on identity_critical cases would have degraded or returned empty.

## Ops notes

- **Billing:** subscription throughout (`ANTHROPIC_API_KEY` absent, enforced by score.py's env guard); `GEMINI_API_KEY` from `.env`.
- **Env-strip:** every costed command ran under the fleet-ops §6 strip set (`env -u CLAUDECODE -u CLAUDE_CODE_SESSION_ID …`). Canary fast; escalation un-throttled.
- **Spend:** ~230 live case-runs (46 × 5) + a handful of Opus escalations, ~25s/case mean, 0 errored gaps. In the ~$2–12 G5-comparable band, subscription-absorbed.
- **Trace isolation:** `--trace-name mascot-baseline-2026-06-30` wrote **only** its own trace; sean's `last-run.md` and the frozen g6.1b trace were never touched.
- **Guards held (asserted start + end):** `vision_critic.py` byte-unchanged; sean's 52 cases untouched (0 rows removed); g6.1b md5 `2af75906…` and voice md5 `945af824…` intact. 708 contract tests + mocked runner green.
- **Teardown:** branched in place (no separate worktree dir — the uncommitted ingest lived in the primary checkout; a fresh worktree off a committed ref wouldn't have contained it). Orphan sweep clean. PR #66 rebase-merged (not squashed — squash would have re-bundled the two prior-session WIP commits into the slice).

## Handoff to Slice 2 (the calibration)

The baseline is the gate. The concrete targets it surfaced, in rough priority:

1. **Construction-lines-absent detection** — the concentrated blind spot (3/3 false-passes). Test whether the criteria-text lever (grounding Em with `IR.claude-mascot.face.construction-cross-line`) lifts detection, and/or reference images. This is where the reference-blind-vs-criteria-text fork gets decided for the mascot.
2. **Leg-count / anatomy detection** — the 06-18 blind spot; the corpus now has the `A-D*` cases to measure it (they scored fine reference-blind here, but severity/threshold calibration is Slice-2's remit).
3. **The view seam handle → real `IR.claude-mascot.view.*` rules** — parallels sean's G6.1; would lift the view-class citation floor.
4. **The 2 clean FPs** (`clean-c02`, `clean-c07`) — re-examine as an over-caution calibration question, not a fixture change.

Any Slice-2 Em change is eval-gated against this baseline; the verdict-baseline md5 moves only on a deliberate, ratified re-baseline.
