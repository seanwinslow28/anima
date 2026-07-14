# Transport strategy decision — direct APIs vs. Higgsfield-for-everything

**Date:** 2026-07-13 · **Status:** **RATIFIED** (Sean, 2026-07-13, Checkpoint 2) · **Workstream:** the outward turn / animation-vocabulary-expansion (infrastructure decision within it — resolves the standing deferred-gpt-image-transport ticket; opens no new workstream).
**Session shape:** brainstorm (5 axes locked) → Human Checkpoint 1 (frame + probes greenlit) → research pass (3 fresh-pricing research agents + first-party Higgsfield MCP/CLI data + live capability probes) → Human Checkpoint 2 (Sean's eye on the probe plates + ratification).
**Evidence:** [probe + pricing field report](../anima-test-runs/2026-07-13-transport-probes-and-pricing-field-report.md) · probe artifacts (local-only): `runs/2026-07-13-transport-probes/` (`CONTACT-SHEET.png` + per-transport plates + prompts + logs).
**Origin:** [kickoff](2026-07-13-transport-strategy-decision-kickoff.md).

---

## 1. The decision frame (locked at Checkpoint 1)

Sean's answers structured the whole decision — recorded so future sessions don't re-litigate:

1. **Capability is a hard gate.** Any workload where a direct API measurably beats Higgsfield stays direct; Higgsfield earns each workload by matching quality. Hybrid was the expected outcome, not a compromise.
2. **At parity, marginal cost at real volume is the tiebreaker** (not one-bill simplicity, not lock-in aversion in the abstract).
3. **The ULTRA subscription is on the table** — modeled at full monthly cost against the direct-API bill it displaces, not treated as sunk.
4. **Scope:** three lanes — exploration/brainstorm generation (character/background/style/motion/angle dev, Step-S spikes, ART-VIZ), production image gen/edit (Cy Bible passes + Phase 5 frames), and Motion (Seedance). **Em's verification and the text agents stay direct — off the table** (pinned `gemini-3.5-flash` + served-model read-back; Anthropic subscription billing per fleet-ops).
5. **Cached-CLI-auth is acceptable for production transports.** Sean is at the keyboard for costed runs anyway; `higgsfield auth login`'s human-only OAuth is not a disqualifier.

## 2. The ratified calls

### D1 — Exploration lane → **Higgsfield, standing default** (ratifies existing practice)
Breadth of models is the entire value; Sean's eye reviews everything, so the capability gate barely binds; ~1,400+ credits of real harness work already prove it. The Step-S look-spike guidance in the [authoring playbook](../architecture/style-register-authoring-playbook.md) (ChatGPT / Google Flow / Higgsfield web) is unchanged — this ratifies Higgsfield CLI/MCP as the *programmatic* exploration surface too.

### D2 — Motion → **Higgsfield Seedance; fal stays the verified exit hedge**
Same underlying model both paths; Higgsfield is ~half fal's price (Fast 720p: 3.5 cr/s ≈ **$0.116/s** at ULTRA-annual vs fal **$0.242/s**) and carries richer reference roles (`start_image` / `end_image` / `image_references` / `video_references` — real semantic roles, richer than fal's start/end pair). When Phase 6 Motion wires into the orchestrator, it targets the Higgsfield transport. `fal_runner.py` stays verified + retained (the 2026-06-10 B0 verification holds) as the documented fallback — the exit cost of D2 is a transport re-point, not a rebuild.

### D3 — NB2 / NB Pro production workloads → **stay direct (Gemini API)** + GA repin rider
Already wired, criteria-locked Bibles and plate caches live on this path, and it carries anima's only strong provenance story (pinned model ID + `resp.model_version` read-back — the A2 discipline). Moving would save pennies (~$0.017/image) and forfeit that. **Rider (hygiene, next build):** repin `gemini-3.1-flash-image-preview` → **`gemini-3.1-flash-image`** and `gemini-3-pro-image-preview` → **`gemini-3-pro-image`** in `pipeline/registers.py` (+ skill script default + tests). Google's docs record the preview IDs as deprecated/shut-down 2026-06-25, yet the probe's control call **still served on the preview ID today** — repin is announced-deprecation hygiene, not an emergency.

### D4 — gpt-image → **wire via Higgsfield (`gpt_image_2`); OpenAI-direct is the documented fallback, not built**
This resolves the forcing function: `primal-sketch-grit`, `samurai-jack-s5`, `flat-cast-painted-world`, and GRANDMASTER stop being blocked on an OpenAI runner.

Why Higgsfield wins this one:
- **Capability (the hard gate):** the P1 probe — anchor-first multi-reference edit chain, 4 plates + 1 edit-of-edit — held identity and register on every plate via Higgsfield `gpt_image_2`; **Sean's eye passed it** at Checkpoint 2. It was also the only row that ignored a deliberately-wrong preserve-list item (anchor dominance over prompt noise).
- **Cost:** parity-or-better (1k medium: 2 cr ≈ $0.066 vs direct ~$0.041–0.053 *plus* a real input-token tax on every anchor/ref; 1k high: 4 cr ≈ $0.13 vs direct ~$0.211+tax).
- **The direct path's pinning advantage is weak for OpenAI specifically:** the Images API has **no served-model echo** (request-side dated-snapshot pinning only, `gpt-image-2-2026-04-21`), and is operationally gated — org verification required, Tier-1 caps at 5 images/min, and Sean's account is currently at its **billing hard limit** (the direct probe leg could not run).
- **Fallback prerequisites recorded** (Sean-side, only if/when the fallback is ever built): raise the OpenAI billing cap; complete org verification; pin the dated snapshot.

### D5 — Build **one `higgsfield_runner.py`**, shaped like `nb_pro_runner.py`, with the weak-pinning mitigations baked in
The runner is where Higgsfield's structural risks get managed:
- **Content-addressed cache** (prompt + ref hashes + model + explicit params → key), mirroring `_compute_cache_key`.
- **Credential-free stub fallback** (placeholder PNG, `stub_fallback=True`) so `python -m pytest tests/` stays green with no login — the standing CI ladder. `ANIMA_FORCE_STUB` honored.
- **Explicit `resolution` + `quality` on every call, never surface defaults** — measured per-surface default drift (CLI defaults 2k/high, MCP 1k/low) swings cost 4–8× for the same job name.
- **5xx retry with bounded attempts** (a real HTTP 502 hit the probe mid-batch; failed jobs auto-refund credits per Higgsfield's FAQ, so retry is safe).
- **Immediate download** of results (Higgsfield retains outputs only ~7 days) + **job-id + display-name provenance log** per generation — the honest substitute for served-model read-back (Higgsfield exposes no version field and its ToS permits silent model swaps; the naming muddle is real — the CLI's `nano_banana_2` job type *displays* "Nano Banana Pro").
- **Model allowlist at the boundary** (mirror `SUPPORTED_IMAGE_MODELS` — exact job-type names, fail-loud on anything else). `pipeline/registers.py` keeps recording the honest vendor model (`gpt-image-2`); the transport map, not the register, owns `gpt-image-2 → higgsfield:gpt_image_2`.

### D6 — Standing constraints (survive any future re-decision)
Em + text agents stay direct (frame item 4). Cache keys always encode transport + model + explicit params. The credential-free stub ladder is non-negotiable for every runner. Accepted trades, recorded eyes-open: Higgsfield may swap/reprice silently (mitigated by D5's provenance log + the D2/D4 fallbacks), retains training rights on inputs/outputs (ToS §4.4), and its full current-model roster is only proven on the OAuth surfaces (the key-based Cloud API exists but its current-model coverage is unverified — re-check if headless/cron ever becomes a hard requirement).

## 3. The pricing model (why the money says this)

First-party numbers (Higgsfield MCP `get_cost` dry-runs + plans widget + Sean's real transaction ledger; fresh vendor price sheets), 2026-07-13:

| Unit | Direct API | Higgsfield @ ULTRA-annual ($0.033/cr) |
|---|---|---|
| NB2 image (1k) | $0.067 | 1.5 cr ≈ $0.050 |
| NB Pro image (1k/2k) | $0.134 | 2 cr ≈ $0.066 |
| gpt-image (1k medium) | ~$0.041–0.053 + ref-input tax | 2 cr ≈ $0.066 |
| gpt-image (1k high) | ~$0.165–0.211 + ref-input tax | 4 cr ≈ $0.13 |
| Seedance Fast 720p | $0.242/s (fal) | 3.5 cr/s ≈ $0.116/s |
| Seedance Std 720p | $0.303/s (fal) | 4.5 cr/s ≈ $0.149/s |

ULTRA = 3,000 cr/mo at $99/mo annual ($129 monthly); top-ups ≈ $0.0475–0.052/cr (90-day expiry, promo-fragile). Sean's measured burn: **~1,620 credits in 9 days** (Jul 4–13; ~⅚ video) — direct-API equivalent ≈ $300/mo vs the $99–129 sub. **Exploration + Motion justify the subscription on their own; production images are a rounding error on either path** — which is exactly why D3 could be decided on structure (pinning) rather than dollars.

## 4. The phased build plan (a later session executes; nothing here is built)

| Phase | What | Gate |
|---|---|---|
| **T1** | `higgsfield_runner.py` (D5 spec) + transport map + `gpt_image_2` route + TDD suite (stub-green; live smoke is a small Sean-gated spend) | Sean greenlights the build session |
| **T2** | The **real GRANDMASTER production gate**: in-register (primal-sketch-grit) Bible-pass-shaped edit-identity validation via Higgsfield `gpt_image_2`, Sean-eyed — this probe was pencil-register; the gritty register is the actual consumer | rides the costed, Sean-greenlit GRANDMASTER build (unchanged gate, now with a chosen transport) |
| **T3** | Gemini GA repin (D3 rider): `registers.py` constants + skill-script default + tests | next Fable build; batch with the standing `primal-sketch-grit.generation_model` code note if not already landed |
| **T4** | Phase 6 Motion wiring targets Higgsfield Seedance (D2); fal path kept verified | when Motion enters the orchestrator (its own workstream slice) |

**What this decision does NOT change:** Em's pinned Gemini API transport and eval baselines; text-agent transports + fleet-ops billing discipline; the locked Bibles and their plate caches; the register registry's honest `generation_model` records and the fail-loud `UnwiredTransportError` boundary (it stays until T1 actually wires the route — never a silent fallback); the R→S→B playbook (its §Transport ladder gets a pointer to this doc at T1 time).
