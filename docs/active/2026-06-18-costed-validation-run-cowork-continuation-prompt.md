# Cowork continuation prompt — Drive the Tier-1 costed validation run of "The Spark, Shared"

*Paste this whole block into a fresh Cowork session opened on the `anima` repo. It is the standing brief for the session. Your job is to be Sean's co-pilot while **he** drives a real, money-spending fleet run in his terminal — interpreting outputs at each gate, fixing artifacts when needed, and capturing the data the next phase needs.*

---

You're picking up a long-running build in **anima** — Sean's 2D-animation pipeline made by a human plus a fleet of named agents. The whole fleet is built and wired; a first live end-to-end run already shipped a loop; a two-slice round of fixes (Tier 1) just landed. **This session drives the costed *validation* run that proves those fixes against live models and harvests the data for the next phase.** This is not a $0 planning session — Sean will spend real (modest) model budget, driving each step himself in a plain terminal, and you help him read and decide at every gate.

## First: read these, in this order (do this before anything else)

The session must understand what anima is, what we're trying to accomplish, and exactly what this run is testing. Read:

1. **`PHILOSOPHY.md`** — the load-bearing thesis. The human owns taste, story, timing, and the decision to ship; the agents own what's cheap, parallel, structured. The north star behind *this* run: get anima to a place Sean can **trust enough to step away from while it creates.** We are not there yet — and this run is a measured step toward it.
2. **`CLAUDE.md`** — the fleet manual + the Skills Map (every built agent: Maya planner, Cy character-designer, Sam scriptwriter, Bea storyboard-artist, Flo frame-router, Em vision-critic, Mo museum-writer, the T3 council, the orchestrator). Skim the Key Commands → "the run orchestrator" section.
3. **`docs/anima-test-runs/2026-06-17-spark-authored-costed-run-post-mortem.md`** — *the most important context.* The first live run's findings: the pipeline works human-in-the-loop, but it surfaced five issues, and the headline one is **Em (the vision critic) is mis-calibrated to Sean's eye in both directions** — that's the real blocker to autonomy. Read the Em-vs-eye table and §4 (the path to "step away").
4. **`docs/anima-test-runs/2026-06-17-bea-prompt-quality-field-report.md`** (Tier 1 Slice A) and **`docs/anima-test-runs/2026-06-18-tier1-slice-b-field-report.md`** (Tier 1 Slice B) — what the fixes actually changed, and the hypotheses this run tests.
5. **`docs/2026-06-16-spark-authored-costed-run-runbook.md`** — **THE procedure.** The gate-by-gate commands Sean runs. (Its pre-flight already has the venv-activation + `ANTHROPIC_API_KEY`-unset fixes, and its Gate-5 example + troubleshooting were corrected in Slice B.) This run follows it.
6. **`docs/pipeline-architecture-v1.md`** §Phase 5 GENERATE + §The Critic Stack — so you can interpret the eye gate (T1 rule gates + Em the T2 vision critic).
7. **`pipeline/orchestration/shots.py`** — the `shots.yaml` schema (slug + frames[{id, beat_id, cast, beat, prompt, extra_references, chain_anchors, hold, chain_from}], top-level `locked`). You'll read/curate this file during the run.
8. **`docs/research/2026-05-30-nb2-editing-character-consistency-template.md`** — the NB2 editing physics (terse-edit-beats-verbose, positive identity-lock, name-the-fix-not-the-defect). This is what you lean on when a frame drifts and Sean needs a better prompt or retry note.
9. **`briefs/2026-06-16-spark-authored/00_studio_brief.md`** — the piece being made (Sean at his desk, the Claude mascot on his shoulder, a 5-keyframe pencil-test loop). And **`docs/fleet-ops-protocol.md`** — the costed-run discipline (subscription billing, plain terminal, single owner, clean state).

For comparison, the first run's output + evidence are at `runs/2026-06-17-spark-authored-run/` (gitignored, local-only): the shipped loop (`export/spark-authored.gif`), the Em verdict trail (`em_verdicts.jsonl`), and the curated `brief/shots.yaml`. Useful as the baseline this run is measured against.

## How we work (standing doctrine — internalize this)

- **Verify against the tree, never trust a label — including this prompt and any doc.** Use the `mcp__workspace__bash` shell to check git state, read real code, run the actual validators, and confirm claims before asserting. Cautionary tales that earned this rule across this project: a runbook claimed a loop "self-isolates" and the run crashed on case #0; a docstring lied about `agy -m`; a kickoff's "the anchors are clean" was false on arrival (they carried production labels); `--stub` once silently spent real money. Assert before you spend.
- **Two standing guards must never move.** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` must stay `2af75906502f1caf8857e18828ceb2e4` (Em's eval baseline). `md5sum pipeline/agents/prompts/sean-screenwriting-voice.md` must stay `945af824fa53b948a18ac6bf206d67ef` (Sam/Bea's shared voice instrument). This session touches neither — but check them if anything edits the tree.
- **Sean drives; you co-pilot.** The whole reason the first runs felt opaque is that Claude Code was running agents in the background. **Do NOT run the orchestrator or spend money for him.** Sean runs each `python -m pipeline.run …` command himself in his terminal and pastes you the output; you interpret it, read the artifacts, fix YAML/prompts when he asks, advise approve-vs-retry, and capture the labels. The spend and the gate decisions are his.
- **When you edit an artifact for him, write valid YAML.** Last run, hand-pasting a prompt containing `ONLY CHANGE:` broke the `shots.yaml` parse (a bare `:` is a YAML mapping). If Sean wants a prompt changed, *you* write it into the file with a folded `>-` block (or via `python -m pipeline.cli storyboard mutate`), then verify it parses with `load_shots` before he re-runs. Never hand him raw text with a colon to paste.
- **Use AskUserQuestion** for genuine forks (e.g., accept-a-close-frame vs retry, which brief). **Keep responses concise and direct** (Sean's stated preference — give the "why," don't over-explain). Sean is a PM who digs into the "how"; respect that. Use TaskCreate/TaskUpdate to track the run's gates if helpful.

## Where the repo is right now

Branch `main`, HEAD `a287ef2` (Slice B prep docs, on top of #60 Slice B build) — verify with `git log --oneline -3`; if Sean has merged more by the time you read this, HEAD will be newer. **Tier 1 is complete.** The named fleet is complete and wired into `python -m pipeline.run` (`PLAN → SCRIPT → STORYBOARD → GENERATE → ASSEMBLE`). The suite is green credential-free (665 in `tests/` + `pipeline/tests/` 10 at last check).

## The active work — drive the costed validation run

This run has a **dual purpose**, and you should hold both the whole way through:

**Purpose 1 — prove Tier 1 against live models.** Everything in Tier 1 was verified against *stubs*. This run is the first time real Sonnet (Bea) + real NB2 (Flo) + real Em touch it. The hypotheses to test, each tied to a fix:
- *Bea's edit-frame prompts land terse* (Slice A): frames 2–N should open `Same fixed two-shot … ONLY CHANGE: …`, so Sean needs **far fewer curation edits** than the first run (which needed all four of frames 2–5 rewritten by hand). This is the headline "did curation cost drop" signal.
- *No text bleed* (Slice A): no `A-2` / `A-7` / `C-B` production labels should appear in any generated frame (the reference assets were cleaned + the no-text negative added).
- *The loop-return holds* (Slice B): frame 5 should chain off frame 1 (`chain_from: 1`) and be authored as "composition identical to frame 1" — so it should **not** put up the three-attempt fight it did last time.
- *The eye gate is legible* (Slice B): on a borderline/fail verdict the gate now prints **Em's reasoning + her proposed patch**, not just a verdict. Sean reads that before deciding.

**Purpose 2 — harvest the Em-vs-eye labels for Tier 2.** This is the data that lets us eventually close the autonomy gap. At **every eye gate**, Em now shows her verdict + reasoning. Note, per frame, whether Sean **agrees** with Em or **overrides** her — and *why* on an override (that rationale is the richest calibration signal, and it's only in Sean's head unless captured). The logs pair Em's verdict with which attempt Sean approved (`em_verdicts.jsonl` + the approvals trail), but the agree/override *reasoning* is what you help capture live.

### The run, in brief (full detail in the runbook)

Sean drives, in a plain terminal, venv active, `ANTHROPIC_API_KEY` unset. The authoring brief already exists and can be reused; today's date gives a fresh run dir automatically (no collision with the 06-17 run):

```
python -m pipeline.run --brief briefs/2026-06-16-spark-authored --slug spark-authored
```

Then gate by gate, each its own `--resume` command: **plan gate** (`--approve-plan`, Maya plans) → **script gate** (`--approve-script`, Sam writes beats) → **storyboard curation gate** (`--approve-storyboard`, Bea boards → Sean curates `shots.yaml`) → **per-frame eye gates** (`--approve-frame N` / `--retry-frame N --note "…"`, Flo generates + Em critiques) → auto-assemble. Your co-pilot job at each: open and read the artifact Sean points at (`run_dir/brief/plan.md`, `script.md`, `beats.json`, `storyboard.md`, `shots.yaml`, `maya_raw_pass1.txt` / `sam_raw.txt` / `bea_raw.txt`, the candidate PNGs, `em_verdicts.jsonl`), tell him what you see, and help him decide. On a frame that drifts, read Em's surfaced reasoning first, then write a **positive, identity-locked** retry note (assert the desired end-state; never name the defect — it's appended as `CORRECTION:` and reinforces).

### The known traps (from the last run — help Sean avoid them)

- **macOS:** `source .venv/bin/activate` first (no bare `python` otherwise); `unset ANTHROPIC_API_KEY` (subscription billing — the run refuses otherwise). Re-do both in any new terminal tab.
- **Never pass `--stub`** — that's the $0 offline smoke; this is the real run.
- **YAML edits go through you, as folded blocks, verified with `load_shots` before re-run.** Don't hand Sean colon-bearing text to paste.
- **Retry notes assert the fix, not the flaw.** And remember Sean's shirt is *supposed* to be a deep navy (`#243044`) — "it's blue" was a misleading complaint last time.

### Cost reality

Authoring (Maya/Sam/Bea, Opus + Sonnet) is **$0 incremental** (subscription). The only metered spend is **Gemini** (the 5 NB2 frames + Em's reads), roughly **$0.35–$2.25**, scaling with retries. Modest.

## What to produce when the run is done

1. **A Tier-1 validation post-mortem** (`docs/anima-test-runs/<date>-tier1-validation-run-post-mortem.md`) — grounded in the run's evidence: did curation cost actually drop (count Sean's hand-edits vs the first run's four)? Any text bleed? Did the loop-return hold first-try? Plus the **Em-vs-eye label table** (verdict vs Sean's approve/override, per frame/attempt, with override rationale) — the deliverable that feeds Tier 2.
2. **Then tee up Tier 2 — the Em calibration campaign** (the autonomy core): converge with Sean on the calibration method using the harvested labels, and write the plan + kickoff in the established rhythm (Cowork plans $0 → Claude Code executes under fleet-ops → field report → verify).

## Immediate first action

Confirm you've read `PHILOSOPHY.md` + `CLAUDE.md` + the first-run post-mortem + both Tier-1 field reports + the runbook. Verify HEAD / `git status` / both md5 guards against the tree. Then tell Sean you're caught up and ready to co-pilot, restate the two purposes of this run in a sentence each, and point him at the first command (the pre-flight + the start command from the runbook). From there, walk him gate by gate — he runs, you read and advise, and you capture the Em-vs-eye signal as you go.
