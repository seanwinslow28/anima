# Cowork Continuation Prompt — anima / the run orchestrator

*Paste this whole document into a fresh Cowork session. It catches you up on everything done so far, the files to read, and the active work: scoping and planning **the run orchestrator** — the fleet's agreed next priority after the first integrated end-to-end run shipped. Date of handoff: 2026-06-11.*

---

You're picking up a long-running build in **anima** — Sean's 2D animation pipeline made by a human + a fleet of named agents. The fleet just **ran end-to-end as one chain for the first time** and shipped a piece. Your job this session is to be a thinking partner and help Sean **scope, sequence, and plan the run orchestrator** — the one major fleet member still missing — then produce a plan + a paste-ready Claude Code kickoff. **Read `CLAUDE.md` and `PHILOSOPHY.md` first** (the project manual + the load-bearing intent), then the field report below.

## How we work (standing doctrine — internalize this)
- **Cowork plans and reviews ($0, no model spend); Claude Code executes costed/multi-step builds under fleet-ops.** The rhythm: Cowork writes a dated plan doc + a paste-ready Claude Code kickoff → Sean runs it in Claude Code → Sean merges + pulls → Cowork verifies the result against the tree and plans the next step.
- **Verify against the tree, never trust a label — including reports, docstrings, and this prompt.** Use the `mcp__workspace__bash` shell to check git state, run/read real code, and confirm claims before asserting. Cautionary tales that earned this rule: a flag silently off measured nothing; a runbook claimed a loop "self-isolates" and the run crashed on case #0; the T3 smoke caught a docstring lying about `agy -m`; a "ticketed" follow-on was never actually filed (caught 2026-06-10); Flo's CHANGELOG read "built" while nothing dispatched it (caught 2026-06-10). Assert before you spend.
- **The verdict-baseline guard:** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` must stay **`2af75906502f1caf8857e18828ceb2e4`** — it's Em's eval baseline; all new work is additive and must never touch `evals/vision_critic/`.
- **Use AskUserQuestion to surface genuine scope/strategy forks before building.** Use TaskCreate/TaskUpdate to track multi-step work. Present files with the present-files tool. Keep responses concise and direct (Sean's stated preference: give the "why," don't over-explain). Sean is a PM who digs into the "how" — respect that.
- **Fleet-ops for any costed run:** isolated git worktree off `origin/main`, single owner, §0 gates before spend, subscription billing where possible (`ANTHROPIC_API_KEY` absent so Opus bills the Claude subscription), bounded API keys from `.env`, land via squash PR, clean teardown. Full protocol: `docs/fleet-ops-protocol.md`.

## Where the repo is right now
- Branch `main`, HEAD **`f157564`** (#48), clean, divergence `0 0` with origin. (Verify with `git log --oneline -6`; if Sean has done more by the time you read this, HEAD will be newer.)
- Recent landed PRs: **#45** Flo-C (Flo dispatched in the run path + HF01 fix), **#46** Flo-C report, **#47** the first integrated run + 2 PlannerNode fixes, **#48** the run kickoff brief.
- The pencil-test (Act 1 shipped, Act 2 ready) is the **first reference implementation**, not the project's definition. anima itself is the 10-phase pipeline + the agent fleet.

## What just happened (the recent arc)
1. **Flo (Phase 5 generation router) — BUILT across three sessions.** Flo-A ($0 skeleton: `generation.routing:` + `FloNode` + Maya cost-preview), Flo-B (costed fal.ai in-between pencil pilot → **NB2 pivot**: Sean's eye disqualified fal Seedream for morphing faces through the tween — the metric missed it, the eye caught it; Reve was disqualified the same way earlier), Flo-C (**made Flo live** in the run path — it was registered-not-dispatched — + the HF01 NB-Pro-renders-square fix). Two open Flo tickets in code-brain's manual lane: self-hosted FLUX + Shakker sketch-LoRA (the $0-ongoing in-between future), and the NB-Pro-aspect-ratio production gap (fixed in Flo-C; verify).
2. **The first integrated end-to-end run — SHIPPED (PR #47, 2026-06-11, ~$0.66 actual).** Maya → Flo → Em → assemble → museum ran as **one chain for the first time** on "The Spark, Shared" — a 6-keyframe two-character pencil-test micro-loop (Sean draws; the Claude mascot perched on his shoulder notices → excites → delights → settles → loops). **Sean's eye: SHIPS.** Both identities held (the two-character consistency bar this run existed to test). The loop is preserved at `runs/2026-06-11-spark-shared-first-integrated/export/SS_L1_loop.{gif,mp4,webm}`. **The nodes are solid; what's missing is the orchestrator** — every node was chained by hand.

## The fleet state (built vs missing)
**Built + proven in a real run:** Maya (Phase 0 planner, Opus — now with 2 live-run bug fixes), Cy (Phase 2 character designer; sean-anchor + claude-mascot Bibles locked), Flo (Phase 5 router, now LIVE in the run path), Em (T2 vision critic, fully evaluated, criteria-grounded citations working in production), Mo (museum writer), the T3 council (built + validated separately), the DAG runner *engine* (`pipeline/dag.py`), the T1 rule gates, and two new hand-built **driver scripts** (`scripts/author_plan.py` for Maya, `scripts/spark_frame.py` per-frame).
**Missing:** **the run orchestrator (THIS SESSION'S WORK)** — there is no whole-piece chainer; the DAG runner is the engine but no full-piece graph is authored and no `run` CLI exists. Also still missing: Sam + Bea (Phase 3 scriptwriter + storyboard artist; Phase 3 is human-authored today) and Phase 4 Animatic (so the `post_animatic` T3 gate is a declared seam).

---

## THE ACTIVE WORK: the run orchestrator

**Why it's next (Sean's call, 2026-06-10/11):** the first integrated run proved the *nodes* work but ran the chain by hand. The field report logged **16 orchestration seams** — every hand-wiring point — and those seams **are the orchestrator's spec.** This is the agreed next priority.

**What it is (the field report's synthesis):** a `python -m pipeline.run --brief <dir>` that drives Maya (right timeout + parsed envelope + stub guard) → stops at the human gate → wires the criteria bundle once → per frame runs Flo → T1 → Em (multi-character) → stages patches → presents for Sean's eye → retries with a correction note → assembles (handling JPEG-as-PNG, arbitrary key names, variable holds) → captures a real loop exhibit to the museum.

**Reassuring scope note:** this is NOT a from-scratch agent build. The DAG runner already does the hard part (typed nodes, content-addressed caching, `post_run` hooks). The orchestrator is mostly: author the full-piece graph (`phases.*.nodes` chaining planner→flo→audit→vision_critic→assemble→museum), a thin `run` CLI/driver on top, and the one genuinely new piece — **handling the human approval gate mid-graph** (pause after Maya, resume on approval). The two driver scripts committed in the run (`author_plan.py`, `spark_frame.py`) are its prototype.

**The 16 seams, grouped (read the field report for the full text — this is the planning raw material):**
- **Orchestrator-core (the chaining itself):** #1 (no `author_plan.py` — now built), #6 (Em has no CLI), #7 (patch staging needs the DAG runner's `post_run` hook), #8 (`ctx.criteria` is a bundle, `brief_file` doesn't auto-wire from `brief.active_dir`), #9 + #11 (`character_id` means different things to Flo (folder key `sean-anchor`) vs Em (IR namespace `sean`) — a two-character frame needs two Em passes on the namespace ids), #16 (the whole chain + per-frame human gate is hand-wired: no queue, no resume, no one-command run).
- **Real bugs / fixes that should land regardless:** #2 + #3 (PlannerNode 120s timeout + envelope parser — **already fixed** in #47), #5 (**`cost_estimator._phase_2_cost` double-counts locked Bibles** → phantom ~$5.40 Phase-2 band on an animation_piece run; NOT fixed — deserves a TDD fix), #12 (Gemini saves **JPEG-as-`.png`** → ffmpeg rejects it; re-encode via PIL before assembly), #13 (`assemble.sh` is hardcoded to the PT_A1 sequence — won't see new pieces), #10 (Em's **absolute** left/right stylus-hand verdict is noisy in profile — CC01 wants a **frame-to-frame** continuity check, not per-frame-absolute).
- **Architecture / infra findings:** #4 (**nested-SDK rate-limit contention** — driving an Opus node via the Claude Agent SDK from *inside* a live Opus Claude Code session adds ~285–390s throttle latency; the biggest "this is rough" finding — implies the orchestrator should run heavy Opus nodes **out of the interactive session**), #14 (**the museum has no exhibit type for a keyframe-loop run + no `project_slug`** → the loop was NOT captured into the museum; it lives only in gitignored `runs/`), #15 (bash CWD unreliable between calls — explicit `cd` always).

**The genuine forks to surface with Sean before planning (use AskUserQuestion):**
1. **Slicing / sequencing.** One big orchestrator build, or incremental — e.g., (a) a quick "cheap-bug cleanup" pass first (#5 cost double-count, #12 JPEG-as-PNG, #13 assemble.sh generalize, #10 Em CC01 continuity — all small, high-value, independent of the orchestrator), then (b) the orchestrator core, then (c) museum capture (#14)? Sean tends to prefer disciplined increments with $0 verification between.
2. **The nested-Opus constraint (#4).** Should the orchestrator be designed to run **standalone from a plain shell** (not from inside a Claude Code session) so heavy Opus nodes (Maya, T3) run uncontended? This is an architecture decision that shapes the whole build. The T3 gate was stopped in the run for exactly this reason — run it out-of-session.
3. **Museum capture (#14) priority.** Fixing it is the gate to the **portfolio museum Astro export** (the job-hunt payoff — see backlog). The loop is portfolio-worthy *now* but isn't in the museum. Pull #14 forward, or keep it in the orchestrator build?
4. **Human-gate UX.** How should the mid-graph gate work — pause-and-resume (orchestrator writes state, stops, Sean approves, re-invoke resumes), or the gate stays a Cowork/Claude-Code-mediated step? This is the one genuinely new mechanism.

**Immediate next action:** read `CLAUDE.md` + `PHILOSOPHY.md` + the field report, verify HEAD/divergence/md5, then surface the forks above with Sean (AskUserQuestion), converge on a slicing, and write the orchestrator **build plan** + the first paste-ready Claude Code kickoff (likely the $0 cheap-bug-cleanup pass or the orchestrator-core skeleton, depending on Sean's call). Don't pre-decide the slice — that's the conversation.

---

## What's still on the list (backlog, roughly prioritized)
1. **The run orchestrator** (active — this session scopes + plans it).
2. **Museum capture for keyframe-loop runs (seam #14)** — unblocks the portfolio museum export; the shipped loop is waiting on it. May fold into the orchestrator or land first.
3. **The museum Astro export into `sw-ai-pm-portfolio`** — the job-hunt portfolio payoff; blocked on #14 producing a real exhibit. "The Spark, Shared" loop + the Engine-Truth grin-as-peak override is strong portfolio narrative.
4. **The cheap seam fixes** (#5 cost double-count, #12 JPEG-as-PNG, #13 assemble.sh, #10 Em CC01 continuity) — small, independent, high-value; candidates for a pre-orchestrator cleanup pass.
5. **T3 gate, run out-of-session** over a real (non-thin) exhibit — validated separately already; the lesson is *where* to run it (uncontended Opus, after #14).
6. **Phase 3 personas — Sam (scriptwriter) + Bea (storyboard artist)** — un-deferred in the brainstorm, lower urgency (Phase 3 is human-authored today).
7. **Ticketed follow-ons** (code-brain `vault/00_inbox/tickets.md` manual lane): the two Flo tickets (FLUX + Shakker sketch-LoRA; NB-Pro aspect-ratio), the Sage-tier bake-off, the `agy` transport cleanup, the `post_animatic` T3 gate (when Phase 4 lands), a scored T3 eval, the SF03 sean-anchor body-turnaround re-bake (bundled with the next heads-tall character authoring), and the Em view-correctness fix-rate improvement.

## Reading list (the necessary context files)
**Read first:** `CLAUDE.md`, `PHILOSOPHY.md`.
**The run + the orchestrator spec (the active work):** `docs/anima-test-runs/2026-06-11-first-integrated-run.md` (**the 16 seams + the "what a run orchestrator should absorb" synthesis — the heart of this session**), the two drivers `scripts/author_plan.py` + `scripts/spark_frame.py` (the prototype), `docs/2026-06-10-first-integrated-run-kickoff.md` (the run brief).
**The orchestration engine:** `pipeline/dag.py` (`class Runner`, `load_graph_from_manifest`, `run_from_legacy_cli`), the `phases:` block in `manifest.yaml` (currently only `enabled` — no graph authored), `pipeline/agents/__init__.py` (the AgentSpec / `register_node` contract).
**The nodes the orchestrator drives:** `pipeline/agents/planner.py` (Maya), `pipeline/agents/frame_router.py` (Flo), `pipeline/agents/vision_critic.py` (Em), `pipeline/agents/cost_estimator.py` (seam #5 lives here), `pipeline/agents/t3_council.py`, `scripts/build_museum.py` (Mo + T3 gate; seam #14).
**The piece (Engine Truth):** `runs/2026-06-11-spark-shared-first-integrated/export/SS_L1_loop.gif` + `SS_filmstrip_6.png` + `approved/SS_F03b_key.png` (the grin-as-peak).
**Architecture + ops:** `docs/pipeline-architecture-v1.md`, `docs/fleet-ops-protocol.md`, `docs/museum-exhibit-schema.md` (for seam #14).

## How to start this session
Confirm you've read `CLAUDE.md` + `PHILOSOPHY.md` + the field report; verify HEAD / divergence `0 0` / the md5 guard against the tree; glance at the shipped loop so you've seen the proof. Then tell Sean you're caught up, and open the orchestrator-scoping conversation by surfacing the four forks above with AskUserQuestion. Converge on a slice, then write the build plan + the first Claude Code kickoff. The 16 seams are your spec — don't re-derive them, build on them.
