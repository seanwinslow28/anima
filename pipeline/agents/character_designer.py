"""anima — Cy the Character Designer (Phase 2 AgentSpec).

Cy runs once per character. Three-phase loop with categorically different
model assignment per phase:

  Pass 1 — Opus 4.7 authors (text-only).
           Emits the five-artifact JSON envelope: character.yaml + IR.* graph
           entries + risk-bible.md + cy-confidence-notes.md +
           plate_generation_plan.json.

  Pass 2 — Nano Banana Pro generates plates per Pass 1's plan (image).
           Per-plate cache; ingest-from-source-refs or generate-via-NB-Pro
           per plate.source value. Reject-aware regeneration via the
           reject_reason parameter when Pass 3 flags a plate.

  Pass 3 — Gemini 3.1 Pro verifies every plate against cited IR.* rules
           (vision, via the same agy CLI wrapper Em uses). Three-attempt
           ceiling per plate; ceiling-hit surfaces 'human_gate_required'
           in plate_results without failing the whole run.

The AgentSpec shape mirrors Maya verbatim — three-phase orchestration,
JSON envelope contract, atomic writes via temp-then-rename, clean-markdown
enforcement on the prose artifacts. The model assignment per phase is the
structural difference: Maya is Opus→Sonnet→Opus (all text); Cy is
Opus→NB-Pro→Gemini (text → image → vision).

Per brainstorm TOP-3 + ENG3. Per Sean's commit-2 planning clarification:
the per-character acceptance_criteria.json file lives in the character
folder (Bible is self-contained); the runner merges it with Maya's brief
file via the manifest criteria_sources block (Task 1.8).
"""

from __future__ import annotations

import asyncio
import json
import re
import shutil
from pathlib import Path
from typing import Any, ClassVar

import yaml

from pipeline.agents import (
    AgentContext,
    AgentResult,
    CostEstimate,
    register_node,
)
from pipeline.agents.cli_runners import run_antigravity_with_image
from pipeline.agents.nb_pro_runner import NBProResponse, invoke_nb_pro
from pipeline.agents.sdk_runners import invoke_opus_text
from pipeline.criteria import validate_criteria

PROMPTS_DIR = Path(__file__).parent / "prompts"
ANIMA_PREAMBLE_FILE = PROMPTS_DIR / "anima-standing-context.md"
CY_ADDENDUM_FILE = PROMPTS_DIR / "cy-character-designer-context.md"

# The 2D animation principles skill — Cy loads its SKILL.md verbatim as an
# inline appendix per ENG5 (folded into TOP-3). Skill lives at the project's
# .claude/skills/ directory.
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
ANIMATION_PRINCIPLES_SKILL_FILE = (
    _PROJECT_ROOT / ".claude" / "skills" / "2d-animation-principles" / "SKILL.md"
)

# JSON code-fence stripper. LLMs habitually wrap structured output in
# ```json ... ```; the parser tolerates either shape.
_CODE_FENCE_RE = re.compile(r"^\s*```(?:json)?\s*\n?(.*?)\n?\s*```\s*$", re.DOTALL)

# Box-drawing characters forbidden in risk-bible.md + cy-confidence-notes.md.
# Same contract enforcement Maya applies to plan.md — the CLI renders boxes
# in `pipeline bible show`; Cy emits clean prose. Burning Opus tokens on
# box-drawing characters is a contract violation.
_BOX_CHARACTERS = frozenset("╔═╗║╚╝┌─┐│└┘├┤┬┴┼")

# Per-plate ceiling. Three attempts (initial + two regens) before surfacing
# the plate to the human gate. Mirrors Maya's three-call ceiling per plan,
# but per-plate scope since Cy may have many plates.
_PLATE_ATTEMPT_CEILING = 3

# Pass-3 Gemini timeout per plate. Same default Em uses in vision_critic.py.
_GEMINI_TIMEOUT_S = 120


@register_node("character_designer")
class CharacterDesignerNode:
    """Cy — character designer. Phase 2 AgentSpec."""

    name: ClassVar[str] = "character_designer"
    inputs: ClassVar[dict[str, type]] = {
        "character_dir": str,
        "studio_brief": str,
    }
    outputs: ClassVar[dict[str, type]] = {
        "character_yaml_path": str,
        "criteria_path": str,
        "risk_bible_path": str,
        "cy_confidence_notes_path": str,
        "plate_generation_plan_path": str,
        "plate_results": dict,
    }
    cites_criteria: ClassVar[list[str]] = []

    def cost_estimate(self, ctx: AgentContext) -> CostEstimate:
        # Subscription-absorbed Opus + Gemini; NB Pro is the variable cost.
        # Budget envelope per brainstorm TOP-3: ~20-30 plates × $0.15 = $3-5
        # per Bible. The actual estimate refines once Pass 1's plate plan is
        # known; this static estimate is what Maya consumes for the pre-run
        # cost preview.
        return CostEstimate(usd=4.0, latency_s=900.0, confidence=0.6)

    def run(self, ctx: AgentContext) -> AgentResult:
        character_dir = Path(ctx.inputs["character_dir"])
        source_refs_dir = character_dir / "source-refs"

        # Precondition: source-refs/ must exist AND contain at least one file
        # so Cy has material to read during Pass 1. Empty folder is the
        # blank-page tax — Sean needs to drop something first.
        if not source_refs_dir.exists() or not any(source_refs_dir.iterdir()):
            raise FileNotFoundError(
                f"source-refs/ at {source_refs_dir} is missing or empty. "
                f"Run `python -m pipeline.cli bible init --target {character_dir}` "
                f"and drop source material per source-refs-checklist.md first."
            )

        # ---------- Pass 1 — Opus authors ----------
        studio_brief = str(ctx.inputs.get("studio_brief", ""))
        opus_prompt = self._build_pass1_prompt(
            studio_brief=studio_brief,
            character_dir=character_dir,
        )
        # 900s timeout for Cy's Pass-1: the prompt is ~55KB (anima preamble
        # + Cy addendum + 2d-animation-principles skill inline + per-Bible
        # brief) and the envelope is ~50KB (character.yaml + 15-20 IR.* rules
        # + risk-bible + confidence-notes + plate plan). Observed wall time
        # against real Opus on the sean-anchor authoring run: ~500s. The
        # invoke_opus_text default of 120s would cleanly time out before
        # Pass 1 ever completed.
        opus_resp = asyncio.run(invoke_opus_text(prompt=opus_prompt, timeout_s=900))

        parsed = self._parse_pass1_envelope(
            opus_resp.text,
            character_dir=character_dir,
            stub_fallback=bool(getattr(opus_resp, "stub_fallback", False)),
        )

        character_yaml: dict = parsed["character_yaml"]
        ir_entries: list[dict] = parsed["ir_entries"]
        risk_bible_md: str = parsed["risk_bible_md"]
        cy_confidence_notes_md: str = parsed["cy_confidence_notes_md"]
        plate_plan: dict = parsed["plate_generation_plan"]

        # Contract: prose artifacts must be clean markdown (no terminal-aesthetic).
        self._enforce_clean_markdown(risk_bible_md, "risk-bible.md")
        self._enforce_clean_markdown(cy_confidence_notes_md, "cy-confidence-notes.md")

        # Build + validate the per-character acceptance_criteria.json.
        criteria_json = {
            "version": "1.2",
            "locked": False,
            "criteria": ir_entries,
        }
        validate_criteria(criteria_json)  # raises on invalid IR.* entries

        # Write Pass-1 artifacts atomically.
        character_dir.mkdir(parents=True, exist_ok=True)
        character_yaml_path = character_dir / "character.yaml"
        criteria_path = character_dir / "acceptance_criteria.json"
        risk_bible_path = character_dir / "risk-bible.md"
        confidence_notes_path = character_dir / "cy-confidence-notes.md"
        plate_plan_path = character_dir / "plate_generation_plan.json"

        _atomic_write_text(character_yaml_path, yaml.safe_dump(character_yaml, sort_keys=False))
        _atomic_write_text(criteria_path, json.dumps(criteria_json, indent=2))
        _atomic_write_text(risk_bible_path, risk_bible_md)
        _atomic_write_text(confidence_notes_path, cy_confidence_notes_md)
        _atomic_write_text(plate_plan_path, json.dumps(plate_plan, indent=2))

        # ---------- Passes 2 + 3 — per-plate generate + verify ----------
        nb_pro_cache_dir = ctx.cache_dir / "nb_pro"
        nb_pro_cache_dir.mkdir(parents=True, exist_ok=True)

        plate_results: dict[str, dict] = {}
        for plate in plate_plan.get("plates", []):
            status = self._run_plate(
                plate=plate,
                ir_entries=ir_entries,
                character_dir=character_dir,
                cache_dir=nb_pro_cache_dir,
            )
            plate_results[plate["target_path"]] = status

        # ---------- Collect cites_criteria + return ----------
        cites = [entry["id"] for entry in ir_entries]
        human_gate_count = sum(
            1 for v in plate_results.values()
            if v.get("status") == "human_gate_required"
        )
        notes = (
            f"cy@phase_2 character_id={character_yaml.get('character_id', '?')!r} "
            f"plates={len(plate_results)} human_gate_required={human_gate_count}"
        )

        return AgentResult(
            outputs={
                "character_yaml_path": str(character_yaml_path),
                "criteria_path": str(criteria_path),
                "risk_bible_path": str(risk_bible_path),
                "cy_confidence_notes_path": str(confidence_notes_path),
                "plate_generation_plan_path": str(plate_plan_path),
                "plate_results": plate_results,
            },
            tier=ctx.tier,
            cites_criteria=cites,
            notes=notes,
        )

    # ----- prompt builders -----

    def _build_pass1_prompt(
        self,
        *,
        studio_brief: str,
        character_dir: Path,
    ) -> str:
        """Concatenate anima preamble + Cy addendum + 2d-animation-principles
        skill + per-invocation brief into the Pass-1 prompt."""
        sections: list[str] = []

        if ANIMA_PREAMBLE_FILE.exists():
            sections.append(ANIMA_PREAMBLE_FILE.read_text(encoding="utf-8"))
        if CY_ADDENDUM_FILE.exists():
            sections.append(CY_ADDENDUM_FILE.read_text(encoding="utf-8"))
        if ANIMATION_PRINCIPLES_SKILL_FILE.exists():
            sections.append(
                "## Inline appendix — 2D animation principles\n\n"
                + ANIMATION_PRINCIPLES_SKILL_FILE.read_text(encoding="utf-8")
            )

        sections.append(self._per_invocation_brief(studio_brief, character_dir))
        return "\n\n".join(sections)

    def _per_invocation_brief(self, studio_brief: str, character_dir: Path) -> str:
        """The per-Bible brief — Studio Brief + source-refs/ contents listing."""
        source_refs_dir = character_dir / "source-refs"
        listing_lines: list[str] = []
        for entry in sorted(source_refs_dir.rglob("*")):
            if entry.is_file():
                rel = entry.relative_to(character_dir)
                listing_lines.append(f"- {rel}")
        listing = "\n".join(listing_lines) if listing_lines else "(empty)"

        notes_path = source_refs_dir / "notes.md"
        notes_excerpt = ""
        if notes_path.exists():
            notes_excerpt = (
                "\n\n### source-refs/notes.md\n\n"
                + notes_path.read_text(encoding="utf-8", errors="replace")
            )

        return (
            f"## Pass 1 — author this Bible\n\n"
            f"### Studio Brief\n\n{studio_brief}\n\n"
            f"### source-refs/ contents\n\n{listing}"
            f"{notes_excerpt}\n\n"
            f"Emit the five-artifact JSON envelope your role addendum specifies. "
            f"Wrap it in a ```json``` code fence. The envelope's keys, in order: "
            f"`character_yaml`, `ir_entries`, `risk_bible_md`, "
            f"`cy_confidence_notes_md`, `plate_generation_plan`."
        )

    def _build_pass3_prompt(
        self,
        *,
        plate: dict,
        ir_entries: list[dict],
        attempt: int,
    ) -> str:
        """The Gemini Pass-3 verification prompt for one plate."""
        cited_rule_ids = list(plate.get("cites_identity_rules", []))
        cited_descriptions: list[str] = []
        for rule_id in cited_rule_ids:
            for entry in ir_entries:
                if entry.get("id") == rule_id:
                    cited_descriptions.append(
                        f"- **{rule_id}**: {entry.get('description', '')}"
                    )
                    break

        rules_block = (
            "\n".join(cited_descriptions)
            if cited_descriptions
            else "(no cited rules on this plate — verdict should be 'borderline')"
        )

        return (
            f"You are Cy's Pass 3 verifier — Gemini 3.1 Pro reading a Bible plate "
            f"to check whether it honors the identity rules Cy cited for it. "
            f"Attempt {attempt} of {_PLATE_ATTEMPT_CEILING}.\n\n"
            f"### Plate\n\n"
            f"Target path: `{plate.get('target_path', '?')}`\n"
            f"Source: `{plate.get('source', '?')}`\n\n"
            f"### Identity rules this plate cites\n\n"
            f"{rules_block}\n\n"
            f"### Your task\n\n"
            f"Look at the attached plate image. For each cited rule, judge "
            f"whether the plate honors the rule's description. Emit one JSON "
            f"envelope (no code fence is fine; the parser strips fences if present):\n\n"
            f'{{"verdict": "pass | borderline | fail", '
            f'"confidence": 0.0-1.0, '
            f'"reasoning": "Specific. Cite which rules were honored, which were borderline, which were violated.", '
            f'"cites_identity_rule": ["IR.x.y.z", ...]}}\n\n'
            f"Be specific in reasoning. 'The plate looks fine' is not useful. "
            f"Cite specific rule IDs in your reasoning when you can."
        )

    # ----- parsing -----

    def _parse_pass1_envelope(
        self,
        text: str,
        *,
        character_dir: Path,
        stub_fallback: bool,
    ) -> dict:
        """Parse the Pass-1 envelope. Tolerant of ```json``` code fences.

        Stub fallback: if invoke_opus_text returned the Maya-shaped stub
        (planning envelope, not a Cy envelope), substitute a deterministic
        Cy-shaped envelope built from the source-refs listing so the rest
        of the pipeline can exercise downstream paths during stub-only runs.
        """
        try:
            payload = _parse_json_envelope(text)
        except ValueError:
            payload = {}

        required_keys = (
            "character_yaml", "ir_entries", "risk_bible_md",
            "cy_confidence_notes_md", "plate_generation_plan",
        )
        if all(key in payload for key in required_keys):
            return payload

        # Stub-shape detected (or invalid payload). Build a deterministic
        # Cy envelope from what we can infer. character_id comes from the
        # folder name.
        if stub_fallback or not payload:
            return self._build_stub_envelope(character_dir)

        # Partial payload — surface specifically what was missing.
        missing = [k for k in required_keys if k not in payload]
        raise ValueError(
            f"Cy Pass-1 envelope missing required keys: {missing}. "
            f"Got: {sorted(payload)}"
        )

    def _build_stub_envelope(self, character_dir: Path) -> dict:
        """Deterministic Cy envelope for stub-fallback runs.

        Builds a minimal valid Bible from the folder name + whatever source-refs
        exist. Used when the underlying Opus call returned a stub (no real model
        available) so downstream pipeline paths still exercise. Production runs
        should never hit this path; tests run on the monkeypatched-Opus path.

        The style_register inference is folder-name-aware so the stub Bible
        for a pixel-art character (e.g. `claude-mascot/`) doesn't get the
        pencil-test-colored default the rest of the pipeline would silently
        coerce against. This is intentional-test-only — real Cy reads
        source-refs and infers the register from the material, not from the
        folder name.
        """
        character_id = character_dir.name
        stub_register = _infer_stub_style_register(character_id)
        ir_entries = [
            {
                "id": f"IR.{character_id}.style.stub-rule",
                "description": (
                    f"STUB FALLBACK — Opus was unavailable. Sean: review "
                    f"and replace this rule with real identity rules authored "
                    f"by Cy against the source-refs/ contents."
                ),
                "cites_phase": [5],
                "cites_personas": ["em"],
                "impact_tag": "aesthetic",
                "character_id": character_id,
                "derived_from": [f"characters/{character_id}/anchor.png"],
            }
        ]
        return {
            "character_yaml": {
                "character_id": character_id,
                "display_name": character_id.replace("-", " ").title(),
                "style_register": stub_register,
                "palette": [],
                "proportions": {"head_to_body": "", "shoulder_to_hip": "", "notes": ""},
                "identity_rules_pointer": "./acceptance_criteria.json",
                "cy_confidence_notes": "(STUB FALLBACK — see cy-confidence-notes.md)",
                "flux_lora_seed_plates": ["anchor.png"],
                "risks": "./risk-bible.md",
                "source_refs_consumed": [],
            },
            "ir_entries": ir_entries,
            "risk_bible_md": (
                f"## STUB FALLBACK\n\n"
                f"The {character_id} Bible was authored against a stub Opus call. "
                f"Real authoring requires a working Opus 4.7 connection. Sean: "
                f"re-run Cy with the SDK available before approving this Bible."
            ),
            "cy_confidence_notes_md": (
                f"## STUB FALLBACK\n\n"
                f"Cy could not author this Bible — the Opus call returned a stub. "
                f"Confidence is artificial. Do not approve."
            ),
            "plate_generation_plan": {"plates": []},
        }

    def _parse_gemini_verdict(self, text: str) -> dict:
        """Parse Gemini's Pass-3 verdict envelope. Tolerant of code fences."""
        try:
            payload = _parse_json_envelope(text)
        except ValueError:
            return {
                "verdict": "borderline",
                "confidence": 0.0,
                "reasoning": "Gemini's response could not be parsed as JSON.",
                "cites_identity_rule": [],
            }

        verdict = str(payload.get("verdict", "borderline")).lower().strip()
        if verdict not in {"pass", "borderline", "fail"}:
            verdict = "borderline"
        try:
            confidence = float(payload.get("confidence", 0.0))
        except (TypeError, ValueError):
            confidence = 0.0
        confidence = max(0.0, min(1.0, confidence))

        return {
            "verdict": verdict,
            "confidence": confidence,
            "reasoning": str(payload.get("reasoning", "")),
            "cites_identity_rule": list(payload.get("cites_identity_rule", []) or []),
        }

    # ----- plate orchestration -----

    def _run_plate(
        self,
        *,
        plate: dict,
        ir_entries: list[dict],
        character_dir: Path,
        cache_dir: Path,
    ) -> dict:
        """Run Pass 2 + Pass 3 for a single plate. Returns the plate status dict."""
        target_path = character_dir / plate["target_path"]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        source = str(plate.get("source", "generate"))
        cites_rules = tuple(plate.get("cites_identity_rules", []))
        prompt_text = str(plate.get("prompt", ""))
        # Opus is supposed to emit character-dir-relative paths per the
        # addendum's "What good looks like" example ("anchor.png", not
        # "characters/sean-anchor/anchor.png"). In practice the first
        # sean-anchor authoring run emitted project-root-relative paths
        # anyway, so resolve defensively: prefer character-dir, fall back
        # to project root if that doesn't exist (same pattern the ingest
        # path uses at the start of this function).
        reference_images = []
        for ref in plate.get("reference_images", []):
            if not ref:
                continue
            ref_path = Path(ref)
            candidate = character_dir / ref_path
            if not candidate.exists():
                fallback = _PROJECT_ROOT / ref_path
                if fallback.exists():
                    candidate = fallback
            reference_images.append(candidate)

        status: dict[str, Any] = {
            "status": "pending",
            "attempts": 0,
            "cache_hit": False,
        }

        # ----- Pass 2 — ingest or generate -----
        if source.startswith("ingest:"):
            source_rel = source[len("ingest:"):].split("#", 1)[0]
            source_full = (character_dir / source_rel).resolve()
            if not source_full.exists():
                # Try project root as fallback.
                source_full = (_PROJECT_ROOT / source_rel).resolve()
            if source_full.exists():
                shutil.copy2(source_full, target_path)
                status.update({"status": "ingested", "cache_hit": True, "attempts": 0})
            else:
                status.update({
                    "status": "ingest_source_missing",
                    "reasoning": f"source path {source_rel} did not resolve",
                })
                return status
        else:
            nb_resp = invoke_nb_pro(
                prompt=prompt_text,
                reference_images=reference_images,
                output_path=target_path,
                cache_dir=cache_dir,
                cites_identity_rules=cites_rules,
            )
            status.update({
                "status": "stub" if nb_resp.stub_fallback else "generated",
                "cache_hit": nb_resp.cache_hit,
                "attempts": 1,
                "cache_key": nb_resp.cache_key,
            })
            if not nb_resp.ok:
                status["status"] = "generation_failed"
                status["exit_code"] = nb_resp.exit_code
                return status

        # ----- Pass 3 — Gemini verifies (and regenerates on fail, up to ceiling) -----
        for attempt in range(1, _PLATE_ATTEMPT_CEILING + 1):
            verify_prompt = self._build_pass3_prompt(
                plate=plate,
                ir_entries=ir_entries,
                attempt=attempt,
            )
            gemini_resp = asyncio.run(run_antigravity_with_image(
                prompt=verify_prompt,
                image_paths=[target_path],
                timeout_s=_GEMINI_TIMEOUT_S,
            ))
            verdict_envelope = self._parse_gemini_verdict(gemini_resp.text)

            status["gemini_verdict"] = verdict_envelope["verdict"]
            status["gemini_confidence"] = verdict_envelope["confidence"]
            status["cites_identity_rule"] = verdict_envelope["cites_identity_rule"]
            status["reasoning"] = verdict_envelope["reasoning"]
            status["attempts"] = attempt

            if verdict_envelope["verdict"] in {"pass", "borderline"}:
                if status["status"] == "pending":
                    status["status"] = "verified"
                return status

            # verdict == "fail". Decide whether to regenerate.
            if attempt >= _PLATE_ATTEMPT_CEILING:
                status["status"] = "human_gate_required"
                return status

            if source.startswith("ingest:"):
                # Ingested plates can't regenerate — the pixel is Sean's source.
                # Surface immediately rather than burn Gemini calls.
                status["status"] = "human_gate_required"
                return status

            # Regenerate via NB Pro with the reject reason threaded in.
            nb_resp = invoke_nb_pro(
                prompt=prompt_text,
                reference_images=reference_images,
                output_path=target_path,
                cache_dir=cache_dir,
                cites_identity_rules=cites_rules,
                reject_reason=verdict_envelope["reasoning"],
            )
            if not nb_resp.ok:
                status["status"] = "regeneration_failed"
                status["exit_code"] = nb_resp.exit_code
                return status

        # Shouldn't reach here — the loop returns on every branch.
        return status

    # ----- contract enforcement -----

    def _enforce_clean_markdown(self, text: str, artifact_name: str) -> None:
        """Raise if `text` contains box-drawing characters.

        Mirrors PlannerNode's enforcement in pipeline/agents/planner.py:138-143.
        The CLI renders box-decorated tear sheets in `pipeline bible show`;
        Cy emits clean prose. Burning Opus tokens on ╔═╗ characters is a
        contract violation that pollutes every downstream consumer's context.
        """
        offending = _BOX_CHARACTERS & set(text)
        if offending:
            raise ValueError(
                f"Cy emitted box-drawing characters in {artifact_name}: "
                f"{sorted(offending)!r}. pipeline bible show renders boxes "
                f"in the CLI layer; Cy emits clean prose."
            )


# ---------- helpers ----------


def _parse_json_envelope(text: str) -> dict:
    """Strip a ```json``` code fence if present, then json.loads."""
    if not text.strip():
        raise ValueError("Empty response")
    match = _CODE_FENCE_RE.match(text.strip())
    body = match.group(1) if match else text
    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Response is not parseable JSON: {exc}") from exc


def _atomic_write_text(path: Path, content: str) -> None:
    """temp-then-rename atomic write. Mirrors the patch_stager idiom."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


# Folder-name heuristics for the stub fallback's style_register inference.
# Intentional-test-only: real Cy reads source-refs and infers the register
# from the material; this map exists so the stub Bible for a pixel-art
# character doesn't get the pencil-test-colored default the rest of the
# pipeline would silently coerce against. Extend conservatively; new entries
# are a deliberate commit, not an inline tweak.
_STUB_STYLE_REGISTER_BY_KEYWORD = {
    "mascot": "pixel-art-8bit",
    "pixel": "pixel-art-8bit",
    "watercolor": "watercolor",
    "lineart": "line-art-only",
    "photoreal": "photoreal",
    "3d": "3d-rendered",
}


def _infer_stub_style_register(character_id: str) -> str:
    """Guess a sensible style_register from the folder name for stub Bibles.

    The default remains pencil-test-colored because the Pencil-Test reference
    implementation is anima's first reference style and most existing character
    folders carry it. The folder-name match is conservative — a substring hit
    on a known keyword wins; anything else falls through to the default.
    """
    name = character_id.lower()
    for keyword, register in _STUB_STYLE_REGISTER_BY_KEYWORD.items():
        if keyword in name:
            return register
    return "pencil-test-colored"
