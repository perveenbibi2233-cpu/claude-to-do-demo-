"""Single source of truth for the book: metadata, story text and the 32-page plan.
Edit AUTHOR_NAME (pen name) here, then rebuild with ./build.sh."""

TITLE = "Juniper and the Little Lost Star"
SUBTITLE = "A Cozy Christmas Eve Adventure"
AUTHOR_NAME = "Clara Winterbourne"   # <- pen name; change to your own name or pen name before publishing
YEAR = 2026
AGES = "Ages 3–7"

STYLE = ("Soft, rounded flat-vector children's picture-book illustration, gentle gradients, subtle paper grain, "
         "deep navy night skies, blue-white snow, warm golden window light, rich holly reds and pine greens, "
         "cozy and magical, no text, no watermark, square 1:1 full-bleed composition")

CHARACTER_LOCK = {
    "Juniper": "Juniper: a small young hedgehog (age ~5 in story terms), front-facing, egg-shaped cream face and belly, "
               "chocolate-brown spikes with lighter caramel tips forming a halo, a signature tuft of three lighter spikes on top of her head, "
               "small round ears with pink insides, big glossy black oval eyes with white highlights, rosy cheeks, small black button nose on a pale snout, "
               "short cream arms, brown oval feet; wears a holly-red knitted scarf with two white stripes and fringe on the right-hand tail (except where noted)",
    "Glimmer": "Glimmer: a small five-pointed star with softly rounded points, glowing golden yellow (pale and dim when sad or cold), "
               "simple kawaii face: two small black oval eyes, tiny smile, pink cheeks; surrounded by a soft golden glow",
    "Grandma": "Grandma Hedgehog: same build as Juniper but silver-grey spikes, round brown spectacles, lavender knitted shawl",
    "Ruby": "Ruby: a plump round robin, brown back, bright orange-red breast and face, golden beak, black bead eye",
    "Ember": "Ember: a friendly red fox, side view, orange coat, white chest and muzzle, dark brown socks and ear tips, huge bushy tail with white tip",
    "Oakley": "Old Oakley: a large round grey owl, pale lavender-grey belly with chevron markings, cream face discs, big amber eyes, white eyebrow tufts, ear tufts",
}

# ---------------------------------------------------------------------------------------------
# kind: art   = full-bleed illustration with story text (text_pos top|bottom, text_color light|dark)
#       front = front/back matter page (cream background, spot illustration)
PAGES = [
    dict(n=1, kind="front", scene="fm_belongs", label="This Book Belongs To"),
    dict(n=2, kind="front", scene="fm_title", label="Title page"),
    dict(n=3, kind="front", scene="fm_copyright", label="Copyright page"),
    dict(n=4, kind="front", scene="fm_dedication", label="Dedication"),

    dict(n=5, scene="s05", text_pos="top", text_color="light",
         text="Juniper the hedgehog had never, ever seen Christmas.\n\nEvery year, when the first frost came, her eyes grew heavy. She curled into a prickly ball in her cozy burrow under the old holly tree... and she slept right through it.",
         desc="Cross-section of a cozy underground burrow lit by a lantern. Juniper sleeps curled in a ball on a bed of autumn leaves; Grandma Hedgehog dozes nearby with red yarn. A round window shows the first frosty night.",
         chars="Juniper (curled ball) centre-bottom on leaf bed; Grandma right foreground; yarn ball beside Grandma.",
         bg="Earthen burrow walls with roots, round window (night, stars, snow) left, glowing lantern right, red oval rug.",
         prompt="Cozy underground hedgehog burrow at night, cross-section, lantern glow; little hedgehog Juniper curled asleep in a ball on autumn leaves, no scarf; Grandma Hedgehog dozing beside a ball of red yarn; round window showing frosty starry night; floating 'z' sleep marks."),
    dict(n=6, scene="s06", text_pos="top", text_color="dark",
         text="Every spring, Juniper asked the same question.\n\n“Grandma, what is Christmas like?”\n\n“Oh, it sparkles,” said Grandma. “The windows glow like little suns. And high above Hollyberry Village shines one special star, to show Santa the way.”",
         desc="Bright spring meadow full of flowers. Grandma raises her arms as she describes Christmas; Juniper listens wide-eyed. A dream bubble shows a snowy village with glowing windows and a smiling star above.",
         chars="Juniper left foreground (no scarf yet); Grandma right foreground, arms raised; thought bubble centre.",
         bg="Pale blue spring sky, soft sun top-right, rolling green hills, scattered daisies.",
         prompt="Sunny spring meadow with flowers; Grandma Hedgehog (spectacles, lavender shawl) excitedly describing Christmas, arms raised; little hedgehog Juniper without a scarf listening in awe; a cloud-shaped thought bubble showing a snowy village with glowing windows and one smiling golden star."),
    dict(n=7, scene="s07", text_pos="top", text_color="light",
         text="“One day,” Juniper whispered, “I'll see it.”\n\nThis winter, Grandma knitted her a scarf, red as holly berries, with two white stripes.\n\n“For the Christmas you'll finally see,” she said, and tucked her in.\n\nJuniper yawned the biggest yawn. Her eyes went close... close... closed.",
         desc="Inside the burrow. Juniper, now wearing her new red striped scarf, yawns hugely under a blanket of leaves. Grandma, eyes closed in a contented smile, has just tucked her in.",
         chars="Juniper right of centre in leaf bed, yawning, arms hugging; Grandma left.",
         bg="Burrow interior mirrored from page 5: lantern left, round night window right.",
         prompt="Inside the cozy burrow: little hedgehog Juniper wearing her brand-new holly-red scarf with two white stripes, yawning sleepily under a blanket of autumn leaves; Grandma Hedgehog smiling with closed eyes after tucking her in; lantern glow."),
    dict(n=8, scene="s08", text_pos="top", text_color="light",
         text="Then, on the darkest night of the whole year...\n\nTHUMP!\n\nSomething bumped against the burrow door. Something small. Something bright.",
         desc="Snowy night outside. A golden streak arcs down from the sky and ends in a surprised little star landing in the snow beside the holly tree's round burrow door.",
         chars="Glimmer small, surprised, lower right of centre in sparkles; no other characters.",
         bg="Starry navy sky, pine forest silhouette, the old holly tree with berries and snow, round wooden burrow door.",
         prompt="Snowy starry night; a golden streak of light falling from the sky ending in a tiny surprised star with a face landing in the snow beside a round wooden door under a big snowy holly tree; sparkles; pine forest behind."),
    dict(n=9, scene="s09", text_pos="top", text_color="light",
         text="Juniper opened one eye. Then the other.\n\nGolden light was peeking through the door. She tiptoed outside, into her very first snow. It was soft and sparkly, and much, much colder than she had ever imagined.\n\n“Ooh! Cold, cold, COLD!” she squeaked, hopping from foot to foot.",
         desc="Juniper hops on the snow with her arms up and eyes wide, her open burrow door glowing behind her. A mysterious golden glow shines from the right edge.",
         chars="Juniper centre, mid-hop, arms up, mouth 'o'; burrow and holly tree left.",
         bg="Night sky, pine row, falling snowflakes, warm glow from open burrow door, golden light from the right.",
         prompt="Little hedgehog Juniper in her red striped scarf hopping in her very first snow with arms raised and wide surprised eyes, open glowing burrow door behind her under a holly tree; snowflakes falling; mysterious golden glow at the right."),
    dict(n=10, scene="s10", text_pos="top", text_color="light",
         text="“Hello?” Juniper called softly.\n\nThere, in a little dip in the snow, sat a tiny star.\n\nIt had a sweet round face, and it was sniffling.\n\n“Oh no, oh no,” said the star. “I fell down, and I can't get back up!”",
         desc="Close-up: Glimmer sits in a dip in the snow, teary and sad, glowing softly. Juniper leans in, wide-eyed and concerned.",
         chars="Juniper left, looking right toward Glimmer; Glimmer right of centre in a snow dip.",
         bg="Night sky with stars, smooth snow field, a few snowflakes.",
         prompt="Close-up snowy night: a tiny sad golden star with a teardrop sitting in a dip in the snow; little hedgehog Juniper in red striped scarf leaning toward it with wide worried eyes."),
    dict(n=11, scene="s11", text_pos="bottom", text_color="dark",
         text="“I'm Glimmer,” said the star. “I'm Hollyberry's star. Tonight is Christmas Eve, and if I'm not back in the sky by midnight, Santa won't find the village!”\n\nGlimmer's light flickered... and dimmed... just a little.\n\n“What can I do?” Juniper wondered. “I'm only small.”",
         desc="Glimmer floats above a sleeping village with dark windows, pale and dimming. High in the sky a dotted star outline marks her empty place. Juniper looks up, worried.",
         chars="Juniper left middle; Glimmer centre, pale; dotted outline top-right.",
         bg="Starry sky, dark sleeping cottages and pines on the horizon, snow field (text area).",
         prompt="Night scene: a pale, dimming little star with a worried face floating above a sleepy snowy village with dark windows; a dotted empty star outline high in the sky where it belongs; little hedgehog Juniper in red striped scarf looking up worried; snowy foreground left clear for text."),
    dict(n=12, scene="s12", text_pos="top", text_color="light",
         text="Juniper's tummy did a flip. No Santa? No sparkle? Not on the one Christmas she was finally awake for!\n\nShe held up her paws.\n\n“Little light, little light, don't you fade tonight,” she said. “I'll help you home.”",
         desc="Juniper stands tall and brave, arms raised, big determined grin. Glimmer hovers above her paws, a little brighter, surrounded by sparkles.",
         chars="Juniper centre, large; Glimmer floating directly above.",
         bg="Night sky, pine row, snow.",
         prompt="Brave little hedgehog Juniper in red striped scarf standing tall with both paws raised and a determined grin; small golden star Glimmer hovering above her paws with sparkles; snowy pine forest at night."),
    dict(n=13, scene="s13", text_pos="top", text_color="light",
         text="But how do you carry a star? Glimmer was too warm for paws.\n\n“Hop on my prickles!” said Juniper.\n\nGlimmer settled between her spines, snug as a button.\n\n“Hee hee!” giggled Glimmer. “You're like a pincushion!”\n\nOff they went, crunch, crunch, crunch, through the snow.",
         desc="Glimmer rides happily on Juniper's spikes like a little badge; Juniper grins and peeks back at her.",
         chars="Juniper centre, large; Glimmer tucked in the spikes at upper right of her head.",
         bg="Night sky, pine row, snow.",
         prompt="Little hedgehog Juniper in red striped scarf grinning and glancing back at a tiny happy golden star nestled among the spikes on her back like a pincushion; snowy night forest."),
    dict(n=14, scene="s14", text_pos="bottom", text_color="dark",
         text="First, Juniper tried the holly tree. She climbed up, up, up... all the way to the third branch.\n\nThen she looked down. “Oh my,” she said, and climbed back down, very carefully.\n\nThe sky was still far, far away.",
         desc="The big holly tree under a full sky of stars. Juniper clings nervously to a low branch with Glimmer just above her; the sky stretches far overhead.",
         chars="Juniper hugging the branch left of the trunk; Glimmer tiny above her.",
         bg="Huge starry sky, moon top-left, holly tree with burrow door, snow foreground (text area).",
         prompt="Tall snowy holly tree with a round burrow door at its base under a vast starry sky; little hedgehog Juniper in red scarf clinging nervously to a low branch with a tiny pale star above her; snowy foreground clear for text."),
    dict(n=15, scene="s15", text_pos="top", text_color="light",
         text="“Need a lift?” chirped Ruby the robin.\n\nShe grabbed Juniper's scarf and flapped with all her might. Flap, flap, FLAP! Juniper rose one... two... three inches...\n\n...and PLOP! Into a snowdrift.\n\n“Perhaps,” puffed Ruby, “you're a little too prickly for flying.”",
         desc="Comic moment: Juniper is upside-down in a snowdrift, feet and scarf sticking out, snow puffing up. Ruby flutters above, out of breath. Glimmer looks on, surprised.",
         chars="Juniper upside-down centre in drift; Ruby flying above right; Glimmer left.",
         bg="Night sky, pine row, big white snowdrift.",
         prompt="Funny snowy night scene: little hedgehog upside-down in a big white snowdrift with only her feet and red striped scarf showing, snow puffs flying; a plump robin fluttering above out of breath; a tiny surprised star watching."),
    dict(n=16, scene="s16", text_pos="top", text_color="light",
         text="Out from behind a pine tree trotted a fox with a tail like a torch.\n\n“I'm Ember,” he said. “The highest place I know is the top of Hollyberry Hill. Hold on!”\n\nJuniper held on tight, and away they bounded, whoosh, whoosh, whoosh, over the moonlit snow.",
         desc="Ember races across moonlit snow with Juniper riding on his back and Glimmer on her spikes; motion lines and kicked-up snow.",
         chars="Ember centre, running right; Juniper on his back; Glimmer on Juniper's spikes.",
         bg="Big moon right, layered snowy hills with pines, kicked-up snow.",
         prompt="A friendly red fox bounding across moonlit snowy hills with a little hedgehog in a red striped scarf riding on his back and a tiny star tucked in her spikes; big glowing moon; speed lines and snow spray."),
    dict(n=17, scene="s17", text_pos="top", text_color="light",
         text="From the top of the hill, they could see the whole village below. But the sky was still far, far away.\n\nEmber's ears drooped. Juniper's heart felt heavy, too. And Glimmer was growing paler.\n\n“I'm so cold,” she whispered. “And so far from home.”",
         desc="On the hilltop, Juniper and Ember look out over the dark sleeping village below. Glimmer is very pale and sad. The sky is enormous.",
         chars="Ember right facing left; Juniper centre-right; Glimmer pale above Juniper.",
         bg="Vast starry sky, distant valley village with dark windows, snowy hilltop foreground right.",
         prompt="Snowy hilltop at night overlooking a tiny sleeping village with dark windows far below; a red fox and a little hedgehog in red scarf small in the frame; a very pale, sad little star; enormous starry sky."),
    dict(n=18, scene="s18", text_pos="top", text_color="light",
         text="Juniper didn't think twice. She unwound her brand-new scarf and wrapped it around Glimmer, gently, gently. The wind nipped at Juniper's neck, but she didn't mind one bit.\n\n“There,” said Juniper. “Now you're not cold. And you're not alone.”\n\nGlimmer's light flickered warmer.",
         desc="Juniper, without her scarf, hugs her arms and smiles; Glimmer now wears the red striped scarf and glows warmer. Ember sits behind, eyes closed, smiling.",
         chars="Juniper left-centre, large, no scarf; Glimmer right-centre wearing scarf; Ember far right.",
         bg="Night sky, snowy hilltop.",
         prompt="Tender moment on a snowy hill at night: little hedgehog without her scarf smiling, having wrapped her red striped scarf around a small golden star who now glows warmer; red fox sitting nearby smiling with closed eyes."),
    dict(n=19, scene="s19", text_pos="bottom", text_color="dark",
         text="“Whooo is out so late?” A great grey owl landed on a branch. It was Old Oakley, the wisest bird in the wood.\n\nJuniper told him everything, all in one big breath. Oakley blinked his big moon eyes. “Stars don't rise by climbing or flying,” he said. “Stars rise on light. And Glimmer needs more light than she has left.”",
         desc="Old Oakley perches on a snowy branch across the top of the scene, looking down. Ember, Juniper and scarf-wrapped Glimmer gaze up at him.",
         chars="Oakley upper left on branch; Ember and Juniper middle right; Glimmer above Juniper.",
         bg="Moon top-right, snowy branch, snow field (text area).",
         prompt="Large round grey owl with big amber eyes perched on a snowy branch at night, looking down kindly; a red fox, a little hedgehog without scarf and a small star wearing a red striped scarf looking up at him; full moon; snowy foreground clear for text."),
    dict(n=20, scene="s20", text_pos="top", text_color="light",
         text="Juniper looked down at Hollyberry Village. Every window was dark. Everyone was fast asleep.\n\n“Then we'll wake up the light!” she said.\n\nShe left Glimmer safe with Oakley and tumbled down the hill, roly-poly, roly-poly, all the way to the village.",
         desc="Juniper rolls down the long snowy slope as a spiky ball toward the dark village; Oakley and Glimmer watch from a branch on the hilltop.",
         chars="Juniper (ball) centre-right on slope; Oakley and Glimmer small, upper left.",
         bg="Night sky, dark village on the horizon, long diagonal snow slope with a dashed roll trail.",
         prompt="Little hedgehog rolled into a spiky ball tumbling down a long snowy slope toward a dark sleeping village, dashed trail behind her; an owl holding a tiny star in a red scarf watching from a branch on the hilltop."),
    dict(n=21, scene="s21", text_pos="top", text_color="light",
         text="Tap, tap, tap! Ruby pecked at the windows. Ember yipped at the doors. At first, nothing happened.\n\nSo Juniper, tiny Juniper, stood in the snow and sang as loud as she could:\n\n“Little light, little light, won't you shine tonight?”",
         desc="A village street at night with two big dark cottages. Ruby taps on a window, Ember yips at a door, and Juniper sings with her arms up as musical notes float upward.",
         chars="Ember left; Juniper centre singing; Ruby at right-hand window.",
         bg="Two large snowy cottages with dark windows, starry sky, snowy street.",
         prompt="Snowy village street at night with two cottages with dark windows; a robin tapping on a window, a red fox yipping at a door, and a little hedgehog without scarf singing with arms raised as glowing musical notes float up."),
    dict(n=22, scene="s22", text_pos="top", text_color="light",
         text="One window glowed. Then another. Then the bakery, and the school, and the little blue house at the end of the lane.\n\nA little girl held up a candle. A grandpa switched on the tree lights. A baby's night-light blinked on.\n\nSoon every window in Hollyberry Village was glowing like a little sun.",
         desc="The whole village lights up: rows of cottages with glowing golden windows, wreaths on doors, small silhouettes holding candles. The three friends watch from the snowy street.",
         chars="Ember, Juniper and Ruby small at bottom centre.",
         bg="Two rows of cottages, every window glowing, warm halos.",
         prompt="Whole snowy village lit up at night, every cottage window glowing warm gold, wreaths on doors, small silhouettes holding candles in windows; a red fox, little hedgehog and robin watching happily from the street."),
    dict(n=23, scene="s23", text_pos="bottom", text_color="dark",
         text="Up on the hill, Glimmer began to shine. Brighter... brighter... BRIGHTER!\n\nThen, slowly, gently, she began to float, up past Oakley's branch, up past the tallest pine, up, up, up into the night, with the red scarf trailing behind her like a ribbon.",
         desc="Glimmer soars up into the sky, blazing with light, the red striped scarf streaming below like a comet tail, sparkles everywhere. Oakley watches from his branch.",
         chars="Glimmer upper centre; Oakley small on branch left.",
         bg="Starry sky, pine row on the hill, snow (text area).",
         prompt="A little golden star blazing with light rising high into a starry night sky, a red striped scarf trailing below it like a comet tail, sparkles all around; small owl watching from a branch; snowy hill with pines; snowy foreground clear for text."),
    dict(n=24, scene="s24", text_pos="top", text_color="light",
         text="The village clock began to chime. Bong... bong... bong...\n\nTwelve!\n\nJuniper held her breath. And across the big round moon flew a sleigh pulled by reindeer, following one bright little star straight to Hollyberry Village.\n\nAll across the village, everyone cheered.",
         desc="A huge glowing moon with the silhouette of a sleigh and four reindeer crossing it. Glimmer shines bright to the right. The clock tower and lit village sit below.",
         chars="Sleigh silhouette across moon; Glimmer right.",
         bg="Night sky, giant moon centre, clock tower left, lit village along the bottom.",
         prompt="Giant glowing full moon with the dark silhouette of a sleigh pulled by four reindeer flying across it; a bright little star shining nearby; a village clock tower and cottages with glowing windows below."),
    dict(n=25, scene="s25", text_pos="top", text_color="light",
         text="Snow. Sparkle. Windows like little suns. One special star.\n\n“So this is Christmas,” Juniper whispered, smiling so wide that her cheeks glowed.\n\nEmber curled his warm tail around her. Ruby snuggled close. And they watched until her eyes grew heavy once more.",
         desc="Juniper, sleepy and content, is wrapped in Ember's bushy tail on the hill. Ruby snuggles close. The glowing village and Glimmer, with a faint sleigh, fill the sky behind them.",
         chars="Ember left lying with eyes closed; Juniper centre-right wrapped in his tail; Ruby beside her.",
         bg="Starry sky, Glimmer and faint sleigh, glowing village, snow.",
         prompt="Sleepy little hedgehog wrapped snugly in a red fox's bushy tail on a snowy hill, a robin snuggled close, overlooking a village with glowing windows; a bright star and faint distant sleigh in the night sky."),
    dict(n=26, scene="s26", text_pos="top", text_color="light",
         text="In the morning, Juniper woke in her own snug bed. Had it all been a dream?\n\nThen she saw it: her red scarf, folded by her pillow and dusted with stardust. Tucked inside was a tiny note:\n\nThank you for lighting my way home. Look up! — G.\n\nGrandma smiled a knowing smile.",
         desc="Morning in the burrow. Juniper sits up delighted, holding her folded scarf sparkling with stardust and a tiny note with a star. Grandma smiles with closed eyes. Daylight through the round window.",
         chars="Juniper centre with scarf and note; Grandma right.",
         bg="Burrow interior, daytime window left, lantern right.",
         prompt="Morning inside a cozy burrow: little hedgehog sitting up in a leaf bed holding her folded red striped scarf sparkling with stardust and a tiny note marked with a gold star; Grandma Hedgehog smiling knowingly; daylight through a round window."),
    dict(n=27, scene="s27", text_pos="bottom", text_color="dark",
         text="That night, Juniper peeked out of her burrow one last time.\n\nHigh above Hollyberry Village, one little star twinkled... and winked.\n\nJuniper waved with her whole paw. “Goodnight, little light.”",
         desc="Juniper stands at her glowing burrow door waving up at the sky, where Glimmer winks among the stars.",
         chars="Juniper beside the door, waving; Glimmer upper right, winking.",
         bg="Starry sky, holly tree with open glowing door, snow (text area).",
         prompt="Little hedgehog in red striped scarf standing by her glowing open burrow door under a snowy holly tree, waving up at a small golden star winking in the starry sky; snowy foreground clear for text."),
    dict(n=28, scene="s28", text_pos="top", text_color="light",
         text="Then she snuggled into her scarf beside Grandma, curled into a cozy, prickly ball, and fell fast asleep until spring.\n\nAnd all winter long, Juniper dreamed of Christmas, the very first one she ever saw.",
         desc="Cross-section: above ground, snowy pines under a starry sky with Glimmer; below ground, Juniper and Grandma sleep curled on leaves, Juniper's scarf tucked around her.",
         chars="Grandma (ball) left, Juniper (ball with scarf) right, underground; Glimmer in sky upper right.",
         bg="Split view: night sky and snow line above, warm burrow below.",
         prompt="Cross-section view: snowy pines under a starry sky with one little star shining above; below ground a warm burrow where two hedgehogs sleep curled into balls on autumn leaves, the smaller one tucked into a red striped scarf."),
    dict(n=29, scene="s29", text_pos="top", text_color="light", text="", end=True,
         desc="Final wide scene: Glimmer shines brightest above a peaceful, glowing Hollyberry Village, the holly tree with Juniper's warm round door in the corner, gentle snowfall. 'The End' is set in the sky.",
         chars="Glimmer top centre; holly-tree burrow lower right.",
         bg="Starry sky, lit village, snow.",
         prompt="Peaceful wide view of a snowy village with glowing windows under a starry sky, one bright smiling star shining above it, a holly tree with a small glowing round door at lower right, gentle snowfall."),

    dict(n=30, kind="front", scene="bm_talk", label="Let's Talk About the Story"),
    dict(n=31, kind="front", scene="bm_author", label="About the Author"),
    dict(n=32, kind="front", scene="bm_goodnight", label="Goodnight page"),
]

TALK_QUESTIONS = [
    "Juniper had never seen Christmas. What would you show her first?",
    "Why do you think Juniper gave Glimmer her brand-new scarf?",
    "Ruby, Ember and Oakley each helped in a different way. How do you help your friends?",
    "How did the whole village help Glimmer get home?",
    "What makes you feel warm and glowing inside?",
]

DEDICATION = "For everyone who has ever waited\na long, long time\nfor something wonderful."

AUTHOR_BIO = (f"{AUTHOR_NAME} writes cozy, read-aloud picture books for little ones and the grown-ups who tuck them in. "
              "She believes the best stories end with a warm feeling and a sleepy smile, and that even the smallest kindness can light up the darkest night. "
              "Juniper and the Little Lost Star is her first Christmas story.")


def word_count():
    import re
    return sum(len(re.findall(r"[A-Za-z']+", p.get("text", ""))) for p in PAGES)


if __name__ == "__main__":
    print("story words:", word_count())
