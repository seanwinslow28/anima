# Cowork continuation prompt — Plan the last two agents: Sam (scriptwriter) + Bea (storyboard artist)

*Paste this whole block into a fresh Cowork session opened on the `anima` repo. It is the standing brief for the session.*

> **⚠ Updated 2026-06-15:** Sam/Bea planning is done (brainstorm + build plan + kickoff shipped) and the voice layer is now resolved — see [`2026-06-15-screenwriting-modes-integration-addendum.md`](2026-06-15-screenwriting-modes-integration-addendum.md). Where this brief says "Sam writes in Sean's register via `writing-voice-modes`," the dedicated **`screenwriting-modes`** skill now exists and Sam vendors its **full** instrument (`docs/2026-06-15-sam-bea-screenwriting-voice-context.md`), not a condensed note. The pairwise-preference eval framing (line ~46) is also enriched with binary ships-red anti-pattern cases per the addendum.

---

You're picking up a long-running build in **anima** — Sean's 2D animation pipeline made by a human + a fleet of named agents. The orchestrator (the connective tissue that runs the whole fleet as one resumable program) just shipped and was hardened. **The fleet is now complete except for two agents: Sam (Phase 3 scriptwriter) and Bea (Phase 3 storyboard artist).** Your job this session is to be a thinking partner and help Sean **brainstorm and plan the creation of Sam + Bea** — produce a brainstorm doc, a build plan (or plans), and a paste-ready Claude Code kickoff for the first build — so the fleet is fully fleshed out.

## How we work (standing doctrine — internalize this)

- **Cowork plans and reviews ($0, no model spend); Claude Code executes costed/multi-step builds under fleet-ops.** The rhythm: Cowork writes a dated plan doc + a paste-ready Claude Code kickoff → Sean runs it in Claude Code → Sean merges + pulls → Cowork verifies the result against the tree and plans the next step.
- **Verify against the tree, never trust a label — including reports, docstrings, and this prompt.** Use the `mcp__workspace__bash` shell to check git state, run/read real code, and confirm claims before asserting. Cautionary tales that earned this rule: a flag silently off measured nothing; a runbook claimed a loop "self-isolates" and the run crashed on case #0; a docstring lied about `agy -m`; Flo's CHANGELOG read "built" while nothing dispatched it; `--stub` silently spent real money via subscription OAuth that the `ANTHROPIC_API_KEY`-absent gate couldn't see (caught in Slice 2.1). Assert before you spend.
- **The verdict-baseline guard:** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` must stay `2af75906502f1caf8857e18828ceb2e4` — it's Em's eval baseline; all new work is additive and must never touch `evals/vision_critic/` without a deliberate, ratified re-baseline.
- **Use AskUserQuestion** to surface genuine scope/strategy forks before building. **Use TaskCreate/TaskUpdate** to track multi-step work. **Present files** with the present-files tool. Keep responses concise and direct (Sean's stated preference: give the "why," don't over-explain). Sean is a PM who digs into the "how" — respect that.
- **Fleet-ops for any costed run** (not this session — this is $0 planning): isolated git worktree off `origin/main`, single owner, §0 gates before spend, subscription billing where possible (`ANTHROPIC_API_KEY` absent so Opus bills the subscription), bounded API keys from `.env`, land via squash PR, clean teardown. Full protocol: `docs/fleet-ops-protocol.md`.

## Where the repo is right now

- Branch `main`, HEAD `742b629` (#51, Slice 2.1) — verify with `git log --oneline -5`; if Sean has done more by the time you read this, HEAD will be newer. Divergence `0 0`, clean.
- Recent landed PRs: #49 Slice 1 (cleanup), #50 Slice 2 (the orchestrator core), #51 Slice 2.1 (offline `--stub` + brief snapshot + the `ANIMA_FORCE_STUB` silent-spend gate).
- The pencil-test ("The Spark, Shared" — Act 1 shipped, the first integrated loop SHIPPED) is the first reference implementation, **not** the project's definition. anima itself is the 10-phase pipeline + the agent fleet.

## What just happened (the recent arc)

Over Slices 1 → 2 → 2.1, the **run orchestrator** was built and hardened: `python -m pipeline.run` is now a resumable stage machine (`PLAN → GENERATE → ASSEMBLE → DONE`) over a durable `runs/<id>/run_state.json`, exiting at every human gate, driving Maya → per-frame Flo→T1→Em (one Em pass per cast namespace, patch-staging via the DAG Runner's `post_run` hook) → assemble. `--stub` is now a fully-offline $0 smoke (walks to DONE with no key, force-stub-gated across all three model transports), and each run snapshots its brief so committed inputs are never clobbered. **Cowork-verified end-to-end 2026-06-12:** the `--stub` walk reaches DONE, the committed brief stays clean, suite is 576 green credential-free, Em baseline md5 intact.

**Two things are deliberately parked (ticketed in code-brain's Manual lane — do NOT pursue them this session):**
1. **The costed validation run is HELD** by Sean — the first real ~$0.66 end-to-end CLI run, to be run later from a plain terminal.
2. **A fleet-wide hardening/eval campaign is ticketed** — each agent needs more tests/evals/hardening to be rock-solid; sequenced to happen *after* the fleet is complete (i.e., after Sam + Bea land).

## The fleet state — built vs missing

**Built + proven** (registered nodes + personas): Maya (`planner`, Phase 0), Cy (`character_designer`, Phase 2), Flo (`flo`, Phase 5 routing) + the generators, Em (`vision_critic`, T2 — the only agent with a full scored eval baseline), Mo (`museum_writer`), the T3 council (`t3_council`), the Seedance motion node, the assemble/audit nodes, and now the **orchestrator**. The DAG runner engine (`pipeline/dag.py`) underpins it all.

**Missing — the only two left** (confirmed against the registered-node list + the eval handbook's canonical roster *Maya / Cy / Em / Mo / Flo / Sam / Bea / T3 / orchestrator*):
- **Sam — Phase 3 scriptwriter.**
- **Bea — Phase 3 storyboard artist.**

(Phase 4 Animatic is intentionally human-authored — Sean blocks motion in Procreate shapes; it has no agent by design. The `post_animatic` T3 gate stays a declared seam until Phase 4 tooling exists. So Sam + Bea genuinely complete the named-agent fleet.)

## THE ACTIVE WORK — brainstorm + plan Sam + Bea

These are **Phase 3 (Storyboard)** agents. The architecture is explicit and load-bearing (`docs/pipeline-architecture-v1.md` §Phase 3): *"Lock the beat sheet and shot list. **Mostly human-authored. Agents assist with prompt drafts and continuity checks; they don't pick beats.**"* Inputs: `plan.md` + Character Bible references. Outputs: a beat sheet + shot list + per-shot intent + camera notes (`docs/storyboard.md` or per-shot files; `pencil-test-storyboard.md` is the reference shape). **No critic checkpoint at phase exit — storyboard coherence is the human's responsibility.** This is the PHILOSOPHY's "human owns timing and taste" made structural: Sam and Bea **propose**, the human **decides**.

**The prior thinking already on disk** (read it — don't re-derive). The eval handbook's per-agent matrix (`docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md`) already scopes both:
- **Sam (scriptwriter, Opus)** — a *creative generator*. Failure modes: surface pastiche vs real stylistic-mechanism modeling, beat/structure failures, voice drift. Eval: few hand-labeled real script attempts, **pairwise preference** (this draft vs that), subjective → small set. Scoring: **pairwise win/lose/tie (Sean)** + structural checks (beat coverage). Judge: LLM-judge is *weak/secondary* for creative quality (self-preference risk) — lean on Sean's pairwise preference; LLM judge only for mechanical structure.
- **Bea (storyboard, Sonnet)** — a generator. Failure modes: script↔board conflict, shot-coverage gaps, composition errors. The **lowest-confidence assignment (65%) → a three-way bake-off candidate (Sonnet / Gemini / Codex)**. Scoring: coverage/consistency checks + **blind Sean preference + revision count**. Judge: mixed — deterministic coverage checks + human preference for composition.

**The beautiful structural payoff to surface in the brainstorm:** the orchestrator currently consumes a *human-authored* `shots.yaml` (the externalized frame list — `briefs/2026-06-10-spark-shared/shots.yaml`, schema in `pipeline/orchestration/shots.py`). **Sam + Bea close that loop:** Sam drafts the script/beat sheet from `plan.md`; Bea turns beats into the shot list + per-shot intent (+ optional draft panels); the human curates the result *into* `shots.yaml`. Today Sean writes that file from scratch — Sam + Bea would draft it for him to refine. Phase 0 (Maya) and Phase 5 (Flo/the orchestrator) already exist on both sides; Phase 3 is the missing middle.

## The genuine design tensions to brainstorm (use AskUserQuestion to converge with Sean)

These are the forks worth pressure-testing — don't pre-decide them:

1. **Own vs propose / the human gate.** Phase 3 is human-authored. What exactly do Sam and Bea *emit*, and where does the human sit? (Likely: they draft, the human curates — but what's the artifact contract and the gate shape? Mirror Maya's "propose → human approve" or looser?)
2. **The handoff chain.** Sam → Bea → `shots.yaml` → orchestrator. Does Sam emit a script + beat sheet, Bea consume beats → shot list + camera/intent, and the human curate into `shots.yaml`? Should Bea emit `shots.yaml` *directly* (as a draft) so the loop literally closes, or a richer storyboard the human distills?
3. **Does Bea generate visual panels or text?** The architecture's draft tier = "rough beat sketches (silhouettes)", pro tier = "full storyboard panels (composition + camera)". Does Bea *generate draft panels* (via the gemini pencil skill / a Flo-style route) or just structured text shot descriptions in v1? (Draft→pro escalation applies.)
4. **Build pattern + sequencing.** Reuse the Maya/Cy template (AgentSpec + `register_node` + a two-tier brief + CLI subcommands + `evals/{agent}/` cases + the propose-don't-decide contract)? Sam first (script→beats), then Bea (beats→board), or together? Sam is Opus, Bea is Sonnet + a bake-off candidate — does the bake-off happen during the build or after?
5. **Eval approach at build time.** The handbook says Sam = pairwise-Sean-preference + beat-coverage; Bea = coverage/consistency + blind-Sean-preference + revision-count, Bea a Sonnet/Gemini/Codex bake-off. How much eval scaffolding lands *with* the build vs in the later hardening campaign?

## Reading list (read before brainstorming — the necessary context)

Read first: **`PHILOSOPHY.md`** (the human-owns-taste thesis Phase 3 embodies), **`CLAUDE.md`** (fleet manual + the Skills Map showing every built agent's shape). Then:
- **`docs/pipeline-architecture-v1.md`** §Phase 3 STORYBOARD (+ §Phase 0 and §Phase 5 for the handoff neighbors) — the canonical phase spec.
- **`docs/research/2026-05-31-ai-evals-best-practices-and-anima-eval-strategy.md`** — the per-agent eval matrix (Sam + Bea rows) + the LLM-judge-for-creative-work caveats (lean on Sean's pairwise preference).
- **`docs/2026-05-26-maya-planner-brainstorm.md`** — the *template* for how a new agent gets brainstormed + scoped (two-tier brief, the AgentSpec, the cost-estimator, the adversarial pass, deferred-items-with-promotion-triggers). Sam/Bea should follow this shape.
- **`docs/pencil-test-storyboard.md`** — the reference shape for Phase 3 output (beats, shot list, frame counts).
- **The downstream consumer:** `pipeline/orchestration/shots.py` (the `shots.yaml` schema Sam/Bea draft toward) + `briefs/2026-06-10-spark-shared/shots.yaml` (a real example).
- **The build pattern (how an agent is coded):** `pipeline/agents/planner.py` (Maya) + `pipeline/agents/character_designer.py` (Cy) — the AgentSpec / `register_node` / three-pass / CLI-subcommand pattern; `scripts/author_bible.py` + `scripts/author_plan.py` as driver examples.
- For Sam's craft specifically, Sean's own voice tooling is relevant: the `writing-voice-modes` skill (in code-brain / the portfolio repo) — Sam writing in Sean's register, not generic-screenplay pastiche.

## Skills to use this session

Sean will likely invoke **`pm-product-discovery:brainstorm`** (or `superpowers:brainstorming`) to get the multi-perspective PM/Designer/Engineer headspace the fleet was planned in — honor it: generate breadth before converging, pressure-test every idea against *"is this anima's human-owns-taste thesis, or a generic AI-writes-the-movie shortcut?"*. **`sw-creative-toolkit:storytelling`** and **`sw-creative-toolkit:brainstorm`** are also apt for Sam's craft.

## Immediate first action

Confirm you've read `PHILOSOPHY.md` + `CLAUDE.md` + the Phase 3 spec + the eval-handbook Sam/Bea rows. Verify HEAD / divergence `0 0` / the md5 guard against the tree. Then tell Sean you're caught up, and open the **Sam + Bea brainstorm**: surface the five design tensions above with AskUserQuestion, converge on scope + sequencing, and produce (1) a brainstorm doc, (2) a build plan (Sam first is the likely call), and (3) the first paste-ready Claude Code kickoff — mirroring how Maya, Cy, and Flo were planned. Keep the costed run and the hardening campaign parked (ticketed); this session completes the fleet's design.
