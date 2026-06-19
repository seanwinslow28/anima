# Runbook — deferred Em reference-images re-baseline

**Purpose:** the single sheet to follow when actually running the costed Em live re-baseline that the reference-images workstream deferred. Folds the three operational gates + the field report's run recipe + the scoring disciplines into one ordered procedure.

**Sources this consolidates:** [field report](2026-06-02-em-reference-images-field-report.md) (§"the deferred run" recipe + §9 disciplines) · [remediation plan](2026-06-02-operational-incidents-remediation-plan.md) (the three gates) · [fleet-ops protocol](../architecture/fleet-ops-protocol.md).

**What we're measuring:** does giving Em references + criteria lift **precision** on the performs segment **without costing any false pass** (recall must hold at 1.00, false-pass at 0.00)? The reference-blind baseline to beat: **performs precision 0.62, recall 1.00, false-pass 0.00** (2026-06-01).

---

## 0. Gates — all three must be green before a costed call

| Gate | Status | Re-confirm command |
|---|---|---|
| **#1 — subscription billing** | ✅ closed 2026-06-02 | `echo "${ANTHROPIC_API_KEY:+LEAK}${ANTHROPIC_API_KEY:-clean}"` → `clean`; `claude /status` → Max subscription |
| **#2 — agy MCP-free** | ✅ closed 2026-06-02 | `agy plugin list` → empty; (servers emptied in `~/.gemini/settings.json`) |
| **#3 — singleton + worktree** | run-time | the pre-flight in step 2 |

If gate #1 ever reads `LEAK`, **stop** — `score.py` will refuse anyway (`--allow-api-key` is the deliberate override, not for this run).

---

## 1. Auth for the headless run

The run is non-interactive, so make subscription billing durable (slot #5 OAuth token), and confirm the key is absent (slot #3 would outrank the token):

```bash
echo "${ANTHROPIC_API_KEY:+LEAK — fix before proceeding}${ANTHROPIC_API_KEY:-key absent ✓}"
# If you don't already have one set for this shell:
claude setup-token                       # prints a 1-yr token (Max plan)
export CLAUDE_CODE_OAUTH_TOKEN=...        # paste it
claude /status                           # confirm: claude.ai / max
```

> **2026-06-15 note:** on/after that date, subscription Agent-SDK / `claude -p` usage draws from the new separate monthly Agent-SDK credit pool, not your interactive limits. Doesn't block the run; just where the ~$2–3 lands.

## 2. Singleton pre-flight + isolated worktree (gate #3)

```bash
# (a) Am I the only agent in the repo?  Expect only your own shell.
ps aux | grep -E 'claude|agy|score\.py|bakeoff|node' | grep -v grep
lsof -d cwd 2>/dev/null | grep -i Code-Brain/anima
# Resolve your OWN shell's claude ancestor before killing anything:
P=$$; while [ "$P" -gt 1 ]; do echo "$P $(ps -o comm= -p $P)"; P=$(ps -o ppid= -p $P | tr -d ' '); done

# (b) Decide the preserved stash (likely redundant — `--segment` is already on main):
git -C ~/Code-Brain/anima stash show -p stash@{0}    # then keep, or: git stash drop

# (c) Isolated worktree off main — never run the eval from the main checkout:
cd ~/Code-Brain/anima
git worktree add .claude/worktrees/em-rebaseline -b eval/em-rebaseline main
cd .claude/worktrees/em-rebaseline
```

Use this worktree's venv (or the repo venv): confirm `.venv/bin/python`, `agy` on PATH, `claude_agent_sdk` importable.

## 3. Smoke first (cheap, proves the harness survives)

```bash
# 2-case smoke — confirms orchestrator survives worker teardowns + references attach.
# A --limit run is PARTIAL — its last-run.md is NOT a baseline.
.venv/bin/python -m evals.vision_critic.score --segment performs --limit 2
```

Want: it runs, prints per-case progress (`[1/2] … refs=[anchor, head-front, …]`), and writes a matrix without the orchestrator dying. If it prints `REFUSING TO RUN`, gate #1 regressed — fix the env, don't pass `--allow-api-key`.

## 4. The full run — 23 performs + 1 motion smoke (24 cases)

Per the field report recipe: **detach only the orchestrator** (so a worker teardown-signal can't kill it), **never the workers** (they need the session for Claude Code auth). On macOS:

```bash
# Detached orchestrator; workers stay session-attached:
python -c "import subprocess,sys; subprocess.Popen([sys.executable,'-m','evals.vision_critic.score',\
  '--segment','performs','--motion-smoke','1'], start_new_session=True)"

# …or simply run it foreground in a real terminal (also fine, simpler to watch):
.venv/bin/python -m evals.vision_critic.score --segment performs --motion-smoke 1
```

Scope rationale: the headline metrics live in the **performs** segment; a still-image contact sheet can't score motion-proper (eval-strategy §3.5), so the other 5 motion cases are logged as intentionally-not-scored. The 1 motion smoke exercises reference-attach on the phase-6 contact-sheet path. Runtime ≈ 20–25 min (Gemini default + Opus escalation, ~25–80s/case).

## 5. Read the result with the §9 disciplines — in this order

Outputs: `evals/vision_critic/last-run.md` + a dated trace.

1. **False-pass first.** Did `recall` hold at **1.00** and `false_pass_rate` at **0.00** on the performs segment? A precision lift that costs *any* false pass on performs is a **worse Em** — it blocks the change and **promotes follow-on #3 (DINOv2 backstop) from deferred to next.**
2. **Then precision lift.** Compare to the reference-blind baseline (0.62). Report the delta with `stderr()` on it — is it real or noise?
3. **Then cites-correct.** Did surfacing `IR.*`/`AC.*` raise citation accuracy?
4. **Labels stay locked.** If any case's label looks wrong, present it to Sean and re-ratify *before* changing it — never tune a label to flatter Em.

## 6. Write-up + teardown

- Append the result (pre/post precision, recall/false-pass held, cites-correct, the n) to the field report and a CHANGELOG entry; flip the CLAUDE.md Em row to "reference-grounded, baseline re-run **measured**" with the number.
- The pre/post delta (0.62 reference-blind → measured-with-references) is the portfolio artifact — the moment Em stopped grading blind.
- Teardown: orphan sweep (`ps … | grep -E 'agy|score\.py'` → none), then `git worktree remove` once the branch merges.

## 7. Follow-on (separate quota window, optional) — the three-way bake-off re-run

The Gemini column of the 2026-05-31 bake-off was invalid (consumer-tier quota exhausted mid-run). A clean three-way (Gemini re-run after quota reset + the shipped `RateCapExhausted` fix + **references attached**) belongs in its own Gemini-quota window:

```bash
python evals/bakeoffs/2026-05-31-t2-vision-critic-gemini-vs-sonnet-vs-opus/bakeoff.py
```

Not on the critical path — the T2 default stays Gemini until a valid, reference-grounded three-way licenses a swap.

---

## One-screen checklist

- [ ] `ANTHROPIC_API_KEY` absent · `claude /status` = Max · `CLAUDE_CODE_OAUTH_TOKEN` set
- [ ] `agy plugin list` empty (gate #2)
- [ ] singleton clean · own PID known · `stash@{0}` decided
- [ ] isolated worktree off `main`
- [ ] `--limit 2` smoke runs + references attach
- [ ] full `--segment performs --motion-smoke 1`
- [ ] recall 1.00 + false-pass 0.00 **first**, then precision delta, then cites-correct
- [ ] write-up + CHANGELOG + CLAUDE.md Em row · orphan sweep · worktree removed
