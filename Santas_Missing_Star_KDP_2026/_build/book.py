"""Single source of truth for "Where Is Santa's Missing Star?".
Story text, 32-page plan, search targets, art prompts and print geometry all live here;
docs, the layout proof and the final PDFs are generated from it."""

TITLE = "Where Is Santa's Missing Star?"
SUBTITLE = "A Magical Christmas Search-and-Find Adventure"
AUTHOR_NAME = ""          # fill in before final export (left blank on purpose; preflight blocks export while empty)
ISBN = ""                 # optional; KDP can assign a free ISBN. Never invent one.
YEAR = 2026
AGES = "Ages 3–6"

# ------------------------------------------------------------------ print geometry (KDP, 8.5 x 11 in, bleed)
TRIM_W, TRIM_H, BLEED = 8.5, 11.0, 0.125
PAGE_W, PAGE_H = TRIM_W + BLEED, TRIM_H + 2 * BLEED          # 8.625 x 11.25 in PDF page
DPI = 300
SPREAD_PX = (round((2 * TRIM_W + 2 * BLEED) * DPI), round(PAGE_H * DPI))   # 5175 x 3375
PAGE_PX = (round(PAGE_W * DPI), round(PAGE_H * DPI))                         # 2588 x 3375
PAGES = 32
SPINE = round(PAGES * 0.002347, 4)                                          # premium colour
COVER_W, COVER_H = 2 * TRIM_W + SPINE + 2 * BLEED, PAGE_H                   # 17.3251 x 11.25 in

# ------------------------------------------------------------------ art direction
STYLE = ("Warm, polished 2D children's picture-book illustration with soft painterly brush textures and gentle shading, "
         "richly detailed cozy Christmas environment, glowing golden light, bright harmonious colours, cute expressive characters. "
         "Not 3D, not photorealistic, not flat vector clip art. No text, letters, numbers, signatures or watermarks anywhere in the image.")

LOCK = {
    "Pip": "Pip: small orange-red fox cub (the hero, our height reference), rounded soft body, large rounded head, large warm amber-brown eyes, "
           "upright triangular ears with dark brown tips and cream insides, cream muzzle and chest, tiny dark brown nose, dark brown lower legs and paws, "
           "big fluffy orange-red tail with cream-white tip, teal knitted scarf with small white snowflake motifs wrapped twice around the neck with two fringed ends on the chest. "
           "No other clothing.",
    "Mimi": "Mimi: petite fluffy round white rabbit, about two-thirds of Pip's height, large violet-brown eyes, long upright white ears with pink insides, "
            "tiny pink triangular nose, small round tail, lavender cable-knit winter hat with a round lavender pom-pom, ears poking up through the hat. No other clothing.",
    "Bramble": "Bramble: round, sturdy chestnut-brown bear cub, a little taller and wider than Pip, small round ears, honey-brown eyes, cream muzzle, dark brown nose, "
               "rounded paws, bright red knitted Christmas jumper with a large white snowflake on the chest and white Nordic pattern bands. No hat or scarf.",
    "Tinsel": "Tinsel: small, slightly plump caramel-brown baby reindeer, about Pip's shoulder height, cream muzzle and chest, small cream spots on her back, "
              "large dark brown eyes with lashes, tiny symmetrical light-brown branching antlers, soft rosy-pink round nose (rosy pink, NOT red), dark chocolate hooves, fluffy cream-tipped tail, "
              "red collar with one small golden bell. No other accessories.",
    "Santa": "Santa Claus: kind elderly man (about 65–70), tall and broad with a gentle round belly, rosy cheeks, warm dark blue eyes, thick fluffy white eyebrows, "
             "full fluffy white beard to his upper chest, white hair at the sides, pinkish-red round nose, bright red coat and trousers with white fur trim, "
             "red Santa hat with white pom-pom, wide black belt with golden buckle, black boots, white gloves.",
    "Goldie": "Goldie: a very tiny round fluffy golden-yellow bird (small enough to sit in Pip's front paws), buttery-yellow feather highlights, large sparkling dark brown eyes, "
              "small orange-yellow beak, short rounded wings, three short golden tail feathers, tiny orange feet, a small feather crest. No clothing.",
}

FRIENDS_RULE = "Psst! Our friends' own scarves, hats, jumpers and bells don't count."

# Target "method": sticker = drawn separately and placed by the layout tool (exact count guaranteed);
#                  scene   = must be painted into the scene by the image tool with the exact count, then hand-verified.
T = lambda n, name, method="sticker", note="": dict(n=n, name=name, method=method, note=note)

SPREADS = [
    dict(pages=(2, 3), key="s01_missing_star", title="The Missing Star", search=False,
         text=["It was Christmas Eve at the North Pole, and the whole village sparkled.",
               "Santa looked up at his enormous Christmas tree and gasped. “Oh my snowflakes! My golden star is gone!”",
               "Pip the little fox stepped forward. “Don't worry, Santa. We'll find it!”",
               "“We'll help too!” said Mimi, Bramble and Tinsel."],
         extra="Look for clues on every page, and find all the hidden objects along the way!",
         scene="Santa's snowy Christmas village at dusk: candy-coloured cottages with glowing windows, Santa's enormous Christmas tree in the town square, dressed in garlands and warm fairy lights (no baubles yet), with an EMPTY treetop (no star). "
               "Right page: Santa stands beside the tree, hands on his cheeks in surprise, looking up at the empty top. Pip stands in front of Santa, chest out, brave and determined, "
               "with Mimi, Bramble and Tinsel gathered close behind him looking up. Left page: the village street leading to the square, lantern light, gentle falling snow.",
         chars=["Santa", "Pip", "Mimi", "Bramble", "Tinsel"]),

    dict(pages=(4, 5), key="s02_toy_workshop", title="Santa's Toy Workshop",
         text=["First stop: Santa's Toy Workshop! Hammers tapped and paintbrushes swished.",
               "“Look!” whispered Mimi. Something shiny lay on a workbench.",
               "It was a golden feather. “A clue!” said Pip."],
         targets=[T(3, "teddy bears"), T(4, "red toy trains"), T(2, "golden bells"), T(5, "candy canes"), T(1, "golden feather")],
         scene="A cozy wooden toy workshop: long workbenches with tools, paint pots and wood shavings, shelves of half-finished toys (wooden boats, spinning tops, kites, rocking horse, blocks), "
               "a crackling fireplace, frosty windows. Pip leans over a workbench pointing; Mimi beside him; Bramble holding a paintbrush with a little paint on his nose; Tinsel peeking over a toy box.",
         chars=["Pip", "Mimi", "Bramble", "Tinsel"]),

    dict(pages=(6, 7), key="s03_candy_cane_village", title="Candy Cane Village",
         text=["Next they hurried to Candy Cane Village. The streets smelled of peppermint!",
               "“Mmm, gingerbread,” sniffed Bramble. “Focus, Bramble!” giggled Tinsel.",
               "Then Pip saw a tiny golden sparkle shaped just like a star. “The star came this way!”"],
         targets=[T(5, "striped candy canes"), T(3, "snowmen"), T(4, "red mittens"), T(2, "gingerbread men"), T(1, "tiny golden star clue")],
         scene="A sweet, snowy village street of pastel cottages with icing-like snow on the roofs, lollipop-shaped street lamps, peppermint-swirl paving, gumdrop bushes, a frozen fountain. "
               "Pip in the middle of the street looking down excitedly; Bramble sniffing the air dreamily; Tinsel nudging Bramble and giggling; Mimi pointing ahead.",
         chars=["Pip", "Mimi", "Bramble", "Tinsel"]),

    dict(pages=(8, 9), key="s04_reindeer_stable", title="The Reindeer Stable",
         text=["In the Reindeer Stable, everyone was getting ready for the big night.",
               "“This is where I live!” said Tinsel proudly.",
               "Tucked in the straw was another golden feather. “Who keeps dropping feathers?” wondered Mimi."],
         targets=[T(4, "horseshoes", "sticker", "Shiny horseshoes hanging on the walls or lying in the straw."),
                  T(3, "golden bells"), T(5, "carrots"), T(2, "blue scarves", "sticker", "Royal blue, clearly different from Pip's teal scarf; hanging on pegs."),
                  T(1, "golden feather")],
         scene="A warm wooden stable with four stalls, hay bales, straw on the floor, harness straps and red blankets on pegs, lanterns, a hayloft ladder, snow visible through the big open door. "
               "Four grown-up reindeer with ordinary dark brown noses stand in the stalls, friendly and smiling. Tinsel prances proudly in front; Pip and Mimi look around; Bramble pats a hay bale.",
         chars=["Pip", "Mimi", "Bramble", "Tinsel"]),

    dict(pages=(10, 11), key="s05_snowflake_forest", title="Snowflake Forest",
         text=["The friends tiptoed into Snowflake Forest. Snow sparkled on every branch.",
               "“Feathers... and a falling star,” said Mimi slowly. “I think a little bird is part of this mystery!”"],
         targets=[T(6, "big snowflakes", "sticker", "Large, sparkly six-pointed snowflake shapes. Ordinary falling snow is soft round dots only."),
                  T(3, "pinecones"), T(4, "red berries", "sticker", "Single shiny red berries, easy to see."),
                  T(2, "little birds", "sticker", "Small bluebirds (blue and white). Never golden."), T(1, "golden feather")],
         scene="A magical snowy forest of tall birch and fir trunks with snow-laden branches, soft blue-violet shadows, a winding path, a little frozen stream, gentle soft-dot snowfall. "
               "Mimi in the middle, paw on chin, thinking; Pip listening; Bramble making a snow angel; Tinsel hopping through a snowdrift.",
         chars=["Pip", "Mimi", "Bramble", "Tinsel"]),

    dict(pages=(12, 13), key="s06_gift_room", title="Santa's Gift Room",
         text=["In Santa's Gift Room, ribbons and wrapping paper were everywhere!",
               "Bramble tried to peek inside a box. “No peeking!” laughed Tinsel.",
               "Behind a drum, Pip found another twinkle of stardust. “We're getting closer!”"],
         targets=[T(5, "wrapped presents", "sticker", "The ONLY wrapped presents in the room. Everything else is open sacks, unwrapped boxes and rolls of paper."),
                  T(3, "toy drums"), T(4, "golden ribbons", "sticker", "Golden bows."), T(2, "wooden dolls"), T(1, "tiny golden star clue")],
         scene="A bright attic-style gift room with tall shelves of empty boxes, big open sacks of toys, rolls of colourful wrapping paper, spools of red and green ribbon, scissors, tape, a big list scroll pinned to the wall (no readable writing). "
               "Bramble lifting a box lid with one eye peeking; Tinsel laughing; Pip crouching low, pointing behind something; Mimi on tiptoe beside a shelf.",
         chars=["Pip", "Mimi", "Bramble", "Tinsel"]),

    dict(pages=(14, 15), key="s07_gingerbread_bakery", title="The Gingerbread Bakery",
         text=["Sniff, sniff! Bramble led the way to the Gingerbread Bakery. Warm treats cooled on every shelf.",
               "“Just one little taste?” asked Bramble.",
               "Then everyone gasped. A golden feather was floating in through the window!"],
         targets=[T(4, "gingerbread cookies", "sticker", "Round or star-shaped gingerbread cookies with white icing (not people-shaped)."),
                  T(3, "cupcakes"), T(5, "candy canes"), T(2, "rolling pins"), T(1, "golden feather")],
         scene="A cozy bakery with a big brick oven glowing orange, wooden counters dusted with flour, loaves of bread, pies, jars of sprinkles, mixing bowls and whisks, a window with snow outside. "
               "Bramble at the front with his eyes closed blissfully sniffing; Pip, Mimi and Tinsel looking up toward the window, mouths open in surprise.",
         chars=["Pip", "Mimi", "Bramble", "Tinsel"]),

    dict(pages=(16, 17), key="s08_frozen_ice_lake", title="The Frozen Ice Lake",
         text=["The feather drifted toward the Frozen Ice Lake, where penguins were sliding in swirly circles.",
               "Tinsel tried sliding too... wheee! All the way across on her tummy!",
               "Everyone laughed. And there on the ice glimmered another golden feather."],
         targets=[T(4, "penguins"), T(3, "ice skates", "sticker", "Single ice skates lying on the snow or ice; penguins do NOT wear skates."),
                  T(5, "snowballs"), T(2, "blue fish", "sticker", "Visible under clear patches of ice or held up by a penguin."), T(1, "golden feather")],
         scene="A wide frozen lake under a pale pink-and-gold winter sky, snowy banks with fir trees, a little wooden jetty, swirly skate marks on the ice, clear blue patches of ice. "
               "Tinsel sliding happily on her tummy across the ice; Pip, Mimi and Bramble on the bank laughing.",
         chars=["Pip", "Mimi", "Bramble", "Tinsel"]),

    dict(pages=(18, 19), key="s09_train_station", title="The Christmas Train Station",
         text=["Toot, toot! At the Christmas Train Station, the Holly Express had just puffed away.",
               "Mimi studied the sparkly trail. “The stardust goes up, up, up the hill!”"],
         targets=[T(5, "toy trains", "sticker", "Small toy trains. NO full-size train in the scene: the real train has already left."),
                  T(4, "red lanterns"), T(3, "suitcases"), T(2, "snowmen"), T(1, "tiny golden star clue")],
         scene="A charming snowy station platform with a wooden canopy, benches, a big round station clock (no numbers), an empty track curving away, a puff of steam far in the distance on the hillside, "
               "a little toy kiosk, parcels and a luggage trolley. Mimi kneeling to look at the sparkly trail on the platform; Pip, Bramble and Tinsel following her gaze up the hill.",
         chars=["Pip", "Mimi", "Bramble", "Tinsel"]),

    dict(pages=(20, 21), key="s10_northern_lights_hill", title="Northern Lights Hill",
         text=["Up on Northern Lights Hill, the sky danced green and purple.",
               "Two little rabbits were fast asleep in the snow. “Shh!” whispered Mimi.",
               "On the hilltop lay one more golden feather, pointing back toward town!"],
         targets=[T(5, "stars", "sticker", "The ONLY stars: five big golden stars. The sky has aurora ribbons but no other star dots."),
                  T(3, "pine trees", "scene", "Exactly three pine trees on the hill."),
                  T(4, "snowflakes", "sticker", "Large sparkly snowflake shapes."),
                  T(2, "sleeping rabbits", "sticker", "Brown wild rabbits curled up asleep. Mimi is awake and doesn't count."),
                  T(1, "golden feather")],
         scene="A rounded snowy hilltop at night under swirling green and purple northern lights (aurora ribbons only, no star dots in the sky), the glowing village far below, EXACTLY THREE pine trees on the hill. "
               "Mimi with a finger to her lips; Pip pointing at the hilltop; Bramble tiptoeing exaggeratedly; Tinsel gazing at the sky.",
         chars=["Pip", "Mimi", "Bramble", "Tinsel"]),

    dict(pages=(22, 23), key="s11_tree_square", title="Christmas Tree Square",
         text=["Back in Christmas Tree Square, everyone was busy decorating.",
               "Pip looked high. Pip looked low. Then he heard a tiny “Tweet!” from a snowy fir tree nearby.",
               "“Follow me,” he whispered."],
         targets=[T(6, "Christmas ornaments", "sticker", "Round baubles. The big tree has garland and lights only, no other baubles."),
                  T(4, "wrapped presents"), T(3, "golden bells"), T(2, "little birds", "sticker", "Small bluebirds, never golden."),
                  T(1, "tiny golden star clue")],
         scene="The town square at evening: Santa's enormous Christmas tree with garlands and warm fairy lights (no baubles) and an empty treetop, a ladder against it, cottages around, a snowy fir tree at one side. "
               "Pip in the centre with one ear turned toward the fir tree, a paw raised to say shh; Mimi, Bramble and Tinsel behind him leaning in to listen.",
         chars=["Pip", "Mimi", "Bramble", "Tinsel"]),

    dict(pages=(24, 25), key="s12_goldies_secret", title="Goldie's Secret", search=False,
         text=["In the branches of the fir tree sat a tiny nest. Bramble lifted Pip up to see.",
               "Inside was a tiny golden bird, and beside her, safe and sound, was Santa's golden star!",
               "“Did you take the star?” Pip asked gently.",
               "“Oh no,” peeped the bird. “I'm Goldie. The wind blew the star off the tree. I flew all over the village looking for a safe place to keep it, and I lost a few feathers on the way!”"],
         scene="Close, warm scene in a snowy fir tree at evening: a cozy nest of twigs and moss on a sturdy branch. Inside the nest sits tiny Goldie, and beside her the big shining golden five-pointed star, glowing softly. "
               "Bramble stands below holding Pip up on his shoulders so Pip is eye-level with the nest; Pip looks at Goldie with a gentle, kind face. Mimi and Tinsel watch from below. A few loose golden feathers on the branch.",
         chars=["Pip", "Bramble", "Mimi", "Tinsel", "Goldie"]),

    dict(pages=(26, 27), key="s13_celebration", title="The Christmas Celebration", search=False,
         text=["Santa smiled his warmest smile. “Thank you, Goldie. You kept my star safe, and that was very kind.”",
               "Santa lifted Pip high, and Pip placed the star on top of the tree. It glowed brighter than ever!",
               "“Will you join our celebration, Goldie?” asked Santa. “Yes, please!” she chirped.",
               "And the whole village cheered."],
         scene="Joyful celebration in the town square at night: the enormous Christmas tree now topped with the shining golden star. Santa holds Pip up high near the treetop as Pip sets the star in place; "
               "Goldie flutters beside them. Below, Mimi, Bramble and Tinsel hang the last decorations and cheer; warm lights, gentle snow, glowing cottage windows.",
         chars=["Santa", "Pip", "Goldie", "Mimi", "Bramble", "Tinsel"]),
]

SINGLES = {
    1: dict(key="p01_title", label="Title page",
            scene="Portrait title illustration: the enormous decorated Christmas tree glowing at night with the golden star on top; Santa, Pip, Mimi, Bramble, Tinsel and tiny Goldie gathered happily at its base. "
                  "Keep the TOP THIRD calm (night sky) for the title.",
            chars=["Santa", "Pip", "Mimi", "Bramble", "Tinsel", "Goldie"]),
    32: dict(key="p32_goodnight", label="Christmas message + copyright",
             scene="Portrait closing illustration: Pip, Mimi, Bramble, Tinsel and Goldie snuggled together on a snowy bench under a lamplight, the star-topped tree glowing in the distance. "
                   "Keep the TOP THIRD calm for the message, and the BOTTOM 2 inches plain snow for small copyright text.",
             chars=["Pip", "Mimi", "Bramble", "Tinsel", "Goldie"]),
}

MESSAGE = "Merry Christmas! May your days be filled with kindness, friendship, and a little Christmas magic."

SPOT_DIFF = dict(pages=(28, 29), key="s14_spot_difference",
                 text="Bonus! Pip and his friends took two pictures at the party. Can you spot 5 differences?",
                 scene="Square illustration (1:1): Pip, Mimi, Bramble, Tinsel and Goldie posing together in front of the star-topped Christmas tree, simple clear background, large readable shapes (this will be used for a spot-the-difference game).",
                 chars=["Pip", "Mimi", "Bramble", "Tinsel", "Goldie"],
                 differences=None)   # filled in by me when I make the second picture from your image

PAGE_ORDER = (["1: Title page"] + [f"{a}–{b}: {s['title']}" for s in SPREADS for a, b in [s["pages"]]]
              + ["28–29: Bonus spot-the-difference", "30–31: Answer key", "32: Christmas message + copyright"])

# ------------------------------------------------------------------ sticker sheets (objects placed by the layout tool)
STICKER_SHEETS = {
    "sheet_A_toys":    ["teddy bear", "red toy train", "toy drum", "wooden doll", "wrapped present with ribbon", "golden bell"],
    "sheet_B_treats":  ["red-and-white striped candy cane", "gingerbread man", "round iced gingerbread cookie", "cupcake with frosting", "wooden rolling pin", "carrot"],
    "sheet_C_winter":  ["small snowman", "red mitten", "royal-blue knitted scarf", "snowball", "single ice skate", "red lantern", "small suitcase", "shiny horseshoe"],
    "sheet_D_nature":  ["large sparkly snowflake", "pinecone", "single shiny red berry", "small bluebird", "brown wild rabbit curled up asleep", "penguin", "blue fish"],
    "sheet_E_golden":  ["golden feather", "tiny golden star with sparkles", "big shiny golden star", "round Christmas bauble ornament", "golden ribbon bow"],
}


def word_count():
    import re
    txt = " ".join(" ".join(s["text"]) for s in SPREADS) + " " + MESSAGE
    return len(re.findall(r"[A-Za-z']+", txt))


if __name__ == "__main__":
    print("story words:", word_count())
    for p in PAGE_ORDER:
        print(p)
