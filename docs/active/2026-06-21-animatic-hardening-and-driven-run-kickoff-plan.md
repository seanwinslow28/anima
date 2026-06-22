# Part 2 — Drive the costed Spark-animatic run (close DoD #6)

## Context

Part 1 (two bug fixes — validate `impact_tags`, the human owns the frame count) already
shipped: **PR #63 squash-merged to `main` as commit `7c61278`.** This session is the
*costed, end-to-end driven run* that proves the ANIMATIC stage on a real loop and closes
**ROADMAP DoD #6** — the one open item under TOP-1 Animatic ("a costed run exercising the
new stage end-to-end that ships a loop whose placement holds").

The run exercises Sean's 7 hand-drawn placement roughs against the now-built ANIMATIC
ingest, so NB2 respects placement *before* it draws each frame. The bar to beat is the
2026-06-18 5-frame run, which drifted: **mascot on the wrong shoulder, inconsistent scale,
2↔4 leg count.** This is the only spend (Gemini-metered: NB2 stills + Em).

**Operating model (load-bearing):** *I* run every command, read every traceback, copy
files, curate the board mechanically, and handle retries. **Sean makes only the taste
calls** — plan approval, script approval, storyboard sign-off, and each per-frame
approve/retry. At each gate I *present* (artifact/image + Em's read) and *wait*. I never
auto-approve a frame. Em is **not calibrated** (that's the next workstream) — her verdicts
inform, they do not decide.

---

## Critical pre-flight finding (verified, not assumed)

The current working tree is on branch `repo-reorg-public-readiness` @ `cc0608f`, which
**does not contain Part 1** — `--frames` is absent here, present only on `origin/main`
(`7c61278`, verified ancestor). Sean's checkout also has uncommitted/untracked work.

⇒ **Isolation is a fresh git worktree off `origin/main`** (the prompt's preferred path).
Never stash/clobber Sean's branch. Verified on `origin/main`:
- `--frames N` at [pipeline/run.py:80](pipeline/run.py#L80); threaded as `target_frames` (line 235).
- Count gate `_enforce_frame_count` at `pipeline/orchestration/storyboard_stage.py:94` —
  refuses to lock a board whose frame count ≠ target, message: *"board has {n} frame(s)
  but the target loop length is {target} (--frames {target}) — curate … (the human owns the count)."*
- Both md5 guards on `origin/main` match (`2af75906…`, `945af824…`).
- ANIMATIC ingest contract: roughs named `F<id>.<ext>` (regex `^F(\d+)\.(png|jpg|jpeg)$`,
  padding-insensitive), optional `holds.json`; `--approve-animatic` ingests into run-state,
  never mutates the board; confirms *"ingested N placement rough(s)…"*.

**Worktree asset hygiene (because these are gitignored/untracked → absent from the worktree):**
- **`.env`** — copy into the worktree (run needs `GEMINI_API_KEY`).
- **Brief** — tracked on `origin/main`, so it lands in the worktree automatically. ✓
- **7 roughs** (`images/final-animatic-test/frame-1.png … frame-7.png`, untracked) — copy from
  the main checkout's absolute path into `<RUN>/animatic/` at the ANIMATIC gate (rename
  `frame-N.png → F0N.png`). The `F-named/` subdir is empty (.DS_Store only) — ignore the
  kickoff's stale `cp …/F-named/…` command; use the rename loop.
- **Baseline GIF** (`runs/2026-06-18-spark-authored-run/export/spark-authored.gif`, gitignored)
  — reference by absolute path from the main checkout at comparison time; no copy.

---

## Step 0 — Isolation + pre-flight (NO spend)

1. Create the worktree off `origin/main` (via the `superpowers:using-git-worktrees` skill;
   fallback native):
   ```
   git worktree add -b spark-animatic-driven-run /Users/seanwinslow/Code-Brain/anima-spark-run origin/main
   cp /Users/seanwinslow/Code-Brain/anima/.env /Users/seanwinslow/Code-Brain/anima-spark-run/.env
   ```
   Run all subsequent commands from the worktree root (absolute paths; avoid `cd` in compound commands).
2. Verify in the worktree (all read-only): `git log --oneline -1` shows `7c61278`;
   `python -m pipeline.run --help | grep -- --frames` prints the flag; the two md5 guards
   match; `echo ANTHROPIC=${ANTHROPIC_API_KEY:-ABSENT}` → **ABSENT**; `grep -q GEMINI_API_KEY .env`.
3. Confirm the chosen run-dir is free: `runs/2026-06-21-spark-animatic-driven` (the cancelled
   `runs/2026-06-21-spark-animatic-run` won't exist in the fresh worktree, but pass `--run-dir`
   explicitly anyway).

**Throttle/long-call handling:** Maya/Sam/Bea are live authoring calls (~350s each,
`*_CALL_TIMEOUT_S` 1200s; up to 3 Maya calls). The foreground Bash ceiling is 10 min, so
**run every costed orchestrator command in the background and monitor to completion** — this
survives the long calls without killing a paid subprocess. PLAN is the throttle canary
(below).

---

## Step 1 — Start the run (FIRST spend; PLAN = throttle canary)

```
python -m pipeline.run \
  --brief briefs/2026-06-16-spark-authored \
  --slug spark-animatic --animatic --frames 7 \
  --run-dir runs/2026-06-21-spark-animatic-driven
```
(background + monitor). This runs the api-key guard → the `smoke_live_opus` canary → drafts
Maya's plan → post-scans for the `STUB FALLBACK` marker.

**Canary rule:** if the smoke raises `GuardError` (SDK/auth down) or the plan stalls past its
timeout, **STOP and report the wall-clock + the honest failure — do not work around it by
stubbing** (no `--stub`, no `--skip-smoke`). If PLAN finishes as a *real* plan (no stub
marker; gate prints "plan drafted"), nesting is fine → proceed.

---

## Step 2–7 — Drive the gates (present → WAIT for Sean → advance). Run dir = `<RUN>`.

**2. PLAN (Maya).** Present `<RUN>/brief/plan.md` + the cost preview. On Sean's go:
`python -m pipeline.run --resume <RUN> --approve-plan`.
(Part-1 Fix A: an illegal `impact_tag` fails at authoring/lock with the legal-set message —
**re-run Maya, never hand-patch the criteria.**)

**3. SCRIPT (Sam).** Present `<RUN>/brief/script.md` + `beats.json`. On go:
`--approve-script` (auto-runs Bea, pauses at the storyboard gate).

**4. STORYBOARD (Bea, 7 frames).** Present `<RUN>/brief/shots.yaml`. **I curate** to a clean
7-frame loop: ids `1..7` strictly ascending, every beat covered, the closing frame a
**frame-1 match carrying `chain_from: 1`** (loop-return). The count gate enforces exactly 7 —
if Bea's board ≠ 7 it's refused; I curate then re-approve. On Sean's sign-off:
`--approve-storyboard` → routes to ANIMATIC (gate prints "Board has 7 frame(s).").

**5. ANIMATIC (placement).** The stage created `<RUN>/animatic/`. Copy-rename the 7 roughs in:
```
for n in 1 2 3 4 5 6 7; do
  cp /Users/seanwinslow/Code-Brain/anima/images/final-animatic-test/frame-$n.png <RUN>/animatic/F0$n.png
done
```
Confirm 7 files land; eye each rough against board frame N with Sean. On go:
`--approve-animatic` (expect "ingested 7 placement rough(s)"; enters GENERATE, fans frame 1).

**6. PER FRAME (the eye gate).** For each generated frame: **Read the candidate PNG** it names
(so Sean sees it in the IDE) and relay **Em's verdict + reasoning + proposed-fix summary**
(the gate prints all three). **Wait for Sean.**
- Approve: `--approve-frame N` (chains + fans N+1, or assembles after the last).
- Correct: `--retry-frame N --note "<desired end-state>"` — write the note as a *positive
  identity/placement lock* (it's appended to the prompt; naming the defect reinforces it).
- **Never approve on my own judgment.** Repeat to DONE → loop assembles under `<RUN>/export/`.

---

## Step 8 — Close DoD #6

1. **Before/after:** put `<RUN>/export/<loop>.gif` beside the absolute-path baseline
   `runs/2026-06-18-spark-authored-run/export/spark-authored.gif`. Eye it **with Sean**: does
   placement now hold where 06-18 drifted — mascot on the correct shoulder, consistent scale,
   stable leg/limb count?
2. **Write** [docs/anima-test-runs/2026-06-21-spark-animatic-run-post-mortem.md](docs/anima-test-runs/2026-06-21-spark-animatic-run-post-mortem.md):
   spend (Gemini $), retries per frame, the before/after read, whether `--frames 7` made the
   count Just Work, the throttle finding, any new seams.
3. **Only on a clean run** (placement holds, loop ships): edit [ROADMAP.md](ROADMAP.md) — mark
   TOP-1 Animatic ✅ (DoD #6 met), advance Current Focus to **workstream 2 (Tier-2 Em
   calibration)**. Per the anti-drift contract, **not before.** Add a [CHANGELOG.md](CHANGELOG.md) entry.
4. Commit the **doc updates only** (post-mortem + ROADMAP + CHANGELOG) on the worktree branch
   (`spark-animatic-driven-run`, off `main`) and open a PR to `main`. Run output under `runs/`
   stays gitignored. Commit trailer: `Co-Authored-By: Claude Opus 4.8 (1M context)
   <noreply@anthropic.com>`; PR body ends with the Claude Code generated-with line.

---

## Verification / acceptance

- The driven run shipped a **7-frame** Spark loop whose **placement holds** (before/after
  beats the 06-18 drift) — and every plan/script/board/frame decision was Sean's eye, not auto.
- Post-mortem written; ROADMAP advanced **only if clean**; **both md5 guards intact**
  (re-check at the end).
- Final report to Sean: total spend, retries, the DoD #6 verdict, the throttle finding, any
  seam that fought us.

## Risks / hard stop conditions

- **SDK/auth (throttle canary):** smoke `GuardError` or a stalled authoring call → STOP +
  report honestly; never stub around it.
- **Illegal `impact_tag` from Maya** → re-run Maya (Fix A surfaces it); don't hand-patch.
- **Board ≠ 7 frames** → curate to exactly 7, then re-approve (count gate refuses otherwise).
- **md5 guards** — touch neither file; re-verify at close.
- The deeper "animatic natively defines frame count" fix and the frontend stay **parked**.
