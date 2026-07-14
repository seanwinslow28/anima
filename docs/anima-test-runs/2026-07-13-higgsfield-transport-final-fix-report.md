# Higgsfield transport consolidated final-fix report

**Date:** 2026-07-13  
**Worktree:** `/Users/seanwinslow/Code-Brain/anima/.claude/worktrees/feature+higgsfield-transport`  
**Starting HEAD:** `2d68fb6be4723024440c7f0607bed8428f8d585e`  
**Fix commit:** `743da27` (`fix(transport): preserve charged jobs and honest caches`)  
**Second re-review fix commit:** `4923b18` (`fix(transport): fail closed on uncertain receipts`)  
**Third re-review fix commit:** `4a1d1e0` (`fix(transport): guard pre-create uncertainty`)  
**Fourth durability fix commit:** `56a2f47` (`fix(transport): make receipt transitions durable`)  
**Execution boundary:** Task 7 did not run. No live Higgsfield, Gemini, OpenAI, fal, or other model generation ran. Every pytest command below used `ANIMA_FORCE_STUB=1`; every test that deliberately entered a real-shaped branch installed its fake subprocess/API seam before clearing the force-stub variable locally.

## Outcome

All final-review groups are resolved across four contained fix waves:

1. Charged Higgsfield jobs survive the complete create-through-publication uncertainty window. A durable pre-create intent blocks ambiguous duplicate creates; known identities upgrade to an atomic, validated pending or quarantine receipt; identical retries recover the same job before any create; download and wait retries are bounded; and terminal failures return a non-ok identity-bearing response.
2. Gemini forced/no-key/missing-script placeholders do not read or publish the real cache. Forced stub wins before cache lookup, so an identical later mocked-live invocation executes and publishes real-shaped bytes.
3. The register backlog, ROADMAP counts/history, and manifest transport comment agree with current code: four authored expansion registers, ten total, seven Gemini-direct generation defaults plus three `gpt-image-2`/Higgsfield registers.
4. A stdlib `fcntl.flock` per cache key covers the second cache/pending check through generation, download, and complete cache publication. The OS-level lock is proven exclusive across processes.
5. The completed animation-vocabulary execution plan moved from `docs/active/` to `docs/COMPLETED/`, gained a completed/historical banner, retained its historical preview IDs/body, and every inbound link plus its two move-sensitive internal links was updated.

The earlier helper minor was adjudicated **DONE**: mocked-real Gemini helpers now require their fake generator/image bytes explicitly. This improves fail-loud test setup without production scope churn.

## Second final re-review wave

The first fix commit received a second re-review with four additional charged-job receipt findings and one stale docstring link. All five are closed without live generation.

### Second-wave RED

Command:

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest tests/test_higgsfield_runner.py -q
```

Observed before second-wave production edits:

```text
5 failed, 30 passed in 0.24s
```

Expected failures:

- create-time `TimeoutExpired.output` was ignored, so `job-create-timeout` identity was absent and an identical retry could create again;
- canonical pending-write `OSError` escaped instead of preserving the successful create's identity;
- malformed and CLI-version-stale receipts were deleted, followed by a create (exit 1 instead of actionable exit 78);
- an expired retained URL exhausted downloads and returned without using the valid job ID to refresh via `generate wait`.

### Second-wave GREEN

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest tests/test_higgsfield_runner.py -q
35 passed in 0.17s
```

New behavior proven:

- create-timeout stdout/output and stderr are parsed; known identity is persisted before an exit-124 response; identical retry performs zero additional creates;
- pending-write failure uses an independent low-level + fsync + replace quarantine path, returns identity-bearing exit 78, and every identical retry remains blocked pending operator resolution;
- invalid/version-stale receipts remain byte-preserved and block create with an actionable error;
- an expired URL performs three bounded old-URL downloads, one same-ID wait, atomically persists the replacement URL, and succeeds on the refreshed URL with zero creates.

The lock remains one per-key critical section. Receipt/quarantine inspection, wait refresh, downloads, and publication all occur under that existing lock. The quarantine writer acquires no lock, so the second wave introduces no nested-lock or lock-order edge.

## Third final re-review wave

The second fix commit received one final contained correction: close the identity-free window before `create --wait`, validate the identity returned by every same-job wait, and correct this report's stale invalid-receipt cleanup statement. No live generation or Task 7 work ran.

### Third-wave RED -> GREEN

The output-less timeout regression failed first because two identical invocations each reached create:

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest tests/test_higgsfield_runner.py::test_outputless_create_timeout_intent_blocks_duplicate_create -q
1 failed in 0.07s
```

After the pre-create intent primitive landed, the same regression passed with exactly one create and an actionable exit-78 retry. The pre-intent publication regression also proves a write failure reaches zero creates.

The dual post-create publication regression then failed first because the quarantine `OSError` escaped:

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest tests/test_higgsfield_runner.py::test_pending_and_quarantine_write_failure_retains_create_intent -q
1 failed in 0.08s
```

It now returns an identity-bearing exit 78, retains the durable create intent, and performs exactly one create across the original invocation and identical retry.

The same-ID validation regression failed first because a wait response for `job-other` overwrote `job-original`, attempted six downloads, and returned exit 1:

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest tests/test_higgsfield_runner.py::test_wait_job_id_mismatch_preserves_original_receipt_and_fails_closed -q
1 failed in 12.11s
```

It now returns exit 78 with `job-original`, preserves the original pending receipt byte-for-byte, and performs one wait with zero creates, downloads, or cache publications. The complete Higgsfield runner suite is green at 39 tests.

The final durability sensitivity check then observed only the intent's two fsyncs and failed `assert 2 >= 4`; the canonical pending receipt still used replace without fsync. The pending and quarantine writers now fsync the staged file and parent directory before they can supersede the intent. The publication regression passes with at least four fsyncs across intent + pending.

### Third-wave safety ordering

- The intent is atomically replaced, file-fsynced, and directory-fsynced under the existing per-key flock before the first charged command.
- An intent publication failure returns before create. Identity-free timeout/failure leaves the intent operator-visible and blocks identical automatic retries.
- Known metadata publishes pending first; only a durable pending or durable quarantine permits intent removal. If both fail, the intent remains.
- Any intent left beside a visible receipt marks an incomplete transition and blocks automatic recovery; only the same invocation's explicit durable outcome can authorize durable intent removal.
- Same-ID validation occurs before metadata merge, receipt rewrite, download, or cache publication in every wait path.
- No helper acquires another lock, so there is no nested-lock or lock-order edge.

## Fourth durability audit wave

The narrow post-wave audit found two remaining crash-consistency gaps: callers still inferred successor durability from path visibility, and the cache pair plus receipt removals were not fsynced. Both are closed without live generation or Task 7.

### Fourth-wave RED -> GREEN

The visible-receipt fault first failed because pending and quarantine renames both existed after their directory fsyncs raised, and the old `Path.exists()` branch removed the intent:

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest tests/test_higgsfield_runner.py::test_visible_receipts_without_directory_fsync_retain_create_intent -q
1 failed in 0.07s
```

`_persist_pending_or_failure` now returns `PendingPersistenceResult` with the explicit enum outcome `DURABLE_PENDING`, `DURABLE_QUARANTINE`, or `NOT_DURABLE`, plus any response. Only the first two outcomes authorize durable intent removal. The regression is green with identity-bearing exit 78, visible-but-unconfirmed receipts, retained intent, and one create across identical retry.

The success-order regression then failed because only intent removal used the durable-unlink seam and the cache pair contributed no fsyncs:

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest tests/test_higgsfield_runner.py::test_cache_publishes_valid_provenance_before_image -q
1 failed in 0.08s
```

The green sequence is exactly nine fsyncs: four staged files (intent, pending, provenance, image) and five parent-directory transitions (intent publication, pending publication, intent removal, cache-pair publication, pending removal). Publication remains provenance-before-image.

Additional fault injection proves:

- cache renames whose parent-directory fsync fails return non-ok and retain pending;
- intent-unlink fsync failure returns exit 78 before download while durable pending remains;
- pending-unlink fsync failure cannot report success even though the cache pair is already durable.

The crash-transition order is now: durable intent → durable pending/quarantine → durable cache pair → durable pending removal. Every step stays under the one existing per-key flock; fsync and unlink helpers acquire no lock.

## Strict RED -> GREEN evidence

### RED 1: Higgsfield receipt/retry/timeout/lock behavior

Command:

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest tests/test_higgsfield_runner.py -q
```

Observed before production edits:

```text
3 failed, 27 passed in 5.13s
```

Expected failures:

- `test_completed_job_download_failure_resumes_without_duplicate_create`: `TimeoutError: cdn timed out` escaped from `_download`; no pending receipt/recovery existed.
- `test_resume_timeout_returns_known_job_identity`: `subprocess.TimeoutExpired` escaped from the same-ID wait path.
- `test_cache_key_lock_is_exclusive_across_processes`: child failed with `AttributeError` because `_cache_key_lock` did not exist.

GREEN after the minimal behavior implementation and deliberate update to the existing atomic-publication test:

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest tests/test_higgsfield_runner.py -q
30 passed in 0.21s
```

The completed-job regression asserts all of the following:

- one create total across the failed first invocation and identical retry;
- exactly three bounded failed downloads, then one recovery download;
- pending receipt exists and contains the known job ID/result URL before every download;
- first response is non-ok and retains `job_id`, `result_url`, `display_name`, and `cli_version`;
- second response succeeds on the same job and clears the receipt only after cache publication.

The publication regression observes atomic destination order:

```text
<key>.pending.json -> <key>.provenance.json -> <key>.png
```

and proves the pending receipt still exists when the cache image becomes visible, then is removed afterward.

### RED 2: Gemini forced-stub cache poisoning

Command:

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest tests/test_nb_pro_runner.py::test_force_stub_placeholder_never_poisoned_real_cache -q
```

Observed before production edits:

```text
1 failed in 0.04s
assert calls["n"] == 1
E assert 0 == 1
```

The forced placeholder had populated the real cache, so the identical mocked-live request returned it without calling the safely mocked subprocess.

GREEN after moving forced stub before cache lookup and removing placeholder publication from all safe stub fallbacks:

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest tests/test_nb_pro_runner.py::test_force_stub_placeholder_never_poisoned_real_cache -q
1 passed in 0.03s

ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest tests/test_nb_pro_runner.py -q
17 passed in 0.05s
```

The old cache-hit test was intentionally converted to a mocked-real first publication. It still proves a second identical real-shaped request is a cache hit and that the contained subprocess ran once.

## Implementation notes

### Higgsfield runner

- `_cache_key_lock`: per-key interprocess exclusive lock using `fcntl.flock`.
- `_read_valid_pending`: rejects malformed, incomplete, wrong-key, wrong-parameter, or wrong-CLI receipts.
- `_atomic_write_json`: temp-file plus `os.replace` receipt publication.
- `_persist_pending`: runs immediately after create/wait metadata reveals a job ID or result URL.
- `_download_with_retries`: three bounded attempts; removes partial output and catches downloader exceptions.
- `_resume_existing_job`: three bounded same-ID attempts; converts `TimeoutExpired` into exit 124 without losing job ID.
- `_recover_pending_job`: re-downloads a known URL or resumes a known ID before any create.
- `_finish_known_job`: retains pending receipt through download and atomic provenance/image publication; clears it only after success.
- All known-identity terminal paths return a non-ok `HiggsfieldResponse` carrying known provenance.

### Gemini runner and helper containment

- `ANIMA_FORCE_STUB` is checked after key computation but before `cached_file.exists()`.
- Forced, missing-key, and missing-script placeholders write only the requested output path.
- The mocked-real NB helper requires explicit `image_bytes` and installs `subprocess.run` before clearing force stub.
- The Gemini API `_force_real` helper requires explicit `generate`; its ordering guard still proves `_generate` is replaced before force stub is cleared.

## Documentation dispositions

- `docs/active/2026-07-04-register-backlog-and-transport-findings.md`: Samurai transport/authoring and Nicktoon authoring/pending-action text reconciled.
- `ROADMAP.md`: historical outward-turn paragraph now says four authored expansion registers and ten total, matching current focus/count text.
- `manifest.yaml`: comment now states seven Gemini-direct generation defaults and three gpt-image/Higgsfield defaults; executable manifest values did not change.
- `docs/COMPLETED/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md`: archived with historical banner; preview model IDs and historical execution body retained.
- All old `docs/active/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md` inbound links were changed to `docs/COMPLETED/...` with correct relative paths.
- `CHANGELOG.md`: records what/why and review dispositions, including the still-gated T2 and Task 7 work.

## Verification evidence

Final fourth-wave verification, run as separate forced-stub commands:

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest tests/test_higgsfield_runner.py -q
43 passed in 0.20s

ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest \
  tests/test_higgsfield_runner.py tests/test_nb_pro_runner.py \
  tests/test_gemini_api_runner.py tests/test_register_registry.py \
  tests/test_register_characterization.py tests/test_prompt_style_neutrality.py -q
141 passed, 1 warning in 0.71s

ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest tests/ -q
988 passed, 2 warnings in 18.39s

ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest pipeline/tests/ -q
10 passed in 0.04s
```

Final third-wave Higgsfield verification:

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest tests/test_higgsfield_runner.py -q
39 passed in 0.16s
```

Final third-wave focused verification:

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest \
  tests/test_higgsfield_runner.py tests/test_nb_pro_runner.py \
  tests/test_gemini_api_runner.py tests/test_register_registry.py \
  tests/test_register_characterization.py tests/test_prompt_style_neutrality.py -q
137 passed, 1 warning in 0.74s
```

Final third-wave full verification, run separately:

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest tests/ -q
984 passed, 2 warnings in 17.77s

ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest pipeline/tests/ -q
10 passed in 0.03s
```

Final second-wave focused verification:

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest \
  tests/test_higgsfield_runner.py tests/test_nb_pro_runner.py \
  tests/test_gemini_api_runner.py tests/test_register_registry.py \
  tests/test_register_characterization.py tests/test_prompt_style_neutrality.py -q
133 passed, 1 warning in 0.66s
```

Final second-wave full verification:

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest tests/ -q
980 passed, 2 warnings in 18.42s

ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest pipeline/tests/ -q
10 passed in 0.04s
```

Focused runners/registry/neutrality:

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest \
  tests/test_higgsfield_runner.py tests/test_nb_pro_runner.py \
  tests/test_gemini_api_runner.py tests/test_register_registry.py \
  tests/test_register_characterization.py tests/test_prompt_style_neutrality.py -q
128 passed, 1 warning in 0.74s
```

Full primary suite:

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest tests/ -q
975 passed, 2 warnings in 18.66s
```

Separate pipeline suite:

```text
ANIMA_FORCE_STUB=1 .venv/bin/python -m pytest pipeline/tests/ -q
10 passed in 0.04s
```

Warnings are dependency deprecations only: Starlette `TestClient`/httpx and google-genai `_UnionGenericAlias`.

Static/diff checks:

```text
git diff --check
# exit 0, no output

.venv/bin/python -m py_compile pipeline/agents/higgsfield_runner.py \
  pipeline/agents/nb_pro_runner.py tests/test_higgsfield_runner.py \
  tests/test_nb_pro_runner.py tests/test_gemini_api_runner.py
# exit 0
```

AST/import-order review: all five changed Python files parse; stdlib imports are grouped and ordered; no new third-party dependency was introduced.

Frozen guards:

```text
md5 -q evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md
2af75906502f1caf8857e18828ceb2e4

md5 -q pipeline/agents/prompts/sean-screenwriting-voice.md
945af824fa53b948a18ac6bf206d67ef
```

Archive/link check:

```text
find docs/active -maxdepth 1 -name '2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md' -print
# no output

test -f docs/COMPLETED/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md
# success

rg -n 'docs/active/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md|\.\./active/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md|\(2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md' --glob '*.md' .
# no output
```

Live preview-ID check:

```text
rg -n 'gemini-3\.1-flash-image-preview|gemini-3-pro-image-preview' \
  pipeline manifest.yaml tests .claude/skills docs/architecture docs/active \
  --glob '!docs/active/2026-07-13-transport-strategy-decision.md' \
  --glob '!docs/active/2026-07-13-higgsfield-switchover-build-kickoff.md'
# no output
```

The two excluded dated docs deliberately describe the preview-to-GA decision/build instruction and remain historical evidence; runtime code/config/tests/current skills are clean. The archived converged plan deliberately retains its historical preview IDs per review instruction.

## Self-review and remaining concerns

- Confirmed the lock scope begins before the second cache/pending check and ends after download/publication or terminal response.
- Confirmed invalid cache pairs are removed only inside the lock; invalid or version-stale pending receipts are preserved byte-for-byte and remain operator-visible.
- Confirmed URL-only receipts recover without requiring a CLI; ID-only receipts never create when the CLI is absent.
- Confirmed create-timeout identity is recovered from both text/bytes output and stderr before return.
- Confirmed invalid/stale and quarantined receipts take precedence over cache/create and remain operator-visible.
- Confirmed expired-URL refresh reuses the known ID under the same lock and has only one bounded refresh cycle per invocation.
- Confirmed publication failure returns non-ok with identity and retains the pending receipt.
- Confirmed forced Gemini stub cannot read an existing real cache entry and no placeholder branch writes cache bytes.
- No unresolved implementation concern found in the requested scope.
- Standing product gates remain explicit: the costed T2 GRANDMASTER across-edit identity validation and Task 7 production-path live smoke are not performed here.
