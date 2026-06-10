# Kickoff — T3 Council, Session A: smoke test + transports + engine (commit 9A)

*Paste-ready brief for a **Claude Code** session. **$0 — no model spend** (a stub-green build plus a subscription-absorbed CLI smoke test; no API-key billing). Builds the first half of anima's last unbuilt critic tier — the T3 multi-CLI variance council. Session A delivers: the Open-Q4 smoke findings, Codie's Codex transport, and the gate-agnostic council engine (Codie + Annie + Sage peers → distinct Opus chairman), all CI-green on stubs. Session B (separate) wires the `pre_museum` gate, runs the live smoke, and does the Sage-tier bake-off. Plan of record: [`docs/2026-06-10-t3-council-build-plan.md`](2026-06-10-t3-council-build-plan.md) (APPROVED — engine + `pre_museum`, defer `post_animatic`; two-session split).*

**Standing doctrine: verify against the tree, never trust a label — including this brief and the docstrings it points at.** This codebase's worst moments came from trusting a label over the tree: a flag silently off measured nothing (2026-06-07); a runbook claimed a loop "self-isolates" and the run crashed on case #0 (Gate-3 v1). **This build has a live example baked in:** `cli_runners.py` *requires* `agy -m <model>` (A2, 2026-06-02), but the Anti-Gravity findings say `-m` **doesn't exist on `agy` v1.0.2**. Do not assume — the Step-0 smoke test exists to resolve exactly that. Read the loop, not the docstring.

## ⚠ FIRST, EVERY SESSION — divergence + tree guard
A Cowork sandbox can't reach GitHub; you (Claude Code) can. Run before anything else:
1. `git fetch origin && git rev-list --left-right --count main...origin/main` → expect `0 0` (last known clean 2026-06-10, HEAD `b2a06f2` / #40).
2. `git log --oneline -4` — confirm `b2a06f2` (#40 Gate-2 calibration) is HEAD.
3. `git status -s` → expect **clean**.
4. **Verdict-baseline guard (additive guarantee):** `md5sum evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` → **`2af75906502f1caf8857e18828ceb2e4`**, byte-identical through ALL of Session A. T3 is purely additive — it must never touch Em's verdict baseline or any `evals/vision_critic/` artifact.
5. Branch off `origin/main` into an isolated worktree (fleet-ops): `feature/t3-council-session-a`.

## Read, in order
1. [`docs/2026-06-10-t3-council-build-plan.md`](2026-06-10-t3-council-build-plan.md) — the approved plan (Steps 0–2 are this session).
2. [`docs/2026-05-26-agent-fleet-brainstorm-v2.md`](2026-05-26-agent-fleet-brainstorm-v2.md) **§2.4, §2.5, §5, §6** — the T3 locks: three heterogeneous peers (production/visual/narrative) from three vendors + a **distinct** Opus chairman (not a promoted peer — Pattern C); all defenses by construction.
3. [`docs/research/2026-05-26-anti-gravity-cli-findings.md`](research/2026-05-26-anti-gravity-cli-findings.md) — the `agy` reality (the 2026-05-27 addendum: working image incantation is `--add-dir` + plain-text paths, **`-m` and `--output-format json` flagged as NOT on v1.0.2**) and the Codex-image Open-Q4 note.
4. **The contracts you build against (read the code, not a summary):** `pipeline/agents/__init__.py` (AgentSpec / AgentResult / **Patch** — note `proposed_by` + `cites_criteria`), `pipeline/agents/cli_runners.py` (the `agy` wrapper + `CLIResponse` already typed for `cli="codex"`), `pipeline/agents/sdk_runners.py` (`invoke_opus_text` / `invoke_opus_vision` — Sage + Chairman transport, proven live), `pipeline/agents/patch_stager.py` (`stage_patches_hook` — reusable, stages any peer's patches), `pipeline/contact_sheet.py` (`build_contact_sheet` — for video/PNG-sequence artifacts later).
5. **The structural reference:** code-brain `agents-sdk/agents/vault_critic.py` — the proven asyncio parallel fan-out of Codex CLI + Anti-Gravity CLI + Claude SDK, per-source status promotion (`ok`/`partial`/`success-empty`/`error`), both-capped→`partial`, separate chairman call. Mirror this shape; do not reinvent it.
6. [`pipeline/agents/prompts/em-vision-critic-context.md`](../pipeline/agents/prompts/em-vision-critic-context.md) — the standing-context preamble template for the four new persona preambles. Honor [`docs/prompt-style-neutrality-doctrine.md`](prompt-style-neutrality-doctrine.md) (style-neutral across the six registers; CI-enforced by `tests/test_prompt_style_neutrality.py`).

## Where we are (verify each)
- T1 ✓, T2/Em ✓ (3 axes measured), **T3 ✗** — greenfield. No `t3_council.py` / `cli_critic` exists.
- Placement is **already declared**: `manifest.yaml` `critics.placement` carries `post_animatic: T3` + `pre_museum_publish: T3`. Only the `critics.t3:` config block + the implementation are missing. (Session B adds the config block; Session A is implementation-only.)
- Transports: **Sage + Chairman** (Opus SDK) exist + proven live. **Annie** (`agy`) exists, image path verified for Em, `-m` unverified. **Codie** (Codex) — `CLIResponse` types `cli="codex"` but there is **no `run_codex_*` function**. Build it.
- The **Animatic phase (Phase 4) is NOT built** — `post_animatic` is deferred this session by design.

---

## STEP 0 — Open-Q4 smoke test ($0, subscription CLIs; do first)
Resolve the transport unknowns *before* writing council code. Each is a single real CLI call (subscription-absorbed — no `ANTHROPIC_API_KEY`, no `GEMINI_API_KEY` billing). If a binary isn't installed, record that and proceed against stubs — but say so plainly.

1. **Annie / `agy -m`:** run `agy -m gemini-3.1-pro -p "Return the JSON {\"hello\":\"world\"}. No other text."` and an image read: `agy --dangerously-skip-permissions --add-dir characters/sean-anchor -p "Describe the image at characters/sean-anchor/anchor.png in one sentence."` Does v1.0.2 accept `-m`? Does it error on an unknown flag? Capture stdout/stderr verbatim.
2. **Codie / `codex`:** verify `codex exec` (per code-brain `vault_critic.py`) accepts a file/image reference at anima resolutions. Capture the working invocation.
3. **Video handling:** confirm the **contact-sheet** approach (`pipeline/contact_sheet.py`) is the path for the (future) animatic — no peer needs native video. Record the **motion-proper blind spot** acceptance (still judges see staging/identity/continuity, not true motion timing).
4. **Output:** `docs/research/2026-06-10-t3-cli-multimodal-smoke.md` — the three resolutions + the verbatim captures. **This note decides Reserved Decision 2** (if `agy` rejects `-m`: default to the Gemini API transport for Annie, consistent with Em — flag it for Sean, don't silently accept the Flash backend-default).

## STEP 1 — Codie's Codex transport + tests ($0, stub-green)
- Add `run_codex_with_image` to `pipeline/agents/cli_runners.py`, mirroring `run_antigravity_with_image`: async subprocess, **deterministic stub fallback** when the binary is absent (CI-green on a fresh machine), `RateCapExhausted` on quota signals, returns `CLIResponse(cli="codex", ...)`. Invocation shape from Step 0 + `vault_critic.py`.
- Extend `tests/test_cli_runners.py`: stub path returns a well-formed envelope; quota → `RateCapExhausted`; `.ok` semantics; timeout path.

## STEP 2 — The council engine ($0, stub-green) — the substantive build
- New `pipeline/agents/t3_council.py` — `T3CouncilNode` satisfying AgentSpec (`@register_node("t3_council")`):
  - **Inputs:** artifact refs (stills/text) + context bundle (storyboard + `acceptance_criteria.json` + brief).
  - **Outputs:** per-peer verdicts, agreement score, chairman adjudication note. Plus `proposed_patches` (staged) + `cites_criteria`.
  - **Parallel fan-out** (`asyncio.gather`) of three peers, each with its own role preamble: **Codie** (production, gpt-5.5/Codex) · **Annie** (visual + identity/continuity, Gemini/`agy`-or-API per Step 0) · **Sage** (narrative/beat, Opus/SDK via `invoke_opus_vision`/`_text`).
  - **Status promotion** per peer (`ok`/`partial`/`success-empty`/`error`); both-CLIs-capped → `partial`. **A peer erroring is an honest errored gap in the result, never a run-abort** (the Gate-3 containment lesson — wrap each peer; surface failures, don't crash the gate).
  - **Chairman:** a **separate** `invoke_opus_text` call that synthesizes the three peer verdicts → consensus + dissent + adjudication note + final `proposed_patches`, citing criteria IDs. **Not** a promoted peer.
  - Each peer + chairman emits `Patch(proposed_by="codie"|"annie"|"sage"|"chairman", cites_criteria=...)`; the existing `stage_patches_hook` stages them — do not write a new stager.
- New preambles `pipeline/agents/prompts/{codie,annie,sage,chairman}-context.md` (mirror `em-vision-critic-context.md`); style-neutral.
- `tests/test_t3_council.py`: fan-out runs all three peers; status promotion; **chairman is a separate call** (assert the call count / that the chairman input includes peer outputs); patches staged carry the right `proposed_by`; an errored peer is contained (no raise); full stub path is CI-green.

## Out of scope for Session A (Session B)
- The `critics.t3:` manifest config block; the `pre_museum` gate wiring + DAG threading.
- The live smoke run on a real artifact; the Sage-tier bake-off (Open Q2).
- Flipping the CLAUDE.md T3 row to "built." (Session A lands a CHANGELOG entry only.)
- Anything touching `post_animatic` (deferred until the Animatic phase exists) or `evals/vision_critic/`.

## Fleet-ops (Session A is $0 but still disciplined)
Isolated worktree off `origin/main` · single owner · `git fetch` + divergence before AND after · **`ANTHROPIC_API_KEY` absent** (Sage/Chairman bill the subscription via the SDK; the Step-0 smoke uses subscription CLIs — Codex Plus + Google personal OAuth — at $0) · no `start_new_session` on the worker · land via squash PR off `origin/main` · clean teardown. Full protocol: [`docs/fleet-ops-protocol.md`](fleet-ops-protocol.md).

## The mistake ledger — do not re-learn
- **A docstring is not a verified code path.** The `agy -m` requirement contradicts the v1.0.2 findings; Step 0 resolves it against the real binary before any council call depends on it.
- **A peer erroring must be contained**, surfaced as an errored gap — never a gate-aborting crash (Gate-3 v1).
- **Stub-green before anything real** — the whole of Session A is CI-green on stubs; no credential is required to pass the suite.
- **Patches stage, never auto-apply.** Peers/chairman emit `proposed_patches`; the hook stages; Sean reviews later (`auto_apply: false`).
- **Don't touch `evals/vision_critic/` or Em's verdict baseline** (md5 above stays byte-identical).

## Deliverables checklist (Session A)
- [ ] §0 tree guard logged (divergence `0 0`, baseline md5 unchanged, clean worktree).
- [ ] `docs/research/2026-06-10-t3-cli-multimodal-smoke.md` — Annie `-m`, Codie image, video-handling resolutions + verbatim captures; Reserved Decision 2 flagged for Sean if `agy` rejects `-m`.
- [ ] `run_codex_with_image` + `tests/test_cli_runners.py` extensions, green.
- [ ] `pipeline/agents/t3_council.py` (`T3CouncilNode`) + 4 standing-context preambles + `tests/test_t3_council.py`, green.
- [ ] Full contract suite (`python -m pytest tests/`) + `python -m pytest pipeline/tests/` still green; prompt-style-neutrality test passes for the 4 new preambles.
- [ ] CHANGELOG entry (Session A: smoke + Codie transport + council engine, stub-green; no gate wiring yet). Verdict baseline md5 unchanged.
- [ ] Land via squash PR off `origin/main`; report the Step-0 findings (esp. the `agy -m` verdict) so Session B's transport choice for Annie is settled before it wires the gate.
