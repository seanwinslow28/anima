# Continuation prompt — three operational incidents (auth billing, agy MCP overhead, orphaned agents)

*Paste everything below the divider into a fresh Cowork session opened on the anima project. This is an operational-remediation session, NOT a feature session — its job is to make the agent fleet safe to run again. Three incidents surfaced during the Em reference-images workstream; one of them (API-key billing) is actively costing money and gates everything else. Verify first, then research, then present a plan — do not execute account/environment changes or any costed run until Sean approves the plan.*

---

## Who you are and what this is

anima is a human-and-agent 2D animation pipeline (`/Users/seanwinslow/Code-Brain/anima` — read `CLAUDE.md` and `PHILOSOPHY.md` first). The current program is hardening the agent fleet so Act 2 can run end-to-end. The most recent workstream — giving Em (the T2 vision critic) reference images — **shipped its code successfully** (test-pinned, 264 tests green, case-7 flipped) but **deferred its costed live measurement**, and in the process surfaced three operational problems that must be fixed before any further live/costed agent runs. That is this session.

**This is a Cowork session, not Claude Code.** Do not spawn Claude Code agents or background executors that could outlive this session — uncontrolled agent lifecycle is literally incident #3 below. You may read files, run read-only bash to inspect processes/env/config, search the web, and write docs. Account re-authentication and shell/Keychain edits are Sean's to perform; your job is to diagnose precisely and hand him an exact, verified procedure.

## Read these first (in order)

1. [`docs/anima-test-runs/2026-06-02-em-reference-images-field-report.md`](anima-test-runs/2026-06-02-em-reference-images-field-report.md) — the workstream that surfaced all three incidents. Read "## The live measurement: why it's deferred (the harness saga)" (the three failed live attempts + the trilemma) and "## An incident worth recording" (the parallel-execution sighting) closely. The auth root-cause clue is in Attempt 3.
2. [`docs/anima-test-runs/2026-06-01-em-critic-spine-hardening-postmortem.md`](anima-test-runs/2026-06-01-em-critic-spine-hardening-postmortem.md) — "Failure 2 — a second agent was executing the same plan in the same tree." This is incident #1 recurring; the postmortem already drew the lesson (worktree isolation, resolve-your-own-PID-before-killing). Treat it as prior art, not new ground.
3. [`docs/research/2026-05-26-anti-gravity-cli-findings.md`](research/2026-05-26-anti-gravity-cli-findings.md) — what's already known about the `agy` (Antigravity CLI) binary, flags, and the 2026-06-18 sunset. The starting point for incident #2.
4. `CLAUDE.md` (anima) §"Anti-Gravity CLI Findings" + the auth notes; and `/Users/seanwinslow/Code-Brain/code-brain/CLAUDE.md` §"Agents SDK" — which states the **intended** auth model verbatim: *"Auth: `claude login` OAuth (no API key)."* The intent has always been subscription; somewhere the anima runs diverged from it.

## The three incidents — what happened, and the research/fix mandate for each

### Incident #1 (CRITICAL — money) — the Claude Agent SDK billed Sean's API key instead of his subscription

**What happened.** Sean received an email from Anthropic that his **API credits were suddenly exhausted**. The Em live runs should have billed his **Claude subscription** (Max/Pro via Claude Code OAuth), not the pay-as-you-go API. Every Opus/Sonnet escalation during the (repeated, failed) live attempts appears to have hit the API instead.

**The load-bearing clue (verify it).** The field report's Attempt 3 says detaching the workers *"broke Claude Code auth for the Opus-SDK `claude` child,"* and the design spec §12 said *"no `ANTHROPIC_API_KEY` (SDK uses Claude Code auth — keep it that way)."* **Leading hypothesis:** an `ANTHROPIC_API_KEY` was present in the environment the agents ran in — most likely the **worktree `.env` copy the agent created for the live run** (the field report notes it created a local `.env` secret-copy in the worktree, since removed) — and the **Claude Agent SDK / `anthropic` SDK prefers an API key over OAuth whenever the key is in the environment.** So OAuth subscription was available but silently overridden by API billing.

**Research + verify (this is the heart of the session):**
- Confirm the **current (2026) auth-precedence behavior** of the Claude Agent SDK (`claude-agent-sdk`, anima pins ~0.1.63) and the `claude` CLI it shells to: does a present `ANTHROPIC_API_KEY` override `claude login` OAuth subscription credentials? How do you **force subscription billing** for SDK/headless runs? Cite primary docs (docs.claude.com / docs.anthropic.com SDK + Claude Code auth pages, the SDK changelog/README). Verify against current docs — do not answer from memory; this has changed over time.
- **Audit where the key leaked in.** Read-only: grep every plausible source for `ANTHROPIC_API_KEY` — shell rc files (`~/.zshrc`/`~/.bashrc`/`~/.zprofile`), any `.env` in anima + the (now-removed) worktree + code-brain, launchd plists under `agents-sdk/schedules/`, and whether anything exports it from macOS Keychain. Determine the exact precedence path that led `invoke_opus_vision`/`invoke_sonnet_vision` (`pipeline/agents/sdk_runners.py`) to bill the API.
- **Produce the exact remediation procedure**, splitting agent-doable vs Sean-doable: remove `ANTHROPIC_API_KEY` from every environment the agents touch; confirm `claude login` / `claude setup-token` subscription auth is active; and a **positive verification test** — a single cheap SDK call whose billing you can confirm landed on the subscription, not the API (e.g. watch the API usage dashboard stay flat). The fix isn't done until that test passes.
- **Billing hygiene to flag to Sean:** check whether API **auto-reload** is enabled (if so, disable it so an accidental API run can't silently top up and bleed more), and where to watch API usage to confirm it's flat after the fix.

### Incident #2 (rate/latency) — `agy` reloads its MCP servers on every invocation

**What happened.** The Antigravity CLI (`agy`, Em's Gemini path) **loads its MCP servers every time it runs** (the cleanup transcript saw `agy`/session children spawning MCP servers — "Pencil, notebooklm"). That startup cost is paid per call, inflating latency and consuming usage/rate against the consumer-tier Gemini quota that the field report already flagged as a binding constraint (and contributed to the ~4× latency blowup: 199s/case). Sean wants MCP loading **disabled** for anima's `agy` critic calls — he believes there's a flag or config setting for it.

**Research + fix:**
- Find the **exact mechanism** to disable MCP-server loading for `agy` invocations — a CLI flag (e.g. an allowed-MCP-servers allowlist set to empty, an `--exclude`/no-extensions flag), a project/global settings file (`~/.gemini/settings.json` / Antigravity equivalent / a project `.gemini/`), or an env var. Cite the current Antigravity/Gemini-CLI docs (mind the `gemini`→`agy` rename and the 2026-06-18 sunset noted in the findings doc — verify against the version actually installed: `agy --version`, `agy --help`).
- anima only needs `agy` as a **headless single-image vision critic** — it needs *no* MCP servers at all. Recommend the cleanest way to run it MCP-free: per-invocation flag (preferred — surgical, in `cli_runners.run_antigravity_with_image`) vs. a config change (broader blast radius, affects Sean's interactive `agy` too). Note the tradeoff and let Sean choose.
- Quantify the expected win if the docs allow (startup time saved/call, quota pressure relieved) — this directly de-risks the deferred live re-baseline + bake-off.

### Incident #3 (corruption risk) — agents kept running and editing the branch after the session ended

**What happened.** After Sean's Claude Code session ended, **agents kept running** — an Anti-Gravity agent and other Claude agents continued working and editing the branch. The field report's "incident worth recording" + the cleanup transcript identify the culprit: **PID 22428, a parallel agent executing the *same plan* in the *main checkout*** (not the worktree), which had moved a branch onto another commit and left uncommitted edits to the same files. This is exactly the critic-spine postmortem's "Failure 2" recurring — two agents, one repo, silent-corruption hazard — except this time they **persisted past session end**.

**Verify + research + fix:**
- **First, verify the prior session's cleanup actually holds** (do not trust "all clean" given the circumstances). Read-only: are there any live `claude` / `agy` / `node` / `score.py` / `bakeoff` processes with anima in their cwd right now (`ps`, `lsof` by cwd)? Is git state on `main @ 79d36f2` clean and single-worktree as claimed? Is the preserved `stash@{0}` (22428's parallel bakeoff.py work) still there, and does Sean want it kept or dropped? **Resolve your own PID before suggesting any kill** (the postmortem's near-miss: one authorized kill of the wrong PID would have ended the session).
- **Research the lifecycle question:** *why do agent/background processes survive session end*, and how to prevent it — Claude Code background tasks vs detached subprocesses, process-group/session semantics (the field report's `start_new_session` detachment is directly entangled with this AND with incident #1's auth break — they're the same trilemma), and macOS specifics.
- **Produce a standing operational protocol** for the fleet (this should become a durable doc / CLAUDE.md pointer, not just advice): (a) **worktree isolation** for every plan execution (already adopted — formalize it); (b) a **pre-flight singleton check** ("am I the only agent in this repo?" — the postmortem already recommended this); (c) a **clean teardown checklist** at session end (no orphaned costed processes); (d) **costed runs have a single, known owner** and never run from a shared checkout. Tie each rule to the incident it prevents.

## The deliverable

A **detailed remediation plan**, presented to Sean before any execution, structured as:

1. **Verified diagnosis per incident** — what actually happened, confirmed against current state + primary docs (not the leading hypotheses restated; the *verified* root cause). Call out explicitly where a hypothesis was confirmed, corrected, or remains uncertain.
2. **The fix per incident** — exact steps, each tagged **[agent-can-do]** or **[Sean-must-do]** (account re-auth, shell/Keychain/`.env` edits, and any `claude login` step are Sean's). For incident #1, include the positive verification test that proves billing moved to the subscription.
3. **Immediate guardrails** — what to put in place *now* so this can't recur (the operational protocol from #3; auto-reload disabled; MCP-free agy; an env-hygiene check). Flag which are safe for you to apply this session (e.g. writing the protocol doc, a `.gitignore`/`.env.example` change) vs. which need Sean.
4. **The path back to the deferred work** — the Em live re-baseline + three-way bake-off are still pending (field report §"the deferred run"). State the gate plainly: **no costed live run resumes until incident #1 is fixed and the subscription-billing verification test passes**, agy is MCP-free (incident #2), and the singleton/worktree protocol is in place (incident #3). Then the deferred run proceeds per the field report's recipe (23 performs + 1 motion smoke, false-pass-first).

## Working discipline (non-negotiable)

- **Verify before asserting; cite primary sources.** The auth-precedence behavior and the agy MCP-disable mechanism are load-bearing and have changed over time — confirm against current docs.claude.com / Antigravity docs, not memory. Use `WebSearch`/web-fetch; the OpenRouter API (Perplexity or another research model) is available as a heavier fallback **only if** the official docs don't settle it.
- **Read-only until the plan is approved.** Inspect processes, env, config, git state — but do not kill processes, edit env/account settings, drop the stash, or run anything costed before Sean signs off. Account-touching steps are Sean's to execute.
- **No costed agent calls this session.** Diagnosis is free; the whole point is to stop the bleeding, not add to it. A single cheap subscription-verification call is the *only* permissible live call, and only after the env fix, with Sean's go-ahead.
- **STOP and present the plan** before executing any fix. This is an incident response — measure twice.
- Studio voice, clean markdown, honest about uncertainty. Update CHANGELOG; if the operational protocol warrants it, propose a CLAUDE.md pointer or a standing-ops doc (surface it, don't decide silently).

**The throughline:** the fleet's code is sound — the Em reference-images change shipped and works at n=1. What broke was the *operating environment*: API billing where subscription was intended, MCP overhead throttling the quota, and agents outliving their session to corrupt a shared tree. Fix the environment, prove the fix, and the deferred measurement can finally run safely. Stop the money leak first.
