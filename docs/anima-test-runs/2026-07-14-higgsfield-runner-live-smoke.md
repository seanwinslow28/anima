# Field report — Higgsfield runner live smoke (Task 7): DEFECT FOUND

**Date:** 2026-07-14 · **Session:** the [Higgsfield live smoke + closeout kickoff](../active/2026-07-14-higgsfield-live-smoke-and-closeout-kickoff.md) — Task 7 of the [ratified transport switchover](../active/2026-07-13-transport-strategy-decision.md) (plan §T1's final live gate).
**Outcome:** **SMOKE FAILED at the runner level — the transport generation SUCCEEDED.** The live smoke did exactly what Task 7 exists to do: it caught a real runner defect that the $0 stub-green suite could not. **No state-of-record docs were flipped** (per the kickoff's FAILED branch); the runner's fail-closed behavior is itself the evidence, and this report + the defect list below feed a separate fix session.
**Spend:** **4 Higgsfield credits** (balance 4011.64 → 4007.64), one charged job, no refund (the job completed; the failure was on anima's parse side, not Higgsfield's). Extra-capture spend **deferred** (Sean's call).

---

## 1. What ran

First real generation through the **production seam** (`invoke_image_edit`, the path Cy/Flo call — NOT raw CLI, because the runner is what Task 7 validates):

```python
from pathlib import Path
from pipeline.agents.nb_pro_runner import invoke_image_edit
resp = invoke_image_edit(
    prompt=("Same character as the reference image. Full-body three-quarter "
            "view model plate, standing neutral. Keep the face, hairstyle, "
            "outfit, and proportions exactly the same as the reference. "
            "Same raw gritty hand-inked style as the reference."),
    reference_images=[Path("registers/primal-sketch-grit/refs/grandmaster-chosen-pose-1.png")],
    output_path=Path("runs/2026-07-14-higgsfield-smoke/plate.png"),
    cache_dir=Path("runs/2026-07-14-higgsfield-smoke/.cache"),
    model="gpt-image-2",
)
```

> **Reference-path correction:** the kickoff snippet named `registers/primal-sketch-grit/refs/primal-sketch-grit-hero.png`, which does not exist on disk. The real primal exemplar is `grandmaster-chosen-pose-1.png` — exactly what red-team ledger item #11 (CHANGELOG 2026-07-13) specified Task 7 should use. The kickoff prose carried the stale path; the run used the real file.

## 2. The response — fail-closed, not silent

```
HiggsfieldResponse(
  ok=False, exit_code=1, stub_fallback=False, cache_hit=False,
  job_id=None, result_url=None, display_name=None, error=None,
  cli_version='0.2.3',
  cache_key='70821efdc0906821bd23edb8282af17fcc2e4ab56c16c8d846f0b1658d6751d3',
)
```

- **NOT exit-78.** It was a plain `exit_code=1` hard failure with no captured job identity (`job_id`/`result_url` both `None`, `error` unset).
- **The fail-closed design held.** The runner left the pre-create `…​.create_in_flight.json` intent marker on disk, so an identical retry would have been **blocked (exit-78), never silently re-charged**. No `plate.png` was written (the runner failed before download).

## 3. The surprise: a job WAS charged and DID complete

- **Balance moved:** 4011.64 → **4007.64** = **4 credits** — a real charged job, despite `job_id=None` in the response.
- **Recovered read-only** via `higgsfield generate list --json`:
  - `id`: `631ecdb7-2fb2-440d-b58b-fb29d1291bd5`
  - `status`: **completed**
  - `job_set_type`: `gpt_image_2` · quality `high` · resolution `1k` · `aspect_ratio` `1:1` (CLI-defaulted from our `None`) · internal `model: videotape-alpha`
  - `result_url`: a valid CloudFront PNG (retained ~7 days)
  - `prompt`: matches the call exactly; one input media, `role: image` (the anchor).
- The result was downloaded to `runs/2026-07-14-higgsfield-smoke/plate-recovered.png` (1.95 MB; `runs/` is gitignored — local evidence only). Named `-recovered` on purpose: the runner did not produce it, the operator did.

## 4. Root cause — pinned to the combined `create --wait` path

The runner (`_invoke_real`) issues **one combined command**:

```
higgsfield generate create gpt_image_2 --prompt "…" --quality high --resolution 1k \
  --wait --wait-timeout 9m --json --image <anchor>
```

This command **charged, the job completed, but it exited nonzero and its stdout was not what `_parse_cli_output` expects** (no top-level `id`/`result_url` were extracted; the fallback bare-`https://` token scan also missed — pretty-printed JSON tokens are quoted, e.g. `"https://…​.png",`, which fails `startswith("https://")`).

Verified **read-only** (no spend) against the already-completed job that the standalone commands are fine:

| Command | Exit | Output shape |
|---|---|---|
| `generate get <job_id> --json` | **0** | clean flat JSON dict, top-level `id` + `result_url` |
| `generate wait <job_id> --json` | **0** | clean flat JSON dict, top-level `id` + `result_url` |
| `generate create … --wait --json` | **1** (charged) | not parseable by the runner (exact bytes not captured — see §6) |

So `_parse_cli_output` is correct for `get`/`wait`; the **combined `create --wait` is the fragile path**. This is consistent with the runner's own recovery path (`_resume_existing_job`) already using the *flat* `generate wait <job_id>` shape successfully in its unit tests — the create path is the one the stub suite never exercised against a real CLI.

## 5. Indicated fix (for a separate fix session — NOT applied here)

**Decouple create from wait**, mirroring the already-working resume path:

1. `generate create <job_type> … --json` **without** `--wait` → capture `job_id` (and `result_url` if the ack carries it).
2. `generate wait <job_id> --json` → block to completion (the flat shape the runner already parses correctly).
3. Download + publish + provenance as today.

This also tightens the charged-job-identity guarantee: the `create` ack yields the `job_id` **before** the long wait, so a create that charges can never again land in "charged but no identity captured." Harden `_parse_cli_output`'s fallback URL scan to strip JSON punctuation, and add a regression fixture built from the real `create --wait` output (capture it in the fix session — see §6). Re-verifying the fix costs one more charged create (~4 cr, Sean-gated).

## 6. Deferred (Sean's call, this session)

- **Exact `create --wait --json` stdout/stderr/exit capture:** deferred to the fix session, which will reproduce + capture it while verifying the fix anyway (avoids a second charged job for a smoke). The defect is already pinned without it.
- **Cache-hit proof (kickoff Phase 1.2):** not demonstrable — the runner never published a cache entry (it failed before download). Deferred to post-fix verification.
- **Edit-of-edit (kickoff Phase 1.4):** moot until the runner path is fixed.

## 7. Sean's eye — the generation half (PASS)

Sean reviewed `plate-recovered.png` against the hero (`grandmaster-chosen-pose-1.png`). **Verdict: PASS — both hold.** gpt_image_2 via Higgsfield produced a clean 3-view model sheet (front / ¾ / profile) of the same character — same headband, dirty tank top, shorts, worn boots, tousled black hair, scowl — and the `primal-sketch-grit` register held (heavy hand-inked line, dry-brush grit, cream ground, muted earthy palette; not cleaned up).

**Caveat (recorded):** this validates the **transport's generation capability** for the in-register plate, **not** the runner's parse/download/cache path, which failed. It is a smoke-level single plate (n=1), not the T2 GRANDMASTER Bible-pass identity gate — which remains standing and Sean-gated.

## 8. Receipt resolution (operator action taken, $0)

The charged job `631ecdb7…` is confirmed **completed and recovered**, so the "uncertain state" is resolved. The `…​.create_in_flight.json` intent marker and the `…​.lock` file were removed. **No synthetic cache entry was hand-published** — the fix session gets a clean slate to test the real create → wait → download → cache path end-to-end. Final balance confirmed stable at **4007.64** (no further spend).

## 9. State-of-record: deliberately NOT flipped

Per the kickoff's FAILED branch, `CLAUDE.md` / `AGENTS.md` keep **"Task 7 live transport has not been verified"** — because it now reads more precisely as *verified-to-fail with a pinned defect*, not *verified-working*. The backlog and decision-doc §T1 status are unchanged. This report + the CHANGELOG entry are the record; the fix session flips state only after a green re-run.

## 10. What stays gated (unchanged)

- **T2** — the in-register (primal) Bible-pass edit-identity validation (rides the costed, Sean-greenlit GRANDMASTER build).
- **T4** — Phase-6 Motion wiring to Higgsfield Seedance (when Motion enters the orchestrator).

## Appendix — verification ledger (all $0 except the one 4-cr create)

| Check | Result |
|---|---|
| `main` carries #113 | ✅ `8f1f114` |
| Contract suite `tests/` (forced-stub) | ✅ 988 passed |
| Seedance suite `pipeline/tests/` (forced-stub) | ✅ 10 passed |
| Merged worktree + 3 branches + stale remotes | ✅ torn down; `final-fix-report.md` preserved to `docs/anima-test-runs/2026-07-13-higgsfield-transport-final-fix-report.md` |
| `ANTHROPIC_API_KEY` / `ANIMA_FORCE_STUB` | ✅ both absent |
| `higgsfield --version` | ✅ `0.2.3` (pin exact — runner did not fail-close on version) |
| Auth / balance | ✅ ULTRA, 4011.64 → 4007.64 |
| Cost dry-run gpt_image_2 high 1k | ✅ 4 cr (matched actual) |
