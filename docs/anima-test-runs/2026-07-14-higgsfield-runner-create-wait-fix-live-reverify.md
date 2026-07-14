# Field report — Higgsfield create→wait runner fix: LIVE RE-VERIFY FAILED

**Date:** 2026-07-14
**Base:** `main` at `32d9c42` (#114)
**Branch:** `codex/higgsfield-create-wait-fix` in an isolated worktree
**Outcome:** **The transport generated successfully, but anima still returned `ok=False`. Do not merge or flip Task 7.**

## 1. Scope and safety boundary

This session addressed only the create→identity→parse seam identified by the first live smoke. It preserved the existing intent, pending, quarantine, per-key `flock`, retry, same-ID validation, cache-publication, provenance, and fsync ordering.

The fleet pre-flight passed before spend:

- `ANTHROPIC_API_KEY` absent;
- `ANIMA_FORCE_STUB` absent;
- isolated worktree on `codex/higgsfield-create-wait-fix`;
- no other Higgsfield/costed executor in that worktree;
- Higgsfield CLI exactly `0.2.3` (`868f62a…`), not upgraded;
- ULTRA balance 4007.64 credits;
- fresh `runs/2026-07-14-higgsfield-smoke-fix/`;
- reference present at `registers/primal-sketch-grit/refs/grandmaster-chosen-pose-1.png`.

Sean gave GO for one generation only.

## 2. TDD before live spend

The network-free regression first failed for the intended old behavior: create still carried `--wait`, and the fallback parser did not recognize a quoted/comma-suffixed URL. The contained implementation then:

1. removed `--wait --wait-timeout 9m` from `generate create`;
2. durably published the create acknowledgment before waiting;
3. routed the captured ID through the existing `_resume_existing_job` same-ID wait path;
4. persisted the completed wait metadata before download/publication;
5. stripped JSON double quotes and commas in the fallback URL token scan.

Pre-live verification was green:

```text
tests/test_higgsfield_runner.py  45 passed
tests/                           990 passed, 2 warnings
pipeline/tests/                  10 passed
git diff --check                 clean
py_compile                       clean
```

Frozen guards stayed unchanged:

```text
2af75906502f1caf8857e18828ceb2e4  evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md
945af824fa53b948a18ac6bf206d67ef  pipeline/agents/prompts/sean-screenwriting-voice.md
```

## 3. Live result — failed runner, successful charged job

The production `invoke_image_edit` seam ran once with `gpt-image-2`, the required GRANDMASTER reference, and the same in-register plate prompt used by the first smoke.

The runner returned:

```text
ok=False
exit_code=1
stub_fallback=False
cache_hit=False
job_id=None
result_url=None
output_exists=False
provenance_count=0
create calls=1
wait calls=0
```

The durable `*.create_in_flight.json` intent remained, so an automatic identical retry was blocked. No second create ran.

Balance moved exactly once, 4007.64 → **4003.64** (4 credits).

## 4. Corrected root cause — real create acknowledgment is an array

The split command itself exited **0**. Its exact stdout shape was:

```json
[
  "0a6db7e0-c138-454f-9b67-2019e97b23cc"
]
```

CLI 0.2.3 therefore returns a one-element JSON array of job IDs from `generate create ... --json`; it does **not** return the dict shape assumed by the first fix specification. `_parse_cli_output` only extracts identity from a JSON dict, so it discarded the successful acknowledgment, never published pending, never called wait, and returned identity-free exit 1.

This corrects the first smoke's narrower diagnosis. Decoupling create from wait is still the right transport sequence, but it is insufficient until the parser recognizes the observed create-ack array.

After the job completed, standalone `generate wait <id> --json` exited 0 with the expected flat dict carrying these top-level keys:

```text
created_at, display_name, id, job_set_type, params, result_url, status
```

Sanitized, network-free copies of both real shapes now live at:

- `tests/fixtures/higgsfield/create-ack-v0.2.3.json`
- `tests/fixtures/higgsfield/wait-complete-v0.2.3.json`

The create-ack fixture is now wired into the regression and deliberately RED:

```text
test_create_ack_is_persisted_before_wait_and_identical_retry_does_not_create
FAILED: first.ok is False; job_id/result_url are None
```

That RED is the exact next fix boundary. This session stopped rather than silently widening the live-failed implementation.

## 5. Receipt resolution

Read-only recovery used the captured ID `0a6db7e0-c138-454f-9b67-2019e97b23cc`:

- status reached `completed`;
- standalone wait returned the flat completion dict;
- result downloaded to `runs/2026-07-14-higgsfield-smoke-fix/plate-recovered.png`;
- recovered artifact is a valid 1024×1024 RGB PNG, 1,912,084 bytes;
- final balance remained 4003.64;
- no synthetic cache/provenance entry was authored.

Sean confirmed the receipt resolved. Only then were the exact recovered run's intent and lock markers removed.

## 6. State-of-record and next boundary

No success state was flipped:

- `CLAUDE.md` and `AGENTS.md` still say Task 7 live transport has not been verified;
- backlog §7 and transport-decision §T1 remain unchanged;
- no PR was opened;
- no second live generation or edit-of-edit ran.

The next contained fix is to accept the observed one-element string-array acknowledgment as the create job ID, keep flat-dict parsing for wait/get, turn the captured fixture regression GREEN, rerun both test directories separately, and require a fresh Sean GO before any new ~4-credit verification.

Still gated afterward: **T2** GRANDMASTER in-register Bible-pass identity validation and **T4** Motion→Higgsfield Seedance wiring.
