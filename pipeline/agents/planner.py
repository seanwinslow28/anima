"""anima — Maya the line producer. Phase 0 planner.

Maya runs once per piece. Three-phase loop:
  1. Opus 4.7 primary  — read briefs + manifest, draft plan + criteria graph.
  2. Sonnet 4.6 adversarial validation  — find one untestable criterion, one
     under-estimated cost line, or one wrong impact_tag. Or flag low-signal.
  3. Resolution  — revise on real flag; ship on clean+confident; second-Opus
     pass on low-signal. Three-call ceiling per plan, enforced.

Per v2 brainstorm-v2 §6: Maya is Opus 4.7 primary → Sonnet 4.6 validation
→ human gate at 90% confidence. Per Maya brainstorm TOP-5: the Sonnet pass
is adversarial, not echo confirmation — the cheap-judge defense ladder from
synthesis §1.5 (sycophancy at 58.19% baseline, self-preference bias up to
+90%, miscalibrated confidence) applied at the planning layer.

Four artifacts emitted into briefs/{date}-{slug}/:
  - 01_production_brief.md   (Maya-drafted, Sean-edited before approval)
  - acceptance_criteria.json (v1.1 graph schema, locked after approval)
  - plan.md                  (clean markdown — no box-drawing characters;
                              pipeline plan show renders ASCII boxes in the
                              CLI layer, not in the artifact)
  - cost_estimate            (in-memory RunCostEstimate from CostEstimatorNode;
                              surfaced into plan.md's Cost preview section)
"""

from __future__ import annotations

import asyncio
import json
import re
from pathlib import Path
from typing import Any, ClassVar

from pipeline.agents import (
    AgentContext,
    AgentResult,
    CostEstimate,
    NODE_REGISTRY,
    register_node,
)
from pipeline.agents.sdk_runners import invoke_opus_text, invoke_sonnet_text

PROMPTS_DIR = Path(__file__).parent / "prompts"
ANIMA_PREAMBLE_FILE = PROMPTS_DIR / "anima-standing-context.md"
MAYA_ADDENDUM_FILE = PROMPTS_DIR / "maya-planner-context.md"

# JSON code-fence stripper. LLMs habitually wrap structured output in
# ```json ... ```; both parsers tolerate it.
_CODE_FENCE_RE = re.compile(r"^\s*```(?:json)?\s*\n?(.*?)\n?\s*```\s*$", re.DOTALL)

# Box-drawing characters Maya must never emit in plan.md. The pipeline plan
# show CLI renders these from Maya's clean prose; emitting them inline burns
# Opus tokens on rendering and pollutes downstream consumers' context windows.
_BOX_CHARACTERS = frozenset("╔═╗║╚╝┌─┐│└┘├┤┬┴┼")


@register_node("planner")
class PlannerNode:
    """Maya — line producer. Phase 0 planner."""

    name: ClassVar[str] = "planner"
    inputs: ClassVar[dict[str, type]] = {"brief_dir": str}
    outputs: ClassVar[dict[str, type]] = {
        "plan_path": str,
        "criteria_path": str,
        "production_brief_path": str,
        "cost_estimate": dict,
    }
    cites_criteria: ClassVar[list[str]] = []

    def cost_estimate(self, ctx: AgentContext) -> CostEstimate:
        # Subscription-absorbed via Sean's Anthropic Pro plan. ~3 minutes of
        # wall-clock for the full three-call loop in production.
        return CostEstimate(usd=0.0, latency_s=180.0, confidence=0.85)

    def run(self, ctx: AgentContext) -> AgentResult:
        brief_dir = Path(ctx.inputs["brief_dir"])
        studio_brief_path = brief_dir / "00_studio_brief.md"
        if not studio_brief_path.exists():
            raise FileNotFoundError(
                f"Studio Brief not found at {studio_brief_path}. "
                f"Run `python -m pipeline.cli plan init --target {brief_dir}` first."
            )
        studio_brief = studio_brief_path.read_text(encoding="utf-8")
        manifest = ctx.manifest

        # Cost preview comes from CostEstimatorNode — Maya never invents prices.
        cost_node = NODE_REGISTRY["cost_estimator"]()
        cost_result = cost_node.run(ctx)
        cost_estimate = cost_result.outputs["estimate"]

        counts = {"opus": 0, "sonnet": 0}

        # Pass 1 — Opus primary.
        opus_prompt = self._build_opus_prompt(studio_brief, manifest, cost_estimate)
        opus_resp = asyncio.run(invoke_opus_text(prompt=opus_prompt))
        counts["opus"] += 1
        parsed = self._parse_opus(opus_resp.text)
        production_brief_md: str = parsed["production_brief_md"]
        criteria_json: dict = parsed["criteria_json"]
        plan_md: str = parsed["plan_md"]

        # Pass 2 — Sonnet adversarial validation.
        sonnet_prompt = self._build_sonnet_prompt(plan_md, criteria_json, cost_estimate)
        sonnet_resp = asyncio.run(invoke_sonnet_text(prompt=sonnet_prompt))
        counts["sonnet"] += 1
        sonnet_parsed = self._parse_sonnet(sonnet_resp.text)

        # Pass 3 — Resolution.
        unresolved_concern: str | None = None
        if sonnet_parsed.get("flag"):
            # Real flag — revise via second Opus.
            revision_prompt = self._build_revision_prompt(
                plan_md, criteria_json, sonnet_parsed["flag"]
            )
            revision_resp = asyncio.run(invoke_opus_text(prompt=revision_prompt))
            counts["opus"] += 1
            revised = self._parse_opus(revision_resp.text)
            plan_md = revised["plan_md"]
            criteria_json = revised["criteria_json"]
            production_brief_md = revised.get("production_brief_md", production_brief_md)
        elif sonnet_parsed.get("low_signal"):
            # Low-signal — second Opus acts as validator.
            second_opus_resp = asyncio.run(invoke_opus_text(prompt=sonnet_prompt))
            counts["opus"] += 1
            second_parsed = self._parse_sonnet(second_opus_resp.text)
            if second_parsed.get("flag"):
                unresolved_concern = second_parsed["flag"]
        # Else: clean + confident — ship as-is to the human gate.

        total_calls = counts["opus"] + counts["sonnet"]
        if total_calls > 3:
            raise RuntimeError(
                f"Three-call ceiling exceeded: opus={counts['opus']} sonnet={counts['sonnet']}"
            )

        # Contract enforcement: plan.md must be clean markdown — no box chars.
        offending = _BOX_CHARACTERS & set(plan_md)
        if offending:
            raise ValueError(
                f"Maya emitted box-drawing characters in plan.md: {sorted(offending)!r}. "
                f"pipeline plan show renders boxes in the CLI layer; Maya emits clean prose."
            )

        # Inject unresolved concern as a confidence note (no fourth model call).
        if unresolved_concern:
            plan_md = self._inject_confidence_note(plan_md, unresolved_concern)

        # Write artifacts atomically (temp-then-rename per the patch_stager idiom).
        brief_dir.mkdir(parents=True, exist_ok=True)
        production_brief_path = brief_dir / "01_production_brief.md"
        _atomic_write(production_brief_path, production_brief_md)

        criteria_path = brief_dir / "acceptance_criteria.json"
        _atomic_write(criteria_path, json.dumps(criteria_json, indent=2))

        plan_path = brief_dir / "plan.md"
        _atomic_write(plan_path, plan_md)

        cited = [c.get("id", "") for c in criteria_json.get("criteria", []) if c.get("id")]
        notes = (
            f"maya@phase_0 calls={total_calls} (opus={counts['opus']} sonnet={counts['sonnet']})"
        )
        if unresolved_concern:
            notes += " unresolved_concern_in_plan_md"

        return AgentResult(
            outputs={
                "plan_path": str(plan_path),
                "criteria_path": str(criteria_path),
                "production_brief_path": str(production_brief_path),
                "cost_estimate": {
                    "low_usd": cost_estimate.low_usd,
                    "median_usd": cost_estimate.median_usd,
                    "high_usd": cost_estimate.high_usd,
                    "by_phase": dict(cost_estimate.by_phase),
                },
            },
            tier=ctx.tier,
            cites_criteria=cited,
            notes=notes,
        )

    # ----- prompt builders -----

    def _build_opus_prompt(
        self,
        studio_brief: str,
        manifest: dict,
        cost_estimate: Any,
    ) -> str:
        return "\n\n".join([
            self._load_anima_preamble(),
            self._load_maya_addendum(),
            self._per_invocation_brief(studio_brief, manifest, cost_estimate, pass_name="primary"),
        ])

    def _build_sonnet_prompt(
        self,
        plan_md: str,
        criteria_json: dict,
        cost_estimate: Any,
    ) -> str:
        return "\n\n".join([
            self._load_anima_preamble(),
            self._load_maya_addendum(),
            (
                "## Pass 2 — adversarial validation\n\n"
                "You are now in the Sonnet validation pass. Maya's primary Opus pass "
                "produced the plan + criteria + cost estimate below. Your job is "
                "adversarial — find ONE specific problem:\n\n"
                "  - one criterion that's untestable (vague, unmeasurable, or "
                "interpretive without grounding), or\n"
                "  - one cost line that's under-estimated by 2x or more given the "
                "manifest, or\n"
                "  - one impact_tag that's wrong (e.g., marked 'aesthetic' but should "
                "be 'identity_critical').\n\n"
                "If you find one, return:\n"
                "```json\n"
                "{\"flag\": \"<criterion-id or cost-line or impact-tag> — <one-sentence explanation>\"}\n"
                "```\n\n"
                "If you genuinely cannot find one, return:\n"
                "```json\n"
                "{\"flag\": null, \"low_signal\": true}\n"
                "```\n\n"
                "so the escalation hatch fires a second-Opus pass. Do not return "
                "`{\"flag\": null, \"low_signal\": false}` unless you'd stake your "
                "judgment that the plan is genuinely clean.\n\n"
                f"### Plan\n\n{plan_md}\n\n"
                f"### Criteria\n\n```json\n{json.dumps(criteria_json, indent=2)}\n```\n\n"
                f"### Cost estimate\n\nlow: ${cost_estimate.low_usd:.2f} / "
                f"median: ${cost_estimate.median_usd:.2f} / "
                f"high: ${cost_estimate.high_usd:.2f}"
            ),
        ])

    def _build_revision_prompt(
        self,
        plan_md: str,
        criteria_json: dict,
        flag: str,
    ) -> str:
        return "\n\n".join([
            self._load_anima_preamble(),
            self._load_maya_addendum(),
            (
                "## Pass 3 — revision\n\n"
                "The Sonnet adversarial pass surfaced a real flag. Revise the plan "
                "and criteria to address it. Emit the same three-key JSON envelope "
                "as the primary pass — production_brief_md, criteria_json, plan_md. "
                "Address the flag explicitly in plan.md's confidence notes.\n\n"
                f"### Sonnet's flag\n\n{flag}\n\n"
                f"### Current plan\n\n{plan_md}\n\n"
                f"### Current criteria\n\n```json\n{json.dumps(criteria_json, indent=2)}\n```"
            ),
        ])

    def _per_invocation_brief(
        self,
        studio_brief: str,
        manifest: dict,
        cost_estimate: Any,
        *,
        pass_name: str,
    ) -> str:
        # Surface only the manifest blocks Maya needs — generation.routing,
        # phases, tiering — instead of dumping the whole file.
        manifest_excerpt = {
            "generation": manifest.get("generation", {}),
            "phases": manifest.get("phases", {}),
            "tiering": manifest.get("tiering", {}),
            "critics": manifest.get("critics", {}),
        }
        return (
            f"## Pass 1 — primary planning\n\n"
            f"Read the Studio Brief, the manifest excerpt, and the cost estimate "
            f"below. Draft:\n\n"
            f"  1. The Production Brief (markdown + YAML frontmatter).\n"
            f"  2. The acceptance_criteria.json (v1.1 graph schema — mnemonic IDs, "
            f"cites_phase, cites_personas, impact_tag, parent_id, derived_from).\n"
            f"  3. The plan.md (clean markdown — no box-drawing characters; the CLI "
            f"renders those).\n\n"
            f"Emit one JSON object with these three keys wrapped in a ```json "
            f"code fence:\n\n"
            f"```json\n"
            f"{{\n"
            f'  "production_brief_md": "...",\n'
            f'  "criteria_json": {{"version": "1.1", "locked": false, "criteria": [...]}},\n'
            f'  "plan_md": "..."\n'
            f"}}\n"
            f"```\n\n"
            f"### Studio Brief\n\n{studio_brief}\n\n"
            f"### Manifest excerpt\n\n```yaml\n{json.dumps(manifest_excerpt, indent=2)}\n```\n\n"
            f"### Cost estimate\n\nlow: ${cost_estimate.low_usd:.2f} / "
            f"median: ${cost_estimate.median_usd:.2f} / "
            f"high: ${cost_estimate.high_usd:.2f}\n"
            f"by_phase: {dict(cost_estimate.by_phase)}\n"
        )

    def _load_anima_preamble(self) -> str:
        if ANIMA_PREAMBLE_FILE.exists():
            return ANIMA_PREAMBLE_FILE.read_text(encoding="utf-8")
        return ""

    def _load_maya_addendum(self) -> str:
        if MAYA_ADDENDUM_FILE.exists():
            return MAYA_ADDENDUM_FILE.read_text(encoding="utf-8")
        return ""

    # ----- parsers -----

    def _parse_opus(self, text: str) -> dict:
        """Parse the planning envelope. Tolerant of ```json``` code fences."""
        payload = _parse_json_envelope(text)
        for key in ("production_brief_md", "criteria_json", "plan_md"):
            if key not in payload:
                raise ValueError(
                    f"Opus response missing required key {key!r}. "
                    f"Got keys: {sorted(payload)}"
                )
        return payload

    def _parse_sonnet(self, text: str) -> dict:
        """Parse the adversarial envelope. Defensive: returns clean+confident
        when the response isn't parseable as adversarial (e.g., stub-shape
        mismatch during stub-only test runs)."""
        try:
            payload = _parse_json_envelope(text)
        except ValueError:
            return {"flag": None, "low_signal": False}
        if "flag" in payload or "low_signal" in payload:
            return {
                "flag": payload.get("flag"),
                "low_signal": bool(payload.get("low_signal", False)),
            }
        # Stub fallback may return a planning envelope here — treat as clean.
        return {"flag": None, "low_signal": False}

    def _inject_confidence_note(self, plan_md: str, concern: str) -> str:
        """Append a confidence-notes section naming the unresolved concern."""
        note_block = (
            f"\n\n## Maya's confidence notes\n\n"
            f"The adversarial validation pass and the low-signal escalation pass "
            f"both surfaced this concern; we hit the three-call ceiling before "
            f"resolving it:\n\n"
            f"> {concern}\n\n"
            f"Sean — review this before approving the plan.\n"
        )
        return plan_md.rstrip() + note_block


def _parse_json_envelope(text: str) -> dict:
    """Strip a ```json``` code fence if present, then json.loads."""
    if not text.strip():
        raise ValueError("Empty response from model")
    match = _CODE_FENCE_RE.match(text.strip())
    body = match.group(1) if match else text
    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model response is not parseable JSON: {exc}") from exc


def _atomic_write(path: Path, content: str) -> None:
    """temp-then-rename atomic write. Mirrors the patch_stager idiom."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)
