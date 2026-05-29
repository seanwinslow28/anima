# The visual-fidelity fix — session writeup

*2026-05-29. This is the narrative of the implementation session that acted on the [visual-fidelity post-mortem](../2026-05-29-cy-visual-fidelity-post-mortem.md). The post-mortem diagnosed why Cy's generated Bible plates passed every automated gate and still read as a different character. This session built the fix, validated it against live models on both registers, and surfaced (and fixed) three second-order failures along the way. It ends with what was deliberately deferred and what to do next.*

---

## 1. The one-paragraph version

The fidelity gap was real and is now closed at the mechanism level. The root cause was **prompt-dominance**: Cy fed NB Pro long verbal *descriptions* of the character, and the model synthesized a generic person from the words while treating the anchor pixels as a loose hint. A ~15-minute disambiguating experiment confirmed it — feed the anchor with a terse "redraw this exact character" prompt and identity snaps back. The fix makes the **runner the source of truth**: every generate plate is seeded with the anchor unconditionally, never chains off another generated plate, and the plate prompt is a short intent wrapped in fixed reference-role-tag framing plus an anti-caption guardrail. Validated live: the worst drifters came back recognizably Sean (and the mascot came back as its octopus, not a chibi humanoid). Adopting Opus 4.8 for the authoring tier — folded in per the director's call — introduced two parser/runtime failures that the live re-bake surfaced and that are now fixed. Seven commits, 176 tests green throughout.

---

## 2. What was validated (the wins)

- **The mechanism recovers identity on the pencil-test-colored register.** The `head-front`, `neutral`, `surprised`, `focused`, `contemplative`, and `stylus` plates regenerated as recognizably Sean — blonde hair, blue eyes, warm full-color skin, navy tee, gray jeans — versus the pre-fix monochrome "romance-hero." Similarity scores **0.58–0.69** against the anchor, vs the old drift at **0.468**.
- **The anti-caption guardrail killed the `stylus.png` bug.** The pre-fix stylus plate rendered the prompt's meta-prose as handwritten captions on the page; the new plate is clean.
- **The fix generalizes to the pixel-art-8bit register.** A mascot generate plate run through the exact fixed code path returned the orange pixel-octopus (blocky lozenge, dot eyes, stub legs) — *not* the pre-fix generic chibi humanoid. The fix is structural, not a one-character fluke.
- **The pipeline now leaves an audit trail.** Every plate gets a Pass-2.5 pixel-similarity score persisted to `runs/{run_id}/plate_verdicts.jsonl` next to Gemini's prose verdict — the per-plate signal the 2026-05-28 run lacked.
- **Opus 4.8 authors full-color rules naturally.** Reading the notes + anchor, 4.8 emitted a full-color palette (hair, eyes, costume colors) without being told to — confirming the director's "full-color is canonical" decision is the model's natural read, not a fight.

---

## 3. The failures, and how each was overcome

This session's real value is in the failures it surfaced. Three were second-order consequences of adopting Opus 4.8; one was a pre-existing data bug; one is an honest limitation of a tool we built. None were silent — and that is the point.

### 3.1 Opus 4.8 Pass-1 timeout → silent stub (commit 2b)

**Failure.** The first live re-bake under Opus 4.8 ran for *exactly* 900 seconds, hit Cy's Pass-1 timeout, returned empty text, and the parser fell back to a STUB FALLBACK envelope (0 plates, placeholder rules) — while the orchestrator still exited 0. A successful exit code lying about what happened: the exact failure mode the 2026-05-28 test report warned about.

**Root cause.** Opus 4.7 authored the ~50KB envelope in ~500s; 4.8 spends more on extended thinking for the same structured emission and ran past the 900s ceiling. A direct small-prompt call to `claude-opus-4-8` succeeded fast (slug valid, SDK path fine) — it was specifically the long envelope that ran over.

**Overcome.** Raised the Pass-1 timeout to 1800s, *and* made the stub a loud failure: `CharacterDesignerNode.run` now computes a `pass1_stub` flag (stub-flagged response, non-zero exit, or empty text) surfaced in `AgentResult.notes`, and `author_bible.py` exits non-zero with a diagnostic instead of silently shipping a stub Bible.

### 3.2 Opus 4.8 narrates around the JSON fence → silent stub again (commit 2c)

**Failure.** The *second* re-bake (now under 1800s) stubbed again — but this time returned in 329s, exit 0, 26KB of text. Not a timeout. And the loud guard from 3.1 did *not* fire, because the response wasn't empty.

**Root cause (found by capturing the raw output, not guessing).** Opus 4.8 wraps the JSON envelope in conversational prose — *"I'm Cy, authoring Pass 1… Here is the Pass 1 envelope:"* before the ` ```json ` fence, and authoring notes after it. Cy's fence regex was anchored to the whole string (`^…$`), so prose around the fence broke the match → `json.loads` on the whole blob failed → synthetic stub. This is the Opus 4.8 "honesty/narration" disposition; 4.7 emitted a bare fence.

**Overcome.** Rewrote `_parse_json_envelope` as a three-rung ladder: (1) the first ` ```json ``` ` fenced block found *anywhere* in the text (de-anchored + `finditer`); (2) the whole stripped text as raw JSON; (3) `_extract_first_json_object` — a brace-depth scanner (string/escape-aware) that pulls the first balanced `{…}` object out of prose. Validated against the captured 26KB output: parses cleanly. Also marked the synthetic stub envelope with a `_pass1_stub` sentinel so the loud guard now fires on the unparseable-but-non-empty case too.

### 3.3 The `#region` crop bug (pre-existing, fixed in commit 3 / Phase 4)

**Failure.** Body turnarounds were byte-identical full-sheet copies (6,151,720 bytes each) — the `#region:body-front` suffix was split off and ignored, so the crop never ran.

**Overcome.** Implemented real region cropping: `_region_box` + `_crop_region` read a `<sheet>.regions.json` sidecar (fractional or pixel boxes) and crop. When a region can't be mapped, the runner copies the whole sheet *and flags `region_not_cropped`* — never a silent wrong crop. Authored `turnaround-1.regions.json` (7 boxes), visually verified each crop.

### 3.4 Line-art-vs-color register inconsistency (fixed in commit 3 / Phase 4)

**Failure.** Some head turnarounds ingested *line-art motion frames* (`head-turn-1.png`, `head-turn-9.png`) while the rest of the Bible is colored — an internally register-inconsistent turnaround set.

**Overcome.** `turnaround-1.png` is itself full-color, so the head turnarounds were repointed to colored `#region` crops of it (`head-front`/`head-3quarter`/`head-profile-left`), with `head-profile-right` set to `generate` (full-color mirror). The line-art frames stay where they belong — `motion_plates/`.

### 3.5 The similarity gate inverted on the mascot (an honest limitation, commit 3b)

**Failure.** The Pass-2.5 gate scored the *recovered* mascot plate **0.460** and the *drifted* one **0.571** — it ranked the correct plate below the wrong one.

**Root cause.** The pure-PIL tier (the only one available without `torch`) is a global color-histogram + luma metric, so it is scale/background-sensitive. The mascot anchor is a tiny creature on a mostly-white field; the recovered plate fills the frame with orange. The white/orange ratio swamped the identity signal. On sean-anchor (consistent full-figure framing) the ordering was correct.

**Overcome — partially, and honestly.** Not "fixed" — *documented* as a KNOWN BLIND SPOT in `similarity_gate.py` and the [mascot finding](2026-05-29-phase1-rebake-recovery/mascot-cross-register-finding.md). The PIL tier is a useful severe-drift detector for consistent-framing characters but is unreliable for tiny-subject/variable-crop registers; the human/visual gate is the arbiter there. The gate's method ladder already prefers DINOv2 (semantic, scale/background-robust) when its deps are installed — that is the real fix, deferred (see §6).

---

## 4. What we learned

1. **Capture the raw output before fixing.** Both Opus 4.8 failures (3.1, 3.2) looked identical from the outside — "the re-bake stubbed." Only capturing the actual Opus response distinguished a timeout from a parser mismatch. Guessing would have fixed the wrong thing.
2. **A more capable model is not a drop-in.** Opus 4.8 is better at the *content* (it authored full-color rules unprompted, with honest risk notes) but its dispositions changed the *plumbing*: slower on long structured emissions, and chattier around structured output. Both broke assumptions baked in against 4.7. Model bumps need their own validation pass, not just a slug change.
3. **Loud failure is load-bearing.** The post-mortem's organizing lesson — "a successful exit code can lie" — recurred twice this session. Each time, the fix was as much "make it fail loudly" as "make it work." The mascot's transient stub proved the guard's worth: it caught a one-off malformed emission with no silent ship.
4. **A cheap metric has a cheap metric's blind spots.** The PIL similarity gate is genuinely useful for the case it was built for (consistent-framing severe-monochrome drift) and actively misleading outside it (tiny-subject-on-background). Knowing *where* a tool lies is as valuable as the tool. The visual gate remained the final arbiter, exactly as the engine truth says it should.
5. **The runner, not the model, should own identity grounding.** The whole fix rests on moving reference resolution and prompt framing out of Cy's (model-authored) hands and into the runner. A more capable model emitting wordier prompts can no longer reintroduce drift, because the runner overrides the framing every time.
6. **Prompt-dominance was the lever — the model was not the ceiling.** The external evidence suggested NB Pro's multi-ref was structurally degraded and might cap any prompt fix. Phase 0 showed otherwise: NB Pro recovers identity fine when it isn't fighting a verbose description. This saved us from prematurely standing up an expensive model bake-off (Track B).

---

## 5. What was deferred (and why)

- **Track B — the model bake-off (FLUX.2 / GPT-Image-2 / FLUX+LoRA).** Closed, not run. Phase 0 + the re-bake showed NB Pro recovers identity once prompt-dominance is removed; the generated-plate class no longer drifts. The director's standing call was "small probe, conditional on a class still drifting" — the condition was not met. Reopen only if a future piece exposes a drift class the mechanism can't fix.
- **Production plate regeneration for the locked Bibles.** The sean-anchor Bible's *rules, plan, and `regions.json`* are fixed and committed, but left `locked: false` and its *plate PNGs were not regenerated*. This is deliberate: the director approves the Bible, and the new plates should be baked against the approved rules, not pre-empted. The claude-mascot locked Bible is entirely untouched.
- **The DINOv2 similarity tier.** The gate's ladder is built for it, but it needs `pip install torch transformers` (~2GB) and a model download — too large to add unilaterally to the environment. The PIL fallback ships today with zero new deps; DINOv2 is the upgrade that makes the gate trustworthy on the mascot register and safe to promote to a hard pre-Gemini gate.
- **Cy retry-on-parse-failure.** The mascot's transient malformed Pass-1 emission was caught loudly but required a human re-run. Cy has a three-call Pass-1 budget; wiring a retry on parse failure (not just on contract violation) would auto-recover from transient malformations. Logged, not built — the loud guard makes it an optimization, not a correctness fix.
- **The full mascot re-bake.** Only one mascot plate (`head-front`) was generated, via a direct mechanism check, because the full bake hit the transient stub. Re-running it now (the parser handles its output) would produce the full mascot plate set — deferred with the production regeneration above.

---

## 6. Recommended next steps

In rough priority order:

1. **Review and re-approve the sean-anchor Bible.** Open `characters/sean-anchor/acceptance_criteria.json` (now full-color, 22 rules, `locked: false`), eyeball the ported palette/skin/hair/eye rules, adjust the skin hex `#F0DFCB` / eye hex `#4A6D8C` and the `turnaround-1.regions.json` boxes if they need tightening, then `python -m pipeline.cli bible approve --character-dir characters/sean-anchor/`.
2. **Bake the production plates against the approved Bible.** With the fixed mechanism + crop + repointed plan, run the authoring orchestrator (or a narrowed `bible iterate`) to regenerate sean-anchor's plate PNGs into the production folder. The crop ingests are deterministic; the generate plates use the recovered mechanism.
3. **Run the full mascot re-bake** (`scripts/author_bible.py characters/claude-mascot/ …`) to produce its full plate set, then apply the same review → approve → bake loop. Expect to need a retry if it hits the transient stub (the loud guard will tell you).
4. **Install the DINOv2 tier** (`pip install torch transformers`) and re-score both Bibles' `plate_verdicts.jsonl`. This is what makes the similarity gate trustworthy on the mascot register and lets you promote it from a record-only flag to a hard pre-Gemini reject. Add a regression eval that asserts recovered > drifted on *both* registers.
5. **Wire Cy's Pass-1 retry-on-parse-failure** so transient Opus 4.8 malformations self-heal within the three-call budget.
6. **Preserve the scratch outputs you care about.** The full recovered sean-anchor plate set lives in `runs/2026-05-29-cy-sean-anchor-rebake/scratch-sean-anchor/` (gitignored). If you want it kept permanently, copy it into `docs/anima-test-runs/`. The raw Opus captures in `/tmp` will vanish on reboot.

---

## 7. The commit trail (this session)

| Commit | What |
|--------|------|
| `6e46ac0` | Phase 0 — disambiguating experiment (prompt-dominance confirmed) |
| `8b9630d` | Commit 1 — mechanism: anchor injection + no-chaining + role-tag prompts + Opus 4.8 |
| `585f4d3` | Commit 2 — Pass-2.5 similarity gate + persisted `plate_verdicts.jsonl` |
| `d09e527` | Commit 2b — Opus 4.8 Pass-1 timeout fix + loud stub-fallback |
| `d5e8443` | Commit 2c — robust JSON-envelope parser (narration around the fence) |
| `0da37fb` | Commit 3 (Phase 4) — full-color rule port + `#region` crop fix + register repoint |
| `09dc3d3` | Commit 3b — mascot cross-register validation + documented gate blind spot |

176 tests green at every commit (157 baseline + 19 added across the session).

## 8. Where the outputs live

- **Committed evidence (curated, in git):** `docs/anima-test-runs/2026-05-29-phase0-fidelity-experiment/`, `…-phase1-rebake-recovery/`, `…-phase4-crop-fix/`.
- **Full re-bake working dirs (gitignored, on disk):** `runs/2026-05-29-cy-sean-anchor-rebake/scratch-sean-anchor/` (complete set) and `runs/2026-05-29-cy-claude-mascot-rebake/scratch-claude-mascot/` (one plate; rest stubbed).
- **Production Bibles (in git):** `characters/sean-anchor/` (rules/plan/regions updated, plates not yet regenerated) and `characters/claude-mascot/` (untouched).
- **Ephemeral:** raw Opus Pass-1 captures at `/tmp/opus_pass1_raw.txt` and `/tmp/mascot_pass1_raw.txt`.

---

*Engine truth: the character must be "recognizably itself in its intended medium." After this session it is — Sean reads as Sean and the mascot reads as the mascot, in full color, through the fixed mechanism. What remains is the director's approval and the production bake. — filed 2026-05-29*
