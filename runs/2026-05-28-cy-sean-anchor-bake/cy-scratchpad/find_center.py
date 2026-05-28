from PIL import Image

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
w, h = img.size

# Background color
bg = (246, 242, 223)

def is_fg(p):
    return abs(p[0]-bg[0]) > 20 or abs(p[1]-bg[1]) > 20 or abs(p[2]-bg[2]) > 20

# Let's count how many foreground pixels there are in each column in the top half (y: 50 to 1200)
col_counts = []
for x in range(1800, 2400):
    count = 0
    for y in range(50, 1200):
        if is_fg(img.getpixel((x, y))):
            count += 1
    col_counts.append((x, count))

# Let's print the column counts to find where the figure starts and ends
for x, c in col_counts:
    if c > 0:
        print(f"Col {x}: {c}")

