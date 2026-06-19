# Cowork Prompt — Cy post-mortem (visual fidelity) + agent-fleet audit + Anima rename plan

**Created:** 2026-05-29
**For:** A fresh Cowork session (analysis + structured ideation; NOT an implementation session).
**Workstream:** Diagnose why Cy's emitted Bible plates aren't faithful to the source-ref characters, audit Maya and Em for regression, scope supplementary research, and plan the project rename `sw-portfolio-animation-pipeline → anima` across MacBook Pro + GitHub + Mac Mini.
**Reads as:** Studio-manual voice, prose where reasonable. Sean's tonal directive — *"I don't like it when the docs feel like it was strictly made for the terminal. We're making art. It should feel free."*

---

You're picking up the anima project after Cy authored two real Bibles end-to-end against live Opus 4.7 + Nano Banana Pro + Gemini 3.1 Pro on 2026-05-28. The test report at [`docs/anima-test-runs/2026-05-28-cy-bibles-end-to-end-against-live-models.md`](../../anima-test-runs/2026-05-28-cy-bibles-end-to-end-against-live-models.md) covers what shipped — five failed sean-anchor attempts surfaced three real runner fixes (max_turns 1→10, .env gate dual-source check, defensive path resolution); the sixth attempt landed clean; claude-mascot Bible authored first-attempt-clean as validation that the Task 1.4.5 defang held against live Opus. Two locked Bibles on disk. 167-test baseline preserved.

What the report didn't address — and what Sean caught on visual inspection: **the emitted Bible plates have similarities to the source-ref characters but aren't faithful to them.** Poses turn out well. Identity drift in specific markers (face shape, hair specifics, body proportion, costume detail) is present across multiple plates. The plates pass Gemini's Pass-3 verification because Gemini grounds against the IR.* rule descriptions Cy wrote, not against the source-ref pixels themselves — so an inferior plate that nominally satisfies the rule's prose can pass while looking categorically different from Sean's anchor.

Sean's instinct on the fix shape: NB Pro needs to receive the anchor image and the turnaround sheet during EVERY plate generation call as multi-reference inputs, not lean primarily on the text prompt to describe the character. The contract supports this (`invoke_nb_pro(reference_images=...)` already takes a list), and Cy's Pass-1 emission does specify reference_images per plate — but something between Opus's emission, NB Pro's API call, and the actual generation is losing identity fidelity. This session diagnoses where, and produces the fix plan.

This is an analysis + brainstorm session. No code changes. The deliverable is a structured diagnostic doc + an implementation prompt that the next Claude Code session will execute. Plus a scoped rename plan as a separate workstream.

## Read these binding docs first, in this order

Don't skip ahead. The test report comes first because it's the most recent ground truth.

1. [`docs/anima-test-runs/2026-05-28-cy-bibles-end-to-end-against-live-models.md`](../../anima-test-runs/2026-05-28-cy-bibles-end-to-end-against-live-models.md) — the test session's field report. Names what broke during runner debugging and what shipped. Does NOT address visual fidelity — that's the gap this session fills.
2. [`templates/bible/source-refs-checklist.md`](../../../templates/bible/source-refs-checklist.md) — the contract Sean signed when populating `source-refs/` for each character. This is the ground truth for what Cy was supposed to consume during Pass 1.
3. [`PHILOSOPHY.md`](../../../PHILOSOPHY.md) — the engine truth: *"if the loop plays smoothly and the character is recognizably itself in its intended medium, it ships."* The "recognizably itself" half is what's at stake.
4. [`CLAUDE.md`](../../../CLAUDE.md) — anima project manual, current state.
5. [`docs/2026-05-27-cy-character-bible-brainstorm.md`](2026-05-27-cy-character-bible-brainstorm.md) — the design lock for Cy. The synthesis §5 thesis (*"validators cannot recover taste that was absent at generation time"*) applies to identity references too, not just style register.
6. [`docs/Image-Model-DR-2026/SYNTHESIS.md`](../../Image-Model-DR-2026/SYNTHESIS.md) §1.4 ("Pencil aesthetic preservation is an unsolved benchmark") and §4 (the layered identity-defense pattern: style-lock LoRA + multi-reference conditioning + negative prompting). The report names multi-image conditioning as the structural fix; this session validates whether Cy is using it correctly.
7. [`pipeline/agents/character_designer.py`](../../../pipeline/agents/character_designer.py) — specifically `_run_plate` at line 442 and `_build_pass1_prompt` at line 214. Trace the actual reference_images flow from Opus emission through NB Pro invocation.
8. [`pipeline/agents/nb_pro_runner.py`](../../../pipeline/agents/nb_pro_runner.py) — `invoke_nb_pro` at line 81 + `_build_skill_cmd` at line 238. Confirm that reference_images actually reach the skill script's `--reference` flag.
9. [`pipeline/agents/prompts/cy-character-designer-context.md`](../../../pipeline/agents/prompts/cy-character-designer-context.md) — Cy's role addendum. Specifically the JSON envelope schema at line 27 (`reference_images` field) and the "What good looks like" Example A + B reference-image lists. What did Sean's prompt teach Cy about reference_images?
10. [`runs/2026-05-28-cy-sean-anchor-bake/`](../../../runs/2026-05-28-cy-sean-anchor-bake) and [`runs/2026-05-28-cy-claude-mascot-bake/`](../../../runs/2026-05-28-cy-claude-mascot-bake) — the actual run directories from the shipped Bibles. The `plate_generation_plan.json` files inside name exactly what reference_images Opus emitted per plate.

## Your job this session — six phases

### Phase 1 — Visual audit: side-by-side comparison (~60-90 min)

Use the `Read` tool on the PNG files directly — it surfaces images so you can compare them visually in conversation. For each character, work through systematically:

**For `characters/sean-anchor/`:**
1. View `characters/sean-anchor/anchor.png` — the canonical source identity reference.
2. View `characters/sean-anchor/source-refs/turnaround-1.png` and `turnaround-2.png` — the canonical turnaround sheets.
3. View `characters/sean-anchor/source-refs/head-turn/head-turn-{1..9}.png` — the canonical head turn library.
4. View `characters/sean-anchor/source-refs/walk-cycle/source.png` + `derived-v1.png` + `derived-v2.png` — the canonical motion library.

Then view the emitted plates in this order (or whatever exists on disk — list `characters/sean-anchor/turnarounds/`, `characters/sean-anchor/expressions/`, `characters/sean-anchor/motion_plates/`):
- Each generated turnaround (front, 3-quarter, profile, back) vs the canonical turnaround sheet's same angle
- Each generated expression vs the head-turn library (which carries the canonical face/expression vocabulary)
- Each generated motion plate vs walk-cycle source/derived

For every comparison, write a one-paragraph assessment naming **specifically** what drifted. Not "the face looks different" — *"the eye spacing widened roughly 15%, the jaw lost the slight asymmetric chin curve, the hair lost the center cowlick's forward 2cm offset"*. The IR.sean.* rules already name the load-bearing markers; use them as the diagnostic vocabulary. If a plate fails IR.sean.hair.center-cowlick visually but Gemini passed it, that's a finding.

**For `characters/claude-mascot/`:** same flow against `source-refs/claude-mascot-{1,2,3}.png` plus `anchor.png`. The pixel-art-8bit register makes drift more visible — palette shifts, integer-pixel-grid breaks, dithering-pattern variations are quantifiable.

The output of this phase is a structured **plate-by-plate drift table** for each Bible, with columns `target_path / source_ref_compared / drift_severity (none|minor|moderate|severe) / specific markers that drifted / IR.* rule(s) the drift violates / Gemini's verdict for this plate`. The last column is the load-bearing one — if Gemini passed plates where you see severe drift, the Pass-3 verification contract is failing in a specific way the runner doesn't currently catch.

### Phase 2 — Trace WHY: from Opus emission to NB Pro generation (~30-45 min)

Read the on-disk plate plans + cache keys to reconstruct what actually happened during Pass 2.

1. **Read `runs/2026-05-28-cy-sean-anchor-bake/.../plate_generation_plan.json` (and the claude-mascot equivalent).** For each plate Cy emitted with `source: "generate"`, capture the `reference_images` list Opus specified. Count: how many references per plate? Were they always the anchor + a turnaround? Were they sometimes empty? Did the list match the addendum's example pattern (anchor.png + turnarounds/head-front.png)?

2. **Cross-check against `nb_pro_runner.py:_build_skill_cmd` line 238.** Confirm the cmd-list construction passes `--reference <p1> <p2> ...` for each reference. Then check `.claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py` (skill script) — does it actually pass reference images to the `google.genai` client's `generate_content` call as multi-modal inputs? Or does it stuff the path as a string into the prompt? The behavior here is load-bearing.

3. **Check the cache keys** at `runs/.../cache/nb_pro/*.png` against the cache_key construction in `nb_pro_runner.py:_compute_cache_key`. Are the reference image hashes part of the key? If they are, that confirms references were processed at hash time. If the keys are stable across plates that should have had different reference images, something is funny.

4. **Inspect one generation directly.** Pick one plate that drifted in Phase 1, find its NB Pro cache entry, and trace: prompt text → reference images list → cache key → output PNG. If you can, manually re-run the skill script (`python3 .claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py "..." --reference anchor.png turnaround-1.png --output /tmp/test.png --model gemini-3-pro-image-preview --env-file .env`) with the same inputs and see if the output drifts the same way. If a hand-invocation with the SAME inputs produces a more faithful plate, Cy's invocation differs from yours in a way worth finding. If it produces the same drift, NB Pro itself is the limitation and the fix is upstream (different model, custom LoRA, or different prompt construction).

The output of this phase is a **root-cause hypothesis** — one of (a) Cy's Opus emission specified insufficient references; (b) the runner correctly passes references but the skill script drops them; (c) NB Pro receives references but its identity preservation across multi-image conditioning is weaker than the brainstorm assumed; (d) something else surfaces in the trace. Each has a different fix shape.

### Phase 3 — Audit Maya + Em for regression (~20-30 min)

Quick sanity check that the existing agents still behave as designed. The Cy work was structurally extensive; some of the changes (max_turns 1→10 in `sdk_runners.py`, the .env gate dual-source check in `nb_pro_runner.py`) live in shared infrastructure that Maya and Em depend on.

1. **Maya.** Run `.venv/bin/pytest tests/test_planner.py tests/test_plan_cli.py tests/test_criteria*.py -v`. Expect all green. Spot-read `pipeline/agents/planner.py:_phase_1` to confirm the three-phase Opus→Sonnet→resolution loop hasn't drifted. Confirm the `max_turns=10` lift doesn't break Maya's three-call ceiling (Maya's ceiling is on the agent-side counter, not the SDK-side turn count — but verify).

2. **Em.** Run `.venv/bin/pytest tests/test_vision_critic.py tests/test_cli_runners.py -v`. Expect all green. Confirm Em's standing-context defang from Task 1.4.5 didn't soften the failure-mode prose so much that Em now passes everything. Read the latest baseline trace at `evals/vision-critic/traces/baseline-2026-05-27-with-cli.md` and check whether a fresh run against an Act 1 frame produces verdicts of similar specificity.

3. **The closing-the-loop eval (commit 2b case 7) is still xfailed.** That's expected. The diff that flips it to green is Em's prompt tightening to load the merged CriteriaBundle's IR.* entries — separate workstream noted in the test report. Don't fix it in this session; flag it as the natural next-implementation-session work after the Cy fix lands.

The output of this phase is a **regression report**: green/yellow/red on Maya and Em.

### Phase 4 — Supplementary research (~30-60 min)

Three questions to research using the tools you have available — `WebSearch`, `mcp__workspace__web_fetch`, plus shell-invocable harnesses at `code-brain/agents-sdk/scripts/gemini_dr.py` (Gemini DR Max) and `code-brain/tools/llm-council/` (multi-vendor council via OpenRouter, including Perplexity). Pick the right tool per question — heavy multi-target compound questions go to Gemini DR Max; single-shape lookups go to WebSearch + web_fetch.

**Q1 — NB Pro (gemini-3-pro-image-preview) multi-image conditioning best practices.** Is the recommended pattern "anchor + 1-2 angle references"? "Anchor + full turnaround sheet as a single multi-character image"? "Anchor + per-angle reference"? The Image-Model-DR SYNTHESIS §2 names NB Pro as accepting "up to 14 refs" — is that real, and how do practitioners pack references for character consistency? Look for Reddit threads in r/StableDiffusion or community blog posts from May-June 2026 specifically on NB Pro identity work.

**Q2 — Alternatives if NB Pro's identity preservation is the limiting factor.** What's shipped recently that's better at character consistency from references? Imagen 4 / Imagen 4 Pro? GPT-Image-2 with the new multi-image coherent-set feature (named in Image-Model-DR §3)? FLUX.2 with multi-ref conditioning? Self-hosted FLUX.1 Kontext [dev] + a custom character LoRA trained on Sean's 30 approved Act 1 frames (Image-Model-DR Config C, Experiment 1)? Look specifically at multi-image identity-lock benchmarks, not just text-to-image quality.

**Q3 — Pencil-test specifically as the hard case.** Sean's pencil-test register has a documented gap (Image-Model-DR SYNTHESIS §4 — "Pencil aesthetic preservation is an unsolved benchmark"). What's shipped in the May-June 2026 window for hand-drawn / non-photoreal / cream-paper-grain preservation in multi-image conditioning? Has ByteDance Lance landed community workflows? Has anyone published a NB Pro custom-LoRA pattern that's tuned for pencil-test? Differential Diffusion + Qwen + multi-image — any ComfyUI ports?

Each question's answer should land in the diagnostic doc as a one-paragraph synthesis with source citations. The goal isn't to pick a fix yet — it's to know what options exist before the synthesis phase chooses.

### Phase 5 — Synthesis: what worked, what didn't, the fix plan (~45-60 min)

Write the diagnostic + fix doc at `docs/2026-05-29-cy-visual-fidelity-post-mortem.md`. Studio-manual voice. Structure:

1. **What worked.** The five-attempt debug saga from the test report is portfolio content — runner robustness landed under load. Two locked Bibles. The defang held against live Opus. The closed `style_register` vocabulary validated across two registers. The orchestrator + cache layer + scratchpad + audit trail all shipped.

2. **What didn't work.** The visual fidelity gap. The plate-by-plate drift table from Phase 1. The Gemini-verification-doesn't-catch-pixel-drift finding. The named root cause from Phase 2.

3. **The structural fix.** Based on Phase 2's root cause + Phase 4's research. Each candidate fix gets a one-paragraph treatment: scope, blast radius, cost, expected effect on identity faithfulness. Likely candidates (let the analysis surface the right one):

   - **Tighten Cy's Pass-1 prompt to always emit anchor + N angle references per generate plate.** Smallest blast radius. Lands as a prompt-file edit. The addendum's Example A + B already gestures at this; the brief is to make it non-negotiable in the role contract.
   - **Tighten the runner to inject anchor + canonical references unconditionally,** regardless of what Opus emits. The runner becomes the source of truth for "what references seed every plate." Larger blast radius — changes the contract layer — but most robust against future bias.
   - **Add a Pass-2.5 pixel-similarity check** between the generated plate and the source-ref it was supposed to match. CLIP similarity or a structural similarity index applied before Pass 3 fires. Doesn't fix identity drift; surfaces it loudly so Gemini's pass doesn't mask it.
   - **Switch generation tier for Bible authoring.** If NB Pro's multi-image conditioning is structurally weak (Phase 4 finding), the routing decision changes. Imagen 4 Pro / GPT-Image-2 multi-ref / self-hosted FLUX + custom LoRA become candidates per the Image-Model-DR routing table. Highest blast radius — changes the model assignment in v2 §6 — but if NB Pro is the limit, no amount of prompt-tightening recovers it.
   - **Train a character LoRA per Bible.** Image-Model-DR Experiment 1 — one Sunday afternoon, ~3hrs total on a 4090, $0 marginal cost after training. The Bible's `flux_lora_seed_plates` field anticipates this. Highest leverage, biggest dependency on Sean's hardware availability.

4. **Recommended fix sequence.** Probably "smallest blast radius first" — tighten Cy's prompt, see if it solves the problem, escalate to runner-level reference injection if not, escalate further to model swap or LoRA training only if the upstream fixes don't recover. Each step is a discrete commit.

5. **Implementation prompt.** Save a paste-ready continuation prompt at `docs/2026-05-29-cy-visual-fidelity-fix-implementation-prompt.md` that the next Claude Code session executes. Same structure as the earlier Cy prompts (binding docs, three-phase work plan, working-pattern constraints, verification commands).

### Phase 6 — Anima rename plan (~20-30 min, separate workstream)

The project's name changes from `sw-portfolio-animation-pipeline` to `anima` per the lock at `docs/2026-05-24-pipeline-v2-change-map.md` §5 ("Directory rename deferred to public-repo creation time so git history stays clean during the transition"). With two real Bibles on disk + 167 green tests + the agent fleet meaningfully present, this is the right window — but it's mechanical work with its own risk profile (every hardcoded path breaks if missed), so it deserves a scoped plan, not an inline edit.

Write the rename plan at `docs/2026-05-29-anima-rename-plan.md`. Cover three workstreams:

1. **MacBook Pro local rename.** `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline/` → `/Users/seanwinslow/Code-Brain/anima/`. Sequence: stop any running processes referencing the old path, `mv` the folder (single rename, preserves inode + git history), re-clone `.venv` if any tooling caches absolute paths, restart any IDE pointing at the old path. Find every hardcoded path with `grep -rn "sw-portfolio-animation-pipeline" .` and audit each — most should be relative paths that survive the rename, but `agents-sdk` references in `code-brain/` carry absolute paths.

2. **GitHub rename.** Repository settings → rename. GitHub auto-creates a redirect from the old URL. Existing clones (Mac Mini, any other machines) need `git remote set-url origin <new-url>`. CI / Actions pointing at the repo by name update automatically; ones pointing by URL need manual fix.

3. **Mac Mini rename + sync.** Find where the project lives on the Mac Mini (likely a clone for the LDR / vault-synthesizer / vault-critic infrastructure to read from). Rename the local folder + update the git remote. Confirm no scheduled agent in `agents-sdk/schedules/` reads from the old path — `grep -rn "sw-portfolio-animation-pipeline" /Users/seanwinslow/Code-Brain/code-brain/` is the audit shape.

For each workstream: a checklist with verification commands. Plus a section on what to update INSIDE the renamed folder:

- `CLAUDE.md` — every `sw-portfolio-animation-pipeline` reference + paths in the file map
- `pyproject.toml` / `setup.cfg` if a project name is declared
- `.env` if it carries absolute paths
- `manifest.yaml` if any block points at absolute paths
- README files
- Docs that cross-reference each other by path

The rename is its own commit (probably `rename: sw-portfolio-animation-pipeline → anima`). Tests stay green post-rename or the rename rolls back. The recommended timing: AFTER the visual-fidelity fix ships, not before — the fix is the more time-sensitive workstream.

## Working pattern + constraints

- **No code changes this session.** Analysis + brainstorm + planning artifacts only. Phase 5's diagnostic doc and Phase 6's rename plan are the outputs; the next Claude Code session executes them.
- **Studio-manual voice in every artifact.** The diagnostic post-mortem reads like a working studio's "what happened on the shoot" debrief, not a postmortem of a CI failure. The rename plan reads like an opinionated runbook, not a sysadmin checklist.
- **Visual evidence over speculation.** Phase 1 is the load-bearing phase. If you can't see the drift, you can't write the diagnostic. View the actual PNGs side by side. The IR.* rules are your shared vocabulary — *"IR.sean.hair.center-cowlick visually violated on `expressions/contemplative.png` despite Gemini's pass at confidence 0.94"* is the format.
- **Don't redo the Image-Model-DR research.** It already covered NB Pro / NB2 / GPT-Image-2 / FLUX / Qwen / LoRA training options through mid-May 2026. Phase 4's job is to find what shipped in the May-June window that the existing synthesis didn't catch, not to rebuild the existing synthesis.
- **The rename is a SEPARATE deliverable** from the visual fidelity work. Don't conflate. The fix plan ships first; the rename ships when timing allows.
- **`AskUserQuestion` for any cross-decision that splits two ways.** If Phase 5's synthesis surfaces a real fork (e.g., "tighten prompts vs. swap model"), ask Sean before locking the recommendation.

## End-of-session deliverables

1. **`docs/2026-05-29-cy-visual-fidelity-post-mortem.md`** — the diagnostic + fix plan. Five sections per Phase 5.
2. **`docs/2026-05-29-cy-visual-fidelity-fix-implementation-prompt.md`** — paste-ready prompt for the next Claude Code session. Mirrors the structure of the earlier Cy implementation prompts.
3. **`docs/2026-05-29-anima-rename-plan.md`** — the scoped rename plan covering MacBook Pro + GitHub + Mac Mini.
4. **CHANGELOG entry** covering all three artifacts.
5. **Optional: `PORTFOLIO-GOLD.md` entry** if the visual-fidelity finding has portfolio-grade shape — Sean's call. The "Gemini passes plates with drift because rules are prose, not pixels" pattern is structurally interesting if it generalizes, and it probably does.
6. **All artifacts presented via `mcp__cowork__present_files`.**

## What this session doesn't cover

- The actual code fixes. The implementation prompt sets them up; the next Claude Code session executes.
- Em's prompt tightening to flip the closing-the-loop case to green. Separate workstream. Flag it in the diagnostic doc as the natural follow-up but don't scope it here.
- Commit 5 (Draft → Pro tier escalation), commit 6 (Museum + Mo persona), commit 9 (T3 stack). All pending; out of scope.
- Bake-offs from v2 §8 (T2 critic shoot-out, Sage tier ablation, etc.). Out of scope.

## Start

1. Read the binding docs in the listed order. The test report is the most recent ground truth.
2. **Phase 1 — visual audit.** Load PNG files with the `Read` tool. Compare side by side. Build the drift table. This is the load-bearing phase; budget time for it (~60-90 min).
3. **Phase 2 — trace the WHY.** Read plate plans on disk; cross-check the runner code path; manually re-run one generation if useful.
4. **Phase 3 — Maya + Em regression check.** Run their test suites; spot-read the agent files.
5. **Phase 4 — supplementary research.** Three questions, right tool per question.
6. **Phase 5 — synthesis.** Diagnostic doc + implementation prompt for the fix.
7. **Phase 6 — rename plan.** Separate deliverable; ~20-30 min.
8. **CHANGELOG entry + present files.**

Net wall-clock estimate: 4-6 hours of focused work, mostly in Phase 1's visual audit and Phase 4's research. The rename plan is the smallest phase but worth doing in this session so it's queued for whenever the timing works.

---

*Two Bibles on disk. Pipeline works end-to-end. Identity fidelity is the next mountain. Diagnose what's keeping the plates from being recognizably Sean (and recognizably Claude Mascot) in their intended medium, then ship the smallest fix that closes the gap. The engine truth is the engine truth — if the loop plays smoothly AND the character is recognizably itself, it ships. We've got the loop; now we need the character.*
