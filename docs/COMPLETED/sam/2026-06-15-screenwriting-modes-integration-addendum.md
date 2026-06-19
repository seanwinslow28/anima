# Integration Addendum — `screenwriting-modes` skill → Sam & Bea

*Dated 2026-06-15. Updates the [Sam + Bea brainstorm](2026-06-12-sam-bea-phase3-brainstorm.md) and the [Sam build plan](2026-06-12-sam-scriptwriter-build-plan.md) / [kickoff](2026-06-12-sam-scriptwriter-kickoff.md). $0 — planning + a vendored prompt artifact, no code, no model spend.*

---

## Why this addendum exists

The Sam/Bea design (2026-06-12) was written **before** Sean's screenwriting voice skill existed. It therefore deferred the voice layer: brainstorm §8 lists "Full `writing-voice-modes` calibration" as deferred ("lives in another repo"), and §5 + the build-plan file map call for Sam's persona preamble to embed a **condensed "Sean's register" note**.

That skill now exists. Sean completed the full pipeline (deep research → compile → interview + 5 writing exercises → build) and shipped **`screenwriting-modes`** (the screen twin of `writing-voice-modes`) plus a refit `script-writing` skill, both in `code-brain/.claude/skills/`. The calibration was built *specifically* so Sam and Bea could write in his voice.

**The correction:** the condensed-note plan is now both unnecessary and wrong. The skill's own **anti-distillation contract** states the thesis plainly — *voice does not survive distillation; exemplars drive, mechanics annotate* — and a condensed bullet note is exactly the failure it warns against. It also *is* the build plan's named #1 Sam failure mode ("surface pastiche vs. real stylistic-mechanism modeling"). So Sam vendors the **full instrument**, not a note. Sean ratified this (full-fidelity vendor) on 2026-06-15.

This addendum supersedes: brainstorm §8 row 1 (the condensed-note deferral), §5 final bullet ("v1 embeds a condensed register note"), and the build-plan / kickoff file-map + build-order references to "a condensed 'Sean's register' note."

---

## The integration mechanism (grounded in the real code)

anima agents load `pipeline/agents/prompts/anima-standing-context.md` + a role addendum (e.g. `maya-planner-context.md` 11KB, `cy-character-designer-context.md` 29KB). The shared standing context **already names** "Sam (the scriptwriter, Opus 4.7 with screenwriting-modes)" — the seat is reserved.

Because the skill lives in **a different repo** (`code-brain`), and anima's discipline is to stay self-contained and stub-green, integration is a **cross-repo vendor** (a tracked copy with provenance), not a runtime read across repos:

- **New shared prompt file:** `pipeline/agents/prompts/sean-screenwriting-voice.md` — vendored **verbatim** from [`docs/2026-06-15-sam-bea-screenwriting-voice-context.md`](../../design/2026-06-15-sam-bea-screenwriting-voice-context.md) (authored in this session, ready to drop in).
- **Loaded by both** `sam-scriptwriter-context.md` and (when Bea lands) `bea-storyboard-context.md` — same pattern as both loading `anima-standing-context.md`. DRY: one voice instrument, two consumers.
- **Provenance header** records the source path + skill version + a re-sync trigger (the skill will evolve — e.g. the ticketed Bukowski 6th-author add). Canonical source of truth stays the code-brain skill; this is a tracked copy.

A formal sync script is a deferred nicety; a provenance header + a re-sync line in the ticket backlog is enough for v1.

---

## The six integration points

### 1. Sam's voice context — full-fidelity vendor (replaces the condensed note)
Vendor `sean-screenwriting-voice.md` (the §8 verbatim samples, the moves table, the WHAT + taste layers, the anti-distillation contract, the anti-patterns). `sam-scriptwriter-context.md` loads it after `anima-standing-context.md`. Context size is a non-issue: Sam is once-per-piece Opus, and Cy's context is already 29KB. **Build-order step 3 of the kickoff changes** from "loads … a condensed 'Sean's register' note" to "loads `anima-standing-context.md` + `sean-screenwriting-voice.md` (the full vendored voice instrument)."

### 2. The anti-patterns become Sam's eval material (enriches the deferred eval scope)
The build plan correctly defers the **pairwise-preference** harness (the eval handbook: LLM judges are weak/self-preferring on creative quality). But the skill's anti-patterns (§7) + the anti-distillation contract are near-**binary, ships-red checks** that don't need a quality judge:

- theme stated aloud in narration → red
- a recycled prop / hardcoded specific from the doc's example bank → red
- a naked mid-scene tender pivot (un-armored, un-punished sincerity) → red
- clean Pixar catharsis (Want resolved + world fixed + theme spoken) → red
- cheese/pun in the narrator's own voice (not diegetic, not punished) → red

Seed `evals/scriptwriter/cases.yaml` with a few of these as ships-red negatives alongside the Spark-beats positive case. This stays within the build plan's "scaffold + a few real cases" scope — it just makes the cases sharper than beat-coverage alone.

**Ready-made seed material:** the 2026-06-15 voice dry-run produced a Sean-ratified positive case ("Figgy Pudding") and two extracted ships-red negatives (SR-1 narrator-grade meta-quip in a character's mouth; SR-2 register-contrast collapse / two-clever-people) — captured build-ready in [`docs/anima-test-runs/2026-06-15-screenwriting-voice-dry-run-and-eval-seed.md`](../../anima-test-runs/2026-06-15-screenwriting-voice-dry-run-and-eval-seed.md). The build session lifts these into `cases.yaml` (the Figgy Pudding positive is *additive to* the Spark-beats seed — voice vs. plumbing — not a replacement; SR-2 is the by-ear case a deterministic check under-catches).

### 3. Structural patterns flow to the beat sheet (script-writing layer)
The refit `script-writing` skill added short-form structural spines — **therefore/but, want-engine, kishotenketsu, trope-autopsy** — which are ORDER-layer and inform Sam's `beats.json` shape (and arguably Maya's plan). **Declare-then-Puncture** is the structural+voice hybrid: it should surface as an actual beat shape, not just a line-level move. No code change needed; this is guidance for Sam's authoring prompt and for how the deterministic structural pass reads "arc presence."

### 4. The Sam→Bea seam is now concrete: the Loaded Object
The brainstorm wanted a real handoff definition beyond "they collaborate." The calibration gives it: **the Room-as-Biography / Loaded-Object move is the seam.** Sam writes the loaded object into a beat's `intent`/`notes`; Bea boards it as the shot. §8 Sample 4 (the wedding photo that shifts and falls *after* the character leaves) is the canonical specimen. This also defines a candidate for Bea's **Opus-escalation-on-conflict** trigger: if a beat's emotional payload rides on a loaded object and Bea can't realize it as a fixed-camera shot, that's a script↔board conflict worth escalating.

### 5. Bea's few-shot seeds (when Bea is built)
Bea's hard part — the per-shot `prompt` in pencil-test register — is seeded by the skill's **visual moves** (Room-as-Biography, Loaded Object, Haptic Visuality, Metaphor-Compression-in-an-empty-frame) and the script-mining report's **action-line bank** (§2). `bea-storyboard-context.md` loads the same `sean-screenwriting-voice.md`; its "How this maps to your job" section already carries Bea's slice. Headline Bea metric stays **revision count**.

> **Build-time gap to close for Bea (not Sam):** the vendored `sean-screenwriting-voice.md` carries the §8 *dialogue-heavy* samples, which are right for Sam. Bea needs *prose-action* exemplars — the **action-line bank (§2 of `2026-06-04-script-mining-report.md`)**: "a woman covered in vomit stains and regret", the dying-mom's-room-as-biography paragraph, the buried-rotten-beat montage, etc. That bank is **not** in the vendored file today (it lives only in the canonical code-brain skill's references). When Bea is built, fold the action-line bank into the shared voice file (or a small `bea-storyboard-context.md` addendum) so Bea has prose-action few-shot, not just dialogue samples. This is a Bea-build task — it does **not** affect Sam or the Sam dry-run.

### 6. The animation-pipeline crossover (already ticketed)
The Miyazaki/visual findings feed the `animation-pipeline` skill too (object-economy, room-as-biography, the wordless-ache-via-object door, plus the "Sean converts stillness to an errand — coach the contemplative hold" note). Ticketed in code-brain `vault/00_inbox/tickets.md` (2026-06-15). Bea's board work and the animation-pipeline skill share this visual vocabulary — keep them consistent.

---

## What changes in the existing docs

| Doc | Change |
|-----|--------|
| `2026-06-12-sam-bea-phase3-brainstorm.md` | §8 row 1 (condensed-note deferral) and §5 final bullet are **superseded** — full vendor now. Banner pointer added at top. |
| `2026-06-12-sam-scriptwriter-build-plan.md` | File-map row for `sam-scriptwriter-context.md` now loads `sean-screenwriting-voice.md` (full vendor). Eval-scaffold step gains the ships-red anti-pattern cases. Banner pointer added. |
| `2026-06-12-sam-scriptwriter-kickoff.md` | Build-order step 3 updated (full vendor, not condensed note). Banner pointer added so the paste-block can't build the wrong thing. |

The four locked forks (brainstorm §6), the `beats.py` contract, the single-call + deterministic-structural-pass design, the TDD/$0/stub-green discipline, and the Sam-first sequencing are **all unchanged**. This addendum only swaps the voice layer from "condensed note (deferred full)" to "full vendor (now)," and adds the eval/Bea/seam guidance that the skill makes possible.

---

## For the next anima build session (what to actually do)

1. Vendor `docs/2026-06-15-sam-bea-screenwriting-voice-context.md` → `pipeline/agents/prompts/sean-screenwriting-voice.md` (verbatim; keep the provenance header).
2. `sam-scriptwriter-context.md` loads `anima-standing-context.md` + `sean-screenwriting-voice.md` (drop the condensed-note plan).
3. Seed `evals/scriptwriter/cases.yaml` with the Spark-beats positive case **plus** 2–3 ships-red anti-pattern negatives from integration point 2.
4. Everything else per the existing build plan / kickoff (TDD, stub-green, $0, isolated worktree, the md5 guard on `evals/vision_critic/`).

The costed validation run and Bea's build remain parked exactly as planned.
