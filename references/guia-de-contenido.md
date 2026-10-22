# Guía de contenido

Plantilla de cada sección con la profundidad que el usuario aprobó. Los títulos se traducen al idioma pedido. Los ejemplos de texto son ilustrativos: el contenido real sale de los documentos fuente.

## Secciones exigidas por el documento fuente

Antes de definir la estructura, revisar si el documento fuente (pliego, RFP, brief, términos de referencia) **pide secciones o contenidos explícitamente**. Suelen aparecer como "la propuesta debe incluir", "contenido de la oferta", "qué tiene que traer la propuesta", "anexo técnico", "formulario de propuesta" o una tabla de puntos que se evalúan.

Con esa lista armar la estructura así:

1. **Sección exigida que equivale a una por defecto**: usar la por defecto con el **nombre exacto que usa el documento fuente**, en su orden si lo fija. Por ejemplo, "Metodología y plan de trabajo" reemplaza a Estimación por Sprints, "Equipo propuesto" a Composición del Equipo, "Arquitectura de la solución" a Propuesta de Infraestructura.
2. **Sección exigida sin equivalente**: agregarla como H2 propio en la posición que pida el documento o donde mejor encaje. Por ejemplo cronograma por fase, distribución de horas por fase, enfoque de calidad, evidencias de pruebas, plan de transferencia, experiencia o antecedentes, o qué se necesita del cliente para arrancar.
3. **Contenido exigido dentro de una sección**: incluirlo en la sección que corresponda y nombrarlo con las mismas palabras, para que el evaluador lo encuentre.
4. **Sección por defecto que el documento fuente no pide**: se mantiene, salvo que contradiga el formato exigido.

Registrar la correspondencia (sección exigida → sección del documento) en las notas de trabajo y repasarla en la revisión final: cada punto exigido tiene que estar cubierto.

## Orden por defecto de las secciones

1. Descripción General
2. Descripción de la Plataforma
3. MVP y NO MVP
4. Composición del Equipo y Responsabilidades por Rol
5. Propuesta de Infraestructura
6. Estimación por Sprints

Las secciones exigidas por el documento fuente se suman o reemplazan según el apartado anterior. Si el documento pide experiencia o antecedentes, va antes del equipo. Si pide riesgos y supuestos como sección propia, va al final y absorbe el H3 de riesgos de la infraestructura y el párrafo de supuestos de la estimación, para no repetirlos.

## Descripción General (sin H3)

Cuatro párrafos y dos figuras:

1. Qué es la plataforma, para quién y qué problema resuelve. Primera mención del nombre en negrita.
2. Cómo se organiza la solución. Si hay modalidades o productos distintos, nombrarlos en negrita y decir explícitamente si en la práctica son productos separados.
3. Alcance: qué incluye la plataforma completa y por qué la propuesta se concentra en una **primera versión acotada**. En la modalidad A, mencionar el **discovery inicial de dos semanas**. En la B, mencionar la duración en sprints.
4. Valor para el negocio y para el usuario operativo, con hechos concretos.

Figura 1 (visión general) después del párrafo 1. Figura 2 (estados o flujo principal) al final.

## Descripción de la Plataforma

Solo lo funcional del MVP, sin tecnologías en el texto. Un párrafo de apertura (superficies del producto, unidad de trabajo principal, redes o integraciones iniciales) seguido de la figura de módulos de la plataforma, y luego unos 5 H3, por ejemplo:

- Operación y control: ítems con etiqueta en negrita (organizaciones y roles, credenciales, entidades principales, carga de datos, políticas).
- Ejecución del flujo principal: 2 párrafos y la figura del flujo, más una línea sobre evidencia y entorno de pruebas.
- Interfaces: pantallas principales como lista sin etiquetas y un párrafo para la app o superficie secundaria. Si hay mockups, 2 a 4 pantallas clave como figuras (por ejemplo tablero, flujo principal y back-office); el set completo queda en `images/`.
- Modalidad diferencial (si existe): un párrafo y su figura.

Lo que queda fuera del MVP no va en esta sección: va en "MVP y NO MVP".

## MVP y NO MVP

Sección propia, después de Descripción de la Plataforma. Deja explícito qué se entrega y qué no, que es lo que más discusiones evita con el cliente y lo que el evaluador busca primero.

- Párrafo de apertura: qué es el MVP (la versión mínima que cumple los objetivos o entregables del documento fuente en el plazo propuesto) y qué pasa con lo que queda afuera (fases posteriores u hoja de ruta). Si hay componentes condicionales, decir cómo impactan en el plan: por ejemplo, que entran en las horas solo si reemplazan alcance equivalente y si no se acuerdan como ajuste de alcance. Sin esa frase, el cliente puede exigir lo condicional sin costo.
- **H3 "Incluido en el MVP"**: 6 a 8 viñetas con etiqueta en negrita, una por bloque funcional o entregable (por ejemplo flujos principales, consola o paneles, integraciones, entregables documentales, infraestructura). Cada una dice qué se entrega, no cómo se construye.
- **Etiqueta "Solo si el caso o el alcance validado lo requiere"** (opcional): viñetas cortas con los componentes condicionales (integraciones opcionales, colas para cargas masivas, conexiones dedicadas, tratamiento de datos personales). Tienen que coincidir con lo que la infraestructura y las figuras marcan como opcional.
- **H3 "Fuera del MVP"**: 5 a 8 viñetas cortas sin etiqueta (producción si no se pide, integraciones en línea, más casos o módulos, migraciones, soporte posterior, funcionalidades de fases futuras).

Lo que esta sección declara tiene que coincidir con los sprints o fases de la estimación y con lo que dicen la Descripción General y la infraestructura.

## Composición del Equipo y Responsabilidades por Rol (sin H3)

- Párrafo de apertura: cuántos **Senior Fullstack** (según el alcance o lo que pida el usuario), con qué orientaciones, QA y PM a tiempo parcial, y quién actúa como referente técnico.
- Cada rol como etiqueta (`lbl`): "**Senior Fullstack Engineer, orientación X** (tiempo completo)" seguida de 4 o 5 viñetas cortas de responsabilidades.
- Roles habituales: Senior Fullstack orientado a Blockchain (o al dominio técnico crítico del proyecto, por ejemplo IA o integraciones), Senior Fullstack orientado a Backend e integraciones (incluye AWS y pipelines), Senior Fullstack orientado a Frontend y producto, QA Engineer (tiempo parcial), Project Manager (tiempo parcial). Con dos desarrolladores, combinar orientaciones en lugar de dejar un área sin responsable.
- No usar Tech Lead, Arquitecto ni UX/UI como roles separados salvo que el usuario lo pida.
- Cierre (solo en la modalidad A): quiénes participan del discovery.

## Propuesta de Infraestructura

Párrafo de apertura con la arquitectura general (por ejemplo monolito modular en NestJS sobre AWS y procesamiento asíncrono) y la figura de arquitectura: sobre AWS, el diagrama de infraestructura AWS. Si el alcance técnico depende de algo que se define en el discovery o el primer sprint (por ejemplo el caso de uso), aclarar en este párrafo que las tecnologías son la propuesta de partida y cuáles podrían sumarse según lo que se valide. Luego estos H3:

1. **Backend, datos e integraciones**: párrafo sobre módulos por dominio y eventos, y viñetas con etiqueta: base de datos y aislamiento multi tenant, idempotencia, consistencia con colas (patrón outbox), API y webhooks, adaptadores por proveedor.
2. **Un H3 por el núcleo técnico del dominio** (por ejemplo despacho multicadena, motor de pagos, procesamiento de documentos): párrafo con la decisión central y 4 viñetas por tecnología o mecanismo.
3. **H3 de seguridad crítica del dominio** si aplica (por ejemplo firma y gestión de llaves).
4. **Seguridad, entornos y calidad**: accesos, infraestructura, evidencia o auditoría, entornos en cuentas separadas con CDK y Bitbucket Pipelines, estrategia de pruebas. Cerrar con una línea sobre IA (si se usa o por qué no).
5. **Decisiones de arquitectura**: 4 o 5 viñetas con el formato "**X en lugar de Y:** motivo concreto". Es lo que más demuestra criterio.
6. **Riesgos técnicos y mitigación**: 4 o 5 viñetas "**Riesgo:** mitigación".
7. **Decisiones a validar en el discovery** (modalidad A) o **Decisiones a validar en el primer sprint** (modalidad B): 3 viñetas.

Preferencias de stack de SpaceDev (usar solo si aportan): React con Vite para paneles internos, Next.js solo con SEO, NestJS, PostgreSQL con TypeORM, AWS (ECS Fargate y SQS cuando hay servicios con escalado o aislamiento distinto; Elastic Beanstalk y Amplify para casos simples), CDK, Bitbucket Pipelines, Cognito. Justificar cada elección frente a la alternativa.

## Estimación por Sprints

Usar la modalidad que eligió el usuario. Los sprints son siempre de dos semanas. Ser realista: si el usuario dice que el plazo es corto para el alcance, agregar sprints en lugar de recortar calidad. Si hay productos distintos (por ejemplo custodia y no custodia), cada uno lleva sus propias fases o sprints.

### Modalidad A: Discovery más fases

- Párrafo de apertura: discovery de dos semanas y N fases en sprints de dos semanas. Aviso en negrita: **se ajustará con los resultados del discovery**.
- Un H3 por etapa: "Discovery (2 semanas)" y "Fase N: Nombre (Sprints a a b)".
- El **discovery va detallado** (ver "Detalle del discovery o del primer sprint" más abajo): un párrafo de enfoque, entre 12 y 16 viñetas de actividades concretas y la línea "**Entregables:**".
- Cada fase lleva un párrafo con el alcance técnico concreto (componentes, no generalidades) y cierra con "**Hito técnico:**", un resultado verificable (por ejemplo "un lote de 500 pagos se despacha en redes de prueba con fallas inyectadas, sin duplicados").
- Cierre con la etiqueta "**Duración estimada**" y tres viñetas: Discovery, Desarrollo del MVP con la cantidad de sprints, y Total en semanas y meses aproximados. Después, un párrafo de supuestos con la estimación de la plataforma completa.
- Referencia aprobada: discovery de 2 semanas más 12 sprints (unos 6 meses) para un MVP con dos modalidades de operación y 3 desarrolladores.

### Modalidad B: Sprints directos

- Párrafo de apertura: "Para el alcance definido del MVP se propone una ejecución de N sprints de dos semanas, equivalente a aproximadamente X semanas de desarrollo".
- Segundo párrafo: en qué flujos se concentra el plan y qué supuestos lo sostienen (proveedores externos, piezas que quedan fuera del MVP).
- Un H3 por sprint: "Sprint N: Nombre". Dentro de cada uno:
  - "**Objetivo:** …" en una línea.
  - "**Principales actividades:**" seguida de 6 a 9 viñetas concretas. El primer sprint incluye la base técnica (repositorios, CI/CD, entornos, autenticación) y la validación de proveedores.
  - Opcionalmente, un párrafo corto de contexto cuando una decisión del sprint lo necesite.
  - "**Resultado:** …" con lo que el usuario o el sistema puede hacer al cerrar el sprint.
- El último sprint es de QA, estabilización y producción: pruebas de punta a punta, regresión, idempotencia y concurrencia, seguridad, monitoreo, documentación operativa y despliegue.
- Cierre con la etiqueta "**Duración estimada**", la línea "La duración estimada es de N sprints / X semanas." y un párrafo de supuestos: alcance controlado, credenciales de proveedores disponibles a tiempo y decisiones oportunas del cliente.
- Con muchos sprints el índice crece. Si pasan de 8, compensar con menos H3 en otras secciones.
- El **Sprint 1** absorbe la alineación técnica que en la modalidad A haría el discovery, con el mismo nivel de detalle (ver la sección siguiente).

### Detalle del discovery o del primer sprint

Es la parte que más demuestra que el equipo sabe qué va a construir. Abrir con una línea de enfoque ("se enfoca en validar el alcance, cerrar las decisiones técnicas críticas y dejar preparada la base técnica") y listar actividades concretas, nombrando los artefactos, componentes y proveedores del proyecto. No usar generalidades como "talleres de requerimientos" sin decir sobre qué. Cubrir estos grupos, adaptados al dominio:

1. **Alcance y negocio**: talleres para priorizar los flujos del MVP, confirmar el primer cliente, el volumen y las integraciones. Revisión de componentes o código existentes del cliente.
2. **Dominio**: definir el ciclo de vida de la entidad principal (estados, transiciones, reglas). Definir el alcance de cada modalidad o producto y sus condiciones regulatorias.
3. **Decisiones técnicas críticas**: la estrategia del componente más riesgoso (por ejemplo firma y llaves) con sus alternativas, y los modelos asociados (llaves, comisiones, gas).
4. **Proveedores**: evaluación con pruebas reales sobre sus APIs (análisis de cadena, nodos, tesorería, KYC, según el caso).
5. **Contratos e integración**: contrato OpenAPI, webhooks, formatos de archivo y correlación con los identificadores externos (hash, nonce, transactionId).
6. **Datos**: modelo de datos inicial e idempotencia.
7. **Base técnica**: inicializar el proyecto con su estructura de módulos, la arquitectura de despliegue en AWS, la separación de cuentas y entornos, la estructura de infraestructura como código y el esqueleto de CI/CD.
8. **Operación y calidad**: estrategia de logs, métricas y alertas, y estrategia de pruebas (cumplimiento del contrato, autenticación, idempotencia, firmas, fallas inyectadas).
9. **Producto**: wireframes de las pantallas principales.

Cerrar con "**Entregables:**" (modalidad A) o "**Resultado:**" (modalidad B): documento de arquitectura con sus decisiones, contrato OpenAPI inicial, modelo de datos, repositorio base con IaC y pipeline, plan de pruebas, backlog priorizado y cronograma definitivo.

## Figuras

- Tipos, plantillas, carpeta `images/`, legibilidad y proceso con subagentes: `imagenes.md`.
- Ubicación: visión general y plan de fases en Descripción General; módulos, flujos del dominio y pantallas en Descripción de la Plataforma; diagrama de infraestructura (con la visual e íconos de AWS cuando es sobre AWS) en Propuesta de Infraestructura.
- Diagramas de flujo: violeta #433273 para destacar, gris #273239 para texto, verde, ámbar y rojo solo para estados. Solo nombres de componentes, grupos con título en mayúsculas espaciadas y flechas ortogonales.
- Epígrafes: "Figura N. Descripción breve".
