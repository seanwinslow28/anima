# Flo — Phase 5 Generation Router — Build Plan

*2026-06-10. **Planning artifact — Cowork, no model spend.** Scopes the build of Flo, the Phase 5 generation router: consults `manifest.yaml`'s `generation.routing:` block per shot to pick the right generator (hero/standard/in-between tiers) instead of the current single-model path. Locked decisions from [`docs/2026-05-26-agent-fleet-brainstorm-v2.md`](2026-05-26-agent-fleet-brainstorm-v2.md) §4 and [`docs/Image-Model-DR-2026/SYNTHESIS.md`](Image-Model-DR-2026/SYNTHESIS.md). Reads first: [`PHILOSOPHY.md`](../PHILOSOPHY.md), the SYNTHESIS routing table, [`docs/fleet-ops-protocol.md`](fleet-ops-protocol.md).*

## Why Flo is next
The critic stack is complete; the fleet's last critical-path gap before a real end-to-end run is **how frames get generated**. Today `pipeline/nodes/frame_generate.py` wraps the legacy `generate_frame()` and always uses one model (`generation.model` = NB2) at a fixed cost. Flo makes generation **cost-routed + quality-tiered** — hero keyframes to the best model, in-betweens to the cheapest that holds the pencil aesthetic — and feeds Maya an accurate Phase 0 cost preview. "Validators cannot recover taste absent at generation time" (brainstorm §2.1): the router is where generation quality is decided.

## What already exists — build ON this
| Asset | State | Where |
|---|---|---|
| Hero transport | **Wired** — NB Pro (~$0.15/frame), Cy's painterly generator | `pipeline/agents/nb_pro_runner.py` |
| Standard transport | **Wired** — NB2 (`gemini-3.1-flash-image-preview`, ~$0.07/frame) | `pipeline/agents/gemini_api_runner.py` + the gemini skill |
| Cost-preview integration | **Half-wired** — `cost_estimator._phase_5_cost` already reads `generation.routing.{hero,standard}_keyframe.usd_per_frame` | `pipeline/agents/cost_estimator.py` |
| Current generate node | The contract layer to extend/route — wraps `generate_frame()`, single-model, fixed $0.067 estimate | `pipeline/nodes/frame_generate.py` |
| Draft→pro convention | The `tiering:` manifest block — Flo's escalation ladder reads it | `manifest.yaml` `tiering:` |
| Routing input | Per-character `style_register` ("Flo's Phase 5 routing reads style_register to pick the right generator") | `manifest.yaml` `characters:` |
| fal.ai client | `fal-client` is already a dependency (Seedance uses it) — the cheap-edit transports ride it | `pipeline/seedance_*.py` |

## The model landscape (SYNTHESIS §2) — what's wired vs not
- **Hero keyframe → NB Pro** (~$0.15) — wired. **Standard keyframe → NB2** (~$0.07) — wired.
- **In-between (cheap edit) → Seedream 4.0 / SeedEdit 3.0** (fal.ai, ~$0.007–0.03, the ~80% cost cut) — **not wired**; the SYNTHESIS flags **zero documented pencil/non-photoreal testing** → pilot-gated.
- **In-between (mid) → Qwen-Image-Edit-2511** (fal.ai, ~$0.021) — not wired; the open-source dark horse for sketch input.
- **Mask-precise → GPT-Image-2 edits** (~$0.21) / **self-hosted → FLUX.1 Kontext [dev] + LoRAs** ($0 ongoing, needs a 24GB GPU + ~2hr LoRA train) — deferred.

## Scope — LOCKED (Sean, 2026-06-10)
1. **Build the router skeleton now ($0)** wiring the already-available NB Pro/NB2; declare the in-between/edit tiers as seams.
2. **In-between tier: pilot fal.ai APIs (Seedream/Qwen) next; if they can't hold the pencil grain, pivot to NB2** for in-betweens. (No self-hosted FLUX, no 24GB-rig dependency this round.)

Two sessions, mirroring the T3 rhythm.

---

## Flo-A — the router skeleton ($0, stub-green) — Session A

### A1 — `generation.routing:` manifest block
Add to `manifest.yaml` under `generation:`, mirroring SYNTHESIS §2. Each route = `{transport, model, usd_per_frame, tier, status}`:
```
generation:
  routing:
    hero_keyframe:     { transport: nb_pro, model: <nb-pro-slug>, usd_per_frame: 0.15, tier: pro,   status: wired }
    standard_keyframe: { transport: nb2,    model: gemini-3.1-flash-image-preview, usd_per_frame: 0.07, tier: draft, status: wired }
    in_between_cheap:  { transport: fal_seedream, usd_per_frame: 0.02,  tier: draft, status: declared }   # Flo-B pilot
    in_between_mid:    { transport: fal_qwen,     usd_per_frame: 0.021, tier: draft, status: declared }   # Flo-B pilot
    mask_edit:         { transport: gpt_image_2,  usd_per_frame: 0.21,  status: deferred }
  fallback: nb2   # a declared/failed route falls back to the wired NB2 path
```
Keep cosmetic-honest (the t2/t3 lesson): `status: declared` means the route exists in config but the transport isn't wired — Flo raises a clear "route declared, transport not wired" rather than silently mis-generating.

### A2 — the Flo router (the build)
- New `pipeline/agents/frame_router.py` — a `resolve_route(shot, manifest, character)` that maps `{shot_type, style_register, tier}` → a `Route(transport, model, usd_per_frame, tier)`. `shot_type` is an explicit field on the frame spec (default `standard_keyframe`); hero is opt-in per frame; in-between cleanups route to the in-between tiers.
- A `FloNode` (AgentSpec, `@register_node("flo")`) that dispatches the resolved route to its transport: `nb_pro` → `nb_pro_runner`, `nb2` → the existing `generate_frame()`/gemini path, `fal_*`/`gpt_image_2` → **declared seams** (a transport stub that raises a clear not-wired error until Flo-B). Emits `candidate_path` + the route taken in `notes` (museum credits + cost provenance).
- **Back-compat:** when `generation.routing:` is absent (the pencil-test reference runs), Flo falls through to the legacy single-model `frame_generate` path unchanged. Additive, like the manifest's dual-schema design.
- **Draft→pro escalation:** default-run the route's `draft` tier; escalate to the `pro` route (e.g., standard→hero) on approval or critic-pass, per the `tiering:` block — the brainstorm's pipeline-wide draft→pro convention.

### A3 — Maya cost-preview integration
Extend `cost_estimator._phase_5_cost` to read the full routing table (it already reads hero/standard) — sum per-shot-type counts × `usd_per_frame` so Maya's Phase 0 preview reflects the *routed* budget, not a flat NB2 rate. Declared/deferred routes price at their config estimate with a confidence flag.

### A4 — tests + deliverables (Flo-A)
- `tests/test_frame_router.py`: route resolution by shot_type + style_register; hero→NB Pro, standard→NB2; a `declared` route raises the clear not-wired error; back-compat fall-through when no routing block; draft→pro escalation picks the pro route; the fal/gpt seams are stubbed CI-green.
- Full contract suite + `pipeline/tests/` green; Em verdict baseline md5 byte-identical (Flo is additive, never touches `evals/vision_critic/`).
- CHANGELOG; **no** CLAUDE.md "Flo built" flip until the live keyframe smoke confirms NB Pro/NB2 route live (fold into Flo-B or a short live check).

---

## Flo-B — the in-between pilot (costed) — Session B
The SYNTHESIS's own recommended next step, which doubles as portfolio evidence ("how I evaluated and chose").
- **Build a 20–50-pair pencil-preservation benchmark** from Sean's approved pencil archive (before/after in-between pairs).
- Run **Seedream 4.0** + **Qwen-Image-Edit-2511** (fal.ai) vs **NB2/NB Pro** through identical in-between prompts; score **grain preservation · identity · instruction-follow** (Sean's eye is ground truth, like the Em labels). Qwen sweet-spot denoise 0.78–0.82.
- **Wire the winner** as the `in_between_*` transport (flip its `status: declared → wired`). **If both fal.ai APIs slick the pencil aesthetic → pivot: route in-betweens to NB2** (the locked fallback) and ticket self-hosted FLUX as the $0-ongoing future.
- Deliverables: the benchmark + scored trace under `evals/bakeoffs/`, the wired in-between route, the CLAUDE.md Flo row → built, a CHANGELOG entry. Fleet-ops (bounded `FAL_KEY` + `GEMINI_API_KEY`; §0 before spend).

---

## Fleet-ops + doctrine
- Flo-A is $0 stub-green (isolated worktree, §0 guard, baseline md5 unchanged, squash PR). Flo-B spends a bounded fal.ai + Gemini budget — §0-before-spend, subscription where possible.
- **Verify the transport, not the docstring** (the agy `-m` lesson): confirm the fal.ai Seedream/Qwen call shapes against the real API in Flo-B before the benchmark depends on them.
- **A declared route is an honest not-wired error, never a silent mis-generation.** **Back-compat: the legacy pencil-test path stays intact.** **Additive — never touch Em's baseline.**

## Reserved decisions
1. **Scope — DECIDED:** router skeleton now ($0); pilot fal.ai in-between next, NB2 fallback.
2. **Shot-type taxonomy — default-carried:** `hero_keyframe` / `standard_keyframe` / `in_between_cheap` / `in_between_mid` / `mask_edit`, explicit `shot_type` field on the frame spec (default standard). Refine in Flo-A if the frame specs suggest a cleaner cut.
3. **Self-hosted FLUX — deferred:** ticketed as the $0-ongoing future if the fal.ai pilot fails *and* Sean stands up a 24GB rig.

## Deliverables checklist (Flo-A)
- [ ] `generation.routing:` manifest block (wired hero/standard + declared in-between seams + `fallback: nb2`).
- [ ] `pipeline/agents/frame_router.py` + `FloNode` (`@register_node("flo")`); legacy back-compat preserved.
- [ ] `cost_estimator._phase_5_cost` reads the full routing table.
- [ ] `tests/test_frame_router.py` + suites green; baseline md5 unchanged.
- [ ] CHANGELOG; Flo-B (pilot) teed up as the costed follow-on.

---

*Plan status: DRAFT for Sean's review. No spend, no code changed. Next: confirm, then the Flo-A kickoff converts paste-ready for Claude Code.*
