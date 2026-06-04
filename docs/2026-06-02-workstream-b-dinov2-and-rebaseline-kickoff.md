# Kickoff — Workstream B: DINOv2 backstop + replicated clean re-baseline

*2026-06-02. Costed, eval-gated handoff for a Claude Code session. The uncosted hardening (Workstream A) shipped as PR #18 and is merged. Read these first: the anchor postmortem [`docs/anima-test-runs/2026-06-02-em-gemini-transport-rebaseline-postmortem.md`](anima-test-runs/2026-06-02-em-gemini-transport-rebaseline-postmortem.md), the A kickoff [`docs/2026-06-02-em-provenance-and-hardening-kickoff.md`](2026-06-02-em-provenance-and-hardening-kickoff.md), and the eval handbook [`docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md`](research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md). This is greenlit by Sean for spend.*

---

## Where A left us

Em runs reference-blind by default (the safe `false_pass 0.00 / recall 1.00` profile). Both costed callers (Em + Cy Pass-3) are pinned-by-ID on the Gemini API and log the served model. The references-grounding path is dormant behind `critics.t2.attach_references`. The re-baseline diagnosed the references regression as **part Opus verdict variance, part reference confabulation** — an MLLM handed a reference bundle recites it onto the subject. The postmortem's verdict: the fine-grained identity/proportion check wants a **deterministic** signal that has no story to tell. That signal is DINOv2.

## What B is — and the cost taxonomy that sequences it

Two different kinds of "costed" live in B, and they sequence the work:

- **Compute-costed, $0 API spend:** the DINOv2 backstop. DINOv2 is a *local* model (`pip install torch torchvision transformers`); running it burns CPU/GPU and disk, **not** the bounded `GEMINI_API_KEY` and **not** the Opus subscription. So the DINOv2 spike can run safely without touching any spend line. **Do this first.**
- **Spend-costed:** the replicated re-baseline and the bake-off — Gemini API on the bounded key + Opus on the subscription. These only run *after* the DINOv2 spike clears its go/no-go, and under full fleet-ops discipline.

This is the opposite of intuition: the "AI backstop" is the cheap, safe first move; the "just re-measure" step is the one that costs money.

---

## The central hypothesis — stated so the eval can kill it

> A deterministic DINOv2 identity/proportion **similarity** (subject vs view-matched reference; *low* similarity = drift), computed beside Em, flags the confabulation-class defects that the MLLM passes — **without** the confabulation, because an embedding similarity has no reference story to narrate.

**Honest scoping — what DINOv2 can and cannot backstop.** The two false passes from the re-baseline are *different defect classes*, and only one is a DINOv2 job:

| False-pass case | Defect class | DINOv2 a fit? |
|---|---|---|
| `proportion-eyes-body-profile-right` | identity / proportion drift (profile) | **Yes** — this is exactly the embedding-similarity case (caveat: it also cites *eye-color* drift; whether DINOv2 embeddings are sensitive to that is part of what the spike measures) |
| `stylus-hand-f13-cc01` | spatial / prop continuity (wrong hand) | **No** — a hand-flip doesn't move identity similarity; the figure is still embedding-recognizably Sean. Whether it's noise or a systematic Em blind spot is what B2's replication **diagnoses** — not the backstop's job either way |

If the spike proves DINOv2 separates the proportion class, that is a **win even though it does nothing for the stylus case** — the spike must not be graded against a defect it was never meant to catch. But be precise about what happens to the stylus case next. It is a **single-frame** case (`frames/defect_F13_stylus_hand.png`, cite `CC01`) where the wrong hand is visible in the one frame, so B2's `--runs 5` **diagnoses** it — it does not automatically fix it:

- If the verdict **flips** across runs → true Opus variance → the majority vote rescues it (B2 owns it).
- If it is **stable** (Em consistently passes the wrong-hand frame) → that is a real Em blind spot on fine prop-position that neither DINOv2 nor majority-vote touches. Its honest home is the **production deterministic CC01 gate** ([`pipeline/continuity_audit.py`](../pipeline/continuity_audit.py)), not T2 — report it as such rather than forcing it onto the backstop or laundering it into the replication number.

---

## B1 — DINOv2 backstop (compute-costed; do first; go/no-go gated)

### B1a — View-aware reference selection (approach A) — prerequisite, mostly uncosted
The existing similarity gate is **record-only even with DINOv2 active** (the 2026-05-29 finding) precisely because *a single front anchor can't separate legitimate view variation from drift*. A profile subject compared to a front anchor reads as "drift" when it's just a different view. So a real DINOv2 signal needs **per-view references**: a profile shot gets profile refs.

- `pipeline/agents/reference_selection.py`'s `select_references(character_id, checkpoint, beat, *, characters_root, cap=3)` **already accepts `checkpoint`/`beat`** — its docstring literally says *"v1 ignores checkpoint/beat (approach B)"*, so the signature is a built-for-it drop-in. Implement the view-aware ranking: infer the subject's view and rank turnarounds to match (profile subject → profile turnaround first).
- **Prerequisite to verify first:** the real `sean-anchor` Bible's `turnarounds/` must carry **inferable view labels** (front / profile / 3-quarter) that the ranker can match; if the naming isn't view-inferable, establishing that convention is part of B1a.
- **Eval-vs-prod asymmetry — scope it honestly.** In the eval, the subject's view is *readable from case metadata* (the cases carry it: `name: …-profile-right`, beat "body profile-right") — cheap and exact. In **production** there is no guaranteed labeled view, so prod view-inference is a separate, harder problem (a cheap view classifier or a manifest hint). B1a delivers the eval path; flag the prod path as follow-on so B1a doesn't over-scope.
- This is **deterministic code + TDD — no model spend.** It can land in its own small PR before any costed run.

### B1b — DINOv2 separation spike (compute-costed, $0 API)
The question, scored like any agent — segmented, false-pass-first:

> On the labeled `evals/vision_critic/` fixture set, does DINOv2 cosine **similarity** (subject vs view-matched reference; *low* similarity = drift) **separate** the identity/proportion defect cases from the clean cases?

- **Deps are already present — this is a confirm, not an install.** `torch 2.12.0` + `transformers 5.9.0` are in `.venv` (the A session's Cy Pass-2.5 already loaded `facebook/dinov2-small`), so `compute_similarity` should hit the `dinov2` rung today. **Assert `result.method == "dinov2"`** (NOT a silent PIL fallback — the gate's docstring warns a missing dep degrades silently to PIL). Only `pip install torch torchvision transformers` if a fresh env is missing them.
- Score DINOv2 similarity across the labeled fixtures using **view-aware refs from B1a**. Report a separation analysis: the similarity distribution for clean vs proportion-defect cases, and whether a threshold cleanly divides them. Reuse the segmented/false-pass scoring discipline from `evals/vision_critic/score.py`.
- **Go/no-go gate:** DINOv2 proceeds to integration **only if** it measurably separates the proportion/identity defect class from clean with a usable threshold. If it can't separate them, **stop and report** — that is a real finding (the deterministic signal isn't discriminative enough at this fixture resolution), not a failure to push through. `SIMILARITY_FLAG_THRESHOLD = 0.5` is the current placeholder; the gate **flags when `score < threshold`** (low similarity = drift), so the spike sets the real threshold from the separation data such that the proportion class falls *below* it and clean stays *above*.

### B1c — Integration (only past the go/no-go)
- Wire DINOv2 as a **deterministic signal beside Em** in the T2 path — augmenting, not replacing, the MLLM. Em owns style/register/semantic verdicts; DINOv2 owns a hard identity/proportion similarity that can *veto a pass* on the confabulation class.
- Keep it **honest about its scope:** DINOv2 flags identity/proportion, says nothing about spatial continuity (stylus) or motion. Log which signal produced a flag.
- TDD credential-free with the stub ladder (PIL rung) so CI stays green without torch; the real DINOv2 path exercises only when deps are present.

---

## B2 — Replicated clean re-baseline (spend-costed; after B1 integration)

Now the scorer's `--runs 5` (shipped in A5) earns its keep.

- Run the costed scorer at **`--runs 5`** on a **pinned, logged** model (read the served model back from `resp.model_version`; confirm it in the trace before trusting any number).
- **Rough spend/latency for the greenlight:** ~5 runs × 2 arms × ~23 performs cases ≈ **~230 Gemini calls** (~15s each on the bounded `GEMINI_API_KEY`) plus the Opus escalations that fire on borderline/hero shots (~60–199s each on the subscription). That's wall-time on the order of an hour-plus and a real (if modest) Gemini bill. Re-derive the estimate from the actual selected-case count before launching, and if it materially exceeds prior runs, stop and report it to Sean rather than spending blind.
- **Two arms for clean attribution** (the postmortem flagged the 0.62 baseline crossed transport + references):
  1. **reference-blind on the same API transport** — the true control the 0.62 number never had.
  2. **references-on (flag true) + view-aware selection + DINOv2 beside Em** — the candidate.
- Report per-segment **false_pass band** + the per-run flip table. The 0.15 was one noisy draw; the decision number is the majority-vote point estimate with its band.
- **This is the gate that decides whether `attach_references` ever flips back to `true`.** References return **only if** the candidate arm clears the false-pass gate (no regression vs the reference-blind control) *with the DINOv2 veto active*. If it still regresses, references stay off and DINOv2 stands alone as the identity signal.

---

## B3 — Three-way bake-off (spend-costed; last; only after B2)

- Re-run the T2 vision-critic bake-off (`evals/bakeoffs/2026-05-31-.../`) with **every column pinned by ID and correctly labeled** — the "Gemini" column was Flash, not Pro; pin it explicitly and log the served model.
- Attach references on all columns **only if B2 cleared the references question.** Otherwise run blind.
- This is where the deferred re-ratification of the 2026-05-31 bake-off labels gets resolved — **bring any label that looks wrong to Sean; do not edit a locked case label unilaterally.**

---

## Decision gates (do not cross without the prior result)

1. **B1b go/no-go** — DINOv2 separates the proportion class, or stop-and-report. (Compute only; safe to run.)
2. **B1 → B2** — integration merged + CI-green before any spend.
3. **B2 references verdict** — clears the false-pass gate → flip `attach_references` default; else references stay off. **Sean's call on the flip, on the data.**
4. **B2 → B3** — bake-off runs only after the re-baseline number is trusted.

## Operating rules (full fleet-ops — this is costed)
- **Billing:** Claude on the subscription SDK (`ANTHROPIC_API_KEY` **absent**); Gemini on the bounded `GEMINI_API_KEY`. Never route Claude through a non-Anthropic API. The Gemini key now also carries Cy's Pass-3 — watch the shared budget on any Bible-bake that overlaps.
- **Isolation:** one isolated worktree per costed run, single owner, singleton pre-flight (own-PID resolution), clean teardown — do **not** `start_new_session` a costed worker. The A-session proved the cleanest fix for a subprocess-lifecycle problem is to not have the subprocess; the Gemini-API path has no child to detach.
- **Pin by ID; verify from logs; never trust a label.** Every costed call asserts its model and logs the model it actually used. A baseline's provenance isn't trustworthy until read back from the runner's own logs.
- **Eval-gated, false-pass-first.** Any false pass on the performs segment is a worse Em — it blocks the change regardless of a precision lift. The intuitively-good change is the one to eval-gate hardest (references already proved that).
- **Labels stay locked.** Eval-case labels and bake-off labels that look wrong go to Sean for re-ratification, not a unilateral edit.
- **Maintenance:** CHANGELOG entry per change; CLAUDE.md update when the Em row's identity-signal story or the `attach_references` default changes.

## First actions for the Claude Code session
1. Task list from B1a → B1b → (gate) → B1c → (merge) → B2 → (gate) → B3.
2. Land **B1a (view-aware selection)** as its own uncosted, CI-green PR first.
3. Run **B1b (DINOv2 separation spike)** — compute-only, $0 API. Report the separation analysis and the go/no-go before integrating.
4. **Stop at each gate and report** — especially B1b go/no-go and the B2 references verdict. Do not flip the `attach_references` default without Sean on the data.
5. Hold all spend until B1 is merged and Sean greenlights the B2 re-baseline run.

---

*The portfolio artifact this produces: not "references made Em better" but the truer arc — the MLLM that started confabulating got a deterministic partner that can't, the baseline that was mismeasured for a whole program got replicated into a trustworthy band, and the decision to re-enable references was made on the data, at a gate, or not at all.*
