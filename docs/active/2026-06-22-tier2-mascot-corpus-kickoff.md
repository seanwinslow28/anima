# Kickoff — Tier-2 Slice 1: ingest the mascot eval corpus + run the baseline (the measurement foundation)

*Paste into a fresh Claude Code session in the `anima` repo. Self-contained.
Design of record: [`docs/active/2026-06-22-tier2-mascot-corpus-design.md`](2026-06-22-tier2-mascot-corpus-design.md).
Generation spec (Sean's Flow prompts): [`prompts/eval-corpus/claude-mascot-fixture-corpus.md`](../../prompts/eval-corpus/claude-mascot-fixture-corpus.md).*

---

> **STATUS 2026-06-22 — Part 1 (ingest) is DONE (in Cowork, $0).** The 46 fixtures are landed (re-encoded into `evals/vision_critic/fixtures/frames/claude-mascot/` — a subdir, because the mascot reuses the sean fixture IDs and a flat copy would clobber them; re-encoded so they don't collide with the `images/` source under the contamination guard). The 46 cases are appended to `cases.yaml` (`character_id: claude-mascot`, real `IR.claude-mascot.*` handles, the view-class seam handle, leg-count → the real `anatomy.four-stub-legs`). Contamination guard green; the mocked runner scores all 98 cases green; the frozen sean md5 + the 52 sean cases are untouched. `tests/test_patch_efficacy_harness.py` was scoped to sean (the mascot wires into Gate-3 in Slice 2). **Corpus RATIFIED 2026-06-30** — Sean confirmed all 46 by eye; the C02/C03 dupe is resolved (C03 re-rolled to a true left-side view, all 46 fixtures now unique); the `sean_note`s read `ratified by Sean 2026-06-30`. **Remaining for this session: just Part 2 — the costed reference-blind baseline.** Parts 1's read-first + doctrine below still apply; skip Part 1's build steps.

You're building **Tier-2's first slice — the mascot eval corpus + baseline.** The entire Em-vs-eye gap we've measured (the 06-21 finish-register borderlines, the 06-18 leg-count blind spot) is on the **mascot**, but the eval corpus is 52 cases, 100% `sean`, zero mascot — so the calibration is blocked on measurement. This slice makes the mascot measurable, which unblocks every later Em change as eval-gated work. **It is pure measurement: you change nothing in Em.**

**Prerequisite (human, $0):** Sean generates the ~46 mascot fixtures in Google Flow against the corpus spec and ratifies each image + label. **Do not start Part 1 until those ratified fixtures exist** — confirm at §0. You operate the ingest + the costed baseline; Sean's eye is the label ground truth.

Read first: the design doc above; the generation spec; `evals/vision_critic/README.md` + `cases.yaml` (the per-case schema + the contamination/segmentation conventions) + `failure-modes.md`; `evals/vision_critic/scoring.py` + `score.py` (the baseline protocol); `tests/test_fixture_contamination.py`; then `PHILOSOPHY.md`, `ROADMAP.md`, `CLAUDE.md`.

## Doctrine — non-negotiable

- **Strictly additive — this is the load-bearing guard.** The sean 52 cases, the sean verdict-baseline trace, and its frozen md5 `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4` are **untouched**. Nothing in `pipeline/agents/vision_critic.py` changes (Em's contract — the `cites_criteria` invariant + the verdict vocabulary — is off-limits). The mascot baseline is its **own** dated trace; the sean md5 cannot move. Re-assert it at the start and the end.
- **Verify against the tree, never trust a label — including this kickoff.** Confirm the exact `cases.yaml` per-case schema (name / corpus_id / pair / description / checkpoint / character_id / input / beat_description / impact_tags / case_class / expected_verdict / expected_cites / defect_label / is_intentionally_red / sean_note), the `character_id` field (set every mascot case to `claude-mascot`), the IR handles that exist on the mascot (`characters/claude-mascot/acceptance_criteria.json` — use real `IR.claude-mascot.*` handles in `expected_cites`, and the same seam-handle convention the sean corpus uses where none exists), and the baseline invocation in `score.py` — before writing.
- **Eval discipline (from the README + failure-modes.md).** Ships-red is the artifact — **never tune a case until Em passes it** (that measures the thermometer against itself). A label edit is legitimate ONLY as a validity fix, never to flatter Em. Sean is the single labeler; the cases encode his ratified rubric.
- **Fleet-ops for the costed baseline** ([`docs/architecture/fleet-ops-protocol.md`](../architecture/fleet-ops-protocol.md) — §6 the operator path): subscription billing (`ANTHROPIC_API_KEY` absent), `GEMINI_API_KEY` present; one isolated worktree; single owner; and because you drive it in-session, run every costed command under the **env-strip** (canary ~7s, not ~94s).
- **Part 1 is $0** (ingest + the CI-green mocked runner). **Part 2 is the only spend** (the live baseline).

## §0 — pre-flight

```bash
cd <anima checkout> && git fetch origin && git log --oneline -1 origin/main
md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md   # 2af75906… (must stay this at the end)
md5sum pipeline/agents/prompts/sean-screenwriting-voice.md                # 945af824…
ls <Sean's ratified mascot fixtures>          # ~46 files, named by ID (C01.., P-D1.., A-D1.., …); confirm present + ratified
echo "ANTHROPIC=${ANTHROPIC_API_KEY:-ABSENT}  GEMINI=${GEMINI:+SET}"       # ABSENT / SET (Part 2)
.venv/bin/pytest evals/vision_critic/runner.py -q                          # sean suite green baseline
```

One isolated worktree off `origin/main`; single owner.

## Part 1 — ingest the corpus ($0, additive)

1. **Land the fixtures.** Place Sean's ratified mascot fixtures under `evals/vision_critic/fixtures/frames/` (uniform JPEG, matching the sean set), named by ID. They are generated outputs — never copies of anything under `characters/` or `images/` (the contamination guard enforces this).
2. **Author the mascot `cases.yaml` entries.** Append (do not edit existing sean cases) ~46 cases using the established per-case schema, `character_id: claude-mascot`, each defect naming its clean `pair:` and exactly one `defect_label` (or `clean`), `case_class` in {clean, identity_style}, `expected_verdict`, `expected_cites` from real `IR.claude-mascot.*` handles (seam handles where none exists, per the sean convention). Mirror the corpus spec's class structure (box-proportion, view-correctness, anatomy-count, palette, construction-lines, shading-register). The view-correctness cases carry the corruption in the **declared view** (`beat_description`), not the pixels — same trick as the sean V-* cases.
3. **Extend the contamination guard.** `tests/test_fixture_contamination.py` must fail CI if any mascot fixture shares a SHA-256/inode with anything under `characters/` or `images/`. Run it green.
4. **Keep the CI-green mocked runner green.** `.venv/bin/pytest evals/vision_critic/runner.py` must load + score every new case, the segmented report stays well-formed, and the `cites_criteria` invariant doesn't crash. No scored claim here — Part 1 only proves the plumbing.

Commit Part 1 ($0) before spending.

## Part 2 — the costed reference-blind baseline (the mascot verdict baseline)

Mirror the sean **G5 protocol**: reference-blind, **N=5 majority vote**, gemini-3.5-flash pinned (+ Opus 4.7 on escalation, as Em ships). Run `score.py` scoped to the mascot cases (verify the scoping flag against the tree; the sean cases are not re-run and their trace is not touched). Write the **mascot verdict baseline** to its own dated trace (`evals/vision_critic/traces/mascot-baseline-2026-MM-DD.md`) + the segment report: **precision / recall / false-pass on the mascot defect class**, segmented performs vs motion-proper. Sean ratifies the baseline as the gate for Slice 2.

## Acceptance (all must hold)

- A Sean-ratified mascot corpus appended to `cases.yaml` (`character_id: claude-mascot`, paired, single-axis), fixtures landed, contamination guard extended + green, CI-green mocked runner green.
- A ratified **mascot verdict baseline** trace (reference-blind N=5) with precision/recall/false-pass on the defect class, segmented.
- **The guard held:** the sean 52 cases, the sean baseline trace, and the frozen md5 `2af75906…` are provably untouched; nothing in `pipeline/agents/vision_critic.py` changed; the shared-voice md5 `945af824…` intact.
- CHANGELOG + CLAUDE.md (the Em row: mascot corpus now exists, baseline figures) + the ROADMAP workstream-2 row updated. One squash PR off the isolated worktree; clean teardown.

## When done

Report: the commits; the mascot baseline numbers (precision/recall/false-pass, segmented) + the spend; confirmation the sean md5 + baseline are untouched; and a one-paragraph note on any seam (especially any class where NB2 refused a corruption and Sean hand-drew it — that's data about Em's blind spot). Then **Slice 2 — the calibration (severity + leg-count detection + cross-namespace coherence)** gets its own brainstorm, now eval-gated against this baseline. Per the anti-drift contract, Current Focus stays on Tier-2.
