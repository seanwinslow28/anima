# Cy the Character Designer — eval suite baseline

**Run date:** 2026-05-28
**Suite:** `evals/character_designer/runner.py`
**Result:** 5 passed, 1 xfailed, 1 xpassed

## Per-case results

| Case | Result | What it exercises |
|------|--------|-------------------|
| `sean-anchor-reproduction` | pass | The pencil-test-colored control case. Clean Pass-3 across all plates; 8 IR rules, 5 categories, style_register matches. |
| `claude-mascot-reproduction` | pass | The pixel-art-8bit validation case. The schema fits a second register cleanly; style_register=pixel-art-8bit is structurally enforced. |
| `gemini-flags-then-converges` | pass | The fail-then-pass regen path. Gemini flags plate 1; NB Pro re-called with reject_reason; final verdict pass. |
| `three-attempt-ceiling-hits-human-gate` | pass | The ceiling-hit path. Three consecutive Gemini fails on the same plate → plate status=human_gate_required; the Bible doesn't fail because of one stubborn plate. |
| `schema-validates-across-style-registers` | pass | The merged-CriteriaBundle case. Both Bibles load; `query_by_character` filters cleanly; no ID collisions. |
| `under-specified-source-refs-flags-risk-bible` | **xpassed** | Marked intentionally red, but the suite's mock conftest emits a satisfying Bible structure. Real Opus may produce different risk-bible specificity — track for the first real authoring run. |
| `closing-the-loop-em-cites-cy-rules` | **xfailed** | The structural novelty over the planner eval suite. Em runs for real against the deliberately-broken Phase 5 frame; asserts at least one `IR.sean-anchor.*` citation. Red because Em's prompt doesn't yet load the merged CriteriaBundle's IR.* entries — the diff that flips this green is the museum content. |

## What this baseline locks in

Five structural facts the suite verifies:

1. **The AgentSpec contract holds end-to-end.** Cy's three-phase loop (Opus authors → NB Pro generates → Gemini verifies) emits the five required artifacts and the AgentResult shape downstream consumers expect.

2. **The IR.* graph schema validates across two style registers.** Sean's pencil-test-colored Bible and Claude Mascot's pixel-art-8bit Bible both fit the same `acceptance_criteria.json` schema. The closed `style_register` vocabulary works as designed.

3. **The three-attempt ceiling per plate surfaces correctly.** Cases 3 + 4 exercise the regen-with-reject_reason path and the human-gate path respectively. A stubborn plate doesn't fail the whole Bible.

4. **The merged-CriteriaBundle path works.** `load_all_criteria(manifest)` reads multiple Bibles into one bundle, dedupes by ID, exposes `query_by_character(character_id)` filtering correctly.

5. **The closing-the-loop test is red on first land.** This is the structural novelty: case 7 ships intentionally red because the contract gap (Em's prompt doesn't load Cy's rules) is real. The xfail-to-green diff in a follow-up commit (when Em's prompt is tightened to load the merged CriteriaBundle's IR.* entries into context) is the museum content documenting *the moment Bible authoring became contract-grounded*.

## What this baseline does NOT cover yet

- **Real Opus + NB Pro + Gemini behavior.** All current cases mock the three runners. The first real authoring run (Tasks 1.10 + 1.11 in Sean's session) will reveal calibration issues the mocks can't surface: how specific Cy's risk-bible reads against under-spec source-refs; whether NB Pro's regen-with-reject_reason actually converges within three attempts; whether Gemini's verdict citations match Cy's IR rule IDs.
- **Pixel-content drift from source-refs.** Failure mode #2 in `failure-modes.md` names this; no case yet covers it. Adding when the real authoring run surfaces the mode.
- **Per-frame motion-plate correspondence.** Failure mode #3. Relevant once a third character authors motion plates with both source and derived halves; not yet on the suite.
- **Cross-piece consistency.** Sean's portfolio thesis says anima ships pieces across multiple registers. The schema-cross-register case (5) is one slice; the broader question — does Cy author internally consistent Bibles across 3+ characters with non-overlapping registers — needs more real authoring data.

## Reproduce

```bash
.venv/bin/pytest evals/character_designer/runner.py -v
```

Expected: 5 passed, 1 xfailed (closing-the-loop), 1 xpassed (under-spec is mock-satisfied; track against real Opus).
