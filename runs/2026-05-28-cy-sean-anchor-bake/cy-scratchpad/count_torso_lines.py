from PIL import Image

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
x_start, x_end = 1950, 2200
# Torso of the back-view figure
y_start, y_end = 310, 700

graphite_pixels = []
for y in range(y_start, y_end):
    for x in range(x_start, x_end):
        r, g, b = img.getpixel((x, y))
        # #8A8580 ±15
        if (123 <= r <= 153) and (118 <= g <= 148) and (113 <= b <= 143):
            graphite_pixels.append((x, y, (r, g, b)))

print(f"Total graphite pixels in torso [310, 700]: {len(graphite_pixels)}")
if graphite_pixels:
    print("Coordinates and colors of first 50 graphite pixels in torso:")
    for x, y, col in graphite_pixels[:50]:
        print(f"  ({x}, {y}): {col}")

