from PIL import Image

img = Image.open('characters/sean-anchor/turnarounds/body-back.png')
# Crop the tee area of the back view figure
# X: 2000 to 2160, Y: 380 to 550
x_start, x_end = 2000, 2160
y_start, y_end = 380, 550

colors = {}
for y in range(y_start, y_end):
    for x in range(x_start, x_end):
        p = img.getpixel((x, y))
        colors[p] = colors.get(p, 0) + 1

# Print the top 10 most common colors
sorted_colors = sorted(colors.items(), key=lambda x: x[1], reverse=True)
print("Top 15 colors in back-view tee:")
for col, cnt in sorted_colors[:15]:
    r, g, b = col
    print(f"  Color {col} (#{r:02X}{g:02X}{b:02X}): count={cnt}")

# Let's do the same for the jeans
# X: 2000 to 2160, Y: 600 to 950
x_start_j, x_end_j = 2000, 2160
y_start_j, y_end_j = 600, 950

colors_j = {}
for y in range(y_start_j, y_end_j):
    for x in range(x_start_j, x_end_j):
        p = img.getpixel((x, y))
        colors_j[p] = colors_j.get(p, 0) + 1

sorted_colors_j = sorted(colors_j.items(), key=lambda x: x[1], reverse=True)
print("\nTop 15 colors in back-view jeans:")
for col, cnt in sorted_colors_j[:15]:
    r, g, b = col
    print(f"  Color {col} (#{r:02X}{g:02X}{b:02X}): count={cnt}")

