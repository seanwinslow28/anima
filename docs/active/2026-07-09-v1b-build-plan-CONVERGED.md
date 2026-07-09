# ② Flow Interface — v1b "REEL ONE": Converged Build Plan

> **For agentic workers:** each unit below is a **titled stub — designed here, built JIT** in its own fresh session. When a unit becomes active, its kickoff is written from this doc (mirror the last same-layer kickoff), then: REQUIRED SUB-SKILLS — superpowers:test-driven-development (red → verify-red → green → verify-green), superpowers:using-git-worktrees (isolate off latest `main`), superpowers:verification-before-completion (evidence before "done"). This plan writes **no production code and no tests** — it is the source of truth the per-unit kickoffs are cut from.

**Date:** 2026-07-09
**Status:** Plan — converged. Drafted this session, then run through an independent adversarial pass (a fresh-context Claude red-team + a Codex-style engineering critique); corrections folded in and marked like the daemon plan's red-team notes (see §Red-team reconciliation).
**Goal:** Kill the terminal. Turn the shipped daemon (Slices 1–5) + the v1a shell into **REEL ONE — the screening room**: the gate screens (plan / script / storyboard / animatic) and the eye-gate, where Sean judges animation *in the medium* — running the loop, calling "print it," watching the next picture come up. The frame is the only lit object in the room; chrome recedes when idle and returns when reached for.
**Milestone contract:** v1b binds to the **CONVERGED daemon exactly as it stands** (read endpoints + `202 {job_id}` gate POSTs + `next_action`). The eye-gate ships **approve/retry with the full instrument engine** (rock/flip, cel-flip, onion, diff-wipe, lights-out, hover-skim, the keyboard state machine) but **no annotation layer** (D1) — annotation, the brainstorm room (D2), and chat (D3) are v1c. This is "the working demo — the terminal is dead."
**Architecture:** REEL ONE is a *re-skin + extend* of the v1a React app, not a rewrite. v1a already ships a two-route `react-router` shell, a typed daemon client, the `nextAction` CTA spine, and an MSW test seam — all kept. The work concentrates in (a) a REEL ONE design-system layer over `tokens.css`, (b) the net-new Run Overview + gate screens + the eye-gate, and (c) one shared job-poll flow every mutating surface reuses.
**Model split** (from the tracker / v1.1 addendum): the **eye-gate interaction engine is Fable 5** (the interaction density is the hard part — the daemon reads are trivial); everything else is **Opus 4.8 / Codex**.

---

## Global Constraints

Copied from the build tracker's "standing discipline," the daemon plan, and the v1b mandate. Every unit's kickoff implicitly includes this section.

- **New code only under `web/`.** `server/`, `pipeline/`, and `evals/` stay **byte-identical** — v1b is a pure frontend milestone that consumes the shipped daemon. If a screen turns out to *need* a backend change, that is a **named daemon delta** (see §Daemon deltas), scoped and deferred — never smuggled into a UI unit.
- **The two md5 guards do not move:** `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4`; `pipeline/agents/prompts/sean-screenwriting-voice.md` = `945af824fa53b948a18ac6bf206d67ef`. No UI unit touches either file; each unit's verification re-checks both.
- **Browser-first. No Electron/Tauri until v1b is proven** (spec + tracker decision). The desktop sidecar shell wraps the browser app *after* the screening room works, not before.
- **Credential-free, MSW-mocked tests.** Every unit's tests run against MSW handlers over the daemon contract — **no live daemon in CI**, no model, no spend. `cd web && npm run test`. The final "does it look right against real runs" check is **Sean's browser eyeball** (`ANIMA_RUNS_ROOT=<repo>/runs uvicorn server.app:app` + `cd web && npm run dev`) — UI units stop green on tests+build; the eyeball is a human step.
- **Commit per task; `web/.gitignore` before `git add`** (node_modules/dist/*.tsbuildinfo). An interrupted v1a session left `web/` uncommitted — don't repeat.
- **Fetch latest `main` first** — `git fetch origin && git reset --hard origin/main` before writing code (the stale-clone trap bit a prior worktree).
- **The dual-Vite typing gotcha holds** (tracker gotcha #4): keep `defineConfig` + `type UserConfig` from `"vite"` and cast the config `as UserConfig`; never import `defineConfig` from `vitest/config` (re-breaks the `react()` plugin type). The shipped `web/vite.config.ts` already does this — don't undo it.
- **Three cross-cutting contracts are DoD on every unit** (see §Cross-cutting contracts): the **five doctrine states**, the **WCAG 2.1 AA a11y contract**, and the **density design gate** ("what can this screen stop saying?"). A unit that ships the happy path only is not done.
- **Full verification gate + stop green + PR** per unit; do not roll into the next.

---

## The premise, re-verified against the tree

Everything below was confirmed this session by reading `web/src/*`, `server/*`, `tests/server/conftest.py`, and the four REEL ONE mockups. Three source-doc premises needed correcting — flagged inline so the per-unit kickoffs start from truth, not from the kickoff's shorthand.

### What v1a actually is (the foundation we extend)

- **A router already exists.** `web/` ships `react-router-dom@6.30` with two routes: `/` → `Dashboard`, `/runs/:id` → `RunOverview` (`main.tsx` `<BrowserRouter>`, `App.tsx` `<Routes>`). **Correction (verified):** the kickoff says "v1a has no router." It does. The "shell + routing" unit is therefore **extend the existing router** (add gate/eye-gate routes, restyle the shell), *not* stand one up. This shrinks the shell unit materially.
- **`Dashboard` is fully built** with all five doctrine states (loading skeleton / error+retry / empty / ready grid / never-drop-an-unreadable-run) → **RE-SKIN only**; the state machine survives.
- **`RunOverview` is a 4-line placeholder** (`<section><h1>Run</h1></section>` — no `useParams`, no fetch) → **the booth board is a NET-NEW build**, not a re-skin. The data contract (`fetchStatus` → `RunStatus`/`FrameState`) already exists to feed it.
- **`useResource` does not poll** (one-shot fetch per dep change; retry = bump a nonce). **Live status during generation + job polling is net-new** — the shared job-poll hook (Unit 3) either extends `useResource` or adds an interval hook.
- **`nextAction.ts` (`nextActionCta`) is the CTA spine** — pure, tested, maps each `NextActionKind` → `{label, tone: act|wait|done}` with crew-named microcopy ("Maya is planning", "Flo is drawing F04"). **KEEP.** REEL ONE's screening-room vocabulary layers *on top of* it (it is the phrasing, not the logic).
- **The dark-stage tokens exist but are unused and cooler than REEL ONE's booth** (`--st0 #15161a` cool-charcoal vs REEL ONE `--booth #141018` warm-black/aubergine). So the design-system unit **replaces/extends** the dark tokens with the booth palette + the tungsten/screenlight/bakelite/print/hold set + the lit-page set — it does not merely "activate" what's there.
- **The MSW test seam is production-quality** (`test/setup.ts` errors on any unmocked fetch; `test/handlers.ts` + `test/fixtures.ts` shaped on the live projection; `test/render.tsx`'s `renderApp(ui,{route})` over `MemoryRouter`). **KEEP verbatim; extend fixtures/handlers per unit.**
- **The Vite dev proxy already forwards `/runs`, `/health`, `/jobs` → `127.0.0.1:8000`** — the client can poll `/jobs` for the job layer with **no config change**.

### What the daemon actually serves (the binding surface, Slices 1–5)

Confirmed against `server/routers/*` + `server/state_view.py` + `server/artifacts.py`:

| The screen needs… | Endpoint(s) | Served? |
|---|---|---|
| Run list + each run's stage + `next_action` | `GET /runs` → `run_summary[]` | ✅ |
| A run's status: stage, `next_action`, `frames[]`, `active_job` | `GET /runs/{id}/status` | ✅ |
| Full raw state incl. `plan.cost_estimate{low,median,high,by_phase}` | `GET /runs/{id}` | ✅ |
| Gate artifacts: plan / brief / script / beats / storyboard / shots | `GET /runs/{id}/artifacts/{kind}` (6 fixed kinds) | ✅ |
| Frame attempts + Em/T1 verdicts | `GET /runs/{id}/frames/{n}/candidates` | ✅ |
| Frame image bytes per attempt (or approved) | `GET /runs/{id}/frames/{n}/image?attempt=K` | ✅ |
| Approve/retry/lock gate actions | 7 POST gates → `202 {job_id}` | ✅ |
| Poll a job to terminal (`state`, `rc`, `logs`, `fresh_state`, `next_action`) | `GET /jobs/{id}` (+ `POST /jobs/{id}/cancel`) | ✅ |
| Single-writer / in-flight signal | `active_job` + `next_action.blocked_by_job` on `/status` | ✅ |

**The Em verdict shape** (verbatim from `make_generate_run`, the eye-gate's core payload), one record per cast namespace, nested inside each attempt of `/candidates`:
```
{ "frame":"DEMO_F01", "character":"sean", "verdict":"flag"|"pass"|"human_review (empty-cites invariant)",
  "confidence": 0.8 | null, "cites":["IR.sean.style.line-weight"], "patches":0,
  "proposed_patches":[{"target","path","value","rationale"}], "reasoning":"line weight drifts on the arm",
  "notes":"em@phase_5_generate frame=DEMO_F01 (gemini)" }
```
Attempt index is the linkage; **there is no timecode field** — timecode is derived client-side (`TC = frame_index × hold @ 12 fps`). (The mockup hardcodes per-loop offsets `+00/+02/+04` rather than this formula; the formula is the real derivation, not a mockup transcription.)

### "Zero daemon deltas" — corrected to "no blockers, but not zero"

The exploration README claims REEL ONE needs **zero** daemon deltas for v1b. Verified against the tree (and hardened by the red-team pass), that's **too strong** — the honest verdict is **no blockers, but not zero.** Everything *visual and interactive* is served; the review flow (list → open → read each gate artifact → eye each frame's attempts + Em → approve/retry → poll the job) is fully covered. But **ten gaps** surfaced (§Daemon deltas G1–G10) — none a blocker, all handled in v1b by client-derivation, a scope-narrowing, or an omit. The ones that shape scope: **(G1)** no actual cost-spent accumulator anywhere (the box-office "spent $0.28" is unbacked); **(G2/G7)** in-UI storyboard curation *and* document-gate send-back/reject are not daemon actions (the daemon serves only `approve`); **(G3)** animatic rough-upload/display isn't served; **(G9)** the Bible anchor image isn't served (so eye-gate diff drops candidate-vs-anchor); **(G8)** no `injected_plates`/provenance record (the recipe strip has no data). The mockups are drawn slightly ahead of the shipped `approve`-only backend in three places (G2/G3/G7). This correction is the plan's most important finding and drives the open decisions below. **No delta is a prerequisite for starting v1b** — each is a named v1c/v2 promotion.

---

## Architecture decisions — resolved

These were the crux calls. Each resolves a fork with the finding + the decision + a red-team note, in the daemon-plan style.

### D-A — Design-system layering: extend `tokens.css`, commit to the dark booth

**Decision:** add a REEL ONE layer — `web/src/styles/reelone.tokens.css` (the booth palette + type scale + the lit-page set) and `reelone.motion.css` (keyframes + reduced-motion) — **extending** `tokens.css`, not replacing it wholesale. The v1a warm-paper tokens stay defined (v1a Dashboard's re-skin still uses warm accents sparingly, and the reading-gate's lit page *is* a warm-cream surface), but **REEL ONE commits to the dark booth as the room**: the shell, overview, gates-chrome, and eye-gate all render on `--booth`. The one warm surface is the **lit continuity page** (the document-gate reading pane) — a sheet of paper in a dark booth, its own `--page*` tokens.

**Why:** the booth *is* the identity ("cinematic-dark, not IDE-dark"). A light mode would break the metaphor. The a11y contract's *principles* carry, but its specific contrast pairs (`--teal` on paper, `--ink-3`) are v1a's — **U0's DoD re-verifies every ratio against the booth palette** (screenlight/text on booth ≥ 4.5:1; tungsten focus ring ≥ 3:1; the reading page keeps its own ink-on-cream ratios). Not a copy of the a11y numbers — a re-derivation.

**Red-team note (folded):** *don't* delete the warm tokens — the reading page needs them and the Dashboard re-skin reads cleaner keeping one warm accent for "your move." Extend, don't replace.

### D-B — The shell + "where the room disappears"

**Decision:** the summonable-HUD / idle-wake mechanism (idle 3s → chrome fades → the booth goes dark; any input wakes it) is a **shell-level provider** (a `BoothShell` / `HudHost` around the routed `<main>`), but **each screen declares its dim level**. The eye-gate opts into **full idle-dark** (the signature; lights-out `L` is its deliberate inverse). The overview and document gates use the density mandate — **default = the art + the one decision; secondary panels (crew stations, legends, recipe, cost detail) reveal on intent (hover/keypress)** — but do **not** timed-fade their own primary content (you shouldn't have a plan you're reading dim itself). The `⌘K` command palette is a shell capability too.

**Why:** the mandate ("show, don't tell") is universal; the *aggressive* idle-dark is the screening room's move and is wrong on a page you're reading. Scoping the timed dark to the eye-gate keeps the metaphor honest. (This is the "how hard to push the HUD" open decision — see §Open decisions; recommendation baked in here.)

### D-C — The job-poll pattern (the load-bearing shared unit)

**Decision:** one reusable hook — `useGateAction(runId, action)` — that every mutating surface (all four gates + the eye-gate's print/again) shares. The daemon's `202 {job_id}` + `GET /jobs/{id}` maps *exactly* onto REEL ONE's **Academy leader** as the working state. **The 409 is two distinct failures with two body shapes** (red-team BLOCKER — the gate router raises `{active_job_id, reason}` (dict) for a busy run but a plain **string** detail for a stage mismatch); the hook MUST branch on them or a stale tab offers "watch a job" pointing at nothing:

```
useGateAction(runId, gateAction):
  1. POST the gate.
       202 {job_id}                     → begin polling.
       409 with detail.active_job_id     → "the booth is busy" (doctrine-state-5); surface active_job, offer "watch it".
       409 without active_job_id (string) → STALE/wrong-stage error ("this run already moved on — refresh").
                                            (Two tabs, or a cascade advanced the stage mid-poll.)
       422 (bad/empty note) / 404 (gone) → error doctrine-state; show the reason.
  2. Poll GET /jobs/{job_id} on an interval (~1s). Render RUNNING as the countdown LEADER
       — a client-side 3-2-1 ritual timer, NOT a real ETA (the daemon gives only running/terminal
       + tailing logs; there is no progress %). The leader loops until the job goes terminal.
  3. Terminal:
       SUCCEEDED — advance ONLY on the full success shape:
                   state=="succeeded" && rc===0 && !load_error && fresh_state && next_action.
                   Then use the INLINE fresh_state + next_action (no extra /status round-trip to navigate).
       succeeded-but-degraded (rc===0 yet load_error set / fresh_state null): the job ran but the
                   post-job state reload failed → show a reload/error state + re-fetch /status, do NOT auto-advance.
       failed (rc!=0): surface job.rc + the job.logs tail HONESTLY ("the take jammed in the gate"
                   + the log + Retry) — never a fake success, never a silent swallow.
       cancelled:  return to the gate.
  4. While active_job owns the run, next_action carries blocked_by_job → DISABLE the mutating control
     (prevents the double-fire the cascade overlay guards against).
```

**Why:** the daemon already solved the hard concurrency problem (atomic slot reservation, the cascade overlay, `blocked_by_job`); the UI's whole job is to *render* it faithfully. Unit 3 builds this hook + proves it on the Plan gate; Units 4 and 5 reuse it verbatim. This is the reusable client flow the kickoff asked to spell out.

**Race-safety — stated at the daemon's exact strength (red-team correction):** `blocked_by_job` + the 409 make the daemon's **daemon-vs-daemon** single-writer guard visible; they do **not** protect **CLI-vs-daemon** (the daemon can't lock `pipeline/run.py` — it stays byte-identical). Surface the 409/busy UI, but don't sell it as global single-writer safety — CLI-vs-daemon is the fleet-ops "one owner" operational rule.

**Red-team note (folded):** the leader is **not** a progress bar — binding it to a fake ETA would lie. It is a ritual timer that resolves on the real terminal signal. If the job outlives the leader's 3-2-1, the leader holds on the last count (or loops the sweep) until terminal — it never "completes" ahead of the job.

### D-D — State management: stay hand-rolled + a run-scoped context

**Decision:** no state library. v1a is deliberately hand-rolled (no Redux/Zustand/React-Query); keep it. Add a small **run-scoped React context** (the current `RunStatus` + the active-job/poll state) so the overview, the active gate, and the eye-gate share one source of truth per run without prop-drilling, and **extend `useResource` with a polling variant** (`usePolledResource` / an interval option) rather than importing a data library. The typed `api/types.ts` contract stays the single mirror of the daemon.

**Why:** the surface is small and the daemon is the source of truth; a data-fetching library would be weight without payoff and would fight the MSW seam. Minimal, testable, consistent with the existing code's grain.

### D-E — The eye-gate is a client-side instrument over reads (confirmed)

**Decision + verification:** every eye-gate *mode* is client-side over already-served data — **no backend call beyond the existing reads + the two gate POSTs** — **with one narrowing (red-team):** the diff/compare mode is **attempt-vs-attempt or candidate-vs-approved-prior**, both served via `?attempt=K`; **candidate-vs-anchor is dropped for v1b** because the character anchor (`characters/{id}/anchor.png`) lives outside `run_dir` and the image endpoint is `run_dir`-confined — it is served by nothing (§Daemon deltas G9). Confirmed per mode: rock/flip + cel-flip + lights-out + onion-skin + diff-wipe + hover-skim are canvas/CSS overlays over `/frames/{n}/image?attempt=K` and `/candidates`; `chain_from` (loop-return onion) comes from the `shots` artifact (raw **YAML** — U5 needs a client YAML parser + YAML MSW fixtures); the Em read-out renders the `/candidates` verdict payload as-is; print/again are `POST …/approve` / `POST …/retry`; auto-advance reads `next_action`. **v1b sends `{note}` only** on retry — the `annotations` field is D1/v1c. This is what makes the eye-gate a **Fable** unit: the interaction density is the whole build.

### D-F — Storyboard curation scope (the mockup is ahead of the backend)

**Finding:** the REEL ONE reading-gate mockup shows a "slate stack — cut · strike · reorder" with "your strikes survive on the report." But the daemon serves **only `POST /storyboard/approve`** (re-validate the on-disk `shots.yaml` + lock); **`mutate` is CLI-only** — there is no in-UI cut/reorder/add-shot endpoint.

**Second finding (red-team BLOCKER — G7):** there is **no reject / send-back gate action at all.** `server/gates.py:GATE_SPECS` carries only `--approve-*` args; the only other write is frame `retry`. So "send back to Maya/Sam/Bea" is **not a daemon action** on *any* document gate (plan, script, storyboard) — the mockup's send-back note has no endpoint.

**Decision (v1b):** every document gate ships **review-the-artifact + approve/lock** only. There is **no send-back button** in v1b (removing the mockup's implied one) — "not ready?" is handled by re-running the stage on disk via the CLI, then re-reading. Storyboard specifically = render Bea's board + lock via `approve` (which enforces coverage + cast-conflict + `--frames N` count and *refuses a failing board with a named reason*). **In-UI curation (cut/reorder/add) is a named delta** (§Daemon deltas G2) and **in-UI send-back/reject is a named delta** (§Daemon deltas G7), both deferred to v1c; until then curation + re-runs happen on disk (the current CLI workflow), then lock. → **Open decision** (build the send-back/mutate deltas into v1b, or narrow — recommendation: narrow to approve/lock only).

### D-G — Animatic gate scope (opt-in, and rough I/O isn't served)

**Finding:** animatic roughs are dropped by the human into `runs/<id>/animatic/` on disk and ingested by `POST /animatic/approve` (deterministic, no model, no spend). There is **no rough-upload endpoint and no rough-display endpoint** — the daemon can neither receive a drag-dropped PNG nor serve one back.

**Decision (v1b):** the animatic gate ships **thin** — it appears in the stepper only when `state.animatic_enabled`, shows the placement-gate status + holds, and offers **"Ingest & generate"** (`POST /animatic/approve`) + **"Skip."** Roughs are placed on disk (CLI workflow); **in-UI drop-upload + thumbnail display is a named delta** (§Daemon deltas G3). Given animatic is opt-in and off by default, a thin gate is honest and sufficient for v1b. → **Open decision** (thin gate vs defer the animatic screen entirely — recommendation: thin gate, it's cheap and completes the stepper).

### D-H — Cost ledger honesty (the box office)

**Finding:** cost **estimate** is served (`GET /runs/{id}` → `plan.cost_estimate`); cost **actually spent** is **tracked nowhere** in `pipeline/` or `server/`. Per-frame price isn't served either (but every orchestrator frame is `standard_keyframe → NB2 → $0.07`, a safe v1 constant).

**Decision (v1b):** the box office shows the **estimate** truthfully (low/median/high + by-phase, from `plan.cost_estimate`) and a **client-derived "spent so far"** = `Σ recorded attempts × $0.07`, **explicitly labelled as a derived running total, not a live meter.** A real spend accumulator is a named backend follow-on (§Daemon deltas G1) — it ties to the museum's cost-evidence story, so it's worth filing, but it does not block v1b. The per-frame `NB2 · $0.07` burn-in is a documented v1-only constant (tier-honesty is D4/v2).

**Red-team note (folded):** label the derived spend so the screen never *claims* a precision it doesn't have — an honest "≈ $0.28 drawn" beats a false "$0.28 spent." This is the density mandate applied to numbers: show what's true, don't tell a number you can't stand behind.

---

## File structure (web/ additions)

All new files under `web/src/`. One responsibility per file; the v1a spine is kept.

```
web/src/
├── styles/
│   ├── tokens.css                 # KEEP + EXTEND (warm tokens stay; reading-page uses them)
│   ├── reelone.tokens.css         # NEW (U0): booth/tungsten/screenlight/bakelite/print/hold + page-set + type scale
│   ├── reelone.motion.css         # NEW (U0): @keyframes flicker/weave/fade-through-black/leader-sweep/circledraw/pulse
│   │                              #            + the steps(1)@83ms loop cadence + the reduced-motion collapse block
│   └── app.css                    # RE-SKIN (per-screen splits as it grows)
├── booth/                         # NEW (U1): the room
│   ├── BoothShell.tsx             #   film-grain overlay, warm-black chrome, the routed <main> host
│   ├── HudHost.tsx                #   the summonable-HUD / idle-wake provider (per-screen dim level)
│   └── CommandPalette.tsx         #   ⌘K jump-to-run/stage/action (scaffold in U1; wired as screens land)
├── reelone/                       # NEW (U0): the signature components (design-system primitives)
│   ├── FilmGrain.tsx  Lamp.tsx  Leader.tsx  CircledTake.tsx  Timecode.tsx  BurnIn.tsx  Filmstrip.tsx
├── lib/
│   ├── useResource.ts             # KEEP
│   ├── usePolledResource.ts       # NEW (U3): the interval/poll variant
│   ├── useGateAction.ts           # NEW (U3): POST→202→poll-leader→terminal→advance (the shared job flow)
│   ├── nextAction.ts              # KEEP (the CTA spine)
│   ├── timecode.ts                # NEW (U0): TC = frame_index × hold @ 12fps
│   └── runContext.tsx             # NEW (U3): run-scoped context (status + active-job/poll state)
├── api/
│   ├── client.ts   types.ts       # KEEP + EXTEND: postGate*, fetchJob, fetchCandidates, fetchArtifact, fetchRawState
├── screens/
│   ├── Dashboard.tsx              # RE-SKIN (U2): the booth marquee
│   ├── RunOverview.tsx            # REPLACE (U2): the booth board (reel of stages + now-screening + box office + crew)
│   └── gates/                     # NEW: the document-gate family (U3/U4) + the eye-gate (U5)
│       ├── GateShell.tsx          #   the reusable lit-page gate frame (U3)
│       ├── PlanGate.tsx           #   U3 (proves the shared pattern + cost-preview)
│       ├── ScriptGate.tsx         #   U4 (script|beats toggle)
│       ├── StoryboardGate.tsx     #   U4 (review + lock; curation narrowed — D-F)
│       ├── AnimaticGate.tsx       #   U4 (thin, opt-in — D-G)
│       └── EyeGate.tsx            #   U5 (Fable — the instrument)
└── test/                          # KEEP the seam; each unit adds fixtures + handlers
```

---

## Screen ↔ binding map (the surface, per screen)

Each surface: its REEL ONE name, the exact daemon bindings, the **default (show)** vs **on-intent (tell)** split (the density mandate), and the doctrine states that matter most.

| Screen (REEL ONE name) | Bindings | Default — the art + one decision | On intent (hover/key/idle) | States that bite |
|---|---|---|---|---|
| **Dashboard** — the marquee | `GET /runs` | Each run as a card: slug, stage, the one next move (`nextActionCta`). | stub tag, `updated_at`. **In-flight badge needs a per-card `/status` fan-out** (`run_summary` carries no `active_job` — G10) → on-hover only, or accept N calls. | empty (invitation), error+retry, unreadable-run-not-dropped |
| **Run overview** — the booth board | `GET /runs/{id}/status` + `GET /runs/{id}` (raw, for `cost_estimate` **+ `needs_storyboard`/`animatic_enabled` to derive the stepper's stage set**) + poll `/jobs/{id}` | The reel of stages (leader segments) + the **now-screening** hero (current `next_action`, one primary action) + the mini frame-reel. | box-office detail (per-frame ledger), **crew stations** (hover a stage → whose hands, a client-side stage→agent constant map), revisit a printed stage. | working (cascade: named agent + leader), busy (409), error |
| **Plan gate** — the read | `GET …/artifacts/plan` + `GET /runs/{id}` (`cost_estimate`) + `POST …/plan/approve` | Maya's plan as a lit page + the primary "Approve — print it" (⌘⏎) + "estimate, not a cap." | the by-phase cost breakdown, "nothing burns until you approve." **(No send-back — not a daemon action, G7.)** | working ("Maya is costing…"), approved→cascade, error |
| **Script gate** — the read | `GET …/artifacts/{script,beats}` + `POST …/script/approve` | Sam's `script.md` as a screenplay page + approve. | the **Script ⇄ Beats** toggle (instant). **(No send-back — G7.)** | working ("Sam is drafting…"), back-compat skip |
| **Storyboard gate** — the continuity report | `GET …/artifacts/{storyboard,shots}` + `POST …/storyboard/approve` | Bea's board read aloud (the lit page) + the shot slates + **"Lock picture" (⌘⏎)**. | per-slate intent/beat link, the validation reason on a refused lock. **(cut/reorder + send-back = deferred deltas — G2/G7)** | invalid-lock (names gap + fix), working |
| **Animatic gate** — placement (opt-in) | `POST …/animatic/approve` | *thin:* placement status + holds + **"Ingest & generate" / "Skip."** | which frames still need a rough (from state). **(drop-upload/display = deferred delta — D-G)** | off (absent from stepper), empty ("drop a silhouette per frame") |
| **Eye-gate** — the screening | `GET …/frames/{n}/candidates` + `…/image?attempt=K` + `GET …/artifacts/shots` (chain_from) + `POST …/frames/{n}/{approve,retry}` + poll `/jobs/{id}` + `GET …/status` | **The frame, lit, alone** + the one decision (print ⏎). Em's one card (verdict lamp + reasoning). | takes 1/2, onion `O`, diff `D`, run `Space`, lights `L`, recipe strip, provenance line, `?` cheat-sheet — all summoned, none permanent. | all five, tight (generating→verdict→your eye→retry→approved→cascade→busy) |

---

## The REEL ONE design system (U0 — name the layers)

Pulled from the four mockups' inline CSS/JS. **Name what is a token, what is a motion primitive, what is a component** — so the builder knows where each thing lives.

### Tokens (`reelone.tokens.css` `:root`)
- **Booth surfaces:** `--booth #141018`, `--booth2 #1D1722`, `--booth3 #251E2B`, `--line #332A3C`.
- **Light:** `--tungsten #E8B36A` (the practical/accent), `--tungsten-dim #8A6F4D`, `--screenlight #FFF6E4` (the lit frame / display text).
- **Lamps (semantic, reserved):** `--print #7FA96B` (approve/PRINT), `--hold #D9A441` (Em HOLD/amber), `--bakelite #C24838` (the projector button / retry). Em's margin mark keeps a **single reserved warning hue** — the two-reds rule (below) protects it.
- **Text:** `--text #DDD5E0`, `--mute #8F8798`.
- **The lit page (reading-gate only):** `--page #F7EFDC`, `--page-ink #2B2417`, `--page-ink2 #57503F`, `--page-rule #C9BB98`.
- **Type scale:** Futura (SMPTE-leader face — display numerals, tracked caps), SF Mono/Menlo (timecode, burn-ins), Georgia (the lit continuity page only). *Note:* v1a self-hosts fonts via `@fontsource`; U0 sources Futura-equivalent + confirms licensing, or falls to the mockup's stack (`"Futura","Avenir Next","Helvetica Neue"`). **Open detail for U0** — don't block on a webfont; the fallback stack ships.
- **Reuse** v1a's spacing/radius scale (4px base) unless the booth needs its own.

### Motion primitives (`reelone.motion.css` — keyframes + utility classes; JS-driven where noted)
- `flicker` — opacity 1 ↔ .986 (the print flicker, ~1.5%).
- `weave` — sub-pixel translate jitter (the gate weave while the loop runs).
- `fade-through-black` — the universal arrival transition ("motion is projection, not transition").
- `leader-sweep` — the 3-2-1 clock-sweep countdown (driven by a `--sweep` deg via `requestAnimationFrame`; **the loading state**, wrapped by `<Leader>`).
- `circledraw` — `stroke-dashoffset → 0` (the circled take on approve; wrapped by `<CircledTake>`).
- `pulse` — the working indicator (0.5 ↔ 1 opacity).
- **The loop cadence** — `steps(1)` at **83 ms** (12 fps stepped), driven by the rock/flip JS (not a CSS animation — it's `Space`-controlled).
- **The reduced-motion collapse block** (a11y, DoD): loop → freeze/single-step; cel-flip → ≤1-opacity crossfade (never a dead cut); leader → skip to done; weave/flicker → off; circledraw/ship-flourish → instant. Scope `reduce` to `animation` + long transitions so hover/press feedback survives.

### Components (`reelone/` — React primitives)
`<FilmGrain>` (fixed grain overlay, `aria-hidden`) · `<Lamp verdict>` (PRINT/HOLD/fail semantic lamp — a lit signal *before* a word) · `<Leader onDone>` (the countdown — a controlled component; **every job's working state reuses it**) · `<CircledTake>` (the approve flourish) · `<Timecode frame hold>` (burn-in; `lib/timecode.ts`) · `<BurnIn>` (the `12 FPS · NB2 · $0.07` model+cost line) · `<Filmstrip frames>` (the reel ledger). Shell primitives (`<BoothShell>`/`<HudHost>`) live in `booth/` (U1).

**U0 DoD adds:** the a11y contrast re-verification against these tokens (§Cross-cutting), a `/dev/system` reference route rendering the palette/type/lamps/leader/circled-take (demoable, testable), and component tests for `<Leader>` (fires `onDone`), `<Lamp>` (semantic aria), and `timecode.ts`.

---

## The eye-gate interaction engine (U5 — the hard unit, Fable 5)

The one keystone screen and the reason Fable builds this unit. Spec'd in the most detail because its per-unit kickoff carries the most risk. **The spec addendum (the R1/R2 ratified picks) is authoritative for the mode + key set; the `reelone-eyegate.html` mockup is a *visual-behavior reference* for the modes it implements — it is a partial prototype.** (Its real `keydown` switch covers only `Enter, r, o, d, l, Space, 1, 2, [, ]`; it has **no** `↑`/`↓`, `?`, hover-skim, real onion-of-approved-N-1 — it toggles a static ghost — no diff-vs-anchor, and its `print()` is a demo reset, not auto-advance-skipping-approved.) So Fable builds the *modes the mockup doesn't cover* **from the spec**, styled to the mockup. Everything here is client-side (D-E).

### The vocabulary map (mockup ⇄ behavior spec)
REEL ONE renames the actions; the builder binds screening-room words to spec behavior: **print = approve**, **again = retry**, **take = attempt**, **run/rock = the `Space` loop**, **ghost = onion-skin**, **wipe = diff/compare**, **lights = lights-out**, **the leader = the working state**, **circle the take = the approve flourish**, **box office = the cost ledger**, **back row = Em**, **the reel = the frame ledger/filmstrip**.

### The instrument modes
- **Rock/flip (`Space`, hold):** run the short loop at **12 fps stepped (83 ms, `steps(1)`)** with a breath of gate weave; release **freezes on the current frame**. Hand-controlled — hold to rock, let go to judge. *"The illusion of motion only appears in the rock — the load-bearing addition."* Drives the mascot idle→look→alert keys.
- **Cel-flip advance:** on print, the **next unreviewed frame** arrives (spec: 260 ms slide from the right; dressed as REEL ONE's "next picture up" — circle-the-take → leader → fade-through-black → new frame). `⏎` approves **and** advances, **skipping already-approved frames** (reads `next_action`).
- **Onion-skin (`O`):** ghost the approved **N-1** (and **frame 1 for a loop-return**, read from `chain_from` in the `shots` artifact — a raw-YAML parse, see D-E) under the candidate at low opacity — judge whether the character *holds* and the loop closes. **Two-reds rule (a re-derivation of spec R2):** R2 ratified "previous = cool-desaturated, next = teal-bright," but REEL ONE has no teal — so the ghost renders **cool/tungsten-dim, never in a lamp hue** (print-green/hold-amber). One reserved warning hue on the stage; the lamp semantics stay unambiguous. (Deviation from R2's literal token, noted.)
- **Diff/compare (`D`, `[`/`]`):** a wipe between **two attempts, or candidate-vs-approved-prior** (both served); `[`/`]` drag the wipe line; highlights identity drift (the "face morphed through the tween" catch — the failure DINOv2 misses and the eye doesn't). **Candidate-vs-anchor is not in v1b** — the Bible anchor isn't served (D-E, G9).
- **Lights-out (`L`):** drop **all** chrome; the frame (or the running loop) alone on the dark stage. The one-key "see it as it ships" (Procreate Dreams' four-finger preview, keyboardized). `L` again restores.
- **Hover-skim:** hovering a reel cell **peeks that frame on the stage without moving the current frame** (the FCP skimmer) — a mouse convenience; the keyboard equivalent is `↑↓`.

### The keyboard state machine (every key — v1b set)
`⏎` print (approve shown take → cel-flip to next unreviewed) · `R` open the retry note **prefilled from Em** + **auto-pause the loop** (`⏎` sends, `Esc` cancels) · `↑`/`↓` walk frames · `1`/`2`/number switch takes (also click) · `Space` rock the loop (hold) · `O` onion · `D` diff · `[`/`]` drag the wipe · `L` lights-out · `?` cheat-sheet overlay · `⌘K` command palette.
**Not an eye-gate key (red-team NIT):** `⌘⏎` belongs to the **document gates** (Approve/Lock picture), not here — the eye-gate's only stage boundary (last-frame approve → assemble) **auto-cascades**, so there's no user-facing gate-approve on this screen; `⏎` (print) is the only commit key. **Excluded from v1b:** `P` (keyboard-pin annotation) — that's the D1/v1c annotation layer. **State rules:** typing in any note auto-pauses the loop; keys ignore `INPUT` targets; **every key has a visible stage-toolbar button** (a11y discoverability).

### Em as a hand in the margin (the read-out)
Four fixed labelled slots beside the frame — **verdict · reasoning · proposed fix · cites** — rendering the `/candidates` Em payload as-is. Verdict as a **`<Lamp>` before a word** (PRINT green / HOLD amber / fail — the show-don't-tell amplifier). The proposed fix (`proposed_patches[].{target,path,value,rationale}`) **pre-fills the retry note, attributed "prefilled from Em"** — accept in a keystroke or edit. Her honest boundary is stated in-context: **"she reads stills, not motion — the loop is yours."** (For videos/motion the daemon reduces to a contact sheet; the eye-gate honors the same blind spot.)

### Provenance line + recipe strip — what's real in v1b (red-team G8)
The **provenance line** ("drawn by Flo (NB2) · read by Em · your call") ships — but it is **client-composed from constants + the verdict**, not a served record: Flo is the only generator in v1, `NB2` is the G5 constant, "read by Em" is true iff the attempt carries an Em verdict, "your call" is always last. The **recipe strip** (injected plates) is different: `/candidates` serves **no** `injected_plates` / prompt / route / provenance record (§Daemon deltas G8), so the recipe strip has **no data in v1b — it is omitted** (it returns with D6 in v2). Don't render a strip with invented contents; ship the honest provenance line, drop the recipe strip.

### The show-don't-tell amplifiers (Fable named these — bake into DoD)
- **Verdicts as lamps before words** — `<Lamp>` lights PRINT/HOLD before the reasoning text is read.
- **The job cascade as the Academy leader** — the 3-2-1 countdown *is* the working state (D-C), not a spinner; the next picture comes up through it.
- **Cost as one burn-in line** — `12 FPS · NB2 · $0.07`, a single mono line, never a panel.
- **The summonable HUD** — booth dark ~3s idle; the decision and the frame are the only permanent things.

### Client-side vs backend (confirmed — no backend beyond the shipped reads)
All modes are overlays over `/image?attempt=K` + `/candidates`; `chain_from` from the `shots` artifact; auto-advance from `next_action`; print/again are the two shipped gate POSTs; the leader is a client timer over `/jobs/{id}` running/terminal. **The only thing v1b deliberately omits is the `annotations` retry payload (D1).**

---

## Unit decomposition, sequencing, and model tiers

Six demoable increments (U0→U5), sequenced so each lands a visible slice and no backend runs ahead of its consumer. Each is a **titled stub — designed here, its TDD kickoff written JIT.** Model tier per the tracker split.

Legend for each unit: **Goal · Bindings · Demo · MSW seam · DoD adds · Model.**

### U0 — REEL ONE design-system extraction · **Opus/Codex**
- **Goal:** the token + motion + component layer (§The REEL ONE design system). Names locked; the booth and lit-page surfaces tokenized; the signature primitives (`<Leader>`, `<Lamp>`, `<CircledTake>`, `<FilmGrain>`, `<Timecode>`, `<BurnIn>`, `<Filmstrip>`) built and unit-tested.
- **Bindings:** none (pure presentation).
- **Demo:** a `/dev/system` reference route (palette · type · lamps · a live leader · circled-take) — the living token sheet.
- **MSW seam:** none needed; component tests + a11y assertions.
- **DoD adds:** contrast re-verified against the booth palette (the a11y numbers, re-derived); reduced-motion collapse implemented; `<Leader onDone>` fires.
- **Foundation — everything downstream imports it.**

### U1 — The booth shell + routing + the HUD host · **Opus/Codex**
- **Goal:** re-skin `App.tsx`/`AppHeader` into the booth chrome (wordmark, film grain, warm-black `<main>`); add the routes for the gates + eye-gate; build `BoothShell`/`HudHost` (the idle-wake / summonable-HUD provider, per-screen dim level — D-B) + the `⌘K` palette scaffold + the shell-level focus-ring + reduced-motion contract.
- **Bindings:** none new (routing over existing screens; Dashboard renders inside, lightly skinned).
- **Demo:** a navigable booth; idle-wake dims/wakes; `⌘K` opens (even if targets are stubbed).
- **MSW seam:** `App.test.tsx`-style shell + a11y landmark tests (extend, keep green).
- **DoD adds:** landmarks (`<header>`, `<nav aria-label="pipeline stages">`, `<main>`); the HUD respects reduced-motion; the router keeps the v7 future flags + the dual-Vite config untouched.

### U2 — Re-skin the Dashboard + build the Run Overview · **Opus/Codex** · **pre-split into two build slices** (red-team: Dashboard is a re-skin, the Overview is a net-new REPLACE — different effort classes, cleaner as two TDD sessions)

**U2a — Dashboard re-skin (the marquee).**
- **Goal:** re-skin `Dashboard` over `GET /runs` — keep the whole state machine + never-drop-an-unreadable-run; only the visual becomes the booth marquee. The "New run" card stays inert ("opens in v1c").
- **Bindings:** `GET /runs`. (In-flight badge is a G10 gap — scope to on-hover `/status` or omit; do **not** claim `run_summary` carries busy.)
- **Demo:** real runs render as the marquee. **MSW seam:** reuse the shipped `/runs` handlers/fixtures.
- **DoD adds:** all five doctrine states (already present — keep green); the density gate (card = slug + stage + the one move; secondary on intent).

**U2b — Run Overview build (the booth board).**
- **Goal:** **net-new** (RunOverview is a 4-line stub): the **reel of stages** (leader segments, revisitable) + the **now-screening hero** (current `next_action`, one primary action) + the **box office** (estimate + derived spent — D-H) + the **crew stations** (hover reveal, a client-side stage→agent constant map) + the mini frame-reel.
- **Bindings:** `GET /runs/{id}/status` + `GET /runs/{id}` (raw — for `cost_estimate` **and** `needs_storyboard`/`animatic_enabled`). **Live-poll is deferred to U3** — U2b reads once + a manual refresh.
- **The Working state without polling (red-team):** U2b renders the Working doctrine state as a **static, one-read visual** — seeded from the single `/status` read (`active_job` present → "Flo is drawing F04" + a **decorative leader that does not self-advance**); it is **not** a `setTimeout` fake and there is **no auto-advance** (both are U3's job). U3 upgrades this to the live polled transition.
- **The stepper's stage set is run-shape-derived (red-team):** the reel omits SCRIPT/STORYBOARD for a back-compat run and ANIMATIC when `animatic_enabled` is false — derived from `needs_storyboard`/`animatic_enabled` (the `state.py` fork map is canonical), mirroring U4's gate-absence rule. Do **not** render a fixed 6-segment reel.
- **Demo:** opening a run shows the booth board. **MSW seam:** extend `fixtures.ts` — a full `RunStatus` + a raw-state fixture with `cost_estimate` + both fork flags; handlers for `/status`, `/runs/{id}`.
- **DoD adds:** all five doctrine states (Working = the static leader, above); the density gate (default = the reel + the one move; box-office detail + crew on intent); the derived-spend label honesty (D-H); the derived stage set.

### U3 — The shared job-poll pattern + the gate shell, proven on the Plan gate · **Opus/Codex**
- **Goal:** build the load-bearing shared unit — `useGateAction` (D-C), `usePolledResource`, `runContext` — and the reusable **`GateShell`** (the lit-page document-gate frame). Prove the whole flow end-to-end on the **Plan gate** (the simplest document gate + its cost-preview differentiator): read `plan.md`, show the cost preview, **Approve → 202 → leader countdown → terminal → advance** (+ the cascade working-state, `blocked_by_job` disable, 409-busy, failed-`rc`/logs honesty). Run Overview adopts the live poll here.
- **Bindings:** `GET …/artifacts/plan`, `GET /runs/{id}` (`cost_estimate`), `POST …/plan/approve`, poll `GET /jobs/{id}`, `GET …/status`.
- **Demo:** approve a plan; watch the leader; land on the next gate. The reusable pattern is proven once.
- **MSW seam:** the **job lifecycle** fixtures — a handler that returns `202 {job_id}` then a `/jobs/{id}` that transitions `running → succeeded`, plus the variants the DoD requires below. This seam is the template Units 4 + 5 reuse, so build it complete.
- **DoD adds (the full job-flow contract — red-team: the 409 is two, and success is conditional):**
  - `202` → poll → **succeeded** (`rc===0 && !load_error && fresh_state && next_action`) → advance on the inline `next_action`.
  - **succeeded-but-degraded** (`rc===0` yet `load_error`/null `fresh_state`) → reload/error state, no auto-advance.
  - **failed** (`rc!=0`) → `rc` + `logs` tail honestly + Retry.
  - **409-busy** (`detail.active_job_id`) → busy state + "watch it".
  - **409-stale** (string detail, no `active_job_id`) → "this run already moved on — refresh".
  - POST **422** (bad/empty note) and POST/job **404** (run/job gone) → error state.
  - `blocked_by_job` on `next_action` → the mutating control is disabled.
  - The leader is a ritual timer, not a fake ETA; the density gate on the gate shell (the plan is the page; cost detail on intent).
- **Note (red-team):** on a *real* run, approve-plan advances to SCRIPT (authoring) or the eye-gate (back-compat) — both unbuilt at U3 — so the demo's "land on the next gate" is aspirational; the **pattern** (POST→poll→terminal→inline `next_action`) is fully MSW-proven regardless. Not a blocker.

### U4 — The remaining document gates · **Opus/Codex** · **pre-split into three build slices** (red-team: three gates with different failure/absence semantics; the Storyboard board-read is the densest, most panel-prone screen in the milestone — don't ship it as a happy-path tail of a triple unit)

All three ride U3's `GateShell` + `useGateAction`, so each inherits the full job-flow contract. **Density gate + the WCAG 2.1 AA a11y contract are DoD on every one** (restated here because this cluster is the most panel-prone in v1b): default = the artifact + the one decision; secondary on intent; real `<button>`s; landmarks; one `<h1>`; the palette-aware focus ring; reduced-motion. **No send-back on any of them** (G7 — not a daemon action).

**U4a — Script gate.**
- **Goal:** Sam's `script.md` as a screenplay page + the instant **Script ⇄ Beats** toggle (over both artifacts) + approve. **Bindings:** `GET …/artifacts/{script,beats}`, `POST …/script/approve`, poll. **MSW seam:** a script/beats fixture pair; reuse U3 job handlers. **DoD adds:** the instant toggle (no reload); back-compat (a run with a `shots.yaml` never reaches this gate); density + a11y.

**U4b — Storyboard gate (the continuity report).**
- **Goal:** render Bea's board (the lit page) + the shot slates + **Lock picture** (⌘⏎); the **refused-lock** state names the gap **and** the fix. Review + lock only — curation + send-back are deferred deltas (D-F, G2/G7). **Bindings:** `GET …/artifacts/{storyboard,shots}`, `POST …/storyboard/approve`, poll. **MSW seam:** a board + shots.yaml (incl. a `chain_from`) + a validation-failure board for the invalid-lock state. **DoD adds:** the invalid-lock state; slates are display-only (no cut/reorder in v1b); density (cut a panel, not shrink it — this is the screen where it bites) + a11y.

**U4c — Animatic gate (thin, opt-in — D-G).**
- **Goal:** appears in the stepper only when `animatic_enabled`; shows placement status + holds + **"Ingest & generate"** and **"Continue without roughs."** Both bind to the **same `POST /animatic/approve`** (Skip is not a separate endpoint — an empty animatic dir proceeds with a warning; red-team NIT). Roughs are placed on disk (no upload endpoint — G3). **Bindings:** `POST …/animatic/approve`, poll. **MSW seam:** an animatic-enabled state fixture. **DoD adds:** the gate is absent when `animatic_enabled` is false (storyboard→generate byte-identical); density + a11y.

- **Demo (U4 whole):** an authoring run walked from plan through the gates to GENERATE in the browser.

### U5 — The eye-gate interaction engine · **Fable 5** · **pre-split into three build slices** (red-team BLOCKER: "the full instrument" — compositing + keyboard SM + onion + diff + skim + lights + Em prefill + job leader + reduced-motion + a11y — is not one red-green slice, and it never defined image cache/error behavior)

The spec addendum (R1/R2) is authoritative for the mode/key set (see §The eye-gate interaction engine); the mockup is a partial visual reference. All three slices are **Fable** (the interaction density is the whole build; the daemon reads are trivial) and all are client-side (D-E). **Cross-slice DoD:** define image behavior explicitly — preload/cache adjacent frames + attempts, and handle a **missing attempt / 404 image / errored fan** as an honest state, not a broken `<img>`; own **keyboard focus** on the stage (the stage is a focusable region; keys ignore `INPUT` targets; `Esc` returns focus from the note).

**U5a — The stage + the Em read-out (static).**
- **Goal:** the dark stage, the lit frame, take 1/2 switching (click + `1`/`2`), the filmstrip/reel ledger, and **Em as a hand in the margin** (verdict `<Lamp>` + reasoning + proposed-fix + cites, from `/candidates` as-is) + the client-composed provenance line (G8). No motion yet. **Bindings:** `GET …/frames/{n}/candidates`, `…/image?attempt=K`. **MSW seam:** a multi-attempt `/candidates` fixture carrying the real Em flag→pass story (`make_generate_run` shape) + a 404-image + errored-attempt fixture. **DoD:** the five states on the stage; the Em read-out is an announced region (grease mark `aria-hidden`, reasoning carries meaning); recipe strip omitted (G8); density + a11y.

**U5b — The keyboard state machine + print/again over the job layer.**
- **Goal:** the key map (`⏎`/`R`/`↑↓`/numbers/`?`/`⌘K`; `Space`/`O`/`D`/`L`/`[]` toggles wired as no-ops until U5c) + **print → circle-the-take → leader → advance** (`useGateAction`) + **again → note prefilled from Em → retry** (`{note}` only — D1 excluded) + auto-advance-skipping-approved (reads `next_action`). **Bindings:** `POST …/frames/{n}/{approve,retry}`, poll `/jobs/{id}`, `GET …/status`. **MSW seam:** reuse U3's job handlers for print/again. **DoD:** every key has a visible stage-toolbar button; the retry note auto-pauses; the full job-flow contract (U3); reduced-motion (cel-flip→crossfade, leader→skip); density + a11y.

**U5c — The instrument modes + polish.**
- **Goal:** rock/flip (`Space`, 12fps stepped/83ms + gate weave), cel-flip advance, onion-skin (`O`, approved N-1 + `chain_from` frame-1, the two-reds rule), diff-wipe (`D`, `[`/`]`, attempt-vs-attempt / candidate-vs-approved-prior — no anchor, G9), lights-out (`L`), hover-skim, the summonable HUD, the amplifiers (lamps-before-words, leader-cascade, cost burn-in). **Bindings:** `GET …/artifacts/shots` (chain_from — raw YAML, needs a client parser + YAML MSW fixtures). **DoD:** reduced-motion (loop→freeze, ship-flourish→static); the diff wipe is *also* a labelled slider; hover-skim doesn't move the current frame; density (all modes summoned, none permanent) + a11y.

- **Demo (U5 whole):** **"the terminal is dead"** — rock a loop, print a take, watch the next picture come up, send one back with Em's note.
- *(Open decision: U5a's Em read-out is "rest-tier" rendering and could be an Opus slice; kept Fable here as the default since it's the stage foundation the Fable slices build on — see §Open decisions.)*

### Sequence — six conceptual units, **eleven build slices** (one TDD session each)
```
U0 design system ─▶ U1 booth shell + routing + HUD
   ─▶ U2a Dashboard re-skin ─▶ U2b Run Overview build
   ─▶ U3 job-poll pattern + gate shell (proven on Plan)      ← the load-bearing shared slice
   ─▶ U4a Script gate ─▶ U4b Storyboard gate ─▶ U4c Animatic gate (thin)
   ─▶ U5a eye-gate stage + Em read-out ─▶ U5b keyboard + print/again ─▶ U5c instrument modes  [ALL FABLE]
        ← "the terminal is dead"
   · Slice 6 (run-create) built JIT only if/when new-run-from-UI is designed (recommend: OUT of v1b — §Slice-6)
```
Each arrow is a merged PR + an independent planning-session review, per the standing rhythm. **U0/U1/U2a can spawn kickoffs now; do the one light revision the red-team asked for (already folded here) before cutting U3** — it is inherited by U4 + U5. Model tier: U5a/b/c = **Fable**; all others = **Opus/Codex**.

---

## Cross-cutting contracts (DoD on *every* unit)

### The five doctrine states
Every **data-bound screen** builds all five, never the happy path alone (the a11y contract makes this explicit; the async `202` poll + the "crew working" leader are first-class, never `setTimeout` stand-ins). **Exempt:** U0 (pure presentation — the `/dev/system` sheet) and U1 (the shell chrome + HUD host) bind no run data, so the five-states DoD applies from U2a onward; U0/U1 still carry a11y + reduced-motion. This keeps the "every unit" language honest.
1. **Empty** — an invitation, not an apology ("Start a new short. Bring a spark and the room opens").
2. **Loading** — a **skeleton of the target screen**, never a spinner-in-a-void.
3. **Working (mid-gen)** — names *which agent* runs + a live poll (the **leader**); logs on tap, not shoved ("Flo is drawing F04…").
4. **Error** — what happened, then **the one recovery action**; no "Error:", no first person; a failed job shows `rc` + the log tail honestly.
5. **Busy (409)** — the run is owned by another action; offer to watch it ("This run is busy. View the running job") — the single-writer rule made visible.

### The a11y contract (WCAG 2.1 AA — re-derived against the booth palette)
Keyboard-first; every clickable is a real `<button>`/`<a>` (never `<span onclick>`); icon-only controls carry `aria-label`; a visible **palette-aware focus ring** (tungsten on booth, ≥3:1; never `outline:none`); landmarks + one `<h1>` per screen; **11px type floor**; toggles carry `aria-pressed`; working states announce via a polite `aria-live` region; provenance is real text, not tooltip-only. **Contrast is re-verified against REEL ONE's tokens, not inherited from v1a's warm pairs.** **Reduced-motion** collapses cel-flip→crossfade (not a dead cut), rock→step, leader→skip, ship-flourish→static — scoped to `animation`/long transitions so hover/press feedback survives. **Every eye-gate key has a visible stage-toolbar button; the `?` cheat-sheet is the discoverability backstop; the diff wipe is also a labelled slider.**

### The density design gate ("what can this screen stop saying?")
The v1b build mandate, treated as a **gate, not a preference** (memory: [[v1b-direction-pick-reelone-show-dont-tell]]). Every unit's review asks it. Rules: **default state = the art + the one decision**; secondary info (critic history, legends, chat, provenance, recipe, cost detail) arrives **on intent** (hover/keypress/idle-wake), never permanently; **prefer a visual signal over a printed label** wherever one exists (lamp > word, motion > description); **when in doubt cut a panel, not shrink it.** Numbers obey it too (D-H: show what's true, don't print a number you can't stand behind).

---

## The Slice-6 decision (flag for Sean)

**Recommendation: Slice 6 is OUT of v1b's first increment.** v1b operates on **runs created via the CLI** (`python -m pipeline.run --brief …`); the daemon has **no `POST /runs`** and no `GET /characters`/cost-estimate endpoint, and building them now would be backend ahead of its consumer (the anti-drift lesson the tracker already applied when it JIT-deferred Slice 6).

- **Consequence if OUT (recommended):** the Dashboard's "New run" affordance stays **inert** (as it already is in v1a — "opens in v1c"); Sean starts runs from the terminal, then the whole screening room drives them. v1b is complete and demoable without run-creation. This matches the milestone contract ("v1b binds to the CONVERGED daemon as-is").
- **Consequence if IN:** adds the Slice-6 backend (`POST /runs` + brief upload + `GET /characters` + a cost-estimate endpoint) **and** a net-new "start a project" UI flow (brief drop, character picker, cost preview) — a large scope add that duplicates the front-door's job and is better designed with the brainstorm room (D2, v1c). Not worth pulling forward.
- **Note:** the Plan-gate cost preview does **not** need Slice 6 — `cost_estimate` is already in raw state (`GET /runs/{id}`). Slice 6 is *only* about creating runs from the UI.

Slice 6 is built JIT when the new-run-from-UI flow is designed (v1c, with D2).

---

## Daemon deltas REEL ONE turned out to need

The honest answer to "did REEL ONE need deltas? (ideally none)": **not zero, but no blockers.** Everything visual/interactive is served; these are derived-value / scope-narrow / nice-to-have. Filed here so the per-unit kickoffs handle them explicitly and Sean can promote any of them.

| # | Gap | v1b handling | Promote to a backend delta when… |
|---|---|---|---|
| **G1** | **Actual cost SPENT** is tracked nowhere (no accumulator in `pipeline/`/`server/`). | Box office shows the **estimate** (served) + a **client-derived "spent so far"** = `Σ attempts × $0.07`, labelled as derived (D-H). | The museum wants real cost-evidence, or tier-mixing makes the $0.07 constant false. **Ties to the museum story — worth filing.** |
| **G2** | **In-UI storyboard curation** (cut/reorder/add) — daemon serves only `approve` (`mutate` is CLI-only). | Storyboard gate = **review + lock only** (D-F); curation on disk until then. | v1c, if in-room curation is wanted — a `storyboard mutate` endpoint over the existing CLI mutate. **Open decision.** |
| **G3** | **Animatic rough upload + display** — no endpoint receives or serves a dropped rough. | **Thin** animatic gate: status + Ingest/Skip (D-G); roughs on disk. | If in-UI drop-upload is wanted — a multipart rough-upload + a rough-image read. **Open decision.** |
| **G4** | **`chain_from` / `beat_id`** live only in `shots.yaml` (served raw). | Client fetches + parses the `shots` artifact for the loop-return arrow. Derivable — no delta needed. | If the YAML parse in the client becomes a burden — fold into `/status.frames[]`. |
| **G5** | **Per-frame model + cost** (`NB2 · $0.07`) not served. | Hardcoded v1 constant (all frames `standard_keyframe → NB2 → $0.07`). | D4/v2, when `route` lands on the candidate payload (tier-honesty). |
| **G6** | **Job ETA / progress** — none; only binary running/terminal + tailing logs. | The leader is a **client-side ritual timer**, not a progress bar — on-brand (D-C). | Never, probably — the leader is a ritual, not a meter. |
| **G7** | **Document-gate reject / send-back is not a daemon action** — `GATE_SPECS` has only `--approve-*`; no reject route on plan/script/storyboard (red-team BLOCKER). | **No send-back button in v1b** — "not ready?" is a CLI re-run on disk, then re-read (D-F). | v1c, if in-room send-back is wanted — a reject/return gate over the CLI. **Open decision.** |
| **G8** | **Recipe strip / structured provenance not served** — `/candidates` carries no `injected_plates`/prompt/route/provenance record (red-team). | Recipe strip **omitted** (no data); the provenance *line* is client-composed from constants + the verdict (eye-gate §G8). | D6/v2, with `injected_plates` on the candidate payload. |
| **G9** | **Character anchor / Bible image not served** — the image endpoint is `run_dir`-confined; `characters/{id}/anchor.png` is outside it. | Eye-gate diff is **attempt-vs-attempt / candidate-vs-approved-prior** only; candidate-vs-anchor dropped (D-E). | If diff-vs-anchor is wanted — a `GET /characters/{id}/anchor` (Slice-6-adjacent). |
| **G10** | **`run_summary` carries no busy signal** — the `/runs` list projection has no `active_job`/`blocked_by_job`. | Dashboard in-flight badge = per-card `/status` fan-out (on-hover) or omit (U2a). | If a marquee busy-badge matters — add `active_job` to `run_summary`. |

Only **G1** is a truly-missing datum for a shipped screen; **G2/G3/G7** are where the mockups run ahead of the shipped `approve`-only backend (all surfaced as open decisions); **G8/G9/G10** are omit-or-derive; **G4/G5/G6** are constants/derivations. **v1b binds to the daemon as-is** — no delta is a prerequisite; each is a named v1c/v2 promotion.

---

## Open decisions surfaced for Sean

Each with a recommendation (the first option). None block starting U0.

1. **Slice 6 — in or out of v1b?** → **OUT** (recommended; §Slice-6; both red-teams confirmed no v1b screen needs run-creation). New-run-from-UI is v1c with the brainstorm room; v1b drives CLI-created runs.
2. **Document-gate write paths (G2 storyboard curation + G7 send-back/reject) — narrow to approve/lock only, or build the mutate/reject deltas into v1b?** → **Narrow to approve/lock only** (recommended). Curation + re-runs happen on disk today; in-room cut/reorder + send-back are clean v1c deltas. Keeps v1b pure-frontend (no `server/` change).
3. **Animatic gate (G3) — thin gate, or defer the screen entirely?** → **Thin gate** (recommended). It's cheap, completes the stepper, and animatic is opt-in/off-by-default; Skip = approve-empty; full drop-upload is a v1c delta.
4. **Cost "spent" (G1/D-H) — derived-and-labelled, estimate-only, or file the spend accumulator now?** → **Derived-and-labelled for v1b + file G1 as a named follow-on** (recommended) — it's the museum's cost-evidence hook, so worth filing, but not a v1b blocker.
5. **Increment boundaries** — this plan **pre-splits** U2→U2a/U2b, U4→U4a/U4b/U4c, U5→U5a/U5b/U5c per the red-team (each split slice is one clean TDD session). → **Ship the eleven-slice sequence** (recommended). If any slice still proves large at kickoff, the JIT kickoff can split further; recombining is discouraged (the red-team flagged the merged forms as over-scoped).
6. **How hard to push the summonable HUD / idle-dark?** → **Scope the timed idle-dark to the eye-gate; density-default (art + one decision, secondary on intent) everywhere else** (recommended; D-B). A plan you're reading shouldn't fade its own text.
7. **The eye-gate Em read-out (U5a) — Fable or a small Opus slice?** → **Keep Fable** (recommended) — it's the stage foundation the Fable modes (U5b/U5c) build on; a model-handoff seam mid-stage costs more than it saves. (Opus is defensible if Fable capacity is tight — U5a is the least interaction-dense of the three.)
8. **Webfont for Futura** (U0 detail) — source a licensed Futura-equivalent via `@fontsource`, or ship the mockup's system fallback stack? → **Ship the fallback stack for v1b; treat a licensed face as polish** (recommended) — don't block the design system on a font procurement.

---

## Risks

1. **The eye-gate engine is the whole milestone's risk** (interaction density, timing, a11y of a keyboard instrument). *Mitigation:* it's the last unit (U5), on the strongest model (Fable), over a **working prototype** (the mockup) and a proven job-poll pattern (U3) — everything it needs is de-risked before it starts.
2. **U3 is load-bearing for U4 + U5** — if the shared job-poll flow is wrong, three units inherit the bug. *This risk already fired once in the draft* (the D-C pseudocode collapsed the two 409 shapes — a stale tab would offer to "watch" a nonexistent job); the red-team caught it and it is fixed in D-C + U3's DoD (the 409 branches on `detail.active_job_id`; success requires `!load_error && fresh_state`). *Mitigation:* U3 proves all branches (202 / 409-busy / 409-stale / failed / degraded-success / 422 / 404 / blocked) on the simplest gate first, with the MSW job-lifecycle seam U4/U5 reuse.
3. **Density mandate vs. completeness** — "cut a panel" can hide a state a screen must handle. *Mitigation:* the five doctrine states are DoD *independent* of the density gate; cut *chrome*, never a *state*. The density gate governs the default view, not whether a state exists.
4. **The derived cost-spent could read as a real meter** (G1/D-H). *Mitigation:* label it as derived; never render it with a false precision.
5. **The mockups are ahead of the backend in two places** (G2 storyboard curation, G3 animatic upload). *Mitigation:* both narrowed for v1b with a named delta + an open decision — the builder never tries to POST an endpoint that isn't there.
6. **Webfont / licensing drift** (Futura). *Mitigation:* fallback stack ships; the face is polish (Open decision 8).
7. **Scope creep from v1c/v2 picks** (annotation, chat, taste ledger, recipe authoring, motion). *Mitigation:* the milestone contract is explicit — v1b sends `{note}` only, renders `injected_plates` read-only *if present*, and touches no D1–D6 backend. Every deferral is named.
8. **The dual-Vite config + `web/.gitignore` traps** (tracker gotchas). *Mitigation:* restated in Global Constraints; every kickoff carries them.

---

## Red-team reconciliation

Two independent adversarial passes ran against the draft, both instructed to **verify claims against the tree, not trust the doc**: a **fresh-context Claude red-team** (re-read `server/*`, both eye-gate sources, `web/*`) and a **Codex `exec` engineering critique** (gpt-5-class, read the real `server/` code). Strong convergence: **every one of the plan's five backend-gap claims verified TRUE** (no cost-spent accumulator — only an unused `actual_cost` placeholder on `AgentResult`, never wired; `mutate` CLI-only; no animatic endpoint; `chain_from` only in `shots.yaml`; `cost_estimate` in raw state only), and the Em payload shape matches `generate_stage.py` exactly. Findings + my calls:

**Blockers — fixed in this doc before it converged:**
- **The D-C job-poll pseudocode collapsed the two 409s** (busy → dict `{active_job_id}`; stage-mismatch → plain string). The hook is inherited by U3→U4→U5, so a source-of-truth bug would propagate. **Fixed:** D-C branches on `detail.active_job_id`; U3's DoD lists 409-busy *and* 409-stale as distinct; Risk #2 records the near-miss.
- **Terminal success was under-specified** — `rc===0` can still carry `load_error`/null `fresh_state`. **Fixed:** D-C + U3 require `state==="succeeded" && rc===0 && !load_error && fresh_state && next_action` to auto-advance; the degraded case shows a reload state.
- **Document-gate send-back/reject is not a daemon action** (`GATE_SPECS` = `--approve-*` only). **Fixed:** removed send-back from every gate; named G7; D-F + the screen map + U4 updated; surfaced as Open Decision 2.
- **U5 ("the full instrument") was too large + never defined image cache/error.** **Fixed:** pre-split into U5a (stage + Em read-out) / U5b (keyboard + print/again) / U5c (modes), with a cross-slice image-behavior + focus-ownership DoD.

**Should-fixes — folded:**
- **U2 + U4 pre-split** (Dashboard vs net-new Overview; three gates with different absence semantics) → U2a/U2b, U4a/U4b/U4c; the sequence is now eleven slices.
- **U2b's Working state can't be the live leader** (polling is U3) → rendered as a static one-read visual, no auto-advance; U3 upgrades it.
- **The Overview stepper's stage set is run-shape-derived** (omit SCRIPT/STORYBOARD back-compat, ANIMATIC when disabled) → added to U2b DoD, mirroring U4's gate-absence rule.
- **U4's DoD named neither the density gate nor a11y** — the most panel-prone cluster → both restated on all three U4 slices.
- **Race-safety was overstated** → scoped to daemon-vs-daemon; CLI-vs-daemon is the one-owner rule (D-C).
- **The recipe strip / provenance record isn't served** (G8) → recipe strip omitted in v1b; the provenance *line* is client-composed from constants + the verdict, stated as such.
- **Diff candidate-vs-anchor is unserved** (the anchor is outside `run_dir`; G9) — *independently caught by both the plan author and both red-teams* → diff narrowed to attempt-vs-attempt / candidate-vs-approved-prior.
- **U3 DoD missing HTTP error branches** (422/404) → added.
- **Dashboard in-flight badge under-flagged** (`run_summary` has no busy signal; G10) → scoped to on-hover fan-out; named as a delta.
- **"Reproduce the mockup" over-trusts a partial prototype** (its `keydown` covers only 10 keys; no `↑↓`/`?`/hover-skim/real-onion/auto-advance) → reframed: the spec addendum R1/R2 is authoritative for the mode/key set; the mockup is a visual reference for what it implements.

**Nits — folded:** `⌘⏎` dropped from the eye-gate key map (it belongs to the document gates; the eye-gate's last-frame boundary auto-cascades); Animatic "Skip" clarified as approve-empty, not a separate endpoint; timecode `frame_index × hold` no longer attributed to the mockup (which hardcodes offsets); the onion "next" color noted as a conscious deviation from R2's teal-bright (REEL ONE has no teal); the `chain_from` client YAML-parse dependency (js-yaml + YAML MSW fixtures) named in D-E + U5c.

**Confirmed unchanged:** the **Slice-6 OUT** call (both red-teams verified no `POST /runs`/`/characters` and no v1b screen needing them); **U3-first on the Plan gate** (a defensible proving ground — all job branches are MSW-provable there; the caveat that a *real* approve-plan advances to an as-yet-unbuilt next screen is noted, and doesn't affect the pattern proof).

**Verdict (both passes):** structurally sound and unusually well-grounded, **not build-ready as originally drafted** — the D-C 409 mis-spec + the send-back/anchor contradictions + the U5/U2/U4 scoping had to be fixed first. **All are fixed above.** U0 / U1 / U2a kickoffs can be cut now; U3 (and everything downstream) inherits the corrected job-flow contract.
