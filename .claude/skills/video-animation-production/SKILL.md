---
name: video-animation-production
description: Automate video editing, conversion, and asset generation using FFmpeg and ImageMagick. Triggers on "convert video", "create GIF", "burn subtitles", "sprite sheet from frames", or "ffmpeg automation".
---

# Video & Animation Production

## Purpose

Automate repetitive media tasks in the game development pipeline. Convert formats, generate optimized GIFs for devlogs, burn subtitles into trailers, and assemble sprite sheets from raw frames without manual editor work.

## When to Use

- Converting large video captures to lightweight GIFs/WEBMs
- Generating sprite sheets from frame sequences (001.png, 002.png...)
- Embedding hard subtitles into promotional clips
- Extracting audio tracks for game engine use
- Batch resizing or compressing assets

## Examples

**Example 1: Devlog GIF Creation**
```
User: "Convert 'gameplay.mp4' to a high-quality GIF for Twitter."
Claude: [Uses video-animation-production]
Generating palette for optimal colors...
Running FFmpeg:
ffmpeg -i gameplay.mp4 -vf "fps=15,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 output.gif
Success! Size: 2.4MB
```

**Example 2: Burning Subtitles**
```
User: "Hardcode the subtitles from 'dialogue.srt' into the trailer."
Claude: [Uses video-animation-production]
Using 'subtitles' filter to burn text:
ffmpeg -i trailer.mp4 -vf "subtitles=dialogue.srt" -c:a copy output_subbed.mp4
```

## Core Workflows

### 1. FFmpeg Automation (Python Wrapper)
Use `ffmpeg-python` for readable, maintainable scripts rather than complex CLI strings.

```python
import ffmpeg

# Basic Conversion (MP4 -> WEBM for web)
def convert_to_webm(input_file, output_file):
    (
        ffmpeg
        .input(input_file)
        .output(output_file, vcodec='libvpx-vp9', crf=30, b='0')
        .run()
    )

# Extract Audio (Video -> OGG for Phaser)
def extract_audio(input_file, output_file):
    (
        ffmpeg
        .input(input_file)
        .output(output_file, acodec='libvorbis')
        .run()
    )
```

### 2. Sprite Sheet Assembly (ImageMagick)
Stitch individual frames into a grid for game engine use.

**Command:**
```bash
magick montage \
  -tile 8x4 \            # Columns x Rows (adjust based on frame count)
  -geometry +0+0 \       # Zero padding (critical for games)
  -background transparent \
  frame_*.png \
  spritesheet.png
```

**Node.js Automation:**
```javascript
const { exec } = require('child_process');

function createAtlas(pattern, output) {
  const cmd = `magick montage -tile 8x4 -geometry +0+0 -background transparent ${pattern} ${output}`;
  exec(cmd, (err) => {
    if (err) console.error(err);
    else console.log(`Atlas created: ${output}`);
  });
}
```

### 3. Subtitle Handling
Two methods: Hard (burned-in) for social media, Soft (embedded track) for players.

**Hard Subtitles (Burned-in):**
```python
# Force subtitles onto video pixels
ffmpeg.input('video.mp4') \
    .output('output.mp4', vf='subtitles=subs.srt') \
    .run()
```

**Soft Subtitles (Selectable Track):**
```python
# Add stream without re-encoding video
ffmpeg.input('video.mp4') \
    .input('subs.srt') \
    .output('output.mkv', c='copy', **{'c:s': 'srt'}) \
    .run()
```

### 4. GIF Optimization Workflow
Quality control for devlogs is crucial. Avoid default FFmpeg GIF conversion (it looks terrible).

**Two-Pass Palette Generation:**
1.  **Generate Palette:** Analyze colors in the video to create a custom 256-color map.
2.  **Apply Palette:** Use the map to render the GIF.

```bash
# Detailed CLI for quality 
ffmpeg -i input.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif
```

## Success Criteria

- [ ] Output GIFs are under 5MB (social media limit)
- [ ] Sprite sheets have 0px padding between frames
- [ ] Audio extracts are in OGG/MP3 format for web
- [ ] Hard subtitles are readable and synced
- [ ] Backgrounds in sprite sheets are transparent (not white/black)

## Copy/Paste Ready

```
"Convert this gameplay clip to a devlog GIF"
"Extract the OGG audio from the cutscene video"
"Assemble these frames into a 8x4 sprite sheet"
"Burn the .srt subtitles into the trailer"
```
