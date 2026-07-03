# Front Door (①) — Slice 4: STRESS-TEST (the pre-mortem + red-team stage) — Converged Build Plan (Opus + Codex)

> **For agentic workers:** REQUIRED SUB-SKILL — use `superpowers:test-driven-development` per code task (red → verify-red → green → verify-green → refactor) and `superpowers:verification-before-completion` before any "done". Steps use checkbox (`- [ ]`) syntax.

**Date:** 2026-07-03
**Status:** Planning — the executable spec for Slice 4 of ①, the **final stage** of the locked chain. **Plan only; no implementation code this session.**
**Builds on:** [2026-07-02-frontdoor-slice3-artviz-CONVERGED.md](2026-07-02-frontdoor-slice3-artviz-CONVERGED.md) (the METHOD model + the reach-the-real-writer lesson; its §13 is a *starting sketch*, not settled requirements), [2026-07-02-frontdoor-slice2-expand-CONVERGED.md](2026-07-02-frontdoor-slice2-expand-CONVERGED.md) (the inline-discipline precedent), and [2026-07-02-frontdoor-build-plan-CONVERGED.md](2026-07-02-frontdoor-build-plan-CONVERGED.md) (§5.5 / §8 Slice-4 sketch — its predicted `stress_verdict` field is overridden here, §2.2).
**Primary evidence:** the two live briefs' **"Open threads"** movements — the by-hand *proto*-stress-tests: [GRANDMASTER](../../briefs/2026-07-02-grandmaster/concept.md) (a strong concept whose register-gap Tiger *blocks Cy's Bible pass* — the shape of proceed-with-a-named-residual) and [ai-guru-pilot](../../briefs/2026-07-02-ai-guru-pilot/concept.md). **There is no live STRESS-TEST run yet** — that absence, plus the self-critique bias unique to this stage, drives the central call (§2.1).
**Co-planned with:** Codex (independent plan §12) + adversarial red-team (§13). **The red-team returned "not right-sized" and reshaped the central call** — see §2.1 and §13.

---

## 0. The remaining front-door roadmap — ①'s Definition of Done (open here)

Slice 4 is the last *stage*. This section says what "① DONE" means, what is **in** that Definition of Done, and what is a **separate later workstream** — so the slice doesn't quietly grow the front door into the whole product.

### 0.1 The DoD, stated

> **① reaches Done when the five-stage locked chain (EXPAND → INTERROGATE → ART-VIZ → STRESS-TEST → SYNTHESIZE) is built, each stage reaches the real writer (SYNTHESIZE emits it), and one live front-door run on a fresh spark exercises all five stages — emitting a brief bundle that `validate_brief_dir` passes and `python -m pipeline.run --brief <dir> --slug S --stub` accepts at the plan gate — with each stage's live rubric passing Sean's eye, AND any production-binding stress residual reaching `00_studio_brief.md` (Maya's actual input), not just `concept.md`.**

The last clause is the red-team's sharpening (§13, finding 2/3): `pipeline.run --brief` and Maya read **only `00_studio_brief.md`** — a Tiger that lives only in `concept.md` is invisible to planning. This mirrors the DoD discipline the other workstreams used (the Animatic DoD closed on a *costed live run*, not on green tests alone). The front door's live rubrics already exist for four of the five stages (`pinata-worked-example` anti-pattern checklist; `good-expand-rubric`; `good-art-viz-rubric`); Slice 4 adds the fifth (`good-stress-test-rubric`). When Slice 4 lands and its Checkpoint-4 live run is green, **the chain is complete and ① is Done.**

### 0.2 What is IN the DoD (this workstream finishes here)

| # | Piece | Status | Where |
|---|---|---|---|
| **A** | **STRESS-TEST stage** — fresh-context (c) authoritative default + inline (a) reflex, reaching SYNTHESIZE + the template + the sidecar contract + **the Studio Brief** | **This plan (Slice 4)** | §2–§10 |
| **B** | **The DoD ratification run** — one live five-stage run on a fresh spark, all four live rubrics scored by Sean; a **production-binding stress residual proven to land in `00_studio_brief.md`** (verifiable by reading the emitted brief), and Sean confirms Maya's plan reflects it | **Checkpoint 4** (Sean's live pass; may be an immediate follow-on) | §10 |

Nothing else is required to call the *front door* done. B is the closing move: the front door's analogue of the Animatic costed run — the live proof the chain works end-to-end, including that stress output is production-binding, not just museum-worthy.

### 0.3 What is OUT — three separate later workstreams (each gated on a consumer that doesn't exist yet)

The §13 sketch and the parent plan named three follow-ons. **None gates the five-stage chain**; each is deferred because its precondition or consumer is absent. Naming and sequencing them here keeps them out of Slice 4.

1. **(i) The SPEND-OK / Higgsfield render gate.** Its gating input is a *shipped* `proceed` verdict **and** a *greenlit piece that wants an in-session render*. Neither exists — both live briefs are $0 dry-run spikes; Sean renders route prompts on his own Flow at $0. Already specified as deferred design (`good-art-viz-rubric.md` appendix). A **convenience layer** on top of the $0-Flow default, not the spark→brief core. → **Built later, co-built with the verdict consumer.** **OUT of ①'s DoD.**

2. **(ii) Front-door museum capture.** Whether a front-door session writes exhibits per the [museum-exhibit-schema](../architecture/museum-exhibit-schema.md) belongs to the **broader Museum workstream** (ROADMAP's "LATER — the long game": "wire museum capture into the orchestrator"). The concept doc is *already* museum-worthy prose (the raw material exists by design). Actual exhibit wiring is workstream 3. → **OUT of ①'s DoD; folded into the Museum workstream.** (The front door is a natural early *producer* for it — a one-line note there, not a Slice-4 task.)

3. **(iii) The seeds → Cy → registration → GENERATE bridge.** The front door's **own side is done** (well-formed seeds + the gap report — Slice 1). The *other* side — Cy authors the Bible → the namespace registers → GENERATE-ready — spans the **parallel register-extension track** ([animation-vocabulary-expansion-scope](2026-07-03-animation-vocabulary-expansion-scope.md), which unblocks GRANDMASTER) and **Cy-authoring-as-a-run** (ROADMAP's parked Q6). Conflating "emit a Maya-ready brief" with "build the finished film" is scope creep. → **OUT of ①'s DoD; the first real closure rides the register track.**

### 0.4 Sequencing — what's next, and what closes ①

- **The register-extension pilot runs *before* Slice 4** (Sean's call, 2026-07-03 — a *production blocker* for GRANDMASTER, a *within-workstream* reorder, not a new workstream). This plan **references it as the parallel priority and does not plan it.** It is also the first real closure of bridge (iii).
- **Slice 4 (this plan) is the next front-door build**, and the **last stage**. There is **no Slice 5 within ①** — the chain is complete at Slice 4 + the ratification run (B).
- **The one contingency:** the default is fresh-context (c). If ≥2 live runs show the fresh-context pass **redundant** with the in-room reflex or **missing load-bearing in-room context**, the standard demotion trigger (§2.1) flips (a) inline back to the authority — a **prose edit**, byte-identical seam, not a new slice.
- **What closes ①:** Slice 4 green + the Checkpoint-4 live five-stage run passing Sean's eye. After that, the ROADMAP's sequence resumes — the **seeds→Cy/register bridge (iii)** is the next real blocker to turning these briefs into GENERATE-ready work (Codex's Q6 call; it overlaps the parallel register track); **② the daemon foundation** is the parallel-safe workstream; **Museum wiring** (which absorbs (ii)) is the long game; the SPEND-OK gate (i) promotes when its consumer appears.

---

## 1. The one-sentence goal

Formalize the front door's **pressure-test stage** ("STRESS-TEST" in Sean's locked chain) as a **fresh-context red-team of the concept the room just built** — a sub-agent that reads only the emitted-or-draft `concept.md` + `00_studio_brief.md` (blind to the room's love story) and runs a pre-mortem (Tiger / Paper-Tiger / Elephant, default-to-Tiger) + red-team (steelman → "Fails if ___" → cheapest test, don't-manufacture-doubt), **preceded by a cheap inline in-room reflex** — that proposes findings + a recommended `proceed | revise` verdict (the four proposal kinds only; Sean decides), and folds them as prose into `concept.md` **and — when production-binding — into `00_studio_brief.md`** via the existing SYNTHESIZE writer — **without a `stress_verdict` handoff field, without building the spend gate, without any spend, and (bar one stale-comment fix) without changing `pipeline/frontdoor` schema or behavior.**

## 2. The position: fresh-context (c) is the authoritative default; inline (a) is the reflex; the verdict, the field, and the spend gate all defer

Five claims (Q1–Q5), ordered by how hard the evidence pushed. The through-line: STRESS-TEST is the one stage whose job is to **verify, not author** — and verification is exactly where fresh-context beats same-context, so this stage rightly *differs* from EXPAND/ART-VIZ rather than copying their inline-authoring default.

### 2.1 [Q1] Fresh-context (c) is the authoritative STRESS-TEST; inline (a) is a cheap in-room reflex. (b) is dead. No A/B protocol.

This is the load-bearing call. My first draft hedged — "ship (a) inline, specify (c), let a live comparison decide" — and the red-team was right that the hedge (a) *dodged a position* and (b) built bespoke A/B machinery no prior slice built. The corrected call **takes a position and drops the machinery:**

**Why (b) — a same-session `frontdoor-stress-test` skill — is dead.** A same-session model call framed as an "adversarial role" **shares the authoring context that fell in love with the concept.** It reframes the critique but doesn't *attack the bias* — the same context is still grading its own work. It looks like a seam without being one, and pays a context-switch cost for no independence. (Verified reasoning from the Slice-3 red-team F8; it holds.)

**Why fresh-context (c) is the authority, not inline (a).** EXPAND and ART-VIZ are inline because they are **authoring** moves (divergence, style routes) that belong in-room. STRESS-TEST is a **verification** move — and the stage's *unique, documented* risk is self-critique bias: the room red-teaming a concept it just built. Anthropic's own Fable-5 guidance is explicit that *fresh-context verifier subagents tend to outperform self-critique*, and the Slice-3 sketch's own reasoning called fresh-context "the only option that actually attacks the bias." Crucially, **(c) is not heavier to build than (a):** it is an orchestrator dispatch instruction (a `Task` reading only `concept.md` + `00_studio_brief.md`), **no `pipeline/frontdoor` code, not unit-tested** (fleet-ops: no live sub-agent in CI). So committing to (c) as the authority is not over-build — it is the *same weight* as inline, and it **earns** its place against the one piece of evidence that matters here (the documented bias). This is the "make any separate thing earn its place against evidence" test, passed.

**So Slice 4 commits:**
- **Fresh-context (c) is the authoritative STRESS-TEST.** After ART-VIZ, the orchestrator dispatches a fresh-context reviewer that reads **only the draft `concept.md` + `00_studio_brief.md` — not the sidecar's locked-decisions love story, not the proposals log** — and returns the four proposal kinds. It is the T3-council / verifier-subagent pattern.
- **Inline (a) is a cheap in-room reflex, not the authority.** Before the dispatch, the orchestrator runs a quick in-room pre-mortem to surface the obvious Tigers while still in context (cheap, catches the low-hanging). Its findings feed the fresh-context pass; they do **not** hold final authority. This keeps a warm-up without pretending same-context self-critique is unbiased.
- **No bespoke A/B comparison protocol, no separate authored weak-concept fixture file.** Those were the over-build. The default is decided (fresh-context); the *demotion trigger* is the **standard** discipline the other slices use: **if ≥2 live runs show the fresh-context pass redundant with the in-room reflex, or missing load-bearing in-room context that mattered, demote (c) to an escalation and make (a) the default.** A weak concept stays as an **inline ships-red anti-example in the rubric** (the calibration case), not a committed fixture file — exactly how good-EXPAND/good-ART-VIZ carry their anti-examples.

Whichever form runs, it returns **only** the four proposal kinds; **Sean decides; the orchestrator locks the verdict.** Control never leaves the room's ownership of the decision.

### 2.2 [Q2] `stress_verdict` stays **prose + a sidecar LOCKED DECISION**; **no `handoff.py` field**; **no spend gate built here**

The parent plan *predicted* Slice 4 adds a `stress_verdict: proceed|revise` field to `handoff.py`. **No-schema-theater — verified against `main` — overrides that prediction, exactly as Slice 3 overrode the predicted `style_route` field:**

- **Nothing reads `stress_verdict`.** Verified: the *only* occurrence of the string anywhere on `main` is a *comment* in `handoff.py`; no reader in `pipeline/`, `tests/`, `scripts/`. The daemon plan returns `run_state.json` + artifacts and Em's *vision-critic* verdict — **not** any front-door verdict field (the daemon's "verdict" is Em's, a different thing). The *only* named would-be consumer is the **SPEND-OK render gate**, which is not built and has a second missing precondition (a greenlit piece). And `Handoff.from_json` **rejects unknown fields** (`handoff.py:49-52`), so a field is a real schema commitment for a value nothing consumes.
- **The verdict has a schema-sanctioned home already:** a **LOCKED DECISION** the orchestrator writes to the sidecar (`[Ln] stress verdict: proceed (residuals: <named Tigers>)`) and **prose in `concept.md`** (the Stress-test movement, §2.4) — plus, when production-binding, the Studio Brief non-negotiables. A human reads it; no machine does.
- **The machine record is a provenance string, not a field.** `stage_provenance` gains a `stress-test` entry. **Honest contract (red-team finding 5):** `stage_provenance` is runtime-validated as a **non-empty list**; element *types* are **not** enforced — `Handoff(stage_provenance=[1])` round-trips today. So a `stress-test` string round-trips **by convention** (pinned by the characterization test), **not** by a code-enforced `list[str]`. The existing generic `test_rejects_unknown_field` already pins "no `stress_verdict` field"; no magic-word test is added.

**The spend gate is not built here** (both preconditions absent). **`pipeline/frontdoor/` stays schema- and behavior-identical — the third consecutive slice.** The sole touch is a **one-line comment fix** (finding 6, §9 Task 1c): the stale `handoff.py` docstring still says `style_route / stress_verdict land with Slices 3/4` — false now that both slices deliberately ship **no** such field. Retiring that comment is source-of-truth honesty (this repo's discipline), not a schema/behavior change; the "byte-identical" claim is refined to "schema + behavior identical; one stale comment retired."

### 2.3 [Q3] Always-on / non-blocking / default-to-Tiger — three different axes, no conflict

- **Always-on:** once built, STRESS-TEST runs on every concept — never routed around (a skipped stage would be *declared* skipped in `stage_provenance`, never silently faked). The fresh-context pass is the always-on authority; the inline reflex always precedes it.
- **Default-to-Tiger:** the *classification bias within* the stage — when unsure whether a risk is a Tiger (real, act) or Paper-Tiger (overblown, document), call it a Tiger. Keeps the stage from under-flagging. About honesty of flagging, not halting.
- **Non-blocking:** the stage **does not unilaterally halt** the pipeline. It surfaces its Tigers + a recommended `proceed | revise`, and **Sean decides.** The verdict *informs* the human. (This is also why `stress_verdict` needs no machine reader.)

Together: run every time, flag aggressively, decide humanly. **GRANDMASTER is the canonical output shape:** proceed **with** named residuals (the register-gap Tiger, Launch-Blocking *for Cy* not front-door-blocking) — not a clean pass, not a block.

### 2.4 [Q5] Reach the real writer — SIX surfaces, and the Studio Brief is the load-bearing one

This is the Slice-3 UNDER-BUILT lesson, and the red-team caught my draft still under-building it: I reached `concept.md` but not **`00_studio_brief.md` — the only file `pipeline.run` and Maya actually read** (`run.py:174`; Maya/Sam/Bea consume the Studio Brief as free text, never `concept.md`). A Launch-Blocking Tiger that lives only in `concept.md` is invisible to planning. So — verified against `main` — **six** writer-side surfaces must be taught:

- **`session-sidecar-contract.md`** — add a `### stress-test` PROPOSALS block (four kinds) + the verdict LOCKED-DECISION convention.
- **`concept-doc-template.md`** — add a **"Stress test (pre-mortem + red-team + verdict)"** movement; reframe "Open threads" as its downstream tail (Track / Fast-Follow residuals).
- **`frontdoor-synthesize/SKILL.md`** — fold the `### stress-test` block into the new movement; carry the verdict lock as prose; add `stress-test` to `stage_provenance` when present.
- **`studio-brief-contract.md` (the red-team's required addition).** **A production-binding stress residual — a Launch-Blocking Tiger, or a proceed-with-residual that changes buildability / budget / constraints (GRANDMASTER's register gap is the exemplar) — MUST fold into the Studio Brief** (under `### What this is NOT` or `## What are the non-negotiables?`), so Maya sees it. Non-binding (Track / Fast-Follow) findings stay in `concept.md`. The non-negotiables section is already free-text "one checkable directive per," so a stress-driven constraint fits the existing shape — the contract edit *names that this is where it lands*, no new schema.
- **`SKILL.md` (orchestrator)** — the new Step 2.75 (§9 Task 2.1).
- **`chain-map.md`** — flip the STRESS-TEST row off the stale skill/field sketch.

**Don't stop at the orchestrator, and don't stop at `concept.md`.** The load-bearing target is the Studio Brief — the artifact the pipeline actually consumes.

### 2.5 [Q4] The eval is Slice 1/2/3's honest split — a tiny structural characterization + a live good-STRESS-TEST rubric

Stress quality is judgment, **not** a CI assertion (every prose-grep is theater; a "concept.md contains a Tiger" lint is gameable by a name-drop). The split (§7):
- **Structural (CI, no keys):** essentially **one** new test — a `stress-test` provenance round-trip characterization (no module, no field) — leaning on the **existing** generic unknown-field guard. The thinness *is* the finding.
- **Semantic (live, blocking — Sean's eye):** the **good-STRESS-TEST rubric** — a live human-review checklist (never a CI/self-pass gate), with GRANDMASTER + ai-guru as worked positives (proceed-with-residuals) and a **deliberately-thin weak concept described inline** as the worked negative (must surface ≥1 launch-blocking Tiger + `revise`). Blocking rule and anti-gaming design in §7.2. **No A/B comparison protocol** (cut per §2.1).

## 3. Architecture — a fresh-context reviewer (+ an inline reflex) over the untouched Slice-1/2/3 seam

**No new skill. No new `pipeline/frontdoor` code (bar one comment). No spend.** Slice 4 is: (A) prose that specifies the inline reflex + the authoritative fresh-context STRESS-TEST in the orchestrator `SKILL.md`, flips the chain-map row, adds the rubric reference, and — the load-bearing half — **teaches SYNTHESIZE + the concept template + the sidecar contract + the Studio Brief contract to fold `### stress-test`**; and (B) a small amount of *test* work that pins the no-code contract, plus the one stale-comment fix. The Slice-1/2/3 seam already carries everything STRESS-TEST produces:

- Findings + the recommended verdict live in the sidecar **PROPOSALS LOG** `### stress-test` block. SYNTHESIZE folds them into `concept.md`'s Stress-test movement and, when production-binding, the Studio Brief.
- The verdict is a **LOCKED DECISION** (orchestrator-written, after Sean decides), prose — never a `handoff.py` field.
- `stage_provenance: [..., "stress-test", ...]` round-trips (a string value, by convention — §2.2).

**Verify-the-no-code-claim discipline:** the build session confirms against the built seam — `Handoff(stage_provenance=[..., "stress-test", ...])` round-trips; unknown *fields* still reject. State the actual runtime contract (non-empty list, types unenforced); do not overstate it.

## 4. The two STRESS-TEST forms (authority vs reflex)

| | **(c) Fresh-context reviewer — the authoritative default** | **(a) Inline in-room pre-mortem — the cheap reflex** |
|---|---|---|
| What | A sub-agent reading only `concept.md` + `00_studio_brief.md`, blind to the sidecar; full pre-mortem + red-team | A quick in-room pre-mortem that surfaces the obvious Tigers while still in context |
| Attacks the self-critique bias? | **Yes** — genuine independence (verifier-subagent pattern; Fable-5 guidance) | **No** — same context; it is a warm-up, not the authority |
| Authority | **Holds the recommended verdict** (Sean decides) | Feeds the fresh-context pass; no final authority |
| Cost | $0 build (prose dispatch); a runtime cost (one fresh context window) | $0, in-room, cheapest |
| `pipeline/frontdoor` code? | **None** | **None** |
| Unit-tested? | No (fleet-ops) | No (live discipline) |
| Demotion trigger | ≥2 live runs redundant-with-reflex or missing-in-room-context → demote to escalation, promote (a) | — |

The default is **decided**, not deferred to a bespoke protocol — the standard two-run promotion/demotion discipline governs any change, same as EXPAND/ART-VIZ.

## 5. Flow placement: nominally fourth, Step 2.75 between ART-VIZ and SYNTHESIZE

Sean **locked** the nominal order (`EXPAND → INTERROGATE → ART-VIZ → STRESS-TEST → SYNTHESIZE`). Slice 4 realizes it **without a reorder:**

- A new **Step 2.75 — STRESS-TEST** sits between ART-VIZ (Step 2.5) and SYNTHESIZE (Step 3) in the orchestrator `SKILL.md` and the chain diagram. (Numbered 2.75, not 3.5 — it *precedes* SYNTHESIZE, which is Step 3; Codex's correction.)
- **Skip condition:** none — always-on. A concept that needs no revision is still *run through* and returns `proceed` with an honest "no launch-blocking Tigers"; it is never skipped.
- Like every stage, STRESS-TEST **proposes** (findings = `observations`+`options`, verdict = `recommendation`, unresolved = `open_questions`); **Sean decides; the orchestrator locks.**

## 6. The propose-vs-decide boundary — prose + sidecar convention (not a lint)

Unchanged from Slices 1–3: STRESS-TEST **proposes** findings + a recommended verdict; it **never locks** the verdict. Only the orchestrator writes the LOCKED DECISION, append-only, after Sean decides. Enforced by prose discipline + the append-only sidecar convention + human review — **not** a unit test and **not** a "verdict-shape lint" (a parser asserting "concept.md has a Tiger + a proceed|revise token" gives false confidence — a manufactured-doubt pass with a name-dropped Tiger passes). The honest split holds: the **seam** is unit-tested; the **discipline** is a live rubric + Sean's eye.

## 7. Eval strategy — the honest split, grounded in the craft + the two live briefs

**The seam is unit-tested (CI-green, credential-free); stress *quality* is a live rubric eval (blocking human checkpoint).** No model transport, no sub-agent, no MCP, no spend in any test.

### 7.1 Structural (CI, no keys) — deliberately tiny
STRESS-TEST adds **no code and no schema** (bar the comment), so there is almost nothing new to assert — that thinness is the finding. **One** new test, plus a lean on the existing guard:
- **`stress-test` provenance round-trips** (Task 1, a *characterization*): `Handoff(stage_provenance=["micro-expand","interrogate","art-viz","stress-test","synthesize"], …)` round-trips — the machine proof no `stress.py` module and no field are needed. Passes on first run; that greenness *is* the finding.
- **Lean on the existing `test_rejects_unknown_field`** (Slice 3, on `main`): it already pins "no `stress_verdict` field." **No magic-word test.**
- **Cut:** any "concept.md carries a Stress-test movement / a Tiger" validator; any `stress_verdict`-specific field test; any stress-skill contract test.

### 7.2 Semantic (live, blocking — the real quality gate): the good-STRESS-TEST rubric
A **good pass exhibits all six** (live human-review checklist, never a CI/self-pass gate):

1. **A real kill-assumption found (steelman-then-attack).** The pass extracts the concept's load-bearing assumptions, steelmans the *strongest* version, attacks that — not a strawman, not a cosmetic nitpick. A *real* kill-assumption is one you can state as a falsifiable **"Fails if ___"** (criterion 2) — a worry you cannot falsify is manufactured doubt (criterion 4). *Worked positive:* GRANDMASTER's assumption "the six-register vocabulary can render the locked *Primal* look" — attacked, and it fails. *Anti-example:* "what if the title is weak" as the headline risk.
2. **Each risk is a "Fails if ___" with a cheapest test.** Concrete, falsifiable, with the cheapest way to find out this week. *Worked positive:* "Fails if Cy cannot author a *Primal* Bible in any of the six registers — cheapest test: a $0 stub Cy pass in `pencil-test-colored` and Sean's eye on whether it reads as Primal." *Anti-example:* "the animation might not land."
3. **Tiger / Paper-Tiger / Elephant triage, default-to-Tiger.** Classified; ambiguous → Tiger; Launch-Blocking named + separated from Fast-Follow / Track. *Worked positive:* GRANDMASTER — register gap = **Launch-Blocking for Cy** (not front-door); runtime flex = Track; music/sound = Fast-Follow.
4. **No manufactured doubt; the fragile intuition is protected — the anima-specific bar.** A sound concept is said sound plainly ("five real kill-assumptions beat twenty generic risks"); the **fragile high-value intuition that makes the piece special is NOT attacked as a risk** (mirrors good-EXPAND #5). **Loophole-closer (red-team finding 4):** every invocation of "protecting the intuition" must **name three things** — (a) the protected engine, (b) the *nearest legitimate adjacent risk* (the real weakness sitting next to the engine), and (c) why the flagged weakness is *not merely the engine wearing a scary label*. This blocks both games: manufactured false rigor (attacking the engine) **and** using "fragile intuition" as a bare veto shield to dodge a real structural attack. *Worked positive:* GRANDMASTER's genre-collision-with-no-mockery is the engine — protected, but the adjacent real risk (does the no-mockery rule survive the disarm beat?) is still named and attacked. *Anti-example:* waving off "is a samurai-piñata too weird" — turning on the engine; or refusing to attack a real structural hole by calling it "the fragile intuition."
5. **An honest recommended verdict with correctly-triaged, named residuals.** `proceed` with residuals on a strong concept (**GRANDMASTER proceeds WITH the register-gap Tiger — never a clean pass**); `revise` on a broken one. The residual is **correctly triaged** (criterion 3): GRANDMASTER's gap is *Launch-Blocking for Cy, not front-door-blocking* — mis-scoping it (a front-door halt, or a mere Track item) is a calibration failure. Verdict is a recommendation; Sean decides. *Anti-example:* a clean "proceed, looks great" on GRANDMASTER, or a "revise" naming no fixable residual.
6. **Names its own self-critique limit / reaches production.** The pass is honest that a same-context read is biased (which is *why* the authority is fresh-context); and a production-binding residual is flagged for the Studio Brief, not left in `concept.md` only. *Anti-example:* a Launch-Blocking Tiger that never reaches Maya's input.

**Blocking rule (anti-gaming): criteria 1, 4, and 5 block together.** These are the three ways the stage becomes theater; blocking on any one alone is gameable:
- **1 (a real kill-assumption)** — else *toothless* (a clean pass on everything). Carries criterion 2's falsifiability.
- **4 (no manufactured doubt / intuition protected, *substantiated*)** — else the stage games *rigor* (twenty generic risks / attacking the engine) **or** dodges via the veto shield. The substantiation requirement is what makes 4 safe to hard-block.
- **5 (honest, correctly-triaged verdict)** — the directional check: **GRANDMASTER must not clean-pass; the weak anti-example must not proceed.** Carries criterion 3's triage.
Criteria 2, 3, 6 are findings to fold — but 1 and 5 carry 2's and 3's substance, so the block **absorbs** Codex's independently-proposed "falsifiability + triage + calibration" block (§12) while keeping criterion 4 a hard block (the anima-specific core), now loophole-closed.

**Is any part gameable?** Honestly, weakly — a persuasive model can manufacture false rigor or under-flag. That residual is precisely why the **authority is the fresh-context pass** (the independent check) and why criterion 4 now demands substantiation. The rubric names its limits rather than pretending a self-critique is unbiased.

### 7.3 Fixtures — two live briefs as worked positives + one thin concept as an inline worked negative
- **Adopt GRANDMASTER + ai-guru** as the rubric's worked positives (proceed-with-residuals), same as good-ART-VIZ adopted their route sets — **reference material, not machine-asserted fixtures** (no CI oracle for stress quality). GRANDMASTER is the anchor: its register-gap Tiger *blocks Cy*, so a good pass proceeds-with-that-residual, never clean-passes.
- **Describe one deliberately-thin weak concept inline in the rubric** as the ships-red worked negative (generic grief; the-protagonist-is-the-joke; no genre collision; no mechanic; no register; no single objective) — a good pass returns **`revise` with ≥1 launch-blocking Tiger**. It is an **inline anti-example** (the good-EXPAND/good-ART-VIZ pattern), **not** a separate authored fixture file. The live protocol lets Sean run a fresh thin spark or a deliberately-thinned real concept as the cold-run negative.

### 7.4 Deferred design — the SPEND-OK gate + Higgsfield render (still NOT built)
Unchanged from `good-art-viz-rubric.md`'s appendix — recorded here now that STRESS-TEST *produces* the verdict:
- **Trigger:** ART-VIZ routes proposed AND the STRESS-TEST verdict is `proceed` AND Sean types `SPEND OK: Higgsfield <model> <count> <max-credits>`.
- **Behavior:** cost estimate first; refuse `generate_image` without the phrase; render the chosen route; write into the seed's `anchor_ref` / `style_ref_ids`.
- **CI:** never exercised. Built later **co-built with the verdict consumer**, only when a greenlit piece exists — and *that* is the slice where `stress_verdict` may finally earn a `handoff.py` field (field + reader together).

## 8. File layout (Slice 4 — prose + rubric + one tiny test + one comment fix; no skill, no schema, no spend)

```
.claude/skills/brainstorm-front-door/
  SKILL.md                              # EDIT — insert Step 2.75 STRESS-TEST (inline reflex + authoritative
                                        #        fresh-context reviewer); update the chain diagram + the
                                        #        "one future stage" note
  references/
    chain-map.md                        # EDIT — STRESS-TEST row: stale skill/field sketch → fresh-context
                                        #        default + inline reflex / status: live (Slice 4); no stress_verdict
                                        #        field; always-on/non-blocking/default-to-Tiger; demotion trigger;
                                        #        deferred spend gate
    good-stress-test-rubric.md          # NEW  — the six-criterion live-review rubric (criterion 4 substantiated)
                                        #        + inline weak-concept anti-example + the deferred SPEND-OK appendix
    concept-doc-template.md             # EDIT — add the "Stress test (pre-mortem + red-team + verdict)" movement;
                                        #        reframe "Open threads" as its downstream tail
    session-sidecar-contract.md         # EDIT — add the ### stress-test PROPOSALS block + the verdict LOCKED-DECISION
    studio-brief-contract.md            # EDIT (red-team finding 2, REQUIRED) — a production-binding stress residual
                                        #        (Launch-Blocking Tiger / buildability-or-budget-changing) lands in
                                        #        "What this is NOT" / non-negotiables; non-binding stays in concept.md
.claude/skills/frontdoor-synthesize/
  SKILL.md                              # EDIT — fold ### stress-test into concept.md's Stress-test movement AND
                                        #        the Studio Brief when production-binding; verdict lock as prose;
                                        #        add stress-test to stage_provenance when present

pipeline/frontdoor/
  handoff.py                            # EDIT (finding 6, COMMENT-ONLY) — retire the stale docstring line
                                        #        "style_route / stress_verdict land with Slices 3/4"; NO schema/
                                        #        behavior change (the only pipeline/frontdoor touch)

tests/
  test_frontdoor_handoff.py             # EDIT — add ONE stress-test provenance characterization (Task 1).
                                        #        The generic unknown-field test already on main pins "no field".
```

**No `frontdoor-stress-test/` skill. No `stress_verdict` field, no `stress.py`, no spend/MCP code, no verdict-shape lint, no A/B protocol, no separate weak-concept fixture file, no `criteria.py`/neutrality-test change.** `pipeline/frontdoor/` is schema- and behavior-identical (the sole diff is one retired comment). `git status` at Checkpoint 4 shows only the paths above.

## 9. Per-slice TDD task list

Discipline every code task: `superpowers:test-driven-development`; tests run **per-directory from repo root** (`python -m pytest tests/`); commit at each task end; `superpowers:verification-before-completion` before "done"; **both md5 guards byte-unchanged** — Slice 4 touches neither:
`evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4`;
`pipeline/agents/prompts/sean-screenwriting-voice.md` = `945af824fa53b948a18ac6bf206d67ef`.

### Pre-flight (worktree)
- [ ] **P0.** Branch the Slice-4 worktree from **local `main`** (Slices 1+2+3 at `cb86ff3`; local main may be ahead of `origin/main` and unpushed — **branch from local main**). Use `superpowers:using-git-worktrees` (detect native isolation first; verify the dir is gitignored). Confirm `python -m pytest tests/` green before writing. Confirm this CONVERGED doc is on the worktree's branch.

### Task 1 — The no-code characterization + the stale-comment fix
**Files:** Modify `tests/test_frontdoor_handoff.py` and `pipeline/frontdoor/handoff.py` (comment only).

- [ ] **1a. Stress-test provenance characterization** (honestly labeled — synthetic, not proof of a live run):
```python
from pipeline.frontdoor.handoff import Handoff

def test_stage_provenance_carries_stress_test_with_no_schema_change():
    """Characterization: the seam already carries a 'stress-test' stage entry — no stress.py, no field.
    Synthetic (a real run would interleave it); proves the CONTRACT, not a run. Note: element types are
    NOT code-enforced (stage_provenance is validated non-empty only); string values round-trip by convention."""
    h = Handoff(slug="grandmaster", characters=["kid", "grandma", "host-dad"],
                stage_provenance=["micro-expand", "interrogate", "art-viz", "stress-test", "synthesize"],
                mode="interactive")
    assert Handoff.from_json(h.to_json()) == h
```
- [ ] **1b.** Confirm `test_rejects_unknown_field` still green (the "no `stress_verdict` field" guard — no new test needed). Do **not** add a `stress_verdict`-specific magic-word test.
- [ ] **1c. Retire the stale docstring** in `handoff.py` (finding 6): change the line `style_route / stress_verdict land with Slices 3/4 — the schema grows with real consumers.` to reflect reality — both slices deliberately ship **no** such field; the verdict/route live as prose + seed refs, and the schema grows only when a real consumer exists. **Comment-only; no code/behavior/field change.** (This is the sole `pipeline/frontdoor/` touch; the schema and behavior stay byte-identical.)
- [ ] **1d. Verify + commit.** `python -m pytest tests/test_frontdoor_handoff.py -v`. `git commit -m "test(frontdoor): pin stress-test provenance round-trips; retire stale style_route/stress_verdict docstring"`

### Task 2 — Specify the fresh-context STRESS-TEST + reach all six writer surfaces (prose — the real deliverable)
**Files:** Modify `.claude/skills/brainstorm-front-door/SKILL.md`, `.../references/chain-map.md`, `.../references/concept-doc-template.md`, `.../references/session-sidecar-contract.md`, **`.../references/studio-brief-contract.md`**, **and `.claude/skills/frontdoor-synthesize/SKILL.md`**. Prose — verified by the Checkpoint-4 live rubric eval, not a unit test.

- [ ] **2.1 Insert Step 2.75 — STRESS-TEST** into `SKILL.md`, between ART-VIZ (2.5) and SYNTHESIZE (3): *once the look is locked, pressure-test the concept the room just built. First, a **cheap in-room reflex** — a quick pre-mortem that surfaces the obvious Tigers while still in context (a warm-up, not the authority). Then, **the authoritative pass: dispatch a fresh-context reviewer** (a sub-agent) that reads **only the draft `concept.md` + `00_studio_brief.md` — not this sidecar, not the proposals log** — blind to the room's love story, and runs the full pre-mortem + red-team: classify each risk **Tiger** (real → act) / **Paper-Tiger** (overblown → document) / **Elephant** (unspoken → investigate), **default to Tiger when unsure**, name the **Launch-Blocking** Tigers vs Fast-Follow / Track; steelman each load-bearing assumption then attack it; write each surviving risk as **"Fails if ___"** with its **cheapest test**; rank by impact × likelihood × cheapness-to-test. **Do not manufacture doubt** — a sound concept is said sound; **never attack the fragile high-value intuition** (name the engine, the nearest legitimate adjacent risk, and why the flagged weakness is not the engine in disguise — criterion 4). Propose a recommended verdict — **`proceed` (with named residuals) or `revise`** — as a `recommendation`; append only the four proposal kinds; **Sean decides; you** lock the verdict as a LOCKED DECISION and record `stress-test` in `stage_provenance`. **$0 — no spend, no render.*** State plainly: **not** a skill call; there is no `frontdoor-stress-test` skill; the fresh-context pass is the authority because verification wants independence; the **demotion trigger** (≥2 live runs redundant-with-reflex or missing-in-room-context) flips the inline reflex back to authority. **The production-binding rule:** a Launch-Blocking Tiger or a proceed-with-residual that changes buildability / budget / constraints must be handed to SYNTHESIZE for the **Studio Brief**, not left in `concept.md` only. Add STRESS-TEST to the chain diagram; update the "one future stage (STRESS-TEST)" note to "the STRESS-TEST stage, Step 2.75."

- [ ] **2.2 Edit `session-sidecar-contract.md`.** Add a `### stress-test` block (four kinds — `observations` = which assumptions are load-bearing + the same-context-bias note; `options` = the Tigers/Paper-Tigers/Elephants + "Fails if ___" red-team, each with its cheapest test + Launch-Blocking/Fast-Follow/Track tag; `recommendation` = the recommended verdict + named residuals; `open_questions` = unresolved). Add the LOCKED-DECISIONS convention `[Ln] stress verdict: proceed (residuals: <named Tigers>)`.

- [ ] **2.3 Edit `concept-doc-template.md`.** Add a movement **"Stress test (pre-mortem + red-team + verdict)"** (after "Objective / audience / distribution", before "Open threads"): the Tiger triage (Launch-Blocking named), the "Fails if ___" red-team with cheapest tests, the recommended verdict + residuals. Reframe "Open threads" as the stress test's **downstream tail** (Fast-Follow / Track residuals + genuinely-open questions), populated *from* the non-launch-blocking Tigers.

- [ ] **2.4 Edit `studio-brief-contract.md` (red-team finding 2, REQUIRED).** Name that a **production-binding stress residual** — a Launch-Blocking Tiger, or a proceed-with-residual that changes buildability / budget / constraints — lands in `### What this is NOT` or `## What are the non-negotiables?` (existing free-text sections; no new schema). Non-binding (Track / Fast-Follow) findings stay in `concept.md`. GRANDMASTER's register-gap Tiger is the exemplar that must reach Maya.

- [ ] **2.5 Edit `frontdoor-synthesize/SKILL.md`.** Teach it to: (a) fold the sidecar's `### stress-test` proposals into `concept.md`'s Stress-test movement; (b) carry the verdict lock as prose; (c) include `stress-test` in `stage_provenance` when present; (d) populate the "Open threads" tail from non-launch-blocking Tigers; (e) **fold any production-binding residual into `00_studio_brief.md`** (the load-bearing half — the brief is what Maya reads). No code — a prose edit mirroring the existing art-viz fold.

- [ ] **2.6 Edit `chain-map.md`.** STRESS-TEST row → **fresh-context reviewer (default) + inline reflex — not a skill / status: live (Slice 4)**; "What it does" = "pre-mortem (Tiger/Paper-Tiger/Elephant, default-to-Tiger) + red-team (steelman → 'Fails if ___' → cheapest test); recommended `proceed|revise` → prose + a sidecar LOCKED DECISION + Studio-Brief non-negotiable when production-binding (**no `stress_verdict` field**)"; skip = "none — always-on, non-blocking"; add the demotion trigger + the deferred SPEND-OK gate. Retire the "Until Slice 4 lands" proto-stress-test stopgap paragraph.

- [ ] **2.7 Commit.** `git commit -m "feat(frontdoor): fresh-context STRESS-TEST (default) + inline reflex; fold stress-test to concept.md, Studio Brief, template, sidecar; defer verdict field + spend gate"`

### Task 3 — The good-STRESS-TEST rubric + live validation protocol
**Files:** Create `.claude/skills/brainstorm-front-door/references/good-stress-test-rubric.md`.

- [ ] **3.1 Write the rubric** — the six §7.2 criteria, each with a worked positive from GRANDMASTER + ai-guru and a one-line anti-example; **criterion 4 carries the three-part substantiation requirement** (engine / nearest adjacent risk / why-not-the-engine-in-disguise); the **inline weak-concept anti-example** (the ships-red calibration case). Header it plainly: **a live human-review checklist for Sean — not a CI/prose gate; a model cannot self-pass it.** Name the **1 + 4 + 5 blocking block**. State the residual gameability honestly (why the authority is fresh-context). Cross-link `good-expand-rubric.md`, `good-art-viz-rubric.md`, `pinata-worked-example.md`.
- [ ] **3.2 Write the live validation protocol** (the Checkpoint-4 hand-off): *pick a piece with a live concept (a fresh spark, or re-open GRANDMASTER cold); run orchestrator → … → ART-VIZ → the inline reflex → the fresh-context STRESS-TEST; capture the `### stress-test` sidecar block + the verdict LOCKED DECISION + `stage_provenance` carrying `stress-test`; confirm a production-binding residual reached `00_studio_brief.md`; score against the six criteria (1+4+5 blocking). Optionally run a thin/weak concept to confirm it revises with ≥1 launch-blocking Tiger.* State plainly: Fable 5 builds to structural-green + this protocol; **Sean runs the live grill.** Include the §7.4 deferred SPEND-OK spec as an appendix.
- [ ] **3.3 Commit.** `git commit -m "docs(frontdoor): good-STRESS-TEST live-review rubric (criterion-4 substantiated) + validation protocol; SPEND-OK deferred spec"`

### Task 4 — Verification gate (before any "done")
- [ ] **4.1** `superpowers:verification-before-completion`: run fresh and paste output —
  `python -m pytest tests/` (full suite green, no regressions);
  `python -m pytest tests/test_frontdoor_*.py -v` (Slice-4 characterization green; Slice-1/2/3 tests still green);
  `md5 evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md pipeline/agents/prompts/sean-screenwriting-voice.md` (== the two guard hashes);
  `git status` (only the §8 paths; `pipeline/frontdoor/handoff.py` shows *only* a comment diff; no `frontdoor-stress-test/`, no `stress_verdict` field, no `criteria.py`/neutrality-test change).
  `git diff pipeline/frontdoor/handoff.py` (confirm the diff is the docstring line only — schema/behavior byte-identical).
- [ ] **4.2** Confirm the orchestrator reads coherently end-to-end: micro-expand → deepen?/EXPAND → INTERROGATE → ART-VIZ (2.5) → **STRESS-TEST (2.75: inline reflex → fresh-context authority)** → SYNTHESIZE (3), all coherent; the rubric is reachable from Step 2.75; "$0, no spend", "no `stress_verdict` field", "fresh-context is the authority", and "production-binding residuals reach the Studio Brief" are explicit; SYNTHESIZE folds `### stress-test` to concept.md **and** the Studio Brief.

## 10. Checkpoints

**Checkpoint 4 (Sean review — STOP here; the Fable 5 kickoff stops at first green).** Three gates:
- **Structural (CI):**
  - **4a** — `python -m pytest tests/test_frontdoor_*.py` (the stress-test characterization green; no frontdoor regression; `test_rejects_unknown_field` still green).
  - **4b** — `python -m pytest tests/` (full suite green) + md5 guards byte-unchanged + `git status` clean except the §8 paths + `git diff pipeline/frontdoor/handoff.py` is the docstring line only.
- **Semantic (§7.2, blocking — Sean's live pass):** the STRESS-TEST inline reflex + fresh-context authority authored; the chain-map flip; the six reach-the-writer folds (incl. the Studio Brief); the good-STRESS-TEST rubric + protocol shipped. Sean runs a live STRESS-TEST pass and scores it against the six criteria (1+4+5 blocking).
- **The ① DoD ratification (§0.2 B — same sitting or immediate follow-on):** one live five-stage run on a fresh spark, all four live rubrics scored, the emitted bundle validating + reaching the plan gate, **and a production-binding stress residual proven present in `00_studio_brief.md`** (read the emitted brief). **This closes ①.**

## 11. Risks

- **Self-critique bias — the load-bearing risk.** *Mitigation:* the authority is the **fresh-context pass** (§2.1), not the in-room reflex; criterion 4 demands substantiation; Sean's eye. The risk is *designed against*, not waved away.
- **Manufactured-doubt / false-rigor (the reverse failure).** *Mitigation:* criterion 4's three-part substantiation + criterion 1 (falsifiable Fails-if) + the fresh-context independence + Sean's eye. Honestly, weakly gameable (§7.2).
- **The Studio-Brief reach is skipped (the Slice-3 under-build, redux).** If a production-binding Tiger stays in `concept.md`, Maya never sees it. *Mitigation:* Task 2.4 + 2.5(e) are **required**; the DoD ratification (§0.2 B) verifies a residual reached `00_studio_brief.md`.
- **Scope creep into the spend gate / museum / Cy bridge.** *Mitigation:* §0 draws the DoD line; §8's `git status` gate enforces schema/behavior-identical `pipeline/frontdoor/`.
- **The one-comment `handoff.py` touch reads as a broken invariant.** *Mitigation:* it is comment-only (finding 6); §9 Task 4.1's `git diff` gate proves schema/behavior byte-identical. Flagged, not silent.

## 12. Codex reconciliation notes

Codex's independent plan (task `task-mr4z14kp-0d11d0`, session `019f282c…`; read the named files on `main` at `cb86ff3`, did **not** read this sketch) **converged strongly** — same call on all six questions: Q1 (ship inline v1, compare against fresh-context before declaring settled; (b) same-session skill is "the worst middle"); Q2 (*verbatim*: "keep `pipeline/frontdoor` byte-identical … Do not build the Higgsfield spend gate here just to manufacture a reader"); Q3 (three axes; GRANDMASTER proceed + Launch-Blocking-for-Cy register Tiger); Q4 (one characterization test, no stress-specific unknown-field test, live rubric); Q5 (same reach-the-writer files); Q6 (same DoD in/out split). The load-bearing call I first held on my own — **no schema field, byte-identical seam** — Codex reached independently, strengthening it.

**Folded from Codex:**
- **F-C1 — the step number.** STRESS-TEST is **Step 2.75** (between ART-VIZ's 2.5 and SYNTHESIZE's 3), not 3.5. A real error, corrected throughout.
- **F-C2 — the Studio Brief stays stress-free unless a lock makes it a constraint.** Adopted, then *sharpened by the red-team* (§13, finding 2) into a **required** rule: production-binding residuals **must** reach the Studio Brief.
- **F-C3 — name the fresh-context promotion as a conditional.** Adopted, then *inverted by the red-team's finding 1*: since fresh-context is now the **default**, the contingency is a **demotion** trigger, not a promotion (§2.1, §0.4).
- **Blocking-rule reconciliation.** Codex blocked on "falsifiability + triage + calibration"; I block on 1+4+5. Reconciled: criterion 1 carries falsifiability, criterion 5 carries triage, so 1+4+5 **absorbs** Codex's block and keeps criterion 4 (protect the intuition) a hard block — which the red-team then loophole-closed with the substantiation requirement.

## 13. Red-team fold (verdict: "not right-sized" — over-built on the fork, under-built on the production handoff — ACCEPTED)

Codex red-teamed the converged doc (task `task-mr4zc2p8-xznqj6`, session `019f2834…`) and returned **not right-sized in two directions at once** — the honest read. It **confirmed** the load-bearing calls (no `frontdoor-stress-test` skill, no `stress_verdict` field, byte-identical seam, the reach-the-writer edits, the GRANDMASTER-blocks-Cy fact) and the plan's named factual checks (finding 7). **All factual claims were verified against `main` before folding** (the file:line checks are in the red-team record). Six findings folded; one confirmation.

| Fold | Finding | What changed |
|---|---|---|
| **F1 — the fork was both over- and under-built (the core).** | Shipping (a) inline default + specifying (c) + an A/B comparison protocol + a separate weak-fixture file *dodged a position* and built bespoke machinery no prior slice built. | **§2.1 rewritten:** commit to **fresh-context (c) as the authoritative default** (verification wants independence; the stage's unique bias justifies it; (c) is the same cheap weight as (a)); inline (a) is the reflex. **Cut the A/B protocol + the separate fixture file;** the weak concept is an inline rubric anti-example; a **standard two-run demotion trigger** replaces the protocol. Smaller *and* takes a position. |
| **F2 — reach-the-writer still stopped at `concept.md`, not `00_studio_brief.md` (the real Slice-3 failure mode).** | `pipeline.run` + Maya read **only** the Studio Brief (`run.py:174`); a Tiger in `concept.md` is invisible to planning. | **Added `studio-brief-contract.md` as a REQUIRED sixth surface (§2.4, §8, Task 2.4/2.5e):** a production-binding residual (Launch-Blocking Tiger / buildability-or-budget-changing) folds into `What this is NOT` / non-negotiables. |
| **F3 — the DoD overstated what the smoke proves.** | `validate_brief_dir` doesn't check stress content or reach; the plan-gate test proves Maya *consumes* the brief, not that stress reached it. | **§0.1/§0.2 B/§10 sharpened:** the DoD ratification verifies a **production-binding residual landed in `00_studio_brief.md`** (readable), and Sean confirms Maya plans around it — not just "the plan gate accepts." |
| **F4 — criterion 4 was a loophole if hard-blocking.** | "Protect the fragile intuition" can be a **veto shield** (dodge a real structural attack by re-labeling it the engine), and hard-blocking it can invite under-flagging. | **§7.2 criterion 4 keeps the hard block but adds a three-part substantiation requirement** (name the engine, the nearest legitimate adjacent risk, and why the flagged weakness is not the engine in disguise). Closes both games. |
| **F5 — the `list[str]` claim was overstated.** | Runtime validation checks non-empty list only, not element types; `Handoff(stage_provenance=[1])` round-trips. | **§2.2/§3/Task 1a corrected:** "non-empty list; element types **not** enforced — string values round-trip **by convention**, not code-enforced `list[str]`." (The Slice-2 F7 / Slice-3 F6 honesty discipline, again.) |
| **F6 — retire the stale `handoff.py` docstring.** | The docstring still says `style_route / stress_verdict land with Slices 3/4` — false now that both ship no such field; leaving it is source-of-truth drift. | **Task 1c: a comment-only fix** retiring the line; the "byte-identical" claim refined to "schema + behavior identical; one stale comment retired," with a `git diff` gate (Task 4.1) proving it. The one deliberate, flagged `pipeline/frontdoor/` touch. |
| **F7 — confirmed, no change.** | The writer/template/sidecar facts and GRANDMASTER-blocks-Cy all hold. | Kept as-is. |

**Net:** the slice got **smaller on the fork** (cut the A/B protocol + the fixture file; committed to fresh-context) and **larger on the handoff** (the Studio Brief is now a required surface; the DoD verifies stress reaches Maya) — exactly the two-direction correction the red-team's verdict named. Every over-build boundary still holds: no new skill, no field, no spend, schema/behavior-identical seam (bar one comment).

## 14. Anti-drift note
Slice 4 opens no new workstream — ① is the active build (ROADMAP lock) and this is its **final** slice. It touches only `.claude/skills/brainstorm-front-door/*`, `.claude/skills/frontdoor-synthesize/SKILL.md`, `tests/`, and **one comment line** in `pipeline/frontdoor/handoff.py`; the seam's schema + behavior are byte-unchanged; no new skill; no `stress_verdict` field; no `criteria.py`/neutrality-test change; the two md5 guards are untouched; $0 spend. The whole-front-door plan already scoped STRESS-TEST as Slice 4; this refines its *implementation* (fresh-context authority + inline reflex, the verdict + field + spend gate deferred, the Studio Brief reached) against the evidence, the self-critique-bias caveat, and the red-team's two-direction correction — and it draws ①'s Definition of Done (§0) so the front door finishes *here*. It shrinks scope on the fork and sharpens it on the handoff; it does not expand it.
```
