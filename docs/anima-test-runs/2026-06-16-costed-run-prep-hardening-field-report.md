# Field Report — Pre-costed-run hardening: Sam/Bea raw-dumps + gate smokes ($0 stub-green, TDD)

**Date:** 2026-06-16
**Kickoff:** [`docs/2026-06-16-costed-run-prep-kickoff.md`](../COMPLETED/orchestrator/2026-06-16-costed-run-prep-kickoff.md)
**Precedes:** [`docs/2026-06-16-spark-authored-costed-run-runbook.md`](../COMPLETED/orchestrator/2026-06-16-spark-authored-costed-run-runbook.md) (the first live authoring run — human-driven by Sean, **not** this session)
**Spend:** $0 (stub-green throughout; no model call — smokes asserted *invoked* via a mock, dumps write whatever the call returned)
**Branch / PR:** `costed-run-prep-hardening` off `origin/main` `98aeed8` (#55) → [PR #56](https://github.com/seanwinslow28/anima/pull/56); two TDD commits, each revertible alone

---

## What this was

Two small, independent hardening changes to the run orchestrator that must land **before** the first **live** Sam/Bea authoring run, so that run is **inspectable** and **fails before it spends**:

- **Change A — raw-dumps (visibility).** Maya dumps her raw Opus envelope to `run_dir/maya_raw_pass1.txt`; Sam and Bea did not, so a live run left only the *parsed* artifacts — not the raw model envelope. Both now call `planner._dump_raw` (best-effort, never raises) on the response **before** parsing: Sam → `run_dir/sam_raw.txt`, Bea → `run_dir/bea_raw.txt`.
- **Change B — gate smokes (fail before spend).** `run_plan_stage` smokes Opus live *before* Maya runs; the script + storyboard gates did not — they only caught a silently-stubbed call *after* it returned (the post-hoc stub-marker scan). Added the matching pre-authoring smoke to the top of each stage: `run_script_stage` → `guards.smoke_live_opus()`, `run_storyboard_stage` → `guards.smoke_live_sonnet()`.

No live model spend — the whole change is exercised stub-side. Not a costed run; the post-mortem below is about *build-time* verification and one design fork, not generation quality.

The slice landed exactly as scoped. **8 new tests (647 → 655); zero regressions; `pipeline/tests/` green.**

---

## Verification against the tree (the part worth reading)

Unlike the Bea build — where the doctrine's "verify against the tree, never trust a label, *including this kickoff*" overturned the single load-bearing semantic — this kickoff held up under verification. That itself is worth recording: the discipline is the same whether or not it finds an error, and the value of running it is that you *know* the kickoff is right rather than hoping. Two parallel Explore sweeps confirmed every claim before a line was edited.

### What the kickoff got right (all confirmed)

- `planner._dump_raw(run_dir, name, text)` exists at [`planner.py:488`](../../pipeline/agents/planner.py), is best-effort (try/except), and never raises — Maya calls it `_dump_raw(ctx.run_dir, "maya_raw_pass1.txt", opus_resp.text)`. Mirrored exactly.
- `scriptwriter.py` already imports `_parse_json_envelope` from `planner`, so adding `_dump_raw` to that import is a one-token change; `storyboard_artist.py` likewise.
- `guards.smoke_live_opus` / `guards.smoke_live_sonnet` / `guards.GuardError` all exist; `run_plan_stage`'s smoke shape is exactly `if not (stub or skip_smoke): try: guards.smoke_live_opus() except guards.GuardError as e: print(...); return 1`.
- `run_script_stage` / `run_storyboard_stage` both take `stub: bool` as a parameter and have **no** pre-run smoke yet — only the post-hoc `scan_stub_marker`. Exactly the gap the kickoff described.

### #1 — The one nuance: dumps go to `run_dir`, but the agents' *artifacts* go to `brief_dir`

The kickoff says "the agents write to `ctx.run_dir` (so the dump lands beside `maya_raw_pass1.txt`)." Verifying the actual node bodies showed a subtlety: Sam and Bea write their **parsed artifacts** (`script.md`, `beats.json`, `storyboard.md`, `shots.yaml`) to `brief_dir` (`ctx.inputs["brief_dir"]`), **not** `ctx.run_dir` — only Maya writes to `run_dir`. `ctx.run_dir` is present on the context but was previously **unused** in both nodes.

This is *not* a conflict — it's the right design, and the kickoff's literal `_dump_raw(ctx.run_dir, "sam_raw.txt", resp.text)` call is correct. The raw dumps belong in `run_dir` (per-run debugging evidence, all three raw envelopes together) while the parsed artifacts belong in the brief snapshot (`brief_dir`, which under the orchestrator is itself a copy under `run_dir/brief/`). Recording it because a careless reading of "the agents write to run_dir" could have led someone to relocate the *artifacts*, which would break the gate that reads them from `brief_dir`. The seam was confirmed by reading both node bodies before editing.

### #2 — The genuine design fork: `skip_smoke` persistence (the kickoff's optional polish)

The kickoff offered an optional "fidelity" polish: persist `skip_smoke` in `new_state` at `_start` and gate the new smokes `not (stub or state.get("skip_smoke"))`, matching `run_plan_stage` exactly. Verification confirmed the asymmetry that makes this a real choice: `skip_smoke` is **CLI-only** — read from `args.skip_smoke` at `_start` and **never persisted** to `run_state.json` ([`state.py:38`](../../pipeline/orchestration/state.py)). The plan gate runs at `_start` where `args.skip_smoke` is live; the script/storyboard gates run during `--resume`, where it is not. So honoring `--skip-smoke` at the two new gates requires extra plumbing (persist it, or thread it through the resume handlers).

**Resolution (surfaced to Sean before finalizing the plan):** gate on `stub` only (`if not stub:`). The costed run *wants* smokes ON — that is the whole point of fail-before-spend — and developers iterating offline use `--stub`, which already short-circuits both gates. `--skip-smoke` at the script/storyboard gates would be near-zero use bought with a `state.py` schema touch. Took the smallest revertible change; the asymmetry with `run_plan_stage` is a known, documented, intentional gap (one line in the CHANGELOG decision note), not an oversight.

---

## What we got right (and why it held)

- **TDD red→green, two independent commits.** Each change was proven failing first (Change A: `sam_raw.txt` / `bea_raw.txt` absent; Change B: the 4 non-stub smoke tests red, the 2 stub tests trivially green because the smoke wasn't wired yet — a clean signal that the gate, not the test, was the variable). Each commit reverts alone.
- **The smoke tests isolate the gate, not the node.** Rather than drive the full orchestrator (which would entangle `ANIMA_FORCE_STUB`, the stub-marker scan, and downstream stages), the six smoke tests stub the agent node to a marker-free no-op and monkeypatch `guards.smoke_live_*`. That makes the three behaviors per stage provable in isolation: smoke fires before authoring (the no-op records it ran second), `--stub` never smokes, and a `GuardError` returns non-zero with the node-run recorder *empty* — the literal "fail before spend" assertion.
- **Mirrored the existing pattern exactly.** Both the dump call (before parse, best-effort) and the smoke block (`if not stub: try/except GuardError → print + return 1`) are byte-for-byte the shapes already in `planner.py` and `plan_stage.py`. No new idiom invented; a future reader sees one pattern in four places.
- **The two standing guards never moved.** Em verdict-baseline `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` md5 `2af75906502f1caf8857e18828ceb2e4` and Sam's voice file `sean-screenwriting-voice.md` md5 `945af824fa53b948a18ac6bf206d67ef` were captured at §0 and re-checked after both commits — byte-identical. Nothing under `evals/vision_critic/` was touched; the diff is 8 files, all of them named in the plan.

---

## What we learned

1. **A verification pass that finds nothing is still worth running.** The Bea build's lesson was "the plausible plan error is the dangerous one." This build's lesson is the complement: the same cheap `grep`/`Read` that *would* have caught an inverted rule is what lets you ship with confidence when the kickoff is actually right. The discipline isn't conditional on finding a bug — it's how you earn the right to say "the kickoff is accurate."
2. **"Write to run_dir" and "the artifacts live in run_dir" are different claims.** The one nuance (#1) was a place where a true statement about the *dump* could be misread as a statement about the *artifacts*. Reading the node body, not the prose summary, kept the dump in the right place without disturbing where the gate reads its inputs.
3. **An intentional asymmetry, documented, beats an undocumented symmetry.** Declining the `skip_smoke` polish (#2) leaves the three gates slightly inconsistent — but the inconsistency is one line of CHANGELOG away from obvious, and the alternative spent a schema touch on a path the costed run will never take. Name the gap; don't paper it.
4. **Stub-side tests can still prove a spend-gating property.** "Fail before spend" sounds like it needs a live call to test. It doesn't: monkeypatch the smoke to raise, record whether the node ran, assert the recorder is empty. The property is about *ordering and control flow*, which is fully observable at $0.

---

## How to proceed

1. **The live authoring run is now unblocked — and is Sean's to drive.** With raw-dumps and gate smokes in place, the first costed Sam/Bea run ([runbook](../COMPLETED/orchestrator/2026-06-16-spark-authored-costed-run-runbook.md)) will fail fast on a broken auth (before any spend) and leave `sam_raw.txt` / `bea_raw.txt` on disk for inspection if the envelope parser trips. Run it from a plain terminal (the nested-SDK throttle), subscription billing, per the fleet-ops protocol. **This session does not launch it.**
2. **The raw dumps are the diagnostic for the run's first real failure mode.** The first integrated run (2026-06-11) broke on Opus's persona preamble; Maya's raw dump is what diagnosed it. Sam/Bea now have the same safety net. If the live run's structural pass or curation gate rejects, read the raw envelope first — it is the ground truth the parser saw.
3. **`skip_smoke` symmetry is a parked, low-priority follow-on, not a debt.** If a future workflow genuinely needs `--skip-smoke` to apply at the script/storyboard gates (e.g. an offline-but-non-stub dev path), persist it in `new_state` and gate `not (stub or state.get("skip_smoke"))` — the one-line change the kickoff described. Until such a consumer exists, the gap is correct.

---

## Done criteria — checked

- [x] `python -m pytest tests/test_scriptwriter.py tests/test_storyboard_artist.py tests/test_run_storyboard_wiring.py` green, credential-free.
- [x] `python -m pytest tests/` → **655 passed** (647 + 8), no regressions; `pipeline/tests/` → 10 passed.
- [x] A stub authoring walk leaves non-empty `run_dir/sam_raw.txt` + `run_dir/bea_raw.txt` (proven by test).
- [x] The script gate smokes Opus and the storyboard gate smokes Sonnet on the non-stub path; neither smokes under `--stub`; a `GuardError` returns non-zero before the authoring node runs (all proven by test with a mocked smoke — no real call).
- [x] `ANTHROPIC_API_KEY` ABSENT throughout; suite green credential-free.
- [x] Em baseline md5 `2af75906502f1caf8857e18828ceb2e4` unchanged; nothing under `evals/vision_critic/` touched.
- [x] `sean-screenwriting-voice.md` md5 `945af824fa53b948a18ac6bf206d67ef` unchanged from §0.
- [x] CHANGELOG.md updated. Two TDD commits, each revertible alone; one squash PR (#56) off the isolated worktree; clean teardown to follow merge.
