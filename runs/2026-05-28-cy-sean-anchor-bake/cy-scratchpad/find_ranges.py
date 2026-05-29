from PIL import Image
import math

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
w, h = img.size
bg = (246, 242, 223)

def is_fg(p):
    dist = math.sqrt((p[0]-bg[0])**2 + (p[1]-bg[1])**2 + (p[2]-bg[2])**2)
    return dist > 35

col_counts = {}
for x in range(1700, 2350):
    cnt = sum(1 for y in range(100, 1050) if is_fg(img.getpixel((x, y))))
    col_counts[x] = cnt

# Let's list the contiguous blocks of columns with non-zero counts
in_block = False
block_start = None
for x in range(1700, 2350):
    cnt = col_counts[x]
    if cnt > 0 and not in_block:
        in_block = True
        block_start = x
    elif cnt == 0 and in_block:
        in_block = False
        print(f"Block: {block_start} to {x-1}")

if in_block:
    print(f"Block: {block_start} to 2349")

