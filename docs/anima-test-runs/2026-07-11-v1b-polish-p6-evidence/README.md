# P6 closing evidence — one room, every screen

**Date:** 2026-07-11

**Branch:** `polish/p6-one-room`

**Live seam:** Vite `:5173` over the real daemon `:8000`, read-only against the existing `runs/` tree.

## Closing four-width pack

Every station was captured at **1024×900, 1280×900, 1440×900, and 1920×900**:

| Station | Route / live run |
|---|---|
| Marquee | `/` |
| Booth board | `/runs/2026-07-11-p4-script-live` |
| Plan gate | `/runs/2026-07-10-polish-audit/plan` |
| Script gate | `/runs/2026-07-11-p4-script-live-authoring/script` |
| Storyboard gate | `/runs/2026-07-10-u4a-script-eyeball/storyboard` |
| Animatic gate | `/runs/2026-06-21-spark-animatic-run/animatic` |
| Eye-gate | `/runs/2026-07-10-v1b-eyeball/frames/4` |
| Living system sheet | `/dev/system` |

The 32 files follow `<station>-<width>x900.png`. Visual review against DESIGN §5 confirmed one
coherent room: desktop columns remain in flow, the frame/rail never overlap, burn-ins stay inside
the stage, document pages remain the lit object, and no station clips horizontally.

## Graceful and short-viewport proof

The same eight stations were captured at **600×900**, **899×900**, and **1280×600** (24 more
screenshots). The automated sweep asserts:

- `documentElement.scrollWidth - clientWidth <= 1` on every route;
- `.gate-columns`, `.bb-marquee`, `.bb-lower`, and `.eg-stagewrap` resolve to one column below
  900px whenever present;
- the eye-gate stage and rail do not intersect;
- the 1280×600 eye-gate adds zero document height beyond the viewport;
- no visible element escapes the viewport unless an ancestor intentionally contains decorative
  artwork with `overflow: hidden|clip` or provides a deliberate horizontal scroller.

The first pass failed the four narrow document gates: the lamp wash extended the page by 70px.
The narrow `-30px` inline inset was written behind a red CSS contract; the repeated **56-check
pass reports zero failures**. Machine-readable output is in `sweep-results.json`.

## D10 and shared state proof

- Marquee fetch errors and unreadable-run cards now use a full `--bakelite` edge; no 2px+ left
  or right border remains in `marquee.css`.
- Board and eye-gate read failures use the same full error edge as document-gate failures.
- `.eg-logs` and `.gate-logs` carry byte-equal declaration bodies; class names remain local.
- `.mq-new` has no button/link role, no tab stop, and no enabled interactive control.
- P5's existing `spends hover warmth only on leader segments and reel cells that navigate`
  contract remains green.

## Scope and milestone boundary

The production delta remains inside `web/`; docs record the closeout. `server/`, `pipeline/`,
and `evals/` are unchanged, and the two locked md5 guards are rechecked in the PR evidence.
P6 closes the code sweep; **Sean's engine-truth session after merge closes the milestone**.
