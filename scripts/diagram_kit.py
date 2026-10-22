#!/usr/bin/env python3
"""Kit para diagramas de flujo con el estilo de la propuesta (solo nombres de componentes).

Uso como librería desde un script propio:

    import sys; sys.path.insert(0, "<skill>/scripts")
    from diagram_kit import D
    d = D(1800, 420)                       # lienzo en px lógicos
    d.group(40, 40, 320, 340, "Entradas")  # grupo con título en mayúsculas
    d.box(70, 120, 260, 80, "API REST")    # kind: plain | accent | green | amber | red
    d.box(70, 220, 260, 110, ["Zona de", "aterrizaje"])   # varias líneas: lista de textos
    d.path([(330, 160), (420, 160)])       # flecha ortogonal (lista de puntos)
    d.path([(330, 160), (380, 160)], head=False)   # tramo sin punta, para buses
    d.label(375, 146, "Transformación")    # rótulo chico sobre una flecha
    d.save("diagrama-vision-general")      # images/htmls/<nombre>.html y images/pngs/<nombre>.png (requiere rsvg-convert)

save() imprime WARN si un texto no entra en su caja o grupo (medido con Noto Sans Bold).
Corregir todos los WARN antes de usar la imagen.

Legibilidad: la imagen se inserta a 468 pt de ancho, así que el tamaño efectivo de un texto
es px / ancho_del_lienzo * 468. Con el lienzo de 1800, los títulos de grupo (26 px) quedan en
~6,8 pt y las cajas (30 px) en ~7,8 pt. No achicar las fuentes para que algo entre: acortar el
texto, pasarlo a dos líneas o agrandar la caja.

Reglas que dieron buen resultado:
- Etiquetas cortas, sin descripciones ni subtítulos.
- Flechas ortogonales y buses compartidos en lugar de diagonales que se cruzan.
- Dejar 50 px libres debajo del título de cada grupo, para que el contenido no lo tape.
- Ancho 1800 y alto entre 420 y 900. Si una fila no entra a este tamaño de letra, partir el
  diagrama en dos filas (forma de U) antes que achicar.
- Revisar cada PNG antes de insertarlo y corregir cruces, textos que se salen de su caja y títulos tapados.
"""
import os, subprocess

P, INK, LINE, SOFT, ARROW = "#433273", "#273239", "#c4c2d4", "#f4f3f8", "#6b6880"
KINDS = {
    "plain": ("#fff", LINE, INK, 2),
    "accent": ("#fff", P, P, 3),
    "green": ("#e8f4ee", "#1f7a52", "#1f7a52", 2),
    "amber": ("#fbf2e0", "#8a5a00", "#8a5a00", 2),
    "red": ("#fbeceb", "#a8322d", "#a8322d", 2),
}
GROUP_PX, BOX_PX, LABEL_PX = 26, 30, 26
LINE_H = 36  # interlineado de las cajas de varias líneas

_FONT = "/usr/share/fonts/noto/NotoSans-Bold.ttf"
try:
    from PIL import ImageFont
    _FB = ImageFont.truetype(_FONT, BOX_PX)
    _FG = ImageFont.truetype(_FONT, GROUP_PX)
except Exception:  # sin PIL o sin la fuente: no se mide
    _FB = _FG = None


def _w_box(s):
    return _FB.getlength(s) if _FB else 0


def _w_group(s):
    return _FG.getlength(s) + 2 * len(s) if _FG else 0  # suma el letter-spacing


class D:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.warns = []
        self.o = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Noto Sans, Liberation Sans, sans-serif">',
            f'<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{ARROW}"/></marker></defs>',
            f'<rect width="{w}" height="{h}" fill="#fff"/>',
        ]

    def group(self, x, y, w, h, title):
        t = title.upper()
        if _w_group(t) + 40 > w:
            self.warns.append(f"título de grupo no entra: {title!r} ({_w_group(t):.0f} px en {w})")
        self.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{SOFT}" stroke="{LINE}" stroke-width="2"/>')
        self.o.append(f'<text x="{x + w / 2}" y="{y + 40}" font-size="{GROUP_PX}" font-weight="700" letter-spacing="2" fill="{P}" text-anchor="middle">{t}</text>')

    def box(self, x, y, w, h, label, kind="plain"):
        lines = [label] if isinstance(label, str) else list(label)
        fill, stroke, color, sw = KINDS[kind]
        for ln in lines:
            if _w_box(ln) + 36 > w:
                self.warns.append(f"texto no entra en la caja: {ln!r} ({_w_box(ln):.0f} px en {w})")
        if len(lines) * LINE_H + 16 > h:
            self.warns.append(f"{len(lines)} líneas no entran en {h} px de alto: {lines[0]!r}")
        self.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        y0 = y + h / 2 - (len(lines) - 1) * LINE_H / 2 + 10
        for i, ln in enumerate(lines):
            self.o.append(f'<text x="{x + w / 2}" y="{y0 + i * LINE_H}" font-size="{BOX_PX}" font-weight="600" fill="{color}" text-anchor="middle">{ln}</text>')

    def label(self, x, y, text):
        self.o.append(f'<text x="{x}" y="{y}" font-size="{LABEL_PX}" font-weight="600" fill="{ARROW}" text-anchor="middle">{text}</text>')

    def path(self, pts, dashed=False, head=True):
        pts_s = " ".join(f"{x},{y}" for x, y in pts)
        dash = ' stroke-dasharray="7 6"' if dashed else ""
        mk = ' marker-end="url(#a)"' if head else ""
        self.o.append(f'<polyline points="{pts_s}" fill="none" stroke="{ARROW}" stroke-width="2.4" stroke-linejoin="round"{dash}{mk}/>')

    def save(self, name, root="images"):
        for w in self.warns:
            print("WARN", w)
        svg = "\n".join(self.o + ["</svg>"])
        for sub in ("htmls", "pngs"):
            os.makedirs(os.path.join(root, sub), exist_ok=True)
        html = os.path.join(root, "htmls", name + ".html")
        open(html, "w", encoding="utf-8").write(
            f'<!doctype html>\n<html><head><meta charset="utf-8"><meta name="render-width" content="{self.w}">'
            f'<meta name="render-pad" content="0"><title>{name}</title></head>\n'
            f'<body style="margin:0;background:#fff">\n{svg}\n</body></html>\n')
        png = os.path.join(root, "pngs", name + ".png")
        subprocess.run(["rsvg-convert", "-w", str(self.w * 4 // 3), "-o", png], input=svg.encode(), check=True)
        return png
