# `primal-sketch-grit` — register research

**Date:** 2026-07-03 · **Consumer:** GRANDMASTER (greenlit; its STRESS-TEST returned `revise` on this register's absence) · **Status:** authored into `pipeline/registers.py`; transport verdict `RESOLVED — gpt-image` (2026-07-11, fork #1: unwired, fails loud until a runner is wired — see §4; spike history in `briefs/2026-07-02-grandmaster/go-no-go.md`)

**Method:** four parallel deep-research subagents (line/ink/paint-process · palette/staging · form/timing · tells/negative-controls), synthesized here into the four wire-ready outputs the [animation-vocabulary-expansion plan](../../docs/active/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md) §2a requires. Research answers *"what makes the look the look,"* grounded in primary sources (Tartakovsky and crew interviews), never surface pastiche.

---

## 0. Corrections to the concept doc's craft baseline (ratified by Sean, 2026-07-03)

The GRANDMASTER concept's Genndy bible was pre-filled from memory; the research corrected three claims, and **the register is authored against the corrected Primal**:

1. **Primal is NOT flat-angular.** It is **organic-illustrative with a heavy, weight-varying ink contour kept OVER the color** — Tartakovsky: "We even kept the line-work over the color, which was very new for us" ([Dot and Line](https://dotandline.net/genndy-tartakovsky-primal-interview/)); on *Samurai Jack* "all marks from the hand-drawn process were rendered out," on *Primal* they chose to keep them for "a gritty 1970s look" ([Yahoo Entertainment](https://www.yahoo.com/entertainment/genndy-tartakovsky-primal-evolution-animation-163031835.html)). Flat-angular/no-outline is Samurai Jack's register — the mutually-exclusive sibling.
2. **The candy/oil-geyser is NOT a Primal feature.** Blood-substitution (oil, sparks, goo — never red) is **Samurai Jack's** kids'-network convention ([CBR](https://www.cbr.com/primal-is-more-samurai-jack-than-samurai-jack/)). Primal's own convention is **explicit, copious, shock-colored blood** — "bursts of bright red blood" ([Goomba Stomp](https://tilt.goombastomp.com/idiot-box/primal-is-genndy-tartakovsky-at-his-best-and-most-brutal/)); Wills names **green blood** as a Genndy "crazy color statement" ([Sloan Science & Film](https://scienceandfilm.org/articles/3346/genndy-tartakovskys-primal-art-director-scott-wills)). GRANDMASTER's candy-geyser stays as staged — a **deliberate cross-register staging borrow**, recorded as such in the concept + Studio Brief; no register field or `IR.*` rule claims it. `tests/test_primal_sketch_grit.py` guards the spec text.
3. **"Hold the pre-strike frame 2–4 seconds" conflates two different holds.** The *stand-off* is a scene-scale beat (4–15+ s of near-stillness with micro-motion: breathing, wind, pupil work); the true *dead-stop* freeze is a short accent (~0.5–2 s) at recognition/post-impact beats. Both exist; they are different tools (§8).

Also sharpened, not a reversal: **"sketchy" overstates the line.** The final stroke is thick, confident, "blotted," organically imperfect — retained hand marks, **not** construction-sketch scribble and **no visible under-drawing pass**. Do not prompt for exposed construction geometry (that is pencil-test vocabulary).

---

## 1. Output 1 — the RegisterSpec (as shipped in `pipeline/registers.py`)

| Field | Value | Sourcing |
|---|---|---|
| `name` | `primal-sketch-grit` | Locked in the greenlit seeds ([L17]) |
| `summary` | Tartakovsky-Primal register. Heavy weight-varying ink kept over the color, gritty painterly figure and background, warm earthy desaturated base, one bold color statement per scene. | §§5.1–5.2 |
| `identity_lock` | Match face/hair/palette/proportions/silhouette of Image 1 exactly; **the heavy ink contour is surface treatment and must never alter the anatomy.** | The line-is-treatment finding (§5.1) + silhouette-first doctrine (§5.4) |
| `preserve` | Drawn ink line visible over every color area — thick, near-black, weight varying with mass and silhouette, deliberately imperfect; gritty hand-painted texture on BOTH figure and background; warm earthy desaturated base. Negatives: no clean uniform outlines (line-art-only drift), no outline-free color-field flatness (Samurai Jack drift), no smooth gradients/airbrush polish (over-cleaning drift). | §5.1, §5.5, §6 |
| `style_token` | "Raw seventies-pulp 2D animation still: heavy weight-varying ink line kept over the color, gritty painterly brushwork shared by figure and background, flat earthy fills with drawn tonal shading, warm earthy desaturated palette punctuated by a single bold color statement." | §§5.1–5.3; the '70s-pulp stack (Leone/Kurosawa/Bakshi/Frazetta/Heavy Metal) Tartakovsky names |
| `generation_model` | **RESOLVED — gpt-image (`gpt-image-2`), 2026-07-11 fork #1** (unwired; fails loud via `UnwiredTransportError` until a runner is wired). The NB2 hypothesis was judged by the costed spike and batched to gpt-image. | §4 |
| `final_model` | NB Pro — rides the painterly-final seam (no consumer yet, same as watercolor/photoreal/3d) | Registry convention |
| `markers` | `weight-varying ink` · `gritty painterly texture` · `warm earthy desaturated` · `line-work kept over the color` · `dead-stop hold` · the name | §5 tells; verified collision-free against all other registers' markers |
| `stub_keywords` | `("primal",)` — appended AFTER the legacy six (precedence oracle-pinned) | Task 2.5 |

**Deliberate prompt-authoring choice:** pencil-test negative controls ("no graphite / cream paper / cross-hatch") do **not** appear in `preserve` — naming a register's vocabulary in a negative can evoke it in the image model. Pencil-drift policing lives in the review checks (Cy Example C's risk-bible excerpt) instead.

## 2. Output 2 — the Cy block

Shipped as **Example C** in [`pipeline/agents/prompts/cy-character-designer-context.md`](../../pipeline/agents/prompts/cy-character-designer-context.md): three sample IR.* entries for the GRANDMASTER kid (`IR.kid.style.line-work-over-color`, `IR.kid.palette.earth-base-mood-flood`, `IR.kid.proportion.slight-child-silhouette`) + the four-paragraph risk-bible excerpt (drift directions, what the register can't do, where references thin, the three binary review checks). Additional wire-ready IR drafts the Bible pass can draw on:

- `IR.{char}.palette.value-silhouette-contrast` — every frame reads as a clear value silhouette: dark figure on light field or the inverse, never mid-value on mid-value (Tartakovsky's stated "very stark contrast" rule, [CGMag](https://www.cgmagonline.com/interviews/a-primal-evolution-talking-to-cartoon-legend-genndy-tartakovsky/)).
- `IR.{char}.motion.move-stop-burst` — action decomposes into travel → dead-stop pose → burst; escalations enter via a NEW stillness, never continuous acceleration.
- `IR.{char}.motion.post-burst-aftermath-hold` — after the climactic burst, one aftermath pose held past comfort; the emotional cost plays in the hold (brow/pupil change, breathing), not in motion.

## 3. Output 3 — `refs/` + bibliography

`refs/` ships **empty of third-party frames by design** (see `refs/README.md`): Primal stills are copyrighted study material, linked below, never committed or fed to generation. What lands in `refs/`: **Sean's own confirmed ART-VIZ Route-B hero frame** (the §4.4 go/no-go target — his call, per plan Task 2.6) and any future self-authored exemplars. Key sources (full per-dimension bibliographies in the four research transcripts):

- [Dot and Line — Tartakovsky interview](https://dotandline.net/genndy-tartakovsky-primal-interview/) — line-work over color ("very new for us"); Schellewald's "almost Moebius-type" BG designs; Bakshi/'70s-sci-fi steer
- [Sloan Science & Film — Scott Wills interview](https://scienceandfilm.org/articles/3346/genndy-tartakovskys-primal-art-director-scott-wills) — one hand colors environments + characters; nature-doc base vs "crazy color statement that shocks you"; green blood
- [Yahoo Entertainment — Tartakovsky](https://www.yahoo.com/entertainment/genndy-tartakovsky-primal-evolution-animation-163031835.html) — kept hand marks vs Jack's rendered-out; gritty '70s *Heavy Metal* look; "done with somebody's hands"
- [CGMag — Tartakovsky](https://www.cgmagonline.com/interviews/a-primal-evolution-talking-to-cartoon-legend-genndy-tartakovsky/) — mood-first color derivation; the hot-pink despair climb; stark light/dark figure contrast
- [Rotten Tomatoes editorial](https://editorial.rottentomatoes.com/article/primal-creator-genndy-tartakovsky-revolutionized-animated-action/) — "a good action sequence is really like a good music sequence"; camera "where I can read the action the clearest"; the silent stand-off
- [Animation Obsessive — The Visual World of Samurai Jack](https://animationobsessive.substack.com/p/the-visual-world-of-samurai-jack) — the negative control's doctrine (no outlines, "no green grass, no blue sky")
- [canmom — Animation Night 35](https://canmom.art/films/animation-night/35-genndy-tartakovsky) — textured detail + complex shading vs Jack; composition ethos; [smear taxonomy](https://canmom.art/animation/smears)
- [fullfrontal.moe — Studio La Cachette](https://fullfrontal.moe/whats-hidden-in-studio-la-cachette/) — thick "open" linework house style; limited framerates; TVPaint
- [Schellewald portfolio](https://cwschellewald.art/primal/) + [Orolfo Primal BGs](https://victoriaorolfoart.tumblr.com/post/692135335412514816/backgrounds-from-genndy-tartakovskys-primal) + [Wills' BG blog](http://animationbgs.blogspot.com/) — the two-stage background pipeline (drawn design indicating material/light → Wills' final color), Photoshop paint
- [Goomba Stomp](https://tilt.goombastomp.com/idiot-box/primal-is-genndy-tartakovsky-at-his-best-and-most-brutal/) + [Glitterati Lobotomy](https://glitteratilobotomycom.wordpress.com/2020/12/18/genndy-tartakovskys-primal-review/) — "thick, blotted black outlines"; visible squiggles/drawn shading; 2.39:1
- [SlashFilm](https://www.slashfilm.com/569935/primal-review-genndy-tartakovsky/) + [CBR](https://www.cbr.com/genndy-tartakovsky-primal-interview/) — brow/pupil acting, the "20 shots" wordless-emotion mechanism
- Episode anatomy: "Spear and Fang" (Wills' juried Emmy), "River of Snakes" (red blood into blue water), "Rage of the Ape-Men" (red-flood arena), "Plague of Madness" (Emmy; terrain-authored chase tempo), "A Cold Death" (DeStefano's juried Emmy; winter palette)

## 4. Output 4 — transport recommendation

**Transport verdict: RESOLVED — gpt-image (2026-07-11, fork #1, Sean-ratified; unwired — the register's `generation_model` records `gpt-image-2` and `invoke_image_edit` fails loud with `UnwiredTransportError` until a gpt-image runner is wired via the `openai-image-gen` skill and validated for across-edit identity; `final_model` stays NB Pro, the dormant painterly-final seam).** The paragraph below is the original recommendation that the costed spike judged — kept as the record of the §3c hypothesis:

**Author clauses → spike ONE hero frame on NB2 from text alone → Sean's eye** (the §3c default; the register's `generation_model` recorded the NB2 hypothesis at authoring). Evidence is circumstantial both ways and the spike is the only real instrument: the SD community trained dedicated Primal LoRAs (text prompting under-delivered there — [Civitai](https://civitai.com/models/502844/genndy-tartakovsky-style-series-for-pony)), while Gemini-family guidance favors explicit attribute language and supports style-reference feeds if text alone reads generic ([Gemini API docs](https://ai.google.dev/gemini-api/docs/interactions/image-generation)). **Predicted NB2 miss:** the retained-hand-mark grit — watch for uniform line + grain-filter-over-clean-render. Escalation ladder (pre-agreed in `go-no-go.md`): NB2-from-text → NB2 + `refs/` style-image feed (watch the Flo-B identity-morph) → **NO-GO → Route C** (`pencil-test-colored`, already buildable); never a new transport mid-Bible-pass.

---

## 5. The look, by dimension (condensed; corrections folded)

**5.1 Line & contour.** Thick, near-black, **weight-varying** ink contour kept over the color on figure AND environment. Weight follows **mass and silhouette** (heaviest on outer silhouette + mass-bearing edges — jaw, shoulder, haunch; interior lines thinner, sparser: "only the details that are necessary"). Roughness lives in the retained final stroke (wobble, breaks, "squiggles that look a little out of place") — no separate visible construction pass. Variance is structural, not cosmetic: "we all draw the characters subtly different and that gives it an organic look… done with somebody's hands." Made digitally (TVPaint characters, Photoshop backgrounds) but reads as hand ink. *Honesty flag: the weight rule is reconstructed from stills + critic language; no published studio line doctrine exists.*

**5.2 Palette & color logic.** Two-layer system: a grounded, **warm earthy desaturated** naturalistic-leaning base (nature-doc reference, never generic — "not green grass or blue sky… something specific in nature") punctured by deliberate saturation spikes — "Genndy always wants some crazy color statement that shocks you." **Mood is the derivation; location is the constraint**: one dominating mood-light event per scene (rage = red flood, despair = hot pink, grief = drained/ash), flooding figure, shadow, and background in a single cast. Hard readability rule: **stark value contrast** — dark figure on light field or the inverse. Shadow reads as hard-edged drawn shapes in a darker value of the scene's cast (*inferred from practice + Wills' value discipline; no stated shadow-hue doctrine — flag*). Blood, when the register shows it, is a **shock-color statement** (red, green, fluorescent), never naturalistic local color.

**5.3 Shading, texture & the paint process.** Volume is asserted at anatomy (muscle masses as drawn tonal shading with rough painterly edges) and refused elsewhere — visibly *drawn*, never airbrushed. The grit is **four compounding process choices**, not an overlay: retained hand marks; painterly backgrounds with visible strokes (Wills' acrylic/drybrush formation executed in Photoshop); the '70s-pulp reference stack; limited framerates. Figure and background are **split production, unified treatment**: characters (flatter fills + drawn shade) over dense paint, but both keep the line over the color and one hand (Wills) colors both under one mood light. *No evidence of a compositing-stage film-grain overlay — do not encode grain as the mechanism.*

**5.4 Form & proportion.** Organic-illustrative, Frazetta-mass-filtered-through-graphic-shapes: chunky squared-off muscle planes under heavy contour, not anatomical rendering and not flat cutout. Silhouette-first staging (poses must read in near-silhouette). Faces: squared planes dominated by the **brow shelf**; the acting channel in a dialogue-free register is **brow compression + pupil state** (dilate/shrink/bloodshot) + whole-body posture, delivered across many shots ("maybe in 20 shots… it makes it actually more emotional"). *Heads-tall: no published spec — measure per character at Bible authoring (SF03 declares the target); child-proportion figures have no canonical Primal reference — the kid is authored fresh.*

**5.5 Signature tells (ranked).** (1) **Visible heavy line-work over color** — the deliberate break from Tartakovsky's no-outline past; the single axis separating Primal from every other Tartakovsky show. (2) **Painted-grit illustrative surface** shared by figure and background. (3) **Earthy base punctured by expressionist color violence** (hot-pink sky, shock-color blood) — the peak-moment recognizer. The dead-stop hold is real but career-wide (shared with Jack) — a timing tell, not a still-frame discriminator.

## 6. Negative controls (the confusable-adjacent registers)

| Axis | **primal-sketch-grit** | Samurai Jack | `line-art-only` | `pencil-test-colored` |
|---|---|---|---|---|
| Line | Heavy, weight-varying, blotted dark ink; figure AND environment | **None** — color-field edges | Bold **uniform** outline, clean | Thin graphite grey + construction lines |
| Fill | Tonal painted color, drawn shading | Flat poster-graphic fills | Flat, unshaded | Flat fills over paper |
| Texture | Gritty painterly everywhere; one treatment | Clean flats over stylized paint (split) | None; clean white ground | Cream paper grain |
| Palette | Earthy base + one expressionist statement | Bold clean graphic fields | Unconstrained flat | Warm muted, paper-tinted |
| Shadow | Painted tonal mass, visible hand | Flat shape-shadow or none | None | Cross-hatch strokes |

Frame-classification checklist (review-time): visible drawn contour? (no → Jack drift) · texture continues into the figure? (no → split-treatment drift) · shadow painted mass on opaque paint? (hatching/paper → pencil drift) · line weight varies? (uniform → line-art-only drift).

## 7. The non-derivative rule

Capture the register, never the cast or the frames. Everything expressible as an **attribute** — weight-varying ink over color, shared figure/background grit, earthy base + one color statement, move→dead-stop→burst timing — is style and is reusable. Any recognizable **delineated thing** — Spear, Fang, Primal's creature designs, a restaged specific shot, the title trade dress — is protected content: never generated, never named in production prompts, never approximated to recognition. Production clauses are fully genericized (no "in the style of Primal" — attribute language only; named-source language lives in research docs like this one). `refs/` third-party images are study exemplars for human ratification only. **The review test: a Primal fan should recognize the school; no one should be able to name the episode.**

## 8. Timing-bible additions (for the piece's animatic/motion phases; informs Bea/Mo, not the still register)

At 24fps — halve for the 12fps pipeline. *Frame values are register rules derived from sourced descriptions, not measured canon; frame-step refs at the spike.*

1. **Two holds, never conflated:** the *stand-off* (pre-violence threat assessment; scene-scale, 4–15+ s; never frozen — breathing/wind/pupil micro-motion stays alive) vs the *dead-stop accent* (true freeze ~12–48 frames at recognition, pre-strike cock, post-impact).
2. **Bursts are frame-scale:** a strike reads in ~4–10 drawings on ones/twos with one elongated smear or multiple at peak; buildup is measured in seconds, the strike in frames.
3. **Escalation = reset to stillness:** a new threat enters via a fresh stand-off, not faster cutting.
4. **Tempo like a song, terrain-authored in chases:** vary speed with environmental squeeze-points, not shot-length alone.
5. **End quiet:** every violent sequence closes on an aftermath hold past comfort; the cost plays in brow/pupils there.
6. **Camera locked and legible:** placed "where I can read the action the clearest"; cut on impacts; the ECU eye insert is the exclamation mark; no shaky-cam, no motion-blur-as-cover.
7. **Base exposure:** twos/threes with long holds; ones only inside bursts (*inferred from La Cachette practice; unpublished — flag*).

## 9. Honesty flags (what the research could NOT establish)

- The line-weight *rule* and shadow-hue logic are reconstructions from stills + critic language, not quoted studio doctrine.
- No published exposure sheets or smear breakdowns exist for Primal — frame-step the refs at the spike before hard-coding timing numbers.
- No public evidence on Gemini-family models reproducing this register from text — the go/no-go spike was the only real instrument. *(Transport since RESOLVED — gpt-image, unwired; fails loud until a runner is wired. See §4.)*
- Child-proportion figures in this register have effectively zero canonical reference; the kid's proportions are authored, not matched.
- Several quotes trace to paywalled/403 pages via search snippets (AWN, IndieWire, Deadline, Collider) — attributed but not re-verified against full page text.
