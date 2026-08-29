# EXPLANATION.md

A 4Q comprehension artifact (Nate B. Jones) for anima. The explanation that travels with the work: what this is, why this approach, what would break, what I learned.

---

## What is this?

A 2D-animation pipeline where a human owns timing, casting, and taste, and a fleet of seven named agents does the volume: generation, variation, in-betweens, critique, capture. A free-text brief flows through ten phases (plan, character bible, storyboard, animatic, generate, motion, audit, assemble, QA), and four of those phases stop and wait for a person's call. The premise is a hard line. Human creativity and AI creativity are different things, and pretending otherwise makes worse work. The agents propose; they don't decide.

The first shipped proof is the *Pencil Test* portfolio loop, a piece whose seven keyframes were generated first-try against human-drawn placement roughs. The repo is both the working system and the record of how it was built, post-mortems and cost figures included.

## Why this approach?

**The animatic is non-negotiable, and it is the load-bearing rejection.** The alternative, generating motion straight from a prompt, is the template trap: click-to-generate output with no human-authored constraint, which is exactly the product category this pipeline exists to not be. So a human blocks placement, facing, scale, even leg count in rough shapes *before* any model draws a frame. The `7 frames, 0 retries` result is that choice paying for itself. Constraint up front is cheaper than critique after.

**A three-tier critic stack instead of one smart judge.** T1 is deterministic rule gates (free, instant, every frame). T2 is a vision critic that proposes prompt diffs rather than just flagging. T3 is a heterogeneous multi-model council at phase boundaries. I didn't want a single LLM judge, because one model's blind spots become the pipeline's blind spots, and the critic-calibration saga (below) showed how much trust even one critic costs to earn.

**Draft-tier first, pro-tier on approval.** Nothing burns expensive compute before a human approves the plan. Generating at final quality from the start was the obvious default and I skipped it: the money saved by cheap drafts funds the volume the fleet's whole value depends on.

**Named agents with per-agent eval suites, not one monolithic prompt.** Each agent (Maya, Cy, Sam, Bea, Flo, Em, Mo) carries its own eval from day one, because "the fleet works" is unfalsifiable but "Em's false-pass rate is 0.10 on the mascot corpus" is a number you can argue with.

## What would break?

These are live, knowingly accepted risks, not fixed defects.

**1. The critic has a measured gap, inspected and deliberately not closed.** Em's mascot baseline (2026-06-30, n=46, reference-blind, N=5 majority vote) reads precision 0.93 / recall 0.90 / false-pass 0.10, measurably weaker than the sean-character baseline (0.97 / 1.00 / 0.00). All three false-passes are one class: a cleaned-up frame with no visible construction lines. I looked at all three fixtures and ruled them shippable. The "defect" Em misses is one I ship anyway, so I designed the calibration campaign and shelved it the same day as tuning waste; the design doc stays in the repo as the record of that reasoning. The accepted risk: the gap is real and stays open on purpose. If the aesthetic ever changes so construction lines matter, that shelved doc is where the thinking resumes.

**2. Critic calibration does not scale with the cast.** Em's trust was earned per-character: a 52-case corpus for one character, a 46-fixture corpus for the second, each with its own ratified baseline. I ruled out per-character calibration as unscalable, which means every new character joins the pipeline with a weaker critic until someone pays for a new baseline, and the roster's growth rate is bounded by eval-building, not generation capacity. I accept that, because the alternative is trusting an uncalibrated critic, and an uncalibrated critic is how I ended up grading against a void baseline (the contamination story in the next section).

**3. Motion-proper is structurally unscoreable by the current critic.** Em reads still contact sheets; timing, arcs, and easing live between frames. The motion phase's expected-red eval (recall 0.67) is not a regression. It's the honest measurement of a critic reviewing the wrong artifact class for that phase. The human gate at QA is the actual motion check, and stays so until a video-native critic earns its own baseline.

**4. The whole quality story leans on one person's taste being available.** Four human gates is the design, and it means the pipeline's throughput ceiling is me. That's correct for a director-driven studio and fatal for a service. Anima chooses the studio.

## What did I learn?

**The baseline you trust can be void.** Nineteen of twenty-three critic fixtures turned out to be byte-identical copies of the reference plates. The critic was matching, not grading, and every green light it had given was meaningless. A contamination test now forbids that by construction. Error analysis of the eval *itself* was the highest-leverage debugging I did on this project.

**Depth in the wrong order is still a cost.** The critic-calibration saga, six gated rounds to precision 0.97 / recall 1.00, was the right work run at the wrong time: ahead of the orchestrator, ahead of the animatic keystone. Real rigor, wrong sequence. The roadmap now exists to stop that.

**Knowing when to stop tuning is a product decision, not an eval decision.** The numbers said Em had a gap; a $0 label check said the gap was phantom. "If she's flagging that a single hair might be out of place, it's a waste of time and money" is the actual spec, and no metric would have written it. The critic's job was never to be right. It was to make my review time land where it matters.
