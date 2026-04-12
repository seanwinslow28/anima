#!/usr/bin/env python3
"""Composite sprite onto Sean-only frames for flight path and fade.

Handles two transitions:
1. F28→F31 flight: sprite travels along a parabolic arc from F28 position to F31 shoulder
2. F36→F40 fade: sprite dissolves at 66% and 33% opacity on existing IB frames

Uses multiply blend mode to preserve paper texture through the sprite.
"""

import math
import argparse
from pathlib import Path
from PIL import Image, ImageChops
import numpy as np


# --- Sprite position data (measured from approved keyframes) ---

# F28: sprite bouncing at arm's length, right side of frame
F28_POS = (955, 330)   # center (x, y)
F28_HEIGHT = 130       # approximate sprite height in pixels

# F31: sprite seated on left shoulder
F31_POS = (603, 110)   # center (x, y)
F31_HEIGHT = 80        # approximate sprite height in pixels

# Flight arc height (pixels above straight line at midpoint)
ARC_HEIGHT = 100


def sprite_position(t, start=F28_POS, end=F31_POS, arc_height=ARC_HEIGHT):
    """Interpolate sprite position along a parabolic arc.

    t: 0.0 (at F28) to 1.0 (at F31)
    arc_height: pixels above the straight-line path at midpoint
    """
    x = start[0] * (1 - t) + end[0] * t
    y = start[1] * (1 - t) + end[1] * t
    # Parabolic arc offset — peaks at t=0.5
    y -= arc_height * math.sin(t * math.pi)
    return int(x), int(y)


def sprite_scale(t, start_h=F28_HEIGHT, end_h=F31_HEIGHT):
    """Interpolate sprite height with ease-out (fast departure, slow arrival)."""
    t_eased = 1 - (1 - t) ** 2
    return int(start_h * (1 - t_eased) + end_h * t_eased)


def load_sprite(path):
    """Load sprite asset and ensure RGBA mode."""
    sprite = Image.open(path).convert("RGBA")
    return sprite


def resize_sprite(sprite, target_height):
    """Resize sprite maintaining aspect ratio to target height."""
    if target_height <= 0:
        target_height = 1
    ratio = target_height / sprite.height
    new_width = max(1, int(sprite.width * ratio))
    return sprite.resize((new_width, target_height), Image.LANCZOS)


def composite_multiply(background, sprite, position):
    """Composite sprite using multiply blend mode.

    Multiply: result = (bg * sprite) / 255
    White pixels in sprite layer = no change to background.
    Dark pencil lines darken the paper texture beneath them.
    Paper grain shows through the sprite's lighter areas.
    """
    bg = background.convert("RGBA")
    w, h = bg.size

    # Create a white canvas and paste the sprite onto it
    sprite_layer = Image.new("RGBA", (w, h), (255, 255, 255, 255))

    # Calculate paste position (position is center, convert to top-left)
    paste_x = position[0] - sprite.width // 2
    paste_y = position[1] - sprite.height // 2

    # Only paste if within bounds
    if paste_x < w and paste_y < h:
        sprite_layer.paste(sprite, (paste_x, paste_y), sprite)

    # Multiply blend on RGB channels
    bg_rgb = bg.convert("RGB")
    sprite_rgb = sprite_layer.convert("RGB")
    multiplied = ImageChops.multiply(bg_rgb, sprite_rgb)

    return multiplied.convert("RGBA")


def composite_alpha(background, sprite, position, opacity=1.0):
    """Simple alpha composite with opacity control (fallback if multiply looks wrong)."""
    bg = background.convert("RGBA").copy()

    if opacity < 1.0:
        # Reduce sprite alpha by opacity factor
        sprite = sprite.copy()
        alpha = sprite.getchannel("A")
        alpha = alpha.point(lambda a: int(a * opacity))
        sprite.putalpha(alpha)

    paste_x = position[0] - sprite.width // 2
    paste_y = position[1] - sprite.height // 2

    if paste_x < bg.width and paste_y < bg.height:
        bg.paste(sprite, (paste_x, paste_y), sprite)

    return bg


def main():
    parser = argparse.ArgumentParser(description="Composite sprite onto Sean-only frames")
    parser.add_argument("--run-dir", type=Path, required=True, help="Run directory")
    parser.add_argument("--sprite", type=Path, required=True, help="Path to sprite RGBA PNG")
    parser.add_argument("--blend-mode", choices=["multiply", "alpha"], default="multiply",
                        help="Blend mode for compositing (default: multiply)")
    parser.add_argument("--dry-run", action="store_true", help="Print plan without compositing")
    args = parser.parse_args()

    approved = args.run_dir / "approved"
    composited = args.run_dir / "composited"
    composited.mkdir(exist_ok=True)

    sprite_img = load_sprite(args.sprite)
    print(f"Sprite loaded: {sprite_img.size}, mode={sprite_img.mode}")

    blend_fn = composite_multiply if args.blend_mode == "multiply" else composite_alpha

    # --- Flight path composites (F28→F31 IB01 and IB02) ---
    flight_frames = [
        ("PT_A1_F28toF31_IB01.png", 0.40),  # 40% of the way
        ("PT_A1_F28toF31_IB02.png", 0.75),  # 75% of the way
    ]

    print(f"\n=== Flight Path Composites (blend: {args.blend_mode}) ===")
    for filename, t in flight_frames:
        pos = sprite_position(t)
        height = sprite_scale(t)
        print(f"  {filename}: t={t:.2f}, pos={pos}, height={height}px")

        if not args.dry_run:
            sean_frame = Image.open(approved / filename)
            sized_sprite = resize_sprite(sprite_img, height)
            result = blend_fn(sean_frame, sized_sprite, pos)
            out_path = composited / filename
            result.convert("RGB").save(out_path)
            print(f"    -> Saved {out_path} ({out_path.stat().st_size // 1024}KB)")

    # --- Fade composites (F38 and F39) ---
    fade_frames = [
        ("PT_A1_F36toF40_IB01.png", 0.66),  # 66% opacity
        ("PT_A1_F36toF40_IB02.png", 0.33),  # 33% opacity
    ]

    print(f"\n=== Sprite Fade Composites ===")
    for filename, opacity in fade_frames:
        print(f"  {filename}: opacity={opacity:.0%}, pos={F31_POS}, height={F31_HEIGHT}px")

        if not args.dry_run:
            sean_frame = Image.open(approved / filename)
            sized_sprite = resize_sprite(sprite_img, F31_HEIGHT)

            if args.blend_mode == "multiply":
                # For fade with multiply: reduce sprite alpha first, then multiply blend
                faded_sprite = sized_sprite.copy()
                alpha = faded_sprite.getchannel("A")
                alpha = alpha.point(lambda a: int(a * opacity))
                faded_sprite.putalpha(alpha)
                result = composite_multiply(sean_frame, faded_sprite, F31_POS)
            else:
                result = composite_alpha(sean_frame, sized_sprite, F31_POS, opacity)

            out_path = composited / filename
            result.convert("RGB").save(out_path)
            print(f"    -> Saved {out_path} ({out_path.stat().st_size // 1024}KB)")

    print(f"\n=== Done ===")
    if not args.dry_run:
        print(f"Composited frames in: {composited}/")
        print(f"Next: copy approved composites to approved/ and rebuild assembly")
    else:
        print("(dry run — no files written)")


if __name__ == "__main__":
    main()
