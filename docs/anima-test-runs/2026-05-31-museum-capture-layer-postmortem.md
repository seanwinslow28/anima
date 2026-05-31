# The Museum capture layer — what broke, what we learned

*2026-05-31. The session that built anima's Museum end-to-end on `feature/museum-capture-layer` — the orthogonal capture layer that turns `runs/` evidence into a self-contained, dated, browsable static site inside the repo. 18 commits, 207 → 231 tests, two human review gates that each caught a real mistake. Unlike the Cy-bibles session, nothing here was a live-model debugging saga: the scraper is offline and deterministic. Every failure this session was a **judgment** failure — wrong showcase, wrong weight, incomplete exhibit — and every one surfaced only when a human or a real rendered artifact looked at the output. This is the field report.*

---

## What the session was supposed to be

The kickoff (`docs/2026-05-31-museum-capture-layer-kickoff.md`) was explicit on shape and discipline: plan-mode first, then a **vertical slice before breadth** — build the durable exhibit schema, point a minimal scraper at the single richest run, render it standalone, open it in a browser, and **STOP** for Sean's approval of the shape before building the full scraper, Mo, or the comparison GIFs. The architecture collapses three distinct mechanisms into one word, "capture"; the plan split them along their real seams (A schema, C scraper, D Mo the writer, E comparison artifact, F renderer, B live hook) and committed along those seams.

Two locked scope decisions governed: **backfill everything** (read-only retroactive scraper over real on-disk artifacts, noise-filtered) and **standalone first** (self-contained site inside `anima/`; the Astro export into `sw-ai-pm-portfolio` is a named follow-on, not coupled here).

What was supposed to happen: schema → one real exhibit rendered → Sean approves the shape → fan out to breadth → Mo → finished renderer → wrap. What actually happened followed that arc almost exactly — but the slice STOP and a later review each caught a mistake that would have been expensive to discover after breadth, and the offline build surfaced two resource failures (a 60× weight blowup, a bare-page completeness gap) that no test would have flagged because no test asserts "does this read like the real story to a human."

---

## Failure 1 — the vertical slice showcased the wrong thing (the "same image twice" pivot)

The first slice did exactly what the plan said: minimal scraper against the richest run (`2026-05-30-cy-claude-mascot-pencil-bake`, 7 plate verdicts + the no-hair mutation), rendered standalone, opened in a browser. It was technically correct — real DINOv2 scores, real Gemini verdicts, real cited `IR.*` rules, honest thin/rich framing. Every test green.

Sean's read at the STOP gate was the failure the tests couldn't see: **"they're all through Nano Banana 2… the curious page has the same image twice."** The plate exhibits paired the generated plate against the `anchor.png` it was scored against — but plate-vs-anchor is the *boring* comparison. The whole point of an NB2 plate is that the output matches the reference, so the two images look identical. The exhibit showed identity-hold (an internal QA fact) where the portfolio needed to show the **division of labor** (the human/agent story). The comparison was a tautology dressed as an artifact.

The resolution was a pivot, not a patch: the **motion plates** carry the real story. Sean draws a B&W motion key sheet *by hand* (the manual shape-block, the Phase 4 animatic); the pipeline ingests it into colored animatic frames. One exhibit per motion now pairs the hand-drawn sheet (left) against the colored frames assembled into a playing loop (right). The redundant anchor was dropped from plate pages entirely (which also killed 76 duplicate anchor copies — see Failure 2). The NB2 batch was kept, not deleted, because Sean will draw shape-block sketches for it later so it gets the same treatment.

**The deepest lesson**: the vertical-slice STOP gate did exactly its job. The plan's insistence on rendering one real exhibit in its target medium *before* building breadth is what made this a 30-minute course-correction instead of a 6-phase rebuild. A schema that's "technically faithful" can still showcase the wrong fact; only a human looking at the rendered medium catches that, and the cheapest place to put that human is in front of the slice. This is the museum's own engine-truth test — *does a stranger see what the human did and what the agents did?* — and the slice failed it productively.

---

## Failure 2 — the first full backfill was 589 MB (a 60× weight blowup)

With the pivot in and breadth built, the first `--all` backfill produced a **589 MB** museum. The committed-artifact target was single-digit MB.

Three compounding causes, each invisible until measured:
1. **Full-resolution plate copies.** `_copy_assets` used `shutil.copy2` — the NB2 plate PNGs are 1–2 MB each, and there are ~76 plate exhibits.
2. **Per-exhibit anchor duplication.** Every plate exhibit copied its own `anchor.png` — 76 copies of the same image (this one resolved itself when Failure 1 dropped the anchor from plate pages).
3. **`_site` doubling.** The renderer copies assets into the static build, so every byte counted twice (295 MB of the 589 MB was `_site`).

The resolution layered three fixes: thumbnail + palette-quantize every committed raster to ≤480 px (the flat pencil-test palette quantizes near-losslessly), downscale the loop GIFs (`max_w` on the assembler), and gitignore the regenerable `_site/` so only the source exhibit tree is committed. Result: **~9.5 MB**. The full-res originals stay where they already live — gitignored `runs/` and the locked character dirs.

**The deepest lesson**: a static-site generator that copies assets has a silent multiplier (source × `_site`), and "copy the evidence out" is the obvious-but-wrong default when the evidence is full-res production imagery. The museum is a *display* artifact; its assets should be thumbnails from the first commit, with the originals addressed by provenance, not duplicated. No test catches repo weight — `du -sh` is the only gate, and it has to be run deliberately.

---

## Failure 3 — the Seedance pages were bare (an incomplete exhibit shipped a STOP)

The finished museum was committed and re-opened for Sean. He went to the Pencil-Test Seedance pages and found the failure: **"I don't see anything within any of the Seedance pages. Are they supposed to have the videos playing?"**

They were bare by a chain of half-decisions. I'd chosen not to copy the Seedance mp4s into the museum (≈31 MB at 720p — reasonable size caution), recording only `prompt` + provenance in the exhibit. But then the renderer never surfaced the `prompt` either (it lived in the JSON, unrendered), and Mo's fallback prose said the exhibit was *"intentionally sparse"* — which was actively false for a shot that carries a full v4-template prompt and a seed. So the page showed a title, two pills, a misleading "sparse" sentence, and a provenance line. The richest single thing about a Seedance shot — the prompt engineering and the motion it produced — was the one thing not on the page.

The resolution did the work the size-caution had skipped rather than reaching for it as an excuse: transcode each mp4 to a light web loop via ffmpeg (480 px, muted, no audio, faststart) — **31 MB → 0.8 MB total** — embedded as an autoplay-loop `<video>`; surface the prompt in a styled block; show the params (tier/resolution/duration/seed/wall-clock) inline via a new `Exhibit.meta` field; and reframe Mo's fallback so a generated-from-prompt shot reads honestly (*"generated from the prompt below; no critique verdict was logged"*) instead of "sparse." Committed weight went 9.7 → 10.5 MB.

**The deepest lesson**: "the video is heavy, so skip it" silently became "so skip the whole exhibit." A size constraint is a transcode problem, not a delete-the-content problem — the same lesson as Failure 2 from the other direction. And the honesty contract has a failure mode I'd underweighted: *thin* is only honest when the evidence is actually thin. A `seedance_shot` was marked `partial` but rendered as `sparse`, which made an exhibit that had rich evidence (prompt + params) *look* empty. Honest framing has to match what's actually on disk, not what the renderer happened to surface.

---

## Failure 4 — Mo's real narration hit a cost/latency wall

Mo (the Sonnet 4.6 docent) was built test-first with a faithful deterministic fallback for CI. When I ran the real `--narrate` pass over the 97-exhibit backfill, the SDK path was live (claude-agent-sdk, subscription auth) and the prose was genuinely excellent — given the no-hair plate's verdict, Mo wrote four faithful paragraphs (9,957 colors where four were required, the 0.2673 score, the hourglass-vs-lozenge silhouette), attributed to Cy, no fabrication. But each call ran ~2–3 minutes; serial it was ~2 hours, and even parallelized (bounded `narrate_many`) it was ~45 minutes of heavy subscription spend.

The resolution was a judgment call about *whose* spend this is: stop the run, ship the committed museum with Mo's deterministic fallback (instant, zero-cost, faithful), and make real-Sonnet narration a documented one-command upgrade (`build_museum.py --narrate`, drop `--no-sonnet`). Added a `--no-sonnet` force-fallback flag so the committed artifact is deterministic regardless of whether creds are present. The capability is built, tested, and proven on real samples; running it at scale is Sean's call, not a default the build makes for him.

**The deepest lesson**: a per-item LLM pass over a backfill is an O(N) spend the build shouldn't silently incur on the user's account. Mo needed two paths from the start — a deterministic one for the committed default and an opt-in one for the polished pass — and the fallback has to be *faithful*, not a placeholder, so the default museum is honest on its own. The parallelization also revealed that real value isn't latency-bound here; it's cost-bound, and the right lever was the opt-in flag, not more concurrency.

---

## Failure 5 — the scraper silently dropped a colored key (idle-04)

A quiet one, caught while reading the pre-existing CLAUDE.md diff during wrap. The motion scraper read only `motion-additions.json` (the original line-rough ingest, idle = 3 frames). But Sean's colored pass had added a 4th idle key (`idle-04`, the risen breath peak) via a *separate* spec, `motion-idle04-addition.json`. The museum's idle loop was missing a frame and nobody would have known from the rendered page — it just looked like a complete 3-frame loop.

The resolution: `scrape_motion_plates` now globs **every** `motion-*.json` spec, merges plates per motion, and sorts frames so a later-added key lands in numeric order. Idle now carries all 4 colored frames.

**The deepest lesson**: a scraper that reads "the spec file" instead of "all the spec files" silently truncates whenever the source grows a second file. The honest-thin contract protects against *invented* content but not against *missing* content — a complete-looking exhibit built from partial evidence is its own quiet lie. Where a source can be multi-file, the scraper has to enumerate, not name.

---

## The minor stuff (logged, not dwelt on)

- **Stale `git index.lock`** from a crashed prior process blocked the first commit; removed after confirming no git process was running. (The inherited handoff had warned the tool display could lag and leave detritus — it did.)
- **Empty kept runs** (`cy-claude-mascot-rebake`, `act2-exploration`) passed the noise filter on a marker dir but scraped 0 exhibits; added a skip so they don't leave stray 0-exhibit `run.json` files in the tree.
- **A misleading log line** ("all stub (no SDK)") printed even when the SDK *was* available and we'd forced the fallback; fixed to distinguish `--no-sonnet` from genuine SDK-absence.

---

## What we learned

The structural takeaways that should outlive this session.

**Every failure this session was a judgment failure, and the rendered medium is the only test that catches them.** The Cy-bibles session learned "live runs catch the bugs CI can't." This session's mirror: *the rendered artifact in its target medium catches the judgment bugs CI can't.* The wrong-showcase (Failure 1) and the bare-page (Failure 3) both passed every unit test and both were caught by a human opening a browser. Tests assert structure; they cannot assert "does a stranger see the right story." The two human STOP gates were not ceremony — they were the only instrument that could have caught these, and they caught one each.

**The vertical slice is the cheapest place to be wrong about the schema's *intent*.** The slice was technically faithful and still showcased the wrong fact. Building breadth first would have made the same mistake 84 times before anyone saw it. The plan's "render one real exhibit before building breadth, then STOP" turned a schema-level mistake into a 30-minute pivot. This is the single most load-bearing process decision of the session.

**A size constraint is a transcode/thumbnail problem, never a delete-the-content problem.** Failures 2 and 3 are the same lesson from opposite sides: copying full-res evidence blew up to 589 MB; *not* copying heavy evidence emptied the Seedance pages. Both resolved the same way — downscale on copy (thumbnails, ≤480 px GIFs, 480 px muted mp4s) so the content is present *and* light. The museum is a display artifact; its assets are derivatives, and the originals live by reference in gitignored `runs/`. "Heavy" should trigger a transcode, not a skip.

**The honesty contract protects against invented content but not against missing or mis-framed content.** `evidence_completeness` + empty-rationale stops fabrication (Failure-free — Mo never invented). But a *complete-looking* exhibit built from a partial spec (Failure 5) and a *rich* exhibit rendered as "sparse" (Failure 3) are both quiet lies the contract didn't catch. Honesty has three failure modes, not one: invented, missing, and mis-framed. The schema guards the first; the scraper has to guard the second (enumerate all sources); the renderer + Mo have to guard the third (framing must match what's actually on disk).

**Per-item LLM passes are an O(N) spend the build must make opt-in.** Mo's real narration is excellent and the right artifact for a portfolio-final pass — but at ~45 minutes / heavy subscription for 97 exhibits, the build shipping it by default would spend the user's account without being asked. The deterministic-faithful default + the `--narrate` upgrade is the correct shape: the committed museum is honest and free; the polish is a deliberate, costed choice. This generalizes to any future fleet member that runs a model per artifact across a backfill.

**Offline, deterministic, test-first is a fundamentally calmer build than live-model orchestration — and that's a feature.** Where the Cy-bibles session burned $5–10 and two hours on five stubbed live attempts, this session's entire mechanism layer was built credential-free, green at every commit, with zero spend until the optional Mo pass. The lesson isn't "offline is better"; it's that pushing the model dependency to a single opt-in seam (Mo) kept 17 of 18 commits deterministic and reviewable. The expensive, flaky surface should be one named, optional node — not woven through the pipeline.

---

## What landed on disk

| Commit(s) | What | Seam |
|-----------|------|------|
| `38342fd` `b77d691` | Exhibit schema (`Exhibit`/`Decision`/`Verdict`) + `museum/` tree + schema doc + additive `museum:` manifest block | A |
| `2876464` `25fb682` `049d072` | Vertical slice — minimal scraper + throwaway renderer + orchestrator, one real run rendered standalone → **STOP** | C+F slice |
| `69ccbb3` `5d697e6` `7439c5d` `75553f0` `944bc8b` `548f418` | The pivot: `motion_keys` schema + Pillow loop assembler + `scrape_motion_plates` + comparison renderer + `--motion` batch + hop forward-loop fix | E |
| `29b8282` | Full-breadth backfill — `walk_runs` noise filter + seedance/keyframe readers + thumbnailing (589M→~10M) | C |
| `a4885b3` `3e23c82` `047385d` | Mo the museum writer + finished project→run→exhibit renderer + faithful-fallback narration | D+F |
| `ccc3356` | Aggregate all `motion-*.json` specs (idle-04 was dropped) | C fix |
| `da2ca5c` | Wrap — CHANGELOG + CLAUDE.md + field report | docs |
| `5d60914` | Seedance pages play the clip + show prompt/params (transcode 31M→0.8M, `Exhibit.meta`) | E fix |

Test suite at end of session: **231 passed** (from a 207 baseline; +24 across schema/scraper/motion/motion_gif/writer/render), zero regressions, each mechanism test-first and its own commit. Committed museum: **~10.5 MB** (97 exhibits — character-bible 84, pencil-test 13 — thumbnailed + 6 motion loops + 10 transcoded Seedance clips); `museum/_site/` gitignored. Live spend: **$0** for the committed artifact (the optional real-Sonnet narration pass was started and stopped, ~8 exhibits' worth).

The Museum exists. The receipts are visible. The pipeline-as-portfolio thesis has its load-bearing artifact, dated and standalone, well ahead of the portfolio sprint.

---

## How we should proceed

In priority order, with the reasoning each carries:

1. **Run the real-Sonnet narration pass when the portfolio prose matters** (`build_museum.py --narrate`, drop `--no-sonnet`). The fallback is honest and ships today; Mo's real docent prose is the portfolio-final polish. It's ~45 minutes and subscription-absorbed — a deliberate one-time cost when Sean wants the museum to *read* like a studio, not just *be* correct. Consider letting it run unattended (it's idempotent; re-running overwrites `exhibit.md`).

2. **Draw the NB2-plate shape-block sketches** so the turnaround/expression batch gets the same hand-drawn ↔ output comparison the motion plates have. This is the move that makes the *whole* character-bible story show the division of labor, not just the motion exhibits. It's Sean's hand-work, asset-gated; the renderer already supports the comparison layout, so ingestion is mechanical once the sketches exist.

3. **Build the live DAG capture hook (seam B)** — the one named mechanism this session deferred. Subscribe to the real `post_run` hook exactly like `patch_stager` (one observer, many subscribers; never a parallel one), synthesize an exhibit from each `AgentResult` as future runs execute. This closes the loop so the museum captures *forward*, not just backfills. Low-risk, additive, behind the schema that's now proven.

4. **The Astro export into `sw-ai-pm-portfolio`** — the standalone-first deferral, now unblocked. The Phase-0 field names were chosen to map cleanly onto the portfolio's MDX frontmatter; this session deliberately did not read the portfolio's locked schema. Its own session: read that schema, write the exhibit → MDX mapping, wire the publish.

5. **The T3 pre-publish critic gate** (Codie + Annie + Sage → Opus chairman) — commit 9, unbuilt. The publish step has an obvious slot and a human takes the look for now. Sequence it *after* the museum has content (its whole job is to read museum content under independent eyes), which it now does.

The throughline for all five: the schema is the load-bearing thing and it held. Everything ahead — real narration, the NB2 sketches, the live hook, the export, the T3 gate — fans out from the exhibit model this session proved against real, dated evidence. Build on it; don't re-litigate it.
