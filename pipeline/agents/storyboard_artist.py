"""anima — Bea the storyboard artist. Phase 3b (Storyboard / board half).

Bea runs once per piece, after `script approve`. She reads Sam's approved
beats.json + the Studio Brief and *proposes* the board: a studio-voice
storyboard.md and a draft shots.yaml (the machine input the GENERATE stage
consumes — pipeline/orchestration/shots.py). Phase 3 is "mostly human-authored;
agents assist, they don't pick beats" (architecture lock + PHILOSOPHY): Bea
proposes, Sean curates and decides at the `storyboard approve` gate. The
shots.yaml is born unlocked and never auto-runs. There is no critic checkpoint
at Phase-3 exit.

Single Sonnet 4.6 authoring call, then a free deterministic validation pass —
NOT a second LLM call (the eval handbook bars LLM aesthetic judges on creative
quality; the composition call is the human gate). The pass is coverage +
script↔board-conflict (the named red classes): every beat is boarded by >=1
shot, no shot points at a missing beat, and every shot keeps the full focal cast
of its beat (beat.cast subset of shot.cast). On failure, one re-roll with the
error threaded back into the prompt (Cy's reject-reason pattern).

Emits two artifacts into the brief dir:
  - storyboard.md  (studio-voice board — human-readable)
  - shots.yaml     (draft machine artifact; born unlocked; `storyboard approve`
                    flips its top-level `locked` flag)
"""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import ClassVar

import yaml

from pipeline.agents import AgentContext, AgentResult, CostEstimate, register_node
# Reuse Maya's battle-tested envelope hardening (brace-balanced scan tolerating
# a persona preamble — "Bea here — ..." — and ```json fences / nested braces).
from pipeline.agents.planner import _parse_json_envelope
from pipeline.agents.sdk_runners import STUB_MODEL, SDKResponse, invoke_sonnet_text
from pipeline.orchestration.beats import BeatSheet, load_beats
from pipeline.orchestration.cast import derive_cast
from pipeline.orchestration.shots import ShotList, load_shots

PROMPTS_DIR = Path(__file__).parent / "prompts"
ANIMA_PREAMBLE_FILE = PROMPTS_DIR / "anima-standing-context.md"
BEA_ADDENDUM_FILE = PROMPTS_DIR / "bea-storyboard-context.md"
# The full vendored voice instrument (verbatim, shared with Sam — stays byte-stable).
VOICE_FILE = PROMPTS_DIR / "sean-screenwriting-voice.md"

# Per-call timeout for Bea's Sonnet authoring call. Mirrors Maya/Sam's lesson:
# live authoring runs minutes, not the sdk_runners 120s default (a silent crash).
_BEA_CALL_TIMEOUT_S = int(os.environ.get("BEA_CALL_TIMEOUT_S", "1200"))

# The fixed pencil-test register clause block every per-shot prompt must end in.
# Matches the shipped Spark shots.yaml prompt tails verbatim — the medium is
# fixed; only the voice inside it is Bea's.
_REGISTER_CLAUSE = (
    "Pencil test animation key drawing on cream paper with visible paper grain; "
    "warm graphite line, light construction lines and sparse cross-hatching for "
    "shading; hand-drawn rough animation, soft colored-pencil fills in the "
    "pencil-test-colored register. 16:9 widescreen, fixed camera, locked framing. "
    "NOT a clean digital, anime, or 3D render."
)

_STUB_MARKER = "STUB FALLBACK"


@register_node("storyboard_artist")
class StoryboardArtistNode:
    """Bea — storyboard artist. Phase 3b."""

    name: ClassVar[str] = "storyboard_artist"
    inputs: ClassVar[dict[str, type]] = {"brief_dir": str}
    outputs: ClassVar[dict[str, type]] = {"storyboard_path": str, "shots_path": str}
    cites_criteria: ClassVar[list[str]] = []

    def cost_estimate(self, ctx: AgentContext) -> CostEstimate:
        # Single Sonnet authoring call, subscription-absorbed via Sean's Pro plan.
        return CostEstimate(usd=0.0, latency_s=120.0, confidence=0.85)

    def run(self, ctx: AgentContext) -> AgentResult:
        brief_dir = Path(ctx.inputs["brief_dir"])
        studio_brief_path = brief_dir / "00_studio_brief.md"
        if not studio_brief_path.exists():
            raise FileNotFoundError(
                f"Studio Brief not found at {studio_brief_path}. "
                f"Run `python -m pipeline.cli plan init --target {brief_dir}` "
                f"and author the brief first."
            )
        beats_path = brief_dir / "beats.json"
        if not beats_path.exists():
            raise FileNotFoundError(
                f"Sam's beats.json not found at {beats_path}. Run Sam "
                f"(`python scripts/author_script.py {brief_dir} ...`) and "
                f"`python -m pipeline.cli script approve` first."
            )
        studio_brief = studio_brief_path.read_text(encoding="utf-8")
        plan_md_path = brief_dir / "plan.md"
        plan_md = plan_md_path.read_text(encoding="utf-8") if plan_md_path.exists() else ""

        # known_namespaces is derived exactly as the GENERATE stage derives it for
        # load_shots (cast.derive_cast → ir_namespace set) so beats and shots share
        # one namespace vocabulary and Bea's beat → shot cast carries unchanged.
        known_namespaces = {
            m["ir_namespace"] for m in derive_cast(ctx.manifest) if m["ir_namespace"]
        }

        # Sam's approved beat sheet — the spine Bea boards. Validated by load_beats.
        sheet = load_beats(beats_path, known_namespaces=known_namespaces)

        # The credential-free stub emits one shot per real beat (so coverage /
        # conflict pass by construction for ANY beats.json), with the STUB marker.
        stub_fn = _make_bea_stub(sheet)

        brief_dir.mkdir(parents=True, exist_ok=True)
        storyboard_path = brief_dir / "storyboard.md"
        shots_path = brief_dir / "shots.yaml"

        # --- Single Sonnet authoring pass (+ at most one re-roll on a structural
        # failure, with the error threaded back — Cy's reject-reason pattern) ---
        reject_reason = ""
        last_err: ValueError | None = None
        resp: SDKResponse | None = None
        for _ in range(2):
            prompt = self._build_prompt(
                studio_brief, plan_md, _beats_payload(sheet), known_namespaces,
                reject_reason=reject_reason,
            )
            resp = asyncio.run(
                invoke_sonnet_text(
                    prompt=prompt, timeout_s=_BEA_CALL_TIMEOUT_S, stub_fn=stub_fn
                )
            )
            if not resp.ok:
                raise RuntimeError(f"Bea's Sonnet authoring call failed: {resp.error}")
            parsed = self._parse(resp.text)
            _atomic_write(storyboard_path, parsed["storyboard_md"])
            _atomic_write(
                shots_path,
                yaml.safe_dump(parsed["shots_yaml"], sort_keys=False, allow_unicode=True),
            )

            try:
                shot_list = load_shots(shots_path, known_namespaces=known_namespaces)
                storyboard_validate(sheet, shot_list, known_namespaces=known_namespaces)
                last_err = None
                break
            except ValueError as e:
                last_err = e
                reject_reason = str(e)
        if last_err is not None:
            raise last_err

        notes = (
            f"bea@phase_3b shots={len(shot_list.frames)} beats={len(sheet.beats)} "
            f"stub={resp.stub_fallback} model={resp.model}"
        )
        return AgentResult(
            outputs={"storyboard_path": str(storyboard_path), "shots_path": str(shots_path)},
            tier=ctx.tier,
            cites_criteria=[],
            notes=notes,
        )

    # ----- prompt -----

    def _build_prompt(
        self,
        studio_brief: str,
        plan_md: str,
        beats_payload: dict,
        known_namespaces: set[str],
        *,
        reject_reason: str = "",
    ) -> str:
        return "\n\n".join([
            _load(ANIMA_PREAMBLE_FILE),
            _load(BEA_ADDENDUM_FILE),
            _load(VOICE_FILE),
            self._per_invocation_brief(
                studio_brief, plan_md, beats_payload, known_namespaces, reject_reason
            ),
        ])

    def _per_invocation_brief(
        self,
        studio_brief: str,
        plan_md: str,
        beats_payload: dict,
        known_namespaces: set[str],
        reject_reason: str,
    ) -> str:
        has_plan = bool(plan_md.strip())
        plan_section = f"### Maya's plan.md\n\n{plan_md}\n\n" if has_plan else ""
        retry_section = (
            "### Re-roll — fix this structural failure\n\n"
            f"Your previous draft failed the deterministic check:\n\n    {reject_reason}\n\n"
            "Fix exactly that and re-emit both artifacts.\n\n"
            if reject_reason
            else ""
        )
        return (
            "## Board the beats\n\n"
            + retry_section
            + "Read Sam's approved beat sheet"
            + (" and Maya's plan" if has_plan else "")
            + " and the Studio Brief. Author a studio-voice `storyboard.md` board "
            "AND a draft `shots.yaml`. You PROPOSE — Sean curates and locks at the "
            "gate; the shots.yaml is born unlocked. Write in Sean's voice (the "
            "instrument above + the Action-Line Prose Bank are the load-bearing "
            "references — board from the exemplars; do not distill them).\n\n"
            "Board EVERY beat: each beat gets >=1 shot whose `beat_id` is that "
            "beat's id (coverage). Each shot's `cast` must include every IR "
            "namespace the beat carries, and may add others in frame "
            f"(use only these namespaces: {sorted(known_namespaces)}); never drop a "
            "character the beat is about. Shot `id`s strictly ascending from 1.\n\n"
            "Every per-shot `prompt` is prose-action and MUST end in this exact "
            "pencil-test register clause block:\n\n"
            f"    {_REGISTER_CLAUSE}\n\n"
            "Emit ONE JSON object with exactly two keys, wrapped in a ```json "
            "code fence:\n\n"
            "```json\n"
            "{\n"
            '  "storyboard_md": "<studio-voice board, clean markdown>",\n'
            '  "shots_yaml": {\n'
            '    "slug": "<short-slug>",\n'
            '    "frames": [\n'
            '      {"id": 1, "beat_id": 1, "cast": ["..."], "beat": "<what the shot shows>", '
            '"prompt": "<prose-action ... ' + _REGISTER_CLAUSE[:40] + '...>", '
            '"chain_anchors": ["..."], "hold": 2}\n'
            "    ]\n"
            "  }\n"
            "}\n"
            "```\n\n"
            f"### Sam's beat sheet (beats.json)\n\n```json\n{json.dumps(beats_payload, indent=2)}\n```\n\n"
            f"### Studio Brief\n\n{studio_brief}\n\n"
            f"{plan_section}"
        )

    def _parse(self, text: str) -> dict:
        payload = _parse_json_envelope(text)
        for key in ("storyboard_md", "shots_yaml"):
            if key not in payload:
                raise ValueError(
                    f"Bea response missing required key {key!r}. Got keys: {sorted(payload)}"
                )
        if not isinstance(payload["shots_yaml"], dict):
            raise ValueError(
                f"Bea response 'shots_yaml' must be a JSON object (the shot list), "
                f"got {type(payload['shots_yaml']).__name__}"
            )
        return payload


def storyboard_validate(
    sheet: BeatSheet, shot_list: ShotList, *, known_namespaces: set[str]
) -> None:
    """Deterministic board-vs-script pass (coverage + conflict).

    Raises ValueError on:
      - coverage gap: a beat that no shot boards (no shot with beat_id == beat.id);
      - orphan shot: a shot whose beat_id points at no beat in the sheet;
      - script↔board conflict: a shot that drops a character its beat carries
        (beat.cast must be a subset of shot.cast — the board may add characters in
        frame, e.g. a fixed-camera two-shot, but may never drop a scripted one).

    load_shots has already enforced the shots.yaml schema (ascending ids,
    cast ⊆ known_namespaces, chain_anchors ⊆ cast, non-empty beat/prompt), so this
    is the relational layer on top. It does NOT judge composition (the human gate).
    `known_namespaces` backstops the cast bound for callers that pass a ShotList
    not freshly loaded against it (defense in depth).
    """
    beat_ids = {b.id for b in sheet.beats}

    # orphan shots
    for s in shot_list.frames:
        if s.beat_id is not None and s.beat_id not in beat_ids:
            raise ValueError(
                f"orphan shot {s.id}: beat_id {s.beat_id} is not a beat in the sheet "
                f"{sorted(beat_ids)}"
            )

    # coverage — every beat boarded by >=1 shot
    covered = {s.beat_id for s in shot_list.frames if s.beat_id is not None}
    missing = sorted(beat_ids - covered)
    if missing:
        raise ValueError(
            f"coverage gap: beat(s) {missing} are boarded by no shot "
            f"(no frame carries their beat_id) — every beat needs a shot"
        )

    # cast consistency (beat.cast ⊆ shot.cast) + defensive namespace bound
    for s in shot_list.frames:
        bad_ns = [ns for ns in s.cast if ns not in known_namespaces]
        if bad_ns:
            raise ValueError(
                f"shot {s.id}: cast names unknown IR namespace(s) {bad_ns} "
                f"(known: {sorted(known_namespaces)})"
            )
        if s.beat_id is None:
            continue
        beat = sheet.by_id(s.beat_id)
        dropped = sorted(set(beat.cast) - set(s.cast))
        if dropped:
            raise ValueError(
                f"script↔board conflict: shot {s.id} (beat {s.beat_id}) drops "
                f"character(s) {dropped} that beat '{beat.title}' carries "
                f"(beat cast {sorted(beat.cast)}, shot cast {sorted(s.cast)})"
            )


def _beats_payload(sheet: BeatSheet) -> dict:
    """The beat sheet as a plain dict for the prompt (one source of truth)."""
    return {
        "slug": sheet.slug,
        "logline": sheet.logline,
        "beats": [
            {
                "id": b.id,
                "title": b.title,
                "intent": b.intent,
                "emotional_beat": b.emotional_beat,
                "cast": list(b.cast),
                **({"feel": b.feel} if b.feel else {}),
                **({"notes": b.notes} if b.notes else {}),
            }
            for b in sheet.beats
        ],
    }


def _load(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def _atomic_write(path: Path, content: str) -> None:
    """temp-then-rename atomic write. Mirrors the planner.py / patch_stager idiom."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def _make_bea_stub(sheet: BeatSheet):
    """Build Bea's deterministic stub from the real beat sheet.

    Emits one shot per beat (beat_id-linked, cast = the beat's cast, so coverage /
    orphan / conflict all pass by construction for ANY beats.json), each prompt
    ending in the register clause block. Carries the STUB FALLBACK marker in the
    storyboard so author_storyboard.py's scan_stub_marker refuses to treat it as a
    real authored board. Proves the whole contract end-to-end with no key.
    """

    def _stub_bea_text(prompt: str) -> SDKResponse:
        frames = []
        lines = []
        for b in sheet.beats:
            cast = list(b.cast)
            frames.append({
                "id": b.id,
                "beat_id": b.id,
                "cast": cast,
                "beat": b.intent or b.title,
                "prompt": f"{b.title}: {b.intent} {_REGISTER_CLAUSE}",
                "chain_anchors": cast[:1],
                "hold": 2,
            })
            lines.append(f"- Beat {b.id} — {b.title}: {b.intent}")
        storyboard_md = (
            "# Storyboard (STUB)\n\n"
            f"{_STUB_MARKER} — Sonnet SDK unavailable. Bea's studio-voice board "
            "would render here. Install claude-agent-sdk or set ANTHROPIC_API_KEY "
            "(and unset ANIMA_FORCE_STUB) for real authoring.\n\n"
            "## Boarded beats\n\n" + "\n".join(lines) + "\n"
        )
        payload = {
            "storyboard_md": storyboard_md,
            "shots_yaml": {"slug": sheet.slug, "frames": frames},
        }
        return SDKResponse(
            model=STUB_MODEL,
            text=json.dumps(payload),
            duration_s=0.0,
            exit_code=0,
            error=None,
            stub_fallback=True,
        )

    return _stub_bea_text
