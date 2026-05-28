from PIL import Image
import math

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
# Back view body is roughly X in [1950, 2200], Y in [300, 700]
x_start, x_end = 1950, 2200
y_start, y_end = 300, 700

# Graphite color range: R in [123, 153], G in [118, 148], B in [113, 143]
graphite_pixels = []
for y in range(y_start, y_end):
    for x in range(x_start, x_end):
        r, g, b = img.getpixel((x, y))
        if (123 <= r <= 153) and (118 <= g <= 148) and (113 <= b <= 143):
            # Let's verify it's not part of the tee (which was sampled as #394757 = 57, 71, 87)
            # and not part of the jeans (#9C9E9C = 156, 158, 156 - which is close, but let's check)
            graphite_pixels.append(((x, y), (r, g, b)))

print(f"Total candidate graphite pixels in back body: {len(graphite_pixels)}")
# Let's print some sample coordinates to see if they are inside the figure or background
# Background at top-left is (246, 242, 223) - color distance check
bg = (246, 242, 223)
inside_fg_pixels = []
for pos, col in graphite_pixels:
    x, y = pos
    # Check if this pixel is inside the figure contour
    # By checking if there are non-bg pixels to its left and right
    has_left = False
    for lx in range(x_start, x):
        p = img.getpixel((lx, y))
        if math.sqrt((p[0]-bg[0])**2 + (p[1]-bg[1])**2 + (p[2]-bg[2])**2) > 35:
            has_left = True
            break
    has_right = False
    for rx in range(x + 1, x_end):
        p = img.getpixel((rx, y))
        if math.sqrt((p[0]-bg[0])**2 + (p[1]-bg[1])**2 + (p[2]-bg[2])**2) > 35:
            has_right = True
            break
    if has_left and has_right:
        inside_fg_pixels.append((pos, col))

print(f"Inside-figure graphite-like pixels: {len(inside_fg_pixels)}")
if inside_fg_pixels:
    print("Sample inside-figure graphite pixels:")
    for pos, col in inside_fg_pixels[:30]:
        print(f"  Pos {pos}: {col}")

