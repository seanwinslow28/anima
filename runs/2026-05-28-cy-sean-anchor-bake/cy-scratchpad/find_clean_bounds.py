from PIL import Image
import math

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
w, h = img.size
bg = (246, 242, 223)

def is_fg(p):
    # Let's use a threshold of 35
    dist = math.sqrt((p[0]-bg[0])**2 + (p[1]-bg[1])**2 + (p[2]-bg[2])**2)
    return dist > 35

# Let's calculate the number of foreground pixels in Y=[100, 1050] for each column X in [1700, 2350]
col_counts = []
for x in range(1700, 2350):
    cnt = sum(1 for y in range(100, 1050) if is_fg(img.getpixel((x, y))))
    col_counts.append((x, cnt))

# Let's find the column X between 1850 and 2000 that has the absolute minimum count
min_gap_cnt = 99999
gap_x = None
for x, cnt in col_counts:
    if 1850 <= x <= 2000:
        if cnt < min_gap_cnt:
            min_gap_cnt = cnt
            gap_x = x

# Let's find the column X between 2200 and 2350 that has the absolute minimum count
min_right_cnt = 99999
right_x = None
for x, cnt in col_counts:
    if 2200 <= x <= 2350:
        if cnt < min_right_cnt:
            min_right_cnt = cnt
            right_x = x

print(f"Left Gap X (start of back view): {gap_x} (count={min_gap_cnt})")
print(f"Right Gap X (end of back view): {right_x} (count={min_right_cnt})")

