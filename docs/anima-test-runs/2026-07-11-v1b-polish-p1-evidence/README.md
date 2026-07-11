# P1 evidence — the stage owns the room

**Slice:** P1 · **Branch:** `polish/p1-stage-geometry` · **Date:** 2026-07-11

**Scope:** D1 / D2 / D3 / D9-eye-gate; zero daemon mutation; screenshots use the live
read-only run `2026-07-10-v1b-eyeball` unless named otherwise.

## Geometry proof

The before build is `origin/main` at `64f93bb`; the after build is this branch. Playwright
measured the rendered boxes at the five required viewports:

| Viewport | Before frame | After frame | Rail/transport overlap | Burn-in overlap | Horizontal overflow |
|---|---:|---:|---|---|---|
| 1024×900 | 352×220 | 560×350 | yes → **no** | yes → **no** | yes → **no** |
| 1280×900 | 352×220 | 816×510 | yes → **no** | yes → **no** | yes → **no** |
| 1440×900 | 352×220 | 976×610 | yes → **no** | yes → **no** | yes → **no** |
| 1920×900 | 352×220 | 1066×666 | yes → **no** | yes → **no** | yes → **no** |
| 1280×680 | 352×220 | 805×503 | yes → **no** | yes → **no** | yes → **no** |

Visual comparison: [before at 1440](before-eyegate-w1440.png) ·
[after at 1440](after-eyegate-normal-1440x900.png).

Required after set: [1024](after-eyegate-normal-1024x900.png) ·
[1280](after-eyegate-normal-1280x900.png) ·
[1440](after-eyegate-normal-1440x900.png) ·
[1920](after-eyegate-normal-1920x900.png) ·
[1280×680](after-eyegate-normal-1280x680.png).

Below the 900px collapse, the rail is in flow and the page has no horizontal overflow at
[800px](after-eyegate-narrow-800x900.png) or
[600px](after-eyegate-narrow-600x900.png); the summoned sheet stays within 92vw at
[600px](after-eyegate-cheat-600x900.png).

## Interaction-state proof

Each mode was exercised against the live app. The leader capture intercepts the approve and job
poll requests inside Playwright, so it proves the real job-veil rendering without writing to the
run.

- [Onion](after-eyegate-onion-1440x900.png)
- [Diff + `[` wipe movement](after-eyegate-diff-wiped-1440x900.png)
- [Lights-out](after-eyegate-lights-1440x900.png)
- [Cheat sheet](after-eyegate-keys-1440x900.png)
- [Retry note](after-eyegate-retry-1440x900.png)
- [Idle-dark after 4 seconds](after-eyegate-idledark-1440x900.png)
- [Leader/job veil](after-eyegate-leader-1440x900.png)

The veil deliberately belongs to `.eg-stagecol`: it covers the projected frame during a commit
and leaves the in-flow Em rail visible. No state-machine code changed. The existing eight
EyeGate behavior suites stayed green unchanged; `EyeGate.layout.test.tsx` adds six structural
assertions for the height chain, app-wide flex-child sizing, stage/rail grid, burn-in row,
cheat-sheet clamp, and narrow beam bound.

## App-wide layout and scroll regression proof

The `booth.css` flex-link touches every screen. The first live pass caught a marquee shrink-wrap
regression; a new red test pinned direct-child sizing before the fix. Final Playwright metrics
match main exactly and show no horizontal overflow:

| Station | Before / after scroll size @ 1440×900 | Result |
|---|---:|---|
| Marquee | 1440×900 / 1440×900 | no page scroll; four-column grid preserved |
| PLAN booth board | 1440×900 / 1440×900 | no page scroll; board geometry preserved |
| Long plan gate | 1440×3304 / 1440×3304 | vertical scroll preserved |
| Long script gate | 1440×2665 / 1440×2665 | vertical scroll preserved |
| Long storyboard gate | 1440×1916 / 1440×1916 | vertical scroll preserved |

Before/after pairs: [marquee before](before-marquee-1440x900.png) /
[after](after-marquee-1440x900.png) · [board before](before-board-plan-1440x900.png) /
[after](after-board-plan-1440x900.png) · [long plan before](before-long-plan-1440x900.png) /
[after](after-long-plan-1440x900.png) · [long script before](before-long-script-1440x900.png) /
[after](after-long-script-1440x900.png) ·
[long storyboard before](before-long-storyboard-1440x900.png) /
[after](after-long-storyboard-1440x900.png).

## Design-contract re-check

- **Density:** no panel or permanent chrome was added; the frame gained the room and Em remains
  the one in-flow secondary column.
- **A11y:** DOM semantics and interaction behavior are unchanged; burn-ins now truncate before
  collision, and 600/800px render with no clipped horizontal canvas.
- **Reduced motion:** no animation, transition, or reduced-motion rule changed.
- **Contrast:** layout-only change; every foreground/background pair is unchanged.
- **Impeccable:** product-register layout assessment ran in the main context (delegation was not
  authorized); the scoped post-change detector returned `[]`.
