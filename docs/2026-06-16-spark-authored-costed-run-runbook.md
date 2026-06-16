# Runbook — "The Spark, Shared," authored by the fleet (the first live end-to-end run)

*Dated 2026-06-16. This is **yours to drive** — you run each command in a plain terminal opened in the
`anima` project folder, one gate at a time, reading the output as it happens. Do **not** hand this to
Claude Code to run in the background (that's why you've only been seeing final results). The whole
point is that you see the process unfold and hold every gate yourself.*

---

## Step 0 — land the pre-run hardening first

This runbook assumes the raw-dumps + gate smokes from
[`docs/2026-06-16-costed-run-prep-kickoff.md`](2026-06-16-costed-run-prep-kickoff.md) are merged and
pulled. They give you `sam_raw.txt` / `bea_raw.txt` (the raw model output, for under-the-hood
visibility) and make the script/storyboard gates fail *before* spending if auth is broken. Land that
PR, `git pull`, then come back here.

## What you're about to do

Run the whole fleet on one small piece, live, for the first time: **Maya plans → Sam writes the script
→ Bea boards it → you curate → Flo generates 5 frames → Em critiques each → FFmpeg assembles the loop.**
You stop at four kinds of gate and decide at each. The agents only propose.

**Billing:** Maya/Sam/Bea (Opus + Sonnet) run on your Claude subscription = **$0 incremental**. The only
metered spend is **Gemini** (the 5 NB2 frames + Em's reads) ≈ **$0.35–$2.25**, scaling up if frames need
retries. **Wall-clock:** roughly 30–60 min, mostly waiting on the authoring calls (Opus runs a few
minutes each) — paced by your reviews.

---

## Pre-flight (once)

```bash
cd /Users/seanwinslow/Code-Brain/anima            # open your terminal HERE

# 1. Be synced to main (after the hardening PR merged)
git fetch origin && git status -sb | head -1      # expect: ## main...origin/main (clean)

# 2. Subscription billing — Opus/Sonnet must NOT hit the metered API.
unset ANTHROPIC_API_KEY
echo "${ANTHROPIC_API_KEY:-ABSENT}"               # expect ABSENT (the run refuses to start otherwise)

# 3. Confirm the Gemini key is present (NB2 + Em — the only metered spend)
grep -q "GEMINI_API_KEY" .env && echo ".env has GEMINI_API_KEY" || echo "MISSING — add it before running"

# 4. Confirm you're logged in for the subscription-billed agents
claude --version                                   # and that `claude` is logged in (claude login)
```

Then **create the authoring brief** — a fresh dir holding *only* the studio brief (no `shots.yaml`, no
`plan.md`), which is what makes the orchestrator run the full Maya→Sam→Bea chain instead of skipping to
GENERATE:

```bash
mkdir -p briefs/2026-06-16-spark-authored
cp briefs/2026-06-10-spark-shared/00_studio_brief.md briefs/2026-06-16-spark-authored/00_studio_brief.md
ls briefs/2026-06-16-spark-authored/               # expect ONLY 00_studio_brief.md
```

---

## The run, gate by gate

### Gate 1 — START → Maya plans

```bash
python -m pipeline.run --brief briefs/2026-06-16-spark-authored --slug spark-authored
```

This smokes Opus, then **Maya** authors the plan + the acceptance-criteria rule graph, and stops at the
plan gate. **Copy the run-dir path it prints** into a shell variable so every later command is clean
(it'll be `runs/2026-06-16-spark-authored-run` if you run today):

```bash
RUN=runs/2026-06-16-spark-authored-run            # paste the EXACT path START printed
```

**Review** (this is the "see under the hood" part):

```bash
open "$RUN/brief/plan.md"                          # Maya's plan
open "$RUN/brief/acceptance_criteria.json"         # the AC.*/IR.* rules Em will check frames against
open "$RUN/maya_raw_pass1.txt"                     # Maya's RAW Opus output
python -m pipeline.cli plan show --plan "$RUN/brief/plan.md"   # optional: tidy tear sheet
```

### Gate 2 — APPROVE PLAN → Sam writes the script

```bash
python -m pipeline.run --resume "$RUN" --approve-plan
```

Locks the criteria, smokes Opus, runs **Sam** (authors `script.md` + `beats.json`), stops at the script
gate. **Review:**

```bash
open "$RUN/brief/script.md"                         # Sam's studio-voice treatment
open "$RUN/brief/beats.json"                        # the structured beat sheet (Sam→Bea contract)
open "$RUN/sam_raw.txt"                             # Sam's RAW Opus output (new)
python -m pipeline.cli script show --beats "$RUN/brief/beats.json"   # optional tear sheet
```

### Gate 3 — APPROVE SCRIPT → Bea boards it (the curation gate)

```bash
python -m pipeline.run --resume "$RUN" --approve-script
```

Locks the beats, smokes Sonnet, runs **Bea** (authors `storyboard.md` + a **draft `shots.yaml`**), stops
at the curation gate. **Review, then curate** — this is the big one:

```bash
open "$RUN/brief/storyboard.md"                     # Bea's board
open "$RUN/bea_raw.txt"                             # Bea's RAW Sonnet output (new)
open "$RUN/brief/shots.yaml"                        # THE DRAFT — edit this file directly
python -m pipeline.cli storyboard show --shots "$RUN/brief/shots.yaml"   # optional tear sheet
```

Edit `$RUN/brief/shots.yaml` however you like — rewrite weak per-shot prompts, fix `hold` values,
reorder, adjust the `beat_id` links. This is where your taste enters. (Watch how much you have to rewrite
— light edits mean Bea's prompts are good; heavy edits are the signal we're looking for.)

### Gate 4 — APPROVE STORYBOARD → enter GENERATE, frame 1

```bash
python -m pipeline.run --resume "$RUN" --approve-storyboard
```

Re-validates your edited `shots.yaml` (coverage + the `beat.cast ⊆ shot.cast` conflict rule) and
**refuses to lock a broken board** — if it complains, fix `shots.yaml` and re-run this same command. On a
pass it locks the board, enters GENERATE, and generates frame 1, stopping at its eye gate. The terminal
prints the candidate path + T1 + Em's verdict. **Review:**

```bash
open "$RUN/candidates/F01/attempt_01.png"          # or the exact candidate path printed
open "$RUN/em_verdicts.jsonl"                       # Em's reads, appended per frame
```

### Gate 5 — the per-frame eye gate (repeat for each frame, in order)

For each frame, look at the candidate and the printed Em verdict, then either approve or retry:

```bash
# happy path — approve frame N (chains into frame N+1 automatically):
python -m pipeline.run --resume "$RUN" --approve-frame 1

# or re-roll with a correction (up to 3 attempts), e.g.:
python -m pipeline.run --resume "$RUN" --retry-frame 1 --note "mascot drifted toward red — hold the terracotta box-creature palette"
```

Approve frames **in sequence** (1, then 2, …) — the chain references the prior approved frame, so the
orchestrator enforces order. The Spark piece is 5 frames, but the real count comes from your curated
board — check anytime with:

```bash
python -m pipeline.run --resume "$RUN" --status
```

After you approve the **last** frame, ASSEMBLE runs automatically and builds the loop. **Done:**

```bash
open "$RUN/export/"                                 # the GIF/WebM loop
```

---

## The payoff — compare the fleet's board to your hand-authored one

The original Spark brief still holds *your* hand-written `shots.yaml`. Diff it against what the fleet
authored — this is the real read on whether Sam/Bea are good:

```bash
diff briefs/2026-06-10-spark-shared/shots.yaml "$RUN/brief/shots.yaml" | less
```

(They won't match line-for-line — you're comparing intent, prompt quality, and structure, not bytes.)

---

## Troubleshooting

- **"ANTHROPIC_API_KEY is set — this would bill the Anthropic API"** → you forgot `unset ANTHROPIC_API_KEY`. Unset it and re-run.
- **"STUB FALLBACK marker … was NOT really authored"** at a gate → the subscription auth isn't working, so the agent silently stubbed. Run `claude login`, confirm `claude` works, and re-run the same command. (With the hardening, the gate smoke should catch this *before* the authoring call now.)
- **A gate smoke fails (`GuardError`)** → same root cause (auth/SDK). The gate stops before spending; fix auth and re-run. Good — that's the smoke doing its job.
- **"manifest not found"** → you're not in the repo root. `cd /Users/seanwinslow/Code-Brain/anima`.
- **"--approve-frame N but the current frame is X"** → approve frames in order; check `--status`.
- **4th attempt on a frame** → the retry ladder stops and flags for you. Either curate the prompt and retry, or accept the best attempt.
- **Never pass `--stub`** here — that's the $0 offline smoke; it would not produce real frames.

## Two reminders

- **You drive it, not Claude Code.** Every command above is yours to run in your terminal so you see the process live. If you want Cowork to explain any stage's output in detail afterward, save the `run_dir` and bring it back — that's the best way to learn it properly.
- **Stop and look before each approve.** The gates exist so your taste is in the loop. The agents proposed; you decide.
