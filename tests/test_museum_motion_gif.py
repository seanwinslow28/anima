from pathlib import Path

from PIL import Image

from pipeline.museum.motion_gif import assemble_loop_gif


def _rgba(path: Path, size, color):
    img = Image.new("RGBA", size, (0, 0, 0, 0))  # transparent bg
    # a solid blob so the frame isn't empty
    blob = Image.new("RGBA", (size[0] // 2, size[1] // 2), color)
    img.paste(blob, (size[0] // 4, size[1] // 4))
    img.save(path)


def test_assemble_loop_gif_animated_and_padded(tmp_path: Path):
    f1 = tmp_path / "a.png"
    f2 = tmp_path / "b.png"
    _rgba(f1, (40, 60), (200, 100, 60, 255))
    _rgba(f2, (80, 40), (200, 100, 60, 255))  # different size on purpose
    out = tmp_path / "loop.gif"
    result = assemble_loop_gif([f1, f2], out, duration_ms=120, pingpong=True)
    assert result == out and out.exists()
    gif = Image.open(out)
    assert gif.format == "GIF"
    assert getattr(gif, "n_frames", 1) > 1          # actually animated
    # Canvas normalized to the max dims (+ padding) so frames don't jitter.
    assert gif.size[0] >= 80 and gif.size[1] >= 60


def test_assemble_loop_gif_empty_returns_none(tmp_path: Path):
    assert assemble_loop_gif([], tmp_path / "x.gif") is None
