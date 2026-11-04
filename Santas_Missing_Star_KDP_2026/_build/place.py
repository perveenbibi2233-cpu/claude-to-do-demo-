"""Place hidden objects into a prepared scene and build its answer-key image.

Placements live in 05_Art_Inbox/placements/<scene_key>.json:
  [{"target": "teddy bears", "sticker": "sheet_A_toys_01.png", "x": 0.21, "y": 0.64, "h": 0.07, "rot": -8, "flip": false},
   {"target": "red noses", "painted": true, "x": 0.62, "y": 0.41, "r": 0.03}, ...]
x, y = centre as a fraction of the full spread (0..1, from the top-left); h = height as a fraction of the spread height.
"painted": true marks a target that is part of the artwork itself (only circled in the answer key).

Run: python3 place.py s02_toy_workshop   (or: python3 place.py all)
Refuses to write anything if a count is wrong or an object sits in the binding, a text panel or the trim margin."""
import os, sys, json
from PIL import Image, ImageDraw, ImageFilter, ImageStat, ImageEnhance
import book as B

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
PREP = os.path.join(ROOT, "05_Art_Inbox", "prepared"); PLC = os.path.join(ROOT, "05_Art_Inbox", "placements")
SW, SH = B.SPREAD_PX
IN = lambda inches: inches / (2 * B.TRIM_W + 2 * B.BLEED)        # inches -> fraction of spread width
INH = lambda inches: inches / B.PAGE_H
# keep-out zones (fractions of the spread): binding strip, story panel (left page), search panel (right page), trim margin
KEEP_OUT = {
    "binding": (0.5 - IN(0.75), 0.0, 0.5 + IN(0.75), 1.0),
    "story panel": (IN(0.125 + 0.6), INH(0.125 + 0.6), IN(0.125 + 0.75 + 4.85), INH(0.125 + 0.75 + 3.9)),
    "search panel": (1 - IN(0.125 + 0.75 + 3.85), 1 - INH(0.125 + 0.75 + 3.0), 1 - IN(0.6), 1 - INH(0.6)),
}
EDGE = (IN(0.125 + 0.35), INH(0.125 + 0.35))
COLOURS = ["#E53935", "#1E88E5", "#43A047", "#FB8C00", "#8E24AA"]


def check(scene, places):
    errs = []
    want = {t["name"]: t["n"] for t in scene["targets"]}
    got = {}
    for p in places:
        got[p["target"]] = got.get(p["target"], 0) + 1
        if p["target"] not in want:
            errs.append(f"unknown target {p['target']!r}")
        half = (p.get("h", 0.05) * SH / SW) / 2 if not p.get("painted") else p.get("r", 0.03)
        for zone, (x0, y0, x1, y1) in KEEP_OUT.items():
            if x0 - half < p["x"] < x1 + half and y0 - half < p["y"] < y1 + half and not (zone != "binding" and p.get("painted")):
                errs.append(f"{p['target']} at ({p['x']:.2f},{p['y']:.2f}) is inside the {zone}")
        if not (EDGE[0] < p["x"] < 1 - EDGE[0] and EDGE[1] < p["y"] < 1 - EDGE[1]):
            errs.append(f"{p['target']} at ({p['x']:.2f},{p['y']:.2f}) is too close to the trim")
    for k, n in want.items():
        if got.get(k, 0) != n:
            errs.append(f"{k}: need {n}, placed {got.get(k, 0)}")
    return errs


def paste(base, p):
    st = Image.open(os.path.join(PREP, "stickers", p["sticker"])).convert("RGBA")
    if p.get("flip"):
        st = st.transpose(Image.FLIP_LEFT_RIGHT)
    th = int(p["h"] * SH); st = st.resize((max(1, int(st.width * th / st.height)), th), Image.LANCZOS)
    if p.get("rot"):
        st = st.rotate(p["rot"], expand=True, resample=Image.BICUBIC)
    cx, cy = int(p["x"] * SW), int(p["y"] * SH)
    box = (cx - st.width // 2, cy - st.height // 2)
    # match local brightness gently so stickers sit in the scene's light
    region = base.crop((max(0, box[0]), max(0, box[1]), min(SW, box[0] + st.width), min(SH, box[1] + st.height))).convert("L")
    local = ImageStat.Stat(region).mean[0] / 255
    rgb = ImageEnhance.Brightness(st.convert("RGB")).enhance(0.8 + 0.25 * local); rgb.putalpha(st.split()[3]); st = rgb
    shadow = Image.new("RGBA", st.size, (0, 0, 0, 0)); a = st.split()[3].point(lambda v: int(v * 0.35))
    shadow.putalpha(a); shadow = shadow.filter(ImageFilter.GaussianBlur(max(2, th // 40)))
    base.alpha_composite(shadow, (box[0] + th // 30, box[1] + th // 25)); base.alpha_composite(st, box)
    return (box[0], box[1], box[0] + st.width, box[1] + st.height)


def run(key):
    scene = next(s for s in B.SPREADS if s["key"] == key)
    places = json.load(open(os.path.join(PLC, key + ".json")))
    errs = check(scene, places)
    if errs:
        print(f"{key}: NOT written\n  - " + "\n  - ".join(errs)); return False
    base_path = os.path.join(PREP, key + "_base.jpg")
    if not os.path.exists(base_path):
        os.replace(os.path.join(PREP, key + ".jpg"), base_path)       # keep the untouched scene once
    img = Image.open(base_path).convert("RGBA")
    boxes = []
    for p in places:
        if p.get("painted"):
            r = p.get("r", 0.03) * SW
            boxes.append((p, (p["x"] * SW - r, p["y"] * SH - r, p["x"] * SW + r, p["y"] * SH + r)))
        else:
            boxes.append((p, paste(img, p)))
    img.convert("RGB").save(os.path.join(PREP, key + ".jpg"), quality=94, dpi=(300, 300), subsampling=0)
    # answer-key image: same picture, smaller, with a coloured ring per target type
    ans = img.convert("RGB").resize((SW // 3, SH // 3), Image.LANCZOS); d = ImageDraw.Draw(ans)
    names = [t["name"] for t in scene["targets"]]
    for p, (x0, y0, x1, y1) in boxes:
        col = COLOURS[names.index(p["target"]) % len(COLOURS)]
        pad = 12
        d.ellipse((x0 / 3 - pad, y0 / 3 - pad, x1 / 3 + pad, y1 / 3 + pad), outline=col, width=9)
    ans.save(os.path.join(PREP, key + "_answers.jpg"), quality=90)
    json.dump({"colours": dict(zip(names, COLOURS)), "counts": {t["name"]: t["n"] for t in scene["targets"]}},
              open(os.path.join(PREP, key + "_answers.json"), "w"), indent=1)
    print(f"{key}: placed {sum(1 for p in places if not p.get('painted'))} objects, circled {len(places)} answers — counts verified")
    return True


if __name__ == "__main__":
    keys = [s["key"] for s in B.SPREADS if s.get("targets")] if sys.argv[1] == "all" else sys.argv[1:]
    ok = all([run(k) for k in keys if os.path.exists(os.path.join(PLC, k + ".json"))])
    sys.exit(0 if ok else 1)
