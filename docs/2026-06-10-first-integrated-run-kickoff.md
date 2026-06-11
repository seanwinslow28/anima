# Kickoff — The First Integrated End-to-End Run: "The Spark, Shared"

*Paste-ready brief for a **Claude Code** session. **COSTED — bounded, mostly subscription-absorbed** (~$5 ceiling; the real $ is ~5 NB2 frames + retries + Gemini critic calls; Maya/Sage/Em-escalation bill the Claude subscription). This is the **first time the fleet runs as one chain** — Maya plans a small 5-keyframe two-character loop, you approve at the gate, then Flo generates, Em + the T3 council critique, it's assembled into a loop, and the museum captures the whole thing. The piece is the proof; exercising the integrated fleet is the point. Studio Brief (authored): [`briefs/2026-06-10-spark-shared/00_studio_brief.md`](../briefs/2026-06-10-spark-shared/00_studio_brief.md).*

**Standing doctrine: verify against the tree — never the label.** Two things this session WILL discover (they are expected, not failures): (1) there is **no one-command run orchestrator** — Maya (`PlannerNode`), Flo (`FloNode`), Em (`VisionCriticNode`), the T3 council, and the museum are built as separate nodes/scripts; you are chaining them by hand for the first time. (2) Capture every orchestration seam that's rough — that field note is half the value of this run (it scopes a future `run` orchestrator). Drive the real nodes; don't fake the chain.

## ⚠ FIRST — hard pre-flight (stop if any fails)
1. `git fetch origin && git rev-list --left-right --count main...origin/main` → `0 0`; `git status -s` clean.
2. **Flo-C MUST be merged** (this run depends on it): `git log --oneline -12 | grep -i "flo.*session c\|flo-c\|flo router.*c"` → present. Confirm Flo is **dispatchable** (a run routes through `flo`, not single-model `frame_generate`) and the **HF01 fix** landed. If Flo-C isn't in `main`, **stop** — run it first.
3. **Verdict-baseline guard:** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` → **`2af75906502f1caf8857e18828ceb2e4`**, byte-identical throughout. This run never touches `evals/vision_critic/`.
4. Branch an isolated worktree `feature/first-integrated-run` off `origin/main`.

## ⚠ §0 — before ANY spend (fleet-ops; costed run)
[`docs/fleet-ops-protocol.md`](fleet-ops-protocol.md) §Pre-costed-run checklist:
1. `echo "${ANTHROPIC_API_KEY:+SET}"` prints **nothing** · `claude /status` shows **subscription** (Maya/Sage/Em-escalation bill the subscription, not the API).
2. `GEMINI_API_KEY` present in the worktree `.env` (NB2 generation + Em + Annie). No keys echoed.
3. Singleton confirmed · own PID resolved · single owner.
4. **The human gate is real:** Maya plans, then you STOP and present `plan.md` + the cost preview to Sean. **No generation spend until Sean approves.**
5. At end: orphan sweep clean; worktree removed on merge.

## Read, in order
1. [`briefs/2026-06-10-spark-shared/00_studio_brief.md`](../briefs/2026-06-10-spark-shared/00_studio_brief.md) — the piece. 5-keyframe two-character loop, **all NB2 (standard tier)**, clean loop, frame-chained.
2. [`CLAUDE.md`](../CLAUDE.md) — the 10-phase pipeline + the fleet Skills Map (Maya / Flo / Em / T3 / Mo rows = how each node runs).
3. **The nodes you'll drive:** [`pipeline/agents/planner.py`](../pipeline/agents/planner.py) (`PlannerNode` — Maya, Opus primary → Sonnet validation) + [`pipeline/agents/cost_estimator.py`](../pipeline/agents/cost_estimator.py); [`pipeline/agents/frame_router.py`](../pipeline/agents/frame_router.py) (`FloNode`); [`pipeline/agents/vision_critic.py`](../pipeline/agents/vision_critic.py) (`VisionCriticNode` — Em); [`pipeline/agents/t3_council.py`](../pipeline/agents/t3_council.py); [`scripts/build_museum.py`](../scripts/build_museum.py) (Mo + the `--t3-gate`).
4. **The CLIs/scripts:** `python -m pipeline.cli plan show/approve`; [`pipeline/audit.py`](../pipeline/audit.py) (T1 gates HF/SF/CC); [`pipeline/assemble.sh`](../pipeline/assemble.sh); the Key Commands section of CLAUDE.md.
5. [`manifest.yaml`](../manifest.yaml) — `brief:` (repoint `active_dir` → `briefs/2026-06-10-spark-shared`), `generation.routing:` (Flo's table — every frame routes `standard_keyframe → nb2`), `characters:` (both Bibles), `critics:`.

## PHASE 0 — Maya plans (live Opus) → THE HUMAN GATE
- Point Maya at the brief: set `manifest.brief.active_dir` → `briefs/2026-06-10-spark-shared` (the Studio Brief is authored; Maya drafts `01_production_brief.md` + `acceptance_criteria.json` + `plan.md` + the `RunCostEstimate`).
- Drive `PlannerNode` (real Opus 4.8 primary → Sonnet 4.6 adversarial validation, 3-call ceiling). There is **no `author_plan.py`** — drive the node directly (mirror how `scripts/author_bible.py` drives Cy). Maya reads `00_studio_brief.md` + `PHILOSOPHY.md`.
- The plan must reflect: 5 keyframes, **all `standard_keyframe → NB2`** (the establishing frame is the compositional anchor, NOT an NB Pro hero), frame-chained, 16:9, two characters (sean-anchor + claude-mascot, both locked Bibles loaded), clean loop. Cost preview reads Flo's routing table → should price ~5 × $0.07 + retry budget.
- **STOP. Present `plan.md` + the cost preview to Sean and wait for explicit approval** (`python -m pipeline.cli plan approve` once Sean says go). Nothing below this line runs until then.

## PHASE 5 — Flo generates the 5 keys (NB2) + critics  *(post-approval only)*
- Generate the 5 keyframes through the **Flo path Flo-C wired** — every frame `shot_type: standard_keyframe` → NB2, 16:9. **Frame-chain:** frame 1 (the establishing two-shot anchor) first; frames 2–5 each reference frame 1 + the prior approved frame (the Act-1 Chain-1 pattern) so identity + the mascot's perch hold.
- Per frame: **T1 rule gates** (`pipeline/audit.py` — HF01 16:9, HF02 paper, HF05 aesthetic; CC01/CC02 stylus-right-hand; SF drift) run deterministically. **Em (T2, `VisionCriticNode`)** critiques each frame against the beat + Maya's `acceptance_criteria.json`, proposing prompt diffs (**staged, never auto-applied**).
- **Retry ladder** on failures (re-anchor + correction notes, per CLAUDE.md). Cap at the brief's retry budget; flag for human review at the ceiling rather than burning past it.
- The two-character bar is the headline: **Sean stays Sean and the mascot stays the mascot — no morph** (the exact thing this run tests). Your eye is the arbiter; Em + DINOv2-style checks corroborate.

## PHASE 8 — Assemble the loop
- `bash pipeline/assemble.sh runs/{run_id}` (or the FFmpeg recipe in CLAUDE.md) → build the GIF/WebM loop from the 5 approved frames, **on twos**, returning cleanly (frame 5 → frame 1). A T2 pass reads loop coherence across the cut.

## MUSEUM — capture + Mo + the T3 gate
- `python scripts/build_museum.py --only {run_id} --narrate --t3-gate --render` → exhibits capture the approve/reject/retry trail; **Mo** narrates them (deterministic fallback is fine, or real Sonnet if credentials present); the **T3 council pre-museum gate** runs (chairman `fail` blocks `--render`, `borderline` proceeds, patches stage `auto_apply: false`).

## PHASE 9 — final QA + human
- The `creative-director` rubric pass + **Sean's last look** on the loop (Engine Truth: does it play smoothly and is each character recognizably itself?).

## Deliverables
- [ ] §0 + pre-flight logged (divergence `0 0`, Flo-C confirmed in `main`, baseline md5 unchanged).
- [ ] Maya's `plan.md` + `acceptance_criteria.json` + cost preview; **Sean's approval recorded** before any generation.
- [ ] 5 approved NB2 keyframes (frame-chained, 16:9, two-character, no morph) + the assembled loop (GIF/WebM).
- [ ] Em (T2) verdicts + any staged patches; T1 gate logs; retry trail.
- [ ] Museum exhibit (Mo narration + T3 pre-museum gate verdict) for the run.
- [ ] **Field report** `docs/anima-test-runs/2026-06-10-first-integrated-run.md` — the orchestration story: what chained smoothly, **every seam that needed hand-wiring** (this scopes a future `run` orchestrator), per-agent behavior (Maya/Flo/Em/T3/Mo), cost actual-vs-estimate, and Sean's eye verdict on the loop.
- [ ] CHANGELOG; verdict baseline md5 unchanged; squash PR off `origin/main`; orphan sweep clean.

## Fleet-ops + mistake ledger
Isolated worktree off `origin/main` · single owner · §0 before AND after · subscription billing (`ANTHROPIC_API_KEY` absent) · the human gate after Maya is real (no spend unapproved) · smoke/observe before committing to all 5 · squash PR · clean teardown. **Drive the real nodes (don't fake the chain); keep Cy's locked Bibles untouched (load, never re-author); a declared route still errors honestly; never touch `evals/vision_critic/`.**
