# Flo in-between pencil-preservation pilot (2026-06-10)

A costed generator head-to-head for **in-betweens**: does a fal.ai image-edit model preserve the
pencil-test aesthetic (graphite line + cream-paper grain) and the character's identity through a
tween — well enough to wire as Flo's `in_between_*` route — or do both fal models slick the pencil,
forcing the **NB2 pivot** (the locked fallback)?

Builds on Flo-A (PR #43): the `generation.routing:` skeleton declared `in_between_cheap`
(`fal_seedream`) and `in_between_mid` (`fal_qwen`) but left them **not wired**. This pilot supplies
the empirical evidence to wire the winner (or record the pivot).

## What it does

Four generators run the **same 14 approved Act-1 in-between cases** (held prompt + references +
anchors — only the engine varies):

| variant | engine | role | $/img |
|---|---|---|---|
| `nb2` | `invoke_image_edit` (gemini-3.1-flash-image-preview) | incumbent baseline / locked fallback | 0.067 |
| `nb-pro` | `invoke_image_edit` (gemini-3-pro-image-preview) | painterly hero ceiling | 0.15 |
| `fal-seedream` | `invoke_fal_seedream` | candidate cheap route (`in_between_cheap`) | ~0.02 |
| `fal-qwen` | `invoke_fal_qwen` (denoise 0.80) | candidate mid route (`in_between_mid`) | ~0.021 |

Each case is one approved IB target: the **two endpoint keyframes** are both the `references` and
the `per_view_anchors` (DINOv2 scored against BOTH endpoints, take the MIN — the Subject-Collapse
floor). The approved IB itself is the `reference_target` — Sean's visual reference for grain/morph,
**not** a DINOv2 target.

## The metric contract

- **DINOv2 Δ vs `nb2` (HEADLINE)** — no universal threshold; the per-case delta + Subject-Collapse
  count is the signal (eval-strategy §3.5/§6). Needs `torch torchvision transformers`, else it
  degrades to `pil-perceptual` — **which is not a verdict**.
- **Em (SECONDARY)** — reference-blind; corroborates SF01/register, flags gross drift.
- **Sean's eye (FINAL ARBITER)** — grain-preservation + character-morph are the two failure modes
  the embedding metric cannot see. Reve scored +0.006 DINOv2 vs NB2 and Em passed it; Sean's eye
  disqualified it because it morphed the character. **The eye wins (Engine Truth).**

## STEP B0 — verify the fal transports LIVE before the benchmark leans on them

`pipeline/agents/fal_runner.py` ships with the Seedream/Qwen endpoint ids as **UNVERIFIED
CANDIDATES** and REFUSES the real path until verified (the reve mirror-schema lesson). Before any
spend: probe the live fal model pages, confirm the endpoint id + arg names (`image_urls` vs
`image_url`, edit route, output url field, Qwen denoise exposure), set
`_FAL_ENGINES[engine]['verified'] = True`, and pin the served-model string into
`variants.yaml snapshots:`.

## How to run

```bash
# 1) Plumbing check (credential-free; gray placeholders; $0; no scored claim):
.venv/bin/python evals/bakeoffs/2026-06-10-flo-inbetween-pencil-pilot/bakeoff.py --stage all --stub

# 2) Live smoke (after B0): 2 cases, <$1 — eyeball that real fal generations land:
.venv/bin/python evals/bakeoffs/2026-06-10-flo-inbetween-pencil-pilot/bakeoff.py --stage generate --limit 2

# 3) Full run (~$10–15): 4 variants × 14 cases ≈ 56 generations, then score:
.venv/bin/python evals/bakeoffs/2026-06-10-flo-inbetween-pencil-pilot/bakeoff.py --stage generate
.venv/bin/python evals/bakeoffs/2026-06-10-flo-inbetween-pencil-pilot/bakeoff.py --stage score --score-em
```

Live run guardrails (fleet-ops §0): isolated worktree, `ANTHROPIC_API_KEY` UNSET (subscription
billing for Em's Opus escalation), `FAL_KEY` (+ `GEMINI_API_KEY`) from the worktree `.env`, smoke
before full, bounded ~$10–15 ceiling.

## Decision rule

Wire the winning fal route (`status: declared → wired` in `manifest.yaml`, plus a dispatch branch
in `pipeline/agents/frame_router.py`) ONLY if it holds grain **and** identity by Sean's eye AND its
DINOv2 doesn't collapse. **If BOTH fal models slick the pencil → pivot: route in-betweens to `nb2`**
(the locked fallback) and ticket self-hosted FLUX + Shakker sketch-LoRA as the $0-ongoing future.
Never declare a winner off a `pil-perceptual` or `--stub` run.

## Files

| file | role |
|---|---|
| `variants.yaml` | the 4 generators + pinned `snapshots:` (fal rows TODO until B0) |
| `cases.yaml` | the 14 approved Act-1 in-between cases (held prompt; both endpoints as refs + anchors) |
| `fixtures/` | committed — 9 endpoint keyframes + 14 approved IB references (runs/ is gitignored) |
| `bakeoff.py` | `--stage generate\|score\|all`, `--stub`, `--limit N`, `--variants`, `--score-em` |
| `results.md` | the committed decision artifact (placeholder until the live run) |
| `pipeline/agents/fal_runner.py` | the fal Seedream/Qwen transport (production home; B5 wires the winner from here) |

## Provenance / honesty

`results.md` is a **placeholder** until the costed live run — the harness is smoke-validated in
`--stub` mode only. A scaffold that says "not yet run" beats a stub matrix that looks real.
