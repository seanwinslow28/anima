from PIL import Image

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
w, h = img.size
bg = (246, 242, 223)

def is_fg(p):
    return abs(p[0]-bg[0]) > 20 or abs(p[1]-bg[1]) > 20 or abs(p[2]-bg[2]) > 20

# Let's count foreground pixels per column for each column from X=1700 to 2200, but only for Y=100 to 1100
col_counts = []
for x in range(1700, 2200):
    cnt = 0
    for y in range(100, 1100):
        if is_fg(img.getpixel((x, y))):
            cnt += 1
    col_counts.append((x, cnt))

# Let's find the minimum between two peaks
# The third figure (side view) peak is around X=1800-1950.
# The fourth figure (back view) peak is around X=2000-2150.
# Let's search for a gap (minimum count) in the range X=1850 to 2050.
min_count = 99999
gap_x = None
for x, cnt in col_counts:
    if 1850 <= x <= 2050:
        if cnt < min_count:
            min_count = cnt
            gap_x = x

print(f"Minimum column foreground count in gap range X=[1850, 2050]: {min_count} at X={gap_x}")

# Let's check if the count at gap_x is close to 0. If it is, then X=gap_x is a clean split point!
# Let's also print the column counts around gap_x:
for x in range(gap_x - 30, gap_x + 30):
    # Find the count in col_counts
    cnt = next(c for col, c in col_counts if col == x)
    print(f"Col {x}: {cnt}")

