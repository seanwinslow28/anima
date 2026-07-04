# Flow Interface — Build Tracker (② daemon + UI)

**Date:** 2026-07-04 · **Status:** Living. This is the single source of truth for *where the ② build is and what the next unit is*. A fresh session should read **this doc + the three specs** (linked at the bottom) and be able to continue the review→kickoff rhythm with no other context.

**Why this exists:** the ② daemon + UI is a long, multi-session build executed one unit at a time. Conversations run out of context; this doc is the hand-off anchor so the cadence survives a fresh session.

---

## How we work (the standing rhythm — do not change without a reason)

- **One unit per fresh Claude Code session**, then: TDD → PR → a planning session reviews it independently → merge → next unit. Three units have landed this way (#73, #74, and the v1a UI branch).
- **The loop:** Sean asks for the next kickoff → the planning session (a) independently verifies the last unit's PR/worktree, then (b) hands Sean a ready-to-paste kickoff for the next unit. Sean runs it in a fresh session set to the right model.
- **Model split (Sean's call, from the v1.1 addendum):** **Fable 5** for the *tough* builds; **Opus 4.8 / Codex** for the rest. Tough = the daemon **job layer (Slice 4)**, the **eye-gate interaction engine** (Pick 1), the **taste-memory derivation** (Pick 4 / D5). Everything else is Opus/Codex.
- **Standing discipline every unit carries** (bake into every kickoff):
  - Fresh git worktree off **latest** `main` — `git fetch origin && git reset --hard origin/main` **before writing code** (the stale-clone trap bit us once: a worktree branched from a pre-#73 main and had to be reset onto `origin/main`).
  - TDD: red → verify-red → green → verify-green; **commit per task** (an interrupted v1a agent left all work uncommitted — don't repeat).
  - Credential-free tests; `ANTHROPIC_API_KEY` absent; per-directory test runs (`python -m pytest tests/` and `pipeline/tests/`; `cd web && npm run test`).
  - **Daemon slices:** all new code under `server/`; `pipeline/` and `evals/` **byte-identical**; the two md5 guards unmoved (`2af75906…` g6.1b trace, `945af824…` screenwriting voice).
  - **UI slices:** all new code under `web/`; browser-first (no Electron/Tauri until v1b); the mockups' CSS tokens + the a11y contract; MSW-mocked tests (no live daemon in CI). **`web/.gitignore` must exist** (node_modules / dist / *.tsbuildinfo) before `git add`.
  - Full verification gate + **stop green + PR**; do not roll into the next slice.

---

## Status board

Legend: ✅ merged · 🟡 built-green, PR open (needs review/merge) · 🔷 kickoff issued / in flight · ⬜ not started.

| Unit | Layer | Status | PR / branch | Model | Unblocks |
|---|---|---|---|---|---|
| Daemon Slice 1 — skeleton + `GET /runs/{id}/status` | daemon | ✅ | #73 | Fable | v1a |
| Daemon Slice 2 — `GET /runs` + `GET /runs/{id}` | daemon | ✅ | #74 | Fable | v1a |
| **UI v1a — Dashboard + Run overview** | ui | 🟡 | `worktree-flow-web-v1a` (commit 5b0e93a) | Opus/Codex | the first visible app |
| Daemon Slice 3 — artifacts + frame images | daemon | ✅ | merged (Kickoff A) | Opus/Codex | v1b gate/eye-gate reads |
| Daemon Slice 4 — the job layer (subprocess driver + lock + `202`/poll) | daemon | ⬜ | — | **Fable** | all writes |
| Daemon Slice 5 — POST gate actions | daemon | ⬜ | — | Opus/Codex | v1b gates |
| Daemon Slice 6 — run creation + brief upload | daemon | ⬜ | — | Opus/Codex | new-run from UI |
| UI v1b — the gate screens + eye-gate | ui | ⬜ | — | mixed (eye-gate engine = **Fable**) | "the terminal is dead" |
| Deltas D1 (retry annotations) / D2 (front-door surface) / D3 (chat) | daemon | ⬜ | — | Opus/Codex | v1c |
| UI v1c — brainstorm room + chat bar + eye-gate annotation | ui | ⬜ | — | mixed | the anima differentiators |
| D5 — studio taste-memory | daemon | ⬜ | — | **Fable** | the taste ledger |
| D4 (Cy bible jobs, `route` on candidate, Motion) / D6 (`injected_plates`) | daemon | ⬜ | — | Opus/Codex | v2 |
| UI v2 — character builder / storyboard board / generate grid / motion | ui | ⬜ | — | mixed | the visual pages |
| UI v3 — the timeline | ui | ⬜ | — | Opus/Codex | arrange/trim/export |

**Right now:** Daemon Slices 1–3 (the full read API) are merged. UI v1a is built-green on its branch (typecheck clean, 17/17 Vitest, `npm run build` ok, daemon-smoke confirmed against real runs) — **open its PR + merge after Sean's browser eyeball.** After v1a lands, the next backend unit is **Slice 4 (the job layer — Fable 5)**, and the next UI milestone is **v1b (gates + eye-gate)**.

---

## The execution sequence (interleaved, JIT backend)

The principle: **build backend just-in-time for the UI milestone that consumes it — never backend ahead of its consumer** (the anti-drift lesson). UI + its backing daemon slices land together as demoable increments.

```
[done] Slices 1–2 (read spine) ──▶ v1a UI  ‖  Slice 3 (artifacts+images)   ← WE ARE HERE
   ──▶ Slice 4 (job layer, Fable) ──▶ Slices 5–6 (POST gates, run-create)
   ──▶ v1b UI (gates + eye-gate; eye-gate engine = Fable)          ← "the terminal is dead"
   ──▶ D1–D3 ──▶ v1c UI (room + chat + pen)
   ──▶ D4/D6 ──▶ v2 UI (visual pages)  ·  D5 ──▶ taste ledger (Fable)
   ──▶ v3 UI (timeline)
```

The desktop Electron/Tauri shell wraps the browser app **once v1b is proven** (spec decision), not before.

---

## Next units — scope + how to write each kickoff

Each kickoff is written by mirroring the last same-layer kickoff. The pattern is fixed (intent → context/read-first → scope boundaries → contract → TDD tasks → verification gate → discipline → stop-green+PR).

- **Daemon Slice 4 — the job layer (Fable 5).** The pivotal backend build. Per the daemon plan's Fork 1/2 + the "Slice 4" stub: an in-process job registry (`pending/running/succeeded/failed`, `rc`, captured stdout/stderr, `fresh_state|null`, `load_error?`), a **per-run file lock (daemon-vs-daemon only** — the honest limit; the CLI can't be made to take it without touching `pipeline/`), and a subprocess driver that runs `python -m pipeline.run --resume …` with `cwd=<repo root>` under the fleet-ops env-strip (never `--allow-api-key`). `GET /jobs/{job_id}`. `status_view` gains an `active_job` field. **Test seam:** inject a stub driver (no real subprocess). Read: daemon plan §Fork 1, §Fork 2, "Slice 4/5" stubs, and the red-team notes.
- **Daemon Slice 5 — POST gate actions (Opus/Codex).** The eight write endpoints over the job layer: advisory stage pre-check → 409; atomic job-slot reservation → 202 `{job_id}`; second POST to a busy run → 409; on completion re-read `load_state` (even on `rc != 0`, with a `load_error` branch); suppress the mutating `next_action` while a job owns the run. Retry → `retry_frame` (not `run_frame_fan`).
- **Daemon Slice 6 — run creation + brief upload (Opus/Codex).** `POST /runs` (multipart brief upload → `python -m pipeline.run --brief …` job), `GET /runs/{id}/cost-estimate`, `GET /characters`, `GET /characters/{id}`.
- **UI v1b — gates + eye-gate (mixed).** The plan/script/storyboard/animatic gate screens + the eye-gate (approve/retry) over the artifact reads (Slice 3) + the `202` job layer (Slices 4–5). **The eye-gate interaction engine (rock/flip, onion-skin, diff-wipe, the keyboard state machine — v1.1 Pick 1) is the Fable-5 sub-unit**; the gate shells are Opus/Codex. Read: uxui-spec screens 4–8, addendum Picks 1/2/3.
- **v1c / v2 / v3 + D1–D6 + the taste ledger (D5, Fable):** per the uxui-spec §Build sequencing + the addendum's daemon-delta table + model-routing section. Write each kickoff when its milestone becomes active.

---

## Recurring gotchas (write these into kickoffs)

1. **Fetch latest `main` first.** A worktree cut from a stale local clone missed a merged slice; always `git fetch origin && git reset --hard origin/main` before coding.
2. **Commit per task.** An interrupted v1a session left `web/` fully uncommitted (zero commits) and 3 tests red — the work looked "maybe done" but wasn't. Commit as you go so a stop leaves a clean, reviewable state.
3. **`web/.gitignore` before `git add`.** Vite scaffolds don't always include it; without it `git add web/` stages 150M of `node_modules` (+ `dist`, `*.tsbuildinfo`).
4. **Dual-Vite test typing.** Keep `defineConfig` from `vite` (so the `react()` plugin type matches) and cast the config `as UserConfig` to carry the Vitest `test` key — importing `defineConfig` from `vitest/config` pulls Vitest's nested Vite and breaks the plugin type.
5. **The browser eyeball is a human step.** UI kickoffs end green on tests + build; the final "does it look right against real runs" check is Sean's (`ANIMA_RUNS_ROOT=<repo>/runs uvicorn server.app:app` + `cd web && npm run dev`).

---

## Where the detail lives (the three specs)

- **Daemon contract + per-slice stubs + fork decisions + red-team:** [`2026-07-02-daemon-build-plan-CONVERGED.md`](2026-07-02-daemon-build-plan-CONVERGED.md).
- **UI screens (v1→v3), design system, a11y contract, §Build sequencing, §Daemon-contract deltas D1–D4:** [`2026-07-03-flow-interface-uxui-spec.md`](2026-07-03-flow-interface-uxui-spec.md).
- **v1.1 ratified picks (eye-gate instrument, taste ledger, crew, warmth-motion, recipe strip) + deltas D5/D6 + model routing:** [`2026-07-03-flow-interface-spec-addendum-v1.1.md`](2026-07-03-flow-interface-spec-addendum-v1.1.md).

*Update this tracker's status board on every merge, and add the next unit's kickoff-recipe row as its milestone becomes active. Keep it trustworthy — it's the continuity anchor.*
