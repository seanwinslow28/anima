from PIL import Image

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
x_start, x_end = 1897, 2258
y_start, y_end = 350, 700

# Let's count graphite-like pixels (#8A8580 ±15) per row
for y in range(y_start, y_end, 10):
    row_pixels = []
    for x in range(x_start, x_end):
        r, g, b = img.getpixel((x, y))
        if (123 <= r <= 153) and (118 <= g <= 148) and (113 <= b <= 143):
            row_pixels.append(x)
    if row_pixels:
        print(f"Row {y}: {len(row_pixels)} pixels at X coordinates: {row_pixels}")

