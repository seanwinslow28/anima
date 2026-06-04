# Em's instrumented mini-run — the failures we prevented, the one the remote handed us, and what the cites told us

*2026-06-04. The first costed move of the G6 arc: a single-pass diagnostic of Em (T2 vision critic) to de-confound the `cites-correct = 0.03` finding from G5. Unlike the Cy Bible session — five live failures debugged one at a time — this run had **zero execution failures**. A 19-row pre-flight flag table turned every predicted failure into a non-event before it could fire, and a $0 stub proof + a smoke-then-pause checkpoint kept the live spend honest. The one real failure arrived at `git push`, where the plan's "merge into main" step collided with a remote that had diverged. This is the field report on why the boring runs are the ones that went right, and the one place the brief was wrong about the world.*

---

## What the session was supposed to be

The handoff ([`docs/2026-06-04-em-instrumented-mini-run-handoff.md`](2026-06-04-em-instrumented-mini-run-handoff.md)) was explicit about shape and discipline: a **diagnostic, not a baseline**. One run × 50 cases (~50 Gemini calls + occasional Opus escalations), config held **identical to the ratified G5 baseline** so the verdicts stay comparable, persist per-case `cites` + `reasoning` into a trace, answer three questions (Q1 style cites, Q2 `clean-c06`, Q3 geometry vocabulary), and land it on main without moving the baseline, relabeling a case, or touching Em's prompt/criteria.

The standing doctrine printed at the top of the handoff was the load-bearing instruction: **"verify against the tree, never trust a label — including this brief."** That sentence ended up being the thread that ran through both the win and the one failure.

What was supposed to happen: instrument the trace writer (a small diff), prove it costs $0 mocked, run Em live once, read the cites, write it up, merge into main. What actually happened: exactly that — until the final `git push`, which the plan had described as a one-liner and reality made into a governance decision.

---

## The discipline that prevented the failures

The Cy session learned that stub fallbacks hide real-model failures until a live run trips them. This session inverted that: we ran the failure analysis **first**, in plan mode, and shipped a 19-row flag table (F1–F19, severity + mitigation) before any code or any spend. Most of those rows describe a failure that *would* have happened and didn't. The load-bearing ones:

**F1 — the same-day trace clobber (CRITICAL, prevented).** The live scorer writes its dated trace to `traces/baseline-{YYYY-MM-DD}-scored.md`. Today is 2026-06-04 — the exact filename of the **ratified G5 baseline trace**. An unmodified run would have silently overwritten the ratified artifact and the `last-run.md` that the CLAUDE.md Em row cites as the baseline matrix. This is the Cy-session failure shape in miniature (an action that looks successful while destroying something load-bearing), and it was caught at the planning desk, not on disk. Mitigation shipped as a `--trace-name LABEL` flag that writes only `traces/{LABEL}.md` and leaves `last-run.md` + the dated baseline untouched. We then **proved** it: the G5 trace's sha (`2138ccd…`) was recorded at pre-flight and re-checked after the stub run, the smoke run, the second smoke, and the full run — byte-identical at every checkpoint.

**F2 — the `gemini_api` cost-leak class (CRITICAL, proven closed).** This is the exact bug commit `71f8d80` fixed during the G5 pre-flight: the mocked harness stubbed only the legacy `agy` transport, so on a machine with a `GEMINI_API_KEY` the "credential-free" path fired real, costed calls. The handoff's pre-work step named it specifically. Rather than trust that the fix held, we proved $0 the way the Cy session's lesson would prescribe — by making a leaked call *fail loudly*: ran `--stub` and confirmed every case returned the distinctive STUB verdict (`borderline`@0.78, 0s wall, the STUB reasoning string). A real call cannot produce that signature. Zero live calls, demonstrated rather than asserted.

**F8 — `.env` is gitignored, so a fresh worktree doesn't have it (HIGH, prevented).** The per-case subprocess worker re-loads `.env` from the worktree root. A `git worktree add` does not carry gitignored files, so without an explicit `cp .env` the workers would have had no `GEMINI_API_KEY` and every live call would have failed (or worse, stub-fallen-back and produced a fake matrix). Caught in the flag table; the worktree got its own `.env` copy, grep-verified to carry `GEMINI_API_KEY` and **not** `ANTHROPIC_API_KEY`.

**F10 / F11 — the two ways the instrumentation diff could have broken the suite (HIGH, prevented).** F10: appending `reasoning` anywhere but the *last* field of `CaseScore` would have broken the positional constructors in `test_em_score_report.py` and `score.py`. F11: the new typed `EmptyCitesInvariant` had to keep every `except ValueError` and the two `pytest.raises(ValueError, match="cites_criteria")` tests valid. Both were neutralized by design (field last + defaulted; exception subclasses `ValueError`), and confirmed by grepping the tests for the exact assertions *before* editing — verify-against-the-tree applied to my own diff.

The pattern worth keeping: **a failure surfaced in planning is a line in a table; the same failure surfaced in production is a debugging session.** The Cy run paid ~$5–10 and two hours to discover its failure modes live. This run paid the cost up front in a Plan agent and a flag table, and the live phase was uneventful by construction.

---

## The one self-inflicted stumble — premature evidence deletion

Not every move was clean. During the `--limit 2` live smoke, I verified the matrix and the detail table, confirmed the model label (`gemini-3.5-flash@gemini_api + opus-4.7-escalation`), and then **deleted the smoke trace before confirming the reasoning prose was non-empty** — which is the entire point of the instrumentation. A `sed` range that stopped at the first blank line had shown an empty-looking reasoning section, and I'd already `rm`'d the file. The fix was cheap (one more 1-case live call, ~1 Gemini call, which showed Em's full multi-sentence reasoning paragraph), but it was avoidable: I disposed of the evidence before I'd actually read it.

**The lesson is small and concrete:** when the deliverable is "did this artifact capture X," confirm X is present *in the artifact* before deleting the artifact — and don't trust a `sed`/`grep` range to prove absence (the prose was there; my range query wasn't). It cost a dollar's worth of tokens, not a baseline, but it's the same family as the Cy session's "a successful-looking output can lie."

It also surfaced a real signal worth recording: across the three live touches of `clean-c01` this session it returned `pass@0.78`, `borderline@0.68`, and `pass@0.82` — the Opus verdict **variance** the G5 baseline diagnosed, visible in three samples of one case. A single N=1 pass is a snapshot, not a distribution. We answered the diagnostic's questions on one sample by design (it was a cheap diagnostic), but the variance is the asterisk on every per-case number below.

---

## The real failure — the remote had diverged, and the plan didn't know

Everything through "merge feature→main" went to plan. Then `git push origin main` was **rejected**: origin/main contained work I didn't have locally.

The investigation (fetch, then `rev-list --left-right --count`, then `merge-base`) told the story:

- The ratified **G5 work had landed on origin as a squash-merge, PR #22** (`13a1892`) — one commit.
- My local `main` carried the same G5 content as the **full branch history** (the G6-kickoff fast-forward), plus the local-only **G6-kickoff commit `fc87e54` that had never been pushed** (the prior session's CHANGELOG even said the push was "pending on Sean's machine").
- So the same content existed on both sides via *different commits*, local was 8 ahead / 1 behind, and an in-memory merge conflicted **only** in the two narrative source-of-truth docs (CHANGELOG.md, CLAUDE.md) — because the squash wrote a different G5 narrative than the full history did.

The plan's final step — "merge feature→main, push" — was written to *correct* the G5 near-miss (which had merged main *into* the branch, the wrong direction). The intent was right. But the step silently assumed local `main` was the canonical history, and the repo's actual workflow is **squash PRs on GitHub**. The brief was wrong about the world, exactly the case the standing doctrine warns about.

**The honest process miss is mine:** I executed the local `feature→main` merge *before* verifying remote state, creating a throwaway local merge commit (`d6dd58c`) that I then had to unwind. Had I run `git fetch && git rev-list --left-right --count main...origin/main` *before* the merge — a free, read-only check — I'd have seen the divergence and gone straight to the PR. The verify-against-the-tree doctrine applies to remote refs too, and it applies *before* the irreversible-looking step, not at the error message.

**How it resolved (cleanly, with the user in the loop):** I stopped at the rejected push rather than force-anything, surfaced the divergence with the three concrete options (clean PR / merge-and-push / hand off), and Sean chose the clean PR. The mechanic that made it tidy: branch off `origin/main`, **cherry-pick both** `fc87e54` (the unpushed G6-kickoff docs — my report and CHANGELOG link to them, so omitting them would dangle) and the G6.2 commit, verify the branch tree was byte-identical to local main (`git diff --stat main <pr-branch>` empty), push, open **PR #23**. Then `git reset --hard origin/main` to undo the local-only merge so main tracked the remote again. The cherry-picks applied with zero conflicts because, off origin/main, the additions were purely additive — the merge-tree conflict had been a 3-way-merge artifact, not a real content collision. Sean squash-merged #23; local main fast-forwarded to `be0ce90`; the merged branch was deleted and pruned. Final state: `main` == `origin/main`, 0/0, 302 tests green, G5 trace still `2138ccd`.

---

## What the diagnostic actually found

The run did its job. On the performs segment (n=44), a single N=1 pass **reproduced the ratified G5 numbers exactly**: precision **0.97** / recall **1.00** / false_pass **0.00**, cites-correct **0.03**, lone FP `clean-c06`. The verdict layer needs nothing. The diagnostic was the citation layer, and it is now de-confounded:

- **`cites-correct = 0.03` splits cleanly by class.** The only `cites_correct = yes` in the whole run is `clean-c06`, and that's a scorer quirk (a flagged case with empty `expected_cites` scores true on any non-empty cite). **Every real defect with a specific expected handle scored NO**, under exact list-membership matching, for three distinct reasons:
  - **proportion** — Em names the right leaf (`head-to-body`) but confabulates the namespace and format (`IR.sean-anchor.…-1-7`) against the real, existing `IR.sean.proportion.head-to-body-1-to-7`. **Matcher-recoverable** — a namespace-insensitive, leaf-normalized matcher recovers these today with no change to Em.
  - **construction / shading** — Em substitutes the manifest QA reason-codes (`HF05` wrong-aesthetic, `SF01` style-drift) and **never** reaches for the `IR.sean.style.*` handle, even though it's in her merged criteria. A **real vocabulary gap** — a prompt-surfacing problem.
  - **view / anatomy** — there is **no IR rule in the Bible to cite at all** (22 rules; zero view, zero anatomy). Em invents structured `IR.sean.view.*` / `IR.sean.anatomy.*-count` handles — which are the exact shapes G6.1 should author. The diagnostic handed G6.1 Em's natural vocabulary on a plate.

- **`clean-c06`** flagged borderline@0.95 on an orientation read ("facing screen-right instead of screen-left") — a view-correctness / facing-convention seam, not a register or identity complaint. The case's own ratification note flags the same convention fragility. Recommendation: **keep it red as a known disagreement** (ships-red discipline — the image violates no ratified rule), and treat it as the canonical test case for the G6.1 view rule. Do not relabel to flatter the metric.

The full per-class table and verbatim reasoning live in the companion field report ([`2026-06-04-em-instrumented-mini-run.md`](2026-06-04-em-instrumented-mini-run.md)) and the trace ([`evals/vision_critic/traces/2026-06-04-instrumented-mini-run.md`](../../evals/vision_critic/traces/2026-06-04-instrumented-mini-run.md)).

---

## The capability we shipped that never fired

Option B — the user's call — made the empty-cites invariant a typed `EmptyCitesInvariant(ValueError)` carrying the parsed payload, so a geometry case that flags a defect but can't ground it gets its reasoning **captured** by the eval worker instead of dying as a blind errored gap. Production behavior is unchanged (it still raises; the subclass is caught only by the diagnostic harness). We built it specifically so Q3 could read Em's geometry reasoning even on the cases that trip.

Then the run produced **0 invariant trips**. At N=1, Em happened to cite *something* on every flagged geometry case, so the capture path never executed live. G5 had 3 trips across 250 case-runs (variance-driven, run-specific); this 50-case pass caught none.

This is worth naming honestly: **we shipped a production-touching change for a diagnostic and the live run never exercised it.** Its only proof of correctness is the unit test (`test_render_per_case_detail` plus the existing invariant tests confirming the subclass still raises and is still caught by `except ValueError`). That's defensible — the change is small, behavior-preserving, correct by construction, and *will* fire at N≥2 or on a different seed — but the unit test is load-bearing in a way it wouldn't be if a live trip had confirmed it end-to-end. The Cy session's mirror-image lesson ("no test could have caught it; only a live run could") applies inverted here: the live run *didn't* cover the new branch, so don't let the green suite imply it did.

---

## What we learned

**Failure analysis up front is cheaper than failure analysis live.** The 19-row flag table is the single highest-leverage artifact of this session. Each critical row (trace clobber, cost leak, `.env`-in-worktree, positional-ctor break) describes a real failure mode that the Cy session would have discovered by hitting it. We discovered them by writing them down. For any costed, irreversible-adjacent run, the flag table earns its keep before the first dollar.

**Prove $0, don't assert it.** The cost-leak class (F2) was already fixed in code with a pinning test. We still proved zero live calls by making a leaked call observable (uniform STUB verdicts) rather than trusting the fix. "The mock is correct" and "this run made no live call" are different claims; only the second one protects the budget.

**Verify remote state before the merge-to-main step, not at the push.** The one genuine failure — the divergent-main collision — was free to detect (`git fetch` + a `rev-list` count) and I detected it one step too late, after a local merge I then had to unwind. The standing doctrine ("verify against the tree, never trust the brief") extends to remote refs and to *when* you verify: before the action the brief frames as routine, because the brief can be wrong about the world. The plan said "merge and push"; the world had a squash-PR workflow and an unpushed predecessor commit.

**A diverged main is a governance decision, not a merge.** When local and origin `main` carry the same content via different commits, the right move is to stop and ask, not to pick a reconciliation unilaterally — especially on a repo with a published PR history. Force-pushing or hand-merging two narratives of the same work is exactly the kind of hard-to-reverse, outward-facing action that warrants a human in the loop. The cherry-pick-onto-origin/main PR was clean precisely because it didn't try to reconcile histories — it re-applied the content as new commits on the canonical base.

**Confirm the artifact captured the thing before deleting the artifact.** The premature smoke-trace deletion cost a redundant call. When the deliverable is "did we capture X," read X out of the artifact (not a `grep` range that can lie about absence) before `rm`.

**N=1 answers questions but doesn't measure distributions.** The diagnostic correctly de-confounded the cites story on one pass, but the same pass showed `clean-c01` flipping pass/borderline/pass across three live touches. Verdict variance is real; every per-case number in the field report is a snapshot. The split verdict/citation re-baseline (G6.1) should run replicated (N≥5), as G5 did.

**The verdict engine is done; the citation engine is the whole G6 question.** This is the organizing finding. Em's verdicts reproduced 0.97/1.00/0.00 at N=1 with no help. The 0.03 is not a verdict problem and not (mostly) mis-reading — it is one part scorer (proportion namespace/format), one part prompt-surfacing (style classes default to QA codes), one part missing rules (geometry has nothing to cite). All three are addressed by G6.1, and the diagnostic specified each precisely enough to build against.

---

## What landed on disk

| Ref | What | Where |
|-----|------|-------|
| Instrumentation diff | `CaseScore.reasoning` (last/defaulted); `_score_one` capture + `consensus_scores` preserve; pure `render_per_case_detail()` (always-on); `--trace-name` redirect; typed `EmptyCitesInvariant(ValueError)` + eval-worker capture (Option B); new render test | `scoring.py`, `score.py`, `vision_critic.py`, `tests/test_em_score_report.py` |
| Dated trace | 50-case per-case cite/`cites_correct`/reasoning table | `evals/vision_critic/traces/2026-06-04-instrumented-mini-run.md` |
| Field report | Q1/Q2/Q3 answered, per-class cite-classification table | `docs/anima-test-runs/2026-06-04-em-instrumented-mini-run.md` |
| CHANGELOG + CLAUDE.md | G6.2 decision-log entry; Critic Stack ¶ + Em row marked mini-run RAN with the finding | `CHANGELOG.md`, `CLAUDE.md` |
| **PR #23** | All of the above + the previously-unpushed G6-kickoff docs, cherry-picked clean onto `origin/main`; squash-merged to `be0ce90` | `github.com/seanwinslow28/anima/pull/23` |

Live spend: ~50 Gemini calls + a handful of Opus escalations for the full run, plus ~5 calls across the two smokes — well under the G5 N=5 run's footprint (this was N=1 on ~50 cases vs N=5 on 250). Ratified G5 baseline trace + `last-run.md` byte-identical (`2138ccd`) start to finish; no baseline moved; no label, prompt, or criterion changed. Tests green (302 contract + 51 eval) on the merged main. Worktree torn down clean, `.env` copy gone with it, 0 orphan processes, merged branch deleted and pruned.

---

## How we should proceed

The G6 dependency chain is now concrete, and the sequencing constraint still holds — G5-comparable diagnostics run **before** anything changes Em's input surface:

1. **References re-test** — the other G5-comparable diagnostic, ungated, on the clean corpus, *before* G6.1 lands. Run it the way this run should be re-run: **replicated (N≥5)**, so the references profile is measured as a distribution, not a snapshot. It's the last read we get at the current input surface.

2. **G6.1 — citation grounding**, informed directly by this run:
   - **Author the geometry IR rules in Em's own vocabulary** — `IR.sean.view.{specific-view}` + a declared-view↔drawn-view check, `IR.sean.anatomy.{finger|hand|limb|leg}-count`. She already reaches for exactly these shapes; give her the handle.
   - **Split the eval's verdict and citation axes**, and have the citation scorer (a) normalize namespace/format so the proportion near-misses score correctly, and (b) credit a correct manifest reason-code (SF03 for proportion, HF03 for direction) as *partial* grounding rather than zero. Half of the 0.03 is recoverable without changing Em at all.
   - This is the change that triggers the next re-baseline — run it replicated.

3. **`clean-c06`** stays red as a known view/facing disagreement and becomes the acceptance test for the new view rule. Do not relabel.

4. **Process changes for the next costed handoff:** add a `git fetch` + `main...origin/main` divergence check to the *pre-flight*, before the merge-to-main step — the divergence this session hit at push time should be a flag-table row next time, not a surprise. And bias the teardown sequence toward "PR off the canonical remote base" rather than "merge to local main then push," given the repo's squash-PR workflow.

The headline for the arc: Em is a trustworthy verdict ruler and an untrustworthy citation ruler, and this run turned "untrustworthy citation ruler" from a mystery into a three-item build list. The boring run was the right kind of boring — the failures were all on paper, and the only live drama was a `git push` that taught us to read the remote before we trust the plan.
