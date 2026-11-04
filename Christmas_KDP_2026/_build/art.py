"""
Vector art library for "Juniper and the Little Lost Star".

Every character is drawn by ONE function, so proportions, colours and
clothing are identical on every page (this is how character consistency
is enforced). All coordinates are SVG user units; a page canvas is
2588 x 2625 units = 8.625 x 8.75 in at 300 DPI (KDP bleed page size for an
8.5 x 8.5 in trim).
"""
import math
import random

# ---------------------------------------------------------------- palette
P = {
    # Juniper (hedgehog)
    "spike": "#6B4430", "spike_tip": "#B07F57", "spike_dark": "#4A2E20",
    "face": "#F6DFBC", "face_shade": "#E9C99C", "ear_in": "#F2A79F",
    "cheek": "#F2948A", "ink": "#2B1B14", "foot": "#9A6646",
    "scarf": "#C8303A", "scarf_dark": "#9E1F2A", "stripe": "#FFF7EE",
    # Grandma
    "g_spike": "#8E8079", "g_tip": "#CBBFB3", "shawl": "#8E7CC3", "shawl_dark": "#6E5DA3",
    # Glimmer (star)
    "star_hi": "#FFF4B8", "star": "#FFD54A", "star_lo": "#F5A623",
    # Ruby (robin)
    "robin": "#7A5236", "robin_dark": "#5A3A24", "breast": "#E8582F", "beak": "#E9B44C",
    # Ember (fox)
    "fox": "#DB6A2A", "fox_lt": "#F29A55", "fox_white": "#FFF6EC", "fox_dark": "#3B2418",
    # Oakley (owl)
    "owl": "#8A8EA3", "owl_dark": "#666A80", "owl_belly": "#CDD0DD", "owl_face": "#EEE7D7", "owl_eye": "#F4B42F",
    # world
    "night_top": "#0A1736", "night_mid": "#1C3566", "night_low": "#3F5F95",
    "snow": "#F4F8FF", "snow_shade": "#C9D8EE", "snow_deep": "#9DB4D6",
    "pine": "#1F4D3A", "pine_dark": "#163829", "pine_lt": "#2E6B4F",
    "bark": "#5A3B28", "window": "#FFD27A", "window_hot": "#FFF1C2",
    "holly": "#24603F", "berry": "#D3283A", "wall": "#E7D2B3", "roof": "#7B3B33",
}


def ring_points(cx, cy, rx, ry, a0, a1, n, jitter=0.0, seed=1):
    rnd = random.Random(seed)
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        r = 1 + rnd.uniform(-jitter, jitter)
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    return pts


def spiky_path(cx, cy, rx, ry, a0, a1, n, spike=1.22, seed=3):
    """Closed path of soft spikes along an elliptical arc, back to centre."""
    rnd = random.Random(seed)
    d = []
    for i in range(n * 2 + 1):
        a = math.radians(a0 + (a1 - a0) * i / (n * 2))
        k = spike + rnd.uniform(-0.04, 0.05) if i % 2 else 1.0
        x, y = cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)
        d.append(("M" if i == 0 else "L") + f"{x:.1f},{y:.1f}")
    d.append(f"L{cx:.1f},{cy:.1f}Z")
    return " ".join(d)


def star_path(cx, cy, R, r, rot=-90, n=5):
    pts = []
    for i in range(n * 2):
        a = math.radians(rot + i * 180 / n)
        rr = R if i % 2 == 0 else r
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return "M" + " L".join(pts) + "Z"


# ------------------------------------------------------------------ defs
def defs():
    return f"""
<defs>
 <radialGradient id="glow" r="0.5"><stop offset="0" stop-color="#FFF6C8" stop-opacity="0.95"/>
   <stop offset="0.35" stop-color="#FFD966" stop-opacity="0.45"/><stop offset="1" stop-color="#FFC94A" stop-opacity="0"/></radialGradient>
 <radialGradient id="warmglow" r="0.5"><stop offset="0" stop-color="#FFE7A8" stop-opacity="0.9"/>
   <stop offset="0.4" stop-color="#FFB85C" stop-opacity="0.35"/><stop offset="1" stop-color="#FF9A3C" stop-opacity="0"/></radialGradient>
 <radialGradient id="starfill" cx="0.45" cy="0.35" r="0.7"><stop offset="0" stop-color="{P['star_hi']}"/>
   <stop offset="0.55" stop-color="{P['star']}"/><stop offset="1" stop-color="{P['star_lo']}"/></radialGradient>
 <radialGradient id="paleStar" cx="0.45" cy="0.35" r="0.7"><stop offset="0" stop-color="#FFF9E0"/>
   <stop offset="0.6" stop-color="#F3E3A6"/><stop offset="1" stop-color="#D9C27E"/></radialGradient>
 <radialGradient id="moon" cx="0.4" cy="0.4" r="0.6"><stop offset="0" stop-color="#FFFDF2"/><stop offset="1" stop-color="#F3E6B8"/></radialGradient>
 <linearGradient id="spikeG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P['spike_tip']}"/><stop offset="0.5" stop-color="{P['spike']}"/><stop offset="1" stop-color="{P['spike_dark']}"/></linearGradient>
 <linearGradient id="gspikeG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P['g_tip']}"/><stop offset="1" stop-color="{P['g_spike']}"/></linearGradient>
 <linearGradient id="faceG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FBEBD0"/><stop offset="1" stop-color="{P['face_shade']}"/></linearGradient>
 <linearGradient id="snowG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="{P['snow_shade']}"/></linearGradient>
 <linearGradient id="snowNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#DCE7F8"/><stop offset="1" stop-color="#8FA7CF"/></linearGradient>
 <linearGradient id="foxG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P['fox_lt']}"/><stop offset="1" stop-color="{P['fox']}"/></linearGradient>
 <linearGradient id="burrowG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7A4E30"/><stop offset="1" stop-color="#4E301E"/></linearGradient>
 <filter id="blur8"><feGaussianBlur stdDeviation="8"/></filter>
 <filter id="blur20"><feGaussianBlur stdDeviation="20"/></filter>
 <filter id="blur50"><feGaussianBlur stdDeviation="50"/></filter>
 <filter id="soft"><feGaussianBlur stdDeviation="2.5"/></filter>
 <filter id="grain" x="0" y="0" width="100%" height="100%">
   <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" result="n"/>
   <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.5  0 0 0 0 0.45  0 0 0 0 0.4  0 0 0 0.10 0"/>
 </filter>
 <filter id="paper" x="0" y="0" width="100%" height="100%">
   <feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="3" seed="3" result="n"/>
   <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 0.95  0 0 0 0 0.85  0 0 0 0.10 0"/>
 </filter>
</defs>"""


def grain(W, H):
    return (f'<rect width="{W}" height="{H}" filter="url(#paper)" style="mix-blend-mode:soft-light"/>'
            f'<rect width="{W}" height="{H}" filter="url(#grain)" opacity="0.55"/>')


def g(x, y, s=1.0, flip=False, body="", rot=0):
    sx = -s if flip else s
    return f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot}) scale({sx},{s})">{body}</g>'


# ------------------------------------------------------------- JUNIPER
def hedgehog(look=0, arms="down", eyes="open", mouth="smile", scarf=True,
             grandma=False, blush=True, ear_wiggle=0):
    """Front-facing storybook hedgehog. Origin = between the feet, ~640 tall.
    look: -1..1 shifts face features (gaze).  arms: down|up|hold|wave|hug.
    eyes: open|closed|wide|sleepy.  mouth: smile|o|grin|small."""
    dx = 22 * look
    sp_fill = "url(#gspikeG)" if grandma else "url(#spikeG)"
    sp_dark = "#6F625B" if grandma else P["spike_dark"]
    o = []
    # spike halo (two layers for depth)
    o.append(f'<path d="{spiky_path(0,-330,250,270,150,390,17,1.24,seed=11)}" fill="{sp_dark}"/>')
    o.append(f'<path d="{spiky_path(0,-335,232,252,158,382,15,1.2,seed=5)}" fill="{sp_fill}"/>')
    # signature top tuft (3 lighter spikes)
    tuft = P["g_tip"] if grandma else P["spike_tip"]
    o.append(f'<path d="M-50,-560 L-30,-650 L-8,-575 L12,-675 L30,-578 L58,-640 L62,-560Z" fill="{tuft}" stroke="{sp_dark}" stroke-width="6" stroke-linejoin="round"/>')
    # feet
    for fx in (-85, 85):
        o.append(f'<ellipse cx="{fx}" cy="-22" rx="66" ry="30" fill="{P["foot"]}"/>')
    # body / belly
    o.append(f'<path d="M-195,-330 C-215,-150 -150,-20 0,-20 C150,-20 215,-150 195,-330 Z" fill="url(#faceG)"/>')
    # face
    o.append(f'<ellipse cx="0" cy="-345" rx="182" ry="160" fill="url(#faceG)"/>')
    # ears
    for ex in (-1, 1):
        ox = ex * (150 + ear_wiggle)
        o.append(f'<circle cx="{ox}" cy="-462" r="48" fill="{P["face_shade"]}"/><circle cx="{ox}" cy="-460" r="27" fill="{P["ear_in"]}"/>')
    # cheeks
    if blush:
        for cx_ in (-112, 112):
            o.append(f'<ellipse cx="{cx_+dx}" cy="-300" rx="34" ry="20" fill="{P["cheek"]}" opacity="0.6"/>')
    # eyes
    for ex in (-68, 68):
        x = ex + dx
        if eyes == "closed":
            o.append(f'<path d="M{x-28},-352 Q{x},-322 {x+28},-352" fill="none" stroke="{P["ink"]}" stroke-width="10" stroke-linecap="round"/>')
        elif eyes == "sleepy":
            o.append(f'<path d="M{x-28},-345 Q{x},-330 {x+28},-345" fill="none" stroke="{P["ink"]}" stroke-width="10" stroke-linecap="round"/>')
        else:
            ry = 42 if eyes == "wide" else 35
            o.append(f'<ellipse cx="{x}" cy="-352" rx="27" ry="{ry}" fill="{P["ink"]}"/>'
                     f'<circle cx="{x+9}" cy="-366" r="10" fill="#fff"/><circle cx="{x-9}" cy="-338" r="4.5" fill="#fff" opacity="0.8"/>')
    if grandma:  # round spectacles
        for ex in (-68, 68):
            o.append(f'<circle cx="{ex+dx}" cy="-352" r="50" fill="#ffffff" fill-opacity="0.12" stroke="#7C5A3A" stroke-width="8"/>')
        o.append(f'<path d="M{-18+dx},-356 Q{dx},-368 {18+dx},-356" stroke="#7C5A3A" stroke-width="8" fill="none"/>')
    # snout + nose
    o.append(f'<ellipse cx="{dx}" cy="-282" rx="62" ry="44" fill="#FFF3DF"/>')
    o.append(f'<ellipse cx="{dx}" cy="-300" rx="27" ry="21" fill="{P["ink"]}"/><ellipse cx="{dx+8}" cy="-307" rx="9" ry="6" fill="#fff" opacity="0.7"/>')
    # mouth
    if mouth == "smile":
        o.append(f'<path d="M{dx-26},-268 Q{dx},-246 {dx+26},-268" fill="none" stroke="{P["ink"]}" stroke-width="7" stroke-linecap="round"/>')
    elif mouth == "grin":
        o.append(f'<path d="M{dx-32},-270 Q{dx},-224 {dx+32},-270 Z" fill="#8E2B2B" stroke="{P["ink"]}" stroke-width="6" stroke-linejoin="round"/>')
    elif mouth == "o":
        o.append(f'<ellipse cx="{dx}" cy="-258" rx="14" ry="18" fill="#8E2B2B" stroke="{P["ink"]}" stroke-width="5"/>')
    elif mouth == "small":
        o.append(f'<path d="M{dx-14},-264 Q{dx},-256 {dx+14},-264" fill="none" stroke="{P["ink"]}" stroke-width="6" stroke-linecap="round"/>')
    elif mouth == "worried":
        o.append(f'<path d="M{dx-22},-256 Q{dx},-272 {dx+22},-256" fill="none" stroke="{P["ink"]}" stroke-width="7" stroke-linecap="round"/>')
    # scarf / shawl
    if scarf and not grandma:
        o.append(f'<path d="M-182,-236 Q0,-180 182,-236 L176,-188 Q0,-130 -176,-188 Z" fill="{P["scarf"]}"/>')
        o.append(f'<path d="M-180,-214 Q0,-160 180,-214" stroke="{P["scarf_dark"]}" stroke-width="6" fill="none" opacity="0.5"/>')
        # hanging tail with two white stripes + fringe
        o.append(f'<path d="M70,-196 L150,-200 L168,-60 L98,-52 Z" fill="{P["scarf"]}"/>'
                 f'<path d="M86,-130 L158,-136 L161,-112 L89,-106 Z" fill="{P["stripe"]}"/>'
                 f'<path d="M92,-94 L163,-100 L165,-78 L95,-72 Z" fill="{P["stripe"]}"/>')
        for i in range(6):
            fx = 102 + i * 12
            o.append(f'<path d="M{fx},-54 L{fx+2},-28" stroke="{P["scarf"]}" stroke-width="7" stroke-linecap="round"/>')
    if grandma:
        o.append(f'<path d="M-200,-250 Q0,-160 200,-250 L210,-150 Q0,-40 -210,-150 Z" fill="{P["shawl"]}"/>'
                 f'<path d="M-205,-200 Q0,-110 205,-200" stroke="{P["shawl_dark"]}" stroke-width="8" fill="none" stroke-dasharray="20 14"/>')
    # arms
    arm = P["face_shade"]
    def a(x, y, rot):
        return f'<ellipse cx="0" cy="0" rx="34" ry="66" fill="{arm}" stroke="{P["foot"]}" stroke-width="5" transform="translate({x},{y}) rotate({rot})"/>'
    if arms == "down":
        o += [a(-178, -170, 22), a(178, -170, -22)]
    elif arms == "up":
        o += [a(-210, -360, -35), a(210, -360, 35)]
    elif arms == "wave":
        o += [a(-178, -170, 22), a(235, -330, 45)]
    elif arms == "hold":
        o += [a(-95, -175, -40), a(95, -175, 40)]
    elif arms == "hug":
        o += [a(-70, -190, -70), a(70, -190, 70)]
    elif arms == "point":
        o += [a(-178, -170, 22), a(220, -300, 65)]
    return "".join(o)


def hedgehog_ball(eyes="closed", grandma=False, peek=True):
    """Curled sleeping ball, origin at bottom centre, ~430 wide."""
    sp_fill = "url(#gspikeG)" if grandma else "url(#spikeG)"
    sp_dark = "#6F625B" if grandma else P["spike_dark"]
    o = [f'<ellipse cx="0" cy="-8" rx="210" ry="22" fill="#000" opacity="0.15"/>',
         f'<path d="{spiky_path(0,-190,190,170,0,360,22,1.22,seed=8)}" fill="{sp_dark}"/>',
         f'<path d="{spiky_path(0,-195,176,158,0,360,20,1.18,seed=2)}" fill="{sp_fill}"/>']
    if peek:
        o.append(f'<ellipse cx="70" cy="-120" rx="105" ry="82" fill="url(#faceG)"/>')
        o.append(f'<circle cx="20" cy="-178" r="30" fill="{P["face_shade"]}"/><circle cx="20" cy="-178" r="16" fill="{P["ear_in"]}"/>')
        o.append(f'<path d="M58,-132 Q76,-114 94,-132" fill="none" stroke="{P["ink"]}" stroke-width="8" stroke-linecap="round"/>')
        o.append(f'<ellipse cx="150" cy="-100" rx="22" ry="17" fill="{P["ink"]}"/>')
        o.append(f'<ellipse cx="100" cy="-96" rx="22" ry="13" fill="{P["cheek"]}" opacity="0.6"/>')
    return "".join(o)


# ------------------------------------------------------------- GLIMMER
def glimmer(mood="happy", glow=1.0, pale=False, scarf=False, wink=False):
    """The little star. Origin at centre, ~240 across (plus glow)."""
    o = []
    if glow > 0:
        o.append(f'<circle r="{260*glow:.0f}" fill="url(#glow)" opacity="{min(1,0.35+0.65*glow):.2f}"/>')
    fill = "url(#paleStar)" if pale else "url(#starfill)"
    edge = "#E3C77A" if pale else P["star_lo"]
    sp = star_path(0, 0, 112, 56)
    o.append(f'<path d="{sp}" fill="{edge}" stroke="{edge}" stroke-width="34" stroke-linejoin="round"/>')
    o.append(f'<path d="{sp}" fill="{fill}" stroke="{fill}" stroke-width="22" stroke-linejoin="round"/>')
    o.append(f'<path d="M-30,-60 Q-8,-90 6,-104" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity="0.7" fill="none"/>')
    ink = P["ink"]
    # eyes
    if mood == "sad":
        o.append(f'<ellipse cx="-26" cy="6" rx="9" ry="11" fill="{ink}"/><ellipse cx="26" cy="6" rx="9" ry="11" fill="{ink}"/>')
        o.append(f'<path d="M-42,-6 L-16,-18 M42,-6 L16,-18" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>')
        o.append(f'<path d="M-14,40 Q0,30 14,40" stroke="{ink}" stroke-width="6" fill="none" stroke-linecap="round"/>')
        o.append(f'<path d="M30,22 q-8,16 0,22 q8,-6 0,-22Z" fill="#9FD3FF"/>')
    elif mood == "surprised":
        o.append(f'<ellipse cx="-26" cy="4" rx="10" ry="14" fill="{ink}"/><ellipse cx="26" cy="4" rx="10" ry="14" fill="{ink}"/>')
        o.append(f'<ellipse cx="0" cy="38" rx="9" ry="11" fill="#8E2B2B"/>')
    else:
        if wink:
            o.append(f'<path d="M-36,6 Q-26,-6 -16,6" stroke="{ink}" stroke-width="7" fill="none" stroke-linecap="round"/>')
        else:
            o.append(f'<ellipse cx="-26" cy="4" rx="9" ry="12" fill="{ink}"/><circle cx="-23" cy="0" r="3.5" fill="#fff"/>')
        o.append(f'<ellipse cx="26" cy="4" rx="9" ry="12" fill="{ink}"/><circle cx="29" cy="0" r="3.5" fill="#fff"/>')
        o.append(f'<path d="M-16,30 Q0,46 16,30" stroke="{ink}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    o.append(f'<ellipse cx="-46" cy="26" rx="13" ry="8" fill="{P["cheek"]}" opacity="0.6"/><ellipse cx="46" cy="26" rx="13" ry="8" fill="{P["cheek"]}" opacity="0.6"/>')
    if scarf:
        o.append(f'<path d="M-70,56 Q0,86 70,56 L64,84 Q0,112 -64,84 Z" fill="{P["scarf"]}"/>'
                 f'<path d="M30,82 L58,84 L70,150 L44,152 Z" fill="{P["scarf"]}"/>'
                 f'<path d="M38,112 L64,114 L66,124 L40,122 Z M41,132 L67,134 L68,142 L42,140Z" fill="{P["stripe"]}"/>')
    return "".join(o)


def scarf_ribbon(x0, y0, x1, y1, bend=120, width=46):
    """The red scarf trailing like a ribbon (used when Glimmer rises)."""
    mx, my = (x0 + x1) / 2 + bend, (y0 + y1) / 2
    return (f'<path d="M{x0},{y0} Q{mx},{my} {x1},{y1}" stroke="{P["scarf"]}" stroke-width="{width}" fill="none" stroke-linecap="round"/>'
            f'<path d="M{x0},{y0} Q{mx},{my} {x1},{y1}" stroke="{P["stripe"]}" stroke-width="{width}" fill="none" stroke-dasharray="14 120" stroke-dashoffset="-60"/>')


# --------------------------------------------------------------- RUBY
def robin(pose="stand", look=1):
    """Ruby the robin, facing right. Origin at feet. ~200 tall."""
    o = []
    if pose == "stand":
        o.append(f'<path d="M-5,0 L-12,-40 M15,0 L12,-40" stroke="#6B4A2A" stroke-width="7" stroke-linecap="round"/>')
    o.append(f'<path d="M-70,-90 L-150,-60 L-140,-110 Z" fill="{P["robin_dark"]}"/>')  # tail
    o.append(f'<ellipse cx="0" cy="-105" rx="88" ry="78" fill="{P["robin"]}"/>')
    o.append(f'<ellipse cx="34" cy="-92" rx="56" ry="58" fill="{P["breast"]}"/>')
    o.append(f'<circle cx="38" cy="-165" r="52" fill="{P["robin"]}"/>')
    o.append(f'<path d="M30,-140 Q60,-150 84,-128 Q60,-100 30,-112Z" fill="{P["breast"]}"/>')
    o.append(f'<circle cx="54" cy="-176" r="11" fill="{P["ink"]}"/><circle cx="57" cy="-180" r="4" fill="#fff"/>')
    o.append(f'<path d="M84,-170 L118,-160 L84,-152 Z" fill="{P["beak"]}"/>')
    if pose == "fly":
        o.append(f'<path d="M-30,-120 Q-60,-260 30,-250 Q0,-180 20,-120Z" fill="{P["robin_dark"]}"/>')
        o.append(f'<path d="M-20,-115 Q-130,-230 -110,-140 Z" fill="{P["robin_dark"]}" opacity="0.85"/>')
    else:
        o.append(f'<path d="M-50,-120 Q-10,-150 30,-110 Q-10,-70 -60,-80Z" fill="{P["robin_dark"]}"/>')
    o.append(f'<ellipse cx="66" cy="-150" rx="12" ry="7" fill="{P["cheek"]}" opacity="0.5"/>')
    return "".join(o)


# --------------------------------------------------------------- EMBER
def fox(pose="stand", eyes="open", tail=True):
    """Ember the fox, side view facing right. Origin at feet. ~620 tall."""
    o = []
    # tail
    if tail:
        o.append(f'<path d="M-200,-260 C-380,-260 -460,-420 -400,-560 C-330,-470 -260,-380 -170,-330 Z" fill="url(#foxG)"/>')
    if tail:
        o.append(f'<path d="M-400,-560 C-430,-500 -420,-470 -380,-450 C-370,-500 -390,-530 -400,-560Z" fill="{P["fox_white"]}"/>')
    legs = [(-150, 0), (-95, 0), (95, 0), (150, 0)]
    if pose == "run":
        legs = [(-200, -40), (-110, 10), (110, -10), (200, -50)]
    for i, (lx, ly) in enumerate(legs):
        o.append(f'<rect x="{lx-24}" y="{-200+ly}" width="48" height="{200}" rx="24" fill="{P["fox"] if i%2 else P["fox_lt"]}"/>'
                 f'<rect x="{lx-24}" y="{-80+ly}" width="48" height="{80}" rx="24" fill="{P["fox_dark"]}"/>')
    o.append(f'<ellipse cx="0" cy="-270" rx="240" ry="130" fill="url(#foxG)"/>')
    o.append(f'<ellipse cx="170" cy="-260" rx="85" ry="105" fill="{P["fox_white"]}"/>')
    # head
    o.append(f'<path d="M190,-330 L180,-540 L250,-460 Z" fill="{P["fox"]}"/><path d="M190,-470 L184,-540 L222,-494Z" fill="{P["fox_dark"]}"/>')
    o.append(f'<circle cx="250" cy="-410" r="115" fill="url(#foxG)"/>')
    o.append(f'<path d="M260,-500 L310,-600 L340,-470 Z" fill="{P["fox"]}"/><path d="M292,-540 L310,-600 L322,-540Z" fill="{P["fox_dark"]}"/><path d="M278,-500 L306,-560 L322,-490Z" fill="#F6C9A6"/>')
    o.append(f'<path d="M300,-450 Q420,-430 450,-392 Q420,-350 300,-340 Z" fill="url(#foxG)"/>')
    o.append(f'<path d="M210,-380 Q300,-300 450,-388 Q380,-320 300,-320 Q230,-320 200,-350Z" fill="{P["fox_white"]}"/>')
    o.append(f'<ellipse cx="450" cy="-394" rx="22" ry="17" fill="{P["ink"]}"/>')
    if eyes == "closed":
        o.append(f'<path d="M282,-440 Q300,-424 318,-440" stroke="{P["ink"]}" stroke-width="9" fill="none" stroke-linecap="round"/>')
    else:
        o.append(f'<ellipse cx="300" cy="-438" rx="15" ry="20" fill="{P["ink"]}"/><circle cx="305" cy="-445" r="6" fill="#fff"/>')
    o.append(f'<path d="M360,-360 Q384,-348 404,-362" stroke="{P["ink"]}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    o.append(f'<ellipse cx="300" cy="-385" rx="20" ry="12" fill="{P["cheek"]}" opacity="0.45"/>')
    return "".join(o)


def fox_tail_curl():
    """Ember's tail curled as a blanket (used on the 'This is Christmas' page)."""
    return (f'<path d="M-330,-40 C-360,-260 -100,-330 120,-260 C260,-210 300,-80 220,-30 C120,-120 -140,-140 -330,-40Z" fill="url(#foxG)"/>'
            f'<path d="M220,-30 C280,-90 270,-170 230,-200 C240,-130 220,-80 180,-50Z" fill="{P["fox_white"]}"/>')


# --------------------------------------------------------------- OAKLEY
def owl(eyes="open"):
    """Old Oakley, front view. Origin at feet. ~560 tall."""
    o = []
    o.append(f'<path d="M-130,-470 L-170,-570 L-70,-500 Z M130,-470 L170,-570 L70,-500 Z" fill="{P["owl_dark"]}"/>')
    o.append(f'<ellipse cx="0" cy="-260" rx="200" ry="255" fill="{P["owl"]}"/>')
    o.append(f'<ellipse cx="0" cy="-200" rx="135" ry="170" fill="{P["owl_belly"]}"/>')
    for row in range(4):
        for col in range(-2, 3):
            x, y = col * 52 + (26 if row % 2 else 0), -290 + row * 55
            if abs(x) < 110:
                o.append(f'<path d="M{x-14},{y} Q{x},{y+16} {x+14},{y}" stroke="{P["owl_dark"]}" stroke-width="6" fill="none" opacity="0.6"/>')
    o.append(f'<path d="M-195,-300 Q-260,-150 -150,-60 Q-160,-200 -120,-300Z" fill="{P["owl_dark"]}"/>'
             f'<path d="M195,-300 Q260,-150 150,-60 Q160,-200 120,-300Z" fill="{P["owl_dark"]}"/>')
    for ex in (-80, 80):
        o.append(f'<circle cx="{ex}" cy="-390" r="92" fill="{P["owl_face"]}"/>')
        if eyes == "closed":
            o.append(f'<path d="M{ex-40},-392 Q{ex},-360 {ex+40},-392" stroke="{P["ink"]}" stroke-width="10" fill="none" stroke-linecap="round"/>')
        else:
            o.append(f'<circle cx="{ex}" cy="-392" r="58" fill="{P["owl_eye"]}"/><circle cx="{ex}" cy="-392" r="30" fill="{P["ink"]}"/><circle cx="{ex+12}" cy="-405" r="10" fill="#fff"/>')
    o.append(f'<path d="M-130,-470 Q-80,-500 -30,-462 M130,-470 Q80,-500 30,-462" stroke="#ECE7DE" stroke-width="14" fill="none" stroke-linecap="round"/>')
    o.append(f'<path d="M-22,-350 L0,-300 L22,-350 Z" fill="#E7A23B"/>')
    for fx in (-60, 60):
        o.append(f'<path d="M{fx-26},0 L{fx-18},-26 M{fx},0 L{fx},-28 M{fx+26},0 L{fx+18},-26" stroke="#E7A23B" stroke-width="12" stroke-linecap="round"/>')
    return "".join(o)


# --------------------------------------------------------------- WORLD
def sky(W, H, top=None, mid=None, low=None):
    top, mid, low = top or P["night_top"], mid or P["night_mid"], low or P["night_low"]
    return (f'<defs><linearGradient id="skyG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
            f'<stop offset="0.55" stop-color="{mid}"/><stop offset="1" stop-color="{low}"/></linearGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#skyG)"/>')


def stars(W, H, n=120, seed=1, ymax=None, avoid=None):
    rnd = random.Random(seed)
    ymax = ymax or H * 0.6
    o = []
    for _ in range(n):
        x, y = rnd.uniform(0, W), rnd.uniform(0, ymax)
        if avoid and avoid[0] < x < avoid[2] and avoid[1] < y < avoid[3]:
            continue
        r = rnd.choice([2.5, 3, 4, 5, 6, 8])
        op = rnd.uniform(0.5, 1)
        if r >= 6:
            o.append(f'<path d="{star_path(x,y,r*2.6,r*0.7,n=4,rot=0)}" fill="#FFF8DC" opacity="{op:.2f}"/>')
        else:
            o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#FFF8E6" opacity="{op:.2f}"/>')
    return "".join(o)


def moon(x, y, r):
    return (f'<circle cx="{x}" cy="{y}" r="{r*2.2}" fill="url(#glow)" opacity="0.45"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#moon)"/>'
            f'<circle cx="{x-r*0.3}" cy="{y+r*0.2}" r="{r*0.14}" fill="#E8D9A6" opacity="0.5"/>'
            f'<circle cx="{x+r*0.35}" cy="{y-r*0.25}" r="{r*0.09}" fill="#E8D9A6" opacity="0.5"/>')


def snowflakes(W, H, n=90, seed=4, ymin=0, ymax=None, size=1.0):
    rnd = random.Random(seed)
    ymax = ymax or H
    o = []
    for _ in range(n):
        x, y, r = rnd.uniform(0, W), rnd.uniform(ymin, ymax), rnd.uniform(4, 11) * size
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff" opacity="{rnd.uniform(.55,.95):.2f}"/>')
    return "".join(o)


def hill(W, y, amp, color, seed=1, H=2625, waves=3):
    rnd = random.Random(seed)
    ph = rnd.uniform(0, 6)
    pts = [f"M0,{H}", f"L0,{y}"]
    for i in range(0, 41):
        x = W * i / 40
        yy = y - amp * math.sin(ph + waves * math.pi * i / 40) * (0.6 + 0.4 * math.sin(i / 7 + ph))
        pts.append(f"L{x:.0f},{yy:.0f}")
    pts.append(f"L{W},{H}Z")
    return f'<path d="{" ".join(pts)}" fill="{color}"/>'


def fir(x, y, h, color=None, snow=True, tiers=4, dark=None):
    color = color or P["pine"]
    dark = dark or P["pine_dark"]
    w = h * 0.55
    o = [f'<rect x="{x-h*0.04:.0f}" y="{y-h*0.12:.0f}" width="{h*0.08:.0f}" height="{h*0.14:.0f}" fill="{P["bark"]}"/>']
    for t in range(tiers):
        f = t / tiers
        top = y - h + h * f * 0.85
        bot = y - h * 0.1 - (tiers - 1 - t) * h * 0.12
        ww = w * (0.35 + 0.65 * (t + 1) / tiers)
        o.append(f'<path d="M{x},{top:.0f} L{x+ww/2:.0f},{bot:.0f} Q{x},{bot+h*0.05:.0f} {x-ww/2:.0f},{bot:.0f} Z" fill="{color}"/>')
        o.append(f'<path d="M{x},{top:.0f} L{x+ww/2:.0f},{bot:.0f} Q{x+ww/4:.0f},{bot+h*0.03:.0f} {x},{bot+h*0.04:.0f} Z" fill="{dark}" opacity="0.6"/>')
        if snow:
            o.append(f'<path d="M{x-ww*0.32:.0f},{bot-h*0.02:.0f} Q{x},{bot+h*0.02:.0f} {x+ww*0.42:.0f},{bot-h*0.03:.0f} Q{x+ww*0.3:.0f},{bot-h*0.06:.0f} {x},{bot-h*0.05:.0f} Q{x-ww*0.2:.0f},{bot-h*0.06:.0f} {x-ww*0.32:.0f},{bot-h*0.02:.0f}Z" fill="#F2F7FF" opacity="0.92"/>')
    if snow:
        o.append(f'<path d="M{x-w*0.07:.0f},{y-h+h*0.1:.0f} L{x},{y-h:.0f} L{x+w*0.07:.0f},{y-h+h*0.1:.0f} Q{x},{y-h+h*0.13:.0f} {x-w*0.07:.0f},{y-h+h*0.1:.0f}Z" fill="#fff"/>')
    return "".join(o)


def forest_row(W, y, h, n, seed=1, color=None, snow=True, jitter=0.25):
    rnd = random.Random(seed)
    o = []
    for i in range(n):
        x = W * (i + rnd.uniform(0.1, 0.9)) / n
        hh = h * rnd.uniform(1 - jitter, 1 + jitter)
        o.append(fir(x, y + rnd.uniform(-10, 20), hh, color=color, snow=snow))
    return "".join(o)


def holly_sprig(x, y, s=1.0, rot=0):
    leaf = "M0,0 Q30,-22 60,-10 Q70,-34 100,-30 Q100,-6 120,6 Q90,22 60,14 Q40,30 10,20 Q16,8 0,0Z"
    body = (f'<path d="{leaf}" fill="{P["holly"]}" transform="rotate(-25)"/>'
            f'<path d="{leaf}" fill="#2F7A50" transform="scale(-1,1) rotate(-25)"/>'
            f'<circle cx="-10" cy="10" r="18" fill="{P["berry"]}"/><circle cx="14" cy="14" r="18" fill="{P["berry"]}"/><circle cx="2" cy="-8" r="18" fill="#E23A4A"/>'
            f'<circle cx="-4" cy="-14" r="5" fill="#fff" opacity="0.7"/>')
    return g(x, y, s, body=body, rot=rot)


def holly_tree_burrow(x, y, s=1.0, door_glow=False, door_open=False):
    """The old holly tree with Juniper's round burrow door between the roots.
    Origin at ground centre. ~1500 tall at s=1."""
    o = []
    o.append(f'<path d="M-260,0 C-200,-60 -120,-150 -110,-520 L110,-520 C120,-150 200,-60 300,0Z" fill="{P["bark"]}"/>')
    o.append(f'<path d="M-60,-520 C-50,-300 -40,-150 -90,0 M50,-500 C70,-300 60,-160 120,0" stroke="#463021" stroke-width="12" fill="none" opacity="0.6"/>')
    rnd = random.Random(5)
    for cx, cy, r in [(0, -900, 420), (-280, -720, 280), (300, -740, 290), (-150, -1150, 260), (180, -1140, 260), (0, -1320, 200)]:
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{P["holly"]}"/>')
        o.append(f'<circle cx="{cx+r*0.25}" cy="{cy+r*0.25}" r="{r*0.8}" fill="#1B4A31" opacity="0.5"/>')
    for _ in range(46):
        bx, by = rnd.uniform(-500, 520), rnd.uniform(-1450, -560)
        if (bx / 560) ** 2 + ((by + 980) / 520) ** 2 < 1:
            o.append(f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="16" fill="{P["berry"]}"/>')
    for cx, cy, rx in [(-200, -560, 220), (220, -570, 220), (0, -1480, 150), (-380, -760, 120), (380, -780, 120)]:
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{rx*0.22:.0f}" fill="#F4F8FF"/>')
    # door
    if door_glow:
        o.append(f'<circle cx="0" cy="-140" r="420" fill="url(#warmglow)"/>')
    o.append(f'<path d="M-120,0 L-120,-150 A120,120 0 0 1 120,-150 L120,0Z" fill="#3B2416"/>')
    if door_open:
        o.append(f'<path d="M-100,0 L-100,-150 A100,100 0 0 1 100,-150 L100,0Z" fill="{P["window"]}"/>')
        o.append(f'<path d="M100,0 L100,-150 A100,100 0 0 0 60,-226 L40,-10Z" fill="#8A5A36"/>')
    else:
        o.append(f'<path d="M-100,0 L-100,-150 A100,100 0 0 1 100,-150 L100,0Z" fill="#9A6A42"/>')
        for lx in (-50, 0, 50):
            o.append(f'<path d="M{lx},-235 L{lx},0" stroke="#7B5232" stroke-width="10"/>')
        o.append(f'<circle cx="65" cy="-90" r="13" fill="#E6B54A"/>')
        if door_glow:
            o.append(f'<path d="M-100,-150 A100,100 0 0 1 100,-150" stroke="{P["window"]}" stroke-width="10" fill="none" opacity="0.9"/>'
                     f'<path d="M-25,-240 L-25,0 M25,-240 L25,0" stroke="{P["window_hot"]}" stroke-width="5" opacity="0.8"/>')
    o.append(f'<circle cx="-170" cy="-260" r="34" fill="#3B2416"/><circle cx="-170" cy="-260" r="26" fill="{P["window"] if door_glow else "#F3C66A"}"/>')
    return g(x, y, s, body="".join(o))


def house(x, y, w=420, h=320, lit=True, roof=None, seed=1, wreath=False, silhouette=None, chimney=True):
    """Cottage. Origin bottom-left at (x,y)."""
    roof = roof or P["roof"]
    o = []
    win = P["window"] if lit else "#2B3B5C"
    if lit:
        o.append(f'<circle cx="{x+w/2}" cy="{y-h*0.45}" r="{w*0.9}" fill="url(#warmglow)" opacity="0.55"/>')
    o.append(f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="{P["wall"]}"/>')
    o.append(f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="#000" opacity="0.12"/>')
    if chimney:
        o.append(f'<rect x="{x+w*0.68}" y="{y-h-h*0.75}" width="{w*0.12}" height="{h*0.5}" fill="#8A4B3E"/>'
                 f'<rect x="{x+w*0.66}" y="{y-h-h*0.78}" width="{w*0.16}" height="{h*0.07}" fill="#F4F8FF"/>')
    o.append(f'<path d="M{x-w*0.1},{y-h} L{x+w/2},{y-h-h*0.65} L{x+w*1.1},{y-h} Z" fill="{roof}"/>')
    o.append(f'<path d="M{x-w*0.12},{y-h+4} L{x+w/2},{y-h-h*0.67} L{x+w*1.12},{y-h+4} L{x+w*1.04},{y-h-14} L{x+w/2},{y-h-h*0.58} L{x-w*0.04},{y-h-14}Z" fill="#F4F8FF"/>')
    ww, wh = w * 0.26, h * 0.34
    for i, wx in enumerate((x + w * 0.12, x + w * 0.62)):
        wy = y - h * 0.78
        o.append(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="8" fill="{win}" stroke="#5A3B28" stroke-width="10"/>')
        if lit:
            o.append(f'<rect x="{wx+ww*0.15}" y="{wy+wh*0.1}" width="{ww*0.3}" height="{wh*0.35}" fill="{P["window_hot"]}" opacity="0.7"/>')
        if silhouette and i == silhouette.get("win", 0):
            sx, sy = wx + ww / 2, wy + wh
            kind = silhouette.get("kind", "child")
            if kind == "child":
                o.append(f'<circle cx="{sx}" cy="{sy-wh*0.62}" r="{ww*0.16}" fill="#6A4430"/><path d="M{sx-ww*0.28},{sy} Q{sx},{sy-wh*0.62} {sx+ww*0.28},{sy}Z" fill="#6A4430"/>'
                         f'<rect x="{sx+ww*0.14}" y="{sy-wh*0.52}" width="{ww*0.07}" height="{wh*0.2}" fill="#FFF"/><circle cx="{sx+ww*0.175}" cy="{sy-wh*0.56}" r="{ww*0.07}" fill="#FFB347"/>')
        o.append(f'<path d="M{wx+ww/2},{wy} L{wx+ww/2},{wy+wh} M{wx},{wy+wh/2} L{wx+ww},{wy+wh/2}" stroke="#5A3B28" stroke-width="8"/>')
        o.append(f'<rect x="{wx-8}" y="{wy+wh-4}" width="{ww+16}" height="16" fill="#F4F8FF"/>')
    dx = x + w * 0.42
    o.append(f'<path d="M{dx},{y} L{dx},{y-h*0.42} A{w*0.08},{w*0.08} 0 0 1 {dx+w*0.16},{y-h*0.42} L{dx+w*0.16},{y}Z" fill="#6B2E2A"/>')
    if wreath:
        o.append(f'<circle cx="{dx+w*0.08}" cy="{y-h*0.33}" r="{w*0.045}" fill="none" stroke="{P["holly"]}" stroke-width="{w*0.025}"/>'
                 f'<circle cx="{dx+w*0.08}" cy="{y-h*0.29}" r="{w*0.012}" fill="{P["berry"]}"/>')
    return "".join(o)


def village(W, y, scale=1.0, lit=1.0, seed=3, silhouettes=False):
    """Row of cottages along y. lit = fraction of houses lit."""
    rnd = random.Random(seed)
    o = []
    x = -80 * scale
    i = 0
    roofs = ["#7B3B33", "#3E5A7A", "#5E7A4A", "#8A5A3A", "#6B3F63"]
    while x < W:
        w = rnd.uniform(330, 440) * scale
        h = rnd.uniform(250, 330) * scale
        is_lit = rnd.random() < lit
        sil = {"win": rnd.choice([0, 1]), "kind": "child"} if (silhouettes and is_lit and i % 3 == 1) else None
        o.append(house(x, y + rnd.uniform(-10, 10) * scale, w, h, lit=is_lit, roof=rnd.choice(roofs), wreath=is_lit, silhouette=sil))
        x += w + rnd.uniform(70, 160) * scale
        i += 1
    return "".join(o)


def sleigh(x, y, s=1.0, color="#1A2440"):
    """Silhouette of a sleigh pulled by reindeer, flying left-to-right."""
    o = []
    for i in range(4):
        rx = 260 + i * 170
        ry = -40 - i * 26
        o.append(f'<g transform="translate({rx},{ry})">'
                 f'<ellipse cx="0" cy="0" rx="62" ry="26" fill="{color}"/>'
                 f'<path d="M-40,10 L-70,46 M-26,14 L-36,52 M30,12 L48,50 M42,8 L74,40" stroke="{color}" stroke-width="10" stroke-linecap="round"/>'
                 f'<path d="M48,-10 L74,-46 L96,-40 L92,-26 L66,-6Z" fill="{color}"/>'
                 f'<path d="M78,-44 L70,-82 M70,-70 L54,-84 M84,-46 L96,-84 M92,-70 L108,-80" stroke="{color}" stroke-width="6" stroke-linecap="round"/>'
                 f'</g>')
    o.append(f'<path d="M80,-40 L800,-150" stroke="{color}" stroke-width="5"/>')
    o.append(f'<path d="M-140,-120 L120,-120 Q170,-120 160,-60 L130,-10 L-110,-10 Q-150,-10 -150,-60Z" fill="{color}"/>')
    o.append(f'<path d="M-170,20 L150,20 Q200,20 200,-20" stroke="{color}" stroke-width="12" fill="none" stroke-linecap="round"/>')
    o.append(f'<path d="M-120,-10 L-120,20 M100,-10 L100,20" stroke="{color}" stroke-width="10"/>')
    o.append(f'<circle cx="-40" cy="-170" r="46" fill="{color}"/><path d="M-100,-120 Q-40,-230 30,-120Z" fill="{color}"/>')
    o.append(f'<path d="M-60,-150 Q-100,-250 -20,-220 Z" fill="{color}"/><path d="M60,-120 L90,-190 L130,-120Z" fill="{color}"/>')
    return g(x, y, s, body="".join(o))


def clock_tower(x, y, s=1.0, lit=True):
    o = [f'<rect x="-90" y="-620" width="180" height="620" fill="#D9C3A2"/>',
         f'<rect x="-90" y="-620" width="180" height="620" fill="#000" opacity="0.15"/>',
         f'<path d="M-120,-620 L0,-820 L120,-620Z" fill="#3E5A7A"/>',
         f'<path d="M-124,-616 L0,-826 L124,-616 L110,-630 L0,-800 L-110,-630Z" fill="#F4F8FF"/>',
         f'<circle cx="0" cy="-500" r="70" fill="{P["window_hot"] if lit else "#EDE3CF"}" stroke="#5A3B28" stroke-width="10"/>',
         f'<path d="M0,-500 L0,-555 M0,-500 L0,-548" stroke="{P["ink"]}" stroke-width="10" stroke-linecap="round"/>']
    for a in range(12):
        ang = math.radians(a * 30)
        o.append(f'<circle cx="{58*math.sin(ang):.0f}" cy="{-500-58*math.cos(ang):.0f}" r="4" fill="{P["ink"]}"/>')
    o.append(f'<rect x="-40" y="-220" width="80" height="120" rx="40" fill="{P["window"] if lit else "#2B3B5C"}" stroke="#5A3B28" stroke-width="8"/>')
    return g(x, y, s, body="".join(o))


def branch(x0, y0, x1, y1, w=60, snow=True):
    o = [f'<path d="M{x0},{y0} Q{(x0+x1)/2},{(y0+y1)/2-30} {x1},{y1}" stroke="{P["bark"]}" stroke-width="{w}" stroke-linecap="round" fill="none"/>']
    if snow:
        o.append(f'<path d="M{x0},{y0-w*0.45} Q{(x0+x1)/2},{(y0+y1)/2-30-w*0.5} {x1},{y1-w*0.45}" stroke="#F4F8FF" stroke-width="{w*0.4}" stroke-linecap="round" fill="none"/>')
    return "".join(o)


def svg_doc(W, H, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'{defs()}{body}{grain(W, H)}</svg>')
