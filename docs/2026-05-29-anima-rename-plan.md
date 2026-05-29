# The anima rename — a runbook

*2026-05-29. The v2 change-map (§5) deferred the directory rename `sw-portfolio-animation-pipeline → anima` to "public-repo creation time, so git history stays clean." With two locked Bibles, 157 green tests, and the agent fleet meaningfully present, the window is open. This is mechanical work with a sharp edge — every missed hardcoded path breaks silently — so it gets a runbook, not an inline edit. **Timing: ship this AFTER the visual-fidelity fix. The fix is time-sensitive; the rename is not.***

---

## The good news: the blast radius is small

I audited the actual footprint this session. It's much smaller than the v2 change-map worried about.

- **Exactly one load-bearing hardcoded absolute path in production code:** `pipeline/generate_inbetweens.py:23` → `PIPELINE_DIR = Path("/Users/seanwinslow/Code-Brain/sw-portfolio-animation-pipeline")`. This is the one line that *breaks execution* on rename.
- **No `pyproject.toml` / `setup.py` / `setup.cfg`** — there is no declared package name to update.
- **`.env` carries no absolute paths.**
- **`code-brain/` has zero live dependencies on the folder name** — no `.py`, `.toml`, `.plist`, or `.sh` under `agents-sdk/` (or anywhere in the fleet) references it. No scheduled agent reads from this path. The only `code-brain` hits are historical markdown (interview notes, roadmap docs) and ephemeral session-log JSON — cosmetic, non-breaking.
- **Everything else in-repo** (≈22 files) is text: `CLAUDE.md`, `CHANGELOG.md`, and historical continuation-prompt docs under `docs/`. These don't break anything; they're just stale references to update for trustworthiness.
- **The `.venv` will break** — venvs hardcode their absolute path in `bin/activate`, `pyvenv.cfg`, and every script shebang. After `mv`, the venv must be recreated (cheap; deps are few).
- **GitHub remote is already `sw-portfolio-2D-animation`** — note this: the local folder name and the GitHub repo name *already* differ. Renaming the local folder to `anima` does not require touching GitHub at all. Renaming the GitHub repo to `anima` is a separate, optional consistency move.

So this is a one-line code fix + a venv rebuild + a `mv` + cosmetic text updates. The risk is real but contained.

---

## Workstream 1 — MacBook Pro local rename (the load-bearing one)

This is where the project lives and is edited. Do this first.

### Pre-flight
- [ ] Commit or stash all work in the repo. `git status` clean. The fidelity fix must already be shipped + committed.
- [ ] Close any IDE / editor window pointing at the old path (VS Code remembers absolute workspace paths).
- [ ] Stop any running process with the old path in its cwd (the `.remember` hook, any `author_bible.py` run, any pytest watcher).

### The rename
```bash
cd /Users/seanwinslow/Code-Brain
mv sw-portfolio-animation-pipeline anima        # single rename — preserves inode + full git history
cd anima
```

### Fix the one breaking path
```bash
# pipeline/generate_inbetweens.py:23 — the only production absolute path
sed -i '' 's#Code-Brain/sw-portfolio-animation-pipeline#Code-Brain/anima#' pipeline/generate_inbetweens.py
grep -n "anima" pipeline/generate_inbetweens.py          # verify
```
**Preferred over the `sed`:** change line 23 to a path-relative resolution so it never breaks on a move *and works on every machine regardless of where the clone lives* — `PIPELINE_DIR = Path(__file__).resolve().parents[1]`. This matters because the Mac Mini clone may sit at a different absolute path; a hardcoded `/Users/.../anima` would be wrong there too. The relative form fixes both machines at once. Use the `sed` only as a fallback if the relative form somehow breaks an import.

### Rebuild the venv (it broke on `mv`)
```bash
rm -rf .venv
python3 -m venv .venv
.venv/bin/pip install -q pytest pyyaml Pillow google-genai fal-client anthropic claude-agent-sdk
```
*(Match the deps the project actually imports — confirm against what the prior `.venv` carried if unsure.)*

### Verify
```bash
.venv/bin/pytest tests/ -q                # MUST be 176 passed — post-fidelity-fix baseline (157 + 19 added 2026-05-29), post-rename
grep -rIl "sw-portfolio-animation-pipeline" . --exclude-dir=.git --exclude-dir=.venv \
  | grep -vE "CHANGELOG|docs/2026-0[0-9]" || echo "no live refs remain"
```
- [ ] 176 tests green (post-fidelity-fix baseline).
- [ ] No live (non-historical-doc) references to the old name remain.
- [ ] Reopen the IDE on `/Users/seanwinslow/Code-Brain/anima`.

---

## Workstream 2 — GitHub rename (optional, for consistency)

The remote is `https://github.com/seanwinslow28/sw-portfolio-2D-animation.git`. The local folder name and repo name already differ, so this is **decoupled** from Workstream 1. Do it only if you want the GitHub repo to read `anima` too. (Recommended at public-repo time, since the v2 lock ties the rename to "public-repo creation.")

### On GitHub
- [ ] Repo → Settings → rename `sw-portfolio-2D-animation` → `anima`. GitHub auto-creates a redirect from the old URL, so existing clones keep working until you repoint them.

### Repoint the local remote
```bash
cd /Users/seanwinslow/Code-Brain/anima
git remote set-url origin https://github.com/seanwinslow28/anima.git
git remote -v                              # verify
git fetch origin                           # confirm the new URL resolves
```
- [ ] CI / Actions: none referencing the repo by hardcoded URL were found, but if any exist, update them. Anything pointing by repo *name* via the GitHub API updates automatically through the redirect.

---

## Workstream 3 — Mac Mini rename + sync

The audit found **no live dependency** on the folder name anywhere in `code-brain/` (the fleet that runs on the Mini reads the vault, not this project). So this workstream is "tidy the clone if one exists," not "untangle a dependency."

- [ ] **Find any clone:** `find ~ -maxdepth 5 -type d -name "sw-portfolio-animation-pipeline" 2>/dev/null` and `find ~ -maxdepth 5 -type d -name "sw-portfolio-2D-animation" 2>/dev/null` on the Mini.
- [ ] If a clone exists: `mv` it to `anima/`, then `git remote set-url origin https://github.com/seanwinslow28/anima.git` inside it.
- [ ] **Confirm no scheduled agent reads the old path** (belt-and-suspenders — the audit says clean):
  ```bash
  grep -rIn "sw-portfolio-animation-pipeline" ~/Code-Brain/code-brain/agents-sdk/ \
    --include="*.py" --include="*.toml" --include="*.plist" --include="*.sh" --include="*.json"
  # expect: no output
  ```
- [ ] If the Mini accesses the project via Google Drive mirror (per the interview notes), the Drive folder name follows the local rename on next sync — no action, but verify the sync completed before any Mini-side job expects the new name.

---

## What to update INSIDE the renamed folder

These don't break execution but keep `CLAUDE.md`/`CHANGELOG.md` trustworthy (the project's own maintenance rule). Do them in the rename commit.

- [ ] **`CLAUDE.md`** — every `sw-portfolio-animation-pipeline` mention + the Directory Structure file-map header. The doc already says "renames to `anima/` at public-repo creation"; flip that to past tense and update the tree's root line.
- [ ] **`CHANGELOG.md`** — add the rename entry (don't rewrite history; just append).
- [ ] **`pyproject.toml` / `setup.cfg`** — none exist; nothing to do. (If one is added later, name it `anima`.)
- [ ] **`.env`** — no absolute paths; nothing to do.
- [ ] **`manifest.yaml`** — confirm no absolute paths point at the old name (audit found none; the `project.name` is already `"anima"`).
- [ ] **README files** — update root references.
- [ ] **Historical `docs/` continuation-prompts** — these are dated session artifacts (the 2026-05-2x prompt files). **Leave them as-is** — they're a record of what the path *was* at the time. Rewriting them would falsify the history. Optionally add a one-line note at the top of `CLAUDE.md`'s file-map that pre-rename docs reference the old path by design.
- [ ] **`sw-ai-pm-portfolio`** (separate repo) — its `CLAUDE.md` references this project's path for the museum/Astro handoff. Update that reference in the portfolio repo's own next commit, not this one.

---

## The commit + rollback contract

- One commit: `rename: sw-portfolio-animation-pipeline → anima`. Includes the `generate_inbetweens.py` fix + CLAUDE.md/CHANGELOG/README text updates.
- **Tests stay green post-rename or the rename rolls back.** Rollback is trivial: `mv anima sw-portfolio-animation-pipeline`, `git checkout pipeline/generate_inbetweens.py`, rebuild venv.
- The `.venv` rebuild is *not* committed (it's gitignored); it's a local-environment step that must be redone on every machine that had a venv.

---

*The rename is cosmetic to the architecture and load-bearing to the story — "anima" is the name the public repo ships under. Small job, sharp edge, worth a runbook. Ship it once the character actually looks like Sean. — filed 2026-05-29*
