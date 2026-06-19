# Kickoff prompt — anima rename: Mac Mini

*Paste everything below the divider into a Claude Code session opened in the `sw-portfolio-animation-pipeline` clone on the Mac Mini.*

**Run the MacBook + GitHub prompt FIRST and let it fully finish.** This Mini prompt assumes the GitHub repo has already been renamed to `anima` and the rename commit is pushed. If the GitHub repo is still named `sw-portfolio-2D-animation`, stop and finish the MacBook side first.

*Same caveat as the MacBook side: a Claude Code session can't keep working after it renames its own root folder. The agent does everything possible in the current session, performs the `mv` last, and hands you a short Phase 4 block for a fresh session at the new path.*

---

You are completing the **anima rename** on the Mac Mini. The MacBook Pro session already renamed the folder there, renamed the GitHub repo `sw-portfolio-2D-animation → anima`, fixed the one production path to a machine-independent relative form, updated the docs, and pushed everything. Your job is to bring this Mini clone into line: sync from the renamed remote, rename the local folder, and confirm nothing on the Mini's autonomous fleet was reading the old folder name. The canonical runbook is `docs/2026-05-29-anima-rename-plan.md` (Workstream 3) — read it first if present in this clone.

Work in plan mode first (`Shift+Tab` twice), show me the plan, proceed on approval. Execute in order.

### Phase 0 — Locate and sanity-check (current session)

1. Run `pwd` and `git rev-parse --show-toplevel` to capture this clone's exact absolute path. Run `git remote -v`.
2. **Google Drive guard:** if the path contains `CloudStorage` or `GoogleDrive` (i.e. this folder is Drive-synced, not a plain local clone), **stop and tell me** — renaming a Drive-synced folder triggers a re-sync and can create conflict copies. We'll handle that case differently. Only continue if it's a plain local git clone.
3. Run `git status`. If there are uncommitted local changes on the Mini, **stop and show me** — don't clobber anything. Continue only on a clean tree.

### Phase 1 — Sync from the renamed remote (current session, old path)

4. Repoint the remote to the renamed repo: `git remote set-url origin https://github.com/seanwinslow28/anima.git`, then `git remote -v` to confirm.
5. `git fetch origin && git pull` to pull the rename commit and the in-file edits (the relative-path fix in `pipeline/generate_inbetweens.py`, the CLAUDE.md/CHANGELOG updates). Resolve nothing by guessing — if there's a conflict, stop and show me.
6. Confirm the sync landed: `grep -n "parents\[1\]" pipeline/generate_inbetweens.py` should show the relative path (no hardcoded `/Users/...`). If it still shows a hardcoded absolute path, the pull didn't land — stop and report.

### Phase 2 — Verify the fleet doesn't depend on the old folder name (current session)

7. Confirm no autonomous agent / schedule on the Mini reads the old path. Run, and expect **no output**:
   ```bash
   grep -rIn "sw-portfolio-animation-pipeline" ~/Code-Brain/code-brain/agents-sdk/ \
     --include="*.py" --include="*.toml" --include="*.plist" --include="*.sh" --include="*.json" 2>/dev/null
   ```
   Also check launchd plists and any cron: `grep -rIn "sw-portfolio-animation-pipeline" ~/Library/LaunchAgents/ 2>/dev/null; crontab -l 2>/dev/null | grep "sw-portfolio-animation-pipeline"`. If anything matches, **show me each hit** — we update those before renaming. (The MacBook-side audit found zero live dependencies, so this should be clean, but the Mini is where the fleet actually runs, so verify it here.)

### Phase 3 — Rename the local folder (final action of this session)

8. Run the suite once before renaming to capture the Mini's baseline, if a venv exists here: `.venv/bin/pytest tests/ -q` (note the count; expect 176 if this clone's venv has the deps — if the venv is broken or missing, skip and we rebuild in Phase 4).
9. As the **last** command, rename from the parent dir using the path you captured in step 1 (substitute the real parent):
   ```bash
   cd <parent-of-this-clone> && mv sw-portfolio-animation-pipeline anima
   ```
10. **Stop.** Tell me: *"Mini folder renamed to `<parent>/anima`. This session's cwd is now invalid — open a fresh Claude Code session there and paste the Phase 4 block."* Run nothing further in this session.

### Phase 4 — Fresh session at the new path (I will paste this into a new Claude Code window opened at the renamed `…/anima` on the Mini)

> Finish the Mac Mini side of the anima rename. The folder is renamed and the remote already repointed. Do the post-`mv` steps:
> 1. If a `.venv` exists and is now broken (its shebangs pointed at the old path), rebuild it: `rm -rf .venv && python3 -m venv .venv && .venv/bin/pip install -q pytest pyyaml Pillow google-genai fal-client anthropic claude-agent-sdk`. (No torch/transformers — DINOv2 tier is deferred.) If this Mini clone is read-only infrastructure that never ran tests, skip the venv.
> 2. If you rebuilt the venv, run `.venv/bin/pytest tests/ -q` and confirm **176 passed**.
> 3. Confirm `git remote -v` shows the `anima` URL, `git status` is clean, and `git pull` is up to date.
> 4. Re-run the fleet-dependency grep from Phase 2 against the new path to be sure nothing still references the old folder name. Report final state.

**Rollback** (if Phase 4 fails irrecoverably): `cd <parent> && mv anima sw-portfolio-animation-pipeline`, rebuild venv. The remote/redirect on GitHub is unaffected.

**Do not** modify Bible state, `runs/`, or any fleet config beyond a remote URL — if step 7 surfaced a real dependency, show it to me rather than editing it unprompted.
