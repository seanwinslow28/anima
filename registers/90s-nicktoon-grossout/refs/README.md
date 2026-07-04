# `90s-nicktoon-grossout/refs/` — what belongs here (and what never does)

This folder holds the register's **style exemplars** — the images the human
eye ratifies the look against, and (only if a go/no-go escalates to a
style-reference feed) the images fed to generation.

**Status:** this register is a **CANDIDATE** — research + look-spike stage,
**not yet authored** into `pipeline/registers.py`. It is gated on Sean liking
a look-spike (his cross-engine test in the ChatGPT + Flow web apps), exactly
like the `primal-sketch-grit` process. See [`../research.md`](../research.md).

**What lands here:**
- The **look-spike frames** themselves, once generated (in a dated
  `spike-<date>/` subfolder, mirroring `primal-sketch-grit/refs/spike-2026-07-04/`),
  so the look-decision's evidence stays with the register.
- Sean's confirmed **hero frame(s)** once a look is picked (the ai-guru
  ART-VIZ target lives at `briefs/2026-07-02-ai-guru-pilot/` today).
- Any future **self-authored** exemplars in this register.

**What NEVER lands here:** third-party *Ren & Stimpy* stills, cels, or artbook
scans — and no frames that reproduce a specific copyrighted character design.
They are copyrighted study material — reasoned about with sources in
[`../research.md`](../research.md), never committed to the repo and never fed
to a generation call. This register's non-derivative rule (research.md §7) is
**doubly load-bearing** here: the ai-guru concept's own non-negotiable is that
the look is a *genericized 90s-nicktoon-gross-out aesthetic* — homage to a
school of animation, never a copy of one show's cast or a real person's IP.
Capture the school; never the specific character or frame.

The `RegisterSpec.reference_images` tuple in `pipeline/registers.py` stays
empty until real files land here (and until the register is authored); update
it (paths relative to the repo root) in the same commit that adds them.
