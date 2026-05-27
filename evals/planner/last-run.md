# Maya — planner eval suite, baseline trace

**Date:** 2026-05-27
**Run command:** `.venv/bin/pytest evals/planner/runner.py -v`
**Result:** 5 passed, 1 xfailed
**Notes:** First run of the suite. Stub-fallback path — Maya's runners are
mocked via `monkeypatch` in `runner.py`'s `_patch_runners` helper, so this
baseline measures the contract layer, not real Opus/Sonnet behavior.

---

## What this trace captures

The structural baseline for Maya — six seed cases drawn from the v2 brainstorm
+ the Maya brainstorm's TOP-1 + TOP-5 + the cost ceiling discipline. Each case
threads a fixture Studio Brief and a fixture manifest through Maya with mocked
SDK responses, then asserts against an `expected` block: plan emission, criteria
count + category coverage, cost band, exact Opus + Sonnet call counts, the
clean-markdown invariant.

This is the pre-fix reference point. When commit 3b ships against real Opus +
Sonnet (Sean's Anthropic Pro subscription absorbs both), a second `last-run.md`
lands documenting how real-model behavior diffs from the stub baseline.

---

## Per-case results

| Case | Result | Branch exercised | Notes |
|------|--------|------------------|-------|
| `pencil-test-act1-reproduction` | ✅ PASS | clean Sonnet → 2 calls total | Cost median $7.77 within [1.0, 30.0] range — matches v2 §7 baseline ($5–40 Phase 5, $10–20 Phase 6). |
| `multi-character-scene` | ✅ PASS | clean Sonnet → 2 calls total | Both `identity` and `continuity` categories present per multi-character handling. |
| `authoring-first-bible` | ✅ PASS | clean Sonnet → 2 calls total | Phase-2-only run; cost stays under $10 (no Phase 5 or 6 compute). |
| `ambiguous-tone-brief` | ✅ PASS | flag → revision Opus → 3 calls total | Adversarial Sonnet surfaces `AC.tone.warm-and-melancholy` as untestable; revision Opus emits a tightened plan. |
| `under-spec-brief-needs-clarification` | ⚠️ XFAIL | low-signal → second Opus → 3 calls total | Intentionally red — Maya ships a thin plan when the right behavior is to refuse with a "tighten brief" message. See failure-modes.md §4. |
| `cost-undercount-trap` | ✅ PASS | clean Sonnet → 2 calls total | 50-hero-frame piece returns a median ≥ $3; estimator doesn't under-estimate. |

---

## What this baseline locks in

Five things, ordered by load-bearing weight:

1. **Maya's contract holds under stub-fallback.** Plan + criteria + production
   brief + cost preview emit cleanly across six diverse cases. The
   `00_studio_brief.md` precondition fires on missing input. The
   clean-markdown invariant survives every test.

2. **The three-phase loop's three branches all exercise.** Clean (2 calls),
   real-flag → revision (3 calls), low-signal → second-Opus (3 calls). The
   four-artifact emission is identical across branches.

3. **The graph criteria schema validates end-to-end.** Mnemonic IDs match
   `AC.{category}.{handle}`, categories belong to the closed vocab, impact
   tags belong to the closed vocab. The `category_must_include` assertion
   exercises the persona-routing edges (Em cites identity + tone; Cy cites
   identity + proportion).

4. **The cost estimator's bands match v2 §7's stated ranges.** Phase 5
   keyframes priced from the routing block; Phase 6 Seedance Fast→Pro at
   the 30% escalation rate; subscription-absorbed phases at $0 incremental.

5. **The under-spec failure mode is documented + red.** This is the eval
   discipline lift from Hamel Husain — pre-fix red cases are the portfolio
   content. When Maya's prompt tightens to refuse under-spec briefs, the
   case flips green and the diff is the museum walkthrough.

---

## What's NOT in this baseline

- **Real Opus + Sonnet behavior.** Every response is mocked through
  `_patch_runners`. The real-model trace lands after Sean runs the
  authenticated `claude-agent-sdk` against the same cases.
- **Cost-estimator-against-real-pricing variance.** The fixtures use the v2
  §7 baseline prices; production runs may show drift as Flo's routing table
  evolves.
- **Cross-piece consistency.** Each case is independent. The ENG4 deferred
  item — Maya's standing-context carrying a historical-plan corpus — lands
  after 3+ real planning runs exist.
- **The `impact_tag-mismatch` failure mode.** Documented in failure-modes.md
  §3 but not yet captured by a dedicated case. Add when a real run surfaces
  one.

---

*Next run: re-run after the next prompt iteration on Maya (especially
sharpening the under-spec refusal). Compare per-case branch and call count.
The diff is the artifact.*
