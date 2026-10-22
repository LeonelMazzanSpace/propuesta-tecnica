# Revisión final con subagentes

Cuando el documento está escrito y las figuras insertadas, se revisa todo con revisores independientes: **un subagente por imagen** (las del documento y las que solo van en la carpeta de entrega) y **un subagente para el documento completo**. Un revisor que no armó la figura encuentra lo que el autor ya no ve: cifras que no cierran entre pantallas, diagramas que contradicen el texto, servicios de AWS mal ubicados, letra que en la página queda en 3 pt.

Los revisores **solo leen y reportan**: no modifican archivos. El agente principal consolida, decide y corrige.

## 1. Preparar los insumos

En el scratchpad:

- **Texto de la propuesta** en texto plano, generado desde `bloques.json` (que coincide con el Doc verificado):

```bash
python3 -I -c '
import json,sys
b=json.load(open(sys.argv[1])); out=[]
for t,*r in b:
    v=r[0] if r else ""
    if not isinstance(v,str): v=json.dumps(v,ensure_ascii=False)
    out.append({"h2":"\n## ","h3":"\n### "}.get(t,"")+("- " if t=="b" else "")+v.replace("**",""))
open(sys.argv[2],"w").write("\n".join(out))' bloques.json propuesta.txt
```

- **Texto del documento fuente** (`pdftotext -layout` del pliego, brief o RFP).
- **`prompt-revision-imagen.md`** con las instrucciones comunes de abajo, adaptadas al proyecto: decisiones técnicas vigentes, plan (fases, semanas, sprints), roles y el caso de ejemplo de las pantallas.

## 2. Instrucciones comunes para revisar una imagen

```markdown
# Revisión de una imagen de la propuesta <proyecto> (solo lectura)

No modifiques ningún archivo. Solo leé y reportá.

Insumos: texto de la propuesta <ruta propuesta.txt>, documento fuente <ruta>, plan de imágenes
<ruta images/IMAGENES.md>, y el PNG y el HTML que se indican abajo. Mirá el PNG con Read
(achicado si es grande) y recortes a resolución completa para leer el texto chico. Usá el HTML
para confirmar textos exactos.

Qué revisar:
1. Sentido: ¿comunica lo que dice su epígrafe y el párrafo que la rodea? ¿Las flechas tienen una lectura lógica?
2. Coherencia con el texto: cada componente, nombre, cifra, fase, rol o servicio coincide con la
   propuesta. Señalá lo que está en la imagen y no en el texto, lo que lo contradice y lo
   importante del texto que falta. Decisiones vigentes: <lista>.
3. Coherencia con el documento fuente: fases, entregables y restricciones.
4. Datos de ejemplo (pantallas): verosímiles y consistentes con las otras pantallas (IDs, fechas,
   conteos que suman, porcentajes, roles y avatares, versiones). Sin normas ni entidades reales comprometedoras.
5. Corrección técnica (infraestructura): subredes, zonas, salida de red, endpoints, servicios
   regionales, qué es opcional.
6. Legibilidad: la imagen se inserta a 468 pt. pt efectivos = px ÷ render-width × 468. Marcá todo
   texto por debajo del mínimo de references/imagenes.md, superposiciones, textos cortados,
   flechas que cruzan textos o bordes.
7. Redacción: idioma del documento, tildes, mayúsculas consistentes, sin "—", sin inglés evitable.

Formato (máx. ~350 palabras): Veredicto (OK / Ajustes menores / Requiere cambios); hallazgos
numerados con severidad (Alta/Media/Baja), cita exacta de lo que se ve, por qué es un problema y
el cambio concreto (texto exacto a poner); tamaño mínimo efectivo en pt. No inventes problemas.
```

Prompt de cada subagente: "Leé primero `<scratchpad>/prompt-revision-imagen.md` y seguilo. Imagen: Figura N, "<epígrafe>" (sección). PNG: … HTML: …", más el foco específico de esa figura (por ejemplo, para la de infraestructura: comparar servicio por servicio con las subsecciones del texto; para una pantalla: comparar con las demás pantallas). Las imágenes que solo van a la carpeta de entrega se revisan a tamaño real, no a 468 pt.

## 3. Revisión del documento completo

```markdown
Sos revisor senior de una propuesta técnica de SpaceDev para <cliente>. No modifiques archivos.
Insumos: <propuesta.txt> ("## " = H2, "### " = H3, "- " = viñeta), <documento fuente>, <IMAGENES.md>.

1. Cobertura del documento fuente: plazos, horas, fases con todos sus entregables, cronograma y
   distribución de horas por fase, secciones exigidas explícitamente, qué se necesita del cliente
   para arrancar, condiciones legales o contractuales (confidencialidad, propiedad intelectual,
   protección de datos). Marcá lo que falte.
2. Coherencia interna: decisiones vigentes = <lista>. Buscá restos de decisiones anteriores, cifras
   que no cierren (horas por fase y por rol, semanas), sprints contra fases, roles contra
   responsabilidades, MVP contra sprints y alcance, contradicciones entre secciones.
3. Redundancias entre secciones que convenga recortar.
4. Estructura: H2 y H3 (15 a 18 H3) y orden lógico.
5. Redacción según las reglas de la casa: sin "—", sin ";" ni "-" como recurso, sin relleno, tildes,
   mayúsculas de títulos consistentes, frases demasiado largas.
6. Riesgo comercial: promesas que no se sostienen en el plazo o las horas, afirmaciones técnicas
   exageradas, componentes condicionales sin decir si entran en las horas.

Formato (máx. ~500 palabras): veredicto general y hallazgos numerados por severidad, cada uno con
la cita exacta, el problema y el texto de reemplazo concreto. No inventes problemas.
```

## 4. Lanzar, consolidar y corregir

1. Lanzar todos los revisores **en un solo mensaje** (en paralelo). Mientras trabajan, el agente principal exporta el PDF y arma la hoja de miniaturas para revisar la paginación.
2. Al llegar cada informe, verificar en el PNG o en el texto los hallazgos de severidad alta antes de aceptarlos. Los revisores a veces se equivocan.
3. Consolidar para el usuario, sin repetir cada informe:
   - **Para corregir**: contradicciones con el texto o el documento fuente, errores técnicos y riesgos comerciales, en una tabla con dónde, problema y corrección.
   - **Legibilidad**: tamaño mínimo por figura.
   - **Menores**: una línea por figura o sección.
   - **Pendiente de decidir**: lo que es decisión del usuario (equipo, horas, alcance).
4. Si el usuario pidió "revisá y corregí", aplicar directamente. Si solo pidió revisar, presentar el consolidado y preguntar qué aplicar.
5. Al aplicar, agrupar las correcciones de imágenes en lotes por tipo para subagentes, con las instrucciones exactas de cada hallazgo. Corregir el texto en paralelo:
   - cambios dentro de un párrafo con `replaceAllText` (con `matchCase`, y cada texto viejo único y dentro de un mismo estilo);
   - secciones nuevas o reordenadas con `build_blocks.py` por tramo;
   - mantener `bloques.json` sincronizado.
6. Reemplazar en el Doc solo las figuras que cambiaron (`insercion-de-imagenes.md`), verificar con `verify_doc.py` y revisar la hoja de miniaturas del PDF: ninguna página con una sola viñeta, ningún título huérfano.
