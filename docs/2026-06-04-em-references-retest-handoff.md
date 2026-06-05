# Em References Re-Test — Claude Code Run Brief

*2026-06-04. G6 sequence step 2 (per the locked roadmap: instrumented mini-run ✅ → **references re-test** → G6.1 citation grounding). The 2026-06-02 reference-grounding regression (false_pass 0.00→0.15, recall 1.00→0.85) is now explained as the contaminated fixtures' confabulation trap by construction — "clean" cases literally WERE the reference plates. This run re-asks the question on the trustworthy corpus: does attaching the Bible reference bundle help, hurt, or wash? It is the last G5-comparable read before G6.1 changes Em's input surface, which is why it runs NOW and ungated.*

**Standing doctrine: verify against the tree, never trust a label — including this brief.**

**This is a diagnostic-with-teeth, not a flag flip.** The repo default `critics.t2.attach_references: false` does NOT change in this run regardless of outcome. The flip is a separate, Sean-gated decision against the criteria in §Decision rules.

---

## Pre-flight (every row must pass before the first costed call)

Process rows are the 2026-06-04 postmortem's lessons, promoted from surprises to checks:

1. **Remote divergence check FIRST:** `git fetch && git rev-list --left-right --count main...origin/main` must be `0 0` before branching, and again before teardown. The repo workflow is **squash PRs off origin/main** — plan the landing as a PR, not a local merge-to-main.
2. Isolated worktree per fleet-ops (`docs/fleet-ops-protocol.md`); **copy `.env` into the worktree** (gitignored files don't follow `git worktree add`); grep it carries `GEMINI_API_KEY` and NOT `ANTHROPIC_API_KEY`.
3. Guards green in the worktree: `python -m pytest tests/ -q` (includes contamination guard) and `python -m pytest evals/vision_critic/runner.py -q`.
4. **Trace-clobber guard:** run the scorer with `--trace-name references-retest-2026-06-DD`. Record the SHA-256 of `evals/vision_critic/traces/baseline-2026-06-04-scored.md`, `traces/2026-06-04-instrumented-mini-run.md`, and `last-run.md` at pre-flight; re-verify byte-identical at every checkpoint and at teardown. If the scorer would touch `last-run.md`, redirect or stash-restore — the ratified artifacts move for no one.
5. **Prove $0 before live:** `--stub` pass shows the uniform STUB signature on every case (borderline@0.78, 0s wall). A leaked real call cannot produce that signature.
6. **References mechanism — pre-work required, verified 2026-06-04:** score.py has **no scoped enable today** — it reads `critics.t2.attach_references` from the manifest only (line ~464: `manifest.get("critics",{}).get("t2",{}).get("attach_references", False)`) and exposes no `--attach-references` or `--manifest` CLI arg (full arg surface: stub/model/only/segment/motion-smoke/limit/runs/allow-api-key/trace-name). **Pre-work (uncosted, mocked):** add a run-scoped `--attach-references` override to score.py that wins over the manifest read, plus a mocked test proving (a) the flag engages the references path and (b) the default invocation stays blind. Never enable by committing a manifest change. Then verify in the smoke trace that references actually attached (reference paths/count visible in the run record — when off, the trace prints `blind (attach_references off)`; the on-arm must show the bundle) — an arm that silently ran blind would "reproduce the baseline" and lie.
7. **Smoke then pause:** `--limit 2` live; confirm (a) served model `gemini-3.5-flash` read back from `resp.model_version`, (b) references attached, (c) reasoning prose captured in the trace — READ it in the artifact before deleting anything. Then proceed to the full run.

## The run

```bash
python -m evals.vision_critic.score --runs 5 --trace-name references-retest-2026-06-DD   # references ON (scoped)
```

- **N=5 full replications, majority vote** (3-of-5; conservative tie-break fail > borderline > pass), per-run table + false-pass band preserved. The 2026-06-02 lesson stands: a references read at N=1 is a snapshot; the regression we're testing for was variance-flavored.
- Config otherwise **identical to the ratified G5 baseline**: pinned `gemini-3.5-flash` via `gemini_api` transport, Opus 4.7 escalation rules unchanged, same 50 cases (the two pending re-roll slots stay excluded), prompt/criteria/labels untouched.
- Reference bundle as shipped: `select_references` (view-aware B1a path — subject image 1, anchor + deduped turnarounds). Do not hand-pick references; we're testing the production path.
- **Control = the ratified G5 blind baseline** (same corpus, same pinned model, same scorer). Do not re-burn 250 blind calls. **Skip the optional blind sanity arm:** the 2026-06-04 instrumented mini-run already served as the N=1 blind reproduction (0.97/1.00/0.00, same day, same config) — burning ~50 more calls on it buys nothing.
- **Bundle provenance (why this re-test is a different experiment than 2026-06-02):** the references attached this time are the **re-locked 1:7 region crops** (plus the net-new `body-front`), not the drifted ~1:4–1:5.3 plates the regression run saw; and `tests/test_fixture_contamination.py` now guarantees fixtures ≠ references by SHA and inode. Both structural causes of the confabulation trap are gone — say so in the field report's side-by-side.
- **Expect sporadic empty-cites invariant trips on geometry cases** (G5 blind: 3/250, all majority-recovered). Subprocess isolation lands them as honest gaps; record errored case-runs in the trace for both comparison axes — a references-driven change in trip *rate* is itself a finding.
- Cost: ~250 calls references-on (+~50 optional blind sanity + smokes) — same envelope as G5 (~$3–13). Zero-429 expected on the API transport; partial-N is not a result.

## What to read out of it (in priority order)

1. **Safety axes vs blind baseline (majority vote):** false_pass (blind: 0.00) and recall (blind: 1.00). Any false-pass regression is the old disease — capture the confabulation evidence verbatim (does Em recite the reference register onto a defect subject?). This is the gate metric.
2. **Precision / the clean set:** blind FP is exactly one (`clean-c06`, an orientation read). Watch it specifically — references include turnarounds with declared facing; they may FIX c06 (the known headroom 0.97→1.00) or spread doubt onto other cleans (the regression shape). Per-clean-case verdicts, all 16.
3. **Citations (secondary, now instrumented for free):** does seeing references move Em's cite vocabulary toward `IR.sean.*` handles, or amplify confabulated namespaces? Feeds G6.1; doesn't gate this run.
4. **Variance:** flip count + false-pass band vs G5's (performs band 0.00–0.04). References that widen the band are a cost even at equal point estimates.
5. **Geometry classes:** do references change proportion/view/anatomy detection or grounding? (Layer-ownership says Bible-lock owns these in production — this is informational for SF03/G6.1.)

## Decision rules (proposed to Sean, not self-executing)

- **Flip-eligible** only if, at N=5 majority: false_pass = 0.00 AND recall = 1.00 AND precision ≥ 0.97 AND the per-run false-pass band is no wider than blind's (worst run ≤ 0.04).
- **Wash** (same numbers, no c06 fix): flag stays off — references add tokens/latency for nothing on this distribution; note for re-test after G6.1.
- **Any false-pass regression:** flag stays off, regression is now *confirmed real* (not fixture-borne) — record it as the definitive answer and stop relitigating references until Em's input surface changes (G6.1) or DINOv2-class grounding exists.
- Whatever the outcome: **Sean ratifies** before any CLAUDE.md/flag change. `clean-c06` is not relabeled regardless (ships-red; it's the G6.1 view-rule acceptance case).

## Deliverables

1. Dated trace `evals/vision_critic/traces/references-retest-2026-06-DD.md` (per-case verdicts, cites, reasoning, reference attachment record).
2. Field report `docs/anima-test-runs/2026-06-DD-em-references-retest-field-report.md` — side-by-side vs the G5 blind baseline, the five reads above, and the flip recommendation against the decision rules.
3. CHANGELOG entry. CLAUDE.md Em-row update only after Sean ratifies.
4. Land via **PR off origin/main** (cherry-pick if needed), divergence check before and after, worktree torn down clean, ratified traces byte-identical, tests green on merged main.

## Hard lines

- No baseline moves. No label, prompt, or criterion edits. No default-flag flips. No force-push; a diverged main is a stop-and-ask, not a merge.
- Ships-red discipline: nothing gets tuned to flatter Em — in either arm.
