# Flujo de escritura en Google Docs

Pasos y lecciones de la primera propuesta hecha con esta skill. `<skill>` es la carpeta de la skill.

## Preparación

- Cargar `anthropic-skills:google-workspace` y leer su `references/docs.md`.
- Las herramientas de Google Docs pueden ser diferidas: cargarlas con ToolSearch (en Claude Code se llaman `mcp__claude_ai_Google_Docs__read_doc` y `mcp__claude_ai_Google_Docs__update_doc`; en otras superficies el nombre puede variar). Si solo aparece `authenticate`, pedirle al usuario que corra `/mcp` y autorice "claude.ai Google Docs".
- `read_doc` de un documento con imágenes supera el límite y se guarda en un archivo: trabajar ese archivo con `jq` o Python, nunca leerlo entero en el contexto.

## Ubicar el punto de escritura

```bash
python3 -I -c '
import json,sys
d=json.load(open(sys.argv[1]))["content"]
print(d["revisionId"])
for el in d["tabs"][0]["documentTab"]["body"]["content"]:
    p=el.get("paragraph")
    if p: print(el["startIndex"],el["endIndex"],p["paragraphStyle"]["namedStyleType"],repr("".join(e.get("textRun",{}).get("content","") for e in p["elements"])[:40]))
' <read_doc guardado>
```

- **Con plantilla**: la portada de la plantilla de SpaceDev termina antes del primer H2 (en la plantilla usada hasta ahora, en el índice 40, pero confirmarlo siempre con la lectura). Escribir desde ese índice y borrar hasta `fin del cuerpo - 1` (el último salto de línea del cuerpo no se puede borrar).
- Título de portada, en un solo lote: insertar el nombre del proyecto en mayúsculas en el `inicio` del párrafo H1, borrar el texto viejo que quedó después (`[inicio + largo nuevo, fin + largo nuevo - 1]`) y aplicar `updateTextStyle` sobre el nombre nuevo con Proxima Nova 400, 36 y #433273. No borrar primero: el salto de línea del H1 tiene otro formato (26 pt, sin color) y el texto insertado lo heredaría. Leer de nuevo y guardar esa lectura como referencia de portada.
- **Sin plantilla**: crear el documento con Drive `create_file` (título del proyecto y `contentMimeType` `application/vnd.google-apps.document`) y leerlo. El cuerpo vacío es un solo salto de línea en `[1, 2)`. Poner `["h1", "NOMBRE DEL PROYECTO"]` como primer bloque y generar con `--start 1 --delete-end 1 --page-setup`. El H2 siguiente ya trae salto de página, así que el título queda solo en la portada. Verificar con `--start 1` y sin `--cover-from`. Los documentos nuevos pueden venir en A4 según la configuración regional de la cuenta: `--page-setup` lo corrige y `verify_doc.py` marca `PÁGINA` si no quedó en Carta con márgenes de 72.
- Para reemplazar solo una sección: `--start` en el primer párrafo del tramo, `--delete-end` en el inicio del párrafo siguiente que se conserva, y `--trailing-newline`.

## Generar y enviar

```bash
python3 <skill>/scripts/build_blocks.py bloques.json --start <fin de portada> --delete-end <fin del cuerpo - 1> --out lote
python3 <skill>/scripts/verify_doc.py <read_doc guardado> bloques.json --start <fin de portada> --cover-from <lectura de referencia>
```

- `lote_texto.json` va en un `update_doc` con `writeControl.requiredRevisionId` de la última lectura.
- Volver a leer y correr `verify_doc.py ... --text-only`. Si hay una diferencia, corregir antes de seguir: los estilos dependen de índices exactos.
- Enviar `lote_estilos.json` con la nueva revisión, leer otra vez y correr `verify_doc.py` completo. El objetivo es `errores 0`.
- Los requests se transcriben en la llamada a la herramienta. Para reducir errores, imprimirlos uno por línea y en el orden en que se envían.
- Varias operaciones en un mismo lote: aplicarlas de mayor a menor índice. Los estilos de un tramo se aplican antes de insertar texto en otro tramo anterior.

## Lecciones aprendidas

- **Estilos con nombre**: la API no los modifica. Se aplica formato directo. Al cambiar `namedStyleType`, el estilo de texto del párrafo vuelve al del estilo con nombre, así que la fuente, el tamaño, el color y la negrita del título se aplican después.
- **Colores y tamaños**: H2 #433273 en 14, H3 #273239 en 13, texto #273239 en 12. Errores previos: usar #273279 (azul) en lugar de #273239, y texto normal en 13 en lugar de 12.
- **Heading 3 de la plantilla** trae sangría de 36 pt: anularla con `indentStart` e `indentFirstLine` en 0.
- **Índice lateral**: con muchos H3 se vuelve ilegible. Mantener entre 15 y 18 y usar etiquetas en negrita (`lbl`) para roles e ítems.
- **Verificación visual**: exportar a PDF (`download_file_content` con `application/pdf`, que se guarda en un archivo) y correr `contact_sheet.py`. La primera página "Analysis" del PDF es el nombre de la pestaña, no un error.
- **Figura que no entra al final de página**: deja espacio en blanco. Es aceptable. Si molesta, achicar la imagen o mover el párrafo anterior.
- **Comandos con `rm`** pueden ser rechazados por permisos: generar en carpetas nuevas en lugar de borrar.
