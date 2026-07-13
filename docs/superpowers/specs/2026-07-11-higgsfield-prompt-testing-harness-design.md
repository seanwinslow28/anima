# Design — Higgsfield prompt-testing harness (image gen / image edit / video)

**Date:** 2026-07-11 · **Status:** DESIGN (Sean-approved; refined) · **Execution surface:** run inside **Claude Code**, all generation through the **Higgsfield CLI** (not the MCP) — this Cowork session writes the spec + plan; a Claude Code session executes them. · **Operating model:** Claude runs every generation; Sean makes every taste call (the runbook's Engine Truth). · **Billing:** Higgsfield subscription credits (image + video share one pool); no `ANTHROPIC_API_KEY`, no paid Gemini/OpenAI API. · **Budget:** ~300 credits, block-gated.

---

## 0. Goal (one sentence)

Spend a bounded pool of Higgsfield credits to **prove, with side-by-side visual evidence, where over-prompting helps vs hurts** across image generation, image editing, and video — and to produce three durable artifacts (a reusable test harness, register-clause updates for `samurai-jack-s5`, and a prompt-writing decision-card skill) — using the GRANDMASTER kid-samurai character as the single subject.

**What this is NOT:** a from-scratch discovery of prompt rules (anima already has strong doctrine — see §1); a costed GRANDMASTER production run; wiring a gpt-image runner; authoring the `samurai-jack-s5` register into `pipeline/registers.py` (that build is a separate, already-planned $0 drill).

---

## 1. Premise — anima already has the rules; we are proving and extending them

anima's documented prompt doctrine (distilled from `docs/research/2026-05-30-nb2-editing-character-consistency-template.md`, `prompts/seedance-template-v4.md`, the Bea field reports, and the style-neutrality doctrine) already says exactly what Sean's instinct says:

- **Image edit (reference-based):** *the reference carries identity; the text carries only the change; the two compete.* Terse + strong reference beats verbose prose. One variable per edit. Enumerated identity-lock. Role-tag every reference. Never chain — re-anchor to the original. Explicit negatives are load-bearing; the anti-text clause is mandatory.
- **Image gen (from scratch):** detail helps — there is no reference to compete with. Let specific objects do characterization; style token is descriptive, never a brand.
- **Video (Seedance):** 80–100 words (hard cap 100); `<30` hallucinates, `>150` collapses. Do not re-describe the subject (the anchor frames carry it). **No in-prompt negation ever** (Seedance has no negative-prompt support — the opposite of the NB2 image path). Genre anchor leads; banned-words list; single camera line; start+end interpolation is the strongest consistency tool.

So the value here is **not** the rules. It is:
1. **Visual proof** — a picture of the ladder that shows Rung 4 degrading, so the doctrine stops being a claim.
2. **The undocumented edge — compositing.** anima has *no* documented doctrine for editing a character **into a pre-made background / frame** (Sean's hardest named pain, visible in `registers/samurai-jack-s5/refs/chatgpt/kid-samurai-scene-{before,after}-*.png`). This block generates anima's first compositing doctrine.
3. **A bonus deliverable — the `samurai-jack-s5` hero lock.** That register is a CANDIDATE; its look-spike (Human Checkpoint 2) is pending. Block A's from-scratch ladder doubles as the cross-engine spike and can lock the one hero frame the register build is waiting on.

---

## 2. The method — the prompt ladder (one controlled variable)

For every test, hold **subject, references, and target-change fixed**; vary **only prompt verbosity** across rungs; generate the whole ladder in one sitting; Sean's eye ranks the outputs. This is a controlled A/B, not free-form iteration.

The four canonical rungs (adapt per surface):

| Rung | Name | Shape |
|---|---|---|
| **1** | Terse | one action verb + one variable. "Place the boy from Image 1 into Image 2." |
| **2** | Anchored-terse | + enumerated identity-lock + role-tags + anti-text. "…match his face, hair, palette exactly; Image 2 is the background only — keep its light and color; do not add text." |
| **3** | Medium | + one sentence of integration (scale / where he stands / light direction). |
| **4** | Over-prompted | the kitchen-sink literary prose Sean would normally write. |

**Predicted result** (from doctrine): Rung 2 wins on edits/compositing, Rung 4 visibly degrades identity; on generation the ranking inverts (more detail helps). The point is the *picture*, not the prediction.

**Rejected alternatives:** free-form iteration (no controlled variable, not reusable); a full Latin-square parameter sweep across word-count × reference-count × verbosity (≈3× the credits for marginal extra signal). The ladder is the cheap decisive middle.

**Scoring.** One row per rung in a per-block scoring sheet: `identity_hold` (1–5), `change_landed` (Y/N), `style_match` (1–5), `artifacts` (text/labels/melt/bleed), `Sean_rank`, one-line note. The sheet *is* the finding.

---

## 3. The matrix — four blocks, sequenced, block-gated

Run **one block at a time**. After each, Sean reviews the contact sheet + scoring sheet and greenlights the next. If a block (compositing, most likely) consumes more than its share, we **stop and bank the finding** rather than burn the remaining budget.

| # | Surface | Question under test | Rungs | Est. credits | Doubles as |
|---|---|---|---|---|---|
| **A** | Image gen (scratch) | Does more detail build the character cleaner? | 2 (terse vs detailed) × 2 subjects | ~15–25 | Register look-spike / candidate hero |
| **B** | Image edit (identity) | Terse vs verbose on a pose/expression change | 4 | ~15–30 | The core over-prompting proof |
| **C** | Image edit (**compositing**) | Character → pre-made background/frame, identical + true-to-framing | base 4 + sub-tests C1–C4 | ~60–110 | anima's first compositing doctrine |
| **D** | Video (Seedance) | Word-count band + motion-only vs re-describe | 2 short ladders (~4 clips) | ~60–90 | Video doctrine confirmation |

Indicative totals land ~150–225 credits with headroom to re-roll winners inside 300. Image edits are cheap; video dominates the spend (~14 cr/Fast-720p-4s clip per the runbook).

### Block detail

- **A — generation.** Same original character brief, two rungs: a terse attribute line vs a full descriptive prompt, each × two poses/expressions. Style vocabulary drawn from `registers/samurai-jack-s5/research.md` money axes (outline-sparse flat color, hard-edged flat shadow, single emotional cast, dramatic negative space). Genericized — no franchise name in any prompt (style-neutrality doctrine). Winners are candidate hero frames.
- **B — identity edit.** Feed one character anchor (`kid-samurai-chatgpt-*.png`); target change = a single pose or expression delta; run all four rungs. Anti-text clause on every rung. Expect Rung 4 to drift face/palette.
- **C — compositing (the prize block).** The core question: can the model keep the character **identical** while placing him in the **right area** at **true-to-framing size** (a close-up fills the frame; an extreme-wide makes him tiny in vast negative space — the `samurai-jack-s5` signature). Beyond the base verbosity ladder, four compositing-specific sub-tests, each cheap and decisive:
  - **C1 — source of the character.** Anchor-as-source vs **turnaround-sheet-as-source**: feed the multi-view turnaround sheet and ask the model to lift a specific view of the character into the frame. Sean's observed workflow (anchor → turnaround → separate background → place). Tests whether a turnaround gives the model a cleaner grab than a single anchor.
  - **C2 — scale-by-framing.** Same character + same background, target framing varied: close-up / medium / wide / extreme-wide. Tests whether the prompt can drive true-to-size placement, or whether the model defaults to one scale regardless.
  - **C3 — the colored-shape placeholder.** Put a colored circle/shape in the background at the exact spot + size the character should occupy; instruct "place the character where the shape is, matching its size and position, and remove the shape." Tests placement precision against a concrete visual target. **Then** the precision probe: can the model hit the mark on its own from a text description of location, or does it need the shape?
  - **C4 — manual-placeholder fallback.** If C3's model-drawn/auto placement misses, Sean draws the placeholder shape manually on his iPad at the exact mark and re-runs C3's placement step. Tests whether a human-authored placeholder closes the gap — the practical escape hatch if the model can't self-place.
  This block generates anima's first documented **compositing doctrine**; the budget concentrates here.
- **D — video.** Two anchor frames (start+end) from the character; two short ladders: (i) word count 30 / 80 / 130 words, (ii) motion-only vs re-describe-the-subject. Via the Higgsfield CLI runbook (Seedance 2.0 Fast 720p). Claude reads extracted stills for identity/aesthetic; **Sean watches the .mp4 for the motion verdict** (Claude can't watch video).

---

## 4. Mechanics — how Claude runs it (all via the Higgsfield CLI, in Claude Code)

Everything runs through the `higgsfield` CLI in a Claude Code session — one tool, one credit pool, image + video.

- **Preflight (blocking, do first):** `higgsfield account status` (auth + credits) and `higgsfield model list` / `higgsfield model get <model> --json` to find the CLI's **image / edit model** and its exact params (the runbook only documented Seedance video; the image model's name, reference-image flags, and cost are an unknown to resolve before spending). **Contingency:** if the CLI exposes no usable Nano-Banana-class image-edit model, that is itself a finding — record it, and the image blocks fall back to the connected Higgsfield MCP (`generate_image`); video is unaffected. This is the one branch the plan must carry.
- **Auth:** one-time `higgsfield auth login` is human-only (interactive OAuth) — the single command Sean runs; Claude runs everything after.
- **References:** the CLI auto-uploads local PNGs passed as image args (as it does for `--start-image` / `--end-image` in the video runbook); the GRANDMASTER frames are referenced by local path from the run folder.
- **Prompts to files:** every rung prompt is written to a `.txt` and passed as `--prompt "$(cat p.txt)"` — pencil/samurai prompts carry apostrophes and quotes that break inline `--prompt` (runbook §8).
- **Engine (video D):** `higgsfield generate create seedance_2_0 … --mode fast --resolution 720p --duration N --generate_audio false --aspect_ratio 16:9 --wait` per the runbook. 4s minimum; Claude reads extracted stills, Sean watches the .mp4.
- **Output tree (the harness convention):** `runs/2026-07-11-prompt-ladder-grandmaster/` (gitignored/local per Sean's convention), one subfolder per block (`A_generation/`, `B_identity_edit/`, `C_compositing/{C1..C4}/`, `D_video/`), each with the rung prompts (`.txt`), outputs, a contact sheet, and `scoring.md`.
- **Cost safety:** read-only `higgsfield generate cost …` before each block; block gate before proceeding; rejected/too-short requests cost 0.

---

## 5. Deliverables

1. **Reusable harness** — the `runs/…prompt-ladder…/` folder convention + a rung-prompt template + the `scoring.md` sheet, rerunnable whenever a model updates. Committed as a small template under `docs/` (not the gitignored run outputs).
2. **Register + doctrine updates** — winning clauses fold into the `samurai-jack-s5` research/spec draft; **compositing findings become a new short doctrine doc** (anima's first) alongside the NB2 editing template; the Block-A hero candidate is offered for the register's Human Checkpoint 2 lock.
3. **Prompt-writing skill / decision card** — a one-page "image-gen vs image-edit vs compositing vs video: how much to prompt" card distilled from the scoring sheets, packaged so any future session (or Sean) reaches for it.

Plus a `CHANGELOG.md` entry recording the run, credits spent, and the findings.

---

## 6. Out of scope / guardrails

- No authoring `samurai-jack-s5` into `pipeline/registers.py` (separate $0 drill, already planned).
- No wiring a gpt-image runner; no across-edit identity *validation* as a gated GRANDMASTER production build.
- No third-party *Samurai Jack* frames committed or fed to any generation call (style-neutrality doctrine — capture the school, never the episode). Only Sean's own genericized outputs land in the repo.
- No LLM aesthetic judge on creative quality — Sean's eye is the sole arbiter at every block gate (eval-handbook rule).
- Block gates are hard: budget overrun on one block stops the run and banks the finding.

---

## 7. Open questions (resolved this session)

- **Image engine** → Higgsfield Nano-Banana (one credit pool).
- **Operating model** → Claude runs, Sean reviews.
- **Subject** → the GRANDMASTER kid-samurai (`registers/samurai-jack-s5/refs/chatgpt/`).
- **Deliverables** → harness + register updates + prompt skill (all three).

---

## References

- `docs/research/2026-05-30-nb2-editing-character-consistency-template.md` — the NB2 editing doctrine.
- `prompts/seedance-template-v4.md` · `docs/research/seedance-research-findings.md` — video prompting rules.
- `docs/anima-test-runs/2026-06-22-higgsfield-seedance-generation-runbook.md` — the CLI video runbook (costs, gotchas).
- `docs/active/2026-07-11-samurai-jack-s5-register-design.md` — the register plan (look-spike / hero lock pending).
- `registers/samurai-jack-s5/refs/chatgpt/` — the character anchors + scene-before/after compositing exemplars.
- `docs/architecture/prompt-style-neutrality-doctrine.md` — genericization rule for all prompts.
