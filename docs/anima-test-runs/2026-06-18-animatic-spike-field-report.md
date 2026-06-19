# Field Report — Animatic placement spike: the kickflip (the bet, tested before any plumbing)

**Date:** 2026-06-18
**Kickoff:** [`docs/2026-06-18-animatic-phase-kickoff.md`](../2026-06-18-animatic-phase-kickoff.md) (Step 1)
**Design of record:** [`docs/2026-06-18-animatic-phase-design.md`](../2026-06-18-animatic-phase-design.md)
**Spend:** ~**$1.0** (15 live NB2 calls — 14 spike + 1 transport smoke — at ~$0.07/image, `gemini-3.1-flash-image-preview`, Gemini-metered; well under the ~$2–3 ceiling)
**Branch:** `animatic-phase-v1` off `main` `71ad992` (isolated worktree)
**Status:** spike complete; **awaiting Sean's GO/NO-GO** (his eye is the engine-truth arbiter)

---

## The bet under test

> **A hand-drawn stick-figure placement rough actually makes the image model respect placement** —
> shoulder side, scale, leg count, left/right.

If that's false, the whole ANIMATIC stage is wasted plumbing — so per the kickoff this spike runs
**before a line of stage code.** The corpus is harder than reproducing the 2026-06-18 drift: a
**skateboard kickflip**, six keys, poses far outside Sean's sitting-and-drawing register, on roughs
that are a *competing* character (red shirt, a face, blue jeans) on a **pink ground** — so the
role-tag quarantine ("match placement, do NOT copy line/colour/character/background; identity comes
only from the anchor") is stressed at its hardest. Single character: `characters/sean-anchor/anchor.png`.

## Method

For each of the six keys, two ref slots — **anchor first (identity), rough last (composition
target)** — re-anchored every key, **no chaining** (NB2 research: re-anchor to canonical, never
chain off a generated frame). Three arms:

- **(a) prose-only baseline** — anchor only + prose naming the kickflip beat. *What does NB2 do
  with words alone?*
- **(b) with-rough** — anchor + the colored rough + the exact kickoff role-tag clause; prose stays
  generic ("Sean is performing a skateboard kickflip"), the rough carries the specific pose.
- **(c) silhouette A/B** — same as (b) but the rough stripped to a flat silhouette, on F2 + F5.

14 live calls (6 + 6 + 2). All returned `live`, `rc=0`, **zero stub fallbacks** (the harness aborts
on any stub — a stubbed spike proves nothing). Transport: the same `invoke_image_edit`
(`pipeline/agents/nb_pro_runner.py`) the production stage and Flo dispatch. Scratch harness:
`spike_animatic.py` / `spike_contact_sheets.py` (not committed to `pipeline/`).

## The evidence

**Sheet 1 — per key: rough input vs prose-only vs with-rough.**

![main contact sheet](assets/2026-06-18-animatic-spike/spike_sheet_main.png)

**Sheet 2 — A/B: colored rough vs stripped silhouette (F2, F5).**

![A/B contact sheet](assets/2026-06-18-animatic-spike/spike_sheet_ab.png)

Full-res outputs: [`assets/2026-06-18-animatic-spike/outputs/`](assets/2026-06-18-animatic-spike/outputs/).

**Sheet 3 — Sean's pre-build request: colored rough vs silhouette across ALL six keys (no baseline).**
After ruling GO, Sean asked to extend the silhouette test from the two A/B keys to the full kickflip
before any stage code. The four missing silhouettes (F3, F9, F14, F18) were generated from the colored
roughs by color-keying the uniform `(254, 232, 255)` pink ground (PIL, no ImageMagick here) — figure →
black, near-white shoes kept white, matching the two pre-made silhouettes — and run through the same
anchor + role-tag clause. 4 more live calls (~$0.28).

![colored vs silhouette, six keys](assets/2026-06-18-animatic-spike/spike_sheet_color_vs_silhouette.png)

**Read:** both forms land the pose and hold identity across all six. The **silhouette outputs avoid the
colored rough's palette echo** (no green board on the F5 apex) and read clean. Two costs on the
silhouette side: a couple of cells (F14, F18) render lighter / more line-sketch than fully shaded, and
two (F9, F14) picked up a faint hallucinated text artifact in a corner. The colored outputs are a touch
more consistently shaded but carry the minor palette-echo risk. **Net: silhouettes are a viable — arguably
cleaner — authoring path; the stage is agnostic to which the human drops in** (`animatic_ref` points at
whatever rough is dropped), so this is authoring guidance, not a code fork.

## Initial read (mine — Sean's eye decides)

1. **The rough lands placement that prose misses.** Column (b) tracks the rough's pose and airborne
   body line markedly better than the prose-only column (a) — most visibly on the *hard* beats
   (apex, mid-flip, catch/land), where prose-only keeps defaulting to a grounded skate stance.
   This is the bet's core claim, and it reads as **supported**: a visual placement reference does
   what words cannot reliably do.
2. **The quarantine held.** Every with-rough output stayed in Sean's pencil-test register on cream
   paper — **no pink ground, no red shirt, no competing face** bled through, despite the rough
   carrying all three. The role-tag clause ("don't copy its colour/character/background") did its
   job at the hardest setting. (Minor nit: one apex cell picked up a greenish board — a small palette
   echo, not a quarantine failure.)
3. **Identity held across six radically different poses.** Sean reads as the same character —
   light hair, consistent face/build — from a deep anticipation crouch through a fully airborne flip
   to an upright ride-out. The anchor-first slot carried identity through poses far outside its
   register.
4. **Colored rough ≈ silhouette — stripping looks unnecessary in v1.** On both F2 and F5 the colored
   rough and the silhouette landed the pose and held identity about equally; because the quarantine
   already suppressed the rough's palette, the colored rough needed no stripping. **Authoring-effort
   win:** v1 can ingest finished/colored roughs as-is; the silhouette step is an optional fallback,
   not a requirement. (The harder per-loop questions — establishing-frame propagation, fifth-ref
   dilution — ride to the first costed *loop* run, per the design doc.)

**Sheet 4 — the trail-off, diagnosed and fixed.** Sean's eye caught that both forms "start off
great but trail off at the end of the run." At full res the cause is clear and it is **a prompt gap,
not a model limit**: the "warm pencil-test register" cue pulls the model toward real *animation
production sheets* — so later/action frames sprouted **hallucinated label text** ("KICKFLIP APEX /
CLEAN SKETCH / POSE B", frame numbers like "0042"), **hole-punch marks**, and a drift from finished
shading toward a looser line-rough. The spike prompt carried no negative against any of that. Fix
tested on the two worst later keys (F14 + F18, both forms; 4 live calls, ~$0.28): add a strengthened
negative + a finished-frame clause —

> *"Do not render any text, captions, labels, frame numbers, hole-punch marks, watermarks, or
> production-sheet annotations — draw only Sean and the skateboard on clean cream paper. Render a
> fully finished, shaded pencil-test frame, not a loose line rough."*

![trail-off before/after](assets/2026-06-18-animatic-spike/spike_sheet_notext_fix.png)

**Result:** the label text and the line-sketch looseness are **cleared reliably** — F14 silhouette
AFTER is a fully shaded, label-free Sean kickflip; F18 colored AFTER re-centers and finishes. One
**residual**: hole-punch marks are greatly reduced but can persist faintly at the frame's bottom edge
(F18 AFTER still shows three) — the hole-punch motif is more stubborn than the text. Acceptable for v1
(faint, bottom-edge, croppable); a stronger lever can follow. **Build consequence:** the strengthened
negative + finished-frame clause is baked into the animatic role-tag clause Step 3 appends — an
extension of the no-text negative Bea shipped in Tier-1 Slice A (F6), which covers text/labels but not
production-sheet artifacts or sketch-looseness. (Recommendation noted: Bea's base register negative
could grow the same way — out of this phase's scope.)

## Ruling — GO (Sean, 2026-06-18)

**Sean ruled GO.** The mechanism does the one thing the stage rests on (visual rough → respected
placement) while holding identity and quarantining the look, on a corpus deliberately harder than the
real use case; the colored-rough-works finding *lowers* the authoring cost the design flagged as the
#1 risk. Two riders on the GO:

1. **Silhouette is the recommended authoring form** (Sean's call). Both work and the stage is agnostic
   (`animatic_ref` points at whatever rough is dropped), but silhouettes read cleaner and avoid the
   colored rough's palette echo — so the stage docs/instructions recommend silhouettes while keeping
   colored roughs fully supported.
2. **The trail-off was Sean's catch and is fixed before the build** (Sheet 4): the strengthened
   no-text/no-production-artifact + finished-frame negative goes into the animatic role-tag clause
   Step 3 bakes in. Residual hole-punch faintness noted.

→ Proceed to Steps 2–7: the $0 stub-green, TDD build of the opt-in ANIMATIC stage. The full 18-frame
kickflip becomes the proven-bet follow-on and a publishable museum piece ("Sean lands a kickflip,
generated from his own roughs").

## Spend + fleet-ops

- ~$1.0 Gemini-metered (15 live NB2 calls), under the ~$2.5 estimate / ~$2–3 ceiling.
- Subscription billing untouched (`ANTHROPIC_API_KEY` absent); one isolated worktree off
  `main` `71ad992`; single owner; `.env` copied into the worktree (gitignored) so the key resolved.
- Both standing guards unchanged: Em verdict baseline `2af75906…`, shared voice `945af824…`.
