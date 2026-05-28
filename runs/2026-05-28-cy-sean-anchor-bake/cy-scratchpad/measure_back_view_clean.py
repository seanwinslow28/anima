from PIL import Image
import math

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
w, h = img.size
bg = (246, 242, 223)

def is_fg(p):
    dist = math.sqrt((p[0]-bg[0])**2 + (p[1]-bg[1])**2 + (p[2]-bg[2])**2)
    return dist > 35

x_start, x_end = 1897, 2258
y_start, y_end = 50, 1150

# 1. Find top_y and bottom_y
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

total_height = bottom_y - top_y
print(f"Clean Figure Bounds: Y={top_y} to Y={bottom_y}, Height={total_height} px")

# 2. Get widths of each row
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
        widths.append((y, right_x - left_x + 1, left_x, right_x))
    else:
        widths.append((y, 0, 0, 0))

# 3. Analyze head (top_y to top_y + 250)
head_max_w = 0
head_max_y = None
for idx in range(220): # first 220 pixels from top_y
    y, w_val, lx, rx = widths[idx]
    if w_val > head_max_w:
        head_max_w = w_val
        head_max_y = y

# Neck (search in head_max_y to head_max_y + 120)
neck_min_w = 9999
neck_min_y = None
for idx in range(head_max_y - top_y, head_max_y - top_y + 120):
    y, w_val, lx, rx = widths[idx]
    if w_val < neck_min_w:
        neck_min_w = w_val
        neck_min_y = y

# Shoulder (search in neck_min_y to neck_min_y + 150)
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

shoulder_to_head_width_ratio = shoulder_max_w / head_max_w
print(f"Shoulder width / Head width: {shoulder_to_head_width_ratio:.2f}")

# Hip height is approximately four head-heights from floor, i.e. bottom_y - 4 * head_height.
# Let's see: hip_to_floor should be approx 4 * head_height.
# Total height = 1100 px. 4 * head_height = 4 * 213 = 852 px.
# Let's calculate: Hip height from floor = bottom_y - hip_y.
# Let's find hip_y. Hips are below waist. Waist is a local minimum of width below shoulder_max_y.
# Let's search for waist minimum in Y = shoulder_max_y to shoulder_max_y + 250
waist_min_w = 9999
waist_min_y = None
for idx in range(shoulder_max_y - top_y, shoulder_max_y - top_y + 250):
    y, w_val, lx, rx = widths[idx]
    if w_val < waist_min_w:
        waist_min_w = w_val
        waist_min_y = y

# Hips are a local maximum below waist.
hips_max_w = 0
hips_max_y = None
for idx in range(waist_min_y - top_y, waist_min_y - top_y + 200):
    y, w_val, lx, rx = widths[idx]
    if w_val > hips_max_w:
        hips_max_w = w_val
        hips_max_y = y

print(f"Waist Min Width: {waist_min_w} px at Y={waist_min_y}")
print(f"Hips Max Width: {hips_max_w} px at Y={hips_max_y}")
hip_to_floor = bottom_y - hips_max_y
print(f"Hip-to-floor height: {hip_to_floor} px (approx {hip_to_floor / head_height:.2f} head heights)")

# Let's output some line-by-line profile details around head and neck
print("\nHead and Neck width profile details:")
for idx in range(0, neck_min_y - top_y + 20, 10):
    y, w_val, lx, rx = widths[idx]
    print(f"Idx {idx} (Y={y}): w={w_val}, lx={lx}, rx={rx}")

