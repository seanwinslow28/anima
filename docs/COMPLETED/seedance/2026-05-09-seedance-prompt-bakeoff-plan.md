# Seedance Prompt Template Bake-off — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run a structured 9-variant × 2-shot × 2-seed bake-off on Seedance 2.0, score manually with a binary rubric, lock the winning prompt structure as a reusable canonical template at `prompts/seedance-template-v4.md`.

**Architecture:** A new YAML file (`seedance_bakeoff_variants.yaml`) defines all 9 variants with their per-shot prompts. A new orchestrator script (`pipeline/seedance_bakeoff.py`) iterates `variant × shot × seed` using the existing `seedance_lib.py` helpers, mirrors the async-batch pattern from `seedance_generate.py`, writes outputs to a structured run dir, and produces an empty scoring CSV. After the user manually scores clips, a synthesis writeup and locked template are committed.

**Tech Stack:** Python 3 + PyYAML (already a dep), `fal-client` (already a dep), `seedance_lib.py` helpers (already in repo).

**Design spec:** [docs/2026-05-09-seedance-prompt-bakeoff-design.md](2026-05-09-seedance-prompt-bakeoff-design.md)

---

## File structure

| File | Status | Responsibility |
|---|---|---|
| `pipeline/seedance_bakeoff_variants.yaml` | **Create** | Defines V0–V8 with per-shot prompts (W1 + S0) |
| `pipeline/seedance_lib.py` | **Modify** | Add `load_bakeoff_variants()` and `make_bakeoff_run_dir()` helpers |
| `pipeline/seedance_bakeoff.py` | **Create** | Orchestrator that runs the variant matrix |
| `tests/test_seedance_bakeoff_lib.py` | **Create** | Unit tests for the new lib helpers (pure-function logic only) |
| `runs/seedance-bakeoff-2026-05-09/` | **Create at runtime** | Output dir — MP4s, meta JSONs, scoring CSV, results writeup |
| `runs/seedance-bakeoff-2026-05-09/scoring.csv` | **Create at runtime** | Empty scoring template; manually filled |
| `runs/seedance-bakeoff-2026-05-09/results.md` | **Create after scoring** | Synthesis: winner, margins, axis breakdown |
| `prompts/seedance-template-v4.md` | **Create after winner locked** | The canonical reusable template asset |
| `docs/2026-05-09-seedance-prompt-bakeoff-results.md` | **Create after winner locked** | Committed copy of run results (since `runs/` is gitignored) |
| `CHANGELOG.md` | **Modify** | Append entry for the bake-off + template lock |
| `CLAUDE.md` | **Modify** | Reference template v4 in source-of-truth doc table |

---

## Task 1: Create the variants YAML

**Files:**
- Create: `pipeline/seedance_bakeoff_variants.yaml`

- [ ] **Step 1: Create the file with all 9 variants × 2 shots**

```yaml
# Seedance Prompt Template Bake-off — Variant Matrix
# Spec: docs/2026-05-09-seedance-prompt-bakeoff-design.md
# Each variant defines the same prompt structure for both test shots (W1, S0).
# The orchestrator iterates: variant × shot × seed (42, 1337).

version: 1
created: 2026-05-09

# Test shots (anchors come from pipeline/seedance_shotlist.yaml at runtime).
test_shots:
  - W1
  - S0

# Seeds used per (variant, shot). Two seeds per cell => stable signal under model variance.
seeds: [42, 1337]

# Run defaults (overridable via CLI).
defaults:
  tier: fast
  resolution: 720p
  duration: 4
  generate_audio: false

variants:
  - id: V00
    name: v3_control
    description: "v3 baseline (control). Original wording, ~115 words."
    isolates_axis: control
    prompts:
      W1: |
        Traditional 2D animation pencil test in the style of classic Disney rough animation. Sean walks left to right across the frame at a steady, relaxed pace. His head turns slightly as he takes in the floating Film props around him. The props remain stationary — only Sean moves. Sean is clean-shaven throughout.

        CAMERA: Completely static, locked tripod. No pan, no zoom, no jitter, no rotation.

        CRITICAL STYLE REQUIREMENTS:
        - Rough graphite pencil line quality on every frame
        - Cream paper grain texture stays consistent
        - Visible construction marks on the character
        - Bold dark pencil outlines, no anti-aliasing on edges
        - Flat graphite shading only, no digital gradients or smooth blending
        - Even diffuse animation paper lighting, no cinematic shadows
        - No anime stylization, no digital cleanness, no glossy polish

        Duration: 4 seconds.
      S0: |
        Traditional 2D animation pencil test in the style of classic Disney rough animation. The floating AI news headlines dissolve away from the frame as the desk, laptop, second monitor, coffee mug, and chair materialize in their place. Sean transitions from a mid-stride walk to a seated working pose at the desk. A subtle 5-o'clock shadow stubble grows in on his face as time passes.

        CAMERA: Completely static, locked tripod. No pan, no zoom, no jitter, no rotation.

        CRITICAL STYLE REQUIREMENTS:
        - Rough graphite pencil line quality on every frame
        - Cream paper grain texture stays consistent
        - Visible construction marks on the character
        - Bold dark pencil outlines, no anti-aliasing on edges
        - Flat graphite shading only, no digital gradients or smooth blending
        - Even diffuse desk lighting, no cinematic shadows
        - No anime stylization, no digital cleanness, no glossy polish

        Duration: 4 seconds.

  - id: V01
    name: research_corrected_baseline
    description: "v3 with negations dropped, word count trimmed, redundant style description removed. ~80 words."
    isolates_axis: research_priors_applied
    prompts:
      W1: |
        Traditional 2D animation pencil test in the style of classic Disney rough animation. Sean walks left to right across the frame at a steady, relaxed pace. His head turns slightly as he takes in the floating Film props around him. The props stay stationary; only Sean moves. Sean is clean-shaven throughout.

        CAMERA: Completely static, locked tripod.

        STYLE: Graphite on cream paper, rough pencil line quality, organic line wavering, visible construction marks, warm ivory paper tone, flat graphite shading.

        Duration: 4 seconds.
      S0: |
        Traditional 2D animation pencil test in the style of classic Disney rough animation. The floating AI news headlines dissolve away as the desk, laptop, monitor, coffee mug, and chair materialize. Sean transitions from a mid-stride walk to a seated working pose at the desk. A subtle 5-o'clock shadow stubble grows in on his face as time passes.

        CAMERA: Completely static, locked tripod.

        STYLE: Graphite on cream paper, rough pencil line quality, organic line wavering, visible construction marks, warm ivory paper tone, flat graphite shading.

        Duration: 4 seconds.

  - id: V02
    name: transition_arc
    description: "V1 + transition-arc framing (Starting with… transitioning to… ending with…)."
    isolates_axis: B
    prompts:
      W1: |
        Traditional 2D animation pencil test in the style of classic Disney rough animation. Starting with Sean stepping into frame from the left amid floating Film props, transitioning to him walking steadily across the frame with his head turning to take in the props, ending with him approaching the right edge as the Film props give way. The props stay stationary; only Sean moves. Sean is clean-shaven throughout.

        CAMERA: Completely static, locked tripod.

        STYLE: Graphite on cream paper, rough pencil line quality, organic line wavering, visible construction marks, warm ivory paper tone, flat graphite shading.

        Duration: 4 seconds.
      S0: |
        Traditional 2D animation pencil test in the style of classic Disney rough animation. Starting with Sean mid-stride amid floating AI news headlines, transitioning to him approaching and lowering himself into the chair as the desk, laptop, monitor, coffee mug, and chair materialize and the headlines dissolve, ending with Sean seated at the desk in a working pose with subtle 5-o'clock shadow stubble grown in.

        CAMERA: Completely static, locked tripod.

        STYLE: Graphite on cream paper, rough pencil line quality, organic line wavering, visible construction marks, warm ivory paper tone, flat graphite shading.

        Duration: 4 seconds.

  - id: V03
    name: animation_timing
    description: "V1 + animation-timing motion language (anticipation, hold, snap, settle)."
    isolates_axis: C
    prompts:
      W1: |
        Traditional 2D animation pencil test in the style of classic Disney rough animation. Sean walks left to right across the frame: anticipation as his weight shifts forward, settled walk cycle through the middle, head turning with a slight delayed follow-through to take in the floating Film props. The props stay stationary; only Sean moves. Sean is clean-shaven throughout.

        CAMERA: Completely static, locked tripod.

        STYLE: Graphite on cream paper, rough pencil line quality, organic line wavering, visible construction marks, warm ivory paper tone, flat graphite shading.

        Duration: 4 seconds.
      S0: |
        Traditional 2D animation pencil test in the style of classic Disney rough animation. The floating AI news headlines fade out as the desk, laptop, monitor, coffee mug, and chair materialize. Sean's mid-stride walk anticipates a slow-down, settles into a chair-bend with weight shift, holds momentarily in seated pose. A subtle 5-o'clock shadow stubble grows in across the duration.

        CAMERA: Completely static, locked tripod.

        STYLE: Graphite on cream paper, rough pencil line quality, organic line wavering, visible construction marks, warm ivory paper tone, flat graphite shading.

        Duration: 4 seconds.

  - id: V04
    name: audio_cues
    description: "V1 + minimal subtle audio descriptors. generate_audio remains False; tests whether audio cues drive visual physics."
    isolates_axis: D
    prompts:
      W1: |
        Traditional 2D animation pencil test in the style of classic Disney rough animation. Sean walks left to right across the frame at a steady, relaxed pace. His head turns slightly as he takes in the floating Film props around him. The props stay stationary; only Sean moves. Sean is clean-shaven throughout.

        AUDIO: Soft footsteps on paper, faint pencil scratch, paper rustle.

        CAMERA: Completely static, locked tripod.

        STYLE: Graphite on cream paper, rough pencil line quality, organic line wavering, visible construction marks, warm ivory paper tone, flat graphite shading.

        Duration: 4 seconds.
      S0: |
        Traditional 2D animation pencil test in the style of classic Disney rough animation. The floating AI news headlines dissolve away as the desk, laptop, monitor, coffee mug, and chair materialize. Sean transitions from a mid-stride walk to a seated working pose at the desk. A subtle 5-o'clock shadow stubble grows in on his face as time passes.

        AUDIO: Faint paper rustle, soft chair creak, quiet pencil tap.

        CAMERA: Completely static, locked tripod.

        STYLE: Graphite on cream paper, rough pencil line quality, organic line wavering, visible construction marks, warm ivory paper tone, flat graphite shading.

        Duration: 4 seconds.

  - id: V05
    name: canonical_camera
    description: "V1 + canonical camera syntax (locked tripod, micro push-in 2%, 50mm look)."
    isolates_axis: E
    prompts:
      W1: |
        Traditional 2D animation pencil test in the style of classic Disney rough animation. Sean walks left to right across the frame at a steady, relaxed pace. His head turns slightly as he takes in the floating Film props around him. The props stay stationary; only Sean moves. Sean is clean-shaven throughout.

        CAMERA: Locked tripod, micro push-in 2%, 50mm look.

        STYLE: Graphite on cream paper, rough pencil line quality, organic line wavering, visible construction marks, warm ivory paper tone, flat graphite shading.

        Duration: 4 seconds.
      S0: |
        Traditional 2D animation pencil test in the style of classic Disney rough animation. The floating AI news headlines dissolve away as the desk, laptop, monitor, coffee mug, and chair materialize. Sean transitions from a mid-stride walk to a seated working pose at the desk. A subtle 5-o'clock shadow stubble grows in on his face as time passes.

        CAMERA: Locked tripod, micro push-in 2%, 50mm look.

        STYLE: Graphite on cream paper, rough pencil line quality, organic line wavering, visible construction marks, warm ivory paper tone, flat graphite shading.

        Duration: 4 seconds.

  - id: V06
    name: no_genre_anchor
    description: "V1 minus genre anchor. Tests whether 'classic Disney rough animation' is load-bearing."
    isolates_axis: A
    prompts:
      W1: |
        Sean walks left to right across the frame at a steady, relaxed pace. His head turns slightly as he takes in the floating Film props around him. The props stay stationary; only Sean moves. Sean is clean-shaven throughout.

        CAMERA: Completely static, locked tripod.

        STYLE: Graphite on cream paper, rough pencil line quality, organic line wavering, visible construction marks, warm ivory paper tone, flat graphite shading.

        Duration: 4 seconds.
      S0: |
        The floating AI news headlines dissolve away as the desk, laptop, monitor, coffee mug, and chair materialize. Sean transitions from a mid-stride walk to a seated working pose at the desk. A subtle 5-o'clock shadow stubble grows in on his face as time passes.

        CAMERA: Completely static, locked tripod.

        STYLE: Graphite on cream paper, rough pencil line quality, organic line wavering, visible construction marks, warm ivory paper tone, flat graphite shading.

        Duration: 4 seconds.

  - id: V07
    name: trimmed_style_block
    description: "V1 with hyper-trimmed style block (3 affirmative descriptors only)."
    isolates_axis: F
    prompts:
      W1: |
        Traditional 2D animation pencil test in the style of classic Disney rough animation. Sean walks left to right across the frame at a steady, relaxed pace. His head turns slightly as he takes in the floating Film props around him. The props stay stationary; only Sean moves. Sean is clean-shaven throughout.

        CAMERA: Completely static, locked tripod.

        STYLE: Graphite on cream paper, organic line wavering, warm ivory tone.

        Duration: 4 seconds.
      S0: |
        Traditional 2D animation pencil test in the style of classic Disney rough animation. The floating AI news headlines dissolve away as the desk, laptop, monitor, coffee mug, and chair materialize. Sean transitions from a mid-stride walk to a seated working pose at the desk. A subtle 5-o'clock shadow stubble grows in on his face as time passes.

        CAMERA: Completely static, locked tripod.

        STYLE: Graphite on cream paper, organic line wavering, warm ivory tone.

        Duration: 4 seconds.

  - id: V08
    name: combined_best
    description: "Combined-best: V2 + V3 + V5 + V7. Tests whether non-mutually-exclusive winners stack."
    isolates_axis: stack
    prompts:
      W1: |
        Traditional 2D animation pencil test in the style of classic Disney rough animation. Starting with Sean stepping into frame from the left amid floating Film props, transitioning through a steady walk cycle with anticipation in his forward weight shift and a slight delayed follow-through as his head turns to take in the props, ending as he approaches the right edge. The props stay stationary; only Sean moves. Sean is clean-shaven throughout.

        CAMERA: Locked tripod, micro push-in 2%, 50mm look.

        STYLE: Graphite on cream paper, organic line wavering, warm ivory tone.

        Duration: 4 seconds.
      S0: |
        Traditional 2D animation pencil test in the style of classic Disney rough animation. Starting with Sean mid-stride amid floating AI news headlines, transitioning through a slow-down anticipation and chair-bend with weight shift settling into a seated pose as the desk, laptop, monitor, coffee mug, and chair materialize, ending in held seated working pose with subtle 5-o'clock shadow stubble grown in.

        CAMERA: Locked tripod, micro push-in 2%, 50mm look.

        STYLE: Graphite on cream paper, organic line wavering, warm ivory tone.

        Duration: 4 seconds.
```

- [ ] **Step 2: Validate the YAML parses**

Run: `python3 -c "import yaml; yaml.safe_load(open('pipeline/seedance_bakeoff_variants.yaml'))"`
Expected: no output (silent success). If a parse error fires, fix the indentation of the offending block and re-run.

- [ ] **Step 3: Sanity-check variant count and shot count**

Run: `python3 -c "import yaml; d=yaml.safe_load(open('pipeline/seedance_bakeoff_variants.yaml')); print(f'variants={len(d[\"variants\"])}, shots={len(d[\"test_shots\"])}, seeds={len(d[\"seeds\"])}')"`
Expected: `variants=9, shots=2, seeds=2`

- [ ] **Step 4: Commit**

```bash
git add pipeline/seedance_bakeoff_variants.yaml
git commit -m "$(cat <<'EOF'
seedance-bakeoff: add variant matrix YAML (9 variants × 2 shots)

V00 control + V01 research-corrected baseline + V02-V07 isolated-axis
variants + V08 combined-best. Anchors reused from seedance_shotlist.yaml
at runtime via shot ID.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Add bake-off helpers to seedance_lib.py

**Files:**
- Modify: `pipeline/seedance_lib.py` (append two helper functions)
- Create: `tests/test_seedance_bakeoff_lib.py` (new test file — first tests in this codebase)

- [ ] **Step 1: Confirm pytest is installed**

This is the first test file in the codebase, so pytest may not yet be in the environment. Run:
```bash
python3 -m pytest --version
```
If it errors with `No module named pytest`, install: `pip install pytest`. Otherwise proceed.

- [ ] **Step 2: Create test directory and write failing tests first**

Create `tests/__init__.py` (empty) and `tests/test_seedance_bakeoff_lib.py`:

```python
"""Tests for the bake-off helpers in seedance_lib.py.

These cover only the pure-function logic (variant loading + run-dir naming).
The orchestrator's API-call paths are integration-tested via the smoke run
in Task 4 and have no unit tests, matching the existing pipeline pattern.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pipeline"))
from seedance_lib import load_bakeoff_variants, make_bakeoff_run_dir


# --- load_bakeoff_variants ---

def test_load_bakeoff_variants_returns_dict_with_expected_keys(tmp_path):
    yaml_path = tmp_path / "v.yaml"
    yaml_path.write_text(
        "version: 1\n"
        "test_shots: [W1, S0]\n"
        "seeds: [42, 1337]\n"
        "defaults:\n"
        "  tier: fast\n"
        "  resolution: 720p\n"
        "variants:\n"
        "  - id: V00\n"
        "    name: control\n"
        "    isolates_axis: control\n"
        "    prompts:\n"
        "      W1: hello\n"
        "      S0: world\n"
    )
    data = load_bakeoff_variants(yaml_path)
    assert data["test_shots"] == ["W1", "S0"]
    assert data["seeds"] == [42, 1337]
    assert len(data["variants"]) == 1
    assert data["variants"][0]["id"] == "V00"
    assert data["variants"][0]["prompts"]["W1"] == "hello"


def test_load_bakeoff_variants_raises_on_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_bakeoff_variants(tmp_path / "missing.yaml")


def test_load_bakeoff_variants_raises_on_missing_required_key(tmp_path):
    yaml_path = tmp_path / "v.yaml"
    yaml_path.write_text("version: 1\ntest_shots: [W1]\n")  # no 'variants' key
    with pytest.raises(ValueError, match="variants"):
        load_bakeoff_variants(yaml_path)


# --- make_bakeoff_run_dir ---

def test_make_bakeoff_run_dir_creates_dir_with_date_suffix(tmp_path):
    run_dir = make_bakeoff_run_dir(base=tmp_path)
    today = datetime.now().strftime("%Y-%m-%d")
    assert run_dir.exists()
    assert run_dir.name == f"seedance-bakeoff-{today}"


def test_make_bakeoff_run_dir_is_idempotent(tmp_path):
    a = make_bakeoff_run_dir(base=tmp_path)
    b = make_bakeoff_run_dir(base=tmp_path)
    assert a == b
    assert a.exists()
```

- [ ] **Step 3: Run tests to verify they fail (functions not yet defined)**

Run: `python3 -m pytest tests/test_seedance_bakeoff_lib.py -v`
Expected: FAIL with `ImportError: cannot import name 'load_bakeoff_variants' from 'seedance_lib'`

- [ ] **Step 4: Add the two helpers to `pipeline/seedance_lib.py`**

Append to the end of `pipeline/seedance_lib.py` (after the `reencode_to_png` function):

```python
# ---------------------------------------------------------------------------
# Bake-off helpers (Phase 2 prompt template bake-off)
# ---------------------------------------------------------------------------


def load_bakeoff_variants(path: str | Path) -> dict:
    """Load and validate the bake-off variants YAML.

    The file must contain at minimum: 'test_shots' (list of shot IDs),
    'seeds' (list of ints), and 'variants' (list of variant dicts, each
    with 'id', 'name', 'isolates_axis', and 'prompts' keys, where
    'prompts' is a dict mapping shot ID -> prompt string).

    Raises FileNotFoundError if missing, ValueError if a required top-level
    key is absent.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Bake-off variants YAML not found: {path}")
    with open(path) as f:
        data = yaml.safe_load(f)

    for required in ("test_shots", "seeds", "variants"):
        if required not in data:
            raise ValueError(
                f"Bake-off variants YAML at {path} missing required key: '{required}'"
            )
    return data


def make_bakeoff_run_dir(base: str | Path = "runs") -> Path:
    """Create runs/seedance-bakeoff-{YYYY-MM-DD}/ and return its path.

    Idempotent: returns the existing path if the directory already exists.
    Does NOT create per-variant subdirs — the orchestrator does that as it
    iterates so partial runs are visible (one variant dir per completed
    variant).
    """
    date_stamp = datetime.now().strftime("%Y-%m-%d")
    run_dir = Path(base) / f"seedance-bakeoff-{date_stamp}"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_seedance_bakeoff_lib.py -v`
Expected: 5 PASS

- [ ] **Step 6: Commit**

```bash
git add pipeline/seedance_lib.py tests/__init__.py tests/test_seedance_bakeoff_lib.py
git commit -m "$(cat <<'EOF'
seedance-bakeoff: add load_bakeoff_variants + make_bakeoff_run_dir helpers

Pure-function helpers for the bake-off orchestrator. Establishes a tests/
directory with the first unit tests in the codebase — covers only the
pure-function logic; orchestrator API paths are integration-tested via
the live smoke run.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Create the bake-off orchestrator

**Files:**
- Create: `pipeline/seedance_bakeoff.py`

- [ ] **Step 1: Create the orchestrator script**

Create `pipeline/seedance_bakeoff.py` with the following content:

```python
"""Seedance prompt template bake-off orchestrator.

Iterates: variant × shot × seed -> Seedance API submission, polling, download.
Mirrors the async-batch pattern from seedance_generate.py --all so multiple
generations run concurrently on fal.ai.

CLI:
    # Full bake-off (9 variants × 2 shots × 2 seeds = 36 generations):
    python3 pipeline/seedance_bakeoff.py

    # Smoke test (single cell):
    python3 pipeline/seedance_bakeoff.py --variants V00 --shots W1 --seeds 42

    # Resume an in-progress run dir (refuses to overwrite existing MP4s):
    python3 pipeline/seedance_bakeoff.py --run-dir runs/seedance-bakeoff-2026-05-09

Outputs (per cell):
    {run_dir}/V{NN}_{name}/{shot_id}/seed_{NNNN}/output.mp4
    {run_dir}/V{NN}_{name}/{shot_id}/seed_{NNNN}/meta.json
    {run_dir}/anchor_urls.json                  (cache — reused across cells)
    {run_dir}/audit/bakeoff_log.jsonl           (submit + generated events)
    {run_dir}/manifest.lock.yaml                (frozen run config)
    {run_dir}/scoring.csv                       (empty rubric template)
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

# Project-local imports
sys.path.insert(0, str(Path(__file__).parent))
from seedance_lib import (
    load_bakeoff_variants,
    load_env,
    load_shotlist,
    log_event,
    make_bakeoff_run_dir,
    upload_anchor,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_MODEL_IDS = {
    "fast": "bytedance/seedance-2.0/fast/image-to-video",
    "standard": "bytedance/seedance-2.0/image-to-video",
}
_API_MIN_DURATION = 4
_COST_PER_SECOND = {"fast": 0.24, "standard": 0.48}

# 5 binary scoring criteria — matches design spec §4.4
_SCORING_CRITERIA = [
    "c1_style",       # style preservation
    "c2_identity",    # identity preservation
    "c3_motion",      # motion plausibility
    "c4_artifacts",   # absence of artifacts
    "c5_anchor",      # anchor adherence
]


# ---------------------------------------------------------------------------
# Cell-path helpers
# ---------------------------------------------------------------------------

def _variant_dir_name(variant: dict) -> str:
    """Return the per-variant subdir name, e.g. 'V00_v3_control'."""
    return f"{variant['id']}_{variant['name']}"


def _cell_dir(run_dir: Path, variant: dict, shot_id: str, seed: int) -> Path:
    """Return the directory for a single (variant, shot, seed) cell."""
    return run_dir / _variant_dir_name(variant) / shot_id / f"seed_{seed:04d}"


# ---------------------------------------------------------------------------
# Manifest + scoring template generation
# ---------------------------------------------------------------------------

def write_manifest(
    run_dir: Path,
    variants_data: dict,
    cli_args: argparse.Namespace,
) -> None:
    """Write {run_dir}/manifest.lock.yaml with the frozen run config."""
    import yaml

    manifest = {
        "run_started_at": datetime.now().isoformat(timespec="seconds"),
        "variants_file": str(Path(cli_args.variants_file).resolve()),
        "shotlist_file": str(Path(cli_args.shotlist).resolve()),
        "tier": cli_args.tier,
        "resolution": cli_args.resolution,
        "selected_variants": cli_args.variants or [v["id"] for v in variants_data["variants"]],
        "selected_shots": cli_args.shots or variants_data["test_shots"],
        "selected_seeds": cli_args.seeds or variants_data["seeds"],
    }
    (run_dir / "manifest.lock.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False))


def write_scoring_template(run_dir: Path, cells: list[dict]) -> None:
    """Write empty scoring.csv with one row per cell.

    Refuses to overwrite an existing file (preserves manual scores between runs).
    """
    csv_path = run_dir / "scoring.csv"
    if csv_path.exists():
        print(f"  Scoring template already exists at {csv_path} — keeping existing scores.")
        return

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["variant_id", "variant_name", "shot", "seed"]
            + _SCORING_CRITERIA
            + ["total", "notes"]
        )
        for cell in cells:
            writer.writerow(
                [cell["variant"]["id"], cell["variant"]["name"], cell["shot_id"], cell["seed"]]
                + ["" for _ in _SCORING_CRITERIA]
                + ["", ""]
            )
    print(f"  Wrote scoring template: {csv_path}")


# ---------------------------------------------------------------------------
# Cell submission + polling (mirrors seedance_generate.py async-batch)
# ---------------------------------------------------------------------------

def _build_arguments(prompt: str, start_url: str, end_url: str, resolution: str, seed: int) -> dict:
    return {
        "prompt": prompt,
        "image_url": start_url,
        "end_image_url": end_url,
        "resolution": resolution,
        "duration": str(_API_MIN_DURATION),
        "generate_audio": False,
        "seed": seed,
    }


def _submit_cell(
    cell: dict,
    shot: dict,
    model_id: str,
    run_dir: Path,
    cache_path: Path,
    resolution: str,
    tier: str,
) -> dict:
    """Submit one cell to fal.ai. Returns in-flight job dict."""
    import fal_client  # deferred

    variant = cell["variant"]
    shot_id = cell["shot_id"]
    seed = cell["seed"]
    prompt = variant["prompts"][shot_id]

    start_url = upload_anchor(shot["start"], cache_path)
    end_url = upload_anchor(shot["end"], cache_path)

    arguments = _build_arguments(prompt, start_url, end_url, resolution, seed)

    log_event(
        run_dir,
        {
            "event": "bakeoff_submit",
            "variant_id": variant["id"],
            "variant_name": variant["name"],
            "shot": shot_id,
            "seed": seed,
            "tier": tier,
            "resolution": resolution,
            "model": model_id,
            "anchor_urls": {"start": start_url, "end": end_url},
        },
    )

    handler = fal_client.submit(model_id, arguments=arguments)
    return {
        "cell": cell,
        "shot": shot,
        "model_id": model_id,
        "handler": handler,
        "request_id": handler.request_id,
        "arguments": arguments,
        "anchor_urls": {"start": start_url, "end": end_url},
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "wall_start": datetime.now(),
        "status": "PENDING",
    }


def _download_mp4(video_url: str, local_mp4: Path) -> None:
    try:
        urllib.request.urlretrieve(video_url, local_mp4)
    except Exception as exc:
        print(f"  urlretrieve failed ({exc}), trying urlopen fallback …")
        with urllib.request.urlopen(video_url) as resp:
            local_mp4.write_bytes(resp.read())


def _handle_completion(job: dict, run_dir: Path, tier: str) -> tuple[bool, str]:
    """Process a Completed result for one job. Returns (succeeded, message)."""
    import fal_client

    cell = job["cell"]
    variant = cell["variant"]
    shot_id = cell["shot_id"]
    seed = cell["seed"]
    request_id = job["request_id"]

    cell_path = _cell_dir(run_dir, variant, shot_id, seed)
    cell_path.mkdir(parents=True, exist_ok=True)
    local_mp4 = cell_path / "output.mp4"

    if local_mp4.exists():
        return False, f"refusing to overwrite {local_mp4}"

    try:
        result = fal_client.result(job["model_id"], request_id)
        video_url = result["video"]["url"]
        returned_seed = result.get("seed")
        completed_at = datetime.now().isoformat(timespec="seconds")
        wall_s = (datetime.now() - job["wall_start"]).total_seconds()

        _download_mp4(video_url, local_mp4)
        size_mb = local_mp4.stat().st_size / (1024 * 1024)

        meta = {
            "variant_id": variant["id"],
            "variant_name": variant["name"],
            "isolates_axis": variant.get("isolates_axis"),
            "shot_id": shot_id,
            "seed_requested": seed,
            "seed_returned": returned_seed,
            "tier": tier,
            "resolution": job["arguments"]["resolution"],
            "duration_s": _API_MIN_DURATION,
            "model_id": job["model_id"],
            "prompt": variant["prompts"][shot_id],
            "anchor_urls": job["anchor_urls"],
            "anchor_paths": {"start": job["shot"]["start"], "end": job["shot"]["end"]},
            "fal_request_id": request_id,
            "video_url": video_url,
            "video_size_bytes": local_mp4.stat().st_size,
            "started_at": job["started_at"],
            "completed_at": completed_at,
            "wall_clock_s": round(wall_s, 1),
        }
        (cell_path / "meta.json").write_text(json.dumps(meta, indent=2))

        log_event(
            run_dir,
            {
                "event": "bakeoff_generated",
                "variant_id": variant["id"],
                "shot": shot_id,
                "seed": seed,
                "video_path": str(local_mp4),
                "video_size_bytes": local_mp4.stat().st_size,
                "fal_request_id": request_id,
                "wall_clock_s": round(wall_s, 1),
            },
        )

        cost = _API_MIN_DURATION * _COST_PER_SECOND[tier]
        return True, f"{size_mb:.2f} MB, ~${cost:.2f}, {wall_s:.0f}s"
    except Exception as exc:
        log_event(
            run_dir,
            {
                "event": "bakeoff_failed",
                "variant_id": variant["id"],
                "shot": shot_id,
                "seed": seed,
                "fal_request_id": request_id,
                "error": str(exc),
            },
        )
        return False, str(exc)


# ---------------------------------------------------------------------------
# Main run loop
# ---------------------------------------------------------------------------

def _build_cells(
    variants_data: dict,
    selected_variants: list[str] | None,
    selected_shots: list[str] | None,
    selected_seeds: list[int] | None,
) -> list[dict]:
    """Compose the (variant, shot, seed) cell list, filtered by CLI selections."""
    variants = variants_data["variants"]
    if selected_variants:
        variants = [v for v in variants if v["id"] in selected_variants]
    shots = selected_shots or variants_data["test_shots"]
    seeds = selected_seeds or variants_data["seeds"]

    cells: list[dict] = []
    for variant in variants:
        for shot_id in shots:
            for seed in seeds:
                cells.append({"variant": variant, "shot_id": shot_id, "seed": seed})
    return cells


def run_bakeoff(args: argparse.Namespace) -> None:  # noqa: C901
    """Submit all cells, poll until done, write outputs + scoring template."""
    import fal_client
    from fal_client.client import Completed, InProgress, Queued

    load_env(".env")
    variants_data = load_bakeoff_variants(args.variants_file)
    shotlist = load_shotlist(args.shotlist)
    shots_by_id: dict[str, dict] = {s["id"]: s for s in shotlist.get("shots", [])}

    # Resolve run dir
    if args.run_dir:
        run_dir = Path(args.run_dir)
        if not run_dir.exists():
            sys.exit(f"--run-dir '{run_dir}' does not exist. Omit to auto-create.")
        (run_dir / "audit").mkdir(exist_ok=True)
    else:
        run_dir = make_bakeoff_run_dir()
        (run_dir / "audit").mkdir(exist_ok=True)

    cache_path = run_dir / "anchor_urls.json"
    write_manifest(run_dir, variants_data, args)

    # Scoring CSV must always cover the full 9×2×2 matrix, even on filtered runs.
    # (Otherwise a smoke run with --variants V00 would leave a 1-row CSV that
    # the next full run won't overwrite, since write_scoring_template refuses to clobber.)
    full_matrix_cells = _build_cells(variants_data, None, None, None)
    write_scoring_template(run_dir, full_matrix_cells)

    # Compose this invocation's cells (filtered by CLI), then drop any whose MP4
    # already exists so reruns and resumes work cleanly.
    filtered_cells = _build_cells(variants_data, args.variants, args.shots, args.seeds)
    cells_to_run: list[dict] = []
    pre_existing: list[str] = []
    for cell in filtered_cells:
        if cell["shot_id"] not in shots_by_id:
            sys.exit(
                f"Shot '{cell['shot_id']}' not found in {args.shotlist}. "
                f"Available: {list(shots_by_id)}"
            )
        local_mp4 = _cell_dir(run_dir, cell["variant"], cell["shot_id"], cell["seed"]) / "output.mp4"
        if local_mp4.exists():
            pre_existing.append(f"{cell['variant']['id']}/{cell['shot_id']}/seed_{cell['seed']}")
            continue
        cells_to_run.append(cell)

    if not cells_to_run:
        print("\nNo cells to run (all already complete).")
        return

    print(f"\nRun dir:      {run_dir}")
    print(f"Tier:         {args.tier}  (${_COST_PER_SECOND[args.tier]}/s)")
    print(f"Resolution:   {args.resolution}")
    print(f"Cells to run: {len(cells_to_run)}")
    print(f"Pre-existing: {len(pre_existing)} (will skip)")
    print(f"Est. cost:    ~${len(cells_to_run) * _API_MIN_DURATION * _COST_PER_SECOND[args.tier]:.2f}")
    print()

    model_id = _MODEL_IDS[args.tier]

    # Pre-upload all unique anchors (idempotent via cache)
    print("=== Uploading anchors ===")
    unique_anchors: set[str] = set()
    for cell in cells_to_run:
        s = shots_by_id[cell["shot_id"]]
        unique_anchors.add(s["start"])
        unique_anchors.add(s["end"])
    for anchor in sorted(unique_anchors):
        upload_anchor(anchor, cache_path)
        print(f"  cached: {anchor}")
    print()

    # Submit all cells
    print("=== Submitting jobs ===")
    in_flight: list[dict] = []
    batch_start = datetime.now()

    for cell in cells_to_run:
        cid = f"{cell['variant']['id']}/{cell['shot_id']}/seed_{cell['seed']}"
        try:
            job = _submit_cell(
                cell=cell,
                shot=shots_by_id[cell["shot_id"]],
                model_id=model_id,
                run_dir=run_dir,
                cache_path=cache_path,
                resolution=args.resolution,
                tier=args.tier,
            )
            in_flight.append(job)
            print(f"  submitted {cid}  request_id={job['request_id']}")
        except Exception as exc:
            print(f"  ❌ {cid} SUBMIT FAILED: {exc}")
            log_event(run_dir, {"event": "bakeoff_submit_failed", "cell": cid, "error": str(exc)})

    print(f"\n{len(in_flight)} jobs in flight. Polling every 15s …\n")

    # Poll until done
    pending = list(in_flight)
    generated: list[str] = []
    failed: list[tuple[str, str]] = []

    while pending:
        time.sleep(15)
        elapsed = (datetime.now() - batch_start).total_seconds()
        elapsed_str = f"{int(elapsed // 60):02d}:{int(elapsed % 60):02d}"

        still_pending: list[dict] = []
        progress: list[str] = []

        for job in pending:
            cell = job["cell"]
            cid = f"{cell['variant']['id']}/{cell['shot_id']}/seed_{cell['seed']}"
            try:
                st = fal_client.status(job["model_id"], job["request_id"])
            except Exception as exc:
                progress.append(f"{cid}=ERR")
                still_pending.append(job)
                continue

            if isinstance(st, Queued):
                progress.append(f"{cid}=Q{st.position}")
                still_pending.append(job)
            elif isinstance(st, InProgress):
                progress.append(f"{cid}=IP")
                still_pending.append(job)
            elif isinstance(st, Completed):
                if st.error:
                    progress.append(f"{cid}=FAIL")
                    failed.append((cid, f"{st.error} (type={st.error_type})"))
                    log_event(run_dir, {
                        "event": "bakeoff_failed",
                        "cell": cid,
                        "error": str(st.error),
                    })
                else:
                    progress.append(f"{cid}=OK")
                    ok, msg = _handle_completion(job, run_dir, args.tier)
                    if ok:
                        generated.append(cid)
                        print(f"\n  ✅ {cid}  {msg}")
                    else:
                        failed.append((cid, msg))
                        print(f"\n  ❌ {cid}  {msg}")
            else:
                progress.append(f"{cid}=?")
                still_pending.append(job)

        # Compact status line — chunk to keep it readable
        chunks = [progress[i:i + 6] for i in range(0, len(progress), 6)]
        for chunk in chunks:
            print(f"[{elapsed_str}] {' | '.join(chunk)}")
        pending = still_pending

    # Summary
    total_wall = (datetime.now() - batch_start).total_seconds()
    total_cost = len(generated) * _API_MIN_DURATION * _COST_PER_SECOND[args.tier]

    print("\n=== Bake-off complete ===")
    print(f"✅ Generated: {len(generated)}/{len(in_flight)}")
    print(f"❌ Failed:    {len(failed)}")
    print(f"Total wall-clock: {int(total_wall // 60)}m {int(total_wall % 60)}s")
    print(f"Total cost:       ~${total_cost:.2f}")
    print(f"Run dir:          {run_dir}")
    print(f"Scoring CSV:      {run_dir}/scoring.csv  (open in any spreadsheet tool)")
    if failed:
        print("\nFailed cells (re-run with --variants/--shots/--seeds to retry):")
        for cid, msg in failed:
            print(f"  {cid}: {msg}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="seedance_bakeoff.py",
        description="Run the 9-variant Seedance prompt template bake-off.",
    )
    p.add_argument(
        "--variants-file",
        default="pipeline/seedance_bakeoff_variants.yaml",
        help="Path to bake-off variants YAML.",
    )
    p.add_argument(
        "--shotlist",
        default="pipeline/seedance_shotlist.yaml",
        help="Path to shot-list YAML (anchors come from here by shot ID).",
    )
    p.add_argument(
        "--variants",
        nargs="+",
        default=None,
        metavar="ID",
        help="Subset of variant IDs to run (e.g. V00 V01). Default: all.",
    )
    p.add_argument(
        "--shots",
        nargs="+",
        default=None,
        metavar="ID",
        help="Subset of shot IDs to run (default: all from variants YAML).",
    )
    p.add_argument(
        "--seeds",
        nargs="+",
        type=int,
        default=None,
        metavar="N",
        help="Subset of seeds (default: all from variants YAML).",
    )
    p.add_argument(
        "--tier",
        choices=["fast", "standard"],
        default="fast",
    )
    p.add_argument(
        "--resolution",
        choices=["480p", "720p"],
        default="720p",
    )
    p.add_argument(
        "--run-dir",
        default=None,
        help="Reuse an existing run dir (resumes — skips cells whose MP4 exists).",
    )
    return p


def main() -> None:
    args = build_parser().parse_args()
    run_bakeoff(args)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verify the script imports without error**

Run: `python3 -c "import sys; sys.path.insert(0, 'pipeline'); import seedance_bakeoff"`
Expected: no output (silent success).

- [ ] **Step 3: Verify the CLI parses --help**

Run: `python3 pipeline/seedance_bakeoff.py --help`
Expected: argparse usage output listing `--variants-file`, `--shotlist`, `--variants`, `--shots`, `--seeds`, `--tier`, `--resolution`, `--run-dir`.

- [ ] **Step 4: Verify cell composition without API calls**

Run a dry import check that exercises `_build_cells`:
```bash
python3 -c "
import sys; sys.path.insert(0, 'pipeline')
from seedance_bakeoff import _build_cells
from seedance_lib import load_bakeoff_variants
data = load_bakeoff_variants('pipeline/seedance_bakeoff_variants.yaml')
cells = _build_cells(data, None, None, None)
print(f'total cells: {len(cells)}')
print(f'first: {cells[0][\"variant\"][\"id\"]}/{cells[0][\"shot_id\"]}/seed_{cells[0][\"seed\"]}')
print(f'last:  {cells[-1][\"variant\"][\"id\"]}/{cells[-1][\"shot_id\"]}/seed_{cells[-1][\"seed\"]}')
"
```
Expected: `total cells: 36`, first = `V00/W1/seed_42`, last = `V08/S0/seed_1337`.

- [ ] **Step 5: Commit**

```bash
git add pipeline/seedance_bakeoff.py
git commit -m "$(cat <<'EOF'
seedance-bakeoff: add bake-off orchestrator

Iterates variant × shot × seed (9 × 2 × 2 = 36 cells), submits async to
fal.ai, polls every 15s, downloads MP4s into per-cell subdirs, writes
manifest.lock.yaml + empty scoring.csv. Refuses to overwrite existing
output.mp4 — supports --run-dir for resume after partial runs.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: Smoke test — single-cell live run

This task burns ~$1 on a real Fal.ai call to verify the harness end-to-end before committing to the full $35 run.

**Files:**
- Reads: `.env` (must contain `FAL_KEY=...`)
- Writes (at runtime): `runs/seedance-bakeoff-2026-05-09/V00_v3_control/W1/seed_0042/{output.mp4, meta.json}`

- [ ] **Step 1: Confirm the FAL_KEY is set in .env**

Run: `grep -q '^FAL_KEY=' .env && echo OK || echo MISSING`
Expected: `OK`. If `MISSING`, add `FAL_KEY=<your-key>` to `.env` before continuing.

- [ ] **Step 2: Run a single-cell smoke test**

Run:
```bash
python3 pipeline/seedance_bakeoff.py \
  --variants V00 \
  --shots W1 \
  --seeds 42
```
Expected: ~60–180s wall-clock. Output ends with `✅ Generated: 1/1`. Cost: ~$0.97.

- [ ] **Step 3: Inspect the output MP4**

Run: `open runs/seedance-bakeoff-2026-05-09/V00_v3_control/W1/seed_0042/output.mp4`
Expected: a ~4-second 720p video plays. The aesthetic and motion don't have to be perfect — we're verifying the harness works, not the prompt.

- [ ] **Step 4: Inspect the meta JSON**

Run: `cat runs/seedance-bakeoff-2026-05-09/V00_v3_control/W1/seed_0042/meta.json`
Expected: JSON with `variant_id: V00`, `shot_id: W1`, `seed_returned: <int>`, `fal_request_id`, `prompt`, etc.

- [ ] **Step 5: Inspect the bakeoff log**

Run: `cat runs/seedance-bakeoff-2026-05-09/audit/seedance_log.jsonl`
Expected: at least 2 lines — one `bakeoff_submit` event, one `bakeoff_generated` event.

- [ ] **Step 6: Verify the manifest and scoring template were written**

Run:
```bash
ls runs/seedance-bakeoff-2026-05-09/manifest.lock.yaml runs/seedance-bakeoff-2026-05-09/scoring.csv
head -3 runs/seedance-bakeoff-2026-05-09/scoring.csv
```
Expected: both files exist; scoring.csv header is `variant_id,variant_name,shot,seed,c1_style,c2_identity,c3_motion,c4_artifacts,c5_anchor,total,notes` followed by rows for all 36 cells.

- [ ] **Step 7: STOP if anything looks broken**

If steps 2–6 produced unexpected output, do NOT proceed to the full bake-off. Diagnose and fix the orchestrator first. The smoke test exists specifically to catch bugs before the $35 run.

**No commit at this step** — runtime artifacts are gitignored, no code changed.

---

## Task 5: Run the full bake-off

This is the $35 run. Hands-off after kickoff.

- [ ] **Step 1: Run the full matrix, skipping the V00/W1/seed_42 cell already generated**

The orchestrator's resume logic detects the existing MP4 and skips it automatically. Just run:
```bash
python3 pipeline/seedance_bakeoff.py
```
Expected: `Cells to run: 35`, `Pre-existing: 1 (will skip)`, est. cost `~$33.95`.

The run takes ~30–60 minutes wall-clock as fal.ai processes the queue.

- [ ] **Step 2: Walk away — observe the polling output periodically**

Each line shows `[mm:ss] V00/W1/seed_42=OK | V00/S0/seed_42=IP | …`. If a cell hits ERR or FAIL, that's recoverable — see Step 4.

- [ ] **Step 3: Confirm completion summary**

When the run ends, the script prints a summary. Expected:
- `✅ Generated: 36/36` (or `35/35` if step 1 skipped one)
- `❌ Failed: 0`

If `Failed > 0`, note the failed cell IDs.

- [ ] **Step 4: Re-run any failed cells**

For each `cid` (e.g. `V03/S0/seed_1337`) that failed, re-run that cell only:
```bash
python3 pipeline/seedance_bakeoff.py \
  --variants V03 \
  --shots S0 \
  --seeds 1337 \
  --run-dir runs/seedance-bakeoff-2026-05-09
```
The `--run-dir` flag reuses the existing dir; resume logic skips the cells that already succeeded.

- [ ] **Step 5: Verify all 36 cells produced output**

Run:
```bash
find runs/seedance-bakeoff-2026-05-09 -name 'output.mp4' | wc -l
```
Expected: `36`. If less, identify the gaps with:
```bash
find runs/seedance-bakeoff-2026-05-09 -mindepth 3 -maxdepth 3 -type d ! -exec test -e {}/output.mp4 \; -print
```

**No commit at this step** — runtime artifacts.

---

## Task 6: Manual scoring (human gate)

The 5-criteria binary rubric is in `scoring.csv`. This is Sean's eyeball pass.

- [ ] **Step 1: Open the scoring CSV in a spreadsheet tool**

Run: `open runs/seedance-bakeoff-2026-05-09/scoring.csv`
(Opens in Numbers / Excel / whatever the system handles `.csv` with.)

- [ ] **Step 2: Score each cell against the 5 binary criteria**

For each row, watch the corresponding MP4 (path constructed from variant_id + shot + seed) and answer each criterion 1 (yes) or 0 (no):

| Column | Question |
|---|---|
| `c1_style` | Does the clip maintain rough pencil line quality, paper grain, and visible construction marks throughout — without digital smoothing, anime stylization, or photoreal rendering creeping in? |
| `c2_identity` | Does Sean remain recognizably himself from frame 1 to last frame, matching the start anchor and arriving at the end anchor? |
| `c3_motion` | Is the action physically and anatomically coherent (no morphing limbs, no warping, no rubber-banding)? |
| `c4_artifacts` | Is the clip free of major artifacts (flickering, ghosting, hand/finger distortion, texture crawl, jitter)? |
| `c5_anchor` | Do the start and end of the clip plausibly match the start and end anchor frames (composition, pose, environment all line up at boundaries)? |

Then fill `total` = sum of the 5 columns (0–5 per cell).

Use the `notes` column to capture anything specific that helps later synthesis (e.g. "stylus shows up briefly at frame 30", "head morphs at end").

To open a specific clip from a CSV row:
```bash
open runs/seedance-bakeoff-2026-05-09/V03_animation_timing/W1/seed_0042/output.mp4
```

Score one variant at a time (4 clips per variant) for consistency.

- [ ] **Step 3: Save the scored CSV**

Save it back to the same path. The synthesis step in Task 7 reads from this file.

**No commit at this step** — runtime artifacts.

---

## Task 7: Synthesize results

**Files:**
- Read: `runs/seedance-bakeoff-2026-05-09/scoring.csv`
- Create: `runs/seedance-bakeoff-2026-05-09/results.md`
- Create: `docs/2026-05-09-seedance-prompt-bakeoff-results.md` (committed copy)

- [ ] **Step 1: Generate per-variant totals from the CSV**

Run:
```bash
python3 -c "
import csv
from collections import defaultdict
rows = list(csv.DictReader(open('runs/seedance-bakeoff-2026-05-09/scoring.csv')))
totals = defaultdict(lambda: {'W1': 0, 'S0': 0})
for r in rows:
    if r['total'].strip():
        totals[r['variant_id']][r['shot']] += int(r['total'])
print(f'{\"variant\":<6} {\"W1\":>4} {\"S0\":>4} {\"sum\":>5}')
for vid in sorted(totals):
    w1, s0 = totals[vid]['W1'], totals[vid]['S0']
    print(f'{vid:<6} {w1:>4} {s0:>4} {w1+s0:>5}')
"
```
Expected: a table of variant totals, max 20 per variant (10 per shot × 2 shots).

Note the **winner** (highest sum). If tied, the **identity-stress shot (S0) score** is tiebreaker 1; **shorter prompt** is tiebreaker 2.

- [ ] **Step 2: Apply halt conditions**

- If V00 wins by 2+ points over V01 → research-derived priors are wrong. **STOP**, investigate, and report back before locking the template.
- If no variant reaches ≥14/20 on the S0 score → template is fundamentally weak. **STOP** and revisit Phase 1 with a fourth focused research query.

If neither halt fires, proceed.

- [ ] **Step 3: Create results.md in the run dir**

Create `runs/seedance-bakeoff-2026-05-09/results.md` with this structure:

```markdown
# Seedance Prompt Bake-off — Results

**Date:** 2026-05-09
**Run dir:** `runs/seedance-bakeoff-2026-05-09/`
**Total cost:** $<actual from summary>
**Total wall-clock:** <actual from summary>

## Per-variant scores (max 20)

| Variant | Name | Axis | W1 (max 10) | S0 (max 10) | Total | Δ vs V01 |
|---|---|---|---|---|---|---|
| V00 | v3_control | control | <fill> | <fill> | <fill> | <fill> |
| V01 | research_corrected_baseline | baseline | <fill> | <fill> | <fill> | 0 |
| V02 | transition_arc | B | <fill> | <fill> | <fill> | <fill> |
| V03 | animation_timing | C | <fill> | <fill> | <fill> | <fill> |
| V04 | audio_cues | D | <fill> | <fill> | <fill> | <fill> |
| V05 | canonical_camera | E | <fill> | <fill> | <fill> | <fill> |
| V06 | no_genre_anchor | A | <fill> | <fill> | <fill> | <fill> |
| V07 | trimmed_style_block | F | <fill> | <fill> | <fill> | <fill> |
| V08 | combined_best | stack | <fill> | <fill> | <fill> | <fill> |

## Winner

**Variant:** V<XX> (<name>)
**Score:** <X>/20
**Margin over V01:** +<X> points

## Per-axis findings

- **Axis A (genre anchor — V06 vs V01):** <effect: helped/hurt/neutral>, evidence: <notes>
- **Axis B (transition-arc — V02 vs V01):** <effect>, evidence: <notes>
- **Axis C (animation-timing — V03 vs V01):** <effect>, evidence: <notes>
- **Axis D (audio cues — V04 vs V01):** <effect>, evidence: <notes>
- **Axis E (canonical camera — V05 vs V01):** <effect>, evidence: <notes>
- **Axis F (style block density — V07 vs V01):** <effect>, evidence: <notes>
- **Stack (combined-best — V08 vs winner of B/C/E/F):** <stacks cleanly / interferes>, evidence: <notes>

## Failure modes observed

<bullet list of common failure patterns from the 'notes' column, e.g. style drift, identity warping, hand artifacts>

## Variants disqualified by halt conditions

<list any variant that scored ≤10 — these are clearly broken and shouldn't influence the template>

## Decision

Lock template based on V<winner> structure. See `prompts/seedance-template-v4.md`.
```

Fill in every `<placeholder>` with actual scoring data and observations from the `notes` column.

- [ ] **Step 4: Copy results to docs/ for git tracking**

Run: `cp runs/seedance-bakeoff-2026-05-09/results.md docs/2026-05-09-seedance-prompt-bakeoff-results.md`

(The `runs/` directory is gitignored; the committed copy in `docs/` preserves evidence.)

- [ ] **Step 5: Commit**

```bash
git add docs/2026-05-09-seedance-prompt-bakeoff-results.md
git commit -m "$(cat <<'EOF'
seedance-bakeoff: results synthesis

Per-variant scores + per-axis findings + failure-mode log from the
9 × 2 × 2 = 36-cell bake-off. Locks the winning variant for v4 template.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: Lock the winning template

**Files:**
- Create: `prompts/seedance-template-v4.md`

- [ ] **Step 1: Identify the winning variant's structural elements**

From `docs/2026-05-09-seedance-prompt-bakeoff-results.md`, note:
- Winning variant ID
- Whether genre anchor is present
- Action framing (action-arc vs transition-arc)
- Motion language (prose vs animation-timing)
- Audio block (yes/no)
- Camera syntax (plain vs canonical)
- Style block density (full vs trimmed)

- [ ] **Step 2: Create the template doc**

Create `prompts/seedance-template-v4.md`. Replace `<...>` placeholders with the winner's actual structural choices:

```markdown
# Seedance 2.0 Prompt Template — v4

> **Status:** Locked 2026-05-09 — winning structure from the prompt bake-off (Variant <V>, score <X>/20).
> **Supersedes:** [docs/2026-05-02-act2-seedance-prompts-v3-conversation-style.md](2026-05-02-act2-seedance-prompts-v3-conversation-style.md) (v3)
> **Evidence:** [docs/2026-05-09-seedance-prompt-bakeoff-results.md](2026-05-09-seedance-prompt-bakeoff-results.md)
> **Design spec:** [docs/2026-05-09-seedance-prompt-bakeoff-design.md](2026-05-09-seedance-prompt-bakeoff-design.md)

## When to use this template

For all Seedance 2.0 image-to-video generations on hand-drawn pencil-test aesthetic content. Fill in the `[BRACKETED]` placeholders with shot-specific content; leave the structural scaffolding alone.

## The template

```
<paste the winning variant's structural skeleton here, replacing the W1-specific
content with [BRACKETED PLACEHOLDERS]. For example, if V08 won:

Traditional 2D animation pencil test in the style of classic Disney rough animation. Starting with [SHOT START STATE], transitioning through [SHOT MIDDLE BEAT], ending with [SHOT END STATE]. [SHOT-SPECIFIC CONTINUITY REMINDER — clean-shaven / stubble / no stylus / wardrobe note].

CAMERA: Locked tripod, micro push-in 2%, 50mm look.

STYLE: Graphite on cream paper, organic line wavering, warm ivory tone.

Duration: [N] seconds.
>
```

## Locked rules (do NOT relax)

These are baked in by the research priors and the bake-off evidence. Modifying them invalidates the template.

1. **Word count target: 80–100 words.** Hard cap 100. <30 hallucinates, >150 attention-collapses.
2. **No in-prompt negation.** Never write "no X." Replace every negative with an affirmative descriptor.
3. **Banned words.** Never use: `cinematic`, `4K`, `8K`, `ultra high res`, `sharp focus`, `polished`, `smooth`, `highly detailed`, `studio-quality`, `masterpiece`, `lens` (standalone), `anime` (unqualified).
4. **Don't redescribe the frames.** The start/end anchors carry composition, pose, line quality, paper grain. Don't restate.
5. **Single camera instruction.** Multiple camera directives produce jitter.
6. **Affirmative material descriptors only.** "Graphite on cream paper, organic line wavering, warm ivory tone" — what you DO want, never what you don't.

## Per-axis verdicts (from the bake-off)

<paste verdict from each axis test from results.md, e.g.:

- **Genre anchor (Axis A):** KEEP. Removing it dropped W1 score by N points and S0 score by N. The "classic Disney rough animation" anchor is load-bearing on Seedance.
- **Action framing (Axis B):** USE TRANSITION-ARC for start+end frame mode. V02 outscored V01 on S0 by N points.
- **Animation-timing language (Axis C):** USE. anticipation/hold/snap/settle outperformed prose motion by N points on the motion-stress shot.
... etc.
>

## Filling out the template

For a new shot:

1. Identify the **start state**, **middle beat**, and **end state** (transition-arc framing requires you to think in 3 beats).
2. Identify the **continuity reminder** for that shot (clean-shaven / stubble / no stylus / wardrobe).
3. Adjust the duration if the shot isn't 4s. (Seedance API minimum is 4s; if your shot is 3s, clamp to 4 and trim in assembly.)
4. Drop the filled prompt into the API call. Use the `seedance_generate.py` script with `--shot <ID>` if your shot is registered in `seedance_shotlist.yaml`.

## Example fills (from Act 2 production)

<after Phase 3 starts, append concrete examples here as Act 2 shots are written>
```

Fill in the actual winning structure based on the bake-off results. The placeholder `<paste the winning variant's structural skeleton here>` is your responsibility — it must be the literal structure of the winning variant, not a guess.

- [ ] **Step 3: Sanity-check the template**

Run: `wc -w prompts/seedance-template-v4.md`
Expected: a reasonable line count. Then visually verify all `<placeholder>` markers from Step 2 are replaced.

- [ ] **Step 4: Commit**

```bash
git add prompts/seedance-template-v4.md
git commit -m "$(cat <<'EOF'
seedance-template-v4: lock winning prompt structure

Winning variant from the 2026-05-09 bake-off. Supersedes v3 conversation-
style structure. Captures the structural rules + per-axis verdicts so
future projects can lift the template verbatim.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 9: Standard-tier verification on the identity-stress shot

A single Standard-tier run confirms the winner's quality scales Fast→Standard.

- [ ] **Step 1: Generate the winning variant on S0 at Standard tier in a separate run dir**

Use a fresh run dir to avoid colliding with the existing Fast-tier output (the orchestrator refuses to overwrite). Substitute `<VWINNER>` with the actual winning variant ID (e.g. `V08`):

```bash
mkdir -p runs/seedance-bakeoff-2026-05-09-standard-verify
python3 pipeline/seedance_bakeoff.py \
  --variants <VWINNER> \
  --shots S0 \
  --seeds 42 \
  --tier standard \
  --run-dir runs/seedance-bakeoff-2026-05-09-standard-verify
```
Expected: ~1 minute, ~$1.92 cost. Output at `runs/seedance-bakeoff-2026-05-09-standard-verify/<VWINNER>_<name>/S0/seed_0042/output.mp4`.

- [ ] **Step 2: Compare Fast vs Standard side-by-side**

Open both:
```bash
open runs/seedance-bakeoff-2026-05-09/<VWINNER>_<name>/S0/seed_0042/output.mp4
open runs/seedance-bakeoff-2026-05-09-standard-verify/<VWINNER>_<name>/S0/seed_0042/output.mp4
```

Score the Standard run on the same 5-criteria rubric. Expected: Standard score ≥ Fast score (Standard should be at least as good; usually slightly cleaner).

- [ ] **Step 3: Append Standard-tier verdict to results.md**

Append a section to `docs/2026-05-09-seedance-prompt-bakeoff-results.md`:

```markdown
## Standard-tier verification

- **Shot:** S0
- **Variant:** V<winner>
- **Fast score:** <X>/5
- **Standard score:** <Y>/5
- **Verdict:** <fidelity scales / fidelity drops / no meaningful change>
```

- [ ] **Step 4: Commit**

```bash
git add docs/2026-05-09-seedance-prompt-bakeoff-results.md
git commit -m "$(cat <<'EOF'
seedance-bakeoff: add Standard-tier verification verdict

Confirms winning template's quality scales from Fast to Standard tier
on the identity-stress shot before Act 2 production runs at Standard.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 10: Update CHANGELOG.md and CLAUDE.md

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Read the current CHANGELOG to understand its format**

Run: `head -40 CHANGELOG.md`
Expected: existing entries with date headings + bullet lists.

- [ ] **Step 2: Append the bake-off entry**

Open `CHANGELOG.md` and add a new dated entry at the top (or in chronological position matching the file's convention). Replace `<...>` with actuals:

```markdown
## 2026-05-09 — Seedance prompt template v4 (bake-off)

- **Locked `prompts/seedance-template-v4.md`** as the canonical Seedance 2.0 prompt template, replacing v3 (`docs/2026-05-02-act2-seedance-prompts-v3-conversation-style.md`).
- Winning variant: V<XX> (<name>) — score <X>/20 across W1 + S0 test shots.
- Process: 3-phase plan (deep research → 9-variant structured bake-off → Act 2 application). Spec at [docs/2026-05-09-seedance-prompt-bakeoff-design.md](docs/2026-05-09-seedance-prompt-bakeoff-design.md). Results at [docs/2026-05-09-seedance-prompt-bakeoff-results.md](docs/2026-05-09-seedance-prompt-bakeoff-results.md).
- Why: scattered v3 outputs flagged the template as suboptimal. Phase 1 deep research surfaced 5 settled priors (drop negation; trim word count; don't redescribe frames; banned-words list; structured prose beats JSON). Phase 2 bake-off resolved 6 testable axes with empirical evidence on Sean's specific aesthetic.
- Total cost: $<actual> (Phase 1 free; Phase 2 ~$<actual>).
- New infrastructure: `pipeline/seedance_bakeoff.py`, `pipeline/seedance_bakeoff_variants.yaml`, `tests/test_seedance_bakeoff_lib.py`. Helpers `load_bakeoff_variants()` and `make_bakeoff_run_dir()` added to `pipeline/seedance_lib.py`.
```

- [ ] **Step 3: Update the CLAUDE.md source-of-truth doc table**

Open `CLAUDE.md`. Find the Source of Truth Documents table (currently lists Seedance Research, Act 2 Seedance Shot List, Act 2 Seedance Execution Plan, etc.). Add a row for the locked template. Insert the row after the existing "Seedance Research" row:

```markdown
| **Seedance Prompt Template (v4)** | `prompts/seedance-template-v4.md` | **Canonical Seedance 2.0 prompt template — copy/fill for every new shot.** Locked 2026-05-09 from a 9-variant bake-off. Supersedes v3 (`docs/2026-05-02-act2-seedance-prompts-v3-conversation-style.md`). |
```

Then in the same file, find the "Seedance prompting rules:" bullet list (in the "Seedance Generation" section) and add:

```markdown
- **For all new shots, use the v4 template at `prompts/seedance-template-v4.md`.** Fill the `[BRACKETED]` placeholders; do not modify the structural scaffolding.
```

- [ ] **Step 4: Verify nothing else in CLAUDE.md still references v3 as the active template**

Run: `grep -n 'v3' CLAUDE.md`
Expected: any remaining v3 references should be in archive context (e.g. "supersedes v3"), not active guidance.

- [ ] **Step 5: Commit**

```bash
git add CHANGELOG.md CLAUDE.md
git commit -m "$(cat <<'EOF'
docs: lock Seedance template v4 — update CHANGELOG and CLAUDE.md

CHANGELOG entry summarizes the bake-off process, winning variant, and
new infrastructure. CLAUDE.md source-of-truth table now points at
prompts/seedance-template-v4.md as the canonical template; supersedes v3.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Self-review checklist (run before declaring complete)

- [ ] All 36 (or N successful) cells have an `output.mp4` and `meta.json`
- [ ] `runs/seedance-bakeoff-2026-05-09/scoring.csv` is fully filled (no blank `total` cells)
- [ ] `docs/2026-05-09-seedance-prompt-bakeoff-results.md` exists, all `<placeholder>` markers replaced
- [ ] `prompts/seedance-template-v4.md` exists with the actual winning structural skeleton
- [ ] `CHANGELOG.md` has the 2026-05-09 entry with actual numbers
- [ ] `CLAUDE.md` source-of-truth table references v4
- [ ] No halt condition was triggered without follow-up (V0 by 2+ points, or no variant ≥14/20 on identity-stress shot)
- [ ] All commits applied with the correct co-author trailer
