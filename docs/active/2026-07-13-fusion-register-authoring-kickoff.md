# Kickoff — author the FUSION style register (fresh-session prompt)

*Paste the block below into a fresh Claude Code session in the `anima` repo. It runs the [style-register authoring playbook](../architecture/style-register-authoring-playbook.md) (R → S → B) for the fusion look Sean locked by eye on 2026-07-13 (taste brainstorm + costed spike + Seedance motion test — see [`2026-07-13-signature-style-taste-and-blend-brainstorm.md`](2026-07-13-signature-style-taste-and-blend-brainstorm.md) §6).*

---

## The pasteable kickoff prompt

> You are authoring a NEW closed style register for the anima project — the **FUSION** look Sean selected by eye (a costed Higgsfield image spike + a Seedance 2.0 motion test, 2026-07-13; his eye the sole arbiter). This is the active thread of the outward-turn / style-register-expansion workstream. **Read the source of truth before anything else and follow it exactly.**
>
> **Read first (in order):**
> 1. [`docs/architecture/style-register-authoring-playbook.md`](../architecture/style-register-authoring-playbook.md) — the canonical R→S→B workflow. THIS GOVERNS THE BUILD.
> 2. [`docs/active/2026-07-13-signature-style-taste-and-blend-brainstorm.md`](2026-07-13-signature-style-taste-and-blend-brainstorm.md) — the taste profile (§1), the decision (§6), and the un-explored lanes (§7).
> 3. [`docs/architecture/prompt-style-neutrality-doctrine.md`](../architecture/prompt-style-neutrality-doctrine.md) — genericization + the neutrality gate.
> 4. The two existing gpt-image registers as the closest precedent: `registers/primal-sketch-grit/` and `registers/samurai-jack-s5/` (+ `docs/active/2026-07-11-samurai-jack-s5-register-design.md` as the worked drill).
>
> **The look to author (from Sean's eye — the ratified target):**
> Flat, boldly hand-drawn 2D cartoon characters with a **living, boiling, wobbling hand-inked outline and flat cel colors** (no rendered volume on the figures), set inside a richly **hand-PAINTED** gritty children's-storybook world: cross-hatched dry-brush weathered urban surfaces, a muted earthy palette (ochre, brick-red, sage, cream), folk-decorative flourishes, soft gouache washes, warm golden-hour grime. **Two media in one frame** — the flat graphic cast pops against the painterly-gritty painted environment. Warm, hand-made, tactile, grounded; never glossy/3D/anime.
> - **Ratified hero candidate (Sean's pick):** `runs/2026-07-13-signature-blend-spike/round2/out/FU1_fusion.png` (gpt_image_2). **Motion proof (survived Seedance):** `runs/2026-07-13-signature-blend-spike/round2/seedance/out/FU1.mp4`. The generating prompt is `runs/2026-07-13-signature-blend-spike/round2/prompts/FU1_fusion_gpt.txt`.
>
> **Run the playbook, but note what's already done vs. still open:**
> - **Step R (deep research) — DO THIS.** Ground the craft: how a flat lineless/boiling-line cast reads *against* a painted world (the edge/figure-ground logic that keeps the two media legible), the boiling-line convention, the painted-grit background craft, and the **negative-control table** distinguishing this register from its neighbors — vs **Collage Real** (same flat cast but on a *photographic* world, not painted), vs **Gritty Storybook** (a *unified* painterly medium, cast and world the same — the banked sibling), vs `primal-sketch-grit` (gritty ink-over-color, unified), vs `samurai-jack-s5` (flat-minimal, no world-grit). Produce the four wire-ready outputs (draft RegisterSpec, the Cy Example block, the refs policy + bibliography, the transport record). End at Human Checkpoint 1 (Sean ratifies research).
> - **Resolve the ONE load-bearing design question in Step R:** is this **one `RegisterSpec`** whose `style_token` describes the whole fused frame (flat cast + painted world — which is how FU1 was generated, as a single gpt-image), **or** a character register **plus a compositing/staging convention** (the "register + recipe" honest-scope note from the brainstorm §3 Concept A)? Recommend one, with reasoning, at Checkpoint 1. Default lean: one RegisterSpec (FU1 proves the whole look renders from a single prompt), with the compositing-a-Bible-character-into-it question flagged as downstream.
> - **Step S (look-spike + hero lock) — LIGHT / confirm.** The look is already chosen by eye and motion-tested. Formally lock the hero: copy `FU1_fusion.png` bytes unchanged into `registers/{slug}/refs/{slug}-hero.png` + write `refs/README.md` provenance (engine gpt_image_2, date, exact prompt, dimensions, Sean's reason keyed to the traits, + the motion-proof note). If Step R refines the vocabulary, an optional 1–2 image confirmation spike is Sean's call (costed, his eye). Human Checkpoint 2 (Sean confirms the hero reads as the register, cold). **Commit no third-party frames** — only Sean's own spike output.
> - **Step B (authoring build) — the $0 TDD drill.** Isolated git worktree off the current branch (fleet-ops: subscription billing, never `ANTHROPIC_API_KEY`, clean teardown). TDD red→green. The full touch-point list is Task 1–6 in the playbook: `tests/test_{slug}.py` (RED first) → the RegisterSpec appended last → the stub-order snapshot row → Cy Example block + enumeration lines + "N examples" prose + template comment + doctrine vocab line → state-of-record docs (backlog, CLAUDE.md, AGENTS.md, CHANGELOG, research cross-links) → the verification gate. **Stop at first green for Sean's review; only Sean merges.**
>
> **Transport (record honestly):** the hero was generated with **gpt-image (`gpt_image_2`)**, so `generation_model = GPT_IMAGE` is the honest record — **unwired, fails loud** via the existing `SUPPORTED_IMAGE_MODELS` guard (no new guard code; same as primal/samurai), `final_model = NB_PRO`. During Step R/S, **spike whether NB2 can carry the fusion** (the ladder says NB2 first) — round-2 tested only gpt for FU1; if NB2 holds the flat-cast-on-painted-world split, record NB2 instead (it's wired, buildable now). **Wiring a gpt-image runner + across-edit identity validation stays DEFERRED and gated on a separate, costed, Sean-greenlit build** — the $0 authoring drill does not wire it. (Note: this would be the *third* gpt-image register, and the AI-guru cat series is a real potential consumer — so wiring gpt-image is increasingly justified, but still its own greenlit build.)
>
> **Working slug (finalize at Step R — attribute-only, no franchise/creator/character name):** proposed `flat-cast-painted-world` (alternatives: `flat-cel-painted-grit`, `painted-world-collage`). Whatever wins must pass the genericization test exactly as the other slugs do.
>
> **Named consumer / justification:** a committed signature look Sean will use; first *potential* consumer is the **AI-guru "trash cat" episode idea** (brainstorm §6) — adoption not locked (the AI-guru pilot's authored register is `90s-nicktoon-grossout`). Author it as a capability with this as the candidate first use.
>
> **Guards (must hold):** the two frozen md5 files unchanged (`evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4`; `pipeline/agents/prompts/sean-screenwriting-voice.md` = `945af824fa53b948a18ac6bf206d67ef`); the six legacy registers byte-identical; `SUPPORTED_IMAGE_MODELS` and `nb_pro_runner.py`'s guard untouched; genericization attribute-only; both pytest dirs green; run `superpowers:verification-before-completion` before claiming done. **$0 / stub-green for the authoring drill** — the only costed step is an optional Step-S confirmation spike (Sean-gated) or the deferred transport wiring.
>
> Start by reading the four source docs, then confirm your understanding of the fusion look + the one open design question (single RegisterSpec vs register+recipe) with Sean before Step R research.

---

## Context notes for whoever runs this (not part of the paste)

- **This is a partially-pre-run playbook:** the taste is chosen and the look is eye-ratified + motion-tested, so Step R is the real work; Step S is mostly a formal hero-lock; Step B is the standard drill. Don't re-litigate the look — Sean picked it.
- **The banked siblings** (Gritty Storybook GS1/GS2, Collage Real, Riso, + the six un-spiked candidates) live in the brainstorm doc §6/§7 and the [register backlog](2026-07-04-register-backlog-and-transport-findings.md) — do not author them here; they get their own sessions.
- **Spike artifacts** are gitignored under `runs/2026-07-13-signature-blend-spike/` (local only). The hero + provenance become the register's committed evidence at Step S.
