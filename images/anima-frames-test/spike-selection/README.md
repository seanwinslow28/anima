# Animatic placement spike — kickflip corpus

Curated input for the Animatic phase spike (build step 1 of
[`docs/2026-06-18-animatic-phase-kickoff.md`](../../../docs/active/2026-06-18-animatic-phase-kickoff.md)).
Tests the load-bearing bet: **does a hand-drawn placement rough make NB2 respect
placement on poses far outside Sean's "sitting and drawing" register?** Here, a
skateboard kickflip.

**Single character: Sean only** (`characters/sean-anchor/anchor.png` is the identity
anchor; no Claude mascot). The roughs supply the *pose*; the anchor supplies the
*likeness*. The roughs are a *different* character (red shirt, blue jeans, a face) on
a pink ground — so the role-tag quarantine ("match placement, do NOT copy line/colour/
style/background; identity comes only from the anchor") is tested at its hardest.

## The six keys (a complete kickflip)

| Key | Source frame | Kickflip beat |
|---|---|---|
| key-1 | `Anima_test-2`  | anticipation — crouch loads the pop |
| key-2 | `Anima_test-3`  | pop / ollie — leaves the ground |
| key-3 | `Anima_test-5`  | apex — airborne, board flipping |
| key-4 | `Anima_test-9`  | mid-flip — board rotating under |
| key-5 | `Anima_test-14` | catch / land — board back underfoot |
| key-6 | `Anima_test-18` | ride-out — upright, settled |

## The A/B sub-test (frames key-1 / F2 and key-3 / F5)

Each of these two keys ships in **two forms**, to learn whether finished roughs work
or silhouettes are needed:

- `key-N_F*.png` — the colored rough **as-is** (hard mode: competing identity + palette + pink bg).
- `key-N_F*_silhouette.png` — stripped to a flat pose **silhouette** (easy mode: placement only, nothing to copy).

Generated at $0 via ImageMagick background-floodfill + threshold. Refine the
silhouette method if the spike needs it.

## The full 18

The complete sequence lives in the parent directory (`../Anima_test-1..18.png`).
Reserved for the **proven-bet follow-on** — once the spike is green, the full kickflip
becomes a publishable museum piece ("Sean lands a kickflip, generated from his own roughs").
