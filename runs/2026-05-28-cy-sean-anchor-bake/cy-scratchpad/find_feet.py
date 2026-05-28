from PIL import Image
import math

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
w, h = img.size
bg = (246, 242, 223)

def is_fg(p):
    dist = math.sqrt((p[0]-bg[0])**2 + (p[1]-bg[1])**2 + (p[2]-bg[2])**2)
    return dist > 35

# Let's count foreground pixels in X=[1897, 2258] for each Y from 1000 to 1500
for y in range(1000, 1500, 5):
    cnt = sum(1 for x in range(1897, 2258) if is_fg(img.getpixel((x, y))))
    print(f"Row {y}: {cnt}")

