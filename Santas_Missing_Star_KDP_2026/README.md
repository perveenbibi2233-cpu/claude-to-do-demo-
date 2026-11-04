# Where Is Santa's Missing Star?: KDP production

A 32-page, 8.5 × 11 in Christmas search-and-find picture book for ages 3–6.

## Status
| Part | Status |
|---|---|
| Story, 32-page plan, search lists | ✅ Done (`02_Manuscript`, `03_Page_Plan`) |
| Character lock (your sheets, plus specs for Santa and Goldie) | ✅ Done (`01_Character_Lock`) |
| Art prompts, checklist, production guide | ✅ Done (`04_Art_Prompts`) |
| Layout proof (text placed, art boxes empty) | ✅ Done (`06_Layout_Proof/Layout_Proof_ART_PENDING.pdf`) |
| Tools: art sizing, sticker cutting, object placement, answer key, PDF assembly | ✅ Built and tested on dummy images (`_build`) |
| **Illustrations** | ⏳ **Waiting on you.** No image generator was available in this session. 26 images are listed in `04_Art_Prompts/Art_Checklist.md`. |
| Spot-the-difference picture B, answer key, interior PDF, cover PDF, QC report | ⏳ I do these once the art arrives |

Nothing is print-ready yet, and nothing has been published.

## Decisions made in the plan
- **Facing pages.** Page 1 is a right-hand page, so scenes sit on 2–3, 4–5 … 26–27. Copyright moves to the foot of page 32. The bonus is on 28–29 and the answer key on 30–31, so children meet the puzzle before its answers.
- **Friends never count.** Pages 2–3 tell readers that the friends' own scarves, hats, jumpers and bells don't count. That stops Pip's scarf, Tinsel's bell and Mimi from muddying the counts for blue scarves, golden bells and rabbits.
- **Scenes that would break their own counts were adjusted:**
  - The gift room has only 5 wrapped presents.
  - The station's real train has already left, so only toy trains appear.
  - Northern Lights Hill has only the 5 big stars.
  - The tree in the square has garlands but no baubles.
  - The "little birds" are bluebirds, never golden.
- **Tinsel's nose is rosy pink** (changed from red to keep clear of a protected character). Her reference sheet is remade first (prompt C3). The stable's "4 red noses" search target became **4 horseshoes**, and the stable reindeer have ordinary dark noses.

## Rebuild the proof
```bash
cd _build && python3 gen_docs.py && python3 make_book.py proof
```
