"""Em — anima's T2 vision critic.

Single SDK agent at three checkpoints: per-frame Generate (Phase 5),
post-Motion (Phase 6 → 7), post-Assemble (Phase 8 → 9). Gemini 3.1 Pro via
Anti-Gravity CLI is the default voice; Opus 4.7 via Claude Agent SDK is the
escalation hatch when Gemini's confidence drops below
critics.t2.escalation_threshold OR a shot carries an impact_tag matching
critics.t2.escalation_tags.

Per v2 brainstorm §2.5 + §6 + §10 the patches stage and never auto-apply;
the patch_stager.py post_run hook writes them into manifest.lock.yaml. Per
v2 §2.3 (Pattern B), the cites_criteria invariant is enforced inside run()
before returning — a fail or borderline verdict without a cited AC ID
raises ValueError.
"""

from __future__ import annotations

import asyncio
import json
import re
from pathlib import Path
from typing import Any

from pipeline.agents import (
    AgentContext,
    AgentResult,
    CostEstimate,
    Patch,
    register_node,
)
from pipeline.agents.cli_runners import run_antigravity_with_image
from pipeline.agents.reference_selection import select_references, ReferenceSelectionError
from pipeline.agents.sdk_runners import invoke_opus_vision

PROMPTS_DIR = Path(__file__).parent / "prompts"
PERSONA_NAME = "em-vision-critic"

ANIMA_PREAMBLE_FILE = PROMPTS_DIR / "anima-standing-context.md"
EM_ADDENDUM_FILE = PROMPTS_DIR / "em-vision-critic-context.md"

_DEFAULT_ESCALATION_THRESHOLD = 0.7
_DEFAULT_ESCALATION_TAGS = ("hero", "identity_critical")
_DEFAULT_TIMEOUT_S = 120

# Repo-root-relative characters dir (robust to cwd; works in a worktree too).
_CHARACTERS_ROOT = Path(__file__).resolve().parents[2] / "characters"

# checkpoint -> pipeline phase number, for criteria phase-filtering (Task 4).
_CHECKPOINT_PHASE = {
    "phase_5_generate": 5,
    "phase_6_motion": 6,
    "phase_8_assemble": 8,
}

# Strip ```json ... ``` wrappers that LLMs sometimes add around structured output.
_CODE_FENCE_RE = re.compile(r"^```(?:json)?\s*\n(.*?)\n```\s*$", re.DOTALL)


@register_node("vision_critic")
class VisionCriticNode:
    """T2 vision critic node — Em.

    Reads a generated frame (Phase 5) / motion clip (Phase 6) / assembled cut
    (Phase 8) and emits a structured verdict + reasoning + confidence +
    proposed patches + criteria citations. The escalation hatch from Gemini
    to Opus is gated by either a confidence drop OR an impact_tag match.
    """

    name = "vision_critic"
    inputs: dict = {
        "image_path": str,
        "beat_description": str,
        "frame_id": str,
        "impact_tags": list,
        "checkpoint": str,  # phase_5_generate | phase_6_motion | phase_8_assemble
    }
    outputs: dict = {
        "verdict": str,
        "reasoning": str,
        "confidence": float,
    }
    cites_criteria: list[str] = []  # populated per-run on AgentResult

    def cost_estimate(self, ctx: AgentContext) -> CostEstimate:
        # Subscription-absorbed; $ is decorative until commit 5's runtime
        # enforcement layer reads this field. Latency is the real signal:
        # ~15s for the Gemini default, ~60s when Opus escalates.
        return CostEstimate(usd=0.0, latency_s=15.0, confidence=0.7)

    def run(self, ctx: AgentContext) -> AgentResult:
        t2_cfg = self._t2_config(ctx)
        threshold = float(t2_cfg.get("escalation_threshold", _DEFAULT_ESCALATION_THRESHOLD))
        escalation_tags = set(t2_cfg.get("escalation_tags", _DEFAULT_ESCALATION_TAGS))
        timeout_s = int(t2_cfg.get("per_call_timeout_s", _DEFAULT_TIMEOUT_S))

        image_path = Path(str(ctx.inputs["image_path"]))
        impact_tags = set(ctx.inputs.get("impact_tags", []) or [])
        forced_escalation = bool(impact_tags & escalation_tags)

        references = self._resolve_references(ctx)
        prompt = self._build_prompt(ctx, t2_cfg, n_references=len(references))

        is_video = image_path.suffix.lower() in {".mp4", ".webm", ".mov", ".gif"}
        temp_contact_sheet_path = None
        model_image_path = image_path

        if is_video:
            from pipeline.contact_sheet import build_contact_sheet
            temp_dir = ctx.run_dir / "temp_contact_sheets"
            temp_dir.mkdir(parents=True, exist_ok=True)
            frame_id = ctx.inputs.get("frame_id", "clip")
            temp_contact_sheet_path = temp_dir / f"contact_sheet_{frame_id}.png"
            build_contact_sheet(
                source=image_path,
                out_path=temp_contact_sheet_path,
                n=6,
                cols=3,
            )
            model_image_path = temp_contact_sheet_path

        image_paths = [model_image_path, *references]

        try:
            gemini = asyncio.run(run_antigravity_with_image(
                prompt=prompt,
                image_paths=image_paths,
                timeout_s=timeout_s,
            ))
            parsed = self._parse(gemini.text, default_verdict="borderline")
            escalated = False

            if forced_escalation or parsed["confidence"] < threshold:
                opus = asyncio.run(invoke_opus_vision(
                    prompt=prompt,
                    image_paths=image_paths,
                    timeout_s=timeout_s,
                ))
                parsed = self._parse(opus.text, default_verdict="borderline")
                escalated = True
        finally:
            if temp_contact_sheet_path and temp_contact_sheet_path.exists():
                try:
                    temp_contact_sheet_path.unlink()
                except Exception:
                    pass

        verdict = parsed["verdict"]
        cites = list(parsed.get("cites_criteria", []) or [])

        # v2 brainstorm §2.3 Pattern B — the structural fix for local-optimization
        # drift. A blocking verdict without a citation is rejected at the
        # contract layer; Em cannot block without grounding the verdict.
        if verdict in {"fail", "borderline"} and not cites:
            raise ValueError(
                f"Em emitted verdict={verdict!r} with empty cites_criteria; "
                f"this violates v2 brainstorm §2.3 Pattern B. "
                f"frame_id={ctx.inputs.get('frame_id')!r}, "
                f"checkpoint={ctx.inputs.get('checkpoint')!r}."
            )

        patches = self._build_patches(parsed, ctx)

        return AgentResult(
            outputs={
                "verdict": verdict,
                "reasoning": str(parsed.get("reasoning", "")),
                "confidence": float(parsed["confidence"]),
            },
            tier=ctx.tier,
            proposed_patches=patches,
            cites_criteria=cites,
            notes=(
                f"em@{ctx.inputs.get('checkpoint', '?')} "
                f"frame={ctx.inputs.get('frame_id', '?')} "
                f"{'(escalated)' if escalated else '(gemini)'}"
            ),
        )

    # ---------- internals ----------

    def _t2_config(self, ctx: AgentContext) -> dict[str, Any]:
        return ctx.manifest.get("critics", {}).get("t2", {}) or {}

    def _characters_root(self, ctx: AgentContext) -> Path:
        override = ctx.manifest.get("characters_root")
        return Path(override) if override else _CHARACTERS_ROOT

    def _resolve_references(self, ctx: AgentContext) -> list[Path]:
        """The Bible reference bundle for this frame. Empty when no character_id is
        declared (graceful — today's reference-blind behavior, no wrong-character
        references)."""
        character_id = ctx.inputs.get("character_id")
        if not character_id:
            return []
        try:
            return select_references(
                str(character_id),
                str(ctx.inputs.get("checkpoint", "")),
                str(ctx.inputs.get("beat_description", "")),
                characters_root=self._characters_root(ctx),
            )
        except ReferenceSelectionError:
            return []

    def _build_prompt(self, ctx: AgentContext, t2_cfg: dict, n_references: int = 0) -> str:
        """Concatenate the shared anima preamble + Em's addendum + any
        manifest-declared default_context_files + the per-checkpoint
        frame brief into a single prompt string.

        The preamble pattern is lifted from
        code-brain/agents-sdk/prompts/vault-critic-standing-context.md —
        proven to cut the generic-recommendation failure mode in the
        2026-05-24 ablation runs.
        """
        sections: list[str] = []

        # Always-on standing context. If the file is missing we still ship
        # a sensible critic — but the preamble is non-optional in production.
        if ANIMA_PREAMBLE_FILE.exists():
            sections.append(ANIMA_PREAMBLE_FILE.read_text(encoding="utf-8"))
        if EM_ADDENDUM_FILE.exists():
            sections.append(EM_ADDENDUM_FILE.read_text(encoding="utf-8"))

        # Default supporting-doc context (PHILOSOPHY.md, CLAUDE.md, etc.) —
        # mirrors the vault_critic default_context_files pattern.
        for raw_path in t2_cfg.get("default_context_files", []) or []:
            p = Path(raw_path)
            if not p.is_absolute():
                # Best-effort: resolve relative to ctx.run_dir's repo root.
                candidate = Path.cwd() / p
                if candidate.exists():
                    p = candidate
            if p.exists():
                sections.append(
                    f"## Supporting context — {raw_path}\n\n"
                    + p.read_text(encoding="utf-8", errors="replace")
                )

        # Per-invocation frame brief.
        frame_id = ctx.inputs.get("frame_id", "?")
        beat = ctx.inputs.get("beat_description", "")
        checkpoint = ctx.inputs.get("checkpoint", "?")
        impact_tags = list(ctx.inputs.get("impact_tags", []) or [])
        sections.append(
            f"## Current frame brief\n\n"
            f"- frame_id: {frame_id}\n"
            f"- checkpoint: {checkpoint}\n"
            f"- impact_tags: {impact_tags}\n"
            f"- beat description: {beat}\n\n"
            f"Review the attached image against this brief and the manifest's "
            f"style block. Emit the structured JSON response specified in your "
            f"role addendum — verdict / confidence / reasoning / "
            f"proposed_patches / cites_criteria. Nothing else."
        )

        # Reference plates: tell Em which image is the subject vs the references.
        # This is the licence-to-pass she lacks reference-blind — and a sycophancy
        # surface, so the wording stays deliberately conservative; the false_pass
        # guard in the re-baseline is its empirical check (spec §5.2, §9).
        if n_references > 0:
            sections.append(
                "## Reference plates (identity/style ground truth)\n\n"
                "Image 1 is the FRAME UNDER REVIEW. Every image after it is an "
                "identity/style REFERENCE PLATE from this character's Bible — the "
                "canonical truth for who the character is (anchor + turnaround "
                "views). Compare the subject (image 1) against them. A feature that "
                "MATCHES the references is correct even if it differs from a generic "
                "expectation — do NOT flag a difference the references confirm is "
                "correct. A feature that DRIFTS from the references is exactly the "
                "identity/style defect you exist to catch. Judge the subject against "
                "its own Bible, not against a generic ideal."
            )

        # Phase 6 motion: the attached image is a contact sheet sampling a
        # clip, not a single still. Be explicit about the limit of looking —
        # a contact sheet shows content across time (identity, style,
        # continuity) but NOT motion-proper. Telling Em this is what stops a
        # shuffled-frame guess from laundering itself into a motion verdict.
        # (docs/research/2026-05-31-ai-evals-best-practices-...md §3.5)
        if checkpoint == "phase_6_motion":
            sections.append(
                "## Contact-sheet honesty (Phase 6 motion review)\n\n"
                "The attached image is a CONTACT SHEET sampling this motion "
                "clip: panels read left-to-right, top-to-bottom as time "
                "(t0, t1, ... earliest to latest). You are NOT seeing the "
                "clip play.\n\n"
                "You CAN assess, across the strip: identity continuity (does "
                "Sean stay Sean t0->tN), style/register hold (line weight, "
                "paper grain, palette), stylus-hand continuity, outfit "
                "consistency, gross pose progression against the beat.\n\n"
                "You CANNOT assess from static frames: motion smoothness, "
                "jitter/skating, temporal flicker, or texture-crawl/boiling. "
                "Do NOT issue a verdict on those — you cannot see them in a "
                "contact sheet. If the beat's success depends on motion-proper "
                "quality, say so explicitly in your reasoning and defer it to "
                "a human look or a deterministic metric. Judge only what the "
                "strip can show; name the limit rather than guessing past it."
            )

        return "\n\n".join(sections)

    def _parse(self, text: str, *, default_verdict: str) -> dict[str, Any]:
        """Parse the structured JSON response. Tolerate code-fenced wrapping
        and minor punctuation deviations the LLM sometimes adds. On
        unparseable output, return a defensive borderline shape so the
        cites_criteria invariant check fires (which is the correct behavior —
        an uninterpretable response should never count as a pass).
        """
        stripped = text.strip()
        m = _CODE_FENCE_RE.match(stripped)
        if m:
            stripped = m.group(1).strip()

        try:
            data = json.loads(stripped)
        except json.JSONDecodeError:
            return {
                "verdict": default_verdict,
                "confidence": 0.0,
                "reasoning": (
                    "Em could not parse the model's response as JSON. "
                    "Original text head: " + text[:200].replace("\n", " ")
                ),
                "proposed_patches": [],
                "cites_criteria": [],
            }

        if not isinstance(data, dict):
            return {
                "verdict": default_verdict,
                "confidence": 0.0,
                "reasoning": "Em parsed a JSON response that wasn't an object.",
                "proposed_patches": [],
                "cites_criteria": [],
            }

        verdict = str(data.get("verdict", default_verdict)).lower().strip()
        if verdict not in {"pass", "borderline", "fail"}:
            verdict = default_verdict

        try:
            confidence = float(data.get("confidence", 0.0))
        except (TypeError, ValueError):
            confidence = 0.0
        confidence = max(0.0, min(1.0, confidence))

        return {
            "verdict": verdict,
            "confidence": confidence,
            "reasoning": str(data.get("reasoning", "")),
            "proposed_patches": list(data.get("proposed_patches", []) or []),
            "cites_criteria": list(data.get("cites_criteria", []) or []),
        }

    def _build_patches(
        self, parsed: dict[str, Any], ctx: AgentContext,
    ) -> list[Patch]:
        """Map parsed['proposed_patches'] entries to Patch instances tagged
        with proposed_by=PERSONA_NAME. Drops malformed entries with a noisy
        notes-field-style warning rather than crashing the critic.
        """
        out: list[Patch] = []
        for entry in parsed.get("proposed_patches", []) or []:
            if not isinstance(entry, dict):
                continue
            try:
                target = str(entry.get("target", "manifest.lock.yaml"))
                path = str(entry["path"])
                operation = str(entry.get("operation", "set"))
                if operation not in {"set", "append", "delete"}:
                    operation = "set"
                value = entry.get("value")
                rationale = str(entry.get("rationale", ""))
                cites = tuple(str(c) for c in entry.get("cites_criteria", []) or [])
                out.append(Patch(
                    target=target,
                    path=path,
                    operation=operation,  # type: ignore[arg-type]
                    value=value,
                    rationale=rationale,
                    proposed_by=PERSONA_NAME,
                    cites_criteria=cites,
                ))
            except (KeyError, TypeError, ValueError):
                # Skip malformed patches rather than aborting the whole run.
                continue
        return out
