from PIL import Image
import math

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
w, h = img.size

# Let's count pixels matching graphite-construction-lighter: #8A8580.
# ±15 means R in [123, 153], G in [118, 148], B in [113, 143].
# Let's check if there are any pixels matching this color range.
graphite_count = 0
graphite_pixels = []

# Let's also check for blue/cyan construction lines, e.g. R < 150, G > 180, B > 200 (like light blue)
blue_count = 0
blue_pixels = []

for y in range(0, h, 2):
    for x in range(0, w, 2):
        r, g, b = img.getpixel((x, y))
        # Graphite check
        if (123 <= r <= 153) and (118 <= g <= 148) and (113 <= b <= 143):
            # Check if it's not part of the background or hair
            graphite_count += 1
            if len(graphite_pixels) < 20:
                graphite_pixels.append(((x, y), (r, g, b)))
        
        # Light blue check
        if r < 180 and g > 150 and b > 180 and b > r + 30:
            blue_count += 1
            if len(blue_pixels) < 20:
                blue_pixels.append(((x, y), (r, g, b)))

print(f"Graphite construction line candidate pixels (#8A8580 range): {graphite_count}")
if graphite_pixels:
    print("Sample graphite pixels:")
    for pos, col in graphite_pixels:
        print(f"  Pos {pos}: {col}")

print(f"Light blue construction line candidate pixels: {blue_count}")
if blue_pixels:
    print("Sample blue pixels:")
    for pos, col in blue_pixels:
        print(f"  Pos {pos}: {col}")

