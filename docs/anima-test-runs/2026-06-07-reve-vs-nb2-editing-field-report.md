# Reve vs NB2 — Image-Editing Bake-Off — Field Report

*2026-06-07 (run stamped 2026-06-08 UTC). Generator head-to-head: does Reve hold Sean's identity under a real multi-reference edit at least as well as the NB2 incumbent (`gemini-3.1-flash-image-preview`), and does it suffer the multi-reference downsampling failure that demoted NB Pro? Harness: [`evals/bakeoffs/2026-06-07-reve-vs-nb2-editing/`](../../evals/bakeoffs/2026-06-07-reve-vs-nb2-editing/). Decision artifact: [`results.md`](../../evals/bakeoffs/2026-06-07-reve-vs-nb2-editing/results.md). Method locked by [`docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md`](../research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md) §3.5 + §6. Companion operational account: [`2026-06-07-reve-vs-nb2-bakeoff-postmortem.md`](2026-06-07-reve-vs-nb2-bakeoff-postmortem.md).*

**This run answered the bake-off's headline question and required a live schema correction to get there.** The Reve API schema, as scaffolded from third-party mirrors, was wrong on every field name and 400'd on the first call; it was corrected against the API's own error messages before any scored generation. The schema story is the postmortem's; this report is the result.

---

## TL;DR

- **The decisive question is answered: Reve does NOT share NB-Pro's multi-reference downsampling regression.** On the `t2-remix-3quarter` probe (identity from the anchor, angle from the full-body turnaround), both Reve variants **beat** NB2 (standard +0.041, fast +0.038 DINOv2 vs the same 3⁄4 anchor) — no washed-out / generic face, confirmed by eye. This is the #1 open question the desk-research evaluation flagged, now settled empirically.
- **reve-standard is a viable keyframe / Cy-Bible adopt candidate (pilot, not wholesale-migrate):** it matches or beats NB2 on all three identity cases, at ~40% lower cost and in true 16:9.
- **reve-fast adopts for in-betweens:** it holds the real F06→F10 in-between (+0.006 vs NB2) with no collapse on the decisive case, at ~10× lower cost ($0.007 vs $0.067) and ~2× faster.
- **The margins are small and N=1.** The verdict rests on direction (no collapse; Reve ≥ NB2 on identity), not magnitude. Firm up with pairwise-Em + a replicated pass before trusting Reve with hero keyframes.

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

## Per-use-case verdict (applying the README decision rule, not a new one)

**1 — Multi-reference downsampling (the decisive case): Reve is clean.** No `⚠ worse` on `t2-remix-3quarter` for either variant — both beat NB2. By eye, none of the three outputs shows a soft/generic/downsampled face. Reve is **not** disqualified for multi-reference keyframes; it is the strongest result on the hardest single-identity multi-ref case.

**2 — Keyframe / Cy Bible → reve-standard, as a pilot.** reve-standard matches/beats NB2 on `t1-focused` (+0.003), `t2-remix-3quarter` (+0.041), and `t2-remix-3ref-pairing` (+0.002) — clears the rule's keyframe bar — at ~40% lower cost ($0.040 vs $0.067) and in true 16:9. **reve-fast is the wrong tier here**: it dips to −0.024 on the hardest 3-ref pairing (within tolerance, *not* a collapse, but below NB2).

**3 — In-between → reve-fast, adopt.** Holds `t3-inbetween-f06-f10` (+0.006) and the decisive case shows no collapse — both rule conditions met. ~10× cheaper, ~2× faster. The cleanest call in the set.

---

## Operational confirmations (report §5 Test 4 — recorded, not scored)

- **Watermark / provenance:** No visible watermark on any returned image. A byte scan of a Reve PNG found **no C2PA / JUMBF / XMP markers** — only a `dpi` tag. (Dedicated `c2patool`/`exiftool` weren't installed; the standard JUMBF/`c2pa` byte signatures are absent, so any embedded manifest would have to be non-standard.) Reve outputs are clean *and* unsigned — relevant both ways for a public portfolio.
- **Content filter:** all 9 live Reve calls returned `content_violation: false` — the pencil-test register is **not** content-filtered.
- **Latency:** standard 20–26s/image, fast 11–14s/image in the full run (~2× faster). Isolated single calls were quicker (7–8s fast / ~16s standard) — latency is load-dependent.
- **Rate-limit headers:** none surfaced — responses carried only `content-type` + `x-reve-request-id`. No `x-ratelimit-*` / `retry-after`; no 429s across ~20 calls.
- **Served versions (pinned to `variants.yaml` snapshots):** standard `reve-edit@20250915` / `reve-remix@20250915` (30 credits); fast `reve-edit-fast@20251030` / `reve-remix-fast@20251030` (5 credits). NB2 served-model is **not** surfaced by `invoke_image_edit`, so its snapshot is the pinned request constant, not a read-back.

---

## Honesty caveats (these bound the verdict)

- **Small margins, N=1.** Δ spans +0.002…+0.041 with one generation per cell. Sub-0.04 deltas are ties within noise; the conclusions lean on direction, not magnitude. A replicated (N≥3) pass + the documented **pairwise-Em** harness ("is A or B closer to the anchor?", position-swapped) is the right next step before a hero-keyframe migration.
- **DINOv2 over-rewards copying (§3.5).** NB2 reinterprets more — re-posed *walking* figures, a more polished/finished line, 1024² square (`invoke_image_edit` passes no `aspect_ratio`); both Reve variants stay closer to the reference composition + the looser pencil-test register + 16:9. Part of Reve's DINOv2 edge is "stayed closer to the reference" — *desirable* for identity-hold-under-edit, but not "Reve is the better illustrator."
- **Em is N=1 here, not the G5 N=5 baseline.** The `--score-em` block runs production `VisionCriticNode` once per cell in absolute, reference-blind mode — a corroborator only. Its reve-fast `borderline`s are a mild caution, not a verdict.
- **The Reve schema was wrong as shipped and corrected this session.** It is now API-verified for standard + fast; the one residual gap (the fast `version` strings) was closed from the Edit API doc Sean provided + an empirically-confirmed remix-fast string. See the postmortem.

---

## Decision (proposed to Sean — not self-executing)

1. **Pilot reve-standard for multi-reference keyframes / Cy Bible plates** behind the existing model-routing override (`characters.{id}.generation_model`), not a blanket swap. It clears the identity bar and is cheaper + native-16:9.
2. **Adopt reve-fast for in-betweens** (Phase 5 in-between generation / the retry ladder), where ~10× cost and ~2× speed compound and a mild wobble is tolerable.
3. **Keep NB2 the incumbent default** until a replicated + pairwise-Em pass confirms the small-margin keyframe call.
4. **Ratify the schema correction + the fast version strings** (now in `reve_runner.py`) and the proposed updates to the research doc + CLAUDE.md (surfaced separately, not edited inline).

---

## Hard lines honored

- **Ships-red:** no case tuned to flatter a variant. The only case edit (t3) is a validity fix per the case's own `sean_note`, applied pre-scoring.
- **Subscription billing:** `ANTHROPIC_API_KEY` unset throughout; harness `--score-em` guard armed; Em escalation rode the subscription.
- **Isolation:** ran entirely in the `bakeoff/reve-vs-nb2-editing` worktree; main untouched.
- **Smoke-before-spend:** stub → schema probe → 1-case live smoke (eyeballed) → full run.
- **Couldn't-verify over confident guess:** the wrong schema was *diagnosed from the API*, not guessed past; the fast tier was held until verified; watermark/C2PA reported as "no standard markers detected" given no dedicated tool.
- **DINOv2 ambiguity surfaced, not forced:** small margins + N=1 flagged explicitly; pairwise-Em recommended rather than overclaiming.
