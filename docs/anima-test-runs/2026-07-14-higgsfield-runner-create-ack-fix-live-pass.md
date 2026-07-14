# Field report — Higgsfield create-ack fix: LIVE PASS

**Date:** 2026-07-14
**Base:** `main` at `32d9c42` (#114)
**Branch:** `codex/higgsfield-create-wait-fix` in an isolated worktree
**Outcome:** **PASS — Task 7's production Higgsfield transport is live-verified.**

## 1. Defect closed

CLI 0.2.3 returns a one-element JSON array from `generate create … --json`:

```json
[
  "<job-id>"
]
```

The runner now parses that create-only shape through a dedicated `_parse_create_ack`; wait/get remain on `_parse_cli_output`'s flat-dict contract. A valid acknowledgment contains exactly one non-empty string ID. A multi-ID or otherwise invalid array fails loud, retains the durable create intent, publishes no pending receipt, and never selects an arbitrary job.

The production order is now:

```text
durable intent
→ create --json
→ parse sole job ID
→ durable pending receipt
→ durable intent removal
→ wait same job ID --json
→ durable completed pending receipt
→ download
→ provenance then cache image publication
→ durable pending removal
```

All prior intent/pending/quarantine/flock/retry/same-ID/fsync hardening remains intact.

## 2. TDD and network-free verification

The captured create fixture first reproduced the live defect: the response was `ok=False` with no job ID and the regression stayed RED. A second RED fixed the policy for multi-ID acknowledgments. After the dedicated parser landed:

```text
tests/test_higgsfield_runner.py  47 passed
tests/                           992 passed, 2 dependency warnings
pipeline/tests/                  10 passed
git diff --check                 clean
py_compile                       clean
```

Frozen guards remained byte-identical:

```text
2af75906502f1caf8857e18828ceb2e4  evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md
945af824fa53b948a18ac6bf206d67ef  pipeline/agents/prompts/sean-screenwriting-voice.md
```

The two sanitized CLI 0.2.3 shape fixtures are:

- `tests/fixtures/higgsfield/create-ack-v0.2.3.json`
- `tests/fixtures/higgsfield/wait-complete-v0.2.3.json`

## 3. Fresh live verification

Fleet pre-flight passed immediately before spend:

- `ANTHROPIC_API_KEY` absent;
- `ANIMA_FORCE_STUB` absent;
- CLI pinned at `0.2.3` (`868f62a…`), not upgraded;
- ULTRA balance 4003.64 credits;
- isolated worktree with no competing costed executor;
- fresh `runs/2026-07-14-higgsfield-create-ack-pass/`;
- reference `registers/primal-sketch-grit/refs/grandmaster-chosen-pose-1.png` present.

Sean gave a fresh GO for one ~4-credit production generation. The call ran through `invoke_image_edit`, not raw CLI.

First invocation:

```text
ok=True
exit_code=0
stub_fallback=False
cache_hit=False
job_id=76a6f08b-b1ee-4c47-9e59-3dca96551afb
result_url=<non-null>
output=plate.png (1,688,149 bytes)
provenance sidecars=1
intent/pending/quarantine markers=0/0/0
```

Balance moved once: **4003.64 → 3999.64** (4 credits).

The identical rerun used the same inputs and cache directory:

```text
ok=True
cache_hit=True
job_id=76a6f08b-b1ee-4c47-9e59-3dca96551afb
result_url=<non-null>
output=plate-cache-hit.png (1,688,149 bytes)
balance=3999.64 → 3999.64
```

This proves one charged create, same-ID completion, durable download/provenance publication, and a zero-spend identical cache hit.

## 4. State-of-record

Task 7 is now live-verified in:

- `CLAUDE.md` and `AGENTS.md` (Cy row);
- `docs/active/2026-07-04-register-backlog-and-transport-findings.md` §7;
- `docs/active/2026-07-13-transport-strategy-decision.md` §T1;
- `CHANGELOG.md`.

The earlier failed reports remain unchanged as the honest sequence that found the combined-create defect and then the array-ack defect.

Still gated after this PASS:

- **T2** — GRANDMASTER's real in-register Bible-pass edit-identity validation, costed and Sean-gated;
- **T4** — Phase-6 Motion wiring to Higgsfield Seedance when Motion enters the orchestrator.

Only Sean merges the resulting PR.
