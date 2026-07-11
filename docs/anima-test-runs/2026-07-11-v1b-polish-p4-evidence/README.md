# P4 evidence — the gates read like a room

**Slice:** P4 · **Branch:** `polish/p4-gates-room` · **Date:** 2026-07-11

P4 closes D5, D15, D16, and D17. The before build is merged P3b at `2a33256`
(PR #101); the after build is this branch. The strict comparison uses the same
DONE run (`2026-06-21-spark-animatic-driven`) on both builds, read-only through
the daemon. Every after comparison therefore also proves the archival state:
the artifact remains, the quiet PRINTED/LOCKED stamp appears, and no stale live
primary is present.

## Strict before / after — all four gates, five viewports

Each cell is `before / after`.

| Gate | 1024×900 | 1280×900 | 1440×900 | 1920×900 | 1280×680 |
|---|---|---|---|---|---|
| Plan | [before](before-plan-1024x900.png) / [after](after-plan-1024x900.png) | [before](before-plan-1280x900.png) / [after](after-plan-1280x900.png) | [before](before-plan-1440x900.png) / [after](after-plan-1440x900.png) | [before](before-plan-1920x900.png) / [after](after-plan-1920x900.png) | [before](before-plan-1280x680.png) / [after](after-plan-1280x680.png) |
| Script | [before](before-script-1024x900.png) / [after](after-script-1024x900.png) | [before](before-script-1280x900.png) / [after](after-script-1280x900.png) | [before](before-script-1440x900.png) / [after](after-script-1440x900.png) | [before](before-script-1920x900.png) / [after](after-script-1920x900.png) | [before](before-script-1280x680.png) / [after](after-script-1280x680.png) |
| Storyboard | [before](before-storyboard-1024x900.png) / [after](after-storyboard-1024x900.png) | [before](before-storyboard-1280x900.png) / [after](after-storyboard-1280x900.png) | [before](before-storyboard-1440x900.png) / [after](after-storyboard-1440x900.png) | [before](before-storyboard-1920x900.png) / [after](after-storyboard-1920x900.png) | [before](before-storyboard-1280x680.png) / [after](after-storyboard-1280x680.png) |
| Animatic | [before](before-animatic-1024x900.png) / [after](after-animatic-1024x900.png) | [before](before-animatic-1280x900.png) / [after](after-animatic-1280x900.png) | [before](before-animatic-1440x900.png) / [after](after-animatic-1440x900.png) | [before](before-animatic-1920x900.png) / [after](after-animatic-1920x900.png) | [before](before-animatic-1280x680.png) / [after](after-animatic-1280x680.png) |

## Live decision placement

The live-state appendix shows the D15 hierarchy at 1440×900: each action is a
full-width P3b recipe inside the page's aside gate-card, where reading ends.

- [Plan](after-live-plan-1440x900.png)
- [Script](after-live-script-1440x900.png)
- [Storyboard](after-live-storyboard-1440x900.png)
- [Animatic](after-live-animatic-1440x900.png)

The Script fixture was authored in the pipeline's guaranteed-$0 `--stub` mode
and paused at SCRIPT. The other three are existing live gate fixtures.

## Visual and accessibility read

- **Lamp pool:** wash extent `-70px -100px`, a broader 72% × 64% tungsten pool,
  and a 90px page glow make the sheet the lit object without introducing a
  panel, border, new hue, or permanent chrome. Page ink pairs are unchanged:
  page-ink/page 13.41:1 and page-ink2/page 6.99:1.
- **Density:** the archival truth is a stamp in the existing page head; live
  actions occupy the existing aside. The crew change is one 11px whisper, and
  the derived cost copy only changes its wrapping behavior.
- **A11y browser probe:** all four live gates report one `h1`, one `main`, one
  banner, no horizontal overflow, and a logical focus order ending at the
  gate decision. The Script toggle remains before its decision; Storyboard's
  slate/beat links remain before Lock picture. No focusable archival primary
  exists.
- **Motion:** no animation or transition changed; the reduced-motion contract
  is byte-identical.

## TDD trace

- D5 RED: five failures across the four DONE routes plus `locked: true` at
  STORYBOARD. GREEN: 50/50 focused gate tests.
- D15 RED: the action was outside an existing aside and no aside existed for
  Script. GREEN: 58/58 focused shell + gate tests.
- D16 RED: the resting crew whisper was absent and the box-office derivation
  had no unit-wrap rule. GREEN: 32/32 focused board + CSS tests.
- D17 RED: the CSS contract still carried the visually flat 40/60/58/52/60px
  geometry. GREEN: the tuned wash/glow contract passed, then the browser eye
  check accepted it against `reelone-reading.html`.

## Scope proof

Final PR verification records the two full-suite runs, production build,
`server/ pipeline/ evals/` empty diff, and both md5 guards.
