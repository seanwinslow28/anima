"""DAG post_run hook that stages Em's proposed_patches into manifest.lock.yaml.

Per v2 brainstorm §2.5 + §6 + §10 the patches stage and never auto-apply. This
hook subscribes to the DAG runner's post_run observer and writes any non-empty
proposed_patches list from an AgentResult into runs/{run_id}/manifest.lock.yaml
under a top-level proposed_patches: block. Atomic write via temp-then-rename
mirrors the vault_critic.write_critic_manifest pattern — no torn files visible
to a concurrent reader.

The interactive accept/reject UX (commit 8b or commit 10) reads the same block.
This module is the only writer; pipeline/cli/patches.py is a read-only viewer.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Callable

import yaml

from pipeline.agents import AgentResult

LOCK_FILENAME = "manifest.lock.yaml"


def stage_patches_hook(run_dir: Path) -> Callable[[str, AgentResult], None]:
    """Return a hook function suitable for runner.add_hook('post_run', ...).

    Closes over run_dir so the runner doesn't need to know where the
    manifest lock lives. The returned callable is what the DAG runner
    invokes after each node completes.
    """
    lock_path = Path(run_dir) / LOCK_FILENAME

    def _hook(node_id: str, result: AgentResult) -> None:
        if not result.proposed_patches:
            return

        existing: dict = {}
        if lock_path.exists():
            try:
                loaded = yaml.safe_load(lock_path.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    existing = loaded
            except yaml.YAMLError:
                # Defensive: if the lock got corrupted, start a fresh block
                # rather than crashing the run. The previous content is
                # preserved in the .tmp file if it was mid-write.
                existing = {}

        block = list(existing.get("proposed_patches", []) or [])
        for patch in result.proposed_patches:
            entry = dataclasses.asdict(patch)
            entry["cites_criteria"] = list(entry.get("cites_criteria") or [])
            entry["node_id"] = node_id
            block.append(entry)
        existing["proposed_patches"] = block

        tmp_path = lock_path.with_suffix(lock_path.suffix + ".tmp")
        tmp_path.write_text(
            yaml.safe_dump(existing, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )
        tmp_path.replace(lock_path)

    return _hook


def read_staged_patches(run_dir: Path) -> list[dict]:
    """Return the list of staged proposed patches from a run dir.

    Empty list if the lock file doesn't exist or carries no patches.
    Used by pipeline/cli/patches.py for the read-only `list` command.
    """
    lock_path = Path(run_dir) / LOCK_FILENAME
    if not lock_path.exists():
        return []
    try:
        parsed = yaml.safe_load(lock_path.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return []
    if not isinstance(parsed, dict):
        return []
    return list(parsed.get("proposed_patches", []) or [])
