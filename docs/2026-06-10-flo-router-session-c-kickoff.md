# Kickoff — Flo Router, Session C: make Flo LIVE in the run path + the HF01 fix

*Paste-ready brief for a **Claude Code** session. **$0 — no model spend** (a stub-green wiring build). Flo-A built the router + `FloNode`; Flo-B chose the in-between routes. But **Flo is registered, not dispatched** — the generation path a run actually executes is still the single-model `frame_generate` (NB2 only), and the manifest `phases:` block is empty (`enabled` only), so no run chains through Flo. This session makes Flo the **dispatched** Phase-5 generation node, threads the routing signals onto frame specs, and fixes the HF01 square-frame bug on the NB Pro path — the two prerequisites for the first integrated end-to-end run. Plan of record: [`docs/2026-06-10-flo-router-build-plan.md`](2026-06-10-flo-router-build-plan.md). Builds on Flo-A (#43) + Flo-B (#44).*

**Standing doctrine: verify against the tree — never the label, including this doc.** Flo-A's CHANGELOG reads "built"; the tree shows it is **built but not wired into any run**. Confirm that yourself before you start (STEP C0), and confirm the seam shapes (the DAG runner is declarative; `invoke_image_edit` omits `--aspect-ratio`) before you change them.

## ⚠ FIRST — divergence + tree guard
1. `git fetch origin && git rev-list --left-right --count main...origin/main` → expect `0 0`. `git log --oneline -3` should show `46a4995` (Flo-B, #44) in history; `git status -s` → clean.
2. **Verdict-baseline guard:** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` → **`2af75906502f1caf8857e18828ceb2e4`**, byte-identical through ALL of Session C. Additive only — **never touch `evals/vision_critic/`**.
3. Branch an isolated worktree `feature/flo-router-c` off `origin/main`.

## STEP C0 — confirm the gap (don't trust this doc)
Verify before building, so the fix targets the real state:
- `grep -rn '"flo"\|FloNode\|resolve_route' pipeline/ --include='*.py' | grep -v agents/frame_router.py | grep -v test` → today the only hit is the registration import in `pipeline/nodes/__init__.py`. **Nothing dispatches `flo`.**
- `pipeline/nodes/frame_generate.py` still calls `generate_frame()` single-model; `pipeline/generate.py main()` hardcodes `node_id="frame_generate"`; `manifest.yaml` `phases:` has only `enabled` (no node graph). The DAG runner (`dag.py load_graph_from_manifest`) is **declarative** — it dispatches whatever `phases.*.nodes[*].node` names.
- `pipeline/agents/nb_pro_runner.py` `_build_skill_cmd` builds the skill argv with **no `--aspect-ratio`** → the skill defaults to a square render → fails HF01 (`pipeline/audit.py check_aspect_ratio`, 16:9 ±2%). The `nb2`/standard path (`pipeline/generate.py generate_frame`) **does** pass `--aspect-ratio 16:9`, so only the `nb_pro` routes (hero_keyframe + in_between_mid) are affected.

## Read, in order
1. [`docs/2026-06-10-flo-router-build-plan.md`](2026-06-10-flo-router-build-plan.md) + the Flo row in [`CLAUDE.md`](../CLAUDE.md) Skills Map (state-of-record).
2. **The router (already built):** [`pipeline/agents/frame_router.py`](../pipeline/agents/frame_router.py) — `resolve_route` + `FloNode`. `FloNode` already reads `ctx.inputs.get("shot_type")` + `ctx.inputs.get("character_id")` and dispatches `nb_pro`/`nb2`; this session **feeds** it from a real run.
3. **The dispatch seam:** [`pipeline/dag.py`](../pipeline/dag.py) `load_graph_from_manifest` (reads `phases.*.nodes`) + `run_from_legacy_cli`; [`pipeline/generate.py`](../pipeline/generate.py) `main()` (the `frame_generate` hardcode) + `generate_frame` (the legacy NB2 path Flo's `nb2` route reuses); [`pipeline/nodes/frame_generate.py`](../pipeline/nodes/frame_generate.py) (the current node).
4. **The HF01 seam:** [`pipeline/agents/nb_pro_runner.py`](../pipeline/agents/nb_pro_runner.py) `invoke_image_edit` + `_build_skill_cmd`; the skill at `.claude/skills/gemini-pencil-animation-image-gen/scripts/generate_image.py` already accepts `--aspect-ratio`.
5. [`manifest.yaml`](../manifest.yaml) — the `phases:` block (to extend), the `generation.routing:` block (the route table), `characters:` (`style_register`), `act1.keyframes` (the frame-spec shape).

## STEP C1 — make `flo` the dispatched Phase-5 generation node ($0)
**Goal:** a run dispatches `flo` (routing live) instead of single-model `frame_generate`, with the legacy path preserved as back-compat.
- **Preferred (declarative, the v2 path the integrated run will use):** support a `phases.phase_5.nodes` graph whose entries carry `node: flo`, dispatched by the DAG runner. Wire FloNode's input bindings so a node entry supplies `frame_num` / `prompt` / `references` / `shot_type` / `character_id` from the frame spec. Resolve the keyframe-spec ↔ DAG-node-input impedance cleanly (the actual *scene* graph is authored by Maya in the run session — this session establishes the mechanism + a worked example).
- **Acceptable fallback if direct dispatch needs more plumbing than fits a $0 session:** have `FrameGenerateNode` delegate to `resolve_route` + Flo's dispatch (so everything that dispatches `frame_generate` now routes through Flo). Note the tradeoff (conflates the two nodes) in the PR.
- **Back-compat is mandatory:** no `generation.routing:` block → Flo's `resolve_route` returns `None` → legacy single-model fall-through (pencil-test reference runs must produce byte-identical behavior). The `nb2` route already reuses `generate_frame`, so standard-tier output is unchanged.

## STEP C2 — thread `shot_type` + `character_id` onto frame specs ($0)
- Frame specs (keyframes) may carry an optional `shot_type` (default `standard_keyframe`; `hero_keyframe` opt-in) and `character_id`. FloNode already reads both; this step makes the loader/bindings **supply** them so routing is real (hero→NB Pro, standard→NB2) and `style_register` resolves from the named character.
- **Two-character note:** a frame depicting both Sean + the mascot uses one `character_id` only to look up `style_register`; both Bibles share `pencil-test-colored`, so either id resolves the same register — pick the primary subject. (Per-character routing is future work; today all registers share a route.)
- Default/unset `shot_type` must keep the pencil-test runs on `standard_keyframe` → NB2, unchanged.

## STEP C3 — HF01 fix: 16:9 on the NB Pro path ($0)
- Add an `aspect_ratio: str | None = None` parameter to `invoke_image_edit`, threaded into `_build_skill_cmd` (append `--aspect-ratio <ratio>` only when set). **Regression-safety:** `None` must preserve the *exact* current argv + cache key, so Cy's locked-Bible plate generation is byte-identical (don't fold `aspect_ratio` into the cache key when it's `None`).
- Flo's `nb_pro` dispatch branch (`frame_router.py`) passes `aspect_ratio="16:9"` so hero_keyframe + in_between_mid render 16:9 and clear HF01. Verify against `audit.py check_aspect_ratio` (16:9 ±2%).

## STEP C4 — tests + stub-green smoke ($0)
- Unit: `frame_generate`/`flo` dispatch routing (hero→nb_pro, standard→nb2, draft→pro escalation) through the chosen wiring; `shot_type`/`character_id` threading; HF01 — `invoke_image_edit(aspect_ratio="16:9")` emits `--aspect-ratio 16:9` and `aspect_ratio=None` emits the unchanged argv (regression-lock Cy's path).
- **Integration smoke (stub-green, no key):** `USE_DAG_RUNNER=1` runs a tiny declared `flo` graph (one hero + one standard frame) → stub placeholder outputs land, the route taken is in `notes`, no real call fires. Prove `flo` dispatches and routes; this is the seam the run session builds on.
- Full `tests/` + `pipeline/tests/` green; verdict baseline md5 unchanged; CHANGELOG entry; **flip nothing about Flo-B's decision** (in-betweens stay nb2/nb_pro).

## Out of scope (the run session)
Authoring the actual Sean-+-mascot scene graph, the Maya brief/plan, the costed generation, the Em/T3 critique pass, assembly, and museum capture. This session is the **$0 wiring** that makes those possible — it spends nothing and generates no real frames.

## Deliverables checklist (Flo-C)
- [ ] §0 + tree guard logged (divergence `0 0`, baseline md5 unchanged, clean worktree).
- [ ] C0 gap confirmed in the PR description (Flo was registered-not-dispatched; nb_pro omitted aspect ratio).
- [ ] `flo` is the dispatched Phase-5 generation node (preferred declarative graph, or documented delegation fallback); legacy single-model fall-through byte-identical.
- [ ] `shot_type` + `character_id` threaded onto frame specs → real hero/standard routing.
- [ ] HF01 fixed on the NB Pro path (`aspect_ratio` param; Cy's plate path regression-locked).
- [ ] Unit + stub-green `USE_DAG_RUNNER=1` flo-dispatch smoke green; full suites green; baseline md5 unchanged; CHANGELOG.
- [ ] Land via squash PR off `origin/main`; clean teardown.

## Fleet-ops + mistake ledger
Isolated worktree off `origin/main` · single owner · §0 guard before AND after · `ANTHROPIC_API_KEY` absent (no spend) · squash PR · clean teardown. **Confirm the gap before fixing it (C0); keep the legacy pencil-test path byte-identical; regression-lock Cy's `invoke_image_edit` calls; a declared route still errors honestly; never touch `evals/vision_critic/`.**
