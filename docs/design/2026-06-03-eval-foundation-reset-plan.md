# Eval-Foundation Reset — Diagnosis + Foundation-First Plan

*2026-06-03. **Orient-and-decide artifact — NOT a build.** A decision document for Sean's review before any code or spend. Produced after a week of individually-sound eval work that kept returning NO-GOs. The thesis of this reset: the eval foundation (the fixtures and the Bible they reference) is unsound, so every measurement has been noisy or vacuous. Fix the ruler before measuring again.*

---

## 1. The diagnosis, verified against the tree

The starting hypothesis named four defects. All four are **confirmed**; two are **worse** than stated. Every claim below was read back from the actual tree, not trusted from a label.

### Defect 1 — Contaminated fixtures (confirmed, broader than claimed)

The brief said "several `defect_*` fixtures are byte-identical to turnarounds." The reality is broader: **19 of 23 fixtures in `evals/vision_critic/fixtures/frames/` are byte-identical (SHA-256-matched) copies of Bible or source plates**, and the contamination spans **all three label classes**, not just defects:

- **`clean_*`** — `clean_neutral`, `clean_surprised`, `clean_contemplative`, `clean_head_back`, `clean_head_profile_left`, `clean_head_turn_02`, `clean_head_turn_06` are exact copies of `sean-anchor` expression/turnaround plates. "Clean" literally means *"is the reference plate."*
- **`borderline_*`** — `borderline_focused`, `borderline_head_profile_right`, `borderline_head_turn_03`, `borderline_stylus_prop` are exact copies of Bible plates.
- **`defect_*`** — `defect_body_3quarter/back/profile_left/profile_right` are exact copies of the (drifted) body turnarounds; `defect_head_turn_01/09` and `defect_walk_cycle_source` are exact copies of source frames.
- **Only 4 fixtures are genuinely independent:** `clean_F06`, `clean_F13`, `clean_F31` (real Act 1 keyframes) and `defect_F13_stylus_hand`, `defect_F31_scale` (real defect frames).

**Mechanism correction (verify-don't-trust):** the fixtures are byte-identical **copies** (distinct inode from the Bible plate), not hardlinks *to* the Bible. Each carries link-count 2, but the hardlink partner lives outside the repo tree. The substance — *the eval examples ARE the reference plates* — holds and is amplified.

**Why this is the root cause of the reference-grounding NO-GO.** When Em is given references on a "clean" case, she is comparing a plate to *itself or its sibling plates*. That is a confabulation trap by construction — it is precisely the false-pass 0.00→0.15 regression that flag-gated references off on 2026-06-02. The regression was the fixtures, not the idea.

### Defect 2 — Drifted ground truth (confirmed, worse on the low end)

`sean-anchor`'s body turnarounds are baked into the **locked** Bible at **~1:4–1:5.3 heads-tall against a 1:7 target**. This is corroborated two independent ways: the SF03 design doc's measurement, and real Cy `gemini_verdict` reasoning that measures them in pixels ("roughly 1:4 to 1:4.5, stylized/chibi-like"). The gold standard is itself wrong, and nothing in the pipeline caught it — the only proportion-adjacent signal (Cy's Pass-2.5 similarity gate) is record-only and measures identity recognizability, not geometry.

### Defect 3 — Stacked defects (confirmed)

Five fail-cases in `cases.yaml` carry **compound** labels: `style-simplification+hair-drift+jaw-drift`, `proportion-drift+missing-prop+construction-line-loss`, `proportion-drift+missing-prop`, `proportion-drift+jaw-drift+eye-color-drift`, `proportion-drift+jaw-drift+construction-line-loss`. A catch or miss on these cannot be attributed to a single failure mode — they violate the handbook's single-axis-case rule.

### Defect 4 — Tiny, unbalanced n (confirmed)

29 cases total: **15 fail / 10 pass / 4 borderline**, across ~18 mostly-singleton defect labels. ~1 case per failure mode → every per-class number is a single noisy draw (which is why the stylus case flipped pass↔fail between runs). And critically: the `cases.yaml` header records a Sean ratification on 2026-06-01 — but that ratification happened **against this contaminated set**, so it is suspect and must be re-established, not trusted.

**Headline:** the week's NO-GOs were the eval discipline working — killing bad ideas cheaply and surfacing a real data-integrity bug. The mistake was measuring good ideas with a contaminated ruler. The contaminated baseline figures (precision 0.62 / recall 1.00 / false_pass 0.15) are **untrustworthy** and are retired by this reset.

---

## 2. Error-analysis-first — the open-coded taxonomy

Per the handbook (error-analysis-first, bottom-up), the failure-mode taxonomy is derived from **74 real `plate_verdicts.jsonl` records** (30 fail / 19 borderline / 25 pass) carrying pixel-grounded reasoning — *not* guessed top-down. The modes that actually recur, open-coded:

proportion (head-to-body off 1:7 → chibi) · palette (color violation) · construction-lines (missing beneath final) · hair-silhouette (cowlick/tousle drift) · jaw-geometry (rounded vs angular) · view-correctness (¾ drawn as profile) · anatomy-count (mascot ear/arm nubs) · shading-register · eye/brow-features.

**Sean's ratified scope (2026-06-03).** The fixture corpus isolates **six single-axis classes**:

1. **proportion** — head-to-body ratio (1:7 target; mascot has its own box spec)
2. **palette** — color-value violations against the locked palette
3. **view-correctness** — the labeled view matches the drawn view (¾ is ¾, not profile)
4. **anatomy-count** — discrete countable features (mascot ear/arm nubs); per-character
5. **construction-lines** — construction lines visible beneath the final render
6. **shading-register** — correct shading register for the pencil-test aesthetic

**Deliberately deferred this round (reversible):** the per-identity-feature modes — **hair-silhouette, jaw-geometry, eye/brow-features**. These recur in the verdicts and matter, but Sean scoped them out of the first clean corpus to keep it tight. Recorded as a conscious deferral with a promotion trigger (reinstate once the six-class corpus is clean and re-baselined), not a gap.

---

## 3. Layer-ownership map

The reset stops tangling two different problems. Sean's locked split (2026-06-03): **geometry → Bible-lock (deterministic), style/identity → Em (MLLM).**

| Failure class | Owner | Layer | Why it lives here |
|---|---|---|---|
| proportion | **Bible-lock** | deterministic, at author-time | Originates at Bible authoring; measurable against a known armature (SF03). Tiny volume, human-affordable, can be a hard gate. |
| view-correctness | **Bible-lock** | deterministic, at author-time | The declared view is known metadata; the drawn view is checkable against it at lock. |
| anatomy-count | **Bible-lock** | deterministic, at author-time | Discrete countable features; per-character spec. Checkable at lock where volume is tiny. |
| palette | **Em / T2** | MLLM, per production frame | Color-register judgment on arbitrary frames; cheap for a vision model, awkward to hard-code per scene. |
| construction-lines | **Em / T2** | MLLM, per production frame | Style-integrity judgment on production output. |
| shading-register | **Em / T2** | MLLM, per production frame | Aesthetic-register judgment on production output. |

**The principle:** once the Bible's turnarounds are clean, downstream frames inherit correct geometry *because they are generated against the Bible*. The geometry gate pays off at the source (tiny volume); the style/identity judgments belong on the per-frame MLLM path where the volume and ambiguity live. We stop asking Em to catch proportion (she structurally can't, per the DINOv2 NO-GO — embeddings see identity, not geometry), and stop asking the deterministic lock to judge shading register.

The **motion_proper** segment (6 intentionally-red contact-sheet cases) is **out of scope** for this reset — it is a separate, defensible ships-red design (a still contact sheet structurally can't see motion-proper) and is not contaminated the same way. It carries forward unchanged.

---

## 4. Clean Bible — the gold standard (A4 re-bake)

Nothing in the eval may reference a drifted plate again. `sean-anchor`'s body turnarounds get **re-baked to a correct 1:7** and **re-locked through the SF03 proportion gate** — turning the A4 re-bake from "redo and hope" into "redo until the gate passes." This is where the SF03 design (`docs/2026-06-03-sf03-proportion-gate-design.md`, currently parked in its worktree) earns its keep: at Bible-lock, not on Em's per-frame path.

Sequencing note: the SF03 gate has **one make-or-break feasibility question** (does NB2 honor a provided armature underlay — Approach A?) with a guaranteed human-in-the-loop fallback (Approach B, affordable at the tiny lock-time volume). The clean Bible does not block on Approach A succeeding — Approach B can produce the re-locked 1:7 plates either way. The re-baked plates become the new gold standard the fixture corpus references.

**Sean authors this.** The re-baked body turnarounds at correct 1:7 are a human-taste artifact — Sean eyeballs and trusts them. The pipeline verifies them through SF03; Sean ratifies them.

---

## 5. Fixture corpus spec

The deliverable that unblocks everything. Design here; **Sean authors the images.**

### Requirements

- **Class-isolated.** Each defect fixture isolates exactly **one** of the six modes. No compound labels. A `proportion` fixture drifts proportion *and nothing else* — same palette, view, construction, shading as a clean plate.
- **Independent.** Every defect image is a **separate file**, never a copy/hardlink/SHA-match of a reference or Bible plate. The clean set is also independent — clean ≠ "is the reference plate."
- **Balanced + sufficient.** **~5–10 cases per class** for non-noisy per-class estimates. A clean set that spans legitimate variation — multiple views, expressions, beats — so "clean" is never confused with "drift." Target corpus ~40–60 deliberate images (Sean's quality-over-volume rule).
- **Human-labeled + trusted.** Sean has looked at and ratified every label. The existing `cases.yaml` labels are treated as **provisional** this round (built on contaminated fixtures); proposed labels come to Sean, nothing is locked unilaterally.

### CI contamination guard (so this can never silently return)

A test that **fails CI** if any fixture under `evals/vision_critic/fixtures/` either (a) shares a SHA-256 with any plate under `characters/*/` or `images/`, or (b) shares an inode with a Bible plate. This is cheap (the diagnosis above is exactly this check, run once) and it converts "don't contaminate the fixtures" from a convention into an enforced invariant. Lands alongside the new corpus.

### Schema (per case)

Carry forward the useful fields from today's `cases.yaml` — `name`, `description`, `checkpoint`, `character_id`, `input`, `beat_description`, `case_class`, `expected_verdict`, `expected_cites`, `sean_note` — with two hard rules: `defect_label` is **exactly one** of the six classes or `clean`; and `input` must pass the contamination guard.

---

## 6. The sequenced foundation-first plan

Ordered so no future session builds on bad data again. Each arrow is a gate.

```
G1  Clean Bible          Re-bake sean-anchor body turnarounds → 1:7, re-locked through SF03.
        │                Gold standard is correct before anything references it.
        ▼
G2  Clean fixtures       Author ~40–60 class-isolated, independent images (6 classes,
        │                ~5–10 each) + a clean set spanning legitimate variation.
        ▼
G3  Ratified labels      Sean reviews and ratifies every label. cases.yaml rebuilt;
        │                old labels discarded, not trusted.
        ▼
G4  CI contamination     Land the SHA/inode guard. Contamination cannot silently return.
        │  guard
        ▼
G5  Re-baseline Em       Re-run the Em baseline on the trustworthy set. THIS number
        │                replaces the contaminated 0.62 / 1.00 / 0.15 figures.
        ▼
G6  Resume gate work     Only now: SF03 build (Approach A probe → A or B), the references
                         question (re-test on clean fixtures), DINOv2 if still wanted.
```

**No costed gate work resumes until G5.** The references question, the DINOv2 backstop, and the SF03 *build* are all downstream of a trustworthy foundation. Re-running them against the current fixtures would reproduce the same noise.

---

## 7. What Sean owns vs. what the pipeline owns

This is the anima thesis made concrete: **the eval labels are Sean's taste rendered checkable.**

- **Sean (human-taste, only he can do):** re-author the clean 1:7 Bible he trusts; curate the labeled gold corpus (name the modes he sees, assemble good/bad images where each bad one isolates one defect and bad ≠ copy-of-good); ratify every label. He is the ground truth.
- **Pipeline (cheap, parallel, structured):** the contamination guard, the SF03 measurement, the re-baseline harness, the corpus scaffolding. It proposes and verifies; it does not decide taste.

---

## 8. Operating discipline (for the build that follows)

- This session is **orient-and-decide only**: diagnosis + plan + spec. No costed builds; hand the build to Claude Code after Sean's review.
- **Verify against the tree; never trust a label** — model IDs, fixture provenance, Bible correctness. Read it back.
- **Labels are Sean's** — proposed labels and any re-ratification come to him, not locked unilaterally.
- For any later costed work: Claude on the subscription SDK (`ANTHROPIC_API_KEY` absent), Gemini on the bounded API key, isolated worktree, single owner, clean teardown.
- Maintenance: CHANGELOG entry per change; CLAUDE.md update when the eval foundation or layer-ownership map changes (the layer map in §3 is the change to land in CLAUDE.md once Sean approves this doc).

---

## 9. Open questions for Sean (before handing to build)

1. **Re-bake scope** — body turnarounds only, or re-verify the head turnarounds + expressions through a proportion lens too while re-baking? (The verdicts show head plates with their own drift — view-mislabeling, jaw, hair.)
2. **Mascot proportion spec** — `claude-mascot` is a box-creature; its anatomy-count + box-ratio spec needs declaring before its fixtures can be class-isolated. In scope now, or sean-anchor-first?
3. **Deferred identity modes** — confirm hair/jaw/eye stay out of the first corpus (reversible), or fold one in now if it's cheap to isolate.
4. **Corpus authoring path** — does Sean hand-draw the defect fixtures, generate-then-curate via Cy, or a mix? (Affects how the build session is scaffolded.)
