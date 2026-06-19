# Kickoff — Em provenance + critic-spine hardening, then DINOv2

*2026-06-02. Handoff for a Claude Code session. Orient-and-decide already happened (this doc is its output); the decisions below are locked by Sean. Read the anchor postmortem [`docs/anima-test-runs/2026-06-02-em-gemini-transport-rebaseline-postmortem.md`](../../anima-test-runs/2026-06-02-em-gemini-transport-rebaseline-postmortem.md) first — this kickoff assumes it. The program this lives inside is [`docs/2026-05-31-critic-spine-hardening-kickoff.md`](2026-05-31-critic-spine-hardening-kickoff.md).*

---

## The situation in one paragraph

The Em reference-grounding re-baseline ran and produced two consequential results. **First**, a validity gate caught that the agy CLI wrapper invokes `agy -p` with **no `-m` flag**, so the Antigravity backend silently chose the model — `gemini-3.5-flash`, on 272/272 Em-sized calls, not the `gemini-3.1-pro` every label claimed. The entire T2 program (the 0.62 baseline, the 2026-05-31 bake-off) had been running on an unverified model. **Second**, with the model pinned and references attached, the eval measured the *obviously-good* change as a regression: false_pass 0.00 → 0.15, recall 1.00 → 0.85. The false-pass-first gate blocked it. Diagnosis: part Opus verdict variance, part reference **confabulation** (the MLLM recited the Bible's register onto an off-register subject), and a prompt-ablation proved the matching-wording is a forgiveness lever, not a fix.

The provenance bug is not Em-only. **Cy's Pass-3 verification calls the same wrapper** (`character_designer.py:760`) — so Cy's two shipped, locked Bibles (`sean-anchor`, `claude-mascot`) were verified by backend-default Flash, not the Pro their docs claim. `nb_pro_runner.py` does **not** use agy (it calls the pencil-animation skill script) and is clean.

## Decisions locked (Sean, 2026-06-02)

1. **References-attach** → *gate behind a flag, off by default.* Keep the PR #13 code; Em runs reference-blind (the safe 0.62 / recall-1.00 profile) until a deterministic backstop lands and a clean re-baseline clears the false-pass gate.
2. **Provenance audit** → *fix code + labels now (uncosted); defer costed Bible re-verification to a ticket.* Pin model-by-ID and log-actual-model at both agy call sites; correct the two stale "Pro" labels; file a ticket to re-verify Cy's Bibles on a pinned model later.
3. **DINOv2 deterministic identity backstop** → *promote to the next costed workstream* (after this hardening round). The confabulation finding is its motivation; a deterministic identity/proportion signal can't recite references.
4. **Baseline replication** → *N=5 runs, per-case majority vote for the point estimate, report a false_pass band.*
5. **Sequencing** → *uncosted hardening bundle first, as one CI-green PR.* Costed DINOv2 + the replicated re-baseline come after, as separate eval-gated work.

Items #5 (soften matching-wording + view-aware selection) and #6 (re-run the bake-off) from the postmortem are **deferred behind the references flag** — they only matter if references come back on, which won't happen until DINOv2 + a clean re-baseline. Carry them as backlog, don't build them now.

---

## Workstream A — uncosted hardening (do this first; one PR)

Everything here is CI-green and credential-free. No model spend. Land it as a single PR off an isolated worktree, single owner, clean teardown.

### A1 — References behind a flag, off by default
- Add `critics.t2.attach_references` to the manifest, **default `false`**.
- `vision_critic` reads it: when false, take the reference-blind path (no Bible bundle, no `IR.*`/`AC.*` criteria block attached to the subject prompt). When true, the current PR #13 behavior.
- TDD: a test that asserts the default config attaches **zero** reference images, and one that asserts `true` restores the bundle.
- Update the CLAUDE.md Em row: references-attach is **flag-gated off**, not the live default. (The row already documents the regression; just correct "shipped default" → "flag-gated, off pending DINOv2.")

### A2 — Pin model by ID + log the model that actually fired (both call sites)
This is the deepest lesson on disk: *never pin a model by label — pin by ID and verify it fired.*
- **Em** (`gemini_api_runner.py`): already pinned to `gemini-3.5-flash`. Add an explicit **log line** recording the model string the API call used (read back from the response/request, not the constant), so the provenance is in the run logs, not just the source.
- **Cy** (`character_designer.py:760` → `cli_runners.run_antigravity_with_image`): the agy path still chooses the backend default. Either (a) pass an explicit `-m` and assert the returned model matches, or (b) if Cy is also moving to the Gemini API transport, route it through `gemini_api_runner` with an explicit ID. **Whichever path**, the runner must **log the model it actually used** and raise if it can't confirm one. No silent backend-default ever again.
- Add a test that fails if a costed runner returns without an asserted/logged model id.

### A3 — Correct the stale "Pro" labels (shipped-artifact honesty)
- `manifest.yaml:257` — `default_model: "gemini-3.1-pro-via-anti-gravity"` → correct to the model that actually ran (`gemini-3.5-flash`), with an inline note pointing at the 2026-06-02 forensics. (Em's cosmetic label was annotated; finish the job.)
- `CLAUDE.md` Cy row (line ~159) — "Gemini 3.1 Pro verifies via `agy`" → "Gemini 3.5 Flash (backend default; no `-m` was passed — see 2026-06-02 provenance forensics)." Match the correction already made to the Em row.
- Grep the repo for any other `3.1 Pro` / `gemini-3.1-pro` claim tied to agy and correct each. **Do not** touch eval-case labels — those are locked; anything that looks wrong goes to Sean for re-ratification.

### A4 — Cy Bible re-verification ticket
- Append a one-line ticket to `/Users/seanwinslow/Code-Brain/code-brain/vault/00_inbox/tickets.md` under `## Todo`: re-verify `sean-anchor` + `claude-mascot` Bibles' Pass-3 on a pinned model (they were Flash-verified, not Pro) — costed, scheduled after the hardening PR. Assign as appropriate.

### A5 — Replication in the costed scorer
- Extend `evals/vision_critic/score.py` to support `--runs N` (default keep at 1 for cheap smoke; the real baseline runs `--runs 5`).
- Per case: take the **majority verdict** across N runs for the point estimate; compute and report a **false_pass band** (min/max across runs, and ±1 stderr) in `last-run.md`.
- Persist per-run verdicts so a flip (like the stylus case) is visible in the trace, not averaged away silently.
- TDD with mocked verdicts: feed a case that flips 3-pass/2-fail and assert majority = pass and the band is reported.

**Workstream A definition of done:** contract suite green credential-free; `--stub` still exercises both transports; the manifest default makes Em reference-blind; both runners log their model; labels corrected; ticket filed. PR merged to `main`, worktree + branch torn down.

---

## Workstream B — costed, eval-gated (after A; separate handoff)

Do **not** start B in the same session as A unless A is fully merged and Sean greenlights the spend. B is costed and must run under full fleet-ops discipline.

### B1 — DINOv2 backstop spike → integration
- Start from the existing Pass-2.5 similarity gate (`pipeline/agents/similarity_gate.py`, DINOv2→CLIP→PIL ladder) — the embedding machinery already exists.
- **Spike first:** does DINOv2 distance separate the labeled defect cases from the clean ones on the existing 23-case performs fixture set? Score it like any agent — segmented, false-pass-first. If the signal separates the identity/proportion defects (the confabulation cases), promote to integration as a deterministic signal *beside* Em in the T2 path (not replacing the MLLM — augmenting it on fine-grained identity/proportion).
- This needs per-view references to be meaningful (a single front anchor can't separate legitimate view variation from drift — the known similarity-gate limitation). Scope view-aware reference selection (postmortem approach A) **as part of B1**, since DINOv2 needs it too.

### B2 — Replicated, clean re-baseline
- Run the costed scorer at `--runs 5` on a **pinned, logged** model.
- For a clean references-isolation read, also run a **reference-blind** pass on the *same* API transport (the postmortem flagged the 0.62 baseline crossed transport + references). Only then is the references delta attributable.
- Re-baseline is the gate that decides whether references ever come back on (flips A1's flag default).

### B3 — Bake-off re-run (only after B2)
- Re-run the three-way T2 bake-off with **models pinned by ID and correctly labeled** — the "Gemini" column was Flash, pin it explicitly. Attach references on all three columns only if B2 cleared the references question.

---

## Operating rules (non-negotiable)

- **Cowork-then-Code:** this orient-and-decide session produced this doc; the *builds* happen in Claude Code.
- **Plan-first, empirical-not-vibes.** The headline lesson is that the obvious change regressed safety. Treat **every** proposed fix as eval-gated, including the ones that feel too obvious to test.
- **Pin models by ID; verify from logs; never trust a label.** This is the deepest lesson and it now has code teeth (A2).
- **Eval-case labels stay locked.** Anything that looks mislabeled comes to Sean for re-ratification — do not edit a case label unilaterally.
- **Billing + isolation (fleet-ops protocol):** Claude on the subscription SDK (`ANTHROPIC_API_KEY` **absent**), Gemini on the bounded API key. Never route Claude through a non-Anthropic API. Costed work in an isolated worktree, single owner, singleton pre-flight, clean teardown (don't `start_new_session` a costed worker).
- **Maintenance conventions:** append a CHANGELOG.md entry for every change; update CLAUDE.md when structure/conventions/active-phase shift (the label corrections and the references-flag both qualify).

## First actions for the Claude Code session
1. Set up a task list from Workstream A (A1–A5).
2. Create an isolated worktree off clean `main` (`87a839e` or later).
3. Build A1–A5 TDD, red-first, suite green credential-free.
4. Correct labels + file the Cy ticket; CHANGELOG + CLAUDE.md updates.
5. Open the PR; report the diff and the green suite; stop before any costed work (Workstream B is a separate greenlit handoff).
