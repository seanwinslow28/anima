# Kickoff — Eval-foundation reset: fix the ruler before measuring again

*2026-06-03. A paste-ready brief for a FRESH Claude Cowork (orient-and-decide) session. This is a deliberate step back. After a week of individually-sound eval work that kept producing "odd results" and NO-GOs, the diagnosis is that the eval **foundation** — the fixtures and the Bible they reference — is unsound, so every measurement has been noisy or vacuous. This session does NOT build another production gate. It diagnoses what went wrong, then designs a trustworthy eval foundation, with Sean authoring the human-taste artifacts only he can.*

---

## For the fresh session — read this first, then verify everything against the tree

You are resuming anima's critic/eval work after a sequence of honest-but-frustrating NO-GOs. **Do not trust labels, docs, or even this brief — the deepest lesson of this whole arc is "verify against the tree, never trust a label."** Confirm each claim below before acting on it.

**Read, in order:**
1. `PHILOSOPHY.md` — "empirical, not vibes"; the human owns taste; the critic earns its keep by proposing fixes.
2. `docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md` — the eval handbook. **Re-read §error-analysis-first, the binary/single-axis-cases rule, and class balance.** The current fixtures violate all three; this session's job is to make the fixtures match the handbook the team already wrote.
3. The arc of NO-GOs (so you don't re-run dead ends):
   - `docs/anima-test-runs/2026-06-02-em-gemini-transport-rebaseline-postmortem.md` — references-grounding regressed (confabulation); model-provenance bug.
   - `docs/2026-06-02-workstream-b-dinov2-and-rebaseline-kickoff.md` + the B postmortem — DINOv2 NO-GO (embedding sees identity, not geometry; **fixtures were contaminated**).
   - `docs/2026-06-03-sf03-proportion-gate-design.md` — the proportion-gate pivot (constrain-first at Bible-lock). Sound design; parked pending this reset.
4. `CLAUDE.md` — the Critic Stack (T1/T2/T3), the Character Bible primitive, the QA gates (HF/SF/CC), Em's current state (reference-blind by default).

## The diagnosis to verify (starting hypothesis — confirm or correct it)

Every wall this week shares **one** root cause: the eval foundation is unsound. Four specific defects, each verifiable:

1. **Contaminated fixtures.** Confirm: `ls -la evals/vision_critic/fixtures/frames/*.png` — every frame has link count 2 (hardlinked copies of source), and several `defect_*` fixtures are byte-identical (same SHA) to `characters/sean-anchor/turnarounds/*.png`. The "defect" examples ARE the reference plates. Any reference-vs-subject comparison on these is vacuous.
2. **Drifted ground truth.** Confirm: `sean-anchor`'s body turnarounds are ~4.6–5.5 heads-tall against a 1:7 target, baked into the LOCKED Bible. The gold standard is itself wrong.
3. **Stacked defects.** Confirm: `grep "defect_label:" evals/vision_critic/cases.yaml | sort | uniq -c` — most fail-cases carry compound labels (e.g. `proportion-drift+jaw-drift+eye-color-drift`). You cannot attribute a catch/miss to a single defect class.
4. **Tiny, unbalanced n.** ~30 cases, ~15 fails across ~18 mostly-singleton defect labels → ~1 case per failure mode → every per-class number is a single noisy draw (this is why the stylus case flipped pass↔fail).

**The headline:** the NO-GOs were largely the *eval set* failing, not the ideas. You can't get clean results from a dirty ruler. Fix the ruler first.

## What this session produces (no production gate this round)

A **foundation-first plan**, sequenced so no future session builds on bad data again. Specifically:

### 1. Error analysis first (with Sean, bottom-up — not top-down)
Before designing anything, look at **real generated outputs** with Sean and **open-code the failure modes that actually occur** — don't presume the taxonomy. The current defect classes were guessed top-down and then stacked. Replace them with the modes Sean actually sees and cares about, each named and singular. This is straight from the handbook the team wrote and didn't follow.

### 2. A trustworthy fixture corpus (the deliverable that unblocks everything)
Design the spec; Sean authors the images (see "What Sean does," below). Requirements:
- **Class-isolated:** each defect fixture isolates ONE failure mode. No compound labels.
- **Independent:** defect images are separate files, never copies/hardlinks of the references. (Add a CI check that fails if any fixture shares an inode/SHA with a Bible plate — so contamination can never silently return.)
- **Balanced + sufficient:** ~5–10 cases per class for non-noisy per-class estimates; a clean set that spans legitimate variation (views, expressions, beats) so "clean" is never confused with "drift."
- **Human-labeled + trusted:** Sean has looked at and ratified every label. The current labels are **suspect pending re-ratification** (they were built on contaminated fixtures) — treat them as such, bring proposed labels to Sean, do not treat the existing `cases.yaml` as locked gospel this round.

### 3. A clean Bible as gold standard
`sean-anchor`'s body turnarounds get re-baked to correct 1:7 (this is the A4 re-bake, now gated by the SF03 design's proportion check at lock). Nothing in the eval references a drifted plate again. The SF03 gate design (`docs/2026-06-03-sf03-proportion-gate-design.md`) is what the re-bake is verified through — that's where it earns its keep, at Bible-lock, not on Em's per-frame path.

### 4. Layer separation — decide what each layer owns
Stop tangling two different problems:
- **Bible-authoring QA** (deterministic, at lock): proportion (SF03), and other measurable-at-author-time properties. Tiny volume, human-affordable, can be a hard gate.
- **Per-frame critique** (Em/T2, MLLM): style/register/semantic judgments on production frames. Decide which defect classes each layer is responsible for, and stop asking Em's per-frame path to catch what belongs at Bible-lock (and vice-versa).

### 5. A sequenced foundation-first plan
Order of operations, with gates: **clean Bible → clean class-isolated fixtures + ratified labels → CI contamination guard → re-establish the Em baseline on the trustworthy set (this number replaces the contaminated 0.62 / 1.00 / 0.15 figures) → only then resume any production-gate work (SF03 build, references question, etc.).** No costed gate work resumes until the foundation is trustworthy.

## What Sean does on his end (the human-taste work only he can do)
- **Re-author a clean sean-anchor Bible** — body turnarounds at correct 1:7, that he has eyeballed and trusts. The gold standard.
- **Curate the labeled gold corpus** — look at real outputs, name the failure modes he actually sees, and assemble good/bad images where each bad one isolates a single defect, bad ≠ copy-of-good, and he has personally verified every label. Quality and structure over volume (~40–60 deliberate images beats hundreds of random ones).
- He is the ground truth. The eval labels are his taste rendered checkable — this is the anima thesis, and it is the part that makes every downstream number honest.

## Operating rules
- **This is a Cowork orient-and-decide session.** Produce the diagnosis + the foundation plan + the fixture/Bible spec. No costed builds here; hand the build to Claude Code after.
- **Plan-first, empirical-not-vibes.** The lesson of the week: build the measurement foundation before the thing it measures. Treat the current eval numbers as untrustworthy until re-established on a clean set.
- **Verify against the tree; never trust a label** (model IDs, fixture provenance, Bible correctness — read it back, don't assume).
- **Labels are Sean's** — proposed labels and any re-ratification of the existing `cases.yaml` come to Sean; do not lock them unilaterally.
- **Billing/worktree discipline stands** (for any later costed work): Claude on the subscription SDK (`ANTHROPIC_API_KEY` absent), Gemini on the bounded API key, isolated worktree, single owner, clean teardown.
- **Maintenance conventions:** CHANGELOG entry per change; CLAUDE.md update when the eval foundation or the layer-ownership map changes.

## First actions for the fresh session
1. Set up a task list.
2. Verify the four-defect diagnosis against the tree (inode/SHA on fixtures, head-count on the Bible plates, label compounding in `cases.yaml`). Report what you confirm or correct **before** designing.
3. Run error-analysis-first with Sean on real outputs — open-code the actual failure modes.
4. Draft the fixture corpus spec + the clean-Bible gold-standard plan + the layer-ownership map + the sequenced foundation-first plan.
5. Stop and review with Sean before any build or any spend.

---

*The reframe to carry into the room: this week's NO-GOs weren't wasted — they were the eval discipline working, killing bad ideas cheaply and surfacing a real data-integrity bug. The mistake wasn't the ideas; it was measuring them with a contaminated ruler. Fix the ruler, and the pipeline stops producing odd results — because for the first time the numbers will be about the critic, not about the fixtures.*
