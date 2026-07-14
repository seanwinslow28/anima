# Field report — transport capability probes + pricing research (2026-07-13)

**Session:** the transport-strategy decision session ([decision doc](../active/2026-07-13-transport-strategy-decision.md) — RATIFIED; [kickoff](../active/2026-07-13-transport-strategy-decision-kickoff.md)).
**Spend:** ~35 Higgsfield credits (≈$1.20 at ULTRA-annual; refunds honored on the one 502) + ~$0 OpenAI (blocked, see §4) + $0 Gemini beyond six NB2 images (~$0.40). All Sean-greenlit at Checkpoint 1.
**Artifacts (local-only, gitignored):** `runs/2026-07-13-transport-probes/` — `CONTACT-SHEET.png`, per-transport plates (`openai-gpt/` `higgs-gpt/` `nb2-direct/` `higgs-nb2/`), shared prompts (`prompts/P1..P5.txt`), per-transport `run_*.sh` + logs + result URLs.

---

## 1. Probe design (P1 + P2, Checkpoint-1 greenlit)

The load-bearing question: **does Higgsfield's editing surface hold across-edit identity with anchor-first multi-reference injection** — the contract Cy's Bible pass lives on — at parity with the direct APIs?

- **Anchor:** `characters/sean-anchor/anchor.png` (pencil-test-colored; human face = the hardest identity read).
- **Chain:** four anchor-first plates (P1 ¾ view · P2 left profile · P3 surprised expression · P4 walk pose) + **P5 = an edit of P1** (wave; edit-of-edit drift check). Identical prompt files across every transport; 1:1; quality medium where the knob exists.
- **Transports:** OpenAI `gpt-image-2` direct (`images.edit`, openai-image-gen skill) · Higgsfield `gpt_image_2` (CLI, `--image` auto-upload) · Gemini NB2 direct (the production `invoke_image_edit` skill script) · Higgsfield `nano_banana_2` (CLI).
- **Accidental stress test (declared, not designed):** the prompts wrongly listed *"glasses"* in the preserve-list — the anchor has none (authoring slip). Every transport got the identical false hint, so it became a free anchor-vs-prompt dominance test. Glasses are **prompt noise**; identity was judged on face/hair/beard/outfit/proportions.

## 2. Results (Sean's eye = the arbiter; passed at Checkpoint 2)

| Transport | Plates | Read |
|---|---|---|
| **Higgsfield `gpt_image_2`** | 5/5 | **Most anchor-faithful row.** Identity + pencil register held on all five including the edit-of-edit; ignored the false "glasses" hint on every plate (anchor dominance). |
| **NB2 direct (Gemini API)** | 5/5 (+1 control) | Identity holds; **obeyed the false hint on 3/5 plates** (glasses appear P2/P4/P5 — prompt-over-anchor, inconsistently); P5 picked up a construction-grid background artifact. |
| **Higgsfield `nano_banana_2`** | 5/5 (after one 502 re-roll) | Identity holds; obeyed the false hint on **5/5** (consistently wrong-but-obedient); slightly mustier palette; P3 shirt drifted gray. |
| **OpenAI `gpt-image-2` direct** | 0/5 | **Blocked: `billing_hard_limit_reached`** (§4). The API *accepted* the model+endpoint combination — the request failed at billing, not validation. |

**Honesty caveats:** n=1 per cell; pencil register only (the actual gpt-image consumers are the gritty/flat registers — the in-register Bible-pass validation remains the GRANDMASTER production gate, plan §T2); same-model transport differences (NB2 direct vs via-Higgsfield) are within stochastic range — no transport-caused degradation is claimable from one sample.

**Verdict feeding the decision:** capability hard-gate **cleared at spike level** for Higgsfield `gpt_image_2` anchor-first editing → decision D4.

## 3. First-party Higgsfield facts (MCP + CLI, this session)

- **Account:** ULTRA, 4,038.64 credits at session start.
- **Plans (MCP pricing widget):** ULTRA 3,000 cr/mo — $99/mo annual, $129 monthly. Top-ups: 500/$26 · 1,000/$49 · 2,000/$95 · 4,000/$190 (≈$0.0475–0.052/cr; **90-day expiry**; prices are limited-promo, list ≈1.8×). "Unlimited" perks are **web-only** (tooltips first-party confirm) — CLI/MCP/API always metered.
- **`get_cost` dry-runs (no spend):** gpt_image_2 1k low/med/high = **0.5 / 2 / 4 cr**, 2k med = 3 cr; nano_banana_2 1k = **1.5 cr**, 2k = 2 cr; (research agent extended: NB Pro 1k/2k = 2 cr, 4k = 4; Seedance fast 720p = 3.5 cr/s, std 720p = 4.5, std 1080p = 9).
- **Per-surface default drift (measured):** CLI defaults 2k/high; MCP defaults 1k/low — same job name, 4–8× cost swing. → D5's explicit-params rule.
- **Editing contract:** `gpt_image_2` + `nano_banana_2` accept unbounded `medias` (role `image`, flat — no semantic anchor/style roles; role-tagging lives in prompt text, which is already anima's pattern). Seedance has real semantic roles (`start_image`/`end_image`/`image_references`/…).
- **Burn ledger (200 transactions, Jul 4–13):** ≈**1,620 cr / 9 days** (~180/day), ~⅚ video (Seedance 14–67.5 cr/clip), images 1.5–7 cr each; failed generations auto-refunded. Direct-API equivalent ≈ $300/mo vs the $99–129 sub → the sub self-justifies on exploration + motion.
- **Operational:** one mid-batch **HTTP 502** (credits refunded; re-roll succeeded) → runners need bounded 5xx retry. Outputs retained ~7 days → download immediately. CLI v0.2.3 installed locally; upstream already at v1.x (fast release cadence).

## 4. Vendor research highlights (3 web-research agents; full citations in their reports)

- **OpenAI:** `gpt-image-2` (pin dated snapshot `gpt-image-2-2026-04-21`) is the only durable target — `gpt-image-1-mini`/`1.5`/`chatgpt-image-latest` shut down 2026-12-01. Edits endpoint takes up to 16 reference images. Per-image (output tokens): low $0.006 / medium ~$0.053 / high ~$0.211 at 1024², **plus** image-input tokens on every anchor/ref (edit-heavy workflows reportedly run 2–3× baseline). **No served-model echo** in the response. Org verification (government-ID) required; Tier 1 = 5 images/min. **Sean's account is at its billing hard limit** — the direct fallback needs a cap raise + verification before it could ever be built.
- **Google (Gemini API):** the pinned preview IDs are deprecated (docs record shutdown 2026-06-25) — **but the probe's control call on `gemini-3.1-flash-image-preview` still served today** (empirical beats the report; repin is hygiene, decision D3 rider). GA pricing: NB2 1k **$0.067** (project's $0.07 verified), NB Pro 1k/2k **$0.134** (the routing table's $0.15 was ~11% high). New: `gemini-3.1-flash-lite-image` GA at ~$0.034/1k — a future draft-tier candidate.
- **fal.ai:** Seedance 2.0 fast 720p **$0.2419/s**, std 720p $0.3034/s; Seedream v4 edit is now **$0.03** (the runner comment's $0.02 is stale); qwen-edit-plus $0.03/MP verified. Prepaid credits, no subscription, concurrency-based limits.
- **Higgsfield (external):** ~$138M raised, reported talks at ~$5B valuation, ~$500M annualized revenue — not a sunset risk near-term. But: **no model-version field, no changelog; ToS permits silent model swaps + repricing and grants them training rights on inputs/outputs**; a live naming muddle (CLI job type `nano_banana_2` *displays* "Nano Banana Pro"). A key-based **Cloud API exists** (`platform.higgsfield.ai`, `Key {key}:{secret}`, official Python SDK) but its public docs only prove Soul/Reve/Seedance-v1 — current-model coverage unverified; the full roster is only proven on the OAuth CLI/MCP surfaces.

## 5. Riders + loose ends this session leaves

1. **Gemini GA repin** (decision T3) — `registers.py` NB2/NB Pro constants + skill-script default + tests.
2. **fal Seedream cost comment** in `fal_runner.py` (`$0.02` → `$0.03`) — cosmetic, batch with T3.
3. **OpenAI billing cap + org verification** — Sean-side, only if the direct gpt-image fallback is ever built.
4. **The GRANDMASTER in-register edit-identity validation** (T2) is *not* discharged by this probe — pencil-register evidence only.
5. Probe prompts carried the "glasses" noise — reusable probe harness should fix the preserve-list before any re-run.
