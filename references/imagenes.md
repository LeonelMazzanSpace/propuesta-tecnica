# Imágenes de la propuesta

Todas las figuras se arman como archivos propios, con crudo editable y PNG final, para insertarlas en el documento y entregarlas al cliente.

## Carpeta de entrega

Se crea en el directorio donde se ejecuta la skill:

```
images/
  IMAGENES.md   plan y checklist, fuente de verdad de las imágenes
  htmls/        crudos editables, uno por imagen (y htmls/assets/ si hay logos o fotos)
  pngs/         finales, 1:1 con htmls (mismo nombre base). Son los que se insertan y se entregan
```

| Tipo | Archivo | Cómo se hace |
|---|---|---|
| Visión general, plan de fases, flujos | `diagrama-<slug>` | `scripts/diagram_kit.py`, `d.save("diagrama-<slug>")` |
| Módulos de la plataforma | `plataforma-modulos` | copiar `assets/plataforma-modulos.html` |
| Infraestructura en AWS | `infraestructura-aws` | copiar `assets/infraestructura-aws.html` |
| Infraestructura en otra nube | `infraestructura-<slug>` | `diagram_kit.py` |
| Pantallas | `pantalla-NN-<slug>` | copiar `assets/pantalla-base.html` |

Render de los HTML: `python3 -I <skill>/scripts/render_html.py [nombres]` (sin nombres, todos). Genera PNG a 2x. Para mirarlos con Read hay que achicarlos antes (`magick images/pngs/x.png -resize 1600x <scratchpad>/x.jpg`), porque el PNG supera el límite de lectura.

## Qué imagen va en cada sección

| Sección | Figuras | Herramienta |
|---|---|---|
| Descripción General | Visión general (fuentes → plataforma → usuarios, con lo transversal como barras) y plan de fases o sprints con sus entregables | `diagram_kit` |
| Descripción de la Plataforma | Módulos de la plataforma (primera figura de la sección), flujos del dominio (selección, flujo principal, estados) y 2 a 4 pantallas clave. El set completo de pantallas queda en `images/` | plantilla de módulos, `diagram_kit`, plantilla de pantallas |
| Propuesta de Infraestructura | Diagrama de infraestructura. Sobre AWS, con la visual de AWS: contenedores AWS Cloud, región, VPC, zonas y subredes con sus colores, e íconos de servicio con el color de su categoría | plantilla AWS, o `diagram_kit` en otra nube |

Las pantallas solo se hacen si el producto tiene interfaz (web, app o back-office). La visión general y el plan de fases se hacen siempre. Los flujos, según `guia-de-contenido.md`.

## Legibilidad: la regla que manda

Las imágenes se insertan a **468 pt de ancho** (ancho de página). El tamaño con que se lee un texto en el documento es:

```
pt efectivos = px del texto en el HTML ÷ render-width × 468
```

| Tipo | render-width | Mínimo de cualquier texto | Nombres de cajas y servicios |
|---|---|---|---|
| Diagramas de `diagram_kit` | 1800 | 26 px → 6,8 pt | 30 px → 7,8 pt |
| Módulos de la plataforma | ~1060 | 15 px → 6,6 pt | 18 px → 7,9 pt |
| Infraestructura AWS | ~1000 | 14 px → 6,5 pt | 16,5 px → 7,7 pt |
| Pantallas (solo escritorio) | 1064 (artboard 1040) | 14 px → 6,2 pt | cuerpo 15 px → 6,6 pt |

- Las plantillas de `assets/` ya vienen con estos anchos y tamaños. Al adaptarlas, no bajar ningún texto de su mínimo. Las siglas dentro de los íconos de AWS son la única excepción (12 px en negrita, unos 5,6 pt), porque se leen como ícono.
- Cuando algo no entra, **se quita contenido, no se achica la letra**: subtítulos, paneles, descripciones, filas de tabla, columnas secundarias. La figura ilustra; el detalle está en el texto.
- Proporciones: diagramas de flujo de 1800 × 420 a 900; módulos y AWS con alto/ancho ≤ 1,4 para que entren en una página con su epígrafe; pantallas con alto/ancho ≤ 1,05.
- Cada subagente reporta el tamaño mínimo efectivo de cada imagen que entrega.

## Proceso: plan, base, lotes con subagentes, revisión

Las imágenes se hacen **después de redactar los bloques del documento**, para que dibujen exactamente lo que dice el texto. Es más eficiente con subagentes en paralelo: el agente principal define el plan y las reglas comunes, y cada subagente arma su lote.

1. **Plan (agente principal)**. Escribir `images/IMAGENES.md` con una fila por imagen: archivo, figura (`F3`) o `entrega` si no va al documento, qué muestra (componentes con los nombres exactos del texto, o los elementos de la pantalla) y fuente (documento y página).
2. **Especificación común (agente principal)**. Un archivo en el scratchpad que todos los subagentes leen primero, con:
   - las decisiones técnicas vigentes del texto (stack, servicios, qué es opcional, número de zonas, qué no se usa);
   - los roles y sus permisos;
   - el plan (fases, semanas, sprints, entregables con el nombre del pliego);
   - para las pantallas, una **tabla de datos canónicos** (identificadores, fechas, versiones, conteos que cierran entre sí, nombres y avatares por rol) que todas las pantallas usan igual;
   - los mínimos de legibilidad de este archivo y las reglas de redacción.
3. **Base (agente principal)**.
   - Pantallas: definir el sistema visual en los tokens de `:root` (manual de marca del cliente si existe, si no el neutro de la plantilla) y construir la pantalla de referencia, normalmente el tablero, ya con la escala tipográfica de la tabla de legibilidad. Renderizarla, **mostrarle el PNG al usuario y esperar su aprobación** antes de lanzar los lotes.
   - Diagramas HTML: copiar las plantillas a `images/htmls/` con su nombre final.
4. **Lotes en paralelo**. Un solo mensaje con varias llamadas a Agent (`general-purpose`), una por lote, como máximo 6 a la vez. Lotes habituales: flujos de `diagram_kit`; módulos e infraestructura; pantallas (todas en un mismo lote, o con un generador común, para que el CSS y los datos queden idénticos). Prompt de cada subagente:

```
Leé primero <scratchpad>/spec-imagenes.md y <skill>/references/imagenes.md (secciones "Legibilidad" y "<tipo>").
Armá estas imágenes de la propuesta de <proyecto> en <ruta>/images/htmls y renderizalas a images/pngs.
Imágenes asignadas: <filas completas de IMAGENES.md>
Contenido: <extracto del texto redactado de la sección> y fuentes <rutas y páginas>.
Idioma: <idioma>. Estilo: <pantalla de referencia o plantilla>.
Render: python3 -I <skill>/scripts/render_html.py <nombres> (los diagram_kit generan su PNG con save()).
Mirá cada PNG (achicado y con recortes a resolución completa) y corregí hasta que pase la lista de revisión.
No toques IMAGENES.md ni archivos que no sean tuyos. Respondé solo con los archivos creados,
el tamaño mínimo efectivo en pt de cada imagen y las dudas de contenido.
```

5. **Revisión (agente principal)**. Mirar cada PNG con la lista de abajo y marcar la fila en `IMAGENES.md`. Las correcciones menores se hacen directamente; las grandes se le piden al mismo subagente con SendMessage.
6. **Inserción**. Solo las filas con figura, desde `images/pngs/`, en el orden de los marcadores (`insercion-de-imagenes.md`).
7. **Revisión final** del documento completo con un subagente por imagen: `revision-final.md`.

## Reglas por tipo

### Diagramas de flujo (`diagram_kit`)

- Solo nombres de componentes, idénticos a los del texto. Flechas ortogonales, buses compartidos.
- Cajas de varias líneas con una lista (`d.box(..., ["Zona de", "aterrizaje"])`) y rótulos de flecha con `d.label`. `save()` avisa con `WARN` si un texto no entra: corregir todos.
- Lo que el texto describe como transversal (registro de ejecución, linaje, auditoría) va como **barra** debajo de los pasos, conectada a todos, no como un paso más del flujo.
- Lo que el texto describe como parte de la plataforma (por ejemplo la consola) va **dentro** del grupo de la plataforma.
- Diferenciar lo que entrega el proyecto (estilo `accent`) de los marcos o insumos del cliente (estilo `plain`).
- Plan de fases: nombre completo de cada fase como en el pliego y qué sprints o semanas la cubren. Si un sprint se reparte entre dos fases, decirlo explícitamente ("Sprint 2 + 1ª semana del Sprint 3"). Entregables con el nombre del pliego.
- Zonas o estados con su nombre completo ("Zona de aterrizaje", no "Aterrizaje"). Verde, ámbar y rojo solo para estados, y con el mismo criterio en todas las cajas del mismo tipo.
- Si una fila no entra a 30 px, armar el diagrama en dos filas (forma de U) antes que achicar.

### Módulos de la plataforma

- Centro: el sistema con sus capas de ejecución. La **consola o interfaz** va arriba como capa de entrada (es donde llegan las flechas de los usuarios); debajo, la API, el módulo núcleo y la grilla de módulos de dominio; abajo, los workers.
- La grilla de módulos son **los módulos de dominio que nombra el texto del backend**, no pasos del flujo (la ingesta es un paso del worker) ni capacidades sueltas. En 2 columnas si en 3 no entran a 18 px.
- Izquierda: usuarios con sus roles. Derecha: sistemas del cliente (proveedor de identidad, fuentes de datos), con cajas alineadas (`data-align`) a lo que conectan. Abajo: almacenes, cada uno con lo que realmente guarda según el texto.
- Sin título interno: el epígrafe ya lo dice.

### Infraestructura AWS

**Visual**: mantener la de la plantilla, que es la de AWS: contenedores AWS Cloud, región, VPC, zona y subredes con sus colores (pública verde, privada azul), y cada servicio con su **ícono** (`<i>` con la sigla y el color de su categoría `data-c`). Para ganar espacio se quitan paneles y subtítulos, no los íconos.

**Simplificación** para cumplir la legibilidad:
- Sin título, subtítulo ni pie: el epígrafe ya lo dice.
- Leyenda y principios de seguridad solo si queda espacio. Sin leyenda, la línea punteada se reserva para lo **opcional**.
- Servicios de soporte (ECR, Secrets Manager, KMS, CloudWatch, CloudTrail) en **una sola franja** con sus íconos y una sola conexión a la VPC, sin punta de flecha, porque logs y auditoría salen de la VPC.
- Subtítulos de servicio de 2 a 4 palabras, solo si informan (por ejemplo "pgvector · cola de trabajos").
- Actores externos arriba y abajo si así se gana ancho.

**Corrección técnica** (un técnico del cliente lo nota):
- El **ALB y el grupo de subredes de RDS exigen subredes en al menos dos zonas de disponibilidad**, aunque la instancia sea Single-AZ. Si el texto propone "una zona", el rótulo dice "Cómputo y base en una zona · subredes en dos zonas", y el texto dice lo mismo.
- Las subredes privadas necesitan salida: **NAT Gateway** en la subred pública (con una flecha de salida a internet) o endpoints de interfaz para ECR, CloudWatch Logs y Secrets Manager. El texto tiene que nombrar el mecanismo elegido.
- **WAF asociado a un ALB es regional**: va dentro de la región, delante del ALB. Solo con CloudFront va en el perímetro global.
- Endpoints de VPC: S3 de tipo gateway; Bedrock, SQS y otros de tipo interfaz.
- Los servicios regionales fuera de la VPC (S3, Bedrock, SQS, Cognito) se conectan desde el contenedor de la subred cuando los usan varios servicios, en lugar de elegir uno.
- Lo opcional (VPN, colas para cargas masivas, tareas que solo se suman según el caso) con **borde punteado** y "(opcional)" en el nombre, y lo mismo en sus flechas.
- Solo los servicios que nombra el texto, con su nombre oficial, y todo lo que nombra el texto aparece. Se puede dibujar lo que un servicio nombrado exige técnicamente.

**Mecánica de la plantilla**:
- Contenedores que tapan una flecha con su título: título a la derecha con `<span class="t r">`. Una flecha puede apuntar a un contenedor si tiene id.
- Color por categoría con `data-c`: `net` (Route 53, ALB, NAT, API Gateway, CloudFront, VPN), `compute` (ECS, Lambda, ECR), `db` (RDS, DynamoDB, ElastiCache), `storage` (S3), `sec` (WAF, ACM, KMS, Secrets Manager, Cognito), `int` (SQS, SNS, EventBridge), `mgmt` (CloudWatch, CloudTrail), `ml` (Bedrock, SageMaker).
- Etiquetas de flecha de 1 a 4 palabras sobre qué viaja. Ninguna etiqueta cruza el borde de un contenedor: moverla o acortarla.
- Las flechas terminan en un componente, no en el borde de una subred, salvo que el destino sea toda la subred.

### Pantallas

- **Back-office: solo escritorio**, artboard de 1040 px y `render-width` 1064. Si hace falta mobile, va como imagen aparte.
- **Sin el lienzo de presentación** (barra de ruta, rótulo "Desktop · 1360"): no es parte de la interfaz y resta legibilidad. Una nota "Datos ilustrativos" al pie.
- Mismos tokens, CSS base y componentes en todas las pantallas. Con varias pantallas conviene un generador común (un script que arma los HTML desde partes) para que el CSS quede idéntico.
- Datos de la **tabla de datos canónicos** de la especificación: identificadores, fechas y horarios dentro del período del ejemplo, conteos que suman, porcentajes que se pueden recalcular, versiones iguales en todas las pantallas.
- Coherencia con el texto:
  - cada acción visible corresponde al rol del usuario de esa pantalla (un analista no ve "Ejecutar flujo" si eso es del administrador);
  - los estados y las severidades no se mezclan ("Fallida" es un estado, "Bloqueante" una severidad);
  - las reglas del dominio que define el texto se respetan en los datos (por ejemplo, qué va a cuarentena y qué no);
  - las métricas y dimensiones que nombra el texto aparecen, o una nota dice dónde están.
- No citar normas, números de artículo ni entidades reales que puedan leerse como afirmaciones del cliente. Respuestas de ejemplo prudentes y con aviso de revisión humana.
- Textos de la interfaz en el idioma del documento, sin "—" y sin palabras en inglés evitables.

### Al adaptar una plantilla HTML

- Cambiar `lang` y `<title>` y traducir todos los textos fijos al idioma del documento.
- Dos cajas conectadas en línea recta deben tener el centro alineado al píxel. Si no, la flecha dibuja un escalón. Conviene anclar con `"#id"` (por ejemplo `to:["api","top","#waf"]`) en vez de fracciones.
- Si un conector arranca en una coordenada suelta (`[x, y]`), esa x o y debe coincidir con el destino o hay que usar `via`.
- Para revisar detalles, recortar una zona del PNG a resolución completa (`magick x.png -crop 900x600+X+Y <scratchpad>/zona.jpg`) además de la vista achicada.

## Lista de revisión de cada PNG

- No aparece el aviso rojo de la esquina superior izquierda (`desborda #id`, `falta #id`) ni ningún `WARN` de `diagram_kit`.
- Tamaño mínimo efectivo calculado y dentro de la tabla de legibilidad.
- Textos dentro de sus cajas, sin cortes ni superposiciones. Las etiquetas de flecha no tapan títulos ni cruzan bordes.
- Flechas ortogonales que no atraviesan cajas. Los cruces se dibujan con un salto.
- Nombres idénticos a los del texto, en el idioma del documento, sin "—".
- Lo que muestra la figura coincide con el texto y con las otras figuras: nada que el texto no diga, nada importante del texto que falte, mismas cifras y nombres.
- Ninguna caja vacía ni texto de ejemplo de la plantilla.
