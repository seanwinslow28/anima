# Style-register authoring playbook

*The canonical, repeatable workflow for adding a new closed `style_register` to anima — so the pipeline is never limited to the styles it happens to have today. Read this before authoring any new register.*

**Status:** canonical runbook (2026-07-13). Distilled from three worked examples — `primal-sketch-grit` (2026-07-03/11), `90s-nicktoon-grossout` (2026-07-11), `samurai-jack-s5` (2026-07-13) — plus the [prompt style-neutrality doctrine](prompt-style-neutrality-doctrine.md) (the *why*) and the [animation-vocabulary-expansion converged plan](../active/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md) (the mechanism's origin). Where the doctrine's five-step drill and this playbook differ, **this playbook is authoritative** — it carries the full R→S→B arc and the current touch-point list; the doctrine's list predates the later touch-points.

---

## What this is

Adding a style is a **capability**, not a one-off. anima's `style_register` vocabulary is a closed set with one canonical home — [`pipeline/registers.py`](../../pipeline/registers.py), one frozen `RegisterSpec` per register, fail-loud on a nonempty unknown. Extending it is a deliberate, bounded drill that runs the same way every time. This doc is that drill.

**A register is a folder + a spec + its human touch-points**, never a bespoke skill or a code branch:

```
registers/{name}/                # mirrors the Character Bible primitive
├── research.md                  # the sourced craft write-up (Step R output)
└── refs/                        # style exemplars — NO third-party frames
    ├── README.md                # hero provenance + spike spread
    └── {name}-hero.png          # the ONE locked hero (Step S output)
```

plus one `RegisterSpec` entry in `pipeline/registers.py` and a fixed set of documentation touch-points (Step B). **No `family` field, no per-style skill** — see §"Decisions this playbook bakes in."

**When to run it:** only when Sean greenlights a *specific* named consumer or a committed future style. Registers leave the backlog **one at a time, each on Sean's explicit greenlight** ([backlog](../active/2026-07-04-register-backlog-and-transport-findings.md) §5). The playbook does not authorize a speculative fleet.

---

## The three-phase arc (R → S → B) with two human checkpoints

```
Step R  DEEP RESEARCH ($0, no code, no image gen)
        -> registers/{name}/research.md (+ refs/README.md)
        -> HUMAN CHECKPOINT 1: Sean ratifies the research
Step S  LOOK-SPIKE (COSTED, Sean-run — his eye is the SOLE arbiter, no LLM aesthetic judge)
        -> lock ONE hero frame into registers/{name}/refs/
        -> HUMAN CHECKPOINT 2: Sean confirms the hero reads as the register, cold
Step B  AUTHORING BUILD ($0, TDD, stub-green — the doctrine drill)
        -> the RegisterSpec + Cy example + markers + tests + docs, all green
[DEFERRED + GATED] wire any still-unmapped transport (fal / self-hosted) -> a separate, costed, Sean-greenlit run
```

The two checkpoints are load-bearing: **you do not spike a look the research hasn't grounded, and you do not author a register whose look Sean hasn't confirmed by eye.** Each phase is Sean-paced; a phase can be a separate session.

---

## Step R — deep research ($0, no code)

Turn a thin seed (an adjective list, a reference frame) into a wire-ready, cited craft write-up. Method: parallel deep-research subagents, one per dimension cluster (line/edge · palette/lighting · composition/form/timing · tells/negative-controls/genericization/bibliography), synthesized into `registers/{name}/research.md`. **No Python, no prompt edits, no image generation in this phase.**

`research.md` is ratifiable only when it carries:
- a **status header** (`CANDIDATE — research complete; human ratification pending`);
- a **claim ledger** mapping each thin-seed assertion → confirmed / corrected / unsupported, with a citation;
- the **seven-dimension craft account** with real depth (frame-by-frame still analysis, staging grammar, the hard-to-prompt core of the look — concretely, not adjective lists);
- a **sourced bibliography** (primary craft interviews / production commentary / first-party material — title, author/publisher, URL, access date, claims supported; no load-bearing claim resting only on the unsourced seed);
- an **honesty-flags** section (what it could *not* establish — reconstructions vs. quoted doctrine);
- a **negative-control table** vs. the confusable-adjacent registers (this is what makes registers mutually exclusive in practice);
- the **genericization rule** for this style (see §Genericization);
- the **four wire-ready outputs**: the draft `RegisterSpec`, the Cy `Example` block, the `refs/` policy + bibliography, and the transport record.

Ends at `RESEARCH COMPLETE — HUMAN CHECKPOINT 1 PENDING`.

**Human Checkpoint 1 (Sean ratifies research):** the seven-dimension account is accurate enough to author from; the negative-control axis makes the new register mutually exclusive from its neighbors in practice; the draft spec + Cy block are attribute-only; the fixed cross-engine spike prompt depicts an **original** character + setting and tests the money axes; the transport record is honest. On approval, status → `RESEARCH RATIFIED — LOOK SPIKE PENDING`.

---

## Step S — the look-spike (costed, Sean-run)

Sean runs the spike manually in the image web apps (ChatGPT / Google Flow / Higgsfield), **not** through `invoke_image_edit` — the spike is a human web task, independent of whether that model's production transport is already wired. **No LLM aesthetic judge — Sean's eye is the sole arbiter** (the eval handbook bars an LLM aesthetic judge on creative quality). Use the same research-ratified prompt / original character / original environment / aspect ratio across engines so the comparison varies **engine**, not art direction. Candidates land under `registers/{name}/refs/spike-YYYY-MM-DD/` with per-candidate provenance (product, date, exact prompt, dimensions).

**Locking the hero:** select **exactly one** candidate by eye; copy its bytes unchanged to `registers/{name}/refs/{name}-hero.png`; record in `refs/README.md` the chosen path, engine, date, exact prompt, dimensions, and Sean's one-line reason keyed to the money axes; note rejected candidates with one-line reasons. **Commit no third-party show stills** — only original spike outputs + provenance.

**Human Checkpoint 2 (hero lock):** Sean confirms **cold** that the one hero reads as the register without a franchise name in the prompt, hitting the money axes and avoiding the neighbor registers' tells. On approval, status → `LOOK RATIFIED — HERO LOCKED — READY TO AUTHOR`. **The authoring build must not begin until the hero, its provenance, and this status all exist.**

---

## Step B — the authoring build (TDD, $0, stub-green)

The pure doctrine drill in an **isolated git worktree** (per [fleet-ops](fleet-ops-protocol.md): one worktree, subscription billing only, never `ANTHROPIC_API_KEY`, clean teardown). **TDD: red → verify-red → green → verify-green.** Credential-free / stub-green — no live model / MCP / image-gen call, no bypass of the transport guard. Confirm `python -m pytest tests/` + `python -m pytest pipeline/tests/` green *before* writing. **Stop at first green for Sean's review; only Sean merges.**

**Task 0 — preflight.** Verify the three ratified artifacts exist (`research.md`, `refs/README.md`, `refs/{name}-hero.png`) and both checkpoints are recorded. Record the two frozen md5 guards (§Standing guards). Confirm both pytest dirs green (stop on unrelated red rather than absorbing it).

**Task 1 — write `tests/test_{name}.py` (RED first).** Mirror an existing per-register test file ([`tests/test_primal_sketch_grit.py`](../../tests/test_primal_sketch_grit.py) / [`tests/test_90s_nicktoon_grossout.py`](../../tests/test_90s_nicktoon_grossout.py) / [`tests/test_samurai_jack_s5.py`](../../tests/test_samurai_jack_s5.py)). Assertions:
- **registered** — in `ALL_REGISTERS`; `spec.name == {name}`.
- **plate prompt carries the clauses** — build via `_build_plate_prompt(..., style_register={name}, has_pose_ref=False)`; assert the register's own money-phrases **present** AND the neighbor registers' vocabulary **absent** (the negative leak-controls — pencil's `cream paper`/`graphite`/`cross-hatch` at minimum, plus any confusable sibling's signature words).
- **routing** — `_resolve_plate_model({name}, {}) == <gen model>` and `..., final=True) == <final model>`, **importing the model constants** (`GPT_IMAGE` / `NB2_FLASH` / `NB_PRO`), not raw strings.
- **stub keyword inference** — the new keyword resolves to `{name}`; earlier keywords still win (appended-last precedence); no hit → `pencil-test-colored`.
- **stub envelope, no pencil coercion** — `CharacterDesignerNode()._build_stub_envelope(char_dir)` returns `style_register == {name}` for a `{name}`-named char dir.
- **markers exact + no collision** — assert the exact marker set AND loop `REGISTRY` asserting no overlap with any other register's markers.
- **genericization, attribute-only** — scan `summary + identity_lock + preserve + style_token + stub_keywords + [markers except the slug]`, lowercased; assert no franchise/creator/character/studio name leaks. If the slug itself is a franchise name (e.g. `samurai-jack-s5`), **normalize hyphens to spaces** so both `foo bar` and `foo-bar` are caught, and exempt **only** the slug/name-marker.
- **transport honest + dual-map** — always assert `spec.generation_model == <MODEL>` and keep the direct-Gemini boundary exact with `SUPPORTED_IMAGE_MODELS == frozenset({NB2_FLASH, NB_PRO})`. For a Higgsfield-backed register, import `HIGGSFIELD_IMAGE_MODELS`, assert `<MODEL> not in SUPPORTED_IMAGE_MODELS` **and** `<MODEL> in HIGGSFIELD_IMAGE_MODELS`, force `ANIMA_FORCE_STUB=1`, call `invoke_image_edit(..., model=spec.generation_model)`, and assert `resp.ok and resp.stub_fallback` — outside the google-genai allowlist does **not** mean unwired when the Higgsfield map owns the model. Only when `<MODEL>` is absent from **both** `SUPPORTED_IMAGE_MODELS` and `HIGGSFIELD_IMAGE_MODELS` should the test expect `pytest.raises(UnwiredTransportError)`. Do **not** re-assert the filesystem side-effects already covered in [`tests/test_nb_pro_runner.py`](../../tests/test_nb_pro_runner.py).

Run it. **Verify RED** — every case must fail on the missing feature (`UnknownRegisterError`), not a typo.

**Task 2 — add the `RegisterSpec`** (appended **last** in `REGISTRY`), fields authored from `research.md` §1:
- `name`, `summary`, `identity_lock`, `preserve`, `style_token` (the clause text the research produced);
- `generation_model` / `final_model` (the transport record — see §Transport);
- `markers` (natural-phrase, collision-checked against all existing);
- `stub_keywords` (append AFTER the existing — precedence is oracle-pinned);
- `reference_images` — leave default `()` (no code reads it; the hero lives in `refs/`).
- **`preserve` states only positives + generic anti-over-rendering refusals** — it must name **no** neighbor register's vocabulary (naming a neighbor evokes it in the image model — the doctrine, and a real per-register-test trap: a "No cross-hatching" negative fails the `cross-hatch`-absent assertion). Drift-policing against neighbors lives in the Cy risk-bible, not in `preserve`.

Run the per-register test. **Verify GREEN.**

**Task 3 — update the stub-order snapshot oracle** ([`tests/test_register_characterization.py`](../../tests/test_register_characterization.py)). Append exactly **one row per new stub keyword**, AFTER the existing rows. Do **not** reorder any prior row; do **not** touch the pre-registry `_SIX` list (it pins the six legacy registers byte-identical).

**Task 4 — the human touch-points** (each is enforced by a completeness test in [`tests/test_register_registry.py`](../../tests/test_register_registry.py) unless noted):
- **Cy `### Example {X} — {char} (style_register: {name})`** under `## What good looks like` in [`cy-character-designer-context.md`](../../pipeline/agents/prompts/cy-character-designer-context.md): three sample `IR.{char}.*` records in **valid `criteria.py` `VALID_IR_CATEGORIES`** (`anatomy/hair/face/proportion/palette/costume/prop/pose/motion/style/view` — do NOT invent a category) + a four-paragraph risk-bible (drift directions toward each named neighbor's *attributes*; what simplification cannot sacrifice about identity; where the research is thin; three binary human-review checks).
- **Both closed-vocab enumeration lines** in the Cy context (the `character.yaml` field description + the non-negotiables list).
- **The "N examples" prose** — bump the count in both the intro sentence and the closing comparison paragraph (the completeness build greps for these).
- **The `character.yaml.template` permitted-values comment** ([`templates/bible/character.yaml.template`](../../templates/bible/character.yaml.template)).
- **The doctrine vocabulary-list line** in [`prompt-style-neutrality-doctrine.md`](prompt-style-neutrality-doctrine.md) — this is the **hard neutrality gate** ([`tests/test_prompt_style_neutrality.py`](../../tests/test_prompt_style_neutrality.py) requires every `ALL_REGISTERS` value to appear in the doctrine) — plus the register in the "would this prompt make sense to a … author?" review question (recommended hygiene, not test-enforced).

**Task 5 — state-of-record docs.** [Backlog](../active/2026-07-04-register-backlog-and-transport-findings.md) (candidate → authored; any triggers it resolves); `CLAUDE.md` + `AGENTS.md` (register count + any transport exception — keep them in sync); `CHANGELOG.md` (dated entry: checkpoints, new register, transport boundary, tests added/updated, deferred runner); any reciprocal research cross-links to a sibling register; `research.md` §0/§9 status → authored. `ROADMAP.md` is **not** rewritten by an individual register — the register-expansion capability is a standing workstream there (see its scorecard row).

**Task 6 — the verification gate** (every item runs before "done"):
- `python -m pytest tests/` green · `python -m pytest pipeline/tests/` green;
- characterization: the six legacy registers byte-identical (`_SIX` untouched); the stub-order snapshot = prior rows + the appended new row(s);
- completeness green (an incomplete registration goes red) · neutrality green (auto-audits the new markers; the doctrine names every register);
- every sibling per-register test file green;
- **both frozen md5 guards unchanged by hash** (§Standing guards);
- transport boundary intact — `SUPPORTED_IMAGE_MODELS` is still exactly `{NB2_FLASH, NB_PRO}`; Higgsfield-backed models are present in `HIGGSFIELD_IMAGE_MODELS`; only a model absent from **both** maps raises;
- stub-green Cy smoke ($0, no keys) — a `{name}`-named char authors a coherent stub Bible in the register, never silent pencil;
- `git diff --check` + `git diff --name-only` show only the planned files;
- run `superpowers:verification-before-completion`.

Stop for Sean's review; **only Sean merges.**

---

## Transport (the recorded model + escalation ladder)

The `RegisterSpec` records the **honest** generation model. The decision procedure ([converged plan](../active/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md) §3c):

1. **NB2 default** (`gemini-3.1-flash-image`) — author clauses → spike the hero via NB2 from text → Sean's eye. Reads as the register → done (e.g. `90s-nicktoon-grossout`, NB2 GO).
2. Close-but-not-there → spike NB2 **with a `refs/` style image fed in** (watch for the Flo-B identity-morph).
3. NB2 fundamentally can't render it → **record a different model** (`gpt-image-2` for `primal-sketch-grit` + `samurai-jack-s5` + `flat-cast-painted-world`; NB Pro for painterly finals; the ticketed fal / self-hosted-FLUX-LoRA path). `final_model = NB_PRO` is the dormant painterly-final seam convention.

**If the recorded model has no wired runner**, the register is authored honestly and **fails loud**: `invoke_image_edit` raises `UnwiredTransportError` when the model has neither a google-genai mapping in `SUPPORTED_IMAGE_MODELS = {NB2_FLASH, NB_PRO}` nor a Higgsfield mapping — never a silent fallback. Since 2026-07-13 the gpt-image transport **IS wired** — via Higgsfield ([`pipeline/agents/higgsfield_runner.py`](../../pipeline/agents/higgsfield_runner.py), decision D4/D5 in [`docs/active/2026-07-13-transport-strategy-decision.md`](../active/2026-07-13-transport-strategy-decision.md)); a register recording `gpt-image-2` generates through it. The fail-loud rule still governs any model with neither a google-genai nor a Higgsfield mapping. Wiring any other transport runner plus its across-edit identity validation remains a separate, costed, Sean-greenlit build. A green $0 authoring suite proves registration/prompt/routing/stub/docs/neutrality and the expected transport behavior — **not** live generation.

---

## Genericization (doubly load-bearing every time)

A register is a **school** of craft, captured **attribute-only**: no show, creator, character, episode, studio, or logo in any production prompt, clause, marker, comment, or committed ref. `refs/` ships empty of third-party frames by design — the only committed image is Sean's own locked hero. The sole permitted named identifier is the machine slug (and its exact name-marker) — internal, never a production-prompt string, exempt in the genericization test exactly as the existing registers are. Full doctrine + the five-step drill: [`prompt-style-neutrality-doctrine.md`](prompt-style-neutrality-doctrine.md). The review test: **a fan of the school recognizes the school; no one can name the episode.**

---

## Decisions this playbook bakes in (do not re-litigate per register)

- **FOLD, not a skill.** A register = `RegisterSpec` + Cy block + markers + `refs/` + tests + docs. A standalone style skill is *promoted*, never assumed — it needs ≥2 real consumers AND standalone reusable structure (converged plan §3a). None qualifies today.
- **No `family` field.** Flat registers, no metadata-family abstraction — it has no reader in v1 (the front-door anti-pattern). Related registers are linked by **documentation** (reciprocal `research.md` cross-links), not code. The Tartakovsky pair (`primal-sketch-grit` ↔ `samurai-jack-s5`) is the worked example — answered FOLD.
- **The MLLM-critic lesson.** Do not build a bespoke Em eval corpus + costed baseline + calibration campaign *per register/character* — that does not scale and is the exact over-investment the ROADMAP exists to prevent. If a faint-feature nuance ever becomes load-bearing, back it with **one cheap deterministic T1 rule authored once**, never an MLLM calibration campaign.

---

## Standing guards (must not move without a deliberate, ratified change)

```
md5 evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md   # 2af75906502f1caf8857e18828ceb2e4
md5 pipeline/agents/prompts/sean-screenwriting-voice.md                 # 945af824fa53b948a18ac6bf206d67ef
```

Also do not touch (unless real behavior contradicts them): `pipeline/agents/nb_pro_runner.py`'s transport guard or `SUPPORTED_IMAGE_MODELS`; `pipeline/criteria.py`'s IR/AC/impact-tag vocab (it owns criteria categories, not register membership); the six locked legacy registers.

---

## Worked examples (read one before starting)

| Register | Transport | Notable | Design doc |
|---|---|---|---|
| `primal-sketch-grit` | gpt-image (Higgsfield-wired) | first post-registry register; GRANDMASTER's gritty register; fork #1 transport pivot; **T2 in-register GRANDMASTER validation pending** | `registers/primal-sketch-grit/research.md` |
| `90s-nicktoon-grossout` | NB2 (wired) | the appealing-default correction; ai-guru pilot consumer | `registers/90s-nicktoon-grossout/research.md` |
| `samurai-jack-s5` | gpt-image (Higgsfield-wired) | the flat Tartakovsky sibling; the lightest drill at authoring time; the hyphen-normalized genericization carve-out; T2 validation pending with GRANDMASTER | [`docs/active/2026-07-11-samurai-jack-s5-register-design.md`](../active/2026-07-11-samurai-jack-s5-register-design.md) |
| `flat-cast-painted-world` | gpt-image (Higgsfield-wired) | the mixed-media fusion register; NB2 confirmation NO-GO; T2 validation pending before its first production Bible pass | [`registers/flat-cast-painted-world/research.md`](../../registers/flat-cast-painted-world/research.md) |
