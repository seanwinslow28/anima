"""Regression tripwire: the REAL manifest.yaml's merged criteria must load.

Every other criteria test uses fixtures. The 2026-05-30 pivot shipped an
unloadable Bible (bible mutate wrote a content semver into the schema-version
field) and the 188-test suite stayed green because no test loaded the live
manifest's on-disk Bibles. This test closes that gap: it loads the real
manifest, merges every Bible's IR.* graph, and asserts it parses with zero
ID collisions. If this goes red, STOP and fix before any other work.
"""
from pathlib import Path

import yaml

from pipeline.criteria import load_all_criteria

_PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_live_manifest_with_absolute_bible_paths() -> dict:
    """Load manifest.yaml and rewrite criteria_sources paths to absolute so
    the test is independent of the pytest working directory."""
    manifest = yaml.safe_load((_PROJECT_ROOT / "manifest.yaml").read_text(encoding="utf-8"))
    sources = manifest.get("criteria_sources") or {}
    bibles = sources.get("bibles") or []
    sources["bibles"] = [str(_PROJECT_ROOT / p) for p in bibles]
    brief = sources.get("brief_file")
    if brief:
        sources["brief_file"] = str(_PROJECT_ROOT / brief)
    manifest["criteria_sources"] = sources
    return manifest


def test_live_manifest_criteria_loads_without_collision():
    manifest = _load_live_manifest_with_absolute_bible_paths()
    # load_all_criteria raises ValueError on a duplicate ID across sources and
    # raises on an unsupported schema version — so a clean return is the assertion.
    bundle = load_all_criteria(manifest)

    # At least the two real Bibles' IR.* graphs are present.
    ir_ids = [c.id for c in bundle.criteria if c.id.startswith("IR.")]
    assert ir_ids, "expected the live manifest to merge at least one IR.* Bible graph"

    # Zero ID collisions across IR.* namespaces.
    assert len(ir_ids) == len(set(ir_ids)), "duplicate IR.* ids in the merged bundle"

    # The merged schema version is a supported one (1.0/1.1/1.2).
    assert bundle.version.split(".", 2)[0] == "1"
    assert any(i.startswith("IR.sean.") for i in ir_ids)
    assert any(i.startswith("IR.claude-mascot.") for i in ir_ids)
