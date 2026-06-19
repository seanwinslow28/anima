# Reve vs NB2 — Image-Editing Bake-Off — Field Report

*2026-06-07 (run stamped 2026-06-08 UTC). Generator head-to-head: does Reve hold Sean's identity under a real multi-reference edit at least as well as the NB2 incumbent (`gemini-3.1-flash-image-preview`), and does it suffer the multi-reference downsampling failure that demoted NB Pro? Harness: [`evals/bakeoffs/2026-06-07-reve-vs-nb2-editing/`](../../evals/bakeoffs/2026-06-07-reve-vs-nb2-editing). Decision artifact: [`results.md`](../../evals/bakeoffs/2026-06-07-reve-vs-nb2-editing/results.md). Method locked by [`docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md`](../research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md) §3.5 + §6. Companion operational account: [`2026-06-07-reve-vs-nb2-bakeoff-postmortem.md`](2026-06-07-reve-vs-nb2-bakeoff-postmortem.md).*

**This run answered the bake-off's headline question and required a live schema correction to get there.** The Reve API schema, as scaffolded from third-party mirrors, was wrong on every field name and 400'd on the first call; it was corrected against the API's own error messages before any scored generation. The schema story is the postmortem's; this report is the result.

---

## TL;DR

- **Final verdict (Sean's eyeball, 2026-06-08): Reve FAILS for editing the Sean character — not adopted at any tier.** The DINOv2 metric scored Reve ≥ NB2 on identity (which by the harness rule would have meant pilot-keyframes + adopt-in-betweens), **but on face-crop inspection the Reve outputs are morphed and skewed** — body/pose/palette/register hold, the *face* distorts (asymmetric/melted eyes, skewed features). For an identity-locked character that is disqualifying. **NB2 stays the editing engine for Sean.**
- **Why the metric missed it:** DINOv2-vs-full-figure-anchor can't see facial-identity morph — the face is a small fraction of the whole-figure embedding and the overall composition matched. Textbook §3.5 ("DINOv2 over-rewards composition; not a sole good-frame gate"). The human eye is the arbiter (Engine Truth), and it overrode the score.
- **The decisive composition finding still holds:** Reve does NOT share NB-Pro's multi-reference *downsampling* regression (no washed-out/generic faces, no collapse; `t2-remix-3quarter` +0.041). But Reve substitutes a *different* identity failure — morph/skew — that is just as disqualifying for editing Sean.
- **Future direction (not now):** test Reve for *new-character creation* + *backgrounds* in other art styles — use cases with no existing identity to preserve, where its strong pose control, native 16:9, speed, and cost could pay off.

---

## Run config

| Knob | Value |
|---|---|
| Variants | `nb2` (incumbent baseline, `gemini-3.1-flash-image-preview` via `invoke_image_edit`) · `reve-standard` · `reve-fast` |
| Cases | 5 — `t1-edit-neutral-control` (easy), `t1-edit-focused` (moderate), `t2-remix-3quarter` (hard, **decisive**), `t2-remix-3ref-pairing` (hardest), `t3-inbetween-f06-f10` (hard, **real approved in-between**) |
| Headline metric | **DINOv2 cosine vs the per-view anchor**, read as the Reve−NB2 Δ on the same case + anchor (no universal threshold). Tier engaged = `dinov2` (a real identity read, not the `pil-perceptual` fallback) |
| Secondary | Em (T2 vision critic), reference-blind, **N=1 absolute** (the shipped `--score-em` mode — *not* the G5 N=5 majority); corroborator, not decider |
| Replication | **N=1 generation per cell** (15 images). No per-case stderr |
| Reve schema | **CORRECTED against the live API this session** (the scaffolded mirror-inferred schema 400'd). Edit `{edit_instruction, reference_image}`; Remix `{prompt, reference_images}`; tier via `version`; response = top-level base64 `image` |
| Billing | Reve + NB2 = API keys (`.env`); Em escalation = Claude **subscription** (`ANTHROPIC_API_KEY` unset; harness guard armed). Isolated worktree `bakeoff/reve-vs-nb2-editing` |
| Spend | **275 Reve credits (~$0.37) + ~6 NB2 generations (~$0.40) ≈ $0.77 total** (incl. schema-discovery probes; ledger in the postmortem). Credits remaining 7225 |

`t3` was switched from the scaffold's turnaround-crop stand-ins to the **genuine approved Act-1 keyframes PT_A1_F06→F10** (idle, stylus in right hand → right hand raised mid-gesture), committed as SHA-identical fixtures because `runs/` is gitignored. A validity edit applied pre-scoring (ships-red); it now stresses pose/expression motion, not a pure view rotation.

---

## DINOv2 identity hold — the headline

| case | difficulty | nb2 | reve-standard | reve-fast | Δ (best Reve − nb2) |
|---|---|---|---|---|---|
| `t1-edit-neutral-control` | easy | 0.715 | 0.723 | 0.729 | +0.014 |
| `t1-edit-focused` | moderate | 0.774 | 0.778 | 0.774 | +0.003 |
| **`t2-remix-3quarter`** | hard (decisive) | 0.807 | **0.848** | **0.845** | **+0.041** |
| `t2-remix-3ref-pairing` | hardest | 0.905 | 0.907 | 0.881 | +0.002 |
| `t3-inbetween-f06-f10` | hard | 0.971 | 0.977 | 0.976 | +0.006 |
| **mean ± stderr** | | 0.835 ±0.166 | 0.847 ±0.161 | 0.841 ±0.164 | — |

Subject-Collapse Rate (below 0.5): **0/5 for every variant** — no catastrophic identity loss anywhere. (The per-variant stderr is large because cases span 0.71–0.97 by design; the decision is per-case Δ, not the aggregate.)

**Em (secondary, reference-blind N=1):** reve-standard `pass` 5/5 (cleanest profile); reve-fast `borderline` on the three simplest cases + `pass` on the two hardest; NB2 `pass` 4/5 with a lone `fail` on `t3`. NB2's `t3` fail is a **beat-fidelity** flag — NB2 rendered a *walking* pose, not the idle→raised-gesture in-between the beat asked for — not an identity collapse (DINOv2 scored it 0.971). It cleanly illustrates the §3.5 division of labor: DINOv2 reads identity, Em reads the beat.

---

## Per-use-case verdict — the metric rule vs the eyeball override

The harness rule (DINOv2 Δ) and Sean's eye **disagree**, and the eye wins. Both readings are recorded below honestly.

**What the DINOv2 rule said (for the record):** no `⚠ worse` on the decisive `t2-remix-3quarter` (both Reve variants beat NB2 +0.041/+0.038 → no downsampling collapse); reve-standard matches/beats NB2 on all three identity cases (→ would have been a keyframe pilot); reve-fast holds the in-between +0.006 (→ would have been adopt-for-in-betweens). On the metric alone, Reve passes.

**What the eye saw (the override, decisive):** on face-crop inspection the Reve outputs **morph and skew the face** — asymmetric/melted eyes, distorted features — while pose/body/palette/register hold. DINOv2-vs-full-figure-anchor couldn't see it (face = small fraction of the embedding; composition matched). For an identity-locked character that morph is disqualifying.

**Verdict per use case:**
1. **Multi-ref keyframe / Cy Bible → FAIL.** Composition holds, *face does not*. Do not adopt.
2. **In-between → FAIL / not added to the lineup.** Same morph; cost/speed wins are moot when the face isn't Sean. NB2 stays the in-between editing engine.
3. **The downsampling question is still answered:** Reve does *not* share NB-Pro's washout/downsampling regression — but it substitutes its own identity failure (morph), so the net is still "not for editing Sean."
4. **Future (not now):** new-character creation + backgrounds in other art styles (no identity to preserve).

---

## Operational confirmations (report §5 Test 4 — recorded, not scored)

- **Watermark / provenance:** No visible watermark on any returned image. A byte scan of a Reve PNG found **no C2PA / JUMBF / XMP markers** — only a `dpi` tag. (Dedicated `c2patool`/`exiftool` weren't installed; the standard JUMBF/`c2pa` byte signatures are absent, so any embedded manifest would have to be non-standard.) Reve outputs are clean *and* unsigned — relevant both ways for a public portfolio.
- **Content filter:** all 9 live Reve calls returned `content_violation: false` — the pencil-test register is **not** content-filtered.
- **Latency:** standard 20–26s/image, fast 11–14s/image in the full run (~2× faster). Isolated single calls were quicker (7–8s fast / ~16s standard) — latency is load-dependent.
- **Rate-limit headers:** none surfaced — responses carried only `content-type` + `x-reve-request-id`. No `x-ratelimit-*` / `retry-after`; no 429s across ~20 calls.
- **Served versions (pinned to `variants.yaml` snapshots):** standard `reve-edit@20250915` / `reve-remix@20250915` (30 credits); fast `reve-edit-fast@20251030` / `reve-remix-fast@20251030` (5 credits). NB2 served-model is **not** surfaced by `invoke_image_edit`, so its snapshot is the pinned request constant, not a read-back.

---

## Honesty caveats (these bound the verdict)

- **DINOv2-vs-full-figure-anchor cannot see facial morph — CONFIRMED this run.** This is the load-bearing methodological finding: the metric scored Reve ≥ NB2 while the face was visibly distorted. The face is a small fraction of a whole-figure embedding, and Reve matched the *composition*, so the cosine stayed high. §3.5 ("DINOv2 over-rewards copying; not a sole good-frame gate") held exactly. **Identity edits must be gated on the human eye, a face-region metric, or pairwise-Em — never whole-figure DINOv2 alone.** Zoom to the face.
- **Small margins, N=1.** Δ spanned +0.002…+0.041 with one generation per cell — ties within noise even before the eyeball override. Direction over magnitude, and even the direction was metric-blind to the real failure.
- **Em is N=1 here, not the G5 N=5 baseline.** The `--score-em` block runs production `VisionCriticNode` once per cell in absolute, reference-blind mode — a corroborator only. Its reve-fast `borderline`s are a mild caution, not a verdict.
- **The Reve schema was wrong as shipped and corrected this session.** It is now API-verified for standard + fast; the one residual gap (the fast `version` strings) was closed from the Edit API doc Sean provided + an empirically-confirmed remix-fast string. See the postmortem.

---

## Decision (Sean, ratified 2026-06-08)

1. **Reve FAILS for editing the Sean character — not adopted at any tier.** The face morph/skew is disqualifying for an identity-locked character; NB2 remains the editing engine for Sean (keyframes, Cy Bible plates, and in-betweens).
2. **reve-fast is NOT added to the in-between lineup.**
3. **Keep the schema correction + verified fast version strings** in `reve_runner.py` (they're correct and worth keeping for any future Reve use).
4. **Future test (down the line, not now):** Reve for *new-character creation* + *backgrounds* in different art styles — use cases with no existing identity to preserve.
5. **Research doc updated** to record that the tests ran and the FAIL verdict; CLAUDE.md left unchanged (nothing adopted → no pipeline change; the CHANGELOG + research doc are the decision record).

---

## Hard lines honored

- **Ships-red:** no case tuned to flatter a variant. The only case edit (t3) is a validity fix per the case's own `sean_note`, applied pre-scoring.
- **Subscription billing:** `ANTHROPIC_API_KEY` unset throughout; harness `--score-em` guard armed; Em escalation rode the subscription.
- **Isolation:** ran entirely in the `bakeoff/reve-vs-nb2-editing` worktree; main untouched.
- **Smoke-before-spend:** stub → schema probe → 1-case live smoke (eyeballed) → full run.
- **Couldn't-verify over confident guess:** the wrong schema was *diagnosed from the API*, not guessed past; the fast tier was held until verified; watermark/C2PA reported as "no standard markers detected" given no dedicated tool.
- **DINOv2 ambiguity surfaced, not forced:** small margins + N=1 flagged explicitly; pairwise-Em recommended rather than overclaiming.
