# Kickoff prompt — sean-anchor approve + bake, mascot re-bake, gate hardening (next steps 1–5)

*Paste everything below the divider into a Claude Code session opened at `/Users/seanwinslow/Code-Brain/anima`. This is a CODE + authoring session: it ships commits, runs live model calls, and has explicit human-review gates where you (Sean) must look before it proceeds. The folder has already been renamed to `anima`; the remote is `github.com/seanwinslow28/anima.git`; the test baseline is **176 passed**.*

*This session does five things, in order: (1) fix the stylus prop-plate defect at the mechanism level, (2) tighten the turnaround crop boxes, (3) review + approve the sean-anchor Bible, (4) bake its production plates, then (5) re-bake the mascot — followed by two hardening items (DINOv2 similarity tier, Cy parse-retry). Three amendments from the 2026-05-29 plate review are baked into Phases 1–3; do not skip them.*

---

You are executing the post-fidelity-fix production work on the **anima** project. Read these first, in order, and treat them as the source of truth:

1. `docs/2026-05-29-cy-visual-fidelity-post-mortem.md` — the diagnosis (esp. §3 root cause, §5 fix candidates).
2. `docs/anima-test-runs/2026-05-29-fidelity-fix-session-writeup.md` — what the fix session shipped and deferred (§5 deferred, §6 next steps).
3. `pipeline/agents/character_designer.py` — the runner you'll amend. Key functions: `_run_plate` (~495), `_resolve_generate_references` (~877), `_build_nb_pro_prompt` (~911), `_classify_reference` (~837), `_score_plate_identity` (~644), `_region_box`/`_crop_region` (~784/813).
4. `pipeline/agents/similarity_gate.py` — the Pass-2.5 gate (DINOv2→CLIP→PIL ladder).

**Working discipline (non-negotiable):**
- Plan mode first (`Shift+Tab` twice). Show the plan. Proceed only on Sean's approval.
- `.venv/bin/pytest tests/ -q` must stay green (≥176) before and after every commit. Never commit red.
- Each phase is its own commit; CHANGELOG entry per commit.
- **Honor the human-review gates marked 🚦 STOP — present the artifact to Sean and wait. Do not run `bible approve` or commit baked plates without Sean's explicit go.** Taste calls are Sean's; you set them up.
- Live model calls cost money and can hit the transient Opus 4.8 stub — the loud guard will tell you; re-run on a stub, don't ship it.

---

## Phase 1 — Fix the stylus prop-plate defect (the mechanism bug)

**The problem.** The re-baked `props/stylus.png` rendered the *full character* with a stylus floating disconnected beside an empty-gripping hand — not an isolated prop. Root cause: the fidelity fix's `_resolve_generate_references` injects `anchor.png` unconditionally as "Image 1 — match this character exactly," and `_build_nb_pro_prompt` frames every plate around that identity. That's correct for character plates (turnarounds, expressions) and **wrong for prop/object plates**, where the full-body anchor tells NB Pro to draw the whole person. The stylus plan entry (`props/stylus.png`, `source: generate`, `reference_images: ["anchor.png"]`, prompt "isolated stylus on cream paper… no hand gripping it") is being overridden by the injection framing.

**The fix — teach the runner that prop plates are a distinct class:**

1. Add a prop-plate predicate. A plate is a prop plate when its `target_path` starts with `props/`. (Define a small helper or constant, e.g. `_PROP_PLATE_DIRS = {"props"}`, mirroring `_GENERATED_PLATE_DIRS`.)
2. In `_resolve_generate_references`: **for prop plates, do NOT inject `anchor.png`.** Keep only the `source_ref`/`external` references Opus named (for the stylus there are none, which is correct — it becomes a pure text-to-image isolated-object render). Return a signal (e.g. a third tuple element `is_prop` or reuse `has_pose_ref=False`) so the prompt builder knows.
3. Add `_build_prop_prompt` (or branch inside `_build_nb_pro_prompt`) for prop plates. It must frame the generation as an **isolated object**, explicitly forbidding any figure and any text:
   - "Render ONLY the isolated object described below, centered on a warm cream paper background. Do NOT draw any person, character, hand, body, or figure. Do NOT render any text, caption, label, handwriting, or annotation anywhere in the image."
   - then `Render: {plate_intent}`.
   - Keep the existing anti-caption guardrail; this strengthens it for props.
4. **Exempt prop plates from the Pass-2.5 anchor-similarity reject.** In `_score_plate_identity` / `_run_plate`, a prop plate compared against the full-character `anchor.png` will always score near-zero and could trigger spurious regeneration. For prop plates: **record** the similarity score in `plate_verdicts.jsonl` (so the audit trail is complete) but mark it `gate: "record-only (prop plate — not identity-scored)"` and never use it to reject/regenerate.
5. Trim the stylus plate prompt in `characters/sean-anchor/plate_generation_plan.json` to a short intent only — "a single working-illustrator's stylus: straight cylindrical barrel ~14cm, tapered conical tip, rounded blunt end, no clip, lying at a ~60° diagonal." Strip the long meta-prose ("The plate serves as the canonical prop reference for…") that caused the original caption-rendering — the role-tag framing now lives in the runner, not the plate text.

**Tests:** add a unit test asserting (a) a `props/*` plate gets an empty/anchor-free reference list from `_resolve_generate_references`, (b) the prop prompt contains the no-figure + no-text clauses, (c) a prop plate is not anchor-similarity-rejected. Keep the existing 176 green. Commit: `fix: prop plates are isolated objects — no anchor injection, no identity gate, no caption text`.

## Phase 2 — Tighten the turnaround crop boxes

The committed crop mechanism works (verified: `turnaround-1.regions.json` produces distinct ~10–15% crops). One nit: the `body-front` box catches the "A-2" production label in the top-left corner.

1. In `characters/sean-anchor/source-refs/turnaround-1.regions.json`, change `body-front` left edge from `0.02` to `0.05` (→ `[0.05, 0.01, 0.26, 0.60]`). Leave the others unless a render shows a problem.
2. Render all 7 crops to a scratch dir and 🚦 **STOP — show Sean the 7 crops** so he can confirm box placement (each should be one clean figure/head, no neighbor bleed, no label). Apply any box nudges Sean calls, then continue. No commit yet — the regions file rides along with the Phase 4 bake commit, or commit standalone as `fix: nudge body-front crop box off the A-2 label` if Sean prefers.

## Phase 3 — Handle the contemplative bright-blue (no rule edit)

The `IR.sean.costume.navy-tee-cool-gray-jeans` rule already specifies the correct dark navy `#243044`; the scratch `contemplative.png` drifted *brighter* than that. **This is generation variance, not a wrong rule — do NOT change the hex, and do NOT add color adjectives to the plate prompts** (verbose color description risks re-triggering the prompt-dominance the fidelity fix removed). The handling:
- Rely on the existing "match the color palette of Image 1 exactly" framing + the anchor injection; a fresh bake (Phase 5) should pull the navy back toward the anchor.
- If a specific plate still reads bright-royal after the Phase 5 bake, re-roll *that single plate* via `python -m pipeline.cli bible iterate --character-dir characters/sean-anchor/ --target expressions --reject contemplative --reason "tee drifted brighter than anchor navy #243044" --run-dir runs/<run>`. Do not re-bake the whole Bible for one plate.
- No commit in this phase; it's policy that governs Phases 5–6.

## Phase 4 — Review + approve the sean-anchor Bible

1. `python -m pipeline.cli bible show --character-dir characters/sean-anchor/` and open `characters/sean-anchor/acceptance_criteria.json` (22 rules, `locked: false`, full-color v1.2).
2. 🚦 **STOP — present to Sean** the ported color rules for confirmation: skin `#F0DFCB`, eye `#4A6D8C`, cream paper `#F2E6CC`, navy tee `#243044`, cool-gray jeans `#5C6471`, plus the full rule list grouped by category. Ask Sean to confirm or adjust any hex. Apply edits only if Sean calls them.
3. On Sean's explicit go: `python -m pipeline.cli bible approve --character-dir characters/sean-anchor/` (flips `locked: true`). Commit: `bible: approve sean-anchor full-color Bible (22 rules, v1.2)`.

## Phase 5 — Bake the sean-anchor production plates

With Phase 1's prop fix + Phase 2's crops + the approved rules:
1. Run the authoring orchestrator against the approved Bible:
   `python scripts/author_bible.py characters/sean-anchor/ --studio-brief "Pencil Test reference character — full-color, see source-refs/notes.md" --run-dir runs/2026-MM-DD-cy-sean-anchor-production/`
   (If a stub fallback fires — the loud guard exits non-zero — re-run; it's the transient Opus 4.8 case.)
2. The crop-ingest plates (body + head turnarounds, head-profile) should land as proper region crops; the generate plates (head-back, head-profile-right, expressions, stylus) use the fixed mechanism.
3. Copy the approved plate PNGs into the production `characters/sean-anchor/{turnarounds,expressions,props,...}/` folders.
4. 🚦 **STOP — show Sean the full new plate set**, especially: `props/stylus.png` (must now be a clean isolated stylus, no figure, no text), `expressions/contemplative.png` (navy should match the anchor), and the cropped turnarounds (distinct figures, not full-sheet copies). Sean eyeballs against the engine truth ("recognizably Sean"). Re-roll any individual drifters via `bible iterate` per Phase 3. Commit once Sean approves: `bake: sean-anchor production plates against approved Bible`.

## Phase 6 — Full mascot re-bake

The mascot only got `head-front` last session (the rest hit the transient stub). The robust parser handles Opus 4.8 narration now.
1. `python scripts/author_bible.py characters/claude-mascot/ --studio-brief "Pixel-art-8bit mascot — see source-refs/notes.md" --run-dir runs/2026-MM-DD-cy-claude-mascot-production/` (re-run on any stub).
2. 🚦 **STOP — show Sean** the full mascot plate set: it must read as the orange pixel-octopus (blocky lozenge, dot eyes, stub legs, snout) — NOT the generic chibi humanoid the pre-fix run produced. Note the known similarity-gate blind spot on the mascot register (PIL tier is unreliable for tiny-subject framing — the visual gate is the arbiter here until Phase 7's DINOv2 lands).
3. On Sean's go: review → `bible approve` (if the mascot Bible needs re-approval) → commit `bake: claude-mascot production plates (full set, fixed mechanism)`.

## Phase 7 — Install the DINOv2 similarity tier + promote the gate (next step 4)

The PIL-only gate is a known liar on the mascot register (it ranked the drifted mascot above the recovered one). DINOv2 is scale/background-robust and is what makes the gate trustworthy enough to become a hard pre-Gemini reject.
1. `.venv/bin/pip install torch transformers` (~2GB; this is the one place the venv grows). Confirm `similarity_gate.py`'s ladder now selects the DINOv2 tier.
2. Re-score both Bibles' `runs/.../plate_verdicts.jsonl` with DINOv2 and confirm, on **both** registers, recovered plates score above the old drifted ones. Add a regression eval (under `evals/`) asserting `recovered > drifted` for a held pair on each register.
3. Promote the gate from record-only to a **hard pre-Gemini reject** below a tuned threshold — but keep the Phase-1 prop-plate exemption (props are never identity-scored). 🚦 **STOP — show Sean the chosen threshold + the recovered/drifted scores** before flipping it to blocking.
4. Commit: `feat: DINOv2 similarity tier + promote Pass-2.5 to hard gate (prop plates exempt) + regression eval`.

## Phase 8 — Wire Cy's Pass-1 retry-on-parse-failure (next step 5)

The transient Opus 4.8 malformed-emission case is caught loudly but needs a human re-run. Auto-recover within Cy's existing three-call Pass-1 budget.
1. In the Pass-1 path (`CharacterDesignerNode.run` / `_parse_json_envelope`), on a parse failure or `_pass1_stub` sentinel, retry the Opus call up to the remaining three-call budget before falling back to the loud stub. Distinguish *parse failure* (retry) from *contract violation* (don't retry — that's a real rejection).
2. Add a test: a first-call malformed emission + a second-call clean emission yields a real Bible, no stub, within budget.
3. Commit: `feat: Cy Pass-1 retry-on-parse-failure (auto-heal transient Opus 4.8 malformations within the 3-call budget)`.

## Phase 9 — Wrap

1. `.venv/bin/pytest tests/ -q` — confirm green (will be >176 after the added tests; report the number).
2. CHANGELOG entry covering all phases. Update `CLAUDE.md` if the prop-plate contract or the gate-promotion changes how Bible authoring works (they do — note the prop-plate exception and the hard gate).
3. `git push`. Report final state: commits shipped, test count, which plates were re-rolled, the DINOv2 threshold, and anything Sean still needs to eyeball.

**Out of scope this session:** Em's closing-the-loop case 7 (merged CriteriaBundle IR.* load) stays xfailed — that's the next session after this. Don't touch the rename (done). Don't make the GitHub repo public (separate future step).

**Rollback:** every phase is its own commit; if a bake produces worse plates than the scratch set, `git revert` the bake commit and re-roll. The approved rules (`locked: true`) are not touched by a bake.
