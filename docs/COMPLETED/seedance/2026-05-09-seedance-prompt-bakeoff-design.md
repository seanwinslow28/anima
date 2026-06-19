# Seedance 2.0 Prompt Template Bake-off — Design Spec

> **Date:** 2026-05-09
> **Status:** Design approved, ready for implementation plan
> **Goal:** Converge on a canonical Seedance 2.0 prompt template that future 2D animation projects can lift verbatim, validated against Act 2 production shots.

---

## 1. Goal & artifact

The artifact this effort produces is a **canonical Seedance 2.0 prompt template** — `prompts/seedance-template-v4.md` — backed by documented bake-off evidence. Future 2D animation projects fill in shot-specific blanks against this template and run with minimal iteration. Act 2's 10 shots are the proving ground.

This is **not** a per-shot prompt optimization effort. The template is the asset; per-shot wording becomes mechanical.

## 2. Approach

Three phases, sequenced. Phase 1 is complete.

| Phase | Goal | Artifact | Cost |
|---|---|---|---|
| **1 — Deep research** | Surface 2026-era evidence on Seedance prompting; settle as many variant axes as possible without spending API dollars | Three research reports + synthesis (this doc, §3) | $0 |
| **2 — Structured bake-off** | A/B/C across 9 prompt variants on 2 representative shots × 2 seeds; manual binary rubric; pick a winner | `prompts/seedance-template-v4.md` + bake-off run dir | ~$40 |
| **3 — Act 2 production** | Apply the locked template across all 10 Act 2 shots; surgical per-shot tuning only on failures | Production runs; optional autoresearch loop on stubborn shots | ~$30 |

**Why not autoresearch from the start?** The interesting variation space is structural (~6 axes), not millions of micro-text mutations. A targeted bake-off covers it in 9 well-chosen variants. Karpathy's autoresearch pattern earns its keep at N≥25 iterations on a fine-grained mutation operator — below that, structured A/B/C beats evolutionary search. Autoresearch is reserved for Phase 3 surgical work, if needed.

## 3. Phase 1 — Research synthesis (complete)

Three deep research queries were run in parallel and produced rich, convergent evidence. Reports stored at:

- [docs/research/chatgpt-query-a-JSON-structured-prompts.md](../../research/chatgpt-query-a-JSON-structured-prompts.md)
- [docs/research/gemini-query-b-official-seedance-best-practices.md](../../research/gemini-query-b-official-seedance-best-practices.md)
- [docs/research/perplexity-query-c-hand-drawn-pencil-test-preservation.md](../../research/perplexity-query-c-hand-drawn-pencil-test-preservation.md)

### 3.1 Settled by evidence — no longer testable axes

These are now priors, baked into the bake-off baseline (V1 onward):

| Settled axis | Decision | Evidence |
|---|---|---|
| Structure format | Labeled blocks (not JSON, not pure prose) | Convergent across all 3 reports; Lanham's pro-JSON A/B itself recommends "draft in bullets, promote to JSON only if shot grows" |
| Word count | 80–100 words target, 100 hard cap | Gemini synthesis: <30 hallucinates, 50–70 is "the sweet spot," >200 causes attention collapse; fal.ai docs say 50–150 |
| In-prompt negation | Removed entirely, replaced with affirmative material descriptors | Nadine V. controlled experiment: 0% success on negation, 100% on affirmative; confirmed Seedance-specific by Gemini and Perplexity reports |
| Redescription of in-frame style | Dropped or hard-trimmed | ByteDance I2V docs say minimize static-content description; the start/end frames already encode line quality, paper grain, construction marks |
| Banned words | Hard-banned: `cinematic`, `4K`, `8K`, `ultra high res`, `sharp focus`, `polished`, `smooth`, `highly detailed`, `studio-quality`, `masterpiece`, `lens` (standalone), `anime` (unqualified) | Multiple sources flag these as drift triggers toward photoreal/anime |

### 3.2 Genuinely-testable axes — what the bake-off resolves

| Axis | Question | Variants test |
|---|---|---|
| **A** | Is the genre anchor (`classic Disney rough animation`) load-bearing on Seedance, or wasted budget? | V6 (no anchor) vs. V1 (with anchor) |
| **B** | Does transition-arc framing (`Starting with… transitioning to… ending with…`) outperform action-arc for start+end frame mode? | V2 vs. V1 |
| **C** | Does animation-timing language (`anticipation, hold, snap, settle`) reduce "AI floatiness" vs. prose motion language? | V3 vs. V1 |
| **D** | Do subtle audio cues drive better visual physics even with `generate_audio=False`? | V4 vs. V1 |
| **E** | Does canonical camera syntax (`locked tripod, micro push-in 2%, 50mm look`) stabilize better than plain `locked tripod`? | V5 vs. V1 |
| **F** | Is v3's 6-bullet style block doing real work, or does a 3-line affirmative-only block carry it? | V7 vs. V1 |
| **Stack** | Do the winning isolated axes combine cleanly, or do they interfere? | V8 (combined-best) vs. winners of V2/V3/V5/V7 individually |

## 4. Phase 2 — The bake-off

### 4.1 The 9 variants

Each variant is a **template**. The W1 wording is shown below for clarity; each variant gets ported to the second test shot using the same structural template with shot-specific action content.

#### V0 — v3 baseline (control, ~115 words)
```
Traditional 2D animation pencil test in the style of classic Disney rough animation. Sean walks left to right across the frame at a steady, relaxed pace. His head turns slightly as he takes in the floating Film props around him. The props remain stationary — only Sean moves. Sean is clean-shaven throughout.

CAMERA: Completely static, locked tripod. No pan, no zoom, no jitter, no rotation.

CRITICAL STYLE REQUIREMENTS:
- Rough graphite pencil line quality on every frame
- Cream paper grain texture stays consistent
- Visible construction marks on the character
- Bold dark pencil outlines, no anti-aliasing on edges
- Flat graphite shading only, no digital gradients or smooth blending
- Even diffuse animation paper lighting, no cinematic shadows
- No anime stylization, no digital cleanness, no glossy polish

Duration: 4 seconds.
```

#### V1 — research-corrected baseline (~80 words)
```
Traditional 2D animation pencil test in the style of classic Disney rough animation. Sean walks left to right across the frame at a steady, relaxed pace. His head turns slightly as he takes in the floating Film props around him. The props stay stationary; only Sean moves. Sean is clean-shaven throughout.

CAMERA: Completely static, locked tripod.

STYLE: Graphite on cream paper, rough pencil line quality, organic line wavering, visible construction marks, warm ivory paper tone, flat graphite shading.

Duration: 4 seconds.
```

#### V2 — V1 + transition-arc framing (~95 words)
```
Traditional 2D animation pencil test in the style of classic Disney rough animation. Starting with Sean stepping into frame from the left amid floating Film props, transitioning to him walking steadily across the frame with his head turning to take in the props, ending with him approaching the right edge as the Film props give way. The props stay stationary; only Sean moves. Sean is clean-shaven throughout.

CAMERA: Completely static, locked tripod.

STYLE: Graphite on cream paper, rough pencil line quality, organic line wavering, visible construction marks, warm ivory paper tone, flat graphite shading.

Duration: 4 seconds.
```

#### V3 — V1 + animation-timing language (~90 words)
```
Traditional 2D animation pencil test in the style of classic Disney rough animation. Sean walks left to right across the frame: anticipation as his weight shifts forward, settled walk cycle through the middle, head turning with a slight delayed follow-through to take in the floating Film props. The props stay stationary; only Sean moves. Sean is clean-shaven throughout.

CAMERA: Completely static, locked tripod.

STYLE: Graphite on cream paper, rough pencil line quality, organic line wavering, visible construction marks, warm ivory paper tone, flat graphite shading.

Duration: 4 seconds.
```

#### V4 — V1 + audio cues (~90 words)
```
Traditional 2D animation pencil test in the style of classic Disney rough animation. Sean walks left to right across the frame at a steady, relaxed pace. His head turns slightly as he takes in the floating Film props around him. The props stay stationary; only Sean moves. Sean is clean-shaven throughout.

AUDIO: Soft footsteps on paper, faint pencil scratch, paper rustle.

CAMERA: Completely static, locked tripod.

STYLE: Graphite on cream paper, rough pencil line quality, organic line wavering, visible construction marks, warm ivory paper tone, flat graphite shading.

Duration: 4 seconds.
```

#### V5 — V1 + canonical camera syntax (~85 words)
```
Traditional 2D animation pencil test in the style of classic Disney rough animation. Sean walks left to right across the frame at a steady, relaxed pace. His head turns slightly as he takes in the floating Film props around him. The props stay stationary; only Sean moves. Sean is clean-shaven throughout.

CAMERA: Locked tripod, micro push-in 2%, 50mm look.

STYLE: Graphite on cream paper, rough pencil line quality, organic line wavering, visible construction marks, warm ivory paper tone, flat graphite shading.

Duration: 4 seconds.
```

#### V6 — V1 minus genre anchor (~75 words)
```
Sean walks left to right across the frame at a steady, relaxed pace. His head turns slightly as he takes in the floating Film props around him. The props stay stationary; only Sean moves. Sean is clean-shaven throughout.

CAMERA: Completely static, locked tripod.

STYLE: Graphite on cream paper, rough pencil line quality, organic line wavering, visible construction marks, warm ivory paper tone, flat graphite shading.

Duration: 4 seconds.
```

#### V7 — V1 with hyper-trimmed style block (~75 words)
```
Traditional 2D animation pencil test in the style of classic Disney rough animation. Sean walks left to right across the frame at a steady, relaxed pace. His head turns slightly as he takes in the floating Film props around him. The props stay stationary; only Sean moves. Sean is clean-shaven throughout.

CAMERA: Completely static, locked tripod.

STYLE: Graphite on cream paper, organic line wavering, warm ivory tone.

Duration: 4 seconds.
```

#### V8 — Combined-best (V2 + V3 + V5 + V7, ~100 words)
```
Traditional 2D animation pencil test in the style of classic Disney rough animation. Starting with Sean stepping into frame from the left amid floating Film props, transitioning through a steady walk cycle with anticipation in his forward weight shift and a slight delayed follow-through as his head turns to take in the props, ending as he approaches the right edge. The props stay stationary; only Sean moves. Sean is clean-shaven throughout.

CAMERA: Locked tripod, micro push-in 2%, 50mm look.

STYLE: Graphite on cream paper, organic line wavering, warm ivory tone.

Duration: 4 seconds.
```

### 4.2 Test shots

| Shot | Anchors | Stresses |
|---|---|---|
| **W1 — Walk Film** | `runs/act2-exploration/concepts/zone1/film.png` → `runs/act2-exploration/concepts/bridges/film_to_animation.png` | Locomotion, full-body motion, walk-cycle physics |
| **S0 — Stubble grow-in** (fallback: `terminal_closeup_companion` if S0 anchors aren't locked at execution time) | desk-scene start → end | Identity preservation under subtle change, micro-expression stability |

A winner has to land both. The two shots stress different failure modes. Whichever shot fills the second slot is hereafter referred to as the **identity-stress shot**.

### 4.3 Run parameters

| Param | Value |
|---|---|
| Model | `bytedance/seedance-2.0/fast/image-to-video` |
| Resolution | `720p` |
| Duration | `4s` (matches API floor; matches existing shot list) |
| `generate_audio` | `False` |
| Seeds (per variant × shot) | `42`, `1337` |
| Aspect ratio | inherited from start frame |

After the winner is locked, **one additional run on Standard tier** on the identity-stress shot verifies that fidelity scales Fast→Standard. Adds ~$5 to total budget.

### 4.4 Scoring rubric

5 binary criteria. Manual scoring by Sean.

| # | Criterion | Yes/no question |
|---|---|---|
| 1 | Style preservation | Does the clip maintain rough pencil line quality, paper grain, and visible construction marks throughout — without digital smoothing, anime stylization, or photoreal rendering creeping in? |
| 2 | Identity preservation | Does Sean remain recognizably himself from frame 1 to last frame, matching the start anchor and arriving at the end anchor? |
| 3 | Motion plausibility | Is the action physically and anatomically coherent (no morphing limbs, no warping, no rubber-banding)? |
| 4 | No artifacts | Is the clip free of major artifacts (flickering, ghosting, hand/finger distortion, texture crawl, jitter)? |
| 5 | Anchor adherence | Do the start and end of the clip plausibly match the start and end anchor frames (composition, pose, environment all line up at boundaries)? |

**Per-generation:** 0–5. **Per-variant per-shot (sum across 2 seeds):** 0–10. **Per-variant total (both shots):** 0–20.

**Decision rule:** highest total wins. Tiebreaker 1: identity-stress shot score. Tiebreaker 2: shorter prompt.

**Halt conditions:**
- If V0 wins by 2+ points over V1, the research-derived priors are wrong — investigate before locking template.
- If no variant scores ≥14/20 on the identity-stress shot, the template is fundamentally weak — return to Phase 1 with a focused follow-up research query.

## 5. Infrastructure additions

### 5.1 Reusable (already in repo)

- [pipeline/seedance_lib.py](../../../pipeline/seedance_lib.py) — env, run dir, upload, log, frame math
- [pipeline/seedance_generate.py](../../../pipeline/seedance_generate.py) — sync `--shot` mode (the bake-off harness wraps this)
- [pipeline/seedance_shotlist.yaml](../../../pipeline/seedance_shotlist.yaml) — shot definitions (W1 already defined; S0 to be added if missing)

### 5.2 To build (small)

1. **`pipeline/seedance_bakeoff.py`** — wrapper that takes a variants file + test-shots list, iterates `variant × shot × seed`, calls Seedance via `seedance_lib`, writes outputs to a structured run dir, refuses to overwrite, logs every call to `bakeoff_log.jsonl`.

2. **`pipeline/seedance_bakeoff_variants.yaml`** — defines V0–V8 with their template-form prompts (with shot-specific action substitution).

3. **`runs/seedance-bakeoff_2026-05-09/scoring.csv`** — empty scoring template, columns: `variant, shot, seed, c1_style, c2_identity, c3_motion, c4_artifacts, c5_anchor, total, notes`.

### 5.3 Run directory layout

```
runs/seedance-bakeoff_2026-05-09/
├── manifest.lock.yaml          # frozen variants + run params
├── V00_v3_control/
│   ├── W1/
│   │   ├── seed_0042/output.mp4
│   │   └── seed_1337/output.mp4
│   └── S0/
│       ├── seed_0042/output.mp4
│       └── seed_1337/output.mp4
├── V01_research_corrected/...
├── ... (V02–V08)
├── bakeoff_log.jsonl            # per-call: variant, shot, seed, request_id, cost
└── scoring.csv                  # manual rubric fill
```

## 6. Deliverables

| Deliverable | Path | Purpose |
|---|---|---|
| Bake-off run dir | `runs/seedance-bakeoff_2026-05-09/` | Raw evidence — all clips kept |
| Manual scoring CSV | `runs/seedance-bakeoff_2026-05-09/scoring.csv` | Sean's binary rubric scores |
| Synthesis writeup | `runs/seedance-bakeoff_2026-05-09/results.md` | Which variant won, by what margin, on which axes; notes on failed variants |
| **Locked template** | `prompts/seedance-template-v4.md` | The canonical asset — copy/paste structure for all future shots, with documented evidence and bake-off citations |
| CHANGELOG entry | `CHANGELOG.md` | Decision log: template v4 locked, evidence summary, supersedes v3 |
| CLAUDE.md update | `CLAUDE.md` | Updates source-of-truth doc table to reference template v4 |

## 7. Phase 3 — Apply template (out of this design's scope; the template is the input)

After v4 is locked:
1. Rewrite Act 2's 10 shots using the template (mechanical fill-in)
2. Generate them at Standard tier
3. Manually rubric-score each shot
4. For any shot scoring <4/5: hand-tune that single prompt, OR trigger a small autoresearch loop (5–10 iterations) scoped to that shot only

Phase 3 gets its own implementation plan once Phase 2 lands.

## 8. Cost & time

| Phase | Cost | Wall clock |
|---|---|---|
| Phase 1 (research) | $0 | done |
| Phase 2 (bake-off + Standard verification) | ~$40 | ~3 hrs API runtime + ~45 min manual scoring + writeup |
| Phase 3 (Act 2 production) | ~$30 (+optional autoresearch ~$10–20) | ~1 day |
| **Total to canonical template + Act 2 done** | **~$70–90** | **~2 days** |

## 9. Risks & mitigations

| Risk | Mitigation |
|---|---|
| V0 wins by 2+ points over V1 — research priors wrong | Halt condition; investigate which prior is broken before locking template |
| No variant clears ≥14/20 on identity-stress shot | Halt condition; return to Phase 1 with a focused follow-up query |
| Manual scoring fatigue / inconsistency | Score one variant at a time; randomize order; rubric is binary so consistency is high |
| Fast→Standard tier divergence | Verification run on harder shot at Standard before production lock |
| Template overfits to W1 + S0 specifically | Phase 3 surfaces this immediately on the other 8 Act 2 shots; surgical autoresearch fallback exists |
| API cost overrun | Bake-off has fixed `9 × 2 × 2 = 36` generations — hard ceiling, not iterative |

## 10. Out of scope for this design

- Per-shot prompt tuning for individual Act 2 shots (Phase 3)
- Building an autoresearch optimizer loop (Phase 3, only if needed)
- Scoring infrastructure beyond a manual CSV (Claude vision judge deferred until autoresearch is triggered)
- Optimizing existing Claude skills (`prompt-engineering`, `image-generator-prompt-science`) — orthogonal effort
- Audio generation tuning — fixed at `generate_audio=False` for this entire effort

---

## Approval gates

- [x] **Approach approved** (2026-05-09): Approach 1 (research-then-bake-off, manual scoring), template-as-asset
- [x] **Variant matrix approved** (2026-05-09): 9 variants, 6 testable axes
- [x] **Test shots, run params, rubric approved** (2026-05-09)
- [ ] **This design spec approved** — pending review
- [ ] **Implementation plan written** — invoke `writing-plans` skill after design approval
