#!/usr/bin/env python3
"""
THE HQ FLOOR PLAN — the spatial authority for the About-Me short.

Built 2026-08-31 at Sean's direction, after the S07 alarm plate came back reading
as if the CRT were next to Gemini's corner and nobody could say whether it was.

Why a plan and not another prose map: the cut all-corners wide already taught the
lesson the hard way — "FIVE LANES ALONG ONE WALL ARE NOT CORNERS. A corner needs
its own wall and depth." A left-to-right list cannot express that. A plan can, and
it is the only artifact that can be checked against a plate.

WHAT THIS IS DERIVED FROM. Every zone below is read off a plate that already exists
and is banked — the plan was fitted to the generated frames, not imposed on them,
because the frames are the ratified thing (DR #20: when an angle invents a zone,
that plate becomes the zone's bible).

    S04 rack       west wall, running south, turning the SW corner onto a board
    S05 moodboard  a long wall square to camera, a seam and a shelf at frame LEFT
    S06 dartboard  board flat on the wall, a seam at frame RIGHT, cabinet beyond
    S07 CRT        shelf at frame LEFT, seam, CRT high, a board at frame RIGHT

    Facing south, EAST is on your left. Facing east, SOUTH is on your right.
    Those two sentences are what fix the whole layout.

THE ONE THING THE PLAN PREDICTS AND THE PLATES DO NOT YET SHOW: the CRT hangs on
the east wall directly above the binder shelving that sits at the FAR LEFT of the
S05 moodboard frame. So the television belongs in S05's frame, small, top-left —
and it is missing from the plate we have. That is the continuity hole Sean spotted,
stated as geometry.

Renders to SVG + PNG, headless Chrome, $0 and re-runnable. Same idiom as
make_m1_guides.py: flat greyscale set, red for anything addressed to a human.
"""
import os
import subprocess

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1900, 1150
COL = 1476                             # x of the right-hand notes column

# ── the room, in feet, then in pixels ─────────────────────────────────────
# 26 ft x 18 ft break room. One foot = 44 px.
FT = 44
X0, Y0 = 268, 214                      # interior north-west corner
RW, RH = 26 * FT, 18 * FT              # 1144 x 792
X1, Y1 = X0 + RW, Y0 + RH
WALL = 16                              # wall thickness, drawn outside the interior

BG = "#f2f2f2"
FLOOR = "#e4e4e4"
WALLC = "#3a3a3a"
DARK, MID, LIGHT, FAINT = "#292929", "#606060", "#9d9d9d", "#c8c8c8"
CAP = "#c0392b"                        # red: notes to a human, never set content
CAM = "#1f6f8b"                        # teal: cameras, so they never read as props

s = []
add = s.append


def txt(x, y, t, size=17, fill=DARK, anchor="start", weight="400", style="normal"):
    return (f'<text x="{x}" y="{y}" font-family="Helvetica" font-size="{size}" '
            f'font-weight="{weight}" font-style="{style}" text-anchor="{anchor}" '
            f'fill="{fill}">{t}</text>')


def lab(x, y, t, size=15, fill=MID, anchor="middle"):
    """Uppercase tracked label — the plan's own voice."""
    return (f'<text x="{x}" y="{y}" font-family="Helvetica" font-size="{size}" '
            f'letter-spacing="1.6" text-anchor="{anchor}" fill="{fill}">{t}</text>')


def box(x, y, w, h, fill=LIGHT, stroke=MID, sw=2):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>')


def hatchwall(x, y, w, h, n=None, horiz=True):
    """A run of taped-up sheets / binders, drawn as tick marks against a wall."""
    o = box(x, y, w, h, FAINT, MID, 1.5)
    n = n or int((w if horiz else h) // 22)
    for i in range(n):
        if horiz:
            xx = x + 8 + i * ((w - 16) / max(n - 1, 1))
            o += f'<path d="M{xx:.0f} {y+3}v{h-6}" stroke="{LIGHT}" stroke-width="6"/>'
        else:
            yy = y + 8 + i * ((h - 16) / max(n - 1, 1))
            o += f'<path d="M{x+3} {yy:.0f}h{w-6}" stroke="{LIGHT}" stroke-width="6"/>'
    return o


def camera(cx, cy, deg, tag, note, reach=250, spread=31, flip=1):
    """A camera position and its view cone. Cones are the point of this plan:
    a zone list cannot tell you what a lens actually contains."""
    import math
    a = math.radians(deg)
    l = math.radians(deg - spread)
    r = math.radians(deg + spread)
    lx, ly = cx + reach * math.cos(l), cy + reach * math.sin(l)
    rx, ry = cx + reach * math.cos(r), cy + reach * math.sin(r)
    o = (f'<path d="M{cx} {cy}L{lx:.0f} {ly:.0f}L{rx:.0f} {ry:.0f}Z" fill="{CAM}" '
         f'fill-opacity="0.13" stroke="{CAM}" stroke-width="1.5" stroke-dasharray="7 5"/>')
    o += f'<circle cx="{cx}" cy="{cy}" r="13" fill="{CAM}"/>'
    o += txt(cx, cy + 5, tag, 13, "#ffffff", "middle", "700")
    o += txt(cx, cy + 34, note, 15, CAM, "middle", "700")
    return o


# ── ground ────────────────────────────────────────────────────────────────
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="{BG}"/>')
add(box(X0, Y0, RW, RH, FLOOR, "none", 0))
# walls drawn as four thick bars outside the interior
add(box(X0 - WALL, Y0 - WALL, RW + 2 * WALL, WALL, WALLC, "none", 0))   # N
add(box(X0 - WALL, Y1, RW + 2 * WALL, WALL, WALLC, "none", 0))          # S
add(box(X0 - WALL, Y0, WALL, RH, WALLC, "none", 0))                     # W
add(box(X1, Y0, WALL, RH, WALLC, "none", 0))                            # E

# floor tile grid, faint — the plates all show a tiled floor
for i in range(1, 26):
    add(f'<path d="M{X0+i*FT} {Y0}v{RH}" stroke="#dcdcdc" stroke-width="1"/>')
for i in range(1, 18):
    add(f'<path d="M{X0} {Y0+i*FT}h{RW}" stroke="#dcdcdc" stroke-width="1"/>')

# ── NORTH WALL ────────────────────────────────────────────────────────────
# Claude's nook — north-west
add(box(X0 + 10, Y0, 150, 46))                                   # supply desk
add(box(X0 + 172, Y0 + 6, 62, 62, MID))                          # paper tower (hero)
add(box(X0 + 244, Y0 + 10, 46, 46, MID))                         # second tower
add(hatchwall(X0 + 300, Y0, 118, 40, 6))                         # binder shelf
add(box(X0 + 120, Y0 + 62, 54, 40, FAINT))                       # file box on floor
add(lab(X0 + 210, Y0 + 130, "CLAUDE&#8217;S NOOK", 16, DARK))
add(lab(X0 + 210, Y0 + 150, "paper towers &#183; supply desk &#183; binders", 13))

# Sean's desk — dead centre of the north wall
DESKX = X0 + 500
add(box(DESKX, Y0, 250, 54, LIGHT, MID, 2))                      # desk
for i in range(3):                                               # three monitors
    add(box(DESKX + 16 + i * 78, Y0 + 4, 58, 14, MID))
add(f'<circle cx="{DESKX+125}" cy="{Y0+82}" r="24" fill="{DARK}"/>')   # Sean
add(txt(DESKX + 125, Y0 + 87, "S", 16, "#ffffff", "middle", "700"))
add(lab(DESKX + 125, Y0 + 138, "SEAN&#8217;S DESK", 16, DARK))
add(lab(DESKX + 125, Y0 + 158, "three monitors &#183; he faces NORTH, back to the room", 13))

# Grok's dartboard — north-east
GX = X0 + 850
add(f'<path d="M{GX+120} {Y0}a34 34 0 0 0 68 0" fill="none" stroke="{DARK}" stroke-width="4"/>')
add(lab(GX + 154, Y0 + 62, "dartboard", 12, DARK))
add(box(GX + 10, Y0 + 8, 96, 40, FAINT))                         # side table
add(box(GX + 230, Y0 + 6, 54, 44, MID))                          # crates
add(lab(GX + 150, Y0 + 130, "GROK&#8217;S DARTBOARD", 16, DARK))
add(lab(GX + 150, Y0 + 150, "darts in the WALL around it &#183; cans &#183; crates", 13))

# ── WEST WALL ─────────────────────────────────────────────────────────────
add(box(X0 - WALL, Y0 + 60, WALL, 132, BG, WALLC, 2))            # the doorway
add(lab(X0 - 40, Y0 + 132, "DOORWAY", 14, DARK, "end"))
add(lab(X0 - 40, Y0 + 152, "stays empty &#8212; the USER", 12, MID, "end"))
add(lab(X0 - 40, Y0 + 170, "is on the CRT, never here", 12, MID, "end"))

add(box(X0, Y0 + 290, 48, 168, DARK))                            # Codex's rack
add(box(X0, Y0 + 480, 44, 190, LIGHT))                           # counter, coffee
add(box(X0, Y0 + 690, 44, 62, FAINT))                            # water cooler
add(box(X0 + 70, Y0 + 560, 66, 66, FAINT))                       # armchair
add(lab(X0 + 190, Y0 + 470, "CODEX&#8217;S RACK", 16, DARK, "start"))
add(lab(X0 + 190, Y0 + 490, "server rack &#183; coffee counter &#183; cooler", 13, MID, "start"))
add(lab(X0 + 190, Y0 + 508, "the one corner proven end to end (S04)", 13, MID, "start"))

# ── EAST WALL ─────────────────────────────────────────────────────────────
add(hatchwall(X1 - 44, Y0 + 60, 44, 190, 8, horiz=False))        # binder shelving
add(box(X1 - 50, Y0 + 330, 50, 150, LIGHT))                      # credenza
add(f'<path d="M{X1-8} {Y0+368}l-46 34l46 34Z" fill="{DARK}"/>')  # the CRT, wall-mounted
add(lab(X1 - 70, Y0 + 528, "THE CRT", 16, DARK, "end"))
add(lab(X1 - 70, Y0 + 548, "high on the east wall,", 13, MID, "end"))
add(lab(X1 - 70, Y0 + 566, "above the binder shelving", 13, MID, "end"))
add(box(X1 - 44, Y0 + 560, 44, 60, FAINT))                       # cartons

# ── SOUTH WALL — Gemini's moodboard, long, wrapping the SE corner ─────────
add(hatchwall(X0 + 330, Y1 - 40, 700, 40, 26))
add(hatchwall(X1 - 40, Y1 - 190, 40, 150, 6, horiz=False))       # the SE wrap
add(box(X0 + 520, Y1 - 96, 210, 44, LIGHT))                      # worktable
add(box(X0 + 900, Y1 - 92, 60, 48, MID))                         # cartons of card
add(lab(X0 + 660, Y1 - 150, "GEMINI&#8217;S MOODBOARD", 16, DARK))
add(lab(X0 + 660, Y1 - 130, "fifty taped concepts &#183; string lights &#183; worktable", 13))
add(lab(X1 - 56, Y1 - 116, "the moodboard wraps the SE corner", 12, MID, "end"))

# ── the cameras ───────────────────────────────────────────────────────────
add(camera(X0 + 625, Y0 + 296, -90, "02", "SEAN, medium from behind", 258, 21))
add(camera(X0 + 246, Y0 + 328, -118, "03", "CLAUDE&#8217;S NOOK", 300, 26))
add(camera(X0 + 424, Y0 + 604, 178, "04", "CODEX&#8217;S RACK", 300, 28))
add(camera(X0 + 662, Y0 + 452, 90, "05", "GEMINI&#8217;S MOODBOARD", 340, 29))
add(camera(X0 + 878, Y0 + 300, -52, "06", "GROK&#8217;S DARTBOARD", 268, 25))
add(camera(X0 + 866, Y0 + 470, 6, "07", "THE CRT ALARM", 296, 26))

# ── the prediction, called out ───────────────────────────────────────────
add(f'<ellipse cx="{X1-34}" cy="{Y0+402}" rx="44" ry="58" fill="none" stroke="{CAP}" '
    f'stroke-width="3" stroke-dasharray="9 7"/>')
add(f'<path d="M{X1+14} {Y0+380} H{COL-16}" stroke="{CAP}" stroke-width="3" '
    f'stroke-dasharray="9 7"/>')
add(txt(COL, 470, "THE ONE THING THIS PLAN", 15, CAP, "start", "700"))
add(txt(COL, 490, "PREDICTS AND NO PLATE SHOWS", 15, CAP, "start", "700"))
for i, ln in enumerate([
        "S05 looks SOUTH at the moodboard,",
        "so EAST is its frame-LEFT &#8212; and the",
        "CRT hangs on the east wall right",
        "above the shelving that sits at that",
        "frame edge.",
        "",
        "So the television belongs in the",
        "Gemini plate: small, top-left, in the",
        "corner of frame. It is not there.",
        "",
        "That is the continuity hole, stated",
        "as geometry rather than as a worry &#8212;",
        "and it is also the fix for beat 3,",
        "because the alarm can then cut from",
        "a frame the TV is already in."]):
    add(txt(COL, 528 + i * 23, ln, 16, CAP if i < 5 else MID))

# ── compass, scale, titles ───────────────────────────────────────────────
CX, CY = COL + 60, 280
add(f'<circle cx="{CX}" cy="{CY}" r="42" fill="none" stroke="{MID}" stroke-width="2"/>')
add(f'<path d="M{CX} {CY+30}L{CX} {CY-32}" stroke="{DARK}" stroke-width="3"/>')
add(f'<path d="M{CX} {CY-40}l-9 18h18Z" fill="{DARK}"/>')
add(txt(CX, CY - 52, "N", 18, DARK, "middle", "700"))
add(txt(CX + 96, CY - 6, "26 ft &#215; 18 ft", 15, MID, "start"))
add(txt(CX + 96, CY + 16, "one foot = 44 px", 13, MID, "start"))

add(txt(52, 76, "THE HQ &#8212; FLOOR PLAN", 34, DARK, "start", "700"))
add(txt(52, 106, "About-Me short &#183; the spatial authority. Every zone here is read off a "
                 "plate that already exists; the plan was fitted to the frames, not imposed on them.",
        16, MID))
add(txt(52, 130, "Nothing moves between shots. When a new angle invents a zone, ratify that "
                 "plate first &#8212; it becomes the zone&#8217;s bible.", 16, MID))

# legend
LY = H - 96
add(txt(52, LY, "READ IT LIKE THIS", 15, DARK, "start", "700"))
add(f'<circle cx="62" cy="{LY+26}" r="11" fill="{CAM}"/>')
add(txt(82, LY + 31, "camera position; the dashed wedge is what that lens contains", 15, MID))
add(f'<rect x="52" y="{LY+46}" width="20" height="14" fill="{DARK}"/>')
add(txt(82, LY + 59, "solid = a fixture against a wall &#183; ticked panels = taped sheets or binders",
        15, MID))
add(f'<path d="M52 {LY+80}h20" stroke="{CAP}" stroke-width="3" stroke-dasharray="9 7"/>')
add(txt(82, LY + 86, "red = a note to a human, never set content", 15, CAP))
add(txt(W - 52, LY + 86, "make_floor_plan.py &#183; 2026-08-31", 14, MID, "end"))
add(txt(700, LY, "WHAT EACH CAMERA IS", 15, DARK, "start", "700"))
add(txt(700, LY + 26, "02 Sean, medium from behind &#183; 03 Claude&#8217;s nook &#183; 04 Codex&#8217;s rack (proven end to end)", 15, MID))
add(txt(700, LY + 48, "05 Gemini&#8217;s moodboard &#183; 06 Grok&#8217;s dartboard &#183; 07 the CRT alarm &#183; there is no establishing wide", 15, MID))

add("</svg>")
svg = "\n".join(s)

name = "M1-HQ-floor-plan"
with open(f"{OUT}/{name}.svg", "w") as f:
    f.write(svg)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
subprocess.run([CHROME, "--headless", "--disable-gpu",
                f"--screenshot={OUT}/{name}.png", f"--window-size={W},{H}",
                f"file://{OUT}/{name}.svg"], check=True, capture_output=True)
print(f"floor plan → {OUT}/{name}.png")
