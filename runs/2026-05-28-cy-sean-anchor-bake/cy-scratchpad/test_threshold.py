from PIL import Image
import math

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
w, h = img.size
bg = (246, 242, 223)

# Let's check color distance distribution on a vertical line X=1917 (which is in the gap)
# from Y=100 to 1050 (stopping before the ground line at 1070)
dists = []
for y in range(100, 1050):
    p = img.getpixel((1917, y))
    dist = math.sqrt((p[0]-bg[0])**2 + (p[1]-bg[1])**2 + (p[2]-bg[2])**2)
    dists.append(dist)

print(f"Max dist on X=1917 (gap): {max(dists):.2f}")
print(f"Mean dist on X=1917: {sum(dists)/len(dists):.2f}")

# Now let's check a column that runs down the middle of the back view figure: X=2100 (which is on the tee, jeans, head)
dists_fig = []
for y in range(100, 1050):
    p = img.getpixel((2100, y))
    dist = math.sqrt((p[0]-bg[0])**2 + (p[1]-bg[1])**2 + (p[2]-bg[2])**2)
    dists_fig.append(dist)

print(f"Min dist on X=2100 (figure): {min(dists_fig):.2f}")
print(f"Mean dist on X=2100 (figure): {sum(dists_fig)/len(dists_fig):.2f}")

# Let's count how many pixels have dist > 45 in both columns
cnt_gap = sum(1 for d in dists if d > 45)
cnt_fig = sum(1 for d in dists_fig if d > 45)
print(f"Using threshold 45: gap has {cnt_gap} pixels, figure has {cnt_fig} pixels.")

