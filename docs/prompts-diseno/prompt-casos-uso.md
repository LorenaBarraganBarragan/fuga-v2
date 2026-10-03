Act as a senior software architect and UML specialist.

Your task is to create ONLY the UML Use Case Diagram for the FUGA+ project.

IMPORTANT: The folder already exists:

`docs/diagramas/`

DO NOT create another folder.

You MUST physically create the following file:

`docs/diagramas/diagrama-casos-uso.drawio`

Do NOT create any other file.

Do NOT just generate or display the Draw.io XML in the chat.

You must actually write the XML into the project filesystem using the available file-writing/editing capabilities.

After creating the file, verify that the file physically exists and is not empty.

---

# PROJECT CONTEXT

FUGA+ is a mobile application designed mainly for young people and students.

Its purpose is to help users identify possible "money leaks" based on their daily expenses.

Example:

"Hoy gasté $8.000 en un taxi"

The application interprets the expense text and obtains:

* Valor
* Categoría
* Descripción

The expense is then stored and can be consulted through the history and dashboard.

The system can also identify possible money leaks using predefined rules based on repetitive expenses.

IMPORTANT:

Money-leak detection is NOT an AI decision.

It is based on predefined system rules.

---

# DIAGRAM LANGUAGE

All visible text inside the diagram MUST be in Spanish.

The instructions in this prompt are in English, but the actual diagram content must be Spanish.

Use these exact Spanish actor names:

* Visitante
* Usuario
* Administrador

Use this exact system boundary name:

`Sistema FUGA+`

Use Spanish names for all use cases.

---

# ACTORS

The diagram must contain exactly these three system actors:

## 1. Visitante

The visitor is an unauthenticated person who can access public information.

The visitor can:

* Ver información de FUGA+
* Ver cómo funciona
* Registrarse
* Iniciar sesión

IMPORTANT:

Visitante is NOT a database role or stored database entity.

It represents public/unauthenticated access.

---

## 2. Usuario

The registered user can:

* Registrar gasto
* Interpretar gasto con IA
* Consultar historial
* Ver dashboard
* Consultar gastos
* Corregir categoría
* Ver posibles fugas

---

## 3. Administrador

The administrator can:

* Consultar estadísticas generales
* Gestionar usuarios
* Activar/desactivar usuarios

The administrator must NOT be given unnecessary access to detailed personal financial information.

---

# USE CASES

Inside the system boundary named:

`Sistema FUGA+`

create the following use cases.

## Public access

* Ver información de FUGA+
* Ver cómo funciona
* Registrarse
* Iniciar sesión

## User functionality

* Registrar gasto
* Interpretar gasto con IA
* Consultar historial
* Ver dashboard
* Consultar gastos
* Corregir categoría
* Ver posibles fugas

## Administrator functionality

* Consultar estadísticas generales
* Gestionar usuarios
* Activar/desactivar usuarios

---

# ACTOR RELATIONSHIPS

Connect:

### Visitante

Visitante → Ver información de FUGA+

Visitante → Ver cómo funciona

Visitante → Registrarse

Visitante → Iniciar sesión

### Usuario

Usuario → Registrar gasto

Usuario → Consultar historial

Usuario → Ver dashboard

Usuario → Consultar gastos

Usuario → Corregir categoría

Usuario → Ver posibles fugas

### Administrador

Administrador → Consultar estadísticas generales

Administrador → Gestionar usuarios

Administrador → Activar/desactivar usuarios

---

# INCLUDE / EXTEND RELATIONSHIPS

Use UML `include` or `extend` only when they make logical sense.

Use:

`Registrar gasto` <<include>> `Interpretar gasto con IA`

because the main MVP flow uses AI to interpret a natural-language expense.

Use:

`Registrar gasto` <<include>> `Interpretar gasto con IA`

ONLY if the diagram remains clear.

For category correction, represent:

`Corregir categoría` as an optional action associated with the user and the interpretation process.

If using `extend`, use it appropriately:

`Corregir categoría` <<extend>> `Interpretar gasto con IA`

This represents that the user may correct the category when the AI interpretation is not correct or needs adjustment.

For possible money leaks:

`Ver posibles fugas` is based on previously registered expenses.

If an `include` relationship improves clarity, it may be represented as:

`Ver posibles fugas` <<include>> `Analizar gastos mediante reglas`

However, do NOT introduce unnecessary additional use cases just to make the diagram more complex.

The diagram should remain simple and understandable.

---

# IMPORTANT FUNCTIONAL BOUNDARIES

Do NOT add use cases for:

* Bancos
* Pagos
* Transferencias
* Tarjetas
* Créditos
* Préstamos
* Inversiones
* Asesoría financiera profesional
* Predicción de mercados
* Entrenamiento de modelos propios
* Integraciones bancarias externas
* Notificaciones push avanzadas
* Escaneo avanzado de recibos

These functionalities are outside the FUGA+ MVP.

---

# AI REPRESENTATION

The use case:

`Interpretar gasto con IA`

must be present.

However, do NOT create "OpenAI" as an actor.

The Use Case Diagram should focus on users and system functionality.

OpenAI belongs to the Component Diagram, not this Use Case Diagram.

Therefore:

DO NOT add:

* OpenAI API actor
* MongoDB actor
* Redis actor
* FastAPI actor
* Docker actor
* GitHub actor

Those are architectural/technical elements already represented in the Component Diagram.

---

# MONEY LEAK DETECTION

The use case:

`Ver posibles fugas`

must be present.

Make clear through the use-case name or a small note that the detection is:

`Basada en reglas`

Do NOT represent it as an AI functionality.

Do NOT create a separate AI actor.

The purpose is to show that the user can view possible money leaks generated from registered expense patterns.

---

# ADMINISTRATION

The administrator functionality should be clearly separated from normal user functionality.

Administrator:

* Consultar estadísticas generales
* Gestionar usuarios
* Activar/desactivar usuarios

Do NOT add:

* Ver todos los gastos personales
* Editar personal financial information
* Access bank accounts
* Modify user expenses

unless such functionality is explicitly defined in the project requirements.

---

# UML STRUCTURE

Create a true UML Use Case Diagram.

The structure should be:

ACTORS OUTSIDE THE SYSTEM

↓

SYSTEM BOUNDARY

`Sistema FUGA+`

↓

USE CASES INSIDE THE SYSTEM

Actors must remain outside the system boundary.

Use cases must be represented as UML ovals/use-case shapes.

Use association lines between actors and use cases.

Use UML <<include>> or <<extend>> relationships only where appropriate.

---

# VISUAL ORGANIZATION

The diagram should be visually clean and easy to understand.

Recommended layout:

Left side:

Visitante

Center:

Sistema FUGA+

Inside the system:

Public access use cases near the top.

User functionality in the middle.

Administrator functionality near the bottom.

Right side:

Usuario

Administración can be positioned separately if necessary.

The exact layout may be adjusted to avoid crossing lines.

Avoid unnecessary line crossings.

Do not make the diagram excessively large.

The diagram should be suitable for a university software engineering presentation.

---

# TITLE

Use:

`Diagrama de Casos de Uso — FUGA+`

Optional subtitle:

`Actores y funcionalidades principales del sistema`

All visible text must remain in Spanish.

---

# TECHNOLOGY INFORMATION

Do NOT add technology components to this diagram.

Do NOT show:

* React Native
* TypeScript
* FastAPI
* MongoDB
* Redis
* Docker
* GitHub
* OpenAI API

These belong to the Component Diagram.

The Use Case Diagram focuses on:

Actors + System + Functionalities.

---

# FILE CREATION REQUIREMENTS

The folder already exists:

`docs/diagramas/`

Do NOT create it again.

Create ONLY:

`docs/diagramas/diagrama-casos-uso.drawio`

The file must:

* Be valid Draw.io/diagrams.net XML.
* Be editable.
* Open correctly in diagrams.net.
* Contain the complete UML Use Case Diagram.
* Use Spanish for every visible label.
* Contain exactly the defined actors and relevant use cases.
* Use appropriate UML relationships.

DO NOT create:

* PNG
* JPG
* SVG
* PDF
* Markdown
* Additional `.drawio` files
* Other diagrams
* Documentation files

ONLY create:

`docs/diagramas/diagrama-casos-uso.drawio`

---

# CRITICAL FILESYSTEM INSTRUCTION

The previous component-diagram generation showed XML in the OpenCode response.

Do NOT repeat that behavior.

The goal of this task is NOT to display XML.

The goal is to create the actual file in the repository.

You MUST:

1. Generate the Draw.io XML.
2. Write the XML to:
   `docs/diagramas/diagrama-casos-uso.drawio`
3. Save the file.
4. Verify that the file exists.
5. Verify that the file is not empty.
6. Do not create any other file.
7. Do not finish until the file has been physically written.

Use the project's existing filesystem.

Do not ask the user to manually copy XML.

Do not paste the entire XML into the final response.

---

# FINAL VERIFICATION

Before finishing, verify:

1. `docs/diagramas/` already existed.
2. No new diagram folder was created.
3. `docs/diagramas/diagrama-casos-uso.drawio` exists.
4. The file is not empty.
5. The file contains valid Draw.io XML.
6. The diagram opens as an editable Draw.io diagram.
7. The diagram is a UML Use Case Diagram.
8. All visible text is in Spanish.
9. The actors are:

   * Visitante
   * Usuario
   * Administrador
10. The system boundary is:

* Sistema FUGA+

11. Public functionality is represented.
12. User functionality is represented.
13. Administrator functionality is represented.
14. AI interpretation is represented as a use case.
15. Money-leak detection is represented as rule-based functionality.
16. OpenAI is NOT represented as an actor.
17. MongoDB is NOT represented as an actor.
18. Redis is NOT represented as an actor.
19. FastAPI is NOT represented as an actor.
20. No technologies are unnecessarily included.
21. No excluded banking/payment functionality is included.
22. No additional files were created.

After successful verification, respond only with a short confirmation such as:

`Diagrama de casos de uso creado correctamente en docs/diagramas/diagrama-casos-uso.drawio`
