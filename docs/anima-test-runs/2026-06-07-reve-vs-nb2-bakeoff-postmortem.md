# Reve vs NB2 Bake-Off — Operational Postmortem

*2026-06-07 (run stamped 2026-06-08 UTC). The operational companion to the [field report](2026-06-07-reve-vs-nb2-editing-field-report.md). What went right, what went wrong, and what the next costed run should do differently. The *result* is in the field report; this is about *how the run was conducted*.*

> **Final verdict (Sean, eyeball): Reve FAILS for editing the Sean character — face morph/skew.** The run was conducted cleanly and answered the question; the answer is "no" for Sean editing. The most important methodological lesson — that the headline metric scored Reve as a *pass* while the face was visibly broken — is in §"The metric said pass; the eye said fail" below.

---

## The one-line lesson

**A human eyeballing an inferred schema is not verification — hitting the API once is.** Sean confirmed the scaffolded Reve schema looked right; the API rejected it on every field name. A single throwaway live call (a free 400) would have caught what a visual review could not. Build the "first real call" *into* the schema gate next time, not after it.

---

## What went right

- **The smoke-before-spend ladder did its job.** The 1-case live smoke surfaced the schema failure (`HTTP 400` on both Reve variants) *before* the 15-image full run. Had we skipped straight to the full run, we'd have burned the NB2 column and gotten a results matrix with three "missing" Reve cells and no idea why. The ladder is the reason the wrong schema cost ~$0.13 of probing instead of a confusing full run.
- **Fleet-ops discipline held end to end.** `ANTHROPIC_API_KEY` unset the whole session (verified before every phase); the `--score-em` guard was armed; everything ran in the `bakeoff/reve-vs-nb2-editing` worktree with main untouched; singleton pre-flight clean; no orphans at teardown. Money correctness was never in doubt.
- **DINOv2 engaged for real.** `torch`/`torchvision`/`transformers` loaded in the worktree venv; the trace reads `dinov2`, not `pil-perceptual`. The identity read is genuine.
- **The API taught us the schema, cheaply.** Reve returns *structured* 400s (`MISSING_REQUIRED_PARAMETER` / `UNRECOGNIZED_PARAMETER` / `INVALID_PARAMETER_TYPE` with the offending field names). Rejected calls are free, so the full real schema was reverse-engineered from error messages at $0, with one charged call each to confirm response shape + credits + version.
- **Honesty gates held.** The t3 stand-in→real-frame swap was done pre-scoring as a validity fix; the fast tier was *refused* rather than guessed (the runner raises instead of silently running standard); watermark/C2PA was reported as "no standard markers detected (no dedicated tool)" rather than a confident "no C2PA."

---

## What went wrong (and the fix)

### 1. The inferred schema was wrong on every field — and "schema confirmed" didn't catch it
The scaffold's mirror-inferred schema (`prompt` / `image`|`images` / `fast: bool` / `data[0].b64_json`) was wrong in every particular. The real schema: Edit `{edit_instruction, reference_image}`, Remix `{prompt, reference_images}`, tier via a `version` string, response a flat top-level base64 `image`. The Phase-B gate (print constants → human confirms) is necessary but **insufficient** — a human can't field-check an auth-gated API from a printed payload.
- **Fix for next time:** the schema gate should end with a *single deliberate live call* (a cheap one, or a request expected to 400) and inspect the response, not a visual sign-off. For an API with structured errors, that one call is worth more than any amount of doc-reading.

### 2. The harness silently swallows Reve API errors
`bakeoff.py`'s generate loop calls `invoke_reve(...)` and only reads `r.stub_fallback`; it never checks `r.ok` / `r.exit_code`. On the 400, `invoke_reve` returned `exit_code=400` with **no output PNG written**, the loop recorded `stub_fallback=False`, printed a clean line with no `[STUB]` tag, and exited 0. The failure was invisible except in the opt-in debug log. Scoring would later have marked those cells "missing" with no explanation.
- **Fix:** the generate loop should surface a non-ok `ReveResponse` (print a `[HTTP 400]` tag, count failures, and refuse to proceed to scoring if any non-stub cell is missing). Filed as a harness improvement; not fixed this run to avoid changing the harness mid-spend beyond the verified schema correction + the non-scoring debug hook.

### 3. The fast tier was console-gated and cost a second stop
`version` accepts *any* string without parse-time validation, there's no models/versions endpoint (all 404), and no separate fast endpoint exists — so the fast version strings were undiscoverable by probing and required Sean's console doc (the Reve Edit API console page he provided, which lists `reve-edit-fast@20251030`). The remix-fast string isn't in that (Edit-only) doc; it was confirmed empirically (`reve-remix-fast@20251030` → 200, 5 credits). The runner now refuses fast with an unknown version rather than silently running standard.
- **Lesson:** for a versioned model API, capture the *full* version enum (all endpoints) up front. The Edit doc covered Edit; Remix needed a separate confirmation.

### 4. Spend ran ~35% over the plan estimate — all schema-driven
Plan estimate for the full generate was ~$0.57. Actual total ≈ **$0.77**. The overage is entirely the wrong schema's tax: standard discovery probes (~$0.12) + an NB2 re-generation ($0.067, caused by clearing `.cache` between the stub-sanity and corrected smoke) + fast-tier verification ($0.013). No runaway, no surprise billing — just the cost of learning the schema live. Still trivial in absolute terms.

---

## The metric said pass; the eye said fail (the biggest lesson)

The headline metric, DINOv2-vs-per-view-anchor, scored Reve **≥ NB2 on identity** — decisive `t2-remix-3quarter` +0.041, in-between +0.006, no Subject-Collapse. By the harness rule that is a pass (pilot keyframes + adopt in-betweens). **Sean's eyeball on the face crops overturned it: the Reve faces are morphed and skewed** (asymmetric/melted eyes, distorted features) even though body, pose, palette, and pencil-test register hold.

This is not a contradiction — it's the metric working as documented and being **insufficient**:
- DINOv2-vs-**full-figure**-anchor embeds the whole figure; the face is a small fraction of that embedding. A morphed face on a correct body + composition still scores high.
- Reve matched the reference *composition* closely (it reinterprets less than NB2), and DINOv2 rewards that closeness (§3.5: "DINOv2 over-rewards copying"). So Reve scored *higher* while being *worse* on the one thing that matters for an identity-locked character.
- I reviewed the full-figure outputs by eye during the run and they looked fine; **the morph was only obvious at face-crop zoom.** I should have zoomed to the face before reporting a score-based verdict.

**Process fixes for any future identity-edit eval:**
1. **Gate identity on the face, not the figure.** Crop to the face (or run a face-region DINOv2 / a face-embedding metric / pairwise-Em) — whole-figure cosine cannot adjudicate facial identity.
2. **Always zoom to the identity-critical region by eye before writing a verdict.** A contact-sheet / full-figure look masks exactly this failure (the same lesson as the motion-sight contact-sheet honesty clause).
3. **Treat the human eye as the gate, the metric as the screen.** The metric narrows what to look at; it does not decide. Engine Truth: "recognizably itself" is the human's call.

The pairwise-Em refinement I flagged as "the right next step" would likely have caught this (a side-by-side "which face is more Sean?" is far more sensitive than absolute whole-figure cosine) — worth building before any future identity-edit bake-off.

## Spend ledger (actual)

| Phase | What | Reve credits | NB2 imgs |
|---|---|---|---|
| First live smoke (400) | NB2 t1 generated; 2 Reve 400s (free) | 0 | 1 |
| Schema discovery probes | 3 standard calls (remix×2 + edit) | 90 | 0 |
| Corrected smoke | reve-std edit t1; NB2 t1 re-gen (cache cleared) | 30 | 1 |
| Fast-tier verification | remix-fast + edit-fast | 10 | 0 |
| Full generate | std: 1 edit + 3 remix live (t1 cached); fast: 2 edit + 3 remix | 145 | 4 |
| **Total** | | **275 (~$0.37)** | **6 (~$0.40)** |

**Grand total ≈ $0.77.** Reve credits remaining: **7225** (from ~7500). NB2 at $0.067/image (1024² tier). All `--score-em` Em escalations rode the Claude subscription ($0 API).

---

## DINOv2 tier engagement — verified, not assumed

`torch 2.12.0 / torchvision / transformers 5.10.2` installed in the worktree `.venv` (cached wheels from main's `.venv`; install was fast). Both the stub plumbing check and the live score printed `DINOv2 method engaged: dinov2`. Had it read `pil-perceptual`, the run would have been void (not a real identity read) — the field report would have said so and stopped. It did not; the read is real.

---

## Lessons for the next costed run

0. **Gate identity edits on the face, by eye — never whole-figure DINOv2 alone.** The single most important takeaway (see §"The metric said pass; the eye said fail"): the metric passed Reve while the face was broken. Crop to the identity-critical region, look at it, and prefer pairwise-Em / a face-region metric for the call.
1. **End every "verify the schema" gate with one real call.** Visual confirmation of an inferred payload is not verification when the source is an auth-gated SPA. A structured-error API will teach you the schema for free.
2. **Make the harness fail loud on API errors.** A bake-off that silently records a missing cell as a non-stub success is worse than one that crashes — fix `bakeoff.py` to surface non-ok `ReveResponse`es before the next run.
3. **Capture the full version/model enum up front** for versioned APIs — across *all* endpoints, not just the one whose doc you have.
4. **Don't clear `.cache` between smoke rungs** unless you mean to re-pay. The corrected-smoke NB2 re-gen was avoidable.
5. **The opt-in debug hook earned its keep.** `REVE_DEBUG_LOG` (non-scoring, try/except-wrapped) is the only reason the 400s, latencies, credits, and served versions were visible at all. Keep that pattern for any new external-API runner.
6. **N=1 + small margins = pilot, not migrate.** The result is directionally clear (no downsampling collapse; Reve ≥ NB2 on identity) but the magnitudes are within noise. The honest next step is a replicated + pairwise-Em pass, not a wholesale model swap.
