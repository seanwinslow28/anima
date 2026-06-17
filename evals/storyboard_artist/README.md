# Storyboard Artist (Bea) — eval suite

Scaffold-stage eval suite for **Bea**, the Phase-3b storyboard artist. Mirrors
`evals/scriptwriter/`. Seeded from the real "Spark, Shared" anima board.

## What it checks (and deliberately doesn't)

**Positive case** validates that a beat_id-annotated ground-truth board round-trips
through `pipeline/orchestration/shots.py:load_shots` **and** passes Bea's
deterministic `pipeline.agents.storyboard_artist.storyboard_validate` (coverage +
no-orphans + the script↔board cast-conflict check) against its source beat sheet.
This is the beats→board plumbing/coverage contract.

- `spark-shared-board-plumbing` — the beat_id-annotated Spark board derived from the
  shipped `briefs/2026-06-10-spark-shared/shots.yaml`. (It is **not** byte-identical
  to the shipped file, which carries no `beat_id`; that back-compat is guarded by
  `tests/test_spark_shots_equivalence.py`.) Note beat 3 ("The notice") is mascot-only
  yet its fixed-camera two-shot boards both characters — legal under the rule
  `beat.cast ⊆ shot.cast` (the board may add characters, never drop one).

**Ships-red cases** are Bea's **named, deterministic** failure modes. Unlike Sam's
by-ear voice defects (which `xfail`), `beat_id` makes the beat↔shot link checkable,
so these are **green catches**: `storyboard_validate` must raise.

| Case | Detector | Result |
|------|----------|--------|
| `coverage-gap` | `structural` | **green** — a beat with no shot raises "coverage gap" |
| `orphan-shot` | `structural` | **green** — a shot at a non-existent beat raises "orphan" |
| `cast-conflict` | `structural` | **green** — a shot dropping its beat's character raises "conflict" |

**Prompt-quality lint (Tier 1 Slice A, 2026-06-17).** `checks.py:edit_frame_form_lint`
is a deterministic **warning** — the analogue of Sam's `default_prop_lint`, and the
ONE prompt-quality check the first costed-run post-mortem (Findings 2/3) sanctions.
On a chained pencil-test loop, frame 1 is the establishing generation (a full
descriptive prompt) but every later frame is an NB2 *edit* off the prior approved
frame and must be a terse delta — `Same … ONLY CHANGE: <delta>`, or the loop-return
match `composition identical to frame 1` — not a full re-description (verbose prose
competes with the reference and drifts identity). It is **never** wired into
production `storyboard_validate`; the human still curates at the gate.

| Case | Detector | Result |
|------|----------|--------|
| `edit-form-accepted` | `edit_frame_form` | **green** — frame 1 full + frames 2–4 `ONLY CHANGE:` + frame 5 loop-return match → lint accepts (no offenders) |
| `full-redescription-on-edit-frame` | `edit_frame_form` | **green** — frame 2 a full re-description → lint flags it |

## Deliberately deferred (campaign items)

- **Composition pairwise-preference harness.** Whether a board *reads well* —
  framing, the loaded-object choice, the prose-action prompt's voice — is a by-ear
  call the AI-evals handbook bars an LLM aesthetic judge from making. That harness
  (Bea's equivalent of Sam's deferred voice harness) is a campaign item; v1 ships
  the structural contract only. The human gate (`storyboard approve`) owns taste.
- **The Sonnet/Gemini/Codex model bake-off.** Bea's model assignment (Sonnet 4.6)
  is the roster's lowest-confidence pick; the three-way bake-off is the parked
  hardening campaign, not a v1 blocker.

## Run

```bash
python -m pytest evals/storyboard_artist/runner.py -v
```

(Named `runner.py`, so default discovery skips it — run it explicitly.)
