# anima — Flow-like Interface: UX/UI Design Spec (v1)

**Date:** 2026-07-03
**Status:** Design spec, ratified in the 2026-07-03 interface-design brainstorm. Ready for Claude Code to build from. Companion artifacts: the clickable prototype ([`2026-07-03-flow-interface-ux-prototype.html`](2026-07-03-flow-interface-ux-prototype.html)) and the daemon contract ([`2026-07-02-daemon-build-plan-CONVERGED.md`](2026-07-02-daemon-build-plan-CONVERGED.md)).

**Decider:** Sean. Every fork in this doc was resolved by him during the session; the leans that carried are marked where it matters.

---

## What this is

The face over anima's pipeline. A native desktop app (Electron/Tauri shell + the FastAPI daemon as a sidecar) that lets Sean drive the gates — brainstorm, plan, script, storyboard, animatic, generate, assemble — visually, ending on a simple timeline to string clips, preview, and export. It is a **daily tool first, a portfolio piece second**, and it must read like a studio, not a terminal.

The differentiator is not the surfaces — Flow has those. It's the **pipeline's opinion**: the cost gate, the critic's read, the Bible lock, the human-owned animatic, the run state that always knows your next move. This spec exists to make that opinion legible and the 80% loop fast.

### How to read it

Prose carries the *why*; tables carry the reference data (tokens, endpoints, states). Every screen section gives: **purpose · layout · interactions · states · endpoint bindings · microcopy**. The prototype is the moving picture; this is the blueprint.

---

## The three beliefs this UI serves

1. **Read like a studio, not a terminal.** Warm paper, editorial type, the critic's note in the margin. The chrome is a workspace, not a console. Where the pipeline used to speak in CLI flags, the app speaks in decisions.
2. **The human owns taste and timing; the critic proposes.** Every gate reduces to one human choice. Em never blocks with a red X — she proposes a fix you accept, edit, or ignore in a keystroke. The animatic gate is non-negotiable because the human owns timing.
3. **The run drives the app.** The daemon's `next_action` field is the navigation spine. The app always answers "what's my next move?" without you hunting for it.

---

## Design system

### Color — OKLCH, two surfaces bridged by one accent

The load-bearing idea: **warm chrome where you work, a dark stage where you judge.** The art is the subject and art needs a neutral wall; the pipeline's opinion is human and stays warm. Teal bridges both.

| Token | Hex | OKLCH | Role |
|---|---|---|---|
| `--paper` | `#FBF5E9` | `0.96 0.02 85` | page canvas (warm) |
| `--panel` | `#F3EAD8` | `0.93 0.03 84` | chrome panel (bars, rails) |
| `--card` | `#FFFDF7` | `0.99 0.008 90` | raised card |
| `--line` | `#E4D8C0` | `0.88 0.03 84` | hairline border |
| `--line-2` | `#C9B994` | `0.78 0.045 84` | emphasis border |
| `--ink` | `#23201B` | `0.25 0.01 70` | primary text (AA on paper: 12.6:1) |
| `--ink-2` | `#5A5348` | `0.42 0.02 75` | secondary text |
| `--ink-3` | `#6F6349` | `0.46 0.02 78` | hints, captions (darkened from `#9A8E75` for AA at ≥11px) |
| `--stage-0` | `#15161A` | `0.22 0.008 265` | dark stage canvas |
| `--stage-1` | `#1B1D22` | `0.26 0.008 265` | stage inset |
| `--stage-line` | `#2A2E38` | `0.32 0.012 265` | stage border |
| `--stage-ink` | `#EAEAF0` | `0.93 0.004 265` | text on stage |
| `--stage-mute` | `#9AA0AA` | `0.68 0.01 265` | muted on stage |
| `--teal` | `#0A3E42` | `0.34 0.06 200` | action / next (on warm) |
| `--teal-bright` | `#37C7A6` | `0.76 0.11 168` | action / next (on stage) |
| `--teal-bg` | `#E7F0EC` | — | teal tint fill |
| `--grease` | `#B23A2E` | `0.52 0.15 32` | the critic mark, fail, attention |
| `--amber` | `#B2802E` / `#E8A33D` | — | borderline (warm / stage) |
| `--green` | `#2F6B4F` / `#5BC98C` | — | approved / pass (warm / stage) |

**Rules.** One splash per surface, never two. Semantic mapping is fixed: teal = *next/active*, amber = *borderline*, grease-red = *fail/attention/the critic's pen*, green = *approved/pass*. Everything else is neutral. Flat fills only — no gradients, no glow. The paper grain is a static texture, never animated.

### Type — two families, one rule

**Newsreader** (serif) is *what you read*: gate titles, the screenplay, Em's reasoning, plan/script/concept prose, empty-state invitations. **JetBrains Mono** is *what you scan*: stage names, verdicts, criteria cites, cost, filenames, timestamps, buttons, the command bar. No third font, ever — this matches the portfolio's identity so the app and the portfolio read as one studio.

| Role | Family / weight | Size | Notes |
|---|---|---|---|
| Display | Newsreader 500 | 20px | gate titles, hero |
| Title | Newsreader 500 | 17px | screen titles |
| Heading | Newsreader 500 | 15px | section heads |
| Read | Newsreader 400 | 14px / 1.55 | prose, ≤68ch, screenplay ≤58ch |
| Label | JetBrains Mono 400 | 12px | UI chrome, data |
| Micro | JetBrains Mono 400 | 11px | hints, cites |

Two weights only (400/500). Sentence case everywhere except the screenplay's scene headings (screenplay convention: `INT. STUDIO — DAY`).

### Space, radius, density

4px base. Gaps 6 / 8 / 12 / 16 / 24. Screen padding 16–18px. Radius: cards 12px, controls 8px, pills 20px. Density is **compact** — this is a power tool for one expert user, not a consumer onboarding flow.

### Motion — intentional, ease-out-expo

| Moment | Motion | Duration |
|---|---|---|
| Hover / press | opacity / `scale(0.98)` | 120ms |
| Panel / stage swap | crossfade | 200ms |
| **Frame advance** | **cel-flip** — the next frame slides in from the right, like turning a cel | 260ms |
| Approve | teal check-pulse on the reel cell | 180ms |
| Retry note open | field expands | 160ms |
| Stage ↔ warm-mat toggle | crossfade | 200ms |

`@media (prefers-reduced-motion: reduce)` collapses every motion to an instant swap or crossfade. Never animate layout properties. No bounce, no elastic.

### The signature

Spend boldness in three places and keep everything else quiet: **the warm/dark seam** (the studio desk holding a dark lightbox), **the red grease-pencil critic mark** (Em in the margin, the annotation pen), and **the cel-flip** on frame advance. That's the memorable trio; the rest is disciplined restraint.

### Anti-slop bans (enforced)

No cream-serif-terracotta marketing hero (this is a tool, the warmth is earned through the pencil-test materials). No near-black-plus-acid-accent. No gradient text, no glassmorphism, no side-stripe accent borders, no identical card grids, no tracked-uppercase eyebrow on every section, no hero-metric template. Em-dashes stay out of UI microcopy (periods and colons instead); they're allowed only in the project-name convention (`pencil-test — act 2`) and serif "voice" prose.

### Accessibility (WCAG 2.1 AA) — build contract

Ratified against an independent audit (2026-07-03). The visual design passed; these are the requirements the build carries so it stays clean *and* usable. None change the aesthetic.

- **Contrast.** Body/label text ≥4.5:1, large/bold ≥3:1, UI-component boundaries ≥3:1. `--ink-3` was darkened to `#6F6349` (≈4.9:1 on paper and panel) — it failed at `#9A8E75`. Text never sits on a fill below these ratios; amber and the hairline borders carry fills and borders, not text.
- **Type floor: 11px, no exceptions.** Every functional string — clip ids, cites, chips, hints, timestamps — is ≥11px. The verdict/state colors already pass; the sizes are the discipline.
- **Real controls.** Every clickable is a `<button>` (or `<a>` for navigation), never a `<span onclick>`: run cards, the wordmark, attempt cells, reel cells, route tiles, and the runtime pins. Tab-reachable, announced, focusable.
- **Accessible names.** Every icon-only control carries an `aria-label` (`Red pen`, `Pin a note`, `Clear marks`, `Toggle warm mat`, `Send message`); `title` stays for mouse users. Decorative glyphs and the SVG art are `aria-hidden`.
- **Focus.** A visible, palette-aware `:focus-visible` ring — 2px `--teal` on warm surfaces, 2px `--teal-bright` on the stage (both clear 3:1). Never `outline: none` without a replacement.
- **Landmarks + headings.** `<header>` (app bar), `<nav aria-label="pipeline stages">` (stepper), `<main>` (the stage), a labelled command-bar region. One `<h1>` per active screen; gate titles are headings, not styled `<div>`s.
- **Keyboard-first, fully.** The eye-gate global keys (Enter / R / Esc / ↑↓, number keys for attempts) are the fast path; every gate action also has a visible button. **The annotation is operable without a pointer:** freehand pen is a pointer-enhanced convenience, but every spatial correction is *also* expressible as a keyboard-placed pin + text (`P` drops a pin at frame-center, arrows nudge, type the note) or the retry note itself. No correction is mouse-gated.
- **Toggles carry state.** The warm-mat toggle (and any mode control) reflects `aria-pressed` + a visible on-state, never inferred from a computed color.
- **All five doctrine states are built,** not just the happy path: empty, loading (skeletons), working (agent-named + poll), error (what happened + the one fix), busy/409. The async `202 {job_id}` polling and the "crew working" overlay are first-class, never `setTimeout` stand-ins.
- **Reduced motion** collapses the cel-flip to a ≤1 opacity crossfade (not a dead cut); scope the reduce rule to `animation` and long transitions so hover/press feedback survives.

*Prototype status:* the token, the 11px floor, palette-aware focus rings, `aria-label`s on icon controls, the stated mat toggle, and the de-duplicated cost line are applied in the prototype. The deeper semantic pass (full `<button>` conversion, landmarks, the keyboard-pin path) and the error/busy/empty state mocks are specified here as build requirements; they're the first hardening tasks when Claude Code builds v1.

---

## Core components

The reusable primitives Claude Code builds once and composes everywhere.

- **Top stepper** — the pipeline as a horizontal progress map: `brainstorm · plan · script · storyboard · animatic · generate · assemble`. Current stage lit teal; done stages carry a check and are clickable to revisit; todo stages are muted. Preserves full width for the stage.
- **Decision card** — the gate primitive: the agent's proposal (read) + one primary action + one "send back". Nothing competes with the single choice.
- **Em read-out** — `EM · <verdict pill> · <reasoning> · <cite>`. Verdict pills: `pass` (green), `borderline` (amber), `fail` (grease). Lives on the dark stage as an instrument reading.
- **Command bar** — the docked chat, present on every run screen. Context label shifts (`the room…` in brainstorm, `talk to the crew…` elsewhere). Type to message an agent or trigger the next action.
- **Reel filmstrip** — the exposure sheet: per-frame cells with status (✓ approved / number pending / spinner generating / amber current). Click to jump.
- **Cost ledger line** — `spent $X · est $Y · <model>`. Mono, always visible during spend.
- **Annotation layer** (shared) — red pen (freehand) + pin (click-to-point-and-type) over any image. Used in the eye-gate and the brainstorm board. Detailed under the eye-gate.
- **Skeleton loaders, empty-state block, toast** — per the states doctrine below.

---

## The user journey

Two entry modes, one spine. A **brief that already carries a `shots.yaml`** is back-compat (`plan → generate`, byte-identical to the CLI). A **spark** goes through the full front door and authoring path.

```
Dashboard ──▶ New project ──▶ BRAINSTORM (front door) ──emit brief──▶ PLAN gate
                                                                          │
   ┌──────────────────────────────────────────────────────────────────┘
   ▼
PLAN ─▶ [SCRIPT ─▶ STORYBOARD] ─▶ [ANIMATIC] ─▶ GENERATE (eye-gate loop) ─▶ ASSEMBLE ─▶ Timeline / export
        └ authoring only ┘         └ opt-in ┘    └ the 80% screen ┘
```

Navigation is driven by the daemon's `next_action.kind` — each token routes to a screen: `planning`/`approve_plan`, `scripting`/`approve_script`, `storyboarding`/`approve_storyboard`, `approve_animatic`, `generating`/`review_frame`/`assemble`, `done`. Brainstorm is the pre-run front door (it produces the brief `POST /runs` consumes); everything after is a real `run_state` stage.

**Advance model (hybrid, locked):** inside the eye-gate, approving auto-advances frame → frame (a fast loop). At stage boundaries (plan → script, etc.) the app pauses on the run — big decisions get a deliberate confirm, and the async cascade (approve-plan can run Maya → Sam → Bea) surfaces as a "crew working" state, not a freeze.

---

## Global patterns

**Window model:** single window. Dashboard and runs share it; solo creator, one piece at a time.

**States doctrine** — every screen inherits these five:

| State | Treatment | Microcopy shape |
|---|---|---|
| Empty | An invitation, not an apology. Names the space, offers the verb. | "Start a new short. Bring a spark and the room opens." |
| Loading | A skeleton of the *target* screen, never a spinner-in-a-void. | — |
| Working (mid-gen) | Names *which agent* is running; a live poll pulse; logs available on tap, not shoved. | "Flo is drawing F04…" · "Maya is costing the plan…" |
| Error | What happened, then the one recovery action. No "Error:", no first person. | "Couldn't reach the model. Retry, or check the log." |
| Busy (409) | The run is owned by another action; offer to watch it. | "This run is busy. View the running job." |

**Async job model:** every POST gate returns `202 {job_id}`; the UI polls `GET /jobs/{job_id}` and re-reads status on completion. While a job owns the run, the mutating `next_action` is suppressed (the active-cascade overlay) so you can't double-fire.

**Keyboard (locked):** `⌘K` command palette (jump to any run / stage / action). Eye-gate: `Enter` approve, `R` retry, `Esc` cancel, `↑↓` frames, number keys switch attempts. `⌘Enter` approves a gate.

**The shared annotation layer:** red pen + pin, mounted on any judged image — one component, two homes (brainstorm references, eye-gate candidates). Spec under the eye-gate.

---

# v1 screens — chat + gates over the orchestrator

## 1 · Dashboard (run gallery)

**Purpose.** The front door and the resume point. It answers one question per run: *what's my next move here?*

**Layout.** A warm header (`anima` wordmark · `studio` tag · search · `＋ New project`), then a responsive grid of run cards. Each card is a small dark-mat thumbnail (latest approved frame), the run name (Newsreader), a stage chip (mono), and — the load-bearing part — the run's **`next_action` rendered as a call to action** ("F03 waiting on your eye →", "Plan ready · $1.10 →", "Art-viz: pick a route →"). A dashed `＋ New project` card opens the brainstorm room.

**Interactions.** Click a card → open that run at its current stage. `＋ New project` → brainstorm front door. `⌘K` → command palette.

**States.** *Empty:* "No runs yet. Start a short and the room opens." + the new-project card. *Loading:* skeleton cards. *Working:* a card mid-job shows the agent + pulse ("Maya is costing…"). *Error:* a card that failed to load its state shows "Couldn't read this run. Open the log."

**Endpoints.** `GET /runs` (id, stage, slug, updated_at, thumb, `next_action`). `POST /runs` is reached *through* the brainstorm emit, not directly from here.

**Microcopy.** Cards lead with the verb of the next move. Never "In progress" — always the specific move.

## 2 · Brainstorm front door (NEW) — the room

**Purpose.** Turn a one-line spark into a Maya-ready brief bundle (`concept.md` · `00_studio_brief.md` · `character_seeds.yaml`), and gather the visual language for everything downstream. This is the [`brainstorm-front-door`](../../.claude/skills/brainstorm-front-door/SKILL.md) skill made visual.

**Layout.** Three zones inside the run shell.

```
┌ chain rail ┬──────────── the board ─────────────┬── sidecar ──┐
│ ✓ spark    │  ART-VIZ · one hero frame, 3        │ LOCKED      │
│ ✓ expand   │  registers (render on Flow, pick)   │ DECISIONS   │
│ ✓ interro… │  [ Route A ][ Route B ][ Route C ]  │ spark · …   │
│ ● art-viz  │  [ ＋ drop a reference ]            │ premise · … │
│  stress    │  (characters · styles · bgs)        │ tone · …    │
│  synth     │  ← red pen + pin on any image       │ [Emit →]    │
└────────────┴─────────────────────────────────────┴─────────────┘
                     the room (command bar)
```

- **Chain rail** — the brainstorm's own progress (`spark → expand → interrogate → art-viz → stress-test → synthesize`), distinct from the run stepper. Current stage lit.
- **Board** — the visual-exercise canvas. In ART-VIZ it shows the ≥3 hero-frame route cards (same composition, different registers) for Sean to render on Flow and pick; a `＋ drop a reference` tile gathers character / style / background visuals. Any image takes the **shared annotation layer** (red pen + pin) for marking up.
- **Sidecar** — the append-only **LOCKED DECISIONS** spine (Sean's locks, verbatim), and the `Emit brief → start run` action.
- **The room** — the command bar becomes the conversation ("the room — deepen, or proceed?"); the front-door orchestrator runs the chain here one question at a time.

**Interactions.** Chat drives the chain. Pick a route → locked to the sidecar. Drop / generate a reference → onto the board, annotatable. `Emit brief` → writes the bundle, validates, and starts the run at Plan (`POST /runs`). Stress-test surfaces a `proceed`/`revise` verdict before emit.

**States.** *Empty:* "What's the spark? One line is enough." *Working:* the running stage named on the rail. *Art-viz:* routes present, awaiting a pick. *Stress-test:* the verdict card (proceed with named residuals / revise). *Ready:* `Emit` enabled once synthesize completes; the anti-pattern rubric flags surface plainly before emit.

**Endpoints (new front-door surface — daemon delta, see below).** Run the chain, persist the session sidecar (LOCKED DECISIONS + PROPOSALS), store art-viz / reference images, and emit → `POST /runs {brief_dir}`. The docs already frame this as the "① front door" that meets the daemon "exactly at the brief."

**Microcopy.** "the room — deepen, or proceed?" · "Emit brief → start run" · route labels are specifics, never categories ("Route A · faithful", not "Style 1"). $0 stage — Sean renders on Flow; the app never spends here.

## 3 · Run overview / status

**Purpose.** The run's home base and the pause point between stages. Always answers "what's my next move?"

**Layout.** The stepper up top; a hero decision block naming the current `next_action` ("Your move: review F03") with the primary action, a revisit affordance, and the cost ledger; a mini reel of frame states. On a stage boundary (post-cascade), this is where you land.

**Interactions.** Primary button follows `next_action`. Any done stepper stage is clickable to revisit (read-only where locked). The command bar is docked.

**States.** *Working:* "The crew is drafting…" with the active agent and a pulse (this is the post-approve-plan cascade view). *Error:* the failed gate + "See the log · Retry". *Busy:* "This run is busy. View the running job."

**Endpoints.** `GET /runs/{id}/status` (stage, `next_action`, frames), `GET /runs/{id}` (full state), poll `GET /jobs/{job_id}` while a job runs.

**Microcopy.** "Your move: <specific>". "The crew is drafting." Never a bare spinner.

## 4 · Plan gate — the differentiator

**Purpose.** See Maya's plan and what it will cost, then decide to spend. Flow has no equivalent; this is the trust screen and the portfolio flex.

**Layout.** A decision card: the plan as readable prose (Newsreader), then a **cost-preview card** — low / median / high as three cells (median accented teal) with a by-phase breakdown and the honest "estimate, not a cap". Primary `Approve plan`, secondary `Send back`.

**Interactions.** `Approve plan` → `202` job (may cascade to Sam + Bea in authoring mode) → land on the working state, then the next gate. `Send back` → a note field → returns to Maya. `⌘Enter` approves.

**States.** *Working:* "Maya is costing the plan…" *Approved:* "Plan approved. The crew is drafting." → cascade. *Error:* "Couldn't cost the plan. Retry."

**Endpoints.** `GET /runs/{id}/artifacts/plan` (plan.md), `GET /runs/{id}/cost-estimate` (low/median/high, by_phase), `POST /runs/{id}/plan/approve` → `202 {job_id}`.

**Microcopy.** "Nothing burns compute until you approve." "Approve plan." "Send back." Cost cells labelled `low · median · high`; the caption reads "estimate, not a cap".

## 5 · Script gate — screenplay + beats (ENHANCED)

**Purpose.** Read Sam's treatment like a real script *and* check the beats that form the Sam→Bea contract. Sam proposes; Sean decides; no critic gate here (the taste call is human).

**Layout.** A `Script | Beats` toggle above a decision card. **Script view** renders `script.md` in Final Draft / Celtx format: scene headings (caps, mono), action lines, centered character cues, indented dialogue, parentheticals — a readable screenplay page, ≤58ch, JetBrains Mono (the screenplay's native Courier lineage, on-brand). **Beats view** renders `beats.json` as the structured beat sheet (id · title · intent · cast). Primary `Approve script`, secondary `Send back`.

**Interactions.** Toggle is instant (no reload). Approve → advances to storyboard. Send back → note → Sam.

**States.** *Working:* "Sam is drafting the treatment…" *Empty (back-compat run):* the script stage is skipped; the screen isn't reached.

**Endpoints.** `GET /runs/{id}/artifacts/script` (script.md → screenplay view) + `beats.json` (beats view — served in the artifacts set). `POST /runs/{id}/script/approve`. No backend change; both artifacts already exist.

**Microcopy.** Toggle: "Script" / "Beats". "Read it like a script, or check the beats." "Approve script."

## 6 · Storyboard curation gate

**Purpose.** Curate Bea's draft shot list, then lock it. This is a **curation**, not an acceptance — Sean cuts, reorders, adds, then locks the `shots.yaml` that GENERATE consumes.

**Layout.** Bea's board as a 2×3-style shot grid (Flow precedent), each shot a card (frame id · beat link · one-line intent · a thumbnail slot). Edit affordances: reorder (drag), cut, `＋ add shot`. Primary `Lock the board`, secondary edit actions.

**Interactions.** Drag to reorder; cut a shot; add a shot; edit a shot's intent. `Lock the board` re-validates coverage (every beat boarded) + the cast conflict check, and refuses to lock a failing board with a clear reason. When `--frames N` is set, the lock enforces the exact count.

**States.** *Working:* "Bea is drafting the board…" *Invalid lock:* "Beat 3 isn't boarded. Add a shot or the board won't lock." (names the gap).

**Endpoints.** `GET /runs/{id}/artifacts/storyboard` (storyboard.md + shots.yaml), `POST /runs/{id}/storyboard/approve` (the curation gate — re-validates before locking).

**Microcopy.** "This gate is a curation: cut, reorder, then lock." "Lock the board." Invalid: name the beat, name the fix.

## 7 · Animatic placement gate (opt-in) — the non-negotiable

**Purpose.** The human owns timing. Drop one silhouette rough per frame that pins placement (where they stand, which way they face, scale, leg count) *before* anything is drawn, plus the holds that drive pacing. Opt-in (`--animatic`), off by default.

**Layout.** A row of per-frame drop slots (`F01 … FNN`), each accepting a `F<NN>.png` silhouette (filled slots show a check + thumbnail; empty show "drop"). A holds strip (`holds.json` — per-frame hold counts). Primary `Ingest & generate`, secondary `Skip animatic`.

**Interactions.** Drag a rough onto a slot (or a whole frame-named directory at once). Edit a hold. `Ingest & generate` → deterministically ingests roughs + holds into run-state (the locked board is never mutated; the rough rides last + role-tagged into GENERATE) → GENERATE.

**States.** *Empty:* "Drop a silhouette per frame. Rough is enough — it just pins the placement." *Partial:* slots that still need a rough are marked. *Off:* the stage is absent from the stepper; storyboard → generate is byte-identical.

**Endpoints.** Rough upload (multipart), `POST /runs/{id}/animatic/approve`. Ingestion is deterministic — no model call, no spend.

**Microcopy.** "You own timing." "Ingest & generate." "Skip animatic." Silhouette recommended, stated as a hint not a rule.

## 8 · Generate / eye-gate — the 80% screen (ENHANCED)

**Purpose.** Review each candidate, approve it or retry it with direction. This is where Sean lives; **speed is the feature**, and the annotation tools make the direction spatial.

**Layout.** The **dark stage** dominates: a label row (`STAGE · F03 · <label>`, the **annotation toolbar**, the attempt selector, the warm-mat toggle), the candidate on a cream mat (toggleable to a dark mat), and **Em's read-out** along the bottom (`EM · borderline · 0.72 · "<reasoning>" · <cite>`). Beneath, a warm **action bar** (approve / retry, cost) and the **reel filmstrip**. The command bar docks below.

**Interactions (keyboard-first, locked).**
- `Enter` → approve the shown attempt → **cel-flip** to the next frame (auto-advance in the loop).
- `R` → open the retry note, **prefilled with Em's proposed fix**. Edit, or `⏎` to send. `Esc` cancels.
- `↑↓` walk frames; number keys / click switch attempts; click a reel cell to jump.
- `☀` toggles the stage between neutral dark and a warm mat (the blend Sean asked for — neutral for honest judging, warm on demand).

**The annotation layer (shared, NEW).** A toolbar over the stage: **cursor** (default, annotations show but don't capture), **red pen** (freehand red strokes, ~4px, à la Flow), **pin** (click to drop a numbered pin + a text input, à la ChatGPT's point-comment), **clear**. Marks live on an SVG overlay in normalized (0–100) coordinates so they scale with the frame. On **retry**, the payload composes: `{ note: <Em's fix, edited>, annotations: { overlay, pins:[{x,y,text}] } }`, and the note header shows a chip — `+ 2 marks · 1 pin on the frame`. The daemon forwards the annotation as an edit reference to NB2 (see daemon delta). Annotations clear on frame change.

**States.** *Generating:* skeleton frame + "Flo is drawing F03…" (poll). *Verdict-in:* Em reads (pill + reasoning). *Your eye:* pass / borderline / fail. *Retry:* note open, annotations composing. *Approved:* teal pulse → advance. *Busy (409):* "This run is busy. View the running job." *All approved:* auto-route to assemble.

**Endpoints.** `GET /runs/{id}/frames/{n}/candidates` (image list + Em verdict), `GET /runs/{id}/frames/{n}/image?attempt=K`, `POST /runs/{id}/frames/{n}/approve {attempt}`, `POST /runs/{id}/frames/{n}/retry {note, annotations?}` → `202 {job_id}`, poll `GET /jobs/{job_id}`, `GET /runs/{id}/status` for `next_action`.

**Microcopy.** "Your eye on F03." Verdict pills: `pass · borderline · fail`. Retry note header: "prefilled from Em". Keyboard hint: "⏎ approve · R retry · mark with ✎ / ◉ · ↑↓ frames". Re-roll toast: "Re-rolling F03. Note and annotations sent as a correction."

## 9 · Chat shell — the command bar (cross-cutting)

**Purpose.** The ambient way to talk to the crew and nudge the run, present on every run screen. Never the main event.

**Layout.** A docked bar at the bottom: a message field + send. Context label per stage. Not a separate view — always in reach, never blocking.

**Interactions.** Type to message the stage's agent (Maya, Sam, Bea, Cy, the front-door room). A natural-language request can trigger the stage's `next_action` ("approve", "retry F03 with the stylus fix"). `⌘K` opens the command palette for structured jumps.

**Endpoints (daemon delta — the chat/agent surface).** A message endpoint that routes text to the active stage's agent and maps intents to gate actions. Not in the current daemon plan; flagged below.

**Microcopy.** "talk to the crew…" / "the room — deepen, or proceed?". Responses render in Newsreader (the serif "voice" — the crew is speaking).

---

# v2 screens — the per-stage visual pages

Each has a proven Flow precedent to copy one at a time. They deepen the v1 gates from "read + decide" into "see + shape".

## 10 · Character builder (Cy)

**Purpose.** Author or reference a character Bible — the folder that identity-locks a character across the whole run. Flow precedent: the "New character" screen (sample cards · describe · reuse-for-consistency).

**Layout.** A Bible workspace. A plate gallery grouped by kind (anchor · turnarounds · expressions · motion plates · costumes · props), each plate a card with its verdict. A right panel holds `character.yaml` made legible: the palette as swatches, proportions (heads-tall), and the `IR.*` rules grouped by category. Cy's three-pass loop is visible — Opus authors the plate prompt → NB2 generates → Gemini verifies — with the **similarity gate** (record-only) and the **proportion gate** (hard, at lock) surfaced as plate badges. Primary `Approve Bible` (locks the criteria).

**Interactions.** `bible init / add / iterate / mutate / approve` mapped to buttons: re-roll a rejected plate (iterate), extend a locked Bible (add), audited edit (mutate). Approve runs the proportion gate and refuses the lock on a fail/indeterminate with the measured reason.

**States.** *Working:* "Cy is baking the turnarounds…" (per-plate). *Gate block:* "The body turnaround reads 1:5.3 against a 1:7 target. Re-bake to lock." *Locked:* the Bible is read-only; re-running bakes plates only, never re-authors.

**Endpoints (daemon delta).** `GET /characters`, `GET /characters/{id}` exist; authoring (`bible init/add/iterate/mutate/approve`) needs endpoints over Cy's `AgentSpec`, driven as jobs like the gates.

**Microcopy.** "Approve Bible." "Re-bake the turnaround." Gate block names the measured number and the target.

## 11 · Storyboard board (Bea)

**Purpose.** The v1 curation gate elaborated into a visual board with real shot thumbnails. Flow precedent: the 2×3 storyboard ("Boy growing up").

**Layout.** The shot grid with thumbnails, drag-reorder, cut, and add — each shot showing its `beat_id` link, cast, and the per-shot prompt (the establishing-vs-edit discipline visible: frame 1 full, later frames `ONLY CHANGE:` deltas, loop-return `chain_from`). Curation affordances are first-class here, not an afterthought.

**Interactions.** Same curation gate as v1, with visual drag and per-shot prompt editing. Locking re-validates coverage + cast conflict + exact-count.

**Endpoints.** As the v1 storyboard gate, plus per-shot artifact reads for thumbnails.

## 12 · Generate grid (Flo + Em)

**Purpose.** The batch complement to the single-focus eye-gate — see every frame and its candidates at once, with Flo's routing and Em's verdicts per cell. Use it to survey the reel; drill into a cell to enter the eye-gate.

**Layout.** A grid of frame cells, each showing the current candidate, its status, Em's verdict pill, and Flo's route (which model / tier drew it). Filters: needs-my-eye / approved / generating. Click a cell → the eye-gate for that frame.

**Interactions.** Grid → eye-gate drill-down. Bulk actions deferred (approve-all is a foot-gun; the human judges each). Route visible for cost transparency.

**Endpoints.** `GET /runs/{id}/status` (frames), `GET /runs/{id}/frames/{n}/candidates` per cell; Flo route surfaced in the candidate payload (daemon delta — add `route` to the candidate response).

## 13 · Motion

**Purpose.** Seedance video between two approved anchor stills, draft → pro. A T2 critic reviews motion arc and identity drift.

**Layout.** Anchor pair (start · end approved frames) → the generated clip in the dark stage player, a `draft | pro` tier toggle, Em's motion read, approve. The reel becomes a clip strip once motion lands.

**Interactions.** Generate draft → preview → escalate to pro on approval or critic-pass. Approve the clip. Same keyboard-first approve/retry rhythm.

**Endpoints (daemon delta).** Motion generation + the T2 motion critic aren't in the daemon plan yet; add a motion job endpoint + candidate/verdict reads mirroring the frame endpoints.

---

# v3 — the timeline

## 14 · Timeline (arrange · trim · preview · export)

**Purpose.** String the approved clips, trim, preview the loop, export — then finish in a real editor. Simple by design; explicitly **not** an NLE.

**Layout.** A preview player (dark stage) above a horizontal **clip strip** (Flow precedent): each clip a draggable card, trim handles on the ends, a `＋` to add. Transport controls. Export row: `GIF · WebM · MP4` with the two-pass GIF path. A quiet reminder that the real finish happens elsewhere.

**Interactions.** Drag to reorder, drag the ends to trim, scrub the player, export. No effects, no audio mixing, no keyframed transitions — those are out of scope by decision.

**States.** *Assembling:* "Stitching the loop…" *Ready:* the loop plays; export enabled. *Export:* "Rendered pencil-test-act2.gif."

**Endpoints.** `POST /runs/{id}/assemble`, `GET /runs/{id}/assemble` (sequence_file, gif, webm, mp4). Trim/reorder edits the sequence the assemble step reads.

**Microcopy.** "Assemble the loop." Export verbs name the format. "Engine truth: if the loop plays smoothly and he's still himself, it ships."

---

# Daemon contract — what the UI needs

v1's core (dashboard, overview, the plan/script/storyboard/animatic gates, the eye-gate's approve/retry) binds to the **CONVERGED daemon plan as-is** — read endpoints + the `202 {job_id}` gate actions + `next_action`. Four additive deltas, phased with the UI:

| # | Delta | Why | Phase |
|---|---|---|---|
| **D1** | `POST /runs/{id}/frames/{n}/retry` gains optional **`annotations`** `{ overlay, pins:[{x,y,text}] }` | Spatial direction — the red pen + pins forwarded to NB2 as an edit reference (how Flow's red pen + NB2 edits already work) | v1c |
| **D2** | **Brainstorm front-door surface** — run the chain, persist the session sidecar, store art-viz / reference images, emit the brief → `POST /runs` | The "① front door" the docs already frame as meeting the daemon "at the brief" | v1c |
| **D3** | **Chat / agent surface** — a message endpoint routing text to the active stage's agent + an intent→action map | The command bar drives all screens | v1c |
| **D4** | v2 stage endpoints — Cy `bible *` authoring jobs, `route` on the candidate payload, Motion job + critic | The per-stage visual pages | v2 |

None of these regress the read-only tracer-bullet or the byte-identical pipeline guarantee — they're all additive, driven as the same audited jobs the CLI runs.

---

# Build sequencing

Mapped to the daemon's own slice plan so the UI and backend advance together.

1. **v1a — the spine.** Dashboard + run overview, read-only, over `GET /runs` + `GET /runs/{id}/status`. Proves *daemon-reads-state → renders-screen* on a real run. (Daemon Slices 1–2.)
2. **v1b — the gates.** Plan / script / storyboard / animatic gates + the eye-gate (approve / retry, no annotation yet), over the artifact reads + the `202` job layer + POST gates. This is the working demo — the terminal is dead. (Daemon Slices 3–6.)
3. **v1c — the room + the pen.** Brainstorm front door (D2), the chat command bar (D3), the eye-gate annotation layer (D1). The differentiators that make it anima, not a Flow clone.
4. **v2 — the visual pages.** Character builder, storyboard board, generate grid, motion (D4), one Flow precedent at a time.
5. **v3 — the timeline.** Arrange / trim / preview / export.

The desktop shell (Electron/Tauri sidecar spawning the daemon) wraps this once v1b is proven; a recruiter can't click a link, but a screen-recorded walkthrough keeps the portfolio weight.

---

# Open questions (reserved, not blocking)

- **Annotation → NB2 form.** Overlay PNG vs binary mask vs pins-rendered-as-text-coordinates. Needs a one-frame spike against NB2's edit path before D1 locks.
- **Chat intent scope.** How much natural language drives gate actions vs. structured buttons. Start narrow (message the agent; explicit buttons for gate actions), widen with evidence.
- **Generate grid vs eye-gate default.** Does a run mid-generate open on the grid (survey) or the eye-gate (the current frame)? Lean: eye-gate on `review_frame`, grid on demand.
- **Brainstorm state model.** Pre-run workspace vs a `run_state` stage-0. Lean: pre-run workspace that emits the brief; the run begins at PLAN (matches the daemon's `POST /runs`).
- **Concurrency UX.** What the app shows when a background job owns a run and you navigate elsewhere (the 409 single-writer rule made visible).

---

# Microcopy library

The recurring strings, following the ux-writing standard: sentence case, verb-first, no "please" / "successfully", errors say what happened then the one fix.

| Context | String |
|---|---|
| New project | "Start a new short. Bring a spark and the room opens." |
| Dashboard card CTA | the specific next move ("F03 waiting on your eye →") |
| Brainstorm room | "the room — deepen, or proceed?" · "Emit brief → start run" |
| Plan gate | "Nothing burns compute until you approve." · "Approve plan" · "Send back" |
| Script toggle | "Read it like a script, or check the beats." · "Approve script" |
| Storyboard | "This gate is a curation: cut, reorder, then lock." · "Lock the board" |
| Storyboard invalid | "Beat 3 isn't boarded. Add a shot or the board won't lock." |
| Animatic | "You own timing." · "Ingest & generate" · "Skip animatic" |
| Eye-gate | "Your eye on F03." · "prefilled from Em" · verdict `pass · borderline · fail` |
| Eye-gate keys | "⏎ approve · R retry · mark with ✎ / ◉ · ↑↓ frames" |
| Retry toast | "Re-rolling F03. Note and annotations sent as a correction." |
| Working | "Flo is drawing F04…" · "Maya is costing the plan…" · "The crew is drafting." |
| Error | "Couldn't reach the model. Retry, or check the log." |
| Busy (409) | "This run is busy. View the running job." |
| Timeline | "Assemble the loop." · export verbs name the format |

---

*Ratified 2026-07-03. This spec and the prototype are the build inputs for the Flow-like interface; the daemon deltas above are the backend's phased asks. Update this doc in place when a decision changes, per the anima maintenance convention.*
