"""GENERATE stage — the per-frame Flo -> T1 -> Em fan + the eye gates.

Generalizes scripts/spark_frame.py (seams #6, #7, #9, #11, #16). Each frame's
fan runs through the DAG Runner as small in-memory graphs:

  Graph A:  flo_fNN -> audit_fNN          (one try/except -> honest errored attempt)
  then:     one em_fNN_<ns> single-node graph per cast namespace
            (EmptyCitesInvariant contained per namespace, spark-faithful)

The split (not one big graph) is deliberate: Runner.execute aborts wholesale
on a raising node, losing the sibling results — and Em's empty-cites invariant
is a *recoverable* per-namespace verdict, not a run abort. Patch staging fires
for free via the post_run hook (seam #7); a cache-hit re-fire is patch-less by
construction (the sidecar doesn't persist proposed_patches), and state-first
idempotency means a recorded attempt is never re-fanned anyway.

The Flo node carries config={"attempt": k} as a cache salt: config is part of
the content-addressed cache key, so a retry with an identical prompt (same
correction note twice) is still a REAL re-roll, while a resume of the same
attempt is an idempotent cache hit.
"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

# Populate NODE_REGISTRY for the per-frame fan.
import pipeline.nodes  # noqa: F401  (audit_gate, assemble, ...)
import pipeline.agents.frame_router  # noqa: F401  (flo)
import pipeline.agents.vision_critic  # noqa: F401  (vision_critic)
from pipeline.agents.patch_stager import stage_patches_hook
from pipeline.agents.vision_critic import EmptyCitesInvariant
from pipeline.dag import Edge, Graph, Node, Runner
from pipeline.orchestration import assemble_stage
from pipeline.orchestration import state as st
from pipeline.orchestration.cast import namespace_to_member
from pipeline.orchestration.shots import Shot, load_shots


def combined_criteria_hash(manifest: dict) -> str:
    """Hash over every criteria_sources file (the same set load_all_criteria
    reads, missing files skipped) — a mutation in ANY source invalidates
    downstream cache, preserving the single-file hash's property."""
    sources = manifest.get("criteria_sources") or {}
    paths: list[Path] = []
    if sources.get("brief_file"):
        paths.append(Path(sources["brief_file"]))
    for entry in sources.get("bibles") or []:
        paths.append(Path(entry))
    h = sha256()
    for p in sorted(paths, key=str):
        if p.exists():
            h.update(str(p).encode("utf-8"))
            h.update(b"\x00")
            h.update(p.read_bytes())
            h.update(b"\x00")
    return h.hexdigest()


def approved_key_path(state: dict, run_dir: Path, n: int) -> Path:
    return Path(run_dir) / "approved" / f"{state['slug']}_F{n:02d}_key.png"


def resolve_references(shot: Shot, state: dict, run_dir: Path) -> list[str]:
    """spark_frame's reference recipe, generalized and deduped order-preserving.

    First frame: every cast member's Bible anchor + the shot's extras.
    Frame N:     approved(first) + approved(prior) + chain_anchors' anchors
                 + the shot's extras — the chain runs off APPROVED frames only.
    """
    members = namespace_to_member(state["cast"])
    order = state["frame_order"]
    first = order[0]
    if shot.id == first:
        refs = [members[ns]["anchor"] for ns in shot.cast] + list(shot.extra_references)
    else:
        prior = order[order.index(shot.id) - 1]
        f_first = approved_key_path(state, run_dir, first)
        f_prior = approved_key_path(state, run_dir, prior)
        missing = [str(p) for p in (f_first, f_prior) if not p.exists()]
        if missing:
            raise FileNotFoundError(
                f"frame F{shot.id:02d} chains off approved frames that don't exist yet: "
                f"{missing} — approve the prior frame(s) first."
            )
        refs = (
            [str(f_first), str(f_prior)]
            + [members[ns]["anchor"] for ns in shot.chain_anchors]
            + list(shot.extra_references)
        )
    seen: set[str] = set()
    deduped: list[str] = []
    for r in refs:
        r = str(r)
        if r not in seen:
            seen.add(r)
            deduped.append(r)
    return deduped


def _load_shot_list(state: dict):
    known = {m["ir_namespace"] for m in state["cast"] if m["ir_namespace"]}
    return load_shots(Path(state["shots_path"]), known_namespaces=known)


def run_frame_fan(
    state: dict,
    shot: Shot,
    manifest: dict,
    bundle,
    run_dir: Path,
    *,
    note: str | None = None,
    escalate: bool = False,
) -> int:
    run_dir = Path(run_dir)
    frame_rec = st.get_frame(state, shot.id)
    attempt_idx = len(frame_rec["attempts"]) + 1
    prompt = shot.prompt
    if note:
        prompt += f"\n\nCORRECTION (re-roll, address the prior attempt's defect): {note}"
    refs = resolve_references(shot, state, run_dir)
    members = namespace_to_member(state["cast"])
    primary_folder_key = members[shot.cast[0]]["folder_key"]
    frame_id = f"{state['slug']}_F{shot.id:02d}"
    fid = f"f{shot.id:02d}"
    ts = datetime.now(timezone.utc).isoformat()

    runner = Runner(
        run_dir=run_dir,
        manifest=manifest,
        criteria=None,
        criteria_bundle=bundle,
        criteria_hash=combined_criteria_hash(manifest),
    )
    runner.add_hook("post_run", stage_patches_hook(run_dir))

    gen_graph = Graph(
        nodes=[
            Node(
                id=f"flo_{fid}",
                node_name="flo",
                config={"attempt": attempt_idx},  # cache salt — same-note retries re-roll
                input_bindings={
                    "frame_num": f"literal_json:{shot.id}",
                    "prompt": f"literal:{prompt}",
                    "references": "literal_json:" + json.dumps(refs),
                    "shot_type": "literal:standard_keyframe",
                    "character_id": f"literal:{primary_folder_key}",  # FOLDER key (seam #11)
                },
            ),
            Node(
                id=f"audit_{fid}",
                node_name="audit_gate",
                config={},
                input_bindings={
                    "candidate_path": f"node:flo_{fid}.candidate_path",
                    "frame_num": f"literal_json:{shot.id}",
                    "pose_description": f"literal:{shot.beat}",
                },
            ),
        ],
        edges=[Edge(from_id=f"flo_{fid}", to_id=f"audit_{fid}")],
    )

    try:
        gen_results = runner.execute(gen_graph)
    except Exception as e:  # an honest errored attempt — never a corrupted state
        frame_rec["attempts"].append(
            {"index": attempt_idx, "candidate": None, "note": note,
             "t1": None, "em": [], "errored": f"{type(e).__name__}: {e}", "ts": ts}
        )
        st.save_state(run_dir, state)
        print(f"error: frame F{shot.id:02d} attempt {attempt_idx} errored: {e}",
              file=sys.stderr)
        print(f'  recover with: python -m pipeline.run --resume {run_dir} '
              f'--retry-frame {shot.id} --note "<correction>"', file=sys.stderr)
        return 1

    candidate = gen_results[f"flo_{fid}"].outputs["candidate_path"]
    audit_out = gen_results[f"audit_{fid}"].outputs
    t1 = {"verdict": audit_out["verdict"], "fail_codes": list(audit_out["fail_codes"])}

    impact_tags = ["identity_critical"] if escalate else []
    em_records: list[dict] = []
    for ns in shot.cast:  # one Em pass per cast namespace (seam #9)
        em_node = Node(
            id=f"em_{fid}_{ns}",
            node_name="vision_critic",
            config={},
            input_bindings={
                "image_path": f"literal:{candidate}",
                "beat_description": f"literal:{shot.beat}",
                "frame_id": f"literal:{frame_id}",
                "impact_tags": "literal_json:" + json.dumps(impact_tags),
                "checkpoint": "literal:phase_5_generate",
                "character_id": f"literal:{ns}",  # IR NAMESPACE (seam #11)
            },
        )
        try:
            r = runner.execute(Graph(nodes=[em_node], edges=[]))[f"em_{fid}_{ns}"]
            em_records.append(
                {"frame": frame_id, "character": ns,
                 "verdict": r.outputs["verdict"], "confidence": r.outputs["confidence"],
                 "cites": list(r.cites_criteria), "patches": len(r.proposed_patches),
                 "reasoning": r.outputs["reasoning"], "notes": r.notes}
            )
        except EmptyCitesInvariant as e:
            # Recoverable per-namespace verdict (spark-faithful): Em detected but
            # couldn't ground — a human looks, the other namespace still runs.
            em_records.append(
                {"frame": frame_id, "character": ns,
                 "verdict": "human_review (empty-cites invariant)", "confidence": None,
                 "cites": [], "patches": 0, "reasoning": e.reasoning,
                 "notes": "EmptyCitesInvariant"}
            )

    vlog = run_dir / "em_verdicts.jsonl"
    with vlog.open("a", encoding="utf-8") as fh:
        for v in em_records:
            fh.write(json.dumps(v) + "\n")

    frame_rec["attempts"].append(
        {"index": attempt_idx, "candidate": str(candidate), "note": note,
         "t1": t1, "em": em_records, "errored": None, "ts": ts}
    )
    frame_rec["status"] = "generated"
    st.save_state(run_dir, state)

    print(f"\nframe F{shot.id:02d} attempt {attempt_idx}:")
    print(f"  candidate: {candidate}")
    print(f"  T1: {t1['verdict']}" + (f"  {t1['fail_codes']}" if t1["fail_codes"] else ""))
    for v in em_records:
        print(f"  Em[{v['character']}]: {v['verdict']} "
              f"(conf={v['confidence']}, cites={v['cites']})")
    print("\nHUMAN GATE — eye the candidate, then:")
    print(f"  python -m pipeline.run --resume {run_dir} --approve-frame {shot.id} "
          f"[--attempt {attempt_idx}]")
    print(f'  python -m pipeline.run --resume {run_dir} --retry-frame {shot.id} '
          f'--note "<correction>"')
    return 0


def generate_current_frame(state: dict, manifest: dict, bundle, run_dir: Path,
                           *, note: str | None = None, escalate: bool = False) -> int:
    n = st.current_frame(state)
    if n is None:
        print("error: no frame awaiting generation.", file=sys.stderr)
        return 2
    shot_list = _load_shot_list(state)
    return run_frame_fan(state, shot_list.by_id(n), manifest, bundle, run_dir,
                         note=note, escalate=escalate)


def approve_frame(state: dict, manifest: dict, bundle, run_dir: Path,
                  frame: int, attempt: int | None) -> int:
    run_dir = Path(run_dir)
    current = st.current_frame(state)
    if frame != current:
        where = "none (all approved)" if current is None else f"F{current:02d}"
        print(f"error: --approve-frame {frame} but the current frame is {where}.",
              file=sys.stderr)
        return 2
    rec = st.get_frame(state, frame)
    if rec["status"] != "generated":
        print(f"error: frame F{frame:02d} has no generated candidate to approve "
              f"(status={rec['status']!r}) — retry it first.", file=sys.stderr)
        return 2
    candidates = [a for a in rec["attempts"] if a.get("candidate")]
    if attempt is None:
        attempt = max(a["index"] for a in candidates)
    chosen = next((a for a in candidates if a["index"] == attempt), None)
    if chosen is None or not Path(chosen["candidate"]).exists():
        print(f"error: frame F{frame:02d} has no attempt {attempt} candidate on disk.",
              file=sys.stderr)
        return 2

    cand = Path(chosen["candidate"])
    dst = approved_key_path(state, run_dir, frame)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(cand, dst)
    log = run_dir / "approved" / "approvals.jsonl"
    with log.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"frame": f"{state['slug']}_F{frame:02d}", "attempt": attempt,
                             "candidate": str(cand), "approved": str(dst)}) + "\n")
    rec["status"] = "approved"
    rec["approved_attempt"] = attempt
    rec["approved_path"] = str(dst)
    st.save_state(run_dir, state)
    print(f"approved: {cand} -> {dst}")

    if st.current_frame(state) is not None:
        return generate_current_frame(state, manifest, bundle, run_dir)

    st.advance_stage(state, "ASSEMBLE")
    st.save_state(run_dir, state)
    print("all frames approved — assembling the loop")
    return assemble_stage.run_assemble_stage(state, manifest, bundle, run_dir)


def retry_frame(state: dict, manifest: dict, bundle, run_dir: Path,
                frame: int, note: str, escalate: bool) -> int:
    current = st.current_frame(state)
    if frame != current:
        where = "none (all approved)" if current is None else f"F{current:02d}"
        print(f"error: --retry-frame {frame} but the current frame is {where}.",
              file=sys.stderr)
        return 2
    shot_list = _load_shot_list(state)
    return run_frame_fan(state, shot_list.by_id(frame), manifest, bundle, run_dir,
                         note=note, escalate=escalate)
