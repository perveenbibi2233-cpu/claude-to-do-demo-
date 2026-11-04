#!/usr/bin/env bash
# Rebuild everything: SVG sources -> 300-DPI PNG (Chromium) -> JPEG illustrations -> KDP PDFs -> docs -> preflight.
# Requires: python3 (pillow, reportlab, pypdf, pypdfium2, python-docx, numpy), node + playwright with Chromium, poppler (pdffonts).
set -euo pipefail
cd "$(dirname "$0")"
PNG_DIR="${PNG_DIR:-png}"
mkdir -p ~/.local/share/fonts && cp fonts/*.ttf ~/.local/share/fonts/ && (fc-cache -f >/dev/null 2>&1 || true)
python3 gen_svgs.py svg
python3 gen_docs.py
node render.js svg "$PNG_DIR"
python3 make_pdf.py "$PNG_DIR"
python3 export_panels.py "$PNG_DIR"
python3 preflight.py
