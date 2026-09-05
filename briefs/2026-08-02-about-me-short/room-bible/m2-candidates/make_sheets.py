#!/usr/bin/env python3
"""
CONTACT SHEETS for the Movement-2 camera candidates — one sheet per beat, $0.

Each sheet puts the locked Movement-1 frame of that corner ("what the audience
already saw") beside the three candidate roughs, so Sean compares a repeat against
each alternative with his eye instead of reading about it. A LEAN badge marks the
session's recommendation; it is a proposal, not a decision.

Also draws every candidate camera onto the ground plan (camera-map.png).
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
RB = os.path.dirname(HERE)                       # room-bible/
BRIEF = os.path.dirname(RB)                      # the brief dir
sys.path.insert(0, RB)
from m2_candidates import M2                     # noqa: E402
from make_shot_roughs import aim, cast_boxes     # noqa: E402

PAPER, PAPER2, INK, INK2, RULE = "#f5e8d1", "#ecdcbf", "#2c2a26", "#6b6459", "#c9b998"
LEAN, GREEN, RED = "#b93a2b", "#2e8b57", "#c0392b"
FONT = "/System/Library/Fonts/Helvetica.ttc"


def font(size, bold=False):
    return ImageFont.truetype(FONT, size, index=1 if bold else 0)


TILE_W, TILE_H, CAP_H, GAP, PAD = 760, 428, 118, 24, 28
LEANS = {"B3h": "A", "B4": "A", "B5": "A", "B6": "A", "B7": "B", "B8": "A"}
SHEETS = [
    ("B3h", "3½ · THE ROOM REACTS", "the CRT's own point of view · room state A (nothing wrecked yet)",
     "normalised/S07-plate-v2.png", "BEAT 3 · the alarm, as the audience saw it (S07)"),
    ("B4", "4 · THE SILENT GO", "Sean turned to the room · the mascots look to him · state A",
     "normalised/S02-sean-composite-v1.png", "BEAT 2 · Sean's station, the S02 camera (locked) — his back"),
    ("B5", "5 · CLAUDE'S 40-PAGE DOCUMENT", "the NW corner, escalated · paper past the top of frame",
     "normalised/S03-claude-composite-frontal-v1.png", "BEAT 2 · Claude's nook, the S03 camera (locked)"),
    ("B6", "6 · CODEX REBUILDS EVERYTHING", "the code wall lit over the counter · ten thousand lines",
     "normalised/S04-codex-composite-frontal-v1.png", "BEAT 2 · Codex's rack, the S04 camera (locked)"),
    ("B7", "7 · GEMINI'S FIFTY CONCEPTS", "the moodboard, escalated · concepts on every surface",
     "normalised/S05-gemini-composite-frontal-v1.png", "BEAT 2 · Gemini's board, the S05 camera (locked)"),
    ("B8", "8 · GROK DEMOLISHES THE WALL", "THE HOLE in the NE corner · the rocket leans out",
     "normalised/S06-grok-composite-frontal-v1.png", "BEAT 2 · Grok's corner, the S06 camera (locked)"),
]


def fit(img, w, h):
    im = Image.open(img).convert("RGB")
    im.thumbnail((w, h), Image.LANCZOS)
    canvas = Image.new("RGB", (w, h), PAPER2)
    canvas.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    return canvas


def wrap(draw, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def tile(sheet, x, y, img, letter, title, note, lean=False, ref=False):
    d = ImageDraw.Draw(sheet)
    sheet.paste(fit(img, TILE_W, TILE_H), (x, y))
    d.rectangle([x, y, x + TILE_W - 1, y + TILE_H - 1], outline=RULE, width=2)
    # caption band
    cy = y + TILE_H + 10
    if ref:
        d.text((x, cy), "WHAT THE AUDIENCE SAW", font=font(15, True), fill=INK2)
        d.text((x, cy + 24), title, font=font(20), fill=INK)
        return
    d.text((x, cy - 4), letter, font=font(44, True), fill=INK)
    tx = x + 62
    d.text((tx, cy), title, font=font(21, True), fill=INK)
    ny = cy + 30
    for ln in wrap(d, note, font(17), TILE_W - 62 - (110 if lean else 0))[:3]:
        d.text((tx, ny), ln, font=font(17), fill=INK2)
        ny += 21
    if lean:
        bw, bh = 92, 30
        bx, by = x + TILE_W - bw, cy + 2
        d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=4, fill=LEAN)
        d.text((bx + 14, by + 6), "LEAN", font=font(16, True), fill=PAPER)


def sheet_for(key, head, sub, refimg, refcap):
    cols, rows = 2, 2
    W = PAD * 2 + cols * TILE_W + (cols - 1) * GAP
    H = PAD * 2 + 96 + rows * (TILE_H + CAP_H) + (rows - 1) * GAP
    s = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(s)
    d.text((PAD, PAD), head, font=font(34, True), fill=INK)
    d.text((PAD, PAD + 44), sub, font=font(19), fill=INK2)
    d.text((W - PAD - 470, PAD + 4), "camera roughs · $0 · make_shot_roughs.py", font=font(15), fill=INK2)
    d.text((W - PAD - 470, PAD + 26), "green = cast at real scale · red = M2 fixture", font=font(15), fill=INK2)
    d.line([PAD, PAD + 78, W - PAD, PAD + 78], fill=RULE, width=2)
    slots = [(PAD, PAD + 96), (PAD + TILE_W + GAP, PAD + 96),
             (PAD, PAD + 96 + TILE_H + CAP_H + GAP), (PAD + TILE_W + GAP, PAD + 96 + TILE_H + CAP_H + GAP)]
    tile(s, *slots[0], os.path.join(BRIEF, refimg), "", refcap, "", ref=True)
    cands = [k for k in M2 if k.startswith(key + "-")]
    for (x, y), k in zip(slots[1:], cands):
        letter = k.split("-")[1]
        title, _, note = M2[k]["note"].partition(" — ")
        tile(s, x, y, os.path.join(HERE, f"SHOT-{k}-rough.png"), letter, title, note,
             lean=(LEANS[key] == letter))
    out = os.path.join(HERE, "sheets", f"{key}-sheet.jpg")
    s.save(out, quality=88)
    print(" ", out)


def camera_map():
    """Every candidate camera on the ground plan. X0/Y0/FT are the plan's own constants."""
    X0, Y0, FT = 268, 214, 44
    im = Image.open(os.path.join(RB, "ROOM-01-ground-plan.png")).convert("RGB")
    d = ImageDraw.Draw(im)
    colours = {"B3h": "#1f6f8b", "B4": "#3f6b4f", "B5": "#b7791f", "B6": "#6a5580",
               "B7": "#8c4a6b", "B8": RED}
    for k, sh in M2.items():
        beat = k.split("-")[0]
        col = colours[beat]
        cx, cy = X0 + sh["pos"][0] * FT, Y0 + sh["pos"][1] * FT
        cast = sh.get("cast", [])
        extra = [bx for bx, _, _ in cast_boxes(cast)] if sh.get("on_cast") else []
        yaw, _, hfov = aim(sh["pos"], sh["on"], sh.get("fill", 0.75), sh.get("eye", 5.5),
                           sh.get("pitch", 0), extra)
        for sgn in (-1, 1):
            a = math.radians(yaw + sgn * hfov / 2)
            d.line([cx, cy, cx + 110 * math.cos(a), cy + 110 * math.sin(a)], fill=col, width=2)
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=col)
        lab = k.replace("B3h-", "3½-").replace("B4-", "4-").replace("B5-", "5-") \
               .replace("B6-", "6-").replace("B7-", "7-").replace("B8-", "8-")
        d.text((cx - d.textlength(lab, font=font(12, True)) / 2, cy - 7), lab,
               font=font(12, True), fill="#ffffff")
        for c in cast:
            px, py = X0 + c["x"] * FT, Y0 + c["y"] * FT
            d.ellipse([px - 5, py - 5, px + 5, py + 5], outline=GREEN, width=2)
    d.rectangle([1480, 990, 1880, 1175], fill="#f2f2f2")
    d.text((1490, 1006), "M2 CANDIDATE CAMERAS", font=font(15, True), fill=INK)
    d.text((1490, 1030), "dot = lens · lines = solved field of view", font=font(13), fill=INK2)
    d.text((1490, 1050), "green rings = where the cast stands", font=font(13), fill=INK2)
    yy = 1076
    for beat, col in colours.items():
        d.ellipse([1490, yy, 1504, yy + 14], fill=col)
        d.text((1512, yy - 1), {"B3h": "3½ the room reacts", "B4": "4 the silent GO", "B5": "5 Claude",
                                "B6": "6 Codex", "B7": "7 Gemini", "B8": "8 Grok"}[beat],
               font=font(13), fill=INK)
        yy += 17
    out = os.path.join(HERE, "sheets", "camera-map.jpg")
    im.save(out, quality=88)
    print(" ", out)


if __name__ == "__main__":
    for args in SHEETS:
        sheet_for(*args)
    camera_map()
