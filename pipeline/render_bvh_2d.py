#!/usr/bin/env python3
"""
Render BVH skeleton as 2D stick figure frames using PIL.

Bypasses Blender entirely — parses BVH via bvhio, computes forward kinematics,
projects 3D joint positions to 2D, draws circles + lines on a canvas.

Usage:
    python3 pipeline/render_bvh_2d.py \
        --bvh runs/kimodo_motion/act1_beat1_test.bvh \
        --output-dir runs/kimodo_motion/pose_frames/ \
        --fps 12

Requires: pip install bvhio Pillow
"""

import argparse
import math
import os
import sys

from PIL import Image, ImageDraw

try:
    import bvhio
    import glm
except ImportError:
    print("Error: bvhio required. Install with: pip install bvhio", file=sys.stderr)
    sys.exit(1)


BG_GREEN = (90, 180, 90)
BG_WHITE = (255, 255, 255)
BONE_COLOR = (40, 40, 40)
JOINT_COLOR = (60, 60, 60)

# Major body joints to render (skip finger bones for cleaner pose reference)
SKIP_PREFIXES = (
    "LeftHandThumb", "LeftHandIndex", "LeftHandMiddle", "LeftHandRing", "LeftHandPinky",
    "RightHandThumb", "RightHandIndex", "RightHandMiddle", "RightHandRing", "RightHandPinky",
    "Jaw", "LeftEye", "RightEye", "HeadEnd",
    "LeftToeEnd", "RightToeEnd",
)


def get_all_joints(joint):
    """Recursively collect all joints."""
    joints = [joint]
    for child in joint.Children:
        joints.extend(get_all_joints(child))
    return joints


def compute_world_positions(joint, frame, parent_world_pos, parent_world_rot):
    """
    Forward kinematics: compute world position for each joint at a given frame.
    Returns list of (name, world_pos_vec3, parent_world_pos_vec3_or_None).
    """
    kf = joint.Keyframes[frame]
    local_pos = kf.Position
    local_rot = kf.Rotation

    # World position = parent_pos + parent_rot * local_pos
    world_pos = parent_world_pos + parent_world_rot * local_pos
    # World rotation = parent_rot * local_rot
    world_rot = parent_world_rot * local_rot

    results = [(joint.Name, world_pos, parent_world_pos)]

    for child in joint.Children:
        results.extend(compute_world_positions(child, frame, world_pos, world_rot))

    return results


def project_to_2d(positions, canvas_size, view="front-3/4", padding=0.12):
    """Project 3D positions to 2D canvas. Returns list of (name, (sx,sy), parent_screen)."""

    # Collect all 3D points for bounds calculation
    all_pts = []
    for name, pos, ppos in positions:
        all_pts.append((pos.x, pos.y, pos.z))
        if ppos is not None:
            all_pts.append((ppos.x, ppos.y, ppos.z))

    def project_point(px, py, pz):
        """Project a 3D point based on view angle.
        BVH coordinate system: X=right, Y=up, Z=forward."""
        if view == "front":
            return px, -py  # X right, Y up (negate for screen)
        elif view == "side":
            return pz, -py  # Z depth → screen X, Y up
        elif view == "front-3/4":
            angle = math.radians(30)
            return px * math.cos(angle) + pz * math.sin(angle), -py
        return px, -py

    # Project all points to find bounds
    proj_pts = [project_point(x, y, z) for x, y, z in all_pts]
    xs = [p[0] for p in proj_pts]
    ys = [p[1] for p in proj_pts]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    range_x = max_x - min_x or 1
    range_y = max_y - min_y or 1
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2

    w, h = canvas_size
    usable_w = w * (1 - 2 * padding)
    usable_h = h * (1 - 2 * padding)
    scale = min(usable_w / range_x, usable_h / range_y)

    projected = []
    for name, pos, ppos in positions:
        px2d, py2d = project_point(pos.x, pos.y, pos.z)
        sx = (px2d - center_x) * scale + w / 2
        sy = (py2d - center_y) * scale + h / 2

        parent_screen = None
        if ppos is not None:
            ppx, ppy = project_point(ppos.x, ppos.y, ppos.z)
            parent_screen = (
                (ppx - center_x) * scale + w / 2,
                (ppy - center_y) * scale + h / 2,
            )

        projected.append((name, (sx, sy), parent_screen))

    return projected


def draw_skeleton(projected, canvas_size, bg_color=BG_GREEN,
                  bone_width=4, joint_radius=6):
    """Draw stick figure on canvas."""
    img = Image.new("RGB", canvas_size, bg_color)
    draw = ImageDraw.Draw(img)

    # Filter out finger/end bones for cleaner output
    filtered = [(n, p, pp) for n, p, pp in projected
                if not n.startswith(SKIP_PREFIXES)]

    # Draw bones
    for name, pos, parent_pos in filtered:
        if parent_pos is not None:
            draw.line([parent_pos, pos], fill=BONE_COLOR, width=bone_width)

    # Draw joints
    for name, pos, _ in filtered:
        x, y = pos
        r = joint_radius
        # Larger dot for head, hips
        if name in ("Head", "Hips"):
            r = joint_radius * 2
        draw.ellipse([x - r, y - r, x + r, y + r], fill=JOINT_COLOR)

    return img


def main():
    parser = argparse.ArgumentParser(description="Render BVH as 2D stick figure frames")
    parser.add_argument("--bvh", required=True, help="Path to BVH file")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    parser.add_argument("--fps", type=int, default=12, help="Target FPS (default: 12)")
    parser.add_argument("--start", type=int, default=0, help="Start frame (default: 0)")
    parser.add_argument("--end", type=int, default=0, help="End frame (0=all)")
    parser.add_argument("--resolution", default="1920x1080", help="Canvas WxH")
    parser.add_argument("--view", default="front-3/4",
                        choices=["front", "side", "front-3/4"])
    parser.add_argument("--background", default="green",
                        choices=["green", "white"])
    parser.add_argument("--bone-width", type=int, default=4)
    parser.add_argument("--joint-radius", type=int, default=6)

    args = parser.parse_args()
    w, h = [int(x) for x in args.resolution.split("x")]
    canvas_size = (w, h)
    bg_color = BG_GREEN if args.background == "green" else BG_WHITE

    os.makedirs(args.output_dir, exist_ok=True)

    print("=" * 60)
    print("BVH 2D Stick Figure Renderer")
    print("=" * 60)

    print(f"Loading: {args.bvh}")
    bvh = bvhio.readAsBvh(args.bvh)
    root = bvh.Root

    n_frames = bvh.FrameCount
    bvh_fps = round(1.0 / bvh.FrameTime) if bvh.FrameTime > 0 else 30
    joints = get_all_joints(root)
    print(f"  Joints: {len(joints)}, Frames: {n_frames}, BVH FPS: {bvh_fps}")

    start = args.start
    end = min(args.end if args.end > 0 else n_frames - 1, n_frames - 1)

    # Subsample to target FPS
    step = max(1, round(bvh_fps / args.fps))
    frame_indices = list(range(start, end + 1, step))
    print(f"  Rendering {len(frame_indices)} frames (step={step}, target {args.fps}fps)")
    print(f"  View: {args.view}, Resolution: {w}x{h}")

    identity_pos = glm.vec3(0, 0, 0)
    identity_rot = glm.quat(1, 0, 0, 0)

    for i, frame_idx in enumerate(frame_indices):
        positions = compute_world_positions(root, frame_idx, identity_pos, identity_rot)
        projected = project_to_2d(positions, canvas_size, view=args.view)
        img = draw_skeleton(projected, canvas_size, bg_color=bg_color,
                            bone_width=args.bone_width, joint_radius=args.joint_radius)

        out_path = os.path.join(args.output_dir, f"pose_F{i + 1:04d}.png")
        img.save(out_path)

        if (i + 1) % 10 == 0 or i == 0 or i == len(frame_indices) - 1:
            progress = (i + 1) / len(frame_indices) * 100
            print(f"  Frame {i + 1}/{len(frame_indices)} ({progress:.0f}%) → {out_path}")

    print(f"\nDone: {len(frame_indices)} frames → {args.output_dir}")


if __name__ == "__main__":
    main()
