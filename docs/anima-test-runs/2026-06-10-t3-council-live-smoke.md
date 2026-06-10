# T3 Council — LIVE pre_museum gate smoke (2026-06-10)

**Portfolio-grade "T3 works end-to-end" evidence.** Session B wired the `pre_museum`
gate ([`pipeline/museum/t3_gate.py`](../../pipeline/museum/t3_gate.py)) into the museum
build and ran the council **live** over committed-museum exhibits. This is the first time
all three vendors fired live in the council (Session A was stub-only; codex wasn't installed).

## Result — the headline

- **Three vendors fired LIVE, not stub** (the 2026-06-07 silent-flag lesson, asserted):
  every peer returned `stub_fallback=False`.
  - **Codie** → `codex exec` (codex-cli 0.139.0, ChatGPT Plus, $0 incremental)
  - **Annie** → Gemini API, `model=gemini-3.5-flash` (bounded `GEMINI_API_KEY`, ~pennies)
  - **Sage** → Opus vision, `model=claude-opus-4-7` (Claude Agent SDK, subscription, $0 incremental)
- **Chairman synthesized** as a SEPARATE Opus call (`invoke_opus_text`, `claude-opus-4-8`),
  producing a real adjudication that weighed the peers' dissent.
- **Agreement score computed** per exhibit (0.33 split → 0.67 → 1.00 unanimous, all observed).
- **Patches staged, never auto-applied** (`auto_apply: false`) with `proposed_by ∈
  {codie, annie, sage, chairman}` into the gate's `manifest.lock.yaml`.
- **Gate semantics proven both ways:** a chairman `fail` **blocked** render; `borderline`
  **proceeded** (human call).

§0 (fleet-ops): divergence `0 0`; Em verdict baseline md5 `2af75906…ceb2e4` byte-identical;
`ANTHROPIC_API_KEY` **absent** (Sage + Chairman bill the subscription via the SDK);
`GEMINI_API_KEY` present + bounded; `which codex` confirmed; full stub suite green first.

## Run A — `character-bible`, 1 exhibit → BLOCKED (fail)

`t3_council_gate(museum, manifest, limit=1, project_slug="character-bible")` · **wall 58.4s** · `blocked=True`

Exhibit `01-turnarounds-body-front`: **verdict=fail, status=ok, agreement=0.67**, 1 artifact.

| peer | live? | model | verdict | conf |
|------|-------|-------|---------|------|
| codie | ✅ live | (config default) | fail | 0.78 |
| annie | ✅ live | gemini-3.5-flash | fail | 0.70 |
| sage  | ✅ live | claude-opus-4-7 | pass | 0.55 |

**Chairman (fail):** *"Two in-lane structural fails (provenance + visual identity drift)
against one out-of-lane narrative pass. The plate fails the cited identity invariants and
is already at `human_gate_required`; the museum must record it as a non-canonical reject,
not publish it as an approved turnaround. Council fails it and promotes the
provenance-honesty patches; the register re-bake defers to Cy/Sean."*

A real catch: the council read the exhibit's own `human_gate_required` outcome and refused to
let the museum publish it as approved. **5 patches staged** (codie ×2 outcome/publishable
locks, annie ×1 style_register, chairman ×2). The gate returned exit 2 and would refuse `--render`.

> Note: Annie's "abandons the required pixel-art register" reasoning is itself a likely *misfire*
> — the mascot pivoted pixel→pencil long ago. That doesn't weaken the smoke (the machinery is
> proven); it's a substance signal that the committed `character-bible` exhibits may carry a stale
> style-register hint Annie keys on. Recorded, not fixed (out of Session-B scope).

## Run B — `pencil-test`, 2 exhibits → NOT blocked (borderline ×2)

`t3_council_gate(museum, manifest, limit=2, project_slug="pencil-test")` · **wall 171.7s** · `blocked=False`

**`seedance-PB-01`** — verdict=borderline, **agreement=0.33** (full three-way dissent):

| peer | live? | model | verdict | conf |
|------|-------|-------|---------|------|
| codie | ✅ live | (config default) | pass | 0.54 |
| annie | ✅ live | gemini-3.5-flash | borderline | 0.90 |
| sage  | ✅ live | claude-opus-4-7 | fail | 0.72 |

Chairman adjudicated the split to **borderline** — "adjudicates the honesty of the record, not
the shot's craft… Codie (most on-lens) passes the record as honestly thin; Annie's grounded
continuity drift and Sage's corroborating tonal note keep it [borderline]."

**`seedance-PM-01`** — verdict=borderline, **agreement=1.00** (unanimous borderline);
chairman: "Annie's high-confidence clean-plate artifact in t5 is the decisive, fixable blocker;
the provenance gap is honest thinness to be made explicit, not invented around."

**14 patches staged** across `codie / annie / sage / chairman`. Borderline did **not** block —
exactly the intended "surface but proceed, human call" semantics.

## What this proves

1. The `pre_museum` gate runs the gate-agnostic `T3CouncilNode` over real assembled exhibits,
   mapping each exhibit's `assets/*` → `artifact_paths` and its title/rationale → `beat_description`.
2. All three heterogeneous transports work live and are correctly distinguished from stub
   (`peer_verdicts[*].stub_fallback` surfaced for the assertion).
3. The chairman is a real, separate Opus synthesis that weighs dissent — not a vote count.
4. Patches stage (never auto-apply); a `fail`/all-errored blocks render, `borderline` proceeds.
5. Per-exhibit wall ≈ 58–86s (Opus escalation dominates), well within `per_call_timeout_s: 120`.

## Honest caveats

- **`codie` model reads as the config default (None surfaced).** `run_codex_with_image` passed no
  `-m`, so codex used its `~/.codex/config.toml` model; the live signal is `stub_fallback=False`
  (codex ran), which held. A future enhancement could pin + read codie's served model back.
- **Annie's `character-bible` style-register misfire** (above) is a substance finding for a later
  pass, not a gate defect.
- This is a **smoke** (3 exhibits), not a scored eval. It proves the pipeline is real and live;
  it does not measure council precision/recall. A scored T3 eval + the Sage-tier bake-off (Open Q2)
  are ticketed.

## Reproduce

```bash
# §0 first: divergence 0 0, ANTHROPIC_API_KEY absent, GEMINI_API_KEY in .env, which codex.
python scripts/build_museum.py --t3-gate --t3-project character-bible --t3-limit 1
# fail → exit 2, refuses --render; borderline/pass → proceeds. Patches:
python -m pipeline.cli patches list --run-dir museum/_t3_gate
```
