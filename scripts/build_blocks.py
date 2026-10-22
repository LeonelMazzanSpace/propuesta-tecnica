#!/usr/bin/env python3
"""Genera los requests de Google Docs (update_doc) a partir de una lista de bloques.

Bloques (JSON): [["h2", "Título"], ["p", "Texto con **negrita**"], ...]
  h1   título de portada (solo en documentos sin plantilla, como primer bloque)
  h2   título de sección (Heading 2, salto de página antes)
  h3   subtítulo (Heading 3)
  p    párrafo normal
  b    viñeta (las viñetas consecutivas forman una lista)
  lbl  etiqueta en negrita que encabeza una lista (no aparece en el índice)
  img  marcador de imagen, por ejemplo "{{F1}}" (se reemplaza luego desde Chrome)
  cap  epígrafe de figura

Uso:
  build_blocks.py bloques.json --start 40 --delete-end 23206 --out lote
  build_blocks.py bloques.json --start 8115 --delete-end 9799 --trailing-newline --out lote
  build_blocks.py bloques.json --start 1 --delete-end 1 --page-setup --out lote   (documento nuevo sin plantilla)

--start         índice donde empieza el contenido nuevo (fin de la portada, o inicio del tramo a reemplazar)
--delete-end    fin del tramo a borrar antes de insertar (igual a --start para solo insertar)
--trailing-newline  usar cuando se inserta antes de párrafos existentes (no al final del cuerpo)
--page-setup    agrega al lote de texto el formato de página de SpaceDev (Carta, márgenes de 72 pt)

Escribe <out>_texto.json (borrado, inserción y estilo base) y <out>_estilos.json (títulos,
negritas, epígrafes y viñetas). Enviar el primero, verificar el texto y después el segundo.
"""
import argparse, json, re, sys

H2_COLOR = {"red": 0.2627, "green": 0.1961, "blue": 0.451}   # #433273
BODY_COLOR = {"red": 0.1529, "green": 0.1961, "blue": 0.2235}  # #273239
FONT = {"fontFamily": "Proxima Nova", "weight": 400}
SIZES = {"h1": 36, "h2": 14, "h3": 13, "body": 12, "cap": 10}


def pt(m):
    return {"magnitude": m, "unit": "PT"}


def u16(s):
    return len(s.encode("utf-16-le")) // 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("blocks")
    ap.add_argument("--start", type=int, required=True)
    ap.add_argument("--delete-end", type=int, required=True)
    ap.add_argument("--trailing-newline", action="store_true")
    ap.add_argument("--page-setup", action="store_true")
    ap.add_argument("--out", default="lote")
    a = ap.parse_args()

    blocks = json.load(open(a.blocks))
    paras, pos, full = [], a.start, []
    for kind, raw in blocks:
        bolds, out = [], ""
        for part in re.split(r"(\*\*.*?\*\*)", raw):
            if part.startswith("**") and part.endswith("**"):
                t = part[2:-2]
                s = pos + u16(out)
                out += t
                bolds.append((s, s + u16(t)))
            else:
                out += part
        for bad in ("—", ";", " - "):
            if bad in out:
                print(f"AVISO: '{bad}' en: {out[:60]}", file=sys.stderr)
        paras.append((kind, out, pos, pos + u16(out) + 1, bolds))
        full.append(out)
        pos += u16(out) + 1

    text = "\n".join(full) + ("\n" if a.trailing_newline else "")
    end = a.start + u16(text) + (0 if a.trailing_newline else 1)
    R = lambda s, e: {"startIndex": s, "endIndex": e}

    texto = []
    if a.page_setup:
        texto.append({"updateDocumentStyle": {"documentStyle": {
            "pageSize": {"width": pt(612), "height": pt(792)},
            "marginTop": pt(72), "marginBottom": pt(72), "marginLeft": pt(72), "marginRight": pt(72)},
            "fields": "pageSize,marginTop,marginBottom,marginLeft,marginRight"}})
    if a.delete_end > a.start:
        texto.append({"deleteContentRange": {"range": R(a.start, a.delete_end)}})
    texto += [
        {"insertText": {"location": {"index": a.start}, "text": text}},
        {"updateParagraphStyle": {"range": R(a.start, end), "paragraphStyle": {
            "namedStyleType": "NORMAL_TEXT", "alignment": "START", "lineSpacing": 115,
            "spaceAbove": pt(0), "spaceBelow": pt(10), "indentStart": pt(0), "indentFirstLine": pt(0),
            "keepWithNext": False, "pageBreakBefore": False},
            "fields": "namedStyleType,alignment,lineSpacing,spaceAbove,spaceBelow,indentStart,indentFirstLine,keepWithNext,pageBreakBefore"}},
        {"updateTextStyle": {"range": R(a.start, end), "textStyle": {
            "weightedFontFamily": FONT, "fontSize": pt(SIZES["body"]),
            "foregroundColor": {"color": {"rgbColor": BODY_COLOR}}, "bold": False, "italic": False},
            "fields": "weightedFontFamily,fontSize,foregroundColor,bold,italic"}},
    ]

    est = []
    groups, cur = [], None
    for k, t, s, e, b in paras:
        if k == "b":
            if cur and cur[1] == s:
                cur[1] = e
            else:
                cur = [s, e]
                groups.append(cur)
        else:
            cur = None
    for k, t, s, e, b in paras:
        if k == "h1":
            # Portada sin plantilla: el espacio superior ubica el título como en la plantilla.
            est.append({"updateParagraphStyle": {"range": R(s, e), "paragraphStyle": {
                "namedStyleType": "HEADING_1", "alignment": "CENTER", "spaceAbove": pt(250), "spaceBelow": pt(0)},
                "fields": "namedStyleType,alignment,spaceAbove,spaceBelow"}})
            est.append({"updateTextStyle": {"range": R(s, e - 1), "textStyle": {
                "weightedFontFamily": FONT, "fontSize": pt(SIZES["h1"]),
                "foregroundColor": {"color": {"rgbColor": H2_COLOR}}, "bold": False},
                "fields": "weightedFontFamily,fontSize,foregroundColor,bold"}})
        elif k == "h2":
            # El cambio de namedStyleType borra el estilo de texto: el estilo de texto va después.
            est.append({"updateParagraphStyle": {"range": R(s, e), "paragraphStyle": {
                "namedStyleType": "HEADING_2", "pageBreakBefore": True, "keepWithNext": True,
                "spaceAbove": pt(0), "spaceBelow": pt(14)},
                "fields": "namedStyleType,pageBreakBefore,keepWithNext,spaceAbove,spaceBelow"}})
            est.append({"updateTextStyle": {"range": R(s, e - 1), "textStyle": {
                "weightedFontFamily": FONT, "fontSize": pt(SIZES["h2"]),
                "foregroundColor": {"color": {"rgbColor": H2_COLOR}}, "bold": True},
                "fields": "weightedFontFamily,fontSize,foregroundColor,bold"}})
        elif k == "h3":
            est.append({"updateParagraphStyle": {"range": R(s, e), "paragraphStyle": {
                "namedStyleType": "HEADING_3", "keepWithNext": True, "indentStart": pt(0),
                "indentFirstLine": pt(0), "spaceAbove": pt(16), "spaceBelow": pt(8)},
                "fields": "namedStyleType,keepWithNext,indentStart,indentFirstLine,spaceAbove,spaceBelow"}})
            est.append({"updateTextStyle": {"range": R(s, e - 1), "textStyle": {
                "weightedFontFamily": FONT, "fontSize": pt(SIZES["h3"]),
                "foregroundColor": {"color": {"rgbColor": BODY_COLOR}}, "bold": True},
                "fields": "weightedFontFamily,fontSize,foregroundColor,bold"}})
        elif k == "lbl":
            est.append({"updateParagraphStyle": {"range": R(s, e), "paragraphStyle": {
                "keepWithNext": True, "spaceAbove": pt(12), "spaceBelow": pt(6)},
                "fields": "keepWithNext,spaceAbove,spaceBelow"}})
        elif k == "img":
            est.append({"updateParagraphStyle": {"range": R(s, e), "paragraphStyle": {
                "alignment": "CENTER", "spaceAbove": pt(6), "spaceBelow": pt(4), "keepWithNext": True},
                "fields": "alignment,spaceAbove,spaceBelow,keepWithNext"}})
        elif k == "cap":
            est.append({"updateParagraphStyle": {"range": R(s, e), "paragraphStyle": {
                "alignment": "CENTER", "spaceBelow": pt(14)}, "fields": "alignment,spaceBelow"}})
            est.append({"updateTextStyle": {"range": R(s, e - 1), "textStyle": {
                "italic": True, "fontSize": pt(SIZES["cap"])}, "fields": "italic,fontSize"}})
        if k not in ("h1", "h2", "h3"):
            for bs, be in b:
                est.append({"updateTextStyle": {"range": R(bs, be), "textStyle": {"bold": True}, "fields": "bold"}})
    for s, e in groups:
        est.append({"updateParagraphStyle": {"range": R(s, e), "paragraphStyle": {"spaceBelow": pt(4)}, "fields": "spaceBelow"}})
        est.append({"updateParagraphStyle": {"range": R(e - 1, e), "paragraphStyle": {"spaceBelow": pt(10)}, "fields": "spaceBelow"}})
        est.append({"createParagraphBullets": {"range": R(s, e), "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"}})

    json.dump(texto, open(f"{a.out}_texto.json", "w"), ensure_ascii=False)
    json.dump(est, open(f"{a.out}_estilos.json", "w"), ensure_ascii=False)
    h3 = sum(1 for p in paras if p[0] == "h3")
    print(f"texto: {len(text)} caracteres, fin {end}; requests texto {len(texto)}, estilos {len(est)}; H3 {h3}")


if __name__ == "__main__":
    main()
