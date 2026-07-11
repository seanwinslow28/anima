# P3b evidence — the button recipe + shared primitives + the living sheet

**Slice:** P3b · **Branch:** `polish/p3b-button-recipe` · **Date:** 2026-07-11

P3b closes D13/D14 and repairs D20. The before build is merged P3a (`1fb53ec`, PR #100);
its screenshots are the `after-*` images in the adjacent
[`2026-07-11-v1b-polish-p3a-evidence`](../2026-07-11-v1b-polish-p3a-evidence/) pack. The after
build is this branch. Both use live, read-only daemon data from the main checkout.

## Every touched station — required viewport set

Each after link is 1024×900 / 1280×900 / 1440×900 / 1920×900 / 1280×680.

| Station | 1024 | 1280 | 1440 | 1920 | 1280×680 |
|---|---|---|---|---|---|
| Marquee | [after](after-dashboard-1024x900.png) | [after](after-dashboard-1280x900.png) | [after](after-dashboard-1440x900.png) | [after](after-dashboard-1920x900.png) | [after](after-dashboard-1280x680.png) |
| Booth board | [after](after-board-1024x900.png) | [after](after-board-1280x900.png) | [after](after-board-1440x900.png) | [after](after-board-1920x900.png) | [after](after-board-1280x680.png) |
| Plan gate | [after](after-plan-1024x900.png) | [after](after-plan-1280x900.png) | [after](after-plan-1440x900.png) | [after](after-plan-1920x900.png) | [after](after-plan-1280x680.png) |
| Script gate | [after](after-script-1024x900.png) | [after](after-script-1280x900.png) | [after](after-script-1440x900.png) | [after](after-script-1920x900.png) | [after](after-script-1280x680.png) |
| Storyboard gate | [after](after-storyboard-1024x900.png) | [after](after-storyboard-1280x900.png) | [after](after-storyboard-1440x900.png) | [after](after-storyboard-1920x900.png) | [after](after-storyboard-1280x680.png) |
| Animatic gate | [after](after-animatic-1024x900.png) | [after](after-animatic-1280x900.png) | [after](after-animatic-1440x900.png) | [after](after-animatic-1920x900.png) | [after](after-animatic-1280x680.png) |
| Eye-gate | [after](after-eyegate-1024x900.png) | [after](after-eyegate-1280x900.png) | [after](after-eyegate-1440x900.png) | [after](after-eyegate-1920x900.png) | [after](after-eyegate-1280x680.png) |
| System sheet | [after](after-system-1024x900.png) | [after](after-system-1280x900.png) | [after](after-system-1440x900.png) | [after](after-system-1920x900.png) | [after](after-system-1280x680.png) |

## Eye-gate instrument + interaction evidence

At 1440×900: [onion](after-eyegate-onion-1440x900.png) ·
[diff + `[`](after-eyegate-diff-wiped-1440x900.png) ·
[lights](after-eyegate-lights-1440x900.png) · [key sheet](after-eyegate-keys-1440x900.png) ·
[retry composition](after-eyegate-retry-1440x900.png) ·
[idle-dark after 4.2s](after-eyegate-idledark-1440x900.png) ·
[settled Print-it hover](after-eyegate-print-hover-1440x900.png).

Playwright computed the D13 hover from `rgb(232, 179, 106)` to
`rgb(242, 194, 132)` after the 180ms transition. Under emulated reduced motion, shared flicker
computed to `animation-name: none`, while a soft-arrival probe computed to
`fade-through-black` at `0.18s`; arrivals crossfade rather than dead-cut.

## Contract evidence

- **Button grep:** action-specific rules retain sizing/spacing only; primary/quiet/danger
  hue, border, radius, tracking, hover, active, and disabled states have one owner in
  `reelone/reelone.css`.
- **Sprocket grep:** `circle at 10px 3.5px` occurs once, in `.ro-sprocket`; marquee cards,
  board segments, and filmstrip cells consume the class.
- **Motion grep:** `animation: flicker|weave|pulse` occurs only in
  `reelone.motion.css`; the 180ms `.eg-stage--arrive-soft` remains bespoke.
- **Z grep:** no raw `z-index` integer remains under `web/src`; all occupants consume the seven
  DESIGN §4 tier tokens, with veil + leader both on tier 5.
- **Density:** no production panel or permanent chrome was added. `/dev/system` is the living
  reference surface; production screens only consolidate existing controls.
- **Contrast:** unchanged ratified pairs: on-tungsten/tungsten 10.05:1,
  on-tungsten/tungsten-bright 11.62:1, screenlight/bakelite 4.57:1,
  screenlight/danger-hover 5.87:1, text/booth2 11.35:1. All body/action pairs remain AA;
  focus remains tungsten ≥3:1.

## TDD trace

- D20 RED: merged main failed the full suite 2/5 runs and the isolated HUD file 1/20, reading
  `density` after the stage appeared. GREEN: layout-effect declaration passed the isolated
  file 30/30 and the full suite 5/5 before P3b styling began.
- Shared-contract RED: 11 failures across z tiers, recipe, sprockets, motion ownership, living
  sheet, and screen-consumption assertions. Focused GREEN: 79/79.
- Reduced-arrival RED: the browser exposed `0.01ms`; the new cascade guard failed once before
  the narrow override. GREEN: the CSS + eye-gate print suites passed 24/24, and Chromium
  computed `0.18s` under reduced motion.

## Final verification

- `npm run typecheck` — clean.
- `npm run build` — 342 modules transformed, clean production build.
- Full suite twice consecutively — **46 files / 325 tests passed** on both runs (320 → 325;
  five new named contract tests, plus existing screen assertions extended).
- `git diff origin/main -- server/ pipeline/ evals/` — empty.
- g6.1b guard — `2af75906502f1caf8857e18828ceb2e4`.
- screenwriting-voice guard — `945af824fa53b948a18ac6bf206d67ef`.
