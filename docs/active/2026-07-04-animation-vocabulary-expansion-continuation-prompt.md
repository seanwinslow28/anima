# Continuation prompt — animation vocabulary expansion (for a fresh Opus 4.8 session)

*Paste the block below into a fresh Claude Code session (Opus 4.8, `[1m]`). It continues the animation-vocabulary-expansion workstream where the prior session left off. It is self-contained but points at the source-of-truth docs — verify against main, don't trust this summary.*

---

You are continuing anima's **animation-vocabulary-expansion** workstream: turning the closed six-register style vocabulary into a **deliberately-growing, still-closed** multi-animator "powerhouse" — a bigger closed vocabulary + a reusable extension pattern + deep per-style research, NOT an open-ended freeform style string. The closedness is load-bearing (it keeps every agent prompt style-neutral and testable). This is within the active **outward-turn** workstream (ROADMAP), a production unblock, not a new workstream.

## Where we are (verify against main)

- **The registry module + `primal-sketch-grit` register are BUILT + MERGED to main.** `pipeline/registers.py` is now the canonical closed vocabulary (7 registers): one frozen `RegisterSpec` per register (clauses + `generation_model`/`final_model` + neutrality markers + stub keywords + `reference_images`). A **nonempty unknown register raises `UnknownRegisterError`** (empty still defaults to `pencil-test-colored`). All five+ touch-points read from it; the six pre-registry registers are pinned byte-identical by `tests/test_register_characterization.py`; completeness by `tests/test_register_registry.py`; the neutrality test reads the vocabulary FROM the registry. Both frozen md5 guards held.
- **The doctrine's "step 1 = criteria.py" was WRONG against main** — corrected in `docs/architecture/prompt-style-neutrality-doctrine.md` to point at `pipeline/registers.py` (the vocabulary is NOT in `criteria.py`). The extension pattern is a five-step drill (research → `RegisterSpec` → Cy `## What good looks like` block → template comment → suite refuses to pass until complete).
- **The GRANDMASTER go/no-go spike RAN (2026-07-04) and RESOLVED.** NB2 **NO-GO** for `primal-sketch-grit` — it renders Primal-*lite* / polished, not the raw retained-hand-mark grit, and it **cannot edit** into the style. Sean tested the same prompts across four engines (ChatGPT Image 2 / gpt-image, NB Pro, NB2): **ChatGPT Image 2 was best by far.** It's a **model limit, not a style limit.** `briefs/2026-07-02-grandmaster/go-no-go.md` is resolved to **transport-escalated = gpt-image**; the real remaining GRANDMASTER gate is a **gpt-image across-edit identity validation** (Cy's Bible is an edit pipeline; gpt-image's across-edit identity hold is unproven).
- **A backlog doc captures everything surfaced:** `docs/active/2026-07-04-register-backlog-and-transport-findings.md` — the per-register transport rule, two new candidate registers, the 90s-nicktoon "research first" note, and the register-family trigger.
- **UNCOMMITTED on the main working tree** (commit these FIRST, see below): the go-no-go.md resolution, the backlog doc, this continuation prompt, and the spike frames at `registers/primal-sketch-grit/refs/spike-2026-07-04/` (A-register-verbatim, B-grit-amplified, C-route-c-pencil). Sean's own art-viz frames (pose-1/2/3) are in the WORKTREE at `.claude/worktrees/register-registry-pilot/registers/primal-sketch-grit/refs/`.

## How we work (mirror this process)

- **`superpowers:brainstorming` is the hard gate** for any design/planning — explore context, ask ONE question at a time, propose approaches with a recommendation, present the design in sections with approval after each, THEN write the doc.
- **Converged planning:** draft our own plan → get **Codex's independent plan** (`/codex:rescue --background "..."`, then poll `codex-companion.mjs status <job>` / `result <job>`, reconcile divergences into the doc) → **red-team the converged doc** (a second `/codex:rescue --background` adversarial pass; fold surviving findings; expect BOTH over-build and under-build attacks; verify every claim against main). **Codex CLI gotcha:** keep the tokens `-m`, any `--flag`, and `<angle-brackets>` OUT of the prompt body (the companion misreads them) — spell them out.
- **Builds:** Fable 5, in an **isolated git worktree branched from LOCAL main**, **TDD** (red → verify-red → green → verify-green), **credential-free / stub-green** (suite stays green with no keys and NO spend; no live model/MCP call in tests), `superpowers:verification-before-completion` before any "done," and **stop at the first green checkpoint for Sean's review.** End Fable kickoffs by pointing at the plan doc rather than re-enumerating (Fable 5 does well with intent + a spec pointer).
- **Costed spikes:** Sean's eye is the sole arbiter (Engine Truth — "if it reads as the register in its medium, it ships"); **no LLM aesthetic judge.** Sean tests outputs across engines himself (ChatGPT web app + Flow web app) and picks the preferred look.
- **Guards:** two frozen md5 files must NOT move — `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4` and `pipeline/agents/prompts/sean-screenwriting-voice.md` = `945af824fa53b948a18ac6bf206d67ef`. Subscription billing only, never `ANTHROPIC_API_KEY` (GEMINI_API_KEY for NB2 image gen is fine). Fleet-ops for costed runs. pytest per-directory from repo root.

## Sean's decisions this session (the 3 forks — act on these)

1. **The `primal-sketch-grit.generation_model` change → BATCH into the next Fable build** (don't do it standalone). Set it off NB2 to the gpt-image id, **pinning the exact model id against the `openai-image-gen` skill / OpenAI API**, TDD; update `tests/test_primal_sketch_grit.py` + `registers/primal-sketch-grit/research.md` §4. A gpt-image id with no wired runner should fail loud at generation (correct — never silently fall back to NB2).
2. **The `90s-nicktoon-grossout` (Ren & Stimpy) look-spike → YES, and it comes BEFORE authoring register #2.** Sean wants to **research the look first, then generate look-spike images, and test the outputs himself in the ChatGPT web app + the Flow web app to pick the preferred look** — exactly the Primal process. Only after Sean likes a look do we author register #2 via the doctrine drill. (The `warm-storybook-pencil` candidate — see the backlog §2 — is a possible alternative if the grossout look disappoints.)
3. **Commit the uncommitted docs → do it in THIS fresh session as the FIRST action** (branch from main, not main directly; add a CHANGELOG entry).

## Immediate next actions (ordered)

1. **Commit the uncommitted work.** Branch from local main; commit the go-no-go.md resolution, the backlog doc, this continuation prompt, and the spike frames; add a dated CHANGELOG entry (what changed + why). Open a PR or merge per Sean's preference.
2. **Deep-research the `90s-nicktoon-grossout` (Ren & Stimpy) look** — per the research-brief template in the plan (`docs/active/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md` §2a) WITH its depth requirements (frame-by-frame still analysis, staging grammar, the line/wet-edge logic, negative controls vs Rugrats, the genericization rule). Grounded, not surface pastiche. The consumer + its craft bible are in `briefs/2026-07-02-ai-guru-pilot/concept.md` (§style bible).
3. **Produce the look-spike.** Give Sean Flow-ready + ChatGPT-ready prompts in the corrected `90s-nicktoon-grossout` vocabulary (genericized, attribute-only, no named source in production prompts), and/or run an NB2 spike — so Sean can test across the ChatGPT and Flow web apps and pick the look. Record the transport verdict (which engine renders it).
4. **On Sean's pick →** author register #2 via the drill (batching the primal `generation_model` change), OR pivot to `warm-storybook-pencil` if that's what Sean prefers for ai-guru.

## Deferred / gated (don't do now; named so they're not lost)

- **gpt-image transport wiring + across-edit identity validation** — gated on Sean actually building GRANDMASTER. Alt path: Sean hand-authors GRANDMASTER's key plates in ChatGPT Image 2 and ingests them as Bible anchors (like the mascot's colored keys), sidestepping the transport build.
- **`samurai-jack-s5` register** — a strong candidate (research: `docs/research/samurai-jack-season-5-art-style-description.md`; example: `images/samuria-first-pose-chatgpt.png`), now GRANDMASTER's **revised fallback** (over pencil-test Route C — same samurai world, gpt-image-renderable). Author via the drill when Sean greenlights; that authoring session **revisits the register-family question** (two Tartakovsky registers = the ≥2 trigger for optional `family: tartakovsky` metadata + a possible `tartakovsky` skill — held until there's real shared structure to justify it, not just the count).
- **`warm-storybook-pencil` candidate** — the Route-C spike prompt Sean liked (backlog §2), kept for a future project.

## Read first (source of truth)

- `docs/active/2026-07-04-register-backlog-and-transport-findings.md` — the immediate state + backlog + pending actions.
- `docs/active/2026-07-03-animation-vocabulary-expansion-execution-CONVERGED.md` — the plan (extension pattern §1, research agenda §2a, fold/family/transport §3, TDD tasks §5).
- `briefs/2026-07-02-grandmaster/go-no-go.md` — the resolved go/no-go + the gpt-image edit-identity gate.
- `pipeline/registers.py` + `registers/primal-sketch-grit/research.md` — the registry + the model for how a register is researched/authored.
- `docs/architecture/prompt-style-neutrality-doctrine.md` — the doctrine (corrected).
- `briefs/2026-07-02-ai-guru-pilot/concept.md` — the `90s-nicktoon-grossout` consumer + craft bible.
- `ROADMAP.md` — the anti-drift contract.
- `docs/research/Fable-5-prompting-best-practices-anthropic.md` — for writing the Fable build kickoff.

When you have enough to act, act — commit first, then start the 90s-nicktoon research. Ask Sean only where the evidence leaves a genuine fork you can't resolve.
