"""Unit suite for the Higgsfield image transport (decision D5, plan T1).

Every test is credential-free AND network-free: the real path is reached only
through the _run_cli seam, which tests monkeypatch. Sean's machine has an
authenticated `higgsfield` binary on PATH, so an unmocked real call would
SPEND CREDITS — never let one escape this file.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.agents.higgsfield_runner import (
    HIGGSFIELD_IMAGE_MODELS,
    HiggsfieldResponse,
    invoke_higgsfield_image_edit,
)
from pipeline.agents.nb_pro_runner import UnwiredTransportError
from pipeline.registers import GPT_IMAGE


def _mk_ref(tmp_path: Path, name: str = "ref.png") -> Path:
    p = tmp_path / name
    p.write_bytes(b"\x89PNG\r\n\x1a\nfakebytes")
    return p


def test_transport_map_carries_gpt_image():
    assert HIGGSFIELD_IMAGE_MODELS == {GPT_IMAGE: "gpt_image_2"}


def test_unmapped_model_raises_unwired(tmp_path):
    with pytest.raises(UnwiredTransportError):
        invoke_higgsfield_image_edit(
            prompt="x", reference_images=[], output_path=tmp_path / "o.png",
            cache_dir=tmp_path / "c", model="not-a-model",
        )


def test_force_stub_writes_placeholder(tmp_path, monkeypatch):
    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")
    resp = invoke_higgsfield_image_edit(
        prompt="plate", reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "out" / "o.png", cache_dir=tmp_path / "c",
    )
    assert resp.ok and resp.stub_fallback and not resp.cache_hit
    assert resp.output_path.exists()


def test_missing_cli_stubs(tmp_path, monkeypatch):
    monkeypatch.delenv("ANIMA_FORCE_STUB", raising=False)
    monkeypatch.setattr(
        "pipeline.agents.higgsfield_runner.shutil.which", lambda _: None
    )
    resp = invoke_higgsfield_image_edit(
        prompt="plate", reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png", cache_dir=tmp_path / "c",
    )
    assert resp.ok and resp.stub_fallback


def test_stub_never_populates_real_cache(tmp_path, monkeypatch):
    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")
    kwargs = dict(
        prompt="plate", reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png", cache_dir=tmp_path / "c",
    )
    first = invoke_higgsfield_image_edit(**kwargs)
    second = invoke_higgsfield_image_edit(**kwargs)
    assert not first.cache_hit and not second.cache_hit
    assert first.stub_fallback and second.stub_fallback
    assert first.cache_key == second.cache_key
    assert not list((tmp_path / "c").glob("*.png"))


def test_cache_key_varies_on_explicit_params(tmp_path, monkeypatch):
    """D5: resolution/quality/aspect/reject/model are all part of the key."""
    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")
    base = dict(
        prompt="plate", reference_images=[_mk_ref(tmp_path)],
        output_path=tmp_path / "o.png", cache_dir=tmp_path / "c",
    )
    k0 = invoke_higgsfield_image_edit(**base).cache_key
    assert invoke_higgsfield_image_edit(**base, quality="medium").cache_key != k0
    assert invoke_higgsfield_image_edit(**base, resolution="2k").cache_key != k0
    assert invoke_higgsfield_image_edit(**base, aspect_ratio="16:9").cache_key != k0
    assert invoke_higgsfield_image_edit(**base, reject_reason="fix jaw").cache_key != k0


def test_cache_key_preserves_anchor_first_reference_order(tmp_path, monkeypatch):
    monkeypatch.setenv("ANIMA_FORCE_STUB", "1")
    anchor = _mk_ref(tmp_path, "anchor.png")
    pose = _mk_ref(tmp_path, "pose.png")
    pose.write_bytes(b"different")
    base = dict(prompt="plate", output_path=tmp_path / "o.png", cache_dir=tmp_path / "c")
    k_anchor_first = invoke_higgsfield_image_edit(
        **base, reference_images=[anchor, pose]
    ).cache_key
    k_pose_first = invoke_higgsfield_image_edit(
        **base, reference_images=[pose, anchor]
    ).cache_key
    assert k_anchor_first != k_pose_first
