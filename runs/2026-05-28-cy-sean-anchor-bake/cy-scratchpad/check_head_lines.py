from PIL import Image
import math

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
# Bottom-left head is roughly in X=[200, 600], Y=[1200, 1750]
x_start, x_end = 200, 600
y_start, y_end = 1200, 1750

# We want to find colors that look like sketch lines:
# They are not the cream background (approx 246, 242, 223),
# not the black lineart (dark gray, R,G,B < 80),
# not the skin (light pinkish/peach, R > 230, G > 200, B > 190),
# not the hair (yellowish, R > 200, G > 180, B > 130).
# Let's list colors that are medium-light gray or blue/cyan.

bg = (246, 242, 223)

colored_pixels = []
for y in range(y_start, y_end, 2):
    for x in range(x_start, x_end, 2):
        p = img.getpixel((x, y))
        r, g, b = p
        
        # Calculate distance to background
        dist_bg = math.sqrt((r-bg[0])**2 + (g-bg[1])**2 + (b-bg[2])**2)
        if dist_bg < 30:
            continue
            
        # Ignore dark contour lines
        if r < 100 and g < 100 and b < 100:
            continue
            
        # Ignore skin/hair
        if r > 210 and g > 180:
            continue
            
        # What is left? Let's sample them.
        colored_pixels.append(((x, y), p))

print(f"Total non-contour, non-bg, non-skin/hair pixels in head close-up: {len(colored_pixels)}")
# Let's print the most common colors
color_counts = {}
for pos, col in colored_pixels:
    color_counts[col] = color_counts.get(col, 0) + 1

sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
print("Top 30 unique colors in this range:")
for col, cnt in sorted_colors[:30]:
    # Check if it matches graphite: #8A8580 ± 15 (123-153, 118-148, 113-143)
    r, g, b = col
    is_graphite = (123 <= r <= 153) and (118 <= g <= 148) and (113 <= b <= 143)
    is_blue = (b > r + 15) and (b > g + 10)
    label = "GRAPHITE" if is_graphite else ("BLUE-GRAY" if is_blue else "OTHER")
    print(f"  Color {col} (#{r:02X}{g:02X}{b:02X}): count={cnt} ({label})")

