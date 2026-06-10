# T3 Council — Open-Q4 CLI multimodal smoke test (Session A, Step 0)

*Run 2026-06-10 in the `feature/t3-council-session-a` worktree. **$0** — subscription-absorbed
CLI calls (Google personal OAuth on `agy`); no `ANTHROPIC_API_KEY` / `GEMINI_API_KEY` billing.
Resolves the three transport unknowns before any council code depends on them. Standing
doctrine: **verify against the real binary, not the docstring.***

## TL;DR — the three resolutions

| # | Unknown | Resolution |
|---|---------|------------|
| 1 | Does `agy` v1.0.x accept `-m <model>`? | **NO.** `agy -m …` → `flags provided but not defined: -m`, exit 2. There is **no `--model` flag at all** in `agy --help`. The findings doc was right; the `cli_runners.py` A2 docstring is wrong. |
| 2 | Annie's transport (Reserved Decision 2) | **→ Gemini API** (`run_gemini_api_with_image`, `gemini-3.5-flash`, `model_version` read-back), consistent with Em. **NOT `agy`.** Flagged for Sean below. |
| 3 | Codie / `codex exec` image handling | **Unverified — `codex` not installed** on this machine. Build against the stub (kickoff-sanctioned); Session B confirms the live invocation. Documented shape below. |
| 4 | Video handling | **Contact-sheet path** (`pipeline/contact_sheet.py::build_contact_sheet`) confirmed present. No peer needs native video. Motion-proper blind spot accepted. |

---

## Environment

```
agy     → /Users/seanwinslow/.local/bin/agy   v1.0.4   (findings doc referenced 1.0.2)
codex   → NOT FOUND on PATH
gemini  → NOT FOUND on PATH   (the pre-Antigravity CLI; sunset 2026-06-18 anyway)
```

## TEST 1 — Annie / `agy -m` (text) — **REJECTED**

Command:
```
agy -m gemini-3.1-pro -p 'Return the JSON {"hello":"world"}. No other text.'
```
Result — **exit 2**, empty stdout. stderr (verbatim, trimmed to the load-bearing lines):
```
flags provided but not defined: -m
Usage of agy:
  --add-dir                       Add a directory to the workspace (repeatable) (default [])
  -c / --continue                 Continue the most recent conversation
  --dangerously-skip-permissions  Auto-approve all tool permission requests without prompting
  -i / --prompt-interactive       Run an initial prompt interactively and continue the session
  -p / --print / --prompt         Run a single prompt non-interactively and print the response
  --sandbox                       Run in a sandbox with terminal restrictions enabled
Available subcommands: changelog, help, install, plugin, update
```
**There is no model-selection flag on `agy` v1.0.4 at all.** This confirms the Anti-Gravity
findings (`-m` not on v1.0.2) and **falsifies the `cli_runners.py` A2 docstring**, which claims
`-m gemini-3.1-pro` is the model pin.

### ⚠ Latent bug surfaced (for Sean / a follow-up ticket — out of scope for Session A)
`run_antigravity_with_image` ([cli_runners.py:229](../../pipeline/agents/cli_runners.py#L229))
builds `cmd = [agy, "--dangerously-skip-permissions", "-m", model, *add_dirs, "-p", full_prompt]`.
On a real (non-stub) call this would **always fail with exit 2** on the installed `agy`, because
`-m` is rejected. It has never been caught because Em's production transport pivoted to the
Gemini API (`gemini_api`), so the agy `-m` path is never exercised live. **This Session does not
touch `cli_runners.py`'s agy path** (additive-only discipline) — flagging only. The clean fix is
either drop `-m`/`model` from the agy wrapper (model is unpinnable on this CLI by design — the
backend auto-routes) or formally retire the agy transport in favor of the Gemini API.

## TEST 2 — Annie / `agy` image read (no `-m`) — **WORKS, but agentic & meandering**

Command (the findings-doc incantation — `--add-dir` + plain path, no `-m`):
```
agy --dangerously-skip-permissions --add-dir characters/sean-anchor \
    -p 'Describe the image at characters/sean-anchor/anchor.png in one sentence.'
```
Result — **exit 0**, correct final answer:
> "The image at anchor.png depicts a cartoon-style sketch of a smiling young man with tousled
> blonde hair and blue eyes wearing a navy blue T-shirt, grey jeans, and grey sneakers while
> holding a white stylus in his hands against a textured cream paper background containing a
> circled 'A-2' label in the upper-left corner."

**But the path to that answer is the problem.** `agy -p` is not a clean attach-image→answer call —
it is a **full agentic harness**. Before viewing the image it ran ~30 tool steps: `find` sweeps of
scratch dirs, multiple Python scripts to ASCII-render the PNG, color-segmentation attempts, reading
`character.yaml`/`notes.md`/`cy-confidence-notes.md`, copying the file around — only then did its
`view_file` tool actually see the image. It also resolved the relative `--add-dir` oddly (searched
`~/.gemini/antigravity/scratch/16BitFit-V*` first). For a council **peer that must return a
structured JSON verdict deterministically**, this is fragile, slow, and non-reproducible.

**This is the second, independent reason to pick the Gemini API for Annie** (beyond the `-m`
rejection): the API gives a single clean multimodal call with a pinned, read-back model, no agentic
detour, no permission gymnastics.

## Reserved Decision 2 — RESOLVED → Gemini API for Annie (flagged for Sean)

> **Decision:** Annie (the T3 visual + identity/continuity peer) routes through
> **`pipeline/agents/gemini_api_runner.py::run_gemini_api_with_image`** (`gemini-3.5-flash` pinned,
> `resp.model_version` read-back), **not `agy`** — exactly as Em's production transport does
> (`critics.t2.transport: gemini_api`). Rationale: (a) `agy` rejects `-m`, so the model can't be
> pinned on the CLI — the silent-backend-default trap the whole A2 forensics existed to kill;
> (b) `agy -p` is an agentic harness, not a vision call, so verdicts wouldn't be deterministic.
> **Do not silently accept the `agy` Flash backend-default.** Session A wires Annie to the Gemini
> API transport; Session B can revisit if a vendor-diversity argument outweighs determinism (the
> T3 premise is heterogeneous *vendors* — Gemini for Annie still satisfies that vs. Codex/OpenAI
> for Codie and Anthropic/Opus for Sage).

## TEST 3 — Codie / `codex exec` — **binary absent, build against stub**

`codex` is **not installed** on this machine, so the live image invocation is **unverified**. Per
the kickoff ("if a binary isn't installed, record that and proceed against stubs — but say so
plainly"), Session A builds `run_codex_with_image` with a deterministic stub fallback that runs
CI-green, and **Session B confirms the live invocation**.

Documented invocation shape (from code-brain `lib/cli_runners.py::run_codex`, the proven
text-only vault-critic path):
```
codex exec --sandbox read-only --skip-git-repo-check <prompt>
```
- run from `Path.home()` (trusted via `~/.codex/config.toml [projects]`)
- stdout = markdown response; stderr = session metadata + `tokens used` footer
- rate-cap detected from stderr; returns a `CLIResponse(cli="codex", …)`, never raises on CLI failure

For **image** input (Codie sees stills), the anima wrapper mirrors the agy approach — reference
the image path(s) in the prompt body under read-only sandbox — and, pending Session B's live
check, may use Codex's `-i/--image <file>` multimodal flag if confirmed. **The stub path is what
runs in CI regardless**, so Session A is unblocked.

## TEST 4 — Video handling — **contact-sheet path confirmed**

`pipeline/contact_sheet.py::build_contact_sheet` ([contact_sheet.py:80](../../pipeline/contact_sheet.py#L80))
is present, with `sample_frame_indices` + `_extract_frames_to_dir` + `_collect_source_frames`. The
(future) Animatic / motion artifacts are reduced to a still **contact sheet** before any peer sees
them — **no peer needs native video.** This carries Em's accepted **motion-proper blind spot**: a
still-image judge sees staging / identity / continuity across a clip but **not** true motion timing.
`post_animatic` is deferred this session anyway (Phase 4 isn't built), so this is recorded, not wired.

## What Session A does with this

1. Build `run_codex_with_image` (stub-green; live shape documented above for Session B).
2. Wire **Annie → `run_gemini_api_with_image`** (Reserved Decision 2), not `agy`.
3. Leave `cli_runners.py`'s agy path untouched; surface the `-m` latent bug to Sean (above).
4. Council engine treats every peer's failure as a contained errored gap (Gate-3 lesson).

---

## SESSION B — Codie verified LIVE (2026-06-10), and the `-i` variadic bug it caught

Codex is now installed (`codex-cli 0.139.0`). Verified the binary before depending on it — and the
verification **caught a real bug in the Session-A wrapper**, exactly the "verify the binary, not the
docstring" hazard this doc was written to guard against (the agy `-m` lesson, recurring).

**The bug.** `codex exec --help` shows `-i, --image <FILE>...` is **variadic** (one-or-more values).
Session A built the command as `… --skip-git-repo-check -i <img> <prompt>` — prompt as the trailing
positional. Run live, the trailing prompt was **swallowed as a second image value**, leaving no
positional; codex fell back to stdin and exited 1:

```
$ codex exec --sandbox read-only --skip-git-repo-check -i <anchor.png> '<prompt>'
Reading prompt from stdin...
No prompt provided via stdin.       # exit 1
```

**The fix.** The prompt positional must come **before** the `-i` flags. Confirmed live:

```
$ codex exec --sandbox read-only --skip-git-repo-check '<JSON-verdict prompt>' -i <anchor.png>
{"verdict":"pass","confidence":0.9,"reasoning":"cartoon man holding pen"}   # exit 0, 15,378 tokens
```

`run_codex_with_image` was reordered to emit `[exec, --sandbox, read-only, --skip-git-repo-check,
(--model X), <prompt>, -i img1, -i img2, …]`. Regression test
`tests/test_cli_runners.py::test_codex_prompt_precedes_image_flags` captures the argv and asserts
`prompt_idx < min(-i idx)`; it was written RED (reproduced idx 9 vs 5), then GREEN after the fix. All
11 `test_cli_runners.py` tests pass (stub path unchanged → CI stays credential-free green).

**End-to-end live confirmation** through the real wrapper (not just raw codex):

```
run_codex_with_image(prompt=<Codie verdict prompt>, image_paths=[sean-anchor/anchor.png])
→ cli='codex'  exit_code=0  stub_fallback=False  ok=True
  text={"verdict":"pass","confidence":0.91,"reasoning":"Clear character sketch with appealing readable production design"}
```

Codie is **live, three-vendor council unblocked.** The flags `-s/--sandbox` (read-only valid),
`--skip-git-repo-check`, `-i/--image`, `-m/--model` are all confirmed present on 0.139.0.
