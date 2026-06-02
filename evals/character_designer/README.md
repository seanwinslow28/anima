# Cy — character-designer eval suite

A small eval suite for anima's Phase 2 character designer. Seven cases at first landing, grounded in the two real Bibles authored end-to-end during commit 2 (sean-anchor pencil-test-colored + claude-mascot pixel-art-8bit), plus the closing-the-loop test that is intentionally red on the first day and flips green when Em's prompt is tightened to load Cy's rules into context.

---

## What this evaluates

Cy the Character Designer runs once per character in a three-phase loop:

  Pass 1 — Opus 4.7 authors `character.yaml` + the `IR.{character_id}.*` graph + `risk-bible.md` + `cy-confidence-notes.md` + `plate_generation_plan.json` (text-only).

  Pass 2 — Nano Banana Pro generates plates per Cy's plan (image; per-plate cache; ingest from source-refs or generate via NB Pro per plate.source).

  Pass 3 — gemini-3.5-flash (via the Gemini API transport, `run_gemini_api_with_image`) verifies every plate against the IR.* rules it cites (vision). Three-attempt ceiling per plate; ceiling-hit surfaces `human_gate_required` in plate_results. (Was agy, whose backend-default Flash was mislabeled "3.1 Pro"; routed to the API transport 2026-06-02 — A2 model-provenance fix.)

The eval suite verifies seven things:

1. **Bible reproduction across registers.** Sean's pencil-test-colored Bible and Claude Mascot's pixel-art-8bit Bible both reproduce against the same schema. The closed `style_register` vocabulary works as designed.

2. **Regen-with-reject_reason path.** Gemini flags a plate; NB Pro re-called with the reject_reason threaded in; cache key invalidates; fresh generation runs; Gemini re-verifies. The convergence path is testable.

3. **Three-attempt ceiling.** Three consecutive Gemini fails on the same plate surface `human_gate_required` in `plate_results` without failing the whole Bible. The Bible's robustness against one stubborn plate is testable.

4. **Schema validates across style registers.** Both Bibles load into one merged CriteriaBundle via `load_all_criteria(manifest)`. `query_by_character(character_id)` filters correctly; no ID collisions; the v1.2 schema's IR.* namespace works as the closed-vocab structural fix the synthesis §5 thesis demanded.

5. **Under-specified source-refs surfaces risk-bible gaps.** Cy authors against a bare-anchor fixture; the risk-bible names the gaps explicitly. (Marked intentionally red — the mock conftest passes; tracking for real-Opus calibration.)

6. **The closing-the-loop test.** The structural novelty over the planner eval suite. Em runs for real against the deliberately-broken Phase 5 frame with the merged CriteriaBundle loaded; the case asserts Em's `cites_criteria` list contains at least one `IR.sean.*` entry. **Green as of the em-reference-images workstream (2026-06-01)** — Em's prompt now surfaces the merged CriteriaBundle's `IR.sean.*` rules (`vision_critic._criteria_block`), so the reference+criteria-loaded critic cites a Bible rule against the broken frame. The xfail→green diff is the museum content documenting *the moment Bible authoring became contract-grounded*.

7. **The clean-markdown invariant.** Cy's prose artifacts (`risk-bible.md`, `cy-confidence-notes.md`) carry zero box-drawing characters. The Bible CLI renders boxes; Cy emits clean prose. Enforced at `CharacterDesignerNode.run()` via `_enforce_clean_markdown()` — re-verified per-case via the schema check.

---

## Why we evaluate this

Three reasons, layered on top of commit 3b's planner-suite rationale:

1. **The Bible is the cross-phase invariant.** Every Phase 5 frame Em verdicts implicitly cites the Bible's IR.* rules. If Cy's schema drifts, Em's verdicts unmoor. The suite is the structural backstop at the rule-authoring layer; the closing-the-loop test is the structural backstop at the rule-citation layer.

2. **The closing-the-loop test is the museum content.** Pre-fix red → post-fix green when Em's prompt is tightened to load the merged CriteriaBundle's IR.* entries is the diff that documents *the moment Bible authoring became contract-grounded* per the v2 synthesis §5 thesis. The xfail → pass arc IS the portfolio narrative — *validators cannot recover taste that was absent at generation time*, applied at the T2-critic-cites-Bible-rules layer.

3. **The two-register validation is the structural commitment.** Sean's portfolio thesis depends on anima being a 2D animation pipeline, not a pencil-test pipeline. The two Bibles + the schema-cross-register case + the style-neutrality guardrail at `tests/test_prompt_style_neutrality.py` together prove the closed `style_register` vocabulary works across categorically different aesthetic registers, not just one.

---

## How to run

```bash
.venv/bin/pytest evals/character_designer/runner.py -v
```

Expected baseline: 5 passed, 1 xfailed (closing-the-loop-em-cites-cy-rules — the structural xfail-to-green arc), 1 xpassed (under-specified — tracking for real-Opus calibration; mock conftest happens to pass).

Re-run after Em's prompt is tightened to load the merged CriteriaBundle's IR.* entries — case 7 should flip from xfail to pass. The diff (the prompt change + the green test) is the museum walkthrough's portfolio narrative.

---

## What we've learned (baseline)

See [`last-run.md`](last-run.md) for the per-case results and the five structural facts the baseline locks in. See [`failure-modes.md`](failure-modes.md) for the observed failure-mode taxonomy (5 modes named; each with surface symptom + how the suite catches it + fix vector).

---

## Provenance

This suite is the structural fix at the source synthesis §5 demands, operationalized at the Bible-rule-authoring layer. The eval-suite template is lifted from `evals/planner/` (commit 3b) — same `cases.yaml` schema, same conftest fixture-builder pattern, same mocked-runner shape in `runner.py`, same red/xfail discipline. The closing-the-loop test is the structural novelty introduced here that commits 8b (vision-critic eval suite, when it lands as `evals/vision_critic/runner.py`) and 9b (cli-critic eval suite) will mirror.

The two Bibles this suite reproduces (sean-anchor + claude-mascot) are the real artifacts authored in Tasks 1.10 + 1.11 during Sean's authoring session — the eval suite's `mocked_responses` are the contract; Sean's real authoring run is the validation that the contract matches reality.

The discipline canon: Hamel Husain *"Your AI Product Needs Evals"* (evals as inner loop), Shreya Shankar *"Eval-Driven Development for Modern AI Systems"* (eval-as-spec), Anthropic *"Demystifying Agent Evals"* (failure modes from real production beat imagined ones), the v2 brainstorm-v2 §2.1 (Cy as missed pinnacle phase), the v2 change-map §7 (eval-suite template established in 3b; mirrored in 8b + 9b + this one).
