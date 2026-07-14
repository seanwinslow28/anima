# Kickoff — Higgsfield transport live smoke (Task 7) + build closeout

**Date:** 2026-07-14 · **Workstream:** the outward turn (closes out the T1 build of the [ratified transport decision](2026-07-13-transport-strategy-decision.md)) · **Status:** kickoff — not yet run · **Prereqs (all met):** PR #112 (decision docs) + PR #113 (the runner build) squash-merged to main; Claude's review passed (2026-07-14). · **Spend:** ~8–15 Higgsfield credits, Sean-gated in-session.

---

## The pasteable kickoff prompt

> You are running the **Higgsfield transport live smoke + closeout** for anima — Task 7 of the switchover plan, the first real generation through the production gpt-image path, plus the post-merge housekeeping. Everything before the smoke is $0; the smoke itself costs ~8–15 credits and **each spend needs Sean's explicit go in this session**. Walk Sean through it step by step — he is at the keyboard.
>
> **Read first:**
> 1. `docs/active/2026-07-13-transport-strategy-decision.md` — the ratified policy (D1–D6); this session executes its plan §T1's final gate.
> 2. `CHANGELOG.md` top entries (the 2026-07-13/14 transport build) — what shipped, the red-team ledger, and the runner's safeguards.
> 3. `pipeline/agents/higgsfield_runner.py` — skim the module docstring + `invoke_higgsfield_image_edit` + `_invoke_real`. Know before you run: the runner **fail-closes on any CLI version other than the pinned `0.2.3`** (`PINNED_HIGGSFIELD_CLI_VERSION`), and a response with `exit_code=78` means "charged job in an uncertain state — operator resolution required" (inspect `<key>.pending.json` / `.quarantine.json` / `.create_in_flight.json` in the cache dir; remove only after resolving the job).
> 4. `docs/architecture/fleet-ops-protocol.md` — costed-run discipline.
> 5. `docs/anima-test-runs/2026-07-13-transport-probes-and-pricing-field-report.md` §2 — the probe evidence this smoke extends (the smoke = the *production path*; the probe was raw CLI).
>
> **PHASE 0 — housekeeping ($0).**
> 1. Confirm `main` carries #113 (`git log --oneline -3`) and both suites are green on main: `python -m pytest tests/ -q` then `python -m pytest pipeline/tests/ -q` (separate runs, ANIMA_FORCE_STUB=1).
> 2. Tear down the merged build worktree + branches: `git worktree remove .claude/worktrees/feature+higgsfield-transport` (add `--force` only if it refuses on the gitignored `.superpowers/` dir — but FIRST copy `.superpowers/sdd/final-fix-report.md` somewhere if Sean wants it kept; it is not committed), then `git branch -d feature/higgsfield-transport docs/transport-strategy-decision` and prune stale remotes (`git remote prune origin`).
> 3. Fleet-ops pre-flight: `echo "${ANTHROPIC_API_KEY:+SET}"` prints nothing; singleton check per protocol §3; confirm `ANIMA_FORCE_STUB` is NOT set in the shell.
> 4. CLI pre-flight — **do NOT upgrade or reinstall the CLI** (upstream is v1.x; the runner refuses anything but 0.2.3): `higgsfield --version` → must say `0.2.3`. Sean (human-only) confirms auth + balance: `higgsfield account status`. Read-only cost check: `higgsfield generate cost gpt_image_2 --quality high --resolution 1k --prompt x`.
>
> **PHASE 1 — the live smoke (Sean's explicit GO required before each spend).**
> 1. **First real generation through the production path** (the plan's Task 7 shape — Python via `invoke_image_edit`, NOT raw CLI, because the runner is what's being validated). From the repo root:
>
> ```bash
> python3 - <<'EOF'
> from pathlib import Path
> from pipeline.agents.nb_pro_runner import invoke_image_edit
> resp = invoke_image_edit(
>     prompt=("Same character as the reference image. Full-body three-quarter "
>             "view model plate, standing neutral. Keep the face, hairstyle, "
>             "outfit, and proportions exactly the same as the reference. "
>             "Same raw gritty hand-inked style as the reference."),
>     reference_images=[Path("registers/primal-sketch-grit/refs/primal-sketch-grit-hero.png")],
>     output_path=Path("runs/2026-07-14-higgsfield-smoke/plate.png"),
>     cache_dir=Path("runs/2026-07-14-higgsfield-smoke/.cache"),
>     model="gpt-image-2",
> )
> print(resp)
> EOF
> ```
>
>    Expected: `ok=True, stub_fallback=False, cache_hit=False`, non-null `job_id`/`result_url`/`cli_version="0.2.3"`; the PNG exists; the cache dir holds `<key>.png` + `<key>.provenance.json` (open it — verify transport/vendor_model/job_type/params/job_id recorded) and NO leftover `.pending.json`/`.create_in_flight.json`. If instead `exit_code=78`: stop, read the `error` field, resolve the receipt with Sean before any retry (a job may have been charged).
> 2. **Cache-hit proof (zero spend):** run the identical snippet again → `cache_hit=True`; Sean confirms the credit balance moved only once (`higgsfield account status`, or MCP `balance`).
> 3. **Sean's eye (the arbiter):** open the plate next to the hero (`registers/primal-sketch-grit/refs/primal-sketch-grit-hero.png`). Two questions: does the character read as the same character, and does the register hold (raw grit, not cleaned-up)? Record PASS/notes verbatim. (This is a smoke, not the T2 gate — one plate proves the transport, not Bible-pass identity.)
> 4. *(Optional, Sean's call, ~4 more credits)* one edit-of-edit: same snippet with `reference_images=[Path("runs/2026-07-14-higgsfield-smoke/plate.png")]` and a terse "raise right arm in a wave, change nothing else" prompt — exercises the anchor-first edit shape end-to-end.
>
> **PHASE 2 — closeout docs (in a short PR; only Sean merges).**
> 1. Field report `docs/anima-test-runs/2026-07-14-higgsfield-runner-live-smoke.md`: commands, credits spent (before/after balance), the response fields, provenance sidecar contents, Sean's eye verdict, any surprises (parse fallbacks hit? retries? wall time).
> 2. Flip the state-of-record: `CLAUDE.md` + `AGENTS.md` Cy row — replace "Task 7 live transport has not been verified" with the smoke result + field-report link (keep the T2 GRANDMASTER gate language — that is STILL gated). Backlog (`docs/active/2026-07-04-register-backlog-and-transport-findings.md` §7): the policy-decided line → T1 built (#113) + live-smoked. Decision doc's phased-plan table: mark T1 done. CHANGELOG entry. Also commit `docs/active/2026-07-14-higgsfield-live-smoke-and-closeout-kickoff.md` (this file) if it isn't already tracked.
> 3. If the smoke FAILED: no doc flips beyond an honest field report + a defect list; the runner's fail-closed behavior is itself evidence — bring the findings back for a fix session.
>
> **Guardrails:** never set `ANTHROPIC_API_KEY`; never upgrade the CLI mid-session; every generation needs Sean's go; both md5 guards must not move (`2af75906…` g6.1b trace, `945af824…` screenwriting voice); pytest runs stay per-directory. **What stays gated after this session:** T2 — the in-register Bible-pass edit-identity validation (rides the costed GRANDMASTER build); T4 — Motion wiring to Higgsfield Seedance (when Phase 6 enters the orchestrator).
>
> Start with the five reads, then Phase 0, and stop for Sean's GO before the first spend.

---

## Context notes (not part of the paste)

- **Why the smoke runs on the primal hero, not sean-anchor:** the three gpt-image registers are the transport's real consumers; the 2026-07-13 probe already covered pencil-register via raw CLI. One in-register plate is the highest-signal single spend.
- **The version-pin cliff is the #1 way this session can confusingly fail:** if anything upgraded the CLI since 2026-07-14, every call raises `UnsupportedHiggsfieldCLIVersion` — that's the runner working as designed, not a bug. Re-verifying a new CLI version is its own deliberate change (argv/output schema re-check + pin bump), not a quick fix.
- **Desktop-app backlog rider (noted in the 2026-07-14 review, not this session's work):** the front end should eventually surface exit-78 and version-pin failures as distinct transport states, not generic generation errors.
