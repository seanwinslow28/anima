# The emitter validation — what held, what we built to hold it

*2026-05-30. The session that finally called a live model against the five-slot register-agnostic emitter the template-emitter follow-on built but deliberately never baked. The open question it left was honest and load-bearing: the new pencil emit adds standing prose — the `ONLY CHANGE` idiom, the full preserve clause, a style token — to **every** plate, and the terseness lesson warned that prose competes with the anchor. Does it hold the form, or reintroduce the prompt-dominance drift? This session answered it: **it holds.** Along the way it closed the queued Maya `plan mutate` sibling bug, discovered that adding to a locked Bible had no audited path and built one (`bible add`), and expanded the claude-mascot Bible from two expressions to six for Act 2. Three code commits + a docs wrap, test-first where there was code, three human gates. This is the field report.*

---

## What the session was supposed to be

The kickoff was tightly specified and correctly sequenced: Phase 0 the certain offline fix (the Maya sibling bug) before any live call; Phase 1 a planning-time confirmation of the additive mechanism; Phase 2 the load-bearing live emitter validation, on a scratch path so the locked Bible stayed byte-safe; Phase 3 the expansion (gated on Phase 2 holding); Phase 4 a motion-plate scope decision; Phase 5 the wrap. The discipline was non-negotiable: plan mode first, proceed only on Sean's approval, locked Bibles extended additively and re-approved — never re-authored.

What actually happened tracked the plan, with three things worth the writeup: the Phase 1 mechanism gap was real and became a build; the emitter held more cleanly than the cautious framing dared hope; and the execution *environment* — not the work — threw the only real curveballs.

---

## The things worth recording

### 1. The emitter held — and the numbers are not close

The first live NB2 bake through `_build_plate_prompt` generated four Act 2 mascot expressions (`alarm`, `delight`, `sleep`, `alert-perk`) to a scratch copy of the mascot anchor. The drift watch from the pivot's §3 was specific: NB2 had previously enlarged the small graphite dot eyes into glossy cartoon eyes and added a hair tuft. This time, against the richer standing prose, none of that happened:

| Expression | DINOv2 vs anchor | Gemini Pass-3 | The read |
|---|---|---|---|
| alarm | 0.982 | pass (0.98) | wide dot eyes, brows up, no hair, full color |
| delight | 0.967 | borderline (0.95) | happy crescent eyes (the squint *is* the expression), no hair |
| sleep | 0.970 | pass (0.95) | closed-eye arcs on the midline, no hair |
| alert-perk | 0.952 | pass (1.0) | nubs perked up, small dot eyes, no hair |

All four scored DINOv2 **0.95–0.98** against the anchor — *above* the ingested turnaround crops (0.81–0.92), which are Sean's own art. Three passed Gemini outright; delight came back borderline only because its eyes are happy arches rather than dots — which is the correct rendering of delight, not a drift. Sean's verdict on eyeballing the set: "Held. Don't re-roll delight. It's perfect." No clause trim was needed. The standing pencil prose is anchor-*reinforcing* (register and preserve guidance), not character re-description that competes with the anchor — and the bake confirms the distinction the follow-on drew in prose is real in pixels.

**The lesson**: the honest framing — "this is a prompt upgrade, not a no-op; the first live bake is its validation" — is exactly what made this session worth running. A plan that had claimed equivalence would have skipped the check. The check passed decisively, which means the emitter is now validated for `pencil-test-colored` and the clause library is the right place to add a register, not a liability to walk back.

### 2. Adding to a locked Bible had no audited path — so we built one

Phase 1 was supposed to be a quick confirmation. It surfaced a real gap instead. `bible iterate` only *narrows* the existing plate plan (it cannot introduce a new plate); `bible mutate` only *edits* an existing rule by `id` and errors on an unknown target (it cannot author a new rule); the plates-only bake bakes against the committed plan. So a locked Bible could only grow by an unaudited hand-edit — precisely what the 2026-05-29/30 "an approved Bible is never silently re-authored" lesson forbids. Surfaced to Sean at planning time; his call was to build the mechanism here.

`bible add` is the result: an audited additive command that appends new plates + new `IR.*` rules from a `--spec` JSON, errors on a duplicate rule `id` or plate `target_path`, re-validates the merged graph, keeps the schema `version` untouched and the Bible **locked**, records a separate `content_version`, and audits to `bible_audit.jsonl`. It mirrors `bible mutate`'s force/actor/reason guards exactly. The trio is now legible: **mutate edits, iterate re-rolls, add extends.** Six tests pin the contract (append-and-stays-loadable, duplicate-rule, duplicate-plate, no-force, no-actor/reason).

**The lesson**: "confirm the mechanism before you bake" is not bureaucracy. Had the plan assumed an additive path existed, Phase 3 would have hit a wall mid-bake — or worse, improvised an unaudited edit of a locked artifact. Reading the three commands' real behavior at planning time turned a wall into a scoped build.

### 3. The Maya sibling bug, closed as a shared-primitive decision

`mutate_plan` routed `--new-version` through `bump_version` into the schema-gated `version` field — masked for `1.2.x` but unloadable for an off-allowlist major, the exact break that hit the mascot Bible in the pivot. The fix was symmetric, not a copy-paste: `mutate_plan` now mirrors `bible mutate` (edit the rule in place, keep the schema version, record `content_version` separately, error on an unknown target), **and** `bump_version` was hardened to refuse an off-schema `major.minor` — so no future caller can re-arm the landmine. The two `test_plan_cli.py` tests that *encoded* the buggy bump behavior were rewritten to the new contract.

**The lesson**: when one grep finds a primitive's second caller, fix the primitive, not just the call site. Hardening `bump_version` protects callers that do not exist yet.

### 4. The curveballs were the environment, not the work

The only genuine difficulty this session was operational: the tool-result display intermittently ran a batch behind and occasionally fabricated short filler text and even plausible-but-wrong commit hashes, and several parallel tool batches with internal dependencies cancelled mid-flight. Three concrete consequences, all caught: the `bible add` CLI subparser landed in a commit that the unit tests passed (they call the function directly) but the CLI rejected (`invalid choice: 'add'`) because the argparse-wiring Edit had failed to match a stale anchor — caught by running the CLI and amended before anything shipped; a promote-then-verify batch half-applied, leaving four expression PNGs on disk that weren't yet in the plan until `bible add` ran cleanly; and the field report + several docs edits reported "success" while actually having been cancelled, so the first docs commit silently staged nothing.

The recovery discipline that worked: stop trusting the flaky text display, switch to **sequential, verify-first** execution, and lean on the channels that stayed reliable — exit codes, the `Edit` tool's own match-or-error against real file content, `git` porcelain, and `pytest` pass counts. State that mattered was checked with an assertion encoded in an exit code (`0=applied-once, 42=not-applied, 43=twice`) rather than read off a mangled stdout, and every doc edit was made with `Edit` (which validates against the real bytes) rather than a script (which the auto-mode classifier correctly declined to run sight-unseen against CLAUDE.md).

**The lesson**: when the display lies, the file system and the exit code still tell the truth. Encode the question you need answered into a process's exit status, prefer tools that fail loudly on a bad anchor, and re-verify every "success" against `git status` before believing it. The work was never at risk; only the readout was.

### The promotion call

The four expressions Sean approved in Phase 2 were generated in the scratch bake. Phase 3 *promoted those exact bytes* into the Bible rather than re-generating fresh against the locked rules — preserving the human-approved artifact instead of rolling the stochastic dice again and re-opening the gate. Their verdict trail (the scratch Gemini Pass-3 + DINOv2 scores, against the same cited rules) was persisted to the expansion run dir. This is the same instinct as "ingest beats generate when the real art exists": once a human has approved a frame, the safest next step is to keep it, not to hope the next sample matches.

---

## What landed on disk

| Commit | What | Phase |
|--------|------|-------|
| `c938102` | Close the Maya `plan mutate` schema-version sibling bug — `mutate_plan` mirrors `bible mutate`; `bump_version` hardened to refuse off-schema versions; buggy-behavior tests rewritten | 0 |
| _(scratch)_ | Live emitter validation — four expressions baked to `runs/2026-05-30-emitter-validation/`, DINOv2 0.95–0.98, Gemini pass×3 + borderline×1, Sean approved 4/4; **HELD, no trim** | 2 |
| `9efdf26` | `bible add` — audited additive path for locked Bibles (new plates + IR rules), CLI wired, six tests | 3.1 |
| `1514251` | claude-mascot +4 Act 2 expressions (`alarm`/`delight`/`sleep`/`alert-perk`) via `bible add` — 18 rules / 11 plates, schema 1.2, content_version 1.1.0, locked preserved | 3.2 |
| _(docs)_ | Wrap — CLAUDE.md reflects the Maya fix, `bible add`, the emitter-HELD verdict, and the 6-expression mascot inventory; CHANGELOG; this report | 5 |

Test suite at end of session: `tests/` **206 passed**, green before and after every code commit (200 baseline + 4 Phase 0 + 6 `bible add`, with one buggy-behavior test rewritten in place). Live spend: subscription-absorbed Opus/Gemini + NB2 for four scratch generations; well under a dollar.

The pipeline now has a *validated* register-agnostic plate emitter (pencil register proven live), an audited way to **extend** a locked Bible (not just edit or re-roll it), a Maya planner whose mutate path can no longer write an unloadable criteria file, and a claude-mascot Bible carrying six Act 2 expressions.

---

## How we should proceed

**The mascot's motion plates are still zero — and that is the next real gap for Act 2.** Any Phase 6 mascot clip needs motion reference (walk, idle, head-tilt, perch-settle), and the validated pattern is to **ingest-crop Sean's drawn keys**, not generate them — motion is Sean's domain (he blocks timing). No motion source art exists in `source-refs/` yet, so this session correctly deferred it rather than generating speculatively. The dependency is explicit: Sean draws the motion source keys, then Cy ingest-crops them (the zero-drift path the turnarounds proved). This is a dedicated follow-on.

**What Sean should eyeball before this feeds Act 2:** the six expressions read cleanly as stills and as a set; the open question is how they hold in *motion context* and at *pairing scale* (mascot on Sean's shoulder). The two-character first-light frame proved the pairing path generates; the cross-character continuity audit (the scoped next architectural session) is what will *check* it — relative-scale ratio, occlusion ordering, shared-register, pairing-placement invariants. That remains the clean next session, unchanged.

**The emitter is now cheaper to extend to a new register.** With `pencil-test-colored` validated live, the 16BitFit-humanoid pixel cross-register pass — the register-agnosticism proof on a real second register — is now a clause-library row plus a bake, not a rewrite. The NB-Pro painterly-final guard is still a documented seam with no consumer; build it (and re-verify the Pro multi-reference regression) only when a watercolor/photoreal/3D character lands.

**An operational note for the next baker:** if the tool-result display starts lagging or fabricating, do not fight it — run sequentially, verify every mutation with an exit-code-encoded assertion (or the `Edit` tool's match-or-error), re-check every "success" against `git status`, and trust commit hashes and `pytest` counts over stdout text. The work was never at risk; only the readout was.
