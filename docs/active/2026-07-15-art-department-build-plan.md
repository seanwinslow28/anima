
> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Per code task, also use superpowers:test-driven-development (red → verify-red → green → verify-green) and superpowers:verification-before-completion before any "done".

**Goal:** Build the Art Department — the visual-development stage between the Brainstorm Front Door and Cy — per the ratified design doc [`2026-07-15-art-department-stage-design.md`](2026-07-15-art-department-stage-design.md).

**Architecture:** Mirror the front door's proven two-layer split: a user-invoked orchestrator skill (`art-department`, run by the **Artie** persona) + two model-invoked discipline skills (`artdept-interrogate`, `artdept-synthesize`) over a thin, credential-free code seam (`pipeline/artdept/`) that validates structure and emits the bundle. Taste is never unit-tested — it is Sean's live eye + a rubric. The GRANDMASTER sprint artifacts are the worked example and the golden fixture's shape.

**Tech Stack:** Pure Python (stdlib + PyYAML), pytest, markdown skills. No model transport, no MCP, no spend anywhere in this build.

## Global Constraints

- **$0 build.** No live model call, no image generation, no MCP in any task or test. The live validation session (Checkpoint 3) is Sean-run, later, with its own session budget.
- **Never `ANTHROPIC_API_KEY`** (fleet-ops). Nothing in this build needs credentials at all.
- **`pipeline/frontdoor/` stays byte-identical.** The seam imports `SLUG_RE` from `pipeline.frontdoor.handoff` (read-only import); no frontdoor file is edited.
- **`manifest.yaml` is never mutated** by the stage or its tests — the readiness report *names* registration gaps, exactly like `manifest_gap_report.md`.
- **Both md5 guards byte-unchanged:** `evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md` = `2af75906502f1caf8857e18828ceb2e4`; `pipeline/agents/prompts/sean-screenwriting-voice.md` = `945af824fa53b948a18ac6bf206d67ef`.
- **Tests run per-directory from the repo root** (`python -m pytest tests/`) — a bare `pytest` collects site-packages; `tests/` + `pipeline/tests/` must never run combined (duplicate `tests` package basename).
- **No schema field without a real consumer** (the front door's no-schema-theater discipline, red-team-proven twice).
- **The propose-vs-decide invariant:** discipline skills return only `observations` / `options` / `recommendation` / `open_questions`; only the orchestrator writes locked decisions, append-only, after Sean decides.
- **Persona name:** `Artie` is the working default throughout the skill prose. It is flagged for Sean's confirmation at Checkpoint 2; a rename is a prose find-replace only (no code carries the name).
- **CHANGELOG.md** gets an entry with the final task; **CLAUDE.md + ROADMAP.md** updates ride the same task (this is a significant project change: new stage, new skills, new `pipeline/` package).

## File Structure

```
pipeline/artdept/                      # the code seam (mirrors pipeline/frontdoor/)
  __init__.py                          # docstring + public re-exports
  __main__.py                          # python -m pipeline.artdept
  handoff.py                           # Handoff dataclass — artdept.json
  emit.py                              # emit_artdept_dir + readiness_report
  validate.py                          # validate_artdept_dir + register_warnings (cast shape inline — no cast.py, per the seeds.py-was-schema-theater precedent)
  cli.py                               # `validate <dir>` subcommand

tests/
  test_artdept_handoff.py
  test_artdept_emit.py
  test_artdept_validate.py
  test_artdept_cli.py

evals/artdept/
  README.md                            # live-validation protocol (Checkpoint 3)
  fixtures/grandmaster-mini/           # committed golden fixture (mode: fixture)

.claude/skills/art-department/
  SKILL.md                             # the orchestrator — Artie runs the room
  references/
    session-sidecar-contract.md        # artdept-session.md shape (two blocks)
    prompt-technique-kit.md            # web-search lever, fresh-vs-edit, dependency map
    good-look-test-rubric.md           # live human-review checklist (never CI)
    grandmaster-worked-example.md      # the 2026-07-14 sprint as the quality bar
.claude/skills/artdept-interrogate/
  SKILL.md                             # the relentless art-direction grill
.claude/skills/artdept-synthesize/
  SKILL.md                             # synthesize-don't-interview; owns the emit-seam call
```

**The bundle contract** (decided here, consumed by Tasks 2–4 and the skills):

```
<bundle_dir>/                          # e.g. briefs/<slug>/artdept/
  design-bible.md                      # design-intent doc (museum-worthy prose)
  prompt-pack.md                       # the reproducible recipe (GRANDMASTER pack = reference shape)
  chatgpt-orchestration.md             # the batch runner Sean hands to the web app
  environment-style.md                 # the locked world-style note
  cast_list.yaml                       # designed cast + world locations + extras_guidance
  artdept.json                         # machine handoff (Handoff dataclass)
  cy_readiness_report.md               # generated — who is Cy-ready vs pending (never mutates manifest)
  refs/… , world/…                     # optional in-bundle image refs (fixture anchors live here)
```

`cast_list.yaml` schema (exact):

```yaml
designed:                    # every recurring identity — the "designed anchor" side of the scope line
  - character_id: kid        # lowercase-kebab (SLUG_RE)
    display_name: The Kid
    tier: principal          # principal | named
    style_register: primal-sketch-grit
    anchors:                 # ≥1 ref; resolved against bundle_dir first, then repo root
      - characters/kid/source-refs/anchor-timid.png
world:                       # key locations only — optional list
  - id: backyard-party
    display_name: The backyard party
    refs: [world/backyard-wide.png]
extras_guidance: |           # required — extras are covered by guidance, never by silence
  Background kids ages 8–10, varied heights/hair/skin, casual summer party clothes…
```

---

### Task 0: Pre-flight — worktree + baseline green

**Files:** none (setup only).

- [ ] **Step 1:** Create an isolated worktree from local `main` via `superpowers:using-git-worktrees`. Confirm the design doc `docs/active/2026-07-15-art-department-stage-design.md` is present on the branch (commit it to main first if it isn't).
- [ ] **Step 2:** Baseline: run `python -m pytest tests/` from the repo root. Expected: green (0 failures). Record the count.
- [ ] **Step 3:** Guard check: `md5 evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md pipeline/agents/prompts/sean-screenwriting-voice.md` — must equal the two hashes in Global Constraints.

---

### Task 1: `pipeline/artdept/handoff.py` — the artdept.json descriptor

**Files:**
- Create: `pipeline/artdept/__init__.py`, `pipeline/artdept/handoff.py`
- Test: `tests/test_artdept_handoff.py`

**Interfaces:**
- Consumes: `SLUG_RE` from `pipeline.frontdoor.handoff` (import only — frontdoor unedited).
- Produces: `Handoff(slug: str, characters: list[str], stage_provenance: list[str], mode: str = "interactive")` with `.to_json() -> str` and `Handoff.from_json(text) -> Handoff`; `MODES = ("interactive", "fixture")`. Deliberately the same four fields as the front door's — no `register`, no `budget`, no new field until a real consumer reads it (registers live in `cast_list.yaml`; nothing machine-reads a budget).

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_artdept_handoff.py
"""artdept.json — same four-field discipline as frontdoor.json (design §8).

The schema is deliberately identical in shape: slug/characters/stage_provenance/mode.
No register field (registers live per-entry in cast_list.yaml, which the readiness
report reads); no budget field (nothing machine-reads one). No-schema-theater.
"""
import pytest

from pipeline.artdept.handoff import MODES, Handoff


def test_round_trips():
    h = Handoff(
        slug="grandmaster",
        characters=["kid", "grandma", "host-dad"],
        stage_provenance=["micro-expand", "interrogate", "look-test", "synthesize"],
        mode="interactive",
    )
    assert Handoff.from_json(h.to_json()) == h


def test_rejects_unknown_fields():
    with pytest.raises(ValueError, match="unknown artdept.json fields"):
        Handoff.from_json(
            '{"slug":"x","characters":["a"],"stage_provenance":["s"],"register":"primal-sketch-grit"}'
        )


def test_rejects_bad_slug_and_empty_lists():
    with pytest.raises(ValueError):
        Handoff(slug="Not Kebab", characters=["a"], stage_provenance=["s"])
    with pytest.raises(ValueError):
        Handoff(slug="ok", characters=[], stage_provenance=["s"])
    with pytest.raises(ValueError):
        Handoff(slug="ok", characters=["a"], stage_provenance=[])


def test_rejects_unknown_mode():
    assert MODES == ("interactive", "fixture")
    with pytest.raises(ValueError, match="mode"):
        Handoff(slug="ok", characters=["a"], stage_provenance=["s"], mode="live")
```

- [ ] **Step 2: Run to verify failure**

Run: `python -m pytest tests/test_artdept_handoff.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'pipeline.artdept'`.

- [ ] **Step 3: Implement**

```python
# pipeline/artdept/__init__.py
"""pipeline.artdept — the Art Department bundle seam (design doc
docs/active/2026-07-15-art-department-stage-design.md §8).

Pure Python, credential-free. Validates structure and emits the handoff;
taste (look quality, prompt-pack quality) is Sean's live eye + the
good-look-test rubric, never a unit test. Mirrors pipeline/frontdoor/.
"""
```

```python
# pipeline/artdept/handoff.py
"""Handoff — the artdept.json machine descriptor (design §8).

Deliberately the same four fields as frontdoor.json: the schema grows only
when a real consumer exists. Registers live per-entry in cast_list.yaml
(the readiness report reads them); there is no top-level register or
budget field because nothing machine-reads either.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from pipeline.frontdoor.handoff import SLUG_RE

MODES = ("interactive", "fixture")


@dataclass
class Handoff:
    slug: str
    characters: list[str]
    stage_provenance: list[str]
    mode: str = "interactive"

    def __post_init__(self) -> None:
        if not (isinstance(self.slug, str) and SLUG_RE.match(self.slug)):
            raise ValueError(f"slug {self.slug!r} is not a clean lowercase-kebab token")
        if not (isinstance(self.characters, list) and self.characters):
            raise ValueError("characters must be a non-empty list of character slugs")
        for c in self.characters:
            if not (isinstance(c, str) and SLUG_RE.match(c)):
                raise ValueError(f"character id {c!r} is not lowercase-kebab")
        if not (isinstance(self.stage_provenance, list) and self.stage_provenance):
            raise ValueError("stage_provenance must be a non-empty list of stage names")
        if self.mode not in MODES:
            raise ValueError(f"mode {self.mode!r} not in {MODES}")

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2) + "\n"

    @classmethod
    def from_json(cls, text: str) -> "Handoff":
        payload = json.loads(text)
        if not isinstance(payload, dict):
            raise ValueError("artdept.json must be a JSON object")
        known = {f for f in cls.__dataclass_fields__}
        unknown = set(payload) - known
        if unknown:
            raise ValueError(f"unknown artdept.json fields: {sorted(unknown)}")
        return cls(**payload)
```

- [ ] **Step 4: Run to verify pass**

Run: `python -m pytest tests/test_artdept_handoff.py -v`
Expected: 4 PASS.

- [ ] **Step 5: Commit**

```bash
git add pipeline/artdept/__init__.py pipeline/artdept/handoff.py tests/test_artdept_handoff.py
git commit -m "feat(artdept): Handoff dataclass — the artdept.json descriptor"
```

---

### Task 2: `pipeline/artdept/validate.py` — the structural gate

**Files:**
- Create: `pipeline/artdept/validate.py`
- Test: `tests/test_artdept_validate.py`

**Interfaces:**
- Consumes: `Handoff` from Task 1; `ALL_REGISTERS` from `pipeline.registers`; `SLUG_RE` from `pipeline.frontdoor.handoff`.
- Produces: `validate_artdept_dir(bundle_dir: Path, repo_root: Path | None = None) -> list[str]` (empty = valid); `register_warnings(bundle_dir: Path) -> list[str]` (soft flags — an unregistered register is a *discovered authoring dependency*, not a failure; the hard gate is Cy execution); constants `TIERS = ("principal", "named")`, `REQUIRED_DESIGNED_FIELDS`, `PROSE_FILES`.
- Cast-list shape validation is **inline here** — no `cast.py` module, per the front door's red-team precedent (seeds.py was cut as schema theater).

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_artdept_validate.py
"""Structural gate for an Art Department bundle dir (design §8).

Structure only: files present + non-empty, cast_list shape, anchors resolve,
handoff↔cast cross-check. Look/prompt quality is Sean's rubric, never asserted.
"""
from pathlib import Path

import yaml

from pipeline.artdept.handoff import Handoff
from pipeline.artdept.validate import register_warnings, validate_artdept_dir


def make_bundle(tmp_path: Path, *, register: str = "pencil-test-colored") -> Path:
    d = tmp_path / "artdept"
    (d / "refs").mkdir(parents=True)
    (d / "refs" / "kid-anchor.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    (d / "design-bible.md").write_text("# Design bible\nGlasses = shed armor.\n")
    (d / "prompt-pack.md").write_text("# Prompt pack\n```\nFull-body anchor…\n```\n")
    (d / "chatgpt-orchestration.md").write_text("# Orchestration\nBatch 1 …\n")
    (d / "environment-style.md").write_text("# Environment style\nSunlit backyard…\n")
    cast = {
        "designed": [
            {
                "character_id": "kid",
                "display_name": "The Kid",
                "tier": "principal",
                "style_register": register,
                "anchors": ["refs/kid-anchor.png"],
            }
        ],
        "world": [
            {"id": "backyard-party", "display_name": "The backyard party", "refs": []}
        ],
        "extras_guidance": "Background kids 8-10, varied, casual summer clothes.",
    }
    (d / "cast_list.yaml").write_text(yaml.safe_dump(cast, sort_keys=False))
    h = Handoff(slug="grandmaster", characters=["kid"],
                stage_provenance=["interrogate", "look-test", "synthesize"], mode="fixture")
    (d / "artdept.json").write_text(h.to_json())
    (d / "cy_readiness_report.md").write_text("# Cy readiness — grandmaster\n- kid …\n")
    return d


def test_valid_bundle_passes(tmp_path):
    assert validate_artdept_dir(make_bundle(tmp_path)) == []


def test_missing_files_and_empty_prose_fail(tmp_path):
    d = make_bundle(tmp_path)
    (d / "prompt-pack.md").write_text("   \n")
    (d / "environment-style.md").unlink()
    problems = validate_artdept_dir(d)
    assert "prompt-pack.md is empty" in problems
    assert "missing file: environment-style.md" in problems


def test_cast_shape_enforced(tmp_path):
    d = make_bundle(tmp_path)
    cast = yaml.safe_load((d / "cast_list.yaml").read_text())
    cast["designed"][0].pop("style_register")
    cast["designed"][0]["tier"] = "cameo"
    cast["designed"][0]["anchors"] = []
    cast.pop("extras_guidance")
    (d / "cast_list.yaml").write_text(yaml.safe_dump(cast, sort_keys=False))
    problems = validate_artdept_dir(d)
    assert any("missing required field style_register" in p for p in problems)
    assert any("tier 'cameo'" in p for p in problems)
    assert any("anchors must be a non-empty list" in p for p in problems)
    assert any("extras_guidance" in p for p in problems)


def test_anchor_must_resolve_bundle_first_then_repo_root(tmp_path):
    d = make_bundle(tmp_path)
    cast = yaml.safe_load((d / "cast_list.yaml").read_text())
    cast["designed"][0]["anchors"] = ["refs/nonexistent.png"]
    (d / "cast_list.yaml").write_text(yaml.safe_dump(cast, sort_keys=False))
    problems = validate_artdept_dir(d, repo_root=tmp_path)
    assert any("anchor ref 'refs/nonexistent.png' does not resolve" in p for p in problems)
    # …and a repo-root-relative ref resolves even though it is not in the bundle:
    (tmp_path / "characters" / "kid" / "source-refs").mkdir(parents=True)
    (tmp_path / "characters" / "kid" / "source-refs" / "a.png").write_bytes(b"x")
    cast["designed"][0]["anchors"] = ["characters/kid/source-refs/a.png"]
    (d / "cast_list.yaml").write_text(yaml.safe_dump(cast, sort_keys=False))
    assert validate_artdept_dir(d, repo_root=tmp_path) == []


def test_handoff_cast_cross_check(tmp_path):
    d = make_bundle(tmp_path)
    h = Handoff(slug="grandmaster", characters=["kid", "grandma"],
                stage_provenance=["interrogate"], mode="fixture")
    (d / "artdept.json").write_text(h.to_json())
    problems = validate_artdept_dir(d)
    assert any("do not match" in p for p in problems)


def test_unregistered_register_warns_not_fails(tmp_path):
    d = make_bundle(tmp_path, register="not-a-register-yet")
    assert validate_artdept_dir(d) == []          # structure valid
    warnings = register_warnings(d)
    assert len(warnings) == 1
    assert "style-register-authoring-playbook" in warnings[0]
```

- [ ] **Step 2: Run to verify failure**

Run: `python -m pytest tests/test_artdept_validate.py -v`
Expected: FAIL — `ModuleNotFoundError` / `ImportError` on `pipeline.artdept.validate`.

- [ ] **Step 3: Implement**

```python
# pipeline/artdept/validate.py
"""validate_artdept_dir — the structural gate on an Art Department bundle (design §8).

Checks files + cast_list shape + anchor resolution + handoff cross-check.
Look quality, prompt-pack quality, and register *fit* are Sean's live eye +
the good-look-test rubric — never asserted here. Cast shape is validated
inline (no cast.py: the front door's red-team cut seeds.py as schema theater;
the same call holds).
"""

from __future__ import annotations

from pathlib import Path

import yaml

from pipeline.artdept.handoff import Handoff
from pipeline.frontdoor.handoff import SLUG_RE
from pipeline.registers import ALL_REGISTERS

PROSE_FILES = (
    "design-bible.md",
    "prompt-pack.md",
    "chatgpt-orchestration.md",
    "environment-style.md",
    "cy_readiness_report.md",
)
TIERS = ("principal", "named")
REQUIRED_DESIGNED_FIELDS = (
    "character_id",
    "display_name",
    "tier",
    "style_register",
    "anchors",
)


def _resolves(ref: str, bundle_dir: Path, repo_root: Path) -> bool:
    """Bundle-dir-first, then repo root — fixture refs live in the bundle;
    ratified production anchors live in characters/{id}/source-refs/."""
    return (bundle_dir / ref).exists() or (repo_root / ref).exists()


def validate_artdept_dir(bundle_dir: Path, repo_root: Path | None = None) -> list[str]:
    bundle_dir = Path(bundle_dir)
    repo_root = Path(repo_root) if repo_root is not None else Path(".")
    problems: list[str] = []

    for name in PROSE_FILES:
        p = bundle_dir / name
        if not p.exists():
            problems.append(f"missing file: {name}")
        elif not p.read_text(encoding="utf-8").strip():
            problems.append(f"{name} is empty")

    handoff: Handoff | None = None
    handoff_path = bundle_dir / "artdept.json"
    if handoff_path.exists():
        try:
            handoff = Handoff.from_json(handoff_path.read_text(encoding="utf-8"))
        except (ValueError, KeyError, TypeError) as e:
            problems.append(f"artdept.json invalid: {e}")
    else:
        problems.append("missing file: artdept.json")

    designed_ids: list[str] = []
    cast_path = bundle_dir / "cast_list.yaml"
    if cast_path.exists():
        cast = yaml.safe_load(cast_path.read_text(encoding="utf-8"))
        if not isinstance(cast, dict):
            problems.append("cast_list.yaml must be a mapping")
        else:
            designed = cast.get("designed")
            if not isinstance(designed, list) or not designed:
                problems.append("cast_list.yaml: designed must be a non-empty list")
                designed = []
            for i, entry in enumerate(designed):
                if not isinstance(entry, dict):
                    problems.append(f"designed #{i} is not a mapping")
                    continue
                for fld in REQUIRED_DESIGNED_FIELDS:
                    if not entry.get(fld):
                        problems.append(
                            f"designed #{i} ({entry.get('character_id', '?')}): "
                            f"missing required field {fld}"
                        )
                cid = entry.get("character_id")
                if isinstance(cid, str):
                    designed_ids.append(cid)
                    if not SLUG_RE.match(cid):
                        problems.append(f"designed character_id {cid!r} is not lowercase-kebab")
                tier = entry.get("tier")
                if tier and tier not in TIERS:
                    problems.append(
                        f"designed #{i} ({cid or '?'}): tier {tier!r} not in {TIERS} — "
                        "a non-recurring identity is extras_guidance, not a designed entry"
                    )
                anchors = entry.get("anchors")
                if anchors is not None and (not isinstance(anchors, list) or not anchors):
                    problems.append(
                        f"designed #{i} ({cid or '?'}): anchors must be a non-empty list of refs"
                    )
                elif isinstance(anchors, list):
                    for ref in anchors:
                        if not (isinstance(ref, str) and _resolves(ref, bundle_dir, repo_root)):
                            problems.append(
                                f"designed #{i} ({cid or '?'}): anchor ref {ref!r} does not "
                                "resolve (checked bundle dir, then repo root)"
                            )
            world = cast.get("world")
            if world is not None:
                if not isinstance(world, list):
                    problems.append("cast_list.yaml: world must be a list of locations")
                else:
                    for j, loc in enumerate(world):
                        if not isinstance(loc, dict) or not loc.get("id"):
                            problems.append(f"world #{j}: missing id")
                            continue
                        for ref in loc.get("refs") or []:
                            if not (isinstance(ref, str) and _resolves(ref, bundle_dir, repo_root)):
                                problems.append(
                                    f"world #{j} ({loc['id']}): ref {ref!r} does not resolve"
                                )
            if not (isinstance(cast.get("extras_guidance"), str) and cast["extras_guidance"].strip()):
                problems.append(
                    "cast_list.yaml: missing extras_guidance — extras are covered by "
                    "guidance baked into the prompt pack, never by silence (design §6)"
                )
    else:
        problems.append("missing file: cast_list.yaml")

    if handoff is not None and cast_path.exists() and sorted(handoff.characters) != sorted(designed_ids):
        problems.append(
            f"artdept.json characters {sorted(handoff.characters)} do not match "
            f"cast_list.yaml designed ids {sorted(designed_ids)}"
        )

    return problems


def register_warnings(bundle_dir: Path) -> list[str]:
    """SOFT flags. The Art Department locks a register by look-test, but a
    design can legitimately complete while the register's authoring rides the
    playbook as a called dependency (design §7 — the GRANDMASTER shape). So an
    unregistered register WARNS with the playbook pointer; the hard gate stays
    Cy execution (pipeline.registers raises UnknownRegisterError)."""
    bundle_dir = Path(bundle_dir)
    warnings: list[str] = []
    cast_path = bundle_dir / "cast_list.yaml"
    if not cast_path.exists():
        return warnings
    cast = yaml.safe_load(cast_path.read_text(encoding="utf-8"))
    if not isinstance(cast, dict) or not isinstance(cast.get("designed"), list):
        return warnings
    for i, entry in enumerate(cast["designed"]):
        if not isinstance(entry, dict):
            continue
        reg = entry.get("style_register")
        if isinstance(reg, str) and reg and reg not in ALL_REGISTERS:
            warnings.append(
                f"designed #{i} ({entry.get('character_id', '?')}): style_register "
                f"{reg!r} is not in the closed vocabulary yet — run "
                f"docs/architecture/style-register-authoring-playbook.md (R→S→B) "
                f"before the Cy pass (Cy fails loud on an unregistered register)."
            )
    return warnings
```

- [ ] **Step 4: Run to verify pass**

Run: `python -m pytest tests/test_artdept_validate.py -v`
Expected: 6 PASS.

- [ ] **Step 5: Commit**

```bash
git add pipeline/artdept/validate.py tests/test_artdept_validate.py
git commit -m "feat(artdept): validate_artdept_dir structural gate + register soft-warnings"
```

---

### Task 3: `pipeline/artdept/emit.py` — write the bundle + the Cy readiness report

**Files:**
- Create: `pipeline/artdept/emit.py`
- Test: `tests/test_artdept_emit.py`

**Interfaces:**
- Consumes: `Handoff` (Task 1); `validate_artdept_dir` (Task 2, in tests).
- Produces: `BUNDLE_FILES` tuple; `emit_artdept_dir(out_dir, *, design_bible_md, prompt_pack_md, orchestration_md, environment_style_md, cast: dict, handoff: Handoff, manifest: dict | None = None, repo_root: Path | None = None) -> Path`; `readiness_report(handoff, cast, manifest, bundle_dir, repo_root) -> str`. Deterministic + idempotent: same inputs, same bytes. Never touches `manifest.yaml`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_artdept_emit.py
from pathlib import Path

import yaml

from pipeline.artdept.emit import BUNDLE_FILES, emit_artdept_dir
from pipeline.artdept.handoff import Handoff
from pipeline.artdept.validate import validate_artdept_dir


def _cast(anchor: str) -> dict:
    return {
        "designed": [
            {"character_id": "kid", "display_name": "The Kid", "tier": "principal",
             "style_register": "pencil-test-colored", "anchors": [anchor]}
        ],
        "world": [],
        "extras_guidance": "Background kids, varied, casual.",
    }


def _emit(tmp_path: Path, manifest: dict | None = None) -> Path:
    out = tmp_path / "artdept"
    out.mkdir()
    (out / "refs").mkdir()
    (out / "refs" / "kid.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    h = Handoff(slug="grandmaster", characters=["kid"],
                stage_provenance=["interrogate", "look-test", "synthesize"], mode="fixture")
    return emit_artdept_dir(
        out,
        design_bible_md="# Design bible\nGlasses = shed armor.\n",
        prompt_pack_md="# Prompt pack\n```\nanchor prompt\n```\n",
        orchestration_md="# Orchestration\nBatch 1…\n",
        environment_style_md="# Environment style\nSunlit backyard.\n",
        cast=_cast("refs/kid.png"),
        handoff=h,
        manifest=manifest,
        repo_root=tmp_path,
    )


def test_emits_all_bundle_files_and_validates(tmp_path):
    out = _emit(tmp_path)
    for name in BUNDLE_FILES:
        assert (out / name).exists(), name
    assert validate_artdept_dir(out, repo_root=tmp_path) == []


def test_emit_is_deterministic(tmp_path):
    out = _emit(tmp_path)
    first = {n: (out / n).read_bytes() for n in BUNDLE_FILES}
    out2 = _emit(tmp_path)
    assert {n: (out2 / n).read_bytes() for n in BUNDLE_FILES} == first


def test_readiness_report_names_the_gap_and_the_ready(tmp_path):
    report = (_emit(tmp_path, manifest={"characters": {}}) / "cy_readiness_report.md").read_text()
    assert "kid" in report
    assert "not in manifest `characters:`" in report
    assert "author_bible.py" in report
    report2 = (_emit(tmp_path, manifest={"characters": {"kid": {}}}) / "cy_readiness_report.md").read_text()
    assert "registered" in report2


def test_cast_round_trips_through_yaml(tmp_path):
    out = _emit(tmp_path)
    assert yaml.safe_load((out / "cast_list.yaml").read_text()) == _cast("refs/kid.png")
```

- [ ] **Step 2: Run to verify failure**

Run: `python -m pytest tests/test_artdept_emit.py -v`
Expected: FAIL — no module `pipeline.artdept.emit`.

- [ ] **Step 3: Implement**

```python
# pipeline/artdept/emit.py
"""emit_artdept_dir — write the Art Department bundle (design §8).

Deterministic and idempotent: same inputs, same bytes. The readiness report
is the honesty artifact — the bundle is Cy-READY only where anchors exist,
the register is authored, and the manifest carries the character; the report
names each gap and the next action. manifest.yaml itself is never touched
(the front door's gap-report discipline, applied one stage later).
"""

from __future__ import annotations

from pathlib import Path

import yaml

from pipeline.artdept.handoff import Handoff
from pipeline.registers import ALL_REGISTERS

BUNDLE_FILES = (
    "design-bible.md",
    "prompt-pack.md",
    "chatgpt-orchestration.md",
    "environment-style.md",
    "cast_list.yaml",
    "artdept.json",
    "cy_readiness_report.md",
)


def emit_artdept_dir(
    out_dir: Path,
    *,
    design_bible_md: str,
    prompt_pack_md: str,
    orchestration_md: str,
    environment_style_md: str,
    cast: dict,
    handoff: Handoff,
    manifest: dict | None = None,
    repo_root: Path | None = None,
) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "design-bible.md").write_text(design_bible_md, encoding="utf-8")
    (out_dir / "prompt-pack.md").write_text(prompt_pack_md, encoding="utf-8")
    (out_dir / "chatgpt-orchestration.md").write_text(orchestration_md, encoding="utf-8")
    (out_dir / "environment-style.md").write_text(environment_style_md, encoding="utf-8")
    (out_dir / "cast_list.yaml").write_text(
        yaml.safe_dump(cast, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    (out_dir / "artdept.json").write_text(handoff.to_json(), encoding="utf-8")
    (out_dir / "cy_readiness_report.md").write_text(
        readiness_report(handoff, cast, manifest, out_dir, repo_root), encoding="utf-8"
    )
    return out_dir


def readiness_report(
    handoff: Handoff,
    cast: dict,
    manifest: dict | None,
    bundle_dir: Path,
    repo_root: Path | None = None,
) -> str:
    repo_root = Path(repo_root) if repo_root is not None else Path(".")
    registered = set((manifest or {}).get("characters") or {})
    designed = [e for e in (cast.get("designed") or []) if isinstance(e, dict)]

    lines = [
        f"# Cy readiness report — {handoff.slug}",
        "",
        "The Art Department emits ratified anchors + a locked register per",
        "designed character. A character is Cy-READY when its anchors are in",
        "`characters/{id}/source-refs/`, its register is in the closed vocabulary,",
        "and it is registered in the manifest `characters:` block. This report",
        "names each remaining gap; the Art Department never mutates manifest.yaml.",
        "",
    ]
    for e in designed:
        cid = e.get("character_id", "?")
        gaps: list[str] = []
        srcdir = repo_root / "characters" / str(cid) / "source-refs"
        if not any((srcdir / Path(a).name).exists() or str(a).startswith(f"characters/{cid}/")
                   for a in (e.get("anchors") or [])):
            gaps.append(
                f"anchors are bundle-local — copy the ratified anchors into `characters/{cid}/source-refs/` "
                "(Cy refuses to author from an empty source-refs/)"
            )
        reg = e.get("style_register")
        if reg not in ALL_REGISTERS:
            gaps.append(
                f"style_register {reg!r} is unauthored — run the style-register authoring "
                "playbook (R→S→B) as the called dependency"
            )
        if cid not in registered:
            gaps.append(
                f"not in manifest `characters:` — after the Bible pass, register `{cid}:` "
                "and its acceptance_criteria.json under `criteria_sources:`"
            )
        if gaps:
            lines.append(f"- **{cid}** ({e.get('display_name', '?')}) — NOT Cy-ready:")
            lines += [f"  {n}. {g}," for n, g in enumerate(gaps, 1)]
            lines.append(
                f"  then: `python scripts/author_bible.py characters/{cid}/ "
                f"--studio-brief \"<from design-bible.md>\" --run-dir runs/<id>/`"
            )
        else:
            lines.append(f"- **{cid}** ({e.get('display_name', '?')}) — registered; Cy-ready.")
    lines.append("")
    return "\n".join(lines)
```

- [ ] **Step 4: Run to verify pass**

Run: `python -m pytest tests/test_artdept_emit.py -v`
Expected: 4 PASS. (If the readiness-report anchor heuristic fails the `registered` case, fix the implementation, not the test — the test states the contract.)

- [ ] **Step 5: Commit**

```bash
git add pipeline/artdept/emit.py tests/test_artdept_emit.py
git commit -m "feat(artdept): emit_artdept_dir + cy_readiness_report (deterministic, manifest-untouched)"
```

---

### Task 4: CLI — `python -m pipeline.artdept validate <dir>`

**Files:**
- Create: `pipeline/artdept/cli.py`, `pipeline/artdept/__main__.py`
- Test: `tests/test_artdept_cli.py`

**Interfaces:**
- Consumes: `validate_artdept_dir`, `register_warnings` (Task 2).
- Produces: `main(argv) -> int` — exit 0 valid, 1 problems, 2 usage/missing dir. Warnings print on every path, never affect the exit code (the frontdoor CLI contract, verbatim).

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_artdept_cli.py
from pipeline.artdept.cli import main


def test_missing_dir_is_usage_error(tmp_path, capsys):
    assert main(["validate", str(tmp_path / "nope")]) == 2
    assert "not a directory" in capsys.readouterr().out


def test_invalid_dir_exits_1(tmp_path, capsys):
    d = tmp_path / "empty"
    d.mkdir()
    assert main(["validate", str(d)]) == 1
    assert "FAIL:" in capsys.readouterr().out


def test_valid_dir_exits_0(tmp_path, capsys, monkeypatch):
    import pipeline.artdept.cli as cli
    monkeypatch.setattr(cli, "validate_artdept_dir", lambda d: [])
    monkeypatch.setattr(cli, "register_warnings", lambda d: ["w1"])
    d = tmp_path / "ok"
    d.mkdir()
    assert main(["validate", str(d)]) == 0
    out = capsys.readouterr().out
    assert "WARN: w1" in out and "ok:" in out
```

- [ ] **Step 2: Run to verify failure**

Run: `python -m pytest tests/test_artdept_cli.py -v` — Expected: FAIL (no `cli` module).

- [ ] **Step 3: Implement**

```python
# pipeline/artdept/cli.py
"""python -m pipeline.artdept validate <dir> — validate only, no scaffold.

Exit codes: 0 valid, 1 problems found, 2 usage/missing dir. Register warnings
print on every path but never affect the exit code: an unauthored register at
the Art Department is a called dependency, not a failure (the hard gate is Cy).
"""

from __future__ import annotations

import argparse
from pathlib import Path

from pipeline.artdept.validate import register_warnings, validate_artdept_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m pipeline.artdept",
        description="Art Department bundle-dir contract checks.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    p_validate = sub.add_parser("validate", help="Validate an Art Department bundle dir.")
    p_validate.add_argument("bundle_dir", metavar="DIR")
    args = parser.parse_args(argv)

    bundle_dir = Path(args.bundle_dir)
    if not bundle_dir.is_dir():
        print(f"error: {bundle_dir} is not a directory")
        return 2
    problems = validate_artdept_dir(bundle_dir)
    for w in register_warnings(bundle_dir):
        print(f"WARN: {w}")
    if problems:
        for p in problems:
            print(f"FAIL: {p}")
        return 1
    print(f"ok: {bundle_dir} is a valid Art Department bundle dir")
    return 0
```

```python
# pipeline/artdept/__main__.py
import sys

from pipeline.artdept.cli import main

sys.exit(main())
```

- [ ] **Step 4: Run to verify pass**

Run: `python -m pytest tests/test_artdept_cli.py -v` — Expected: 3 PASS.
Also run the module for real: `python -m pipeline.artdept validate docs` — Expected: exit 1 with `FAIL:` lines (docs is a dir but not a bundle).

- [ ] **Step 5: Commit**

```bash
git add pipeline/artdept/cli.py pipeline/artdept/__main__.py tests/test_artdept_cli.py
git commit -m "feat(artdept): validate CLI — python -m pipeline.artdept validate <dir>"
```

---

### Task 5: The golden fixture — `evals/artdept/fixtures/grandmaster-mini/`

**Files:**
- Create: `evals/artdept/fixtures/grandmaster-mini/` (a committed, minimal, `mode: fixture` bundle)
- Create: `evals/artdept/README.md` (the live-validation protocol — Checkpoint 3)
- Test: `tests/test_artdept_fixture.py`

**Interfaces:**
- Consumes: the whole seam (Tasks 1–4). Produces: the committed reference bundle every future session can validate against, shaped by the real GRANDMASTER artifacts (`runs/2026-07-14-grandmaster-kid-design/GRANDMASTER-PROMPT-PACK.md` + `ORCHESTRATION-PROMPT-FOR-CHATGPT.md` — condensed excerpts, since `runs/` is gitignored and the fixture must be committed).

- [ ] **Step 1: Write the failing test**

```python
# tests/test_artdept_fixture.py
"""The committed golden fixture stays valid. mode must be 'fixture' —
a fixture bundle can never masquerade as a live Artie session."""
import json
from pathlib import Path

from pipeline.artdept.validate import validate_artdept_dir

FIXTURE = Path("evals/artdept/fixtures/grandmaster-mini")


def test_golden_fixture_validates():
    assert FIXTURE.is_dir()
    assert validate_artdept_dir(FIXTURE) == []


def test_fixture_mode_is_fixture():
    payload = json.loads((FIXTURE / "artdept.json").read_text())
    assert payload["mode"] == "fixture"
```

- [ ] **Step 2: Run to verify failure** — `python -m pytest tests/test_artdept_fixture.py -v` — Expected: FAIL (`FIXTURE.is_dir()` false).

- [ ] **Step 3: Build the fixture.** Create `evals/artdept/fixtures/grandmaster-mini/` with:
  - `design-bible.md` — a ~30-line condensation of the sprint's locked decisions (glasses = shed armor; same body, new attitude; grandma = two artifact looks, unmistakably one woman; daytime/neutral reads matter). Source: the [field report](../anima-test-runs/2026-07-14-grandmaster-character-design-sprint.md) §Decisions-locked.
  - `prompt-pack.md` — prompts #1 (boy wimpy anchor, one style block), #6 (reusable turnaround edit), #9 (composite keepsake photo), copied verbatim from `GRANDMASTER-PROMPT-PACK.md` with a header noting the full pack lives in the (gitignored) run dir. This pins the fresh-vs-edit economy shape.
  - `chatgpt-orchestration.md` — the dependency-map + batching sections of `ORCHESTRATION-PROMPT-FOR-CHATGPT.md`, condensed (~25 lines): golden rule (FRESH/EDIT/COMPOSITE), never-cross-styles, checkpointed batches.
  - `environment-style.md` — the backyard-party world description from pack prompt #3 (~8 lines).
  - `cast_list.yaml` — `designed:` kid (principal, `primal-sketch-grit`, anchor `refs/kid-anchor.png`) + grandma (principal, `primal-sketch-grit`, anchor `refs/grandma-anchor.png`); `world:` backyard-party with `refs: []`; `extras_guidance:` the background-kids line from pack prompt #3.
  - `refs/kid-anchor.png`, `refs/grandma-anchor.png` — 1×1 placeholder PNGs: `python -c "from PIL import Image; Image.new('RGB',(1,1),(200,150,100)).save('evals/artdept/fixtures/grandmaster-mini/refs/kid-anchor.png')"` (and grandma). Placeholders, clearly named — the real anchors are gitignored run artifacts.
  - `artdept.json` — `{"slug": "grandmaster", "characters": ["kid", "grandma"], "stage_provenance": ["micro-expand", "interrogate", "look-test", "lock", "expand-outward", "synthesize"], "mode": "fixture"}`.
  - `cy_readiness_report.md` — generate it honestly: `python - <<'EOF'` calling `readiness_report()` with `manifest=yaml.safe_load(open("manifest.yaml"))` and write the output, so the committed report reflects the real manifest state (kid/grandma unregistered → NOT Cy-ready, playbook pointer for the register if unauthored).
- [ ] **Step 4: Write `evals/artdept/README.md`** — the live-validation protocol: *Checkpoint 3 is a Sean-run live Art Department session on a real piece (GRANDMASTER's host-dad, or the next greenlit piece). Artie runs the room; Sean declares a session credit budget up front; the session ends with `python -m pipeline.artdept validate <bundle>` exiting 0 AND Sean scoring the session against `good-look-test-rubric.md` (criteria 1–3 block together). The fixture here is the structural reference, never a quality oracle.*
- [ ] **Step 5: Run to verify pass** — `python -m pytest tests/test_artdept_fixture.py -v` — Expected: 2 PASS. Also: `python -m pipeline.artdept validate evals/artdept/fixtures/grandmaster-mini` — Expected: exit 0 (a register WARN is acceptable if `primal-sketch-grit`'s vocabulary state changes; it must not fail).
- [ ] **Step 6: Commit**

```bash
git add evals/artdept/ tests/test_artdept_fixture.py
git commit -m "feat(artdept): grandmaster-mini golden fixture + live-validation protocol"
```

---

### Task 6: The orchestrator skill — `.claude/skills/art-department/`

**Files:**
- Create: `.claude/skills/art-department/SKILL.md`
- Create: `references/session-sidecar-contract.md`, `references/prompt-technique-kit.md`, `references/good-look-test-rubric.md`, `references/grandmaster-worked-example.md`

Prose task — no unit test; verified by the Task-8 read-through + Checkpoint 2 (Sean) + Checkpoint 3 (live). Author against the design doc §4–§7 with `brainstorm-front-door/SKILL.md` as the structural reference implementation. The load-bearing content each file MUST carry:

- [ ] **Step 1: `SKILL.md`** — frontmatter `name: art-department`; description: *"The anima Art Department — the visual-development playground between the Brainstorm Front Door and Cy. Turn a front-door bundle (or hand brief) into ratified anchors + a locked register + the prompt pack Sean batch-generates in ChatGPT. Use when a piece needs its look found: character design, look-tests, world design, register lock. USER-INVOKED — runs the room; do not invoke from another skill."* Body sections, in order:
  1. **You are Artie** — art-director persona; the room is a playground (*"This is about playing around and finding the right style… a fun playground for art and characters"* — quote Sean verbatim from the design doc §2); domain lens = the `creative-director` skill; Artie **proposes, Sean's eye decides**, every lock is Sean's.
  2. **The chain diagram** — `bundle/brief → MICRO-EXPAND (inline) → INTERROGATE (artdept-interrogate) → LOOK-TEST forks (inline) ⇄ lock → EXPAND-OUTWARD (inline, per named-cast member + key location) → SYNTHESIZE (artdept-synthesize) → emit + validate`. A skipped stage is declared skipped in `stage_provenance`; never pretend a stage ran.
  3. **Step 0 — session sidecar** — create `artdept-session.md` (shape: `references/session-sidecar-contract.md`): LOCKED DECISIONS (append-only, orchestrator-only, after Sean decides) + PROPOSALS LOG (four kinds only). Record the input bundle path + the **session credit budget Sean declares** as the first locked entries.
  4. **The spend discipline (design §10)** — Sean declares a credit ceiling at session start (Higgsfield credits / subscription; **never `ANTHROPIC_API_KEY`**); every look-test render announces its cost against the running total; **hard-stop at the ceiling** — ask Sean to raise it explicitly or continue $0 (prompts only). In-stage generation is *cheap and exploratory only*; the definitive batch is always Sean's in ChatGPT.
  5. **MICRO-EXPAND (inline)** — before grilling, per principal: 3 divergent visual directions (silhouette/shape-language reads of the personality), 3 candidate registers from `pipeline/registers.py`, the loaded-object question surfaced. Then one question: deepen, or proceed to the grill?
  6. **LOOK-TEST forks (inline)** — when an axis is contested (register A vs B; design variant): write candidate prompts using `references/prompt-technique-kit.md`; render a *few* cheap candidates within budget (or emit prompts for Sean's $0 web-app pass); Sean's eye arbitrates; you lock. Include the register rule verbatim: **pick from the closed vocabulary by default; on no-fit, surface the gap + hand off to the style-register authoring playbook as a called dependency — never inline-author a register.**
  7. **EXPAND-OUTWARD (inline)** — the same grill-and-lock loop for named secondary cast + key locations + environment style, **reusing locked anchors as edit references (never cross styles; edit the anchors you make)**. The scope line, verbatim from design §6: designed anchor = every principal + named/recurring character; extras + set-dressing = `extras_guidance`, never individually designed; world = key locations + the environment-style note only.
  8. **SYNTHESIZE + emit** — invoke `artdept-synthesize`; the bundle lands per the code-seam contract; finish with `python -m pipeline.artdept validate <bundle>` and paste the output. Read `references/grandmaster-worked-example.md` before your first session — it is the quality bar.
- [ ] **Step 2: `references/session-sidecar-contract.md`** — the two-block shape (mirror the front door's file, retargeted): LOCKED DECISIONS entries (`spark/bundle`, `budget`, `design locks` per character, `register lock`, `chosen prompt recipes`) + PROPOSALS LOG (four kinds; `### micro-expand`, `### interrogate`, `### look-test`, `### expand-outward` example blocks).
- [ ] **Step 3: `references/prompt-technique-kit.md`** — the technique kit, each with a worked example from the sprint: (a) **the web-search-the-show lever** — quote the working clause verbatim: *"STYLE: a stylized 2D hand-drawn ANIMATED CARTOON in the raw hand-inked register of Genndy Tartakovsky's show Primal. Use Web search to research Genndy Tartakovsky's show Primal to accurately depict the character animation art style."*; (b) **fresh-vs-edit economy** (from `prompt-how-much` + the pack's Rule header): FRESH = full description + named style + anti-render negation; EDIT/COMPOSITE = terse, only the change, reference carries identity+style, one style-agnostic prompt; (c) **the dependency map** — FRESH establishes identity → EDITs always edit the anchor of that character in that style → COMPOSITEs feed both named anchors; never cross styles; (d) **daytime/neutral reads** — flat even daylight for design reads (dramatic lighting hides the face); (e) **register research** — read `registers/{name}/research.md` before writing a route in that register.
- [ ] **Step 4: `references/good-look-test-rubric.md`** — a live human-review checklist for Sean, **never a CI/self-pass gate**. Six criteria (mirroring good-art-viz-rubric's shape): (1) contested forks rendered as *same-composition, different-register/design* comparisons — apples-to-apples; (2) **identity survives the fork** — the character is recognizably itself across looks (across-edit identity, the sprint's craft finding #1); (3) every lock is a **named specific** Sean chose, recorded with why the winner won; (4) the prompt pack reproduces the locked look (FRESH/EDIT economy respected, dependency map present, batches checkpointed); (5) scope line held — no individually-designed extras, extras_guidance present; (6) register no-fit surfaced to the playbook, never inline-authored. Criteria 1–3 block together (a gameable single bar is the art-viz red-team lesson). Worked positives: the sprint's kid two-state + grandma two-look tests.
- [ ] **Step 5: `references/grandmaster-worked-example.md`** — a ~60-line narrative condensation of the [sprint field report](../anima-test-runs/2026-07-14-grandmaster-character-design-sprint.md): what the loop looked like, the decisions locked, the three craft findings, and the deliverables shape — with pointers to the full report + the fixture.
- [ ] **Step 6: Commit**

```bash
git add .claude/skills/art-department/
git commit -m "feat(artdept): art-department orchestrator skill — Artie runs the room"
```

---

### Task 7: The discipline skills — `artdept-interrogate` + `artdept-synthesize`

**Files:**
- Create: `.claude/skills/artdept-interrogate/SKILL.md`
- Create: `.claude/skills/artdept-synthesize/SKILL.md`

Prose task. Author against `frontdoor-interrogate/SKILL.md` and `frontdoor-synthesize/SKILL.md` as the reference implementations (same discipline, retargeted from *story* to *look*). Load-bearing content:

- [ ] **Step 1: `artdept-interrogate/SKILL.md`** — frontmatter description: *"The Art Department's INTERROGATE stage — the relentless art-direction grill that turns a seed + personality into locked visual specifics. MODEL-INVOKED by the art-department orchestrator only."* Must carry, adapted from the frontdoor sibling: **one question at a time** (never a questionnaire); **always recommend your answer** (every question ships with Artie's lean + one line of why, grounded in the brief/concept); **discover, don't ask** (mine the bundle first — a seed's `source_notes` half-answers the silhouette question); **the generic-answer detector** (refuse categories: not "glasses" but *"large thick square eyeglasses a size too big that slide down his nose"* — after two pushes, propose three named specifics and ask Sean to pick or veto); **the visual North Star** (each principal exits with: silhouette/shape language, the loaded object, palette anchors, face/identity notes, wardrobe + its story states, the register hypothesis to look-test); proposals-only output (four kinds; the orchestrator locks).
- [ ] **Step 2: `artdept-synthesize/SKILL.md`** — frontmatter description: *"The Art Department's SYNTHESIZE stage — write the bundle from the session sidecar and emit through the pipeline.artdept code seam. MODEL-INVOKED by the art-department orchestrator only."* Must carry: **synthesize, don't interview** (a hole = an `open_question` back to the orchestrator, never an invention); what to write — `design-bible.md` (museum-worthy prose from the locked decisions, sidecar phrasing verbatim where it sings), `prompt-pack.md` (the **winning recipes** from the look-tests — the locked prompt techniques, FRESH/EDIT economy, style blocks; never re-derive a prompt the room already ratified), `chatgpt-orchestration.md` (dependency map + never-cross-styles + checkpointed batches — the sprint's orchestration prompt is the shape), `environment-style.md`, `cast_list.yaml` (the scope line made rows), `artdept.json` (`mode: interactive`); then **call the seam**: build the `Handoff`, call `emit_artdept_dir(...)` (or write the files then run `python -m pipeline.artdept validate <dir>`), paste the validator output; a FAIL returns to the orchestrator, never silently shipped.
- [ ] **Step 3: Read-through check** — trace one imagined session end-to-end across the three skills: bundle in → sidecar → grill → look-test lock → expand-outward → synthesize → validate exit 0. Confirm no skill writes a lock, no skill spends without the budget entry, and every reference file named in prose exists.
- [ ] **Step 4: Commit**

```bash
git add .claude/skills/artdept-interrogate/ .claude/skills/artdept-synthesize/
git commit -m "feat(artdept): interrogate + synthesize discipline skills"
```

---

### Task 8: Docs — CHANGELOG, CLAUDE.md, ROADMAP

**Files:**
- Modify: `CHANGELOG.md` (append the dated entry), `CLAUDE.md` (Skills Map + directory structure), `ROADMAP.md` (road-ahead placeholder)

- [ ] **Step 1: CHANGELOG.md** — dated entry: what shipped (the Art Department stage: `pipeline/artdept/` seam, three skills, golden fixture), why (the GRANDMASTER sprint proved the missing middle between the front door's seeds and Cy's bake; design doc link), and the boundary decisions (facilitator-primary playground; prompt pack as headline output; pick-register-by-default/playbook-on-no-fit; the scope line; session-budget spend model).
- [ ] **Step 2: CLAUDE.md** — add a Skills Map row for **`art-department` (+ `artdept-interrogate` / `artdept-synthesize`) — Artie**, between the front-door row and the Maya row (pipeline order), summarizing: BUILT date, the stage's position (front door → **Art Department** → Cy), the bundle contract + CLI (`python -m pipeline.artdept validate <dir>`), the register rule, and the Checkpoint-3 live-validation status (pending until the live session runs). Add `pipeline/artdept/` and `evals/artdept/` to the directory tree. Keep the row a *summary* — the design doc stays the source of truth.
- [ ] **Step 3: ROADMAP.md** — per the design doc §12 (Sean's sequencing call at Checkpoint 2): either advance "Current focus" (if Sean promotes this to the active workstream) or add it to "The road ahead" as a scoped placeholder with its DoD: *(1) seam + skills green ($0, this plan); (2) a Sean-run live Art Department session on a real piece produces a bundle that validates AND passes the good-look-test rubric; (3) that bundle's characters flow into a real Cy authoring pass.* Do not silently pick — this edit encodes whichever call Sean made.
- [ ] **Step 4: Commit**

```bash
git add CHANGELOG.md CLAUDE.md ROADMAP.md
git commit -m "docs: Art Department stage — CHANGELOG entry, CLAUDE.md rows, ROADMAP placement"
```

---

### Task 9: Verification gate (before any "done")

- [ ] **Step 1:** `superpowers:verification-before-completion` — run fresh and paste output:
  - `python -m pytest tests/` — full suite green, count = baseline + the new artdept tests (≈ +15).
  - `python -m pytest pipeline/tests/` — separately, green (the duplicate-basename rule).
  - `python -m pipeline.artdept validate evals/artdept/fixtures/grandmaster-mini` — exit 0.
  - `md5 evals/vision_critic/traces/g6.1b-criteria-attached-2026-06-08.md pipeline/agents/prompts/sean-screenwriting-voice.md` — both hashes unchanged.
  - `git diff --stat main -- pipeline/frontdoor/` — empty (byte-identical).
  - `git status` — only the paths named in this plan's File Structure + Task 8 docs.
- [ ] **Step 2:** Confirm the three skills cross-reference coherently (every `references/*.md` named in prose exists; the seam CLI command in the skills matches `python -m pipeline.artdept validate`).
- [ ] **Step 3:** STOP — Checkpoint 2 (Sean review): persona name confirmation (Artie / rename = prose find-replace), ROADMAP placement call, and the skill prose read-through. Checkpoint 3 (the live session) is Sean-run per `evals/artdept/README.md`, not part of this build.

---

## Checkpoints

- **Checkpoint 1 (structural, after Task 5):** seam + fixture green, CLI works, frontdoor byte-identical. Safe to pause here — the skills stack on a proven seam.
- **Checkpoint 2 (Sean review, after Task 9):** skill prose read-through; persona name; ROADMAP placement. The build stops at first green — no live session in this plan.
- **Checkpoint 3 (live, later, Sean-run):** the real Art Department session per `evals/artdept/README.md` — session budget declared, bundle validates exit 0, rubric criteria 1–3 pass Sean's eye. This is the stage's DoD item #2, deliberately outside the $0 build.

## What this plan deliberately does NOT build

- No orchestrator (`pipeline/run.py`) wiring — the Art Department is skill-invoked pre-pipeline, like the front door; a `run.py` stage has no consumer until a piece flows through live (promotion trigger: the first live bundle feeding a real Cy pass).
- No in-seam generation/transport code — look-test rendering rides the existing skills/runners under the session budget; the seam stays credential-free.
- No register authoring, no `registers.py` change, no manifest mutation.
- No new `artdept.json` fields beyond the four (no `budget`, no `register` — no consumer).
