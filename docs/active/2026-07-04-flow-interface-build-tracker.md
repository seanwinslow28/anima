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
| **UI v1a — Dashboard + Run overview** | ui | ✅ | #78 | Opus/Codex | the first visible app |
| Daemon Slice 3 — artifacts + frame images | daemon | ✅ | #75 | Opus/Codex | v1b gate/eye-gate reads |
| Daemon Slice 4 — the job layer (subprocess driver + lock + `202`/poll + cancel) | daemon | ✅ | #82 | **Fable** | all writes |
| Daemon Slice 5 — POST gate actions (7 gates over the job layer) | daemon | ✅ | #83 | Opus/Codex | v1b gates |
| Daemon Slice 6 — run creation + brief upload | daemon | ⬜ (JIT-deferred) | — | Opus/Codex | new-run from UI |
| UI v1b — the gate screens + eye-gate | ui | 🔷 plan converged (11 slices) | `docs/v1b-build-plan` | mixed (eye-gate engine = **Fable**) | "the terminal is dead" |
| **v1b U0 — REEL ONE design system** (tokens + motion + 7 primitives + `/dev/system`) | ui | ✅ | #86 | Fable | U1–U5 (everything downstream imports it) |
| **v1b U1 — booth shell + routing + HUD host** (BoothShell/HudHost/⌘K + the URL scheme) | ui | ✅ | #87 | Fable | U2a+ (every screen renders inside it) |
| **v1b U2a — Dashboard re-skin** (the booth marquee: run cards + all five doctrine states) | ui | ✅ | #88 | Fable | U2b (the Run Overview build follows) |
| **v1b U2b — Run Overview build** (the booth board: stage reel + hero + box office + crew + frame-reel, two reads, no polling) | ui | ✅ | #89 | Fable | U3 (the job-poll pattern + gate shell) |
| **v1b U3 — the shared job-poll pattern + gate shell, proven on the Plan gate** (useGateAction/usePolledResource/runContext + GateShell + PlanGate + the overview live-poll swap; the MSW job seam U4/U5 inherit) | ui | ✅ | #90 | Fable | U4a/b/c + U5 (every gate reuses the hook + shell) |
| **v1b U4a — the Script gate** (ScriptGate + BeatsSheet: the screenplay lit page + the instant Script ⇄ Beats toggle + approve over U3's hook) | ui | ✅ | #91 | Fable | U4b (Storyboard gate next) |
| **v1b U4b — the Storyboard gate** (StoryboardGate + SlateStack + `parseShots`: the lit continuity report + display-only slates + the chain_from loop marker + Lock picture over U3's hook, with THE INVALID-LOCK state — the daemon's refusal framed as "the board won't lock yet"; NEW DEP js-yaml) | ui | ✅ | #92 | Fable | U4c (Animatic gate next) |
| **v1b U4c — the Animatic gate, thin + opt-in** (AnimaticGate: the placement instruction page (G3 — roughs on disk, no upload) + the holds strip off `/status.frames[].hold` with the empty shape first-class + BOTH roads — "Ingest & generate" AND "Continue without roughs" — through the SAME `POST /animatic/approve` (skip = approve-empty) + the REFUSED-INGEST state. **The document gates are COMPLETE — only U5 (eye-gate) remains.** Live seam finding: the daemon serves `frames: []` at stage ANIMATIC — `frame_order`/holds populate in `enter_generate`, AFTER this gate — so the quiet board-holds line is the live default; the strip lights if the projection ever carries frames here) | ui | ✅ | #93 | Fable | U5a (the eye-gate stage — the last unit) |
| **v1b U5a — the eye-gate stage + Em read-out + THE ROCK/FLIP LOOP** (EyeGate at `/runs/:id/frames/:n`: the lit stage + take switching + burn-ins/timecode + honest missing-image states; EmReadout — one card per cast namespace, four slots, Lamp-before-words, the boundary line; the client-composed provenance line (G8); the filmstrip ledger ringed on the viewed frame; **rock/flip — hold Space, 12fps stepped, the shown take riding its slot, release freezes; reduced-motion = a single hand-step** (LOOP-FIRST: pulled forward from U5c per Sean's call); imagePreload + the stage's keyboard-focus infra (Space + numbers only — ⏎/R/↑↓ are U5b, O/D/L are U5c). All client-side over the shipped reads; live-verified on a stub GENERATE run) | ui | ✅ | #94 | **Fable** | U5b (print/again over the job layer) |
| **v1b U5b — the eye-gate keyboard SM + PRINT/AGAIN over the job layer** (the rest of the key map — `⏎` print · `R` again · `↑↓` walk reviewable frames · `?` cheat-sheet · `⌘K` pass-through, every key with a visible toolbar button; **PRINT** = `POST /frames/{n}/approve?attempt=<shown>` via U3's `useGateAction` → CircledTake → ritual-leader veil → **cel-flip advance on the inline `next_action`** (skips approved; assemble/done → overview; reduced-motion = soft crossfade, never a dead cut); **AGAIN** = the retake note **prefilled from Em** (`composeEmNote`: proposed fixes first, flagged reasoning fallback, honest no-attribution when empty), auto-pauses the loop, `retry {note}` → same-frame terminal re-reads takes in place; all D-C branches surfaced honestly; two structural finds — the decision layer lives in EyeGate above the Screening remount, and the last-ready `/status` keeps the stage lit through the terminal re-read. Live-verified: print + retry on the wire against a stub GENERATE run. NO onion/diff/lights — U5c's seams clean) | ui | 🟡 | `feat/v1b-u5b-eyegate-decide` | **Fable** | U5c (instrument modes + polish — the last slice) |
| Deltas D1 (retry annotations) / D2 (front-door surface) / D3 (chat) | daemon | ⬜ | — | Opus/Codex | v1c |
| UI v1c — brainstorm room + chat bar + eye-gate annotation | ui | ⬜ | — | mixed | the anima differentiators |
| D5 — studio taste-memory | daemon | ⬜ | — | **Fable** | the taste ledger |
| D4 (Cy bible jobs, `route` on candidate, Motion) / D6 (`injected_plates`) | daemon | ⬜ | — | Opus/Codex | v2 |
| UI v2 — character builder / storyboard board / generate grid / motion | ui | ⬜ | — | mixed | the visual pages |
| UI v3 — the timeline | ui | ⬜ | — | Opus/Codex | arrange/trim/export |

**Right now (updated 2026-07-09):** Daemon Slices 1–5 **and** UI v1a are all merged — **the entire core-gate-loop backend is done.** Read API (#73/#74/#75), the first visible app (#78), the job layer (#82: registry + injectable subprocess driver + flock + `202`/poll + psutil cancel), and now the **seven POST gate actions** (#83: plan/script/storyboard/animatic approve, frame approve/retry, assemble — each over the job layer with the single-writer 409 + the additive `blocked_by_job` suppression that closes the active-cascade catch). Independently verified this session: `python -m pytest tests/` = **910 green**, `tests/server/` = **103 green**, `pipeline/tests/` = **10 green**; scope clean (`server/` only, `jobs.py` frozen, `pipeline/`+`evals/` byte-identical, both md5 guards unmoved).

**The JIT-correct next move is the UI — v1b (gates + eye-gate) — NOT Slice 6.** v1b's gate/eye-gate screens bind to Slices 1–5 exactly as they stand. **Slice 6 (run-create + brief upload + `GET /characters` + cost-estimate) is deferred JIT** — built right before/with the v1b screen that needs new-run-from-UI, decided during the v1b brainstorm (building it now would be backend ahead of its consumer — the anti-drift lesson). **v1b direction chosen (2026-07-09):** the Fable-5 exploration pass shipped 3 directions (PR #84); Sean picked **B · REEL ONE — the screening room** as the v1b language, and **banked C · ACCESSION for the future museum redesign.** Standing build mandate (in memory, a design gate not a preference): **show, don't tell** — default state = the art + the one decision; secondary info arrives on intent. REEL ONE needs **zero daemon deltas** for v1b (D4 Motion later makes the screening room a player for free). See the exploration brief ([`2026-07-09-v1b-elevate-exploration-brief.md`](2026-07-09-v1b-elevate-exploration-brief.md)) + the directions ([`2026-07-09-v1b-elevate-directions/`](2026-07-09-v1b-elevate-directions/), PR #84).

**Done: the full v1b build is mapped.** [`2026-07-09-v1b-build-plan-CONVERGED.md`](2026-07-09-v1b-build-plan-CONVERGED.md) decomposes v1b into **six conceptual units → eleven build slices** (one TDD session each), each a titled stub with daemon bindings + MSW seam + model tier: **U0** design system → **U1** booth shell + routing + HUD → **U2a** Dashboard re-skin → **U2b** Run Overview build → **U3** the shared job-poll pattern + gate shell (proven on the Plan gate) → **U4a/b/c** Script / Storyboard / Animatic gates → **U5a/b/c** the eye-gate engine [**Fable**]. Two independent adversarial passes ran (a fresh-context Claude red-team + a Codex `exec` critique); corrections folded in (the plan carries the reconciliation). **Correction to the earlier "zero deltas" line:** REEL ONE needs **no daemon deltas as a prerequisite**, but not *zero* — ten gaps (G1–G10) are handled in v1b by derive/omit/narrow, each a named v1c/v2 promotion (the load-bearing ones: no cost-spent accumulator; no send-back/curation/animatic-upload write paths; the Bible anchor isn't served). **Eight open decisions await Sean** (Slice-6 OUT, the write-path narrowings, HUD scope, the U5a model call — all with recommendations in the plan). **Next: cut the U0 kickoff** (mirror the last UI kickoff) once Sean signs off on the decomposition; U0/U1/U2a can spawn now, with one light contract-tighten already folded before U3.

---

## The execution sequence (interleaved, JIT backend)

The principle: **build backend just-in-time for the UI milestone that consumes it — never backend ahead of its consumer** (the anti-drift lesson). UI + its backing daemon slices land together as demoable increments.

```
[done] Slices 1–3 (read spine + artifacts+images) ──▶ v1a UI [done]
   ──▶ Slice 4 (job layer) [done]  ──▶ Slice 5 (POST gates) [done]
   ──▶ v1b UI (gates + eye-gate; eye-gate engine = Fable)   ← WE ARE HERE ("the terminal is dead")
        · Slice 6 (run-create) built JIT when v1b needs new-run-from-UI
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
