from PIL import Image

def detect_grid_size(path):
    img = Image.open(path)
    width, height = img.size
    
    # We want to find the minimum run length of colors horizontally and vertically.
    # Because of JPEG compression, colors might not be exactly identical, but we can look for
    # where transitions (large color differences) happen.
    
    # Let's compute local color differences horizontally and vertically
    diffs_x = []
    diffs_y = []
    
    for y in range(0, height, 4): # sample some rows
        row = [img.getpixel((x, y))[:3] for x in range(width)]
        transitions = []
        for x in range(1, width):
            # Euclidean distance
            p1, p2 = row[x-1], row[x]
            dist = sum((p1[i] - p2[i])**2 for i in range(3))**0.5
            if dist > 15: # Significant transition
                transitions.append(x)
        # Find distances between adjacent transitions
        diffs = [transitions[i] - transitions[i-1] for i in range(1, len(transitions))]
        diffs_x.extend(diffs)
        
    for x in range(0, width, 4): # sample some columns
        col = [img.getpixel((x, y))[:3] for y in range(height)]
        transitions = []
        for y in range(1, height):
            p1, p2 = col[y-1], col[y]
            dist = sum((p1[i] - p2[i])**2 for i in range(3))**0.5
            if dist > 15:
                transitions.append(y)
        diffs = [transitions[i] - transitions[i-1] for i in range(1, len(transitions))]
        diffs_y.extend(diffs)
        
    # Analyze frequency of difference lengths
    from collections import Counter
    print("Horizontal transition run lengths (top 15):")
    for val, count in Counter(diffs_x).most_common(15):
        print(f" - {val} px: count {count}")
        
    print("\nVertical transition run lengths (top 15):")
    for val, count in Counter(diffs_y).most_common(15):
        print(f" - {val} px: count {count}")

if __name__ == '__main__':
    detect_grid_size('body-3quarter.png')
