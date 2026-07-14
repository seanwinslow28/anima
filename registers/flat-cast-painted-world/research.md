# `flat-cast-painted-world` — register research

**Date:** 2026-07-13 · **Consumer:** a committed signature look Sean selected by eye (costed Higgsfield image spike + Seedance 2.0 motion test, 2026-07-13; his eye the sole arbiter). First *potential* consumer: the AI-guru "trash cat" episode idea (adoption not locked — the AI-guru pilot's authored register is `90s-nicktoon-grossout`). · **Status:** `LOOK RATIFIED — HERO LOCKED — READY TO AUTHOR (2026-07-13)`. **Human Checkpoint 1 PASSED** (Sean ratified the research as-is) + **Human Checkpoint 2 PASSED** (Sean cold-confirmed the hero reads as the register). Hero locked at [`refs/flat-cast-painted-world-hero.png`](refs/flat-cast-painted-world-hero.png) (= the ratified `FU1_fusion.png`, gpt-image, md5 `0235b6c6192b798291fe306a776c382e`, 2688×1520). **Transport RESOLVED — `GPT_IMAGE` (unwired, fails loud):** the Step-S NB2 confirmation spike (2026-07-13, Higgsfield MCP, same FU1 prompt on NB2) came back **NO-GO** — NB2 collapsed the two-media split into one unified illustrated medium and dropped the boiling line (Sean's eye + this analysis agreed; spike at [`refs/spike-2026-07-13/FU1-NB2-transport-spike.png`](refs/spike-2026-07-13/FU1-NB2-transport-spike.png)). This is the **third gpt-image register**; the gpt-image runner stays deferred + gated on a separate costed build. **AUTHORED into `pipeline/registers.py` (register #10) on 2026-07-13 — Step B complete** (the pure doctrine drill: RegisterSpec + Cy Example F + markers + doctrine line + template comment + `tests/test_flat_cast_painted_world.py`, $0/stub-green; both frozen md5 guards unchanged; six legacy registers byte-identical). Pending Sean's review — **only Sean merges.** See CHANGELOG 2026-07-13.

**Method:** four parallel deep-research subagents (living/boiling line & the flat cel figure · the two-media split & figure/ground legibility · the painted gritty storybook world · negative controls, tells, staging, genericization & bibliography), synthesized here into the four wire-ready outputs the [style-register authoring playbook](../../docs/architecture/style-register-authoring-playbook.md) + the [animation-vocabulary-expansion plan](../../docs/COMPLETED/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md) §2a require, plus the depth requirements (concrete craft mechanics, the hardest-to-prompt core, negative controls, the genericization rule). Research answers *"what makes the look the look,"* grounded in primary craft sources (animator/background-artist interviews, production commentary, illustration-craft writing), never surface pastiche. This register is a **school of mixed-media 2D craft**, studied attribute-only; **never a show, a cast, or a frame** (§7).

**The register in one line:** a **flat, boldly hand-inked 2D cartoon cast** — a living **boiling/wobbling** outline, flat cel color, **no rendered volume on the figures** — that visibly **pops** against a richly **hand-painted** gritty children's-storybook world (dry-brush weathered urban surfaces, muted earthy palette, folk-decorative flourishes, gouache washes, warm golden-hour grime). **Two media in one frame**, unified only by the shared warm light + a faint overall grain. It is the mixed-media sibling of two banked looks: **Collage Real** (same flat cast, but on a *photographic* world) and **Gritty Storybook** (a *unified* painterly medium, cast and world the same paint). This register is the middle path — **the cast is flat-graphic, the world is painterly, and the deliberate split is the point.**

---

## 0. The design question, resolved (Sean, 2026-07-13) — ONE RegisterSpec

The kickoff flagged one load-bearing design question: is the fusion look **one `RegisterSpec`** whose `style_token` describes the whole fused frame, **or** a flat-character register **plus** a compositing/staging convention (the brainstorm §3 Concept-A "register + recipe" note)?

**Resolved: ONE RegisterSpec.** Two grounds:
1. **The hero renders the whole look from a single prompt.** `FU1_fusion.png` (gpt-image, the ratified hero) was generated from **one text prompt** — the flat cel cast *and* the painted world came out together, no compositing pass. The look is *emergent from one generation*, so the whole frame is what the `style_token` must describe.
2. **The "register + recipe" split was Concept A's honest-scope note for Collage Real** (a flat character composited onto a *photographic* plate), where a compositing recipe is genuinely needed. It does not apply here — the painted world is not a separate plate, it is part of the same rendered frame. A separate "recipe" field would be a reader-less abstraction (the `family`-field anti-pattern the playbook bakes against — [samurai design doc](../../docs/active/2026-07-11-samurai-jack-s5-register-design.md) §2A).

**Downstream boundary (flagged, not in the spec):** the separate question of dropping a *pre-authored Bible character* (authored in its own register) INTO the painted world is a **Bea/Flo staging concern** that exists for every register, not a property of this one. It is out of scope for the `RegisterSpec`; §5.6 records the staging logic for whoever wires it later.

---

## 1. The claim ledger — the brief's assertions, verified

The "thin seed" here is Sean's brief description of the look + the FU1 generating prompt. Every load-bearing craft claim below is now web-verified against primary/secondary sources; **nothing rests on the seed alone.** The register is authored against this ledger.

| # | Brief / seed assertion | Verdict | Source(s) | Note |
|---|---|---|---|---|
| 1 | "living, boiling, wobbling hand-inked outline" | **Confirmed** | Line-boil doctrine [C1]/[C2]; *Ed, Edd n Eddy* three-tracing method [C4]; Plympton "alternate them back and forth… shimmering… feel alive" [C3] | Boil = the outline *redrawn slightly differently frame-to-frame*, most visible on a HELD pose. It is a property of the ink path, not of the pose being off-model (the guardrail, §5.1). |
| 2 | "flat cel colors, no rendered volume on the figures" | **Confirmed, with a named fork** | UPA flat-icon doctrine [C6]/[C7]; cel-shading vs flat-design distinction [C9] | The register sits at the **flat-design / UPA** end (no volume), NOT the cel-shaded-form end (flat shadows used to model roundness). Any shadow is a graphic mark or absent, never a rendered falloff (§5.2). |
| 3 | "thick, boldly hand-drawn outline" | **Confirmed, mechanism sharpened** | John K. logical-line-weight doctrine [C5]; line-weight craft [C13] | Bold ≠ uniform. A three-level weight hierarchy — heaviest on the outer silhouette, thinner interior, pressure-taper swell-and-snap — is what reads "hand-drawn" vs a uniform vector/anime keyline (§5.1). |
| 4 | "flat graphic cast POPS against the painterly world" (the two-media split) | **Confirmed — the register's core** | Classical cel figure/ground craft (Earle/*Sleeping Beauty*) [T5]; the modern deliberate-friction lineage (Cartoon Saloon, OtGW, Hey Arnold) [T7]–[T15] | The split is a century-old legibility craft (hold detail back around the figure; separate by value + bold outline) run in **reverse intent** — the visible media difference is now the *aesthetic statement*, not a production compromise (§5.3). |
| 5 | "richly hand-PAINTED gritty children's-storybook world" | **Confirmed** | Hey Arnold BG craft (acrylic + colored-pencil texture) [W1]/[W4]; Cartoon Saloon painterly-decorative worlds [W5]–[W7]; picture-book gouache lineage (Blair/Provensen/Keats) [W10]–[W13] | The world is a **painted** medium (hand-made grit drawn *in*, never a filter), NOT photographic — this is the firewall vs Collage Real (§5.4). |
| 6 | "cross-hatched dry-brush weathered urban surfaces" | **Confirmed as craft; term genericized in the spec** | Gouache surface verbs (dry-brush, hatch, sgraffito, rag-lift) [W18]/[W19]; Hey Arnold colored-pencil-over-acrylic grit [W1] | The world's texture IS built with dry-brush + hatched marks. **But the exact compound `cross-hatch` is pencil-test-colored's signature vocabulary** — so the spec describes the world as "dry-brush, scumbled, hatched, weathered" and keeps `cross-hatch` out of every clause/marker (§1 authoring choice + §6). |
| 7 | "muted earthy palette (ochre, brick-red, sage, cream)" | **Confirmed, mechanism sharpened** | Golden-hour analogous warm-earth palette [W15]; color-script desaturated-local-color + saturated-light [W16] | The mechanism: **muted local pigment + saturation carried by the warm light**, not by the pigment. Mood-keyed, not naturalistic (§5.5). |
| 8 | "soft gouache washes, folk-decorative flourishes" | **Confirmed** | Keats patterned-collage / hand-stamps / spatter [W12]/[W13]; insular/Celtic ornament worked into design [W14]; picture-book gouache [W10]/[W11] | "Folk-decorative flourishes worked into the environment" = hand-drawn repeated motifs on awnings/tile/signage/pattern, *belonging to the place*, not applied vector pattern (§5.4). |
| 9 | "warm golden-hour grime" | **Confirmed** | Gurney golden-hour light doctrine (warm light / cool shadow / single-source unifies) [W17] | One warm key light is the single strongest tool for making a flat cast sit *in* a painted world rather than pasted on; grime reads as warmth (not squalor) because of the warm key + soft contrast + muted saturation, not the subject (§5.5). |
| 10 | "two media in one frame, unified into one world" | **Confirmed, mechanism sharpened** | Wolfwalkers baked-in print-offset / chromatic aberration as an analog unifier [T11]; OtGW cinematic-light envelope [T14] | Because the cast is *flat* and the world is *painted*, the **unification is done by light + palette + a faint shared grain**, not by rendering. When it fails, it fails two ways: figure *sinks in* (value match) or reads *pasted-on* (no shared grade/grain) — §5.3. |
| 11 | "warm, hand-made, tactile; never glossy/3D/anime" | **Confirmed** | Visible-hand-as-a-feature doctrine [W5]/[T11]; cel-shading-vs-3D distinction [C9] | The warmth comes from *both* layers reading as authored by a person (visible ink boil + visible brush/pencil). Photographic seamlessness or rendered volume reads cold — the register forbids both (§5.2/§5.3). |
| 12 | "mixed-media / collage instinct" | **Confirmed as spiritual ancestor; boundary sharpened** | Gilliam cutout-collage ethic ("embrace the limitations," visible seams as content) [T16]; Gumball cartoon-on-photo [T17] | The collage instinct (things that don't belong on one screen, sharing it) is the *license*. But the classic collage/Gumball version is **cartoon-on-photographic** = the banked Collage Real register. **PAINTED world is what makes this one warm-and-authored rather than uncanny-composite** (§5.3/§6). |

---

## 2. Output 1 — the draft RegisterSpec (proposed; authored into `pipeline/registers.py` only on Sean's greenlight)

The asserted **money-phrases** (the per-register test asserts them as substrings present in a `flat-cast-painted-world` plate prompt): `boiling`, `flat cel color`, `no rendered volume`, `two media in one frame`, `hand-painted`, `muted earthy`, `golden-hour`. The **negative leak-controls** (asserted absent): pencil's `graphite` + `cream paper` + `cross-hatch`; primal's `weight-varying ink` + `over the color`; samurai's `outline-sparse` + `negative space`.

| Field | Value | Sourcing |
|---|---|---|
| `name` | `flat-cast-painted-world` | The machine slug — attribute-only (a FLAT cast against a PAINTED world); Sean-confirmed 2026-07-13. |
| `summary` | Mixed-media register: a flat, boldly hand-inked cel cast with a living boiling outline and no rendered volume, popping against a richly hand-painted gritty children's-storybook world — muted earthy palette, weathered urban surfaces, folk-decorative flourishes, golden-hour warmth. Two media, one frame. | §§5.1–5.7 |
| `identity_lock` | Match the face, hair, color palette, proportions, and silhouette of Image 1 exactly. The character is a flat graphic shape read by its bold outline and silhouette; the boiling line is surface treatment on the contour only and must never swim the proportions, features, or flat colors off-model. | The boil-is-line-only guardrail (§5.1) + silhouette-carries-identity (§5.6) |
| `preserve` | Keep the cast flat: a bold thick-to-thin hand-inked outline heaviest on the outer silhouette, a living boiling wobble on the contour, flat unmodulated cel color inside, and no rendered volume on the figures. Keep the world a separate hand-painted medium: dry-brush, scumbled, hatched, weathered urban surfaces, soft gouache washes, folk-decorative flourishes, and a muted earthy palette under one warm golden-hour key. Keep the two media legibly distinct — the flat graphic cast reads against the painterly world, unified only by the shared warm light and a faint overall grain. No airbrushed or volumetric modeling on the figures; no photographic or rendered world; no clean vector-smooth outline. | §5.1, §5.2, §5.3, §5.5, §6 |
| `style_token` | "Mixed-media 2D animation still — two media in one frame: a flat, boldly hand-inked cartoon cast with a living boiling outline, flat cel color, and no rendered volume, popping against a richly hand-painted gritty children's-storybook world of dry-brush weathered urban surfaces, folk-decorative flourishes, soft gouache washes, and a muted earthy palette (ochre, brick-red, sage, cream) under warm golden-hour light." | §§5.1–5.7 |
| `generation_model` | **`GPT_IMAGE` (`gpt-image-2`) — RESOLVED, honest to the ratified hero; UNWIRED, fails loud.** The hero `FU1_fusion.png` is Sean's own gpt-image generation, and the Step-S NB2 confirmation spike came back **NO-GO** (NB2 collapsed the two-media split; §4). Third gpt-image register; runner deferred + gated. | §4 |
| `final_model` | `NB_PRO` — the dormant painterly-final seam convention (no consumer yet; same as watercolor/photoreal/3d/primal/samurai). | Registry convention |
| `markers` | `flat-cast-painted-world` (the name) · `boiling hand-inked cast outline` · `flat cel cast no rendered volume` · `hand-painted gritty storybook world` · `two-media split` · `muted earthy ochre-brick-sage-cream` | §5 tells; collision-checked against all 9 existing registers' markers — clean (§6) |
| `stub_keywords` | `("fusion",)` — a single low-false-match keyword (Sean's mental name for the look), appended AFTER the legacy six + `primal` + `nicktoon`/`grossout` + `samurai` (precedence oracle-pinned) | §7; Task 2 |
| `reference_images` | **default `()`** — no code reads `spec.reference_images` (red-team fold, [samurai design](../../docs/active/2026-07-11-samurai-jack-s5-register-design.md) §4.1); the locked hero + provenance live in `refs/README.md`. | Matches all 9 existing registers |

**Deliberate prompt-authoring choice (mirrors primal §1 / samurai §1 / nicktoon §1):** `preserve` names **only this register's positives + generic anti-over-rendering refusals**. It does **not** name pencil's, primal's, samurai's, or line-art's *identity vocabulary* as negatives — naming a neighbor register can evoke it in the image model (the doctrine). In particular the world's real texture is **dry-brush + hatched**, but the exact compound `cross-hatch` (pencil-test's signature) is kept out of every clause and marker; drift-policing against neighbors lives in the Cy risk-bible (§3), not in `preserve`. The `preserve` text above contains none of the leak-control substrings (`graphite`, `cream paper`, `cross-hatch`, `weight-varying ink`, `over the color`, `outline-sparse`, `negative space`).

**Candidate Python (research-refined; the build's `RegisterSpec` source):**

```python
RegisterSpec(
    name="flat-cast-painted-world",
    summary=(
        "Mixed-media register: a flat, boldly hand-inked cel cast with a "
        "living boiling outline and no rendered volume, popping against a "
        "richly hand-painted gritty children's-storybook world — muted earthy "
        "palette, weathered urban surfaces, folk-decorative flourishes, "
        "golden-hour warmth. Two media, one frame."
    ),
    identity_lock=(
        "Match the face, hair, color palette, proportions, and silhouette of "
        "Image 1 exactly. The character is a flat graphic shape read by its "
        "bold outline and silhouette; the boiling line is surface treatment on "
        "the contour only and must never swim the proportions, features, or "
        "flat colors off-model."
    ),
    preserve=(
        "Keep the cast flat: a bold thick-to-thin hand-inked outline heaviest "
        "on the outer silhouette, a living boiling wobble on the contour, flat "
        "unmodulated cel color inside, and no rendered volume on the figures. "
        "Keep the world a separate hand-painted medium: dry-brush, scumbled, "
        "hatched, weathered urban surfaces, soft gouache washes, "
        "folk-decorative flourishes, and a muted earthy palette under one warm "
        "golden-hour key. Keep the two media legibly distinct — the flat "
        "graphic cast reads against the painterly world, unified only by the "
        "shared warm light and a faint overall grain. No airbrushed or "
        "volumetric modeling on the figures; no photographic or rendered "
        "world; no clean vector-smooth outline."
    ),
    style_token=(
        "Mixed-media 2D animation still — two media in one frame: a flat, "
        "boldly hand-inked cartoon cast with a living boiling outline, flat "
        "cel color, and no rendered volume, popping against a richly "
        "hand-painted gritty children's-storybook world of dry-brush "
        "weathered urban surfaces, folk-decorative flourishes, soft gouache "
        "washes, and a muted earthy palette (ochre, brick-red, sage, cream) "
        "under warm golden-hour light."
    ),
    generation_model=GPT_IMAGE,  # RESOLVED — NB2 spike NO-GO (§4); unwired, fails loud
    final_model=NB_PRO,
    markers=frozenset({
        "flat-cast-painted-world",
        "boiling hand-inked cast outline",
        "flat cel cast no rendered volume",
        "hand-painted gritty storybook world",
        "two-media split",
        "muted earthy ochre-brick-sage-cream",
    }),
    stub_keywords=("fusion",),
    # reference_images left default () — no code reads it (red-team fold);
    # the locked hero + provenance live in refs/README.md.
),
```

---

## 3. Output 2 — the Cy block (draft `### Example F — trashcat`)

Proposed **Example F** for [`pipeline/agents/prompts/cy-character-designer-context.md`](../../pipeline/agents/prompts/cy-character-designer-context.md) (added at authoring): three sample `IR.trashcat.*` records + a four-paragraph risk-bible excerpt, in the register's own vocabulary. **Categories verified against `criteria.py`'s `VALID_IR_CATEGORIES`** (`anatomy, hair, face, proportion, palette, costume, prop, pose, motion, style, view`) — this register's signature axes (the two-media split, staging, the painted world) are **NOT** IR categories (they describe the *frame*, not the *character*), so they live in the risk-bible prose and the staging notes (§5.6), never as an invented category. The three IR records describe the **character** (the flat cel cast), which is the half a Bible owns.

**Three sample `IR.trashcat.*` (the load-bearing trio):**
- `IR.trashcat.style.flat-cel-no-volume` — the figure is filled with **flat unmodulated cel color** and carries **no rendered volume**: no airbrushed shading, no soft gradient, no lit roundness. Any shadow is a single hard-edged flat graphic shape or is absent — never a modeled falloff. A frame where the cat is rendered with volumetric shading, a glossy sheen, or a soft gradient body fails.
- `IR.trashcat.style.boiling-inked-contour` — the character is wrapped in a **bold, thick-to-thin, hand-inked outline** (heaviest on the outer silhouette, thinner interior) that carries a **living boiling wobble** — the contour re-inks slightly differently frame to frame. A clean uniform vector keyline (no boil, constant width) fails; a boil that swims the *proportions or features* off-model (not just the line path) also fails.
- `IR.trashcat.palette.muted-earthy-cast` — the cat's local colors sit in the world's **muted earthy family** (ochre / brick-red / sage / cream range) so it reads as native to the painted world, keyed *into* the warm golden-hour light rather than lit against it, while still holding a clean value break against the painted field behind it.

**Additional wire-ready `IR.*` drafts the Bible pass can draw on:**
- `IR.{char}.style.silhouette-first-shape` — because the figure has no volume, the **silhouette carries identity**; the unique head/hair-mass/stance shape must read as this exact character filled solid black. If identity lived in fine rendering, it was never in-register.
- `IR.{char}.palette.value-break-against-world` — the character's value package must differ enough from the local painted background directly behind it to survive a grayscale/silhouette test (the figure/ground make-or-break, §5.3); never mid-value on mid-value.
- `IR.{char}.style.sparse-descriptive-interior` — interior linework is **sparse and descriptive** (one line per fold/plane), never hatched or tonal — this holds the figure graphic-flat and separates it hard from a pencil-graphite look.

**Risk-bible excerpt (four paragraphs, for Example F):**
1. **Drift directions.** Four pulls, each toward a named neighbor's *attributes* (never named in the prompt): (a) toward **heavy ink-over-color grit** — a weight-varying contour laid over the color with gritty texture *on the figure* — which collapses the flat cel cast into the primal sibling's unified grit; (b) toward **glossy 3D / anime rendering** — soft airbrushed volume, specular sheen, rendered depth — which kills the flat-no-volume discipline; (c) toward **outline-sparse flat poster minimalism** — dropping the bold boiling contour and the painterly world for clean flats and empty negative space — which is the flat-minimal sibling; (d) toward a **unified single medium** — either the whole frame painterly (the cast dissolving into the same paint as the world, the Gritty-Storybook sibling) OR the whole frame flat-graphic (a UPA-style world flattened to match the cast). The register lives in the **tension between a flat-graphic cast and a painterly-gritty world**; lose either pole, or unify them, and it collapses.
2. **What simplification cannot sacrifice about identity.** Because the figure has no rendered volume, the **silhouette is the identity** — the unique head/hair-mass/stance/proportion shape must survive every simplification, and the figure/ground value break must be engineered as a *pair* (the character's local colors chosen against the specific painted field behind them) so the character never sinks into the world. The boiling line may wobble the *contour path* but must never swim the *proportions, features, or flat colors* off-model. If the silhouette reads as this exact character with interior detail stripped, it holds.
3. **Where the research is thin.** Several attributes are reconstructions synthesized across separate sourced accounts, not single quoted doctrine: the **exact aesthetic-boil-vs-crude-drift line** (amplitude/on-model control — the sources state boil is intentional but not a hard amplitude spec); the **two-media unification recipe** (shared grade + faint grain + shared light — each mechanic is sourced, the assembly into a generation contract is synthesis); the **"grime reads warm not squalid" rule** (warm key + soft contrast + muted saturation — derived from the color-script principle applied to the Hey-Arnold/Keats examples). Treat these as authoring guidance grounded in the sources, not canon; frame-check against the locked hero.
4. **The three binary human-review checks.** (i) Is the **cast flat with no rendered volume** (flat cel color, hard/absent shadow shapes, no airbrush) AND wrapped in a **bold boiling outline**? soft-rendered / clean-uniform-line → figure-register fail. (ii) Is the **world hand-painted and gritty** (dry-brush, hatched, weathered, muted earthy, folk flourishes) rather than photographic, flat-clean, or negative-space? photographic → Collage-Real drift; clean-flat → flat-minimal drift; unified paint on the figure → Gritty-Storybook drift. (iii) Do the **two media read as distinct-but-one-world** — the flat cast pops against the painterly field, unified by one warm golden-hour key + a faint overall grain, the figure neither sinking in nor reading as a pasted sticker? sunk-in or pasted-on → two-media-split fail.

---

## 4. Output 4 — transport record

**Transport: RESOLVED — `GPT_IMAGE` (`gpt-image-2`) generation, `NB_PRO` final — INTENTIONALLY UNWIRED; fails loud.** The Step-S NB2 confirmation spike (2026-07-13) resolved the one open item **NO-GO for NB2** → `GPT_IMAGE`.

**What is settled:**
- The ratified hero (`FU1_fusion.png`) is Sean's own **gpt-image** generation, so `GPT_IMAGE` is the honest record. `invoke_image_edit` raises `UnwiredTransportError` at its first line for any model outside `SUPPORTED_IMAGE_MODELS = {NB2_FLASH, NB_PRO}` (`gpt-image-2` included), so the existing guard **already covers it — no new code** (same as primal fork #1's post-fix state, and samurai). `final_model` stays `NB_PRO` (the dormant painterly-final seam).
- This is the **third gpt-image register** (after primal + samurai). Wiring an actual gpt-image runner + across-edit identity validation is **DEFERRED and GATED** on a separate, costed, Sean-greenlit build — the $0 authoring drill does not wire it. (The AI-guru cat series is a real potential consumer, so wiring gpt-image is increasingly justified — but it stays its own greenlit build.)

**The NB2 confirmation spike (2026-07-13, Higgsfield MCP `nano_banana_2`, the exact FU1 prompt, 16:9) — NO-GO:**
- The ladder says spike NB2 first ([converged plan](../../docs/COMPLETED/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md) §3c); round 2 had tested only gpt-image, so the fusion look was unproven on NB2. The spike ran the same FU1 prompt on NB2 so the comparison varied **engine**, not art direction.
- **Result:** NB2 hit the scene + the muted-earthy palette + golden-hour warmth, but **collapsed the register's core two-media split** into one unified illustrated cartoon medium, and **dropped the boiling hand-inked outline** (clean uniform digital line instead; the cat drifted toward rendered fur volume). It landed closer to the banked **Gritty Storybook** (unified medium) than to the fusion split — the exact predicted "single model solves two media into one" failure mode.
- **Verdict:** NB2 does **not** hold the flat-cast-on-painted-world split; gpt-image does (as it did on the ratified hero, mirroring primal's spike). **Sean's eye + this analysis agreed** (no LLM aesthetic judge). Spike artifact retained at [`refs/spike-2026-07-13/FU1-NB2-transport-spike.png`](refs/spike-2026-07-13/FU1-NB2-transport-spike.png) (1376×768).
- **Recorded:** `generation_model = GPT_IMAGE` (unwired, fails loud). Buildable-now-on-NB2 is off the table for this register — its identity IS the two-media split NB2 can't render.

---

## 5. The look, by dimension (the seven-dimension craft account)

### 5.1 Line & contour — the living boiling outline + the weighted taper

**The boil (SOURCED).** Line boil is the visible wobble of a hand-drawn outline caused by the same shape being **redrawn slightly differently frame to frame** — most conspicuous when a character is *holding still* yet the outline keeps shimmering; "it's impossible for a human to draw the exact same line twice," and in sequence "these minor variations create a vibrating energy," a "bubbly quality, hence 'boil'" [C1]/[C2]. Concrete production method (the cleanest documented case): on *Ed, Edd n Eddy* "the boiling line is created by tracing off a drawing three times," and even a held pose is not one cel but **2–3 re-inked tracings cycled**, so "there is life and movement (called 'boiling') in the lines of the held characters themselves" [C4]. Plympton: "sometimes they're the same drawing, and I alternate them back and forth and it gives it a kind of shimmering effect that makes it feel alive" [C3]. Three perceptual payloads: it "imparts life to static objects," reads as "texture reminiscent of physical media like ink," and "triggers nostalgia associated with traditional cartoons" [C2].

**The guardrail — aesthetic boil vs crude drift (RECONSTRUCTION on [C1]).** Early animators considered boil an *imperfection*; the reframe is that avoiding it makes characters "seem frozen in place like statues," so it is "purposely used or even exaggerated to add life" [C1]. The operative line for this register: **aesthetic boil is controlled, small-amplitude, and confined to the line** (silhouette stays on-model; colors/proportions do not swim); **crude low-framerate drift is uncontrolled** (the whole shape wanders off-model). Boil is a property of the *ink path*, not of the drawing being wrong. This is the single most important identity guardrail (encoded in `identity_lock`).

**The weighted taper (SOURCED — John K. inking doctrine [C5], corroborated [C13]).** A three-level hierarchy, heaviest outside: (1) **outer silhouette** thickest, with extra weight "at the bottom of major forms — the jaw, feet — to give the whole character a feeling of weight"; (2) **subdivisions** (clothing, hair-mass, color separations) slightly thinner; (3) **interior detail** thinnest, tapering to a point [C5]. "Every line should mean something… there should never be floating lines that don't mean anything" [C5] — the anti-noodle rule that keeps the figure graphic and sparse (not hatched). What reads "hand-drawn" vs vector/anime keyline is the **thick-to-thin contrast + the pressure taper** ("thin → swell → snap to a point") [C13]; a uniform-weight line is the vector tell. **The heavy tapered outline is the element that boils** — the register's look is the *Ed, Edd n Eddy* thick wobbling contour, not a thin nervous scribble.

### 5.2 Figure fill — the anti-rendering discipline (flat cel, no volume)

**Flat local color, no gradient (SOURCED).** The figure is filled with **flat unmodulated local color** inside the ink outline; if any shadow appears it is a **hard-edged flat shape** (at most 2–3 discrete tones "as blocks of color rather than being smoothly mixed in a gradient") [C9]. The purest lineage is UPA: "simplified shapes, bold colors unmodulated by rounding effects or shadow," "a forceful engagement with the two-dimensional surface" [C6]/[C7].

**The load-bearing fork — flat-design vs cel-shading (SOURCED, [C9]).** Cel-shading and flat-no-volume are *not* the same: "cel shading simulates 3D form using flat shadow zones… so objects still look three-dimensional… whereas flat design avoids any impression of depth or volume entirely" [C9]. The brief says **no rendered volume**, so the register sits at the **flat-design / UPA end** — either no shadow, or a shadow used *graphically* (a design mark), never to model a form turning away from light. If a hard shadow describes a sphere's roundness, it has slid into cel-shaded volume and out of register. This is also the clean separation from (a) pencil-test graphite hatching (no tonal buildup here — value is a flat fill), (b) painterly tonal rendering (no continuous hue/value modulation), and (c) glossy 3D/anime volume (no airbrushed roundness, rim light, or gradient).

### 5.3 The two-media split — the register's hardest-to-prompt core

This is the axis that makes the register itself, and the axis a single image model most wants to "solve" into one medium. It is a **century-old legibility craft run in reverse intent.**

**The classical craft (SOURCED).** Cel animation is definitionally two media stacked — flat inked/painted characters on cels over separately **painted** backgrounds [T1]. Legibility across that split was engineered by **holding detail back around the figure**: the cleanest documented case is Eyvind Earle on *Sleeping Beauty*, where director Geronimi's complaint — "All that beautiful detail in the trees… who the hell's going to look at all that?" — drove the fixes: Earle **airbrushed backgrounds so they "wouldn't compete with the animation,"** rationed detail by light ("where a streak of light crosses a tree, ornate bark appears; in shadow areas there's less detail"), and organized background richness into **big readable shapes "rather than brushstrokes or gradients"** [T5]. The general rule is the notan/silhouette doctrine: positive space (subject) gets detail; negative space (around it) gets held back, so the figure survives the **grayscale silhouette test** [T6].

**The modern reverse-intent lineage (SOURCED) — the register's license and warmth.** Cartoon Saloon is the anchor: **flat, decorative, graphic 2D characters set into watercolour-painted worlds**, a chosen decorative idiom (medieval art / illuminated manuscripts), 2D's "organic feel and timelessness" the stated rationale [T7]/[T8]. *Wolfwalkers* runs **two art directions that "have to live together somehow,"** designs characters explicitly to **stand out** against the textured field (Robyn's angular hood), choreographs **transition zones** where the media approach each other, and bakes **print-registration offset + chromatic aberration** into the whole frame as an analog unifier [T9]/[T10]/[T11]. *Over the Garden Wall*: a simple flat cast under lush painted storybook worlds, unified by **classical cinematic light** that "envelops" the cast "rather than competing with them" [T13]/[T14]. *Hey Arnold!* is the TV-scale proof the split survives a **busy, grimy urban field** [T15].

**What makes the friction read intentional + warm (SOURCED synthesis).** (1) Both layers are **legibly hand-made** — visible brush/watercolour grain in the world + visible ink boil in the cast; the eye enjoys the difference because both read as "a person made this," not "an asset keyed over a plate." (2) The difference is **consistent and total** (every character flat; the whole world painted) — consistency reads as a rule, inconsistency as a mistake. (3) **One light/color logic governs both layers.** (4) The cast is **designed to pop** — the pop is engineered staging.

**Failure modes (the two poles) — prompt against both:** the cast **sinks into the world** (value/hue matches the local field, outline thins → figure/ground collapse — Earle's pre-airbrush failure), OR the cast reads as a **pasted-on sticker** (too-clean cut edge, no shared grade, no shared grain, mismatched light → tips from friction into compositing-error). The difference between the two is entirely the **unifier: one warm grade + one light direction + a faint shared grain.** A third failure is the media getting "solved" into one (rendered cast → unified painterly; flattened world → UPA).

### 5.4 The painted world — surface craft & texture

**Grit is a two-pass additive build, never a filter (SOURCED synthesis).** The cross-cutting mechanic across the references: a **flat/painted base** establishing local color, then a **second textural pass** carrying the grain. Hey Arnold's is the most concrete — **acrylic paint, then textured on top with colored pencil** worked over the dry acrylic (the mortar lines, cracks, brick tooth are *drawn back into* the paint) [W1]/[W4]; the lived-in read comes from **cataloguing specific worn objects** (rusty cars, cracked concrete, crushed cans, mattresses) into the frame, not a global dirt pass [W1]. Wolfwalkers' town uses **degraded woodcut-print linework** as weathering [W5]; Craig of the Creek supplies **line + flat-grey blocking, then a paint department renders over it** [W9] — the same base-then-texture division of labor. The concrete gouache surface verbs: **dry-brush** (scratchy broken marks for peeling paint / rough brick / dusty concrete), **hatch/stipple** (grit + tone), **sgraffito/scraping** (cracks, wire-lines, mortar), **rag-lifting** (soot streaks, water stains), **layered washes** (atmospheric depth) [W18]/[W19].

**Folk-decorative flourishes, concretely (SOURCED).** Three sourced mechanisms: **insular/Celtic ornament** worked *into* the design of props/surfaces (decoration as structure) [W14]; **pattern-as-surface** (Keats's patterned-paper standing in for wallpaper, tile, brick coursing) [W12]; **hand-painted vernacular signage** (hand-lettered shop signs, awning stripes — the folk content of a working-class street) [W1]. For this register: repeated hand-drawn motifs on awnings/tile/brick/signage/patterned windows — marks that are **drawn by hand and belong to the place**, never applied flat vector pattern.

**Storybook lineage (SOURCED).** The world's DNA is the warm hand-made picture-book tradition — Mary Blair's flat gouache "snappy unified color" [W10], the Provensens' "flat gouache… soft colour palette" [W11], and above all **Ezra Jack Keats's collage-urban** *Snowy Day*: a flat, graphic city built from paper cut-outs with pattern-collage, hand stamps, and India-ink toothbrush spatter — a warm, dignified, *charming* city (grit-but-not-grim) [W12]/[W13].

**How it stays storybook (charming), not gritty-realism (harsh) — the governing rule (SOURCED levers):** (1) **visible hand / imperfection is a feature** (marks meant to be seen — photographic seamlessness reads cold) [W5]; (2) **flat/graphic, not volumetric** — hold the flatness + limited palette and it stays picture-book [W7]/[W10]; (3) **warm key + soft contrast + muted saturation = charm; cool key + high contrast + full saturation = grim** (same subject, opposite read) [W16]; (4) **grime as specific loved objects, not generic filth** [W1].

### 5.5 Palette & lighting — muted earthy + golden-hour, mood-keyed

**The palette mechanism (SOURCED).** A warm-earth analogous run — **yellow ochre → burnt sienna/brick-red → cream**, with **sage** as the cool complementary rest-note [W15]. The key mechanic: **desaturated local color in the surfaces + saturation carried by the warm light** [W16] — the world's pigments stay muted; the *light* carries the saturation. This makes the register **mood-keyed, not naturalistic** — pick the warmth first, bend local color toward it.

**Golden-hour light (SOURCED — Gurney [W17]).** Low sun → light travels nearly parallel through more atmosphere; blue scatters out, leaving orange dominant. **Warm light / cool (bluish) shadow**, and a **single warm source naturally harmonizes everything** — "golden illumination creates visual coherence across diverse landscape elements." Atmospheric depth: farther planes go cooler/lighter. For a flat cast in a painted world, **one warm key is the single strongest unifier** — the cast and world bathed in the same wash is what makes the flat figure sit *in* the world rather than pasted on. Grime reads as warmth (not squalor) because of the warm key + soft contrast, not the subject.

### 5.6 Form, appeal & staging — silhouette-first, grounding the cast (for Bea/Flo, not the still spec)

**Appeal with no volume (SOURCED).** Strip rendered volume and appeal is carried by **design, line, and pose**: the silhouette must read filled solid black [C10]; **shape language** communicates traits [C10]; expression comes through the **confident line and the pose**, not the modeling (Cartoon Saloon clean-up artists "work like comic-book inkers," expressive with the line [C8]; UPA "based on feelings rather than anatomy" [C6]).

**Grounding the flat cast in the painted world (SOURCED doctrine — the Bea/Flo staging note).** The Cartoon Saloon doctrine is to **key the characters to the environment's register and light** [W5]. Concretely: **contact shadows / occlusion** (a simple flat cast-shadow shape seating the figure); a **shared golden key + cool shadow** on the figures; an **earth-toned cast** (ochre/brick/sage/cream family) so it reads native [W9]; **medium-shot as home base** (enough world to establish the painted place, enough cast to read the flat graphic figure — ECUs collapse the split, extreme wides lose the pop); the **world as a lived-in character** doing expository work the flat cast doesn't; a **held/gentle camera** so the two media don't fight. This is the downstream boundary (§0) — captured here so it survives into a Storyboard/Motion phase; the still `RegisterSpec` owns none of it.

### 5.7 Timing (for the Motion phase; informs Bea/Mo, NOT the still register)

- **The boil lives on holds.** A hold is authored as a **2–3 drawing boil loop** (the *Ed, Edd n Eddy* three-tracing method [C4]), never a single frozen cel — avoiding it makes the figure "seem frozen like a statue" [C1].
- **Boil cadence: on twos/threes** — swapped every ~2–4 frames reads as hand-drawn; every single frame (ones) reads too busy [C11]/[C12]. **Never let the boil-swap drift the *pose* off-model** — the boil is a line-path loop over a locked drawing.
- **~12fps limited timing** reads more authentic than 60fps-smooth [C2]. *Honesty flag: exact per-show swap counts beyond the "three tracings" and the generic "~every 4 frames" heuristic are not authoritatively documented — treat 2–4 frames as a well-supported heuristic, frame-step the hero at the spike.*

---

## 6. Negative controls (the confusable-adjacent registers)

The load-bearing table — it must let a reviewer classify any single frame. **The two axes that carry the whole table are World medium and Figure↔World relationship** — those two alone resolve most collisions.

| Axis | **flat-cast-painted-world** (THIS) | Collage Real (banked sibling) | Gritty Storybook (banked sibling) | `primal-sketch-grit` | `samurai-jack-s5` | `line-art-only` | `pencil-test-colored` |
|---|---|---|---|---|---|---|---|
| **Line / outline** | **Thick, boiling** hand-inked contour on the CAST; world has little/no outline (paint reads the form) | Thick boiling contour on cast (same as THIS) | Little/no hard outline — forms read by paint, both cast & world | Heavy **weight-varying** ink kept **over the color**, figure AND ground | **Almost none** — edges are color shapes | **Bold, UNIFORM, clean** line, no boil | Soft **graphite** line + construction lines |
| **Figure fill & render** | **Flat cel color, no rendered volume** | Flat cel color, no volume (same as THIS) | **Painterly** — cast modeled in the same paint as the world | Painterly/gritty fill under ink; textured | Clean flat color, maybe one hard shadow shape | Flat/limited color; line describes | **Graphite + cross-hatch shading on the figure**, cream tint |
| **World medium** | **Hand-PAINTED** — dry-brush, hatched, gouache, weathered | **PHOTOGRAPHIC / real-textured** | Hand-painted, **SAME paint as the cast** | Gritty painterly, unified with figure | Clean flat fields, **dramatic negative space** | None / blank | **Cream paper**, minimal ground |
| **Figure↔World relationship** | **TWO MEDIA, ONE FRAME** — flat graphic cast POPS against painterly world | TWO MEDIA — flat cast pops against a *photographic* world | **ONE UNIFIED MEDIUM** — cast & world the same paint (no pop-out) | **UNIFIED** — one gritty ink-over-color treatment | **UNIFIED** flat-graphic poster | Unified line world (or figure on blank) | Unified pencil-on-paper |
| **Palette** | **Muted earthy** (ochre/brick-red/sage/cream), golden-hour | Cast may be saturated-flat vs realistic photo color | Muted earthy painterly | Earthy desaturated base + one shock accent | Bold, **limited high-contrast** flats; saturated accents | Monochrome / limited | Graphite gray + cream |
| **Texture** | **SPLIT** — cast texture-less (flat) / world texture-rich | SPLIT — flat cast / photo-real texture | **Uniform** paint texture everywhere | **Uniform** grit/ink everywhere | **Minimal** — clean flats | Line only | Uniform paper-grain + graphite |
| **Tone** | Warm, lived-in, folk storybook-with-grit; wistful | Graphic-vs-real friction; deadpan/uncanny | Cozy-melancholy painterly warmth | Raw, punk, grimy | Cool, mythic, minimal, poster | Clean, diagrammatic | Intimate, in-progress |

**The clean cuts, as one-liners:**
- **vs Collage Real** → the *world medium*. Painted (THIS) vs photographic (Collage Real). Same flat boiling cast; only the ground differs. **This is the firewall the "painted, not photographic" constraint enforces.**
- **vs Gritty Storybook** → the *split*. Two media (THIS) vs one unified paint (Gritty). The cast pops out (THIS) vs the cast dissolves into the same paint (Gritty).
- **vs `primal-sketch-grit`** → flat-cel cast + grit kept **off** the figure, on the painted world only (THIS) vs weight-varying ink kept **over the color** across everything, unified grit (primal).
- **vs `samurai-jack-s5`** → bold boiling **outline** + gritty painterly **world** (THIS) vs near-no-outline + clean flats + negative space, no world-grit (samurai).
- **vs `line-art-only`** → painterly world + flat color + boiling line (THIS) vs bold **uniform** clean line, no painterly world (line-art).
- **vs `pencil-test-colored`** → ink/cel cast + paint world (THIS) vs graphite line + cream paper + figure cross-hatch (pencil).

**Frame-classification checklist (review-time, first branch that resolves wins):**
1. Does the figure have a **thick hand-drawn contour**? No → not THIS (near-no-outline+negative-space = samurai; painterly-modeled figure = Gritty Storybook; graphite+cream = pencil).
2. Is that line **uniform/clean** (+ no painterly world) → `line-art-only`; or **boiling/wobbling** → continue.
3. Is the figure **flat cel, no volume** → continue; or **painterly/gritty with ink over color, figure & ground sharing it** → `primal-sketch-grit`.
4. Is the **world photographic** → **Collage Real**; **hand-painted** (dry-brush/hatched/gouache/weathered) → continue; **clean flat fields + negative space** → re-check for `samurai-jack-s5`.
5. Do cast & world look like the **same medium** (cast dissolves into the paint) → **Gritty Storybook**; or **two media, flat cast popping against a painterly world** → ✅ **`flat-cast-painted-world`**.
6. (Confirm) muted earthy palette + weathered urban surfaces + folk flourishes + golden-hour grime → confirms THIS.

**Marker collision check (this session):** the six markers are collision-free against all nine existing registers' marker sets (verified by string against `pipeline/registers.py`). The world's real cross-hatched texture is described as **dry-brush / hatched** in every clause — the exact compound `cross-hatch` (pencil-test's marker) is deliberately kept out so the register does not evoke or collide with the pencil vocabulary.

---

## 7. The non-derivative rule (doubly load-bearing)

Capture the **school**, never the cast, the frames, the title, or the person. **Legal frame (SOURCED):** the idea/expression dichotomy — copyright protects the *expression* fixed in a work, not the "ideas, procedures, processes, systems, methods of operation… concepts, principles," nor "familiar symbols or designs" (US Copyright Office *Circular 33* [L3]); "style alone is not usually considered the subject matter of copyright" — monopolizing style would "chill expression" (Creative Commons [L1]). **Refinements:** style is not an absolute shield — stylistic similarity "can be part of" but "cannot be determinative of substantial similarity by itself" [L1], scholars note style straddles idea/expression [L2]/[L5], and **specific well-developed characters are independently protectable** (the *Nichols v. Universal* lineage [L4]). The discipline is therefore **attribute-extraction + zero specific-expression reuse** — which is why `refs/` ships with no third-party frames. **Genre/technique is free:** "line boil," "cel color," "gouache," "golden hour," "mixed media" are craft techniques, not protected expression.

| Reusable ATTRIBUTE (safe in prompts/clauses/markers/committed refs) | Protected / AVOID (specific IP or person — forbidden) |
|---|---|
| Flat cel cast with a thick boiling hand-inked outline, no rendered volume | Any show/film title in a production prompt, clause, marker, or committed ref |
| Hand-painted, dry-brush, hatched, weathered urban world | Any studio, creator, director, or background-artist name |
| Muted earthy palette (ochre, brick-red, sage, cream); golden-hour grime | Any named character (a show's protagonist, mascot, etc.) |
| The two-media split — flat graphic cast popping against a painterly world | Any logo, wordmark, title card, or trade dress |
| Folk-decorative flourishes; soft gouache washes; boiling line; dry-brush texture | A recreation of a specific recognizable frame/shot/scene from any work |
| Generic craft terms (line boil, cel color, limited palette, paper tooth, sgraffito) | A character design substantially similar to a specific protected character |
| Naming real shows/artists **in this research doc only**, as craft lineage | Naming them in any **production prompt, register clause, neutrality marker, or committed reference image** |

**The review test:** *A fan of the school recognizes the school; no one can name the episode.* The sole unavoidable named identifier anywhere in the register is the machine slug `flat-cast-painted-world` (internal, never a production string), exempt exactly as `primal-sketch-grit` / `samurai-jack-s5` / `90s-nicktoon-grossout` are.

---

## 8. Honesty flags (what the research could NOT establish)

- **Strongly sourced (quoted/primary):** the boil definition + method + *Ed, Edd n Eddy* three-tracing [C1]/[C2]/[C4]; Plympton's shimmer quote [C3]; John K.'s line-weight hierarchy [C5]; UPA flat-icon doctrine + cel-vs-flat-design distinction [C6]/[C7]/[C9]; Earle's hold-back-around-the-figure craft + the Geronimi quote [T5]; Cartoon Saloon flat-cast/painted-world + Wolfwalkers analog-unifier [T7]–[T11]; OtGW cinematic-light envelope [T14]; Hey Arnold acrylic+colored-pencil BG mechanic [W1]; Gurney golden-hour light [W17]; Keats collage-urban technique [W12]/[W13]; gouache surface verbs [W18]/[W19]; the copyright doctrine [L1]/[L3].
- **Reconstruction / synthesis (grounded, not single-quoted):** the exact aesthetic-boil-vs-crude-drift amplitude line (§5.1); the two-media **generation contract** and its two named failure modes (each mechanic sourced, the assembly is synthesis, §5.3); the "grit is a two-pass additive build" framing (§5.4); the "grime reads warm not squalid = warm key + soft contrast + muted saturation" rule (§5.4); "fold the cast into the world via shared light + earth palette + contact shadow" (§5.6).
- **Weak / unverified (flagged):** *Over the Garden Wall* specific BG-painting technique could not be sourced to a primary art-director account (palette/vintage-storybook attributions are community-level); Craig of the Creek pipeline is a portfolio blurb, not a full interview; the Gumball "without graphic unity" quote is corroborated but its retrieved page is a content-farm — re-verify before quoting verbatim (it establishes the Collage-Real boundary, not this register); a couple of legal sources (SSRN/JOLT PDFs, one 403 lay-legal blog) are real but not fully fetched — the load-bearing legal citations ([L1] Creative Commons + [L3] Circular 33) were both fetched. No load-bearing craft claim rests solely on an unverified page.
- **`stevelowtwait.com` TLS note:** the Hey Arnold BG mechanic (acrylic + colored pencil) comes from Google's indexed snippets of the artist's own site (a TLS cert mismatch blocked a deep fetch), corroborated across two independent search passes — treat the specific media claim as solid-but-snippet-sourced.

---

## 9. Bibliography

All accessed **2026-07-13**. Prefix key: **[C]** = cast/line cluster, **[T]** = two-media split cluster, **[W]** = painted-world cluster, **[L]** = legal/genericization.

**Cast, line & flat cel:**
- **[C1]** *Line Boil* — TV Tropes — https://tvtropes.org/pmwiki/pmwiki.php/Main/LineBoil — boil definition, "impossible to draw the same line twice," the aesthetic-vs-sloppy/"statues" reframe. *(Full fetch 403'd; content from the search-index excerpt, which quoted the page.)*
- **[C2]** *Understanding the 'Boil' Effect in Animation* — Paper Animation — https://paper-animation.com/blog/understanding-boil-effect-animation — "vibrating energy," the three perceptual payloads, 12fps reads more authentic.
- **[C3]** *Bill Plympton* — Wikipedia — https://en.wikipedia.org/wiki/Bill_Plympton — "alternate them back and forth… shimmering… feel alive"; strong static poses over classic principles.
- **[C4]** *Ed, Edd n Eddy* — Wikipedia — https://en.wikipedia.org/wiki/Ed,_Edd_n_Eddy — "boiling line created by tracing off a drawing three times," held cels swapped for boil, Antonucci "helps keep the characters alive."
- **[C5]** *Inking Advanced pt 1 — Logical Line Weights* — John Kricfalusi (John K Stuff) — http://johnkstuff.blogspot.com/2008/11/inking-advanced-pt-1-logical-line.html — three-level weight hierarchy, heaviest outer silhouette, "every line should mean something." *(Primary animator craft.)*
- **[C6]** *What the 'UPA Style' Actually Is* — Animation Obsessive — https://animationobsessive.substack.com/p/what-the-upa-style-actually-is — flat graphic icons, unmodulated by shadow, movement "based on feelings rather than anatomy."
- **[C7]** *United Productions of America — Biography* — Cooper Hewitt, Smithsonian — https://collection.cooperhewitt.org/people/1108826279/bio — "simplified shapes, bold colors unmodulated by rounding effects or shadow."
- **[C8]** *"Less Precise But More Emotional": Cartoon Saloon and WolfWalkers* — The Roarbots — https://theroarbots.com/less-precise-but-more-emotional-cartoon-saloon-goes-4-for-4-with-wolfwalkers/ — clean-up crew as "comic-book inkers" expressing emotion through the line.
- **[C9]** *Cel Shading* — Wikipedia — https://en.wikipedia.org/wiki/Cel_shading — flat color + hard shadow definition; the load-bearing cel-shading-simulates-3D vs flat-design-avoids-volume distinction.
- **[C10]** *Creating Character Silhouettes and Shapes* — Fiveable (2D Animation) — https://library.fiveable.me/2d-animation/unit-13/creating-character-silhouettes-shapes/study-guide/1oo2tSb8S1byAuIV — silhouette-must-read-in-black test; shape language communicates traits.
- **[C11]** *Animation Boil* — Jonti Rudd — https://www.jontirudd.com/post/animation-boil — boil update "every 4 frames or so," "handmade rustic feel."
- **[C12]** *Traditional animation* — Wikipedia — https://en.wikipedia.org/wiki/Traditional_animation — "on twos" = 12 unique drawings/sec; revert to ones for fast motion.
- **[C13]** *How to Draw Pictures Part 4: Line Thickness* — Aaron Hertzmann (+ Clip Studio Tips) — https://aaronhertzmann.com/2021/05/19/how-to-draw-line-thickness.html — interior strokes thinner than silhouette; pressure-taper "thin→swell→snap"; uniform weight is the vector tell.

**The two-media split:**
- **[T1]** *What is Cel Animation? History, Process, and Examples* — Cloud Animations — https://www.cloudanimations.com/blog/what-is-cel-animation/ — the two-media apparatus (flat cels over separately painted backgrounds); flat color + bold outline as the native character look.
- **[T5]** *Artist Eyvind Earle Made Disney's 'Sleeping Beauty' Enchanting—and Nearly Impossible to Animate* — Artsy — https://www.artsy.net/article/artsy-editorial-artist-made-disneys-sleeping-beauty-enchanting-impossible-animate — Geronimi "who's going to look at all that"; airbrushed so backgrounds "wouldn't compete with the animation"; light rations detail; geometric shapes not gradients. *(Corroborated: Walt Disney Family Museum, waltdisney.org/blog/eyvind-earle-artistic-devotion-distinction-sleeping-beauty.)*
- **[T6]** *Animation Principles: Staging* — Wave Motion Cannon — https://wavemotioncannon.com/2017/05/27/animation-principles-staging/ — silhouette test, value flat-pass, positive/negative-space figure-ground doctrine.
- **[T7]** *An interview with Cartoon Saloon's Tomm Moore* — Skwigly — https://www.skwigly.co.uk/tomm-moore/ — Moore/Cartoon Saloon flat-decorative 2D philosophy. *(Primary interview.)*
- **[T8]** *Song of the Sea (2014 film)* — Wikipedia — https://en.wikipedia.org/wiki/Song_of_the_Sea_(2014_film) — flat 2D characters + watercolour backgrounds; watercolour research trips; "timelessness/organic feel" rationale.
- **[T9]** *Inside the Look of 'Wolfwalkers' with Sandra Andersen* — Animation Obsessive — https://animationobsessive.substack.com/p/inside-the-look-of-wolfwalkers-with — two-art-directions conceit; characters must not move "like cutouts."
- **[T10]** *Cartoon Saloon: Running With Wolves in Wolfwalkers* — VFX Voice — https://vfxvoice.com/cartoon-saloon-running-with-wolves-in-wolfwalkers/ — character-designed-to-stand-out (Robyn's hood), transition zones, woodcut vs watercolour split.
- **[T11]** *Behind the scenes of the beautiful, hand-animated 'Wolfwalkers'* — Frame.io Insider (Mullery interview) — https://blog.frame.io/2021/05/03/made-in-frame-wolfwalkers/ — baked-in print-offset / chromatic aberration as an optical unifier; preserved pencil/charcoal underdrawing. *(Primary crew interview.)*
- **[T13]** *The Art of Over The Garden Wall* — Character Design References — https://characterdesignreferences.com/art-of-animation-9/art-of-over-the-garden-wall — Nick Cross painterly storybook backgrounds; Doré/Shishkin/Cady refs; autumnal palette.
- **[T14]** *The Look of 'Over the Garden Wall'* — Animation Obsessive — https://animationobsessive.substack.com/p/the-look-of-over-the-garden-wall — Cross's cinematic light as the unifier "enveloping" the flat cast "rather than competing."
- **[T15]** *Hey Arnold! Backgrounds* — Steve Lowtwait — http://stevelowtwait.com/hey-arnold-backgrounds — dense vintage urban painted backgrounds under a flat cast; the busy-grimy-world proof.
- **[T16]** *Terry Gilliam's unusual animated collages* — Pixartprinting — https://www.pixartprinting.co.uk/blog/terry-gilliams-unusual-animated-collages/ — cutout collage, "embrace the limitations," visible-seam friction as content. *(Corroborated: Open Culture BBC 1974 how-to.)*
- **[T17]** *The Amazing World of Gumball — Art Styles & Animation* — Shapes.inc — https://shapes.inc/fandom/the-amazing-world-of-gumball/art-styles — stylized cast against photographic/live-action plates; "a show without graphic unity." *(⚠ content-farm source; quote corroborated but re-verify. Establishes the Collage-Real boundary, not this register.)*

**The painted world:**
- **[W1]/[W4]** *Hey Arnold! Background Designs / Backgrounds* — Steve Lowtwait — http://stevelowtwait.com/blog/hey-arnold-background-designs · http://stevelowtwait.com/hey-arnold-backgrounds — acrylic paint + colored-pencil texture; urban-grunge object inventory; design→layout→paint. *(Primary BG artist; TLS-blocked deep fetch, snippet-sourced + corroborated.)*
- **[W5]** *Cartoon Saloon: Running With Wolves in Wolfwalkers* — VFX Voice — (same as [T10]) — woodcut town / watercolour forest; print-degradation weathering; character-keyed-to-environment.
- **[W6]** *'Wolfwalkers': How Cartoon Saloon Created a Gamechanger* — IndieWire — https://www.indiewire.com/awards/industry/wolfwalkers-cartoon-saloon-oscar-nomination-animation-1234626601/ — hand-crafted/physical-media philosophy; woodcut-town inspiration.
- **[W7]** *Cartoon Saloon: Unique Animation Techniques and Visual Style* — Indigo Music — https://indigomusic.com/feature/cartoon-saloon-unique-animation-techniques-and-visual-style — flat-decorative, layered/textured, folk/Celtic warmth thesis.
- **[W9]** *Craig of the Creek — BG Paint* (Carolyn Ramirez portfolio) — https://carolynramirez.carbonmade.com/projects/7223737 — line + flat-grey blocking then painted-over; earth-toned cast vs green world. *(Portfolio blurb, lightly sourced.)*
- **[W10]** *Mary Blair* — Illustration History — https://www.illustrationhistory.org/artists/mary-blair — gouache/tempera, flat simplified shapes, "snappy" unified color; Little Golden Books.
- **[W11]** *The Art of Alice and Martin Provensen* — https://books.google.com/books/about/The_Art_of_Alice_and_Martin_Provensen.html?id=fiA5EAAAQBAJ — flat gouache picture-book illustration, soft palette.
- **[W12]** *The Snowy Day* — Wikipedia — https://en.wikipedia.org/wiki/The_Snowy_Day — collage of patterned paper/oilcloth, hand-stamps, India-ink toothbrush spatter; flat rectangular-cutout city.
- **[W13]** *The Snowy Day and the Art of Ezra Jack Keats* — Skirball Cultural Center — https://www.skirball.org/museum/snowy-day-and-art-ezra-jack-keats — corroborates the collage/urban technique + sparse graphic city.
- **[W14]** *Insular Style of The Secret of Kells* — guriguriblog (+ Celtic art, Wikipedia) — https://guriguriblog.wordpress.com/2009/09/21/insular-style-of-the-secret-of-kells/ — interlace/knotwork ornament worked into backgrounds as folk-decorative structure.
- **[W15]** *Painting During the Golden Hour* — Artists Network — https://www.artistsnetwork.com/magazine/painting-during-the-golden-hour/ — analogous warm-earth palette (yellow ochre / burnt sienna / cad-red-light), long shadows, soft contrast.
- **[W16]** *Color Script in Animation: Mood, Tone & Storytelling* — Brink Helsinki — https://brinkhelsinki.com/logs/color-script-in-animation/ — mood-keyed color, desaturated local color + saturated light, warm=comfort emotional coding.
- **[W17]** *The Golden Hour* — Gurney Journey (James Gurney) — http://gurneyjourney.blogspot.com/2008/01/golden-hour.html — warm-light/cool-bluish-shadow mechanic, single-source unification, atmospheric temperature depth. *(Primary craft, fetched.)*
- **[W18]** *Creating Textures and Dimension with Gouache* — Ceciley Adro (+ Mont Marte "10 gouache techniques") — https://cecileyadro.com/creating-textures-and-dimension-with-gouache/ — dry-brush, hatch, stipple, sgraffito/scraping, rag-lifting surface verbs.
- **[W19]** *An Introduction to Gouache Techniques* — Manda Comisari / Counter Arts — https://medium.com/counterarts/an-introduction-to-gouache-techniques-650c0f1b43ed — corroborates dry-brush/hatch/layered-wash weathering technique.

**Legal / genericization:**
- **[L1]** *The Complex World of Style, Copyright, and Generative AI* — Creative Commons — https://creativecommons.org/2023/03/23/the-complex-world-of-style-copyright-and-generative-ai/ — "style alone is not usually the subject matter of copyright"; genre analogy; style as a non-determinative ingredient of substantial similarity. *(Fetched.)*
- **[L2]** *Copyrighting Style* — Christopher Buccafusco (SSRN) — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5198346 — style as "both idea and expression"; a proposed dual-copying test. *(Abstract-level; full text not fetched.)*
- **[L3]** *Circular 33: Works Not Protected by Copyright* — U.S. Copyright Office — https://www.copyright.gov/circs/circ33.pdf — authoritative list of unprotected subject matter (ideas, methods, familiar symbols/designs). *(Fetched.)*
- **[L4]** *Idea–expression distinction* — Wikipedia (orienting; cite *Nichols v. Universal Pictures*, 1930, as the primary authority) — https://en.wikipedia.org/wiki/Idea%E2%80%93expression_distinction — well-developed characters are protectable; the boundary is famously unfixable.
- **[L5]** *Elements of Style: Copyright, Similarity, and Generative AI* — Benjamin L.W. Sobel — Harvard JOLT v38 — https://jolt.law.harvard.edu/assets/articlePDFs/v38/2-Sobel.pdf — style vs similarity in the generative-AI era. *(Real PDF; not fully fetched.)*

---

## 10. The wire-ready outputs (index)

Per the playbook, Step R produces four wire-ready outputs — all present above:
1. **Draft `RegisterSpec`** — §2 (table + candidate Python).
2. **Cy `Example F` block** — §3 (three `IR.trashcat.*` + four-paragraph risk-bible).
3. **`refs/` policy + bibliography** — §9 + [`refs/README.md`](refs/README.md) (empty of third-party frames; hero locked at Step S).
4. **Transport record** — §4 (`GPT_IMAGE` provisional / `NB_PRO` final / unwired-fails-loud; NB2 spike is the Step-S decision).

Ends at `RESEARCH RATIFIED BY SEAN (2026-07-13) — LOOK SPIKE PENDING`.
</content>
</invoke>
