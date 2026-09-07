#!/usr/bin/env python3
"""
FILM ROUGH CUT — all three movements, every locked clip, at the beat sheet's timings, so the
film can be judged as a film (and read against with a stopwatch). $0, deterministic. Sibling
of m3_roughcut.py, which only ever cut Movement 3; this is the first assembly of the whole
piece. Every clip stays intact in _LOCKED-M*/ — this file only TRIMS.

Two edits live here, chosen with --variant:

  v7   the M3 rough cut v6 carried forward + M1 and M2 cut for the first time, with the two
       post-kickoff fixes: beat 12 now cuts at 5.6s (the eyes begin opening at ~5.7s, not the
       FACE sheet's ~6.2s — v6's 5.9s out-point caught them), and the pit stop is 4.8s (v6's
       1.3+1.3+1.3+1.4 = 5.3s was over the ≤5s floor).
  v8   the trim lean from GAPS/story check (2026-09-07): Movement 2 and the head of Movement 3
       give, the swivel / replay / pit stop floors do not. This is the edit that puts the typed
       question back near the 60s bar.

Each segment's label carries its running-start timecode, so a frame grab reads as a stopwatch
lap. The beat table (start / duration / end per beat) prints to stdout and is written beside
the mp4 as <out>.beats.md.

    Usage:  film_roughcut.py <out.mp4> [--variant v7|v8] [--movement 1|2|3|all]
"""
import os, subprocess, sys, tempfile

FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
W, H, FPS = 1280, 720, 24
M1, M2, M3 = "_LOCKED-M1/", "_LOCKED-M2/", "_LOCKED-M3/"

# kind: clip (src, in, dur) | still (src, dur) | red (src, dur) | black (dur)
# every row: (beat, kind, src, in|dur, dur|None, label)

def movement_1(v):
    corner = 1.6 if v == "v7" else 1.45
    title = 4.5   # the VO title read ("How to solve a problem. In a few simple steps.") is 4.3s at 2.3 w/s
    return [
        ("1",   "still", M1+"01_beat1_S01_title-card.png", title, None, "1 · TITLE"),
        ("2",   "clip", M1+"02_beat2_S03_claude-writing-loop.mp4", 2.0, corner, "2 · Claude's nook"),
        ("2",   "clip", M1+"03_beat2_S04_codex-study-fix.mp4", 2.2, corner, "2 · Codex's rack"),
        ("2",   "clip", M1+"04_beat2_S05_gemini-one-more.mp4", 2.0, corner, "2 · Gemini's moodboard"),
        ("2",   "clip", M1+"05_beat2_S06_grok-throw.mp4", 1.6, corner, "2 · Grok's dartboard"),
        ("2",   "clip", M1+"06_beat2_S02_sean-coffee.mp4", 4.6, corner, "2 · Sean, coffee"),
        # S07: the screen snaps on at 1.8s; the push-in starts at 4.54s. Sean pulls the zoom to ~3s in the cut → two pieces.
        ("3",   "clip", M1+"07_beat3_S07_alarm-pushin.mp4", 1.0, 1.6, "3 · ALARM #1 — PROBLEM!"),
        ("3",   "clip", M1+"07_beat3_S07_alarm-pushin.mp4", 4.3, 1.0, "3 · ALARM #1 — the push-in"),
    ]

def movement_2(v):
    if v == "v7":
        b = dict(react=(0.2, 1.3, 5.0, 1.5), go=(3.8, 2.8), claude=(1.0, 5.0), codex=(0.5, 5.5), gemini=(0.3, 5.2), grok=(0.5, 5.5), hollow=(1.7, 4.5), alarm2=(0.8, 4.5))
    else:
        b = dict(react=(0.3, 1.1, 5.1, 1.3), go=(4.2, 2.4), claude=(1.2, 4.0), codex=(0.6, 4.2), gemini=(0.3, 4.0), grok=(0.6, 4.4), hollow=(1.9, 3.8), alarm2=(0.9, 3.8))
    r = b["react"]
    return [
        # S09 ends on Sean turned to the mascots, S10 opens on him facing the room — the cut is on his look (M2 README).
        ("3.5", "clip", M2+"08_beat3h_S09_room-reacts.mp4", r[0], r[1], "3½ · the room looks up"),
        ("3.5", "clip", M2+"08_beat3h_S09_room-reacts.mp4", r[2], r[3], "3½ · …then at Sean"),
        ("4",   "clip", M2+"09_beat4_S10_silent-go.mp4", *b["go"], "4 · the silent GO"),
        ("5",   "clip", M2+"10_beat5_S12_claude-canyon.mp4", *b["claude"], "5 · Claude — the 40 pages"),
        ("6",   "clip", M2+"11_beat6_S13_codex-screen-pop.mp4", *b["codex"], "6 · Codex — the full rebuild"),
        ("7",   "clip", M2+"12_beat7_S14_gemini-whirlwind.mp4", *b["gemini"], "7 · Gemini — the fifty"),
        ("8",   "clip", M2+"13_beat8_S06B_grok-demolition.mp4", *b["grok"], "8 · Grok — the wall"),
        ("9",   "clip", M2+"14_beat9_S02_hollow-ship-it.mp4", *b["hollow"], "9 · the hollow SHIP IT"),
        ("10",  "clip", M2+"15_beat10_S08_alarm2.mp4", *b["alarm2"], "10 · ALARM #2 — PROBLEM (STILL!)"),
    ]

def movement_3(v):
    # The wide: motion 3.0–7.5s, frozen from ~7.7s to the end (Sean's own roll ends on the freeze).
    # Beat 12: the eyes begin to open at ~5.7s → out-point 5.6s (answer 4). Never shortened below the held breath.
    if v == "v7":
        notices, wide, freeze, turn, hands = (1.6, 2.6), (2.0, 5.8), 1.5, (0.4, 5.2), (0.0, 2.4)
        pit, deleg, celeb, colorize = 1.2, (0.6, 7.4), (0.3, 3.2), (0.8, 4.0)
    else:
        notices, wide, freeze, turn, hands = (2.0, 1.8), (3.0, 4.8), 1.2, (0.6, 3.9), (0.6, 1.6)
        pit, deleg, celeb, colorize = 1.2, (0.6, 5.2), (0.3, 2.6), (0.9, 3.2)
    return [
        ("10.5", "clip", M3+"16_beat10.5_S19_sean-notices.mp4", *notices, "10.5 · Sean alone notices"),
        ("11",   "clip", M3+"17_beat11_S15_the-wide.mp4", *wide, "11 · THE WIDE — chaos, the swivel, the freeze"),
        ("11",   "still", M3+"17_beat11_S15_freeze-frame.png", freeze, None, "11 · RECORD SCRATCH (the freeze, held)"),
        ("12",   "clip", M3+"18_beat12_S10_the-swivel.mp4", 0.5, 5.1, "12 · THE SWIVEL (held; out before the eyes open)"),
        ("13.1", "clip", M3+"19_beat13.1_S16_the-turn-back.mp4", *turn, "13.1 · the turn back — eyes open on us"),
        ("13.2", "clip", M3+"20_beat13.2_S17_the-hands.mp4", *hands, "13.2 · the hands"),
        ("13.3", "clip", M3+"21_beat13.3_S11_chat-typewriter.mp4", 0.0, 4.67, "13.3 · THE QUESTION (typed; Sean crops in)"),
        ("14",   "clip", M3+"22_beat14_S08_replay-cursor.mp4", 0.0, 6.0, "14 · THE REPLAY"),
        ("15",   "clip", M3+"23_beat15_S03_claude-relief.mp4", 0.9, 1.1, "15 · relief — Claude"),
        ("15",   "clip", M3+"24_beat15_S04_codex-relief.mp4", 0.9, 1.1, "15 · relief — Codex"),
        ("15",   "clip", M3+"25_beat15_S05_gemini-relief.mp4", 0.9, 1.1, "15 · relief — Gemini"),
        ("15",   "clip", M3+"26_beat15_S06B_grok-relief.mp4", 0.9, 1.2, "15 · relief — Grok"),
        ("16",   "clip", M3+"27_beat16_S02_the-delegation.mp4", *deleg, "16 · THE DELEGATION"),
        ("16.5", "clip", M3+"28_beat16.5_S03_claude-pitstop.mp4", 0.0, pit, "16.5 · PIT STOP — Claude"),
        ("16.5", "clip", M3+"29_beat16.5_S04_codex-pitstop.mp4", 0.0, pit, "16.5 · PIT STOP — Codex"),
        ("16.5", "clip", M3+"30_beat16.5_S05_gemini-pitstop.mp4", 0.0, pit, "16.5 · PIT STOP — Gemini"),
        ("16.5", "clip", M3+"31_beat16.5_S06B_grok-pitstop.mp4", 0.4, pit, "16.5 · PIT STOP — Grok, the BUY button"),
        ("17",   "clip", M3+"32_beat17_S18_the-ship-key.mp4", 1.4, 2.0, "17 · THE SHIP KEY"),
        ("18",   "clip", M3+"33_beat18_S08_user-colorizes.mp4", *colorize, "18 · the USER colorizes"),
        ("18.5", "clip", M3+"34_beat18.5_S09_team-celebrates.mp4", *celeb, "18.5 · the team celebrates"),
        # The button line is 11 words ≈ 4.8s at 2.3 w/s; the alarm cuts "quiet—". Hold 4.6s + the sting's 0.6s of green.
        ("19",   "still", M3+"35_beat19_S08_the-button-hold.png", 4.6, None, "19 · THE BUTTON (VO runs here)"),
        # The sting clip: green holds to 1.5s, white flash 1.5–1.75s, ANOTHER PROBLEM! from 2.0s, the set rocks to ~3s.
        ("20",   "clip", M3+"36_beat20_S08_sting-transition.mp4", 0.9, 1.6, "20 · the sting — the alarm cuts the word"),
        ("20",   "red",  M3+"36_beat20_S08_end-frame.png", 0.15, None, ""),
        ("20",   "black", None, 1.0, None, ""),
    ]

def label_png(tmp, i, text):
    from PIL import Image, ImageDraw, ImageFont
    if not text: return None
    try: f = ImageFont.truetype(FONT, 22)
    except Exception: f = ImageFont.load_default()
    im = Image.new("RGBA", (W, 44), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    w = d.textlength(text, font=f); d.rectangle([0, 0, w + 24, 40], fill=(0, 0, 0, 140)); d.text((12, 8), text, fill=(255, 255, 255, 255), font=f)
    p = os.path.join(tmp, f"lab{i:02d}.png"); im.save(p); return p

def tc(t): return f"{int(t // 60)}:{t % 60:04.1f}"

def dur_of(s):
    return s[4] if s[1] == "clip" else s[3]

def seg(i, tmp, s, t_start):
    out = os.path.join(tmp, f"seg{i:02d}.mp4")
    base = f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={FPS}"
    beat, kind, src, a, b, lab = s
    lab = f"{tc(t_start)}  {lab}" if lab else ""
    if kind == "clip":
        cmd = ["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{a:.2f}", "-t", f"{b:.2f}", "-i", src]
    elif kind == "still":
        cmd = ["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-t", f"{a:.2f}", "-i", src]
    elif kind == "red":
        cmd = ["ffmpeg", "-loglevel", "error", "-y", "-loop", "1", "-t", f"{a:.2f}", "-i", src, "-vf", base + ",drawbox=c=red@0.5:t=fill"]
    else:
        cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-t", f"{a:.2f}", "-i", f"color=black:s={W}x{H}:r={FPS}", "-vf", "setsar=1"]
    if kind in ("clip", "still"):
        lp = label_png(tmp, i, lab)
        if lp: cmd += ["-loop", "1", "-i", lp, "-filter_complex", f"[0:v]{base}[v];[v][1:v]overlay=16:16:shortest=1"]
        else: cmd += ["-vf", base]
    cmd += ["-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-r", str(FPS), out]
    subprocess.run(cmd, check=True)
    return out

def main():
    args = sys.argv[1:]
    out = args[0]; v = "v7"; mv = "all"
    if "--variant" in args: v = args[args.index("--variant") + 1]
    if "--movement" in args: mv = args[args.index("--movement") + 1]
    parts = {"1": movement_1, "2": movement_2, "3": movement_3}
    shots = []
    for k in (["1", "2", "3"] if mv == "all" else [mv]): shots += parts[k](v)
    tmp = tempfile.mkdtemp(); t = 0.0; rows = []; segs = []
    for i, s in enumerate(shots):
        segs.append(seg(i, tmp, s, t)); d = dur_of(s); rows.append((s[0], s[5], t, d, t + d)); t += d
    lst = os.path.join(tmp, "list.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in segs))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-r", str(FPS), out], check=True)
    md = [f"# {os.path.basename(out)} — beat table ({v}, movement {mv}) · total {tc(t)} ({t:.1f}s)", "", "| beat | segment | start | dur | end |", "|---|---|---|---|---|"]
    for beat, lab, a, d, b in rows:
        md.append(f"| {beat} | {lab or '(red / black)'} | {tc(a)} | {d:.2f} | {tc(b)} |")
    open(out.rsplit(".", 1)[0] + ".beats.md", "w").write("\n".join(md) + "\n")
    print("\n".join(md))

if __name__ == "__main__":
    main()
