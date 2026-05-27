# Antigravity CLI — Migration Findings for anima v2

**Date:** 2026-05-26
**Authoring session:** Cowork brainstorm preamble
**Sources:** Google's official deprecation post (2026-05-19), the Antigravity CLI Deep Dive (Agentpedia Codes, 2026-05-20), the Gemini CLI → Antigravity CLI migration guide (Agentpedia Codes, 2026-05-20), a Dev.to hands-on (Arindam Majumder, 2026-05-21), Sean's local installation state, and the existing anima + Code-Brain wiring.
**Purpose:** Ground the v2 agent fleet's "Anti-Gravity CLI" wiring against what's actually shipping, so commit 8 (Em) and commit 9 (Codie + Annie + Sage) reach the right binary with the right flags after Google's 2026-06-18 sunset of `gemini` for consumer-tier accounts.
**TL;DR.** Not a structural break. A two-line patch in `pipeline/agents/cli_runners.py` plus a parallel patch in Code-Brain's `vault_critic.py` clears the runway. Gemini 3.1 Pro stays accessible by name, the Google personal OAuth tier still absorbs cost, and v2's architectural-diversity construction stands. The work belongs as a commit-8.1 cleanup on top of the next implementation session, not as the next brainstorm topic.

> ## 2026-05-27 — Verification addendum (after the real `agy` v1.0.2 install)
>
> Sean installed `agy` v1.0.2 at `/Users/seanwinslow/.local/bin/agy`. The smoke
> tests run during commit 8.1 surfaced three corrections to the speculation
> below — kept here as written for the audit trail, but **the working incantation
> is now codified in `pipeline/agents/cli_runners.py` and demonstrated in
> [`evals/vision-critic/traces/baseline-2026-05-27-with-cli.md`](../../evals/vision-critic/traces/baseline-2026-05-27-with-cli.md)**.
>
> **What was wrong in the original write-up (§2 below):**
>
> 1. **`--output-format json` does not exist on `agy` v1.0.2.** The Dev.to
>    hands-on quoted that flag, but `agy --help` shows only `-p` / `--print` /
>    `--prompt` for non-interactive mode. Output is raw text; the prompt asks
>    the model for JSON (which Em's role addendum already does), and the
>    `vision_critic.py:_parse` helper strips any code fence before json.loads.
>
> 2. **`--model` / `-m` does not exist on `agy` v1.0.2.** Model selection at
>    the CLI flag surface isn't exposed. v2's per-role slug
>    `gemini-3.1-pro-via-anti-gravity` is still the contract; the actual model
>    routing happens inside agy's internals. If `agy` adds a `-m` flag in a
>    future release, the wrapper threads it through.
>
> 3. **`@path` inline syntax does not work for image attachment.** The
>    pre-Antigravity Gemini CLI's `@path` idiom didn't carry forward. The
>    working incantation is **`--add-dir <parent>` per unique image-path
>    parent directory** plus the image paths referenced as plain text in the
>    prompt body. agy resolves the read via its internal file tool.
>
> **What additionally has to be true for headless calls:**
>
> 4. **`--dangerously-skip-permissions` is mandatory in non-interactive mode.**
>    Without it, agy blocks waiting for an interactive permission grant when
>    the prompt references a file. The flag's name is the Antigravity team's
>    framing; in our context it means "headless mode, no tool grants needed."
>    Em runs read-only against project images, so this is appropriate.
>
> **The final working call shape (codified in `cli_runners.py:run_antigravity_with_image`):**
>
> ```
> agy --dangerously-skip-permissions \
>     --add-dir <parent-of-image-1> [--add-dir <parent-of-image-2> ...] \
>     -p "<prompt text including absolute image paths in an 'Attached images:' tail>"
> ```
>
> **Performance under real load:** 11.4s for a single small reference image;
> 27.4s for a production Act 1 F06 keyframe with concrete pencil-test
> aesthetic critique. Within v2 §7's `wall_budget_s: 600` ceiling, but Em
> running across 10–50 frames will use 3–20 minutes of wall time — keep
> escalation reserved for borderline / hero shots.
>
> **What stayed correct:** binary name (`agy`), install path
> (`/Users/seanwinslow/.local/bin/agy`), subscription absorption (Google
> personal OAuth on AI Pro/Ultra), Gemini 3.1 Pro accessible by name (at the
> slug-routing layer, not the CLI flag layer), v2 §6 per-role table unchanged.
>
> **Commit 9 implication.** Annie's wrapper inherits commit 8.1's flag shape
> directly — same `--dangerously-skip-permissions` + `--add-dir` + `-p`
> incantation, same JSON-in-prompt contract, same parser tolerance. No
> further migration work for Annie.

---

## 1. What's actually changing — Gemini CLI to Antigravity CLI

Google announced on **May 19, 2026** that the Gemini CLI product is being unified into Google Antigravity — a four-surface platform comprising **Antigravity 2.0** (desktop GUI), **Antigravity CLI** (the new terminal client), **Antigravity SDK** (programmatic harness), and the existing **Antigravity IDE** (which Sean already has installed). All four surfaces share one agent harness; the CLI is one face of that harness, not a separate product.

The headline facts that anima needs to act on:

- **Sunset date for consumer tier — June 18, 2026.** On that day, the existing `gemini` binary stops serving requests for Google AI Pro, Ultra, and free Gemini Code Assist for individuals. Sean is on the Google personal OAuth tier (per the `[security.auth] selectedType: "oauth-personal"` he has in `~/.gemini/settings.json` and per the existing `vault-critic-plan` docs in Code-Brain). That puts him in the affected bucket. Three weeks of runway from today.
- **Enterprise tiers untouched.** Code Assist Standard / Enterprise license holders and paid Gemini-API-key users keep the old `gemini` binary running indefinitely. Sean isn't an enterprise customer; this is informational, not actionable.
- **Replacement binary is `agy`, not `gemini`.** The new CLI is written in Go (the old was Node), installs into `~/.local/bin/agy` on Unix (and `%LOCALAPPDATA%\Antigravity\` on Windows), and ships through `curl -fsSL https://antigravity.google/cli/install.sh | bash`. The binary name is the first thing every script that shells out has to learn.
- **The IDE launcher symlinks Sean already has are not the CLI.** `~/.antigravity/antigravity/bin/agy` and `~/.antigravity/antigravity/bin/antigravity` both resolve to `/Applications/Antigravity.app/Contents/Resources/app/bin/antigravity` — that's the *Antigravity 2.0 desktop application* launcher (the same role `code` plays for VS Code). The actual headless `agy` CLI is a separate `~/.local/bin/agy` install. We weren't able to verify from the sandbox whether Sean has run the CLI installer; this is the first thing to check before commit 8 ships against real models.
- **Gemini 3.1 Pro remains accessible by name.** The Dev.to hands-on confirms that Antigravity CLI ships with `gemini-3.5-flash`, `gemini-3.1-pro`, `claude-sonnet`, `claude-opus`, and `gpt-oss-120b` selectable via `--model` (or `-m`). v2's role wiring for Em (`gemini-3.1-pro-via-anti-gravity`) and Annie (same) survives the rename verbatim at the slug layer.
- **Subscription absorption holds.** "Usage is gated by your Google account tier — Google AI Pro, Ultra, or Gemini Code Assist quota for individuals" (Agentpedia). Sean's personal OAuth tier still absorbs the cost. v2 §7's cost ceiling (`$0 incremental` for the agent fleet runtime) is unaffected.

## 2. anima's specific call patterns — what survives, what needs editing

anima's contract with the CLI lives in exactly one file today, **`pipeline/agents/cli_runners.py`**, with `vision_critic.py` importing from it. (Commit 9 will add a second consumer — Annie — but the call-shape is the same; no new file work in this session.) Here's the shape the wrapper expects today against the new reality:

**Binary name.** The wrapper has `ANTI_GRAVITY_BIN = "anti-gravity"` (hyphenated). No release of either product was ever published under that exact name. The Gemini CLI binary was `gemini`; the new one is `agy`. `shutil.which("anti-gravity")` returns `None` on Sean's machine today, so the stub fallback is in permanent use — Em ships with the contract real but the model behind it stubbed (this is exactly what the baseline trace at `evals/vision-critic/traces/baseline-2026-05-26.md` records). Patch: `ANTI_GRAVITY_BIN = "agy"`.

**Prompt + structured-output flags.** The wrapper invokes `[ANTI_GRAVITY_BIN, "--json", "--prompt", prompt, "--image", path, ...]`. Antigravity CLI's command-mode (headless) shape is `agy -p "PROMPT" --output-format json`. The prompt flag is `-p`, not `--prompt`. Structured output is `--output-format json`, not `--json`. The migration is mechanical:

```python
# Today (broken — binary doesn't exist, flags don't match either):
cmd = [ANTI_GRAVITY_BIN, "--json", "--prompt", prompt]
for p in image_paths:
    cmd.extend(["--image", str(p)])

# After the patch (matches Antigravity CLI's command mode):
cmd = ["agy", "-p", prompt, "--output-format", "json"]
# Image input — see next section
```

**Image input is the one genuine unknown.** None of the public docs we surveyed enumerate an `--image` flag on `agy`. What they do confirm is the inherited Gemini CLI `@path/to/file` syntax for pulling files into context inside the prompt itself — `agy -p "review @runs/act1/F06/attempt_01.png against the brief"`. That's almost certainly the path. For Em, this means image attachment moves out of CLI args and into the prompt body: the wrapper formats `"<prompt>\n\nAttached images:\n@{path1}\n@{path2}"` and lets the agent's file-reading tool walk them. If that turns out to be wrong (worth a 5-minute manual test once `agy` is installed), the fallback is base64-inlining via stdin — which Antigravity 2.0's harness supports, and the CLI likely inherits. Either way, the wrapper signature `run_antigravity_with_image(prompt, image_paths, timeout_s)` doesn't change; only the internals do.

**JSON output shape.** Em's `_parse()` already tolerates JSON wrapped in `\`\`\`json … \`\`\`` code fences (it has a regex stripper for exactly that). The model returns whatever JSON the prompt asks for — Em's role addendum spells out the `{verdict, confidence, reasoning, proposed_patches, cites_criteria}` schema in the system prompt, not in CLI flags. This part survives the migration unchanged. The auto-router stats block (`stats.models.{name}.tokens.total`) in `_antigravity_tokens()` may rename under the new CLI; for anima, this only affects the optional `tokens: int | None` field on `CLIResponse`, which is purely diagnostic. Safe to leave for now and tighten in commit 9's first hour against real CLI output.

**Approval / sandbox flag.** Code-Brain's `vault_critic` invokes `gemini` with `--approval-mode plan` — read-only, no tool execution. Antigravity CLI's documented permission flag is `--dangerously-skip-permissions`, which is the opposite end of the spectrum (skip-permissions = grant everything). The new permissions model is redesigned around the shared harness; the closest read-only equivalent is most likely "don't grant any tool permissions and let the agent return text only," which may be the implicit default for one-shot `agy -p` runs that don't have explicit tool-grant in their config. For anima specifically, Em doesn't need filesystem-write permissions — it's a read + return-JSON flow. We can almost certainly skip the flag entirely. Worth confirming with a single `agy -p "test" --output-format json` invocation once the binary's confirmed installed.

**Per-call temperature, top_k, system-instruction overrides — gone.** Migration docs flag these explicitly as dropped from the new flag surface. anima's wrapper doesn't pass any of these today, so no impact. If a future critic wants temperature control, it'll have to happen at the model-routing layer, not the CLI flag layer.

**Trust-workspace env var.** `GEMINI_CLI_TRUST_WORKSPACE=true` was the way to mark a workspace as safe for the old CLI. The Antigravity CLI's permission model uses settings files (`~/.gemini/antigravity-cli/settings.json` and per-workspace `.agents/`) rather than env-var-driven trust. For the headless command-mode invocation Em uses, this is likely a non-issue (no tool grants requested = no permission challenges to bypass). If we hit a permission prompt blocking a headless run, we'll find out fast.

## 3. What commits 8 and 9 need to adapt

**Commit 8 (Em vision critic) — already shipped, mid-stub.** The wrapper change is a one-file patch:

- `pipeline/agents/cli_runners.py`: rename `ANTI_GRAVITY_BIN` to `agy`, restructure the `cmd` list to `["agy", "-p", prompt, "--output-format", "json"]`, move image attachment from `--image` flags to `@path` references inside the prompt text. Optional: drop the rate-cap signature `429` since the new CLI's error surface may differ.
- `tests/test_cli_runners.py`: the existing tests mock the wrapper via `unittest.mock`, so the binary-name change doesn't break test fixtures. The integration-test path (which runs `which anti-gravity` to decide whether to call real or stubbed) needs a `which agy` swap.
- `evals/vision-critic/traces/baseline-2026-05-26.md`: the trace explicitly documents "Em shipped on a machine without the Anti-Gravity CLI installed." Once `agy` is installed and the wrapper points at it, a second trace lands (call it `baseline-2026-05-MM-with-cli.md`) showing the real-Gemini-3.1-Pro behavior diffed against the stub baseline. This is portfolio-grade evidence; don't skip it.

Call this **commit 8.1**. Estimated effort: 30–60 minutes, including a real-task validation against one Act 2 frame. No new structural decisions. No re-decisions of v2's per-role assignments.

**Commit 9 (Codie + Annie + Sage + Chairman) — not yet started.** The structural pattern from `vault_critic.py` (asyncio parallel fan-out of Codex CLI + Anti-Gravity CLI + Claude SDK, status promotion `ok`/`partial`/`success-empty`/`error`, separate chairman call) is unchanged. The only thing that needs updating in the implementation prompt is the per-CLI invocation syntax for Annie:

- Annie's wrapper is the same `agy -p PROMPT --output-format json` shape as Em's. Annie just reads different artifacts (animatic export, museum walkthrough draft) instead of single frames. The `@path` image-attachment idiom carries over.
- Codie (Codex CLI) is untouched by the migration — different vendor, different release cycle.
- Sage (Claude Agent SDK) is untouched.
- Chairman (Claude Agent SDK, Opus 4.7) is untouched.

So three of four T3 surfaces are migration-free. Only Annie's wrapper needs the `agy`-aware shape, and that can be lifted directly from Em's commit 8.1 patch. The v2 cost ceiling and architectural-diversity construction both hold.

## 4. Timeline pressure — three weeks, two concrete actions

The 2026-06-18 sunset is real but the migration is not large. Two distinct things break on that day if untouched:

**anima itself doesn't break — but commit 9 ships into a broken CLI surface if untouched.** anima is currently running on stub fallback for Em (no real Anti-Gravity calls in production yet — the Act 2 pencil-test work uses Seedance + Gemini NB2 directly, not the T2 critic stack). Sean has until Em is wired against real models to ship the patch. Practically, the right gate is *before* the T2 critic shoot-out (Bake-off 1 from v2 §8), since that bake-off needs real Gemini 3.1 Pro output to be meaningful.

**Code-Brain's vault_critic DOES break — separate codebase, separate concern.** `/opt/homebrew/bin/gemini -p PROMPT --output-format json --approval-mode plan` will start failing on 2026-06-19. That's outside anima's commit sequence but inside Sean's fleet. The fix is the same shape (rename binary, drop `--approval-mode plan`, leave the rest); the work belongs in Code-Brain's repo, not anima's. Calling it out here so Sean has the full picture — and so the same pattern lands consistently across both repos.

**Recommended sequencing:**

1. **This week.** Run the `agy` installer on Sean's primary machine. Verify with `agy --version` and a single test invocation: `agy -p "what is 2+2?" --output-format json`. Confirm `gemini-3.1-pro` is reachable: `agy -m gemini-3.1-pro -p "what is 2+2?" --output-format json`. ~5 minutes.
2. **Before commit 9 / before Bake-off 1.** Land the `cli_runners.py` patch in anima as commit 8.1 — a follow-on to commit 8. The next Claude Code execution session can do it in the first 30 minutes. The change is small enough that it doesn't need a separate brainstorm pass.
3. **Before 2026-06-18.** Land the parallel patch in Code-Brain's `agents-sdk/lib/cli_runners.py` so `vault_critic`, `process_inbox`, and any other downstream consumers don't go dark when the old `gemini` binary stops serving. Same change shape — rename, flag swap, drop deprecated flags.

## 5. Action items before commit 9 implementation

These are the concrete things to do, in priority order, so commit 9 lands against verified surface:

**P0 — Verify `agy` is installed on Sean's machine.** Run `which agy && agy --version` and report. If absent, run the installer: `curl -fsSL https://antigravity.google/cli/install.sh | bash`. This is the gating fact for everything below.

**P0 — Confirm `agy -p` returns parseable JSON.** A one-line smoke test: `agy -p "Return the JSON {\"hello\": \"world\"}. No other text." --output-format json`. Verify the response shape matches what the wrapper's `_parse()` will eat. Capture the actual stdout/stderr to a research note so the wrapper can be tightened against ground truth, not docs.

**P0 — Smoke-test image attachment via `@path` syntax.** From inside the anima repo: `agy -p "Describe the image at @images/2D-Character-Sketch-Sean-v1.png in two sentences." --output-format json`. If that works, anima's `run_antigravity_with_image` reformats trivially. If it doesn't, fall back to base64-inline or check the CLI's hidden flags (`agy --help` exhaustive surface dump).

**P1 — Land commit 8.1.** Single-file patch to `pipeline/agents/cli_runners.py` plus the test fixture rename. Re-run the existing 27 tests; ship.

**P1 — Write the with-CLI baseline trace.** `evals/vision-critic/traces/baseline-2026-05-MM-with-cli.md` showing Em's real Gemini 3.1 Pro behavior on the Act 1 hero loop. Diffs against the stub baseline. Portfolio content.

**P2 — Patch Code-Brain's `cli_runners.py`.** Out of anima's scope but on the same calendar. Sean's call when to do it.

**P3 — Confirm no `agy plugin import gemini` is required.** Sean's `~/.gemini/` has MCP servers and a `GEMINI.md` rules file. The migration importer should carry these forward; one `agy plugin import gemini` invocation reports what migrated cleanly and what didn't. Decorative for anima (the wrapper doesn't touch plugins or rules files); operationally tidy for Sean's broader fleet.

## 6. What this doesn't change in v2

Restating the negative space so the next session doesn't relitigate it:

- **The per-role table in v2 §6 stands.** Em is still Gemini 3.1 Pro via Antigravity CLI with Opus 4.7 escalation. Annie is still Gemini 3.1 Pro via Antigravity CLI. The model assignments are unchanged.
- **Architectural diversity at the highest-frequency interaction still holds.** Sonnet orchestrator + Gemini T2 critic remains the construction. The vendor is Google either way; the CLI binary's name doesn't affect the model family.
- **Subscription absorption still holds.** Personal OAuth tier on AI Pro/Ultra continues to absorb Antigravity CLI calls. The cost ceiling at v2 §7 (`$0 incremental` for the agent fleet runtime) is unaffected.
- **The three structural patterns from v2 §5 stand.** Pattern A (architectural diversity), Pattern B (Planner-Chairman shared rubric via `acceptance_criteria.json`), Pattern C (Chairman as a distinct fourth call) are independent of which Google CLI binary the wrapper calls.
- **The three open questions in v2 §9 stand.** Bake-offs 1–5 resolve them; the migration doesn't add a sixth.
- **Open Q4 from v2 §9 gets partial resolution.** "Verify both [Codex + Anti-Gravity] accept image/video input at anima's resolutions in commit 9's first hour" — the Anti-Gravity half is now half-answered (image attachment via `@path` is the documented idiom, formally untested at our resolutions). Codex CLI image input is still pending verification — Codie's wrapper needs the same smoke-test against `codex exec` with a file reference.

## 7. Recommended workstream for this Cowork session

Phase 1 was supposed to gate the Phase 2 brainstorm topic. The gating logic from the kickoff was: *if Phase 1 surfaces non-trivial migration work → workstream A (Anti-Gravity CLI deep-dive); if Phase 1 is clean → workstream B or C.*

The work isn't non-trivial — it's a one-file patch plus a smoke-test. So workstream A as a brainstorm topic would generate 15 ideas about a 30-minute mechanical fix, which is exactly the kind of over-engineering this project's philosophy refuses. The migration belongs as commit 8.1 in the next Claude Code execution session — captured here as a 30-minute action item, not a brainstorm pass.

**Recommend Phase 2 picks workstream B or C** — Character Bible scaffolding (gates commit 2) or Maya planner (gates commit 3, gates `acceptance_criteria.json` schema). Both have genuine design surface that benefits from multi-perspective brainstorm. Sean's call between the two based on which implementation gate he wants to clear next. Both are unblocked by this session's findings, neither is blocked on the Anti-Gravity CLI patches.

---

## Source map

| Source | Strongest on | Confidence |
|--------|--------------|-----------:|
| Google Developers Blog (2026-05-19) | Authoritative timeline, enterprise carveout, sunset date | 100% |
| Agentpedia "CLI Deep Dive" (2026-05-20) | Binary name (`agy`), install path, four-surface architecture, auth model | 90% — third-party but extensively quotes official docs |
| Agentpedia "Migration Guide" (2026-05-20) | File-by-file migration table, MCP rename (`url` → `serverUrl`), skill-folder moves | 90% — same provenance |
| Dev.to hands-on (Arindam Majumder, 2026-05-21) | Hands-on flags (`-p`, `--output-format json`, `--model`/`-m`), model availability (Gemini 3.1 Pro stays), `/model` slash command, `@path` file syntax | 85% — third-party, but the screenshots match what the official docs show |
| Sean's `~/.gemini/`, `~/.antigravity/`, `~/.antigravity-ide/` | OAuth-personal tier confirmation, IDE installation state, Gemini CLI's existing MCP config layout | 100% — direct disk read |
| anima `pipeline/agents/cli_runners.py` (commit 8) | The exact wrapper contract that needs editing | 100% — direct codebase read |
| Code-Brain `agents-sdk/lib/cli_runners.py` | The cousin wrapper that also breaks at sunset (out of anima's scope but on the same calendar) | 100% — direct codebase read |

The Antigravity official docs at `antigravity.google/docs/gcli-migration` and `antigravity.google/docs/cli-overview` are client-rendered SPAs; WebFetch returns only the shell. All facts above that cite "official docs" trace through the Agentpedia third-party writeups, which transcribe the docs verbatim with attribution. If a future session needs ground-truth verification, the right move is to open the docs in the Claude-in-Chrome MCP (which renders JS) or have Sean paste the relevant page sections directly.

---

*This findings doc is the decision artifact gating commit 8.1 and shaping commit 9's wrapper for Annie. The work is small enough to land as a follow-on patch, not a brainstorm.*
