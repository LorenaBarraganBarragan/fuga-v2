# Task — Create FUGA+ User Story Diagram

Create ONLY this file:

`docs/diagramas/diagrama-historias-usuario.drawio`

Do NOT create additional folders.
Do NOT create any other files.
Do NOT modify any existing files.

## Objective

Create a visual User Story Diagram for the FUGA+ mobile application.

The diagram must organize the main user stories according to the actors and main functionality of the application.

The diagram must be editable in Draw.io / diagrams.net and must use valid Draw.io XML.

## IMPORTANT LANGUAGE REQUIREMENT

The instructions in this prompt are written in English, but ALL VISIBLE TEXT INSIDE THE DIAGRAM MUST BE IN SPANISH.

The diagram title must be:

**Diagrama de Historias de Usuario — FUGA+**

Subtitle:

**Funcionalidades principales de la aplicación móvil**

## Project Context

FUGA+ is a mobile application designed to help young people and students identify possible money leaks by recording and analyzing their expenses.

The user can enter expenses using natural language, for example:

"Hoy gasté $8.000 en un taxi"

The application extracts relevant information such as:

- Valor
- Categoría
- Descripción

The application stores the expense history and analyzes recurring spending patterns using business rules to identify possible money leaks.

The MVP focuses on expense registration, expense history, categorization, dashboard information, and possible money-leak detection.

## Actors

Create the following actors:

### Usuario

The main authenticated user of FUGA+.

### Administrador

The administrative user responsible for managing categories and administrative information.

### Visitante

An unauthenticated visitor who can access the public part of the application.

Do NOT create technical actors such as:

- OpenAI
- MongoDB
- Redis
- FastAPI
- React Native
- JWT
- Docker
- GitHub

These are technologies or infrastructure and must not appear as actors.

## User Stories

Create the following user stories.

### US01 — Registrarse

**Como usuario, quiero registrarme en FUGA+ para crear una cuenta y guardar mis gastos.**

Actor:

Usuario

Priority:

Must

### US02 — Iniciar sesión

**Como usuario, quiero iniciar sesión para acceder de forma segura a mi información financiera.**

Actor:

Usuario

Priority:

Must

### US03 — Registrar gasto

**Como usuario, quiero registrar un gasto escribiendo una descripción en lenguaje natural para guardar rápidamente lo que gasté.**

Actor:

Usuario

Priority:

Must

Example:

"Hoy gasté $8.000 en un taxi"

### US04 — Interpretar gasto

**Como usuario, quiero que el sistema interprete el texto de mi gasto para identificar el valor, la categoría y la descripción.**

Actor:

Usuario

Priority:

Must

This functionality is related to the expense analysis logic.

Do not represent this as a separate external actor.

### US05 — Consultar historial

**Como usuario, quiero consultar mi historial de gastos para conocer en qué he utilizado mi dinero.**

Actor:

Usuario

Priority:

Must

### US06 — Categorizar gasto

**Como usuario, quiero que mis gastos estén organizados por categorías para entender mejor mis hábitos de consumo.**

Actor:

Usuario

Priority:

Must

Examples:

- Transporte
- Alimentación
- Entretenimiento
- Compras
- Otros

### US07 — Consultar dashboard

**Como usuario, quiero visualizar un resumen de mis gastos para conocer mis principales categorías y valores gastados.**

Actor:

Usuario

Priority:

Should

### US08 — Detectar posible fuga

**Como usuario, quiero recibir alertas sobre posibles fugas de dinero para identificar gastos repetitivos que pueden estar afectando mi presupuesto.**

Actor:

Usuario

Priority:

Must

The detection is based on business rules and expense history.

Do NOT describe it as an AI prediction.

### US09 — Consultar posibles fugas

**Como usuario, quiero consultar las posibles fugas detectadas para entender qué gastos repetitivos debo revisar.**

Actor:

Usuario

Priority:

Should

### US10 — Gestionar perfil

**Como usuario, quiero actualizar mis datos personales para mantener mi información actualizada.**

Actor:

Usuario

Priority:

Could

### US11 — Gestionar categorías

**Como administrador, quiero crear, actualizar y consultar categorías para mantener organizada la clasificación de gastos.**

Actor:

Administrador

Priority:

Should

### US12 — Acceder a información pública

**Como visitante, quiero consultar información general sobre FUGA+ para conocer el propósito de la aplicación antes de registrarme.**

Actor:

Visitante

Priority:

Could

## Diagram Structure

Create a visual hierarchy using:

**Actor → Epic/Module → User Stories**

Organize the diagram into the following main functional areas:

### 1. Autenticación y acceso

Include:

- US01 — Registrarse
- US02 — Iniciar sesión
- US10 — Gestionar perfil
- US12 — Acceder a información pública

### 2. Gestión de gastos

Include:

- US03 — Registrar gasto
- US04 — Interpretar gasto
- US05 — Consultar historial
- US06 — Categorizar gasto

### 3. Análisis financiero

Include:

- US07 — Consultar dashboard
- US08 — Detectar posible fuga
- US09 — Consultar posibles fugas

### 4. Administración

Include:

- US11 — Gestionar categorías

## Visual Requirements

Use a clean UML-like or Agile user-story visualization.

Each user story must be represented as a separate visual element.

Each story element must contain:

- Story ID
- Short title
- Full user story
- Priority

Example:

`US03`

`Registrar gasto`

`Como usuario, quiero registrar un gasto escribiendo una descripción en lenguaje natural para guardar rápidamente lo que gasté.`

`Prioridad: Must`

Do not make the story elements excessively large.

Use containers or sections to visually separate:

- Autenticación y acceso
- Gestión de gastos
- Análisis financiero
- Administración

Clearly distinguish the actors from the user stories.

Use connectors to show which actor is associated with each story.

## Priority Representation

Represent priorities visually using labels:

- `Must`
- `Should`
- `Could`

Do NOT use numerical scores.

Do NOT invent additional priorities.

## Important Restrictions

Do NOT add user stories that are not specified in this prompt.

Do NOT add payment functionality.

Do NOT add bank integrations.

Do NOT add voice input.

Do NOT add financial transactions.

Do NOT add cryptocurrency.

Do NOT add social networking.

Do NOT add external APIs as user stories.

Do NOT represent OpenAI as an actor.

Do NOT represent MongoDB as an actor.

## File Requirements

Physically create:

`docs/diagramas/diagrama-historias-usuario.drawio`

The file must:

- Be valid Draw.io XML.
- Be editable in Draw.io / diagrams.net.
- Contain the title and subtitle.
- Contain all 12 user stories.
- Contain the three actors:
  - Usuario
  - Administrador
  - Visitante
- Contain the four functional areas.
- Show the relationship between actors and user stories.
- Show the priority of each story.
- Use Spanish for all visible diagram text.

## Mandatory Verification

After creating the file:

1. Verify that `docs/diagramas/diagrama-historias-usuario.drawio` physically exists.
2. Verify that the file is not empty.
3. Verify that it contains valid Draw.io XML.
4. Verify that all 12 user stories exist:
   - US01
   - US02
   - US03
   - US04
   - US05
   - US06
   - US07
   - US08
   - US09
   - US10
   - US11
   - US12
5. Verify that the three actors exist:
   - Usuario
   - Administrador
   - Visitante
6. Verify that the four functional areas exist.
7. Verify that the title is:
   `Diagrama de Historias de Usuario — FUGA+`
8. Verify that all visible text inside the diagram is in Spanish.
9. Do not create any other file.
10. Do not modify any other project file.

## Final Response

After successfully creating and verifying the file, respond only with a short confirmation that the file was created and verified.