# Christmas_KDP_2026: *Juniper and the Little Lost Star*

An original 32-page Christmas picture book for ages 3–7, packaged for Amazon KDP (8.5 × 8.5 in square paperback, premium colour).

> Juniper the hedgehog has slept through every Christmas of her life... until a tiny star lands with a THUMP outside her door.

## Review it in 5 minutes
1. **Read the book:** `08_Print_Ready_PDF/Juniper_Interior_8.5x8.5_32pp_bleed.pdf`. Use two-page view, with the cover shown separately.
2. **See the cover:** `06_Front_Cover/Cover_FullWrap_preview.jpg` and `Front_Cover_8.5x8.5_300dpi.jpg`.
3. **Read the report:** `10_Final_Publishing_Report/Final_Publishing_Report.md`. It covers the QC results, KDP specs, the **three things to do before upload**, and honest limitations.
4. **Technical checks:** `10_Final_Publishing_Report/preflight_report.txt`.

## Folder map
| Folder | Contents |
|---|---|
| `01_Market_Research` | Market scan, 5 concepts, the selected concept and why, sources |
| `02_Story_Manuscript` | Manuscript (`.md`, plus `.docx` you can edit) |
| `03_Character_References` | Character bible and `character_sheet.png` |
| `04_Illustrations` | All 32 page images at 300 DPI, and painted-edition prompts |
| `05_Page_Layouts` | Page-by-page plan: text, art, character positions, background, text placement, prompt |
| `06_Front_Cover` | Front cover (print and listing sizes), full-wrap art and preview |
| `07_Back_Cover` | Back cover at 300 DPI |
| `08_Print_Ready_PDF` | **Upload these two files to KDP**: interior and full-wrap cover |
| `09_Amazon_SEO` | Titles, description HTML, 7 keywords, categories, ages, bio, price, marketing |
| `10_Final_Publishing_Report` | Final report and the automated preflight report |
| `_build` | Complete source: vector art code, SVG sources, fonts, build scripts |

## Publishing on KDP
Follow section 6 of the final report. In short:
- **Paperback:** Premium Color, 8.5 × 8.5 in, **Bleed**, glossy finish.
- **Upload:** the interior PDF, then the cover PDF.
- **Check and order:** run the KDP Previewer, then order a proof.
- **Publish:** only when you're happy with the proof.

Nothing has been published. That step is yours.

## Changing the book (author name, text, art)
Everything is generated from source, so text, art, PDFs and docs never drift apart.

- **Author / pen name, title, story text, page plan:** `_build/story.py`
- **Characters and colours:** `_build/art.py` (one function per character)
- **Scene compositions:** `_build/scenes.py`
- **Cover:** `_build/cover.py` (art) and `_build/make_pdf.py` (typography)

Rebuild everything and re-run preflight with:
```bash
cd Christmas_KDP_2026/_build
./build.sh            # ~3 minutes; needs python3 (pillow, reportlab, pypdf, pypdfium2, python-docx, numpy),
                      # node with playwright + Chromium, and poppler-utils (pdffonts)
```
`build.sh` exits non-zero if any preflight check fails.

**If you change the page count,** the spine width and cover size update automatically (`cover.py`). Keep the page count a multiple of 2, and at least 24 pages.
