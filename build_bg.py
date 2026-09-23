"""Rebuild e6_bg.png from ref-measured geometry, 4x supersampled then downscaled,
so every diagonal/circular edge is properly anti-aliased.
All coordinates below are in final 600x194 card space, measured from the ref."""
from PIL import Image, ImageDraw

S = 4  # supersample factor
W, H = 600 * S, 194 * S

YELLOW = (255, 192, 27)   # #FFC01B
TEAL = (0, 63, 94)        # #003F5E
NAVY = (12, 40, 62)       # #0C283E
WHITE = (255, 255, 255)

def X(v): return v * S

img = Image.new('RGB', (W, H), WHITE)
d = ImageDraw.Draw(img)

def poly(points, fill):
    d.polygon([(X(x), X(y)) for x, y in points], fill=fill)

def rect(x0, y0, x1, y1, fill):
    d.rectangle([X(x0), X(y0), X(x1), X(y1)], fill=fill)

# 1. yellow wedge: triangle (0,13.8)-(81.6,103.3)-(0,187.2), apex hidden behind photo
poly([(0, 13.8), (81.6, 103.3), (0, 187.2)], YELLOW)

# 2. teal trapezoid under photo: top edge y165 (hidden mid-section behind photo),
#    flaring to (25,194)-(215,194)
poly([(44, 165), (203, 165), (215, 194), (25, 194)], TEAL)

# 3. yellow slash: thin slanted bar, centerline (214.5,163)->(224.5,194), width 2.5
poly([(213.2, 163), (215.7, 163), (223.2, 194), (220.7, 194)], YELLOW)

# 4. teal footer strip
rect(257, 165, 600, 194, TEAL)

# 5. white icon disks straddling the strip's top edge (d24)
for cx in (445.5, 481.5, 517.5, 552.5):
    d.ellipse([X(cx - 12), X(173 - 12), X(cx + 12), X(173 + 12)], fill=WHITE)

# 6. top-right teal bar
rect(459, 0, 553, 6, TEAL)

# 7. stripe tab: x554-600, y0-7, N/W/Y/W period 12 from x554
stripe_cols = [NAVY, WHITE, YELLOW, WHITE]
x = 554
i = 0
while x < 600:
    x1 = min(x + 3, 600)
    rect(x, 0, x1, 7, stripe_cols[i % 4])
    x = x1
    i += 1

# 8. divider
rect(254, 51, 257, 127, NAVY)

img = img.resize((600, 194), Image.LANCZOS)
img.save('slices/e6_bg.png')
print('wrote slices/e6_bg.png', img.size)
