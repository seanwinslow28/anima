from PIL import Image

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
x_start, x_end = 204, 670
y_start, y_end = 60, 1149

blue_pixels = []
for y in range(y_start, y_end):
    for x in range(x_start, x_end):
        r, g, b = img.getpixel((x, y))
        # Wide blue/cyan check: B > R + 12 and B > G + 8 and 100 < b < 220
        if b > r + 12 and b > g + 8 and 100 < b < 220:
            blue_pixels.append((x, y, (r, g, b)))

print(f"Total blue pixels in front view: {len(blue_pixels)}")
if blue_pixels:
    print("Sample blue pixels in front view:")
    for x, y, col in blue_pixels[:30]:
        print(f"  ({x}, {y}): {col}")

