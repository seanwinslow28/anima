# Studio Brief contract — the 8-section shape

`00_studio_brief.md` is the machine-facing Phase-0 input. Maya, Sam, and Bea
consume it as free text — nothing downstream parses the headers — so this
shape is a discipline anima enforces on itself, and `pipeline.frontdoor`'s
validator is that enforcement. Exact headers, exact order, every body
non-empty:

```markdown
## What is this story about?
## Who is this character?
## What is the tone?
### What this is NOT        ← required, nested inside the tone section
## What is the format?
## What is the target medium?
## What is the deadline?
## What are the non-negotiables?
```

An H1 title and a short preamble above the first section are fine (the
validator ignores them; the piñata golden carries both).

## What each section is for

- **Story** — the whole arc in one paragraph. A reader who stops here can
  still describe the piece. Name the emotional engine, not just the plot.
- **Character** — every character that needs designing, each with
  design-bearing specifics (bold the name; state the load-bearing object or
  trait). This section seeds Cy via `character_seeds.yaml` — write it so a
  designer could start.
- **Tone** — the register in the piece's own language, plus references with
  their *what* ("Tartakovsky: timing-as-a-song, silhouette, stylized
  violence").
- **### What this is NOT** — the discipline block, and usually the most
  load-bearing text in the brief. Name the nearest failure modes and fence
  them: the wrong medium ("not anime, not 3D-rendered"), the wrong register
  ("melancholic, not grieving"), the wrong joke ("the kid is never the
  joke"). A NOT that merely inverts a positive ("not bad timing") is
  padding — every line here should kill a *plausible* wrong version. This is
  where taste survives the handoff.
- **Format** — runtime, act structure, ratio posture. Bounded — Maya can't
  plan "2 to 10 minutes, we'll see."
- **Target medium** — where it lives; masters and cut-downs.
- **Deadline** — hard/soft, or an explicit `TBD — Sean to set`.
- **Non-negotiables** — the piece's contract, one checkable directive per
  bullet. Phrase them so a critic could verdict a frame against them:
  numbers, holds, objects, continuity rules. "Timing is a song: ~15% silent
  held buildup before payoffs" is checkable; "great timing" is not.

## Style

Directive prose, no decoration. Every sentence either constrains or
describes something buildable. Sean's voice survives in word choice, not in
throat-clearing — the piñata brief is the register to match.
