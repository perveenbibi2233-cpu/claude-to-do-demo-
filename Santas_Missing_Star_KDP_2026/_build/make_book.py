"""Assemble the 32-page interior.

  python3 make_book.py proof   -> 06_Layout_Proof/Layout_Proof_ART_PENDING.pdf  (grey "ART PENDING" boxes + trim/safe/gutter guides)
  python3 make_book.py final   -> 07_Print_Ready_PDF/...  (refuses to run until every art file, the author name and the answer key exist)

Art is read from ../05_Art_Inbox/prepared/ (print-size files produced by prepare_art.py)."""
import os
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, Color
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import book as B

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ART = os.path.join(ROOT, "05_Art_Inbox", "prepared")
for n, f in [("Andika", "Andika-Regular.ttf"), ("Andika-Bold", "Andika-Bold.ttf"), ("Fredoka", "Fredoka-SemiBold.ttf"),
             ("Fredoka-Bold", "Fredoka-Bold.ttf"), ("Fredoka-Medium", "Fredoka-Medium.ttf")]:
    pdfmetrics.registerFont(TTFont(n, os.path.join(HERE, "fonts", f)))

PW, PH = B.PAGE_W * inch, B.PAGE_H * inch
SAFE = 0.75 * inch                     # text/panels >= 0.75 in from trim edges (KDP minimum 0.375 + bleed)
CREAM, GOLD, RED, NAVY, INK = HexColor("#FFF8EC"), HexColor("#E3B54A"), HexColor("#C0272D"), HexColor("#1C3566"), HexColor("#3A2A20")
MODE = sys.argv[1] if len(sys.argv) > 1 else "proof"


def art_path(name):
    p = os.path.join(ART, name + ".jpg")
    return p if os.path.exists(p) else None


def placeholder(c, x, y, w, h, label):
    c.saveState()
    c.setFillColor(HexColor("#DCE3EE")); c.rect(x, y, w, h, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#C3CEDF")); c.setLineWidth(1)
    step = 0.5 * inch
    p = c.beginPath(); c.clipPath(p, stroke=0) if False else None
    k = -h
    while k < w:
        x0, y0, x1, y1 = x + max(k, 0), y + max(-k, 0), x + min(k + h, w), y + min(h, w - k)
        c.line(x0, y0, x1, y1); k += step
    c.setFillColor(HexColor("#6B7A93")); c.setFont("Fredoka-Bold", 26)
    c.drawCentredString(x + w / 2, y + h / 2 + 8, "ART PENDING")
    c.setFont("Andika", 13); c.drawCentredString(x + w / 2, y + h / 2 - 16, label)
    c.restoreState()


def draw_art(c, name, side, label):
    """side: 'left'/'right' half of a spread, or 'full' single page."""
    p = art_path(name)
    if p:
        if side == "full":
            c.drawImage(p, 0, 0, PW, PH)
        else:
            dx = 0 if side == "left" else -PW
            c.saveState(); p_ = c.beginPath(); p_.rect(0, 0, PW, PH); c.clipPath(p_, stroke=0, fill=0)
            c.drawImage(p, dx, 0, 2 * PW, PH); c.restoreState()
        return True
    if MODE == "final":
        raise SystemExit(f"missing art: {name}")
    placeholder(c, 0, 0, PW, PH, label)
    return False


def guides(c, side):
    if MODE != "proof":
        return
    c.saveState(); c.setLineWidth(0.8); c.setDash(4, 3)
    b = B.BLEED * inch
    tx0 = b if side in ("left", "full_left") else 0   # trim box x origin (bleed is on the outside edge; even pages bleed left)
    c.setStrokeColor(HexColor("#D23B3B")); c.rect(tx0, b, B.TRIM_W * inch, B.TRIM_H * inch)            # trim
    c.setStrokeColor(HexColor("#2E8B57")); c.rect(tx0 + SAFE, b + SAFE, B.TRIM_W * inch - 2 * SAFE, B.TRIM_H * inch - 2 * SAFE)  # safe
    if side in ("left", "right"):              # binding keep-out (0.75 in each side of the fold)
        c.setStrokeColor(HexColor("#8A5CC2"))
        gx = PW if side == "left" else 0
        c.rect(gx - 0.75 * inch if side == "left" else gx, 0, 0.75 * inch, PH)
    c.setDash(); c.setFont("Andika", 7); c.setFillColor(HexColor("#D23B3B"))
    c.drawString(tx0 + 4, b + 4, "proof guides: red = trim, green = text safe area, purple = binding keep-out (not printed)")
    c.restoreState()


def panel(c, x, y_top, w, flow, pad=0.22 * inch):
    """Cream rounded panel sized to its paragraphs; returns bottom y."""
    hs = [f.wrap(w - 2 * pad, PH)[1] for f in flow]
    gaps = 7
    h = sum(hs) + gaps * (len(flow) - 1) + 2 * pad
    c.saveState(); c.setFillColor(CREAM); c.setStrokeColor(GOLD); c.setLineWidth(2)
    c.roundRect(x, y_top - h, w, h, 14, fill=1, stroke=1); c.restoreState()
    y = y_top - pad
    for f, fh in zip(flow, hs):
        y -= fh; f.drawOn(c, x + pad, y); y -= gaps
    return y_top - h


ST = {
    "title": ParagraphStyle("t", fontName="Fredoka-Bold", fontSize=22, leading=26, textColor=RED),
    "body": ParagraphStyle("b", fontName="Andika", fontSize=17, leading=24, textColor=INK),
    "small": ParagraphStyle("s", fontName="Andika", fontSize=13, leading=17, textColor=NAVY),
    "find": ParagraphStyle("f", fontName="Fredoka-Medium", fontSize=16, leading=20, textColor=NAVY),
    "row": ParagraphStyle("r", fontName="Andika-Bold", fontSize=17, leading=21, textColor=INK),
}


def search_panel(c, s):
    w = 3.7 * inch
    x = PW - B.BLEED * inch - SAFE - w
    rows = [Paragraph("Can you find all five hidden objects? Look carefully!", ST["find"])]
    for t in s["targets"]:
        rows.append(Paragraph(f'<font name="Fredoka-Bold" size="22" color="#C0272D">{t["n"]}</font>&nbsp;&nbsp;{t["name"]}', ST["row"]))
    # measure, then place so the panel's bottom sits on the safe line
    hs = sum(r.wrap(w - 0.44 * inch, PH)[1] for r in rows) + 7 * (len(rows) - 1) + 0.44 * inch
    panel(c, x, B.BLEED * inch + SAFE + hs, w, rows)


def spread(c, s):
    a, b = s["pages"]
    label = f"pages {a}–{b} · {s['title']} · scenes/{s['key']}.png"
    # left page
    draw_art(c, s["key"], "left", label)
    flow = [Paragraph(s["title"], ST["title"])] + [Paragraph(p, ST["body"]) for p in s["text"]]
    panel(c, B.BLEED * inch + SAFE, PH - B.BLEED * inch - SAFE, 4.7 * inch, flow)
    guides(c, "left"); c.showPage()
    # right page
    draw_art(c, s["key"], "right", label)
    if s.get("targets"):
        search_panel(c, s)
    elif s.get("extra"):
        w = 3.9 * inch
        flow = [Paragraph(s["extra"], ST["find"]), Paragraph(B.FRIENDS_RULE, ST["small"])]
        hs = sum(f.wrap(w - 0.44 * inch, PH)[1] for f in flow) + 7 + 0.44 * inch
        panel(c, PW - B.BLEED * inch - SAFE - w, B.BLEED * inch + SAFE + hs, w, flow)
    guides(c, "right"); c.showPage()


def outlined(c, text, font, size, y, fill, stroke, sw):
    c.saveState()
    t = c.beginText(); t.setFont(font, size); t.setTextRenderMode(2)
    c.setFillColor(fill); c.setStrokeColor(stroke); c.setLineWidth(sw); c.setLineJoin(1)
    t.setTextOrigin(PW / 2 - pdfmetrics.stringWidth(text, font, size) / 2, y); t.textLine(text); c.drawText(t)
    c.restoreState()


def title_page(c):
    draw_art(c, "p01_title", "full", "page 1 · title page · singles/p01_title.png")
    outlined(c, "Where Is Santa's", "Fredoka-Bold", 50, PH - 1.55 * inch, HexColor("#FFF3D6"), HexColor("#9E1F2A"), 3)
    outlined(c, "Missing Star?", "Fredoka-Bold", 62, PH - 2.4 * inch, HexColor("#FFD54A"), HexColor("#0A1736"), 3.5)
    c.setFillColor(HexColor("#FFF8EC")); c.setFont("Fredoka-Medium", 18)
    c.drawCentredString(PW / 2, PH - 2.95 * inch, B.SUBTITLE)
    c.setFont("Fredoka-Medium", 18)
    c.drawCentredString(PW / 2, PH - 3.4 * inch, "by " + (B.AUTHOR_NAME or "[Author name]"))
    guides(c, "full_right"); c.showPage()


def spot_diff(c):
    a, b = B.SPOT_DIFF["pages"]
    for i, side in enumerate(("left", "right")):
        c.setFillColor(CREAM); c.rect(0, 0, PW, PH, fill=1, stroke=0)
        tx0 = B.BLEED * inch if side == "left" else 0
        cx = tx0 + B.TRIM_W * inch / 2
        if i == 0:
            c.setFillColor(RED); c.setFont("Fredoka-Bold", 34); c.drawCentredString(cx, PH - 1.5 * inch, "Bonus: Spot 5 Differences!")
            p = Paragraph(B.SPOT_DIFF["text"], ParagraphStyle("x", parent=ST["body"], alignment=TA_CENTER)); w = 6 * inch
            p.wrap(w, PH); p.drawOn(c, cx - w / 2, PH - 2.0 * inch - p.height)
        else:
            c.setFillColor(NAVY); c.setFont("Fredoka-Bold", 26); c.drawCentredString(cx, PH - 1.5 * inch, "Now look closely...")
        size = 6.6 * inch; x = cx - size / 2; y = 1.4 * inch
        name = "s14_spot_difference" + ("" if i == 0 else "_B")
        p = art_path(name)
        if p:
            c.drawImage(p, x, y, size, size)
        elif MODE == "final":
            raise SystemExit(f"missing art: {name}")
        else:
            placeholder(c, x, y, size, size, "picture " + ("A: singles/s14_spot_difference.png" if i == 0 else "B: made by me with exactly 5 changes"))
        c.setStrokeColor(GOLD); c.setLineWidth(4); c.roundRect(x, y, size, size, 10)
        c.setFillColor(NAVY); c.setFont("Fredoka-Medium", 18); c.drawCentredString(cx, y - 0.45 * inch, "Picture " + ("A" if i == 0 else "B"))
        guides(c, side); c.showPage()


def answer_key(c):
    searches = [s for s in B.SPREADS if s.get("targets")]
    pages = [searches[:6], searches[6:]]
    for k, group in enumerate(pages):
        side = "left" if k == 0 else "right"
        c.setFillColor(CREAM); c.rect(0, 0, PW, PH, fill=1, stroke=0)
        tx0 = B.BLEED * inch if side == "left" else 0
        x0 = tx0 + SAFE; usable = B.TRIM_W * inch - 2 * SAFE
        c.setFillColor(RED); c.setFont("Fredoka-Bold", 28)
        c.drawString(x0, PH - B.BLEED * inch - SAFE - 0.3 * inch, "Answer Key" + (" (continued)" if k else ""))
        colw = (usable - 0.3 * inch) / 2; tw = colw; th = tw * 2 / 3
        top = PH - B.BLEED * inch - SAFE - 0.7 * inch
        for i, s in enumerate(group):
            col, row = i % 2, i // 2
            x = x0 + col * (colw + 0.3 * inch); y = top - row * (th + 0.95 * inch) - th
            p = art_path(s["key"] + "_answers")
            if p:
                c.drawImage(p, x, y, tw, th)
            elif MODE == "final":
                raise SystemExit("answer-key image missing for " + s["key"])
            else:
                placeholder(c, x, y, tw, th, "")
            a, b = s["pages"]
            c.setFillColor(NAVY); c.setFont("Fredoka-Bold", 11); c.drawString(x, y - 14, f"Pages {a}–{b}: {s['title']}")
            c.setFont("Andika", 9.5); c.setFillColor(INK)
            line = ", ".join(f"{t['n']} {t['name']}" for t in s["targets"])
            pr = Paragraph(line, ParagraphStyle("k", fontName="Andika", fontSize=9.5, leading=12, textColor=INK)); pr.wrap(tw, 100); pr.drawOn(c, x, y - 18 - pr.height)
        if k == 1:
            y = top - 2 * (th + 0.95 * inch) - 0.2 * inch
            c.setFillColor(NAVY); c.setFont("Fredoka-Bold", 15); c.drawString(x0, y, "Bonus: the 5 differences")
            diffs = B.SPOT_DIFF["differences"] or ["(listed here once picture B is made)"]
            c.setFont("Andika", 12); c.setFillColor(INK)
            for j, d in enumerate(diffs):
                c.drawString(x0, y - 20 - j * 17, f"{j + 1}. {d}" if B.SPOT_DIFF["differences"] else d)
        guides(c, side); c.showPage()


def closing(c):
    draw_art(c, "p32_goodnight", "full", "page 32 · singles/p32_goodnight.png")
    p = Paragraph(B.MESSAGE, ParagraphStyle("m", fontName="Fredoka-Bold", fontSize=26, leading=34, textColor=HexColor("#FFF8EC"), alignment=TA_CENTER))
    w = 6.2 * inch; p.wrap(w, PH); x = B.BLEED * inch + (B.TRIM_W * inch - w) / 2
    c.saveState(); c.setFillColor(Color(0.04, 0.09, 0.21)); c.roundRect(x - 14, PH - 1.3 * inch - p.height - 14, w + 28, p.height + 28, 16, fill=1, stroke=0); c.restoreState()
    p.drawOn(c, x, PH - 1.3 * inch - p.height)
    author = B.AUTHOR_NAME or "[Author name]"
    txt = (f"{B.TITLE} Copyright © {B.YEAR} {author}. All rights reserved. No part of this book may be reproduced without written permission "
           "from the author, except for brief quotations in reviews. This is a work of fiction." + (f" ISBN {B.ISBN}." if B.ISBN else "")
           + " Typeset in Andika and Fredoka (SIL Open Font License).")
    st = ParagraphStyle("c", fontName="Andika", fontSize=8.5, leading=11, textColor=INK, alignment=TA_CENTER)
    q = Paragraph(txt, st); w2 = 6.4 * inch; q.wrap(w2 - 0.3 * inch, PH)
    bx = B.BLEED * inch + (B.TRIM_W * inch - w2) / 2; by = B.BLEED * inch + SAFE
    c.saveState(); c.setFillColor(CREAM); c.roundRect(bx, by, w2, q.height + 0.25 * inch, 10, fill=1, stroke=0); c.restoreState()
    q.drawOn(c, bx + 0.15 * inch, by + 0.125 * inch)
    guides(c, "full_left"); c.showPage()


def build():
    if MODE == "final" and not B.AUTHOR_NAME:
        raise SystemExit("Set AUTHOR_NAME in book.py before the final export.")
    out_dir = os.path.join(ROOT, "06_Layout_Proof" if MODE == "proof" else "07_Print_Ready_PDF")
    os.makedirs(out_dir, exist_ok=True)
    name = "Layout_Proof_ART_PENDING.pdf" if MODE == "proof" else "Missing_Star_Interior_8.5x11_32pp_bleed.pdf"
    path = os.path.join(out_dir, name)
    c = canvas.Canvas(path, pagesize=(PW, PH), initialFontName="Andika", initialFontSize=12)
    c.setTitle(B.TITLE + (" - LAYOUT PROOF (art pending)" if MODE == "proof" else ""))
    title_page(c)
    for s in B.SPREADS:
        spread(c, s)
    spot_diff(c)
    answer_key(c)
    closing(c)
    c.save()
    from pypdf import PdfReader
    n = len(PdfReader(path).pages)
    assert n == 32, n
    print(path, n, "pages")


if __name__ == "__main__":
    build()
