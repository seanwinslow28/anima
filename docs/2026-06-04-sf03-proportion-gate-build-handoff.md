# Handoff — SF03 proportion-gate build (G6.4): probe Approach A, then build A or B

*2026-06-04. Costed Claude Code handoff under [`docs/fleet-ops-protocol.md`](fleet-ops-protocol.md). Executes the parked design at [`docs/2026-06-03-sf03-proportion-gate-design.md`](2026-06-03-sf03-proportion-gate-design.md) — read it first; this brief does not restate it. Sean queued the build in the 2026-06-04 G6 Cowork session. Runs in parallel with the Em diagnostics arc — SF03 is generation-time (Cy Pass-3 / Bible-lock), independent of Em, references, and the citation work; it never touches Em's input surface, so no re-baseline interaction.*

**Standing doctrine: verify against the tree, never trust a label — including this brief.**

> **Cleared for parallel execution — 2026-06-08 Cowork planning session.** Sean confirmed this build runs concurrently with G6.9 ([`docs/2026-06-08-g6.9-prompt-diff-eval-handoff.md`](2026-06-08-g6.9-prompt-diff-eval-handoff.md)). Separate worktree, single owner each; SF03 is generation-time and never touches Em's surface, so the two can't collide. Re-verify the tree (HEAD was `3dfdc24` at planning time; `git fetch` was offline in the sandbox) before starting.

---

## Sequence

### 1 — The gating probe (small costed generation: a handful of NB2 plates)

The design's make-or-break question: **does NB2 honor a provided armature underlay** — crown to line 0, feet to line N, head filling band 0–1? Generate a small probe set (front + profile + back + ¾, the view-invariance check is free if all four are probed) with the heads-tall ladder as underlay. Then a measurement micro-spike on the gridded renders: can the gate reliably read printed armature lines + chin-at-first-division? (Design doc open questions 1, 3, 4.)

**Decision point — record the verdict in the field report:**
- Probe PASSES → build **Approach A** (armature-constrained generation + automated grid-alignment check).
- Probe FAILS → build **Approach B** (lock-time assisted measurement — guided crown/chin/feet capture → locked proportion spec, enforced deterministically thereafter). B is guaranteed-feasible and exactly scoped to the tiny lock-time volume.

Do not let the probe sprawl: a handful of plates decides it. If ambiguous, B.

### 2 — The build (whichever approach won)

- **Hard gate at Bible-lock** (unlike the record-only Pass-2.5 similarity gate): a body turnaround outside tolerance (default `[6.5, 7.5]` heads for sean-anchor) **blocks the lock** with a proportion verdict.
- **Per-character spec-driven, never hardcoded 1:7**: the target ratio + tolerance live in the character's spec; `claude-mascot` (box-creature, not heads-tall) gets its own declared proportion spec or an explicit opt-out.
- Wires a measured `heads_tall` + per-division alignment into the plate verdict, persisted beside `runs/{run_id}/plate_verdicts.jsonl`.
- Makes `IR.sean.proportion.head-to-body-1-to-7` *checkable* instead of prose.
- Credential-free stub path so the contract layer exercises in CI; tests in `tests/`, green without API keys.

### 3 — Retroactive re-verification (the A4 loop close)

Run the built gate against `characters/sean-anchor/turnarounds/` body plates — the 1:7 re-lock that shipped in `b7323e3` with a **human gate standing in for SF03**. This is the promised retroactive verification. If a re-locked plate FAILS the gate, that is a finding to surface to Sean immediately, not to quietly fix.

## Deliverables

1. Probe verdict + measurement-spike result (field report `docs/anima-test-runs/2026-06-XX-sf03-probe-and-build.md`).
2. Gate implementation + tests (CI-green, credential-free stubs).
3. Retroactive verdicts on sean-anchor's re-locked body turnarounds, persisted.
4. CHANGELOG entry; CLAUDE.md QA-gates section update if the gate ships (SF03 row gains its automated test).
5. Merge the branch **INTO MAIN**, push, clean-teardown the worktree.

## Fleet-ops checklist

Isolated worktree · `ANTHROPIC_API_KEY` absent · `GEMINI_API_KEY` bounded from `.env` (NB2 probe generations) · singleton pre-flight · single owner · no `start_new_session` on the costed worker · clean teardown · merge into main.

## Out of scope

Em / T2 / references (explicitly not on Em's path per the design) · re-baking any Bible plate (a gate failure is a *finding*, the re-bake is its own decided work) · per-frame proportion checking (the gate lives at Bible-lock where the volume is tiny and the drift originates).
