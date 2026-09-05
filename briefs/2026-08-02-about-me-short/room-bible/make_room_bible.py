#!/usr/bin/env python3
"""
THE ROOM BIBLE — ground plan + unrolled wall elevations for the whole film.

Built 2026-08-31 at Sean's direction, replacing the Movement-1-only floor plan.

WHY, in his words: "In 2D animation, everything is fully planned out, full extended
rooms are drawn, character turnarounds are drawn, then the scenes, individual
characters, and sectioned off backgrounds get drawn out and created separately and
then composited." And: plan the FULL LIFECYCLE of the room, Movements 1 through 3,
"instead of doing half and then having to circle back."

── REVISION 2, 2026-08-31 afternoon. EVERYONE GETS A CORNER. ─────────────
Sean, on rev 1: "Everything is very close together, so trying to crop out corners
might look awkward. Sean's station is on the north wall, Claude is on the north west
corner (left of Sean) and Grok is on the north east corner (right of Sean). Everyone
should have their own respective sections without completely overlapping on one wall."

He is right, and it is the lesson the cut all-corners wide already taught: FIVE LANES
ALONG ONE WALL ARE NOT CORNERS — a corner needs its own wall and depth. Rev 1 still
had Claude, Sean and Grok sharing the north wall, which is a lane arrangement wearing
a corner's name. So:

    NORTH  Sean's station alone, plus neutral office overflow at the ends
    WEST   Claude's nook at the NORTH end, the doorway, Codex's rack at the SOUTH end
    EAST   Grok's dartboard at the NORTH end, then the CRT, then the moodboard wrap
    SOUTH  Gemini's moodboard, long

S03 and S06 become genuine two-wall corner shots. S04 keeps the SW corner and S05
stays square to the south wall.

Sean also settled the doorway: it stays dressing. The USER lives on the CRT, and Sean
asks the question AT HIS COMPUTER rather than at a door — "that fits better with the
theme of no dialogue and just VO, music, and sound effects anyway." That puts beats 2,
4, 12 and 13 all at the same setup, which makes his station the film's most-used angle.
It is drawn to earn that.

── WHAT WENT WRONG WITHOUT A BIBLE ───────────────────────────────────────
Corners were generated independently and continuity checked afterwards, which makes
continuity something you CATCH rather than something TRUE BY CONSTRUCTION:

  1. Codex's rack and Gemini's moodboard claimed the same end of the same wall.
  2. The CRT was two fixtures — near the ceiling in one plate, at shelf height in
     another, and a different television in each.
  3. Gemini stood on the baseboard, because the composite prompt had lost the
     "soft graphite contact shadow" clause the proven S04 prompt carried.

An elevation fixes 1 and 2 by construction. 3 was a prompt regression, fixed there.

── ONE SOURCE OF TRUTH ───────────────────────────────────────────────────
WALLS below is the only place a fixture is described. The ground plan draws it from
above using its depth, the elevations draw it from the front using its height, and the
bare roughs draw it for the generator. Rev 1 kept two copies and they had already
started to disagree — the same failure mode, one level up.

ROOM STATES. Movement-2 additions are drawn in red on both sheets:
  A QUIET  M1 beats 1-3   the room as drawn
  B CHAOS  M2 beats 5-9   code wall lit, concepts everywhere, THE HOLE at the NE
                          corner with the rocket leaning out, the bell rung hollow
  C AFTER  M3             still wrecked, but calm

$0, deterministic, re-runnable.
"""
import math
import os
import subprocess

OUT = os.path.dirname(os.path.abspath(__file__))
ROOM_W_FT, ROOM_D_FT, ROOM_H_FT = 26, 18, 10

BG, FLOORC = "#f2f2f2", "#e4e4e4"
WALLC = "#3a3a3a"
DARK, MID, LIGHT, FAINT = "#292929", "#606060", "#9d9d9d", "#c8c8c8"
CAP = "#c0392b"          # red: a note to a human, or a Movement-2 addition
CAM = "#1f6f8b"          # teal: cameras, so they never read as props
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def F(a, b, h, sill, depth, name, detail, fill=LIGHT, red=0, plan=True):
    """One fixture. a/b run west→east on N and S walls, north→south on W and E.
    plan=False for anything sitting ON another fixture — monitors, a corkboard —
    so it does not double-draw as its own footprint on the ground plan."""
    return dict(a=a, b=b, h=h, sill=sill, depth=depth, name=name, detail=detail,
                fill=fill, red=red, plan=plan)


WALLS = {
    "north": dict(
        length=ROOM_W_FT, label="NORTH WALL &#183; 26&#8242;",
        sub="SEAN&#8217;S STATION, alone on this wall. Seen in S02 &#8212; and in beats "
            "4, 12 and 13, which makes it the film&#8217;s most-used angle.",
        items=[
            F(0.5, 4.0, 5.0, 0, 1.5, "filing cabinet", "boxes and a tired plant on top", FAINT),
            F(5.2, 9.0, 2.4, 0, 1.5, "printer bench", "printer, paper trays", LIGHT),
            F(5.0, 9.2, 4.0, 3.0, 0.2, "whiteboard", "half-erased diagrams", "#ffffff",
              plan=False),
            F(10.0, 17.0, 2.5, 0, 2.5, "SEAN&#8217;S DESK", "he sits facing north", LIGHT),
            F(10.9, 16.1, 1.6, 2.5, 0.6, "three monitors", "quiet lines of code", MID,
              plan=False),
            F(10.6, 16.4, 3.4, 4.6, 0.2, "corkboard + shelf",
              "notes, binders, trailing plant, cable run", FAINT, plan=False),
            F(18.0, 19.0, 1.0, 6.4, 0.6, "SHIP IT bell",
              "bracket + pull cord &#183; hollow at beat 9, earned at 17", MID),
            F(19.6, 21.0, 1.6, 0, 1.2, "confetti cannon", "tripod &#183; misfires at beat 9", MID),
            F(22.0, 25.5, 2.2, 0, 1.5, "storage bench", "boxes, coat rack above", FAINT),
        ]),
    "west": dict(
        length=ROOM_D_FT, label="WEST WALL &#183; 18&#8242;",
        sub="CLAUDE&#8217;S NOOK at the north end, the doorway, then CODEX&#8217;S RACK at "
            "the south end. Seen in S03 (NW corner) and S04 (SW corner).",
        items=[
            F(0.4, 2.4, 2.6, 0, 1.8, "supply desk", "jar of pens, stapler", LIGHT),
            F(2.7, 3.9, 5.6, 0, 1.4, "PAPER TOWER", "flagged, leaning, the hero prop", MID),
            F(4.1, 5.0, 3.4, 0, 1.0, "second stack", "shorter, also flagged", MID),
            F(5.3, 7.3, 6.2, 0, 1.2, "binder shelf", "squared and labelled", FAINT),
            F(8.0, 10.8, 7.0, 0, 0.3, "DOORWAY", "empty &#8212; dressing only", "#ffffff"),
            F(11.5, 12.6, 7.4, 0, 2.5, "SERVER RACK", "status lights, loose cabling", DARK),
            F(12.9, 15.8, 3.0, 0, 2.0, "coffee counter", "machine, jug, mugs", LIGHT),
            F(13.1, 15.6, 2.6, 4.2, 0.4, "THE CODE WALL", "M2 beat 6 &#183; scrolling code",
              None, red=1, plan=False),
            F(16.3, 17.7, 4.2, 0, 1.4, "water cooler", "and paper cups", FAINT),
        ]),
    "east": dict(
        length=ROOM_D_FT, label="EAST WALL &#183; 18&#8242;",
        sub="GROK&#8217;S DARTBOARD at the north end, then THE CRT, then the moodboard "
            "wrapping in. Seen in S06 (NE corner) and S07.",
        items=[
            F(0.4, 2.6, 2.2, 0, 2.0, "side table", "crushed cans, a mug", FAINT),
            F(2.2, 3.9, 1.7, 3.8, 0.3, "DARTBOARD", "face clean, darts in the WALL around it",
              LIGHT, plan=False),
            F(4.2, 5.5, 2.4, 0, 1.6, "crates", "stacked", MID),
            F(0.0, 2.0, 6.4, 0, 0.4, "THE HOLE", "M2 beat 8 &#183; the rocket leans out",
              None, red=1),
            F(6.5, 9.8, 7.0, 0, 1.2, "BINDER SHELVING", "tall, full", FAINT),
            F(10.5, 13.1, 3.0, 0, 1.6, "credenza", "paper trays, a mug", LIGHT),
            F(10.7, 12.9, 2.5, 6.5, 1.4, "THE CRT",
              "ONE fixture &#183; bracket + cable down", MID, plan=False),
            F(14.5, 18.0, 6.6, 1.6, 0.2, "moodboard wraps", "the SE corner", FAINT),
        ]),
    "south": dict(
        length=ROOM_W_FT, label="SOUTH WALL &#183; 26&#8242;",
        sub="GEMINI&#8217;S MOODBOARD, long. Seen in S05, and its west end appears at "
            "frame-LEFT of S04.",
        items=[
            F(0.4, 4.6, 3.2, 0, 1.6, "storage cabinet", "west end", FAINT),
            F(0.6, 4.4, 1.4, 3.2, 1.4, "cartons", "stacked on top", MID, plan=False),
            F(6.0, 22.0, 6.6, 1.6, 0.2, "GEMINI&#8217;S MOODBOARD",
              "~50 taped product and mascot concepts", FAINT),
            F(6.4, 21.6, 0.4, 8.4, 0.5, "string lights", "swagged above the board", LIGHT,
              plan=False),
            F(9.5, 14.1, 2.4, 0, 1.6, "worktable", "tape, markers, mug", LIGHT),
            F(22.0, 26.0, 6.6, 1.6, 0.2, "board wraps SE", "round the corner", FAINT),
        ]),
}


def txt(x, y, t, size=17, fill=DARK, anchor="start", weight="400"):
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-family="Helvetica" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">{t}</text>')


def lab(x, y, t, size=14, fill=MID, anchor="middle"):
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-family="Helvetica" font-size="{size}" '
            f'letter-spacing="1.5" text-anchor="{anchor}" fill="{fill}">{t}</text>')


def box(x, y, w, h, fill=LIGHT, stroke=MID, sw=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'fill="{fill if fill else "none"}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def render(name, svg, w, h):
    with open(f"{OUT}/{name}.svg", "w") as f:
        f.write(svg)
    subprocess.run([CHROME, "--headless", "--disable-gpu",
                    f"--screenshot={OUT}/{name}.png", f"--window-size={w},{h}",
                    f"file://{OUT}/{name}.svg"], check=True, capture_output=True)
    print(f"  {name}.png")


# ══════════════════════════════════════════════════════════════════════════
def ground_plan():
    W, H = 1900, 1200
    COL, FT = 1476, 44
    X0, Y0 = 268, 214
    RW, RH = ROOM_W_FT * FT, ROOM_D_FT * FT
    X1, Y1 = X0 + RW, Y0 + RH
    WALL = 16
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="{BG}"/>']
    a = s.append

    a(box(X0, Y0, RW, RH, FLOORC, "none", 0))
    a(box(X0 - WALL, Y0 - WALL, RW + 2 * WALL, WALL, WALLC, "none", 0))
    a(box(X0 - WALL, Y1, RW + 2 * WALL, WALL, WALLC, "none", 0))
    a(box(X0 - WALL, Y0, WALL, RH, WALLC, "none", 0))
    a(box(X1, Y0, WALL, RH, WALLC, "none", 0))
    for i in range(1, ROOM_W_FT):
        a(f'<path d="M{X0+i*FT} {Y0}v{RH}" stroke="#dcdcdc" stroke-width="1"/>')
    for i in range(1, ROOM_D_FT):
        a(f'<path d="M{X0} {Y0+i*FT}h{RW}" stroke="#dcdcdc" stroke-width="1"/>')

    for key, wl in WALLS.items():
        for it in wl["items"]:
            if not it["plan"]:
                continue
            L, D = (it["b"] - it["a"]) * FT, it["depth"] * FT
            if key == "north":
                x, y, w, h = X0 + it["a"] * FT, Y0, L, D
            elif key == "south":
                x, y, w, h = X0 + it["a"] * FT, Y1 - D, L, D
            elif key == "west":
                x, y, w, h = X0, Y0 + it["a"] * FT, D, L
            else:
                x, y, w, h = X1 - D, Y0 + it["a"] * FT, D, L
            red = it["red"]
            a(box(x, y, w, h, None if red else it["fill"], CAP if red else MID,
                  3 if red else 2, dash="9 7" if red else None))

    a(f'<circle cx="{X0+13.5*FT:.0f}" cy="{Y0+3.4*FT:.0f}" r="{0.55*FT:.0f}" fill="{DARK}"/>')
    a(txt(X0 + 13.5 * FT, Y0 + 3.55 * FT, "S", 16, "#ffffff", "middle", "700"))

    zones = [(13.5, 5.2, "SEAN&#8217;S STATION",
              "desk, monitors, board &#183; bell and cannon to his right"),
             (5.8, 2.4, "CLAUDE &#183; NW CORNER",
              "paper towers &#183; supply desk &#183; binders"),
             (20.4, 2.4, "GROK &#183; NE CORNER",
              "darts in the WALL &#183; cans &#183; crates"),
             (6.6, 14.4, "CODEX &#183; SW CORNER",
              "rack &#183; coffee counter &#183; cooler"),
             (13.8, 15.4, "GEMINI&#8217;S MOODBOARD",
              "fifty taped concepts &#183; string lights &#183; worktable"),
             (21.8, 9.6, "THE CRT", "sill 6&#8242;6&#8243; above the credenza")]
    for xf, yf, t1, t2 in zones:
        a(lab(X0 + xf * FT, Y0 + yf * FT, t1, 15, DARK))
        a(lab(X0 + xf * FT, Y0 + (yf + 0.45) * FT, t2, 12))

    a(lab(X0 + 1.6 * FT, Y0 + 9.4 * FT, "DOORWAY &#8212; dressing only", 12, MID, "start"))
    a(lab(X0 + 25.2 * FT, Y0 + 4.6 * FT, "M2 &#183; THE HOLE", 12, CAP, "end"))
    a(lab(X0 + 25.2 * FT, Y0 + 5.0 * FT, "beat 8 &#183; rocket leans out", 11, CAP, "end"))

    def camera(xf, yf, deg, tag, note, reach=250, spread=29):
        cx, cy = X0 + xf * FT, Y0 + yf * FT
        l, r = math.radians(deg - spread), math.radians(deg + spread)
        o = (f'<path d="M{cx:.0f} {cy:.0f}L{cx+reach*math.cos(l):.0f} '
             f'{cy+reach*math.sin(l):.0f}L{cx+reach*math.cos(r):.0f} '
             f'{cy+reach*math.sin(r):.0f}Z" fill="{CAM}" fill-opacity="0.13" '
             f'stroke="{CAM}" stroke-width="1.5" stroke-dasharray="7 5"/>')
        o += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="13" fill="{CAM}"/>'
        o += txt(cx, cy + 5, tag, 13, "#ffffff", "middle", "700")
        o += txt(cx, cy + 34, note, 15, CAM, "middle", "700")
        return o

    a(camera(13.5, 8.4, -90, "02", "SEAN&#8217;S STATION", 250, 20))
    a(camera(6.8, 7.6, -140, "03", "CLAUDE &#183; NW corner", 270, 27))
    a(camera(7.2, 10.6, 198, "04", "CODEX &#183; SW corner", 250, 27))
    a(camera(14.6, 9.8, 92, "05", "GEMINI&#8217;S MOODBOARD", 290, 27))
    a(camera(19.4, 7.8, -42, "06", "GROK &#183; NE corner", 260, 27))
    a(camera(18.8, 12.2, 4, "07", "THE CRT ALARM", 250, 24))

    CX, CY = COL + 60, 280
    a(f'<circle cx="{CX}" cy="{CY}" r="42" fill="none" stroke="{MID}" stroke-width="2"/>')
    a(f'<path d="M{CX} {CY+30}L{CX} {CY-32}" stroke="{DARK}" stroke-width="3"/>')
    a(f'<path d="M{CX} {CY-40}l-9 18h18Z" fill="{DARK}"/>')
    a(txt(CX, CY - 52, "N", 18, DARK, "middle", "700"))
    a(txt(CX + 96, CY - 6, f"{ROOM_W_FT} ft &#215; {ROOM_D_FT} ft", 15, MID))
    a(txt(CX + 96, CY + 16, f"ceiling {ROOM_H_FT} ft &#183; 1 ft = {FT} px", 13, MID))

    a(txt(COL, 430, "EVERYONE GETS A CORNER", 15, CAP, "start", "700"))
    for i, ln in enumerate([
            "Revision 2. Rev 1 still had Claude, Sean",
            "and Grok sharing the north wall &#8212; which",
            "is a LANE arrangement wearing a corner&#8217;s",
            "name, and lanes are what killed the cut",
            "all-corners wide.",
            "",
            "Now Sean holds the north wall alone.",
            "Claude wraps the NW corner off the west",
            "wall; Grok wraps the NE corner off the",
            "east wall. S03 and S06 become genuine",
            "two-wall corner shots with real depth.",
            "",
            "The doorway stays dressing. Sean asks the",
            "question at his computer, not at a door,",
            "so beats 2, 4, 12 and 13 all play at this",
            "one station &#8212; and it is drawn to earn",
            "that screen time.",
            "",
            "RED = Movement 2. The hole, the code wall,",
            "the bell and the cannon are all here from",
            "the start so no later beat has to invent a",
            "fixture the room never had."]):
        a(txt(COL, 466 + i * 23, ln, 16, CAP if i < 5 else MID))

    LY = H - 96
    a(txt(52, 76, "THE HQ &#183; SHEET 1 &#8212; GROUND PLAN", 34, DARK, "start", "700"))
    a(txt(52, 106, "The room bible, revision 2. One source of truth: this sheet and the "
                   "elevations are drawn from the same table.", 16, MID))
    a(txt(52, 130, "Nothing moves between shots, and nothing appears in a later beat that is "
                   "not on these sheets.", 16, MID))
    a(txt(52, LY, "READ IT LIKE THIS", 15, DARK, "start", "700"))
    a(f'<circle cx="62" cy="{LY+26}" r="11" fill="{CAM}"/>')
    a(txt(82, LY + 31, "camera position; the dashed wedge is what that lens contains", 15, MID))
    a(f'<rect x="52" y="{LY+46}" width="20" height="14" fill="{DARK}"/>')
    a(txt(82, LY + 59, "solid = a fixture against a wall, drawn from above at its real depth",
          15, MID))
    a(f'<path d="M52 {LY+80}h20" stroke="{CAP}" stroke-width="3" stroke-dasharray="9 7"/>')
    a(txt(82, LY + 86, "red = a Movement 2 addition, or a note to a human", 15, CAP))
    a(txt(W - 52, LY + 86, "make_room_bible.py &#183; rev 2 &#183; 2026-08-31", 14, MID, "end"))
    a("</svg>")
    render("ROOM-01-ground-plan", "\n".join(s), W, H)


# ══════════════════════════════════════════════════════════════════════════
def elevations():
    PX = 40
    LEFT, TOP = 150, 300
    WALL_H = ROOM_H_FT * PX
    ROW = WALL_H + 316
    W, H = 1460, TOP + 4 * ROW + 90
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="{BG}"/>']
    a = s.append

    def wall(idx, key, marks):
        wl = WALLS[key]
        items = wl["items"]
        y1 = TOP + idx * ROW + WALL_H
        y0 = y1 - WALL_H
        x0 = LEFT
        w = wl["length"] * PX
        a(txt(x0, y0 - 52, wl["label"], 25, DARK, "start", "700"))
        a(txt(x0, y0 - 28, wl["sub"], 15, MID))
        a(box(x0, y0, w, WALL_H, "#ffffff", WALLC, 3))
        a(f'<path d="M{x0} {y1}h{w}" stroke="{WALLC}" stroke-width="6"/>')
        for hft, note, col in ((5.5, "eye 5&#8242;6&#8243;", MID),
                               (6.5, "CRT sill 6&#8242;6&#8243;", CAP)):
            yy = y1 - hft * PX
            a(f'<path d="M{x0} {yy:.0f}h{w}" stroke="{col}" stroke-width="1" '
              f'stroke-dasharray="6 8" opacity="0.5"/>')
            a(txt(x0 - 12, yy + 5, note, 12, col, "end"))
        a(box(x0, y1 - 0.5 * PX, w, 0.5 * PX, FAINT, MID, 1.5))

        for i, it in enumerate(items, 1):
            col = CAP if it["red"] else MID
            x = x0 + it["a"] * PX
            bw = (it["b"] - it["a"]) * PX
            y = y1 - (it["sill"] + it["h"]) * PX
            a(box(x, y, bw, it["h"] * PX, None if it["red"] else it["fill"], col,
                  3 if it["red"] else 2, dash="9 7" if it["red"] else None))
            bx, by = x + 15, y + 17
            a(f'<circle cx="{bx}" cy="{by}" r="11" fill="{col}"/>')
            a(txt(bx, by + 5, str(i), 13, "#ffffff", "middle", "700"))

        yy = y1 + 26
        a(f'<path d="M{x0} {yy}h{w}" stroke="{MID}" stroke-width="1"/>')
        for m in marks:
            a(f'<path d="M{x0+m*PX:.0f} {yy-5}v10" stroke="{MID}" stroke-width="1"/>')
            a(txt(x0 + m * PX, yy + 20, f"{m}&#8242;", 11, MID, "middle"))
        a(txt(x0 + w + 14, y1, f'{wl["length"]}&#8242;', 15, MID))
        a(txt(x0 - 12, y0 + 6, f"{ROOM_H_FT}&#8242;", 12, MID, "end"))

        ky, colw = y1 + 92, 432
        per = -(-len(items) // 3)
        for i, it in enumerate(items, 1):
            c, r = (i - 1) // per, (i - 1) % per
            kx, yy2 = x0 + c * colw, ky + r * 25
            col = CAP if it["red"] else MID
            a(f'<circle cx="{kx+11}" cy="{yy2-5}" r="10" fill="{col}"/>')
            a(txt(kx + 11, yy2, str(i), 12, "#ffffff", "middle", "700"))
            hgt = f'{it["h"]:g}&#8242;h' + (f' @ {it["sill"]:g}&#8242;' if it["sill"] else "")
            body = (f'<tspan font-weight="700" fill="{CAP if it["red"] else DARK}">'
                    f'{it["name"]}</tspan>  {it["a"]:g}&#8211;{it["b"]:g}&#8242; '
                    f'&#183; {hgt}' + (f' &#183; {it["detail"]}' if it["detail"] else ''))
            a(f'<text x="{kx+28:.0f}" y="{yy2:.0f}" font-family="Helvetica" font-size="12" '
              f'fill="{col}">{body}</text>')

    wall(0, "north", [0, 4, 8, 12, 16, 20, 26])
    wall(1, "west", [0, 4, 8, 12, 18])
    wall(2, "east", [0, 4, 8, 12, 18])
    wall(3, "south", [0, 4, 8, 12, 16, 20, 26])

    a(txt(52, 78, "THE HQ &#183; SHEET 2 &#8212; WALL ELEVATIONS", 34, DARK, "start", "700"))
    a(txt(52, 110, "All four walls unrolled, flat, at one scale. Every fixture has one wall, "
                   "one left-to-right position and one height.", 16, MID))
    a(txt(52, 136, "A corner plate is a CROP OF A WALL &#8212; or, for S03 and S06, of two "
                   "walls meeting. Two plates can no longer contradict each other.", 16, MID))
    a(txt(52, 168, "RED = Movement 2, drawn now so no later beat has to invent a fixture the "
                   "room never had.", 16, CAP))
    a(txt(52, 194, "Eye level 5&#8242;6&#8243; is the horizon every plate sits on. The CRT "
                   "sill at 6&#8242;6&#8243; is the number both earlier CRT plates got wrong "
                   "&#8212; one had it near the ceiling, one at shelf height.", 15, MID))
    a(txt(W - 52, H - 40, "make_room_bible.py &#183; rev 2 &#183; 2026-08-31", 14, MID, "end"))
    a("</svg>")
    render("ROOM-02-elevations", "\n".join(s), W, H)


# ══════════════════════════════════════════════════════════════════════════
def wall_roughs():
    """Bare per-wall composition roughs. Fixtures only: no numbers, no guides, no
    key. A generator handed guide marks draws the guide marks."""
    PX, PAD = 46, 60
    for key, wl in WALLS.items():
        w, hh = wl["length"] * PX, ROOM_H_FT * PX
        W, H = w + 2 * PAD, hh + 2 * PAD
        s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="#ffffff"/>']
        a = s.append
        x0, y1 = PAD, PAD + hh
        a(box(x0, PAD, w, hh, "#ffffff", "#000000", 3))
        a(f'<path d="M{x0} {y1}h{w}" stroke="#000000" stroke-width="6"/>')
        a(box(x0, y1 - 0.5 * PX, w, 0.5 * PX, FAINT, MID, 2))
        for it in wl["items"]:
            if it["red"]:
                continue
            a(box(x0 + it["a"] * PX, y1 - (it["sill"] + it["h"]) * PX,
                  (it["b"] - it["a"]) * PX, it["h"] * PX,
                  it["fill"] if it["fill"] else "#ffffff", MID, 2))
        a("</svg>")
        render(f"ROOM-ELEV-{key}-rough", "\n".join(s), W, H)


print(f"room bible → {OUT}")
ground_plan()
elevations()
wall_roughs()
