# Reve vs NB2 — image-editing bake-off — RESULTS (not yet run)

**Status: SCAFFOLD. No live run has happened.** This file is the committed decision
artifact and will be overwritten by the first real `--stage all` run (keys set, from
an isolated worktree). Until then there is no result to read.

The harness has been smoke-validated in `--stub` mode only (placeholder outputs, $0,
no scored claim) — that proves the plumbing, never a verdict.

Run it (see [README.md](README.md) for the full fleet-ops guardrails):

```bash
# isolated worktree, ANTHROPIC_API_KEY UNSET, REVE_API_KEY + GEMINI_API_KEY set,
# torch+transformers installed for the DINOv2 tier:
.venv/bin/python evals/bakeoffs/2026-06-07-reve-vs-nb2-editing/bakeoff.py --stage all --score-em
```

The decision rule lives in [README.md](README.md) §Decision rule.
