# Maya — observed failure-mode taxonomy

The eval suite catches three families of failure today. Each family is named,
illustrated by a real eval case, and pointed at a fix vector. The list grows
as real planning runs surface modes the cases didn't predict.

---

## 1. criteria-too-vague-to-test

**What it looks like.** Maya emits a criterion like `AC.tone.feel-melancholy`
that no critic can verifiably evaluate. Em refuses to ground a borderline
verdict against it (the `cites_criteria` invariant fires), but the cost is one
wasted T2 call before the refusal lands.

**How it surfaces in the eval suite.** The `ambiguous-tone-brief` case
documents this — the Studio Brief contradicts itself ("warm but melancholy,
urgent but slow"), Maya emits a criterion that inherits the contradiction,
and the adversarial Sonnet pass flags it as untestable. The 3-call revision
path fires; the revised plan tightens the criterion.

**Fix vectors.** Tighten Maya's prompt to refuse interpretive criteria
without a measurable handle. The adversarial Sonnet pass is the structural
backstop — even when Maya emits a vague criterion, Sonnet's job is to find it.
Future tightening: a separate `criteria-tightness` rubric Maya self-scores
against before returning the plan.

## 2. cost-line-under-estimates-by-2x+

**What it looks like.** Maya's cost preview is off by ≥2× because the
manifest's `generation.routing:` block is incomplete (no hero/standard split
declared, or `seconds_per_clip` set to a default that doesn't match the
brief's actual runtime). Sean approves a plan he thinks costs $5; the real
run hits $12.

**How it surfaces in the eval suite.** The `cost-undercount-trap` case is
the structural guard — declares 50 hero-tier keyframes in the manifest with
hero pricing $0.15/frame and verifies the median doesn't drop below $3.
The case currently passes because the estimator's `_phase_5_cost` uses
hero pricing for every frame when `frame_count_standard: 0`. Adding a 50%
escalation assumption (hero pricing × 2 attempts for the median band) would
move this from "documented baseline" to "actively tightening."

**Fix vectors.** Validate manifest completeness inside `CostEstimatorNode` —
warn (not error) when routing is missing pricing data. The Sonnet adversarial
pass also looks for under-estimates by ≥2× as one of three named flags.
Long-term: seed the median band with historical pass-rate data once 3+ real
planning runs exist (the ENG4 deferred item in the Maya brainstorm).

## 3. impact_tag-mismatch

**What it looks like.** A criterion marked `impact_tag: aesthetic` should
have been `impact_tag: identity_critical`. Example: "the character's stylus
stays in their right hand" — that's a structural identity rule, not an
aesthetic preference. Em's escalation hatch keys off `impact_tag`, so the
mistag means Em doesn't force Opus on the frames that should always get
heavier review.

**How it surfaces in the eval suite.** The current cases don't directly
exercise this — every fixture brief leaves the impact_tag assignment to
`make_planning_envelope`'s closed mapping, which is correct by construction.
The failure mode is real in production, just not yet captured here.

**Fix vectors.** Add a dedicated case (`impact-tag-mismatch-non-negotiable`)
where the Studio Brief's "non-negotiables" section names an identity-level
rule, Maya emits the criterion with `impact_tag: aesthetic`, and Sonnet's
adversarial pass flags the mismatch. Until then, this mode is documented
but not regression-tested.

---

## 4. under-spec-brief-ships-thin-plan (intentionally red — XFAIL)

**What it looks like.** Studio Brief is missing fields (no deadline, no
target medium, no concrete non-negotiables). Maya ships a thin plan with
a confidence note rather than refusing.

**How it surfaces in the eval suite.** The `under-spec-brief-needs-
clarification` case carries `is_intentionally_red: true`. The case xfails by
design; the failure is the artifact.

**Fix vectors.** Maya's prompt should detect under-spec and respond with
"Sean — tighten the Studio Brief at sections X, Y, Z before re-running"
rather than emitting a plan. This is prompt iteration territory, not a
schema change. Promote out of red when Maya's prompt stabilizes (3+ real
planning runs against under-spec briefs).

---

*Eval discipline: pre-fix → post-fix improvement is the portfolio content.
Cases ship red intentionally where the failure documents a real production
gap. The list grows as real runs surface modes the seed cases didn't predict.*
