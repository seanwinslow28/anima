# Kickoff — Run Orchestrator, Slice 1: the cleanup pass ($0, TDD)

*Paste the block below into a fresh Claude Code session in the `anima` repo. It is self-contained.
Plan of record: [`docs/2026-06-11-run-orchestrator-build-plan.md`](2026-06-11-run-orchestrator-build-plan.md).*

---

You're building **Slice 1 of the run orchestrator: a $0, TDD cleanup pass** that fixes three
seams the first integrated run logged. No model spend — this is pure code + unit tests. The
seams are in [`docs/anima-test-runs/2026-06-11-first-integrated-run.md`](../../anima-test-runs/2026-06-11-first-integrated-run.md);
the full arc is in [`docs/2026-06-11-run-orchestrator-build-plan.md`](2026-06-11-run-orchestrator-build-plan.md).
Read both before touching code. Then read `PHILOSOPHY.md` and `CLAUDE.md` if not already in context.

**The three fixes, all independent:**

1. **#5 — `cost_estimator._phase_2_cost` double-counts locked Bibles** (~$5.40 phantom Phase-2 band on an `animation_piece` run).
2. **#12 — Gemini saves JPEG-as-`.png`** (ffmpeg's PNG decoder rejects it) — normalize at the source.
3. **#13 — `assemble.sh` is hardcoded to the PT_A1 sequence** — generalize it, PT_A1 stays byte-identical.

**Explicitly OUT of scope:** seam #10 (Em's stylus-hand verdict). It changes Em's verdicts and
carries eval-baseline blast radius — it is a separate eval-gated track. Do not touch
`evals/vision_critic/` for any reason this session.

## Doctrine — non-negotiable

- **Verify against the tree, never trust a label — including this kickoff.** Every diagnosis
  below was checked this session, but re-confirm each against the live tree before you fix it
  (grep the function, read the file, run the failing case). Cautionary tales that earned this:
  a runbook claimed a loop self-isolates and the run crashed on case #0; a docstring lied about
  `agy -m`; Flo's CHANGELOG read "built" while nothing dispatched it.
- **The Em verdict-baseline guard:** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md`
  must stay `2af75906502f1caf8857e18828ceb2e4` at the end. Nothing here should reach
  `evals/vision_critic/` — if you find yourself there, stop.
- **TDD, red→green, one bug per commit.** Write the failing test first, confirm it's red for the
  right reason, fix, confirm green. Three independent commits so each fix is revertible alone.

## §0 — fleet-ops gates (before any edit)

Per [`docs/fleet-ops-protocol.md`](../../architecture/fleet-ops-protocol.md). This is $0, but the worktree
discipline still applies — the 2026-06-10 path-leak incident happened on a $0 session.

```bash
cd <anima main checkout>
git fetch origin
git log --oneline -1 origin/main          # expect f157564 (#48) or newer
git rev-list --left-right --count origin/main...HEAD   # expect divergence 0 0 on a clean base
md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md  # 2af75906502f1caf8857e18828ceb2e4
echo "${ANTHROPIC_API_KEY:-ABSENT}"        # expect ABSENT (no spend possible anyway; keep the habit)
```

Create one isolated worktree off `origin/main` and do ALL edits inside it (after the worktree
switch, the worktree path is the only valid edit root — treat a surprising test-collection
count as an isolation tell, and spot-check `git -C <main> status -s` is clean after your first edit).

Baseline the suites green before you start:

```bash
python -m pytest tests/ -q          # the contract suite
python -m pytest pipeline/tests/ -q # Seedance select/cleanup (must run separately — duplicate `tests` basename)
```

## Fix #5 — cost estimator skips locked Bibles

**Re-verify the diagnosis.** Read `pipeline/agents/cost_estimator.py::_phase_2_cost`. Confirm
it prices every non-`ingest:` plate from each registered character's `plate_generation_plan.json`
and never checks lock state. Confirm both `characters/sean-anchor/acceptance_criteria.json` and
`characters/claude-mascot/acceptance_criteria.json` are `locked: true`. Confirm the docstring
claims animation-piece runs "don't re-pay" — the bug is that it only zeroes when there's *no*
`characters:` block, not when the registered Bibles are locked.

**Test first** (`tests/test_cost_estimator.py`, hermetic tmp fixtures — do NOT point at the real
`characters/`): a manifest registering a character whose `acceptance_criteria.json` is
`locked: true` (with a plate plan present) → `phase_2` band is `$0.00`. A second case: an
unlocked character with a plate plan → prices the plates exactly as today (lock the current
behavior so the fix stays surgical).

**Fix.** In `_phase_2_cost`, per character, detect lock via the character's own
`<folder>/acceptance_criteria.json` `locked: true` — the authoritative per-Bible signal that
`pipeline.cli bible approve` flips and `pipeline/criteria.py::load_criteria(...).locked` reads.
Locked → contribute $0 (skip). No lock file / `locked: false` → price as today. Don't invent a
new manifest flag; read the on-disk lock.

## Fix #12 — normalize JPEG-as-PNG at the source

**Re-verify.** `python3 -c "from PIL import Image; print(Image.open('runs/2026-06-11-spark-shared-first-integrated/approved/SS_F01_key.png').format)"`
→ `JPEG`. Confirm every generation route funnels through `FloNode.run`
(`pipeline/agents/frame_router.py`) emitting `candidate_path`. Confirm `pipeline/assemble.sh`
already has a "Step 2b" PIL re-encode (the existing backstop — keep it).

**Test first.** Unit: write JPEG bytes to a `*.png` tmp path, run the new `normalize_to_png`,
assert `Image.open(path).format == "PNG"`; assert it's idempotent on an already-PNG file (no
needless rewrite). Then a FloNode-level test (stub transport) that a JPEG-as-PNG candidate
comes back as PNG from `FloNode.run`.

**Fix.** Add a small `normalize_to_png(path)` helper (open with PIL; if `format != "PNG"`,
re-save as PNG in place) and call it at the `FloNode.run` return boundary, before
`candidate_path` is handed back — so Em, assemble, and the future museum capture all get a real
PNG. Pick the helper's home during the build (a `pipeline/` util or alongside `generate.py`);
the call site is the FloNode boundary regardless. Keep `assemble.sh` Step 2b as the backstop.

## Fix #13 — generalize `assemble.sh` (PT_A1 byte-identical)

**Re-verify.** Read `pipeline/assemble.sh`. Confirm the hardcoded `FRAME_SEQ`, the
`PT_A1_${ASSET}.png` source prefix, the `pencil-test-act1.{mp4,webm,gif}` output names, and the
`1920×1080` scale. Read `pipeline/nodes/assemble.py` — the `assemble` node shells to the script
with `run_dir` only, and its docstring makes byte-identical back-compat the verification anchor.

**Test first — the load-bearing one.** A golden back-compat test: assembling the PT_A1 reference
sequence with no new args produces a **byte-identical** frame sequence + the same output
filenames as before (mirror how Flo-C regression-locked the NB-Pro cache key against a captured
golden digest). Then a positive test: a small custom sequence + slug (e.g. two `SS_*` keys with
holds `2,2`) produces slugged outputs from the right sources. Hermetic — tmp run dir, tiny
generated PNGs, don't shell out to a real ffmpeg if you can assert on the staged `sequence/`
+ planned output names instead (keep it fast and CI-safe).

**Fix.** Let the assembler take an optional **sequence spec** (an `export/sequence.txt` in the
existing internal `KEY:hold` line format) + an optional **`--slug <name>`** (and derive the
source-path prefix from the keys, e.g. `SS_F03b_key`, not `PT_A1_*`). When neither is supplied,
fall back to the embedded PT_A1 `FRAME_SEQ` + `PT_A1_` prefix + `pencil-test-act1` slug — today's
behavior, byte-identical. Keep Step 2b. Thread optional `slug` / `sequence_file` through
`AssembleNode` inputs (default → legacy) so Slice 2's orchestrator can drive it; absent inputs =
today's behavior.

## Done criteria

- All three fixes landed, each its own commit, each red→green.
- `python -m pytest tests/ -q` and `python -m pytest pipeline/tests/ -q` green.
- The PT_A1 golden back-compat test proves `assemble.sh` is byte-identical on the legacy path.
- `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` == `2af75906502f1caf8857e18828ceb2e4`.
- `git -C <main> status -s` clean (no worktree path leak).
- **CHANGELOG.md** entry in the decision-log voice (what + why per fix, the md5-guard line, the
  test counts). **CLAUDE.md** touched only if a convention/command changed — the assembler's new
  sequence/slug interface likely warrants a one-line note in the assemble command block; don't
  over-edit.
- Land as a single squash PR off `origin/main`. Clean teardown of the worktree.

When you're done, report: the three diffs in one line each, the before/after `_phase_2_cost`
band on a locked-Bible manifest, the golden-test digest, and the final test counts.
