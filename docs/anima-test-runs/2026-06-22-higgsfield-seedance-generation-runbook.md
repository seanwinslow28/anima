# Higgsfield Seedance Generation Runbook

> **Worked example:** the 2026-06-22 Act 2 pencil-test pass (10 Seedance clips, 147 credits, $0 of it
> from API key — Higgsfield subscription credits). This doc is a **reusable playbook**: read it before
> running a Seedance generation pass for Act 1, or any future piece, through the Higgsfield CLI.

**Audience:** a future Claude Code session that has been asked to "generate / re-render shots with
Seedance." **Operating model:** Claude Code runs every command; the human (Sean) makes every taste
call. Seedance *finds the motion*; the locked anchor frames *protect the aesthetic*.

---

## 0. TL;DR

1. Ensure the `higgsfield` CLI is installed + authenticated (§2). The human runs `higgsfield auth login`.
2. For each shot: `higgsfield generate create seedance_2_0 --start-image A --end-image B --prompt "$(cat p.txt)" --mode fast --resolution 720p --duration N --generate_audio false --aspect_ratio 16:9 --wait` → prints a URL (§3).
3. `curl` the URL down, extract frames at 2fps, build a contact sheet, **read identity + aesthetic from stills**, then **the human watches the .mp4** for motion (Engine Truth). Work in **small batches** (§4).
4. Assemble a rough cut by normalizing + concatenating clips, with placeholder holds (§5).
5. Cost is **real** — Fast 720p ≈ **3.5 credits/sec** (§7). The "unlimited Fast/Mini" web perk does **not**
   apply to the metered CLI/API.

## 1. When to use this — and the philosophy

This is the **manual / exploratory** Seedance path via the Higgsfield CLI (distinct from anima's
in-pipeline Motion phase, which targets fal.ai Seedance — see `docs/architecture/pipeline-architecture-v1.md`).
Use it to interpolate motion **between two locked anchor frames** (start + end) in the pencil-test style.

**Pipeline philosophy (inherited):** *Seedance generates fluid motion between anchors; the anchors are
the aesthetic contract.* Output frames are reference-quality; the locked NB2 anchors carry identity and
the pencil-on-cream look. If Fast holds identity + aesthetic on a shot, ship it; if not, escalate tier
or fall back (§6). **Engine Truth:** if the loop plays smoothly and the character is recognizably itself
in pencil-test style, it ships — the human's eye on the *playing* clip is the final arbiter, not the stills.

## 2. Prerequisites

**Install the CLI (sudo-free).** Only documented install is a pipe-to-shell; install to `~/.local`
(already on PATH on this machine) to avoid a sudo prompt:

```bash
curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh -s -- --prefix=$HOME/.local
command -v higgsfield   # → ~/.local/bin/higgsfield (v0.2.3 as of 2026-06-22)
```

The installer fetches a prebuilt binary from GitHub releases and strips the macOS quarantine bit — it's
a third-party closed binary (Snyk flags it "Critical" because it can't introspect a binary). Read
`install.sh` before running if unsure.

**Authenticate (human-run, interactive).** Claude Code CANNOT run this — it's an OAuth/browser flow that
hangs a non-interactive shell. Ask Sean to run it in his terminal (`! higgsfield auth login`), then:

```bash
higgsfield account status   # → "<email> — ultra plan, NNNN credits"
```

**Credits are real.** The ultra plan shows a credit balance; Seedance jobs **spend credits** (§7). The
"unlimited Seedance Fast/Mini" advertised on the web UI does **not** reflect the metered CLI/API — budget
in credits, not "free."

## 3. The generation procedure (per shot)

**Discover params once** (model schema is the source of truth):

```bash
higgsfield model get seedance_2_0 --json    # params: mode(std|fast), resolution, duration, generate_audio, aspect_ratio, ...
higgsfield generate cost seedance_2_0 --mode fast --resolution 720p --duration 4 --prompt x   # read-only cost check
```

**Write each prompt to a file** (avoids shell-quoting hell — pencil-test prompts contain apostrophes,
inner double-quotes like `"c:\>_ hello"`, and backslashes):

```bash
# prompts/<SHOT>.txt — the verbatim shot-list draft prompt (~60–95 words, action-focused)
```

**Generate** (start+end-frame interpolation; CLI auto-uploads the local PNGs; `--wait` blocks and prints
the result URL):

```bash
higgsfield generate create seedance_2_0 \
  --start-image <path/to/start_anchor.png> \
  --end-image   <path/to/end_anchor.png> \
  --prompt "$(cat prompts/<SHOT>.txt)" \
  --mode fast --resolution 720p --duration <N> --generate_audio false --aspect_ratio 16:9 \
  --wait --wait-timeout 9m
```

Parameter notes (all learned on the Act 2 run):
- **`--mode fast`** is "Seedance Fast" (the cheap, production-default tier). `std` is ~1.6× the cost.
- **`--duration` minimum is 4** — a 3s request errors `duration: Input should be greater than or equal
  to 4` (and costs nothing). Shots creatively spec'd at 3s **generate at 4s and trim to 3s in assembly.**
- **`--generate_audio false`** (underscore!). The hyphen form `--generate-audio` errors `Unknown params`.
  Pencil animation is silent; leaving audio on generates an unwanted track.
- **`--resolution 720p`** is the pencil-test default. 1080p/4k exist but cost more and aren't needed.
- **`--aspect_ratio 16:9`** — in start+end mode the output inherits the start frame's aspect; pass it
  anyway for clarity. Anchors are 16:9.
- **`--wait-timeout 9m`** — Fast 4–5s clips return in ~1–3 min; 9m is safe headroom.
- Set the Bash tool timeout to its max (600000 ms) for each `--wait` call; run them **one per Bash call**
  so a slow job can't time out a whole batch.

## 4. The batch review loop (Engine Truth)

Work in **small batches** (the human reviews each before continuing). For Act 2 the batches were:
hardest-morphs (S0, REV) → walk trio (W1–W3) → terminal pair (T0, T2) → action/close (TR, PM, PB).

Per clip, after the URL returns:

```bash
curl -fsSL "<result_url>" -o <SHOT>.mp4
ffmpeg -loglevel error -i <SHOT>.mp4 -vf fps=2 frames/<SHOT>_%02d.png            # 2fps stills
ffmpeg -loglevel error -framerate 1 -i frames/<SHOT>_%02d.png \
  -vf "scale=480:-1,tile=4x2" <SHOT>_contact.png                                  # contact sheet (4s→4x2, 5s→5x2)
```

**Two-layer review:**
- **Claude reads the stills** — the contact sheet for the whole arc, plus 2–3 full-res mid-morph + landing
  frames to judge **identity hold** (does the face melt mid-transition?) and **aesthetic** (pencil-on-cream,
  construction lines, paper grain). Report PASS/concern per the shot-list verification gates.
- **The human watches the .mp4** (`open <SHOT>.mp4`) — this is Engine Truth. Stills can't show motion
  quality (smooth walk-cycle vs. floaty slide; morph that reads as animation vs. an AI "smart dissolve").
  Claude cannot watch video; **always hand the motion call to Sean.**

On a failed shot: retry with a refined prompt, or escalate `--mode std`, or use the shot's documented
fallback (hard cut + crossfade, drop to 4s, or split the shot). The shot list pre-ranks risk and lists
per-shot fallbacks.

## 5. Assembling the rough cut

Normalize every segment to identical codec params, then concat with `-c copy`. **zsh needs
`setopt shwordsplit`** for the flag variables to word-split (see §8).

```bash
setopt shwordsplit
SCALE="scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24"
NORM="-c:v libx264 -crf 20 -pix_fmt yuv420p -an"
# each Seedance clip:        ffmpeg -y -i <SHOT>.mp4 -vf "$SCALE" $NORM seg/NN_<SHOT>.mp4
# trim a 4s clip to 3s:      add  -t 3
# placeholder hold from a still:  ffmpeg -y -loop 1 -t <secs> -i <anchor>.png -vf "$SCALE" $NORM seg/NN_hold.mp4
# concat (segments are now identical → stream copy):
printf "file 'NN_xxx.mp4'\n" ... > seg/list.txt
ffmpeg -y -f concat -safe 0 -i seg/list.txt -c copy rough_cut.mp4
```

Hard cuts are just concatenation points (no special handling). Holds that aren't yet built use the
single anchor frame held for its duration. See the Act 2 assembly: `runs/Act-2-Pencil-Test/5_ROUGH_CUT/assembly-map.md`.

## 6. The holds question (deferred decision)

Holds (static beats, terminal blinks, final panorama) can be:
- **FFmpeg static / Ken Burns** — $0, but a dead frame next to lively Seedance shots can feel inert.
- **Seedance "breathing holds"** — image-to-video from a single start frame with a "locked camera,
  subtle breathing, minimal motion" prompt; adds life. Good for short reaction/breath beats.
- **Avoid Seedance on long static cream-paper fields** (e.g. a 5s panorama) — texture-crawl/shimmer risk;
  prefer a Ken Burns pan.

This was left open on the Act 2 run — decide per piece.

## 7. Costs (real numbers from the Act 2 run)

Seedance 2.0 **Fast 720p ≈ 3.5 credits/sec** (Std 720p ≈ 4.5/sec). Read-only `higgsfield generate cost …`
before a batch to confirm.

| Shot(s) | Dur | Credits |
|---|---|---|
| W1, W2, W3, S0, T0, T2, TR, PM (each) | 4s | 14 |
| REV, PB (each) | 5s | 17.5 |
| **All 10 Act 2 clips** | | **147** |

A full ~10-shot act is well under 150 credits on Fast — trivial against an ultra plan's balance, but it
*is* metered. Rejected (too-short) requests cost 0.

## 8. Gotchas & lessons (all hit on the Act 2 run)

- **zsh does not word-split unquoted variables** (the default shell here). `$NORM="-c:v libx264 …"`
  passed unquoted reaches ffmpeg as ONE argument → "At least one output file must be specified." Fix:
  `setopt shwordsplit` at the top of the script. Same root cause broke a `for pair in "W1 $url"` loop
  (the URL didn't split). Prefer explicit per-item commands or `setopt shwordsplit`.
- **Prompts with inner quotes/backslashes** (`"c:\>_ hello, sean..."`) break `--prompt "…"`. Write the
  prompt to a file and pass `--prompt "$(cat file)"`.
- **4s minimum** on Higgsfield Seedance (§3). Generate 3s-spec shots at 4s, trim in assembly.
- **`--generate_audio false`** (underscore), not `--generate-audio`.
- **"Unlimited" ≠ free via CLI.** The web-UI Fast/Mini perk is not the metered API; credits are spent.
- **`higgsfield auth login` is human-only** (interactive). Claude can install the CLI and run everything
  else, but not the OAuth login.
- **Background tasks reset CWD to the primary checkout** (a known fleet-ops seam). If running inside a
  git worktree, `cd /abs/path/worktree && …` explicitly in every backgrounded command.
- **Claude can't watch video.** Always extract stills for Claude's read AND hand the .mp4 to the human
  for the motion verdict.

## 9. Project-folder convention (how the output was organized)

Each act gets a self-contained, **gitignored / local-only** project folder under `runs/` (Sean's
preference), built by **non-destructive copy** (never move tracked/referenced sources):

```
runs/Act-N-Pencil-Test/
├── README.md                  # premise, shot/beat map, what's done/missing, where originals live
├── 1_STORYBOARD_AND_PLAN/     # the narrative + shot plan docs
├── 2_… (anchors / keyframes)  # the input frames
├── 3_… (prompts)              # the generation prompts
├── 4_… (clips / shipped loop) # the outputs
├── 5_… (rough cut / evidence)
└── 6_… (prior run / museum exhibit)
```

Canonical tracked sources (docs, `prompts/act2/`, `runs/act2-exploration/`, museum) stay where they are
and are referenced from the README's "Where the originals live" section. Plans for these migrations:
`docs/superpowers/plans/2026-06-22-act-{1,2}-pencil-test-project-folder.md`.

## 10. Applying this to Act 1 (concrete next use)

Act 1 is the shipped keyframe loop (`runs/Act-1-Pencil-Test/`). To give it the same Seedance
motion-enhancement pass:
- **Anchors = the approved Act 1 keyframes** in `runs/Act-1-Pencil-Test/2_KEYFRAMES_AND_INBETWEENS/approved/`
  (`PT_A1_F01_key.png` … `PT_A1_F40_key.png`).
- **Chains to interpolate** (start→end): F01→F06, F06→F10, F13→F18, F31→F36, F36→F40 (the documented
  Act 1 Seedance clips — see `runs/Act-1-Pencil-Test/1_STORYBOARD_AND_PLAN/act1-seedance-integration-plan.md`
  and `…-v2-execution-plan.md`).
- **Prompts** already drafted in those integration docs and in the superseded production plan's Act 1
  section. Keep them style-locked ("hand-drawn pencil on cream paper … fixed camera … stylus in right
  hand … no digital effects"). Note: in Act 1 the **stylus stays in Sean's right hand** (unlike Act 2,
  where that rule is dropped).
- Run them through §3–§5 exactly as Act 2; review in small batches; the human's eye decides whether the
  Seedance motion beats the existing NB2 in-betweens (it may not — Act 1 already shipped, so this is
  enhancement, not rescue).

## 11. References

- **Act 2 shot list (source of truth):** `runs/Act-2-Pencil-Test/1_STORYBOARD_AND_PLAN/act2-shot-list.md`
  (canonical: `docs/pencil-test/act2-seedance-shot-list.md`).
- **Act 2 session log (per-batch, with verdicts):** `runs/Act-2-Pencil-Test/5_ROUGH_CUT/seedance-session-notes.md`.
- **Seedance prompt template (v4):** `prompts/seedance-template-v4.md`; research: `docs/research/seedance-research-findings.md`.
- **Fleet ops discipline (costed runs):** `docs/architecture/fleet-ops-protocol.md`.
- **The two project folders:** `runs/Act-1-Pencil-Test/`, `runs/Act-2-Pencil-Test/`.
