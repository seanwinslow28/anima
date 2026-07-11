# P3a evidence — tokens, literals, and the type floor

**Slice:** P3a · **Branch:** `polish/p3a-token-lockdown` · **Date:** 2026-07-11

P3a closes D7/D8 and the gates half of D9. The before build is merged P2 (`5ed6de2`, PR
#99); the after build is this branch. Both use the live, read-only daemon data under the main
checkout. Dashboard/board/plan/animatic/eye-gate use run `2026-07-10-v1b-eyeball`; the script
and storyboard use artifact-complete run `2026-07-10-u4a-script-eyeball-2`.

## Every station — required viewport set

Each link is a before/after pair at 1024×900, 1280×900, 1440×900, 1920×900, and 1280×680.

| Station | 1024 | 1280 | 1440 | 1920 | 1280×680 |
|---|---|---|---|---|---|
| Marquee | [before](before-dashboard-1024x900.png) / [after](after-dashboard-1024x900.png) | [before](before-dashboard-1280x900.png) / [after](after-dashboard-1280x900.png) | [before](before-dashboard-1440x900.png) / [after](after-dashboard-1440x900.png) | [before](before-dashboard-1920x900.png) / [after](after-dashboard-1920x900.png) | [before](before-dashboard-1280x680.png) / [after](after-dashboard-1280x680.png) |
| Booth board | [before](before-board-1024x900.png) / [after](after-board-1024x900.png) | [before](before-board-1280x900.png) / [after](after-board-1280x900.png) | [before](before-board-1440x900.png) / [after](after-board-1440x900.png) | [before](before-board-1920x900.png) / [after](after-board-1920x900.png) | [before](before-board-1280x680.png) / [after](after-board-1280x680.png) |
| Plan gate | [before](before-plan-1024x900.png) / [after](after-plan-1024x900.png) | [before](before-plan-1280x900.png) / [after](after-plan-1280x900.png) | [before](before-plan-1440x900.png) / [after](after-plan-1440x900.png) | [before](before-plan-1920x900.png) / [after](after-plan-1920x900.png) | [before](before-plan-1280x680.png) / [after](after-plan-1280x680.png) |
| Script gate | [before](before-script-1024x900.png) / [after](after-script-1024x900.png) | [before](before-script-1280x900.png) / [after](after-script-1280x900.png) | [before](before-script-1440x900.png) / [after](after-script-1440x900.png) | [before](before-script-1920x900.png) / [after](after-script-1920x900.png) | [before](before-script-1280x680.png) / [after](after-script-1280x680.png) |
| Storyboard gate | [before](before-storyboard-1024x900.png) / [after](after-storyboard-1024x900.png) | [before](before-storyboard-1280x900.png) / [after](after-storyboard-1280x900.png) | [before](before-storyboard-1440x900.png) / [after](after-storyboard-1440x900.png) | [before](before-storyboard-1920x900.png) / [after](after-storyboard-1920x900.png) | [before](before-storyboard-1280x680.png) / [after](after-storyboard-1280x680.png) |
| Animatic gate | [before](before-animatic-1024x900.png) / [after](after-animatic-1024x900.png) | [before](before-animatic-1280x900.png) / [after](after-animatic-1280x900.png) | [before](before-animatic-1440x900.png) / [after](after-animatic-1440x900.png) | [before](before-animatic-1920x900.png) / [after](after-animatic-1920x900.png) | [before](before-animatic-1280x680.png) / [after](after-animatic-1280x680.png) |
| Eye-gate | [before](before-eyegate-1024x900.png) / [after](after-eyegate-1024x900.png) | [before](before-eyegate-1280x900.png) / [after](after-eyegate-1280x900.png) | [before](before-eyegate-1440x900.png) / [after](after-eyegate-1440x900.png) | [before](before-eyegate-1920x900.png) / [after](after-eyegate-1920x900.png) | [before](before-eyegate-1280x680.png) / [after](after-eyegate-1280x680.png) |
| System sheet | [before](before-system-1024x900.png) / [after](after-system-1024x900.png) | [before](before-system-1280x900.png) / [after](after-system-1280x900.png) | [before](before-system-1440x900.png) / [after](after-system-1440x900.png) | [before](before-system-1920x900.png) / [after](after-system-1920x900.png) | [before](before-system-1280x680.png) / [after](after-system-1280x680.png) |

The breakpoint proof adds 920×900 pairs for every two-column document gate: Plan
([before](before-plan-920x900.png) / [after](after-plan-920x900.png)), Script
([before](before-script-920x900.png) / [after](after-script-920x900.png)), Storyboard
([before](before-storyboard-920x900.png) / [after](after-storyboard-920x900.png)), and Animatic
([before](before-animatic-920x900.png) / [after](after-animatic-920x900.png)). Before P3a they
collapse under the drifted 960px rule; after P3a they remain two-column until the ratified 900px
boundary.

## Eye-gate instrument regression

All pairs are confirmed 1440×900: onion
([before](before-eyegate-onion-1440x900.png) / [after](after-eyegate-onion-1440x900.png)),
diff + `[` ([before](before-eyegate-diff-wiped-1440x900.png) / [after](after-eyegate-diff-wiped-1440x900.png)),
lights ([before](before-eyegate-lights-1440x900.png) / [after](after-eyegate-lights-1440x900.png)),
key sheet ([before](before-eyegate-keys-1440x900.png) / [after](after-eyegate-keys-1440x900.png)),
retry composition ([before](before-eyegate-retry-1440x900.png) / [after](after-eyegate-retry-1440x900.png)),
and idle-dark after 4.2s ([before](before-eyegate-idledark-1440x900.png) / [after](after-eyegate-idledark-1440x900.png)).
The only console error in either browser session is the pre-existing missing `/favicon.ico` 404.

## Intended visual delta — exhaustive

- Six remaining floor violations rise to 11px: `.gate-approve small` 8.5→11,
  `.ro-empty` 8.5→11, `.mq-cta-mark--print` 9→11, `.ro-cap` 9.5→11,
  `.syssheet-sw` 10.5→11, and `.syssheet button` 10.5→11. P2 had already raised the seventh,
  `.eg-wipe-tag`, to 11px; P3a verifies it stays compliant. Filmstrip captions may re-wrap
  inside their existing cells.
- The near-black filmstrip/board wells unify `#0E0B11` to `--booth-deep` (`#0B080D`);
  marquee retry hover unifies `#D3543F` to `--bakelite`; the failed flow-note border unifies
  its drifted translucent red to full `--bakelite`.
- The expressly requested gate boundary moves 960→900; the 920px pairs above are the only
  structural layout shift.

All other literal replacements are computed-value preserving: exact color tokens replace exact
hex values, and every glow wash retains its original channels and alpha through a named
`--*-rgb` triple. The 100-image review found no other shift, clipping, or density change.

## Literal allowlist and contrast

The two-pattern DoD audit is manual PR evidence, deliberately not CI-wired. Hex matches are
allowed only in `web/src/styles/tokens.css` and `web/src/styles/reelone.tokens.css`. Every
non-token-file `rgb(`/`rgba(` match must be exactly `rgba(var(--*-rgb), alpha)` using one of:
`--black-rgb`, `--booth-shadow-rgb`, `--booth-deep-rgb`, `--on-tungsten-rgb`, `--booth-rgb`,
`--booth2-rgb`, `--page-ink-rgb`, `--tungsten-rgb`, `--screenlight-rgb`. No free channel triple
remains.

Recomputed WCAG pairs: on-tungsten/tungsten **10.05:1**;
on-tungsten/tungsten-bright **11.62:1**; bakelite/booth **3.83:1**;
bakelite/booth-deep **4.06:1**; screenlight/booth-deep **18.54:1**;
text/booth-deep **13.91:1**. Body pairs remain AA; semantic borders/focus accents remain ≥3:1.

## Contract re-check

- **Density:** no panel, control, permanent chrome, or copy was added.
- **A11y:** all seven audited selectors are ≥11px; all changed text pairs remain AA.
- **Reduced motion:** no animation or transition changed; arrivals retain their existing
  crossfade behavior.
- **Tests/build:** baseline 316 → **320** (four named P3a guards); the exact full suite passed
  **320/320 twice consecutively** in the final quiet-process flake check; `npm run build`
  transformed 342 modules cleanly. One earlier run under the three live screenshot servers
  reproduced merged P2's intermittent `EyeGate.hud.test.tsx` `full`/`density` race that was also
  observed before any P3a edit; P3a does not touch that test or behavior.
- **Scope:** production changes are confined to `web/src`; `server/`, `pipeline/`, and `evals/`
  remain byte-identical, and both locked md5 guards remain unchanged.
