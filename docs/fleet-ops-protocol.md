# Fleet operations protocol

**Status:** Standing operating discipline for anima's agent fleet. Adopted 2026-06-02 after three operational incidents (one costing real money). Every session that runs a **costed** or **multi-step plan** in this repo follows it.

This is the operating-environment companion to the architecture: the code can be perfect and still bleed money or corrupt a branch if the environment around it is wrong. These rules are cheap insurance against the exact failures we already hit.

> Source incidents: [`docs/anima-test-runs/2026-06-02-operational-incidents-remediation-plan.md`](anima-test-runs/2026-06-02-operational-incidents-remediation-plan.md) · [`docs/anima-test-runs/2026-06-02-em-reference-images-field-report.md`](anima-test-runs/2026-06-02-em-reference-images-field-report.md) · [`docs/anima-test-runs/2026-06-01-em-critic-spine-hardening-postmortem.md`](anima-test-runs/2026-06-01-em-critic-spine-hardening-postmortem.md)

---

## 1. Subscription billing, never the API key — *(prevents incident #1: API credits drained)*

anima's Claude agents bill the **Claude subscription** via `claude-agent-sdk` → the `claude` CLI's OAuth login. A present `ANTHROPIC_API_KEY` silently overrides that and bills the Anthropic **API** — in non-interactive mode the `claude` CLI *always* uses the key when set, ahead of subscription OAuth.

- **Before any live run:** `ANTHROPIC_API_KEY` must be **absent** from the shell. Check: `echo "${ANTHROPIC_API_KEY:+SET}"` → must print nothing.
- Interactive billing: `claude login`; verify with `claude /status` (shows subscription, not a key).
- Headless billing: `claude setup-token` → export `CLAUDE_CODE_OAUTH_TOKEN`. The key must still be absent (it outranks the OAuth token).
- `evals/vision_critic/score.py` refuses to start if the key is set (override: `--allow-api-key`). The same fail-fast guard belongs on any other costed entrypoint (e.g. `evals/bakeoffs/.../bakeoff.py`) before it runs live.
- Keep API auto-reload **disabled** at console.anthropic.com so an accidental API run can't silently top up.
- **Positive verification:** after a fix, fire one cheap real call and confirm the API usage dashboard stays flat. Billing-route changes aren't done until proven, not assumed.

## 2. One isolated worktree per plan execution — *(prevents incidents #1's repeated edits + the shared-tree corruption in both prior sessions)*

- Run every costed / multi-step plan in a dedicated `git worktree` on its own branch — **never** the main checkout.
  ```bash
  git worktree add .claude/worktrees/feature+<slug> -b feature/<slug> main
  cd .claude/worktrees/feature+<slug>
  ```
- A second agent in the *same* working tree is silent corruption: two writers moving one HEAD. The worktree makes a stray session physically unable to move your HEAD.
- Tear the worktree down when the branch merges (`git worktree remove`), so it can't become a stale parallel checkout.

## 3. Singleton pre-flight — *(prevents the duplicate-executor sighting + the wrong-PID kill near-miss)*

Before starting a costed run, confirm you are the **only** agent in the repo, and always resolve your own PID before killing anything:

```bash
# Anyone else executing in this tree?
ps aux | grep -E 'claude|agy|score\.py|bakeoff|node' | grep -v grep
lsof -d cwd 2>/dev/null | grep -i Code-Brain/anima
# Resolve YOUR shell's `claude` ancestor up the ppid chain — never kill blind:
P=$$; while [ "$P" -gt 1 ]; do echo "$P $(ps -o comm= -p $P)"; P=$(ps -o ppid= -p $P | tr -d ' '); done
```

If a rogue executor is found, kill only what you've positively identified as *not* your session. (The critic-spine postmortem's near-miss: the most-suspicious PID was the session's own ancestor — one blind kill from ending the work.)

## 4. Single known owner for costed runs — *(prevents parallel `--segment` executions)*

A costed run has **one** launching shell, **one** branch/worktree, **one** owner. No second executor in a shared checkout. If you didn't launch it, don't assume it's safe — trace it.

## 5. Clean teardown at session end — *(prevents agents outliving the session)*

A child started with `start_new_session=True` (Python `setsid`) becomes its own session/process-group leader, detached from the terminal — it ignores the `SIGHUP` that ends the session and keeps running (and editing) afterward.

- **Do not** `start_new_session` a *costed worker*. Keep it a child of the session so teardown reaps it. (Detaching only a non-costed *orchestrator* across teardown crashes — the field-report pattern — is fine; the worker stays attached for Claude Code auth and for reaping.)
- At session end, sweep for orphans and confirm zero before closing:
  ```bash
  ps aux | grep -E 'claude|agy|score\.py|bakeoff' | grep -v grep   # expect none but your session
  ```
- Any costed process you didn't intend to leave running gets terminated before you walk away.

---

## Pre-costed-run checklist (the one-screen version)

1. `echo "${ANTHROPIC_API_KEY:+SET}"` prints nothing · `claude /status` shows subscription.
2. In an isolated worktree on a feature branch — not the main checkout.
3. Singleton confirmed (`ps`/`lsof` clean) · own PID resolved.
4. MCP overhead handled (incident #2): `agy plugin list` shows the heavy servers disabled for the run (no per-invocation flag exists; scope the disable in time — re-enable after).
5. Smoke first (`--limit 2`), then the full run.
6. At end: orphan sweep clean; worktree removed on merge.
