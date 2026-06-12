"""Slice 2.1 follow-on — --stub can never silently spend (ANIMA_FORCE_STUB).

The live smoke surfaced the inverse of the silent-stub trap: with
claude-agent-sdk importable (subscription OAuth) or a populated .env,
`--stub` skipped the smoke guard but Maya/Em still went LIVE — a silent
SPEND on a run whose contract is $0. pipeline.run now exports
ANIMA_FORCE_STUB=1 for the dynamic extent of a --stub invocation, and every
model transport gate honors it.
"""

from __future__ import annotations

import asyncio
import os
import sys
import types
from pathlib import Path

from pipeline import run as run_cli
from tests.orch_fixtures import force_stub_sdk, mk_project, stub_critic_env


def test_sdk_available_false_under_force_stub(monkeypatch):
    from pipeline.agents import sdk_runners

    # make claude_agent_sdk importable — the subscription path would be live
    monkeypatch.setitem(sys.modules, "claude_agent_sdk", types.ModuleType("claude_agent_sdk"))
    monkeypatch.delenv("ANIMA_FORCE_STUB", raising=False)
    assert sdk_runners._sdk_available() is True  # the dangerous baseline

    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")
    assert sdk_runners._sdk_available() is False


def test_gemini_api_transport_stubs_under_force_stub(monkeypatch):
    from pipeline.agents import gemini_api_runner as gar

    monkeypatch.setattr(gar, "_genai_available", lambda: True)
    monkeypatch.setattr(gar, "_has_gemini_api_key", lambda: True)
    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")

    resp = asyncio.run(
        gar.run_gemini_api_with_image(prompt="p", image_paths=[Path("x.png")])
    )
    assert resp.stub_fallback is True


def test_agy_transport_stubs_under_force_stub(monkeypatch):
    import shutil

    from pipeline.agents import cli_runners

    monkeypatch.setattr(shutil, "which", lambda name: "/fake/bin/agy")
    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")

    resp = asyncio.run(
        cli_runners.run_antigravity_with_image(prompt="p", image_paths=[Path("x.png")])
    )
    assert resp.stub_fallback is True


def test_stub_run_sets_force_stub_for_the_invocation_and_restores(tmp_path, monkeypatch):
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    force_stub_sdk(monkeypatch)
    monkeypatch.delenv("ANIMA_FORCE_STUB", raising=False)

    import pipeline.agents.planner as planner_mod

    seen = {}
    real_run = planner_mod.PlannerNode.run

    def spy(self, ctx):
        seen["force_stub"] = os.environ.get("ANIMA_FORCE_STUB")
        return real_run(self, ctx)

    monkeypatch.setattr(planner_mod.PlannerNode, "run", spy)

    rc = run_cli.main(["--brief", str(brief_dir), "--stub",
                       "--run-dir", str(root / "runs" / "x")])
    assert rc == 0
    assert seen["force_stub"] == "1"  # live while Maya ran
    assert "ANIMA_FORCE_STUB" not in os.environ  # restored after main()


def test_stub_resume_sets_force_stub_too(tmp_path, monkeypatch):
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    stub_critic_env(monkeypatch)
    monkeypatch.delenv("ANIMA_FORCE_STUB", raising=False)
    run_dir = root / "runs" / "x"
    assert run_cli.main(["--brief", str(brief_dir), "--stub",
                         "--run-dir", str(run_dir)]) == 0

    import pipeline.agents.vision_critic as vc

    seen = {}
    real_run = vc.VisionCriticNode.run

    def spy(self, ctx):
        seen["force_stub"] = os.environ.get("ANIMA_FORCE_STUB")
        return real_run(self, ctx)

    monkeypatch.setattr(vc.VisionCriticNode, "run", spy)

    assert run_cli.main(["--resume", str(run_dir), "--approve-plan"]) == 0
    assert seen["force_stub"] == "1"  # the resumed stub run re-exported it
    assert "ANIMA_FORCE_STUB" not in os.environ


def test_non_stub_run_never_sets_force_stub(tmp_path, monkeypatch):
    root, brief_dir = mk_project(tmp_path, monkeypatch)
    force_stub_sdk(monkeypatch)
    monkeypatch.delenv("ANIMA_FORCE_STUB", raising=False)

    import pipeline.agents.planner as planner_mod

    seen = {}
    real_run = planner_mod.PlannerNode.run

    def spy(self, ctx):
        seen["force_stub"] = os.environ.get("ANIMA_FORCE_STUB")
        return real_run(self, ctx)

    monkeypatch.setattr(planner_mod.PlannerNode, "run", spy)

    # no --stub: the stub-marker guard fails the run (rc 1), but the env var
    # must never have been exported on this non-stub invocation.
    rc = run_cli.main(["--brief", str(brief_dir), "--skip-smoke",
                       "--run-dir", str(root / "runs" / "x")])
    assert rc == 1
    assert seen["force_stub"] is None
    assert "ANIMA_FORCE_STUB" not in os.environ
