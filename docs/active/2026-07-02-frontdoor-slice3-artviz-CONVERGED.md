# Front Door (①) — Slice 3: ART-VIZ (the style stage) — Converged Build Plan (Opus + Codex)

> **For agentic workers:** REQUIRED SUB-SKILL — use `superpowers:test-driven-development` per code task (red → verify-red → green → verify-green → refactor) and `superpowers:verification-before-completion` before any "done". Steps use checkbox (`- [ ]`) syntax.

**Date:** 2026-07-02
**Status:** Planning — the executable spec for Slice 3 of ①. **Plan only; no implementation code this session.**
**Builds on:** [2026-07-02-frontdoor-slice2-expand-CONVERGED.md](2026-07-02-frontdoor-slice2-expand-CONVERGED.md) (the METHOD model + the inline-discipline precedent) and [2026-07-02-frontdoor-build-plan-CONVERGED.md](2026-07-02-frontdoor-build-plan-CONVERGED.md) (§5.5 / §8 Slice-3 sketch — treated as hypotheses, not settled requirements).
**Primary evidence:** the FOUR by-hand/live ART-VIZ runs — the "3 style routes" + "style + timing bible" + "money shot" sections of the piñata concept ([`2026-07-02-frontdoor-dryrun-pinata-short-concept.md`](2026-07-02-frontdoor-dryrun-pinata-short-concept.md)) and the ai-guru concept ([`briefs/2026-07-02-ai-guru-pilot/concept.md`](../../.claude/worktrees/frontdoor-slice1/briefs/2026-07-02-ai-guru-pilot/concept.md)), plus both docs' "Open threads" (the STRESS-TEST proto-runs).
**Co-planned with:** Codex (independent plan §11) + adversarial red-team (§12). **See §2 for where the evidence overrode the §8 sketch.**

---

## 1. The one-sentence goal

Formalize the front door's **style stage** ("ART-VIZ" in Sean's locked chain) as an **inline orchestrator discipline** — write ≥3 mutually-distinct, Flow-ready style-route prompts as **prose in `concept.md`** (folded there by the existing SYNTHESIZE writer), each rendering the piece's signature hero frame with its **signature mechanic rendered in-frame or captured in the concept doc's money-shot prose — never dropped**, flag any register anima can't yet build, and record the route Sean picks — **without adding a `frontdoor-art-viz` skill, without building the `genndy-tartakovsky` style skill, without any spend, and without one byte of new `pipeline/frontdoor` code.**

## 2. The position: ART-VIZ is an inline discipline; the style skill + the spend path defer

Six claims, ordered by how hard the evidence pushed on the §8 sketch.

### 2.1 ART-VIZ is an inline orchestrator discipline, NOT a `frontdoor-art-viz` skill

**All four runs produced the style routes inline as prose Route A/B/C in `concept.md`, with no ART-VIZ skill in existence.** That is the same evidence shape that reversed EXPAND in Slice 2 (§2.2 there), and it points the same way. The decisive facts:

- **The job is a bounded authoring move, not a sustained distinct interaction mode.** INTERROGATE earns a skill because it is a *long, sustained one-at-a-time grill* — a genuinely different way of behaving that the orchestrator should not inline. SYNTHESIZE earns a skill because it is *synthesize-don't-interview* + it owns the emit-seam call. ART-VIZ is neither: it is "write three route prompts, each carrying the money shot, flag the un-buildable register, record the pick." That is a section of the concept doc, not a mode-switch — and both live runs wrote it exactly that way, inline.
- **A separate skill would step out of the room for no capability.** The style routes live *inside* `concept.md`, which SYNTHESIZE already emits. Carving the route-writing into its own model-invoked skill means raise-open_question → invoke sibling → return — heavier machinery than what worked, and the exact "steps out of the room" cost the Slice-2 red-team flagged (F8 there). Zero of four runs needed it.
- **The meta-lesson binds here.** A named stage is not automatically a skill. EXPAND is now evidence-backed twice as an inline discipline; ART-VIZ has the *same* four-run inline record and the *weaker* case for a skill (it does not even have EXPAND's "used at many trigger points" property — it runs once, in one place).

**So: Slice 3 ships ART-VIZ as an inline discipline** — a new orchestrator `SKILL.md` step + a `good-art-viz-rubric.md` reference, mirroring exactly how Slice 2 shipped EXPAND. **Promotion trigger (YAGNI-honest):** promote to a standalone `frontdoor-art-viz` skill only if ≥2 live runs show inline route-writing demonstrably underperforming (thin routes, dropped signature mechanic, routing confusion). We have four runs of the opposite.

### 2.2 The `genndy-tartakovsky` style skill is DEFERRED — it has no consumer, and it belongs to the Cy/generation layer

The §8 sketch made the `genndy-tartakovsky` style skill a Slice-3 deliverable. **The evidence says defer it, on two independent grounds:**

- **No consumer exists.** Both concept docs are **$0 dry-run spikes** — the piñata was never greenlit, and the ai-guru pilot is exploratory. A style-prompt library with no production run consuming it is exactly the speculative artifact the doctrine warns against ("the closed vocabulary is extended deliberately, not inline") and the Slice-2 red-team cut as over-build. Building the AKCodez scaffold now is building ahead of a real need.
- **It is not a front-door artifact.** A style skill is a *reusable prompt library for a specific look* — "first of a per-project style-skill library" (build-plan §9). That is a **Cy/generation-layer** asset, authored when a piece is greenlit and Cy needs it as `source-refs/` material. The front door's job is to *decide the route and hand Cy the seed*; it is not to build Cy's tooling.

**What Slice 3 ships instead:** the ART-VIZ discipline captures the piece's **timing/craft bible + signature mechanic as prose** in `concept.md` (the piñata's 8 directives + candy-as-oil; the ai-guru's 8 + Orby-glitch) and in the Studio Brief's non-negotiables — **exactly what both runs already did**. The style-skill *shape* (the AKCodez scaffold: 2-second hook → `[BRACKETED]` master template → timeline segmentation → domain encyclopedia → worked examples) is named in the rubric as the *deferred* target the first greenlit piece will fill. **First real style skill rides the first greenlit piece's Cy authoring run**, not Slice 3.

### 2.3 Slice 3 spends nothing and builds no render path

v1 ART-VIZ is prompt-only (build-plan §12-A3). Slice 3 holds that line and goes further: **it does not build the SPEND OK gate or the Higgsfield MCP render path at all.** Two reasons the parent plan did not fully weigh:

- **The spend gate's gating input does not exist yet.** The parent design gates a live render on a `proceed` **stress verdict** — a STRESS-TEST output. STRESS-TEST is **Slice 4, not built.** Building a spend gate in Slice 3 means building machinery whose precondition is a stage that has not shipped.
- **No greenlit piece wants an in-session render.** Both runs stayed as **Flow-ready prompts** — no image was ever rendered inside the session; Sean would run the routes on his $0 Flow subscription himself and pick. That is the Grill-Me `prototype` pattern done at zero cost: emit ≥3 variations (route prompts), the human renders + switches, keep the verdict (the chosen id), discard the rest.

**So Slice 3 is $0, no MCP, no spend gate, no live call in CI (fleet-ops holds trivially — there is nothing to gate).** The SPEND OK gate + Higgsfield render is specified as **deferred design** in §7.4 so it is ready to build the day a greenlit piece + a shipped STRESS-TEST verdict both exist — the two grow together.

### 2.4 No new `pipeline/frontdoor` code; the chosen route needs no `style_route` field

The §5.5 hypothesis records the chosen route as a `style_route` id in `frontdoor.json`. **Applying the no-schema-theater discipline (add a field only when a real consumer reads it) kills it:**

- **Nothing reads `style_route`.** `pipeline.run` reads `--slug`; the gap report reads `handoff.characters`; Cy reads the *character seeds*' `anchor_ref` / `style_ref_ids`, **not** `frontdoor.json.style_route`. There is no machine consumer for a top-level chosen-route field. (`Handoff.from_json` *rejects* unknown fields, so adding it is not free — it is a real schema commitment for a value nothing consumes.)
- **The chosen route already has a schema-sanctioned home.** When Sean picks (and, later, renders) a route, its ref lands in the seed's **`anchor_ref` / `style_ref_ids`** — fields **already optional-and-permitted** in `validate.py` (`REQUIRED_SEED_FIELDS` omits them; unknown-but-present is not rejected). **Honest scope (red-team F6, verified against `main`):** these are the *future Cy landing spot* — **passthrough today; no pipeline code reads `style_ref_ids` yet** (`git grep style_ref_ids -- pipeline/` on `main` = empty). So they are not an *active* machine consumer — but they are the seed schema's declared home for a rendered route, and populating them is a no-code change. Crucially, `style_route` has no such home and no consumer at all — so the seed fields, not a new top-level field, are where a chosen route belongs.
- **The record of "the style stage ran" is a provenance string, not a field.** `stage_provenance` gains an `art-viz` entry (and, if a route is chosen, that is the whole record) — proven in Slice 2 to round-trip with **zero** schema change (provenance strings are values, not fields; pinned by `tests/test_frontdoor_handoff.py`).
- **One existing skill + one template contradict this call and must be fixed (red-team F1/F2).** `frontdoor-synthesize/SKILL.md` (the stage that actually writes `concept.md` + seeds) still hardcodes `anchor_ref: null` / `style_ref_ids: []`, and `concept-doc-template.md` says "Route letters become `style_route` ids." Slice 3 **edits both** (§8, Task 2) — SYNTHESIZE to fold the ART-VIZ proposals + populate the seed refs only when real refs exist; the template to say route letters are prose/locked-decision handles, **no `style_route`**. These are prose edits to skill/reference files, not code.

**So `pipeline/frontdoor/` stays byte-identical** — Slice 2's proof-point holds a second time. Slice 3 is prose + rubric + three tiny tests. A `style_route` field is deferred to the slice that builds a real consumer (the museum/handoff wiring or the spend gate), same discipline as Slice 1's A6 and Slice 2's no-module call.

### 2.5 ART-VIZ SURFACES the un-buildable register; it does not own the doctrine extension

The live front door already **surfaces** registers anima can't build and **routes the fix to Cy** — proven twice: ai-guru's `90s-nicktoon-grossout` (carried into both seeds' `style_register` + `source_notes` with the doctrine pointer) and grandmaster's Tartakovsky flat-no-outline `[L14]`. **Slice 3 keeps that split, it does not close it:**

- **ART-VIZ's job is to flag, not to extend.** A rubric criterion (mirroring good-EXPAND #6) requires every route to surface a register anima can't yet build as an `open_question` + a seed `style_register` NEW-flag + the doctrine pointer. That is the discipline; the run already exhibits it.
- **The doctrine 3-step extension rides a real Cy authoring run.** Extending `pipeline/criteria.py`'s closed vocabulary → adding the `## What good looks like — {register}` block to `cy-character-designer-context.md` → updating `tests/test_prompt_style_neutrality.py` markers is a **Cy-layer change gated on a real Bible authored against that register.** Doing it speculatively in Slice 3, for a register no greenlit piece uses, is precisely the "extend inline" the doctrine forbids. **Slice 3 does not touch `criteria.py` or the neutrality test.**

### 2.6 The eval is Slice 1/2's honest split — a tiny structural seam + a live good-ART-VIZ rubric

Route quality is prose/taste; it is **not** a CI assertion (the Slice-2 red-team cut every prose-grep as theater). The split (§7):
- **Structural (CI, no keys):** three tiny tests — an `art-viz` provenance round-trip (no module needed), a chosen-route seed *passthrough* round-trip (the future Cy landing spot, no code), and a *generic* unknown-field rejection (pinning the deliberately-not-widened schema, red-team F5). The first two are honestly-labeled characterizations; they pin the no-code contract, they do not "prove ART-VIZ ran."
- **Semantic (live, blocking — Sean's eye):** the **good-ART-VIZ rubric** — a live human-review checklist, never a CI/self-pass gate — with the piñata + ai-guru route sets as its worked positives. **The non-negotiable across both runs: the piece's signature mechanic is never dropped** — rendered in the hero frame (ai-guru's Orby-glitch) or captured in the concept doc's money-shot/timing-bible prose when the hero frame is a pre-mechanic beat (piñata's landing pose, candy-as-oil in the money-shot section — **not** painted into the routes; red-team F3). Three criteria block together (fixed-frame-distinct-registers + mechanic-not-dropped + Flow-ready prompt; red-team F4).

## 3. Architecture — an inline discipline over the untouched Slice-1/2 seam

**No new skill. No new `pipeline/frontdoor` code. No spend.** Slice 3 is: (A) prose that specifies the inline ART-VIZ discipline in the orchestrator `SKILL.md`, flips the chain-map ART-VIZ row from `frontdoor-art-viz`/Slice-3 to **inline/live**, and adds the rubric reference; and (B) a small amount of *test + fixture* work that pins the no-code contract and adopts the two route sets as the rubric's reference material. The Slice-1/2 seam already carries everything ART-VIZ produces:

- Route options + the chosen-route recommendation live in the sidecar **PROPOSALS LOG** (the four-kinds contract already holds them — `options` = the routes, `recommendation` = the lean, `open_questions` = the un-buildable-register flag). SYNTHESIZE folds the routes into `concept.md`'s "3 style routes" section, exactly as it folds everything else.
- The chosen route is a **LOCKED DECISION** (orchestrator-written, after Sean picks) and, when rendered, populates the seed's already-permitted `anchor_ref` / `style_ref_ids`.
- `stage_provenance: [..., "art-viz", ...]` validates and round-trips with **zero code change** (the Slice-2 verification of provenance-as-values applies unchanged).

**Verify-the-no-code-claim discipline (Slice-2 F7):** the build session confirms against the built seam — `Handoff(stage_provenance=[..., "art-viz", ...])` round-trips through `to_json`/`from_json`; a seed with `anchor_ref` set + `style_ref_ids: ["route-c"]` passes `validate_brief_dir`; unknown *fields* still reject. State the actual runtime contract; do not overstate it.

## 4. The ART-VIZ discipline ↔ the style skill (two layers, only one built now)

| | **ART-VIZ (Slice 3 — inline discipline)** | **`genndy-tartakovsky` style skill (deferred — Cy/generation layer)** |
|---|---|---|
| What | Decide the look: ≥3 distinct Flow-ready route prompts + the signature mechanic + the chosen lean | A reusable prompt library for one look (the AKCodez scaffold, filled) |
| Where | Inline in the orchestrator, prose in `concept.md` | Its own skill folder, authored when a piece is greenlit |
| Consumer | Sean (picks the route); Cy (the seed's `source_notes` / `style_ref_ids`) | Cy / the generation layer, on a real production run |
| Built when | **Slice 3 (now)** | The first greenlit piece's Cy authoring run — **not now** |
| Owns the register extension? | **No** — surfaces it only (§2.5) | The doctrine 3-step rides *its* authoring run |

The ART-VIZ discipline **captures the timing bible + money shot as prose today**; the style skill would later *extract* that prose into a `[BRACKETED]`-templated library. Building the library before a piece consumes it inverts the order the evidence supports.

## 5. Flow placement: nominally third, one inline step between INTERROGATE and SYNTHESIZE

Sean **locked** the nominal order (`EXPAND → INTERROGATE → ART-VIZ → STRESS-TEST → SYNTHESIZE`). Slice 3 realizes ART-VIZ's slot **without a reorder and without a skill invocation:**

- A new **Step 2.5 — ART-VIZ (inline)** sits between INTERROGATE (Step 2) and SYNTHESIZE (Step 3) in the orchestrator `SKILL.md`, and in the chain diagram.
- **Skip condition (kept from the chain-map):** a piece with a locked register already (e.g. an act inside an existing piece) skips ART-VIZ — declared skipped in `stage_provenance`, never silently faked.
- Like every stage, ART-VIZ **proposes** (routes = `options`, lean = `recommendation`, un-buildable register = `open_questions`); **Sean picks; the orchestrator locks.** Control never leaves the room.

## 6. The propose-vs-decide boundary — prose + sidecar convention (not a lint)

Unchanged from Slice 1/2, and enforced the same way: ART-VIZ **proposes** the routes and a lean; it **never locks** the style. Only the orchestrator writes the LOCKED DECISION (the chosen route), append-only, after Sean decides. **How it is enforced/tested:** by prose discipline in the orchestrator + the append-only sidecar convention + human review — **not** a unit test and **not** a "route-shape lint." A markdown parser asserting "concept.md has ≥3 route bullets each containing the mechanic word" gives false confidence (a flat route that name-drops "candy" passes; a superb route phrased differently fails) — the same test theater the Slice-2 red-team cut (F4). The honest split holds: the **seam** is unit-tested; the **discipline** is a live rubric + Sean's eye.

## 7. Eval strategy — the honest split, grounded in both runs

**The seam is unit-tested (CI-green, credential-free); route *quality* is a live rubric eval (blocking human checkpoint).** No model transport, no MCP, no spend in any test.

### 7.1 Structural (CI, no keys) — deliberately tiny
Because ART-VIZ adds **no code and no schema**, there is almost nothing new to assert — and that thinness is the finding, not a gap. Three tiny tests, all honestly scoped:
- **`art-viz` provenance round-trips** (Task 1a, a *characterization*): `Handoff(stage_provenance=["micro-expand","interrogate","art-viz","synthesize"], …)` round-trips through the seam — the machine proof no `art_viz.py` module is needed. It passes on first run; that greenness *is* the finding (§3).
- **Chosen-route passthrough** (Task 1b, a *characterization* — relabeled per red-team F6): a `character_seeds.yaml` seed with `anchor_ref: "characters/<id>/source-refs/route-c.png"` + `style_ref_ids: ["route-c-hybrid"]` passes `validate_brief_dir` and round-trips through `emit_brief_dir` — proving the chosen route **passes through** already-permitted seed fields with byte-identical code. Sold as *seed passthrough / the future Cy landing spot*, **not** "a real current Cy consumer" (nothing reads it yet).
- **Generic unknown-field rejection** (Task 1c — added per red-team F5): the plan's no-`style_route` argument leans on `Handoff.from_json` rejecting unknown fields, but `test_frontdoor_handoff.py` on `main` has **no such test** (it has `test_rejects_unknown_mode` — an unknown *value*, not an unknown *field*). Add one **generic** test: `from_json` on a payload with an extra field (e.g. `{"…", "style_route": "x"}`) raises with `unknown frontdoor.json fields`. Generic, not a `style_route` magic-word assert (that would be the prose-grep theater F5 warns against) — it pins "the schema is deliberately not widened."
- **Cut (pre-empting the red-team):** any "concept.md carries a ≥3-route section" validator (prose-grep theater); any `style_route`-*specific* field test; any style-skill contract test (no skill is built).

### 7.2 Semantic (live, blocking — the real quality gate): the good-ART-VIZ rubric
A **captured live ART-VIZ run** scored against the **good-ART-VIZ rubric** — the divergence-side companion is `good-expand-rubric.md`; this is the style-side companion, same discipline (a live human-review checklist for Sean, **never** a CI/prose/self-pass gate). Sean runs the live session; Slice 3 ships the **rubric + validation protocol**. A good ART-VIZ pass exhibits **all six**:

1. **One fixed hero frame, ≥3 mutually-distinct registers** — the routes hold the *composition* constant (the landing pose; Aiden mid-glitch with Orby on the laptop) and vary only the *rendering language*, so it is a true look-to-look comparison — and the registers are mutually distinct (anti-clustering), not one look reworded. Both runs do exactly this ("Same composition, rendered in [register]"; Codex fold, §11). *Judged by Sean, live.* — Worked positive: piñata's Samurai-Jack-faithful / Primal-grit / hybrid-pencil are three different rendering languages over one landing-pose frame. Anti-example: three "Genndy-ish" routes that differ only in adjective, or three routes that also change the composition (nothing to compare).
2. **The signature mechanic is never dropped** — **the anima-specific bar.** Two honest shapes (red-team F3): when the hero frame *is* the mechanic moment, every route renders it (ai-guru's Aiden-mid-glitch-with-Orby-watching); when the hero frame is a pre/post-mechanic beat, the mechanic is **explicitly captured in the concept doc's money-shot + timing-bible prose and carried into the non-negotiables** (piñata's landing pose renders the *pose*, with candy-as-oil locked in the "candy mechanic (the money shot)" section — the routes do **not** paint the geyser, and that is fine because the mechanic is captured, not lost). Anti-example: a route pass that renders the pose and the money-shot prose **omits** the candy-as-blood substitution entirely (build-plan §8.1 red #4) — the mechanic dropped, not relocated.
3. **Each route is a self-contained, Flow-ready prompt** — a named specific someone could paste into Flow and get the hero frame, not "a Samurai-Jack-style route." Anti-example: a category label with no renderable prompt.
4. **The timing/craft bible is captured as prose** — the piece's spine directives land in `concept.md` + the Studio Brief non-negotiables (piñata's 8 directives; ai-guru's 8). Anti-example: routes with no "timing is a song" / hold-then-burst discipline recorded (build-plan §8.1 red #5).
5. **The personal-lineage route is present** — both runs offered a "fuse with anima's own pencil-test warmth" route (piñata Route C; ai-guru Route C) — the "most Sean" option. *Soft criterion — a taste default, not a hard bar; its absence is a finding, not a block.*
6. **Un-buildable registers surfaced as `open_questions`** — a register outside the six-vocabulary is flagged (seed NEW-flag + doctrine pointer), not waved through (§2.5). Anti-example: a photoreal route recommended with no word that anima has no photoreal register.

**Blocking rule (tightened per red-team F4):** criteria **1, 2, and 3 block together** — a single "signature mechanic" bar is gameable (three clustered, non-renderable, same-ish prompts can name-drop the mechanic and pass), so the block requires all three: **one fixed hero frame in ≥3 genuinely distinct registers (1)** + **the mechanic not dropped (2)** + **each route a self-contained, Flow-ready prompt (3)**. Still Sean's live judgment, not a CI lint. Criteria 4–6 are findings to fold at Sean's call.

### 7.3 Fixture decision: adopt both runs' route sets as the rubric's worked positives
**Adopt** — the piñata A/B/C and ai-guru A/B/C route sets become the good-ART-VIZ rubric's worked positives (and the anti-examples are their negations), exactly as good-EXPAND uses the ai-guru workshop block. They are **reference material for the rubric, not machine-asserted fixtures** (no CI oracle for route quality). Both already live in committed/worktree concept docs; the rubric quotes them.

### 7.4 Deferred design — the SPEND OK gate + Higgsfield render (NOT built in Slice 3)
Specified now so it is ready when a greenlit piece + a shipped STRESS-TEST verdict both exist:
- **Trigger:** only after ART-VIZ has proposed routes AND the STRESS-TEST `stress_verdict` is `proceed` AND Sean types the exact phrase `SPEND OK: Higgsfield <model> <count> <max-credits>`.
- **Behavior:** emit a cost estimate first; refuse to call `generate_image` without the phrase; on the phrase, render the chosen route's hero frame via the Higgsfield MCP; write the render into the chosen seed's `anchor_ref` / `style_ref_ids`.
- **CI:** never exercised — no live MCP in tests (fleet-ops). Built in a later slice with the stress-verdict consumer, not now.

## 8. File layout (Slice 3 — prose + rubric + three tiny tests; no skill, no `pipeline/frontdoor`, no spend)

```
.claude/skills/brainstorm-front-door/
  SKILL.md                              # EDIT — insert Step 2.5 ART-VIZ (inline discipline) between
                                        #        INTERROGATE and SYNTHESIZE; update the chain diagram
  references/
    chain-map.md                        # EDIT — ART-VIZ row: frontdoor-art-viz/Slice-3 → inline/live;
                                        #        keep the "locked register" skip; note the promotion trigger
    good-art-viz-rubric.md              # NEW  — the six-criterion live-review rubric + validation protocol
    session-sidecar-contract.md         # EDIT — name the art-viz proposals shape (### art-viz block)
    concept-doc-template.md             # EDIT (required, red-team F2) — "Route letters become style_route
                                        #        ids" → route letters are prose/locked-decision handles;
                                        #        NO frontdoor.json.style_route; rendered refs → seed refs
.claude/skills/frontdoor-synthesize/
  SKILL.md                              # EDIT (required, red-team F1) — fold ### art-viz proposals into
                                        #        concept.md; carry the chosen-route lock as prose; add
                                        #        art-viz to provenance when present; populate seed
                                        #        anchor_ref/style_ref_ids ONLY when real refs exist

tests/
  test_frontdoor_handoff.py             # EDIT — art-viz provenance characterization (1a) +
                                        #        generic unknown-field rejection test (1c, red-team F5)
  test_frontdoor_emit.py  (or _validate.py)  # EDIT — chosen-route seed passthrough characterization (1b)
```

**No `frontdoor-art-viz/` skill. No `genndy-tartakovsky/` skill. No `style_route` field, no `art_viz.py`, no `criteria.py`/neutrality-test change, no MCP/spend code, no route-shape lint.** Nothing under `pipeline/frontdoor/` changes. `git status` at Checkpoint 3 shows only the paths above. (The two required skill/template edits are what shift the slice from the red-team's UNDER-BUILT to right-sized — the inline contract now reaches the writer that emits the routes.)

## 9. Per-slice TDD task list

Discipline every code task: `superpowers:test-driven-development`; tests run **per-directory from repo root** (`python -m pytest tests/`); commit at each task end; `superpowers:verification-before-completion` before "done"; **both md5 guards byte-unchanged** — Slice 3 touches neither:
`evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4`;
`pipeline/agents/prompts/sean-screenwriting-voice.md` = `945af824fa53b948a18ac6bf206d67ef`.

### Pre-flight (worktree)
- [ ] **P0.** Branch the Slice-3 worktree from **local `main`** (which carries Slices 1+2 at `bb49144`; local main is ahead of `origin/main` and unpushed — branch from local main, no merge pre-flight). Use `superpowers:using-git-worktrees` (detect native isolation first; verify the dir is gitignored). Confirm `python -m pytest tests/` green before writing anything. Confirm this CONVERGED doc is present on the worktree's branch (land it on main first if needed).

### Task 1 — The no-code characterizations (the "no module, no field" proof)
**Files:** Modify `tests/test_frontdoor_handoff.py`, `tests/test_frontdoor_emit.py` (or `_validate.py`).
**Interfaces consumed:** `Handoff` (round-trip); `validate_brief_dir`; `emit_brief_dir` / `BUNDLE_FILES`.

- [ ] **1a. Art-viz provenance characterization** (a *characterization*, honestly labeled — synthetic, not proof of a live run):
```python
from pipeline.frontdoor.handoff import Handoff

def test_stage_provenance_carries_art_viz_with_no_schema_change():
    """Characterization: the seam already carries an 'art-viz' stage entry — no art_viz.py needed.
    Synthetic (a real run would interleave it); proves the CONTRACT, not a run."""
    h = Handoff(slug="grandmaster", characters=["kid", "grandma", "host-dad"],
                stage_provenance=["micro-expand", "interrogate", "art-viz", "synthesize"],
                mode="interactive")
    assert Handoff.from_json(h.to_json()) == h
```
- [ ] **1b. Chosen-route passthrough characterization** — a seed carrying a chosen route's `anchor_ref` + `style_ref_ids` validates + round-trips through emit (proving the chosen route passes through already-permitted seed fields, byte-identical code). Build a minimal valid brief dir in a tmp path (or extend the pinata/ai-guru fixture path) whose `character_seeds.yaml` has one seed with `anchor_ref` set + `style_ref_ids: ["route-c-hybrid"]`; assert `validate_brief_dir(dir) == []` and the emitted seed round-trips. Label it **passthrough / future Cy landing spot** (red-team F6) — not a current-consumer proof.
- [ ] **1c. Generic unknown-field rejection** (red-team F5 — the plan's no-`style_route` argument had no test behind it). RED: assert `Handoff.from_json('{"slug":"x","characters":["a"],"stage_provenance":["s"],"nonesuch":1}')` raises `ValueError` mentioning `unknown frontdoor.json fields`. Verify it fails only if the guard is absent/schema widened. GREEN: it passes today (the behavior exists; the *test* did not). **Generic — never a `style_route`-specific magic-word assert.**
- [ ] **1d. Verify + commit.** 1a/1b pass on first run — that greenness is the finding (§3); 1c pins the deliberately-not-widened schema. `python -m pytest tests/test_frontdoor_handoff.py tests/test_frontdoor_emit.py -v`. `git commit -m "test(frontdoor): pin art-viz provenance + chosen-route seed passthrough + generic unknown-field rejection"`

### Task 2 — Specify the inline ART-VIZ discipline + reach the SYNTHESIZE writer (prose — the real deliverable)
**Files:** Modify `.claude/skills/brainstorm-front-door/SKILL.md`, `.../references/chain-map.md`, `.../references/concept-doc-template.md`, `.../references/session-sidecar-contract.md`, **and `.claude/skills/frontdoor-synthesize/SKILL.md`** (the writer — red-team F1). Prose — verified by the Checkpoint-3 live rubric eval, not a unit test (Slice-1/2 precedent).

- [ ] **2.1 Insert Step 2.5 — ART-VIZ (inline, no skill call)** into `SKILL.md`, between INTERROGATE (Step 2) and SYNTHESIZE (Step 3): *once the North Star is locked, propose the look — in place, without leaving the room: pick one hero frame (the piece's signature moment) and write ≥3 mutually-distinct, Flow-ready route prompts that render **that same composition** in different registers (a faithful homage, a grittier sibling, a personal-lineage fusion with anima's own pencil-test warmth) — vary the rendering language, not the frame, so Sean compares looks apples-to-apples; **the piece's signature mechanic is never dropped** — rendered in the hero frame when the frame is the mechanic moment (ai-guru's Orby-glitch), or captured in the money-shot/timing-bible prose when the frame is a pre-mechanic beat (piñata's landing pose, candy-as-oil in the money-shot section); each route a self-contained prompt Sean could paste into Flow; capture the piece's timing/craft bible as prose (it also seeds the Studio Brief non-negotiables); flag any register anima can't yet build as an `open_question` + a seed `style_register` NEW-flag + the doctrine pointer. Append only the four proposal kinds; Sean renders on Flow and picks; **you** lock the chosen route and record `art-viz` in `stage_provenance`. **This is a $0 prompt-only stage — you never render or spend; Sean runs Flow himself.*** **The no-library operating rule (red-team F7):** draw the route language from the locked references, the timing bible, and the character seeds' `source_notes` — the material already in the room; if that reference knowledge is missing for a route, **raise an `open_question`; do not invent a reusable style doctrine** (that is the deferred style skill's job, on a real Cy run). Add ART-VIZ to the chain diagram. State plainly: **not** a skill call; the `genndy-tartakovsky` style skill is a deferred Cy-layer asset, not built here.

- [ ] **2.2 Edit `concept-doc-template.md` (required — red-team F2).** Movement 8 currently reads "Route letters become `style_route` ids" — a direct contradiction of §2.4. Change it to: *route letters are prose labels / locked-decision handles; there is **no** `frontdoor.json.style_route`; a rendered route's ref later lives in the chosen character seed's `anchor_ref` / `style_ref_ids`.* Keep the "≥3 render-ready, visually distinct" movement.
- [ ] **2.3 Edit `frontdoor-synthesize/SKILL.md` (required — red-team F1, the load-bearing fold).** SYNTHESIZE is the stage that actually writes `concept.md` + seeds; on `main` it hardcodes `anchor_ref: null` / `style_ref_ids: []` and reads only the template. Teach it to: (a) fold the sidecar's `### art-viz` proposals into `concept.md`'s Style-routes + timing-bible + money-shot movements (the routes are prose it emits, not invents); (b) carry the chosen-route lock as prose (e.g. "Chosen route: C — hybrid"); (c) include `art-viz` in `stage_provenance` when the sidecar carries an art-viz block; (d) populate a seed's `anchor_ref` / `style_ref_ids` **only when actual refs exist**, else keep `null` / `[]`. No code — a prose edit to a model-invoked skill.
- [ ] **2.4 Edit `chain-map.md`.** ART-VIZ row → **inline in orchestrator — not a skill / status: live (Slice 3)**; "What it does" = "≥3 distinct Flow-ready route prompts + signature mechanic, inline prose in concept.md; chosen route → prose + seed `anchor_ref`/`style_ref_ids` (no `style_route` field)"; keep the "piece has a locked register already" skip; add the promotion-to-skill trigger (≥2 underperforming live runs); note the deferred SPEND OK render (§7.4) and the deferred style skill.
- [ ] **2.5 Edit `session-sidecar-contract.md`.** Add an `### art-viz` example under the PROPOSALS-LOG shape (four kinds only — `options` = the routes, `recommendation` = the lean, `open_questions` = the un-buildable-register flag) so the contract names the style-stage proposals like it names micro-expand/interrogate/expand/synthesize.
- [ ] **2.6 Commit.** `git commit -m "feat(frontdoor): inline ART-VIZ discipline; teach SYNTHESIZE + template to fold routes; defer style skill + spend gate"`

### Task 3 — The good-ART-VIZ rubric + live validation protocol
**Files:** Create `.claude/skills/brainstorm-front-door/references/good-art-viz-rubric.md`.

- [ ] **3.1 Write the rubric** — the six §7.2 criteria, each with a worked positive drawn from the piñata + ai-guru route sets (the three distinct registers; the candy-as-oil / Orby-glitch mechanic in every route; the captured timing bibles; the pencil-test-fusion Route C; the surfaced `90s-nicktoon-grossout` register) and a one-line anti-example (its negation). Header it plainly: **a live human-review checklist for Sean — not a CI/prose gate; a model cannot self-pass it.** Name criterion 2 (signature mechanic) as the blocking bar. Cross-link `good-expand-rubric.md` (divergence-side companion) and `pinata-worked-example.md` (convergence-side).
- [ ] **3.2 Write the live validation protocol** (the Checkpoint-3 hand-off): *pick a piece with a live style question (a fresh spark, or re-open the piñata/ai-guru route choice cold); run orchestrator → … → INTERROGATE → the inline ART-VIZ step; capture the `### art-viz` sidecar block + the chosen-route lock + `stage_provenance` carrying `art-viz`; score against the six criteria; a miss on criterion 2 (signature mechanic) blocks.* State plainly: Fable 5 builds to structural-green + this protocol; **Sean runs the live grill + renders on Flow.** Include the §7.4 deferred SPEND OK spec as an appendix so it is on record.
- [ ] **3.3 Commit.** `git commit -m "docs(frontdoor): good-ART-VIZ live-review rubric + validation protocol; SPEND OK deferred spec"`

### Task 4 — Verification gate (before any "done")
- [ ] **4.1** `superpowers:verification-before-completion`: run fresh and paste output —
  `python -m pytest tests/` (full suite green, no regressions);
  `python -m pytest tests/test_frontdoor_*.py -v` (Slice-3 characterizations green; Slice-1/2 tests still green);
  `md5 evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md pipeline/agents/prompts/sean-screenwriting-voice.md` (== the two guard hashes);
  `git status` (only the §8 paths; nothing under `pipeline/frontdoor/`; no `frontdoor-art-viz/`, no `genndy-tartakovsky/`, no `criteria.py`/neutrality-test change).
- [ ] **4.2** Confirm the orchestrator reads coherently: micro-expand → deepen?/EXPAND → INTERROGATE → **ART-VIZ (inline)** → SYNTHESIZE, all in the room; the rubric is reachable from Step 2.5; the "$0, no spend" and "defer the style skill" statements are explicit.

## 10. Checkpoints

**Checkpoint 3 (Sean review — STOP here; the Fable 5 kickoff stops at first green).** Two gates:
- **Structural (CI):**
  - **3a** — `python -m pytest tests/test_frontdoor_*.py` (both characterizations green; no frontdoor regression).
  - **3b** — `python -m pytest tests/` (full suite green) + md5 guards byte-unchanged + `git status` clean except the §8 paths (no `frontdoor-art-viz/`, no `genndy-tartakovsky/`, `pipeline/frontdoor/` byte-identical).
- **Semantic (§7.2, blocking — Sean's live pass):** the ART-VIZ inline discipline + chain-map flip + sidecar-contract wiring authored; the good-ART-VIZ rubric + protocol shipped. Sean runs a live ART-VIZ pass and scores it against the six criteria (criterion 2 = signature mechanic, blocking). **Fable 5 delivers everything up to and including the protocol, structurally green; the live capture is Sean's.**

## 11. Codex reconciliation notes

Codex's independent plan (task `task-mr4b7oix-utqe46`, session `019f25ca…`) **converged strongly** — it independently reached the same call on **eight of the nine questions**: ART-VIZ inline not a skill (Q1); defer `genndy-tartakovsky` as a Cy/generation-layer asset with no current consumer (Q2); Slice 3 spends nothing, no Higgsfield MCP / spend gate, same "the render gate depends on a Slice-4 stress verdict" reasoning (Q3); **no `pipeline/frontdoor` code, no `style_route` field** — "`Handoff.from_json` rejects unknown fields, and no named consumer reads `style_route`; a rendered route uses the already-permitted seed `anchor_ref`/`style_ref_ids`" (Q4, verbatim agreement); surface-not-solve the register, doctrine extension rides the first real Cy run (Q5); the honest eval split with the two route sets as **worked fixtures not CI oracles** (Q6); `stress_verdict` prose-only until a real gate reads it (Q8); always-on + default-to-Tiger + non-blocking reconcile cleanly, "non-blocking means no CI/pipeline block, not ignore Tigers" (Q9). The one place I held my own first instinct against Codex — no schema module, no field — is the load-bearing call, and Codex reached it independently, which strengthens it.

Two Codex contributions **folded**:

| Fold | Codex point | What changed |
|---|---|---|
| **F-C1 — same hero frame across routes.** | Codex's Q6 rubric addition: "require the same hero frame across routes" — both runs literally render *one* composition in three registers ("Same composition, rendered in…"). | **Folded into rubric criterion 1** (§7.2) and Step 2.5 (§9 Task 2.1): the routes hold the composition constant and vary only the register, so it is a true look-to-look comparison. A route that also changes the composition is now an anti-example. |
| **F-C2 — STRESS-TEST leans toward a distinct role.** | Codex takes a **stronger** position than my draft on Q7: STRESS-TEST *likely earns a distinct `frontdoor-stress-test` skill* because it critiques the room's **own** concept — "an adversarial role-seam, not code." | **§13.1 rewritten** to weigh three options (inline / distinct same-session skill / fresh-context sub-agent) as a genuine open fork. *(The subsequent red-team then demoted the same-session-skill option — it shares the authoring context, so it doesn't actually attack the bias; the real poles are inline vs fresh-context. See §12 F8.)* The pick is deferred to Slice 4's converge, which compares them head-to-head. |

Two Codex suggestions **recorded but not adopted as requirements** (both kept optional, pending the red-team):
- **A separate `art-viz-worked-examples.md` file** (Codex proposed one, plus a `concept-doc-template.md` edit). Kept the worked positives **inside `good-art-viz-rubric.md`** to match how Slice 2 kept them inside `good-expand-rubric.md` (one fewer file); the `concept-doc-template.md` touch is an **optional, verify-first** note in Task 2.1 (the build plan says the template already names the movements).
- **A `style_route`-specific unknown-field guard test** (Codex: "optional, only if absent"). I first argued it redundant ("Slice 1's generic test covers it") — **the red-team proved that claim false** (§12 F5): `test_frontdoor_handoff.py` on `main` has no generic unknown-field test. Resolution: Slice 3 adds a **generic** unknown-field rejection test (Task 1c), *not* Codex's `style_route`-specific magic-word version — the generic test pins "the schema is deliberately not widened" without prose-grep theater.

## 12. Red-team fold (verdict: UNDER-BUILT — accepted)

Codex red-teamed the converged doc (task `task-mr4bh2f4-e14uzt`, session `019f25d0…`) and returned **UNDER-BUILT** — the opposite of Slice 2's OVER-BUILT, and the honest read. It **confirmed** the load-bearing calls (no `frontdoor-art-viz` skill, no `genndy-tartakovsky` skill, no new `pipeline/frontdoor` code, no `style_route` field, prose `stress_verdict`) but found the inline contract **did not yet reach the existing SYNTHESIZE writer + concept template that actually emit the routes**, plus three overstated claims. **All four of its factual claims were verified against `main` before folding** (F1/F2/F5/F6 — the git-show checks are in the build session's record). Eight findings folded; the ninth is a confirmation.

| Fold | Finding | What changed |
|---|---|---|
| **F1 — reach the SYNTHESIZE writer (the UNDER-BUILT core).** | The plan edited the orchestrator/chain-map/sidecar/rubric but **not** `frontdoor-synthesize/SKILL.md` — the stage that actually writes `concept.md` + seeds, which on `main` hardcodes `anchor_ref: null` / `style_ref_ids: []`. Without teaching it, ART-VIZ's proposals would be dropped at emission. | **Added `frontdoor-synthesize/SKILL.md` to §8 + Task 2.3:** fold `### art-viz` proposals into `concept.md`; carry the chosen-route lock as prose; add `art-viz` to provenance when present; populate seed refs only when real refs exist. Prose, no code. **This is what makes the slice right-sized.** |
| **F2 — the template contradicts the plan (required edit).** | `concept-doc-template.md` says "Route letters become `style_route` ids" — directly against §2.4's no-`style_route` call. | The template edit is now **required** (§8, Task 2.2): route letters are prose/locked-decision handles, **no `style_route`**, rendered refs → seed `anchor_ref`/`style_ref_ids`. (Was an optional note; the contradiction makes it mandatory.) |
| **F3 — don't oversell the piñata worked positive.** | I claimed "every route carries the signature mechanic" for **both** runs. False for piñata: its routes render the *landing pose* (piñata intact behind him); candy-as-oil lives in the money-shot prose, not the routes. Only ai-guru renders its mechanic in-frame. | **Rubric criterion 2 rewritten (§7.2), §1 + §2.6 softened:** the mechanic is *rendered in-frame* (ai-guru) **or** *captured in the money-shot/timing-bible prose and never dropped* (piñata). The block is "mechanic not dropped," not "painted in every route." |
| **F4 — the blocking rule was gameable.** | Blocking on criterion 2 alone lets three clustered, non-renderable, mechanic-name-dropping prompts pass — yet the slice's own goal demands ≥3 distinct, Flow-ready routes. | **Criteria 1, 2, and 3 now block together** (§7.2): fixed frame + distinct registers, mechanic-not-dropped, self-contained Flow-ready prompt. Still Sean's live judgment, not CI. |
| **F5 — the no-`style_route` argument had no test behind it.** | I claimed a generic unknown-field test already covers Codex's `style_route` guard. **It doesn't** — `test_frontdoor_handoff.py` on `main` tests unknown *mode value*, not unknown *field*. | **Added a generic unknown-field rejection test (Task 1c)** — not a `style_route`-specific magic-word assert. §11 corrected. |
| **F6 — don't overstate the seed-field contract.** | §2.4/§7.1 called `anchor_ref`/`style_ref_ids` "the real Cy consumer." Verified: no pipeline code reads `style_ref_ids` — it is passthrough, not an active consumer. | **Relabeled "seed passthrough / future Cy landing spot"** (§2.4, §7.1, Task 1b). The no-`style_route` conclusion is unchanged — nothing reads `style_route` either, and the seed fields are the schema-sanctioned future home. (The Slice-2 F7 honesty discipline, applied again.) |
| **F7 — ART-VIZ needs a no-library operating rule.** | Deferring the style skill is right, but Step 2.5 didn't say *how* ART-VIZ writes good routes without one. | **Added the no-library rule to Step 2.5 (Task 2.1):** draw route language from the locked references + timing bible + seed `source_notes`; if reference knowledge is missing, raise an `open_question` — don't invent a reusable style doctrine. |
| **F8 — the same-session STRESS-TEST skill was oversold.** | A same-session `frontdoor-stress-test` role shares the authoring context, so it doesn't actually fix self-critique bias; only fresh-context review does. | **§13.1 revised:** demoted option (b) to the seductive-but-weak middle; the real poles are (a) inline-honest-about-its-limits and (c) fresh-context-independent; Slice 4 compares (a) vs (c) head-to-head before committing. |
| **F9 — confirmed, no change.** | No museum/handoff consumer for `stress_verdict` exists; the only named reader is the deferred spend gate. Prose-until-consumer is right. | §13.2 stands as written — validated by the red-team's own `rg`. |

**Net:** the slice moved from UNDER-BUILT to right-sized by **adding two required prose edits** (SYNTHESIZE + the template) and **one generic test** — closing the loop to the writer that emits the routes — while every over-build boundary held: **no new skill, no genndy skill, no `pipeline/frontdoor` code, no `style_route` field, $0 spend.** Two Slice-2-style honesty corrections (F3 oversell, F6 overstated contract) landed for the same reason they did in Slice 2.

## 13. Slice 4 — STRESS-TEST (full plan, PROVISIONAL — do not build; kickoff waits for Slice 3 green)

**Provisional** because Slice 4 stacks on Slice 3 and may be reshaped by Slice 3's live run (e.g. if the inline ART-VIZ pass reveals the room can't red-team its own concept cleanly, Slice 4's skill-vs-inline call flips). Its Fable 5 kickoff is withheld until Slice 3 is green.

### 13.1 SKILL vs INLINE (Q7) — a genuine open fork, deferred to Slice 4's converge
Unlike EXPAND and ART-VIZ, STRESS-TEST red-teams the room's **own** concept — a real self-critique bias (Fable 5's own note: *fresh-context verifier subagents outperform self-critique*). That single difference means the inline-by-default reflex is **weaker here than anywhere else in the chain**, and Codex (§11, F-C2) independently pushed past it. Three live options, none yet chosen:

- **(a) Inline discipline** (like EXPAND/ART-VIZ) — cheapest, in-the-room, but the same context that fell in love with the concept now grades it. Weakest against the bias.
- **(b) A distinct `frontdoor-stress-test` skill** (Codex's lean) — a same-session model call framed as an **adversarial role**. **The red-team (§12 F8) demoted this to the seductive-but-weak middle:** a same-session role *reframes* the critique but **shares the authoring context, so it does not actually attack the self-critique bias** — the same context that fell for the concept is still grading it, now wearing a critic hat. It looks like a seam without being one.
- **(c) A fresh-context red-team sub-agent** — a genuinely independent reviewer of the emitted concept (the pattern the T3 council + Fable 5's verifier note endorse). **The only option that actually attacks the bias**; heaviest machinery.

**So the real poles are (a) and (c),** not (b): (a) is inline, cheapest, and *honest that it is same-context* (it does not pretend to be independent); (c) actually buys independence at the cost of a sub-agent. **The evidence to pick is not in yet** — both dry-runs' "Open threads" are *proto*-stress-tests (unresolved-question lists), not a real steelman→"Fails if"→cheapest-test pass, so there is **no live STRESS-TEST run** to arbitrate the way the four ART-VIZ runs arbitrated Q1. **The call is deferred to Slice 4's own converge**, which will **compare (a) inline vs (c) fresh-context head-to-head on one strong and one weak concept** before committing (red-team F8: "do not default to a role-skill just because it sounds like a seam"). Whichever wins returns only the four proposal kinds; the orchestrator locks the verdict. *(This is the one place Slice 4 may add machinery where Slice 3 refused it — and it would be evidence-driven, not sketch-driven.)*

### 13.2 The `stress_verdict` enum (Q8) — prose until the spend gate that reads it is co-built
`stress_verdict: proceed|revise` has **no machine consumer if spend is deferred** (§2.3): the only design that reads it is the SPEND OK render gate, which is not built. **So in Slice 4 the verdict is prose in `concept.md` + a sidecar LOCKED DECISION** — not a `handoff.py` field. It becomes a real enum field **only co-built with the spend gate that consumes it** (a later slice) — the field and its consumer grow together, same discipline as §2.4. This means Slice 4, like Slice 3, keeps `pipeline/frontdoor/` byte-identical (the "first real schema growth since Slice 1" the parent predicted is deferred to the spend-gate slice, not Slice 4).

### 13.3 Always-on / non-blocking ⋈ default-to-Tiger (Q9)
No conflict — the three describe different axes:
- **Always-on:** STRESS-TEST always runs (once built) — every concept gets the pre-mortem + red-team; it is not routed around.
- **Default-to-Tiger:** the *classification bias within* the stage — when unsure whether a risk is real, call it a Tiger (a real problem to surface prominently), so the stage does not under-flag. This is about honesty of flagging, not about halting.
- **Non-blocking:** the stage does not unilaterally halt the pipeline; it surfaces its Tigers and a recommended `proceed|revise`, and **Sean decides.** The verdict informs the human, it is not an automatic gate.
Together: run every time, flag aggressively (default-to-Tiger keeps it from being toothless), decide humanly (non-blocking keeps the human the one decider). The piñata's own "Open threads" (the tough-grandma-stereotype risk, runtime flex, the title pick) are the shape of a `proceed`-with-named-residuals output — not a clean pass, not a block.

### 13.4 Slice-4 shape (provisional)
- **The STRESS-TEST discipline** (placement: between ART-VIZ and SYNTHESIZE — nominal Step 3.5), realized as **whichever of §13.1's (a)/(b)/(c) the Slice-4 converge picks**: pre-mortem Tiger/Paper-Tiger/Elephant (default-to-Tiger) + red-team steelman→"Fails if ___"→rank-by-(impact × likelihood × cheapness-to-test); "don't manufacture doubt" rule; proposes findings + a recommended verdict (four proposal kinds only); Sean decides; orchestrator locks the verdict as prose + records `stress-test` in `stage_provenance`.
- **`good-stress-test-rubric.md`** (live checklist): a real fork found (≥1 launch-blocking Tiger on a weak concept), each risk a "Fails if ___" with a cheapest test, no manufactured doubt (a sound concept is said sound plainly), the fragile intuition not attacked as a "risk," a `proceed`-with-named-residuals on a strong concept (the piñata should NOT clean-pass — it flags the tough-grandma-stereotype residual).
- **Structural (CI):** a `stress-test` provenance characterization (no module); **no `stress_verdict` field, no `stress.py`** (byte-identical seam). Optionally a ships-red weak-concept reference for the rubric's worked negative.
- **No spend, no new `pipeline/frontdoor` code** — same posture as Slice 3, *unless* §13.1 lands on option (c), whose sub-agent wiring is the one place Slice 4 could grow beyond prose. Even then, `pipeline/frontdoor/` stays byte-identical (a sub-agent is orchestrator/skill machinery, not the artifact seam).

## 14. Anti-drift note
Slice 3 opens no new workstream — ① is the active build (ROADMAP lock) and this is its next slice. It touches only `.claude/skills/brainstorm-front-door/*` + `tests/`; `pipeline/frontdoor/` is byte-unchanged; no new skill; no `criteria.py`/neutrality-test change; the two md5 guards are untouched; $0 spend. The whole-front-door plan already scoped ART-VIZ as Slice 3; this refines its *implementation* (inline discipline, style skill + spend deferred) against four runs of evidence — it does not expand scope. It shrinks it.
