# The Museum capture layer — what shipped, what backfilled, what we learned

*2026-05-31 · branch `feature/museum-capture-layer` · 207 → 230 tests*

## What this was

The one unbuilt piece serving both of Sean's goals at once: ship Act 2, and make
the pipeline itself the portfolio differentiator. `sw-ai-pm-portfolio`'s walkthrough
is a hard dependency on a `museum/` output that did not exist — no `museum/` dir, a
two-line `museum:` manifest stub with nothing behind it — while `runs/` held ~25
directories of real, dated production evidence sitting ungenerated. This session
built the capture layer that turns that evidence into a self-contained, browsable,
dated museum, and converts the heavy Cy investment from sunk cost into displayable
proof.

Two locked scope decisions held throughout: **backfill everything** (a read-only
retroactive scraper over the real on-disk artifacts, noise-filtered) and **standalone
first** (a self-contained static site inside `anima/`; the Astro export into the
portfolio is an explicit follow-on, not coupled here).

## The build (commit-split along real seams)

The architecture collapses three distinct mechanisms into one word, "capture." We
named them separately and committed along the seams, vertical-slice first:

| Seam | What | File |
|------|------|------|
| **A** Exhibit schema | the durable data model everything reads/writes | `pipeline/museum/schema.py` |
| **C** Scraper | read-only walk of `runs/` → exhibits | `pipeline/museum/scraper.py`, `motion.py` |
| **D** Mo | Sonnet docent that narrates a structured exhibit | `pipeline/agents/museum_writer.py` |
| **E** Comparison artifact | hand-drawn sheet ↔ colored loop GIF | `pipeline/museum/motion_gif.py` |
| **F** Renderer | self-contained static site | `pipeline/museum/render.py` |

The live DAG `post_run` capture hook (seam B) is **not** built this session — the
backfill (C) is the deadline-critical piece, and the scraper covers the existing
evidence. B remains a clean follow-on (subscribe to the real hook like
`patch_stager`, never a parallel observer).

## The backfill (counts)

**97 exhibits**, 15 runs kept, 13 filtered + 2 empty-skipped.

- **character-bible = 84** — Cy plate verdicts across 8 bakes (the pixel-art
  production run, the rebakes, the pencil-register pencil-bake, the expression
  expansion), bible mutations/adds (the no-hair invariant, the motion ingests), and
  the **6 motion comparison exhibits**.
- **pencil-test = 13** — 10 Seedance shots (prompt + seed + tier + timing as the
  artifact; the video is not copied) + Act 1 / head-turn approved-keyframe rollups.

**Filtered, every skip logged** (no silent truncation): 5 `*.log` files, the
torch/torchvision install runs, and 6 *aborted* runs (the honest definition: no
`approved/`, no `plate_verdicts.jsonl`, no `bible_audit.jsonl`, no `seedance/` — no
decision evidence on disk). Two kept runs scraped 0 exhibits (empty verdict log /
no Seedance meta) and were skipped from the tree.

## The pivot (Sean's review, mid-build)

The first vertical slice scraped the NB2 turnaround/expression plates and rendered
them standalone. Sean's read was exactly right: **plate-vs-anchor is the boring "AI
matched the reference" comparison** — the anchor and the plate look identical
("same image twice"), so the exhibit shows nothing about the division of labor. The
NB2 plates are an identity-hold story, not a human/agent story.

So the showcase pivoted to the **motion plates**, where the real division of labor
is legible: Sean draws a B&W motion key sheet *by hand* (the manual shape-block, the
Phase 4 animatic), and the pipeline ingests it into colored animatic frames. One
exhibit per motion pairs the hand-drawn sheet (left) with the colored frames
assembled into a **playing loop** (right) — composited onto cream paper, ping-pong
for settle motions, **forward for the hop** (locomotion reads wrong as a rewind,
per Sean's second note). The NB2 batch is kept (Sean will draw sketches for it later
so it gets the same treatment); the redundant anchor was dropped from plate pages.

This is the engine-truth test applied to the museum itself: if the loop plays and
the character is recognizably itself, it ships.

## Mo's verdict — docent, not drifting

Mo (Sonnet 4.6) narrates a structured exhibit into studio-manual prose. On the real
path she is **genuinely good** — given the no-hair plate's verdict, she wrote a
four-paragraph explanation of the failure modes (9,957 colors where four were
required, the 0.2673 PIL score, the hourglass-vs-lozenge silhouette), attributed it
to Cy correctly, and connected it to the pixel→pencil pivot — using *only* facts the
exhibit carried. No fabrication. That is the docent we wanted.

Two honesty mechanisms make her trustworthy:
1. **Structural honesty in the schema** — `decision.rationale` stays empty +
   `rationale_source` null when the logs are silent; `evidence_completeness` is a
   sortable thin/partial/rich signal. A thin exhibit is narrated as honestly sparse.
2. **A faithful deterministic fallback** — built only from the exhibit's own fields
   (no invented score, date, or cause). It runs credential-free (CI-green) and is
   what the **committed** museum carries.

**Cost call:** real Sonnet narration of all 97 exhibits is ~2–3 min/call (≈45 min,
heavy subscription) — too much to incur unprompted. The committed museum ships with
the deterministic fallback; real Sonnet docent prose is a one-command upgrade
(`build_museum.py --narrate`, drop `--no-sonnet`). The capability is built, tested,
and proven; running it at scale is Sean's call.

## Weight discipline

First full backfill was **589 MB** (full-res plate copies + per-exhibit anchor
duplication + `_site` doubling). Fixed: thumbnail + palette-quantize every committed
image to ≤480px PNG, drop the redundant per-plate anchor, downscale the loop GIFs,
and gitignore the regenerable `_site/`. Committed museum: **~9.5 MB**. The full-res
originals live in gitignored `runs/` and the locked character dirs.

## What's true now

- `museum/` is a committed convention; `museum/_site/` is the gitignored render.
- The `museum:` manifest block grew additively — the pencil-test reference blocks
  are untouched, so Act 2 Seedance work runs unchanged.
- Mo joins the persona roster as shipped (Maya, Cy, Em, **Mo**).
- 230 tests green (+23), each mechanism test-first and its own commit.

## Named follow-ons (declared seams, NOT built)

1. **Astro export into `sw-ai-pm-portfolio`** — the standalone-first deferral. Maps
   the exhibit schema → the portfolio's MDX frontmatter. The schema field names were
   chosen to make that easy without coupling now.
2. **T3 pre-publish critic gate** (Codie + Annie + Sage → Opus chairman) — the
   publish step has an obvious slot; a human takes the look for now.
3. **Live DAG capture hook (seam B)** — for future runs; subscribe to the real
   `post_run` hook like `patch_stager`.
4. **NB2-plate comparison sketches** — Sean draws shape-block sketches for the
   turnaround/expression batch so those exhibits get the same sketch↔output treatment.
