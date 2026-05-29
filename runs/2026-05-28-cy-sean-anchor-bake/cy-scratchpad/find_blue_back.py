from PIL import Image

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
x_start, x_end = 1897, 2258
y_start, y_end = 92, 1135

blue_pixels = []
for y in range(y_start, y_end):
    for x in range(x_start, x_end):
        r, g, b = img.getpixel((x, y))
        # Blue/cyan check: B is higher than R and G, and not too dark or light
        if b > r + 15 and b > g + 10 and 100 < b < 220:
            blue_pixels.append((x, y, (r, g, b)))

print(f"Total blue pixels in back view: {len(blue_pixels)}")
if blue_pixels:
    print("Sample blue pixels in back view:")
    for x, y, col in blue_pixels[:30]:
        print(f"  ({x}, {y}): {col}")

