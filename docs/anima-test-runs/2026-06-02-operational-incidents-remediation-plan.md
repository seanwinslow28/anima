# Operational incidents — remediation plan (2026-06-02)

**Status:** DRAFT for Sean's approval. Read-only diagnosis complete; **no fix executed, nothing costed run.**
**Scope:** The three operational incidents the Em reference-images workstream surfaced ([field report](2026-06-02-em-reference-images-field-report.md) · [critic-spine postmortem](2026-06-01-em-critic-spine-hardening-postmortem.md)). The fleet's *code* is sound (Em's reference-images change shipped, 264 green, n=1 live-proven). What broke is the **operating environment**: API billing where subscription was intended, MCP overhead on every `agy` call, and agents outliving their session in a shared tree.

A note on what I could and couldn't inspect: my shell sandbox sees only the four mounted repos — it **cannot** see your macOS processes, `~/.zshrc`/`~/.zprofile`, `~/.gemini/`, or the Keychain. So the in-repo evidence below is verified first-hand; anything in your home dir or live process table is tagged **[Sean-must-verify]**.

---

## Incident #1 (CRITICAL — money): the SDK billed the API key, not the subscription

### Verified diagnosis

**Confirmed — the precedence rule (primary docs).** Claude Code's [authentication doc](https://code.claude.com/docs/en/authentication) gives the exact order. When multiple credentials are present Claude Code picks, in order: (1) cloud-provider creds → (2) `ANTHROPIC_AUTH_TOKEN` → (3) **`ANTHROPIC_API_KEY`** → (4) `apiKeyHelper` → (5) `CLAUDE_CODE_OAUTH_TOKEN` → (6) subscription OAuth from `/login`. The decisive line for headless runs: *"In non-interactive mode (`-p`), the key is always used when present."* And explicitly: *"If you have an active Claude subscription but also have `ANTHROPIC_API_KEY` set in your environment, the API key takes precedence once approved. Run `unset ANTHROPIC_API_KEY` to fall back to your subscription, and check `/status`."* So the design-spec §12 instinct ("no `ANTHROPIC_API_KEY` — SDK uses Claude Code auth, keep it that way") was exactly right, and the leak is a textbook instance of it.

**Confirmed — the code path that bills.** anima's venv has `claude_agent_sdk 0.2.87` **and** `anthropic 0.105.2` installed. `pipeline/agents/sdk_runners.py` takes **Path 1** (claude-agent-sdk → the `claude` CLI subprocess) since the CLI is installed; it only falls through to the raw `anthropic` SDK on `CLINotFoundError`. Either path bills the API when `ANTHROPIC_API_KEY` is in the environment: Path 1 because the `claude` CLI obeys the precedence above in non-interactive mode; Path 2 because `anthropic.AsyncAnthropic()` reads `ANTHROPIC_API_KEY` by default. Every Opus/Sonnet escalation in the repeated live attempts went through this.

**Corrected — where the key came from.** The leading hypothesis was the worktree `.env` secret-copy. The evidence narrows it: **anima's `.env` has NO `ANTHROPIC_API_KEY`** (verified — it carries `GEMINI_API_KEY`, `FAL_KEY`, `OPENAI_API_KEY`, `OPENROUTER_API_KEY`, plus two scraper keys, and nothing Anthropic). `evals/vision_critic/score.py` calls bare `load_dotenv()` (no path, `override=False`), which can only *add* a key from a found `.env`, and anima's doesn't have one to add — and a copy of it wouldn't either. So the key did **not** enter through anima's repo. It was **already exported in the shell environment** when the live runs fired. The most likely source — note `code-brain/.env` **does** carry `ANTHROPIC_API_KEY`, so a shell that had that exported (login profile, a sourced `.env`, or a code-brain tool that exports it) carries the key into any `cd anima && python -m evals...` run. **This is the one piece I can't confirm from the sandbox — it lives in your shell, not the repo.**

> **Uncertain until [Sean-must-verify]:** which of (`~/.zshrc` / `~/.zprofile` / `~/.bashrc` export · a sourced `code-brain/.env` · a Keychain-backed export · a wrapper script) put `ANTHROPIC_API_KEY` into the live-run shell. The fix is the same regardless, but knowing the source prevents recurrence.

### The fix

**[Sean-must-verify] — find the leak source (read-only, ~2 min).**
```bash
echo "${ANTHROPIC_API_KEY:+SET (leak present)}${ANTHROPIC_API_KEY:-unset (good)}"
grep -RnE 'ANTHROPIC_API_KEY' ~/.zshrc ~/.zprofile ~/.bashrc ~/.profile ~/.zshenv 2>/dev/null
# Does any tool source code-brain/.env into the interactive shell?
grep -RnE 'code-brain/.env|set -a' ~/.zshrc ~/.zprofile 2>/dev/null
```

**[Sean-must-do] — stop the bleed, restore subscription billing.**
```bash
# 1. Remove the export from wherever step-1 found it (edit the rc file), then in THIS shell:
unset ANTHROPIC_API_KEY
# 2. Re-auth on the subscription only — decline any Console/API credential if prompted:
claude logout && claude login        # choose your Pro/Max account
# 3. Confirm the active route:
claude /status                        # should show subscription, NOT an API key
```

**[Sean-must-do] — headless/costed runs the durable way.** For background/SDK runs where there's no interactive login, the doc's sanctioned subscription path is a long-lived OAuth token (precedence slot #5), **not** an API key:
```bash
claude setup-token                    # prints a 1-yr token; requires Pro/Max/Team/Enterprise
export CLAUDE_CODE_OAUTH_TOKEN=...    # set this for the deferred Em run's shell
```
Because `ANTHROPIC_API_KEY` (slot #3) beats `CLAUDE_CODE_OAUTH_TOKEN` (slot #5), **the key must be absent for the token to win.** Both conditions, not one.

**[agent-can-do, after approval] — positive verification test (the fix isn't done until this passes).**
1. Open the API usage dashboard at console.anthropic.com → Usage; note the current spend and timestamp.
2. Fire one cheap, real subscription call from the fixed shell — the smallest possible:
   ```bash
   cd <anima> && .venv/bin/python -c "import asyncio; from pipeline.agents.sdk_runners import invoke_sonnet_text; \
     print(asyncio.run(invoke_sonnet_text(prompt='Reply with the single word: OK')).text)"
   ```
   (Sonnet text, no images — the cheapest path that still exercises the real `claude-agent-sdk` → `claude` CLI route.)
3. **Pass = the API dashboard spend does NOT move** (stays flat 5–10 min after the call) **and** `claude /status` shows subscription. If the dashboard ticks up, the key is still winning — stop and re-check step-1.

### Billing hygiene to flag

- **[Sean-must-do] Disable API auto-reload.** console.anthropic.com → Billing → turn off auto-reload/auto-recharge, so an accidental API run can't silently top up and bleed further. (This is what produced the "credits exhausted" email.)
- **[Sean-must-verify] Watch the dashboard stays flat** for a day after the fix to confirm nothing else on the machine is quietly billing the API.
- **[Sean-aware] Calendar note — the rules change June 15, 2026 (13 days).** Per the same doc: *"Starting June 15, 2026, Agent SDK and `claude -p` usage on subscription plans will draw from a new monthly Agent SDK credit, separate from your interactive usage limits."* So even a correctly-subscription-billed Em run, if it lands after the 15th, draws on that new SDK-credit bucket rather than your interactive limits. Worth knowing before the deferred 24-case run.

### Result — Incident #1 CLEARED (2026-06-02)

> Subscription billing restored and **proven** in a sole-agent session. The `[agent-can-do]` positive verification test passed; the `[Sean-must-verify]`/`[Sean-must-do]` env items were confirmed clean. (Already-verified before this session, not re-done: shell rc files, macOS Keychain — OAuth only, `~/.claude.json`, direnv.)

- **Two unchecked hiding spots — clean.** Parent `~/Code-Brain/.env` doesn't exist (no `load_dotenv` walk-up vector); launchd `ANTHROPIC_API_KEY` unset (`launchctl getenv` empty — nothing inherited by GUI-launched apps). Bonus: `~/.claude/settings.json` carries no `apiKeyHelper` (precedence slot #4) and no env-injection block.
- **The known on-disk copy was already gone.** `code-brain/.env` had **0** `ANTHROPIC_API_KEY` lines / 0 `sk-ant` signatures (file mtime 09:20 EDT — removed earlier in the day; the diagnosis above reflects an earlier state). `config.py:127` reads the key as optional (`os.environ.get(...) or None`); the `agents-sdk` suite ran **845 passed / 5 failed**, all 5 unrelated to Anthropic (Gemini cost-math, a missing `python-dotenv` in a bare-`python3` subprocess from the relocated venv, HDBSCAN fallback) — `test_config.py` green.
- **Env clean across interactive + non-interactive shells:** current shell, `zsh -c`, full-login `zsh -lic`, and Python `os.environ` all read clean/`None` (the leak was headless — this is the load-bearing check).
- **Active route:** `claude auth status` → `authMethod: claude.ai`, `subscriptionType: max` (not an API key).
- **Positive billing test PASSED:** real Sonnet call via `sdk_runners.invoke_sonnet_text` fired 09:55:47 EDT → returned `OK`; console.anthropic.com → Usage stayed **flat** over the recheck window → the call billed the **Max subscription, not the API**.

**Net:** `ANTHROPIC_API_KEY` is absent everywhere checkable on this machine and the subscription is the live billing route. **Gate condition #1 for the deferred Em re-baseline is satisfied** (#2 MCP-free agy and #3 singleton/worktree protocol still pending). Standing hygiene unchanged: keep API auto-reload disabled; mind the 2026-06-15 SDK-credit change.

---

## Incident #2 (rate/latency): `agy` reloads MCP servers on every invocation

### Verified diagnosis

**Confirmed — agy auto-loads its configured MCP servers per run.** MCP servers live in the **shared** `~/.gemini/config/mcp_config.json` (`mcpServers` object), consumed by *all* Antigravity surfaces — agy CLI, the IDE, and Antigravity 2.0 ([Google Cloud Community config guide](https://medium.com/google-cloud/configuring-mcp-servers-and-skills-for-antigravity-cli-and-ide-a938c7eebb78)). anima's wrapper (`cli_runners.run_antigravity_with_image`) invokes `agy --dangerously-skip-permissions --add-dir <parent> -p <prompt>` with **no MCP-control flag**, so agy spins up every enabled server (the "Pencil, notebooklm" spawns the cleanup transcript saw) on each call. anima's vision-critic path needs **zero** MCP servers.

**Corrected — what it actually costs.** The hypothesis was that MCP loading "consumes usage/rate against the Gemini quota." More precisely: spawning stdio MCP servers (`uvx`/`npx` child processes) is **local startup latency and process contention**, not Gemini *token* quota — a headless `agy -p` vision critique shouldn't call those tools, so it burns no model quota on them. The real costs are (a) seconds of cold-start per call, and (b) extra local subprocesses contending with the asyncio child-watcher — the same contention the postmortem's Failure-1 (no-traceback exit) traces to. So disabling MCP **de-risks the latency/stability** of the deferred re-baseline; it does not, by itself, relieve the *Gemini quota* pressure (that's the consumer-tier limit, addressed by spacing calls / the `RateCapExhausted` guard already shipped).

**Uncertain — no per-invocation disable flag is documented.** I could not find a documented `agy` flag to disable MCP for a single call (no confirmed `--allowed-mcp-server-names`, `--no-mcp`, or `--extensions none` on the current `agy`; the published flag surface is `-p`, `--output-format`, `-m`, `--add-dir`, `--dangerously-skip-permissions`, plus `agy inspect` and the `/mcp` slash command). Config is file-based. (Corroborating the plumbing risk: a community project exists *solely* to work around agy's headless `-p` empty-stdout bug by reading agy's transcript files — the same bug anima's `RateCapExhausted` guard now catches.)

### The fix — two options, Sean chooses the blast radius

**Option A (surgical, anima-only) — point anima's `agy` at an isolated, MCP-free config. [agent-can-do, pending one verification].**
The certain, low-blast-radius shape: give the wrapper its own config dir containing an empty `mcpServers`, so only anima's calls are MCP-free and your interactive `agy`/IDE keep their servers. This needs one fact I can't get from the sandbox — whether `agy` honors a config-dir override (env var or flag):
- **[Sean-must-verify]** `agy --help` and `agy mcp --help` — look for `--config` / `--mcp-config` / a config-dir flag or a `GEMINI_*`/`ANTIGRAVITY_*` config-dir env var.
- If one exists → [agent-can-do] I add it to `run_antigravity_with_image`, pointing at a committed `pipeline/agents/agy-config/mcp_config.json` with `{"mcpServers": {}}`. Surgical, version-controlled, no effect on your interactive setup.

**Option B (certain, broader) — disable the unneeded servers in the shared config. [Sean-must-do].**
In `~/.gemini/config/mcp_config.json`, add `"disabled": true` to the servers anima doesn't need (this is a documented per-server field). **Tradeoff:** the file is shared across agy CLI + IDE + Antigravity 2.0, so disabling there also removes those servers from your interactive sessions. Fine if you don't use Pencil/notebooklm interactively; otherwise prefer A.

**Recommendation:** try A first (verify the flag), fall back to B. Either way, confirm with `agy inspect` (lists connected MCP servers) that anima's path shows none. **Expected win:** removes the per-call MCP cold-start and the extra child-process contention — a stability/latency improvement that directly de-risks the long deferred run; I'll quantify the seconds-saved against a before/after `agy inspect` + timed call once we pick the option.

### Result — Incident #2 CLEARED (2026-06-02)

> Resolved by **emptying the MCP config**, not the time-scoped toggle — Sean confirmed he doesn't use MCP in Antigravity at all, so a permanent wipe is cleaner than per-run disable.

- **Corrections to the diagnosis above (verified on Sean's v1.0.2):** (a) `agy --help` has **no** per-invocation config/MCP flag and **no** `agy inspect`/`/mcp` subcommand — the management surface is `agy plugin` (`list`/`enable`/`disable`); Option A (isolated config-dir) is therefore unreachable. (b) The servers were configured in **`~/.gemini/settings.json`** under `mcpServers`, not a separate `mcp_config.json`. (c) `agy plugin list` was empty — the spawns came from the config block, not plugins.
- **The fix:** `~/.gemini/settings.json` `mcpServers` → `{}` (removed `notebooklm-mcp` + `pencil`); all other keys (`ui`, `security.auth: oauth-personal`, `general`, `ide`) untouched; JSON re-validated; backup at `~/.gemini/settings.json.bak.1780411432` (rollback: `cp` it back).
- **Verified MCP-free:** `agy -p "Reply OK"` exited 0 on Google OAuth and spawned **zero** MCP children — process set byte-identical across 17 live samples, no orphans. The notebooklm/pencil/obsidian processes a `ps` grep catches are pre-existing and parented by **Claude.app / Claude Code inside the Antigravity IDE**, not `agy`.
- **Note (out of scope, optional):** those servers still load in Claude Code, which keeps its **own** MCP config separate from `~/.gemini/`. Irrelevant to the anima gate (Em reaches Gemini via `agy`, not Claude Code MCP); clean it only if the IDE startup cost bothers you.

**Net: gate condition #2 is satisfied** — anima's `agy` path loads no MCP servers; the latency/contention nuisance is gone permanently.

---

## Incident #3 (corruption risk): agents kept running and editing the branch after session end

### Verified diagnosis

**Confirmed — current state is clean (in-repo).** Verified first-hand in the mounted repo: `git status` clean on `main @ 79d36f2`; **single worktree** (the feature worktree was removed and merged via PR #13); only untracked file is the continuation prompt. The `feature/em-reference-images` branch is gone locally (merged). `stash@{0}` is present and labeled: *"22428 parallel em-reference-images work (auto-stashed during 2026-06-02 cleanup … incl. bakeoff.py --segment additions)."* So the prior cleanup's git outcome holds.

**[Sean-must-verify] — the live-process check I cannot do.** My sandbox is a separate Linux box; it cannot see your macOS process table. Before any costed run, confirm nothing is still executing in the tree:
```bash
ps aux | grep -E 'claude|agy|score\.py|bakeoff|node' | grep -v grep
lsof -d cwd 2>/dev/null | grep -i Code-Brain/anima
# Resolve YOUR shell's claude ancestor FIRST so you never kill your own session:
P=$$; while [ "$P" -gt 1 ]; do echo "$P $(ps -o comm= -p $P)"; P=$(ps -o ppid= -p $P | tr -d ' '); done
```
(The postmortem's near-miss: the most-suspicious PID was the session's own ancestor. Resolve own PID up the `ppid` chain before killing anything.)

**[Sean's call] — the preserved stash.** `stash@{0}` is 22428's parallel `bakeoff.py --segment` work. The `--segment` capability is already on `main` (it's how the deferred run is invoked), so the stash is most likely redundant. Recommend: skim `git stash show -p stash@{0}`, then `git stash drop` unless it carries something not already merged. Your decision — I won't touch it.

**Confirmed — why processes survived session end (research).** A child started with `start_new_session=True` (Python's `setsid`) becomes a new session/process-group leader, detached from the controlling terminal — so it does **not** receive the `SIGHUP` that tears down the session, and it keeps running after the parent/session exits ([Python subprocess detach](https://bugs.python.org/issue27068)). This is the same mechanism the field report used deliberately to keep the *orchestrator* alive across teardown crashes — and the same mechanism that, applied to a costed worker (or any agent spawned detached), lets it outlive the session and keep editing the tree. The trilemma in the field report is real: workers must keep the session for Claude Code auth, but a shared session couples their teardown signals to the parents. The resolution there — detach only the orchestrator, never the workers — is correct; the operational gap is that *nothing enforced single-owner / clean-teardown*, so a second detached executor in the main checkout could (and did, transiently) appear.

### The fix — a standing operational protocol

Proposed as a durable doc (`docs/fleet-ops-protocol.md`) with a pointer from anima's `CLAUDE.md`. Each rule is tied to the incident it prevents:

1. **Worktree isolation for every plan execution.** All costed/multi-step plan work runs in a dedicated `git worktree` off a branch — never the main checkout. *(Prevents: two writers on one HEAD — postmortem Failure 2, field-report incident.)* Already adopted ad hoc; this formalizes it.
2. **Singleton pre-flight.** Before any costed run, confirm you're the only agent in the repo (`ps`/`lsof` by cwd above) and resolve your own PID up the `ppid` chain before killing anything. *(Prevents: the authorized-kill-of-wrong-PID near-miss.)*
3. **Clean teardown checklist at session end.** No orphaned costed processes: list `agy`/`claude`/`score.py`/`bakeoff` by cwd, terminate any that aren't your session, confirm zero before closing. Don't `start_new_session` a *costed* worker — keep it a child of the session so teardown reaps it. *(Prevents: agents outliving the session — this incident.)*
4. **Single known owner for costed runs.** A costed run has one launching shell, one branch/worktree, one owner. No parallel executor in a shared checkout. *(Prevents: the duplicate `--segment` `score.py` sighting.)*

**[agent-can-do, after approval]** I'll write `docs/fleet-ops-protocol.md`, add the CLAUDE.md pointer, and append a CHANGELOG entry. This is documentation, not an env/account change — safe for me once you approve the content.

---

## Immediate guardrails — what to put in place now

| Guardrail | Prevents | Who |
|---|---|---|
| `unset ANTHROPIC_API_KEY` + remove the export from shell rc; re-auth subscription; `claude setup-token` for headless | #1 recurrence | **[Sean-must-do]** |
| Disable API auto-reload at console.anthropic.com | runaway API spend | **[Sean-must-do]** |
| `.env.example` + a one-line `.gitignore`/README note: anima agents use Claude Code subscription auth — **never** set `ANTHROPIC_API_KEY` in an anima shell | #1 recurrence | **[agent-can-do]** |
| Env-hygiene assert in the costed entrypoint: `score.py` refuses to start if `ANTHROPIC_API_KEY` is set (fail-fast, with an `--allow-api-key` override) | #1 recurrence — makes the leak impossible to run past | **[agent-can-do]** |
| MCP-free agy (Option A or B) + verify with `agy inspect` | #2 latency/contention | **A: [agent-can-do] after verify · B: [Sean]** |
| `docs/fleet-ops-protocol.md` + CLAUDE.md pointer + CHANGELOG | #3 recurrence | **[agent-can-do]** |

The two `[agent-can-do]` code guardrails (the `.env.example` note and the `score.py` fail-fast assert) are the highest-leverage things I can safely apply this session — they make incident #1 *structurally* hard to repeat. I'll do them only on your go-ahead.

---

## The path back to the deferred work

The deferred Em live re-baseline + three-way bake-off (field report §"the deferred run": **23 performs cases + 1 motion smoke = 24**, false-pass-first) stays **gated**. It does not resume until all three are true:

1. ✅ **#1 fixed and the positive billing test passed** — `ANTHROPIC_API_KEY` absent, Max subscription active, real call left the API dashboard flat (2026-06-02).
2. ✅ **agy is MCP-free** — `~/.gemini/settings.json` `mcpServers` emptied; zero MCP children across 17 samples (2026-06-02).
3. **The singleton/worktree protocol is in place** — run from an isolated worktree, sole-agent confirmed, clean-teardown checklist ready. *(Doc shipped; two run-time loose ends remain: the live-process sweep and the `stash@{0}` keep/drop call.)*

Then the run proceeds per the field report's recipe (orchestrator-detached, workers session-attached; smoke `--limit 2` first), holding the §9 disciplines: recall ≥ 1.00 and false-pass = 0.00 before precision, labels stay locked. **And mind the June 15 SDK-credit change** if the run lands after that date.

**Stop the money leak first (#1). Then #2 and #3. Then measure.**
