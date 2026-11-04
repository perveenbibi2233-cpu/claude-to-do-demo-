"""Generate the manuscript, page plan, art prompt pack, art checklist, character lock and KDP spec docs from book.py."""
import os
import docx
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import book as B

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = lambda rel, txt: open(os.path.join(ROOT, rel), "w").write(txt)
REF = "Attach as references: "
SHEETS = {"Pip": "Pip_fox.png", "Mimi": "Mimi_rabbit.png", "Bramble": "Bramble_bear.png", "Tinsel": "Tinsel_reindeer.png",
          "Santa": "Santa_reference.png (make it first, prompt C1)", "Goldie": "Goldie_reference.png (make it first, prompt C2)"}


def find_line(t):
    return f"{t['n']} {t['name']}"


# ------------------------------------------------------------------ manuscript
md = [f"# {B.TITLE}", f"### {B.SUBTITLE}", f"{B.AGES} · {B.word_count()} words · 32 pages · 10 search-and-find scenes", ""]
dd = docx.Document(); dd.styles["Normal"].font.name = "Georgia"; dd.styles["Normal"].font.size = Pt(13)
h = dd.add_heading(B.TITLE, 0); h.alignment = WD_ALIGN_PARAGRAPH.CENTER
dd.add_paragraph(B.SUBTITLE).alignment = WD_ALIGN_PARAGRAPH.CENTER
for s in B.SPREADS:
    a, b = s["pages"]
    md += [f"## Pages {a}–{b}: {s['title']}", ""] + [p + "\n" for p in s["text"]]
    dd.add_heading(f"Pages {a}–{b}: {s['title']}", 2)
    for p in s["text"]:
        dd.add_paragraph(p)
    if s.get("extra"):
        md.append(f"*{s['extra']}*\n*{B.FRIENDS_RULE}*\n"); dd.add_paragraph(s["extra"]); dd.add_paragraph(B.FRIENDS_RULE)
    if s.get("targets"):
        md.append("**Can you find all five hidden objects? Look carefully!**\n")
        md += [f"- {find_line(t)}" for t in s["targets"]] + [""]
        dd.add_paragraph("Can you find all five hidden objects? Look carefully!")
        for t in s["targets"]:
            dd.add_paragraph(find_line(t), style="List Bullet")
md += ["## Pages 28–29: Bonus", B.SPOT_DIFF["text"], "", "## Pages 30–31: Answer key", "(Built from the finished pictures.)", "",
       "## Page 32", B.MESSAGE, ""]
dd.add_heading("Pages 28–29: Bonus", 2); dd.add_paragraph(B.SPOT_DIFF["text"])
dd.add_heading("Page 32", 2); dd.add_paragraph(B.MESSAGE)
W("02_Manuscript/Manuscript.md", "\n".join(md))
dd.save(os.path.join(ROOT, "02_Manuscript/Manuscript_Editable.docx"))

# ------------------------------------------------------------------ prompts
def char_block(names):
    return "\n".join(f"- {B.LOCK[n]}" for n in names)


def scene_prompt(s):
    excl = ""
    stick = [t for t in s.get("targets", []) if t["method"] == "sticker"]
    scene_t = [t for t in s.get("targets", []) if t["method"] == "scene"]
    if stick:
        excl = ("\nIMPORTANT, do NOT include any of these anywhere in the picture (they are added separately later): "
                + ", ".join(t["name"].replace("tiny golden star clue", "golden stars or sparkles").replace("golden feather", "feathers") for t in stick) + ".")
    if scene_t:
        excl += "\nInclude EXACTLY: " + "; ".join(f"{t['n']} {t['name']} ({t['note']})" for t in scene_t) + "."
    return (f"{B.STYLE}\n\nWide landscape double-page picture-book spread, 3:2 aspect ratio (1536×1024).\n\n"
            f"SCENE: {s['scene']}{excl}\n\n"
            f"CHARACTERS (match the attached reference sheets exactly: same faces, proportions, colours and clothing):\n{char_block(s['chars'])}\n\n"
            "LAYOUT: Keep the vertical middle strip (centre 12% of the width) free of faces, characters and important objects, because it falls in the book's binding. "
            "Keep the top-left area (about 40% wide × 30% tall) calm and simple (sky, wall or snow) for story text."
            + (" Keep the bottom-right corner (about 35% wide × 35% tall) calm and simple for the search list." if s.get("targets") else "")
            + " Keep all characters at least 5% away from every edge. No text anywhere.")


P = [f"# Art Prompt Pack: {B.TITLE}", "",
     "Paste each prompt into your image tool **with the listed reference sheets attached**. Save each result into `05_Art_Inbox/` using the exact file name shown, then send the images to me.",
     "", "**Before you start:** read `04_Art_Prompts/Art_Production_Guide.md` (sizes, upscaling and how the hidden objects work).", ""]
P += ["## C. Character references to make first", "",
      "### C1 → `05_Art_Inbox/characters/Santa_reference.png`",
      f"```\n{B.STYLE}\n\nCharacter reference sheet on a plain warm-white background, 3:2 landscape: front, side, three-quarter and back views plus four expressions (warm smile, surprised, laughing, thoughtful) of:\n{B.LOCK['Santa']}\nInclude Pip the fox standing beside him for scale (Pip reaches just below Santa's knee).\n{B.LOCK['Pip']}\n```",
      f"{REF}{SHEETS['Pip']}, Tinsel_reindeer_lineup_with_Santa.png", "",
      "### C2 → `05_Art_Inbox/characters/Goldie_reference.png`",
      f"```\n{B.STYLE}\n\nCharacter reference sheet on a plain warm-white background, 3:2 landscape: front, side, back and flying views plus four expressions (shy, happy, worried, singing) of:\n{B.LOCK['Goldie']}\nInclude one view of Goldie sitting in Pip's cupped front paws for scale.\n{B.LOCK['Pip']}\n```",
      f"{REF}{SHEETS['Pip']}", ""]
P += ["## S. Scene spreads (3:2 landscape, 1536×1024 or larger)", ""]
for s in B.SPREADS:
    a, b = s["pages"]
    P += [f"### Pages {a}–{b}: {s['title']} → `05_Art_Inbox/scenes/{s['key']}.png`",
          f"```\n{scene_prompt(s)}\n```", REF + ", ".join(SHEETS[c] for c in s["chars"]), ""]
P += ["## T. Title, bonus and closing pictures", ""]
for n, sp in B.SINGLES.items():
    P += [f"### Page {n}: {sp['label']} → `05_Art_Inbox/singles/{sp['key']}.png`",
          f"```\n{B.STYLE}\n\nPortrait picture-book page, 2:3 aspect ratio (1024×1536). Leave generous margins: the top and bottom 7% will be trimmed.\n\nSCENE: {sp['scene']}\n\nCHARACTERS (match the attached reference sheets exactly):\n{char_block(sp['chars'])}\n\nNo text anywhere.\n```",
          REF + ", ".join(SHEETS[c] for c in sp["chars"]), ""]
sd = B.SPOT_DIFF
P += [f"### Pages 28–29: Spot-the-difference base picture → `05_Art_Inbox/singles/{sd['key']}.png`",
      f"```\n{B.STYLE}\n\n{sd['scene']}\n\nCHARACTERS (match the attached reference sheets exactly):\n{char_block(sd['chars'])}\n\nNo text anywhere.\n```",
      REF + ", ".join(SHEETS[c] for c in sd["chars"]), "I make the second picture with exactly five changes, so the answer key is exact.", ""]
P += ["## K. Covers", "",
      "### Front cover → `05_Art_Inbox/singles/cover_front.png`",
      f"```\n{B.STYLE}\n\nPortrait book-cover illustration, 2:3 (1024×1536). A magical Christmas mystery: Pip the fox in front, holding a magnifying glass up to one eye, with Mimi, Bramble and Tinsel peeking excitedly behind him; behind them Santa's enormous Christmas tree with an empty, glowing gap at the very top; a trail of golden sparkles and one golden feather floating across the scene; tiny Goldie half-hidden in a snowy branch (a secret for sharp eyes). Night-blue sky, warm golden light. Keep the TOP 35% calm sky for the title. No text.\n\nCHARACTERS (match the attached reference sheets exactly):\n{char_block(['Pip', 'Mimi', 'Bramble', 'Tinsel', 'Goldie'])}\n```",
      REF + ", ".join(SHEETS[c] for c in ["Pip", "Mimi", "Bramble", "Tinsel", "Goldie"]), "",
      "### Back cover → `05_Art_Inbox/singles/cover_back.png`",
      f"```\n{B.STYLE}\n\nPortrait 2:3 (1024×1536). Matching night-time Christmas village scene, calm and simple: soft snowy rooftops along the bottom third, night-blue sky with gentle snow above. Bramble and Tinsel waving small at the lower left. Leave the upper two-thirds very calm for text and the lower-right corner plain for a barcode. No text.\n\nCHARACTERS:\n{char_block(['Bramble', 'Tinsel'])}\n```",
      REF + ", ".join(SHEETS[c] for c in ["Bramble", "Tinsel"]), ""]
P += ["## O. Hidden-object sticker sheets", "",
      "Each sheet gives me the objects I place into the scenes, so every count is exact and the answer key is exact.", ""]
for k, items in B.STICKER_SHEETS.items():
    P += [f"### `05_Art_Inbox/stickers/{k}.png`",
          f"```\n{B.STYLE.replace('richly detailed cozy Christmas environment, ', '')}\n\nSticker sheet on a PLAIN, FLAT, PURE WHITE background (no shadows on the background, no floor, no scenery). "
          f"Square 1:1 (1024×1024). Arrange in a neat grid with lots of empty white space between every item; nothing touching or overlapping. "
          f"Draw each of these objects THREE times, in three slightly different angles or poses, all in the same storybook style: {', '.join(items)}. "
          "Each object clearly outlined, cheerful and easy for a 3-year-old to recognise.\n```", ""]
W("04_Art_Prompts/Art_Prompt_Pack.md", "\n".join(P))

# ------------------------------------------------------------------ checklist
C = ["# Art Checklist", "", "Tick each file off as it lands in `05_Art_Inbox/`.", "",
     "| # | File | Shape | Used on |", "|---|---|---|---|",
     "| C1 | `characters/Santa_reference.png` | 3:2 | reference only |",
     "| C2 | `characters/Goldie_reference.png` | 3:2 | reference only |"]
for i, s in enumerate(B.SPREADS, 1):
    C.append(f"| S{i} | `scenes/{s['key']}.png` | 3:2 | pages {s['pages'][0]}–{s['pages'][1]} |")
C += [f"| T1 | `singles/p01_title.png` | 2:3 | page 1 |", "| T2 | `singles/s14_spot_difference.png` | 1:1 | pages 28–29 |",
      "| T3 | `singles/p32_goodnight.png` | 2:3 | page 32 |", "| K1 | `singles/cover_front.png` | 2:3 | front cover |", "| K2 | `singles/cover_back.png` | 2:3 | back cover |"]
C += [f"| O{i} | `stickers/{k}.png` | 1:1 | hidden objects |" for i, k in enumerate(B.STICKER_SHEETS, 1)]
C += ["", f"**Total: {2 + len(B.SPREADS) + 5 + len(B.STICKER_SHEETS)} images.**"]
W("04_Art_Prompts/Art_Checklist.md", "\n".join(C))

# ------------------------------------------------------------------ page plan
L = [f"# 32-Page Plan: {B.TITLE}", "",
     "Page 1 is a right-hand page, so the facing pairs in a printed book are 2–3, 4–5 … 30–31. Every scene is a true two-page spread.", "",
     "| Pages | Content | Art file |", "|---|---|---|", "| 1 | Title page: title, subtitle, author | `singles/p01_title.png` |"]
for s in B.SPREADS:
    a, b = s["pages"]
    L.append(f"| {a}–{b} | {s['title']}" + (" (search-and-find)" if s.get('targets', None) else "") + f" | `scenes/{s['key']}.png` |")
L += ["| 28–29 | Bonus: spot 5 differences (picture on each page) | `singles/s14_spot_difference.png` + my edited copy |",
      "| 30–31 | Answer key: every search scene with circled answers, plus the 5 differences | built from the finished art |",
      "| 32 | Christmas message; copyright block at the foot of the page | `singles/p32_goodnight.png` |", ""]
for s in B.SPREADS:
    a, b = s["pages"]
    L += [f"## Pages {a}–{b}: {s['title']}", "", "**Story text (left page, top-left panel):**", ""] + [f"> {p}" for p in s["text"]] + [""]
    if s.get("extra"):
        L += [f"> *{s['extra']}*", f"> *{B.FRIENDS_RULE}*", ""]
    if s.get("targets"):
        L += ["**Search panel (right page, bottom-right):** “Can you find all five hidden objects? Look carefully!”", ""]
        L += [f"- {find_line(t)}" + (f": *{t['note']}*" if t["note"] else "") + f" ({'placed from sticker sheet' if t['method']=='sticker' else 'painted in scene, verified by hand'})" for t in s["targets"]]
        L.append("")
    L += [f"**Illustration:** {s['scene']}", "", f"**Characters:** {', '.join(s['chars'])}", ""]
W("03_Page_Plan/Page_Plan.md", "\n".join(L))

# ------------------------------------------------------------------ character lock
CL = [f"# Character Lock: {B.TITLE}", "", "Reference sheets you supplied are in `reference_sheets/`. Santa and Goldie need sheets made first (prompts C1, C2).", ""]
for n, d in B.LOCK.items():
    CL += [f"## {n}", d.split(": ", 1)[1], "", f"Reference: `{SHEETS[n]}`", ""]
CL += ["## Size ladder (shortest → tallest)", "Goldie (fits in Pip's paws) → Mimi (⅔ of Pip) → Tinsel (to Pip's shoulder, antlers above) → Pip → Bramble (a little taller and wider) → Santa (Pip reaches below his knee).", "",
       "## Checks I run on every picture you send", "- Same face shapes, eye colours, markings and clothing as the sheets (Pip's teal scarf wrapped twice; Mimi's lavender pom-pom hat; Bramble's red snowflake jumper; Tinsel's red collar and one golden bell and back spots).",
       "- No extra clothing or accessories; no random extra characters.", "- Size ladder respected.", "- No text, letters or watermarks.", "- Hidden-object counts (see the answer-key process in the production guide)."]
W("01_Character_Lock/Character_Lock.md", "\n".join(CL))
print("docs written,", B.word_count(), "story words")
