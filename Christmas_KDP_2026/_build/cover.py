"""Full-wrap cover artwork (back | spine | front) for KDP, 32 pages, premium colour."""
from art import *
from scenes import sparkles

DPI = 300
TRIM_W, TRIM_H, BLEED = 8.5, 8.5, 0.125
PAGES = 32
SPINE = round(PAGES * 0.002347, 4)            # KDP premium colour paper thickness/page
COVER_W_IN = BLEED + TRIM_W + SPINE + TRIM_W + BLEED
COVER_H_IN = BLEED + TRIM_H + BLEED
CW, CH = round(COVER_W_IN * DPI), round(COVER_H_IN * DPI)
FRONT_X0 = round((BLEED + TRIM_W + SPINE) * DPI)   # left edge of front panel (px)
BACK_X1 = round((BLEED + TRIM_W) * DPI)            # right edge of back panel (px)


def cover_body():
    b = sky(CW, CH) + stars(CW, CH, 320, seed=77, ymax=CH * 0.7)
    b += hill(CW, 1900, 40, "#2B4372", seed=7)
    b += village(CW, 2010, scale=0.5, lit=1.0, seed=9)
    b += f'<path d="M0,2120 Q{CW*0.3},2040 {CW*0.5},2110 Q{CW*0.75},2180 {CW},2080 L{CW},{CH} L0,{CH}Z" fill="url(#snowNight)"/>'
    # front: Juniper lifting Glimmer
    fx = FRONT_X0 + 1150
    b += f'<circle cx="{fx+420}" cy="1560" r="700" fill="url(#glow)" opacity="0.7"/>'
    b += g(fx, 2560, 1.45, body=hedgehog(arms="up", mouth="grin", look=0.6))
    b += g(fx + 430, 1600, 1.0, body=glimmer(glow=1.1))
    b += sparkles(fx + 430, 1600, 22, 420, seed=5)
    b += snowflakes(CW, CH, 160, seed=12, ymin=900)
    # back: Ember and Ruby, kept left of the barcode box
    b += g(1250, 2420, 0.75, body=fox(eyes="closed"))
    b += g(560, 2400, 0.55, body=robin())
    return b


def cover_svg():
    return svg_doc(CW, CH, cover_body())
