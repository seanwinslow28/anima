# Product — ② Flow / REEL ONE (the screening room)

> The strategic context for anima's Flow interface — the browser app under `web/` that killed
> the terminal. This file answers *who/what/why*; [`DESIGN.md`](DESIGN.md) answers *how it looks*.
> The project-level soul lives in [`PHILOSOPHY.md`](PHILOSOPHY.md); this document applies it to
> the one surface a human actually touches. Written 2026-07-10 as part of the v1b design lockdown.

## Register

product

## Users

One user: **Sean — the director, the editor, the taste-keeper.** He is not "a persona"; he is
the specific human the room was built around. He sits down at night, in a dark room, at a desktop
browser, to do one job at a time: read a plan, lock a board, or judge animation. He is an animator
and a PM — fluent in both film-craft vocabulary (print it, takes, holds, dailies, leader) and
pipeline vocabulary (gates, criteria, retries). The crew he directs is the agent fleet: Maya plans,
Sam writes, Bea boards, Flo draws, Em critiques from the back row, Mo files the record.

Context that shapes every screen: he is **in a task, with taste engaged**. The interface's job is
to put the work in front of his eye and get out of the way — chrome recedes when idle and returns
when reached for. He drives keyboard-first at the eye-gate (the instrument), mouse-first on the
document gates (the reading).

## Product Purpose

② Flow is the human gate surface for anima's 10-phase pipeline. The daemon (Slices 1–5) already
serves every read and every `202 {job_id}` gate action; REEL ONE renders that contract as a
screening room. The jobs, in order of sanctity:

1. **Walk a run** — brief → plan gate → script gate → storyboard gate → [animatic] → generate,
   one lit decision at a time, with the booth board (Run Overview) as the room between gates.
2. **Judge animation *in motion*** — the eye-gate is the keystone. You cannot judge animation
   from a still; the room's sacred act is running the loop (hold `Space`, 12 fps, gate weave),
   ghosting the prior print, wiping two takes, and killing the lights. The medium is judged in
   the medium.
3. **Print it** — approve with one key, watch the circled take, let the Academy leader count the
   next picture up. Or send it back with one key and Em's note riding the retake.
4. **Never open the terminal** — a run created on the CLI is *driven* entirely from the room.
   ("The terminal is dead" is v1b's milestone contract.)

**Success looks like:** Sean reviews a full run — plan to loop — without leaving the browser,
faster than the terminal flow, and *enjoys sitting in the room*. The final arbiter is the
**engine truth**: if the loop plays smoothly and the character is recognizably itself in its
intended medium, it ships. Every screen exists in service of that one test.

## Brand Personality

**Ritual, warm, honest.** A projection booth at night — dailies culture made an interface.
Tungsten practicals in warm darkness; one impossibly bright frame; film grain over everything;
the decision verb animation directors have always used. The voice is a night crew's: *print it*,
*go again*, *the booth waits for the director*, *estimate, not a cap*. Reverent about the work,
never solemn about itself.

Three feelings, in priority order: **focus** (the frame is the only lit object in the room),
**craft** (every artifact detail — sprockets, burn-ins, slates, the leader — does real UI work),
**trust** (the room never lies: derived numbers are labelled derived, a failed job shows its rc
and log tail, a thin state reads honestly thin).

## Non-negotiables (inherited from PHILOSOPHY.md, binding on every screen)

- **The human owns taste and timing.** Every irreversible act (approve, lock, print, ingest) is
  a human keystroke behind a human gate. No screen ever auto-approves, and nothing burns compute
  until the director says so.
- **The critic proposes, never decides.** Em is a hand in the margin — verdict lamp, reasoning,
  a proposed fix that pre-fills the note *for Sean to send or edit*. She never touches the
  projector, and the UI must never render her verdict as a blocking state. Her honest boundary
  stays stated in-context: she reads stills, not motion — the loop is yours.
- **Honesty over polish.** The UI renders only what the daemon serves or what it can truthfully
  derive (and labels the derivation). No invented provenance, no fake progress bars — the leader
  is a ritual timer, not an ETA. Failed jobs surface rc + logs; busy runs name their owner.
- **The five doctrine states** on every data-bound screen: empty (an invitation), loading (a
  skeleton of the target), working (which agent + the leader), error (what happened + the one
  recovery), busy (the single-writer rule made visible). Never the happy path alone.

## Anti-references

- **The terminal.** The thing v1b killed. No CLI-reference voice, no wall-of-log defaults
  (logs arrive on tap), no monospace-everything.
- **The generic AI dashboard.** Metric-card grids, gradient accents, spinner-in-a-void loading,
  eyebrow labels over every section. REEL ONE has one metaphor and spends it everywhere; nothing
  gets added because "dashboards have one."
- **IDE-dark.** Flat dev-tool gray-dark (VS Code, Linear-dark-as-default). The booth is
  *cinematic* dark: warm-black, tungsten-lit, grained. If a surface reads as an editor theme,
  it's off-brand.
- **The click-to-generate service.** Any flow where generation starts without a human gate, or
  where the critic's verdict looks like a decision. (PHILOSOPHY: what anima refuses to become.)

## Design Principles

1. **Show, don't tell.** Default state = the art + the one decision. Everything secondary
   (cost detail, crew, legends, provenance, critic history) arrives on intent — hover, keypress,
   idle-wake — never permanently. Prefer a lit signal to a printed label: lamp > word,
   motion > description. *When in doubt, cut a panel — never shrink one.* (The density mandate
   is a review gate, not a preference.)
2. **The frame is the only lit object in the room.** Screen light is hierarchy: the work gets
   the lumens, chrome stays warm-black. On a page whose job is reading, the page is the lit
   object (one warm sheet in the dark booth).
3. **Motion is projection, not transition.** Everything arrives by fade-through-black; the loop
   runs `steps(1)` at 83 ms; the print flickers 1.5%. Motion conveys state (working, arrival,
   the circled take) — never decoration. Reduced-motion collapses to crossfades and freezes,
   never dead cuts or missing content.
4. **Ritual over chrome.** The screening-room vocabulary is the interaction model, not a skin:
   print/again are keys, the leader is the working state, the circled take is the approve
   flourish, lights-out is one key. New UI earns its place by deepening the ritual, not by
   adding controls.
5. **Keyboard-first, honestly discoverable.** Every eye-gate key has a visible toolbar button;
   `?` is the backstop; the palette (`⌘K`) jumps anywhere. Accessibility is a contract
   (WCAG 2.1 AA), not a pass.

## Accessibility & Inclusion

WCAG 2.1 AA, re-derived against the booth palette (the contrast ledger lives in
[`web/src/styles/reelone.tokens.css`](web/src/styles/reelone.tokens.css) and DESIGN.md):

- Keyboard-first; every clickable a real `<button>`/`<a>`; icon-only controls carry `aria-label`.
- Visible palette-aware focus ring (tungsten on booth, ≥3:1); never `outline: none`.
- Landmarks + one `<h1>` per screen; toggles carry `aria-pressed`; working states announce via
  polite `aria-live`; verdicts never rely on color alone (the lamp carries a `role="img"` label).
- **11px type floor** — no interface text below 11px, including whisper sub-labels and filmstrip
  captions. (Ratified in the 2026-07-10 lockdown; pre-lockdown violations are polish-plan work.)
- **Reduced motion is a first-class contract:** loop → freeze/single-step; cel-flip → crossfade
  (never a dead cut); leader → skip to done; weave/flicker → off; circled take → instant.
  Scoped so hover/press feedback survives.
- Target medium is a desktop browser ≥900px; the room is an instrument, not a phone app.
  Narrower viewports must degrade gracefully (single-column, nothing clipped), not pixel-perfectly.
