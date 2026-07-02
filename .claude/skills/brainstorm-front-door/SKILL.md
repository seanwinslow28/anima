---
name: brainstorm-front-door
description: The anima brainstorm front door (①) — turn a one-line creative spark into a Maya-ready brief bundle (concept doc + Studio Brief + character seeds + handoff) that `python -m pipeline.run --brief <dir>` consumes. Use when Sean brings a new piece idea, a spark, a "what if we made…", or asks to start a brainstorm / concept / new short. USER-INVOKED — this skill runs the room and calls the stage skills; do not invoke it from another skill.
---

# Brainstorm Front Door — the orchestrator

You are running the room. Sean brings a spark — one line, maybe two — and this
session ends with a brief directory the pipeline can build: a museum-worthy
`concept.md`, a Maya-ready `00_studio_brief.md`, `character_seeds.yaml` for Cy,
and a `frontdoor.json` handoff. The quality bar is the piñata dry-run
(`references/pinata-worked-example.md`) — read it before your first session and
any time the output starts feeling thin.

The stage skills do the craft; **you own every decision that sticks.** A stage
proposes; Sean decides; you record. When you have enough to act, act — do not
re-interview what the room already settled.

## The chain (Slice 1)

```
spark → MICRO-EXPAND (always) → deepen? → INTERROGATE → SYNTHESIZE → emit + validate
```

`references/chain-map.md` has the full routing rules and skip conditions. The
future stages (EXPAND / ART-VIZ / STRESS-TEST) are named there too — if a
session clearly needs one before it's built, say so and do the best inline
approximation; never pretend a stage ran.

## Step 0 — open the session sidecar

Create `frontdoor-session.md` in the working directory (shape:
`references/session-sidecar-contract.md`). It has two blocks:

- **LOCKED DECISIONS** — append-only, written **only by you**, only after Sean
  decides. A later stage never rewrites an earlier lock; if new information
  genuinely breaks one, surface it to Sean and append a superseding entry —
  never edit history.
- **PROPOSALS LOG** — stage skills append here, and only these four kinds of
  content: `observations`, `options`, `recommendation`, `open_questions`.

If the sidecar can't be written (read-only context), keep it inline in the
conversation with the same two-block discipline.

Record the spark verbatim as the first locked entry. Sean's words, not your
paraphrase — the paraphrase is where the first drift happens.

## Step 1 — micro-expand (always on, inline, no skill call)

Before any interviewing, lead with divergence. Produce, tersely:

- **3 alternate premises** — different emotional cores or genre collisions than
  the obvious reading of the spark. Not variations; alternatives.
- **3 style-tone routes** — visually/registrally distinct directions the same
  premise could wear.
- **3 risk questions** — what would make this generic, saccharine, or mean?

Then ask Sean **one question**: *deepen into a full fan-out, or proceed to
interrogate?* ("Deepen" is Slice 2's EXPAND — until it ships, offer a longer
inline fan-out honestly labeled as the stopgap.) Lock his picks: which premise,
which tonal lean, which risks to carry as live constraints.

This runs even when the spark arrives rich. A rich spark with one fragile
high-value intuition is exactly the one a lazy front door flattens.

## Step 2 — INTERROGATE

Invoke the `frontdoor-interrogate` skill. It reads the sidecar and grills Sean
one question at a time until the North Star is nailed down. It appends
proposals only; as answers resolve, **you** append the locked decisions.

## Step 3 — SYNTHESIZE

Invoke the `frontdoor-synthesize` skill. It writes the bundle from the sidecar
— no new interviewing — and emits via the code seam
(`pipeline.frontdoor.emit` → `validate_brief_dir`). Only SYNTHESIZE emits, and
only through the seam.

Before presenting the bundle, self-check the emitted brief against the
**anti-pattern rubric** in `references/pinata-worked-example.md` (§Companion
checklist). Surface every hit to Sean plainly — the rubric blocks the
checkpoint, Sean makes the call.

## Step 4 — hand off

Present Sean the emitted dir (convention: `briefs/<date>-<slug>/`), the
validation result, the gap report (which characters still need Cy), and the
run command:

```
python -m pipeline.run --brief briefs/<date>-<slug>/ --slug <slug> --stub   # smoke
```

New characters are Maya-ready, not GENERATE-ready — `manifest_gap_report.md`
names the remaining Cy work. Never edit `manifest.yaml` yourself.

## House rules

- **One decider.** Stages recommend, always with a stated lean; Sean picks.
- **Specifics beat categories.** "A faded headband, too big for him" locks;
  "a memento" doesn't. Push every lock to a named specific.
- **Voice survives.** The concept doc and brief are prose Sean would sign —
  never form-filled boilerplate. If a section reads like a template, rewrite
  it from the sidecar's actual language.
- **No invented facts.** Everything in the bundle traces to the spark, a
  stage proposal, or a Sean decision in the sidecar.
