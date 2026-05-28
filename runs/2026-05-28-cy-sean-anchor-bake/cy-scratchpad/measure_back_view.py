from PIL import Image

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
bg = (246, 242, 223)

def is_fg(p):
    return abs(p[0]-bg[0]) > 20 or abs(p[1]-bg[1]) > 20 or abs(p[2]-bg[2]) > 20

x_start, x_end = 1960, 2258
y_start, y_end = 50, 1200

# Find top and bottom Y of the back view figure
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
print(f"Figure bounds: Y={top_y} to Y={bottom_y}, height={total_height} px")

# Widths profile of just this figure
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

# Print the width of the figure at each row to inspect where the head and shoulders are
# Head range: Y=top_y to Y=top_y+200
head_max_w = 0
head_max_y = None
for i in range(200):
    y, w, lx, rx = widths[i]
    if w > head_max_w:
        head_max_w = w
        head_max_y = y

# Neck: local minimum in width below the head max.
# Let's search from head_max_y to head_max_y + 120
neck_min_w = 9999
neck_min_y = None
for i in range(head_max_y - top_y, head_max_y - top_y + 120):
    y, w, lx, rx = widths[i]
    if w < neck_min_w:
        neck_min_w = w
        neck_min_y = y

# Shoulders: maximum width in range neck_min_y to neck_min_y + 150
shoulder_max_w = 0
shoulder_max_y = None
for i in range(neck_min_y - top_y, neck_min_y - top_y + 150):
    y, w, lx, rx = widths[i]
    if w > shoulder_max_w:
        shoulder_max_w = w
        shoulder_max_y = y

print(f"Head Max Width: {head_max_w} px at Y={head_max_y}")
print(f"Neck Min Width (chin/base of head): {neck_min_w} px at Y={neck_min_y}")
print(f"Shoulder Max Width: {shoulder_max_w} px at Y={shoulder_max_y}")

head_height = neck_min_y - top_y
print(f"Calculated Head Height: {head_height} px")
print(f"Head-to-body ratio: 1 : {total_height / head_height:.2f}")

shoulder_to_head_width_ratio = shoulder_max_w / head_max_w
print(f"Shoulder width / Head width: {shoulder_to_head_width_ratio:.2f}")

# Let's write the profile details for manual validation
for idx in range(0, shoulder_max_y - top_y + 50, 10):
    y, w, lx, rx = widths[idx]
    print(f"Idx {idx} (Y={y}): w={w}, lx={lx}, rx={rx}")

