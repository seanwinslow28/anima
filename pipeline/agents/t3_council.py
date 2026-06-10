"""T3 council — anima's multi-CLI variance critic (the last unbuilt critic tier).

Three HETEROGENEOUS peers fan out in parallel, each a different vendor + lens:
  - Codie — production lens, Codex CLI (run_codex_with_image)
  - Annie — visual + identity/continuity lens, Gemini API
    (run_gemini_api_with_image — Reserved Decision 2, 2026-06-10: agy v1.0.4
    rejects -m so the model can't be pinned on the CLI, and agy -p is an agentic
    harness not a vision call; the API transport pins gemini-3.5-flash by ID and
    reads the served model back, consistent with Em. See
    docs/research/2026-06-10-t3-cli-multimodal-smoke.md.)
  - Sage — narrative/beat lens, Opus via the Claude Agent SDK (invoke_opus_vision)

A SEPARATE Opus chairman (invoke_opus_text — NOT a promoted peer, Pattern C from
agent-fleet-brainstorm-v2 §2.4) synthesizes the three reads into one adjudicated
verdict: consensus + dissent + adjudication note + the council's recommended
proposed_patches.

Structural reference: code-brain/agents-sdk/agents/vault_critic.py — the proven
asyncio fan-out of Codex + Anti-Gravity + SDK with per-source status promotion
(ok / partial / success-empty / error; both-capped → partial). This mirrors its
fan-out + status shape; the chairman is net-new (vault_critic has none).

# Containment (the Gate-3 v1 lesson)
A peer erroring is an HONEST ERRORED GAP in the result — never a gate-aborting
crash. Each peer call is wrapped; a raise (incl. RateCapExhausted) becomes a
peer with status="error", and the council still adjudicates on the survivors.

# Patches stage, never auto-apply
Every peer + the chairman emit Patch(proposed_by=<persona>); the existing
patch_stager.stage_patches_hook writes them into runs/{run_id}/manifest.lock.yaml.
Sean reviews. (critics.t3.auto_apply stays false — Session B wires the config.)

# Session A scope
Engine only — CI-green on stubs, $0. The pre_museum gate wiring + the
critics.t3 manifest config block land in Session B.
"""

from __future__ import annotations

import asyncio
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pipeline.agents import (
    AgentContext,
    AgentResult,
    CostEstimate,
    Patch,
    register_node,
)
from pipeline.agents.cli_runners import RateCapExhausted, run_codex_with_image
from pipeline.agents.gemini_api_runner import run_gemini_api_with_image
from pipeline.agents.sdk_runners import invoke_opus_text, invoke_opus_vision

PROMPTS_DIR = Path(__file__).parent / "prompts"
ANIMA_PREAMBLE_FILE = PROMPTS_DIR / "anima-standing-context.md"

_VIDEO_SUFFIXES = {".mp4", ".webm", ".mov", ".gif"}
_DEFAULT_TIMEOUT_S = 120

# Strip ```json ... ``` fences LLMs sometimes wrap structured output in.
_CODE_FENCE_RE = re.compile(r"^```(?:json)?\s*\n(.*?)\n```\s*$", re.DOTALL)


@dataclass(frozen=True)
class _Peer:
    """A council seat: a persona name, its lens, its addendum file, its transport."""

    name: str
    lens: str
    addendum_file: str
    transport: str  # "codex" | "gemini_api" | "opus_vision"


# The three heterogeneous peers. Order is display order; fan-out is parallel.
_PEERS: tuple[_Peer, ...] = (
    _Peer("codie", "production", "codie-context.md", "codex"),
    _Peer("annie", "visual + identity/continuity", "annie-context.md", "gemini_api"),
    _Peer("sage", "narrative/beat", "sage-context.md", "opus_vision"),
)

# The CLI/quota-prone transports (the "both-CLIs-capped → partial" rule from
# vault_critic). Sage rides the SDK, which surfaces limits as exceptions we
# still contain, but it is not one of the two CLI seats.
_CLI_PEERS = frozenset({"codie", "annie"})

CHAIRMAN_NAME = "chairman"
CHAIRMAN_ADDENDUM_FILE = "chairman-context.md"


@dataclass
class _PeerResult:
    name: str
    status: str  # "ok" | "error"
    rate_capped: bool = False
    error: str | None = None
    parsed: dict[str, Any] | None = field(default=None)


@register_node("t3_council")
class T3CouncilNode:
    """T3 multi-CLI variance council — gate-agnostic.

    Reads an artifact (stills, or a video reduced to a contact sheet) + a
    context bundle (storyboard beat + acceptance_criteria + brief), fans out to
    three heterogeneous peers in parallel, and a separate Opus chairman
    adjudicates. Emits per-peer verdicts, an agreement score, the chairman's
    adjudication note, and staged proposed_patches.
    """

    name = "t3_council"
    inputs: dict = {
        "artifact_paths": list,   # stills and/or videos to review
        "beat_description": str,
        "frame_id": str,
        "checkpoint": str,        # the council gate, e.g. pre_museum_publish
        "gate": str,
    }
    outputs: dict = {
        "verdict": str,           # the chairman's adjudicated verdict
        "agreement_score": float,
        "chairman_note": str,
        "peer_verdicts": dict,
        "status": str,            # ok | partial | success-empty | error
    }
    cites_criteria: list[str] = []  # populated per-run on AgentResult

    def cost_estimate(self, ctx: AgentContext) -> CostEstimate:
        # T3 is $0 incremental on subscriptions (Codex Plus + Google OAuth +
        # Claude Code SDK). Latency is the real cost: ~120s/CLI, run in parallel,
        # plus the chairman synthesis.
        return CostEstimate(usd=0.0, latency_s=150.0, confidence=0.6)

    def run(self, ctx: AgentContext) -> AgentResult:
        t3_cfg = ctx.manifest.get("critics", {}).get("t3", {}) or {}
        timeout_s = int(t3_cfg.get("per_call_timeout_s", _DEFAULT_TIMEOUT_S))

        artifact_paths = [Path(str(p)) for p in (ctx.inputs.get("artifact_paths") or [])]

        # success-empty: nothing to review (the vault_critic "no targets" status).
        if not artifact_paths:
            return self._result(
                verdict="pass",
                agreement=1.0,
                chairman_note="No artifact supplied to the council; nothing to review.",
                peer_results=[],
                patches=[],
                cites=[],
                status="success-empty",
                ctx=ctx,
            )

        temp_sheets: list[Path] = []
        try:
            image_paths = self._resolve_images(artifact_paths, ctx, temp_sheets)

            # Parallel fan-out of the three peers; each contained.
            peer_results = asyncio.run(self._gather_peers(ctx, image_paths, timeout_s))
            status = self._council_status(peer_results)

            ok_results = [p for p in peer_results if p.status == "ok"]
            agreement = self._agreement_score(ok_results)

            # Chairman adjudicates only when at least one peer reported. With no
            # survivors there is nothing to synthesize — honor the total gap.
            if ok_results:
                chairman_parsed = asyncio.run(
                    self._call_chairman(ctx, peer_results, image_paths, timeout_s)
                )
            else:
                chairman_parsed = {
                    "verdict": "borderline",
                    "confidence": 0.0,
                    "reasoning": (
                        "All three peers errored — the council has no survivors to "
                        "adjudicate. Treat as an errored gap, not a pass; a human "
                        "look is required."
                    ),
                    "proposed_patches": [],
                    "cites_criteria": [],
                }
        finally:
            for sheet in temp_sheets:
                try:
                    if sheet.exists():
                        sheet.unlink()
                except OSError:
                    pass

        patches = self._collect_patches(peer_results, chairman_parsed)
        cites = list(chairman_parsed.get("cites_criteria", []) or [])

        return self._result(
            verdict=str(chairman_parsed.get("verdict", "borderline")),
            agreement=agreement,
            chairman_note=str(chairman_parsed.get("reasoning", "")),
            peer_results=peer_results,
            patches=patches,
            cites=cites,
            status=status,
            ctx=ctx,
            chairman_parsed=chairman_parsed,
        )

    # ---------- fan-out ----------

    async def _gather_peers(
        self, ctx: AgentContext, image_paths: list[Path], timeout_s: int,
    ) -> list[_PeerResult]:
        async def _one(peer: _Peer) -> _PeerResult:
            prompt = self._build_peer_prompt(ctx, peer)
            fn = self._peer_transport(peer.transport)
            try:
                resp = await fn(prompt=prompt, image_paths=image_paths, timeout_s=timeout_s)
            except RateCapExhausted as exc:
                return _PeerResult(peer.name, status="error", rate_capped=True, error=str(exc)[:300])
            except Exception as exc:  # noqa: BLE001 — contain ANY peer failure
                return _PeerResult(peer.name, status="error", error=str(exc)[:300])
            if not getattr(resp, "ok", True):
                return _PeerResult(peer.name, status="error", error=getattr(resp, "error", None))
            parsed = self._parse(getattr(resp, "text", ""))
            return _PeerResult(peer.name, status="ok", parsed=parsed)

        return list(await asyncio.gather(*[_one(p) for p in _PEERS]))

    def _peer_transport(self, transport: str):
        """Resolve the transport coroutine BY MODULE GLOBAL at call time so test
        monkeypatching of these names takes effect (mirrors vision_critic)."""
        if transport == "codex":
            return run_codex_with_image
        if transport == "gemini_api":
            return run_gemini_api_with_image
        if transport == "opus_vision":
            return invoke_opus_vision
        raise ValueError(f"unknown peer transport: {transport!r}")

    async def _call_chairman(
        self, ctx: AgentContext, peer_results: list[_PeerResult],
        image_paths: list[Path], timeout_s: int,
    ) -> dict[str, Any]:
        """The SEPARATE chairman synthesis call (invoke_opus_text, Pattern C)."""
        prompt = self._build_chairman_prompt(ctx, peer_results)
        try:
            resp = await invoke_opus_text(prompt=prompt, timeout_s=timeout_s)
        except Exception as exc:  # noqa: BLE001 — a failed chairman is a gap, not a crash
            return {
                "verdict": "borderline",
                "confidence": 0.0,
                "reasoning": f"Chairman synthesis failed ({str(exc)[:200]}); defer to a human look.",
                "proposed_patches": [],
                "cites_criteria": [],
            }
        return self._parse(getattr(resp, "text", ""))

    # ---------- status + agreement ----------

    def _council_status(self, peer_results: list[_PeerResult]) -> str:
        errored = [p for p in peer_results if p.status == "error"]
        if len(errored) == len(peer_results):
            return "error"
        # both-CLIs-capped → partial (vault_critic); generalizes to "any peer errored".
        if errored:
            return "partial"
        return "ok"

    def _agreement_score(self, ok_results: list[_PeerResult]) -> float:
        """Fraction of surviving peers sharing the modal verdict. 0.0 with no
        survivors; 1.0 with a single survivor (trivially unanimous)."""
        if not ok_results:
            return 0.0
        verdicts = [str((p.parsed or {}).get("verdict", "borderline")) for p in ok_results]
        counts: dict[str, int] = {}
        for v in verdicts:
            counts[v] = counts.get(v, 0) + 1
        modal = max(counts.values())
        return modal / len(verdicts)

    # ---------- patches ----------

    def _collect_patches(
        self, peer_results: list[_PeerResult], chairman_parsed: dict[str, Any],
    ) -> list[Patch]:
        out: list[Patch] = []
        for p in peer_results:
            if p.status != "ok" or not p.parsed:
                continue
            out.extend(self._patches_from(p.parsed, proposed_by=p.name))
        out.extend(self._patches_from(chairman_parsed, proposed_by=CHAIRMAN_NAME))
        return out

    def _patches_from(self, parsed: dict[str, Any], *, proposed_by: str) -> list[Patch]:
        out: list[Patch] = []
        for entry in parsed.get("proposed_patches", []) or []:
            if not isinstance(entry, dict):
                continue
            try:
                operation = str(entry.get("operation", "set"))
                if operation not in {"set", "append", "delete"}:
                    operation = "set"
                out.append(Patch(
                    target=str(entry.get("target", "manifest.lock.yaml")),
                    path=str(entry["path"]),
                    operation=operation,  # type: ignore[arg-type]
                    value=entry.get("value"),
                    rationale=str(entry.get("rationale", "")),
                    proposed_by=proposed_by,
                    cites_criteria=tuple(str(c) for c in entry.get("cites_criteria", []) or ()),
                ))
            except (KeyError, TypeError, ValueError):
                continue
        return out

    # ---------- prompt assembly ----------

    def _anima_preamble(self) -> str:
        if ANIMA_PREAMBLE_FILE.exists():
            return ANIMA_PREAMBLE_FILE.read_text(encoding="utf-8")
        return ""

    def _addendum(self, filename: str) -> str:
        path = PROMPTS_DIR / filename
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""

    def _council_brief(self, ctx: AgentContext) -> str:
        frame_id = ctx.inputs.get("frame_id", "?")
        gate = ctx.inputs.get("gate", ctx.inputs.get("checkpoint", "?"))
        beat = ctx.inputs.get("beat_description", "")
        return (
            "## Council brief\n\n"
            f"- gate: {gate}\n"
            f"- frame_id: {frame_id}\n"
            f"- beat description: {beat}\n\n"
            "Review the attached artifact against this brief and your lens. Emit the "
            "structured JSON response specified in your role addendum — verdict / "
            "confidence / reasoning / proposed_patches / cites_criteria. Nothing else."
        )

    def _build_peer_prompt(self, ctx: AgentContext, peer: _Peer) -> str:
        sections = [s for s in (
            self._anima_preamble(),
            self._addendum(peer.addendum_file),
            self._council_brief(ctx),
        ) if s]
        return "\n\n".join(sections)

    def _build_chairman_prompt(self, ctx: AgentContext, peer_results: list[_PeerResult]) -> str:
        peer_block_lines = ["## Peer reports to adjudicate", ""]
        for p in peer_results:
            if p.status == "ok" and p.parsed:
                peer_block_lines.append(
                    f"### {p.name} ({self._lens_for(p.name)}) — status: ok\n"
                    f"- verdict: {p.parsed.get('verdict')}\n"
                    f"- confidence: {p.parsed.get('confidence')}\n"
                    f"- cites_criteria: {p.parsed.get('cites_criteria')}\n"
                    f"- reasoning: {p.parsed.get('reasoning')}\n"
                    f"- proposed_patches: {json.dumps(p.parsed.get('proposed_patches', []))}\n"
                )
            else:
                peer_block_lines.append(
                    f"### {p.name} ({self._lens_for(p.name)}) — status: ERROR\n"
                    f"- This peer returned no usable report ({p.error or 'errored'}). "
                    f"Weigh the surviving peers; do not invent this one's verdict.\n"
                )
        sections = [s for s in (
            self._anima_preamble(),
            self._addendum(CHAIRMAN_ADDENDUM_FILE),
            self._council_brief(ctx),
            "\n".join(peer_block_lines),
        ) if s]
        return "\n\n".join(sections)

    def _lens_for(self, name: str) -> str:
        for p in _PEERS:
            if p.name == name:
                return p.lens
        return "?"

    # ---------- artifacts ----------

    def _resolve_images(
        self, artifact_paths: list[Path], ctx: AgentContext, temp_sheets: list[Path],
    ) -> list[Path]:
        """Map artifacts to still images the peers can read. Videos become a
        contact sheet (the motion-proper blind spot is accepted — a still judge
        sees staging/identity/continuity, not true motion timing)."""
        out: list[Path] = []
        for path in artifact_paths:
            if path.suffix.lower() in _VIDEO_SUFFIXES:
                from pipeline.contact_sheet import build_contact_sheet
                temp_dir = ctx.run_dir / "temp_contact_sheets"
                temp_dir.mkdir(parents=True, exist_ok=True)
                sheet = temp_dir / f"council_sheet_{path.stem}.png"
                build_contact_sheet(source=path, out_path=sheet, n=6, cols=3)
                temp_sheets.append(sheet)
                out.append(sheet)
            else:
                out.append(path)
        return out

    # ---------- parsing + result ----------

    def _parse(self, text: str) -> dict[str, Any]:
        """Parse a peer/chairman JSON envelope; tolerate code fences. An
        unparseable response becomes a defensive borderline (never a silent pass)."""
        stripped = (text or "").strip()
        m = _CODE_FENCE_RE.match(stripped)
        if m:
            stripped = m.group(1).strip()
        try:
            data = json.loads(stripped)
        except json.JSONDecodeError:
            return {
                "verdict": "borderline", "confidence": 0.0,
                "reasoning": "Unparseable response; defensive borderline. Head: "
                + (text or "")[:200].replace("\n", " "),
                "proposed_patches": [], "cites_criteria": [],
            }
        if not isinstance(data, dict):
            return {
                "verdict": "borderline", "confidence": 0.0,
                "reasoning": "Response was not a JSON object; defensive borderline.",
                "proposed_patches": [], "cites_criteria": [],
            }
        verdict = str(data.get("verdict", "borderline")).lower().strip()
        if verdict not in {"pass", "borderline", "fail"}:
            verdict = "borderline"
        try:
            confidence = float(data.get("confidence", 0.0))
        except (TypeError, ValueError):
            confidence = 0.0
        confidence = max(0.0, min(1.0, confidence))
        # The chairman may carry consensus/dissent/adjudication; fold adjudication
        # into reasoning if reasoning is absent so chairman_note is always populated.
        reasoning = str(data.get("reasoning") or data.get("adjudication") or "")
        return {
            "verdict": verdict,
            "confidence": confidence,
            "reasoning": reasoning,
            "consensus": str(data.get("consensus", "")),
            "dissent": str(data.get("dissent", "")),
            "proposed_patches": list(data.get("proposed_patches", []) or []),
            "cites_criteria": list(data.get("cites_criteria", []) or []),
        }

    def _result(
        self, *, verdict: str, agreement: float, chairman_note: str,
        peer_results: list[_PeerResult], patches: list[Patch], cites: list[str],
        status: str, ctx: AgentContext, chairman_parsed: dict[str, Any] | None = None,
    ) -> AgentResult:
        peer_verdicts = {
            p.name: {
                "status": p.status,
                "verdict": (p.parsed or {}).get("verdict") if p.parsed else None,
                "confidence": (p.parsed or {}).get("confidence") if p.parsed else None,
                "reasoning": (p.parsed or {}).get("reasoning") if p.parsed else None,
                "cites_criteria": (p.parsed or {}).get("cites_criteria", []) if p.parsed else [],
                "error": p.error,
            }
            for p in peer_results
        }
        note_extra = ""
        if chairman_parsed:
            consensus = chairman_parsed.get("consensus")
            dissent = chairman_parsed.get("dissent")
            if consensus or dissent:
                note_extra = f" | consensus: {consensus} | dissent: {dissent}"
        return AgentResult(
            outputs={
                "verdict": verdict,
                "agreement_score": agreement,
                "chairman_note": chairman_note,
                "peer_verdicts": peer_verdicts,
                "status": status,
            },
            tier=ctx.tier,
            proposed_patches=patches,
            cites_criteria=cites,
            notes=(
                f"t3-council@{ctx.inputs.get('gate', ctx.inputs.get('checkpoint', '?'))} "
                f"status={status} agreement={agreement:.2f} verdict={verdict}{note_extra}"
            ),
        )
