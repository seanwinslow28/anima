# Kickoff prompt — anima rename: MacBook Pro + GitHub

*Paste everything below the divider into a Claude Code session opened at `/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline`. Run this one FIRST and let it finish completely (including the GitHub repo rename + push) before you run the Mac Mini prompt — the Mini depends on the renamed GitHub repo existing.*

*One structural caveat baked into the steps below: a Claude Code session cannot keep working after it renames its own root folder — its working directory becomes invalid. So this prompt has the agent do everything possible in the current session, perform the `mv` as its final action, and then hand you a short Phase 2 block to paste into a fresh session opened at the new path. That's expected, not a failure.*

---

You are executing the **anima rename** on the MacBook Pro. The canonical runbook is `docs/2026-05-29-anima-rename-plan.md` — read it first; it is the source of truth and these steps implement it. The rename is `sw-portfolio-animation-pipeline → anima`. Work carefully: this is mechanical work with a sharp edge (a missed path breaks silently), and it must be a clean, reversible, isolated commit.

**Context you need:**
- The fidelity fix already shipped (7 commits, `6e46ac0`→`11d48b3`). The test baseline is now **176 passed**, not 157.
- The only load-bearing hardcoded absolute path in production code is `pipeline/generate_inbetweens.py:23`.
- There is no `pyproject.toml`/`setup.py`, and `.env` carries no absolute paths.
- The GitHub remote is currently `https://github.com/seanwinslow28/sw-portfolio-2D-animation.git` — the repo name already differs from the folder name, so the local rename and the GitHub rename are independent.
- Use `gh` (GitHub CLI) for the repo rename if it's installed and authenticated; if not, stop at that step and tell me so I can do it in the web UI.

Work in plan mode first (`Shift+Tab` twice), show me the plan, and proceed once I approve. Then execute these phases in order.

### Phase 1 — Git hygiene (current session, old path)

1. Run `git status`. There is a stack of untracked docs (the rename plan, the fidelity-fix implementation prompt, the post-mortem cowork prompt, `docs/anima-test-runs/*`, and some `docs/superpowers/plans/*` scratch files). Show me the list and propose which to commit vs. gitignore. The `docs/superpowers/plans/*` files are session scratch — propose adding them to `.gitignore` unless I say otherwise. Commit the real docs with a clear message.
2. Confirm the 7 fidelity-fix commits and the hygiene commit are pushed: `git push`. Verify `git status` is clean and `git log --oneline origin/HEAD..HEAD` is empty before continuing. **Do not proceed to Phase 2 with a dirty tree or unpushed commits.**

### Phase 2 — In-file edits (current session, old path)

3. **Fix the one production path.** Edit `pipeline/generate_inbetweens.py:23` to a machine-independent relative resolution: `PIPELINE_DIR = Path(__file__).resolve().parents[1]`. (This is preferred over hardcoding `/Users/.../anima` because the Mac Mini clone lives at a different absolute path — the relative form fixes both machines at once.) Confirm the file still imports and the path resolves to the repo root.
4. **Update the docs that carry the old name as live references** (not historical artifacts):
   - `CLAUDE.md` — every `sw-portfolio-animation-pipeline` mention and the Directory-Structure file-map root line; flip the "renames to anima at public-repo creation" note to past/active tense.
   - `CHANGELOG.md` — append a dated rename entry (don't rewrite history).
   - `README` files — update root references.
   - **Leave the dated `docs/2026-05-2x-*` continuation-prompts and `docs/anima-test-runs/*` untouched** — they're historical records and should reference the old path by design.
5. **Run the suite: `.venv/bin/pytest tests/ -q` — expect 176 passed.** If it's not 176, stop and tell me.
6. Commit as `rename: sw-portfolio-animation-pipeline → anima (in-file path + doc updates)` and `git push`.

### Phase 3 — GitHub repo rename + remote (current session, old path)

7. If `gh` is installed and authenticated (`gh auth status`): rename the repo with `gh repo rename anima --repo seanwinslow28/sw-portfolio-2D-animation`. If `gh` is not available, **stop here and tell me** — I'll rename it in the web UI, then you continue.
8. Repoint the local remote: `git remote set-url origin https://github.com/seanwinslow28/anima.git`, then `git remote -v` and `git fetch origin` to confirm the new URL resolves. (GitHub keeps a redirect from the old URL, so this is safe.)

### Phase 4 — The folder rename (final action of this session)

9. As the **last** command in this session, rename the folder from the parent directory:
   ```bash
   cd /Users/seanwinslow/Code-Brain && mv sw-portfolio-animation-pipeline anima
   ```
10. **Stop.** Tell me clearly: *"The folder is renamed to `/Users/seanwinslow/Code-Brain/anima`. This session's working directory is now invalid — open a fresh Claude Code session at the new path and paste the Phase 5 block to finish."* Do not attempt any further commands in this session — they will fail against the stale cwd.

### Phase 5 — Fresh session at the new path (I will paste this into a new Claude Code window opened at `/Users/seanwinslow/Code-Brain/anima`)

> Finish the anima rename. The folder has been renamed and the GitHub remote already repointed. Do the post-`mv` steps only:
> 1. Rebuild the broken venv (its shebangs pointed at the old path): `rm -rf .venv && python3 -m venv .venv && .venv/bin/pip install -q pytest pyyaml Pillow google-genai fal-client anthropic claude-agent-sdk`. (Do **not** install torch/transformers — the DINOv2 tier is deliberately deferred.)
> 2. Run `.venv/bin/pytest tests/ -q` — confirm **176 passed**. If not, report what failed.
> 3. Run `grep -rIl "sw-portfolio-animation-pipeline" . --exclude-dir=.git --exclude-dir=.venv | grep -vE "docs/2026-05-2|docs/anima-test-runs"` — confirm no *live* references remain (only historical docs should match, and the grep above already excludes them, so ideally zero output).
> 4. Confirm `git remote -v` shows the `anima` URL and `git status` is clean. Report final state.

**Rollback** (if anything fails irrecoverably in Phase 5): `cd /Users/seanwinslow/Code-Brain && mv anima sw-portfolio-animation-pipeline`, `git checkout pipeline/generate_inbetweens.py`, rebuild the venv, and `gh repo rename sw-portfolio-2D-animation` + `git remote set-url` back. The redirect makes the GitHub side reversible.

**Do not** touch the Bible state (`characters/*`, `plate_verdicts.jsonl`, `runs/*`) — the rename is orthogonal to it. The sean-anchor Bible approval and production plate bake happen separately, in the renamed folder, after this.
