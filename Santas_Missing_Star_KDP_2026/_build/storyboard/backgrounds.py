"""Placeholder settings for the rough storyboard (drawn in code; NOT final art).
Each background deliberately leaves out that page's hidden-object types so the eventual counts stay clean.
Writes storyboard/bg_svg/<key>.svg; render with: node render.js bg_svg bg"""
import os
import random
from vec import (defs, grain, sky, stars, moon, snowflakes, hill, fir, forest_row, house, village, branch, star_path, P)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "bg_svg"); os.makedirs(OUT, exist_ok=True)
SW, SH = 2588, 1688
PW, PH = 1294, 1688


def doc(W, H, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'{defs()}<defs><filter id="soft2"><feGaussianBlur stdDeviation="6"/></filter><filter id="far"><feGaussianBlur stdDeviation="2.5"/></filter>'
            f'<filter id="aur"><feGaussianBlur stdDeviation="28"/></filter></defs>{body}{grain(W, H)}</svg>')


def snow_floor(W, H, y, col1="#EEF4FD", col2="#BFD0EA"):
    return (f'<defs><linearGradient id="sf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{col1}"/><stop offset="1" stop-color="{col2}"/></linearGradient></defs>'
            f'<path d="M0,{y} Q{W*.25},{y-H*.03} {W*.5},{y} T{W},{y-H*.01} L{W},{H} L0,{H}Z" fill="url(#sf)"/>')


def planks(x, y, w, h, base="#8A5A36", seed=1, vertical=True, n=None):
    rnd = random.Random(seed); o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{base}"/>']
    n = n or int((w if vertical else h) / 90)
    for i in range(n):
        if vertical:
            px = x + w * i / n
            o.append(f'<rect x="{px:.0f}" y="{y}" width="{w/n:.0f}" height="{h}" fill="#000" opacity="{rnd.uniform(0,.12):.2f}"/>'
                     f'<line x1="{px:.0f}" y1="{y}" x2="{px:.0f}" y2="{y+h}" stroke="#3A2416" stroke-width="4" opacity=".45"/>')
        else:
            py = y + h * i / n
            o.append(f'<rect x="{x}" y="{py:.0f}" width="{w}" height="{h/n:.0f}" fill="#000" opacity="{rnd.uniform(0,.12):.2f}"/>'
                     f'<line x1="{x}" y1="{py:.0f}" x2="{x+w}" y2="{py:.0f}" stroke="#3A2416" stroke-width="4" opacity=".45"/>')
    return "".join(o)


def floorboards(W, H, y, base="#A87445"):
    o = [f'<rect x="0" y="{y}" width="{W}" height="{H-y}" fill="{base}"/>']
    for i in range(-12, 13):
        o.append(f'<line x1="{W/2 + i*W*0.035:.0f}" y1="{y}" x2="{W/2 + i*W*0.16:.0f}" y2="{H}" stroke="#5A3A24" stroke-width="5" opacity=".45"/>')
    for k in range(1, 5):
        yy = y + (H - y) * (k / 5) ** 1.4
        o.append(f'<line x1="0" y1="{yy:.0f}" x2="{W}" y2="{yy:.0f}" stroke="#5A3A24" stroke-width="3" opacity=".25"/>')
    o.append(f'<rect x="0" y="{y-10}" width="{W}" height="20" fill="#4A2E1E" opacity=".55"/>')
    return "".join(o)


def window(x, y, w, h, night=True):
    sky_c = "#22356A" if night else "#BFD9F2"
    o = [f'<rect x="{x-14}" y="{y-14}" width="{w+28}" height="{h+28}" rx="10" fill="#5A3A24"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{sky_c}"/>',
         f'<path d="M{x},{y+h*.75} Q{x+w*.5},{y+h*.6} {x+w},{y+h*.75} L{x+w},{y+h} L{x},{y+h}Z" fill="#EEF4FD"/>']
    rnd = random.Random(int(x))
    for _ in range(14):
        o.append(f'<circle cx="{x+rnd.uniform(0,w):.0f}" cy="{y+rnd.uniform(0,h*.7):.0f}" r="{rnd.uniform(3,7):.0f}" fill="#fff" opacity=".85"/>')
    o.append(f'<path d="M{x+w/2},{y} V{y+h} M{x},{y+h/2} H{x+w}" stroke="#5A3A24" stroke-width="12"/>')
    o.append(f'<path d="M{x},{y} l{w*.25},{h*.12} M{x+w},{y} l{-w*.25},{h*.12}" stroke="#fff" stroke-width="10" opacity=".6"/>')
    return "".join(o)


def glow(x, y, r, op=.7, warm=True):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#{"warmglow" if warm else "glow"})" opacity="{op}"/>'


def xmas_tree(x, base, h, star=False, lights=True, seed=3):
    """Big Christmas tree with garland and warm white fairy lights (no baubles)."""
    rnd = random.Random(seed); o = []
    o.append(f'<rect x="{x-h*.05:.0f}" y="{base-h*.1:.0f}" width="{h*.1:.0f}" height="{h*.12:.0f}" fill="#5A3B28"/>')
    tiers = 6
    for t in range(tiers):
        top = base - h + h * t * 0.14
        bot = base - h * 0.08 - (tiers - 1 - t) * h * 0.1
        ww = h * 0.62 * (0.25 + 0.75 * (t + 1) / tiers)
        o.append(f'<path d="M{x},{top:.0f} L{x+ww/2:.0f},{bot:.0f} Q{x},{bot+h*.04:.0f} {x-ww/2:.0f},{bot:.0f}Z" fill="#1E5A3D"/>')
        o.append(f'<path d="M{x},{top:.0f} L{x+ww/2:.0f},{bot:.0f} Q{x+ww/4:.0f},{bot+h*.03:.0f} {x},{bot+h*.035:.0f}Z" fill="#143F2B" opacity=".6"/>')
        o.append(f'<path d="M{x-ww*.42:.0f},{bot-h*.03:.0f} Q{x},{bot+h*.03:.0f} {x+ww*.42:.0f},{bot-h*.05:.0f}" stroke="#E8C25A" stroke-width="{h*.008:.0f}" fill="none"/>')
        if lights:
            for _ in range(10):
                fx = rnd.uniform(-.4, .4) * ww; fy = rnd.uniform(top + h * .06, bot - h * .02)
                if abs(fx) < (fy - top) / (bot - top) * ww / 2:
                    o.append(f'<circle cx="{x+fx:.0f}" cy="{fy:.0f}" r="{h*.018:.0f}" fill="url(#glow)" opacity=".8"/><circle cx="{x+fx:.0f}" cy="{fy:.0f}" r="{h*.0055:.0f}" fill="#FFF6D0"/>')
    if star:
        o.append(f'<circle cx="{x}" cy="{base-h:.0f}" r="{h*.16:.0f}" fill="url(#glow)"/>')
        o.append(f'<path d="{star_path(x, base-h, h*.065, h*.03)}" fill="url(#starfill)" stroke="#F5A623" stroke-width="6" stroke-linejoin="round"/>')
    else:
        o.append(f'<circle cx="{x}" cy="{base-h+h*.01:.0f}" r="{h*.05:.0f}" fill="none" stroke="#FFF3C4" stroke-width="5" stroke-dasharray="10 10" opacity=".8"/>')
    return "".join(o)


def lamp_globe(x, base, h):
    return (f'<rect x="{x-6}" y="{base-h}" width="12" height="{h}" fill="#2B2B3A"/>{glow(x, base-h, h*.35)}'
            f'<circle cx="{x}" cy="{base-h}" r="{h*.07:.0f}" fill="#FFF3C4"/>')


# ------------------------------------------------------------------ scenes
def s01():
    W, H = SW, SH
    b = sky(W, H, "#1D2A5A", "#4E4A88", "#B88AA6") + stars(W, H, 90, seed=1, ymax=H * .45) + moon(W * .55, H * .16, 70)
    b += village(W, H * .66, scale=.55, lit=1, seed=4)
    b += xmas_tree(W * .80, H * .80, H * .68)
    b += snow_floor(W, H, H * .72) + snowflakes(W, H, 70, seed=2, size=.8)
    return doc(W, H, b)


def s02():
    W, H = SW, SH
    b = planks(0, 0, W, H * .72, "#8A5A36", seed=2)
    b += window(W * .33, H * .14, W * .09, H * .22)
    b += f'<rect x="{W*.78}" y="{H*.30}" width="{W*.16}" height="{H*.42}" fill="#7D4B32"/><rect x="{W*.80}" y="{H*.42}" width="{W*.12}" height="{H*.30}" fill="#2A1A12"/>'
    b += glow(W * .86, H * .62, 260) + f'<path d="M{W*.82},{H*.72} Q{W*.86},{H*.52} {W*.9},{H*.72}Z" fill="#FF9A3C"/><path d="M{W*.845},{H*.72} Q{W*.86},{H*.6} {W*.875},{H*.72}Z" fill="#FFE07A"/>'
    for sx, sy in [(W * .56, H * .22), (W * .56, H * .38)]:   # shelves with wooden blocks and spinning tops only
        b += f'<rect x="{sx}" y="{sy}" width="{W*.18}" height="14" fill="#5A3A24"/>'
        for k in range(5):
            c = ["#E0B04A", "#4F8FCB", "#6BB36B", "#E07A4A", "#B07ACB"][k]
            b += f'<rect x="{sx+20+k*W*.034:.0f}" y="{sy-60}" width="60" height="60" rx="6" fill="{c}"/>'
    b += floorboards(W, H, H * .72)
    b += f'<rect x="{W*.04}" y="{H*.60}" width="{W*.40}" height="{H*.05}" fill="#6B4228"/><rect x="{W*.06}" y="{H*.65}" width="20" height="{H*.12}" fill="#5A3A24"/><rect x="{W*.41}" y="{H*.65}" width="20" height="{H*.12}" fill="#5A3A24"/>'
    b += f'<path d="M{W*.10},{H*.585} l90,0 l0,-14 l-90,0Z" fill="#9A9AA6"/><rect x="{W*.18}" y="{H*.57}" width="70" height="30" rx="6" fill="#C0392B" opacity=".0"/>'
    return doc(W, H, b)


def s03():
    W, H = SW, SH
    b = sky(W, H, "#F4B6C8", "#FBD9E2", "#FFF1F4")
    rnd = random.Random(3); x = -60
    pastel = ["#F7A8C4", "#A8E0D2", "#FFD39A", "#C7B6F2", "#9FD3F5"]
    while x < W:
        w = rnd.uniform(300, 380); h = rnd.uniform(230, 300)
        b += house(x, H * .70, w, h, lit=True, roof=rnd.choice(pastel), wreath=False, chimney=True)
        x += w + rnd.uniform(60, 140)
    for gx in [W * .08, W * .30, W * .58, W * .70]:
        b += f'<ellipse cx="{gx}" cy="{H*.715}" rx="70" ry="45" fill="#7FD18B"/><ellipse cx="{gx+60}" cy="{H*.72}" rx="55" ry="38" fill="#F48FB1"/>'
    for lx in [W * .20, W * .50, W * .90]:
        b += f'<rect x="{lx-8}" y="{H*.42}" width="16" height="{H*.30}" fill="#F7F7F7"/><circle cx="{lx}" cy="{H*.42}" r="50" fill="#FF8FB0"/><circle cx="{lx}" cy="{H*.42}" r="28" fill="#FFD1E0"/>'
    b += snow_floor(W, H, H * .72, "#FFFFFF", "#F3DDE6")
    return doc(W, H, b)


def s04():
    W, H = SW, SH
    b = planks(0, 0, W, H * .72, "#6E4428", seed=4)
    for k in range(4):   # four stalls along the back wall
        sx = W * (0.06 + k * 0.235)
        b += f'<rect x="{sx}" y="{H*.36}" width="{W*.20}" height="{H*.36}" fill="#4A2E1E"/>'
        b += planks(sx, H * .52, W * .20, H * .20, "#9A6A40", seed=k + 9, vertical=False, n=4)
        b += f'<path d="M{sx},{H*.36} L{sx+W*.2},{H*.36}" stroke="#3A2416" stroke-width="14"/>'
    b += f'<rect x="{W*.60}" y="{H*.06}" width="{W*.12}" height="{H*.26}" fill="#22356A"/>' + snowflakes(W, H, 0)
    b += f'<rect x="{W*.60}" y="{H*.06}" width="{W*.12}" height="{H*.26}" fill="none" stroke="#3A2416" stroke-width="16"/>'
    b += glow(W * .30, H * .20, 180) + glow(W * .86, H * .20, 180)
    b += f'<rect x="0" y="{H*.72}" width="{W}" height="{H*.28}" fill="#D9B25E"/>'
    rnd = random.Random(7)
    for _ in range(220):
        x, y = rnd.uniform(0, W), rnd.uniform(H * .72, H)
        b += f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+rnd.uniform(-30,30):.0f}" y2="{y+rnd.uniform(-8,8):.0f}" stroke="#B58A3A" stroke-width="4" opacity=".7"/>'
    for hx in [W * .02, W * .47]:
        b += f'<rect x="{hx}" y="{H*.60}" width="{W*.08}" height="{H*.12}" rx="14" fill="#E8C468"/><path d="M{hx},{H*.64} h{W*.08} M{hx},{H*.68} h{W*.08}" stroke="#B58A3A" stroke-width="6"/>'
    return doc(W, H, b)


def s05():
    W, H = SW, SH
    b = sky(W, H, "#2E4A7C", "#6E8FC2", "#C7D7EE")
    b += f'<g filter="url(#far)">{forest_row(W, H*.62, H*.42, 14, seed=3, color="#3E6A78")}</g>'
    rnd = random.Random(5)
    for k in range(9):
        x = W * (k + rnd.uniform(.1, .9)) / 9
        b += f'<rect x="{x-22}" y="0" width="44" height="{H*.75}" fill="#F2F2EE"/>'
        for m in range(6):
            b += f'<rect x="{x-22}" y="{rnd.uniform(0,H*.7):.0f}" width="{rnd.uniform(15,40):.0f}" height="8" fill="#3A3A3A" opacity=".7"/>'
    b += forest_row(W, H * .74, H * .48, 6, seed=8, color="#1F4D3A")
    b += snow_floor(W, H, H * .72)
    b += f'<path d="M{W*.40},{H} Q{W*.48},{H*.82} {W*.62},{H*.74}" stroke="#D6E3F5" stroke-width="90" fill="none" opacity=".7"/>'
    return doc(W, H, b)


def s06():
    W, H = SW, SH
    b = f'<rect width="{W}" height="{H}" fill="#EAD3AE"/>'
    b += f'<path d="M0,0 L{W*.5},{-H*.1} L{W},0 L{W},{H*.18} L{W*.5},{H*.06} L0,{H*.18}Z" fill="#8A5A36"/>'
    for k in range(7):
        x = W * k / 6
        b += f'<line x1="{x}" y1="{H*.18 - abs(x-W/2)/(W/2)*0 :.0f}" x2="{W*.5}" y2="{-H*.1}" stroke="#6B4228" stroke-width="16" opacity=".6"/>'
    for sx in [W * .36, W * .56, W * .76]:   # shelves of plain unwrapped boxes
        b += f'<rect x="{sx}" y="{H*.24}" width="{W*.16}" height="{H*.48}" fill="#9A6A40"/>'
        for r in range(3):
            y = H * (0.36 + r * 0.12)
            b += f'<rect x="{sx}" y="{y}" width="{W*.16}" height="14" fill="#6B4228"/>'
            for k in range(3):
                b += f'<rect x="{sx+18+k*W*.05:.0f}" y="{y-H*.07:.0f}" width="{W*.04:.0f}" height="{H*.07:.0f}" fill="#C9A06A" stroke="#8A6A40" stroke-width="3"/>'
    for i, c in enumerate(["#D94A4A", "#3E8E5A", "#3F6FC2", "#E8B84A"]):   # rolls of paper
        b += f'<rect x="{W*.05+i*70}" y="{H*.46}" width="56" height="{H*.26}" rx="24" fill="{c}"/>'
    b += f'<ellipse cx="{W*.92}" cy="{H*.66}" rx="{W*.05}" ry="{H*.10}" fill="#C8A878"/><ellipse cx="{W*.92}" cy="{H*.57}" rx="{W*.035}" ry="{H*.025}" fill="#A88858"/>'
    b += floorboards(W, H, H * .72, "#B5835A")
    return doc(W, H, b)


def s07():
    W, H = SW, SH
    b = f'<rect width="{W}" height="{H*.72}" fill="#B5653A"/>'
    for r in range(int(H * .72 / 60)):
        y = r * 60; off = 0 if r % 2 else 60
        b += f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#8A4528" stroke-width="5"/>'
        for x in range(-off, W, 120):
            b += f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+60}" stroke="#8A4528" stroke-width="5"/>'
    b += window(W * .33, H * .12, W * .09, H * .22)
    ox, oy = W * .86, H * .72
    b += f'<path d="M{ox-W*.11},{oy} V{oy-H*.32} A{W*.11},{H*.2} 0 0 1 {ox+W*.11},{oy-H*.32} V{oy}Z" fill="#7A3A22"/>'
    b += glow(ox, oy - H * .15, 300) + f'<path d="M{ox-W*.06},{oy} V{oy-H*.2} A{W*.06},{H*.1} 0 0 1 {ox+W*.06},{oy-H*.2} V{oy}Z" fill="#FF8A2A"/>'
    b += f'<rect x="{W*.04}" y="{H*.58}" width="{W*.40}" height="{H*.14}" fill="#7A4A2E"/><rect x="{W*.04}" y="{H*.575}" width="{W*.40}" height="18" fill="#F3E6D2"/>'
    for k in range(5):   # loaves and pies only
        x = W * (.07 + k * .075)
        b += (f'<ellipse cx="{x}" cy="{H*.56}" rx="60" ry="32" fill="#D79A52"/><path d="M{x-35},{H*.55} l20,-12 M{x-5},{H*.55} l20,-12 M{x+25},{H*.55} l20,-12" stroke="#A86A2E" stroke-width="5"/>'
              if k % 2 == 0 else f'<ellipse cx="{x}" cy="{H*.565}" rx="64" ry="22" fill="#C96A3A"/><ellipse cx="{x}" cy="{H*.555}" rx="54" ry="14" fill="#E9A86A"/>')
    b += floorboards(W, H, H * .72, "#8C5A3C")
    return doc(W, H, b)


def s08():
    W, H = SW, SH
    b = sky(W, H, "#F2B39A", "#F9D6C2", "#FCEBDD")
    b += hill(W, H * .48, 40, "#C9B6D6", seed=2, H=H) + f'<g filter="url(#far)">{forest_row(W, H*.52, H*.20, 18, seed=4, color="#6F8F9A")}</g>'
    b += f'<ellipse cx="{W*.5}" cy="{H*.76}" rx="{W*.62}" ry="{H*.22}" fill="#BFE0F2"/>'
    b += f'<ellipse cx="{W*.5}" cy="{H*.76}" rx="{W*.55}" ry="{H*.17}" fill="#D7EEF9"/>'
    for k in range(6):
        b += f'<path d="M{W*(.15+k*.12)},{H*(.7+k%2*.06)} q120,-40 240,0" stroke="#fff" stroke-width="6" fill="none" opacity=".7"/>'
    b += f'<rect x="{W*.80}" y="{H*.63}" width="{W*.15}" height="26" fill="#8A5A36"/>' + "".join(f'<rect x="{W*(.81+k*.045):.0f}" y="{H*.63}" width="14" height="70" fill="#6B4228"/>' for k in range(3))
    b += f'<path d="M0,{H*.86} Q{W*.25},{H*.80} {W*.45},{H*.90} L{W*.45},{H} L0,{H}Z" fill="#F4F8FF"/><path d="M{W*.40},{H*.95} Q{W*.8},{H*.82} {W},{H*.86} L{W},{H} L{W*.40},{H}Z" fill="#F4F8FF"/>'
    b += forest_row(W, H * .64, H * .26, 5, seed=9, color="#2E6B4F")
    return doc(W, H, b)


def s09():
    W, H = SW, SH
    b = sky(W, H, "#2F4276", "#7A8CBC", "#C9D3EA")
    b += hill(W, H * .50, 60, "#9FB0D4", seed=3, H=H)
    b += f'<circle cx="{W*.88}" cy="{H*.36}" r="60" fill="#fff" opacity=".7" filter="url(#soft2)"/><circle cx="{W*.92}" cy="{H*.30}" r="44" fill="#fff" opacity=".6" filter="url(#soft2)"/>'
    b += f'<path d="M{W*.55},{H*.74} Q{W*.75},{H*.55} {W*.86},{H*.42}" stroke="#5A5A6A" stroke-width="10" fill="none"/><path d="M{W*.60},{H*.74} Q{W*.78},{H*.56} {W*.875},{H*.43}" stroke="#5A5A6A" stroke-width="10" fill="none"/>'
    b += f'<path d="M0,{H*.12} L{W*.47},{H*.12} L{W*.47},{H*.17} L0,{H*.17}Z" fill="#7B3B33"/><path d="M0,{H*.11} L{W*.47},{H*.11}" stroke="#F4F8FF" stroke-width="16"/>'
    for x in [W * .06, W * .24, W * .42]:
        b += f'<rect x="{x}" y="{H*.17}" width="22" height="{H*.55}" fill="#4A3A3A"/>'
    b += f'<circle cx="{W*.33}" cy="{H*.26}" r="70" fill="#F7F2E4" stroke="#3A2A20" stroke-width="12"/><path d="M{W*.33},{H*.26} v-48 M{W*.33},{H*.26} h34" stroke="#3A2A20" stroke-width="10" stroke-linecap="round"/>'
    b += f'<rect x="0" y="{H*.72}" width="{W}" height="{H*.28}" fill="#C9C1B3"/><rect x="0" y="{H*.72}" width="{W}" height="16" fill="#E8C25A"/>'
    b += f'<rect x="{W*.10}" y="{H*.60}" width="{W*.12}" height="20" rx="8" fill="#6B4228"/><rect x="{W*.11}" y="{H*.62}" width="12" height="{H*.1}" fill="#6B4228"/><rect x="{W*.20}" y="{H*.62}" width="12" height="{H*.1}" fill="#6B4228"/>'
    b += lamp_globe(W * .62, H * .72, H * .40)
    return doc(W, H, b)


def s10():
    W, H = SW, SH
    b = sky(W, H, "#081633", "#16335C", "#2B5480")   # no star dots: stars are a hidden-object target here
    for k, (col, y) in enumerate([("#5CFFB0", .14), ("#9F7BFF", .26), ("#5CFFD8", .36)]):
        b += f'<path d="M{-W*.1},{H*y} C{W*.25},{H*(y-.12)} {W*.5},{H*(y+.12)} {W*.75},{H*y} S{W*1.1},{H*(y-.08)} {W*1.1},{H*y}" stroke="{col}" stroke-width="{H*.07:.0f}" fill="none" opacity=".55" filter="url(#aur)"/>'
    b += village(W, H * .70, scale=.35, lit=1, seed=6)
    b += f'<path d="M0,{H*.74} Q{W*.35},{H*.56} {W*.62},{H*.66} Q{W*.85},{H*.72} {W},{H*.70} L{W},{H} L0,{H}Z" fill="url(#snowNight)"/>'
    for x, y, h in [(W * .52, H * .66, H * .34), (W * .70, H * .69, H * .30), (W * .86, H * .71, H * .26)]:   # exactly three pine trees
        b += fir(x, y, h, color="#1F4D3A")
    return doc(W, H, b)


def s11():
    W, H = SW, SH
    b = sky(W, H, "#18264E", "#3E5488", "#7487B8") + stars(W, H, 60, seed=11, ymax=H * .4)
    b += village(W, H * .64, scale=.5, lit=1, seed=12)
    b += xmas_tree(W * .82, H * .80, H * .66)
    b += f'<path d="M{W*.70},{H*.80} L{W*.76},{H*.26} M{W*.74},{H*.80} L{W*.80},{H*.26}" stroke="#8A5A36" stroke-width="12"/>' + "".join(f'<path d="M{W*(.70+k*.0063):.0f},{H*(.72-k*.08):.0f} l{W*.04:.0f},0" stroke="#8A5A36" stroke-width="10"/>' for k in range(6))
    b += fir(W * .48, H * .76, H * .52, color="#2E6B4F")
    b += snow_floor(W, H, H * .72) + snowflakes(W, H, 50, seed=13, size=.8)
    return doc(W, H, b)


def s12():
    W, H = SW, SH
    b = sky(W, H, "#1D2E58", "#4E66A0", "#8EA2CF") + stars(W, H, 50, seed=12, ymax=H * .5)
    b += f'<g filter="url(#far)">{village(W, H*.70, scale=.45, lit=1, seed=21)}</g>'
    b += snow_floor(W, H, H * .74)
    b += fir(W * .86, H * .96, H * 1.0, color="#1F5A3E")
    b += branch(W * 1.02, H * .36, W * .66, H * .42, w=46)
    nx, ny = W * .72, H * .40
    b += glow(nx, ny - 40, 260) + f'<path d="{star_path(nx+40, ny-60, 70, 32)}" fill="url(#starfill)" stroke="#F5A623" stroke-width="10" stroke-linejoin="round"/>'
    b += f'<ellipse cx="{nx}" cy="{ny}" rx="110" ry="40" fill="#7A5232"/><path d="M{nx-110},{ny} q110,40 220,0" stroke="#5A3A20" stroke-width="10" fill="none"/>'
    return doc(W, H, b)


def s13():
    W, H = SW, SH
    b = sky(W, H, "#101C44", "#2D4680", "#5B74AE") + stars(W, H, 80, seed=31, ymax=H * .5)
    b += village(W, H * .66, scale=.5, lit=1, seed=33)
    b += xmas_tree(W * .44, H * .82, H * .70, star=True)
    b += snow_floor(W, H, H * .72) + snowflakes(W, H, 80, seed=34, size=.8)
    return doc(W, H, b)


def p01():
    W, H = PW, PH
    b = sky(W, H, "#0D1A40", "#2F4680", "#5E77B0") + stars(W, H, 60, seed=41, ymax=H * .5)
    b += village(W, H * .70, scale=.45, lit=1, seed=42)
    b += xmas_tree(W * .5, H * .86, H * .52, star=True)
    b += snow_floor(W, H, H * .76) + snowflakes(W, H, 50, seed=43, size=.7)
    return doc(W, H, b)


def p32():
    W, H = PW, PH
    b = sky(W, H, "#0D1A40", "#2A4078", "#566EA8") + stars(W, H, 50, seed=51, ymax=H * .45) + moon(W * .78, H * .38, 60)
    b += village(W, H * .62, scale=.35, lit=1, seed=52) + xmas_tree(W * .30, H * .64, H * .30, star=True)
    b += snow_floor(W, H, H * .66) + lamp_globe(W * .9, H * .74, H * .36)
    b += f'<rect x="{W*.08}" y="{H*.70}" width="{W*.84}" height="22" rx="8" fill="#6B4228"/>'
    b += snowflakes(W, H, 40, seed=53, size=.7)
    return doc(W, H, b)


def s14():
    W = H = 990
    b = sky(W, H, "#F6E3C2", "#FBEFDC", "#FDF7EC")
    b += xmas_tree(W * .5, H * .78, H * .70, star=True, lights=True)
    b += snow_floor(W, H, H * .72, "#F3F6FC", "#D9E3F2")
    return doc(W, H, b)


SCENES = {"s01_missing_star": s01, "s02_toy_workshop": s02, "s03_candy_cane_village": s03, "s04_reindeer_stable": s04,
          "s05_snowflake_forest": s05, "s06_gift_room": s06, "s07_gingerbread_bakery": s07, "s08_frozen_ice_lake": s08,
          "s09_train_station": s09, "s10_northern_lights_hill": s10, "s11_tree_square": s11, "s12_goldies_secret": s12,
          "s13_celebration": s13, "p01_title": p01, "p32_goodnight": p32, "s14_spot_difference": s14}

if __name__ == "__main__":
    for k, f in SCENES.items():
        open(os.path.join(OUT, k + ".svg"), "w").write(f())
    print(len(SCENES), "background SVGs")
