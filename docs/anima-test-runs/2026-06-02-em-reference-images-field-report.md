# Field report — Em reference-images: giving the critic the Bible

**Date:** 2026-06-02 (workstream opened 2026-06-01)
**Branch:** `feature/em-reference-images` (isolated worktree off `main` @ `458b248`)
**Closes:** [`2026-06-01-em-reference-blindness-FINDING.md`](2026-06-01-em-reference-blindness-FINDING.md) — the locked #1 critic-spine fix (code), measurement deferred.
**Spec / plan:** [`docs/superpowers/specs/2026-06-01-em-reference-images-design.md`](../superpowers/specs/2026-06-01-em-reference-images-design.md) · [`docs/superpowers/plans/2026-06-01-em-reference-images.md`](../superpowers/plans/2026-06-01-em-reference-images.md)

---

## The one-line story

Em judged every frame **reference-blind** — text only, no anchor, no Bible plate, and she never read `ctx.criteria`. This workstream **gives her the Bible**: a capped, Bible-driven reference bundle plus the character's `IR.*`/`AC.*` rules, attached to both her Gemini and Opus paths. The code shipped and is test-pinned (+22 contract tests, all green); the case-7 xfail flipped green. **The costed live re-baseline + bake-off are deferred** to a clean-terminal run — not because the change is unproven (it works live at n=1) but because the agent-harness execution environment fought the repeated-live-call pattern three different ways. This report is the honest record so the next session starts from the truth.

---

## What shipped (the four code seams + the case-7 flip)

All TDD'd (failing test → red → implement → green → commit), credential-free in CI.

1. **`RateCapExhausted` (agy wrapper)** — `41f2eca`. The bake-off had surfaced that `agy` writes its 429/`RESOURCE_EXHAUSTED` to its *log file* and returns exit-0 with empty stdout, so the stderr-only scan reported `ok=True` and every frame silently degraded to `borderline` during quota exhaustion. The wrapper now **raises** a distinct `RateCapExhausted` on (a) empty-stdout-exit-0 or (b) an explicit quota signal in stderr/log. A non-empty-but-malformed response is **not** a rate cap — it stays on the documented defensive-borderline path. The empty-vs-malformed distinction is load-bearing (keeps the two failure modes separate in the trace).

2. **`select_references()` (`pipeline/agents/reference_selection.py`)** — `864484d`. Approach **B**: a fixed, Bible-driven, capped bundle — `anchor.png` + up to `cap` canonical deduped turnarounds (front / 3-quarter / profile) — resolved *from the Bible* (folder mapped via `character.yaml`; turnarounds globbed + ranked by a view-preference list), so it generalizes to any character without hardcoded filenames. Same bundle every frame; eval == prod. The `checkpoint`/`beat` params are accepted but ignored in v1 — the view-aware seam (approach A) drops into this module later with no eval-contract change. Sean resolves to `anchor + head-front + head-profile-left + body-3quarter`. **Plan deviation (evidence-driven):** the plan's substring matcher picked `body-3quarter-back` over `body-3quarter` (the former sorts first, `-` < `.`); fixed the *implementation* (exact-stem-match before substring fallback), not the test.

3. **Em attaches references (`vision_critic.run` + `_build_prompt`)** — `288dc91`. `run()` prepends the subject frame to the bundle and passes `[subject, *references]` to **both** the Gemini default and Opus escalation paths (incl. phase-6 contact sheets). The ordering block tells Em image 1 is the subject and the rest are her Bible's canonical references — the licence-to-pass she lacked. `character_id` absent → no references (graceful, today's behavior). `RateCapExhausted` propagates (errored gap, never silent borderline).

4. **Em surfaces the criteria (`vision_critic._criteria_block`)** — `7ed1ae3`. Em now reads `ctx.criteria` (the merged `CriteriaBundle` she ignored) and surfaces `query_by_character ∩ query_by_phase` as a terse "cite these by ID" block (the Databricks Grading-Notes pattern). Graceful when the bundle is `None` (pencil-test legacy) or the intersection is empty (designed). This is the diff that flips case-7 green.

5. **case-7 flipped xfail → green (`evals/character_designer/`)** — `e47d375`. Three legitimate fixes: (a) validity — the `em_ctx` used `candidate_path`/`frame_num`/`manifest_style_block`; Em reads `image_path`/`frame_id`/`checkpoint`, so it threw `KeyError` before judging; (b) ID alignment — canonical is `IR.sean.*`, not `IR.sean-anchor.*` (folder key ≠ `character_id`); (c) honesty — replaced the hardcoded-`AC01` stub with a prompt-reading mock that cites whatever `IR.sean.*` rule Em's prompt *actually surfaced*, so it's green only if the criteria-half of the fix worked. **Plan deviation (evidence-driven):** the case's `impact_tags=[identity_critical]` force-escalates to Opus, so the *Opus* path produces the verdict — the plan mocked only Gemini, leaving the case red (Em's invariant raised on the unmocked Opus stub's empty cites). Fix: mock both paths with the same prompt-reading behavior (they share one prompt). Proven red-first.

6. **Eval re-wire for structural parity** — `16695f4`. `cases.yaml` gained `character_id` (not a hand-authored plate list — that would reintroduce the eval-prod gap approach B avoids). The harness and `score.py` both call the **same** `select_references` and load the **same** merged `CriteriaBundle` — parity is structural, not maintained by hand.

**Tests:** `tests/` **264 passed** (242 baseline + 6 rate-cap + 7 reference_selection + 5 references + 4 criteria); `evals/vision_critic/runner.py` green (30 passed, 6 motion xpass); `evals/character_designer/runner.py` **6 passed, 1 xpass** (case-7 now passed — one fewer xfail than baseline). `pipeline/tests/` green.

---

## The live measurement: why it's deferred (the harness saga)

The plan's Task 7 is a costed live re-baseline (run Em real, measure the precision lift with `false_pass_rate` held). It is **deferred**, not abandoned. Three live-run attempts each failed in a *different* place — a textbook "the architecture/environment is the problem" signal, not a code bug.

| # | Setup | Outcome |
|---|-------|---------|
| 1 | Single-process `score.py` (as written), via the agent's background-task | Case 1 scored a **correct** verdict (`pass`, conf 0.85, references attached) → then the process died at interpreter teardown: `Loop ... is closed`, exit 144, no traceback. |
| 2 | Subprocess-per-case isolation (`8a611d4`), no detachment | Case 1 scored (`borderline`, conf 0.72, refs attached) → the orchestrator was killed mid-`subprocess.run` for case 2 (no traceback = signal death). |
| 3 | Orchestrator **+ worker** session-detachment (`start_new_session`) | Orchestrator **survived** both teardowns and wrote the matrix ✓ — but **both cases errored** (`borderline` + empty cites → Em's invariant), because detaching the *workers* broke **Claude Code auth** for the Opus-SDK `claude` child. |

**Root cause (a trilemma on this Python 3.14 + `agy`/Opus-CLI + agent-harness stack):**
- The real `agy`/Opus child teardown emits an exit-144 / SIGURG-class signal that propagates through the shared process group and kills parent processes. (A zero-quota repro of 8× `asyncio.run()` + a trivial subprocess ran clean — so it is **specific to the real Go/Node children**, not the asyncio pattern.)
- Isolating the workers' signal by detaching them into a new session **breaks Claude Code auth** (the `claude` child needs the session context — exactly the "SDK uses Claude Code auth, keep it that way" coupling).
- So: workers must keep the session (to authenticate), but in the shared session their teardown signal destabilizes the parents.

**The resolution (shipped in the harness, validated for survival):** subprocess-per-case isolation + **detach only the orchestrator at launch** (`start_new_session` in a small Python launcher — macOS has no `setsid`), **never the workers**. The orchestrator parses each worker's `CaseScore` from stdout *before* the worker's teardown crash (the worker flushes its verdict first), so a teardown crash can't lose the verdict. The 2-case smoke confirmed the detached orchestrator survives multiple teardowns. What it does **not** fix inside the agent harness is the worker-auth-vs-signal tension cleanly enough to trust a 24-case costed run — hence the deferral to a clean terminal.

**The recipe for the deferred run (clean terminal, normal session):**
```bash
cd <worktree>
# Orchestrator detached into its own session; workers keep the session (Claude Code auth).
python -c "import subprocess,sys; subprocess.Popen([sys.executable,'-m','evals.vision_critic.score',
  '--segment','performs','--motion-smoke','1'], start_new_session=True)"
# or simply run it foreground in a real terminal:
python -m evals.vision_critic.score --segment performs --motion-smoke 1
# smoke first:  ... --limit 2
```
Scope (Sean's call): the **23 performs cases + exactly 1 motion smoke** (24). The headline metrics live in the performs segment; a still-image contact sheet can't score motion-proper (eval-strategy §3.5), so the other 5 motion cases are logged as intentionally-not-scored (honest segmentation). One motion case stays live to smoke-test reference-attach on the phase-6 contact-sheet path.

**The one number we do have (n=1, real):** in attempts 1–2 the reference mechanism worked end-to-end against live `agy` — `select_references` resolved the exact target bundle (`anchor, head-front, head-profile-left, body-3quarter`), attached it subject-first, and Em scored. That is the proof the *code* is correct; the deferral is purely an execution-environment matter.

**When the deferred run lands, hold the §9 disciplines:** false-pass-first (did `recall` hold at 1.00 and `false_pass_rate` at 0.00?), then precision lift with `stderr()` on the delta, then `cites-correct`. Labels stay locked — any that would flip is presented to Sean and re-ratified before lock. A precision lift that costs *any* false pass on the performs segment is a worse Em and blocks the change (and promotes follow-on #3, DINOv2, from deferred to next).

---

## An incident worth recording

Mid-investigation, a `score.py` process (`--segment performs --motion-smoke 1`) appeared running **from the main checkout** (`/Users/seanwinslow/Code-Brain/anima/evals/...`), distinct from every launch this session made (all of which ran from the worktree). It used the `--segment` flag, which only exists in this branch's uncommitted changes. It vanished before it could be traced; nothing was running afterward. The most likely explanation is a **parallel execution in the main checkout** (the idle session `22428` was cwd'd there) — the same shared-tree hazard the critic-spine postmortem records. No active collision occurred, but it reinforces: **costed runs need a single, known owner.** Flagged to Sean.

---

## Out of scope — the three named follow-ons (unchanged)

1. **View-aware reference selection (approach A).** Slots into `select_references`'s existing signature. Trigger: a precision shortfall on profile/turn shots in the (deferred) re-baseline.
2. **Pairwise-verdict reframe** ("is A or B closer to the anchor?"). A separate change to Em's verdict shape; a future sharpening.
3. **DINOv2 deterministic identity backstop.** The strongest identity signal is deterministic; Em-with-references is the right MLLM layer beside it. **Promoted to *next* if the re-baseline shows any false pass.**

Plus the deferred **live re-baseline + three-way bake-off** themselves (this report's headline), and the unchanged motion-proper metric (E_warp/VBench).

---

## Definition of done — status

- ✅ `select_references` ships, Bible-driven, capped, view-aware seam, unit-tested.
- ✅ Em attaches references (subject = image 1, both paths, incl. phase-6) + surfaces `IR.*`/`AC.*`, unit-tested.
- ✅ `RateCapExhausted` ships with the empty-vs-malformed distinction, unit-tested.
- ✅ case-7 flipped xfail → green (validity + ID alignment + honest mock).
- ✅ Eval re-wired for structural parity; CI harness green, motion cases red.
- ✅ Harness hardened (subprocess isolation + `--limit`; orchestrator-detach recipe).
- ✅ **Live re-baseline — MEASURED 2026-06-02** via a transport pivot (agy → Gemini API; agy's personal-tier quota was 429-walling). **Result: the references change is BLOCKED by the false-pass gate** — see the postscript "Re-baseline measured" below.
- ⏸ **Bake-off re-run — NOT RUN.** Gated on the re-baseline reading clean; it didn't. (Separately, Task-4 forensics show the 2026-05-31 "Gemini" column was Flash, not Pro — a mislabel to correct when it does run.)
- ✅ Docs: this field report + CHANGELOG + CLAUDE.md Em row.

---

## Postscript — 2026-06-02 (later): re-baseline MEASURED via a transport pivot — and the references change is BLOCKED

The twice-deferred live re-baseline finally ran. The blocker was never the code — it was agy's personal-tier Gemini quota 429-walling every repeated run. So we **pivoted the transport**: a new `pipeline/agents/gemini_api_runner.py` calls Gemini directly via `google-genai` + `GEMINI_API_KEY` (a separate vendor billing line from agy's Google personal OAuth), config-selected by `critics.t2.transport: agy | gemini_api`. The references, criteria, and Opus-SDK escalation are untouched — the transport only delivers images+prompt. **It worked**: real verdicts, references attached, **no quota wall**, plain foreground run (the API path has no Go/Node child to crash at teardown, so the orchestrator-detach gymnastics this report agonized over are no longer needed).

### Forensics correction — the baseline never ran on Gemini 3.1 Pro
The validity gate (does the API request the *same* model agy used?) surfaced something bigger. agy passes **no `-m` flag** (`cli_runners` never set one), so its print-mode calls log `model=""` and the **Antigravity backend default ran**. Across **272/272 Em-sized agy calls** — spanning the **2026-06-01 0.62 baseline** *and* the 2026-06-02 attempts — the propagated backend model was **"Gemini 3.5 Flash (Medium)"**, never Pro. No `settings.json` pin. So:
- The 0.62 reference-blind baseline ran on **gemini-3.5-flash**, not the `gemini-3.1-pro` the manifest/docs/CLAUDE.md label. The label was aspirational.
- To hold the model **constant** (one variable: transport agy→API), the API transport pins **`gemini-3.5-flash`** (`gemini_api_runner.GEMINI_VISION_MODEL`). Sean confirmed.
- Knock-on: the 2026-05-31 three-way bake-off's "Gemini" column was Flash too — a mislabel to fix when it re-runs.

### The measured result (performs segment, n=23; gemini-3.5-flash@gemini_api + Opus escalation)

| Metric | Reference-blind baseline (2026-06-01) | References (2026-06-02) | Read |
|---|---|---|---|
| **false_pass_rate** | **0.00** | **0.15** | ❌ gate failed |
| **recall** | 1.00 | 0.85 (±0.10) | ❌ dropped |
| precision | 0.62 | 0.73 | lift, but **disqualified** |
| cites-correct | — | 0.80 | n/a |

Two false passes on performs — both real defects Em let through: `stylus-hand-f13-cc01` (the known costly CC01 wrong-hand defect) and `proportion-eyes-body-profile-right`. **Per §9, a precision lift bought with *any* false pass on performs is a worse Em — the change is BLOCKED, and follow-on #3 (DINOv2 deterministic identity backstop) is promoted from deferred to *next*.**

### Why — diagnosis (false passes investigated, plus a prompt-ablation)
1. **Verdict variance (Opus stochasticity).** `stylus-hand-f13-cc01` is `identity_critical` → Opus produces the verdict, and Opus is non-deterministic on a genuinely hard spatial call (left/right hand from a ¾ view): it scored `pass` in the baseline run but **`fail` (correct) on a plain re-run**. So ~1/23 of the 0.15 is sampling noise — a single 24-case run is a noisy estimate of false_pass_rate.
2. **Confabulation / forgiveness (the real signal).** `proportion-eyes-body-profile-right` passed in **both** runs. The fixture is a flat-digital cartoon (off-register from the A-2 anchor) with a subtle proportion/jaw/eye drift in profile — yet Opus's reasoning claims *"warm-graphite contour… visible construction marks… cream paper substrate with visible grain."* Those features **aren't in the fixture**: Opus is reciting the reference bundle's register onto the subject and confabulating a match. Given a reference "story," the MLLM narrates it.
3. **Prompt-ablation** (forgiveness sentence *"a feature that MATCHES the references is correct…"* stripped): `proportion-eyes` flipped pass→fail — **but for the wrong rule** (it flagged the absent stylus it had previously forgiven, while *still* reading the labeled proportion/eye defect as holding and *still* confabulating grain). So the matching-wording **is** a forgiveness lever, but removing it is **not a fix** — the underlying confabulation and the unseen fine-grained defect persist. This is the case for a deterministic backstop the prompt can't fix.

### Decision + open items
- **§9 block stands.** Promote **DINOv2 (follow-on #3)** to next — a deterministic identity/proportion signal can't confabulate grain.
- **Implicated levers recorded** (future, not this session): soften the *"matches references = correct"* wording; **view-aware reference selection** (approach A) so profile shots get profile refs.
- **Open decision for Sean (not acted on here):** references-attach is the *shipped* default (merged in PR #13) and is now **eval-blocked**. Whether to revert it, gate it behind a flag, or leave it pending the DINOv2 work is a scoping call — flagged, not decided. The **transport pivot itself is kept** (`transport: gemini_api`): it's orthogonal to the references finding and it's what made the measurement possible.
- **The portfolio artifact** is not "0.62 → a better number." It's the honest one: the intuitively-good change (give Em the Bible) **regressed the safety metric**, the eval caught it, and the diagnosis is legible. Empirical, not vibes.

_Artifacts: `evals/vision_critic/last-run.md` + `traces/baseline-2026-06-02-scored.md` (the measured matrix). Build commits on `eval/em-rebaseline`: transport (`59b095c`), selector (`27f3358`), scorer/manifest (`0cb37eb`), pin correction (`d7d136a`)._
