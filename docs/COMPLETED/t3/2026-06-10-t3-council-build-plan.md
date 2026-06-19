# T3 Council — Build Plan (commit 9)

*2026-06-10. **Planning artifact — Cowork, no model spend.** Scopes the build of anima's last unbuilt critic tier: the T3 multi-CLI variance council (Codie + Annie + Sage + a distinct Opus chairman). Grounded against the tree, not the labels. Locked decisions from [`docs/2026-05-26-agent-fleet-brainstorm-v2.md`](../agent-fleet/2026-05-26-agent-fleet-brainstorm-v2.md) §2.4 / §2.5 / §5 / §6 and the placement in [`manifest.yaml`](../../../manifest.yaml) `critics.placement`. Reads first: [`PHILOSOPHY.md`](../../../PHILOSOPHY.md), [`docs/pipeline-architecture-v1.md`](../../architecture/pipeline-architecture-v1.md) §Critic Stack, [`docs/research/2026-05-26-anti-gravity-cli-findings.md`](../../research/2026-05-26-anti-gravity-cli-findings.md), [`docs/fleet-ops-protocol.md`](../../architecture/fleet-ops-protocol.md).*

## Why T3 is the next chunk

The critic stack is the brainstorm's central thesis. **T1 ✓** (rule gates) · **T2 ✓** (Em — now rigorously evaluated across all three axes) · **T3 ✗** — the only tier with *zero* implementation. It is locked at 90–95% confidence, **$0 incremental** (subscription-absorbed), retires the human stand-in at two gates, and compounds directly on the Em work (Em is now the proven template for building + evaluating a critic). A human is currently the only thing standing at both T3 checkpoints.

## What already exists — build ON this, not from scratch

| Asset | State | Where |
|---|---|---|
| AgentSpec contract | Names the T3 stack by persona ("Codie/Annie/Sage/Chairman satisfies AgentSpec") | `pipeline/agents/__init__.py` |
| Patch staging | Reusable for any critic — `Patch.proposed_by` carries the persona for museum credits; `stage_patches_hook` auto-stages | `pipeline/agents/patch_stager.py` |
| T3 **placement** | **Already declared** (commit 1): `post_animatic: T3`, `pre_museum_publish: T3` | `manifest.yaml` `critics.placement` |
| Sage + Chairman transport | **Exists + proven live** (Em escalates to Opus vision in production) — `invoke_opus_vision` / `invoke_opus_text`, subscription-absorbed | `pipeline/agents/sdk_runners.py` |
| Annie transport (Gemini/`agy`) | **Exists** — `run_antigravity_with_image`, image incantation verified for Em (`--add-dir` + plain-text paths). One open risk (below) | `pipeline/agents/cli_runners.py` |
| Contact-sheet helper | Reusable to turn a video/PNG-sequence animatic into stills the still-image peers can read (the tool Em uses for motion-sight) | `pipeline/contact_sheet.py` |
| Structural reference | The proven parallel-CLI-fan-out + chairman pattern: asyncio fan-out, status promotion (`ok`/`partial`/`success-empty`/`error`), both-capped→partial, separate chairman, 600s wall / 120s per-CLI | code-brain `agents-sdk/agents/vault_critic.py` (800 lines) |

## The two real gaps (and one contradiction to resolve)

1. **Codie's Codex transport is greenfield.** `CLIResponse` anticipates `cli="codex"`, but there is **no `run_codex_*` function**. Build it (mirror `run_antigravity_with_image`). Multimodal (image) input is unverified — lift the `codex exec` invocation from code-brain's `vault_critic.py`.
2. **Annie's `agy -m` flag is an unverified contradiction.** `cli_runners.py` (A2, 2026-06-02) now *requires* `-m <model>` and raises without it — but the migration findings (2026-05-27 addendum) say **`-m`/`--model` does not exist on `agy` v1.0.2**. A real Annie call could fail today. The smoke test resolves it.
3. **Sage/Chairman are de-risked** — Opus SDK runs live in Em's escalation path already.

## The dependency reality that shapes sequencing

- **The Animatic phase (Phase 4) is NOT built** — no animatic node in `pipeline/`. So the `post_animatic` T3 gate would be building *ahead of its phase*.
- The `pre_museum` gate gates Mo's museum draft (which **does** exist) — but the museum is on hold per Sean until the pipeline produces more content.
- **Conclusion:** build the council **engine gate-agnostic** (a reusable AgentSpec node taking `{artifact stills/text + storyboard/criteria/brief context + per-peer role framing}`), validate it on an **available** artifact, and **defer the specific gate wiring** until each phase is ready. Don't build a gate for a phase that doesn't exist.

---

## The build — staged, each chunk stub-green and shippable

### Step 0 — Open Q4 smoke test ($0, do first, ~30 min)
The cheapest, highest-information move. Resolves the transport unknowns *before* any council code (the SF03/Gate-3 "assert before you build" discipline).
- **Annie/`agy`:** run `agy -m gemini-3.1-pro -p "..."`. Does v1.0.2 accept `-m`? If it errors on an unknown flag, decide (Reserved Decision 2): drop `-m` and accept the backend default (Flash — a downgrade, but T3 is *variance*, not identity-critical), **or** route Annie through the Gemini API transport (`gemini_api_runner`) like Em (bounded API $, confirms the served model). Capture stdout/stderr.
- **Codie/`codex`:** `codex exec` with a file/image reference — does it accept image input at anima's resolutions? Capture.
- **Sage/Opus:** already proven — no test.
- **Video handling:** do any peer accept video natively, or do we contact-sheet the animatic? **Default: contact-sheet** (`pipeline/contact_sheet.py`), accepting the *motion-proper blind spot* — the same honest limitation the Em eval established: still judges see staging / identity / continuity across keys, **not** true motion timing; the human keeps motion timing.
- **Output:** a dated research note under `docs/research/` resolving the three unknowns. Gates the rest.

### Step 1 — Codie's Codex transport + tests ($0, stub-green)
- Add `run_codex_with_image` to `cli_runners.py` (mirror `run_antigravity_with_image`: async subprocess, **stub fallback** when the binary is absent, `RateCapExhausted` on quota, `CLIResponse(cli="codex")`). Invocation shape from Step 0 + code-brain's `vault_critic.py`.
- Extend `tests/test_cli_runners.py` with the codex stub-path tests.
- This is the only missing transport.

### Step 2 — The council engine ($0, stub-green) — the substantive build
- New module `pipeline/agents/t3_council.py`: a `T3CouncilNode` satisfying AgentSpec.
  - **Inputs:** artifact refs (stills/text), context bundle (storyboard + `acceptance_criteria.json` + brief).
  - **Outputs:** per-peer verdicts, agreement score, chairman adjudication note.
  - **`proposed_patches`** (staged, never applied) + **`cites_criteria`**.
- **Parallel fan-out** (`asyncio.gather`) of three peers, each with a role-specific standing-context preamble:
  - **Codie** — production peer (gpt-5.5 / Codex): production/structural correctness.
  - **Annie** — visual peer (Gemini / `agy` or API): visual + identity/continuity.
  - **Sage** — narrative peer (Opus / SDK): narrative / beat / story coherence.
- **Status promotion** per peer (`ok`/`partial`/`success-empty`/`error`); both-CLIs-capped → `partial` (the vault-critic pattern). **A peer erroring is an honest errored gap, never a run-abort** (the Gate-3 v1-crash lesson).
- **Chairman** — a **separate** Opus call (`invoke_opus_text`) that synthesizes the three peer verdicts into consensus + dissent + an adjudication note + final `proposed_patches`, citing criteria IDs. **Not a promoted peer** (Pattern C — avoids self-favoring bias).
- Each peer + chairman emits `Patch(proposed_by="codie"|"annie"|"sage"|"chairman", cites_criteria=...)` → `stage_patches_hook` stages them automatically.
- New preambles `pipeline/agents/prompts/{codie,annie,sage,chairman}-context.md` (mirror `em-vision-critic-context.md`), **style-neutral** per the prompt-style-neutrality doctrine.
- **Stub-green:** all four transports already fall back to deterministic stubs when binaries/SDK are absent → CI-green without credentials (the Em/Cy discipline).
- `tests/test_t3_council.py`: fan-out, status promotion, chairman-is-a-separate-call, patches-staged-with-`proposed_by`, errored-peer containment, stub path.

### Step 3 — Config + gate wiring (defer-aware)
- **Manifest:** add the `critics.t3:` config block (mirror `critics.t2:` shape): peers list, per-peer model/transport, chairman model, `auto_apply: false` (v2 lock), `per_call_timeout_s: 120`, `wall_budget_s: 600`, `default_context_files`. (Placement is already declared.)
- **Wire the gate that's ready — `pre_museum`:** Mo's museum draft exists, so this is the buildable + testable gate (the validation vehicle), even with the museum on hold. Council reads the draft (text + thumbnails) before publish.
- **Defer `post_animatic`:** leave a declared seam + a ticket; the engine's contact-sheet input path (Step 0/2) is ready to plug in the moment the Animatic phase lands.
- DAG integration: register the node; thread it at the declared placement.

### Step 4 — Validation + the eval ($0 mostly; one small subscription-absorbed live smoke)
- Structural tests green (Steps 1–3) + full contract suite still green.
- **One LIVE smoke run** on a real available artifact (the existing museum draft, or an Act 1 frame set): proves the three real transports fan out, the chairman synthesizes, patches stage. Capture a dated trace under `evals/` (portfolio-grade evidence, like the Em traces). Subscription-absorbed (+ bounded Gemini API only if Annie routes via API per Step 0).
- **The T3 eval = Bake-off 2 (Sage tier ablation, brainstorm §8):** Opus-Sage vs Sonnet-Sage with the chairman held constant — measure dissent-map richness + chairman synthesis quality + adjudication usefulness. Resolves **Open Q2**. T3 is **not** scored with an Em-style confusion matrix — a synthesis critic's quality is dissent richness + adjudication usefulness, per the eval handbook's per-agent matrix.
- **A small Sean-rated adjudication-quality check:** on a handful of artifacts, does the chairman's adjudication + staged patches read as useful art direction? Sean's taste is ground truth (same as the Em labels).

---

## Fleet-ops framing (Step 4 live smoke + any costed bake-off)
Isolated worktree off `origin/main` · single owner · §0 gates before spend · **subscription billing** (`ANTHROPIC_API_KEY` absent for the Opus seats; Codex Plus + Google personal OAuth absorb Codie/Annie; bounded `GEMINI_API_KEY` *only* if Annie routes via API) · no `start_new_session` on a costed worker · land via squash PR off `origin/main` · clean teardown. Full protocol: [`docs/fleet-ops-protocol.md`](../../architecture/fleet-ops-protocol.md).

## Standing doctrine (do not re-learn)
- **Verify the tree, never trust a label — including this plan.** The `agy -m` contradiction and the Gate-3 v1 crash are the cautionary tales: read the loop, not the docstring.
- **Stub-green before any spend.**
- **Patches stage, never auto-apply** (`auto_apply: false` — v2 lock).
- **A peer erroring is an honest errored gap, never a run-abort.**
- **The motion-proper blind spot is real and documented** — still judges (incl. contact-sheeted animatics) validate staging/identity/continuity, not true motion timing; the human owns motion.

## Reserved decisions
1. **Gate sequencing — DECIDED (Sean, 2026-06-10):** build the engine gate-agnostic, wire `pre_museum` as the validation vehicle, **defer `post_animatic`** until the Animatic phase lands (ready-to-plug seam + ticket).
2. **Annie transport if `agy` rejects `-m` — default-carried:** decide from the Step-0 smoke; default to the Gemini API transport (consistent with Em; confirms the served model) over accepting the Flash backend-default. Sean to confirm at the smoke result.
3. **Eval depth — default-carried:** structural tests + one live smoke + Bake-off 2 (Sage ablation) + a small Sean-rated adjudication check. Not an Em-style scored suite (wrong shape for a synthesis critic).
4. **Session split — DECIDED (Sean, 2026-06-10):** two Claude Code sessions — **(A)** Steps 0–2 (smoke + Codie transport + engine, all $0 stub-green) → **(B)** Steps 3–4 (`pre_museum` wiring + live smoke + Sage bake-off). Session A kickoff: [`docs/2026-06-10-t3-council-session-a-kickoff.md`](2026-06-10-t3-council-session-a-kickoff.md).

## Deliverables
- Step 0 research note (Open Q4 resolution: Annie `-m`, Codie image, video handling).
- `run_codex_with_image` + tests.
- `pipeline/agents/t3_council.py` (`T3CouncilNode`) + 4 standing-context preambles + `tests/test_t3_council.py`.
- `critics.t3:` manifest block + `pre_museum` gate wiring + declared/ticketed `post_animatic` seam.
- Live smoke trace + Bake-off 2 (Sage ablation) results under `evals/bakeoffs/`.
- State-of-record: CLAUDE.md (T3 row: pending → built), CHANGELOG entry, `docs/pipeline-architecture-v1.md` + `docs/production-checklist.md` status, manifest `critics.t3`.

---

*Plan status: APPROVED (Sean, 2026-06-10) — gate scope + two-session split locked. No spend, no code changed. Session A kickoff is paste-ready at [`docs/2026-06-10-t3-council-session-a-kickoff.md`](2026-06-10-t3-council-session-a-kickoff.md); Session B kickoff follows once A lands.*
