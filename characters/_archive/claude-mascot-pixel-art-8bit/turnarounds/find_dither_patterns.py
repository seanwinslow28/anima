from PIL import Image

def find_dither(path):
    img = Image.open(path)
    width, height = img.size
    
    TARGETS = {
        'primary_orange': (232, 155, 107),
        'warm_brown_shadow': (168, 107, 69)
    }
    TOLS = {
        'primary_orange': 10,
        'warm_brown_shadow': 6
    }
    
    # We want to find any columns/rows that alternate between orange and shadow.
    # Specifically, look for single isolated warm brown shadow pixels in orange areas.
    isolated_shadows = 0
    bg_ref = (247, 248, 242)
    
    for y in range(2, height - 2):
        for x in range(2, width - 2):
            p = img.getpixel((x, y))[:3]
            # Is it warm brown shadow?
            is_shadow = abs(p[0] - TARGETS['warm_brown_shadow'][0]) <= TOLS['warm_brown_shadow'] and \
                        abs(p[1] - TARGETS['warm_brown_shadow'][1]) <= TOLS['warm_brown_shadow'] and \
                        abs(p[2] - TARGETS['warm_brown_shadow'][2]) <= TOLS['warm_brown_shadow']
            if is_shadow:
                # Check if it has orange neighbors above and below
                p_above = img.getpixel((x, y-1))[:3]
                p_below = img.getpixel((x, y+1))[:3]
                
                is_orange_above = abs(p_above[0] - TARGETS['primary_orange'][0]) <= TOLS['primary_orange'] and \
                                  abs(p_above[1] - TARGETS['primary_orange'][1]) <= TOLS['primary_orange'] and \
                                  abs(p_above[2] - TARGETS['primary_orange'][2]) <= TOLS['primary_orange']
                is_orange_below = abs(p_below[0] - TARGETS['primary_orange'][0]) <= TOLS['primary_orange'] and \
                                  abs(p_below[1] - TARGETS['primary_orange'][1]) <= TOLS['primary_orange'] and \
                                  abs(p_below[2] - TARGETS['primary_orange'][2]) <= TOLS['primary_orange']
                                  
                if is_orange_above and is_orange_below:
                    isolated_shadows += 1
                    if isolated_shadows <= 10:
                        print(f"Isolated shadow pixel at x={x}, y={y}")
                        
    print(f"Total isolated shadow pixels (vertical dither candidates): {isolated_shadows}")

if __name__ == '__main__':
    find_dither('body-3quarter.png')
