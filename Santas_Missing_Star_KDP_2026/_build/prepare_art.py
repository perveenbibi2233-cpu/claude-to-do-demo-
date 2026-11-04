"""Turn the images you drop in 05_Art_Inbox/ into exact print-size JPEGs in 05_Art_Inbox/prepared/.
Also cuts every object out of the sticker sheets. Reports any image that would print below 300 DPI."""
import os, glob, json
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
import book as B

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
INBOX = os.path.join(ROOT, "05_Art_Inbox"); OUT = os.path.join(INBOX, "prepared"); os.makedirs(OUT, exist_ok=True)
report = []


def fit(src, size, name):
    im = Image.open(src).convert("RGB")
    tw, th = size
    r = tw / th
    w, h = im.size
    if w / h > r:   # too wide: crop sides
        nw = round(h * r); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:           # too tall: crop top/bottom
        nh = round(w / r); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    scale = tw / im.size[0]
    im = im.resize(size, Image.LANCZOS)
    im.save(os.path.join(OUT, name + ".jpg"), quality=94, dpi=(300, 300), subsampling=0)
    report.append((name, f"{w}x{h}", f"enlarged {scale:.2f}x", "OK" if scale <= 1.05 else "UPSCALE FIRST (prints soft)"))


for s in B.SPREADS:
    for ext in ("png", "jpg", "jpeg", "webp"):
        p = os.path.join(INBOX, "scenes", f"{s['key']}.{ext}")
        if os.path.exists(p):
            fit(p, B.SPREAD_PX, s["key"]); break
for key in ["p01_title", "p32_goodnight"]:
    for p in glob.glob(os.path.join(INBOX, "singles", key + ".*")):
        fit(p, B.PAGE_PX, key)
for p in glob.glob(os.path.join(INBOX, "singles", "s14_spot_difference.*")):
    fit(p, (1980, 1980), "s14_spot_difference")


def cut_stickers(sheet_path, prefix):
    """Split a white-background sticker sheet into separate RGBA cut-outs."""
    im = Image.open(sheet_path).convert("RGB"); a = np.asarray(im).astype(int)
    bg = (a.min(axis=2) > 235) & ((a.max(axis=2) - a.min(axis=2)) < 18)          # near-white, unsaturated
    fg = ndimage.binary_closing(~bg, iterations=3)
    fg = ndimage.binary_fill_holes(fg)
    lab, n = ndimage.label(fg)
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        hgt, wid = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        if hgt * wid < 0.002 * a.shape[0] * a.shape[1]:
            continue
        mask = Image.fromarray(((lab[sl] == i) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
        piece = im.crop((sl[1].start, sl[0].start, sl[1].stop, sl[0].stop)); piece.putalpha(mask)
        fn = f"{prefix}_{len(out) + 1:02d}.png"; piece.save(os.path.join(OUT, "stickers", fn)); out.append(fn)
    return out


os.makedirs(os.path.join(OUT, "stickers"), exist_ok=True)
cut = {}
for p in sorted(glob.glob(os.path.join(INBOX, "stickers", "*.*"))):
    k = os.path.splitext(os.path.basename(p))[0]
    cut[k] = cut_stickers(p, k)
json.dump(cut, open(os.path.join(OUT, "stickers", "index.json"), "w"), indent=1)

for r in report:
    print(" | ".join(r))
print("stickers cut:", {k: len(v) for k, v in cut.items()})
