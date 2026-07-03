# `primal-sketch-grit/refs/` — what belongs here (and what never does)

This folder holds the register's **style exemplars** — the images the human
eye ratifies the look against, and (only if the go/no-go escalates to a
style-reference feed) the images fed to generation.

**What lands here:**
- Sean's confirmed ART-VIZ **Route-B hero frame** (the go/no-go target from
  `briefs/2026-07-02-grandmaster/go-no-go.md`) — his call, drop-in when ready.
- The go/no-go **spike frames** themselves, once generated (NB2-from-text +
  the Route-C comparison frame), so the decision's evidence stays with the
  register.
- Any future **self-authored** exemplars in this register.

**What NEVER lands here:** third-party *Primal* stills or artbook scans.
They are copyrighted study material — linked with sources in
[`../research.md`](../research.md) §3, viewed there, never committed to the
repo and never fed to a generation call. The register's non-derivative rule
(research.md §7): capture the school, never the episode.

The `RegisterSpec.reference_images` tuple in `pipeline/registers.py` stays
empty until real files land here; update it (paths relative to the repo
root) in the same commit that adds them.
