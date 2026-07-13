# `samurai-jack-s5` — register research

**Date:** 2026-07-11 · **Consumer:** GRANDMASTER (revised style/identity-hold fallback — a committed future style, one of Sean's two go-to registers; see the [ratified plan](../../docs/active/2026-07-11-samurai-jack-s5-register-design.md) §2B/§2D) · **Status:** **LOOK RATIFIED — HERO LOCKED — READY TO AUTHOR (2026-07-13).** Human Checkpoint 1 passed ("this works") + Human Checkpoint 2 passed — Sean picked one hero by eye across a cross-engine spike (ChatGPT gpt-image + NB2 + the Higgsfield `gpt_image_2` prompt-ladder run; his eye the sole arbiter, no LLM judge). The locked hero is `refs/samurai-jack-s5-hero.png` (= `refs/spike-2026-07-11/beta_3_flat.png`, Higgsfield `gpt_image_2`, 2688×1520, md5 `4010abff22a542046286d0e6d4a7af53`); full provenance + the retained spike spread + the aspect-ratio call (**16:9, letterbox optional**) are in [`refs/README.md`](refs/README.md). A live composition-phrase A/B (2026-07-13) ratified **keeping all five money-phrases** in the injected clause (see §1). The authoring build (Step B) is now cleared. **NOT YET authored into `pipeline/registers.py` — that is Step B.**

**Method:** four parallel deep-research subagents (line & shading / no-outline logic · palette & lighting · composition, form & timing · signature tells, negative controls, genericization & bibliography), synthesized here into the four wire-ready outputs the [animation-vocabulary-expansion plan](../../docs/active/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md) §2a requires, plus its depth requirements (frame-by-frame still analysis, composition & staging grammar, the paint *process*, negative controls, the genericization rule). Research answers *"what makes the look the look,"* grounded in primary craft sources (Tartakovsky and crew interviews; art-director Scott Wills; co-art-director Dan Krall; production commentary), never surface pastiche. The real-world reference is the final season (Season 5, 2017 Adult Swim/Toonami) of *Samurai Jack*, and the flat-graphic school it belongs to — **studied as a school of craft, captured attribute-only; never the show, the cast, or the frames** (§7).

**The register in one line:** the **flat cinematic poster-art** school — clean flat color shapes with almost no visible outlines, forms read through adjacent color and value contrast, hard-edged flat shadow shapes, dramatic negative space, a single emotional color cast, staged with silent-samurai-film clarity. It is the **mutually-exclusive flat sibling of `primal-sketch-grit`**: same director, same colorist, opposite *surface* (§6).

---

## 0. Corrections to the thin seed's craft baseline — the claim ledger

The seed research (`docs/research/samurai-jack-season-5-art-style-description.md`) is a single unsourced ChatGPT pass — an adjective list, a prompt template, and the magic phrase. It was the research **input**, not its output. Every load-bearing claim below is now web-verified against primary/secondary sources; **nothing rests on the seed alone.** The register is authored against this ledger, not the pre-fill.

| # | Thin-seed assertion | Verdict | Source(s) | Note |
|---|---|---|---|---|
| 1 | "clean flat color shapes" | **Confirmed** | Tartakovsky making-of quote (Better Posters [B3]); Animation Obsessive "Visual World" [B1] | "If it's a white robe, you just see the white shape" — direct creator doctrine. |
| 2 | "almost no visible outlines / avoids conventional black outlines" | **Confirmed, with a named exception** | Better Posters [B3] (verbatim Tartakovsky "took the line completely off"); Dot and Line [B6] | Exception: thin black lines persist **only around eyes and a few facial features** (interior detail, not contour). "Color holds" carry any other line. |
| 3 | "relies on shape contrast, color blocking, sharp value separation to define forms" | **Confirmed** | Dot and Line [B6] (Christen Smith); Animation Obsessive [B1] (Krall) | Krall's "Jack's nose disappears against the sky" quote proves color/value contrast IS the edge mechanism — and names its failure mode. |
| 4 | "hard-edged shadow shapes / flat shadow shapes" | **Confirmed as practice; NOT quoted doctrine** | Reconstruction from legally-viewable stills + reviews ([B10]–[B12]); repo Primal negative-control table | No crew member is on record stating a shadow-edge rule. Abundantly visible; flag as reconstruction (§9). |
| 5 | "restrained facial detail" | **Confirmed** | Better Posters [B3]; Dot and Line [B6] | Faces are shape-built; interior line is minimal and localized to the eyes. Emotion is carried by silhouette/posture, not face-acting. |
| 6 | "sharp angular silhouettes / angular planes" | **Confirmed as design language; "angular" is critic-vocab not crew-vocab** | canmom [B7] ("clear geometric shapes"); CGWire shape-language [B16] | Crew vocabulary is "graphic / stylized / designed." Keep "angular" as attribute language; don't cite it as a crew quote. |
| 7 | "long elegant proportions / stylized anatomy" | **Unsupported (elegance/heads-tall); "stylized/silhouette-first" Confirmed** | canmom [B7]; Dot and Line [B6] | **No source gives a heads-tall ratio or "long elegant proportions."** Silhouette-first, shape-built figures are sourced; the *elegance* phrasing is seed language. Author proportions per-character (SF03), not as a register constant. |
| 8 | "painterly but simplified atmospheric backgrounds" (figure/BG split) | **Confirmed and sharpened** | Animation Obsessive "How They Painted" [B2]; IndieWire/Yahoo [B5] | Figures flat cel-color; backgrounds carry the texture/atmosphere — painterliness disciplined *inside* hard-edged designed shapes. Original run = physical Cel Vinyl + airbrush; S5 = digital (TVPaint) with Wills' hand-mimicking brushes. |
| 9 | "limited palette dominated by a single emotional color cast" | **Confirmed, mechanism sharpened** | Dot and Line [B6]; Animation Obsessive [B1]; reviews [B10]–[B12] | The *stated* doctrine is per-scene mood-first palette + anti-naturalism ("no green grass, no blue sky"). Because figures are **lineless**, figure and field are forced into one designed palette — the structural reason a scene reads as one cast. Whole-frame single-cast floods (red cave, white snow, gray rain) are a verified S5 device but not a *quoted* law (§9). |
| 10 | "hard rim light" | **Unsupported as doctrine** | — | No source names rim/backlight. S5's documented moves are darkness + single-source + full silhouette. Prefer "stark value silhouette against the lit field" over "rim light" (§9). |
| 11 | "high-contrast lighting / stark silhouettes" | **Confirmed** | Animation Obsessive [B1] (Wills "cinematic lighting… feel stylized"); reviews [B10]–[B12] | Also *structurally forced*: lineless figures vanish without value separation. |
| 12 | **"2.39:1 cinematic letterbox"** | **CORRECTED → 1.78:1 (16:9)** | Wikipedia S5 [B8] (aspect ratio 1.78:1); Nerdist Blu-ray review [B15] ("full native HD… 1.78:1") | **S5 aired native 16:9, NOT 2.39:1.** "Cinemascope" appears in criticism [B9] as a *compositional adjective*, not a delivery format. The 4:3 original run used in-frame letterbox bars as a stylistic device. **This corrects the plan's §2C/Appendix "2.39:1" assumption** — the spike targets **16:9**; letterbox bars are an optional *declared homage*, not the register's format (§5.7, §10). |
| 13 | "long horizontal compositions, huge empty skies / tiny figure in a vast landscape" | **Confirmed** | Wikipedia S5 reception [B8] (Jack "dwarfed by the grand solemnity of nature… undercurrent of loneliness"); Animation Obsessive [B1]/[B2] | Deliberate scale-isolation is critic-observed for S5 specifically. No numeric empty-field ratio exists in any source (§9). |
| 14 | "backgrounds treated like cinema landscapes / environment as a character" | **Confirmed (strongest pillar)** | Animation Obsessive [B1]/[B2] (direct Tartakovsky quotes) | Quoted, not reconstructed — modeled on David Lean (*Lawrence of Arabia*) and Kurosawa. |
| 15 | "poses held like comic panels, then action erupts in sudden bursts" | **Confirmed (timing — for Bea/Mo)** | canmom [B7]; Animation Wiki [B14]; Fatherly [B13] | Move→hold→burst, triangulated. A *timing* tell, shared career-wide (not a still-frame discriminator) — §8. |
| 16 | "stylized sword fights, slow dialogue-free passages, classic samurai-film framing" | **Confirmed** | canmom [B7] (jidaigeki/chanbara); Rotten Tomatoes editorial [B_RT] (Tartakovsky: S5's "silent sequences" begat *Primal*) | "Silent samurai-film staging" is well-grounded. Note: *Primal* is the **more** silent show ([B_CBR]) — do not carry "more silence than Primal" as a discriminator (§9). |
| 17 | "mid-century modern / UPA-like graphic quality" | **Confirmed with refinement** | Animation Obsessive UPA [B4]; "How They Painted" [B2] (Wills names Charley Harper) | UPA lineage is on record — but it lives in **shape design + limited-animation timing**, not the linelessness (Tartakovsky traces that to '50s Disney/*Sleeping Beauty*/Golden Books/Toei). Encode UPA as *one ancestor*, not the register's definition (§6). |
| 18 | "where Primal feels like rough pulp illustration, Samurai Jack feels like animated poster art" | **Confirmed in substance; the phrase is a coined metaphor** | Dot and Line [B_DL] (Primal's Bakshi/'70s-sci-fi/pulp lineage); Animation Obsessive [B2] (crew's own "Japanese prints and posters" reference) | The pulp-vs-poster contrast is real and sourceable axis-by-axis; "animated poster art" is not a sourced phrase — use as characterization, not quotation. |
| 19 | "S5 = 2017 Adult Swim/Toonami revival, 10-episode darker conclusion" | **Confirmed** | Wikipedia S5 [B8]; Vice [B_Vice] | Mar 11–May 20 2017; 10 episodes; ~50-year time-skip; TV-14 (vs original Y7); 100% Rট. |
| 20 | (implicit) "Bryan Andrews directed S5" | **CORRECTED** | Wikipedia S5 [B8] | **Tartakovsky directed all 10 S5 episodes.** Andrews storyboarded + co-wrote several. Say "storyboarded by," never "directed by" — matters only for accurate sourcing, not the register. |

**Attribution correction propagated (§9 flag 1):** the Tartakovsky "we kept the line-work over the color, which was very new for us" quote (Primal) is **verbatim** [B_DL]. The companion "all marks from the hand-drawn process were rendered out" line (Samurai Jack) is a **journalist's paraphrase** in the Yahoo/IndieWire article [B5], *not* a direct Tartakovsky quote (verified by fetch). The sibling `primal-sketch-grit/research.md` §0 cites it quote-like; that is an **errata candidate** to fix at the cross-link step (plan Task 5). It does not change the finding — the per-axis inversion is the creators' *stated intent* (Primal's line choice was made specifically to differentiate it from Jack's rendered-out flatness), corroborated independently by the no-black-outlines doctrine [B1]/[B3].

---

## 1. Output 1 — the draft RegisterSpec (proposed; authored into `pipeline/registers.py` only on Sean's greenlight)

Refined from the plan's Appendix A against the research. **The asserted money-phrases are preserved** (the per-register test asserts them as substrings): `almost no visible outlines`, `hard-edged flat shadow`, `single emotional color cast`, `dramatic negative space`, `silent-samurai-film staging`. The models, marker uniqueness, and the mutual-exclusion vs primal are preserved.

| Field | Value | Sourcing |
|---|---|---|
| `name` | `samurai-jack-s5` | The machine slug — the sole permitted franchise-derived identifier; internal, never a production-prompt string (§7). |
| `summary` | Flat cinematic poster-art register. Clean outline-sparse color shapes, hard-edged flat shadow masses, dramatic negative space, and one emotional color cast staged with silent-film clarity. | §§5.1–5.7 |
| `identity_lock` | Match the face, hair, color palette, proportions, and silhouette of Image 1 exactly. Simplification may remove interior detail but must preserve the character's unique silhouette, facial landmarks, and long-axis proportions **as readable flat shapes** — because with almost no outline, the silhouette and the figure/ground value break are the *only* things carrying identity. | The no-outline doctrine [B1]/[B3]/[B6] + the silhouette-first finding (§5.4) |
| `preserve` | Keep clean flat color shapes with almost no visible outlines; define edges through adjacent color and value contrast. Keep hard-edged flat shadow shapes, restrained facial detail, dramatic cinematic negative space, and one dominant emotional color cast across figure and setting. No soft airbrushed modeling, no rendered volumetric shading, and no busy interior detail that weakens the silhouette. | §5.1, §5.3, §5.5, §6 |
| `style_token` | "Dark minimalist cinematic 2D poster-art still: clean flat color shapes, almost no visible outlines, sharp angular silhouette, long elegant proportions, hard-edged flat shadow shapes, bold value blocking, dramatic negative space, a single emotional color cast, and silent-samurai-film staging." | §§5.1–5.7; the chanbara/Kurosawa/Leone + UPA/Charley-Harper lineage |
| `generation_model` | **`GPT_IMAGE` (`gpt-image-2`) — unwired; fails loud via `UnwiredTransportError` until a runner is wired** (the existing `SUPPORTED_IMAGE_MODELS` allowlist guard already covers it — no new code). The proof frame (`images/samuria-first-pose-chatgpt.png`, Sean's own gpt-image gen) demonstrates the register renders clean on gpt-image (near-silhouette figure, vast muted-amber sky, hard-edged flat shadow shapes, dramatic negative space). | §4 |
| `final_model` | `NB_PRO` — the dormant painterly-final seam convention (no consumer yet; same as watercolor/photoreal/3d/primal/nicktoon). | Registry convention |
| `markers` | `samurai-jack-s5` (the name) · `outline-sparse flat color shapes` · `hard-edged flat shadow masses` · `single emotional color cast` · `dramatic cinematic negative space` · `silent-samurai-film staging` | §5 tells; collision-checked against all 8 existing registers' markers (plan §4 — clean) |
| `stub_keywords` | `("samurai",)` — the **genre word** (chanbara; parallel to primal's "70s-pulp"), single, low-false-match, appended AFTER the legacy six + `primal` + `nicktoon`/`grossout` (precedence oracle-pinned) | §7 (genre is free); Task 2 |
| `reference_images` | **default `()`** — no code reads `spec.reference_images` (plan §4.1, red-team fold); the locked hero + provenance live in `refs/README.md` + this doc. | Matches all 8 existing registers |

**Deliberate prompt-authoring choice (mirrors primal §1 / nicktoon §1):** `preserve` names **only samurai's positives + generic anti-over-rendering refusals**. It does **not** name pencil's, primal's, or line-art's vocabulary as negatives — naming a neighbor register can evoke it in the image model (doctrine). It contains **none** of the six forbidden substrings the per-register test guards (`cream paper`, `graphite`, `cross-hatch`, `weight-varying ink`, `over the color`, `gritty`). Pencil/primal/line-art/UPA drift-policing lives in the Cy risk-bible (§2), exactly as it does for the two siblings.

**Candidate Python (research-refined; the build's `RegisterSpec` source — matches Appendix A fields):**

```python
RegisterSpec(
    name="samurai-jack-s5",
    summary=(
        "Flat cinematic poster-art register. Clean outline-sparse color shapes, "
        "hard-edged flat shadow masses, dramatic negative space, and one "
        "emotional color cast staged with silent-film clarity."
    ),
    identity_lock=(
        "Match the face, hair, color palette, proportions, and silhouette of "
        "Image 1 exactly. Simplification may remove interior detail but must "
        "preserve the character's unique silhouette, facial landmarks, and "
        "long-axis proportions as readable flat shapes."
    ),
    preserve=(
        "Keep clean flat color shapes with almost no visible outlines; define "
        "edges through adjacent color and value contrast. Keep hard-edged flat "
        "shadow shapes, restrained facial detail, dramatic cinematic negative "
        "space, and one dominant emotional color cast across figure and setting. "
        "No soft airbrushed modeling, no rendered volumetric shading, and no "
        "busy interior detail that weakens the silhouette."
    ),
    style_token=(
        "Dark minimalist cinematic 2D poster-art still: clean flat color shapes, "
        "almost no visible outlines, sharp angular silhouette, long elegant "
        "proportions, hard-edged flat shadow shapes, bold value blocking, "
        "dramatic negative space, a single emotional color cast, and "
        "silent-samurai-film staging."
    ),
    generation_model=GPT_IMAGE,
    final_model=NB_PRO,
    markers=frozenset({
        "samurai-jack-s5",
        "outline-sparse flat color shapes",
        "hard-edged flat shadow masses",
        "single emotional color cast",
        "dramatic cinematic negative space",
        "silent-samurai-film staging",
    }),
    stub_keywords=("samurai",),
    # reference_images left default () — no code reads it (red-team fold).
),
```

---

## 2. Output 2 — the Cy block (draft `### Example E — ronin`)

Proposed **Example E** for [`pipeline/agents/prompts/cy-character-designer-context.md`](../../pipeline/agents/prompts/cy-character-designer-context.md) (added at authoring): three sample `IR.ronin.*` entries + a four-paragraph risk-bible excerpt, in the register's own vocabulary. **Categories verified against `criteria.py`'s `VALID_IR_CATEGORIES`** (`anatomy, hair, face, proportion, palette, costume, prop, pose, motion, style, view`) — this register's signature axes (composition, staging, negative space) are **NOT** IR categories, so they live in the risk-bible prose and the timing bible (§8), never as an invented `staging` rule.

**Three sample `IR.ronin.*` (the load-bearing trio):**
- `IR.ronin.style.outline-free-color-boundaries` — the figure carries almost no drawn contour; every edge between the figure and its surroundings (and between forms within the figure) is a deliberate **hue or value break between adjacent flat color shapes**. A frame where a black outline fences the figure, OR where the figure and its background land the same value and the silhouette dissolves ("the nose disappears against the sky"), fails.
- `IR.ronin.palette.single-emotional-cast` — figure, shadow, and setting are keyed to **one** dominant scene cast (moonlit blue / ember amber / cold-gray rain / blood red); the base is muted and non-naturalistic ("no default green grass, no default blue sky"), with at most one small lurid accent. Naturalistic local color, or a figure lit *against* the cast instead of keyed *into* it, is a defect.
- `IR.ronin.proportion.angular-graphic-silhouette` — the figure is built from clean angular graphic shapes that read as one instantly-legible silhouette; identity survives at the pose extreme because the silhouette is preserved. *(Heads-tall is authored per-character at Bible-lock via SF03 — the register does NOT impose a canonical ratio; §9 flag.)*

**Additional wire-ready `IR.*` drafts the Bible pass can draw on:**
- `IR.{char}.style.hard-flat-shadow-shape` — where a shadow appears on the figure, it is a **single hard-edged flat shape** in a darker step of the scene's cast (poster-style mask), never a soft gradient or airbrushed falloff. At dramatic peaks the figure may drop to a full one-color silhouette with no interior shadow at all.
- `IR.{char}.palette.value-silhouette-contrast` — every frame reads as a clear value silhouette: a light figure on a dark field or the inverse, never mid-value on mid-value (the structural rule that keeps a lineless figure legible).
- `IR.{char}.style.restrained-face-detail` — interior facial line is minimal, held to the eyes and one or two reading-critical features; expression is delivered by silhouette, posture, and eye-direction, not rendered face-acting.
- `IR.{char}.face.eye-line-exception` — the one place a thin dark line legitimately survives the outline ban is around the eyes / a few facial features; everywhere else, contour is a color/value boundary.

**Risk-bible excerpt (four paragraphs, for Example E):**
1. **Drift directions.** Four pulls, each toward a named neighbor's *attributes* (never named in the prompt): (a) toward **heavy ink / gritty painterly texture** — a visible weight-varying contour laid over the color, grit on the figure — which is the flat sibling's register and collapses the "no outline / clean flat shape" identity; (b) toward **glossy 3D or anime rendering** — smooth airbrushed volume, specular sheen, rendered depth — which kills the poster flatness; (c) toward **bold uniform outlines** — a clean even keyline fencing every shape (the all-outline opposite of "almost no outline"); (d) toward **flat-but-decorative modernist** graphics — flat and geometric but bright, non-cinematic, and un-atmospheric, missing the dramatic negative space, the single emotional cast, and the painterly-atmospheric backgrounds under the flat figures. The register lives in the tension between *lineless flat figures* and *cinematic, mood-flooded, negative-space staging*; lose either and it collapses.
2. **What simplification cannot sacrifice about identity.** Because the figure carries almost no outline, the **silhouette is the identity** — the unique shape of the head, hair-mass, stance, and long-axis proportion must survive every simplification, and the figure/ground value break must be engineered as a *pair* (the character's local colors chosen against the specific field behind them) so the character never dissolves into the background. If the silhouette reads as this exact character with the interior detail stripped, it holds; if identity lived in fine facial rendering, it was never in-register.
3. **Where the research is thin.** Several load-bearing attributes are reconstructions from stills + reviews, not quoted studio doctrine: the **hard-edged flat shadow-shape rule** (visible everywhere, stated nowhere), **rim light** (unsupported — prefer "stark value silhouette"), the **single-whole-frame cast as a law** (the sourced doctrine is per-scene color-key scripting + anti-naturalism; the whole-frame flood is a verified recurring device), and **heads-tall / "long elegant proportions"** (unsourced — author per character). Treat these as authoring guidance, not canon; frame-check against the locked hero.
4. **The three binary human-review checks.** (i) Do forms read **without** black outlines — via flat shape + value contrast — with the silhouette clean and separated from the field? black-outlined or value-camouflaged → outline/contrast fail. (ii) Is the frame keyed to **one** emotional color cast with a muted non-naturalistic base (at most one small accent), figure and setting unified? naturalistic or multi-cast → palette fail. (iii) Are shadows **hard-edged flat shapes** (or absent, figure→silhouette) with no airbrushed/rendered volume, and is the staging cinematic negative space rather than a busy filled frame? soft-rendered or cluttered → render/staging fail.

---

## 3. Output 3 — `refs/` + bibliography

`refs/` ships **empty of third-party frames by design** ([`refs/README.md`](refs/README.md)): *Samurai Jack* stills, frame-grabs, and artbook scans are copyrighted study material, reasoned about with the sources below, **never committed or fed to generation.** What lands in `refs/` at the look-spike (Step S): the cross-engine spike candidates in a dated `spike-YYYY-MM-DD/` subfolder, and Sean's **one** locked hero frame once the look is picked (Human Checkpoint 2). The register's non-derivative rule (§7): capture the school, never the episode.

**Bibliography** (all accessed **2026-07-11**; each entry names what it supports; no load-bearing claim rests only on the unsourced seed):

- **[B1] "The Visual World of 'Samurai Jack'"** — Animation Obsessive (Substack). https://animationobsessive.substack.com/p/the-visual-world-of-samurai-jack — no-black-outlines doctrine; '50s-Disney/*Sleeping Beauty*/Golden Books/Toei lineage; Krall's "nose disappears against the sky" color-separation quote; Wills "cinematic lighting… feel stylized"; "no green grass, no blue sky"; environment-as-character; UPA/Bobe-Cannon timing; long holds.
- **[B2] "How They Painted the 'Samurai Jack' Backgrounds"** — Animation Obsessive (Substack). https://animationobsessive.substack.com/p/how-they-painted-samurai-jack — physical media (Cel Vinyl, Iwata airbrush, paper-towel texture); "between realism and pure design"; **Charley Harper** as the supreme background influence (mid-century minimal-realism); ~30–50 color keys/episode; Tartakovsky's minute-plus environment-establishing sequences (Lean/Kurosawa/Miyazaki).
- **[B3] "Lessons from Samurai Jack"** — Zen Faulkes, Better Posters blog (May 2013). http://betterposters.blogspot.com/2013/05/lessons-from-samurai-jack.html — **verbatim** Tartakovsky making-of quote: "we took the line completely off… you just see the white shape, you see no linework"; black lines only at eyes/facial features; "color holds."
- **[B4] "What the 'UPA Style' Actually Is"** — Animation Obsessive (Substack). https://animationobsessive.substack.com/p/what-the-upa-style-actually-is — UPA definition (flat icons, backgrounds *more* abstract than characters, Matisse/Klee/Léger, anti-Disney modernism); Tartakovsky "I don't think a week goes by that I don't reference one of their films"; "UPA revival" framing. Grounds the UPA negative control.
- **[B5] "Genndy Tartakovsky on 'Primal,' the Evolution of His Animation…"** — Yahoo Entertainment (IndieWire mirror). https://www.yahoo.com/entertainment/genndy-tartakovsky-primal-evolution-animation-163031835.html — the "all marks from the hand-drawn process were rendered out" sentence (**journalist paraphrase re: Tartakovsky + Wills — not a direct quote**, verified by fetch; §0 / §9); Primal's "gritty 1970s look"; S5 TVPaint + Wills' hand-mimicking brushes; "bolder and more saturated"; Kellman's "heroic and less cartoony" S5 redesign.
- **[B6] "The Elements of Style: 'Samurai Jack'"** — Eric Vilas-Boas, The Dot and Line (Medium). https://medium.com/the-dot-and-line/samurai-jack-design-elements-f7b094176500 — animation professor **Christen Smith** on the lineless figure/ground color-control rule ("without the aid of a line… the colors of the entire scene had to be carefully picked"); harmony/hierarchy/contrast per shot; S5 retained design elements + TV-14.
- **[B7] "Animation Night 35 — Genndy Tartakovsky"** — canmom.art. https://canmom.art/films/animation-night/35-genndy-tartakovsky — "simple graphic shapes… clear geometric shapes"; sharp composition; gesture/timing over volume; jidaigeki/chanbara influence; move-then-pause rhythm / long holds; S5-reception dissent (noted, minority view).
- **[B8] "Samurai Jack season 5"** — Wikipedia. https://en.wikipedia.org/wiki/Samurai_Jack_season_5 — **1.78:1 aspect ratio**; Tartakovsky directed all 10 episodes; Andrews storyboard/co-write credits; Adult Swim/Toonami Mar 11–May 20 2017; 10 episodes; darker/more-mature tone; ~50-year time-skip; the "dwarfed by the grand solemnity of nature" reception quote.
- **[B9] "Samurai Jack Is Probably the Most Beautiful, Inventive Cartoon Ever"** — Patrick Marlborough, Vice. https://www.vice.com/en/article/samurai-jack-is-probably-the-most-beautiful-inventive-cartoon-ever/ — S5 "cinemascope framing of a pastoral skyline"; "shogun road warrior" framing; cross-tradition frame synthesis; restraint-as-punctuation. (Grounds "cinemascope" as a *look*, not the delivery format.)
- **[B10] "Samurai Jack and the Daughters of Aku meet their destiny" (XCIV)** — The A.V. Club. https://www.avclub.com/samurai-jack-and-the-daughters-of-aku-meet-their-destin-1798190797 — all-white snow-battle field; blood-red silhouette at a cave mouth; deliberate echo of the original ninja episode; the introduction of red blood.
- **[B11] "Samurai Jack has a captivating battle with human consequences" (XCIII)** — The A.V. Club. https://www.avclub.com/samurai-jack-has-a-captivating-battle-with-human-conseq-1798190713 — pitch-black catacomb fight lit only by weapon sparks; firefly-lit walk in pure black; the first human blood-spurt; Aku's fiery lair vs earth tones.
- **[B12] "After all these years, Samurai Jack's quest comes to a swift, fitting end" (CI)** — The A.V. Club. https://www.avclub.com/after-all-these-years-samurai-jack-s-quest-comes-to-a-1798191398 — the muted pastoral finale coda; the "vibrant pink" ladybug as the lone saturated accent (accent-against-muted-field as the emotional full stop).
- **[B13] "Why You Should Watch 'Samurai Jack' With Your Kids Right Now"** — Fatherly. https://www.fatherly.com/entertainment/making-of-samurai-jack — Leone extreme-close-up + sparse-movement influence; tension held before action; spaghetti-western + chanbara + Lean inspiration mix.
- **[B14] Samurai Jack — Animation Wiki (Fandom).** https://animation.fandom.com/wiki/Samurai_Jack — comic-book screen framing; in-frame widescreen letterbox bars; split screens; manga-panel devices ("a comic book with occasional sound commentary"). Grounds letterbox-as-in-frame-device.
- **[B15] "SAMURAI JACK's Complete Series Looks Gorgeous in HD"** — Nerdist (Blu-ray review). https://archive.nerdist.com/samurai-jack-complete-series-blu-ray-review/ — S5 native HD **1.78:1** vs seasons 1–4 in 4:3; digital hand-painting. (Confirms the aspect-ratio correction.)
- **[B16] "Character Shape Language"** — CGWire blog. https://blog.cg-wire.com/character-shape-language/ — Jack's "sleek, angular design" as shape-language (secondary craft source for the angular-silhouette attribute).
- **[B_DL] "Genndy Tartakovsky Gets 'Primal'"** — Eric Vilas-Boas, The Dot and Line. https://dotandline.net/genndy-tartakovsky-primal-interview/ — **verbatim** Tartakovsky: "We even kept the line-work over the color, which was very new for us" and "we also wanted it to look different from Samurai Jack" (the mutual-exclusion proof; §6).
- **[B_SW] "Genndy Tartakovsky's PRIMAL: Art Director Scott Wills"** — Sloan Science & Film. https://scienceandfilm.org/articles/3346/genndy-tartakovskys-primal-art-director-scott-wills — Wills: Jack was "a very stylized show with crazy color," Primal "so much more grounded in reality"; "Genndy always wants some crazy color statement that shocks you"; anti-realistic color doctrine (the Primal-side anchor of the color contrast, §6).
- **[B_CBR] "Tartakovsky's Primal Is More Samurai Jack Than Samurai Jack"** — CBR. https://www.cbr.com/primal-is-more-samurai-jack-than-samurai-jack/ — the silence axis: *Primal* is the *more* purely-visual/pre-language show; corrects the seed's "more silence than Primal" (§9).
- **[B_RT] "5 Ways Primal Creator Genndy Tartakovsky Revolutionized Animated Action"** — Rotten Tomatoes Editorial. https://editorial.rottentomatoes.com/article/primal-creator-genndy-tartakovsky-revolutionized-animated-action/ — "a good action sequence is really like a good music sequence"; "I place the camera where I can read the action the clearest"; light-vs-dark value clarity; the silence doctrine + "people loved the silent sequences" S5→Primal bridge (career-doctrine; §8/§9 flag).
- **[B_Vice] Genndy Tartakovsky interview** — Vice (S5). https://www.vice.com/en/article/samurai-jack-genndy-tartakovsky-interview-season-5/ — "We knew we had to make the tone darker… He's breaking down… losing his mind, his hope, his will"; handcrafted-look retained; "the art style has changed a little bit."
- **[B_CGM] "Samurai Jack Season 5 Review"** — CGMagazine. https://www.cgmagonline.com/review/tv-series/samurai-jack-season-5-review/ — S5 "muted grays and moody atmospheres… closer to a graphic novel than a cartoon" (the darker resting register).
- **Copyright / genericization sources** — **[B_CC]** Stephen Wolfson, "The Complex World of Style, Copyright, and Generative AI," Creative Commons (2023), https://creativecommons.org/2023/03/23/the-complex-world-of-style-copyright-and-generative-ai/ (idea/expression dichotomy; "style alone is not usually the subject matter of copyright"; genre uncopyrightable; case-by-case substantial-similarity caveat); **[B_LA]** Greg Kanaan, "You Can't Copyright Style," The Legal Artist, https://www.thelegalartist.com/blog/you-cant-copyright-style ("copyright protects finished works… not… an artist's style"; *Steinberg v. Columbia Pictures*); **[B_Buc]** Christopher Buccafusco, "Copyrighting Style," SSRN, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5198346 (the courts-are-split counterweight); **[B_Chanbara]** "Samurai cinema," Wikipedia, https://en.wikipedia.org/wiki/Samurai_cinema (chanbara = the sword-fight film genre — grounds "samurai-film" as an allowed *genre* term). See §7.

*Sources 403/402'd at fetch (AWN Dan Sarto S5 interview; some TV Tropes recaps; The Verge; The Fandomentals) were triangulated via search snippets + at least one readable corroborating source; no load-bearing claim rests solely on an unread page (§9).*

---

## 4. Output 4 — transport record

**Transport: `GPT_IMAGE` (`gpt-image-2`) generation, `NB_PRO` final — INTENTIONALLY UNWIRED; fails loud.** This is a **recorded decision the research does not reopen** (plan §2B). The register's `generation_model` records `gpt-image-2`; `invoke_image_edit` raises `UnwiredTransportError` at its first line for any model outside the `SUPPORTED_IMAGE_MODELS = {NB2_FLASH, NB_PRO}` allowlist (`gpt-image-2` included), so the guard **already covers it — no new code** (unlike primal's fork #1, which had to add the guard). `final_model` stays `NB_PRO` (the dormant painterly-final seam).

**The evidence (why gpt-image, not NB2):**
- The proof frame `images/samuria-first-pose-chatgpt.png` is Sean's own **gpt-image** generation and it renders the register clean: a near-black near-silhouette figure read entirely by value contrast against a vast muted-amber dusk sky, hard-edged flat shadow shapes (the cast lawn shadow, the flat tree mass), broad flat color fields, and dramatic negative space. No black contour; the figure/ground edge is a pure value break — exactly the money axis.
- **Predicted NB2 miss (the register's hardest-to-prompt core, §5.6):** NB2's failure mode on the flat siblings is to *add* line and *add* rendering — a clean vector keyline fencing the figure, or soft airbrushed volume — which is precisely the two things this register forbids ("almost no outline"; "no rendered volumetric shading"). The outline-free, value-contrast-defined, hard-flat-shadow read is the axis gpt-image nails and NB2 is predicted to miss. This mirrors primal's spike verdict (gpt-image won the grit NB2 couldn't render).
- **Honest framing of the fallback role (plan §2B):** `samurai-jack-s5` is a **style/identity-hold fallback on the *same* unwired transport as primal** — not a transport-safe fallback (the transport-safe fallback stays Route C, `pencil-test-colored`, NB2). What it protects against: a *style* mismatch (the gritty primal look doesn't land for GRANDMASTER, or Sean prefers the cleaner poster look), **and plausibly** a better across-edit identity hold on gpt-image (flat clean shapes carry less high-frequency detail to drift than primal's grit — **recorded as a hypothesis, unvalidated**).

**The instrument is Sean's look-spike (Step S), not a metric.** Cross-engine (ChatGPT gpt-image + Google Flow), his eye the sole arbiter (the eval handbook bars an LLM aesthetic judge on creative quality), using the research-refined vocabulary and the §10 spike prompt. **Wiring an actual gpt-image runner + the across-edit identity validation is DEFERRED and GATED** on a separate, costed, Sean-greenlit GRANDMASTER build. This research (and the authoring build it feeds) does not wire it.

---

## 5. The look, by dimension (the seven-dimension craft account, with the §2a depth)

### 5.1 Line & contour — the outline ban and its one exception

**The constitutional sentence (direct-quoted, high confidence).** Tartakovsky, in an early making-of clip [B3]: *"If you look at cartoons, every character has a black outline around them. For us, we took the line completely off, so if it's a white robe, you just see the white shape, you see no linework around it."* Contour is the boundary between two flat color fields, not a drawn line. **[ATTRIBUTE]**

**How the eye separates figure from ground — the color-hold mechanism.** With no line, the edge is manufactured at the **palette** level: animation professor Christen Smith [B6] — *"Without the aid of a line to define the separation between character and environment,"* the colors of the whole scene must be picked so *"the action doesn't get lost in the backgrounds."* Co-art-director Dan Krall [B1] names the failure mode outright: if a patch of sky comes back *flesh-toned,* *"Jack's nose disappears against the sky because they're the same color."* The generalized rule: **every figure/ground adjacency must carry a deliberate hue OR value break, because nothing else will save it** — which is *why* the standing background rule exists (Wills [B1]: *"no green grass, no blue sky"* — unexpected background color keeps figure palettes separable).

**The one exception (narrow, real).** Thin black lines survive **only around the eyes and a few facial features** [B3] — interior reading-critical detail, not contour. Where any other line appears it is a **color hold** (held to a value related to the fill, not black) [B3]/[B14].

**vs the flat sibling:** this is the exact axis primal *inverts* — primal keeps a *heavy weight-varying ink contour over the color* [B_DL]; this register takes the line completely off. Same director, opposite line decision, made on purpose to tell the two shows apart.

### 5.2 Palette & color logic — the single emotional cast

**Expressionist by standing rule, never naturalistic.** *"No green grass, no blue sky"* [B1]; Wills [B_SW]: *"We always try to do very bold and unexpected colors — basically not realistic."* Color is derived **mood first, location second**; the background is treated as a character [B1]/[B2].

**Limited per-scene palettes are literal production mechanics.** ~30–50 color keys per episode, personally corrected by Wills, overseas painters forced to match the key [B2] — a scene's palette is a designed, *closed* set.

**The linelessness→single-cast causal chain (load-bearing).** Because figures are lineless "blocks of color" that would otherwise blend into the field [B6], figure, shadow, and setting are **palette-engineered together, per scene** — which is the structural reason a frame reads as one unified emotional cast. The seed's "single emotional color cast" is the *observable output* of this pipeline, not a separate rule.

**S5's specific move: a muted-gray noir base with the range widened at both ends.** CGMag [B_CGM]: the original run's bright colors are *"replaced by muted grays and moody atmospheres… closer to a graphic novel than a cartoon."* Simultaneously the S5 look is *"bolder and more saturated, thanks to digital advances"* [B5]. These reconcile (synthesis, §9 flag): the *resting register* is grayer/sadder, while the mood floods and single accents hit harder — a wider gap between the muted field and the one saturated statement. Verified S5 single-accent-against-muted-field signatures: red blood on the all-white snowfield [B10]; the blood-red silhouette at a cave mouth [B10]; firefly points in the black catacombs [B11]; the "vibrant pink" ladybug closing the muted finale [B12].

### 5.3 Shading & render register — the hard flat shadow shape

**Flat tone masks, near-zero gradient modeling on figures.** Wills' stated thesis [B1]: *"combine everything that's good about realistic painting… and everything that's good about [UPA-type] stylization… cinematic lighting, with mood and depth, but at the same time have it feel stylized"* — **cinematic light delivered through stylized means.** In practice: most shots run the figure in flat local color with *no* tone at all; where shadow appears it is a **single hard-edged flat shape** (a darker step of the scene's cast, laid as a poster mask), never a modeled falloff; gradients/airbrush live in the **backgrounds** (skies, atmosphere), not on the figure. At dramatic peaks the figure drops to a **full one-color silhouette** (the [B_Fandomentals] dusk-beam scene: *"the light cast gave equal parts shadow and light, and depending on the characters' location, only one was visible"* — visibility itself is a value decision).

**Honesty:** "hard-edged flat shadow shapes," "2–3 value steps," and "rim light" are **not** in any crew quote — they are reconstruction from stills + reviews (§9). The register asserts them as authoring guidance grounded in the flat-shape/color-hold doctrine; treat step-counts as guidance, and prefer "stark value silhouette against the lit field" over "rim light."

### 5.4 Form & proportion — silhouette-first, shape-built

Figures are built from *"simple graphic shapes… clear geometric shapes, repeating patterns and motifs"* [B7], not Disney volumetric drawing — angular, thick shapes engineered for **unique, instantly-readable silhouettes** [B16]. Expression is carried by **silhouette, posture, and eye-direction, not face-acting** (restrained interior detail; canmom's "immensely strong sense of gesture and timing" compensating for graphic simplicity [B7]). S5 characterizes *by silhouette change* (the redesigned armor/helmet reads "more demonic" — a silhouette move, not a face move).

**Honesty:** **no source gives a heads-tall ratio or "long elegant proportions"** (§9). The figure reads tall/vertical, but the elegance phrasing is seed language; proportions are authored per-character at Bible-lock (SF03), not imposed by the register.

### 5.5 Texture & surface — the disciplined figure/background split

Figures: **flat cel color, no outline, hard flat tone masks only** — no grain, no grit. Backgrounds carry all the texture/atmosphere, but *inside* hard-edged designed shapes: original run = physical Cel Vinyl, airbrushed skies, sponge/paper-towel texture [B2]; S5 = digital (TVPaint) with Wills' brushes *built to mimic hand brushes* — Tartakovsky [B5]: *"The hardest part was trying to make it feel hand-crafted… getting an organic look is difficult."* The shared property that unifies figure and field into one world is the **no-outline, shape-first construction.** This is a **split** treatment — and it is the second thing that separates the register from primal (where figure AND background share one gritty painterly treatment) and from UPA (where backgrounds are *more* abstract than the figures, not more atmospheric).

### 5.6 The flat-color-shape + hard-edged-flat-shadow logic — the register's hardest-to-prompt core

This is the axis gpt-image nails that NB2 is predicted to miss, and the one the spike must prove. Stated as a generation contract:

- **A form is its flat local-color shape.** A white robe is a white shape; a black-clad figure is a black shape. No modeling, no interior rendering — the shape *is* the form.
- **Edges are value/hue breaks between adjacent flat shapes, not lines.** To read a dark figure against a dark field, the register does one of three sourced things (§3 walkthroughs): (1) put the figure in **silhouette against a brighter field** (sky, snow, firelight); (2) **selectively illuminate** — draw only the lit fragment of the form, let the rest merge honestly into black; (3) ride a **single accent color** on the figure (S5: blood-red on black). It never fakes a contour line to solve the problem.
- **Shadow is a hard flat shape or nothing.** A shadow is a second flat color shape (a darker step of the cast) with a hard graphic edge — or the figure drops entirely to one silhouette value. There is no soft falloff, no airbrushed volume, no specular sheen.
- **The whole frame obeys one cast.** Figure, shadow, and setting are keyed together into one emotional color; the base is muted and non-naturalistic; at most one small accent breaks it.

The failure modes to prompt *against* (as attributes, never named neighbors): an added black keyline; airbrushed/rendered volume; a busy, filled, cluttered frame that kills the negative space; naturalistic multi-color local color; a figure lit *against* the cast rather than keyed *into* it.

### 5.7 Composition & staging grammar — the cinematic-poster signature primal does not share

**Frame: native 16:9 (1.78:1)** [B8]/[B15] — **NOT 2.39:1** (the seed/plan's assumption; corrected §0 #12). S5 was the first widescreen season (1–4 were 4:3). "Cinemascope" [B9] is a *compositional look*, achieved inside 16:9; the original run's stylistic **in-frame letterbox bars / split screens / manga-panel layouts** [B14] are an optional *declared homage* device, not the delivery format. **The spike targets 16:9** (§10).

**Camera (quoted doctrine, career-wide):** *"I place the camera where I can read the action the clearest"* [B_RT]; predominantly **static/locked** cameras — attention is steered by *which frames are shown*, not by camera moves [B7].

**Environment as a character (quoted — the strongest pillar):** [B1]/[B2] — modeled on David Lean (*Lawrence of Arabia*, "you really feel that desert"), *Doctor Zhivago*, Kurosawa, Miyazaki; Tartakovsky ran *"a minute or two sequence of just establishing environment."*

**Negative space / scale-isolation:** critic-confirmed for S5 — a *"distinctive undercurrent of loneliness,"* Jack *"dwarfed by the grand solemnity of nature"* [B8]. Figure placement swings between **dead-center symmetry** (ritual/meditative beats) and **figure-small-in-the-lower-third** against a huge sky/field (journey beats). **Honesty:** no source gives a numeric empty-field ratio (§9); "the figure occupies well under a quarter of the frame in establishing shots" is guidance from imagery, not doctrine.

**Chanbara / Kurosawa / Leone lineage:** jidaigeki/chanbara framing + Kurosawa silence + Leone standoff-tension and extreme-close-up inserts [B7]/[B13]. This is what "silent-samurai-film staging" means in the register: **stillness before violence, emotion carried by posture, scale, and composition** — the marker is staging, not a franchise reference (chanbara is a genre, §7).

---

## 6. Negative controls (the confusable-adjacent registers)

The load-bearing table — the inverted `primal-sketch-grit` §6 axis, plus `line-art-only` (the all-outline opposite) and UPA/mid-century flat-graphic (the genuinely-close neighbor).

| Axis | **samurai-jack-s5** (this register) | **primal-sketch-grit** (mutually-exclusive flat sibling) | **line-art-only** | **UPA / mid-century flat-graphic** |
|---|---|---|---|---|
| **Line** | **Almost none** — "took the line completely off" [B3]; edges are color/value breaks; thin line only at the eyes | Heavy, weight-varying ink **kept over the color** — "very new for us" [B_DL] | Bold **uniform** clean outline everywhere — the line IS the register | Clean, sparse line used **decoratively** — a few lines atop bold flat color [B4] |
| **Fill** | Clean flat color masses; figure read via color/value separation | Flat earthy fills under gritty painterly treatment | Flat, unshaded; line does the describing | Flat graphic shapes — "icons rather than realistic figures" [B4] |
| **Shadow** | **Hard-edged flat shadow shapes**, or none (figure→silhouette); darker step of the cast | Painted **tonal shadow mass**, visible hand, rough edges | Minimal / hatched; not a mass system | Often omitted or purely decorative |
| **Palette** | **One whole-frame emotional cast**; muted non-naturalistic base + ≤1 accent; "no green grass, no blue sky" | Warm **earthy desaturated base + one shock-color statement** (base + puncture) | Neutral ground + line color; palette secondary | Bright, modernist-poster colors (Matisse/Klee/Léger lineage) |
| **Texture** | Clean flat figure over softly-**painted atmospheric** BG (split treatment) | Gritty hand-mark texture on figure **AND** background (unified grit) | None; clean/paper ground | Flat, untextured, graphic-design surface |
| **Composition** | **Cinematic**: locked camera, tiny-figure negative space, environment-as-character, 16:9 | Cinematic too, but **denser, illustrative, action-forward** | Neutral/graphic; composition not register-defining | **Decorative, abstract, non-cinematic** — BGs *more* abstract than characters [B4] |
| **Tone** | Mythic, dark, silent-epic (S5 darker/mature [B8]) | Brutal, visceral, pulp | N/A (technique register) | Bright, comedic, whimsical modernism |

**The Primal inversion, made explicit + sourced.** Same director (Tartakovsky), same colorist (Scott Wills), same timing skeleton — the register boundary is a **surface** boundary. Every figure-surface axis flips: line (none ↔ heavy-over-color, the creators' *stated* differentiator [B_DL]/[B5]); figure texture (clean ↔ gritty); figure/ground treatment (split flat-on-painterly ↔ unified grit); shadow (flat hard shape ↔ painted tonal mass); palette logic (whole-frame single cast ↔ earthy base + shock accent [B_SW]). What does **not** flip (do NOT use as discriminators): the move→hold→burst timing, silhouette-first staging, mood-first color derivation, and Wills himself — the shared studio spine. This is exactly why the two registers are per-axis mutually exclusive and safe to co-exist in one vocabulary. *(The sibling's `preserve` already names "outline-free color-field flatness (Samurai Jack drift)" as its negative — the two registers reference each other symmetrically; §0 carries the one attribution errata to propagate.)*

**The UPA separation (the genuinely close call).** Both are flat + graphic + limited; the seed itself invokes "UPA-like graphic quality." Four sourced separators [B4]/[B1]/[B2]: (1) **backgrounds** — UPA abstracts them toward nothing; this register makes them the *most* naturalistic-atmospheric element in frame; (2) **staging** — UPA is decorative/graphic, this register is cinematic (Kurosawa framing, depth, negative space); (3) **lighting** — UPA has essentially none, this register is built on "cinematic lighting, with mood and depth"; (4) **tone** — UPA's brand was comedic modernist whimsy vs the mythic/dark chanbara epic. Tartakovsky's own stated formula IS the separation: UPA-type stylization **plus** realistic/feature painting — UPA alone is only half the register.

**The line-art-only separation** is the cleanest: it is the *all-outline* opposite of "almost no outline." A single frame decides it — visible uniform keyline fencing every shape → line-art-only; edges made of color/value breaks → this register.

**Frame-classification checklist (review-time):** forms read without black outlines, via flat shape + value contrast? (no black-keyline → not line-art; value-camouflaged silhouette → contrast fail) · figure clean-flat over a painterly-atmospheric BG (split), not gritty-everywhere? (unified grit → primal drift) · one whole-frame emotional cast on a muted non-naturalistic base? (naturalistic/multi-cast → palette drift; bright decorative flat → UPA drift) · shadows hard flat shapes or absent, no airbrushed volume? (soft-rendered → glossy-3D/anime drift) · cinematic negative space, not a busy filled frame? (cluttered → staging drift).

---

## 7. The non-derivative rule (doubly load-bearing)

Capture the **school**, never the cast, the frames, the title, or the person. **Legal frame (confirmed, with one refinement):** the idea/expression dichotomy — *"style alone is not usually considered the subject matter of copyright"* [B_CC]; *"copyright protects finished works of art… not… an artist's style"* [B_LA]. **Refinement:** this is not an absolute shield — mimicry can infringe *specific works* via substantial similarity, on a case-by-case basis [B_CC], courts are split at the margins [B_Buc], and **fictional characters are independently protectable** (so Jack/Aku/Ashi/Scotsman/the Daughters of Aku are radioactive, not merely un-named). The discipline is therefore **attribute-extraction + zero specific-expression reuse** — which is exactly why `refs/` ships with no third-party frames. **Genre is free:** *chanbara* (the sword-fight film genre) is uncopyrightable [B_Chanbara]/[B_CC]; "samurai-film staging" parallels primal's allowed "'70s-pulp" exactly.

| Reusable ATTRIBUTE (style — safe in prompts/clauses/markers) | Protected / AVOID (specific IP or person — forbidden) |
|---|---|
| Outline-free figures built from flat color shapes + value contrast ("color holds") | The names "Samurai Jack," "Jack," "Aku," "Ashi," "Scotsman," "Daughters of Aku" |
| Hard-edged flat shadow masses; full-silhouette commitment | "Tartakovsky" / "Genndy" in any prompt (credit the craft lineage generically) |
| Dramatic negative space; tiny-figure-in-vast-landscape cinematic staging | Any specific character design (the white-gi/topknot samurai *as that character*; the flame-collar shadow demon) |
| One whole-frame emotional color cast; muted non-naturalistic palette; "no default green grass / blue sky" | Specific frames, painted backgrounds, or shot re-creations from any episode |
| Painterly-atmospheric simplified backgrounds under flat figures | Episode titles/numerals, the series logo / title card, theme lyrics |
| Held-pose-then-burst timing; long silent stretches | Show-specific iconography as identifiers (the time-portal, the sword mythology) |
| "Chanbara / samurai-film" as *genre*; Kurosawa/Leone framing as film grammar; "UPA / mid-century-modern flat-graphic" as art-historical lineage | Committed reference images taken from the show (none in `refs/`) |

**The review test:** *A fan of the school recognizes the school; no one can name the episode.* Operationally, every production prompt / clause / marker / committed ref must pass (a) **zero banned tokens** (show, creator, character, episode, logo), and (b) **no output a fan could match to a specific frame, character, or scene** — attribute resemblance is the goal, expression resemblance is the failure. The sole unavoidable named identifier anywhere in the register is the machine slug `samurai-jack-s5` (internal, never a production string), exempt exactly as `primal-sketch-grit` / `90s-nicktoon-grossout` are.

---

## 8. Timing-bible additions (for the piece's animatic/motion phases; informs Bea/Mo, NOT the still register)

*The still `RegisterSpec` owns none of this — it is captured so the timing survives into Motion, and cross-linked to primal §8 (the shared Tartakovsky timing spine).*

1. **Move → hold → burst (triangulated [B7]/[B13]/[B_RT]).** Long environmental quiet → a held standoff (close-up inserts, eyes) → a burst of a few fast decisive strokes → a hard stop on a readable pose → an aftermath held long. Tartakovsky: *"a good action sequence is really like a good music sequence… there's a natural rhythm"*; *"it's always important to breathe in a sequence."*
2. **Silence before violence.** Score drops out; the frame goes to environmental sound (rain on stone). Tartakovsky (the S5-specific bridge): *"When we did the last season of Samurai Jack, people loved the silent sequences"* [B_RT] — which directly begat *Primal*. **Honesty:** *Primal* is the *more* silent show [B_CBR]; do not carry "more silence than Primal" as a Jack discriminator.
3. **Held poses like comic panels** [B14]; emotion delivered in the hold (posture, eye state, scale) rather than continuous motion.
4. **Holds are limited-animation-derived; the bursts spend the budget on fuller motion** (resolves the sourcing conflict, §9). Escalation enters via a *new* stillness, not faster cutting — the same rule as primal.
5. **Locked, legible camera** placed "where I can read the action the clearest"; cut on impacts; static frames steer attention. No shaky-cam, no motion-blur-as-cover.

*Frame values are register rules derived from sourced descriptions, not measured canon — frame-step the locked hero + any spike clip before hard-coding timing numbers (§9).*

---

## 9. Honesty flags (what the research could NOT establish)

1. **The "rendered out" line is a journalist paraphrase**, not a Tartakovsky quote [B5] (verified by fetch). The finding (per-axis inversion as stated intent) holds via the verbatim line-over-color quote [B_DL] + the independent no-outline doctrine [B1]/[B3]. **Errata candidate:** the sibling `primal-sketch-grit/research.md` §0 cites it quote-like — fix at the cross-link step (plan Task 5).
2. **"Hard-edged flat shadow shapes," "2–3 value steps," "rim light":** no crew quote states any of these. The flat-mask shading account is reconstruction from stills + reviews. Prefer "stark value silhouette against the lit field" over "rim light"; treat step-counts as authoring guidance.
3. **"Single whole-frame emotional color cast" as a law:** the *quoted* doctrine is per-scene color-key scripting (~30–50 keys/ep) + anti-naturalism ("no green grass, no blue sky"); the whole-frame flood is a verified *recurring S5 device* (XCIV red, XCIV white, XCIII rain), not a crew-stated rule.
4. **"Muted grays" [B_CGM] vs "bolder, more saturated" [B5]:** both are cited reporting; the reconciliation (gray resting register + harder saturated statements = widened range) is synthesis.
5. **Aspect ratio:** the seed/plan's **2.39:1 is wrong** — S5 is 1.78:1 (16:9) [B8]/[B15]. "Cinemascope" [B9] is compositional, not a format. Letterbox bars are an in-frame homage device [B14], not the register's delivery format. **This corrects the plan §2C/Appendix.**
6. **"Long elegant proportions" / heads-tall: unsourced.** Angular/stylized/silhouette-first is sourced; the elegance phrasing is seed language. Proportions authored per-character (SF03), not a register constant.
7. **No numeric negative-space ratio** exists in any source; scale-isolation is critic-confirmed for S5 [B8], the exact figure-to-frame fraction is not.
8. **The two marquee action quotes** ("good music sequence"; "camera where I can read the action clearest") are from **Primal-era** interviews stating *career* doctrine [B_RT] — legitimately applicable to Jack (his method spans both), but not S5-specific. The S5-specific bridge is "people loved the silent sequences."
9. **"Bryan Andrews directed S5": corrected** — Tartakovsky directed all 10; Andrews storyboarded/co-wrote several [B8]. (Matters only for accurate sourcing.)
10. **Most style doctrine on record describes the 2001–04 run + S5 jointly.** The flat/lineless/cinematic system is series-wide; S5-specific sourcing confirms continuity ("sleeker lines, richer colors") + the darker/more-mature tone + the digital-hand-crafted texture. The register name pins S5 for the **mature-tone calibration**, not a different visual system.
11. **UPA-likeness is partial:** sourced lineage, yes — but the *linelessness* traces to '50s Disney/Golden Books/Toei per Tartakovsky himself [B1]. Encode UPA as one ancestor, not the definition.
12. **Several pages 403/402'd** (AWN Dan Sarto; some TV Tropes recaps; The Verge; The Fandomentals) — content triangulated from search snippets + a readable corroborating source; no load-bearing claim rests solely on an unread page.
13. **Copyright section is US-doctrine** summarized from secondary sources (a CC counsel post, an attorney blog, one law-review preprint), not primary caselaw reading; the courts-are-split caveat [B_Buc] is real.
14. **Shot walkthroughs (§3-referenced / §5) are described from secondary sources** (reviews, Fandom, TV Tropes summaries), not from committed frame-grabs — shot details are approximate, and no third-party frame is committed or reproduced.

---

## 10. The genericized cross-engine spike prompt (for Sean's Step S look-spike)

**Fixed across both engines** (ChatGPT gpt-image + Google Flow) so the comparison varies **engine**, not art direction. Depicts an **original character + original setting** (no franchise reference — the review test §7). Tests the five money axes: **outline scarcity, flat shadow geometry, dramatic negative space, one emotional color cast, silent-film staging.** Target **16:9** (the corrected format, §5.7); a letterbox bar is an *optional declared homage*, not required.

> **A 16:9 widescreen cinematic frame, low wide static shot.** A lone armored wanderer stands motionless at the far left of a vast empty salt plain at dusk, a long straight blade held point-down at their side, cloak hanging still. The figure is tiny against the immense sky; the rest of the frame is open negative space. The scene should feel solemn, lonely, and tense — a held stillness before violence.
>
> Rendered as dark minimalist cinematic 2D action-animation poster art: **clean flat color shapes, almost no visible outlines** — forms read through adjacent color and value contrast, not ink lines; sharp angular silhouette; **hard-edged flat shadow shapes**; bold color blocking and strong value separation; restrained facial detail. The wanderer reads instantly as a simple iconic dark silhouette against the sky.
>
> Use a limited palette dominated by **a single emotional color cast**: a deep muted amber-and-ember dusk throughout, the figure dropped to a near-black silhouette, with one small warm accent — the last sliver of sun on the horizon. Backgrounds are simplified but atmospheric: broad flat painted color fields, abstract low geometry, **dramatic cinematic negative space**. Stage the image like a **silent samurai-film frame** — emotion carried through posture, scale, and composition, not facial detail.
>
> No text, no watermark, not photorealistic, not 3D, no glossy anime rendering, no heavy comic-book outlines, no soft airbrush modeling, no busy detail.

**Why this prompt:** every clause maps to a verified attribute — "took the line completely off" (§5.1) → *almost no visible outlines*; the color-hold edge mechanism (§5.1/§5.6) → *forms read through color and value contrast*; the hard flat shadow shape (§5.3) → *hard-edged flat shadow shapes*; the linelessness→single-cast chain (§5.2) → *a single emotional color cast*; environment-as-character + scale-isolation (§5.7) → *dramatic cinematic negative space* + *tiny against the immense sky*; chanbara staging (§5.7) → *silent samurai-film frame*. The negatives are the four drift directions (§2 risk-bible ¶1) as *attributes*, naming no neighbor register. **No franchise token appears** — "samurai-film" is the genre (§7), the character is an original wanderer, the setting an original salt plain.

**Locking the hero (Step S, Human Checkpoint 2):** select exactly one candidate by eye; copy its bytes unchanged to `refs/samurai-jack-s5-hero.png`; record its provenance (engine, date, exact prompt, dimensions) + Sean's one-line reason keyed to the money axes in `refs/README.md`. Commit no third-party stills.

---

## Status

**LOOK RATIFIED — HERO LOCKED — READY TO AUTHOR (2026-07-13).**

Human Checkpoint 1 passed 2026-07-11 (Sean ratified the doc as-is, "this works", aspect-ratio correction to 16:9 confirmed). **Human Checkpoint 2 passed 2026-07-13** — Step S ran cross-engine (ChatGPT gpt-image + NB2 + the Higgsfield `gpt_image_2` prompt-ladder run), Sean's eye the sole arbiter (no LLM aesthetic judge). He locked **exactly one** hero by eye: `refs/samurai-jack-s5-hero.png` (a byte-copy of `refs/spike-2026-07-11/beta_3_flat.png` — Higgsfield `gpt_image_2`, 2688×1520, the GRANDMASTER kid on the register's own gpt-image transport; the cleanest hard-edged flat-poster surface of the batch). Full provenance, the retained spike spread (register-range documentation — the register is a *surface*, not a single-shot template), and the composition-phrase A/B outcome (**keep all five money-phrases**) are recorded in [`refs/README.md`](refs/README.md).

**Both human checkpoints are now recorded — the authoring build (Step B, a separate isolated-worktree Fable-5 $0 drill) is cleared to begin.** The register is still absent from `pipeline/registers.py`; Step B wires it via the five-step doctrine drill (plan §4).

## References (internal)

- The ratified plan: [`docs/active/2026-07-11-samurai-jack-s5-register-design.md`](../../docs/active/2026-07-11-samurai-jack-s5-register-design.md) (§2 the four ratified decisions; §2C/§3 Step R deliverable; §4 the build task list; §5 genericization; Appendix A the candidate spec).
- The thin seed (research INPUT): [`docs/research/samurai-jack-season-5-art-style-description.md`](../../docs/research/samurai-jack-season-5-art-style-description.md).
- The proof frame: [`images/samuria-first-pose-chatgpt.png`](../../images/samuria-first-pose-chatgpt.png) (Sean's gpt-image gen).
- The depth template + the negative-control axis to invert: [`registers/primal-sketch-grit/research.md`](../primal-sketch-grit/research.md) (§6 ↔ this doc §6; the reciprocal cross-link the plan Task 5 wires at build time).
- The most recent worked example: [`registers/90s-nicktoon-grossout/research.md`](../90s-nicktoon-grossout/research.md).
- The doctrine + five-step drill: [`docs/architecture/prompt-style-neutrality-doctrine.md`](../../docs/architecture/prompt-style-neutrality-doctrine.md).
- The seven research dimensions + depth bar + four required outputs: [`docs/active/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md`](../../docs/active/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md) §2a.
- Valid IR categories (the Cy block's constraint): [`pipeline/criteria.py`](../../pipeline/criteria.py) `VALID_IR_CATEGORIES`.
