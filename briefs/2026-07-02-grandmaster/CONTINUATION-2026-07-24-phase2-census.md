# FIRST LICKS — Continuation (Phase 1 closed → Phase 2 asset census)

*Fresh-session handoff, 2026-07-24. Paste the body below into a fresh Claude Code
session. Propose-only — Sean owns taste and every lock.*

---

You're continuing an active thread on **FIRST LICKS** (the piñata / samurai-homage short
at `briefs/2026-07-02-grandmaster/`). The project just hit its biggest milestone:
**Phase 1 (story) is CLOSED** — the whole short is ratified beat-by-beat, formalized,
and tracked. Your job this session: **Phase 2 — the asset census**, then (checkpointed)
Phase-3 pack drafting. Everything is propose-only; Sean decides every lock.

## FIRST — invoke the standing lenses, in this order (how this thread runs)

1. **`/creative-director`** — the planning/critique rubric, turned on production planning.
2. **`/prompt-how-much`** — when you start writing any generation prompts (Phase-3 packs).

## WHERE WE ARE (the 4-phase plan of record, Sean-ratified 2026-07-23)

- **Phase 0 DONE:** per-project docs convention — the project `CLAUDE.md` (auto-loads,
  law digest) + `STORYBOARD.md` (per-beat tracker) + templates in `docs/templates/`.
- **Phase 1 CLOSED (2026-07-24):** the full-story writers' room ran; Sean marked up the
  beat sheet beat-by-beat and every item was workshopped live. **DR #33 a–p** (concept.md)
  records every ruling; **DR #34** blessed runtime **~4:00–4:20** (montage trims first,
  the turn NEVER trims, final squeeze at assembly to the song). Formalized:
  `beat-sheet-v2.md` (48 beats, ZERO open picks) → `beats.json` (12 story beats,
  **validated against the real `pipeline/orchestration/beats.py` `load_beats`**;
  namespaces `kid/grandma/brittany/dad/mom/neighbor` register later at the Cy step) +
  `script-v1.md` (screenplay pass — 5 spoken lines in the whole film, the kid silent).
- **Phase 2 = THIS SESSION:** the asset census (below).
- **Phase 3:** generation waves (ChatGPT Desktop packs) + Sean's approval sweep.
- **Phase 4:** pipeline run + the v1b screening-room UI test.

## READ FIRST (in order — the project CLAUDE.md auto-loads in this tree; trust it)

1. `briefs/2026-07-02-grandmaster/CLAUDE.md` — the law digest (register, anti-drift,
   NJ setting, time-of-day, wardrobe, Seedance 2D anchor, Act-3 weapons, spend rules)
2. `briefs/2026-07-02-grandmaster/STORYBOARD.md` — **the live per-beat act tables:
   the census's primary input** (per-beat asset status + the needs-gen queue + standing gaps)
3. `briefs/2026-07-02-grandmaster/beat-sheet-v2.md` — the 48-beat spine of record
4. `briefs/2026-07-02-grandmaster/concept.md` — §Decision Record **#31–34** especially
   (#33 a–p = the story pass; #33p = D1 fixed-frame tree; #34 = runtime)
5. `briefs/2026-07-02-grandmaster/script-v1.md` + `beats.json` — the formalized story
6. `runs/2026-07-19-first-licks-artdept/montage-prompt-pack-v2.md` — **the proven pack
   format** (PATH KEYs, [STYLE] clause, checkpointed batches, M0 wardrobe pattern,
   KEEPER anchor) — new packs copy this format
7. `.claude/skills/art-department/references/prompt-technique-kit.md` — fresh-vs-edit
   economy, dependency map, never-chain-styles, §(g) cross-style comp/light refs
8. `runs/2026-07-19-first-licks-artdept/bundle/environment-style.md` — palette/setting
   law + the party-yard placement map
9. `registers/primal-sketch-grit/research.md` — the register truth (heavy bold ink)

## THE PHASE-2 TASK — the asset census

Walk the 48 beats (STORYBOARD tables) against everything banked and produce **the
complete generation manifest**, organized into checkpointed ChatGPT pack waves.
Deliverable: a census doc (e.g. `runs/2026-07-19-first-licks-artdept/full-film-census.md`
or a new run dir — propose) + updated STORYBOARD rows. Cover, per beat:

- **Locations + DR #20 angle sets.** Known: party-yard ⑬ angles banked BUT
  `world[].refs` under-recorded (fix); **grandma-room is single-angle — needs its full
  DR #20 set** (master + reverse + per-mark angles + placement map) before Act-2 boards;
  NJ street-pan plate(s) new; the final-image road+dark-yard set new.
- **Characters × context × outfit (DR #32 wardrobe pass).** Banked: kid wimpy/MID/FALL/
  WINTER/TRAINED turnarounds, grandma-young, Y1+Y2 host family, neighbor states,
  boombox states, target rig. New/needed: the **young kid inside the home-movie tape**
  (with young grandma — never designed), Act-1 kid at party 1 (wimpy, banked), any
  Y2 escalation gaps.
- **Props/plates (the DR #33 queue, already listed in STORYBOARD standing gaps):**
  the **tournament-victory photo REGEN** (beat-up, hand raised, ref/opponent scale —
  the flying-kick photo is RETIRED, DR #33j) · the box + star-tray prop · the red
  streamer element · the invitation + mocking-doodle prop · the **D1 replica framing's
  3 missing seasonal states** (end-summer/fall/winter; spring exists) · the petal-pin
  still (#32) · (optional, mockup-gated) the cassette credits stinger.
- **VHS treatment spec** (WR §2.3) — design-once, reused cold-open + Act-2 (post
  treatment, but the 4:3 framing affects boards).
- **What's already banked and must NOT be regenerated** — the montage stills (M0–M6,
  M-VAR), the geyser pair (✓S + motion "perfect"), anchors/turnarounds. List them as
  protected.

Then propose the **pack-wave order** (locations/angles → props → character contexts →
composites; montage-pack format, checkpointed) for Sean's sign-off BEFORE drafting
prompts. Draft packs only after he blesses the census.

## STANDING RULES (non-negotiable, from the record)

- **$0 unless Sean opens a budget.** ChatGPT gen = Sean's own pass; Higgsfield credits
  only with a declared ceiling; never `ANTHROPIC_API_KEY`. Announce any spend.
- **NO CHAIN-EDITING (DR #31):** fresh, or ONE edit off a clean source; KEEPER
  art-style-only anchor on fresh environment plates; discard drifted plates.
- **Positive-led anti-drift clause** — never enumerate loaded mediums as negatives.
- **Seedance 2.0:** lead EVERY prompt with the flat-2D-cel **"animated on twos"**
  anchor (no negation); generate longer than the hold + trim; seconds upfront for held
  beats; Engine-Truth caveat — the better-MOVING take wins (see memory
  `seedance-2d-animation-anchor`).
- **Belly-cut lore (DR #33k):** Sparkle Horse's head stays intact, always.
- **Star staging (gate #3):** stills must read "cut the string," never "blade at the man."
- **Neighbor spacing (DR #33m):** runner beats never adjacent (board/edit rule).
- **CHANGELOG on every change; STORYBOARD.md on every generation/approval; new
  decisions → concept.md DR (numbered, dated).** Keep the memory truthful
  (`grandmaster-character-design-state`).

## DEFERRED (do not lose, do not start unprompted)

Boombox track pick (1 vs 2; `music/`) · the montage motion library beyond the 8 M7
beats · the animatic phase (where framing/timing get real — all montage frames are
non-final) · the cassette-stinger mockup decision · namespace registration + Cy Bible
authoring (the slice-run plan `docs/active/2026-07-19-first-licks-act2-slice-run-plan.md`
predates the full-story lock — flag for reconciliation, don't act on it) · the costed
pipeline run (NOT green-lit).

**Start by** invoking the two lenses, reading the STORYBOARD tables + beat-sheet-v2,
then present Sean the census plan (scope + proposed output location) before building it.
