"""Build the KDP interior PDF and full-wrap cover PDF from rendered illustrations.

Interior: 32 pages, 8.5 x 8.5 in trim WITH bleed -> PDF page 8.625 x 8.75 in.
Cover:    full wrap, 32 pages premium colour -> 17.3251 x 8.75 in.
"""
import os
import sys
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import story as S
import cover as C

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PNG = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "png")
ILL = os.path.join(ROOT, "04_Illustrations")
OUT = os.path.join(ROOT, "08_Print_Ready_PDF")
F = os.path.join(HERE, "fonts")

for name, file in [("Andika", "Andika-Regular.ttf"), ("Andika-Bold", "Andika-Bold.ttf"),
                   ("Fredoka", "Fredoka-SemiBold.ttf"), ("Fredoka-Bold", "Fredoka-Bold.ttf"), ("Fredoka-Medium", "Fredoka-Medium.ttf")]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(F, file)))

PW, PH = 8.625 * inch, 8.75 * inch
SAFE_X = 0.8 * inch                       # >= 0.125 bleed + 0.375 gutter/outside margin, with room to spare
TOP_ZONE = (0.6 * inch, 2.95 * inch)      # distance from top edge (start, end) - matches scene art
BOTTOM_ZONE = (5.85 * inch, 8.2 * inch)
LIGHT, DARK = HexColor("#FFF8EC"), HexColor("#14213D")
RED, NAVY, BROWN = HexColor("#B8262F"), HexColor("#1C3566"), HexColor("#5A3B28")


def to_jpg(scene, label):
    """Save a 300-DPI print JPEG of the scene into 04_Illustrations and return its path."""
    os.makedirs(ILL, exist_ok=True)
    out = os.path.join(ILL, f"{label}.jpg")
    im = Image.open(os.path.join(PNG, f"{scene}.png")).convert("RGB")
    im.save(out, "JPEG", quality=94, dpi=(300, 300), subsampling=0)
    return out


def paras(text, size, color, font="Andika", align=TA_CENTER, leading=1.38):
    st = ParagraphStyle("t", fontName=font, fontSize=size, leading=size * leading, textColor=color,
                        alignment=align, spaceAfter=size * 0.55)
    out = []
    for p in text.split("\n\n"):
        p = p.replace("\n", "<br/>")
        if p.startswith("Thank you for lighting"):
            p = f'<font name="Fredoka-Medium">{p}</font>'
        out.append(Paragraph(p, st))
    return out


def draw_block(c, ps, x, w, y_top, y_bot, valign="center"):
    """Draw paragraphs between two distances-from-top; returns total height."""
    hs = [p.wrap(w, PH)[1] + p.style.spaceAfter for p in ps]
    total = sum(hs) - ps[-1].style.spaceAfter
    avail = y_bot - y_top
    y = PH - y_top - (max(0, (avail - total) / 2) if valign == "center" else 0)
    for p, h in zip(ps, hs):
        p.wrap(w, PH)
        y -= p.height
        p.drawOn(c, x, y)
        y -= p.style.spaceAfter
    return total


def fit(text, color, zone, w, start=16.5, minimum=16.5):
    size = start
    while size >= minimum:
        ps = paras(text, size, color)
        total = sum(p.wrap(w, PH)[1] + p.style.spaceAfter for p in ps) - ps[-1].style.spaceAfter
        if total <= zone[1] - zone[0]:
            return ps, size
        size -= 0.5
    raise SystemExit(f"Text does not fit: {text[:60]}")


def centred(c, text, font, size, y_from_top, color):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawCentredString(PW / 2, PH - y_from_top, text)


def interior():
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "Juniper_Interior_8.5x8.5_32pp_bleed.pdf")
    c = canvas.Canvas(path, pagesize=(PW, PH), initialFontName="Andika", initialFontSize=12)
    c.setTitle(f"{S.TITLE} - Interior")
    c.setAuthor(S.AUTHOR_NAME)
    w = PW - 2 * SAFE_X
    report = []
    for pg in S.PAGES:
        n = pg["n"]
        label = f"p{n:02d}_{pg['scene']}"
        img = to_jpg(pg["scene"], label)
        c.drawImage(img, 0, 0, PW, PH)
        kind = pg.get("kind", "art")
        if kind == "art" and pg.get("end"):
            centred(c, "The End", "Fredoka-Bold", 64, 1.75 * inch, LIGHT)
        elif kind == "art":
            zone = TOP_ZONE if pg["text_pos"] == "top" else BOTTOM_ZONE
            col = LIGHT if pg["text_color"] == "light" else DARK
            ps, size = fit(pg["text"], col, zone, w)
            draw_block(c, ps, SAFE_X, w, zone[0], zone[1])
            report.append((n, size))
        elif n == 1:
            centred(c, "This book belongs to", "Fredoka", 34, 1.7 * inch, NAVY)
            c.setStrokeColor(HexColor("#C9B79A")); c.setLineWidth(1.5)
            c.line(2.0 * inch, PH - 2.75 * inch, PW - 2.0 * inch, PH - 2.75 * inch)
            centred(c, "Merry Christmas!", "Fredoka-Medium", 22, 7.65 * inch, RED)
        elif n == 2:
            centred(c, "Juniper", "Fredoka-Bold", 74, 1.55 * inch, RED)
            centred(c, "and the Little Lost Star", "Fredoka-Bold", 40, 2.25 * inch, NAVY)
            centred(c, S.SUBTITLE, "Fredoka-Medium", 18, 2.75 * inch, BROWN)
            centred(c, S.AUTHOR_NAME, "Fredoka-Medium", 20, 8.1 * inch, NAVY)
        elif n == 3:
            txt = (f"{S.TITLE}<br/>Text and illustrations copyright © {S.YEAR} {S.AUTHOR_NAME}.<br/><br/>"
                   "All rights reserved. No part of this book may be reproduced, stored, or transmitted in any form or by any means "
                   "without written permission from the author, except for brief quotations in reviews.<br/><br/>"
                   "This is a work of fiction. Names, characters, places, and events are products of the author's imagination.<br/><br/>"
                   "Typeset in Andika and Fredoka (SIL Open Font License).<br/><br/>"
                   f"First edition, {S.YEAR}. Independently published.")
            st = ParagraphStyle("c", fontName="Andika", fontSize=10.5, leading=15, textColor=BROWN, alignment=TA_CENTER)
            p = Paragraph(txt, st)
            p.wrap(5.2 * inch, PH)
            p.drawOn(c, (PW - 5.2 * inch) / 2, PH - 2.2 * inch - p.height)
        elif n == 4:
            ps = paras(S.DEDICATION, 24, NAVY, font="Fredoka-Medium")
            draw_block(c, ps, SAFE_X, w, 1.2 * inch, 3.2 * inch)
        elif n == 30:
            centred(c, "Let's Talk About the Story", "Fredoka-Bold", 32, 1.25 * inch, RED)
            st = ParagraphStyle("q", fontName="Andika", fontSize=17, leading=24, textColor=NAVY, alignment=TA_LEFT,
                                spaceAfter=12, leftIndent=22, bulletIndent=0, bulletFontName="Andika-Bold", bulletColor=RED)
            ps = [Paragraph(q, st, bulletText="•") for q in S.TALK_QUESTIONS]
            draw_block(c, ps, 1.1 * inch, PW - 2.2 * inch, 1.75 * inch, 6.4 * inch, valign="top")
        elif n == 31:
            centred(c, "About the Author", "Fredoka-Bold", 32, 1.25 * inch, RED)
            ps = paras(S.AUTHOR_BIO, 17, NAVY)
            draw_block(c, ps, 1.2 * inch, PW - 2.4 * inch, 1.9 * inch, 5.6 * inch, valign="top")
        elif n == 32:
            centred(c, "Goodnight, little light.", "Fredoka-Medium", 38, 7.75 * inch, NAVY)
        c.showPage()
    c.save()
    return path, report


def cover_pdf():
    os.makedirs(OUT, exist_ok=True)
    W, H = C.COVER_W_IN * inch, C.COVER_H_IN * inch
    jpg = os.path.join(ROOT, "06_Front_Cover", "cover_fullwrap_art_300dpi.jpg")
    Image.open(os.path.join(PNG, "cover.png")).convert("RGB").save(jpg, "JPEG", quality=95, dpi=(300, 300), subsampling=0)
    path = os.path.join(OUT, f"Juniper_Cover_FullWrap_{C.COVER_W_IN}x{C.COVER_H_IN}in.pdf")
    c = canvas.Canvas(path, pagesize=(W, H), initialFontName="Andika", initialFontSize=12)
    c.setTitle(f"{S.TITLE} - Cover")
    c.setAuthor(S.AUTHOR_NAME)
    c.drawImage(jpg, 0, 0, W, H)
    fx0 = C.FRONT_X0 / C.DPI * inch
    fcx = fx0 + (C.TRIM_W * inch) / 2
    # title (fill + stroke for punch)
    def ttl(text, font, size, y_top, fill, stroke, sw):
        c.saveState()
        t = c.beginText()
        t.setFont(font, size)
        t.setTextRenderMode(2)
        c.setLineWidth(sw); c.setStrokeColor(stroke); c.setFillColor(fill)
        c.setLineJoin(1)
        tw = pdfmetrics.stringWidth(text, font, size)
        t.setTextOrigin(fcx - tw / 2, H - y_top)
        t.textLine(text)
        c.drawText(t)
        c.restoreState()
    ttl("Juniper", "Fredoka-Bold", 104, 1.55 * inch, HexColor("#FFF3D6"), HexColor("#9E1F2A"), 5)
    ttl("and the Little Lost Star", "Fredoka-Bold", 50, 2.35 * inch, HexColor("#FFD54A"), HexColor("#0A1736"), 3)
    c.setFillColor(HexColor("#FFF8EC")); c.setFont("Fredoka-Medium", 22)
    c.drawCentredString(fcx, H - 2.9 * inch, S.SUBTITLE)
    c.setFont("Fredoka-Medium", 21); c.setFillColor(HexColor("#FFD54A"))
    c.drawCentredString(fcx, H - 3.45 * inch, "by " + S.AUTHOR_NAME)
    # back cover blurb
    bx = C.BLEED * inch + 0.75 * inch
    bw = C.TRIM_W * inch - 1.5 * inch
    blurb = [
        "Juniper the hedgehog has slept through every Christmas of her life...",
        "...until a tiny star lands with a <b>THUMP</b> right outside her door.",
        "Glimmer has fallen from the sky, and if she isn't home by midnight, Santa won't find Hollyberry Village!",
        "With a brave heart, a brand-new scarf, and a little help from her friends, Juniper sets off to light the way home.",
        "A cozy, glowing Christmas Eve story about kindness, friendship, and how even the smallest of us can help the light shine. Perfect for bedtime.",
    ]
    st = ParagraphStyle("b", fontName="Andika", fontSize=15.5, leading=22, textColor=HexColor("#FFF8EC"), alignment=TA_CENTER, spaceAfter=10)
    from reportlab.lib.fonts import addMapping
    addMapping("Andika", 0, 0, "Andika"); addMapping("Andika", 1, 0, "Andika-Bold")
    ps = [Paragraph(t, st) for t in blurb]
    y = H - 0.95 * inch
    for p in ps:
        p.wrap(bw, H); y -= p.height; p.drawOn(c, bx, y); y -= 10
    c.setFont("Fredoka-Bold", 20); c.setFillColor(HexColor("#FFD54A"))
    c.drawCentredString(bx + bw / 2, y - 0.25 * inch, S.AGES + "  •  Read-aloud picture book")
    c.save()
    # also export flat front/back panels for marketing and the KDP/ebook cover
    return path


if __name__ == "__main__":
    p, rep = interior()
    print("interior:", p)
    for n, s in rep:
        print(f"  page {n}: {s}pt")
    print("cover:", cover_pdf())
