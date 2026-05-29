# Mascot cross-register validation + a similarity-gate blind spot

*2026-05-29, fidelity-fix session. Companion to the sean-anchor recovery evidence in this folder.*

## The fix generalizes to the pixel-art register

The visual-fidelity mechanism (commit 1: unconditional anchor injection + no-chaining + role-tag prompts) was validated on `sean-anchor` (pencil-test-colored). To confirm it generalizes, one `claude-mascot` (pixel-art-8bit) generate plate — `turnarounds/head-front.png` — was run through the **exact** `_resolve_generate_references` → `_build_nb_pro_prompt` → `invoke_nb_pro` path against live NB Pro.

**Result: recovered.** The generated head-front (`recovered-mascot-head-front.png`) is recognizably the same creature as the anchor (`mascot-anchor.png`) — the blocky orange lozenge form, two black square dot eyes, multiple stub legs, the orange palette. This is the octopus-critter, **not** the generic chibi humanoid (two arms, two legs, smiling mouth, cheek-blush) the pre-fix run produced. A minor caveat: the generated plate has some anti-aliasing on the diagonal pixel steps, which the `IR.claude-mascot.style.integer-pixel-grid-no-anti-aliasing` rule would flag at Gemini Pass-3 — a register-purity nit, not identity drift.

## The similarity gate inverted on this register — a real blind spot

The commit-2 Pass-2.5 similarity gate (PIL-perceptual tier, on a deps-free machine) scored the recovered plate **0.460** and the old drifted plate **0.571** — i.e. it ranked the *correct* plate *below* the *wrong* one. Backwards.

**Why:** the PIL tier is a global color-histogram + luma-structure metric, so it is scale/background-sensitive. The mascot anchor is a tiny creature on a mostly-white field; the recovered head-front fills the frame with orange. The white-vs-orange ratio difference swamps the identity signal. The old drifted chibi happened to share more of the anchor's white-dominated composition, so it scored higher despite being the wrong character.

For comparison, on `sean-anchor` — consistent full-figure framing on cream paper — the gate ordered correctly (recovered 0.564 vs drift 0.468).

**Takeaways:**
- The PIL tier is a useful *severe-monochrome-drift detector for consistent-framing characters*, and it is explicitly a record-not-block flag in commit 2 precisely because it is coarse.
- It is **not reliable** for tiny-subject-on-background or variable-crop registers (pixel-art/mascot). For those, the **human/visual gate is the arbiter** (and it caught the truth here).
- The **DINOv2 tier** (semantic embedding, scale/background-robust) is the real fix; the gate's method ladder already prefers it when `torch`+`transformers` are installed. Do not promote the PIL tier to a hard gate for these registers. Documented in `similarity_gate.py`'s KNOWN BLIND SPOT note.

## The transient Pass-1 stub (loud guard worked)

The first full mascot scratch re-bake stubbed at Pass-1 — and the commit-2b/2c **loud-fail guard fired** ("ERROR: Pass-1 returned a STUB envelope"), so it did not silently ship. A subsequent raw capture of the same Pass-1 call **parsed cleanly** (452s, 30.8KB, all five envelope keys), so the stub was a transient malformed Opus 4.8 emission, not a systematic parser gap. The robust parser handles the mascot output; the failure was caught loudly as designed.

**Follow-up worth considering (not done here):** have Cy *retry* the Opus Pass-1 call on a parse failure (within the existing three-call budget) instead of falling straight to the stub, so a transient malformed emission auto-recovers rather than requiring a human re-run. The loud guard makes this an optimization, not a correctness fix.
