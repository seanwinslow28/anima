# Kickoff prompt — the Cy template-emitter refactor (+ the two tool-bug fixes + the safety-net test)

*Paste everything below the divider into a Claude Code session opened at `/Users/seanwinslow/Code-Brain/anima`. This is a CODE session — mostly mechanism refactor + tool-bug fixes, runnable largely offline (stub fallback + tests). It does NOT re-author or re-bake any Bible against live models; the two locked Bibles (sean-anchor, claude-mascot) stay untouched. **Plan first, with the writing-plans skill, and get Sean's approval on the plan before writing any code.***

---

You are implementing the follow-on the 2026-05-30 claude-mascot pivot deferred: turn Cy's plate-prompt construction into the register-agnostic editing template, wire per-register model routing, and fix the two tool bugs that session surfaced. The research and the decisions are already done — your job is to land them cleanly, test-first, one commit per coherent change.

**Read these first, in order, before you plan:**
1. [`docs/research/2026-05-30-nb2-editing-character-consistency-template.md`](research/2026-05-30-nb2-editing-character-consistency-template.md) — the five-slot register-agnostic editing template (`{identity_lock}` / `{variation}` / `{preserve_and_negative}` / `{style_register}` / `{output_spec}`), the per-register clause library, the three worked examples, the storyboard variant. **This is the spec for the refactor.**
2. [`docs/2026-05-30-claude-mascot-pencil-register-pivot-kickoff-amendments.md`](2026-05-30-claude-mascot-pencil-register-pivot-kickoff-amendments.md) — Amendment A (refactor `_build_nb_pro_prompt` → register-parameterized emitter), Amendment B (per-register NB2/Pro routing), Amendment C (storyboard variant as a Phase-2/3/5 primitive). The two locked decisions: **refactor the runner builder**, **per-register split**.
3. [`docs/anima-test-runs/2026-05-30-claude-mascot-pencil-register-pivot.md`](anima-test-runs/2026-05-30-claude-mascot-pencil-register-pivot.md) — the post-mortem. §3 (the `bible iterate` reject-reason never reaches the prompt), §4 (the `bible mutate --new-version` schema-version break), and the recurring lesson: *green CI that mocks the boundary that broke is not coverage — every fix here gets the test that would have caught the bug.*

**Then read the code surfaces you'll touch** (read, don't guess — the pivot session proved the plan must match the mechanism's real shape):
- `pipeline/agents/character_designer.py` — `_build_nb_pro_prompt` (~1071, the current fixed pencil-leaning framing), `_build_prop_prompt` (~1099, the isolated-object exception), `_resolve_generate_references` (~1028, runner-owned anchor injection + no-chaining), `_run_plate` (~495, the call site).
- `pipeline/agents/nb_pro_runner.py` — `invoke_nb_pro` (default already flipped to NB2 last session), `_build_skill_cmd` (builds the subprocess argv from `prompt` alone — this is *why* `reject_reason` never reaches the model today), `_compute_cache_key` (where `reject_reason` currently lands).
- `pipeline/agents/prompts/cy-character-designer-context.md` — the prompt-contract section that needs the paired paragraph (Amendment A).
- `pipeline/cli/bible.py` + `pipeline/criteria.py` — `bible mutate`, `validate_criteria` (the `1.0/1.1/1.2` schema allowlist), `load_all_criteria` (the live-manifest merge).
- `manifest.yaml` — the `characters.{id}` block (per-register model assignment lands here).

---

## The work (your INPUT — sequence and commit-split it yourself in the plan)

This is the substance the plan must cover. Order is a suggestion; you own the final sequence, dependency graph, and commit boundaries. Each piece is test-first: **write the test that would have caught the bug (or that pins the new behavior), watch it fail, then make it pass.**

**1. The safety-net integration test (do this first — cheapest, highest-leverage).** Add a test that calls `load_all_criteria` on the *live* `manifest.yaml` (not a fixture) and asserts the merged `CriteriaBundle` parses and has zero ID collisions across `IR.*` namespaces. This is the single test that would have caught the `bible mutate` schema break at commit time — the pivot session shipped an unloadable Bible with a green suite because every criteria test uses fixtures. It should pass against the current (restored) state; it's the regression guard, not a red-to-green. Land it before anything else so the rest of the session has the net.

**2. Fix `bible mutate`'s schema-version conflation (post-mortem §4).** `--new-version` writes a content semver into the schema-`version` field that `validate_criteria` gates on a `1.0/1.1/1.2` allowlist, making the Bible unloadable. Split content-version from schema-version (a separate `content_version` field, or refuse a `--new-version` outside the schema allowlist — you choose, justify it in the plan). The post-mortem also notes mutate currently writes the audit record *without applying the field change to the rule content* — the mutation is audit-only today; fix that too so a mutate actually edits the rule and keeps the Bible loadable. Test: mutate a locked test Bible, assert the field changed AND `load_all_criteria` still parses it. (The CLAUDE.md example was already defused with a ⚠️ caution on 2026-05-30; this is the code fix that lets the caution be lifted.)

**3. Refactor `_build_nb_pro_prompt` → a register-parameterized template emitter (Amendment A — the core).** Build the five-slot emitter from the template doc: it reads a per-register clause library keyed on the closed `style_register` vocabulary (`pencil-test-colored | pixel-art-8bit | line-art-only | watercolor | photoreal | 3d-rendered`) and fills `{identity_lock}`, `{preserve_and_negative}`, `{style_register}` from the matched row; `{variation}` stays Cy's terse intent wrapped in the `ONLY CHANGE` idiom; `{output_spec}` comes from the plate/manifest. **Must not regress:** the terse-intent contract, the universal anti-text clause, and the "keep the full color of Image 1" line (now the `pencil-test-colored` row's preserve clause — the line that recovered `focused`). Keep `_build_prop_prompt` as the isolated-object `{output_spec}` case. Add the per-register clause library as a real data structure (a dict/table), so adding a register is a deliberate row-add. Then add the paired paragraph to `cy-character-designer-context.md` (Cy authors only `{variation}`; the runner wraps it in the five-slot template; `style_register` now also selects the identity-lock enumeration and style token). Tests: each register fills the slots correctly; pencil-test still emits the full-color line; the prop path is unchanged; the terse-intent + anti-text invariants hold.

**4. Wire `bible iterate`'s reject-reason into the prompt (post-mortem §3) — depends on #3.** Today `reject_reason` only busts the cache key; `_build_skill_cmd` never passes it to the model, so a re-roll re-samples with the identical prompt (gambling, not steering). With the template emitter in place, thread `reject_reason` into the `{preserve_and_negative}` slot so the correction actually reaches NB2. Test: an `iterate` with a reject reason produces an emitted prompt containing the reason in the preserve/negative slot — not merely a changed cache key.

**5. Per-register model routing + the rename (Amendment B) — depends on #3.** Wire per-register model assignment through the manifest `characters.{id}` block (e.g. `generation_model` / `final_model`) read at plate time, per Amendment B's table (NB2 default for editing/consistency + pixel/flat/line/pencil; NB Pro reserved for painterly/watercolor/3D *finals*). Rename `invoke_nb_pro` → `invoke_image_edit` (model is a parameter; the name shouldn't assert Pro) with the call sites updated. The verification+regenerate guard for the NB-Pro-final path has no consumer yet (no Pro-routed character exists) — scaffold it minimally or leave a clearly-marked seam; don't over-build a branch nothing takes. Justify your call in the plan. Tests: a `watercolor`-register character routes its final to the Pro slug; a `pencil-test-colored` character routes to NB2; the rename leaves behavior identical.

**6. Wrap.** CLAUDE.md (lift the ⚠️ mutate caution if #2 fixed it; document the template emitter as the prompt-construction source of truth and the per-register routing; note `invoke_image_edit`); CHANGELOG per commit; `git push`; final report.

---

## Working discipline (non-negotiable)

- **Plan mode first** (`Shift+Tab` twice). Use the **writing-plans skill** to map the full execution — phases, dependency order, commit boundaries, the test for each fix, the verification step. **🚦 STOP and present the plan to Sean; proceed only on his explicit approval.** This is the one hard gate; the rest of the session is mechanism work.
- **Test-first, every fix.** Each of the six pieces lands with the test that pins it (or that would have caught the bug). `.venv/bin/pytest tests/ -q` stays green (baseline **188 passing**) before and after every commit; report the count each time.
- **Each phase its own commit; CHANGELOG entry per commit.** Studio-manual voice in docs (prose, not terminal-dump); clean markdown, no box-drawing characters.
- **Verify the emitter by emitted-prompt assertions, not by re-baking.** Do NOT re-run live Cy bakes against sean-anchor or claude-mascot — the locked Bibles and their approved plates stay byte-untouched. If you want a live smoke-test of the new emitter, generate ONE throwaway plate to a scratch run-dir path; never into a committed `characters/{id}/` tree.
- **Honor the contract the template encodes** (don't fight the field lessons): terse intent + strong reference beats verbose prose; the runner owns identity framing; Cy authors only `{variation}`; editing ≠ generation.

## Out of scope (queued — do NOT start)

- **The cross-character continuity audit** — its own next session. The two-Bible *generation* path works; the gap is the *checking* (per-character IR into one verdict, relative-scale rule, occlusion, shared-register check). Scoped in [`docs/anima-test-runs/2026-05-30-two-character-first-light.md`](anima-test-runs/2026-05-30-two-character-first-light.md). Don't build it here.
- **Re-authoring or re-baking any Bible**; expression/motion-plate expansion for sean-anchor or claude-mascot (that's a live-bake session, and the validated pattern there is *Sean draws the source plates, Cy ingest-crops them*).
- The 16BitFit-humanoid pixel-register pass; the per-view-reference hard similarity gate; Em's closing-the-loop case 7; sean-anchor identity tuning; the repo rename. None of these.

## Rollback

Each phase is its own commit. The refactor is behavior-preserving by construction (the pencil-test register must emit a prompt equivalent to today's `_build_nb_pro_prompt` output for the same intent) — if a register's emitted prompt regresses, `git revert` that commit; the locked Bibles are never touched, so nothing downstream can corrupt. The safety-net test (#1) is the tripwire: if `load_all_criteria` on the live manifest ever fails, stop and fix before proceeding.

**Freshness caveat to carry in:** the NB Pro multi-reference regression that motivates the NB2 default is operational (reported late-Feb/early-Mar 2026) and may be patched. The per-register routing is correct regardless (NB2 is cheaper and faster either way), but if you build the Pro-final guard, treat "Pro reference handling is currently unreliable" as a condition to re-verify, not a permanent law.
