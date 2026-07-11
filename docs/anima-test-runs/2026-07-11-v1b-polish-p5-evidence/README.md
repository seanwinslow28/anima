# P5 evidence — deepen the ritual

**Slice:** P5 · **Branch:** `polish/p5-deepen-ritual` · **Date:** 2026-07-11

P5 ships all six delights in their ranked order. The evidence run is the local,
guaranteed-$0 `2026-07-10-v1b-eyeball` fixture, served through the real daemon and
Vite app. Production changes remain inside `web/`; this directory and the
status/changelog edits are evidence only.

## Booth-board read

The same REVIEW_FRAME state at four widths proves the current-frame bleed,
leader/reel density, and unchanged responsive room:

- [1024px](board-1024.png)
- [1280px](board-1280.png)
- [1440px](board-1440.png)
- [1920px](board-1920.png)

The hero bleed reuses the already-served current-frame URL, is rotated −4° at
0.16 opacity, clips off the Now screening corner, and is `aria-hidden` with an
empty alt. It is artwork inside the existing hero—not new permanent chrome.

## Delight and interaction proof

| Rank | Delight | Browser evidence | A11y + reduced-motion contract |
|---|---|---|---|
| L1 | Booth intercom | [PRINTED line](intercom.png) | One shared route-persistent `role="status"`, `aria-live="polite"`, `aria-atomic="true"` region; pointer-inert; 2.6s dismissal; animation removed under reduced motion. Tests pin the exact print/again copy and timer. |
| L2 | Primary whispers | [Eye gate, 1280×680](eyegate-1280x680-active.png) | Visible text—not pseudo-content—at 11px mono. Tests pin `⏎ · circle the take`, `R · the note rides along`, and `re-validates · then it's the camera's`, plus the ≥11px floor. |
| L3 | Hero thumbnail bleed | [Board, 1440px](board-1440.png) | Decorative, `aria-hidden`, empty alt, existing frame image only; no motion. |
| L4 | Busy ritual | [Rolling…](rolling-cta.png) | CTA keeps link semantics, becomes `aria-disabled` during the 1.2s handoff, and modified clicks remain native. Reduced motion navigates immediately. The crew dot is decorative after the working agent's readable name and is test-pinned to live-job ownership. |
| L5 | Honest hover warmth | [linked leader](leader-hover-linked.png) · [linked reel cell](reel-hover-linked.png) | Only real links receive the linked class and hover treatment. Non-link segments and pending cells remain inert in DOM and CSS contract tests. |
| L6 | Idle halo swell | [1280×680 active](eyegate-1280x680-active.png) / [idle](eyegate-1280x680-idle.png) · [1440×900 active](eyegate-1440x900-active.png) / [idle](eyegate-1440x900-idle.png) | The existing stage shadow rises slightly as chrome fades. Reduced motion suppresses the timed idle state and explicitly resets the halo variables with no transition. |

## Density gate

- Intercom and Rolling are transient; the crew dot exists only while a named
  crew member is working; hover warmth is summoned only over an actual link;
  the glow swell exists only in the already-summonable idle-dark state.
- Whispers live inside the existing primary controls. The hero bleed is
  decorative frame art inside the existing board hero. No panel, toolbar,
  badge, or decision-blocking layer was added.
- Browser console check: zero errors. The decision terminal remains above the
  idle effect, and the intercom is fixed, pointer-inert, and outside terminal
  flow.

## TDD trace

- L1 RED pinned one shared polite live region, exact decision feedback, and
  2600ms dismissal; GREEN covered shell persistence and print/again success.
- L2 RED pinned all three whispers and the numeric 11px mono recipe.
- L3–L4 RED pinned decorative image semantics, active crew ownership, the
  1.2s navigation delay, modified clicks, and immediate reduced-motion travel.
- L5 RED pinned link-only reel semantics and selectors that cannot warm inert
  leader/reel cells.
- L6 RED pinned the stronger idle halo variables plus the reduced-motion reset.

## Scope proof

Final PR verification records two full-suite runs, a production build,
`server/ pipeline/ evals/` empty diff, both md5 guards, and `git diff --check`.
