# Final Publishing Report: *Juniper and the Little Lost Star*

**Status: print files generated, and every automated KDP technical check passes** (see `preflight_report.txt`, which the build regenerates on every run).
**Not yet published. Nothing has been uploaded to Amazon.** Three items need you before upload (section 4).

## 1. What was delivered
| Deliverable | File |
|---|---|
| Market research and concept selection | `01_Market_Research/Market_Research.md` |
| Read-aloud manuscript (1,013 words) | `02_Story_Manuscript/Manuscript.md`, `Manuscript_Editable.docx` |
| Character bible and visual reference sheet | `03_Character_References/` |
| 32 page illustrations (300 DPI JPEG) and prompts | `04_Illustrations/p01…p32_*.jpg`, `Illustration_Prompts.md` |
| Page-by-page layout plan (text, art, positions, background, prompt) | `05_Page_Layouts/Page_Layout_Plan.md` |
| Front cover (300 DPI, plus a listing image) and full-wrap art | `06_Front_Cover/` |
| Back cover (300 DPI) | `07_Back_Cover/` |
| **KDP interior PDF** (32 pp, 8.625 × 8.75 in with bleed) | `08_Print_Ready_PDF/Juniper_Interior_8.5x8.5_32pp_bleed.pdf` |
| **KDP full-wrap cover PDF** (17.3251 × 8.75 in) | `08_Print_Ready_PDF/Juniper_Cover_FullWrap_17.3251x8.75in.pdf` |
| Listing package (titles, description, keywords, categories, price, marketing) | `09_Amazon_SEO/Amazon_Listing_Package.md` |
| Complete source (vector art code, SVGs, fonts, build pipeline) | `_build/` |

## 2. KDP specifications used (from KDP help pages, checked 4 Nov 2026)
- **Trim** 8.5 × 8.5 in, **bleed** on. The interior PDF page is **8.625 × 8.75 in** (KDP's listed bleed size for this trim).
- **Ink and paper:** premium colour. The 32-page count is above KDP's 24-page paperback minimum.
- **Margins:** KDP's minimum is a 0.375 in gutter for 24–150 pages, and 0.375 in outside margins when bleed is used. The book keeps all text ≥ 0.8 in from the side edges and ≥ 0.6 in from the top and bottom edges. Preflight verifies that no text falls within 0.5 in of any edge on any page.
- **Spine:** 32 × 0.002347 in (premium colour) = **0.0751 in**. No spine text, because KDP prints spine text only on books over 79 pages.
- **Cover:** 0.125 + 8.5 + 0.0751 + 8.5 + 0.125 = **17.3251 in** wide × 8.75 in tall.
- **Barcode:** KDP places a 2 × 1.2 in barcode at the lower right of the back cover. That zone (plus a 0.25 in inset) is verified free of text.
- **Fonts:** Andika and Fredoka (SIL Open Font License, commercial use permitted), all subset-embedded. Licence: `_build/fonts/OFL-Andika.txt`, `OFL-Fredoka.txt`.
- **Images:** every illustration measures exactly 300 DPI at its placed size.

## 3. Quality-control pass (strict editor review)
| Area | Result |
|---|---|
| **Originality** | An original premise, characters, names, village and refrain. Searches turned up a famous mouse called "Nutmeg" and an older "mouse and falling star" book, so the hero became a hedgehog named Juniper. No copyrighted characters. Santa appears only as a generic silhouette. |
| **Grammar and spelling** | Full read-through. US spelling throughout (e.g. "cozy"). Consistent curly quotes and ellipses. |
| **Pacing** | Hook (p5), call to adventure (p8–11), three escalating tries (tree → robin → fox), low point (p17), sacrifice (p18), mentor clue (p19), community climax (p21–24), wonder (p25), gift (p26), bedtime landing (p27–28). |
| **Age fit (3–7)** | Short sentences, sound words (THUMP, PLOP, roly-poly, crunch), a repeated refrain, gentle suspense, no peril or villains. |
| **Emotional payoff** | Setups pay off: Grandma's scarf ("for the Christmas you'll finally see"), "I'm only small" → "tiny Juniper" wakes the whole village, and Glimmer's "Look up!" → the wink. |
| **Character continuity** | Scarf state checked page by page: none before the gift (p5–6), worn p7–17, on Glimmer p18–24, returned p26–28. Glimmer's glow tracks her feelings (bright → pale → brighter → blazing). |
| **Text–image continuity** | Every page's art was composed from its text. Fixes made during QC: removed the scarf from the spring flashback (p6); made Juniper visible in the snowdrift (p15); connected Ember's tail to Ember (p25); moved the moon, streak, chimneys and star away from text (p8, 21, 24, 28, 29). |
| **Layout** | One body size (16.5 pt) on every story page. Text sits only on calm sky or snow. No text over faces. |
| **Cover** | Title readable at thumbnail size. Fixed: an outline style that leaked onto the back blurb, the author name overlapping the art, and a moon behind the blurb. |
| **Metadata** | Title and subtitle match the cover. No keyword stuffing, no trademarks, no "bestseller" claims. |

## 4. Before you upload, three things only you can do
1. **Author name.** "Clara Winterbourne" is a suggested pen name. Set `AUTHOR_NAME` in `_build/story.py` and rebuild (instructions in the README), then edit the bio so it's true.
2. **AI disclosure (required by KDP).** KDP asks whether the text, images or translations are AI-generated. The story text and illustrations here were created with an AI (Claude), and the illustrations were drawn by AI-written code. Answer **"Yes", AI-generated, for both text and images**, unless you substantially rewrite or redraw them yourself. Also note that in the US, purely AI-generated material may have limited copyright protection. Your own revisions and creative changes strengthen your claim.
3. **Order a proof copy** and read it aloud to a child. Check the print colour: deep navy can print darker on premium colour. If it does, lighten `night_top` / `night_mid` in `_build/art.py` and rebuild.

## 5. Honest limitations
- **Illustration style.** No image-generation model or API was available in this environment. The illustrations are original **vector art drawn programmatically**: clean, rounded, flat storybook style with soft gradients and paper grain. That guarantees perfect character consistency and print sharpness, but it's simpler than hand-painted, watercolour-style premium picture books. To upgrade to painted art, give `04_Illustrations/Illustration_Prompts.md` and the character sheet to a human illustrator (recommended for a flagship title) or an image model. The layout, PDFs and preflight rebuild around new images.
- **Market data.** No verified sales figures or rankings were available, so none are quoted. Check live Amazon lists and prices before you set the final price.
- **Not checked automatically.** KDP's online Print Previewer and the cover-calculator template overlay. Run both during upload. KDP may also flag issues its own previewer finds.
- **Prices and print costs** are estimates from KDP help pages and third-party calculators. Confirm them in KDP's pricing tool.

## 6. Upload steps (KDP → Create → Paperback)
1. **Details:** title, subtitle, author, description (HTML from the listing package), seven keywords, three categories, reading age 3–7. Mark the AI disclosure honestly.
2. **Content:**
   - ISBN: free KDP ISBN, or your own.
   - Print options: Premium Color, white paper, 8.5 × 8.5 in, **Bleed**, glossy cover finish (recommended for picture books).
   - Manuscript: upload the interior PDF.
   - Cover: "Upload a cover you already have", then the full-wrap cover PDF.
   - Launch the Previewer and check every page.
3. **Rights and pricing:** set the list price. $11.99 is suggested; check the royalty shown.
4. **Order a proof.** Publish only after the proof looks right. **Nothing is published until you click Publish yourself.**
