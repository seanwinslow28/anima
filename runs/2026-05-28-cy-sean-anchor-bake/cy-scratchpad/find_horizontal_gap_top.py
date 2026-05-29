from PIL import Image

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
w, h = img.size
bg = (246, 242, 223)

def is_fg(p):
    return abs(p[0]-bg[0]) > 20 or abs(p[1]-bg[1]) > 20 or abs(p[2]-bg[2]) > 20

# Let's count foreground pixels per column for Y = 100 to 1100
col_counts = []
for x in range(1800, 2250):
    cnt = sum(1 for y in range(100, 1100) if is_fg(img.getpixel((x, y))))
    col_counts.append((x, cnt))

# Let's find the minimum between X=1850 and X=2000
min_cnt = 99999
gap_x = None
for x, cnt in col_counts:
    if 1850 <= x <= 2000:
        if cnt < min_cnt:
            min_cnt = cnt
            gap_x = x

print(f"Minimum column count in X=[1850, 2000] for Y=[100, 1100]: {min_cnt} at X={gap_x}")

# Let's print counts around gap_x
for x in range(gap_x - 10, gap_x + 10):
    cnt = next(c for col, c in col_counts if col == x)
    print(f"Col {x}: {cnt}")

# Let's also find the right edge of the back view figure (where count drops to 0 or min near the right margin X=[2150, 2250])
min_cnt_right = 99999
right_gap_x = None
for x, cnt in col_counts:
    if 2150 <= x <= 2250:
        if cnt < min_cnt_right:
            min_cnt_right = cnt
            right_gap_x = x

print(f"Minimum column count in X=[2150, 2250] for Y=[100, 1100]: {min_cnt_right} at X={right_gap_x}")
for x in range(right_gap_x - 10, right_gap_x + 10):
    cnt = next(c for col, c in col_counts if col == x)
    print(f"Col {x}: {cnt}")

