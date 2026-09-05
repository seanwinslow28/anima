#!/usr/bin/env python3
"""
SHOT ROUGHS — the room, projected through each camera.

The last piece of the chain. make_room_bible.py holds the only description of the
set; this file puts a lens in it and renders what that lens actually contains, so a
corner rough can no longer disagree with the plan it came from. Hand-drawn roughs
could, and did.

    ground plan  →  elevations  →  THESE  →  corner plates  →  characters  →  motion

Straight pinhole projection of axis-aligned boxes. Camera position, heading and
horizontal field of view come from the ground plan; eye level is 5'6" unless a shot
says otherwise. Each fixture is drawn as the convex hull of its eight projected
corners — a silhouette, which is all a composition rough owes anybody — with the
walls and floor behind it and the room's vertical corner seams on top.

Two things this buys that a hand-drawn rough does not:

  1. A corner shot is now GEOMETRICALLY the corner. S03 sees the west wall meeting
     the north wall because the camera is standing where the plan says it is, not
     because someone drew two rectangles and hoped.
  2. Re-cameraing a shot is a one-line edit. Change the yaw, re-run, $0.

Coordinates: x east 0-26, y south 0-18 (y=0 IS the north wall), z up 0-10.
Headings match the ground plan's convention — 0 = east, 90 = south, -90 = north.

── MOVEMENT 2 CANDIDATES, 2026-09-03 ──────────────────────────────────────
Sean's ruling (2026-09-02): no cutting back to a corner in the same angle unless
the frame is visibly wrecked and the motion is chaotic. So every M2 wrong-build
beat needs a camera DECISION, and he cannot judge one from prose. m2_candidates.py
holds the candidate cameras; `python make_shot_roughs.py` roughs them into
m2-candidates/, $0, for his eye.

Two additive per-shot keys, both optional, both inert on the M1 SHOTS (whose
six roughs stay byte-identical — checked by md5 on 2026-09-03):

  state="B"   draw the Movement-2 additions from WALLS (the red rows: THE CODE
              WALL, THE HOLE) as red-outlined blocks. Default "A" skips them.
  cast=[...]  stand the cast in the room as green blocks at their real heights
              (Sean 6.0 ft; Grok 0.42 / Codex 0.36 / Gemini 0.30 / Claude 0.26
              of him). They are silhouettes for SCALE and PLACEMENT, not
              drawings. Green so they never read as fixtures.
  on_cast=True  include the cast blocks in what the lens is solved on, for a
              shot whose subject is the people rather than the furniture.
"""
import math
import os
import subprocess

from make_room_bible import WALLS, ROOM_W_FT, ROOM_D_FT, ROOM_H_FT, render, CAP

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1536, 864
EYE = 5.5

WALLTONE, FLOORTONE = "#f4f4f4", "#e2e2e2"
SEAM, EDGE = "#b4b4b4", "#606060"
M2FILL = "#f3c9c4"                         # Movement-2 additions: pale red block, red edge
CASTFILL, CASTEDGE = "#bfe3cf", "#2e8b57"  # cast silhouettes: green, never a fixture

SEAN_FT = 6.0
RATIO = dict(sean=1.00, grok=0.42, codex=0.36, gemini=0.30, claude=0.26)


def who(tag, x, y, h=None, w=None, seated=False):
    """One cast member as a block: footprint centred on (x, y), real height."""
    if h is None:
        h = 4.3 if seated else SEAN_FT * RATIO[tag]
    if w is None:
        w = 0.42 * h if tag == "sean" else 0.8 * h
    return dict(tag=tag, x=x, y=y, h=h, w=w)


# Where everyone stands at rest, read off the approved M1 composites.
REST = dict(
    sean=who("sean", 13.5, 3.4, seated=True),
    claude=who("claude", 1.7, 3.6),
    codex=who("codex", 2.0, 12.9),
    gemini=who("gemini", 8.8, 16.6),
    grok=who("grok", 23.6, 3.4),
)

SHOTS = {
    "S02": dict(pos=(13.5, 11.0), pitch=-3, eye=4.6, fill=0.62,
                on=["SEAN&#8217;S DESK", "corkboard"],
                title="SEAN&#8217;S STATION &#183; medium from behind"),
    "S03": dict(pos=(8.0, 7.6), pitch=-3, fill=0.86,
                on=["supply desk", "PAPER TOWER", "second stack", "binder shelf"],
                title="CLAUDE &#183; the NW corner"),
    "S04": dict(pos=(9.5, 9.0), pitch=-3, fill=0.86,
                on=["SERVER RACK", "coffee counter", "water cooler"],
                title="CODEX &#183; the SW corner"),
    "S05": dict(pos=(13.5, 3.0), pitch=-4, fill=0.80,
                on=["GEMINI&#8217;S MOODBOARD", "worktable"],
                title="GEMINI&#8217;S MOODBOARD &#183; square on"),
    "S06": dict(pos=(17.5, 7.2), pitch=-3, fill=0.82,
                on=["side table", "DARTBOARD", "crates"],
                title="GROK &#183; the NE corner"),
    "S07": dict(pos=(15.0, 12.0), pitch=1, eye=5.2, fill=0.74,
                on=["BINDER SHELVING", "credenza", "THE CRT"],
                title="THE CRT ALARM"),
}


def boxes(named=False):
    """Every fixture as (x0,x1, y0,y1, z0,z1, fill). One source of truth."""
    out = []
    for key, wl in WALLS.items():
        for it in wl["items"]:
            if it["red"]:                     # Movement 2 additions stay off the M1 rough
                continue
            a, b, d = it["a"], it["b"], it["depth"]
            z0, z1 = it["sill"], it["sill"] + it["h"]
            if key == "north":
                bx = (a, b, 0.0, d, z0, z1)
            elif key == "south":
                bx = (a, b, ROOM_D_FT - d, ROOM_D_FT, z0, z1)
            elif key == "west":
                bx = (0.0, d, a, b, z0, z1)
            else:
                bx = (ROOM_W_FT - d, ROOM_W_FT, a, b, z0, z1)
            out.append((bx, it["fill"] or "#ffffff", it["name"]) if named
                       else (bx, it["fill"] or "#ffffff"))
    return out


def m2_boxes():
    """The Movement-2 additions only — the red rows of WALLS."""
    out = []
    for key, wl in WALLS.items():
        for it in wl["items"]:
            if not it["red"]:
                continue
            a, b, d = it["a"], it["b"], it["depth"]
            z0, z1 = it["sill"], it["sill"] + it["h"]
            if key == "north":
                bx = (a, b, 0.0, d, z0, z1)
            elif key == "south":
                bx = (a, b, ROOM_D_FT - d, ROOM_D_FT, z0, z1)
            elif key == "west":
                bx = (0.0, d, a, b, z0, z1)
            else:
                bx = (ROOM_W_FT - d, ROOM_W_FT, a, b, z0, z1)
            out.append((bx, M2FILL, it["name"]))
    return out


def cast_boxes(cast):
    """Cast members as upright blocks, footprint centred on their floor spot."""
    out = []
    for c in cast:
        hw = c["w"] / 2
        out.append(((c["x"] - hw, c["x"] + hw, c["y"] - hw, c["y"] + hw, 0.0, c["h"]),
                    CASTFILL, c["tag"]))
    return out


NEAR = 0.35


def subject_boxes(names):
    """The boxes a shot is ABOUT, matched by fixture name."""
    out = []
    for bx, fill, nm in boxes(named=True):
        for n in names:
            if n.lower() in nm.lower():
                out.append(bx)
                break
    return out


def aim(pos, names, fill, eye, pitch_bias=0.0, extra=()):
    """Solve heading, PITCH and field of view from the subject.

    Pitch has to be solved, not chosen. From 10 ft away with the lens at 5'6",
    keeping the foot of a wall in frame needs either an ~89-degree lens or a camera
    that tilts down like a real one. Two earlier passes tried to fix it with field
    of view alone and produced shots that were all crop, then shots that were all
    wide-angle. Aim at the subject's centre, then open the lens just enough."""
    cx, cy = pos
    bxs = subject_boxes(names) + [bx for bx, _, nm in m2_boxes()
                                  if any(n.lower() in nm.lower() for n in names)]
    bxs += list(extra)
    pts = [(x, y, z)
           for x0, x1, y0, y1, z0, z1 in bxs
           for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    ax = sum(p[0] for p in pts) / len(pts)
    ay = sum(p[1] for p in pts) / len(pts)
    az = sum(p[2] for p in pts) / len(pts)
    yaw = math.atan2(ay - cy, ax - cx)
    flat = math.hypot(ax - cx, ay - cy)
    pitch = math.atan2(az - eye, flat) + math.radians(pitch_bias)

    cyaw, syaw = math.cos(yaw), math.sin(yaw)
    cp, sp = math.cos(pitch), math.sin(pitch)
    halfh = halfv = 0.0
    for px, py, pz in pts:
        vx, vy, vz = px - cx, py - cy, pz - eye
        fwd = vx * cyaw * cp + vy * syaw * cp + vz * sp
        if fwd <= NEAR:
            continue
        u = -vx * syaw + vy * cyaw
        v = -vx * cyaw * sp - vy * syaw * sp + vz * cp
        halfh = max(halfh, abs(math.atan2(u, fwd)))
        halfv = max(halfv, abs(math.atan2(v, fwd)))
    hf = 2 * halfh / max(fill, 0.2)
    hf_from_v = 2 * math.atan(math.tan(halfv) * 16 / 9)      # vertical: just fits
    hfov = min(max(math.degrees(max(hf, hf_from_v)), 28.0), 86.0)
    return math.degrees(yaw), math.degrees(pitch), hfov


def make(name, shot):
    """Project the room through one lens.

    Geometry behind the camera is CLIPPED, never clamped. The first version clamped
    depth to a small positive number, and every box with a corner behind the lens
    projected to something enormous — six frames of solid grey. Near-plane clipping
    in camera space is the fix and it is the only fiddly part of this file."""
    cx, cy = shot["pos"]
    ch = shot.get("eye", EYE)
    cast = shot.get("cast", [])
    extra = [bx for bx, _, _ in cast_boxes(cast)] if shot.get("on_cast") else []
    yaw_deg, pitch_deg, hfov = aim(shot["pos"], shot["on"], shot.get("fill", 0.75),
                                   ch, shot.get("pitch", 0), extra)
    shot["_solved"] = dict(yaw=round(yaw_deg, 1), pitch=round(pitch_deg, 1),
                           hfov=round(hfov, 1))
    yaw, pitch = math.radians(yaw_deg), math.radians(pitch_deg)
    f = (W / 2) / math.tan(math.radians(hfov) / 2)
    # A level camera at eye height puts the floor line below frame in a room this
    # size — the wall fills everything and the shot reads as a wallpaper swatch.
    # Real cameras tilt. Pitch is negative for down.
    fw = (math.cos(yaw) * math.cos(pitch), math.sin(yaw) * math.cos(pitch), math.sin(pitch))
    rt = (-math.sin(yaw), math.cos(yaw), 0.0)
    up = (fw[1] * rt[2] - fw[2] * rt[1],       # fw x rt, NOT rt x fw:
          fw[2] * rt[0] - fw[0] * rt[2],       # the other order points DOWN and
          fw[0] * rt[1] - fw[1] * rt[0])       # renders the whole room upside down

    def cam(p):
        """World → camera space: (right, up, forward)."""
        v = (p[0] - cx, p[1] - cy, p[2] - ch)
        return (v[0] * rt[0] + v[1] * rt[1] + v[2] * rt[2],
                v[0] * up[0] + v[1] * up[1] + v[2] * up[2],
                v[0] * fw[0] + v[1] * fw[1] + v[2] * fw[2])

    def clip_near(poly):
        """Sutherland-Hodgman against forward >= NEAR."""
        out = []
        n = len(poly)
        for i in range(n):
            a1, b1 = poly[i], poly[(i + 1) % n]
            in1, in2 = a1[2] >= NEAR, b1[2] >= NEAR
            if in1:
                out.append(a1)
            if in1 != in2:
                t = (NEAR - a1[2]) / (b1[2] - a1[2])
                out.append((a1[0] + t * (b1[0] - a1[0]),
                            a1[1] + t * (b1[1] - a1[1]), NEAR))
        return out

    def screen(poly, fill, stroke=EDGE, sw=2):
        c = clip_near([cam(p) for p in poly])
        if len(c) < 3:
            return "", 0.0
        pts = " ".join(f"{W/2 + u/d*f:.1f},{H/2 - v/d*f:.1f}" for u, v, d in c)
        mean = sum(d for _, _, d in c) / len(c)
        return (f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" '
                f'stroke-width="{sw}" stroke-linejoin="round"/>'), mean

    def faces(bx):
        x0, x1, y0, y1, z0, z1 = bx
        return [
            [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],   # -y
            [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)],   # +y
            [(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)],   # -x
            [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)],   # +x
            [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)],   # top
        ]

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<clipPath id="fr"><rect width="{W}" height="{H}"/></clipPath>',
         '<g clip-path="url(#fr)">']
    a = s.append

    shell = [([(0, 0, 0), (ROOM_W_FT, 0, 0), (ROOM_W_FT, ROOM_D_FT, 0),
               (0, ROOM_D_FT, 0)], FLOORTONE),
             ([(0, 0, 0), (ROOM_W_FT, 0, 0), (ROOM_W_FT, 0, ROOM_H_FT),
               (0, 0, ROOM_H_FT)], WALLTONE),
             ([(0, ROOM_D_FT, 0), (ROOM_W_FT, ROOM_D_FT, 0),
               (ROOM_W_FT, ROOM_D_FT, ROOM_H_FT), (0, ROOM_D_FT, ROOM_H_FT)], WALLTONE),
             ([(0, 0, 0), (0, ROOM_D_FT, 0), (0, ROOM_D_FT, ROOM_H_FT),
               (0, 0, ROOM_H_FT)], WALLTONE),
             ([(ROOM_W_FT, 0, 0), (ROOM_W_FT, ROOM_D_FT, 0),
               (ROOM_W_FT, ROOM_D_FT, ROOM_H_FT), (ROOM_W_FT, 0, ROOM_H_FT)], WALLTONE)]
    drawn = []
    for poly, fill in shell:
        svg, m = screen(poly, fill, SEAM, 1)
        if svg:
            drawn.append((m, svg))
    for _, svg in sorted(drawn, key=lambda t: -t[0]):
        a(svg)

    items = []
    drawlist = [(bx, fill, EDGE, 2) for bx, fill in boxes()]
    if shot.get("state", "A") == "B":
        drawlist += [(bx, fill, CAP, 3) for bx, fill, _ in m2_boxes()]
    if shot.get("draw_cast", True):
        drawlist += [(bx, fill, CASTEDGE, 3) for bx, fill, _ in cast_boxes(cast)]
    for bx, fill, stroke, sw in drawlist:
        fs = []
        for fc in faces(bx):
            svg, m = screen(fc, fill, stroke, sw)
            if svg:
                fs.append((m, svg))
        if fs:
            items.append((min(m for m, _ in fs), fs))
    for _, fs in sorted(items, key=lambda t: -t[0]):
        for _, svg in sorted(fs, key=lambda t: -t[0]):
            a(svg)

    for p in ((0, 0), (ROOM_W_FT, 0), (ROOM_W_FT, ROOM_D_FT), (0, ROOM_D_FT)):
        c0, c1 = cam((p[0], p[1], 0.0)), cam((p[0], p[1], float(ROOM_H_FT)))
        if c0[2] < NEAR or c1[2] < NEAR:
            continue
        x1s, y1s = W / 2 + c0[0] / c0[2] * f, H / 2 - c0[1] / c0[2] * f
        x2s, y2s = W / 2 + c1[0] / c1[2] * f, H / 2 - c1[1] / c1[2] * f
        if -300 < x1s < W + 300:
            a(f'<path d="M{x1s:.0f} {y1s:.0f}L{x2s:.0f} {y2s:.0f}" stroke="{SEAM}" '
              f'stroke-width="4"/>')

    a("</g></svg>")
    render(f"{shot.get('dir', '')}SHOT-{name}-rough", "\n".join(s), W, H)


M2DIR = "m2-candidates/"

if __name__ == "__main__":
    import sys
    print(f"shot roughs → {OUT}")
    if "m2" not in sys.argv:                       # `m2` = candidates only
        for n, sh in SHOTS.items():
            make(n, sh)
    if "m1" not in sys.argv:                       # `m1` = the six M1 roughs only
        os.makedirs(os.path.join(OUT, M2DIR), exist_ok=True)
        from m2_candidates import M2
        for n, sh in M2.items():
            sh.setdefault("state", "B")
            sh.setdefault("dir", M2DIR)
            make(n, sh)
            print("     ", n, sh["_solved"])
            # The PLATE rough: identical camera (the cast still steers the solve), cast
            # not drawn. This is the file a plate prompt hands to the generator.
            make(n + "-plate", dict(sh, draw_cast=False))
