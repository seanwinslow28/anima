# Cy's Bibles look *like* Sean, not *as* Sean — the visual-fidelity post-mortem

*2026-05-29. The 2026-05-28 session landed two locked Bibles end-to-end against live Opus 4.7 + NB Pro + Gemini 3.1 Pro. The runner held up under load; the test report tells that story well. This is the part the test report didn't cover — what Sean saw when he actually looked at the plates. The poses are good. The identity isn't. The plates pass Gemini's verification and still read as a different character. This debrief names where the fidelity leaks, why Gemini's pass didn't catch it, and what we do about it.*

---

## 1. What worked

It would be a mistake to read this as a failed shoot. Most of the rig held.

The **five-attempt debug saga is portfolio content.** Runner robustness landed under live fire — `max_turns 1→10`, the `.env` dual-source gate, defensive reference-path resolution, `sys.executable` subprocess pinning. Each fix sat on a code branch the stub-fallback path had been silently bypassing in CI, and only a real-model call could surface it. That's the kind of war story that proves the pipeline ships, not just compiles.

**Two Bibles are locked on disk** with real four-color palettes, populated IR.\* rule graphs (20 for sean-anchor across 8 categories, 13 for claude-mascot), risk-bibles that name their own negative space, and confidence-notes that hedge honestly. The **closed `style_register` vocabulary validated across two categorically different registers** — pencil-test-colored and pixel-art-8bit — with zero pencil-test markers leaking into the mascot Bible. The Task 1.4.5 defang held against live Opus, which the stub-only test suite could never have proven.

The **contract layer is sound.** The orchestrator, the content-addressed cache (keyed correctly on reference *content* hashes, confirmed in this session), the Cy scratchpad as bidirectional-provenance evidence, the audit trail — all shipped and all behaved. **157 tests green, re-confirmed this session** in a clean offline environment. Maya and Em show no regression from the shared-infrastructure changes (§4).

None of that is in question. What's in question is one thing: the generated plates don't look enough like Sean's characters.

## 2. What didn't work — the fidelity gap

Sean caught it on visual inspection, which is the only place it *could* have been caught — because every automated gate passed.

### 2.1 The plate-by-plate drift table

Severity scale: **none** (faithful) · **minor** (recognizably the character, small marker drift) · **moderate** (recognizable but markers wrong) · **severe** (reads as a different character). "Gemini verdict" is what Pass-3 returned; per-plate verdicts are **not persisted to disk** (a finding in itself — §2.3), so PASS is inferred from the run log's "1 plate flagged for human gate," which the test report identifies as `head-turn-09` — an *ingest*, not a generated plate. Every generated plate passed.

**sean-anchor** (`pencil-test-colored`)

| target_path | source_ref compared | severity | what drifted | IR.\* violated (visually) | Gemini |
|---|---|---|---|---|---|
| `turnarounds/head-front.png` | anchor.png + turnaround-1 head | **severe** | Idealized romance-hero face — sharper cheekbones, aquiline nose, fuller lips, deeper-set eyes, heavier square jaw. Not the friendlier rounder cartoon Sean. Rendered monochrome graphite vs. the colored anchor. | `IR.sean.face.jaw-line-angular-not-rounded` (over-angularized), `IR.sean.face.eye-spacing-one-eye-width` (narrowed/deeper-set), palette mismatch (monochrome) | PASS |
| `turnarounds/head-3quarter.png` | anchor + (referenced **drifted** head-front) | **severe** | Inherits and reinforces head-front's drift — the same different-person, now self-consistent. Compounding-reference failure. | same as head-front, plus identity propagation | PASS |
| `turnarounds/head-back.png` | profile-left/right only — **anchor not in reference set** | **moderate** | Extrapolated back-of-head with zero anchor grounding (Opus emitted this plate with no `anchor.png` reference). Hair mass plausible but ungrounded. | `IR.sean.hair.silhouette-tousled-medium-short` (ungrounded) | PASS |
| `expressions/neutral.png` | anchor + drifted head-front | **severe** | Equals the drifted head-front identity. Expression read (neutral) is fine; the face is the wrong face. | face-cluster rules | PASS |
| `expressions/focused.png` | anchor + head-front + neutral | **severe** *(inferred from chain)* | Same drifted identity; expression execution good. | face-cluster rules | PASS |
| `expressions/surprised.png` | anchor + head-front + neutral | **severe** | Wide eyes / parted lips / raised brows executed well — the expression *acting* is genuinely good. Identity is the same wrong person. | face-cluster rules | PASS |
| `expressions/contemplative.png` | anchor + drifted head-3quarter + neutral | **severe** *(inferred)* | Drifts off two already-drifted references. | face-cluster rules | PASS |
| `props/stylus.png` | anchor only | **severe (different failure)** | NB Pro **rendered the prompt text as handwritten captions on the plate** — "A working-illustrator's stylus — straight cylindrical barrel approximately 14cm long…", "Canonical prop reference for IR.seanan.prop…" (note the garbled rule ID, hallucinated from the prompt). The model treated meta-instructions as text-to-draw. | n/a (prop) — but proves the prompt is being read as *content* | PASS |
| `turnarounds/body-{front,3quarter,profile-right,back}.png` | turnaround-1 regions | **none (faithful) but mis-framed** | Byte-identical full copies of `turnaround-1.png` (6,151,720 bytes each). The `#region:body-front` crop **never executed** — each "turnaround" is the entire sheet. | n/a — framing bug, not identity | n/a (ingest) |
| `turnarounds/head-profile-{left,right}.png` | head-turn-1 / head-turn-9 | **none, register mismatch** | Faithful copies of line-art motion frames — pure black-on-white line, a different register from the colored anchor. The turnaround set is internally register-inconsistent. | n/a | n/a (ingest) |

**claude-mascot** (`pixel-art-8bit`)

| target_path | source_ref compared | severity | what drifted | IR.\* violated (visually) | Gemini |
|---|---|---|---|---|---|
| `turnarounds/body-3quarter.png` | anchor.png (tiny octopus-critter) | **severe** | A categorically different creature: detailed chibi *humanoid* with two arms, two legs, a smiling mouth, and cheek-blush. The anchor has a snout, multiple stub legs, a tail, and no arms, at ~16–24px. Palette + vertical-dither register held; the *character* did not. | `IR.claude-mascot.proportion.silhouette-round-topped-lozenge` (became a standing humanoid), `…head-to-body-2-to-3-chibi` (reads ~1:2) | PASS |
| `turnarounds/head-front.png` | anchor | **severe** | Clean generic round smiley-head. Lost the anchor's defining snout/nose protrusion and blocky low-res form. Visible gradient/anti-aliasing on the shadow side. | `IR.claude-mascot.style.integer-pixel-grid-no-subpixel` + `…no-gradient-interpolation` (soft-edged shading present) | PASS |
| `turnarounds/body-profile-right.png` | anchor | **severe** *(inferred)* | Same generic chibi humanoid, side view. | proportion + silhouette rules | PASS |
| `turnarounds/body-back.png` | anchor | **severe** *(inferred)* | Same; extrapolated back. | proportion + silhouette rules | PASS |
| `expressions/surprised.png` | anchor | **severe** *(inferred)* | Generic chibi head, open mouth. | face + proportion rules | PASS |
| `expressions/contemplative.png` | anchor | **severe** *(inferred)* | Generic chibi head, curved mouth. | face + proportion rules | PASS |
| `turnarounds/body-front.png`, `expressions/neutral.png` | anchor | **none** | Faithful ingested copies of the anchor. | n/a | n/a (ingest) |

The pattern is identical across both registers: **the generated plates satisfy the prose rules and look like a different character.** The mascot makes it unmissable because the source is so simple and quantifiable — a tiny octopus became a gingerbread man, and it passed.

### 2.2 The poses are the good news

Worth saying plainly: the *acting* and *construction* are excellent. The expression arc reads (neutral → focused → surprised → contemplative all land their intended emotion), the pencil-test surface is beautiful (warm cream paper, construction-line underlay, cross-hatch shadow, hole-punch production marks), the pixel-art palette and dithering are clean. NB Pro is a strong renderer. The failure is narrow and specific: **it is not preserving identity from the reference images.** Everything that can be specified in words came out right. Everything that lives in the anchor's pixels — *this* face, *this* creature — drifted.

### 2.3 Why Gemini's Pass-3 didn't catch it

This is the structurally interesting part, and it generalizes. **Gemini grounds its verdict against the IR.\* rule *descriptions* Cy wrote — prose — not against the source-ref *pixels*.** A plate that nominally satisfies "jaw angular at the mandibular corner, ~100–110°" and "eyes spaced approximately one eye-width apart" passes, because the drifted romance-hero face *does* have an angular jaw and ~one-eye-width spacing. The rule is true of the plate. The plate is still the wrong person.

Prose rules are necessary but they are a **lossy compression of identity.** They capture the markers a human thought to write down; they cannot capture the gestalt — the specific cartoon-ness of Sean's face, the specific blockiness of the mascot — that makes a character recognizably itself. Verification against prose can only ever confirm that the named markers are present. It is structurally blind to "looks like a different character who also happens to have those markers."

Compounding it: **per-plate Gemini verdicts are not persisted.** The only durable signal is the run log's "1 plate flagged for human gate." We can't reconstruct confidence scores or citations per plate from disk. So even the lossy verification leaves no audit trail to inspect after the fact.

This is the load-bearing finding, and it echoes the test report's organizing lesson — *"a successful exit code can lie about what actually happened"* — one layer up: **a passing critic verdict can lie about what the plate actually looks like, when the critic checks words instead of pixels.**

## 3. Why it happened — the root-cause trace

I traced the reference-image flow from Opus's emission through to the genai call. The references are *not* being dropped. Here is the actual mechanism, in order of contribution.

**(a) The skill script forwards references correctly — this is not a plumbing bug.** `nb_pro_runner.py:_build_skill_cmd` passes `--reference <p1> <p2> …`; the skill script (`generate_image.py:101`) loads each as `types.Part.from_bytes(...)` and prepends them to `contents`, prompt last. The cache key includes reference *content* hashes. References reach NB Pro as genuine multimodal inputs. Hypothesis "the runner passes references but the skill drops them" is **false**, confirmed by code-read.

**(b) Prompt-dominance over reference conditioning — the largest single contributor.** Cy's plate prompts are long, prescriptive verbal *descriptions of the character* ("heroic-realistic adult proportion… angular jaw… strong horizontal brow… warm graphite #3D3530…"). NB Pro can synthesize a plausible character from that text alone, and it weights the text heavily — producing a generic-handsome-man / generic-chibi that matches the *words* while treating the reference pixels as loose style hints. The `props/stylus.png` plate is the proof in the pudding: the model literally rendered the prompt's meta-prose as captions on the page. When the prompt is content, the prompt wins.

**(c) NB Pro's multi-reference identity-lock is independently degraded — externally documented.** This is not only an anima prompt problem. The Google AI Developers Forum carries an open, unresolved thread (Lauren Redman, 2026-03-04): *"since the launch of Gemini 3.1 Flash Image, the Pro model has become highly inconsistent… the model appears to **downsample reference images so aggressively that it can't see or replicate fine details, resulting in generic or inaccurate outputs.**"* A sibling thread is titled *"Nano banana pro ignoring prompt and reference images."* "Generic or inaccurate outputs" is precisely what we observed. The model itself is part of the problem, which means prompt-tightening alone may be **capped** below faithful identity. (Sean's call: we run the model bake-off in parallel with the cheap fixes, not after — §5.)

**(d) Reference-chaining compounds drift — sean-anchor specifically.** Opus emitted generated plates that reference *other generated plates*: `head-3quarter` references the already-drifted `head-front`; the expressions reference the drifted `neutral`; and `head-back` references **no anchor at all.** Once `head-front` drifted, the chain locked onto the drifted identity and reinforced it downstream. The runner is a faithful pass-through — `_run_plate` forwards exactly the references Opus emitted and never injects the anchor unconditionally. The addendum's own "what good looks like" example models this anti-pattern (`reference_images: ["anchor.png", "turnarounds/head-front.png"]` — chaining off a generated plate) and never mandates the anchor.

**(e) The register is mis-specified against the anchor — a contract bug.** `anchor.png` is a **full-color** illustration (blonde hair, navy tee, gray jeans, blue eyes, warm skin). Cy's `pencil-test-colored` IR rules and prompts describe monochrome warm-graphite with *"no explicit skin tone"* and cross-hatching. So even a perfectly faithful generation would diverge from the anchor on color. **Sean's decision: full-color is canonical Sean.** The rules are wrong, not the anchor. This is its own fix workstream — the `pencil-test-colored` rule graph must be rewritten to carry the palette/skin/hair colors the anchor actually shows.

**Root cause, in one sentence:** identity lives in the anchor's pixels, but generation is driven by a verbal description the model can satisfy without copying the pixels — and NB Pro's reference-conditioning is currently too weak (b + c) to override that description, while the verification gate checks the same words rather than the pixels (§2.3), so the drift ships silently. Chaining (d) and register mis-spec (e) make it worse.

## 4. Regression check — Maya and Em

Both **GREEN**. 157 tests pass (exact baseline). Specifics:

- **Maya — GREEN.** `test_planner.py`, `test_plan_cli.py`, `test_criteria*.py` all pass. The three-call ceiling is enforced agent-side at `planner.py:146` on an `opus`/`sonnet` counts dict — **independent of the SDK `max_turns`**. The `max_turns 1→10` lift governs SDK-internal turns *within* a single call; it cannot inflate Maya's call count. No regression.
- **Em — GREEN.** `test_vision_critic.py`, `test_cli_runners.py` pass. The defang touched standing-context prose, not verdict logic: Em still rejects any `fail`/`borderline` verdict that carries no cited criterion (`vision_critic.py:113–117`), escalation threshold intact at 0.7. The defang did not soften Em into passing everything.
- **Evals — not run in-sandbox** (they use a custom `cases.yaml` + `runner.py` harness, not pytest discovery; the `.venv` is a macOS interpreter that can't execute here). Unchanged per the test report: 10 passed + 2 xfailed + 1 xpassed. **Flag:** the closing-the-loop case 7 stays xfailed by design — it flips green when Em loads the merged `CriteriaBundle`'s IR.\* entries at run start. That is the natural next-implementation-session work *after* this fidelity fix lands; do not scope it here.

## 5. The structural fix

Sean's three locked calls shape the plan: **full-color is canonical** (e is in scope), **run the model bake-off in parallel** (not after), **adopt Opus 4.8 now** for Cy/Maya. Candidates, each with blast radius:

**Track A — cheap, ships immediately (prompt + runner + gate):**

1. **Re-weight prompts toward references, not description.** Stop re-describing the character in prose. Adopt NB Pro's documented best-practice pattern: short prompts with **explicit reference role tags** ("Image A: identity anchor — match this face exactly; Image B: pose target") rather than verbal character descriptions. Strip pipeline-meta text from prompts entirely (it gets rendered as captions). *Blast radius: prompt-file + Cy addendum edit. Smallest.*
2. **Inject the anchor + turnaround sheet unconditionally at the runner.** Make `_run_plate` (or `invoke_nb_pro`) the source of truth for "every generate plate is seeded with the anchor," regardless of what Opus emits. **Never chain off a generated plate** — references come from the source-ref set + anchor only. Fixes (d) and the `head-back`-has-no-anchor class of bug structurally. *Blast radius: runner contract. Medium.*
3. **Add a Pass-2.5 pixel-similarity gate before Pass-3.** Compute CLIP / DINOv2 / SSIM similarity between the generated plate and the source-ref it was meant to match; reject below a threshold *before* Gemini's prose check. Doesn't fix drift — surfaces it loudly so the prose pass can't mask it. Also **persist per-plate verdicts** (similarity score + Gemini verdict + citations) to a run artifact. *Blast radius: new node + criteria. Medium.*
4. **Rewrite the `pencil-test-colored` rule graph to full-color** (Sean's call e). Carry the anchor's actual palette (blonde hair, navy tee, gray jeans, warm skin) into the IR.\* rules and plate prompts. Fix the `#region` crop bug so body turnarounds are actually cropped, not full-sheet copies. Resolve the line-art-vs-color register inconsistency in the turnaround set. *Blast radius: Bible re-author. Medium-large.*

**Track B — runs in parallel (model bake-off), per Sean's call:**

5. **Bake off NB Pro against stronger identity-lock paths.** External evidence says NB Pro multi-ref is structurally unreliable right now. Candidates from Phase-4 research + Image-Model-DR: **FLUX.2 multi-reference** (up to 8 API / 10 playground refs, fuses up to 10 into a stable identity, ~92/100 community consistency benchmark); **GPT-Image-2** edit/coherent-set for iterative refinement; **self-hosted FLUX.1 Kontext [dev] + a custom character LoRA** trained on Sean's ~30 approved Act 1 frames (Image-Model-DR Config C / Experiment 1 — ~3hrs on a 4090, $0 marginal after training), optionally stacked with a **FLUX sketch-style LoRA** (Shakker-Labs `FLUX.1-Kontext-dev-LoRA-Sketch-Style` exists today) for the pencil register. The Bible's `flux_lora_seed_plates` field already anticipates this. *Blast radius: model assignment in v2 §6. Highest — but if NB Pro is the limit, no prompt fix recovers it.*

6. **Adopt Opus 4.8 for Cy + Maya now** (Sean's call). Same price as 4.7; +agentic-coding, and ~4× less likely to let flaws pass / more likely to flag uncertainty — which is directly useful for Cy's confidence-hedging honesty and Em-adjacent judgment. Fold into the fidelity commit. *Note for honesty: 4.8 will not fix the fidelity gap — that's an image-model problem, not a reasoning-model one. It helps author the fix; it isn't the fix.*

## 6. Recommended fix sequence

The brief's instinct was "cheap-first, escalate only if needed." Sean's call modifies it to run Track B **concurrently**, because the external evidence says the cheap track may be capped by the model. So:

1. **Commit 1 — Track A items 1+2+6:** prompt re-weighting (role tags, strip meta), unconditional anchor injection + no-chaining, Opus 4.8 bump. Re-run both Bible bakes. This is the fastest possible read on "how much does NB Pro recover when we stop fighting it with prose and feed it the anchor properly?"
2. **Commit 2 — Track A item 3:** the pixel-similarity gate + persisted per-plate verdicts. Now drift is measured, not eyeballed — and the bake-off in Track B has a quantitative scoreboard.
3. **In parallel from day one — Track B item 5:** stand up the FLUX.2 / GPT-Image-2 / FLUX+LoRA bake-off using the same source-refs and the same similarity gate as its scoreboard. Pick the winner empirically (this is the "empirical, not vibes" belief).
4. **Commit 3 — Track A item 4:** rewrite the `pencil-test-colored` rule graph to full-color and fix the crop/register bugs. Do this once the winning model is known, so the rules are written against the model that will actually render them.

Each step is a discrete commit; tests stay green or the step rolls back. The disambiguating experiment to run *first* (it's nearly free and settles b-vs-c): re-run one drifted plate with **anchor-only reference + a terse "redraw this exact character, front view, same face" prompt.** If fidelity jumps, prompt-dominance (b) was the lever and Track A will largely recover it. If it stays generic, the model (c) is the limit and Track B is load-bearing.

---

## Appendix — Phase 0 disambiguating experiment result (2026-05-29, fix session)

The experiment §6 prescribed ran first, before any code. One drifted plate
(`turnarounds/head-front.png`) re-generated against **anchor.png only** with a
**terse role-free prompt** — *"Redraw this exact character — same face, same
hair, same friendly cartoon style, front-facing head-and-shoulders view. Keep
the full color."* — through the unmodified skill script at
`gemini-3-pro-image-preview`. Evidence saved to
`docs/anima-test-runs/2026-05-29-phase0-fidelity-experiment/`
(`anchor-only-terse-prompt-result.png` vs `drifted-head-front-BEFORE.png`).

**Verdict: fidelity jumped, decisively.** The terse-prompt output is
recognizably the *same character* as the anchor — blonde tousled hair, navy
tee, blue eyes, warm full-color skin, and the friendly *rounded cartoon* face,
not the monochrome aquiline romance-hero the verbose-prompt plate produced. A
stranger comparing both against the anchor would say "same character" of the
terse result and "different character" of the drifted plate.

**What this settles (the b-vs-c question):** root cause **(b) prompt-dominance
was the lever, not (c) a hard NB Pro multi-ref ceiling.** When the prose stops
re-describing the character and the model is simply told to copy the anchor,
NB Pro recovers identity at single-anchor front view. The externally-documented
multi-ref regression (c) is real but is **not** the binding constraint here —
it was being triggered *by* our own verbose, character-describing prompts.

**Consequences for the plan:**
- **Track A is load-bearing and expected to largely close the gap.** Weight
  effort there. Commit 1 (prompt re-weighting + unconditional anchor injection
  + no-chaining) is the high-value work.
- **Full-color (decision e) is confirmed natural.** The model produced the
  anchor's real palette unprompted; "keep the full color" was enough. The
  monochrome drift was authored *into* the rules, not imposed by the renderer.
- **Track B (the bake-off) drops from critical-path to de-risking option.**
  Sean locked "run in parallel"; the Phase 0 result is grounds to revisit at
  the commit-1 checkpoint whether the expensive FLUX/GPT-Image-2/LoRA stand-up
  is still warranted once the re-bake shows how much Track A recovered. Flagged
  for Sean, not unilaterally descoped.

---

*The engine truth says the character must be "recognizably itself in its intended medium." Right now it's recognizably *a* character in a beautiful medium — just not Sean's. The poses proved NB Pro can act. This fix is about making it cast the right actor. — filed 2026-05-29*
