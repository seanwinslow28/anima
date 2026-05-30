# The template-emitter follow-on — what broke, what we learned

*2026-05-30. The session that paid down the two tool bugs the claude-mascot pivot surfaced, generalized Cy's plate-prompt construction into the register-agnostic five-slot emitter, wired per-register model routing, and — the load-bearing move — landed the one integration test that would have caught the bug the pivot shipped. Six commits, test-first, one per coherent change, the suite green before and after every one (188 → 200). No live model was called; the locked Bibles were never touched. This is the companion field report to [`2026-05-30-claude-mascot-pencil-register-pivot.md`](2026-05-30-claude-mascot-pencil-register-pivot.md) — that session was the bake that found the bugs; this one is the fix, and it is deliberately the opposite kind of session: slow, mechanical, every change pinned by a test that asserts on the real boundary rather than a mock of it.*

---

## What the session was supposed to be

The pivot post-mortem closed with a tightly-scoped follow-on: turn `_build_nb_pro_prompt` into a register-parameterized template emitter (Amendment A), wire per-register NB2/NB-Pro routing and the `invoke_nb_pro → invoke_image_edit` rename (Amendment B), and fix the two latent tool bugs — `bible mutate` writing a content semver into the schema-gated `version` field, and `bible iterate`'s reject reason never reaching the prompt. The research and the decisions were already done; the job was to land them cleanly. The kickoff added a hard gate: plan in plan mode, present to Sean, proceed only on explicit approval.

The work decomposed into six pieces, and the order was itself a lesson the prior two sessions had taught. The first piece was not any of the fixes — it was the *safety net*. The recurring lesson across 2026-05-28 and 2026-05-30 was the same sentence twice: "green CI that mocks the boundary that broke is not coverage." The pivot shipped an unloadable Bible with a 188-test suite passing because every criteria test used fixtures and nothing loaded the live manifest's on-disk Bibles. So before touching a single fix, the plan landed the test that closes that gap, as the tripwire that guards the rest of the session.

What was supposed to happen: land the net, fix the two bugs at the mechanism (with the test that would have caught each), build the emitter, wire the routing, wrap the docs, push. What actually happened tracked the plan almost exactly — the interesting parts are three mechanism details the plan got *approximately* right and execution had to sharpen, one correction Sean made to the plan before approving it, and one latent sibling bug a single grep turned up.

---

## The things worth the writeup

### 1. The safety-net test passed on the first run — and that was the point

The first commit was `tests/test_live_manifest_criteria.py`: load the real `manifest.yaml` (not a fixture), merge every Bible's `IR.*` graph through `load_all_criteria`, assert it parses with zero ID collisions and that both `IR.sean.*` and `IR.claude-mascot.*` are present. It passed immediately.

That is not an anticlimax; it is the design. This test is a *regression guard*, not a red-to-green — the pivot's emergency fix (`efe19e8`, restoring the mascot criteria to schema `version: 1.2`) had already repaired the on-disk state, so the live manifest loads clean today. The test's job is to make sure it *stays* that way: if any future `bible mutate`, hand-edit, or merge ever writes a Bible into an unloadable state, this is the test that goes red at commit time instead of three phases later when something calls `load_all_criteria` for real. The pivot learned this lesson the hard way — the schema break surfaced only when Phase 5's two-character merge tried to load both Bibles. Landing the net first means the rest of the session ran with the tripwire armed.

The one wrinkle worth recording: the test rewrites the manifest's `criteria_sources` Bible paths to absolute (rooted at the repo) before calling `load_all_criteria`, so it is independent of pytest's working directory. The relative paths in the manifest resolve against CWD, and a test that only passes when run from the repo root is a test that fails in CI for the wrong reason.

**The lesson**: the most valuable test in a session is sometimes the one that does not change color. The tripwire's value is entirely in the future failures it will catch — and it covers not just the bug we fixed this session but any unloadable-Bible state anyone introduces later. Write the integration test that loads the real artifact, and land it first.

### 2. The `bible mutate` fix had a second, quieter bug hiding behind the loud one

The headline bug was the schema-version conflation: `--new-version 1.3.0` wrote `1.3.0` into the `version` field that `validate_criteria` gates on a `1.0/1.1/1.2` allowlist, making the Bible unloadable. The fix decoupled the two — the schema `version` stays `1.2`, and `--new-version` now records a separate top-level `content_version` field the loader ignores.

But writing the test surfaced the quieter bug the pivot post-mortem had flagged in passing: `mutate` was *audit-only*. It bumped the version, wrote the audit record, printed success — and never applied the field change to the rule content. The mutation that was supposed to edit `IR.claude-mascot.anatomy.no-hair`'s description would have written an audit line claiming the edit happened while the rule sat unchanged on disk. The test for the fix had to assert three things, not one: the field changed *on the rule*, the schema version stayed loadable, and the content version recorded separately. Only asserting "it loads" would have left the audit-only bug live.

The fix also makes an unknown `--target` a hard error (rc 1) rather than a silent no-op — mutate now finds the criterion by `id`, edits the named field, re-validates the whole graph before writing, and writes back in place with no symlink/versioned-file dance (the symlink mechanism is exactly what `bump_version` created and the pivot had to undo). `bump_version` itself was left alone because Maya's plan/brief flow still uses it — which turned out to matter (see §5).

**The lesson**: a bug report names the symptom that hurt, not necessarily every defect in the code path. "mutate writes a bad version" was the symptom; "mutate never applied the change at all" was sitting right next to it. The test that pins the fix has to assert the *whole* contract — the change is applied, the file stays valid, the audit is honest — or it pins half a fix.

### 3. The §3 fix needed two wires, not one — and the test for "it reaches the prompt" is what found the second

The plan's reading of post-mortem §3 was: `reject_reason` busts the cache key but never reaches the prompt, so wire it into the `{preserve_and_negative}` slot. Correct, but incomplete. There are two distinct paths a reject reason travels, and the emitter refactor only fixed one of them automatically.

The Pass-3 regenerate path (a Gemini fail inside `_run_plate`) was straightforward: rebuild the prompt with `reject_reason=verdict_envelope["reasoning"]` instead of reusing the original `prompt_text`. But the `bible iterate` path is different — the iterate CLI writes a narrowed plan with a plate-level `reject_reason`, and `_run_plate` reads that on the *initial* generate of the re-run. Threading it into the prompt was easy. The catch surfaced when the test asserted on two things: that the reason appears in the emitted prompt *and* that the cache key is busted. The initial-generate `invoke_image_edit` call did not forward `reject_reason` to the runner at all — so the prompt would carry the correction but the cache would happily return the stale plate, and the steering would never run. The fix was a one-line addition (`reject_reason=plate_reject` on the initial call), but it only got written because the test asserted on the cache-bust as well as the prompt content.

**The lesson**: the pivot's §3 finding was "the reason reaches the cache key but not the prompt." The real shape was subtler — on the iterate path, the reason reached *neither* until both were wired. Writing the test the way the post-mortem demanded ("assert on the emitted prompt, not merely a changed cache key") is what forced the discovery that the iterate initial-generate path needed the cache-bust too. The post-mortem's own prescription, taken literally, found the gap the plan's prose had glossed.

### 4. The module-load ordering trap — hit twice, caught instantly both times

Twice this session, the suite went from green to a collection-time `NameError` the moment a constant was introduced. `_run_plate` gained two new parameters with default values — `style_register: str = _DEFAULT_REGISTER` and later `generation_model: str = _NB2_FLASH`. Default argument values are evaluated at function-definition time, which is module-import time. Both constants had been defined *below* the class, next to the clause library and the model table where they are conceptually at home. So the import blew up before any test ran: the default referenced a name that did not exist yet.

The fix both times was to hoist the constant above the class — `_DEFAULT_REGISTER`, then `_NB2_FLASH` and `_NB_PRO` — and delete the duplicate definition below, leaving a comment explaining *why* they live at the top (default-arg evaluation order) so the next person does not "tidy" them back down next to the table they belong with.

**The lesson**: this is a small, recoverable trap, and the reason it cost almost nothing is that the test suite caught it at collection time on the very next run. That is the tight feedback loop the whole test-first discipline buys. The deeper note for the next refactor: a constant that is *used* next to a data table but *referenced* as a default argument has two homes, and the default-argument home wins. Put it at the top, comment the why.

### 5. One grep turned up a sibling bug — and we left it, on purpose

When Sean reviewed the plan, one of his three notes was a question: does Maya's `plan mutate` share the same schema-version landmine? The fix scoped cleanly to `bible mutate` and left `bump_version` for Maya's flow — but if `plan mutate` also routes a `--new-version` through `bump_version` into a schema-gated field, the identical unloadable-criteria bug lives there too.

One grep confirmed it. `pipeline/cli/plan.py:246` calls `bump_version(criteria_path, new_version=new_version)`, which writes straight into the `version` field. It is partially masked — a content semver like `1.2.0` survives because `"1.2.0".startswith("1.2")` is true — so the break only fires for an off-allowlist major like `1.3.0` or `2.0.0`, which is exactly the value that broke the mascot Bible. And the new tripwire only covers the brief path when the manifest sets `criteria_sources.brief_file`, which is currently empty — so Maya's surface is not under the net today.

We did not fix it. It is out of scope for a bible-focused session, the right fix is a shared-primitive decision (decouple `mutate_plan` the same way, or harden `bump_version` itself to refuse an off-schema version and protect both callers at once), and folding it in would have widened a clean six-commit session into something harder to review and revert. It is queued in the plan's "out of scope" section, in the CHANGELOG, in CLAUDE.md's Cy row, and in the handoff.

**The lesson**: when you fix a bug at one call site, grep for the primitive's other callers before you call it done. The fix here was correct to scope narrowly, but "correct to scope narrowly" and "the sibling bug does not exist" are different claims — name the second one explicitly so the next session can pick it up instead of rediscovering it in a future bake.

### The correction Sean made before approving — the one that mattered most

The plan's first draft claimed the refactor was "behavior-preserving by construction for pencil-test-colored." Sean caught it in review and rejected the framing: it is not behavior-preserving, and that distinction matters. The new pencil emit is deliberately *richer* than the old `_build_nb_pro_prompt` — it adds the `ONLY CHANGE` idiom, the full preserve clause (cream paper, cross-hatch, "do not render monochrome"), and a standing style token to *every* plate. That is the approved template spec — it is literally worked Example 1 from the research doc, the prompt that would have prevented the `focused` monochrome drift — so it is the right change. But it is a *change*, and the substring tests pin the new clauses' presence, not equivalence to the old output.

The honest framing went into the plan, the CHANGELOG, and the handoff: this is a prompt upgrade, the first live bake on the new emitter is its validation point, and adding standing prose to every prompt is the exact surface the prompt-dominance lesson warns about. The saving grace — and the reason it is the right kind of added prose — is that it is anchor-reinforcing register/preserve guidance, not character re-description that competes with the anchor. If a future bake shows drift traceable to the added prose, the move is to trim the clause library, not revert the structure.

**The lesson**: do not let a plan claim an equivalence it is not enforcing. "Behavior-preserving by construction" is a strong claim with a specific meaning — that the output is identical — and the tests here assert something weaker and truer (the right clauses are present). Saying so plainly is what tells the next baker to *watch the first bake* rather than assume the refactor was a no-op.

---

## What we learned

**The integration test that loads the real artifact is the highest-leverage test in the suite — land it first.** Two sessions in a row learned that fixture-only coverage hides the bug that actually ships. This session acted on it: `test_live_manifest_criteria.py` was commit one, before any fix, and it now guards not just the schema-version break but any future unloadable-Bible state. The cost was one small test; the coverage is every `load_all_criteria`-shaped failure from here forward. The pattern generalizes — for any artifact the pipeline reads at run start, there should be one test that reads the *real* one, not a mock of its shape.

**Test-first is what made a coupled, three-file refactor safe to do inline.** The emitter, the reject-reason wiring, and the model routing all touched `character_designer.py` in overlapping regions, and the rename rippled across two test files. None of it was scary because the suite ran green between every step and went red the instant an edit broke something (the module-load trap, twice; the monkeypatch-target rename). The 188 → 200 progression is twelve new assertions, each pinning one behavior, and the count going up by exactly the expected amount at each commit was the signal that nothing silently regressed.

**A bug report names the symptom, not the defect set — assert the whole contract.** The `bible mutate` fix would have been half-done if the test only checked "it loads," because the audit-only bug (the change never reached the rule) was hiding behind the loud schema-version bug. The reject-reason fix would have been half-done if the test only checked the prompt, because the iterate cache-bust was a second wire. In both cases the test that asserted the *full* intended behavior — not just the absence of the reported symptom — is what found the second defect.

**Scope a fix narrowly, then name what you did not fix.** The `bible mutate` fix correctly left `bump_version` alone for Maya's flow, and the session correctly did not balloon into fixing `plan mutate` too. But "scoped narrowly" is only safe if the sibling bug is written down where the next session will see it. One grep found it; four sentences (plan, CHANGELOG, CLAUDE.md, handoff) queued it. That is cheaper than a future bake rediscovering it.

**The rename's cost was almost entirely in the tests, and that is fine.** `invoke_nb_pro → invoke_image_edit` is a one-line change in the runner plus a deprecation alias, but it touched ~30 references across two test files (imports, call sites, monkeypatch targets). Renaming the production symbol means the monkeypatch target `pipeline.agents.character_designer.invoke_nb_pro` no longer intercepts the call, so every patch site had to move in lockstep. This is expected churn for a deliberate rename, not a sign the rename was wrong — but it is a reminder that monkeypatch-by-string couples tests to symbol names, and a rename is the moment that coupling comes due.

**The honest framing is worth more than the optimistic one.** Sean's correction — "this is a prompt upgrade, not a no-op" — is the single most important sentence to carry out of this session, because it is the thing that turns the first live bake from a rubber-stamp into a real validation. A plan that claimed equivalence would have invited the next baker to skip the check. The corrected framing tells them exactly what to watch: did adding standing prose to every prompt reintroduce the drift the terseness lesson warned about?

---

## What landed on disk

| Commit | What | Phase |
|--------|------|-------|
| `bee3647` | Safety-net tripwire — `test_live_manifest_criteria.py` loads the real manifest, asserts merged `IR.*` criteria parse with zero collisions | 1 |
| `fe2969f` | `bible mutate` fix — edits the target rule in place, keeps schema `version` at 1.2, `--new-version` → separate `content_version`, unknown `--target` errors | 2 |
| `6eedc43` | Register-parameterized five-slot emitter — `_build_plate_prompt` + `_REGISTER_CLAUSE_LIBRARY` (six closed registers); Cy authors only `{variation}`; prop path unchanged; Cy addendum paragraph | 3 |
| `8088972` | `bible iterate` reject-reason reaches the prompt — threads into `{preserve_and_negative}` on both initial-generate and Pass-3 regenerate, and busts the cache key; pinned by a test that asserts on the emitted prompt | 4 |
| `30f96c8` | Per-register model routing — `_resolve_plate_model` / `_REGISTER_MODELS` (NB2 editing default; NB Pro painterly-final seam); manifest per-character override; `invoke_nb_pro → invoke_image_edit` rename + deprecation alias | 5 |
| `1ae945c` | Wrap — lifted the ⚠️ CLAUDE.md mutate caution, documented the emitter as prompt-construction source of truth + the routing + the rename; flagged the queued Maya sibling bug | 6 |

Test suite at end of session: `tests/` **200 passed** (188 baseline + 12 new), green before and after every commit. No live model spend — this was a mechanism session; the locked sean-anchor and claude-mascot Bibles and their approved plates were never read or re-baked. The plan, the six commits, the updated CLAUDE.md + CHANGELOG, and the handoff at `.remember/remember.md` are the receipts. Branch `feature/maya-planner-and-em-live` pushed through `1ae945c`.

The pipeline now has one home for plate-prompt construction — the register-agnostic five-slot emitter — that Phase 3 storyboarding and Phase 5 Flo can draw from instead of reinventing the structure; per-register model routing with NB2 as the editing default and a documented (not built) NB-Pro painterly-final seam; a `bible mutate` that actually mutates and stays loadable; a `bible iterate` whose reject reason steers the model instead of gambling; and — the quiet structural win — a tripwire that loads the real manifest, so the next Bible committed in an unloadable state goes red at commit time instead of three phases downstream.

---

## How we should proceed

**The first live bake on the new emitter is the validation that this session deferred.** Every change here was verified by emitted-prompt assertions, never by re-baking — deliberately, to keep the locked Bibles byte-untouched. That means the new pencil emit (richer prose on every plate) has not yet met a real NB2 call. The next expression/motion-plate expansion pass for sean-anchor or claude-mascot is that validation: watch whether the added standing prose holds the form or reintroduces drift. If it drifts, trim the clause library; do not revert the structure. This is the open question the honest framing names.

**Fix the Maya `plan mutate` sibling bug — as a shared-primitive decision, not a copy-paste.** `pipeline/cli/plan.py` still routes `--new-version` through `bump_version` into the schema-gated `version` field. The cleanest fix protects both callers at once: harden `bump_version` to refuse a `new_version` whose major.minor is not a known schema version, or give `mutate_plan` the same content-version decoupling `bible mutate` now has. Extend the tripwire to cover the brief path once `criteria_sources.brief_file` is populated. Small, scoped, its own commit.

**Build the NB-Pro painterly-final guard when — and only when — a consumer lands.** `_resolve_plate_model(final=True)` routes watercolor/photoreal/3d finals to NB Pro and is unit-tested, but `_run_plate` never takes that branch because no Pro-routed character exists. When the first painterly-register character is authored, that is the moment to build the reference-fidelity guard (the cheap "were the references actually used?" check + auto-regenerate the forum teams built) — and the moment to re-verify the NB Pro multi-reference regression, which was operational in Feb/Mar 2026 and may be patched by now. Do not build the guard against a hypothesis; build it against a character.

**The cross-character continuity audit remains the scoped next session, unchanged.** The pivot's two-character first light proved the generation path; the gap is still the checking — per-character `IR.*` into one verdict, a relative-scale ratio rule, occlusion ordering, a shared-register check, pairing-placement invariants. `continuity_audit.py`'s CC01–CC08 are still Sean/Act-1-hardcoded. Nothing this session touched that surface; the scope from [`2026-05-30-two-character-first-light.md`](2026-05-30-two-character-first-light.md) stands.

**Still deferred, unchanged:** the 16BitFit-humanoid pixel-register cross-validation pass (now with the emitter ready to prove register-agnosticism on a real second register); the per-view-reference hard similarity gate; Em's closing-the-loop case 7; sean-anchor identity tuning; the repo rename. None were touched, and the emitter refactor makes the first of these cheaper than it was — the template is built to take a new register as a row, not a rewrite.
