# Em's reference-grounding re-baseline — the change we built, measured, and blocked

*2026-06-02. The session that finally ran the twice-deferred Em re-baseline — by pivoting her Gemini transport off the quota-walled Antigravity CLI onto the Gemini API — and then used the measurement to **block** the very change it was meant to validate. Unlike the Cy Bible session, the code didn't fight us: five clean TDD commits, 275 green, no runner drama. The failures here were of a different and more interesting kind — a false premise that had been load-bearing for the whole eval program, and a hypothesis that the eval killed. This is the field report.*

---

## What the session was supposed to be

The reference-images workstream had shipped its code (PR #13, merged) — Em now attaches a Bible reference bundle (anchor + deduped turnarounds) and surfaces the character's `IR.*`/`AC.*` rules. What it *hadn't* done was measure whether that helped. The costed live re-baseline had been deferred **twice**: once to a clean-terminal run, then again when the run was attempted and agy's personal-tier Gemini quota came back `RESOURCE_EXHAUSTED (429)`. The [field report](2026-06-02-em-reference-images-field-report.md) closed with the deferral and a recipe for "next time."

This session was "next time," with one structural change: **stop waiting on agy's quota.** The plan was a transport-only swap — route Em's Gemini call through the Gemini API (`google-genai` + `GEMINI_API_KEY`, a separate vendor billing line) instead of the `agy` CLI — **holding the model constant** so the references-isolation read stayed valid against the reference-blind baseline (`performs precision 0.62, recall 1.00, false_pass 0.00`). Build the transport TDD, verify the snapshot matches, smoke it, run the 24-case re-baseline, score it false-pass-first, then re-run the three-way bake-off. The expectation, unspoken but real, was a precision *lift*: giving the critic her character's Bible is the kind of thing that's *obviously* going to help.

What actually happened: the build went clean, the validity gate found the premise was false, and the measurement found the change made Em **worse**.

---

## The build went clean — which is itself worth recording

Four TDD commits, each red-first, each leaving the contract suite green credential-free:

- **`59b095c`** — `pipeline/agents/gemini_api_runner.py`: `run_gemini_api_with_image`, a drop-in for the agy wrapper. Same `(*, prompt, image_paths, timeout_s)` signature, same `.text`-bearing response, the same `RateCapExhausted` honesty contract (empty/quota → raise, never silent borderline), the same stub-fallback-for-CI ladder. The blocking `google-genai` call runs in `asyncio.to_thread` under a timeout; prompt-first-then-images ordering matches the Opus SDK path.
- **`27f3358`** — `vision_critic._vision_transport(t2_cfg)` reads `critics.t2.transport: agy | gemini_api`, defaulting to `agy`. References, criteria, and the Opus-SDK escalation are untouched — the selector only chooses who delivers the images+prompt.
- **`0cb37eb`** — `--stub` forces the credential-free path for both transports; `score.py`'s `model_label` reads the live transport; manifest defaults `transport: gemini_api`.
- **`d7d136a`** — the pin correction (below).

Eleven new tests, suite **275 green**. The whole agonized harness saga from the prior field report — the exit-144 teardown signal, the orchestrator-vs-worker detach trilemma, the three failed live attempts — simply **evaporated**: the Gemini-API path has no Go/Node child to crash at interpreter shutdown, so the full 24-case run executed as a plain foreground background-task with zero teardown drama. *The cleanest fix for a process-lifecycle problem was to delete the process.*

This is the inverse of the Cy Bible session, where five live attempts surfaced five runner bugs that stub-fallback CI had hidden. Here, nothing hid. The failures this session were not in the code.

---

## Failure #1 — the premise was false: Em never ran on Gemini 3.1 Pro

The plan's validity gate asked one question before trusting any comparison: *does the API request the same model agy used?* The brief was explicit — if the API only exposed a differently-named snapshot, **stop**, because that's two variables moving, not one.

The answer was worse than a renamed snapshot. **agy was never running Gemini 3.1 Pro at all.**

`cli_runners.run_antigravity_with_image` invokes `agy -p <prompt>` with **no `-m` flag** ([cli_runners.py:183](../../pipeline/agents/cli_runners.py)). agy's own per-invocation logs confirm the consequence: every print-mode call records `model=""`, and the Antigravity backend picks the model. Across **272 / 272** Em-sized agy calls (prompts of 50K–107K chars — the real vision prompts, not probes), spanning **both the 2026-06-01 0.62 baseline run *and* the 2026-06-02 quota-blocked attempts**, the propagated backend model was logged as **`"Gemini 3.5 Flash (Medium)"`**. Never Pro. No `settings.json` pin. 1657 Flash propagations in the logs; zero for any Pro model.

So the manifest's `default_model: "gemini-3.1-pro-via-anti-gravity"`, the findings doc, the CLAUDE.md Em row — all of it was **aspirational**. The 0.62 reference-blind baseline ran on **gemini-3.5-flash**. The 2026-05-31 three-way bake-off's "Gemini" column was Flash too. An entire eval program had been quietly running on a model nobody had pinned and nobody had verified, because agy's "select your model" UX never propagated to its headless `-p` mode and the wrapper never asserted one.

**Resolution:** pin `GEMINI_VISION_MODEL = "gemini-3.5-flash"` — the model that actually produced the baseline — to hold the model genuinely constant (one variable: transport agy→API). Sean confirmed the pin. The cosmetic `critics.t2.default_model` label was annotated in place (no code reads it) rather than rewritten, to preserve the audit trail. The Gemini API exposes `models/gemini-3.5-flash` exactly, so the pin is real, not a guess.

This was caught only because the transport swap *forced* the question. Had we swapped to `gemini-3.1-pro-preview` as the plan's first draft assumed, we'd have moved two variables — transport **and** a Flash→Pro upgrade — and reported a contaminated precision delta as if it were the references effect. The validity gate earned its place in the plan.

---

## Failure #2 — the hypothesis was wrong: references made Em *less safe*

With the model pinned and the smoke clean (references attached exactly — `anchor + head-front + head-profile-left + body-3quarter` — real verdicts, no quota wall), the full re-baseline ran: 23 performs cases + 1 motion smoke, 0 errors, ~76s/case mean.

The §9 disciplines are ordered false-pass-first for a reason, and the first read settled it:

| Metric (performs, n=23) | reference-blind baseline | references + gemini-3.5-flash@api | read |
|---|---|---|---|
| **false_pass_rate** | **0.00** | **0.15** | ❌ gate failed |
| **recall** | 1.00 | 0.85 (±0.10) | ❌ dropped |
| precision | 0.62 | 0.73 | lift, **disqualified** |
| cites-correct | — | 0.80 | n/a |

Two false passes on the performs segment — both real defects Em let through: **`stylus-hand-f13-cc01`** (the known costly CC01 wrong-hand defect, the exact case Opus passed in the 2026-05-31 bake-off) and **`proportion-eyes-body-profile-right`**.

The §9 rule, written into the runbook and the field report long before this run, is unambiguous: *a precision lift that costs **any** false pass on performs is a worse Em — it blocks the change and promotes follow-on #3 (DINOv2 backstop) from deferred to next.* The precision *did* rise 0.62→0.73, but it was bought with false passes, and at n=23 with recall ±0.10 it's within ~1 stderr of noise anyway. **Blocked.**

The honest framing: giving Em the Bible made her **more confident and less safe**. Reference-blind Em caught everything (recall 1.00) by over-flagging (precision 0.62); references-Em became decisive and started passing real defects. The intuitively-good change — the *locked #1 fix* — regressed the one metric that matters most. This is not a process failure. It is the eval doing exactly its job, and the false-pass-first discipline catching exactly what it was built to catch.

---

## The diagnosis — why the false passes happened

Sean's call at the gate was "investigate the two false passes before writing conclusions." The run hadn't persisted Em's reasoning (the `CaseScore` carries only verdict/confidence/cites), so we re-ran the two cases to capture it, looked at the fixtures directly, and ran a prompt-ablation. Three distinct findings:

**1. Verdict variance (Opus stochasticity).** `stylus-hand-f13-cc01` is `identity_critical`, so Opus produces the verdict — and Opus is non-deterministic on a genuinely hard spatial call (which arm is "right" from a three-quarter turn). It scored **`pass` in the baseline run** but **`fail` (correct) on a plain re-run**, citing `IR.sean.prop.stylus-right-hand-always`, with reasoning that nailed it: *"Stylus is in Sean's left hand… a clean hand-flip on the load-bearing prop rule."* Same input, same code path, opposite verdict. So ~1/23 of the 0.15 is sampling noise: **a single 24-case run is a noisy estimate of false_pass_rate.**

**2. Confabulation / forgiveness (the real signal).** `proportion-eyes-body-profile-right` passed in **both** runs. The fixture is a flat-digital cartoon — off-register from the A-2 anchor (no cream-paper grain, no construction lines) — with a subtle proportion/jaw/eye drift in profile, where the face is tiny. Yet Opus's reasoning claimed *"register is honored — warm-graphite contour… visible construction marks… **cream paper substrate with visible grain**."* Those features **are not in the fixture.** Given the reference bundle, Opus recited *what the character should look like* and projected it onto the subject, confabulating a match. An MLLM handed a reference "story" narrates it.

**3. The prompt-ablation — the matching-wording is a lever, not a fix.** We stripped the sentence *"a feature that MATCHES the references is correct… do NOT flag a difference the references confirm is correct"* (the deliberate sycophancy surface the spec had flagged) and re-ran the two cases. `proportion-eyes` flipped pass→fail — **but for the wrong rule**: ablated, Em flagged the *absent stylus* she'd previously forgiven, while **still** reading the labeled proportion/eye defect as holding and **still** confabulating the cream-paper grain. So the wording demonstrably reduces Em's forgiveness, but removing it does not restore *perception* of the fine-grained defect, and does not stop the confabulation. The prompt alone cannot close the gap.

Together these say something precise: the references regression is part Opus noise, part a perceptual/confabulation limit that a prompt tweak won't fix. That is the textbook case for a **deterministic** identity signal sitting *beside* the MLLM — DINOv2 can't confabulate cream-paper grain or hallucinate a 1:7 proportion match.

---

## What we learned

The takeaways that should outlive this session.

**Never pin a model by label — pin it by ID, and verify it fired.** This is the deepest lesson, and it indicts more than this workstream. agy's headless `-p` mode silently ran the backend-default model because the wrapper never passed `-m`; the manifest *labeled* the model `gemini-3.1-pro` and everyone believed the label. A whole eval program — the 0.62 baseline, the 2026-05-31 bake-off, every Em verdict to date — ran on an unverified, unpinned model that turned out to be a different capability tier than the docs claimed. The fix isn't just "pin Flash"; it's a discipline: **any costed model call must assert its model explicitly and log the model it actually used**, and a baseline's provenance is not trustworthy until you've read back the model from the runner's own logs. The transport swap only caught this because it forced the question. Nothing else would have.

**The intuitively-good change is exactly the one to eval-gate hardest.** "Give the critic her character's Bible" is so obviously correct that it was the *locked #1 fix* — shipped to code before measurement, merged in PR #13. It regressed the safety metric. If a change feels too obvious to need an eval, that feeling is the signal to run the eval. PHILOSOPHY's "empirical, not vibes" is not a slogan for the uncertain cases; it's for the ones you're sure about.

**An MLLM given references recites them.** The confabulation finding generalizes beyond Em. When you hand a vision model a set of "this is the ground truth" reference images and ask "does the subject match," you bias it toward narrating the references onto the subject. The reference bundle is not a neutral measurement aid; it's a prior the model will confabulate toward. Fine-grained identity/proportion verification wants a **deterministic** signal (embedding distance, pixel measurement) that has no story to tell.

**Prompt wording is a lever, not a fix.** The ablation cleanly separated the two: the "matches references = correct" sentence does induce forgiveness (removing it made Em stricter), but the underlying perceptual miss and the confabulation persisted without it. Reaching for a prompt edit when the failure is perceptual is treating a symptom. Worth keeping the lever in mind (soften the wording if references are kept), but it is not the remedy.

**Single-run eval verdicts are noisy on hard cases — baselines need replication.** The stylus case flipping `pass`↔`fail` across two identical runs is direct evidence that a single 24-case run gives a false_pass_rate with real sampling error. The 0.15 is one noisy draw; the "true" systematic false-pass set may be one case (proportion-eyes) plus variance. Future costed baselines should run N times (or majority-vote per case) and report a band, not a point. We recorded the variance honestly rather than treating 0.15 as exact.

**Transport choice has second-order effects the comparison crossed.** The 0.62 baseline ran via agy (which applies a "Medium" thinking-effort); the new run via the API at default config. Same model name, possibly different effort. The references-isolation read is therefore strictly references **+** transport, not references alone. The clean attribution — a reference-blind run on the *same* API transport — was offered and deferred; it remains the way to fully separate the two. The false-pass block stands regardless, because the gate is absolute (0.00) and the candidate Em lets the costly defect through on its own merits.

**The failures lived in the verification layer, and that's where they were caught.** The Cy Bible session's lesson was "stub fallbacks hide real-model bugs; live runs catch them." This session's mirror: the build was clean, but the *premise* was false and the *hypothesis* failed — and both were caught not by debugging code but by the **validity gate** and the **false-pass discipline**. The meta-lesson holds across both: invest in the verification layer (snapshot checks, ordered scoring disciplines, replication), because that is where truth about an LLM system actually lives.

**Deleting the process beat managing it.** The prior field report spent its length on an exit-144 teardown signal and an orchestrator-vs-worker detach trilemma — all artifacts of agy's Go/Node child crashing at shutdown. Moving to the API removed the child entirely and the whole class of failure with it. When a subprocess lifecycle is fighting you, the cheapest fix may be to not have the subprocess.

---

## What landed on disk

| Commit | What |
|--------|------|
| `59b095c` | `gemini_api_runner.py` — Gemini-API vision transport (drop-in for the agy wrapper; RateCapExhausted contract; stub-fallback) + 7 tests |
| `27f3358` | `vision_critic._vision_transport` selector (`critics.t2.transport: agy \| gemini_api`) + 3 tests |
| `0cb37eb` | `--stub` patches both transports; manifest defaults `gemini_api`; `model_label` reflects transport + 1 test |
| `d7d136a` | pin correction → `gemini-3.5-flash` (the model agy actually ran); label fixes |
| `9151cae` | docs: field-report postscript + CHANGELOG + CLAUDE.md Em row + manifest annotation; the measured matrix (`last-run.md` + trace) |

Merged to `main` as **PR #15** (`b30039b`). Contract suite **275 passed** (264 baseline + 11 new). 

Live spend: cents of `gemini-3.5-flash` across the 24-case run + a 2-case smoke + 2 investigation re-runs + a 2-case ablation; Opus escalation subscription-absorbed. Wall time ~40–50 min for the full run (Opus escalation fires on `identity_critical` cases at ~100–150s each). `ANTHROPIC_API_KEY` absent throughout — Opus billed the subscription, Gemini billed the bounded API key, exactly as the fleet-ops protocol requires. Orchestrator detach was never needed; a plain foreground background-task carried the run. Single owner, isolated worktree, clean orphan sweep at end.

The receipts: a working Gemini-API transport, a corrected model provenance for the whole T2 program, and an honest measured verdict — references-grounding, as built, is a regression — with a legible diagnosis.

---

## How to proceed

1. **Decide the references-attach disposition** *(open, Sean's call — flagged in the PR, not acted on).* It's the shipped default (PR #13) and is now eval-blocked. Options: revert it; gate it behind a flag (off by default) until a deterministic backstop lands; or leave it pending DINOv2 and accept the known regression in the interim. This is the one decision the session deliberately did not make.

2. **Promote DINOv2 (follow-on #3) to next.** The confabulation finding is the strongest possible motivation: a deterministic identity/proportion signal can't recite the references. Em-with-references is the wrong layer for fine-grained identity; DINOv2 beside her is the right one. The reference-images workstream's own out-of-scope list named this; the measurement just promoted it.

3. **Close the model-provenance gap program-wide.** Em wasn't the only agent calling agy without `-m`. **Cy's Pass-3 verification** ("Gemini 3.1 Pro via agy") calls the *same* `run_antigravity_with_image` wrapper ([character_designer.py:760](../../pipeline/agents/character_designer.py)) — confirmed this session — so Cy's two locked Bibles were verified by backend-default **Flash**, not the Pro the CLAUDE.md row claims. Audit every agy caller, pin models explicitly at the call site, and make runners log the model they actually used. The label-vs-reality gap that bit Em is real wherever agy chooses the model for us, and it's already touched shipped artifacts.

4. **Replicate baselines.** Make the costed scorer support N runs (or per-case majority vote) and report a false_pass band. The stylus flip proved a single draw is noisy; the next baseline number should be a stable estimate, not one sample.

5. **If references survive in any form, fix the two implicated levers.** Soften the "matches references = correct" wording (the ablation showed it induces forgiveness), and ship **view-aware selection** (approach A) so a profile shot gets profile references rather than a front anchor — the `proportion-eyes` profile case is exactly where the front-heavy bundle underserved the judge.

6. **Re-run the three-way bake-off with pinned, correctly-labeled models.** It was skipped this session (gated on a clean re-baseline that didn't happen). When it runs: the "Gemini" column must pin its model explicitly (it was Flash, not Pro), and the comparison should attach references on all three only after the references question itself is resolved.

The portfolio artifact here is not "0.62 → a better number." It's the harder, truer one: the obviously-good change regressed the safety metric, a validity gate caught that the baseline had been mismeasured for the whole program, and the false-pass discipline blocked the change before it could ship as an improvement. The moment Em *stopped grading blind* turned out to be the moment she started grading *wrong* — and the eval is what told us so. That is the system working.
