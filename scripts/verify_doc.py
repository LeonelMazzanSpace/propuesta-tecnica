#!/usr/bin/env python3
"""Verifica un Google Doc contra los bloques que se escribieron.

Uso:
  verify_doc.py doc.json bloques.json --start 40 [--text-only] [--cover-from doc_anterior.json]

doc.json es el resultado de read_doc tal como lo guarda la herramienta ({"content": {...}}).
--text-only    solo compara el texto (para validar el lote de texto antes de aplicar estilos)
--cover-from   compara la portada (todo lo anterior a --start) con una lectura previa

Comprueba formato de página (Carta, márgenes de 72 pt), texto, estilo de párrafo, viñetas, negritas efectivas, fuente, tamaño y color,
cantidad de imágenes y marcadores {{...}} sin reemplazar. Imprime "errores 0" si todo coincide.
"""
import argparse, json, re

EXPECT = {"h1": (36, "#433273"), "h2": (14, "#433273"), "h3": (13, "#273239"), "cap": (10, "#273239")}
BODY = (12, "#273239")
STYLE = {"h1": "HEADING_1", "h2": "HEADING_2", "h3": "HEADING_3"}


def load(path):
    d = json.load(open(path))
    return d.get("content", d)


def body_paras(doc, start):
    tab = doc["tabs"][0]["documentTab"] if "tabs" in doc else doc
    return tab, [el for el in tab["body"]["content"] if "paragraph" in el and el["startIndex"] >= start]


def text_of(p):
    return "".join(e.get("textRun", {}).get("content", "") for e in p["elements"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("doc")
    ap.add_argument("blocks")
    ap.add_argument("--start", type=int, required=True)
    ap.add_argument("--text-only", action="store_true")
    ap.add_argument("--cover-from")
    a = ap.parse_args()

    doc = load(a.doc)
    blocks = json.load(open(a.blocks))
    tab, paras = body_paras(doc, a.start)
    ns = {s["namedStyleType"]: s["textStyle"] for s in tab["namedStyles"]["styles"]}
    print("revisionId", doc.get("revisionId"))

    errs = imgs = marks = 0
    ds = tab["documentStyle"]
    page = (ds["pageSize"]["width"].get("magnitude"), ds["pageSize"]["height"].get("magnitude"),
            *(ds[m].get("magnitude") for m in ("marginTop", "marginBottom", "marginLeft", "marginRight")))
    if page != (612, 792, 72, 72, 72, 72):
        errs += 1; print("PÁGINA", page)

    if a.cover_from:
        old = load(a.cover_from)
        cov = lambda d: [(text_of(el["paragraph"]), json.dumps(el["paragraph"]["paragraphStyle"], sort_keys=True))
                         for el in (d["tabs"][0]["documentTab"] if "tabs" in d else d)["body"]["content"]
                         if "paragraph" in el and el["startIndex"] < a.start]
        print("portada intacta:", cov(doc) == cov(old))

    def eff(st, ts, key):
        v = ts.get(key)
        return v if v is not None else ns.get(st, {}).get(key, ns["NORMAL_TEXT"].get(key))

    for (k, raw), el in zip(blocks, paras):
        p = el["paragraph"]
        st = p["paragraphStyle"]["namedStyleType"]
        t = text_of(p).rstrip("\n")
        imgs += sum(1 for e in p["elements"] if "inlineObjectElement" in e)
        marks += len(re.findall(r"\{\{.*?\}\}", t))
        want_t = re.sub(r"\*\*(.*?)\*\*", r"\1", raw)
        if not (k == "img" and not t) and t != want_t:
            errs += 1
            print("TEXTO", el["startIndex"], repr(t[:50]), "!=", repr(want_t[:50]))
        if a.text_only:
            continue
        if st != STYLE.get(k, "NORMAL_TEXT"):
            errs += 1; print("ESTILO", k, t[:40])
        if ("bullet" in p) != (k == "b"):
            errs += 1; print("VIÑETA", k, t[:40])
        bolds = {e["textRun"]["content"].strip() for e in p["elements"]
                 if "textRun" in e and e["textRun"]["content"].strip() and eff(st, e["textRun"]["textStyle"], "bold")}
        want_b = {want_t} if k in ("h2", "h3") else set(re.findall(r"\*\*(.*?)\*\*", raw))
        if bolds != want_b:
            errs += 1; print("NEGRITA", k, bolds, want_b)
        for e in p["elements"]:
            tr = e.get("textRun")
            if not tr or not tr["content"].strip():
                continue
            ts = tr["textStyle"]
            fam = eff(st, ts, "weightedFontFamily")
            size = eff(st, ts, "fontSize")["magnitude"]
            col = eff(st, ts, "foregroundColor")["color"]["rgbColor"]
            h = "#%02x%02x%02x" % tuple(round(col.get(c, 0) * 255) for c in ("red", "green", "blue"))
            if fam["fontFamily"] != "Proxima Nova" or fam["weight"] != 400 or (size, h) != EXPECT.get(k, BODY):
                errs += 1; print("FORMATO", k, fam, size, h, t[:30])
    if len(paras) < len(blocks):
        errs += 1; print("FALTAN PÁRRAFOS", len(paras), "de", len(blocks))
    print(f"párrafos {min(len(paras), len(blocks))}/{len(blocks)} imágenes {imgs} marcadores {marks} errores {errs}")


if __name__ == "__main__":
    main()
