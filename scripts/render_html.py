#!/usr/bin/env python3
"""Renderiza images/htmls/*.html a images/pngs/*.png con Chrome headless (a 2x).

Uso:
    python3 render_html.py                       # todos los HTML de ./images/htmls
    python3 render_html.py --root images infraestructura-aws pantalla-06-tablero

El ancho de la captura sale de <meta name="render-width" content="1600"> (por defecto 1600).
El alto se calcula solo: se captura alto y se recorta debajo del último píxel con contenido,
dejando el mismo margen inferior (<meta name="render-pad" content="40">). Requiere
google-chrome-stable (o chromium) y Pillow.
"""
import argparse, glob, os, re, shutil, subprocess, tempfile
from PIL import Image, ImageChops

SCALE = 2


def chrome():
    for b in ("google-chrome-stable", "google-chrome", "chromium", "chromium-browser", "brave"):
        if shutil.which(b):
            return b
    raise SystemExit("No se encontró Chrome ni Chromium")


def meta(html, name, default):
    m = re.search(rf'<meta\s+name="{name}"\s+content="(\d+)"', html)
    return int(m.group(1)) if m else default


def shot(src, png, width, height):
    subprocess.run([chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--force-device-scale-factor={SCALE}", f"--window-size={width},{height}",
                    "--virtual-time-budget=5000", f"--screenshot={png}", "file://" + os.path.abspath(src)],
                   check=True, capture_output=True, timeout=120)


def render(src, out):
    html = open(src, encoding="utf-8").read()
    width, pad = meta(html, "render-width", 1600), meta(html, "render-pad", 40)
    height = 3000
    with tempfile.TemporaryDirectory() as tmp:
        raw = os.path.join(tmp, "raw.png")
        while True:
            shot(src, raw, width, height)
            im = Image.open(raw).convert("RGB")
            bg = Image.new("RGB", im.size, im.getpixel((2, 2)))
            box = ImageChops.difference(im, bg).point(lambda v: 255 if v > 12 else 0).getbbox()
            bottom = box[3] if box else im.height
            if bottom < im.height - pad * SCALE or height >= 12000:
                break
            height *= 2
        im.crop((0, 0, im.width, min(im.height, bottom + pad * SCALE))).save(out, optimize=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*", help="nombres sin extensión; vacío = todos")
    ap.add_argument("--root", default="images")
    a = ap.parse_args()
    src_dir, out_dir = os.path.join(a.root, "htmls"), os.path.join(a.root, "pngs")
    os.makedirs(out_dir, exist_ok=True)
    srcs = [os.path.join(src_dir, n + ".html") for n in a.names] or sorted(glob.glob(os.path.join(src_dir, "*.html")))
    for s in srcs:
        out = os.path.join(out_dir, os.path.splitext(os.path.basename(s))[0] + ".png")
        im = Image.open(render(s, out))
        print(f"{out}  {im.width}x{im.height}")


if __name__ == "__main__":
    main()
