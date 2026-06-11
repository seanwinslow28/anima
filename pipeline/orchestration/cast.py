"""Cast/namespace discovery — seams #9 + #11.

`character_id` means two different things in the node fleet: FloNode wants
the manifest folder key (`sean-anchor`, for the style_register lookup); Em
wants the IR namespace (`sean`, the query_by_character key). derive_cast
builds the one table that threads both, derived once at run start and
persisted to state.cast.

The namespace comes from each Bible's acceptance_criteria.json: the v1.2
validator enforces that every IR rule's character_id field matches its
`IR.<namespace>.*` id prefix, so loading the file and reading the field is
authoritative — no string parsing.
"""

from __future__ import annotations

from pathlib import Path

from pipeline.criteria import load_criteria


def derive_cast(manifest: dict) -> list[dict]:
    """[{folder_key, ir_namespace, anchor, criteria}] in manifest characters: order.

    A character whose Bible has no criteria file (not yet authored) is
    registered with ir_namespace=None — it only errors when a shot casts it.
    A Bible carrying more than one namespace is a config error (Bible folders
    are per-character).
    """
    cast: list[dict] = []
    for folder_key, spec in (manifest.get("characters") or {}).items():
        folder = Path(spec["folder"])
        criteria_path = folder / "acceptance_criteria.json"
        namespace: str | None = None
        if criteria_path.exists():
            bundle = load_criteria(criteria_path)
            namespaces = sorted({c.character_id for c in bundle.criteria if c.character_id})
            if len(namespaces) > 1:
                raise ValueError(
                    f"Bible {folder_key!r} ({criteria_path}) carries {len(namespaces)} IR "
                    f"namespaces {namespaces} — a Bible folder is per-character."
                )
            namespace = namespaces[0] if namespaces else None
        cast.append(
            {
                "folder_key": folder_key,
                "ir_namespace": namespace,
                "anchor": str(folder / "anchor.png"),
                "criteria": str(criteria_path),
            }
        )
    return cast


def namespace_to_member(cast: list[dict]) -> dict[str, dict]:
    return {m["ir_namespace"]: m for m in cast if m["ir_namespace"]}
