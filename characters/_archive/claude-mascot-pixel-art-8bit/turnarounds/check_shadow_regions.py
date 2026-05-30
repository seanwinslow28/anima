from PIL import Image

img = Image.open('body-back.png')
width, height = img.size

TARGETS = {
    'primary_orange': (232, 155, 107),
    'warm_brown_shadow': (168, 107, 69)
}
TOLS = {
    'primary_orange': 10,
    'warm_brown_shadow': 6
}

# Find bounding box
bg_sample = (230, 230, 230)
ymin, ymax = height, 0
xmin, xmax = width, 0
for y in range(height):
    for x in range(width):
        p = img.getpixel((x, y))[:3]
        is_bg = (p[0] > 210 and p[1] > 210 and p[2] > 210 and abs(p[0] - p[1]) < 15 and abs(p[1] - p[2]) < 15)
        if not is_bg:
            if y < ymin: ymin = y
            if y > ymax: ymax = y
            if x < xmin: xmin = x
            if x > xmax: xmax = x

print(f"Bounding box: ymin={ymin}, ymax={ymax}, xmin={xmin}, xmax={xmax}")

# Let's count how many warm brown shadow pixels have:
# - warm brown shadow neighbor at (x, y-1) or (x, y+1)
# - orange neighbor at (x, y-1) or (x, y+1)
# Let's check a patch with high density of shadow.
shadow_counts_per_row = [0] * height
for y in range(height):
    for x in range(width):
        p = img.getpixel((x, y))[:3]
        if abs(p[0] - TARGETS['warm_brown_shadow'][0]) <= TOLS['warm_brown_shadow'] and \
           abs(p[1] - TARGETS['warm_brown_shadow'][1]) <= TOLS['warm_brown_shadow'] and \
           abs(p[2] - TARGETS['warm_brown_shadow'][2]) <= TOLS['warm_brown_shadow']:
            shadow_counts_per_row[y] += 1

print("\nShadow pixels per row in some regions:")
for y in range(ymin, ymax+1, 20):
    print(f"Row {y} (rel {y-ymin}): {shadow_counts_per_row[y]} shadow pixels")
