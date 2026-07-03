# anima — Flow-like Interface: Spec Addendum v1.1

**Date:** 2026-07-03
**Status:** Proposals for ratification. Six picks chosen by Sean from the 2026-07-03 design-research + brainstorm session. Extends the v1 spec ([`2026-07-03-flow-interface-uxui-spec.md`](2026-07-03-flow-interface-uxui-spec.md)); grounded in the research brief ([`2026-07-03-flow-interface-design-research-brief.md`](2026-07-03-flow-interface-design-research-brief.md)); companion mockups in [`2026-07-03-flow-interface-mockups-v1.1.html`](2026-07-03-flow-interface-mockups-v1.1.html).
**Decider:** Sean. Every proposal carries a lean; the picks are his. Items that change a *locked* v1 decision are flagged **→ ratify** and consolidated at the end.

---

## What this is

Six additions to the v1 spec, from the brainstorm's top-8. Sean picked **1, 2, 3, 4, 7, 8** — with **Pick 4 (the taste ledger)** flagged as the special one. Picks 5 (morning easel) and 6 (stage-as-gallery) were not carried; Pick 6's dark-stage craft still lands *partially* through Pick 7 and the mockups, but its gallery treatment (light-pool, mat, gray color-check) is deferred, not built.

Nothing here reopens Direction C, the two-font rule, the signature trio, the anti-slop bans, or the WCAG AA contract — every proposal extends them. Two new daemon deltas are introduced (**D5 taste-memory**, **D6 injected-plates**); the rest binds to the CONVERGED daemon as-is or is free/UI-only.

The organizing belief this addendum serves: **the app should feel like an instrument Sean plays and a studio that knows him** — the eye-gate is where he plays fastest, the crew and the taste ledger are what make it *his*.

---

## Pick 1 — The eye-gate becomes an instrument you play *(screen 8, ENHANCED)*

**Purpose.** You cannot judge animation from a still, and the v1 eye-gate shows a still. Every professional animation and dailies tool treats the *rock/flip* as sacred (research §A, §C). This turns the eye-gate from a page you read into an instrument you play: see the motion, judge it clean, decide in one keystroke.

**What to add (to the dark stage).**
- **Rock/flip.** Hold `Space` to rock the loop between the current frame and its neighbor (or play the short loop) at hand-controlled speed; release freezes on the current frame. The illusion of motion only appears in the rock — this is the load-bearing addition.
- **Lights-out.** `L` drops all chrome and shows the frame (or plays the loop) alone on the dark stage; `L` again restores the instruments. The one-key "see it as it ships" toggle (Procreate Dreams' four-finger preview, keyboardized).
- **Onion-skin.** `O` ghosts the approved N-1 (and frame 1 for a loop-return, read from `chain_from`) under the candidate at low opacity — judge whether the character *holds* and the loop will play.
- **Diff/compare.** `D` opens a wipe between two attempts (or candidate-vs-anchor); `[`/`]` drag the wipe line; a difference view highlights identity drift (the "face morphed" catch).
- **Hover-skim.** Hovering a reel cell peeks that frame on the stage without moving the current frame (FCP skimmer).

**Interactions (the locked rhythm, extended).** `Enter` approves **and** cel-flips to the next *unreviewed* frame (auto-advance, skipping approved). `R` opens the retry note **and auto-pauses** the loop. Typing anywhere in a note auto-pauses. `?` summons a keyboard cheat-sheet overlay.

**Daemon.** **Feeds today.** All of it is client-side playback + SVG/canvas overlays over the candidate and approved images the daemon already serves (`GET /runs/{id}/frames/{n}/candidates`, `/image?attempt=K`); `chain_from` comes from `shots.yaml` (artifact read); approve/retry are the existing gates; `next_action` drives auto-advance. No backend change.

**Lean.** Build the rock/flip + lights-out first (highest leverage, lowest cost); onion-skin and diff second. This is the single biggest daily-tool upgrade in the addendum.

**a11y.** Every new key has a visible button on the stage toolbar; the cheat-sheet (`?`) is the discoverability backstop; motion respects `prefers-reduced-motion` (rock collapses to a step, cel-flip to a crossfade); the diff wipe is also expressible as a labelled slider.

**→ ratify (R1):** extends the locked eye-gate keyboard map (`Enter / R / Esc / ↑↓ / numbers`) with `Space`, `L`, `O`, `D`, `[`/`]`, `?`, and adds loop-playback / onion / diff as first-class eye-gate modes.

---

## Pick 2 — Em as a physical hand in the margin *(screen 8, the Em read-out component)*

**Purpose.** Make the critic's read something beautiful to *use*, not a log to parse. Em proposes; she never blocks; her fix is one keystroke from applied.

**What to change.**
- **A fielded instrument, not a line.** The Em read-out becomes four fixed labelled slots beside the frame — `verdict · reasoning · proposed fix · cites` (Storyboard Pro's caption-panel model). The verdict pill keeps its semantic color (pass/borderline/fail).
- **A hand, not a vector.** Her margin mark renders as a pressure/speed-tapered grease-pencil stroke (SyncSketch), so it reads as a hand in the margin — this is the signature grease-red, kept sacred (see the two-reds ratify below).
- **The clause, pre-filled.** Her proposed fix is pre-filled into the retry note, attributed ("prefilled from Em"); accept in a keystroke or edit. Already half-specced in v1; this makes it the default and adds the attribution.

**Daemon.** **Feeds today.** The Em verdict payload already carries `verdict`, `score/confidence`, `reasoning`, the proposed-fix `target → value (rationale)`, and `cites` (per the eye-gate endpoints + the run orchestrator's eye-gate print). This pick is mostly rendering existing data faithfully.

**Lean.** Ship with Pick 1 — they share the stage. Lowest-effort, high-signal.

**a11y.** The read-out is a labelled region announced to screen readers; the grease mark is decorative (`aria-hidden`) with the reasoning text carrying the meaning; the pre-filled clause is a real editable field.

**→ ratify (R2 — the two reds):** onion-skin convention is "previous = red." To protect the grease-red critic signature, **onion "previous" renders as a desaturated cool tint and "next" as `--teal-bright`** — two reds never share the stage. (Lean: yes.)

---

## Pick 3 — The crew at their stations *(cross-cutting: stepper, command bar, working states)*

**Purpose.** A crew is people whose judgment you route trust to. Make each agent visible at their station, their hand on the work legible, and the whole thing directed — not chatted at.

**What to add.**
- **Stations on the stepper.** Each stage names its agent; hovering a stage shows whose hands are on it (Maya=plan, Sam=script, Bea=board, Cy=Bible, Flo=frames, Em=critic, Mo=docent).
- **Provenance line.** Each frame carries a quiet "drawn by Flo (NB2) · read by Em · your call" — trust routed to the right specialist, and the human's call named last.
- **Honest boundaries.** Each agent shows one capability boundary where relevant ("Em reads stills, not motion") — never over-claims (the Clippy law, research §G).
- **Named working states.** The existing "Flo is drawing F04…" / "Maya is costing…" pattern is the model; extend it to name the on-deck agent during a cascade so the async chain reads as a crew working, not a freeze.
- **Directed voice.** The command bar addresses the stage's agent by name; responses render in Newsreader (the serif "voice"); the register is wire-service — no emoji, no exclamation, opinions about *the work* only, never feelings about Sean.

**Daemon.** **Feeds today** for provenance + stations (stage and active agent are in run-state; the drawing model/route is in the candidate payload). **D3 (chat/agent surface)** carries the directed command-bar voice — already a declared delta.

**Lean.** Provenance + stations first (free, feeds today); the directed voice rides D3 when the command bar lands (v1c).

**a11y.** Agent names carry `aria-label`s; the provenance line is real text, not a tooltip-only affordance; working states announce via a polite live region.

---

## Pick 4 — The taste ledger *(NEW surface · the special one · D5)*

**Purpose.** The unfakeable "it's mine." A studio that remembers Sean's eye and reflects it back — transparently, editably — is the thing no generic AI tool can copy. "People treasure what they tweak; the apps we remember are the ones that remember us back" (research §G).

**What it is.** A surface (its own view, reachable from the studio chrome and `⌘K`) that renders **what the studio remembers about your eye** as an append-only, *editable* ledger. Each line is a plain-language taste statement, its **evidence**, its **effect**, and a **forget/edit** control:

> `You reject digital-render looks.` — *from 6 ratified verdicts (HF05)* → *HF05 weighted up in Em's read* · edit · forget
> `Your loops run ~7 heads tall.` — *from the sean-anchor proportion lock (1:7)* → *SF03 proportion gate target* · edit · forget
> `You prefer terse, edit-form prompts.` — *from Bea's establishing-vs-edit discipline you ratified* → *board prompts default to `ONLY CHANGE:` deltas* · edit · forget
> `Stylus stays in the right hand.` — *from your F12 continuity call* → *`IR.sean.prop.stylus-right-hand-always` (hard rule)* · edit · forget

**The honesty contract (load-bearing).** The ledger **never invents a taste fact.** Every line traces to real repo evidence — a ratified Sean verdict in a field report, a register/proportion lock in `character.yaml` or the manifest, a QA reason-code frequency, an Em eval outcome. A thin ledger reads as honestly sparse, never padded (mirrors the museum's structural-honesty contract + PHILOSOPHY's "no invented facts"). This is what separates it from a generic "we personalized this for you" black box.

**Two phases, sequenced.**
1. **Reflect (read-only, first).** Derive the ledger from signals anima *already has* (ratified verdicts, register/proportion locks, QA reason-code frequencies, Em's corpus) and let Sean **edit/forget** any line. Reflection alone is the personalization — safe, honest, and the whole emotional payload.
2. **Act (deferred, second).** Once the reflection is trusted, let ledger lines *weight* routing and critique (a forgotten line stops acting; an edited line acts as edited). Flagged as the deeper, later half — do not couple it to shipping the reflective view.

**Daemon. → new delta D5 (studio taste-memory).**
- **Read:** `GET /studio/taste-memory` → `[{id, statement, evidence:[{kind, ref}], effect, editable, active}]`, derived server-side from the ratified-verdict / lock / reason-code signals. Read-only first.
- **Write:** `PATCH /studio/taste-memory/{id}` (edit the statement/effect) and `DELETE …/{id}` (forget → `active:false`, never a hard delete — reversible).
- **Phase:** derive-and-reflect first (read + forget); the act-on-routing weights ride phase 2. This is the **tough build** — an honest derivation from real repo signals + safe write-back is the genuinely hard, genuinely special part.

**Lean.** Build the read-only reflective ledger + forget first; it delivers the entire "it's mine" feeling before any auto-acting exists. This is the pick to over-invest in.

**a11y.** Standard editable list — labelled rows, real controls for edit/forget, `aria-live` on changes; plain Newsreader/JetBrains-Mono, no color-only meaning.

**→ ratify (R3):** adds a **new surface** (the taste ledger) and a **new daemon delta D5**. Net-new, doesn't change an existing lock, but worth explicit sign-off given the delta and its "act" phase-2.

---

## Pick 7 — Warmth-as-motion, made a doctrine (+ the one earned delight) *(design system)*

**Purpose.** Codify the research's clearest finding so the build can't drift into skeuomorph-kitsch: **warmth is motion + instant response, not texture** (Procreate Dreams is the existence proof — its warmth is 100% haptics/gesture/responsiveness, 0% decoration).

**What to add (to the design system's motion section).**
- **The tactility budget is spent on:** the cel-flip family (frame advance, stage swaps), sub-100ms keyboard→frame response, and *optional, off-by-default, seam-only* sound (a soft paper-slide on advance, a pencil-tick on approve). Nowhere else.
- **Never spent on:** faux-paper texture on the stage, page-curl, drop shadows-as-desk-objects, ambient/idle animation. The warm-paper `#FBF5E9` chrome supplies "paper" as a calm static surface; that is the whole paper budget.
- **The one earned delight — the ship moment.** When a full loop passes the gate (`next_action: done`), the stage "lights up" (warms) and the finished loop plays, with a small hand-drawn flourish from Sean's pencil character. One quiet, earned celebration of a real milestone, executed to the product's full quality bar (Raycast's confetti principle: useful + well-made, never a cheap easter egg).

**Daemon.** **Free / UI-only.** The ship trigger reads `next_action: done`; everything else is client motion.

**Lean.** Cheapest pick — mostly a written doctrine + one moment. Land it early so every other build inherits the rule.

**a11y.** All motion ≤260ms, `prefers-reduced-motion` collapses the cel-flip to a ≤1-opacity crossfade and the ship flourish to a static frame; sound is opt-in and never the sole signal.

**→ ratify (R4):** the ship moment is a *milestone* delight, not a fourth signature — the locked signature trio (warm/dark seam · grease-pencil mark · cel-flip) stays three. Confirm it doesn't dilute the trio. (Lean: it's a milestone, keep the trio at three.)

---

## Pick 8 — The Bible as a folder-chip, with the per-frame recipe shown *(screens 10 + 8 · D6)*

**Purpose.** Identity injection is where drift is judged, so make it legible. A character is a folder you drop, and the eye-gate shows exactly which plates were injected for this frame — injection as an auditable act, not Flow's opaque "an ingredient was used."

**What to add.**
- **Folder-chip.** In the character builder and a cast rail, a character is one chip that expands to its Bible (anchor / turnarounds / expressions / props). Drop the *character*; the generator (Cy/Flo) selects the right plates per shot.
- **The recipe strip.** On the eye-gate, a quiet strip shows the plates injected for this candidate — role-tagged and in order ("anchor + front turnaround + stylus prop, appended last"). Bible health (clean anchor? proportion gate green?) shows as a plate badge.

**Daemon. → new delta D6 (injected-plates)** — `GET /runs/{id}/frames/{n}/candidates` gains, per candidate, `injected_plates: [{character_id, plate_path, role_tag, order}]`. Extends D4's proposed `route` field (same payload). The folder-chip authoring rides **D4** (Cy `bible *` jobs).

**Lean.** The recipe strip (D6) is a small, high-signal read; the full folder-chip authoring UI rides the v2 character builder. Ship the recipe read first.

**a11y.** Chips in mono with `aria-label`s; the recipe strip is real text; plate badges carry text, not color-only status.

**→ ratify (R5):** confirm **D6** joins the delta roadmap (v2, with D4).

---

## Daemon deltas (updated)

The v1 spec declared D1–D4. This addendum adds D5 and D6.

| # | Delta | Backs | Phase |
|---|---|---|---|
| D1 | `retry` gains optional `annotations {overlay, pins:[{x,y,text}]}` | eye-gate red pen + pins → NB2 edit ref | v1c |
| D2 | Brainstorm front-door surface | the room / brief emit | v1c |
| D3 | Chat / agent surface (message → active agent + intent→action) | the directed command bar (**Pick 3**) | v1c |
| D4 | v2 stage endpoints (Cy `bible *` authoring, `route` on candidate, Motion job + critic) | character builder (**Pick 8**), generate grid, motion | v2 |
| **D5** | **Studio taste-memory** — `GET /studio/taste-memory` (derived read), `PATCH`/`DELETE` (edit/forget). Read-and-reflect first; act-on-routing weights phase 2. | **the taste ledger (Pick 4)** | **v1c/v2 (read first)** |
| **D6** | **`injected_plates` on the candidate payload** `[{character_id, plate_path, role_tag, order}]` (extends D4's `route`) | **the per-frame recipe (Pick 8)** | **v2 (with D4)** |

All additive; none regress the read-only tracer-bullet or the byte-identical pipeline guarantee. D5's derivation is read-only over existing signals — no pipeline change; the write side is audited like the CLI's own mutations.

---

## Build sequencing + model routing

Mapped to Sean's stated split — **Fable 5 for the tough builds; Codex + Opus 4.8 for the rest.** Lean, adjust freely.

**Tough tier → Fable 5.**
- **Pick 1's eye-gate interaction engine** — loop playback, onion-skin compositing, the diff/wipe, the keyboard state machine, the cel-flip timing. The interaction density is the hard part (the daemon reads are trivial).
- **Pick 4's taste-memory derivation + D5** — deriving an *honest, non-fabricated* ledger from real repo signals (ratified verdicts, locks, reason-code frequencies) and the safe, reversible write-back. This is the special-but-hard build; give it the strongest model.

**Rest → Codex + Opus 4.8.**
- **Pick 2** (Em read-out rendering — mostly presenting existing data), **Pick 3** (crew stations/provenance + the D3 voice), **Pick 7** (the motion doctrine + the ship moment), **Pick 8's recipe strip + D6 read**, and the UI shells around Picks 1 and 4.

**Suggested order:** Pick 7 doctrine (cheap, everyone inherits it) → Pick 2 (rides the stage) → **Pick 1** (the daily-tool upgrade, Fable 5) → Pick 3 (stations/provenance) → **Pick 4 read-only ledger** (Fable 5, the special one) → Pick 8 recipe strip → later: Pick 4 phase-2 acting, Pick 8 authoring UI.

---

## Ratification asks (consolidated — your explicit yes)

- **R1 — eye-gate keys + modes.** Extend the locked keyboard map with `Space` (rock), `L` (lights-out), `O` (onion), `D` (diff), `[`/`]` (wipe), `?` (cheat sheet); add loop/onion/diff as eye-gate modes. *(Lean: yes.)*
- **R2 — the two reds.** Keep grease-red for Em (signature); render onion "previous" cool-desaturated, "next" `--teal-bright`. *(Lean: yes.)*
- **R3 — the taste ledger + D5.** Add the new surface and the taste-memory delta; ship read-only reflect first, defer acting. *(Lean: yes — this is the special one.)*
- **R4 — the ship moment.** Add it as a milestone delight; keep the signature trio at three. *(Lean: yes.)*
- **R5 — D6.** Confirm `injected_plates` joins the v2 delta roadmap with D4. *(Lean: yes.)*

None of R1–R5 touch Direction C's palette/type/signature, the anti-slop bans, or the a11y contract.

---

## Parked for the museum redesign (noted per Sean, 2026-07-03)

**The museum auto-composes itself as you work.** From the brainstorm's exploratory branches (ideas 99 + 105): rather than the museum being a post-hoc build step, every approve / reject / retry / escalation *quietly composes its own exhibit as the run happens* — so by the time a loop ships, its walkthrough already exists, drafted from real decisions. Pairs with the Stage-1 research on museum presentation (research brief §E: curated linear scrollytelling + before/after sliders, curated to decision-moments). **This is the anchor idea for the future museum redesign + setup — hold it there; not in scope for the v1.1 interface build.** Sean deprioritized the museum for this pass on purpose; this note keeps the idea durable for when the redesign starts.

---

*Ratified picks from the 2026-07-03 session. This addendum + the v1 spec + the mockups are the build inputs for the enhanced interface; D5 and D6 are the backend's new phased asks. Update in place when a decision changes, per the anima maintenance convention.*
