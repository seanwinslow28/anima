# Em critic-spine hardening — what broke, what we learned

*2026-06-01. The session that took Em (anima's T2 vision critic) from "shipped at three checkpoints, never scored" to "a scored, segmented baseline against 29 labeled cases, an honest motion-sight path, and — the headline finding — proof that the critic everything downstream trusts has been judging blind." The plan promised a clean six-commit TDD march. What we got was a real baseline, a genuine concurrency incident that nearly killed the live session, four code fixes the plan's stub-green CI couldn't have caught, and one finding big enough to reorganize the next workstream. This is the field report.*

---

## What the session was supposed to be

The plan (`docs/superpowers/plans/2026-05-31-em-critic-spine-hardening.md`) was tight: six commits, two STOP gates, two live runs. Build a two-mode eval harness for Em (CI-green mocked `runner.py` + deliberate live `score.py`), a contact-sheet builder so a still-image judge can see a clip's content-across-time, a `phase_6_motion` honesty clause so she defers what a contact sheet structurally can't show, and a three-way bake-off (Gemini / Sonnet / Opus) to put an evidence-backed default under the T2 seat. Make Em's "100% solid" claim empirical.

The premise was that the fleet's infrastructure had outrun its art: six agent seats shipped, but the critic Act 2's motion QA depends on had never been scored against a labeled defect set, nor could she actually see a video. This session was meant to retire that premise with a number.

What actually happened: the eval got built and run live, the baseline came back with a striking shape, and along the way the session surfaced (a) a second Claude agent executing the *same plan* in the *same working tree*, and (b) the single most important fact about Em — she has no reference image to judge against. The eval did exactly what an eval is for: it found the thing that was wrong.

---

## The baseline came back honest, and a little alarming

The live baseline ran Em as she ships — Gemini 3.1 Pro via `agy` as the default voice, Opus 4.7 via the Claude Agent SDK on escalation — across 29 labeled cases (10 clean, 13 identity/style defects, 6 motion-proper-red), 0 errored.

| Segment | n | precision | recall | **false-pass** | exact-agreement | cites-correct |
|---|---|---|---|---|---|---|
| **Performs** (clean + identity/style) | 23 | 0.62 | **1.00** | **0.00** | 0.57 | 0.43 |
| Motion-proper (expected-red) | 6 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| Overall | 29 | 0.70 | **1.00** | **0.00** | 0.45 | 0.33 |

The load-bearing number is `false_pass_rate = 0.00`: across every segment, Em let through **zero** labeled defects. The costly error — a drifted frame waved to `pass` — never happened. She caught all 13 real identity/style defects (recall 1.00).

The cost shows up in precision (0.62 on the performs segment): Em flagged **8 clean frames**. Four she failed outright (`clean_F13`, `clean_F31`, two head-turn plates); four she softened to borderline. That over-flagging is the whole story of the next section.

---

## Failure 1 — the live baseline aborted with no traceback

The first full `score.py` run died at exit 1 with nothing in the log but an asyncio warning (`Loop … that handles pid … is closed`). No Python traceback, no `last-run.md`, no partial matrix. A single 4-case diagnostic ran clean (so the path worked); the 29-case loop did not.

Two compounding causes, both real:

1. **`score.py` was fragile by one bad case.** Em's `cites_criteria` invariant legitimately *raises* when a model returns a blocking verdict with no citation (e.g. a JSON parse-failure → defensive borderline + empty cites — a documented real mode). One such case in a 29-case loop aborted the whole ~24-minute run with no usable output.

2. **The `agy` subprocess contended on stdin.** `run_antigravity_with_image` spawned `agy` without redirecting stdin; across dozens of sequential calls (made worse by a *second process* also driving `agy` — see Failure 2), the macOS asyncio child-watcher degraded into the no-traceback exit.

**Resolution.** `score.py` is now per-case resilient: each case is caught independently, errored cases are recorded *honestly* (excluded from the matrix, listed explicitly — never fabricated into a verdict), and per-case progress prints so the failure point is always visible (`be82692`). `cli_runners` passes `stdin=DEVNULL` to `agy` (`c5b9dae`). The resilient re-run completed 29/29 with 0 errored.

> **The deepest lesson.** A scoring harness that runs costed, minutes-long live calls must never let one bad case abort the whole run — and it must print where it is. The plan's `score.py` collected all scores in a single list comprehension; the right shape is a resilient loop that degrades to a partial-but-honest matrix.

---

## Failure 2 — a second agent was executing the same plan in the same tree

This is the headline. Midway through, the working tree started changing under me: `vision_critic.py` and `score.py` showed edits I didn't make, then two commits I never ran appeared in the log — `5f45ec5` (Task 8, invoke_sonnet_vision) and `379fdfa` (Task 9, the bake-off harness) — authored "Sean Winslow" (the machine's git identity) with the plan's **exact verbatim** commit messages. Plus `agy_test.log` junk and a bake-off `results.md`.

Sean confirmed he wasn't working in parallel. The forensics were unambiguous:

- `git reflog` showed `5f45ec5`/`379fdfa` as `commit:` operations on **this working copy's HEAD** at 06:27–06:28 — i.e. committed *through this same `.git`*, during my session, by something that wasn't me.
- `ps` + `lsof` showed **five+ `claude` processes with `/Code-Brain/anima` as cwd** — a second session (PID 17151, from the prior evening) plus the rogue executors that had since exited.

A second agent on one shared working tree is silent corruption waiting to happen: two writers moving one HEAD, editing the same files. It also explains Failure 1 — the rogue was editing `cli_runners.py`/`vision_critic.py` and hammering `agy` *underneath* my baseline.

**Resolution.** Sean authorized killing the stale sessions. The dangerous part: when I walked the process tree to find what to kill, **my own session was PID 78328** — the exact PID I'd flagged as most suspicious (it started 5:54 AM, four minutes before I cut the branch). Killing it would have ended the conversation. After confirming 78328 was the ancestor of my shell, I killed only the lingering rogue anima session (17151), left the unrelated `code-brain` sessions alone, and verified I was the sole `claude` process in the repo. Per Sean's call, the rogue's Task 8/9 commits were **kept** (they matched the plan verbatim and the suite was green) after I verified them (18 + 1 tests, correct refactor, no escalation in the bake-off); its junk + bake-off output were deleted; its other uncommitted edits were reviewed and adopted (they were genuinely good — see below).

> **The deepest lesson.** Never run two agents against one working tree. Plan execution should happen in an isolated git worktree (or a dedicated clone) so a stray session can't move your HEAD. And operationally: **always identify your own PID before killing anything** — walk `ppid` from `$$` up to the `claude` ancestor. I was one authorized `kill` away from terminating the session that was doing the work.

---

## Failure 3 — `--stub` didn't actually stub (plan code vs. plan intent)

The plan's prose said `score.py --stub` "forces the credential-free path" (Mo's `--no-sonnet` discipline). The plan's *code* only relabeled the output — on this machine, where `agy` + the SDK are both present, `--stub` would have fired **live, costed** calls while printing "STUB." The Step-4 smoke test would have been meaningless and quietly spent money.

**Resolution.** `--stub` now genuinely forces the credential-free path: it patches Em's two runner references with a deterministic stub before scoring (`be82692`), so the matrix is honestly degenerate and labeled STUB.

> **The deepest lesson.** An opt-out-of-cost flag has to actually opt out — verified on a machine where the real path is available, not just where it isn't. A relabel is not a safeguard.

---

## Failure 4 — the bake-off couldn't run as documented

`bakeoff.py`'s docstring said to run it as `python evals/bakeoffs/.../bakeoff.py`, but run as a script, the repo root isn't on `sys.path`, so `from evals.vision_critic… import` died with `ModuleNotFoundError: No module named 'evals'`. (This is almost certainly what the rogue's `agy_test.log` debugging was chasing.)

**Resolution.** A run-as-script bootstrap inserts the repo root (`parents[3]`) onto `sys.path` before the `evals.*` imports, so the documented command works. (Committed alongside the bake-off run.)

> **The deepest lesson.** A script in a dated, non-package directory either needs a `sys.path` bootstrap or has to be run with `-m`/`PYTHONPATH`. The plan generated the harness but never ran it as written, so the gap shipped.

---

## The finding that reorganizes the next workstream — Em is reference-blind

The 8 false alarms weren't noise; they were a symptom. Tracing what Em actually receives:

`VisionCriticNode.run()` attaches exactly **one** image — the frame under review (`image_paths=[model_image_path]`). She is shown **no `anchor.png`, no Bible plate, no A-2, no prior approved frame, no side-by-side.** Everything she "compares to" is *text*: her standing context, the `default_context_files` (PHILOSOPHY.md, CLAUDE.md — where the HF/SF/CC gate codes live, docs/pipeline-architecture-v1.md), and the one-line `beat_description`. She doesn't even load `acceptance_criteria.json` — `ctx.criteria` is never read.

The kicker: her own addendum *trains her to reason about an anchor she can't see* — "the A-2 anchor and F18 both read closer to 65°… SF02 identity-drift." She is prompted to compare against a reference that is never attached.

This explains the baseline's exact shape:

- **Recall 1.00 makes sense:** gross breaks (head-to-body 1:4 vs the *written* 1:7 rule, a fully-rounded jaw, a missing stylus) are catchable from text rules + measuring the image.
- **Precision 0.62 makes sense:** without the anchor, Em has no way to *confirm* "this IS correctly Sean → pass." She flags on whatever text-rule she can measure off the pixels (HF01 16:9; SF05 expression-vs-beat). Sean looked at the two frames she failed hardest — `clean_F13` and `clean_F31` — and confirmed they are unmistakably the correct Sean. Her "fail" there is **reference-blindness, not a bad frame.**

Sean's labels were ratified unchanged; the 0.62 is the honest reference-blind number; and giving Em reference images is now the **locked #1 next fix** (`docs/anima-test-runs/2026-06-01-em-reference-blindness-FINDING.md`).

> **The deepest lesson.** The eval did its job. We built the ruler, and the ruler found that the critic has been grading without the answer key. No amount of model-swapping fixes a critic asked to compare against an anchor it isn't given. This is, almost certainly, worth more than the entire bake-off — and it sits next to a known-adjacent gap: Em also doesn't load the merged `CriteriaBundle` (the open case-7 xfail from the Cy-Bibles session). The fix is one shape: **give Em the Bible — its reference plates AND its `IR.*`/`AC.*` criteria — as inputs.**

---

## What worked exactly as designed — the motion-sight honesty clause (STOP GATE 2)

Run live on the W1 walk contact sheet (`phase_6_motion`, escalated to Opus), Em returned **`fail` @0.78** and reasoned precisely as the design intends:

- **Caught (content across time):** *"The break is the right-side set dressing… director's chair at t0–t1, a Wacom-on-stand at t2, a wooden mannequin at t3, a different pose at t4, a smaller mannequin + sketchbook at t5. The classic Seedance background-regeneration failure mode — the model locks the subject and re-invents the background each frame."* A real, shippable defect a per-frame review would miss.
- **Deferred (the structural limit, named):** *"On 'watch line stability': that is a temporal-proper concern (line crawl, boil, jitter) and a contact sheet cannot show it. I am explicitly deferring line-stability to a human review of the clip itself or a deterministic temporal-coherence pass; I will not guess past what the strip shows."*

An elegant consistency: continuity-*across-the-strip* (does the prop stay the same prop) is self-referential — the strip is its own reference — so Em catches it even while reference-blind. It's identity-*vs-the-canonical-Sean* that needs the anchor. The two findings don't contradict; they partition cleanly.

The six motion-proper-red cases in the suite confirm the segmentation works: Em flagged them on style grounds and **never** cited a motion criterion (cites-correct 0.00 there), i.e. she does not pretend to see motion. Ships-red, by design.

---

## The rogue's code was good — adopted after review

Per Sean's "keep 8/9, verify; decide the rest per-file," the rogue's uncommitted edits were reviewed and — surprisingly — all kept, because they were clean, tested, and beneficial:

- **`cli_runners.py` `stdin=DEVNULL`** — the agy-subprocess robustness fix (above).
- **`vision_critic.py` video block + `tests/test_vision_critic_video.py`** — `run()` auto-builds a contact sheet when `image_path` is a clip, reviews it, cleans it up; backward-compatible (a pre-built `.png` sheet takes the prior path); contract untouched; properly tested. Lines up with the deferred Phase-6 live-wiring.
- **`bakeoff_lib.py` concurrency** — `score_config_async` with `asyncio.gather` + a `Semaphore(5)` cap, turning the bake-off from ~87 sequential calls into a tractable run.

A pre-existing breakage also surfaced and was fixed in passing: `evals/character_designer/runner.py` was monkeypatching `invoke_nb_pro`, renamed to `invoke_image_edit` on 2026-05-30 — 4 dead tests, now green (`ccc24a6`).

---

## What we learned

- **Two agents, one working tree, is silent corruption.** Isolate plan execution in a git worktree; detect concurrent sessions early (`reflog` `commit:` entries you didn't author; `lsof`/`ps` by cwd). And always resolve your own PID before you kill.
- **An eval's job is to find what's wrong — and it did.** The headline output of this session isn't the 0.62; it's *why* it's 0.62. Building the measurement instrument is what made the reference-blindness flaw visible, quantified, and confirmable against Sean's eye.
- **A reference-free critic can catch gross breaks but can't license a pass.** Recall came from text rules; precision needs the anchor. Give the critic the answer key.
- **Costed live harnesses must be per-case resilient and loud about progress.** One bad case can't be allowed to torch a 24-minute run, and silence is the enemy of debugging a slow loop.
- **Opt-out-of-cost flags must actually opt out** — verified where the real path *is* available.
- **Scripts in non-package dirs need a path bootstrap or `-m`** — and the only way to know is to actually run them as documented.
- **The honesty clause is the right pattern.** Telling the model what it cannot see, and to defer rather than guess, produced exactly the behavior we wanted on a real clip — and kept a shuffled-frame guess from laundering into a motion verdict.
- **Live latency is a real design constraint.** ~25–80s/case (Gemini + Opus escalation); the full 29-case baseline is ~24 minutes. Run live scorers in the background; concurrency (with `stdin=DEVNULL`) is what makes the bake-off feasible.

---

## What landed on disk

| Commit | What |
|--------|------|
| `542a787` | docs: conservative CLAUDE.md optimization pass (standalone, pre-existing edits) |
| `bda0fd5` | **Commit 1** — contact-sheet builder + Em `phase_6_motion` honesty clause |
| `0ab6e2d` | **Commit 2** — Em eval suite (scoring.py, cases.yaml, conftest, runner, score.py, failure-modes) |
| `5f45ec5` | Task 8 — `invoke_sonnet_vision` (rogue session; verified + kept) |
| `379fdfa` | Task 9 — three-way bake-off harness (rogue session; verified + kept) |
| `ccc24a6` | fix — char_designer eval runner (`invoke_nb_pro` → `invoke_image_edit`) |
| `c5b9dae` | feat — Em reviews raw clips via auto contact-sheet + `agy` stdin hardening |
| `be82692` | fix — `score.py` per-case resilience + real `--stub` + dotenv |
| `021a9ba` | perf — concurrent bake-off scoring |
| `af7950d` | eval — lock case labels + scored baseline + reference-blindness FINDING |
| *(uncommitted)* | `bakeoff.py` run-as-script `sys.path` bootstrap — commits with the bake-off run |

Test suite at the time of writing: `tests/` **242 passed** (231 baseline + the motion-sight, eval-suite, sonnet-vision, video, score-report, and bake-off-dispatch additions). Eval suite `evals/vision_critic/runner.py`: 30 passed + 6 xpassed (the red motion cases). Live spend: roughly one baseline (~$2–3, subscription-absorbed); the bake-off had not yet completed a clean live run (first attempt = the import bug, now fixed).

---

## How to proceed (next session, in priority order)

1. **Reference-images for Em — the #1 fix.** Attach the anchor + relevant Bible plate(s) (and, while there, load the merged `CriteriaBundle` — `ctx.criteria` — closing the open case-7 xfail from the Cy session). Add a `references:` field to `cases.yaml`, wire the harness, **re-run the baseline**, and measure the precision lift (recall should hold, false alarms should resolve). The pre/post delta is the portfolio artifact — the moment Em stopped grading blind. Spec: `2026-06-01-em-reference-blindness-FINDING.md`. Do it in an **isolated worktree**.
2. **Finish Task 10 — the live bake-off.** The harness is fixed (concurrency + `sys.path` bootstrap); run `evals/bakeoffs/2026-05-31-t2-vision-critic-gemini-vs-sonnet-vs-opus/bakeoff.py`, write the Decision section per the metric contract (precision/recall/false-pass on performs; cites-correct; confidence-vs-correctness; wall-time; pinned model snapshots), commit. Note: all three models are *equally* reference-blind today, so the comparison is valid as a relative read but should be re-run once references land.
3. **Task 11 wrap.** CHANGELOG entry; CLAUDE.md Em row → "validated, with a known reference-blindness gap"; this post-mortem is the field report. Confirm final test count vs the 231 before-number.
4. **Operational hygiene.** Adopt worktree isolation for plan execution; add a quick "am I the only agent in this repo?" pre-flight; consider making the orchestrators loud about stub-fallback (the same lesson the Cy session reached).
5. **The motion-proper metric (E_warp/VBench)** stays deferred; the 6 red motion cases are its ready-made validation set. The human seam covers it now (STOP GATE 2 proved Em defers it honestly).
