# {PROJECT TITLE} — Project Manual  *(template)*

> **Template usage:** copy this file to `briefs/{project-dir}/CLAUDE.md` when a new
> animation project starts (pair it with `project-STORYBOARD-md-template.md`). It
> auto-loads for any session working in that tree. Fill every `{…}`; delete rows that
> don't apply. **Worked example:** `briefs/2026-07-02-grandmaster/CLAUDE.md`.
> Design rule: this is the **orientation layer** — one-liners + pointers. It never
> forks the record: decisions live in the project's `concept.md` Decision Record;
> production state lives in `STORYBOARD.md`. If this file and concept.md disagree,
> concept.md wins — fix this file.

## The piece in one breath

{Logline + shape in 3–5 sentences: who, want, turn, payoff, runtime target.}

## Read first (in order)

1. `concept.md` — story SoT + the Decision Record (every lock + why)
2. `STORYBOARD.md` — per-beat production tracker
3. {writers-room / research docs for this piece}
4. {the piece's prompt pack(s) — the proven prompt format}
5. `registers/{register}/research.md` — the register truth

## The law (one-liners; full text lives in the Decision Record)

- **Register `{register}`, piece-locked:** {one-line look description + transport}.
- **Anti-drift:** NO CHAIN-EDITING — fresh, or ONE edit off a clean source; feed a
  `KEEPER` plate as an art-style-only reference on fresh environment gens; discard
  drifted plates, never re-edit them.
- **Comedy/tone engine:** {the piece's one-line law}.
- **Setting law:** {region/period cues to name + cues to negate}.
- **Light law:** {default light; what's reserved for hero beats}.
- **Wardrobe:** {constant signifier that never changes; per-context outfits + where
  the turnarounds live} (art-department §8.5 wardrobe pass).
- **Multi-angle locations (DR #20, repo-wide):** key location = master + reverse +
  per-mark angles + placement map.
- **Motion start-pose (repo-wide):** Seedance-bound stills = the STARTING pose.
- **Seedance 2.0 (repo-wide):** lead with the flat-2D-cel "animated on twos" anchor
  (no negation); generate longer than the hold + trim; seconds upfront for held beats.
- **Generation is path-based:** cite refs BY PATH + name them; never re-describe a
  designed character/location; composites inherit the location's light; no text; 16:9.
- {Any piece-specific non-negotiables — e.g. weapon rules, forbidden imagery.}

## Spend discipline

$0 unless Sean opens a budget. Subscription credits / Sean's own generation pass —
**never `ANTHROPIC_API_KEY`**. Announce every spend against a declared ceiling.
Sean owns taste and every lock; agents propose.

## Where things live

| What | Where |
|---|---|
| Story + decisions (SoT) | `concept.md` |
| Production tracker | `STORYBOARD.md` |
| Art-Dept bundle | `runs/{artdept-run}/bundle/` |
| Prompt packs + generated stills | `runs/{…}` |
| Motion clips | `runs/{…}/motion/` |
| Character anchors | `{…}` |
| Register research | `registers/{register}/` |

## Session maintenance

- **STORYBOARD.md on every generation/approval** — the tracker is only useful if true.
- **CHANGELOG.md (repo root) on every change** — per the repo-wide convention.
- **New creative decisions → concept.md Decision Record** (numbered, dated, with why),
  then reflect the one-liner here if it's law.
