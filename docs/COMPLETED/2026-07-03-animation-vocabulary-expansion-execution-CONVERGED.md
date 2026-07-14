# Animation vocabulary expansion — the register registry + the powerhouse pattern — Converged Execution Plan (Opus + Codex + red-team)

**Date:** 2026-07-03
**Completed / historical (archived 2026-07-13).** This is the ratified execution plan that produced the register registry and the first four authored expansion registers. Its body, including then-current preview model IDs and pending-state language, is preserved as historical execution evidence; current runtime truth lives in `pipeline/registers.py`, ROADMAP, and the style-register authoring playbook.

**Status:** Completed historical execution plan (design ratified by Sean across four brainstorm sections + two live addenda).
**Predecessor:** [`docs/active/2026-07-03-animation-vocabulary-expansion-scope.md`](../active/2026-07-03-animation-vocabulary-expansion-scope.md) — the scope + prior decisions. This doc turns that scope into an execution plan.
**Relation to ROADMAP:** within the active **outward-turn workstream** ("the tool + more characters/styles"). A **production unblock** for a greenlit piece (GRANDMASTER), *not* a new workstream. The full powerhouse roster is deferred to the post-front-door-DoD sidequest.
**Method model:** mirrors [`2026-07-03-frontdoor-slice4-stress-test-CONVERGED.md`](../active/2026-07-03-frontdoor-slice4-stress-test-CONVERGED.md) — position → TDD tasks with real test code → verification → checkpoints → risks → Codex reconciliation → red-team fold. Right-sizing honesty throughout.

---

## 0. The one-sentence goal

Turn the closed six-register `style_register` vocabulary into a **deliberately-growing, still-closed** multi-animator style powerhouse — by consolidating the scattered register touch-points (the table in §1.1 is authoritative) into one canonical **registry module** that fails loud on an incomplete registration, then authoring the first production-blocking register (`primal-sketch-grit`) into it as the worked example of the reusable pattern.

**What this is:** a registry module (safe refactor of existing scattered state) + one new register + the reusable extension pattern + the per-style research agenda.
**What this is NOT:** an open-ended freeform style string; the full powerhouse roster; any costed run in the build session; any change to Em, the two frozen md5 guards, or the pencil-test reference implementation's byte-for-byte behavior.

**The load-bearing constraint (the powerhouse must not break it):** the vocabulary stays **closed**. Each register is authored deliberately — its own clause data, its own "what good looks like" Cy block, its own neutrality markers, grounded against its own reference images. Closedness is what keeps every agent prompt style-neutral and testable (the doctrine's thesis: *validators cannot recover taste that was absent at generation time*). The registry module makes closedness **enforced** rather than merely conventional; it does not make per-style taste free.

---

## 1. The reusable extension pattern (open here — the powerhouse playbook)

### 1.1 The finding that reframes the deliverable (verified against main, 2026-07-03)

The doctrine and the scope doc both say **step 1 is "extend the vocabulary in `pipeline/criteria.py`."** That is **wrong against main.** `criteria.py` contains no `style_register` vocabulary, and **nothing anywhere validates a register against a closed set.** The register actually threads through *five* places, and the two the doctrine omits are the load-bearing ones:

| Touch-point | File | If you skip it | In the doctrine's "3-step"? |
|---|---|---|---|
| `_REGISTER_CLAUSE_LIBRARY` (identity_lock / preserve / style_token) | `pipeline/agents/character_designer.py` (~L1153) | Register **silently falls back to pencil-test-colored** clauses via `.get(x) or _DEFAULT` — Cy authors the wrong look, no error | ❌ omitted — **load-bearing** |
| `_REGISTER_MODELS` (transport routing) | `pipeline/agents/character_designer.py` (~L1230) | Silently falls back to the pencil default row | ❌ omitted |
| `character.yaml.template` comment (human closed-list) | `templates/bible/character.yaml.template` | Sean/Cy can't see the register is legal | ◑ (the doctrine's "step 1b") |
| `## What good looks like — {register}` block | `pipeline/agents/prompts/cy-character-designer-context.md` | Cy has no worked example of the look | ✅ step 2 |
| `_STYLE_REGISTERS` + `_REGISTERS_TO_MARKERS` | `tests/test_prompt_style_neutrality.py` | Neutrality guard can't check the register's markers | ✅ step 3 |
| `_STUB_STYLE_REGISTER_BY_KEYWORD` (optional) | `pipeline/agents/character_designer.py` (~L1374) | The `--stub` Cy smoke defaults the register to pencil | ❌ (only for the smoke) |
| Front-door validator (Codex-found) | `pipeline/frontdoor/validate.py` (~L18-24, 68-72) | Checks `style_register` **presence, not membership** — an unregistered register passes the front door silently | ❌ omitted — **soft-flag surface** (§10) |

So the "reusable extension pattern" deliverable is **not** "write down the doctrine 3-step." It is: **build a registry module that makes these one place, fix the doctrine's criteria.py error, and make an incomplete registration fail loud.**

### 1.2 The registry module (the mechanism)

One new module, `pipeline/registers.py`, is the single source of truth. Each register is one frozen `RegisterSpec`; the touch-points import from it.

```python
# pipeline/registers.py  — the canonical home of the closed vocabulary
from dataclasses import dataclass

@dataclass(frozen=True)
class RegisterSpec:
    name: str                    # "primal-sketch-grit"
    summary: str                 # one line for the character.yaml.template human list
    identity_lock: str           # was _REGISTER_CLAUSE_LIBRARY[x]["identity_lock"]
    preserve: str                # was ...["preserve"]
    style_token: str             # was ...["style_token"]
    generation_model: str        # was _REGISTER_MODELS[x]["generation"]
    final_model: str             # was _REGISTER_MODELS[x]["final"]
    markers: frozenset[str]      # was _REGISTERS_TO_MARKERS[x]  (may be just {name})
    stub_keywords: tuple[str, ...] = ()      # reverse of _STUB_STYLE_REGISTER_BY_KEYWORD
    reference_images: tuple[str, ...] = ()   # style exemplars that DEFINE the look (Section 4.4)

REGISTRY: dict[str, RegisterSpec] = { ... }   # the 6 existing + primal-sketch-grit
ALL_REGISTERS = frozenset(REGISTRY)

class UnknownRegisterError(ValueError):
    pass

def get_register(name: str) -> RegisterSpec:
    try:
        return REGISTRY[name]
    except KeyError:
        raise UnknownRegisterError(name)   # loud, not silent-coerce
```

**Back-compat rule (keeps old characters working):** a **nonempty, unrecognized** register (a typo, or a style you forgot to register) → `UnknownRegisterError`. An **empty/missing** `style_register` → still defaults to `pencil-test-colored` (the existing behavior every old character folder relies on). Empty → pencil default; nonempty-unknown → loud error. This is the exact fix for the silent-wrong-default that Sean flagged.

### 1.3 The corrected extension pattern — add one register end to end

After the module lands, "add a style" collapses from a multi-file scavenger hunt (§1.1 table) to a known drill:

1. **Research** the style (the per-style research agenda, §2) — grounded against its reference images.
2. **Add one `RegisterSpec` entry** to `REGISTRY` — the research fills the fields (name, clauses, models, markers, refs).
3. **Add the `## What good looks like — {name}` prose block** to `cy-character-designer-context.md`.
4. **Add the one-line summary** to `character.yaml.template`'s comment.
5. **Run the suite.** The completeness test **refuses to pass** until 2–4 all exist for the new register. Incomplete registration fails loud, not silent.

**The minimal per-register deliverable (so registers 3-through-N are cheap):** *one `RegisterSpec` entry + one Cy prose block + one template-comment line*, backed by the research's four outputs (§2a). Everything else (routing, marker checking, stub inference, sync enforcement) is handled by the module. Steps 3–4 stay prose because that is authored **taste**, not data; step 5 enforces they exist.

This corrects and supersedes the doctrine's 3-step. `prompt-style-neutrality-doctrine.md` gets updated to point at the registry as step 1 (fixing the criteria.py error) as part of Checkpoint 2.

---

## 2. The per-style research agenda (primary deliverable)

### 2a. The research-brief template

Seven dimensions, each written so its output **drops into a specific machine field** — that's what keeps research from producing prose that doesn't wire in. The rule: research answers *"what makes the look the look,"* grounded against the register's `refs/`, never surface pastiche.

| # | Dimension | The question | Fills |
|---|---|---|---|
| 1 | **Line & contour** | Weight (uniform vs varied)? Medium (ink/graphite/vector)? Edge (clean/wet/rough)? Outline color (black vs self-colored darker-value)? Construction lines visible? | `style_token`, `preserve`, markers |
| 2 | **Palette & color logic** | Saturated vs desaturated? Naturalistic vs not? Per-location palettes? Flat fills vs gradients? Indexed vs open? How does shadow get its color? | `style_token`, a palette `IR.*`, markers |
| 3 | **Shading / render register** | Cross-hatch / dither / cel / painterly / flat / gradient? Is volume rendered or refused? | `preserve`, markers |
| 4 | **Form & proportion grammar** | Flat-angular vs rubbery vs realistic? Silhouette-readability? Proportion tendency? How is expression exaggerated? | `identity_lock`, a proportion `IR.*`, Cy block |
| 5 | **Texture & surface** | Paper/film grain? Gritty vs clean? Do figure and background share one treatment or split? | `style_token`, markers |
| 6 | **Timing & motion grammar** | Holds, smears, spacing? "Timing as a song"? Move→hold→burst? Limited vs full? | The piece's timing bible + motion `IR.*` (informs Bea/Mo more than the still register) |
| 7 | **Signature tells + what-it's-NOT** | The 2–3 instant-recognition tells? The adjacent registers it's confused with, as explicit contrast? | The money-shot + `preserve` negatives + risk-bible |

**The four required outputs** (so the research is wire-ready, not an essay):
1. A **draft `RegisterSpec`** — name, summary, `identity_lock`, `preserve`, `style_token`, `generation_model`, `final_model`, `markers`.
2. The **Cy block** — 3 sample `IR.*` entries + a 4-paragraph risk-bible excerpt, in the register's own vocabulary.
3. The **`refs/` set + a sourced bibliography** (the images + where the craft claims came from).
4. A **transport recommendation** — can NB2 hit this from text clauses alone, or does the evidence say spike a style-ref-fed generation or a different transport? (Feeds the go/no-go.)

**Depth requirements (so the seven dimensions don't collapse into a surface-pastiche checklist — the scope's "extensive and first-class" bar).** The research is not done until it also produces: (a) **frame-by-frame still analysis** of real exemplars, not adjectives — trace how a specific line, shadow, or hold is actually built; (b) **composition & staging grammar** (camera height, letterbox usage, negative space, figure placement); (c) the **figure/background paint *process*** — *how* the grit/texture is made, not just that it exists; (d) **negative controls** — the register held side-by-side against its nearest confusable (Primal vs Samurai-Jack; Ren & Stimpy vs Rugrats), so `preserve`'s negatives are grounded in a real contrast; (e) a **non-derivative / genericization rule** — capture the *look* without reproducing a specific copyrighted frame or a real tool's recognizable UI (the ai-guru concept's own non-negotiable; homage, not copy).

**Method:** Fable 5 parallel deep-research subagents, one per dimension cluster, synthesized into the four outputs — then **Sean's eye ratifies the look against an art-viz frame** (the eval handbook bars an LLM aesthetic judge on creative quality; the taste call is human). "Does a generated frame read as this register" is the verification, not a metric.

### 2b. The two production blockers, filled to "brief + known + gap"

Pre-filled from the craft bibles already in the two concept docs; the deep-dive *adds* the gaps. **The research is NOT run in this planning session.**

**`primal-sketch-grit` (Tartakovsky's *Primal*)** — GRANDMASTER's blocker
- **Known** (concept §Genndy bible; AWN Primal interview; Animation Obsessive; canmom.art): raw, visible, **weight-varying** hand-drawn ink, heavier weight; gritty **painterly** texture, raw not clean; warm earthy **desaturated**, non-naturalistic per-location; figure + background **share** the hand-drawn treatment; timing-as-a-song, move→dead-stop-hold→burst.
- **What-it's-NOT** (load-bearing): **not** Samurai-Jack flat-no-outline; **not** `line-art-only` (bold *uniform* outlines — the opposite); **not** `pencil-test-colored` (graphite line + cream paper + cross-hatch).
- **Gap:** precise line-weight *logic*, exact palette derivation, how the painterly grit is achieved, and the transport verdict (NB2-from-text vs a Primal style-ref feed).
- **RESEARCH CORRECTIONS (Checkpoint-1 deep-dive, 2026-07-03 — these SUPERSEDE the concept doc's craft claims; the register is authored from these, not the pre-fill above):**
  1. **The candy/oil-geyser blood convention is *Samurai Jack's*, not *Primal's*.** Primal's real tell is **explicit shock-colored blood**. So GRANDMASTER's candy geyser is a **deliberate cross-register staging choice** (Samurai-Jack's blood-substitution applied to a piñata), **not a `primal-sketch-grit` register feature** — the register spec must NOT claim the oil-geyser as its own tell.
  2. **"Flat angular figures" under-describes Primal.** The register is **organic-illustrative** with a heavy **weight-varying contour kept *over* the color** (Tartakovsky: "very new for us") — flat-angular is the Samurai-Jack read, not Primal.
  3. The concept's "2–4s pre-strike hold" **conflates two holds** — the scene-scale stand-off vs the 0.5–2s dead-stop accent (a timing/staging note for Bea, not the still register).

**`90s-nicktoon-grossout` (Ren & Stimpy)** — ai-guru's blocker
- **Known** (concept §style bible): wet, alive linework, **self-colored** line, thick rubbery outlines, no dead-clean-for-tidiness outlines; flat **unnaturalistic** color, sickly greens; extreme close-up detail (wrinkles/pores) at gross-out beats; **unhinged proportions**, grotesque distortion; tell = one fully-committed gross-out distortion, don't cut away early.
- **What-it's-NOT:** **not** Rugrats (Klasky-Csupo — rounder, not gross-out; a *different* 90s-Nick register); **not** clean/glossy; **not** pencil-test.
- **Gap:** John K's broken-construction head logic, the wet-edge line rule, and the **genericizing** discipline (capture the *style* without reproducing a specific real show/tool — the concept's own non-negotiable).

### 2c. The powerhouse roster (sketched, not filled — deferred to the post-DoD sidequest)

The *backlog*, held to the research agenda. **Not a build list.** The transport-risk column front-loads which registers will need a non-NB2 spike (§3c).

| Register (candidate) | Signature tell | Transport risk |
|---|---|---|
| `tartakovsky-samurai-jack` | Flat color, **no outline**, near-silhouette | Med |
| `ghibli-painterly-cel` | Soft painted cel, naturalistic light | Low–med |
| `spiderverse-halftone` | Ben-Day dots + chromatic offset + on-2s motion | **High** |
| `fleischer-cuphead-rubberhose` | 1930s rubber-hose, boil, film grain | Med |
| `upa-midcentury-modern` | Flat geometric limited-modernist | Low |
| `bakshi-rotoscope` | Traced-motion realism over paint | **High** |
| `adventure-time-flat-graphic` | Noodle limbs, flat fills, thin uniform line | Low |
| `aardman-claymation` | Fingerprinted clay, stop-motion surface | **High** |
| `klasky-csupo-rugrats` | Lumpy heads, squiggle contour, flat palette | Low–med |

---

## 3. Positions the scope doc left to "the research"

### 3a. Fold-first; a standalone style skill is promoted, never assumed
**Default: fold.** A register = `RegisterSpec` entry + Cy block + markers + `refs/`. No skill.
**A standalone style skill** (the AKCodez scaffold — hook → bracketed master template → domain encyclopedia → worked examples, portable SKILL.md driven through the Higgsfield MCP) is promoted **only when BOTH**: (a) **≥2 real consumers** of the look (≥2 greenlit pieces) *or* research surfaces reusable structure spanning **≥2 registers**; **and** (b) the look has **standalone reusable structure**, not merely "it's a great style."
**primal-sketch-grit → FOLD** (one consumer). Mirrors EXPAND/ART-VIZ shipping as inline disciplines with zero new code.

### 3b. No register-family abstraction now (flat registers)
"Tartakovsky" is **two flat registers** (`primal-sketch-grit`, a future `tartakovsky-samurai-jack`), only the first with a consumer. The registry scales to 50 **flat** registers with no family concept — a family would be *sugar* (shared clause strings), not a scaling requirement. **Deferred trigger:** reopen when a 2nd Tartakovsky register greenlights (which is also when the `tartakovsky` skill question reopens — they move together).

### 3c. Transport: NB2-by-default, per-register spike as the instrument
**Default: NB2** (`gemini-3.1-flash-image-preview`) — the `_REGISTER_MODELS` generation default; the choice is **recorded in the `RegisterSpec`**. Decision procedure: author clauses → spike hero frame via NB2 from text alone → Sean's eye. Reads as the register → done. Close-but-not-there → spike NB2 **with a `refs/` style image fed in** (watch for the Flo-B identity-morph). NB2 fundamentally can't → escalate to NB Pro or the ticketed **fal / self-hosted-FLUX-LoRA** path (costed, Sean-gated, never speculative). The roster's transport-risk column marks which registers to expect this for.

---

## 4. Architecture

### 4.1 The module + the five refactored touch-points
`pipeline/registers.py` owns the **data** (clauses, routing, markers, stub keywords, refs). The touch-points become thin reads:
- `_build_plate_prompt` / `_resolve_plate_model` (`character_designer.py`) → `get_register(style_register)`.
- `_STUB_STYLE_REGISTER_BY_KEYWORD` → derived from the specs' `stub_keywords`.
- `test_prompt_style_neutrality.py` → imports `ALL_REGISTERS` + markers from the registry (the test can never drift from the canon).
- `character.yaml.template` comment + the Cy `## What good looks like — {register}` block **stay prose** — but the completeness test asserts one exists per register in the canon.

### 4.2 The safety invariant (the load-bearing TDD discipline)
Before any refactor, capture a characterization snapshot of the **exact plate-prompt string + model routing for all 6 current registers**. The refactor is "green" only when that snapshot is **byte-identical** afterward — proving no existing character (sean, mascot) shifts. Cy's hot path (`_build_plate_prompt`) is under the cache-key lock; a byte change would break the locked Bibles.

### 4.3 The two frozen md5 guards (must not move)
- `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` → `2af75906502f1caf8857e18828ceb2e4`
- `pipeline/agents/prompts/sean-screenwriting-voice.md` → `945af824fa53b948a18ac6bf206d67ef`
Neither is touched by register work (one is an Em eval trace, one is Sam/Bea's voice). The register work touches Cy's plate prompts + the neutrality test + the Cy context markdown — none of them the guarded files. Verified by hash at the verification gate.

### 4.4 Hero-frame persistence — ART-VIZ → brief → register → go/no-go
The front-door **ART-VIZ stage persists the confirmed hero frame(s)** into the brief folder — durable, first-class, using fields that already exist:
```
briefs/{piece}/
├── concept.md, 00_studio_brief.md, character_seeds.yaml   # style_ref_ids → the saved frames
└── style-refs/           # the confirmed hero frame(s)
```
**What is real today vs. deferred (red-team correction).** Saving the frames into `briefs/{piece}/style-refs/` is real — they're files on disk. `character_seeds.yaml`'s `style_ref_ids: []` carries the paths as **metadata that today is passthrough only**: `tests/test_frontdoor_emit.py:112` documents *"no pipeline code reads style_ref_ids yet."* So **Cy consuming these frames is a deferred future wire** — the seeds→Cy bridge the scope doc flags as a separate front-door DoD piece — **not claimed as current behavior** and **not built in this pilot.** What the pilot *does* use, needing no code, is the saved frame as the **human-in-the-loop go/no-go target** (§6).

**The honesty nuance:** the brainstorm frame confirms *"is this the style I want"* (Sean's taste, from a freeform art-viz prompt). It does **not** prove *"NB2 can reproduce it from the authored register, holding identity"* — that stays the go/no-go, now measured against the **saved target frame** instead of memory. **Refinement:** prefer generating the confirmed frame on **NB2** (the register's transport) so "the style I'm confirming" equals "the style the pipeline can build"; if art-viz used a different engine, the go/no-go re-confirms on NB2.

**A register is a folder** (mirrors the Character Bible primitive):
```
registers/{name}/
├── refs/            # style exemplars (research-sourced + the piece's confirmed hero frame)
└── research.md      # the deep-research write-up (§2a output)
```

---

## 5. Per-checkpoint TDD task list

Worktree isolation, branched from local main. Confirm `python -m pytest tests/` green before writing. TDD (red → verify-red → green → verify-green). Credential-free / stub-green. Tests run per-directory from the repo root.

### Checkpoint 1 — the registry module, proven safe (**the Fable-5 build STOPS here for Sean's review**)

**Task 1.0 — Characterization snapshot (capture BEFORE refactor).** The byte-identical oracle. Records the exact `_build_plate_prompt` output + `_resolve_plate_model` result for all 6 current registers across the **full input surface** the red-team flagged, not just `has_pose_ref`:
- `has_pose_ref` ∈ {True, False}
- **`is_prop=True`** — the prop path bypasses register lookup (`character_designer.py:1288`); snapshot it to prove the refactor left it untouched.
- **a `char_cfg` manifest override present** — `_resolve_plate_model` honors a per-character `generation_model`/`final_model` override (`:1246`); snapshot with and without so override precedence is preserved.
- **the full cache key**, not just the prompt string — the cache key (`nb_pro_runner.py:235`) includes prompt + model + rule cites + reject + refs and is what actually protects the locked Bibles. Rule-cites/reject/refs are **not** register-derived (so unchanged by construction), but assert the composed cache key for a representative plate is byte-identical as the strongest guard.
```python
# tests/test_register_characterization.py  (RED first: write against current behavior, must pass on main)
import pytest
from pipeline.agents.character_designer import _build_plate_prompt, _resolve_plate_model

_SIX = ["pencil-test-colored","pixel-art-8bit","line-art-only","watercolor","photoreal","3d-rendered"]

@pytest.mark.parametrize("reg", _SIX)
@pytest.mark.parametrize("has_pose_ref", [True, False])
@pytest.mark.parametrize("is_prop", [True, False])
def test_plate_prompt_snapshot(reg, has_pose_ref, is_prop):
    got = _build_plate_prompt("neutral standing pose", style_register=reg,
                              has_pose_ref=has_pose_ref, is_prop=is_prop)
    assert got == _EXPECTED_PROMPT[(reg, has_pose_ref, is_prop)]   # frozen literal from main

@pytest.mark.parametrize("reg", _SIX)
def test_model_routing_snapshot(reg):
    base = (_resolve_plate_model(reg, final=False), _resolve_plate_model(reg, final=True))
    override = _resolve_plate_model(reg, {"generation_model": "X", "final_model": "Y"})
    assert (base, override) == _EXPECTED_ROUTING[reg]   # frozen literals capture override precedence
```
*(Inline the expected strings as frozen literals — the suite is credential-free and must stay dependency-light.)*

**Task 1.1 — Build `pipeline/registers.py`.** `RegisterSpec`, `REGISTRY` (the 6 existing, values copied verbatim from `_REGISTER_CLAUSE_LIBRARY` + `_REGISTER_MODELS` + `_REGISTERS_TO_MARKERS`), `get_register` (empty→pencil default handled by CALLERS, nonempty-unknown→`UnknownRegisterError`), `ALL_REGISTERS`.

**Task 1.2 — Refactor the touch-points to read from the registry.** `_build_plate_prompt`, `_resolve_plate_model`, `_STUB_STYLE_REGISTER_BY_KEYWORD`, and `test_prompt_style_neutrality.py` all import from `registers.py`. Verify Task 1.0 snapshots stay byte-identical (verify-green).

**Task 1.2b — Invert the two silent-fallback tests (Codex-found; REQUIRED, not optional).** `tests/test_character_designer.py:1175-1182` ("unknown register falls back to pencil") and `:1275-1276` (unknown model routing returns NB2) currently *lock in* the silent coercion. Fail-loud breaks them by design. Rewrite both so a **nonempty-unknown** register asserts `UnknownRegisterError` (or the raise at the caller), while a separate case confirms **empty/missing still defaults to pencil-test-colored** (back-compat preserved). Grep for any other test relying on silent coercion before flipping.

**Task 1.2c — Front-door validator reads the registry as a SOFT flag (Codex-found).** `pipeline/frontdoor/validate.py` gains a membership check against `ALL_REGISTERS` that **warns, does not fail**, on an unrecognized register — because the front door is where a *new* register is discovered (the seeds already carry a NEW-flag + doctrine pointer). Discovery warns; Cy execution hard-fails. Keep any existing front-door tests green; add one asserting a NEW register warns rather than raises.

**Task 1.3 — The registry sync + completeness test.** The enforcement that makes "closed" real:
```python
# tests/test_register_registry.py
from pipeline.registers import ALL_REGISTERS, REGISTRY
from pathlib import Path

def test_every_register_is_complete():
    for name, spec in REGISTRY.items():
        assert spec.identity_lock and spec.preserve and spec.style_token
        assert spec.generation_model and spec.final_model
        assert spec.markers                       # at least {name}

def test_every_register_has_a_cy_block():
    cy = Path("pipeline/agents/prompts/cy-character-designer-context.md").read_text()
    section = cy.split("## What good looks like", 1)[1]        # scope to the examples section
    section = section.split("\n## ", 1)[0]                     # ...up to the next H2
    for name in ALL_REGISTERS:
        assert f"style_register: {name}" in section, \
            f"{name} has no example block under '## What good looks like'"

def test_every_register_is_in_the_template_comment():
    tmpl = Path("templates/bible/character.yaml.template").read_text()
    for name in ALL_REGISTERS:
        assert name in tmpl

def test_unknown_register_raises_not_coerces():
    import pytest
    from pipeline.registers import get_register, UnknownRegisterError
    with pytest.raises(UnknownRegisterError):
        get_register("totally-made-up-register")
```
*(Matcher is **section-scoped** (red-team fix): the existing blocks are `### Example A — sean-anchor (style_register: pencil-test-colored)` under one `## What good looks like` H2, so the check requires `style_register: {name}` **inside that section** — green for all 6 today (add the new register's example block to make it green for #7), red only for a register with no block. It guarantees a block *exists*; whether the block is *substantive* stays a human review — prose quality isn't cheaply assertable.)*

**Task 1.4 — Verify Checkpoint 1.** Full `python -m pytest tests/` green (+ the new tests); characterization byte-identical; both md5 guards verified by hash; `superpowers:verification-before-completion`. **Stop for Sean's review.**

### Checkpoint 2 — `primal-sketch-grit` authored (continuation after review)

**Task 2.1 — Deep Primal research** (Fable 5 parallel subagents, §2a) → the four outputs. Sean ratifies the look against an art-viz frame.

**Task 2.2 — Add the `RegisterSpec`** for `primal-sketch-grit` to `REGISTRY` (clauses from the research; `generation_model` = NB2 hypothesis; `markers` = the load-bearing Primal drift phrases, e.g. `"weight-varying ink"`, `"gritty painterly texture"`, `"warm earthy desaturated"` — chosen so they don't collide with existing markers).

**Task 2.3 — Add the Cy `## What good looks like — primal-sketch-grit` block** (3 `IR.*` + 4-para risk-bible excerpt, Primal vocabulary) and the `character.yaml.template` one-line summary. `test_register_registry.py` now goes green *because* these exist (it was red for the new register until now).

**Task 2.4 — Update the doctrine** (`prompt-style-neutrality-doctrine.md`): step 1 points at `pipeline/registers.py` (fixing the criteria.py error); the pattern is the §1.3 five-step drill.

**Task 2.5 — Stub-green Cy authoring smoke.** Drive Cy with `style_register: primal-sketch-grit` in `--stub` mode (e.g. `scripts/author_bible.py characters/kid/ ... --stub`, or a targeted test) → a coherent stubbed Bible, **no silent pencil coercion**, $0, no keys. Add `"primal"` to the stub keyword inference so the stub picks the register.

**Task 2.6 — Produce the go/no-go recording artifact ($0).** Write `briefs/2026-07-02-grandmaster/go-no-go.md` per §6 — owner, decision rule, pre-agreed Route C fallback, transport escalation ladder, `status: PENDING SPIKE`. This is the artifact the STRESS-TEST verdict requires *recorded before Cy's pass*; the gate (§7) reads it. Optionally also drop Sean's locked Route B Flow frame into `briefs/2026-07-02-grandmaster/style-refs/` as the go/no-go target (Sean's call; not on the critical path).

**Task 2.7 — Verify Checkpoint 2.** Full suite green; neutrality green; completeness green; both md5 held; `go-no-go.md` present; `superpowers:verification-before-completion`. **Pilot DoD met.**

### Checkpoint 3 — the GRANDMASTER go/no-go (COSTED, Sean-gated, NOT in the build session) — see §6.

---

## 6. The GRANDMASTER go/no-go — a hard precondition gate, not a scheduled aspiration (red-team CRITICAL fold)

The STRESS-TEST verdict demands an explicit go/no-go **recorded before Cy's GRANDMASTER Bible pass starts**, with Route C pre-agreed. The red-team's sharpest catch: my first draft only *scheduled* it, and "Deadline: Sean sets" is not a deadline. The fix splits it into a $0 recording (in the build) and the one costed frame (Sean-gated), and makes it a **gate**:

**Produced in Checkpoint 2 ($0, in the build session): the recording artifact `briefs/2026-07-02-grandmaster/go-no-go.md`**, with everything fillable-now filled:
- **Owner:** Sean (eye) + Claude Code (operator).
- **Decision rule:** the `primal-sketch-grit` frame reads as Primal **and** holds the kid's identity **and** matches the §4.4 ART-VIZ target → **GO** (author GRANDMASTER Bibles in `primal-sketch-grit`). Otherwise → **NO-GO**.
- **Pre-agreed fallback (recorded now, not decided mid-pass):** NO-GO → author in Route C (`pencil-test-colored`), which is already buildable.
- **Transport escalation ladder (§3c), pre-agreed:** NB2-from-text misses → spike NB2 + `refs/` style-ref feed (watch the Flo-B identity-morph); that misses → NO-GO→Route C fires rather than chasing a new transport mid-Bible-pass.
- **Status field:** `PENDING SPIKE` — the only thing left is the costed frame + Sean's eye.

**The gate (the enforced part):** the GRANDMASTER Cy Bible pass **does not start** until `go-no-go.md`'s status is `GO` or `NO-GO (Route C)`. No calendar deadline — Sean sets pace — but the recorded decision is a **precondition**, not an aspiration. Everything except the single costed spike frame + Sean's verdict is produced at $0 in the build.

**Checkpoint 3 (COSTED, Sean-gated):** generate one `primal-sketch-grit` hero frame (the kid landing in a ninja crouch) via NB2 from the authored clauses + one Route C frame; compare against the §4.4 target, shown cold; flip `go-no-go.md`'s status. Then the Bible pass is unblocked.

---

## 7. Sequencing + anti-drift

**Order:** `primal-sketch-grit` register pilot (this build, $0; produces `go-no-go.md` at `PENDING SPIKE`) → **[go/no-go spike, Sean-gated → flips `go-no-go.md` to GO or NO-GO (Route C)]** → **the GRANDMASTER Cy Bible pass is gated on that recorded decision (§6) — it does not start until `go-no-go.md` resolves** → then `90s-nicktoon-grossout` (rides the now-cheap pattern — the **2nd instance** that unblocks ai-guru AND tests the fold-vs-skill trigger) → then the powerhouse sidequest (**research-agenda-only**, post-front-door-DoD).

**Anti-drift honesty:** within the active outward-turn workstream; a production unblock, not a new workstream. **Guardrail:** hold to the **two blocking registers + the research agenda.** Building the full roster before GRANDMASTER is unblocked *is* drift — defer the roster to the post-DoD sidequest.

---

## 8. Credential-free verification + the two DoDs

**Every "done" claim runs:** `python -m pytest tests/` green · characterization (6 registers byte-identical) · completeness (incomplete register → red) · neutrality green · both md5 guards verified by hash · stub-green Cy smoke ($0) · `superpowers:verification-before-completion`. No live model/MCP call in tests; subscription billing only; the sole costed thing (the spike) is separate and Sean-gated.

**Two DoDs:**
- **Pilot DoD** (this build): registry byte-identical + `primal-sketch-grit` authored + stub-green Cy smoke + neutrality green + both md5 held + the go/no-go **planned as a task** with owner/deadline/fallback. $0.
- **Powerhouse-pattern DoD** (proven, not just designed): validated as *reusable* only when the **2nd register (90s-nicktoon-grossout) rides it cheaply**. Until then, designed not proven.

**Where cost enters:** the go/no-go spike is the first costed step (Sean-gated); the GRANDMASTER Cy Bible pass follows on a GO.

---

## 9. Risks

- **R1 — The byte-identical refactor breaks a locked Bible.** *Mitigation:* Task 1.0 characterization captured BEFORE the refactor is the oracle; Checkpoint 1 stops for Sean's review before any new-register content. Highest-priority risk.
- **R2 — Fail-loud on unknown register breaks existing tests.** *Confirmed by Codex:* `tests/test_character_designer.py:1175-1182` and `:1275-1276` explicitly assert silent fallback. *Mitigation:* Task 1.2b inverts them deliberately (nonempty-unknown raises; empty still defaults to pencil); grep for any others; stub inference always returns a valid register. Now a planned task, not a lurking risk.
- **R6 — Flo's frame_router is a second register-routing surface, not touched here.** *Codex note:* Flo threads `style_register` but all registers share a route today (`frame_router.py:64`). The registry v1 serves Cy's Bible-plate path; Flo's per-register Phase-5 routing is a **deferred future consumer** of the registry. *Mitigation:* scoped out explicitly; no per-register Flo routing exists to break. Low.
- **R3 — The confirmed art-viz frame is unreproducible by NB2-from-register** (art-viz used a stronger/different engine). *Mitigation:* §4.4 refinement (confirm on NB2); the go/no-go's NO-GO→Route C fallback catches it. Medium.
- **R4 — Scope creep into the full roster.** *Mitigation:* §7 guardrail; the roster is sketch-only, sidequest-deferred.
- **R5 — The completeness test's Cy-block matcher is too strict/loose.** *Mitigation:* Task 1.3 note — pick the matcher that's green for all 6 today, red only for a forgetful new register.

---

## 10. Codex reconciliation notes

Codex ran an independent plan against the same source of truth (session `019f29f8…`). **Strong convergence** on all seven positions: the registry module (its position #7 = canonical registry, not convention), the minimal per-register deliverable, fold-first + ≥2-consumer promotion, the research-brief dimensions, NB2-default + spike transport, primal-then-nicktoon sequencing, and the empty→pencil / nonempty-unknown→fail-loud rule. It independently confirmed the verification finding (criteria.py has criteria/impact-tag/IR vocabularies at `criteria.py:36-67` but **no `style_register` vocabulary**; the doctrine is wrong).

**Divergences and new facts folded in (the valuable part):**

- **[FOLDED — required task] Two existing tests explicitly lock the silent fallback and WILL break under fail-loud.** Codex found `tests/test_character_designer.py:1175-1182` ("unknown register falls back to pencil") and `:1275-1276` (unknown model routing returns NB2). My R2 anticipated this abstractly; Codex named them. **Action:** Checkpoint 1 gains **Task 1.2b — invert these two tests** so a nonempty-unknown register asserts `UnknownRegisterError` / raises, not silent-coerce. This is the behavior change, not a side effect. (Added to the task list + R2.)

- **[FOLDED — new touch-point] `pipeline/frontdoor/validate.py` is a SIXTH surface.** It requires `style_register` present but checks **presence only, not membership** (`validate.py:18-24, 68-72`). Added to the §1.1 table. **The important nuance:** the front door is where you *discover* you need a new register — so it must **NOT hard-fail** on an unregistered register (that would block the very brainstorm that surfaces the gap; the seeds already carry a NEW-flag + doctrine pointer). Position: **soft-flag at the front door** ("this register isn't in the vocabulary yet — author it per the doctrine"), **hard-fail at Cy generation.** Discovery warns; execution blocks. The front-door check reads `ALL_REGISTERS` to decide known-vs-new.

- **[FOLDED — scope note] Flo's `frame_router.py` is a second, deferred model-routing surface.** Codex: Flo threads `style_register` for provenance but "all registers share a route today" (`frame_router.py:64`). The registry v1 serves **Cy's Bible-plate path** (`_REGISTER_MODELS`); Flo's per-register Phase-5 routing is a **deferred future consumer** of the same registry — not built in this pilot (no current per-register routing there). Recorded in §9.

- **[DIVERGENCE — my call kept] Optional `family: tartakovsky` metadata.** Codex #4 suggests keeping flat execution slugs *plus* an optional `family` metadata field for research reuse / UI grouping. I'm **deferring it** to the same trigger as the family/skill question (a 2nd Tartakovsky register greenlighting): a `family` field with **no reader** in v1 is exactly the reader-less speculative field the front-door red-teams catch. We agree on flat slugs now; I decline the metadata field until it has a consumer. (Documented so the red-team can contest it.)

- **[FOLDED — task detail] The Cy context has two closed-vocab prose lines to update, not just the example block.** `cy-character-designer-context.md:13` (top closed-vocab line) and `:111` (the non-negotiables closed-vocab line) both enumerate the six values; registering `primal-sketch-grit` adds the 7th to both, alongside the new `## What good looks like` block. Adding a register to the non-negotiables section is safe against the neutrality test (more registers named = better). Folded into Task 2.3; the completeness test asserts the register name appears in the Cy context.

- **[NOTED] ai-guru material also lives at `tests/fixtures/frontdoor/ai-guru/`** (in addition to `briefs/2026-07-02-ai-guru-pilot/`). For the 2nd register the source of truth is the `briefs/` version; the fixture is the front-door test copy.

Codex's own "does not resolve" list matches ours: it doesn't prove NB2 can render Primal (that's the spike), doesn't pre-decide the `genndy-tartakovsky` skill (research-gated), doesn't resolve Flo routing (deferred), and doesn't touch GRANDMASTER's separate ninja-star readability risk (a different STRESS-TEST Tiger, out of scope here).

---

## 11. Red-team fold

A fresh-context adversarial Codex pass (session `019f29fe…`) attacked the doc and verified every factual claim against main. **All my factual claims held** (criteria.py has no `style_register` vocabulary; unknown nonempty registers coerce to pencil; the two `test_character_designer.py` line refs; **both md5 hashes confirmed correct by `md5`**). Surviving findings and their dispositions:

**FOLDED — behavior/accuracy changes:**

- **[CRITICAL → FOLDED] The plan scheduled the GRANDMASTER go/no-go but didn't *produce* it; "Deadline: Sean sets" is not a deadline.** The STRESS-TEST demands the decision recorded *before* Cy's Bible pass starts. *Fold:* the go/no-go is now a **hard precondition gate** — the GRANDMASTER Cy Bible pass does not start without the recorded decision (§6, §7). Checkpoint 2 (still $0) **produces the recording artifact** `briefs/2026-07-02-grandmaster/go-no-go.md` with the owner, the decision rule, and the **pre-agreed Route C fallback filled in now** — leaving only the single costed spike frame + Sean's eye verdict for Checkpoint 3. The "deadline" is reframed: no calendar date (Sean sets pace), but the recorded decision is a **precondition, not an aspiration**.

- **[HIGH → FOLDED] `style_ref_ids` is passthrough today, not a Cy/register consumer — §4.4 overstated the wire.** `tests/test_frontdoor_emit.py:112` documents "no pipeline code reads style_ref_ids yet"; Slice 3 confirms. *Fold:* §4.4 corrected — **saving frames to the brief folder is real** (files on disk) and they serve as the human-in-the-loop go/no-go target (needs no code); **Cy consuming `style_ref_ids` is a deferred future wire** (the seeds→Cy bridge the scope doc flags as a separate front-door DoD piece), not claimed as current behavior.

- **[HIGH → FOLDED] Task 1.0 characterization missed the prop path and the manifest override path.** The prop plate bypasses register lookup (`character_designer.py:1288`); `_resolve_plate_model` honors a per-character `char_cfg` override (`:1246`). *Fold:* Task 1.0 now snapshots `is_prop=True` **and** a `char_cfg`-override case, **and** asserts the full **cache key** (not just the prompt string) is byte-identical for a representative plate — the cache key (`nb_pro_runner.py:235`) is what actually protects the locked Bibles.

- **[MEDIUM → FOLDED] The Cy-block completeness matcher was too loose** (accepted `style_register: {name}` anywhere in the file). *Fold:* tightened to require the label **inside the `## What good looks like` section** (using the neutrality test's section splitter) — matches the real `### Example X — {char} (style_register: {name})` structure and catches a register with no example block. (A "the block is *substantive*" check stays a human review — prose quality isn't cheaply assertable.)

- **[MEDIUM → FOLDED] Research agenda read as a generic checklist vs the scope's "extensive and first-class" bar.** *Fold:* §2a gains explicit **depth requirements**: frame-by-frame still analysis, composition/staging grammar, the figure/background paint *process* (how the grit is made), **negative controls** (Primal vs Samurai-Jack side-by-side), and a **non-derivative/genericization rule** (applies to Ren & Stimpy too).

- **[MEDIUM → FOLDED] "Five scattered touch-points" was an unstable count** (the table lists 7). *Fold:* the prose no longer claims a fixed number; the table is authoritative.

- **[LOW → FOLDED] Stale line ref** `frame_router.py:64` → `:64`.

**ACCEPTED with rationale (surviving, not folded):**

- **[A-HIGH / A-MEDIUM — the OVER-BUILD attack] "The registry module may be too much mechanism today; a sync test + row additions delivers most of the value with less refactor risk."** *This survives verification and it is real* — the two runtime tables are already co-located, so only the runtime-dispatch refactor carries the cache-key risk. **But Sean made this call with the trade-off explicit** (2026-07-03): the module is built *for the future scale* he intends ("this will expand beyond 7… I don't want to run into the same issue… knock it out today"), it has 2 consumers waiting, and it is consolidation of existing state, not speculative surface. **Disposition: accept, and de-risk maximally** — the byte-identical characterization (Task 1.0, now hardened), the loud fail on unknown, and the Checkpoint-1 stop-for-review make the runtime move as safe as a smaller change. The smaller alternative is recorded here so the decision stays visible. *(This is the one finding worth Sean's eyes before the build — see the session summary.)*

- **[C-HIGH — front-door porousness] The vocabulary stays porous at the front door (warns, doesn't fail).** *Deliberate, not a defect* — the front door is the discovery point for a new register; hard-failing there blocks the brainstorm that surfaces the gap. The hard gate is at Cy generation + the completeness test. Bounded: front-door warns → Cy blocks before any costed pass.

- **[C-MEDIUM — markers can't catch absent taste] The completeness test guarantees markers *exist* (`spec.markers` non-empty); whether they're the *right* load-bearing phrases is a human review + the research's job.** Inherent — taste isn't auto-gradable (the doctrine's own thesis). Accepted bound.

---

## 12. Anti-drift note

This plan builds exactly one register + the mechanism to add more, unblocks one greenlit piece, and writes down the reusable pattern. It does not build the roster, does not touch Em or the front-door DoD pieces, and does not open a new workstream. The registry module earns its place on two grounds the front-door red-teams accept: it is a **consolidation of existing scattered state** (not speculative new surface), and it has **two consumers already waiting** (primal-sketch-grit, 90s-nicktoon-grossout) plus Sean's stated intent to add more. The taste work per style stays deliberate — that is the doctrine, not a limitation to engineer away.
