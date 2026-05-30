from PIL import Image
from collections import Counter

img = Image.open('body-back.png')
colors = img.getdata()
counter = Counter(colors)

print("Top 25 colors in body-back.png:")
for color, count in counter.most_common(25):
    hex_color = '#{:02x}{:02x}{:02x}'.format(*color[:3])
    print(f" - {color} ({hex_color}): count {count} ({count/len(colors):.2%})")
