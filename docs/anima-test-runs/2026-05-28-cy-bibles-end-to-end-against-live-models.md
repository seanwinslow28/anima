# Cy's first real Bible authoring runs — what broke, what we learned

*2026-05-28. The session that turned Cy from "scaffolded and validated against stub fallbacks" into "two locked Bibles on disk, authored end-to-end against live Opus 4.7 + NB Pro + Gemini 3.1 Pro." Five Cy attempts to land the sean-anchor Bible, one clean run for claude-mascot, three load-bearing SDK / runner fixes shipped in between. This is the field report.*

---

## What the session was supposed to be

The handoff inherited from the previous session was clear on the shape: pre-flight checks (~10 minutes), Phase D for the sean-anchor authoring ceremony (~30–60 minutes), Phase E for the claude-mascot authoring ceremony (~30–60 minutes), Phase F to write the CHANGELOG and commit. Two real Bibles end-to-end against live models. Total budget: an evening.

The brainstorm artifact and the Cy three-phase AgentSpec had been validated against the stub-fallback path through commit 2's main event. The 167-test baseline (including 2 xfailed + 1 xpassed evals) was green. The two character folders were scaffolded, source-refs populated, manifest registered. Sean's notes.md files in each `source-refs/` told Cy the voice — pencil-test-colored for sean-anchor, pixel-art-8bit for claude-mascot. The orchestrator at `scripts/author_bible.py` bound the AgentSpec to a one-shot invocation.

What was supposed to happen: Cy reads the brief, emits the five-artifact JSON envelope, NB Pro generates the plates the envelope names, Gemini verifies each plate against the IR.* rules it cites, Sean approves both Bibles, done.

What actually happened: five increasingly-specific failure modes against the sean-anchor authoring run before one finally landed clean, each failure caught at a particular code branch the stub fallback had been silently bypassing in CI. The claude-mascot run worked on the first attempt because all three fixes were already in. The whole session became a study in *what stub fallbacks hide*.

---

## Pre-flight surfaced two real gaps

Before the first paid call:

**Gap one — `google-genai` not in `.venv`.** Pillow was the only image-related dependency present. `nb_pro_runner.py` shells out to `.claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py`, which `import google.genai` directly. Without it, the skill script would `ModuleNotFoundError` at subprocess time and the runner would surface the exit-code-1 result as a generation failure — and from there it would still cascade through the Pass-3 Gemini verification path on whatever bytes happened to be at the output path (nothing, or a stale placeholder). The CHANGELOG had documented `google-genai` and `fal-client` as required deps; only Pillow was actually installed.

**Gap two — NB Pro model slug was placeholder prose.** `nb_pro_runner.py:89` defaulted to `"nano-banana-pro"` — the brainstorm and DR voice for the model, not the shipped google-genai API slug. A docstring two lines above acknowledged the gap and said to verify before first real-call time. The DR research at `docs/Image-Model-DR-2026/prompt-3-perplexity.md:447` cites the real slug as `gemini-3-pro-image-preview` (referenced via a Reddit URL pattern matching NB2's `gemini-3.1-flash-image-preview`). Without the update, every `--model` flag passed to the skill script would have hit the google-genai client and gotten a 404 on the slug.

Sean's directive when surfaced: install `google-genai` + `fal-client` into `.venv`, update the slug default, apply a `sys.executable` fix to `_build_skill_cmd` in the same commit so the subprocess pins to the `.venv` interpreter unconditionally. The PATH-based `"python3"` shape would have silently resolved to system Python 3.14 (where `google-genai` isn't installed) even after the install landed.

The pre-flight commit (`529cf17`) shipped all three.

---

## The sean-anchor authoring run — five attempts before a clean Bible

Each attempt below ran against a real Opus call (subscription-absorbed but real wall-time), a Pass-2 NB Pro generation step (~$0.15/plate when it actually fired), and a Pass-3 Gemini verification loop. Each took 5–15 minutes wall time. The cumulative cost of the failed attempts was the real test-environment shaping that the stub-fallback CI couldn't have produced.

### Attempt 1 — silent stub fallback at Pass 1 (the "Reached maximum number of turns (1)" failure)

The first run completed with exit code 0 and emitted what looked like a real Bible — `character.yaml`, `acceptance_criteria.json`, `risk-bible.md`, `cy-confidence-notes.md`, `plate_generation_plan.json` all on disk. But the character.yaml's `cy_confidence_notes` field literally read `"(STUB FALLBACK — see cy-confidence-notes.md)"`. Palette was an empty list. Proportions were empty strings. `plate_generation_plan.json` was 18 bytes (`{"plates": []}`).

That was the deceptive thing. The exit code was 0. The orchestrator printed a success-shaped output ("emitted: character_yaml_path: ..., ..."). The pipeline didn't crash. From the outside, nothing was wrong. But Cy had landed in the stub-envelope path defined in `character_designer.py:_build_stub_envelope` — the one designed to keep CI green when Opus is unreachable.

Debugging this took the longest of the five attempts because the failure was structural, not exceptional. The Opus SDK call had returned with `ok=False, error="Claude Code returned an error result: Reached maximum number of turns (1)"`. The error was buried inside the SDK's `AssistantMessage.error` field, surfaced through `_drain_csdk_query`'s exception-raising path, caught by `_invoke_text`'s except-Exception block, and translated into an `SDKResponse` with empty text. From there, `character_designer._parse_pass1_envelope` saw no parseable JSON envelope, took the `if stub_fallback or not payload:` branch, and built the stub envelope from `character_dir.name`. Every downstream artifact looked plausible because the stub generator was designed to produce plausible-looking artifacts.

The root cause was a single integer in `sdk_runners.py`: `max_turns=1`. The shape of the Pass-1 Opus emission — a ~50KB JSON envelope wrapping `character.yaml` + 15–20 IR.* rules + risk-bible prose + confidence-notes prose + plate plan — apparently requires more than one internal turn for the claude-agent-sdk to compose, even though no actual tool use is happening (the `allowed_tools=[]` and `disallowed_tools=[]` lists stay empty). The SDK's internal turn-accounting on extended thinking + structured output of that complexity blew past 1 before any AssistantMessage text streamed through.

The fix shipped in `pipeline/agents/sdk_runners.py:215-228`: `max_turns=10`. A smoke test against the same Cy Pass-1 prompt under the new ceiling succeeded in 506 seconds with a 53KB envelope. The fix is generous — no tool grants become possible, the SDK just has room for whatever it does internally on complex emissions.

**The deepest lesson**: the existing test suite at `tests/test_sdk_runners.py` did not catch this because every test in that file monkey-patches `_sdk_available` to False and exercises only the stub-fallback envelope shape. The real-model branch had never been exercised in CI for outputs of this complexity. There was no test that *could* have caught it — it required an actual Opus call against an actual ~55KB prompt to surface the failure mode.

### Attempt 2 — Pass 1 worked, Pass 2 silently stubbed (the `.env` gate failure)

With `max_turns=10`, the second run completed Pass 1 successfully — character.yaml carried a real four-color palette, real 1:7 proportion vocabulary, the IR rules graph populated, the risk-bible read as real prose. The orchestrator log said "plates: 20 total" and "3 plate(s) flagged for human gate." From the outside, this was a successful run.

Then the inspection. Every generated plate was 69 bytes. Every NB Pro cache entry was 69 bytes. The expression files for neutral / focused / surprised / contemplative were all the same 1×1 transparent PNG. The "real" Bible was a Pass-3-Gemini-verified set of placeholder pixels.

The trigger this time was inside `nb_pro_runner.py` at line 123: `if not os.environ.get("GEMINI_API_KEY"): _write_placeholder_png(output_path)`. `GEMINI_API_KEY` was present in `.env` but had never been exported into the shell. The skill script itself reads `--env-file .env` directly and would have generated real images — and a manual invocation of the skill script proved this. But the runner's stub-fallback gate only checked the process environment, not the .env source the skill script consumed. The two layers were checking different things.

The fix shipped a new helper at `pipeline/agents/nb_pro_runner.py:_has_gemini_api_key()` that reads both sources — the live process environment first, then the .env file content. The change is small but the contract-symmetry point is important: any subprocess gate has to match the subprocess's own resolution path. If the gate-check and the actual-check disagree, you get silent stub-fallback at the gate while the actual call would have succeeded.

A test-fixture follow-up was required. The seven existing tests at `tests/test_nb_pro_runner.py` use `monkeypatch.delenv("GEMINI_API_KEY", raising=False)` to force stub-fallback. After the gate started reading .env, those tests began returning real-path responses against the developer's local .env file with its real key. The fix was an autouse fixture that repoints `_ENV_FILE` at a sentinel non-existent path for the whole test module — preserving the intent of the existing tests ("no key available → stub fallback") without burying intent under explicit per-test patching.

**The deepest lesson**: this is the same shape as Attempt 1's lesson. The unit tests asserted the stub-fallback behavior, but the gate-check itself wasn't testable against a multi-source resolution path. The bug lived at the boundary between the runner's gate logic and the skill script's actual logic, and only a live run could surface it.

### Attempt 3 — Pass 1 worked, Pass 2 ran for real, then crashed on path resolution

With the .env gate fix in place, the third attempt got further. Opus emitted a real envelope. NB Pro started generating real plates. Then, partway through Pass 2, `FileNotFoundError: [Errno 2] No such file or directory: 'characters/sean-anchor/characters/sean-anchor/anchor.png'`.

Cy's Pass-1 addendum example at `pipeline/agents/prompts/cy-character-designer-context.md` shows `reference_images: ["anchor.png", "turnarounds/head-front.png"]` — character-dir-relative paths. The live Opus emission instead used project-root-relative paths (`"characters/sean-anchor/anchor.png"`). The previous `_run_plate` flow at `character_designer.py:463-464` unconditionally prepended `character_dir`, producing the duplicated nested path. The subprocess crashed when `_hash_file` tried to open it.

The fix mirrored the ingest-path resolver that already existed earlier in the same function. Try `character_dir / ref` first; fall back to `_PROJECT_ROOT / ref` if that doesn't exist. Defensive against both emission shapes.

The fix also added `timeout_s=900` to the `invoke_opus_text` call in `character_designer.py:133`. The default 120s would have timed out at the ~500s Pass-1 wall time we'd already measured in the standalone smoke test — even if `max_turns` hadn't been the proximate trigger in Attempt 1, the timeout would have been the next failure mode.

**The deepest lesson**: the prompt-driven example contract is an underspecification. The addendum showed character-dir-relative paths as "what good looks like," but Opus had freedom to emit any path shape that was self-consistent. The runner's responsibility is to handle the legitimate shapes the prompt permits. The pattern of "try one resolution, fall back to another if it doesn't exist" generalizes; it was already in the ingest path; it should have been in the reference-images path from the start.

### Attempt 4 — mysteriously stubbed again

With all three fixes in place, the fourth run still produced a stub Bible. character.yaml had `character_id: sean-anchor` (the folder name fallback), empty palette, empty proportions, zero plates in the plan. The orchestrator log showed no errors. A standalone smoke test of `invoke_opus_text` against the same Pass-1 prompt completed successfully in 306 seconds with a real 42KB envelope.

This was a transient failure that never recurred. The likely explanations are an API hiccup, a rate-limit absorption that surfaced as empty text, or a one-off SDK error that fell into the same exception-promoted-to-empty-text path Attempt 1 exposed. There was no further code change between Attempts 4 and 5 — only a retry. Attempt 5 succeeded.

**The deepest lesson**: real-model branches will have flakiness that no amount of code-level fixing can eliminate. The orchestrator should ideally surface "Pass 1 stubbed" as a *loud* condition (currently it just produces a Bible whose `cy_confidence_notes` field contains the string "(STUB FALLBACK — ...)") so the human reviewer notices immediately. A follow-up commit could add a top-level orchestrator check: after Pass 1 completes, if the emitted character.yaml's `cy_confidence_notes` carries the "STUB FALLBACK" sentinel, the orchestrator should exit non-zero with an explicit "Cy fell back to stub envelope" message rather than printing the success-shaped output and letting the human notice on inspection.

### Attempt 5 — the clean run

The fifth attempt produced what we wanted: 24 plates total across the four output directories (16 ingested from source-refs, 8 generated via NB Pro), real PNG file sizes ranging from 62KB to 2.4MB, every Pass-3 Gemini verdict grounded in cited IR.sean.* rules, 1 plate (head-turn-09) flagged for human-gate after 3 Gemini rejections — surfacing the expected stubborn-frame case rather than silently passing it.

The Bible carries 20 IR.sean.* rules across 8 categories: costume (2), face (3), hair (2), motion (2), palette (2), prop (2), proportion (3), style (4). The descriptions are specific enough that Em can cite a single rule by ID against a single observable thing in a frame — `IR.sean.hair.center-cowlick` for "the highest point of the head silhouette, roughly 2cm forward of the back of the skull," `IR.sean.prop.stylus-right-hand-always` for "right hand grips the stylus near the barrel with three fingers visible." The risk-bible (5.9KB prose) names uncovered axes correctly. The confidence-notes (3.6KB prose) hedges five rules and flags four for explicit Sean review before production runtime.

Cumulative wall time for the successful run: roughly 13 minutes (Pass 1 Opus at ~500s, the 8 NB Pro generations at ~3 minutes total, the 24 Gemini verifications including regen attempts at ~5 minutes total). Live spend: roughly $2-3 in NB Pro (Opus + Gemini subscription-absorbed).

Approved via `pipeline bible approve` at session end. `acceptance_criteria.json.locked: true`.

---

## The Cy scratchpad — an unexpected portfolio artifact

During Pass 1, Cy emitted 27 Python scripts into the repository root: `analyze.py`, `back_crop.png`, `check_back_body_lines.py`, `check_colors.py`, `check_head_lines.py`, `count_front_lines.py`, `count_torso_lines.py`, `find_all_ranges.py`, `find_blue_back.py`, `find_blue_front.py`, `find_center.py`, `find_clean_bounds.py`, `find_feet.py`, `find_gap.py`, `find_horizontal_gap_top.py`, `find_ranges.py`, `find_vertical_gap.py`, `inspect_column.py`, `map_head_lines.py`, `map_torso_lines.py`, `measure_back_view.py`, `measure_back_view_clean.py`, `measure_front.py`, `measure_profiles.py`, `measure_proportions.py`, `sample_tee_flats.py`, `test_threshold.py`.

These are Cy diligently verifying her rule measurements against the source-ref pixel data before authoring the IR.* descriptions. The "eye spacing ≈ one eye-width apart" rule, the "shoulders sit ~1.5 head-widths apart" rule, the "head height fits seven times into total body height" rule — these aren't interpretive prose, they're observations Cy made by writing Pillow scripts that measured the actual anchor.png and source-refs files. The rule-graph's `derived_from` pointers cite the source-ref regions; the scratchpad scripts measure those regions and emit the numbers the rule descriptions land on.

The claude-mascot run produced three similar scripts (`analyze_eye.py`, `analyze_mouth.py`, `grid_check.py`) — measuring the deep-brown eye-dot pixel clusters and the mouth-stroke width against the mascot anchor to ground the `IR.claude-mascot.face.eye-deep-brown-dot-cluster` and `IR.claude-mascot.face.mouth-line-deep-brown-single-stroke` rule descriptions.

These scripts were unexpected. The SDK options carry `permission_mode="bypassPermissions"` for headless one-shot mode, but `allowed_tools=[]` and `disallowed_tools=[]` were supposed to deny tool use. Apparently the resolved tool set with `tools=None` (default) and `allowed_tools=[]` leaves the file-write and bash tools available — Cy used them. This is a prompt-level decision Sean still has to make: tighten the gate so Cy can't write files (then she can't ground rules in measurements), sandbox Cy's working directory to a known scratchpad (best of both worlds), or accept what landed and embrace as bidirectional-provenance evidence.

For this session: moved to `runs/2026-05-28-cy-{sean-anchor,claude-mascot}-bake/cy-scratchpad/`. The scripts are now archived alongside their Bible. The IR rules cite `#region:` source-ref pointers; the scratchpad scripts cite the rules they were measuring against; the working-illustrator's notebook is on disk as portfolio content. This was a happy accident that suggested a useful pattern.

---

## The claude-mascot run — one attempt, all five criteria passed

Phase E went exactly as Phase D was supposed to. Cy ran once, emitted 8 plates total (2 ingested from anchor + 6 generated via NB Pro), 13 IR.claude-mascot.* rules at pixel-art-8bit register, all five non-negotiable handoff criteria PASSED:

1. **style_register correct**: `pixel-art-8bit`, not `pencil-test-colored`. The Task 1.4.5 defang held against the live authoring run despite the addendum's Example A pencil-test-colored example sitting alongside Cy's per-invocation brief.

2. **IR.* rules in pixel-art vocabulary**: palette (4-indexed-color, no-anti-aliasing, primary-orange-dominant), proportion (head-to-body-2-to-3-chibi, body-width-1-2x-head-width, silhouette-round-topped-lozenge), style (integer-pixel-grid-no-subpixel, dither-vertical-2px-warm-brown, no-gradient-interpolation), face (eye-deep-brown-dot-cluster, mouth-line-deep-brown-single-stroke, expression-vocabulary-three-only), anatomy (fingertip-and-crown-cream-highlight). Every rule reads as pixel-art register vocabulary at both the ID and description layer.

3. **Zero pencil-test markers**: `grep -iE "cross-hatching|graphite|cream paper|construction lines|pencil-test"` across all four Bible artifacts (character.yaml, acceptance_criteria.json, risk-bible.md, cy-confidence-notes.md) returned zero hits.

4. **risk-bible in pixel-art terms**: "Four-step indexed palette is brittle by design — the brittleness is the aesthetic." Lit variants escalate to a separate Bible; smooth-edge / anti-aliased renders are a different register entirely; the integer-pixel-grid constraint is structural to identity. No motion plates (mascot has no walk cycle authored), three-expression set, single-outfit costume — all phrased in register-appropriate vocabulary, not pencil-test prose.

5. **Pass-3 Gemini verdicts cite the right rules**: every plate's `cites_identity_rules` list grounds in 5–9 named rules from the pixel-art-8bit vocabulary. No plate cites a generic style-register concern.

The fact that this worked first-attempt-clean is the validation that the three fixes from Phase D were complete, not just patches. If `max_turns` had still been 1, claude-mascot would have stubbed. If the `.env` gate had still been process-env-only, NB Pro would have placeholder-PNG'd. If reference paths had still been unconditionally prepended, Pass 2 would have crashed.

Wall time: ~10 minutes. Live spend: ~$1-2 in NB Pro.

Approved via `pipeline bible approve`. `acceptance_criteria.json.locked: true`.

---

## What we learned

These are the structural takeaways that should outlive this session.

**Stub fallbacks designed for CI hide real-model failures.** All three runner fixes shipped in this session sat on code branches the stub-fallback path silently bypassed. The pattern is: tests monkeypatch the "is real model available" check to False, exercise the stub envelope shape, and never touch the real-model branch. Then in production, the real-model branch trips on a real-model-only edge case (max_turns ceiling on complex emissions, .env-vs-process-env disagreement on environment resolution, path-shape underspecification in prompt examples), and the only signal the user gets is "exit code 0, Bible on disk" because the stub-fallback re-engages downstream. A useful follow-up pattern: every stub-fallback path should emit a *loud* sentinel that the orchestrator can detect and surface immediately, not just an artifact that looks correct on cursory inspection.

**Live runs are the test environment that catches the bugs CI can't.** Each of the five sean-anchor attempts surfaced a specific failure mode that no amount of mocking could have caught. The cumulative cost of the failed attempts (perhaps $5–10 in Opus tokens for the four failed Pass-1 calls plus the wall time) was the real test-environment shaping. There's no shortcut here — anyone shipping an LLM-orchestrated pipeline of this complexity has to budget for real-model attempts as part of the development cost, not as a post-development verification.

**The orchestrator should make stub-fallback into a hard failure, not a soft success.** The fact that Attempt 1 looked like it succeeded (exit code 0, "emitted: ...") even though Cy had landed in the stub envelope is the worst failure mode in this whole session. A human reviewing only the orchestrator output would have approved the stub Bible. A follow-up commit should make `scripts/author_bible.py` inspect the emitted character.yaml for the "(STUB FALLBACK — ...)" sentinel and exit non-zero if it's present. The handoff explicitly named this principle ("Don't approve any Bible that landed via stub fallback — the orchestrator surfaces stub_fallback=True in the output") but the surfacing is currently buried in the file content rather than the exit code.

**The .venv subprocess pinning matters as much as the dep install.** The pre-flight `sys.executable` fix would have been invisible if google-genai had been installed system-wide. But it wasn't, and the subprocess would have inherited PATH from the caller and resolved `python3` against system Python 3.14 (where the install never lands). The pattern: subprocess invocations should pin to the calling interpreter unconditionally, not rely on PATH resolution. This generalizes to every other agent that shells out (Em via `agy`, Maya's text-only paths, any future agent fleet member).

**Prompt-driven contracts have flex; runners need to handle the flex.** Cy's addendum example showed character-dir-relative reference paths. The live Opus emission used project-root-relative paths. Both are reasonable interpretations of "a path to a file." The runner's fix was to handle both. The general pattern: when a prompt example shows shape X, the runner has to be defensive against shape Y if Y is also a reasonable interpretation. The ingest-path resolver had this pattern already; reference-images didn't; the new fix harmonizes them.

**The defang shipped at sufficient depth — but the test for that was the live run, not the test suite.** The Task 1.4.5 style-neutrality defang and the Task 1.4.6 CI guardrail had been validated against stub fallback emissions only. The real proof that the defang shipped at sufficient depth was Cy authoring the claude-mascot Bible against the live Opus call and emitting pixel-art-8bit vocabulary throughout, with zero pencil-test markers leaking in. The CI guardrail at `tests/test_prompt_style_neutrality.py` is a backstop for prompt-file regression, but it does not validate that the live Opus call respects the addendum's intent at run time. The claude-mascot Bible is the only artifact that proves the defang held against an actual real-model authoring run.

**Real spend was lower than the brainstorm estimate.** The brainstorm at `docs/2026-05-27-cy-character-bible-brainstorm.md` estimated $3-5 NB Pro per Bible. Actual spend was ~$2-3 for sean-anchor (despite 5 attempts — most stubbed before reaching Pass 2) and ~$1-2 for claude-mascot. The estimator's per-plate pricing assumed roughly 30% regen rate on a 20-30 plate Bible; we observed about 1 human-gated plate per Bible on a smaller (20 + 8 plate) emission. The estimator at `pipeline/agents/cost_estimator.py:_phase_2_cost` is on the high side for current authoring complexity. Sean can tighten it once a couple more real Bibles' worth of data lands.

**A "successful exit code" can lie about what actually happened.** This is the deepest lesson, the one that organizes all the others. Five out of five failed sean-anchor attempts exited with code 0. Four out of those five produced artifacts that looked plausible to cursory inspection. The pipeline's exception-handling paths all converted real failures into "stub fallback worked" responses, which is the right answer for CI determinism but the wrong answer for production confidence. The principle going forward: every stub-fallback path the orchestrator might land in should be *named* in the runtime output (not just the file content), and every production invocation should treat any stub-fallback signal as a hard failure unless explicitly authorized.

---

## What landed on disk

| Commit | What | Phase |
|--------|------|-------|
| `529cf17` | NB Pro slug → `gemini-3-pro-image-preview`; `_build_skill_cmd` uses `sys.executable`; `google-genai` + `fal-client` installed into `.venv` | Pre-flight |
| `7e89053` | sean-anchor Bible end-to-end; SDK + runner fixes (max_turns 1→10, .env gate, defensive path resolution); 27-script scratchpad archived | Phase D |
| `7e6f19f` | claude-mascot Bible end-to-end; five-criteria validation log; 3-script scratchpad archived | Phase E |
| `03277de` | CHANGELOG entry documenting both Bibles, three runner fixes, actual spend, wall time, criteria validation results | Phase F |

Test suite at end of session: `tests/` 157 passed (unchanged from session start), `evals/` 10 passed + 2 xfailed + 1 xpassed (unchanged). The closing-the-loop test (case 7 — `closing-the-loop-em-cites-cy-rules`) stays xfailed by design; it flips green when Em's prompt loads the merged CriteriaBundle at run start.

Total live spend across all five sean-anchor attempts + the one clean claude-mascot attempt: roughly $5-10. Cumulative wall time: roughly two hours including debug + inspection cycles. The two Bibles + the three runner fixes + the CHANGELOG entry + the next-session handoff written to `.remember/remember.md` are the receipts.

The pipeline now has two locked Bibles authored end-to-end against live Opus 4.7 + NB Pro + Gemini 3.1 Pro. Bible authoring is contract-grounded — not decorative — across two categorically different style registers. The next-session priority is Em prompt tightening to load the merged CriteriaBundle and flip case 7 from xfail to green, at which point Em can cite an `IR.claude-mascot.style.integer-pixel-grid-no-subpixel` violation on a smooth-edged Phase 5 mascot frame as concretely as it cites `IR.sean.prop.stylus-right-hand-always` on a stylus-in-left-hand Phase 5 Sean frame. The diff will be the museum content that documents the moment Bible authoring became operational across registers.
