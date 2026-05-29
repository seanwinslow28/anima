from PIL import Image
import math

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
bg = (246, 242, 223)

def is_fg(p):
    dist = math.sqrt((p[0]-bg[0])**2 + (p[1]-bg[1])**2 + (p[2]-bg[2])**2)
    return dist > 35

# Front view is roughly X in [204, 670]
# But wait, does it have other elements in the crop?
# Let's find the active columns in [204, 670] above Y=1100
col_counts = []
for x in range(200, 700):
    cnt = sum(1 for y in range(100, 1050) if is_fg(img.getpixel((x, y))))
    col_counts.append((x, cnt))

non_zero_x = [x for x, cnt in col_counts if cnt > 0]
x_start = min(non_zero_x)
x_end = max(non_zero_x)
print(f"Front View X range: {x_start} to {x_end}")

# Measure the block
top_y = None
bottom_y = None
for y in range(50, 1150):
    row_fg = False
    for x in range(x_start, x_end + 1):
        if is_fg(img.getpixel((x, y))):
            row_fg = True
            break
    if row_fg and top_y is None:
        top_y = y
    if row_fg:
        bottom_y = y

total_height = bottom_y - top_y
print(f"Front View bounds: Y={top_y} to {bottom_y}, Height={total_height} px")

# Widths profile
widths = []
for y in range(top_y, bottom_y + 1):
    left_x = None
    right_x = None
    for x in range(x_start, x_end + 1):
        if is_fg(img.getpixel((x, y))):
            if left_x is None:
                left_x = x
            right_x = x
    if left_x is not None:
        widths.append((y, right_x - left_x + 1, left_x, right_x))
    else:
        widths.append((y, 0, 0, 0))

# Head max width (search in first 220 rows)
head_max_w = 0
head_max_y = None
for idx in range(220):
    y, w_val, lx, rx = widths[idx]
    if w_val > head_max_w:
        head_max_w = w_val
        head_max_y = y

# Neck min width
neck_min_w = 9999
neck_min_y = None
for idx in range(head_max_y - top_y, head_max_y - top_y + 120):
    y, w_val, lx, rx = widths[idx]
    if w_val < neck_min_w:
        neck_min_w = w_val
        neck_min_y = y

# Shoulders max width (in next 150 rows)
shoulder_max_w = 0
shoulder_max_y = None
for idx in range(neck_min_y - top_y, neck_min_y - top_y + 150):
    y, w_val, lx, rx = widths[idx]
    if w_val > shoulder_max_w:
        shoulder_max_w = w_val
        shoulder_max_y = y

print(f"Head Max Width: {head_max_w} px at Y={head_max_y}")
print(f"Neck Min Width (chin/base of head): {neck_min_w} px at Y={neck_min_y}")
print(f"Shoulder Max Width: {shoulder_max_w} px at Y={shoulder_max_y}")

head_height = neck_min_y - top_y
print(f"Calculated Head Height: {head_height} px")
print(f"Head-to-body ratio: 1 : {total_height / head_height:.2f}")
print(f"Shoulder width / Head width: {shoulder_max_w / head_max_w:.2f}")

