from PIL import Image
from inspect_dither import inspect_dither
from find_dither_patterns import find_dither

print("=== Running inspect_dither ===")
inspect_dither('body-back.png')

print("\n=== Running find_dither ===")
find_dither('body-back.png')
