# Kickoff amendments — fold the register-agnostic editing template into Cy

*2026-05-30. A companion to [`2026-05-30-claude-mascot-pencil-register-pivot-kickoff.md`](2026-05-30-claude-mascot-pencil-register-pivot-kickoff.md). That kickoff re-authors the claude-mascot Bible in pencil-test using a multi-view turnaround; it is correct as written and these amendments do not replace it. They generalize its prompting beyond pencil-test by wiring in the register-agnostic NB2 editing template from [`research/2026-05-30-nb2-editing-character-consistency-template.md`](../../research/2026-05-30-nb2-editing-character-consistency-template.md), and they record two decisions Sean made this session about how that template lands. This is a plan — **no code changes this session**; the next Claude Code session implements.*

---

## Why this exists

The mascot kickoff bakes the right prompting discipline (terse intent, strong references, trait-locked tokens) but states it in pencil-test terms and proves it on one character. The research session that produced the editing template asked the harder question — what is the *register-agnostic* version of that discipline, and does it hold across pixel-art, anime, watercolor, and 3D-look as well as pencil? It does, with the structure landed in the template doc. These amendments connect that structure to the code surface it plugs into (`_build_nb_pro_prompt`, the Cy addendum, the manifest) so the mascot pass and every pass after it speak the same template.

Two forks surfaced that were Sean's to decide. He decided both this session:

- **Template wiring → refactor the runner builder.** `_build_nb_pro_prompt` becomes a register-parameterized template emitter that owns the full five-slot structure; Cy keeps authoring only the terse `{variation}` intent. Single source of truth, "runner owns framing" preserved.
- **Model routing → per-register split.** NB2 (`gemini-3.1-flash-image-preview`) is the default for all editing/consistency work and the pixel/flat/line/pencil registers; NB Pro is reserved for painterly/watercolor/3D-look *finals*, wrapped in a verification + regenerate guard.

Both are planned for the implementation session, not done here.

---

## Amendment A — the template wiring (refactor `_build_nb_pro_prompt`)

Today `_build_nb_pro_prompt(plate_intent, *, has_pose_ref)` emits a fixed pencil-leaning framing: "Image 1 is the identity anchor… match the face, hair, color palette, skin tone, and proportions… keep the full color." That is the `pencil-test-colored` instance of the template with the register hard-coded. The refactor generalizes it without losing what works.

**The shape the next session should build.** Turn the builder into a register-parameterized emitter that assembles the five slots from the template doc in their fixed order:

```
_build_plate_prompt(
    plate_intent: str,           # Cy's terse {variation} — unchanged contract
    *,
    style_register: str,         # from character.yaml, drives the register clauses
    has_pose_ref: bool,          # unchanged — gates the Image-2 role line
    is_prop: bool = False,       # unchanged — prop exception still wins
) -> str
```

Internally it reads a **per-register clause table** (the library in the template doc, §"The per-register clause library") keyed on the closed `style_register` vocabulary, and fills `{identity_lock}`, `{preserve_and_negative}`, and `{style_register}` from the matched row. `{variation}` stays Cy's intent wrapped in the `ONLY CHANGE` idiom. `{output_spec}` comes from the plate/manifest. The reference-role preamble and the prop path carry over verbatim — `_build_prop_prompt` is already the `{output_spec}`-isolated-object special case and needs no change beyond living beside the new emitter.

**What must not regress.** The current builder encodes three field-won lessons; the refactor has to keep all three. The terse-intent contract stays (Cy never re-describes the character — the template's whole point). The anti-text clause stays universal (`props/stylus.png` caption failure). And the "keep the full color of Image 1" assertion — the line that recovered `focused` — becomes the `pencil-test-colored` row's preserve clause rather than a hard-coded string, so it survives the generalization instead of being lost in it.

**Why refactor rather than document-only.** Sean's call. Centralizing the template in the runner keeps the single source of truth the field report argued for ("the runner owns identity framing"), and means Phase 3 storyboarding and Phase 5 Flo can later call the same emitter instead of reinventing the structure. The lighter "contract-only" path would have left the structure as prose in the addendum and per-register clauses scattered — more surface for the registers to drift apart. The refactor is the bigger change and the cleaner one.

**The Cy addendum amendment that pairs with it.** [`pipeline/agents/prompts/cy-character-designer-context.md`](../../../pipeline/agents/prompts/cy-character-designer-context.md) already states the prompt contract correctly — short plate intent, no character re-description, runner owns framing. It needs one added paragraph under "The prompt contract": that the runner now wraps Cy's intent in the **full five-slot register-agnostic template** (cite the template doc), that `{variation}` is the only slot Cy authors, and that the register clauses are looked up from `style_register` — so Cy must get `style_register` right in `character.yaml` (it already must, for Flo's routing), because it now also selects the identity-lock enumeration and the style token. No change to what Cy emits; a sharpening of *why* terseness is load-bearing (her intent is one slot of five, not the whole prompt).

---

## Amendment B — the model routing (per-register split)

This is the correction with the most leverage and the one that contradicts current behavior. `invoke_nb_pro` in [`pipeline/agents/nb_pro_runner.py`](../../../pipeline/agents/nb_pro_runner.py) defaults `model="gemini-3-pro-image-preview"` — NB Pro — for every plate. The research is unambiguous that this is backwards for editing: NB2 holds identity better across edits, costs half, runs 4× faster, and avoids NB Pro's confirmed multi-reference downsampling regression (Google AI dev forum, 4 Mar 2026). Cy's entire job is identity-preserving editing. She is routed to the wrong model.

**The routing the next session should wire**, per register, into the manifest's `characters.{id}` block and read by the runner at plate time:

| `style_register` | Plate / editing model | Final-render model | Notes |
|---|---|---|---|
| `pencil-test-colored` | NB2 | NB2 (no painterly final needed) | sean-anchor + the new mascot both land here |
| `pixel-art-8bit` | NB2 | NB2 + post-process | grid-snap/quantize + chroma-key downstream |
| `line-art-only` | NB2 | NB2 | flat register, NB2 throughout |
| `watercolor` | NB2 (drafts) | **NB Pro**, guarded | Pro's painterly edge earns it; guard required |
| `photoreal` | NB2 (drafts) | **NB Pro**, guarded | as above |
| `3d-rendered` | NB2 (drafts) | **NB Pro**, guarded | as above |

**The manifest surface.** The v2 schema already supports per-register model assignment. The clean shape is a per-character (or per-register) `generation_model` / `final_model` pair under `characters.{id}` — e.g. `claude-mascot.generation_model: gemini-3.1-flash-image-preview`. The runner's `invoke_nb_pro` default flips to NB2, and any NB-Pro final render is an explicit opt-in from the manifest, never the default. Rename or alias `invoke_nb_pro` → `invoke_image_edit` (model is a parameter, the function name shouldn't assert Pro) when the refactor lands; not load-bearing, but the current name will mislead the next reader.

**The guard for the NB-Pro finals.** Where a register does route to NB Pro (the painterly finals), wrap the call in what the forum's production teams built: a cheap "were the references actually used?" check (an NB2 or similarity-gate pass on the output vs the anchor) plus an auto-regenerate on failure. This is the documented mitigation for Pro ignoring references 10–20% of the time. It maps onto anima's existing draft→pro escalation and the Pass-2.5 similarity gate — the gate already computes the anchor comparison; here it gates the *Pro* call's reference-fidelity rather than just recording it.

**What this means for the mascot pass specifically.** The mascot kickoff's Phase 4 bake should run on **NB2**, not NB Pro. The pencil-test mascot is `pencil-test-colored` → NB2 per the table, and NB2 is the better identity-holder for the across-angle editing the turnaround sheet enables. This is a one-line addition to the kickoff's Phase 4 (the bake command passes the NB2 slug, or the manifest sets it) and it strengthens the kickoff's own expectation that "the new-angle plates should hold the box-creature form." Route the bake to the model that holds form best.

**Freshness caveat to carry into the session.** The NB Pro regression is operational, reported late-Feb to early-Mar 2026, and may be patched. The decision treats "Pro reference handling is currently unreliable" as a condition to re-verify at implementation time, not a permanent law. If a quick NB2-vs-Pro bake on a mascot plate shows Pro has recovered, the per-register table still stands (NB2 is cheaper and faster regardless) but the guard can relax. Re-verify; don't assume.

---

## Amendment C — how this generalizes to storyboarding (Phase 3)

The mascot kickoff's Phase 5 ("first two-character continuity check") is, quietly, the first storyboard frame anima will generate — Sean and the mascot in one scene, referenced against the A-7 pairing. The template doc's **storyboard variant** is exactly the prompt shape that frame should use, and naming it here makes the connection explicit rather than incidental.

The storyboard variant is the base template plus a `{shot}` block (shot size · camera height · lens · staging) and an action in `{variation}` instead of a static pose, with the same iron rule Cy already follows — re-reference the same anchors every frame, never chain. The two-character first-light frame in the kickoff's Phase 5 should be built through it: Image 1 = Sean's anchor, Image 2 = the mascot's anchor, Image 3 = A-7 for scale, `{identity_lock}` enumerating both characters, `{variation}` = the single action, `{shot}` = the framing, style-register held constant. The worked example is in the template doc (§"The storyboard variant").

The larger point for the implementation session: **the template is a Phase-wide primitive, not a Cy-only helper.** Phase 2 (Cy's Bible plates), Phase 3 (the storyboard shot list's per-shot prompts), and Phase 5 (Flo's runtime keyframes) are all the same editing operation — anchor plus one constrained delta — and all three should draw from the one register-parameterized emitter the refactor builds. When Phase 3's prompt-drafting assist lands, it emits the storyboard variant; it does not invent a parallel prompt shape. The continuity audit Phase 3 needs becomes, in part, a check that the identity-lock and style-register slots stayed verbatim across the beat sequence (trait-lock). Building the emitter in Amendment A with this in view — register as a parameter, slots as a stable contract — is what lets Phase 3 reuse it for free instead of forking it.

---

## What lands where (summary for the implementation session)

This session produced two docs and no code. The next session, in rough order:

1. **Refactor `_build_nb_pro_prompt` → a register-parameterized template emitter** (Amendment A), reading the per-register clause library, preserving the terse-intent contract + anti-text clause + the full-color preserve line. Add the paired paragraph to `cy-character-designer-context.md`.
2. **Flip the editing model default to NB2 and wire per-register routing** through the manifest (Amendment B); add the verification+regenerate guard on any NB-Pro final path; consider the `invoke_nb_pro` → `invoke_image_edit` rename.
3. **Run the mascot pass on NB2** (the existing kickoff, with Phase 4 routed to NB2) and build its Phase 5 two-character frame through the **storyboard variant** (Amendment C).
4. **Carry the freshness caveat** — re-verify the NB Pro regression before relying on the guard's necessity.

Out of scope, unchanged from the mascot kickoff: the 16BitFit-humanoid pixel-register pass, the per-view-reference hard gate, Em's closing-the-loop case 7, sean-anchor identity tuning, the rename. Don't touch the sean-anchor Bible.
