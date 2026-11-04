"""Cut characters out of the supplied reference sheets (white background) for the rough storyboard preview."""
import os
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "..", "01_Character_Lock", "reference_sheets")
OUT = os.path.join(HERE, "cutouts"); os.makedirs(OUT, exist_ok=True)

# (sheet, crop box x0, y0, x1, y1)
CROPS = {
    "pip_hero":      ("Pip_fox.png", (0, 0, 610, 1010)),
    "pip_front":     ("Pip_fox.png", (615, 25, 890, 500)),
    "pip_side":      ("Pip_fox.png", (930, 25, 1305, 500)),
    "pip_happy":     ("Pip_fox.png", (590, 540, 925, 1010)),
    "pip_surprised": ("Pip_fox.png", (925, 540, 1235, 1010)),
    "pip_thinking":  ("Pip_fox.png", (1240, 540, 1536, 1010)),
    "mimi_hero":     ("Mimi_rabbit.png", (0, 150, 430, 1015)),
    "mimi_front":    ("Mimi_rabbit.png", (515, 385, 705, 690)),
    "mimi_three_q":  ("Mimi_rabbit.png", (1005, 385, 1195, 690)),
    "mimi_curious":  ("Mimi_rabbit.png", (420, 740, 610, 965)),
    "mimi_surprised":("Mimi_rabbit.png", (1105, 740, 1300, 965)),
    "mimi_happy":    ("Mimi_rabbit.png", (1320, 740, 1520, 965)),
    "bramble_hero":  ("Bramble_bear.png", (10, 140, 470, 785)),
    "bramble_front": ("Bramble_bear.png", (478, 75, 722, 470)),
    "bramble_happy": ("Bramble_bear.png", (420, 590, 630, 880)),
    "bramble_surprised": ("Bramble_bear.png", (640, 580, 812, 880)),
    "bramble_excited": ("Bramble_bear.png", (1000, 585, 1225, 880)),
    "tinsel_front":  ("Tinsel_reindeer.png", (468, 55, 728, 475)),
    "tinsel_side":   ("Tinsel_reindeer.png", (712, 55, 968, 475)),
    "santa":         ("Tinsel_reindeer_lineup_with_Santa.png", (652, 548, 928, 905)),
}
# Tinsel's nose is now rosy pink: recolour red pixels inside these nose boxes (sheet coordinates)
NOSES = {"tinsel_front": (365, 140, 430, 200), "tinsel_side": (540, 130, 595, 200)}


def cut(name, sheet, box):
    im = Image.open(os.path.join(REF, sheet)).convert("RGB").crop(box)
    a = np.asarray(im).astype(int)
    corner = np.median(np.concatenate([a[:4, :4].reshape(-1, 3), a[-4:, -4:].reshape(-1, 3), a[:4, -4:].reshape(-1, 3)]), axis=0)
    bgish = np.abs(a - corner).max(axis=2) <= 10
    if name == "santa":   # Santa stands on a cream panel inside the sheet
        panel = np.median(a[-12:-4, 20:60].reshape(-1, 3), axis=0)
        bgish |= np.abs(a - panel).max(axis=2) <= 12
    lab, n = ndimage.label(bgish)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge))
    fg = ndimage.binary_opening(~bg, iterations=1)
    lab2, n2 = ndimage.label(fg)
    if n2:
        sizes = ndimage.sum(fg, lab2, range(1, n2 + 1))
        fg = lab2 == (int(np.argmax(sizes)) + 1)          # keep only the character itself
    filled = ndimage.binary_fill_holes(fg)
    if not name.startswith("mimi"):   # reopen enclosed background gaps (between legs, under arms); Mimi's white fur is too close to the paper
        holes, nh = ndimage.label(filled & ~fg & bgish)
        for i in range(1, nh + 1):
            if (holes == i).sum() > 150:
                filled[holes == i] = False
    fg = filled
    alpha = Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))
    if name.startswith("tinsel"):
        # Tinsel's nose is now rosy pink: find the strict-red blob highest up (the collar sits lower) and recolour it
        arr = np.asarray(im).astype(float).copy()
        r, g_, b = arr[..., 0], arr[..., 1], arr[..., 2]
        red = (r > 160) & (g_ < 95) & (b < 105) & (np.abs(g_ - b) < 45)       # true red (fur has green well above blue)
        labr, nr = ndimage.label(ndimage.binary_dilation(red, iterations=2))
        blobs = [(ndimage.center_of_mass(labr == i)[0], i) for i in range(1, nr + 1) if (labr == i).sum() > 150]
        if blobs:
            nose = labr == min(blobs)[1]
            m = nose & (r - g_ > 60) & (r - b > 50)
            lum = (0.3 * r + 0.59 * g_ + 0.11 * b) / 255
            pink = np.stack([215 + 40 * lum, 110 + 110 * lum, 125 + 100 * lum], axis=-1)
            arr[m] = np.clip(pink[m], 0, 255)
            im = Image.fromarray(arr.astype(np.uint8))
    bb = alpha.getbbox()
    im = im.convert("RGBA"); im.putalpha(alpha)
    im.crop(bb).save(os.path.join(OUT, name + ".png"))


for k, (s, b) in CROPS.items():
    cut(k, s, b)
print(len(CROPS), "cut-outs")
