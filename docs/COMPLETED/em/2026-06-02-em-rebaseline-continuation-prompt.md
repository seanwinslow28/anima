# Continuation prompt — Em re-baseline (paste into a fresh Cowork session)

We're resuming anima's agent-fleet work. The three operational incidents that blocked
costed eval runs are resolved; the next job is the deferred Em (T2 vision critic) live
re-baseline. Get oriented from the files below, then help me run it.

READ FIRST, in this order (don't skip — they carry the verified state):
1. ~/Code-Brain/anima/CLAUDE.md  and  ~/Code-Brain/anima/PHILOSOPHY.md  (project orientation)
2. ~/Code-Brain/anima/docs/anima-test-runs/2026-06-02-em-rebaseline-runbook.md  (THE runbook — what we're executing)
3. ~/Code-Brain/anima/docs/anima-test-runs/2026-06-02-operational-incidents-remediation-plan.md  (the three incidents + their cleared/closed result notes)
4. ~/Code-Brain/anima/docs/fleet-ops-protocol.md  (the standing run discipline)
5. ~/Code-Brain/anima/docs/anima-test-runs/2026-06-02-em-reference-images-field-report.md  (what shipped + the deferred-run recipe + §9 scoring disciplines)
6. ~/Code-Brain/anima/CHANGELOG.md  (top 3 entries: incident #1 closed, incident #2 cleared, the env-hardening)

STATE (as of 2026-06-02):
- Em's reference-images code shipped, test-pinned (264 green, n=1 live-proven). The
  COSTED live re-baseline + 3-way bake-off were deferred — that's what we're doing now.
- Gate #1 (subscription billing, not API key): CLOSED + proven (dashboard flat).
- Gate #2 (agy MCP-free): CLOSED (~/.gemini/settings.json mcpServers emptied; zero spawns).
- Gate #3 (singleton + isolated worktree + clean teardown): protocol shipped; two run-time
  loose ends remain — the live-process sweep and the `stash@{0}` keep/drop decision.
- Reference-blind baseline to beat: performs precision 0.62, recall 1.00, false-pass 0.00.

NON-NEGOTIABLE operating rules (this is a Cowork session — see fleet-ops-protocol.md):
- Subscription billing only. NEVER set/export ANTHROPIC_API_KEY. For the headless run use
  `claude setup-token` → CLAUDE_CODE_OAUTH_TOKEN, and confirm the key is absent first.
  score.py refuses to start if the key is set (don't use --allow-api-key to bypass).
- Run the eval from an ISOLATED git worktree, never the main checkout. Confirm you're the
  sole agent (ps/lsof) and resolve your own PID before killing anything.
- Detach only the orchestrator at launch, NEVER the workers (they need the session for
  Claude Code auth). Don't spawn background executors that outlive the session.
- Smoke with --limit 2 before the full 24-case run.
- Score with the §9 disciplines IN ORDER: recall 1.00 + false-pass 0.00 FIRST, then the
  precision delta (with stderr), then cites-correct. Labels stay locked unless a validity
  fix is re-ratified by me.

FIRST ACTIONS:
1. Set up a task list. Walk me through gate #3's two loose ends (live-process sweep +
   stash decision) and confirm gates #1/#2 still hold with the runbook's re-confirm commands.
2. Then drive the runbook step by step: worktree → auth → --limit 2 smoke → full
   `--segment performs --motion-smoke 1` → read last-run.md with the disciplines → write-up
   (field report + CHANGELOG + CLAUDE.md Em row) → teardown.
3. STOP and show me the smoke result before the full costed run.

Note: from 2026-06-15, subscription Agent-SDK / `claude -p` usage draws from a separate
monthly Agent-SDK credit pool — relevant only to where the ~$2–3 lands, not a blocker.
