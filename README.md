# propuesta-tecnica-gdocs

Skill de Claude Code que genera la propuesta técnica y la estimación de un proyecto (Technical Analysis) para un cliente de SpaceDev, escrita directamente en un Google Doc con el formato de la casa. Parte de los documentos del cliente (PDF, docx, notas de llamadas, atlas, manuales, RFP) y entrega el documento, las figuras en PNG y una revisión final hecha con subagentes.

## Qué produce

- **Un Google Doc** con seis secciones por defecto, más las que exija el documento fuente (pliego, RFP, brief):
  1. Descripción General
  2. Descripción de la Plataforma
  3. MVP y NO MVP
  4. Composición del Equipo y Responsabilidades por Rol
  5. Propuesta de Infraestructura
  6. Estimación por Sprints
- **Una carpeta `images/`** en el directorio donde se ejecuta la skill, lista para pasarle al cliente: `htmls/` con los crudos editables, `pngs/` con los finales y `IMAGENES.md` con el plan.
- Un resumen final con lo que quedó en cada sección, lo que corrigió la revisión y lo que queda por decidir.

## Requisitos

- **Conectores de Claude**: Google Docs (lectura y edición) y Google Drive (`copy_file` / `create_file`). Si Google Docs pide autenticación, correr `/mcp` y autorizar "claude.ai Google Docs".
- **Skills de Claude**: `anthropic-skills:google-workspace` (se lee antes de escribir en el Doc) y `claude-in-chrome` (para pegar las imágenes).
- **Chrome** con la extensión de Claude, porque la API de Docs exige una URL pública para las imágenes y el material del cliente es confidencial.
- **Python 3** con `Pillow`.
- **Herramientas locales**: `pdftotext` y `pdftoppm` (poppler), Chrome o Chromium para renderizar HTML a PNG, y `rsvg-convert` para `diagram_kit.py`. Opcional: `magick` para achicar PNG antes de revisarlos.
- Opcional: la **plantilla de SpaceDev** en Google Docs. Aporta logo, borde violeta y encabezado, que la API no puede recrear. Sin plantilla se crea un Doc nuevo con la misma tipografía y diseño, pero sin logo ni marco.

## Instalación

Copiar esta carpeta al directorio de skills:

```bash
cp -r propuesta-tecnica-gdocs ~/.claude/skills/
```

## Uso

Se activa sola cuando el pedido coincide con su descripción ("armá la propuesta técnica", "estimá por sprints", "technical analysis", "project estimate", "rehacé la propuesta"), con o sin mencionar la skill o Google Docs.

Antes de empezar pregunta, en un solo mensaje, lo que falte:

1. Documentos fuente (única fuente de verdad del contenido).
2. Idioma del documento final.
3. Google Doc destino y si hay plantilla de SpaceDev.
4. Modalidad de estimación.
5. Restricciones de alcance, equipo o tiempo.
6. Si hay pantallas, si se arman mockups y si existe manual de marca.
7. Opcional: un documento de referencia de estructura, solo para estructura y estilo.

### Modalidades de estimación

| Modalidad | Estructura | Conviene cuando |
|---|---|---|
| **A. Discovery más fases** | Discovery de 2 semanas y fases de varios sprints, cada una con un "Hito técnico" | El alcance es grande o ambiguo |
| **B. Sprints directos** | Lista de "Sprint N" con objetivo, actividades y resultado | El alcance del MVP ya está claro |

Los sprints son siempre de dos semanas.

## Cómo funciona

1. **Insumos:** pide lo que falte y no repite lo que el usuario ya dijo.
2. **Lectura de fuentes:** busca primero las secciones que el documento fuente exige, las reemplaza o suma a las por defecto y cuenta la correspondencia antes de redactar.
3. **Redacción:** escribe los bloques en JSON (`h2`, `h3`, `p`, `b`, `lbl`, `img`, `cap`) siguiendo `references/guia-de-contenido.md`.
4. **Escritura en el Doc:** `build_blocks.py` genera los requests; primero se envía el texto, se verifica carácter por carácter con `verify_doc.py --text-only` y recién después los estilos.
5. **Imágenes:** diagramas con `diagram_kit.py`, plantillas HTML de `assets/`, render con `render_html.py` y trabajo en paralelo con subagentes. Se pegan en el Doc desde Chrome sobre los marcadores `{{F1}}`…
6. **Revisión visual:** exporta a PDF y arma una hoja de miniaturas con `contact_sheet.py` para detectar páginas en blanco, títulos huérfanos e imágenes mal ubicadas.
7. **Revisión final:** un subagente por imagen y uno para el documento completo, en paralelo. Revisan coherencia con el texto y la fuente, cifras, corrección técnica, legibilidad, redacción y riesgo comercial. El agente principal verifica los hallazgos graves, corrige y vuelve a verificar.

### Ajustes sobre una propuesta existente

Reemplaza solo el tramo afectado (`--start`, `--delete-end`, `--trailing-newline`), sin reescribir el documento ni tocar las imágenes, y verifica el documento completo al terminar.

## Estándar visual de SpaceDev

| Elemento | Valor |
|---|---|
| Fuente | Proxima Nova, peso Normal (la negrita es un atributo) |
| Violeta SpaceDev | `#433273` (títulos H1 y H2, acentos) |
| Gris de texto | `#273239` (texto, H3 y epígrafes) |
| Tamaños | H1 36, H2 14, H3 13, texto 12, epígrafe 10 |
| Página | Carta (612 × 792 pt), márgenes de 72 pt |
| Imágenes | Ancho completo de página (468 pt), centradas, con epígrafe "Figura N. Descripción" |

Todos los valores están aplicados en `build_blocks.py` y controlados en `verify_doc.py`.

## Reglas de redacción

- Tono profesional, formal y conciso, como propuesta de un arquitecto.
- Sin "—", "-" ni ";" como recurso de redacción.
- Sin menciones a conversaciones previas, documentos de referencia ni nombres de participantes.
- Sin afirmaciones comerciales genéricas ni palabras de relleno.
- El stack de la empresa no se fuerza: Next.js solo con SEO, IA solo si aporta valor real.
- Equipo: todos los desarrolladores son Senior Fullstack con una orientación; no hay Tech Lead ni Arquitecto; QA y Project Manager a tiempo parcial.

## Qué no hace

- No usa un documento de referencia como fuente de contenido ni lo menciona en el texto.
- No inventa contenido: todo sale de los documentos fuente.
- Con plantilla, no toca el logo, el borde, el encabezado ni los párrafos vacíos de la portada; solo cambia el texto del título.
- No inserta imágenes por URL pública: el material del cliente es confidencial.

## Archivos

| Archivo | Contenido |
|---|---|
| `SKILL.md` | Instrucciones de la skill |
| `references/guia-de-contenido.md` | Plantilla de cada sección, secciones exigidas por la fuente y detalle del discovery o primer sprint |
| `references/flujo-google-docs.md` | Pasos para escribir en el Doc y lecciones aprendidas |
| `references/imagenes.md` | Tipos de figura, carpeta `images/`, legibilidad y trabajo con subagentes |
| `references/insercion-de-imagenes.md` | Cómo pegar los PNG desde Chrome sobre los marcadores |
| `references/revision-final.md` | Revisión final con subagentes: insumos y prompts |
| `scripts/build_blocks.py` | Genera los requests de `update_doc` a partir de los bloques JSON |
| `scripts/verify_doc.py` | Verifica texto, estilos, página, portada e imágenes del Doc contra los bloques |
| `scripts/diagram_kit.py` | Kit para diagramas de flujo con el estilo de la propuesta |
| `scripts/render_html.py` | Renderiza `images/htmls/*.html` a PNG con Chrome headless a 2x |
| `scripts/contact_sheet.py` | Arma la hoja de miniaturas a partir de la exportación PDF |
| `assets/plataforma-modulos.html` | Plantilla del diagrama de módulos |
| `assets/infraestructura-aws.html` | Plantilla del diagrama de infraestructura con la visual de AWS |
| `assets/pantalla-base.html` | Plantilla base de mockups de pantallas |
