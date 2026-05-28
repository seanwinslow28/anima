from PIL import Image

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
x_start, x_end = 1950, 2200
y_start, y_end = 112, 304

graphite_pixels = []
for y in range(y_start, y_end):
    for x in range(x_start, x_end):
        r, g, b = img.getpixel((x, y))
        # #8A8580 ±15
        if (123 <= r <= 153) and (118 <= g <= 148) and (113 <= b <= 143):
            graphite_pixels.append((x, y))

print(f"Total graphite pixels in back head: {len(graphite_pixels)}")

# Let's count them per row:
for y in range(y_start, y_end, 10):
    row_pixels = [x for (x, ry) in graphite_pixels if ry == y]
    if row_pixels:
        print(f"Row {y}: {len(row_pixels)} pixels at X: {row_pixels}")

