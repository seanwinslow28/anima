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

## The chain (Slice 3)

```
spark → MICRO-EXPAND (always) → deepen? → INTERROGATE → ART-VIZ (inline) → SYNTHESIZE → emit + validate
                                   │            │
                                   └─ EXPAND ───┘   the inline contested-axis workshop —
                                                    on "deepen", or mid-grill whenever an
                                                    axis turns contested. Same room; the
                                                    session never steps out to a skill.
```

`references/chain-map.md` has the full routing rules and skip conditions. The
one future stage (STRESS-TEST) is named there too — if a session clearly
needs it before it's built, say so and do the best inline approximation;
never pretend a stage ran.

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

Then ask Sean **one question**: *deepen, or proceed to interrogate?* On
"deepen", run the contested-axis workshop below. Lock his picks: which
premise, which tonal lean, which risks to carry as live constraints.

This runs even when the spark arrives rich. A rich spark with one fragile
high-value intuition is exactly the one a lazy front door flattens.

### The contested-axis workshop (EXPAND at workshop depth — inline, same room)

The micro-expand is EXPAND's reflex depth; this is the same mechanism turned
up on **one contested axis** — a live tension the room hasn't resolved (the
ending, the stakes, the signature mechanic). Two triggers, one behavior:

- Sean answers **"deepen"** at the micro-expand gate, or
- an axis turns contested **mid-grill** — INTERROGATE deepens **in place**;
  it does not raise-and-return or invoke a sibling. The room never leaves
  itself.

**Not a volume fan-out.** The old "≥8 avenues across ≥4 domains" count is
dead — volume is gameable (eight semantic neighbours hit the number and say
nothing). Per contested axis, run this instead:

1. **N≈3–5 options, mutually distinct.** Rotate the lens to force real
   spread — emotional core / structural mechanic / tonal register /
   failure-mode / cross-domain analogy — because left alone the model
   clusters semantically: four phrasings of one idea wearing four hats.
2. **Each option is a named specific with its tradeoff.** "His biggest hit
   is an accidental humiliating clip he never meant to film — and he's
   mortified it worked" locks; "a surprising ending" doesn't.
3. **Qualify against the job.** JTBD (functional / emotional / social) and
   "structural, not narrative": does the option change how the piece is
   built, or just re-describe it?
4. **Converge.** One stated recommendation — combining options is fair —
   phrased so Sean can accept or veto in a line.
5. **Protect the fragile intuition.** Name the duality/tension that makes
   the spark special and check no option flattens it into a clean moral.
6. **Surface buildability risks as `open_questions`.** A register anima
   can't yet build gets flagged, not waved through.

Append only the four proposal kinds to the sidecar, one block per axis
(`### expand:<axis-slug>` — see `references/session-sidecar-contract.md`);
Sean picks; **you** lock, and record `expand:<axis-slug>` in
`stage_provenance`. The quality bar and Sean's live-review checklist:
`references/good-expand-rubric.md`.

## Step 2 — INTERROGATE

Invoke the `frontdoor-interrogate` skill. It reads the sidecar and grills Sean
one question at a time until the North Star is nailed down. It appends
proposals only; as answers resolve, **you** append the locked decisions.

## Step 2.5 — ART-VIZ (inline, no skill call)

Once the North Star is locked, propose the look — in place, without leaving
the room. **Not** a skill call: the `genndy-tartakovsky` style skill is a
deferred Cy-layer asset, not built here, and there is no `frontdoor-art-viz`
skill to invoke.

- **Pick one hero frame** — the piece's signature moment — and write **≥3
  mutually-distinct, Flow-ready route prompts** that render **that same
  composition** in different registers (a faithful homage, a grittier
  sibling, a personal-lineage fusion with anima's own pencil-test warmth).
  Vary the rendering language, not the frame, so Sean compares looks
  apples-to-apples.
- **The piece's signature mechanic is never dropped.** Rendered in the hero
  frame when the frame *is* the mechanic moment (ai-guru's Orby-glitch); or
  captured in the money-shot/timing-bible prose when the frame is a
  pre-mechanic beat (the piñata's landing pose, with candy-as-oil locked in
  the money-shot section).
- **Each route is a self-contained prompt** Sean could paste into Flow and
  get the hero frame — a named specific, never a category label.
- **Capture the piece's timing/craft bible as prose** — the numbered spine
  directives. It also seeds the Studio Brief non-negotiables.
- **Flag any register anima can't yet build** as an `open_question` + a seed
  `style_register` NEW-flag + the doctrine pointer
  (`docs/architecture/prompt-style-neutrality-doctrine.md`). Surface it;
  never extend the closed vocabulary inline.
- **The no-library operating rule:** draw the route language from the locked
  references, the timing bible, and the character seeds' `source_notes` —
  the material already in the room. If that reference knowledge is missing
  for a route, raise an `open_question`; **do not invent a reusable style
  doctrine** (that is the deferred style skill's job, on a real Cy run).

Append only the four proposal kinds to the sidecar (`### art-viz` — see
`references/session-sidecar-contract.md`): `options` = the routes,
`recommendation` = the lean, `open_questions` = the un-buildable-register
flag. Sean renders on Flow and picks; **you** lock the chosen route and
record `art-viz` in `stage_provenance`. **This is a $0 prompt-only stage —
you never render or spend; Sean runs Flow himself.**

Skip condition: a piece with a locked register already (e.g. an act inside
an existing piece) skips ART-VIZ — declared skipped in `stage_provenance`,
never silently faked. The quality bar and Sean's live-review checklist:
`references/good-art-viz-rubric.md`.

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
