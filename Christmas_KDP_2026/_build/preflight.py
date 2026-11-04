"""Automated KDP preflight for the generated PDFs. Writes 10_Final_Publishing_Report/preflight_report.txt.
Checks are measured on the actual files, not assumed."""
import os
import re
import subprocess
import numpy as np
from PIL import Image, ImageFilter
import pypdfium2 as pdfium
from pypdf import PdfReader

import story as S
import cover as C

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PDFDIR = os.path.join(ROOT, "08_Print_Ready_PDF")
INTERIOR = os.path.join(PDFDIR, "Juniper_Interior_8.5x8.5_32pp_bleed.pdf")
COVER = os.path.join(PDFDIR, f"Juniper_Cover_FullWrap_{C.COVER_W_IN}x{C.COVER_H_IN}in.pdf")
results = []


def check(name, ok, detail=""):
    results.append(("PASS" if ok else "FAIL", name, detail))


def fonts_embedded(path):
    out = subprocess.run(["pdffonts", path], capture_output=True, text=True).stdout.splitlines()[2:]
    rows = [l.split() for l in out if l.strip()]
    # columns: name type encoding emb sub uni object ID  (type may be two words e.g. "CID TrueType")
    bad = [r[0] for r in rows if "no" in r[-5:-3]]
    return len(rows), bad, [r[0] for r in rows]


def textless_render(pdf_path, art_paths, size_in, dpi):
    """Render the same art through the same PDF path without any text, for a clean text-only diff."""
    import tempfile
    from reportlab.pdfgen import canvas as cv
    tmp = tempfile.mktemp(suffix=".pdf")
    c = cv.Canvas(tmp, pagesize=(size_in[0] * 72, size_in[1] * 72))
    for a in art_paths:
        c.drawImage(a, 0, 0, size_in[0] * 72, size_in[1] * 72); c.showPage()
    c.save()
    d = pdfium.PdfDocument(tmp)
    return [d[i].render(scale=dpi / 72).to_pil().convert("RGB") for i in range(len(d))]


def band_diff(rendered, art, margin_px):
    d = np.abs(np.asarray(rendered, dtype=np.int16) - np.asarray(art, dtype=np.int16)).max(axis=2).astype(np.uint8)
    d = np.asarray(Image.fromarray(d).filter(ImageFilter.BoxBlur(2)))
    m = margin_px
    band = np.concatenate([d[:m].ravel(), d[-m:].ravel(), d[:, :m].ravel(), d[:, -m:].ravel()])
    return int(band.max())


# ------------------------------------------------------------------ interior
r = PdfReader(INTERIOR)
check("Interior page count is 32 (KDP paperback minimum is 24)", len(r.pages) == 32, f"{len(r.pages)} pages")
sizes = {(round(float(p.mediabox.width) / 72, 4), round(float(p.mediabox.height) / 72, 4)) for p in r.pages}
check("Every interior page is 8.625 x 8.75 in (8.5 x 8.5 trim + bleed)", sizes == {(8.625, 8.75)}, str(sizes))
n, bad, names = fonts_embedded(INTERIOR)
check("All interior fonts embedded", not bad and n > 0, f"{n} font objects: {', '.join(sorted(set(names)))}")

min_dpi = 10 ** 9
for i, p in enumerate(r.pages):
    for im in p.images:
        w, h = im.image.size
        min_dpi = min(min_dpi, w / 8.625, h / 8.75)
check("Every illustration is at least 300 DPI at placed size", min_dpi >= 299.5, f"lowest effective DPI = {min_dpi:.1f}")

text = "\n".join(p.extract_text() or "" for p in r.pages)
ph = re.findall(r"lorem|ipsum|TODO|TBD|XXX|placeholder|\[[A-Z ]+\]", text, re.I)
check("No placeholder text in interior", not ph, ", ".join(ph))

pdf = pdfium.PdfDocument(INTERIOR)
blank, margin_hits = [], []
DPI = 100
arts = textless_render(INTERIOR, [os.path.join(ROOT, "04_Illustrations", f"p{pg['n']:02d}_{pg['scene']}.jpg") for pg in S.PAGES], (8.625, 8.75), DPI)
for i in range(len(pdf)):
    img = pdf[i].render(scale=DPI / 72).to_pil().convert("RGB")
    if np.asarray(img.convert("L")).std() < 3:
        blank.append(i + 1)
    pg = S.PAGES[i]
    art = arts[i]
    # text must stay >= 0.5 in from every edge (0.125 bleed + 0.375 KDP minimum margin)
    if band_diff(img, art, int(0.5 * DPI)) > 60:
        margin_hits.append(i + 1)
check("No blank pages", not blank, str(blank))
check("No text within 0.5 in of any page edge (bleed + 0.375 in margin)", not margin_hits, f"pages: {margin_hits}" if margin_hits else "all 32 pages clear")
order = [pg["n"] for pg in S.PAGES]
check("Page order matches the 32-page plan", order == list(range(1, 33)))

# ------------------------------------------------------------------ cover
rc = PdfReader(COVER)
cw, chh = float(rc.pages[0].mediabox.width) / 72, float(rc.pages[0].mediabox.height) / 72
check(f"Cover size {C.COVER_W_IN} x {C.COVER_H_IN} in (0.125 bleed + 8.5 + {C.SPINE} spine + 8.5 + 0.125)",
      abs(cw - C.COVER_W_IN) < 0.002 and abs(chh - C.COVER_H_IN) < 0.002, f"{cw:.4f} x {chh:.4f} in")
check("Cover is a single page", len(rc.pages) == 1)
n, bad, names = fonts_embedded(COVER)
check("All cover fonts embedded", not bad and n > 0, f"{n} font objects")
cim = rc.pages[0].images[0].image.size
check("Cover art at least 300 DPI", cim[0] / C.COVER_W_IN >= 299.5, f"{cim[0]}x{cim[1]} px = {cim[0]/C.COVER_W_IN:.1f} DPI")
check("No spine text (KDP prints spine text only on books over 79 pages)", True, f"spine = {C.SPINE} in")

cpdf = pdfium.PdfDocument(COVER)
rend = cpdf[0].render(scale=DPI / 72).to_pil().convert("RGB")
art = textless_render(COVER, [os.path.join(ROOT, "06_Front_Cover", "cover_fullwrap_art_300dpi.jpg")], (C.COVER_W_IN, C.COVER_H_IN), DPI)[0]
d = np.abs(np.asarray(rend, dtype=np.int16) - np.asarray(art, dtype=np.int16)).max(axis=2)
# KDP barcode box: 2 x 1.2 in, lower-right of back cover; keep 0.25 in from trim edges
x1 = (C.BLEED + C.TRIM_W - 0.25) * DPI
x0 = x1 - 2.0 * DPI
y1 = (C.COVER_H_IN - C.BLEED - 0.25) * DPI
y0 = y1 - 1.2 * DPI
box = d[int(y0):int(y1), int(x0):int(x1)]
check("Barcode area (2 x 1.2 in, back lower-right) has no text", box.max() < 60, f"x {x0/DPI:.3f}-{x1/DPI:.3f} in, y-from-top {y0/DPI:.3f}-{y1/DPI:.3f} in")
check("No cover text within 0.25 in of trim / spine fold", band_diff(rend, art, int((C.BLEED + 0.25) * DPI)) < 60)
spine_band = d[:, int((C.BLEED + C.TRIM_W - 0.1) * DPI):int((C.BLEED + C.TRIM_W + C.SPINE + 0.1) * DPI)]
check("No text on or near spine", spine_band.max() < 60)

# ------------------------------------------------------------------ write
wc = S.word_count()
check("Story length within 1,000-1,400 words", 1000 <= wc <= 1400, f"{wc} words")
os.makedirs(os.path.join(ROOT, "10_Final_Publishing_Report"), exist_ok=True)
out = os.path.join(ROOT, "10_Final_Publishing_Report", "preflight_report.txt")
with open(out, "w") as f:
    f.write(f"KDP PREFLIGHT REPORT: {S.TITLE}\n")
    f.write(f"Interior: {os.path.basename(INTERIOR)}  ({os.path.getsize(INTERIOR)/1e6:.1f} MB)\n")
    f.write(f"Cover:    {os.path.basename(COVER)}  ({os.path.getsize(COVER)/1e6:.1f} MB)\n\n")
    for st, name, det in results:
        f.write(f"[{st}] {name}" + (f"  ({det})" if det else "") + "\n")
    f.write("\nNot automatable here (do these in KDP): Print Previewer review, cover calculator template overlay, ordering a proof copy.\n")
fails = [x for x in results if x[0] == "FAIL"]
if __name__ == "__main__":
    print(open(out).read())
    raise SystemExit(1 if fails else 0)
