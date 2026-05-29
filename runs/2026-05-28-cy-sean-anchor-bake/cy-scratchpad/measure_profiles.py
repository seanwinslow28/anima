from PIL import Image
import math

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
bg = (246, 242, 223)

def is_fg(p):
    dist = math.sqrt((p[0]-bg[0])**2 + (p[1]-bg[1])**2 + (p[2]-bg[2])**2)
    return dist > 35

def measure_block(name, x_start, x_end):
    # Find top and bottom
    top_y = None
    bottom_y = None
    for y in range(50, 1150):
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
            widths.append((y, right_x - left_x + 1, left_x, right_x))
        else:
            widths.append((y, 0, 0, 0))

    # Head max width and neck min Y
    head_max_w = 0
    head_max_y = None
    for idx in range(min(220, len(widths))):
        y, w_val, lx, rx = widths[idx]
        if w_val > head_max_w:
            head_max_w = w_val
            head_max_y = y

    # Neck
    neck_min_w = 9999
    neck_min_y = None
    for idx in range(head_max_y - top_y, min(head_max_y - top_y + 120, len(widths))):
        y, w_val, lx, rx = widths[idx]
        if w_val < neck_min_w:
            neck_min_w = w_val
            neck_min_y = y

    head_height = neck_min_y - top_y
    ratio = total_height / head_height
    print(f"[{name}] Y={top_y} to {bottom_y}, Height={total_height} px. Head Height={head_height} px. Ratio = 1 : {ratio:.2f}")

measure_block("Profile Right", 888, 1083)
measure_block("Profile Left", 1424, 1620)
measure_block("Back View", 1897, 2258)

