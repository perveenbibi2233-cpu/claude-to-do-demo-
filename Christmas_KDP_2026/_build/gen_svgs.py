"""Write every scene (and the full-wrap cover) as an SVG file - the editable vector source of each illustration."""
import os, sys
from art import svg_doc
from scenes import SCENES, W, H
import cover
out = sys.argv[1] if len(sys.argv) > 1 else "svg"
os.makedirs(out, exist_ok=True)
for name, fn in sorted(SCENES.items()):
    open(os.path.join(out, f"{name}.svg"), "w").write(svg_doc(W, H, fn()))
open(os.path.join(out, "cover.svg"), "w").write(cover.cover_svg())
print(len(SCENES) + 1, "SVGs written to", out)
