# Cy the Character Designer — Phase 2 Brainstorm

**Date:** 2026-05-27
**Workstream:** Commit 2 — Character Bible migration + Cy persona (gating the `characters/{character_id}/` schema, the `character.yaml` shape, the Bible-authoring workflow, Cy's three-phase loop, the identity-rules emission contract, and Cy's connection to Em's downstream verification).
**Skill invoked:** `pm-product-discovery:brainstorm-ideas-existing` — multi-perspective product trio (PM + Designer + Engineer), 5 ideas per perspective, anti-bias rotation pass, converge on top 5. Mirrors the Maya brainstorm structure verbatim.
**Grounded in:** [`PHILOSOPHY.md`](../PHILOSOPHY.md) (the human owns taste; the critic earns its keep by proposing fixes; iteration must be cheap; read like a studio), [`docs/2026-05-26-agent-fleet-brainstorm-v2.md`](2026-05-26-agent-fleet-brainstorm-v2.md) §2.1 (Cy as the missed pinnacle phase), §6 (per-role table — Cy at 92% confidence, the highest non-Chairman assignment), §11 (Phase 2 wiring in the architecture-implied strawman), [`docs/research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md`](research/2026-05-26-orchestrator-and-judge-delegation-SYNTHESIS.md) §5 (verbatim: *"validators cannot recover taste that was absent at generation time"* — the single decision Sean was about to get wrong if he shipped v1), [`docs/Image-Model-DR-2026/SYNTHESIS.md`](Image-Model-DR-2026/SYNTHESIS.md) §2 (NB Pro for hero shots — Cy's generation tier), [`docs/pipeline-architecture-v1.md`](pipeline-architecture-v1.md) Phase 2 spec, [`docs/2026-05-24-pipeline-v2-change-map.md`](2026-05-24-pipeline-v2-change-map.md) §2 TOP-5 (the original folder-shape sketch) + §4 (commit 2 in the sequence), and the Cowork pre-brainstorm session that resolved three structural splits: Cy-leads-Sean-reviews, commit 2 ships both author + consume Project-Types, and the legacy anchor path keeps a symlink through commit 7.
**Status:** Brainstorm complete. Five ideas locked for commit 2 + commit 2b implementation. Nine ideas deferred with explicit promotion triggers. The Bible contract is concrete enough to write code against, the schema is grounded in actual on-disk material rather than the v1 speculation, and Cy's connection to Em's downstream verification is named.

---

## 1. The Cy role, in one paragraph

Cy is anima's character designer. She reads the Studio Brief and any source reference material — Sean's hand-drawn anchor, his pose references, his pixel-art mascot — and authors the Character Bible: the cross-phase invariant every Phase 5 frame and every Phase 6 motion shot is implicitly judged against. She emits a `characters/{character_id}/` folder containing the anchor, turnaround plates, expression sheets, motion plates, costumes, props, and a `character.yaml` that names the identity rules in language Em can cite at T2-critic time. She generates the visual plates via Nano Banana Pro per Flo's Phase 5 routing, then verifies the generated plates against the identity rules via Gemini 3.1 Pro through the same `agy` wrapper Em uses. Three of four LLM council members converged on Cy as the most under-recognized Opus seat — the headline finding of the v2 synthesis. A Sonnet-authored Bible looks complete and silently fails to constrain, which is what the synthesis means by *"validators cannot recover taste that was absent at generation time."* Cy is where taste enters the contract layer at the earliest possible upstream point.

What's locked already:
- Cy's persona name and model assignment (v2 §6, confidence 92% — *not for redecision*).
- Cy authors with Opus 4.7, visually verifies with Gemini 3.1 Pro, generates plates with Nano Banana Pro per Flo's routing table.
- Cy-leads-Sean-reviews is the workflow shape (Cowork preamble decision).
- Commit 2 ships both author and consume Project-Types from day one (Cowork preamble decision, resolves v2 Open Q6).
- The legacy `images/2D-Character-Sketch-Sean-v1.png` keeps a symlink through commit 7 (Cowork preamble decision).
- Cy's identity rules must be machine-readable in a shape Em can cite by ID at T2-critic time (v2 §2.3 Pattern B — Planner-Chairman shared rubric, applied here at the Bible layer).

What this brainstorm decides:
- The `characters/{character_id}/` folder structure — what the v1 sketch missed once Sean's actual material is on the table.
- The `character.yaml` schema — closed vocabularies for style register, palette, proportions, identity-drift triggers.
- Cy's three-phase loop shape — how the Opus-authors + Gemini-verifies contract executes inside a single AgentSpec.
- The `identity_rules.json` emission contract — flat sidecar vs criteria-graph extension.
- The Bible-authoring brief connection — Maya's `00_studio_brief.md` vs a separate `02_character_brief.md`.
- The CLI surface — `pipeline bible init / show / approve / mutate` parity with Maya's plan commands.

The product trio frame: Sean (PM) + Sean (Designer) + Sean (Engineer) + Claude. Three independent reads of the problem, then convergence.

---

## 2. PM Perspective — Strategic alignment, portfolio leverage, downstream cascade

The Cy brief from a product-management lens is *"how do we make Bible authoring the structural fix at the source for every taste-failure mode downstream."* Every PM idea below targets a specific cascade from synthesis §5 — the Bible's blast radius across the pipeline.

**PM1. The Bible has two readers, and Cy authors for both.** The `characters/{character_id}/` folder ships two kinds of artifact: visual plates that humans read (anchor, turnarounds, expressions, motion plates) and structured rules that agents read (`character.yaml`, `identity_rules.json`). Cy authors both passes in one loop — the visual plates first, then the structured rules derived from them with explicit pointers back to the plate that anchored each rule. The two-reader split mirrors Maya's two-tier-brief separation (Sean reads prose, the orchestrator reads structured fields). It prevents the failure mode where the visual library looks complete but no downstream agent can articulate *which plate enforces what* — a failure mode that's especially insidious because it's invisible until Em cites a generic rule at T2-critic time and the chairman can't trace the rule back to a plate.

**PM2. Identity-rule impact tags travel with the rule through every downstream consumer.** Each entry in `identity_rules.json` carries an `impact_tag` from the same closed vocabulary Maya's criteria use — `hero | identity_critical | continuity | aesthetic | structural`. Em already keys its escalation hatch off impact tag (commit 8's `_DEFAULT_ESCALATION_TAGS`). Cy's identity rules become first-class citizens in that escalation ladder: when Em sees a borderline frame on `sean-anchor`, the impact tag of the rule it's citing routes the verdict to Opus escalation or Sonnet default automatically. The taste signal travels with the rule, end to end, from Bible authoring through Phase 5 generation through Phase 8 assembly. This is v2 Pattern B (Planner-Chairman shared rubric) extended one layer up: Bible rules become the rubric for character continuity the same way Maya's acceptance criteria become the rubric for spec continuity.

**PM3. Cy emits a `risk-bible.md` alongside the Bible — what this character can't do.** Mirrors Maya's `risks-if-rejected.md` (deferred in the Maya brainstorm but explicitly named). The Bible's negative space — the poses Sean's anchor can't anchor, the expressions the reference doesn't cover, the motion plates that are missing for downstream Seedance work — is just as load-bearing as the positive space. When Em flags a Phase 5 frame as identity drift, the chairman can read the risk-bible to see whether the drift is on a covered axis (real failure) or an uncovered one (the Bible never claimed to lock this — escalate to Sean for a new plate). The risk-bible is also portfolio content: it shows the Bible was authored with deliberate scope, not a hopeful guess at completeness.

**PM4. Cy's first job is to migrate the pencil-test anchor; commit 2 ships against a real character.** Not a hypothetical multi-character abstraction — commit 2 stands up `characters/sean-anchor/` from the material already on disk and proves the schema against Act 1's existing approved frames. Then Cy authors `characters/claude-mascot/` as the second-character validation case (the pixel-art mascot already exists in `images/Claude-Mascot/`) — different aesthetic register, different palette vocabulary, same Bible schema. Two characters on day one means the schema gets pressure-tested against actual diversity rather than authored against the pencil-test single-case bias. The pixel-art Claude mascot is the structural proof that style itself is a Bible-level attribute, not a downstream prompt detail.

**PM5. Bible authoring is a Project-Type, and Maya routes to it.** The Cowork preamble resolved v2 Open Q6 in favor of both Project-Types day one. Maya's `01_production_brief.md` adds a `project_type: bible_authoring | animation_piece` field. When `bible_authoring` is the type, Maya's plan skips Phases 3-9 and ships a Bible-authoring run that consists of Phase 0 (Maya plans the Bible) → Phase 2 (Cy authors) → human-approval gate. The Bible IS the deliverable. This is the structural fix at the source synthesis §5 names — taste enters the system at the earliest possible upstream point, not as a Phase 5 recovery operation. Bonus: it makes Bible-authoring a first-class anima output, which means a finished Bible IS a museum walkthrough — Cy's process becomes portfolio content the same way a finished short does.

---

## 3. Designer Perspective — How the Bible reads, how the workflow feels

The Cy brief from a design lens is *"how does the studio-manual voice live in a Bible artifact, and how does the authoring loop feel as fast as Sean's actual drawing hand."* Every Designer idea targets the philosophy §6 "read like a studio" directive applied to character-design ceremony.

**DES1. The Bible is a tear sheet, not a JSON dump — same rendering split as Maya.** `pipeline bible show characters/sean-anchor/` is a Python rendering layer that reads the clean markdown + image files on disk and paints a terminal tear sheet — character header, anchor thumbnail (ASCII art or path), palette swatch line, identity rules grouped by category with their plate references, motion-plate inventory, costume + prop checklist. The file system on disk stays prose and JSON and PNG — no boxes baked into the artifact. Downstream consumers (Em, Flo, Maya, the museum writer) read the clean files; Sean reviews via the tear sheet. The rendering separation is the structural pattern from Maya TOP-4 applied to the Bible. Zero Opus tokens spent on box-drawing. The portfolio thesis (the work is readable; the process is visible) survives because the Bible reads like a character bible from a real animation studio, not a config file.

**DES2. Identity rule IDs are mnemonic, mirroring Maya's AC IDs.** Not `IR01, IR02, IR03` but `IR.sean.hair.center-cowlick`, `IR.sean.proportion.head-to-body-1-to-7`, `IR.sean.stylus.right-hand-always`, `IR.claude-mascot.palette.pixel-orange-#E89B6B`. The pattern is `IR.{character_id}.{category}.{specific-handle}` with category drawn from a short closed vocabulary (`anatomy / hair / face / proportion / palette / costume / prop / pose / motion / style`). When Em cites `IR.sean.stylus.right-hand-always` in a borderline verdict, Sean reads "the stylus drifted to the left hand on frame F23" in plain English, no cross-reference. The Bible's structured rules become as readable as Maya's acceptance criteria — a single visual idiom across the whole agent fleet.

**DES3. The brief stays singular — Cy reads Maya's Studio Brief, no `02_character_brief.md`.** Two-tier brief stays at two tiers, not three. The Studio Brief's seven prompts already include `character` as a structural field; Cy's role is to read what's there and ask Sean for the missing structural inputs through `pipeline bible init`, not to demand a third file. Cy's `init` command scaffolds a `characters/{character_id}/source-refs/` directory and a `0-sean-author-this.md` checklist (drop your anchor here; drop your turnaround here; if you have motion refs, drop them here; if you have a 3D mannequin pose ref, drop it here) — single-shot. The blank-page tax that kills authoring velocity gets paid by the scaffold. Mirrors the same DES5 pattern from the Maya brainstorm — opinionated defaults that the user can edit but doesn't have to author from scratch.

**DES4. Cy's confidence notes ship inside `character.yaml` as a top-level field.** Each Bible entry has a `cy_confidence_notes:` section with prose where Cy hedged — which plate is interpretive (the back angle of the head-turn was extrapolated; the 3-quarter back is a guess), which identity rule she couldn't fully resolve from the references (Sean's stylus hand is locked in the anchor but the head-turn doesn't show it), which motion plate ranges are inferred (the walk cycle covers neutral; turns and runs aren't covered by the source refs). Visible-confidence is the studio-manual voice (philosophy §6) applied to Cy's own self-awareness — same pattern Maya uses, same downstream value (the chairman and Sean both read these when arbitrating Em's verdicts). When a confidence note flags a hedge, that's the Bible itself telling downstream consumers to escalate rather than trust.

**DES5. The authoring loop has a `cy iterate` command that re-runs only the bits that changed.** When Sean rejects three of Cy's generated expression-sheet plates, `pipeline bible iterate characters/sean-anchor/ --target expressions --reject angry,surprised,concerned --reason "registers too cartoonish — pull back to subtle"` re-runs only those plates with the reject reason threaded into the regeneration prompt. Cache the plates that passed; never regenerate them. The draft → pro principle from philosophy §3 applied to Bible authoring — iteration must be cheap because Cy's plates are expensive. NB Pro at ~$0.15/plate × 20-30 generations is a $3-5 Bible; re-running everything when Sean rejects three plates is wasteful. Per-plate caching with reject-aware regeneration keeps the iteration loop at the speed Sean's drawing hand expects.

---

## 4. Engineer Perspective — Contract layer, schema, the AgentSpec shape

The Cy brief from an engineering lens is *"how does the Bible contract look such that every downstream consumer reads from it without needing to know about it."* Every Engineer idea targets the typed-Protocol shape from commit 4's `AgentSpec` and the criteria-graph extension from commit 3's `pipeline/criteria.py`.

**ENG1. The folder schema grows a sixth category — `motion_plates/` — and a cross-cutting `source/` vs `derived/` split.** The v1 change-map sketched `anchor / turnarounds / expressions / costumes / props`. Sean's actual on-disk material proves the v1 sketch missed motion plates: the 9-frame head turn and the 9-frame walk cycle are neither expressions nor turnarounds — they are *motion library plates*. The proposed folder shape:

```
characters/{character_id}/
├── character.yaml                # palette, proportions, style register, identity-rule pointers
├── identity_rules.json           # machine-readable rules, queryable by category/impact-tag
├── risk-bible.md                 # negative-space inventory (PM3)
├── cy-confidence-notes.md        # hedges + interpretive calls (DES4)
├── anchor.png                    # the single canonical identity reference
├── turnarounds/                  # front, 3-quarter, profile, back (body + head separate)
│   ├── body-front.png
│   ├── body-3quarter.png
│   ├── body-profile-right.png
│   ├── body-back.png
│   ├── head-front.png
│   ├── head-3quarter.png
│   └── head-profile.png
├── expressions/                  # 8-12 emotional states, named
├── motion_plates/                # NEW — motion library, the v1 sketch's missing category
│   ├── walk-cycle/
│   │   ├── source/               # raw line-art (Sean's Original-Walk-Cycle.png)
│   │   └── derived/              # rendered/finished plates (sean-walk-cycle.png)
│   ├── head-turn/
│   │   ├── source/
│   │   └── derived/
│   └── (run-cycle/, idle/, gesture-set/ as needed)
├── costumes/{variant}/           # outfit variations (current: default tee + jeans)
├── props/                        # key prop attachments (the stylus)
└── source-refs/                  # Sean-authored input refs Cy consumed during authoring
    ├── 3d-mannequin/             # the Sprite-reference + 3D-Character-Reference-Test material
    └── notes.md                  # Sean's voice notes / sketches / mood
```

Source vs derived inside motion_plates is the cross-cutting split: Em compares Phase 5 frames against `derived/` (visual verification); Flo (when motion in-betweener tooling matures) generates against `source/` (pose construction). Both stay versioned in the Bible.

**ENG2. `identity_rules.json` is a graph that EXTENDS `acceptance_criteria.json`, not a separate sidecar.** Cy's rules emit as `AC.identity.*` and `AC.proportion.*` entries into the same graph Maya emits. The brainstorm considered a separate `identity_rules.json` (parallel structure), but folding into the same graph wins on three counts: (a) Em already cites criteria by ID at T2-critic time — making Bible rules first-class criteria means zero new wiring; (b) the chairman's synthesis already reads the criteria graph — Bible rules surface in disputes without a new code path; (c) `git blame` on a criterion answers "when did this rule get added, and by which Bible iteration" — one provenance trail instead of two. The schema extension: Cy's criteria carry an extra `character_id` field and `derived_from` pointer back to the plate that anchored the rule (`characters/sean-anchor/turnarounds/body-front.png#region:hair`). Mnemonic IDs use the `IR.{character_id}.*` namespace inside the broader `AC.*` graph — categorically isolated, structurally unified.

**ENG3. Cy is an AgentSpec with the same three-phase shape as Maya — Opus authors, Gemini verifies, resolution.** Maya's three-phase loop (Opus primary → Sonnet adversarial validation → resolution) is the structural template. Cy's three-phase loop:

- **Pass 1 — Opus authors.** Reads Studio Brief + Cy role addendum + the source-refs directory; emits the `character.yaml`, the `identity_rules.json` graph (as `AC.identity.*` entries), the `risk-bible.md`, the `cy-confidence-notes.md`, AND a structured generation plan naming each plate to be generated by NB Pro with per-plate prompts grounded in the identity rules. Opus does the taste work; NB Pro does the generation; Opus never writes pixels.
- **Pass 2 — NB Pro generates plates from Opus's plan.** Each plate generation cites the identity rules it must satisfy in its prompt (the same `IR.*` IDs Opus authored). One plate at a time, content-addressed cached by (rule-set + reference-images + prompt-text). The DES5 `cy iterate` command operates over this cache.
- **Pass 3 — Gemini 3.1 Pro visually verifies every plate against the rules it cites.** Same `agy` wrapper Em uses (commit 8.1a's `--dangerously-skip-permissions --add-dir <parent> -p ...` incantation). For each generated plate, Gemini emits `{verdict: pass|borderline|fail, reasoning, confidence, cites_identity_rule: [...]}` — mirroring Em's contract exactly. Plates that fail get re-generated with the failure reasoning threaded into the next prompt; ceiling of three attempts per plate before the human gate fires.

Three-call ceiling per plate (matching Maya's three-call ceiling per plan). The Opus call happens once per Bible; the Gemini calls happen N times where N = plate count. Total Cy run cost: ~$3-5 in NB Pro + zero incremental on Opus + Gemini (subscription-absorbed). v2 §7's cost ceiling holds.

**ENG4. Bible mutation uses the same `--force --actor --reason` audited contract as Maya's plan mutation.** `pipeline bible mutate --force --actor sean --reason "Em flagged IR.sean.hair.center-cowlick drift on F23, tighten tolerance" --target IR.sean.hair.center-cowlick --field tolerance --value 0.08 --character-dir characters/sean-anchor/`. Writes one line to `runs/{run_id}/bible_audit.jsonl` mirroring `plan_audit.jsonl`. Semver-bumps the `identity_rules.json` (or the section of `acceptance_criteria.json` Cy authored). Re-emits the affected plates if the mutation changes a generation rule. The audit pattern is identical to Maya's commit 3 mutation contract — Sean already knows the muscle memory; one ceremony works across Maya and Cy. Museum surfaces the bible-audit log as portfolio content the same way it surfaces the plan-audit log — "here are the four character-rule mutations during this production, and why each one happened."

**ENG5. Cy's role addendum loads the `2d-animation-principles` skill verbatim into her standing context.** The skill is already installed (in the available-skills list). Cy's `cy-character-designer-context.md` standing-context preamble reads the skill's SKILL.md as an inline appendix — the way the existing `maya-planner-context.md` reads the anima standing context. Why: the `references/visual-guides/` folder shows Sean's working vocabulary for character motion is animation-principle-grounded (arc paths, line of action, squash-and-stretch, eye-lead-head-turn, smear-dry-brush, spacing-odd-rule, twinning-detection). The 2D animation principles skill is already calibrated against that vocabulary. Cy reasons in that language when authoring identity rules and motion plates, and her output is more useful to Em (who also speaks it) than if she invented her own vocabulary. The references/visual-guides/ folder doesn't move into `characters/` — it stays as cross-character craft reference — but Cy reads it through the skill.

---

## 5. Anti-Bias Rotation Pass — What each role's prior suppressed

Per the brainstorm skill protocol, after the initial fifteen ideas, re-read with each role's prior off and ask what the other roles would notice. The rotation surfaces ideas that fall between role lenses.

**ROT1 (Engineer thinking with a PM hat). Cy's first run produces a `bible-walkthrough.md` that's portfolio content from day one.** Alongside the Bible artifacts, Cy emits a prose walkthrough of *how the Bible was authored* — which source refs anchored which identity rules, which plates Gemini flagged on the first pass and what the regeneration prompt looked like, which rules Cy hedged on and why. The walkthrough is the museum content for the Bible-authoring run before the museum capture layer (commit 6) ships. The synthesis §8 portfolio-positioning angle (anima as early practitioner of provider-diverse evaluation councils for solo creative production) needs *visible artifacts of the authoring process* — `bible-walkthrough.md` is that artifact for the Bible layer specifically. It's also the structural answer to "the Bible looks complete but I can't trace its decisions" — the walkthrough IS the decision trail.

**ROT2 (Designer thinking with an Engineer hat). The `character.yaml` style register field is closed-vocabulary and load-bearing.** `style_register: pencil-test-colored | pixel-art-8bit | line-art-only | watercolor | photoreal | 3d-rendered` (extend as anima ships more characters). Style register is a top-level character attribute, not a per-plate prompt detail. Em's verification prompt loads the rules for the character's style register *before* it loads the identity rules — pixel-art-8bit Claude mascot drift is a categorically different failure mode from pencil-test-colored Sean drift. Flo's Phase 5 routing reads the style register to pick the right model (pencil-test-colored → NB Pro per the routing table; pixel-art-8bit → potentially a different route entirely). The Claude-Mascot folder is the structural proof — it would have been routed wrong if style register had been a downstream prompt detail rather than a Bible attribute.

**ROT3 (PM thinking with a Designer hat). The `cy-confidence-notes.md` for Sean has a counterpart for Em — `em-citation-cheatsheet.md`.** A separate Cy-authored artifact in the Bible that names the *expected ways* downstream Em verdicts should cite rules. "When evaluating a Phase 5 hero shot of Sean on `characters/sean-anchor/`, the load-bearing rules to cite by ID are: `IR.sean.hair.center-cowlick`, `IR.sean.proportion.head-to-body-1-to-7`, `IR.sean.stylus.right-hand-always`, `IR.sean.face.eye-spacing-1.5x-eye-width`." The cheatsheet doesn't change Em's prompt — it pre-decides which rules are load-bearing for which kind of shot. Two effects: (a) Em's verdicts get more consistent because the rule-citation surface is curated; (b) the cheatsheet becomes the surface where Cy reasons about *what kinds of shots this character is built for*. Subordinate to PM3's risk-bible — if both ship, they're sibling files in the Bible.

**ROT4 (Engineer thinking with a Designer hat). The Bible has a "style anchor LoRA seed" field, even if no LoRA exists yet.** `character.yaml` has a `flux_lora_seed_plates: [anchor.png, body-front.png, head-front.png, expressions/neutral.png, ...]` field that names which plates would seed a custom character LoRA if Sean ever trains one (per Image-Model-DR SYNTHESIS §3 Config C). The field is informational on day one — no LoRA training happens in commit 2 — but it makes the Bible LoRA-ready by construction. When Sean does train a LoRA (Image-Model-DR Experiment 1, one Sunday afternoon, ~3hrs), the seed list IS the training set. The Bible thus structurally anticipates the Phase 5 self-hosted route without committing to it. Forward-leaning, low-cost, optional.

**ROT5 (Designer thinking with a PM hat). Bible-authoring runs emit a "before/after Sean" comparison strip.** When Cy migrates Sean's hand-drawn anchor into `characters/sean-anchor/`, the run produces a side-by-side strip of Sean's source refs (left) and Cy's generated plates (right) at every category — turnarounds, expressions, motion plates. The strip is auto-rendered to `characters/sean-anchor/comparison-strip.png` (Pillow + matplotlib, same stack as Maya's optional cost-preview render). Two effects: (a) Sean reviews the Bible visually in seconds (the strip is the at-a-glance approval surface); (b) the strip is portfolio content — "here's what I drew, here's what Cy authored from it, here's what NB Pro generated from her plan, here's what Gemini verified." The provenance trail becomes a visual artifact. Subordinate to ROT1's walkthrough — if both ship, the strip is the visual companion to the prose.

---

## 6. Converged Top 5 — What Commit 2 Builds

Twenty ideas surfaced. Five converged. The selection criteria, in priority order: (a) structural alignment with v2 §2.1 (Bible as cross-phase invariant) and §2.3 (Pattern B — shared rubric), (b) impact on synthesis §5 (taste at generation time), (c) studio-manual readability (philosophy §6), (d) feasibility for commit 2 + commit 2b (the change-map's M-effort estimate stays honest), (e) portfolio-museum value. The ideas below are written as commit-ready specifications.

### TOP-1 — Folder schema with motion_plates/ and source/derived/ split (ENG1 + ROT2)

**What ships.** The `characters/{character_id}/` folder shape exactly as ENG1 sketched, with style register folded in as a top-level field. The v1 change-map's anchor/turnarounds/expressions/costumes/props sketch becomes anchor/turnarounds/expressions/**motion_plates**/costumes/props/source-refs — six plate categories plus a sources directory. Motion plates carry source/derived sub-folders to preserve both the construction line-art and the rendered plate. `character.yaml` carries `style_register` (closed vocabulary) as a top-level field that Em loads *before* identity rules and Flo reads when routing Phase 5 generation.

**Why it was selected.** Sean's actual on-disk material — `images/NEW-ANIMATION-PIPELINE/sean-head-turn-1.png`, `sean-walk-cycle.png`, `Original-Headturn.png`, `Original-Walk-Cycle.png`, plus the pixel-art `images/Claude-Mascot/` — proved the v1 sketch was incomplete in two structural ways. Motion plates don't fit anchor/turnarounds/expressions; the v1 schema would have forced Sean to file the walk cycle into the wrong drawer. And the pixel-art Claude mascot proved style register is a Bible-level attribute, not a prompt detail — without it, Flo's Phase 5 routing would silently route the mascot to NB Pro (the pencil-test default) and produce a categorically wrong output. The folder schema is the structural fix at the contract layer, and the on-disk material is the receipt that proves it's needed.

**Key assumptions to validate.**
- Motion plates' source/derived split serves both Em (verification reads derived) and Flo (motion generation reads source) without ambiguity. (Validated by writing real Em verdicts against `sean-anchor/motion_plates/walk-cycle/derived/` in commit 2b.)
- The closed style-register vocabulary covers Sean's anticipated characters without forcing a third extension cycle. (Plausible — pencil-test-colored, pixel-art-8bit, line-art-only, watercolor, photoreal, 3d-rendered covers the styles Sean's working in or has gestured at.)
- The `source-refs/` directory pattern lets Sean drop arbitrary input refs without a strict schema. (Plausible — `source-refs/` is intentionally loosely-typed; the only typed sub-folder is `3d-mannequin/` for the existing Sprite-reference + 3D-Character-Reference-Test material.)

### TOP-2 — Identity rules extend `acceptance_criteria.json` with IR.* namespace and impact tags (ENG2 + PM2 + DES2 merged)

**What ships.** Cy's identity rules emit as entries in the same `acceptance_criteria.json` graph Maya emits. Mnemonic IDs follow `IR.{character_id}.{category}.{specific-handle}` — `IR.sean.hair.center-cowlick`, `IR.sean.proportion.head-to-body-1-to-7`, `IR.sean.stylus.right-hand-always`, `IR.claude-mascot.palette.pixel-orange-#E89B6B`. Category vocabulary is closed: `anatomy / hair / face / proportion / palette / costume / prop / pose / motion / style`. Each entry carries the existing v1.1 graph fields (`cites_phase`, `cites_personas`, `impact_tag`, `parent_id`) plus two new Cy-specific fields: `character_id` (the `{character_id}` from the folder) and `derived_from` extended to point at a specific plate region (`characters/sean-anchor/turnarounds/body-front.png#region:hair`). Impact tags from the same closed vocabulary Maya uses; Em's existing `_DEFAULT_ESCALATION_TAGS` from commit 8 fires unchanged when Cy's rules carry `hero` or `identity_critical`.

**Why it was selected.** This is v2 Pattern B applied at the Bible layer. The synthesis §1.3 named `acceptance_criteria.json` as the structural fix for local-optimization drift; folding identity rules into the same graph means *the Bible IS part of the rubric*, not a parallel rulebook. Em already cites criteria by ID at T2-critic time — zero new code path for Em to consume Cy's rules. The chairman's dispute resolution already reads the criteria graph — Bible rules surface in T3 disputes without a new code path. `git blame` on a criterion answers "when did this rule get added, and by which Bible iteration" — single provenance trail. Impact tags routing to Em's escalation hatch closes the loop synthesis §5 demands: the taste signal travels with the rule from authoring through Phase 5 through Phase 8.

**Key assumptions to validate.**
- The `AC.identity.*` namespace inside the broader `AC.*` graph stays readable when 200+ entries exist across a multi-character piece. (Plausible — same readability argument as Maya's mnemonic IDs; tested by writing real criteria for `sean-anchor` + `claude-mascot` in commit 2.)
- Em's prompt can be tightened to cite both spec criteria (Maya's) and identity criteria (Cy's) in the same verdict without confusion. (Validated by the commit 2b eval suite — closing-the-loop test below.)
- `derived_from` pointing at plate regions (`#region:hair`) stays useful when Em can't address regions directly. (Plausible — Gemini 3.1 Pro reads the whole plate; the region pointer is for human review and museum surfacing, not for the model's grounding.)

### TOP-3 — Cy as three-phase AgentSpec mirroring Maya: Opus authors → NB Pro generates → Gemini verifies (ENG3)

**What ships.** A new `pipeline/agents/character_designer.py` registered as `@register_node("character_designer")`. Three-phase `run()`:

1. **Pass 1 — Opus authors.** Reads Studio Brief + `cy-character-designer-context.md` standing-context + the `source-refs/` directory contents. Emits `character.yaml`, the `AC.identity.*` and `AC.proportion.*` graph entries, `risk-bible.md`, `cy-confidence-notes.md`, and a structured generation plan naming each plate to be generated with per-plate prompts that cite the identity rules they must satisfy.
2. **Pass 2 — NB Pro generates plates per Opus's plan.** Per-plate generation via Flo's NB Pro route, content-addressed cached by (rule-set + reference-images + prompt-text). One plate at a time; Cy never generates plates in a single batch call because the prompt for each plate cites different rules.
3. **Pass 3 — Gemini 3.1 Pro verifies every plate.** Same `agy` wrapper Em uses (`--dangerously-skip-permissions --add-dir <parent> -p ...`). Verdict envelope mirrors Em's: `{verdict, reasoning, confidence, cites_identity_rule}`. Failed plates regenerate with the failure reasoning threaded in; three-attempt ceiling per plate.

The Pass-1 Opus call is the load-bearing taste call (the one §5 names). Pass 2's NB Pro calls are deterministic generation. Pass 3's Gemini calls are the verification half that closes the loop. Total Cy run: ~$3-5 in NB Pro + zero incremental on Opus + Gemini. Wall time: dominated by Gemini's 11-27s per plate × ~20-30 plates = 4-13 minutes (within v2 §7's `wall_budget_s: 600` per call but the full Bible authoring is more like a wall-budget-per-Bible question).

**Why it was selected.** Three-phase mirroring Maya means commit 2's implementation lifts patterns directly from commit 3's planner.py — Sean's existing muscle memory carries over, the prompt-iteration discipline carries over, the stub-fallback ladder carries over, the test fixtures carry over. Em's verification contract gets reused for Pass 3 without modification. NB Pro's hero-tier routing per Image-Model-DR SYNTHESIS §2 lands in production as Cy's default — the routing decision shows up as a real artifact, not a hypothetical config. The three-phase shape is also the structural answer to "how do Opus + NB Pro + Gemini collaborate on Bible authoring" — Opus does taste, NB Pro does pixels, Gemini does verification, no agent does work it's wrong for.

**Key assumptions to validate.**
- Opus's Pass-1 plan is structured enough that Pass 2's per-plate generation is mechanical. (Plausible per Maya's structured-output discipline; validated by the commit 2b eval suite.)
- Three attempts per plate is enough for Gemini-flagged regenerations to converge. (Plausible — Em currently runs zero-regeneration; Cy's regeneration loop is similar to Maya's three-call ceiling and held to the same shape.)
- NB Pro's content-addressed cache key (rule-set + reference-images + prompt-text) is stable enough that `cy iterate` regenerations don't accidentally re-run cached plates. (Validated by writing a unit test against the cache hash function in commit 2.)

### TOP-4 — `pipeline bible init / show / approve / mutate / iterate` CLI mirrors Maya's plan CLI (DES1 + DES3 + DES5 + ENG4 merged)

**What ships.** Five subcommands under `pipeline bible`:

- **`init characters/{character_id}/`** — scaffolds the folder structure (per TOP-1) plus a `source-refs/0-sean-author-this.md` checklist asking Sean to drop his source refs. Idempotent.
- **`show characters/{character_id}/`** — Python rendering layer. Reads the clean markdown + JSON + image paths on disk and paints a tear sheet: character header, anchor thumbnail (path + ASCII representation), palette swatch line, identity rules grouped by category with their plate refs, motion-plate inventory, costume + prop checklist, risk-bible callouts, cy-confidence hedges. **The boxes live in the renderer, never on disk** — same separation as Maya's `plan show`.
- **`approve characters/{character_id}/`** — resolves the identity-rules section in `acceptance_criteria.json` and sets `criteria_locked: true` for the `IR.{character_id}.*` namespace. Atomic, idempotent.
- **`mutate --force --actor sean --reason "..." --target IR.sean.hair.center-cowlick --field tolerance --value 0.08 --character-dir characters/sean-anchor/`** — refuses without `--force` + `--actor` + `--reason`. Writes to `runs/{run_id}/bible_audit.jsonl` mirroring Maya's `plan_audit.jsonl`. Semver-bumps the rules file.
- **`iterate characters/{character_id}/ --target expressions --reject angry,surprised --reason "registers too cartoonish"`** — re-runs only the named plates with the reject reason threaded into the regeneration prompt. Cached plates that passed are preserved. The iteration loop runs at the speed of Sean's drawing hand.

**Why it was selected.** Sean already knows Maya's CLI muscle memory — `init / show / approve / mutate` works the same way for Bibles. Adding `iterate` is the one Cy-specific extension because Cy generates plates while Maya only emits prose + JSON. The renderer-as-separation pattern (DES1) keeps the Bible files clean for downstream consumers (Em, Flo, museum writer) while letting Sean read a studio-grade tear sheet. The audit contract reuses commit 4's `criteria_locked` enforcement and commit 3's mutation audit pattern — one ceremony across the whole agent fleet, one shape for the museum to surface ("here are the mutations during this production").

**Key assumptions to validate.**
- The tear-sheet rendering covers the dimensions Sean wants to review at a glance (turnarounds, motion plates, rules grouped by category, palette, risks). (Will be tuned during commit 2 implementation; the first three real Bible reviews calibrate.)
- The `iterate` command's reject-aware regeneration prompt is robust enough to actually change the output. (Validated in commit 2b's eval suite — one case ships intentionally red on a first-pass reject that should converge by the second attempt.)
- The mutation surface is small enough that Sean doesn't reach for "just edit the YAML by hand." (Same assumption as Maya's TOP-4 mutation; same answer if it holds for Maya.)

### TOP-5 — Bible-authoring as a Maya Project-Type with the Closing-the-Loop Em check (PM5 + commit 2b)

**What ships.** Maya's `01_production_brief.md` template gains a `project_type: bible_authoring | animation_piece` YAML frontmatter field. When `bible_authoring` is the type, Maya's plan structurally skips Phases 3-9 and ships a Bible-authoring run: Phase 0 (Maya plans the Bible) → Phase 2 (Cy authors) → human approval gate. The Bible IS the deliverable. Sean can ship a Bible-authoring run independently of any animation piece; the Bible becomes a reusable asset for future runs that consume it.

The structurally critical commit-2b eval case — **the closing-the-loop test** — verifies that Em can cite Cy's identity rules during a real T2 critique. The test:
1. Author `characters/sean-anchor/` via Cy.
2. Generate a deliberately-broken Phase 5 keyframe of Sean (stylus in the wrong hand, hair part flipped) via NB Pro.
3. Run Em against the broken frame with `cites_criteria` enabled.
4. Assert that Em's verdict cites at least one `IR.sean.*` rule by ID.
5. Assert that the impact tag of the cited rule fires Em's escalation hatch correctly.

This is the structural fix synthesis §5 demands made operational. If Em can't cite Cy's rules, the Bible is a decorative artifact, not a contract. The eval case ships intentionally red on commit 2's first day and flips green by the end of commit 2b — the diff is portfolio content (the moment Bible authoring became contract-grounded, not just structured).

**Why it was selected.** Resolving v2 Open Q6 in favor of both Project-Types is the structural fix synthesis §5 names — taste enters the system at the earliest possible upstream point. Bible authoring as a Maya-routable Project-Type means the Bible isn't a side-effect of Phase 2 inside a larger piece; it's a first-class deliverable. The closing-the-loop test is the eval-suite case that proves the architecture works end-to-end — without it, the Bible is structurally complete but operationally untested. The diff (red → green) is the museum content that documents *the moment Bible authoring became real* in the pipeline.

**Key assumptions to validate.**
- Maya's planner code can route to Bible-authoring without a structural rewrite. (Plausible — Maya's plan is structurally a phase list with per-phase configurations; `bible_authoring` becomes a phase-list variant.)
- Em's prompt already supports citing arbitrary `AC.*` IDs without category-specific code. (Plausible per commit 8 — Em already cites criteria by ID; the IR.* prefix is just another mnemonic shape.)
- The deliberately-broken-frame fixture for the closing-the-loop test is generatable within a 5-minute test budget. (Plausible — NB Pro generates a single frame in 30-60 seconds; the fixture can be pre-generated once and committed to `evals/character-designer/fixtures/`.)

---

## 7. Deferred Ideas (Not Rejected — Promotion Triggers)

| Idea | Why deferred | Promotion trigger |
|------|--------------|-------------------|
| PM1 — Two readers, two passes | Folded into TOP-3's three-phase shape — Pass 1 Opus authors both the visual plan AND the structured rules in one envelope | Already promoted |
| PM3 — `risk-bible.md` | Folded into TOP-1's folder schema as a top-level Bible artifact | Already promoted |
| PM4 — Migrate sean-anchor first, then add claude-mascot | Already the commit 2 work plan; the implementation prompt names sean-anchor as warmup and claude-mascot as the second-character validation | Already promoted — sequencing detail |
| DES4 — `cy-confidence-notes.md` | Folded into TOP-1's folder schema as a top-level Bible artifact | Already promoted |
| ENG5 — Load 2d-animation-principles skill into Cy's standing context | Folded into TOP-3's Pass-1 Opus prompt — the standing context loads the skill verbatim | Already promoted — implementation detail |
| ROT1 — `bible-walkthrough.md` portfolio artifact | Pre-museum-capture portfolio content; valuable but not blocking commit 2 | Lands as part of commit 2 final polish; promoted to museum surface in commit 6 |
| ROT2 — Style register as closed-vocabulary top-level | Folded into TOP-1's `character.yaml` schema | Already promoted |
| ROT3 — `em-citation-cheatsheet.md` | Sibling to PM3's risk-bible; ships if PM3 ships, deferred otherwise | Lands as commit 2 polish if writing the cheatsheet from Bible authoring takes < 30 min; otherwise commit 6 |
| ROT4 — LoRA seed plate list in `character.yaml` | Forward-leaning, no LoRA exists yet; the field is informational | Adds one field to `character.yaml`; lands in commit 2 — zero cost, anticipates Image-Model-DR Experiment 1 |
| ROT5 — Before/after comparison strip | Pillow + matplotlib stack already in use; visual companion to ROT1 walkthrough | Lands as commit 2 polish if the matplotlib render is under 30 min; otherwise commit 6 |
| Hand-authored Bible Project-Type variant | The Cowork preamble locked Cy-leads-Sean-reviews; a hand-authored variant could exist but isn't needed in commit 2 | Reopen if Sean wants to ship a Bible without Cy's authoring loop after three Cy-authored Bibles |
| Cross-character shared `style/` directory | Multi-character pieces sharing a palette/style; not needed until pieces routinely run 3+ characters | Promote when the third character lands in production |

Twelve deferred items, eight of which are already absorbed into the top five as sub-components. The brainstorm produced more material than the converged five would suggest — the convergence is about which artifacts ship in commit 2, not which ideas get used.

---

## 8. What Commit 2 + Commit 2b Look Like

Concrete shape of the implementation handoff, ready for the next Claude Code execution session to pick up.

**Files touched (commit 2 — warmup):**
- The anchor migration: `images/2D-Character-Sketch-Sean-v1.png` → `characters/sean-anchor/anchor.png` (git mv), with a symlink at the legacy path through commit 7 (Animatic ingestion lands and Act 2 work is structurally complete).

**Files touched (commit 2 — main event):**
- NEW `pipeline/agents/character_designer.py` — Cy's `AgentSpec` implementation, three-phase Opus → NB Pro → Gemini flow per TOP-3
- NEW `pipeline/agents/prompts/cy-character-designer-context.md` — standing-context preamble (mirror of `maya-planner-context.md`), loads `2d-animation-principles` skill verbatim
- EXTEND `pipeline/criteria.py` — graph schema gains `character_id` field + extended `derived_from` plate-region pointers per TOP-2
- EXTEND `pipeline/agents/cost_estimator.py` — adds NB Pro Bible-authoring spend to the Phase 2 row
- NEW `pipeline/cli/bible.py` — `pipeline bible init / show / approve / mutate / iterate` subcommands per TOP-4
- NEW `templates/bible/character.yaml.template` — anchored template with style_register, palette, proportions, identity-rule pointers, cy_confidence_notes section, flux_lora_seed_plates field (ROT4 folded in)
- NEW `templates/bible/source-refs-checklist.md` — the `0-sean-author-this.md` content per DES3
- NEW `characters/sean-anchor/` — the actual migrated Bible from the warmup, populated with the existing material (anchor.png, the NEW-ANIMATION-PIPELINE turnaround + motion plates, etc.)
- NEW `characters/claude-mascot/` — second-character validation; Cy authors this end-to-end against the existing `images/Claude-Mascot/` source refs
- EXTEND `manifest.yaml` — `brief:` block gains `project_type: bible_authoring | animation_piece` support; `characters:` block points at the active Bible directories
- EXTEND `templates/brief/01_production_brief.md` — adds the `project_type` YAML frontmatter field

**Files touched (commit 2b — evals):**
- NEW `evals/character-designer/cases.yaml` — 5-7 seed cases covering Cy's three-phase loop branches (clean Pass-3 / Gemini-flag + regenerate / three-attempt-ceiling-hit), the graph schema validation (IR.*  namespace), the closing-the-loop test (TOP-5 — Em cites Cy's rules), and one intentionally-red case (Bible drift on an under-spec'd source-refs directory)
- NEW `evals/character-designer/runner.py` — pytest harness, mirrors `evals/planner/runner.py`
- NEW `evals/character-designer/conftest.py` — shared fixtures including the deliberately-broken Phase 5 frame for the closing-the-loop test
- NEW `evals/character-designer/fixtures/` — three fixture source-refs directories (well-specified / under-specified / multi-character) + the deliberately-broken Phase 5 frame
- NEW `evals/character-designer/failure-modes.md` — observed failure taxonomy. Start with four: identity-rule-too-generic-to-cite, plate-passes-gemini-but-drifts-from-source-refs, motion-plate-source/derived-mismatch, em-cannot-cite-cy-rules-at-T2-critic
- NEW `evals/character-designer/last-run.md` — baseline trace (red on the closing-the-loop test on first day)
- NEW `evals/character-designer/README.md` — portfolio-grade write-up mirroring `evals/planner/README.md`

**Out of scope for commit 2:**
- Phase 5 wiring of Cy's identity rules into Flo's per-shot prompt construction (commit 5+ work; ENG2's `derived_from` field is the connection point)
- Museum capture surfacing of Bible artifacts (commit 6; ROT1's walkthrough is the surface)
- The hand-authored Bible variant (deferred — Cy-leads-Sean-reviews is the locked workflow)
- LoRA training run for Sean's custom character LoRA (Image-Model-DR Experiment 1 — separate workstream; ROT4's seed-plate field is the on-ramp)
- The cross-character shared style/ directory (deferred until the third character lands)

**Effort estimate:** 5-7 evenings for commit 2 (the change-map's M estimate stays honest because the schema decisions are made here in the brainstorm; the implementation is grinding the prompts and the cache hash function) plus 1-2 evenings for commit 2b. The wall-time variable is Pass-1 Opus prompt iteration — same as Maya's commit 3, mitigated by the same lift-from-Maya pattern.

**Dependencies:** Commits 3 + 3b are shipped (Maya's planner + the criteria.py v1.1 graph schema). Commit 8.1a is shipped (the corrected `agy` flag shape Cy's Pass-3 verification inherits). Commits 4 + 8 are shipped (DAG runner, Em vision critic). Nothing else blocks commit 2.

---

## 9. What This Brainstorm Doesn't Decide

To prevent scope creep:

- **The exact prompt text for Cy's Pass-1 Opus call.** Commit 2 prompt-iteration territory; the *contract* (read Studio Brief + source-refs, emit character.yaml + IR.* graph entries + risk-bible + cy-confidence-notes + plate-generation plan) is what this brainstorm locks.
- **The exact wording of the closing-the-loop eval case's broken-frame fixture.** Commit 2b implementation detail; the contract (Em must cite at least one IR.* rule against a frame with deliberate identity drift) is what this brainstorm locks.
- **The full closed vocabulary for identity-rule categories.** Starting set is `anatomy / hair / face / proportion / palette / costume / prop / pose / motion / style`; will tighten or expand based on the first two real Bibles (sean-anchor + claude-mascot).
- **The Gemini Pass-3 regeneration prompt's exact wording.** Commit 2 implementation detail; the contract (failure reasoning threads into the next NB Pro call, three-attempt ceiling per plate) is what this brainstorm locks.
- **The `bible iterate` command's reject-aware regeneration UX surface.** Will be tuned during commit 2 implementation; the first three real Bible iterations calibrate.
- **The visual specification of the `comparison-strip.png` from ROT5.** Optional polish; ships a placeholder if matplotlib render slows iteration.

---

*The Bible schema is concrete. The folder shape is grounded in real on-disk material. Cy's three-phase loop mirrors Maya verbatim. The identity rules become first-class criteria. The CLI muscle memory carries over. The closing-the-loop test is named. Commit 2 has its specification.*
