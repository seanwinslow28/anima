from PIL import Image

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
w, h = img.size
bg = (246, 242, 223)

def is_fg(p):
    return abs(p[0]-bg[0]) > 20 or abs(p[1]-bg[1]) > 20 or abs(p[2]-bg[2]) > 20

# Count foreground pixels per row
row_counts = []
for y in range(50, 1750):
    cnt = sum(1 for x in range(50, w - 50) if is_fg(img.getpixel((x, y))))
    row_counts.append((y, cnt))

# Print row counts where there's a dip (gap between top row and bottom row)
# Let's search for a gap in Y=900 to 1300
min_cnt = 999999
gap_y = None
for y, cnt in row_counts:
    if 900 <= y <= 1300:
        if cnt < min_cnt:
            min_cnt = cnt
            gap_y = y

print(f"Minimum row foreground count in vertical gap range Y=[900, 1300]: {min_cnt} at Y={gap_y}")

# Print around gap_y
for y in range(gap_y - 50, gap_y + 50, 5):
    cnt = next(c for row, c in row_counts if row == y)
    print(f"Row {y}: {cnt}")

