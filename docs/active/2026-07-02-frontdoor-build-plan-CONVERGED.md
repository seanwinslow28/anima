# Brainstorm Front Door (①) — Converged Build Plan (Opus + Codex)

**Date:** 2026-07-02
**Status:** Planning — the executable spec for ①, the active build. **Plan only; no code this session.**
**Supersedes the build section of:** [2026-07-02-brainstorm-front-door-build-plan.md](2026-07-02-brainstorm-front-door-build-plan.md) (kept as the *why*; this is the *how*).
**Ground truth / eval fixture:** the 2026-07-02 hand-run dry-run — [piñata concept doc](2026-07-02-frontdoor-dryrun-pinata-short-concept.md) + [Studio Brief](2026-07-02-frontdoor-dryrun-pinata-short-studio-brief.md).
**Co-planned with:** Codex (independent plan + adversarial red-team) — reconciliation notes in §11, red-team fold in §12.

---

## 1. Purpose & scope

Build the **brainstorm front door**: a standalone interactive session that turns a one-line spark into the exact bundle the dry-run produced by hand — a **concept doc + a Maya-ready Studio Brief + locked style refs + character seeds** — which `python -m pipeline.run --brief <dir>` then consumes as an authoring run.

Five stages (**EXPAND → INTERROGATE → ART-VIZ → STRESS-TEST → SYNTHESIZE**), but sequenced walking-skeleton-first:

- **Slice 1 (this kickoff):** orchestrator + **INTERROGATE** + **SYNTHESIZE** + the testable code seam → emits a real brief dir that `pipeline.run` accepts, reproducing a piñata-grade brief.
- **Slice 2:** **EXPAND** (adaptive divergence).
- **Slice 3:** **ART-VIZ** + the first style-prompt skill (`genndy-tartakovsky`).
- **Slice 4:** **STRESS-TEST** (pre-mortem + red-team).

The piñata dry-run is both the spec and eval fixture #1; the skeleton must reproduce a brief of that calibre.

## 2. Architecture — orchestrator + model-invoked disciplines, over a thin code seam

Two layers, cleanly separated:

**(A) The skill layer (human-facing craft, markdown).** A **user-invoked orchestrator** skill runs the room; each stage is a **model-invoked discipline skill** it reaches for (Matt Pocock's composable shape — never a mega-skill). The orchestrator carries a running **session sidecar** (`frontdoor-session.md`, the `storytelling`-skill pattern) that each stage reads and appends to. All new skills live in `anima/.claude/skills/`.

**(B) The code seam (deterministic, credential-free, TDD-able).** A thin Python package `pipeline/frontdoor/` owns the **artifact contract** — schemas, emission, and validation of the brief directory. This is the only part with unit tests, and it needs no API keys, so **CI stays green without credentials**. The skills *produce prose*; the code *validates and emits the handoff*. The interactive craft (the interview quality) is judged by the **piñata golden fixture as an eval**, not a unit test.

Why the seam matters: a skill is a markdown prompt — not directly unit-testable. Pushing the *contract* (does this brief have the 8 sections? does `pipeline.run` accept it? is the handoff descriptor well-formed?) into pure Python is what makes "TDD, stub-green first, CI green" real for a fundamentally prompt-driven feature. It also keeps prose central: the skill writes the museum-worthy concept doc and Studio Brief as *prose* (exactly as the dry-run did), and the code only checks structure and emits the machine descriptor — no form-filling that would flatten the voice.

**The front door is opt-in and back-compat.** A hand-written brief skips the whole thing (the `pipeline.run` contract is unchanged). The front door writes a brief dir; `pipeline.run --brief <dir>` is the unchanged consumer.

## 3. The output contract (what `pipeline.run` actually needs)

Verified against [`pipeline/run.py`](../../pipeline/run.py) `_start` and the Sam/Bea/Maya agents:

- The **hard requirement** is `<brief>/00_studio_brief.md`. A brief **without** a `shots.yaml` is auto-detected as an **authoring run** (`PLAN → SCRIPT → STORYBOARD → GENERATE`) and **requires `--slug`**. The front door emits no `shots.yaml` (Bea drafts the board downstream), so every front-door brief is an authoring run.
- `00_studio_brief.md` is consumed as **free-text context** by Maya/Sam/Bea (`planner.py:91`, `scriptwriter.py:73`, `storyboard_artist.py:85` each read the file and drop it into the prompt) — nothing parses its headers. So the 8-section shape is a **convention we enforce ourselves** (for Maya's benefit and museum legibility), not a downstream parse. The validator owns that enforcement.
- **`derive_cast(manifest)` reads the *manifest*, not the brief** — so a run only starts if the brief's characters are registered as manifest namespaces. **This is the real downstream boundary:** the front door emits *character seeds*, but a new character (the kid, the grandma) is not GENERATE-ready until **Cy authors its Bible and it's registered**. The skeleton's "run accepts it" contract therefore means: **`pipeline.run --brief <dir> --slug S --stub` reaches the plan gate (Maya consumes the brief)** — proven with a test manifest that registers the piñata namespaces; the seeds→Cy→registration bridge is a documented dependency (§10), not part of Slice 1.

## 4. File layout

```
.claude/skills/
  brainstorm-front-door/            # (Slice 1) USER-INVOKED orchestrator — runs the room
    SKILL.md
    references/
      chain-map.md                  # stage order, adaptive-routing rules, skip conditions
      session-sidecar-contract.md   # the frontdoor-session.md shape each stage reads/appends
      studio-brief-contract.md      # the 8 sections + the "What this is NOT" discipline
      concept-doc-template.md       # the museum-worthy concept-doc shape
      pinata-worked-example.md      # the dry-run, verbatim, as the gold reference
  frontdoor-interrogate/            # (Slice 1) MODEL-INVOKED — the relentless grill
    SKILL.md                        # Grill Me loop + voiceprint generic-answer detector + CD North Star
  frontdoor-synthesize/             # (Slice 1) MODEL-INVOKED — synthesize-don't-interview; emit the bundle
    SKILL.md                        # to-prd pattern; calls pipeline.frontdoor to emit + validate
  frontdoor-expand/                 # (Slice 2) MODEL-INVOKED — adaptive divergence
    SKILL.md
  frontdoor-art-viz/                # (Slice 3) MODEL-INVOKED — Flow $0 default + Higgsfield MCP on-demand
    SKILL.md
    references/style-skill-shape.md # the AKCodez scaffold, stripped of marketing flavor
  frontdoor-stress-test/            # (Slice 4) MODEL-INVOKED — pre-mortem + red-team
    SKILL.md
  genndy-tartakovsky/               # (Slice 3) style-prompt skill (AKCodez shape + this session's research)
    SKILL.md
    references/timing-bible.md      # the 8 directives from the piñata concept doc

pipeline/frontdoor/                 # (Slice 1) the testable code seam — TRIMMED per red-team A6
  __init__.py
  brief.py        # StudioBrief: REQUIRED_SECTIONS, parse(text), render(), validate()
  handoff.py      # minimal Handoff descriptor (frontdoor.json): slug / characters / stage_provenance
  emit.py         # emit_brief_dir(...) -> writes the bundle + manifest_gap_report.md
  validate.py     # validate_brief_dir(dir) -> brief sections + handoff + inline seed-shape checks
  cli.py          # python -m pipeline.frontdoor validate <dir>   (validate only; no scaffold)
  # CUT (A6): seeds.py (seed shape checked in validate.py), spark.py (A4 micro-expand replaces it),
  #           style_refs.py / stress.py (style routes + stress verdict = prose in concept.md + one
  #           enum field each in frontdoor.json, added when Slice 3/4 land).

tests/
  test_frontdoor_brief.py           # (Slice 1) section parse / validate / round-trip
  test_frontdoor_emit.py            # (Slice 1) emit -> dir shape; piñata golden; gap report
  test_frontdoor_handoff.py         # (Slice 1) test_maya_plan_gate_accepts_frontdoor_brief (stub, start-only)
  fixtures/frontdoor/pinata/        # (Slice 1) the dry-run concept + studio brief as golden fixtures
  fixtures/frontdoor/manifest_pinata.yaml   # registers kid/grandma/host-dad namespaces for the acceptance test
```

## 5. Artifact schemas

### 5.1 Studio Brief (`00_studio_brief.md`) — the machine-facing Phase-0 input
`REQUIRED_SECTIONS` (7 H2 headers, exact text, order-enforced), plus one required nested H3:

1. `## What is this story about?`
2. `## Who is this character?`
3. `## What is the tone?` — must contain `### What this is NOT`
4. `## What is the format?`
5. `## What is the target medium?`
6. `## What is the deadline?`
7. `## What are the non-negotiables?`

`validate()` fails if any header is missing, out of order, has an empty body, or the `### What this is NOT` sub-block is absent. (Shape drawn from both [`tests/fixtures/studio_brief_seed.md`](../../tests/fixtures/studio_brief_seed.md) and the piñata dry-run brief — they agree.)

### 5.2 Concept doc (`concept.md`) — the human-facing, museum-worthy artifact
Prose, not a form. A light `concept-doc-template.md` names the expected movements (Title options / Logline / Register / Character + engine / Structure / Style-and-timing bible / the money shot / style routes / objective-audience-distribution / open threads) — mirroring the piñata concept doc. Validator checks only that the file is non-empty and carries a logline line; **its quality is an eval, not an assert** (voice can't be unit-tested).

### 5.3 Handoff descriptor (`frontdoor.json`) — the machine hand-off
**Slice 1 is minimal** (three fields — grows with real consumers, per A6/§12); `style_route` + `stress_verdict` land only when Slice 3/4 do.
```json
// Slice 1 (minimal — two immediate consumers: the run's --slug, and the gap report's characters):
{
  "slug": "grandmaster",
  "characters": ["kid", "grandma", "host-dad"],
  "stage_provenance": ["micro-expand", "interrogate", "synthesize"]
}
// Grown (Slice 3/4 add):
//   "style_route": "hybrid-genndy-pencil",   // chosen route id (Slice 3)
//   "stress_verdict": "proceed"              // proceed|revise (Slice 4)
```
The one deterministic contract the orchestrator writes and the validator checks. `characters` must be a valid slug list; `slug` must be a clean lowercase token `pipeline.run` will accept.

### 5.4 Character seeds (`character_seeds.yaml`) — the hand to Cy
Schema grounded (per Codex, R3) in `templates/bible/character.yaml.template` + Cy's node (`character_designer.py:127-166`):
```yaml
- character_id: kid                 # lowercase-kebab, per the character.yaml template
  display_name: "The Kid"
  story_role: "protagonist — smallest at the party; something coiled underneath"
  style_register: pencil-test-colored
  source_notes: |                    # seeds Cy's source-refs/notes.md
    Angular Tartakovsky design. Wears grandmother's faded headband — too big -> fits.
  anchor_ref: null                   # populated by ART-VIZ if a route render is chosen
  style_ref_ids: []                  # ART-VIZ route ids that become Cy source-refs
  cy_target_dir: characters/kid/     # where Cy authors, optional
```
**Not** a Bible — a seed Cy authors from. Cy still needs a non-empty `source-refs/` before it authors (R4).

### 5.5 (Slice 3) Style routes + (Slice 4) Stress verdict — prose, not typed schemas (per A6)
No `style_refs.py` / `stress.py` modules. Both stages write **prose into `concept.md`** (exactly as the dry-run did — the A/B/C route prompts and the open-threads risks are prose), and record **one machine field each in `frontdoor.json`**:
- **Style routes:** ART-VIZ writes ≥3 Flow-ready route prompts as a prose section in `concept.md` (the dry-run's A/B/C). The orchestrator records only the **chosen** `style_route` (an id string) in `frontdoor.json`. Any rendered ref path lives in the character seed's `anchor_ref` / `style_ref_ids` (where Cy needs it), not a separate routes schema.
- **Stress verdict:** STRESS-TEST writes the pre-mortem trichotomy (Tiger/Paper-Tiger/Elephant) + red-team "Fails if ___" as a prose section in `concept.md`. The orchestrator records only `stress_verdict: proceed|revise` in `frontdoor.json`. Always-on, non-blocking (findings surface; human decides).

## 6. Orchestrator ↔ sub-skill contract (a hard I/O boundary, per red-team A2)

The split is only real if a stage skill **cannot smuggle a global decision** into its sidecar block. So the boundary is typed, not conventional:

- **A sub-skill may return only four kinds of content:** `observations`, `options`, `recommendation`, `open_questions`. It proposes; it never decides.
- **Only the orchestrator writes the locked-decision fields:** `chosen_route`, `skip_stage`, `locked_style`, `stress_verdict`, `stage_provenance`. These are what `frontdoor.json` and the Studio Brief are built from.
- **Locked decisions are append-only** in the sidecar — a later stage cannot overwrite an earlier lock (EXPAND cannot re-decide the concept; ART-VIZ cannot silently choose the style; SYNTHESIZE cannot rewrite the meaning). It can only *raise an `open_question`* that sends control back to the orchestrator.
- **Only SYNTHESIZE emits the brief dir**, and only via the code seam (`pipeline.frontdoor.emit` + `validate`).

**Roles:**
- **Orchestrator (user-invoked):** reads the spark; runs the always-on micro-expand (§7); invokes stage skills in order; owns the session sidecar and every locked-decision field; at SYNTHESIZE calls emit + validate.
- **Sub-skills (model-invoked):** each reads `frontdoor-session.md`, does its one stage, appends only the four proposal fields, returns control.
- **Session sidecar (`frontdoor-session.md`):** the running memory — spark, micro-expand + picks, interrogation resolutions, art-viz route recommendation, stress findings — split into an append-only **locked-decisions** block (orchestrator-owned) and a **proposals** log (stage-appended). Falls back to inline conversation if unwritable (the `storytelling` sidecar rule).

## 7. Divergence: an always-on micro-expand, not a binary classifier (per red-team A4)

The original plan used a `classify_spark(text) -> "thin"|"rich"` heuristic to auto-route. **Cut.** A binary classifier mis-routes — a spark can be rich in plot but poor in style/theme, or thin but carrying one fragile high-value intuition that a full fan-out would dilute — and "human-confirmed routing" still frames the decision and invites default-accept.

Instead, the orchestrator **always runs a tiny micro-expand** before INTERROGATE, regardless of spark richness:
- **3 alternate premises** (different emotional cores / genre collisions),
- **3 style-tone routes** (different visual/register directions),
- **3 risk questions** (what could make this generic / saccharine / mean).

Then it asks one question: **deepen into a full fan-out, or proceed to interrogate?** This ships more reliably than a classifier and gives even the skeleton the dry-run's "lead with divergence" reflex.

- **Slice 1** implements the micro-expand *inline in the orchestrator skill* (3 premises / 3 routes / 3 risks — pure prompt, no `spark.py`).
- **Slice 2** (`frontdoor-expand`) is the **"deepen" path** — the full sw-creative fan-out (domain-rotation-every-10, cluster-after-expansion, JTBD lens) reached only when the human says "deepen."

## 8. Per-slice TDD task lists

Every slice: `superpowers:test-driven-development` (red → verify-red → green → verify-green → refactor); `superpowers:verification-before-completion` before "done"; run tests **per-directory from the repo root** (`python -m pytest tests/`); confirm the two md5 guards are byte-unchanged; one isolated worktree for the whole build (`superpowers:using-git-worktrees`).

### Slice 1 — the walking skeleton (the kickoff)
Code seam first (pure-Python, credential-free), then skills, then the end-to-end acceptance.

1. **`brief.py` — StudioBrief.** RED: `test_parses_seed_into_seven_sections` on `studio_brief_seed.md`; `test_missing_non_negotiables_fails`; `test_missing_what_this_is_not_subblock_fails`; `test_render_roundtrips`. GREEN: `REQUIRED_SECTIONS`, `parse`, `render`, `validate`.
2. **`handoff.py` — Handoff.** RED: `test_handoff_json_roundtrip`; `test_rejects_bad_slug` (uppercase/space); `test_characters_must_be_slug_list`. GREEN: dataclass + `to_json`/`from_json` + validation.
3. **CharacterSeed shape (no module — cut per A6).** The seed schema (§5.4) is validated *inline in `validate.py`*, step 5; there is no `seeds.py`. Author the `character_seeds.yaml` shape as part of the fixtures (step 6).
4. **`emit.py` — emit_brief_dir.** RED: `test_emit_writes_bundle` (asserts `00_studio_brief.md`, `concept.md`, `character_seeds.yaml`, `frontdoor.json`, **`manifest_gap_report.md`** all present); `test_emitted_studio_brief_revalidates`; `test_gap_report_lists_unregistered_characters` (given a manifest, the report names each seed character not registered + its next Cy action); `test_emit_is_idempotent`. GREEN.
5. **`validate.py` + `cli.py`.** RED: `test_validate_passes_on_pinata_golden`; `test_validate_fails_on_truncated_brief`; `test_validate_checks_seed_shape` (character_id lowercase-kebab, required fields); `test_cli_validate_exit_codes`. GREEN: `validate_brief_dir` + `python -m pipeline.frontdoor validate <dir>`.
6. **Golden fixtures + gap report.** Copy the dry-run concept + studio brief verbatim into `tests/fixtures/frontdoor/pinata/` (as `concept.md` / `00_studio_brief.md`), author `character_seeds.yaml` + `frontdoor.json` (minimal: slug/characters/stage_provenance) for it, and `manifest_pinata.yaml` registering kid/grandma/host-dad as minimal namespaces. (These fixtures **are** the structural eval bar; the *semantic* bar is §8.1.)
7. **Maya-gate acceptance test (honestly named, per A5).** RED: **`test_maya_plan_gate_accepts_frontdoor_brief`** — `pipeline.run.main(["--brief", <pinata-dir>, "--slug", "grandmaster", "--stub", "--manifest", <manifest_pinata>])` returns 0 and lands at the PLAN gate. This proves **Maya consumes the Studio Brief**, *not* that Cy can author or that it's GENERATE-ready — the `manifest_gap_report.md` names the remaining Cy work. GREEN once emit is correct.
8. **The skills (prose).** Author:
   - `brainstorm-front-door/SKILL.md` — orchestrator: spark → **micro-expand (3 premises / 3 style-tone routes / 3 risk questions)** → deepen? → INTERROGATE → SYNTHESIZE; owns the append-only locked-decisions block (§6); "when you have enough to act, act."
   - `frontdoor-interrogate/SKILL.md` — Grill Me one-at-a-time + always-recommend-your-answer + voiceprint generic-answer detector (push for a *named specific*) + CD 6-point North Star + discover-don't-ask.
   - `frontdoor-synthesize/SKILL.md` — to-prd synthesize-don't-interview → call `pipeline.frontdoor.emit`.
   - references: chain-map, session-sidecar-contract, studio-brief-contract, concept-doc-template, pinata-worked-example. **No unit test** — verified by the §8.1 semantic eval.
9. **Verification gate** (`superpowers:verification-before-completion`). `python -m pytest tests/test_frontdoor_*.py` green; `test_maya_plan_gate_accepts_frontdoor_brief` green; `python -m pytest tests/` shows no regressions; **both md5 guards byte-unchanged** (`2af75906…` / `945af824…`); `git status` clean except intended files. Then **run §8.1** and paste the scored result.

**Checkpoint 1 (Sean review — STOP here).** Two gates, both required:
- **Structural (CI):** the skeleton emits a brief dir that `validate_brief_dir` passes and Maya's plan gate accepts; full suite green; md5 guards intact.
- **Semantic (§8.1, blocking):** a captured live run of the orchestrator on the piñata spark, scored against the anti-pattern rubric — **not** a copied fixture. Sean reviews the three skills' voice + the *generated* brief before Slice 2.

### 8.1 The semantic anti-pattern rubric (per red-team A1 — the real quality gate)
Because prose can't be unit-tested and copied fixtures can go green on a flat brief, Checkpoint 1 is **blocked if the live-generated brief exhibits any of these** (drawn from what the dry-run got *right*):
1. **Generic grief** — the loss is abstract, not carried by a specific object/room/photo.
2. **Tough-grandma stereotype** — the grandmother is a cutout, not a specific person; comedy from the cutout, not the reveal.
3. **The kid is the joke** — the piece mocks the kid rather than the genre collision.
4. **Style route missing the candy-as-oil mechanic** — the signature Tartakovsky "blood" substitution absent from the routes.
5. **Timing bible absent** — no "timing is a song" / hold-then-burst directives in the non-negotiables.
6. **Concept too broad for Maya** — no single objective, no bounded format; Maya couldn't plan it.

The rubric is captured as `references/pinata-worked-example.md`'s companion checklist; the orchestrator self-checks against it at SYNTHESIZE and surfaces any hit, and Sean makes the final call. (This is the concrete eval that replaces "prose can't be tested.")

### Slice 2 — EXPAND (the "deepen" path)
No `spark.py` (cut, A4). EXPAND is the full fan-out the orchestrator reaches only when the human says "deepen" after the always-on micro-expand (§7).
- `frontdoor-expand/SKILL.md` — sw-creative borrow: **domain-rotation-every-10** (fights LLM semantic clustering), Topic→Generate→Cluster→Top-Picks, JTBD functional/emotional/social lens, "structural-not-narrative" qualifier. Returns only proposal fields (§6); the orchestrator locks the chosen avenue.
- **Validate (eval):** on `"a kid at a birthday party that feels like a samurai movie"`, "deepen" fans to ≥8 avenues across ≥4 domains before narrowing to 3–5 picks, then hands INTERROGATE a chosen avenue. Fixture #2 (the thin spark → the piñata avenue).

### Slice 3 — ART-VIZ + `genndy-tartakovsky` (v1 is prompt-only, per A3)
No `style_refs.py` (cut, A6). **v1 ART-VIZ spends nothing:** it writes ≥3 Flow-ready route prompts as prose in `concept.md`; the orchestrator records the chosen `style_route` id in `frontdoor.json`.
- `frontdoor-art-viz/SKILL.md` — **Flow $0 default, prompt-only** (the 3-route A/B/C pattern). **Live Higgsfield MCP is deferred behind an explicit spend gate:** the skill emits a cost estimate and refuses to call `generate_image` without the human typing `SPEND OK: Higgsfield <model> <count> <max-credits>`, and only when the stress verdict is `proceed`. **No live MCP in CI** — the tested surface is prose-route emission + the chosen-id field; the MCP path is never exercised by tests (fleet-ops).
- `genndy-tartakovsky/SKILL.md` — AKCodez scaffold (2-second hook → master template with `[BRACKETED]` vars → timeline segmentation → domain encyclopedia → 5 worked examples), filled from the concept doc's 8-directive timing bible; marketing flavor stripped. `references/timing-bible.md`.
- **Validate (eval):** writes the 3 style routes for the piñata landing-pose hero frame (Route A must carry the candy-as-oil mechanic — rubric item 4); the chosen id lands in `frontdoor.json`; a live render happens only through the spend gate.

### Slice 4 — STRESS-TEST
No `stress.py` (cut, A6). The verdict is prose in `concept.md` + a `stress_verdict: proceed|revise` enum in `frontdoor.json` (add the field to `handoff.py` here).
- `frontdoor-stress-test/SKILL.md` — pre-mortem Tiger/Paper-Tiger/Elephant (default-to-Tiger) + red-team steelman→"Fails if ___"→rank-by-(impact×likelihood×cheapness-to-test); "don't manufacture doubt" rule. Returns proposal fields only (§6); the orchestrator writes the verdict.
- **Validate (eval):** a **ships-red weak-concept fixture** yields ≥1 launch-blocking Tiger + a cheapest-test; the piñata yields `proceed` with named residuals (not a clean pass — it should flag the "tough grandma stereotype" and runtime risks the concept doc itself lists). Fixture #3.

## 9. The `genndy-tartakovsky` style skill (Slice 3 detail)
Built from the AKCodez shape (vetted markdown-only, 2026-07-02) **customized**, not imported; driven through the Higgsfield **MCP**, never their Playwright automation. Source content: the concept doc's "Genndy style + timing bible" (8 directives) + candy-mechanic + the 3 dry-run route prompts as worked examples. It feeds **both** engines (generates the prompt; Flow or Higgsfield renders). First of a per-project style-skill library (open thread — add per project).

## 10. Risks & downstream dependencies

- **Seeds → Cy → registration bridge (medium).** The front door's output is Maya-ready but not GENERATE-ready for *new* characters until Cy authors their Bibles and they're registered in the manifest. Cy's node also **requires a non-empty `source-refs/` directory** before it authors (R4). Slice 1 proves the Maya hand-off only. *Mitigation: (a) document it; (b) do not have the front door mutate `manifest.yaml` (a source-of-truth file); (c) **ART-VIZ's locked style frames double as Cy's `source-refs/` material** — the seed's `anchor_ref`/`style_ref_ids` carry them, partially closing the gap. A future slice may wire a full "front door → Cy authoring run".*
- **Skill prose can't be unit-tested (accepted).** Mitigated by the golden-fixture eval + the code-seam contract. The quality bar is the piñata brief, checked by a human at each checkpoint.
- **Adaptive-routing mis-classification (eliminated — A4).** The binary thin/rich classifier is cut; the always-on micro-expand (§7) has nothing to mis-route.
- **ART-VIZ silent cost (low, now enforced not just documented — A3).** v1 ART-VIZ spends nothing (prompt-only); a live Higgsfield render requires the explicit `SPEND OK: …` phrase + a cost estimate + a `proceed` stress verdict; no live MCP in CI (fleet-ops).
- **Over-engineering the chain (addressed by phasing).** Slice 1 is the *simpler chain* (3 skills) and already ships the piñata-grade brief; EXPAND/ART-VIZ/STRESS-TEST are additive, each gated on its own fixture. We never build a stage the fixture doesn't force.

## 11. Codex reconciliation notes

Codex's independent plan (session `019f246d`) converged strongly with this one: same orchestrator + 5 model-invoked stage skills; same finding that `pipeline.run` only requires `00_studio_brief.md` and that an authoring run needs `--slug` (Codex verified the same `run.py:174-191` lines); same call that the Python helpers are **support/contract code, not a new `pipeline.run` stage**; same 8-section Studio-Brief enforcement; same slice order; same Flow-$0-default / Higgsfield-on-demand / no-live-MCP-in-CI. Where we differed, the chosen call and why:

| # | Point | Opus draft | Codex | Chosen call + rationale |
|---|---|---|---|---|
| R1 | **Are the stages interactive markdown skills, or headless Python nodes?** | Interactive skills; the only tested code is the emit/validate seam. | Leaned on the Sam/Bea `stub_fn` + `invoke_opus_text` node pattern; proposed per-stage stubs and an "INTERROGATE stub-transcript" unit test. | **Interactive skills (Opus call).** The build plan is explicit: "a **standalone interactive session** (not a headless `run.py` stage)." You cannot unit-test an interactive grill as a stub transcript — who answers? The interview quality is an **eval against the piñata fixture**, not a unit test. So there is **no `invoke_opus_text` in the front door** and no per-stage `stub_fn`; the credential-free guarantee comes free because the code seam (emit/validate) is pure Python. *Adopted from Codex:* the silent-stub *discipline* — `frontdoor.json` records `stage_provenance` + a `mode` marker so a fixture-built brief in tests can't masquerade as a real interactive run. |
| R2 | **Concept doc: prose or typed object?** | Prose `concept.md` + a light template; validate non-empty + logline only. | A richly typed concept schema (`title_options[]`, `structure[]` acts, etc.). | **Prose (Opus call), with Codex's fields as the template checklist.** The dry-run concept doc is voice-bearing, museum-worthy prose; a typed object risks form-filling that flattens voice (same reason Sam loads the *verbatim* voice file, not a distillation; the eval handbook bars over-structuring creative output). Codex's field list is excellent as the **movements the `concept-doc-template.md` must prompt for**. A machine-readable `concept.meta.json` sidecar is **deferred (YAGNI)** — `frontdoor.json` already carries the only machine-needed fields (slug, characters, style_route, stress_verdict); add the sidecar only when ②/museum needs it. |
| R3 | **Character-seed schema.** | Minimal (name/role/design_notes/register/refs). | Richer, grounded in `character.yaml.template` + Cy's node: `character_id` (lowercase-kebab), `display_name`, `story_role`, `style_register`, `anchor_ref`, `source_notes`, `style_ref_ids`, `cy_target_dir`. | **Adopt Codex's schema** — it's better grounded (Codex read `character_designer.py:127-166` + the Bible templates). `source_notes` seeds Cy's `source-refs/notes.md`; `character_id` is lowercase-kebab per the template. |
| R4 | **The seeds → Cy bridge.** | Named as a medium risk; front door must not mutate `manifest.yaml`. | Sharpened it: **Cy's node requires a non-empty `source-refs/` directory** before it will author, plus `character_dir`. | **Adopt Codex's sharpening**, and add the bridge insight it implies: **ART-VIZ's locked style frames double as Cy's `source-refs/` material** — the front door writes chosen route renders into each character's seed `source_notes`/`style_ref_ids`, partially closing the gap. Full closure (a "front door → Cy authoring run") stays a future slice; Slice 1 proves only the Maya hand-off. |
| R5 | **Stub precedent.** | Reuse `ANIMA_FORCE_STUB` (already exported by `pipeline.run --stub`). | Grounded the pattern in `sdk_runners.py:377-414` + `_stub_sam_text` / `_make_bea_stub`. | **Both, correctly scoped:** the *acceptance* test uses `pipeline.run --stub` (→ `ANIMA_FORCE_STUB`) so PLAN is stubbed; the front-door code seam itself needs no stub (pure Python). Codex's precedent is the reference if any front-door helper ever calls a model (none does today). |

Net: the plan above already reflects R2–R5 folds; R1 is the one place I explicitly hold my call against Codex, and it is the load-bearing architectural decision — **the front door is interactive skills over a pure-Python contract seam, not a headless node chain.**

## 12. Red-team fold (Codex adversarial review)

Codex adversarially attacked this doc (session `019f2472`). Six of eight findings materially improved the plan and are **folded into the sections above**; two are refined rather than adopted. The folds:

| Fold | From findings | What changed | Where |
|---|---|---|---|
| **A1 — Checkpoint 1 is quality-gated, not structure-gated.** | #1, #8 | Copied golden fixtures + structural validators can go green on a *flat, generic* brief. Checkpoint 1 now **requires a captured live orchestrator run on the piñata spark, scored against a semantic anti-pattern rubric** (the six "worse-than-piñata" red cases). CI stays structural; the human checkpoint is the blocking quality gate. | §8 Slice 1 step 9 + the new **§8.1 semantic rubric** |
| **A2 — Hard stage I/O contract (the boundary is now real, not ceremony).** | #2 | "Reads/appends the whole sidecar" let any stage smuggle a global decision. Now: **a stage may return only `observations`, `options`, `recommendation`, `open_questions`; only the orchestrator writes `chosen_route`, `skip_stage`, `locked_style`, `stress_verdict`, `stage_provenance`; locked decisions are append-only.** | §6 |
| **A3 — ART-VIZ v1 is prompt-only ($0); live render is spend-gated.** | #3, #4 | `--stub` protects `pipeline.run`, not arbitrary MCP calls from a model-invoked skill. **v1 ART-VIZ emits Flow-ready prompts + route text only — no MCP call.** Live Higgsfield is deferred behind an explicit human phrase `SPEND OK: Higgsfield <model> <count> <max-credits>` preceded by a cost estimate, and gated on a `proceed` stress verdict. This keeps Sean's canonical stage order (STRESS at 4) cost-safe without reordering. | §5.5, §8 Slice 3 |
| **A4 — Cut the thin/rich classifier; always micro-expand.** | #5 | A binary `classify_spark` mis-routes (rich-in-plot-poor-in-style; a thin spark with one fragile high-value intuition EXPAND would dilute) and human confirmation invites default-accept. Replaced with an **always-on micro-expand** (3 alternate premises / 3 style-tone routes / 3 risk questions), then "deepen?" The micro-expand ships in **Slice 1** (gives the skeleton the dry-run's "lead with divergence" without building full EXPAND); Slice 2's full fan-out is the "deepen" path. **`spark.py` is cut.** | §7, §8 Slice 1 + Slice 2 |
| **A5 — Honest acceptance-test naming + a gap report.** | #6 | "Proves the whole contract" overstated — it proves Maya consumes free text with a test manifest, not that Cy can author or that it's GENERATE-ready. Test renamed **`test_maya_plan_gate_accepts_frontdoor_brief`**; the emit writes a **`manifest_gap_report.md`** listing unregistered seed characters + the next Cy action. | §8 Slice 1 steps 6–7 |
| **A6 — Trim the code seam (kill schema theater).** | #7 | Keep only `brief.py`, `handoff.py` (minimal), `emit.py`, `validate.py`, `cli.py` (`validate` only). **Cut `seeds.py`** (seed shape validated inline in `validate.py`), **`spark.py`** (A4), **`style_refs.py`, `stress.py`** (style routes + stress verdict become **prose in `concept.md` + one enum field each in `frontdoor.json`**), and the `scaffold` subcommand. | §4, §5.5 |

**Two refined, not adopted verbatim:**
- **#4 (reorder / split ART-VIZ).** Rejected the reorder — Sean named the stage order (EXPAND→INTERROGATE→ART-VIZ→STRESS-TEST→SYNTHESIZE). A3 neutralizes the cost concern *within* that order (v1 ART-VIZ spends nothing; any future live render is gated on the stress `proceed`), which achieves the same protection without overriding the named sequence.
- **#7 (defer `frontdoor.json` entirely).** Rejected full deferral — `frontdoor.json` has **two immediate Slice-1 consumers**: the orchestrator reads `slug` to invoke `pipeline.run --slug`, and `manifest_gap_report.md` reads `characters`. Kept **minimal** (slug / characters / stage_provenance); `style_route` + `stress_verdict` fields are added only when Slice 3/4 land — so it grows with real consumers, not ahead of them.

## 13. Anti-drift note
Tier-2's DoD is met; per the ROADMAP locked sequence, **① is the active build** and this is its spec. ②'s daemon foundation is the parallel-safe next slice (its own plan). ③ (cost) runs alongside as a decision. The order holds; this plan opens no second workstream.
