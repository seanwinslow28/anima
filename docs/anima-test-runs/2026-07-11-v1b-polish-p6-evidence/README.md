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
The full sweep was repeated after the final visual implementation in commit `1b1871e`; its
deterministic screenshots and result payload remained byte-identical.

## D10 and shared state proof

- Marquee fetch errors and unreadable-run cards now use a full `--bakelite` edge; no 2px+ left
  or right border remains in `marquee.css`.
- Board and eye-gate read failures use the same full error edge as document-gate failures.
- `.gate-logs`, `.eg-logs`, and `.mq-logs` keep their per-screen names but consume one shared
  declaration in `reelone.css`; unreadable-run cards expose the daemon's error tail and one
  working `Reread runs` recovery.
- `.mq-new` has no button/link role, no tab stop, and no enabled interactive control.
- P5's existing `spends hover warmth only on leader segments and reel cells that navigate`
  contract remains green.

`marquee-error-1280x900.png` is the final error-state browser proof, driven by a controlled
daemon `RunError` response after commit `1b1871e`. `marquee-error-proof.json` records the served
tail, the `Reread runs` action, and four identical `rgb(194, 72, 56)` bakelite border edges.

## Final verification ledger

The closing commands were rerun after the last implementation change:

```text
web $ npx vitest run --reporter=dot   # pass 1
Test Files  47 passed (47)
Tests       349 passed (349)

web $ npx vitest run --reporter=dot   # flake pass
Test Files  47 passed (47)
Tests       349 passed (349)

web $ npm run build
✓ 344 modules transformed.
✓ built

$ git diff --exit-code origin/main -- server/ pipeline/ evals/
(empty)

$ md5 -q evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md
2af75906502f1caf8857e18828ceb2e4
$ md5 -q pipeline/agents/prompts/sean-screenwriting-voice.md
945af824fa53b948a18ac6bf206d67ef

$ rg -n '#[0-9A-Fa-f]{3,8}\b' web/src --glob '*.css' --glob '*.ts' --glob '*.tsx' | rg -v '^(web/src/styles/(reelone\.)?tokens\.css|web/src/styles/reelone\.test\.ts|web/src/screens/dev/SystemSheet(\.test)?\.tsx):' || true
(empty)
$ rg -n 'rgba?\(' web/src --glob '*.css' --glob '*.ts' --glob '*.tsx' | rg -v 'rgba\(var\(--[a-z0-9-]+-rgb\),' | rg -v '^web/src/screens/dev/SystemSheet\.tsx:' || true
(empty)

$ rg 'circle at 10px 3.5px' web/src --glob '*.css'
web/src/reelone/reelone.css:164: radial-gradient(circle at 10px 3.5px, var(--sprocket) 2.6px, transparent 2.8px)
$ rg 'animation:\s*(flicker|weave|pulse)' web/src --glob '*.css'
web/src/styles/reelone.motion.css:40:.ro-flicker { animation: flicker 1.7s infinite; }
web/src/styles/reelone.motion.css:41:.ro-weave { animation: weave .34s steps(2) infinite; }
web/src/styles/reelone.motion.css:42:.ro-pulse { animation: pulse 1.4s infinite; }
$ rg 'z-index:\s*[0-9]' web/src --glob '*.css'
(empty)
$ rg 'border-(left|right):\s*[2-9]px' web/src/styles/marquee.css
(empty)

$ jq -c '{checks:length, failures:([.[] | select(.failures | length > 0)] | length)}' docs/anima-test-runs/2026-07-11-v1b-polish-p6-evidence/sweep-results.json
{"checks":56,"failures":0}
```

## Scope and milestone boundary

The production delta remains inside `web/`; docs record the closeout. `server/`, `pipeline/`,
and `evals/` are unchanged, and the two locked md5 guards are rechecked in the PR evidence.
P6 closes the code sweep; **Sean's engine-truth session after merge closes the milestone**.
