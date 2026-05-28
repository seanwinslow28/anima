from PIL import Image

# Load the image
img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
w, h = img.size
print(f"Image dimensions: {w}x{h}")

# The back view is roughly the rightmost figure on the top half of the sheet.
back_crop = img.crop((1800, 50, 2300, 1200))
back_crop.save('back_crop.png')
print("Cropped back view saved as back_crop.png")

# Let's get the background color at top-left.
bg_color = img.getpixel((10, 10))
print(f"Background color sample: {bg_color}")

# Let's sample a region on the back view's tee (around X=2080, Y=450)
tee_samples = []
for y in range(400, 500, 10):
    for x in range(2050, 2110, 10):
        r, g, b = img.getpixel((x, y))
        tee_samples.append((r, g, b))

# Average tee color:
tee_r = sum(c[0] for c in tee_samples) // len(tee_samples)
tee_g = sum(c[1] for c in tee_samples) // len(tee_samples)
tee_b = sum(c[2] for c in tee_samples) // len(tee_samples)
print(f"Average tee color sample: #{tee_r:02X}{tee_g:02X}{tee_b:02X} (RGB: {tee_r}, {tee_g}, {tee_b})")

# Let's sample a region on the back view's jeans (around X=2080, Y=800)
jeans_samples = []
for y in range(750, 850, 10):
    for x in range(2050, 2110, 10):
        r, g, b = img.getpixel((x, y))
        jeans_samples.append((r, g, b))

jeans_r = sum(c[0] for c in jeans_samples) // len(jeans_samples)
jeans_g = sum(c[1] for c in jeans_samples) // len(jeans_samples)
jeans_b = sum(c[2] for c in jeans_samples) // len(jeans_samples)
print(f"Average jeans color sample: #{jeans_r:02X}{jeans_g:02X}{jeans_b:02X} (RGB: {jeans_r}, {jeans_g}, {jeans_b})")

