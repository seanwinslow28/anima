# Field report — the costed Spark-animatic driven run (DoD #6 closed)

*Date: 2026-06-22 (run id `2026-06-21-spark-animatic-driven`; started 06-21, completed 06-22).
Operator: Claude Code (drove every command). Taste calls: Sean (plan/script/board/animatic + all 7 per-frame gates).
Verdict: **DoD #6 met — placement holds, the loop ships.***

---

## What this was

The costed, end-to-end **operator-driven** run that closes **ROADMAP DoD #6** (TOP-1 Animatic):
a real loop exercising the built ANIMATIC stage, proving a human-authored placement rough makes
NB2 respect placement *before* it draws — beating the 2026-06-18 baseline, which drifted (mascot
form/scale wobble across frames). Part 1 (the two hardening fixes, PR #63) shipped first; this was
Part 2.

**Operating model held the whole way:** Claude Code ran every command, read every traceback, copied
files, built the before/after, and never auto-approved a frame. Sean made only the taste calls. Em
informed; she never decided.

## Outcome

- **A 7-frame Spark loop shipped** (`runs/2026-06-21-spark-animatic-driven/export/spark-animatic.{gif,webm,mp4}`),
  18 frames on twos (F01/F07 held 4, F02–F06 held 2).
- **Placement held** where 06-18 drifted — Sean's eye, on the playing loop (Engine Truth).
- **Zero retries.** All 7 frames approved on attempt 1.

## Spend

| Stage | Engine | Gemini $ |
|---|---|---|
| PLAN (Maya) | Opus 4.8 + Sonnet adversarial — subscription | $0 |
| SCRIPT (Sam) | Opus 4.8 — subscription | $0 |
| STORYBOARD (Bea) | Sonnet 4.6 — subscription | $0 |
| GENERATE | 7 × NB2 `gemini-3.1-flash-image-preview` @ ~$0.07 | **~$0.49** |
| Em (T2) | 14 calls, gemini-3.5-flash via Gemini API | ~pennies |
| ASSEMBLE | local FFmpeg | $0 |
| **Total** | | **≈ $0.50** |

Came in at **Maya's low band ($0.35 low / $0.93 median / $2.25 high** for 5 frames; ~$0.5–$3.2 scaled
for 7) because the identity-critical two-character work needed **no re-rolls** — the placement seed
plus the establishing-vs-edit chaining carried it first-shot. Last night's failed Maya call
(below) was Opus/subscription → $0 Gemini.

## Retries per frame

**Zero.** Every frame approved on attempt 1.

| Frame | Beat | Em[sean] | Em[claude-mascot] | Sean |
|---|---|---|---|---|
| F01 | Establishing | pass (1.0) | pass (1.0) | approve |
| F02 | The draw | pass (0.98) | pass (0.98) | approve |
| F03 | The notice | pass (0.98) | **borderline (0.95)** | approve (overruled Em) |
| F04 | The delight | pass (1.0) | **borderline (0.95)** | approve (overruled Em) |
| F05 | Delight holds | pass (1.0) | pass (1.0) | approve |
| F06 | The settle | pass (0.98) | pass (0.98) | approve |
| F07 | Loop-return | pass (1.0) | **borderline (0.95)** | approve (overruled Em) |

**The Em-vs-eye delta (Tier-2 input):** Em[claude-mascot] went borderline three times (F3/F4/F7),
each on the *same* finish-register drift — missing face construction cross-line + flat color fills
instead of warm-graphite cross-hatching, plus once (F3) a missing far-side ear-nub. Sean's eye
judged all three shippable: the drift is fine-grained mascot *finish*, not placement or identity,
and it doesn't read at loop speed. Notably **Em[sean] passed all 7 and even contradicted
Em[claude-mascot] on F3** (called the mascot "alert and upright" while the mascot-pass flagged the
perk as not landing) — a concrete reminder the two namespace reads aren't calibrated against each
other, let alone against Sean's eye. This is exactly the calibration target for workstream 2.

## The before/after read (the heart of DoD #6)

| 06-18 failure mode | 06-21 (animatic-driven) |
|---|---|
| Mascot form/identity drifts frame-to-frame (rounded blob → boxier across F01→F05) | **Held** — consistent crisp terracotta box-creature, every frame |
| Inconsistent scale | **Held** — consistent compact shoulder-perch scale all 7 |
| Mascot on the wrong/looser shoulder | **Held** — same shoulder all 7 |
| 2↔4 leg-count drift | **Avoided** — the roughs pin a *perched/compact* form, so legs never splay (not a factor this run) |

The mechanism worked as designed: at GENERATE, the frame-named rough rode in **last + role-tagged**
after both Bible anchors (verified in the logs: `References: …/anchor.png, …/anchor.png,
…/animatic/F0N.png`), so NB2 saw the placement intent without inheriting the rough's look. The loop
the rough was drawn for is the loop that came out.

One nice confirmation: at the animatic gate Sean flagged that rough F07 sat *warmer* than F01's
neutral idle. Because frame 7 chains off **approved frame 1** (`chain_from: 1`, the Slice-B
behavior) and its prompt locked "composition identical to frame 1, mascot perched idle," the
generated F07 came back **neutral** — the chain + prompt overrode the rough's expression, and the
loop closed tight. The role-tag clause quarantines the rough's *look*; the chain + prompt own
expression; the rough owns placement. That division of authority is the right one.

## Did `--frames 7` make the count Just Work?

**Yes — cleanly, end to end.** Sean drew 7 roughs; `--frames 7` reached Bea (Fix B), who boarded
exactly 7 from the 5-beat script (beat 4 → frames 4,5; beat 5 → frames 6,7), ids 1–7 strictly
ascending, `chain_from: 1` on the closer. The storyboard gate's `_enforce_frame_count` printed
*"Board has 7 frame(s)"* and locked without curation — no count veto, no `F06`-mismatch hard-error
(the 06-21 cancellation's Bug 2). The human owned the count and the agent's board conformed, exactly
as PHILOSOPHY requires.

Fix A also earned its keep: Maya's adversarial Sonnet pass **caught and corrected a mislabeled
impact_tag in-call** — `AC.continuity.stylus-right-hand` was carrying `identity_critical`; the pass
re-tagged it `continuity` (her confidence note #1), avoiding a redundant per-frame Opus escalation.
The exact class of mislabel that exploded the cancelled run four gates later was now resolved at
authoring, and the criteria locked legal (impact_tags: aesthetic/continuity/identity_critical/
structural/technical — no `timing`).

## The throttle finding (seam #4 — nested-SDK throttle) + the env-strip outcome

**Confirmed and resolved.** Driving the orchestrator from inside a Claude Code session nests the
Claude SDK: the spawned `claude` inherits the session markers (`CLAUDECODE`,
`CLAUDE_CODE_SESSION_ID`, `CLAUDE_CODE_CHILD_SESSION`, `CLAUDE_CODE_ENTRYPOINT`) and runs as a
throttled child. Last night that produced a degraded canary (94s vs ~3s normal) and an **empty**
Maya response (`maya_raw_pass1.txt` = 0 bytes → `ValueError: Empty response from model`).

The fix Sean chose (option 1): **strip the markers, keep driving.** Every costed orchestrator
command ran under:

```
env -u CLAUDECODE -u CLAUDE_CODE_SESSION_ID -u CLAUDE_CODE_CHILD_SESSION \
    -u CLAUDE_CODE_ENTRYPOINT -u AI_AGENT -u CLAUDE_CODE_ENABLE_TASKS \
    python3 -m pipeline.run …
```

A cheap probe gated the first spend: the stripped-env canary returned in **6.9s** (vs 94s). Across
the whole run the un-nested canary held normal: **11.8s / 7.3s / 6.0s** for the PLAN/SCRIPT/
STORYBOARD smokes. `shutil.which('claude')` resolved fine un-nested (the strip leaves
`CLAUDE_CODE_EXECPATH` intact), so the SDK located the CLI without trouble. Maya's pass-1 came back
**15,653 bytes** of real plan — the empty-response failure did not recur once.

**Verdict on the remedy:** the env-strip is a clean, sufficient workaround for driving costed
authoring from inside a session. CLAUDE.md's documented "run from a plain terminal" remains the
zero-risk path, but the strip-set lets Claude Code drive end-to-end without a human terminal, which
is the whole point of the operator-driven model. Recommend folding the strip-set into the runbook as
the sanctioned in-session path.

## New seam found this run

**Background tasks reset CWD to the primary checkout, not the worktree.** The foreground Bash tool's
working directory persisted to the worktree, so a few `--approve-*` commands ran correctly without
an explicit `cd`. But a **background** task starts from the primary working directory — so the first
`--approve-frame 1` (backgrounded without an explicit `cd`) resolved `--resume
runs/2026-06-21-…` against the *main* checkout (no such run-dir there) and exited 1, with the log
redirect failing for the same reason. **No spend, no state mutation** — the command never found the
run. Fix: always pass an absolute `cd /…/worktree && …` inside every background command (which the
authoring stages already did). Cheap to hit, cheap to fix, but worth a runbook line: *for
worktree-isolated costed runs, background commands must `cd` explicitly; don't rely on the
foreground tool's persisted CWD.*

## Loose threads (not blocking the DoD)

- **Em's mascot finish-register drift** (construction line / cross-hatch) recurred on F3/F4/F7 and
  Sean over-rode it each time. It's a real, consistent Em signal that the human reads as
  below-the-bar-of-mattering — a clean calibration datapoint for **workstream 2 (Tier-2 Em)**.
- **The "notice" beat (F3) didn't perk** much past F2 — Maya flagged this risk in planning (perk and
  delight are adjacent). It's a board/prompt nuance, not a placement or stage failure; the loop still
  reads. Worth a stronger perk-delta in the board prompt if this piece is ever re-cut.
- **`identity_critical` → Opus escalation (discrepancy B)** — first-pass reads still ran on Gemini
  (the Em verdicts above are Gemini-grounded). Unchanged this run; remains a workstream-2 decision.
