# Create the FUGA+ User Story Diagram in Draw.io

Create the UML-style User Story Diagram for the FUGA+ mobile application.

---

## IMPORTANT — PHYSICAL FILE CREATION

You MUST physically create the Draw.io file in the project filesystem.

The exact file that MUST be created is:

`docs/diagramas/diagrama-historias-usuario.drawio`

This is the ONLY file that this task is allowed to create or modify.

DO NOT:

- Only display XML in the chat.
- Only explain the diagram.
- Generate XML without saving it.
- Create the diagram only in memory.
- Create a Markdown diagram.
- Create a Mermaid file.
- Create an SVG.
- Create a PNG.
- Create an HTML file.
- Create another Draw.io file.
- Create another folder.
- Save the file somewhere else.

The final result MUST be a real `.drawio` file containing a complete visible diagram.

When the file is opened with diagrams.net / Draw.io, the diagram must be visually displayed.

---

# PROJECT

FUGA+ is a mobile application that helps users identify possible "money leaks" caused by small and repetitive expenses.

The diagram represents the current functional requirements and the corrected Release 1 user stories.

---

# VISIBLE LANGUAGE

ALL visible text inside the diagram MUST be in Spanish.

Do not use English labels inside the diagram.

Use the exact actor names and user story names specified below.

---

# DIAGRAM HEADER

Title:

**Diagrama de Historias de Usuario — FUGA+**

Subtitle:

**Funcionalidades principales de la aplicación móvil**

Place the title and subtitle clearly at the top of the diagram.

---

# ACTORS

The diagram MUST contain exactly these three actors:

- **Visitante**
- **Usuario**
- **Administrador**

Use UML-style actor symbols or clean actor boxes.

---

# USER STORIES

The diagram MUST contain exactly these 14 user stories.

Do not omit any.

Do not add additional user stories.

---

## MUST — OBLIGATORIO

### HU-01 — Conocer FUGA+

Actor:

Visitante

Description:

Consulta información pública sobre FUGA+ y puede acceder a las opciones de registro e inicio de sesión.

---

### HU-02 — Registrarse e iniciar sesión

Actor:

Visitante

Description:

Crea una cuenta como Usuario e inicia sesión con correo y contraseña.

---

### HU-03 — Registrar gasto en lenguaje natural

Actor:

Usuario

Description:

Escribe un gasto en español mediante una frase libre y envía el texto para su interpretación.

---

### HU-04 — Interpretar gasto con IA

Actor:

Usuario

Description:

La IA identifica monto, categoría y descripción, muestra los datos para revisión y permite corregirlos antes de confirmar.

---

### HU-05 — Consultar historial de gastos

Actor:

Usuario

Description:

Consulta sus gastos confirmados ordenados del más reciente al más antiguo y puede ver el detalle.

---

### HU-06 — Consultar dashboard personal

Actor:

Usuario

Description:

Consulta total del periodo actual, cantidad de gastos, promedio, acumulado por categoría y categoría de mayor peso.

---

### HU-07 — Detectar posibles fugas de dinero

Actor:

Usuario

Description:

Consulta posibles fugas identificadas mediante reglas determinísticas de gastos pequeños y repetitivos.

---

# SHOULD — IMPORTANTE

### HU-08 — Filtrar historial

Actor:

Usuario

Description:

Filtra sus gastos por rango de fechas y categoría y puede limpiar los filtros.

---

### HU-09 — Corregir categoría de un gasto

Actor:

Usuario

Description:

Corrige la categoría antes de confirmar o después de guardar el gasto; el cambio se refleja en historial, dashboard y análisis de fugas.

---

### HU-10 — Consultar estadísticas generales

Actor:

Administrador

Description:

Consulta estadísticas agregadas de usuarios y gastos sin acceder a datos financieros individuales.

---

### HU-11 — Gestionar usuarios

Actor:

Administrador

Description:

Consulta el estado de las cuentas y puede activar o desactivar usuarios; una cuenta desactivada no puede iniciar sesión.

---

# COULD — OPCIONAL

### HU-12 — Recibir alertas de posibles fugas

Actor:

Usuario

Description:

Recibe una alerta dentro de la aplicación cuando se detecta una nueva posible fuga.

---

### HU-13 — Registrar gasto por voz

Actor:

Usuario

Description:

Registra un gasto mediante voz, convirtiendo la voz a texto y reutilizando el flujo de interpretación.

---

### HU-14 — Comparar periodos

Actor:

Usuario

Description:

Compara dos periodos mediante total, cantidad, promedio y variaciones.

---

# ACTOR-STORY RELATIONSHIPS

Create visible connectors between every actor and the user stories that actor can perform.

Use simple UML-style association lines.

---

## VISITANTE

Connect:

Visitante → HU-01

Visitante → HU-02

Do NOT connect Visitante to any other story.

---

## USUARIO

Connect:

Usuario → HU-03

Usuario → HU-04

Usuario → HU-05

Usuario → HU-06

Usuario → HU-07

Usuario → HU-08

Usuario → HU-09

Usuario → HU-12

Usuario → HU-13

Usuario → HU-14

Do NOT connect Usuario to HU-01, HU-02, HU-10 or HU-11.

---

## ADMINISTRADOR

Connect:

Administrador → HU-10

Administrador → HU-11

Do NOT connect Administrador to any other story.

---

# MOSCOW PRIORITY GROUPING

The diagram MUST visually separate the user stories into three priority groups.

---

## MUST — OBLIGATORIO

This group contains:

- HU-01
- HU-02
- HU-03
- HU-04
- HU-05
- HU-06
- HU-07

---

## SHOULD — IMPORTANTE

This group contains:

- HU-08
- HU-09
- HU-10
- HU-11

---

## COULD — OPCIONAL

This group contains:

- HU-12
- HU-13
- HU-14

---

Use large containers, section headers, or clearly separated areas.

The three priority groups must be visually obvious.

Do not use:

- rankings
- scores
- winner labels
- "best"
- "worst"

---

# FUNCTIONAL AREAS

Organize the diagram so that the user stories are easy to understand.

Use these functional areas:

1. **Autenticación y acceso**
2. **Gestión de gastos**
3. **Análisis financiero**
4. **Administración**
5. **Funcionalidades opcionales**

These functional areas should help organize the stories while maintaining the three MoSCoW priority groups.

---

# DRAW.IO DESIGN

Create a professional academic UML-style diagram.

Use:

- A clear title at the top.
- A subtitle below the title.
- UML-style actors.
- Rounded rectangles for user stories.
- Association connectors between actors and stories.
- Clearly separated MoSCoW containers.
- Consistent typography.
- Good spacing.
- Readable text.
- Clean alignment.
- No overlapping elements.
- No unnecessary connector crossings.

All 14 stories must be visible at the same time when the diagram is opened.

Do not make the story text so small that it becomes unreadable.

---

# LEGEND

Add a visible legend.

Title:

**Leyenda**

Include:

**Must = Obligatorio**

**Should = Importante**

**Could = Opcional**

The legend must be inside the diagram.

---

# WON'T REQUIREMENTS

Do NOT include any of these as user stories:

- Conexión con bancos
- Pagos o transferencias
- Tarjetas
- Líneas de crédito
- Préstamos
- Inversiones
- Asesoría financiera profesional
- Entrenamiento de un modelo de IA propio
- Predicción de mercados
- Datos bancarios reales de terceros
- Notificaciones push avanzadas
- Escaneo avanzado de recibos
- Integraciones bancarias externas
- Funciones administrativas avanzadas
- Múltiples niveles de administrador

None of these may appear as user-story boxes.

---

# TECHNICAL DRAW.IO REQUIREMENTS

The file MUST be a valid Draw.io XML document.

The root must be compatible with diagrams.net / Draw.io.

Use:

- `mxfile`
- `diagram`
- `mxGraphModel`
- `mxCell`
- `mxGeometry`

Every visual element must be represented by valid `mxCell` elements.

Every connector must have valid:

- `source`
- `target`

IDs.

All cell IDs must be unique.

Do not create duplicate IDs.

Do not create broken references.

The XML must be well formed.

---

# REQUIRED DIAGRAM ELEMENTS

The final `.drawio` file MUST contain actual visual elements for:

1. Title
2. Subtitle
3. Visitante actor
4. Usuario actor
5. Administrador actor
6. HU-01
7. HU-02
8. HU-03
9. HU-04
10. HU-05
11. HU-06
12. HU-07
13. HU-08
14. HU-09
15. HU-10
16. HU-11
17. HU-12
18. HU-13
19. HU-14
20. Actor-story connectors
21. MUST container
22. SHOULD container
23. COULD container
24. Legend

---

# IMPORTANT — DO NOT CREATE AN EMPTY DIAGRAM

The file MUST NOT contain an empty `mxGraphModel`.

For example, this is NOT acceptable:

```xml
<mxGraphModel>
</mxGraphModel>