# Reve vs NB2 — image-editing bake-off

*Dated bake-off scaffolding, 2026-06-07. The empirical companion to [`docs/research/2026-06-07-reve-ideogram4-evaluation.md`](../../../docs/research/2026-06-07-reve-ideogram4-evaluation.md) — it answers the one question that desk research left open: **does Reve hold Sean's identity under a real multi-reference edit at least as well as NB2, and does it suffer the multi-reference downsampling failure that demoted NB Pro?** Built but **not yet run** — the live run is costed and is the operator's to execute under fleet-ops discipline.*

This is a **generator** bake-off, not a judge bake-off. The 2026-05-31 T2 shoot-out next door varied the model that runs *Em*; this one varies the model that *produces the edit*, and scores the outputs. The shapes are deliberately different, and the method is locked by [`docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md`](../../../docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md).

## What it does

Three variants (`variants.yaml`) each edit the same cases (`cases.yaml`):

| variant | engine | tier | $/img | role |
|---|---|---|---|---|
| `nb2` | `invoke_image_edit` (`gemini-3.1-flash-image-preview`) | standard | $0.067 | **incumbent baseline** — every Reve column is read against it |
| `reve-standard` | Reve Edit/Remix | standard | $0.040 | ~40% cheaper than NB2 |
| `reve-fast` | Reve Edit Fast/Remix Fast | fast | $0.007 | ~10× cheaper — the in-between candidate |

Two stages:

- **`--stage generate`** — each variant edits every case; outputs land in `generated/{variant}/{case}.png` (gitignored). NB2 routes through the real `pipeline/agents/nb_pro_runner.invoke_image_edit`; Reve through the local `reve_runner.invoke_reve` (Edit for 1 reference, Remix for ≥2).
- **`--stage score`** — **DINOv2-vs-per-view-anchor** (the deterministic SF02 headline) + optional **Em** (`--score-em`, secondary). Writes `results.md` + `traces/`.

## The metric contract (why it's built this way)

Straight from the eval-strategy doc's **generator row (§6)** and **vision-judge section (§3.5)**:

1. **DINOv2-vs-per-view-anchor is the headline**, not an MLLM judge. "For the visual generator, DINOv2-vs-anchor *is* the visual groundedness metric." The harness uses anima's shipped `compute_similarity` ladder (DINOv2 → CLIP → PIL); install `torch torchvision transformers` or it silently degrades to `pil-perceptual`, which is **not** a real identity read (the trace says which tier engaged — check it).
2. **Score against the SAME-VIEW anchor.** A 3/4 output is scored against the 3/4 turnaround crop, never the front anchor — "a back-of-head plate is genuinely far from a front anchor in embedding space, as far as a wrong-character front view" (`similarity_gate.py`). Each case names its `per_view_anchor`.
3. **No universal DINO threshold → the DECISION is the Reve-vs-NB2 Δ** on the same case + same anchor. The `results.md` Δ column is the whole point. Absolute scores are context; the delta is signal.
4. **Report the Subject-Collapse count, not just a mean** — "a mean hides one catastrophic drift among many fine plates." The per-variant table carries below-threshold count + `stderr()` on the mean (§5 borrow #2: so a run-over-run delta is distinguishable from noise).
5. **Em is SECONDARY and reference-blind here.** A still-image judge is trustworthy mainly **pairwise**; reference-blind Em cannot truly verify identity (anima's own [reference-blindness finding](../../../docs/anima-test-runs/2026-06-01-em-reference-blindness-FINDING.md)). So Em corroborates SF01/register and flags gross drift, but **DINOv2 decides**. The recommended refinement is pairwise Em — see below.

## Decision rule

Read `results.md` after the live run:

- **Reve adopts for keyframes / Cy Bible** only if its DINOv2 **matches or beats `nb2`** on the identity cases (`t1-edit-focused`, `t2-remix-3quarter`, `t2-remix-3ref-pairing`).
- **`t2-remix-3quarter` is decisive.** A `⚠ worse` there (Reve materially below NB2) means Reve **shares NB-Pro's multi-reference downsampling regression** → disqualified for multi-reference keyframes; at most a single-reference Edit tool.
- **Reve Fast adopts for in-betweens** if `t3-inbetween-*` holds AND `t2-remix-3quarter` shows no collapse — a mild wobble is tolerable on an in-between, fatal on a keyframe.
- **Never declare a winner** off a `pil-perceptual` run (DINOv2 tier absent) or a `--stub` run (placeholder outputs). Both are plumbing checks, not verdicts.

## Em pairwise (the recommended refinement — not built)

The eval-strategy doc is explicit that MLLM image judges are reliable **pairwise** ("is variant A or B closer to the anchor?") and weak at absolute scoring. The shipped `--score-em` path runs Em in **absolute** mode (the only mode the production `VisionCriticNode` exposes), so it's a corroborator, not the decider. A genuine pairwise-Em harness — feed Em the NB2 output and the Reve output side by side, ask which is closer to the per-view anchor, position-swap and require the verdict survive the swap (Balanced Position Calibration, §3.4) — is the right next build if DINOv2 leaves the call ambiguous. Flagged, not faked.

## How to run

**Plumbing check (credential-free, $0, CI-safe — no scored claim):**
```bash
python evals/bakeoffs/2026-06-07-reve-vs-nb2-editing/bakeoff.py --stage all --stub
```
`--stub` hard-short-circuits the runners (it never calls a model — important, because `invoke_image_edit` reads the `.env` file directly, so a populated `.env` would otherwise fire a real costed NB2 call). Outputs are gray placeholders; DINOv2 on them is meaningless by design.

**Live run (costed) — under fleet-ops discipline** ([`docs/architecture/fleet-ops-protocol.md`](../../../docs/architecture/fleet-ops-protocol.md)):
```bash
# 1. isolated git worktree (never the main checkout)
# 2. ANTHROPIC_API_KEY UNSET  → Em's escalation bills your Claude subscription,
#    not the Anthropic API (the harness REFUSES --score-em if it's set, mirroring
#    evals/vision_critic/score.py's guard).
# 3. REVE_API_KEY + GEMINI_API_KEY set in the worktree .env
# 4. DINOv2 tier:  pip install torch torchvision transformers
python evals/bakeoffs/2026-06-07-reve-vs-nb2-editing/bakeoff.py --stage generate
python evals/bakeoffs/2026-06-07-reve-vs-nb2-editing/bakeoff.py --stage score --score-em
```
Estimated spend at the full 5-case × 3-variant matrix: **well under $1** (15 generations: ~$0.57 of image generation + a handful of Em calls, subscription-absorbed). Trivial — the discipline is about *billing correctness and isolation*, not magnitude.

## ⚠ Before the live run — operator must verify

- **Reve endpoint schema is INFERRED, not first-party-verified.** `reve_runner.py`'s request/response shape (paths, auth header, the `fast` tier selector, the `image`/`images` field names, the response `b64_json`/`url` keys) is reconstructed from third-party mirrors because Reve's console docs (`api.reve.com/console/.../docs/{edit,remix}`) are an auth-gated JS SPA desk research couldn't read. **Verify every `_REVE_*` constant + the payload against the authenticated console, then pin the model/build header the API returns into `variants.yaml` `snapshots.reve`.** (`requests` is needed for the live Reve path: `pip install requests`.)
- **Test 3 (`t3-inbetween-*`) uses turnaround-crop stand-ins as endpoints.** Swap in two genuine adjacent approved Act-1/Act-2 anchors from `runs/<id>/approved/` for a real in-between read (noted in the case's `sean_note`).
- **Operational confirmations (report §5 Test 4), one run each, not scored:** inspect a returned Reve image + metadata for a **visible watermark vs invisible C2PA**; confirm the pencil-test register isn't content-filtered; note Fast-vs-standard latency and any rate-limit headers.

## Files

| file | role |
|---|---|
| `variants.yaml` | the 3 engines/tiers + pinned snapshots + per-image cost |
| `cases.yaml` | the 5 test-protocol cases (Tests 1–3), references, per-view anchors, probes |
| `bakeoff.py` | the two-stage harness (generate → score), `--stub` / `--score-em` / `--limit` |
| `reve_runner.py` | thin Reve Edit/Remix client + stub fallback + content cache (schema inferred — verify) |
| `results.md` | **the committed decision artifact** (placeholder until the live run overwrites it) |
| `traces/`, `generate-manifest.json`, `generated/`, `.cache/` | run outputs (gitignored; regenerated each run) |

## Provenance / honesty

The committed `results.md` is a **placeholder** — no live run has happened. The harness is smoke-validated in `--stub` mode only. Ships honest: a scaffold that says "not yet run" beats a stub matrix that looks real (PHILOSOPHY: *empirical, not vibes*; the repo carries its receipts).
