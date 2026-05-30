# The claude-mascot pencil-register pivot — what broke, what we learned

*2026-05-30. The session that retired the pixel-art-8bit claude-mascot — which had failed on a reference gap — and re-authored it from scratch in the pencil-test-colored register against real multi-view art, baked on NB2, and ran the first two-character continuity probe the pipeline has ever seen. One clean Opus authoring run (after one false start that taught us a Python-3.14 lesson), a positive deviation from the plan that produced better plates than the plan asked for, two generation drifts caught and fixed at the human gate, and two latent tool bugs surfaced by going off the happy path. This is the field report. It is a companion to [`2026-05-28-cy-bibles-end-to-end-against-live-models.md`](2026-05-28-cy-bibles-end-to-end-against-live-models.md) — that session made Bible authoring operational; this one stress-tested it on a re-author + a second same-register character.*

---

## What the session was supposed to be

The kickoff was unusually well-specified: six phases, three human STOP gates, each phase its own commit. Retire the pixel mascot (archive, don't delete), stage the real reference art, re-author the Bible in the new register, bake the plates on NB2, run an exploratory two-character check, wrap. The 2026-05-29 production-bake post-mortem had already diagnosed *why* the pixel mascot had to go: a single flat anchor gave NB Pro nothing to infer new angles from, so its turnaround plates invented a standing biped. The pencil-test version closes that gap with a real five-view turnaround sheet (C-1), lives in sean-anchor's register, and is the actual Act 2 shoulder companion.

Two decisions from the prior research session were folded in as inputs: route the bake to **NB2** (`gemini-3.1-flash-image-preview`), not NB Pro, because editing/consistency work holds identity better there; and treat the broader template-emitter refactor as a follow-on, not this session's work. The plan honored both.

What was supposed to happen: archive, stage, flip the model default, author + approve the rule graph, bake plates that hold the box-creature form across angles, probe two-character continuity, wrap. What actually happened tracked the plan closely — but four things off the happy path are worth the writeup, and one of them was Cy being *smarter than the plan*.

---

## The four things that broke (and one that went better than planned)

### 1. The first authoring run vanished at 535 seconds with a zero-byte log

The first `author_bible.py` run was launched in the background with stdout redirected to a log file. Nine minutes later the process was gone, the log was **empty**, and not a single artifact had been written — `character.yaml` was still the May-28 scaffold template.

The puzzle was the empty log. A clean Python exception flushes a traceback to stderr on interpreter shutdown; an empty log after 535 seconds of runtime means the process was **killed by a signal before its block-buffered stdout ever flushed**. The proximate cause surfaced on the rerun: claude-agent-sdk on Python 3.14 emits a noisy async-generator teardown at the end of the Opus call —

```
RuntimeError: aclose(): asynchronous generator is already running
Loop <_UnixSelectorEventLoop ... closed=True> that handles pid 18495 is closed
```

— and on the first run that teardown happened to take the process down before Pass-1's atomic writes, with all the buffered "Pass 1 → Pass 2 → Pass 3" banner output lost to the kill.

The fix was operational, not code: rerun with `PYTHONUNBUFFERED=1 python -u`, fully detached (`nohup ... & disown`) and wrapped in `caffeinate -i` against idle sleep. Unbuffered, the log captured progress live; this time the teardown warning printed *after* Pass-1 had already written all five artifacts, so it was revealed as **noisy but harmless**. Pass 1 completed in ~790s with the full rule graph on disk.

**The lesson**: when you background a long unattended LLM run, never trust a buffered log. An empty log is not "nothing happened" — it can be "everything happened and the buffer died with the process." Run unbuffered from the first attempt so the first failure is diagnosable instead of mysterious. This is the operational cousin of the 2026-05-28 lesson that "a successful exit code can lie" — here, an *empty log* lied about a run that had genuinely done most of its work.

### 2. The turnaround plates came out as full-sheet copies — the regions sidecar didn't exist

This is the one where Cy was smarter than the plan, and the plan's infrastructure hadn't caught up to her.

The kickoff anticipated that Cy would **generate** the five turnaround angles and we'd check whether the form held. Instead, Cy's Pass-1 plate plan chose to **ingest** all five views as crops directly from the real C-1 turnaround sheet (`ingest:source-refs/turnaround-c1.png#region:front`, `#region:side`, …) and to *generate* only the two expressions. This is strictly higher fidelity: a crop of Sean's actual drawing has zero generation drift, where a generated turnaround is a hope. Cy read "the C-1 sheet has all five real angles" and reasoned "so crop them, don't redraw them." That's the right call, and it's documented in her risk-bible ("ingested at the pixel layer, not extrapolated… the angle-expansion gap is closed at the source").

But `#region:NAME` ingest crops require a `<sheet>.regions.json` sidecar mapping each region name to a crop box, and **no sidecar existed**. The runner's documented fallback fired exactly as designed: copy the whole sheet and flag `region_not_cropped` rather than ship a silent wrong crop. The tell was unmistakable — all five turnaround plates were byte-identical at 664,800 bytes (the full sheet), and their DINOv2 similarity-vs-anchor scores were all identical at 0.911.

The fix authored the missing sidecar by **detecting the five figure columns programmatically**: mask the terracotta pixels, find the cream valleys between the figures, and emit five fractional crop boxes. The re-bake then produced five clean, distinct crops (~80–114KB each, similarity now correctly *varying* per view, 0.81–0.92). The side-view crop even shows the circular nub-end-cap that became its own identity rule (below).

**The lesson**: the ingest-crop path's "fall back to a full copy and flag it" behavior — itself a fix from the 2026-05-29 session — worked perfectly, and that's *why* the failure was instantly legible (identical file sizes, identical similarity scores) instead of a silent wrong crop. But the plate plan and its required sidecar are authored in two different places (Cy's Pass 1 vs a hand-authored source-ref artifact), and nothing checks that a plan citing `#region:X` has a sidecar defining `X`. A cheap pre-bake validation — "every `#region:` referenced in the plate plan resolves in some `.regions.json`" — would have caught this before the bake instead of after.

### 3. The generated expressions drifted — and `bible iterate` couldn't steer the fix

The two generated expression plates both drifted, in the specific way the rule graph warns against. NB2 enlarged the mascot's two small graphite dot eyes into **large glossy cartoon eyes** (a violation `IR.claude-mascot.face.two-dot-eyes-with-brows` names explicitly), and the `neutral` plate additionally grew an **orange hair tuft on top** and let the ear/arm nubs **droop downward** instead of projecting horizontally. The form held — box body, four legs, terracotta, cross-hatch, cast shadow, no humanoid — but the face was wrong. Gemini correctly failed both.

The instinct was to re-roll via `bible iterate --reject neutral,curious --reason "…"`. Tracing the path first saved a wasted cycle: `iterate`'s `reject_reason` threads into the `invoke_nb_pro` **cache key** — which busts the cache and forces a fresh sample — but it **never reaches the NB2 prompt**. `_build_skill_cmd` builds the subprocess argv from `prompt` alone. So a bare iterate re-samples with the *identical* prompt; on a stochastic model that might land better or worse, but it is not *steered* by the correction.

The actual lever was the plate **intent**. We edited the `neutral` and `curious` prompts in `plate_generation_plan.json` to carry targeted anti-drift negatives — "keep the eyes as two small simple graphite dots, NOT large glossy cartoon eyes; no hair or tuft on top; nubs project horizontally, not drooping" — and re-baked. The changed prompt naturally produced a new cache key, and the re-roll landed: `neutral` → Gemini pass, `curious` → borderline, both visibly on-model with small dot eyes, no hair, horizontal nubs.

Separately, Sean's "the character has no hair" call was captured as a standing, enforceable invariant — a new rule `IR.claude-mascot.anatomy.no-hair` — so Em can cite it on any future frame, rather than the fix living only in a one-off prompt edit.

**The lesson**: `bible iterate` is advertised as the drift-fix tool, but its reject reason is currently a cache-busting nonce, not a steering signal. Re-rolling a stochastic generator with the same prompt is hoping, not fixing. Until the planned `_build_nb_pro_prompt` → template-emitter refactor wires reject reasons into the prompt, the real fix for a drifted generate-plate is editing the plate intent — and a recurring drift (NB2 reads the box-top as a head and reaches for hair/big-eyes) is worth promoting from a prompt patch to a Bible rule.

### 4. `bible mutate --new-version 1.3.0` broke criteria loading

Adding the `no-hair` rule the right way — audited, on a locked Bible — meant `bible mutate --force --actor sean --reason … --new-version 1.3.0`. It bumped the file, wrote the audit record, and reported success. The full test suite stayed green. Everything looked fine.

Then Phase 5's two-character merge check called `load_all_criteria` on the live manifest and raised: `ValueError: unsupported criteria schema version: 1.3.0`. The `version` field in `acceptance_criteria.json` is the **schema** version — `validate_criteria` gates it on a `1.0`/`1.1`/`1.2` allowlist via `version.startswith(...)`. `bible mutate --new-version` writes a *content* semver into that same field. `1.3.0` matches no schema branch, so the mutated Bible became unloadable. The 188-test suite missed it because every criteria test uses fixtures, not the live manifest's on-disk mascot file.

The fix restored `acceptance_criteria.json` to a plain regular file at `version: "1.2"` (adding a rule needs no schema bump; the 14-rule content is valid 1.2), matching how sean-anchor and Cy's original Pass-1 write store it, and dropped the symlink + versioned file the mutate had created. The two-Bible merge then loaded clean: 22 `IR.sean.*` + 14 `IR.claude-mascot.*`, zero collisions.

**The lesson**: `bible mutate` conflates a content semver (`--new-version`) with the schema-version field, and will break *any* locked Bible it touches until those are split. This is a real tool bug, flagged for the follow-on. The deeper point echoes 2026-05-28: a green suite that mocks the thing that broke is not coverage. There is no test that loads the real manifest's merged criteria — so a Bible can be committed in an unloadable state and CI stays green. That test should exist.

### The positive deviation, restated

It's worth separating the *failure* in §2 (missing sidecar) from the *good decision* that exposed it (ingest-crop the turnarounds). Cy's choice to ingest real crops rather than generate is the single best outcome of the session: the five turnaround plates are Sean's own art, on-model by construction, and Sean approved them with "perfect." The plan asked "will the generated angles hold the form?"; Cy answered "don't generate them — the real angles already exist." The lesson for the kickoff-writer: when a real multi-view sheet exists, ingest beats generate, and the agent may reach that conclusion before you do.

---

## The two-character first light

Phase 5 was the first time the pipeline loaded two real Bibles into one scene. Two things were exercised. The criteria merge — `load_all_criteria` over both Bibles — returned one `CriteriaBundle` of 36 entries (22 `IR.sean.*` + 14 `IR.claude-mascot.*`) with no ID collisions; per-character `IR.{id}.*` namespacing did its job. And one two-character frame, built through the editing-template **storyboard variant** (Sean's anchor + the mascot's anchor + A-7 for scale, one action, one shot, register held constant), generated on NB2.

The frame held against the A-7 ground truth on every axis: Sean recognizable with the stylus in his right hand, the mascot unmistakably the terracotta box-creature with no hair, the box sized to perch (≈ one head tall), and a single consistent pencil-test medium across both figures. It is a *probe*, not an Act 2 asset — but it proves the two-Bible path works end to end, and the findings note ([`2026-05-30-two-character-first-light.md`](2026-05-30-two-character-first-light.md)) scopes what a real cross-character continuity audit needs (per-character IR loading into one verdict, a relative-scale ratio rule, occlusion ordering, a shared-register check, pairing-placement invariants). `continuity_audit.py`'s CC01–CC08 remain Sean/Act-1-hardcoded; building the general system was deliberately deferred.

---

## What we learned

**Unbuffered-from-the-start is non-negotiable for long unattended runs.** The first authoring run cost ~13 minutes and produced zero diagnosable signal because the log was buffered and the process was killed. The rerun cost the same time and was fully legible because it was unbuffered. The marginal cost of `PYTHONUNBUFFERED=1 python -u` is zero; the cost of not using it is a mystery you have to reproduce. (And on Python 3.14, claude-agent-sdk's async-generator teardown is noisy-but-harmless — expect the `aclose()` RuntimeError in logs and don't chase it.)

**Ingest beats generate when the real art exists — and the agent may know that before the plan does.** The plan's whole Phase 4 anxiety was "will the generated turnarounds hold the box form?" Cy sidestepped it by cropping the real C-1 sheet. The five best plates in the session required no generation at all. Future kickoffs for a character with a real turnaround sheet should *assume* ingest-crops for the canonical angles and reserve generation for the views the references don't cover.

**The runner's "fall back and flag, never silently substitute" discipline pays off precisely when something is misconfigured.** The missing-sidecar failure was instantly diagnosable — five byte-identical files, five identical similarity scores — because the ingest path copies-and-flags instead of guessing. That same discipline (from the 2026-05-29 session) is what made a configuration gap a five-minute fix instead of a subtle wrong-crop that ships.

**A drift worth seeing twice is a rule, not a prompt patch.** NB2's tendency to read the box-top as a head (hair tuft) and to cartoonify small eyes (glossy enlargement) is a structural property of the model against this character, not a one-off. Promoting "no hair" to `IR.claude-mascot.anatomy.no-hair` means the next generator, the next critic, and the next session inherit the correction. Fixing it only in a plate prompt would have let it recur the moment anyone re-baked from the plan.

**`bible iterate`'s reject reason is a cache-buster, not a steering signal — know which of your "fix" levers actually reach the model.** Re-rolling a stochastic model with an unchanged prompt is gambling. The correction has to enter the prompt to steer the output. This is the most actionable finding for the follow-on refactor: wire reject reasons into the five-slot template's `{preserve_and_negative}` slot so `iterate` actually iterates.

**Green CI that mocks the boundary that broke is not coverage — twice now.** The 2026-05-28 session learned this about stub fallbacks hiding real-model branches. This session learned the same shape twice more: `bible mutate` wrote an unloadable schema version and the suite stayed green because criteria tests use fixtures; and `bible iterate`'s no-op-steering would pass any test that only checks "a new file was produced." The missing test in both cases is the same one: **load the real manifest's merged criteria and assert it parses.** That single test would have caught the mutate bug at commit time.

**The two-character path works, and the gap is the audit, not the generation.** Generation handled two anchors + a pairing reference in one frame without a continuity system existing. What's missing is the *checking* — a critic that grounds a two-subject verdict in two rule sets, with relative-scale and occlusion and shared-register invariants. That's a clean, scoped next session, not an open research question.

---

## What landed on disk

| Commit | What | Phase |
|--------|------|-------|
| `aa6b02e` | Land the 2026-05-30 NB2 editing-template research + the pivot kickoff/amendments/plan (dangling inputs) | Pre-flight |
| `b6419f3` | Archive the pixel-art-8bit Bible to `characters/_archive/` (history preserved) + README; flip manifest register → pencil-test-colored | Phase 1 |
| `e6c5506` | Stage C-B anchor / C-1 turnaround / A-7 pairing + author `source-refs/notes.md` | Phase 2 |
| `a61acd5` | Flip `invoke_nb_pro` editing-model default to NB2 (`gemini-3.1-flash-image-preview`) + backing test (187→188) | Phase 3.5 |
| `f7380eb` | Cy authoring run; approve the 14-rule pencil-test Bible (incl. the nub-side-view-endcap rule from Sean's review); criteria locked | Phase 3 |
| `fe06861` | Author the C-1 regions sidecar; plates-only bake on NB2 (5 ingested crops + 2 re-rolled expressions); add `no-hair` invariant | Phase 4 |
| `efe19e8` | Restore criteria to schema `version: 1.2` after `bible mutate --new-version 1.3.0` broke loading | Phase 4 fix |
| `aabd4a2` | Two-character first-light frame + continuity-scope findings note | Phase 5 |
| `9dbc047` | CLAUDE.md + CHANGELOG wrap (register pivot, NB2 default, mutate-tool bug note) | Phase 6 |

Test suite at end of session: `tests/` **188 passed** (187 baseline + 1 new `test_default_model_is_nb2_flash`), green before and after every commit. Live spend: subscription-absorbed Opus + Gemini; NB2 for ~4 generated plates across two bakes + one two-character frame, well under a dollar (NB2 is ~half NB Pro's cost). Cumulative wall time including the false-start run, the two bakes, and the debug cycles: roughly 75 minutes.

The pipeline now has **two locked pencil-test-colored Bibles in the same register**, a second character validated against live models, five shippable turnaround crops + two on-model expressions for the Act 2 shoulder companion, and the first evidence that two real Bibles compose into one coherent frame.

---

## How we should proceed

**Next, for the characters (Sean's call this session):** expand expressions and poses for *both* Bibles. The mascot ships with two expressions (calm, curious) by design-minimalism, but Act 2 will want more (alarm, delight, sleep, alert-perk), and the mascot has *zero* motion plates — no walk, idle, head-tilt, or perch-settle — which is the load-bearing gap for any Phase 6 mascot motion clip. sean-anchor would benefit from the same expansion pass. The pattern this session validated: where a real reference sheet exists, **ingest-crop it** (the five turnaround plates) rather than generate; reserve generation for what the references don't cover, and trait-lock the generated ones hard (small dot eyes, no hair) because NB2 will cartoonify and add hair if left unconstrained. Sean may prefer to *draw* the expression/motion source plates and have Cy ingest them, exactly as the turnarounds worked.

**Two tool bugs for the follow-on (the template-emitter refactor is the natural home for both):**
1. **`bible mutate` writes a content semver into the schema-version field** and breaks `validate_criteria`. Split content-version from schema-version, or have mutate refuse a `--new-version` that isn't a known schema version. And it currently writes the audit record without applying the field change to the rule content — the mutation is audit-only today.
2. **`bible iterate`'s `reject_reason` only busts the cache key; it never reaches the NB2 prompt.** Wire it into the five-slot template's `{preserve_and_negative}` slot so a reject reason actually steers the regeneration. This is the difference between `iterate` fixing a drift and `iterate` re-rolling the dice.

**One missing test that would have caught a real bug:** load the live manifest's merged criteria (`load_all_criteria(manifest)`) and assert it parses with no ID collisions. That single integration test catches both the schema-version break and any future Bible committed in an unloadable state — the fixture-only criteria tests cannot.

**The scoped next session is the cross-character continuity audit.** The two-character path generates cleanly; what's missing is the checking. Per the first-light findings note: per-character IR loading into one verdict pass, a relative-scale ratio rule, occlusion/who-occludes-whom, a shared-register consistency check, and pairing-placement invariants citable against an actual two-shot. `continuity_audit.py` CC01–CC08 are Sean/Act-1-hardcoded; this generalizes them.

**Still deferred, unchanged:** the 16BitFit-humanoid pixel-register pass (the cross-register validation the retired pixel mascot was meant to provide — now its own future session); the per-view-reference hard similarity gate; Em's closing-the-loop case 7; sean-anchor identity tuning. None were touched.
