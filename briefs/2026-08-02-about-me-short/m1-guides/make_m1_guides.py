#!/usr/bin/env python3
"""ABOUT-ME SHORT — Movement 1 "Quiet Morning" composition roughs.

Idiom + render path identical to FIRST LICKS' act1-guides/make_guides_v2.py
(headless Chrome — qlmanage forces square, do not use it).

Three beats across seven setups, per Sean's ruling 2026-08-30: beat 2's
"slow pan of the HQ" is NOT one continuous wide — it is the establishing
angle plus a cut to each mascot's own corner.

    S01  title card                      beat 1
    S02  HQ establishing wide, Sean      beat 2
    S03  Claude's tidy nook              beat 2
    S04  Codex's humming rack            beat 2   (plate banked, probe-205)
    S05  Gemini's string-lit moodboard   beat 2
    S06  Grok's dartboard                beat 2
    S07  the CRT alarm                   beat 3

SPATIAL PLACEMENT MAP (art-department DR #20) — the room, read as a clock
from the master angle S02. Every corner setup below is the same room with
the camera turned to that zone; nothing moves between shots.

        far left        left        CENTRE        right      far right
        doorway   →   Claude   →   Codex   →   SEAN    →  Gemini  →  Grok
        (the USER)     nook        rack        desk       moodboard  dartboard
                                                          CRT high above
                                                          on the right wall

    · Doorway is on the WEST wall, screen-left. The USER stands in it (M3).
    · Sean's desk + three monitors sit against the NORTH (back) wall, centre.
    · The CRT is wall-mounted HIGH on the right, above Gemini's moodboard,
      so the alarm can cut from any corner and stay oriented.
    · Grok's hole in the wall is the SOUTH-EAST corner; the rocket leans in it.
    · Ceiling pendant lamp hangs centre; string lights run along the right wall.

Ground line sits at y=700 in every setup so cuts do not jump the horizon.
"""
import os
import subprocess

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1536, 864
GY = 700                       # the shared ground line — never move it

BG, FLOOR = "#eeeeee", "#bcbcbc"
DARK, MID, LIGHT = "#292929", "#555555", "#9a9a9a"
FAINT, CAPTION = "#cfcfcf", "#c0392b"


def head(label):
    """label may carry ' || ' to force a line break; long labels wrap to 2 lines."""
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">\n<rect width="{W}" height="{H}" fill="{BG}"/>\n')
    if " || " in label:
        lines = label.split(" || ")
    elif len(label) > 78:
        cut = label.rfind(" ", 0, 82)
        lines = [label[:cut], label[cut + 1:]]
    else:
        lines = [label]
    ys = (844,) if len(lines) == 1 else (810, 846)
    tail = "".join(f'<text x="24" y="{y}" font-family="Helvetica" font-size="26" '
                   f'fill="{CAPTION}">{ln}</text>' for ln, y in zip(lines, ys))
    return s, tail + "\n</svg>"


# ── set primitives ────────────────────────────────────────────────────────
def floor(y=GY):
    return f'<path d="M0 {y}H{W}V{H}H0Z" fill="{FLOOR}"/>'


def corner(x, y=GY):
    """A wall/wall vertical seam — orients the viewer inside the room."""
    return f'<path d="M{x} 0V{y}" stroke="{LIGHT}" stroke-width="6"/>'


def pendant(cx, drop=150):
    return (f'<path d="M{cx} 0V{drop}" stroke="{MID}" stroke-width="6"/>'
            f'<path d="M{cx-62} {drop+52}Q{cx} {drop-26} {cx+62} {drop+52}Z" fill="{MID}"/>')


def stringlights(x0, x1, y, n=7):
    s = f'<path d="M{x0} {y}Q{(x0+x1)//2} {y+40} {x1} {y}" fill="none" stroke="{MID}" stroke-width="5"/>'
    for i in range(n):
        t = (i + 0.5) / n
        x = x0 + (x1 - x0) * t
        yy = y + 40 * (1 - (2 * t - 1) ** 2) * 0.75
        s += (f'<path d="M{x:.0f} {yy:.0f}v22" stroke="{MID}" stroke-width="4"/>'
              f'<circle cx="{x:.0f}" cy="{yy+30:.0f}" r="13" fill="{LIGHT}"/>')
    return s


def rack(cx, gy=GY, w=210, h=470):
    """Codex's humming server rack."""
    s = f'<rect x="{cx-w//2}" y="{gy-h}" width="{w}" height="{h}" fill="{DARK}"/>'
    for i in range(9):
        y = gy - h + 26 + i * (h - 40) // 9
        s += f'<rect x="{cx-w//2+16}" y="{y}" width="{w-32}" height="18" fill="{MID}"/>'
    return s


def moodboard(cx, cy=330, w=520, h=330):
    """Gemini's wall of taped-up sketches."""
    s = f'<rect x="{cx-w//2}" y="{cy-h//2}" width="{w}" height="{h}" fill="{FAINT}"/>'
    cols, rows = 5, 4
    cw, ch = w // cols, h // rows
    for r in range(rows):
        for c in range(cols):
            if (r * cols + c) % 7 == 3:
                continue
            x = cx - w // 2 + c * cw + 12
            y = cy - h // 2 + r * ch + 10
            s += f'<rect x="{x}" y="{y}" width="{cw-24}" height="{ch-20}" fill="{LIGHT}"/>'
    return s


def paperstack(cx, gy=GY, h=300, w=150):
    """Claude's tower of sticky-flagged pages, leaning."""
    s = ""
    n = 11
    for i in range(n):
        y = gy - (i + 1) * (h // n)
        lean = int(i * 2.2)
        s += (f'<rect x="{cx-w//2+lean}" y="{y}" width="{w}" height="{h//n-3}" '
              f'fill="{MID if i % 2 else LIGHT}"/>')
        if i % 3 == 0:
            s += f'<rect x="{cx+w//2+lean-8}" y="{y+3}" width="26" height="12" fill="{DARK}"/>'
    return s


def dartboard(cx, cy, r=78):
    s = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{LIGHT}"/>'
         f'<circle cx="{cx}" cy="{cy}" r="{r*0.6:.0f}" fill="{FLOOR}"/>'
         f'<circle cx="{cx}" cy="{cy}" r="{r*0.22:.0f}" fill="{DARK}"/>')
    for dx, dy in ((-150, -70), (-120, 90), (140, -40), (170, 80), (-40, -140)):
        s += (f'<path d="M{cx+dx} {cy+dy}l26 14" stroke="{DARK}" stroke-width="9" '
              f'stroke-linecap="round"/>')
    return s


def crt(cx, cy, w=300, h=230, alarm=False):
    """Corner-mounted CRT. alarm=True draws the PROBLEM! plate + falling graph."""
    s = (f'<path d="M{cx} {cy-h//2-70}v70" stroke="{MID}" stroke-width="7"/>'
         f'<rect x="{cx-w//2}" y="{cy-h//2}" width="{w}" height="{h}" rx="18" fill="{MID}"/>'
         f'<rect x="{cx-w//2+22}" y="{cy-h//2+20}" width="{w-44}" height="{h-52}" '
         f'fill="{BG if alarm else FAINT}"/>')
    if alarm:
        x0, y0 = cx - w // 2 + 40, cy - h // 2 + 44
        s += (f'<text x="{cx}" y="{y0+40}" font-family="Helvetica" font-size="42" '
              f'font-weight="bold" text-anchor="middle" fill="{DARK}">PROBLEM!</text>')
        s += (f'<path d="M{x0} {y0+66}L{x0+70} {y0+92}L{x0+130} {y0+80}L{x0+218} {y0+130}" '
              f'fill="none" stroke="{DARK}" stroke-width="9"/>')
        s += (f'<path d="M{x0+200} {y0+118}l20 14l-6-24" fill="{DARK}"/>')
    return s


def desk3mon(cx, gy=GY, w=430):
    """Sean's desk. Drawn in MID/LIGHT, never DARK: Sean sits in front of it and
    HE is the dark read. A dark desk swallows his silhouette."""
    s = f'<rect x="{cx-w//2}" y="{gy-150}" width="{w}" height="26" fill="{LIGHT}"/>'
    s += (f'<path d="M{cx-w//2+18} {gy-124}v124M{cx+w//2-18} {gy-124}v124" '
          f'stroke="{LIGHT}" stroke-width="14"/>')
    for i, dx in enumerate((-150, 0, 150)):
        mh = 118 if i == 1 else 100
        s += f'<rect x="{cx+dx-72}" y="{gy-150-mh}" width="144" height="{mh}" fill="{MID}"/>'
    return s


def mark(cx, text, y=None):
    """A named position mark under a figure. The guide should STATE placement,
    not imply it — the framing audit named 'scale is never stated in words' as
    the whole problem, and the same is true of position."""
    y = y or GY + 34
    return (f'<path d="M{cx} {GY-8}v16" stroke="{CAPTION}" stroke-width="4"/>'
            f'<text x="{cx}" y="{y}" font-family="Helvetica" font-size="21" '
            f'text-anchor="middle" fill="{CAPTION}">{text}</text>')


def doorway(x, gy=GY, w=170, h=380):
    return (f'<rect x="{x}" y="{gy-h}" width="{w}" height="{h}" fill="{FAINT}"/>'
            f'<rect x="{x}" y="{gy-h}" width="{w}" height="{h}" fill="none" '
            f'stroke="{MID}" stroke-width="8"/>')


# ── character silhouettes ─────────────────────────────────────────────────
# Shape language IS the identity at rough stage: cloud lobes, five-point star,
# bat ears, square plush, human. Heights are the cast-scale-lineup ratios —
# Sean 1.00, Grok 0.42, Codex 0.36, Gemini 0.30, Claude 0.26.
def sean(cx, gy=GY, h=340, back=False, lean=0):
    r = h * 0.15
    hcy = gy - h + r
    sh = hcy + r
    hip = gy - h * 0.42
    s = f'<circle cx="{cx+lean:.0f}" cy="{hcy:.0f}" r="{r:.0f}" fill="{DARK}"/>'
    s += (f'<path d="M{cx+lean-r*0.95:.0f} {sh:.0f} H{cx+lean+r*0.95:.0f} '
          f'L{cx+r*1.15:.0f} {hip:.0f} H{cx-r*1.15:.0f} Z" fill="{DARK}"/>')
    s += (f'<path d="M{cx-r*0.7:.0f} {hip:.0f}V{gy}M{cx+r*0.7:.0f} {hip:.0f}V{gy}" '
          f'stroke="{DARK}" stroke-width="{r*0.62:.0f}" stroke-linecap="round"/>')
    if not back:      # facing camera gets a pale face plate so the read is obvious
        s += f'<circle cx="{cx+lean:.0f}" cy="{hcy:.0f}" r="{r*0.42:.0f}" fill="{FLOOR}"/>'
    return s


def codex(cx, gy=GY, h=180):
    """Lobed cloud + two stubby legs."""
    bw = h * 0.92
    by = gy - h * 0.34
    s = ""
    for dx, dy, rr in ((-0.34, 0.06, 0.30), (-0.13, -0.16, 0.33), (0.13, -0.14, 0.32),
                       (0.34, 0.05, 0.29), (0.0, 0.10, 0.36)):
        s += (f'<circle cx="{cx+bw*dx:.0f}" cy="{by+bw*dy:.0f}" r="{bw*rr:.0f}" '
              f'fill="{DARK}"/>')
    s += (f'<path d="M{cx-h*0.16:.0f} {by+h*0.20:.0f}V{gy}M{cx+h*0.16:.0f} '
          f'{by+h*0.20:.0f}V{gy}" stroke="{DARK}" stroke-width="{h*0.15:.0f}" '
          f'stroke-linecap="round"/>')
    return s


def gemini(cx, gy=GY, h=150):
    """Five-point star with a flopping top point + two legs."""
    body = h * 0.68
    cy = gy - h + body * 0.55
    pts = []
    import math
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rad = body * 0.62 if i % 2 == 0 else body * 0.28
        pts.append(f"{cx + rad*math.cos(a):.0f},{cy + rad*math.sin(a):.0f}")
    s = f'<polygon points="{" ".join(pts)}" fill="{DARK}"/>'
    s += f'<circle cx="{cx}" cy="{cy:.0f}" r="{body*0.40:.0f}" fill="{DARK}"/>'
    s += (f'<path d="M{cx-h*0.13:.0f} {cy+body*0.34:.0f}V{gy}M{cx+h*0.13:.0f} '
          f'{cy+body*0.34:.0f}V{gy}" stroke="{DARK}" stroke-width="{h*0.13:.0f}" '
          f'stroke-linecap="round"/>')
    return s


def grok(cx, gy=GY, h=210):
    """Round gremlin, big bat ears, tail."""
    r = h * 0.34
    cy = gy - h + r * 1.15
    s = (f'<path d="M{cx-r*1.02:.0f} {cy-r*0.30:.0f}L{cx-r*2.05:.0f} {cy-r*1.55:.0f}'
         f'L{cx-r*0.62:.0f} {cy-r*1.12:.0f}Z" fill="{DARK}"/>'
         f'<path d="M{cx+r*1.02:.0f} {cy-r*0.30:.0f}L{cx+r*2.05:.0f} {cy-r*1.55:.0f}'
         f'L{cx+r*0.62:.0f} {cy-r*1.12:.0f}Z" fill="{DARK}"/>')
    s += f'<circle cx="{cx}" cy="{cy:.0f}" r="{r:.0f}" fill="{DARK}"/>'
    s += (f'<path d="M{cx-r*0.52:.0f} {cy+r*0.80:.0f}V{gy}M{cx+r*0.52:.0f} '
          f'{cy+r*0.80:.0f}V{gy}" stroke="{DARK}" stroke-width="{r*0.42:.0f}" '
          f'stroke-linecap="round"/>')
    s += (f'<path d="M{cx+r*0.92:.0f} {cy+r*0.55:.0f}q{r*0.9:.0f} {r*0.35:.0f} '
          f'{r*0.5:.0f} {r*1.05:.0f}" fill="none" stroke="{DARK}" '
          f'stroke-width="{r*0.20:.0f}" stroke-linecap="round"/>')
    return s


def claude(cx, gy=GY, h=130):
    """Squarish terracotta plush, stubby limbs, side nubs."""
    bw, bh = h * 0.72, h * 0.66
    x, y = cx - bw / 2, gy - h
    s = (f'<rect x="{x:.0f}" y="{y:.0f}" width="{bw:.0f}" height="{bh:.0f}" '
         f'rx="{bw*0.16:.0f}" fill="{DARK}"/>')
    s += (f'<rect x="{x-bw*0.19:.0f}" y="{y+bh*0.44:.0f}" width="{bw*0.19:.0f}" '
          f'height="{bh*0.22:.0f}" rx="6" fill="{DARK}"/>'
          f'<rect x="{x+bw:.0f}" y="{y+bh*0.44:.0f}" width="{bw*0.19:.0f}" '
          f'height="{bh*0.22:.0f}" rx="6" fill="{DARK}"/>')
    s += (f'<path d="M{cx-bw*0.26:.0f} {y+bh:.0f}V{gy}M{cx+bw*0.26:.0f} {y+bh:.0f}V{gy}" '
          f'stroke="{DARK}" stroke-width="{bw*0.26:.0f}" stroke-linecap="round"/>')
    return s


# ── the seven setups ──────────────────────────────────────────────────────
shots = {}

# S01 — the title card. Typography, not blocking: this one is a layout rough.
s, tail = head("M1-S01 — TITLE CARD · beat 1, 4s · the film's only card · "
               "1950s 'HOW TO' plate, dead centre, held still || the card is the "
               "straight man: nothing moves, so the alarm later has something to break")
b = s + f'<rect x="150" y="210" width="{W-300}" height="340" fill="{FAINT}"/>'
b += (f'<text x="{W//2}" y="382" font-family="Helvetica" font-size="76" font-weight="bold" '
      f'text-anchor="middle" fill="{DARK}">HOW TO SOLVE</text>')
b += (f'<text x="{W//2}" y="472" font-family="Helvetica" font-size="76" font-weight="bold" '
      f'text-anchor="middle" fill="{DARK}">A PROBLEM</text>')
b += f'<path d="M{W//2-190} 512H{W//2+190}" stroke="{MID}" stroke-width="7"/>'
shots["M1-S01-titlecard-guide"] = b + tail

# S02 — Sean at his desk, MEDIUM. Replaces the all-corners wide, cut 2026-08-30.
# Sean's ruling: in the wide the mascots clustered near centre and all faced camera,
# so it contradicted the per-corner premise it was meant to establish. The film now
# opens on Sean working and cuts out to each corner — Goofy grammar: establish almost
# nothing, let each character own its own frame.
s, tail = head("M1-S02 — SEAN AT THE DESK · beat 2 · MEDIUM, from behind · he is typing, "
               "absorbed, unhurried || he fills the frame and the room falls away — no "
               "corner is established here; every mascot gets its own shot instead")
CX, DESK = W // 2, 660          # desk edge crosses the lower frame
b = s
b += f'<path d="M0 214H{W}" stroke="{LIGHT}" stroke-width="5"/>'      # one quiet wall line
# monitors stand ON the desk, behind him
b += f'<rect x="{CX-118}" y="300" width="236" height="176" rx="8" fill="{MID}"/>'
b += f'<rect x="{CX-392}" y="330" width="228" height="150" rx="8" fill="{LIGHT}"/>'
b += f'<rect x="{CX+164}" y="330" width="228" height="150" rx="8" fill="{LIGHT}"/>'
# chair back behind him
b += f'<rect x="{CX-176}" y="452" width="352" height="230" rx="26" fill="{LIGHT}"/>'
# SEAN, seated, from behind — head + shoulders only; the desk crops him
b += f'<circle cx="{CX}" cy="392" r="104" fill="{DARK}"/>'
b += (f'<path d="M{CX-172} {DESK} Q{CX-158} 486 {CX-96} 470 H{CX+96} '
      f'Q{CX+158} 486 {CX+172} {DESK} Z" fill="{DARK}"/>')
# arms reaching forward to the keyboard
b += (f'<path d="M{CX-150} 540 L{CX-96} {DESK-24} M{CX+150} 540 L{CX+96} {DESK-24}" '
      f'stroke="{DARK}" stroke-width="46" stroke-linecap="round"/>')
b += f'<path d="M0 {DESK}H{W}V{H}H0Z" fill="{FLOOR}"/>'               # desk surface
b += f'<rect x="{CX-160}" y="{DESK+26}" width="320" height="30" rx="9" fill="{MID}"/>'  # keyboard
b += (f'<text x="{CX}" y="188" font-family="Helvetica" font-size="21" '
      f'text-anchor="middle" fill="{CAPTION}">wall kept EMPTY — no corner, no clutter</text>')
b += (f'<text x="{CX}" y="{DESK-176}" font-family="Helvetica" font-size="21" '
      f'text-anchor="middle" fill="{CAPTION}">SEAN · seated, back to camera, typing</text>')
shots["M1-S02-sean-desk-medium-guide"] = b + tail

# S03 — Claude's tidy nook.
s, tail = head("M1-S03 — CLAUDE'S NOOK · beat 2 · the tidy corner: everything squared, "
               "flagged, alphabetised || he is MID-BIT — adding one more flag to a stack "
               "already taller than he is. Earnest, not comic.")
b = s + floor() + corner(1120)
b += paperstack(430, h=330, w=170) + paperstack(640, h=250, w=140)
b += f'<rect x="820" y="{GY-120}" width="260" height="120" fill="{MID}"/>'
b += claude(268, h=196)
b += (f'<text x="268" y="{GY-232}" font-family="Helvetica" font-size="22" '
      f'text-anchor="middle" fill="{CAPTION}">reaching up</text>')
shots["M1-S03-claude-nook-guide"] = b + tail

# S04 — Codex's humming rack. The banked probe plate matches this setup.
s, tail = head("M1-S04 — CODEX'S RACK · beat 2 · PLATE + 7s CLIP ALREADY BANKED "
               "(probe-205) || mid-bit: hammering the rack, body squashing on every "
               "strike. The one corner already proven end to end.")
b = s + floor() + corner(980)
b += rack(340, w=230, h=500)
b += f'<rect x="600" y="{GY-150}" width="300" height="150" fill="{MID}"/>'
b += moodboard(1290, cy=320, w=420, h=300)
b += codex(560, h=210)
shots["M1-S04-codex-rack-guide"] = b + tail

# S05 — Gemini's string-lit moodboard.
s, tail = head("M1-S05 — GEMINI'S MOODBOARD · beat 2 · the wall of fifty concepts, "
               "string lights above || mid-bit: taping up yet another one, already "
               "bouncing to the next. Delight, never mania.")
b = s + floor() + corner(240)
b += moodboard(900, cy=340, w=760, h=420) + stringlights(540, 1270, 130, n=9)
b += gemini(400, h=230)
b += (f'<text x="400" y="{GY-265}" font-family="Helvetica" font-size="22" '
      f'text-anchor="middle" fill="{CAPTION}">arm up, taping</text>')
shots["M1-S05-gemini-moodboard-guide"] = b + tail

# S06 — Grok's dartboard corner.
s, tail = head("M1-S06 — GROK'S DARTBOARD · beat 2 · darts in the WALL around the board, "
               "not in it || mid-bit: mid-throw, grinning. The misses are the joke and "
               "they are already on the wall before he throws.")
b = s + floor() + corner(1230)
b += dartboard(1000, 330, r=92)
b += f'<rect x="1250" y="{GY-260}" width="240" height="260" fill="{FAINT}"/>'
b += grok(430, h=290)
b += (f'<text x="430" y="{GY-352}" font-family="Helvetica" font-size="22" '
      f'text-anchor="middle" fill="{CAPTION}">mid-throw, arm back</text>')
shots["M1-S06-grok-dartboard-guide"] = b + tail

# S07 — the CRT alarm. Beat 3.
s, tail = head("M1-S07 — THE ALARM · beat 3, 3s · CRT flicks on: PROBLEM! over the "
               "falling CHECKOUT graph || dead-stop hold, then burst. The CRT is HIGH on "
               "the right wall (see S02) so this cut stays oriented.")
b = s + floor() + corner(420)
b += crt(880, 300, w=520, h=400, alarm=True)
b += (f'<text x="880" y="560" font-family="Helvetica" font-size="24" '
      f'text-anchor="middle" fill="{CAPTION}">CHECKOUT COMPLETIONS</text>')
b += moodboard(1330, cy=300, w=340, h=260)
shots["M1-S07-alarm-guide"] = b + tail


# ── write + render ────────────────────────────────────────────────────────
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

for name, svg in shots.items():
    with open(f"{OUT}/{name}.svg", "w") as f:
        f.write(svg)
    subprocess.run([CHROME, "--headless", "--disable-gpu",
                    f"--screenshot={OUT}/{name}.png", "--window-size=1536,864",
                    f"file://{OUT}/{name}.svg"], check=True, capture_output=True)

print(f"{len(shots)} roughs → {OUT}")
for n in sorted(shots):
    print("  ", n)
