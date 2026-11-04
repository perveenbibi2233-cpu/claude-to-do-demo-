"""Rough storyboard: the user's own character art (cut from their reference sheets) posed on soft scene-coloured
backgrounds, so the preview shows the cast on every page. Every image is badged "ROUGH LAYOUT" — this is NOT final art.
Output: storyboard/art/<key>.jpg, read by make_book.py via ART_DIR."""
import os
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
CUT = os.path.join(HERE, "cutouts"); OUT = os.path.join(HERE, "art"); os.makedirs(OUT, exist_ok=True)
FONT = os.path.join(HERE, "..", "fonts", "Fredoka-Bold.ttf")
SW, SH = 2588, 1688          # half print resolution: plenty for an on-screen preview
PW, PH = 1294, 1688

# palette per scene: sky top, sky bottom, ground, light colour, ground line (fraction of height)
BG = {
    "s01_missing_star":       ("#1f2c5c", "#8a76a8", "#e9eff9", "#ffd77a", 0.72),
    "s02_toy_workshop":       ("#6e4126", "#c98a52", "#8a5a36", "#ffcf7a", 0.70),
    "s03_candy_cane_village": ("#f3b8c6", "#fde8ee", "#ffffff", "#ff8fb0", 0.70),
    "s04_reindeer_stable":    ("#4f321f", "#a8743f", "#d9b25e", "#ffd27a", 0.70),
    "s05_snowflake_forest":   ("#3a5786", "#a8c0e2", "#f2f6fc", "#ffffff", 0.70),
    "s06_gift_room":          ("#e9cfa6", "#f7ead2", "#b5835a", "#ffe08a", 0.70),
    "s07_gingerbread_bakery": ("#a85a32", "#f2b878", "#8c5a3c", "#ffd08a", 0.70),
    "s08_frozen_ice_lake":    ("#f3bfa6", "#fbe6d4", "#cfe8f6", "#ffffff", 0.66),
    "s09_train_station":      ("#36487a", "#a0aed0", "#c9c1b3", "#ffd77a", 0.70),
    "s10_northern_lights_hill": ("#0b1838", "#24486e", "#dfe8f6", "#7dffb0", 0.72),
    "s11_tree_square":        ("#1b2852", "#5b6f9e", "#eef3fb", "#ffd77a", 0.72),
    "s12_goldies_secret":     ("#22345e", "#6a7fb0", "#eef3fb", "#ffe27a", 0.74),
    "s13_celebration":        ("#13214a", "#3f5b94", "#eef3fb", "#ffd77a", 0.72),
    "p01_title":              ("#0f1d44", "#4a5f95", "#eef3fb", "#ffd77a", 0.74),
    "p32_goodnight":          ("#0f1d44", "#3b5287", "#eef3fb", "#ffd77a", 0.74),
    "s14_spot_difference":    ("#f8e7c9", "#fdf4e3", "#e9eff9", "#ffd77a", 0.72),
}

# height ladder (fraction of canvas height) for a "standard" Pip
H_PIP = 0.36
SCALE = {"pip": 1.0, "mimi": 0.68, "tinsel": 1.0, "bramble": 1.15, "santa": 2.3}

# (cutout, x centre, feet y, size multiplier) as fractions of the canvas
CAST = {
    "s01_missing_star": [("mimi_front", .12, .93, 1), ("bramble_surprised", .22, .93, 1.0), ("tinsel_front", .32, .93, 1), ("pip_front", .41, .93, 1), ("santa", .65, .93, 0.95)],
    "s02_toy_workshop": [("pip_side", .20, .92, 1), ("mimi_curious", .33, .92, 1.1), ("bramble_front", .62, .92, 1), ("tinsel_side", .70, .80, 0.9)],
    "s03_candy_cane_village": [("bramble_happy", .18, .93, 1), ("tinsel_front", .32, .93, 1), ("pip_happy", .62, .93, 1), ("mimi_front", .70, .93, 1)],
    "s04_reindeer_stable": [("tinsel_side", .24, .93, 1.1), ("pip_front", .38, .93, 1), ("mimi_three_q", .62, .93, 1), ("bramble_front", .70, .93, 1)],
    "s05_snowflake_forest": [("mimi_curious", .22, .92, 1.2), ("pip_thinking", .36, .92, 1), ("bramble_excited", .62, .92, 1), ("tinsel_front", .70, .92, 1)],
    "s06_gift_room": [("bramble_surprised", .22, .93, 1), ("tinsel_front", .36, .93, 1), ("pip_front", .62, .93, 1), ("mimi_front", .70, .93, 1)],
    "s07_gingerbread_bakery": [("bramble_happy", .24, .93, 1.05), ("pip_surprised", .38, .93, 1), ("mimi_surprised", .62, .93, 1), ("tinsel_side", .70, .93, 1)],
    "s08_frozen_ice_lake": [("tinsel_side", .30, .93, 1), ("pip_happy", .62, .93, 1), ("mimi_happy", .69, .80, 1), ("bramble_happy", .40, .93, 1)],
    "s09_train_station": [("mimi_curious", .24, .93, 1.1), ("pip_side", .38, .93, 1), ("bramble_front", .62, .93, 1), ("tinsel_front", .70, .93, 1)],
    "s10_northern_lights_hill": [("mimi_front", .22, .93, 1), ("pip_front", .36, .93, 1), ("bramble_surprised", .62, .93, 1), ("tinsel_side", .70, .93, 1)],
    "s11_tree_square": [("pip_thinking", .24, .93, 1.05), ("mimi_curious", .37, .93, 1), ("bramble_front", .62, .93, 1), ("tinsel_front", .70, .93, 1)],
    "s12_goldies_secret": [("bramble_excited", .30, .94, 1.1), ("pip_happy", .30, .45, 0.85), ("mimi_front", .62, .94, 1), ("tinsel_front", .72, .94, 1)],
    "s13_celebration": [("santa", .26, .93, 1), ("pip_happy", .40, .55, 0.8), ("mimi_happy", .62, .93, 1), ("bramble_excited", .70, .93, 1), ("tinsel_front", .78, .80, 0.8)],
    "p01_title": [("santa", .74, .93, 0.62), ("bramble_front", .52, .95, 1.0), ("tinsel_front", .30, .96, 1.0), ("pip_hero", .50, .97, 0.95), ("mimi_front", .14, .97, 1.15)],
    "p32_goodnight": [("pip_happy", .45, .74, 1.3), ("mimi_happy", .24, .76, 1.6), ("bramble_happy", .70, .74, 1.3), ("tinsel_front", .88, .76, 1.2)],
    "s14_spot_difference": [("tinsel_front", .36, .90, 1.5), ("bramble_front", .80, .92, 1.45), ("mimi_front", .15, .93, 1.7), ("pip_front", .57, .94, 1.6)],
}
# search spreads: three friends on the left page, one on the right, clear of the "Can you find?" panel
for _k in ["s02_toy_workshop", "s03_candy_cane_village", "s04_reindeer_stable", "s05_snowflake_forest", "s06_gift_room",
           "s07_gingerbread_bakery", "s08_frozen_ice_lake", "s09_train_station", "s10_northern_lights_hill", "s11_tree_square"]:
    CAST[_k] = [(n, x, .93, m) for (n, _, _, m), x in zip(CAST[_k], [.13, .25, .37, .64])]
EMPTY_NOTE = {"s12_goldies_secret": "Goldie & the nest: art pending", "s13_celebration": "Goldie: art pending", "p01_title": "Goldie: art pending"}


def hexrgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def background(key, W, H):
    top, bot, ground, light, gy = BG[key]
    t, b = hexrgb(top), hexrgb(bot)
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        f = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(t[i] + (b[i] - t[i]) * f) for i in range(3)))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = ImageDraw.Draw(glow); rnd = random.Random(hash(key) & 0xffff)
    for _ in range(34):
        x, y, r = rnd.uniform(0, W), rnd.uniform(0, H * gy), rnd.uniform(H * 0.012, H * 0.035)
        g.ellipse((x - r, y - r, x + r, y + r), fill=hexrgb(light) + (rnd.randint(30, 60),))
    if key == "s10_northern_lights_hill":
        for k, col in enumerate([(90, 255, 170, 70), (170, 110, 255, 60)]):
            g.ellipse((-W * 0.2, H * (0.05 + k * 0.12), W * 1.2, H * (0.35 + k * 0.12)), outline=col, width=int(H * 0.06))
    glow = glow.filter(ImageFilter.GaussianBlur(H * 0.012))
    img = Image.alpha_composite(img.convert("RGBA"), glow)
    gr = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(gr)
    gd.ellipse((-W * 0.3, H * gy, W * 1.3, H * (gy + 0.8)), fill=hexrgb(ground) + (255,))
    gr = gr.filter(ImageFilter.GaussianBlur(H * 0.004))
    return Image.alpha_composite(img, gr)


def paste(canvas, name, x, y, mult):
    st = Image.open(os.path.join(CUT, name + ".png"))
    H = canvas.height
    kind = name.split("_")[0]
    full = name.endswith(("front", "side", "hero", "three_q")) or name == "santa"
    h = int(H * H_PIP * SCALE[kind] * mult * (1.0 if full else 0.8))
    st = st.resize((max(1, int(st.width * h / st.height)), h), Image.LANCZOS)
    sh = Image.new("RGBA", (st.width, max(4, h // 12)), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((st.width * .12, 0, st.width * .88, sh.height), fill=(0, 0, 0, 60))
    sh = sh.filter(ImageFilter.GaussianBlur(h // 40 + 1))
    cx, fy = int(x * canvas.width), int(y * H)
    canvas.alpha_composite(sh, (cx - st.width // 2, fy - sh.height // 2))
    canvas.alpha_composite(st, (cx - st.width // 2, fy - h))


def badge(canvas, xr, y, text):
    f = ImageFont.truetype(FONT, int(canvas.height * 0.022))
    d = ImageDraw.Draw(canvas); w = d.textlength(text, font=f); pad = canvas.height * 0.01
    x0 = xr - w - 2 * pad
    d.rounded_rectangle((x0, y, xr, y + f.size + 2 * pad), radius=int(pad * 1.5), fill=(255, 255, 255, 215), outline=(200, 60, 60, 255), width=3)
    d.text((x0 + pad, y + pad * 0.7), text, font=f, fill=(190, 40, 45))


def build(key, W, H, spread):
    c = background(key, W, H)
    for name, x, y, m in CAST[key]:
        paste(c, name, x, y, m)
    bt = H * 0.035
    if spread:
        badge(c, W * 0.455, bt, "ROUGH LAYOUT · not final art")
        badge(c, W * 0.955, bt, "ROUGH LAYOUT · not final art")
    elif key == "s14_spot_difference":
        badge(c, W * 0.97, H * 0.03, "ROUGH LAYOUT")
    else:
        badge(c, W * 0.93, H * 0.335, "ROUGH LAYOUT · not final art")
    if key in EMPTY_NOTE:
        f = ImageFont.truetype(FONT, int(H * 0.02)); d = ImageDraw.Draw(c)
        tx = W * (0.53 if spread else 0.05); ty = H * (0.60 if spread else 0.55)
        d.rounded_rectangle((tx, ty, tx + d.textlength(EMPTY_NOTE[key], font=f) + 30, ty + f.size + 22), radius=12, fill=(255, 248, 225, 230))
        d.text((tx + 15, ty + 9), EMPTY_NOTE[key], font=f, fill=(120, 90, 30))
    c.convert("RGB").save(os.path.join(OUT, key + ".jpg"), quality=88)


for k in CAST:
    if k == "s14_spot_difference":
        build(k, 990, 990, False)
    elif k.startswith("p"):
        build(k, PW, PH, False)
    else:
        build(k, SW, SH, True)
print(len(CAST), "storyboard images")
