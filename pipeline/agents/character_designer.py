"""anima — Cy the Character Designer (Phase 2 AgentSpec).

Cy runs once per character. Three-phase loop with categorically different
model assignment per phase:

  Pass 1 — Opus 4.8 authors (text-only).
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
from pipeline.agents.similarity_gate import compute_similarity
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

# JSON code-fence finder. LLMs wrap structured output in ```json ... ```.
# Searched ANYWHERE in the text (not anchored to the whole string): Opus 4.8
# narrates around the envelope — "Here is the Pass 1 envelope:" before the
# fence and authoring notes after it — so a whole-string anchor silently fails
# to find the JSON and falls back to the synthetic stub (the live-re-bake bug).
_CODE_FENCE_RE = re.compile(r"```(?:json)?\s*\n?(.*?)```", re.DOTALL)

# Box-drawing characters forbidden in risk-bible.md + cy-confidence-notes.md.
# Same contract enforcement Maya applies to plan.md — the CLI renders boxes
# in `pipeline bible show`; Cy emits clean prose. Burning Opus tokens on
# box-drawing characters is a contract violation.
_BOX_CHARACTERS = frozenset("╔═╗║╚╝┌─┐│└┘├┤┬┴┼")

# Per-plate ceiling. Three attempts (initial + two regens) before surfacing
# the plate to the human gate. Mirrors Maya's three-call ceiling per plan,
# but per-plate scope since Cy may have many plates.
_PLATE_ATTEMPT_CEILING = 3

# Pass-1 call ceiling. Cy gets up to three Opus calls to produce a parseable
# envelope; a transient malformed emission (Opus 4.8 narration/truncation) is
# retried within this budget before falling back to the loud stub. A missing
# SDK or a contract violation is NOT retried (see _author_pass1).
_PASS1_CALL_CEILING = 3

# Subdirectories under characters/{id}/ that hold Cy-generated (or
# ingest-target) plates. A `generate` plate must NEVER reference another plate
# in these directories — that is the reference-chaining anti-pattern that
# compounded identity drift (visual-fidelity post-mortem §3d: head-3quarter
# chained off the already-drifted head-front, expressions chained off neutral).
# Legitimate references for a generate plate come from anchor.png + source-refs/
# only. The runner is the source of truth here regardless of what Opus emits.
_GENERATED_PLATE_DIRS = frozenset(
    {"turnarounds", "expressions", "props", "motion_plates", "costumes"}
)

# Subdirectories whose plates are ISOLATED OBJECTS, not the character. A prop
# plate (the stylus, etc.) must NOT get the full-body anchor injected — doing so
# tells NB Pro to draw the whole person beside a floating prop (the re-baked
# props/stylus.png defect). Prop plates also skip the Pass-2.5 anchor-similarity
# gate entirely: scored against a full-character anchor they always land near
# zero, which would spuriously reject/regenerate a perfectly good object plate.
_PROP_PLATE_DIRS = frozenset({"props"})

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

        # ---------- Pass 1 — author OR load an approved Bible ----------
        # A locked Bible (or an explicit plates_only request) must NOT be
        # re-authored. The director approved those rules and the committed
        # plate_generation_plan.json carries hand-curated ingest sources and
        # prompts (trimmed stylus, manual body-turnaround crops). Re-running
        # Opus Pass 1 would overwrite both and flip locked back to false. So in
        # that case we LOAD the on-disk Bible and run Passes 2+3 against it —
        # a plates-only bake that honors the approval.
        character_yaml_path = character_dir / "character.yaml"
        criteria_path = character_dir / "acceptance_criteria.json"
        risk_bible_path = character_dir / "risk-bible.md"
        confidence_notes_path = character_dir / "cy-confidence-notes.md"
        plate_plan_path = character_dir / "plate_generation_plan.json"

        if self._resolve_plates_only(ctx, character_dir):
            character_yaml, ir_entries, plate_plan = self._load_existing_bible(
                character_dir
            )
            pass1_stub = False
        else:
            (
                character_yaml,
                ir_entries,
                risk_bible_md,
                cy_confidence_notes_md,
                plate_plan,
                pass1_stub,
            ) = self._author_pass1(ctx, character_dir)

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

        # Persist the per-plate verdict trail. The 2026-05-28 run left no
        # durable per-plate signal (post-mortem §2.3); this writes one JSONL
        # line per plate carrying the Pass-2.5 similarity score next to
        # Gemini's prose verdict, so a drift Gemini passed is visible after
        # the fact from disk.
        self._persist_plate_verdicts(ctx.run_dir, plate_results)

        # ---------- Collect cites_criteria + return ----------
        cites = [entry["id"] for entry in ir_entries]
        human_gate_count = sum(
            1 for v in plate_results.values()
            if v.get("status") == "human_gate_required"
        )
        notes = (
            f"cy@phase_2 character_id={character_yaml.get('character_id', '?')!r} "
            f"plates={len(plate_results)} human_gate_required={human_gate_count} "
            f"pass1_stub={pass1_stub}"
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

    # ----- Pass 1 — author vs. load -----

    def _resolve_plates_only(self, ctx: AgentContext, character_dir: Path) -> bool:
        """Decide whether this run bakes plates against an existing Bible
        (skipping Pass 1) or authors a fresh one.

        Plates-only is triggered by EITHER an explicit ctx.inputs['plates_only']
        OR a locked acceptance_criteria.json on disk. The locked auto-detect is
        the safety net: an approved Bible must never be silently re-authored,
        even if the caller forgets the flag."""
        if ctx.inputs.get("plates_only"):
            return True
        criteria_path = character_dir / "acceptance_criteria.json"
        if criteria_path.exists():
            try:
                payload = json.loads(criteria_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                return False
            if payload.get("locked"):
                return True
        return False

    def _load_existing_bible(self, character_dir: Path) -> tuple[dict, list[dict], dict]:
        """Load an already-authored Bible from disk for a plates-only bake.

        Returns (character_yaml, ir_entries, plate_plan). Raises FileNotFoundError
        if the Bible was never authored (no criteria / no plate plan) — a
        plates-only bake has nothing to bake against in that case."""
        criteria_path = character_dir / "acceptance_criteria.json"
        plate_plan_path = character_dir / "plate_generation_plan.json"
        if not criteria_path.exists():
            raise FileNotFoundError(
                f"plates-only bake requested but no acceptance_criteria.json at "
                f"{criteria_path}. Author the Bible first (run without --plates-only)."
            )
        if not plate_plan_path.exists():
            raise FileNotFoundError(
                f"plates-only bake requested but no plate_generation_plan.json at "
                f"{plate_plan_path}. Author the Bible first (run without --plates-only)."
            )
        criteria_json = json.loads(criteria_path.read_text(encoding="utf-8"))
        ir_entries = list(criteria_json.get("criteria", []))
        plate_plan = json.loads(plate_plan_path.read_text(encoding="utf-8"))
        character_yaml: dict = {}
        character_yaml_path = character_dir / "character.yaml"
        if character_yaml_path.exists():
            try:
                character_yaml = yaml.safe_load(
                    character_yaml_path.read_text(encoding="utf-8")
                ) or {}
            except yaml.YAMLError:
                character_yaml = {}
        return character_yaml, ir_entries, plate_plan

    def _author_pass1(
        self, ctx: AgentContext, character_dir: Path
    ) -> tuple[dict, list[dict], str, str, dict, bool]:
        """Pass 1 — Opus authors the five-artifact envelope.

        Retries on a transient PARSE FAILURE (the SDK ran but returned empty or
        unparseable text — the Opus 4.8 narration/truncation case) up to the
        three-call budget, auto-healing what previously required a human re-run.
        Does NOT retry: a missing SDK (stub_fallback — deterministic, not
        transient) or a CONTRACT VIOLATION (parseable JSON missing required
        keys — `_parse_pass1_envelope` raises ValueError, which propagates as a
        real rejection).

        Returns (character_yaml, ir_entries, risk_bible_md, cy_confidence_notes_md,
        plate_plan, pass1_stub). The caller enforces clean markdown, validates +
        writes the criteria, and writes the artifacts."""
        studio_brief = str(ctx.inputs.get("studio_brief", ""))
        opus_prompt = self._build_pass1_prompt(
            studio_brief=studio_brief,
            character_dir=character_dir,
        )

        parsed: dict = {}
        for attempt in range(1, _PASS1_CALL_CEILING + 1):
            # 1800s timeout for Cy's Pass-1: the prompt is ~55KB (anima preamble
            # + Cy addendum + 2d-animation-principles skill inline + per-Bible
            # brief) and the envelope is ~50KB. Observed wall time against real
            # Opus 4.7: ~500s. The 2026-05-29 Opus 4.8 bump pushed Pass-1 past
            # the previous 900s ceiling (4.8 spends more on extended thinking);
            # a real re-bake hit the 900s wall and silently stubbed. Raised to
            # 1800s with headroom. The invoke_opus_text default of 120s would
            # cleanly time out before Pass 1 ever completed.
            opus_resp = asyncio.run(invoke_opus_text(prompt=opus_prompt, timeout_s=1800))

            sdk_absent = bool(getattr(opus_resp, "stub_fallback", False))
            resp_problem = (
                sdk_absent
                or getattr(opus_resp, "exit_code", 0) != 0
                or not (opus_resp.text or "").strip()
            )
            # _parse_pass1_envelope returns a synthetic stub (with _pass1_stub)
            # for empty / unparseable output, and RAISES ValueError for a
            # parseable-but-incomplete envelope (a contract violation that must
            # not be retried — let it propagate).
            parsed = self._parse_pass1_envelope(
                opus_resp.text,
                character_dir=character_dir,
                stub_fallback=sdk_absent,
            )
            pass1_stub = resp_problem or bool(parsed.get("_pass1_stub"))

            if not pass1_stub:
                # Real envelope on this attempt — done.
                break
            if sdk_absent or attempt == _PASS1_CALL_CEILING:
                # A missing SDK is deterministic (retrying can't help), and on
                # the final attempt the budget is spent — return the loud stub.
                break
            # Otherwise the SDK ran but produced empty/unparseable output — a
            # transient malformation. Loop and retry within the budget.

        pass1_stub = (
            bool(getattr(opus_resp, "stub_fallback", False))
            or getattr(opus_resp, "exit_code", 0) != 0
            or not (opus_resp.text or "").strip()
            or bool(parsed.get("_pass1_stub"))
        )

        return (
            parsed["character_yaml"],
            parsed["ir_entries"],
            parsed["risk_bible_md"],
            parsed["cy_confidence_notes_md"],
            parsed["plate_generation_plan"],
            pass1_stub,
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
            # Marker so run() can tell a synthetic stub envelope apart from a
            # real Opus emission, regardless of WHY we stubbed (timeout → empty
            # text, no SDK, OR non-empty-but-unparseable output). The first
            # live re-bake stubbed via the last case and slipped past a guard
            # that only checked the Opus response fields.
            "_pass1_stub": True,
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
        plate_intent = str(plate.get("prompt", ""))
        # Reference resolution is now the RUNNER's call, not a faithful
        # pass-through of whatever Opus emitted (post-mortem §3d). For a
        # generate plate the runner unconditionally seeds anchor.png first,
        # keeps only source-refs/ angle targets, and strips any reference to
        # another generated plate (no chaining). For an ingest plate there are
        # no references — the pixel is Sean's own source.
        reference_images, has_pose_ref, is_prop = _resolve_generate_references(
            plate, character_dir
        )
        # Wrap the plate's short intent in the role-tag framing NB Pro responds
        # to (Phase 0 proved a terse "match the anchor exactly" prompt recovers
        # identity). The verbose verbal character-descriptions are gone; the
        # runner owns the framing so a too-wordy Opus prompt can't reintroduce
        # prompt-dominance, and the anti-caption guardrail kills the stylus.png
        # caption failure mode (§3b). A prop plate uses the isolated-object
        # framing instead — no anchor was fed, so a "match Image 1" prompt would
        # be incoherent and would re-invite the floating-figure defect.
        if is_prop:
            prompt_text = _build_prop_prompt(plate_intent)
        else:
            prompt_text = _build_nb_pro_prompt(plate_intent, has_pose_ref=has_pose_ref)

        status: dict[str, Any] = {
            "status": "pending",
            "attempts": 0,
            "cache_hit": False,
        }

        # ----- Pass 2 — ingest or generate -----
        if source.startswith("ingest:"):
            source_rel = source[len("ingest:"):].split("#", 1)[0]
            region_name = None
            if "#region:" in source:
                region_name = source.split("#region:", 1)[1].split("#", 1)[0].strip()
            source_full = (character_dir / source_rel).resolve()
            if not source_full.exists():
                # Try project root as fallback.
                source_full = (_PROJECT_ROOT / source_rel).resolve()
            if source_full.exists():
                # Honor a #region:NAME crop when a <sheet>.regions.json sidecar
                # defines it (post-mortem §2.1 — the suffix used to be ignored
                # and the whole sheet copied). Fall back to a full copy + a loud
                # flag when the region can't be mapped, never a silent wrong crop.
                cropped = False
                if region_name:
                    cropped = _crop_region(source_full, region_name, target_path)
                if not cropped:
                    shutil.copy2(source_full, target_path)
                    if region_name:
                        status["region_not_cropped"] = region_name
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

        # ----- Pass 2.5 — pixel-similarity gate -----
        # Score the plate's identity similarity against the anchor BEFORE
        # Gemini's prose pass, so a plate that satisfies the rule descriptions
        # but doesn't look like the character is surfaced numerically rather
        # than masked (post-mortem §2.3). Recorded, not hard-blocked — see
        # similarity_gate for why the coarse PIL metric is a flag this commit.
        self._score_plate_identity(target_path, character_dir, status, is_prop=is_prop)

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

            # Re-score the freshly regenerated plate against the anchor.
            self._score_plate_identity(target_path, character_dir, status, is_prop=is_prop)

        # Shouldn't reach here — the loop returns on every branch.
        return status

    def _score_plate_identity(
        self, target_path: Path, character_dir: Path, status: dict,
        *, is_prop: bool = False,
    ) -> None:
        """Compute + record the Pass-2.5 similarity of a plate vs the anchor.

        Mutates `status` in place with similarity_score / similarity_method /
        similarity_reference, and similarity_flag='below_threshold' when the
        score is low. Never raises — a scoring failure must not fail a plate
        (the gate is a signal, not a blocker this commit).

        Prop plates are an EXCEPTION: an isolated object scored against the
        full-character anchor always lands near zero, so the score is recorded
        for a complete audit trail but the gate is marked record-only and the
        below-threshold reject flag is never set — a prop is never identity-
        scored against the character anchor."""
        anchor_path = character_dir / "anchor.png"
        if not target_path.exists() or not anchor_path.exists():
            return
        try:
            sim = compute_similarity(target_path, anchor_path)
        except Exception as exc:  # pragma: no cover - defensive
            status["similarity_error"] = str(exc)[:200]
            return
        status["similarity_score"] = round(sim.score, 4)
        status["similarity_method"] = sim.method
        status["similarity_reference"] = "anchor.png"
        if is_prop:
            status["similarity_gate"] = "record-only (prop plate — not identity-scored)"
            return
        if sim.below_threshold:
            status["similarity_flag"] = "below_threshold"

    def _persist_plate_verdicts(
        self, run_dir: Path, plate_results: dict[str, dict]
    ) -> None:
        """Write runs/{run_id}/plate_verdicts.jsonl — one line per plate.

        Each record is the plate's status dict plus its target_path, so the
        similarity score, Gemini verdict, confidence, cited rules, and attempt
        count are all reconstructable from disk after the run."""
        run_dir = Path(run_dir)
        run_dir.mkdir(parents=True, exist_ok=True)
        out = run_dir / "plate_verdicts.jsonl"
        lines = [
            json.dumps({"target_path": target_path, **status}, sort_keys=True)
            for target_path, status in plate_results.items()
        ]
        _atomic_write_text(out, "\n".join(lines) + ("\n" if lines else ""))

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
    """Extract a JSON object from an LLM response, tolerant of prose.

    Conversational models (Opus 4.8 especially) narrate around the structured
    output — preamble before the fence, authoring notes after it. The ladder:
      1. The first ```json ... ``` fenced block anywhere in the text.
      2. The whole (stripped) text as raw JSON.
      3. The first balanced-brace {...} object embedded in the text.
    Raises ValueError only if all three fail.
    """
    if not text.strip():
        raise ValueError("Empty response")

    # 1. Fenced block anywhere in the text (not anchored to the whole string).
    for m in _CODE_FENCE_RE.finditer(text):
        candidate = m.group(1).strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue

    # 2. Whole text as raw JSON.
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass

    # 3. First balanced-brace object embedded in surrounding prose.
    obj = _extract_first_json_object(text)
    if obj is not None:
        return obj

    raise ValueError("Response is not parseable JSON (no fence, raw, or object found)")


def _extract_first_json_object(text: str) -> dict | None:
    """Return the first balanced-brace {...} object that json.loads accepts.

    Scans for a '{', tracks brace depth (ignoring braces inside JSON strings,
    honoring backslash escapes), and attempts json.loads on each balanced span.
    Returns None if no decodable object is found.
    """
    start = None
    depth = 0
    in_string = False
    escaped = False
    for i, ch in enumerate(text):
        if start is None:
            if ch == "{":
                start = i
                depth = 1
                in_string = False
                escaped = False
            continue
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                candidate = text[start:i + 1]
                try:
                    return json.loads(candidate)
                except json.JSONDecodeError:
                    # Not valid — restart the search after this opening brace.
                    start = None
    return None


def _region_box(
    source_path: Path, region_name: str
) -> tuple[float, float, float, float] | None:
    """Look up a `#region:NAME` crop box from a `<sheet>.regions.json` sidecar.

    The sidecar lives beside the source sheet (e.g. turnaround-1.png →
    turnaround-1.regions.json) and maps region name → [left, top, right, bottom].
    Values ≤ 1.0 are treated as fractions of the sheet; larger values as pixels.
    Returns None when the sidecar or the named region is absent — the caller
    then falls back to a full copy and flags it, rather than silently shipping
    a wrong crop (post-mortem §2.1: the #region suffix used to be ignored and
    the whole sheet copied as if it were the cropped region).
    """
    sidecar = source_path.with_name(source_path.stem + ".regions.json")
    if not sidecar.exists():
        return None
    try:
        mapping = json.loads(sidecar.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    box = mapping.get(region_name)
    if not isinstance(box, (list, tuple)) or len(box) != 4:
        return None
    try:
        return tuple(float(v) for v in box)  # type: ignore[return-value]
    except (TypeError, ValueError):
        return None


def _crop_region(source_path: Path, region_name: str, target_path: Path) -> bool:
    """Crop `source_path` to `region_name` (per the sidecar) and save to target.

    Returns True if the crop executed, False if no box was found (caller copies
    the whole sheet and flags it). Fractional boxes scale to the sheet's pixel
    size; pixel boxes are used as-is.
    """
    box = _region_box(source_path, region_name)
    if box is None:
        return False
    from PIL import Image

    img = Image.open(source_path)
    w, h = img.size
    left, top, right, bottom = box
    if max(box) <= 1.0:
        crop_box = (round(left * w), round(top * h), round(right * w), round(bottom * h))
    else:
        crop_box = (round(left), round(top), round(right), round(bottom))
    target_path.parent.mkdir(parents=True, exist_ok=True)
    img.crop(crop_box).save(target_path)
    return True


def _classify_reference(ref: str, character_dir: Path) -> tuple[Path | None, str]:
    """Resolve one plate reference string and classify it.

    Returns (resolved_path | None, kind) where kind is one of:
      'anchor'     — the character's anchor.png (the canonical identity ref)
      'source_ref' — material under source-refs/ (Sean's hand-drawn input)
      'generated'  — a plate under a _GENERATED_PLATE_DIRS subdir (NEVER a
                     valid reference for a generate plate — chaining)
      'external'   — resolves on disk but lives outside the character folder
      'missing'    — could not resolve on disk

    Opus has historically emitted both character-dir-relative ("anchor.png")
    and project-root-relative ("characters/sean-anchor/anchor.png") paths, so
    resolution tries character_dir first, then project root.
    """
    if not ref:
        return None, "missing"
    ref_path = Path(ref)
    candidate = character_dir / ref_path
    if not candidate.exists():
        fallback = _PROJECT_ROOT / ref_path
        candidate = fallback if fallback.exists() else candidate
    if not candidate.exists():
        return None, "missing"

    resolved = candidate.resolve()
    try:
        rel = resolved.relative_to(character_dir.resolve())
    except ValueError:
        return resolved, "external"

    if rel == Path("anchor.png"):
        return resolved, "anchor"
    if rel.parts and rel.parts[0] == "source-refs":
        return resolved, "source_ref"
    if rel.parts and rel.parts[0] in _GENERATED_PLATE_DIRS:
        return resolved, "generated"
    return resolved, "external"


def _is_prop_plate(plate: dict) -> bool:
    """True when the plate is an isolated-object (prop) plate, not the character.

    Identified by target_path landing under a _PROP_PLATE_DIRS subdir
    (props/). Prop plates skip anchor injection and the identity-similarity gate
    — a full-body anchor is the wrong reference for an isolated object.
    """
    target = str(plate.get("target_path", ""))
    head = target.split("/", 1)[0] if "/" in target else ""
    return head in _PROP_PLATE_DIRS


def _resolve_generate_references(
    plate: dict, character_dir: Path
) -> tuple[list[Path], bool, bool]:
    """Build the reference list a generate plate is actually fed.

    The runner — not Opus — owns this. Policy (post-mortem §3d + §5 item 2):
      1. anchor.png is ALWAYS first, injected unconditionally — EXCEPT for prop
         plates, where the full-body anchor is the wrong reference (it makes
         NB Pro draw the whole figure beside a floating object).
      2. source-refs/ material Opus named (the angle/pose target) is kept.
      3. references to other generated plates are STRIPPED (no chaining).

    Returns (ordered_deduped_paths, has_pose_ref, is_prop) where has_pose_ref is
    True when at least one non-anchor reference survived (so the prompt can name
    it as the angle/pose target), and is_prop signals the prop-plate class so
    the caller picks the isolated-object prompt + record-only similarity gate.
    """
    is_prop = _is_prop_plate(plate)
    refs: list[Path] = []
    seen: set[Path] = set()

    if not is_prop:
        anchor_path, anchor_kind = _classify_reference("anchor.png", character_dir)
        if anchor_kind == "anchor" and anchor_path is not None:
            refs.append(anchor_path)
            seen.add(anchor_path)

    has_pose_ref = False
    for raw in plate.get("reference_images", []):
        path, kind = _classify_reference(str(raw), character_dir)
        # For a prop plate the anchor is dropped too (it's the character, not
        # the object); only genuine source-ref/external object refs survive.
        if kind == "anchor" and is_prop:
            continue
        if kind in {"source_ref", "external"} and path is not None and path not in seen:
            refs.append(path)
            seen.add(path)
            has_pose_ref = True
        # 'anchor' already injected (non-prop); 'generated' dropped (no
        # chaining); 'missing' skipped.
    return refs, has_pose_ref, is_prop


def _build_nb_pro_prompt(plate_intent: str, *, has_pose_ref: bool) -> str:
    """Wrap a plate's short intent in NB Pro reference-role-tag framing.

    Phase 0 of the fidelity fix proved that a terse "redraw this exact
    character" prompt against the anchor recovers identity, where verbose
    verbal character descriptions drove prompt-dominance drift. This builds
    that terse framing around whatever short intent Cy authored, and forbids
    rendering text/captions (the props/stylus.png caption failure, §3b).
    """
    lines = [
        "Image 1 is the identity anchor — the canonical reference for this "
        "character. Match the face, hair, color palette, skin tone, and "
        "proportions in Image 1 exactly. Keep the full color of Image 1.",
    ]
    if has_pose_ref:
        lines.append(
            "Image 2 is the angle/pose target — match its viewing angle and "
            "pose, but the identity always comes from Image 1."
        )
    intent = plate_intent.strip() or "a clean reference plate of this character"
    lines.append(f"Render: {intent}.")
    lines.append(
        "The character must stay recognizably identical to Image 1. Do not "
        "add any text, labels, captions, annotations, or watermarks to the image."
    )
    return " ".join(lines)


def _build_prop_prompt(plate_intent: str) -> str:
    """Frame a prop plate as an isolated object — no figure, no text.

    A prop plate (the stylus, etc.) is an object reference, not the character.
    The full-body anchor is deliberately NOT fed (see _resolve_generate_references),
    so the prompt must not invite a figure: NB Pro otherwise draws the whole
    person beside a floating object (the re-baked props/stylus.png defect). The
    anti-text clause is the same guardrail the character prompt carries,
    strengthened here because the original stylus plate rendered its meta-prose
    as handwritten captions (post-mortem §3b)."""
    intent = plate_intent.strip() or "a single isolated prop object"
    return (
        "Render ONLY the isolated object described below, centered on a warm "
        "cream paper background. Do NOT draw any person, character, hand, body, "
        "or figure. Do NOT render any text, caption, label, handwriting, or "
        "annotation anywhere in the image. "
        f"Render: {intent}."
    )


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
