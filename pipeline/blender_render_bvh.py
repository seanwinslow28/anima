#!/usr/bin/env python3
"""
Blender BVH Render Script — Orthographic camera, batch frame export.

Imports a BVH motion file (e.g. from Kimodo), sets up a fixed orthographic
camera matching the animation's 3/4 front-facing view, and renders each
frame as a flat 2D-style reference image for NB2 pose-from-reference.

Usage (run from command line via Blender):
    blender --background --python pipeline/blender_render_bvh.py -- \
        --bvh path/to/motion.bvh \
        --output-dir runs/{run_id}/pose_reference/ \
        --start 1 --end 42 \
        --fps 12 \
        --camera-angle front-3/4

    # Quick test with defaults:
    blender --background --python pipeline/blender_render_bvh.py -- \
        --bvh motion.bvh --output-dir ./pose_frames/

Requires:
    Blender 3.6+ (tested with 4.x)
    BVH file exported from Kimodo (SOMA skeleton) or any standard BVH

Output:
    PNG frames: pose_F{####}.png (transparent or solid background)
    These become NB2 pose references — style doesn't matter, only pose clarity.
"""

import sys
import argparse
import math

# Blender modules — only available when run inside Blender
try:
    import bpy
    import mathutils
except ImportError:
    print("Error: This script must be run inside Blender.", file=sys.stderr)
    print("Usage: blender --background --python pipeline/blender_render_bvh.py -- [args]",
          file=sys.stderr)
    sys.exit(1)


# --- Camera presets ---
# Each preset defines camera location and rotation for a fixed viewing angle.
# These simulate common animation reference angles.
CAMERA_PRESETS = {
    # Classic 3/4 front view — matches most character animation storyboards
    # SOMA BVH uses centimeter units: character ~170cm tall, hips at ~100cm
    "front-3/4": {
        "location": (350, -500, 100),
        "rotation_euler": (math.radians(80), 0, math.radians(30)),
        "ortho_scale": 250,
    },
    # Dead-on front view — good for facial expression reference
    "front": {
        "location": (0, -600, 100),
        "rotation_euler": (math.radians(85), 0, 0),
        "ortho_scale": 250,
    },
    # Side view — good for walk cycles and profile poses
    "side": {
        "location": (600, 0, 100),
        "rotation_euler": (math.radians(85), 0, math.radians(90)),
        "ortho_scale": 250,
    },
    # Slight high angle — adds a bit of depth for dynamic poses
    "high-3/4": {
        "location": (350, -500, 200),
        "rotation_euler": (math.radians(65), 0, math.radians(30)),
        "ortho_scale": 300,
    },
}


def clear_scene():
    """Remove all default objects from the scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def import_bvh(bvh_path, fps=12):
    """Import a BVH file and configure playback."""
    bpy.ops.import_anim.bvh(
        filepath=bvh_path,
        filter_glob="*.bvh",
        global_scale=1.0,
        frame_start=1,
        use_fps_scale=True,
        update_scene_fps=False,
        update_scene_duration=True,
        use_cyclic=False,
        rotate_mode='NATIVE',
    )

    # Find the imported armature
    armature = None
    for obj in bpy.context.scene.objects:
        if obj.type == 'ARMATURE':
            armature = obj
            break

    if armature is None:
        print("Error: No armature found after BVH import.", file=sys.stderr)
        sys.exit(1)

    print(f"Imported armature: {armature.name}")
    print(f"  Bones: {len(armature.data.bones)}")

    # Set scene FPS
    bpy.context.scene.render.fps = fps
    bpy.context.scene.render.fps_base = 1.0

    return armature


def setup_camera(preset_name="front-3/4", ortho_scale_override=None):
    """Create and configure an orthographic camera."""
    preset = CAMERA_PRESETS.get(preset_name)
    if preset is None:
        print(f"Error: Unknown camera preset '{preset_name}'", file=sys.stderr)
        print(f"Available: {', '.join(CAMERA_PRESETS.keys())}", file=sys.stderr)
        sys.exit(1)

    bpy.ops.object.camera_add()
    camera = bpy.context.active_object
    camera.name = "PoseCamera"

    # Orthographic — eliminates perspective distortion for flat 2D reference
    camera.data.type = 'ORTHO'
    camera.data.ortho_scale = ortho_scale_override or preset["ortho_scale"]

    camera.location = preset["location"]
    camera.rotation_euler = mathutils.Euler(preset["rotation_euler"], 'XYZ')

    # Set as active camera
    bpy.context.scene.camera = camera

    print(f"Camera: {preset_name} (orthographic, scale={camera.data.ortho_scale})")
    return camera


def setup_lighting():
    """Add neutral, even lighting — no dramatic shadows."""
    # Key light — soft, from slightly above
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 5))
    sun = bpy.context.active_object
    sun.name = "KeyLight"
    sun.data.energy = 2.0
    sun.rotation_euler = (math.radians(30), 0, 0)

    # Fill light — dimmer, from the opposite side
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 5))
    fill = bpy.context.active_object
    fill.name = "FillLight"
    fill.data.energy = 1.0
    fill.rotation_euler = (math.radians(45), 0, math.radians(180))


def build_skeleton_mesh(armature):
    """
    Create renderable mesh geometry from armature bones.

    BVH imports are bones-only (no mesh), so armature display modes
    don't appear in renders. This builds a real mesh: one edge per bone,
    with a Skin modifier for thickness, parented to the armature.
    """
    import bmesh

    bm = bmesh.new()

    # Map bone names to bmesh verts
    bone_verts = {}

    for bone in armature.data.bones:
        # Create vert at bone head (if not already created by parent)
        if bone.name not in bone_verts:
            v_head = bm.verts.new(bone.head_local)
            bone_verts[bone.name] = v_head

        # Create vert at bone tail
        v_tail = bm.verts.new(bone.tail_local)

        # Edge from head to tail
        bm.edges.new((bone_verts[bone.name], v_tail))

        # If this bone has children, they should start from our tail
        for child in bone.children:
            bone_verts[child.name] = v_tail

    # Write to mesh
    mesh = bpy.data.meshes.new("SkeletonMesh")
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new("Skeleton", mesh)
    bpy.context.collection.objects.link(obj)

    # Skin modifier — gives edges cylindrical thickness
    skin = obj.modifiers.new("Skin", 'SKIN')
    # Set radius scaled to skeleton size — SOMA BVH uses centimeter units
    # Keep thin relative to bone length to avoid webbing at joints
    for sv in mesh.skin_vertices[0].data:
        sv.radius = (0.5, 0.5)

    # Subdivision for smoother joints
    sub = obj.modifiers.new("Subsurf", 'SUBSURF')
    sub.levels = 1
    sub.render_levels = 1

    # Create vertex groups matching bone names for armature deform
    for bone in armature.data.bones:
        obj.vertex_groups.new(name=bone.name)

    # Assign each vert to closest bone's vertex group
    # Since we built verts at bone heads/tails, assign head vert to bone group
    # and tail vert to bone group (or child bone group)
    bm2 = bmesh.new()
    bm2.from_mesh(mesh)
    bm2.verts.ensure_lookup_table()

    vi = 0
    for bone in armature.data.bones:
        # Head vert
        vg = obj.vertex_groups.get(bone.name)
        if vg:
            vg.add([vi], 1.0, 'REPLACE')
        vi += 1
        # Tail vert — assign to this bone
        if vg:
            vg.add([vi], 1.0, 'REPLACE')
        vi += 1

    bm2.free()

    # Parent to armature with armature modifier
    obj.parent = armature
    arm_mod = obj.modifiers.new("Armature", 'ARMATURE')
    arm_mod.object = armature

    # Flat dark material
    mat = bpy.data.materials.new(name="SkeletonMat")
    mat.diffuse_color = (0.15, 0.15, 0.15, 1.0)  # Dark gray for Workbench
    obj.data.materials.append(mat)

    print(f"Built skeleton mesh: {len(armature.data.bones)} bones, "
          f"{len(mesh.vertices)} verts, {len(mesh.edges)} edges")
    return obj


def setup_render(output_dir, resolution=(1920, 1080), background="transparent"):
    """Configure render settings for batch frame export."""
    scene = bpy.context.scene
    render = scene.render

    # Resolution — match pipeline target
    render.resolution_x = resolution[0]
    render.resolution_y = resolution[1]
    render.resolution_percentage = 100

    # PNG output
    render.image_settings.file_format = 'PNG'
    render.image_settings.color_mode = 'RGBA' if background == "transparent" else 'RGB'
    render.image_settings.compression = 15

    # Transparent background (film alpha)
    if background == "transparent":
        scene.render.film_transparent = True
    elif background == "green":
        scene.render.film_transparent = False
        scene.world = bpy.data.worlds.new("GreenScreen")
        scene.world.use_nodes = True
        bg_node = scene.world.node_tree.nodes["Background"]
        bg_node.inputs['Color'].default_value = (0.0, 1.0, 0.0, 1.0)
    else:
        scene.render.film_transparent = False
        scene.world = bpy.data.worlds.new("WhiteBG")
        scene.world.use_nodes = True
        bg_node = scene.world.node_tree.nodes["Background"]
        bg_node.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)

    # Use Workbench — it renders armature display types (sticks) directly,
    # unlike EEVEE which ignores armature overlays
    render.engine = 'BLENDER_WORKBENCH'

    # Output path template
    render.filepath = f"{output_dir}/pose_F"

    print(f"Render: {resolution[0]}x{resolution[1]}, {background} background, EEVEE")


def render_frames(output_dir, start_frame, end_frame):
    """Render each frame as a separate PNG."""
    scene = bpy.context.scene
    total = end_frame - start_frame + 1

    for frame in range(start_frame, end_frame + 1):
        scene.frame_set(frame)
        filepath = f"{output_dir}/pose_F{frame:04d}.png"
        scene.render.filepath = filepath
        bpy.ops.render.render(write_still=True)

        progress = (frame - start_frame + 1) / total * 100
        print(f"  Rendered frame {frame}/{end_frame} ({progress:.0f}%) → {filepath}")

    print(f"Done: {total} frames rendered to {output_dir}/")


def auto_frame_armature(armature, camera):
    """
    Adjust camera ortho_scale to frame the full armature with padding.
    Evaluates the armature bounding box at the current frame.
    """
    # Get bounding box of armature and children
    min_co = mathutils.Vector((float('inf'),) * 3)
    max_co = mathutils.Vector((float('-inf'),) * 3)

    objects = [armature] + list(armature.children)
    for obj in objects:
        if hasattr(obj, 'bound_box'):
            for corner in obj.bound_box:
                world_corner = obj.matrix_world @ mathutils.Vector(corner)
                min_co.x = min(min_co.x, world_corner.x)
                min_co.y = min(min_co.y, world_corner.y)
                min_co.z = min(min_co.z, world_corner.z)
                max_co.x = max(max_co.x, world_corner.x)
                max_co.y = max(max_co.y, world_corner.y)
                max_co.z = max(max_co.z, world_corner.z)

    # Set ortho scale to fit with 15% padding
    height = max_co.z - min_co.z
    camera.data.ortho_scale = height * 1.3

    # Center camera vertically on the armature
    center_z = (min_co.z + max_co.z) / 2
    camera.location.z = center_z

    print(f"Auto-framed: height={height:.2f}m, ortho_scale={camera.data.ortho_scale:.2f}")


def main():
    # Parse arguments after "--" separator
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []

    parser = argparse.ArgumentParser(description="Render BVH motion as flat 2D pose reference frames")
    parser.add_argument("--bvh", required=True, help="Path to BVH motion file")
    parser.add_argument("--output-dir", required=True, help="Directory for rendered frame PNGs")
    parser.add_argument("--start", type=int, default=1, help="Start frame (default: 1)")
    parser.add_argument("--end", type=int, default=0, help="End frame (0 = auto from BVH, default: 0)")
    parser.add_argument("--fps", type=int, default=12, help="Frame rate (default: 12)")
    parser.add_argument("--camera-angle", default="front-3/4",
                        choices=list(CAMERA_PRESETS.keys()),
                        help="Camera preset (default: front-3/4)")
    parser.add_argument("--ortho-scale", type=float, default=0,
                        help="Override orthographic scale (0 = auto-frame)")
    parser.add_argument("--resolution", default="1920x1080",
                        help="Render resolution WxH (default: 1920x1080)")
    parser.add_argument("--background", default="green",
                        choices=["transparent", "green", "white"],
                        help="Background type (default: green)")
    parser.add_argument("--auto-frame", action="store_true", default=True,
                        help="Auto-adjust camera to frame the character (default: True)")

    args = parser.parse_args(argv)

    # Parse resolution
    res_parts = args.resolution.split("x")
    resolution = (int(res_parts[0]), int(res_parts[1]))

    print("=" * 60)
    print("Blender BVH Pose Reference Renderer")
    print("=" * 60)

    # 1. Clear and import
    clear_scene()
    armature = import_bvh(args.bvh, fps=args.fps)

    # 2. Auto-detect end frame if not specified
    end_frame = args.end
    if end_frame == 0:
        end_frame = int(bpy.context.scene.frame_end)
        print(f"Auto-detected end frame: {end_frame}")

    # 3. Setup scene
    camera = setup_camera(
        args.camera_angle,
        ortho_scale_override=args.ortho_scale if args.ortho_scale > 0 else None,
    )
    setup_lighting()
    build_skeleton_mesh(armature)
    setup_render(args.output_dir, resolution=resolution, background=args.background)

    # 4. Auto-frame if requested
    if args.auto_frame and args.ortho_scale == 0:
        # Sample a few frames to find the best framing
        bpy.context.scene.frame_set(args.start)
        auto_frame_armature(armature, camera)

    # 5. Render all frames
    print(f"\nRendering frames {args.start}-{end_frame} at {args.fps}fps...")
    render_frames(args.output_dir, args.start, end_frame)

    print("\n" + "=" * 60)
    print("Render complete.")
    print(f"Frames: {args.output_dir}/pose_F{{####}}.png")
    print(f"Next step: Feed these + A-2 reference to NB2 for pencil-test generation")
    print("=" * 60)


if __name__ == "__main__":
    main()
