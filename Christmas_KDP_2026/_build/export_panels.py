"""Export flat front/back cover images (with typography) from the print cover PDF, plus the character sheet."""
import os, sys, shutil
import pypdfium2 as pdfium
import cover as C
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
PNG = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "png")
pdf = pdfium.PdfDocument(os.path.join(ROOT, "08_Print_Ready_PDF", f"Juniper_Cover_FullWrap_{C.COVER_W_IN}x{C.COVER_H_IN}in.pdf"))
im = pdf[0].render(scale=300 / 72).to_pil().convert("RGB")
b = round(C.BLEED * 300); t = round(C.TRIM_W * 300)
front = im.crop((C.FRONT_X0, b, C.FRONT_X0 + t, b + t))
back = im.crop((b, b, b + t, b + t))
front.save(os.path.join(ROOT, "06_Front_Cover", "Front_Cover_8.5x8.5_300dpi.jpg"), quality=95, dpi=(300, 300))
front.resize((1600, 1600)).save(os.path.join(ROOT, "06_Front_Cover", "Front_Cover_1600px_for_listings.jpg"), quality=92)
back.save(os.path.join(ROOT, "07_Back_Cover", "Back_Cover_8.5x8.5_300dpi.jpg"), quality=95, dpi=(300, 300))
im.resize((im.width // 3, im.height // 3)).save(os.path.join(ROOT, "06_Front_Cover", "Cover_FullWrap_preview.jpg"), quality=90)
shutil.copy(os.path.join(PNG, "charsheet.png"), os.path.join(ROOT, "03_Character_References", "character_sheet.png"))
print("panels exported")
