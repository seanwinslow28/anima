# ② Flow v1b Polish — Codex Execution Handoff

**Date:** 2026-07-11 · **Executor:** Codex 5.6 · **Reviewer:** Claude (Fable 5) · **Owner:** Sean
**Source of truth:** [`docs/active/2026-07-10-v1b-polish-plan-CONVERGED.md`](2026-07-10-v1b-polish-plan-CONVERGED.md) (the converged plan — the slice stubs live there and are NOT duplicated here) · [`PRODUCT.md`](../../PRODUCT.md) · [`DESIGN.md`](../../DESIGN.md)

This document is the execution contract for the seven polish slices (P1 → P2 → P3a → P3b →
P4 → P5 → P6). Codex builds; Claude reviews each PR before the next slice starts; Sean is the
final eye. **One slice per session. Stop after the PR. Never start the next slice unreviewed.**

---

## Read order (every session, before any edit)

1. `PRODUCT.md` — who the room is for; the non-negotiables.
2. `DESIGN.md` — the normative system. **Where shipped code deviates from DESIGN.md, the rule
   wins.** Any visual change re-checks its contrast pair against §2's ledger.
3. The converged plan — §Global constraints, §The audit (your slice's defect rows, with
   file:line root causes), and **your slice's stub only** (its Surface / Work / DoD / Test
   impact is the kickoff).
4. This handoff — the protocol below.

## The ratified decisions (Sean, 2026-07-11 — build with zero ambiguity)

All six of the plan's open decisions are **ratified as recommended**:

1. **Action-hue grammar:** tungsten = commit/recover (approve, print, lock, error-retry — the
   marquee's bakelite retry becomes tungsten); bakelite reserved for strike/destructive + the
   fail lamp; **"Go again" becomes a quiet control** (booth2 + line, like the toolbar).
   P3b implements; DESIGN §2 is the spec.
2. **Whisper sub-labels ship at 11px mono** (P5/L2; never below the floor).
3. **Futura stays the fallback stack.** Optional P3b rider: a `/dev/system`-only A-B toggle
   with a self-hosted open geometric (e.g. Jost) — no production screen ships it.
4. **Dashboard poster thumbnails / in-flight badge: OUT** (G10 stands as a named v1c delta).
5. **Viewport axes:** designed width 900–2560px (below 900 single-column, nothing clips, down
   to ~600px wide); designed height ≥600px.
6. **No standalone state-class refactor** — treatments align via DESIGN §7 + P3 tokens only
   where a slice already touches a file.

## Hard rules (from the plan's §Global constraints — violations fail review)

- **Executors never merge a PR and never push to `main`.** `gh pr merge` is Sean's hand only.
  An executor may push its feature branch and open/update the PR, then it stops for review. PR
  #99 was merged by its executor; that boundary violation must not recur, regardless of code
  quality.
- **`web/` only.** `server/`, `pipeline/`, `evals/` byte-identical — verify per slice:
  `git diff origin/main -- server/ pipeline/ evals/` is empty, and both md5 guards hold:
  `md5 -q evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` →
  `2af75906502f1caf8857e18828ceb2e4`; `md5 -q pipeline/agents/prompts/sean-screenwriting-voice.md`
  → `945af824fa53b948a18ac6bf206d67ef`. Zero daemon deltas — if a slice seems to need one, STOP
  and surface it; do not build it.
- **The suite never shrinks.** Baseline 305 green (`cd web && npx vitest run`); tests are added
  or extended; a pinned assertion changes ONLY where the plan names it (e.g. P2's three
  "ON SCREEN" pins). `npm run build` clean.
- **TDD:** red → verify-red → green → verify-green, per work item. Fresh worktree off latest
  `main` per slice (`git fetch origin && git reset --hard origin/main`). Commit per task;
  `web/.gitignore` respected before `git add`.
- **Untouchables:** the `.reelone` token scoping (never `:root`); the dual-Vite
  `vite.config.ts` workaround + v7 router flags; `useGateAction`'s branch contract; the five
  doctrine states; the reduced-motion contract (DESIGN §8 — arrivals crossfade, **never a dead
  cut**; P3b's motion consolidation is scoped to flicker/weave/pulse ONLY).
- **The density gate is a review question on every change:** default = the art + the one
  decision; lamp > word; cut a panel, never shrink it; no new permanent chrome.

## Skill usage (impeccable v3.9.1, vendored at `.claude/skills/impeccable/`)

- Codex adaptation: read `.claude/skills/impeccable/reference/codex.md` once per session
  (the platform notes), then run `node .claude/skills/impeccable/scripts/context.mjs` — it
  loads PRODUCT.md + DESIGN.md as your design context.
- Per slice: consult `reference/polish.md` for the closing pass of every slice;
  `reference/layout.md` for P1; `reference/audit.md` before/after P3a (the detector:
  `node .claude/skills/impeccable/scripts/detect.mjs --json web/src`); `reference/delight.md`
  + `reference/interaction-design.md` for P5; `reference/adapt.md` for P6's narrow sweep.
- The design-detector hook is installed for the Codex harness (`.codex/hooks.json`) — treat
  its post-edit findings as review feedback, not noise.

## Environment (for live verification + screenshot evidence)

```bash
# two servers, $0, read-only against runs/
ANIMA_RUNS_ROOT=$(pwd)/runs .venv/bin/python -m uvicorn server.app:app --port 8000
cd web && npm run dev        # 5173, proxies /runs /health /jobs → 8000
```

Stations: `/` · `/runs/<id>` · `/runs/<id>/{plan,script,storyboard,animatic}` ·
`/runs/<id>/frames/<n>` · `/dev/system`. A fresh live gate when needed:
`python3 -m pipeline.run --brief briefs/2026-06-10-spark-shared --stub --slug <s> --run-dir runs/<new>`.
Screenshot evidence per the slice DoD: Playwright (a scratchpad script — never committed into
`web/`) at **1024 / 1280 / 1440 / 1920**, plus 1280×680 and the interaction states
(onion `O` on a frame ≥2, diff `D` + `[`, lights `L`, `?`, `R`, idle-dark 4s) for any eye-gate
slice. The audit scripts that produced the plan's evidence are the pattern to copy.

## Per-slice protocol

1. Worktree off latest `main`; branch `polish/p<N>-<slug>` (e.g. `polish/p1-stage-geometry`).
2. Build the slice per its stub. TDD per work item; the DoD checklist is the definition of done.
3. Verify: full suite green ×2 (flake check) · build clean · scope diff empty · md5 guards ·
   screenshot evidence pack · the density/a11y/reduced-motion re-checks the stub names.
4. Open the PR. Body template:
   - **Slice:** P<N> — <title> · closes defect rows D<x>…
   - **DoD checklist** (verbatim from the stub, each item checked with evidence links)
   - **Test delta:** N → M (named new tests; any pinned-assertion change cited to the plan line)
   - **Evidence:** the screenshot pack (before/after per station touched)
   - **Scope proof:** the diff-empty + md5 lines, pasted verbatim
5. **STOP.** Sean takes the PR to Claude for review; the next slice kickoff is cut only after
   that review merges. (Exception per the plan: P2 may ride P1's session as a second commit —
   never the reverse.)

## The review loop (Claude's side, recorded here so the contract is whole)

Per PR, Claude reviews: DoD-vs-diff (every stub item evidenced), DESIGN.md conformance
(tokens, floor, contrast pairs, reduced-motion, density), test-delta honesty, scope proof,
and — for P1/P5 — the taste call against the mockups + the plan's principles, with the
screenshots as the medium. Verdict: merge / named fixes (back to Codex in the same branch) /
escalate to Sean where it's a taste call only he can make. After P5's merge, the engine-truth
session is Sean's: daemon + vite up, a real run walked plan → gates → eye-gate → loop.

## Sequence + status

| Slice | Title | Model rec | Status |
|---|---|---|---|
| P1 | The stage owns the room (eye-gate geometry + rail in flow) | Fable-grade care | ✅ merged (#98) |
| P2 | Honest keys, honest labels (R-leak, D18 idle-dark, YOUR CALL, aria-valuetext) | — | ✅ merged (#99) |
| P3a | Tokens, literals, and the type floor | — | ✅ merged (#100) |
| P3b | Button recipe + shared primitives + the living sheet | — | ✅ merged (#101) |
| P4 | The gates read like a room (archival state + hierarchy + lamp-pool retune) | — | 🟨 in review |
| P5 | Deepen the ritual (intercom, whispers, bleed, warmth; ends with engine truth) | Fable-grade care | ⬜ |
| P6 | One room, every screen (consistency + narrow sweep) | — | ⬜ |

Update this table's status column in each slice PR.
