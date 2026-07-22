# FIRST LICKS — Continuation (montage generation → art-style drift fix)

*Fresh-session handoff, 2026-07-22. Paste the body below into a fresh Claude Code
session. Propose-only — Sean owns taste and every lock.*

---

You're continuing an active thread on **FIRST LICKS** (the piñata / samurai-homage short
at `briefs/2026-07-02-grandmaster/`). We're in the **MONTAGE (Act 2b) still-generation**
phase: Sean generates the montage stills in the ChatGPT Desktop app from a prompt pack;
you (Claude) own the pack, the art direction, and the diagnosis. Everything is
propose-only — Sean owns taste and every lock.

## FIRST — invoke two standing lenses, in this order (this is how the thread runs)

1. **`/creative-director`** — its critique/audit rubric, turned on the drifted frames.
2. **`/wwf5d`** — grounding + evidence discipline + completeness-critic, to sharpen the pass.

Both propose only. (Other skills invoked down the line this thread: `script-writing` for
the beat sheet, and the Art-Dept `prompt-technique-kit` + register research for prompting.)

## THE IMMEDIATE PROBLEM (diagnose, then fix)

ChatGPT's montage generation **drifted its ART STYLE mid-run.** The piece register is
**`primal-sketch-grit`**: heavy, weight-varying, near-black **BOLD ink kept OVER the
color**, gritty painterly masses shared by figure + background, stark value contrast
(see `registers/primal-sketch-grit/research.md` — Primal is NOT thin/clean/illustrative).
Starting in **batch M2** and worsening through **re-editing**, ChatGPT drifted toward a
**"graphic novel" look: THIN uniform cross-hatched pen-and-ink + a muted WATERCOLOR
wash** (architectural-illustration style) — the opposite of Primal.

**VIEW the evidence** side by side:
- Drifted: `runs/2026-07-19-first-licks-artdept/montage/yard-front-drive.png` — the NJ
  SETTING + overcast TIME-OF-DAY fixes are perfect (colonial, clapboard, mailbox, pole,
  deciduous trees, no palm/desert/sunset), but the LINE went thin/uniform/hatched and a
  watercolor wash replaced Primal's bold painterly grit.
- Known-good on-register: `runs/2026-07-19-first-licks-artdept/montage/yard-home-master.png`,
  `boombox-states.png`, `target-rig.png`, `tree-hero-grounded.png` — heavy bold ink, grit.

When Sean advanced to M3, the boy composited **into** the drifted backgrounds and
inherited the graphic-novel style — so he stopped there.

## LIKELY ROOT CAUSE (confirm it)

**Chain-edit generation loss.** gpt-image drifts when you edit an edit of an edit;
repeated re-editing (to fix the palm/desert/text) "refined" the bold Primal ink into
thin illustrative hatching + watercolor. Composites then read the drifted plate as their
location reference and amplified it.

## THE FIX (propose to Sean, then implement in the pack + orchestration)

1. **NO CHAIN-EDITING.** Each plate = generated FRESH, or a SINGLE edit off a CLEAN
   source (the spring master `yard-home-master.png` / a clean anchor) — never an edit of
   an edit. If a plate drifts, DISCARD and regenerate from the clean source; never keep
   re-editing a drifted output.
2. **Add an explicit ANTI-DRIFT clause** to the register-grit rule (pack standing
   disciplines + the orchestration house rules): name the drift AND the target —
   *"HEAVY bold weight-varying near-black ink kept OVER the color, gritty painterly
   masses, stark value contrast; NOT thin uniform cross-hatching, NOT a watercolor/
   ink-wash illustration, NOT fine-line pen-and-ink, NOT a graphic-novel panel, NOT
   architectural illustration."*
3. **Anchor the look with a known-good keeper** where fresh gen drifts — feed an
   on-register plate (`yard-home-master.png` etc.) as a "match this exact art style"
   reference.
4. **Regenerate the drifted plates** (`yard-front-drive`, and check `usedcar-lot` /
   `petting-zoo` / any M3 output) FRESH with the anti-drift clause; re-composite M3 off
   the clean backgrounds.
5. **Add a per-batch consistency check** to the orchestration: compare each new plate to
   a known-good Primal keeper; if the line went thin/uniform or a watercolor wash
   appeared, reject + regenerate (don't re-edit).

## STATE OF PLAY

- **Pack:** `runs/2026-07-19-first-licks-artdept/montage-prompt-pack-v2.md` (v2, revised
  2026-07-22). **Orchestration:** `runs/2026-07-19-first-licks-artdept/montage-orchestration-v2.md`.
- **Decisions banked:** `concept.md` Decision Record **#21–30** — comedy-engine law,
  season order (END-SUMMER→FALL→WINTER→SPRING→summer, tree blooms only spring),
  disguised-chores→tape, donkey+piñata rhyme, subtle grief, time-of-day law (drama
  reserved for hero beats), East-Coast-NJ setting law, rain discipline, motion
  start-pose rule. Palette/setting law also in `bundle/environment-style.md`. CHANGELOG
  current.
- **Generated so far (ChatGPT):** M1 (seasonal backyards + a sunset `yard-home-fall-day`
  dusk variant), M2 (front-drive / usedcar-lot / petting-zoo — **DRIFTED** to
  graphic-novel), started M3 (boy composited into drifted BGs — **stopped**).
- **Story in one line:** a timid kid trains for a year in his late grandmother's memory
  to take a piñata down "like a small samurai"; the montage is a grounded-suburban
  training montage where the gap between epic movie framing and mundane NJ suburbia is
  the comedy AND the beauty. (Full beat list + the montage arc are in the pack.)

## READ FIRST (in order)

`PHILOSOPHY.md` · `CLAUDE.md` · the memory (grandmaster-character-design-state) ·
`briefs/2026-07-02-grandmaster/concept.md` (esp. Decision Record #21–30) ·
`runs/2026-07-19-first-licks-artdept/montage-prompt-pack-v2.md` ·
`runs/2026-07-19-first-licks-artdept/montage-orchestration-v2.md` ·
`registers/primal-sketch-grit/research.md` (the register truth — heavy bold ink, NOT
thin illustration) · `.claude/skills/art-department/references/prompt-technique-kit.md`
(fresh-vs-edit economy, dependency map, never-chain-styles) ·
`runs/2026-07-19-first-licks-artdept/bundle/environment-style.md`.

## DISCIPLINE

- **$0 unless Sean opens a budget** (Higgsfield subscription credits, never
  `ANTHROPIC_API_KEY`; ChatGPT gen is Sean's own pass). Announce any spend.
- **CHANGELOG on every change; keep the concept Decision Record + the memory truthful.**
- When you change the pack, keep the proven format (the web-search-Primal STYLE clause;
  PATH KEY shorthands; checkpointed batches) and **update the pack + orchestration
  together.**
- **Standing rules:** `primal-sketch-grit` (bold ink grit, anti-drift) · East-Coast-NJ
  setting (no palm/cypress/stucco/desert) · time-of-day variety (dramatic golden-hour
  reserved for hero beats) · rain only where it earns it · motion stills = starting
  poses · scene frames inherit location light (no re-grade) · anti-revenge (burlap/tire,
  no piñata) · grief subtle (decaying boombox, no sad glances) · path-based Desktop-app
  gen (cite by path, never attach).

**Start by** invoking `/creative-director` then `/wwf5d`, then VIEW `yard-front-drive.png`
next to `yard-home-master.png` to confirm the drift diagnosis, and propose the anti-drift
pack + orchestration fix to Sean before anything is regenerated.
