# DESIGN.md — the REEL ONE design system (② Flow, `web/`)

> **This is a lockdown, not a proposal.** REEL ONE shipped across v1b (PRs #86–#96); this file
> formalizes the system that exists — extracted from `web/src/styles/reelone.tokens.css`,
> `reelone.motion.css`, `web/src/reelone/`, `web/src/booth/`, and the four ratified mockups in
> `docs/active/2026-07-09-v1b-elevate-directions/` — and fills the gaps the build left unstated
> (responsive rules, spacing rhythm, state patterns, z-scale, token discipline). Where the
> shipped code deviates from a rule below, the rule wins and the deviation is a polish-plan
> work item ([`docs/active/2026-07-10-v1b-polish-plan-CONVERGED.md`](docs/active/2026-07-10-v1b-polish-plan-CONVERGED.md)).
> Strategic context: [`PRODUCT.md`](PRODUCT.md). Living reference render: `/dev/system`.

## 1. Theme — the projection booth

**One theme. Dark, warm, grained — cinematic-dark, not IDE-dark.** There is no light mode and
none is planned: the booth *is* the identity. The one warm surface is the **lit page** (document
gates only) — a sheet of paper under a lamp in a dark room. Scene sentence: *Sean, alone at
night, desktop browser, judging animation the way a director watches dailies.*

Scoping rule (load-bearing): **all REEL ONE tokens live on `.reelone`, never `:root`.**
`BoothShell` carries the class; v1a's warm `:root` tokens (`tokens.css`) stay defined for the
legacy screen and MUST NOT be re-pointed. Any new screen opts in by rendering inside the shell.

## 2. Color — the booth palette

Tokens verbatim from `reelone.tokens.css` (names are canon; they port from the mockups):

| Token | Value | Role |
|---|---|---|
| `--booth` | `#141018` | the room — body surface |
| `--booth2` | `#1D1722` | raised surface (cards, rails, toolbar buttons) |
| `--booth3` | `#251E2B` | highest surface (chips, hover) |
| `--line` | `#332A3C` | rules + borders |
| `--tungsten` | `#E8B36A` | **the practical** — primary action, focus ring, "now" marker |
| `--tungsten-dim` | `#8A6F4D` | dimmed practical (secondary accents, ghost tags) |
| `--screenlight` | `#FFF6E4` | projected light — display headings, the lit frame's glow |
| `--print` | `#7FA96B` | lamp: approve / PRINT |
| `--hold` | `#D9A441` | lamp: Em's HOLD / busy states |
| `--bakelite` | `#C24838` | lamp: fail / strike / the projector's red switch |
| `--text` | `#DDD5E0` | body text |
| `--mute` | `#8F8798` | secondary text |
| `--page` `--page-ink` `--page-ink2` `--page-rule` | `#F7EFDC` `#2B2417` `#57503F` `#C9BB98` | the lit page set (document gates only) |

**Color strategy: committed.** The booth carries the whole surface; tungsten is the one accent
doing primary-action work; the three lamps are **semantic and reserved** — never spent on
decoration. One reserved warning hue on any stage (the two-reds rule): the onion ghost renders
cool/desaturated, never in a lamp color, so a lamp always means what it says.

**Contrast ledger (WCAG 2.1 AA, re-derived against the booth — recorded in the tokens header):**
text/booth 13.13:1 · screenlight/booth 17.51:1 · mute/booth 5.45:1 (4.68:1 on booth3 — body-safe
on every booth surface) · tungsten/booth 9.93:1 (focus ring ≥3 ✓) · page-ink/page 13.41:1 ·
page-ink2/page 6.99:1. `tungsten-dim` (3.99) and `bakelite` (3.83) are UI/accent hues (≥3), not
body-text colors. **Any new pair gets a ratio computed before it ships; any visual change
re-checks its pair.**

**Token discipline (normative, new in this lockdown):**
- **No new hex outside the token files.** The shipped near-blacks and button colors are hereby
  named: `--booth-deep: #0B080D` (the true-black stage/leader well), `--sprocket: #241D2C`
  (perforation dots), `--on-tungsten: #101010` (text on a tungsten fill), `--tungsten-bright:
  #F2C284` (tungsten hover). Glow washes derive via a real mechanism — `color-mix()` or
  `--*-rgb` channel-triple variables — never free hex **and never free rgba channel-triples**
  (a hand-typed `rgba(232,179,106,…)` drifts silently the day the token moves). Pre-lockdown
  literals migrate in the polish pass.
- **Error/fail borders use `--bakelite`** — one red, everywhere. (The eye-gate's
  `rgba(207,106,76,.55)` failed-border is a deviation.)
- **Hue grammar for actions:** tungsten = commit/recover (approve, print, lock, retry-after-error);
  bakelite = strike/destructive and the *fail* lamp; "go again" is a **quiet control**
  (booth2 + line, like the toolbar), not a filled primary — sending work back is routine, not
  alarming. *(Open decision 1 in the polish plan; this line records the recommendation.)*

## 3. Typography — three stacks, three jobs

| Stack | Token | Job |
|---|---|---|
| Futura → Avenir Next → Helvetica Neue → Arial | `--display` | everything — the SMPTE leader's own face. Tracked caps are the house voice. |
| SF Mono → Menlo → Consolas | `--tc-mono` | timecode, burn-ins, IDs, cost figures, IR cites, field values |
| Georgia | `--page-serif` | the lit page's prose **only** — a deliberate register break: documents read like documents |

No licensed webfont ships; the fallback stack is the v1b decision (build-plan Open Decision 8).
Do not add a fourth stack; do not use `--display` for prose paragraphs on the lit page.

**Scale (fixed rem/px, product register — no fluid type except the two display moments):**

- Display: booth-board hero `clamp(24px, 3.6vw, 38px)`; leader numeral `min(30vh, 190px)`.
  These are the only two clamps in the system.
- Headings/titles: 24 / 22 / 18 / 17 / 16.
- UI text: 14 (body default) / 13 / 12.5 / 12 / 11.5.
- **Floor: 11px. Nothing below it, ever** — including whisper sub-labels, filmstrip captions,
  wipe tags, and swatch labels. (Seven pre-lockdown violations, 8.5–10.5px, are polish work.)

**Tracking register (the house signature):** wordmark `.34em` · primary buttons `.26em` · labels/
eyebrows `.22em` · button/chip text `.18em` · titles `.12–.2em` · mono lines `.1–.18em`. Tracked
`text-transform: uppercase` is the default for labels, titles, and buttons; sentence-case is for
prose and Em's reasoning. Never track lowercase prose.

## 4. Layout, spacing, radius

**Geometry:** every screen is `BoothShell` (app bar + film grain + `<main class="booth-stage">`).
Content patterns in use — the marquee grid `repeat(auto-fill, minmax(260px, 1fr))`; the
booth-board column `max-width: 1180px` with `1fr 320px` split rows; the gate two-column
`minmax(0, 1.2fr) 340px` (page + aside; the mockup drew 380 — 340 is the shipped, ratified
value); the eye-gate stage/transport stack. Flex for 1D,
grid for 2D; no nested cards.

**Spacing rhythm (named canon — the shipped values, now normative):** `26 / 16 / 12 / 8 / 6`
— section gap 26, panel padding 26–30, in-panel gap 12–16, row gap 8, chip gap 6. Stay on
whole-px steps of this rhythm; no new `.5px` spacing. (The v1a `--sp-*` scale is dead — do not
revive it; the rhythm above is the booth's own.)

**Radius:** the booth's house radius is **2px** (chips, buttons, cards, focus ring) and `50%`
for dots/lamps. The v1a `--r-*` tokens are dead in the booth. Big rounding reads as consumer-web,
not equipment.

**Z-scale (named, normative — raw integers were shipped, these tiers are now the contract):**

| Tier | Value | Occupants |
|---|---|---|
| grain / stage | 1 | `.ro-grain`, `.booth-stage` |
| chrome | 2 | `.booth-appbar` |
| stage furniture | 4 | the Em rail |
| stage overlays | 5 | the leader, the job veil (nested — the veil *contains* the leader; one tier, not a conflict) |
| summoned sheets | 6 | the cheat sheet |
| takeover | 8 | lights-out |
| palette | 10 | `⌘K` backdrop |

New layers slot into a tier; never a new arbitrary integer, never 999.

## 5. Responsive contract (new in this lockdown)

The room is a **desktop instrument**: designed range 900–2560px wide, ≥600px tall.

- **One breakpoint token: 900px.** Two-column screens (gates, booth-board rows, the eye-gate
  stage+rail) collapse to one column below it. (The gates' shipped 960 is a deviation — unify.)
- **No absolutely-positioned siblings that can collide.** Anything that must share a row with
  variable-width content lives in flex/grid flow. Specifically: the eye-gate's Em rail is a
  **grid column** (stage `1fr` + rail `~280px`) above 900px, in-flow below — never an absolute
  overlay over the transport, the wipe controls, or the provenance line. The two burn-in lines
  share one flex row (`justify-content: space-between`) inside the frame edge — they truncate
  (`text-overflow: ellipsis`) before they collide.
- **The stage fills its room.** The eye-gate frame scales with the viewport — the height chain
  from `BoothShell` down is real (`min-height: 0` flex all the way), target `max-height: 74vh`,
  `aspect-ratio: 16/10`, `max-width` bounded by the stage column. The lights-out geometry is the
  reference: normal mode should approach it, minus chrome. A fixed-size postage-stamp frame in a
  sea of booth is a defect, not restraint.
- Below 900px nothing may clip or overlap; summoned sheets size as `min(<design px>, 92vw)`.
  Phone-first ergonomics are explicitly out of scope (PRODUCT.md).

## 6. Components (the primitives — `web/src/reelone/`, `booth/`, `screens/gates/`)

Signature primitives (keep these; compose, don't fork): `<FilmGrain>` (aria-hidden fixed grain,
5%) · `<Lamp verdict>` (PRINT/HOLD/fail — `role="img"`, the lit signal before a word) ·
`<Leader onDone>` / `<RitualLeader>` (the 3-2-1 clock-sweep — **the only working animation in
the system**; reduced-motion fires `onDone` immediately) · `<CircledTake>` (grease-pencil
ellipse on approve) · `<Timecode>` / `<BurnIn>` (mono burn-ins; TC = frame × hold @ 12 fps) ·
`<Filmstrip>` (sprocketed reel; statuses printed/working/eye/pending; the ring marks **the
frame the room is at** — on the eye-gate that's the staged frame, on the booth board the run's
current frame — and the caption marks the frame's *own* state: `YOUR CALL` for a take awaiting
the director, never `ON SCREEN` unless it is) · shell: `BoothShell` / `HudHost`
(idle-wake, per-screen dim level) / `CommandPalette` (full listbox-in-dialog ARIA) · gates:
`GateShell` (stamp/title/byline/aside/actions) · `StageToolbar` (every key's visible button,
`aria-pressed` toggles) · `EmReadout` (verdict lamp + reasoning + proposed fix + cites +
the honest boundary line) · `RetryNoteRow` (prefill + from-Em attribution; Enter/Esc) ·
`OnionSkin` (cool ghost + role tag) · `DiffWipe`/`WipeControls` (labelled slider + `[`/`]`).

**Component rules:**
- Every interactive component ships default / hover / focus-visible / active / disabled states.
  One primary-button recipe (tungsten fill, `--on-tungsten` text, `--tungsten-bright` hover,
  2px radius, `.26em` caps) — screens consume it, never re-derive it.
- Buttons are real `<button>`s; key hints (`.eg-kx`) are `aria-hidden` beside the label, never
  the label itself.
- The sprocket strip is **one shared class**, not per-screen copies.
- Range inputs carry `aria-valuetext` naming the position meaningfully (e.g. "62% — mostly
  take 2").

## 7. State patterns — the five doctrine states, one vocabulary

Every data-bound screen builds all five (empty / loading / working / error / busy). The visual
canon, regardless of screen prefix:

- **Empty = an invitation** in a dashed `--line` border, mono, quiet ("No cuts on the reel
  yet." / "a take that never developed"). Collapsed intent-reveal panels must still look
  *intentional* at rest (a whisper line, not a bare header on a void).
- **Loading = a skeleton of the target screen**, never a spinner. Skeleton geometry mirrors the
  real layout.
- **Working = the leader + the named agent** ("Flo is drawing F04"), `aria-live` polite; logs
  on tap. The leader is a ritual timer, never a fake ETA.
- **Error = what happened + the one recovery.** Full `--bakelite` border, honest rc + log tail,
  a single tungsten recovery action. No "Error:", no first person, no silent swallow.
- **Busy = the single-writer rule made visible.** `--hold` border, names the owning job, offers
  "watch it".
- **Printed/locked (the archival read):** a gate whose stage has already moved on renders as a
  record — the artifact + a LOCKED/PRINTED mark — with **no live primary action**. Revisiting
  history must never present a button that would 409.

State classes stay per-screen (`mq-` `bb-` `gate-` `eg-`) for now, but their *treatments* follow
this table exactly; unifying the families is refactor work only if a slice is already in the file.

## 8. Motion — projection physics

Primitives (`reelone.motion.css` — consume the `.ro-*` utilities; do not re-declare keyframes
per screen): `flicker` 1.7s (the print breathes, ~1.5%) · `weave` .34s `steps(2)` (only while
the loop runs) · `pulse` 1.4s (working dots) · `fade-through-black` .45s ease-out (**the**
arrival; `.18s` linear for soft intra-stage swaps) · `circledraw` .5s ease-out (approve) ·
the loop itself is JS at **83 ms `steps(1)`** (12 fps), hold-to-run.

**Duration/easing canon:** micro-feedback 150–200ms `ease`/`ease-out`; arrivals 450ms; HUD
fades 600–800ms; ritual (leader count) 700ms/beat. Ease-out only — no bounce, no elastic, no
`ease-in`. Motion conveys state (arrival, working, approve, running); anything else is cut.

**Reduced-motion contract (DoD on every visual change):** loop → freeze/single-step ·
cel-flip/arrival → a short crossfade (never a dead cut, never missing content — "instant" is a
dead cut; the eye-gate's `.18s` soft arrival is the reference) ·
leader → skip to done · weave/flicker/pulse → off · circled take → drawn instantly · idle-dark
→ chrome stays. Scoped to animations and long transitions so hover/press feedback survives.

## 9. The summonable HUD + density doctrine

Per-screen dim levels (D-B): the **eye-gate** opts into full idle-dark (3s → chrome to 12%,
any input wakes; lights-out `L` is the deliberate inverse); **document gates and the board**
use intent-reveal (`[data-reveal]` hover/focus discloses cost detail, crew, slate detail) but
never timed-fade content someone is reading. The density gate is a review question on every
change: *what can this screen stop saying?* Default = the art + the one decision; secondary on
intent; lamp > word; cut a panel, don't shrink it.

## 10. Copy voice

Screening-room register, lowercase-mono whispers, film-crew verbs. Canonical strings: `Print it`
(⏎) · `Go again` (R · the note rides the retake) · `Lock picture` · `To the screening` ·
`estimate, not a cap` · `Nothing burns compute until you approve` · `She reads stills, not
motion — the loop is yours` · `YOUR CALL` (a take waiting on the director) · `ON SCREEN` (the
frame on the stage, and only that frame) · busy: "This run is busy — view the running job" ·
empty reel: "No cuts on the reel yet." Toasts read like the booth intercom ("F03 TAKE 2 —
PRINTED. $0.07 to the ledger."). Numbers stay honest: derived figures carry `≈` and say
`derived`.

## 11. Testing + guard rails

Credential-free MSW tests per screen (five states + interactions); `/dev/system` renders the
living palette/type/lamp/leader sheet; contrast pairs recorded in the tokens header; the
`.reelone` scoping, the dual-Vite config, and the v7 router flags are structural and do not
move. `server/`, `pipeline/`, `evals/` are out of bounds for any design change.
