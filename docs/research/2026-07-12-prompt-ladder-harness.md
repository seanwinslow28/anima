# The prompt-ladder harness — a reusable rig for proving prompt behavior

*2026-07-12. A small, rerunnable methodology for answering "how much should I prompt?" on any image/video model with visual evidence instead of assertion. Built and first run on Higgsfield (Nano-Banana-2 + Seedance-2.0) with the GRANDMASTER kid-samurai subject; the method is transport-agnostic. First run: [`runs/2026-07-11-prompt-ladder-grandmaster/`](../../runs/2026-07-11-prompt-ladder-grandmaster/) (gitignored). Findings from that run: the [compositing doctrine](2026-07-12-compositing-doctrine.md) and the [prompt decision card](../architecture/prompt-decision-card.md).*

---

## The method

**One controlled variable.** Hold subject, references, and target-change fixed; vary **only prompt verbosity** across a ladder of rungs; generate the whole ladder in one sitting; let a human eye rank the outputs. This is a controlled A/B, not free-form iteration — the point is a *picture of the ladder* that shows where more prompting starts to hurt, so a rule stops being a claim.

**The four canonical rungs** (adapt per surface):

| Rung | Name | Shape |
|---|---|---|
| 1 | Terse | one action verb + one variable ("Place the boy from Image 1 into Image 2.") |
| 2 | Anchored-terse | + enumerated identity-lock + role-tags + anti-text |
| 3 | Medium | + one sentence of integration (scale / position / light) |
| 4 | Over-prompted | the kitchen-sink literary prose you'd write by instinct |

**Predicted shape** (usually true): Rung 2 wins on edits/compositing; Rung 4 visibly degrades. On generation-from-scratch the ranking flattens (more detail doesn't hurt when there's no reference to compete with). The value is the *picture*, not the prediction — and the degradation is often not where you expect (see the first run: over-prompting an edit broke *framing and style*, not identity; over-prompting a composite regenerated the *background*).

**A human eye is the sole arbiter.** No LLM aesthetic judge on creative quality (eval-handbook rule). One reviewer ranks each rung at the block gate.

## The folder convention

```
runs/<date>-prompt-ladder-<subject>/
├── README.md               # preflight findings + CLI command shapes + subject
├── make_contact_sheet.py   # Pillow tiler (below) — reused across blocks
├── scoring-template.md      # the blank sheet, copied per block
├── A_generation/           # one folder per block
│   ├── <rung>.txt           # each rung's prompt, in its own file
│   ├── <rung>.png           # the output
│   ├── contact_sheet.png    # all rungs tiled for the gate
│   └── scoring.md           # the finding (the sheet IS the deliverable)
├── B_.../ C_.../ D_.../
```

Run outputs are gitignored (`runs/`); the *findings* (scoring sheets → doctrine docs) are what get committed under `docs/`.

## The scoring sheet

One row per rung; the sheet is the finding.

```
| Rung | identity_hold (1–5) | change_landed (Y/N) | style_match (1–5) | artifacts (text/label/melt/bleed) | rank | note |
```

Add surface-specific columns as needed (compositing added `scale_correct` and `bg_preserved`; those two caught the whole story). End every sheet with a one-line **Finding** and a **Winning clause → doctrine** line.

## Block-gate discipline

Run **one block at a time**; the human reviews the contact sheet + scoring sheet and greenlights the next. Gates are hard: a budget overrun on one block **stops the run and banks the finding** rather than burning the rest. Show the rung prompts before spending on the expensive blocks — that's where a "make it shorter" steer changes the result.

## The CLI reference (Higgsfield, v0.2.3)

All generation through one CLI, one credit pool, image + video. Auth (`higgsfield auth login`) is human-only, one-time.

```bash
# Preflight ($0): auth+credits, model catalog, per-model params/cost
higgsfield account status
higgsfield model list
higgsfield model get <model> --json
higgsfield generate cost <model> --prompt "$(cat p.txt)" [--resolution 2k]

# Image gen / edit / composite. Reference images via repeatable --image (local path auto-uploads).
#   NB2 (nano_banana_flash): identity/edit workhorse, ~1.5 cr @1k / 2 cr @2k
#   NB Pro (nano_banana_2):  ~2 cr;  gpt-image-2 (gpt_image_2): ~7 cr, best at the flat-poster register
higgsfield generate create nano_banana_flash \
  --prompt "$(cat rung.txt)" \
  --image ./character.png [--image ./background.png ...] \
  --aspect_ratio 16:9 --resolution 2k --json --wait --wait-timeout 8m

# Video (Seedance 2.0): ~14 cr / Fast-720p-4s clip; 4s minimum
higgsfield generate create seedance_2_0 \
  --prompt "$(cat p.txt)" \
  --start-image start.png --end-image end.png \
  --mode fast --resolution 720p --duration 4 --aspect_ratio 16:9 --generate_audio false \
  --json --wait --wait-timeout 20m
```

Output: `--json --wait` returns a JSON array with a `result_url` per job; `curl` it to a local file. Rejected/too-short requests cost 0.

**Gotchas (from the runbook + this run):** write every prompt to a `.txt` and pass `--prompt "$(cat p.txt)"` — samurai/pencil prompts carry apostrophes that break inline; `--generate_audio false` uses the underscore; the CLI's `nano_banana_flash` = "Nano Banana 2" (anima's NB2), `nano_banana_2` = "Nano Banana Pro" (the names are inverted from intuition); NB2 uses a `medias[]` reference array, NB Pro uses `input_images[]`, but `--image` maps to either.

## The contact-sheet tiler

`make_contact_sheet.py` (Pillow-only, committed with each run) tiles labelled thumbnails into one reviewable sheet:

```bash
python make_contact_sheet.py out.png "label1" img1.png "label2" img2.png ...
```

Max 2 columns, caption per tile, dark background. It's the fastest way to put a whole block in front of the reviewer at the gate.

## Rerunning when a model updates

The rig is the point: when a transport changes, re-run the same block prompts against the new model, drop the outputs beside the old ones, and re-rank. The scoring sheet's structure makes the regression (or improvement) legible in one pass. Keep the rung `.txt` files stable across re-runs so only the model varies.
