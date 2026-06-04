# Kickoff — Eval-foundation reset, part 2: integrate the clean dataset, rebuild the ruler

*2026-06-04. A paste-ready brief for a FRESH Claude Cowork session continuing the eval-foundation reset. Part 1 (2026-06-03) diagnosed the broken foundation and produced the fixture corpus; Sean has since authored the complete dataset. This session integrates it: ratify labels, land the gold-standard references in the repo, rebuild `cases.yaml`, ship the CI contamination guard, and stage the costed Em re-baseline for a Claude Code handoff. **No costed work runs inside this session.**

---

## For the fresh session — read this first, then verify everything against the tree

You are picking up anima's eval-foundation reset mid-flight. The standing doctrine of this whole arc: **verify against the tree, never trust a label — including this brief.** Confirm counts, paths, and claims before acting.

Read, in order:

1. `PHILOSOPHY.md` — empirical-not-vibes; the human owns taste; critics propose, never decide.
2. `docs/2026-06-03-eval-foundation-reset-plan.md` — **the decision artifact this session executes.** The verified four-defect diagnosis (19/23 old fixtures were SHA-identical Bible copies; the locked Bible's body turnarounds drifted to ~1:4–1:5.3 vs 1:7; compound labels; n too small), the six ratified failure classes, the layer-ownership map (geometry→Bible-lock, style→Em), and the G1–G6 gate sequence.
3. `prompts/eval-corpus/sean-anchor-fixture-corpus.md` — **the corpus spec (v2, minimal grammar).** Every fixture ID ↔ its prompt ↔ its class ↔ its clean pair. This is the labeling source of truth for the new `cases.yaml`.
4. `prompts/eval-corpus/sean-anchor-turnaround-sheet.md` — the two gold-standard turnaround prompts (full-body with the 1:7 lock; head) and why they were split.
5. `docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md` — the eval handbook (error-analysis-first, binary single-axis cases, class balance, ships-red). The corpus was designed to obey it; keep it obeyed.
6. `docs/research/2026-05-30-nb2-editing-character-consistency-template.md` — NB2 editing physics. Headline that part 1 re-learned the hard way: terse text + strong reference beats verbose prose.
7. `CLAUDE.md` — Critic Stack, Character Bible primitive, Em's current state (reference-blind default, flag-gated). `CHANGELOG.md` 2026-06-03 entries record everything part 1 did.
8. The NO-GO arc, for why nothing gets re-run on the old fixtures: `docs/anima-test-runs/2026-06-02-em-gemini-transport-rebaseline-postmortem.md`, the Workstream B DINOv2 postmortem, and the parked SF03 design (in the `sf03-proportion-gate-design` worktree).

## What exists right now (verified 2026-06-03, late)

- **The dataset is COMPLETE: `images/sean-character-dataset/`** — `1-clean/` C01–C16 (16) + `2-defects/` (30): P-D1–3 + P-B1 + `P-B2-1` (proportion), V-D1–4 + V-B1 (view-correctness), A-D1–4 (anatomy-count — Sean confirmed the hand/digit/limb interpretation by authoring them), PA-D1–5 + an extra `PA-D3-1` (palette), CL-D1–4 + CL-B1 (construction-lines), SH-D1–4 + SH-B1 (shading-register). 46 files, uniform JPEG, authored by Sean in Google Flow (NB2, free tier) against the corpus spec's prompts. Sean generated everything including the borderlines.
- **Gold-standard turnarounds exist but are NOT in the repo yet:** `~/Downloads/**sean-character-dataset/sean-anchor-set/` holds `sean-character-full-body-turnaround.png` + `sean-head-turnaround.png` — 1K native (deliberate: the 2K export is a pure 2× upscale that *removes* ~13% of the pencil grit two classes depend on; decision logged in CHANGELOG). Sean has eyeballed both at 1:7 and trusts them. They are the new identity/proportion references and the A4 re-bake material.
- **Old eval set still in place and still condemned:** `evals/vision_critic/cases.yaml` (29 cases) + `fixtures/frames/` (19/23 contaminated). Retired in spirit; not yet physically replaced. The old baseline figures (0.62 / 1.00 / 0.15) are void.
- **Locked decisions (do not relitigate):** six classes (proportion, palette, view-correctness, anatomy-count, construction-lines, shading-register; hair/jaw/eye deferred with a promotion trigger); geometry→Bible-lock vs style→Em ownership; shared clean pool; paired clean/defect; 1K uniform; generate-first.
- **Parked, not dead:** SF03 gate build (design in its worktree), references question (re-test only on the clean set), DINOv2 backstop, mascot corpus (needs its own turnaround first), Astro museum export, T3 council.

## What this session does, in order

1. **Inventory + QC the dataset (uncosted).** Verify resolution/format uniformity; fix the two naming anomalies (`P-B2-1`→`P-B2`; ask Sean whether `PA-D3-1` is a keeper-extra or a discard); confirm every ID in the corpus spec has exactly one file. Decide JPEG-vs-PNG once (uniformity matters more than format; don't mix).
2. **Ratification pass with Sean (the gate for everything downstream).** Walk the 46 images against their spec'd labels — view them, don't trust filenames. For each defect: does it isolate its ONE class (e.g., did a proportion defect also drift palette)? Sean's call per image: ratify / re-roll / relabel. Labels are his; propose, never lock unilaterally.
3. **Land the gold standard in the repo.** Move the two turnaround sheets into `characters/sean-anchor/source-refs/` (and the dataset is already at `images/sean-character-dataset/`). Then put the **A4 re-bake decision** to Sean: ingest per-view plates as crops from the new sheets (the zero-drift `#region` ingest path Cy already has — see the claude-mascot `.regions.json` precedent) to replace the drifted `turnarounds/body-*.png`, vs. keeping the sheets whole as source-refs and re-baking plates through Cy later. The reset plan wants the Bible clean before the eval references it; the human-gate version (Sean's eyeball at 1:7) may stand in for the not-yet-built SF03 gate — reconcile this ordering with him explicitly.
4. **Rebuild `evals/vision_critic/` fixtures + `cases.yaml`.** New fixture tree from the ratified dataset; new cases carrying the corpus spec's schema: one `defect_label` per case (exactly one of the six classes or `clean`), `expected_verdict` (borderlines → `borderline`), pair IDs, and — for view-correctness — the **declared-view trick**: the image is a clean drawing of the *wrong* view; the corruption lives in the case's declared view/beat, not the pixels. Keep the 6 motion_proper ships-red cases unchanged (separate segment, not part of this reset). Map `expected_cites` to the existing IR.* handles where they exist.
5. **Ship the CI contamination guard.** A test that fails if any fixture under `evals/vision_critic/fixtures/` shares a SHA-256 or inode with anything under `characters/` or `images/` *reference* material (the turnaround sheets included — fixtures must never BE the references). Run it; it must pass on the new corpus by construction.
6. **Stage the Em re-baseline (G5) as a Claude Code handoff — do NOT run it here.** Write the run brief: `python -m evals.vision_critic.score` on the new corpus, N=5 replication with majority vote per the postmortem's scorer-replication standard, reference-blind default (flag stays off), gemini-3.5-flash pinned via the API transport. This number replaces 0.62/1.00/0.15 and is the gate for resuming SF03/references/DINOv2 work.
7. **Maintenance.** CHANGELOG entry per change; the CLAUDE.md updates (layer-ownership map, new eval-foundation state, corpus location) are now due — Sean approved the plan by executing it, but confirm before landing the CLAUDE.md edit.

## Sean's role (the human-taste work)

He is the ground truth. He authored every image; this session renders his taste checkable: he ratifies each label, rules on the anomalies and the JPEG/PNG call, decides the A4 ingest path, and gives the final go on the re-baseline handoff.

## Operating rules

- Cowork = orient, ratify, integrate, stage. **No model spend in this session.** The re-baseline is a Claude Code handoff under fleet-ops discipline (`docs/fleet-ops-protocol.md`): subscription SDK for Claude (`ANTHROPIC_API_KEY` absent), bounded `GEMINI_API_KEY` for Gemini, isolated worktree, single owner, clean teardown.
- Verify against the tree; never trust a label — file counts, SHAs, model IDs, this brief.
- Ships-red discipline: never tune a case to flatter Em; a label edit is legitimate only as a validity fix.
- The deferred identity modes (hair/jaw/eye) stay deferred until the six-class corpus is clean and re-baselined.

## First actions

1. Task list.
2. Verify the dataset inventory above against the tree (counts, names, dimensions, format).
3. Start the ratification pass with Sean.
4. Land references; rebuild fixtures + cases; ship the guard.
5. Stop and review with Sean before writing the re-baseline handoff.

The reframe to carry in: part 1 fixed the diagnosis and the authoring; this session makes the ruler real. When it ends, anima should have — for the first time — an eval set where every number is about the critic, not about the fixtures.
