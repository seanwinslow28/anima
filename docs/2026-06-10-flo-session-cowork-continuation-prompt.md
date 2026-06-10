# Cowork Continuation Prompt — anima / Flo (Phase 5 Generation Router)

*Paste this whole document into a fresh Cowork session. It catches you up on everything done so far, the files to read, what's left, and the active Flo plan. Date of handoff: 2026-06-10.*

---

You're picking up a long-running build in **anima** — Sean's 2D animation pipeline made by a human + a fleet of named agents. Your job this session is to help drive the **Flo (Phase 5 generation router)** build, and to be a thinking partner on next steps. **Read `CLAUDE.md` and `PHILOSOPHY.md` first** (the project manual + the load-bearing intent), then the Flo files below.

## How we work (standing doctrine — internalize this)
- **Cowork plans and reviews ($0, no model spend); Claude Code executes costed/multi-step builds under fleet-ops.** The rhythm is: Cowork writes a dated plan doc + a paste-ready Claude Code kickoff → Sean runs it in Claude Code → Sean merges → Cowork verifies the result against the tree and plans the next step.
- **Verify against the tree, never trust a label — including reports, docstrings, and this prompt.** Use the `mcp__workspace__bash` shell to check git state, run tests, and read real code before asserting anything. Cautionary tales that earned this rule: a flag silently off measured nothing (2026-06-07); a runbook claimed a loop "self-isolates" and the run crashed on case #0 (Gate-3 v1); the T3 smoke caught a docstring lying about `agy -m`; Codie's live check caught a variadic `-i/--image` ordering bug. Assert before you spend.
- **The verdict-baseline guard:** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` must stay **`2af75906502f1caf8857e18828ceb2e4`** — it's Em's eval baseline; all new work is additive and must never touch `evals/vision_critic/`.
- **Use AskUserQuestion to surface genuine scope/strategy forks before building.** Use TaskCreate/TaskUpdate to track multi-step work. Present files with the present-files tool. Keep responses concise and direct (Sean's stated preference); give the "why," don't over-explain.
- **Fleet-ops for any costed run:** isolated git worktree off `origin/main`, single owner, §0 gates before spend, subscription billing where possible (`ANTHROPIC_API_KEY` absent so Opus bills the Claude subscription), bounded API keys from `.env`, land via squash PR, clean teardown. Full protocol: `docs/fleet-ops-protocol.md`.

## Where the repo is right now
- Branch `main`, HEAD **`ac95869`** (PR #42), clean, divergence `0 0` with origin. (If Sean has run Flo-A by the time you read this, HEAD will be newer — verify with `git log`.)
- The pencil-test (Act 1 shipped, Act 2 ready-to-execute) is the **first reference implementation**, not the project's definition. anima itself is the 10-phase pipeline + the agent fleet.

## What's been accomplished (the recent arc)
1. **Em (T2 vision critic) eval suite — COMPLETE.** All three axes measured + ratified: verdict (precision 0.97 / recall 1.00 / false_pass 0.00), citation (cites-correct 0.97), constructive fix-rate (normalized lift 0.667). Plus the **Gate-2 golden-agreement judge calibrated** (κ 0.885 / FPR 0.067, PASS iteration 1 — PR #40), so Em's fix-rate is now trackable between costed runs for pennies. Em is the **reference template for how a fleet agent gets fully evaluated.** Field report: `docs/anima-test-runs/2026-06-10-em-gate2-judge-calibration.md`.
2. **T3 council — BUILT + live-validated.** Three heterogeneous peers — **Codie** (production, `codex exec`/ChatGPT Plus), **Annie** (visual+identity, Gemini API `gemini-3.5-flash`, NOT agy), **Sage** (narrative, Opus via Claude SDK) — fan out in parallel; a **separate Opus chairman** (Pattern C) adjudicates. Wired as the **`pre_museum` publish gate** (`pipeline/museum/t3_gate.py`, `build_museum.py --t3-gate`): a chairman `fail` blocks `--render`, `borderline` proceeds, patches stage (`auto_apply: false`). PR #41 (Session A engine, $0 stub) + PR #42 (Session B config + gate + **live 3-vendor smoke**). Live smoke proved all three vendors fire live, the chairman synthesizes real dissent, 19 patches staged, gate blocks correctly. Trace: `docs/anima-test-runs/2026-06-10-t3-council-live-smoke.md`. **The critic stack (T1/T2/T3) is now complete.**

## The fleet state (built vs missing)
**Built:** Maya (Phase 0 planner, Opus), Cy (Phase 2 character designer — sean-anchor + claude-mascot Bibles locked), Em (T2 critic, fully evaluated), Mo (museum writer), the T3 council, the orchestrator/DAG runner, the T1 rule gates (incl. the SF03 proportion gate).
**Missing:** **Flo (Phase 5 generation router — THIS SESSION'S WORK)**, Sam + Bea (Phase 3 scriptwriter + storyboard artist). The **Animatic phase (Phase 4)** doesn't exist yet, so the `post_animatic` T3 gate is a declared seam. The **museum Astro export** into the portfolio is deferred (Sean: hold until the pipeline produces more content).

---

## THE ACTIVE WORK: Flo (Phase 5 Generation Router)

**What Flo is:** the router that picks the right image generator per shot instead of the current single-model path. Today `pipeline/nodes/frame_generate.py` always uses one model (NB2) at a fixed cost. Flo routes hero keyframes → the best model, in-betweens → the cheapest model that holds the pencil aesthetic, and feeds Maya an accurate Phase 0 cost preview.

**Scope — LOCKED (Sean, 2026-06-10):**
1. **Build the router skeleton now ($0, stub-green)** wiring the already-available generators; declare the rest as seams.
2. **In-between tier: pilot fal.ai APIs (Seedream 4.0 / Qwen-Image-Edit) next; if they can't hold the pencil grain, pivot to NB2.** No self-hosted FLUX / no 24GB-rig dependency this round.

**Two sessions (mirrors the T3 rhythm):**
- **Flo-A — the $0 router skeleton. KICKOFF IS WRITTEN + PASTE-READY → `docs/2026-06-10-flo-router-session-a-kickoff.md`.** Builds: the `generation.routing:` manifest block; `pipeline/agents/frame_router.py` + a `FloNode` (`@register_node("flo")`) routing hero→NB Pro / standard→NB2 (both already wired) with the in-between/edit tiers as honest `declared` seams; draft→pro escalation; the `cost_estimator._phase_5_cost` extension; back-compat so the legacy pencil-test path is untouched; tests. **No installs or prep needed — Sean can paste this straight into Claude Code whenever.**
- **Flo-B — the costed fal.ai pencil-preservation pilot (teed up, not yet a kickoff).** Build a 20–50-pair before/after benchmark from Sean's approved pencil archive; run Seedream/Qwen (fal.ai) vs NB2/NB Pro through identical in-between prompts; score grain / identity / instruction-follow (Sean's eye is ground truth); wire the winner as the `in_between_*` route, or pivot to NB2 if both slick the pencil. Doubles as portfolio evidence ("how I evaluated and chose the generation stack"). **Needs `FAL_KEY` (already have it from Seedance) + the folder of ~20–50 pencil before/after pairs.**

**Key grounding facts (already verified against the tree):**
- **NB Pro** (hero, `pipeline/agents/nb_pro_runner.py`) and **NB2** (standard, `pipeline/agents/gemini_api_runner.py`) are already wired — keyframe routing is assembly, not new transports.
- **`cost_estimator._phase_5_cost` already reads `generation.routing.{hero,standard}_keyframe.usd_per_frame`** — Maya's cost preview is half-wired waiting for Flo's block.
- **The integration point** is `pipeline/nodes/frame_generate.py` (wraps the legacy `generate_frame()` in `pipeline/generate.py`).
- **The in-between tier is the real value + the real hard problem** — Seedream/Qwen cut in-between cost ~80%, but the Image-Model-DR SYNTHESIS flags **zero documented pencil/non-photoreal testing**, so it's pilot-gated (hence Flo-B).
- One default I (the prior session) chose without asking: Flo derives the route from an explicit `shot_type` field on each frame spec (default `standard_keyframe`, hero opt-in). If Sean's frame specs carry a better tier signal, refine in Flo-A step A2.

**Full plan:** `docs/2026-06-10-flo-router-build-plan.md`.

**Immediate next action:** if Sean hasn't run Flo-A yet, the move is to hand him the Flo-A kickoff for Claude Code (it's $0, no prep). When Flo-A lands and merges, verify it against the tree (md5 guard, tests, the routing block + FloNode), then write the **Flo-B kickoff** (the costed pilot).

---

## Reading list (the necessary context files)
**Read first:** `CLAUDE.md`, `PHILOSOPHY.md`.
**Flo (the active work):** `docs/2026-06-10-flo-router-build-plan.md`, `docs/2026-06-10-flo-router-session-a-kickoff.md`, `docs/2026-05-26-agent-fleet-brainstorm-v2.md` §4, `docs/Image-Model-DR-2026/SYNTHESIS.md` §2.
**Flo code seams:** `pipeline/nodes/frame_generate.py`, `pipeline/generate.py`, `pipeline/agents/nb_pro_runner.py`, `pipeline/agents/gemini_api_runner.py`, `pipeline/agents/cost_estimator.py`, `pipeline/agents/__init__.py` (AgentSpec), and the `generation:` / `tiering:` / `characters:` blocks in `manifest.yaml`.
**Architecture + ops:** `docs/pipeline-architecture-v1.md`, `docs/fleet-ops-protocol.md`.
**Recent context (the just-finished T3 arc):** `docs/2026-06-10-t3-council-build-plan.md`, `docs/2026-06-10-t3-council-session-a-kickoff.md`, `docs/2026-06-10-t3-council-session-b-kickoff.md`, `docs/anima-test-runs/2026-06-10-t3-council-live-smoke.md`. The T3 council row in `CLAUDE.md`'s Skills Map carries the state-of-record.
**The completed Em arc (the eval template):** `docs/anima-test-runs/2026-06-10-em-gate2-judge-calibration.md` + the Em row in `CLAUDE.md`.

## What's still on the list (backlog, roughly prioritized)
1. **Flo-A → Flo-B** (active — the in-between pilot is the payoff).
2. **The first integrated end-to-end run** — the brainstorm's sanctioned post-commit-9 move: have Maya plan a small scoped piece at Phase 0 → human gate → run it through the fleet (Cy Bibles → Flo generate → Em/T3 critics → assemble → museum). Produces the content that unblocks the museum. This is the natural move once Flo is built.
3. **The museum Astro export** into `sw-ai-pm-portfolio` — after the end-to-end run produces real content (the job-hunt portfolio payoff).
4. **Phase 3 personas — Sam (scriptwriter) + Bea (storyboard artist)** — un-deferred in the brainstorm but lower urgency (Phase 3 is human-authored today).
5. **Ticketed follow-ons** (filed in code-brain's `vault/00_inbox/tickets.md` manual lane): the **Sage-tier bake-off** (Open Q2 — Opus-Sage vs Sonnet-Sage), the **agy transport cleanup** (`run_antigravity_with_image`'s `-m` exit-2 dead-code bug — no critic uses agy anymore), the **`post_animatic` T3 gate** (wire when Phase 4 lands), and a **scored T3 eval** (the council's content trustworthiness isn't yet measured — the live smoke surfaced one confident Annie misfire on a stale style-register signal; patches stage-not-apply keeps it safe meanwhile).

## How to start this session
Confirm you've read `CLAUDE.md` + the Flo plan + the Flo-A kickoff, verify HEAD/divergence/md5 against the tree, then tell Sean you're caught up and either (a) hand him the Flo-A kickoff if it hasn't run, or (b) verify + plan Flo-B if it has. Don't re-plan what's already planned — the Flo-A kickoff is done and paste-ready.
