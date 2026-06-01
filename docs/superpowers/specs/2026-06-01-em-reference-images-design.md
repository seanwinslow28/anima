# Em Reference-Images — Design Spec

**Date:** 2026-06-01
**Status:** Design — approved in brainstorm, pending written-spec review before `writing-plans`.
**Branch:** `feature/em-reference-images` (worktree off `main` @ `458b248`, the #12 merge — the settled critic-spine baseline this work supersedes).
**Spec author session:** brainstorm with Sean, 2026-06-01.
**Finding this closes:** [`docs/anima-test-runs/2026-06-01-em-reference-blindness-FINDING.md`](../../anima-test-runs/2026-06-01-em-reference-blindness-FINDING.md) — the locked #1 critic-spine fix.
**Methodological basis:** [`docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md`](../../research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md) (the eval handbook — §3.4 reference-guided judging, §3.5 vision-judge limits, §4 eval-prod parity + false-pass + snapshot-pinning, §2 ships-red/no-Goodhart, §5 `stderr` on the delta).

---

## 1. The problem (why this exists)

Em, anima's T2 vision critic, **judges every frame against text only.** `VisionCriticNode.run()` attaches exactly one image — the frame under review (`image_paths=[model_image_path]`, [`pipeline/agents/vision_critic.py:113`](../../../pipeline/agents/vision_critic.py) and `:122`). She receives no `anchor.png`, no Bible plate, no prior approved frame. She also never reads `ctx.criteria` (the merged `CriteriaBundle` is defined on `AgentContext` but Em ignores it). Yet her own addendum trains her to reason about an anchor she cannot see ("the A-2 anchor and F18 both read closer to 65°…").

The 2026-06-01 scored baseline quantified the cost: on the **performs** segment (clean + identity/style, n=23) Em scored **recall 1.00, false-pass 0.00, precision 0.62** — she caught every real defect and let through zero, but raised **8 false alarms on clean frames** (failing `clean_F13` and `clean_F31`, which Sean confirmed are unmistakably the correct Sean). With no reference to confirm "this *is* correctly Sean → pass," she has no licence to pass; she flags on whatever text-rule she can measure off the pixels. The precision gap is **reference-blindness, not over-strictness.**

The fix is one shape: **give Em the Bible — its reference plates *and* its `IR.*`/`AC.*` criteria — as inputs.** The pre→post precision lift is the portfolio artifact: the moment Em stopped grading blind. But the same mechanism that lifts precision — granting Em *licence to pass* — is the mechanism that could regress `false_pass_rate` from its baseline 0.00, so recall-holding is the **vigilantly-watched guard, not an assumption** (§9): the headline is "precision rose *and* no false pass appeared," never precision alone.

A second, adjacent finding from the same baseline's bake-off folds into this workstream (same runner surface): **the agy rate-cap wrapper bug** — a quota-exhausted empty response is reported `ok=True` and silently degrades every frame to `borderline` instead of erroring.

---

## 2. Goal & scope

**Goal.** Make Em reference-grounded: attach a capped Bible reference bundle + surface the character's IR/AC criteria, measure the precision lift **without regressing `false_pass_rate`/recall** against the locked baseline, and fix the two adjacent plumbing bugs the baseline surfaced — in one focused, TDD'd arc.

**In scope:**
1. A `select_references()` seam that returns a fixed, Bible-driven, capped reference bundle (approach **B**), with a signature ready for view-aware selection later (approach A) without an eval re-wire.
2. Em reads references (explicit image ordering) + the merged `CriteriaBundle` (cites `IR.*`/`AC.*`).
3. The agy rate-cap wrapper fix (`RateCapExhausted`).
4. The case-7 xfail flip (`evals/character_designer/`) — input-key validity fix + `IR.sean.*` ID alignment.
5. Eval re-wire for parity (`character_id` per case + shared `select_references`), then a **live re-baseline** behind a human re-ratification gate, and a **re-run of the three-way bake-off** with pinned model snapshots.
6. Docs: CHANGELOG, CLAUDE.md Em row, a dated field report, the three named follow-ons.

**Out of scope (named follow-ons, §11):** view-aware reference selection (approach A), the pairwise-verdict reframe, the DINOv2 deterministic identity backstop, the motion-proper metric (E_warp/VBench).

---

## 3. Decisions locked in brainstorm

- **Approach B over A.** Anchor + a capped, deduped turnaround set; the *same bundle every frame*; eval == production. A is the real per-view cure, but production has no per-shot view metadata today, so A's eval would hand-label an idealized view-match prod can't reproduce — measuring a path that doesn't ship (the handbook's §3.5/§4 parity objection). B has a zero parity gap and zero new prod machinery, gives Em a matching view for most shots (it's in the set), and is **the cheapest experiment that tells us whether we even need A**: if anchor+turnarounds lifts precision enough, A never gets built; a shortfall on profile/turn shots is the evidence-backed trigger for A. Empirical, not vibes.
- **Not C (anchor-only):** §3.5 says the single front anchor is known-insufficient (the exact thing the similarity-gate flagged) — it would resolve the near-frontal F13/F31 but knowingly ship what the research said fails for profile/turn shots.
- **Cap small:** anchor + ~3 canonical deduped turnarounds (front / 3-quarter / profile). Too many references dilute the which-image-is-the-subject signal and add position-bias surface + latency to an already 25–80s/case path. The **NB-Pro multi-reference downsampling regression is a *generation* bug (Cy authoring), not a *judging* one** — Em reads images to critique, a different path — so "flooding" is a context/latency/dilution concern, not a downsampling one.
- **`character_id` canonical = `sean`** (not `sean-anchor`). Evidence (grep): `IR.sean.*` is load-bearing in 100+ committed places (the *locked* `acceptance_criteria.json` rule IDs, `plate_generation_plan.json` 127×, ~80 museum exhibit files, three `tests/`, `cases.yaml`, `character.yaml: character_id: sean`, CHANGELOG, docs). `IR.sean-anchor.*` (hyphen) appears in exactly 4 files — all the case-7 scaffolding. So the inconsistency lives in the *case-7 mock*, not the real Bible; reconciling the real ID would ripple through the locked Bible + the entire committed museum. The folder/registry key stays `sean-anchor`; the Bible's own `character.yaml` (`character_id: sean`) is the single source of truth.
- **agy rate-cap → raise an honest errored gap** (not auto-escalate). Quota exhaustion is missing data, not a verdict; `score.py` is already per-case resilient so an errored case is recorded honestly and excluded from the matrix. Auto-escalate would mask the throttle (papering over the finding) and conflate a plumbing failure with Em's judgment-based escalation. Raise a **distinct** `RateCapExhausted` so a real throttle is never confused with a parse failure in the trace.
- **Pairwise reframe → OUT, logged.** It changes Em's whole verdict shape (verdict/confidence/cites_criteria contract) — a separate surfaced contract decision, not something to bury here.
- **Worktree off settled `main`.** #12 is merged; reference-attach invalidates and re-baselines everything #12 produced, so we start from the settled baseline we're about to supersede. Confirmed sole-meaningful-agent (one idle session present, isolated by the worktree).

---

## 4. Component A — `select_references()` (the forward-compatible seam)

**New module:** `pipeline/agents/reference_selection.py`.

```python
class ReferenceSelectionError(Exception): ...   # only for unrecoverable mis-config; missing plates never raise

def select_references(
    character_id: str,
    checkpoint: str,
    beat: str,
    *,
    characters_root: Path,
    cap: int = 3,
) -> list[Path]:
    """Return the reference bundle to attach for one Em invocation.

    v1 (approach B): the FIXED capped bundle — anchor + up to `cap` canonical
    deduped turnarounds (front / 3-quarter / profile) — RESOLVED FROM THE BIBLE,
    ignoring checkpoint/beat. The signature already accepts checkpoint/beat so
    approach A (view-aware selection) drops into this body later with no change
    to the eval contract or the harness shape.
    """
```

**Bible-driven resolution (not hardcoded filenames).** Hardcoding `turnarounds/head-front.png` is the same class of bug as the sean/sean-anchor mismatch — it assumes Sean's exact filenames and breaks on claude-mascot (5 ingested turnaround crops, different naming). Instead:

1. Resolve the character's folder from `characters_root` + a folder lookup. The folder key (`sean-anchor`) is *not* the `character_id` (`sean`); the resolver maps `character_id → folder` by reading each Bible's `character.yaml: character_id` under `characters_root` (single source of truth, no invented mapping table). It also accepts a folder key directly for the common single-Bible case.
2. The anchor is always `<folder>/anchor.png`.
3. Turnarounds come from the Bible's declared plate inventory where available (`character.yaml` / `plate_generation_plan.json`), else by globbing `<folder>/turnarounds/*.png`. From that set, pick up to `cap` canonical, deduped views biased toward **front / 3-quarter / profile** (a view-keyword preference over the available filenames, so it self-adapts: Sean resolves to `anchor + head-front + head-profile-left + body-3quarter`; the mascot resolves to its own front/3-quarter/side crops).
4. **Existence-check every path; silently drop missing ones with a logged note.** A thin bundle is honest; the critic never crashes on a missing plate (mirrors Mo's never-invent / thin-is-honest contract).

**Resolved bundle for Sean (the brainstorm target):** `anchor.png` (¾ hero) + `head-front` + `head-profile-left` + `body-3quarter` — a frontal face, a profile face, and a full-figure proportion reference, plus the anchor. 4 references + the subject = 5 images, under the dilution threshold. (`profile-left` is the default; `-right` is interchangeable.)

**The same function is called by both the eval harness and production** — the parity guarantee (§7).

---

## 5. Component B — Em reads references + criteria

**File:** `pipeline/agents/vision_critic.py`.

### 5.1 Attach references in `run()`
Both the Gemini default path (`:113`) and the Opus escalation path (`:122`) change from `image_paths=[model_image_path]` to:

```python
references = select_references(character_id, checkpoint, beat, characters_root=...)
image_paths = [model_image_path, *references]   # subject is ALWAYS image 1
```

- `character_id` arrives as a new optional Em input (default resolved from the manifest's single registered Bible when absent — acceptable for the single/low-character pencil test; see §7).
- `characters_root` is resolved from the repo root (the `characters/` dir).
- Phase 6 (motion) contact-sheet path: references attach here **too** (identity-across-the-strip benefits from the canonical reference, and Em already catches across-strip continuity). This does **not** change the motion-proper segment's expected-red status — references grant identity licence, not motion sight.

### 5.2 Tell Em which image is which (`_build_prompt`)
Prepend an explicit ordering block:

> *"Image 1 is the frame under review. Images 2..N are identity/style reference plates from this character's Bible — the canonical truth for who the character is. Compare the subject against them. Do not flag a difference that the references confirm is correct; a feature that matches the references is correct even if it differs from a generic expectation."*

This is the licence-to-pass Em lacks today — the §3.4 "reference-guided judging" defense made structural. **It is also a sycophancy surface** (the one confirmed 58% bias number): "do not flag a difference the references confirm is correct" is correct, but phrased too strong it over-suppresses flagging and waves real drift through. The wording stays **deliberately conservative**, and its empirical guard is the `false_pass_rate` (§9) — the prompt grants licence-to-pass; the matrix is what proves the licence wasn't abused.

### 5.3 Surface the criteria (`_build_prompt` + read `ctx.criteria`)
Em reads `ctx.criteria` (the `CriteriaBundle`, currently never read) and surfaces, as a terse labeled list:

```
query_by_character(character_id) ∩ query_by_phase(phase)
```

where `phase` derives from the checkpoint (`phase_5_generate`→5, `phase_6_motion`→6, `phase_8_assemble`→8). The block reads: *"Here are the IR/AC rules for this character at this phase; cite by ID the ones you observe drift on."* — the Databricks Grading-Notes pattern (handbook §3.4). When `ctx.criteria is None` (pencil-test legacy runs), the block is omitted gracefully and Em behaves as today (no regression).

**Designed behavior on an empty intersection.** `query_by_character ∩ query_by_phase` can legitimately be empty — e.g. a character whose IR rules aren't tagged at `phase_6`. That yields an empty criteria block at that checkpoint, which is *correct* (no rules to cite), not a bug; Em falls back to her standing context as today. This is verified by TDD (a phase with no matching rules surfaces no block and does not crash), so the empty case is designed, not a surprise. (Sean's Bible *does* carry `motion`-category rules tagged at phase 6, so the phase-6 intersection is non-empty where it matters today.)

This is the criteria half of "give Em the Bible," and it is what flips case-7 green.

---

## 6. Component C — agy rate-cap fix

**File:** `pipeline/agents/cli_runners.py` (`run_antigravity_with_image`).

Today `_RATE_CAP_SIGNALS` is matched against **stderr only**, but agy writes the 429 / `RESOURCE_EXHAUSTED` to its **log file** and returns exit-0 with empty stdout → `rate_capped=False, exit_code=0, error=None` → `ok=True` → Em parses empty→`borderline`. In production this silently degrades every frame during quota exhaustion.

**Detection rule (the must-get-right part):** raise `RateCapExhausted` when **either**

- **(a)** stdout is empty/whitespace on exit-0, **or**
- **(b)** an explicit `429` / `RESOURCE_EXHAUSTED` / quota signal appears in stderr **or agy's log file** (log path confirmed during implementation).

A **non-empty-but-unparseable** response is **NOT** a rate cap — it stays on the existing defensive-borderline path in `vision_critic._parse` (the documented JSON-parse-failure mode from postmortem Failure 1). **The distinguishing fact is empty vs malformed, not parses-vs-doesn't.** Routing "no parseable JSON" to `RateCapExhausted` would relabel that legitimate mode as a throttle and lose it. Two failure modes, kept separate in the trace.

**Signal (a) is the primary, robust catch.** The observed bug was empty stdout on exit-0 in ~2.2s — so (a) alone detects the known failure; agy-log-path discovery for (b) is a corroborating signal, not a hard dependency. If the log path proves hard to locate reliably, (a) + stderr-scanning still close the silent-degradation hole.

**Behavior on detection:** raise the distinct `RateCapExhausted(Exception)` from the wrapper. `vision_critic.run()` lets it propagate (it is not a verdict); Em's confidence-based escalation stays independent (no auto-escalate-on-throttle). `score.py`'s per-case resilience records it as an honest *errored* gap, excluded from the matrix. The stub-fallback path (binary absent) is unaffected — only a present-but-throttled agy triggers this.

---

## 7. Eval re-wire — the parity refinement (signed off)

The kickoff's literal text was "add a `references:` field per case." Taken literally, a hand-authored plate list per case **is approach A's pattern** — a human labeling which plates to attach — which reintroduces the exact eval-prod gap B was chosen to avoid (the frozen list silently diverges the moment `select_references` changes). Parity-by-discipline rots.

**The refinement (signed off):** `cases.yaml` gains **`character_id:`** (which character the frame contains; defaults to `sean` — all current cases are Sean), **not** a plate list. Then the harness (`runner.py`, `score.py`) **and** production both call the **same** `select_references(character_id, checkpoint, beat)`. One code path computes the bundle, so the eval *cannot* measure a bundle prod doesn't produce — **parity is structural.**

Consequences:
- **Forward-compat is free:** when A lands, `select_references` returns view-matched plates and the eval picks them up because it *calls the function* — no cases.yaml churn, no harness re-baseline.
- **The right thing is unit-tested in the right place:** "does `select_references` pick the profile turnaround for a profile beat?" is a unit test on `select_references`, not an assertion smuggled into cases.yaml. `cases.yaml` stays labels + `character_id`.
- **The trace records what Em saw:** `last-run.md` logs the resolved plate list per case ("Em saw: anchor, head-front, head-profile-left, body-3quarter") as a logged *output*, never a hand-authored *input*.

**Wiring details:** `score.py` (and the mocked `runner.py` harness) must `load_all_criteria(manifest)` and pass the bundle into `ctx.criteria` (today `score.py` passes `criteria=None`), and pass `characters_root`. No optional per-case `references_override:` in v1 (YAGNI; add only if a "wrong-reference" test is ever needed). In production, the DAG runner already calls `load_all_criteria(manifest)`; the plan verifies it threads the bundle into the vision_critic node's `ctx.criteria` and supplies `character_id` from the shot/frame definition (fallback: the single registered Bible).

---

## 8. Component D — case-7 (`evals/character_designer/`)

Two legitimate fixes flip the intentionally-red xfail (`closing-the-loop-em-cites-cy-rules`) green:

1. **Validity fix (input keys):** the test's `em_ctx` passes `candidate_path` / `frame_num` / `manifest_style_block`, but `VisionCriticNode.run()` reads `image_path` / `frame_id` / `checkpoint`. Today the case throws `KeyError` *before* Em judges, and the non-strict xfail swallows it. Correct the keys to Em's real contract.
2. **ID alignment:** the mock Bible + the assertion use `IR.sean-anchor.*`; correct to `IR.sean.*` (canonical, per §3). The mock's authored `character_id` becomes `sean`.

With Component B loading criteria, Em then cites an `IR.sean.*` rule against the deliberately-broken frame → green. That xfail→green diff is the portfolio narrative ("the moment Bible authoring became contract-grounded"). Re-run: `.venv/bin/python -m pytest evals/character_designer/runner.py`.

---

## 9. The re-baseline discipline (the headline, kept honest)

After the code lands, re-run the live scorer and the bake-off. The disciplines, stated so they don't drift — **the false-pass guard first, because the intervention's mechanism is the risk's mechanism:**

1. **The false-pass guard is the primary watch, not precision.** Giving Em references grants "licence to pass" — that is exactly what resolves the 8 clean-frame false alarms *and* exactly what can make her wave a real defect through. The bake-off already demonstrated this: Opus, the voice that licensed the most passes, produced the workstream's only false pass (`stylus-hand-f13-cc01`, a real CC01 defect). The reference-blind baseline's `false_pass_rate = 0.00` / `recall = 1.00` is the number **most at risk of regressing**, and it is the *costly* error (handbook §4). So the headline is not "precision rose" — it is **"precision rose AND `false_pass_rate` stayed 0.00 / recall held."** A precision lift that costs *any* false pass on the performs segment is a **worse Em, not a better one**, and blocks the change. Report precision, recall, *and* false-pass deltas, each with `stderr`.
2. **Report every delta with `stderr()`.** The performs segment is ~23 cases; a move from precision 0.62 (or any recall slip) needs its standard error to separate signal from noise. `scoring.py` already has `stderr()`; apply it to each delta and do not over-claim a lift inside the noise band.
3. **`cites-correct` is the second headline lift — the clean proof the criteria-half worked.** Surfacing `IR.*`/`AC.*` rules should move `cites-correct` (baseline 0.43 performs / 0.33 overall) at least as cleanly as references move precision. It is arguably the *cleaner* portfolio data point: references resolve false alarms (a precision story that the false-pass guard complicates), but `cites-correct` rising is unambiguous evidence the Bible's rules became first-class context Em grounds in. Report its pre/post delta with `stderr` alongside precision.
4. **Labels stay locked.** When precision rises, the cases are **not** re-labeled to flatter Em (Goodhart / handbook §2). "Re-ratification" means Sean re-confirms the locked `af7950d` labels still stand — the baseline *number* moves, the labels don't, unless a genuine validity error surfaces (and that is a separate, surfaced edit, never a quiet one). **A human gate:** any label that would flip is presented to Sean and re-ratified *before* lock.
5. **Re-run the bake-off + pin/record model snapshots.** All three models were equally reference-blind and Gemini's column was quota-invalid, so the T2 model decision can only be licensed after references land + the rate-cap fix. Re-run `evals/bakeoffs/2026-05-31-t2-vision-critic-gemini-vs-sonnet-vs-opus/bakeoff.py`, record the exact model snapshots (the silent-regression catcher, §4), write the Decision section — judging the candidates on the **false-pass-first** lens (cf. the prior round, where Sonnet ≥ Opus precisely because Opus's extra "sharpness" came from a false pass). (If Gemini quota is still throttled, the now-fixed `RateCapExhausted` makes that an honest errored column rather than a fabricated borderline one; a fully-valid three-way may then be a same-day re-run after quota reset.)

**Run mechanics:** the live `score.py` is ~25–80s/case, ~24 min total — **run in the background**; mind the consumer-tier agy/Gemini quota. `--stub` forces the credential-free path for plumbing checks.

---

## 10. Testing strategy (TDD)

Every code seam is test-pinned, written test-first. Credential-free (runners self-stub; no `ANTHROPIC_API_KEY`).

- **`select_references`** — unit tests: resolves Sean's bundle from the real Bible (anchor + 3 turnarounds, capped); resolves the mascot's differently-named crops without code change; drops a missing plate with a thin-but-valid bundle (no raise); subject-order contract (references never include the subject frame); the `character_id → folder` resolver maps `sean`→`sean-anchor/`.
- **`vision_critic` prompt** — `_build_prompt` emits the image-ordering block; surfaces `query_by_character ∩ query_by_phase` rules when `ctx.criteria` is set; omits the criteria block (no crash) when `ctx.criteria is None`; phase-6 still carries the motion honesty clause *and* now references.
- **`vision_critic.run()`** — attaches `[subject, *references]` on both paths (subject index 0); references attach on phase-6 too.
- **`cli_runners`** — empty-stdout-exit-0 → `RateCapExhausted`; 429-in-log → `RateCapExhausted`; **non-empty-unparseable → NOT raised** (stays defensive-borderline); stub-fallback path unaffected.
- **case-7** — flips xfail→green (`evals/character_designer/runner.py`).
- **Eval harness** — `runner.py` (CI-green mocked) still passes incl. the new `character_id` plumbing + `select_references` call; the 6 motion-proper cases stay red; `score.py --stub` still exercises the path.
- **Regression:** `.venv/bin/python -m pytest tests/` (242 baseline) and `.venv/bin/python -m pytest evals/vision_critic/runner.py` stay green; run `tests/` and `pipeline/tests/` separately (duplicate-package-basename collision).

---

## 11. Out of scope — three named follow-ons + one deferred metric

Explicit, not silent gaps:

1. **View-aware reference selection (approach A).** Slots into `select_references`'s existing signature. Trigger: a precision shortfall on profile/turn shots in the re-baseline, or Em drowning in the fixed bundle. Pairs naturally with #2.
2. **Pairwise-verdict reframe** (handbook §3.5: "is A or B closer to the anchor?"). MLLM judges are most reliable pairwise. A separate contract change to Em's verdict shape; a future sharpening once references prove out.
3. **DINOv2 deterministic identity backstop.** Handbook §3.5/§6: MLLM identity judgment alone is weaker than DINOv2 cosine, and anima already has the `similarity_gate` ladder. Em-with-references is the right MLLM layer; the strongest identity signal is a deterministic DINOv2 cross-check beside it.

**Deferred metric (unchanged):** motion-proper (E_warp/VBench). The 6 red motion cases are its ready-made validation set; the human seam covers it now.

---

## 12. Operational guardrails

- **Isolated worktree** at `.claude/worktrees/feature+em-reference-images/`, branch `feature/em-reference-images`, off `main` @ `458b248`. One idle second session present (PID 22428) — isolated by the worktree; **never killed** (Failure-2's near-miss was an authorized kill of the wrong PID; always resolve own PID first).
- `.venv/bin/python` / `.venv/bin/pytest`. `agy` on PATH; `claude_agent_sdk` importable; **no `ANTHROPIC_API_KEY`** (SDK uses Claude Code auth — keep it that way). `.env` has `GEMINI_API_KEY` + `FAL_KEY`. Pass `load_dotenv('.env')` explicitly (heredoc `load_dotenv()` fails).
- **Don't weaken Em's `cites_criteria` invariant** or tune cases to pass. A label edit is legitimate only as a validity fix, never to flatter Em.
- **Update CHANGELOG.md on every change**; update CLAUDE.md (Em row → "reference-grounded, baseline re-run") on structure/convention shift.

---

## 13. Definition of done

- `select_references` ships, Bible-driven, capped, with the view-aware seam; unit-tested.
- Em attaches references (subject = image 1, both paths, incl. phase-6) and surfaces `IR.*`/`AC.*` criteria from `ctx.criteria`; unit-tested.
- agy `RateCapExhausted` fix ships with the empty-vs-malformed distinction; unit-tested.
- case-7 flips xfail→green (validity + ID alignment).
- Eval re-wired for structural parity (`character_id` + shared `select_references`); CI harness green, motion cases red.
- Live re-baseline run (background) → new `last-run.md` + dated trace, showing the precision lift **with `false_pass_rate` held at 0.00 / recall held** and `cites-correct` risen, each delta carrying `stderr`; **labels re-ratified by Sean before lock**. (A precision lift that costs any false pass blocks the change — §9.)
- Bake-off re-run with pinned snapshots → updated `results.md` decision.
- Docs: CHANGELOG, CLAUDE.md Em row, dated field report, the three follow-ons logged.
- `tests/` (242) + `evals/vision_critic/runner.py` green.

---

## 14. Risks

- **References grant licence-to-pass; the danger is recall slips / a false pass appears** (cf. Opus in the bake-off — its lone false pass `stylus-hand-f13-cc01` came from the same licence-to-pass this change hands Em). This is the *costly* error and the metric most at risk of regressing from `false_pass_rate = 0.00`. **Mitigation + named escalation:** the false-pass guard is the §9 primary watch; and **if the re-baseline shows *any* false pass on the performs segment, that promotes follow-on #3 (the DINOv2 deterministic identity backstop) from deferred to *next*** — it is the deterministic guard against exactly the drift a now-licensed Em might wave through. The risk is coupled to its mitigation, not left hanging.
- **Precision lift lands inside the `stderr` noise band** (~23 cases). Mitigation: report the band honestly; a small-but-clear lift still validates the direction, and the discipline is to not over-claim. A null result is itself the evidence-backed trigger for approach A.
- **agy quota still throttled at re-baseline time.** Now surfaces as an honest errored column (the fix), not a fabricated borderline. The Gemini bake-off column may need a post-quota-reset re-run — acceptable; the Sonnet/Opus columns are valid meanwhile.
- **`character_id → folder` resolver edge cases** (a future multi-Bible frame). v1 default-to-single-Bible is honest for the pencil test; multi-character shots are an A-adjacent concern, flagged not built.
- **Production `character_id` source.** The shot/frame definition must carry it; fallback is the single registered Bible. Real multi-character production wiring is downstream of this experiment.
