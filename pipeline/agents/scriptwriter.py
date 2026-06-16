"""anima — Sam the scriptwriter. Phase 3a (Storyboard / script half).

Sam runs once per piece. He reads Maya's plan.md + the Studio Brief and
*proposes* a script: a studio-voice script.md treatment and a structured
beats.json beat sheet (the Sam→Bea contract — pipeline/orchestration/beats.py).
Phase 3 is "mostly human-authored; agents assist, they don't pick beats"
(architecture lock + PHILOSOPHY): Sam proposes, Sean decides at the
`script approve` gate. There is no critic checkpoint at Phase-3 exit.

Single Opus 4.8 authoring call, then a free deterministic structural-validation
pass — NOT a second LLM call. The eval handbook bars LLM aesthetic judges on
creative quality (weak/self-preferring); the taste call is the human gate. The
structural pass is cast-coverage + sanity (Decision #1, 2026-06-15): every
loaded character appears in >=1 beat (the deterministic red failure class), ids
ascending, beat count in a sane band, emotional beats not all identical (arc
presence). It deliberately does NOT parse plan.md prose for "story-point
coverage" — that needs an LLM and v1 bars it.

Emits two artifacts into the brief dir:
  - script.md   (studio-voice treatment — human-readable)
  - beats.json  (machine artifact; carries a top-level `locked` flag that
                 `script approve` flips)
"""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import ClassVar

from pipeline.agents import AgentContext, AgentResult, CostEstimate, register_node
# Reuse Maya's battle-tested envelope hardening (brace-balanced scan tolerating
# a persona preamble — "Sam here — ..." — and ```json fences / nested braces).
from pipeline.agents.planner import _dump_raw, _parse_json_envelope
from pipeline.agents.sdk_runners import STUB_MODEL, SDKResponse, invoke_opus_text
from pipeline.orchestration.beats import BeatSheet, load_beats
from pipeline.orchestration.cast import derive_cast

PROMPTS_DIR = Path(__file__).parent / "prompts"
ANIMA_PREAMBLE_FILE = PROMPTS_DIR / "anima-standing-context.md"
SAM_ADDENDUM_FILE = PROMPTS_DIR / "sam-scriptwriter-context.md"
# The full vendored voice instrument (verbatim from the code-brain
# screenwriting-modes skill). Shared — Bea loads it too when she lands.
VOICE_FILE = PROMPTS_DIR / "sean-screenwriting-voice.md"

# Per-call timeout for Sam's Opus authoring call. Mirrors Maya's lesson
# (MAYA_CALL_TIMEOUT_S): live Opus-4.8 authoring runs minutes, not 120s; the
# sdk_runners 120s default silently times out into an empty-text crash.
_SAM_CALL_TIMEOUT_S = int(os.environ.get("SAM_CALL_TIMEOUT_S", "1200"))

# Deterministic structural-pass bounds (the sane beat-count band).
_MIN_BEATS = 3
_MAX_BEATS = 12


@register_node("scriptwriter")
class ScriptwriterNode:
    """Sam — scriptwriter. Phase 3a."""

    name: ClassVar[str] = "scriptwriter"
    inputs: ClassVar[dict[str, type]] = {"brief_dir": str}
    outputs: ClassVar[dict[str, type]] = {"script_path": str, "beats_path": str}
    cites_criteria: ClassVar[list[str]] = []

    def cost_estimate(self, ctx: AgentContext) -> CostEstimate:
        # Single Opus authoring call, subscription-absorbed via Sean's Pro plan.
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
        studio_brief = studio_brief_path.read_text(encoding="utf-8")
        plan_md_path = brief_dir / "plan.md"
        plan_md = plan_md_path.read_text(encoding="utf-8") if plan_md_path.exists() else ""

        # known_namespaces is derived exactly as the GENERATE stage derives it
        # for load_shots (cast.derive_cast → ir_namespace set) so beats and
        # shots share one namespace vocabulary and Bea's beat → shot cast carries
        # unchanged.
        known_namespaces = {
            m["ir_namespace"] for m in derive_cast(ctx.manifest) if m["ir_namespace"]
        }

        # --- Single Opus authoring pass (stub-backed credential-free) ---
        prompt = self._build_prompt(studio_brief, plan_md, known_namespaces)
        resp = asyncio.run(
            invoke_opus_text(
                prompt=prompt,
                timeout_s=_SAM_CALL_TIMEOUT_S,
                stub_fn=_stub_sam_text,
            )
        )
        if not resp.ok:
            raise RuntimeError(f"Sam's Opus authoring call failed: {resp.error}")
        # Best-effort raw dump BEFORE parsing — mirrors Maya's maya_raw_pass1.txt
        # so a parse failure on a live run still leaves the raw envelope on disk.
        _dump_raw(ctx.run_dir, "sam_raw.txt", resp.text)
        parsed = self._parse(resp.text)
        script_md: str = parsed["script_md"]
        beats_json: dict = parsed["beats_json"]

        # Write artifacts (temp-then-rename atomic, mirrors planner.py).
        brief_dir.mkdir(parents=True, exist_ok=True)
        script_path = brief_dir / "script.md"
        _atomic_write(script_path, script_md)
        beats_path = brief_dir / "beats.json"
        _atomic_write(beats_path, json.dumps(beats_json, indent=2))

        # --- Deterministic structural-validation pass (free — no LLM) ---
        sheet = load_beats(beats_path, known_namespaces=known_namespaces)
        structural_validate(sheet, known_namespaces=known_namespaces)

        notes = (
            f"sam@phase_3a beats={len(sheet.beats)} "
            f"stub={resp.stub_fallback} model={resp.model}"
        )
        return AgentResult(
            outputs={"script_path": str(script_path), "beats_path": str(beats_path)},
            tier=ctx.tier,
            cites_criteria=[],
            notes=notes,
        )

    # ----- prompt -----

    def _build_prompt(self, studio_brief: str, plan_md: str, known_namespaces: set[str]) -> str:
        return "\n\n".join([
            _load(ANIMA_PREAMBLE_FILE),
            _load(SAM_ADDENDUM_FILE),
            _load(VOICE_FILE),
            self._per_invocation_brief(studio_brief, plan_md, known_namespaces),
        ])

    def _per_invocation_brief(
        self, studio_brief: str, plan_md: str, known_namespaces: set[str]
    ) -> str:
        has_plan = bool(plan_md.strip())
        plan_section = f"### Maya's plan.md\n\n{plan_md}\n\n" if has_plan else ""
        return (
            "## Author the script\n\n"
            "Read the Studio Brief"
            + (" and Maya's plan" if has_plan else "")
            + ". Author a studio-voice `script.md` treatment AND a structured beat "
            "sheet. You PROPOSE — Sean decides at the gate; you do not pick the "
            "final beats. Write in Sean's screenwriting voice (the instrument "
            "above is the load-bearing reference — exemplars drive, mechanics "
            "annotate; do not distill it to a checklist).\n\n"
            "Use these exact cast namespaces in each beat's `cast` (a beat may use "
            f"a subset): {sorted(known_namespaces)}. Every loaded character must "
            "appear in at least one beat. ids strictly ascending from 1; aim for "
            "3–12 beats with a real emotional arc (Declare-then-Puncture / "
            "therefore-but — not a flat list).\n\n"
            "Emit ONE JSON object with exactly two keys, wrapped in a ```json "
            "code fence:\n\n"
            "```json\n"
            "{\n"
            '  "script_md": "<studio-voice prose treatment + scene work>",\n'
            '  "beats_json": {\n'
            '    "slug": "<kebab-slug>",\n'
            '    "logline": "<one sentence>",\n'
            '    "beats": [\n'
            '      {"id": 1, "title": "...", "intent": "...", '
            '"emotional_beat": "...", "cast": ["..."], "feel": "...", "notes": "..."}\n'
            "    ]\n"
            "  }\n"
            "}\n"
            "```\n\n"
            f"### Studio Brief\n\n{studio_brief}\n\n"
            f"{plan_section}"
        )

    def _parse(self, text: str) -> dict:
        payload = _parse_json_envelope(text)
        for key in ("script_md", "beats_json"):
            if key not in payload:
                raise ValueError(
                    f"Sam response missing required key {key!r}. Got keys: {sorted(payload)}"
                )
        return payload


def structural_validate(sheet: BeatSheet, *, known_namespaces: set[str]) -> None:
    """Deterministic structural pass (Decision #1: cast-coverage + sanity).

    Raises ValueError on:
      - a loaded character that appears in no beat (the deterministic red class);
      - beat count outside [_MIN_BEATS, _MAX_BEATS];
      - all emotional_beat values identical (no arc presence).

    load_beats has already enforced ascending ids + per-beat non-empty fields +
    cast ⊆ known_namespaces, so this is the layer on top. It does NOT judge
    creative quality (that's the human gate) and does NOT parse plan.md prose.
    """
    n = len(sheet.beats)
    if not (_MIN_BEATS <= n <= _MAX_BEATS):
        raise ValueError(
            f"beat count {n} outside the sane band [{_MIN_BEATS}, {_MAX_BEATS}]"
        )
    covered: set[str] = set()
    for b in sheet.beats:
        covered.update(b.cast)
    missing = sorted(known_namespaces - covered)
    if missing:
        raise ValueError(
            f"cast-coverage gap: loaded character(s) {missing} appear in no beat "
            f"(covered: {sorted(covered)})"
        )
    emotional = {b.emotional_beat.strip().lower() for b in sheet.beats}
    if len(emotional) < 2:
        raise ValueError(
            f"arc-presence: every beat shares one emotional_beat {sorted(emotional)} "
            f"— no arc"
        )


def _load(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def _atomic_write(path: Path, content: str) -> None:
    """temp-then-rename atomic write. Mirrors the planner.py / patch_stager idiom."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def _stub_sam_text(prompt: str) -> SDKResponse:
    """Deterministic Sam envelope — a minimal valid Spark-shaped 5-beat sheet.

    Carries the STUB FALLBACK marker so author_script.py's scan_stub_marker
    refuses to treat it as a real authored script. Cast uses IR namespaces
    (sean / claude-mascot) so it round-trips with the real manifest's
    known_namespaces. The structural pass is always run on it — the stub proves
    the whole contract end-to-end with no key.
    """
    payload = {
        "script_md": (
            "# Script (STUB)\n\nSTUB FALLBACK — Opus SDK unavailable. Sam's "
            "studio-voice treatment would render here. Install claude-agent-sdk "
            "or set ANTHROPIC_API_KEY (and unset ANIMA_FORCE_STUB) for real "
            "authoring.\n"
        ),
        "beats_json": {
            "slug": "stub-piece",
            "logline": "STUB — Sam's logline would render here.",
            "beats": [
                {"id": 1, "title": "Establishing", "intent": "Set the look, framing, and scale.",
                 "emotional_beat": "calm focus", "cast": ["sean", "claude-mascot"],
                 "feel": "establishing — let it breathe", "notes": "loop anchor"},
                {"id": 2, "title": "The draw", "intent": "Sean's hand moves; the mascot turns to look.",
                 "emotional_beat": "first stir", "cast": ["sean", "claude-mascot"]},
                {"id": 3, "title": "The notice", "intent": "The mascot perks up (alert-perk).",
                 "emotional_beat": "spark", "cast": ["claude-mascot"]},
                {"id": 4, "title": "The delight", "intent": "The mascot reacts with small, real delight.",
                 "emotional_beat": "delight", "cast": ["sean", "claude-mascot"]},
                {"id": 5, "title": "The settle", "intent": "The mascot eases back; the loop returns.",
                 "emotional_beat": "settled warmth", "cast": ["sean", "claude-mascot"],
                 "notes": "frame 5 returns to frame 1"},
            ],
        },
    }
    return SDKResponse(
        model=STUB_MODEL,
        text=json.dumps(payload),
        duration_s=0.0,
        exit_code=0,
        error=None,
        stub_fallback=True,
    )
