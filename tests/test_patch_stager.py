"""Tests for pipeline.agents.patch_stager — DAG post_run hook for staging patches."""

from __future__ import annotations

import yaml

from pipeline.agents import AgentResult, Patch
from pipeline.agents.patch_stager import (
    read_staged_patches,
    stage_patches_hook,
)


def _patch(path: str = "act1.keyframes[2].pose", rationale: str = "test") -> Patch:
    return Patch(
        target="manifest.lock.yaml",
        path=path,
        operation="set",
        value="varied line weight 1-3px",
        rationale=rationale,
        proposed_by="em-vision-critic",
        cites_criteria=("AC01",),
    )


def test_writes_proposed_patches_block(tmp_path):
    result = AgentResult(
        outputs={"verdict": "borderline"},
        proposed_patches=[_patch()],
        cites_criteria=["AC01"],
    )
    hook = stage_patches_hook(tmp_path)
    hook("f06_critic", result)

    lock_path = tmp_path / "manifest.lock.yaml"
    assert lock_path.exists()
    parsed = yaml.safe_load(lock_path.read_text())
    assert "proposed_patches" in parsed
    assert len(parsed["proposed_patches"]) == 1
    entry = parsed["proposed_patches"][0]
    assert entry["proposed_by"] == "em-vision-critic"
    assert entry["path"] == "act1.keyframes[2].pose"
    assert entry["node_id"] == "f06_critic"
    assert entry["cites_criteria"] == ["AC01"]


def test_appends_across_invocations(tmp_path):
    """Two separate node runs both write; manifest.lock.yaml grows."""
    hook = stage_patches_hook(tmp_path)

    result_a = AgentResult(
        outputs={"verdict": "borderline"},
        proposed_patches=[_patch(rationale="first call")],
        cites_criteria=["AC01"],
    )
    hook("node_a", result_a)

    result_b = AgentResult(
        outputs={"verdict": "fail"},
        proposed_patches=[
            _patch(path="act1.keyframes[5].pose", rationale="second call A"),
            _patch(path="act1.keyframes[6].pose", rationale="second call B"),
        ],
        cites_criteria=["AC01"],
    )
    hook("node_b", result_b)

    patches = read_staged_patches(tmp_path)
    assert len(patches) == 3
    assert [p["node_id"] for p in patches] == ["node_a", "node_b", "node_b"]


def test_no_patches_no_write(tmp_path):
    """Result with empty proposed_patches doesn't create manifest.lock.yaml."""
    hook = stage_patches_hook(tmp_path)
    hook("clean_node", AgentResult(outputs={"verdict": "pass"}))

    assert not (tmp_path / "manifest.lock.yaml").exists()


def test_read_staged_patches_returns_empty_when_no_file(tmp_path):
    assert read_staged_patches(tmp_path) == []


def test_preserves_pre_existing_manifest_lock_content(tmp_path):
    """If manifest.lock.yaml already has content from elsewhere, the hook
    preserves it and only appends to the proposed_patches block."""
    lock_path = tmp_path / "manifest.lock.yaml"
    pre_existing = {"project": {"name": "anima"}, "tier": "draft"}
    lock_path.write_text(yaml.safe_dump(pre_existing))

    hook = stage_patches_hook(tmp_path)
    hook("late_critic", AgentResult(
        outputs={"verdict": "fail"},
        proposed_patches=[_patch()],
        cites_criteria=["AC01"],
    ))

    parsed = yaml.safe_load(lock_path.read_text())
    assert parsed["project"]["name"] == "anima"
    assert parsed["tier"] == "draft"
    assert len(parsed["proposed_patches"]) == 1


def test_atomic_write_no_torn_file(tmp_path):
    """Writes go via temp + rename. The temp path doesn't survive a successful write."""
    hook = stage_patches_hook(tmp_path)
    hook("a", AgentResult(
        outputs={"v": "x"},
        proposed_patches=[_patch()],
        cites_criteria=["AC01"],
    ))
    # Cleanup invariant: no .tmp files left around after a successful write.
    leftover_tmp = list(tmp_path.glob("manifest.lock.yaml.tmp"))
    assert leftover_tmp == []
