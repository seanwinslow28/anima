# Field Report — Bea the Storyboard Artist (Phase 3b): the fleet's last named agent ($0 stub-green, TDD)

**Date:** 2026-06-15
**Kickoff:** [`docs/2026-06-15-bea-storyboard-kickoff.md`](../2026-06-15-bea-storyboard-kickoff.md)
**Plan of record:** [`docs/2026-06-15-bea-storyboard-build-plan.md`](../2026-06-15-bea-storyboard-build-plan.md)
**Build input:** [`docs/2026-06-15-bea-action-line-bank-context.md`](../2026-06-15-bea-action-line-bank-context.md)
**Spend:** $0 (stub-green throughout; the real Sonnet path is written + guarded, never invoked in CI or this session)
**Branch / PR:** `bea-storyboard-artist` off `origin/main` `807cf99` (#53) → [PR #54](https://github.com/seanwinslow28/anima/pull/54); six TDD commits, each revertible alone

---

## What this was

A standalone build of **Bea**, the Phase-3b storyboard artist and the **ninth and last named agent** in the fleet. She reads Sam's approved `beats.json` + the Studio Brief and *proposes* a studio-voice `storyboard.md` + a **draft `shots.yaml`** (born unlocked); Sean curates and locks it at the `storyboard approve` gate. No live model spend — the headline deliverable is the whole contract layer + CLI + driver + eval proving end-to-end with **no key**, via the stub fallback. Not a costed run; the post-mortem below is about *build-time* failures and corrections, not generation quality.

The slice landed exactly as scoped: two back-compat `shots.yaml` schema additions (`beat_id`, `locked`), the `storyboard_artist` node + stub + deterministic validation, the persona context (shared voice file + the vendored action-line bank), `invoke_sonnet_text`'s `stub_fn=` extension, the `storyboard` CLI + `author_storyboard.py` driver, the `evals/storyboard_artist/` scaffold, and docs. **31 new contract tests (605 → 636) + 4 eval cases; zero regressions.**

---

## Failures & corrections (the part worth reading)

There were no runtime failures — but the doctrine's "verify against the tree, never trust a label, *including this kickoff and the plan*" earned its keep four times. Each is recorded because that's why the doctrine exists.

### #1 — The kickoff's cast-consistency rule was backwards, and the real Spark board proves it

The kickoff and build plan both specified the script↔board conflict check as **`shot.cast ⊆ beat.cast`** ("a shot can't introduce a character the beat didn't carry"). Verifying against the real committed corpus before writing the validator killed that rule: the shipped Spark `beats.json` carries **beat 3 ("The notice") with `cast: [claude-mascot]` only**, while the shipped Spark `shots.yaml` **frame 3 boards both `sean` and the mascot** — because it's a fixed-camera two-shot and both are always in frame. Under the literal kickoff rule, `storyboard_validate` would flag the *shipped, hand-authored, correct* board as a conflict. Worse, the user's chosen "strict gate + annotated Spark fixture" path would have been **unbuildable** — no annotated Spark board could ever pass.

**Resolution:** inverted the rule to **`beat.cast ⊆ shot.cast`** — every character a beat is *about* must appear in its boarded shot; the board may *add* others in frame, but may never *drop* a scripted one. This is the defensible direction (it catches "the board forgot the character the beat is about," a real error) and it passes the real Spark board. The decision was surfaced to the user before finalizing the plan, documented in the node docstring, the CHANGELOG, the CLAUDE.md row, and the eval README, and is proven by the positive eval case (beat 3 mascot-only, shot 3 boards both, green).

**Why it matters:** this is the single load-bearing semantic choice in the slice, and the source document had it exactly inverted. A build that "followed the plan" faithfully would have shipped a validator that rejects correct boards and accepts the one real error class it was meant to catch.

### #2 — The Explore agents mischaracterized three seams; the tree was right, they weren't

Parallel Explore agents scouted the seams up front. Three of their conclusions were wrong and would have produced a subtly broken Bea if trusted:

- **"Bea reuses `invoke_opus_text`."** One agent's cloning checklist had Bea calling the Opus runner. Bea is a **Sonnet 4.6** agent (the roster's lowest-confidence assignment); she uses `invoke_sonnet_text`, which needed the `stub_fn=` param added (the Opus one already had it). Followed the docs, not the agent.
- **"`beat_id` is already in `_FRAME_KEYS` — no change needed."** The same agent's summary self-contradicted its own quoted `_FRAME_KEYS`, which did **not** contain `beat_id`. Both fields were genuinely new.
- **Output shape + file names.** An agent proposed outputs `{shots_path}` only and names `bea_storyboard_artist.py` / `bea-storyboard-artist-context.md`. The authoritative shape is **two** outputs (`{storyboard_path, shots_path}`) and the role-named `storyboard_artist.py` / `bea-storyboard-context.md` (matching `scriptwriter.py`).

**Resolution:** two direct `Bash`/`Read` verifications of the actual `sdk_runners.py` and `shots.py` source settled all three before any code was written. **Lesson re-confirmed:** Explore output is a lead, not a fact; the cheap targeted `grep`/`Read` that confirms a seam is non-negotiable, even (especially) when three agents agree.

### #3 — The positive eval fixture can't be the shipped Spark file (and that's correct)

The plan said "positive ground truth: the Spark `beats.json` → expected Spark `shots.yaml`." But the shipped Spark `shots.yaml` carries **no `beat_id`s**, so it can't pass the coverage gate — and `test_spark_shots_equivalence.py` pins that file byte-identical, so it can't be edited. The two constraints look contradictory.

**Resolution:** the positive fixture is a **beat_id-annotated derivative** of the shipped board (`evals/storyboard_artist/fixtures/spark-shared-expected-shots.yaml`, generated from the real file by adding the 1:1 `beat_id` link), *not* the shipped file. This is exactly why `load_shots` stays lenient (`beat_id` optional, the shipped file unaffected) while strictness concentrates in `storyboard_validate` (Bea's emit + the approve gate). The back-compat tests stay green and meaningful; the eval proves the new contract. This tension was the one genuine design fork put to the user (answered: "strict gate, annotated fixture").

### #4 — A self-introduced test-count error in the CHANGELOG, caught by running the suite

While writing docs I wrote "36 new tests (605 → 641)" in the CHANGELOG before the final suite run. The actual contract suite is **636** (605 + 31 new in `tests/`); the other 4 are eval cases that run via the named `runner.py`, not `tests/`. Running the suite (the verification-before-completion step) surfaced the discrepancy and it was corrected to "31 new contract tests (605 → 636) + 4 eval cases" before commit.

**Lesson:** counts asserted from memory are wrong as often as not; the only trustworthy number is the one the test runner just printed. Evidence before assertions — including in the decision log.

### #5 — Cosmetic: `yaml.safe_dump` escaped the em-dashes

The first end-to-end stub run emitted `shots.yaml` with `—` escapes (default `allow_unicode=False`) — not a box-drawing char, so it passed the acceptance bar, but ugly for a human-curated file. Added `allow_unicode=True` to the node's and the CLI mutate's dumps so em-dashes render literally. Minor, but a human-authored artifact should read like one.

---

## What we got right (and why it held)

- **TDD with small revertible commits.** Six commits, each red→green, each with its own targeted suite run before the full suite. The schema-first ordering (additions + back-compat proof before any agent code) meant the load-bearing back-compat guarantee was locked before anything depended on it.
- **The stub is a closure over the real beat sheet**, not a fixed 5-frame blob like Sam's. `_make_bea_stub(sheet)` emits one shot per beat, so coverage/orphan/conflict pass *by construction* for ANY `beats.json` — the credential-free path proves the whole contract on the real Spark brief and on arbitrary input, not just a hand-tuned fixture.
- **Bea's failure modes are deterministic, so her ships-red cases are green catches** — not `xfail` like Sam's by-ear voice defects. `beat_id` is what makes the beat↔shot link checkable; that single field turns "shot-coverage gap" and "script↔board conflict" from LLM-judge territory into free deterministic gates. This is the structural analogue of Sam's cast-coverage gate.
- **The two standing guards never moved.** Em verdict-baseline `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` md5 `2af75906502f1caf8857e18828ceb2e4` and Sam's voice file `sean-screenwriting-voice.md` md5 `945af824fa53b948a18ac6bf206d67ef` were captured at §0 and re-checked at the end — both byte-identical. The action-line bank went into Bea's own context file, never the shared voice file.

---

## What we learned

1. **The plan is a hypothesis; the tree is the truth — and the most dangerous plan errors are the *plausible* ones.** The cast-rule inversion (#1) read perfectly sensibly on the page ("a shot shouldn't add characters"). It was only wrong against real data. A faithful build would have shipped it.
2. **Parallel scouts converging on a wrong answer is not corroboration.** Three Explore agents, three mischaracterizations (#2). The targeted re-verify is cheap; skipping it because "the agents agreed" is the trap.
3. **A deterministic link field is worth more than a clever judge.** Adding one optional `beat_id` to the schema is what lets Bea's whole conflict/coverage story be free and deterministic — and lets her ships-red eval be green, not deferred. When a failure mode *can* be made checkable with a cheap structural primitive, do that instead of reaching for an LLM gate.
4. **Counts and claims are not free.** Both the source plan (#1, #3) and my own draft (#4) carried assertions that the corpus / the test runner contradicted. The discipline that catches these is the same one: don't assert what you can run.

---

## How to proceed

1. **The orchestrator-wiring slice (the deliberate third slice) is now unblocked.** Wire a `STORYBOARD` stage into `pipeline/run.py` between `PLAN` and `GENERATE` that runs Sam → Bea, exits at a `--approve-storyboard` human-curation gate, and **enforces the `shots.yaml` `locked` flag** before `GENERATE` will consume the board. The schema (`locked`) and the gate (`storyboard approve`) already exist standalone; the slice makes the loop one resumable program and is the moment the orchestrator stops needing a hand-written `shots.yaml`. Plan it in Cowork after #54 merges.
2. **Prove `beat_id` against a *real Bea draft* before wiring.** The positive eval rides a beat_id-annotated *derivative* of the shipped board, and the stub emits one-shot-per-beat. Neither is a real Sonnet board. The first costed Bea run (deferred, with the bake-off) should author a real `shots.yaml` from the Spark `beats.json` and confirm the beat_id-linked board survives `storyboard approve` → `python -m pipeline.run` end to end. Until then, the beat_id contract is proven structurally, not against model output.
3. **The deferred campaign items are real, not hand-waves.** Two stay parked: (a) the **composition pairwise-preference harness** — whether a board *reads well* is a by-ear call the eval handbook bars an LLM judge from making; it's Bea's equivalent of Sam's deferred voice harness. (b) The **Sonnet/Gemini/Codex bake-off** — Bea's Sonnet assignment is the roster's lowest-confidence pick (≈65%); the three-way shoot-out is the hardening campaign, not a v1 blocker.
4. **The fleet's named roster is complete; stop adding agents.** Every node of `Maya → Sam → Bea → shots.yaml → Flo/orchestrator → Em/T3 → Mo` has an agent, and the human still owns the only nodes that matter (`script approve`, `storyboard approve`, the ship call). The remaining work is *wiring and hardening*, not new personas.

---

## Done criteria — checked

- [x] `python -m pytest tests/test_shots.py tests/test_storyboard_artist.py tests/test_storyboard_cli.py` green, credential-free.
- [x] `python -m pytest tests/` → **636 passed** (605 + 31), no regressions; `test_run_shots.py` + `test_spark_shots_equivalence.py` green (back-compat proof). `pipeline/tests/` 10 passed.
- [x] `storyboard init/show/approve` works against a brief with a `beats.json`; a stub draft `shots.yaml` round-trips `load_shots` + passes `storyboard_validate` — proven live end-to-end in stub mode (driver emits → stub-marker guard refuses; show renders; approve validates coverage+conflict and locks).
- [x] Coverage gate catches a beat-with-no-shot AND cast-consistency catches a script↔board conflict — both proven by test (and by the 3 green ships-red eval cases).
- [x] `invoke_sonnet_text`'s `stub_fn=` is backward-compatible (planner tests green).
- [x] Em baseline md5 `2af75906502f1caf8857e18828ceb2e4` unchanged; nothing under `evals/vision_critic/` touched.
- [x] `sean-screenwriting-voice.md` md5 `945af824fa53b948a18ac6bf206d67ef` unchanged from §0.
- [x] CHANGELOG.md + CLAUDE.md updated (incl. the fleet-roster-complete note). One squash PR (#54) off the isolated worktree; clean teardown to follow merge.
