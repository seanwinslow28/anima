# Kickoff — anima Repo Organization & Public-Readiness Audit

> **Paste everything below the line into Claude Code, run from the repo root
> (`/Users/seanwinslow/Code-Brain/anima/`). Start in Plan Mode
> (double `Shift+Tab`) — Phase 0 produces a plan for my approval before any
> file moves.**

---

## Role & mission

You are working in **anima**, my 2D-animation agent-fleet pipeline. I'm about to
start applying to PM jobs and I want to **flip this repo from private to public**
on GitHub (`github.com/seanwinslow28/anima`) so recruiters and hiring managers can
browse it. Before that happens it needs two things:

1. **Organization** — `docs/` has decayed into a flat dump. Restructure the whole
   repo so every continuation prompt, kickoff, build plan, brainstorm, handoff,
   post-mortem, field report, and research doc lives in an obvious place where I
   can find it and know what it is at a glance.
2. **Public-readiness / gitignore audit** — make sure nothing private, secret, or
   junk is tracked, the `.gitignore` is correct, and the repo presents as the work
   of a rigorous AI PM. The candid material (post-mortems, cost figures, incident
   reports) **stays public on purpose** — it's the evidence of rigor — just
   organize it well.

This is a **high-stakes, link-dense repo**: `CLAUDE.md` (93 KB) and `ROADMAP.md`
are woven through with relative-path links to the docs you'll be moving. Breaking
those links silently corrupts the project's source-of-truth. Treat link integrity
as a first-class deliverable, not an afterthought.

## Locked decisions (don't re-litigate these — I already chose)

- **Git history: FORWARD-ONLY.** Do **not** rewrite history. No `git filter-repo`,
  no force-push, no rebase. Use `git rm --cached` to *stop tracking* files that
  shouldn't be tracked, going forward. History stays intact.
- **Candid docs: KEEP PUBLIC.** Post-mortems, `$`-cost figures, "operational
  incident" reports, and confidence hedges stay visible. Do **not** sequester or
  scrub them. For an AI PM portfolio they are the differentiator. Just file them
  sensibly.
- **Execution: PLAN + EXECUTE WITH GATES.** One session. Produce the full plan
  (Phase 0), get my approval, then execute phase by phase, **stopping for my
  sign-off after each phase** — especially before any `git rm --cached` and before
  I flip the repo to public.

## What I already know about the current state (verify, don't trust blindly)

A scan on 2026-06-18 found:

- **`docs/` root holds ~111 loose `.md` files.** Rough taxonomy by filename:
  36 `*-kickoff`, 14 `*-continuation-prompt`, 10 `*-build-plan`, 8 `*-handoff`,
  7 `*-brainstorm`, 6 `*-implementation-prompt`, 4 `*-design`, 2 `*-post-mortem`,
  1 `*-runbook`, plus ~13 canonical/active docs (`pipeline-architecture-v1.md`,
  `production-checklist.md`, `fleet-ops-protocol.md`, `museum-exhibit-schema.md`,
  `prompt-style-neutrality-doctrine.md`, `pencil-test-storyboard.md`,
  `act2-seedance-shot-list.md`, `Sprite-Sheet-Automation-Project_OG-Workflow-Summary.md`,
  `Edit-API-String.md`, `Conversation-that-utilized-prompt-science-successfully.md`).
- **An archive convention already exists and is underused:** `docs/COMPLETED/` (8
  files) and `docs/OLD/` (8 files); `prompts/COMPLETED/` and `prompts/OLD/` too.
  Per `CLAUDE.md` → *Maintenance Conventions*, shipped work goes to `COMPLETED/`,
  superseded work to `OLD/`, moved with `git mv`.
- **Already-foldered and fine:** `docs/anima-test-runs/` (48 field reports),
  `docs/research/` (22), `docs/examples/`, `docs/superpowers/`,
  `docs/Image-Model-DR-2026/`, `docs/open-sourced-video-model-research/`.
- **One real gitignore leak:** `runs/` is gitignored, but **38 files were committed
  before the rule and are still tracked** — throwaway `cy-scratchpad/*.py` analysis
  scripts, `cy-run.log`, a few stray PNGs/`.md`. A handful (`round2-decisions.md`,
  `round3-audit.md`, `selection.md`) may be referenced by `CLAUDE.md` as
  source-of-truth — **check before untracking those specifically.**
- **`.DS_Store` files exist** under `docs/`, `images/`, root — `.gitignore` lists
  `.DS_Store` but verify none slipped into tracking before the rule.
- **No secret leak detected:** `.env` was never committed (only `.env.example` is
  tracked); the two `grep` hits for "api key" were placeholder help-text. **Re-verify
  this** — it's the single most important public-switch check.
- **Asset/image clutter:** `images/` mixes live refs with apparent staging/retired
  dirs (`NEW-ANIMATION-PIPELINE/`, `sean-character-dataset/` which `CLAUDE.md`
  calls RETIRED, `3D-Character-Reference-Test/`, `Sprite-reference/`, `head-turn/`),
  loose annotated PNGs (`PT_A1_F31_key_red-circle.png`), and a back-compat symlink
  (`2D-Character-Sketch-Sean-v1.png → characters/sean-anchor/anchor.png`). Many
  ~6 MB PNGs are tracked. Treat carefully — `CLAUDE.md` documents which paths are
  load-bearing symlinks/back-compat.
- **Repo facts:** 1,436 tracked files, 251 commits, 195 MB `.git`, ~2.2 GB working
  tree (mostly untracked `runs/` + `.venv/`). Remote: `github.com/seanwinslow28/anima`.
- **No top-level `README.md`** — `CLAUDE.md` is the de-facto readme but it's a
  93 KB internal agent-instruction file, not a recruiter's entry point.

## Hard constraints (negative — violating any of these is a failure)

- **NEVER use plain `mv` on a tracked file. Always `git mv`** so history follows
  the file.
- **NEVER move a file without updating every internal link that points at it.**
  After each batch of moves, grep the whole repo for the old paths and fix every
  reference in `CLAUDE.md`, `ROADMAP.md`, `PHILOSOPHY.md`, and any doc-to-doc link.
- **NEVER rewrite git history.** Forward-only. No `filter-repo`/`rebase`/force-push.
- **NEVER delete `runs/` content from disk.** It's gitignored evidence I keep
  locally. For the leak, only `git rm --cached` (untrack, keep the file on disk).
- **NEVER scrub or sequester the candid docs** (costs, post-mortems, incidents).
- **NEVER weaken an existing `.gitignore` rule** (e.g. `PORTFOLIO-GOLD.md`, `.env*`).
- **DON'T break the test suite.** Tests run **per-directory** (`python -m pytest
  tests/`, then `python -m pytest pipeline/tests/` separately — see `CLAUDE.md` →
  *Testing*). Green before and after.
- **Honor the maintenance conventions** in `CLAUDE.md`: append a `CHANGELOG.md`
  entry for the reorg (what + why), and update `CLAUDE.md`'s *Directory Structure*
  + *Source of Truth* table + *Skills Map* file paths to match the new layout.

---

## Phase 0 — Discovery & Plan (READ-ONLY, no changes, stop for approval)

First read, in order: `CLAUDE.md` (esp. *Maintenance Conventions*, *Directory
Structure*, *Source of Truth Documents*), `ROADMAP.md` (the single active
workstream + anti-drift contract), `PHILOSOPHY.md`, and the current `.gitignore`.

Then produce a written plan containing:

1. **Active-vs-historical classification.** For the ~111 loose `docs/` files,
   decide each one's status by cross-referencing `ROADMAP.md` (what's the *active*
   workstream) and whether `CLAUDE.md` links to it as canonical/source-of-truth.
   Output a table: `file → ACTIVE-canonical | HISTORICAL-kept | superseded(OLD) |
   shipped(COMPLETED)`.
2. **Proposed target taxonomy.** Recommend a folder structure and justify it.
   Starting proposal (improve it, then confirm with me):
   - Canonical/active docs stay top-level in `docs/` (or a small `docs/architecture/`)
     so `CLAUDE.md`'s heavy links stay shallow.
   - Historical session docs grouped under an archive root — propose **by-type**
     (`kickoffs/`, `continuation-prompts/`, `build-plans/`, `brainstorms/`,
     `implementation-prompts/`, `handoffs/`, `post-mortems/`) **vs. by-workstream**
     (`maya/`, `cy/`, `em/`, `flo/`, `t3/`, `sam-bea/`, `orchestrator/` …) and tell
     me which you'd pick for "know which is which" and why. Reuse the existing
     `COMPLETED/` and `OLD/` semantics — don't invent a parallel archive scheme.
   - Keep `anima-test-runs/`, `research/`, `examples/` as-is unless there's a clear
     win.
3. **File-by-file move map.** Every `git mv` source → destination.
4. **Link-impact map.** Every internal link that will break, and where it lives
   (file + line). This is the gating risk — be exhaustive.
5. **Tracked-but-shouldn't-be list.** The 38 leaked `runs/` files (flag any that
   `CLAUDE.md` references so we keep those), any tracked `.DS_Store`, any other junk.
   Mark each `git rm --cached` vs. `keep`.
6. **`.gitignore` diff.** Proposed additions/changes.
7. **Public-readiness checklist** (secrets re-scan result, `.env` history check,
   private-content scan, large-binary note — forward-only, so just *note* the
   bloat, don't act on it).
8. **README proposal.** Recommend adding a top-level recruiter-facing `README.md`
   and outline its sections. Note that I may want to write the prose myself in my
   own voice — offer to draft it but don't assume.

**STOP here. Present the plan and wait for my approval before touching anything.**

## Phase 1 — Reorganize `docs/` (and `prompts/` if needed)

On approval: create the agreed folders, `git mv` every file per the move map, then
**immediately run the link-integrity pass** — grep the repo for every old path and
fix all references in `CLAUDE.md`, `ROADMAP.md`, `PHILOSOPHY.md`, and doc-to-doc
links. Report a before/after broken-link count.

**Gate:** show me `git status`, the move count, and the broken-link count (target:
0). Wait for sign-off.

## Phase 2 — Root & asset cleanup

Tidy loose root files and the `images/` clutter (retired/staging dirs, stray
annotated PNGs) per the plan. Respect documented back-compat symlinks and
load-bearing paths — when in doubt, ask, don't delete. **Gate.**

## Phase 3 — Gitignore & public-readiness execution

`git rm --cached` the approved leaked/junk files (keep them on disk). Apply the
`.gitignore` diff. Re-run the secrets scan and confirm `.env` was never committed.
Produce the final public-readiness checklist with pass/fail on each item.
**Gate — this is the last checkpoint before I flip to public.**

## Phase 4 — README & convention updates

Draft the top-level `README.md` (if I approve in Phase 0) framing anima for a
recruiter: what it is, the 10-phase pipeline, the agent fleet, the engineering
rigor (critics, evals, museum). Then update `CLAUDE.md`'s structure/source-of-truth
sections and append the `CHANGELOG.md` entry per conventions. **Gate.**

## Phase 5 — Verification (do this before telling me it's done)

Run and report results for each — **evidence before claims**:

- [ ] `python -m pytest tests/` green
- [ ] `python -m pytest pipeline/tests/` green
- [ ] Zero broken internal markdown links (run a link-resolution check across all
      `.md` and paste the count)
- [ ] `git status` clean / intentional; `git ls-files runs/` returns nothing for
      untracked files
- [ ] No secrets in tracked files; `.env` confirmed never committed
- [ ] `CLAUDE.md` directory tree + source-of-truth table match the new layout
- [ ] `CHANGELOG.md` entry written

Then give me a final summary and the exact GitHub steps to switch the repo to
public. Do not switch visibility yourself — that's my action.

## Working style

Be a thinking partner: if my proposed taxonomy or any move is wrong, push back with
the reason. Surface trade-offs, don't bury them. Keep me in the loop at each gate.
Prefer `git mv` over delete-and-recreate everywhere.
