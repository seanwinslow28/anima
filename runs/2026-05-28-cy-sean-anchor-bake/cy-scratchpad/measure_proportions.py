from PIL import Image

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
# Let's crop the back-view figure
# Bounding box of the back-view figure is approximately: x from 1850 to 2250, y from 50 to 1200
x_start, x_end = 1850, 2250
y_start, y_end = 50, 1200

# Background color is (246, 242, 223) or similar.
# Let's find rows that have figure pixels.
# A pixel is part of the figure if its distance to background is > 20
def is_fg(p, bg=(246, 242, 223)):
    return abs(p[0]-bg[0]) > 20 or abs(p[1]-bg[1]) > 20 or abs(p[2]-bg[2]) > 20

# Let's find the top (crown) and bottom (sole) of the back view figure
top_y = None
bottom_y = None

for y in range(y_start, y_end):
    row_fg = False
    for x in range(x_start, x_end):
        if is_fg(img.getpixel((x, y))):
            row_fg = True
            break
    if row_fg and top_y is None:
        top_y = y
    if row_fg:
        bottom_y = y

print(f"Figure detected from Y={top_y} to Y={bottom_y}")
total_height = bottom_y - top_y
print(f"Total height: {total_height} pixels")

# Let's write a loop to print the width of the silhouette at each Y step
# to identify the head, chin/neck, shoulders, hips, etc.
widths = []
for y in range(top_y, bottom_y + 1):
    left_x = None
    right_x = None
    for x in range(x_start, x_end):
        if is_fg(img.getpixel((x, y))):
            if left_x is None:
                left_x = x
            right_x = x
    if left_x is not None:
        widths.append((y, right_x - left_x, left_x, right_x))
    else:
        widths.append((y, 0, 0, 0))

# Let's find local minima and maxima in width to locate head (max), neck (min), shoulders (max), waist (min), hips (max), etc.
# Head is at the top. Let's find the head's maximum width in the range Y=top_y to Y=top_y+200
head_max_w = 0
head_max_y = None
for y, w, lx, rx in widths[:200]:
    if w > head_max_w:
        head_max_w = w
        head_max_y = y

# Neck (chin base) is the minimum width after the head max, say within Y=top_y+100 to top_y+250
neck_min_w = 9999
neck_min_y = None
for y, w, lx, rx in widths[head_max_y - top_y : head_max_y - top_y + 150]:
    if w < neck_min_w:
        neck_min_w = w
        neck_min_y = y

# Shoulders are the maximum width after the neck, say within Y=neck_min_y to neck_min_y+150
shoulder_max_w = 0
shoulder_max_y = None
for y, w, lx, rx in widths[neck_min_y - top_y : neck_min_y - top_y + 150]:
    if w > shoulder_max_w:
        shoulder_max_w = w
        shoulder_max_y = y

print(f"Head Max Width: {head_max_w} at Y={head_max_y}")
print(f"Neck/Chin Min Width (base of head): {neck_min_w} at Y={neck_min_y}")
print(f"Shoulder Max Width: {shoulder_max_w} at Y={shoulder_max_y}")

# Head height = neck_min_y - top_y
head_height = neck_min_y - top_y
print(f"Head height: {head_height} pixels")
print(f"Head to Body Ratio: 1 : {total_height / head_height:.2f}")

# Let's print out width profile around head and shoulders to verify:
print("\nProfile from Y=top_y to Y=shoulder_max_y + 50:")
for i in range(0, shoulder_max_y - top_y + 50, 10):
    y, w, lx, rx = widths[i]
    print(f"Y={y}: width={w} (L={lx}, R={rx})")

