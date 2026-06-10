# Kickoff — Flo Router, Session A: the $0 router skeleton

*Paste-ready brief for a **Claude Code** session. **$0 — no model spend** (a stub-green build). Builds Flo, the Phase 5 generation router, as a skeleton: the `generation.routing:` manifest block, route resolution (hero→NB Pro / standard→NB2, both already wired), draft→pro escalation, Maya cost-preview integration, and declared seams for the in-between/edit tiers. Flo-B (the costed fal.ai pencil-preservation pilot) is separate. Plan of record: [`docs/2026-06-10-flo-router-build-plan.md`](2026-06-10-flo-router-build-plan.md) (scope LOCKED: skeleton now, fal.ai pilot next with an NB2 fallback).*

**Standing doctrine: verify against the tree and the real transports — never the label.** The recent wins came from this: the T3 smoke caught the `agy -m` docstring lying, and Codie's live check caught the variadic `-i/--image` ordering bug. Flo's version: confirm the NB Pro / NB2 runner call shapes against the actual functions before the router dispatches to them.

## ⚠ FIRST — divergence + tree guard
1. `git fetch origin && git rev-list --left-right --count main...origin/main` → expect `0 0` (HEAD `ac95869` / #42, T3 council Session B).
2. `git log --oneline -3` — confirm `ac95869` at HEAD; `git status -s` → clean.
3. **Verdict-baseline guard:** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` → **`2af75906502f1caf8857e18828ceb2e4`**, byte-identical through ALL of Session A. Flo is additive — never touch `evals/vision_critic/`.
4. Branch an isolated worktree `feature/flo-router-a` off `origin/main`.

## Read, in order
1. [`docs/2026-06-10-flo-router-build-plan.md`](2026-06-10-flo-router-build-plan.md) — the approved plan (Flo-A steps A1–A4 are this session).
2. [`docs/2026-05-26-agent-fleet-brainstorm-v2.md`](2026-05-26-agent-fleet-brainstorm-v2.md) **§4** (Flo routing) + [`docs/Image-Model-DR-2026/SYNTHESIS.md`](Image-Model-DR-2026/SYNTHESIS.md) **§2** (the consensus routing table).
3. **The integration point (read the code):** [`pipeline/nodes/frame_generate.py`](../pipeline/nodes/frame_generate.py) (the current single-model node that wraps `generate_frame()`), [`pipeline/generate.py`](../pipeline/generate.py) (`generate_frame` — the legacy NB2 path Flo's `nb2` route reuses).
4. **The wired transports:** [`pipeline/agents/nb_pro_runner.py`](../pipeline/agents/nb_pro_runner.py) (`invoke_nb_pro`/`invoke_image_edit` — the `nb_pro` hero route) and [`pipeline/agents/gemini_api_runner.py`](../pipeline/agents/gemini_api_runner.py) (NB2/standard). Confirm the exact call signatures before routing to them.
5. **The Maya seam:** [`pipeline/agents/cost_estimator.py`](../pipeline/agents/cost_estimator.py) `_phase_5_cost` — already reads `generation.routing.{hero,standard}_keyframe.usd_per_frame`; extend it to the full table.
6. [`manifest.yaml`](../manifest.yaml) — the current single-model `generation:` block, the `tiering:` block (draft→pro), the `characters:` `style_register`. [`pipeline/agents/__init__.py`](../pipeline/agents/__init__.py) — the AgentSpec contract for `FloNode`.

## STEP A1 — `generation.routing:` manifest block ($0)
Add under `generation:` (keep the existing single-model fields for back-compat), mirroring SYNTHESIS §2:
- `hero_keyframe` → `{transport: nb_pro, usd_per_frame: 0.15, tier: pro, status: wired}`
- `standard_keyframe` → `{transport: nb2, model: gemini-3.1-flash-image-preview, usd_per_frame: 0.07, tier: draft, status: wired}`
- `in_between_cheap` → `{transport: fal_seedream, usd_per_frame: 0.02, tier: draft, status: declared}` (Flo-B)
- `in_between_mid` → `{transport: fal_qwen, usd_per_frame: 0.021, tier: draft, status: declared}` (Flo-B)
- `mask_edit` → `{transport: gpt_image_2, usd_per_frame: 0.21, status: deferred}`
- `fallback: nb2`
Cosmetic-honest: `status: declared/deferred` = config exists, transport not wired → Flo raises a clear not-wired error, never a silent mis-generation.

## STEP A2 — the Flo router ($0, the build)
- `pipeline/agents/frame_router.py`: `resolve_route(shot, manifest, character) -> Route` mapping `{shot_type (explicit on the frame spec, default standard_keyframe), style_register, tier}` → `Route(transport, model, usd_per_frame, tier)`.
- `FloNode` (`@register_node("flo")`, AgentSpec): dispatches the resolved route — `nb_pro` → `nb_pro_runner`, `nb2` → the legacy `generate_frame()` path, `fal_*`/`gpt_image_2` → a **declared seam** (transport stub that raises a clear not-wired error). Output `candidate_path`; record the route taken in `notes` (cost + museum-credit provenance).
- **Back-compat:** no `generation.routing:` block → fall through to the legacy single-model `frame_generate` path unchanged (the pencil-test runs must not break).
- **Draft→pro:** default-run the route's `draft` tier; escalate to the `pro` route on approval / critic-pass per the `tiering:` block.

## STEP A3 — Maya cost-preview ($0)
Extend `cost_estimator._phase_5_cost` to sum the full routing table (per-shot-type counts × `usd_per_frame`), so Maya's Phase 0 preview reflects the routed budget. Declared/deferred routes price at config estimate with a lowered confidence.

## STEP A4 — tests + green
- `tests/test_frame_router.py`: resolution by shot_type + style_register; hero→NB Pro / standard→NB2; a `declared` route raises the not-wired error; back-compat fall-through with no routing block; draft→pro picks the pro route; fal/gpt seams stubbed CI-green.
- Full `tests/` + `pipeline/tests/` green; verdict baseline md5 unchanged; CHANGELOG entry.

## Out of scope (Flo-B)
The fal.ai Seedream/Qwen transports, the pencil-preservation benchmark, wiring the in-between route, the CLAUDE.md "Flo built" flip, and any self-hosted FLUX work. Don't wire a `declared` transport this session.

## Fleet-ops + mistake ledger
Isolated worktree off `origin/main` · single owner · §0 guard before AND after · `ANTHROPIC_API_KEY` absent (no spend anyway) · squash PR · clean teardown. **Verify the runner signatures before dispatch; a declared route errors honestly; keep the legacy path intact; never touch `evals/vision_critic/`.**

## Deliverables checklist (Flo-A)
- [ ] §0 guard logged (divergence `0 0`, baseline md5 unchanged, clean worktree).
- [ ] `generation.routing:` block (wired hero/standard + declared seams + `fallback: nb2`).
- [ ] `pipeline/agents/frame_router.py` + `FloNode`; legacy back-compat preserved.
- [ ] `cost_estimator._phase_5_cost` reads the full routing table.
- [ ] `tests/test_frame_router.py` + suites green; baseline md5 unchanged; CHANGELOG.
- [ ] Land via squash PR off `origin/main`.
