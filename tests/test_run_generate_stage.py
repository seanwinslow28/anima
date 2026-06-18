"""P2 — the GENERATE loop (seams #6, #7, #9, #11, #16).

Per frame: an in-memory Graph (flo_fNN -> audit_fNN, then one em_fNN_<ns>
single-node graph per cast namespace) runs through the DAG Runner with the
stage_patches_hook attached — patch staging fires for free (seam #7). The eye
gate exits; --approve-frame chains N+1 off the approved prior; --retry-frame
re-rolls with the correction note appended and a fresh attempt salt.

Stub-green: a --stub run dispatches the REAL flo_stub production node (Slice
2.1 Fix A) — tests spy it via tests/orch_fixtures.spy_flo_stub (real 1376x768
PNGs; the audit gate PIL-opens candidates). The real `flo` node's dispatch +
seam #11 threading is covered by the non-stub run_frame_fan switch test, with
pipeline.generate.generate_frame faked at the established boundary. Em runs
its real node logic over stubbed or faked transports.
"""

from __future__ import annotations

import json

import pytest

from pipeline import run as run_cli
from pipeline.orchestration import assemble_stage
from pipeline.orchestration import state as st
from tests.orch_fixtures import (
    fake_em_transport,
    fake_flo_generate,
    mk_project,
    spy_flo_stub,
    stub_critic_env,
)


def _start_and_approve(root, brief_dir, *, run_name="tt-run"):
    run_dir = root / "runs" / run_name
    rc = run_cli.main(["--brief", str(brief_dir), "--stub", "--run-dir", str(run_dir)])
    assert rc == 0
    rc = run_cli.main(["--resume", str(run_dir), "--approve-plan"])
    return rc, run_dir


def test_enter_generate_is_reusable_from_storyboard_stage(tmp_path, monkeypatch):
    """The refactor's payoff: enter_generate (load_shots -> validate -> seed ->
    advance -> fan frame 1) is callable from STORYBOARD, not only the plan gate.
    This is the seam the storyboard gate reuses, so both entry paths can't drift."""
    import yaml

    from pipeline.criteria import load_all_criteria
    from pipeline.orchestration import generate_stage
    from pipeline.orchestration.plan_stage import wire_brief_criteria

    root, brief_dir = mk_project(tmp_path, monkeypatch)
    stub_critic_env(monkeypatch)
    run_dir = root / "runs" / "eg-run"
    assert run_cli.main(["--brief", str(brief_dir), "--stub", "--run-dir", str(run_dir)]) == 0
    state = st.load_state(run_dir)
    # Walk the authoring stages directly (unit-isolating enter_generate from the gates).
    st.advance_stage(state, "SCRIPT")
    st.advance_stage(state, "STORYBOARD")

    manifest = yaml.safe_load((root / "manifest.yaml").read_text())
    wire_brief_criteria(manifest, state["brief_dir"])
    bundle = load_all_criteria(manifest)

    fanned: list[int | None] = []

    def fake_fan(s, m, b, rd):
        fanned.append(st.current_frame(s))
        return 0

    monkeypatch.setattr(generate_stage, "generate_current_frame", fake_fan)

    rc = generate_stage.enter_generate(state, manifest, bundle, run_dir)

    assert rc == 0
    assert state["stage"] == "GENERATE"
    assert state["frame_order"] == [1, 2]
    assert state["holds"] == {"1": 2, "2": 3}
    assert fanned == [1]  # frame 1 fanned after seeding
    assert st.load_state(run_dir)["stage"] == "GENERATE"  # persisted


def test_approve_plan_generates_frame1_through_the_fan(tmp_path, monkeypatch, capsys):
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    stub_critic_env(monkeypatch)
    flo_calls = spy_flo_stub(monkeypatch)

    rc, run_dir = _start_and_approve(root, brief_dir)

    assert rc == 0
    state = st.load_state(run_dir)
    assert state["stage"] == "GENERATE"
    frame1 = st.get_frame(state, 1)
    assert frame1["status"] == "generated"
    [attempt] = frame1["attempts"]
    assert attempt["index"] == 1
    assert (run_dir / "candidates" / "F01" / "attempt_01.png").exists()
    assert attempt["candidate"].endswith("candidates/F01/attempt_01.png")
    # T1 ran: a 1376x768 candidate clears HF01
    assert attempt["t1"]["verdict"] == "needs_vision_review"
    assert attempt["t1"]["fail_codes"] == []
    # Em ran once per cast namespace (frame 1 casts al + be), on the stub path:
    # gemini stub 0.65 < 0.7 threshold -> escalated to the opus stub (borderline@0.78)
    assert [v["character"] for v in attempt["em"]] == ["al", "be"]
    for v in attempt["em"]:
        assert v["verdict"] == "borderline"
        assert v["cites"] == ["AC01"]
        assert "(escalated)" in v["notes"]
    # the spark-shaped verdict trail
    vlog = (run_dir / "em_verdicts.jsonl").read_text().strip().splitlines()
    assert len(vlog) == 2
    assert json.loads(vlog[0])["frame"] == "TT_F01"
    # frame 1 references: every cast anchor (no extras in the fixture)
    assert flo_calls[0]["references"] == [
        "characters/alpha/anchor.png", "characters/beta/anchor.png",
    ]
    out = capsys.readouterr().out
    assert "--approve-frame 1" in out  # the eye gate prints the next command


def test_flo_gets_folder_key_em_gets_namespace(tmp_path, monkeypatch):
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    stub_critic_env(monkeypatch)

    import pipeline.agents.flo_stub as fs
    import pipeline.agents.vision_critic as vc

    flo_char_ids, em_char_ids = [], []
    real_flo_run, real_em_run = fs.FloStubNode.run, vc.VisionCriticNode.run

    def spy_flo(self, ctx):
        flo_char_ids.append(ctx.inputs.get("character_id"))
        return real_flo_run(self, ctx)

    def spy_em(self, ctx):
        em_char_ids.append(ctx.inputs.get("character_id"))
        return real_em_run(self, ctx)

    monkeypatch.setattr(fs.FloStubNode, "run", spy_flo)
    monkeypatch.setattr(vc.VisionCriticNode, "run", spy_em)

    rc, _ = _start_and_approve(root, brief_dir)

    assert rc == 0
    assert flo_char_ids == ["alpha"]      # the FOLDER key (primary = first cast member)
    assert em_char_ids == ["al", "be"]    # the IR namespaces (seam #11)


def test_approve_frame_copies_attempt_and_chains_with_correct_refs(tmp_path, monkeypatch):
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    stub_critic_env(monkeypatch)
    flo_calls = spy_flo_stub(monkeypatch)
    rc, run_dir = _start_and_approve(root, brief_dir)
    assert rc == 0

    rc = run_cli.main(["--resume", str(run_dir), "--approve-frame", "1"])

    assert rc == 0
    approved = run_dir / "approved" / "TT_F01_key.png"
    assert approved.exists()
    assert approved.read_bytes() == (
        run_dir / "candidates" / "F01" / "attempt_01.png"
    ).read_bytes()
    log_lines = (run_dir / "approved" / "approvals.jsonl").read_text().strip().splitlines()
    assert json.loads(log_lines[0]) == {
        "frame": "TT_F01", "attempt": 1,
        "candidate": str(run_dir / "candidates" / "F01" / "attempt_01.png"),
        "approved": str(approved),
    }
    state = st.load_state(run_dir)
    assert st.get_frame(state, 1)["status"] == "approved"
    assert st.get_frame(state, 1)["approved_attempt"] == 1
    # frame 2 generated in the same invocation, chained off the APPROVED prior:
    # first==prior==F01 here, then chain_anchors (cast al -> alpha), deduped
    frame2 = st.get_frame(state, 2)
    assert frame2["status"] == "generated"
    assert flo_calls[1]["frame_num"] == 2
    assert flo_calls[1]["references"] == [
        str(approved), "characters/alpha/anchor.png",
    ]
    # one-cast frame -> ONE Em pass (frame 1 ran two)
    assert [v["character"] for v in frame2["attempts"][0]["em"]] == ["al"]


def _refs_state():
    return {
        "slug": "TT",
        "frame_order": [1, 2, 3],
        "cast": [
            {"ir_namespace": "al", "folder_key": "alpha", "anchor": "characters/alpha/anchor.png"},
            {"ir_namespace": "be", "folder_key": "beta", "anchor": "characters/beta/anchor.png"},
        ],
    }


def test_resolve_references_chain_from_chains_off_the_named_frame_not_prior(tmp_path):
    """A loop-return frame (F3, chain_from: 1) chains off frame 1 — the loop
    anchor — not the prior approved frame (F2). The dedup collapses
    approved(first)+approved(chain_from) to a single ref, so F2 never appears."""
    from pipeline.orchestration.generate_stage import approved_key_path, resolve_references
    from pipeline.orchestration.shots import Shot

    state = _refs_state()
    (tmp_path / "approved").mkdir()
    for n in (1, 2):
        approved_key_path(state, tmp_path, n).write_bytes(b"x")

    loop = Shot(id=3, cast=["al"], beat="b", prompt="p", chain_anchors=["al"], chain_from=1)
    refs = resolve_references(loop, state, tmp_path)

    assert refs == [str(approved_key_path(state, tmp_path, 1)), "characters/alpha/anchor.png"]
    assert str(approved_key_path(state, tmp_path, 2)) not in refs  # F4 (the delight mascot) dropped


def test_resolve_references_without_chain_from_uses_prior_frame_unchanged(tmp_path):
    from pipeline.orchestration.generate_stage import approved_key_path, resolve_references
    from pipeline.orchestration.shots import Shot

    state = _refs_state()
    (tmp_path / "approved").mkdir()
    for n in (1, 2):
        approved_key_path(state, tmp_path, n).write_bytes(b"x")

    f3 = Shot(id=3, cast=["al"], beat="b", prompt="p", chain_anchors=["al"])  # no chain_from
    refs = resolve_references(f3, state, tmp_path)

    # prior == F2, so both approved(1) and approved(2) are present (unchanged recipe)
    assert refs == [
        str(approved_key_path(state, tmp_path, 1)),
        str(approved_key_path(state, tmp_path, 2)),
        "characters/alpha/anchor.png",
    ]


def test_retry_appends_note_and_same_note_still_rerolls(tmp_path, monkeypatch):
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    stub_critic_env(monkeypatch)
    flo_calls = spy_flo_stub(monkeypatch)
    rc, run_dir = _start_and_approve(root, brief_dir)
    assert rc == 0

    rc = run_cli.main(["--resume", str(run_dir), "--retry-frame", "1",
                       "--note", "stylus in the RIGHT hand"])
    assert rc == 0
    assert flo_calls[1]["attempt"] == 2
    assert flo_calls[1]["prompt"].endswith(
        "CORRECTION (re-roll, address the prior attempt's defect): stylus in the RIGHT hand"
    )
    assert flo_calls[1]["prompt"].startswith("prompt one")

    # the same note again is still a REAL re-roll (the attempt salt beats the cache)
    rc = run_cli.main(["--resume", str(run_dir), "--retry-frame", "1",
                       "--note", "stylus in the RIGHT hand"])
    assert rc == 0
    assert len(flo_calls) == 3
    state = st.load_state(run_dir)
    assert [a["index"] for a in st.get_frame(state, 1)["attempts"]] == [1, 2, 3]
    assert (run_dir / "candidates" / "F01" / "attempt_03.png").exists()
    assert st.get_frame(state, 1)["status"] == "generated"


def test_empty_cites_invariant_records_human_review_and_continues(tmp_path, monkeypatch):
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    stub_critic_env(monkeypatch)
    # high confidence (no escalation), blocking verdict, NO cites -> the invariant
    fake_em_transport(monkeypatch, verdict="fail", confidence=0.95, cites=())

    rc, run_dir = _start_and_approve(root, brief_dir)

    assert rc == 0  # the fan contains the invariant; the eye gate still reached
    state = st.load_state(run_dir)
    [attempt] = st.get_frame(state, 1)["attempts"]
    assert len(attempt["em"]) == 2  # the second namespace still ran
    for v in attempt["em"]:
        assert v["verdict"] == "human_review (empty-cites invariant)"
        assert v["confidence"] is None
        assert v["cites"] == []


def test_em_patches_staged_via_post_run_hook(tmp_path, monkeypatch):
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    stub_critic_env(monkeypatch)
    fake_em_transport(
        monkeypatch, verdict="fail", confidence=0.95,
        cites=("IR.al.style.line-weight",),
        patches=({"target": "manifest.lock.yaml", "path": "generation.model",
                  "operation": "set", "value": "nb-pro", "rationale": "identity drift",
                  "cites_criteria": ["IR.al.style.line-weight"]},),
    )

    rc, run_dir = _start_and_approve(root, brief_dir)

    assert rc == 0
    import yaml
    lock = yaml.safe_load((run_dir / "manifest.lock.yaml").read_text())
    staged = lock["proposed_patches"]
    assert [p["node_id"] for p in staged] == ["em_f01_al", "em_f01_be"]
    assert staged[0]["proposed_by"] == "em-vision-critic"
    # --status never re-runs the fan or re-stages (state-first idempotency)
    before = (run_dir / "manifest.lock.yaml").read_bytes()
    assert run_cli.main(["--resume", str(run_dir), "--status"]) == 0
    assert (run_dir / "manifest.lock.yaml").read_bytes() == before


def test_eye_gate_surfaces_em_reasoning_and_patch_on_flagged_verdict(tmp_path, monkeypatch, capsys):
    """B1: a borderline/fail verdict surfaces Em's grounded diagnosis — the
    reasoning paragraph AND her proposed-patch summary — at the eye gate, instead
    of dropping them (the F4/F5 finding). The retry hint steers the note positive."""
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    stub_critic_env(monkeypatch)
    fake_em_transport(
        monkeypatch, verdict="fail", confidence=0.95,
        reasoning="front face lacks pencil construction cross-lines; shading is a flat color step",
        cites=("IR.al.style.construction-lines",),
        patches=({"target": "manifest.lock.yaml", "path": "generation.model",
                  "operation": "set", "value": "nb-pro",
                  "rationale": "restore graphite cross-hatching",
                  "cites_criteria": ["IR.al.style.construction-lines"]},),
    )

    rc, run_dir = _start_and_approve(root, brief_dir)
    assert rc == 0

    out = capsys.readouterr().out
    # Em's reasoning surfaces (was dropped at the gate before)
    assert "front face lacks pencil construction cross-lines" in out
    # her proposed-patch summary surfaces (target / value / rationale)
    assert "generation.model" in out
    assert "nb-pro" in out
    assert "restore graphite cross-hatching" in out
    # the retry hint steers toward the positive end-state, not the defect
    assert "desired end-state" in out
    assert "naming the flaw reinforces it" in out


def test_approve_last_frame_enters_assemble(tmp_path, monkeypatch):
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    stub_critic_env(monkeypatch)
    rc, run_dir = _start_and_approve(root, brief_dir)
    assert rc == 0

    assemble_calls = []
    monkeypatch.setattr(
        assemble_stage, "run_assemble_stage",
        lambda state, manifest, bundle, run_dir: (assemble_calls.append(run_dir), 0)[1],
    )

    assert run_cli.main(["--resume", str(run_dir), "--approve-frame", "1"]) == 0
    assert assemble_calls == []  # frame 2 still ahead
    assert run_cli.main(["--resume", str(run_dir), "--approve-frame", "2"]) == 0

    assert len(assemble_calls) == 1
    state = st.load_state(run_dir)
    assert state["stage"] == "ASSEMBLE"  # the fake didn't advance to DONE
    assert st.current_frame(state) is None


def test_gate_guards_wrong_frame_and_errored_attempt(tmp_path, monkeypatch, capsys):
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    stub_critic_env(monkeypatch)

    # Flo blows up -> an honest errored attempt, not a crash or a fake candidate.
    # Post-Fix-A the --stub fan dispatches flo_stub, so that's the node to melt.
    import pipeline.agents.flo_stub as fs

    real_run = fs.FloStubNode.run

    def boom(self, ctx):
        raise RuntimeError("transport melted")

    monkeypatch.setattr(fs.FloStubNode, "run", boom)
    rc, run_dir = _start_and_approve(root, brief_dir)

    assert rc == 1
    state = st.load_state(run_dir)
    assert state["stage"] == "GENERATE"  # plan approval held; the frame did not
    frame1 = st.get_frame(state, 1)
    assert frame1["status"] == "pending"
    [attempt] = frame1["attempts"]
    assert attempt["candidate"] is None
    assert "transport melted" in attempt["errored"]

    # approving the wrong frame (or an errored one) is a usage error
    capsys.readouterr()
    assert run_cli.main(["--resume", str(run_dir), "--approve-frame", "2"]) == 2
    assert run_cli.main(["--resume", str(run_dir), "--approve-frame", "1"]) == 2

    # the retry ladder recovers: fix the transport, re-roll with a note
    monkeypatch.setattr(fs.FloStubNode, "run", real_run)
    flo_calls = spy_flo_stub(monkeypatch)
    assert run_cli.main(["--resume", str(run_dir), "--retry-frame", "1",
                         "--note", "re-roll after transport error"]) == 0
    assert flo_calls[0]["attempt"] == 1  # no candidate file was written by the errored attempt
    state = st.load_state(run_dir)
    assert st.get_frame(state, 1)["status"] == "generated"
    assert [a["index"] for a in st.get_frame(state, 1)["attempts"]] == [1, 2]


@pytest.mark.parametrize("stub,expected", [(True, "flo_stub"), (False, "flo")])
def test_run_frame_fan_dispatches_node_by_stub_flag(tmp_path, monkeypatch, stub, expected):
    """The Fix A switch: state['stub'] selects flo_stub; a real run keeps the
    real flo node — including seam #11 (FOLDER key) threading on that path."""
    import yaml

    import pipeline.agents.flo_stub as fs
    import pipeline.agents.frame_router as fr
    from pipeline.criteria import load_all_criteria
    from pipeline.orchestration import generate_stage
    from pipeline.orchestration.cast import derive_cast
    from pipeline.orchestration.shots import load_shots

    root, brief_dir = mk_project(tmp_path, monkeypatch)
    stub_critic_env(monkeypatch)
    fake_flo_generate(monkeypatch)  # the real FloNode's transport boundary (stub=False arm)

    dispatched, flo_char_ids = [], []
    real_flo, real_stub = fr.FloNode.run, fs.FloStubNode.run

    def spy_flo(self, ctx):
        dispatched.append("flo")
        flo_char_ids.append(ctx.inputs.get("character_id"))
        return real_flo(self, ctx)

    def spy_stub(self, ctx):
        dispatched.append("flo_stub")
        return real_stub(self, ctx)

    monkeypatch.setattr(fr.FloNode, "run", spy_flo)
    monkeypatch.setattr(fs.FloStubNode, "run", spy_stub)

    manifest = yaml.safe_load((root / "manifest.yaml").read_text())
    bundle = load_all_criteria(manifest)
    run_dir = root / "runs" / "switch-run"
    state = st.new_state(
        run_id="switch-run", brief_dir=str(brief_dir), manifest_path="manifest.yaml",
        shots_path=str(brief_dir / "shots.yaml"), slug="TT", stub=stub,
        cast=derive_cast(manifest),
    )
    state["frame_order"] = [1, 2]
    st.set_frame(state, 1, {"status": "pending", "attempts": [],
                            "approved_attempt": None, "approved_path": None})
    shot_list = load_shots(brief_dir / "shots.yaml", known_namespaces={"al", "be"})

    rc = generate_stage.run_frame_fan(state, shot_list.by_id(1), manifest, bundle, run_dir)

    assert rc == 0
    assert dispatched == [expected]  # exactly one Flo-side node fired
    if expected == "flo":
        assert flo_char_ids == ["alpha"]  # seam #11 held on the REAL node
