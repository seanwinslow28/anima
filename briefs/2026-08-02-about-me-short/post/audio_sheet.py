#!/usr/bin/env python3
"""
AUDIO SHEET — one review page per bin: a duration table (asked vs got) + a waveform strip per file, so a take can
be judged for length, transient placement and silence before anyone presses play. $0, deterministic.

    Usage:  audio_sheet.py [bin ...]        bins: sfx-eleven music-eleven music-lyria (default all)
    Writes audio/_sheets/<bin>.png + audio/_sheets/<bin>.md
"""
import subprocess, sys, pathlib, yaml
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent; BRIEF = HERE.parent; OUT = BRIEF / "audio" / "_sheets"
CUES = yaml.safe_load((HERE / "audio_cues.yaml").read_text())
BINS = {"sfx-eleven": (BRIEF / "audio/SFX/eleven", "eleven-sfx"), "music-eleven": (BRIEF / "audio/Music/eleven", "eleven-music"), "music-lyria": (BRIEF / "audio/Music/lyria", "lyria")}
FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"

def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip() or 0)

def wave(p, w, h, tmp):
    png = tmp / (p.stem + ".png")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(p), "-filter_complex", f"showwavespic=s={w}x{h}:colors=0x2b4c6f|0x2b4c6f", "-frames:v", "1", str(png)], check=True)
    return Image.open(png).convert("RGB")

def main():
    OUT.mkdir(parents=True, exist_ok=True); tmp = OUT / "_tmp"; tmp.mkdir(exist_ok=True)
    f = ImageFont.truetype(FONT, 14); fb = ImageFont.truetype(FONT, 16)
    for name in (sys.argv[1:] or list(BINS)):
        d, key = BINS[name]; files = sorted(d.glob("*.mp3"))
        if not files: continue
        asked = {c["id"]: c for c in CUES.get(key, [])}
        W, ROW, LAB = 1400, 96, 300; im = Image.new("RGB", (W, 40 + ROW * len(files)), "white"); dr = ImageDraw.Draw(im)
        dr.text((12, 10), f"{name} · {len(files)} files · waveform scaled to each file's own length; tick = 1s", fill="black", font=fb)
        md = [f"# {name}", "", "| file | cue | asked s | got s | note |", "|---|---|---|---|---|"]
        for i, p in enumerate(files):
            cid = p.stem.split("-lyria")[0].rsplit("-t", 1)[0] if "-lyria" in p.stem else p.stem.rsplit("-t", 1)[0]
            c = asked.get(cid, {}); a = c.get("seconds"); g = dur(p); y = 40 + i * ROW
            note = "" if not a else ("long ×%.1f — cut" % (g / a) if g > a * 1.6 else "short" if g < a * 0.7 else "ok")
            dr.text((12, y + 8), p.stem, fill="black", font=fb); dr.text((12, y + 30), (c.get("name", "") or "")[:44], fill="#555", font=f)
            dr.text((12, y + 50), f"asked {a or '–'}s · got {g:.1f}s · {note}", fill="#900" if "cut" in note else "#555", font=f)
            wv = wave(p, W - LAB - 20, ROW - 24, tmp); im.paste(wv, (LAB, y + 6))
            for s in range(0, int(g) + 1): x = LAB + int((W - LAB - 20) * s / max(g, 0.01)); dr.line([(x, y + 6), (x, y + 6 + (10 if s % 5 else 18))], fill="#bbb")
            md.append(f"| {p.name} | {c.get('name','')} | {a or ''} | {g:.1f} | {note} |")
        im.save(OUT / f"{name}.png"); (OUT / f"{name}.md").write_text("\n".join(md) + "\n"); print(f"{name}: {len(files)} files → {OUT / (name + '.png')}")

if __name__ == "__main__": main()
