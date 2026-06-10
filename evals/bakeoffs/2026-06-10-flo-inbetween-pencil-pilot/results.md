# Flo in-between pencil-preservation pilot — results

> **STATUS: NOT YET RUN (placeholder).** The harness is smoke-validated in `--stub` mode only
> ($0, gray placeholders — not a scored claim). This file is the committed decision artifact and
> is hand-curated AFTER the costed live run (STEP B0 verify → smoke → full → score). A scaffold
> that honestly says "not yet run" beats a stub matrix that looks real.
>
> Note: `bakeoff.py --stage all`/`--stage score` OVERWRITES this file. The `--stub` plumbing
> check therefore clobbers it with a meaningless stub matrix; this placeholder is restored after
> any stub run and is replaced for real only by the live score pass.

## To produce the real results

1. **B0** — verify the fal Seedream + Qwen endpoints/schemas live; flip `verified` in
   `pipeline/agents/fal_runner.py`; pin the served-model strings into `variants.yaml snapshots:`.
2. **Smoke** — `bakeoff.py --stage generate --limit 2`; eyeball the 2 real fal outputs; confirm
   the DINOv2 tier engaged is `dinov2` (not `pil-perceptual`).
3. **Full** — `bakeoff.py --stage generate` (4×14 ≈ 56), then `--stage score --score-em`; this
   overwrites this file with the DINOv2 matrix + aggregates + Em table.
4. **Decide** — Sean reviews the generated in-betweens vs each case's `reference_target` IB for
   grain-preservation + character-morph. Record the verdict here (fal winner wired, or NB2 pivot
   + FLUX ticket), in the spirit of the reve postmortem's eyeball verdict.

## Decision rule (carried from README)

Wire the winning fal route ONLY if it holds grain **and** identity by Sean's eye AND its DINOv2
doesn't collapse. If BOTH fal models slick the pencil → pivot to `nb2` (the locked fallback) and
ticket FLUX. Never declare a winner off a `pil-perceptual` or `--stub` run.
