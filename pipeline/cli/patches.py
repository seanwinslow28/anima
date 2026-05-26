"""Read-only listing of staged proposed_patches from a run dir.

Per v2 brainstorm §2.5 + §10 the patches stage, Sean reviews, never auto-apply.
This command surveys what Em (commit 8) — and later, the T3 stack from
commit 9 — has proposed for human review. The interactive accept/reject
loop is deferred to commit 8b or commit 10.
"""

from __future__ import annotations

from pathlib import Path

from pipeline.agents.patch_stager import read_staged_patches


def list_patches(run_dir: str) -> int:
    rd = Path(run_dir)
    if not rd.exists():
        print(f"Run dir not found: {rd}")
        return 1

    patches = read_staged_patches(rd)
    if not patches:
        print(f"No staged patches in {rd}")
        return 0

    by_persona: dict[str, list[dict]] = {}
    for patch in patches:
        persona = str(patch.get("proposed_by") or "?")
        by_persona.setdefault(persona, []).append(patch)

    lock_path = rd / "manifest.lock.yaml"
    print(f"Staged patches in {lock_path}\n")

    for persona in sorted(by_persona):
        items = by_persona[persona]
        print(f"── {persona} ({len(items)} patch{'es' if len(items) != 1 else ''})")
        for it in items:
            cites = ", ".join(it.get("cites_criteria") or []) or "(none)"
            print(f"  · target:    {it.get('target')}")
            print(f"    path:      {it.get('path')}")
            print(f"    operation: {it.get('operation')}")
            print(f"    value:     {it.get('value')}")
            print(f"    rationale: {it.get('rationale')}")
            print(f"    cites:     {cites}")
            print(f"    node_id:   {it.get('node_id', '?')}")
            print()
    return 0
