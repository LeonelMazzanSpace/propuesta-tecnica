#!/usr/bin/env python3
"""Decodifica la exportación PDF de Drive y arma una hoja de miniaturas para revisar el layout.

Uso:
  contact_sheet.py <resultado_download_file_content.txt> <carpeta_salida> [--cols 8] [--dpi 30]

El primer argumento es el archivo donde la herramienta guardó la respuesta de
download_file_content con exportMimeType application/pdf ({"content": "<base64>"}).
Genera doc.pdf, una imagen por página y sheet.png. Requiere pdftoppm y Pillow.
"""
import argparse, base64, glob, json, os, subprocess
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("export")
ap.add_argument("outdir")
ap.add_argument("--cols", type=int, default=8)
ap.add_argument("--dpi", type=int, default=30)
a = ap.parse_args()

os.makedirs(a.outdir, exist_ok=True)
pdf = os.path.join(a.outdir, "doc.pdf")
open(pdf, "wb").write(base64.b64decode(json.load(open(a.export))["content"]))
subprocess.run(["pdftoppm", "-r", str(a.dpi), "-png", pdf, os.path.join(a.outdir, "p")], check=True)
ims = [Image.open(f) for f in sorted(glob.glob(os.path.join(a.outdir, "p-*.png")))]
w, h = ims[0].size
rows = (len(ims) + a.cols - 1) // a.cols
sheet = Image.new("RGB", (w * a.cols, h * rows), "#888")
for k, im in enumerate(ims):
    sheet.paste(im, ((k % a.cols) * w, (k // a.cols) * h))
out = os.path.join(a.outdir, "sheet.png")
sheet.save(out)
print(f"{len(ims)} páginas -> {out}")
