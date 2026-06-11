"""Shared fixture builder for the run-orchestrator test suites (P0-P4).

Builds a hermetic mini-anima under tmp_path — two Bible'd characters
(folder keys alpha/beta, IR namespaces al/be), a brief dir with
00_studio_brief.md + shots.yaml, and a minimal manifest — then chdirs
into it (the orchestrator anchors repo-relative paths on CWD).
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml
from PIL import Image

CAST_FIXTURE = (("alpha", "al"), ("beta", "be"))


def write_png(path: Path, size: tuple[int, int] = (16, 9)) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", size, (200, 180, 150)).save(path, format="PNG")
    return path


def write_bible(root: Path, folder_key: str, namespace: str) -> Path:
    cdir = root / "characters" / folder_key
    cdir.mkdir(parents=True, exist_ok=True)
    write_png(cdir / "anchor.png")
    (cdir / "acceptance_criteria.json").write_text(
        json.dumps(
            {
                "version": "1.2",
                "locked": True,
                "criteria": [
                    {
                        "id": f"IR.{namespace}.style.line-weight",
                        "description": f"{namespace}: line weight stays steady.",
                        "cites_phase": [5],
                        "cites_personas": ["em"],
                        "character_id": namespace,
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return cdir


def default_shots() -> dict:
    return {
        "slug": "TT",
        "frames": [
            {"id": 1, "cast": ["al", "be"], "beat": "beat one", "prompt": "prompt one"},
            {"id": 2, "cast": ["al"], "beat": "beat two", "prompt": "prompt two", "hold": 3},
        ],
    }


def mk_project(tmp_path: Path, monkeypatch, *, shots: dict | None = None) -> tuple[Path, Path]:
    """Returns (project_root, brief_dir); cwd is the project root afterwards."""
    root = tmp_path / "proj"
    for folder_key, ns in CAST_FIXTURE:
        write_bible(root, folder_key, ns)

    brief_dir = root / "briefs" / "piece"
    brief_dir.mkdir(parents=True, exist_ok=True)
    (brief_dir / "00_studio_brief.md").write_text(
        "# Studio Brief\n\nA tiny two-character test piece.\n", encoding="utf-8"
    )
    (brief_dir / "shots.yaml").write_text(
        yaml.safe_dump(shots if shots is not None else default_shots()),
        encoding="utf-8",
    )

    # The real (self-contained) assembler — AssembleNode shells `bash
    # pipeline/assemble.sh` CWD-relative, so the hermetic project carries it.
    import shutil as _shutil

    real_assemble = Path(__file__).resolve().parents[1] / "pipeline" / "assemble.sh"
    (root / "pipeline").mkdir(parents=True, exist_ok=True)
    _shutil.copy2(real_assemble, root / "pipeline" / "assemble.sh")

    manifest = {
        "project": {"name": "test-piece"},
        "characters": {
            "alpha": {"folder": "characters/alpha/", "style_register": "pencil-test-colored"},
            "beta": {"folder": "characters/beta/", "style_register": "pencil-test-colored"},
        },
        "criteria_sources": {
            "bibles": [
                "characters/alpha/acceptance_criteria.json",
                "characters/beta/acceptance_criteria.json",
            ],
        },
    }
    (root / "manifest.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")

    monkeypatch.chdir(root)
    return root, brief_dir


def force_stub_sdk(monkeypatch) -> None:
    """The established stub-green convention: no SDK, no API key -> deterministic stubs."""
    from pipeline.agents import sdk_runners

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(sdk_runners, "_sdk_available", lambda: False)


def stub_critic_env(monkeypatch) -> None:
    """Force BOTH Em transports onto their deterministic stubs.

    Pointing ANTI_GRAVITY_BIN at a nonexistent command hides agy surgically
    (PATH stays intact for bash/ffmpeg/file) -> cli_runners stub:
    borderline@0.65, cites AC01 — below the 0.7 threshold, so Em always
    escalates to the Opus vision stub (borderline@0.78, cites AC01).
    force_stub_sdk covers that Opus leg.
    """
    import pipeline.agents.cli_runners as cli_runners

    monkeypatch.setattr(cli_runners, "ANTI_GRAVITY_BIN", "agy-disabled-for-tests")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    force_stub_sdk(monkeypatch)


def fake_flo_generate(monkeypatch) -> list[dict]:
    """Fake pipeline.generate.generate_frame at the established boundary
    (tests/test_dag.py convention), writing REAL 1376x768 PNGs — the audit
    gate PIL-opens candidates uncaught. Content varies by attempt so a
    re-roll yields fresh bytes (and fresh Em cache keys)."""
    from pipeline import generate as legacy_generate

    calls: list[dict] = []

    def _fake(*, frame_num, prompt, references, manifest, run_dir):
        candidates_dir = Path(run_dir) / "candidates" / f"F{frame_num:02d}"
        candidates_dir.mkdir(parents=True, exist_ok=True)
        attempt = len(list(candidates_dir.glob("attempt_*.png"))) + 1
        out = candidates_dir / f"attempt_{attempt:02d}.png"
        calls.append(
            {"frame_num": frame_num, "prompt": prompt,
             "references": [str(r) for r in references], "attempt": attempt}
        )
        Image.new(
            "RGB", (1376, 768), (200 - attempt * 3, 180, 100 + frame_num)
        ).save(out, format="PNG")
        return out

    monkeypatch.setattr(legacy_generate, "generate_frame", _fake)
    return calls


def fake_ffmpeg_path(tmp_path: Path, monkeypatch) -> Path:
    """The tests/test_assemble.py PATH-shim pattern: a stub ffmpeg that just
    creates its output file (last arg) — assemble.sh runs for real, encodes don't."""
    import os

    shim_dir = tmp_path / "fakebin"
    shim_dir.mkdir(parents=True, exist_ok=True)
    shim = shim_dir / "ffmpeg"
    shim.write_text(
        '#!/usr/bin/env bash\nout="${@: -1}"\n: > "$out"\nexit 0\n', encoding="utf-8"
    )
    shim.chmod(0o755)
    monkeypatch.setenv("PATH", f"{shim_dir}:{os.environ['PATH']}")
    return shim_dir


def fake_em_transport(
    monkeypatch,
    *,
    verdict: str = "pass",
    confidence: float = 0.95,
    cites: tuple = ("IR.al.style.line-weight",),
    patches: tuple = (),
) -> list[dict]:
    """Replace both Em vision transports with a deterministic high-confidence
    payload (no escalation), so tests can steer verdict/cites/patches."""
    import json as _json
    from types import SimpleNamespace

    import pipeline.agents.vision_critic as vc

    calls: list[dict] = []

    async def _fake(*, prompt, image_paths, timeout_s=120):
        calls.append({"prompt": prompt, "image_paths": [str(p) for p in image_paths]})
        payload = {
            "verdict": verdict,
            "confidence": confidence,
            "reasoning": "fake-em",
            "cites_criteria": list(cites),
            "proposed_patches": [dict(p) for p in patches],
        }
        return SimpleNamespace(text=_json.dumps(payload))

    monkeypatch.setattr(vc, "run_antigravity_with_image", _fake)
    monkeypatch.setattr(vc, "run_gemini_api_with_image", _fake)
    return calls
