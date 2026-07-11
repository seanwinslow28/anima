# ② Flow v1b — REEL ONE Polish Pass: Converged Execution Plan

> **For agentic workers:** each slice below is a **titled stub — designed here, built JIT** in its
> own fresh session. When a slice becomes active, its kickoff is written from this doc (mirror the
> last same-layer kickoff), then: REQUIRED SUB-SKILLS — superpowers:test-driven-development
> (red → verify-red → green → verify-green), superpowers:using-git-worktrees (isolate off latest
> `main`), superpowers:verification-before-completion (evidence before "done"). This plan writes
> **no production code and no tests** — it is the source of truth the per-slice kickoffs are cut from.

**Date:** 2026-07-10
**Status:** Plan — converged. Drafted from a live /impeccable audit of the shipped app (two
Playwright sweeps, 48 screenshots, 4 viewport widths, every station on real runs), then run
through an independent fresh-context red-team pass; corrections folded in and marked
(§Red-team reconciliation), the build plan's discipline.
**Goal:** v1b is code-complete (11 slices, PRs #86–#96, 305 tests, backend byte-identical) and
*solid*. This pass makes it **impeccable**: fix the real defects the audit confirmed, harden the
design system the build left implicit, and deepen the screening-room ritual — without breaking a
single shipped contract. The polish DEEPENS REEL ONE; it never drifts toward generic dashboard
polish.
**Design authority:** [`PRODUCT.md`](../../PRODUCT.md) + [`DESIGN.md`](../../DESIGN.md) — both
written this session (the /impeccable lockdown; DESIGN.md placed at **repo root**, impeccable's
canonical location, so every future design session loads it). Where shipped code deviates from
DESIGN.md, the rule wins and the deviation is a slice below.
**Model split:** the two taste/interaction-dense slices (P1 stage geometry, P5 delight) are
**Fable 5**; everything else is **Opus 4.8 / Codex** (same logic as the build plan's split).

---

## Global constraints (copied forward from the build plan — every kickoff includes these)

- **`web/` ONLY.** `server/`, `pipeline/`, `evals/` stay **byte-identical**; the two md5 guards
  unmoved (`2af75906…` g6.1b trace, `945af824…` screenwriting voice). Every slice's verification
  re-checks both. If a polish idea needs backend, it is a **named delta, deferred** — never
  smuggled in. (This plan needs **zero** daemon deltas — verified per slice.)
- **The 305 tests stay green.** Polish is refinement, not rewrite: the state machines, the
  job-flow contract (`useGateAction`'s branches), the never-drop-an-error discipline, and the
  five doctrine states are untouchable. Tests may be *added* and assertions *extended*; a test
  changes meaning only when the behavior it pinned was itself the defect (each such change is
  named in the slice's kickoff).
- **U0's `.reelone` token scoping holds** (BoothShell carries the class; tokens never on `:root`).
- **The dual-Vite `vite.config.ts` workaround + the v7 router flags do not move.**
  `web/.gitignore` before `git add`. Fresh worktree off latest `main` per slice
  (`git fetch origin && git reset --hard origin/main`).
- **Three cross-cutting contracts are DoD on every slice:** the five doctrine states (no state
  lost to a re-layout), the WCAG 2.1 AA a11y contract (DESIGN.md §2/§3/§8 — any visual change
  re-checks its contrast pair; the 11px floor; reduced-motion), and the density gate (default =
  the art + the one decision; cut a panel, never shrink it; no new permanent chrome).
- **Engine truth ends the milestone:** the last act of the final slice is Sean in the room —
  daemon + vite up, a real run walked plan → gates → eye-gate → loop — not a checklist.
- Full verification gate + stop green + PR per slice; do not roll into the next.

---

## The audit — how it ran, what it found

Two servers (`uvicorn server.app:app` + `npm run dev`), $0, read-only. Stations audited on real
runs: the marquee (`/`), the booth board at PLAN (fresh stub run `2026-07-10-polish-audit`) and
at GENERATE (`2026-07-10-v1b-eyeball`), the plan gate (live), the script gate (on a DONE run —
which itself exposed D5), the storyboard gate (live lock), the animatic gate (live), the
eye-gate on F01 (approved) and F04 (pending — ghost/wipe live), and `/dev/system`. Viewports
1920/1440/1280/1024 plus a short 1280×680; interaction states: onion, diff + wipe drag, lights,
cheat-sheet, retry-note, idle-dark, hold-to-run. Root causes were then verified in code
(file:line cited per finding). Two prior audit passes feed this: the U5c milestone review's
known items 1–2 (both confirmed, both root-caused deeper than reported) and item 3 (dismissed —
stub artifact; real Em verdicts differ per cast namespace, MSW-tested).

### Defects (real, confirmed — most severe first)

| # | Finding | Evidence / root cause | Screen · principle it violates | Slice |
|---|---|---|---|---|
| **D1** | **The stage doesn't own the room.** The lit frame renders as a ~350×220px postage stamp at *every* viewport (1024→1920), with a dead bottom third of booth below. Root cause: the flex height chain above `.eg-screen{height:100%}` is never established, so `.eg-stage` collapses to its `min-height:220px` (`eyegate.css:68-73`). Lights-out (`position:fixed`) escapes the chain and proves the intended geometry — frame near-full-viewport, burn-ins clean. | Known item 1's root; screenshots `eyegate--w1440/w1920.png` vs `eyegate-lights--w1440.png` | Eye-gate · "the frame is the only lit object in the room" | **P1** |
| **D2** | **The Em rail is an absolute overlay that collides at every width ≥901px** — not just ~1440. `.eg-rail{position:absolute; right:22px; width:270px}` (`eyegate.css:468`) floats over the transport row, occludes the provenance line ("…your call" clipped at 1440/1920), buries the wipe-controls slider's right end and the retry-note row's send/cancel, and eats the toolbar at 1024. Only ≤900px goes static. | Known item 2, worse than reported; screenshots all widths + `f4-diff-wiped--w1440.png`, `eyegate-retrynote--w1440.png` | Eye-gate · the responsive contract (DESIGN §5: no absolutely-positioned siblings that can collide) | **P1** |
| **D3** | **The two burn-in lines collide** ("F01 · TAKE 1 · HOLD 2" + "12 FPS · NB2 · $0.07" mash into "H0LI2 2FPS") — two independent absolutes on one baseline (`eyegate.css:400`) inside the D1-shrunken frame. | Known item 1; every normal-mode screenshot; clean in lights-out | Eye-gate · honest burn-ins | **P1** |
| **D4** | **The `R` key leaks into the retry note and destroys Em's prefill.** The `r` branch calls `openAgain()` without `preventDefault()` (`EyeGate.tsx:542-545`) and is **the only branch whose missing preventDefault has a leak destination** — the note input auto-focuses *and selects* on mount (`RetryNoteRow.tsx:49-52`), so the leaked keystroke *replaces the prefilled note*. (Several other branches also skip preventDefault harmlessly — do NOT spray it across them; `?`/digit semantics don't want it.) | Screenshot `eyegate-retrynote--w1440.png` (input contains literal "r"); code-verified | Eye-gate · "the critic proposes" made real | **P2** |
| **D5** | **All four document gates present a live primary on a run that already moved on.** `canApprove/canLock/canAct = flow.phase==="idle" && !blockedBy` never checks the stage (`ScriptGate.tsx:47`, `PlanGate.tsx:41`, `StoryboardGate.tsx:48`, `AnimaticGate.tsx:39`) — a DONE run's script gate shows a fully-lit "APPROVE — PRINT IT" that would 409-stale. The mockup's PICTURE-LOCKED archival treatment was never built. | Screenshot `scriptgate-done--w1440.png`; code-verified ×4 | Gates · honesty; DESIGN §7's printed/locked state | **P4** |
| **D6** | **The filmstrip says "ON SCREEN" about a frame that isn't.** Caption map hardcodes `eye: "ON SCREEN"` (`Filmstrip.tsx:20`) — the pending frame carries it even while the routed frame (the ring) is on the stage; on `/frames/1`, F01 is on screen but F04 claims it. | Screenshots frames/1 vs frames/4; code-verified | Eye-gate · honest labels; DESIGN §10 (`ON SCREEN` = the staged frame, `YOUR CALL` = awaiting the director) | **P2** |
| **D7** | **Seven type sizes below the 11px floor** the a11y contract claims (8.5px `.gate-approve small` gates.css:409 and `.ro-empty` reelone.css:199; 9px `.mq-cta-mark--print` marquee.css:152; 9.5px `.ro-fcell .ro-cap` reelone.css:213 — *semantic status text*; 10px `.eg-wipe-tag` eyegate.css:316; 10.5px ×2 systemsheet.css:49,108). | Design-system extraction (file:line each) | System · the 11px floor (PRODUCT/DESIGN a11y contract) | **P3** |
| **D8** | **Token discipline breaches:** `#101010` button text **×7** (red-team recount), `#f2c284` hover ×3, one-off `#d3543f`, sprocket `#241d2c` ×3 (case-drifted), true-blacks `#0b080d`/`#0e0b11` untokened, and — worst — the eye-gate's *failed* border is `rgba(207,106,76,.55)` (`eyegate.css:161`), **a different red than `--bakelite`**, so "failed" isn't one color across the room. Note the offender class is **rgba literals, not hex** — the enforcement mechanism must see both (P3a). Retry hue splits: marquee retry = bakelite, everywhere else tungsten. | Extraction §8; red-team verified counts | System · one reserved warning hue; DESIGN §2 token discipline | **P3a** |
| **D9** | **Responsive drift:** gates collapse at 960 vs 900 everywhere else (`gates.css:26`); the cheat-sheet's `min-width:340px` overflows <360px (`eyegate.css:681`); no graceful story below 900 for the rail band. | Extraction §3 | System · DESIGN §5 (one breakpoint token) | **P1** (eye-gate) + **P6** (sweep) |
| **D10** | **The marquee's error states use a 3px side-stripe** (`border-left: 3px solid var(--bakelite)`, marquee.css) — the banned pattern; every other screen uses full bakelite borders. | Extraction §5 | Marquee · consistency + the side-stripe ban | **P6** |
| **D11** | The on-stage wipe tag is 10px low-contrast text floating over arbitrary frame art (`eyegate.css:316`). (The tag is `aria-hidden` — this is a *visual* legibility fix; the AT win is D12.) | `f4-diff--w1440.png` | Eye-gate · legibility | **P2** |
| **D12** | The wipe slider announces bare 0–100 — no `aria-valuetext` (`DiffWipe.tsx`). | Extraction §4 | Eye-gate · a11y | **P2** |
| **D13** | `.eg-print` has no `:hover` state — the room's most important button is the only primary without one (`eyegate.css:651`). | Extraction §8 | Eye-gate · component states | **P3b** |
| **D14** | Maintenance smells that will corrupt future polish: sprocket CSS copy-pasted ×3; eyegate writes its own `animation:` shorthands over the shared keyframes instead of consuming `.ro-flicker`/`.ro-weave` (**corrected — the keyframes are NOT duplicated**, and the eye-gate's `.18s` soft-arrival rules are *deliberately bespoke* for the reduced-motion no-dead-cut contract — consolidation is scoped to flicker/weave/pulse ONLY, arrivals untouched); dead v1a token scales (`--sp-*`, `--r-*`, `--e-out` — 0 references); no *named* z-scale (the shipped integers already match DESIGN §4's table; tier 5's two occupants are nested by design — the veil contains the leader — not a conflict). | Extraction §6/§7/§8; red-team corrections folded | System · DESIGN §4/§6/§8 | **P3** |
| **D15** | **Gate actions float at the viewport's left edge, detached from the centered page** — the eye finishes Bea's board bottom-center, then hunts for "LOCK PICTURE" far left. The mockup anchored actions in the aside's gate card. Sub-label wraps awkwardly inside the button. | `plangate/storyboard/scriptgate/animatic--w1440.png` | Gates · hierarchy; "the art + the one decision" (the decision shouldn't hide) | **P4** |
| **D16** | The collapsed "THE CREW TONIGHT" intent-reveal renders as a bare header on a void (reads broken, not quiet); the box-office derived line wraps mid-phrase ("× $0.07" orphaned). | `overview-plan/generate--w1440.png` | Board · DESIGN §7 (collapsed panels look intentional) | **P4** |
| **D17** | **The lit page reads flat — a tuning defect, not an absence** (red-team correction: the mockup's lamp-pool CSS ships *verbatim* — `gates.css:36-46` radial wash + `:54-56` paper glow — yet the live gates read flat at 1440, so the shipped values/geometry are visually swamped in situ). The work is a **retune** (wash intensity/extent, glow radius, page-vs-booth contrast), judged by eye against `reelone-reading.html` — not re-adding CSS that exists. | Gate screenshots vs `reelone-reading.html`; `gates.css:36-56` verified shipped | Gates · "the page is the lit object" | **P4** |
| **D18** | **Idle-dark fades the retry note mid-composition** (red-team discovery). `idleDark = boothDark && !noticeUp && !jobRunning` (`EyeGate.tsx:600`) never checks `againOpen`; the note row renders inside `.eg-transport`, which fades to 12% after 3s of no input — pause to think about a correction and the input you're focused in disappears. Direct violation of DESIGN §9 ("never timed-fade content someone is reading"). The hud test suite never covers `againOpen`. | Code-verified `EyeGate.tsx:600` + `eyegate.css:386-389` + `HudHost.tsx:28,52-58` | Eye-gate · the summonable-HUD doctrine | **P2** |

**Dismissed (audited, not defects):** stub Em cards near-identical across namespaces (stub
artifact — real verdicts differ, MSW-tested; known item 3). The leader-strip numerals counting
5/4/3 (designed: "count down like a film leader — the last segment always reads 3,"
`boothBoard.ts:58,106`). GHOST/WIPE disabled on F01-take-1 (correct: no prior print, single take).

### Delights (deepen the ritual — audited against the mockups' dropped details)

Every candidate is transient or intent-summoned (density-safe); each ships with its
reduced-motion + a11y story. Slice P5 owns them; the list is ranked, cut from the bottom.

| # | Delight | Source · rationale |
|---|---|---|
| L1 | **The booth intercom** — print/again/lock feedback as a bottom-center toast line ("F03 TAKE 2 — PRINTED. $0.07 to the ledger." / "GO AGAIN — note sent as a correction. Flo re-shoots F04."), `aria-live` polite, auto-dismiss ~2.6s. Today printing gives no textual confirmation at all — the circled take is the only ack. | Mockup (verbatim strings); closes the feedback loop without chrome |
| L2 | **Whisper sub-labels** under primaries at 11px mono — "⏎ · circle the take", "R · the note rides along", "re-validates · then it's the camera's". The mockups' quiet second voice; shipped buttons carry key glyphs only (and the one shipped sub-label is 8.5px — D7). | Mockup; discoverability without a legend |
| L3 | **The hero thumbnail bleed** on the booth board's now-screening card — the current frame, rotated −4°, opacity .16, bleeding off the corner (the art ghosting through the decision card). Uses the already-served frame image; no new fetch. | Mockup (overview) |
| L4 | **Crew busy dot** — a tungsten `●` after the working crew member's name; **"Rolling…"** swap on To-the-screening's label (1.2s, then navigate). | Mockup (overview) |
| L5 | **Leader-strip + reel hover warmth, honestly scoped** — the warm wash invites only what navigates (today `.bb-seg:hover` lights *every* segment while only printed ones link — P6's false-affordance fix and this delight are two halves of one rule: hover warmth = "you can go here"). | Mockup (overview); red-team refinement |
| L6 | **Idle-dark glow swell** — as chrome fades to 12%, the frame's screenlight halo intensifies slightly (the room gets darker, the print gets brighter). Reduced-motion: chrome stays, no swell. | Extends the shipped idle-dark; pure CSS |

### Where the mockups stay ahead on purpose (not polish; named deltas, unchanged)

In-UI storyboard curation (G2), send-back/reject (G7), animatic rough upload/display (G3),
recipe strip (G8), diff-vs-anchor (G9), marquee in-flight badge (G10), real cost-spent (G1) —
all remain v1c/v2 promotions per the build plan. **No polish slice touches them.**

---

## The decomposition — six conceptual slices, **seven build slices**

Legend per slice: **Surface · Work · DoD · Test impact · Model.** Sequence is the order below;
every slice is independently demoable and PR'd.

### P1 — The stage owns the room (eye-gate geometry + the rail in flow) · **Fable 5**
- **Surface:** `eyegate.css`, `EyeGate.tsx` (DOM structure only — no state-machine changes),
  `booth.css` (the height chain).
- **Work:** fix D1/D2/D3/D9-eye-gate structurally, per DESIGN §5. **The height chain's one
  missing link (red-team-verified):** `html/body/#root{height:100%}` and the `min-height:0`s
  already exist — what's missing is that `.booth-stage` is **not a flex container** (and
  `.booth{min-height:100vh}` is indefinite), so `.eg-screen{height:100%}` resolves to auto and
  `.eg-stage` collapses to its `min-height:220px`. Fix at that link (e.g. `.booth-stage`
  becomes a flex column its screens can fill), kill the dead min-height, and let the stage
  scale to its room (`max-height:74vh`, `aspect-ratio:16/10`, approaching the lights-out
  geometry minus chrome). **The Em rail becomes a grid column** (stage `1fr` + rail ~280px
  ≥900px, in-flow below — overlap impossible by construction), so the provenance line, wipe
  controls, retry row, and toolbar never sit under it — noting the two `inset:0` absolutes of
  `.eg-stagewrap` (the beam, the job veil) re-anchor to the *stage column*, and deciding
  explicitly whether the veil covers the rail (today z5 > z4 does). The two burn-ins become
  one flex row (`space-between`, ellipsis before collision) pinned inside the frame edge;
  cheat-sheet `min(340px, 92vw)`.
- **DoD:** Playwright evidence at 1024/1280/1440/1920 + 1280×680 — zero overlap, zero clipped
  text, the frame visibly owns the viewport; idle-dark/lights-out/onion/diff/leader all render
  correctly in the new geometry; **the `booth.css` change is app-wide — a one-shot regression
  check of the marquee, booth board, and long document gates (layout + scroll behavior) is
  part of this slice's evidence, not just the eye-gate set** (red-team blast-radius finding);
  the five states intact; reduced-motion untouched; contrast pairs unchanged (layout-only);
  all suites green.
- **Test impact:** existing EyeGate suites (8 files) stay green as-is; add structural
  assertions — rail renders in the grid (not absolute), burn-in single-row, cheat-sheet width
  clamp. No behavioral test changes.
- **Why Fable:** this is the signature screen's geometry — the eye judging "does the frame own
  the room" is the work; the CSS is easy, the taste isn't.

### P2 — Honest keys, honest labels (eye-gate behavior nits) · **Opus 4.8 / Codex**
- **Surface:** `EyeGate.tsx`, `Filmstrip.tsx`, `DiffWipe.tsx`, `eyegate.css` (tag styling),
  their tests.
- **Work:** D4 — `preventDefault()` on the `R` branch **only** (not sprayed across branches —
  see D4's note); D18 — `againOpen` (and by review, any focused composition surface) suppresses
  idle-dark, per DESIGN §9; D6 — the `eye` caption becomes `YOUR CALL` (DESIGN §10; `ON SCREEN`
  reserved for the staged frame — the ring's cell; the `mark` prop is the clean seam); D11 —
  the wipe tag ≥11px with a burn-in-style text shadow so it reads over any art; D12 —
  `aria-valuetext` on the wipe slider ("62% — mostly TAKE 2").
- **DoD:** red → green per fix; the keyboard SM + hud suites green. **Test-framing honesty
  (red-team):** jsdom's `fireEvent.keyDown` cannot reproduce browser text insertion — the D4
  red test asserts `defaultPrevented` on the `r` keydown (plus prefill integrity), not "no
  leaked character." The D18 red test drives the idle timer with `againOpen` true and asserts
  the transport never enters idledark.
- **Test impact:** ~6 new tests; **3 existing assertions updated across 3 files** (the "ON
  SCREEN" pins: `Filmstrip.test.tsx:58`, `EyeGate.test.tsx:288`, `RunOverview.test.tsx:190` —
  a deliberate pinned-behavior change, enumerated here so it's not discovered mid-slice).

### P3 — The token lockdown (design-system hardening) · **Opus 4.8 / Codex** · **pre-split into two build slices** (red-team: the merged form touched every CSS file + tokens + the button recipe + `/dev/system` in one session — two sessions' worth)

**P3a — Tokens, literals, and the type floor.**
- **Surface:** `reelone.tokens.css`, every screen CSS file, `reelone.test.ts`.
- **Work:** add the named tokens (`--booth-deep`, `--sprocket`, `--on-tungsten`,
  `--tungsten-bright`) and migrate every literal 1:1 (D8 — `#101010` **×7**, `#f2c284` ×3,
  `#d3543f`, `#241d2c` ×3, the true-blacks); unify the failed-border to `--bakelite`; raise
  the seven sub-floor sizes to ≥11px (D7 — **the size raises are intended visual changes**,
  enumerated in the PR with before/after: the filmstrip captions re-wrap their cells); gates
  breakpoint 960 → 900 (D9). **Enforcement mechanism (red-team: a hex-only grep cannot see
  D8's own headline offender):** the DoD grep covers `#hex` **and** `rgba?(` with a documented
  allowlist — glow washes must be channel-triples of a token (`--*-rgb` variables or
  `color-mix()`), never free literals; pre-existing washes migrate to the mechanism as touched.
- **DoD:** the two-pattern grep returns only token files + the allowlist (documented in the
  PR, not CI-wired); contrast re-verified for every changed pair; before/after screenshots of
  every station — the only visual shifts are the enumerated intended ones; all suites green.
- **Test impact:** `reelone.test.ts` token-presence extends; size-raise assertions enumerated
  at kickoff.

**P3b — The button recipe + shared primitives + the living sheet.**
- **Surface:** `reelone.css`, `reelone.motion.css` consumers, screen CSS, `SystemSheet.tsx`/
  `systemsheet.css`.
- **Work:** **one primary-button recipe** (+ quiet + danger variants) consumed by `bb-go`/
  `gate-approve`/`eg-print`/retries — landing D13 (`.eg-print` hover) and the action-hue
  grammar (pending Open Decision 1; default = DESIGN §2's recommendation); one shared sprocket
  class (kills the ×3 copies); motion consolidation **scoped to flicker/weave/pulse only** —
  the eye-gate's `.18s` soft-arrival rules are deliberately bespoke and `.ro-arrive` collapses
  to instant under reduced-motion, so a blanket `.ro-*` migration would regress the
  no-dead-cut contract (red-team trap, D14); z-scale tokens naming the DESIGN §4 tiers (the
  shipped integers already match — this is naming, and tier 5's nested veil+leader stay one
  tier); `/dev/system` extends to render the new tokens + the button recipe (the living proof).
- **DoD:** every primary/quiet/danger button across the app renders from the recipe (grep for
  bespoke button color rules); reduced-motion sweep proves arrivals still crossfade;
  screenshots; all suites green.
- **Test impact:** SystemSheet tests extend; button-consumption assertions where screens pinned
  classes.

### P4 — The gates read like a room (document-gate state + hierarchy) · **Opus 4.8 / Codex**
- **Surface:** `GateShell.tsx`, the four gate screens, `gates.css`, `boothboard.css` (crew/box
  office nits), their tests.
- **Work:** D5 — the **printed/locked archival state** on all four gates: when
  `status.stage` has moved past the gate (or the artifact carries `locked: true`), render the
  artifact + a LOCKED/PRINTED mark (the mockup's overlay language, quieted to a stamp) with
  **no live primary**; `canApprove` gains the stage check (the 409-stale branch remains as the
  race backstop; `RunStatus.stage` is already fetched — zero daemon delta, red-team-verified).
  D15 — actions anchor to the page column/aside gate-card (the decision sits where the reading
  ends), sub-label wrap fixed (rides P3b's button recipe). D17 — **retune** the lamp pool (the
  CSS ships verbatim at `gates.css:36-56` and still reads flat — adjust wash intensity/extent,
  glow radius, page-vs-booth contrast, judged by eye against `reelone-reading.html`). D16 —
  the collapsed crew panel gets its whisper line at rest; the box-office derived line wraps as
  a unit.
- **DoD:** each gate's state tests extend with the archival state (route a DONE-run fixture to
  every gate); the five states + job-flow branches untouched and green; density gate re-read
  (the lamp pool is light, not chrome; no new permanent panel); a11y (one `<h1>`, landmarks,
  focus order) re-checked; contrast: page-ink pairs unchanged, glow is decorative.
- **Test impact:** ~6–8 new tests (4 gates × archival state + placement); no daemon change —
  the stage check reads the already-fetched `/status`.

### P5 — Deepen the ritual (the delight pass) · **Fable 5**
- **Surface:** `EyeGate.tsx`/`eyegate.css` (intercom, idle-glow), `RunOverview.tsx`/
  `boothboard.css` (thumbnail bleed, crew dot, Rolling…, hover warmth), `reelone/` (a shared
  `<Intercom>` primitive), their tests.
- **Work:** L1–L6 in rank order, cut from the bottom if the slice runs long. The intercom is
  the load-bearing one (the room finally *answers* a print). Every delight: transient or
  summoned, reduced-motion story (instant/none), a11y story (`aria-live` for the intercom;
  decorative pieces `aria-hidden`), and **the density gate is the review** — if a delight wants
  to be permanent chrome, it dies.
- **DoD:** each delight demoable + Sean's eyeball is the arbiter (engine truth: run the loop,
  print a take, feel the room answer); reduced-motion sweep; suites green; **this slice ends
  with the milestone's engine-truth session** — Sean walks a real run end-to-end in the browser.
- **Test impact:** intercom behavior tests (appears on print success, polite region,
  auto-dismiss, reduced-motion instant); presence tests for sub-labels ≥11px; the rest is
  visual (screenshot evidence).

### P6 — One room, every screen (consistency + narrow sweep) · **Opus 4.8 / Codex**
- **Surface:** `marquee.css`, residual `gates.css`/`boothboard.css`, a final Playwright sweep
  script (scratchpad, not committed to `web/`).
- **Work:** D10 — marquee error states to full bakelite borders (the side-stripe ban); error/
  logs treatment aligned to DESIGN §7 across screens (shared treatment, per-screen classes kept
  — no big-bang rename); **`.bb-seg:hover` scoped to segments that are actually links**
  (red-team: today every segment lights on hover but only `done` segments navigate — a false
  affordance; L5's hover-warmth work coordinates with this); confirm `.mq-new` (the inert
  `cursor:not-allowed` div) carries no interactive semantics; the <900px graceful check on
  every screen (gates aside collapse, board rows, the P1 rail — verify, fix stragglers) plus
  the short-viewport (≥600px tall) check; the final four-width screenshot pack of every
  station, checked against DESIGN §5, filed as the polish pass's closing evidence.
- **DoD:** the evidence pack (all stations × 1024/1280/1440/1920) shows one coherent room;
  no banned patterns remain (side-stripes, sub-floor type, off-token hex — the P3 grep re-run);
  suites green; both md5 guards re-verified one last time.
- **Test impact:** minimal — assertion updates where error classes change.

### Sequence

```
P1 stage geometry (Fable) ─▶ P2 behavior + honest labels ─▶ P3a tokens/literals/type-floor
   ─▶ P3b button recipe + shared primitives ─▶ P4 gates state+hierarchy
   ─▶ P5 delight (Fable, ends with engine truth) ─▶ P6 sweep
```

P1 first — the worst defect on the signature screen; P2 rides the fresh eye-gate context;
P3a/P3b before P4/P5 because both consume the recipe and tokens (dependency red-team-verified:
P4's stamp + D15 sub-labels and P5's L2 whispers all ride P3b); P5 late so delights land on
corrected geometry; P6 closes. Each slice = one TDD session + PR + review, per the standing
rhythm. If P2 proves tiny at kickoff it may ride P1's session as a second commit — never the
reverse (geometry doesn't ride a nit slice).

---

## Open decisions surfaced for Sean

Each with a recommendation (the first option). None block P1.

1. **The action-hue grammar (D8's retry split).** → **Recommended:** tungsten = commit/recover
   (approve, print, lock, error-retry — marquee's bakelite retry becomes tungsten); bakelite
   reserved for strike/destructive + the fail lamp; **"Go again" becomes a quiet control**
   (booth2 + line — sending work back is routine, not alarming). *Alternative:* keep "go again"
   bakelite (the mockup's projector-button reading) — defensible, but it spends the warning hue
   on the most common action in the room. DESIGN §2 records the recommendation; P3b implements
   whichever you ratify.
2. **Whisper sub-labels (L2) — ship at 11px, or drop?** → **Ship at 11px mono** (recommended).
   The mockups' 8.5–10px whispers violate the floor; at 11px they keep the voice and the
   contract. *Alternative:* drop them and let `?` carry discoverability (quieter, but the
   buttons lose their second voice).
3. **Futura — license/self-host now that the system is locking?** → **Keep the fallback stack
   for this milestone** (recommended). Sean-on-macOS renders Avenir Next — excellent; a licensed
   Futura is a procurement call, not a polish slice. *Optional rider:* P3 may add a `/dev/system`
   A-B toggle with a self-hosted open geometric (e.g. Jost via `@fontsource`) so the future call
   is an eyeball, not a guess. No screen ships it.
4. **Dashboard poster thumbnails / in-flight badge (G10-adjacent).** → **OUT of the polish pass**
   (recommended) — both need per-run `/status` fan-out; the marquee stays summary-only. Remains
   a named v1c item.
5. **Phone scope.** → **Ratify DESIGN §5 as written, both axes pinned** (recommended): designed
   **width** 900–2560px (below 900 everything single-columns gracefully — nothing clips or
   overlaps, down to ~600px wide); designed **height** ≥600px (the short-viewport check).
   Phone ergonomics out of scope for the polish pass. (Red-team caught the draft restating the
   600 as a width floor while DESIGN meant height — this wording is the ratified one.)
6. **State-class unification (the `mq-`/`bb-`/`gate-`/`eg-` families, D14's tail).** → **No
   standalone refactor slice** (recommended): treatments align via DESIGN §7 + P3's shared
   tokens/classes where slices already touch a file; a big-bang rename is churn without an
   engine-truth payoff.

---

## Risks

1. **P1 regresses an instrument mode.** The eye-gate's 8 test files pin behavior, not geometry —
   a DOM restructure could pass tests and still break lights-out/onion/leader visually.
   *Mitigation:* P1's DoD demands the interaction-state screenshot set (onion/diff/lights/
   leader/idle-dark) in the new geometry; Fable builds it; the kickoff names "no state-machine
   edits" as a hard boundary.
2. **P3 changes pinned pixels everywhere.** Token migration + size raises brush every screen.
   *Mitigation:* before/after station screenshots in the PR; literals migrate 1:1 (same computed
   color); the only intended visual changes are the enumerated size raises + hue unifications.
3. **P4's stage check double-guards the 409.** If the stage check is wrong, a legitimately
   actionable gate could render archival. *Mitigation:* TDD the mapping stage-per-gate
   (PLAN gate live at PLAN, archival at SCRIPT+; etc.); the 409-stale branch stays as the
   race-condition backstop, so a false-archival is visible, never a silent wrong-approve.
4. **Delight creep (P5).** The mandate's failure mode is decorating the room until it's busy
   again. *Mitigation:* the ranked list is the scope; the density gate is the review; anything
   permanent dies in review; Sean's eyeball closes the slice.
5. **The stub-fixture blind spot.** The audit ran on stub runs (flat yellow frames); real art
   changes contrast on burn-ins/wipe tags. *Mitigation:* P2's tag treatment uses the burn-in
   shadow recipe (already proven over art); the engine-truth session (P5's close) runs on a
   real-art run if one exists by then.

---

## Red-team reconciliation

An independent fresh-context adversarial pass ran against the draft — instructed to verify
every file:line claim against the tree, attack slice boundaries, and probe the zero-delta
claim. It ran the suite live (**305/305 green** — the baseline number is exact) and verified
D1–D6, D8–D13, D15, D16 in code. Findings + my calls, all folded above and marked inline:

**Refuted / corrected (fixed in this doc before convergence):**
- **D17's evidence was false as drafted** — the "absent" lamp-pool CSS ships *verbatim*
  (`gates.css:36-56`, the exact radial wash + glow values). The defect is real to the eye but
  it's a **tuning** problem; P4's work item re-specified as a retune. (The draft would have
  had a worker "add" CSS that already exists.)
- **D14's "duplicate keyframes" don't exist** — eyegate writes `animation:` shorthands over
  the *shared* keyframes; and a literal "consume `.ro-*`" migration would regress reduced
  motion (`.ro-arrive` collapses to an instant dead cut; the eye-gate's `.18s` soft-arrival
  is deliberately bespoke). P3b's motion consolidation scoped to flicker/weave/pulse only.
- **D4's "only action key without preventDefault" was false** — several branches skip it
  harmlessly; `r` is the only one with a *leak destination* (the auto-selecting input).
  Reworded so a worker doesn't spray preventDefault across branches; P2's red test asserts
  `defaultPrevented` (jsdom can't reproduce browser text insertion).
- **D6's test impact undercounted** — three pinned "ON SCREEN" assertions in three files
  (incl. `RunOverview.test.tsx:190`, which the draft missed), enumerated in P2.
- **`#101010` is ×7, not ×6** (a migration checklist off the draft would leave one behind).
- **P3's hex-only enforcement grep couldn't see D8's own headline offender** (an rgba
  literal). P3a's DoD now greps `#hex` **and** `rgba?(` with a token-triple/`color-mix()`
  mechanism + allowlist.
- **P1's fix recipe named the wrong ingredient** — the `min-height:0`s already exist; the
  missing link is that `.booth-stage` is not a flex container (and `.booth{min-height:100vh}`
  is indefinite). Recipe corrected; and because `booth.css` is every screen's ancestor, P1's
  DoD gained the app-wide layout/scroll regression check (the blast radius the draft's
  eye-gate-only evidence missed). The `.eg-beam`/`.eg-jobveil` re-anchoring named.
- **The draft's Open Decision 5 restated DESIGN §5's 600px height floor as a width floor** —
  both axes now pinned explicitly.

**New findings (adopted):**
- **D18 (missed defect, real):** idle-dark fades the retry note to 12% while the director is
  composing in it (`againOpen` absent from the idledark condition) — added to the defect
  table, assigned to P2 with its own red test.
- **`.bb-seg:hover` is a false affordance** (every segment lights; only printed ones link) —
  added to P6, and L5's delight reframed as the other half of the same rule.
- **P3 was the over-scoped slice** (not P4/P5) — pre-split into P3a/P3b, mirroring the build
  plan's U2/U4/U5 pre-splits.
- **DESIGN.md corrections:** the gate aside is 340px, not the draft's 380px (an extraction
  error a worker would have "fixed" into a real 40px layout change); §8's "instant or
  crossfade" self-contradiction resolved to crossfade-only; §4's tier-5 nesting (veil contains
  leader) stated so the z-scale work is naming, not splitting; §6's Filmstrip ring copy made
  consistent with the shared component's booth-board use.

**Confirmed unchanged:** the P1→P6 sequence and the Fable/Opus split; P1/P2 separability
(with the one-directional ride rule); the **zero-daemon-delta claim survived every probe**
(P4's stage check reads the already-fetched `RunStatus.stage`; P5's intercom composes client
data; L3's thumbnail rides the already-consumed image endpoint); the dismissed items
(leader-countdown numerals designed at `boothBoard.ts:57-58,106-107`; stub Em cards).

**Verdict (the pass's own words):** sound plan, not build-ready as drafted — the named
corrections had to fold in first. **All are folded above.** P1's kickoff can be cut now.

---

## What "done" means for the polish pass

All seven slices merged; the audit's defect table cleared (D1–D18 each closed by its named slice
or explicitly re-triaged in a slice PR); DESIGN.md's rules hold against a final grep + the
four-width evidence pack; the 305-test suite grown, never shrunk, green; backend byte-identical
(md5 guards standing); and the milestone closes the way it started — **Sean in the screening
room, running the loop, printing takes, no terminal in sight.**
