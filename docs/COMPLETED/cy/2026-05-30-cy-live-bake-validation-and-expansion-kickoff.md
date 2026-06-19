# Kickoff prompt — first live bake on the new emitter (validation) + mascot expression expansion

*Paste everything below the divider into a Claude Code session opened at `/Users/seanwinslow/Code-Brain/anima`. This is a LIVE session — real NB2 + Gemini calls (needs `GEMINI_API_KEY` in `.env` and `agy` on PATH) — with human 🚦 STOP gates. Its load-bearing purpose is to **validate the register-agnostic emitter against a real model for the first time**; its product is **new Act 2 expression assets for the claude-mascot**. It opens with one offline hygiene fix. **Plan first with the writing-plans skill; present the plan; proceed only on Sean's explicit approval.***

---

You are running the validation the template-emitter follow-on deferred. That session ([`docs/anima-test-runs/2026-05-30-cy-template-emitter-and-tool-bugfix-followon.md`](../../anima-test-runs/2026-05-30-cy-template-emitter-and-tool-bugfix-followon.md)) built the five-slot register-agnostic emitter and proved it with emitted-prompt assertions — but **never called a live model**, on purpose, to keep the locked Bibles byte-untouched. So the new pencil/register emit (richer prose on every plate — the `ONLY CHANGE` idiom, the full preserve clause, a standing style token) has not yet met a real NB2 generation. This session is that meeting. The honest open question, in the follow-on's own words: *does adding standing prose to every prompt hold the form, or reintroduce the prompt-dominance drift the terseness lesson warned about?* If it drifts, the fix is to **trim the clause library, not revert the structure**.

**Read these first, before you plan:**
1. [`docs/anima-test-runs/2026-05-30-cy-template-emitter-and-tool-bugfix-followon.md`](../../anima-test-runs/2026-05-30-cy-template-emitter-and-tool-bugfix-followon.md) — what was built and what was deferred (the live-bake validation is the §"How we should proceed" item 1). Note the two queued items: the Maya `plan mutate` sibling bug, and the NB-Pro guard.
2. [`docs/research/2026-05-30-nb2-editing-character-consistency-template.md`](../../research/2026-05-30-nb2-editing-character-consistency-template.md) — the five-slot template + the per-register clause library that the emitter now reads. This is what you're validating; it's also where a trim lands if the prose drifts.
3. [`docs/anima-test-runs/2026-05-30-claude-mascot-pencil-register-pivot.md`](../../anima-test-runs/2026-05-30-claude-mascot-pencil-register-pivot.md) §3 — the last time mascot expressions were generated: NB2 enlarged the dot eyes to glossy cartoon eyes and added a hair tuft. Those are the *exact* drifts to watch for here; the `no-hair` rule + small-dot-eyes correction now exist to steer against them.

**Read the code surfaces you'll touch** (read, don't guess — three sessions running, the plan must match the mechanism's real shape):
- `pipeline/agents/character_designer.py` — the new `_build_plate_prompt` + `_REGISTER_CLAUSE_LIBRARY` + `_resolve_plate_model`/`_REGISTER_MODELS`, `_run_plate` (now takes `style_register` + `generation_model`), the plates-only bake path, the DINOv2 similarity gate.
- `pipeline/cli/bible.py` — `bible iterate` (the re-roll/`--reject` path) and whether an **additive** path (`--add <names>`) exists for adding new plates + rules to a locked Bible. **This is the open mechanism question — confirm it before planning the expansion.**
- `pipeline/cli/plan.py:246` — the queued Maya sibling bug (`bump_version` into the schema-gated field).
- `characters/claude-mascot/` — the locked Bible (anchor, `acceptance_criteria.json` at `version: 1.2`, the 14 IR rules, the 5 ingested turnaround crops + 2 generated expressions, `plate_generation_plan.json`).

---

## The work (your INPUT — sequence, dependency-order, and commit-split it in the plan)

**Phase 0 — Offline hygiene: close the Maya `plan mutate` sibling bug (open with this).** `pipeline/cli/plan.py:246` still routes `--new-version` through `bump_version` into the schema-gated `version` field — the same landmine `bible mutate` had, partially masked (only breaks on an off-allowlist major like `1.3.0`/`2.0.0`). Fix it as a shared-primitive decision, not a copy-paste: the cleanest move is to **harden `bump_version` to refuse a `new_version` whose major.minor isn't a known schema version**, which protects both callers at once; or give `mutate_plan` the same content-version decoupling `bible mutate` got. Extend the live-manifest tripwire (`tests/test_live_manifest_criteria.py`) to cover the brief path once `criteria_sources.brief_file` is populated (it's empty today, so the brief surface isn't under the net). Test-first, one commit, offline. This is certain, safe work — land it before any live call.

**Phase 1 — Confirm the additive-expansion mechanism (no live calls yet, planning-critical).** Adding new expression plates to a **locked** Bible needs both new plate-plan entries *and* new `IR.{id}.face.*` rules — and the Bible is locked, so this is not a plates-only re-bake of the existing plan. Establish the supported path before generating anything: does `bible iterate --add <names>` exist and author new plates + rules without re-running all of Pass 1? Read the code. If it exists and works, use it. If it doesn't, **STOP and surface the gap to Sean** — adding the mechanism may be a small build of its own, and Sean decides whether to build it here or split it out. Do not improvise an unaudited hand-edit of a locked Bible. (The 2026-05-29 lesson: approval must be *enforceable*, and a locked Bible is never silently re-authored.)

**Phase 2 — The live emitter validation (the load-bearing goal).** Generate a small set of **new mascot expressions** through the new five-slot emitter — Sean picks the set; a sensible Act 2 starting four is `alarm`, `delight`, `sleep`, `alert-perk`. Generate them **first to a scratch run-dir path** (`runs/2026-MM-DD-emitter-validation/`), NOT into the locked Bible, so the validation is byte-safe. For each: eyeball it and score DINOv2 vs `anchor.png`. 🚦 **STOP — present them to Sean.** The bar is the drift watch from §3: does the box-creature form hold with **small graphite dot eyes and no hair tuft**, in full pencil-test color, or did the richer standing prose reintroduce the cartoon-eye / hair drift? **Decision branch:**
- **Holds** → the emitter is validated; proceed to Phase 3 to add the expressions properly.
- **Drifts** → the standing prose is the suspect. **Trim the clause library** (`_REGISTER_CLAUSE_LIBRARY["pencil-test-colored"]`) — not the structure — commit the trim with the before/after evidence, re-generate, re-present. This is the single most important outcome of the session either way: a validated emitter, or a measured trim with the bake that proved it necessary.

**Phase 3 — Add the validated expressions to the mascot Bible (the Act 2 product).** Using the Phase 1 mechanism: add the approved expressions as new plates + author their `IR.claude-mascot.face.*` rules (each citing the `no-hair` and dot-eye invariants), bake them into `characters/claude-mascot/expressions/`, run Pass-3 verification, persist the verdict trail, and re-approve the Bible (now N expressions, still `version: 1.2`, content_version bump is fine — that path is fixed now). 🚦 **STOP — show Sean the full expression set** before committing. Each must read as the same box-creature.

**Phase 4 — Motion plates (scope decision, likely a follow-on).** The mascot has *zero* motion plates — the load-bearing gap for any Phase 6 mascot clip. But motion is Sean's domain (he blocks timing), so motion *reference* plates likely want to come from **Sean's drawn keys via the ingest path**, not generation — which depends on art that may not exist yet. In the plan, **scope this honestly**: if Sean has drawn motion source plates, ingest-crop them (the validated zero-drift path); if not, name the dependency and defer motion plates to a dedicated session. Do not generate motion plates speculatively.

**Phase 5 — Wrap.** Tests green; CHANGELOG per commit; update `CLAUDE.md` (the mascot expression inventory, the emitter-validation outcome — held or trimmed — as a durable note, the Maya fix); the field report (`docs/anima-test-runs/`); push. Report: the validation verdict (held / trimmed, with the evidence), the new plate set, what Sean still needs to eyeball before this feeds Act 2, and the motion-plate decision.

---

## Working discipline (non-negotiable)

- **Plan mode first** (`Shift+Tab` twice), **writing-plans skill**, present the plan, proceed only on Sean's explicit approval. Confirm the Phase 1 mechanism question *in the plan* — don't discover it mid-bake.
- **The emitter validation (Phase 2) is the goal; the expansion is the product.** If Phase 1 reveals the additive mechanism is a real build, the validation in Phase 2 can still run (it's scratch-path, Bible-free) — do the validation regardless, even if the expansion has to split off.
- **Locked Bibles are extended additively + re-approved, never re-authored.** No full Cy Pass-1 re-run on claude-mascot or sean-anchor. The locked rules are not re-emitted; new rules are *added* through the audited path.
- **Test-first for any code change** (the Phase 0 fix, any clause-library trim). `.venv/bin/pytest tests/ -q` stays green (baseline **200 passing**); report the count each time. Each phase its own commit; studio-manual prose, clean markdown.
- **Honor the validated pattern:** where Sean has drawn real source art, **ingest-crop beats generate** (zero drift); reserve generation for what the references don't cover, and trait-lock the generated ones hard (small dot eyes, no hair) — NB2 will cartoonify and add hair if left unconstrained.
- **Watch the drift you can't prompt away vs. the drift you can.** Cartoon-eyes/hair on a generated expression is prompt-steerable (trim + reject-reason now steers, post the §3 fix). If an expression needs an angle/pose the anchor + turnaround don't contain, that's a reference gap — name it, don't grind re-rolls.

## Out of scope (queued — do NOT start)

- **The cross-character continuity audit** — the scoped next architectural session (per [`docs/anima-test-runs/2026-05-30-two-character-first-light.md`](../../anima-test-runs/2026-05-30-two-character-first-light.md)). Not here.
- **The NB-Pro painterly-final guard** — build it when a Pro-routed (watercolor/photoreal/3D) character lands, and re-verify the Pro multi-reference regression then. No consumer yet.
- **The 16BitFit-humanoid pixel-register pass** — the register-agnosticism proof on a real second register; its own session (now cheaper — the emitter takes a new register as a row).
- The per-view-reference hard similarity gate; Em's closing-the-loop case 7; sean-anchor identity tuning; the repo rename. **sean-anchor expression expansion** is a reasonable *stretch* if the mascot work lands cleanly and time remains — but the mascot is the Act 2 priority; don't start sean-anchor at the cost of finishing the mascot.

## Rollback & branch

Each phase its own commit. Phase 2 is scratch-path and Bible-free — nothing to roll back. The Phase 0 fix and any clause-library trim are behavior-pinned by tests; `git revert` the commit if a trim regresses. The locked Bibles are only touched in Phase 3, through the audited additive path, and re-approval is a deliberate gate — a bad expression is a `bible iterate --reject` re-roll, not a re-author. **Branch:** the prior work sits on `feature/maya-planner-and-em-live`; confirm with Sean whether this session continues there or wants its own branch before the first commit.

**The freshness caveat still rides along:** if anything routes to NB Pro (it shouldn't this session — pencil-test-colored is NB2), the Pro multi-reference regression is operational and may be patched; re-verify before relying on it. Pencil-test mascot work is NB2 throughout.
