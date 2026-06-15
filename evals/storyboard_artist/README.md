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
