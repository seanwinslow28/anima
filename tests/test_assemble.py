"""#13: assemble.sh generalization — PT_A1 stays byte-identical.

assemble.sh hardcoded the PT_A1 frame sequence, the `PT_A1_` source prefix, and
the `pencil-test-act1` output slug. Slice 1 generalizes it to accept an optional
`--sequence-file` + `--slug` (defaulting to today's PT_A1 behavior), so Slice 2's
orchestrator can drive an arbitrary piece.

Tests are hermetic: a fake-ffmpeg PATH shim runs the real staging logic without
encoding anything, so we assert on the staged `export/sequence/` directory and
the planned output filenames — fast, CI-safe, no real ffmpeg.

The golden back-compat test is a REGRESSION GUARD: it locks today's PT_A1 staging
(frame → source-key, in order) and must stay green before and after the change.
The custom-sequence and node-threading tests drive the new behavior.
"""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[1]
ASSEMBLE_SH = REPO / "pipeline" / "assemble.sh"

# The 27 PT_A1 source keys the embedded FRAME_SEQ references (fixture inputs —
# the *order* and *holds* are owned by assemble.sh, not re-encoded here).
PT_A1_KEYS = [
    "F01_key", "F01toF06_IB01", "F01toF06_IB02", "F01toF06_IB03", "F06_key",
    "F06toF10_IB01", "F10_key", "F10toF13_IB01", "F13_key", "F13toF18_IB01",
    "F13toF18_IB02", "F13toF18_IB03", "F18_key", "F20_key", "F22_key",
    "F24_key", "F26_key", "F28_key", "F28toF31_IB01_comp", "F28toF31_IB02_comp",
    "F31_key", "F31toF36_IB01", "F31toF36_IB02", "F36_key", "F36toF40_IB01",
    "F36toF40_IB02", "F40_key",
]

# Locked golden digest of the PT_A1 staged sequence (ordered frame→source-key
# manifest). Captured from the current script; any drift in staging order,
# holds, or prefix changes this and fails loudly.
_GOLDEN_PT_A1_SEQUENCE = "70a977a2ad80b4bbe40327d35e1cb7214d6eda2b4505fdca36a7c2ba7a81498c"


def _make_png(path: Path, seed: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (4, 4), (seed % 256, (seed * 5) % 256, (seed * 11) % 256)).save(
        path, "PNG"
    )


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _fake_ffmpeg_env(tmp_path: Path) -> dict:
    """A PATH with a stub ffmpeg that just creates its output file (last arg)."""
    shim_dir = tmp_path / "fakebin"
    shim_dir.mkdir(parents=True, exist_ok=True)
    shim = shim_dir / "ffmpeg"
    shim.write_text(
        '#!/usr/bin/env bash\nout="${@: -1}"\n: > "$out"\nexit 0\n', encoding="utf-8"
    )
    shim.chmod(0o755)
    env = dict(os.environ)
    env["PATH"] = f"{shim_dir}:{env['PATH']}"
    return env


def _run(run_dir: Path, *args: str, env: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(ASSEMBLE_SH), str(run_dir), *args],
        env=env, capture_output=True, text=True,
    )


def _staged_frames(run_dir: Path) -> list[Path]:
    seq = run_dir / "export" / "sequence"
    return sorted(seq.glob("frame_*.png"))


def test_assemble_pt_a1_sequence_byte_identical_golden(tmp_path):
    """REGRESSION GUARD: no slug/sequence args → today's exact PT_A1 staging."""
    run_dir = tmp_path / "run"
    approved = run_dir / "approved"
    for i, key in enumerate(PT_A1_KEYS):
        _make_png(approved / f"PT_A1_{key}.png", seed=i + 1)

    proc = _run(run_dir, env=_fake_ffmpeg_env(tmp_path))
    assert proc.returncode == 0, proc.stderr

    # Reconstruct frame → source-key from content (cp is a byte copy).
    sha_to_key = {_sha((approved / f"PT_A1_{k}.png").read_bytes()): k for k in PT_A1_KEYS}
    frames = _staged_frames(run_dir)
    manifest = "\n".join(
        f"{n:04d}:{sha_to_key[_sha(f.read_bytes())]}"
        for n, f in enumerate(frames, start=1)
    )
    assert _sha(manifest.encode()) == _GOLDEN_PT_A1_SEQUENCE

    export = run_dir / "export"
    for ext in ("mp4", "webm", "gif"):
        assert (export / f"pencil-test-act1.{ext}").exists()


def test_assemble_custom_sequence_and_slug(tmp_path):
    """A custom sequence-file (full-basename keys) + --slug stages from those
    sources with no PT_A1_ prefix and writes slugged outputs."""
    run_dir = tmp_path / "run"
    approved = run_dir / "approved"
    _make_png(approved / "SS_F01_key.png", seed=101)
    _make_png(approved / "SS_F03b_key.png", seed=202)

    seq_file = run_dir / "export" / "sequence.txt"
    seq_file.parent.mkdir(parents=True, exist_ok=True)
    seq_file.write_text("SS_F01_key:2\nSS_F03b_key:2\n", encoding="utf-8")

    proc = _run(
        run_dir, "--slug", "spark", "--sequence-file", str(seq_file),
        env=_fake_ffmpeg_env(tmp_path),
    )
    assert proc.returncode == 0, proc.stderr

    frames = _staged_frames(run_dir)
    assert len(frames) == 4  # holds 2 + 2
    f01 = (approved / "SS_F01_key.png").read_bytes()
    f03b = (approved / "SS_F03b_key.png").read_bytes()
    assert [f.read_bytes() for f in frames] == [f01, f01, f03b, f03b]

    export = run_dir / "export"
    for ext in ("mp4", "webm", "gif"):
        assert (export / f"spark.{ext}").exists()
        assert not (export / f"pencil-test-act1.{ext}").exists()


# --------------------------------------------------------------------------- #
# AssembleNode threading (default → legacy argv; inputs → flags)
# --------------------------------------------------------------------------- #

def test_assemble_node_legacy_argv_when_no_inputs(tmp_path, monkeypatch):
    import pipeline.nodes.assemble as node_mod
    from pipeline.agents import AgentContext, NODE_REGISTRY
    import pipeline.nodes  # noqa: F401  (fires @register_node)

    captured: dict = {}

    def fake_run(argv, **kwargs):
        captured["argv"] = argv
        return subprocess.CompletedProcess(argv, 0)

    monkeypatch.setattr(node_mod.subprocess, "run", fake_run)
    ctx = AgentContext(
        run_dir=tmp_path, inputs={"run_dir": str(tmp_path)}, manifest={},
        criteria=None, tier="draft", cache_dir=tmp_path / ".cache",
    )
    NODE_REGISTRY["assemble"]().run(ctx)
    assert captured["argv"] == ["bash", "pipeline/assemble.sh", str(tmp_path)]


def test_assemble_node_threads_slug_and_sequence_file(tmp_path, monkeypatch):
    import pipeline.nodes.assemble as node_mod
    from pipeline.agents import AgentContext, NODE_REGISTRY
    import pipeline.nodes  # noqa: F401

    captured: dict = {}

    def fake_run(argv, **kwargs):
        captured["argv"] = argv
        return subprocess.CompletedProcess(argv, 0)

    monkeypatch.setattr(node_mod.subprocess, "run", fake_run)
    ctx = AgentContext(
        run_dir=tmp_path,
        inputs={
            "run_dir": str(tmp_path),
            "slug": "spark",
            "sequence_file": "export/sequence.txt",
        },
        manifest={}, criteria=None, tier="draft", cache_dir=tmp_path / ".cache",
    )
    NODE_REGISTRY["assemble"]().run(ctx)
    argv = captured["argv"]
    assert argv[:3] == ["bash", "pipeline/assemble.sh", str(tmp_path)]
    assert "--slug" in argv and argv[argv.index("--slug") + 1] == "spark"
    assert "--sequence-file" in argv
    assert argv[argv.index("--sequence-file") + 1] == "export/sequence.txt"
