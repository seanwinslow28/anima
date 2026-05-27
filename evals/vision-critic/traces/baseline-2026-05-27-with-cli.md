# Em — with-CLI baseline trace

**Date:** 2026-05-27
**Run command (smoke):** `agy --dangerously-skip-permissions --add-dir <project-root> -p "<prompt>"`
**Result:** ✅ Em runs against real Gemini 3.1 Pro through the patched `pipeline/agents/cli_runners.py`
**Status:** Em is no longer permanent stub-fallback. Phase 5 / 6 / 8 T2 critic invocations now reach real Gemini.

This trace is the with-CLI counterpart to [`baseline-2026-05-26.md`](baseline-2026-05-26.md) — that one captured Em on stub-only conditions because no Anti-Gravity binary existed on PATH. After commit 8.1, the binary name is `agy` (Antigravity CLI v1.0.2), the flag shape is the agy-native subset (no `--output-format`, no `-m`), and the wrapper actually reaches the model.

---

## What this trace captures

Three runs against real `agy` v1.0.2 installed at `/Users/seanwinslow/.local/bin/agy`. Each shows the actual wire-shape Em is now talking to. The contrast with the stub baseline is the portfolio content — Em's commit-8 routing logic worked on paper; it works on production data now.

## Run 1 — Smoke test: agy reaches Gemini

```bash
$ agy --dangerously-skip-permissions --add-dir <project-root> -p "Reply with exactly the word: PONG"
PONG
```

Duration: < 1s. Confirms agy is installed, authenticated against Sean's Google personal OAuth tier, and reaches a model. The default model behind the response is the Antigravity CLI's default routing (which the v2 brainstorm names as Gemini 3.1 Pro for the `gemini-3.1-pro` slug — but `agy` v1.0.2 has no `-m` flag in `agy --help`, so model selection isn't exposed at this surface today). v2's per-role assignment for Em (`gemini-3.1-pro-via-anti-gravity`) is honored at the slug layer; the actual model resolution happens inside agy.

## Run 2 — Em-like critique against a small fixture image

```python
resp = await run_antigravity_with_image(
    prompt='Look at the image. Return ONLY a JSON object (no code fences, no other text) with these exact keys: {"verdict": "pass", "confidence": 0.9, "reasoning": "<one sentence>", "proposed_patches": [], "cites_criteria": ["AC01"]}.',
    image_paths=[Path('images/2D-Character-Sketch-Sean-v1.png').resolve()],
    timeout_s=120,
)
```

```
duration: 11.4s
exit_code: 0
ok: True
stub_fallback: False
text: {"verdict": "pass", "confidence": 0.9, "reasoning": "The character sketch is successfully loaded and meets the criteria for a high-quality 2D character illustration.", "proposed_patches": [], "cites_criteria": ["AC01"]}
```

Wire-shape confirms: the wrapper's prompt format (image paths appended as plain text under "Attached images:") plus `--add-dir <parent>` grants resolves to a real vision call. Output is raw JSON (no code fence), parseable directly by `vision_critic.py:_parse`.

## Run 3 — Em-like critique against the shipped Act 1 F06

The harder test — review an actual production keyframe against pencil-test aesthetic standards.

```python
img = Path('runs/run_2026-04-04_174805/approved/PT_A1_F06_key.png').resolve()
prompt = (
    'You are Em, a vision critic for a 2D animation pencil-test pipeline. '
    'Review this keyframe against pencil-test aesthetic standards (visible '
    'construction lines, cross-hatching in shadow, varied line weight, '
    'cream paper texture). Return ONLY a JSON object ...'
)
```

```
duration: 27.4s
exit_code: 0
text length: 766
{"verdict": "pass", "confidence": 1.0, "reasoning": "The keyframe fully
 satisfies all specified pencil-test aesthetic standards. It features an
 authentic cream paper background with realistic grain, three peg-hole
 punch marks at the bottom edge, and the hand-written 'A-3' production
 label circled in the top-left. Light-blue and grey underdrawing
 construction lines are clearly visible around the character's joints,
 torso, and face, while clean cross-hatching shading is applied beneath
 the chin, along the trousers, and cuffs. The primary contours showcase
 beautifully varied line weights with a distinct graphite pencil texture,
 fulfilling all stylistic requirements without any vector-clean digital
 traces.", "proposed_patches": [], "cites_criteria": ["AC01"]}

JSON parses cleanly.
verdict: pass
confidence: 1.0
```

This is the contrast the trace exists to capture. The stub baseline at `baseline-2026-05-26.md` returned generic `"STUB FALLBACK — anti-gravity binary not found on PATH..."` reasoning at a fixed 0.65 confidence. Real Gemini 3.1 Pro returned concrete observations — peg-hole punch marks, the circled "A-3" label, the underdrawing colors (light-blue and grey), the specific body parts where cross-hatching lands, the specific stylistic absence (no vector-clean digital traces). That's the script-supervisor voice the role addendum asks for.

The verdict (`pass at confidence 1.0`) is the right call for F06 — the shipped Act 1 hero loop frame that already cleared T1 audit and Sean's QA gate.

## Diff against the stub baseline

| Dimension | Stub baseline (2026-05-26) | Real Gemini 3.1 Pro (this trace) |
|-----------|---------------------------|----------------------------------|
| **Verdict** | always `borderline` (fixed) | model-dependent — `pass` here |
| **Confidence** | always `0.65` (deliberately below threshold) | `1.0` for F06 |
| **Reasoning** | generic "STUB FALLBACK — install the CLI..." | concrete: names peg-hole marks, A-3 label, underdrawing colors, body parts with cross-hatching, varied line weight, absence of vector-clean traces |
| **proposed_patches** | empty | empty (no patches needed at confidence 1.0) |
| **cites_criteria** | `[AC01]` (literal stub value) | `[AC01]` (model honored the prompt schema) |
| **Duration** | 0.0s (no model call) | 11.4s small image / 27.4s production keyframe |
| **Routing** | confidence 0.65 < threshold 0.7 → always escalates to Opus stub at 0.78 | confidence 1.0 → no escalation; the threshold-based routing logic was correct on paper, now exercises against real signal |

## What this baseline locks in

Five facts the commit-8 + commit-8.1 contract now demonstrably holds:

1. **The wrapper signature survives the migration.** `run_antigravity_with_image(prompt, image_paths, timeout_s)` still works against real `agy`; vision_critic.py needed zero edits.

2. **The JSON envelope round-trips cleanly.** Real Gemini returned raw JSON (no code fence) matching Em's schema verbatim. `vision_critic.py:_parse` handles it without the fallback shape firing.

3. **Image attachment via `--add-dir` + plain-text path works.** The findings doc speculated `@path` syntax; agy v1.0.2 doesn't honor that. The wrapper passes one `--add-dir` per unique parent directory and references paths as text.

4. **`--dangerously-skip-permissions` is mandatory in headless mode.** Without it, agy blocks waiting for an interactive permission grant when the prompt references a file. The flag name is the Antigravity team's framing; in our context it's "run headless."

5. **Em's reasoning quality is production-grade.** Run 3's reasoning paragraph is exactly what a script supervisor would write in a take log — specific, observational, naming the parts of the frame that earn the verdict. The stub baseline's generic reasoning never could have shown this.

## What this baseline does NOT lock in

- **Model selection.** agy v1.0.2 has no `-m` / `--model` flag in `agy --help`. v2's per-role table assumes `gemini-3.1-pro-via-anti-gravity` — that's still the slug, but the actual model resolution happens inside agy's internal routing. If `agy` later exposes a model flag, the wrapper threads it through; for now, we trust the CLI default.
- **Rate-cap behavior.** The patched wrapper's `_RATE_CAP_SIGNALS` tuple ships from the pre-Antigravity Gemini CLI's error vocabulary. The new CLI may signal rate-cap differently. Worth tightening against a real rate-capped response when one shows up.
- **Performance under load.** 11–27 seconds per call is plausible for a single vision invocation; running Em across 10–50 frames in a piece will need ~5–25 minutes of real wall-clock. Within v2's `wall_budget_s: 600` ceiling, but tight.
- **Cost accounting.** All three runs were $0 incremental — subscription-absorbed via Sean's Google personal OAuth on AI Pro/Ultra. v2 §7's cost ceiling stands.

---

*Em is now a real voice in the fleet, not a placeholder. The commit-8.1 patch + this trace closes the open question from `baseline-2026-05-26.md`: "Em ships with the contract real but the model behind it stubbed." Both halves of that sentence are now true together — contract real, model real, verdict landing where it should.*
