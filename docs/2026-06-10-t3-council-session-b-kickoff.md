# Kickoff — T3 Council, Session B: config + pre_museum gate + live-validate (commit 9B)

*Paste-ready brief for a **Claude Code** session. Mostly $0 (subscription-absorbed Opus/Codex) **plus a bounded `GEMINI_API_KEY` cost** for Annie's live calls in the smoke run (~$1–2, like Em's capture). Session A shipped the engine ([PR #41](https://github.com/seanwinslow/anima/pull/41)); Session B makes T3 **real and proven**: the `critics.t3:` config block, the `pre_museum` gate wired into the museum build, Codie verified **live** for the first time, a live council smoke on the committed museum, and the state-of-record flip to "built." Plan of record: [`docs/2026-06-10-t3-council-build-plan.md`](2026-06-10-t3-council-build-plan.md). Scope locked (Sean, 2026-06-10): build + wire + live-validate; **ticket** the Sage bake-off + the agy cleanup.*

**Standing doctrine: verify against the tree — and the real binaries — never the label.** Session A's smoke test already caught the `cli_runners.py` A2 docstring lying about `agy -m`. Session B has its own version: **Codie's Codex transport was built stub-only** (codex wasn't installed during A). Do not trust the documented `codex exec` shape — verify it against the installed binary before the live smoke depends on it.

## ⚠ FIRST — sync, then guard
Session A's #41 is merged on GitHub but **local `main` was behind** at last check. Sync before anything:
1. `git fetch origin && git checkout main && git pull` → local `main` should now carry the #41 squash commit (T3 council Session A).
2. `git worktree remove .claude/worktrees/feature+t3-council-session-a` (it's merged + prunable) and `git worktree prune`.
3. `git rev-list --left-right --count main...origin/main` → expect `0 0`.
4. `git log --oneline -3` — confirm the #41 T3-council commit is at/near HEAD.
5. `git status -s` → clean. Branch a fresh isolated worktree `feature/t3-council-session-b` off `origin/main`.
6. **Verdict-baseline guard:** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` → **`2af75906502f1caf8857e18828ceb2e4`**, byte-identical through ALL of Session B. T3 stays additive — never touch `evals/vision_critic/`.

## Pre-req (Sean does this before the session) — install Codex so Codie runs LIVE
The smoke found `codex` absent, so Session A's `run_codex_with_image` is stub-verified only. For the live smoke to exercise three real vendors (not two), the Codex CLI must be installed + authed:
- Install the OpenAI Codex CLI (`npm i -g @openai/codex` or `brew install codex`), `codex login` (ChatGPT Plus), confirm `which codex` + `codex --version`.
- If Codex still isn't available at session time, Codie falls back to its stub and the live smoke is **two-vendor** — record that honestly and ticket the Codie-live verification rather than fake it.

## Read, in order
1. [`docs/2026-06-10-t3-council-build-plan.md`](2026-06-10-t3-council-build-plan.md) — the approved plan (Steps 3–4 are this session).
2. [`pipeline/agents/t3_council.py`](../pipeline/agents/t3_council.py) — the Session A engine you're wiring. Note: `inputs` = `artifact_paths` / `beat_description` / `frame_id` / `checkpoint` / `gate`; `outputs` = `verdict` / `agreement_score` / `chairman_note` / `peer_verdicts` / `status`; it already reads `ctx.manifest["critics"]["t3"]` for `per_call_timeout_s`; videos auto-reduce to a contact sheet.
3. [`docs/research/2026-06-10-t3-cli-multimodal-smoke.md`](research/2026-06-10-t3-cli-multimodal-smoke.md) — **Annie's transport is settled (Gemini API, not `agy`)**; the documented `codex exec` shape to verify; the dormant `agy -m` latent bug (ticket, do not fix here).
4. [`manifest.yaml`](../manifest.yaml) `critics:` — the `placement` already declares `pre_museum_publish: T3`; the `critics.t2:` block is the **template** for the `critics.t3:` block you add (shape: models/transport, `auto_apply: false`, `per_call_timeout_s`, `wall_budget_s`, `default_context_files`).
5. [`scripts/build_museum.py`](../scripts/build_museum.py) — the museum builder. The publish step is `--render --site`; the `pre_museum` gate hooks **before render**, after exhibits are assembled (+ optionally `--narrate`d). Mirror the existing `--narrate`/`--render` flag pattern.
6. [`docs/museum-exhibit-schema.md`](museum-exhibit-schema.md) — exhibit layout (`exhibit.json` + `exhibit.md` + `assets/` thumbnails). The council reads an exhibit's `assets/*.png` as `artifact_paths`; the exhibit prose + `acceptance_criteria` fold into the context (`beat_description`).
7. [`docs/fleet-ops-protocol.md`](fleet-ops-protocol.md) — the live smoke spends a bounded Gemini cost; honor §0-before-spend.

## STEP 1 — `critics.t3:` config block ($0)
Add `critics.t3:` to `manifest.yaml`, mirroring `critics.t2:`:
- `peers:` — `codie` (transport `codex`), `annie` (transport `gemini_api`, model pinned like Em — `gemini-3.5-flash`), `sage` (transport `opus_vision`, Opus). Per the smoke, **Annie is `gemini_api`, NOT `agy`.**
- `chairman:` Opus (text synthesis, `invoke_opus_text`).
- `auto_apply: false` (v2 lock), `per_call_timeout_s: 120`, `wall_budget_s: 600`, `default_context_files:` (PHILOSOPHY.md, CLAUDE.md, the architecture doc).
- Keep it cosmetic-honest (the t2 block's A3 lesson): the slug must match what actually serves.

## STEP 2 — verify Codie LIVE, finalize `run_codex_with_image` ($0, subscription)
The deferred Step-0-for-Codie, now that Codex is installed.
- Run `codex exec` with an image reference (per the smoke doc's documented shape: `codex exec --sandbox read-only --skip-git-repo-check`, from `~`); confirm whether image input is via a path-in-prompt or a `-i/--image <file>` flag. Capture the verbatim invocation + output.
- Reconcile `run_codex_with_image`'s live path against what the binary actually does; adjust if the stub-built shape was wrong. **Re-run `tests/test_cli_runners.py` green** (stub path must stay CI-green for credential-free machines).
- Append the live findings to the smoke doc (or a dated trace) — "verify the binary" evidence, portfolio-grade.

## STEP 3 — wire the `pre_museum` gate into the museum build ($0, stub-green)
- Add a gate step to `scripts/build_museum.py` that runs `T3CouncilNode` on the assembled exhibits **before `--render`** (gate the publish, not the scrape). Suggested `--t3-gate` flag; when set, after exhibits are built/narrated, instantiate the council per exhibit (or a representative sample), `artifact_paths` = the exhibit's `assets/*.png`, context = exhibit prose + `acceptance_criteria`.
- **Gate semantics:** a chairman `fail` (or all-peers-errored) **blocks `--render`** and surfaces the adjudication + staged patches; `borderline` surfaces but is a human call; `pass` proceeds. Patches stage via the existing `stage_patches_hook` (`auto_apply: false`) — never auto-apply.
- The council is gate-agnostic, so this is wiring + input-prep, not engine changes. **Do not touch `post_animatic`** (Phase 4 doesn't exist — leave the declared seam + the existing ticket).
- Tests (stub-green): the gate runs on a fixture exhibit; a `fail` verdict blocks render; patches stage with the right `proposed_by`; a peer erroring is contained (no crash); full suite + `pipeline/tests/` stay green.

## STEP 4 — the LIVE council smoke (§0 before spend; bounded Gemini) — the proof
Run the wired gate **live** on the committed museum (`museum/character-bible/` or `museum/pencil-test/` exhibits).
- **§0 gates:** divergence `0 0`; baseline md5 byte-identical; `ANTHROPIC_API_KEY` **absent** (Sage + Chairman bill the subscription via the SDK); `GEMINI_API_KEY` present + bounded in `.env` (Annie); `which codex` confirms Codie live. Stub suite green first.
- Run the gate; **assert all three peers fired LIVE, not stub** (check `stub_fallback`/`model` on each response — a silent stub would make the smoke a lie, the 2026-06-07 "flag silently off" lesson). Confirm the chairman synthesized (separate Opus call), the agreement score computed, and patches staged with `proposed_by ∈ {codie, annie, sage, chairman}`.
- Capture a **dated trace** under `evals/` (or `docs/anima-test-runs/`): the per-peer verdicts, the dissent, the chairman adjudication, the staged patches, wall-time, which transports were live vs stub. This is the portfolio-grade "T3 works end-to-end" evidence.
- If Codex wasn't installable, run two-vendor (Codie stub) and **say so plainly** in the trace; ticket the Codie-live confirmation.

## STEP 5 — state-of-record + tickets
- **CLAUDE.md** — flip the T3 row from "Pending agent-fleet session" to **built**, citing the live-smoke trace (transports live, chairman synthesis, gate wired at `pre_museum`). Keep Em's rows untouched.
- **CHANGELOG** + **`docs/pipeline-architecture-v1.md`** §Critic Stack status (T3 implemented at `pre_museum`; `post_animatic` declared-pending-its-phase) + the `critics.t3` manifest note.
- **Ticket the non-blocking follow-ons** (code-brain `vault/00_inbox/tickets.md` manual lane): (a) **Sage-tier bake-off, Open Q2** — Opus-Sage vs Sonnet-Sage, chairman held constant, measure dissent richness + synthesis quality; (b) **agy transport cleanup** — `run_antigravity_with_image` requires `-m` which exit-2s on the real binary, and `agy` is an agentic harness unfit as a critic transport: drop `-m` or retire the transport (no critic consumes it — Em + Annie both use the Gemini API); (c) **`post_animatic` T3 gate** — wire when the Animatic phase lands.

## Fleet-ops
Isolated worktree off `origin/main` · single owner · `git fetch` + divergence before AND after · `ANTHROPIC_API_KEY` **absent** (Opus seats bill the subscription) · `GEMINI_API_KEY` bounded from `.env` (Annie's live calls only) · Codex on ChatGPT Plus (subscription) · no `start_new_session` on the worker · land via squash PR off `origin/main` · clean teardown. Full protocol: [`docs/fleet-ops-protocol.md`](fleet-ops-protocol.md).

## The mistake ledger — do not re-learn
- **Verify the binary, not the docstring** — Codie's live `codex exec` shape before the smoke depends on it (the agy `-m` lesson, again).
- **Assert peers fired live, not stub** — a silent stub-fallback would make the smoke meaningless (the 2026-06-07 silent-flag lesson).
- **A peer erroring is a contained gap, never a gate-aborting crash** (Gate-3 v1).
- **Patches stage, never auto-apply** (`auto_apply: false`).
- **Don't touch `evals/vision_critic/` or Em's verdict baseline** (md5 byte-identical before AND after).
- **`post_animatic` stays unwired** — don't build a gate for a phase that doesn't exist.

## Deliverables checklist (Session B)
- [ ] §0: local main synced to #41, old worktree removed, divergence `0 0`, baseline md5 unchanged.
- [ ] `critics.t3:` manifest block (peers + chairman + budgets, `auto_apply: false`).
- [ ] Codie verified live; `run_codex_with_image` reconciled to the real binary; `tests/test_cli_runners.py` green.
- [ ] `pre_museum` gate wired into `build_museum.py` (blocks `--render` on `fail`; patches stage); gate tests green; full suite + `pipeline/tests/` green.
- [ ] Live council smoke trace (three transports live-or-honestly-noted, chairman synthesis, staged patches, wall-time).
- [ ] CLAUDE.md T3 row → built; CHANGELOG; architecture-doc status; verdict baseline md5 unchanged.
- [ ] Tickets filed: Sage bake-off (Open Q2), agy cleanup, post_animatic gate.
- [ ] Land via squash PR off `origin/main`.
