# Good-ART-VIZ rubric — the six-criterion live-review checklist

**This is a live human-review checklist for Sean — not a CI gate, not a
prose-grep, not a self-assessment. A model cannot self-pass it.** Every
criterion is a taste judgment; the honesty of this instrument is that it
stays in human hands. (The red-team cut every attempt to automate route
quality: a "≥3 route bullets each containing the mechanic word" lint passes
a flat route that name-drops "candy" and fails a superb route phrased
differently.)

Style-side companion to `good-expand-rubric.md` (the divergence-side
checklist) and `pinata-worked-example.md` (the convergence-side quality
bar). The worked positives throughout are the two live route sets: the
piñata concept doc's Routes A/B/C (Samurai-Jack faithful / Primal grit /
hybrid pencil-test) and the ai-guru pilot's Routes A/B/C (Ren & Stimpy
faithful / internet-neon hybrid / pencil-test fusion).

## The six criteria

A good ART-VIZ pass exhibits **all six**:

### 1. One fixed hero frame, ≥3 mutually-distinct registers
The routes hold the *composition* constant — one hero frame, the piece's
signature moment — and vary only the *rendering language*, so it is a true
look-to-look comparison. And the registers are mutually distinct
(anti-clustering), not one look reworded. *Judged by Sean, live.*
- **Worked positive:** the piñata's Samurai-Jack-faithful / Primal-grit /
  hybrid-pencil are three different rendering languages over one
  landing-pose frame ("Same composition, rendered in…"). The ai-guru set
  does the same over one Aiden-mid-glitch frame.
- **Anti-example:** three "Genndy-ish" routes that differ only in adjective;
  or three routes that also change the composition (nothing to compare).

### 2. The signature mechanic is never dropped — **the anima-specific bar**
Two honest shapes, and only these two:
- **When the hero frame IS the mechanic moment,** every route renders it —
  the ai-guru's frame is Aiden mid-glitch with Orby watching from the
  laptop; all three routes carry the distortion and the watching orb.
- **When the hero frame is a pre/post-mechanic beat,** the mechanic is
  explicitly captured in the concept doc's money-shot + timing-bible prose
  and carried into the Studio Brief non-negotiables — the piñata's routes
  render the *landing pose* (piñata intact behind him), with candy-as-oil
  locked in "The candy mechanic (the money shot)" section. The routes do
  **not** paint the geyser, and that is fine: the mechanic is captured, not
  lost.
- **Anti-example:** a route pass that renders the pose while the money-shot
  prose **omits** the candy-as-blood substitution entirely — the mechanic
  dropped, not relocated.

### 3. Each route is a self-contained, Flow-ready prompt
A named specific someone could paste into Flow and get the hero frame.
- **Worked positive:** the piñata's Route A is a complete pasteable prompt —
  subject, pose, camera angle, the no-black-outlines rule, background
  treatment, palette accent, letterbox, "No text, no watermark."
- **Anti-example:** "a Samurai-Jack-style route" — a category label with no
  renderable prompt.

### 4. The timing/craft bible is captured as prose
The piece's spine directives land in `concept.md` + the Studio Brief
non-negotiables.
- **Worked positive:** the piñata's 8 directives ("timing is a song";
  move → dead-stop HOLD → BURST; read in silhouette; no black outlines…)
  and the ai-guru's 8 (wet alive linework; one glitch fully committed; the
  ringmaster cadence; tonal whiplash, same register…), each with sources
  where the craft is borrowed.
- **Anti-example:** routes with no "timing is a song" / hold-then-burst
  discipline recorded anywhere — a look with no spine.

### 5. The personal-lineage route is present
Both runs offered a "fuse with anima's own pencil-test warmth" route — the
"most Sean" option. *Soft criterion — a taste default, not a hard bar; its
absence is a finding, not a block.*
- **Worked positive:** piñata Route C (Genndy × pencil-test: cream paper,
  visible construction lines, warm muted palette); ai-guru Route C
  (grotesque distortion over pencil-test texture, the orb kept glossy-clean
  in contrast).
- **Anti-example:** three routes that are all someone else's language, with
  no option that fuses the house lineage.

### 6. Un-buildable registers surfaced as `open_questions`
A register outside the six-register closed vocabulary is flagged (seed
`style_register` NEW-flag + the doctrine pointer,
`docs/architecture/prompt-style-neutrality-doctrine.md`), not waved
through. Flagging is ART-VIZ's whole job here — the doctrine 3-step
extension rides a real Cy authoring run, never this stage.
- **Worked positive:** the ai-guru run carried `90s-nicktoon-grossout` into
  both character seeds with the NEW flag and the doctrine pointer; the
  grandmaster run flagged Tartakovsky's flat-no-outline register the same
  way ([L14]).
- **Anti-example:** a photoreal route recommended with no word that anima
  has no photoreal register.

## Blocking rule

**Criteria 1, 2, and 3 block together.** A single "signature mechanic" bar
is gameable — three clustered, non-renderable, same-ish prompts can
name-drop the mechanic and pass — so the block requires all three: one
fixed hero frame in ≥3 genuinely distinct registers (1) + the mechanic not
dropped (2, the anima-specific core of the block) + each route a
self-contained, Flow-ready prompt (3). Still Sean's live judgment, not a CI
lint. Criteria 4–6 are findings to fold, at Sean's call.

## Live validation protocol (the Checkpoint-3 semantic gate)

Fable 5 builds to structural-green plus this protocol; **Sean runs the live
grill and renders on Flow.** The capture is his — a copied fixture cannot
stand in for it.

1. **Pick a piece with a live style question.** Either a fresh spark, or
   re-open the piñata / ai-guru route choice cold (ignore the recorded
   lean; re-derive the routes).
2. **Run the chain:** orchestrator → micro-expand → INTERROGATE → the
   inline ART-VIZ step (SKILL.md Step 2.5). No skill call, no render, no
   spend — the routes are prose; Sean runs them on Flow himself.
3. **Capture the artifacts:** the `### art-viz` sidecar block (options =
   the routes, recommendation = the lean, open_questions = any un-buildable
   register), the chosen-route LOCKED DECISION, and `stage_provenance`
   carrying `art-viz`.
4. **Score against the six criteria above.** All six judged, by Sean,
   against the captured transcript — not against the model's account of
   itself.
5. **Blocking rule:** a miss on the criterion 1+2+3 block — with **2 (the
   signature mechanic)** as its anima-specific core — blocks. Misses on
   4–6 are findings to fold, at Sean's call.

## Deferred: the style skill (the shape, named so it isn't lost)

The reusable per-look prompt library (`genndy-tartakovsky` first) is a
**Cy/generation-layer asset, deliberately not built by the front door.**
Its shape, when a greenlit piece needs it: the AKCodez scaffold — 2-second
hook → `[BRACKETED]` master template → timeline segmentation → domain
encyclopedia → worked examples. ART-VIZ captures the timing bible + money
shot as prose today; the style skill later *extracts* that prose into the
templated library. **The first real style skill rides the first greenlit
piece's Cy authoring run.**

## Appendix — the SPEND OK gate + Higgsfield render (deferred design, NOT built)

Specified so it is ready the day a greenlit piece and a shipped STRESS-TEST
verdict both exist. Not one line of it exists in Slice 3.

- **Trigger:** only after ART-VIZ has proposed routes AND the STRESS-TEST
  `stress_verdict` is `proceed` AND Sean types the exact phrase
  `SPEND OK: Higgsfield <model> <count> <max-credits>`.
- **Behavior:** emit a cost estimate first; refuse to call `generate_image`
  without the phrase; on the phrase, render the chosen route's hero frame
  via the Higgsfield MCP; write the render into the chosen seed's
  `anchor_ref` / `style_ref_ids`.
- **CI:** never exercised — no live MCP in tests (fleet-ops). Built in a
  later slice **co-built with the stress-verdict consumer**, not before.
