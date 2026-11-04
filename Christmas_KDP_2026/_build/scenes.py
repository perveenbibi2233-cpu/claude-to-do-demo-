"""Scene compositions. Each function returns an SVG body for a 2588 x 2625 canvas.
Text zones (kept free of key art): TOP = y 170..830, BOTTOM = y 1800..2460."""
from art import *

W, H = 2588, 2625
CREAM = "#FBF4E6"


def night(seed=1, star_n=140, moon_xy=None, ymax=None, avoid=None):
    b = sky(W, H) + stars(W, H, star_n, seed=seed, ymax=ymax or H * 0.55, avoid=avoid)
    if moon_xy:
        b += moon(*moon_xy)
    return b


def snow_ground(y, seed=1, night_=True):
    fill = "url(#snowNight)" if night_ else "url(#snowG)"
    return hill(W, y, 40, fill, seed=seed, waves=2)


def burrow_room(lamp_x=1950, lamp_y=1150, window=None):
    """Cosy underground room."""
    b = f'<rect width="{W}" height="{H}" fill="url(#burrowG)"/>'
    b += f'<ellipse cx="{W/2}" cy="{H*0.82}" rx="{W*0.62}" ry="{H*0.48}" fill="#B98A5E"/>'
    b += f'<ellipse cx="{W/2}" cy="{H*0.88}" rx="{W*0.55}" ry="{H*0.38}" fill="#C99C6E"/>'
    rnd = random.Random(9)
    for _ in range(30):  # roots & pebbles in walls
        x, y = rnd.uniform(0, W), rnd.uniform(880, 1150)
        b += f'<path d="M{x:.0f},{y:.0f} q{rnd.uniform(-80,80):.0f},{rnd.uniform(40,120):.0f} {rnd.uniform(-60,60):.0f},{rnd.uniform(120,220):.0f}" stroke="#5E3B24" stroke-width="{rnd.uniform(6,14):.0f}" fill="none" stroke-linecap="round" opacity="0.6"/>'
    b += f'<rect x="0" y="{H*0.86}" width="{W}" height="{H*0.14}" fill="#8F6440"/>'
    b += f'<path d="M0,{H*0.86} Q{W/2},{H*0.83} {W},{H*0.86}" stroke="#7A5233" stroke-width="16" fill="none"/>'
    # rug
    b += f'<ellipse cx="{W/2}" cy="{H*0.9}" rx="{W*0.36}" ry="{H*0.05}" fill="#B8434A"/><ellipse cx="{W/2}" cy="{H*0.9}" rx="{W*0.3}" ry="{H*0.035}" fill="none" stroke="#F3D9A8" stroke-width="10" stroke-dasharray="26 18"/>'
    if window:
        wx, wy, wr, kind = window
        b += f'<circle cx="{wx}" cy="{wy}" r="{wr+26}" fill="#5E3B24"/>'
        if kind == "night":
            b += f'<circle cx="{wx}" cy="{wy}" r="{wr}" fill="#1C3566"/>'
            b += "".join(f'<circle cx="{wx+dx}" cy="{wy+dy}" r="7" fill="#fff"/>' for dx, dy in [(-60,-40),(40,-70),(70,20),(-20,30),(-80,60),(20,80)])
            b += f'<path d="M{wx-wr},{wy+wr*0.5} Q{wx},{wy+wr*0.2} {wx+wr},{wy+wr*0.5} L{wx+wr},{wy+wr} L{wx-wr},{wy+wr}Z" fill="#DCE7F8"/>'
        else:
            b += f'<circle cx="{wx}" cy="{wy}" r="{wr}" fill="#CFE3F6"/>'
            b += f'<path d="M{wx-wr},{wy+wr*0.4} Q{wx},{wy+wr*0.1} {wx+wr},{wy+wr*0.4} L{wx+wr},{wy+wr} L{wx-wr},{wy+wr}Z" fill="#FFFFFF"/>'
        b += f'<path d="M{wx-wr},{wy} L{wx+wr},{wy} M{wx},{wy-wr} L{wx},{wy+wr}" stroke="#5E3B24" stroke-width="16"/>'
    # lantern
    b += f'<circle cx="{lamp_x}" cy="{lamp_y}" r="520" fill="url(#warmglow)"/>'
    b += f'<path d="M{lamp_x},{lamp_y-200} L{lamp_x},{lamp_y-110}" stroke="#4A2E20" stroke-width="10"/>'
    b += f'<rect x="{lamp_x-55}" y="{lamp_y-110}" width="110" height="150" rx="20" fill="{P["window_hot"]}" stroke="#4A2E20" stroke-width="12"/>'
    b += f'<path d="M{lamp_x-70},{lamp_y-110} L{lamp_x+70},{lamp_y-110} L{lamp_x},{lamp_y-160}Z" fill="#4A2E20"/>'
    return b


def leaf_bed(x, y, w=900):
    rnd = random.Random(int(x))
    b = f'<ellipse cx="{x}" cy="{y}" rx="{w/2}" ry="{w*0.13}" fill="#8A5A36"/>'
    cols = ["#D9822B", "#C2552B", "#E3A33B", "#A8452A", "#C98A3A"]
    for _ in range(60):
        lx, ly = x + rnd.uniform(-w * 0.45, w * 0.45), y + rnd.uniform(-w * 0.1, w * 0.06)
        b += f'<ellipse cx="{lx:.0f}" cy="{ly:.0f}" rx="{rnd.uniform(26,46):.0f}" ry="{rnd.uniform(12,20):.0f}" fill="{rnd.choice(cols)}" transform="rotate({rnd.uniform(-40,40):.0f} {lx:.0f} {ly:.0f})"/>'
    return b


def yarn(x, y, r=70):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{P["scarf"]}"/>'
            f'<path d="M{x-r*0.8},{y-r*0.3} Q{x},{y-r*0.9} {x+r*0.7},{y-r*0.4} M{x-r*0.9},{y+r*0.1} Q{x},{y-r*0.4} {x+r*0.9},{y+r*0.1} M{x-r*0.6},{y+r*0.6} Q{x},{y+r*0.1} {x+r*0.7},{y+r*0.5}" stroke="{P["scarf_dark"]}" stroke-width="8" fill="none"/>')


def motion(x, y, n=3, length=220, gap=60, color="#FFFFFF", op=0.6):
    return "".join(f'<path d="M{x},{y+i*gap} L{x-length+i*40},{y+i*gap}" stroke="{color}" stroke-width="12" stroke-linecap="round" opacity="{op}"/>' for i in range(n))


def sparkles(cx, cy, n=12, r=300, seed=2, size=1.0):
    rnd = random.Random(seed)
    o = ""
    for _ in range(n):
        a, d = rnd.uniform(0, 6.28), rnd.uniform(0.3, 1) * r
        s = rnd.uniform(8, 22) * size
        o += f'<path d="{star_path(cx+d*math.cos(a), cy+d*math.sin(a), s*2.2, s*0.55, n=4, rot=0)}" fill="#FFF3B0" opacity="{rnd.uniform(.6,1):.2f}"/>'
    return o


def notes(x, y, seed=1):
    rnd = random.Random(seed)
    o = ""
    for i in range(5):
        nx, ny = x + i * 120 + rnd.uniform(-20, 20), y - i * 70 + rnd.uniform(-30, 30)
        o += f'<g transform="translate({nx:.0f},{ny:.0f}) rotate({rnd.uniform(-15,15):.0f})"><ellipse cx="0" cy="0" rx="26" ry="20" fill="#FFF3C4"/><path d="M22,-4 L22,-90 Q50,-70 56,-50" stroke="#FFF3C4" stroke-width="9" fill="none"/></g>'
    return o


# ===================================================================== FRONT MATTER
def cream():
    return f'<rect width="{W}" height="{H}" fill="{CREAM}"/>'


def fm_belongs():
    b = cream()
    b += f'<circle cx="{W/2}" cy="1180" r="560" fill="#E9EEF8"/>'
    b += snowflakes(W, H, 30, seed=3, ymin=700, ymax=1700, size=1.4).replace('fill="#fff"', 'fill="#C9D8EE"')
    b += g(W / 2, 1180, 2.0, body=glimmer(glow=0.9))
    b += holly_sprig(W / 2 - 520, 1650, 1.6, rot=-10) + holly_sprig(W / 2 + 520, 1650, 1.6, rot=10)
    return b


def fm_title():
    b = cream()
    b += f'<ellipse cx="{W/2}" cy="2050" rx="900" ry="120" fill="#E3EAF5"/>'
    b += g(W / 2 - 60, 2100, 1.35, body=hedgehog(arms="wave", mouth="grin", look=0.4))
    b += g(W / 2 + 420, 1350, 0.95, body=glimmer(glow=0.8))
    b += sparkles(W / 2 + 420, 1350, 10, 260, seed=4)
    return b


def fm_copyright():
    return cream() + holly_sprig(W / 2, 2130, 1.1)


def fm_dedication():
    b = cream()
    b += g(W / 2, 1720, 1.4, body=hedgehog_ball())
    b += g(W / 2 + 120, 1160, 0.55, body=glimmer(glow=0.7, wink=True))
    return b


def bm_talk():
    b = cream()
    b += g(2150, 2390, 1.5, body=robin())
    b += holly_sprig(420, 2330, 1.2, rot=-15)
    return b


def bm_author():
    b = cream()
    b += f'<path d="M1500,2400 L2400,2380" stroke="{P["bark"]}" stroke-width="50" stroke-linecap="round"/>'
    b += g(1950, 2380, 1.0, body=owl())
    b += holly_sprig(600, 2330, 1.0, rot=10)
    return b


def bm_goodnight():
    b = cream()
    b += f'<circle cx="{W/2}" cy="1250" r="700" fill="#E9EEF8"/>'
    b += g(W / 2, 1650, 1.6, body=hedgehog_ball())
    b += f'<path d="M{W/2-200},1640 q120,-40 300,10" stroke="{P["scarf"]}" stroke-width="44" fill="none" stroke-linecap="round"/>'
    b += g(W / 2 + 250, 880, 0.7, body=glimmer(glow=0.8, wink=True))
    return b


# ========================================================================= STORY
def s05():  # Juniper never saw Christmas: winter sleep
    b = burrow_room(lamp_x=2150, lamp_y=1250, window=(520, 1300, 220, "night"))
    b += leaf_bed(1250, 2080, 1100)
    b += g(1230, 2080, 1.25, body=hedgehog_ball())
    b += g(2050, 2250, 0.95, body=hedgehog(grandma=True, arms="hold", eyes="sleepy", mouth="small", look=-0.6))
    b += yarn(1820, 2260, 60)
    for i in range(4):
        b += f'<text x="{1500+i*90}" y="{1720-i*90}" font-family="Fredoka, sans-serif" font-size="{70+i*24}" fill="#FFF3DA" opacity="0.85">z</text>'
    return b


def s06():  # Spring: Grandma describes Christmas
    b = sky(W, H, "#BFE3F7", "#DDF0F8", "#F3F8EA")
    b += f'<circle cx="2250" cy="420" r="150" fill="#FFF3B5"/><circle cx="2250" cy="420" r="300" fill="url(#glow)" opacity="0.5"/>'
    b += hill(W, 1600, 60, "#A8D58A", seed=2) + hill(W, 1800, 50, "#8CC673", seed=5)
    rnd = random.Random(6)
    for _ in range(60):
        x, y = rnd.uniform(0, W), rnd.uniform(1850, 2600)
        c = rnd.choice(["#FFFFFF", "#FFD24A", "#F49AC1", "#B9A3E3"])
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="16" fill="{c}"/><circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="#F2B233"/>'
    # thought bubble with Christmas village
    b += f'<circle cx="1000" cy="1720" r="30" fill="#fff"/><circle cx="1080" cy="1600" r="45" fill="#fff"/>'
    b += f'<ellipse cx="1300" cy="1260" rx="560" ry="330" fill="#fff"/>'
    b += f'<clipPath id="bub"><ellipse cx="1300" cy="1260" rx="530" ry="300"/></clipPath>'
    inner = f'<rect x="760" y="950" width="1100" height="640" fill="#1C3566"/>' + stars(W, H, 50, seed=8).replace("<circle", "<circle opacity='1'")
    inner += hill(W, 1480, 20, "#DCE7F8", seed=3)
    inner += "".join(house(820 + i * 300, 1480, 220, 170, lit=True, roof=r, wreath=True) for i, r in enumerate(["#7B3B33", "#3E5A7A", "#5E7A4A", "#6B3F63"]))
    inner += g(1300, 1080, 0.5, body=glimmer(glow=0.9))
    b += f'<g clip-path="url(#bub)">{inner}</g>'
    b += g(620, 2450, 0.95, body=hedgehog(arms="hold", eyes="wide", mouth="o", look=0.7, scarf=False))
    b += g(1900, 2450, 1.05, body=hedgehog(grandma=True, arms="up", mouth="grin", look=-0.6))
    return b


def s07():  # The scarf
    b = burrow_room(lamp_x=420, lamp_y=1150, window=(2150, 1200, 200, "night"))
    b += leaf_bed(1500, 2250, 1300)
    b += g(1680, 2290, 1.25, body=hedgehog(arms="hug", eyes="sleepy", mouth="o", look=-0.3))
    b += f'<path d="M1050,2200 Q1500,2000 2150,2200 L2160,2330 Q1500,2420 1040,2330Z" fill="#C2552B" opacity="0.9"/>'
    b += g(820, 2300, 1.1, body=hedgehog(grandma=True, arms="hold", eyes="closed", mouth="smile", look=0.6))
    return b


def s08():  # THUMP
    b = night(seed=3, star_n=160)
    b += f'<path d="M2620,900 Q2000,1300 1700,2150" stroke="url(#glow)" stroke-width="160" fill="none" opacity="0.6"/>'
    b += f'<path d="M2620,900 Q2000,1300 1700,2150" stroke="#FFF1B0" stroke-width="18" fill="none" opacity="0.8" stroke-linecap="round"/>'
    b += forest_row(W, 1950, 650, 7, seed=4, color="#173A2D")
    b += snow_ground(1900, seed=3)
    b += holly_tree_burrow(980, 2350, 0.95)
    b += g(1680, 2240, 0.75, body=glimmer(mood="surprised", glow=1.0))
    b += sparkles(1680, 2200, 16, 280, seed=8)
    b += snowflakes(W, H, 60, seed=9, ymin=900)
    return b


def s09():  # First snow, cold toes
    b = night(seed=4, star_n=110)
    b += forest_row(W, 1800, 700, 6, seed=7, color="#173A2D")
    b += snow_ground(1750, seed=5)
    b += holly_tree_burrow(500, 2300, 0.9, door_glow=True, door_open=True)
    b += f'<circle cx="2150" cy="2050" r="420" fill="url(#glow)" opacity="0.8"/>'
    b += g(1450, 2420, 1.15, body=hedgehog(arms="up", eyes="wide", mouth="o", look=0.3), rot=-6)
    b += f'<path d="M1240,2440 l-40,30 M1660,2440 l40,30 M1280,2470 l-30,40 M1620,2470 l30,40" stroke="#fff" stroke-width="12" stroke-linecap="round"/>'
    b += snowflakes(W, H, 140, seed=10, ymin=850, size=1.2)
    return b


def s10():  # Meet Glimmer, sad
    b = night(seed=5, star_n=120)
    b += snow_ground(1500, seed=7)
    b += f'<ellipse cx="1550" cy="2150" rx="360" ry="90" fill="#9DB4D6"/>'
    b += g(1550, 2050, 1.35, body=glimmer(mood="sad", glow=0.75))
    b += g(780, 2380, 1.2, body=hedgehog(arms="hold", eyes="wide", mouth="o", look=0.9))
    b += snowflakes(W, H, 70, seed=11, ymin=850)
    return b


def s11():  # Glimmer explains, dimming. Text BOTTOM.
    b = night(seed=6, star_n=150, ymax=1100)
    # empty spot in sky where Glimmer belongs
    b += f'<path d="{star_path(1950,420,110,55)}" fill="none" stroke="#FFF3C4" stroke-width="8" stroke-dasharray="20 18" opacity="0.7"/>'
    b += forest_row(W, 1500, 300, 12, seed=3, color="#173A2D")
    b += village(W, 1520, scale=0.55, lit=0.0, seed=4)
    b += hill(W, 1560, 25, "url(#snowNight)", seed=9)
    b += g(1300, 1150, 1.05, body=glimmer(mood="sad", glow=0.45, pale=True))
    b += g(620, 1700, 0.85, body=hedgehog(arms="hold", eyes="wide", mouth="worried", look=0.6))
    return b


def s12():  # The promise
    b = night(seed=7, star_n=120)
    b += forest_row(W, 1700, 600, 6, seed=9, color="#173A2D")
    b += snow_ground(1650, seed=2)
    b += g(1290, 2420, 1.45, body=hedgehog(arms="up", mouth="grin", look=0.0))
    b += g(1290, 1250, 0.85, body=glimmer(mood="happy", glow=0.6, pale=True))
    b += sparkles(1290, 1250, 10, 260, seed=12)
    b += snowflakes(W, H, 60, seed=12, ymin=900)
    return b


def s13():  # Pincushion ride
    b = night(seed=8, star_n=110)
    b += forest_row(W, 1750, 520, 7, seed=11, color="#173A2D")
    b += snow_ground(1700, seed=4)
    b += g(1290, 2460, 1.5, body=hedgehog(arms="down", mouth="grin", look=-0.5))
    b += g(1530, 1580, 0.7, body=glimmer(mood="happy", glow=0.7), rot=15)
    b += snowflakes(W, H, 70, seed=13, ymin=900)
    return b


def s14():  # Climbing the holly tree. Text BOTTOM.
    b = night(seed=9, star_n=180, ymax=900)
    b += moon(500, 300, 120)
    b += hill(W, 1750, 30, "url(#snowNight)", seed=1)
    b += holly_tree_burrow(1450, 1820, 1.05)
    b += branch(1180, 1250, 820, 1180, w=55)
    b += g(930, 1180, 0.55, body=hedgehog(arms="hug", eyes="wide", mouth="worried", look=-0.4))
    b += g(870, 980, 0.3, body=glimmer(glow=0.5, pale=True, mood="surprised"))
    return b


def s15():  # Ruby flaps, plop into snowdrift
    b = night(seed=10, star_n=120)
    b += forest_row(W, 1800, 560, 6, seed=14, color="#173A2D")
    b += snow_ground(1760, seed=6)
    # upside-down Juniper in snowdrift: just feet + spikes + scarf tail sticking out
    b += g(1350, 1720, 1.1, body=hedgehog(arms="up", eyes="closed", mouth="o"), rot=180)
    b += f'<ellipse cx="1350" cy="2330" rx="700" ry="330" fill="#EEF4FF"/><ellipse cx="1350" cy="2240" rx="560" ry="190" fill="#FFFFFF"/>'
    b += snowflakes(W, H, 40, seed=15, ymin=1500, ymax=1950, size=2.0)
    b += g(1750, 1500, 0.9, body=robin(pose="fly"), flip=True)
    b += g(980, 1900, 0.6, body=glimmer(mood="surprised", glow=0.55, pale=True))
    return b


def s16():  # Ember ride
    b = night(seed=11, star_n=120, moon_xy=(2150, 1100, 180))
    b += hill(W, 1500, 120, "#7F98C0", seed=3) + hill(W, 1800, 60, "url(#snowNight)", seed=8)
    b += forest_row(W, 1560, 300, 9, seed=17, color="#1A3F30")
    b += g(1350, 2350, 1.35, body=fox(pose="run"))
    b += g(1300, 1960, 0.55, body=hedgehog(arms="hug", mouth="grin", look=0.6))
    b += g(1220, 1640, 0.32, body=glimmer(glow=0.55, pale=True))
    b += motion(620, 1900, 4, 320, 90)
    b += snowflakes(W, H, 40, seed=18, ymin=2200, ymax=2500, size=1.6)
    return b


def s17():  # Hilltop, village far below, Glimmer pale
    b = night(seed=12, star_n=200, ymax=1200)
    b += hill(W, 1650, 40, "#2B4372", seed=12)
    b += village(W, 1780, scale=0.45, lit=0.0, seed=11)
    b += hill(W, 1840, 20, "#9DB4D6", seed=15)
    b += f'<path d="M1400,{H} Q1700,1950 2100,1900 Q2450,1880 {W},1960 L{W},{H}Z" fill="url(#snowNight)"/>'
    b += g(2050, 2080, 0.7, body=fox(), flip=True)
    b += g(1700, 2160, 0.62, body=hedgehog(arms="hold", eyes="sleepy", mouth="worried", look=-0.3))
    b += g(1700, 2000, 0.4, body=glimmer(mood="sad", glow=0.25, pale=True))
    return b


def s18():  # Scarf wrap
    b = night(seed=13, star_n=110)
    b += hill(W, 1650, 40, "url(#snowNight)", seed=13)
    b += g(2250, 2000, 0.8, body=fox(eyes="closed"), flip=True)
    b += g(1100, 2450, 1.45, body=hedgehog(arms="hug", scarf=False, mouth="smile", look=0.8))
    b += g(1650, 1820, 1.0, body=glimmer(mood="happy", glow=0.85, scarf=True))
    b += sparkles(1650, 1820, 10, 240, seed=18)
    return b


def s19():  # Oakley. Text BOTTOM.
    b = night(seed=14, star_n=140, moon_xy=(2150, 360, 140))
    b += branch(-50, 820, 1250, 900, w=70)
    b += g(800, 860, 1.05, body=owl())
    b += hill(W, 1680, 30, "url(#snowNight)", seed=14)
    b += g(1650, 1760, 0.6, body=fox(), flip=True)
    b += g(1950, 1760, 0.55, body=hedgehog(arms="hold", scarf=False, eyes="wide", mouth="o", look=-0.8))
    b += g(1950, 1500, 0.4, body=glimmer(glow=0.6, scarf=True, mood="surprised"))
    return b


def s20():  # Roll down the hill
    b = night(seed=15, star_n=120)
    b += hill(W, 1500, 30, "#2B4372", seed=4)
    b += village(W, 1600, scale=0.5, lit=0.0, seed=21)
    b += f'<path d="M0,1300 Q900,1500 1600,2100 Q1900,2350 {W},2400 L{W},{H} L0,{H}Z" fill="url(#snowNight)"/>'
    b += branch(-40, 1180, 520, 1150, w=40)
    b += g(300, 1160, 0.45, body=owl())
    b += g(380, 960, 0.3, body=glimmer(glow=0.45, scarf=True))
    b += g(1420, 2120, 0.9, body=hedgehog_ball(eyes="closed"), rot=40)
    b += f'<path d="M700,1600 Q1000,1750 1150,1900" stroke="#fff" stroke-width="14" stroke-dasharray="40 40" fill="none" opacity="0.7" stroke-linecap="round"/>'
    b += snowflakes(W, H, 30, seed=20, ymin=1900, ymax=2200, size=1.8)
    return b


def s21():  # Wake up the village
    b = night(seed=16, star_n=110)
    b += house(120, 2000, 820, 600, lit=False, roof="#3E5A7A", chimney=True)
    b += house(1300, 2000, 950, 620, lit=False, roof="#7B3B33", chimney=True)
    b += f'<rect x="0" y="1990" width="{W}" height="{H}" fill="url(#snowNight)"/>'
    b += g(1640, 1720, 0.6, body=robin(), flip=True)
    b += f'<text x="1520" y="1660" font-family="Fredoka, sans-serif" font-size="70" fill="#FFF3C4">tap!</text>'
    b += g(560, 2470, 0.62, body=fox())
    b += g(1300, 2470, 1.0, body=hedgehog(arms="up", scarf=False, mouth="grin"))
    b += notes(1450, 2100, seed=3)
    return b


def s22():  # Windows glow
    b = night(seed=17, star_n=120, ymax=900)
    b += village(W, 1620, scale=0.95, lit=1.0, seed=7, silhouettes=True)
    b += village(W + 200, 2080, scale=1.3, lit=1.0, seed=12, silhouettes=True)
    b += f'<rect x="0" y="2070" width="{W}" height="{H}" fill="url(#snowNight)"/>'
    b += g(1150, 2480, 0.5, body=hedgehog(arms="up", scarf=False, mouth="grin"))
    b += g(1500, 2480, 0.35, body=robin())
    b += g(700, 2500, 0.4, body=fox(), flip=True)
    return b


def s23():  # Glimmer rises. Text BOTTOM.
    b = night(seed=18, star_n=170, ymax=1500)
    b += forest_row(W, 1650, 380, 10, seed=21, color="#1A3F30")
    b += hill(W, 1680, 35, "url(#snowNight)", seed=18)
    b += branch(-40, 1560, 600, 1520, w=40)
    b += g(320, 1550, 0.42, body=owl())
    b += f'<circle cx="1500" cy="500" r="420" fill="url(#glow)"/>'
    b += scarf_ribbon(1500, 620, 1350, 1250, bend=-220)
    b += g(1500, 500, 1.15, body=glimmer(glow=1.4))
    b += sparkles(1450, 900, 26, 520, seed=30)
    return b


def s24():  # Midnight sleigh across the moon
    b = night(seed=19, star_n=110, ymax=1200)
    b += moon(1500, 1420, 400)
    b += sleigh(1080, 1470, 0.8)
    b += g(2230, 1150, 0.5, body=glimmer(glow=1.2, mood="happy"))
    b += hill(W, 2050, 25, "#2B4372", seed=19)
    b += village(W, 2150, scale=0.6, lit=1.0, seed=5)
    b += clock_tower(420, 2200, 0.85)
    b += f'<rect x="0" y="2160" width="{W}" height="{H}" fill="url(#snowNight)"/>'
    return b


def s25():  # So THIS is Christmas
    b = night(seed=20, star_n=160, ymax=1300)
    b += g(1950, 1000, 0.45, body=glimmer(glow=1.2))
    b += sleigh(800, 1150, 0.45, color="#5A6A9C")
    b += hill(W, 1650, 30, "#2B4372", seed=20)
    b += village(W, 1760, scale=0.5, lit=1.0, seed=31)
    b += f'<path d="M0,1900 Q1000,1800 {W},1950 L{W},{H} L0,{H}Z" fill="url(#snowNight)"/>'
    b += g(1250, 2420, 0.8, body=fox(eyes="closed", tail=False), flip=True)
    b += g(1700, 2440, 0.85, body=hedgehog(arms="hug", scarf=False, eyes="sleepy", mouth="smile", look=-0.4))
    b += g(1650, 2520, 0.95, body=fox_tail_curl())
    b += g(2030, 2300, 0.45, body=robin(), flip=True)
    return b


def s26():  # Morning: scarf returned with stardust
    b = burrow_room(lamp_x=2150, lamp_y=1100, window=(520, 1150, 220, "day"))
    b += leaf_bed(1300, 2250, 1200)
    b += g(1250, 2280, 1.2, body=hedgehog(arms="hold", scarf=False, eyes="wide", mouth="grin", look=0.2))
    b += f'<rect x="1080" y="1950" width="340" height="110" rx="20" fill="{P["scarf"]}"/><rect x="1180" y="1950" width="40" height="110" fill="{P["stripe"]}"/><rect x="1260" y="1950" width="40" height="110" fill="{P["stripe"]}"/>'
    b += f'<rect x="1290" y="1890" width="120" height="90" fill="#FFF8E8" stroke="#E2C27A" stroke-width="6" transform="rotate(8 1350 1935)"/>'
    b += f'<path d="{star_path(1350,1935,22,10)}" fill="{P["star"]}"/>'
    b += sparkles(1250, 1980, 22, 320, seed=40, size=0.9)
    b += g(2150, 2300, 0.9, body=hedgehog(grandma=True, arms="hold", eyes="closed", mouth="smile", look=-0.7))
    return b


def s27():  # Goodnight, little light (Glimmer winks). Text BOTTOM.
    b = night(seed=21, star_n=170, ymax=1300)
    b += g(1950, 520, 0.55, body=glimmer(glow=1.0, wink=True))
    b += sparkles(1950, 520, 8, 200, seed=41)
    b += hill(W, 1720, 30, "url(#snowNight)", seed=21)
    b += holly_tree_burrow(820, 1760, 0.75, door_glow=True, door_open=True)
    b += g(1150, 1760, 0.55, body=hedgehog(arms="wave", mouth="smile", look=0.8))
    return b


def s28():  # Asleep until spring (cross-section)
    b = night(seed=22, star_n=120, ymax=800)
    b += g(2250, 800, 0.4, body=glimmer(glow=1.0))
    b += f'<rect x="0" y="1150" width="{W}" height="{H}" fill="url(#burrowG)"/>'
    b += f'<path d="M0,1150 Q{W/2},1080 {W},1150 L{W},1270 Q{W/2},1220 0,1270Z" fill="#F4F8FF"/>'
    b += forest_row(W, 1160, 300, 8, seed=22, color="#1A3F30")
    b += f'<ellipse cx="{W/2}" cy="2050" rx="1000" ry="450" fill="#B98A5E"/>'
    b += f'<circle cx="2000" cy="1800" r="450" fill="url(#warmglow)" opacity="0.6"/>'
    b += leaf_bed(W / 2, 2280, 1300)
    b += g(1050, 2300, 1.0, body=hedgehog_ball(grandma=True))
    b += g(1600, 2300, 1.0, body=hedgehog_ball())
    b += f'<path d="M1400,2150 q100,-60 260,-40" stroke="{P["scarf"]}" stroke-width="44" fill="none" stroke-linecap="round"/>'
    return b


def s29():  # The End
    b = night(seed=23, star_n=200, ymax=1500)
    b += g(1294, 1180, 0.8, body=glimmer(glow=1.3))
    b += sparkles(1294, 1180, 18, 360, seed=50)
    b += hill(W, 1750, 40, "#2B4372", seed=23)
    b += village(W, 1880, scale=0.55, lit=1.0, seed=17)
    b += f'<path d="M0,1980 Q1200,1880 {W},2000 L{W},{H} L0,{H}Z" fill="url(#snowNight)"/>'
    b += holly_tree_burrow(2050, 2350, 0.5, door_glow=True)
    b += snowflakes(W, H, 80, seed=51, ymin=900)
    return b


SCENES = {k: v for k, v in globals().items() if callable(v) and (k.startswith("s") and k[1:].isdigit() or k.startswith(("fm_", "bm_")))}
