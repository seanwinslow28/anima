# Cy the Character Designer — failure-mode taxonomy

*Observed failure modes from real production + named cases the suite anticipates. Each entry: surface symptom → how the eval suite catches it → fix vector. Add new entries when a real authoring run surfaces a mode the suite missed.*

---

## 1. identity-rule-too-generic-to-cite

**Surface symptom:** Em receives a Phase 5 frame to verdict, opens Cy's IR.* rules in the merged CriteriaBundle, and can't ground a verdict because the rule's `description` field reads like interpretive prose ("Sean looks like Sean") rather than a testable assertion ("stylus is in right hand, never visible in left"). Em downgrades to `pass` rather than `borderline` with a citation, and the structural lock dissolves — a Bible whose rules can't be cited is a decorative artifact, not a contract.

**How the suite catches it:** Case 7 (closing-the-loop-em-cites-cy-rules). Em is invoked for real against the `deliberately-broken-phase-5-frame.png` fixture with the merged CriteriaBundle loaded. The case asserts Em's `cites_criteria` list contains at least one `IR.sean.*` entry. Shipped intentionally red on commit 2b's first day; **flipped green in the em-reference-images workstream (2026-06-01)** when Em's prompt was tightened to surface the merged CriteriaBundle's `IR.sean.*` rules (`vision_critic._criteria_block`).

**Fix vector:** (1) Cy's Pass-1 Opus prompt — name the specificity requirement explicitly in the role addendum's non-negotiables. (Already shipped in `pipeline/agents/prompts/cy-character-designer-context.md`'s "specific enough that Em can ground a verdict in them" line, but Cy may still drift on a real authoring run.) (2) Em's prompt — tighten to load the merged CriteriaBundle's IR.* entries into context with the call structure ("here are the IR rules for the character in this frame; cite the ones you observe drift on"). The diff that flips case 7 green IS this fix.

---

## 2. plate-passes-gemini-but-drifts-from-source-refs

**Surface symptom:** Gemini's Pass-3 verdict on a generated plate is `pass` at high confidence, but Sean reviews the Bible and the plate visibly doesn't match the source-refs (wrong shirt color, slightly wrong hair shape). Cy's IR rule constrains palette by role but not by hex value; Gemini honors the loose rule but the pixel content drifts.

**How the suite catches it:** Not yet directly — case 1 (sean-anchor-reproduction) covers the clean path but doesn't pixel-diff Cy's generated plates against the source-refs. This is a real production failure mode that would surface during the real authoring run in Sean's session (Tasks 1.10 + 1.11). When it does, add a case fixture that uses real source-refs + a real NB Pro response shape and asserts the palette-IR rule names hex values explicitly.

**Fix vector:** Cy's Pass-1 prompt — strengthen the palette IR rule guidance to require hex values with ±tolerance bounds in the description (the claude-mascot fixture shows the shape — "Primary orange `#E89B6B` (skin + body fill, ±10 RGB units tolerance)"). The cy-character-designer-context.md preamble's "What good looks like" Example B carries this shape; verify Sean's real authoring run reproduces it for sean-anchor's palette rules.

---

## 3. motion-plate-source-derived-mismatch

**Surface symptom:** Cy's plate plan generates a `motion_plates/walk-cycle/derived/` frame against an IR.sean.motion.* rule, but the source line-art (`motion_plates/walk-cycle/source/`) and the derived rendering represent different motion phases (source shows mid-step; derived shows full-step). Em flags continuity drift between consecutive motion frames at T2-Phase-6 critique time, but the citation can't disentangle "the Bible is internally inconsistent" from "the generated motion frame drifted from the Bible."

**How the suite catches it:** Not yet — would need a case fixture that wires per-frame correspondence checks across the source/derived split. Adding when the real claude-mascot motion-plate authoring run lands (claude-mascot doesn't have motion plates in commit 2; this case becomes relevant when the third character's Bible is authored with both source and derived motion plates).

**Fix vector:** Cy's Pass-1 plate plan format — extend the plate entry schema to carry an optional `motion_phase` field that ties each plate to a specific phase of the motion cycle. The runtime check at plate generation enforces per-frame correspondence.

---

## 4. em-cannot-cite-cy-rules-at-T2-critic

**Surface symptom:** The structural-fix-at-the-source synthesis §5 names the failure mode directly: *validators cannot recover taste that was absent at generation time.* Em's Phase 5 verdict on a frame says "looks fine" because Em's prompt doesn't carry the Bible's identity rules; Cy's Bible is decorative.

**How the suite catches it:** Case 7 (closing-the-loop-em-cites-cy-rules) IS the regression test for this exact mode. Ships intentionally red on commit 2b's first day because Em's prompt doesn't yet load the merged CriteriaBundle. The xfail-to-green diff in a follow-up commit (when Em's prompt is tightened) is the museum content documenting *the moment Bible authoring became contract-grounded*.

**Fix vector:** Tighten `pipeline/agents/prompts/em-vision-critic-context.md` to load `ctx.criteria.query_by_character(character_id)` into the prompt body for every Phase 5 frame Em verdicts. The Bible's IR.* rules become first-class context Em can cite. The diff is small (3-5 lines in the prompt + a query call in vision_critic.py); the structural shift it represents is large.

---

## 5. style-register-default-anchoring (regression-prevented at the prompt-test layer)

**Surface symptom:** Cy authors a pixel-art-8bit Bible but emits rules in pencil-test vocabulary (cross-hatching, graphite weight, cream paper) because Cy's standing-context preamble carried pencil-test as the implicit default register. The mascot Bible looks plausible at first glance but silently fails to constrain the pixel-art aesthetic Flo's Phase 5 routing was supposed to enforce.

**How this is regression-prevented:** Not by this eval suite directly — by `tests/test_prompt_style_neutrality.py` (the Task 1.4.6 guardrail). The guardrail fires at CI time when register-anchored markers in load-bearing prompt sections appear without cross-register companions. The Task 1.4.5 defang is what removed the bias; the Task 1.4.6 guardrail is what prevents regression. Case 2 (claude-mascot-reproduction) is the eval-layer validation that the architecture supports the pixel-art register — the mock envelope carries `style_register: pixel-art-8bit` and the suite asserts the emitted Bible carries the same.

**Fix vector:** If the guardrail catches a regression, fix the offending prompt section by adding parallel cross-register language. See `docs/architecture/prompt-style-neutrality-doctrine.md` for the procedure.

---

*This taxonomy is expandable. Each new failure mode should follow the surface-symptom / how-the-suite-catches-it / fix-vector structure so the eval suite stays a contract for what we know to look for, not a wishlist of things we might.*
