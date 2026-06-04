# Em Re-Baseline (G5) — Field Report

*2026-06-04. Executes [`docs/2026-06-03-em-rebaseline-g5-handoff.md`](../2026-06-03-em-rebaseline-g5-handoff.md) — the G5 gate of the eval-foundation reset. These are **THE new baseline numbers**; they replace the void contaminated figures (precision 0.62 / recall 1.00 / false_pass 0.15). Numbers stand pending Sean's ratification before the CLAUDE.md Em-row update.*

---

## TL;DR — the number

**Performs segment (the headline, n=44 = 16 clean + 28 single-axis defects), reference-blind, N=5 majority vote:**

| Metric | **G5 (new)** | Void (retired) |
|---|---|---|
| **precision** | **0.97** | 0.62 |
| **recall** | **1.00** | 1.00 |
| **false_pass_rate** | **0.00** | 0.15 |

Em caught **all 28 defects** across all six classes (recall 1.00, FN=0) and **never false-passed** a defect (false_pass 0.00). The single error is one false-positive on a clean case (`clean-c06`), giving precision 0.97. This is a large, clean improvement over the void baseline — and unlike that baseline it was measured on an independent, contamination-guarded corpus.

**The asterisk:** verdict accuracy is excellent, but **citation accuracy is near-zero (cites-correct = 0.03)** — Em reaches the right verdict while almost never citing the expected criterion. See Finding 2. This does not move the headline metric contract (precision/recall/false_pass), but it is the most important thing this run surfaced for G6.

---

## Run configuration & provenance

- **Command:** `python -m evals.vision_critic.score --runs 5` (segment=all → all 50 cases).
- **Replication:** N=5 full passes, per-case **majority verdict** (3-of-5; conservative tie-break fail > borderline > pass). Per-segment false_pass **band** + per-run verdict table preserved (flips not averaged away).
- **Model:** `gemini-3.5-flash` **pinned by ID** via the `gemini_api` transport (`pipeline/agents/gemini_api_runner.py`), Opus 4.7 SDK escalation for `hero`/`identity_critical` cases below the 0.7 confidence threshold. Served model read back from `resp.model_version`.
- **References:** `critics.t2.attach_references: false` — **reference-blind** (shipped default; flag stays off — flipping it is G6 work gated on DINOv2 + a clean re-baseline).
- **Corpus:** 50 cases (16 clean + 28 single-axis across six ratified classes + 6 `motion_proper` ships-red), 44 independent Sean-authored JPEG fixtures (1376×768), contamination guard green. Two slots (P-B1, PA-D4) remain pending Sean re-rolls — **excluded from this baseline by design**; when they land the delta is two added cases, not a re-baseline.
- **Coverage:** **247 of 250 case-runs scored, 3 errored** (Em's empty-cites invariant — Finding 5). No case errored in all 5 runs, so all 50 cases carry a majority verdict; **zero total gaps**.
- **Fleet-ops:** isolated worktree (`eval/em-rebaseline-g5`); `ANTHROPIC_API_KEY` absent throughout (subscription billing for escalations); `GEMINI_API_KEY` bounded from `.env`; singleton confirmed; no `start_new_session` on the costed worker; no quota-throttling (zero 429s).
- **Pre-flight fix:** runner.py's "mocked" pre-flight #2 was firing **real costed Gemini calls** (mock covered only the legacy `agy` transport, never `gemini_api`). Fixed before the baseline; see CHANGELOG 2026-06-04 and commit `71f8d80`.

---

## Headline matrix (majority vote, N=5)

### Performs (identity/style + clean) — n=44
- confusion: **TP=28 FP=1 FN=0 TN=15**
- **precision=0.97 · recall=1.00 · false_pass_rate=0.00**
- 3-way exact agreement=0.91 · cites-correct=**0.03** · mean wall 30.6s
- borderline→fail slippages: `construction-cld3`, `construction-cld4`

### Motion-proper (expected red) — n=6
- confusion: **TP=5 FP=0 FN=1 TN=0**
- precision=1.00 · recall=0.83 · **false_pass_rate=0.17** (the lone slip: `motion-t2-arc`)
- 3-way exact agreement=0.17 · mean wall 40.0s

### Overall — n=50
- confusion: **TP=33 FP=1 FN=1 TN=15**
- precision=0.97 · recall=0.97 · false_pass_rate=0.03

---

## Per-class catch (majority verdict)

| Class | Cases | Em flagged (fail/borderline) | Caught | Notes |
|---|---|---|---|---|
| clean | 16 | 1 | n/a | 15 pass (TN), **1 false-positive: `clean-c06`** (left-profile, flagged fail all 5 runs) |
| proportion | 4 | 4 | **4/4** | `pb2` correctly borderline; `pd3` errored run 1, recovered fail |
| view-correctness | 5 | 5 | **5/5** | declared-view trick worked — all 4 `vd*` fail; `vb1` borderline (errored run 2, recovered) |
| anatomy-count | 4 | 4 | **4/4** | `ad1` errored run 2, recovered fail; `ad3` (third-arm) flipped to pass in run 5 — near-miss |
| palette | 5 | 5 | **5/5** | all fail, zero variance |
| construction-lines | 5 | 5 | **5/5** | `cld3/cld4/clb1` borderline (the clean-final / faint-trace cases) |
| shading-register | 5 | 5 | **5/5** | all fail, zero variance |
| **performs defects** | **28** | **28** | **28/28** | **recall 1.00, FN=0** |
| motion_proper | 6 | 5 | 5/6 | only `motion-t2-arc` slipped — see Finding 4 |

---

## Key findings

**1 — Reference-blind Em is a strong verdict engine (0.97 / 1.00 / 0.00).** Every defect in all six performs-classes was flagged; no defect was ever passed. This is the safe, recall-1.00 / false_pass-0.00 profile the 2026-06-02 work was protecting, now measured on a trustworthy corpus. It vindicates keeping references **off** as the default — Em does not need them to detect single-axis defects.

**2 — Citations are the weak axis: cites-correct = 0.03.** Em reaches the right verdict but almost never cites the *expected* criterion. Two contributing causes, to be separated in G6:
  - *By construction:* the geometry classes (proportion, view-correctness, anatomy-count) carry **declared-seam handles** as `expected_cites` (`view.declared-view-matches-drawn-view`, `anatomy.count-correct`) that **do not exist as IR rules in Em's merged criteria** — she cannot cite-correct what she was never given.
  - *Possibly genuine:* even the style classes (palette/construction/shading), which map to real `IR.sean.*` handles, scored near-zero cites-correct — suggesting Em flags the right defect but cites a generic/wrong criterion rather than the specific rule. This needs per-case cite inspection (not persisted in this run) to confirm.
  This is the headline G6 input: a critic that "proposes fixes grounded in criteria" is only as useful as its grounding. The verdict is trustworthy; the *reason* is not yet.

**3 — One consistent clean false-positive: `clean-c06`.** A Sean-ratified clean left-profile, flagged `fail` in all 5 runs (the entire performs FP). Consistent (not variance), so it's a real Em disagreement with the ground truth on this one image — worth a targeted look in G6 (is Em seeing a left-profile artifact, or mis-reading a legitimate view?).

**4 — Motion: Em flagged 5/6, against the "expected 0 catches" framing — a finding, not a win.** The handoff treats motion_proper as structurally invisible to a still contact sheet. Yet Em flagged five of six. Read carefully: she is **not perceiving motion** — she is catching **spatial traces** the motion defects leave in the contact-sheet frames (jitter/flicker/texture-crawl show up as per-frame anomalies; arc defects may show as pose-spacing). The one true slip — **`motion-t2-arc`** (passed all 5 runs) — is the pure timing/arc defect with no per-frame spatial tell, exactly the case the contact sheet *can't* see. So the contact-sheet path catches motion defects that have a spatial signature and misses the purely-temporal one — useful calibration of what the phase-6 path can and can't do, and it reframes (does not invalidate) the ships-red expectation.

**5 — Geometry classes trip Em's empty-cites invariant (3/250 errored case-runs).** `proportion-pd3` (run 1), `view-vb1` (run 2), `anatomy-ad1` (run 2): Em returned a blocking verdict (`borderline`/`fail`) with **empty `cites_criteria`**, and the production safety invariant (v2 brainstorm §2.3 Pattern B — no uncited block) raised, dropping that case-run to an honest gap. All three are geometry-class, consistent with Finding 2's root cause (geometry has no citeable criteria for Em). It is **sporadic** (the same cases scored in their other runs; runs 3–4 errored zero), so majority vote recovered every verdict — but it is the same disease as the cites-correct=0.03: in production a geometry flag from Em would be *rejected at the contract layer*, not surfaced. Note the design tension this exposes: a production safety invariant (reject uncited blocks) **eats eval signal** (Em *did* detect the defect; the verdict was just ungrounded). G6 should decide whether geometry gets real citeable IR criteria, or whether the eval should record the verdict separately from the citation.

**6 — Model variance is real but majority-resolved.** 7 of 50 cases flipped across runs (`clean-c01`, `clean-c05`, `view-vb1`, `anatomy-ad3`, `construction-cld3`, `motion-s0-flicker`, `motion-rev-jitter`). Most were single-run outliers (4-1 splits) the majority absorbed. The **false_pass band** shows where the variance bites:
  - performs: mean 0.01, band **0.00–0.04** (per-run [0.0, 0.0, 0.0, 0.0, 0.04])
  - motion_proper: mean 0.20, band **0.17–0.33** (per-run [0.17, 0.17, 0.17, 0.17, 0.33])
  - overall: mean 0.04, band **0.03–0.09**
  The performs safety number is stable (≤0.04 in the worst single run). The motion band is wider, driven by the small n=6 and the `anatomy-ad3`/`motion-s0` pass-flips. This is exactly why N=5 + the band exist — a single pass would have reported a point estimate hiding a 0.00→0.04 (performs) / 0.17→0.33 (motion) run-to-run spread.

---

## Full per-run verdict matrix

See [`evals/vision_critic/last-run.md`](../../evals/vision_critic/last-run.md) and the dated trace [`evals/vision_critic/traces/baseline-2026-06-04-scored.md`](../../evals/vision_critic/traces/baseline-2026-06-04-scored.md) for the complete 50-case × 5-run table (verdicts + FLIP markers) and the errored-case appendix.

---

## Cost & operations

- **~247 live Gemini calls** + a handful of Opus 4.7 escalations (the 78–102s walls vs the ~30s Gemini median). Within the handoff's $2.50–12.50 expectation.
- Zero quota-throttling (no 429 / RESOURCE_EXHAUSTED) — the `gemini_api` transport pivot did its job; the partial-N abort condition never triggered.
- Subprocess-per-case isolation held: 3 isolated empty-cites errors did not abort the run.

---

## Scope & caveats (for ratification)

This is a valid, honest baseline for what it measures. Before it becomes *the* locked number in CLAUDE.md, note the scope:

1. **Verdict baseline, not citation baseline.** The 0.97/1.00/0.00 is verdict accuracy. Citation accuracy (0.03) is a separate, much weaker axis — partly an eval-construction artifact (geometry), partly possibly real.
2. **Geometry detection is real but ungrounded.** Em *detects* geometry defects (caught 13/13) but cannot *cite* them, and in production those flags would be rejected by the empty-cites invariant. The geometry half of the matrix measures perception, not production behavior.
3. **Motion is partial by design** — 5/6 caught via spatial traces, not motion perception; `motion-t2-arc` is the structural blind spot.
4. **Two corpus slots pending** (P-B1, PA-D4) — re-baseline not required when they land; they add two cases.

---

## G6 gates this unlocks (NOT done in this run)

- **SF03 proportion-gate build** (Approach A armature probe → A or B).
- **The references question** — re-test on the clean corpus, flag flip gated on DINOv2 + clearing the false-pass gate.
- **DINOv2 deterministic identity backstop.**
- **New this run:** decide how to handle the cites-correct=0.03 / geometry empty-cites finding — add citeable IR criteria for the geometry classes, or record the verdict separately from the citation in the eval. And a targeted look at the `clean-c06` consistent false-positive.
- Deferred identity modes (hair/jaw/eye) corpus extension; mascot corpus (needs its own turnaround sheet first).
