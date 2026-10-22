---
name: propuesta-tecnica-gdocs
description: Genera una propuesta técnica y estimación de proyecto (Technical Analysis) para un cliente de SpaceDev, escrita directamente en un Google Doc con el formato de la casa. Úsala siempre que el usuario pida definir, estimar o armar la propuesta, el análisis técnico, el discovery o la estimación por sprints de una plataforma a partir de documentos del cliente (PDF, docx, notas de llamadas, atlas, manuales, RFP), aunque no diga "skill" ni "Google Doc", y también cuando pida rehacer o ajustar una propuesta de ese tipo. También aplica a pedidos en inglés como "technical analysis", "project estimate", "sprint plan" o "proposal" para un cliente.
---

# Propuesta técnica en Google Docs

Esta skill produce un documento de propuesta tecnológica con seis secciones por defecto (descripción general, plataforma, MVP y NO MVP, equipo, infraestructura y estimación), más las que exija el documento fuente, escrito como lo haría un arquitecto de software y con el formato visual de SpaceDev. El documento vive en un Google Doc, copiado de la plantilla de SpaceDev o creado desde cero con el mismo estándar visual.

## 1. Antes de empezar: pedir los insumos

Pregunta, en un solo mensaje, lo que falte:

1. **Documentos fuente**: carpeta o archivos que describen la plataforma (notas de llamadas, PDFs del cliente, comparativas, manuales de marca). Son la única fuente de verdad del contenido.
2. **Idioma** del documento final. Todo va en ese idioma: títulos, epígrafes ("Figura") y etiquetas fijas como "Hito técnico", "Entregables", "Resultado", "Duración estimada" y "tiempo completo".
3. **Google Doc destino** (URL con `?tab=`). La **plantilla de SpaceDev** es opcional:
   - **Con plantilla** (preferida si existe): un documento copiado de la plantilla, o el link de la plantilla para copiarla con Drive (`copy_file`). Aporta el logo, el borde violeta y el encabezado, que son dibujos que la API no puede recrear.
   - **Sin plantilla**: crear un Google Doc nuevo con Drive (`create_file`). Lleva la misma tipografía, formato de página y diseño, con una portada de solo el título. Avisar al usuario que no tendrá logo ni marco.
4. **Modalidad de estimación**:
   - **A. Discovery más fases**: discovery de 2 semanas y fases de varios sprints, cada una con un hito técnico. Conviene cuando el alcance es grande o ambiguo.
   - **B. Sprints directos**: sin discovery, una lista de "Sprint N" con objetivo, actividades y resultado. Conviene cuando el alcance del MVP ya está claro.
5. **Restricciones de alcance, equipo o tiempo** que el usuario ya tenga en mente (por ejemplo "4 meses con 3 desarrolladores", "son dos productos"). Si no las hay, proponer el equipo según el alcance.
6. **Pantallas**: si el producto tiene interfaz, confirmar que se arman los mockups y pedir el manual de marca (colores, tipografía, logo) si existe.
7. Opcional: un documento de referencia de estructura. Se usa solo para estructura y estilo, nunca como fuente de contenido ni se menciona en el texto.

Si el usuario ya dio algo de esto en la conversación, no lo vuelvas a pedir.

## 2. Leer las fuentes

- docx: extraer texto con `python3 -I` y `zipfile` (no hay pandoc). PDFs: `pdftotext -layout`, y `pdftoppm` para ver diagramas o pantallas.
- **Primero, buscar secciones exigidas.** Antes de planificar la estructura, revisar si el documento fuente (pliego, RFP, brief) pide explícitamente secciones o contenidos ("la propuesta debe incluir", "qué tiene que traer la propuesta", criterios de evaluación). Las exigidas se incluyen; si se parecen a una por defecto, la reemplazan con el nombre del documento fuente. El procedimiento está en `references/guia-de-contenido.md`, "Secciones exigidas por el documento fuente". Contarle al usuario la correspondencia en una línea antes de redactar.
- Identificar: qué es el producto, quién lo usa, módulos, qué es MVP y qué queda afuera, dependencias de terceros, riesgos regulatorios, presupuesto y plazos mencionados.
- Si el material sugiere que la plataforma completa son en realidad varios productos (por ejemplo custodia y no custodia), dilo en la propuesta y planifícalos por separado: fases distintas en la modalidad A, sprints distintos en la B.

## 3. Contenido y estructura

Leer `references/guia-de-contenido.md` antes de redactar. Resumen de lo esencial:

- Seis secciones H2 por defecto, en este orden: Descripción General, Descripción de la Plataforma, MVP y NO MVP, Composición del Equipo y Responsabilidades por Rol, Propuesta de Infraestructura, Estimación por Sprints (traducidas al idioma pedido). Las secciones exigidas por el documento fuente se suman o reemplazan a las equivalentes.
- **MVP y NO MVP** deja explícito qué se entrega, qué se suma solo si el caso lo requiere (y si entra o no en las horas) y qué queda afuera. Reemplaza el viejo "Fuera del alcance" de la plataforma.
- El índice lateral debe leerse de un vistazo: entre 15 y 18 H3 en total. Todo lo demás va como ítems con etiqueta en negrita, no como títulos.
- Nivel de detalle intermedio: técnico y con criterio, sin relleno. El documento completo ronda 14 a 18 páginas.
- La Estimación sigue la modalidad elegida (A o B). Solo en la modalidad A se menciona el discovery en la Descripción General, el equipo y la infraestructura. En la B, lo que queda por validar se resuelve en el primer sprint.
- Equipo SpaceDev: todos los desarrolladores son **Senior Fullstack con una orientación** (por ejemplo Blockchain, Backend e integraciones, Frontend y producto). La cantidad sale del alcance o de lo que pida el usuario; tres es un punto de partida habitual. No existe el rol de Tech Lead ni Arquitecto: uno de los senior actúa como referente técnico. QA y Project Manager a tiempo parcial.

## 4. Imágenes

Leer `references/imagenes.md` antes de armar cualquier figura. Todas las imágenes quedan en la carpeta `images/` del directorio donde se ejecuta la skill: `images/htmls/` con los crudos editables, `images/pngs/` con los finales (mismo nombre base) e `images/IMAGENES.md` con el plan. Esa carpeta es también lo que se le entrega al cliente.

- **Descripción General**: visión general y plan de fases o sprints con sus entregables, con `scripts/diagram_kit.py`.
- **Descripción de la Plataforma**:
  - diagrama de módulos (`assets/plataforma-modulos.html`) con los módulos de dominio que nombra el texto;
  - flujos del dominio con `diagram_kit`, con solo el nombre de cada componente, nunca recortes del material del cliente;
  - si el producto tiene interfaz, mockups de todas las pantallas del MVP (`assets/pantalla-base.html`). En el documento van 2 a 4 pantallas clave; el resto se entrega en la carpeta.
- **Propuesta de Infraestructura sobre AWS**: diagrama `assets/infraestructura-aws.html` con la visual de AWS (contenedores de nube, región, VPC, zonas y subredes, e íconos de servicio con el color de su categoría) y solo los servicios que nombra el texto. Tiene que ser técnicamente correcto: zonas que exigen el ALB y RDS, salida de las subredes privadas, servicios regionales, lo opcional punteado.

**Legibilidad**: las imágenes se insertan a 468 pt de ancho, así que un texto de px píxeles se lee a `px ÷ render-width × 468` pt. Mínimo de 6,5 pt en diagramas y unos 6 pt en pantallas. Las plantillas de `assets/` ya vienen con anchos y tamaños legibles (tabla en `imagenes.md`). Si no entra, se quita contenido, no se achica la letra.

Las imágenes se hacen después de redactar los bloques, con un plan y subagentes, que es lo más eficiente:
- el agente principal escribe `IMAGENES.md`, una especificación común (decisiones técnicas, roles, plan y una tabla de datos canónicos para las pantallas) y la base visual (la pantalla de referencia se aprueba con el usuario);
- despacha lotes por tipo en paralelo (flujos; módulos e infraestructura; pantallas);
- revisa cada PNG antes de insertarlo.

Los HTML se renderizan con `scripts/render_html.py` (Chrome headless a 2x). Los diagramas usan Noto Sans porque Proxima Nova no suele estar instalada localmente.

## 5. Escribir en el Google Doc

Leer primero la skill `anthropic-skills:google-workspace` y su `references/docs.md`. El conector de Google Docs puede pedir autenticación (`/mcp`). Drive solo cambia título y carpeta, no contenido.

Flujo probado (detalles en `references/flujo-google-docs.md`):

1. `read_doc` y ubicar dónde empieza el contenido.
   - **Con plantilla**: el contenido empieza donde termina la portada (primer H2 de la plantilla). De la portada solo se cambia el título H1, que lleva el nombre del proyecto en mayúsculas, reemplazando únicamente su texto. Logo, borde, encabezado y párrafos vacíos no se tocan. Después de cambiar el título, guardar esa lectura como referencia de la portada para las verificaciones siguientes.
   - **Sin plantilla**: el contenido empieza en el índice 1. El primer bloque es `["h1", "NOMBRE DEL PROYECTO"]` y `build_blocks.py` se corre con `--page-setup` para fijar el tamaño Carta y los márgenes. No hay portada que comparar.
2. Escribir el contenido como lista de bloques JSON (`h2`, `h3`, `p`, `b`, `lbl`, `img`, `cap`, con `**negrita**` en línea) y generar los requests con `scripts/build_blocks.py`.
3. Enviar el texto en un lote, verificar con `scripts/verify_doc.py --text-only` que coincide carácter por carácter, y recién después enviar el lote de estilos. Así un error de transcripción no deja estilos en posiciones equivocadas.
4. Verificar estilos y formato de página con `scripts/verify_doc.py` (cero errores) y, con plantilla, la portada intacta respecto de la lectura de referencia (`--cover-from`).
5. Insertar las imágenes de `images/pngs/` con Chrome reemplazando los marcadores `{{F1}}`… (ver `references/insercion-de-imagenes.md`). La API exige URL pública y el material es confidencial, por eso se pegan desde el navegador.
6. Exportar a PDF, armar la hoja de miniaturas con `scripts/contact_sheet.py` y revisar páginas en blanco, títulos huérfanos e imágenes.
7. **Revisión final con subagentes** (`references/revision-final.md`):
   - un subagente por imagen (las del documento y las de la carpeta de entrega) y uno para el documento completo, lanzados en paralelo;
   - revisan coherencia con el texto y el documento fuente, cifras, corrección técnica, legibilidad, redacción y riesgo comercial;
   - el agente principal verifica los hallazgos graves, los consolida para el usuario, corrige texto e imágenes, reemplaza las figuras que cambiaron y vuelve a verificar.

**Ajustes sobre una propuesta existente**: reemplazar solo el tramo afectado (`--start`, `--delete-end` y `--trailing-newline`), sin reescribir el documento ni tocar las imágenes. Para cambios de formato puntuales, como un tamaño o un color, aplicar `updateTextStyle` sobre los rangos de los párrafos de ese tipo. Siempre verificar el documento completo al terminar.

## 6. Estándar visual de SpaceDev

Este es el estándar de la empresa. Todos los valores salen del documento aprobado y ya están aplicados en `scripts/build_blocks.py` y controlados en `scripts/verify_doc.py`.

**Paleta y fuente**
- Violeta SpaceDev: **#433273** (títulos principales y acentos).
- Gris de texto: **#273239** (texto, Heading 3 y epígrafes). Es gris oscuro, no azul: no confundirlo con #273279.
- Fuente única: **Proxima Nova**, peso Normal (400). La negrita se aplica como atributo, no como otro peso.

**Tipografía y espaciado**

| Elemento | Tamaño y color | Formato de párrafo |
|---|---|---|
| Heading 1 (título de portada) | 36, #433273 | Centrado, nombre del proyecto en mayúsculas. Sin plantilla, 250 arriba para ubicarlo como en la plantilla |
| Heading 2 (sección) | 14, #433273, negrita | Salto de página antes, 0 arriba, 14 abajo, se mantiene con el siguiente |
| Heading 3 (subsección) | 13, #273239, negrita | Sangría 0 (la plantilla trae 36), 16 arriba, 8 abajo, se mantiene con el siguiente |
| Texto normal | 12, #273239 | Interlineado 115 %, 0 arriba, 10 abajo, alineado a la izquierda |
| Viñetas | 12, #273239 | Viñeta de disco, 4 abajo entre ítems y 10 después del último |
| Etiqueta (`lbl`) | 12, #273239, negrita | 12 arriba, 6 abajo, se mantiene con el siguiente |
| Imagen | Ancho completo de página (468 pt) | Centrada, 6 arriba, 4 abajo, se mantiene con el epígrafe |
| Epígrafe | 10, #273239, cursiva | Centrado, 14 abajo, "Figura N. Descripción" |

**Página**: tamaño Carta (612 × 792 pt) y márgenes de 72 pt. La plantilla ya los trae y además aporta el encabezado y pie a 36 pt, el logo de SPACE en todas las páginas y la portada con marco y primera página distinta; con plantilla no se modifica nada de esto. Sin plantilla, `--page-setup` aplica el tamaño y los márgenes, y el documento queda sin logo ni marco.

**Diagramas de flujo**: fondo blanco, grupos en #f4f3f8 con borde #c4c2d4, cajas destacadas con borde #433273, flechas #6b6880. Verde, ámbar y rojo se usan solo para estados. Los diagramas de módulos e infraestructura AWS siguen el estilo de sus plantillas, con colores de categoría de AWS en los servicios.

La API no puede modificar los estilos con nombre, así que el formato se aplica directo sobre el texto. Al cambiar `namedStyleType` se borra el estilo de texto del párrafo, por eso el estilo de texto de cada título se aplica después del cambio de estilo de párrafo (el script ya lo hace en ese orden).

## 7. Reglas de redacción

- Tono profesional, formal y conciso, como propuesta de un arquitecto.
- Evitar "—", "-" y ";" como recurso de redacción. Usar coma, dos puntos o una oración nueva.
- No mencionar conversaciones previas, documentos de referencia ni nombres de quienes participaron.
- Sin afirmaciones comerciales genéricas ni palabras de relleno ("robusto", "potenciar", "de punta a punta" solo si es literal).
- No forzar el stack de la empresa: Next.js solo si hay SEO, IA solo si aporta valor real (y decirlo explícitamente si no se usa).

## 8. Cierre

Responder al usuario con un resumen breve de qué quedó en cada sección, cómo se cubrieron las secciones exigidas por el documento fuente, qué corrigió la revisión final y qué quedó pendiente de decidir (supuestos de alcance, tiempos, roles), el link al documento y la ruta de `images/` con la cantidad de imágenes, para que pueda pasárselas al cliente.
