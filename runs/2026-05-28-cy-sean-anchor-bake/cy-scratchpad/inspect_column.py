from PIL import Image

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
w, h = img.size
bg = (246, 242, 223)

fg_pixels = []
for y in range(100, 1100):
    p = img.getpixel((1917, y))
    # Distance to bg
    dist = ( (p[0]-bg[0])**2 + (p[1]-bg[1])**2 + (p[2]-bg[2])**2 )**0.5
    if dist > 20:
        fg_pixels.append((y, p, dist))

print(f"Total fg-like pixels at X=1917: {len(fg_pixels)}")
print("First 20 matching pixels:")
for y, p, dist in fg_pixels[:20]:
    print(f"Y={y}: {p}, dist={dist:.2f}")

print("\nLast 20 matching pixels:")
for y, p, dist in fg_pixels[-20:]:
    print(f"Y={y}: {p}, dist={dist:.2f}")

