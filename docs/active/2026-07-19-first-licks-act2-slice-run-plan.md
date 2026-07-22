# FIRST LICKS — the Act-2-turn-slice costed run: build-brainstorm

*2026-07-19. This is the build-brainstorm the ROADMAP anti-drift contract
requires before the first costed run. It is a **plan, not a green-light** —
the run fires only in a future session where Sean explicitly opens a budget.
Everything decided here was grilled one fork at a time with a recommendation
attached; Sean made every call.*

**The piece:** FIRST LICKS (`briefs/2026-07-02-grandmaster/`). **The slice:**
Act-2 turn, ~10–14 shots, party-exit → reflex → room → box → photo/inscription
→ tape → glitch → headband → ignition, ending on the first training frame
(locked in concept.md §Production principles). **Register:**
`primal-sketch-grit` (piece-locked 2026-07-15). The run doubles as the v1b
screening-room stress test.

## Decisions recorded this session (Sean's calls, 2026-07-19)

- **D1 — Cy pass scope: kid + grandma only.** The slice's on-screen cast. The
  kid carries every frame; grandma appears inside the artifacts (the photo,
  the home-movie tape, the young-warrior glitch footage — she is on screen in
  the match cut, so her young/old identity needs IR rules protecting it).
  Host-dad / birthday-girl / party-mom Bibles ride Runs 3/4 when their acts
  fund them. This pass is where Artie Checkpoint-3 item (3) closes and where
  the go-no-go across-edit T2 gate **formally** closes (go-no-go.md: "closes
  only at the costed Cy Bible pass").
- **D2 — slice scoping: full story in the brief, slice-sized `beats.json`.**
  The run's studio brief carries the whole film (Sam writes the turn knowing
  Acts 1/3) plus an explicit scope directive: this run's `beats.json` covers
  ONLY the Act-2 turn. Rationale: Bea's `storyboard_validate` requires every
  beat boarded and GENERATE has no board-subset mechanism, so a full-film beat
  sheet + slice board fails validation by construction; the machine contract
  must be slice-sized while the prose context stays whole-film. Verified in
  the $0 stub smoke before any burn.
- **D3 — ANIMATIC ON.** Sean draws ~10–14 placement silhouettes + `holds.json`
  for the turn. The Spark run proved this is the zero-retry lever; the turn is
  the film's hinge and a strict no-joke zone where staging is the
  storytelling; and `holds.json` is where the F1 two-band hold spec (2–4s
  in-action / 6–10s hero holds) actually gets encoded for ASSEMBLE.

Also this session (the rest of the pre-pipeline checklist): the five
`characters/{id}/source-refs/` folders were seeded provisionally from the
Art-Dept bundle refs (STEP 0 — definitive ChatGPT keeper batch still Sean's
homework); the boombox-song prompt doc was drafted
([`boombox-song-prompts.md`](../../briefs/2026-07-02-grandmaster/boombox-song-prompts.md),
one-master-+-derive model); and verification **gate 2 (why-did-he-train) RAN
and PASSED 5–0**
([`verification-gates-log.md`](../../briefs/2026-07-02-grandmaster/verification-gates-log.md)).

## Two required $0 build slices (found by this brainstorm; TDD, stub-green)

The go-no-go NO-GO'd NB2 for primal-sketch-grit — and the Phase-5 pipeline
would run it on NB2 today:

- **Slice A — per-register Phase-5 transport routing.**
  [`frame_router.py`](../../pipeline/agents/frame_router.py) says it itself:
  *"today all registers share a route"* — `style_register` is threaded for
  provenance only, so `standard_keyframe` dispatches NB2 regardless of
  register, and the route table's `gpt_image_2` entry is `deferred`
  (`RouteNotWiredError`). The slice: route resolution consults
  `get_register(style_register).generation_model` (the same registry read
  Cy's `_resolve_plate_model` does) and dispatches `gpt-image-2` through the
  live-verified Higgsfield transport
  ([`higgsfield_runner.py`](../../pipeline/agents/higgsfield_runner.py),
  Task 7 production path). Guards: pencil-test runs byte-identical (the
  characterization tests), fail-loud on unwired combinations, Maya's cost
  preview reads the real per-frame price.
- **Slice B — Bea's register clause parameterized.** Her context file and
  [`storyboard_artist.py`](../../pipeline/agents/storyboard_artist.py) (~L55)
  hardcode the pencil-test clause block that every per-shot prompt must end
  in. For a primal run the prompts must close in the primal clause instead —
  pulled from [`pipeline/registers.py`](../../pipeline/registers.py) per the
  style-neutrality doctrine (this hardcoding is the exact drift it exists to
  prevent). Guard: the shipped Spark board and the pencil-test stub outputs
  stay byte-identical when the register is pencil-test-colored.
- **Verify-only (no slice unless it fails):** the animatic role-tag clause in
  [`generate_stage.py`](../../pipeline/orchestration/generate_stage.py) reads
  register-neutral — confirm in the stub smoke that nothing in it pulls
  toward pencil.

## The dependency ladder to green-light (in order)

1. **Sean:** run the definitive ChatGPT keeper batch
   (`bundle/chatgpt-orchestration.md`); keeper anchors **replace** the
   provisional seeds in `characters/{kid,grandma}/source-refs/` (the other
   three can wait). Cy authors from definitive art, not in-room ratifications.
2. **Sean:** generate + pick the boombox master
   (`boombox-song-prompts.md`); derive the two states ($0 ffmpeg). Blocks
   Bea's hold locks and the stopwatch table-read (gate 1).
3. **Build:** Slices A + B above ($0, TDD, own PR; both md5 guards + register
   characterization tests green).
4. **Costed Cy pass — kid + grandma** (own session, fleet-ops discipline,
   Sean opens its budget separately). Closes Checkpoint-3 item (3) + the
   across-edit T2 gate. Details:
   - Copy keeper anchors into `source-refs/`, then
     `python scripts/author_bible.py characters/kid/ …` (studio brief text
     from the bundle's `design-bible.md`), same for `grandma/`.
   - Register both in manifest `characters:` + `criteria_sources:` after
     approval (closing `cy_readiness_report.md` gap 2 for the slice cast).
   - **SF03:** declare the kid's heads-tall spec (a kid build — decide the
     target with Sean at authoring) or `sf03: opt_out` deliberately; the kid
     IS "the next heads-tall character authoring," so the parked sean-anchor
     re-bake rider MAY ride this session's Approach-A feeder if Sean wants it
     (his 2026-06-08 call; optional, not a blocker).
5. **Brief edit:** append the Run-1 scope directive section to
   `00_studio_brief.md` (D2's slice-`beats.json` instruction; a deliberate,
   CHANGELOG'd brief edit — the orchestrator snapshots the brief per run).
6. **$0 stub smoke:** `python -m pipeline.run --brief briefs/2026-07-02-grandmaster
   --slug first-licks --animatic --stub` through every gate to DONE. Proves:
   authoring-mode detection, the scope directive produces slice-sized beats,
   `--frames` mechanics (pick N at run start once Sam's slice beat count is
   known — or omit and accept Bea's natural count; the storyboard gate
   enforces exactness only when set), the animatic pause, and Slice-A routing
   dispatching the gpt-image stub.
7. **Green-light session:** Sean opens the run budget (Higgsfield credits,
   never `ANTHROPIC_API_KEY`), Maya's plan + cost preview at the plan gate,
   fire. Screening room drives it (below).

## Run mechanics (the shape of the burn)

Authoring-mode orchestrator run, plain terminal for the costed leg
(nested-SDK throttle), Flow v1b screening room as the director's seat:

```
python -m pipeline.run --brief briefs/2026-07-02-grandmaster --slug first-licks \
    --animatic [--frames N] [--run-dir runs/<date>-first-licks-act2-slice]
  → plan gate (Maya + cost preview; SEAN APPROVES SPEND HERE)
  → --approve-plan → Sam (full-story context, slice beats) → script gate
  → --approve-script → Bea (primal clause block, --frames if set) → curation gate
  → --approve-storyboard → ANIMATIC pause: Sean drops F<NN>.png silhouettes
    + holds.json (the F1 two-band values) into runs/<id>/animatic/
  → --approve-animatic → per-frame Flo(→Higgsfield gpt-image-2) → T1 → Em(kid,
    grandma) → eye gate per frame → ASSEMBLE (holds from the animatic sidecar)
```

Em runs as the gross-defect assistant she's calibrated to be (flag → re-roll;
Sean owns the fine call). Retry ladder per manifest; museum capture stays the
separate post-run pass (unchanged this run).

**Cost sketch (order-of-magnitude only — Maya's estimator is the real
preview):** ~10–14 frames × ~4 cr (gpt-image-2 via Higgsfield, the Art-Dept
per-render observed price) ≈ 40–60 cr + retries; the Cy pass is separately
budgeted (plate plans for two characters; the Art-Dept session's 28 cr for 7
renders is the reference point, a Bible pass is bigger). Both legs hard-stop
at their declared ceilings.

## Screening-room stress test + friction logging

The run is driven through the Flow v1b room (Sean = director, Claude = ops
copilot). Every friction — a gate the room can't express, a file the room
can't show (known G1–G10 narrowings: no animatic-upload write path, no
cost-spent accumulator…), a decision that forced a terminal detour — gets a
row in the **v1c triggers ledger**
([`2026-07-04-flow-interface-build-tracker.md`](2026-07-04-flow-interface-build-tracker.md)
§ledger) *as it bites, not from memory afterward*. That ledger is v1c's
prioritization input; this run is its first real data.

## Explicitly out of scope (named so they don't drift in)

Runs 2–4 (montage / Act 1 / Act 3) and the master assemble; the audio post
pass (human-owned, on the assembled cut); museum orchestrator wiring; any Em
re-calibration; the `post_animatic` T3 gate (its promotion trigger is
unchanged). The remaining verification gates run at their staged artifacts
(gate 1 at the beat sheet + picked master; gates 3–6 at boards/animatic).
