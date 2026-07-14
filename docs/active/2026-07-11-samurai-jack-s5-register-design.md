# Design — author register `samurai-jack-s5`, the flat-cinematic Tartakovsky sibling

**Date:** 2026-07-11 · **Workstream:** animation-vocabulary-expansion (within the active outward turn — a production-capable style, not a new workstream) · **Status:** PLANNING (this doc is the ratified plan). The deep-research pass, the look-spike, and the authoring build are **subsequent sessions**. · **Build engine (authoring):** Fable 5, TDD, stub-green, $0, stop at first green. · **Method:** Opus brainstorm (five ratified sections) → Codex independent plan → reconciliation (every Codex claim verified against main) → red-team fold. Mirrors the nicktoon/primal converged drill.

---

## 0. Goal (one sentence)

Author a NEW closed style register `samurai-jack-s5` — Tartakovsky final-season flat cinematic poster-art (clean flat color shapes, almost no visible outlines, sharp angular silhouettes, hard-edged flat shadow shapes, bold color blocking, dramatic negative space, a single emotional color cast, silent samurai-film staging) — the mutually-exclusive **flat** sibling of `primal-sketch-grit`, via the proven five-step doctrine drill, transport recorded as gpt-image (unwired, fails loud), the look ratified by Sean's eye **before** authoring.

**What this is:** one `RegisterSpec` + its Cy worked example + markers + `registers/samurai-jack-s5/` folder (research + refs) + one per-register test, riding the now-twice-proven cheap pattern. **What this is NOT:** a register-family abstraction; a `tartakovsky` style skill; a gpt-image runner; any change to Em, the six locked legacy registers, or the two frozen md5 guards.

---

## 1. Where this sits (verified against main, 2026-07-11 — commit f957fb2)

- `pipeline/registers.py` holds **8 registers** (6 legacy + `primal-sketch-grit` + `90s-nicktoon-grossout`). `samurai-jack-s5` is **absent**; `registers/samurai-jack-s5/` does not exist.
- **The fail-loud transport guard already covers gpt-image.** `SUPPORTED_IMAGE_MODELS = frozenset({NB2_FLASH, NB_PRO})` in `nb_pro_runner.py`; `invoke_image_edit` raises `UnwiredTransportError(model)` at its **first line**, before cache and before the stub/no-key check, for any model outside the allowlist (`gpt-image-2` included). **No new guard code is needed** — unlike nicktoon's build, which had to add the guard for primal's fork.
- The **drill is proven twice** (primal; nicktoon, PR #105). Per-register test template: `tests/test_primal_sketch_grit.py` + `tests/test_90s_nicktoon_grossout.py`.
- The **seed research is thin** — `docs/research/samurai-jack-season-5-art-style-description.md` is a single unsourced ChatGPT pass (adjective list + prompt template + the magic phrase). Not wire-ready.
- The **ChatGPT example** `images/samuria-first-pose-chatgpt.png` proves gpt-image renders the register clean (near-silhouette figure, huge amber sky, hard-edged flat shadow shapes, 2.39:1 negative space).
- `GPT_IMAGE = "gpt-image-2"` already exists as a module constant in `registers.py` (added for primal's fork #1). `invoke_image_edit` signature verified: keyword-only `prompt`, `reference_images`, `output_path`, `cache_dir`, `model=...`, etc.

---

## 2. The five ratified design decisions (Sean, this session)

### A — FOLD: no `family` field, no `tartakovsky` skill (open question A, the headline)

The honest test, run with `primal-sketch-grit`'s real content + the samurai seed in hand: the shared structure between the two is **timing & staging grammar** (silhouette-first, the two holds, locked legible camera, a single dominant mood-color-cast) — which `primal-sketch-grit/research.md` §8 already places in a "for Bea/Mo, not the still register" section, and which the seed's staging language echoes. (Honesty note: the samurai deep-research doesn't exist yet — the still-frame/timing split is confirmed for primal and *inferred* for samurai from the seed; Step R's research ratifies it. The FOLD does not rest on that inference — see below.) The `RegisterSpec` still-frame fields (`identity_lock` / `preserve` / `style_token`) **invert** on every axis:

| Axis | `primal-sketch-grit` | `samurai-jack-s5` |
|---|---|---|
| Line | Heavy, weight-varying ink kept **over** color | **No visible outline** — shape + value contrast defines form |
| Fill | Tonal painted color, drawn shading | Flat poster-graphic color shapes |
| Texture | Gritty painterly everywhere | Clean flats, simplified atmospheric BG |
| Shadow | Painted tonal mass | Hard-edged flat shadow shapes |

**The FOLD rests on the present-tense no-reader fact + Sean's product ceiling, NOT on the unwritten samurai research.** A `family` field would have **no reader** in v1 (the front-door red-teams' exact anti-pattern; Codex's own §10 divergence to add a `family` metadata field was declined for this reason on the primal build). The skill fails the §3a bar: promotion needs **≥2 real consumers AND standalone reusable structure**; `samurai-jack-s5` has one named consumer. Sean's confirmation makes it a **product ceiling**: Samurai Jack + Primal are his **only two** Tartakovsky styles, and **Clone Wars collapses into `samurai-jack-s5`** (same flat-graphic register — not a third register). The family caps at two and never grows; abstracting it is sugar.

**Recorded outcome:** the ≥2-Tartakovsky trigger (backlog §5, converged-plan §3b) is **answered FOLD** on those grounds. **Reconsideration is not permanently foreclosed:** Step R's samurai research could, in principle, surface genuinely-shared *still-register* structure (not just timing) — the honest reopen condition — but Sean's two-style product ceiling makes that moot in practice. The two research docs get a reciprocal **cross-link** (primal `research.md` §6 negative-control table ↔ the new samurai `research.md` negative-control section) so the relationship lives as *documentation*, not code, and the next session does not re-litigate the family question cold.

### B — Transport = gpt-image, unwired, fails loud (already covered) (open question B)

`generation_model = GPT_IMAGE` (`"gpt-image-2"`), `final_model = NB_PRO` (the dormant painterly-final seam convention, same as watercolor/photoreal/3d/primal/nicktoon). The **existing** `UnwiredTransportError` guard covers it — **no new code**.

**Honest framing of the fallback role.** The backlog calls `samurai-jack-s5` "GRANDMASTER's revised fallback." Stated plainly: it is a **style/identity-hold fallback on the *same* unwired transport as primal** (both need the gpt-image runner wired), **not** a transport-safe fallback. The transport-safe fallback remains Route C (`pencil-test-colored`, NB2, already buildable). What it actually protects against:
- a **style** mismatch (Primal's gritty look doesn't land for GRANDMASTER, or Sean prefers the cleaner poster look), **and**
- **plausibly** a better across-edit identity hold on gpt-image — flat clean shapes carry less high-frequency detail to drift than primal's grit. **Recorded as a hypothesis, unvalidated**, not a claim.

Wiring an actual gpt-image runner + the across-edit identity validation is **DEFERRED and gated** on a separate, costed, Sean-greenlit GRANDMASTER build. **This authoring plan does not wire it.**

### C — Fresh Fable-5 deep-research pass ($0), not a gap-fill (open question C)

The seed is the research's *input*, not its output. Two head-starts keep it from being from-scratch: (1) the seed feeds dimensions 1/2/5/7 (line, palette, texture, the magic phrase); (2) the negative-control dimension is **half-written** — invert `primal-sketch-grit/research.md` §6's Samurai-Jack column. The pass produces `registers/samurai-jack-s5/research.md` with the doctrine §2a depth made real for this register:
- **Frame-by-frame still analysis** of legally-viewable exemplars (composition, edge construction, shadow construction, figure/background process — concretely, not adjective lists; no third-party frames committed).
- **Composition & staging grammar** — camera height, the 2.39:1 letterbox, negative-space ratios, tiny-figure-in-vast-landscape placement (the register's signature that primal does not share).
- **The flat-color-shape + hard-edged-flat-shadow logic** — how forms read *without* outlines (adjacent value/color contrast). This is the register's hardest-to-prompt core and the axis gpt-image nails that NB2 misses.
- **Negative controls** — the inverted §6 table vs `primal-sketch-grit`, plus vs `line-art-only` (bold *uniform* outlines — the opposite of "no outline") and vs UPA/midcentury-modern flat-graphic (a genuinely-close neighbor worth naming).
- **The genericization rule** (see §5) — a *school* of flat cinematic 2D captured attribute-only.

Runs as a distinct **$0** step (subscription/web research + local synthesis; no paid API, no image gen). **Sean ratifies `research.md`** before it becomes the build's source of truth. The four wire-ready outputs (draft `RegisterSpec`, the Cy block, the refs policy + bibliography, the transport record) are its deliverables.

### D — Anti-drift: GO (open question D)

**Primary justification:** `samurai-jack-s5` is a **committed future style** — one of Sean's two go-to registers, which he *will* use ("If I don't use it for Grandmaster, I would use it eventually"). It is not a merely-conditional fallback, which removes the "wait until proven-needed" objection entirely. It is within the active outward-turn workstream ("more characters/styles"), rides the now-proven cheap pattern, at $0, and resolves the deferred family trigger (banked whether or not the fallback ever fires).

**Guardrail update recorded:** the two-blockers guardrail (`primal` + `nicktoon`, both authored) is superseded by — *the full §2c powerhouse roster stays sidequest-deferred; registers leave the backlog **one at a time, each on Sean's explicit greenlight, only with a specific named consumer.*** `samurai-jack-s5` qualifies (committed style + GRANDMASTER fallback + resolves the family trigger). The remaining roster (spiderverse, ghibli, upa, etc.) stays deferred with no greenlight. The anti-drift contract holds: this authors **one** consumer-justified register, not a speculative fleet. `ROADMAP.md` is **not** edited — the active workstream is unchanged and no new workstream opens.

### E — Sequence: spike-first (Sean's choice this session)

```
Step R  deep research ($0, Fable-5 subagents) -> registers/samurai-jack-s5/research.md
        -> SEAN RATIFIES (Human Checkpoint 1)
Step S  Sean's cross-engine look-spike (COSTED; ChatGPT + Google Flow; his eye the SOLE arbiter,
        NO LLM aesthetic judge) using the research-refined register vocabulary
        -> lock ONE hero frame into registers/samurai-jack-s5/refs/ (Human Checkpoint 2)
Step B  authoring build ($0, Fable 5, TDD, stub-green) -> wire the register via the doctrine drill
[DEFERRED + GATED] gpt-image runner + across-edit identity validation -> rides GRANDMASTER
        (separate, costed, Sean-greenlit)
```

---

## 3. Pre-build phases (Sean-paced, before the authoring build)

### Step R — deep research ($0)

Fable-5 parallel deep-research subagents (one per dimension cluster), synthesized into `registers/samurai-jack-s5/research.md` + `registers/samurai-jack-s5/refs/README.md`. **No** Python/prompt/template/doctrine edits and **no** image generation in this phase. `research.md` is ratifiable only when it carries: a status header (`CANDIDATE — research complete; human ratification pending`); a **claim ledger** mapping each thin-seed assertion to confirmed/corrected/unsupported with a citation; the seven-dimension craft account with the §2C depth; a **sourced bibliography** (primary craft interviews / production commentary / first-party material, each with title, publisher/author, URL, access date, claims supported — no load-bearing claim resting only on the unsourced seed); an **honesty-flags** section (what it could not establish); the **negative-control table** (esp. the inverted primal §6 axis); the **genericization rule**; and the **four wire-ready outputs**. Ends at `RESEARCH COMPLETE — HUMAN CHECKPOINT 1 PENDING`.

**Human Checkpoint 1 (Sean ratifies research):** the seven-dimension account is accurate enough to author from; the negative-control axis makes samurai/primal mutually exclusive in practice; the draft spec + Cy block are attribute-only; the fixed cross-engine spike prompt depicts an **original** character + setting and tests the money axes (outline scarcity, flat shadow geometry, negative space, one emotional cast, silent-film staging); the transport record stays `GPT_IMAGE` gen / `NB_PRO` final / unwired. On approval, status → `RESEARCH RATIFIED BY SEAN — LOOK SPIKE PENDING` (+ date + corrections).

### Step S — the look-spike (costed, Sean-run)

Run manually in ChatGPT + Google Flow, **not** through `invoke_image_edit` (its guard would correctly refuse gpt-image, and the spike is a human web-app task anyway). No LLM aesthetic judge — Sean's eye is the sole arbiter (the eval handbook bars an LLM aesthetic judge on creative quality). Same research-ratified prompt / original character / original environment / aspect ratio across both engines so the comparison varies **engine**, not art direction. Artifacts land under `registers/samurai-jack-s5/refs/spike-YYYY-MM-DD/` with per-candidate provenance (product, date, exact prompt, dimensions).

**Locking the hero:** select **exactly one** candidate by eye; copy its bytes unchanged to `registers/samurai-jack-s5/refs/samurai-jack-s5-hero.png`; record in `refs/README.md` the chosen path, engine, date, exact prompt, dimensions, and Sean's one-line reason keyed to the five money axes; note rejected candidates with one-line reasons. **Commit no third-party show stills** — only original spike outputs + provenance. `refs/` ships empty of third-party frames by design.

**Human Checkpoint 2 (hero lock):** Sean confirms **cold** that the one hero reads as the flat cinematic register without a franchise name in the prompt, showing almost-no-outline shape definition + hard-edged flat shadow + dominant negative space + one emotional cast + silent-samurai staging, and avoiding heavy ink-over-color / gritty figure-wide texture / airbrush modeling / glossy 3D-or-anime / silhouette-weakening busy detail. On approval, status → `LOOK RATIFIED — HERO LOCKED — READY TO AUTHOR`. **The authoring build must not begin until the hero, its provenance, and this status all exist.**

---

## 4. The authoring build (Step B) — checkpoint + TDD task list

Isolated git worktree off local `main`. Confirm `python -m pytest tests/` green before writing. TDD (red → verify-red → green → verify-green). Credential-free / stub-green ($0; no live model/MCP call, no gpt-image/Gemini/OpenAI call, no bypass of `UnwiredTransportError`). Per-directory pytest from repo root. **This is a PURE drill — lighter than nicktoon's build (no guard code; the guard already covers gpt-image).** Stop at first green for Sean's review.

### Checkpoint 1 — author `samurai-jack-s5` end-to-end (the §1.3 five-step drill)

**Task 0 — preflight.** Verify the three ratified artifacts exist (`research.md`, `refs/README.md`, `refs/samurai-jack-s5-hero.png`) and both human checkpoints are recorded. Record the two starting md5 values (§6). Confirm `python -m pytest tests/` + `python -m pytest pipeline/tests/` green (stop on unrelated red rather than absorbing it).

**Task 1 — write `tests/test_samurai_jack_s5.py` (RED — register absent).** Mirror the two sibling test files. `_SAMURAI = "samurai-jack-s5"`. Assertions:
- `test_samurai_register_is_registered` — in `ALL_REGISTERS`; `spec.name == _SAMURAI`.
- `test_samurai_plate_prompt_carries_the_register_clauses` — build a plate prompt via `_build_plate_prompt(..., style_register=_SAMURAI, has_pose_ref=False)`. **POSITIVE** (register's own vocabulary present): `"almost no visible outlines"`, `"hard-edged flat shadow"`, `"single emotional color cast"`, `"dramatic negative space"`, `"silent-samurai-film staging"` (final strings from research). **NEGATIVE leak-controls** — no pencil vocab (`"cream paper"`, `"graphite"`, `"cross-hatch"` absent) AND no primal/sibling vocab (`"weight-varying ink"`, `"over the color"`, `"gritty"` absent). **Do NOT assert bare `"outline"` absence** — the register legitimately says "almost no visible outlines."
- `test_samurai_routing_is_gpt_image_generation` — `_resolve_plate_model(_SAMURAI, {}) == GPT_IMAGE`; `..., final=True) == NB_PRO` (import the constants, not raw strings). Mirrors primal.
- `test_samurai_stub_keyword_inference` — `_infer_stub_style_register("samurai-ronin") == _SAMURAI`; earlier keywords still win (`"pixel-samurai-test" -> pixel-art-8bit`; `"primal-samurai-test" -> primal-sketch-grit`; `"nicktoon-samurai-test" -> 90s-nicktoon-grossout`); no hit -> `pencil-test-colored`.
- `test_samurai_stub_envelope_no_pencil_coercion(tmp_path)` — `CharacterDesignerNode()._build_stub_envelope(char_dir)["character_yaml"]["style_register"] == _SAMURAI` for a `samurai`-named char dir (structural; no image gen).
- `test_samurai_markers_are_exact_and_do_not_collide` — assert the exact marker set (Task 2) **and** loop over `REGISTRY` asserting no overlap with any other register's markers.
- `test_samurai_spec_is_genericized_attribute_only` — mirror nicktoon's forbidden-names test, **with one principled carve-out and punctuation normalization** (see §4.1). Forbidden list: `"samurai jack"`, `"tartakovsky"`, `"genndy"`, `"aku"`, `"ashi"`, `"scotsman"`, `"clone wars"`, `"cartoon network"`, `"adult swim"`, `"toonami"`, `"primal"`. Scan `summary + identity_lock + preserve + style_token + stub_keywords + [m for m in markers if m != _SAMURAI]`, lowercased **and with hyphens normalized to spaces** (so a stray hyphenated `"samurai-jack"` in a semantic field is caught as `"samurai jack"`, not just the space form). Exempt **only** the slug/name-marker `samurai-jack-s5` (the sole permitted franchise-derived identifier). After normalization, bare `"samurai"` (the genre word + the stub keyword) is not forbidden and stays clean.
- `test_samurai_transport_is_honest_and_unwired` — assert `spec.generation_model == GPT_IMAGE` and `GPT_IMAGE not in SUPPORTED_IMAGE_MODELS`, and one light `pytest.raises(UnwiredTransportError)` on `invoke_image_edit(..., model=spec.generation_model)`. **Do NOT re-assert the no-output / no-cache filesystem side-effects** — those are already covered at `tests/test_nb_pro_runner.py:371`; the register test only binds the register's model to the existing boundary (red-team fold, avoid duplicating the transport suite).

**Task 2 — add the `RegisterSpec`** (appended **last** in `REGISTRY`), clauses from ratified research:
- `generation_model=GPT_IMAGE`, `final_model=NB_PRO`.
- `stub_keywords=("samurai",)` — single, genre-word (scannable, low false-match), appended after the legacy six + `primal` + `nicktoon`/`grossout` (precedence preserved).
- `reference_images` — **leave default `()`** (matches all 8 existing registers; red-team fold — no code reads `spec.reference_images`, so setting it is reader-less schema-theater that contradicts the `RegisterSpec` docstring). The locked hero + provenance live in `refs/README.md` + `research.md`, per §4.1.
- `markers` (natural-phrase style, matching existing markers; **collision-checked against all 8 existing this session — clean**): `"samurai-jack-s5"` (the name), `"outline-sparse flat color shapes"`, `"hard-edged flat shadow masses"`, `"single emotional color cast"`, `"dramatic cinematic negative space"`, `"silent-samurai-film staging"`. Final text from research; keep collision-free + genericization-safe.
- **Attribute-only negatives only.** `preserve` states the register's POSITIVE (clean flat color shapes; forms read by adjacent shape + value contrast; hard-edged flat shadow shapes; dramatic negative space; single emotional color cast) — it does **not** name pencil's or primal's vocabulary as negatives (naming a neighbor evokes it — doctrine + primal §1). A candidate baseline spec is in Appendix A; the research may refine wording but must preserve the asserted phrases, the models, marker uniqueness, and the mutual-exclusion vs primal.

**Task 3 — update the `test_stub_keyword_map_full_order_snapshot` oracle** (`tests/test_register_characterization.py:181`). Append exactly one row — `("samurai", "samurai-jack-s5")` — **after** `("grossout", "90s-nicktoon-grossout")`. Do **not** reorder any prior row; do **not** add the register to `_SIX` (that list deliberately characterizes only the six pre-registry registers, byte-identical). This is the touch-point the sibling builds also hit — it is additive-only.

**Task 4 — Cy `### Example E — ronin (style_register: samurai-jack-s5)`** under `## What good looks like` in `cy-character-designer-context.md`: three sample `IR.ronin.*` records (use **valid IR categories** — verify against `criteria.py`'s `VALID_IR_CATEGORIES`; e.g. `IR.ronin.style.outline-free-color-boundaries`, `IR.ronin.palette.single-emotional-cast`, `IR.ronin.proportion.long-elegant-silhouette` — mirror primal's Example C category shape, do not invent an unvalidated `staging` category) + a four-paragraph risk-bible excerpt (drift toward heavy ink/grit + toward glossy rendering; what simplification cannot sacrifice about identity; where the research is thin; three binary human-review checks). Plus: **both closed-vocab enumeration lines** (`:13` field description and `:111` non-negotiables), **the "four examples" → "five examples" prose** (build greps for the count prose and the concluding comparison the sibling builds updated), the `templates/bible/character.yaml.template` comment line, and **add the register to `prompt-style-neutrality-doctrine.md`'s vocabulary list** (**hard test gate** — `test_prompt_style_neutrality.py:180` requires every `ALL_REGISTERS` value to appear *somewhere* in the doctrine; the vocab-list line satisfies it) **plus the "would this prompt make sense…" review question** (recommended hygiene, **not** test-enforced — red-team correction). `test_register_registry.py` completeness goes green because these now exist.

**Task 5 — state-of-record docs.** `docs/active/2026-07-04-register-backlog-and-transport-findings.md` (§3 candidate → authored/committed; §5 family-trigger → answered FOLD; roster/pending-actions updated); `CLAUDE.md` (register count 8 → 9; the gpt-image exception now names **both** registers); `AGENTS.md` (**stale — still says 7 and lacks the gpt-image exception**; bring to 9 + the two-register exception, at minimum the count + exception line); `CHANGELOG.md` (dated entry: research ratification, hero lock, new register, FOLD rationale, gpt-image gen / NB Pro final / intentionally-unwired boundary, tests added/updated, deferred runner + across-edit validation); the primal↔samurai `research.md` cross-link.

**Task 6 — verify Checkpoint 1.** Full `python -m pytest tests/` + `python -m pytest pipeline/tests/` green · characterization (6 legacy registers byte-identical; `_SIX` untouched; stub-order snapshot = prior nine rows + the one appended samurai row) · completeness (incomplete register → red) · neutrality green (auto-audits the new markers; doctrine names every register) · both sibling per-register files green · **both frozen md5 guards unchanged by hash** (`2af75906502f1caf8857e18828ceb2e4`; `945af824fa53b948a18ac6bf206d67ef`) · transport boundary intact (`SUPPORTED_IMAGE_MODELS` still the exact Gemini pair; `GPT_IMAGE` raises) · stub-green Cy smoke ($0) · `git diff --check` + `git diff --name-only` shows only the planned files · `superpowers:verification-before-completion`. **Stop for Sean's review.**

### 4.1 Two reconciliation calls worth stating explicitly (both refined by the red-team)

- **Stub keyword `("samurai",)` + hyphen-normalized genericization scan with one principled carve-out.** The stub keyword is the **genre word** `"samurai"` (chanbara — the real film genre Tartakovsky drew from, parallel to primal's "70s-pulp"; legitimately attribute language, low false-match, scannable). The show is forbidden as `"samurai jack"`. The red-team's fair catch: a raw space-form-only scan would miss a stray hyphenated `"samurai-jack"` leaking into a semantic field. So the test **normalizes hyphens to spaces** before scanning (catching both forms) and **exempts only the slug/name-marker `samurai-jack-s5`** — the one deliberate, permitted franchise-derived identifier. This is stronger than the siblings' raw-substring scan precisely because this register's slug *is* a franchise name (the siblings' slugs are not), so it earns the one carve-out. (This supersedes the draft's "no carve-out" framing.)
- **`reference_images` — do NOT set it (red-team reversal).** Verified: **no code anywhere reads `spec.reference_images`** (grep empty). Unlike `final_model=NB_PRO` — which `_resolve_plate_model(final=True)` genuinely reads (a dormant *route*, not a dormant *field*) — `reference_images` has no reader at all, so populating it is reader-less schema-theater that contradicts the `RegisterSpec` docstring ("all fields are data the touch-points read"). Leave it default `()`, matching all 8 existing registers. The locked hero + full provenance live in `registers/samurai-jack-s5/refs/README.md` + `research.md`; when the seeds→Cy style-ref bridge is eventually wired (a deferred front-door DoD piece), populating the field becomes real work with a real reader.

---

## 5. Genericization (doubly load-bearing again)

The register is a **school**, captured attribute-only: no "Samurai Jack," no "Tartakovsky"/"Genndy," no character (Jack/Aku/Ashi/Scotsman), no episode/title/logo, in any production or spike prompt, clause, marker, comment, or committed ref. `registers/samurai-jack-s5/refs/` ships empty of third-party frames by design; the sole committed image is Sean's own locked hero. The lone unavoidable named identifier is the machine slug `samurai-jack-s5` (and its exact name-marker) — internal, never a production-prompt string, exempt exactly as `90s-nicktoon-grossout`/`primal-sketch-grit` are. Same doctrine as primal/nicktoon; `docs/architecture/prompt-style-neutrality-doctrine.md` is the doctrine. The review test: **a Samurai Jack fan should recognize the school; no one should be able to name the episode.**

---

## 6. Verification gate (converged plan §8) — every "done" runs

`python -m pytest tests/` green · `python -m pytest pipeline/tests/` green · characterization (6 byte-identical; `_SIX` unchanged; stub-order snapshot additive-only) · completeness (incomplete → red) · neutrality green · both sibling register files green · transport boundary intact · **both frozen md5 guards unchanged**:
```
md5 evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md   # 2af75906502f1caf8857e18828ceb2e4
md5 pipeline/agents/prompts/sean-screenwriting-voice.md                 # 945af824fa53b948a18ac6bf206d67ef
```
· stub-green Cy smoke ($0, no keys) · `git diff --check` + `git diff --name-only` (only planned files) · CHANGELOG + CLAUDE.md + AGENTS.md updated · `superpowers:verification-before-completion`. Subscription billing only; never `ANTHROPIC_API_KEY` (GEMINI_API_KEY is fine but no live call runs in the $0 build). **Only Sean merges.**

---

## 7. Out of scope (deferred / gated) — the boundaries the drill must not cross

- Wiring a gpt-image **runner** + across-edit identity validation — gated on the costed GRANDMASTER build (separate greenlight). A green unit suite is **not** permission to run GRANDMASTER; it proves registration/prompt/routing/stub/docs/neutrality/expected-refusal, not gpt-image editing, identity-hold across turnarounds/expressions, or a costed Bible pass.
- `family: tartakovsky` field + a `tartakovsky` style skill — answered FOLD; not built.
- The rest of the §2c powerhouse roster — stays sidequest-deferred (no greenlight).
- No change to: `pipeline/agents/nb_pro_runner.py` (guard already exists) or `SUPPORTED_IMAGE_MODELS`; `tests/test_nb_pro_runner.py` (unless real behavior unexpectedly contradicts it); `pipeline/criteria.py` (owns IR/AC/impact-tag vocab, not register membership); the front-door validator (discovery semantics unchanged); Em / its eval corpus / any LLM aesthetic judge; `ROADMAP.md` (active workstream unchanged); the six locked legacy registers; the two frozen md5 files.

---

## Appendix A — candidate baseline `RegisterSpec` (research refines wording; asserted phrases preserved)

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

***Blocking bug the red-team caught + fixed here:*** the draft's `preserve` said "No cross-hatching," but `_build_plate_prompt` appends `preserve` verbatim and the per-register test asserts the substring `cross-hatch` is **absent** — the test would have stayed red. Naming pencil's vocabulary as a negative also violates the doctrine ("naming a neighbor register can evoke it"). The corrected `preserve` above states **only samurai's positives + generic anti-over-rendering refusals** that name no neighbor register's identity vocabulary — so it contains none of the six forbidden substrings (`cream paper`, `graphite`, `cross-hatch`, `weight-varying ink`, `over the color`, `gritty`). Pencil/primal drift-policing lives in the Cy risk-bible, exactly as it does for the two siblings. The build confirms the negative-leak assertions pass against the final research-authored wording.

---

## References

- `docs/research/samurai-jack-season-5-art-style-description.md` — the thin seed (research INPUT).
- `images/samuria-first-pose-chatgpt.png` — the gpt-image proof frame.
- `docs/COMPLETED/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md` §1.3 (drill), §2a (research depth), §3a (fold-vs-skill), §3b (family), §3c (transport), §4.4 (register-as-folder + refs), §5 (Checkpoint template), §8 (verification).
- `docs/superpowers/specs/2026-07-11-register-2-nicktoon-grossout-design.md` — the most recent worked example of the drill.
- `docs/active/2026-07-04-register-backlog-and-transport-findings.md` §3 (samurai candidate), §5 (family trigger), §6 (roster), §7 (pending actions).
- `tests/test_primal_sketch_grit.py`, `tests/test_90s_nicktoon_grossout.py` — per-register test templates.
- `tests/test_register_characterization.py:181` — the stub-order snapshot oracle (append-one-row touch-point).
- `registers/primal-sketch-grit/research.md` §6 — the negative-control table to invert.
- `docs/architecture/prompt-style-neutrality-doctrine.md` — the doctrine + the five-step drill.
