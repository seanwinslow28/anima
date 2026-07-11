# P2 evidence — honest keys, honest labels

**Slice:** P2 · **Branch:** `polish/p2-honest-keys` · **Date:** 2026-07-11

**Scope:** D4 / D6 / D11 / D12 / D18 / D19; zero daemon mutation. Screenshots use the live,
read-only run `2026-07-10-v1b-eyeball` through the daemon + Vite pair from the handoff.

## D19 — fixed-room geometry

The before build is merged P1 (`9ce455e`, PR #98). P1's own after screenshots are the D19
before state: [1440×900](../2026-07-11-v1b-polish-p1-evidence/after-eyegate-normal-1440x900.png)
and [1280×680](../2026-07-11-v1b-polish-p1-evidence/after-eyegate-normal-1280x680.png).
Playwright measured the document and frame before/after:

| Viewport | Document height | Frame | Transport bottom | Result |
|---|---:|---:|---:|---|
| 1440×900 | 998 → **900** | 976×610 → 864×540 | 917 → 886 | 98px page scroll → **none** |
| 1280×680 | 966 → **680** | 805×503 → 448×280 | 885 → 666 | 286px page scroll → **none** |

After: [1440×900](after-eyegate-normal-1440x900.png) ·
[1280×680](after-eyegate-normal-1280x680.png). The frame yields to the app bar + transport +
filmstrip budget; the Em rail retains its own `overflow-y:auto` at the shortest viewport, so
the fixed room does not make its notes inaccessible. Lights-out remains the picture-only
geometry reference.

Required normal-width set: [1024](after-eyegate-normal-1024x900.png) ·
[1280](after-eyegate-normal-1280x900.png) ·
[1440](after-eyegate-normal-1440x900.png) ·
[1920](after-eyegate-normal-1920x900.png) ·
[1280×680](after-eyegate-normal-1280x680.png).

## Interaction and honesty proof

- **D4:** real-browser `R` opens the [Em-prefilled retry note](after-eyegate-retry-prefill-1440x900.png);
  Playwright read the exact prefill after the keydown, with no leaked `r`. The automated red
  test asserts the actual cancelation contract (`defaultPrevented`) plus prefill integrity.
- **D18:** after 4.2 seconds without input, the open note remains fully awake and its value is
  unchanged ([composition hold](after-eyegate-retry-awake-4s-1440x900.png)); after Escape, the
  same timer produces the intended [idle-dark room](after-eyegate-idledark-1440x900.png).
- **D6:** the normal captures show F04 as `YOUR CALL`; the tungsten ring alone names the frame
  currently staged. The three plan-named pinned assertions changed deliberately.
- **D11/D12:** [diff + `[`](after-eyegate-diff-wiped-1440x900.png) shows the raised, shadowed
  wipe tag over art; the slider announces a meaningful balance such as
  `62% — mostly TAKE 2`.
- Instrument regression set: [onion](after-eyegate-onion-1440x900.png) ·
  [lights-out](after-eyegate-lights-1440x900.png) ·
  [key sheet](after-eyegate-keys-1440x900.png). Browser console: 0 errors, 0 warnings.

## Design-contract re-check

- **Density:** no panel or permanent chrome added; the art and one decision remain the default.
- **A11y:** wipe tag now meets the 11px floor; the range communicates meaning, not a bare number;
  keyboard focus and the focused composition surface remain visible.
- **Reduced motion:** no animation or transition changed; the existing test still proves no
  timed HUD fade under `prefers-reduced-motion`.
- **Contrast:** the visual tag change uses the existing tungsten foreground and established
  black burn-in shadow; no new palette pair was introduced.
- **Impeccable:** the post-change detector reported only pre-existing warnings (including the
  marquee side-stripes already assigned to P6); it found no warning introduced by P2.
