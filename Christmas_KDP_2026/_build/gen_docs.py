"""Generate manuscript (.md + .docx), page-layout plan, illustration prompts and the character sheet SVG
from story.py, so every document always matches the book."""
import os
import docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

import story as S
from art import svg_doc, g, hedgehog, hedgehog_ball, glimmer, robin, fox, owl, P

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
story_pages = [p for p in S.PAGES if p.get("kind", "art") == "art"]

# ------------------------------------------------------------ manuscript (md)
md = [f"# {S.TITLE}", f"### {S.SUBTITLE}", f"by {S.AUTHOR_NAME}  ·  {S.AGES}  ·  {S.word_count()} words  ·  32-page picture book", "",
      "> Read-aloud manuscript. Page numbers match the print interior. The refrain is in italics.", ""]
for p in story_pages:
    md.append(f"## Page {p['n']}")
    md.append("*THE END*" if p.get("end") else p["text"].replace("Little light, little light", "*Little light, little light").replace("tonight,”", "tonight*,”").replace("tonight?”", "tonight?*”"))
    md.append("")
open(os.path.join(ROOT, "02_Story_Manuscript", "Manuscript.md"), "w").write("\n".join(md))

# ------------------------------------------------------------ manuscript (docx, editable)
d = docx.Document()
st = d.styles["Normal"]; st.font.name = "Georgia"; st.font.size = Pt(13)
h = d.add_heading(S.TITLE, 0); h.alignment = WD_ALIGN_PARAGRAPH.CENTER
para = d.add_paragraph(f"{S.SUBTITLE}\nby {S.AUTHOR_NAME}\n{S.AGES} · {S.word_count()} words · 32-page picture book"); para.alignment = WD_ALIGN_PARAGRAPH.CENTER
d.add_heading("Dedication (page 4)", 2); d.add_paragraph(S.DEDICATION)
for p in story_pages:
    d.add_heading(f"Page {p['n']}", 2)
    if p.get("end"):
        d.add_paragraph("THE END")
        continue
    for chunk in p["text"].split("\n\n"):
        d.add_paragraph(chunk)
    r = d.add_paragraph().add_run(f"[Art: {p['desc']}]"); r.italic = True; r.font.size = Pt(10); r.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
d.add_heading("Let's Talk About the Story (page 30)", 2)
for q in S.TALK_QUESTIONS:
    d.add_paragraph(q, style="List Bullet")
d.add_heading("About the Author (page 31)", 2); d.add_paragraph(S.AUTHOR_BIO)
d.save(os.path.join(ROOT, "02_Story_Manuscript", "Manuscript_Editable.docx"))

# ------------------------------------------------------------ page layout plan
FM = {
    1: ("“This book belongs to” + name line, “Merry Christmas!”", "Glimmer glowing in a pale-blue circle, holly sprigs, falling snow (spot art on cream)."),
    2: ("Title page: *Juniper* / and the Little Lost Star / subtitle / author", "Juniper waving with a big grin, Glimmer sparkling at her side (spot art on cream)."),
    3: ("Copyright page", "Small holly sprig (cream)."),
    4: ("Dedication: " + S.DEDICATION.replace("\n", " "), "Juniper asleep in a ball, Glimmer winking above (spot art)."),
    30: ("“Let's Talk About the Story”: five discussion questions", "Ruby the robin, holly sprig (spot art on cream)."),
    31: ("About the Author", "Old Oakley on a branch, holly sprig (spot art on cream)."),
    32: ("“Goodnight, little light.”", "Juniper asleep with her scarf, Glimmer winking (spot art on cream)."),
}
L = [f"# Page Layouts: {S.TITLE}", "",
     "**Format:** 8.5 × 8.5 in square paperback, premium colour, 32 pages, bleed.  **PDF page size:** 8.625 × 8.75 in.",
     "**Margins:** all text sits at least 0.8 in from the left and right edges and 0.6 in from the top and bottom edges of the PDF page. KDP's minimum is 0.125 in bleed + 0.375 in margin.",
     "**Type:** Andika 16.5 pt, 22.8 pt leading, centred (Andika was designed for early-reader legibility). Display type: Fredoka. Both are SIL OFL, embedded.",
     "**Composition:** 24 full-bleed story spreads, each with its own illustration and text set in a calm zone of the art (top sky or bottom snow); 4 front-matter and 3 back-matter pages with spot illustrations on cream; 1 full-bleed finale (“The End”). Every page has a unique image.",
     "**Page side:** odd pages are rectos (right-hand), even pages are versos. Page 1 is a recto.", ""]
for p in S.PAGES:
    n = p["n"]
    L.append(f"## Page {n}: {'recto' if n % 2 else 'verso'}")
    L.append(f"- **Illustration file:** `04_Illustrations/p{n:02d}_{p['scene']}.jpg` (source `_build/svg/{p['scene']}.svg`)")
    if p.get("kind") == "front":
        L.append(f"- **Text:** {FM[n][0]}")
        L.append(f"- **Illustration:** {FM[n][1]}")
    else:
        L.append(f"- **Text placement:** {'top sky band' if p['text_pos']=='top' else 'bottom snow band'}, {'cream text on night sky' if p['text_color']=='light' else 'navy text on light ground'}" + ("; “The End” set large in the sky" if p.get("end") else ""))
        if not p.get("end"):
            L.append("- **Story text:**\n\n" + "\n".join("  > " + line if line else "  >" for line in p["text"].split("\n")) + "\n")
        L.append(f"- **Illustration:** {p['desc']}")
        L.append(f"- **Character positions:** {p['chars']}")
        L.append(f"- **Background:** {p['bg']}")
        L.append(f"- **Illustration prompt:** {p['prompt']}")
    L.append("")
open(os.path.join(ROOT, "05_Page_Layouts", "Page_Layout_Plan.md"), "w").write("\n".join(L))

# ------------------------------------------------------------ prompts for an illustrator / image model
pr = [f"# Illustration Prompts: {S.TITLE}", "",
      "The finished book uses the vector illustrations in `04_Illustrations`, drawn programmatically for exact consistency.",
      "If you later commission a painted edition (human illustrator or image model), use these prompts **with the style line and the character lock text** on every page. Supply `03_Character_References/character_sheet.png` as the visual reference.", "",
      f"**Style line (prefix every prompt):** {S.STYLE}", "", "**Character lock (append the characters that appear):**", ""]
pr += [f"- {v}" for v in S.CHARACTER_LOCK.values()] + [""]
for p in story_pages:
    pr.append(f"### Page {p['n']}\n{S.STYLE}. {p['prompt']} Leave the {'top third' if p['text_pos']=='top' else 'bottom third'} calm and uncluttered for text. Square 2588×2625 px (8.625×8.75 in at 300 DPI).\n")
pr.append("### Front cover\n" + S.STYLE + ". Little hedgehog Juniper in her red striped scarf, arms raised, beaming up at a glowing smiling golden star above her paws; snowy village with glowing windows behind; deep navy starry sky; top 40% left clear for the title.\n")
pr.append("### Back cover\n" + S.STYLE + ". Continuation of the same night scene: red fox Ember sitting with eyes closed and a robin on the snow at lower left; upper two-thirds calm starry sky for the blurb; lower-right 2.2 × 1.4 in kept plain for the barcode.\n")
open(os.path.join(ROOT, "04_Illustrations", "Illustration_Prompts.md"), "w").write("\n".join(pr))

# ------------------------------------------------------------ character sheet SVG
W, H = 3600, 2400
b = f'<rect width="{W}" height="{H}" fill="#FBF4E6"/>'
b += f'<text x="{W/2}" y="150" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="110" fill="#B8262F">Character Reference Sheet</text>'
b += f'<text x="{W/2}" y="235" text-anchor="middle" font-family="Andika" font-size="52" fill="#1C3566">{S.TITLE}</text>'
cast = [
    (450, 1050, 0.95, hedgehog(arms="wave", mouth="grin"), "Juniper", "hedgehog · age ~5"),
    (1150, 1050, 0.95, hedgehog(arms="hug", eyes="closed", mouth="smile", scarf=False), "Juniper", "no scarf (pp. 18–25)"),
    (1800, 1050, 0.95, hedgehog(grandma=True, arms="hold"), "Grandma Hedgehog", "silver spikes · specs · shawl"),
    (2450, 850, 1.2, glimmer(), "Glimmer", "happy / bright"),
    (3100, 850, 1.2, glimmer(mood="sad", pale=True, glow=0.3), "Glimmer", "sad / dim"),
]
for x, y, s, body, name, note in cast:
    b += g(x, y, s, body=body)
    ty = y + 110 if "Glimmer" not in name else y + 300
    b += f'<text x="{x}" y="{ty}" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="58" fill="#1C3566">{name}</text>'
    b += f'<text x="{x}" y="{ty+60}" text-anchor="middle" font-family="Andika" font-size="40" fill="#5A3B28">{note}</text>'
for x, y, s, body, name, note in [(500, 2050, 1.4, robin(), "Ruby", "robin"), (1450, 2050, 0.85, fox(), "Ember", "fox"),
                                   (2350, 2050, 0.85, owl(), "Old Oakley", "owl"), (3150, 1950, 0.8, hedgehog_ball(), "Juniper", "asleep / rolling")]:
    b += g(x, y, s, body=body)
    b += f'<text x="{x}" y="{y+90}" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="58" fill="#1C3566">{name}</text>'
    b += f'<text x="{x}" y="{y+150}" text-anchor="middle" font-family="Andika" font-size="40" fill="#5A3B28">{note}</text>'
sw = [P["spike"], P["spike_tip"], P["face"], P["ear_in"], P["scarf"], P["stripe"], P["star"], P["breast"], P["fox"], P["owl"], P["night_top"], P["window"]]
for i, c in enumerate(sw):
    b += f'<rect x="{300+i*260}" y="1350" width="200" height="120" rx="16" fill="{c}" stroke="#999" stroke-width="3"/>'
    b += f'<text x="{400+i*260}" y="1520" text-anchor="middle" font-family="Andika" font-size="34" fill="#333">{c}</text>'
open(os.path.join(HERE, "svg", "charsheet.svg"), "w").write(svg_doc(W, H, b))
print("docs written; story words:", S.word_count())
