# Claude Code execution prompt — Em live re-baseline (deferred run)

> Paste the block below into a fresh Claude Code session opened in the `anima` project.
> Everything above the `─── PROMPT ───` line is operator context for Sean, not for the agent.

**State at handoff (verified 2026-06-02, from the Cowork pre-flight session):**

- Gates **#1** (subscription billing — `ANTHROPIC_API_KEY` absent, Max active) and **#2** (`agy` MCP-free — `~/.gemini/settings.json` `mcpServers` emptied) are **closed**.
- Gate **#3** loose ends are resolved: `stash@{0}` (the rejected hand-authored-references design from session 22428) was **dropped**; the env-hardening bundle was **committed/merged to `main`** (`c6a2aed` on top of PR #13 `79d36f2`), so the `score.py` fail-fast guard (`REFUSING TO RUN` on a leaked key) is now on `main`. Main working tree is clean.
- The **isolated worktree already exists**: branch `eval/em-rebaseline` at `.claude/worktrees/em-rebaseline`, `.env` symlinked in, main venv reused. **Do not cut a new worktree.**
- The **`--limit 2` smoke already passed operationally**: references attached (`anchor, head-front, head-profile-left, body-3quarter`), `cites-correct=1.00`, orchestrator survived teardowns, no key leak. Its precision/recall numbers are degenerate (2 clean cases, 0 positives) and are **not** a baseline. One honest early signal to carry in: `clean-act1-f13-gesture` was still flagged `fail` *with references attached* — watch whether the full run's precision actually lifts off 0.62 or whether f13-class false alarms persist.
- Runtime ran ~189s/case in the smoke (Opus escalations are slow), so the full 24-case run is realistically **~60–75 min**, not the runbook's 20–25.

---

─── PROMPT ───

We're finishing the deferred **Em (T2 vision critic) live re-baseline** — the costed measurement the reference-images workstream shipped code for but deferred to a clean terminal. The code is done and test-pinned (264 green, n=1 live-proven); this run produces the *number* — does giving Em references + criteria lift **performs precision** off the reference-blind baseline **without costing any false pass**?

**Read first, in order:** `docs/anima-test-runs/2026-06-02-em-rebaseline-runbook.md` (the spine), `docs/anima-test-runs/2026-06-02-em-reference-images-field-report.md` (the deferred-run recipe + the disciplines), `docs/fleet-ops-protocol.md` (the standing run discipline). CLAUDE.md's Em row and the top three CHANGELOG entries carry the rest of the state.

**The baseline to beat (reference-blind, 2026-06-01):** performs **precision 0.62, recall 1.00, false-pass 0.00**.

**Non-negotiable operating rules (this is a costed run — fleet-ops protocol applies):**

1. **Subscription billing only. NEVER set or export `ANTHROPIC_API_KEY`.** Confirm it's absent before anything live. `score.py` refuses to start if it's set — **do not** pass `--allow-api-key` to bypass that. Headless billing is the subscription OAuth (`claude /status` must show `claude.ai / max`); `claude setup-token` → `CLAUDE_CODE_OAUTH_TOKEN` if a token is needed for a detached process. The key must stay absent (it outranks the token).
2. **Run only from the existing isolated worktree** `.claude/worktrees/em-rebaseline` (branch `eval/em-rebaseline`). Never run the eval from the main checkout. Reuse the main venv: `PY=~/Code-Brain/anima/.venv/bin/python`. `.env` is already symlinked in.
3. **Singleton + own-PID.** Before the costed run, confirm you're the only agent in the repo and resolve your own `claude` ancestor up the ppid chain before killing anything.
4. **Detach only the orchestrator at launch, NEVER the workers** — workers need the session for Claude Code auth; detaching them breaks it and every case errors. Don't spawn a costed worker that outlives the session.
5. **Labels stay locked.** If any case's label looks wrong, present it to Sean and re-ratify before changing it — never tune a label to flatter Em.

**Do this:**

1. **Pre-flight (gate re-confirm).** From the worktree:
   ```bash
   cd ~/Code-Brain/anima/.claude/worktrees/em-rebaseline
   PY=~/Code-Brain/anima/.venv/bin/python
   echo "${ANTHROPIC_API_KEY:+LEAK — STOP}${ANTHROPIC_API_KEY:-clean}"   # want: clean
   claude /status                                                        # want: claude.ai / max
   agy plugin list                                                       # want: empty
   ps aux | grep -E 'claude|agy|score\.py|bakeoff|node' | grep -v grep   # want: only your own session
   P=$$; while [ "$P" -gt 1 ]; do echo "$P $(ps -o comm= -p $P)"; P=$(ps -o ppid= -p $P | tr -d ' '); done
   ```
   If `ANTHROPIC_API_KEY` reads `LEAK`, stop and fix the env — do not proceed and do not use `--allow-api-key`.

2. **The full costed run — 23 performs + 1 motion smoke (24 cases).** Detach only the orchestrator; workers stay session-attached. Foreground is also acceptable if you'd rather watch it live.
   ```bash
   $PY -c "import subprocess,sys; subprocess.Popen([sys.executable,'-m','evals.vision_critic.score',\
     '--segment','performs','--motion-smoke','1'], start_new_session=True)"
   # …or foreground:
   # $PY -m evals.vision_critic.score --segment performs --motion-smoke 1
   ```
   Scope rationale: the headline metrics live in the **performs** segment; a still-image contact sheet structurally can't score motion-proper (eval-strategy §3.5), so the other 5 motion cases are logged as intentionally-not-scored. The 1 motion smoke exercises reference-attach on the phase-6 contact-sheet path. Expect ~60–75 min (~189s/case in the smoke; Opus escalations are slow). Poll `evals/vision_critic/last-run.md` for completion; don't relaunch while it's running (single owner).

3. **Score `last-run.md` with the disciplines, IN THIS ORDER — and stop to discuss with Sean before writing conclusions:**
   1. **False-pass first.** Did `recall` hold at **1.00** and `false_pass_rate` at **0.00** on the performs segment? A precision lift that costs *any* false pass on performs is a **worse Em** — it blocks the change and **promotes follow-on #3 (DINOv2 identity backstop) from deferred to next.**
   2. **Then precision lift.** Compare to the reference-blind baseline **0.62**. Report the delta **with `stderr()` on it** — is it real or noise at this n?
   3. **Then cites-correct.** Did surfacing `IR.*`/`AC.*` raise citation accuracy?
   4. **Labels stay locked** — flag any that look wrong to Sean for re-ratification; don't change them in this run.

4. **Write-up + teardown** (after Sean agrees the read):
   - Append the result (pre/post precision, recall + false-pass held, cites-correct, the n) to `docs/anima-test-runs/2026-06-02-em-reference-images-field-report.md` — flip its `⏸ Live re-baseline — DEFERRED` line to **measured**.
   - Add a CHANGELOG entry.
   - Flip the CLAUDE.md Em row to "reference-grounded, baseline re-run **measured**" with the number. The pre/post delta (0.62 reference-blind → measured-with-references) is the portfolio artifact — the moment Em stopped grading blind.
   - Orphan sweep: `ps aux | grep -E 'agy|score\.py|bakeoff' | grep -v grep` → none. Remove the worktree once `eval/em-rebaseline` merges: `git worktree remove .claude/worktrees/em-rebaseline`.

**Out of scope / deferred (don't start without Sean):** the three-way Gemini/Sonnet/Opus bake-off re-run (its own Gemini-quota window), view-aware reference selection (approach A), pairwise-verdict reframe, the DINOv2 backstop (unless step 3.1 surfaces a false pass — then it's promoted to next). Note: from 2026-06-15 subscription Agent-SDK / `claude -p` usage draws from a separate monthly Agent-SDK credit pool — relevant only to where the ~$2–3 lands, not a blocker.

**Stop and show Sean: (a) the pre-flight gate output, (b) the full-run `last-run.md` read under the disciplines — before writing any conclusions or touching the docs.**
