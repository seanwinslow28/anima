# Runbook — "The Spark, Shared," with the Animatic stage (the DoD #6 proof)

*2026-06-18 (roughs added 2026-06-21). This is **yours to drive** — you run each command in a plain terminal opened in the `anima` project folder, one gate at a time, reading the output as it happens. Do **not** hand it to Claude Code to run in the background; the whole point is that you hold every gate yourself, and one gate — ANIMATIC — is where **you drop your hand-drawn roughs**. Model: the [2026-06-16 Spark runbook](../COMPLETED/orchestrator/2026-06-16-spark-authored-costed-run-runbook.md), now with the placement gate added.*

---

## Why this run

It's the **last open Animatic DoD item (#6)** and the real proof of the whole phase. The [2026-06-18 validation run](../anima-test-runs/2026-06-18-tier1-validation-run-post-mortem.md) shipped a clean loop but drifted exactly where the image model can't read prose: the **mascot on the wrong shoulder**, its **leg count wobbling 2↔4**, and **inconsistent scale**. That run is the **"without animatic" baseline.** This run is the same piece **with** your placement roughs pinning all of it — a direct before/after that answers the one question the stage exists to answer: *does a hand-drawn placement rough hold the placement where prose drifted?*

The [kickflip spike](../anima-test-runs/2026-06-18-animatic-spike-field-report.md) already proved the *mechanism* on a turnkey corpus. This run adds the two things the spike deliberately didn't test: **a real loop** (two characters, a loop-return) and **your own roughs** — the design's original #1 risk (*will Sean actually author these every run?*), now answered in the affirmative: you drew them.

## Your roughs (ready)

Seven clean line-art animatic frames at [`images/final-animatic-test/`](../../images/final-animatic-test/) (`frame-1.png`…`frame-7.png`), plus an **ingest-ready, renamed copy** at `images/final-animatic-test/F-named/` (`F01.png`…`F07.png`). They're the Spark loop drawn as placement roughs: **Sean ¾ at the desk, drawing; the mascot perched on his shoulder** through the full arc — idle → look → perk → delight → settle → close. Across all seven the mascot stays on the **same (viewer-left) shoulder at a steady scale** — which is precisely the placement the 06-18 run lost.

**Line-art is the ideal form here** — cleaner than a colored rough (no palette to echo) and it carries more pose detail than a flat silhouette. No stripping needed. What the roughs lock: the mascot's **shoulder side, scale, and perched silhouette held consistent across the whole loop** (this removes the conflicting-establishing-frame mechanism that caused the 2↔4 leg wobble — F01 will no longer disagree with the anchor), **Sean ¾ with the stylus in the right hand**, and **F07 ≈ F01** so the loop closes clean. The mascot's four-leg canon is carried by its anchor + the role-tag clause; the rough's job is placement, and placement is what drifted.

## Billing & shape

Maya/Sam/Bea (Opus + Sonnet) run on your Claude subscription = **$0 incremental.** The ANIMATIC stage is **$0** — no model call; you drop the roughs you already drew. The only metered spend is **Gemini** (7 NB2 frames + Em's reads) ≈ **~$0.50 with zero retries**, scaling to ~$3 if frames need re-rolls. Wall-clock ~45–75 min, paced by your reviews.

**Fleet-ops (non-negotiable):** plain terminal (no nested-SDK throttle); `ANTHROPIC_API_KEY` **absent** (subscription billing) and `GEMINI_API_KEY` **present** in `.env`; one run, single owner; `git pull` so you're on `main` `6ea67bf` (#61) or newer.

---

## Step 0 — pre-flight

```bash
cd <anima checkout>
git pull
git log --oneline -1                                   # 6ea67bf (#61) or newer
echo "ANTHROPIC=${ANTHROPIC_API_KEY:-ABSENT}  GEMINI=${GEMINI_API_KEY:+SET}"   # ANTHROPIC=ABSENT  GEMINI=SET
ls images/final-animatic-test/F-named/                 # F01.png … F07.png (your ingest-ready roughs)
```

## Step 1 — start the run, **with `--animatic`**

```bash
python -m pipeline.run --brief briefs/2026-06-16-spark-authored --slug spark-animatic --animatic
```

This drives **Maya** (the plan) and stops at the plan gate. `--animatic` is passed **once, here** — it sets the opt-in flag for the whole run; you don't repeat it on resumes. The run dir is `runs/<date>-spark-animatic-run/`. Use `--status` any time to see where you are.

Review `plan.md`, then:

```bash
python -m pipeline.run --resume runs/<id> --approve-plan        # -> SCRIPT (Sam)
```

## Step 2 — script, then board (**curate to 7 frames — the one thing to get right**)

```bash
# review the script Sam proposes
python -m pipeline.run --resume runs/<id> --approve-script      # -> STORYBOARD (Bea)
```

Bea drafts `shots.yaml`. **This is the curation gate, and it's load-bearing for this run:** the animatic ingest requires every rough to name a real board frame, so the board must carry **frames with ids 1–7 to match your seven roughs.** Curate Bea's draft so that:

- there are **exactly 7 frames, ids 1 through 7**;
- the **last frame (id 7) carries `chain_from: 1`** (the loop-return — it chains off the approved frame 1, the way the 06-18 board did on its frame 5);
- if Bea drafted fewer than 7, add frame entries (reuse the closing `beat_id`, keep the same `cast`, give each a one-line prompt); if she drafted more, trim to 7.

*Low-friction fallback:* if reshaping the board to 7 is fiddly, run with the frame count Bea produces and drop only the matching subset of your roughs (e.g. a 5-frame board → use `F01`–`F05`). The arc still reads; you just spend a couple of roughs. Either way, **the board's max frame id must be ≥ the highest rough you drop.**

```bash
python -m pipeline.run --resume runs/<id> --approve-storyboard  # -> ANIMATIC (the new pause)
```

Because you passed `--animatic`, storyboard-approve routes to the **ANIMATIC** stage instead of straight to GENERATE. (Without the flag, this run would be byte-identical to 06-18 — that's the back-compat proof, live.)

## Step 3 — **ANIMATIC: drop your roughs** (the heart of this run)

The orchestrator pauses and prints the drop directory: `runs/<id>/animatic/`. Copy your ingest-ready roughs straight in:

```bash
cp images/final-animatic-test/F-named/F0*.png runs/<id>/animatic/
```

(The ingest reads `F<id>.png` — that's why the renamed `F-named/` copies exist; the original `frame-1.png`…`frame-7.png` names would be ignored. Any stray files like `.DS_Store` are skipped.)

**Optional timing** — a `holds.json` sidecar in the same directory maps frame id → on-twos hold count and overrides the board's holds at assembly, e.g. to let the delight beat linger:

```json
{ "5": 4 }
```

Leave it out to keep the board's on-twos default. When the roughs are in:

```bash
python -m pipeline.run --resume runs/<id> --approve-animatic    # ingest -> GENERATE frame 1
```

The ingest validates each rough names a real board frame and the sidecar parses, then wires the roughs in **without mutating the locked board** and generates frame 1. (If it errors that a rough names a frame not in the board, that's the Step 2 reconciliation — fix the board's frame count or remove that rough, and re-run `--approve-animatic`.)

## Step 4 — the per-frame eye gates

For each of the **7 frames**: read Em's verdict (the gate prints her reasoning + proposed fix on a flag), **eye the candidate against your rough**, then:

```bash
python -m pipeline.run --resume runs/<id> --approve-frame N
# or, if it missed:
python -m pipeline.run --resume runs/<id> --retry-frame N --note "<desired end-state, stated positively>"
```

The question to hold at each gate: **did the placement land where your rough put it** — right shoulder, steady scale, perched form — *and* did identity hold? That's the comparison to the 06-18 frames. After F07, the loop assembles automatically to `runs/<id>/export/` (gif/mp4/webm).

## Step 5 — the verdict + the field report

Eye the loop. The DoD #6 question: **does the placement hold where 06-18 drifted?** Put it beside the 06-18 export and judge shoulder / scale / mascot-consistency directly.

Write a short post-mortem to `docs/anima-test-runs/2026-06-18-spark-animatic-run-post-mortem.md`: spend, retries, the before/after on the drift axes, how the **authoring effort** actually felt (the #1-risk test — was drawing seven roughs sustainable?), the board-to-7-frames reconciliation (did it fight you? a signal for whether the animatic should define frame count upstream of Bea in a future slice), and any new seams. Capture the loop + a side-by-side as the proof.

## When it closes

On a clean result, **DoD #6 is met and the Animatic phase is done.** Per the anti-drift contract, that's the moment to **advance ROADMAP Current Focus to workstream 2 — Tier-2 Em calibration** (the autonomy core), and mark TOP-1 Animatic ✅ built + verified. Two parked follow-ons stay parked until their triggers: the full 18-frame kickflip museum piece, and growing Bea's base register negative.

If placement still drifts *with* a rough in hand, that's a real finding, not a failure — it tells us the mechanism needs a stronger lever on a real loop than it needed on the spike, and that becomes the next slice before Tier 2. Either way, this run is the honest test.

---

*Two characters, a real loop, your own roughs — the smallest honest proof that the keystone holds. Drive it yourself; the point is to watch the placement land.*
