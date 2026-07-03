# Front Door (①) — Slice 2: EXPAND (the divergence discipline) — Converged Build Plan (Opus + Codex)

> **For agentic workers:** REQUIRED SUB-SKILL — use `superpowers:test-driven-development` per code task (red → verify-red → green → verify-green → refactor) and `superpowers:verification-before-completion` before any "done". Steps use checkbox (`- [ ]`) syntax.

**Date:** 2026-07-02
**Status:** Planning — the executable spec for Slice 2 of ①. **Plan only; no implementation code this session.**
**Builds on:** [2026-07-02-frontdoor-build-plan-CONVERGED.md](2026-07-02-frontdoor-build-plan-CONVERGED.md) — refines its §7 divergence sketch and §8 Slice-2 stub against live evidence.
**Primary evidence:** the live Slice-1 run — [`frontdoor-session.md`](../../.claude/worktrees/frontdoor-slice1/frontdoor-session.md) + [`briefs/2026-07-02-ai-guru-pilot/`](../../.claude/worktrees/frontdoor-slice1/briefs/2026-07-02-ai-guru-pilot/).
**Co-planned with:** Codex (independent plan §11 + adversarial red-team §12). **The red-team reversed the draft's central call** — see §2 and §12.

---

## 1. The one-sentence goal

Formalize the front door's **divergence discipline** (the "EXPAND" stage in Sean's locked chain) as a **deeper, on-demand, per-axis mode of the orchestrator's *existing inline* micro-expand** — a specified contested-axis workshop (N≈3–5 sharp distinct options + a synthesized recommendation) that replaces the current "deepen = offer a longer inline fan-out (stopgap)" hand-wave — **without adding a separate skill and without any new `pipeline/frontdoor` code**.

## 2. The position (revised by the red-team): EXPAND is an inline deeper mode, not a distinct skill

Two claims, in order of how hard the evidence pushed on them.

### 2.1 EXPAND is targeted per-axis divergence, not a monolithic fan-out — and the `≥8/≥4` metric is dead

The §7 sketch proposed a "≥8 avenues across ≥4 domains" fan-out on "deepen." **The live ai-guru run falsifies that shape.** When Sean flagged two contested axes — the ending ([L5]) and the stakes/clock ([L6]) — the room generated **~4 sharp options per axis** (ending: cyclical-nihilistic / escalation-treadmill / permanent-mutation / bait-and-switch-irony; stakes: subscriber-deadline / rival / personified-algorithm / grounded-real-world) then **a combined, synthesized recommendation** (ending = 1+4+2 fused; stakes = 1+3 fused). That was **enough** — the brief passed the anti-pattern rubric 6/6. **Kill the `≥8/≥4` metric**: it is a gameable volume play (a model hits "8 avenues" with 8 semantic neighbours and clusters them). Replace it with the six-criterion **good-EXPAND rubric** (§7.2) used as a **live human-review checklist only** — not a CI or prose check (a rubric can't be machine-validated for creative quality; §12-F3).

### 2.2 EXPAND stays INLINE in the orchestrator — it is the micro-expand's deeper mode, not a separate model-invoked skill

**The draft proposed a distinct `frontdoor-expand` skill. The red-team + the live evidence reversed that call.** The decisive facts:

- **The live run did the entire EXPAND job with no EXPAND skill.** The deepening is recorded in the sidecar as `### micro-expand (workshop continuation — risks 2 & 3)` — it generated options, synthesized a fused recommendation, protected the admiration/mockery intuition, and handed the orchestrator decisions to lock. That is the full claimed capability, done inline. Zero evidence a separate skill is needed; one data point that inline works.
- **Divergence already lives inline.** The orchestrator *already owns* the micro-expand (Slice 1, no skill call). EXPAND is the same family (breadth-once → depth-on-axis). Making the deeper mode a separate skill breaks the precedent that divergence is an orchestrator-inline discipline; keeping it inline is *more* consistent, not less.
- **The composability pattern argues *against* a skill here.** `frontdoor-interrogate` and `frontdoor-synthesize` are skills because they are **phase-boundary disciplines** (a whole interview; a whole write-up). Divergence is **not a phase** — it is a move used *within* INTERROGATE and *before* it, which is exactly why the micro-expand is already inline. A separate skill invoked mid-grill *steps out of the room* — the very thing the live run's success depended on staying inside (§12-F8).

**So the answer to the plan's central question — "is EXPAND a distinct skill, or a deeper mode of the micro-expand the orchestrator already runs?" — is: a deeper mode, inline.** Slice 2 formalizes that mode; it does not build a skill. **Promotion trigger (YAGNI-honest):** promote to a standalone skill only if ≥2 live runs show inline deepening demonstrably underperforming (routing confusion, dropped discipline). We have zero such runs.

## 3. Architecture — an inline discipline over the untouched Slice-1 seam

**No separate skill. No new `pipeline/frontdoor` code.** Slice 2 is: (A) prose that specifies the inline contested-axis workshop in the orchestrator + kills the dead metric in the chain-map + adds a live-review rubric reference; and (B) a small amount of *test + fixture* work that hardens the existing seam against a second real brief and pins the no-code contract. The Slice-1 seam already carries everything divergence produces:

- Options/recommendation/open_questions live in the sidecar **PROPOSALS LOG** — the four-kinds contract already holds them; the live run's workshop block *is* valid PROPOSALS-LOG content today.
- Provenance is a string in `Handoff.stage_provenance`, a free `list[str]` (`handoff.py:36-37` validates non-empty-list, **not** an enum). `stage_provenance: [..., "expand:ending", ...]` validates and round-trips with **zero code change**.

**This "no-code" claim is verified against the built Slice-1 code, not asserted** (2026-07-02, run against the worktree): `Handoff(stage_provenance=["micro-expand","expand:ending","interrogate","expand:stakes","synthesize"])` round-trips through `to_json`/`from_json` unchanged; unknown *fields* are still rejected (`unknown frontdoor.json fields: ['…']` — the seam stays closed, provenance strings are values not fields); and `validate_brief_dir` returns `[]` on the real ai-guru bundle today. A new `expand.py` schema module would be the schema theater red-team **A6** cut in Slice 1. We refuse it.

## 4. The micro-expand ↔ EXPAND relationship (one mechanism, two depths)

They are the **same inline mechanism** at two depths — not two implementations:

| | **micro-expand (reflex depth)** | **EXPAND (workshop depth)** |
|---|---|---|
| Scope | breadth-once on the **whole spark** | depth on **one contested axis** |
| Shape | fixed 3 premises / 3 routes / 3 risks | N≈3–5 options + a synthesized recommendation |
| Trigger | always, before INTERROGATE | on "deepen", or any contested axis (incl. mid-grill) |
| Where | **inline in the orchestrator** | **inline in the orchestrator / INTERROGATE** — same room |
| Discipline | a terse reflex | anti-clustering + JTBD/structural qualifying + named-specifics-with-tradeoffs + converge + protect-the-intuition |

Both are inline. EXPAND is the micro-expand *turned up* on a contested axis — the discipline the current orchestrator's "deepen = offer a longer inline fan-out honestly labeled as the stopgap" line gestures at but never specifies. Slice 2's job is to **specify it** so the quality the live run reached by improvisation becomes encoded discipline any operator (or Fable 5, or a future session) follows.

## 5. Flow placement: nominally first, invoked inline throughout (no reorder, no context switch)

Sean **locked** the nominal order (`EXPAND → INTERROGATE → ART-VIZ → STRESS-TEST → SYNTHESIZE`). The live run **interleaved** divergence with INTERROGATE. These reconcile without a reorder *and* without a skill invocation:

- EXPAND **retains its first-position** nominally — the always-on **micro-expand is its opening beat**, before INTERROGATE.
- EXPAND (workshop depth) is **reached inline** at two trigger points: (1) the micro-expand "deepen?" gate; (2) any contested axis surfaced mid-grill. In both cases the orchestrator/INTERROGATE **deepens in place** — it does not raise-open_question-return-invoke-a-separate-skill-return (heavier machinery than what worked). Locks are still orchestrator-only, append-only (§6). This is not a reorder — divergence is a reflex the room uses when it hits a fork, and the room never leaves.

## 6. The §6 propose-vs-decide boundary — enforced by prose + the sidecar convention (not a lint)

The boundary is unchanged: the divergence discipline **proposes** (options/recommendation/open_questions in the PROPOSALS LOG) and **never locks** — only the orchestrator writes LOCKED DECISIONS, append-only, after Sean decides. The live sidecar already demonstrates this working for the workshop-continuation (options → PROPOSALS; [L5]/[L6] → orchestrator locks).

**How it is enforced/tested:** exactly as Slice 1 enforced INTERROGATE's identical boundary — **by prose discipline in the orchestrator + the append-only sidecar convention, verified by the live run and human review. It is not unit-tested.** The draft proposed a markdown "boundary lint"; **the red-team correctly cut it** (§12-F4): a first-word bullet check gives *false confidence* — a decision smuggled inside a `recommendation:` bullet's text passes it. An interactive discipline's boundary is not a unit-test surface; asserting it with a shallow parser is test theater. The honest split (the one Slice 1 used): the **seam** is unit-tested; the **discipline** is a live rubric + human review.

## 7. Eval strategy — Slice 1's honest split, trimmed by the red-team

**The seam is unit-tested (CI-green, credential-free); the divergence *quality* is a live rubric eval (blocking human checkpoint).** No model transport in any test.

### 7.1 Structural (CI, no keys) — what survives the red-team
- **Golden fixture #2 = the ai-guru bundle** rides into the existing structural suite (Task 1). `validate_brief_dir` returns `[]`; the round-trip/emit tests run over **both** `pinata` and `ai-guru`. **Sold as what it is: a second golden front-door brief validates** — a different register (90s-nicktoon vs Tartakovsky), structure (one sequence vs three acts), cast size (2 vs 3). **NOT sold as "proof of EXPAND"** — the emitted bundle's provenance is `micro-expand/interrogate/synthesize` (it predates any expand tagging); §12-F6.
- **Expand-provenance characterization** (Task 2): a *tiny synthetic* test that axis-tagged `expand:ending` provenance round-trips through the seam — the machine proof no module is needed. Labeled a characterization, not proof of a real run.
- **Cut by the red-team:** the skill-contract prose-grep tests (no skill to test; grepping magic words is theater) and the boundary lint (false confidence). §12-F4.

### 7.2 Semantic (live, blocking — the real quality gate)
A **captured live EXPAND run on a contested axis**, scored against the **good-EXPAND rubric** — *not* a copied fixture. Sean runs the live grill (the human is his); Slice 2 ships the **rubric + validation protocol**. The rubric — **used only as a live human-review checklist, never a CI/prose check** (§12-F3) — a good EXPAND on a contested axis exhibits all of:

1. **Real fork** — a genuinely contested axis (a live tension the room hasn't resolved), not manufactured to look busy.
2. **Mutually distinct options** — they occupy different regions of the space (the anti-clustering discipline), not four phrasings of one idea. *Judged by Sean, live — no CI oracle.*
3. **Each option a named specific with its tradeoff** — "his biggest hit is an accidental humiliating clip he never meant to film + he's mortified it worked," not "a surprising ending."
4. **Converges** — a synthesized recommendation (combining options is fair), stated so Sean accepts/vetoes in a line.
5. **Protects the fragile intuition** — the duality/tension that makes the spark special survives, not collapsed into a clean moral. **The anima-specific bar** — the whole lesson of the dry-run.
6. **Surfaces buildability risks as `open_questions`** — e.g. a register anima can't yet build (finding #3), flagged not waved through.

The rubric is a *taste instrument for Sean*, not a gate a model self-passes. That honesty is the point (§12-F3).

### 7.3 Fixture-#2 decision: adopt the ai-guru run
**Adopt** — the ai-guru bundle is the second golden brief (register/structure/cast diversity) and its committed **sidecar** is the reference transcript the rubric's worked example draws from. The bundle already exists in the worktree; Task 1 commits it (flipping `frontdoor.json.mode` → `"fixture"` per the chain-map masquerade rule).

## 8. File layout (Slice 2 — prose + one fixture + minimal tests; no skill, no `pipeline/frontdoor`)

```
.claude/skills/brainstorm-front-door/
  SKILL.md                              # EDIT — Step 1: replace "deepen = stopgap fan-out" with the
                                        #        specified inline contested-axis workshop; add mid-grill deepening
  references/
    chain-map.md                        # EDIT — EXPAND row: inline per-axis divergence; KILL "≥8 avenues/≥4 domains"
    session-sidecar-contract.md         # EDIT — name the deepened-axis proposals shape (expand:<axis>)
    good-expand-rubric.md               # NEW  — the six-criterion live-review rubric + validation protocol

tests/
  test_frontdoor_validate.py            # EDIT — parametrize golden-bundle validation over {pinata, ai-guru}
  test_frontdoor_emit.py                # EDIT — parametrize round-trip/gap-report over {pinata, ai-guru}
  test_frontdoor_handoff.py             # EDIT — add the tiny axis-tagged expand-provenance characterization
  fixtures/frontdoor/
    ai-guru/                            # NEW  — the committed golden bundle #2 (mode: "fixture")
      00_studio_brief.md  concept.md  character_seeds.yaml  frontdoor.json  manifest_gap_report.md
    manifest_ai_guru.yaml               # NEW  — registers aiden/orby for the Maya-gate parametrization
```

**No `frontdoor-expand/` skill. No `test_frontdoor_expand_skill.py`, no `test_frontdoor_expand_boundary.py`, no `expand-boundary/` fixtures** (all cut by the red-team). Nothing under `pipeline/frontdoor/` changes. `git status` at Checkpoint 2 shows only the paths above.

## 9. Per-slice TDD task list

Discipline every code task: `superpowers:test-driven-development`; tests run **per-directory from repo root** (`python -m pytest tests/`); commit at each task end; `superpowers:verification-before-completion` before "done"; **both md5 guards byte-unchanged** — Slice 2 touches neither:
`evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4`;
`pipeline/agents/prompts/sean-screenwriting-voice.md` = `945af824fa53b948a18ac6bf206d67ef`.

### Pre-flight (worktree)
- [ ] **P0.** Slice 1 is committed on `worktree-frontdoor-slice1` (`e33c1cb`) but **not yet merged to main** (`git ls-tree main pipeline/ | grep frontdoor` → empty). **Recommended:** open + merge Slice 1's PR to main, then create the Slice-2 worktree from `main`. **If not merging yet:** branch the Slice-2 worktree from `worktree-frontdoor-slice1` (`e33c1cb`). Use `superpowers:using-git-worktrees` (detect native isolation first; verify the dir is gitignored). Confirm `python -m pytest tests/` green before writing anything.

### Task 1 — Golden fixture #2 (the ai-guru bundle) + parametrized structural suite
**Files:** Create `tests/fixtures/frontdoor/ai-guru/{00_studio_brief.md,concept.md,character_seeds.yaml,frontdoor.json,manifest_gap_report.md}`, `tests/fixtures/frontdoor/manifest_ai_guru.yaml`; Modify `tests/test_frontdoor_validate.py`, `tests/test_frontdoor_emit.py`.
**Interfaces consumed:** `validate_brief_dir(dir) -> list[str]`; `Handoff.from_json`; `emit_brief_dir(out, *, studio_brief_md, concept_md, seeds, handoff, manifest=None)`; `BUNDLE_FILES`.

- [ ] **1.1 Copy the bundle in, flip `mode`.** Copy the five files from `.claude/worktrees/frontdoor-slice1/briefs/2026-07-02-ai-guru-pilot/` into `tests/fixtures/frontdoor/ai-guru/`; edit `frontdoor.json` `"mode": "interactive"` → `"mode": "fixture"`. Author `manifest_ai_guru.yaml` registering `aiden`/`orby` (mirror `manifest_pinata.yaml`).
- [ ] **1.2 Write the failing parametrized validate test** in `tests/test_frontdoor_validate.py`:
```python
import pytest
from pathlib import Path
from pipeline.frontdoor.validate import validate_brief_dir

FIXTURES = Path(__file__).parent / "fixtures" / "frontdoor"

@pytest.mark.parametrize("bundle", ["pinata", "ai-guru"])
def test_validate_passes_on_golden_bundle(bundle):
    assert validate_brief_dir(FIXTURES / bundle) == []
```
- [ ] **1.3 Verify red** (point at `ai-guru` before 1.1's files exist): the `ai-guru` case FAILs with a missing-dir/section problem, for the right reason.
- [ ] **1.4 Land the fixture; verify green.** `python -m pytest tests/test_frontdoor_validate.py -v` → both cases PASS. Section problems ⇒ fix the fixture, not the validator. *(Verified feasible: `validate_brief_dir(ai-guru)` returns `[]` today.)*
- [ ] **1.5 Parametrize emit round-trip + gap report** in `test_frontdoor_emit.py` over `{pinata, ai-guru}`: emit from the fixture inputs (seeds + a `Handoff` from its `frontdoor.json`) into a tmp dir; assert all `BUNDLE_FILES` present + `validate_brief_dir(tmp) == []`; gap report vs `manifest_ai_guru.yaml` lists **zero** unregistered, vs empty manifest lists **both**. Red → green.
- [ ] **1.6 Commit.** `git commit -m "test(frontdoor): golden fixture #2 (ai-guru) — a second brief validates through the seam"`

### Task 2 — Axis-tagged expand-provenance characterization (the no-module proof)
**Files:** Modify `tests/test_frontdoor_handoff.py`.

- [ ] **2.1 Write the test** (a *characterization*, honestly labeled — not proof of a real EXPAND run):
```python
from pipeline.frontdoor.handoff import Handoff

def test_stage_provenance_carries_axis_tagged_expand_with_no_schema_change():
    """Characterization: the seam already carries expand:<axis> provenance — no module needed.
    This is synthetic (a real ai-guru run predates expand tagging); it proves the CONTRACT, not a run."""
    h = Handoff(slug="ai-guru-pilot", characters=["aiden", "orby"],
                stage_provenance=["micro-expand", "expand:ending", "interrogate", "expand:stakes", "synthesize"],
                mode="interactive")
    assert Handoff.from_json(h.to_json()) == h
```
- [ ] **2.2 Verify** (passes on first run — that greenness is the finding; §3's verification confirms it) then **commit.** `git commit -m "test(frontdoor): pin axis-tagged expand provenance round-trips with no schema change"`

### Task 3 — Specify the inline contested-axis workshop (prose — the real deliverable)
**Files:** Modify `.claude/skills/brainstorm-front-door/SKILL.md`, `.../references/chain-map.md`, `.../references/session-sidecar-contract.md`. Prose — verified by the Checkpoint-2 live rubric eval, not a unit test (Slice-1 precedent).

- [ ] **3.1 Edit the orchestrator `SKILL.md` Step 1.** Replace the "deepen into a full fan-out … offer a longer inline fan-out honestly labeled as the stopgap" line with the **specified inline contested-axis workshop**: *on "deepen" (or when a mid-grill axis is contested), run — in place, without leaving the room — a per-axis workshop: N≈3–5 options that are mutually distinct (rotate the lens — emotional core / structural mechanic / tonal register / failure-mode / cross-domain analogy — the model clusters semantically by default), each a named specific with its tradeoff, qualified with JTBD (functional/emotional/social) + "structural not narrative", converging to one stated recommendation (combining options is fair); protect the spark's fragile intuition (name it; check no option flattens it); surface any buildability risk as an `open_question`. Append only the four proposal kinds; Sean picks; you lock.* Add the mid-grill trigger to the chain diagram. Explicitly: **not** a volume fan-out; the `≥8/≥4` count is dead.
- [ ] **3.2 Edit `chain-map.md`.** EXPAND row → the inline divergence discipline (reflex depth = micro-expand; workshop depth = contested-axis); "What it does" = "per-axis divergence: N≈3–5 distinct options + a synthesized recommendation, inline"; both triggers; converges + never leaves the orchestrator; provenance convention `expand:<axis-slug>`. **Remove every `≥8 avenues`/`≥4 domains`/"full fan-out" phrase.** Keep "do not reorder" — nominally first (the micro-expand is its opening beat), invoked inline throughout. Note the promotion-to-skill trigger (≥2 underperforming live runs).
- [ ] **3.3 Edit `session-sidecar-contract.md`.** Add an `### expand:<axis>` example under the PROPOSALS-LOG shape (four kinds only) so the contract names the deepened-axis proposals like it names micro-expand/interrogate/synthesize.
- [ ] **3.4 Commit.** `git commit -m "feat(frontdoor): specify the inline contested-axis workshop; kill the ≥8-avenue metric"`

### Task 4 — The good-EXPAND rubric + live validation protocol
**Files:** Create `.claude/skills/brainstorm-front-door/references/good-expand-rubric.md`.

- [ ] **4.1 Write the rubric** — the six §7.2 criteria, each with the ai-guru run as the worked positive (the four distinct endings; the fused 1+4+2 recommendation; the protected admiration/mockery duality) and a one-line anti-example (a flat EXPAND: four semantic-neighbour options, a list with no lean, the duality collapsed into a moral). Header it plainly: **a live human-review checklist for Sean — not a CI/prose gate; a model cannot self-pass it.** Cross-link `pinata-worked-example.md` — this is its divergence-side companion.
- [ ] **4.2 Write the live validation protocol** (the Checkpoint-2 hand-off): *pick a contested axis (a fresh thin spark, or re-open the ai-guru "ending" cold); run orchestrator → micro-expand → "deepen" → the inline workshop; capture the sidecar; score against the six criteria; a miss on criterion 2 (distinctness) or 5 (intuition-protection) blocks.* State plainly: Fable 5 builds to structural-green + this protocol; **Sean runs the live grill.**
- [ ] **4.3 Commit.** `git commit -m "docs(frontdoor): good-EXPAND live-review rubric + validation protocol"`

### Task 5 — Verification gate (before any "done")
- [ ] **5.1** `superpowers:verification-before-completion`: run fresh and paste output —
  `python -m pytest tests/` (full suite green, no regressions);
  `python -m pytest tests/test_frontdoor_validate.py tests/test_frontdoor_emit.py tests/test_frontdoor_handoff.py -v` (Slice-2 tests green, both bundles parametrized);
  `md5 evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md pipeline/agents/prompts/sean-screenwriting-voice.md` (== the two guard hashes);
  `git status` (only the §8 paths; nothing under `pipeline/frontdoor/`; no `frontdoor-expand/`).
- [ ] **5.2** Confirm the orchestrator reads coherently: the micro-expand → "deepen" → inline workshop → lock path, and the mid-grill contested-axis deepening, both stay in the room; the rubric is reachable from Step 1.

## 10. Checkpoints

**Checkpoint 2 (Sean review — STOP here; the Fable 5 kickoff stops at first green).** Two gates:
- **Structural (CI):**
  - **2a** — `python -m pytest tests/test_frontdoor_*.py` (golden fixture #2 round-trips + validates; provenance characterization green; no frontdoor regression).
  - **2b** — `python -m pytest tests/` (full suite green) + md5 guards byte-unchanged + `git status` clean except the §8 paths (no `frontdoor-expand/`).
- **Semantic (§7.2, blocking — Sean's live pass):** the orchestrator's inline-workshop discipline + chain-map metric-kill + sidecar-contract wiring authored; the good-EXPAND rubric + protocol shipped. Sean runs a live EXPAND on a contested axis and scores it against the six criteria. **Fable 5 delivers everything up to and including the protocol, structurally green; the live capture is Sean's.**

## 11. Codex reconciliation notes

Codex's independent plan (task `task-mr45yu0c-ed0bln`) **converged strongly** — it independently chose the same per-axis-not-fan-out shape, killed the same `≥8/≥4` metric, chose the same `expand:ending` provenance convention, the same "no `pipeline/frontdoor` code — no consumer for a schema module", the same adopt-ai-guru-as-fixture-#2, the same surface-not-solve for the new register, and the same nominal-order-stays / reachable-as-scoped-re-entry reconciliation. It differed by adding a distinct `frontdoor-expand` skill + skill-contract tests (D1) + a good/bad boundary-lint pair (D2) + fixture characterizations (D4). **The subsequent red-team overrode D1 and D2** — the skill and its contract/boundary tests are cut (see §12). Codex's D4 (fixture demonstrates EXPAND) was also cut as string-match theater; its D5 (name EXPAND in the sidecar contract) survives as Task 3.3. The one place Codex and I agreed against my own first instinct — no schema module — is the load-bearing call and it held through the red-team.

## 12. Red-team fold (verdict: OVER-BUILT — accepted)

Codex red-teamed the converged doc (task `task-mr46uu8l-64t8y7`) and returned **OVER-BUILT** with a coherent thesis: divergence is judgment the orchestrator exercises inline (the live run proved it), not a module. Six of eight findings materially improved the plan and are folded; the sections above already reflect them.

| Fold | Finding | What changed |
|---|---|---|
| **F1/F2/F8 — cut the separate skill.** | EXPAND doesn't earn a distinct skill; the live run did the job inline (labeled `micro-expand (workshop continuation)`); a separate model-invoked skill adds routing ambiguity + context-switch cost (steps out of the room) without adding capability. | **Reversed the draft's central call.** `frontdoor-expand/` is cut. The divergence discipline is specified **inline in the orchestrator** (§2.2, §4, Task 3). Promotion-to-skill trigger: ≥2 underperforming live runs. |
| **F4 — cut the test theater.** | Skill-contract tests grep magic words; the boundary lint gives false confidence (a decision smuggled inside a `recommendation:` bullet passes the first-word check). | Cut `test_frontdoor_expand_skill.py` and `test_frontdoor_expand_boundary.py` + the `expand-boundary/` fixtures. The §6 boundary is prose + sidecar convention + human review (§6), as in Slice 1. |
| **F3 — the rubric is a live checklist only.** | Every criterion is subjective/gameable by a model; the rubric is a human-review instrument, not a validator. | Rubric reframed as **Sean's live-review checklist**, explicitly **not** a CI/prose gate (§7.2, Task 4.1). |
| **F6 — don't oversell fixture #2.** | The emitted ai-guru bundle's provenance is `micro-expand/interrogate/synthesize` — no `expand:*`; it validates the output seam, not a real EXPAND stage. | Fixture #2 is sold as "a second golden brief validates" (§7.1). The provenance test is a labeled synthetic characterization (Task 2). |
| **F5 — ship the minimal slice.** | The minimal Slice 2 (adopt fixture #2 + kill the metric + one orchestrator paragraph + the rubric) is ~90% of the value at ~20% of the surface. | Adopted wholesale — this is the plan now (§8/§9): no skill, no boundary parser, no contract tests. |
| **F7 — verify the no-code claim, don't overstate the contract.** | `stage_provenance` runtime-validates "non-empty list", not `list[str]`/enum; the validator never inspects provenance values. | §3 now states the *actual* runtime contract and records the **code-verified** round-trip (not "the validator enforces `list[str]`"). |

**Not adopted:** the red-team's implicit "do nothing structural" undertone — Task 1's fixture-#2 parametrization survives because it is real structural coverage (a second brief through the seam), which the red-team itself endorsed keeping. Net: the slice is now **right-sized** — the smallest change that formalizes the divergence discipline the live run proved, kills the dead metric, and adds a second golden brief.

## 13. Slice 3 / Slice 4 — next-up placeholders only (do not build)

- **Slice 3 — ART-VIZ + `genndy-tartakovsky` style skill.** Flow $0 default, prompt-only; live Higgsfield MCP behind the `SPEND OK: …` gate (Slice-1 A3). **Carries finding #3:** the divergence discipline surfaces concepts in registers anima can't yet build (the ai-guru run's `90s-nicktoon-grossout`, live in both character seeds). The *handling* is Slice 3's — the prompt-style-neutrality doctrine's **3-step register extension** (extend `pipeline/criteria.py`'s closed vocabulary → add a `## What good looks like — {register}` block to `cy-character-designer-context.md` → update `_STYLE_REGISTERS`/`_REGISTERS_TO_MARKERS` in `tests/test_prompt_style_neutrality.py`). **Slice 2 does not solve it** — the discipline's only job is to *flag* it as an `open_question`/open-thread (rubric criterion 6), which the live run already did.
- **Slice 4 — STRESS-TEST.** Pre-mortem (Tiger/Paper-Tiger/Elephant) + red-team ("Fails if ___", rank by cheapest-test) prose in `concept.md` + a `stress_verdict: proceed|revise` enum added to `handoff.py` (the first real handoff-schema growth since Slice 1). Always-on, non-blocking.

## 14. Anti-drift note
Slice 2 opens no new workstream — ① is the active build (ROADMAP lock) and this is its next slice. It touches only `.claude/skills/brainstorm-front-door/*` + `tests/` + `tests/fixtures/frontdoor/`; `pipeline/frontdoor/` is byte-unchanged; no new skill; the two md5 guards are untouched. The whole-front-door plan already scoped EXPAND as Slice 2; this refines its *implementation* (inline discipline, not a skill) against evidence — it does not expand scope. It shrinks it.
